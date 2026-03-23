"""Disk-backed member memory helpers for Gary."""

from __future__ import annotations

import re
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

MEMBER_MD_PATH = Path(__file__).resolve().parent.parent / "member.md"
MEMBER_PROMPT_CHAR_LIMIT = 12000
MEMBER_PROMPT_MAX_DYNAMIC = 24
MEMBER_MAX_FILE_CHARS = 40000
MEMBER_MAX_DYNAMIC_ENTRIES = 120
_MEMBER_LOCK = threading.RLock()


def _default_member_content() -> str:
    """Return the default member memory template."""

    return """# Gary Member Memory

## Focus
- 这里只记录高价值、可复用、能提高成功率的经验。
- 自动写入：成功编译、成功运行闭环。
- 主动写入：遇到关键初始化顺序、硬件坑、寄存器判定经验、稳定模板时，调用 `gary_save_member_memory`。
- 经验必须短、具体、可执行，不要粘贴大段原始日志。

## Memories

### [Pinned] 启动标记优先
- UART 初始化后立刻打印 `Gary:BOOT`，再初始化 I2C/SPI/TIM/OLED 等外设。
- 这样即使后续外设卡死，也能先确认程序已启动。

### [Pinned] 裸机 HAL_Delay 依赖 SysTick_Handler
- 裸机代码必须定义 `void SysTick_Handler(void) { HAL_IncTick(); }`。
- 否则 `HAL_Delay()` 会永久阻塞。

### [Pinned] I2C 外设先探测再使用
- 初始化后先 `HAL_I2C_IsDeviceReady()` 检查从设备是否应答。
- 无应答优先怀疑接线或地址，不要盲改业务逻辑。

### [Pinned] 增量修改优先精确替换
- 修改已有工程时优先 `str_replace_edit` + `stm32_recompile`。
- 不要无必要地整文件重写。

### [Pinned] 裸机禁止 sprintf/printf/malloc
- 裸机项目优先手写轻量调试输出，避免 `_sbrk/end` 链接错误。
"""


def _ensure_member_file() -> Path:
    """Create `member.md` on first use and return its path."""

    with _MEMBER_LOCK:
        if not MEMBER_MD_PATH.exists():
            MEMBER_MD_PATH.write_text(_default_member_content(), encoding="utf-8")
    return MEMBER_MD_PATH


def _normalize_member_text(value: Any, limit: int = 220) -> str:
    """Normalize one piece of memory text into a compact single line."""

    text = re.sub(r"\s+", " ", str(value or "")).strip(" -\t\r\n")
    if len(text) > limit:
        text = text[: limit - 3].rstrip() + "..."
    return text


def _member_text_to_lines(
    value: Any,
    per_line_limit: int = 220,
    max_lines: int = 8,
) -> list[str]:
    """Split arbitrary text into normalized member entry lines."""

    source = str(value or "").replace("\r", "\n")
    lines: list[str] = []
    for raw in source.splitlines():
        line = _normalize_member_text(raw, limit=per_line_limit)
        if line:
            lines.append(line)
        if len(lines) >= max_lines:
            break
    if not lines:
        single = _normalize_member_text(source, limit=per_line_limit)
        if single:
            lines.append(single)
    return lines


def _split_member_content(text: str) -> tuple[str, list[str]]:
    """Split member markdown into the header section and memory entries."""

    source = (text or "").strip()
    if not source:
        source = _default_member_content().strip()
    if "## Memories" not in source:
        source = _default_member_content().strip() + "\n\n" + source
    before, _, after = source.partition("## Memories")
    header = before.rstrip() + "\n\n## Memories\n"
    entries = [
        chunk.strip() for chunk in re.split(r"(?m)(?=^### )", after.strip()) if chunk.strip()
    ]
    return header, entries


def _prune_member_content(text: str) -> str:
    """Prune member content to the configured file-size limits."""

    header, entries = _split_member_content(text)
    pinned = [entry for entry in entries if entry.startswith("### [Pinned]")]
    dynamic = [entry for entry in entries if not entry.startswith("### [Pinned]")]
    dynamic = dynamic[-MEMBER_MAX_DYNAMIC_ENTRIES:]

    kept: list[str] = []
    total = len(header)
    for entry in pinned:
        needed = len(entry) + 2
        if kept and total + needed > MEMBER_MAX_FILE_CHARS:
            break
        kept.append(entry)
        total += needed

    recent: list[str] = []
    for entry in reversed(dynamic):
        needed = len(entry) + 2
        if recent and total + needed > MEMBER_MAX_FILE_CHARS:
            break
        recent.append(entry)
        total += needed
    recent.reverse()
    kept.extend(recent)

    content = header.rstrip() + "\n\n" + "\n\n".join(kept).strip()
    return content.strip() + "\n"


