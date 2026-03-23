"""Tests for core.state."""

from __future__ import annotations

from core.state import HardwareContext, get_context


def test_get_context_returns_singleton():
    """Repeated calls should return the same process-wide context object."""

    assert get_context() is get_context()


def test_hardware_context_default_values():
    """A fresh HardwareContext should use the documented default field values."""

    ctx = HardwareContext()

    assert isinstance(ctx.chip, str)
    assert ctx.compiler is None
    assert ctx.bridge is None
    assert ctx.serial is None
    assert ctx.hw_connected is False
    assert ctx.serial_connected is False
    assert ctx.last_bin_path is None
    assert ctx.last_code is None
    assert ctx.compiler_mtime == 0.0
    assert ctx.debug_attempt == 0
    assert ctx.cli_language in {"zh", "en"}
    assert ctx.telegram_cli_autostart_done is False
