#!/bin/bash
# Aerostratospheric Defense GIR — daily automation
# Ingest open feeds + git commit when data changes.
# Cron example (06:00 daily):
#   0 6 * * * /path/to/gir/scripts/daily_gir_automation.sh

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

log "[1/3] Open-tier ingest..."
python3 scripts/ingest_open_tier.py >>"$LOG" 2>&1
log "Ingest finished."

log "[2/3] STAC Sentinel-2 index (Casey IL region)..."
if python3 scripts/stac_search_sentinel2.py --bbox -88.2 39.1 -87.7 39.5 --limit 8 >>"$LOG" 2>&1; then
  log "STAC index updated."
else
  log "STAC search skipped/failed (non-fatal)."
fi

log "[3/3] Git snapshot..."
if [ ! -d .git ]; then
  log "ERROR: not a git repository: $ROOT"
  exit 1
fi

if [ ! -f .gitignore ]; then
  printf 'logs/\n*.pyc\n__pycache__/\n.DS_Store\n*.tmp\n' > .gitignore
fi

git add -A

if git status --porcelain | grep -q .; then
  git -c user.email="gir-automation@aerostratospheric.local" \
      -c user.name="GIR Daily Automation" \
      commit -m "chore(gir): daily open-tier ingest ${STAMP}

Automated UOGW anomaly + EONET event refresh and imagery index update.
Open tier only — no classified content."
  log "Committed: $(git log -1 --oneline)"
else
  log "No changes to commit."
fi

find "$LOG_DIR" -name 'daily_*.log' -mtime +30 -delete 2>/dev/null || true

log "=== Done $STAMP ==="
