"""MSL-S4 Explore-confirm -- scoring pass. Consumes
_explore_confirm_2026-08-21_RAW.json (written by explore_confirm_driver.py's
Phase 1-3) and runs:
  Phase 4 -- pilot calibration of the rank-ACF diagnostic tolerance (fresh,
             NOT borrowed from docs/spec/2026-08-18-magnitude-persistence-
             corrected-null-battery.md -- that battery's 0.04/0.07 numbers
             were fit to a different series; see EXPLORE_GO.md's own
             "Diagnostic gate" section for why reuse would be a defect).
  Phase 5 -- official IAAFT-surrogate significance test (frozen seed block
             [20260821, i], i=0..999 -- drawn ONLY after Phase 4 freezes a
             tolerance, never before) + delete/flip + verdict.

Every function here calls explore_confirm_lib.py for the actual statistics
(iaaft_significance_test, delete_pass, flip_pass, explore_verdict,
surrogate_diagnostic, generate_surrogate_returns, mean_displacement_reduction,
convergence_rate) -- nothing here reimplements them. This file only:
  (a) shapes pulled data into Cycle objects and price/return arrays,
  (b) runs the pilot-calibration procedure the DRAFT names but does not
      numerically pre-specify (structure frozen, numbers are pilot-owed),
  (c) assembles the disclosure bundle (RESULTS.json + LOG.md).

CONFIRM (2025-04-01..2025-09-29) is never read here -- this script only
consumes the RAW json, which itself only ever queried IS-window dates.
"""
import json
from pathlib import Path

import numpy as np

from research_utils.camp_import import load_camp_sibling

lib = load_camp_sibling("explore_confirm_lib", Path(__file__))

HERE = Path(__file__).parent
RAW_PATH = HERE / "_explore_confirm_2026-08-21_RAW.json"

# ---- pilot-calibration design (this driver's own choice, disclosed) --------
# Two DISJOINT pilot batches (both inside the block explicitly reserved for
# pilot/verification use, disjoint from the official i=0..999):
#   calibration batch: measures the natural rank-ACF reconstruction fidelity
#     of IAAFT on THIS series, to set a tolerance with headroom (mirrors the
#     corrected-null-battery's own "1.4x headroom over measured" convention
#     -- same convention, freshly measured numbers, per EXPLORE_GO.md).
#   gate-check batch: a SEPARATE pilot draw (not reused from calibration) is
#     what the frozen tolerance actually gates -- avoids the calibration
#     batch trivially passing the tolerance it was used to set.
CAL_OFFSET, CAL_N = 0, 200
GATE_OFFSET, GATE_N = 200, 50
HEADROOM = 1.4  # same margin convention as the precedent; number re-measured fresh


def _load_raw():
    with open(RAW_PATH) as f:
        return json.load(f)


def build_is_arrays(raw):
    """IS-window-only close/return arrays (start_price + real_returns) for
    the IAAFT significance test -- exactly the window the primary gate scores
    over. Separate from the padded array below (which exists only so the
    DELETE test's 60-session trailing median has real history)."""
    dates = raw["price_dates"]
    closes = raw["price_close"]
    is_start, is_end = str(lib.IS_START)[:10], str(lib.IS_END)[:10]
    is_idx = [i for i, d in enumerate(dates) if is_start <= d <= is_end]
    is_dates = [dates[i] for i in is_idx]
    is_closes = np.array([closes[i] for i in is_idx], dtype=float)
    real_returns = np.diff(np.log(is_closes))
    start_price = float(is_closes[0])
    return is_dates, is_closes, real_returns, start_price


def build_padded_arrays(raw):
    return raw["price_dates"], np.array(raw["price_close"], dtype=float)


def _idx_on_or_before(date_list, date_str):
    lo, hi = 0, len(date_list) - 1
    if date_str < date_list[0]:
        return None
    best = None
    for i, d in enumerate(date_list):
        if d <= date_str:
            best = i
        else:
            break
    return best


