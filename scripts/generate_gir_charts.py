#!/usr/bin/env python3
"""Aerostratospheric Defense GIR — chart generator.
Reads latest open-tier JSON under data/ and writes PNG charts to docs/images/.
Usage: python3 scripts/generate_gir_charts.py
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
IMG = ROOT / "docs" / "images"
IMG.mkdir(parents=True, exist_ok=True)

CYAN, AMBER, GREEN, RED = "#00d4ff", "#f59e0b", "#34d399", "#f87171"
NAVY, BLUE, SLATE, WHITE = "#0a1628", "#0f2744", "#94a3b8", "#e2e8f0"


def load_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"skip {path.name}: {e}")
        return None


def style_axes(ax):
    ax.set_facecolor(BLUE)
    for spine in ax.spines.values():
        spine.set_color("#334155")
    ax.tick_params(colors=SLATE)
    ax.yaxis.label.set_color(WHITE)
    ax.xaxis.label.set_color(WHITE)
    ax.title.set_color(CYAN)


def main() -> int:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib required: pip install matplotlib", file=sys.stderr)
        return 1

    plt.rcParams.update({
        "figure.facecolor": NAVY, "axes.facecolor": BLUE, "axes.edgecolor": "#334155",
        "axes.labelcolor": WHITE, "text.color": WHITE, "xtick.color": SLATE, "ytick.color": SLATE,
        "axes.grid": True, "grid.color": "#1e293b", "grid.alpha": 0.85, "font.size": 10,
    })
    written = []

    manifest = load_json(DATA / "manifests" / "manifest_latest.json")
    if manifest and manifest.get("results"):
        labels = [r.get("source", "?").replace("_", "\n") for r in manifest["results"]]
        oks = [1 if r.get("ok") else 0 for r in manifest["results"]]
        fig, ax = plt.subplots(figsize=(9, max(3.5, 0.35 * len(labels) + 1.5)))
        style_axes(ax)
        ax.barh(labels, [1] * len(labels), color=[GREEN if o else RED for o in oks], edgecolor=NAVY)
        ax.set_xlim(0, 1.25)
        ax.set_xticks([])
        ax.set_title("Daily ingest source status (latest run)", color=CYAN, pad=12)
        for i, r in enumerate(manifest["results"]):
            ax.text(1.05, i, "OK" if r.get("ok") else "FAIL", va="center", fontsize=9,
                    color=GREEN if r.get("ok") else RED)
        fig.tight_layout()
        fig.savefig(IMG / "ingest_status.png", dpi=140, bbox_inches="tight", facecolor=NAVY)
        plt.close()
        written.append("ingest_status.png")

    uogw = load_json(DATA / "anomalies" / "uogw_anomalies_latest.json")
    if uogw:
        counts = uogw.get("counts") or {}
        keys = ["alert", "watch", "info"]
        vals = [int(counts.get(k, 0) or 0) for k in keys]
        fig, ax = plt.subplots(figsize=(6, 4))
        style_axes(ax)
        ax.bar(keys, vals, color=[RED, AMBER, CYAN], edgecolor=NAVY)
        ax.set_title("UOGW anomaly counts by severity", color=CYAN)
        ax.set_ylabel("Count")
        for i, v in enumerate(vals):
            ax.text(i, v + max(vals + [1]) * 0.03, str(v), ha="center", color=WHITE)
        fig.tight_layout()
        fig.savefig(IMG / "uogw_severity.png", dpi=140, bbox_inches="tight", facecolor=NAVY)
        plt.close()
        written.append("uogw_severity.png")

    quakes = load_json(DATA / "events" / "usgs_quakes_2.5_day_latest.geojson")
    if quakes:
        mags = []
        for f in quakes.get("features") or []:
            m = (f.get("properties") or {}).get("mag")
            if m is not None:
                try:
                    mags.append(float(m))
                except (TypeError, ValueError):
                    pass
        if mags:
            fig, ax = plt.subplots(figsize=(7, 4))
            style_axes(ax)
            ax.hist(mags, bins=min(12, max(5, len(set(mags)))), color=CYAN, edgecolor=NAVY, alpha=0.95)
            ax.set_title(f"USGS M2.5+ earthquakes (past day) — n={len(mags)}", color=CYAN)
            ax.set_xlabel("Magnitude")
            ax.set_ylabel("Count")
            fig.tight_layout()
            fig.savefig(IMG / "usgs_mags.png", dpi=140, bbox_inches="tight", facecolor=NAVY)
            plt.close()
            written.append("usgs_mags.png")

    air = load_json(DATA / "defense_open" / "public_military_airfields_ourairports.json")
    if air:
        feats = air.get("features") or []
        top = Counter((f.get("iso_country") or "?") for f in feats).most_common(15)
        if top:
            fig, ax = plt.subplots(figsize=(8, 5))
            style_axes(ax)
            ax.barh([t[0] for t in reversed(top)], [t[1] for t in reversed(top)], color=AMBER, edgecolor=NAVY)
            ax.set_title("Public keyword-flagged military-associated airfields by country", color=CYAN, fontsize=11)
            ax.set_xlabel("Count")
            fig.tight_layout()
            fig.savefig(IMG / "airfields_by_country.png", dpi=140, bbox_inches="tight", facecolor=NAVY)
            plt.close()
            written.append("airfields_by_country.png")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.set_facecolor(NAVY)
    fig.patch.set_facecolor(NAVY)
    ax.axis("off")
    ax.set_title("Aerostratospheric Defense GIR — open data flow", color=CYAN, fontsize=14, pad=16)
    from matplotlib.patches import FancyBboxPatch

    def box(x, y, w, h, text, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05,rounding_size=0.15",
                                    facecolor=BLUE, edgecolor=color, linewidth=2))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=8, color=WHITE)

    box(0.3, 3.2, 2.2, 1.2, "Public feeds\nUOGW · EONET · USGS\nNWS · DONKI · STAC", CYAN)
    box(3.0, 3.2, 2.2, 1.2, "Open defense\nCISA KEV\nOurAirports · awards", AMBER)
    box(5.7, 3.2, 2.0, 1.2, "Ingest scripts\n+ daily git\nautomation", GREEN)
    box(8.0, 3.2, 1.7, 1.2, "GIR git\nrepo\nmanifest", CYAN)
    box(1.5, 0.6, 3.0, 1.4, "Open tier\nPublic maps & research", GREEN)
    box(5.5, 0.6, 3.5, 1.4, "Partner / Restricted\nNot stored in public git", AMBER)
    fig.tight_layout()
    fig.savefig(IMG / "gir_data_flow.png", dpi=140, bbox_inches="tight", facecolor=NAVY)
    plt.close()
    written.append("gir_data_flow.png")

    s2 = load_json(DATA / "imagery_index" / "sentinel2_index_latest.json")
    if s2:
        items = s2.get("items") or []
        clouds = [i.get("cloud_cover") for i in items if i.get("cloud_cover") is not None]
        ids = [(i.get("id") or "")[-18:] for i in items if i.get("cloud_cover") is not None]
        if clouds:
            fig, ax = plt.subplots(figsize=(8, 4))
            style_axes(ax)
            ax.bar(range(len(clouds)), clouds, color=CYAN, edgecolor=NAVY)
            ax.set_xticks(range(len(ids)))
            ax.set_xticklabels(ids, rotation=45, ha="right", fontsize=7)
            ax.set_ylabel("Cloud cover %")
            ax.set_title("Sentinel-2 indexed scenes — cloud cover (sample region)", color=CYAN)
            fig.tight_layout()
            fig.savefig(IMG / "sentinel2_clouds.png", dpi=140, bbox_inches="tight", facecolor=NAVY)
            plt.close()
            written.append("sentinel2_clouds.png")

    usa = load_json(DATA / "defense_open" / "usaspending_defense_naics_latest.json")
    if usa and usa.get("results"):
        names, amounts = [], []
        for r in usa["results"][:12]:
            name = r.get("Recipient Name") or r.get("recipient_name") or r.get("Award ID") or "?"
            amt = r.get("Award Amount") or r.get("award_amount") or 0
            try:
                amt = float(amt)
            except (TypeError, ValueError):
                amt = 0.0
            names.append(str(name)[:28])
            amounts.append(amt)
        if any(amounts):
            fig, ax = plt.subplots(figsize=(9, 5))
            style_axes(ax)
            ax.barh(list(reversed(names)), list(reversed(amounts)), color=CYAN, edgecolor=NAVY)
            ax.set_title("USAspending sample — top awards (selected NAICS, public)", color=CYAN, fontsize=11)
            ax.set_xlabel("Award amount (USD)")
            fig.tight_layout()
            fig.savefig(IMG / "usaspending_top.png", dpi=140, bbox_inches="tight", facecolor=NAVY)
            plt.close()
            written.append("usaspending_top.png")

    print(f"Done. {len(written)} chart(s) in docs/images/")
    return 0 if written else 1


if __name__ == "__main__":
    raise SystemExit(main())
