"""Tests for API message normalization in the agent."""

from __future__ import annotations

from core.agent import STM32Agent


def test_messages_for_api_merges_multiple_system_messages():
    """Only one system message should be sent to providers that reject later system roles."""

    agent = object.__new__(STM32Agent)
    agent._pending_system_hint = ""
    agent.messages = [
        {"role": "system", "content": "base prompt"},
        {"role": "user", "content": "hello"},
        {"role": "system", "content": "legacy hint"},
        {"role": "assistant", "content": "hi"},
    ]

    result = agent._messages_for_api()

    assert [item["role"] for item in result].count("system") == 1
    assert result[0]["role"] == "system"
    assert "base prompt" in result[0]["content"]
    assert "legacy hint" in result[0]["content"]


def test_messages_for_api_appends_pending_web_hint_into_first_system_message():
    """The one-turn browse hint should be folded into the first system prompt."""

    agent = object.__new__(STM32Agent)
    agent._pending_system_hint = "web hint"
    agent.messages = [
        {"role": "system", "content": "base prompt"},
        {"role": "user", "content": "search docs"},
    ]

    result = agent._messages_for_api()

    assert result[0]["role"] == "system"
    assert "base prompt" in result[0]["content"]
    assert "web hint" in result[0]["content"]
    assert [item["role"] for item in result] == ["system", "user"]
