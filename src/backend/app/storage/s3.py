import asyncio
import os
from contextlib import contextmanager
from collections.abc import Iterator
from pathlib import Path

import boto3
from botocore.client import Config

from app.config import Settings
from app.storage.client import StorageClient


@contextmanager
def _without_aws_profile() -> Iterator[None]:
    """Detach from any ambient AWS_PROFILE while building the S3 client.

    We pass explicit storage credentials, so no profile is needed. A malformed
    or empty AWS_PROFILE (e.g. one polluted by an inline `# ...` comment in an
    env file) otherwise makes botocore raise ProfileNotFound during client
    construction. Profile resolution only happens at construction time, so
    restoring the value afterwards is safe.
    """
    saved = os.environ.pop("AWS_PROFILE", None)
    try:
        yield
    finally:
        if saved is not None:
            os.environ["AWS_PROFILE"] = saved


class S3CompatibleStorage(StorageClient):
    def __init__(self, settings: Settings, client_config: Config | None = None) -> None:
        self._bucket = settings.storage_bucket
        self._internal_endpoint = settings.storage_endpoint.rstrip("/")
        self._public_host = settings.storage_public_host.rstrip("/")
        with _without_aws_profile():
            session = boto3.Session()
            self._client = session.client(
                "s3",
                endpoint_url=settings.storage_endpoint,
                aws_access_key_id=settings.storage_access_key,
                aws_secret_access_key=settings.storage_secret_key,
                config=client_config or Config(signature_version="s3v4"),
                region_name="auto",
            )
            self._public_client = session.client(
                "s3",
                endpoint_url=settings.storage_public_host,
                aws_access_key_id=settings.storage_access_key,
                aws_secret_access_key=settings.storage_secret_key,
                config=client_config or Config(signature_version="s3v4"),
                region_name="auto",
            )

    async def ensure_bucket(self) -> None:
        def _ensure() -> None:
            existing = self._client.list_buckets().get("Buckets", [])
            if not any(bucket["Name"] == self._bucket for bucket in existing):
                self._client.create_bucket(Bucket=self._bucket)

        await asyncio.to_thread(_ensure)

    async def put_object(self, key: str, source: bytes | Path, content_type: str) -> str:
        body = source.read_bytes() if isinstance(source, Path) else source
        await asyncio.to_thread(
            self._client.put_object,
            Bucket=self._bucket,
            Key=key,
            Body=body,
            ContentType=content_type,
        )
        return key

    async def get_object(self, key: str) -> bytes:
        response = await asyncio.to_thread(self._client.get_object, Bucket=self._bucket, Key=key)
        return await asyncio.to_thread(response["Body"].read)

    async def delete_object(self, key: str) -> None:
        await asyncio.to_thread(self._client.delete_object, Bucket=self._bucket, Key=key)

    async def generate_signed_url(self, key: str, ttl: int = 900) -> str:
        url: str = await asyncio.to_thread(
            self._public_client.generate_presigned_url,
            "get_object",
            Params={"Bucket": self._bucket, "Key": key},
            ExpiresIn=ttl,
        )
        return url


async def check_storage(settings: Settings) -> str:
    try:
        probe_config = Config(signature_version="s3v4", connect_timeout=1, read_timeout=1, retries={"max_attempts": 1})
        storage = S3CompatibleStorage(settings, client_config=probe_config)
        await storage.ensure_bucket()
    except Exception:
        return "unavailable"
    return "ok"
