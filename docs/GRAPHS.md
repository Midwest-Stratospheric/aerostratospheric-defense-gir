# GIR graphs (git markup)

_Generated 2026-09-03 10:48 UTC from open-tier data. Mermaid only — no image binaries._

Regenerate:

```bash
python3 scripts/generate_gir_charts.py
```

## Data flow

```mermaid
flowchart LR
  A["Public feeds"] --> B["Ingest scripts"]
  C["Open defense sources"] --> B
  B --> D["data folders"]
  D --> E["manifest"]
  E --> F["git commit"]
  D --> G["Defense GIR page / maps"]
```

## Access tiers

```mermaid
flowchart TB
  O["Open tier — this public repo"]
  P["Partner tier — agreements"]
  R["Restricted — authorized only"]
  O --> P --> R
```

## Daily ingest status

**Last run:** `2026-09-03T10:48:17.209107+00:00` · **14/15 sources OK**

```mermaid
pie showData
  title Ingest sources OK vs failed (14/15)
  "OK" : 14
  "Failed or skipped" : 1
```

| Source | Status |
|--------|--------|
| `uogw_anomalies` | OK |
| `eonet_events` | OK |
| `eonet_geojson` | OK |
| `usgs_quakes` | OK |
| `nws_alerts` | OK |
| `sentinel2_stac` | OK |
| `donki_cme` | OK |
| `cisa_kev` | OK |
| `ourairports_military_keywords` | OK |
| `usaspending_defense` | OK |
| `gdelt_lastupdate` | OK |
| `opensky_midwest` | OK |
| `osm_military_landuse` | FAIL |
| `firms` | OK |
| `partner_stubs` | OK |

## UOGW anomaly severity

Public anomaly flags (research-style). Not official emergency alerts.

```mermaid
pie showData
  title UOGW counts by severity
  "alert" : 2
  "watch" : 1
  "info" : 0
```

| alert | watch | info |
|-------|-------|------|
| 2 | 1 | 0 |

## USGS earthquakes (M2.5+, past day)

**Events:** 28

```mermaid
xychart-beta
  title "Quake count by magnitude band"
  x-axis ["2.5-3.4", "3.5-4.4", "4.5-5.4", "5.5+"]
  y-axis "Count" 0 --> 13
  bar [13, 2, 10, 3]
```

## Public keyword-flagged airfields by country

> Heuristic from public OurAirports — **not** an official basing list.

**Records:** 259

```mermaid
xychart-beta
  title "Top countries (keyword heuristic)"
  x-axis ["US", "IN", "RO", "ZA", "RU", "TW", "KR", "CA", "BR", "NL", "AU", "IL"]
  y-axis "Count" 0 --> 130
  bar [130, 40, 8, 5, 4, 4, 4, 3, 3, 3, 3, 3]
```

---

Open tier only. See OPEN_DEFENSE_DATA.md and DATA_POLICY.md.
