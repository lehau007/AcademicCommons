from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


DEFAULT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_COLLECTION_PREFIX = "rag_tutor"
DEFAULT_SIMILARITY_THRESHOLD = 0.55
DEFAULT_MIN_CHUNK_CHARS = 350
DEFAULT_MAX_CHUNK_CHARS = 1200
DEFAULT_TOP_K = 4
DEFAULT_FETCH_K = 8
DEFAULT_MMR_LAMBDA = 0.7
TIER_BOOST_MULTIPLIER = 1.15

COURSES = ("intro_to_ai", "database", "discrete_math")


def resolve_project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def experiment_root() -> Path:
    return Path(__file__).resolve().parent


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Frontmatter and chunking
# ---------------------------------------------------------------------------


def parse_frontmatter(markdown_text: str) -> tuple[dict[str, str], str]:
    text = markdown_text.replace("\r\n", "\n")
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    raw = text[4:end].strip()
    body = text[end + 4 :].lstrip("\n")
    meta: dict[str, str] = {}
    for line in raw.split("\n"):
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()
    return meta, body


def split_paragraphs(text: str) -> list[str]:
    normalized = text.replace("\r\n", "\n").strip()
    if not normalized:
        return []
    parts = re.split(r"\n\s*\n+", normalized)
    return [p.strip() for p in parts if p.strip()]


def normalize_heading_title(line: str) -> str:
    return re.sub(r"^#+\s*", "", line).strip() or "Untitled Section"


@dataclass
class Section:
    title: str
    body: str


@dataclass
class Chunk:
    chunk_id: str
    text: str
    section_title: str
    chunk_order: int
    char_count: int
    source_path: str
    tier: str
    subtype: str
    course_code: str


def parse_markdown_sections(markdown_text: str) -> list[Section]:
    text = markdown_text.replace("\r\n", "\n").strip()
    if not text:
        return []
    sections: list[Section] = []
    current_title = "Document Start"
    current_lines: list[str] = []
    for line in text.split("\n"):
        if re.match(r"^#{1,6}\s+", line):
            body = "\n".join(current_lines).strip()
            if body:
                sections.append(Section(title=current_title, body=body))
            current_title = normalize_heading_title(line)
            current_lines = []
            continue
        current_lines.append(line)
    final_body = "\n".join(current_lines).strip()
    if final_body:
        sections.append(Section(title=current_title, body=final_body))
    return sections


def cosine_similarity(left: list[float], right: list[float]) -> float:
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if left_norm == 0.0 or right_norm == 0.0:
        return 0.0
    return dot / (left_norm * right_norm)


def chunk_section_paragraphs(
    section: Section,
    paragraph_embeddings: list[list[float]],
    similarity_threshold: float,
    min_chunk_chars: int,
    max_chunk_chars: int,
) -> list[str]:
    paragraphs = split_paragraphs(section.body)
    if not paragraphs:
        return []
    chunk_texts: list[str] = []
    current_parts = [paragraphs[0]]
    current_chars = len(paragraphs[0])
    for idx in range(1, len(paragraphs)):
        paragraph = paragraphs[idx]
        candidate_chars = current_chars + 2 + len(paragraph)
        similarity = cosine_similarity(paragraph_embeddings[idx - 1], paragraph_embeddings[idx])
        should_merge = similarity >= similarity_threshold and candidate_chars <= max_chunk_chars
        if should_merge or current_chars < min_chunk_chars:
            current_parts.append(paragraph)
            current_chars = candidate_chars
            continue
        chunk_texts.append("\n\n".join(current_parts).strip())
        current_parts = [paragraph]
        current_chars = len(paragraph)
    if current_parts:
        chunk_texts.append("\n\n".join(current_parts).strip())
    return chunk_texts


