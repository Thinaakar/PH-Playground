#!/usr/bin/env python3
"""Adapt copied Japan build.py into Philippines MCP playground generator."""
from __future__ import annotations

import re
from pathlib import Path

BUILD = Path(__file__).resolve().parent / "build.py"
text = BUILD.read_text(encoding="utf-8")

text = text.replace(
    '"""Generate the MonstarX Japan MCP playground HTML from tool metadata.\n\n'
    "Run from anywhere:  python build/build.py\n"
    "Reads:  build/data.min.json  (tool schemas + captured example responses)\n"
    "Writes: public/index.html  and  japan-mcp-playground.html  (identical)\n"
    '"""',
    '"""Generate the MonstarX Philippines MCP playground HTML from tool metadata.\n\n'
    "Run from anywhere:  python build/build.py\n"
    "Reads:  build/data.min.json  (tool schemas + captured example responses)\n"
    "Writes: public/index.html  and  philippines-mcp-playground.html  (identical)\n"
    '"""',
)

old_dots = (
    "--dot-catalog:#64748b;--dot-weather:#16a34a;--dot-hazards:#dc2626;--dot-geo:#0891b2;"
    "--dot-civic:#7c3aed;--dot-places:#db2777;--dot-finance:#ea580c;"
)
new_dots = (
    "--dot-catalog:#64748b;--dot-weather:#16a34a;--dot-hazards:#dc2626;--dot-geo:#0891b2;"
    "--dot-admin:#0d9488;--dot-civic:#7c3aed;--dot-places:#db2777;--dot-transport:#2563eb;"
    "--dot-finance:#ea580c;--dot-news:#ca8a04;--dot-nature:#15803d;"
)
if old_dots not in text:
    raise SystemExit("category dots not found")
text = text.replace(old_dots, new_dots)

for a, b in [
    ("Japan&nbsp;MCP", "Philippines&nbsp;MCP"),
    ("jp-mcp-staging.monstarxapp.com/mcp", "ph-mcp-staging.monstarxapp.com/mcp"),
    ("MonstarX · Japan MCP", "MonstarX · Philippines MCP"),
    ("Japan's public data,", "The Philippines' public data,"),
    ("Japan-smart products", "Philippines-smart products"),
    ("real Japan data", "real Philippines data"),
    ("MonstarX Japan MCP", "MonstarX Philippines MCP"),
    ("Japan MCP", "Philippines MCP"),
    ("japan-mcp-playground.html", "philippines-mcp-playground.html"),
    ("Filter 27 tools", "Filter tools"),
    ("27ツールを絞り込み", "I-filter ang mga tool"),
    ("All 27 tools", "All tools"),
    ("into 27 tools", "into MCP tools"),
    ("const EP='https://jp-mcp-staging.monstarxapp.com';",
     "const EP='https://ph-mcp-staging.monstarxapp.com';"),
    ("mx-lang-jp", "mx-lang-ph"),
    ("mx-theme-jp", "mx-theme-ph"),
    ("jp-mcp ", "ph-mcp "),
    ("{mcpServers:{japan:", "{mcpServers:{philippines:"),
    ("en-JP", "en-PH"),
    ("+09:00", "+08:00"),
    ("monstarx-mcp-jp", "ph-mcp"),
]:
    text = text.replace(a, b)

text = text.replace(
    '<div class="stat"><div class="n">27</div><div class="l" data-i18n="statTools">ready-made tools</div></div>',
    '<div class="stat"><div class="n" id="statToolN">70</div><div class="l" data-i18n="statTools">ready-made tools</div></div>',
)
text = text.replace(
    '<div class="stat"><div class="n">9</div><div class="l" data-i18n="statSources">free public sources</div></div>',
    '<div class="stat"><div class="n">12</div><div class="l" data-i18n="statSources">free public sources</div></div>',
)

