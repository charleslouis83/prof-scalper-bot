#!/usr/bin/env bash
# Run training and stacking daily, rotating logs.
set -euo pipefail

LOG_DIR="models/logs"
mkdir -p "$LOG_DIR"

python3 models/train.py "$@" >"$LOG_DIR/train_$(date +%F).log" 2>&1
python3 models/stacker.py "$@" >"$LOG_DIR/stacker_$(date +%F).log" 2>&1

# remove logs older than 7 days
find "$LOG_DIR" -type f -mtime +7 -delete
