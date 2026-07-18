from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.llm.embeddings import DeterministicEmbeddingService, NvidiaEmbedding, OpenRouterEmbedding
from app.llm.errors import RerankProviderError
from app.models.enums import DocumentTier
from app.services.retrieval_service import (
    RetrievalService,
    RetrievedChunk,
    _fetch_bm25,
    _fetch_candidates,
    _mmr_rerank,
    _rerank,
    _vec_cosine,
    build_embedding_service,
    rrf_fuse,
)


def _make_chunk(cosine_sim: float, embedding: list[float] | None = None) -> RetrievedChunk:
    return RetrievedChunk(
        id=uuid4(),
        document_id=uuid4(),
        content="test content",
        document_tier=DocumentTier.COMMUNITY,
        subtype=None,
        section_title=None,
        page_number=None,
        chunk_order=1,
        cosine_sim=cosine_sim,
        final_score=cosine_sim,
        _embedding=embedding,
    )


def test_vec_cosine_identical_vectors() -> None:
    v = [1.0, 0.0, 0.0]
    assert abs(_vec_cosine(v, v) - 1.0) < 1e-9


def test_vec_cosine_orthogonal_vectors() -> None:
    a = [1.0, 0.0]
    b = [0.0, 1.0]
    assert abs(_vec_cosine(a, b)) < 1e-9


def test_vec_cosine_none_returns_zero() -> None:
    assert _vec_cosine(None, [1.0, 0.0]) == 0.0
    assert _vec_cosine([1.0, 0.0], None) == 0.0


def test_mmr_rerank_returns_at_most_k() -> None:
    candidates = [_make_chunk(0.9 - i * 0.05) for i in range(10)]
    query_vec = [1.0, 0.0]
    result = _mmr_rerank(candidates, query_vec, lam=0.7, k=3)
    assert len(result) <= 3


def test_mmr_rerank_penalises_duplicates() -> None:
    dim = 4
    embedding_svc = DeterministicEmbeddingService(dim)
    same_vec = embedding_svc.encode(["hello"])[0]
    other_vec = embedding_svc.encode(["completely different topic XYZ"])[0]

    dup1 = _make_chunk(0.9, embedding=same_vec)
    dup2 = _make_chunk(0.85, embedding=same_vec)
    diverse = _make_chunk(0.7, embedding=other_vec)
    candidates = [dup1, dup2, diverse]

    query_vec = [1.0] + [0.0] * (dim - 1)
    result = _mmr_rerank(candidates, query_vec, lam=0.7, k=2)
    result_ids = {c.id for c in result}

    assert len(result) == 2
    assert dup1.id in result_ids
    assert diverse.id in result_ids or dup2.id in result_ids


def test_mmr_rerank_empty_candidates() -> None:
    result = _mmr_rerank([], [1.0, 0.0], lam=0.7, k=5)
    assert result == []


def test_retrieval_service_init() -> None:
    svc = RetrievalService(DeterministicEmbeddingService(1024))
    assert svc._embedding is not None


@pytest.mark.asyncio
async def test_fetch_candidates_filters_by_document_ids_when_given() -> None:
    doc_id = uuid4()
    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = []
    mock_session = AsyncMock()
    mock_session.execute = AsyncMock(return_value=mock_result)

    await _fetch_candidates(
        mock_session,
        uuid4(),
        "[0.1,0.2]",
        ["knowledge"],
        40,
        document_ids=[doc_id],
    )

    mock_session.execute.assert_awaited_once()
    call_args = mock_session.execute.call_args
    compiled_sql = str(call_args.args[0])
    bound_params = call_args.args[1]

    assert "document_id = ANY(:document_ids)" in compiled_sql
    assert bound_params["document_ids"] == [str(doc_id)]


