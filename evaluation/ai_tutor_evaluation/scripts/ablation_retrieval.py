"""Retrieval-source ablation for the AI tutor evaluation.

Drop-in replacements for ``RetrievalService`` that vary ONLY the candidate source
(and, for hybrid, the rerank toggle). Everything downstream — outline filtering,
official-tier boost, community-vote nudges, ``k`` / ``prefetch_k``, the agent loop,
and the judge — is identical to production so the metric deltas are attributable to
the retrieval technique alone.

Modes (see evaluation README / thesis Chapter 5 ablation):
  * ``dense_rerank``     : production path (dense semantic -> production reranker).
  * ``hybrid_rerank``    : dense + BM25 fused by Reciprocal Rank Fusion -> production
                           reranker. Production-faithful hybrid; the clean counterpart to
                           ``dense_rerank`` for the dense-vs-hybrid axis (rerank held
                           constant, only the candidate source differs).
  * ``hybrid_norerank``  : dense + BM25 fused by RRF, top-k taken directly (NO rerank) —
                           isolates the reranker's contribution.
  * ``bm25_rerank``      : PostgreSQL full-text (ts_rank, 'simple' config) -> production reranker.

Notes / honest caveats:
  * The lexical branch is PostgreSQL ``ts_rank`` over ``to_tsvector('simple', content)``.
    'simple' (no stemming/stopwords) is used because the corpus is mixed Vietnamese +
    English; this is a BM25-*style* keyword baseline, not a literal Okapi BM25.
  * The cosine floor (``tutor_sim_threshold``) is a dense-similarity gate, so it is
    applied ONLY in the dense config. Gating lexical/fused candidates by dense cosine
    would contaminate the ablation, so it is skipped for bm25/hybrid.

Runs inside the api container (same as run_tutor.py); reuses production internals.
"""
from __future__ import annotations

import asyncio
from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import DocumentTier
from app.services.retrieval_service import (
    RetrievedChunk,
    _fetch_bm25,
    _fetch_candidates,
    _fetch_net_votes,
    _is_outline_chunk,
    _rerank,
    _row_to_chunk,
    build_embedding_service,
    rrf_fuse,
)


class AblationRetrieval:
    """RetrievalService-compatible ablation that also records every search call.

    ``mode`` selects the candidate source / rerank behaviour. Records chunks exactly
    like run_tutor.RecordingRetrieval so the judge sees the retrieved context.
    """

    MODES = {"dense_rerank", "bm25_rerank", "hybrid_norerank", "hybrid_rerank"}

    def __init__(self, settings: Any, mode: str) -> None:
        if mode not in self.MODES:
            raise ValueError(f"unknown ablation mode: {mode}")
        self._settings = settings
        self._mode = mode
        self._embedding = build_embedding_service(settings)
        self.calls: list[dict] = []

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
        chunks = await self._search(
            session, course_id, query, namespaces, k, prefetch_k, document_ids
        )
        self.calls.append({
            "mode": self._mode,
            "query": query,
            "namespaces": namespaces,
            "chunks": [
                {
                    "chunk_id": str(c.id),
                    "document_id": str(c.document_id),
                    "section_title": c.section_title,
                    "chunk_order": c.chunk_order,
                    "cosine_sim": round(c.cosine_sim, 4),
                    "final_score": round(c.final_score, 4),
                    "content": c.content,
                }
                for c in chunks
            ],
        })
        return chunks

    async def _search(
        self,
        session: AsyncSession,
        course_id: UUID,
        query: str,
        namespaces: list[str] | None,
        k: int,
        prefetch_k: int,
        document_ids: list[UUID] | None,
    ) -> list[RetrievedChunk]:
        settings = self._settings
        effective_namespaces = namespaces or ["knowledge"]

        query_vec = (await asyncio.to_thread(
            self._embedding.encode, [query], input_type="query"
        ))[0]
        query_vec_str = "[" + ",".join(str(v) for v in query_vec) + "]"

        # --- candidate source ---------------------------------------------------
        rrf_scores: dict[UUID, float] = {}
        if self._mode == "dense_rerank":
            rows = await _fetch_candidates(
                session, course_id, query_vec_str, effective_namespaces, prefetch_k, document_ids
            )
            candidates = [_row_to_chunk(r) for r in rows]
            # cosine floor is dense-specific: applied here only.
            if settings.tutor_sim_threshold > 0.0:
                candidates = [c for c in candidates if c.cosine_sim >= settings.tutor_sim_threshold]
        elif self._mode == "bm25_rerank":
            rows = await _fetch_bm25(
                session, course_id, query, query_vec_str, effective_namespaces, prefetch_k, document_ids
            )
            candidates = [_row_to_chunk(r) for r in rows]
        else:  # hybrid_norerank or hybrid_rerank — dense + BM25 fused by RRF
            dense_rows = await _fetch_candidates(
                session, course_id, query_vec_str, effective_namespaces, prefetch_k, document_ids
            )
            bm25_rows = await _fetch_bm25(
                session, course_id, query, query_vec_str, effective_namespaces, prefetch_k, document_ids
            )
            candidates, rrf_scores = rrf_fuse(
                [_row_to_chunk(r) for r in dense_rows],
                [_row_to_chunk(r) for r in bm25_rows],
            )
            candidates = candidates[:prefetch_k]

        if not candidates:
            return []

        # --- outline filter (identical to production) ---------------------------
        non_outline = [c for c in candidates if not _is_outline_chunk(c.section_title, c.content)]
        if len(non_outline) < len(candidates):
            if len(non_outline) < k:
                dropped = [c for c in candidates if _is_outline_chunk(c.section_title, c.content)]
                dropped.sort(key=lambda c: c.cosine_sim, reverse=True)
                non_outline += dropped[: k - len(non_outline)]
            candidates = non_outline

        # --- rerank (dense/bm25) or skip (hybrid) -------------------------------
        do_rerank = self._mode in {"dense_rerank", "bm25_rerank", "hybrid_rerank"}
        if do_rerank:
            ranked = await asyncio.to_thread(_rerank, query, candidates, query_vec, settings, k)
            rerank_floor = getattr(settings, "tutor_rerank_threshold", 0.0)
            if rerank_floor > 0.0 and any(c.rerank_score is not None for c in ranked):
                ranked = [c for c in ranked if (c.rerank_score or 0.0) >= rerank_floor]
        else:
            ranked = candidates  # keep RRF order; rerank_score stays None

        # --- tier boost + community votes (identical to production) -------------
        doc_ids = list({c.document_id for c in ranked})
        net_votes = await _fetch_net_votes(session, doc_ids)
        course_avg = (sum(net_votes.values()) / len(net_votes)) if net_votes else 1.0

        for chunk in ranked:
            if chunk.rerank_score is not None:
                base = chunk.rerank_score
            elif self._mode == "hybrid_norerank":
                base = rrf_scores.get(chunk.id, 0.0)  # fused relevance drives ranking
            else:
                base = chunk.cosine_sim
            score = base
            if chunk.document_tier == DocumentTier.OFFICIAL:
                score *= settings.tutor_tier_boost
            nv = net_votes.get(chunk.document_id, 0)
            vote_factor = max(-0.5, min(0.5, nv / max(abs(course_avg), 1.0)))
            score *= 1.0 + vote_factor
            chunk.final_score = score

        ranked.sort(key=lambda c: c.final_score, reverse=True)
        return ranked[:k]


__all__ = ["AblationRetrieval", "rrf_fuse", "_fetch_bm25"]
