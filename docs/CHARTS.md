# GIR graphs — git markup only

Graphs live as **Mermaid + Markdown tables** in [`docs/GRAPHS.md`](GRAPHS.md).

No PNG/JPG chart binaries are stored in this repository (avoids failed image renders and large binary commits).

## Regenerate from open data

```bash
python3 scripts/generate_gir_charts.py
```

That script reads `data/**` and rewrites `docs/GRAPHS.md`.

## Daily automation

`scripts/daily_gir_automation.sh` runs the generator after ingest so graph markup stays in sync with open-tier feeds.

## View

GitHub renders Mermaid in Markdown automatically when you open `docs/GRAPHS.md`.
