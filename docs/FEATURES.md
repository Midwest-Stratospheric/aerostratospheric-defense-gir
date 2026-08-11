# GIR feature set (v1.4 scientific open tier)

Ten engineered capabilities for a robust, research-grade open repository.

| # | Feature | Code / artifacts | Output |
|---|---------|------------------|--------|
| 1 | **Provenance & integrity** | `scripts/lib/provenance.py` | `*.prov.json` sidecars with SHA-256, license, source URL |
| 2 | **Schema validation** | `scripts/lib/validate.py`, `schema/manifest_v2.json` | Completeness score + error list in quality report |
| 3 | **Temporal version index** | `data/temporal/run_index.jsonl` | Append-only run history for change detection |
| 4 | **AOI spatial filters** | `config/aoi_regions.json`, `scripts/lib/aoi.py` | Per-region USGS subsets under `data/events/usgs_quakes_aoi_*.geojson` |
| 5 | **Statistical baselines** | `scripts/lib/baseline.py` | Rolling μ, σ, z-flag store in `data/quality/baseline_store.json` |
| 6 | **Multi-source fusion** | `scripts/lib/fusion.py` | Corroboration clusters in `data/quality/fusion_clusters_latest.json` |
| 7 | **STAC export** | `scripts/lib/stac_export.py` | `data/stac/collection.json`, `items_latest.json` |
| 8 | **Freshness SLA** | `scripts/lib/freshness.py` | `sla_met`, stale source list on manifest v2 |
| 9 | **Research citation package** | `CITATION.cff` | Citable software/data artifact |
| 10 | **Scientific methodology** | `docs/methodology/` | Methods + uncertainty statements |

## Run

```bash
python3 scripts/ingest_open_tier.py
python3 scripts/gir_quality_suite.py
python3 scripts/generate_gir_charts.py
```

Or: `bash scripts/daily_gir_automation.sh`