def build_chunks_for_document(
    markdown_text: str,
    encoder: Any,
    sample_id: str,
    source_path: str,
    similarity_threshold: float,
    min_chunk_chars: int,
    max_chunk_chars: int,
) -> list[Chunk]:
    meta, body = parse_frontmatter(markdown_text)
    tier = meta.get("tier", "community")
    subtype = meta.get("subtype", "summary_note")
    course_code = meta.get("course_code", "UNKNOWN")
    sections = parse_markdown_sections(body)
    chunks: list[Chunk] = []
    order = 1
    for section in sections:
        paragraphs = split_paragraphs(section.body)
        if not paragraphs:
            continue
        paragraph_embeddings = encoder.encode(
            paragraphs, convert_to_numpy=True, normalize_embeddings=True
        )
        merged = chunk_section_paragraphs(
            section=section,
            paragraph_embeddings=paragraph_embeddings.tolist(),
            similarity_threshold=similarity_threshold,
            min_chunk_chars=min_chunk_chars,
            max_chunk_chars=max_chunk_chars,
        )
        for text in merged:
            chunks.append(
                Chunk(
                    chunk_id=f"{sample_id}-chunk-{order:03d}",
                    text=text,
                    section_title=section.title,
                    chunk_order=order,
                    char_count=len(text),
                    source_path=source_path,
                    tier=tier,
                    subtype=subtype,
                    course_code=course_code,
                )
            )
            order += 1
    return chunks


# ---------------------------------------------------------------------------
# Embeddings + retrieval strategies
# ---------------------------------------------------------------------------


def load_sentence_transformer(model_name: str) -> Any:
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise SystemExit(
            "sentence-transformers is not installed. Install dependencies from requirements.txt before running this experiment."
        ) from exc
    return SentenceTransformer(model_name)


def open_chroma_collection(chroma_dir: Path, collection_name: str) -> Any:
    try:
        import chromadb
    except ImportError as exc:
        raise SystemExit(
            "chromadb is not installed. Install dependencies from requirements.txt before running this experiment."
        ) from exc
    chroma_dir.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(chroma_dir))
    # Reset collection per run to keep results reproducible.
    try:
        client.delete_collection(name=collection_name)
    except Exception:
        pass
    return client.create_collection(name=collection_name, metadata={"hnsw:space": "cosine"})


@dataclass
class RetrievedChunk:
    chunk_id: str
    text: str
    score: float
    tier: str
    subtype: str
    section_title: str
    source_path: str
    raw_similarity: float = 0.0


def naive_top_k(
    query_embedding: list[float],
    chunk_embeddings: list[list[float]],
    chunks: list[Chunk],
    top_k: int,
) -> list[RetrievedChunk]:
    similarities = [
        cosine_similarity(query_embedding, emb) for emb in chunk_embeddings
    ]
    ranking = sorted(range(len(chunks)), key=lambda i: similarities[i], reverse=True)
    return [
        RetrievedChunk(
            chunk_id=chunks[i].chunk_id,
            text=chunks[i].text,
            score=similarities[i],
            raw_similarity=similarities[i],
            tier=chunks[i].tier,
            subtype=chunks[i].subtype,
            section_title=chunks[i].section_title,
            source_path=chunks[i].source_path,
        )
        for i in ranking[:top_k]
    ]


def mmr_select(
    query_embedding: list[float],
    chunk_embeddings: list[list[float]],
    chunks: list[Chunk],
    top_k: int,
    fetch_k: int,
    lambda_mult: float,
) -> tuple[list[RetrievedChunk], list[float]]:
    """Return MMR-selected chunks plus the raw query/chunk similarities for them."""
    similarities = [cosine_similarity(query_embedding, emb) for emb in chunk_embeddings]
    candidate_indices = sorted(range(len(chunks)), key=lambda i: similarities[i], reverse=True)[
        :fetch_k
    ]
    selected: list[int] = []
    while candidate_indices and len(selected) < top_k:
        best_idx = None
        best_score = -math.inf
        for idx in candidate_indices:
            relevance = similarities[idx]
            if selected:
                diversity = max(
                    cosine_similarity(chunk_embeddings[idx], chunk_embeddings[s])
                    for s in selected
                )
            else:
                diversity = 0.0
            mmr_score = lambda_mult * relevance - (1.0 - lambda_mult) * diversity
            if mmr_score > best_score:
                best_score = mmr_score
                best_idx = idx
        if best_idx is None:
            break
        selected.append(best_idx)
        candidate_indices.remove(best_idx)
    results = [
        RetrievedChunk(
            chunk_id=chunks[i].chunk_id,
            text=chunks[i].text,
            score=similarities[i],
            raw_similarity=similarities[i],
            tier=chunks[i].tier,
            subtype=chunks[i].subtype,
            section_title=chunks[i].section_title,
            source_path=chunks[i].source_path,
        )
        for i in selected
    ]
    return results, similarities


