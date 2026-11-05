"""FROZEN: production gate 5e's placebo before #1074, kept as this camp's reference statistic.

Verbatim copy of ``placebo_beaten_share`` from ``lab/builder/gates.py`` at main ``95679c7``
(git blob ``3f03697bf63dd549996ae70139eb903165428988``, file sha256
``4c781f14beb09dc64ba0d00ed5044c10b0920405d22f2cbff47a7da9fc9b3250``; engine sha256
``10f0eb19f302533ffc3ad56f8e06f76734d011ab4a851488e767b41bd4cfa363``). #1074 replaced production
5e with the same-day window slide, so this camp's "production" means this function. Only the
imports below are added; the function body is unchanged. Do not edit it.
"""
from __future__ import annotations

import numpy as np

from builder import compile as C
from builder.cards import Card
from builder.gates import Costs, net
from builder.instruments import INSTRUMENTS


def placebo_beaten_share(card: Card, days: list[C.Day], trades: list[C.Trade], costs: Costs,
                         runs: int, seed: int) -> float:
    """Share of timing-shuffled runs whose net profit is below the card's. Each run keeps every
    trade's day, side and holding length in bars, and redraws its entry bar uniformly from that
    day's live entry bars; entry at that bar's open, exit at the open `hold` bars later (capped
    at the flat bar), or the last close when the day has no flat bar."""
    if not trades:
        return 0.0
    by = {d.date: d for d in days}
    pv, c = INSTRUMENTS[card.instrument].point_value, costs.per_trade(card.instrument)
    rng = np.random.default_rng(seed)
    tot = np.zeros(runs)
    for t in trades:
        d = by[t.date]
        e = rng.integers(d.first, d.cutoff, size=runs)
        x = np.minimum(e + (t.exit_i - t.entry_i), d.flat)
        n = len(d.times)
        exit_px = np.where(x < n, d.o[np.minimum(x, n - 1)], d.c[n - 1])
        exit_px = np.where(x == e, d.c[e], exit_px)
        tot += t.side * (exit_px - d.o[e]) * pv - c
    real = net(card, trades, costs).sum()
    return float((tot < real).mean())
