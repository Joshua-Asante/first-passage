"""G8 discharge re-check under corrected EVAL drawdown geometry (2026-07-22).

Both `trailing_locking` tiers (Tradeify_Select_100K, MFFU_Rapid_100K) carry
`dd_lock_offset_usd: 100` on rows that model the EVALUATION phase, where neither
firm applies drawdown locking:
  - Tradeify article 10495897: "Evaluation accounts do not have drawdown locking."
  - MFFU article 13286542: eval table lists only "Maximum Loss Limit (EOD) $3,000";
    "Max Loss Lock at $100" appears solely under Sim Funded parameters.

G8 (`discharges_falsifier`) requires >=2 firms clearing Part A, of which >=1 is
trailing_locking. The published 2026-07-15 discharge rested on Tradeify + MFFU --
i.e. on exactly the two tiers carrying the defect. This run recomputes the
discharge with the lock made unreachable on both (pure fixed-$ EOD trail = the
real eval geometry). Bulenox/BluSky are dd_type="trailing" and carry no lock
field, so they are untouched controls.

Full frozen four-tier set, frozen seeds/sims -- this is the decision-relevant
question, not a geometry isolation.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[4]
_HARNESS = _ROOT / "lab" / "analysis" / "c1" / "class_s_candidate1_scoring_2026-07-15"
for _p in (_ROOT / "core", _ROOT / "lab", _HARNESS,
           _ROOT / ".claude" / "skills" / "trade-csv-reconcile" / "scripts"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import numpy as np  # noqa: E402
import firm_rules  # noqa: E402
from discovery.prop_survivor_scoring import (  # noqa: E402
    load_scoring_thresholds, score_candidate,
)

sys.argv = [sys.argv[0]]
import run_class_s_c1_scoring as H  # noqa: E402

LOCKING_TIERS = ("Tradeify_Select_100K", "MFFU_Rapid_100K")
UNREACHABLE = 1_000_000.0


def main() -> int:
    thr = load_scoring_thresholds(H.GATE_PREREG)
    print(f"[cfg] tiers={thr.tier_keys}", flush=True)
    print(f"[cfg] seeds={thr.seeds} sims/seed={thr.sims_per_seed} "
          f"horizon={thr.horizon}", flush=True)
    print(f"[cfg] eval_bust_ceiling={thr.eval_bust_ceiling} "
          f"pass_floor={thr.pass_floor}", flush=True)

    panel, meta, trades = H.build_scaled_panel(
        H.C1_STRATS, H.C1_ALLOCS, expect_1r=dict(H.EXPECTED_1R)
    )
    daily = H.book_daily_at_100k(panel)
    tr = np.concatenate([s.to_numpy(dtype=float) for s in trades.values()])

    for t in LOCKING_TIERS:
        firm_rules.FIRM_RULES[t]["dd_lock_offset_usd"] = UNREACHABLE
    print(f"[patch] lock made unreachable on {LOCKING_TIERS}", flush=True)

    rep = score_candidate(
        strategy_label="c1 CORRECTED eval geometry (no eval locking)",
        candidate_daily_pnl=daily,
        full_res_trades=list(tr),
        envelope_verdict="YES",
        thresholds=thr,
        gross_edge_usd=float(tr[tr > 0].sum()),
    ).to_dict()

    # 2026-08-07 W1: restore-to-100 RETIRED (08-04 default is UNREACHABLE).
    # Historical A/B that *needs* the defective 100 baseline lives in
    # remc_eval_lock_fix.py / remc_native_postfix_check — not here.
    # docs/adr/2026-08-07-w1-intraday-honest-engine-remeasure.md
    for t in LOCKING_TIERS:
        firm_rules.FIRM_RULES[t]["dd_lock_offset_usd"] = UNREACHABLE

    print(f"\n{'tier':24s} {'dd_type':18s} {'run1 bust':>10s} {'run2 bust':>10s} "
          f"{'run2 pass':>10s} {'PartA':>7s}")
    for k, t in rep["tiers"].items():
        r1 = (t.get("run1") or {}).get("headline_bust", float("nan"))
        r2 = (t.get("run2") or {}).get("headline_bust", float("nan"))
        p2 = (t.get("run2") or {}).get("pass_rate", float("nan"))
        print(f"{k:24s} {t.get('dd_type',''):18s} {r1*100:9.2f}% {r2*100:9.2f}% "
              f"{p2*100:9.2f}% {str(t.get('clears_part_a')):>7s}")

    clearers = [k for k, t in rep["tiers"].items() if t.get("clears_part_a")]
    print(f"\nPart A clearers: {clearers}")
    print(f"discharges_falsifier (CORRECTED) = {rep['discharges_falsifier']}")
    print(f"  published 2026-07-15 = True (Tradeify + MFFU, both trailing_locking)")
    print(f"  routing = {rep.get('routing')}  halted_at={rep.get('halted_at')}")

    dest = Path(__file__).with_name("remc_g8_discharge_corrected.json")
    dest.write_text(json.dumps(rep, indent=2, default=str), encoding="utf-8")
    print(f"\n[written] {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
