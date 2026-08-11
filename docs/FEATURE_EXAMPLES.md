# GIR feature code examples

Runnable examples for each of the ten open-tier scientific features.
Run from the repository root with `PYTHONPATH=.` if needed.

---

## Feature 1 — Provenance & integrity

```python
from pathlib import Path
from scripts.lib.provenance import make_provenance, write_sidecar, sha256_file

path = Path("data/events/usgs_quakes_2.5_day_latest.geojson")
raw = path.read_bytes()

prov = make_provenance(
    record_id=path.name,
    source_id="usgs_earthquakes",
    source_url="https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson",
    content=raw,
    license="USGS public domain",
    attribution="U.S. Geological Survey",
    tier="open",
    transform={"parser": "geojson", "schema_version": "v1"},
)
side = write_sidecar(path, prov)
print("sidecar:", side)
print("sha256:", prov["content_sha256"])
assert sha256_file(path) == prov["content_sha256"]
```

---

## Feature 2 — Schema validation & completeness

```python
import json
from pathlib import Path
from scripts.lib.validate import validate_manifest_v2, completeness_score, validate_geojson_minimal

manifest = json.loads(Path("data/manifests/manifest_latest.json").read_text())
ok, errors = validate_manifest_v2(manifest)
score = completeness_score(manifest)
print("schema_valid:", ok, "completeness:", score, "errors:", errors)

quakes = json.loads(Path("data/events/usgs_quakes_2.5_day_latest.geojson").read_text())
gok, gerr = validate_geojson_minimal(quakes)
print("geojson_valid:", gok, gerr)
```

---

## Feature 3 — Temporal version index

```python
import json
from datetime import datetime, timezone
from pathlib import Path
from scripts.lib.provenance import sha256_file

TEMPORAL = Path("data/temporal")
TEMPORAL.mkdir(parents=True, exist_ok=True)
index = TEMPORAL / "run_index.jsonl"

entry = {
    "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "completeness_score": 1.0,
    "note": "manual example run",
    "manifest_sha256": sha256_file(Path("data/manifests/manifest_latest.json"))
    if Path("data/manifests/manifest_latest.json").exists() else None,
}
with index.open("a", encoding="utf-8") as f:
    f.write(json.dumps(entry) + "\n")

for line in index.read_text(encoding="utf-8").strip().splitlines()[-5:]:
    print(json.loads(line))
```

---

## Feature 4 — AOI spatial filters

```python
import json
from pathlib import Path
from scripts.lib.aoi import load_regions, filter_features_by_bbox, point_in_bbox

regions = load_regions(Path("config/aoi_regions.json"))
midwest = next(r for r in regions if r["id"] == "midwest_il")
bbox = midwest["bbox"]

print("Chicago in midwest AOI?", point_in_bbox(-87.63, 41.88, bbox))

quakes = json.loads(Path("data/events/usgs_quakes_2.5_day_latest.geojson").read_text())
subset = filter_features_by_bbox(quakes.get("features") or [], bbox)
print(f"quakes in {midwest['name']}:", len(subset))
```

---

## Feature 5 — Statistical baselines (rolling z-score)

```python
from pathlib import Path
from scripts.lib.baseline import update_baseline_store, mean_std, z_score

result = update_baseline_store(
    Path("data/quality/baseline_store.json"),
    series_id="usgs_m25_count_1d",
    value=39.0,
    window=30,
)
print(result)  # includes mu, sigma, z, flag (|z| >= 2)

mu, sigma = mean_std([10, 12, 11, 40])
print("z of 40:", z_score(40, mu, sigma))
```

---

## Feature 6 — Multi-source fusion

```python
from scripts.lib.fusion import fuse_events, haversine_km

print("km:", round(haversine_km(38.0, -88.0, 38.1, -88.1), 2))

events = [
    {"id": "a1", "source": "usgs", "lat": 37.6, "lon": -88.2,
     "time_utc": "2026-08-11T12:00:00Z", "label": "quake A"},
    {"id": "b1", "source": "eonet", "lat": 37.65, "lon": -88.18,
     "time_utc": "2026-08-11T13:30:00Z", "label": "event B"},
    {"id": "c1", "source": "usgs", "lat": 10.0, "lon": 20.0,
     "time_utc": "2026-08-11T12:00:00Z", "label": "far away"},
]
for c in fuse_events(events, distance_km=50.0, time_hours=24.0):
    print(c["cluster_id"], c["sources"], c["corroboration_score"])
```

---

## Feature 7 — STAC export

```python
import json
from pathlib import Path
from scripts.lib.stac_export import stac_collection, stac_item_from_index_row

coll = stac_collection()
index = json.loads(Path("data/imagery_index/sentinel2_index_latest.json").read_text())
items = [stac_item_from_index_row(row, coll["id"]) for row in (index.get("items") or [])[:5]]
print(coll["id"], "items:", len(items))
```

---

## Feature 8 — Freshness SLA

```python
from scripts.lib.freshness import evaluate_freshness, DEFAULT_SLA_HOURS

results = [
    {"source": "usgs_quakes", "ok": True, "fetched_at_utc": "2026-08-11T08:00:00Z"},
    {"source": "nws_alerts", "ok": True, "fetched_at_utc": "2026-08-01T00:00:00Z"},
]
report = evaluate_freshness(results)
print("sla_met:", report["sla_met"], "stale:", report["sources_stale"])
```

---

## Feature 9 — Research citation package

```python
from pathlib import Path
cff = Path("CITATION.cff").read_text(encoding="utf-8")
assert "cff-version:" in cff
print("CITATION.cff lines:", len(cff.splitlines()))
```

APA-style: Aerostratospheric / Midwest Stratospheric Data Systems. (2026). *Aerostratospheric Defense GIR* (Version 1.4.0) [Computer software]. https://github.com/Midwest-Stratospheric/aerostratospheric-defense-gir

---

## Feature 10 — Scientific methodology & uncertainty

```python
from pathlib import Path
for rel in ("docs/methodology/SCIENTIFIC_METHOD.md", "docs/methodology/UNCERTAINTY.md"):
    p = Path(rel)
    print(p, "OK" if p.exists() else "MISSING")
```

---

## Full suite

```bash
python3 scripts/ingest_open_tier.py
python3 scripts/gir_quality_suite.py
python3 scripts/generate_gir_charts.py
```
