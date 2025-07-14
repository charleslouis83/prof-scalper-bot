codex/implement-scripts-with-required-functionality
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
=======
codex/create-docker-compose-and-helm-chart
# prof-scalper-bot
=======
codex/create-next.js-dashboard-app
# prof-scalper-bot

This repository contains the Next.js dashboard for Prof Scalper Bot.

To start the app:

```bash
cd dashboard
npm install
npm run dev
```

Run the tests:

```bash
cd dashboard
npm test
```
=======
# Prof Scalper Bot

This monorepo contains services and tools for building an automated scalping bot.
It includes data ingestion, feature storage, model training, serving
infrastructure, order execution, monitoring and dashboards.

This project aims to provide a modular framework for automated scalping across different markets.

Dev


