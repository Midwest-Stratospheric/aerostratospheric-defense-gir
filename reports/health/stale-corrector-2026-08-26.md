# Stale Pipeline Auto-Corrector Report

**Generated:** 2026-08-26T17:00:00Z (approx)

## Automations Checked

| Task | Status | Notes |
|------|--------|-------|
| GIR Daily (3bb0c193-...) | STALE → corrected | nextRun past; today's run failed (USAGE_POOL_EXHAUSTED); last success 2026-08-25 ~13:03Z. run_now queued + schedule refreshed → nextRun 2026-08-27T13:00Z |
| GIR Weekly (3d9816d1-...) | OK | nextRun 2026-08-31; last success 2026-08-24 |
| Daily Weather (aba4a490-...) | OK (schedule refreshed) | Ran successfully today 12:21Z; nextRun was past → refreshed to 2026-08-27T12:15Z |
| UOGW Weekly (7cf61858-...) | OK | nextRun 2026-08-31; last success 2026-08-24 |
| IGDR Daily (d90779e0-...) | OK (schedule refreshed) | Success today 11:13Z; snapshot present; nextRun refreshed to 2026-08-27T11:00Z |
| MSDS Daily Ground Weather (16777613-...) | OK (schedule refreshed) | Success status today; data file present & complete; nextRun refreshed to 2026-08-27T11:00Z |
| Weekly Pipeline Health Audit (f8324df2-...) | OK | nextRun 2026-08-30; last success 2026-08-23 |

## GitHub Freshness

- `manifest_latest.json`: generated 2026-08-26T08:10Z (fresh, 15/15 OK)
- `msds-data/ground-weather/daily/2026-08-26.json`: present and complete
- IGDR `snapshots/2026-08-26/`: present

## Actions Taken

1. `automation_run_now` on GIR Daily
2. `automation_update` (schedule refresh) on GIR Daily, Daily Weather, IGDR Daily, MSDS Daily Ground Weather to advance nextRun past the stuck past timestamps

## Remaining Issues

- GIR Daily may still hit usage quota on the queued run; monitor results.
- Several older/disabled duplicate msds/igdr automations exist (isEnabled=false) — left untouched per conservative policy.

---
*Automated by Stale Pipeline Auto-Corrector*
