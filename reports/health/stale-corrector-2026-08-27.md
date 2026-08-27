# Stale Pipeline Auto-Corrector Report

**Generated:** 2026-08-27 17:10 UTC (approx)

## Automations Checked

| Task | Status | Notes |
|------|--------|-------|
| GIR Daily (3bb0c193...) | STALE → corrected | nextRun was past; today's scheduled run failed (usage quota); last success 2026-08-26. Schedule refreshed to 2026-08-28T13:00Z. run_now queued. |
| GIR Weekly (3d9816d1...) | OK | nextRun 2026-08-31; last success 2026-08-24 |
| Daily Weather (aba4a490...) | STALE schedule → corrected | Ran successfully today; nextRun was stuck past. Schedule refreshed to 2026-08-28T12:15Z. |
| UOGW Weekly (7cf61858...) | OK | nextRun 2026-08-31; last success 2026-08-24 |
| IGDR Daily (d90779e0...) | STALE schedule → corrected | Ran successfully today; nextRun stuck. Schedule refreshed to 2026-08-28T11:00Z. |
| MSDS Daily Ground Weather (16777613...) | STALE → corrected | nextRun stuck; today's run hit Open-Meteo limit (no 2026-08-27.json). Schedule refreshed; run_now queued. |
| Weekly Pipeline Health Audit (f8324df2...) | OK | nextRun 2026-08-30; last success 2026-08-23 |
| Stale Pipeline Auto-Corrector (self) | Schedule refreshed | nextRun was past; advanced to 2026-08-28T17:00Z. |

## Actions Taken

- **Schedule refresh (automation_update)** on: GIR Daily, Daily Weather, IGDR Daily, MSDS Daily, Stale Corrector (forced nextRun recalculation).
- **run_now** queued for: GIR Daily, MSDS Daily Ground Weather.

## GitHub Freshness Notes

- `manifest_latest.json`: generated 2026-08-26T08:10Z (~33h old). FIRMS still awaiting_key.
- `msds-data/ground-weather/daily/`: latest file 2026-08-26.json; no 2026-08-27 yet (Open-Meteo rate limit).

## Remaining Issues

- Usage quota exhaustion on GIR Daily scheduled runs (may affect run_now).
- Open-Meteo daily limit impacting MSDS ground weather file creation.
- Several older duplicate/disabled ground-weather and IGDR automations remain (not touched; isEnabled=false).

---
*Automated by Stale Pipeline Auto-Corrector. Conservative corrections only.*
