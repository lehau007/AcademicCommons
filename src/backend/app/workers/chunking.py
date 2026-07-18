from __future__ import annotations

import bisect
import math
import re
from dataclasses import dataclass
from typing import Protocol


class Encoder(Protocol):
    def encode(self, texts: list[str]) -> list[list[float]]: ...


@dataclass
class Section:
    title: str
    body: str
    start_line: int = 0


@dataclass
class Chunk:
    text: str
    section_title: str
    chunk_order: int
    char_count: int
    page: int | None = None


def cosine_similarity(left: list[float], right: list[float]) -> float:
    dot = sum(a * b for a, b in zip(left, right, strict=False))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if left_norm == 0.0 or right_norm == 0.0:
        return 0.0
    return dot / (left_norm * right_norm)


def _split_paragraphs(text: str) -> list[str]:
    normalized = text.replace("\r\n", "\n").strip()
    if not normalized:
        return []

    lines = normalized.split("\n")
    blocks: list[str] = []
    current_block_lines: list[str] = []

    in_code_block = False
    in_mermaid = False
    in_math_block_double_dollar = False
    in_math_block_backslash_bracket = False

    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped_line = line.strip()

        # 1. Math block (double dollar $$) state toggle
        if stripped_line.startswith("$$"):
            if in_math_block_double_dollar:
                current_block_lines.append(line)
                blocks.append("\n".join(current_block_lines).strip())
                current_block_lines = []
                in_math_block_double_dollar = False
                i += 1
                continue
            else:
                if current_block_lines:
                    blocks.append("\n".join(current_block_lines).strip())
                    current_block_lines = []
                if stripped_line.endswith("$$") and len(stripped_line) > 2:
                    blocks.append(line)
                    i += 1
                    continue
                else:
                    current_block_lines.append(line)
                    in_math_block_double_dollar = True
                    i += 1
                    continue

        if in_math_block_double_dollar:
            current_block_lines.append(line)
            i += 1
            continue

        # 2. Math block (\[ and \]) state tracking
        if stripped_line.startswith("\\["):
            if current_block_lines:
                blocks.append("\n".join(current_block_lines).strip())
                current_block_lines = []
            current_block_lines.append(line)
            in_math_block_backslash_bracket = True
            i += 1
            continue

        if in_math_block_backslash_bracket:
            current_block_lines.append(line)
            if stripped_line.endswith("\\]"):
                blocks.append("\n".join(current_block_lines).strip())
                current_block_lines = []
                in_math_block_backslash_bracket = False
            i += 1
            continue

        # 3. Mermaid block state tracking
        if stripped_line.startswith("```mermaid"):
            if current_block_lines:
                blocks.append("\n".join(current_block_lines).strip())
                current_block_lines = []
            current_block_lines.append(line)
            in_mermaid = True
            i += 1
            continue

        if in_mermaid:
            current_block_lines.append(line)
            if stripped_line.startswith("```"):
                blocks.append("\n".join(current_block_lines).strip())
                current_block_lines = []
                in_mermaid = False
            i += 1
            continue

        # 4. Code block state tracking (general ```)
        if stripped_line.startswith("```"):
            if in_code_block:
                current_block_lines.append(line)
                blocks.append("\n".join(current_block_lines).strip())
                current_block_lines = []
                in_code_block = False
            else:
                if current_block_lines:
                    blocks.append("\n".join(current_block_lines).strip())
                    current_block_lines = []
                current_block_lines.append(line)
                in_code_block = True
            i += 1
            continue

        if in_code_block:
            current_block_lines.append(line)
            i += 1
            continue

        # 5. Tables: lines containing "|"
        if "|" in stripped_line:
            if current_block_lines and not any("|" in line_val for line_val in current_block_lines):
                blocks.append("\n".join(current_block_lines).strip())
                current_block_lines = []
            current_block_lines.append(line)
            i += 1
            while i < n and "|" in lines[i]:
                current_block_lines.append(lines[i])
                i += 1
            blocks.append("\n".join(current_block_lines).strip())
            current_block_lines = []
            continue

        # 6. MCQ blocks (Question + Options A, B, C, D)
        is_mcq_start = (
            stripped_line.startswith("Câu") or
            stripped_line.lower().startswith("question")
        ) and re.match(r"^(câu|question)\s*\d+[\s:.]", stripped_line, re.IGNORECASE)

        if is_mcq_start:
            if current_block_lines:
                blocks.append("\n".join(current_block_lines).strip())
                current_block_lines = []
            current_block_lines.append(line)
            i += 1
            while i < n:
                next_line = lines[i]
                next_stripped = next_line.strip()
                if not next_stripped:
                    next_non_empty_idx = i
                    while next_non_empty_idx < n and not lines[next_non_empty_idx].strip():
                        next_non_empty_idx += 1
                    if next_non_empty_idx < n:
                        n_stripped = lines[next_non_empty_idx].strip()
                        is_next_mcq = re.match(r"^(câu|question)\s*\d+[\s:.]", n_stripped, re.IGNORECASE)
                        is_next_option = re.match(r"^[a-d][\s:.)\-\]]", n_stripped, re.IGNORECASE)
                        is_next_explanation = any(
                            k in n_stripped.lower()
                            for k in ["explanation", "đáp án", "correct answer", "lời giải"]
                        )
                        if is_next_mcq:
                            break
                        elif is_next_option or is_next_explanation:
                            for k in range(i, next_non_empty_idx + 1):
                                current_block_lines.append(lines[k])
                            i = next_non_empty_idx + 1
                            continue
                        else:
                            break
                    else:
                        break

                if re.match(r"^(câu|question)\s*\d+[\s:.]", next_stripped, re.IGNORECASE):
                    break

                current_block_lines.append(next_line)
                i += 1

            blocks.append("\n".join(current_block_lines).strip())
            current_block_lines = []
            continue

        # 7. Bulleted/Numbered list blocks
        is_list_line = re.match(r"^([\*\-\+]\s+|\d+\.\s+)", stripped_line)
        if is_list_line:
            if current_block_lines and not any(
                re.match(r"^([\*\-\+]\s+|\d+\.\s+)", line_val.strip())
                for line_val in current_block_lines
            ):
                blocks.append("\n".join(current_block_lines).strip())
                current_block_lines = []
            current_block_lines.append(line)
            i += 1
            while i < n:
                next_line = lines[i]
                next_stripped = next_line.strip()
                if not next_stripped:
                    next_non_empty = i
                    while next_non_empty < n and not lines[next_non_empty].strip():
                        next_non_empty += 1
                    if next_non_empty < n and re.match(r"^([\*\-\+]\s+|\d+\.\s+)", lines[next_non_empty].strip()):
                        for k in range(i, next_non_empty + 1):
                            current_block_lines.append(lines[k])
                        i = next_non_empty + 1
                        continue
                    else:
                        break
                elif re.match(r"^([\*\-\+]\s+|\d+\.\s+)", next_stripped):
                    current_block_lines.append(next_line)
                    i += 1
                else:
                    break
            blocks.append("\n".join(current_block_lines).strip())
            current_block_lines = []
            continue

        # 8. Standard paragraph lines
        if not stripped_line:
            if current_block_lines:
                blocks.append("\n".join(current_block_lines).strip())
                current_block_lines = []
        else:
            current_block_lines.append(line)
        i += 1

    if current_block_lines:
        blocks.append("\n".join(current_block_lines).strip())

    return [b for b in blocks if b]


