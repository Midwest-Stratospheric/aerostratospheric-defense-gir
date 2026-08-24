# Stale Pipeline Auto-Corrector Report

**Generated:** 2026-08-24T17:15:00Z (approx)

## Automations Checked

| Task | Name | isActive | Schedule Enabled | nextRun (UTC) | Last Success | Status |
|------|------|----------|------------------|---------------|--------------|--------|
| 3bb0c193-... | GIR Daily | true | true | 2026-08-24T13:00 | 2026-08-24T13:17 | OK |
| 3d9816d1-... | GIR Weekly | true | true | 2026-08-24T14:30 | 2026-08-24T14:31 | OK |
| aba4a490-... | Daily Weather | true | true | 2026-08-24T12:15 | 2026-08-24T12:20 | OK |
| 7cf61858-... | UOGW Weekly | true | true | 2026-08-24T16:00 | 2026-08-24T16:05 | OK |
| d90779e0-... | IGDR Daily | true | true | 2026-08-24T11:00 | 2026-08-24T11:03 | OK |
| 16777613-... | MSDS Daily Ground Weather | true | true | 2026-08-24T11:00 | 2026-08-24T11:10 | OK (API limit noted) |
| f8324df2-... | Weekly Pipeline Health Audit | true | true | 2026-08-30T15:00 | 2026-08-23T15:11 | OK |

## Actions Taken

- None required. All core enabled automations have successful results within the last ~6 hours (or last week for weekly).
- nextRun values for today's daily/weekly slots have passed but corresponding runs completed successfully; schedules appear healthy.

## GitHub Freshness (spot check)

- `data/manifests/manifest_latest.json`: generated_at 2026-08-24T08:28 UTC — fresh (15/15 ok; FIRMS awaiting_key).
- `msds-data/ground-weather/daily/`: 2026-08-24.json present (smaller than prior days; prior days continuous through 08-23).

## Remaining Issues

- MSDS Daily reports Open-Meteo rate limit on recent runs (still marked SUCCESS).
- Several legacy/disabled duplicate automations exist with old nextRun and isEnabled=false (ignored per policy).
- FIRMS source in GIR manifest still awaiting API key.

## Summary

No stale enabled automations detected; no run_now or schedule updates performed.
