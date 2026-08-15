"""D5-RECOST-1 — Stage-2 cost-law re-derivation of the Baltussen H1 construct on
the native-MNQ OOS window (2019-05-06 -> 2026-07-16).

Pre-reg: docs/briefs/pre-registration/D5-RECOST-1-verdict-preregistration.md
Frozen decisions (before this ran):
  D1  reuse parent D5 K_eff=1 (no fresh K).
  D2  window = full OOS 2019-05-06:2026-07-16, edge AND hurdle measured jointly.

Construct is the UNCHANGED parent ``baltussen.py::session_edges`` (@ e1c51f0).
Data is the already-cached ``MNQ.v.0`` continuous OOS panel (zero pull).
Reports the Bulenox_100K hurdle (primary, continuity with the closed IS verdict)
AND the MFFU_Rapid_100K hurdle (mandatory sensitivity, pre-reg §2).

Usage (research venv)::

    PYTHONPATH=lab;core python lab/analysis/d5_recost_2026-07/run_recost.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[2]
_D5 = _ROOT / "lab" / "analysis" / "d5_nq_intraday_mom_2026-07"
for _p in (_ROOT / "lab", _ROOT / "core", _D5):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from discovery.cost_mnq import (  # noqa: E402
    COST_LAW_MULTIPLE,
    hurdle_from_price,
)

from baltussen import session_edges  # noqa: E402  (frozen parent construct)
from series import cached_mnq_continuous_1m  # noqa: E402  (already-cached OOS panel)

OUT_DIR = _HERE
PREREG = "docs/briefs/pre-registration/D5-RECOST-1-verdict-preregistration.md"
WINDOW = "2019-05-06:2026-07-16"  # frozen full-OOS (D2); no sub-window search
PRIMARY_FIRM = "Bulenox_100K"     # gate basis (continuity with the closed IS verdict)
SENSITIVITY_FIRM = "MFFU_Rapid_100K"  # mandatory co-report (pre-reg §2)
DEGRADED_DAYS = ["2020-02-27", "2020-02-28", "2020-06-30"]  # defect-log, NOT dropped


def main() -> int:
    print("[1/3] load cached MNQ.v.0 continuous OOS panel (2019-05-06:2026-07-16) ...")
    raw = cached_mnq_continuous_1m()
    print(f"      rows={len(raw):,}")

    print("[2/3] Baltussen H1 session edges (frozen construct, single-symbol - no stitch) ...")
    edges = session_edges(raw)
    n = len(edges)
    print(f"      sessions={n:,}")
    if n == 0:
        print("ABORT: zero complete RTH sessions - check clock anchors.")
        return 2

    mean_edge = float(edges["edge"].mean())
    sd = float(edges["edge"].std(ddof=1))
    hit = float((edges["edge"] > 0).mean())
    sharpe_gross = (mean_edge / sd) * np.sqrt(252.0) if sd > 0 else float("nan")
    corr = float(edges["r_rod"].corr(edges["r_last"]))
    median_px = float(edges["px_1530"].median())

    # Stage-2 gate: Bulenox primary; MFFU sensitivity.
    h_primary = hurdle_from_price(median_px, firm_key=PRIMARY_FIRM)
    h_sens = hurdle_from_price(median_px, firm_key=SENSITIVITY_FIRM)
    passed = mean_edge >= h_primary.hurdle_4x_frac  # gate on primary basis (pre-reg §6)

    n_degraded = int(edges.index.isin([np.datetime64(d) for d in DEGRADED_DAYS]).sum())

    report = {
        "campaign_id": "d5_recost_1",
        "prereg": PREREG,
        "stage": "2 (cost-law re-derivation)",
        "construct": "Baltussen-2021-JFE-H1 (baltussen.py @ e1c51f0, UNCHANGED)",
        "window": WINDOW,
        "n_sessions": n,
        "date_first": str(edges.index.min().date()),
        "date_last": str(edges.index.max().date()),
        "degraded_days_present": n_degraded,  # defect-log, not dropped (D2)
        "oos_edge": {
            "mean_edge_bp": mean_edge * 1e4,
            "std_edge": sd,
            "hit_rate": hit,
            "sharpe_gross_ann": sharpe_gross,
            "corr_rod_last": corr,
        },
        "median_px_1530": median_px,
        "cost_law": {
            "multiple": COST_LAW_MULTIPLE,
            "primary_firm": PRIMARY_FIRM,
            "primary_hurdle_4x_bp": h_primary.hurdle_4x_frac * 1e4,
            "primary_edge_over_hurdle": mean_edge / h_primary.hurdle_4x_frac,
            "sensitivity_firm": SENSITIVITY_FIRM,
            "sensitivity_hurdle_4x_bp": h_sens.hurdle_4x_frac * 1e4,
            "sensitivity_edge_over_hurdle": mean_edge / h_sens.hurdle_4x_frac,
        },
        # Parent IS verdict, for side-by-side (unchanged, from stage2_4_report.json).
        "parent_is": {
            "mean_edge_bp": 1.4612647044076368,
            "hurdle_4x_bp": 11.062663510651548,
            "median_px_1530": 4013.5,
        },
        "verdict": "PASS" if passed else "KILL",
    }

    edges.to_csv(OUT_DIR / "recost_oos_edges.csv")
    (OUT_DIR / "recost_report.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )

    print("[3/3] Stage-2 cost-law (OOS, jointly measured)")
    print(f"      OOS mean_edge = {mean_edge * 1e4:.4f} bp   (IS was 1.4613 bp)")
    print(f"      median px_1530 = {median_px:.1f}   (IS was 4013.5)")
    print(
        f"      {PRIMARY_FIRM}: hurdle_4x = {h_primary.hurdle_4x_frac * 1e4:.4f} bp   "
        f"edge/hurdle = {mean_edge / h_primary.hurdle_4x_frac:.3f}"
    )
    print(
        f"      {SENSITIVITY_FIRM}: hurdle_4x = {h_sens.hurdle_4x_frac * 1e4:.4f} bp   "
        f"edge/hurdle = {mean_edge / h_sens.hurdle_4x_frac:.3f}"
    )
    print(f"      corr(r_rod,r_last) = {corr:.4f}   hit = {hit:.4f}   n = {n}")
    print(f"      VERDICT (Bulenox basis): {report['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
