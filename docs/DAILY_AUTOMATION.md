# GIR Daily Git Automation (comprehensive)

## Schedule

| Channel | When |
|---------|------|
| GitHub Actions | **06:00 UTC** and **18:00 UTC** daily + manual dispatch |
| Local cron (optional) | `0 6 * * *` via `scripts/install_cron.sh` |

## What gets added every run

| Source | Output |
|--------|--------|
| UOGW anomalies | `data/anomalies/uogw_anomalies_latest.json` |
| NASA EONET events | `data/events/eonet_open_latest.json` + `.geojson` |
| USGS earthquakes (M2.5+ day) | `data/events/usgs_quakes_2.5_day_latest.geojson` |
| NWS active alerts (US) | `data/events/nws_active_alerts_latest.geojson` |
| Sentinel-2 STAC (Casey region) | `data/imagery_index/sentinel2_*.json` |
| NASA DONKI CME (7-day) | `data/events/donki_cme_latest.json` |
| Run manifest | `data/manifests/manifest_latest.json` |

All sources are **public open-tier** only.

## Commands

```bash
bash scripts/daily_gir_automation.sh
python3 scripts/ingest_open_tier.py
```

## GitHub

Repo: https://github.com/Midwest-Stratospheric/aerostratospheric-defense-gir

Actions → **Daily GIR open-tier ingest** → **Run workflow** for an immediate refresh.
