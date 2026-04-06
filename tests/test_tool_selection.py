"""Tests for dynamic tool-schema selection."""

from __future__ import annotations

from ai.tools import select_tool_schemas


def _names(schemas: list[dict]) -> set[str]:
    return {
        schema["function"]["name"]
        for schema in schemas
        if schema.get("type") == "function" and schema.get("function", {}).get("name")
    }


def test_select_tool_schemas_limits_platform_specific_tools():
    """STM32 turns should not carry unrelated MicroPython platform tools."""

    names = _names(select_tool_schemas(chip="STM32F103C8T6", user_input="写一个LED闪烁程序"))

    assert "stm32_compile" in names
    assert "stm32_flash" in names
    assert "stm32_auto_flash_cycle" in names
    assert "rp2040_compile" not in names
    assert "esp_compile" not in names
    assert "canmv_compile" not in names
    assert "browser_search" not in names
    assert "git_commit" not in names


def test_select_tool_schemas_adds_browser_tools_for_research_tasks():
    """Research-oriented turns should opt into browser tools without loading STM32-only tools."""

    names = _names(select_tool_schemas(chip="CANMV_K230", user_input="搜索 K230 最新 API 文档"))

    assert "browser_search" in names
    assert "browser_open_result" in names
    assert "canmv_compile" in names
    assert "canmv_flash" in names
    assert "canmv_soft_reset" in names
    assert "stm32_compile" not in names


def test_select_tool_schemas_adds_git_and_docx_tools_on_demand():
    """Task keywords should pull in specialized tool groups only when needed."""

    names = _names(
        select_tool_schemas(
            chip="STM32F103C8T6",
            user_input="帮我看 git diff，并修改 docx 报告",
        )
    )

    assert "git_status" in names
    assert "git_diff" in names
    assert "read_docx" in names
    assert "replace_docx_text" in names
