from __future__ import annotations

from uuid import UUID

import pytest

from app.services.document_processing.assets import AssetCollector, asset_ref, parse_asset_ref

DOC = "0b7c6f0e-8d8e-4f1a-9a55-1f0c7d9c2a11"


def test_add_returns_ref_and_items_are_sorted() -> None:
    collector = AssetCollector(DOC)

    ref = collector.add("p002-f1.png", b"b", "image/png")
    collector.add("p001-page.jpg", b"a", "image/jpeg")

    assert ref == f"asset://{DOC}/p002-f1.png"
    assert [a.name for a in collector.items()] == ["p001-page.jpg", "p002-f1.png"]
    assert len(collector) == 2


@pytest.mark.parametrize("name", ["../raw/x.pdf", "p001-f1.png/../x", "p1-f1.png", "p001-f1.gif", "x.png"])
def test_add_rejects_invalid_names(name: str) -> None:
    with pytest.raises(ValueError):
        AssetCollector(DOC).add(name, b"x", "image/png")


def test_parse_asset_ref_round_trip_and_rejections() -> None:
    assert parse_asset_ref(asset_ref(DOC, "p010-f3.png")) == (UUID(DOC), "p010-f3.png")
    assert parse_asset_ref(f"asset://{DOC}/../raw/x.pdf") is None
    assert parse_asset_ref("asset://not-a-uuid/p001-f1.png") is None
    assert parse_asset_ref(f"https://x/{DOC}/p001-f1.png") is None