# Hero lede HTML
text = text.replace(
    "Weather, earthquakes, geocoding, postal codes, holidays, evacuation shelters, tourism spots, Bank of Japan series, open datasets — Japan's free public APIs live across many agencies, each with its own formats and quirks. <b>MonstarX unifies them into MCP tools any AI agent can call</b>, through one endpoint, with no API keys. Stop writing integration glue. Start shipping Philippines-smart products.",
    "Weather, earthquakes, geocoding, postal codes, holidays, evacuation shelters, tourism, FX, HDX open datasets — Philippine public APIs live across many agencies, each with its own formats and quirks. <b>MonstarX unifies them into MCP tools any AI agent can call</b>, through one endpoint, with no API keys. Stop writing integration glue. Start shipping Philippines-smart products.",
)

old_chips = '''          <button class="chip-ex" data-ex="wx24" data-i18n-chip="chipWx"><span class="e">⛅</span> Tokyo weather 24h</button>
          <button class="chip-ex" data-ex="quake" data-i18n-chip="chipQuake"><span class="e">🌋</span> Recent quakes</button>
          <button class="chip-ex" data-ex="geo" data-i18n-chip="chipGeo"><span class="e">📍</span> Geocode 東京駅</button>
          <button class="chip-ex" data-ex="postal" data-i18n-chip="chipPostal"><span class="e">✉️</span> Postal 100-0001</button>
          <button class="chip-ex" data-ex="holiday" data-i18n-chip="chipHoliday"><span class="e">🎌</span> Holidays 2026</button>
          <button class="chip-ex" data-ex="shelter" data-i18n-chip="chipShelter"><span class="e">🏫</span> Shelters · Chiyoda</button>
          <button class="chip-ex" data-ex="tourism" data-i18n-chip="chipTourism"><span class="e">🗾</span> Tourism near Tokyo St.</button>
          <button class="chip-ex" data-ex="datasets" data-i18n-chip="chipDatasets"><span class="e">📚</span> Search 天気 datasets</button>'''
new_chips = '''          <button class="chip-ex" data-ex="wx24" data-i18n-chip="chipWx"><span class="e">⛅</span> Manila weather 24h</button>
          <button class="chip-ex" data-ex="quake" data-i18n-chip="chipQuake"><span class="e">🌋</span> Recent quakes</button>
          <button class="chip-ex" data-ex="geo" data-i18n-chip="chipGeo"><span class="e">📍</span> Geocode Intramuros</button>
          <button class="chip-ex" data-ex="postal" data-i18n-chip="chipPostal"><span class="e">✉️</span> Postal 1000</button>
          <button class="chip-ex" data-ex="holiday" data-i18n-chip="chipHoliday"><span class="e">🇵🇭</span> Holidays 2026</button>
          <button class="chip-ex" data-ex="shelter" data-i18n-chip="chipShelter"><span class="e">🏫</span> Shelters · Manila</button>
          <button class="chip-ex" data-ex="tourism" data-i18n-chip="chipTourism"><span class="e">🏝️</span> Tourism near Manila</button>
          <button class="chip-ex" data-ex="datasets" data-i18n-chip="chipDatasets"><span class="e">📚</span> Search typhoon datasets</button>'''
if old_chips not in text:
    raise SystemExit("chips not found")
text = text.replace(old_chips, new_chips)

