#!/usr/bin/env python3
"""
Aerostratospheric GIR — comprehensive open-tier ingest
Fetches public feeds into local GIR data folders and writes a daily manifest.
No classified sources. Respect source terms of use.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UA = "Aerostratospheric-GIR/1.1 (open-tier research ingest; +https://github.com/Midwest-Stratospheric/aerostratospheric-defense-gir)"

OUT = {
    "anomalies": ROOT / "data" / "anomalies",
    "events": ROOT / "data" / "events",
    "imagery_index": ROOT / "data" / "imagery_index",
    "reference": ROOT / "data" / "reference",
    "manifests": ROOT / "data" / "manifests",
}
for p in OUT.values():
    p.mkdir(parents=True, exist_ok=True)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def stamp() -> str:
    return utc_now().strftime("%Y%m%dT%H%M%SZ")


def fetch_json(url: str, timeout: int = 90):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", errors="replace"))


def write_json(path: Path, data) -> Path:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path


def safe_run(name: str, fn, results: list) -> None:
    try:
        info = fn()
        results.append({"source": name, "ok": True, **(info or {})})
        print(f"[ok] {name}: {info}")
    except Exception as e:
        results.append({"source": name, "ok": False, "error": str(e)})
        print(f"[fail] {name}: {e}")


def ingest_uogw():
    url = "https://raw.githubusercontent.com/Midwest-Stratospheric/Unified-Open-Global-Weather/main/data/latest/anomaly-report.json"
    data = fetch_json(url)
    ts = stamp()
    write_json(OUT["anomalies"] / f"uogw_anomalies_{ts}.json", data)
    write_json(OUT["anomalies"] / "uogw_anomalies_latest.json", data)
    return {"file": "uogw_anomalies_latest.json", "counts": data.get("counts", {})}


def ingest_eonet():
    url = "https://eonet.gsfc.nasa.gov/api/v3/events?status=open&limit=100"
    data = fetch_json(url)
    ts = stamp()
    write_json(OUT["events"] / f"eonet_open_{ts}.json", data)
    write_json(OUT["events"] / "eonet_open_latest.json", data)
    return {"file": "eonet_open_latest.json", "events": len(data.get("events", []))}


def ingest_eonet_geojson():
    url = "https://eonet.gsfc.nasa.gov/api/v3/events?status=open&limit=100"
    data = fetch_json(url)
    features = []
    for ev in data.get("events", []):
        cats = ",".join(c.get("title", "") for c in ev.get("categories", []))
        for geo in ev.get("geometry", [])[-1:]:
            coords = geo.get("coordinates")
            gtype = geo.get("type", "Point")
            if not coords:
                continue
            features.append({
                "type": "Feature",
                "geometry": {"type": gtype, "coordinates": coords},
                "properties": {
                    "id": ev.get("id"),
                    "title": ev.get("title"),
                    "categories": cats,
                    "date": geo.get("date"),
                    "source": "NASA EONET",
                },
            })
    fc = {"type": "FeatureCollection", "features": features, "updated_utc": utc_now().isoformat()}
    write_json(OUT["events"] / "eonet_open_latest.geojson", fc)
    return {"file": "eonet_open_latest.geojson", "features": len(features)}


def ingest_usgs_quakes():
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson"
    data = fetch_json(url)
    ts = stamp()
    write_json(OUT["events"] / f"usgs_quakes_2.5_day_{ts}.json", data)
    write_json(OUT["events"] / "usgs_quakes_2.5_day_latest.geojson", data)
    return {"file": "usgs_quakes_2.5_day_latest.geojson", "features": len(data.get("features", []))}


def ingest_nws_alerts_us():
    url = "https://api.weather.gov/alerts/active?status=actual&message_type=alert"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/geo+json"})
    with urllib.request.urlopen(req, timeout=90) as r:
        data = json.loads(r.read().decode("utf-8", errors="replace"))
    feats = data.get("features", [])
    slim = {
        "type": "FeatureCollection",
        "updated_utc": utc_now().isoformat(),
        "count": len(feats),
        "features": feats[:250],
    }
    write_json(OUT["events"] / "nws_active_alerts_latest.geojson", slim)
    return {"file": "nws_active_alerts_latest.geojson", "count": len(feats), "stored": len(slim["features"])}


def ingest_sentinel2_stac(bbox=None, limit=10):
    bbox = bbox or [-88.2, 39.1, -87.7, 39.5]
    end = utc_now()
    start = end - timedelta(days=21)
    body = {
        "collections": ["sentinel-2-l2a"],
        "bbox": bbox,
        "datetime": f"{start.strftime('%Y-%m-%dT%H:%M:%SZ')}/{end.strftime('%Y-%m-%dT%H:%M:%SZ')}",
        "limit": limit,
        "query": {"eo:cloud_cover": {"lt": 40}},
    }
    req = urllib.request.Request(
        "https://earth-search.aws.element84.com/v1/search",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "User-Agent": UA},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=90) as r:
        data = json.loads(r.read().decode())
    write_json(OUT["imagery_index"] / "sentinel2_search_latest.json", data)
    items = []
    for f in data.get("features", []):
        props = f.get("properties", {})
        items.append({
            "id": f.get("id"),
            "datetime": props.get("datetime"),
            "cloud_cover": props.get("eo:cloud_cover"),
            "platform": props.get("platform"),
            "bbox": f.get("bbox"),
        })
    write_json(OUT["imagery_index"] / "sentinel2_index_latest.json", {
        "updated_utc": utc_now().isoformat(),
        "bbox": bbox,
        "count": len(items),
        "items": items,
    })
    return {"file": "sentinel2_search_latest.json", "scenes": len(items), "bbox": bbox}


def ingest_donki_cme():
    end = utc_now().strftime("%Y-%m-%d")
    start = (utc_now() - timedelta(days=7)).strftime("%Y-%m-%d")
    url = f"https://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/CME?startDate={start}&endDate={end}"
    try:
        data = fetch_json(url, timeout=60)
    except Exception:
        data = []
    write_json(OUT["events"] / "donki_cme_latest.json", {
        "updated_utc": utc_now().isoformat(),
        "start": start,
        "end": end,
        "count": len(data) if isinstance(data, list) else 0,
        "events": data if isinstance(data, list) else [],
    })
    return {"file": "donki_cme_latest.json", "count": len(data) if isinstance(data, list) else 0}


def main():
    print("GIR comprehensive open-tier ingest", utc_now().isoformat())
    results = []
    safe_run("uogw_anomalies", ingest_uogw, results)
    safe_run("eonet_events", ingest_eonet, results)
    safe_run("eonet_geojson", ingest_eonet_geojson, results)
    safe_run("usgs_quakes", ingest_usgs_quakes, results)
    safe_run("nws_alerts", ingest_nws_alerts_us, results)
    safe_run("sentinel2_stac", ingest_sentinel2_stac, results)
    safe_run("donki_cme", ingest_donki_cme, results)

    ok = sum(1 for r in results if r.get("ok"))
    manifest = {
        "generated_at_utc": utc_now().isoformat(),
        "ok": ok,
        "total": len(results),
        "results": results,
        "tier": "open",
        "policy": "Public feeds only — no classified content",
    }
    ts = stamp()
    write_json(OUT["manifests"] / f"manifest_{ts}.json", manifest)
    write_json(OUT["manifests"] / "manifest_latest.json", manifest)
    print(f"Manifest: {ok}/{len(results)} sources ok")
    print("Done.")
    return 0 if ok > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
