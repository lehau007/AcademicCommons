from __future__ import annotations

import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "run_ablation", Path(__file__).with_name("run_ablation.py")
)


def _load():
    mod = importlib.util.module_from_spec(_spec)
    # run_ablation imports app.*; only load if importable, else skip via ImportError
    _spec.loader.exec_module(mod)
    return mod


def test_default_out_dir_naming() -> None:
    try:
        mod = _load()
    except ModuleNotFoundError:
        import pytest
        pytest.skip("app.* not importable outside container")
    assert mod.default_out_dir("agentic", "dense_rerank") == "hard/actual_agentic_dense"
    # hybrid_rerank (production-faithful hybrid) is the "hybrid" arm of the 2x2
    assert mod.default_out_dir("agentic", "hybrid_rerank") == "hard/actual_agentic_hybrid"
    # hybrid_norerank (no reranker) gets a distinct short name so it never collides
    assert mod.default_out_dir("traditional", "hybrid_norerank") == "hard/actual_traditional_hybridnr"