def _append_member_memory(
    title: str,
    experience: str,
    tags: list[str] | None = None,
    source: str = "manual",
    importance: str = "high",
) -> dict[str, Any]:
    """Append one normalized memory entry into `member.md`."""

    clean_title = _normalize_member_text(title, limit=120)
    lines = _member_text_to_lines(experience, per_line_limit=220, max_lines=10)
    if not clean_title or not lines:
        return {"success": False, "message": "title 或 experience 为空"}

    normalized_tags = [
        _normalize_member_text(tag, limit=24)
        for tag in (tags or [])
        if _normalize_member_text(tag, limit=24)
    ][:10]
    clean_source = _normalize_member_text(source, limit=40) or "manual"
    clean_importance = _normalize_member_text(importance, limit=16) or "high"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry_lines = [
        f"### [{timestamp}] {clean_title}",
        f"- importance: {clean_importance}",
        f"- source: {clean_source}",
    ]
    if normalized_tags:
        entry_lines.append(f"- tags: {', '.join(normalized_tags)}")
    entry_lines.extend(f"- {line}" for line in lines)
    entry = "\n".join(entry_lines)

    with _MEMBER_LOCK:
        path = _ensure_member_file()
        current = path.read_text(encoding="utf-8")
        _, existing_entries = _split_member_content(current)
        normalized_lines = [_normalize_member_text(line, limit=220).lower() for line in lines]
        for existing in existing_entries:
            normalized_entry = re.sub(r"\s+", " ", existing).lower()
            if clean_title.lower() not in normalized_entry:
                continue
            if all(line in normalized_entry for line in normalized_lines):
                return {
                    "success": True,
                    "deduplicated": True,
                    "path": str(path),
                    "message": f"member.md 已存在相似经验: {clean_title}",
                }
        updated = _prune_member_content(current.rstrip() + "\n\n" + entry + "\n")
        path.write_text(updated, encoding="utf-8")

    return {
        "success": True,
        "deduplicated": False,
        "path": str(MEMBER_MD_PATH),
        "message": f"已写入 member.md: {clean_title}",
    }


def gary_save_member_memory(
    title: str,
    experience: str,
    tags: list[str] | None = None,
    importance: str = "high",
) -> dict[str, Any]:
    """Write a high-value reusable experience into Gary's member memory."""

    return _append_member_memory(
        title=title,
        experience=experience,
        tags=tags or [],
        source="model",
        importance=importance,
    )


def _infer_code_tags(code: str) -> list[str]:
    """Infer compact tags from a generated STM32 source file."""

    text = code or ""
    checks = [
        (
            "rtos",
            any(token in text for token in ("FreeRTOS.h", "xTaskCreate", "vTaskDelay(", "task.h")),
        ),
        ("uart", "HAL_UART_" in text or "USART" in text),
        ("debug_print", "Debug_Print(" in text or "Debug_PrintInt(" in text),
        ("boot_marker", "Gary:BOOT" in text),
        ("systick", "SysTick_Handler" in text),
        ("i2c", "HAL_I2C_" in text or "I2C_HandleTypeDef" in text),
        ("spi", "HAL_SPI_" in text or "SPI_HandleTypeDef" in text),
        ("adc", "HAL_ADC_" in text or "ADC_HandleTypeDef" in text),
        ("pwm", "HAL_TIM_PWM_" in text or "TIM_HandleTypeDef" in text),
        ("oled", "OLED_" in text),
        ("sensor_check", "HAL_I2C_IsDeviceReady" in text),
        ("fault_analysis", "HardFault" in text or "SCB_CFSR" in text),
    ]
    tags = [name for name, matched in checks if matched]
    if "rtos" not in tags:
        tags.insert(0, "baremetal")
    return tags[:10]


