#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="/home/ubuntu/.hermes/data/health/performance"
echo "INFO: backup_performance_log.sh is a legacy command alias; it now delegates to the multi-CSV backup and returns the backup directory path." >&2
exec "$BASE_DIR/ops/backup_performance_data.sh" "$@"
