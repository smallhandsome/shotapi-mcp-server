#!/usr/bin/env python3
"""ShotAPI MCP Server — stdio transport for Claude Code / Claude Desktop / Cursor

Usage:
    # Add to Claude Code (free tier):
    claude mcp add shotapi python mcp_stdio.py

    # With paid tier API Key:
    claude mcp add shotapi -e SHOTAPI_KEY=shotapi_pro_xxx python mcp_stdio.py

    # Or use remote mode (no install):
    claude mcp add --transport streamable-http shotapi https://aiphotoshop.mynatapp.cc/mcp
"""

import asyncio
import atexit
import os
import argparse

# Parse --shotapi-key arg (Smithery passes config this way)
parser = argparse.ArgumentParser()
parser.add_argument("--shotapi-key", default="", help="ShotAPI API Key for paid tiers")
args, _ = parser.parse_known_args()

if args.shotapi_key and not os.getenv("SHOTAPI_KEY"):
    os.environ["SHOTAPI_KEY"] = args.shotapi_key

from mcp_server import mcp, close_client


def _cleanup():
    try:
        client_loop = asyncio.new_event_loop()
        client_loop.run_until_complete(close_client())
        client_loop.close()
    except Exception:
        pass


atexit.register(_cleanup)


async def main():
    try:
        await mcp.run_stdio_async()
    finally:
        await close_client()


if __name__ == "__main__":
    asyncio.run(main())