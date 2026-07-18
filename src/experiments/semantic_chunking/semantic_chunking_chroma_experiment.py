from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_COLLECTION_NAME = "document_chunks"
DEFAULT_SIMILARITY_THRESHOLD = 0.55
DEFAULT_MIN_CHUNK_CHARS = 350
DEFAULT_MAX_CHUNK_CHARS = 1200


def resolve_project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def default_chroma_dir(project_root: Path) -> Path:
    return project_root / "src" / "experiments" / "semantic_chunking" / "chroma_db"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def infer_namespace(tier: str, subtype: str) -> str:
    if tier == "official":
        return "knowledge"
    if subtype in {"summary_note", "review_note"}:
        return "knowledge"
    if subtype in {"past_exam", "solved_exercise"}:
        return "exercise"
    return "knowledge"


def split_paragraphs(text: str) -> list[str]:
    normalized = text.replace("\r\n", "\n").strip()
    if not normalized:
        return []
    parts = re.split(r"\n\s*\n+", normalized)
    paragraphs = [part.strip() for part in parts if part.strip()]
    return paragraphs


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
    paragraph_count: int
    char_count: int


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
) -> list[tuple[str, int]]:
    paragraphs = split_paragraphs(section.body)
    if not paragraphs:
        return []

    chunk_texts: list[tuple[str, int]] = []
    current_parts = [paragraphs[0]]
    current_chars = len(paragraphs[0])
    current_paragraph_count = 1

    for idx in range(1, len(paragraphs)):
        paragraph = paragraphs[idx]
        candidate_chars = current_chars + 2 + len(paragraph)
        similarity = cosine_similarity(paragraph_embeddings[idx - 1], paragraph_embeddings[idx])

        should_merge = (
            similarity >= similarity_threshold
            and candidate_chars <= max_chunk_chars
        )

        if should_merge or current_chars < min_chunk_chars:
            current_parts.append(paragraph)
            current_chars = candidate_chars
            current_paragraph_count += 1
            continue

        chunk_texts.append(("\n\n".join(current_parts).strip(), current_paragraph_count))
        current_parts = [paragraph]
        current_chars = len(paragraph)
        current_paragraph_count = 1

    if current_parts:
        chunk_texts.append(("\n\n".join(current_parts).strip(), current_paragraph_count))

    return chunk_texts


def build_chunks(
    markdown_text: str,
    encoder: Any,
    similarity_threshold: float,
    min_chunk_chars: int,
    max_chunk_chars: int,
    sample_id: str,
) -> list[Chunk]:
    sections = parse_markdown_sections(markdown_text)
    chunks: list[Chunk] = []
    chunk_order = 1

    for section in sections:
        paragraphs = split_paragraphs(section.body)
        if not paragraphs:
            continue

        paragraph_embeddings = encoder.encode(paragraphs, convert_to_numpy=True, normalize_embeddings=True)
        merged_chunks = chunk_section_paragraphs(
            section=section,
            paragraph_embeddings=paragraph_embeddings.tolist(),
            similarity_threshold=similarity_threshold,
            min_chunk_chars=min_chunk_chars,
            max_chunk_chars=max_chunk_chars,
        )

        for text, paragraph_count in merged_chunks:
            chunk_id = f"{sample_id}-chunk-{chunk_order:03d}"
            chunks.append(
                Chunk(
                    chunk_id=chunk_id,
                    text=text,
                    section_title=section.title,
                    chunk_order=chunk_order,
                    paragraph_count=paragraph_count,
                    char_count=len(text),
                )
            )
            chunk_order += 1

    return chunks


def load_sentence_transformer(model_name: str) -> Any:
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise SystemExit(
            "sentence-transformers is not installed. Add dependencies from requirements.txt before running this experiment."
        ) from exc

    return SentenceTransformer(model_name)


def open_chroma_collection(chroma_dir: Path, collection_name: str) -> Any:
    try:
        import chromadb
    except ImportError as exc:
        raise SystemExit(
            "chromadb is not installed. Add dependencies from requirements.txt before running this experiment."
        ) from exc

    chroma_dir.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(chroma_dir))
    return client.get_or_create_collection(name=collection_name)


def delete_existing_sample(collection: Any, sample_id: str) -> int:
    existing = collection.get(where={"source_document_id": sample_id}, include=[])
    ids = existing.get("ids", []) if existing else []
    if ids:
        collection.delete(ids=ids)
    return len(ids)


