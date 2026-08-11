"""Feature 4 — Area-of-interest spatial helpers."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Iterable

def load_regions(config_path: Path) -> list[dict]:
    return json.loads(config_path.read_text(encoding="utf-8")).get("regions") or []

def point_in_bbox(lon: float, lat: float, bbox: list[float]) -> bool:
    west, south, east, north = bbox
    if west <= east:
        return west <= lon <= east and south <= lat <= north
    return (lon >= west or lon <= east) and south <= lat <= north

def filter_features_by_bbox(features: Iterable[dict], bbox: list[float]) -> list[dict]:
    out = []
    for f in features:
        geom = f.get("geometry") or {}
        coords = geom.get("coordinates")
        if not coords:
            continue
        if geom.get("type") == "Point" and len(coords) >= 2:
            if point_in_bbox(float(coords[0]), float(coords[1]), bbox):
                out.append(f)
            continue
        try:
            flat = coords
            while isinstance(flat[0], (list, tuple)):
                flat = flat[0]
            if point_in_bbox(float(flat[0]), float(flat[1]), bbox):
                out.append(f)
        except Exception:
            continue
    return out
