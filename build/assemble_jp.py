#!/usr/bin/env python3
"""Assemble Japan MCP playground build.py from the SG shell + Japan content."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
SG = Path(r"d:\Projects\MCP\sg-mcp-playground-main\sg-mcp-playground-main\build\build.py")
src = SG.read_text(encoding="utf-8")

# Extract STYLE triple-quoted string
m = re.search(r'STYLE = r"""(.*?)"""', src, re.S)
if not m:
    raise SystemExit("STYLE not found")
STYLE = m.group(1)

# Update category CSS dots for Japan
STYLE = re.sub(
    r"--dot-catalog:#64748b;--dot-weather:#16a34a;--dot-carpark:#f59e0b;--dot-transport:#2563eb;\s*"
    r"--dot-geo:#0891b2;--dot-property:#7c3aed;--dot-company:#ea580c;--dot-education:#db2777;--dot-health:#dc2626;",
    "--dot-catalog:#64748b;--dot-weather:#16a34a;--dot-hazards:#dc2626;--dot-geo:#0891b2;"
    "--dot-civic:#7c3aed;--dot-places:#db2777;--dot-finance:#ea580c;",
    STYLE,
)

# Inject language-toggle CSS *inside* the <style> block (not after </style>)
LANG_CSS = """
.lang-wrap{position:relative;flex:none}
.lang-btn{display:inline-flex;align-items:center;gap:6px;height:34px;padding:0 10px;border-radius:8px;border:1px solid var(--border);
  background:var(--panel);color:var(--muted);font-size:12.5px;font-weight:600;cursor:pointer;font-family:var(--sans)}
.lang-btn:hover{color:var(--text);border-color:var(--border-2)}
.lang-btn .chev{opacity:.7;font-size:10px}
.lang-menu{position:absolute;right:0;top:calc(100% + 6px);min-width:160px;background:var(--panel);border:1px solid var(--border-2);
  border-radius:10px;box-shadow:var(--shadow);padding:4px;z-index:60;display:none}
.lang-menu.open{display:block}
.lang-menu button{display:flex;align-items:center;gap:8px;width:100%;text-align:left;border:none;background:none;
  padding:8px 10px;border-radius:7px;font-size:13px;color:var(--muted);cursor:pointer;font-family:var(--sans)}
.lang-menu button:hover,.lang-menu button.active{background:var(--accent-weak);color:var(--accent-ink);font-weight:600}
"""
if "</style>" not in STYLE:
    raise SystemExit("STYLE missing </style>")

# Scroll model: no outer window scrollbar; only sidebar + content/playground scroll
SCROLL_CSS = """
/* App shell fills the viewport — no document (browser) scrollbar */
html,body{height:100%;overflow:hidden}
.layout{height:calc(100vh - 57px);min-height:0;overflow:hidden;align-items:stretch}
/* Sidebar: own scroll */
.sidebar{position:relative;top:auto;height:100%;max-height:none;overflow-x:hidden;overflow-y:auto;overscroll-behavior:contain}
/* Main column: full free width after the sidebar */
.content{
  height:100%;max-height:100%;min-width:0;
  overflow-x:hidden;overflow-y:auto;overscroll-behavior:contain;
  width:100%;max-width:none;box-sizing:border-box;
  padding:0 clamp(24px,3.5vw,56px) 120px
}

/* —— Hero: full width, everything left-aligned (tag + CTAs included) —— */
.hero{
  width:100%;
  max-width:none;
  text-align:left;
  margin-left:0;margin-right:0
}
/* Brand tag: shrink-wrap on the left (not full-width centered) */
.hero .eyebrow{
  display:inline-flex !important;
  align-items:center;
  width:auto !important;
  max-width:100%;
  justify-content:flex-start !important;
  margin:0 !important
}
.hero h1{
  max-width:none !important;
  width:100%;
  margin-left:0 !important;
  margin-right:0 !important;
  text-align:left;
  text-wrap:pretty
}
.lede{
  max-width:none !important;
  width:100%;
  margin-left:0 !important;
  margin-right:0 !important;
  text-align:left
}
/* CTA buttons row: left, not center */
.hero .cta,.cta{
  display:flex !important;
  flex-wrap:wrap;
  gap:12px;
  justify-content:flex-start !important;
  align-items:center;
  width:100%;
  margin-left:0 !important;
  margin-right:0 !important
}
.stats{
  display:flex;
  width:100%;
  max-width:none !important;
  margin-left:0 !important;
  margin-right:0 !important;
  box-sizing:border-box;
  text-align:left
}
.stat{flex:1 1 0;min-width:0}

/* —— Use cases: balanced 3×2 grid (not 5+1 orphan) —— */
.uses{
  display:grid;
  grid-template-columns:repeat(3,minmax(0,1fr));
  gap:14px;
  margin:26px 0;
  width:100%
}
.use{min-width:0}

/* —— Footer: three columns span full content width —— */
footer{
  width:100%;max-width:none;box-sizing:border-box;
  padding:40px 0 24px;
  margin:48px 0 0
}
footer .cols{
  display:grid;
  grid-template-columns:repeat(3,minmax(0,1fr));
  gap:28px 40px;
  width:100%
}
footer .cols>div{min-width:0}
.disc{max-width:none;width:100%}
.sec-blurb,.tdesc{max-width:min(72ch,100%)}

/* Playground: don't stretch form to tool-list height */
.pg-body{align-items:start}
.pg-list{
  max-height:min(560px,calc(100vh - 240px));
  overflow-x:hidden;overflow-y:auto;overscroll-behavior:contain;
  align-self:start;width:100%
}
.pg-main{
  min-width:0;align-self:start;
  max-height:min(560px,calc(100vh - 240px));
  overflow-x:hidden;overflow-y:auto;overscroll-behavior:contain
}
/* Result blocks inside playground stay scrollable */
.wxgrid{max-height:360px;overflow:auto;overscroll-behavior:contain}
.vtwrap{max-height:430px;overflow:auto;overscroll-behavior:contain}
.cpgrid{max-height:430px;overflow:auto;overscroll-behavior:contain}
.ilist,.dlist{max-height:340px;overflow:auto;overscroll-behavior:contain}
.vlist{max-height:210px;overflow:auto;overscroll-behavior:contain}
.code.scroll pre{max-height:420px;overflow:auto;overscroll-behavior:contain}
/* Default OS scrollbars */
*{scrollbar-width:auto;scrollbar-color:auto}
*::-webkit-scrollbar{width:initial;height:initial}
*::-webkit-scrollbar-track{background:transparent}
*::-webkit-scrollbar-thumb{background:initial;border-radius:0;border:none;box-shadow:none}

/* ========== Responsive ========== */
html{overflow-x:hidden}
body{overflow-x:hidden}

@media (max-width:1100px){
  .uses{grid-template-columns:repeat(2,minmax(0,1fr))}
  footer .cols{grid-template-columns:repeat(2,minmax(0,1fr))}
}

/* Tablet / narrow desktop */
@media (max-width:900px){
  html,body{height:auto!important;min-height:100%;overflow-x:hidden;overflow-y:auto}
  .layout{
    grid-template-columns:1fr!important;
    height:auto!important;
    min-height:0;
    overflow:visible!important
  }
  .content{
    height:auto!important;
    max-height:none!important;
    overflow:visible!important;
    max-width:none;
    width:100%;
    padding:0 18px 80px;
    box-sizing:border-box
  }
  /* Drawer sidebar */
  .sidebar{
    position:fixed!important;
    top:57px;left:0;
    width:min(300px,86vw);
    height:calc(100vh - 57px)!important;
    max-height:none;
    z-index:46;
    transform:translateX(-105%);
    transition:transform .22s ease;
    box-shadow:var(--shadow);
    overflow-y:auto!important;
    overscroll-behavior:contain;
    background:var(--bg-sub)
  }
  .sidebar.open{transform:none}
  .menu-btn{display:grid!important}
  .endpoint-pill,.tb-nav{display:none!important}
  .scrim.open{display:block}
  .topbar{padding:0 12px;gap:10px}
  .brand{font-size:15px;gap:8px;min-width:0}
  .brand small{display:none} /* keep topbar uncluttered */
  .brand .sep{display:none}
  .lang-btn{padding:0 8px;font-size:12px}
  #langBtnLabel{max-width:5em;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}

  /* Hero */
  .hero{padding:32px 0 28px}
  .hero h1{font-size:clamp(28px,8.5vw,42px)!important;line-height:1.08}
  .lede{font-size:16px!important;line-height:1.55;margin-top:16px!important}
  .cta{gap:10px;margin-top:22px}
  .btn{width:100%;justify-content:center;padding:12px 16px;font-size:14px}
  .cta .btn{width:auto;min-width:0;flex:1 1 auto}
  .stats{flex-wrap:wrap;margin-top:28px}
  .stat{
    flex:1 1 45%;
    min-width:140px;
    border-right:1px solid var(--border);
    border-bottom:1px solid var(--border);
    padding:14px 16px
  }
  .stat:nth-child(2n){border-right:none}
  .stat:nth-last-child(-n+2){border-bottom:none}
  .stat .n{font-size:22px}

  /* Sections */
  h2{font-size:22px;margin:44px 0 6px}
  .sec-blurb{font-size:14.5px;margin-bottom:16px}
  .grid2{grid-template-columns:1fr!important}

  /* Playground */
  .pg{border-radius:14px}
  .pg-top{padding:12px 14px}
  .pg-body{grid-template-columns:1fr!important;align-items:stretch}
  .pg-list{
    max-height:min(220px,40vh)!important;
    overflow-y:auto!important;
    border-right:none!important;
    border-bottom:1px solid var(--border);
    display:block!important;
    width:100%;
    box-sizing:border-box
  }
  .pg-main{
    max-height:none!important;
    overflow:visible!important;
    padding:16px!important;
    width:100%;
    box-sizing:border-box
  }
  .field{grid-template-columns:1fr!important;gap:6px}
  .field label{padding-top:0!important}
  .runbar{flex-direction:column;align-items:stretch}
  .run{width:100%;justify-content:center}
  .runbar .linkbtn{align-self:flex-start}

  /* Tool cards */
  .tool .head,.tool .body{padding-left:14px;padding-right:14px}
  .tryit{margin-left:0;width:100%;justify-content:center}
  .tool .tname{gap:8px}
  .ptable{display:block;overflow-x:auto;-webkit-overflow-scrolling:touch}
  .ptable th,.ptable td{white-space:normal}
  .ptable td.pn{white-space:nowrap}

  footer{padding:28px 0 16px;margin-top:36px}
  footer .cols{grid-template-columns:1fr!important;gap:22px}
  .disc{font-size:12px;line-height:1.55}

  /* Forms/code don’t overflow */
  .code pre{font-size:12px;padding:12px}
  .card{padding:14px 16px}
  section{scroll-margin-top:68px}
}

/* Phone */
@media (max-width:640px){
  .content{padding:0 14px 72px}
  .hero{padding:24px 0 22px}
  .hero h1{font-size:clamp(26px,9vw,34px)!important}
  .lede{font-size:15px!important}
  .eyebrow{font-size:11px;letter-spacing:.04em;flex-wrap:wrap}
  .cta{flex-direction:column;align-items:stretch}
  .cta .btn{width:100%;flex:none}
  .uses{grid-template-columns:1fr!important;gap:12px}
  .use{padding:16px}
  .stats{border-radius:12px}
  .stat{
    flex:1 1 100%!important;
    min-width:0;
    border-right:none!important;
    border-bottom:1px solid var(--border)
  }
  .stat:last-child{border-bottom:none!important}
  .stat .n{font-size:20px}
  h2{font-size:20px;margin-top:36px}
  h2 .num{display:block;margin:0 0 4px;font-size:13px}
  .pg-list{max-height:180px!important}
  .pg-main .tn code{font-size:14px;word-break:break-all}
  .pg-main .td{font-size:13px}
  .resp-meta{gap:6px}
  .tabs{width:100%;overflow-x:auto}
  .wxgrid{grid-template-columns:repeat(auto-fill,minmax(72px,1fr))!important}
  .topbar{height:52px}
  .sidebar{top:52px;height:calc(100vh - 52px)!important}
  .icon-btn{width:36px;height:36px} /* better touch target */
  .lang-btn{height:36px}
  .brand b{font-size:15px}
  footer .top{font-size:15px;flex-wrap:wrap}
}

