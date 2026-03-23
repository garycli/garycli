"""Tests for core.memory."""

from __future__ import annotations

import core.memory as memory


def test_gary_save_member_memory_writes_and_deduplicates(tmp_path, monkeypatch):
    """Saving the same memory twice should deduplicate the second write."""

    member_path = tmp_path / "member.md"
    monkeypatch.setattr(memory, "MEMBER_MD_PATH", member_path)

    first = memory.gary_save_member_memory(
        title="单元测试经验",
        experience="保持 UART 启动标记稳定输出",
        tags=["uart", "test"],
        importance="low",
    )
    second = memory.gary_save_member_memory(
        title="单元测试经验",
        experience="保持 UART 启动标记稳定输出",
        tags=["uart", "test"],
        importance="low",
    )

    content = member_path.read_text(encoding="utf-8")
    assert first["success"] is True
    assert first["deduplicated"] is False
    assert second["success"] is True
    assert second["deduplicated"] is True
    assert content.count("单元测试经验") == 1


def test_prune_member_content_respects_max_file_chars():
    """Pruned member content should stay within the configured size limit."""

    dynamic_entries = [
        f"### [2026-03-23 12:{index:02d}] 动态经验 {index}\n- {'x' * 320}"
        for index in range(150)
    ]
    content = memory._default_member_content().rstrip() + "\n\n" + "\n\n".join(dynamic_entries)

    pruned = memory._prune_member_content(content)

    assert len(pruned) <= memory.MEMBER_MAX_FILE_CHARS
    assert "### [Pinned] 启动标记优先" in pruned


def test_split_member_content_distinguishes_pinned_and_dynamic():
    """Pinned and dynamic sections should be distinguishable after splitting."""

    content = (
        memory._default_member_content().rstrip()
        + "\n\n### [2026-03-23 12:00] 动态经验\n- 运行成功"
    )

    header, entries = memory._split_member_content(content)
    pinned = [entry for entry in entries if entry.startswith("### [Pinned]")]
    dynamic = [entry for entry in entries if not entry.startswith("### [Pinned]")]

    assert header.startswith("# Gary Member Memory")
    assert pinned
    assert dynamic
    assert all(entry.startswith("### [Pinned]") for entry in pinned)
    assert any("动态经验" in entry for entry in dynamic)
