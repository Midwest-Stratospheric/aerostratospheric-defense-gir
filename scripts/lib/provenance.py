"""Feature 1 — Provenance & content integrity."""
from __future__ import annotations
import hashlib, json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def make_provenance(*, record_id: str, source_id: str, source_url: str, content: bytes, license: str, attribution: str = "", tier: str = "open", published_at_utc: str | None = None, bbox: list[float] | None = None, transform: dict[str, Any] | None = None) -> dict[str, Any]:
    rec = {
        "record_id": record_id, "source_id": source_id, "source_url": source_url,
        "fetched_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "published_at_utc": published_at_utc, "license": license, "attribution": attribution,
        "content_sha256": sha256_bytes(content), "byte_length": len(content), "tier": tier,
        "transform": transform or {"parser": "raw", "schema_version": "v1"},
    }
    if bbox and len(bbox) == 4:
        rec["spatial"] = {"bbox": bbox, "crs": "EPSG:4326"}
    return rec

def write_sidecar(data_path: Path, provenance: dict[str, Any]) -> Path:
    side = data_path.with_suffix(data_path.suffix + ".prov.json")
    side.write_text(json.dumps(provenance, indent=2), encoding="utf-8")
    return side
