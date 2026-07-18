"""Experiment E3 — Mock Test generation (deterministic template-based stub).

This script implements the plan-then-generate Mock Test pipeline from
`.agent/project_description.md` §6.8 *without* calling any LLM. Questions are
produced by templating from source-chunk sentences so the end-to-end shape of
the artefacts (Test Plan v1, Generated Question v1, Citation Object v1) can be
exercised and evaluated. Swap `templated_generate_*` for real LLM calls when
integrating with Gemini/OpenAI.

Phases:
  1. Topic inventory  — parse markdown chunks (with frontmatter) into
     topic -> [chunk] mapping.
  2. Test plan        — deterministic balanced plan across topics, difficulties,
     and question types.
  3. Question gen     — template MCQ / short-answer / true-false per topic with
     citations.
  4. Validation+dedup — embedding similarity dedup (MiniLM, > 0.85 cosine).

Outputs JSON (machine-readable test) and Markdown (human-readable rendering).
"""

from __future__ import annotations

import argparse
import json
import math
import random
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any


DEFAULT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_DEDUP_THRESHOLD = 0.85
DEFAULT_TOTAL_QUESTIONS = 10
DEFAULT_SEED = 42

DIFFICULTIES = ["easy", "medium", "hard"]
QUESTION_TYPES = ["multiple_choice", "short_answer", "true_false"]


# --------------------------------------------------------------------------- #
# Project paths
# --------------------------------------------------------------------------- #


def resolve_project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def default_chunks_dir(project_root: Path) -> Path:
    return project_root / "src" / "experiments" / "mock_test" / "sample_chunks" / "intro_to_ai"


def default_results_dir(project_root: Path) -> Path:
    return project_root / "src" / "experiments" / "mock_test" / "results"


# --------------------------------------------------------------------------- #
# Data classes
# --------------------------------------------------------------------------- #


@dataclass
class Chunk:
    chunk_id: str
    topic: str
    source: str
    section_title: str
    text: str
    file_path: str
    chunk_order: int
    sentences: list[str] = field(default_factory=list)


@dataclass
class Citation:
    document_id: str
    document_title: str
    document_tier: str
    document_subtype: str
    section_title: str | None
    page_number: int | None
    chunk_id: str
    chunk_order: int
    relevance_score: float
    excerpt: str


@dataclass
class GeneratedQuestion:
    question_text: str
    question_type: str
    difficulty: str
    topic: str
    options: list[str] | None
    correct_answer: str
    explanation: str
    citations: list[Citation]


# --------------------------------------------------------------------------- #
# Frontmatter + chunk loading
# --------------------------------------------------------------------------- #


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    raw_fm, body = match.group(1), match.group(2)
    meta: dict[str, str] = {}
    for line in raw_fm.splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()
    return meta, body


def extract_section_title(body: str) -> str:
    for line in body.splitlines():
        if line.startswith("#"):
            return re.sub(r"^#+\s*", "", line).strip()
    return "Untitled Section"


SENT_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"\(\d])")


def split_sentences(text: str) -> list[str]:
    # Strip headings/lists/blank lines.
    body_lines = [
        ln.strip()
        for ln in text.splitlines()
        if ln.strip() and not ln.strip().startswith("#")
    ]
    flat = " ".join(body_lines)
    raw = SENT_SPLIT_RE.split(flat)
    return [s.strip() for s in raw if len(s.strip()) > 25]


def load_chunks(chunks_dir: Path) -> list[Chunk]:
    chunks: list[Chunk] = []
    files = sorted(p for p in chunks_dir.glob("*.md"))
    for order, path in enumerate(files, start=1):
        raw = path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(raw)
        topic = meta.get("topic", "Unknown")
        chunk_id = meta.get("chunk_id", path.stem)
        source = meta.get("source", "")
        section_title = extract_section_title(body)
        chunks.append(
            Chunk(
                chunk_id=chunk_id,
                topic=topic,
                source=source,
                section_title=section_title,
                text=body.strip(),
                file_path=str(path),
                chunk_order=order,
                sentences=split_sentences(body),
            )
        )
    return chunks


