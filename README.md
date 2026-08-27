# MonstarX Philippines MCP — Playground

A self-contained **live playground and docs site** for the MonstarX Philippines MCP (`ph-mcp`) server: **68 `ph_*` tools** (weather, earthquakes, geocoding, holidays, shelters, tourism, FX, HDX catalog, and more).

Same design system as the Japan / India MCP playgrounds — Philippines tools and data only.

> 🔌 **MCP endpoint (staging):** `https://ph-mcp-staging.monstarxapp.com/mcp`  
> Local: `http://localhost:8789/mcp` (from `PH-MCP` + `npm run dev`)

---

## Run locally & deploy

```bash
npm start           # serves public/ on http://localhost:8080  (respects $PORT)
```

Live **Run** on this site posts to same-origin `/mcp`, which `server.js` proxies to local PH-MCP (`http://127.0.0.1:8789`, override with `MCP_URL`) and falls back to staging. Start the Worker with `npm run dev` in `../PH-MCP`. Direct browser calls to staging also work when that host is up (CORS is open on the Worker).

**Deploy to [Railway](https://railway.app):**

```bash
railway up --ci
```

**Regenerate the page** after editing tool metadata or `build/build.py`:

```bash
python build/gen_ph_data.py   # refresh schemas from the tool dump (optional)
python build/build.py         # rewrites public/index.html + philippines-mcp-playground.html
```

To point live **Run** at a different MCP, set `MCP_URL` for the proxy, or open the playground with `?mcp=http://localhost:8789`.

---

## Repository layout

```
├── public/index.html                  # playground (served)
├── philippines-mcp-playground.html    # standalone copy
├── server.js                          # static server + /health + /mcp proxy
├── package.json
├── railway.json
├── build/
│   ├── build.py                       # HTML generator
│   ├── data.min.json                  # 68 ph_* tools + example payloads
│   ├── gen_ph_data.py                 # rebuild data.min.json from tool dump
│   └── adapt_build_ph.py              # one-shot JP→PH adapter (already applied)
├── examples/                          # curl / Python / TS clients
└── README.md
```

---

## Quick start (MCP)

```bash
# List tools
curl -X POST https://ph-mcp-staging.monstarxapp.com/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-protocol-version: 2025-06-18" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'

# Manila 24h weather
curl -X POST https://ph-mcp-staging.monstarxapp.com/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-protocol-version: 2025-06-18" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"ph_weather_24h","arguments":{"area_code":"manila"}}}'
```

---

## Connect from MCP clients

### Claude Code

```bash
claude mcp add --transport http ph-mcp https://ph-mcp-staging.monstarxapp.com/mcp
```

### Cursor / native HTTP

```jsonc
{
  "mcpServers": {
    "philippines": {
      "type": "http",
      "url": "https://ph-mcp-staging.monstarxapp.com/mcp"
    }
  }
}
```

### Claude Desktop (`mcp-remote`)

```jsonc
{
  "mcpServers": {
    "philippines": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://ph-mcp-staging.monstarxapp.com/mcp"]
    }
  }
}
```

---

## Tools (68)

Grouped in the playground sidebar: weather, hazards, geo, PSGC admin, civic, places, transport, finance, news, nature, catalog.

Full parameter docs and example responses are in the playground (**Tools** section) and in `build/data.min.json`.

---

## Data sources

| Source | Used by |
|---|---|
| [Open-Meteo](https://open-meteo.com/) | Weather, UV, rain, AQI, marine, elevation |
| [USGS](https://earthquake.usgs.gov/) | Earthquakes in the PH bounding box |
| [OpenStreetMap](https://www.openstreetmap.org/) | Places, shelters, hospitals, transit POIs |
| [HDX](https://data.humdata.org/) | Philippines open catalog |
| [PSA OpenSTAT](https://psa.gov.ph/) | Statistical tables |
| Nager.Date / Zippopotam.us | Holidays, postal codes |

No API keys required for these free sources. MonstarX is an independent wrapper and is not endorsed by any government agency.

---

## Response format

Successful tool calls return:

- `content[0].text` — JSON string  
- `structuredContent` — same payload as object (prefer this)

Envelope fields typically include `source`, `agency`, `api`, `retrieved_at`, and often `license` / `auth`.

---

*Server: MonstarX Philippines MCP v0.1.0 · Protocol `2025-06-18` · [staging](https://ph-mcp-staging.monstarxapp.com/)*
