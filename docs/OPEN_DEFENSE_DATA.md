# Open Defense Data Strategy (Public GIR)

## Principle

This repository holds **open and publicly licensed** defense-adjacent data only.

| Allowed | Not allowed |
|---------|-------------|
| Public government datasets | Classified / FOUO / CUI without authority |
| Academic conflict research under license | Targeting or kinetic products |
| Keyword-flagged public airfield databases | Live tactical unit locations from non-public sources |
| Cyber KEV / NVD public catalogs | Exploits or weaponization guides |
| Open EO, weather, space weather | Export-controlled technical data packages |

## Layers for a comprehensive open defense GIR

1. **Reference basemap** — Natural Earth, OSM, NASADEM  
2. **Civil + published military airfields** — OurAirports heuristics (this repo)  
3. **Maritime** — World Port Index, public AIS portals  
4. **Hazard & anomaly** — UOGW, EONET, USGS, NWS, FIRMS  
5. **Conflict research** — UCDP (cite), ACLED under partner agreement  
6. **Cyber defense open** — CISA KEV, NVD  
7. **Federal transparency** — USAspending, SAM.gov entity/opportunity data  
8. **Aviation state** — OpenSky ADS-B (public broadcasts only)  
9. **Space weather** — DONKI  
10. **Mission products** — Partner/restricted Aerodefener outputs (not in public git)

## Partner / Restricted (not in public git)

- Aerodefener RF anomaly and fused threat products  
- Controlled partner imagery  
- Any dataset requiring government-to-government channels  

## Implemented in daily ingest (public)

| Source | Status |
|--------|--------|
| UOGW, EONET, USGS, NWS, DONKI, Sentinel-2 | Daily |
| CISA KEV | Daily |
| OurAirports military-keyword airfields | Daily |
| USAspending defense NAICS (90-day) | Daily |
| GDELT lastupdate pointers | Daily |
| OpenSky Midwest ADS-B snapshot | Best-effort (rate limits) |
| OSM landuse=military (IL sample bbox) | Daily sample |
| FIRMS VIIRS USA | When FIRMS_MAP_KEY is set |
| UCDP / ACLED | Registration / partner key — stubs only in public repo |

## Partner tier private repo (suggested)

Create `aerostratospheric-defense-gir-restricted` (private) for:

- Aerodefener restricted products  
- ACLED extracts under license  
- Partner EO  