def build_topic_inventory(chunks: list[Chunk]) -> dict[str, list[Chunk]]:
    inventory: dict[str, list[Chunk]] = {}
    for ch in chunks:
        inventory.setdefault(ch.topic, []).append(ch)
    return inventory


# --------------------------------------------------------------------------- #
# Phase 2 — Test plan
# --------------------------------------------------------------------------- #


def build_test_plan(
    inventory: dict[str, list[Chunk]],
    total_questions: int,
    rng: random.Random,
) -> dict[str, Any]:
    topics = sorted(inventory.keys())
    if not topics:
        raise ValueError("Empty topic inventory")

    # Proportional allocation by chunk count, with at least 1 per topic.
    chunk_counts = {t: len(inventory[t]) for t in topics}
    total_chunks = sum(chunk_counts.values())
    raw_alloc = {t: max(1, round(total_questions * chunk_counts[t] / total_chunks)) for t in topics}

    # Adjust to hit exactly total_questions.
    diff = total_questions - sum(raw_alloc.values())
    sorted_topics = sorted(topics, key=lambda t: chunk_counts[t], reverse=True)
    i = 0
    while diff != 0 and sorted_topics:
        t = sorted_topics[i % len(sorted_topics)]
        if diff > 0:
            raw_alloc[t] += 1
            diff -= 1
        elif raw_alloc[t] > 1:
            raw_alloc[t] -= 1
            diff += 1
        i += 1
        if i > 1000:
            break

    plan_entries: list[dict[str, Any]] = []
    for t in topics:
        count = raw_alloc[t]
        # Balanced difficulty + question type assignment.
        for k in range(count):
            difficulty = DIFFICULTIES[k % len(DIFFICULTIES)]
            qtype = QUESTION_TYPES[(k + topics.index(t)) % len(QUESTION_TYPES)]
            plan_entries.append(
                {
                    "topic": t,
                    "question_count": 1,
                    "difficulty": difficulty,
                    "question_types": [qtype],
                    "source_document_ids": [c.chunk_id for c in inventory[t]],
                }
            )
    return {"total_questions": total_questions, "plan": plan_entries}


# --------------------------------------------------------------------------- #
# Phase 3 — Templated question generation
# --------------------------------------------------------------------------- #


DEFINITION_RE = re.compile(
    r"^(?P<subject>[A-Z][A-Za-z0-9 \-'_/\(\)\*\.]{2,80}?)\s+(?:is|are|means|refers to)\s+(?P<predicate>.{20,400})$"
)


def find_definition_sentence(chunk: Chunk, rng: random.Random) -> tuple[str, str, str] | None:
    candidates: list[tuple[str, str, str]] = []
    for sent in chunk.sentences:
        m = DEFINITION_RE.match(sent.rstrip("."))
        if m:
            subj = m.group("subject").strip()
            pred = m.group("predicate").strip().rstrip(".")
            # Avoid trivial / pronoun-led subjects.
            if subj.lower() in {"it", "this", "that", "they"}:
                continue
            candidates.append((sent, subj, pred))
    if not candidates:
        return None
    return rng.choice(candidates)


def make_citation(chunk: Chunk, score: float) -> Citation:
    excerpt = chunk.text.replace("\n", " ").strip()
    if len(excerpt) > 200:
        excerpt = excerpt[:197] + "..."
    return Citation(
        document_id=chunk.chunk_id,
        document_title=chunk.section_title,
        document_tier="official",
        document_subtype="lecture_slides",
        section_title=chunk.section_title,
        page_number=None,
        chunk_id=chunk.chunk_id,
        chunk_order=chunk.chunk_order,
        relevance_score=score,
        excerpt=excerpt,
    )


