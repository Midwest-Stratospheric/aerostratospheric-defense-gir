#!/usr/bin/env python3
"""Aerostratospheric GIR comprehensive open-tier ingest. Public feeds only."""
from __future__ import annotations
import csv, io, json, os, urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UA = "Aerostratospheric-GIR/1.3 (+https://github.com/Midwest-Stratospheric/aerostratospheric-defense-gir)"
OUT = {k: ROOT / "data" / k for k in ["anomalies", "events", "imagery_index", "reference", "manifests", "defense_open"]}
for p in OUT.values():
    p.mkdir(parents=True, exist_ok=True)

def utc_now():
    return datetime.now(timezone.utc)
def stamp():
    return utc_now().strftime("%Y%m%dT%H%M%SZ")
def fetch_json(url, timeout=60, headers=None):
    h = {"User-Agent": UA, "Accept": "application/json"}
    if headers: h.update(headers)
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", errors="replace"))
def fetch_bytes(url, timeout=60, method="GET", data=None, headers=None):
    h = {"User-Agent": UA}
    if headers: h.update(headers)
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()
def write_json(path, data):
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path
def safe_run(name, fn, results):
    try:
        info = fn() or {}
        results.append({"source": name, "ok": True, **info})
        print(f"[ok] {name}: {info}")
    except Exception as e:
        results.append({"source": name, "ok": False, "error": str(e)})
        print(f"[fail] {name}: {e}")

def ingest_uogw():
    data = fetch_json("https://raw.githubusercontent.com/Midwest-Stratospheric/Unified-Open-Global-Weather/main/data/latest/anomaly-report.json")
    ts = stamp()
    write_json(OUT["anomalies"] / f"uogw_anomalies_{ts}.json", data)
    write_json(OUT["anomalies"] / "uogw_anomalies_latest.json", data)
    return {"file": "uogw_anomalies_latest.json", "counts": data.get("counts", {})}

def ingest_eonet():
    data = fetch_json("https://eonet.gsfc.nasa.gov/api/v3/events?status=open&limit=100")
    write_json(OUT["events"] / "eonet_open_latest.json", data)
    return {"file": "eonet_open_latest.json", "events": len(data.get("events", []))}

def ingest_eonet_geojson():
    data = fetch_json("https://eonet.gsfc.nasa.gov/api/v3/events?status=open&limit=100")
    features = []
    for ev in data.get("events", []):
        cats = ",".join(c.get("title", "") for c in ev.get("categories", []))
        for geo in ev.get("geometry", [])[-1:]:
            coords = geo.get("coordinates")
            if not coords: continue
            features.append({"type": "Feature", "geometry": {"type": geo.get("type", "Point"), "coordinates": coords}, "properties": {"id": ev.get("id"), "title": ev.get("title"), "categories": cats}})
    write_json(OUT["events"] / "eonet_open_latest.geojson", {"type": "FeatureCollection", "features": features, "updated_utc": utc_now().isoformat()})
    return {"file": "eonet_open_latest.geojson", "features": len(features)}

def ingest_usgs_quakes():
    data = fetch_json("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson")
    write_json(OUT["events"] / "usgs_quakes_2.5_day_latest.geojson", data)
    return {"file": "usgs_quakes_2.5_day_latest.geojson", "features": len(data.get("features", []))}

