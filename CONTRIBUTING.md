# Contributing to Aerostratospheric Defense GIR

Thank you for interest in improving this open-tier Geospatial Information Repository.

## Scope

This repository is **open-tier public data only**. We do **not** accept classified, FOUO, export-controlled, or partner-restricted content. If you have higher-tier material, discuss private channels via [contact](https://midwestsds.com/contact/).

## Ways to contribute

1. **Bug reports / data issues** — Open an issue describing the source, expected vs actual behavior, and a timestamp.
2. **New open sources** — Propose public APIs or feeds that fit the defense-adjacent / hazard / EO index mission. Prefer free, redistributable, no-key or documented-key sources.
3. **Scripts & docs** — PRs for ingest improvements, validation, charts, or documentation are welcome.
4. **Citation & attribution** — Help keep upstream credits accurate.

## Development workflow

```bash
git clone https://github.com/Midwest-Stratospheric/aerostratospheric-defense-gir.git
cd aerostratospheric-defense-gir
python3 scripts/ingest_open_tier.py          # optional local run
python3 scripts/compute_us_open_status.py
python3 scripts/generate_gir_charts.py
python3 scripts/generate_daily_exec_summary.py
bash scripts/daily_gir_automation.sh         # full pipeline
```

- Use Python 3.10+ (stdlib preferred; see `requirements.txt`).
- Keep commits focused; message style: `feat:`, `fix:`, `docs:`, `chore(gir):`.
- Do not commit secrets, `.env`, or API keys. Use GitHub Actions secrets for optional keys (e.g. `FIRMS_MAP_KEY`).

## Pull requests

- Describe *what* and *why*.
- Note any new external dependency or license implication.
- Confirm no classified or non-redistributable data is introduced.

## Code of conduct

Be respectful. This is a small research project focused on transparent open data. Harassment or bad-faith contributions will be rejected.

## License

By contributing you agree your contributions are under the same MIT license as the repository (see `LICENSE`), unless otherwise stated.
