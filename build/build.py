#!/usr/bin/env python3
"""Generate the MonstarX Philippines MCP playground HTML from tool metadata.

Run from anywhere:  python build/build.py
Reads:  build/data.min.json  (tool schemas + captured example responses)
Writes: public/index.html  and  philippines-mcp-playground.html  (identical)
"""
import os
from urllib.parse import quote
BASE=os.path.dirname(os.path.abspath(__file__))
REPO=os.path.dirname(BASE)
DATA=open(os.path.join(BASE,'data.min.json'),encoding='utf-8').read()
FAVICON_SVG='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" fill="#0d0d0d"/><g fill="#fff" transform="translate(1 1)"><path fill-rule="evenodd" d="M29.3493 25.3568L20.5472 16.5546L16.5546 20.5472L25.3568 29.3493L29.3493 25.3568ZM8.76813 12.7607L12.7607 8.76813L3.99257 0L0 3.99257L8.76813 12.7607ZM9.03679e-07 25.3568L8.8024 16.5543L12.795 20.5469L3.99257 29.3493L9.03679e-07 25.3568ZM20.5814 12.7605L16.5889 8.7679L25.3568 0L29.3493 3.99257L20.5814 12.7605Z"/></g></svg>'
FAVICON_LINK='<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,'+quote(FAVICON_SVG)+'">'

