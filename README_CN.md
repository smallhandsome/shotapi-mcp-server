# ShotAPI — AI Agent 网页截图与渲染 MCP Server

[![Product Hunt](https://api.producthunt.com/widgets/embed-image/v1/top-post-badge.svg?post_id=960936&theme=light&period=daily)](https://www.producthunt.com/posts/shotapi)


给你的 AI Agent 一双眼睛。一行命令接入，零安装。

## 快速接入（远程模式 — 不需要安装）

```bash
# Claude Code
claude mcp add --transport streamable-http shotapi https://aiphotoshop.mynatapp.cc/mcp

# 或用 npx
npx -y @anthropic-ai/claude-code@latest --mcp https://aiphotoshop.mynatapp.cc/mcp
```

Claude Desktop / Cursor 配置：

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

## 3 个 MCP 工具

| 工具 | 说明 | 示例 |
|------|------|------|
| `screenshot_one_liner` | 一行截图，最简单 | `screenshot_one_liner(url="https://github.com")` |
| `screenshot` | 完整控制：视口、全页、CSS选择器、格式 | `screenshot(url="https://github.com", selector="#hero")` |
| `render` | 把 HTML/CSS 渲染成图片 — Agent写代码，立刻看效果 | `render(html="<h1>Hello</h1>")` |

`render` 工具闭合反馈回路：**写代码 → 渲染 → 看效果 → 修改 → 再渲染**。

## 为什么用 ShotAPI？

- **MCP原生** — 不需要写胶水代码。Agent在对话中直接调用工具。
- **零安装远程模式** — streamable-http，不需要装Python/Playwright/Chromium。
- **国内直连** — 不需要翻墙。微信/支付宝支付。
- **免费层** — 30截图+30渲染/月，IP限流，不需要注册。
- **渲染能力** — 不只是截已有网页。Agent写的HTML也能渲染成图片。
- **内置广告屏蔽** — 截图更干净。

## 马上试试（不需要注册）

```bash
curl -s "https://aiphotoshop.mynatapp.cc/v1/screenshot?url=https://github.com" -o shot.jpg
```

## 定价

| 方案 | 价格 | 额度 |
|------|------|------|
| 免费 | ¥0 | 30截图+30渲染/月（IP限流） |
| 标准版 | ¥29/月 | 5,000次/月 |
| 专业版 | ¥99/月 | 20,000次/月 |

免费层不需要API Key。付费：在[定价页](https://aiphotoshop.mynatapp.cc/pricing)获取Key。

## 本地模式（STDIO）

私有部署或付费用户可本地运行：

```bash
# 安装依赖
pip install -r requirements.txt
playwright install chromium

# 设置环境变量
export SHOTAPI_BASE_URL=https://aiphotoshop.mynatapp.cc
export SHOTAPI_KEY=你的Key  # 付费用户可选

# 接入 Claude Code
claude mcp add shotapi python mcp_stdio.py
```

## 链接

- **文档**: https://aiphotoshop.mynatapp.cc/docs
- **定价**: https://aiphotoshop.mynatapp.cc/pricing
- **健康检查**: https://aiphotoshop.mynatapp.cc/health
- **爱发电（付费）**: https://afdian.com/a/shotapi/plan