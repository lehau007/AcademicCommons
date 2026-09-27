from uuid import UUID

import pytest

from app.config import Settings
from app.storage.client import asset_document_key, asset_document_prefix, markdown_document_key, raw_document_key
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

    def list_objects_v2(  # noqa: N803
        self, Bucket: str, Prefix: str, ContinuationToken: str | None = None, MaxKeys: int = 1000
    ) -> dict:
        keys = sorted(k for (b, k) in self.objects if b == Bucket and k.startswith(Prefix))
        start = int(ContinuationToken or 0)
        page = keys[start : start + MaxKeys]
        truncated = start + MaxKeys < len(keys)
        result: dict = {"Contents": [{"Key": k} for k in page], "IsTruncated": truncated}
        if truncated:
            result["NextContinuationToken"] = str(start + MaxKeys)
        return result

    def delete_objects(self, Bucket: str, Delete: dict) -> None:  # noqa: N803
        for item in Delete["Objects"]:
            self.objects.pop((Bucket, item["Key"]), None)


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


def test_asset_keys_live_under_the_document_prefix() -> None:
    course_id = UUID("00000000-0000-0000-0000-000000000001")
    document_id = UUID("00000000-0000-0000-0000-000000000002")

    assert asset_document_key(course_id, document_id, "p001-f1.png") == (
        f"documents/{course_id}/{document_id}/assets/p001-f1.png"
    )
    assert asset_document_prefix(course_id, document_id) == f"documents/{course_id}/{document_id}/assets/"


@pytest.mark.asyncio
async def test_delete_prefix_pages_through_listing(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_client = FakeS3Client()
    monkeypatch.setattr("app.storage.s3.boto3.client", lambda *a, **k: fake_client)

    class FakeSession:
        def __init__(self, *args, **kwargs) -> None:
            pass

        def client(self, *args, **kwargs) -> FakeS3Client:
            return fake_client

    monkeypatch.setattr("app.storage.s3.boto3.Session", FakeSession)
    storage = S3CompatibleStorage(Settings())
    for i in range(1203):
        fake_client.objects[("documents", f"documents/c/d/assets/p{i:04d}-f1.png")] = b"x"
    fake_client.objects[("documents", "documents/c/d/raw/file.pdf")] = b"keep"

    deleted = await storage.delete_prefix("documents/c/d/assets/")

    assert deleted == 1203
    assert list(fake_client.objects) == [("documents", "documents/c/d/raw/file.pdf")]


@pytest.mark.asyncio
async def test_delete_prefix_raises_when_the_batch_delete_reports_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    class ErroringS3Client(FakeS3Client):
        def delete_objects(self, Bucket: str, Delete: dict) -> dict:  # noqa: N803
            # Quiet mode: per-key failures come back in "Errors" and nothing is deleted.
            return {"Errors": [{"Key": item["Key"], "Code": "AccessDenied"} for item in Delete["Objects"]]}

    fake_client = ErroringS3Client()

    class FakeSession:
        def __init__(self, *args, **kwargs) -> None:
            pass

        def client(self, *args, **kwargs) -> FakeS3Client:
            return fake_client

    monkeypatch.setattr("app.storage.s3.boto3.Session", FakeSession)
    storage = S3CompatibleStorage(Settings())
    for i in range(3):
        fake_client.objects[("documents", f"documents/c/d/assets/p{i:03d}-f1.png")] = b"x"

    with pytest.raises(RuntimeError, match="3"):
        await storage.delete_prefix("documents/c/d/assets/")
