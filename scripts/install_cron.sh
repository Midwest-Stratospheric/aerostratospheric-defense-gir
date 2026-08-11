#!/usr/bin/env bash
# Install daily cron job (06:00 UTC) for GIR automation
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPT="$ROOT/scripts/daily_gir_automation.sh"
if ! command -v crontab >/dev/null 2>&1; then
  echo "crontab not available on this host."
  echo "Add this line to your system scheduler instead:"
  echo "0 6 * * * $SCRIPT >> $ROOT/logs/cron.out 2>&1"
  exit 1
fi
TMP=$(mktemp)
crontab -l 2>/dev/null | grep -v 'daily_gir_automation.sh' > "$TMP" || true
echo "0 6 * * * $SCRIPT >> $ROOT/logs/cron.out 2>&1" >> "$TMP"
crontab "$TMP"
rm -f "$TMP"
echo "Installed: daily at 06:00 (system local time unless cron is UTC)"
crontab -l | grep daily_gir
