"""AI client management and provider-specific streaming helpers."""

from __future__ import annotations

import base64
import importlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator, Optional
from urllib.parse import urlparse

import config as _cfg

_ROOT = Path(__file__).resolve().parent.parent
_CONFIG_PATH = _ROOT / "config.py"

_AI_PRESETS = [
    ("OpenAI", "https://api.openai.com/v1", "gpt-4o"),
    ("DeepSeek", "https://api.deepseek.com/v1", "deepseek-chat"),
    ("Kimi / Moonshot", "https://api.moonshot.cn/v1", "kimi-k2.5"),
    ("Google Gemini (官方 SDK)", "https://generativelanguage.googleapis.com/", "gemini-2.5-flash"),
    ("通义千问 (阿里云)", "https://dashscope.aliyuncs.com/compatible-mode/v1", "qwen-plus"),
    ("智谱 GLM", "https://open.bigmodel.cn/api/paas/v4/", "glm-4-flash"),
    ("Ollama (本地)", "http://127.0.0.1:11434/v1", "qwen2.5-coder:14b"),
    ("自定义 / Other", "", ""),
]

_CONFIG_KEYS_TO_RELOAD = (
    "AI_API_KEY",
    "AI_BASE_URL",
    "AI_MODEL",
    "AI_TEMPERATURE",
    "DEFAULT_CHIP",
    "DEFAULT_CLOCK",
    "CLI_LANGUAGE",
    "SERIAL_PORT",
    "SERIAL_BAUD",
    "POST_FLASH_DELAY",
    "REGISTER_READ_DELAY",
)

AI_API_KEY = getattr(_cfg, "AI_API_KEY", "")
AI_BASE_URL = getattr(_cfg, "AI_BASE_URL", "https://api.openai.com/v1")
AI_MODEL = getattr(_cfg, "AI_MODEL", "gpt-4o")
AI_TEMPERATURE = getattr(_cfg, "AI_TEMPERATURE", 1)
DEFAULT_CHIP = getattr(_cfg, "DEFAULT_CHIP", "")
DEFAULT_CLOCK = getattr(_cfg, "DEFAULT_CLOCK", "HSI_internal")
CLI_LANGUAGE = getattr(_cfg, "CLI_LANGUAGE", "zh")
SERIAL_PORT = getattr(_cfg, "SERIAL_PORT", "")
SERIAL_BAUD = getattr(_cfg, "SERIAL_BAUD", 115200)
POST_FLASH_DELAY = getattr(_cfg, "POST_FLASH_DELAY", 1.5)
REGISTER_READ_DELAY = getattr(_cfg, "REGISTER_READ_DELAY", 0.3)

_AI_CLIENT: Any | None = None
_AI_CLIENT_SIGNATURE: tuple[str, str, str, float] | None = None


@dataclass
class _NormalizedFunctionDelta:
    name: str = ""
    arguments: str = ""
    thought_signature: str | None = None


@dataclass
class _NormalizedToolCallDelta:
    index: int
    id: str = ""
    function: _NormalizedFunctionDelta = field(default_factory=_NormalizedFunctionDelta)
    thought_signature: str | None = None


@dataclass
class _NormalizedDelta:
    content: str | None = None
    reasoning_content: str | None = None
    tool_calls: list[_NormalizedToolCallDelta] | None = None


@dataclass
class _NormalizedChoice:
    delta: _NormalizedDelta


@dataclass
class _NormalizedChunk:
    choices: list[_NormalizedChoice]
    _raw_tool_calls: list[dict[str, Any]] = field(default_factory=list)

    def model_dump(self) -> dict[str, Any]:
        return {
            "choices": [
                {
                    "delta": {
                        "tool_calls": self._raw_tool_calls,
                    }
                }
            ]
        }


def _load_openai_class() -> Any | None:
    """Import and return the OpenAI client class when available."""

    try:
        from openai import OpenAI  # type: ignore
    except ImportError:
        return None
    return OpenAI


