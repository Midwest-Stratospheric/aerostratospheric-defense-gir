# GIR Open-Tier Data Packages

This document describes the **daily data packages** produced by the Aerostratospheric Defense GIR automation. Everything here is public open-tier only.

## Daily package contents

Each successful run of `scripts/daily_gir_automation.sh` refreshes and commits:

| Package area | Path(s) | Description |
|--------------|---------|-------------|
| **Manifest** | `data/manifests/manifest_latest.json` | Per-source ok/fail, counts, timestamp |
| **Anomalies** | `data/anomalies/uogw_anomalies_latest.json` | UOGW research anomaly report (alert/watch/info) |
| **Events** | `data/events/` | EONET, USGS M2.5+ day, NWS active alerts, DONKI CME |
| **Imagery index** | `data/imagery_index/` | Sentinel-2 STAC search + index (Casey AOI) |
| **Defense-open** | `data/defense_open/` | CISA KEV, OurAirports military-keyword sample, OpenSky Midwest snapshot, OSM military landuse (IL), USASpending sample, GDELT lastupdate, FIRMS status |
| **US open status** | `data/status/us_open_conditions_latest.json` | GREEN/YELLOW/… banner from public factors only |
| **Charts** | `docs/charts/`, `docs/GRAPHS.md` | SVG + Mermaid summaries |
| **Executive report** | `reports/daily/YYYY-MM-DD-gir-exec.md`, `reports/latest.md` | Concise quality + observations + actions |

## How to consume

- **Latest everything:** clone or sparse-checkout `main`, or fetch individual raw files via `https://raw.githubusercontent.com/Midwest-Stratospheric/aerostratospheric-defense-gir/main/...`
- **Machine status:** `data/status/us_open_conditions_latest.json` and `data/manifests/manifest_latest.json`
- **Human briefing:** [reports/latest.md](../reports/latest.md)
- **Rebuild locally:** `bash scripts/daily_gir_automation.sh`

## Related ecosystem packages

| Repository | Role |
|------------|------|
| [Unified-Open-Global-Weather](https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather) | Multi-layer atmospheric commons; source of UOGW anomaly report |
| [msds-data](https://github.com/Midwest-Stratospheric/msds-data) | First-party ground weather + planned HAB flight packages |
| [International-Ground-Data-Repository](https://github.com/Midwest-Stratospheric/International-Ground-Data-Repository) | IGRA / international ground indexes |

## License & attribution

- Repository software: MIT (`LICENSE`)
- Upstream data: retain each provider’s terms (NWS, USGS, NASA, CISA, OpenSky, OurAirports, OSM ODbL, etc.)
- Cite this repo via `CITATION.cff` when using the curated package as a whole

## What is intentionally excluded

Classified, FOUO, partner-restricted, and export-controlled material. Higher tiers belong in separate private repositories under agreement.
