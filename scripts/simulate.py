#!/usr/bin/env python3
"""Simulated order gateway and PnL tracking."""

from __future__ import annotations

import random
import pandas as pd


class SimulatedGateway:
    def __init__(self) -> None:
        self.position = 0
        self.cash = 0.0

    def send_order(self, price: float, qty: int) -> None:
        """Immediately fill order and update position."""
        self.position += qty
        self.cash -= price * qty


def run_simulation(prices: list[float]) -> pd.DataFrame:
    gateway = SimulatedGateway()
    history = []
    for price in prices:
        action = random.choice([-1, 0, 1])
        if action:
            gateway.send_order(price, action)
        pnl = gateway.cash + gateway.position * price
        history.append({"price": price, "pnl": pnl})
    return pd.DataFrame(history)


if __name__ == "__main__":
    prices = [100 + random.random() for _ in range(100)]
    df = run_simulation(prices)
    df.to_csv("simulate_pnl.csv", index=False)
