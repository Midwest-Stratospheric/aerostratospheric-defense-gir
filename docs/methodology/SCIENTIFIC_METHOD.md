# GIR scientific methodology (open tier)

## Purpose

Document how the open Geospatial Information Repository acquires, validates, scores, and versions public geospatial and defense-adjacent data so results are **reproducible**, **auditable**, and **scientifically cautious**.

## Design principles

1. **Public sources only** in this repository (tier = open).
2. **Provenance first** — every retained payload can be tied to URL, time, license, and content hash.
3. **Uncertainty is stated** — open feeds have latency, gaps, and classification error; we measure freshness and validation, we do not claim ground truth.
4. **Separation of tiers** — partner/restricted products are out of band.
5. **Reproducibility** — git history + manifests + scripts allow re-running the pipeline.

## Pipeline

```text
Source APIs → Fetch → Hash + provenance → Parse → Schema checks → AOI filter
  → Baseline / fusion → Manifest + freshness SLA → STAC → Charts → Git commit
```

## Statistical baseline

Rolling window mean/σ and z-score flags (|z| ≥ 2) are **screening aids**, not calibrated detection probabilities.

## Fusion score

`corroboration_score = unique_sources / member_count` within distance/time thresholds.

## Non-goals

Not a sole life-safety source. Not a targeting system. Keyword military landmarks are heuristics only.

See also: [UNCERTAINTY.md](UNCERTAINTY.md)
