"""Feature 2 — Schema validation & completeness scoring."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any

def validate_manifest_v2(manifest: dict[str, Any]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    for key in ("generated_at_utc", "tier", "policy", "results"):
        if key not in manifest:
            errors.append(f"missing required key: {key}")
    if manifest.get("tier") not in (None, "open"):
        errors.append("tier must be 'open' for public GIR")
    results = manifest.get("results")
    if not isinstance(results, list):
        errors.append("results must be a list")
    else:
        for i, r in enumerate(results):
            if not isinstance(r, dict) or "source" not in r or "ok" not in r:
                errors.append(f"results[{i}] invalid")
    return len(errors) == 0, errors

def completeness_score(manifest: dict[str, Any]) -> float:
    results = manifest.get("results") or []
    if not results:
        return 0.0
    return round(sum(1 for r in results if r.get("ok")) / len(results), 4)

def validate_geojson_minimal(doc: dict[str, Any]) -> tuple[bool, list[str]]:
    errors = []
    if doc.get("type") not in ("FeatureCollection", "Feature"):
        errors.append("GeoJSON type must be Feature or FeatureCollection")
    if doc.get("type") == "FeatureCollection" and not isinstance(doc.get("features"), list):
        errors.append("FeatureCollection.features must be a list")
    return len(errors) == 0, errors
