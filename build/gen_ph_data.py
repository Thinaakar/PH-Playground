#!/usr/bin/env python3
"""Build build/data.min.json from the Philippines MCP tool dump."""
from __future__ import annotations

import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
DUMP = BASE / "ph_tools_dump.json"

CATEGORY_RULES: list[tuple[str, str, str, list[str]]] = [
    ("weather", "Weather & Environment", "Open-Meteo / PAGASA-compatible forecasts, UV, rain, AQI, marine, METAR.", [
        "ph_weather_", "ph_uv_", "ph_rainfall", "ph_air_temperature", "ph_relative_humidity",
        "ph_air_quality", "ph_historical_weather", "ph_marine", "ph_metar", "ph_sunrise", "ph_flood",
    ]),
    ("hazards", "Hazards & Safety", "Earthquakes, tsunami, volcanoes, floods, shelters, fire and police POIs.", [
        "ph_earthquake_", "ph_tsunami_", "ph_volcanoes", "ph_natural_events", "ph_evacuation_",
        "ph_fire_stations", "ph_police_stations",
    ]),
    ("geo", "Geocoding & Addresses", "Nominatim, postal codes, elevation, and place search.", [
        "ph_address_", "ph_geocode", "ph_reverse_geocode", "ph_postal_code", "ph_elevation", "ph_place_search",
    ]),
    ("admin", "PSGC & Admin", "Regions, provinces, cities, barangays, and PSGC code parsing.", [
        "ph_regions", "ph_provinces", "ph_cities", "ph_barangays", "ph_parse_psgc",
    ]),
    ("civic", "Civic & IDs", "Holidays, disease datasets, TIN/SSS/PhilHealth format, plates, mobile prefixes.", [
        "ph_public_holidays", "ph_next_holidays", "ph_long_weekend", "ph_disease_",
        "ph_id_format", "ph_lto_plate", "ph_mobile_network", "ph_prayer_",
    ]),
    ("places", "Places & Services", "Tourism, hospitals, pharmacies, schools, universities.", [
        "ph_tourism_", "ph_hospitals", "ph_pharmacies", "ph_schools", "ph_universities",
    ]),
    ("transport", "Transport", "Bus stops, metro/PNR, airports, ferries, fuel stations.", [
        "ph_bus_", "ph_metro_", "ph_airports", "ph_ferry_", "ph_fuel_",
    ]),
    ("finance", "Finance", "USD/PHP, banks, gold, crypto in PHP, PSE quotes.", [
        "ph_bsp_", "ph_banks", "ph_crypto_", "ph_gold_", "ph_pse_",
    ]),
    ("news", "News", "Headlines from Rappler, Philstar, Inquirer RSS.", [
        "ph_news",
    ]),
    ("nature", "Biodiversity", "GBIF species and occurrence records for the Philippines.", [
        "ph_species", "ph_occurrences",
    ]),
    ("catalog", "Open Data Catalog", "HDX CKAN search plus PSA OpenSTAT and World Bank helpers.", [
        "ph_datasets_", "ph_dataset_", "ph_psa_", "ph_worldbank",
    ]),
]

DEFAULT_ARGS: dict[str, dict] = {
    "ph_weather_24h": {"area_code": "manila"},
    "ph_weather_4day": {"area_code": "cebu"},
    "ph_weather_overview": {"area_code": "manila"},
    "ph_weather_week_overview": {"area_code": "manila"},
    "ph_weather_warnings": {"area_code": "manila"},
    "ph_uv_index": {"area_code": "manila"},
    "ph_rainfall": {"area_code": "manila"},
    "ph_air_temperature": {"area_code": "manila"},
    "ph_relative_humidity": {"area_code": "manila"},
    "ph_air_quality": {"area_code": "manila"},
    "ph_address_search": {"query": "Intramuros", "limit": 5},
    "ph_geocode": {"query": "Intramuros Manila", "limit": 3},
    "ph_reverse_geocode": {"latitude": 14.5995, "longitude": 120.9842},
    "ph_postal_code": {"zipcode": "1000"},
    "ph_elevation": {"latitude": 14.5995, "longitude": 120.9842},
    "ph_place_search": {"query": "Cebu", "limit": 5},
    "ph_earthquake_list": {"limit": 5},
    "ph_tsunami_list": {"limit": 5},
    "ph_public_holidays": {"year": 2026},
    "ph_evacuation_shelters": {"latitude": 14.5995, "longitude": 120.9842, "limit": 10},
    "ph_tourism_spots": {"latitude": 14.5995, "longitude": 120.9842, "radius_m": 1500, "limit": 8},
    "ph_hospitals": {"latitude": 14.5995, "longitude": 120.9842, "limit": 8},
    "ph_bus_stops": {"latitude": 14.5995, "longitude": 120.9842, "limit": 10},
    "ph_datasets_search": {"query": "typhoon", "rows": 5},
    "ph_dataset_show": {"id": "cod-ab-phl"},
    "ph_dataset_metadata": {"id": "cod-ab-phl"},
    "ph_cities": {"region_code": "130000000"},
    "ph_barangays": {"city_code": "133900000"},
    "ph_parse_psgc": {"code": "133900000"},
    "ph_bsp_finance": {"from": "USD", "to": "PHP"},
    "ph_pse_quote": {"ticker": "BDO"},
    "ph_id_format": {"kind": "tin", "value": "123-456-789"},
    "ph_lto_plate": {"plate": "NBC 1234"},
    "ph_mobile_network": {"phone": "09171234567"},
    "ph_banks": {"query": "BDO", "limit": 10},
}


