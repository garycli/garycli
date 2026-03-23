"""Public TUI API."""

from .commands import GaryCompleter, handle_slash_command
from .ui import console, print_banner, run_doctor, run_interactive, run_oneshot

__all__ = [
    "console",
    "run_interactive",
    "run_oneshot",
    "print_banner",
    "run_doctor",
    "handle_slash_command",
    "GaryCompleter",
]