/* Very small phones */
@media (max-width:380px){
  .content{padding:0 12px 64px}
  .hero h1{font-size:24px!important}
  .btn{font-size:13px;padding:11px 12px}
  .endpoint-pill{display:none!important}
}

/* Prefer reduced motion (mobile drawer) */
@media (prefers-reduced-motion:reduce){
  .sidebar{transition:none}
}

/* Notched phones */
@supports (padding:max(0px)){
  .topbar{
    padding-left:max(12px,env(safe-area-inset-left));
    padding-right:max(12px,env(safe-area-inset-right))
  }
  @media (max-width:900px){
    .content{padding-bottom:max(80px,calc(64px + env(safe-area-inset-bottom)))}
    .sidebar{padding-bottom:max(24px,env(safe-area-inset-bottom))}
  }
}
"""
STYLE = STYLE.replace("</style>", LANG_CSS + SCROLL_CSS + "</style>", 1)

LOGO = (
    '<svg class="mx" viewBox="0 0 30 30" fill="currentColor" xmlns="http://www.w3.org/2000/svg">'
    '<path fill-rule="evenodd" clip-rule="evenodd" d="M29.3493 25.3568L20.5472 16.5546L16.5546 20.5472L25.3568 29.3493L29.3493 25.3568ZM8.76813 12.7607L12.7607 8.76813L3.99257 0L0 3.99257L8.76813 12.7607ZM9.03679e-07 25.3568L8.8024 16.5543L12.795 20.5469L3.99257 29.3493L9.03679e-07 25.3568ZM20.5814 12.7605L16.5889 8.7679L25.3568 0L29.3493 3.99257L20.5814 12.7605Z"/></svg>'
)

BODYTOP = r'''
<div class="topbar">
  <button class="icon-btn menu-btn" id="menuBtn" aria-label="Menu"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button>
  <a class="brand" href="#top"><span class="logo">''' + LOGO + r'''</span><b>MonstarX</b><span class="sep">·</span><small>Japan&nbsp;MCP</small></a>
  <nav class="tb-nav">
    <a href="#playground" data-i18n="navPlayground">Playground</a>
    <a href="#reference" data-i18n="navTools">Tools</a>
    <a href="#quickstart" data-i18n="navConnect">Connect</a>
  </nav>
  <div class="tb-spacer"></div>
  <div class="endpoint-pill" id="epPill" title="Copy MCP endpoint">
    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
    <span class="u">jp-mcp-staging.monstarxapp.com/mcp</span>
  </div>
  <button class="icon-btn" id="themeBtn" aria-label="Toggle theme"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.8A9 9 0 1 1 11.2 3 7 7 0 0 0 21 12.8z"/></svg></button>
  <div class="lang-wrap">
    <button type="button" class="lang-btn" id="langBtn" aria-haspopup="listbox" aria-expanded="false" title="Language">
      <span aria-hidden="true">🌐</span><span id="langBtnLabel">EN</span><span class="chev">▾</span>
    </button>
    <div class="lang-menu" id="langMenu" role="listbox">
      <button type="button" data-lang="en" role="option">🇺🇸 English</button>
      <button type="button" data-lang="ja" role="option">🇯🇵 日本語</button>
    </div>
  </div>
</div>
<div class="layout" id="top">
  <div class="scrim" id="scrim"></div>
  <aside class="sidebar" id="sidebar">
    <div class="search"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>
      <input id="filter" type="text" data-i18n-placeholder="filterTools" placeholder="Filter 27 tools…" autocomplete="off" spellcheck="false"></div>
    <div class="nav-quick" style="margin-bottom:6px">
      <a href="#playground" class="spot" data-i18n="navLivePg">▶ Live playground</a>
      <a href="#usecases" data-i18n="navUseCases">What you can build</a>
      <a href="#quickstart" data-i18n="navConnectAgent">Connect your agent</a>
      <a href="#response" data-i18n="navResponse">Response format</a>
      <a href="#errors" data-i18n="navErrors">Errors</a>
    </div>
    <div id="nav"></div>
  </aside>
  <main class="content">
    <section class="hero" id="overview">
      <span class="eyebrow"><span class="logo">''' + LOGO + r'''</span> <span data-i18n="eyebrow">MonstarX · Japan MCP</span></span>
      <h1 data-i18n-html="heroTitle">Japan's public data, <span class="hl">ready for your AI</span>.</h1>
      <p class="lede" data-i18n-html="heroLede">Weather, earthquakes, geocoding, postal codes, holidays, evacuation shelters, tourism spots, Bank of Japan series, open datasets — Japan's free public APIs live across many agencies, each with its own formats and quirks. <b>MonstarX unifies them into 27 tools any AI agent can call</b>, through one endpoint, with no API keys. Stop writing integration glue. Start shipping Japan-smart products.</p>
      <div class="cta">
        <a class="btn primary" href="#playground" data-i18n="ctaTry">▶ Try it live in your browser</a>
        <a class="btn ghost" href="#quickstart" data-i18n="ctaConnect">Connect Claude or Cursor</a>
      </div>
      <div class="stats">
        <div class="stat"><div class="n">27</div><div class="l" data-i18n="statTools">ready-made tools</div></div>
        <div class="stat"><div class="n">9</div><div class="l" data-i18n="statSources">free public sources</div></div>
        <div class="stat"><div class="n">0</div><div class="l" data-i18n="statKeys">API keys or signup</div></div>
        <div class="stat"><div class="n" data-i18n="statLiveN">Live</div><div class="l" data-i18n="statLive">real-time data</div></div>
      </div>
    </section>

    <section id="playground">
      <h2><span class="num">▶</span><span data-i18n="secPlayground">Live playground</span></h2>
      <p class="sec-blurb" data-i18n-html="secPlaygroundBlurb">Pick a tool, tweak the inputs, hit <b>Run</b> — the query goes straight to the live MCP server and streams back real Japan data. No sign-up, nothing to install. Try a one-click example to start:</p>
      <div class="pg">
        <div class="pg-note" id="pgNote"></div>
        <div class="pg-top">
          <span class="lbl" data-i18n="tryLabel">Try</span>
          <button class="chip-ex" data-ex="wx24" data-i18n-chip="chipWx"><span class="e">⛅</span> Tokyo weather 24h</button>
          <button class="chip-ex" data-ex="quake" data-i18n-chip="chipQuake"><span class="e">🌋</span> Recent quakes</button>
          <button class="chip-ex" data-ex="geo" data-i18n-chip="chipGeo"><span class="e">📍</span> Geocode 東京駅</button>
          <button class="chip-ex" data-ex="postal" data-i18n-chip="chipPostal"><span class="e">✉️</span> Postal 100-0001</button>
          <button class="chip-ex" data-ex="holiday" data-i18n-chip="chipHoliday"><span class="e">🎌</span> Holidays 2026</button>
          <button class="chip-ex" data-ex="shelter" data-i18n-chip="chipShelter"><span class="e">🏫</span> Shelters · Chiyoda</button>
          <button class="chip-ex" data-ex="tourism" data-i18n-chip="chipTourism"><span class="e">🗾</span> Tourism near Tokyo St.</button>
          <button class="chip-ex" data-ex="datasets" data-i18n-chip="chipDatasets"><span class="e">📚</span> Search 天気 datasets</button>
        </div>
        <div class="pg-body">
          <div class="pg-list" id="pgList"></div>
          <div class="pg-main" id="pgMain"></div>
        </div>
      </div>
    </section>

    <section id="usecases">
      <h2><span class="num">01</span><span data-i18n="secUse">What you can build</span></h2>
      <p class="sec-blurb" data-i18n="secUseBlurb">A weekend hackathon or a production feature — these are all a few tool calls away.</p>
      <div class="uses">
        <div class="use"><div class="ico">⛅</div><h4 data-i18n="useWxT">Weather-aware apps</h4><p data-i18n="useWxP">Area codes, daily/weekly JMA text, 24h/4-day forecasts, UV, rain, and air quality for Tokyo or any prefecture office.</p><div class="tools"><code>jp_weather_24h</code><code>jp_weather_warnings</code><code>jp_uv_index</code></div></div>
        <div class="use"><div class="ico">🌋</div><h4 data-i18n="useDisT">Disaster awareness</h4><p data-i18n="useDisP">Surface recent earthquakes, tsunami advisories, and nearby designated evacuation shelters.</p><div class="tools"><code>jp_earthquake_list</code><code>jp_tsunami_list</code><code>jp_evacuation_shelters</code></div></div>
        <div class="use"><div class="ico">📍</div><h4 data-i18n="useMapT">Maps &amp; addressing</h4><p data-i18n="useMapP">Search places, geocode, reverse-geocode, resolve postal codes, and read GSI elevation — all without keys.</p><div class="tools"><code>jp_geocode</code><code>jp_postal_code</code><code>jp_elevation</code></div></div>
        <div class="use"><div class="ico">🗾</div><h4 data-i18n="useTourT">Travel &amp; tourism</h4><p data-i18n="useTourP">Find nearby attractions from OpenStreetMap and pair with weather or holiday calendars.</p><div class="tools"><code>jp_tourism_spots</code><code>jp_public_holidays</code></div></div>
        <div class="use"><div class="ico">📈</div><h4 data-i18n="useFinT">Macro / finance bots</h4><p data-i18n="useFinP">Pull Bank of Japan series such as overnight call rates into research or agent workflows.</p><div class="tools"><code>jp_boj_finance</code></div></div>
        <div class="use"><div class="ico">📚</div><h4 data-i18n="useDataT">Open data explorer</h4><p data-i18n="useDataP">Search DATA.GO.JP / e-Gov packages, inspect metadata, and query datastore tables.</p><div class="tools"><code>jp_datasets_search</code><code>jp_dataset_query</code></div></div>
      </div>
    </section>

    <section id="quickstart">
      <h2><span class="num">02</span><span data-i18n="secConnect">Connect your agent</span></h2>
      <p class="sec-blurb" data-i18n="secConnectBlurb">MonstarX Japan MCP is a remote HTTP server speaking the Model Context Protocol. Point any MCP-capable client at the endpoint — no auth handshake, it's stateless.</p>
      <div class="grid2">
        <div><div class="mini-label" data-i18n="labClaude">Claude Code</div>__CB_CC__</div>
        <div><div class="mini-label" data-i18n="labCursor">Cursor / native HTTP clients</div>__CB_CURSOR__</div>
      </div>
      <div class="mini-label" style="margin-top:18px" data-i18n-html="labDesk">Claude Desktop &mdash; <span style="text-transform:none;letter-spacing:0;font-weight:400;color:var(--faint)">claude_desktop_config.json</span></div>
      __CB_DESK__
      <div class="mini-label" style="margin-top:18px" data-i18n="labCurl">Or just cURL it</div>
      __CB_QS__
    </section>

    <section id="response">
      <h2><span class="num">03</span><span data-i18n="secResponse">Response format</span></h2>
      <p class="sec-blurb" data-i18n-html="secResponseBlurb">Every call returns the payload twice — as a JSON string in <code>content[0].text</code> and as a parsed object in <code>structuredContent</code> (prefer this). Each payload wraps the data in a consistent provenance envelope so your agent always knows the source, agency and freshness.</p>
      __CB_ENV__
      <div class="card" style="margin-top:16px"><table class="ptable" style="margin:0"><thead><tr><th data-i18n="thField">Field</th><th data-i18n="thMeaning">Meaning</th></tr></thead><tbody>
        <tr><td class="pn">source</td><td data-i18n="fSource">Upstream platform — JMA bosai, Open-Meteo, GSI, DATA.GO.JP, BOJ, zipcloud, etc.</td></tr>
        <tr><td class="pn">agency</td><td data-i18n="fAgency">Originating body — Japan Meteorological Agency, GSI, Digital Agency, Bank of Japan, …</td></tr>
        <tr><td class="pn">api</td><td data-i18n="fApi">The specific upstream API that was queried.</td></tr>
        <tr><td class="pn">license</td><td data-i18n="fLicense">Data licence / terms note when applicable.</td></tr>
        <tr><td class="pn">retrieved_at</td><td data-i18n="fRetrieved">Server fetch time (UTC). Live timestamps inside payloads are often JST (+09:00).</td></tr>
        <tr><td class="pn">data / results</td><td data-i18n-html="fData">The payload. List tools add context like <code>total</code>, <code>shown</code>, <code>found</code>.</td></tr>
      </tbody></table></div>
    </section>

    <section id="errors">
      <h2><span class="num">04</span><span data-i18n="secErrors">Errors</span></h2>
      <p class="sec-blurb" data-i18n-html="secErrorsBlurb">Errors come back as a normal result with <code>isError: true</code> and a message in <code>content[0].text</code> — not as a transport-level failure. Invalid or missing arguments return MCP error <code>-32602</code>. An empty list is a valid "no matches", not an error.</p>
      __CB_ERR__
    </section>

    <section id="reference">
      <h2><span class="num">05</span><span data-i18n="secTools">All 27 tools</span></h2>
      <p class="sec-blurb" data-i18n-html="secToolsBlurb">Every tool is prefixed <code>jp_</code>; required params are marked <span style="color:var(--accent)">*</span>. Hit <b>Try in playground</b> on any tool to load it above with a working example.</p>
      <div id="tools"></div>
    </section>

    <footer>
      <div class="top"><span class="logo">''' + LOGO + r'''</span> <b>MonstarX</b> <span style="color:var(--faint)">Japan MCP</span></div>
      <div class="cols">
        <div><h4 data-i18n="ftSources">Data sources</h4><div><a href="https://www.jma.go.jp/bosai/">JMA bosai</a> · weather, quakes, tsunami</div><div><a href="https://open-meteo.com/">Open-Meteo</a> · hourly / air quality</div><div><a href="https://www.gsi.go.jp/">GSI</a> · address, elevation</div><div><a href="https://www.e-gov.go.jp/">DATA.GO.JP / e-Gov</a> · open catalog</div><div><a href="https://www.boj.or.jp/">Bank of Japan</a> · time-series</div></div>
        <div><h4 data-i18n="ftEndpoints">Endpoints</h4><div style="font-family:var(--mono);font-size:12.5px">GET&nbsp; /</div><div style="font-family:var(--mono);font-size:12.5px">GET&nbsp; /health</div><div style="font-family:var(--mono);font-size:12.5px">POST /mcp</div></div>
        <div><h4 data-i18n="ftServer">Server</h4><div>MonstarX Japan MCP · v0.1.0</div><div>Protocol <code>2025-06-18</code> · <span class="tag">staging</span></div><div><a href="https://monstarx.com">monstarx.com</a></div></div>
      </div>
      <p class="disc" data-i18n="ftDisc">Data remains subject to each source's terms (JMA, GSI, Open-Meteo, DATA.GO.JP/e-Gov, BOJ, zipcloud, Nager.Date, OpenStreetMap ODbL). You are responsible for complying with the source licences. MonstarX is an independent wrapper and is not endorsed by any government agency. This is a staging deployment — don't build production load on it. Example payloads captured for documentation 2026-08-07.</p>
    </footer>
  </main>
</div>
'''

SCRIPT = r'''
<script id="apidata" type="application/json">__DATA__</script>
<script>
const DATA=JSON.parse(document.getElementById('apidata').textContent);
const EP='https://jp-mcp-staging.monstarxapp.com';
let LANG=localStorage.getItem('mx-lang-jp')||'en';

const I18N={
en:{
navPlayground:'Playground',navTools:'Tools',navConnect:'Connect',
navLivePg:'▶ Live playground',navUseCases:'What you can build',navConnectAgent:'Connect your agent',navResponse:'Response format',navErrors:'Errors',
filterTools:'Filter 27 tools…',eyebrow:'MonstarX · Japan MCP',
heroTitle:"Japan's public data, <span class=\"hl\">ready for your AI</span>.",
heroLede:"Weather, earthquakes, geocoding, postal codes, holidays, evacuation shelters, tourism spots, Bank of Japan series, open datasets — Japan's free public APIs live across many agencies, each with its own formats and quirks. <b>MonstarX unifies them into 27 tools any AI agent can call</b>, through one endpoint, with no API keys. Stop writing integration glue. Start shipping Japan-smart products.",
ctaTry:'▶ Try it live in your browser',ctaConnect:'Connect Claude or Cursor',
statTools:'ready-made tools',statSources:'free public sources',statKeys:'API keys or signup',statLiveN:'Live',statLive:'real-time data',
secPlayground:'Live playground',
secPlaygroundBlurb:'Pick a tool, tweak the inputs, hit <b>Run</b> — the query goes straight to the live MCP server and streams back real Japan data. No sign-up, nothing to install. Try a one-click example to start:',
tryLabel:'Try',
chipWx:'Tokyo weather 24h',chipQuake:'Recent quakes',chipGeo:'Geocode 東京駅',chipPostal:'Postal 100-0001',
chipHoliday:'Holidays 2026',chipShelter:'Shelters · Chiyoda',chipTourism:'Tourism near Tokyo St.',chipDatasets:'Search 天気 datasets',
secUse:'What you can build',secUseBlurb:'A weekend hackathon or a production feature — these are all a few tool calls away.',
useWxT:'Weather-aware apps',useWxP:'Area codes, daily/weekly JMA text, 24h/4-day forecasts, UV, rain, and air quality for Tokyo or any prefecture office.',
useDisT:'Disaster awareness',useDisP:'Surface recent earthquakes, tsunami advisories, and nearby designated evacuation shelters.',
useMapT:'Maps & addressing',useMapP:'Search places, geocode, reverse-geocode, resolve postal codes, and read GSI elevation — all without keys.',
useTourT:'Travel & tourism',useTourP:'Find nearby attractions from OpenStreetMap and pair with weather or holiday calendars.',
useFinT:'Macro / finance bots',useFinP:'Pull Bank of Japan series such as overnight call rates into research or agent workflows.',
useDataT:'Open data explorer',useDataP:'Search DATA.GO.JP / e-Gov packages, inspect metadata, and query datastore tables.',
secConnect:'Connect your agent',
secConnectBlurb:'MonstarX Japan MCP is a remote HTTP server speaking the Model Context Protocol. Point any MCP-capable client at the endpoint — no auth handshake, it\'s stateless.',
labClaude:'Claude Code',labCursor:'Cursor / native HTTP clients',
labDesk:'Claude Desktop — <span style="text-transform:none;letter-spacing:0;font-weight:400;color:var(--faint)">claude_desktop_config.json</span>',
labCurl:'Or just cURL it',
secResponse:'Response format',
secResponseBlurb:'Every call returns the payload twice — as a JSON string in <code>content[0].text</code> and as a parsed object in <code>structuredContent</code> (prefer this). Each payload wraps the data in a consistent provenance envelope so your agent always knows the source, agency and freshness.',
thField:'Field',thMeaning:'Meaning',
fSource:'Upstream platform — JMA bosai, Open-Meteo, GSI, DATA.GO.JP, BOJ, zipcloud, etc.',
fAgency:'Originating body — Japan Meteorological Agency, GSI, Digital Agency, Bank of Japan, …',
fApi:'The specific upstream API that was queried.',
fLicense:'Data licence / terms note when applicable.',
fRetrieved:'Server fetch time (UTC). Live timestamps inside payloads are often JST (+09:00).',
fData:'The payload. List tools add context like <code>total</code>, <code>shown</code>, <code>found</code>.',
secErrors:'Errors',
secErrorsBlurb:'Errors come back as a normal result with <code>isError: true</code> and a message in <code>content[0].text</code> — not as a transport-level failure. Invalid or missing arguments return MCP error <code>-32602</code>. An empty list is a valid "no matches", not an error.',
secTools:'All 27 tools',
secToolsBlurb:'Every tool is prefixed <code>jp_</code>; required params are marked <span style="color:var(--accent)">*</span>. Hit <b>Try in playground</b> on any tool to load it above with a working example.',
ftSources:'Data sources',ftEndpoints:'Endpoints',ftServer:'Server',
ftDisc:'Data remains subject to each source\'s terms (JMA, GSI, Open-Meteo, DATA.GO.JP/e-Gov, BOJ, zipcloud, Nager.Date, OpenStreetMap ODbL). You are responsible for complying with the source licences. MonstarX is an independent wrapper and is not endorsed by any government agency. This is a staging deployment — don\'t build production load on it. Example payloads captured for documentation 2026-08-07.',
cat_weather:'Weather & Environment',cat_hazards:'Earthquakes & Tsunami',cat_geo:'Geocoding & Addresses',cat_civic:'Civic & Safety',cat_places:'Tourism',cat_finance:'Finance (BOJ)',cat_catalog:'Open Data Catalog',
runQuery:'▶ Run query',running:'Running…',copyCurl:'Copy as cURL',copiedCurl:'Copied cURL',resetEx:'Reset to example',
noParams:'This tool takes no parameters — just run it.',sampleReqs:'Sample requests',tryPlay:'▶ Try in playground',
exCall:'Example call & response',exCallSub:'Example call',exRespSub:'Example response — trimmed',
noParamsBadge:'no params',tabVisual:'Visual',tabJson:'JSON',tabRaw:'Raw',
contacting:'contacting server…',hintCors:'Live calls need the MCP server reachable from your browser (CORS open). Use the staging URL or local monstarx-mcp-jp.',
previewNote:'<b>Preview mode.</b> Live queries are sandboxed — download this page and open it from your own host (or locally) to run against the server.',
paramRequired:'required',paramOptional:'optional'
},
ja:{
navPlayground:'プレイグラウンド',navTools:'ツール',navConnect:'接続',
navLivePg:'▶ ライブデモ',navUseCases:'できること',navConnectAgent:'エージェント接続',navResponse:'レスポンス形式',navErrors:'エラー',
filterTools:'27ツールを絞り込み…',eyebrow:'MonstarX · Japan MCP',
heroTitle:'日本の公開データ、<span class="hl">AIですぐ使える</span>。',
heroLede:'天気・地震・ジオコーディング・郵便番号・祝日・避難所・観光スポット・日銀系列・オープンデータ。日本の無料公開APIは機関ごとに形式が違います。<b>MonstarX は 27 のツールにまとめ、1つのエンドポイント・APIキー不要でAIエージェントから呼べます</b>。連携の糊を書くのをやめて、日本に強いプロダクトを届けましょう。',
ctaTry:'▶ ブラウザで試す',ctaConnect:'Claude / Cursor に接続',
statTools:'準備済みツール',statSources:'無料の公開ソース',statKeys:'APIキー・登録不要',statLiveN:'Live',statLive:'リアルタイムデータ',
secPlayground:'ライブプレイグラウンド',
secPlaygroundBlurb:'ツールを選び、入力を調整して <b>実行</b> — クエリはライブ MCP サーバーへ飛び、実際の日本データが返ります。サインアップ不要。ワンクリック例からどうぞ:',
tryLabel:'試す',
chipWx:'東京の24時間天気',chipQuake:'直近の地震',chipGeo:'東京駅をジオコード',chipPostal:'郵便番号 100-0001',
chipHoliday:'2026年の祝日',chipShelter:'避難所 · 千代田',chipTourism:'東京駅付近の観光',chipDatasets:'天気データセット検索',
secUse:'できること',secUseBlurb:'週末ハッカソンでも本番機能でも — 数回のツール呼び出しで届きます。',
useWxT:'天気対応アプリ',useWxP:'エリアコード、JMA 概況、24時間/4日予報、UV・雨・気温・空気質。',
useDisT:'防災・意識',useDisP:'直近の地震・津波情報と指定避難所を表示。',
useMapT:'地図と住所',useMapP:'場所検索・ジオコード・逆ジオコード・郵便番号・標高 — キー不要。',
useTourT:'旅行・観光',useTourP:'OpenStreetMap の観光スポットと祝日を組み合わせ。',
useFinT:'マクロ/金融ボット',useFinP:'無担保コールレートなど日銀時系列をエージェントへ。',
useDataT:'オープンデータ探索',useDataP:'DATA.GO.JP / e-Gov の検索・メタデータ・データストア照会。',
secConnect:'エージェント接続',
secConnectBlurb:'MonstarX Japan MCP は Model Context Protocol のリモート HTTP サーバーです。MCP 対応クライアントをエンドポイントに向けるだけ — 認証ハンドシェイク不要でステートレスです。',
labClaude:'Claude Code',labCursor:'Cursor / ネイティブ HTTP',
labDesk:'Claude Desktop — <span style="text-transform:none;letter-spacing:0;font-weight:400;color:var(--faint)">claude_desktop_config.json</span>',
labCurl:'または cURL',
secResponse:'レスポンス形式',
secResponseBlurb:'呼び出し結果は JSON 文字列の <code>content[0].text</code> とオブジェクトの <code>structuredContent</code>（推奨）の両方で返ります。出典・機関・取得時刻つきの封筒でラップされます。',
thField:'フィールド',thMeaning:'意味',
fSource:'上流 — JMA bosai、Open-Meteo、GSI、DATA.GO.JP、BOJ、zipcloud など',
fAgency:'元機関 — 気象庁、国土地理院、デジタル庁、日本銀行 など',
fApi:'実際に問い合わせた上流 API',
fLicense:'ライセンス / 利用条件（該当時）',
fRetrieved:'サーバー取得時刻 (UTC)。ペイロード内は多くの場合 JST (+09:00)',
fData:'本体。一覧ツールは <code>total</code> / <code>shown</code> / <code>found</code> などを付与',
secErrors:'エラー',
secErrorsBlurb:'エラーは <code>isError: true</code> の通常結果と <code>content[0].text</code> のメッセージ。不正引数は MCP <code>-32602</code>。空リストは「一致なし」でエラーではありません。',
secTools:'全 27 ツール',
secToolsBlurb:'すべて <code>jp_</code> 接頭辞。必須パラメータは <span style="color:var(--accent)">*</span>。各ツールの <b>プレイグラウンドで試す</b> で上のデモに読み込めます。',
ftSources:'データソース',ftEndpoints:'エンドポイント',ftServer:'サーバー',
ftDisc:'データは各ソースの利用条件に従います（JMA、GSI、Open-Meteo、DATA.GO.JP/e-Gov、BOJ、zipcloud、Nager.Date、OpenStreetMap ODbL）。配布・利用時はソースのライセンス遵守は利用者の責任です。MonstarX は独立したラッパーであり、政府機関の公式製品ではありません。ステージング環境のため本番負荷には使わないでください。ドキュメント用サンプルは 2026-08-07 時点。',
cat_weather:'天気・環境',cat_hazards:'地震・津波',cat_geo:'ジオコーディング・住所',cat_civic:'防災・行政',cat_places:'観光',cat_finance:'金融（日銀）',cat_catalog:'オープンデータ',
runQuery:'▶ 実行',running:'実行中…',copyCurl:'cURL をコピー',copiedCurl:'コピー済み',resetEx:'例に戻す',
noParams:'このツールにパラメータはありません — そのまま実行できます。',sampleReqs:'サンプルリクエスト',tryPlay:'▶ プレイグラウンドで試す',
exCall:'呼び出し例とレスポンス',exCallSub:'呼び出し例',exRespSub:'レスポンス例 — 抜粋',
noParamsBadge:'パラメータなし',tabVisual:'表示',tabJson:'JSON',tabRaw:'Raw',
contacting:'サーバー接続中…',hintCors:'ブラウザから MCP に届く必要があります（CORS 開放）。ステージング URL またはローカル monstarx-mcp-jp を使ってください。',
previewNote:'<b>プレビューモード。</b> ライブ呼び出しはサンドボックス制限があります。自分のホストやローカルから開いてサーバーへ接続してください。',
paramRequired:'必須',paramOptional:'任意'
}
};
function t(key){const pack=I18N[LANG]||I18N.en;return pack[key]??I18N.en[key]??key;}
function catLabel(key){return t('cat_'+key)||CATLABEL[key]||key;}
function applyLang(lang){
  if(!I18N[lang])lang='en';
  LANG=lang;
  document.documentElement.lang=lang==='ja'?'ja':'en';
  document.documentElement.setAttribute('data-lang',lang);
  localStorage.setItem('mx-lang-jp',lang);
  const lbl=document.getElementById('langBtnLabel');
  if(lbl)lbl.textContent=lang==='ja'?'日本語':'EN';
  document.querySelectorAll('#langMenu [data-lang]').forEach(b=>b.classList.toggle('active',b.dataset.lang===lang));
  document.querySelectorAll('[data-i18n]').forEach(el=>{
    const k=el.getAttribute('data-i18n');const v=t(k);if(v!=null)el.textContent=v;
  });
  document.querySelectorAll('[data-i18n-html]').forEach(el=>{
    const k=el.getAttribute('data-i18n-html');const v=t(k);if(v!=null)el.innerHTML=v;
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el=>{
    const k=el.getAttribute('data-i18n-placeholder');const v=t(k);if(v!=null)el.placeholder=v;
  });
  document.querySelectorAll('[data-i18n-chip]').forEach(el=>{
    const k=el.getAttribute('data-i18n-chip');const v=t(k);
    if(v!=null){const emoji=el.querySelector('.e');el.innerHTML=(emoji?emoji.outerHTML+' ':'')+esc(v);}
  });
  // category headers in sidebar + playground list + tool cards
  document.querySelectorAll('.nav-h').forEach(el=>{
    const g=el.closest('[data-cat]');if(!g)return;
    const dot=el.querySelector('.dot');el.innerHTML=(dot?dot.outerHTML:'')+esc(catLabel(g.dataset.cat));
  });
  document.querySelectorAll('.pg-list .gl').forEach(el=>{
    const cat=el.dataset.cat;if(!cat)return;
    const dot=el.querySelector('.dot');el.innerHTML=(dot?dot.outerHTML:'')+esc(catLabel(cat));
  });
  document.querySelectorAll('[data-catsec]').forEach(el=>{
    const cat=el.dataset.catsec;const h=el.querySelector('h2');if(!h||!cat)return;
    const num=h.querySelector('.num');
    h.innerHTML=(num?num.outerHTML:'')+esc(catLabel(cat));
  });
  document.querySelectorAll('.tool .badge.cat').forEach(el=>{
    const toolEl=el.closest('.tool');if(!toolEl)return;
    const tool=DATA.tools[toolEl.id];if(!tool)return;
    const dot=el.querySelector('.dot');
    el.innerHTML=(dot?dot.outerHTML:'')+esc(catLabel(tool.cat));
  });
  document.querySelectorAll('.tool .tryit').forEach(el=>{el.textContent=t('tryPlay');});
  document.querySelectorAll('.tool .badge.np').forEach(el=>{el.textContent=t('noParamsBadge');});
  document.querySelectorAll('details.ex > summary').forEach(el=>{el.childNodes.forEach((n,i)=>{if(n.nodeType===3)n.textContent='';});el.appendChild(document.createTextNode(t('exCall')));});
  // refresh open tool form if any
  const sel=document.querySelector('#pgList button.sel');
  if(sel&&sel.dataset.tool){const n=sel.dataset.tool;const keep=collectArgsSafe();selectTool(n,Object.keys(keep).length?keep:undefined);}
  else if(document.getElementById('runBtn')){/* noop */}
}
function collectArgsSafe(){try{return collectArgs();}catch(e){return {};}}

const CATLABEL={}; DATA.categories.forEach((c,i)=>CATLABEL[c.key]=c.label);
const CATNUM={}; DATA.categories.forEach((c,i)=>CATNUM[c.key]=String(i+1));

function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function hl(obj){let j=(typeof obj==='string')?obj:JSON.stringify(obj,null,2);j=esc(j);
  return j.replace(/("(?:\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(?:true|false)\b|\bnull\b|-?\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?)/g,
   (m)=>{let c='num';if(/^"/.test(m)){c=/:$/.test(m)?'key':'str';}else if(/true|false/.test(m))c='bool';else if(/null/.test(m))c='null';return '<span class="'+c+'">'+m+'</span>';});}
function sh(s){return esc(s).replace(/(#.*)$/gm,'<span class="shc">$1</span>').replace(/\b(curl|claude|npx)\b/g,'<span class="shk">$1</span>')
  .replace(/(^|\s)(-[A-Za-z]\b|--[a-z-]+)/g,'$1<span class="shu">$2</span>').replace(/(https?:\/\/[^\s"']+)/g,'<span class="shs">$1</span>');}
function codeblock(label,inner,opts){opts=opts||{};const cls='code'+(opts.scroll?' scroll':'');
  return '<div class="'+cls+'"><button class="copy" data-raw="'+encodeURIComponent(opts.raw||inner.replace(/<[^>]+>/g,''))+'">Copy</button>'+
    '<div class="bar"><span class="dots"><i></i><i></i><i></i></span>'+esc(label)+'</div><pre class="tok">'+inner+'</pre></div>';}
function curlFor(name,args){return 'curl -X POST '+EP+'/mcp \\\n  -H "Content-Type: application/json" \\\n  -H "Accept: application/json, text/event-stream" \\\n  -H "mcp-protocol-version: 2025-06-18" \\\n  -d \''+JSON.stringify({jsonrpc:'2.0',id:1,method:'tools/call',params:{name:name,arguments:args}})+'\'';}

/* static blocks */
const content=document.querySelector('.content');
content.innerHTML=content.innerHTML
 .replace('__CB_CC__',codeblock('shell',sh('claude mcp add --transport http \\\n  jp-mcp '+EP+'/mcp'),{raw:'claude mcp add --transport http jp-mcp '+EP+'/mcp'}))
 .replace('__CB_CURSOR__',codeblock('mcp.json',hl({mcpServers:{japan:{type:"http",url:EP+'/mcp'}}})))
 .replace('__CB_DESK__',codeblock('json',hl({mcpServers:{japan:{command:"npx",args:["-y","mcp-remote",EP+'/mcp']}}})))
 .replace('__CB_QS__',codeblock('bash',sh(curlFor('jp_weather_24h',{area_code:'130000'})),{raw:curlFor('jp_weather_24h',{area_code:'130000'})}))
 .replace('__CB_ENV__',codeblock('structuredContent — jp_weather_24h',hl({source:"Open-Meteo JMA",agency:"Open-Meteo",retrieved_at:"2026-08-07T04:00:00.000Z",api:"v1/jma (hourly forecast 24h)",area_code:"130000",location:{latitude:35.6895,longitude:139.6917},data:{hourly:{time:["2026-08-07T00:00"],temperature_2m:[26.1]}}})))
 .replace('__CB_ERR__',codeblock('isError: true — missing required argument',hl({content:[{type:"text",text:"MCP error -32602: Input validation error: Invalid arguments for tool jp_postal_code: [{ path: ['zipcode'], message: 'expected string, received undefined' }]"}],isError:true})));

/* sidebar nav + reference cards */
const nav=document.getElementById('nav'),tools=document.getElementById('tools');
DATA.categories.forEach(cat=>{
  const g=document.createElement('div');g.className='nav-group';g.dataset.cat=cat.key;
  g.innerHTML='<div class="nav-h"><span class="dot" style="background:var(--dot-'+cat.key+')"></span>'+esc(catLabel(cat.key))+'</div><div class="nav">'+
    cat.tools.map(n=>'<a href="#'+n+'" data-tool="'+n+'">'+n+'</a>').join('')+'</div>';
  nav.appendChild(g);
  const sh2=document.createElement('div');sh2.dataset.catsec=cat.key;
  sh2.innerHTML='<h2 id="cat-'+cat.key+'"><span class="num">05.'+CATNUM[cat.key]+'</span>'+esc(catLabel(cat.key))+'</h2><p class="sec-blurb">'+esc(cat.blurb)+'</p>';
  tools.appendChild(sh2);
  cat.tools.forEach(n=>{
    const tDef=DATA.tools[n],hasP=tDef.params.length>0;
    const ptable=hasP?('<table class="ptable"><thead><tr><th>Parameter</th><th>Type</th><th>Description</th></tr></thead><tbody>'+
      tDef.params.map(p=>'<tr><td class="pn">'+p.name+(p.required?'<span class="req">*</span>':'')+'</td><td class="pt">'+p.type+'</td><td>'+esc(p.desc||'')+'</td></tr>').join('')+'</tbody></table>'):'<div class="noparam">'+esc(t('noParams'))+'</div>';
    const el=document.createElement('article');el.className='tool';el.id=n;el.dataset.hay=(n+' '+tDef.desc).toLowerCase();
    el.innerHTML='<div class="head"><div class="tname"><code>'+n+'</code><span class="badge cat"><span class="dot" style="background:var(--dot-'+cat.key+')"></span>'+esc(catLabel(cat.key))+'</span>'+
      (hasP?'':'<span class="badge np">'+esc(t('noParamsBadge'))+'</span>')+'<button class="tryit" data-try="'+n+'">'+esc(t('tryPlay'))+'</button></div><p class="tdesc">'+esc(tDef.desc)+'</p></div>'+
      '<div class="body">'+ptable+
      '<details class="ex"><summary>'+esc(t('exCall'))+'</summary>'+
        '<div class="mini-label">'+esc(t('exCallSub'))+'</div>'+codeblock('tools/call · arguments',hl(tDef.args))+
        '<div class="mini-label">'+esc(t('exRespSub'))+'</div>'+codeblock('structuredContent',hl(tDef.response),{scroll:true})+
      '</details></div>';
    tools.appendChild(el);
  });
});

/* ---------- PLAYGROUND ---------- */
const pgList=document.getElementById('pgList'),pgMain=document.getElementById('pgMain');
let respTab='visual',lastResp=null;

const SAMPLES={
 jp_weather_overview:{area_code:['130000','270000','040000','140000','230000']},
 jp_weather_week_overview:{area_code:['130000','270000','016000']},
 jp_weather_warnings:{area_code:['130000','270000','400000']},
 jp_weather_24h:{area_code:['130000','270000','040000','230000','016000']},
 jp_weather_4day:{area_code:['130000','270000','400000']},
 jp_uv_index:{area_code:['130000','270000']},
 jp_rainfall:{area_code:['130000','270000']},
 jp_air_temperature:{area_code:['130000','270000']},
 jp_relative_humidity:{area_code:['130000','270000']},
 jp_air_quality:{area_code:['130000','270000']},
 jp_earthquake_list:{limit:['5','10','20']},
 jp_tsunami_list:{limit:['5','10','20']},
 jp_postal_code:{zipcode:['1000001','100-0005','5300001','0600001','4600001']},
 jp_public_holidays:{year:['2026','2025','2027']},
 jp_elevation:{latitude:['35.681236','34.6937','43.0642'],longitude:['139.767125','135.5023','141.3469']},
 jp_boj_finance:{db:['FM01','IR02','CO'],code:['STRDCLUCON']},
 jp_disease_reports:{query:['感染症','インフルエンザ','COVID']},
 jp_evacuation_shelters:{municipality_code:['13101','131016','27100','01100'],type:['evacuation','emergency']},
 jp_tourism_spots:{latitude:['35.681236','35.0116','34.6937'],longitude:['139.767125','135.7681','135.5023']},
 jp_address_search:{query:['新宿','大阪城','札幌駅','渋谷','京都駅']},
 jp_geocode:{query:['東京駅','大阪駅','名古屋駅','福岡空港','富士山']},
 jp_reverse_geocode:{latitude:['35.681236','34.6937','35.0116'],longitude:['139.767125','135.5023','135.7681']},
 jp_datasets_search:{query:['天気','人口','防災','交通','統計']},
 jp_dataset_show:{id:['soumu_20140909_0289']},
 jp_dataset_metadata:{id:['soumu_20140909_0289']},
 jp_dataset_query:{resource_id:['fa8076f1-b13f-4d07-bb9a-fc0b521d1825']}
};
const ASK={
 jp_weather_areas:"What JMA area codes can I use for forecasts?",
 jp_weather_overview:"What's the JMA daily overview for Tokyo?",
 jp_weather_week_overview:"What's the week-ahead outlook for Tokyo?",
 jp_weather_warnings:"Are there any weather warnings for Tokyo right now?",
 jp_weather_24h:"What's the hourly forecast in Tokyo for the next 24 hours?",
 jp_weather_4day:"What's the 4-day forecast for Tokyo?",
 jp_uv_index:"How high is the UV index in Tokyo today?",
 jp_rainfall:"Is it raining in Tokyo right now (hourly)?",
 jp_air_temperature:"What are hourly temperatures in Tokyo?",
 jp_relative_humidity:"How humid is it in Tokyo hour by hour?",
 jp_air_quality:"How's the air quality (PM2.5 / AQI) in Tokyo?",
 jp_earthquake_list:"What earthquakes has JMA reported recently?",
 jp_tsunami_list:"Are there any recent tsunami advisories?",
 jp_postal_code:"What address is postal code 100-0001?",
 jp_public_holidays:"Which public holidays does Japan have in 2026?",
 jp_elevation:"What's the elevation at Tokyo Station?",
 jp_boj_finance:"What's the BOJ overnight call rate series?",
 jp_disease_reports:"Find open datasets about infectious diseases.",
 jp_evacuation_shelters:"Where are designated shelters in Chiyoda (Tokyo)?",
 jp_tourism_spots:"What tourist attractions are near Tokyo Station?",
 jp_address_search:"Find addresses matching 新宿.",
 jp_geocode:"What are the coordinates of 東京駅?",
 jp_reverse_geocode:"What's the address at 35.681236, 139.767125?",
 jp_datasets_search:"What open datasets mention 天気?",
 jp_dataset_show:"Show metadata for package soumu_20140909_0289.",
 jp_dataset_metadata:"Get dataset metadata by package id.",
 jp_dataset_query:"Query rows from a DATA.GO.JP datastore resource."
};
const PRESETS={
 jp_reverse_geocode:[
  {label:'Tokyo Station',args:{latitude:35.681236,longitude:139.767125}},
  {label:'Osaka',args:{latitude:34.6937,longitude:135.5023}},
  {label:'Kyoto',args:{latitude:35.0116,longitude:135.7681}}
 ],
 jp_elevation:[
  {label:'Tokyo Station',args:{latitude:35.681236,longitude:139.767125}},
  {label:'Mt. Fuji area',args:{latitude:35.3606,longitude:138.7274}}
 ],
 jp_tourism_spots:[
  {label:'Tokyo Station',args:{latitude:35.681236,longitude:139.767125,radius_m:1000,limit:10}},
  {label:'Shibuya',args:{latitude:35.6595,longitude:139.7005,radius_m:1200,limit:10}}
 ],
 jp_evacuation_shelters:[
  {label:'Chiyoda',args:{municipality_code:'13101',limit:10}},
  {label:'Near Tokyo St.',args:{latitude:35.681236,longitude:139.767125,limit:10}}
 ]
};

/* ---------- visual helpers ---------- */
function num(n){n=(typeof n==='number')?n:parseFloat(n);return isNaN(n)?'—':n.toLocaleString('en-US');}
function timeOnly(iso){try{return new Date(iso).toLocaleString('en-JP',{month:'short',day:'numeric',hour:'numeric',minute:'2-digit'});}catch(e){return iso||'';}}
function wkday(iso){try{return new Date(iso+(iso&&iso.length===10?'T00:00:00+09:00':'')).toLocaleDateString('en-JP',{weekday:'short',day:'numeric',month:'short'});}catch(e){return iso;}}
function vstat(big,label,sub){return '<div class="vstat"><div class="bn">'+big+'</div><div class="bl">'+esc(label)+'</div>'+(sub?'<div class="bs">'+esc(sub)+'</div>':'')+'</div>';}
function uvSev(v){if(v<3)return['Low','var(--sv-good)'];if(v<6)return['Moderate','var(--sv-mod)'];if(v<8)return['High','var(--sv-high)'];if(v<11)return['Very high','var(--sv-vhigh)'];return['Extreme','var(--sv-ext)'];}
function aqiSev(v){if(v<=20)return['Good','var(--sv-good)'];if(v<=40)return['Fair','var(--sv-mod)'];if(v<=60)return['Moderate','var(--sv-high)'];if(v<=80)return['Poor','var(--sv-vhigh)'];return['Very poor','var(--sv-ext)'];}
function wmoEmoji(c){c=+c;if(c===0)return'☀️';if(c<=3)return'⛅';if(c<=48)return'🌫️';if(c<=67)return'🌧️';if(c<=77)return'🌨️';if(c<=82)return'🌦️';if(c<=99)return'⛈️';return'🌤️';}
function gauge(v,max,sev,color){const pct=Math.max(3,Math.min(100,(+v||0)/max*100));return '<div class="gauge"><div class="gv" style="color:'+color+'">'+v+'<small> '+esc(sev)+'</small></div><div class="gbar"><i style="width:'+pct+'%;background:'+color+'"></i></div></div>';}

/* Japan map bounds (main islands + Okinawa) */
const JPB={lo:122.5,ln:146.5,la:24.0,lt:46.0};
const JP_OUTLINE=[[129.5,33.2],[130.5,31.5],[131.2,30.8],[135.0,33.5],[136.5,34.5],[137.5,34.8],[139.0,35.0],[140.5,35.5],[141.5,38.0],[142.0,41.5],[141.5,43.5],[140.0,45.5],[139.0,43.0],[138.0,37.0],[136.0,36.0],[133.0,34.5],[131.0,34.0],[129.5,33.2]];
function prj(lng,lat){return [((lng-JPB.lo)/(JPB.ln-JPB.lo))*1000,((JPB.lt-lat)/(JPB.lt-JPB.la))*600];}
function mapView(points,note){
 points=(points||[]).filter(p=>isFinite(p.lat)&&isFinite(p.lng)&&p.lat>20&&p.lat<50&&p.lng>120&&p.lng<150);
 if(!points.length)return null;
 const cap=60,shown=points.slice(0,cap);
 const path='M'+JP_OUTLINE.map(c=>prj(c[0],c[1]).map(n=>n.toFixed(1)).join(',')).join(' L')+' Z';
 const pins=shown.map(p=>{const a=prj(p.lng,p.lat);return '<g><circle cx="'+a[0].toFixed(1)+'" cy="'+a[1].toFixed(1)+'" r="9" fill="var(--accent)" fill-opacity="0.92" stroke="#fff" stroke-width="2"/>'+(p.value?'<text x="'+a[0].toFixed(1)+'" y="'+(a[1]-14).toFixed(1)+'" class="pv">'+esc(p.value)+'</text>':'')+'<title>'+esc((p.label||'')+(p.sub?' · '+p.sub:''))+'</title></g>';}).join('');
 const list=shown.map(p=>'<li><span class="dotp"></span><b>'+esc(p.label||'—')+'</b>'+(p.sub?' <span>'+esc(p.sub)+'</span>':'')+(p.value?' <em>'+esc(p.value)+'</em>':'')+'</li>').join('');
 return '<div class="vmap"><svg viewBox="0 0 1000 600" preserveAspectRatio="xMidYMid meet"><path d="'+path+'" fill="var(--map-land)" stroke="var(--map-stroke)" stroke-width="2" stroke-linejoin="round"/>'+pins+'</svg></div><ol class="vlist">'+list+'</ol>'+(points.length>cap?'<div class="vnote">Showing '+cap+' of '+points.length+' points.</div>':'')+(note?'<div class="vnote">'+esc(note)+'</div>':'');
}
function locHead(p){const L=p.location||{};return (L.query||L.area_code||'')?(esc(L.query||('area '+L.area_code))+' · '+(L.latitude!=null?L.latitude.toFixed(3)+', '+L.longitude.toFixed(3):'')):'';}
function hourlyTable(h,cols){
 if(!h||!h.time)return null;
 const n=Math.min(h.time.length,24);
 let head='<th>Time</th>'+cols.map(c=>'<th class="r">'+esc(c.label)+'</th>').join('');
 let body='';
 for(let i=0;i<n;i++){
  body+='<tr><td>'+esc((h.time[i]||'').replace('T',' '))+'</td>'+cols.map(c=>{const v=h[c.key]?h[c.key][i]:null;return '<td class="r">'+(v==null?'—':esc(v)+(c.unit||''))+'</td>';}).join('')+'</tr>';
 }
 return '<div class="vtwrap"><table class="vt"><thead><tr>'+head+'</tr></thead><tbody>'+body+'</tbody></table></div>';
}
function overviewText(p){const d=p.data||{};const text=d.text||d.headlineText||(typeof d==='string'?d:JSON.stringify(d).slice(0,400));const title=d.targetArea||d.headTitle||p.area_code||'overview';return '<div class="vhead">JMA overview · '+esc(title)+' · '+timeOnly(d.reportDatetime||'')+'</div><div class="ccard"><div style="white-space:pre-wrap;line-height:1.55">'+esc(String(text).slice(0,1200))+'</div></div>';}
function officesView(p){const o=p.offices||[];return '<div class="vhead">'+num(p.total_offices||o.length)+' JMA forecast offices</div><div class="vtwrap"><table class="vt"><thead><tr><th>Code</th><th>Name</th><th>English</th></tr></thead><tbody>'+o.slice(0,40).map(x=>'<tr><td class="mono"><b>'+esc(x.area_code)+'</b></td><td>'+esc(x.name)+'</td><td>'+esc(x.en_name||'')+'</td></tr>').join('')+'</tbody></table></div>'+(o.length>40?'<div class="vnote">Showing 40 of '+o.length+'.</div>':'');}
function wx24(p){const h=(p.data&&p.data.hourly)||{};const head=locHead(p)||('area '+p.area_code);const temps=h.temperature_2m||[];const hi=temps.length?Math.max(...temps.filter(x=>x!=null)):'—';const lo=temps.length?Math.min(...temps.filter(x=>x!=null)):'—';return '<div class="vhead">24h forecast · '+esc(head)+'</div><div class="statrow">'+vstat(hi+'°','high')+vstat(lo+'°','low')+vstat(num((h.time||[]).length),'hours')+'</div>'+(hourlyTable(h,[{key:'temperature_2m',label:'Temp',unit:'°'},{key:'relative_humidity_2m',label:'RH',unit:'%'},{key:'rain',label:'Rain',unit:'mm'},{key:'weather_code',label:'WMO'}])||'');}
function wx4(p){const d=(p.data&&p.data.daily)||{};const times=d.time||[];return '<div class="vhead">4-day forecast · '+esc(locHead(p)||p.area_code||'')+'</div><div class="daygrid">'+times.map((t,i)=>'<div class="day"><div class="dd">'+wkday(t)+'</div><div class="e">'+wmoEmoji(d.weather_code&&d.weather_code[i])+'</div><div class="dt">'+(d.temperature_2m_min?d.temperature_2m_min[i]:'—')+'–'+(d.temperature_2m_max?d.temperature_2m_max[i]:'—')+'°</div><div class="df">precip '+(d.precipitation_sum?d.precipitation_sum[i]:'—')+' mm</div></div>').join('')+'</div>';}
function uvView(p){const h=(p.data&&p.data.hourly)||{};const vals=h.uv_index||[];const cur=vals.length?Math.max(...vals.map(Number).filter(x=>!isNaN(x))):0;const s=uvSev(cur);return '<div class="vhead">UV index · '+esc(locHead(p)||'')+'</div>'+gauge((+cur).toFixed(1),12,s[0],s[1])+(hourlyTable(h,[{key:'uv_index',label:'UV'}])||'');}
function rainView(p){const h=(p.data&&p.data.hourly)||{};const rains=(h.rain||[]).map(Number);const sum=rains.reduce((a,b)=>a+(isNaN(b)?0:b),0);const peak=rains.length?Math.max(...rains):0;return '<div class="vhead">Hourly rainfall · '+esc(locHead(p)||'')+'</div><div class="statrow">'+vstat(sum.toFixed(1)+' mm','24h total')+vstat(peak.toFixed(1)+' mm','peak hour')+'</div>'+(hourlyTable(h,[{key:'rain',label:'Rain',unit:' mm'}])||'');}
function tempView(p){const h=(p.data&&p.data.hourly)||{};const t=(h.temperature_2m||[]).map(Number).filter(x=>!isNaN(x));const hi=t.length?Math.max(...t):'—';const lo=t.length?Math.min(...t):'—';return '<div class="vhead">Hourly temperature · '+esc(locHead(p)||'')+'</div><div class="statrow">'+vstat(hi+'°C','high')+vstat(lo+'°C','low')+'</div>'+(hourlyTable(h,[{key:'temperature_2m',label:'°C'}])||'');}
function humView(p){const h=(p.data&&p.data.hourly)||{};return '<div class="vhead">Relative humidity · '+esc(locHead(p)||'')+'</div>'+(hourlyTable(h,[{key:'relative_humidity_2m',label:'RH',unit:'%'}])||'');}
function aqView(p){const h=(p.data&&p.data.hourly)||{};const aqi=(h.european_aqi||[]).map(Number).filter(x=>!isNaN(x));const cur=aqi.length?aqi[Math.min(aqi.length-1,12)]||aqi[0]:0;const s=aqiSev(cur);return '<div class="vhead">Air quality · '+esc(locHead(p)||'')+'</div>'+gauge(cur,100,s[0],s[1])+(hourlyTable(h,[{key:'european_aqi',label:'EAQI'},{key:'pm2_5',label:'PM2.5'},{key:'pm10',label:'PM10'},{key:'ozone',label:'O₃'}])||'');}
function warningsView(p){
 const d=p.data||{};let rows=[];
 try{
  (d.areaTypes||[]).forEach(function(at){
   (at.areas||[]).forEach(function(a){
    (a.warnings||[]).forEach(function(w){
     rows.push({area:a.name||a.code,code:w.code,status:w.status||w.name||''});
    });
   });
  });
 }catch(e){}
 if(!rows.length)return '<div class="vhead">Warnings · area '+esc(p.area_code||'')+'</div>'+vstat('\u2705','no structured warnings','or format not listed');
 return '<div class="vhead">Warnings · '+esc(p.area_code||'')+' · '+rows.length+' row(s)</div><div class="vtwrap"><table class="vt"><thead><tr><th>Area</th><th>Code</th><th>Status</th></tr></thead><tbody>'+rows.slice(0,40).map(function(r){return '<tr><td><b>'+esc(r.area)+'</b></td><td class="mono">'+esc(r.code)+'</td><td>'+esc(r.status)+'</td></tr>';}).join('')+'</tbody></table></div>';
}
function eventsView(p,kind){const ev=p.events||[];if(!ev.length)return '<div class="vhead">'+kind+'</div>'+vstat('—','no events','in this response');
 return '<div class="vhead">'+kind+' · '+num(p.shown||ev.length)+' of '+num(p.total||ev.length)+'</div><ul class="ilist">'+ev.map(e=>'<li><span class="tt">'+(e.magnitude!=null?'M'+esc(e.magnitude):'')+(e.max_intensity!=null?' · max '+esc(e.max_intensity):'')+'</span><b>'+esc(e.hypocenter||e.title||e.event_id||'event')+'</b> · '+esc(timeOnly(e.issued_at))+(e.hypocenter_en?' <span class="sub">'+esc(e.hypocenter_en)+'</span>':'')+'</li>').join('')+'</ul>';}
function postalView(p){const a=p.addresses||[];return '<div class="vhead">Postal '+esc(p.zipcode||'')+' · '+num(p.found)+' match(es)</div>'+a.map(x=>'<div class="ccard" style="margin-bottom:10px"><div class="cn">'+esc((x.prefecture||'')+(x.city||'')+(x.town||''))+'</div><div class="cg"><span>Prefecture</span><b>'+esc(x.prefecture||'—')+'</b></div><div class="cg"><span>City</span><b>'+esc(x.city||'—')+'</b></div><div class="cg"><span>Town</span><b>'+esc(x.town||'—')+'</b></div><div class="cg"><span>Zip</span><b class="mono">'+esc(x.zipcode||p.zipcode||'')+'</b></div></div>').join('');}
function holidaysView(p){const h=p.holidays||[];return '<div class="vhead">Japan public holidays · '+esc(p.year||'')+' · '+num(p.total||h.length)+'</div><div class="vtwrap"><table class="vt"><thead><tr><th>Date</th><th>Local name</th><th>English</th></tr></thead><tbody>'+h.map(x=>'<tr><td class="mono">'+esc(x.date)+'</td><td><b>'+esc(x.local_name)+'</b></td><td>'+esc(x.name)+'</td></tr>').join('')+'</tbody></table></div>';}
function elevView(p){const r=p.result||{};const src=r.data_source||r.hsrc||'';return '<div class="vhead">Elevation</div><div class="statrow">'+vstat((r.elevation_m!=null?r.elevation_m:'—')+' m','elevation',src)+vstat((r.latitude||'')+', '+(r.longitude||''),'coordinates')+'</div>';}
function geoResults(p){const r=p.results||[];const pts=r.filter(x=>x.latitude!=null).map(x=>({lat:+x.latitude,lng:+x.longitude,label:x.title,sub:x.address_code}));return '<div class="vhead">'+(p.found!=null?num(p.found)+' found · ':'')+'showing '+r.length+(p.query?' · "'+esc(p.query)+'"':'')+'</div>'+(mapView(pts)||'')+'<div class="vtwrap" style="margin-top:10px"><table class="vt"><thead><tr><th>Title</th><th>Lat</th><th>Lon</th><th>Code</th></tr></thead><tbody>'+r.map(x=>'<tr><td><b>'+esc(x.title)+'</b></td><td class="mono">'+esc(x.latitude)+'</td><td class="mono">'+esc(x.longitude)+'</td><td class="mono">'+esc(x.address_code||'')+'</td></tr>').join('')+'</tbody></table></div>';}
function reverseView(p){const r=p.result||{};const pts=(r.found&&r.latitude!=null)?[{lat:+r.latitude,lng:+r.longitude,label:r.address,sub:r.municipality_code}]:[];return '<div class="vhead">Reverse geocode</div>'+(r.found?vstat(esc(r.address||'—'),'address','muni '+esc(r.municipality_code||'')):vstat('—','not found'))+(mapView(pts)||'');}
function shelterView(p){const s=p.shelters||[];const pts=s.filter(x=>x.latitude!=null).map(x=>({lat:+x.latitude,lng:+x.longitude,label:x.name,sub:x.address}));return '<div class="vhead">Shelters · muni '+esc(p.municipality_code||'')+' · '+num(p.shown||s.length)+' of '+num(p.total||s.length)+' · '+esc(p.type||'')+'</div>'+(mapView(pts)||'')+'<ul class="ilist">'+s.map(x=>'<li><span class="tt">'+esc(x.name||'')+'</span>'+esc(x.address||'')+'</li>').join('')+'</ul>';}
function tourismView(p){const s=p.spots||[];const pts=s.filter(x=>x.latitude!=null).map(x=>({lat:+x.latitude,lng:+x.longitude,label:x.name||x.name_ja||x.name_en,sub:x.tourism}));return '<div class="vhead">Tourism · '+num(p.shown||s.length)+' spots · r='+num(p.radius_m)+'m</div>'+(mapView(pts)||'')+'<div class="vtwrap" style="margin-top:10px"><table class="vt"><thead><tr><th>Name</th><th>Type</th><th>Lat</th><th>Lon</th></tr></thead><tbody>'+s.map(x=>'<tr><td><b>'+esc(x.name||x.name_ja||x.name_en||'—')+'</b></td><td>'+esc(x.tourism||'')+'</td><td class="mono">'+esc(x.latitude)+'</td><td class="mono">'+esc(x.longitude)+'</td></tr>').join('')+'</tbody></table></div>';}
function datasetsView(p){const d=p.datasets||[];return '<div class="vhead">Datasets · '+num(p.total)+' total · showing '+d.length+(p.query?' · "'+esc(p.query)+'"':'')+'</div><div class="vtwrap"><table class="vt"><thead><tr><th>Title</th><th>Org</th><th>Name</th></tr></thead><tbody>'+d.map(x=>'<tr><td><b>'+esc(x.title||x.name)+'</b><div class="sub">'+(x.tags||[]).slice(0,4).join(', ')+'</div></td><td>'+esc(x.organization||'')+'</td><td class="mono">'+esc(x.name||x.id||'')+'</td></tr>').join('')+'</tbody></table></div>';}
function datasetShow(p){const d=p.dataset||{};const res=d.resources||[];return '<div class="vhead">'+esc(d.title||d.name||p.id||'dataset')+'</div><div class="ccard"><div class="cg"><span>Name</span><b class="mono">'+esc(d.name||'')+'</b></div><div class="cg"><span>Org</span><b>'+esc(d.organization||'')+'</b></div><div class="cg"><span>Tags</span><b>'+esc((d.tags||[]).join(', '))+'</b></div></div>'+(res.length?'<div class="mini-label">Resources</div><div class="vtwrap"><table class="vt"><thead><tr><th>Name</th><th>Format</th><th>Id</th></tr></thead><tbody>'+res.map(r=>'<tr><td>'+esc(r.name)+'</td><td>'+esc(r.format)+'</td><td class="mono">'+esc(r.id)+'</td></tr>').join('')+'</tbody></table></div>':'');}
function genTable(recs){recs=recs||[];if(!recs.length)return null;const cols=Object.keys(recs[0]).filter(k=>k!=='_id').slice(0,7);return '<div class="vhead">'+recs.length+' rows</div><div class="vtwrap"><table class="vt"><thead><tr>'+cols.map(c=>'<th>'+esc(c)+'</th>').join('')+'</tr></thead><tbody>'+recs.map(r=>'<tr>'+cols.map(c=>'<td>'+esc(r[c])+'</td>').join('')+'</tr>').join('')+'</tbody></table></div>';}
function bojView(p){
  const d=p.data||{};
  // Live shape: full BOJ payload with RESULTSET[].VALUES.{SURVEY_DATES,VALUES}
  // Legacy/sample shape: OBS[{TIME,OBS_VALUE}]
  const series=(d.RESULTSET||d.resultset||[])[0];
  let rows=[];
  if(series&&series.VALUES){
    const dates=series.VALUES.SURVEY_DATES||series.VALUES.survey_dates||[];
    const vals=series.VALUES.VALUES||series.VALUES.values||[];
    rows=dates.map((t,i)=>({time:t,value:vals[i]})).filter(r=>r.value!=null);
  }else{
    const obs=d.OBS||d.obs||[];
    rows=(Array.isArray(obs)?obs:Object.values(obs||{})).map(o=>({time:o.TIME||o.time,value:o.OBS_VALUE||o.value}));
  }
  const head=series?(esc(series.SERIES_CODE||p.code||'')+(series.NAME_OF_TIME_SERIES?' · '+esc(series.NAME_OF_TIME_SERIES):'')+(series.UNIT?' ('+esc(series.UNIT)+')':'')):esc(p.db||'')+' / '+esc(p.code||'');
  return '<div class="vhead">BOJ · '+esc(p.db||'')+(series?' · '+head:'')+'</div>'+(rows.length?genTable(rows.slice(0,40)):codeblock('data',hl(d),{scroll:true}));
}

function visualize(name,p){try{return _viz(name,p);}catch(e){console.warn('viz fail',name,e);return null;}}
function _viz(name,p){if(!p||typeof p!=='object')return null;switch(name){
 case 'jp_weather_areas':return officesView(p);
 case 'jp_weather_overview':
 case 'jp_weather_week_overview':return overviewText(p);
 case 'jp_weather_warnings':return warningsView(p);
 case 'jp_weather_24h':return wx24(p);
 case 'jp_weather_4day':return wx4(p);
 case 'jp_uv_index':return uvView(p);
 case 'jp_rainfall':return rainView(p);
 case 'jp_air_temperature':return tempView(p);
 case 'jp_relative_humidity':return humView(p);
 case 'jp_air_quality':return aqView(p);
 case 'jp_earthquake_list':return eventsView(p,'Earthquakes');
 case 'jp_tsunami_list':return eventsView(p,'Tsunami advisories');
 case 'jp_postal_code':return postalView(p);
 case 'jp_public_holidays':return holidaysView(p);
 case 'jp_elevation':return elevView(p);
 case 'jp_boj_finance':return bojView(p);
 case 'jp_disease_reports':return datasetsView(p);
 case 'jp_evacuation_shelters':return shelterView(p);
 case 'jp_tourism_spots':return tourismView(p);
 case 'jp_address_search':
 case 'jp_geocode':return geoResults(p);
 case 'jp_reverse_geocode':return reverseView(p);
 case 'jp_datasets_search':return datasetsView(p);
 case 'jp_dataset_show':
 case 'jp_dataset_metadata':return datasetShow(p);
 case 'jp_dataset_query':return genTable(p.records)||null;
}return null;}

DATA.categories.forEach(cat=>{
  const gl=document.createElement('div');gl.className='gl';gl.dataset.cat=cat.key;gl.innerHTML='<span class="dot" style="background:var(--dot-'+cat.key+')"></span>'+esc(catLabel(cat.key));
  pgList.appendChild(gl);
  cat.tools.forEach(n=>{const b=document.createElement('button');b.textContent=n;b.dataset.tool=n;b.onclick=()=>selectTool(n);pgList.appendChild(b);});
});
function sampleChips(tool,param){const vals=(SAMPLES[tool]||{})[param];if(!vals||!vals.length)return '';return '<div class="samples">'+vals.map(v=>'<button type="button" class="samp" data-p="'+param+'" data-v="'+esc(v)+'">'+esc(v)+'</button>').join('')+'</div>';}
function fieldFor(p,val,tool){
  const req=p.required?' <span class="req">*</span>':'';
  const ty='<span class="ty">'+p.type+' · '+(p.required?t('paramRequired'):t('paramOptional'))+'</span>';
  let ctrl;
  if(p.type==='boolean'){ctrl='<select data-p="'+p.name+'" data-t="boolean"><option value="">—</option><option value="true"'+(val===true?' selected':'')+'>true</option><option value="false"'+(val===false?' selected':'')+'>false</option></select>';}
  else if(p.type==='integer'||p.type==='number'){ctrl='<input data-p="'+p.name+'" data-t="'+p.type+'" type="number" value="'+(val!==undefined&&val!==null?esc(val):'')+'" step="any" placeholder="'+(p.required?t('paramRequired'):t('paramOptional'))+'">';}
  else if(p.type==='array'){ctrl='<input data-p="'+p.name+'" data-t="array" type="text" value="'+(Array.isArray(val)?esc(val.join(', ')):'')+'" placeholder="comma,separated">';}
  else if(p.type==='object'){ctrl='<textarea data-p="'+p.name+'" data-t="object" rows="2" placeholder="{ }">'+(val?esc(JSON.stringify(val)):'')+'</textarea>';}
  else{ctrl='<input data-p="'+p.name+'" data-t="string" type="text" value="'+(val!==undefined&&val!==null?esc(val):'')+'" placeholder="'+(p.required?t('paramRequired'):t('paramOptional'))+'">';}
  return '<div class="field"><label>'+p.name+req+ty+'</label><div>'+ctrl+(p.desc?'<div class="hint">'+esc(p.desc)+'</div>':'')+sampleChips(tool,p.name)+'</div></div>';
}
function selectTool(n,overrideArgs){
  [...pgList.querySelectorAll('button')].forEach(b=>b.classList.toggle('sel',b.dataset.tool===n));
  const toolDef=DATA.tools[n];const args=overrideArgs||toolDef.args||{};const cat=toolDef.cat;
  let form;
  if(toolDef.params.length){form='<div class="form">'+toolDef.params.map(p=>fieldFor(p,args[p.name],n)).join('')+'</div>';}
  else{form='<div class="noparams">'+esc(t('noParams'))+'</div>';}
  const ask=ASK[n]?'<div class="ask">💬 <span class="q">'+esc(ASK[n])+'</span></div>':'';
  const presets=PRESETS[n]?'<div class="presets"><span class="pl">'+esc(t('sampleReqs'))+'</span>'+PRESETS[n].map((pr,i)=>'<button class="preset" data-n="'+n+'" data-i="'+i+'">'+esc(pr.label)+'</button>').join('')+'</div>':'';
  pgMain.innerHTML='<div class="tn"><code>'+n+'</code><span class="badge cat"><span class="dot" style="background:var(--dot-'+cat+')"></span>'+esc(catLabel(cat))+'</span></div>'+
    '<p class="td">'+esc(toolDef.desc)+'</p>'+ask+presets+form+
    '<div class="runbar"><button class="run" id="runBtn">'+esc(t('runQuery'))+'</button>'+
      '<button class="linkbtn" id="curlBtn">'+esc(t('copyCurl'))+'</button>'+
      '<button class="linkbtn" id="resetBtn">'+esc(t('resetEx'))+'</button></div>'+
    '<div class="resp" id="resp"></div>';
  document.getElementById('runBtn').onclick=()=>runCurrent(n);
  document.getElementById('resetBtn').onclick=()=>selectTool(n);
  document.getElementById('curlBtn').onclick=(e)=>{navigator.clipboard.writeText(curlFor(n,collectArgs()));e.target.textContent=t('copiedCurl');setTimeout(()=>e.target.textContent=t('copyCurl'),1400);};
  lastResp=null;
}
function collectArgs(){
  const args={};pgMain.querySelectorAll('[data-p]').forEach(el=>{
    const k=el.dataset.p,t=el.dataset.t;let v=el.value;
    if(v===''||v===null){return;}
    if(t==='integer'||t==='number'){v=Number(v);if(!isNaN(v))args[k]=v;}
    else if(t==='boolean'){args[k]=(v==='true');}
    else if(t==='array'){args[k]=v.split(',').map(s=>s.trim()).filter(Boolean);}
    else if(t==='object'){try{args[k]=JSON.parse(v);}catch(e){}}
    else{args[k]=v;}
  });return args;
}
function parseMaybeSSE(text){
  try{return JSON.parse(text);}catch(e){}
  const lines=text.split(/\r?\n/).filter(l=>l.startsWith('data:'));
  for(let i=lines.length-1;i>=0;i--){try{return JSON.parse(lines[i].slice(5).trim());}catch(e){}}
  return null;
}
async function runCurrent(n){
  const args=collectArgs();const btn=document.getElementById('runBtn'),resp=document.getElementById('resp');
  btn.disabled=true;btn.textContent=t('running');
  resp.innerHTML='<div class="resp-meta"><span class="pill" style="color:var(--muted);background:var(--panel-2)"><span class="d"></span> '+esc(t('contacting'))+'</span></div>';
  const t0=performance.now();
  try{
    const res=await fetch(EP+'/mcp',{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json, text/event-stream','mcp-protocol-version':'2025-06-18'},body:JSON.stringify({jsonrpc:'2.0',id:1,method:'tools/call',params:{name:n,arguments:args}})});
    const ms=Math.round(performance.now()-t0);
    const text=await res.text();const json=parseMaybeSSE(text);
    const r=json&&json.result;const isErr=r&&r.isError;
    let payload;
    if(r&&r.structuredContent)payload=r.structuredContent;
    else if(r&&r.content&&r.content[0]){try{payload=JSON.parse(r.content[0].text);}catch(e){payload=r.content[0].text;}}
    else payload=json;
    lastResp={ms,status:res.status,isErr,payload,raw:text,rpc:json,name:n};
    respTab=(!isErr&&visualize(n,payload))?'visual':'pretty';
    renderResp();
  }catch(err){
    const ms=Math.round(performance.now()-t0);
    lastResp={ms,status:0,isErr:true,payload:{error:String(err),hint:t('hintCors')},blocked:true,name:n};
    respTab='pretty';
    renderResp();
  }
  btn.disabled=false;btn.textContent=t('runQuery');
}
function renderResp(){
  const r=lastResp;if(!r)return;const resp=document.getElementById('resp');
  const vis=(!r.isErr)?visualize(r.name,r.payload):null;
  if(respTab==='visual'&&!vis)respTab='pretty';
  const okpill=r.isErr?'<span class="pill err"><span class="d"></span> '+(r.status||'error')+(r.blocked?' · blocked':' · isError')+'</span>':'<span class="pill ok"><span class="d"></span> '+r.status+' OK</span>';
  const tab=(id,lbl)=>'<button class="'+(respTab===id?'on':'')+'" data-tab="'+id+'">'+lbl+'</button>';
  const tabs=r.blocked?'':'<span class="tabs">'+(vis?tab('visual',t('tabVisual')):'')+tab('pretty',t('tabJson'))+tab('raw',t('tabRaw'))+'</span>';
  let inner;
  if(respTab==='visual'&&vis)inner='<div class="vis">'+vis+'</div>';
  else if(respTab==='raw')inner=codeblock('response',hl(r.rpc||r.raw||''),{scroll:true,raw:(r.raw||JSON.stringify(r.rpc,null,2))});
  else inner=codeblock('response',hl(r.payload),{scroll:true,raw:(typeof r.payload==='string'?r.payload:JSON.stringify(r.payload,null,2))});
  resp.innerHTML='<div class="resp-meta">'+okpill+'<span>'+r.ms+' ms</span>'+tabs+'</div>'+inner;
  resp.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>{respTab=b.dataset.tab;renderResp();});
}
const EXAMPLES={
  wx24:['jp_weather_24h',{area_code:'130000'}],
  quake:['jp_earthquake_list',{limit:5}],
  geo:['jp_geocode',{query:'東京駅',limit:3}],
  postal:['jp_postal_code',{zipcode:'1000001'}],
  holiday:['jp_public_holidays',{year:2026}],
  shelter:['jp_evacuation_shelters',{municipality_code:'13101',limit:5}],
  tourism:['jp_tourism_spots',{latitude:35.681236,longitude:139.767125,radius_m:1000,limit:8}],
  datasets:['jp_datasets_search',{query:'天気',rows:5}]
};
document.querySelectorAll('.chip-ex').forEach(c=>c.onclick=()=>{const [n,a]=EXAMPLES[c.dataset.ex];selectTool(n,a);document.getElementById('playground').scrollIntoView();setTimeout(()=>runCurrent(n),120);});
document.addEventListener('click',e=>{const b=e.target.closest('.tryit');if(!b)return;const n=b.dataset.try;selectTool(n);document.getElementById('playground').scrollIntoView({behavior:'smooth'});});
document.addEventListener('click',e=>{
  const s=e.target.closest('.samp');if(s){const inp=pgMain.querySelector('[data-p="'+s.dataset.p+'"]');if(inp){inp.value=s.dataset.v;inp.focus();}return;}
  const pr=e.target.closest('.preset');if(pr){const n=pr.dataset.n,i=+pr.dataset.i;selectTool(n,PRESETS[n][i].args);runCurrent(n);return;}
});
selectTool('jp_weather_24h');

/* copy / theme / lang / filter / menu */
document.addEventListener('click',e=>{const b=e.target.closest('.copy');if(!b)return;navigator.clipboard.writeText(decodeURIComponent(b.dataset.raw||'')).then(()=>{const o=b.textContent;b.textContent='Copied';b.classList.add('ok');setTimeout(()=>{b.textContent=o;b.classList.remove('ok');},1400);});});
document.getElementById('epPill').onclick=()=>{navigator.clipboard.writeText(EP+'/mcp');const u=document.querySelector('#epPill .u');const o=u.textContent;u.textContent='Copied!';setTimeout(()=>u.textContent=o,1100);};
const root=document.documentElement,saved=localStorage.getItem('mx-theme-jp');if(saved)root.setAttribute('data-theme',saved);
document.getElementById('themeBtn').onclick=()=>{const cur=root.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light');const nx=cur==='dark'?'light':'dark';root.setAttribute('data-theme',nx);localStorage.setItem('mx-theme-jp',nx);};

const langBtn=document.getElementById('langBtn'),langMenu=document.getElementById('langMenu');
function setLangMenu(open){langMenu.classList.toggle('open',open);langBtn.setAttribute('aria-expanded',open?'true':'false');}
langBtn.onclick=(e)=>{e.stopPropagation();setLangMenu(!langMenu.classList.contains('open'));};
langMenu.querySelectorAll('[data-lang]').forEach(b=>{
  b.onclick=(e)=>{e.stopPropagation();applyLang(b.dataset.lang);setLangMenu(false);};
});
document.addEventListener('click',()=>setLangMenu(false));

applyLang(LANG);

const filter=document.getElementById('filter');filter.oninput=()=>{const q=filter.value.trim().toLowerCase();DATA.categories.forEach(cat=>{let vis=0;cat.tools.forEach(n=>{const card=document.getElementById(n),link=document.querySelector('.nav a[data-tool="'+n+'"]');const m=!q||card.dataset.hay.includes(q);card.style.display=m?'':'none';if(link)link.style.display=m?'':'none';if(m)vis++;});const sec=document.querySelector('[data-catsec="'+cat.key+'"]'),ng=document.querySelector('.nav-group[data-cat="'+cat.key+'"]');if(sec)sec.style.display=vis?'':'none';if(ng)ng.style.display=vis?'':'none';});};
const links=[...document.querySelectorAll('.nav a[data-tool]')],byTool={};links.forEach(l=>byTool[l.dataset.tool]=l);
const io=new IntersectionObserver(ents=>{ents.forEach(e=>{if(e.isIntersecting){links.forEach(l=>l.classList.remove('active'));const l=byTool[e.target.id];if(l)l.classList.add('active');}});},{rootMargin:'-72px 0px -70% 0px'});
document.querySelectorAll('.tool').forEach(t=>io.observe(t));
const sb=document.getElementById('sidebar'),scrim=document.getElementById('scrim');
function toggleMenu(on){sb.classList.toggle('open',on);scrim.classList.toggle('open',on);}
document.getElementById('menuBtn').onclick=()=>toggleMenu(!sb.classList.contains('open'));
scrim.onclick=()=>toggleMenu(false);sb.addEventListener('click',e=>{if(e.target.closest('a'))toggleMenu(false);});
if(location.hostname.endsWith('claude.ai')||location.hostname.includes('artifact')){const nt=document.getElementById('pgNote');nt.classList.add('show');nt.innerHTML=t('previewNote');}
</script>
'''

# Write build.py pieces safely (no f-string — STYLE/SCRIPT contain many braces).
# BODYTOP already has LOGO SVG expanded.

def py_triple(name, s, raw=False):
    # Only the *opening* delimiter may use r"""; closing is always """.
    # Using r""" as the closer made the trailing "r" part of the string
    # (STYLE ended with "</style>\nr") and broke the generated HTML/JS.
    if '"""' in s:
        raise SystemExit(f"{name} contains triple quotes")
    start = 'r"""' if raw else '"""'
    return f"{name} = {start}{s}\"\"\"\n"

