from uuid import UUID

import pytest

from app.config import Settings
from app.storage.client import markdown_document_key, raw_document_key
from app.storage.s3 import S3CompatibleStorage


class FakeS3Body:
    def __init__(self, data: bytes) -> None:
        self._data = data

    def read(self) -> bytes:
        return self._data


class FakeS3Client:
    def __init__(self) -> None:
        self.buckets: set[str] = set()
        self.objects: dict[tuple[str, str], bytes] = {}

    def list_buckets(self) -> dict[str, list[dict[str, str]]]:
        return {"Buckets": [{"Name": bucket} for bucket in sorted(self.buckets)]}

    def create_bucket(self, Bucket: str) -> None:
        self.buckets.add(Bucket)

    def put_object(self, Bucket: str, Key: str, Body: bytes, ContentType: str) -> None:
        self.objects[(Bucket, Key)] = Body

    def get_object(self, Bucket: str, Key: str) -> dict[str, FakeS3Body]:
        return {"Body": FakeS3Body(self.objects[(Bucket, Key)])}

    def generate_presigned_url(self, ClientMethod: str, Params: dict[str, str], ExpiresIn: int) -> str:
        return f"https://storage.test/{Params['Bucket']}/{Params['Key']}?ttl={ExpiresIn}"


def test_document_storage_keys_follow_phase_a_layout() -> None:
    course_id = UUID("00000000-0000-0000-0000-000000000001")
    document_id = UUID("00000000-0000-0000-0000-000000000002")

    assert raw_document_key(course_id, document_id, "lecture.pdf") == (
        "documents/00000000-0000-0000-0000-000000000001/"
        "00000000-0000-0000-0000-000000000002/raw/lecture.pdf"
    )
    assert markdown_document_key(course_id, document_id) == (
        "documents/00000000-0000-0000-0000-000000000001/"
        "00000000-0000-0000-0000-000000000002/markdown/output.md"
    )


@pytest.mark.asyncio
async def test_s3_storage_put_get_signed_url_and_bucket_bootstrap(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_client = FakeS3Client()

    def fake_boto3_client(*args, **kwargs) -> FakeS3Client:
        return fake_client

    class FakeSession:
        def __init__(self, *args, **kwargs) -> None:
            pass

        def client(self, *args, **kwargs) -> FakeS3Client:
            return fake_client

    monkeypatch.setattr("app.storage.s3.boto3.client", fake_boto3_client)
    monkeypatch.setattr("app.storage.s3.boto3.Session", FakeSession)
    storage = S3CompatibleStorage(Settings())

    await storage.ensure_bucket()
    key = await storage.put_object("documents/course/doc/raw/file.pdf", b"%PDF-test", "application/pdf")
    data = await storage.get_object(key)
    url = await storage.generate_signed_url(key, ttl=900)

    assert fake_client.buckets == {"documents"}
    assert data == b"%PDF-test"
    assert url == "https://storage.test/documents/documents/course/doc/raw/file.pdf?ttl=900"