def _load_gemini_sdk() -> tuple[Any | None, Any | None]:
    """Import and return `(genai, types)` from the official Gemini SDK."""

    try:
        from google import genai  # type: ignore
        from google.genai import types  # type: ignore
    except ImportError:
        return None, None
    return genai, types


def _parse_cli_language(value: Any, default: Optional[str] = None) -> Optional[str]:
    """Normalize CLI language aliases to `en` or `zh`."""

    raw = str(value or "").strip().lower()
    if not raw:
        return default
    if raw in {"en", "eng", "english", "英文"}:
        return "en"
    if raw in {"zh", "cn", "zh-cn", "zh_cn", "chinese", "中文"}:
        return "zh"
    return None


def _normalize_cli_language(value: Any) -> str:
    """Return a safe CLI language code."""

    return _parse_cli_language(value, default="zh") or "zh"


CLI_LANGUAGE = _normalize_cli_language(CLI_LANGUAGE)


def _current_settings() -> dict[str, Any]:
    """Return the current runtime configuration snapshot."""

    return {
        "AI_API_KEY": AI_API_KEY,
        "AI_BASE_URL": AI_BASE_URL,
        "AI_MODEL": AI_MODEL,
        "AI_TEMPERATURE": AI_TEMPERATURE,
        "DEFAULT_CHIP": DEFAULT_CHIP,
        "DEFAULT_CLOCK": DEFAULT_CLOCK,
        "CLI_LANGUAGE": CLI_LANGUAGE,
        "SERIAL_PORT": SERIAL_PORT,
        "SERIAL_BAUD": SERIAL_BAUD,
        "POST_FLASH_DELAY": POST_FLASH_DELAY,
        "REGISTER_READ_DELAY": REGISTER_READ_DELAY,
    }


def _upsert_config_assignment(text: str, key: str, value: Any) -> str:
    """Insert or replace a single assignment in `config.py` text."""

    line = f"{key} = {json.dumps(value, ensure_ascii=False)}"
    pattern = rf"^{key}\s*=.*$"
    if re.search(pattern, text, re.MULTILINE):
        return re.sub(pattern, line, text, flags=re.MULTILINE)
    if text and not text.endswith("\n"):
        text += "\n"
    return text + line + "\n"


def _read_ai_config() -> tuple[str, str, str]:
    """Read `(api_key, base_url, model)` from `config.py`."""

    if not _CONFIG_PATH.exists():
        return AI_API_KEY, AI_BASE_URL, AI_MODEL
    text = _CONFIG_PATH.read_text(encoding="utf-8")

    def _get(pattern: str) -> str:
        match = re.search(pattern, text, re.MULTILINE)
        return match.group(1).strip() if match else ""

    return (
        _get(r'^AI_API_KEY\s*=\s*["\']([^"\']*)["\']') or AI_API_KEY,
        _get(r'^AI_BASE_URL\s*=\s*["\']([^"\']*)["\']') or AI_BASE_URL,
        _get(r'^AI_MODEL\s*=\s*["\']([^"\']*)["\']') or AI_MODEL,
    )


def _write_config_assignments(updates: dict[str, Any]) -> bool:
    """Update multiple assignments in `config.py` in place."""

    if not _CONFIG_PATH.exists():
        return False
    text = _CONFIG_PATH.read_text(encoding="utf-8")
    for key, value in updates.items():
        text = _upsert_config_assignment(text, key, value)
    _CONFIG_PATH.write_text(text, encoding="utf-8")
    return True


def _write_ai_config(api_key: str, base_url: str, model: str) -> bool:
    """Persist the core AI settings to `config.py`."""

    return _write_config_assignments(
        {
            "AI_API_KEY": api_key,
            "AI_BASE_URL": base_url,
            "AI_MODEL": model,
        }
    )


def _write_cli_language_config(language: str) -> bool:
    """Persist the CLI language to `config.py`."""

    return _write_config_assignments({"CLI_LANGUAGE": _normalize_cli_language(language)})


