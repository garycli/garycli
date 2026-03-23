"""Terminal UI helpers and REPL runtime."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Any, Callable, Optional

from rich import box
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

try:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
    from prompt_toolkit.formatted_text import HTML
    from prompt_toolkit.history import FileHistory, InMemoryHistory
    from prompt_toolkit.styles import Style

    PROMPT_TOOLKIT_AVAILABLE = True
except Exception:  # pragma: no cover - optional dependency fallback
    PromptSession = None
    AutoSuggestFromHistory = None
    HTML = None
    FileHistory = None
    InMemoryHistory = None
    Style = None
    PROMPT_TOOLKIT_AVAILABLE = False

console = Console()


def print_banner(
    *,
    chip: str,
    model: str,
    hw_connected: bool,
    serial_connected: bool,
    cli_text: Callable[[str, str], str],
    theme: str,
) -> None:
    """Render the startup banner and current runtime status."""

    chip_line = cli_text(
        f"芯片: [bold]{chip}[/]  |  模型: [bold]{model}[/]",
        f"Chip: [bold]{chip}[/]  |  Model: [bold]{model}[/]",
    )
    hw_line = (
        cli_text(
            f"硬件: [green]已连接[/]  串口: [{'green' if serial_connected else 'yellow'}]"
            f"{'已连接' if serial_connected else '未连接'}[/]",
            f"Hardware: [green]connected[/]  Serial: [{'green' if serial_connected else 'yellow'}]"
            f"{'connected' if serial_connected else 'disconnected'}[/]",
        )
        if hw_connected
        else cli_text("硬件: [dim]未连接[/]", "Hardware: [dim]disconnected[/]")
    )
    art = (
        "   ██████╗  █████╗ ██████╗ ██╗   ██╗\n"
        "  ██╔════╝ ██╔══██╗██╔══██╗╚██╗ ██╔╝\n"
        "  ██║  ███╗███████║██████╔╝ ╚████╔╝ \n"
        "  ██║   ██║██╔══██║██╔══██╗  ╚██╔╝  \n"
        "  ╚██████╔╝██║  ██║██║  ██║   ██║   \n"
        "   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝  "
    )
    panel = Panel(
        f"[bold {theme}]{art}[/]\n\n"
        f"  {chip_line}\n  {hw_line}\n\n"
        f"  [dim]{cli_text('输入需求即可生成代码 · Tab 补全命令 · /help 查看命令 · /connect 连接硬件', 'Describe what you want to build · Tab completes commands · /help shows commands · /connect attaches hardware')}[/]",
        title=f"[bold {theme}]Gary Dev Agent[/]",
        border_style=theme,
        padding=(0, 1),
    )
    console.print(panel)
    console.print()


def _print_status_bar(
    *,
    chip: str,
    model: str,
    hw_connected: bool,
    tokens: int,
    cli_text: Callable[[str, str], str],
) -> None:
    """Render the per-turn status bar above the prompt."""

    hw = (
        f"[green]●[/] {chip}"
        if hw_connected
        else cli_text("[dim]○ 未连接[/]", "[dim]○ Disconnected[/]")
    )
    console.print(f"[dim]{hw}  │  {model}  │  {cli_text('上下文', 'context')}: ~{tokens} tokens[/]")
    console.rule(style="dim")


def _build_history(history_path: Path, ensure_gary_home: Optional[Callable[[], None]]):
    """Create a prompt history backend with a prompt_toolkit fallback."""

    if not PROMPT_TOOLKIT_AVAILABLE:
        return None
    try:
        if ensure_gary_home is not None:
            ensure_gary_home()
        return FileHistory(str(history_path))
    except Exception:
        return InMemoryHistory()


def run_interactive(
    agent: Any,
    *,
    handle_command: Callable[[Any, str], bool],
    cli_text: Callable[[str, str], str],
    theme: str,
    model: str,
    status_snapshot: Callable[[], dict[str, Any]],
    ensure_cli_telegram_daemon: Callable[[], Optional[dict]],
    shutdown_runtime: Callable[[bool], dict],
    history_path: Path,
    ensure_gary_home: Optional[Callable[[], None]] = None,
    completer: Any = None,
) -> None:
    """Run the interactive REPL, falling back to plain input when needed."""

    telegram_startup = ensure_cli_telegram_daemon()
    console.clear()
    print_banner(cli_text=cli_text, theme=theme, model=model, **status_snapshot())
    if telegram_startup and telegram_startup.get("message"):
        color = "green" if telegram_startup.get("success") else "yellow"
        console.print(f"[{color}]  Telegram: {telegram_startup.get('message', '')}[/]")
        console.print()

    session = None
    prompt_style = None
    if PROMPT_TOOLKIT_AVAILABLE:
        history = _build_history(history_path, ensure_gary_home)
        session = PromptSession(
            history=history or InMemoryHistory(),
            complete_while_typing=False,
            enable_history_search=True,
            completer=completer,
            auto_suggest=AutoSuggestFromHistory(),
            reserve_space_for_menu=8,
        )
        prompt_style = Style.from_dict({"prompt": f"bold {theme}"})

    while True:
        try:
            _print_status_bar(
                model=model,
                tokens=agent._tokens(),
                cli_text=cli_text,
                **status_snapshot(),
            )
            if session is not None and HTML is not None:
                user_input = session.prompt(
                    HTML('<style color="cyan"><b>Gary > </b></style>'),
                    style=prompt_style,
                )
            else:
                user_input = input("Gary > ")

            if not user_input.strip():
                continue
            if user_input.startswith("/") or user_input.strip() == "?":
                handle_command(agent, user_input.strip())
                continue
            agent.chat(user_input)
        except KeyboardInterrupt:
            console.print(
                f"\n[dim]{cli_text('Ctrl+C 中断。/exit 退出。', 'Interrupted by Ctrl+C. Use /exit to quit.')}[/]"
            )
        except EOFError:
            shutdown_runtime(True)
            break


def run_oneshot(agent: Any, task: str) -> str:
    """Run a single non-interactive chat task."""

    console.print(f"\n[cyan]  ▶ Gary do: {task}[/]\n")
    return agent.chat(task)


def run_doctor(*, cli_text: Callable[[str, str], str]) -> None:
    """Check AI settings, toolchain, dependencies, and hardware visibility."""

    from ai.client import (
        _api_key_is_placeholder,
        _mask_key,
        _read_ai_config,
        get_ai_client,
        reload_ai_config,
    )
    from config import WORKSPACE
    from hardware.serial_mon import detect_serial_ports

    console.print()
    console.rule("[bold cyan]  Gary Doctor  —  环境诊断[/]")
    console.print()
    all_ok = True

    console.print("[bold]■ AI 接口[/]")
    cur_key, cur_url, cur_model = _read_ai_config()
    ai_configured = bool(cur_key and not _api_key_is_placeholder(cur_key))
    if ai_configured:
        console.print(f"  [green]✓[/] API Key   {_mask_key(cur_key)}")
        console.print(f"  [green]✓[/] Base URL  {cur_url}")
        console.print(f"  [green]✓[/] Model     {cur_model}")
        try:
            reload_ai_config()
            client = get_ai_client(timeout=8.0, force_reload=True)
            client.models.list()
            console.print("  [green]✓[/] API 连通性  [dim]测试通过[/]")
        except Exception as exc:
            err_msg = str(exc)[:80]
            if any(code in err_msg for code in ("401", "403", "404", "400")):
                console.print(f"  [yellow]⚠[/] API 连通性  [dim]{err_msg}[/]")
            else:
                console.print(f"  [red]✗[/] API 连通性  [dim]{err_msg}[/]")
                console.print("    [dim]→ 运行 Gary config 重新设置 API Key[/]")
                all_ok = False
    else:
        console.print("  [red]✗[/] API Key 未配置")
        console.print("    [dim]→ 运行 Gary config 配置 AI 接口[/]")
        all_ok = False
    console.print()

    console.print("[bold]■ 编译工具链[/]")
    gcc = shutil.which("arm-none-eabi-gcc")
    if gcc:
        try:
            result = subprocess.run([gcc, "--version"], capture_output=True, text=True, check=False)
            version = result.stdout.split("\n")[0][:70]
        except Exception:
            version = gcc
        console.print(f"  [green]✓[/] arm-none-eabi-gcc  [dim]{version}[/]")
    else:
        console.print("  [red]✗[/] arm-none-eabi-gcc  未找到")
        console.print("    [dim]→ sudo apt install gcc-arm-none-eabi  或  python3 setup.py --auto[/]")
        all_ok = False

    hal_dir = WORKSPACE / "hal"
    hal_found = []
    for family in ("f0", "f1", "f3", "f4"):
        if (hal_dir / "Inc" / f"stm32{family}xx_hal.h").exists():
            hal_found.append(f"STM32{family.upper()}xx")
    cmsis_ok = (hal_dir / "CMSIS" / "Include" / "core_cm3.h").exists()
    if hal_found and cmsis_ok:
        console.print(f"  [green]✓[/] HAL 库      {', '.join(hal_found)}")
        console.print("  [green]✓[/] CMSIS Core")
    elif hal_found:
        console.print(f"  [yellow]⚠[/] HAL 库      {', '.join(hal_found)}（CMSIS Core 缺失）")
        console.print("    [dim]→ python3 setup.py --hal[/]")
        all_ok = False
    else:
        console.print("  [yellow]⚠[/] HAL 库      未下载（仅代码生成模式）")
        console.print("    [dim]→ python3 setup.py --hal  下载所需系列[/]")
    console.print()

    console.print("[bold]■ Python 依赖[/]")
    required = [("openai", "openai"), ("rich", "rich"), ("prompt_toolkit", "prompt_toolkit")]
    optional = [
        ("serial", "pyserial"),
        ("pyocd", "pyocd"),
        ("docx", "python-docx"),
        ("PIL", "Pillow"),
    ]
    for module_name, package_name in required:
        try:
            __import__(module_name)
            console.print(f"  [green]✓[/] {package_name}")
        except ImportError:
            console.print(f"  [red]✗[/] {package_name}  [dim][必须] pip install {package_name}[/]")
            all_ok = False
    for module_name, package_name in optional:
        try:
            __import__(module_name)
            console.print(f"  [green]✓[/] {package_name}  [dim](可选)[/]")
        except Exception:
            console.print(f"  [dim]○[/] {package_name}  [dim](可选，pip install {package_name})[/]")
    console.print()

    console.print("[bold]■ 硬件探针[/]")
    try:
        import pyocd.probe.usb_probe as usb_probe

        probes = usb_probe.USBProbe.get_all_connected_probes(unique_id=None, is_explicit=False)
        if probes:
            for probe in probes:
                console.print(f"  [green]✓[/] {probe.description}  [dim]({probe.unique_id})[/]")
        else:
            console.print("  [yellow]⚠[/] 未检测到探针  [dim](连接 ST-Link / CMSIS-DAP 后重试)[/]")
    except Exception:
        console.print("  [dim]○[/] pyocd 未安装，无法扫描探针")

    serial_ports = detect_serial_ports(verbose=False)
    if serial_ports:
        for port in serial_ports:
            console.print(f"  [green]✓[/] 串口 {port}")
    else:
        console.print(f"  [dim]○[/] {cli_text('未检测到串口设备', 'No serial devices detected')}")
    console.print()

    if all_ok:
        console.print("[bold green]  ✅  所有核心配置正常，Gary 已就绪！[/]")
    else:
        console.print("[bold yellow]  ⚠  存在问题，请按上方提示修复[/]")
    console.print()


__all__ = [
    "console",
    "run_interactive",
    "run_oneshot",
    "print_banner",
    "run_doctor",
    "Panel",
    "Markdown",
    "Table",
    "box",
]
