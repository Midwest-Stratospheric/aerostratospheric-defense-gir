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

## Daily automation

`scripts/ingest_open_tier.py` already pulls open streams.  
ACLED/GDELT full history and OpenSky live snapshots can be added behind API keys in a private Actions secret workflow later.
