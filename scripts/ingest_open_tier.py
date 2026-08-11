#!/usr/bin/env python3
"""
Aerostratospheric GIR — daily open-tier ingest
Fetches public UOGW anomalies and NASA EONET events into local GIR data folders.
No classified sources. Respect source terms of use.
"""
from __future__ import annotations
import json, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_ANOM = ROOT / "data" / "anomalies"
OUT_EVENTS = ROOT / "data" / "events"
OUT_ANOM.mkdir(parents=True, exist_ok=True)
OUT_EVENTS.mkdir(parents=True, exist_ok=True)

UA = "Aerostratospheric-GIR/1.0 (open-tier research ingest)"

def fetch_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))

def ingest_uogw():
    url = "https://raw.githubusercontent.com/Midwest-Stratospheric/Unified-Open-Global-Weather/main/data/latest/anomaly-report.json"
    data = fetch_json(url)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = OUT_ANOM / f"uogw_anomalies_{stamp}.json"
    path.write_text(json.dumps(data, indent=2))
    latest = OUT_ANOM / "uogw_anomalies_latest.json"
    latest.write_text(json.dumps(data, indent=2))
    print(f"UOGW anomalies: {data.get('counts', {})} -> {path.name}")

def ingest_eonet():
    url = "https://eonet.gsfc.nasa.gov/api/v3/events?status=open&limit=50"
    data = fetch_json(url)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = OUT_EVENTS / f"eonet_open_{stamp}.json"
    path.write_text(json.dumps(data, indent=2))
    (OUT_EVENTS / "eonet_open_latest.json").write_text(json.dumps(data, indent=2))
    print(f"EONET open events: {len(data.get('events', []))} -> {path.name}")

def main():
    print("GIR open-tier ingest", datetime.now(timezone.utc).isoformat())
    try:
        ingest_uogw()
    except Exception as e:
        print("UOGW failed:", e)
    try:
        ingest_eonet()
    except Exception as e:
        print("EONET failed:", e)
    print("Done.")

if __name__ == "__main__":
    main()
