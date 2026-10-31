"""Synthetic inputs for the builder tests: 15m bar panels and raw BAR EXPORT v0.2 files."""
from __future__ import annotations

import hashlib

import numpy as np
import pandas as pd

# A two-sided MCL breakout card used across the gate and run tests.
CARD = """
id: g-001
family: orb
instrument: MCL
entry: {type: breakout, range: first_n_bars, side: both, order: stop}
exit: {stop: range_opposite, target: none, flat_at: "12:30"}
params: {n_bars: {value: 2, step: 1}}
"""
HEADER = "Trade number,Type,Date and time,Signal,Price USD,Size (qty)"


def panel(n_days: int, trend: float = 0.08, seed: int | None = None, start: str = "03:00",
          end: str = "13:00") -> tuple[pd.DataFrame, list[str]]:
    """Weekday 15m MCL bars start-end ET. Before 10:15 the price sits in a 69.90-70.20 box; from
    10:15 it moves `trend` per bar (up), so the breakout times the move; with `seed` it follows a
    seeded random walk from 09:30 instead. Prices stay on the 0.01 tick grid."""
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2023-01-02", periods=n_days)
    rows, idx = [], []
    for d in dates:
        px = 70.05
        for t in pd.date_range(f"{d.date()} {start}", f"{d.date()} {end}", freq="15min", tz="America/New_York"):
            hm = t.strftime("%H:%M")
            if hm < ("09:30" if seed is not None else "10:15"):
                o, h, l, c = (70.0, 70.2, 69.9, 70.05) if hm in ("09:00", "09:15") else (70.05, 70.1, 70.0, 70.05)
            else:
                step = trend if seed is None else float(rng.normal(0, 0.08))
                o, c = px, round(px + step, 2)
                h, l = round(max(o, c) + 0.02, 2), round(min(o, c) - 0.02, 2)
                px = c
            rows.append((o, h, l, c)); idx.append(t)
    b = pd.DataFrame(rows, columns=["open", "high", "low", "close"], index=pd.DatetimeIndex(idx))
    return b, [str(d.date()) for d in dates]


def signal(epoch: int, o, h, l, c, tf: str = "15", ticker: str = "MCL1!", close_ms: int | None = None,
           mintick: str = "0.01", pv: str = "100", tz: str = "America/New_York") -> str:
    tc = epoch + 900_000 if close_ms is None else close_ms
    return f"{epoch}|{o:.2f}|{h:.2f}|{l:.2f}|{c:.2f}|5|{tc}|2|M|{ticker}|futures|USD||{mintick}|{pv}|{tz}|{tf}"


def export_lines(bars: pd.DataFrame) -> list[str]:
    """One Entry row per bar (trade number = bar order), each followed by an Exit row, as TV writes."""
    out = [HEADER]
    for i, (t, r) in enumerate(bars.iterrows(), 1):
        e = int(t.tz_convert("UTC").value // 10**6)
        side = "long" if i % 2 else "short"
        out.append(f"{i},Entry {side},x,{signal(e, r.open, r.high, r.low, r.close)},{r.close:.2f},1")
        out.append(f"{i},Exit {side},x,{signal(e, r.open, r.high, r.low, r.close)},{r.close:.2f},1")
    return out


def write(tmp_path, lines: list[str], name: str = "BAR_EXPORT.csv"):
    p = tmp_path / name
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return p, hashlib.sha256(p.read_bytes()).hexdigest()

