from __future__ import annotations

import ast
from pathlib import Path

SRC = Path(__file__).with_name("ablation_retrieval.py").read_text()


def test_no_hardcoded_openrouter_rerank() -> None:
    assert "OpenRouterRerank(" not in SRC


def test_delegates_to_production_rerank() -> None:
    # imports and calls retrieval_service._rerank so rerank behaviour == production
    assert "_rerank" in SRC
    tree = ast.parse(SRC)
    imported = {
        n.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module == "app.services.retrieval_service"
        for n in node.names
    }
    assert "_rerank" in imported
