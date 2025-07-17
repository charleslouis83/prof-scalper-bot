#!/usr/bin/env bash
# Build Docker images for all services.
set -euo pipefail

docker build -t prof-scalper/data_ingest ./data_ingest

docker build -t prof-scalper/model_server ./model_server

docker build -t prof-scalper/order_gateway ./order_gateway

docker build -t prof-scalper/feature_store ./feature_store

docker build -t prof-scalper/dashboard ./dashboard

docker build -t prof-scalper/risk_engine -f risk_engine/Dockerfile .