old_uses = '''      <div class="uses">
        <div class="use"><div class="ico">⛅</div><h4 data-i18n="useWxT">Weather-aware apps</h4><p data-i18n="useWxP">Area codes, daily/weekly JMA text, 24h/4-day forecasts, UV, rain, and air quality for Tokyo or any prefecture office.</p><div class="tools"><code>jp_weather_24h</code><code>jp_weather_warnings</code><code>jp_uv_index</code></div></div>
        <div class="use"><div class="ico">🌋</div><h4 data-i18n="useDisT">Disaster awareness</h4><p data-i18n="useDisP">Surface recent earthquakes, tsunami advisories, and nearby designated evacuation shelters.</p><div class="tools"><code>jp_earthquake_list</code><code>jp_tsunami_list</code><code>jp_evacuation_shelters</code></div></div>
        <div class="use"><div class="ico">📍</div><h4 data-i18n="useMapT">Maps &amp; addressing</h4><p data-i18n="useMapP">Search places, geocode, reverse-geocode, resolve postal codes, and read GSI elevation — all without keys.</p><div class="tools"><code>jp_geocode</code><code>jp_postal_code</code><code>jp_elevation</code></div></div>
        <div class="use"><div class="ico">🗾</div><h4 data-i18n="useTourT">Travel &amp; tourism</h4><p data-i18n="useTourP">Find nearby attractions from OpenStreetMap and pair with weather or holiday calendars.</p><div class="tools"><code>jp_tourism_spots</code><code>jp_public_holidays</code></div></div>
        <div class="use"><div class="ico">📈</div><h4 data-i18n="useFinT">Macro / finance bots</h4><p data-i18n="useFinP">Pull Bank of Japan series such as overnight call rates into research or agent workflows.</p><div class="tools"><code>jp_boj_finance</code></div></div>
        <div class="use"><div class="ico">📚</div><h4 data-i18n="useDataT">Open data explorer</h4><p data-i18n="useDataP">Search DATA.GO.JP / e-Gov packages, inspect metadata, and query datastore tables.</p><div class="tools"><code>jp_datasets_search</code><code>jp_dataset_query</code></div></div>
      </div>'''
new_uses = '''      <div class="uses">
        <div class="use"><div class="ico">⛅</div><h4 data-i18n="useWxT">Weather-aware apps</h4><p data-i18n="useWxP">City codes, 24h/4-day forecasts, UV, rain, humidity, and air quality for Manila, Cebu, Davao, and more.</p><div class="tools"><code>ph_weather_24h</code><code>ph_weather_warnings</code><code>ph_uv_index</code></div></div>
        <div class="use"><div class="ico">🌋</div><h4 data-i18n="useDisT">Disaster awareness</h4><p data-i18n="useDisP">Surface recent earthquakes, tsunami lists, volcanoes, and nearby evacuation points.</p><div class="tools"><code>ph_earthquake_list</code><code>ph_tsunami_list</code><code>ph_evacuation_shelters</code></div></div>
        <div class="use"><div class="ico">📍</div><h4 data-i18n="useMapT">Maps &amp; addressing</h4><p data-i18n="useMapP">Search places, geocode, reverse-geocode, resolve ZIP codes, and read elevation — no keys.</p><div class="tools"><code>ph_geocode</code><code>ph_postal_code</code><code>ph_elevation</code></div></div>
        <div class="use"><div class="ico">🏝️</div><h4 data-i18n="useTourT">Travel &amp; tourism</h4><p data-i18n="useTourP">Find nearby attractions from OpenStreetMap and pair with holiday calendars.</p><div class="tools"><code>ph_tourism_spots</code><code>ph_public_holidays</code></div></div>
        <div class="use"><div class="ico">📈</div><h4 data-i18n="useFinT">FX &amp; markets</h4><p data-i18n="useFinP">USD/PHP rates, bank directory, gold, crypto in pesos, and PSE quotes.</p><div class="tools"><code>ph_bsp_finance</code><code>ph_pse_quote</code></div></div>
        <div class="use"><div class="ico">📚</div><h4 data-i18n="useDataT">Open data explorer</h4><p data-i18n="useDataP">Search HDX Philippines packages, inspect metadata, and query datastore tables.</p><div class="tools"><code>ph_datasets_search</code><code>ph_dataset_query</code></div></div>
      </div>'''
if old_uses not in text:
    raise SystemExit("use-cases not found")
text = text.replace(old_uses, new_uses)

