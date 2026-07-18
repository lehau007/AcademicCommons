from __future__ import annotations

import asyncio
import math
import re
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.llm.embeddings import (
    DeterministicEmbeddingService,
    EmbeddingService,
    NvidiaEmbedding,
    OpenRouterEmbedding,
)
from app.models.enums import DocumentTier

RRF_K = 60  # standard Reciprocal Rank Fusion constant


@dataclass
class RetrievedChunk:
    id: UUID
    document_id: UUID
    content: str
    document_tier: DocumentTier
    subtype: str | None
    section_title: str | None
    page_number: int | None
    chunk_order: int
    cosine_sim: float
    final_score: float
    rerank_score: float | None = None
    _embedding: list[float] | None = None


class RetrievalService:
    def __init__(self, embedding_service: EmbeddingService) -> None:
        self._embedding = embedding_service

    async def search(
        self,
        session: AsyncSession,
        course_id: UUID,
        query: str,
        namespaces: list[str] | None = None,
        k: int = 8,
        prefetch_k: int = 40,
        document_ids: list[UUID] | None = None,
    ) -> list[RetrievedChunk]:
        settings = get_settings()
        effective_namespaces = namespaces or ["knowledge"]

        query_vec = (await asyncio.to_thread(self._embedding.encode, [query], input_type="query"))[0]
        query_vec_str = "[" + ",".join(str(v) for v in query_vec) + "]"

        dense_rows = await _fetch_candidates(
            session, course_id, query_vec_str, effective_namespaces, prefetch_k, document_ids
        )
        dense = [_row_to_chunk(row) for row in dense_rows]

        # Drop weak matches below the configured cosine floor. Returning nothing here is
        # intentional for out-of-scope questions: the agent then says the material does not
        # cover the topic instead of citing low-relevance noise. This is a dense-similarity
        # gate, so it applies ONLY to the dense branch — lexical candidates are not gated by
        # cosine (gating them by dense cosine would defeat the point of hybrid retrieval).
        if settings.tutor_sim_threshold > 0.0:
            dense = [c for c in dense if c.cosine_sim >= settings.tutor_sim_threshold]

        # Hybrid retrieval: fuse the dense list with a BM25-style lexical branch via
        # Reciprocal Rank Fusion, then let the reranker order the fused pool. Falls back to
        # dense-only when the lexical branch returns nothing (e.g. an all-stop-word query) so
        # retrieval never breaks. Disabling the flag restores the pure-dense behavior.
        if getattr(settings, "tutor_hybrid_enabled", True):
            bm25_rows = await _fetch_bm25(
                session, course_id, query, query_vec_str, effective_namespaces, prefetch_k, document_ids
            )
            lexical = [_row_to_chunk(row) for row in bm25_rows]
            if lexical:
                fused, _ = rrf_fuse(dense, lexical)
                candidates = fused[:prefetch_k]
            else:
                candidates = dense
        else:
            candidates = dense

        if not candidates:
            return []

        # Table-of-contents / outline / agenda chunks are keyword-rich but hold no answer
        # content, so they pollute precision. Drop them before reranking, but never starve
        # retrieval: if too few substantive chunks remain, top back up by cosine.
        non_outline = [c for c in candidates if not _is_outline_chunk(c.section_title, c.content)]
        if len(non_outline) < len(candidates):
            if len(non_outline) < k:
                dropped = [c for c in candidates if _is_outline_chunk(c.section_title, c.content)]
                dropped.sort(key=lambda c: c.cosine_sim, reverse=True)
                non_outline += dropped[: k - len(non_outline)]
            candidates = non_outline

        ranked = await asyncio.to_thread(_rerank, query, candidates, query_vec, settings, k)

        # Dynamic-k: when the reranker returned relevance scores, drop chunks below the
        # configured floor so out-of-scope questions surface few/no chunks instead of
        # padding top-k with the "least irrelevant" matches. Only active when enabled and
        # scores are present (offline/MMR fallback has none, so behavior is unchanged).
        rerank_floor = getattr(settings, "tutor_rerank_threshold", 0.0)
        if rerank_floor > 0.0 and any(c.rerank_score is not None for c in ranked):
            ranked = [c for c in ranked if (c.rerank_score or 0.0) >= rerank_floor]

        doc_ids = list({c.document_id for c in ranked})
        net_votes = await _fetch_net_votes(session, doc_ids)
        course_avg = (sum(net_votes.values()) / len(net_votes)) if net_votes else 1.0

        for chunk in ranked:
            # Rank on the cross-encoder relevance when available; fall back to cosine only
            # for the offline/MMR path. Tier boost and community votes are secondary nudges,
            # not the primary signal (previously cosine overrode the reranker's ordering).
            base = chunk.rerank_score if chunk.rerank_score is not None else chunk.cosine_sim
            score = base
            if chunk.document_tier == DocumentTier.OFFICIAL:
                score *= settings.tutor_tier_boost
            nv = net_votes.get(chunk.document_id, 0)
            vote_factor = max(-0.5, min(0.5, nv / max(abs(course_avg), 1.0)))
            score *= 1.0 + vote_factor
            chunk.final_score = score

        ranked.sort(key=lambda c: c.final_score, reverse=True)
        return ranked[:k]