def _normalize_heading(line: str) -> str:
    return re.sub(r"^#+\s*", "", line).strip() or "Untitled Section"


def _page_for_line(page_map: list[tuple[int, int]], line: int) -> int | None:
    """Return the page whose boundary is at or before ``line`` (bisect)."""
    if not page_map:
        return None
    starts = [start for start, _ in page_map]
    idx = bisect.bisect_right(starts, line) - 1
    if idx < 0:
        return page_map[0][1]
    return page_map[idx][1]


def parse_markdown_sections(markdown_text: str) -> list[Section]:
    text = markdown_text.replace("\r\n", "\n").strip()
    if not text:
        return []

    sections: list[Section] = []
    current_title = "Document Start"
    current_lines: list[str] = []
    current_start = 0

    for line_no, line in enumerate(text.split("\n")):
        if re.match(r"^#{1,6}\s+", line):
            body = "\n".join(current_lines).strip()
            if body:
                sections.append(Section(title=current_title, body=body, start_line=current_start))
            current_title = _normalize_heading(line)
            current_lines = []
            current_start = line_no
        else:
            current_lines.append(line)

    final_body = "\n".join(current_lines).strip()
    if final_body:
        sections.append(Section(title=current_title, body=final_body, start_line=current_start))

    return sections


def _chunk_section(
    section: Section,
    paragraph_embeddings: list[list[float]],
    similarity_threshold: float,
    min_chunk_chars: int,
    max_chunk_chars: int,
) -> list[tuple[str, int]]:
    paragraphs = _split_paragraphs(section.body)
    if not paragraphs:
        return []

    chunk_texts: list[tuple[str, int]] = []
    current_parts: list[str] = []
    current_chars = 0
    current_count = 0

    for idx, paragraph in enumerate(paragraphs):
        p_len = len(paragraph)

        if p_len > max_chunk_chars:
            if current_parts:
                chunk_texts.append(("\n\n".join(current_parts).strip(), current_count))
                current_parts = []
                current_chars = 0
                current_count = 0
            chunk_texts.append((paragraph, 1))
            continue

        candidate_chars = current_chars + (2 if current_parts else 0) + p_len

        if not current_parts:
            current_parts = [paragraph]
            current_chars = p_len
            current_count = 1
            continue

        similarity = cosine_similarity(paragraph_embeddings[idx - 1], paragraph_embeddings[idx])

        should_merge = similarity >= similarity_threshold and candidate_chars <= max_chunk_chars
        if (should_merge or current_chars < min_chunk_chars) and candidate_chars <= max_chunk_chars:
            current_parts.append(paragraph)
            current_chars = candidate_chars
            current_count += 1
        else:
            chunk_texts.append(("\n\n".join(current_parts).strip(), current_count))
            current_parts = [paragraph]
            current_chars = p_len
            current_count = 1

    if current_parts:
        chunk_texts.append(("\n\n".join(current_parts).strip(), current_count))

    return chunk_texts