def _derive_success_patterns_from_code(code: str) -> list[str]:
    """Derive reusable success heuristics from a known-good code sample."""

    text = code or ""
    patterns: list[str] = []
    if "Gary:BOOT" in text and ("MX_USART" in text or "HAL_UART_Init" in text):
        patterns.append("UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。")
    if "SysTick_Handler" in text and "FreeRTOS.h" not in text:
        patterns.append("裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。")
    if "vApplicationTickHook" in text:
        patterns.append("FreeRTOS 项目通过 vApplicationTickHook 维持 HAL tick。")
    if "HAL_I2C_IsDeviceReady" in text:
        patterns.append("I2C 设备在使用前会先做在线探测。")
    if "Debug_Print(" in text or "Debug_PrintInt(" in text:
        patterns.append("代码保留了轻量串口调试输出，便于运行时定位问题。")
    if "xTaskCreate" in text:
        patterns.append("当前成功模板已经包含可编译的 FreeRTOS 任务结构。")
    if "str_replace_edit" in text:
        patterns.append("此模板来自增量修改链路，适合继续做精准替换。")
    return patterns[:5]


def _record_success_memory(
    event_type: str,
    code: str,
    result: Mapping[str, Any] | None = None,
    request: str = "",
    steps: Sequence[Mapping[str, Any]] | None = None,
    chip: str = "",
    log_error: Callable[[str], None] | None = None,
) -> None:
    """Persist compile/runtime success summaries into `member.md`."""

    try:
        tags = _infer_code_tags(code)
        chip_name = _normalize_member_text(chip or "UNKNOWN", limit=40) or "UNKNOWN"
        mode = "rtos" if "rtos" in tags else "baremetal"
        short_request = _normalize_member_text(request, limit=60)
        if event_type == "runtime_success":
            title = f"运行成功闭环 | {chip_name} | {mode}"
            if short_request:
                title += f" | {short_request}"
        else:
            title = f"编译成功模板 | {chip_name} | {mode}"

        lines: list[str] = []
        if short_request:
            lines.append(f"需求: {short_request}")
        if result and result.get("bin_size"):
            lines.append(f"bin_size: {result['bin_size']} B")
        if tags:
            lines.append(f"特征: {', '.join(tags[:8])}")
        if event_type == "runtime_success":
            lines.append("烧录、启动、串口/寄存器验证通过，无 HardFault、无硬件缺失。")
            uart_step = next((step for step in (steps or []) if step.get("step") == "uart"), None)
            reg_step = next(
                (step for step in (steps or []) if step.get("step") == "registers"),
                None,
            )
            if uart_step and uart_step.get("boot_ok"):
                lines.append("串口已看到 Gary:BOOT，启动链路正常。")
            if reg_step and reg_step.get("key_regs"):
                reg_names = list(reg_step["key_regs"].keys())[:6]
                lines.append(f"运行时已回读关键寄存器: {', '.join(reg_names)}")
        else:
            lines.append("当前代码已在本机工具链上成功编译通过。")
        lines.extend(_derive_success_patterns_from_code(code))

        _append_member_memory(
            title=title,
            experience="\n".join(lines),
            tags=tags,
            source=event_type,
            importance="critical" if event_type == "runtime_success" else "high",
        )
    except Exception as exc:
        if log_error is not None:
            log_error(f"member auto_save error={str(exc)[:160]}")


def _member_preview_markdown(max_dynamic: int = 10, path_label: str = "Path") -> str:
    """Build a markdown preview of the pinned and most recent member entries."""

    with _MEMBER_LOCK:
        path = _ensure_member_file()
        current = path.read_text(encoding="utf-8")
    header, entries = _split_member_content(current)
    pinned = [entry for entry in entries if entry.startswith("### [Pinned]")]
    dynamic = [entry for entry in entries if not entry.startswith("### [Pinned]")]
    selected = pinned + dynamic[-max_dynamic:]
    body = header.rstrip()
    if selected:
        body += "\n\n" + "\n\n".join(selected)
    return f"**{path_label}:** `{path}`\n\n{body.strip()}"


__all__ = [
    "MEMBER_MAX_DYNAMIC_ENTRIES",
    "MEMBER_MAX_FILE_CHARS",
    "MEMBER_MD_PATH",
    "MEMBER_PROMPT_CHAR_LIMIT",
    "MEMBER_PROMPT_MAX_DYNAMIC",
    "_MEMBER_LOCK",
    "_append_member_memory",
    "_ensure_member_file",
    "_member_preview_markdown",
    "_prune_member_content",
    "_record_success_memory",
    "_split_member_content",
    "gary_save_member_memory",
]
