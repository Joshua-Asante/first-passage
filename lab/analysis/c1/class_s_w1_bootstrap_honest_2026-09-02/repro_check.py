"""Reproduction control: do THIS harness's full/H1/H2 partitions match the published pins?

Isolates whether the bootstrap control gap (this run ~0.68% vs published 1.20%) comes from the
panel/engine layer or only from the bootstrap layer. Published pins:
  EOD corrected 0.50x  Tradeify full 0.11% / H1 0.22% / H2 0.04%  (CORRECTED_FULLPANEL.md)
  Honest  W1   0.50x   Tradeify full 0.72% / H1 1.77% / H2 0.28%  (RESULTS_INTRADAY_W1.md)
No bootstrap. Tradeify only. $0/K=0.
"""
from __future__ import annotations
import json, os, sys, time
from pathlib import Path
for k in ("OMP_NUM_THREADS","MKL_NUM_THREADS","OPENBLAS_NUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(k, "1")
import numpy as np
_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[3]
_W1 = _ROOT/"lab"/"analysis"/"c1"/"class_s_c1_haircut_regime_remc_2026-07-16"
for p in (str(_HERE), str(_ROOT/"core"), str(_ROOT/"lab"), str(_W1)):
    if p not in sys.path: sys.path.insert(0, p)
import firm_rules
from discovery.prop_survivor_scoring import load_scoring_thresholds, paired_blocks_from_daily, run_tier_remc
_a = list(sys.argv); sys.argv = [sys.argv[0]]
import run_class_s_c1_scoring as S
import run_class_s_c1_regime_gate as R
import run_w1_intraday_both_halves as W1
sys.argv = _a

PUB = {"eod": {"full":0.0011,"H1":0.0022,"H2":0.0004},
       "honest": {"full":0.0072,"H1":0.0177,"H2":0.0028}}
TIER = "Tradeify_Select_100K"

S.phase0_verify()
for leg in S.C1_STRATS: S.resolve_panel_path(leg)
panel, meta, _ = S.build_scaled_panel(S.C1_STRATS, S.C1_ALLOCS, expect_1r=dict(S.EXPECTED_1R))
daily = S.book_daily_at_100k(panel)
thr = load_scoring_thresholds(S.GATE_PREREG)
intraday, cov = W1.build_book_intraday_low(panel, meta)
firm_rules.FIRM_RULES[TIER]["dd_lock_offset_usd"] = 1_000_000.0
firm_rules.FIRM_RULES["MFFU_Rapid_100K"]["dd_lock_offset_usd"] = 1_000_000.0
dh, ih = daily*0.50, intraday*0.50
h1,h2,mid = R.half_panel_split(dh); i1,i2,_ = R.half_panel_split(ih)
cons = R._consistency_frac(TIER)
out = {"tier":TIER,"panel_span":meta["panel_span"],"n_bdays":meta["n_bdays"],
       "numpy":np.__version__,"published":PUB,"measured":{"eod":{},"honest":{}}}
for name,(dd,ii) in {"full":(dh,ih),"H1":(h1,i1),"H2":(h2,i2)}.items():
    bp, bl = paired_blocks_from_daily(dd, ii)
    t=time.time()
    e = run_tier_remc(TIER, bp, thr, consistency=cons)
    h = run_tier_remc(TIER, bp, thr, consistency=cons, intraday_blocks=bl)
    for arm,r in (("eod",e),("honest",h)):
        b=float(r["headline_bust"]); p=float(r["pass_rate"])
        d=b-PUB[arm][name]
        out["measured"][arm][name]={"bust":b,"pass":p,"published":PUB[arm][name],
                                    "delta_pp":d*100,"match_1e4":abs(d)<=1e-4}
        print(f"{name:5s} {arm:6s} bust={b:.4%} pass={p:.2%} published={PUB[arm][name]:.2%} "
              f"delta={d*100:+.3f}pp {'MATCH' if abs(d)<=1e-4 else 'MISMATCH'}", flush=True)
    print(f"      ({time.time()-t:.0f}s)", flush=True)
(_HERE/"repro_check_report.json").write_text(json.dumps(out, indent=2)+"\n", encoding="utf-8")
print("written repro_check_report.json")