def build_cycles(raw, is_dates, padded_dates, padded_closes):
    """One lib.Cycle per scored candidate, with arm_start_idx/arm_end_idx
    relative to the IS-only array, and sham_reference (60-session trailing
    median of REAL padded prices, ending at arm_start) for the DELETE test."""
    cycles = []
    skipped = []
    for c in raw["scored_cycles"]:
        arm_start_idx = _idx_on_or_before(is_dates, c["arm_start"])
        arm_end_idx = _idx_on_or_before(is_dates, c["exp_date"])
        if arm_start_idx is None or arm_end_idx is None or arm_end_idx <= arm_start_idx:
            skipped.append(dict(c, reason="index_resolution_failed"))
            continue
        padded_i = _idx_on_or_before(padded_dates, c["arm_start"])
        if padded_i is None or padded_i < 59:
            skipped.append(dict(c, reason="insufficient_60session_lookback"))
            continue
        sham_ref = float(np.median(padded_closes[padded_i - 59: padded_i + 1]))
        cycles.append(lib.Cycle(
            contract=c.get("contract_code", c["exp_date"]),
            expiry=c["exp_date"],
            strike_star=c["strike_star"],
            arm_start_idx=arm_start_idx,
            arm_end_idx=arm_end_idx,
            sham_reference=sham_ref,
        ))
    return cycles, skipped


# ============================================================================
# Phase 4 -- pilot calibration (fresh, on real IS returns)
# ============================================================================

def calibrate_tolerance(real_returns, n_iter):
    deltas = []
    for i in range(CAL_OFFSET, CAL_OFFSET + CAL_N):
        rng = np.random.default_rng([lib.IAAFT_SEED_BLOCK, lib.IAAFT_PILOT_SEED_BLOCK + i])
        surr = lib.generate_surrogate_returns(real_returns, rng, n_iter=n_iter)
        diag = lib.surrogate_diagnostic(real_returns, surr)
        deltas.append(diag["max_abs_delta"])
    deltas = np.array(deltas)
    return dict(
        n_iter=n_iter, n_draws=CAL_N,
        median=float(np.median(deltas)), p95=float(np.percentile(deltas, 95)),
        tol_median=float(HEADROOM * np.median(deltas)),
        tol_p95=float(HEADROOM * np.percentile(deltas, 95)),
        raw_deltas=deltas.tolist(),
    )


def gate_check(real_returns, n_iter, tol_median, tol_p95):
    deltas = []
    for i in range(GATE_OFFSET, GATE_OFFSET + GATE_N):
        rng = np.random.default_rng([lib.IAAFT_SEED_BLOCK, lib.IAAFT_PILOT_SEED_BLOCK + i])
        surr = lib.generate_surrogate_returns(real_returns, rng, n_iter=n_iter)
        diag = lib.surrogate_diagnostic(real_returns, surr)
        deltas.append(diag["max_abs_delta"])
    deltas = np.array(deltas)
    med, p95 = float(np.median(deltas)), float(np.percentile(deltas, 95))
    passed = (med <= tol_median) and (p95 <= tol_p95)
    return dict(n_iter=n_iter, n_draws=GATE_N, median=med, p95=p95, passed=passed,
                raw_deltas=deltas.tolist())


def run_pilot_ladder(real_returns):
    """Escalation ladder per EXPLORE_GO.md: n_iter=100 default -> n_iter=500
    -> VOID. (The DRAFT's third rung, "Schreiber end-matching trim," is not
    implemented in explore_confirm_lib.py -- disclosed as a real gap, not
    silently skipped; VOID is the actual floor this driver can reach.)"""
    for n_iter in (lib.IAAFT_ITER_DEFAULT, lib.IAAFT_ITER_ESCALATED):
        cal = calibrate_tolerance(real_returns, n_iter)
        gate = gate_check(real_returns, n_iter, cal["tol_median"], cal["tol_p95"])
        if gate["passed"]:
            return dict(diagnostic_ok=True, n_iter_used=n_iter, calibration=cal, gate=gate,
                        escalated=(n_iter != lib.IAAFT_ITER_DEFAULT))
    return dict(diagnostic_ok=False, n_iter_used=lib.IAAFT_ITER_ESCALATED,
                calibration=cal, gate=gate, escalated=True,
                note="Schreiber end-matching trim not implemented in explore_confirm_lib.py; "
                     "VOID reached without that third rung.")


