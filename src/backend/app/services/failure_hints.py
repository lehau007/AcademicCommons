"""Map raw pipeline failure strings to actionable, user-friendly suggestions.

Failed documents store the raw exception text (``job.failure_reason``), which is
useful for engineers but opaque for students. ``friendly_failure`` translates the
common causes (encrypted PDF, unsupported format, empty scan, timeout, ...) into a
concrete Vietnamese suggestion the uploader can act on.
"""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import EvaluationJob, ProcessingJob
from app.models.enums import JobStatus, ProcessingJobType

# First matching group wins. Keywords are matched case-insensitively against the
# raw failure text.
_PATTERNS: list[tuple[tuple[str, ...], str]] = [
    (
        ("encrypt", "password", "/encrypt"),
        "Tệp PDF đang bị mã hoá hoặc đặt mật khẩu. Vui lòng gỡ mật khẩu rồi tải lại.",
    ),
    (
        ("unsupported file format", "unsupported", "cannot identify image", "not a valid"),
        "Định dạng tệp hoặc ảnh không được hỗ trợ. Hệ thống chỉ hỗ trợ PDF, PPTX, PNG, JPG.",
    ),
    (
        ("timed out", "timeout"),
        "Quá trình xử lý vượt quá thời gian cho phép. Hãy thử lại với tệp nhỏ/nhẹ hơn.",
    ),
    (
        ("empty", "no text", "no content", "no extractable", "0 pages"),
        "Không trích xuất được nội dung. Tệp có thể là ảnh scan mờ hoặc không có văn bản — "
        "hãy dùng bản rõ nét hơn.",
    ),
    (
        ("corrupt", "damaged", "eof marker", "broken"),
        "Tệp có thể bị hỏng. Hãy mở lại và xuất/tải lên một bản mới.",
    ),
]

_JOB_FALLBACK: dict[str, str] = {
    "ocr": "Lỗi khi trích xuất văn bản (OCR) từ tài liệu. Hãy kiểm tra tệp không bị hỏng/mã hoá rồi tải lại.",
    "index": "Lỗi khi lập chỉ mục tài liệu. Vui lòng thử lại hoặc liên hệ quản trị viên.",
    "eval": "Lỗi khi đánh giá nội dung tài liệu. Vui lòng thử lại hoặc liên hệ quản trị viên.",
}

_GENERIC = "Hệ thống gặp sự cố khi xử lý tài liệu. Vui lòng thử lại hoặc liên hệ quản trị viên."


def friendly_failure(raw_reason: str | None, job_type: str) -> str:
    """Translate a raw failure string + job type into an actionable suggestion."""
    text = (raw_reason or "").lower()
    for keywords, suggestion in _PATTERNS:
        if any(keyword in text for keyword in keywords):
            return suggestion
    return _JOB_FALLBACK.get(job_type, _GENERIC)


async def get_failure_hints(session: AsyncSession, document_ids: list[UUID]) -> dict[UUID, str]:
    """Map each FAILED document id to a user-friendly failure suggestion.

    Considers the latest failed job, preferring OCR → INDEX → EVAL (the order in
    which the pipeline runs), so the suggestion reflects the earliest breakage.
    """
    if not document_ids:
        return {}

    processing_rows = await session.execute(
        select(ProcessingJob).where(
            ProcessingJob.document_id.in_(document_ids),
            ProcessingJob.is_latest.is_(True),
            ProcessingJob.status == JobStatus.FAILED,
        )
    )
    ocr_jobs: dict[UUID, ProcessingJob] = {}
    index_jobs: dict[UUID, ProcessingJob] = {}
    for job in processing_rows.scalars():
        if job.job_type == ProcessingJobType.OCR:
            ocr_jobs[job.document_id] = job
        elif job.job_type == ProcessingJobType.INDEX:
            index_jobs[job.document_id] = job

    eval_rows = await session.execute(
        select(EvaluationJob).where(
            EvaluationJob.document_id.in_(document_ids),
            EvaluationJob.is_latest.is_(True),
            EvaluationJob.status == JobStatus.FAILED,
        )
    )
    eval_jobs = {job.document_id: job for job in eval_rows.scalars()}

    hints: dict[UUID, str] = {}
    for doc_id in document_ids:
        if doc_id in ocr_jobs:
            hints[doc_id] = friendly_failure(ocr_jobs[doc_id].failure_reason, "ocr")
        elif doc_id in index_jobs:
            hints[doc_id] = friendly_failure(index_jobs[doc_id].failure_reason, "index")
        elif doc_id in eval_jobs:
            hints[doc_id] = friendly_failure(eval_jobs[doc_id].failure_reason, "eval")
    return hints
