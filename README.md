# Aerostratospheric Defense GIR

**A plain-language guide to our open Geospatial Information Repository**

[![Daily automation](https://img.shields.io/badge/updates-twice%20daily%20UTC-00d4ff)](.github/workflows/daily-gir.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-slategray.svg)](LICENSE)
[![Open data only](https://img.shields.io/badge/data-public%20open%20tier-34d399)](docs/DATA_POLICY.md)
[![SAM.gov](https://img.shields.io/badge/SAM.gov-registered-0f2744)](https://midwestsds.com/)
[![Charts](https://img.shields.io/badge/charts-SVG%20in%20git-00d4ff)](docs/charts/)

> **In one sentence:** We automatically collect free, public map and hazard information, organize it, and save dated copies here — without secret military data.

**Live web page:** [Defense GIR on midwestsds.com](https://midwestsds.com/aerostratospheric-defense-gir.html) · **Charts:** [docs/charts/](docs/charts/) · **Status JSON:** [data/status/](data/status/) · **Latest report:** [reports/latest.md](reports/latest.md)

---

## What is this, in plain English?

Imagine you need a **shared notebook of public facts about the world**—storms that were already warned about, earthquakes that already happened, free satellite “library cards,” public cyber patch lists, and open research balloon flight summaries. You do **not** want secrets. You want something you can audit, re-run, and explain to a non-specialist.

That notebook is this repository.

**GIR** means **Geospatial Information Repository**: place-based information stored in an organized library. Software here downloads free public feeds on a schedule, checks whether the download worked, keeps a short history in git, draws simple charts, and publishes a **US open-status** summary for the website banner. Partner or restricted sensor products from Aerostratospheric platforms (when fielded) stay **out** of this public tree on purpose.

Think of it as the **weather-and-world briefing binder** that sits beside more sensitive tools—not the classified mission folder, not a weapons system, and not a substitute for official emergency alerts on your phone.

| Word | Everyday meaning |
|------|------------------|
| **Geospatial** | Facts tied to a place on Earth |
| **Information** | Measurements and events (quakes, alerts, satellite catalogs, public cyber lists, flight log summaries, …) |
| **Repository** | An organized digital filing cabinet with history |

---

## How it is used (sample use cases)

These examples are **open-tier** only. They describe realistic ways people and programs use this kind of public data—not targeting, not classified operations.

### 1. Morning open briefing for a small research team
A Midwest balloon or environmental team opens the [GIR web page](https://midwestsds.com/aerostratospheric-defense-gir.html), checks the **US open status** strip (GREEN/YELLOW/…), skims NWS and USGS charts, and notes whether any **public research flight** is marked active in the flight log. Decision: proceed with a dry-run checklist or delay outdoor recovery training if public weather alerts are elevated in the ops area.

### 2. “What can an uncleared partner already see?”
Before a partner discussion, staff review the **Sentinel-2 index** and public hazard layers. That answers a simple question in lay terms: *which free satellite scenes and public alerts already exist for this region?* It sets expectations before anyone talks about higher-tier or restricted products.

### 3. Classroom or STEM outreach
A teacher uses the earthquake magnitude chart and EONET categories to show how open science feeds work. Students learn that “defense-adjacent” public data can mean **weather, disasters, and transparency lists**—not secret bases. The README and charts are designed so a non-engineer can follow along.

### 4. Cyber hygiene desk check
An IT lead glances at the **CISA KEV** sample in `data/defense_open/`. It is a public “patch these known-exploited holes first” catalog. Use case: remind the team that open GIR is also a pointer to ordinary cyber hygiene, not a live attack map.

### 5. Flight log continuity for public launches
When Aerostratospheric / MSDS publishes a **public** balloon event summary, it is appended to `data/flight_logs/`. Use case: one place for the public timeline (planned / complete / dry-run) that matches website messaging—without publishing sensitive recovery coordinates or restricted telemetry.

### 6. Automation and reproducibility
A developer runs:

```bash
python3 scripts/ingest_open_tier.py
python3 scripts/compute_us_open_status.py
python3 scripts/generate_gir_charts.py
python3 scripts/generate_daily_exec_summary.py
```

Use case: prove that yesterday’s charts, status, and executive summary can be rebuilt from scripts + public sources, with git history as the audit trail.

### 7. Grant / SAM.gov narrative support
Because Aerostratospheric is a **registered SAM.gov entity**, open GIR materials can illustrate a responsible open-data posture: public inputs, clear tiers, disclaimers, and no claim to replace NWS, USGS, or military command systems.

**Non-use cases (on purpose):** sole life-safety alerting, classified basing lists, targeting folders, or kinetic system control.

---

## Executive reports

Open-tier **daily executive summaries** are generated automatically by the same GitHub Actions pipeline that refreshes the data. They focus on data quality / completeness, key open-source counts (NWS, USGS, EONET, UOGW, OpenSky, CISA KEV, etc.), notable anomalies, and short recommended actions.

| Resource | Link |
|----------|------|
| **Latest summary** | [reports/latest.md](reports/latest.md) |
| **Daily archive** | [reports/daily/](reports/daily/) |

Each file is named `YYYY-MM-DD-gir-exec.md`. The pipeline also keeps the US open-status banner and Mermaid charts in sync. Weekly roll-up reports can be added to the same automation later if needed.

---

## Live visual charts

These **SVG** files are committed in git and render as images on GitHub.

```bash
python3 scripts/generate_gir_charts.py
```

See **[docs/charts/](docs/charts/)** for the full category gallery (manifests, anomalies, events, imagery, defense-open, quality, temporal).

---

## Access tiers

```mermaid
flowchart TB
  O["Open — this public repo"] --> P["Partner — agreement"] --> R["Restricted — authorized only"]
```

---

## What’s inside (short tour)

| Area | Plain meaning |
|------|----------------|
| **Satellite / EO** | Library-card indexes for free imagery (Sentinel, Landsat, …) |
| **Military-marked (public)** | Keyword heuristics on public airport names — **not** official basing |
| **Alerts & hazards** | USGS, NWS, EONET, UOGW, DONKI |
| **Cyber & spending** | CISA KEV + USAspending samples |
| **Flight logs** | Public research balloon / test summaries |
| **US open status** | Banner levels from public feeds only — **not** DEFCON |
| **Executive reports** | Daily (and optional weekly) open-tier briefing summaries |

---

## Automation

```bash
bash scripts/daily_gir_automation.sh
```

Schedule: **06:00** and **18:00 UTC** (plus manual Actions dispatch).

The automation runs open-tier ingest → US open-status → charts → daily executive summary → git commit.

---

## Links

| Resource | URL |
|----------|-----|
| Defense GIR page | https://midwestsds.com/aerostratospheric-defense-gir.html |
| Defense Systems | https://midwestsds.com/aerostratospheric-defense-systems.html |
| Latest exec report | [reports/latest.md](reports/latest.md) |
| Daily report archive | [reports/daily/](reports/daily/) |
| Contact | https://midwestsds.com/contact/index.php?a=add |

Aerostratospheric is a **registered SAM.gov entity**. Passive sensing · intelligence support · communications — **no kinetic weapons**. Open-tier data is not an official warning service alone.
