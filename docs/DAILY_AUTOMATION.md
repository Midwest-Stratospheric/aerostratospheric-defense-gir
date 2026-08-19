# GIR Daily Git Automation (comprehensive)

## Schedule

| Channel | When |
|---------|------|
| GitHub Actions | **06:00 UTC** and **18:00 UTC** daily + manual dispatch |
| Local cron (optional) | `0 6 * * *` via `scripts/install_cron.sh` |

## What runs every time

`scripts/daily_gir_automation.sh` executes this sequence:

1. **Open-tier ingest** (`scripts/ingest_open_tier.py`)
2. **US open-status banner** (`scripts/compute_us_open_status.py`)
3. **Mermaid / SVG charts** (`scripts/generate_gir_charts.py`)
4. **Daily executive summary** (`scripts/generate_daily_exec_summary.py`)
5. **Git commit** of all refreshed data + reports

## Data outputs

| Source | Output |
|--------|--------|
| UOGW anomalies | `data/anomalies/uogw_anomalies_latest.json` |
| NASA EONET events | `data/events/eonet_open_latest.json` + `.geojson` |
| USGS earthquakes (M2.5+ day) | `data/events/usgs_quakes_2.5_day_latest.geojson` |
| NWS active alerts (US) | `data/events/nws_active_alerts_latest.geojson` |
| Sentinel-2 STAC (Casey region) | `data/imagery_index/sentinel2_*.json` |
| NASA DONKI CME (7-day) | `data/events/donki_cme_latest.json` |
| CISA KEV, OpenSky, OurAirports, etc. | `data/defense_open/` |
| Run manifest | `data/manifests/manifest_latest.json` |
| US open-status | `data/status/us_open_conditions_latest.json` |

All sources are **public open-tier** only.

## Executive reports

Daily open-tier executive summaries are written automatically:

| Resource | Link |
|----------|------|
| **Latest summary** | [reports/latest.md](../reports/latest.md) |
| **Daily archive** | [reports/daily/](../reports/daily/) |

Each file is named `YYYY-MM-DD-gir-exec.md`. Content covers data quality / completeness, key open-source counts, notable anomalies/events, and short recommended actions. Weekly roll-ups can be added to the same pipeline later if desired.

## Commands

```bash
bash scripts/daily_gir_automation.sh
# or step-by-step:
python3 scripts/ingest_open_tier.py
python3 scripts/compute_us_open_status.py
python3 scripts/generate_gir_charts.py
python3 scripts/generate_daily_exec_summary.py
```

## GitHub

Repo: https://github.com/Midwest-Stratospheric/aerostratospheric-defense-gir

Actions → **Daily GIR open-tier ingest** → **Run workflow** for an immediate refresh.
