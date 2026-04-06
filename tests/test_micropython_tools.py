"""Tests for generic MicroPython connect helpers."""

from __future__ import annotations

from core.micropython_tools import micropython_connect, micropython_flash, micropython_list_files_tool
from core.state import get_context


def test_micropython_connect_autodetects_board(monkeypatch):
    """Generic MICROPYTHON connect should probe, infer chip, and connect serial."""

    ctx = get_context()
    old_chip = ctx.chip
    old_hw = ctx.hw_connected
    old_serial_connected = ctx.serial_connected
    old_serial = ctx.serial

    monkeypatch.setattr(
        "core.micropython_tools._autodetect_micropython_board",
        lambda **kwargs: {
            "success": True,
            "port": "/dev/ttyACM0",
            "chip": "PICO_W",
            "platform": "rp2040",
            "info": {
                "platform": "rp2",
                "machine": "Raspberry Pi Pico W with RP2040",
            },
        },
    )
    monkeypatch.setattr(
        "core.micropython_tools._reconnect_monitor",
        lambda port, baud, console=None: {"success": True, "port": port},
    )

    try:
        result = micropython_connect("MICROPYTHON")
        assert result["success"] is True
        assert result["chip"] == "PICO_W"
        assert result["platform"] == "rp2040"
        assert result["port"] == "/dev/ttyACM0"
        assert result["detected_info"]["platform"] == "rp2"
        assert ctx.chip == "PICO_W"
    finally:
        ctx.chip = old_chip
        ctx.hw_connected = old_hw
        ctx.serial_connected = old_serial_connected
        ctx.serial = old_serial


def test_micropython_connect_autodetect_returns_clear_error(monkeypatch):
    """Generic MICROPYTHON connect should surface scan failures cleanly."""

    monkeypatch.setattr(
        "core.micropython_tools._autodetect_micropython_board",
        lambda **kwargs: {
            "success": False,
            "candidate_ports": ["/dev/ttyACM0"],
            "message": "未扫描到可自动识别的 MicroPython 设备",
        },
    )

    result = micropython_connect("MIRCOPYTHON")
    assert result["success"] is False
    assert result["chip"] == "MICROPYTHON"
    assert result["candidate_ports"] == ["/dev/ttyACM0"]


def test_canmv_flash_deploys_to_sdcard_main(monkeypatch):
    """CanMV K230 deployment should write to /sdcard/main.py on the device."""

    ctx = get_context()
    old_chip = ctx.chip
    old_hw = ctx.hw_connected
    old_serial_connected = ctx.serial_connected
    old_serial = ctx.serial

    calls: list[dict[str, object]] = []

    monkeypatch.setattr(
        "core.micropython_tools.upload_text_file",
        lambda **kwargs: calls.append(kwargs) or {"success": True, "boot_output": "Gary:BOOT\n"},
    )
    monkeypatch.setattr(
        "core.micropython_tools._reconnect_monitor",
        lambda port, baud, console=None: {"success": True, "port": port},
    )

    try:
        ctx.chip = "CANMV_K230"
        result = micropython_flash(code="print('Gary:BOOT')\n", port="/dev/ttyACM0")
        assert result["success"] is True
        assert result["device_main_path"] == "/sdcard/main.py"
        assert calls[0]["device_path"] == "/sdcard/main.py"
    finally:
        ctx.chip = old_chip
        ctx.hw_connected = old_hw
        ctx.serial_connected = old_serial_connected
        ctx.serial = old_serial


def test_canmv_list_files_defaults_to_sdcard(monkeypatch):
    """CanMV file listing should default to the /sdcard directory."""

    ctx = get_context()
    old_chip = ctx.chip

    monkeypatch.setattr(
        "core.micropython_tools.list_remote_files",
        lambda **kwargs: {"success": True, "path": kwargs["path"], "files": ["main.py"]},
    )

    try:
        ctx.chip = "CANMV_K230"
        result = micropython_list_files_tool(port="/dev/ttyACM0")
        assert result["success"] is True
        assert result["path"] == "/sdcard"
    finally:
        ctx.chip = old_chip
