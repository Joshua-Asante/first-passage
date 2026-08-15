"""CC-handoff §2.6 follow-on #2 — RISK-NEUTRAL 5th-leg insertion (constant total risk).

The part-2 sweep ADDED the 5th leg (total risk 2.91% -> 3.41%), so the added
capital-at-risk fought the diversification and nothing restored the p99 gate. This
script holds TOTAL RISK CONSTANT at the locked 2.91%: trim the four legs by
k = (2.91% - w5)/2.91% and slot the freed risk w5 into the 5th leg. Scaling a
leg's static $-stream by k exactly models running it at k× its risk
(roe×200K -> k·roe×200K).

Three configs per w5, each on full panel + H1 (2020-2023 chop) + H2 (2023-2026):
  * baseline       : 4 legs @ locked (total 2.91%)
  * de-risk-only   : 4 legs ×k (total 2.91-w5, NO 5th)  -- the 2026-06-07 reference
  * insertion      : 4 legs ×k + 5th @ w5 (total 2.91%) -- the test

Isolates the 5th leg's MARGINAL value at constant total risk. Reuses the production
MC + part-2 synthetic generator verbatim; joblib-parallel over (config × partition).
NO fabricated instrument CSV.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
from analyze_part1 import run_mc, ACCOUNT, ALLOC, FIXED_1R  # noqa: E402
import analyze_part2 as P2  # noqa: E402  (panel, make_synth, worst_days)

panel = P2.panel
LEGS = list(panel.columns)
ORIG = dict(ALLOC)                          # locked 4-leg allocations
TOTAL = sum(ORIG.values())                  # 0.0291
ACCT = ACCOUNT
SPLIT = pd.Timestamp("2023-03-20")
H1 = np.asarray(panel.index < SPLIT)
H2 = np.asarray(panel.index >= SPLIT)
FULL = np.ones(len(panel), bool)
PARTS = {"full": FULL, "H1": H1, "H2": H2}


def mc_config(k, synth_arr, w5, mask):
    """4 legs scaled by k (+ optional synth at w5), run on the masked sub-panel.
    Top-level so loky can pickle it; rebuilds trades from `panel` (module global,
    re-imported in workers) + passed arrays."""
    idx = panel.index[mask]
    trades, allocs, fixed = {}, {}, {}
    for leg in LEGS:
        trades[leg] = pd.DataFrame({"exit_date": idx, "pnl": panel[leg].to_numpy()[mask]})
        allocs[leg] = k * ORIG[leg]
        fixed[leg] = ORIG[leg] * ACCT       # natural 1R of the static stream -> scale = k
    if synth_arr is not None:
        trades["synth5"] = pd.DataFrame({"exit_date": idx, "pnl": synth_arr[mask]})
        allocs["synth5"] = w5
        fixed["synth5"] = w5 * ACCT
    return run_mc(trades, allocs, fixed)


def gate(r):
    return "CLEAR" if (r["bust_rate"] < 0.01 and r["p99_dd"] < 0.05) else "fail"


W5_GRID = [0.0050, 0.0100]          # 0.50% and 1.00% reallocated into the 5th leg
RHO_GRID = [0.0, -0.6]              # uncorrelated vs strongly anti-correlated
PF_GRID = ["solid(PF~1.5)", "strong(PF~2.0)"]
ACTIVE = {3, 4}                     # Thu/Fri fill


def main():
    base = {p: mc_config(1.0, None, 0.0, m) for p, m in PARTS.items()}
    print("=" * 104)
    print("§2.6 RISK-NEUTRAL 5th-leg INSERTION (constant total risk 2.91%) — does reallocation clear")
    print("     the gates / the H1 regime where ADD could not and de-risk-only could not?")
    print("=" * 104)
    print(f"{'config':<46}{'Σrisk%':>7}{'part':>6}{'pass':>8}{'bust':>8}{'p99':>8}{'med':>5}{'gate':>7}")

    def show(label, sigma, parts_res):
        for p in ("full", "H1", "H2"):
            r = parts_res[p]
            print(f"{(label if p=='full' else ''):<46}{(f'{sigma*100:.2f}' if p=='full' else ''):>7}"
                  f"{p:>6}{r['pass_rate']:>8.2%}{r['bust_rate']:>8.2%}{r['p99_dd']:>8.2%}"
                  f"{str(r['median_days_to_pass']):>5}{gate(r):>7}")

    show("BASELINE 4-leg @ locked", TOTAL, base)
    print("-" * 104)

    rows = []
    # precompute synth arrays per (w5, pf, rho) so partitions share one realization
    from joblib import Parallel, delayed
    for w5 in W5_GRID:
        k = (TOTAL - w5) / TOTAL
        # de-risk-only reference (no 5th leg) at total = 2.91 - w5
        dro = {p: mc_config(k, None, w5, m) for p, m in PARTS.items()}
        show(f"de-risk-only k={k:.3f} (no 5th)", TOTAL - w5, dro)
        # insertion cells
        for pf in PF_GRID:
            for rho in RHO_GRID:
                synth, diag = P2.make_synth(ACTIVE, pf, rho, w5, seed=2000 + int(w5 * 1e4) + int(rho * 10))
                arr = synth.to_numpy()
                res = dict(zip(PARTS, Parallel(n_jobs=6, backend="loky")(
                    delayed(mc_config)(k, arr, w5, m) for m in PARTS.values())))
                label = f"insert {pf} ρ{rho:+.1f}(r{diag['realized_rho']:+.2f}) PF{diag['realized_pf']:.2f}"
                show(label, TOTAL, res)
                f = res["full"]
                rows.append({"w5": w5, "k": k, "pf": pf, "rho": rho,
                             "rho_real": diag["realized_rho"], "pf_real": diag["realized_pf"],
                             "full_pass": f["pass_rate"], "full_bust": f["bust_rate"],
                             "full_p99": f["p99_dd"], "full_gate": gate(f),
                             "H1_gate": gate(res["H1"]), "H1_bust": res["H1"]["bust_rate"],
                             "H1_p99": res["H1"]["p99_dd"],
                             "dpass": f["pass_rate"] - base["full"]["pass_rate"],
                             "dp99": f["p99_dd"] - base["full"]["p99_dd"]})
        print("-" * 104)

    # ── summary verdicts ───────────────────────────────────────────────────
    bf = base["full"]
    print(f"\nBaseline full-panel: pass {bf['pass_rate']:.2%} / bust {bf['bust_rate']:.2%} / "
          f"p99 {bf['p99_dd']:.2%}  (both gates breach).  H1 baseline gate: {gate(base['H1'])} "
          f"(bust {base['H1']['bust_rate']:.2%}, p99 {base['H1']['p99_dd']:.2%}).")
    full_clear = [r for r in rows if r["full_gate"] == "CLEAR"]
    h1_clear = [r for r in rows if r["H1_gate"] == "CLEAR"]
    print(f"\nRisk-neutral insertions that RESTORE the FULL-panel gates at constant 2.91% risk: "
          f"{len(full_clear)}/{len(rows)}")
    for r in sorted(full_clear, key=lambda r: r["full_p99"]):
        print(f"  w5={r['w5']*100:.2f}% {r['pf']} ρ{r['rho']:+.1f}: pass {r['full_pass']:.2%} "
              f"bust {r['full_bust']:.2%} p99 {r['full_p99']:.2%}  (Δp99 {r['dp99']*100:+.2f}pp vs baseline)")
    print(f"\nRisk-neutral insertions that CLEAR the hard H1 regime: {len(h1_clear)}/{len(rows)}")
    for r in h1_clear:
        print(f"  w5={r['w5']*100:.2f}% {r['pf']} ρ{r['rho']:+.1f}: H1 bust {r['H1_bust']:.2%} p99 {r['H1_p99']:.2%}")
    if not h1_clear:
        print("  NONE — reallocation does not fix the chop-regime tail (same as static de-risk & ADD).")
    json.dump({"baseline_full": bf["pass_rate"], "rows": rows},
              open(OUT_JSON := str(_HERE / "fifth_leg_riskneutral.json"), "w"), indent=2)
    print(f"\nSaved {OUT_JSON}")


if __name__ == "__main__":
    main()
