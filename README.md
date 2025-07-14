# Prof Scalper Bot

This repository contains the source code for **Prof Scalper Bot**, a cryptocurrency trading bot. The bot is designed to run either locally via Docker Compose or in Kubernetes using Helm.

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