header = '''#!/usr/bin/env python3
"""Generate the MonstarX Japan MCP playground HTML from tool metadata.

Run from anywhere:  python build/build.py
Reads:  build/data.min.json  (tool schemas + captured example responses)
Writes: public/index.html  and  japan-mcp-playground.html  (identical)
"""
import os
from urllib.parse import quote
BASE=os.path.dirname(os.path.abspath(__file__))
REPO=os.path.dirname(BASE)
DATA=open(os.path.join(BASE,'data.min.json'),encoding='utf-8').read()
FAVICON_SVG='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" fill="#0d0d0d"/><g fill="#fff" transform="translate(1 1)"><path fill-rule="evenodd" d="M29.3493 25.3568L20.5472 16.5546L16.5546 20.5472L25.3568 29.3493L29.3493 25.3568ZM8.76813 12.7607L12.7607 8.76813L3.99257 0L0 3.99257L8.76813 12.7607ZM9.03679e-07 25.3568L8.8024 16.5543L12.795 20.5469L3.99257 29.3493L9.03679e-07 25.3568ZM20.5814 12.7605L16.5889 8.7679L25.3568 0L29.3493 3.99257L20.5814 12.7605Z"/></g></svg>'
FAVICON_LINK='<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,'+quote(FAVICON_SVG)+'">'

'''

