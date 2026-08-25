# Stale Pipeline Auto-Corrector Report

**Generated:** 2026-08-25 ~17:10 UTC

## Automations Checked

| Automation | taskId | Status | Last Success | nextRun (before) | Action |
|------------|--------|--------|--------------|------------------|--------|
| GIR Daily Data Quality & Exec Summary | 3bb0c193-... | OK (recent success) / schedule was stuck | 2026-08-25 13:03 UTC | 2026-08-24 13:00 | Schedule refreshed → 2026-08-26 13:00 |
| GIR Weekly Status Digest | 3d9816d1-... | OK (weekly) / schedule stuck | 2026-08-24 14:31 UTC | 2026-08-24 14:30 | Schedule refreshed → 2026-08-31 14:30 |
| Daily Weather Data Quality & Exec Summary | aba4a490-... | OK (recent success) / schedule stuck | 2026-08-25 12:20 UTC | 2026-08-24 12:15 | Schedule refreshed → 2026-08-26 12:15 |
| UOGW Weekly Report Digest | 7cf61858-... | OK (weekly) / schedule stuck | 2026-08-24 16:05 UTC | 2026-08-24 16:00 | Schedule refreshed → 2026-08-31 16:00 |
| IGDR Daily Snapshot | d90779e0-... | OK (recent success) / schedule stuck | 2026-08-25 11:07 UTC | 2026-08-24 11:00 | Schedule refreshed → 2026-08-26 11:00 |
| MSDS Daily Ground Weather | 16777613-... | OK (recent success; Open-Meteo limit noted) / schedule stuck | 2026-08-25 11:11 UTC | 2026-08-24 11:00 | Schedule refreshed → 2026-08-26 11:00 |
| Weekly Pipeline Health Audit | f8324df2-... | OK | 2026-08-23 15:11 UTC | 2026-08-30 15:00 (future) | None |
| Stale Pipeline Auto-Corrector (self) | cea25ee8-... | Running now / schedule was stuck | prior 2026-08-24 | 2026-08-24 17:00 | Schedule refreshed → 2026-08-26 17:00 |

## Actions Taken

- **Schedule refresh (automation_update)** on 6 core enabled automations whose `nextRun` was still pointing at 2026-08-24 (stuck past). All nextRun values advanced to the correct future occurrence.
- **No `automation_run_now`** issued: every core daily task already produced a successful result on 2026-08-25; weeklies had success within the last 24–48 h. Conservative policy applied.
- Disabled legacy duplicates (older msds/igdr variants) left untouched.

## GitHub Freshness (spot-check)

- `Midwest-Stratospheric/aerostratospheric-defense-gir` → `data/manifests/manifest_latest.json` generated_at **2026-08-25T08:10:51Z** (15/15 OK; FIRMS still `awaiting_key`). Fresh.
- `Midwest-Stratospheric/msds-data` → `ground-weather/daily/` contains **2026-08-25.json**. Fresh.

## Remaining Issues

- MSDS Daily Ground Weather continues to hit Open-Meteo rate limits on some runs (title reflects this). Data file for today still present; monitor.
- FIRMS source remains `awaiting_key` in the GIR manifest (known long-standing gap).
- Several older, disabled duplicate automations (msds-daily-ground-weather, igdr-daily-snapshot variants) still appear in the list; harmless while `isEnabled=false`.

## Status Summary

**All core pipelines healthy; stuck schedules corrected; no run_now required.**
