"""Reduce the operator-supplied TradingView List-of-Trades export for
orb_mnq_recon_v3.pine (core/strategies/candidates/, MANIFEST.sha256
be800cb4...) into the daily_pnl / daily_mae schema this repo's own
combined_sim.py-family scripts consume.

Source CSV is NOT committed (vendor-sourced, same posture as
core/data/tv_exports/ and the aegis_orbmnq_combined_book_2026-08-26 precedent)
-- only the derived data/*.json panels land in-repo.

Reduction convention (matches lab/analysis/c1/aegis_orbmnq_combined_book_2026-08-26/
followup_intraday_mae_proxy.py::load_day_mae, extended to the daily PnL side):
  - qty is constant at 2 for every row in this export (base entry qty=2,
    scale-in qty=2 since scaleInQtyPct defaults to 100) -- verified below,
    hard-fails if that ever stops holding, since the /qty normalization
    assumes one constant divisor for the whole panel.
  - Group by EXIT date (a scale-in add gets its own trade-number row sharing
    the day's exit, per the 2026-08-25 session's own finding -- see
    MEMORY.md project_orb_mnq_recon_tuning_session_2026_08_25.md); sum Net
    PnL USD across every exit row that day, divide by qty=2. This is $ per
    1x of the base-config contract unit, so build_combined_path's
    leg_contracts={"orbmnq": k} scaling reproduces what running the SAME
    construct at qty=k (base entry AND every scale-in, since they share one
    qty in this config) would have realized -- exact, not approximate,
    because every entry that day shares one qty.
  - daily_mae: the single worst (most negative) per-contract Adverse
    Excursion USD among that day's exit rows, divided by qty=2 -- a
    disclosed trade-level MAE proxy, NOT a true bar-level intraday
    reconstruction (see followup_intraday_mae_proxy.py's own docstring for
    why: no intraday timestamps to sequence same-day scale-ins' own worst
    moments). Consumed via simulate_path's intraday_low.

Step-0 panel-integrity battery already run clean on this export
(lab/research_utils/step0_battery.py, --tz UTC workaround -- see this
directory's RESULTS.md for why: Joshua's TradingView chart displays ET, not
UTC, contrary to the script's own hardcoded "TV standard" comment).
"""
from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict

SRC = sys.argv[1] if len(sys.argv) > 1 else \
    r"C:\Users\joshu\Downloads\ORB-MNQ-1_recon_v3_CME_MINI_MNQ1!_2026-08-31_70648.csv"
OUT_PNL = "data/daily_pnl.json"
OUT_MAE = "data/daily_mae.json"


def main() -> None:
    rows = list(csv.DictReader(open(SRC, encoding="utf-8-sig")))
    exits = [r for r in rows if r["Type"].startswith("Exit")]

    qtys = {float(r["Size (qty)"]) for r in rows}
    if qtys != {2.0}:
        raise ValueError(f"expected constant qty=2 throughout; found {sorted(qtys)}")
    qty = 2.0

    pnl_by_day: dict[str, float] = defaultdict(float)
    mae_by_day: dict[str, float] = {}
    for r in exits:
        date = r["Date and time"].split(" ")[0]
        pnl_by_day[date] += float(r["Net PnL USD"])
        mae = float(r["Adverse excursion USD"])
        if mae > 0.0:
            raise ValueError(f"positive adverse-excursion value on {date}: {mae}")
        mae_by_day[date] = min(mae_by_day.get(date, 0.0), mae)

    pnl_records = [
        {"date": d, "pnl_per_contract": round(v / qty, 6)}
        for d, v in sorted(pnl_by_day.items())
    ]
    mae_records = [
        {"date": d, "mae_per_contract": round(v / qty, 6)}
        for d, v in sorted(mae_by_day.items())
    ]

    with open(OUT_PNL, "w") as fh:
        json.dump(pnl_records, fh, indent=2)
    with open(OUT_MAE, "w") as fh:
        json.dump(mae_records, fh, indent=2)

    total_net = sum(v for v in pnl_by_day.values())
    print(f"trade-days: {len(pnl_by_day)}  total exit rows: {len(exits)}  "
          f"sum(NetPnL)={total_net * qty:.2f}  (qty-normalized total={total_net:.2f})")
    print(f"wrote {OUT_PNL} ({len(pnl_records)} days), {OUT_MAE} ({len(mae_records)} days)")


if __name__ == "__main__":
    main()
