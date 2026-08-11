# Aerostratospheric Defense GIR

**Geospatial Information Repository** — open-tier data backbone for [Aerostratospheric](https://midwestsds.com/) Defense Systems.

[![Daily GIR ingest](https://img.shields.io/badge/automation-daily%20UTC-00d4ff)](.github/workflows/daily-gir.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-slategray.svg)](LICENSE)

## Purpose

Versioned open geospatial feeds that support Aerostratospheric defense platforms:

- Public anomaly screening (UOGW)
- Natural events (NASA EONET)
- Worldwide open satellite / EO source catalog + STAC scene indexes
- Public reference features (civil airports, ports, maritime chokepoints, ops nodes)

**This repository is open-tier only.** Partner and restricted defense products are not stored here.

## Quick start

```bash
# Daily ingest (UOGW + EONET) and optional STAC index
bash scripts/daily_gir_automation.sh

# Sentinel-2 search over a bbox (W S E N)
python3 scripts/stac_search_sentinel2.py --bbox -88.2 39.1 -87.7 39.5 --limit 8
```

## Layout

```
schema/     GIR schema and access tiers
catalog/    Open satellite sources + public OSINT/reference feeds
data/
  anomalies/      UOGW anomaly snapshots
  events/         EONET open events
  imagery_index/  STAC search results
  reference/      Public GeoJSON/JSON features
scripts/    Ingest + daily automation + cron installer
docs/       Data policy and automation notes
.github/workflows/  Daily Actions schedule (06:00 UTC)
```

## Access tiers

| Tier | Contents |
|------|----------|
| **Open** | Public EO catalogs, UOGW, EONET, civil reference features |
| **Partner** | Controlled products under written agreement (not in this repo) |
| **Restricted** | Authorized government/military only (not in this repo) |

## Policy

- No classified military intelligence in this tree  
- No kinetic or targeting products  
- Satellite imagery is **indexed/queried** via open STAC APIs — full global archives are not mirrored  
- Attribute ESA Copernicus, USGS, NASA, NOAA, and other providers per their terms  

See [docs/DATA_POLICY.md](docs/DATA_POLICY.md).

## Automation

- Local: `scripts/daily_gir_automation.sh` (+ optional `scripts/install_cron.sh`)  
- GitHub Actions: `.github/workflows/daily-gir.yml` — runs daily at **06:00 UTC** and on manual dispatch  

## Related

- Site: https://midwestsds.com/  
- Data Hub: https://midwestsds.com/msds-data-hub.html  
- Contact (gov/military): https://midwestsds.com/contact/index.php?a=add  

Aerostratospheric is a registered SAM.gov entity. Passive sensing, intelligence, and communications systems only.
