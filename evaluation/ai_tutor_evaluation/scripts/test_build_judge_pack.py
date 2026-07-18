# evaluation/ai_tutor_evaluation/scripts/test_build_judge_pack.py
from __future__ import annotations

import json
from pathlib import Path

import importlib.util

_spec = importlib.util.spec_from_file_location(
    "build_judge_pack", Path(__file__).with_name("build_judge_pack.py")
)
bjp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bjp)


def test_build_pack_emits_bundles_and_meta(tmp_path: Path) -> None:
    actual = tmp_path / "actual"
    actual.mkdir()
    (actual / "q1.json").write_text(json.dumps({
        "qid": "q1", "question": "What is A*?", "answer": "A* uses f=g+h.",
        "citations": [], "retrieval_calls": [
            {"query": "A* search", "chunks": [{"content": "A* expands lowest f=g+h."}]}
        ],
    }))
    questions = [{"qid": "q1", "ground_truth": "A* selects the node with lowest f=g+h."}]
    out = tmp_path / "pack"
    n = bjp.build_pack(actual, questions, "RUBRIC-TEXT", out, "agentic_dense")

    assert n == 1
    assert (out / "INSTRUCTIONS.md").exists()
    assert (out / "schema.json").exists()
    assert "RUBRIC-TEXT" in (out / "rubric.md").read_text()
    bundle = (out / "q1.md").read_text()
    assert "What is A*?" in bundle
    assert "A* selects the node with lowest f=g+h." in bundle  # ground truth
    assert "A* expands lowest f=g+h." in bundle  # retrieved context
    assert "A* uses f=g+h." in bundle  # tutor answer
    # schema lists the six metrics
    schema = json.loads((out / "schema.json").read_text())
    for m in ["faithfulness", "answer_relevancy", "answer_correctness",
              "context_precision", "context_recall", "citation_accuracy"]:
        assert m in json.dumps(schema)


def test_instructions_name_the_output_dir(tmp_path: Path) -> None:
    out = tmp_path / "pack"
    bjp.build_pack(tmp_path / "empty", [], "R", out, "traditional_hybrid")
    assert "results_traditional_hybrid" in (out / "INSTRUCTIONS.md").read_text()
