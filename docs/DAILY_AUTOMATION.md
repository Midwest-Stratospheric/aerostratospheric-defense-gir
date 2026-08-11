# GIR Daily Git Automation

## What runs daily

1. **UOGW anomaly report** → `data/anomalies/`
2. **NASA EONET open events** → `data/events/`
3. **Sentinel-2 STAC search** (Casey IL bbox) → `data/imagery_index/`
4. **Git commit** only when files changed

## Local one-shot

```bash
cd /path/to/gir
./scripts/daily_gir_automation.sh
```

## Install system cron (if `crontab` exists)

```bash
./scripts/install_cron.sh
# default: 0 6 * * *  (06:00 daily)
```

## GitHub Actions (recommended for remote)

Workflow: `.github/workflows/daily-gir.yml`

- Runs **06:00 UTC** daily
- Also triggerable manually (`workflow_dispatch`)
- Commits and pushes open-tier updates to `main`

## Policy

Automation touches **open tier only**. Do not point these scripts at classified or restricted sources.
