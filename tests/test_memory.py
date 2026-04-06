"""Tests for core.memory."""

from __future__ import annotations

import core.memory as memory
import prompts.member as member_prompt


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
        f"### [2026-03-23 12:{index:02d}] 动态经验 {index}\n- {'x' * 320}" for index in range(150)
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

    assert header.startswith("# gary Memory")
    assert pinned
    assert dynamic
    assert all(entry.startswith("### [Pinned]") for entry in pinned)
    assert any("动态经验" in entry for entry in dynamic)


def test_compile_success_is_not_auto_written_to_member(tmp_path, monkeypatch):
    """Automatic success hooks should not create member entries."""

    member_path = tmp_path / "member.md"
    monkeypatch.setattr(memory, "MEMBER_MD_PATH", member_path)

    memory._record_success_memory(
        "compile_success",
        code="print('Gary:BOOT')\n",
        result={"bin_size": 123},
        chip="PICO_W",
    )
    memory._record_success_memory(
        "runtime_success",
        code="print('Gary:BOOT')\n",
        result={"bin_size": 123},
        request="blink",
        chip="PICO_W",
    )

    content = memory._ensure_member_file().read_text(encoding="utf-8")
    assert "编译成功模板" not in content
    assert "运行成功闭环" not in content
    assert "PICO_W" not in content


def test_gary_delete_member_memory_removes_matching_dynamic_entries(tmp_path, monkeypatch):
    """Gary should be able to delete wrong or useless dynamic memories by query."""

    member_path = tmp_path / "member.md"
    monkeypatch.setattr(memory, "MEMBER_MD_PATH", member_path)

    memory.gary_save_member_memory(
        title="错误经验",
        experience="这个经验已经过时，需要删掉",
        tags=["obsolete"],
    )
    result = memory.gary_delete_member_memory("错误经验")

    content = member_path.read_text(encoding="utf-8")
    assert result["success"] is True
    assert result["deleted_count"] == 1
    assert "错误经验" not in content
    assert "启动标记优先" in content


def test_member_prompt_limits_are_tightened_and_hashed(tmp_path, monkeypatch):
    """Injected member prompt should respect the tightened limits and expose a stable hash."""

    member_path = tmp_path / "member.md"
    dynamic_entries = [
        f"### [2026-04-06 12:{index:02d}] 动态经验 {index}\n- {'x' * 260}" for index in range(30)
    ]
    member_path.write_text(
        memory._default_member_content().rstrip() + "\n\n" + "\n\n".join(dynamic_entries),
        encoding="utf-8",
    )
    monkeypatch.setattr(memory, "MEMBER_MD_PATH", member_path)

    section, digest = member_prompt.get_member_prompt_section_state("STM32F103C8T6")

    assert memory.MEMBER_PROMPT_CHAR_LIMIT == 6000
    assert memory.MEMBER_PROMPT_MAX_DYNAMIC == 12
    assert len(digest) == 40
    assert section.count("### [2026-04-06") <= memory.MEMBER_PROMPT_MAX_DYNAMIC
