import hashlib
import os
from uuid import uuid4

import httpx
import pytest

from app.config import Settings
from app.storage.client import raw_document_key
from app.storage.s3 import S3CompatibleStorage

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_STORAGE_INTEGRATION") != "1",
    reason="Set RUN_STORAGE_INTEGRATION=1 with MinIO running to execute storage integration tests.",
)


@pytest.mark.asyncio
async def test_minio_put_signed_url_and_fetch_round_trip() -> None:
    settings = Settings()
    storage = S3CompatibleStorage(settings)
    await storage.ensure_bucket()

    payload = b"%PDF-1.4\n" + (b"0" * (5 * 1024 * 1024))
    key = raw_document_key(uuid4(), uuid4(), "sample.pdf")

    await storage.put_object(key, payload, "application/pdf")
    signed_url = await storage.generate_signed_url(key, ttl=900)

    async with httpx.AsyncClient() as client:
        response = await client.get(signed_url)

    assert response.status_code == 200
    assert hashlib.sha256(response.content).hexdigest() == hashlib.sha256(payload).hexdigest()
