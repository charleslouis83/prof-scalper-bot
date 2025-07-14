#!/usr/bin/env bash
# Check service health endpoints and restart on failure.
set -euo pipefail

SERVICES=(service-a service-b)

for svc in "${SERVICES[@]}"; do
    if ! curl -fsS "http://localhost/${svc}/health" > /dev/null; then
        systemctl restart "$svc"
    fi
done