def gather_distractor_sentences(
    all_chunks: list[Chunk], exclude_topic: str, n: int, rng: random.Random
) -> list[str]:
    pool: list[str] = []
    for c in all_chunks:
        if c.topic == exclude_topic:
            continue
        for s in c.sentences:
            m = DEFINITION_RE.match(s.rstrip("."))
            if m:
                pred = m.group("predicate").strip().rstrip(".")
                if 20 < len(pred) < 200:
                    pool.append(pred)
    rng.shuffle(pool)
    out: list[str] = []
    for cand in pool:
        if cand in out:
            continue
        out.append(cand)
        if len(out) >= n:
            break
    return out


def templated_multiple_choice(
    chunk: Chunk,
    all_chunks: list[Chunk],
    difficulty: str,
    rng: random.Random,
) -> GeneratedQuestion | None:
    found = find_definition_sentence(chunk, rng)
    if not found:
        return None
    _, subject, predicate = found
    correct = predicate
    distractors = gather_distractor_sentences(all_chunks, chunk.topic, n=3, rng=rng)
    if len(distractors) < 3:
        return None
    options = distractors + [correct]
    rng.shuffle(options)
    letters = ["A", "B", "C", "D"]
    rendered_options = [f"{letters[i]}. {opt}" for i, opt in enumerate(options)]
    correct_letter = letters[options.index(correct)]
    return GeneratedQuestion(
        question_text=f"Which of the following best describes '{subject}'?",
        question_type="multiple_choice",
        difficulty=difficulty,
        topic=chunk.topic,
        options=rendered_options,
        correct_answer=f"{correct_letter}. {correct}",
        explanation=f"Source chunk '{chunk.chunk_id}' defines {subject} as: {predicate}",
        citations=[make_citation(chunk, score=0.92)],
    )


def templated_short_answer(
    chunk: Chunk,
    difficulty: str,
    rng: random.Random,
) -> GeneratedQuestion | None:
    found = find_definition_sentence(chunk, rng)
    if not found:
        # Fall back to first interrogative-style sentence if present.
        for sent in chunk.sentences:
            if "?" in sent:
                return GeneratedQuestion(
                    question_text=sent,
                    question_type="short_answer",
                    difficulty=difficulty,
                    topic=chunk.topic,
                    options=None,
                    correct_answer="See cited chunk.",
                    explanation=f"Direct quotation from '{chunk.chunk_id}'.",
                    citations=[make_citation(chunk, score=0.88)],
                )
        return None
    _, subject, predicate = found
    return GeneratedQuestion(
        question_text=f"What is {subject}?",
        question_type="short_answer",
        difficulty=difficulty,
        topic=chunk.topic,
        options=None,
        correct_answer=predicate,
        explanation=f"Derived by templating an X-is-Y sentence from chunk '{chunk.chunk_id}'.",
        citations=[make_citation(chunk, score=0.90)],
    )


SUBJECT_NOUN_RE = re.compile(r"\b([A-Z][a-zA-Z\-]{3,})\b")