def _reload_ai_globals() -> dict[str, Any]:
    """Reload runtime settings from `config.py` and invalidate the cached client if needed."""

    global AI_API_KEY
    global AI_BASE_URL
    global AI_MODEL
    global AI_TEMPERATURE
    global DEFAULT_CHIP
    global DEFAULT_CLOCK
    global CLI_LANGUAGE
    global SERIAL_PORT
    global SERIAL_BAUD
    global POST_FLASH_DELAY
    global REGISTER_READ_DELAY
    global _AI_CLIENT
    global _AI_CLIENT_SIGNATURE

    previous_signature = (AI_API_KEY, AI_BASE_URL, AI_MODEL)
    importlib.reload(_cfg)
    defaults = {
        "AI_API_KEY": "",
        "AI_BASE_URL": "https://api.openai.com/v1",
        "AI_MODEL": "gpt-4o",
        "AI_TEMPERATURE": 1,
        "DEFAULT_CHIP": "",
        "DEFAULT_CLOCK": "HSI_internal",
        "CLI_LANGUAGE": "zh",
        "SERIAL_PORT": "",
        "SERIAL_BAUD": 115200,
        "POST_FLASH_DELAY": 1.5,
        "REGISTER_READ_DELAY": 0.3,
    }
    for name in _CONFIG_KEYS_TO_RELOAD:
        globals()[name] = getattr(_cfg, name, defaults[name])
    CLI_LANGUAGE = _normalize_cli_language(CLI_LANGUAGE)
    if (AI_API_KEY, AI_BASE_URL, AI_MODEL) != previous_signature:
        _AI_CLIENT = None
        _AI_CLIENT_SIGNATURE = None
    return _current_settings()


def reload_ai_config() -> dict[str, Any]:
    """Public wrapper for reloading AI/runtime settings."""

    return _reload_ai_globals()


def _mask_key(key: str) -> str:
    """Mask a secret for CLI display."""

    if not key:
        return "(未设置)"
    return key[:6] + "..." + key[-4:] if len(key) > 12 else "***"


def _api_key_is_placeholder(api_key: str) -> bool:
    """Return whether the API key is empty or still using a template value."""

    key = (api_key or "").strip()
    if not key:
        return True
    placeholder_prefixes = ("YOUR_API_KEY", "sk-YOUR")
    return any(key.startswith(prefix) for prefix in placeholder_prefixes)


def _ai_is_configured() -> bool:
    """Return whether the runtime has a usable AI configuration."""

    api_key, base_url, model = _read_ai_config()
    return bool(api_key and base_url and model and not _api_key_is_placeholder(api_key))


def _extract_api_version_from_url(base_url: str) -> str | None:
    """Extract Gemini API version from a configured URL when present."""

    path = urlparse(base_url or "").path.strip("/")
    if not path:
        return None
    for segment in path.split("/"):
        if re.fullmatch(r"v\d+(?:alpha|beta)?\d*", segment):
            return segment
    return None


def _is_gemini_provider(base_url: str | None = None, model: str | None = None) -> bool:
    """Return whether the current config should use the official Gemini SDK."""

    target_url = (base_url or AI_BASE_URL or "").strip().lower()
    parsed = urlparse(target_url)
    host = parsed.netloc.lower()
    if host == "generativelanguage.googleapis.com" or host.endswith(
        ".generativelanguage.googleapis.com"
    ):
        return True
    return target_url in {"gemini", "gemini://official", "google-gemini"}


def _provider_kind(base_url: str | None = None, model: str | None = None) -> str:
    """Return the active provider kind."""

    return "gemini" if _is_gemini_provider(base_url=base_url, model=model) else "openai"


def provider_name(base_url: str | None = None, model: str | None = None) -> str:
    """Return a human-readable provider label."""

    return "Google Gemini (official SDK)" if _provider_kind(base_url, model) == "gemini" else (
        "OpenAI-compatible"
    )