@pytest.mark.asyncio
async def test_fetch_candidates_no_document_filter_when_none() -> None:
    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = []
    mock_session = AsyncMock()
    mock_session.execute = AsyncMock(return_value=mock_result)

    await _fetch_candidates(
        mock_session,
        uuid4(),
        "[0.1,0.2]",
        ["knowledge"],
        40,
        document_ids=None,
    )

    mock_session.execute.assert_awaited_once()
    call_args = mock_session.execute.call_args
    compiled_sql = str(call_args.args[0])
    bound_params = call_args.args[1]

    assert "document_id = ANY(:document_ids)" not in compiled_sql
    assert "document_ids" not in bound_params


def _settings(**overrides) -> SimpleNamespace:
    base = dict(
        openrouter_api_key=None,
        openrouter_base_url="https://openrouter.ai/api/v1",
        openrouter_embedding_model="openai/text-embedding-3-small",
        openrouter_rerank_model="cohere/rerank-v3.5",
        nvidia_api_key=None,
        nvidia_base_url="https://integrate.api.nvidia.com/v1",
        nvidia_rerank_base="https://ai.api.nvidia.com/v1/retrieval",
        embedding_model="nvidia/nv-embedqa-e5-v5",
        embedding_dim=1536,
        rerank_model="nvidia/llama-nemotron-rerank-vl-1b-v2",
        rerank_enabled=True,
        tutor_mmr_lambda=0.7,
    )
    base.update(overrides)
    return SimpleNamespace(**base)


def test_build_embedding_service_prefers_openrouter() -> None:
    svc = build_embedding_service(_settings(openrouter_api_key="or-key", nvidia_api_key="nv-key"))
    assert isinstance(svc, OpenRouterEmbedding)
    assert svc.model == "openai/text-embedding-3-small"
    assert svc.dimension == 1536


def test_build_embedding_service_nvidia_when_no_openrouter_key() -> None:
    svc = build_embedding_service(_settings(nvidia_api_key="nv-key"))
    assert isinstance(svc, NvidiaEmbedding)


def test_build_embedding_service_offline_stub_without_keys() -> None:
    svc = build_embedding_service(_settings())
    assert isinstance(svc, DeterministicEmbeddingService)
    assert svc.dimension == 1536