footer = '''
BODY=STYLE+BODYTOP+SCRIPT.replace('__DATA__',DATA)
standalone=('<!doctype html><html lang="en"><head><meta charset="utf-8">'
 '<meta name="viewport" content="width=device-width,initial-scale=1">'
 '<title>MonstarX Japan MCP | Live</title>'
 +FAVICON_LINK+
 '<meta name="description" content="Japan government open data as 27 MCP tools any AI agent can call. Live in-browser playground: weather, earthquakes, geocoding, holidays, shelters, tourism, open data.">'
 +STYLE+'</head><body>'+BODYTOP+SCRIPT.replace('__DATA__',DATA)+'</body></html>')
os.makedirs(os.path.join(REPO,'public'),exist_ok=True)
open(os.path.join(REPO,'japan-mcp-playground.html'),'w',encoding='utf-8').write(standalone)
open(os.path.join(REPO,'public','index.html'),'w',encoding='utf-8').write(standalone)
open(os.path.join(REPO,'public','favicon.svg'),'w',encoding='utf-8').write(FAVICON_SVG)
print('wrote public/index.html and japan-mcp-playground.html ('+str(len(standalone))+' bytes)')
'''

out = header + py_triple("STYLE", STYLE, raw=True) + "\n" + py_triple("BODYTOP", BODYTOP, raw=False) + "\n" + py_triple("SCRIPT", SCRIPT, raw=True) + footer
ROOT.joinpath("build.py").write_text(out, encoding="utf-8")
print("wrote build/build.py", len(out), "chars")