def templated_true_false(
    chunk: Chunk,
    all_chunks: list[Chunk],
    difficulty: str,
    rng: random.Random,
) -> GeneratedQuestion | None:
    if not chunk.sentences:
        return None
    make_false = rng.random() < 0.5
    sentence = rng.choice(chunk.sentences)
    if make_false:
        # Find a capitalised noun to swap with one from another topic.
        cap_nouns = SUBJECT_NOUN_RE.findall(sentence)
        cap_nouns = [n for n in cap_nouns if n.lower() not in {"the", "this", "that", "with", "from", "into"}]
        if not cap_nouns:
            make_false = False
        else:
            target = rng.choice(cap_nouns)
            # Pull a noun from a different topic.
            foreign_pool: list[str] = []
            for c in all_chunks:
                if c.topic == chunk.topic:
                    continue
                for s in c.sentences:
                    for n in SUBJECT_NOUN_RE.findall(s):
                        if n != target and n.lower() not in {"the", "this", "that"}:
                            foreign_pool.append(n)
            if not foreign_pool:
                make_false = False
            else:
                swap = rng.choice(foreign_pool)
                falsified = re.sub(rf"\b{re.escape(target)}\b", swap, sentence, count=1)
                return GeneratedQuestion(
                    question_text=f"True or False: {falsified}",
                    question_type="true_false",
                    difficulty=difficulty,
                    topic=chunk.topic,
                    options=["True", "False"],
                    correct_answer="False",
                    explanation=(
                        f"Original chunk '{chunk.chunk_id}' uses '{target}', not '{swap}'. "
                        f"Term swap produced a false statement."
                    ),
                    citations=[make_citation(chunk, score=0.85)],
                )
    # True case (or fallback).
    return GeneratedQuestion(
        question_text=f"True or False: {sentence}",
        question_type="true_false",
        difficulty=difficulty,
        topic=chunk.topic,
        options=["True", "False"],
        correct_answer="True",
        explanation=f"Statement is taken verbatim from chunk '{chunk.chunk_id}'.",
        citations=[make_citation(chunk, score=0.95)],
    )


def generate_question_for_entry(
    entry: dict[str, Any],
    inventory: dict[str, list[Chunk]],
    all_chunks: list[Chunk],
    rng: random.Random,
) -> GeneratedQuestion | None:
    topic = entry["topic"]
    qtype = entry["question_types"][0]
    difficulty = entry["difficulty"]
    topic_chunks = list(inventory.get(topic, []))
    if not topic_chunks:
        return None
    # Try each chunk until a template succeeds.
    rng.shuffle(topic_chunks)
    for chunk in topic_chunks:
        if qtype == "multiple_choice":
            q = templated_multiple_choice(chunk, all_chunks, difficulty, rng)
        elif qtype == "short_answer":
            q = templated_short_answer(chunk, difficulty, rng)
        else:
            q = templated_true_false(chunk, all_chunks, difficulty, rng)
        if q is not None:
            return q
    return None


# --------------------------------------------------------------------------- #
# Phase 4 — Validation, dedup, citation checks
# --------------------------------------------------------------------------- #


def cosine(a, b) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)


def load_sentence_transformer(model_name: str):
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise SystemExit(
            "sentence-transformers is not installed. Run `pip install -r requirements.txt`."
        ) from exc
    return SentenceTransformer(model_name)


def dedup_questions(
    questions: list[GeneratedQuestion],
    threshold: float,
    encoder,
) -> tuple[list[GeneratedQuestion], list[dict[str, Any]]]:
    if not questions:
        return [], []
    texts = [q.question_text for q in questions]
    embs = encoder.encode(texts, convert_to_numpy=True, normalize_embeddings=True).tolist()
    keep: list[GeneratedQuestion] = []
    keep_embs: list[list[float]] = []
    removed: list[dict[str, Any]] = []
    for q, e in zip(questions, embs):
        is_dup = False
        for ke in keep_embs:
            sim = cosine(e, ke)
            if sim > threshold:
                is_dup = True
                removed.append({"question_text": q.question_text, "similarity": round(sim, 4)})
                break
        if not is_dup:
            keep.append(q)
            keep_embs.append(e)
    return keep, removed


def validate_citations(
    questions: list[GeneratedQuestion],
    chunk_index: dict[str, Chunk],
) -> dict[str, Any]:
    total = 0
    valid = 0
    bad: list[dict[str, Any]] = []
    for q in questions:
        for cit in q.citations:
            total += 1
            chunk = chunk_index.get(cit.chunk_id)
            if chunk is None:
                bad.append({"chunk_id": cit.chunk_id, "reason": "chunk_not_found"})
                continue
            excerpt = cit.excerpt.replace("...", "").strip()
            # Simple substring containment check (first 80 chars of excerpt).
            probe = excerpt[:80]
            if probe and probe in chunk.text.replace("\n", " "):
                valid += 1
            else:
                bad.append({"chunk_id": cit.chunk_id, "reason": "excerpt_not_in_chunk"})
    pct = (valid / total * 100.0) if total else 0.0
    return {"total_citations": total, "valid_citations": valid, "valid_pct": round(pct, 2), "invalid": bad}


