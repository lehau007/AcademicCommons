from __future__ import annotations

import asyncio
import re
from collections import Counter
from datetime import UTC, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.llm import DeterministicEmbeddingService, EmbeddingService, SentenceTransformerEmbedding
from app.models import DocumentSummary, Language, OcrQuality

SUMMARY_SCHEMA_VERSION = "1.0"
_WORD_RE = re.compile(r"[A-Za-z0-9À-ỹ]{3,}", re.UNICODE)
_HEADING_RE = re.compile(r"^(#{1,6})\s+(?P<title>.+?)\s*$", re.MULTILINE)
_VIETNAMESE_HINTS = {
    "va",
    "cua",
    "cho",
    "trong",
    "mot",
    "nhung",
    "khong",
    "duoc",
    "kien",
    "thuc",
    "he",
    "thong",
}
_ENGLISH_HINTS = {
    "the",
    "and",
    "for",
    "with",
    "from",
    "this",
    "that",
    "into",
    "using",
    "system",
    "data",
}
_STOPWORDS = _VIETNAMESE_HINTS | _ENGLISH_HINTS | {
    "document",
    "section",
    "chapter",
    "course",
    "page",
    "pages",
    "introduction",
    "summary",
    "overview",
}


class SectionSummaryPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    heading: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    page_range: tuple[int, int]


class DocumentSummaryPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: str = Field(default=SUMMARY_SCHEMA_VERSION, pattern=r"^1\.0$")
    topic: str = Field(min_length=1)
    concepts: list[str]
    language: Language
    ocr_quality: OcrQuality
    section_summaries: list[SectionSummaryPayload]
    overall_summary: str = Field(min_length=1)


def build_embedding_service(*, prefer_sentence_transformer: bool = False) -> EmbeddingService:
    if prefer_sentence_transformer:
        return SentenceTransformerEmbedding()
    from app.config import get_settings
    from app.services.retrieval_service import build_embedding_service as build_tiered_embedding_service

    return build_tiered_embedding_service(get_settings())


def summarize_markdown(markdown_text: str) -> DocumentSummaryPayload:
    text = _clean_markdown(markdown_text)
    sections = _split_sections(text)
    section_payloads = [
        SectionSummaryPayload(
            heading=section["heading"],
            summary=_summarize_block(section["content"]),
            page_range=(index, index),
        )
        for index, section in enumerate(sections, start=1)
    ]

    if not section_payloads:
        section_payloads = [
            SectionSummaryPayload(
                heading="Document Overview",
                summary=_summarize_block(text),
                page_range=(1, 1),
            )
        ]

    topic = _pick_topic(text, section_payloads)
    concepts = _extract_concepts(text, section_payloads, fallback=topic)
    overall_summary = _build_overall_summary(section_payloads, text)

    return DocumentSummaryPayload(
        topic=topic,
        concepts=concepts,
        language=_detect_language(text),
        ocr_quality=_estimate_ocr_quality(text),
        section_summaries=section_payloads,
        overall_summary=overall_summary,
    )


async def upsert_document_summary(
    session: AsyncSession,
    *,
    document_id: UUID,
    markdown_text: str,
    embedding_service: EmbeddingService | None = None,
    now: datetime | None = None,
) -> tuple[DocumentSummary, DocumentSummaryPayload]:
    payload = summarize_markdown(markdown_text)
    service = embedding_service or build_embedding_service()
    try:
        vector = (await asyncio.to_thread(service.encode, [payload.overall_summary], input_type="passage"))[0]
    except RuntimeError:
        from app.config import get_settings

        vector = DeterministicEmbeddingService(get_settings().embedding_dim).encode(
            [payload.overall_summary], input_type="passage"
        )[0]
    timestamp = now or datetime.now(UTC)

    summary = await session.scalar(select(DocumentSummary).where(DocumentSummary.document_id == document_id))
    if summary is None:
        summary = DocumentSummary(document_id=document_id, created_at=timestamp)

    summary.schema_version = payload.schema_version
    summary.topic = payload.topic
    summary.concepts = payload.concepts
    summary.language = payload.language
    summary.ocr_quality = payload.ocr_quality
    summary.section_summaries = payload.model_dump(mode="json")["section_summaries"]
    summary.overall_summary = payload.overall_summary
    summary.summary_embedding = vector
    summary.updated_at = timestamp

    session.add(summary)
    await session.flush()
    return summary, payload


