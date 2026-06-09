# ShotAPI — Web Screenshot & Render MCP Server for AI Agents

Give your AI Agent eyes. One command, zero install.

[![GitHub stars](https://img.shields.io/github/stars/smallhandsome/shotapi-mcp-server)](https://github.com/smallhandsome/shotapi-mcp-server)
[![MCP Registry](https://img.shields.io/badge/MCP-Registry-blue)](https://registry.modelcontextprotocol.io/servers/io.github.smallhandsome/shotapi-mcp-server)

[中文文档](README_CN.md)

## Quick Start (Remote Mode — No Install)

```bash
# Claude Code
claude mcp add --transport streamable-http shotapi https://aiphotoshop.mynatapp.cc/mcp

# Or with npx
npx -y @anthropic-ai/claude-code@latest --mcp https://aiphotoshop.mynatapp.cc/mcp
```

For Claude Desktop / Cursor, add to your config:

```json
{
  "mcpServers": {
    "shotapi": {
      "type": "streamable-http",
      "url": "https://aiphotoshop.mynatapp.cc/mcp"
    }
  }
}
```

## Real Use Cases

### 1. Claude verifies its own code

```
Human: Build a landing page with a hero section, testimonials, and pricing grid.

Claude: [writes HTML/CSS code]

Claude: Let me check this with the render tool...

[Claude calls ShotAPI render tool with the HTML it wrote]

Claude: The pricing grid overlaps on mobile. Fixing responsive breakpoints...
```

### 2. Deployment verification

```
Human: I just deployed. Check if it looks right.

Claude: [calls ShotAPI screenshot on https://yourapp.com]

Claude: Footer text is cut off — CSS overflow issue. Background image 404.
```

### 3. UI regression in CI/CD

```bash
# Capture before/after screenshots and compare
curl -s "https://aiphotoshop.mynatapp.cc/v1/screenshot?url=https://staging.myapp.com" -o before.png
curl -s "https://aiphotoshop.mynatapp.cc/v1/screenshot?url=https://staging.myapp.com" -o after.png
```

## 3 MCP Tools

| Tool | Description | Example |
|------|-------------|---------|
| `screenshot_one_liner` | One URL, one screenshot | `screenshot_one_liner(url="https://github.com")` |
| `screenshot` | Full control: viewport, full-page, CSS selector, format | `screenshot(url="https://github.com", selector="#hero")` |
| `render` | Render HTML/CSS to image — Agent writes code, sees result instantly | `render(html="<h1>Hello</h1>")` |

The `render` tool closes the feedback loop: **write code → render → see → revise → render again**.

## Why ShotAPI?

- **MCP-native** — No glue code. Agent calls tools directly in conversation.
- **Zero install remote mode** — streamable-http, no Python/Playwright needed.
- **Direct China access** — No VPN required.
- **Free tier** — 100 screenshots + 100 renders/month, IP-based, no signup, no API key.
- **Render capability** — Not just screenshots of existing pages. Render Agent-generated HTML.
- **Built-in ad blocking** — Cleaner screenshots, less noise.
- **Listed in MCP Registry** — Official Anthropic MCP server directory.

## Try It Now (No Signup)

```bash
curl -s "https://aiphotoshop.mynatapp.cc/v1/screenshot?url=https://github.com" -o shot.jpg
```

## Pricing

| Plan | Price | Limit |
|------|-------|-------|
| Free | $0 | 100+100/month (IP-based, no signup) |
| Starter | $4.90/mo | 5,000/month |
| Pro | $9.90/mo | 20,000/month |

Free tier: no API key needed. Paid: get key at [pricing page](https://aiphotoshop.mynatapp.cc/pricing).

## Local Mode (STDIO)

For private deployments or paid-tier usage, run locally:

```bash
# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Set env vars
export SHOTAPI_BASE_URL=https://aiphotoshop.mynatapp.cc
export SHOTAPI_KEY=your_key_here  # optional for paid tiers

# Add to Claude Code
claude mcp add shotapi python mcp_stdio.py
```

## Links

- **Docs**: https://aiphotoshop.mynatapp.cc/docs
- **Pricing**: https://aiphotoshop.mynatapp.cc/pricing
- **Health**: https://aiphotoshop.mynatapp.cc/health
- **MCP Registry**: https://registry.modelcontextprotocol.io/servers/io.github.smallhandsome/shotapi-mcp-server
- **Smithery**: https://smithery.ai/server/@ljs/shotapi
- **awesome-mcp-servers**: https://github.com/punkpeye/awesome-mcp-servers
- **Dev.to Article**: https://dev.to/smallhandsome/give-your-ai-agent-eyes-building-a-visual-mcp-server-for-web-screenshots-3f49