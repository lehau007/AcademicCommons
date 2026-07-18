from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from app.models import EvaluationJob, ProcessingJob
from app.models.enums import JobStatus, ProcessingJobType
from app.workers import jobs
from app.workers.queue import EvalWorkerSettings, IndexWorkerSettings, OcrWorkerSettings, settings
from app.workers.recovery_worker import recover_stale_pending_jobs_for_session


class FakeSession:
    def __init__(self, scalars: list[object | None]) -> None:
        self._scalars = list(scalars)

    async def scalar(self, query: object) -> object | None:
        del query
        return self._scalars.pop(0)


class FakePool:
    def __init__(self, enqueue_result: object | None = object()) -> None:
        self.enqueued: list[dict[str, object]] = []
        self.closed = False
        self.enqueue_result = enqueue_result

    async def enqueue_job(self, function: str, payload: dict[str, str], **kwargs: object) -> object | None:
        self.enqueued.append({"function": function, "payload": payload, **kwargs})
        return self.enqueue_result

    async def close(self) -> None:
        self.closed = True


class FakeScalarResult:
    def __init__(self, items: list[object]) -> None:
        self._items = items

    def all(self) -> list[object]:
        return list(self._items)


class FakeRecoverySession:
    def __init__(self, result_sets: list[list[object]]) -> None:
        self._result_sets = list(result_sets)

    async def scalars(self, query: object) -> FakeScalarResult:
        del query
        return FakeScalarResult(self._result_sets.pop(0))


def test_ocr_worker_uses_explicit_long_job_timeout() -> None:
    process_job = next(fn for fn in OcrWorkerSettings.functions if getattr(fn, "name", None) == "process_ocr_job")

    assert process_job.timeout_s == settings.worker_ocr_job_timeout_seconds


@pytest.mark.asyncio
async def test_enqueue_ocr_job_uses_stable_arq_id_and_named_queue(monkeypatch: pytest.MonkeyPatch) -> None:
    document_id = uuid4()
    job = ProcessingJob(
        id=uuid4(),
        document_id=document_id,
        job_type=ProcessingJobType.OCR,
        run_number=2,
        is_latest=True,
        status=JobStatus.PENDING,
    )
    session = FakeSession([job, job])
    pool = FakePool()

    async def fake_create_pool(*args: object, **kwargs: object) -> FakePool:
        del args, kwargs
        return pool

    monkeypatch.setattr(jobs.arq, "create_pool", fake_create_pool)

    await jobs.enqueue_ocr_job(session, document_id, job.id)  # type: ignore[arg-type]

    assert pool.closed is True
    assert pool.enqueued == [
        {
            "function": "process_ocr_job",
            "payload": {"document_id": str(document_id), "processing_job_id": str(job.id)},
            "_job_id": f"{document_id}:ocr:2",
            "_queue_name": jobs.OCR_QUEUE,
        }
    ]


@pytest.mark.asyncio
async def test_enqueue_raises_when_arq_rejects_existing_job_key(monkeypatch: pytest.MonkeyPatch) -> None:
    document_id = uuid4()
    job = ProcessingJob(
        id=uuid4(),
        document_id=document_id,
        job_type=ProcessingJobType.OCR,
        run_number=1,
        is_latest=True,
        status=JobStatus.PENDING,
    )
    session = FakeSession([job, job])
    pool = FakePool(enqueue_result=None)

    async def fake_create_pool(*args: object, **kwargs: object) -> FakePool:
        del args, kwargs
        return pool

    monkeypatch.setattr(jobs.arq, "create_pool", fake_create_pool)

    with pytest.raises(jobs.DuplicateQueueJobError, match="Redis job/result storage"):
        await jobs.enqueue_ocr_job(session, document_id, job.id)  # type: ignore[arg-type]

    assert pool.closed is True


@pytest.mark.asyncio
async def test_enqueue_rejects_another_latest_active_processing_job() -> None:
    document_id = uuid4()
    intended_job = ProcessingJob(
        id=uuid4(),
        document_id=document_id,
        job_type=ProcessingJobType.OCR,
        run_number=1,
        is_latest=True,
        status=JobStatus.PENDING,
    )
    active_job = ProcessingJob(
        id=uuid4(),
        document_id=document_id,
        job_type=ProcessingJobType.OCR,
        run_number=2,
        is_latest=True,
        status=JobStatus.RUNNING,
    )

    with pytest.raises(jobs.DuplicateQueueJobError):
        await jobs._validate_enqueue_request(  # noqa: SLF001
            FakeSession([intended_job, active_job]),  # type: ignore[arg-type]
            job_kind="ocr",
            document_id=document_id,
            job_id=intended_job.id,
        )


