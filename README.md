# prof-scalper-bot

Utility scripts for running research, simulation and deployment tasks.

## Scripts
- `scripts/research.py` - query TimescaleDB and run walk-forward analysis
- `scripts/backtest.py` - backtest strategy on historical ticks
- `scripts/simulate.py` - stub order gateway and record PnL
- `scripts/aggregate_features.py` - aggregate features from ticks
- `scripts/train_daily.sh` - daily training wrapper with log rotation
- `scripts/heartbeat.sh` - check service health and restart on failure
- `scripts/deploy.sh` - upgrade Kubernetes deployment via Helm
