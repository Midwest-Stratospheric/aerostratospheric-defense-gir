"""Feature 7 — STAC Collection/Item export for imagery index."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

def stac_collection(collection_id: str = "gir-sentinel2-open-index", title: str = "Aerostratospheric GIR open Sentinel-2 index") -> dict[str, Any]:
    return {
        "type": "Collection", "stac_version": "1.0.0", "id": collection_id, "title": title,
        "description": "Open-tier catalog of Sentinel-2 scene search results retained by the Aerostratospheric Defense GIR.",
        "license": "various — upstream Copernicus open data terms apply",
        "extent": {"spatial": {"bbox": [[-180, -90, 180, 90]]}, "temporal": {"interval": [[None, None]]}},
        "links": [],
        "providers": [{"name": "Aerostratospheric / Midwest Stratospheric Data Systems", "roles": ["processor", "host"], "url": "https://midwestsds.com/"}],
    }

def stac_item_from_index_row(row: dict[str, Any], collection_id: str) -> dict[str, Any]:
    item_id = row.get("id") or row.get("scene_id") or "unknown"
    return {
        "type": "Feature", "stac_version": "1.0.0", "id": item_id, "collection": collection_id,
        "geometry": row.get("geometry"), "bbox": row.get("bbox"),
        "properties": {
            "datetime": row.get("datetime") or row.get("acquired"),
            "eo:cloud_cover": row.get("cloud_cover"),
            "gir:tier": "open",
            "gir:indexed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        },
        "assets": row.get("assets") or {}, "links": row.get("links") or [],
    }
