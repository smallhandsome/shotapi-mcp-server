# ShotAPI — AI Agent 网页截图与渲染 MCP Server

给你的 AI Agent 一双眼睛。一行命令接入，零安装。

[![GitHub stars](https://img.shields.io/github/stars/smallhandsome/shotapi-mcp-server)](https://github.com/smallhandsome/shotapi-mcp-server)
[![MCP Registry](https://img.shields.io/badge/MCP-Registry-blue)](https://registry.modelcontextprotocol.io/servers/io.github.smallhandsome/shotapi-mcp-server)

[English](README.md)

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

## 真实使用场景

### 1. Claude 验证自己写的代码

```
你: 写一个着陆页，包含hero区、testimonial、价格网格。

Claude: [写HTML/CSS代码]

Claude: 用render工具检查一下效果...

[Claude调用ShotAPI render工具渲染刚写的HTML]

Claude: 价格网格在手机上重叠了，修复响应式断点...
```

### 2. 部署验证

```
你: 刚部署了，看看页面是否正常。

Claude: [调用ShotAPI截图 https://yourapp.com]

Claude: 页脚文字被截断 — CSS溢出问题。背景图片404。
```

### 3. CI/CD 中的UI回归测试

```bash
# 对比部署前后截图
curl -s "https://aiphotoshop.mynatapp.cc/v1/screenshot?url=https://staging.myapp.com" -o before.png
curl -s "https://aiphotoshop.mynatapp.cc/v1/screenshot?url=https://staging.myapp.com" -o after.png
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
- **国内直连** — 不需要翻墙。
- **免费层** — 10截图+10渲染/月，IP限流，不需要注册，不需要API Key。
- **渲染能力** — 不只是截已有网页。Agent写的HTML也能渲染成图片。
- **内置广告屏蔽** — 截图更干净。
- **MCP Registry收录** — Anthropic官方MCP服务器目录。

## 马上试试（不需要注册）

```bash
curl -s "https://aiphotoshop.mynatapp.cc/v1/screenshot?url=https://github.com" -o shot.jpg
```

## 定价

| 方案 | 价格 | 额度 |
|------|------|------|
| 免费 | ¥0 | 10截图+10渲染/月（IP限流，无需注册） |
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
- **MCP Registry**: https://registry.modelcontextprotocol.io/servers/io.github.smallhandsome/shotapi-mcp-server
- **爱发电（付费）**: https://afdian.com/a/shotapi/plan
- **Dev.to文章**: https://dev.to/smallhandsome/give-your-ai-agent-eyes-building-a-visual-mcp-server-for-web-screenshots-3f49