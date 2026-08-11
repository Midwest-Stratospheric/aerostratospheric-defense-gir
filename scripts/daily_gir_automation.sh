#!/bin/bash
# Aerostratospheric Defense GIR — comprehensive daily automation
# 1) Multi-source open-tier ingest
# 2) Git commit when data changed
# Cron: 0 6 * * * /path/to/gir/scripts/daily_gir_automation.sh

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$ROOT/logs"
mkdir -p "$LOG_DIR"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
LOG="$LOG_DIR/daily_$STAMP.log"

log() { echo "$@" | tee -a "$LOG"; }

log "=== GIR daily automation $STAMP ==="
log "ROOT=$ROOT"
cd "$ROOT"

log "[1/2] Comprehensive open-tier ingest..."
if python3 scripts/ingest_open_tier.py >>"$LOG" 2>&1; then
  log "Ingest finished OK."
else
  log "Ingest finished with errors (see log)."
fi

log "[2/2] Git snapshot..."
if [ ! -d .git ]; then
  log "ERROR: not a git repository: $ROOT"
  exit 1
fi

if [ ! -f .gitignore ]; then
  printf 'logs/\n*.pyc\n__pycache__/\n.DS_Store\n*.tmp\n.env\n' > .gitignore
fi

git add -A

if git status --porcelain | grep -q .; then
  git -c user.email="gir-automation@aerostratospheric.local" \
      -c user.name="GIR Daily Automation" \
      commit -m "chore(gir): daily open-tier data refresh ${STAMP}

Sources: UOGW anomalies, EONET, USGS quakes, NWS alerts, Sentinel-2 STAC, DONKI CME.
Open tier only — no classified content."
  log "Committed: $(git log -1 --oneline)"
else
  log "No changes to commit."
fi

find "$LOG_DIR" -name 'daily_*.log' -mtime +45 -delete 2>/dev/null || true
log "=== Done $STAMP ==="