old_footer_src = (
    '<div><h4 data-i18n="ftSources">Data sources</h4>'
    '<div><a href="https://www.jma.go.jp/bosai/">JMA bosai</a> · weather, quakes, tsunami</div>'
    '<div><a href="https://open-meteo.com/">Open-Meteo</a> · hourly / air quality</div>'
    '<div><a href="https://www.gsi.go.jp/">GSI</a> · address, elevation</div>'
    '<div><a href="https://www.e-gov.go.jp/">DATA.GO.JP / e-Gov</a> · open catalog</div>'
    '<div><a href="https://www.boj.or.jp/">Bank of Japan</a> · time-series</div></div>'
)
new_footer_src = (
    '<div><h4 data-i18n="ftSources">Data sources</h4>'
    '<div><a href="https://open-meteo.com/">Open-Meteo</a> · weather, UV, AQI, marine</div>'
    '<div><a href="https://earthquake.usgs.gov/">USGS</a> · earthquakes in PH bbox</div>'
    '<div><a href="https://www.openstreetmap.org/">OpenStreetMap</a> · places, POIs, shelters</div>'
    '<div><a href="https://data.humdata.org/">HDX</a> · Philippines open catalog</div>'
    '<div><a href="https://psa.gov.ph/">PSA / Nager.Date</a> · stats &amp; holidays</div></div>'
)
if old_footer_src not in text:
    raise SystemExit("footer sources not found")
text = text.replace(old_footer_src, new_footer_src)

text = text.replace(
    "Data remains subject to each source's terms (JMA, GSI, Open-Meteo, DATA.GO.JP/e-Gov, BOJ, zipcloud, Nager.Date, OpenStreetMap ODbL). You are responsible for complying with the source licences. MonstarX is an independent wrapper and is not endorsed by any government agency. This is a staging deployment — don't build production load on it. Example payloads captured for documentation 2026-08-07.",
    "Data remains subject to each source's terms (Open-Meteo, USGS, OSM, HDX, PSA, Nager.Date, Zippopotam.us). You are responsible for complying with the source licences. MonstarX is an independent wrapper and is not endorsed by any government agency. This is a staging deployment — don't build production load on it. Example payloads captured for documentation 2026-08-27.",
)

text = text.replace(
    '<button type="button" data-lang="ja" role="option">🇯🇵 日本語</button>',
    '<button type="button" data-lang="tl" role="option">🇵🇭 Filipino</button>',
)
text = text.replace(
    "Japan government open data as 27 MCP tools",
    "Philippines public data as MCP tools",
)
text = text.replace(
    "Live in-browser playground: weather, earthquakes, geocoding, holidays, shelters, tourism, open data.",
    "Live in-browser playground: weather, earthquakes, geocoding, holidays, shelters, tourism, open data.",
)
text = text.replace("MonstarX Japan MCP | Live", "MonstarX Philippines MCP | Live")
text = text.replace("prefixed <code>jp_</code>", "prefixed <code>ph_</code>")

