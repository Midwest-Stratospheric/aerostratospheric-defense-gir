# GIR feature set (v1.6 scientific open tier)

## Core quality & science features

| # | Feature | Code / artifacts | Output |
|---|---------|------------------|--------|
| 1 | **Provenance & integrity** | `scripts/lib/provenance.py` | `*.prov.json` sidecars |
| 2 | **Schema validation** | `scripts/lib/validate.py` | Quality report |
| 3 | **Temporal version index** | `data/temporal/` | Run history |
| 4 | **AOI spatial filters** | `scripts/lib/aoi.py` | Per-region subsets |
| 5 | **Statistical baselines** | `scripts/lib/baseline.py` | Rolling z-flags |
| 6 | **Multi-source fusion** | `scripts/lib/fusion.py` | Clusters |
| 7 | **STAC export** | `scripts/lib/stac_export.py` | STAC items |
| 8 | **Freshness SLA** | `scripts/lib/freshness.py` | Stale source list |
| 9 | **Research citation** | `CITATION.cff` | Citable artifact |
| 10 | **Scientific methodology** | `docs/methodology/` | Methods notes |

## New scientific suite (v1.6)

| # | Feature | Script | Output |
|---|---------|--------|--------|
| 17 | **Quality scorecard** | `generate_scientific_features.py` | `data/quality/scientific_scorecard_latest.json` — grade A–F from completeness × freshness × integrity |
| 18 | **Change detection** | same | `data/quality/change_detection_latest.json` — status flips + count deltas vs prior run |
| 19 | **Coverage report** | same | `data/quality/coverage_report_latest.json` — hazards / EO / defense-open layer inventory |
| 20 | **FAIR package card** | same | `data/quality/fair_package_card_latest.json` + `reports/scientific/` digest |

## Daily automation & products

| # | Feature | Output |
|---|---------|--------|
| 11–16 | Ingest, US status, charts, exec summary, Actions, auto-rerun | See `docs/DAILY_AUTOMATION.md` |

## Run

```bash
bash scripts/daily_gir_automation.sh
# or:
python3 scripts/generate_scientific_features.py
```