def ingest_nws_alerts_us():
    req = urllib.request.Request("https://api.weather.gov/alerts/active?status=actual&message_type=alert", headers={"User-Agent": UA, "Accept": "application/geo+json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read().decode("utf-8", errors="replace"))
    feats = data.get("features", [])
    write_json(OUT["events"] / "nws_active_alerts_latest.geojson", {"type": "FeatureCollection", "updated_utc": utc_now().isoformat(), "count": len(feats), "features": feats[:250]})
    return {"file": "nws_active_alerts_latest.geojson", "count": len(feats)}

def ingest_sentinel2_stac(bbox=None, limit=10):
    bbox = bbox or [-88.2, 39.1, -87.7, 39.5]
    end, start = utc_now(), utc_now() - timedelta(days=21)
    body = {"collections": ["sentinel-2-l2a"], "bbox": bbox, "datetime": f"{start.strftime('%Y-%m-%dT%H:%M:%SZ')}/{end.strftime('%Y-%m-%dT%H:%M:%SZ')}", "limit": limit, "query": {"eo:cloud_cover": {"lt": 40}}}
    req = urllib.request.Request("https://earth-search.aws.element84.com/v1/search", data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "User-Agent": UA}, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read().decode())
    write_json(OUT["imagery_index"] / "sentinel2_search_latest.json", data)
    items = [{"id": f.get("id"), "datetime": f.get("properties", {}).get("datetime"), "cloud_cover": f.get("properties", {}).get("eo:cloud_cover")} for f in data.get("features", [])]
    write_json(OUT["imagery_index"] / "sentinel2_index_latest.json", {"updated_utc": utc_now().isoformat(), "count": len(items), "items": items})
    return {"file": "sentinel2_search_latest.json", "scenes": len(items)}

def ingest_donki_cme():
    end, start = utc_now().strftime("%Y-%m-%d"), (utc_now() - timedelta(days=7)).strftime("%Y-%m-%d")
    try:
        data = fetch_json(f"https://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/CME?startDate={start}&endDate={end}", timeout=45)
    except Exception:
        data = []
    write_json(OUT["events"] / "donki_cme_latest.json", {"updated_utc": utc_now().isoformat(), "count": len(data) if isinstance(data, list) else 0, "events": data if isinstance(data, list) else []})
    return {"file": "donki_cme_latest.json", "count": len(data) if isinstance(data, list) else 0}

def ingest_cisa_kev():
    data = fetch_json("https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json")
    write_json(OUT["defense_open"] / "cisa_kev_latest.json", data)
    return {"file": "cisa_kev_latest.json", "count": len(data.get("vulnerabilities", []))}

def ingest_ourairports_military_keywords():
    raw = fetch_bytes("https://davidmegginson.github.io/ourairports-data/airports.csv", timeout=90).decode("utf-8", errors="replace")
    military = []
    for row in csv.DictReader(io.StringIO(raw)):
        name, keywords, nl = row.get("name") or "", (row.get("keywords") or "").lower(), (row.get("name") or "").lower()
        if not ("military" in keywords or "air force" in keywords or "naval air" in keywords or "afb" in nl or "air force base" in nl or "naval air station" in nl):
            continue
        try:
            lat, lon = float(row["latitude_deg"]), float(row["longitude_deg"])
        except Exception:
            continue
        military.append({"feature_id": f"OA-{row.get('ident')}", "name": name, "lat": lat, "lon": lon, "iso_country": row.get("iso_country"), "source": "OurAirports", "tier": "open"})
    military = sorted(military, key=lambda x: x["name"])[:5000]
    write_json(OUT["defense_open"] / "public_military_airfields_ourairports.json", {"updated_utc": utc_now().isoformat(), "count": len(military), "features": military, "disclaimer": "Keyword heuristic — not official basing list"})
    return {"file": "public_military_airfields_ourairports.json", "count": len(military)}

def ingest_usaspending_defense():
    end, start = utc_now().date(), utc_now().date() - timedelta(days=90)
    payload = json.dumps({"filters": {"time_period": [{"start_date": str(start), "end_date": str(end)}], "award_type_codes": ["A", "B", "C", "D"], "naics_codes": ["336411", "336412", "336413", "336414", "541715", "928110"]}, "fields": ["Award ID", "Recipient Name", "Award Amount", "Description", "Awarding Agency", "NAICS Code"], "page": 1, "limit": 50, "sort": "Award Amount", "order": "desc"}).encode()
    req = urllib.request.Request("https://api.usaspending.gov/api/v2/search/spending_by_award/", data=payload, headers={"Content-Type": "application/json", "User-Agent": UA}, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read().decode())
    results = data.get("results", [])
    write_json(OUT["defense_open"] / "usaspending_defense_naics_latest.json", {"updated_utc": utc_now().isoformat(), "count": len(results), "results": results, "tier": "open"})
    return {"file": "usaspending_defense_naics_latest.json", "count": len(results)}

def ingest_gdelt_lastupdate():
    text = fetch_bytes("http://data.gdeltproject.org/gdeltv2/lastupdate.txt", timeout=30).decode()
    urls = [ln.split()[-1] for ln in text.strip().splitlines() if "http" in ln]
    write_json(OUT["defense_open"] / "gdelt_lastupdate.json", {"updated_utc": utc_now().isoformat(), "files": urls, "tier": "open"})
    return {"file": "gdelt_lastupdate.json", "files": len(urls)}

def ingest_opensky_midwest():
    try:
        data = fetch_json("https://opensky-network.org/api/states/all?lamin=37&lomin=-91&lamax=41&lomax=-86", timeout=40)
    except Exception as e:
        write_json(OUT["defense_open"] / "opensky_status.json", {"ok": False, "error": str(e), "tier": "open"})
        raise
    states, features = data.get("states") or [], []
    for s in states:
        if not s or s[5] is None or s[6] is None: continue
        features.append({"type": "Feature", "geometry": {"type": "Point", "coordinates": [s[5], s[6]]}, "properties": {"icao24": s[0], "callsign": s[1], "origin_country": s[2]}})
    write_json(OUT["defense_open"] / "opensky_midwest_snapshot.geojson", {"type": "FeatureCollection", "count": len(features), "features": features, "tier": "open"})
    return {"file": "opensky_midwest_snapshot.geojson", "count": len(features)}

def ingest_osm_military_landuse():
    q = b'[out:json][timeout:40];way["landuse"="military"](38.8,-89.2,40.2,-87.8);out center tags;'
    data = json.loads(fetch_bytes("https://overpass-api.de/api/interpreter", timeout=55, method="POST", data=q).decode())
    features = []
    for el in data.get("elements", []):
        c = el.get("center") or {}
        lat, lon = c.get("lat", el.get("lat")), c.get("lon", el.get("lon"))
        if lat is None or lon is None: continue
        features.append({"type": "Feature", "geometry": {"type": "Point", "coordinates": [lon, lat]}, "properties": {"id": el.get("id"), **(el.get("tags") or {})}})
    write_json(OUT["defense_open"] / "osm_military_landuse_il_sample.geojson", {"type": "FeatureCollection", "count": len(features), "features": features, "license": "ODbL", "tier": "open"})
    return {"file": "osm_military_landuse_il_sample.geojson", "count": len(features)}

def ingest_firms_status_or_data():
    key = os.environ.get("FIRMS_MAP_KEY", "").strip()
    if not key:
        write_json(OUT["defense_open"] / "firms_status.json", {"status": "MAP_KEY required", "env": "FIRMS_MAP_KEY", "tier": "open"})
        return {"file": "firms_status.json", "status": "awaiting_key"}
    raw = fetch_bytes(f"https://firms.modaps.eosdis.nasa.gov/api/country/csv/{key}/VIIRS_SNPP_NRT/USA/1", timeout=60).decode("utf-8", errors="replace")
    (OUT["defense_open"] / "firms_viirs_usa_1day_latest.csv").write_text(raw)
    return {"file": "firms_viirs_usa_1day_latest.csv", "rows": max(0, raw.count(chr(10)) - 1)}

def write_partner_stubs():
    write_json(OUT["defense_open"] / "ucdp_access.json", {"status": "registration required", "portal": "https://ucdp.uu.se/", "tier": "open/academic"})
    write_json(OUT["defense_open"] / "acled_partner.json", {"status": "partner API key required", "secret": "ACLED_API_KEY", "tier": "partner"})
    write_json(OUT["defense_open"] / "partner_tier_note.json", {"message": "Restricted products belong in a private repo.", "suggested_private_repo": "aerostratospheric-defense-gir-restricted"})
    return {"files": 3}

def main():
    print("GIR comprehensive open-tier ingest", utc_now().isoformat())
    results = []
    for name, fn in [("uogw_anomalies", ingest_uogw), ("eonet_events", ingest_eonet), ("eonet_geojson", ingest_eonet_geojson), ("usgs_quakes", ingest_usgs_quakes), ("nws_alerts", ingest_nws_alerts_us), ("sentinel2_stac", ingest_sentinel2_stac), ("donki_cme", ingest_donki_cme), ("cisa_kev", ingest_cisa_kev), ("ourairports_military_keywords", ingest_ourairports_military_keywords), ("usaspending_defense", ingest_usaspending_defense), ("gdelt_lastupdate", ingest_gdelt_lastupdate), ("opensky_midwest", ingest_opensky_midwest), ("osm_military_landuse", ingest_osm_military_landuse), ("firms", ingest_firms_status_or_data), ("partner_stubs", write_partner_stubs)]:
        safe_run(name, fn, results)
    ok = sum(1 for r in results if r.get("ok"))
    manifest = {"generated_at_utc": utc_now().isoformat(), "ok": ok, "total": len(results), "results": results, "tier": "open"}
    write_json(OUT["manifests"] / "manifest_latest.json", manifest)
    write_json(OUT["manifests"] / f"manifest_{stamp()}.json", manifest)
    print(f"Manifest: {ok}/{len(results)} sources ok")
    return 0 if ok > 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())
