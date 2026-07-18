from typing import Any

from arq import cron
from arq.connections import RedisSettings
from arq.worker import func as arq_func

from app.config import get_settings
from app.services.retrieval_service import build_embedding_service
from app.workers.eval_worker import check_sla_breaches, process_eval_job
from app.workers.index_worker import process_index_job
from app.workers.jobs import EVAL_QUEUE, INDEX_QUEUE, OCR_QUEUE
from app.workers.ocr_worker import process_ocr_job
from app.workers.recovery_worker import recover_stale_pending_jobs

settings = get_settings()


async def startup(ctx: dict[str, Any]) -> None:
    ctx["settings"] = settings
    ctx["embedding_service"] = build_embedding_service(settings)


async def worker_healthcheck(ctx: dict[str, Any]) -> str:
    return "ok"


class WorkerSettings:
    redis_settings = RedisSettings.from_dsn(settings.redis_url)
    on_startup = startup
    functions: list[Any] = [worker_healthcheck]
    max_jobs = settings.worker_ocr_concurrency + settings.worker_eval_concurrency + settings.worker_index_concurrency
    max_tries = 3


class OcrWorkerSettings:
    queue_name = OCR_QUEUE
    redis_settings = RedisSettings.from_dsn(settings.redis_url)
    on_startup = startup
    functions: list[Any] = [
        arq_func(
            process_ocr_job,
            name="process_ocr_job",
            max_tries=3,
            timeout=settings.worker_ocr_job_timeout_seconds,
        ),
        worker_healthcheck,
    ]
    max_jobs = settings.worker_ocr_concurrency
    max_tries = 3


class EvalWorkerSettings:
    queue_name = EVAL_QUEUE
    redis_settings = RedisSettings.from_dsn(settings.redis_url)
    on_startup = startup
    functions: list[Any] = [
        arq_func(process_eval_job, name="process_eval_job", max_tries=3),
        worker_healthcheck,
    ]
    cron_jobs = [
        cron(check_sla_breaches, name="check_sla_breaches", minute={0, 15, 30, 45}, max_tries=1),
        cron(recover_stale_pending_jobs, name="recover_stale_pending_jobs", minute={5, 20, 35, 50}, max_tries=1),
    ]
    max_jobs = settings.worker_eval_concurrency
    max_tries = 3


class IndexWorkerSettings:
    queue_name = INDEX_QUEUE
    redis_settings = RedisSettings.from_dsn(settings.redis_url)
    on_startup = startup
    functions: list[Any] = [
        arq_func(process_index_job, name="process_index_job", max_tries=3),
        worker_healthcheck,
    ]
    max_jobs = settings.worker_index_concurrency
    max_tries = 3
