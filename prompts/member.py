"""Prompt formatter for member memory."""

from __future__ import annotations

import hashlib

from core.platforms import is_micropython_target
from core.memory import (
    MEMBER_PROMPT_CHAR_LIMIT,
    MEMBER_PROMPT_MAX_DYNAMIC,
    _MEMBER_LOCK,
    _ensure_member_file,
    _split_member_content,
)


def _entry_matches_platform(entry: str, chip: str | None) -> bool:
    """Return whether one memory entry should be injected for the current platform."""

    if not is_micropython_target(chip):
        return True
    text = entry.lower()
    blocked_keywords = (
        "stm32",
        "hal_",
        "haldelay",
        "systick_handler",
        "hardfault",
        "cfsr",
        "pyocd",
        "_sbrk",
        "main.c",
    )
    return not any(keyword in text for keyword in blocked_keywords)


def _render_member_prompt_section(current: str, chip: str | None = None) -> str:
    """Render one trimmed member-memory section from raw member.md text."""

    header, entries = _split_member_content(current)
    pinned = [
        entry
        for entry in entries
        if entry.startswith("### [Pinned]") and _entry_matches_platform(entry, chip)
    ]
    dynamic = [
        entry
        for entry in entries
        if not entry.startswith("### [Pinned]") and _entry_matches_platform(entry, chip)
    ]

    selected: list[str] = []
    total = len(header)
    for entry in pinned:
        needed = len(entry) + 2
        if selected and total + needed > MEMBER_PROMPT_CHAR_LIMIT:
            break
        selected.append(entry)
        total += needed

    recent: list[str] = []
    for entry in reversed(dynamic):
        needed = len(entry) + 2
        if recent and (
            total + needed > MEMBER_PROMPT_CHAR_LIMIT or len(recent) >= MEMBER_PROMPT_MAX_DYNAMIC
        ):
            break
        recent.append(entry)
        total += needed
    recent.reverse()
    selected.extend(recent)

    excerpt = header.rstrip()
    if selected:
        excerpt += "\n\n" + "\n\n".join(selected)
    return (
        "## Gary Memory（重点）\n"
        "以下内容来自 member.md，是 `Gary` 的长期经验库。优先复用这些成功经验；"
        "遇到新的高价值经验时，调用 `gary_save_member_memory` 写进去；"
        "发现错误、过时、无用经验时，调用 `gary_delete_member_memory` 删除。\n\n"
        f"{excerpt.strip()}"
    )


def get_member_prompt_section_state(chip: str | None = None) -> tuple[str, str]:
    """Return `(section, content_hash)` for the current member prompt snippet."""

    # `core.memory` owns persistence and pruning rules. This formatter only
    # consumes its helpers and the persisted markdown artifact.
    with _MEMBER_LOCK:
        path = _ensure_member_file()
        current = path.read_text(encoding="utf-8")
    section = _render_member_prompt_section(current, chip)
    digest = hashlib.sha1(section.encode("utf-8")).hexdigest()
    return section, digest


def get_member_prompt_section(chip: str | None = None) -> str:
    """Return the trimmed member-memory section injected into the system prompt."""

    section, _ = get_member_prompt_section_state(chip)
    return section