# EN i18n key strings
text = text.replace("filterTools:'Filter tools…'", "filterTools:'Filter tools…'")
text = text.replace(
    'heroLede:"Weather, earthquakes, geocoding, postal codes, holidays, evacuation shelters, tourism spots, Bank of Japan series, open datasets — Japan\'s free public APIs live across many agencies, each with its own formats and quirks. <b>MonstarX unifies them into MCP tools any AI agent can call</b>, through one endpoint, with no API keys. Stop writing integration glue. Start shipping Philippines-smart products."',
    'heroLede:"Weather, earthquakes, geocoding, postal codes, holidays, evacuation shelters, tourism, FX, HDX open datasets — Philippine public APIs live across many agencies, each with its own formats and quirks. <b>MonstarX unifies them into MCP tools any AI agent can call</b>, through one endpoint, with no API keys. Stop writing integration glue. Start shipping Philippines-smart products."',
)
text = text.replace(
    "chipWx:'Tokyo weather 24h',chipQuake:'Recent quakes',chipGeo:'Geocode 東京駅',chipPostal:'Postal 100-0001',\nchipHoliday:'Holidays 2026',chipShelter:'Shelters · Chiyoda',chipTourism:'Tourism near Tokyo St.',chipDatasets:'Search 天気 datasets',",
    "chipWx:'Manila weather 24h',chipQuake:'Recent quakes',chipGeo:'Geocode Intramuros',chipPostal:'Postal 1000',\nchipHoliday:'Holidays 2026',chipShelter:'Shelters · Manila',chipTourism:'Tourism near Manila',chipDatasets:'Search typhoon datasets',",
)
text = text.replace(
    "useWxP:'Area codes, daily/weekly JMA text, 24h/4-day forecasts, UV, rain, and air quality for Tokyo or any prefecture office.',\nuseDisT:'Disaster awareness',useDisP:'Surface recent earthquakes, tsunami advisories, and nearby designated evacuation shelters.',\nuseMapT:'Maps & addressing',useMapP:'Search places, geocode, reverse-geocode, resolve postal codes, and read GSI elevation — all without keys.',\nuseTourT:'Travel & tourism',useTourP:'Find nearby attractions from OpenStreetMap and pair with weather or holiday calendars.',\nuseFinT:'Macro / finance bots',useFinP:'Pull Bank of Japan series such as overnight call rates into research or agent workflows.',\nuseDataT:'Open data explorer',useDataP:'Search DATA.GO.JP / e-Gov packages, inspect metadata, and query datastore tables.',",
    "useWxP:'City codes, 24h/4-day forecasts, UV, rain, humidity, and air quality for Manila, Cebu, Davao, and more.',\nuseDisT:'Disaster awareness',useDisP:'Surface recent earthquakes, tsunami lists, volcanoes, and nearby evacuation points.',\nuseMapT:'Maps & addressing',useMapP:'Search places, geocode, reverse-geocode, resolve ZIP codes, and read elevation — no keys.',\nuseTourT:'Travel & tourism',useTourP:'Find nearby attractions from OpenStreetMap and pair with holiday calendars.',\nuseFinT:'FX & markets',useFinP:'USD/PHP rates, bank directory, gold, crypto in pesos, and PSE quotes.',\nuseDataT:'Open data explorer',useDataP:'Search HDX Philippines packages, inspect metadata, and query datastore tables.',",
)
text = text.replace(
    "fSource:'Upstream platform — JMA bosai, Open-Meteo, GSI, DATA.GO.JP, BOJ, zipcloud, etc.',\nfAgency:'Originating body — Japan Meteorological Agency, GSI, Digital Agency, Bank of Japan, …',",
    "fSource:'Upstream platform — Open-Meteo, USGS, OSM, HDX, PSA, Nager.Date, etc.',\nfAgency:'Originating body — PAGASA-compatible feeds, PHIVOLCS-adjacent USGS, PSA, …',",
)
text = text.replace(
    "fRetrieved:'Server fetch time (UTC). Live timestamps inside payloads are often JST (+08:00).'",
    "fRetrieved:'Server fetch time (UTC). Live timestamps inside payloads are often PHT (+08:00).'",
)
text = text.replace(
    "cat_weather:'Weather & Environment',cat_hazards:'Earthquakes & Tsunami',cat_geo:'Geocoding & Addresses',cat_civic:'Civic & Safety',cat_places:'Tourism',cat_finance:'Finance (BOJ)',cat_catalog:'Open Data Catalog',",
    "cat_weather:'Weather & Environment',cat_hazards:'Hazards & Safety',cat_geo:'Geocoding & Addresses',cat_admin:'PSGC & Admin',cat_civic:'Civic & IDs',cat_places:'Places & Services',cat_transport:'Transport',cat_finance:'Finance',cat_news:'News',cat_nature:'Biodiversity',cat_catalog:'Open Data Catalog',",
)
text = text.replace(
    "ftDisc:'Data remains subject to each source\\'s terms (JMA, GSI, Open-Meteo, DATA.GO.JP/e-Gov, BOJ, zipcloud, Nager.Date, OpenStreetMap ODbL). You are responsible for complying with the source licences. MonstarX is an independent wrapper and is not endorsed by any government agency. This is a staging deployment — don\\'t build production load on it. Example payloads captured for documentation 2026-08-07.',",
    "ftDisc:'Data remains subject to each source\\'s terms (Open-Meteo, USGS, OSM, HDX, PSA, Nager.Date). You are responsible for complying with the source licences. MonstarX is an independent wrapper and is not endorsed by any government agency. This is a staging deployment — don\\'t build production load on it. Example payloads captured for documentation 2026-08-27.',",
)

# Replace Japanese I18N block with Filipino
m = re.search(r"\nja:\{", text)
if not m:
    raise SystemExit("ja: start not found")