# ============================================================================
# Phase 5 -- official IAAFT test + delete/flip + verdict
# ============================================================================

def naive_control_full_n(padded_dates, padded_closes, raw):
    """The 2026-08-21 cheap falsifier's own fixed-offset control, re-run at
    full IS n for continuity (disclosed, non-gating per EXPLORE_GO.md's
    Disclose row)."""
    rows = []
    for c in raw["scored_cycles"]:
        arm_start_i = _idx_on_or_before(padded_dates, c["arm_start"])
        arm_end_i = _idx_on_or_before(padded_dates, c["exp_date"])
        ctrl_start_date = str(np.busday_offset(np.datetime64(c["exp_date"], "D"), -13, roll="backward"))
        ctrl_end_date = str(np.busday_offset(np.datetime64(c["exp_date"], "D"), -10, roll="backward"))
        ctrl_start_i = _idx_on_or_before(padded_dates, ctrl_start_date)
        ctrl_end_i = _idx_on_or_before(padded_dates, ctrl_end_date)
        if None in (arm_start_i, arm_end_i, ctrl_start_i, ctrl_end_i):
            continue
        strike = c["strike_star"]
        arm_disp_start = abs(padded_closes[arm_start_i] - strike)
        arm_disp_end = abs(padded_closes[arm_end_i] - strike)
        ctrl_disp_start = abs(padded_closes[ctrl_start_i] - strike)
        ctrl_disp_end = abs(padded_closes[ctrl_end_i] - strike)
        rows.append(dict(
            exp_date=c["exp_date"],
            arm_converged=bool(arm_disp_end < arm_disp_start),
            ctrl_converged=bool(ctrl_disp_end < ctrl_disp_start),
            arm_reduction=float(arm_disp_start - arm_disp_end),
            ctrl_reduction=float(ctrl_disp_start - ctrl_disp_end),
        ))
    if not rows:
        return dict(n=0)
    arm_rate = np.mean([r["arm_converged"] for r in rows])
    ctrl_rate = np.mean([r["ctrl_converged"] for r in rows])
    both_conv = sum(1 for r in rows if r["arm_converged"] and r["ctrl_converged"])
    both_div = sum(1 for r in rows if not r["arm_converged"] and not r["ctrl_converged"])
    outcome_correlated = (both_conv + both_div) / len(rows)
    return dict(
        n=len(rows), arm_converge_rate=float(arm_rate), ctrl_converge_rate=float(ctrl_rate),
        outcome_correlated_frac=float(outcome_correlated), rows=rows,
    )


