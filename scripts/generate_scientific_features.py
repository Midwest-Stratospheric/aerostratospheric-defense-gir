#!/usr/bin/env python3
"""GIR scientific feature suite (4 modules).

1. Quality scorecard — completeness, freshness, integrity composite
2. Change detection — deltas vs previous scorecard/manifest snapshot
3. Coverage report — open-tier observing-system inventory
4. FAIR package card — research-ready citation / reuse metadata

Outputs under data/quality/ and reports/scientific/.
"""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
QUALITY = ROOT / "data" / "quality"
REPORTS = ROOT / "reports" / "scientific"
MANIFEST = ROOT / "data" / "manifests" / "manifest_latest.json"


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime | None = None) -> str:
    return (dt or now_utc()).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def write_json(path: Path, doc: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def file_sha256(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_ts(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        s2 = s.replace("Z", "+00:00")
        return datetime.fromisoformat(s2)
    except Exception:
        return None


def age_hours(ts: datetime | None, now: datetime) -> float | None:
    if ts is None:
        return None
    return round((now - ts).total_seconds() / 3600.0, 2)


def feature_1_scorecard(manifest: dict, now: datetime) -> dict:
    results = manifest.get("results") or []
    total = int(manifest.get("total") or len(results) or 0)
    ok = int(manifest.get("ok") or sum(1 for r in results if r.get("ok")))
    completeness = round(100.0 * ok / total, 1) if total else 0.0

    gen = parse_ts(manifest.get("generated_at_utc"))
    hours = age_hours(gen, now)
    if hours is None:
        freshness_score = 50.0
        freshness_label = "unknown"
    elif hours <= 12:
        freshness_score, freshness_label = 100.0, "fresh"
    elif hours <= 36:
        freshness_score, freshness_label = 75.0, "acceptable"
    elif hours <= 72:
        freshness_score, freshness_label = 40.0, "stale"
    else:
        freshness_score, freshness_label = 10.0, "very_stale"

    failed = [r.get("source") for r in results if not r.get("ok")]
    awaiting = [
        r.get("source")
        for r in results
        if r.get("ok") and (r.get("status") == "awaiting_key" or r.get("counts") is None and r.get("status"))
    ]
    # integrity: share of ok sources that point at an existing file
    existing = 0
    checked = 0
    for r in results:
        fn = r.get("file")
        if not fn:
            continue
        checked += 1
        # search common data trees
        found = False
        for sub in ("anomalies", "events", "imagery_index", "defense_open", "status", "manifests", "flight_logs"):
            p = ROOT / "data" / sub / fn
            if p.exists():
                found = True
                break
            # nested globs not needed; also try direct under data
            p2 = ROOT / "data" / fn
            if p2.exists():
                found = True
                break
        if found:
            existing += 1
    integrity = round(100.0 * existing / checked, 1) if checked else completeness

    composite = round(0.45 * completeness + 0.30 * freshness_score + 0.25 * integrity, 1)
    if composite >= 90:
        grade = "A"
    elif composite >= 80:
        grade = "B"
    elif composite >= 70:
        grade = "C"
    elif composite >= 60:
        grade = "D"
    else:
        grade = "F"

    return {
        "schema": "gir.scientific_scorecard.v1",
        "generated_at_utc": iso(now),
        "tier": "open",
        "completeness_pct": completeness,
        "sources_ok": ok,
        "sources_total": total,
        "freshness": {
            "manifest_generated_at_utc": manifest.get("generated_at_utc"),
            "age_hours": hours,
            "score": freshness_score,
            "label": freshness_label,
        },
        "integrity_pct": integrity,
        "composite_score": composite,
        "grade": grade,
        "failed_sources": failed,
        "notes": [
            "Composite = 0.45·completeness + 0.30·freshness + 0.25·integrity",
            "Research screening only — not an operational readiness certificate",
        ],
    }


def feature_2_change_detection(scorecard: dict, manifest: dict, now: datetime) -> dict:
    prev_path = QUALITY / "scientific_scorecard_previous.json"
    prev = load_json(prev_path) or {}
    prev_manifest = load_json(QUALITY / "manifest_snapshot_previous.json") or {}

    changes = {
        "schema": "gir.change_detection.v1",
        "generated_at_utc": iso(now),
        "compared_to": prev.get("generated_at_utc"),
        "score_delta": None,
        "completeness_delta_pct": None,
        "source_status_flips": [],
        "count_deltas": [],
        "summary": [],
    }

    if prev:
        changes["score_delta"] = round(
            float(scorecard.get("composite_score", 0)) - float(prev.get("composite_score", 0)), 1
        )
        changes["completeness_delta_pct"] = round(
            float(scorecard.get("completeness_pct", 0)) - float(prev.get("completeness_pct", 0)), 1
        )

    prev_results = {r.get("source"): r for r in (prev_manifest.get("results") or []) if r.get("source")}
    for r in manifest.get("results") or []:
        src = r.get("source")
        if not src:
            continue
        old = prev_results.get(src)
        if old is None:
            continue
        if bool(old.get("ok")) != bool(r.get("ok")):
            changes["source_status_flips"].append(
                {"source": src, "from_ok": bool(old.get("ok")), "to_ok": bool(r.get("ok"))}
            )
        # numeric count fields
        for key in ("count", "events", "features", "scenes", "files"):
            if key in r or key in old:
                a, b = old.get(key), r.get(key)
                if isinstance(a, (int, float)) and isinstance(b, (int, float)) and a != b:
                    changes["count_deltas"].append(
                        {"source": src, "field": key, "from": a, "to": b, "delta": b - a}
                    )
        oc = (old.get("counts") or {})
        nc = (r.get("counts") or {})
        if oc or nc:
            for k in set(list(oc.keys()) + list(nc.keys())):
                a, b = oc.get(k), nc.get(k)
                if isinstance(a, (int, float)) and isinstance(b, (int, float)) and a != b:
                    changes["count_deltas"].append(
                        {"source": src, "field": f"counts.{k}", "from": a, "to": b, "delta": b - a}
                    )

    if changes["score_delta"] is not None:
        changes["summary"].append(f"Composite score Δ {changes['score_delta']}")
    changes["summary"].append(f"Status flips: {len(changes['source_status_flips'])}")
    changes["summary"].append(f"Count deltas: {len(changes['count_deltas'])}")
    if not prev:
        changes["summary"].append("First scorecard baseline established")

    return changes


def feature_3_coverage(manifest: dict, now: datetime) -> dict:
    categories = {
        "hazards_alerts": ["nws_alerts", "usgs_quakes", "eonet_events", "eonet_geojson", "donki_cme"],
        "atmosphere_anomalies": ["uogw_anomalies"],
        "eo_imagery": ["sentinel2_stac", "firms"],
        "defense_open": [
            "cisa_kev",
            "ourairports_military_keywords",
            "usaspending_defense",
            "opensky_midwest",
            "osm_military_landuse",
            "gdelt_lastupdate",
            "partner_stubs",
        ],
    }
    by_src = {r.get("source"): r for r in (manifest.get("results") or [])}

    layers = []
    for name, sources in categories.items():
        present = [s for s in sources if s in by_src]
        ok_n = sum(1 for s in present if by_src[s].get("ok"))
        layers.append(
            {
                "layer": name,
                "sources_configured": len(sources),
                "sources_present": len(present),
                "sources_ok": ok_n,
                "coverage_pct": round(100.0 * ok_n / len(sources), 1) if sources else 0.0,
                "sources": present,
            }
        )

    return {
        "schema": "gir.coverage_report.v1",
        "generated_at_utc": iso(now),
        "tier": "open",
        "purpose": "Observing-system style inventory of open-tier GIR source groups",
        "layers": layers,
        "overall_ok": manifest.get("ok"),
        "overall_total": manifest.get("total"),
        "notes": [
            "Coverage is source-success based, not spatial grid completeness",
            "FIRMS may report ok while status=awaiting_key",
        ],
    }


def feature_4_fair_card(scorecard: dict, coverage: dict, now: datetime) -> dict:
    return {
        "schema": "gir.fair_package_card.v1",
        "generated_at_utc": iso(now),
        "title": "Aerostratospheric Defense GIR open-tier daily package",
        "version_hint": "See GitHub Releases (vMAJOR.MINOR)",
        "repository": "https://github.com/Midwest-Stratospheric/aerostratospheric-defense-gir",
        "license_software": "MIT",
        "license_data": "Retain upstream provider terms (NWS, USGS, NASA, CISA, OSM ODbL, etc.)",
        "findable": {
            "identifiers": ["reports/latest.md", "data/manifests/manifest_latest.json"],
            "keywords": ["geospatial", "open data", "hazards", "EO index", "defense open tier"],
        },
        "accessible": {
            "access": "public git + raw.githubusercontent.com",
            "formats": ["JSON", "GeoJSON", "Markdown", "SVG"],
        },
        "interoperable": {
            "schemas": ["gir.scientific_scorecard.v1", "manifest open-tier"],
            "related": ["Unified-Open-Global-Weather anomaly report"],
        },
        "reusable": {
            "citation": "CITATION.cff",
            "intended_use": "Research screening, education, open situational context",
            "not_for": "Sole life-safety alerting or classified operations",
        },
        "quality_snapshot": {
            "grade": scorecard.get("grade"),
            "composite_score": scorecard.get("composite_score"),
            "completeness_pct": scorecard.get("completeness_pct"),
        },
        "coverage_snapshot": {
            "layers": [L.get("layer") for L in (coverage.get("layers") or [])],
        },
    }


def write_markdown_digest(scorecard: dict, changes: dict, coverage: dict, fair: dict, now: datetime) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# GIR Scientific Features Digest — {now.strftime('%Y-%m-%d')}",
        "",
        f"Generated: {iso(now)}",
        "",
        "## 1. Quality scorecard",
        "",
        f"- Grade: **{scorecard.get('grade')}** (composite {scorecard.get('composite_score')})",
        f"- Completeness: {scorecard.get('completeness_pct')}% "
        f"({scorecard.get('sources_ok')}/{scorecard.get('sources_total')})",
        f"- Freshness: {scorecard.get('freshness', {}).get('label')} "
        f"({scorecard.get('freshness', {}).get('age_hours')} h)",
        f"- Integrity: {scorecard.get('integrity_pct')}%",
        "",
        "## 2. Change detection",
        "",
    ]
    for s in changes.get("summary") or []:
        lines.append(f"- {s}")
    flips = changes.get("source_status_flips") or []
    if flips:
        lines.append("")
        lines.append("Status flips:")
        for f in flips[:12]:
            lines.append(f"- `{f.get('source')}`: {f.get('from_ok')} → {f.get('to_ok')}")
    lines += ["", "## 3. Coverage", ""]
    for L in coverage.get("layers") or []:
        lines.append(
            f"- **{L.get('layer')}**: {L.get('sources_ok')}/{L.get('sources_configured')} ok "
            f"({L.get('coverage_pct')}%)"
        )
    lines += [
        "",
        "## 4. FAIR package card",
        "",
        f"- Title: {fair.get('title')}",
        f"- Repository: {fair.get('repository')}",
        f"- Citation: {fair.get('reusable', {}).get('citation')}",
        "",
        "---",
        "*Open-tier research features — not an official product.*",
        "",
    ]
    text = "\n".join(lines)
    (REPORTS / "latest.md").write_text(text, encoding="utf-8")
    (REPORTS / f"{now.strftime('%Y-%m-%d')}-scientific.md").write_text(text, encoding="utf-8")


def main() -> int:
    now = now_utc()
    QUALITY.mkdir(parents=True, exist_ok=True)
    manifest = load_json(MANIFEST) or {"ok": 0, "total": 0, "results": []}

    # rotate previous baselines
    cur_score_path = QUALITY / "scientific_scorecard_latest.json"
    if cur_score_path.exists():
        (QUALITY / "scientific_scorecard_previous.json").write_text(
            cur_score_path.read_text(encoding="utf-8"), encoding="utf-8"
        )
    if MANIFEST.exists():
        (QUALITY / "manifest_snapshot_previous.json").write_text(
            MANIFEST.read_text(encoding="utf-8"), encoding="utf-8"
        )

    scorecard = feature_1_scorecard(manifest, now)
    # change detection compares to previous files written above
    changes = feature_2_change_detection(scorecard, manifest, now)
    coverage = feature_3_coverage(manifest, now)
    fair = feature_4_fair_card(scorecard, coverage, now)

    write_json(QUALITY / "scientific_scorecard_latest.json", scorecard)
    write_json(QUALITY / "change_detection_latest.json", changes)
    write_json(QUALITY / "coverage_report_latest.json", coverage)
    write_json(QUALITY / "fair_package_card_latest.json", fair)
    write_markdown_digest(scorecard, changes, coverage, fair, now)

    print(
        "GIR scientific features OK",
        scorecard.get("grade"),
        scorecard.get("composite_score"),
        "flips", len(changes.get("source_status_flips") or []),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