def mmr_with_tier_boost(
    query_embedding: list[float],
    chunk_embeddings: list[list[float]],
    chunks: list[Chunk],
    top_k: int,
    fetch_k: int,
    lambda_mult: float,
) -> list[RetrievedChunk]:
    """Run MMR on a larger fetch_k, apply tier boost, then re-sort and trim to top_k."""
    fetched, _ = mmr_select(
        query_embedding=query_embedding,
        chunk_embeddings=chunk_embeddings,
        chunks=chunks,
        top_k=fetch_k,
        fetch_k=fetch_k,
        lambda_mult=lambda_mult,
    )
    for item in fetched:
        if item.tier == "official":
            item.score = item.raw_similarity * TIER_BOOST_MULTIPLIER
        else:
            item.score = item.raw_similarity
    fetched.sort(key=lambda r: r.score, reverse=True)
    return fetched[:top_k]


# ---------------------------------------------------------------------------
# Answer stub + custom RAGAS-like metrics
# ---------------------------------------------------------------------------


_TOKEN_RE = re.compile(r"[A-Za-z0-9]+")


def tokenize(text: str) -> list[str]:
    return [t.lower() for t in _TOKEN_RE.findall(text)]


STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "is", "are",
    "be", "by", "with", "as", "at", "it", "its", "this", "that", "these", "those",
    "from", "into", "which", "what", "how", "when", "where", "who", "whom",
    "can", "may", "will", "would", "should", "could", "do", "does", "did",
    "not", "no", "if", "than", "then", "so", "such", "between", "two", "one",
    "any", "all", "each", "every", "other", "more", "less", "also",
}


def content_tokens(text: str) -> set[str]:
    return {t for t in tokenize(text) if t not in STOPWORDS and len(t) > 1}


def assemble_answer(retrieved: list[RetrievedChunk]) -> str:
    return "\n\n".join(f"[{r.chunk_id}] {r.text}" for r in retrieved)


def answer_similarity(
    generated_answer: str,
    ground_truth: str,
    encoder: Any,
) -> float:
    if not generated_answer.strip() or not ground_truth.strip():
        return 0.0
    embeddings = encoder.encode(
        [generated_answer, ground_truth],
        convert_to_numpy=True,
        normalize_embeddings=True,
    ).tolist()
    return cosine_similarity(embeddings[0], embeddings[1])


def context_precision(retrieved: list[RetrievedChunk], ground_truth: str) -> float:
    if not retrieved:
        return 0.0
    truth_tokens = content_tokens(ground_truth)
    if not truth_tokens:
        return 0.0
    hits = 0
    for r in retrieved:
        if content_tokens(r.text) & truth_tokens:
            hits += 1
    return hits / len(retrieved)


def context_recall(retrieved: list[RetrievedChunk], ground_truth: str) -> float:
    truth_tokens = content_tokens(ground_truth)
    if not truth_tokens:
        return 0.0
    covered: set[str] = set()
    for r in retrieved:
        covered |= content_tokens(r.text) & truth_tokens
    return len(covered) / len(truth_tokens)


def citation_accuracy(retrieved: list[RetrievedChunk], ground_truth: str) -> float:
    """Fraction of cited chunks (top-1) that contain a salient ground-truth phrase."""
    if not retrieved:
        return 0.0
    truth_tokens = content_tokens(ground_truth)
    if not truth_tokens:
        return 0.0
    top = retrieved[0]
    overlap = content_tokens(top.text) & truth_tokens
    # Considered accurate if the cited chunk covers >= 25% of ground-truth content tokens.
    return 1.0 if len(overlap) / len(truth_tokens) >= 0.25 else 0.0


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------


def discover_course_documents(corpus_dir: Path) -> list[Path]:
    return sorted(p for p in corpus_dir.glob("*.md") if p.is_file())


