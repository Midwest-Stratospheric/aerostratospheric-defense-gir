# GIR charts (git code)

Charts under `docs/images/` are produced by:

```bash
python3 scripts/generate_gir_charts.py
```

## What it reads

| Input | Chart output |
|-------|----------------|
| `data/manifests/manifest_latest.json` | `ingest_status.png` |
| `data/anomalies/uogw_anomalies_latest.json` | `uogw_severity.png` |
| `data/events/usgs_quakes_2.5_day_latest.geojson` | `usgs_mags.png` |
| `data/defense_open/public_military_airfields_ourairports.json` | `airfields_by_country.png` |
| `data/imagery_index/sentinel2_index_latest.json` | `sentinel2_clouds.png` |
| `data/defense_open/usaspending_defense_naics_latest.json` | `usaspending_top.png` |
| (static diagram) | `gir_data_flow.png` |

## Automation

`scripts/daily_gir_automation.sh` runs chart generation after ingest and before the git commit, so refreshed PNGs are included when data changes.

## Dependency

```bash
pip install matplotlib
# or: pip install -r requirements.txt
```

Open tier only — charts summarize public feeds.