i = m.end() - 1
depth = 0
end = None
for j in range(i, len(text)):
    if text[j] == "{":
        depth += 1
    elif text[j] == "}":
        depth -= 1
        if depth == 0:
            end = j + 1
            break
if end is None:
    raise SystemExit("ja brace end not found")
if text[end:end + 1] == ",":
    end += 1

tl_block = r'''
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
contacting:'kinokontak ang server…',hintCors:'Kailangan maabot ng browser ang MCP server (CORS).',
previewNote:'<b>Preview mode.</b> Buksan ang page sa sarili mong host para tumakbo laban sa server.',
paramRequired:'kailangan',paramOptional:'opsyonal'
},
'''
text = text[:m.start()] + tl_block.rstrip() + ("\n" if text[end:end + 1] != "\n" else "") + text[end:]

text = text.replace(
    "document.documentElement.lang=lang==='ja'?'ja':'en';",
    "document.documentElement.lang=lang==='tl'?'tl':'en';",
)
text = text.replace(
    "if(lbl)lbl.textContent=lang==='ja'?'日本語':'EN';",
    "if(lbl)lbl.textContent=lang==='tl'?'FIL':'EN';",
)

# After DATA parse, set tool count
if "const DATA=JSON.parse" in text and "statToolN" in text:
    text = text.replace(
        "const DATA=JSON.parse(document.getElementById('apidata').textContent);",
        "const DATA=JSON.parse(document.getElementById('apidata').textContent);\n"
        "(function(){const n=Object.keys(DATA.tools||{}).length;const el=document.getElementById('statToolN');if(el)el.textContent=String(n);"
        "const f=document.getElementById('filter');if(f&&f.placeholder)f.placeholder='Filter '+n+' tools…';})();",
    )

# SAMPLES / ASK / PRESETS / EXAMPLES
samples = r'''
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
'''
ask = r'''
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
'''
presets = r'''
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
'''
text = re.sub(r"const SAMPLES=\{.*?\n\};", samples.strip() + "\n", text, count=1, flags=re.S)
text = re.sub(r"const ASK=\{.*?\n\};", ask.strip() + "\n", text, count=1, flags=re.S)
text = re.sub(r"const PRESETS=\{.*?\n\};", presets.strip() + "\n", text, count=1, flags=re.S)

ex_m = re.search(r"const EXAMPLES=\{.*?\n\};", text, re.S)
if not ex_m:
    raise SystemExit("EXAMPLES not found")
new_ex = """const EXAMPLES={
  wx24:['ph_weather_24h',{area_code:'manila'}],
  quake:['ph_earthquake_list',{limit:5}],
  geo:['ph_geocode',{query:'Intramuros Manila',limit:3}],
  postal:['ph_postal_code',{zipcode:'1000'}],
  holiday:['ph_public_holidays',{year:2026}],
  shelter:['ph_evacuation_shelters',{latitude:14.5995,longitude:120.9842,limit:5}],
  tourism:['ph_tourism_spots',{latitude:14.5896,longitude:120.9747,radius_m:1500,limit:8}],
  datasets:['ph_datasets_search',{query:'typhoon',rows:5}]
};"""
text = text[:ex_m.start()] + new_ex + text[ex_m.end():]

text = text.replace("selectTool('jp_weather_24h');", "selectTool('ph_weather_24h');")
text = text.replace(
    "curlFor('jp_weather_24h',{area_code:'130000'})",
    "curlFor('ph_weather_24h',{area_code:'manila'})",
)
text = text.replace(
    "codeblock('structuredContent — jp_weather_24h'",
    "codeblock('structuredContent — ph_weather_24h'",
)
text = text.replace('"area_code":"130000"', '"area_code":"manila"')
text = text.replace("latitude:35.6895,longitude:139.6917", "latitude:14.5995,longitude:120.9842")
text = text.replace("jp_postal_code", "ph_postal_code")
text = text.replace("['zipcode']", "['zipcode']")

