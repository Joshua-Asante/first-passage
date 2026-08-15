"""Static-equity recompute for TradingView trade-list exports.

Lifts ``static_equity_recompute`` from the Q-TXG-1 striker x MNQ score cell into a
shared util with required ``point_value_usd`` / ``commission_per_side`` (no
silent instrument hardcode). Pairs Exit/Entry by ``Trade #``; net =

    qty * (exit_price - entry_price) * point_value_usd
    - 2 * commission_per_side * qty

When TV ``Net P&L USD`` diverges from that static recompute beyond tolerance,
the export is flagged ``compounded_divergent`` (TV percent-of-equity path).
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

# Score-cell provenance defaults for MNQ fixtures only — callers must still pass
# these explicitly; they are not applied as module-level fallthroughs.
MNQ_POINT_VALUE_USD = 2.00
MNQ_COMMISSION_PER_SIDE = 0.91

_DEFAULT_ABS_DELTA_TOLERANCE = 1.0

_REQUIRED_COLUMNS = frozenset(
    {"Trade #", "Type", "Price USD", "Size (qty)", "Net P&L USD"}
)

# Current TV schema aliases -> pre-migration names (same map as reconcile skill).
_COLUMN_ALIASES = {
    "Trade number": "Trade #",
    "Net PnL USD": "Net P&L USD",
}


def load_tv_trade_list(source: pd.DataFrame | Path | str) -> pd.DataFrame:
    """Load a TV trade-list DataFrame or CSV path; normalize column aliases."""
    if isinstance(source, pd.DataFrame):
        df = source.copy()
    else:
        df = pd.read_csv(Path(source), encoding="utf-8-sig")
    rename = {src: dst for src, dst in _COLUMN_ALIASES.items() if src in df.columns}
    if rename:
        df = df.rename(columns=rename)
    missing = _REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"TV trade list missing columns {sorted(missing)}")
    return df


def static_equity_recompute(
    source: pd.DataFrame | Path | str,
    *,
    point_value_usd: float,
    commission_per_side: float,
    abs_delta_tolerance: float = _DEFAULT_ABS_DELTA_TOLERANCE,
) -> dict[str, Any]:
    """Recompute per-leg static USD nets and compare to TV Net P&L.

    Parameters
    ----------
    source
        TV trade-list DataFrame or path to a CSV export.
    point_value_usd
        Contract dollar value per point (required; e.g. MNQ = 2.00).
    commission_per_side
        Commission per contract per side (required; e.g. MNQ = 0.91).
    abs_delta_tolerance
        Per-leg |recompute - TV| threshold for ``ok_within_1usd`` /
        ``compounded_divergent`` (default 1.0 USD, matching score_cell).

    Returns
    -------
    dict
        Summary keys compatible with score_cell
        (``n_legs``, ``tv_net_sum``, ``recompute_net_sum``, ``max_abs_delta``,
        ``mean_abs_delta``, ``ok_within_1usd``) plus ``compounded_divergent``
        and ``legs`` (per-trade static-equity series DataFrame).
    """
    if point_value_usd is None or commission_per_side is None:
        raise TypeError("point_value_usd and commission_per_side are required")

    df = load_tv_trade_list(source)
    exits = df[df["Type"].astype(str).str.startswith("Exit")].copy()
    entries = df[df["Type"].astype(str).str.startswith("Entry")].copy()
    entry_by_trade = entries.set_index("Trade #")

    rows: list[dict[str, Any]] = []
    deltas: list[float] = []
    tv_sum = 0.0
    recom_sum = 0.0
    static_equity = 0.0

    # Preserve exit-row order (TV export order) for the equity series.
    for _, ex in exits.iterrows():
        tid = ex["Trade #"]
        if tid not in entry_by_trade.index:
            continue
        en = entry_by_trade.loc[tid]
        if isinstance(en, pd.DataFrame):
            en = en.iloc[0]
        qty = float(ex["Size (qty)"])
        entry_px = float(en["Price USD"])
        exit_px = float(ex["Price USD"])
        gross = qty * (exit_px - entry_px) * float(point_value_usd)
        net_recompute = gross - (2.0 * float(commission_per_side) * qty)
        tv_net = float(ex["Net P&L USD"])
        abs_delta = abs(net_recompute - tv_net)
        static_equity += net_recompute
        deltas.append(abs_delta)
        tv_sum += tv_net
        recom_sum += net_recompute
        rows.append(
            {
                "Trade #": tid,
                "entry_price": entry_px,
                "exit_price": exit_px,
                "qty": qty,
                "tv_net": tv_net,
                "recompute_net": net_recompute,
                "abs_delta": abs_delta,
                "static_equity": static_equity,
            }
        )

    ok_within = bool(all(d < abs_delta_tolerance for d in deltas))
    legs = pd.DataFrame(rows)
    return {
        "n_legs": len(deltas),
        "tv_net_sum": tv_sum,
        "recompute_net_sum": recom_sum,
        "max_abs_delta": max(deltas) if deltas else 0.0,
        "mean_abs_delta": float(np.mean(deltas)) if deltas else 0.0,
        "ok_within_1usd": ok_within,
        "compounded_divergent": not ok_within,
        "legs": legs,
    }
