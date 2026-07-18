"""Offline cost reporting over the optimizer's JSONL invocation log.

The optimizer SDK appends one JSON record per invocation (cost, token usage,
cache tier, and the ``run_context.metadata`` we set in ``OptimizerAdapter``).
This module reads that log and aggregates it for the thesis evaluation chapter.

Record shapes vary across SDK versions, so extraction is defensive: every value
is looked up at the top level first, then under the common nested containers
(``metadata``, ``usage``, ``cache_info``, ``result``).
"""
from __future__ import annotations

import json
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class GroupStat:
    key: tuple[str, ...]
    calls: int = 0
    cost_usd: float = 0.0
    tokens_in: int = 0
    tokens_out: int = 0
    cache_hits: int = 0

    @property
    def cache_hit_rate(self) -> float:
        return self.cache_hits / self.calls if self.calls else 0.0


@dataclass
class CostReport:
    group_by: tuple[str, ...]
    groups: list[GroupStat] = field(default_factory=list)
    total: GroupStat = field(default_factory=lambda: GroupStat(key=("TOTAL",)))


def load_records(path: str | Path) -> list[dict[str, Any]]:
    """Parse a JSONL log file; silently skip blank or malformed lines."""
    records: list[dict[str, Any]] = []
    file_path = Path(path)
    if not file_path.exists():
        return records
    with file_path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                parsed = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(parsed, dict):
                records.append(parsed)
    return records


def aggregate_records(
    records: Iterable[dict[str, Any]],
    *,
    group_by: Sequence[str] = ("flow", "provider"),
) -> CostReport:
    keys = tuple(group_by)
    report = CostReport(group_by=keys)
    by_key: dict[tuple[str, ...], GroupStat] = {}
    for record in records:
        group_key = tuple(_dimension(record, dim) for dim in keys)
        stat = by_key.get(group_key)
        if stat is None:
            stat = GroupStat(key=group_key)
            by_key[group_key] = stat
        _accumulate(stat, record)
        _accumulate(report.total, record)
    report.groups = sorted(by_key.values(), key=lambda s: s.cost_usd, reverse=True)
    return report


def render_markdown(report: CostReport) -> str:
    header = [*report.group_by, "calls", "cost_usd", "tokens_in", "tokens_out", "cache_hit_rate"]
    lines = ["| " + " | ".join(header) + " |", "|" + "|".join(["---"] * len(header)) + "|"]
    for stat in [*report.groups, report.total]:
        cells = [
            *stat.key,
            str(stat.calls),
            f"{stat.cost_usd:.6f}",
            str(stat.tokens_in),
            str(stat.tokens_out),
            f"{stat.cache_hit_rate:.1%}",
        ]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def _accumulate(stat: GroupStat, record: dict[str, Any]) -> None:
    stat.calls += 1
    stat.cost_usd += _number(_lookup(record, "cost_usd", "cost"))
    stat.tokens_in += int(_number(_lookup(record, "tokens_in", "input_uncached", "input_tokens", "prompt_tokens")))
    stat.tokens_in += int(_number(_lookup(record, "input_cached")))
    stat.tokens_out += int(_number(_lookup(record, "tokens_out", "output", "output_tokens", "completion_tokens")))
    if _is_cache_hit(record):
        stat.cache_hits += 1


# Some grouping dimensions live under a different canonical key in the SDK log.
_DIMENSION_ALIASES: dict[str, tuple[str, ...]] = {
    "flow": ("flow", "skill_id"),
}


def _dimension(record: dict[str, Any], dimension: str) -> str:
    value = _lookup(record, *_DIMENSION_ALIASES.get(dimension, (dimension,)))
    if value is None or value == "":
        return "unknown"
    return str(value)


_NESTED_CONTAINERS = ("metadata", "usage", "cache_info", "result")


def _lookup(record: dict[str, Any], *names: str) -> Any:
    for name in names:
        if name in record and record[name] not in (None, ""):
            return record[name]
        for container in _NESTED_CONTAINERS:
            nested = record.get(container)
            if isinstance(nested, dict) and name in nested and nested[name] not in (None, ""):
                return nested[name]
    return None


def _is_cache_hit(record: dict[str, Any]) -> bool:
    hit = _lookup(record, "cache_hit", "hit")
    if isinstance(hit, bool):
        return hit
    tier = _lookup(record, "cache_tier", "tier")
    status = _lookup(record, "status")
    return tier not in (None, "", "none") or str(status).upper() == "CACHE_HIT"


def _number(value: Any) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0
