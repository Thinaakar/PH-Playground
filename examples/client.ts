/** Minimal TypeScript / Node client for MonstarX Philippines MCP (fetch). */

const BASE =
  process.env.PH_MCP_URL ?? "https://ph-mcp-staging.monstarxapp.com/mcp";

async function callTool(
  name: string,
  args: Record<string, unknown> = {},
): Promise<unknown> {
  const res = await fetch(BASE, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json, text/event-stream",
      "mcp-protocol-version": "2025-06-18",
      "User-Agent": "PH-Playground-Example/1.0",
    },
    body: JSON.stringify({
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: { name, arguments: args },
    }),
  });
  const { result } = (await res.json()) as {
    result: {
      isError?: boolean;
      content?: { text: string }[];
      structuredContent?: unknown;
    };
  };
  if (result.isError) throw new Error(result.content?.[0]?.text ?? "tool error");
  return result.structuredContent ?? JSON.parse(result.content?.[0]?.text ?? "{}");
}

const w = (await callTool("ph_weather_24h", { area_code: "manila" })) as {
  data?: { hourly?: { time?: string[] } };
};
console.log("Manila 24h hours:", w.data?.hourly?.time?.length ?? 0);

const g = (await callTool("ph_geocode", { query: "Intramuros Manila", limit: 2 })) as {
  results?: unknown[];
};
console.log("Geocode rows:", g.results?.length ?? 0);