STYLE = r"""
<style>
:root{
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"Apple Color Emoji",sans-serif;
  --mono:ui-monospace,"SF Mono",SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace;
  --bg:#ffffff;--bg-sub:#fafafa;--panel:#ffffff;--panel-2:#f5f5f5;
  --border:#ececec;--border-2:#e0e0e0;--shadow:0 1px 2px rgba(13,13,13,.05),0 10px 30px -14px rgba(13,13,13,.14);
  --text:#0d0d0d;--muted:#5f5f66;--faint:#9b9ba2;
  --accent:#dc2626;--accent-ink:#b91c1c;--accent-weak:#fef2f2;--accent-2:#ef4444;
  --code-bg:#0d0d0f;--code-text:#e8e8ec;--code-border:#1c1c22;
  --k-key:#7ee3ff;--k-str:#9ff0a8;--k-num:#ffd479;--k-bool:#ff9db1;--k-null:#c9a0ff;
  --ok:#16a34a;--ok-bg:#f0fdf4;--warn:#c2780a;--err:#dc2626;
  --dot-catalog:#64748b;--dot-weather:#16a34a;--dot-hazards:#dc2626;--dot-geo:#0891b2;--dot-admin:#0d9488;--dot-civic:#7c3aed;--dot-places:#db2777;--dot-transport:#2563eb;--dot-finance:#ea580c;--dot-news:#ca8a04;--dot-nature:#15803d;
}
@media (prefers-color-scheme:dark){:root{
  --bg:#0a0a0b;--bg-sub:#0c0c0e;--panel:#0f0f12;--panel-2:#16161a;
  --border:#232327;--border-2:#2e2e34;--shadow:0 1px 2px rgba(0,0,0,.5),0 14px 36px -18px rgba(0,0,0,.75);
  --text:#f2f2f4;--muted:#9a9aa4;--faint:#68686f;
  --accent:#ef4444;--accent-ink:#f87171;--accent-weak:#2a1315;--accent-2:#f87171;
  --code-bg:#0b0b0e;--code-text:#e8e8ec;--code-border:#20202a;--ok-bg:#0e1c12;--accent-weak:#2a1315;
}}
:root[data-theme="dark"]{
  --bg:#0a0a0b;--bg-sub:#0c0c0e;--panel:#0f0f12;--panel-2:#16161a;
  --border:#232327;--border-2:#2e2e34;--shadow:0 1px 2px rgba(0,0,0,.5),0 14px 36px -18px rgba(0,0,0,.75);
  --text:#f2f2f4;--muted:#9a9aa4;--faint:#68686f;
  --accent:#ef4444;--accent-ink:#f87171;--accent-weak:#2a1315;--accent-2:#f87171;
  --code-bg:#0b0b0e;--code-text:#e8e8ec;--code-border:#20202a;--ok-bg:#0e1c12;
}
:root[data-theme="light"]{
  --bg:#ffffff;--bg-sub:#fafafa;--panel:#ffffff;--panel-2:#f5f5f5;
  --border:#ececec;--border-2:#e0e0e0;--text:#0d0d0d;--muted:#5f5f66;--faint:#9b9ba2;
  --accent:#dc2626;--accent-ink:#b91c1c;--accent-weak:#fef2f2;--accent-2:#ef4444;
  --code-bg:#0d0d0f;--code-text:#e8e8ec;--code-border:#1c1c22;--ok-bg:#f0fdf4;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:76px}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{animation:none!important;transition:none!important}}
body{margin:0;background:var(--bg);color:var(--text);font-family:var(--sans);font-size:15px;line-height:1.6;
  -webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
a{color:inherit;text-decoration:none}
code,pre,kbd{font-family:var(--mono)}
::selection{background:var(--accent-weak);color:var(--accent-ink)}
svg.mx{width:1em;height:1em;display:block}

/* topbar */
.topbar{position:sticky;top:0;z-index:50;height:57px;display:flex;align-items:center;gap:16px;padding:0 20px;
  background:color-mix(in srgb,var(--bg) 80%,transparent);backdrop-filter:saturate(160%) blur(12px);border-bottom:1px solid var(--border)}
.brand{display:flex;align-items:center;gap:11px;white-space:nowrap;font-size:16px}
.brand .logo{font-size:24px;color:var(--text);display:grid;place-items:center}
.brand b{font-weight:700;letter-spacing:-.02em}
.brand .sep{color:var(--faint);font-weight:400}
.brand small{color:var(--faint);font-weight:500;font-size:13px}
.tb-nav{display:flex;gap:4px;margin-left:8px}
.tb-nav a{padding:7px 11px;border-radius:8px;font-size:13.5px;color:var(--muted);font-weight:500}
.tb-nav a:hover{background:var(--panel-2);color:var(--text)}
.tb-spacer{flex:1}
.endpoint-pill{display:flex;align-items:center;gap:8px;font-family:var(--mono);font-size:12px;color:var(--muted);
  background:var(--panel-2);border:1px solid var(--border);border-radius:8px;padding:6px 10px;max-width:320px;cursor:pointer}
.endpoint-pill .u{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.endpoint-pill:hover{border-color:var(--border-2);color:var(--text)}
.icon-btn{width:34px;height:34px;border-radius:8px;border:1px solid var(--border);background:var(--panel);color:var(--muted);
  display:grid;place-items:center;cursor:pointer;flex:none}
.icon-btn:hover{color:var(--text);border-color:var(--border-2)}
.menu-btn{display:none}

.layout{display:grid;grid-template-columns:284px minmax(0,1fr);align-items:start}
.sidebar{position:sticky;top:57px;height:calc(100vh - 57px);overflow-y:auto;overscroll-behavior:contain;
  border-right:1px solid var(--border);padding:18px 14px 60px;background:var(--bg-sub)}
.search{position:relative;margin-bottom:14px}
.search input{width:100%;padding:9px 11px 9px 32px;border-radius:9px;border:1px solid var(--border);background:var(--panel);
  color:var(--text);font-size:13.5px;font-family:var(--sans)}
.search input:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-weak)}
.search svg{position:absolute;left:10px;top:50%;transform:translateY(-50%);color:var(--faint)}
.nav-quick a{display:block;padding:6px 8px;border-radius:7px;font-size:13.5px;color:var(--muted);font-weight:500}
.nav-quick a:hover{background:var(--panel-2);color:var(--text)}
.nav-quick a.spot{color:var(--accent-ink);font-weight:600}
.nav-group{margin-bottom:2px}
.nav-h{display:flex;align-items:center;gap:8px;padding:12px 8px 5px;font-size:11px;font-weight:680;letter-spacing:.06em;
  text-transform:uppercase;color:var(--faint)}
.nav-h .dot{width:7px;height:7px;border-radius:50%;flex:none}
.nav a{display:flex;align-items:center;gap:8px;padding:5px 8px 5px 24px;border-radius:7px;font-size:13px;color:var(--muted);
  font-family:var(--mono);letter-spacing:-.01em}
.nav a:hover{background:var(--panel-2);color:var(--text)}
.nav a.active{background:var(--accent-weak);color:var(--accent-ink);font-weight:600}

.content{padding:0 clamp(20px,4vw,60px) 120px;max-width:1000px}
section{scroll-margin-top:76px}

/* hero */
.hero{padding:56px 0 40px}
.eyebrow{display:inline-flex;align-items:center;gap:9px;font-size:12px;font-weight:650;letter-spacing:.05em;
  text-transform:uppercase;color:var(--accent-ink)}
.eyebrow .logo{font-size:15px}
.hero h1{font-size:clamp(34px,5.2vw,58px);line-height:1.03;letter-spacing:-.03em;margin:20px 0 0;font-weight:760;
  text-wrap:balance;max-width:16ch}
.hero h1 .hl{color:var(--accent)}
.lede{font-size:19px;color:var(--muted);max-width:56ch;margin:20px 0 0;line-height:1.55}
.lede b{color:var(--text);font-weight:600}
.cta{display:flex;flex-wrap:wrap;gap:12px;margin-top:30px}
.btn{display:inline-flex;align-items:center;gap:9px;font-size:14.5px;font-weight:600;padding:11px 18px;border-radius:10px;
  cursor:pointer;border:1px solid transparent;font-family:var(--sans)}
.btn.primary{background:var(--accent);color:#fff;box-shadow:0 4px 14px -4px var(--accent)}
.btn.primary:hover{background:var(--accent-ink)}
.btn.ghost{background:var(--panel);color:var(--text);border-color:var(--border-2)}
.btn.ghost:hover{border-color:var(--faint)}
.stats{display:flex;flex-wrap:wrap;gap:0;margin-top:40px;border:1px solid var(--border);border-radius:14px;overflow:hidden}
.stat{flex:1;min-width:130px;padding:18px 20px;border-right:1px solid var(--border)}
.stat:last-child{border-right:none}
.stat .n{font-size:26px;font-weight:720;letter-spacing:-.02em}
.stat .l{font-size:12.5px;color:var(--muted);margin-top:2px}

h2{font-size:25px;letter-spacing:-.02em;margin:64px 0 6px;font-weight:700;scroll-margin-top:76px}
h2 .num{color:var(--accent);font-family:var(--mono);font-size:15px;font-weight:600;margin-right:12px}
.sec-blurb{color:var(--muted);margin:0 0 22px;max-width:66ch;font-size:15.5px}
h3{font-size:15px;margin:24px 0 10px;font-weight:640;color:var(--muted)}
p{max-width:68ch}

/* use-cases */
.uses{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:14px;margin:26px 0}
.use{border:1px solid var(--border);border-radius:13px;padding:18px;background:var(--panel);transition:border-color .15s,transform .15s}
.use:hover{border-color:var(--border-2);transform:translateY(-2px)}
.use .ico{font-size:22px}
.use h4{margin:12px 0 5px;font-size:15px;font-weight:640}
.use p{margin:0;font-size:13.5px;color:var(--muted)}
.use .tools{margin-top:11px;display:flex;flex-wrap:wrap;gap:5px}
.use .tools code{font-size:11px;background:var(--panel-2);border:1px solid var(--border);border-radius:6px;padding:2px 6px;color:var(--muted)}

/* PLAYGROUND */
.pg{border:1px solid var(--border-2);border-radius:18px;overflow:hidden;background:var(--panel);box-shadow:var(--shadow)}
.pg-top{padding:16px 18px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:10px;flex-wrap:wrap;background:var(--panel-2)}
.pg-top .lbl{font-size:12px;font-weight:650;letter-spacing:.05em;text-transform:uppercase;color:var(--faint);margin-right:2px}
.chip-ex{display:inline-flex;align-items:center;gap:7px;font-size:13px;font-weight:500;padding:7px 12px;border-radius:99px;
  border:1px solid var(--border-2);background:var(--panel);color:var(--text);cursor:pointer}
.chip-ex:hover{border-color:var(--accent);color:var(--accent-ink)}
.chip-ex .e{font-size:14px}
.pg-body{display:grid;grid-template-columns:240px minmax(0,1fr)}
.pg-list{border-right:1px solid var(--border);max-height:560px;overflow-y:auto;padding:8px;background:var(--bg-sub)}
.pg-list .gl{font-size:10.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--faint);
  padding:12px 8px 5px;display:flex;align-items:center;gap:7px}
.pg-list .gl .dot{width:6px;height:6px;border-radius:50%}
.pg-list button{display:block;width:100%;text-align:left;padding:6px 9px;border-radius:7px;border:none;background:none;
  font-family:var(--mono);font-size:12.5px;color:var(--muted);cursor:pointer}
.pg-list button:hover{background:var(--panel-2);color:var(--text)}
.pg-list button.sel{background:var(--accent-weak);color:var(--accent-ink);font-weight:600}
.pg-main{padding:20px 22px;min-width:0}
.pg-main .tn{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.pg-main .tn code{font-size:16px;font-weight:650}
.pg-main .td{color:var(--muted);margin:9px 0 0;font-size:14px}
.form{margin:18px 0 6px;display:grid;gap:12px}
.field{display:grid;grid-template-columns:150px 1fr;gap:12px;align-items:start}
.field label{font-family:var(--mono);font-size:13px;color:var(--text);padding-top:9px}
.field label .req{color:var(--accent);font-weight:700}
.field .ty{display:block;font-size:11px;color:var(--faint);font-family:var(--mono);margin-top:2px}
.field input,.field select,.field textarea{width:100%;padding:9px 11px;border-radius:9px;border:1px solid var(--border-2);
  background:var(--bg);color:var(--text);font-size:13.5px;font-family:var(--mono)}
.field input:focus,.field select:focus,.field textarea:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-weak)}
.field .hint{font-size:12px;color:var(--muted);margin-top:5px;font-family:var(--sans)}
.noparams{color:var(--faint);font-style:italic;font-size:13.5px;margin:16px 0}
.runbar{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-top:16px;padding-top:16px;border-top:1px solid var(--border)}
.run{display:inline-flex;align-items:center;gap:8px;background:var(--accent);color:#fff;border:none;font-weight:650;font-size:14px;
  padding:10px 18px;border-radius:10px;cursor:pointer;font-family:var(--sans)}
.run:hover{background:var(--accent-ink)}.run:disabled{opacity:.6;cursor:default}
.linkbtn{background:none;border:none;color:var(--muted);font-size:13px;cursor:pointer;font-family:var(--sans);padding:6px 8px;border-radius:7px}
.linkbtn:hover{color:var(--text);background:var(--panel-2)}
.resp{margin-top:16px}
.resp-meta{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:8px;font-size:12.5px;color:var(--muted)}
.pill{display:inline-flex;align-items:center;gap:6px;font-size:11.5px;font-weight:650;padding:3px 9px;border-radius:99px}
.pill.ok{color:var(--ok);background:var(--ok-bg)}
.pill.err{color:var(--err);background:var(--accent-weak)}
.pill .d{width:6px;height:6px;border-radius:50%;background:currentColor}
.tabs{display:inline-flex;gap:2px;background:var(--panel-2);border:1px solid var(--border);border-radius:8px;padding:2px}
.tabs button{border:none;background:none;font-size:12px;font-weight:600;color:var(--muted);padding:4px 10px;border-radius:6px;cursor:pointer;font-family:var(--sans)}
.tabs button.on{background:var(--bg);color:var(--text);box-shadow:0 1px 2px rgba(0,0,0,.1)}
.pg-note{margin:0;padding:11px 14px;background:var(--accent-weak);color:var(--accent-ink);font-size:13px;border-bottom:1px solid var(--border);display:none}
.pg-note.show{display:block}
.pg-note b{font-weight:700}

/* code */
.code{position:relative;background:var(--code-bg);border:1px solid var(--code-border);border-radius:11px;overflow:hidden}
.code .bar{display:flex;align-items:center;gap:8px;padding:8px 12px;border-bottom:1px solid var(--code-border);
  font-family:var(--mono);font-size:11.5px;color:#8b8b96}
.code .bar .dots{display:flex;gap:5px}.code .bar .dots i{width:9px;height:9px;border-radius:50%;background:#2d2d36}
.code pre{margin:0;padding:14px 16px;overflow-x:auto;font-size:12.7px;line-height:1.62;color:var(--code-text)}
.code.scroll pre{max-height:420px;overflow-y:auto}
.copy{position:absolute;top:7px;right:8px;z-index:2;font-family:var(--sans);font-size:11.5px;color:#b7b7c2;background:#1a1a22;
  border:1px solid #2a2a34;border-radius:7px;padding:4px 9px;cursor:pointer}
.copy:hover{color:#fff;background:#24242e}.copy.ok{color:#9ff0a8;border-color:#2f5c39}
.tok .key{color:var(--k-key)}.tok .str{color:var(--k-str)}.tok .num{color:var(--k-num)}
.tok .bool{color:var(--k-bool)}.tok .null{color:var(--k-null)}
.shc{color:#8b8b96}.shk{color:#ff9db1}.shs{color:#9ff0a8}.shu{color:#7ee3ff}

.card{background:var(--panel);border:1px solid var(--border);border-radius:14px;padding:18px 20px;margin:16px 0}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media (max-width:760px){.grid2{grid-template-columns:1fr}}
.mini-label{font-size:11px;font-weight:640;letter-spacing:.06em;text-transform:uppercase;color:var(--faint);margin:16px 0 7px}

/* tool cards */
.tool{background:var(--panel);border:1px solid var(--border);border-radius:14px;margin:16px 0;overflow:hidden;box-shadow:var(--shadow)}
.tool .head{padding:16px 20px}
.tool .tname{display:flex;align-items:center;gap:11px;flex-wrap:wrap}
.tool .tname code{font-size:15.5px;font-weight:650;color:var(--text)}
.badge{font-size:11px;font-weight:600;padding:3px 9px;border-radius:99px;display:inline-flex;align-items:center;gap:6px}
.badge.cat{color:var(--muted);background:var(--panel-2);border:1px solid var(--border)}
.badge.cat .dot{width:6px;height:6px;border-radius:50%}
.badge.np{color:var(--ok);background:var(--ok-bg)}
.tryit{margin-left:auto;display:inline-flex;align-items:center;gap:6px;font-size:12.5px;font-weight:600;color:var(--accent-ink);
  background:var(--accent-weak);border:1px solid transparent;border-radius:8px;padding:6px 11px;cursor:pointer;font-family:var(--sans)}
.tryit:hover{border-color:var(--accent)}
.tdesc{margin:12px 0 0;color:var(--muted);max-width:72ch}
.tool .body{padding:0 20px 18px}
.ptable{width:100%;border-collapse:collapse;margin:8px 0 4px;font-size:13px}
.ptable th{text-align:left;font-weight:600;color:var(--faint);font-size:11px;letter-spacing:.05em;text-transform:uppercase;
  padding:7px 10px;border-bottom:1px solid var(--border)}
.ptable td{padding:8px 10px;border-bottom:1px solid var(--border);vertical-align:top;color:var(--muted)}
.ptable tr:last-child td{border-bottom:none}
.ptable td.pn{font-family:var(--mono);color:var(--text);white-space:nowrap}
.ptable .req{color:var(--accent);font-weight:700;margin-left:3px}
.ptable td.pt{font-family:var(--mono);color:var(--faint);font-size:12px;white-space:nowrap}
.noparam{color:var(--faint);font-size:13px;font-style:italic;margin:10px 0 2px}
details.ex{margin-top:12px;border-top:1px solid var(--border);padding-top:6px}
details.ex summary{cursor:pointer;font-size:12.5px;font-weight:600;color:var(--muted);padding:8px 0;list-style:none;display:flex;align-items:center;gap:7px}
details.ex summary::-webkit-details-marker{display:none}
details.ex summary::before{content:"";width:0;height:0;border-left:5px solid var(--faint);border-top:4px solid transparent;border-bottom:4px solid transparent;transition:transform .15s}
details.ex[open] summary::before{transform:rotate(90deg)}
details.ex summary:hover{color:var(--text)}

footer{border-top:1px solid var(--border);padding:40px clamp(20px,4vw,60px) 64px;color:var(--muted);font-size:13.5px}
footer .top{display:flex;align-items:center;gap:12px;margin-bottom:24px;font-size:17px}
footer .top .logo{font-size:22px}
footer .cols{display:flex;flex-wrap:wrap;gap:44px}
footer h4{font-size:12px;letter-spacing:.05em;text-transform:uppercase;color:var(--faint);margin:0 0 10px}
footer a{color:var(--accent-ink)}
footer a:hover{text-decoration:underline}
.disc{margin-top:26px;font-size:12.5px;color:var(--faint);max-width:88ch;line-height:1.55}
.tag{display:inline-block;font-size:11px;font-family:var(--mono);color:var(--warn);background:color-mix(in srgb,var(--warn) 13%,transparent);padding:2px 8px;border-radius:6px}
.scrim{position:fixed;inset:57px 0 0;background:rgba(0,0,0,.4);z-index:45;display:none}
/* severity + map palette */
:root{--sv-good:#16a34a;--sv-mod:#ca8a04;--sv-high:#ea580c;--sv-vhigh:#dc2626;--sv-ext:#7c3aed;--map-bg:#eef3f0;--map-land:#dde9e0;--map-stroke:#bcd0c3}
@media (prefers-color-scheme:dark){:root{--sv-good:#22c55e;--sv-mod:#eab308;--sv-high:#f97316;--sv-vhigh:#f87171;--sv-ext:#a78bfa;--map-bg:#0d1311;--map-land:#17221b;--map-stroke:#26332a}}
:root[data-theme="dark"]{--sv-good:#22c55e;--sv-mod:#eab308;--sv-high:#f97316;--sv-vhigh:#f87171;--sv-ext:#a78bfa;--map-bg:#0d1311;--map-land:#17221b;--map-stroke:#26332a}
:root[data-theme="light"]{--sv-good:#16a34a;--sv-mod:#ca8a04;--sv-high:#ea580c;--sv-vhigh:#dc2626;--sv-ext:#7c3aed;--map-bg:#eef3f0;--map-land:#dde9e0;--map-stroke:#bcd0c3}
/* sample data + ask */
.ask{display:flex;align-items:flex-start;gap:7px;margin:11px 0 2px;font-size:13.5px;color:var(--muted)}
.ask .q{font-style:italic;color:var(--text)}
.presets{display:flex;flex-wrap:wrap;gap:7px;align-items:center;margin:15px 0 2px}
.presets .pl{font-size:11px;font-weight:650;letter-spacing:.05em;text-transform:uppercase;color:var(--faint);margin-right:2px}
.preset{font-size:12.5px;font-weight:500;padding:6px 11px;border-radius:99px;border:1px solid var(--border-2);background:var(--panel);color:var(--text);cursor:pointer;font-family:var(--sans)}
.preset:hover{border-color:var(--accent);color:var(--accent-ink)}
.samples{display:flex;flex-wrap:wrap;gap:5px;margin-top:7px}
.samp{font-size:11.5px;font-family:var(--mono);padding:3px 8px;border-radius:6px;border:1px dashed var(--border-2);background:transparent;color:var(--muted);cursor:pointer}
.samp:hover{border-style:solid;border-color:var(--accent);color:var(--accent-ink)}
/* visual renderers */
.vis{font-size:14px;animation:vfade .25s ease}
@keyframes vfade{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}
.vhead{font-size:12.5px;font-weight:600;color:var(--muted);margin:2px 0 12px}
.vstat{display:inline-block;padding:16px 22px;border:1px solid var(--border);border-radius:14px;background:var(--panel-2);min-width:150px}
.vstat .bn{font-size:34px;font-weight:760;letter-spacing:-.02em;line-height:1}
.vstat .bl{font-size:13px;color:var(--muted);margin-top:6px}.vstat .bs{font-size:12px;color:var(--faint);margin-top:3px}
.statrow{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:12px}
.wxgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(116px,1fr));gap:8px;max-height:360px;overflow:auto}
.wx{border:1px solid var(--border);border-radius:11px;padding:11px;text-align:center;background:var(--panel-2)}
.wx .e{font-size:24px}.wx .a{font-size:12px;font-weight:600;margin-top:5px}.wx .f{font-size:11.5px;color:var(--muted);margin-top:2px}
.wxbig{display:flex;align-items:center;gap:16px;border:1px solid var(--border);border-radius:14px;padding:16px 20px;background:var(--panel-2);margin-bottom:12px}
.wxbig .e{font-size:44px}.wxbig .bf{font-size:19px;font-weight:680}.wxbig .bm{font-size:13px;color:var(--muted);margin-top:4px}
.daygrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px}
.day{border:1px solid var(--border);border-radius:13px;padding:14px;text-align:center;background:var(--panel-2)}
.day .dd{font-size:12.5px;font-weight:600;color:var(--muted)}.day .e{font-size:32px;margin:6px 0}.day .dt{font-size:17px;font-weight:700}.day .df{font-size:12px;color:var(--muted);margin-top:4px}
.gauge{border:1px solid var(--border);border-radius:14px;padding:16px 20px;background:var(--panel-2)}
.gauge .gv{font-size:36px;font-weight:760}.gauge .gv small{font-size:15px;font-weight:600}
.gauge .gbar{height:10px;border-radius:99px;background:var(--border);margin-top:10px;overflow:hidden}.gauge .gbar i{display:block;height:100%;border-radius:99px}
.rgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(108px,1fr));gap:10px}
.rc{border:1px solid var(--border);border-radius:12px;padding:14px;text-align:center;background:var(--panel-2)}
.rc .rn{font-size:11px;text-transform:uppercase;letter-spacing:.05em;color:var(--faint)}
.rc .rv{font-size:30px;font-weight:760;line-height:1.1}.rc .rs{font-size:12px;font-weight:600}.rc .rp{font-size:11px;color:var(--muted);margin-top:3px}
.vt{width:100%;border-collapse:collapse;font-size:13px;margin-top:4px}
.vtwrap{max-height:430px;overflow:auto;border:1px solid var(--border);border-radius:12px}
.vt th{text-align:left;font-size:11px;letter-spacing:.04em;text-transform:uppercase;color:var(--faint);padding:9px 11px;border-bottom:1px solid var(--border);position:sticky;top:0;background:var(--panel);z-index:1}
.vt td{padding:9px 11px;border-bottom:1px solid var(--border);color:var(--muted);vertical-align:top}
.vt tr:last-child td{border-bottom:none}.vt td b{color:var(--text)}.vt td.r,.vt th.r{text-align:right;font-variant-numeric:tabular-nums}
.vt td .sub{font-size:11.5px;color:var(--faint)}.vt td.mono{font-family:var(--mono)}
.sp{font-size:11.5px;font-weight:600;padding:2px 9px;border-radius:99px;color:var(--c);background:color-mix(in srgb,var(--c) 15%,transparent)}
.vbanner{padding:12px 15px;border-radius:11px;font-weight:600;font-size:14px;margin-bottom:12px}
.vbanner.ok{background:color-mix(in srgb,var(--sv-good) 15%,transparent);color:var(--sv-good)}
.vbanner.no{background:var(--accent-weak);color:var(--accent-ink)}
.ccard{border:1px solid var(--border);border-radius:13px;padding:16px 18px;background:var(--panel-2)}
.ccard .cn{font-size:16px;font-weight:680;margin-bottom:6px}
.ccard .cg{display:flex;gap:12px;padding:7px 0;border-top:1px solid var(--border);font-size:13.5px}
.ccard .cg span{color:var(--faint);min-width:120px}.ccard .cg b{color:var(--text)}
.chiprow{display:flex;flex-wrap:wrap;gap:7px}.yc{font-family:var(--mono);font-size:12.5px;padding:4px 10px;border-radius:7px;background:var(--panel-2);border:1px solid var(--border)}
.cpgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:10px;max-height:430px;overflow:auto}
.cpk{border:1px solid var(--border);border-radius:12px;padding:13px 15px;background:var(--panel-2)}
.cpk .cpn{font-family:var(--mono);font-weight:650}.cpk .cpa{font-size:12px;color:var(--muted);margin:4px 0;line-height:1.4}.cpk .cpl{font-size:16px;font-weight:700}.cpk .cpt{font-size:11px;color:var(--faint);margin-top:3px}
.buscols{display:grid;grid-template-columns:repeat(auto-fit,minmax(148px,1fr));gap:10px}
.busc{border:1px solid var(--border);border-radius:12px;padding:13px 15px;background:var(--panel-2)}
.busc .bs2{font-size:20px;font-weight:760}.busc .bb{display:flex;gap:6px;flex-wrap:wrap;margin:8px 0 4px}.busc .bo{font-size:11px;color:var(--faint)}
.bt{display:inline-flex;align-items:center;gap:5px;font-size:12px;font-weight:600;padding:3px 8px;border-radius:7px;background:var(--panel);border:1px solid var(--border)}
.bt i{width:6px;height:6px;border-radius:50%}.bt.none{color:var(--faint)}
.ilist,.dlist{list-style:none;padding:0;margin:12px 0 0;display:grid;gap:7px;max-height:340px;overflow:auto}
.ilist li{font-size:13px;color:var(--muted);padding:9px 12px;border:1px solid var(--border);border-radius:10px;background:var(--panel-2)}
.ilist .tt{font-weight:650;color:var(--text);margin-right:6px}
.dlist li{display:flex;align-items:flex-start;gap:10px;font-size:13px;padding:9px 12px;border:1px solid var(--border);border-radius:10px;background:var(--panel-2)}
.cs{flex:none;font-weight:700;font-size:13px;min-width:30px;text-align:center;color:var(--c);background:color-mix(in srgb,var(--c) 16%,transparent);border-radius:7px;padding:2px 6px}
.vmap{border:1px solid var(--border);border-radius:14px;overflow:hidden;background:var(--map-bg)}
.vmap svg{width:100%;height:auto;display:block}
.vmap .pv{font-size:19px;font-weight:700;fill:var(--text);paint-order:stroke;stroke:var(--map-bg);stroke-width:5px;text-anchor:middle}
.vlist{list-style:none;padding:0;margin:12px 0 0;display:grid;gap:6px;max-height:210px;overflow:auto}
.vlist li{font-size:13px;color:var(--muted)}.vlist li b{color:var(--text)}.vlist li em{color:var(--accent-ink);font-style:normal;font-weight:600}
.vlist .dotp{display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--accent);margin-right:7px}
.vnote{font-size:12px;color:var(--faint);margin-top:8px}

@media (max-width:1000px){.pg-body{grid-template-columns:1fr}.pg-list{max-height:200px;border-right:none;border-bottom:1px solid var(--border);
  display:flex;flex-wrap:wrap;gap:4px}.pg-list .gl{width:100%}}
@media (max-width:900px){
  .layout{grid-template-columns:1fr}
  .sidebar{position:fixed;top:57px;left:0;width:284px;z-index:46;transform:translateX(-104%);transition:transform .22s ease;box-shadow:var(--shadow)}
  .sidebar.open{transform:none}
  .menu-btn{display:grid}.endpoint-pill,.tb-nav{display:none}
  .scrim.open{display:block}
  .field{grid-template-columns:1fr}.field label{padding-top:0}
}

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
</style>
"""

