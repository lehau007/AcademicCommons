from __future__ import annotations

import asyncio
import uuid
from contextlib import asynccontextmanager

import pytest

from app.models.enums import DocumentStatus, JobStatus
from app.workers import eval_worker


class _FakeDocument:
    def __init__(self, status: DocumentStatus) -> None:
        self.id = uuid.uuid4()
        self.status = status


class _FakeEvaluationJob:
    def __init__(self) -> None:
        self.id = uuid.uuid4()
        self.attempt_count = 0
        self.status = JobStatus.PENDING
        self.failure_reason: str | None = None
        self.raw_failure_output: dict[str, object] | None = None
        self.completed_at = None
        self.updated_at = None


class _FakeSession:
    """Minimal stand-in for AsyncSession: only the methods eval_worker touches."""

    def __init__(self, job: _FakeEvaluationJob, document: _FakeDocument) -> None:
        self._job = job
        self._document = document
        self.added: list[object] = []
        self.committed = False

    async def scalar(self, stmt: object) -> object:
        # Both lookups in _record_eval_failure select by primary-key-ish filters;
        # returning by declared model type keeps this fake trivial.
        compiled = str(stmt)
        if "evaluation_jobs" in compiled:
            return self._job
        if "documents" in compiled:
            return self._document
        return None

    def add(self, obj: object) -> None:
        self.added.append(obj)

    async def commit(self) -> None:
        self.committed = True

    async def flush(self) -> None:
        pass


def _patch_session(monkeypatch: pytest.MonkeyPatch, job: _FakeEvaluationJob, document: _FakeDocument) -> _FakeSession:
    session = _FakeSession(job, document)

    @asynccontextmanager
    async def _fake_session_local():
        yield session

    monkeypatch.setattr(eval_worker, "AsyncSessionLocal", _fake_session_local)
    return session


def test_record_eval_failure_stays_pending_before_max_tries(monkeypatch: pytest.MonkeyPatch) -> None:
    job = _FakeEvaluationJob()
    document = _FakeDocument(DocumentStatus.EVALUATING)
    _patch_session(monkeypatch, job, document)

    asyncio.run(
        eval_worker._record_eval_failure(
            document_id=document.id,
            evaluation_job_id=job.id,
            exc=RuntimeError("boom"),
        )
    )

    assert job.attempt_count == 1
    assert job.status == JobStatus.PENDING
    assert document.status == DocumentStatus.EVALUATING


def test_record_eval_failure_flips_to_failed_after_max_tries(monkeypatch: pytest.MonkeyPatch) -> None:
    job = _FakeEvaluationJob()
    document = _FakeDocument(DocumentStatus.EVALUATING)
    session = _patch_session(monkeypatch, job, document)

    # Simulate repeated failures across separately-enqueued arq jobs (e.g. the
    # hourly recovery cron), each of which sees ctx["job_try"] reset to 1 —
    # attempt_count must still accumulate to the persisted cap.
    for _ in range(eval_worker.EVAL_MAX_TRIES):
        asyncio.run(
            eval_worker._record_eval_failure(
                document_id=document.id,
                evaluation_job_id=job.id,
                exc=RuntimeError("boom"),
            )
        )

    assert job.attempt_count == eval_worker.EVAL_MAX_TRIES
    assert job.status == JobStatus.FAILED
    assert job.completed_at is not None
    assert document.status == DocumentStatus.FAILED
    assert session.committed is True


def test_record_eval_failure_does_not_exceed_max_tries_cap(monkeypatch: pytest.MonkeyPatch) -> None:
    job = _FakeEvaluationJob()
    document = _FakeDocument(DocumentStatus.EVALUATING)
    _patch_session(monkeypatch, job, document)

    for _ in range(eval_worker.EVAL_MAX_TRIES + 2):
        asyncio.run(
            eval_worker._record_eval_failure(
                document_id=document.id,
                evaluation_job_id=job.id,
                exc=RuntimeError("boom"),
            )
        )

    assert job.attempt_count == eval_worker.EVAL_MAX_TRIES
