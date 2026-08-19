#!/usr/bin/env python3
"""Generate daily GIR executive summary from open-tier data files.

Writes:
  reports/daily/YYYY-MM-DD-gir-exec.md
  reports/latest.md  (pointer)

Pure stdlib. Open-tier public data only. Research screening — not an official product.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
DAILY = REPORTS / "daily"


def load_json(rel: str | Path):
    p = DATA / rel if not str(rel).startswith("/") else Path(rel)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def age_hours(iso_str: str | None) -> float | None:
    if not iso_str:
        return None
    try:
        # tolerate Z or +00:00
        s = iso_str.replace("Z", "+00:00")
        ts = datetime.fromisoformat(s)
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - ts).total_seconds() / 3600.0
    except Exception:
        return None


def main() -> int:
    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")
    gen_stamp = now.strftime("%Y-%m-%d %H:%M UTC")

    manifest = load_json("manifests/manifest_latest.json") or {}
    quality = load_json("quality/quality_report_latest.json") or {}
    temporal = load_json("temporal/latest_run.json") or {}
    uogw = load_json("anomalies/uogw_anomalies_latest.json") or {}
    eonet = load_json("events/eonet_open_latest.json") or {}
    status = load_json("status/us_open_conditions_latest.json") or {}

    # ---- Quality / completeness assessment ----
    ok = int(manifest.get("ok") or 0)
    total = int(manifest.get("total") or 0)
    gen_at = manifest.get("generated_at_utc")
    m_age = age_hours(gen_at)

    flagged = []
    for r in manifest.get("results") or []:
        src = r.get("source", "?")
        if not r.get("ok"):
            flagged.append(f"{src} (failed)")
        elif r.get("status") == "awaiting_key":
            flagged.append(f"{src} (awaiting_key)")
        elif "timeout" in str(r.get("error", "")).lower():
            flagged.append(f"{src} (timeout)")

    # Stale secondary artifacts
    q_age = age_hours(quality.get("generated_at_utc"))
    t_age = age_hours(temporal.get("ts"))
    s_age = age_hours(status.get("generated_at_utc"))

    if total == 0:
        q_status = "Gap detected"
    elif flagged or (m_age is not None and m_age > 36):
        q_status = "Warning"
    else:
        q_status = "OK"

    completeness_note = ""
    if temporal.get("completeness_score") is not None:
        completeness_note = f" (historical completeness_score {temporal.get('completeness_score')})"
    elif quality.get("completeness_note"):
        completeness_note = f" ({quality.get('completeness_note')})"

    # ---- Key counts from manifest results ----
    counts = {}
    for r in manifest.get("results") or []:
        src = r.get("source", "")
        if "events" in r:
            counts[src] = r["events"]
        elif "features" in r:
            counts[src] = r["features"]
        elif "count" in r:
            counts[src] = r["count"]
        elif "scenes" in r:
            counts[src] = r["scenes"]
        elif "counts" in r and isinstance(r["counts"], dict):
            counts[src] = r["counts"]
        elif "status" in r:
            counts[src] = r["status"]
        elif "files" in r:
            counts[src] = r["files"]

    # ---- Anomalies summary ----
    anom_counts = (uogw.get("counts") or {})
    anom_list = uogw.get("anomalies") or []
    anom_bullets = []
    for a in anom_list[:8]:
        sev = a.get("severity", "?")
        subj = a.get("subject", "?")
        kind = a.get("kind", "")
        detail = a.get("detail") or a.get("metric", "")
        anom_bullets.append(f"- **{sev.title()}** — {subj}: {kind} ({detail})")

    # ---- EONET highlights (first few open events) ----
    eonet_events = eonet.get("events") or []
    eonet_n = len(eonet_events)
    eonet_bullets = []
    for ev in eonet_events[:6]:
        title = ev.get("title", "?")
        cats = ", ".join(c.get("title", "") for c in (ev.get("categories") or []))
        eonet_bullets.append(f"- {title} ({cats})")

    # ---- Status banner ----
    overall_level = status.get("overall_level", "—")
    overall_msg = status.get("overall_message", "")

    # ---- Build markdown ----
    lines = []
    lines.append(f"# GIR Daily Executive Summary — {today}")
    lines.append(f"**Generated:** {gen_stamp}")
    lines.append("")
    lines.append("## Data Quality / Completeness")
    lines.append(f"**Status: {q_status}**{completeness_note}")
    lines.append("")
    lines.append(f"- Manifest (`manifest_latest.json`): **{ok}/{total} sources OK**" +
                 (f" (generated {gen_at})" if gen_at else ""))
    if m_age is not None:
        lines.append(f"- Manifest age: ~{m_age:.1f} h")
    if flagged:
        lines.append(f"- Flagged sources: {', '.join(flagged)}")
    else:
        lines.append("- No failed sources in latest manifest.")
    stale_notes = []
    if q_age is not None and q_age > 36:
        stale_notes.append(f"quality_report ~{q_age:.0f}h old")
    if t_age is not None and t_age > 36:
        stale_notes.append(f"temporal/latest_run ~{t_age:.0f}h old")
    if s_age is not None and s_age > 36:
        stale_notes.append(f"us_open_conditions ~{s_age:.0f}h old")
    if stale_notes:
        lines.append(f"- Secondary artifacts lagging: {'; '.join(stale_notes)}")
    lines.append("")

    lines.append("## Key Observations (Open-tier feeds)")
    lines.append("")
    lines.append("| Source | Count / Status |")
    lines.append("|--------|----------------|")

    # Preferred display order
    preferred = [
        ("eonet_events", "EONET events"),
        ("nws_alerts", "NWS active alerts"),
        ("usgs_quakes", "USGS quakes (M2.5+ day)"),
        ("opensky_midwest", "OpenSky Midwest snapshot"),
        ("cisa_kev", "CISA KEV"),
        ("sentinel2_stac", "Sentinel-2 STAC scenes"),
        ("donki_cme", "DONKI CME"),
        ("uogw_anomalies", "UOGW anomalies"),
        ("ourairports_military_keywords", "OurAirports military keywords"),
        ("usaspending_defense", "USASpending defense sample"),
        ("osm_military_landuse", "OSM military landuse (IL sample)"),
        ("gdelt_lastupdate", "GDELT lastupdate"),
        ("firms", "FIRMS"),
        ("partner_stubs", "Partner stubs"),
    ]
    seen = set()
    for key, label in preferred:
        if key in counts:
            val = counts[key]
            if isinstance(val, dict):
                val = f"{val.get('total', '?')} total ({val.get('alert', 0)} alert / {val.get('watch', 0)} watch)"
            lines.append(f"| {label} | {val} |")
            seen.add(key)
    for key, val in counts.items():
        if key not in seen:
            if isinstance(val, dict):
                val = str(val)
            lines.append(f"| {key} | {val} |")
    lines.append("")

    if overall_level and overall_level != "—":
        lines.append(f"**US open-status banner:** {overall_level} — {overall_msg}")
        lines.append("")

    lines.append("## Anomalies or Notable Events")
    if anom_bullets:
        lines.append(f"- **UOGW research anomalies** ({anom_counts.get('total', len(anom_list))} total: "
                     f"{anom_counts.get('alert', 0)} alert / {anom_counts.get('watch', 0)} watch):")
        lines.extend(anom_bullets)
    else:
        lines.append("- No UOGW anomalies in latest report (or file missing).")
    lines.append("")
    if eonet_n:
        lines.append(f"- **EONET open events:** {eonet_n} total. Sample:")
        lines.extend(eonet_bullets)
        if eonet_n > 6:
            lines.append(f"  … and {eonet_n - 6} more (see `data/events/eonet_open_latest.json`).")
    else:
        lines.append("- EONET events file missing or empty.")
    lines.append("")

    lines.append("## Recommended Actions")
    actions = []
    if any("firms" in f for f in flagged) or counts.get("firms") == "awaiting_key":
        actions.append("1. Supply / rotate `FIRMS_MAP_KEY` secret so fire detections can be ingested.")
    if stale_notes:
        actions.append("2. Ensure `compute_us_open_status.py` and quality/temporal jobs run in the same daily pipeline so secondary artifacts stay fresh.")
    if not actions:
        actions.append("1. Continue routine open-tier Actions schedule; no critical gaps in latest manifest.")
    actions.append("3. Review NWS / USGS / EONET official channels for any operational decisions (this summary is research screening only).")
    lines.extend(actions)
    lines.append("")
    lines.append("---")
    lines.append("*Open-tier public data only. Research screening — not an official product. Aerostratospheric Defense GIR.*")
    lines.append("")

    md = "\n".join(lines)

    DAILY.mkdir(parents=True, exist_ok=True)
    out_path = DAILY / f"{today}-gir-exec.md"
    out_path.write_text(md, encoding="utf-8")
    print(f"Wrote {out_path}")

    # Pointer
    REPORTS.mkdir(parents=True, exist_ok=True)
    pointer = (
        f"# Latest GIR Daily Executive Summary\n\n"
        f"**Pointer:** [{today}](daily/{today}-gir-exec.md)\n\n"
        f"See `reports/daily/` for dated archives.\n"
    )
    (REPORTS / "latest.md").write_text(pointer, encoding="utf-8")
    print(f"Updated reports/latest.md → {today}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
