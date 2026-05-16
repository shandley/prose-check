"""Text parsing utilities for prose_check."""

from __future__ import annotations

import re


def word_count(text: str) -> int:
    return len(text.split())


def split_paragraphs(text: str) -> list[str]:
    """Split on blank lines, return non-empty paragraphs."""
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def split_sentences(text: str) -> list[str]:
    """Rough sentence splitter on .!? boundaries."""
    parts = re.split(r"[.!?]+", text)
    return [s.strip() for s in parts if s.strip()]


def count_list_items(text: str) -> int:
    """Count bullet and numbered list items."""
    bullets = len(re.findall(r"^\s*[-•*]\s", text, re.MULTILINE))
    numbered = len(re.findall(r"^\s*\d+\.\s", text, re.MULTILINE))
    return bullets + numbered


def find_context(text: str, match_start: int, match_end: int, window: int = 40) -> str:
    """Return a snippet of text around a match position."""
    start = max(0, match_start - window)
    end = min(len(text), match_end + window)
    snippet = text[start:end].replace("\n", " ")
    prefix = "..." if start > 0 else ""
    suffix = "..." if end < len(text) else ""
    return f"{prefix}{snippet}{suffix}"
