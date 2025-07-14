#!/usr/bin/env python3
"""Aggregate features to be run periodically from cron or systemd."""

from __future__ import annotations

import time
from pathlib import Path
import pandas as pd


TICKS_PATH = Path("ticks.csv")
FEATURES_PATH = Path("features.csv")


def aggregate() -> None:
    if not TICKS_PATH.exists():
        return
    df = pd.read_csv(TICKS_PATH)
    features = {
        "timestamp": int(time.time()),
        "price_mean": df["price"].mean(),
        "volume": len(df),
    }
    header = not FEATURES_PATH.exists()
    pd.DataFrame([features]).to_csv(FEATURES_PATH, mode="a", index=False, header=header)


if __name__ == "__main__":
    aggregate()