def compute_coverage(questions: list[GeneratedQuestion], inventory: dict[str, list[Chunk]]) -> dict[str, Any]:
    covered = {q.topic for q in questions}
    all_topics = set(inventory.keys())
    return {
        "topics_total": len(all_topics),
        "topics_covered": len(covered & all_topics),
        "coverage_pct": round(100.0 * len(covered & all_topics) / max(1, len(all_topics)), 2),
        "missing_topics": sorted(all_topics - covered),
    }


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #


def question_to_dict(q: GeneratedQuestion) -> dict[str, Any]:
    d = asdict(q)
    return d


def render_markdown(test_payload: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append(f"# Mock Test — {test_payload['course']}")
    lines.append("")
    lines.append(f"Total questions: **{len(test_payload['questions'])}**")
    lines.append("")
    lines.append("## Test Plan Summary")
    plan = test_payload["test_plan"]
    lines.append(f"- Planned total: {plan['total_questions']}")
    from collections import Counter
    by_topic = Counter(e["topic"] for e in plan["plan"])
    for t, c in sorted(by_topic.items()):
        lines.append(f"  - {t}: {c}")
    lines.append("")
    lines.append("## Questions")
    lines.append("")
    for i, q in enumerate(test_payload["questions"], start=1):
        lines.append(f"### Q{i}. [{q['topic']} | {q['difficulty']} | {q['question_type']}]")
        lines.append("")
        lines.append(q["question_text"])
        lines.append("")
        if q["options"]:
            for opt in q["options"]:
                lines.append(f"- {opt}")
            lines.append("")
        lines.append(f"**Answer:** {q['correct_answer']}")
        lines.append("")
        lines.append(f"_Explanation:_ {q['explanation']}")
        lines.append("")
        lines.append("_Citations:_")
        for cit in q["citations"]:
            lines.append(
                f"- `{cit['chunk_id']}` ({cit['section_title']}) — score={cit['relevance_score']:.2f}"
            )
            lines.append(f"  > {cit['excerpt']}")
        lines.append("")
    lines.append("## Metrics")
    metrics = test_payload["metrics"]
    lines.append(f"- Coverage: {metrics['coverage']['coverage_pct']}% "
                 f"({metrics['coverage']['topics_covered']}/{metrics['coverage']['topics_total']} topics)")
    lines.append(f"- Dedup removed: {metrics['dedup']['removed_count']} "
                 f"(rate={metrics['dedup']['dedup_rate_pct']}%)")
    lines.append(f"- Citation validity: {metrics['citations']['valid_pct']}% "
                 f"({metrics['citations']['valid_citations']}/{metrics['citations']['total_citations']})")
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Deterministic Mock Test generation experiment (E3) — template-based stub for LLM behaviour."
    )
    parser.add_argument("--chunks-dir", default=None, help="Directory with frontmatter-tagged .md chunks.")
    parser.add_argument("--course", default="intro_to_ai", help="Course identifier used in output file names.")
    parser.add_argument("--total-questions", type=int, default=DEFAULT_TOTAL_QUESTIONS)
    parser.add_argument("--dedup-threshold", type=float, default=DEFAULT_DEDUP_THRESHOLD)
    parser.add_argument("--model-name", default=DEFAULT_MODEL_NAME)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--results-dir", default=None)
    parser.add_argument("--inventory-output", default=None,
                        help="Optional path to dump the topic inventory JSON.")
    return parser


