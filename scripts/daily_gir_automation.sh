#!/bin/bash
# Aerostratospheric Defense GIR — comprehensive daily automation
# Fully self-contained: ingest → status → charts → exec summary → git commit
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

log "[1/4] Comprehensive open-tier ingest..."
if python3 scripts/ingest_open_tier.py >>"$LOG" 2>&1; then
  log "Ingest finished OK."
else
  log "Ingest finished with errors (see log). Continuing."
fi

log "[2/4] US open-status banner + charts + executive summary..."
python3 scripts/compute_us_open_status.py >>"$LOG" 2>&1 || log "compute_us_open_status warned"
python3 scripts/generate_gir_charts.py >>"$LOG" 2>&1 || log "generate_gir_charts warned"
python3 scripts/generate_daily_exec_summary.py >>"$LOG" 2>&1 || log "generate_daily_exec_summary warned"

log "[3/4] Git snapshot..."
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
      commit -m "chore(gir): daily open-tier data + exec summary ${STAMP}

Sources: UOGW, EONET, USGS, NWS, Sentinel-2, DONKI, CISA KEV, OurAirports, USAspending, GDELT, OpenSky, OSM military, FIRMS optional.
Includes: US open-status, Mermaid charts, reports/daily/YYYY-MM-DD-gir-exec.md
Open tier only — no classified content."
  log "Committed: $(git log -1 --oneline)"
else
  log "No changes to commit."
fi

log "[4/4] Cleanup old logs..."
find "$LOG_DIR" -name 'daily_*.log' -mtime +45 -delete 2>/dev/null || true
log "=== Done $STAMP ==="
