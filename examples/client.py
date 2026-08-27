"""Minimal Python client for MonstarX Philippines MCP (stdlib only)."""
from __future__ import annotations

import json
import os
import urllib.request

BASE = os.environ.get("PH_MCP_URL", "https://ph-mcp-staging.monstarxapp.com/mcp")


def call_tool(name: str, arguments: dict | None = None):
    body = json.dumps(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": name, "arguments": arguments or {}},
        }
    ).encode()
    req = urllib.request.Request(
        BASE,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "mcp-protocol-version": "2025-06-18",
            "User-Agent": "PH-Playground-Example/1.0",
        },
    )
    with urllib.request.urlopen(req) as r:
        result = json.load(r)["result"]
    if result.get("isError"):
        raise RuntimeError(result["content"][0]["text"])
    return result.get("structuredContent") or json.loads(result["content"][0]["text"])


if __name__ == "__main__":
    wx = call_tool("ph_weather_24h", {"area_code": "manila"})
    print("Manila 24h hours:", len((wx.get("data") or {}).get("hourly", {}).get("time") or []))

    geo = call_tool("ph_geocode", {"query": "Intramuros Manila", "limit": 2})
    print("Geocode results:", geo.get("shown") or geo.get("found"), geo.get("results") or geo.get("places"))

    holidays = call_tool("ph_public_holidays", {"year": 2026})
    print("Holidays 2026:", holidays.get("count") or holidays.get("total"))
