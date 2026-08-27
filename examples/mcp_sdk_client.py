"""Official MCP Python SDK client against MonstarX Philippines MCP."""
from __future__ import annotations

import asyncio
import os

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

BASE = os.environ.get("PH_MCP_URL", "https://ph-mcp-staging.monstarxapp.com/mcp")


async def main() -> None:
    async with streamablehttp_client(BASE) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print("tools:", len(tools.tools))
            result = await session.call_tool(
                "ph_public_holidays",
                arguments={"year": 2026},
            )
            print(result)


if __name__ == "__main__":
    asyncio.run(main())
