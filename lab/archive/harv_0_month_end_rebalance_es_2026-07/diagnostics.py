"""Non-gating diagnostics for HARV-2026-001 (brief §3 Phase 3, §4, §7).

Reads the frozen monthly_panel.parquet produced by run_harv0.py and reports:
  - pooled vs ex-quarter-end vs quarter-end-only signed effect (roll-contamination
    read; brief §4 "ex-quarter-end reported as a diagnostic, not a rescue/selection axis")
  - per-era (2010-2017 / 2018-2026) signed effect (regime read)
  - next-month reversal (T-1->T+3) on qualifying months
  - unconditional TOM window mean

These are REPORTS. They do not alter the §6 verdict (pooled panel gates).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from run_harv0 import effect_on  # noqa: E402

DATA = HERE / "data"


def _sub_effect(panel: pd.DataFrame, mask: pd.Series, label: str) -> dict:
    sub = panel.loc[mask].copy()
    if not len(sub) or not sub["qualifying"].any():
        return {"label": label, "n_months": int(len(sub)), "n_qual": 0}
    r = effect_on(sub, "window", "signed_window", label)
    return {
        "label": label,
        "n_months": int(len(sub)),
        "n_qual": r.n_qual,
        "mean_bp": round(r.mean_signed * 1e4, 3),
        "ci95_bp": [round(r.ci95_lo * 1e4, 3), round(r.ci95_hi * 1e4, 3)],
        "perm_p": r.perm_p,
        "trade_rate": round(r.trade_rate, 4),
    }


def main() -> None:
    panel_path = DATA / "monthly_panel.parquet"
    if not panel_path.exists():
        raise SystemExit(f"missing {panel_path} — run run_harv0.py first")
    panel = pd.read_parquet(panel_path)

    out: dict = {}
    out["pooled"] = _sub_effect(panel, pd.Series(True, index=panel.index), "pooled")
    out["ex_quarter_end"] = _sub_effect(panel, ~panel["quarter_end"], "ex_quarter_end")
    out["quarter_end_only"] = _sub_effect(panel, panel["quarter_end"], "quarter_end_only")

    # Era split (regime read; not a gate).
    era1 = panel["year"] <= 2017
    out["era_2010_2017"] = _sub_effect(panel, era1, "era_2010_2017")
    out["era_2018_2026"] = _sub_effect(panel, ~era1, "era_2018_2026")

    # Micro era (2019-05->), same subset the OOS gate uses on parent for continuity.
    out["micro_era_parent"] = _sub_effect(panel, panel["micro_era"], "micro_era_parent")

    # Next-month reversal on qualifying months (signal-aligned): fade should reverse.
    q = panel.loc[panel["qualifying"]].copy()
    if "reversal_T1_to_next_T3" in q.columns:
        rev = (q["signal"] * q["reversal_T1_to_next_T3"]).to_numpy(dtype=float)
        rev = rev[np.isfinite(rev)]
        out["reversal_signed_next_T3"] = {
            "n": int(len(rev)),
            "mean_bp": round(float(np.mean(rev)) * 1e4, 3) if len(rev) else None,
        }

    out["unconditional_TOM_window_mean_bp"] = round(float(panel["window"].mean()) * 1e4, 3)

    # Roll-contamination read: among quarter-end qualifying months, what share have
    # |R_spread| within one ES-roll-phantom (~135bp) of the 100bp threshold?
    qe_q = panel.loc[panel["quarter_end"] & panel["qualifying"]].copy()
    if len(qe_q):
        near = (qe_q["R_spread_bp"].abs() < 235).sum()  # 100bp thr + ~135bp phantom
        out["quarter_end_roll_note"] = {
            "n_qe_qualifying": int(len(qe_q)),
            "n_abs_rspread_lt_235bp": int(near),
            "note": "months whose qualification could flip if a ~135bp ES-roll phantom "
                    "were removed; diagnostic only, operationalization frozen",
        }

    (HERE / "diagnostics.json").write_text(json.dumps(out, indent=2, default=str))
    print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