def chunk_to_metadata(
    chunk: Chunk,
    source_document_id: str,
    course_code: str,
    tier: str,
    subtype: str,
    rag_namespace: str,
    source_path: str,
) -> dict[str, Any]:
    return {
        "source_document_id": source_document_id,
        "course_code": course_code,
        "document_tier": tier,
        "document_subtype": subtype,
        "rag_namespace": rag_namespace,
        "section_title": chunk.section_title,
        "chunk_order": chunk.chunk_order,
        "paragraph_count": chunk.paragraph_count,
        "char_count": chunk.char_count,
        "source_path": source_path,
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Structure-aware semantic chunking experiment with Sentence Transformers + ChromaDB."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to a normalized_result.md generated by the document processing pipeline.",
    )
    parser.add_argument("--sample-id", required=True, help="Stable source document id for chunk ids and Chroma metadata.")
    parser.add_argument("--course-code", required=True, help="Course code metadata, e.g. IT3040.")
    parser.add_argument("--tier", required=True, choices=["official", "community"], help="Document tier.")
    parser.add_argument(
        "--subtype",
        required=True,
        help="Document subtype, e.g. lecture_slides, summary_note, past_exam.",
    )
    parser.add_argument("--model-name", default=DEFAULT_MODEL_NAME, help="Sentence Transformer model name.")
    parser.add_argument("--collection-name", default=DEFAULT_COLLECTION_NAME, help="Target Chroma collection.")
    parser.add_argument("--chroma-dir", default=None, help="Persistent Chroma directory.")
    parser.add_argument("--similarity-threshold", type=float, default=DEFAULT_SIMILARITY_THRESHOLD)
    parser.add_argument("--min-chunk-chars", type=int, default=DEFAULT_MIN_CHUNK_CHARS)
    parser.add_argument("--max-chunk-chars", type=int, default=DEFAULT_MAX_CHUNK_CHARS)
    parser.add_argument(
        "--summary-output",
        default=None,
        help="Optional JSON path for a run summary.",
    )
    return parser


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    project_root = resolve_project_root()
    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = (project_root / input_path).resolve()
    if not input_path.exists():
        print(json.dumps({"error": "input_not_found", "input": str(input_path)}), file=sys.stderr)
        return 2

    markdown_text = read_text(input_path)
    encoder = load_sentence_transformer(args.model_name)
    chunks = build_chunks(
        markdown_text=markdown_text,
        encoder=encoder,
        similarity_threshold=args.similarity_threshold,
        min_chunk_chars=args.min_chunk_chars,
        max_chunk_chars=args.max_chunk_chars,
        sample_id=args.sample_id,
    )

    if not chunks:
        print(json.dumps({"error": "no_chunks_created", "input": str(input_path)}), file=sys.stderr)
        return 3

    rag_namespace = infer_namespace(args.tier, args.subtype)
    chroma_dir = Path(args.chroma_dir) if args.chroma_dir else default_chroma_dir(project_root)
    if not chroma_dir.is_absolute():
        chroma_dir = (project_root / chroma_dir).resolve()

    collection = open_chroma_collection(chroma_dir=chroma_dir, collection_name=args.collection_name)
    deleted_count = delete_existing_sample(collection, args.sample_id)

    chunk_texts = [chunk.text for chunk in chunks]
    chunk_embeddings = encoder.encode(chunk_texts, convert_to_numpy=True, normalize_embeddings=True)
    collection.add(
        ids=[chunk.chunk_id for chunk in chunks],
        documents=chunk_texts,
        embeddings=chunk_embeddings.tolist(),
        metadatas=[
            chunk_to_metadata(
                chunk=chunk,
                source_document_id=args.sample_id,
                course_code=args.course_code,
                tier=args.tier,
                subtype=args.subtype,
                rag_namespace=rag_namespace,
                source_path=input_path.relative_to(project_root).as_posix() if input_path.is_relative_to(project_root) else str(input_path),
            )
            for chunk in chunks
        ],
    )

    summary = {
        "input_path": input_path.relative_to(project_root).as_posix() if input_path.is_relative_to(project_root) else str(input_path),
        "sample_id": args.sample_id,
        "course_code": args.course_code,
        "tier": args.tier,
        "subtype": args.subtype,
        "rag_namespace": rag_namespace,
        "model_name": args.model_name,
        "collection_name": args.collection_name,
        "chroma_dir": str(chroma_dir),
        "deleted_existing_chunks": deleted_count,
        "chunk_count": len(chunks),
        "avg_chunk_chars": round(sum(chunk.char_count for chunk in chunks) / len(chunks), 2),
        "chunks": [
            {
                "chunk_id": chunk.chunk_id,
                "section_title": chunk.section_title,
                "chunk_order": chunk.chunk_order,
                "paragraph_count": chunk.paragraph_count,
                "char_count": chunk.char_count,
                "preview": chunk.text[:160],
            }
            for chunk in chunks
        ],
    }

    if args.summary_output:
        summary_path = Path(args.summary_output)
        if not summary_path.is_absolute():
            summary_path = (project_root / summary_path).resolve()
        write_json(summary_path, summary)

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
