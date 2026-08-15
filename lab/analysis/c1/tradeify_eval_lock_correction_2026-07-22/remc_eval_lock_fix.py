"""Eval-tier re-MC: Tradeify Select drawdown-LOCKING correction (2026-07-22).

Authorised by operator 2026-07-22.

Defect: `FIRM_RULES["Tradeify_Select_*"]["dd_lock_offset_usd"] = 100` encodes a
mechanism that does not exist in the EVALUATION phase. Tradeify, verbatim
(help.tradeify.co article 10495897, re-verified 2026-07-22):
    "Q: Does drawdown lock on Evaluation accounts?
     A: No. Drawdown only locks on Sim Funded accounts.
        Evaluation accounts do not have drawdown locking."

These rows model the eval (profit_target 6% = eval target, min_trading_days 3
from the eval-only consistency rule, eval micro caps), so the lock is wrong here.

Correction: keep dd_type="trailing_locking" (the fixed-$ trail is right) but make
the lock unreachable, which is the engine's own idiom for "pure fixed-$ trail"
(tests/core/test_trailing_locking_boundary.py uses dd_lock_offset_usd=1_000_000).
NOT None -- None makes the whole branch inert (no DD check at all).

Run 1 reproduces the published 2026-07-15 Class-S c1 scoring numbers (baseline
integrity check -- an artefact agreeing with its own pin is not evidence);
Run 2 applies the correction. Same panel bytes, same seeds, same sims.
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

import firm_rules  # noqa: E402
from discovery.prop_survivor_scoring import (  # noqa: E402
    blocks_from_daily_pnl, load_scoring_thresholds, run_tier_remc,
)

sys.argv = [sys.argv[0]]
import run_class_s_c1_scoring as H  # noqa: E402

TIER = "Tradeify_Select_100K"
UNREACHABLE = 1_000_000.0


PUBLISHED = {"run1_bust": 0.026466666666666666, "run1_pass": 0.9734333333333334,
             "run2_bust": 0.1788}


def main() -> int:
    from discovery.prop_survivor_scoring import score_candidate
    import numpy as np

    thr = load_scoring_thresholds(H.GATE_PREREG)
    print(f"[cfg] seeds={thr.seeds} sims/seed={thr.sims_per_seed} horizon={thr.horizon}",
          flush=True)

    panel, meta, trades = H.build_scaled_panel(
        H.C1_STRATS, H.C1_ALLOCS, expect_1r=dict(H.EXPECTED_1R)
    )
    daily_100k = H.book_daily_at_100k(panel)
    tr = np.concatenate([s.to_numpy(dtype=float) for s in trades.values()])
    print(f"[panel] legs={H.C1_STRATS} rows={len(panel)} days={len(daily_100k)}",
          flush=True)
    print(f"[scope] Tradeify tier ONLY — geometry-isolation diagnostic, not a "
          f"live scoring claim (score_candidate tiers= override)", flush=True)

    dest = Path(__file__).with_name("remc_eval_lock_fix_report.json")
    out = {}
    for label, offset in (("BASELINE_lock_100_as_published", 100.0),
                          ("CORRECTED_eval_no_locking", UNREACHABLE)):
        firm_rules.FIRM_RULES[TIER]["dd_lock_offset_usd"] = offset
        rep = score_candidate(
            strategy_label=f"c1 {label}",
            candidate_daily_pnl=daily_100k,
            full_res_trades=list(tr),
            envelope_verdict="YES",
            thresholds=thr,
            gross_edge_usd=float(tr[tr > 0].sum()),
            tiers=(TIER,),
        ).to_dict()
        t = rep["tiers"][TIER]
        out[label] = {"dd_lock_offset_usd": offset, "tier": t}
        dest.write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
        print(f"\n=== {label} (dd_lock_offset_usd={offset}) ===", flush=True)
        for run in ("run1", "run2"):
            r = t.get(run) or {}
            print(f"  {run}: bust={r.get('headline_bust', float('nan'))*100:6.2f}%  "
                  f"pass={r.get('pass_rate', float('nan'))*100:6.2f}%", flush=True)
        print(f"  clears_part_a={t.get('clears_part_a')} gated_on={t.get('gated_on')}",
              flush=True)

    # 2026-08-07 W1: end-of-script restore-to-100 RETIRED for process hygiene.
    # The BASELINE arm above still temporarily sets 100 for the A/B measurement;
    # leave process memory at the post-08-04 production default (UNREACHABLE).
    # docs/adr/2026-08-07-w1-intraday-honest-engine-remeasure.md
    firm_rules.FIRM_RULES[TIER]["dd_lock_offset_usd"] = UNREACHABLE

    b, c = out["BASELINE_lock_100_as_published"]["tier"], \
           out["CORRECTED_eval_no_locking"]["tier"]
    print("\n=== DELTA (corrected - baseline) ===")
    for run in ("run1", "run2"):
        bb, cc = b.get(run) or {}, c.get(run) or {}
        if "headline_bust" in bb and "headline_bust" in cc:
            d = (cc["headline_bust"] - bb["headline_bust"]) * 100
            print(f"  {run} bust: {bb['headline_bust']*100:.2f}% -> "
                  f"{cc['headline_bust']*100:.2f}%  ({d:+.2f} pp)")
    print(f"\n[published 2026-07-15] Run-1 bust {PUBLISHED['run1_bust']*100:.2f}% / "
          f"pass {PUBLISHED['run1_pass']*100:.2f}%; Run-2 bust {PUBLISHED['run2_bust']*100:.2f}%")
    r1 = (b.get('run1') or {}).get('headline_bust')
    if r1 is not None:
        ok = abs(r1 - PUBLISHED['run1_bust']) < 5e-4
        print(f"[reproduction] baseline Run-1 {r1*100:.2f}% vs published 2.65% -> "
              f"{'MATCH' if ok else 'MISMATCH - delta NOT trustworthy'}")
    print(f"\n[written] {dest}")

    dest = Path(__file__).with_name("remc_eval_lock_fix_report.json")
    dest.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\n[written] {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