def main():
    raw = _load_raw()
    is_dates, is_closes, real_returns, start_price = build_is_arrays(raw)
    padded_dates, padded_closes = build_padded_arrays(raw)
    cycles, skipped = build_cycles(raw, is_dates, padded_dates, padded_closes)
    n_cycles_is = len(cycles)
    print(f"[score] {n_cycles_is} cycles usable ({len(skipped)} skipped) "
          f"of {len(raw['scored_cycles'])} pulled")
    for s in skipped:
        print(f"  skipped {s.get('exp_date')}: {s['reason']}")

    print("=== Phase 4: pilot calibration ===")
    ladder = run_pilot_ladder(real_returns)
    print(f"[pilot] n_iter_used={ladder['n_iter_used']} diagnostic_ok={ladder['diagnostic_ok']}")
    print(f"[pilot] calibration (n={ladder['calibration']['n_draws']}): "
          f"median={ladder['calibration']['median']:.5f} p95={ladder['calibration']['p95']:.5f} "
          f"-> tol_median={ladder['calibration']['tol_median']:.5f} tol_p95={ladder['calibration']['tol_p95']:.5f}")
    print(f"[pilot] gate-check (n={ladder['gate']['n_draws']}): "
          f"median={ladder['gate']['median']:.5f} p95={ladder['gate']['p95']:.5f} passed={ladder['gate']['passed']}")

    if n_cycles_is < 20:
        verdict = "VOID"
        result = None
    else:
        print("=== Phase 5: official IAAFT significance test (seed block frozen, i=0..999) ===")
        result = lib.iaaft_significance_test(
            real_returns, start_price, cycles,
            m=lib.IAAFT_M, n_iter=ladder["n_iter_used"], seed_block=lib.IAAFT_SEED_BLOCK,
            statistic="mean_displacement_reduction",
        )
        print(f"[iaaft] real_stat={result.real_stat:.4f} p_upper={result.p_upper:.4f} "
              f"p_lower={result.p_lower:.4f} percentile={result.percentile:.2f}")

        real_price_is = start_price * np.exp(np.concatenate([[0.0], np.cumsum(real_returns)]))
        conv_rate = lib.convergence_rate(real_price_is, cycles)
        constrained_stat = lib.mean_displacement_reduction(real_price_is, cycles, reference="strike")
        sham_stat = lib.mean_displacement_reduction(real_price_is, cycles, reference="sham")
        delete_passed = lib.delete_pass(constrained_stat, sham_stat)
        diverge_stat = -constrained_stat
        flip_passed = lib.flip_pass(constrained_stat, diverge_stat)

        verdict = lib.explore_verdict(
            iaaft_p_upper=result.p_upper, delete_passed=delete_passed, flip_passed=flip_passed,
            diagnostic_ok=ladder["diagnostic_ok"], n_cycles_is=n_cycles_is,
        )
        print(f"[req1a] constrained_stat={constrained_stat:.4f} sham_stat={sham_stat:.4f} "
              f"delete_pass={delete_passed}")
        print(f"[req1a] converge_stat={constrained_stat:.4f} diverge_stat={diverge_stat:.4f} "
              f"flip_pass={flip_passed}")
        print(f"[disclose] convergence_rate={conv_rate:.4f}")

    print("=== Disclosure: naive fixed-offset control re-run at full n ===")
    naive = naive_control_full_n(padded_dates, padded_closes, raw)
    print(f"[naive] n={naive.get('n')} arm_rate={naive.get('arm_converge_rate')} "
          f"ctrl_rate={naive.get('ctrl_converge_rate')} "
          f"outcome_correlated_frac={naive.get('outcome_correlated_frac')}")

    print(f"\n=== VERDICT: {verdict} ===")

    out = dict(
        verdict=verdict,
        n_cycles_is=n_cycles_is,
        n_skipped=len(skipped),
        skipped=skipped,
        pilot=dict(
            n_iter_used=ladder["n_iter_used"], diagnostic_ok=ladder["diagnostic_ok"],
            escalated=ladder["escalated"],
            calibration={k: v for k, v in ladder["calibration"].items() if k != "raw_deltas"},
            calibration_raw_deltas=ladder["calibration"]["raw_deltas"],
            gate={k: v for k, v in ladder["gate"].items() if k != "raw_deltas"},
            gate_raw_deltas=ladder["gate"]["raw_deltas"],
            note=ladder.get("note"),
        ),
        iaaft=None if result is None else dict(
            real_stat=result.real_stat, p_upper=result.p_upper, p_lower=result.p_lower,
            percentile=result.percentile, m=lib.IAAFT_M, n_iter=ladder["n_iter_used"],
            seed_block=lib.IAAFT_SEED_BLOCK,
            null_stats_summary=dict(
                mean=float(np.mean(result.null_stats)), sd=float(np.std(result.null_stats)),
                percentiles={p: float(np.percentile(result.null_stats, p))
                             for p in (2.5, 5, 25, 50, 75, 95, 97.5)},
            ),
            null_stats_full=result.null_stats.tolist(),
        ),
        req1a=None if result is None else dict(
            convergence_rate=conv_rate, constrained_stat=constrained_stat, sham_stat=sham_stat,
            delete_passed=delete_passed, diverge_stat=diverge_stat, flip_passed=flip_passed,
        ),
        naive_control_full_n=naive,
        cycles_used=[dict(contract=c.contract, expiry=c.expiry, strike_star=c.strike_star,
                           arm_start_idx=c.arm_start_idx, arm_end_idx=c.arm_end_idx,
                           sham_reference=c.sham_reference) for c in cycles],
    )
    out_path = HERE / "_explore_confirm_2026-08-21_RESULTS.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"[done] wrote {out_path}")
    return out


if __name__ == "__main__":
    main()
