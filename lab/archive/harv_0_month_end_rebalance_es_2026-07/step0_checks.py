"""Step-0 panel integrity checks for HARV-0 (before any metric)."""
from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd


@dataclass
class Step0Report:
    n_months: int
    expected_months_lo: int = 180
    expected_months_hi: int = 200
    duplicate_months: list[str] = field(default_factory=list)
    nan_census: dict[str, int] = field(default_factory=dict)
    quarter_end_count: int = 0
    ok: bool = True
    notes: list[str] = field(default_factory=list)


def run_step0(panel: pd.DataFrame) -> Step0Report:
    rep = Step0Report(n_months=len(panel))
    if not (rep.expected_months_lo <= rep.n_months <= rep.expected_months_hi):
        rep.ok = False
        rep.notes.append(
            f"month count {rep.n_months} outside [{rep.expected_months_lo},{rep.expected_months_hi}]"
        )
    dups = panel["month_id"][panel["month_id"].duplicated()].tolist()
    rep.duplicate_months = dups
    if dups:
        rep.ok = False
        rep.notes.append(f"duplicate months: {dups}")
    for col in ("R_spread", "window", "C", "G", "placebo"):
        if col in panel.columns:
            rep.nan_census[col] = int(panel[col].isna().sum())
    if "quarter_end" in panel.columns:
        rep.quarter_end_count = int(panel["quarter_end"].sum())
    # Trading-day count sanity: most months 19–23 CME sessions
    if "n_trading_days" in panel.columns:
        bad = panel.loc[
            (panel["n_trading_days"] < 15) | (panel["n_trading_days"] > 25), "month_id"
        ].tolist()
        if bad:
            rep.notes.append(f"unusual n_trading_days months: {bad[:10]}")
    return rep