def _rerank(
    query: str,
    candidates: list[RetrievedChunk],
    query_vec: list[float],
    settings: Any,
    k: int,
) -> list[RetrievedChunk]:
    """Reorder candidates via the top-tier reranker.

    With an OpenRouter key the OpenRouter reranker is authoritative: failures
    raise ``RerankProviderError`` (surfaced to the UI) instead of silently
    falling back, because a silent quality drop is worse than a visible error.
    Without an OpenRouter key the legacy chain applies: NVIDIA reranker when
    configured (errors fall back to local MMR), else local MMR, so offline
    tests and degraded deployments keep working.
    """
    if not candidates:
        return []

    if getattr(settings, "openrouter_api_key", None) and getattr(settings, "rerank_enabled", False):
        import app.llm.rerank as rerank_module

        service = rerank_module.OpenRouterRerank(
            api_key=settings.openrouter_api_key,
            base_url=settings.openrouter_base_url,
            model=settings.openrouter_rerank_model,
        )
        scored = service.rank_scored(query, [c.content for c in candidates])
        reranked: list[RetrievedChunk] = []
        for idx, rerank_score in scored:
            if 0 <= idx < len(candidates):
                candidates[idx].rerank_score = rerank_score
                reranked.append(candidates[idx])
        # Return the full ranked pool with scores attached; search() applies the dynamic-k
        # floor and trims to k so the relevance floor is enforced before truncation.
        return reranked

    api_key = getattr(settings, "nvidia_api_key", None)
    if api_key and getattr(settings, "rerank_enabled", False):
        try:
            from app.llm.rerank import RerankService

            rerank_url = f"{settings.nvidia_rerank_base.rstrip('/')}/{settings.rerank_model}/reranking"
            service = RerankService(
                api_key=api_key,
                url=rerank_url,
                model=settings.rerank_model,
            )
            order = service.rank(query, [c.content for c in candidates])
            reranked = [candidates[i] for i in order if 0 <= i < len(candidates)]
            if reranked:
                return reranked[:k]
        except Exception:
            pass

    return _mmr_rerank(candidates, query_vec, lam=settings.tutor_mmr_lambda, k=k)


# Slide titles that mark a navigational / agenda page rather than answer content.
# "roadmap" is deliberately excluded: a suggested learning path beyond the course is
# genuine content we want to keep retrievable.
_OUTLINE_TITLES = {
    "learning points", "outline", "contents", "table of contents", "mục lục",
    "agenda", "overview", "objectives", "learning objectives", "topics",
    "syllabus", "course outline",
}


def _is_outline_chunk(section_title: str | None, content: str) -> bool:
    """Detect table-of-contents / outline / agenda chunks (navigational, not answer-bearing).

    Conservative by design: high precision on the 'outline' label so we never drop a
    substantive content chunk. A false negative (a missed outline) only leaves retrieval
    slightly noisier; a false positive would delete real material. In particular we do
    NOT flag on bullet density alone — CS lecture slides carry real content as bullets.
    """
    if (section_title or "").strip().lower() in _OUTLINE_TITLES:
        return True
    lines = [ln.strip() for ln in (content or "").splitlines() if ln.strip()]
    if len(lines) < 3:
        return False
    prose = sum(1 for ln in lines if ln.endswith((".", ":")) and len(ln.split()) > 8)
    # A list that is mostly numbered section references ("- 2.1. Union", "- 3. The MST"),
    # with no prose sentences: a table of contents, not explanatory content.
    numbered = sum(1 for ln in lines if re.match(r"^[-*•]?\s*\d+(\.\d+)*\.\s+\S", ln))
    if numbered >= 3 and numbered / len(lines) >= 0.6 and prose == 0:
        return True
    return False