def load_golden_set(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_course_index(
    corpus_dir: Path,
    encoder: Any,
    similarity_threshold: float,
    min_chunk_chars: int,
    max_chunk_chars: int,
    chroma_dir: Path,
    collection_name: str,
) -> tuple[list[Chunk], list[list[float]], Any]:
    documents = discover_course_documents(corpus_dir)
    if not documents:
        raise SystemExit(f"No markdown documents found under {corpus_dir}")
    all_chunks: list[Chunk] = []
    for doc_path in documents:
        sample_id = doc_path.stem
        text = read_text(doc_path)
        chunks = build_chunks_for_document(
            markdown_text=text,
            encoder=encoder,
            sample_id=sample_id,
            source_path=doc_path.name,
            similarity_threshold=similarity_threshold,
            min_chunk_chars=min_chunk_chars,
            max_chunk_chars=max_chunk_chars,
        )
        all_chunks.extend(chunks)
    if not all_chunks:
        raise SystemExit(f"Corpus produced zero chunks: {corpus_dir}")
    embeddings = encoder.encode(
        [c.text for c in all_chunks],
        convert_to_numpy=True,
        normalize_embeddings=True,
    ).tolist()
    collection = open_chroma_collection(chroma_dir=chroma_dir, collection_name=collection_name)
    collection.add(
        ids=[c.chunk_id for c in all_chunks],
        documents=[c.text for c in all_chunks],
        embeddings=embeddings,
        metadatas=[
            {
                "section_title": c.section_title,
                "tier": c.tier,
                "subtype": c.subtype,
                "course_code": c.course_code,
                "source_path": c.source_path,
                "chunk_order": c.chunk_order,
            }
            for c in all_chunks
        ],
    )
    return all_chunks, embeddings, collection


@dataclass
class StrategyResult:
    name: str
    per_question: list[dict[str, Any]] = field(default_factory=list)

    def aggregate(self) -> dict[str, float]:
        if not self.per_question:
            return {}
        keys = ("answer_similarity", "context_precision", "context_recall", "citation_accuracy")
        agg: dict[str, float] = {}
        for k in keys:
            values = [q["scores"][k] for q in self.per_question]
            agg[k] = round(sum(values) / len(values), 4)
        return agg


def run_strategy(
    name: str,
    selector,
    qa_pairs: list[dict[str, Any]],
    chunks: list[Chunk],
    chunk_embeddings: list[list[float]],
    encoder: Any,
    top_k: int,
) -> StrategyResult:
    result = StrategyResult(name=name)
    for qa in qa_pairs:
        question = qa["question"]
        ground_truth = qa["answer"]
        query_embedding = encoder.encode(
            [question], convert_to_numpy=True, normalize_embeddings=True
        ).tolist()[0]
        retrieved = selector(query_embedding, chunk_embeddings, chunks)
        answer = assemble_answer(retrieved)
        scores = {
            "answer_similarity": round(
                answer_similarity(answer, ground_truth, encoder), 4
            ),
            "context_precision": round(context_precision(retrieved, ground_truth), 4),
            "context_recall": round(context_recall(retrieved, ground_truth), 4),
            "citation_accuracy": round(citation_accuracy(retrieved, ground_truth), 4),
        }
        result.per_question.append(
            {
                "id": qa.get("id"),
                "question": question,
                "ground_truth": ground_truth,
                "retrieved": [
                    {
                        "chunk_id": r.chunk_id,
                        "tier": r.tier,
                        "subtype": r.subtype,
                        "section_title": r.section_title,
                        "source_path": r.source_path,
                        "raw_similarity": round(r.raw_similarity, 4),
                        "final_score": round(r.score, 4),
                    }
                    for r in retrieved
                ],
                "generated_answer_preview": answer[:300],
                "scores": scores,
            }
        )
    return result


def build_strategies(top_k: int, fetch_k: int, lambda_mult: float):
    def naive(query_emb, chunk_embs, chunks):
        return naive_top_k(query_emb, chunk_embs, chunks, top_k=top_k)

    def mmr(query_emb, chunk_embs, chunks):
        retrieved, _ = mmr_select(
            query_emb, chunk_embs, chunks,
            top_k=top_k, fetch_k=fetch_k, lambda_mult=lambda_mult,
        )
        return retrieved

    def mmr_boost(query_emb, chunk_embs, chunks):
        return mmr_with_tier_boost(
            query_emb, chunk_embs, chunks,
            top_k=top_k, fetch_k=fetch_k, lambda_mult=lambda_mult,
        )

    return [("naive_top_k", naive), ("mmr", mmr), ("mmr_tier_boost", mmr_boost)]


def run_course(
    course: str,
    args: argparse.Namespace,
    encoder: Any,
) -> dict[str, Any]:
    project_root = resolve_project_root()
    corpus_dir = experiment_root() / "corpus" / course
    golden_path = project_root / "data" / "RAG_evaluation_data" / f"{course}.json"
    if not corpus_dir.exists():
        raise SystemExit(f"Missing corpus directory: {corpus_dir}")
    if not golden_path.exists():
        raise SystemExit(f"Missing golden Q&A file: {golden_path}")

    chroma_dir = experiment_root() / "chroma_db" / course
    collection_name = f"{DEFAULT_COLLECTION_PREFIX}_{course}"

    chunks, chunk_embeddings, _collection = build_course_index(
        corpus_dir=corpus_dir,
        encoder=encoder,
        similarity_threshold=args.similarity_threshold,
        min_chunk_chars=args.min_chunk_chars,
        max_chunk_chars=args.max_chunk_chars,
        chroma_dir=chroma_dir,
        collection_name=collection_name,
    )

    qa_pairs = load_golden_set(golden_path)
    strategies = build_strategies(
        top_k=args.top_k, fetch_k=args.fetch_k, lambda_mult=args.mmr_lambda
    )
    results_dir = experiment_root() / "results" / course
    course_summary: dict[str, Any] = {
        "course": course,
        "chunk_count": len(chunks),
        "question_count": len(qa_pairs),
        "strategies": {},
    }
    for name, selector in strategies:
        result = run_strategy(
            name=name,
            selector=selector,
            qa_pairs=qa_pairs,
            chunks=chunks,
            chunk_embeddings=chunk_embeddings,
            encoder=encoder,
            top_k=args.top_k,
        )
        aggregate = result.aggregate()
        report = {
            "course": course,
            "strategy": name,
            "top_k": args.top_k,
            "fetch_k": args.fetch_k,
            "mmr_lambda": args.mmr_lambda,
            "tier_boost_multiplier": TIER_BOOST_MULTIPLIER if name == "mmr_tier_boost" else None,
            "question_count": len(qa_pairs),
            "aggregate": aggregate,
            "per_question": result.per_question,
        }
        write_json(results_dir / f"{name}_report.json", report)
        course_summary["strategies"][name] = aggregate
    write_json(results_dir / "summary.json", course_summary)
    return course_summary


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="E1: RAG Tutor retrieval evaluation harness."
    )
    parser.add_argument(
        "--course",
        choices=(*COURSES, "all"),
        default="intro_to_ai",
        help="Course to evaluate (default: intro_to_ai).",
    )
    parser.add_argument("--model-name", default=DEFAULT_MODEL_NAME)
    parser.add_argument("--similarity-threshold", type=float, default=DEFAULT_SIMILARITY_THRESHOLD)
    parser.add_argument("--min-chunk-chars", type=int, default=DEFAULT_MIN_CHUNK_CHARS)
    parser.add_argument("--max-chunk-chars", type=int, default=DEFAULT_MAX_CHUNK_CHARS)
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    parser.add_argument("--fetch-k", type=int, default=DEFAULT_FETCH_K)
    parser.add_argument("--mmr-lambda", type=float, default=DEFAULT_MMR_LAMBDA)
    return parser


def main() -> int:
    args = build_arg_parser().parse_args()
    encoder = load_sentence_transformer(args.model_name)
    targets = COURSES if args.course == "all" else (args.course,)
    overall: dict[str, Any] = {"runs": {}}
    for course in targets:
        overall["runs"][course] = run_course(course, args, encoder)
    print(json.dumps(overall, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
