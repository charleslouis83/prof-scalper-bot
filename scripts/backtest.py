#!/usr/bin/env python3
"""Replay strategy using simulate.py on historical ticks."""

from __future__ import annotations

import pandas as pd
from pathlib import Path
from simulate import run_simulation


def load_ticks(path: str = "ticks.csv") -> list[float]:
    if not Path(path).exists():
        return []
    df = pd.read_csv(path)
    return df.get("price", pd.Series()).tolist()


def main() -> None:
    ticks = load_ticks()
    results = run_simulation(ticks)
    results.to_html("report.html", index=False)


if __name__ == "__main__":
    main()