def _mmr_rerank(candidates: list[RetrievedChunk], query_vec: list[float], lam: float, k: int) -> list[RetrievedChunk]:
    if not candidates:
        return []

    sorted_candidates = sorted(candidates, key=lambda c: c.cosine_sim, reverse=True)
    selected: list[RetrievedChunk] = [sorted_candidates[0]]
    remaining = sorted_candidates[1:]

    while len(selected) < k and remaining:
        best_score = float("-inf")
        best_idx = 0

        for i, candidate in enumerate(remaining):
            sim_to_query = candidate.cosine_sim
            max_sim_to_selected = max(
                _vec_cosine(candidate._embedding, s._embedding) for s in selected
            )
            mmr_score = lam * sim_to_query - (1.0 - lam) * max_sim_to_selected
            if mmr_score > best_score:
                best_score = mmr_score
                best_idx = i

        selected.append(remaining.pop(best_idx))

    return selected


def _vec_cosine(a: list[float] | None, b: list[float] | None) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b, strict=False))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


def _parse_vec(raw: Any) -> list[float] | None:
    if raw is None:
        return None
    if isinstance(raw, list):
        return [float(v) for v in raw]
    if isinstance(raw, str):
        stripped = raw.strip().lstrip("[").rstrip("]")
        if not stripped:
            return []
        return [float(v) for v in stripped.split(",")]
    return None


def _row_to_chunk(row: Any) -> RetrievedChunk:
    return RetrievedChunk(
        id=UUID(str(row["id"])),
        document_id=UUID(str(row["document_id"])),
        content=str(row["content"]),
        document_tier=DocumentTier(str(row["document_tier"])),
        subtype=row["subtype"],
        section_title=row["section_title"],
        page_number=row["page_number"],
        chunk_order=int(row["chunk_order"]),
        cosine_sim=float(row["cosine_sim"]),
        final_score=float(row["cosine_sim"]),
        _embedding=_parse_vec(row["embedding"]),
    )


def rrf_fuse(
    dense: list[RetrievedChunk],
    lexical: list[RetrievedChunk],
    rrf_k: int = RRF_K,
) -> tuple[list[RetrievedChunk], dict[UUID, float]]:
    """Fuse two ranked candidate lists via Reciprocal Rank Fusion.

    Each list is assumed already sorted best-first. Returns (unique chunks sorted by
    fused score desc, {chunk_id: fused_score}). A chunk present in both lists has its
    scores summed, so it outranks chunks seen in only one list. The kept object prefers
    the dense one (it carries cosine + embedding), which we saw first.
    """
    scores: dict[UUID, float] = {}
    objs: dict[UUID, RetrievedChunk] = {}
    for ranked in (dense, lexical):
        for rank, chunk in enumerate(ranked, start=1):
            scores[chunk.id] = scores.get(chunk.id, 0.0) + 1.0 / (rrf_k + rank)
            objs.setdefault(chunk.id, chunk)
    fused = sorted(objs.values(), key=lambda c: scores[c.id], reverse=True)
    return fused, scores


async def _fetch_candidates(
    session: AsyncSession,
    course_id: UUID,
    query_vec_str: str,
    namespaces: list[str],
    prefetch_k: int,
    document_ids: list[UUID] | None = None,
) -> list[Any]:
    document_filter_sql = ""
    params: dict[str, Any] = {
        "course_id": str(course_id),
        "query_vec": query_vec_str,
        "namespaces": namespaces,
        "prefetch_k": prefetch_k,
    }
    if document_ids:
        document_filter_sql = "AND (document_id = ANY(:document_ids))"
        params["document_ids"] = [str(d) for d in document_ids]

    result = await session.execute(
        text(
            f"""
            SELECT id, document_id, content, document_tier, subtype,
                   section_title, page_number, chunk_order, embedding,
                   1 - (embedding <=> CAST(:query_vec AS vector)) AS cosine_sim
            FROM document_chunks
            WHERE course_id = :course_id
              AND rag_namespace::text = ANY(:namespaces)
              AND embedding IS NOT NULL
              {document_filter_sql}
            ORDER BY embedding <=> CAST(:query_vec AS vector)
            LIMIT :prefetch_k
            """
        ),
        params,
    )
    return result.mappings().all()  # type: ignore[return-value]


