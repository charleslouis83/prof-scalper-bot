#!/usr/bin/env python3
"""Run walk-forward analysis on data from TimescaleDB."""

from __future__ import annotations

import os
import pandas as pd
from sqlalchemy import create_engine

TIMESCALE_URI = os.getenv("TIMESCALE_URI", "postgresql://user:pass@localhost:5432/scalper")


def fetch_data() -> pd.DataFrame:
    """Fetch tick data ordered by timestamp."""
    engine = create_engine(TIMESCALE_URI)
    query = "SELECT ts, price FROM ticks ORDER BY ts"
    return pd.read_sql(query, engine)


def walkforward(df: pd.DataFrame, window: int = 100) -> pd.DataFrame:
    """Simple walk-forward analysis returning cumulative returns."""
    metrics = []
    for start in range(0, len(df) - window, window):
        train = df.iloc[start : start + window]
        test = df.iloc[start + window : start + 2 * window]
        if test.empty:
            break
        ret = test["price"].pct_change().sum()
        metrics.append({"start": train["ts"].iloc[0], "return": ret})
    return pd.DataFrame(metrics)


def main() -> None:
    df = fetch_data()
    metrics = walkforward(df)
    metrics.to_csv("research_metrics.csv", index=False)


if __name__ == "__main__":
    main()
