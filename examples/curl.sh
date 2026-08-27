#!/usr/bin/env bash
# Minimal curl examples against MonstarX Philippines MCP
set -euo pipefail

BASE="${PH_MCP_URL:-https://ph-mcp-staging.monstarxapp.com/mcp}"

hdr() {
  echo "--- $1 ---"
}

hdr "tools/list"
curl -sS -X POST "$BASE" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-protocol-version: 2025-06-18" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | head -c 500
echo

hdr "ph_weather_24h (Manila)"
curl -sS -X POST "$BASE" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-protocol-version: 2025-06-18" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"ph_weather_24h","arguments":{"area_code":"manila"}}}' | head -c 800
echo

hdr "ph_geocode (Intramuros)"
curl -sS -X POST "$BASE" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-protocol-version: 2025-06-18" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"ph_geocode","arguments":{"query":"Intramuros Manila","limit":2}}}' | head -c 800
echo
