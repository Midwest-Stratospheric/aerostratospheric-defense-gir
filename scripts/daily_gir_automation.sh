#!/bin/bash
# Aerostratospheric Defense GIR — comprehensive daily automation
# ingest → status → charts → exec summary → scientific features → git commit
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

log "[1/5] Comprehensive open-tier ingest..."
if python3 scripts/ingest_open_tier.py >>"$LOG" 2>&1; then
  log "Ingest finished OK."
else
  log "Ingest finished with errors (see log). Continuing."
fi

log "[2/5] US open-status + charts + executive summary..."
python3 scripts/compute_us_open_status.py >>"$LOG" 2>&1 || log "compute_us_open_status warned"
python3 scripts/generate_gir_charts.py >>"$LOG" 2>&1 || log "generate_gir_charts warned"
python3 scripts/generate_daily_exec_summary.py >>"$LOG" 2>&1 || log "generate_daily_exec_summary warned"

log "[3/5] Scientific features (scorecard, change detection, coverage, FAIR)..."
python3 scripts/generate_scientific_features.py >>"$LOG" 2>&1 || log "generate_scientific_features warned"

log "[4/5] Git snapshot..."
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
      commit -m "chore(gir): daily open-tier data + scientific features ${STAMP}

Includes: ingest, US open-status, charts, exec summary, quality scorecard, change detection, coverage report, FAIR package card.
Open tier only — no classified content."
  log "Committed: $(git log -1 --oneline)"
else
  log "No changes to commit."
fi

log "[5/5] Cleanup old logs..."
find "$LOG_DIR" -name 'daily_*.log' -mtime +45 -delete 2>/dev/null || true
log "=== Done $STAMP ==="
