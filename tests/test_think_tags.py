"""Tests for streamed `<think>` tag parsing."""

from __future__ import annotations

from core.agent import STM32Agent


def _parse_segments(chunks: list[str]) -> list[tuple[str, str]]:
    """Run the think-tag parser across streamed chunks."""

    agent = object.__new__(STM32Agent)
    state = {"inside_think": False, "pending": ""}
    segments: list[tuple[str, str]] = []
    for chunk in chunks:
        segments.extend(agent._extract_think_segments(chunk, state))
    segments.extend(agent._flush_think_segments(state))
    return segments


def test_think_tags_are_split_from_visible_content():
    """Visible content and hidden think content should be separated."""

    segments = _parse_segments(["你好<think>内部思考</think>世界"])

    assert segments == [("content", "你好"), ("think", "内部思考"), ("content", "世界")]


def test_think_tags_can_span_multiple_chunks():
    """Partially streamed think tags should still parse correctly."""

    segments = _parse_segments(["你好<thi", "nk>内部思考</thi", "nk> 世界"])

    assert segments == [("content", "你好"), ("think", "内部思考"), ("content", " 世界")]


def test_stray_closing_tag_is_removed_from_visible_content():
    """An unmatched closing tag should not leak into the final reply."""

    segments = _parse_segments(["A</think>B"])

    assert segments == [("content", "A"), ("content", "B")]
