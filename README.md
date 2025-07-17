# Prof Scalper Bot

This repository contains the source code for **Prof Scalper Bot**, a cryptocurrency trading bot. The bot can run locally via Docker Compose or in Kubernetes using Helm.

[Architecture Diagram](https://example.com/architecture.png)

## Prerequisites

- Docker and Docker Compose
- [k3s](https://k3s.io/) or another Kubernetes distribution
- [Helm](https://helm.sh/) package manager

## Setup

Clone the repository and create a `.env` file using `.env.example` as a template:

```bash
cp .env.example .env
```

Fill in the API keys and any other secrets.

### Directory Layout

The repository assumes the following service directories exist at the project
root. Each directory contains a `Dockerfile` and the code for its service,
which are built and started in step 3 below:

```bash
data_ingest/
order_gateway/
model_server/
dashboard/
feature_store/
risk_engine/
```

If these directories are missing, create them before continuing:

```bash
mkdir -p data_ingest order_gateway model_server dashboard feature_store risk_engine
```

## Local Development

Run the stack locally with Docker Compose:

```bash
docker-compose up
```

Once started, access the bot at [http://localhost:3000](http://localhost:3000).

### Testnet vs. Production

By default the bot connects to the exchange in testnet mode. Set `EXCHANGE_ENV` in your `.env` file:

```bash
EXCHANGE_ENV=testnet   # for sandbox trading
EXCHANGE_ENV=live      # for real trades
```

## Deployment

Deploy to your Kubernetes cluster using Helm:

```bash
helm install scalper ./helm
# or upgrade
helm upgrade scalper ./helm
```

## Troubleshooting

- **Containers fail to start** – ensure Docker is running and ports are free.
- **Helm errors about missing resources** – verify k3s is running and you have access to the correct cluster context.
- **Connection issues to the exchange** – check that your API key and secret are correct and that `EXCHANGE_ENV` is set properly.

## Scripts

Utility scripts for running research, simulation and deployment tasks.

- `scripts/research.py` - query TimescaleDB and run walk-forward analysis
- `scripts/backtest.py` - backtest strategy on historical ticks
- `scripts/simulate.py` - stub order gateway and record PnL
- `scripts/aggregate_features.py` - aggregate features from ticks
- `scripts/train_daily.sh` - daily training wrapper with log rotation
- `scripts/heartbeat.sh` - check service health and restart on failure
- `scripts/deploy.sh` - upgrade Kubernetes deployment via Helm

## Dashboard

This repository also contains the Next.js dashboard for Prof Scalper Bot.

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

## About

This monorepo contains services and tools for building an automated scalping bot. It includes data ingestion, feature storage, model training, serving infrastructure, order execution, monitoring and dashboards. The project provides a modular framework for automated scalping across different markets.
