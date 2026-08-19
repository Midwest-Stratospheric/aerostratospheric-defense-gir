# GIR feature set (v1.5 scientific open tier)

Engineered capabilities for a robust, research-grade open Geospatial Information Repository.

## Core quality & science features

| # | Feature | Code / artifacts | Output |
|---|---------|------------------|--------|
| 1 | **Provenance & integrity** | `scripts/lib/provenance.py` | `*.prov.json` sidecars with SHA-256, license, source URL |
| 2 | **Schema validation** | `scripts/lib/validate.py`, `schema/` | Completeness score + error list in quality report |
| 3 | **Temporal version index** | `data/temporal/` | Run history for change detection |
| 4 | **AOI spatial filters** | `config/aoi_regions.json`, `scripts/lib/aoi.py` | Per-region subsets |
| 5 | **Statistical baselines** | `scripts/lib/baseline.py` | Rolling μ, σ, z-flag store |
| 6 | **Multi-source fusion** | `scripts/lib/fusion.py` | Corroboration clusters |
| 7 | **STAC export** | `scripts/lib/stac_export.py` | STAC collection / items |
| 8 | **Freshness SLA** | `scripts/lib/freshness.py` | `sla_met`, stale source list |
| 9 | **Research citation package** | `CITATION.cff` | Citable software/data artifact |
| 10 | **Scientific methodology** | `docs/methodology/` | Methods + uncertainty statements |

## Daily automation & products

| # | Feature | Code / artifacts | Output |
|---|---------|------------------|--------|
| 11 | **Open-tier multi-source ingest** | `scripts/ingest_open_tier.py` | `data/**` latest + timestamped |
| 12 | **US open-status banner** | `scripts/compute_us_open_status.py` | `data/status/us_open_conditions_latest.json` |
| 13 | **Git-native charts** | `scripts/generate_gir_charts.py` | `docs/charts/*.svg`, `docs/GRAPHS.md` |
| 14 | **Daily executive summary** | `scripts/generate_daily_exec_summary.py` | `reports/daily/YYYY-MM-DD-gir-exec.md`, `reports/latest.md` |
| 15 | **Scheduled GitHub Actions** | `.github/workflows/daily-gir.yml` | Twice daily (06:00 / 18:00 UTC) + dispatch |
| 16 | **Auto-rerun on failure** | `.github/workflows/auto-rerun-failures.yml` | One automatic retry of failed jobs |

## Repository hygiene (GitHub features)

- `CONTRIBUTING.md` — contribution and open-tier boundaries
- `SECURITY.md` — vulnerability reporting
- `LICENSE` (MIT) + `CITATION.cff`
- `docs/DATA_PACKAGES.md` — package map for consumers
- `docs/DATA_POLICY.md`, `docs/OPEN_DEFENSE_DATA.md`, `docs/DAILY_AUTOMATION.md`

## Run

```bash
python3 scripts/ingest_open_tier.py
python3 scripts/compute_us_open_status.py
python3 scripts/generate_gir_charts.py
python3 scripts/generate_daily_exec_summary.py
# or full pipeline:
bash scripts/daily_gir_automation.sh
```
