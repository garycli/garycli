"""CanMV K230 wrappers over the generic MicroPython workflow."""

from __future__ import annotations

from typing import Any, Callable

from core.micropython_tools import (
    micropython_auto_sync_cycle,
    micropython_compile,
    micropython_connect,
    micropython_flash,
    micropython_hardware_status,
    micropython_list_files_tool,
    micropython_soft_reset,
)
from core.platforms import canonical_target_name, detect_target_platform
from core.state import get_context


def _ensure_canmv_context() -> str:
    ctx = get_context()
    if detect_target_platform(ctx.chip) != "canmv":
        ctx.chip = canonical_target_name("CANMV_K230")
    return ctx.chip


def canmv_connect(
    chip: str | None = None,
    *,
    port: str | None = None,
    baud: int = 115200,
    console: Any = None,
) -> dict[str, Any]:
    return micropython_connect(chip or "CANMV_K230", port=port, baud=baud, console=console)


def canmv_hardware_status(*, console: Any = None) -> dict[str, Any]:
    _ensure_canmv_context()
    return micropython_hardware_status(console=console)


def canmv_compile(
    code: str,
    *,
    chip: str | None = None,
    console: Any = None,
    record_success_memory: Callable[..., None] | None = None,
    log_error: Callable[[str], None] | None = None,
) -> dict[str, Any]:
    return micropython_compile(
        code,
        chip=chip or "CANMV_K230",
        console=console,
        record_success_memory=record_success_memory,
        log_error=log_error,
    )


def canmv_flash(
    *,
    file_path: str | None = None,
    code: str | None = None,
    port: str | None = None,
    baud: int = 115200,
    console: Any = None,
    capture_timeout: float = 5.0,
) -> dict[str, Any]:
    _ensure_canmv_context()
    return micropython_flash(
        file_path=file_path,
        code=code,
        port=port,
        baud=baud,
        console=console,
        capture_timeout=capture_timeout,
    )


def canmv_auto_sync_cycle(
    code: str,
    *,
    request: str = "",
    baud: int = 115200,
    console: Any = None,
    max_attempts: int = 8,
    record_success_memory: Callable[..., None] | None = None,
    log_error: Callable[[str], None] | None = None,
) -> dict[str, Any]:
    _ensure_canmv_context()
    return micropython_auto_sync_cycle(
        code,
        request=request,
        baud=baud,
        console=console,
        max_attempts=max_attempts,
        record_success_memory=record_success_memory,
        log_error=log_error,
    )


def canmv_list_files_tool(
    *,
    path: str = ".",
    port: str | None = None,
    baud: int = 115200,
    console: Any = None,
) -> dict[str, Any]:
    _ensure_canmv_context()
    return micropython_list_files_tool(path=path, port=port, baud=baud, console=console)


def canmv_soft_reset(
    *,
    port: str | None = None,
    baud: int = 115200,
    console: Any = None,
    capture_timeout: float = 5.0,
) -> dict[str, Any]:
    _ensure_canmv_context()
    return micropython_soft_reset(
        port=port,
        baud=baud,
        console=console,
        capture_timeout=capture_timeout,
    )


__all__ = [
    "canmv_auto_sync_cycle",
    "canmv_compile",
    "canmv_connect",
    "canmv_flash",
    "canmv_hardware_status",
    "canmv_list_files_tool",
    "canmv_soft_reset",
]
