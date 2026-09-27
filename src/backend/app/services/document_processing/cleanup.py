"""Deterministic Markdown cleanup that replaces the v3 LLM normalization pass."""

from __future__ import annotations

import math
import re
from collections import Counter

_PICTURE_OMITTED_RE = re.compile(r"^\*\*==> picture \[[^\]]*\] intentionally omitted <==\*\*[ \t]*$", re.MULTILINE)
_PICTURE_TEXT_RE = re.compile(
    r"\*\*----- Start of picture text -----\*\*<br>.*?\*\*----- End of picture text -----\*\*<br>[ \t]*\n?",
    re.DOTALL,
)
_PAGE_NUMBER_RE = re.compile(r"^\**\s*\d{1,4}\s*\**$")
_IMAGE_LINE_RE = re.compile(r"^!\[.*\]\(.*\)$")
_BOILERPLATE_MAX_LEN = 80
_BOILERPLATE_MIN_PAGES = 3
_BOILERPLATE_PAGE_RATIO = 0.5


def _is_protected(line: str) -> bool:
    """Lines that are content structure, never boilerplate."""
    return (
        line.startswith("|")
        or line.startswith("[Figure:")
        or bool(_IMAGE_LINE_RE.match(line))
        or not any(ch.isalnum() for ch in line)
    )


def _lines_outside_fences(text: str) -> list[str]:
    lines: list[str] = []
    in_fence = False
    for raw in text.splitlines():
        if raw.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            lines.append(raw.strip())
    return lines


class MarkdownCleaner:
    def clean_pages(self, pages: list[str]) -> list[str]:
        stripped = [self._strip_picture_artifacts(page) for page in pages]
        boilerplate = self._boilerplate_lines(stripped)
        return [self._clean_page(page, boilerplate) for page in stripped]

    @staticmethod
    def _strip_picture_artifacts(page: str) -> str:
        page = _PICTURE_TEXT_RE.sub("", page)
        return _PICTURE_OMITTED_RE.sub("", page)

    @staticmethod
    def _boilerplate_lines(pages: list[str]) -> set[str]:
        if len(pages) < _BOILERPLATE_MIN_PAGES:
            return set()
        counts: Counter[str] = Counter()
        for page in pages:
            counts.update(
                {
                    line
                    for line in _lines_outside_fences(page)
                    if line and len(line) <= _BOILERPLATE_MAX_LEN and not _is_protected(line)
                }
            )
        threshold = max(_BOILERPLATE_MIN_PAGES, math.ceil(len(pages) * _BOILERPLATE_PAGE_RATIO))
        return {line for line, count in counts.items() if count >= threshold}

    @staticmethod
    def _clean_page(page: str, boilerplate: set[str]) -> str:
        out: list[str] = []
        in_fence = False
        for raw in page.splitlines():
            line = raw.rstrip()
            if line.strip().startswith("```"):
                in_fence = not in_fence
                out.append(line)
                continue
            if not in_fence:
                key = line.strip()
                if key in boilerplate or _PAGE_NUMBER_RE.match(key):
                    continue
            out.append(line)
        text = "\n".join(out)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()