def _build_gemini_http_options(timeout: float) -> dict[str, Any]:
    """Build HTTP options for the Gemini SDK from current runtime config."""

    http_options: dict[str, Any] = {"timeout": int(max(timeout, 1.0) * 1000)}
    if _is_gemini_provider(AI_BASE_URL, AI_MODEL):
        parsed = urlparse(AI_BASE_URL)
        if parsed.scheme and parsed.netloc:
            http_options["base_url"] = f"{parsed.scheme}://{parsed.netloc}/"
        api_version = _extract_api_version_from_url(AI_BASE_URL)
        if api_version:
            http_options["api_version"] = api_version
    return http_options


def _encode_thought_signature(value: Any) -> str:
    """Serialize Gemini thought signatures for message history."""

    if value is None:
        return ""
    if isinstance(value, bytes):
        return base64.b64encode(value).decode("ascii")
    if isinstance(value, str):
        return value
    return ""


def _decode_thought_signature(value: Any) -> bytes | None:
    """Decode a persisted Gemini thought signature back to bytes."""

    if not value:
        return None
    if isinstance(value, bytes):
        return value
    if not isinstance(value, str):
        return None
    try:
        return base64.b64decode(value.encode("ascii"), validate=True)
    except Exception:
        return value.encode("utf-8")


def get_ai_client(timeout: float = 180.0, force_reload: bool = False) -> Any | None:
    """Return a lazily-created client for the current provider config."""

    global _AI_CLIENT
    global _AI_CLIENT_SIGNATURE

    kind = _provider_kind(AI_BASE_URL, AI_MODEL)
    signature = (kind, AI_API_KEY, AI_BASE_URL, float(timeout))
    if force_reload:
        _AI_CLIENT = None
        _AI_CLIENT_SIGNATURE = None
    if _AI_CLIENT is not None and _AI_CLIENT_SIGNATURE == signature:
        return _AI_CLIENT

    if kind == "gemini":
        genai, _ = _load_gemini_sdk()
        if genai is None:
            return None
        kwargs: dict[str, Any] = {"api_key": AI_API_KEY}
        http_options = _build_gemini_http_options(timeout)
        if http_options:
            kwargs["http_options"] = http_options
        _AI_CLIENT = genai.Client(**kwargs)
        _AI_CLIENT_SIGNATURE = signature
        return _AI_CLIENT

    openai_class = _load_openai_class()
    if openai_class is None:
        return None
    _AI_CLIENT = openai_class(api_key=AI_API_KEY, base_url=AI_BASE_URL, timeout=timeout)
    _AI_CLIENT_SIGNATURE = signature
    return _AI_CLIENT


def probe_ai_connection(client: Any | None = None, timeout: float = 8.0) -> None:
    """Perform a minimal provider-specific connectivity probe."""

    active_client = client or get_ai_client(timeout=timeout)
    if active_client is None:
        if _provider_kind(AI_BASE_URL, AI_MODEL) == "gemini":
            raise RuntimeError("google-genai 未安装: pip install google-genai")
        raise RuntimeError("openai 未安装: pip install openai")

    if _provider_kind(AI_BASE_URL, AI_MODEL) == "gemini":
        pager = active_client.models.list(config={"page_size": 1})
        next(iter(pager), None)
        return

    active_client.models.list()


def _coerce_tool_payload(raw_content: Any) -> dict[str, Any]:
    """Convert a tool message body into Gemini function-response JSON."""

    if isinstance(raw_content, dict):
        return raw_content
    if isinstance(raw_content, list):
        return {"output": raw_content}
    text = str(raw_content or "").strip()
    if not text:
        return {"output": ""}
    try:
        parsed = json.loads(text)
    except Exception:
        return {"output": text}
    if isinstance(parsed, dict):
        return parsed
    return {"output": parsed}


