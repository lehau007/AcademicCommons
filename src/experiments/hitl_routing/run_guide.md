# Experiment E4 — HITL Routing + SLA Escalation

Pure-logic simulation of the review-routing rules from
`.agent/project_description.md` Sections 5 (Reviewer Assignment Model) and 6.2
(Review Routing + SLA Configuration). No LLM calls, no real clock — a
deterministic fake clock drives SLA escalation.

## Layout

```
src/experiments/hitl_routing/
  mock_data/
    courses.json        # 4 courses with varied SLA (24h / 48h / 72h)
    users.json          # 1 admin, 3 reviewers, 5 students
    assignments.json    # IT3210 -> 2 reviewers, IT3160E -> 1, IT3292E -> 0 (inactive only), IT3220 -> 0
    documents.json      # 9 community contributions entering NEEDS_REVIEW
  hitl_routing_experiment.py
  results/
    scenario_log.json         # full audit trail
    queue_snapshots.json      # queue state at 4 key ticks
    scenario_assertions.json  # assertion results
```

## How to Run

```bash
python3 src/experiments/hitl_routing/hitl_routing_experiment.py
```

Exit code `0` means all assertions passed.

## Public API (importable functions in `hitl_routing_experiment.py`)

- `route_on_needs_review(state, doc, now)` — Look up active `CourseReviewerAssignment` rows. If ≥1 reviewer, fan-out to all of them. If 0 reviewers, route directly to `ADMIN_QUEUE` with the `no_reviewer` flag (immediate escalation, no SLA wait). Returns `{"target_queues": [...], "flags": [...]}`.
- `reviewer_action(state, doc, reviewer_id, decision, now, note=None)` — Apply APPROVE/REJECT, remove the doc from **all** queues (first-acts-wins). Re-acting on a closed doc is a no-op logged as `reviewer_action_rejected`. Admin uses the same function (`reviewer_id="admin-001"`).
- `reassign_to_reviewer(state, doc, reviewer_id, now)` — Admin recovery path. Removes the doc from every queue and pushes it onto the chosen reviewer's queue. Does **not** reset `needs_review_at`, so the SLA clock keeps running from the original NEEDS_REVIEW timestamp.
- `tick(state, now)` — Advance the fake clock. Any NEEDS_REVIEW doc whose course SLA deadline (`needs_review_at + sla_hours`) has passed gets moved to `ADMIN_QUEUE` with the `sla_breached` flag. Docs already flagged `no_reviewer` are skipped (they're already with admin).

## Scripted Scenario — all four paths

| t (offset from 2026-05-20 08:00 +07) | Event | Path under test |
|--------------------------------------|-------|-----------------|
| t+0h … t+8h | Initial routing for 9 docs | Fan-out + `no_reviewer` immediate escalation |
| t+2h | reviewer-001 approves doc-001 | **Path 1 — Normal review** |
| t+3h | reviewer-003 rejects doc-002 first; reviewer-001 acts 5 min later | **Path 2 — First-acts-wins** |
| Routing time | doc-006 / doc-007 (IT3292E) and doc-008 (IT3220) go straight to admin | **Path 3 — no_reviewer** |
| t+12h, t+30h | Ticks — nothing breached | SLA negative case |
| t+50h | doc-003 (IT3210 SLA 48h, NRA t+2h) breaches → admin queue | **Path 4 — sla_breached** |
| t+50h+15m | Admin reassigns doc-009 to reviewer-001 | Admin reassign path |
| t+50h+30m | Admin directly approves doc-006 | Admin direct review of orphan |
| t+80h | IT3160E (SLA 72h) doc-004/doc-005 + leftover doc-009 breach | SLA breach across courses |

## Expected vs Actual Outcomes

| Assertion | Expected | Actual |
|-----------|----------|--------|
| doc-006/007/008 in `ADMIN_QUEUE` with `no_reviewer` | ✓ | ✓ |
| doc-001/002/003/009 in both reviewer-001 and reviewer-003 queues | ✓ | ✓ |
| doc-004/005 in reviewer-002 queue | ✓ | ✓ |
| doc-001 → APPROVED, removed from reviewer-003 | ✓ | ✓ |
| doc-002 → REJECTED by reviewer-003; late reviewer-001 call no-ops | ✓ | ✓ |
| No SLA breach at t+12h, t+30h | ✓ | ✓ |
| doc-003 breaches at t+50h, lands in admin queue with `sla_breached` | ✓ | ✓ |
| doc-009 reassign removes it from reviewer-003 queue | ✓ | ✓ |
| admin-001 can directly close doc-006 (`no_reviewer` orphan) | ✓ | ✓ |
| At t+80h, escalations = {doc-004, doc-005, doc-009} | ✓ | ✓ |

Result: **15 / 15 assertions passed.**

## Spec Ambiguity Notes

1. **Reassignment SLA reset.** Section 6.2 does not say whether admin reassignment resets the SLA clock. This experiment treats `needs_review_at` as immutable — SLA is anchored to the original NEEDS_REVIEW entry. That matches the literal wording "after SLA expiry … the document is moved to the Admin review queue" but means a reassigned doc can breach a second time.
2. **`no_reviewer` vs `sla_breached` ordering.** Spec says immediate escalation when no reviewer exists. Implementation sets `no_reviewer` at routing time and skips those docs during SLA ticks (admin already has them), so they never accumulate both flags. If both were desired, only the `tick` skip condition needs to change.
3. **Queue ordering.** Spec is silent on intra-queue ordering. Implementation uses arrival order (append).
4. **Late actor behavior.** Spec implies first-acts-wins removes the doc from other queues but is silent on what happens if a stale UI submits a decision afterward. Implementation rejects the late action with `already_<state>` and logs it for audit.

## Relationship to E1 (LangGraph evaluation flow)

`src/experiments/evaluation_agentstate/document_evaluation_langgraph.py` defines
`has_active_reviewer`, `sla_breached`, and `queue_route` fields on
`EvaluationState` but only stubs the routing logic. This experiment is the
standalone, fully-exercised version of that routing layer and can be wired into
the langgraph nodes later without touching the existing evaluation pipeline.
