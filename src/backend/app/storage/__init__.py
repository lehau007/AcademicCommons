"""Object storage adapters."""

from __future__ import annotations

from functools import lru_cache

from app.config import get_settings
from app.storage.client import StorageClient
from app.storage.s3 import S3CompatibleStorage


@lru_cache
def get_storage() -> StorageClient:
    return S3CompatibleStorage(get_settings())
