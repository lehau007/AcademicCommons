"""Output quality validation + structured-block canonicalization.

Ports the inline quality-flag / structured-data validators inside the experiment's
``run_mode`` (lines ~1512-1645) plus ``render_deterministic_markdown`` (1372-1415).

The experiment interleaves two concerns in ``run_mode``:
  1. scanning structured (``schema_version``) text blocks to set validators AND rewriting
     their ``content`` to deterministic markdown (this feeds normalization — critical path);
  2. assembling the final ``quality_flags`` dict (route_match, non_empty_output, warnings).
These are split into :meth:`canonicalize_structured_blocks` and :meth:`assemble_quality_flags`
so the pipeline can compute the merged markdown in between, exactly like ``run_mode``.
"""

from __future__ import annotations

import json
import re
from typing import Any

from app.services.document_processing.models import Block


def render_deterministic_markdown(data: dict[str, Any]) -> str:
    content_type = data.get("content_type", "")
    if content_type in ("adjacency_matrix", "incidence_matrix", "table", "table_or_matrix"):
        rows = data.get("values", [])
        col_labels = data.get("column_labels", [])
        row_labels = data.get("row_labels", [])

        md_lines = []
        if col_labels:
            header = "| " + " | ".join([""] + [str(c) for c in col_labels]) + " |"
            sep = "| " + " | ".join(["---"] * (len(col_labels) + 1)) + " |"
            md_lines.extend([header, sep])
        elif rows and len(rows[0]) > 0:
            header = "| " + " | ".join(["Col " + str(i + 1) for i in range(len(rows[0]))]) + " |"
            sep = "| " + " | ".join(["---"] * len(rows[0])) + " |"
            md_lines.extend([header, sep])

        for i, row in enumerate(rows):
            r_label = str(row_labels[i]) if i < len(row_labels) else ""
            row_vals = [str(v) for v in row]
            if col_labels:
                line = "| " + " | ".join([r_label] + row_vals) + " |"
            else:
                line = "| " + " | ".join(row_vals) + " |"
            md_lines.append(line)

        if data.get("notes"):
            md_lines.append("")
            for note in data["notes"]:
                md_lines.append(f"**Note:** {note}")

        return "\n".join(md_lines)

    elif content_type == "graph_diagram":
        nodes = data.get("nodes", [])
        edges = data.get("edges", [])
        md_lines = ["**Graph/Diagram:**\n", "- Nodes: " + ", ".join(map(str, nodes))]
        if edges:
            md_lines.append("- Edges:")
            for e in edges:
                md_lines.append(f"  - {e}")
        return "\n".join(md_lines)

    return json.dumps(data, indent=2)


class OutputValidator:
    def canonicalize_structured_blocks(self, blocks: list[Block]) -> dict[str, Any]:
        """Scan structured blocks: set validators AND rewrite their content to
        deterministic markdown in place. Mirrors the loop in ``run_mode`` (1524-1554).

        Returns the ``validators`` sub-dict (parseable/matrix_shape/binary_values/
        table_consistency).
        """
        validators: dict[str, Any] = {
            "parseable": None,
            "matrix_shape": None,
            "binary_values": None,
            "table_consistency": None,
        }
        for b in blocks:
            if b["kind"] == "text" and "schema_version" in str(b.get("content", "")):
                validators["parseable"] = False
                try:
                    match = re.search(r"\{.*\}", str(b.get("content", "")), re.DOTALL)
                    if match:
                        parsed = json.loads(match.group(0))
                        validators["parseable"] = True

                        c_type = parsed.get("content_type", "")
                        if c_type in ("adjacency_matrix", "incidence_matrix"):
                            vals = parsed.get("values", [])
                            if vals:
                                num_cols = len(vals[0])
                                validators["matrix_shape"] = len(vals) == num_cols
                                validators["binary_values"] = all(
                                    str(v).strip() in ("0", "1") for row in vals for v in row
                                )
                        elif c_type in ("table", "table_or_matrix"):
                            vals = parsed.get("values", [])
                            if vals:
                                num_cols = len(vals[0])
                                validators["table_consistency"] = all(
                                    len(row) == num_cols for row in vals
                                )

                        b["content"] = render_deterministic_markdown(parsed)
                except Exception:
                    pass
        return validators

    def assemble_quality_flags(
        self,
        *,
        route: str,
        expected_route: str | None,
        validators: dict[str, Any],
        raw_markdown: str,
    ) -> dict[str, Any]:
        """Assemble the final quality_flags dict. Mirrors ``run_mode`` (1512-1645).

        ``raw_markdown`` is the merged raw result (``result_md``), computed by the
        pipeline AFTER :meth:`canonicalize_structured_blocks` mutated the blocks.
        """
        route_match = (route == expected_route) if expected_route is not None else None
        quality_flags: dict[str, Any] = {
            "route_match": route_match,
            "non_empty_output": bool(raw_markdown.strip()),
            "warnings": [],
            "validators": validators,
        }

        if not route_match:
            quality_flags["warnings"].append("route_mismatch")
        if "[VISION_PLACEHOLDER]" in raw_markdown:
            quality_flags["warnings"].append("vision_output_placeholder_detected")

        is_valid = True
        if validators.get("parseable") is False:
            is_valid = False
            quality_flags["warnings"].append("structured_content_parse_failed")
        for value in validators.values():
            if value is False:
                is_valid = False
                if "validator_failed" not in quality_flags["warnings"]:
                    quality_flags["warnings"].append("validator_failed")

        quality_flags["is_valid"] = is_valid
        return quality_flags