def _assistant_message_to_gemini_parts(message: dict[str, Any], types_mod: Any) -> list[Any]:
    """Convert an assistant history message into Gemini parts."""

    parts: list[Any] = []
    reasoning = str(message.get("reasoning_content") or "")
    if reasoning:
        parts.append(types_mod.Part(text=reasoning, thought=True))

    content = str(message.get("content") or "")
    if content:
        parts.append(types_mod.Part.from_text(text=content))

    for tool_call in message.get("tool_calls") or []:
        func = tool_call.get("function") or {}
        args_text = str(func.get("arguments") or "").strip()
        try:
            args = json.loads(args_text) if args_text else {}
        except Exception:
            args = {"raw_arguments": args_text}
        part = types_mod.Part(
            function_call=types_mod.FunctionCall(
                id=tool_call.get("id") or None,
                name=func.get("name") or None,
                args=args,
            ),
            thought_signature=_decode_thought_signature(func.get("thought_signature")),
        )
        parts.append(part)
    return parts


def _tool_message_to_gemini_parts(message: dict[str, Any], types_mod: Any) -> list[Any]:
    """Convert a tool response history message into Gemini parts."""

    name = str(message.get("name") or "").strip()
    response = types_mod.FunctionResponse(
        id=message.get("tool_call_id") or None,
        name=name or None,
        response=_coerce_tool_payload(message.get("content")),
    )
    return [types_mod.Part(function_response=response)]


def _messages_to_gemini_payload(messages: list[dict[str, Any]], types_mod: Any) -> tuple[str, list[Any]]:
    """Convert Gary's OpenAI-style history into Gemini `contents` + `system_instruction`."""

    system_parts: list[str] = []
    contents: list[Any] = []

    for message in messages:
        role = str(message.get("role") or "").strip().lower()
        if role == "system":
            text = str(message.get("content") or "").strip()
            if text:
                system_parts.append(text)
            continue

        if role == "assistant":
            parts = _assistant_message_to_gemini_parts(message, types_mod)
            target_role = "model"
        elif role == "tool":
            parts = _tool_message_to_gemini_parts(message, types_mod)
            target_role = "user"
        else:
            text = str(message.get("content") or "")
            parts = [types_mod.Part.from_text(text=text)] if text else []
            target_role = "user"

        if parts:
            contents.append(types_mod.Content(role=target_role, parts=parts))

    return "\n\n".join(system_parts).strip(), contents


def _openai_tools_to_gemini_tools(tools: Optional[list[dict[str, Any]]], types_mod: Any) -> list[Any]:
    """Convert OpenAI function schemas into Gemini function declarations."""

    if not tools:
        return []

    declarations = []
    for tool in tools:
        if tool.get("type") != "function":
            continue
        func = tool.get("function") or {}
        declarations.append(
            types_mod.FunctionDeclaration(
                name=func.get("name") or "",
                description=func.get("description") or "",
                parameters_json_schema=func.get("parameters")
                or {"type": "object", "properties": {}, "required": []},
            )
        )

    if not declarations:
        return []
    return [types_mod.Tool(function_declarations=declarations)]


def _normalize_gemini_chunk(chunk: Any) -> _NormalizedChunk:
    """Project a Gemini SDK response chunk into an OpenAI-like delta shape."""

    try:
        parts = chunk.parts or []
    except Exception:
        try:
            parts = ((chunk.candidates or [])[0].content.parts or [])
        except Exception:
            parts = []

    text_parts: list[str] = []
    reasoning_parts: list[str] = []
    tool_calls: list[_NormalizedToolCallDelta] = []
    raw_tool_calls: list[dict[str, Any]] = []

    for index, part in enumerate(parts):
        function_call = getattr(part, "function_call", None)
        if function_call is not None:
            args_text = json.dumps(function_call.args or {}, ensure_ascii=False)
            thought_signature = _encode_thought_signature(getattr(part, "thought_signature", None))
            func = _NormalizedFunctionDelta(
                name=function_call.name or "",
                arguments=args_text,
                thought_signature=thought_signature or None,
            )
            tool_call = _NormalizedToolCallDelta(
                index=index,
                id=function_call.id or f"gemini-call-{index}",
                function=func,
                thought_signature=thought_signature or None,
            )
            tool_calls.append(tool_call)
            raw = {
                "id": tool_call.id,
                "function": {
                    "name": func.name,
                    "arguments": func.arguments,
                },
            }
            if thought_signature:
                raw["function"]["thought_signature"] = thought_signature
            raw_tool_calls.append(raw)
            continue

        text = getattr(part, "text", None)
        if not text:
            continue
        if getattr(part, "thought", False):
            reasoning_parts.append(text)
        else:
            text_parts.append(text)

    delta = _NormalizedDelta(
        content="".join(text_parts) or None,
        reasoning_content="".join(reasoning_parts) or None,
        tool_calls=tool_calls or None,
    )
    return _NormalizedChunk(choices=[_NormalizedChoice(delta=delta)], _raw_tool_calls=raw_tool_calls)