def cat_for(name: str) -> str:
    for key, _label, _blurb, prefixes in CATEGORY_RULES:
        for p in prefixes:
            if name.startswith(p) or name == p.rstrip("_"):
                return key
    return "catalog"


def schema_to_params(schema: dict) -> list[dict]:
    props = (schema or {}).get("properties") or {}
    required = set((schema or {}).get("required") or [])
    out = []
    for pname, pdef in props.items():
        pdef = pdef or {}
        typ = pdef.get("type")
        if isinstance(typ, list):
            typ = next((t for t in typ if t != "null"), typ[0] if typ else "string")
        if typ is None:
            typ = "string"
        out.append({
            "name": pname,
            "type": typ,
            "required": pname in required,
            "desc": pdef.get("description") or "",
        })
    return out


def default_args_for(name: str, params: list[dict], schema: dict) -> dict:
    if name in DEFAULT_ARGS:
        return dict(DEFAULT_ARGS[name])
    args: dict = {}
    props = (schema or {}).get("properties") or {}
    required = set((schema or {}).get("required") or [])
    names = {p["name"] for p in params}
    if "area_code" in names:
        args["area_code"] = "manila"
    if "latitude" in required and "longitude" in required:
        args["latitude"] = 14.5995
        args["longitude"] = 120.9842
    if "query" in required:
        args["query"] = "Manila"
    if "limit" in names and "limit" not in args and ("query" in args or "latitude" in args):
        args["limit"] = min(int((props.get("limit") or {}).get("default") or 10), 20)
    for p in params:
        n = p["name"]
        if n in args:
            continue
        pdef = props.get(n) or {}
        if n in required and "default" not in pdef:
            if p["type"] == "string":
                args[n] = "Manila"
            elif p["type"] in ("integer", "number"):
                args[n] = 10 if "limit" in n else 1
    return args


def sample_response(name: str, args: dict) -> dict:
    return {
        "source": "MonstarX Philippines MCP",
        "agency": "Multiple public sources",
        "retrieved_at": "2026-08-27T07:00:00.000Z",
        "note": "Hit Run for live data from ph-mcp.",
        "tool": name,
        "example_args": args,
    }


def main() -> None:
    raw = json.loads(DUMP.read_text(encoding="utf-8-sig"))
    tools_list = raw.get("tools") or []
    tools: dict = {}
    buckets: dict[str, list[str]] = {k: [] for k, *_ in CATEGORY_RULES}

    for t in tools_list:
        name = t.get("tool") or t.get("name")
        if not name or name == "mcp_auth" or not str(name).startswith("ph_"):
            continue
        schema = t.get("inputSchema") or {}
        params = schema_to_params(schema)
        cat = cat_for(name)
        args = default_args_for(name, params, schema)
        tools[name] = {
            "cat": cat,
            "desc": t.get("description") or name,
            "params": params,
            "args": args,
            "response": sample_response(name, args),
        }
        buckets.setdefault(cat, []).append(name)

    categories = []
    for key, label, blurb, _prefs in CATEGORY_RULES:
        names = buckets.get(key) or []
        if names:
            categories.append({"key": key, "label": label, "blurb": blurb, "tools": names})

    dest = BASE / "data.min.json"
    dest.write_text(json.dumps({"categories": categories, "tools": tools}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {dest} — {len(tools)} tools, {len(categories)} categories")


if __name__ == "__main__":
    main()