async def _fetch_bm25(
    session: AsyncSession,
    course_id: UUID,
    query: str,
    query_vec_str: str,
    namespaces: list[str],
    prefetch_k: int,
    document_ids: list[UUID] | None = None,
) -> list[Any]:
    """Lexical candidates via PostgreSQL full-text ``ts_rank`` ('simple' config).

    Uses DISJUNCTIVE (OR) matching: a chunk matching ANY query term is a candidate,
    ranked by ts_rank. This mirrors how BM25/keyword retrieval works — plainto_tsquery's
    default AND would require every token of a paraphrased question in one chunk and return
    almost nothing. We derive the OR-query by lexemizing with plainto_tsquery (handles
    stop-word/tokenization) then swapping '&' for '|'. 'simple' (no stemming/stopwords) is
    used because the corpus is mixed Vietnamese + English.

    ``cosine_sim`` is computed per row so fused chunks carry the same metadata as dense
    ones. Returns rows ordered by descending lexical rank; empty list when the query has no
    lexemes. Speed relies on a GIN index on ``to_tsvector('simple', content)`` (migration).
    """
    or_query = await session.scalar(
        text("SELECT replace(plainto_tsquery('simple', :query)::text, '&', '|')"),
        {"query": query},
    )
    if not or_query:  # query had no lexemes (all stop words / punctuation)
        return []

    document_filter_sql = ""
    params: dict[str, Any] = {
        "course_id": str(course_id),
        "or_query": or_query,
        "query_vec": query_vec_str,
        "namespaces": namespaces,
        "prefetch_k": prefetch_k,
    }
    if document_ids:
        document_filter_sql = "AND (document_id = ANY(:document_ids))"
        params["document_ids"] = [str(d) for d in document_ids]

    result = await session.execute(
        text(
            f"""
            SELECT id, document_id, content, document_tier, subtype,
                   section_title, page_number, chunk_order, embedding,
                   1 - (embedding <=> CAST(:query_vec AS vector)) AS cosine_sim,
                   ts_rank(to_tsvector('simple', content),
                           to_tsquery('simple', :or_query)) AS bm25_score
            FROM document_chunks
            WHERE course_id = :course_id
              AND rag_namespace::text = ANY(:namespaces)
              AND embedding IS NOT NULL
              AND to_tsvector('simple', content) @@ to_tsquery('simple', :or_query)
              {document_filter_sql}
            ORDER BY bm25_score DESC
            LIMIT :prefetch_k
            """
        ),
        params,
    )
    return result.mappings().all()  # type: ignore[return-value]


async def _fetch_net_votes(session: AsyncSession, doc_ids: list[UUID]) -> dict[UUID, int]:
    if not doc_ids:
        return {}
    result = await session.execute(
        text(
            """
            SELECT document_id,
                   SUM(CASE WHEN vote='up' THEN 1 WHEN vote='down' THEN -1 ELSE 0 END) AS net_votes
            FROM community_votes
            WHERE document_id = ANY(:doc_ids)
            GROUP BY document_id
            """
        ),
        {"doc_ids": [str(d) for d in doc_ids]},
    )
    return {UUID(str(row["document_id"])): int(row["net_votes"]) for row in result.mappings()}


def get_retrieval_service(settings: Any = None) -> RetrievalService:
    from app.config import get_settings as _get_settings

    s = settings or _get_settings()
    return RetrievalService(build_embedding_service(s))


def build_embedding_service(settings: Any) -> EmbeddingService:
    """Return the highest-tier embedder with credentials: OpenRouter → NVIDIA → offline stub."""
    if getattr(settings, "openrouter_api_key", None):
        return OpenRouterEmbedding(
            api_key=settings.openrouter_api_key,
            base_url=settings.openrouter_base_url,
            model=settings.openrouter_embedding_model,
            dimension=settings.embedding_dim,
        )
    if settings.nvidia_api_key:
        return NvidiaEmbedding(
            api_key=settings.nvidia_api_key,
            base_url=settings.nvidia_base_url,
            model=settings.embedding_model,
            dimension=settings.embedding_dim,
        )
    return DeterministicEmbeddingService(settings.embedding_dim)


__all__ = [
    "RetrievalService",
    "RetrievedChunk",
    "build_embedding_service",
    "get_retrieval_service",
    "rrf_fuse",
    "_fetch_bm25",
    "_row_to_chunk",
]
