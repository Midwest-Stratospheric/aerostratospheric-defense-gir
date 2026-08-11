"""Feature 8 — Data freshness SLA metrics."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

DEFAULT_SLA_HOURS = {
    "uogw_anomalies": 12, "usgs_quakes": 6, "nws_alerts": 3, "eonet_events": 12,
    "sentinel2_stac": 36, "donki_cme": 24, "cisa_kev": 48, "default": 24,
}

def parse_utc(ts: str | None) -> datetime | None:
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except Exception:
        return None

def evaluate_freshness(results: list[dict[str, Any]], *, now: datetime | None = None, sla_hours: dict[str, float] | None = None) -> dict[str, Any]:
    now = now or datetime.now(timezone.utc)
    sla = {**DEFAULT_SLA_HOURS, **(sla_hours or {})}
    stale, details = [], []
    for r in results:
        src = r.get("source") or "default"
        limit = float(sla.get(src, sla["default"]))
        fetched = parse_utc(r.get("fetched_at_utc")) or parse_utc(r.get("generated_at_utc"))
        age_h, is_stale = None, False
        if fetched is not None:
            age_h = (now - fetched).total_seconds() / 3600.0
            is_stale = age_h > limit
        elif not r.get("ok"):
            is_stale = True
        if is_stale:
            stale.append(src)
        details.append({"source": src, "age_hours": None if age_h is None else round(age_h, 3), "sla_hours": limit, "stale": is_stale, "ok": bool(r.get("ok"))})
    return {"max_age_hours_target": max(sla.values()), "sources_stale": sorted(set(stale)), "sla_met": len(stale) == 0, "details": details, "evaluated_at_utc": now.strftime("%Y-%m-%dT%H:%M:%SZ")}
