"""Feature 6 — Multi-source event fusion (corroboration scoring)."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
from math import radians, sin, cos, sqrt, atan2

def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0
    p1, p2 = radians(lat1), radians(lat2)
    dp, dl = radians(lat2 - lat1), radians(lon2 - lon1)
    a = sin(dp / 2) ** 2 + cos(p1) * cos(p2) * sin(dl / 2) ** 2
    return 2 * r * atan2(sqrt(a), sqrt(1 - a))

def fuse_events(events: list[dict[str, Any]], *, distance_km: float = 50.0, time_hours: float = 24.0) -> list[dict[str, Any]]:
    parsed = []
    for e in events:
        try:
            t = datetime.fromisoformat(str(e["time_utc"]).replace("Z", "+00:00"))
        except Exception:
            continue
        parsed.append({**e, "_t": t})
    used, clusters = set(), []
    for i, e in enumerate(parsed):
        if i in used:
            continue
        members = [e]
        used.add(i)
        for j, o in enumerate(parsed):
            if j in used:
                continue
            if haversine_km(e["lat"], e["lon"], o["lat"], o["lon"]) > distance_km:
                continue
            if abs((e["_t"] - o["_t"]).total_seconds()) > time_hours * 3600:
                continue
            members.append(o)
            used.add(j)
        sources = sorted({m["source"] for m in members})
        clusters.append({
            "cluster_id": f"fuse-{len(clusters)+1:04d}",
            "member_count": len(members),
            "sources": sources,
            "corroboration_score": round(len(sources) / max(len(members), 1), 4),
            "unique_source_count": len(sources),
            "centroid": {"lat": sum(m["lat"] for m in members) / len(members), "lon": sum(m["lon"] for m in members) / len(members)},
            "labels": [m.get("label") for m in members if m.get("label")],
            "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        })
    return clusters
