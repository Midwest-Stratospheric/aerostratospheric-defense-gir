#!/usr/bin/env python3
"""GIR git-native chart markup (Mermaid). Writes docs/GRAPHS.md from open-tier JSON. No PNGs."""
from __future__ import annotations
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "docs" / "GRAPHS.md"

def load_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"skip {path.name}: {e}")
        return None

def esc(s: str) -> str:
    return str(s).replace('"', "'").replace("\n", " ")[:40]

def main() -> int:
    lines = []
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines += ["# GIR graphs (git markup)", "", f"_Generated {now} from open-tier data. Mermaid only — no image binaries._", "",
              "Regenerate:", "", "```bash", "python3 scripts/generate_gir_charts.py", "```", ""]
    lines += ["## Data flow", "", "```mermaid", "flowchart LR",
              '  A["Public feeds"] --> B["Ingest scripts"]',
              '  C["Open defense sources"] --> B',
              '  B --> D["data folders"]', '  D --> E["manifest"]', '  E --> F["git commit"]',
              '  D --> G["Defense GIR page / maps"]', "```", ""]
    lines += ["## Access tiers", "", "```mermaid", "flowchart TB",
              '  O["Open tier — this public repo"]', '  P["Partner tier — agreements"]',
              '  R["Restricted — authorized only"]', "  O --> P --> R", "```", ""]
    manifest = load_json(DATA / "manifests" / "manifest_latest.json")
    lines += ["## Daily ingest status", ""]
    if manifest and manifest.get("results"):
        ok = sum(1 for r in manifest["results"] if r.get("ok"))
        total = len(manifest["results"])
        fail = max(total - ok, 0)
        lines += [f"**Last run:** `{manifest.get('generated_at_utc', '—')}` · **{ok}/{total} sources OK**", "",
                  "```mermaid", "pie showData", f'  title Ingest sources OK vs failed ({ok}/{total})',
                  f'  "OK" : {ok}', f'  "Failed or skipped" : {fail}', "```", "",
                  "| Source | Status |", "|--------|--------|"]
        for r in manifest["results"]:
            st = "OK" if r.get("ok") else "FAIL"
            lines.append(f"| `{r.get('source', '?')}` | {st} |")
        lines.append("")
    else:
        lines += ["_No manifest yet — run ingest first._", ""]
    uogw = load_json(DATA / "anomalies" / "uogw_anomalies_latest.json")
    lines += ["## UOGW anomaly severity", "", "Public anomaly flags (research-style). Not official emergency alerts.", ""]
    if uogw:
        counts = uogw.get("counts") or {}
        a, w, i = int(counts.get("alert", 0) or 0), int(counts.get("watch", 0) or 0), int(counts.get("info", 0) or 0)
        lines += ["```mermaid", "pie showData", "  title UOGW counts by severity",
                  f'  "alert" : {a}', f'  "watch" : {w}', f'  "info" : {i}', "```", "",
                  f"| alert | watch | info |", f"|-------|-------|------|", f"| {a} | {w} | {i} |", ""]
    quakes = load_json(DATA / "events" / "usgs_quakes_2.5_day_latest.geojson")
    lines += ["## USGS earthquakes (M2.5+, past day)", ""]
    if quakes:
        mags = []
        for f in quakes.get("features") or []:
            m = (f.get("properties") or {}).get("mag")
            if m is not None:
                try: mags.append(float(m))
                except (TypeError, ValueError): pass
        lines.append(f"**Events:** {len(mags)}")
        lines.append("")
        if mags:
            buckets = {"2.5-3.4": 0, "3.5-4.4": 0, "4.5-5.4": 0, "5.5+": 0}
            for m in mags:
                if m < 3.5: buckets["2.5-3.4"] += 1
                elif m < 4.5: buckets["3.5-4.4"] += 1
                elif m < 5.5: buckets["4.5-5.4"] += 1
                else: buckets["5.5+"] += 1
            labels, vals = list(buckets.keys()), list(buckets.values())
            lines += ["```mermaid", "xychart-beta", '  title "Quake count by magnitude band"',
                      "  x-axis " + json.dumps(labels), '  y-axis "Count" 0 --> ' + str(max(max(vals), 1)),
                      "  bar " + json.dumps(vals), "```", ""]
    air = load_json(DATA / "defense_open" / "public_military_airfields_ourairports.json")
    lines += ["## Public keyword-flagged airfields by country", "",
              "> Heuristic from public OurAirports — **not** an official basing list.", ""]
    if air:
        feats = air.get("features") or []
        top = Counter((f.get("iso_country") or "?") for f in feats).most_common(12)
        lines += [f"**Records:** {len(feats)}", ""]
        if top:
            labels, vals = [t[0] for t in top], [t[1] for t in top]
            lines += ["```mermaid", "xychart-beta", '  title "Top countries (keyword heuristic)"',
                      "  x-axis " + json.dumps(labels), '  y-axis "Count" 0 --> ' + str(max(max(vals), 1)),
                      "  bar " + json.dumps(vals), "```", ""]
    lines += ["---", "", "Open tier only. See OPEN_DEFENSE_DATA.md and DATA_POLICY.md.", ""]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
