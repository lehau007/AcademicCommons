from abc import ABC, abstractmethod
from pathlib import Path
from uuid import UUID


def raw_document_key(course_id: UUID, document_id: UUID, filename: str) -> str:
    return f"documents/{course_id}/{document_id}/raw/{filename}"


def markdown_document_key(course_id: UUID, document_id: UUID) -> str:
    return f"documents/{course_id}/{document_id}/markdown/output.md"


def pagemap_document_key(course_id: UUID, document_id: UUID) -> str:
    return f"documents/{course_id}/{document_id}/markdown/pagemap.json"


class StorageClient(ABC):
    @abstractmethod
    async def put_object(self, key: str, source: bytes | Path, content_type: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def get_object(self, key: str) -> bytes:
        raise NotImplementedError

    @abstractmethod
    async def generate_signed_url(self, key: str, ttl: int = 900) -> str:
        raise NotImplementedError

    @abstractmethod
    async def delete_object(self, key: str) -> None:
        raise NotImplementedError