def _clean_markdown(markdown_text: str) -> str:
    text = markdown_text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"`{3,}.*?`{3,}", " ", text, flags=re.DOTALL)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"\[[^\]]+\]\([^)]+\)", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _split_sections(markdown_text: str) -> list[dict[str, str]]:
    matches = list(_HEADING_RE.finditer(markdown_text))
    if not matches:
        return [{"heading": "Document Overview", "content": markdown_text}]

    sections: list[dict[str, str]] = []
    if matches[0].start() > 0:
        prefix = markdown_text[: matches[0].start()].strip()
        if prefix:
            sections.append({"heading": "Document Overview", "content": prefix})

    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown_text)
        content = markdown_text[start:end].strip()
        if content:
            sections.append({"heading": match.group("title").strip(), "content": content})

    return sections or [{"heading": "Document Overview", "content": markdown_text}]


def _summarize_block(text: str, *, max_sentences: int = 2, max_chars: int = 280) -> str:
    normalized = re.sub(r"\s+", " ", text).strip()
    if not normalized:
        return "No extractable text was available for this section."

    sentences = re.split(r"(?<=[.!?])\s+", normalized)
    picked = " ".join(sentence.strip() for sentence in sentences[:max_sentences] if sentence.strip()).strip()
    summary = picked or normalized
    if len(summary) <= max_chars:
        return summary
    truncated = summary[: max_chars - 1].rsplit(" ", 1)[0].strip()
    return f"{truncated}..."


def _pick_topic(markdown_text: str, sections: list[SectionSummaryPayload]) -> str:
    title_candidate = next((section.heading for section in sections if section.heading != "Document Overview"), None)
    if title_candidate:
        return title_candidate

    for line in markdown_text.splitlines():
        cleaned = _strip_inline_markdown(line)
        if cleaned:
            return cleaned[:120]
    return "Document Overview"


def _extract_concepts(
    markdown_text: str,
    sections: list[SectionSummaryPayload],
    *,
    fallback: str,
    limit: int = 8,
) -> list[str]:
    concepts: list[str] = []
    seen: set[str] = set()

    for section in sections:
        cleaned = _strip_inline_markdown(section.heading)
        lowered = cleaned.lower()
        if cleaned and lowered not in seen and lowered != "document overview":
            concepts.append(cleaned)
            seen.add(lowered)
        if len(concepts) >= limit:
            return concepts

    counts = Counter(
        token.lower()
        for token in _WORD_RE.findall(markdown_text)
        if token.lower() not in _STOPWORDS and not token.isdigit()
    )
    for token, _ in counts.most_common(limit):
        if token not in seen:
            concepts.append(token)
            seen.add(token)
        if len(concepts) >= limit:
            break

    if not concepts:
        concepts.append(fallback)
    return concepts


def _build_overall_summary(sections: list[SectionSummaryPayload], markdown_text: str, *, max_words: int = 220) -> str:
    parts = [f"{section.heading}: {section.summary}" for section in sections[:6]]
    combined = " ".join(parts).strip()
    if not combined:
        combined = _summarize_block(markdown_text, max_sentences=4, max_chars=1200)

    words = combined.split()
    if len(words) <= max_words:
        return combined
    return " ".join(words[:max_words]).rstrip(" ,.;:") + "..."


def _detect_language(markdown_text: str) -> Language:
    tokens = [token.lower() for token in _WORD_RE.findall(markdown_text)]
    vi_score = sum(token in _VIETNAMESE_HINTS for token in tokens) + sum(
        "à" <= char.lower() <= "ỹ" for char in markdown_text
    )
    en_score = sum(token in _ENGLISH_HINTS for token in tokens)

    if vi_score > 0 and en_score > 0:
        return Language.MIXED
    if vi_score > en_score:
        return Language.VI
    return Language.EN


def _estimate_ocr_quality(markdown_text: str) -> OcrQuality:
    tokens = markdown_text.split()
    if len(tokens) < 15:
        return OcrQuality.LOW

    suspicious = 0
    for token in tokens:
        stripped = token.strip(".,:;!?()[]{}")
        if not stripped:
            continue
        if len(stripped) <= 2 and not stripped.isdigit():
            suspicious += 1
            continue
        if re.search(r"[^\wÀ-ỹ/-]{2,}", stripped):
            suspicious += 1

    ratio = suspicious / max(len(tokens), 1)
    if len(tokens) < 40:
        if ratio >= 0.15:
            return OcrQuality.MEDIUM
        return OcrQuality.HIGH
    if ratio >= 0.22:
        return OcrQuality.LOW
    if ratio >= 0.1:
        return OcrQuality.MEDIUM
    return OcrQuality.HIGH


def _strip_inline_markdown(text: str) -> str:
    cleaned = re.sub(r"[*_`>#-]+", " ", text)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


__all__ = [
    "DocumentSummaryPayload",
    "SectionSummaryPayload",
    "build_embedding_service",
    "summarize_markdown",
    "upsert_document_summary",
]
