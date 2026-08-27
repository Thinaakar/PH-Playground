// Minimal, dependency-free static server for the MonstarX Philippines MCP playground.
// Serves ./public, respects Railway's $PORT, exposes /health, and proxies POST /mcp
// to local PH-MCP (or MCP_URL) with a staging fallback so live Run is same-origin.
const http = require("http");
const fs = require("fs");
const path = require("path");

const PORT = process.env.PORT || 8080;
const ROOT = path.join(__dirname, "public");
const MCP_PRIMARY = (process.env.MCP_URL || "http://127.0.0.1:8789").replace(/\/$/, "");
const MCP_FALLBACK = (process.env.MCP_FALLBACK || "https://ph-mcp-staging.monstarxapp.com").replace(/\/$/, "");
const MCP_TIMEOUT_MS = Number(process.env.MCP_TIMEOUT_MS) || 60000;

const TYPES = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "application/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".ico": "image/x-icon",
  ".txt": "text/plain; charset=utf-8",
};

function collectBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    req.on("data", (c) => chunks.push(c));
    req.on("end", () => resolve(Buffer.concat(chunks)));
    req.on("error", reject);
  });
}

function isLocal(origin) {
  return /localhost|127\.0\.0\.1/i.test(origin);
}

function errInfo(err) {
  return {
    error: err.cause?.code || err.code || err.name,
    message: err.message,
  };
}

async function originAlive(origin, ms = 2000) {
  try {
    const res = await fetch(origin + "/health", { signal: AbortSignal.timeout(ms) });
    return res.ok;
  } catch {
    return false;
  }
}

async function proxyMcp(req, res) {
  if (req.method === "OPTIONS") {
    res.writeHead(204, {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET,POST,DELETE,OPTIONS",
      "Access-Control-Allow-Headers":
        "Content-Type,mcp-session-id,Last-Event-ID,mcp-protocol-version,Authorization",
    });
    return res.end();
  }

  const body = req.method === "GET" || req.method === "HEAD" ? undefined : await collectBody(req);
  const primaryUp = await originAlive(MCP_PRIMARY);
  const origins = primaryUp
    ? [MCP_PRIMARY]
    : [...new Set([MCP_PRIMARY, MCP_FALLBACK])];
  const errors = [];

  for (const origin of origins) {
    const timeoutMs = isLocal(origin) ? MCP_TIMEOUT_MS : Math.min(MCP_TIMEOUT_MS, 20000);
    try {
      const headers = {
        "Content-Type": req.headers["content-type"] || "application/json",
        Accept: "application/json, text/event-stream",
        "mcp-protocol-version": req.headers["mcp-protocol-version"] || "2025-06-18",
      };
      const upstream = await fetch(origin + "/mcp", {
        method: req.method,
        headers,
        body: body && body.length ? body : undefined,
        signal: AbortSignal.timeout(timeoutMs),
      });
      const buf = Buffer.from(await upstream.arrayBuffer());
      const out = {
        "Content-Type": upstream.headers.get("content-type") || "application/json",
      };
      const session = upstream.headers.get("mcp-session-id");
      if (session) out["mcp-session-id"] = session;
      res.writeHead(upstream.status, out);
      return res.end(buf);
    } catch (err) {
      errors.push({ origin, ...errInfo(err) });
    }
  }

  res.writeHead(502, { "Content-Type": "application/json" });
  res.end(
    JSON.stringify({
      error: "MCP upstream unreachable",
      tried: errors,
      hint: primaryUp
        ? "Local PH-MCP is up but the tool call timed out. Retry, or check wrangler in ../PH-MCP."
        : "Start local PH-MCP (`npm run dev` in ../PH-MCP on :8789). Staging is currently down.",
    }),
  );
}

const server = http.createServer((req, res) => {
  const url = decodeURIComponent((req.url || "/").split("?")[0]);

  if (url === "/mcp") {
    return proxyMcp(req, res).catch((err) => {
      if (!res.headersSent) {
        res.writeHead(500, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ error: String(err) }));
      }
    });
  }

  if (url === "/health") {
    res.writeHead(200, { "Content-Type": "application/json" });
    return res.end(JSON.stringify({ status: "ok", service: "ph-mcp-playground" }));
  }

  let rel = url === "/" ? "/index.html" : url === "/favicon.ico" ? "/favicon.svg" : url;
  let filePath = path.normalize(path.join(ROOT, rel));
  if (!filePath.startsWith(ROOT)) {
    res.writeHead(403);
    return res.end("Forbidden");
  }

  fs.readFile(filePath, (err, data) => {
    if (err) {
      return fs.readFile(path.join(ROOT, "index.html"), (e2, home) => {
        if (e2) {
          res.writeHead(404);
          return res.end("Not found");
        }
        res.writeHead(200, { "Content-Type": TYPES[".html"] });
        res.end(home);
      });
    }
    const ext = path.extname(filePath).toLowerCase();
    res.writeHead(200, {
      "Content-Type": TYPES[ext] || "application/octet-stream",
      "Cache-Control": ext === ".html" ? "no-cache" : "public, max-age=3600",
    });
    res.end(data);
  });
});

server.listen(PORT, () => {
  console.log(`ph-mcp-playground listening on ${PORT} (MCP proxy → ${MCP_PRIMARY}, timeout ${MCP_TIMEOUT_MS}ms)`);
});