def test_rerank_uses_openrouter_order_and_attaches_scores(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict = {}

    class FakeRerank:
        def __init__(self, **kwargs) -> None:
            captured["kwargs"] = kwargs

        def rank_scored(self, query: str, passages: list[str]) -> list[tuple[int, float]]:
            captured["query"] = query
            return [(2, 0.91), (0, 0.55), (1, 0.12)]

    monkeypatch.setattr("app.llm.rerank.OpenRouterRerank", FakeRerank)
    candidates = [_make_chunk(0.9), _make_chunk(0.8), _make_chunk(0.7)]

    result = _rerank("q", candidates, [1.0, 0.0], _settings(openrouter_api_key="or-key"), k=2)

    # _rerank returns the full ranked pool (search() trims to k); order follows the
    # reranker and each chunk carries its cross-encoder relevance score.
    assert [c.id for c in result] == [candidates[2].id, candidates[0].id, candidates[1].id]
    assert [c.rerank_score for c in result] == [0.91, 0.55, 0.12]
    assert captured["kwargs"]["model"] == "cohere/rerank-v3.5"


def test_rerank_openrouter_error_propagates(monkeypatch: pytest.MonkeyPatch) -> None:
    class FailingRerank:
        def __init__(self, **kwargs) -> None:
            pass

        def rank_scored(self, query: str, passages: list[str]) -> list[tuple[int, float]]:
            raise RerankProviderError()

    monkeypatch.setattr("app.llm.rerank.OpenRouterRerank", FailingRerank)

    with pytest.raises(RerankProviderError):
        _rerank("q", [_make_chunk(0.9)], [1.0, 0.0], _settings(openrouter_api_key="or-key"), k=1)


def test_rerank_without_keys_uses_mmr() -> None:
    chunk = _make_chunk(0.9, embedding=[1.0, 0.0])
    result = _rerank("q", [chunk], [1.0, 0.0], _settings(), k=1)
    assert result == [chunk]


def test_rerank_openrouter_disabled_uses_mmr() -> None:
    chunk = _make_chunk(0.9, embedding=[1.0, 0.0])
    result = _rerank("q", [chunk], [1.0, 0.0], _settings(openrouter_api_key="or-key", rerank_enabled=False), k=1)
    assert result == [chunk]


# --- hybrid search: RRF fusion + BM25 lexical branch ---------------------------


def test_rrf_fuse_prefers_chunks_in_both_lists() -> None:
    both = _make_chunk(0.5)
    dense_only = _make_chunk(0.9)  # rank 1 in dense but only appears once
    lexical_only = _make_chunk(0.4)

    dense = [dense_only, both]  # both at rank 2 in dense
    lexical = [both, lexical_only]  # both at rank 1 in lexical

    fused, scores = rrf_fuse(dense, lexical)

    # `both` appears in both lists → summed RRF score → ranked first despite lower cosine.
    assert fused[0].id == both.id
    assert scores[both.id] > scores[dense_only.id]
    assert scores[both.id] > scores[lexical_only.id]
    # Every unique chunk is present exactly once.
    assert sorted(str(c.id) for c in fused) == sorted(
        {str(dense_only.id), str(both.id), str(lexical_only.id)}
    )


def test_rrf_fuse_empty_lists() -> None:
    fused, scores = rrf_fuse([], [])
    assert fused == []
    assert scores == {}


def test_rrf_fuse_keeps_dense_object_for_shared_id() -> None:
    # A chunk seen in both lists keeps the dense object (carries cosine + embedding).
    shared_id = uuid4()
    dense_obj = _make_chunk(0.8, embedding=[1.0, 0.0])
    dense_obj.id = shared_id
    lexical_obj = _make_chunk(0.1, embedding=None)
    lexical_obj.id = shared_id

    fused, _ = rrf_fuse([dense_obj], [lexical_obj])
    assert len(fused) == 1
    assert fused[0]._embedding == [1.0, 0.0]


@pytest.mark.asyncio
async def test_fetch_bm25_builds_or_query_and_document_filter() -> None:
    doc_id = uuid4()
    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = []
    mock_session = AsyncMock()
    mock_session.scalar = AsyncMock(return_value="'union' | 'find'")
    mock_session.execute = AsyncMock(return_value=mock_result)

    await _fetch_bm25(
        mock_session,
        uuid4(),
        "union find",
        "[0.1,0.2]",
        ["knowledge"],
        40,
        document_ids=[doc_id],
    )

    # Disjunctive query derived via plainto_tsquery then '&' -> '|'.
    scalar_sql = str(mock_session.scalar.call_args.args[0])
    assert "plainto_tsquery" in scalar_sql
    assert "'&', '|'" in scalar_sql

    exec_args = mock_session.execute.call_args
    compiled_sql = str(exec_args.args[0])
    params = exec_args.args[1]
    assert "to_tsvector('simple', content)" in compiled_sql
    assert "document_id = ANY(:document_ids)" in compiled_sql
    assert params["or_query"] == "'union' | 'find'"
    assert params["document_ids"] == [str(doc_id)]


@pytest.mark.asyncio
async def test_fetch_bm25_returns_empty_when_query_has_no_lexemes() -> None:
    mock_session = AsyncMock()
    mock_session.scalar = AsyncMock(return_value="")  # all stop words / punctuation
    mock_session.execute = AsyncMock()

    rows = await _fetch_bm25(mock_session, uuid4(), "the a of", "[0.1]", ["knowledge"], 40)

    assert rows == []
    mock_session.execute.assert_not_called()


def _hybrid_settings(**overrides) -> SimpleNamespace:
    base = dict(
        tutor_sim_threshold=0.0,
        tutor_rerank_threshold=0.0,
        tutor_tier_boost=1.15,
        tutor_hybrid_enabled=True,
        tutor_mmr_lambda=0.7,
    )
    base.update(overrides)
    return SimpleNamespace(**base)


def _row(cid, cosine_sim, content="content", tier="community"):
    return {
        "id": cid,
        "document_id": uuid4(),
        "content": content,
        "document_tier": tier,
        "subtype": None,
        "section_title": None,
        "page_number": None,
        "chunk_order": 1,
        "embedding": None,
        "cosine_sim": cosine_sim,
    }


@pytest.mark.asyncio
async def test_search_hybrid_queries_bm25_and_fuses(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.services.retrieval_service as rs

    dense_id, shared_id, lexical_id = uuid4(), uuid4(), uuid4()
    dense_rows = [_row(dense_id, 0.9), _row(shared_id, 0.6)]
    bm25_rows = [_row(shared_id, 0.6), _row(lexical_id, 0.2)]

    monkeypatch.setattr(rs, "get_settings", lambda: _hybrid_settings(), raising=False)
    monkeypatch.setattr(rs, "_fetch_candidates", AsyncMock(return_value=dense_rows))
    fetch_bm25 = AsyncMock(return_value=bm25_rows)
    monkeypatch.setattr(rs, "_fetch_bm25", fetch_bm25)
    monkeypatch.setattr(rs, "_fetch_net_votes", AsyncMock(return_value={}))
    # Reranker is a no-op identity here so we can assert on the fused candidate pool.
    monkeypatch.setattr(rs, "_rerank", lambda q, cands, qv, s, k: cands)

    svc = RetrievalService(DeterministicEmbeddingService(8))
    result = await svc.search(AsyncMock(), uuid4(), "union find", k=8)

    fetch_bm25.assert_awaited_once()
    ids = {c.id for c in result}
    # Fused pool is the union of both sources; the shared chunk appears once.
    assert ids == {dense_id, shared_id, lexical_id}


@pytest.mark.asyncio
async def test_search_falls_back_to_dense_when_bm25_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.services.retrieval_service as rs

    dense_id = uuid4()
    monkeypatch.setattr(rs, "get_settings", lambda: _hybrid_settings(), raising=False)
    monkeypatch.setattr(rs, "_fetch_candidates", AsyncMock(return_value=[_row(dense_id, 0.9)]))
    monkeypatch.setattr(rs, "_fetch_bm25", AsyncMock(return_value=[]))  # no lexical matches
    monkeypatch.setattr(rs, "_fetch_net_votes", AsyncMock(return_value={}))
    monkeypatch.setattr(rs, "_rerank", lambda q, cands, qv, s, k: cands)

    svc = RetrievalService(DeterministicEmbeddingService(8))
    result = await svc.search(AsyncMock(), uuid4(), "xyzzy", k=8)

    assert {c.id for c in result} == {dense_id}


@pytest.mark.asyncio
async def test_search_flag_off_never_queries_bm25(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.services.retrieval_service as rs

    dense_id = uuid4()
    monkeypatch.setattr(rs, "get_settings", lambda: _hybrid_settings(tutor_hybrid_enabled=False), raising=False)
    monkeypatch.setattr(rs, "_fetch_candidates", AsyncMock(return_value=[_row(dense_id, 0.9)]))
    fetch_bm25 = AsyncMock(return_value=[])
    monkeypatch.setattr(rs, "_fetch_bm25", fetch_bm25)
    monkeypatch.setattr(rs, "_fetch_net_votes", AsyncMock(return_value={}))
    monkeypatch.setattr(rs, "_rerank", lambda q, cands, qv, s, k: cands)

    svc = RetrievalService(DeterministicEmbeddingService(8))
    result = await svc.search(AsyncMock(), uuid4(), "union find", k=8)

    fetch_bm25.assert_not_called()
    assert {c.id for c in result} == {dense_id}