@pytest.mark.asyncio
async def test_enqueue_allows_ocr_and_eval_for_same_document_independently() -> None:
    document_id = uuid4()
    processing_job = ProcessingJob(
        id=uuid4(),
        document_id=document_id,
        job_type=ProcessingJobType.OCR,
        run_number=1,
        is_latest=True,
        status=JobStatus.PENDING,
    )
    evaluation_job = EvaluationJob(
        id=uuid4(),
        document_id=document_id,
        run_number=1,
        is_latest=True,
        status=JobStatus.PENDING,
    )

    ocr_run = await jobs._validate_enqueue_request(  # noqa: SLF001
        FakeSession([processing_job, processing_job]),  # type: ignore[arg-type]
        job_kind="ocr",
        document_id=document_id,
        job_id=processing_job.id,
    )
    eval_run = await jobs._validate_enqueue_request(  # noqa: SLF001
        FakeSession([evaluation_job, evaluation_job]),  # type: ignore[arg-type]
        job_kind="eval",
        document_id=document_id,
        job_id=evaluation_job.id,
    )

    assert ocr_run == 1
    assert eval_run == 1


def test_phase_c_worker_settings_register_named_functions_and_queues() -> None:
    assert OcrWorkerSettings.queue_name == jobs.OCR_QUEUE
    assert EvalWorkerSettings.queue_name == jobs.EVAL_QUEUE
    assert IndexWorkerSettings.queue_name == jobs.INDEX_QUEUE

    ocr_function = OcrWorkerSettings.functions[0]
    eval_function = EvalWorkerSettings.functions[0]
    index_function = IndexWorkerSettings.functions[0]

    assert ocr_function.name == "process_ocr_job"
    assert eval_function.name == "process_eval_job"
    assert index_function.name == "process_index_job"
    assert ocr_function.max_tries == 3
    assert eval_function.max_tries == 3
    assert index_function.max_tries == 3
    cron_names = {cron_job.name for cron_job in EvalWorkerSettings.cron_jobs}
    assert "check_sla_breaches" in cron_names
    assert "recover_stale_pending_jobs" in cron_names


@pytest.mark.asyncio
async def test_recover_stale_pending_jobs_reenqueues_all_job_kinds() -> None:
    now = datetime.now(UTC)
    ocr_job = ProcessingJob(
        id=uuid4(),
        document_id=uuid4(),
        job_type=ProcessingJobType.OCR,
        run_number=1,
        is_latest=True,
        status=JobStatus.PENDING,
        created_at=now - timedelta(minutes=15),
    )
    index_job = ProcessingJob(
        id=uuid4(),
        document_id=uuid4(),
        job_type=ProcessingJobType.INDEX,
        run_number=1,
        is_latest=True,
        status=JobStatus.PENDING,
        created_at=now - timedelta(minutes=15),
    )
    eval_job = EvaluationJob(
        id=uuid4(),
        document_id=uuid4(),
        run_number=1,
        is_latest=True,
        status=JobStatus.PENDING,
        created_at=now - timedelta(minutes=15),
    )
    session = FakeRecoverySession([[ocr_job, index_job], [eval_job]])
    calls: list[tuple[str, object, object]] = []

    async def ocr_enqueuer(session_arg: object, document_id: object, job_id: object) -> None:
        del session_arg
        calls.append(("ocr", document_id, job_id))

    async def index_enqueuer(session_arg: object, document_id: object, job_id: object) -> None:
        del session_arg
        calls.append(("index", document_id, job_id))

    async def eval_enqueuer(session_arg: object, document_id: object, job_id: object) -> None:
        del session_arg
        calls.append(("eval", document_id, job_id))

    result = await recover_stale_pending_jobs_for_session(
        session,  # type: ignore[arg-type]
        cutoff=now - timedelta(minutes=10),
        ocr_enqueuer=ocr_enqueuer,  # type: ignore[arg-type]
        index_enqueuer=index_enqueuer,  # type: ignore[arg-type]
        eval_enqueuer=eval_enqueuer,  # type: ignore[arg-type]
    )

    assert result == {"recovered": 3, "failed": 0}
    assert calls == [
        ("ocr", ocr_job.document_id, ocr_job.id),
        ("index", index_job.document_id, index_job.id),
        ("eval", eval_job.document_id, eval_job.id),
    ]