BODYTOP = """
<div class="topbar">
  <button class="icon-btn menu-btn" id="menuBtn" aria-label="Menu"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button>
  <a class="brand" href="#top"><span class="logo"><svg class="mx" viewBox="0 0 30 30" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M29.3493 25.3568L20.5472 16.5546L16.5546 20.5472L25.3568 29.3493L29.3493 25.3568ZM8.76813 12.7607L12.7607 8.76813L3.99257 0L0 3.99257L8.76813 12.7607ZM9.03679e-07 25.3568L8.8024 16.5543L12.795 20.5469L3.99257 29.3493L9.03679e-07 25.3568ZM20.5814 12.7605L16.5889 8.7679L25.3568 0L29.3493 3.99257L20.5814 12.7605Z"/></svg></span><b>MonstarX</b><span class="sep">·</span><small>Philippines&nbsp;MCP</small></a>
  <nav class="tb-nav">
    <a href="#playground" data-i18n="navPlayground">Playground</a>
    <a href="#reference" data-i18n="navTools">Tools</a>
    <a href="#quickstart" data-i18n="navConnect">Connect</a>
  </nav>
  <div class="tb-spacer"></div>
  <div class="endpoint-pill" id="epPill" title="Copy MCP endpoint">
    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
    <span class="u">ph-mcp-staging.monstarxapp.com/mcp</span>
  </div>
  <button class="icon-btn" id="themeBtn" aria-label="Toggle theme"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.8A9 9 0 1 1 11.2 3 7 7 0 0 0 21 12.8z"/></svg></button>
  <div class="lang-wrap">
    <button type="button" class="lang-btn" id="langBtn" aria-haspopup="listbox" aria-expanded="false" title="Language">
      <span aria-hidden="true">🌐</span><span id="langBtnLabel">EN</span><span class="chev">▾</span>
    </button>
    <div class="lang-menu" id="langMenu" role="listbox">
      <button type="button" data-lang="en" role="option">🇺🇸 English</button>
      <button type="button" data-lang="tl" role="option">🇵🇭 Filipino</button>
    </div>
  </div>
</div>
<div class="layout" id="top">
  <div class="scrim" id="scrim"></div>
  <aside class="sidebar" id="sidebar">
    <div class="search"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>
      <input id="filter" type="text" data-i18n-placeholder="filterTools" placeholder="Filter tools…" autocomplete="off" spellcheck="false"></div>
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
      <span class="eyebrow"><span class="logo"><svg class="mx" viewBox="0 0 30 30" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M29.3493 25.3568L20.5472 16.5546L16.5546 20.5472L25.3568 29.3493L29.3493 25.3568ZM8.76813 12.7607L12.7607 8.76813L3.99257 0L0 3.99257L8.76813 12.7607ZM9.03679e-07 25.3568L8.8024 16.5543L12.795 20.5469L3.99257 29.3493L9.03679e-07 25.3568ZM20.5814 12.7605L16.5889 8.7679L25.3568 0L29.3493 3.99257L20.5814 12.7605Z"/></svg></span> <span data-i18n="eyebrow">MonstarX · Philippines MCP</span></span>
      <h1 data-i18n-html="heroTitle">The Philippines' public data, <span class="hl">ready for your AI</span>.</h1>
      <p class="lede" data-i18n-html="heroLede">Weather, earthquakes, geocoding, postal codes, holidays, evacuation shelters, tourism, FX, HDX open datasets — Philippine public APIs live across many agencies, each with its own formats and quirks. <b>MonstarX unifies them into MCP tools any AI agent can call</b>, through one endpoint, with no API keys. Stop writing integration glue. Start shipping Philippines-smart products.</p>
      <div class="cta">
        <a class="btn primary" href="#playground" data-i18n="ctaTry">▶ Try it live in your browser</a>
        <a class="btn ghost" href="#quickstart" data-i18n="ctaConnect">Connect Claude or Cursor</a>
      </div>
      <div class="stats">
        <div class="stat"><div class="n" id="statToolN">70</div><div class="l" data-i18n="statTools">ready-made tools</div></div>
        <div class="stat"><div class="n">12</div><div class="l" data-i18n="statSources">free public sources</div></div>
        <div class="stat"><div class="n">0</div><div class="l" data-i18n="statKeys">API keys or signup</div></div>
        <div class="stat"><div class="n" data-i18n="statLiveN">Live</div><div class="l" data-i18n="statLive">real-time data</div></div>
      </div>
    </section>

    <section id="playground">
      <h2><span class="num">▶</span><span data-i18n="secPlayground">Live playground</span></h2>
      <p class="sec-blurb" data-i18n-html="secPlaygroundBlurb">Pick a tool, tweak the inputs, hit <b>Run</b> — the query goes straight to the live MCP server and streams back real Philippines data. No sign-up, nothing to install. Try a one-click example to start:</p>
      <div class="pg">
        <div class="pg-note" id="pgNote"></div>
        <div class="pg-top">
          <span class="lbl" data-i18n="tryLabel">Try</span>
          <button class="chip-ex" data-ex="wx24" data-i18n-chip="chipWx"><span class="e">⛅</span> Manila weather 24h</button>
          <button class="chip-ex" data-ex="quake" data-i18n-chip="chipQuake"><span class="e">🌋</span> Recent quakes</button>
          <button class="chip-ex" data-ex="geo" data-i18n-chip="chipGeo"><span class="e">📍</span> Geocode Intramuros</button>
          <button class="chip-ex" data-ex="postal" data-i18n-chip="chipPostal"><span class="e">✉️</span> Postal 1000</button>
          <button class="chip-ex" data-ex="holiday" data-i18n-chip="chipHoliday"><span class="e">🇵🇭</span> Holidays 2026</button>
          <button class="chip-ex" data-ex="shelter" data-i18n-chip="chipShelter"><span class="e">🏫</span> Shelters · Manila</button>
          <button class="chip-ex" data-ex="tourism" data-i18n-chip="chipTourism"><span class="e">🏝️</span> Tourism near Manila</button>
          <button class="chip-ex" data-ex="datasets" data-i18n-chip="chipDatasets"><span class="e">📚</span> Search typhoon datasets</button>
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
        <div class="use"><div class="ico">⛅</div><h4 data-i18n="useWxT">Weather-aware apps</h4><p data-i18n="useWxP">City codes, 24h/4-day forecasts, UV, rain, humidity, and air quality for Manila, Cebu, Davao, and more.</p><div class="tools"><code>ph_weather_24h</code><code>ph_weather_warnings</code><code>ph_uv_index</code></div></div>
        <div class="use"><div class="ico">🌋</div><h4 data-i18n="useDisT">Disaster awareness</h4><p data-i18n="useDisP">Surface recent earthquakes, tsunami lists, volcanoes, and nearby evacuation points.</p><div class="tools"><code>ph_earthquake_list</code><code>ph_tsunami_list</code><code>ph_evacuation_shelters</code></div></div>
        <div class="use"><div class="ico">📍</div><h4 data-i18n="useMapT">Maps &amp; addressing</h4><p data-i18n="useMapP">Search places, geocode, reverse-geocode, resolve ZIP codes, and read elevation — no keys.</p><div class="tools"><code>ph_geocode</code><code>ph_postal_code</code><code>ph_elevation</code></div></div>
        <div class="use"><div class="ico">🏝️</div><h4 data-i18n="useTourT">Travel &amp; tourism</h4><p data-i18n="useTourP">Find nearby attractions from OpenStreetMap and pair with holiday calendars.</p><div class="tools"><code>ph_tourism_spots</code><code>ph_public_holidays</code></div></div>
        <div class="use"><div class="ico">📈</div><h4 data-i18n="useFinT">FX &amp; markets</h4><p data-i18n="useFinP">USD/PHP rates, bank directory, gold, crypto in pesos, and PSE quotes.</p><div class="tools"><code>ph_bsp_finance</code><code>ph_pse_quote</code></div></div>
        <div class="use"><div class="ico">📚</div><h4 data-i18n="useDataT">Open data explorer</h4><p data-i18n="useDataP">Search HDX Philippines packages, inspect metadata, and query datastore tables.</p><div class="tools"><code>ph_datasets_search</code><code>ph_dataset_query</code></div></div>
      </div>
    </section>

    <section id="quickstart">
      <h2><span class="num">02</span><span data-i18n="secConnect">Connect your agent</span></h2>
      <p class="sec-blurb" data-i18n="secConnectBlurb">MonstarX Philippines MCP is a remote HTTP server speaking the Model Context Protocol. Point any MCP-capable client at the endpoint — no auth handshake, it's stateless.</p>
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
        <tr><td class="pn">source</td><td data-i18n="fSource">Upstream platform — Open-Meteo, USGS, OSM, HDX, PSA, Nager.Date, etc.</td></tr>
        <tr><td class="pn">agency</td><td data-i18n="fAgency">Originating body — PAGASA-compatible feeds, USGS, PSA, HDX, …</td></tr>
        <tr><td class="pn">api</td><td data-i18n="fApi">The specific upstream API that was queried.</td></tr>
        <tr><td class="pn">license</td><td data-i18n="fLicense">Data licence / terms note when applicable.</td></tr>
        <tr><td class="pn">retrieved_at</td><td data-i18n="fRetrieved">Server fetch time (UTC). Live timestamps inside payloads are often PHT (+08:00).</td></tr>
        <tr><td class="pn">data / results</td><td data-i18n-html="fData">The payload. List tools add context like <code>total</code>, <code>shown</code>, <code>found</code>.</td></tr>
      </tbody></table></div>
    </section>

    <section id="errors">
      <h2><span class="num">04</span><span data-i18n="secErrors">Errors</span></h2>
      <p class="sec-blurb" data-i18n-html="secErrorsBlurb">Errors come back as a normal result with <code>isError: true</code> and a message in <code>content[0].text</code> — not as a transport-level failure. Invalid or missing arguments return MCP error <code>-32602</code>. An empty list is a valid "no matches", not an error.</p>
      __CB_ERR__
    </section>

    <section id="reference">
      <h2><span class="num">05</span><span data-i18n="secTools">All tools</span></h2>
      <p class="sec-blurb" data-i18n-html="secToolsBlurb">Every tool is prefixed <code>ph_</code>; required params are marked <span style="color:var(--accent)">*</span>. Hit <b>Try in playground</b> on any tool to load it above with a working example.</p>
      <div id="tools"></div>
    </section>

    <footer>
      <div class="top"><span class="logo"><svg class="mx" viewBox="0 0 30 30" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M29.3493 25.3568L20.5472 16.5546L16.5546 20.5472L25.3568 29.3493L29.3493 25.3568ZM8.76813 12.7607L12.7607 8.76813L3.99257 0L0 3.99257L8.76813 12.7607ZM9.03679e-07 25.3568L8.8024 16.5543L12.795 20.5469L3.99257 29.3493L9.03679e-07 25.3568ZM20.5814 12.7605L16.5889 8.7679L25.3568 0L29.3493 3.99257L20.5814 12.7605Z"/></svg></span> <b>MonstarX</b> <span style="color:var(--faint)">Philippines MCP</span></div>
      <div class="cols">
        <div><h4 data-i18n="ftSources">Data sources</h4><div><a href="https://open-meteo.com/">Open-Meteo</a> · weather, UV, AQI, marine</div><div><a href="https://earthquake.usgs.gov/">USGS</a> · earthquakes in PH bbox</div><div><a href="https://www.openstreetmap.org/">OpenStreetMap</a> · places, POIs, shelters</div><div><a href="https://data.humdata.org/">HDX</a> · Philippines open catalog</div><div><a href="https://psa.gov.ph/">PSA / Nager.Date</a> · stats &amp; holidays</div></div>
        <div><h4 data-i18n="ftEndpoints">Endpoints</h4><div style="font-family:var(--mono);font-size:12.5px">GET&nbsp; /</div><div style="font-family:var(--mono);font-size:12.5px">GET&nbsp; /health</div><div style="font-family:var(--mono);font-size:12.5px">POST /mcp</div></div>
        <div><h4 data-i18n="ftServer">Server</h4><div>MonstarX Philippines MCP · v0.1.0</div><div>Protocol <code>2025-06-18</code> · <span class="tag">staging</span></div><div><a href="https://monstarx.com">monstarx.com</a></div></div>
      </div>
      <p class="disc" data-i18n="ftDisc">Data remains subject to each source's terms (Open-Meteo, USGS, OSM, HDX, PSA, Nager.Date, Zippopotam.us). You are responsible for complying with the source licences. MonstarX is an independent wrapper and is not endorsed by any government agency. This is a staging deployment — don't build production load on it. Example payloads captured for documentation 2026-08-27.</p>
    </footer>
  </main>
</div>
"""

