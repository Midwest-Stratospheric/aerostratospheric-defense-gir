# Aerostratospheric Defense GIR

**Open Geospatial Information Repository** — public data backbone for [Aerostratospheric](https://midwestsds.com/) Defense Systems.

[![Daily automation](https://img.shields.io/badge/updates-twice%20daily%20UTC-00d4ff)](.github/workflows/daily-gir.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-slategray.svg)](LICENSE)
[![Open data only](https://img.shields.io/badge/data-public%20open%20tier-34d399)](docs/DATA_POLICY.md)
[![SAM.gov](https://img.shields.io/badge/SAM.gov-registered-0f2744)](https://midwestsds.com/)
[![Charts](https://img.shields.io/badge/charts-SVG%20in%20git-00d4ff)](docs/charts/)

> We automatically collect free, public map and hazard information, organize it, and save dated copies — without secret military data.

**Web page:** [Defense GIR](https://midwestsds.com/aerostratospheric-defense-gir.html) · **Chart gallery:** [docs/charts/](docs/charts/)

```bash
python3 scripts/generate_gir_charts.py   # rebuild SVGs from open-tier JSON
```

---

## Live visual charts

These **SVG** files are committed in git and render as images on GitHub.

### Data flow

![GIR data flow](docs/charts/gir_data_flow.svg)

### Ingest health

![Ingest status](docs/charts/ingest_status.svg)

![Ingest sources](docs/charts/ingest_sources.svg)

### UOGW anomalies (public research flags)

![UOGW severity](docs/charts/uogw_severity.svg)

### USGS earthquakes (M2.5+, past day)

![USGS magnitudes](docs/charts/usgs_mags.svg)

### Sentinel-2 cloud cover (indexed scenes)

![Sentinel-2 clouds](docs/charts/sentinel2_clouds.svg)

### More charts

See the full set under **[docs/charts/](docs/charts/)** (airfields, USAspending, and others regenerate with the script).

---

## What is a GIR?

| Word | Meaning |
|------|--------|
| Geospatial | Facts with a place on Earth |
| Information | Quakes, alerts, satellite catalogs, cyber lists, … |
| Repository | Versioned digital filing cabinet |

Open briefing binder for the public layer of awareness — not targeting, not classified storage, not weapons.

### Access tiers

```mermaid
flowchart TB
  O["Open — this public repo"] --> P["Partner — agreement"] --> R["Restricted — authorized only"]
```

---

## Satellite & EO (open)

Library-card indexes for free imagery (Sentinel, Landsat, MODIS/VIIRS, GOES) — not a secret image vault. Path: `data/imagery_index/`.

## Military-marked public landmarks

OurAirports **keyword heuristic** (names like “Air Force Base”) — **not** an official basing list. OSM `landuse=military` sample is volunteer ODbL data only. Path: `data/defense_open/`.

## Alerts, disasters & hazards

USGS · NWS · EONET · UOGW · DONKI · FIRMS (optional key) — public hazard board. Paths: `data/events/`, `data/anomalies/`.

## Conflict context

Public: GDELT pointers, hazards, KEV, spending samples. Partner: ACLED / UCDP under license. Restricted: Aerodefener products — not in public git.

## Cyber & spending

CISA KEV + USAspending selected NAICS — open transparency data only.

---

## Automation

1. Ingest open feeds  
2. `generate_gir_charts.py` → SVG charts in `docs/charts/`  
3. Git commit when data changes  

```bash
bash scripts/daily_gir_automation.sh
```

Schedule: 06:00 & 18:00 UTC.

---

## Links

| Resource | URL |
|----------|-----|
| Defense GIR page | https://midwestsds.com/aerostratospheric-defense-gir.html |
| Defense Systems | https://midwestsds.com/aerostratospheric-defense-systems.html |
| Contact | https://midwestsds.com/contact/index.php?a=add |

Aerostratospheric is a **registered SAM.gov entity**. Passive sensing · intelligence support · communications — no kinetic weapons. Open-tier data is not an official warning service.
