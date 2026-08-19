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
6. **Email** the summary via Hostinger SMTP (if secrets are set)

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

Each file is named `YYYY-MM-DD-gir-exec.md`.

## Daily email (Hostinger SMTP)

After each successful run, the workflow can email the executive summary.

| Setting | Value |
|---------|--------|
| From / To | `launchcontrol@midwestsds.com` |
| SMTP host | `smtp.hostinger.com` |
| SMTP port | `465` (SSL) |

### Required GitHub Actions secrets

Add these under **Settings → Secrets and variables → Actions** (repository or org):

| Secret name | Value |
|-------------|--------|
| `SMTP_USERNAME` | `launchcontrol@midwestsds.com` |
| `SMTP_PASSWORD` | Hostinger mailbox password for that address |

If `SMTP_PASSWORD` is missing, the email step is skipped (ingest/report still run).

Subject line example: `GIR Daily Exec — 2026-08-19`  
Body: full text of the day’s `reports/daily/YYYY-MM-DD-gir-exec.md` plus a GitHub link.

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

Actions → **Daily GIR open-tier ingest** → **Run workflow** for an immediate refresh (and test email once secrets are set).
