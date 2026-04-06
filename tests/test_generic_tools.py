"""Tests for generic file-edit helpers."""

from __future__ import annotations

from core.generic_tools import (
    browser_extract_links,
    browser_open,
    browser_open_result,
    browser_search,
    str_replace_edit,
)


def test_str_replace_edit_missing_latest_workspace_returns_actionable_hint(tmp_path):
    """Missing latest workspace files should return guidance instead of a bare path error."""

    missing = tmp_path / "workspace" / "projects" / "latest_workspace" / "main.py"
    result = str_replace_edit(str(missing), "old", "new")

    assert "文件不存在" in result["error"]
    assert "latest_workspace 还没有缓存源码" in result["error"]
    assert "compile / auto_sync_cycle" in result["error"]


class _DummyResponse:
    def __init__(self, *, json_data=None, html: str = "", url: str = "", status_code: int = 200):
        self._json_data = json_data
        self.content = html.encode("utf-8")
        self.url = url
        self.status_code = status_code

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            import requests

            raise requests.HTTPError(f"{self.status_code} Client Error")
        return None


def test_browser_search_respects_limit(monkeypatch):
    """Structured browser search should proxy SearX results and honor the limit."""

    monkeypatch.setattr(
        "core.generic_tools.requests.get",
        lambda *args, **kwargs: _DummyResponse(
            json_data={
                "results": [
                    {"title": "A", "url": "https://a.example", "content": "alpha"},
                    {"title": "B", "url": "https://b.example", "content": "beta"},
                    {"title": "C", "url": "https://c.example", "content": "gamma"},
                ]
            }
        ),
    )

    result = browser_search("k230 docs", limit=2)

    assert result["success"] is True
    assert result["query"] == "k230 docs"
    assert result["backend"] == "searxng"
    assert result["base_url"] == "http://127.0.0.1:8080"
    assert result["count"] == 2
    assert [item["title"] for item in result["results"]] == ["A", "B"]
    assert [item["id"] for item in result["results"]] == [1, 2]


def test_browser_search_uses_configured_local_searxng_url(monkeypatch):
    """Search should honor the configured local SearXNG base URL."""

    captured = {}

    def _fake_get(url, *args, **kwargs):
        captured["url"] = url
        return _DummyResponse(json_data={"results": []})

    monkeypatch.setenv("GARY_SEARXNG_URL", "http://127.0.0.1:18080/")
    monkeypatch.setattr("core.generic_tools.requests.get", _fake_get)

    result = browser_search("gary", limit=1)

    assert result["success"] is True
    assert result["base_url"] == "http://127.0.0.1:18080"
    assert captured["url"] == "http://127.0.0.1:18080/search"


def test_browser_search_falls_back_to_html_when_json_is_forbidden(monkeypatch):
    """Newer SearXNG defaults may disable JSON; browser_search should parse HTML results."""

    html = """
    <html><body>
      <article class="result">
        <h3><a href="https://docs.example/api">STM32 UART API</a></h3>
        <p class="content">Official UART guide for STM32.</p>
      </article>
      <article class="result">
        <h3><a href="/local">Local Result</a></h3>
        <p class="content">Fallback via HTML page.</p>
      </article>
    </body></html>
    """

    def _fake_get(url, *args, **kwargs):
        if kwargs.get("params", {}).get("format") == "json":
            return _DummyResponse(status_code=403, html="Forbidden", url=url)
        return _DummyResponse(html=html, url="http://127.0.0.1:8080/search?q=stm32")

    monkeypatch.setattr("core.generic_tools.requests.get", _fake_get)

    result = browser_search("stm32 uart", limit=2)

    assert result["success"] is True
    assert result["backend"] == "searxng_html"
    assert result["count"] == 2
    assert "已回退到 HTML 解析" in result["warning"]
    assert result["results"][0]["title"] == "STM32 UART API"
    assert result["results"][1]["url"] == "http://127.0.0.1:8080/local"


def test_browser_open_returns_text_title_and_links(monkeypatch):
    """Opening a page should expose title, cleaned text, and resolved links."""

    html = """
    <html>
      <head><title>K230 API</title><style>body { display:none; }</style></head>
      <body>
        <main>
          <h1>K230 Camera</h1>
          <p>Use the official CanMV sensor stack.</p>
          <a href="/sensor">Sensor API</a>
          <a href="https://docs.example/display">Display API</a>
        </main>
        <script>console.log('ignore me')</script>
      </body>
    </html>
    """
    monkeypatch.setattr(
        "core.generic_tools.requests.get",
        lambda *args, **kwargs: _DummyResponse(html=html, url="https://docs.example/start"),
    )

    result = browser_open("https://docs.example/start", max_chars=200)

    assert result["success"] is True
    assert result["title"] == "K230 API"
    assert "K230 Camera" in result["content"]
    assert "official CanMV sensor stack" in result["content"]
    assert "ignore me" not in result["content"]
    assert result["final_url"] == "https://docs.example/start"
    assert result["links"][0]["url"] == "https://docs.example/sensor"
    assert result["links"][1]["url"] == "https://docs.example/display"
    assert result["link_count"] == 2


def test_browser_extract_links_returns_only_link_payload(monkeypatch):
    """Link extraction should skip the page text and return structured links only."""

    html = """
    <html><body>
      <a href="/a">A</a>
      <a href="/b">B</a>
    </body></html>
    """
    monkeypatch.setattr(
        "core.generic_tools.requests.get",
        lambda *args, **kwargs: _DummyResponse(html=html, url="https://docs.example/root"),
    )

    result = browser_extract_links("https://docs.example/root")

    assert result["success"] is True
    assert result["link_count"] == 2
    assert [item["text"] for item in result["links"]] == ["A", "B"]
    assert "content" not in result


def test_browser_open_result_opens_selected_search_hit(monkeypatch):
    """Open-result should search first and then open the selected indexed result."""

    monkeypatch.setattr(
        "core.generic_tools.browser_search",
        lambda query, limit=5: {
            "success": True,
            "query": query,
            "results": [
                {"id": 1, "title": "A", "url": "https://a.example", "snippet": "alpha"},
                {"id": 2, "title": "B", "url": "https://b.example", "snippet": "beta"},
            ],
            "count": 2,
        },
    )
    monkeypatch.setattr(
        "core.generic_tools.browser_open",
        lambda url, max_chars=8000: {
            "success": True,
            "url": url,
            "final_url": url,
            "title": "Opened",
            "status_code": 200,
            "content": "page body",
            "links": [],
            "truncated": False,
            "content_chars": 9,
            "link_count": 0,
        },
    )

    result = browser_open_result("k230 camera", index=1)

    assert result["success"] is True
    assert result["url"] == "https://b.example"
    assert result["query"] == "k230 camera"
    assert result["search_index"] == 1
    assert result["search_result"]["title"] == "B"