def build_chunks(
    markdown_text: str,
    encoder: Encoder,
    page_map: list[tuple[int, int]] | None = None,
    similarity_threshold: float = 0.55,
    min_chunk_chars: int = 350,
    max_chunk_chars: int = 1200,
) -> list[Chunk]:
    sections = parse_markdown_sections(markdown_text)
    chunks: list[Chunk] = []
    chunk_order = 1

    for section in sections:
        paragraphs = _split_paragraphs(section.body)
        if not paragraphs:
            continue

        section_page = _page_for_line(page_map, section.start_line) if page_map else None

        paragraph_embeddings = encoder.encode(paragraphs)
        merged = _chunk_section(
            section=section,
            paragraph_embeddings=paragraph_embeddings,
            similarity_threshold=similarity_threshold,
            min_chunk_chars=min_chunk_chars,
            max_chunk_chars=max_chunk_chars,
        )
        for text, _ in merged:
            chunks.append(
                Chunk(
                    text=text,
                    section_title=section.title,
                    chunk_order=chunk_order,
                    char_count=len(text),
                    page=section_page,
                )
            )
            chunk_order += 1

    return chunks


__all__ = [
    "Chunk",
    "Encoder",
    "Section",
    "build_chunks",
    "cosine_similarity",
    "parse_markdown_sections",
]
