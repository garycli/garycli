"""System prompt construction helpers."""

from __future__ import annotations

from pathlib import Path

from config import DEFAULT_CLOCK
from core.platforms import (
    canonical_target_name,
    device_main_path_for_target,
    device_root_for_target,
    detect_target_platform,
    is_micropython_target,
    source_filename_for_target,
    target_runtime_label,
)

_TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"


def _load_template(name: str) -> str:
    """Load a markdown prompt template from disk."""

    return (_TEMPLATES_DIR / name).read_text(encoding="utf-8").strip()


def build_system_prompt(chip: str, language: str, hw_connected: bool) -> str:
    """Build the base system prompt with dynamic runtime context."""

    normalized_language = "en" if str(language).strip().lower().startswith("en") else "zh"
    chip_name = canonical_target_name(chip)
    platform = detect_target_platform(chip_name)
    if platform == "rp2040":
        template_name = "rp2040_en.md" if normalized_language == "en" else "rp2040_zh.md"
    elif platform == "canmv":
        template_name = "canmv_k230_en.md" if normalized_language == "en" else "canmv_k230_zh.md"
    elif platform == "esp":
        template_name = "esp_en.md" if normalized_language == "en" else "esp_zh.md"
    else:
        template_name = "system_en.md" if normalized_language == "en" else "system_zh.md"
    prompt = _load_template(template_name)
    if normalized_language == "en":
        prompt += (
            "\n\n## Reply Language\n"
            "- Current CLI language: English.\n"
            "- Reply in English by default, including tool result summaries.\n"
            "- Only switch to Chinese if the user explicitly asks for Chinese."
        )
    else:
        prompt += (
            "\n\n## 回复语言\n"
            "- 当前 CLI 语言：中文。\n"
            "- 默认使用中文回复。\n"
            "- 若用户明确要求英文，或全程使用英文交流，再切换为英文。"
        )
    if normalized_language == "en":
        if is_micropython_target(chip_name):
            dynamic = (
                "\n\n## Runtime Context\n"
                f"- Current target: `{chip_name}`\n"
                f"- Runtime: `{target_runtime_label(chip_name)}`\n"
                f"- Source file: `{source_filename_for_target(chip_name)}`\n"
                f"- Device main path: `{device_main_path_for_target(chip_name)}`\n"
                f"- Writable device root: `{device_root_for_target(chip_name)}`\n"
                f"- CLI language: `{normalized_language}`\n"
                f"- Hardware connected: `{str(bool(hw_connected)).lower()}`\n"
                "- Deployment transport: `USB serial raw REPL`\n"
                "- If hardware is disconnected, prefer syntax validation and explain that runtime verification is limited."
            )
        else:
            dynamic = (
                "\n\n## Runtime Context\n"
                f"- Current chip: `{chip_name}`\n"
                f"- Clock source: `{DEFAULT_CLOCK}`\n"
                f"- Runtime: `{target_runtime_label(chip_name)}`\n"
                f"- CLI language: `{normalized_language}`\n"
                f"- Hardware connected: `{str(bool(hw_connected)).lower()}`\n"
                "- If hardware is disconnected, prefer compile-first guidance and state the verification limit clearly."
            )
    else:
        if is_micropython_target(chip_name):
            dynamic = (
                "\n\n## 当前运行上下文\n"
                f"- 当前目标板：`{chip_name}`\n"
                f"- 当前运行时：`{target_runtime_label(chip_name)}`\n"
                f"- 当前主源码：`{source_filename_for_target(chip_name)}`\n"
                f"- 板端主脚本路径：`{device_main_path_for_target(chip_name)}`\n"
                f"- 板端可写根目录：`{device_root_for_target(chip_name)}`\n"
                f"- 当前 CLI 语言：`{normalized_language}`\n"
                f"- 当前硬件连接状态：`{str(bool(hw_connected)).lower()}`\n"
                "- 当前部署通道：`USB 串口 raw REPL`\n"
                "- 若硬件未连接，优先走语法检查和缓存路径，并明确说明无法做运行时验证。"
            )
        else:
            dynamic = (
                "\n\n## 当前运行上下文\n"
                f"- 当前芯片：`{chip_name}`\n"
                f"- 当前时钟源：`{DEFAULT_CLOCK}`\n"
                f"- 当前运行时：`{target_runtime_label(chip_name)}`\n"
                f"- 当前 CLI 语言：`{normalized_language}`\n"
                f"- 当前硬件连接状态：`{str(bool(hw_connected)).lower()}`\n"
                "- 若硬件未连接，优先走可编译路径，并明确说明无法做运行时验证。"
            )
    if normalized_language == "en":
        web_workflow = (
            "\n\n## Web Research Workflow\n"
            "- For online docs, latest information, API references, and tutorials, prefer this flow: "
            "`browser_search -> browser_open_result -> browser_extract_links`.\n"
            "- Do not stop after only listing search hits. Open the most relevant result and read the page.\n"
            "- If the target URL is already known, use `browser_open` directly.\n"
            "- Use `fetch_url` only for lightweight exact-URL text fetches when title and links are not needed.\n"
            "- `browser_search` and `web_search` depend on a local SearXNG instance. If search fails, clearly tell the user to start local SearXNG or run `python setup.py --searxng`.\n"
            "- Do not silently switch to public search backends when local SearXNG is unavailable."
        )
    else:
        web_workflow = (
            "\n\n## 联网检索工作流\n"
            "- 需要查在线文档、最新信息、API 说明或教程时，优先走："
            "`browser_search -> browser_open_result -> browser_extract_links`。\n"
            "- 不要只停留在搜索结果列表，必须打开最相关网页并读取正文。\n"
            "- 已知目标 URL 时，直接用 `browser_open`。\n"
            "- `fetch_url` 只用于已知 URL 的轻量纯文本抓取；若需要标题和链接列表，优先用 `browser_open`。\n"
            "- `browser_search` 和 `web_search` 依赖本地 SearXNG；若搜索失败，要明确提示用户启动本地 SearXNG，或运行 `python setup.py --searxng` 完成一键安装。\n"
            "- 本地 SearXNG 不可用时，不要擅自切换到公共搜索后端。"
        )
    return prompt.rstrip() + dynamic + web_workflow
