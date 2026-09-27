"""In-memory figure/page image assets produced by the pipeline and uploaded by the worker."""

from __future__ import annotations

import re
import threading
from dataclasses import dataclass
from uuid import UUID

ASSET_NAME_RE = re.compile(r"p\d{3,4}-(?:f\d{1,3}|page)\.(?:png|jpg|jpeg)")
_ASSET_REF_RE = re.compile(
    r"asset://(?P<document_id>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/"
    r"(?P<name>p\d{3,4}-(?:f\d{1,3}|page)\.(?:png|jpg|jpeg))"
)


@dataclass(frozen=True)
class Asset:
    name: str
    data: bytes
    content_type: str


def asset_ref(document_id: str, name: str) -> str:
    return f"asset://{document_id}/{name}"


def parse_asset_ref(ref: str) -> tuple[UUID, str] | None:
    match = _ASSET_REF_RE.fullmatch(ref.strip())
    if match is None:
        return None
    return UUID(match.group("document_id")), match.group("name")


class AssetCollector:
    """Thread-safe collector; extractor worker threads add assets concurrently."""

    def __init__(self, document_id: str) -> None:
        self._document_id = document_id
        self._assets: dict[str, Asset] = {}
        self._lock = threading.Lock()

    def add(self, name: str, data: bytes, content_type: str) -> str:
        if not ASSET_NAME_RE.fullmatch(name):
            raise ValueError(f"invalid asset name: {name!r}")
        with self._lock:
            self._assets[name] = Asset(name=name, data=data, content_type=content_type)
        return asset_ref(self._document_id, name)

    def items(self) -> list[Asset]:
        with self._lock:
            return [self._assets[name] for name in sorted(self._assets)]

    def __len__(self) -> int:
        with self._lock:
            return len(self._assets)
