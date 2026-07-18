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
DEFAULT_SIMILARITY_THRESHOLD = 0.82
DEFAULT_TOPIC_MIN_DOCS = 2


def resolve_project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, payload: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload, encoding="utf-8")


def slugify(label: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", label.lower()).strip("_")
    return slug or "node"


def normalize_concept(label: str) -> str:
    cleaned = re.sub(r"\s+", " ", label).strip().lower()
    cleaned = re.sub(r"[^a-z0-9 +#-]", "", cleaned)
    return cleaned


def cosine_similarity(left: list[float], right: list[float]) -> float:
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if left_norm == 0.0 or right_norm == 0.0:
        return 0.0
    return dot / (left_norm * right_norm)


@dataclass
class DocumentSummary:
    document_id: str
    path: Path
    topic: str
    concepts: list[str]
    section_summaries: list[dict[str, Any]]
    overall_summary: str


@dataclass
class ConceptRecord:
    canonical_label: str
    normalized_key: str
    aliases: set[str] = field(default_factory=set)
    source_documents: set[str] = field(default_factory=set)
    embedding: list[float] | None = None


def load_summaries(summaries_dir: Path) -> list[DocumentSummary]:
    summaries: list[DocumentSummary] = []
    for path in sorted(summaries_dir.glob("*.json")):
        data = read_json(path)
        summaries.append(
            DocumentSummary(
                document_id=path.stem,
                path=path,
                topic=data["topic"],
                concepts=list(data.get("concepts", [])),
                section_summaries=list(data.get("section_summaries", [])),
                overall_summary=data.get("overall_summary", ""),
            )
        )
    return summaries


def load_sentence_transformer(model_name: str) -> Any:
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise SystemExit(
            "sentence-transformers is not installed. Install requirements.txt before running this experiment."
        ) from exc
    return SentenceTransformer(model_name)


def collect_concepts(summaries: list[DocumentSummary]) -> dict[str, ConceptRecord]:
    """Phase 2 step 1: dedupe concepts by normalized string across all summaries."""
    records: dict[str, ConceptRecord] = {}
    for summary in summaries:
        for raw in summary.concepts:
            key = normalize_concept(raw)
            if not key:
                continue
            rec = records.get(key)
            if rec is None:
                rec = ConceptRecord(canonical_label=raw.strip(), normalized_key=key)
                records[key] = rec
            rec.aliases.add(raw.strip())
            rec.source_documents.add(summary.document_id)
    return records


def cluster_near_duplicates(
    records: dict[str, ConceptRecord],
    encoder: Any,
    similarity_threshold: float,
) -> dict[str, ConceptRecord]:
    """Merge concepts whose embeddings are near-duplicates (greedy single-linkage)."""
    keys = list(records.keys())
    if not keys:
        return records

    labels = [records[k].canonical_label for k in keys]
    embeddings = encoder.encode(labels, convert_to_numpy=True, normalize_embeddings=True).tolist()
    for key, emb in zip(keys, embeddings):
        records[key].embedding = emb

    merged: dict[str, ConceptRecord] = {}
    assigned: dict[str, str] = {}  # original key -> cluster key

    for key in keys:
        rec = records[key]
        best_cluster_key: str | None = None
        best_score = 0.0
        for cluster_key, cluster_rec in merged.items():
            score = cosine_similarity(rec.embedding or [], cluster_rec.embedding or [])
            if score > best_score:
                best_score = score
                best_cluster_key = cluster_key
        if best_cluster_key is not None and best_score >= similarity_threshold:
            cluster_rec = merged[best_cluster_key]
            cluster_rec.aliases.update(rec.aliases)
            cluster_rec.source_documents.update(rec.source_documents)
            # Prefer the canonical label with the highest source-document count.
            if len(rec.source_documents) > 0 and len(rec.canonical_label) < len(cluster_rec.canonical_label):
                cluster_rec.canonical_label = rec.canonical_label
            assigned[key] = best_cluster_key
        else:
            merged[key] = rec
            assigned[key] = key

    return merged


def build_concept_graph(
    summaries: list[DocumentSummary],
    course_seed: dict[str, Any] | None,
    encoder: Any,
    similarity_threshold: float,
    topic_min_docs: int,
) -> dict[str, Any]:
    """Phase 2: deterministic stand-in for the LLM call. Builds the v1 concept graph."""
    records = collect_concepts(summaries)
    clustered = cluster_near_duplicates(records, encoder, similarity_threshold)

    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    used_ids: set[str] = set()

    def make_id(prefix: str, label: str) -> str:
        base = f"{prefix}_{slugify(label)}"
        candidate = base
        counter = 2
        while candidate in used_ids:
            candidate = f"{base}_{counter}"
            counter += 1
        used_ids.add(candidate)
        return candidate

    # Level 0 — course root
    course_label = (course_seed or {}).get("name") or "Course"
    course_id = make_id("course", course_label)
    nodes.append({
        "id": course_id,
        "label": course_label,
        "level": 0,
        "source_documents": [s.document_id for s in summaries],
    })

    # Level 1 — topic nodes from each DocumentSummary.topic
    topic_id_by_doc: dict[str, str] = {}
    topic_id_by_key: dict[str, str] = {}
    for summary in summaries:
        key = normalize_concept(summary.topic)
        if key in topic_id_by_key:
            topic_id_by_doc[summary.document_id] = topic_id_by_key[key]
            continue
        topic_id = make_id("topic", summary.topic)
        topic_id_by_key[key] = topic_id
        topic_id_by_doc[summary.document_id] = topic_id
        nodes.append({
            "id": topic_id,
            "label": summary.topic,
            "level": 1,
            "source_documents": [
                s.document_id for s in summaries if normalize_concept(s.topic) == key
            ],
        })
        edges.append({"source": course_id, "target": topic_id, "relation": "contains"})

    # Concepts: level 1 if shared across >= topic_min_docs documents, else level 2 (concept).
    # Promoted shared concepts become topic-level cross-cutting nodes attached to the course root.
    # Document-specific concepts attach to that document's topic node.
    concept_id_by_key: dict[str, str] = {}
    for key, rec in clustered.items():
        is_shared = len(rec.source_documents) >= topic_min_docs
        # Skip a concept that exactly matches an existing topic label to avoid duplicates.
        if key in topic_id_by_key:
            concept_id_by_key[key] = topic_id_by_key[key]
            continue
        level = 1 if is_shared else 2
        prefix = "topic" if is_shared else "concept"
        concept_id = make_id(prefix, rec.canonical_label)
        concept_id_by_key[key] = concept_id
        nodes.append({
            "id": concept_id,
            "label": rec.canonical_label,
            "level": level,
            "source_documents": sorted(rec.source_documents),
            "aliases": sorted(rec.aliases) if len(rec.aliases) > 1 else [],
        })
        if is_shared:
            edges.append({"source": course_id, "target": concept_id, "relation": "contains"})
            # Also mark it as related to each topic node where it appears.
            for doc_id in sorted(rec.source_documents):
                parent_topic = topic_id_by_doc.get(doc_id)
                if parent_topic and parent_topic != concept_id:
                    edges.append({"source": parent_topic, "target": concept_id, "relation": "related"})
        else:
            # Attach to the (single) parent topic.
            doc_id = next(iter(rec.source_documents))
            parent_topic = topic_id_by_doc.get(doc_id)
            if parent_topic and parent_topic != concept_id:
                edges.append({"source": parent_topic, "target": concept_id, "relation": "contains"})

    # Dedupe edges
    seen_edges: set[tuple[str, str, str]] = set()
    deduped_edges: list[dict[str, Any]] = []
    for edge in edges:
        sig = (edge["source"], edge["target"], edge["relation"])
        if sig in seen_edges:
            continue
        seen_edges.add(sig)
        deduped_edges.append(edge)

    return {
        "schema_version": "concept_graph_v1",
        "course_root_id": course_id,
        "nodes": nodes,
        "edges": deduped_edges,
    }


def render_markdown(graph: dict[str, Any]) -> str:
    nodes_by_id = {n["id"]: n for n in graph["nodes"]}
    children: dict[str, list[str]] = {nid: [] for nid in nodes_by_id}
    for edge in graph["edges"]:
        if edge["relation"] != "contains":
            continue
        children.setdefault(edge["source"], []).append(edge["target"])

    lines: list[str] = []
    root_id = graph["course_root_id"]

    def walk(node_id: str, depth: int, seen: set[str]) -> None:
        if node_id in seen:
            return
        seen = seen | {node_id}
        node = nodes_by_id[node_id]
        indent = "  " * depth
        src = ", ".join(node.get("source_documents", []))
        suffix = f"  _(docs: {src})_" if src else ""
        lines.append(f"{indent}- **{node['label']}** (level {node['level']}){suffix}")
        for child_id in sorted(children.get(node_id, []), key=lambda i: nodes_by_id[i]["label"].lower()):
            walk(child_id, depth + 1, seen)

    lines.append("# Concept Graph")
    lines.append("")
    walk(root_id, 0, set())
    lines.append("")
    return "\n".join(lines)


def compute_stats(graph: dict[str, Any], summaries: list[DocumentSummary], course_seed: dict[str, Any] | None) -> dict[str, Any]:
    nodes = graph["nodes"]
    edges = graph["edges"]
    level_counts: dict[int, int] = {}
    for node in nodes:
        level_counts[node["level"]] = level_counts.get(node["level"], 0) + 1
    max_depth = max(level_counts.keys()) if level_counts else 0

    seed_text = ((course_seed or {}).get("topic_summary") or "").lower()
    if seed_text:
        labels = [n["label"] for n in nodes if n["level"] >= 1]
        covered = sum(1 for label in labels if normalize_concept(label) and normalize_concept(label) in seed_text)
        topic_coverage = covered / max(1, len(labels))
    else:
        topic_coverage = 0.0

    return {
        "node_count": len(nodes),
        "edge_count": len(edges),
        "max_depth": max_depth,
        "level_counts": level_counts,
        "topic_coverage_vs_seed": round(topic_coverage, 3),
        "document_count": len(summaries),
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="E2 Mindmap concept extraction experiment (deterministic Phase-2 stand-in for the LLM call)."
    )
    parser.add_argument(
        "--summaries-dir",
        default="src/experiments/mindmap/sample_summaries/intro_to_ai",
        help="Directory containing DocumentSummary JSON files.",
    )
    parser.add_argument(
        "--course-seed",
        default="src/experiments/mindmap/sample_course_seed.json",
        help="Path to the Course Seed JSON.",
    )
    parser.add_argument(
        "--graph-output",
        default="src/experiments/mindmap/results/intro_to_ai_graph.json",
        help="Where to write the concept graph JSON.",
    )
    parser.add_argument(
        "--markdown-output",
        default="src/experiments/mindmap/results/intro_to_ai_graph.md",
        help="Where to write the markdown bullet tree rendering.",
    )
    parser.add_argument(
        "--summary-output",
        default=None,
        help="Optional JSON path for the run summary (stats).",
    )
    parser.add_argument("--model-name", default=DEFAULT_MODEL_NAME)
    parser.add_argument("--similarity-threshold", type=float, default=DEFAULT_SIMILARITY_THRESHOLD)
    parser.add_argument("--topic-min-docs", type=int, default=DEFAULT_TOPIC_MIN_DOCS)
    return parser


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    project_root = resolve_project_root()

    def resolve(path_str: str) -> Path:
        p = Path(path_str)
        if not p.is_absolute():
            p = (project_root / p).resolve()
        return p

    summaries_dir = resolve(args.summaries_dir)
    course_seed_path = resolve(args.course_seed)
    graph_output = resolve(args.graph_output)
    markdown_output = resolve(args.markdown_output)

    if not summaries_dir.exists():
        print(json.dumps({"error": "summaries_dir_not_found", "path": str(summaries_dir)}), file=sys.stderr)
        return 2

    # Phase 1 — collect pre-extracted document summaries.
    summaries = load_summaries(summaries_dir)
    if not summaries:
        print(json.dumps({"error": "no_summaries_found", "path": str(summaries_dir)}), file=sys.stderr)
        return 3

    course_seed = read_json(course_seed_path) if course_seed_path.exists() else None

    # Phase 2 — deterministic concept graph build (stand-in for the single LLM call).
    encoder = load_sentence_transformer(args.model_name)
    graph = build_concept_graph(
        summaries=summaries,
        course_seed=course_seed,
        encoder=encoder,
        similarity_threshold=args.similarity_threshold,
        topic_min_docs=args.topic_min_docs,
    )

    write_json(graph_output, graph)
    write_text(markdown_output, render_markdown(graph))

    stats = compute_stats(graph, summaries, course_seed)
    run_summary = {
        "summaries_dir": str(summaries_dir),
        "course_seed": str(course_seed_path) if course_seed else None,
        "graph_output": str(graph_output),
        "markdown_output": str(markdown_output),
        "model_name": args.model_name,
        "similarity_threshold": args.similarity_threshold,
        "topic_min_docs": args.topic_min_docs,
        "stats": stats,
    }

    if args.summary_output:
        write_json(resolve(args.summary_output), run_summary)

    print(json.dumps(run_summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