def _stream_chat_gemini(
    *,
    messages: list[dict[str, Any]],
    tools: Optional[list[dict[str, Any]]] = None,
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    client: Any | None = None,
    timeout: float = 180.0,
) -> Iterator[_NormalizedChunk]:
    """Create a Gemini official SDK streaming request and normalize its chunks."""

    _, types_mod = _load_gemini_sdk()
    active_client = client or get_ai_client(timeout=timeout)
    if active_client is None or types_mod is None:
        raise RuntimeError("google-genai 未安装: pip install google-genai")

    system_instruction, contents = _messages_to_gemini_payload(messages, types_mod)
    config = types_mod.GenerateContentConfig(
        system_instruction=system_instruction or None,
        temperature=AI_TEMPERATURE if temperature is None else temperature,
        tools=_openai_tools_to_gemini_tools(tools, types_mod) or None,
        automatic_function_calling=types_mod.AutomaticFunctionCallingConfig(disable=True),
        thinking_config=types_mod.ThinkingConfig(include_thoughts=True),
    )

    stream = active_client.models.generate_content_stream(
        model=model or AI_MODEL,
        contents=contents,
        config=config,
    )
    for chunk in stream:
        yield _normalize_gemini_chunk(chunk)


def stream_chat(
    *,
    messages: list[dict[str, Any]],
    tools: Optional[list[dict[str, Any]]] = None,
    tool_choice: str | dict[str, Any] = "auto",
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    client: Any | None = None,
    timeout: float = 180.0,
) -> Any:
    """Create a streaming chat request using the active provider runtime config."""

    if _provider_kind(AI_BASE_URL, AI_MODEL) == "gemini":
        return _stream_chat_gemini(
            messages=messages,
            tools=tools,
            model=model,
            temperature=temperature,
            client=client,
            timeout=timeout,
        )

    active_client = client or get_ai_client(timeout=timeout)
    if active_client is None:
        raise RuntimeError("openai 未安装: pip install openai")
    request: dict[str, Any] = {
        "model": model or AI_MODEL,
        "messages": messages,
        "temperature": AI_TEMPERATURE if temperature is None else temperature,
        "stream": True,
    }
    if tools is not None:
        request["tools"] = tools
        request["tool_choice"] = tool_choice
    return active_client.chat.completions.create(**request)


__all__ = [
    "AI_API_KEY",
    "AI_BASE_URL",
    "AI_MODEL",
    "AI_TEMPERATURE",
    "CLI_LANGUAGE",
    "DEFAULT_CHIP",
    "DEFAULT_CLOCK",
    "POST_FLASH_DELAY",
    "REGISTER_READ_DELAY",
    "SERIAL_BAUD",
    "SERIAL_PORT",
    "_AI_PRESETS",
    "_ai_is_configured",
    "_api_key_is_placeholder",
    "_is_gemini_provider",
    "_mask_key",
    "_provider_kind",
    "_read_ai_config",
    "_reload_ai_globals",
    "_write_ai_config",
    "_write_cli_language_config",
    "get_ai_client",
    "probe_ai_connection",
    "provider_name",
    "reload_ai_config",
    "stream_chat",
]
