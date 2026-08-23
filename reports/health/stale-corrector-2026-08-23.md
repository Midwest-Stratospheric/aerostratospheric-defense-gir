# Stale Pipeline Auto-Corrector Report

**Generated:** 2026-08-23T18:40:00Z (approx)

## Automations Checked

| Task ID | Name | isActive | Schedule Enabled | nextRun | Last Success | Status |
|---------|------|----------|------------------|---------|--------------|--------|
| 3bb0c193-64b5-4e45-b46e-fdf9fa15b028 | GIR Daily | true | true | 2026-08-24T13:00Z | 2026-08-23T13:04Z | OK |
| 3d9816d1-1cab-4ca0-a247-1df1a2af3edb | GIR Weekly | true | true | 2026-08-24T14:30Z | 2026-08-23T18:31Z | OK |
| aba4a490-e150-475f-b9d3-188c60887b5b | Daily Weather | true | true | 2026-08-24T12:15Z | 2026-08-23T12:19Z | OK |
| 7cf61858-5707-43d4-81b7-1ec60e0d991e | UOGW Weekly | true | true | 2026-08-24T16:00Z | None recorded | STALE → corrected |
| d90779e0-99a8-439a-ad72-5f08724ead41 | IGDR Daily | true | true | 2026-08-24T11:00Z | 2026-08-23T11:01Z | OK |
| 16777613-b91e-4d85-9771-afe84ca62b8d | MSDS Daily Ground Weather | true | true | 2026-08-24T11:00Z | 2026-08-23T11:00Z (title indicated issues) | OK |
| f8324df2-5839-4d95-8345-7f03b5cb9b0c | Weekly Pipeline Health Audit | true | true | 2026-08-30T15:00Z | 2026-08-23T15:11Z | OK |
| cea25ee8-2788-44fd-80c5-bd5acbcb16b1 | Stale Pipeline Auto-Corrector | true | true | 2026-08-24T17:00Z | (this run) | OK |

## Actions Taken

- **UOGW Weekly** (`7cf61858-5707-43d4-81b7-1ec60e0d991e`): No successful results found in history. Queued `automation_run_now`.
- No schedule updates needed (all nextRun values are in the future; none stuck in the past).
- Older duplicate/disabled automations (isEnabled=false, past nextRun) left untouched per policy.

## GitHub Freshness Notes

- `aerostratospheric-defense-gir` manifest_latest.json: generated 2026-08-23T07:48Z — fresh.
- `msds-data` ground-weather/daily: commits present for 2026-08-23 — fresh (despite tree listing lag).
- UOGW data/latest/ files present.

## Remaining Issues

- UOGW Weekly had empty results history; manual/queued run should populate. Monitor next scheduled run.
- MSDS Daily titles occasionally report "failed" / Open-Meteo limits; data still lands via other paths. Watch for recurring API quota issues.
- Several legacy disabled automations exist with past nextRun; no action required.

---
*Automated by Stale Pipeline Auto-Corrector*