# Map Philippines
old_map = """/* Japan map bounds (main islands + Okinawa) */
const JPB={lo:122.5,ln:146.5,la:24.0,lt:46.0};
const JP_OUTLINE=[[129.5,33.2],[130.5,31.5],[131.2,30.8],[135.0,33.5],[136.5,34.5],[137.5,34.8],[139.0,35.0],[140.5,35.5],[141.5,38.0],[142.0,41.5],[141.5,43.5],[140.0,45.5],[139.0,43.0],[138.0,37.0],[136.0,36.0],[133.0,34.5],[131.0,34.0],[129.5,33.2]];
function prj(lng,lat){return [((lng-JPB.lo)/(JPB.ln-JPB.lo))*1000,((JPB.lt-lat)/(JPB.lt-JPB.la))*600];}
function mapView(points,note){
 points=(points||[]).filter(p=>isFinite(p.lat)&&isFinite(p.lng)&&p.lat>20&&p.lat<50&&p.lng>120&&p.lng<150);
 if(!points.length)return null;
 const cap=60,shown=points.slice(0,cap);
 const path='M'+JP_OUTLINE.map(c=>prj(c[0],c[1]).map(n=>n.toFixed(1)).join(',')).join(' L')+' Z';"""
new_map = """/* Philippines map bounds */
const PHB={lo:116.5,ln:127.0,la:4.5,lt:21.5};
const PH_OUTLINE=[[119.8,18.5],[121.0,18.6],[122.2,18.2],[122.0,16.0],[124.0,13.5],[125.5,12.0],[126.2,9.5],[126.5,7.2],[126.0,6.0],[125.0,5.5],[122.0,6.0],[120.8,6.2],[119.5,6.0],[118.0,7.0],[117.0,8.5],[118.5,10.5],[119.5,11.5],[120.2,13.5],[120.0,16.0],[119.8,18.5]];
function prj(lng,lat){return [((lng-PHB.lo)/(PHB.ln-PHB.lo))*1000,((PHB.lt-lat)/(PHB.lt-PHB.la))*600];}
function mapView(points,note){
 points=(points||[]).filter(p=>isFinite(p.lat)&&isFinite(p.lng)&&p.lat>4&&p.lat<22&&p.lng>116&&p.lng<128);
 if(!points.length)return null;
 const cap=60,shown=points.slice(0,cap);
 const path='M'+PH_OUTLINE.map(c=>prj(c[0],c[1]).map(n=>n.toFixed(1)).join(',')).join(' L')+' Z';"""
if old_map not in text:
    raise SystemExit("map block not found")
text = text.replace(old_map, new_map)

text = text.replace("JMA overview", "Weather overview")
text = text.replace("JMA forecast offices", "forecast cities")
text = text.replace("Japan public holidays", "Philippines public holidays")

viz_m = re.search(
    r"function _viz\(name,p\)\{if\(!p\|\|typeof p!=='object'\)return null;switch\(name\)\{.*?\n\}return null;\}",
    text,
    re.S,
)
if not viz_m:
    raise SystemExit("_viz not found")
new_viz = r'''function _viz(name,p){if(!p||typeof p!=='object')return null;switch(name){
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
 return null;}'''
text = text[:viz_m.start()] + new_viz + text[viz_m.end():]

text = text.replace(
    "open(os.path.join(REPO,'japan-mcp-playground.html')",
    "open(os.path.join(REPO,'philippines-mcp-playground.html')",
)
text = text.replace(
    "print('wrote public/index.html and japan-mcp-playground.html",
    "print('wrote public/index.html and philippines-mcp-playground.html",
)

# Source/agency table leftover
text = text.replace(
    "Upstream platform — JMA bosai, Open-Meteo, GSI, DATA.GO.JP, BOJ, zipcloud, etc.",
    "Upstream platform — Open-Meteo, USGS, OSM, HDX, PSA, Nager.Date, etc.",
)
text = text.replace(
    "Originating body — Japan Meteorological Agency, GSI, Digital Agency, Bank of Japan, …",
    "Originating body — PAGASA-compatible feeds, USGS, PSA, HDX, …",
)

BUILD.write_text(text, encoding="utf-8")
print("adapted", BUILD)
