#!/usr/bin/env bash
# Upgrade Kubernetes deployment via Helm.
set -euo pipefail

CHART="helm/prof-scalper"
NAMESPACE="${1:-scalper}"

helm upgrade --install scalper "$CHART" -n "$NAMESPACE"
