from __future__ import annotations

from uuid import UUID

from app.storage.client import markdown_document_key, pagemap_document_key


def test_pagemap_key_sits_next_to_markdown() -> None:
    course = UUID("11111111-1111-1111-1111-111111111111")
    doc = UUID("22222222-2222-2222-2222-222222222222")
    md = markdown_document_key(course, doc)
    pm = pagemap_document_key(course, doc)
    assert pm == md.rsplit("/", 1)[0] + "/pagemap.json"
    assert pm.endswith("pagemap.json")
