"""ShotAPI MCP Server — standalone version for Smithery/stdio deployment

Connects to remote ShotAPI API via HTTP. No local Playwright needed.
- Free tier: IP-based, 100+100/month, no API key
- Paid tier: SHOTAPI_KEY env var → 20K+ calls/month
"""

import asyncio
import os
import base64
import logging
import argparse

import httpx
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent, ImageContent

logger = logging.getLogger("shotapi.mcp")

SHOTAPI_BASE_URL = os.getenv("SHOTAPI_BASE_URL", "https://aiphotoshop.mynatapp.cc")
SHOTAPI_KEY = os.getenv("SHOTAPI_KEY", "")

mcp = FastMCP(
    "ShotAPI",
    stateless_http=True,
    streamable_http_path="/",
)

_client: httpx.AsyncClient | None = None
_client_lock = asyncio.Lock()


async def _get_client() -> httpx.AsyncClient:
    global _client
    async with _client_lock:
        if _client is None or _client.is_closed:
            headers = {}
            if SHOTAPI_KEY:
                headers["X-API-Key"] = SHOTAPI_KEY
            _client = httpx.AsyncClient(
                base_url=SHOTAPI_BASE_URL,
                headers=headers,
                timeout=60.0,
                trust_env=False,
            )
    return _client


async def close_client():
    global _client
    if _client and not _client.is_closed:
        await _client.aclose()
        _client = None


def _build_path(endpoint: str) -> str:
    if SHOTAPI_KEY:
        return f"/v1/auth/{endpoint}"
    return f"/v1/{endpoint}"


def _extract_metadata(headers: httpx.Headers, format: str, size: int) -> str:
    lines = [
        f"Format: {format}, Size: {size / 1024:.0f}KB",
        f"Tier: {'paid (API Key)' if SHOTAPI_KEY else 'free (IP-based)'}",
    ]
    if "x-cache" in headers:
        lines.append(f"Cache: {headers['x-cache']}")
    if "x-ratelimit-limit" in headers:
        used = int(headers.get("x-ratelimit-used", "0"))
        limit = int(headers.get("x-ratelimit-limit", "0"))
        lines.append(f"RateLimit: {used}/{limit}")
        if not SHOTAPI_KEY and used >= int(limit * 0.8):
            lines.append(f"Approaching free limit ({used}/{limit}). Upgrade Pro: https://aiphotoshop.mynatapp.cc/en/pricing")
    if "x-usage-count" in headers:
        lines.append(f"Usage: {headers['x-usage-count']}/{headers['x-usage-limit']}")
    return "\n".join(lines)


MIME_MAP = {"png": "image/png", "jpeg": "image/jpeg", "webp": "image/webp"}


async def _call_and_return(path: str, params: dict | None, body: dict | None, format: str) -> list:
    client = await _get_client()
    try:
        if body:
            resp = await client.post(path, json=body)
        else:
            resp = await client.get(path, params=params)
    except httpx.TimeoutException:
        return [TextContent(type="text", text="Error: request timed out. The page may be slow to load — try again or increase timeout.")]
    except httpx.ConnectError:
        return [TextContent(type="text", text="Error: cannot reach ShotAPI server. Is it running?")]

    if resp.status_code != 200:
        try:
            error = resp.json().get("error", f"HTTP {resp.status_code}")
        except Exception:
            error = f"HTTP {resp.status_code}"
            logger.warning(f"Failed to parse error response: HTTP {resp.status_code}")
        return [TextContent(type="text", text=f"Error: {error}")]

    mime = MIME_MAP.get(format, "image/png")
    metadata = _extract_metadata(resp.headers, format, len(resp.content))
    image_b64 = base64.b64encode(resp.content).decode("ascii")
    return [
        TextContent(type="text", text=metadata),
        ImageContent(type="image", data=image_b64, mimeType=mime),
    ]


@mcp.tool()
async def screenshot_one_liner(url: str) -> list[TextContent | ImageContent]:
    """Capture a webpage as a JPEG screenshot. The simplest way to see what a webpage looks like.

    Use this when you need to quickly check a webpage's appearance, verify a design, or see content that requires rendering.
    Returns a 1280x720 JPEG image (~50KB) with ads blocked.

    Args:
        url: The URL to screenshot (e.g. "https://example.com")
    """
    return await _call_and_return(
        _build_path("screenshot"),
        params={"url": url, "format": "jpeg", "width": 1280, "height": 720, "block_ads": "true"},
        body=None,
        format="jpeg",
    )


@mcp.tool()
async def screenshot(
    url: str,
    width: int = 1280,
    height: int = 720,
    fullpage: bool = False,
    format: str = "jpeg",
    block_ads: bool = True,
    wait_for: str = "",
    selector: str = "",
) -> list[TextContent | ImageContent]:
    """Capture a webpage screenshot with full control over viewport, format, and element selection.

    Args:
        url: The URL to screenshot
        width: Viewport width in pixels (default: 1280)
        height: Viewport height in pixels (default: 720)
        fullpage: Capture the entire scrollable page instead of just the viewport (default: false)
        format: Image format — "jpeg" saves tokens (~50KB), "png" for quality, "webp" smallest (default: "jpeg")
        block_ads: Remove ads and cookie banners (default: true)
        wait_for: CSS selector to wait for before capturing, e.g. ".main-content" to ensure content loaded
        selector: CSS selector to capture only a specific element, e.g. ".hero" or "#pricing-table"
    """
    params = {
        "url": url,
        "width": width,
        "height": height,
        "fullpage": str(fullpage).lower(),
        "format": format,
        "block_ads": str(block_ads).lower(),
    }
    if wait_for:
        params["wait_for"] = wait_for
    if selector:
        params["selector"] = selector
    return await _call_and_return(
        _build_path("screenshot"),
        params=params,
        body=None,
        format=format,
    )


@mcp.tool()
async def render(
    html: str,
    width: int = 1280,
    height: int = 720,
    format: str = "jpeg",
) -> list[TextContent | ImageContent]:
    """Render HTML/CSS code as an image. Turn any markup into a visual preview.

    Useful for: previewing UI code, checking CSS layouts, turning design mockups into shareable images.
    Supports <style> tags, inline CSS, and common HTML features.
    Output is auto-cropped to content — no wasted blank space below.

    Args:
        html: The HTML/CSS code to render
        width: Viewport width in pixels (default: 1280)
        height: Viewport height in pixels — output auto-cropped to content (default: 720)
        format: Image format — "jpeg" saves tokens, "png" for crisp text, "webp" smallest (default: "jpeg")
    """
    return await _call_and_return(
        _build_path("render"),
        params=None,
        body={"html": html, "width": width, "height": height, "format": format},
        format=format,
    )