def main() -> int:
    args = build_arg_parser().parse_args()
    project_root = resolve_project_root()
    chunks_dir = Path(args.chunks_dir) if args.chunks_dir else default_chunks_dir(project_root)
    results_dir = Path(args.results_dir) if args.results_dir else default_results_dir(project_root)
    results_dir.mkdir(parents=True, exist_ok=True)

    rng = random.Random(args.seed)

    # Phase 1 — Topic inventory.
    chunks = load_chunks(chunks_dir)
    if not chunks:
        print(json.dumps({"error": "no_chunks_found", "chunks_dir": str(chunks_dir)}), file=sys.stderr)
        return 2
    inventory = build_topic_inventory(chunks)

    inventory_dump = {
        topic: [
            {
                "chunk_id": c.chunk_id,
                "section_title": c.section_title,
                "source": c.source,
                "file_path": str(Path(c.file_path).relative_to(project_root))
                if Path(c.file_path).is_relative_to(project_root)
                else c.file_path,
                "sentence_count": len(c.sentences),
            }
            for c in chunks_in_topic
        ]
        for topic, chunks_in_topic in inventory.items()
    }
    inventory_path = (
        Path(args.inventory_output) if args.inventory_output
        else project_root / "src" / "experiments" / "mock_test" / "sample_topic_inventory.json"
    )
    inventory_path.parent.mkdir(parents=True, exist_ok=True)
    inventory_path.write_text(json.dumps(inventory_dump, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Phase 2 — Test plan.
    test_plan = build_test_plan(inventory, args.total_questions, rng)

    # Phase 3 — Generation.
    questions: list[GeneratedQuestion] = []
    for entry in test_plan["plan"]:
        q = generate_question_for_entry(entry, inventory, chunks, rng)
        if q is not None:
            questions.append(q)

    # Phase 4 — Validation / dedup / citation checks.
    encoder = load_sentence_transformer(args.model_name)
    pre_dedup_count = len(questions)
    questions, removed = dedup_questions(questions, args.dedup_threshold, encoder)
    chunk_index = {c.chunk_id: c for c in chunks}
    citation_report = validate_citations(questions, chunk_index)
    coverage = compute_coverage(questions, inventory)

    dedup_rate_pct = round(100.0 * len(removed) / max(1, pre_dedup_count), 2)

    by_topic = {}
    by_difficulty = {}
    by_type = {}
    for q in questions:
        by_topic[q.topic] = by_topic.get(q.topic, 0) + 1
        by_difficulty[q.difficulty] = by_difficulty.get(q.difficulty, 0) + 1
        by_type[q.question_type] = by_type.get(q.question_type, 0) + 1

    payload = {
        "course": args.course,
        "config": {
            "total_questions_requested": args.total_questions,
            "dedup_threshold": args.dedup_threshold,
            "model_name": args.model_name,
            "seed": args.seed,
            "generator": "deterministic_template_stub_v1",
        },
        "test_plan": test_plan,
        "questions": [question_to_dict(q) for q in questions],
        "metrics": {
            "counts": {
                "generated_pre_dedup": pre_dedup_count,
                "final": len(questions),
                "by_topic": by_topic,
                "by_difficulty": by_difficulty,
                "by_type": by_type,
            },
            "coverage": coverage,
            "dedup": {
                "threshold": args.dedup_threshold,
                "removed_count": len(removed),
                "removed": removed,
                "dedup_rate_pct": dedup_rate_pct,
            },
            "citations": citation_report,
        },
    }

    json_path = results_dir / f"{args.course}_test.json"
    md_path = results_dir / f"{args.course}_test.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(payload), encoding="utf-8")

    summary = {
        "course": args.course,
        "chunks_loaded": len(chunks),
        "topics": sorted(inventory.keys()),
        "questions_final": len(questions),
        "questions_pre_dedup": pre_dedup_count,
        "dedup_removed": len(removed),
        "dedup_rate_pct": dedup_rate_pct,
        "coverage": coverage,
        "citations": citation_report,
        "counts": payload["metrics"]["counts"],
        "outputs": {
            "inventory": str(inventory_path),
            "test_json": str(json_path),
            "test_md": str(md_path),
        },
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
