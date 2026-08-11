#!/usr/bin/env python3
"""
Query public STAC API (Element84 Earth Search) for Sentinel-2 scenes over a bbox.
Example: python stac_search_sentinel2.py --bbox -88.2 39.1 -87.7 39.5 --limit 5
"""
from __future__ import annotations
import argparse, json, urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

STAC = "https://earth-search.aws.element84.com/v1/search"

def search(bbox, limit=5, days=14):
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)
    body = {
        "collections": ["sentinel-2-l2a"],
        "bbox": bbox,
        "datetime": f"{start.strftime('%Y-%m-%dT%H:%M:%SZ')}/{end.strftime('%Y-%m-%dT%H:%M:%SZ')}",
        "limit": limit,
        "query": {"eo:cloud_cover": {"lt": 30}},
    }
    req = urllib.request.Request(
        STAC,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "User-Agent": "Aerostratospheric-GIR/1.0"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--bbox", nargs=4, type=float, metavar=("W","S","E","N"),
                   default=[-88.2, 39.1, -87.7, 39.5], help="West South East North")
    p.add_argument("--limit", type=int, default=5)
    args = p.parse_args()
    data = search(args.bbox, args.limit)
    feats = data.get("features", [])
    print(f"Found {len(feats)} Sentinel-2 scenes")
    for f in feats:
        props = f.get("properties", {})
        print("-", f.get("id"), "cloud", props.get("eo:cloud_cover"), "datetime", props.get("datetime"))
    out = Path(__file__).resolve().parents[1] / "data" / "imagery_index"
    out.mkdir(parents=True, exist_ok=True)
    (out / "sentinel2_search_latest.json").write_text(json.dumps(data, indent=2))
    print("Wrote imagery_index/sentinel2_search_latest.json")

if __name__ == "__main__":
    main()
