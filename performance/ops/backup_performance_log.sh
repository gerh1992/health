#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="/home/ubuntu/.hermes/data/health/performance"
SRC="$BASE_DIR/data/performance_log.csv"
BACKUP_DIR="$BASE_DIR/backups"
TS="$(date -u +%Y%m%dT%H%M%SZ)"

mkdir -p "$BACKUP_DIR"

if [[ ! -f "$SRC" ]]; then
  echo "ERROR: source file not found: $SRC" >&2
  exit 1
fi

cp "$SRC" "$BACKUP_DIR/performance_log.backup_${TS}.csv"
echo "$BACKUP_DIR/performance_log.backup_${TS}.csv"
