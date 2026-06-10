#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="/home/ubuntu/.hermes/data/health/performance"
DATA_DIR="$BASE_DIR/data"
BACKUP_DIR="$BASE_DIR/backups"
TS="$(date -u +%Y%m%dT%H%M%SZ)"
DEST_DIR="$BACKUP_DIR/performance_data_backup_${TS}"

FILES=(
  "biometrics.csv"
  "sessions.csv"
  "fitness_metrics.csv"
  "match_details.csv"
  "supplements.csv"
)

mkdir -p "$DEST_DIR"

for file in "${FILES[@]}"; do
  src="$DATA_DIR/$file"
  if [[ ! -f "$src" ]]; then
    echo "ERROR: source file not found: $src" >&2
    exit 1
  fi
  cp "$src" "$DEST_DIR/$file"
done

printf '%s\n' "$DEST_DIR"
