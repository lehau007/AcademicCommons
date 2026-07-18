"""HITL routing + SLA escalation experiment (E4).

Pure-logic simulation of the review routing rules described in
``.agent/project_description.md`` (Sections 5 and 6.2). No LLM calls, no real
clock — a deterministic fake clock drives SLA escalation.

Run:
    python -m src.experiments.hitl_routing.hitl_routing_experiment
or:
    python src/experiments/hitl_routing/hitl_routing_experiment.py
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


DEFAULT_SLA_HOURS = 48
ADMIN_QUEUE = "ADMIN_QUEUE"
TZ = timezone(timedelta(hours=7))


def resolve_project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def experiment_root() -> Path:
    return Path(__file__).resolve().parent


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_ts(text: str) -> datetime:
    return datetime.fromisoformat(text)


def fmt_ts(ts: datetime) -> str:
    return ts.isoformat()


@dataclass
class Course:
    course_code: str
    name: str
    sla_hours: int = DEFAULT_SLA_HOURS


@dataclass
class User:
    user_id: str
    full_name: str
    role: str


@dataclass
class Assignment:
    user_id: str
    course_code: str
    is_active: bool


@dataclass
class Document:
    document_id: str
    course_code: str
    uploader_id: str
    contribution_type: str
    title: str
    needs_review_at: datetime
    state: str = "NEEDS_REVIEW"
    flags: list[str] = field(default_factory=list)
    decision: str | None = None
    decided_by: str | None = None
    decided_at: datetime | None = None


@dataclass
class RouterState:
    courses: dict[str, Course]
    users: dict[str, User]
    assignments: list[Assignment]
    documents: dict[str, Document]
    # queue_name -> list of document_ids (order = arrival order)
    queues: dict[str, list[str]] = field(default_factory=dict)
    audit: list[dict[str, Any]] = field(default_factory=list)
    snapshots: list[dict[str, Any]] = field(default_factory=list)

    def active_reviewers(self, course_code: str) -> list[str]:
        return [a.user_id for a in self.assignments if a.course_code == course_code and a.is_active]

    def sla_hours(self, course_code: str) -> int:
        course = self.courses.get(course_code)
        return course.sla_hours if course else DEFAULT_SLA_HOURS

    def queue_for(self, name: str) -> list[str]:
        return self.queues.setdefault(name, [])

    def log(self, now: datetime, event: str, **fields: Any) -> None:
        entry = {"timestamp": fmt_ts(now), "event": event, **fields}
        self.audit.append(entry)

    def snapshot(self, label: str, now: datetime) -> None:
        self.snapshots.append(
            {
                "label": label,
                "timestamp": fmt_ts(now),
                "queues": {name: list(items) for name, items in self.queues.items() if items},
                "documents": {
                    doc.document_id: {
                        "state": doc.state,
                        "flags": list(doc.flags),
                        "decision": doc.decision,
                        "decided_by": doc.decided_by,
                    }
                    for doc in self.documents.values()
                },
            }
        )


def load_state(mock_dir: Path) -> RouterState:
    courses = {c["course_code"]: Course(**c) for c in read_json(mock_dir / "courses.json")}
    users = {u["user_id"]: User(**u) for u in read_json(mock_dir / "users.json")}
    assignments = [
        Assignment(user_id=a["user_id"], course_code=a["course_code"], is_active=a["is_active"])
        for a in read_json(mock_dir / "assignments.json")
    ]
    documents: dict[str, Document] = {}
    for raw in read_json(mock_dir / "documents.json"):
        documents[raw["document_id"]] = Document(
            document_id=raw["document_id"],
            course_code=raw["course_code"],
            uploader_id=raw["uploader_id"],
            contribution_type=raw["contribution_type"],
            title=raw["title"],
            needs_review_at=parse_ts(raw["needs_review_at"]),
        )
    return RouterState(courses=courses, users=users, assignments=assignments, documents=documents)


def route_on_needs_review(state: RouterState, doc: Document, now: datetime) -> dict[str, Any]:
    """Enqueue ``doc`` to reviewer queue(s) or admin queue. Returns routing result."""
    reviewers = state.active_reviewers(doc.course_code)
    if reviewers:
        for reviewer_id in reviewers:
            queue = state.queue_for(reviewer_id)
            if doc.document_id not in queue:
                queue.append(doc.document_id)
        result = {"target_queues": list(reviewers), "flags": []}
    else:
        if "no_reviewer" not in doc.flags:
            doc.flags.append("no_reviewer")
        queue = state.queue_for(ADMIN_QUEUE)
        if doc.document_id not in queue:
            queue.append(doc.document_id)
        result = {"target_queues": [ADMIN_QUEUE], "flags": ["no_reviewer"]}
    state.log(
        now,
        "route_on_needs_review",
        document_id=doc.document_id,
        course_code=doc.course_code,
        target_queues=result["target_queues"],
        flags=result["flags"],
    )
    return result


def _remove_doc_from_all_queues(state: RouterState, document_id: str) -> list[str]:
    removed_from: list[str] = []
    for queue_name, items in state.queues.items():
        if document_id in items:
            items.remove(document_id)
            removed_from.append(queue_name)
    return removed_from


def reviewer_action(
    state: RouterState,
    doc: Document,
    reviewer_id: str,
    decision: str,
    now: datetime,
    note: str | None = None,
) -> dict[str, Any]:
    """Apply a reviewer/admin decision; remove the doc from all queues."""
    if decision not in {"APPROVE", "REJECT"}:
        raise ValueError(f"Unsupported decision: {decision}")
    if doc.state in {"APPROVED", "REJECTED"}:
        state.log(
            now,
            "reviewer_action_rejected",
            document_id=doc.document_id,
            reviewer_id=reviewer_id,
            reason=f"already_{doc.state.lower()}",
        )
        return {"applied": False, "reason": f"already_{doc.state.lower()}"}

    removed_from = _remove_doc_from_all_queues(state, doc.document_id)
    doc.state = "APPROVED" if decision == "APPROVE" else "REJECTED"
    doc.decision = decision
    doc.decided_by = reviewer_id
    doc.decided_at = now
    state.log(
        now,
        "reviewer_action",
        document_id=doc.document_id,
        reviewer_id=reviewer_id,
        decision=decision,
        removed_from=removed_from,
        note=note,
    )
    return {"applied": True, "removed_from": removed_from, "new_state": doc.state}


def reassign_to_reviewer(state: RouterState, doc: Document, reviewer_id: str, now: datetime) -> None:
    if doc.state != "NEEDS_REVIEW":
        return
    _remove_doc_from_all_queues(state, doc.document_id)
    state.queue_for(reviewer_id).append(doc.document_id)
    state.log(
        now,
        "admin_reassign",
        document_id=doc.document_id,
        target_reviewer=reviewer_id,
    )


def tick(state: RouterState, now: datetime) -> list[str]:
    """Advance the fake clock. Escalate any SLA-breached docs to the admin queue."""
    escalated: list[str] = []
    for doc in state.documents.values():
        if doc.state != "NEEDS_REVIEW":
            continue
        if "sla_breached" in doc.flags or "no_reviewer" in doc.flags:
            # already in admin queue (no_reviewer was an immediate escalation)
            continue
        deadline = doc.needs_review_at + timedelta(hours=state.sla_hours(doc.course_code))
        if now >= deadline:
            doc.flags.append("sla_breached")
            _remove_doc_from_all_queues(state, doc.document_id)
            state.queue_for(ADMIN_QUEUE).append(doc.document_id)
            state.log(
                now,
                "sla_escalation",
                document_id=doc.document_id,
                course_code=doc.course_code,
                sla_hours=state.sla_hours(doc.course_code),
                deadline=fmt_ts(deadline),
            )
            escalated.append(doc.document_id)
    return escalated


# ---------------------------------------------------------------------------
# Scripted scenario
# ---------------------------------------------------------------------------


def run_scenario(state: RouterState) -> dict[str, Any]:
    """Walk through all four paths:

    1. Normal review            (doc-001, single reviewer acts within SLA)
    2. First-acts-wins          (doc-002, two reviewers race; first wins)
    3. no_reviewer immediate    (doc-006, IT3292E has 0 active reviewers)
    4. sla_breached escalation  (doc-005, IT3160E SLA expires before action)
    Plus: admin reassign        (doc-009 admin reroutes to reviewer-001)
    """
    assertions: list[dict[str, Any]] = []

    def assert_that(label: str, condition: bool, expected: Any, actual: Any) -> None:
        assertions.append(
            {"label": label, "passed": bool(condition), "expected": expected, "actual": actual}
        )

    t0 = parse_ts("2026-05-20T08:00:00+07:00")

    # Route every doc as it enters NEEDS_REVIEW (sorted by timestamp).
    docs_sorted = sorted(state.documents.values(), key=lambda d: d.needs_review_at)
    for doc in docs_sorted:
        route_on_needs_review(state, doc, doc.needs_review_at)

    state.snapshot("after_initial_routing", docs_sorted[-1].needs_review_at)

    # Path 3 (no_reviewer): IT3292E + IT3220 docs should already be in admin queue.
    admin_queue = state.queue_for(ADMIN_QUEUE)
    for did in ("doc-006", "doc-007", "doc-008"):
        assert_that(
            f"{did} routed to admin queue (no_reviewer)",
            did in admin_queue and "no_reviewer" in state.documents[did].flags,
            "ADMIN_QUEUE + no_reviewer",
            {"in_admin": did in admin_queue, "flags": state.documents[did].flags},
        )

    # IT3210 has reviewer-001 + reviewer-003. doc-001..003, doc-009 must be in both.
    for did in ("doc-001", "doc-002", "doc-003", "doc-009"):
        in_r1 = did in state.queue_for("reviewer-001")
        in_r3 = did in state.queue_for("reviewer-003")
        assert_that(
            f"{did} fan-out to both IT3210 reviewers",
            in_r1 and in_r3,
            True,
            {"reviewer-001": in_r1, "reviewer-003": in_r3},
        )

    # IT3160E has only reviewer-002.
    for did in ("doc-004", "doc-005"):
        in_r2 = did in state.queue_for("reviewer-002")
        assert_that(
            f"{did} fan-out to single IT3160E reviewer",
            in_r2,
            True,
            {"reviewer-002": in_r2},
        )

    # ---- Path 1: normal review. reviewer-001 approves doc-001 at t+2h.
    t_normal = t0 + timedelta(hours=2)
    reviewer_action(state, state.documents["doc-001"], "reviewer-001", "APPROVE", t_normal)
    assert_that(
        "doc-001 approved + removed from reviewer-003 queue",
        state.documents["doc-001"].state == "APPROVED"
        and "doc-001" not in state.queue_for("reviewer-003"),
        "APPROVED, removed from other queues",
        {
            "state": state.documents["doc-001"].state,
            "in_r3": "doc-001" in state.queue_for("reviewer-003"),
        },
    )

    # ---- Path 2: first-acts-wins race. reviewer-003 rejects doc-002 first.
    t_race = t0 + timedelta(hours=3)
    reviewer_action(state, state.documents["doc-002"], "reviewer-003", "REJECT", t_race)
    # reviewer-001 tries to act after the fact — should no-op.
    late = reviewer_action(
        state, state.documents["doc-002"], "reviewer-001", "APPROVE", t_race + timedelta(minutes=5)
    )
    assert_that(
        "doc-002 first-acts-wins (reviewer-003 rejected)",
        state.documents["doc-002"].state == "REJECTED"
        and state.documents["doc-002"].decided_by == "reviewer-003"
        and not late["applied"],
        "REJECTED by reviewer-003, late action rejected",
        {
            "state": state.documents["doc-002"].state,
            "decided_by": state.documents["doc-002"].decided_by,
            "late_applied": late["applied"],
        },
    )

    state.snapshot("after_normal_and_race", t_race + timedelta(minutes=10))

    # ---- Tick forward 12h — nothing should have breached yet.
    t_12h = t0 + timedelta(hours=12)
    escalated_12 = tick(state, t_12h)
    assert_that(
        "no SLA breach by t+12h",
        escalated_12 == [],
        [],
        escalated_12,
    )

    # ---- Tick forward to t+30h — IT3160E (SLA=72h) not breached, IT3210 (48h) not breached.
    t_30h = t0 + timedelta(hours=30)
    escalated_30 = tick(state, t_30h)
    assert_that(
        "no SLA breach by t+30h",
        escalated_30 == [],
        [],
        escalated_30,
    )

    # ---- Tick forward to t+50h — only doc-003 (IT3210, NRA=t0+2h, SLA=48h) breaches.
    # doc-009 (NRA=t0+8h) deadline is t0+56h, not yet breached.
    t_50h = t0 + timedelta(hours=50)
    escalated_50 = tick(state, t_50h)
    expected_50 = {"doc-003"}
    assert_that(
        "doc-003 breaches at t+50h (others still within SLA)",
        set(escalated_50) == expected_50,
        sorted(expected_50),
        sorted(escalated_50),
    )
    assert_that(
        "doc-003 in admin queue with sla_breached flag",
        "doc-003" in state.queue_for(ADMIN_QUEUE)
        and "sla_breached" in state.documents["doc-003"].flags,
        "ADMIN_QUEUE + sla_breached",
        {
            "in_admin": "doc-003" in state.queue_for(ADMIN_QUEUE),
            "flags": state.documents["doc-003"].flags,
        },
    )

    state.snapshot("after_sla_breach_t+50h", t_50h)

    # ---- Admin reassigns doc-009 back to reviewer-001 (admin recovery path).
    # doc-009 is still NEEDS_REVIEW in reviewer queues at this point.
    reassign_to_reviewer(state, state.documents["doc-009"], "reviewer-001", t_50h + timedelta(minutes=15))
    assert_that(
        "doc-009 reassigned to reviewer-001 only (removed from reviewer-003)",
        "doc-009" in state.queue_for("reviewer-001")
        and "doc-009" not in state.queue_for("reviewer-003"),
        "in reviewer-001 queue, removed from reviewer-003",
        {
            "in_r1": "doc-009" in state.queue_for("reviewer-001"),
            "in_r3": "doc-009" in state.queue_for("reviewer-003"),
        },
    )

    # ---- Admin directly approves doc-006 (no_reviewer path resolution).
    reviewer_action(
        state,
        state.documents["doc-006"],
        "admin-001",
        "APPROVE",
        t_50h + timedelta(minutes=30),
        note="Admin direct approval for orphan course IT3292E",
    )
    assert_that(
        "admin directly approved no_reviewer doc-006",
        state.documents["doc-006"].state == "APPROVED"
        and state.documents["doc-006"].decided_by == "admin-001",
        "APPROVED by admin-001",
        {
            "state": state.documents["doc-006"].state,
            "decided_by": state.documents["doc-006"].decided_by,
        },
    )

    # ---- Tick forward past IT3160E SLA (72h). doc-004/005 (IT3160E) breach;
    # doc-009 also breaches (reassign did not reset needs_review_at — by spec, SLA
    # is anchored to NEEDS_REVIEW entry, not to reassignment).
    t_80h = t0 + timedelta(hours=80)
    escalated_80 = tick(state, t_80h)
    expected_80 = {"doc-004", "doc-005", "doc-009"}
    assert_that(
        "IT3160E + leftover IT3210 docs breach at t+80h",
        set(escalated_80) == expected_80,
        sorted(expected_80),
        sorted(escalated_80),
    )

    state.snapshot("final_state", t_80h)

    return {
        "assertions": assertions,
        "passed": sum(1 for a in assertions if a["passed"]),
        "failed": sum(1 for a in assertions if not a["passed"]),
        "total": len(assertions),
    }


def main() -> int:
    root = experiment_root()
    state = load_state(root / "mock_data")
    summary = run_scenario(state)

    results_dir = root / "results"
    write_json(results_dir / "scenario_log.json", state.audit)
    write_json(results_dir / "queue_snapshots.json", state.snapshots)
    write_json(
        results_dir / "scenario_assertions.json",
        {
            "passed": summary["passed"],
            "failed": summary["failed"],
            "total": summary["total"],
            "assertions": summary["assertions"],
        },
    )

    print(
        json.dumps(
            {
                "passed": summary["passed"],
                "failed": summary["failed"],
                "total": summary["total"],
                "audit_entries": len(state.audit),
                "snapshots": len(state.snapshots),
                "results_dir": str(results_dir.relative_to(resolve_project_root())),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if summary["failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
