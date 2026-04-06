"""Tests for debug prompt web-verification guidance."""

from __future__ import annotations

from prompts.debug import get_debug_prompt


def test_micropython_runtime_debug_prompt_requires_web_verification_for_unknown_apis():
    """Runtime debug guidance should require web verification for unfamiliar APIs."""

    prompt = get_debug_prompt("runtime", {"chip": "CANMV_K230"})

    assert "先联网搜索官方文档 / 示例验证" in prompt
    assert "先联网查证" in prompt


def test_micropython_compile_debug_prompt_requires_web_verification_for_unknown_imports():
    """Compile debug guidance should prefer docs/examples for uncertain imports and syntax."""

    prompt = get_debug_prompt("compile", {"chip": "RP2040"})

    assert "先用 `browser_search -> browser_open_result`" in prompt
    assert "板级专有 API" in prompt
