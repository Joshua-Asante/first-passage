#!/usr/bin/env python3
"""Q-JOINT-TAIL-WEEKLY §9 authoring-time panel-shape sanity check.

Per docs/briefs/2026-05-27-q-joint-tail-weekly-pre-q.md §9. Does NOT run the
verdict (that is the CC handoff's job / forbidden move #1). Only checks the
panel-shape assumption that gates whether the CC handoff is worth authoring:
  - n_active = 4 dominant overall (>50% of week-blocks)?
  - n_active = 4 in the bottom-decile of portfolio-week PnL (>=15 of ~23)?

Aggregation matches MC exactly: Monday-anchored non-overlapping 5-business-day
blocks (core.mc build_week_blocks convention), over the union business-day index.
Uses raw $ PnL (sign is scale-invariant per brief §4 Simplify).

Data: the four canonical 2026-05-24 Pepperstone panels (core.mc PEPPERSTONE_PANELS),
gitignored vendor CSVs. Skips cleanly if they are not present locally.

Executed 2026-07-14 -> §9 FAIL -> Q-JOINT-TAIL-WEEKLY RETIRED (see
docs/briefs/closures/Q-JOINT-TAIL-WEEKLY-closure-retired.md).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

# Resolve core/ relative to this file (repo-root/lab/analysis/<slug>/sanity_check.py)
CORE = Path(__file__).resolve().parents[3] / "core"
sys.path.insert(0, str(CORE))

from portfolio_mc import PEPPERSTONE_PANELS, load_trades  # noqa: E402

STRATS = ["guardian", "striker", "aegis", "striker_nas100"]


def main() -> int:
    missing = [s for s in STRATS if not PEPPERSTONE_PANELS[s].exists()]
    if missing:
        print(f"SKIP: canonical panel CSV(s) absent for {missing} "
              f"(gitignored vendor data; run where the 2026-05-24 panels are present).")
        return 0

    daily_pnl, daily_cnt = {}, {}
    for s in STRATS:
        tb = load_trades(PEPPERSTONE_PANELS[s], strategy=s)  # exit_date + pnl per exit
        g = tb.groupby("exit_date")["pnl"]
        daily_pnl[s] = g.sum()
        daily_cnt[s] = g.size()

    allmin = min(v.index.min() for v in daily_pnl.values())
    allmax = max(v.index.max() for v in daily_pnl.values())
    bdays = pd.bdate_range(allmin, allmax)

    pnl_panel = pd.DataFrame({s: daily_pnl[s].reindex(bdays).fillna(0.0) for s in STRATS})
    cnt_panel = pd.DataFrame({s: daily_cnt[s].reindex(bdays).fillna(0) for s in STRATS})

    rows = []
    idx = pnl_panel.index
    for i, day in enumerate(idx):
        if day.weekday() == 0 and i + 5 <= len(idx):  # Mon-anchored, non-overlapping 5-bday
            wk_pnl = pnl_panel.iloc[i:i + 5].sum()
            wk_active = cnt_panel.iloc[i:i + 5].sum() > 0
            rows.append({
                "week_start": day.date(),
                "port_pnl": float(wk_pnl.sum()),
                "n_active": int(wk_active.sum()),
                "n_negative": int((wk_pnl < 0).sum()),
            })
    wk = pd.DataFrame(rows)
    N = len(wk)

    print("=" * 68)
    print(f"panel business-day span : {allmin.date()} -> {allmax.date()}  ({len(bdays)} bdays)")
    print(f"total Mon-anchored 5-day week-blocks : {N}   (brief expected ~227)")
    print("=" * 68)

    print("\n[2] n_active distribution over ALL week-blocks:")
    for k, c in wk["n_active"].value_counts().sort_index().items():
        print(f"    n_active={k} : {c:>4}  ({c / N:>6.1%})")
    share4 = float((wk["n_active"] == 4).mean())
    print(f"    -> n_active=4 share overall = {share4:.1%}   (gate >50%? {'YES' if share4 > 0.50 else 'NO'})")

    n_dec = max(1, round(N * 0.10))
    bottom = wk.nsmallest(n_dec, "port_pnl")
    print(f"\n[3] bottom decile of portfolio-week PnL : N={n_dec}   (brief expected ~23)")
    print(f"    worst week = {bottom['port_pnl'].min():,.0f}   decile cutoff = {bottom['port_pnl'].max():,.0f}")

    print("\n[4] n_active distribution WITHIN bottom decile:")
    for k, c in bottom["n_active"].value_counts().sort_index().items():
        print(f"    n_active={k} : {c:>4}  ({c / n_dec:>6.1%})")
    n4_bottom = int((bottom["n_active"] == 4).sum())
    print(f"    -> n_active=4 in bottom decile = {n4_bottom} of {n_dec}   (gate >=15? {'YES' if n4_bottom >= 15 else 'NO'})")

    print("\n[preview, NOT the verdict] mean n_negative in bottom decile = "
          f"{bottom['n_negative'].mean():.2f}  (H1 wants >=3.0; H0 wants <=2.0)")

    gate = (share4 > 0.50) and (n4_bottom >= 15)
    print("\n" + "=" * 68)
    print(f"§9 DISPOSITION: {'PASS -> author CC handoff' if gate else 'FAIL -> RETIRE (mirror Q-JOINT-TAIL-1)'}")
    print("=" * 68)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
