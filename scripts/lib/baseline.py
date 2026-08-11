"""Feature 5 — Statistical anomaly baselines (rolling z-score style)."""
from __future__ import annotations
import json, math
from pathlib import Path
from typing import Any

def mean_std(values: list[float]) -> tuple[float, float]:
    n = len(values)
    if n == 0:
        return 0.0, 0.0
    mu = sum(values) / n
    if n == 1:
        return mu, 0.0
    var = sum((x - mu) ** 2 for x in values) / (n - 1)
    return mu, math.sqrt(var)

def z_score(x: float, mu: float, sigma: float) -> float | None:
    if sigma <= 1e-12:
        return None
    return (x - mu) / sigma

def update_baseline_store(store_path: Path, series_id: str, value: float, window: int = 30) -> dict[str, Any]:
    store: dict[str, Any] = {}
    if store_path.exists():
        try:
            store = json.loads(store_path.read_text(encoding="utf-8"))
        except Exception:
            store = {}
    series = store.setdefault(series_id, {"values": [], "window": window})
    values: list[float] = list(series.get("values") or [])
    values.append(float(value))
    values = values[-window:]
    series["values"] = values
    mu, sigma = mean_std(values)
    series["mu"], series["sigma"], series["n"] = mu, sigma, len(values)
    z = z_score(value, mu, sigma)
    series["last_z"] = z
    store[series_id] = series
    store_path.parent.mkdir(parents=True, exist_ok=True)
    store_path.write_text(json.dumps(store, indent=2), encoding="utf-8")
    return {"series_id": series_id, "value": value, "mu": mu, "sigma": sigma, "z": z, "n": len(values), "flag": abs(z) >= 2.0 if z is not None else False}