SCRIPT = r"""
<script id="apidata" type="application/json">__DATA__</script>
<script>
const DATA=JSON.parse(document.getElementById('apidata').textContent);
(function(){const n=Object.keys(DATA.tools||{}).length;const el=document.getElementById('statToolN');if(el)el.textContent=String(n);const f=document.getElementById('filter');if(f&&f.placeholder)f.placeholder='Filter '+n+' tools…';})();
const EP='https://ph-mcp-staging.monstarxapp.com';
function liveBase(){
  try{const q=new URLSearchParams(location.search).get('mcp');if(q)return q.replace(/\/$/,'');}catch(e){}
  try{const s=localStorage.getItem('mcp_ep');if(s)return s.replace(/\/$/,'');}catch(e){}
  if(location.protocol==='http:'||location.protocol==='https:')return '';
  return EP;
}
let LANG=localStorage.getItem('mx-lang-ph')||'en';

const I18N={
en:{
navPlayground:'Playground',navTools:'Tools',navConnect:'Connect',
navLivePg:'▶ Live playground',navUseCases:'What you can build',navConnectAgent:'Connect your agent',navResponse:'Response format',navErrors:'Errors',
filterTools:'Filter tools…',eyebrow:'MonstarX · Philippines MCP',
heroTitle:"The Philippines' public data, <span class=\"hl\">ready for your AI</span>.",
heroLede:"Weather, earthquakes, geocoding, postal codes, holidays, evacuation shelters, tourism, FX, HDX open datasets — Philippine public APIs live across many agencies, each with its own formats and quirks. <b>MonstarX unifies them into MCP tools any AI agent can call</b>, through one endpoint, with no API keys. Stop writing integration glue. Start shipping Philippines-smart products.",
ctaTry:'▶ Try it live in your browser',ctaConnect:'Connect Claude or Cursor',
statTools:'ready-made tools',statSources:'free public sources',statKeys:'API keys or signup',statLiveN:'Live',statLive:'real-time data',
secPlayground:'Live playground',
secPlaygroundBlurb:'Pick a tool, tweak the inputs, hit <b>Run</b> — the query goes straight to the live MCP server and streams back real Philippines data. No sign-up, nothing to install. Try a one-click example to start:',
tryLabel:'Try',
chipWx:'Manila weather 24h',chipQuake:'Recent quakes',chipGeo:'Geocode Intramuros',chipPostal:'Postal 1000',
chipHoliday:'Holidays 2026',chipShelter:'Shelters · Manila',chipTourism:'Tourism near Manila',chipDatasets:'Search typhoon datasets',
secUse:'What you can build',secUseBlurb:'A weekend hackathon or a production feature — these are all a few tool calls away.',
useWxT:'Weather-aware apps',useWxP:'City codes, 24h/4-day forecasts, UV, rain, humidity, and air quality for Manila, Cebu, Davao, and more.',
useDisT:'Disaster awareness',useDisP:'Surface recent earthquakes, tsunami lists, volcanoes, and nearby evacuation points.',
useMapT:'Maps & addressing',useMapP:'Search places, geocode, reverse-geocode, resolve ZIP codes, and read elevation — no keys.',
useTourT:'Travel & tourism',useTourP:'Find nearby attractions from OpenStreetMap and pair with holiday calendars.',
useFinT:'FX & markets',useFinP:'USD/PHP rates, bank directory, gold, crypto in pesos, and PSE quotes.',
useDataT:'Open data explorer',useDataP:'Search HDX Philippines packages, inspect metadata, and query datastore tables.',
secConnect:'Connect your agent',
secConnectBlurb:'MonstarX Philippines MCP is a remote HTTP server speaking the Model Context Protocol. Point any MCP-capable client at the endpoint — no auth handshake, it\'s stateless.',
labClaude:'Claude Code',labCursor:'Cursor / native HTTP clients',
labDesk:'Claude Desktop — <span style="text-transform:none;letter-spacing:0;font-weight:400;color:var(--faint)">claude_desktop_config.json</span>',
labCurl:'Or just cURL it',
secResponse:'Response format',
secResponseBlurb:'Every call returns the payload twice — as a JSON string in <code>content[0].text</code> and as a parsed object in <code>structuredContent</code> (prefer this). Each payload wraps the data in a consistent provenance envelope so your agent always knows the source, agency and freshness.',
thField:'Field',thMeaning:'Meaning',
fSource:'Upstream platform — Open-Meteo, USGS, OSM, HDX, PSA, Nager.Date, etc.',
fAgency:'Originating body — PAGASA-compatible feeds, PHIVOLCS-adjacent USGS, PSA, …',
fApi:'The specific upstream API that was queried.',
fLicense:'Data licence / terms note when applicable.',
fRetrieved:'Server fetch time (UTC). Live timestamps inside payloads are often PHT (+08:00).',
fData:'The payload. List tools add context like <code>total</code>, <code>shown</code>, <code>found</code>.',
secErrors:'Errors',
secErrorsBlurb:'Errors come back as a normal result with <code>isError: true</code> and a message in <code>content[0].text</code> — not as a transport-level failure. Invalid or missing arguments return MCP error <code>-32602</code>. An empty list is a valid "no matches", not an error.',
secTools:'All tools',
secToolsBlurb:'Every tool is prefixed <code>ph_</code>; required params are marked <span style="color:var(--accent)">*</span>. Hit <b>Try in playground</b> on any tool to load it above with a working example.',
ftSources:'Data sources',ftEndpoints:'Endpoints',ftServer:'Server',
ftDisc:'Data remains subject to each source\'s terms (Open-Meteo, USGS, OSM, HDX, PSA, Nager.Date). You are responsible for complying with the source licences. MonstarX is an independent wrapper and is not endorsed by any government agency. This is a staging deployment — don\'t build production load on it. Example payloads captured for documentation 2026-08-27.',
cat_weather:'Weather & Environment',cat_hazards:'Hazards & Safety',cat_geo:'Geocoding & Addresses',cat_admin:'PSGC & Admin',cat_civic:'Civic & IDs',cat_places:'Places & Services',cat_transport:'Transport',cat_finance:'Finance',cat_news:'News',cat_nature:'Biodiversity',cat_catalog:'Open Data Catalog',
runQuery:'▶ Run query',running:'Running…',copyCurl:'Copy as cURL',copiedCurl:'Copied cURL',resetEx:'Reset to example',
noParams:'This tool takes no parameters — just run it.',sampleReqs:'Sample requests',tryPlay:'▶ Try in playground',
exCall:'Example call & response',exCallSub:'Example call',exRespSub:'Example response — trimmed',
noParamsBadge:'no params',tabVisual:'Visual',tabJson:'JSON',tabRaw:'Raw',
contacting:'contacting server…',hintCors:'Staging MCP is unreachable. Start local PH-MCP (`npm run dev` in ../PH-MCP on :8789). Live Run on this site is proxied through /mcp.',
previewNote:'<b>Preview mode.</b> Live queries are sandboxed — download this page and open it from your own host (or locally) to run against the server.',
paramRequired:'required',paramOptional:'optional'
},
tl:{
navPlayground:'Playground',navTools:'Mga tool',navConnect:'Ikonekta',
navLivePg:'▶ Live playground',navUseCases:'Ano ang maaari mong gawin',navConnectAgent:'Ikonekta ang agent',navResponse:'Format ng sagot',navErrors:'Mga error',
filterTools:'I-filter ang mga tool…',eyebrow:'MonstarX · Philippines MCP',
heroTitle:"Pampublikong data ng Pilipinas, <span class=\"hl\">handa para sa AI</span>.",
heroLede:"Panahon, lindol, geocoding, ZIP, holiday, evacuation, turismo, FX, HDX open data — pinag-iisa ng <b>MonstarX</b> sa MCP tools, isang endpoint, walang API key.",
ctaTry:'▶ Subukan sa browser',ctaConnect:'Ikonekta ang Claude o Cursor',
statTools:'handang tools',statSources:'pampublikong source',statKeys:'API key / signup',statLiveN:'Live',statLive:'real-time data',
secPlayground:'Live playground',
secPlaygroundBlurb:'Pumili ng tool, baguhin ang inputs, pindutin ang <b>Run</b> — diretso sa live MCP server.',
tryLabel:'Subukan',
chipWx:'Panahon sa Maynila 24h',chipQuake:'Mga lindol',chipGeo:'Geocode Intramuros',chipPostal:'Postal 1000',
chipHoliday:'Holidays 2026',chipShelter:'Shelters · Maynila',chipTourism:'Turismo malapit sa Maynila',chipDatasets:'Hanapin ang typhoon datasets',
secUse:'Ano ang maaari mong gawin',secUseBlurb:'Hackathon o production — ilang tool call lang.',
useWxT:'Weather apps',useWxP:'24h/4-araw na forecast, UV, ulan, humidity, AQI.',
useDisT:'Kalamidad',useDisP:'Lindol, tsunami, bulkán, evacuation points.',
useMapT:'Mapa at address',useMapP:'Geocode, reverse geocode, ZIP, elevation.',
useTourT:'Turismo',useTourP:'OSM attractions at holiday calendar.',
useFinT:'FX at markets',useFinP:'USD/PHP, bangko, ginto, crypto, PSE.',
useDataT:'Open data',useDataP:'Hanapin ang HDX Philippines packages.',
secConnect:'Ikonekta ang iyong agent',
secConnectBlurb:'Ang MonstarX Philippines MCP ay remote HTTP MCP server. Ituro ang kahit anong MCP client — walang auth handshake.',
labClaude:'Claude Code',labCursor:'Cursor / HTTP clients',
labDesk:'Claude Desktop — <span style="text-transform:none;letter-spacing:0;font-weight:400;color:var(--faint)">claude_desktop_config.json</span>',
labCurl:'O cURL lang',
secResponse:'Format ng sagot',
secResponseBlurb:'Bawat call ay nagbabalik ng payload dalawang beses — JSON string sa <code>content[0].text</code> at object sa <code>structuredContent</code> (ito ang mas maganda).',
thField:'Field',thMeaning:'Kahulugan',
fSource:'Upstream — Open-Meteo, USGS, OSM, HDX, PSA, Nager.Date, atbp.',
fAgency:'Pinagmulan — PAGASA-compatible feeds, USGS, PSA, …',
fApi:'Tiyak na upstream API',
fLicense:'Lisensya / terms kung applicable',
fRetrieved:'Oras ng fetch ng server (UTC). Madalas PHT (+08:00) sa payload.',
fData:'Ang payload. May <code>total</code>, <code>shown</code>, <code>found</code> sa list tools.',
secErrors:'Mga error',
secErrorsBlurb:'Ang error ay normal result na may <code>isError: true</code>. Invalid args → MCP <code>-32602</code>.',
secTools:'Lahat ng tools',
secToolsBlurb:'Bawat tool ay nagsisimula sa <code>ph_</code>; required params ay may <span style="color:var(--accent)">*</span>.',
ftSources:'Mga source',ftEndpoints:'Mga endpoint',ftServer:'Server',
ftDisc:'Ang data ay nasasaklawan ng terms ng bawat source. Ang MonstarX ay independent wrapper. Staging — huwag gamitin sa production load.',
cat_weather:'Panahon',cat_hazards:'Panganib',cat_geo:'Geo',cat_admin:'PSGC',cat_civic:'Sibiko',
cat_places:'Lugar',cat_transport:'Transport',cat_finance:'Pananalapi',cat_news:'Balita',cat_nature:'Kalikasan',cat_catalog:'Catalog',
runQuery:'▶ Run query',running:'Tumatakbo…',copyCurl:'Kopyahin ang cURL',copiedCurl:'Nakopya',resetEx:'I-reset',
noParams:'Walang parameter ang tool na ito — i-run mo na lang.',sampleReqs:'Mga sample',tryPlay:'▶ Subukan sa playground',
exCall:'Halimbawang call at sagot',exCallSub:'Halimbawang call',exRespSub:'Halimbawang sagot',
noParamsBadge:'walang params',tabVisual:'Visual',tabJson:'JSON',tabRaw:'Raw',
contacting:'kinokontak ang server…',hintCors:'Hindi maabot ang staging MCP. Patakbuhin ang PH-MCP (`npm run dev` sa ../PH-MCP sa :8789). Ang Run dito ay dumadaan sa /mcp.',
previewNote:'<b>Preview mode.</b> Buksan ang page sa sarili mong host para tumakbo laban sa server.',
paramRequired:'kailangan',paramOptional:'opsyonal'
},
};
function t(key){const pack=I18N[LANG]||I18N.en;return pack[key]??I18N.en[key]??key;}
function catLabel(key){return t('cat_'+key)||CATLABEL[key]||key;}
function applyLang(lang){
  if(!I18N[lang])lang='en';
  LANG=lang;
  document.documentElement.lang=lang==='tl'?'tl':'en';
  document.documentElement.setAttribute('data-lang',lang);
  localStorage.setItem('mx-lang-ph',lang);
  const lbl=document.getElementById('langBtnLabel');
  if(lbl)lbl.textContent=lang==='tl'?'FIL':'EN';
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
 .replace('__CB_CC__',codeblock('shell',sh('claude mcp add --transport http \\\n  ph-mcp '+EP+'/mcp'),{raw:'claude mcp add --transport http ph-mcp '+EP+'/mcp'}))
 .replace('__CB_CURSOR__',codeblock('mcp.json',hl({mcpServers:{philippines:{type:"http",url:EP+'/mcp'}}})))
 .replace('__CB_DESK__',codeblock('json',hl({mcpServers:{philippines:{command:"npx",args:["-y","mcp-remote",EP+'/mcp']}}})))
 .replace('__CB_QS__',codeblock('bash',sh(curlFor('ph_weather_24h',{area_code:'manila'})),{raw:curlFor('ph_weather_24h',{area_code:'manila'})}))
 .replace('__CB_ENV__',codeblock('structuredContent — ph_weather_24h',hl({source:"Open-Meteo",agency:"PAGASA-compatible forecast",retrieved_at:"2026-08-27T07:00:00.000Z",api:"forecast 24-hour",area_code:"manila",location:{latitude:14.5995,longitude:120.9842,label:"Manila"},data:{hourly:{time:["2026-08-27T12:00"],temperature_2m:[31.2]}}})))
 .replace('__CB_ERR__',codeblock('isError: true — missing required argument',hl({content:[{type:"text",text:"MCP error -32602: Input validation error: Invalid arguments for tool ph_postal_code: [{ path: ['zipcode'], message: 'expected string, received undefined' }]"}],isError:true})));

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
 ph_weather_overview:{area_code:['manila','cebu','davao','baguio']},
 ph_weather_week_overview:{area_code:['manila','cebu']},
 ph_weather_warnings:{area_code:['manila','cebu']},
 ph_weather_24h:{area_code:['manila','cebu','davao','iloilo','baguio']},
 ph_weather_4day:{area_code:['manila','cebu','davao']},
 ph_uv_index:{area_code:['manila','cebu']},
 ph_rainfall:{area_code:['manila','cebu']},
 ph_air_temperature:{area_code:['manila','cebu']},
 ph_relative_humidity:{area_code:['manila','cebu']},
 ph_air_quality:{area_code:['manila','cebu']},
 ph_earthquake_list:{limit:['5','10','20']},
 ph_tsunami_list:{limit:['5','10']},
 ph_postal_code:{zipcode:['1000','6000','8000','2600']},
 ph_public_holidays:{year:['2026','2025','2027']},
 ph_elevation:{latitude:['14.5995','10.3157','7.1907'],longitude:['120.9842','123.8854','125.4553']},
 ph_bsp_finance:{from:['USD','EUR','JPY'],to:['PHP']},
 ph_disease_reports:{query:['dengue','malaria','health']},
 ph_evacuation_shelters:{latitude:['14.5995'],longitude:['120.9842']},
 ph_tourism_spots:{latitude:['14.5995','10.3157'],longitude:['120.9842','123.8854']},
 ph_address_search:{query:['Intramuros','Ayala Avenue Makati','Osmeña Blvd Cebu']},
 ph_geocode:{query:['Intramuros Manila','Rizal Park','Ayala Triangle']},
 ph_reverse_geocode:{latitude:['14.5995','10.3157'],longitude:['120.9842','123.8854']},
 ph_datasets_search:{query:['typhoon','population','earthquake']},
 ph_dataset_show:{id:['cod-ab-phl']},
 ph_dataset_metadata:{id:['cod-ab-phl']},
 ph_pse_quote:{ticker:['BDO','SM','ALI','TEL']}
};

const ASK={
 ph_weather_areas:"Which city codes can I use for forecasts?",
 ph_weather_overview:"What's the weather overview for Manila?",
 ph_weather_week_overview:"What's the week-ahead outlook for Manila?",
 ph_weather_warnings:"Are there weather warnings for Manila?",
 ph_weather_24h:"What's the hourly forecast in Manila for the next 24 hours?",
 ph_weather_4day:"What's the 4-day forecast for Cebu?",
 ph_uv_index:"How high is the UV index in Manila today?",
 ph_rainfall:"Is it raining in Manila right now (hourly)?",
 ph_air_temperature:"What are hourly temperatures in Manila?",
 ph_relative_humidity:"How humid is it in Manila hour by hour?",
 ph_air_quality:"How's the air quality (PM2.5 / AQI) in Manila?",
 ph_earthquake_list:"What earthquakes have been reported recently in the Philippines?",
 ph_tsunami_list:"Are there any recent tsunami-related events?",
 ph_postal_code:"What place is postal code 1000?",
 ph_public_holidays:"Which public holidays does the Philippines have in 2026?",
 ph_elevation:"What's the elevation in Manila?",
 ph_bsp_finance:"What's USD to PHP right now?",
 ph_disease_reports:"Find open datasets about dengue.",
 ph_evacuation_shelters:"Where are nearby evacuation points in Manila?",
 ph_tourism_spots:"What tourist attractions are near Intramuros?",
 ph_address_search:"Find addresses matching Intramuros.",
 ph_geocode:"What are the coordinates of Intramuros?",
 ph_reverse_geocode:"What's the address at 14.5995, 120.9842?",
 ph_datasets_search:"What open datasets mention typhoon?",
 ph_dataset_show:"Show metadata for package cod-ab-phl.",
 ph_regions:"List Philippine regions and PSGC codes."
};

const PRESETS={
 ph_reverse_geocode:[
  {label:'Manila',args:{latitude:14.5995,longitude:120.9842}},
  {label:'Cebu',args:{latitude:10.3157,longitude:123.8854}},
  {label:'Davao',args:{latitude:7.1907,longitude:125.4553}}
 ],
 ph_elevation:[
  {label:'Manila',args:{latitude:14.5995,longitude:120.9842}},
  {label:'Baguio',args:{latitude:16.4023,longitude:120.5960}}
 ],
 ph_tourism_spots:[
  {label:'Intramuros',args:{latitude:14.5896,longitude:120.9747,radius_m:1500,limit:10}},
  {label:'Makati',args:{latitude:14.5547,longitude:121.0244,radius_m:1200,limit:10}}
 ],
 ph_evacuation_shelters:[
  {label:'Manila',args:{latitude:14.5995,longitude:120.9842,limit:10}},
  {label:'Quezon City',args:{latitude:14.6760,longitude:121.0437,limit:10}}
 ],
 ph_weather_24h:[
  {label:'Manila',args:{area_code:'manila'}},
  {label:'Cebu',args:{area_code:'cebu'}},
  {label:'Davao',args:{area_code:'davao'}}
 ]
};


/* ---------- visual helpers ---------- */
function num(n){n=(typeof n==='number')?n:parseFloat(n);return isNaN(n)?'—':n.toLocaleString('en-US');}
function timeOnly(iso){try{return new Date(iso).toLocaleString('en-PH',{month:'short',day:'numeric',hour:'numeric',minute:'2-digit'});}catch(e){return iso||'';}}
function wkday(iso){try{return new Date(iso+(iso&&iso.length===10?'T00:00:00+08:00':'')).toLocaleDateString('en-PH',{weekday:'short',day:'numeric',month:'short'});}catch(e){return iso;}}
function vstat(big,label,sub){return '<div class="vstat"><div class="bn">'+big+'</div><div class="bl">'+esc(label)+'</div>'+(sub?'<div class="bs">'+esc(sub)+'</div>':'')+'</div>';}
function uvSev(v){if(v<3)return['Low','var(--sv-good)'];if(v<6)return['Moderate','var(--sv-mod)'];if(v<8)return['High','var(--sv-high)'];if(v<11)return['Very high','var(--sv-vhigh)'];return['Extreme','var(--sv-ext)'];}
function aqiSev(v){if(v<=20)return['Good','var(--sv-good)'];if(v<=40)return['Fair','var(--sv-mod)'];if(v<=60)return['Moderate','var(--sv-high)'];if(v<=80)return['Poor','var(--sv-vhigh)'];return['Very poor','var(--sv-ext)'];}
function wmoEmoji(c){c=+c;if(c===0)return'☀️';if(c<=3)return'⛅';if(c<=48)return'🌫️';if(c<=67)return'🌧️';if(c<=77)return'🌨️';if(c<=82)return'🌦️';if(c<=99)return'⛈️';return'🌤️';}
function gauge(v,max,sev,color){const pct=Math.max(3,Math.min(100,(+v||0)/max*100));return '<div class="gauge"><div class="gv" style="color:'+color+'">'+v+'<small> '+esc(sev)+'</small></div><div class="gbar"><i style="width:'+pct+'%;background:'+color+'"></i></div></div>';}

/* Philippines map bounds */
const PHB={lo:116.5,ln:127.0,la:4.5,lt:21.5};
const PH_OUTLINE=[[119.8,18.5],[121.0,18.6],[122.2,18.2],[122.0,16.0],[124.0,13.5],[125.5,12.0],[126.2,9.5],[126.5,7.2],[126.0,6.0],[125.0,5.5],[122.0,6.0],[120.8,6.2],[119.5,6.0],[118.0,7.0],[117.0,8.5],[118.5,10.5],[119.5,11.5],[120.2,13.5],[120.0,16.0],[119.8,18.5]];
function prj(lng,lat){return [((lng-PHB.lo)/(PHB.ln-PHB.lo))*1000,((PHB.lt-lat)/(PHB.lt-PHB.la))*600];}
function mapView(points,note){
 points=(points||[]).filter(p=>isFinite(p.lat)&&isFinite(p.lng)&&p.lat>4&&p.lat<22&&p.lng>116&&p.lng<128);
 if(!points.length)return null;
 const cap=60,shown=points.slice(0,cap);
 const path='M'+PH_OUTLINE.map(c=>prj(c[0],c[1]).map(n=>n.toFixed(1)).join(',')).join(' L')+' Z';
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
function overviewText(p){const d=p.data||{};const text=d.text||d.headlineText||(typeof d==='string'?d:JSON.stringify(d).slice(0,400));const title=d.targetArea||d.headTitle||p.area_code||'overview';return '<div class="vhead">Weather overview · '+esc(title)+' · '+timeOnly(d.reportDatetime||'')+'</div><div class="ccard"><div style="white-space:pre-wrap;line-height:1.55">'+esc(String(text).slice(0,1200))+'</div></div>';}
function officesView(p){const o=p.offices||[];return '<div class="vhead">'+num(p.total_offices||o.length)+' forecast cities</div><div class="vtwrap"><table class="vt"><thead><tr><th>Code</th><th>Name</th><th>English</th></tr></thead><tbody>'+o.slice(0,40).map(x=>'<tr><td class="mono"><b>'+esc(x.area_code)+'</b></td><td>'+esc(x.name)+'</td><td>'+esc(x.en_name||'')+'</td></tr>').join('')+'</tbody></table></div>'+(o.length>40?'<div class="vnote">Showing 40 of '+o.length+'.</div>':'');}
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
function holidaysView(p){const h=p.holidays||[];return '<div class="vhead">Philippines public holidays · '+esc(p.year||'')+' · '+num(p.total||h.length)+'</div><div class="vtwrap"><table class="vt"><thead><tr><th>Date</th><th>Local name</th><th>English</th></tr></thead><tbody>'+h.map(x=>'<tr><td class="mono">'+esc(x.date)+'</td><td><b>'+esc(x.local_name)+'</b></td><td>'+esc(x.name)+'</td></tr>').join('')+'</tbody></table></div>';}
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
 case 'ph_weather_areas':return officesView(p);
 case 'ph_weather_overview':
 case 'ph_weather_week_overview':return overviewText(p);
 case 'ph_weather_warnings':return warningsView(p);
 case 'ph_weather_24h':return wx24(p);
 case 'ph_weather_4day':return wx4(p);
 case 'ph_uv_index':return uvView(p);
 case 'ph_rainfall':return rainView(p);
 case 'ph_air_temperature':return tempView(p);
 case 'ph_relative_humidity':return humView(p);
 case 'ph_air_quality':return aqView(p);
 case 'ph_earthquake_list':return eventsView(p,'Earthquakes');
 case 'ph_tsunami_list':return eventsView(p,'Tsunami advisories');
 case 'ph_postal_code':return postalView(Object.assign({},p,{addresses:p.addresses||p.places||p.results||[],zipcode:p.zipcode||p.postal_code}));
 case 'ph_public_holidays':
 case 'ph_next_holidays':return holidaysView(Object.assign({},p,{holidays:p.holidays||p.data||[]}));
 case 'ph_elevation':return elevView(p);
 case 'ph_bsp_finance':return '<div class="vhead">FX</div><div class="statrow">'+vstat(esc(String(p.rate||p.value||((p.rates&&Object.values(p.rates)[0])||'—'))),esc(p.from||p.base||'')+' → '+esc(p.to||p.quote||'PHP'),esc(p.date||p.retrieved_at||''))+'</div>';
 case 'ph_disease_reports':
 case 'ph_datasets_search':return datasetsView(Object.assign({},p,{datasets:p.datasets||p.results||[]}));
 case 'ph_evacuation_shelters':return shelterView(p);
 case 'ph_tourism_spots':return tourismView(p);
 case 'ph_address_search':
 case 'ph_geocode':
 case 'ph_place_search':return geoResults(Object.assign({},p,{results:(p.results||p.places||[]).map(function(x){return {title:x.title||x.name||x.display_name,latitude:x.latitude||x.lat,longitude:x.longitude||x.lon||x.lng,address_code:x.address_code||x.postcode};})}));
 case 'ph_reverse_geocode':return reverseView(Object.assign({},p,{result:p.result||p}));
 case 'ph_dataset_show':
 case 'ph_dataset_metadata':return datasetShow(Object.assign({},p,{dataset:p.dataset||p.metadata||p}));
 case 'ph_dataset_query':return genTable(p.records)||null;
}
 if(Array.isArray(p.records))return genTable(p.records);
 if(Array.isArray(p.rows))return genTable(p.rows);
 if(Array.isArray(p.results))return genTable(p.results);
 if(Array.isArray(p.events))return eventsView(p,'Events');
 if(Array.isArray(p.data)&&p.data.length&&typeof p.data[0]==='object')return genTable(p.data);
 return null;}

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
    const res=await fetch(liveBase()+'/mcp',{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json, text/event-stream','mcp-protocol-version':'2025-06-18'},body:JSON.stringify({jsonrpc:'2.0',id:1,method:'tools/call',params:{name:n,arguments:args}})});
    const ms=Math.round(performance.now()-t0);
    const text=await res.text();const json=parseMaybeSSE(text);
    const r=json&&json.result;const isErr=Boolean((r&&r.isError)||!res.ok);
    let payload;
    if(r&&r.structuredContent)payload=r.structuredContent;
    else if(r&&r.content&&r.content[0]){try{payload=JSON.parse(r.content[0].text);}catch(e){payload=r.content[0].text;}}
    else payload=json||{error:text||('HTTP '+res.status),hint:t('hintCors')};
    lastResp={ms,status:res.status,isErr,payload,raw:text,rpc:json,name:n,blocked:!res.ok&&!r};
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
  wx24:['ph_weather_24h',{area_code:'manila'}],
  quake:['ph_earthquake_list',{limit:5}],
  geo:['ph_geocode',{query:'Intramuros Manila',limit:3}],
  postal:['ph_postal_code',{zipcode:'1000'}],
  holiday:['ph_public_holidays',{year:2026}],
  shelter:['ph_evacuation_shelters',{latitude:14.5995,longitude:120.9842,limit:5}],
  tourism:['ph_tourism_spots',{latitude:14.5896,longitude:120.9747,radius_m:1500,limit:8}],
  datasets:['ph_datasets_search',{query:'typhoon',rows:5}]
};
document.querySelectorAll('.chip-ex').forEach(c=>c.onclick=()=>{const [n,a]=EXAMPLES[c.dataset.ex];selectTool(n,a);document.getElementById('playground').scrollIntoView();setTimeout(()=>runCurrent(n),120);});
document.addEventListener('click',e=>{const b=e.target.closest('.tryit');if(!b)return;const n=b.dataset.try;selectTool(n);document.getElementById('playground').scrollIntoView({behavior:'smooth'});});
document.addEventListener('click',e=>{
  const s=e.target.closest('.samp');if(s){const inp=pgMain.querySelector('[data-p="'+s.dataset.p+'"]');if(inp){inp.value=s.dataset.v;inp.focus();}return;}
  const pr=e.target.closest('.preset');if(pr){const n=pr.dataset.n,i=+pr.dataset.i;selectTool(n,PRESETS[n][i].args);runCurrent(n);return;}
});
selectTool('ph_weather_24h');

/* copy / theme / lang / filter / menu */
document.addEventListener('click',e=>{const b=e.target.closest('.copy');if(!b)return;navigator.clipboard.writeText(decodeURIComponent(b.dataset.raw||'')).then(()=>{const o=b.textContent;b.textContent='Copied';b.classList.add('ok');setTimeout(()=>{b.textContent=o;b.classList.remove('ok');},1400);});});
document.getElementById('epPill').onclick=()=>{navigator.clipboard.writeText(EP+'/mcp');const u=document.querySelector('#epPill .u');const o=u.textContent;u.textContent='Copied!';setTimeout(()=>u.textContent=o,1100);};
const root=document.documentElement,saved=localStorage.getItem('mx-theme-ph');if(saved)root.setAttribute('data-theme',saved);
document.getElementById('themeBtn').onclick=()=>{const cur=root.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light');const nx=cur==='dark'?'light':'dark';root.setAttribute('data-theme',nx);localStorage.setItem('mx-theme-ph',nx);};

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
"""

BODY=STYLE+BODYTOP+SCRIPT.replace('__DATA__',DATA)
standalone=('<!doctype html><html lang="en"><head><meta charset="utf-8">'
 '<meta name="viewport" content="width=device-width,initial-scale=1">'
 '<title>MonstarX Philippines MCP | Live</title>'
 +FAVICON_LINK+
 '<meta name="description" content="Philippines public data as MCP tools any AI agent can call. Live in-browser playground: weather, earthquakes, geocoding, holidays, shelters, tourism, open data.">'
 +STYLE+'</head><body>'+BODYTOP+SCRIPT.replace('__DATA__',DATA)+'</body></html>')
os.makedirs(os.path.join(REPO,'public'),exist_ok=True)
open(os.path.join(REPO,'philippines-mcp-playground.html'),'w',encoding='utf-8').write(standalone)
open(os.path.join(REPO,'public','index.html'),'w',encoding='utf-8').write(standalone)
open(os.path.join(REPO,'public','favicon.svg'),'w',encoding='utf-8').write(FAVICON_SVG)
print('wrote public/index.html and philippines-mcp-playground.html ('+str(len(standalone))+' bytes)')
