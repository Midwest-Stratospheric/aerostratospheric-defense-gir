#!/usr/bin/env python3
"""Compute US open-tier situational status for the GIR web banner. NOT military DEFCON."""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = DATA / "status"
OUT.mkdir(parents=True, exist_ok=True)

def load(rel):
    p = DATA / rel
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None

def level_rank(level):
    return {"GREEN": 0, "YELLOW": 1, "ORANGE": 2, "RED": 3, "UNKNOWN": -1}.get(level, -1)

def main():
    factors = []
    nws = load("events/nws_active_alerts_latest.geojson")
    n_nws = len((nws or {}).get("features") or [])
    if n_nws >= 250:
        factors.append({"id": "nws_alerts", "level": "ORANGE", "detail": f"{n_nws} active NWS alerts (high volume)"})
    elif n_nws >= 80:
        factors.append({"id": "nws_alerts", "level": "YELLOW", "detail": f"{n_nws} active NWS alerts"})
    else:
        factors.append({"id": "nws_alerts", "level": "GREEN", "detail": f"{n_nws} active NWS alerts"})
    quakes = load("events/usgs_quakes_2.5_day_latest.geojson")
    feats = (quakes or {}).get("features") or []
    max_mag = 0.0
    for f in feats:
        try:
            max_mag = max(max_mag, float((f.get("properties") or {}).get("mag") or 0))
        except Exception:
            pass
    if max_mag >= 6.5:
        factors.append({"id": "usgs", "level": "ORANGE", "detail": f"Max M{max_mag:.1f} in past-day open feed"})
    elif max_mag >= 5.0:
        factors.append({"id": "usgs", "level": "YELLOW", "detail": f"Max M{max_mag:.1f}"})
    else:
        factors.append({"id": "usgs", "level": "GREEN", "detail": f"Max M{max_mag:.1f}; routine"})
    uogw = load("anomalies/uogw_anomalies_latest.json") or {}
    counts = uogw.get("counts") or {}
    alerts = int(counts.get("alert") or 0)
    watches = int(counts.get("watch") or 0)
    if alerts >= 5:
        factors.append({"id": "uogw", "level": "ORANGE", "detail": f"{alerts} UOGW alert flags"})
    elif alerts >= 1 or watches >= 5:
        factors.append({"id": "uogw", "level": "YELLOW", "detail": f"{alerts} alert / {watches} watch"})
    else:
        factors.append({"id": "uogw", "level": "GREEN", "detail": "UOGW quiet"})
    flights = load("flight_logs/flight_logs_latest.json") or {}
    active = [f for f in (flights.get("flights") or []) if f.get("status") == "active"]
    factors.append({"id": "flight_ops", "level": "YELLOW" if active else "GREEN", "detail": f"{len(active)} active public research flight(s)" if active else "No active public research flights"})
    overall = "GREEN"
    for f in factors:
        if level_rank(f["level"]) > level_rank(overall):
            overall = f["level"]
    messages = {
        "GREEN": "Open-tier US picture: routine public hazard and research indicators.",
        "YELLOW": "Open-tier US picture: elevated public alerts or research flags — monitor official sources.",
        "ORANGE": "Open-tier US picture: significant public hazard indicators — rely on NWS/USGS/CISA official channels.",
        "RED": "Open-tier US picture: severe public indicators — this is not a classified defense status.",
    }
    doc = {
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tier": "open",
        "scope": "United States — public open-tier indicators only",
        "disclaimer": "NOT military DEFCON/FPCON or classified readiness.",
        "overall_level": overall,
        "overall_message": messages.get(overall, messages["GREEN"]),
        "factors": factors,
    }
    OUT.joinpath("us_open_conditions_latest.json").write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(overall)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
