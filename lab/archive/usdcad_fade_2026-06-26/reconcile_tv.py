"""Reconcile the native TradingView UCAD-FADE export against the Python pre-filter NULL.

UCAD-FADE is a non-locked candidate (no Pine-header baseline), so this is a native
CONFIRMATION, not a locked-anchor reconcile. Honors the trade-csv-reconcile traps:
utf-8-sig BOM, Exit-rows-only P&L (entry+exit duplicate Net PnL here), pair-by-Trade#.
Sizing is %-risk compounded, so PF/WR and per-year SIGN are the sizing-invariant arbiters.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

CSV = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
    r"C:\Users\joshu\Downloads\UCAD-FADE_PEPPERSTONE_USDCAD_2026-06-26_66171.csv")
ACCT = 200_000.0


def metrics(net: np.ndarray) -> dict:
    n = len(net)
    if n == 0:
        return dict(n=0)
    wins = net[net > 0]
    losses = net[net <= 0]
    gw, gl = wins.sum(), -losses.sum()
    eq = ACCT + np.cumsum(net)
    peak = np.maximum.accumulate(eq)
    dd = peak - eq
    i = int(np.argmax(dd))
    return dict(n=n, net=float(net.sum()), wr=float((net > 0).mean()),
                pf=float(gw / gl) if gl > 0 else np.inf,
                avg_win=float(wins.mean()) if len(wins) else 0.0,
                avg_loss=float(losses.mean()) if len(losses) else 0.0,
                maxdd=float(dd.max()), maxdd_pct=float(dd[i] / peak[i] * 100),
                rf=float(net.sum() / dd.max()) if dd.max() > 0 else np.inf)


def line(tag, m):
    if m.get("n", 0) == 0:
        print(f"  {tag:>6}: n=0"); return
    print(f"  {tag:>6}: n={m['n']:>4}  net=${m['net']:+9.2f} ({m['net']/ACCT*100:+.2f}%)  "
          f"PF={m['pf']:.3f}  WR={m['wr']*100:4.1f}%  maxDD={m['maxdd_pct']:.2f}%  RF={m['rf']:+.2f}")


def main():
    df = pd.read_csv(CSV, encoding="utf-8-sig")
    df.columns = [c.strip() for c in df.columns]
    pnl_col = next(c for c in df.columns if c.startswith("Net PnL"))
    df["dt"] = pd.to_datetime(df["Date and time"])
    n_entry = int(df["Type"].str.startswith("Entry").sum())
    exits = df[df["Type"].str.startswith("Exit")].copy().sort_values("Trade number")
    print(f"file: {CSV.name}")
    print(f"P&L column: {pnl_col!r}  (USD-converted)")
    print(f"rows={len(df)}  entries={n_entry}  exits={len(exits)}  "
          f"(1:1 -> {n_entry == len(exits)})")
    print(f"span: {df['dt'].min()} -> {df['dt'].max()}\n")

    net = exits[pnl_col].to_numpy(float)
    print("=== FULL PANEL (native TV, %-risk compounded) ===")
    line("ALL", metrics(net))
    final_cum = float(df[df.columns[df.columns.str.startswith('Cumulative PnL USD')][0]].iloc[0]) \
        if any(df.columns.str.startswith('Cumulative PnL USD')) else None
    # cross-check vs TV's own cumulative column (last row in file order)
    cum_col = next(c for c in df.columns if c.startswith("Cumulative PnL"))
    print(f"  cross-check: sum(Exit Net)= ${net.sum():+.2f}  vs TV last Cumulative= "
          f"${float(df[cum_col].iloc[-1]):+.2f}")

    print("\n=== PER-YEAR (regime check — Python had 2021 NEGATIVE) ===")
    exits["year"] = exits["dt"].dt.year
    for y in sorted(exits["year"].unique()):
        line(str(y), metrics(exits[exits["year"] == y][pnl_col].to_numpy(float)))

    print("\n=== PYTHON PRE-FILTER (selected N48/k3.0/tp1.5, fixed-R, no halts, event-OFF) ===")
    print("  ALL : n= 652  exp=+0.0302R  PF=1.069  (SUB-COST: 4x hurdle 0.16R)")
    print("  2021: NEGATIVE (-0.0402R)   2023-25: positive (trend)   walk-fwd H2->H1 -0.039R")
    print("\nNOTE: native config differs (event-avoid ON, FXIFY %-risk + halts, TV chart")
    print("      back to 2020-03 incl COVID) -> trade-count parity not expected; the test")
    print("      is whether the QUALITATIVE verdict (flat/sub-cost, 2021 weak) agrees.")


if __name__ == "__main__":
    main()
