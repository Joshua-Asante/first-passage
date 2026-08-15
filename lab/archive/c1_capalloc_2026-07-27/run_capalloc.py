#!/usr/bin/env python3
"""Q-CAPALLOC-1 runner — is the c1 per-leg contract-cap allocation dominated?

Executes the FROZEN pre-registration:
    docs/briefs/pre-registration/Q-CAPALLOC-1-verdict-preregistration.md @ 4fac99c
    (signed §9 2026-07-27; this file must be committed AFTER that one — §10 hook 5)

Nothing here re-decides the pre-registration. Candidate set, rung, partitions,
engine, seeds, horizons, and the D1-D5 gate are all consumed as fixed inputs.

WHAT IS IMPORTED, NOT REIMPLEMENTED (§8: "imports the kernels; must not edit in
place"): `reserve`, `load_leg`, `day_stack`, `eval_sim`, `funded_sim`, and the
Select-100K rule constants all come from
`lab/analysis/tradeify_book_composition_2026-07-23/gap_stage2_capbound.py`,
whose own kernels are verbatim ports of `gap_stage2.py` @ `61424aa`.

ONE PERFORMANCE REFACTOR, PROVEN EQUIVALENT
-------------------------------------------
`build_paths` rebuilds resampled paths per (cell, partition, seed) with a
6,000-iteration Python loop. The block-index draw does not depend on the cell:
`gap_stage2.py::run_scenario` creates `default_rng(seed)` fresh per scenario, so
every cell would draw the IDENTICAL `picks` array. This runner therefore hoists
the draw into `build_day_index`, which returns the (n_paths, horizon) matrix of
panel-day indices; each cell's series is then `pnl[day_idx]` / `qmax[day_idx]`.

Equivalence is exact, not approximate: same `rng.integers(0, nb, size=...)` call
with the same arguments in the same order (eval draw, then funded draw), the same
block concatenation order, the same `[:horizon]` truncation. It is verified, not
asserted — CONTROL 1 below reproduces the incumbent's published figures.

Side benefit: all 12 cells are now compared on IDENTICAL resampled paths, i.e.
the comparison is paired. That strictly reduces contrast variance and cannot
favour any cell.

CONTROLS (all must pass before any verdict is emitted)
------------------------------------------------------
1. Incumbent reproduction (§6 row c): canonical cell 68/12 at FULL panel must
   reproduce the 2026-07-27 session figures 12.2 mo eval median / 5.5 mo first
   payout / $32,904 E[cash] within 1 across-seed sd. Miss => harness defect,
   NO VERDICT.
2. Split-identity: live 69/11 and canonical 68/12 yield reserve pair (8,1) and
   must produce byte-identical daily series.
3. Candidate-set identity: the enumeration must reproduce the frozen 12 cells
   from §5 exactly, in order.
4. Compliance invariant (D5): every scored cell's max combined stack <= 80.
5. Half-panel coverage: H1 + H2 business days must sum to the full panel.

  python lab/analysis/c1_capalloc_2026-07-27/run_capalloc.py
  python lab/analysis/c1_capalloc_2026-07-27/run_capalloc.py --smoke   # fast wiring check
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
_REPO = _HERE.parent.parent.parent
_BOOKCOMP = _REPO / "lab" / "analysis" / "tradeify_book_composition_2026-07-23"
for _p in (str(_BOOKCOMP), str(_HERE)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import funded_scaling as FS
import gap_stage2_capbound as G  # noqa: E402
from paths import DAILY_PANEL  # noqa: E402

PREREG = "docs/briefs/pre-registration/Q-CAPALLOC-1-verdict-preregistration.md"
PREREG_COMMIT = "4fac99c"

# --- FROZEN from the pre-registration §5 (consumed, never re-decided) --------
SEEDS = (11, 12, 13)
N_PATHS = 6_000
H_EVAL = 2_600
H_FUND = 2_600
CAP_FIRM = 80
BD_PER_MO = 21.7

# §6 row c — the incumbent figures this run must reproduce.
# Incumbent reproduction pins.
# `eval_med_mo` RE-PINNED 12.2 -> 10.3 on 2026-07-29. Justification traces to a
# merged fix, not to greening a run: PR #544 removed the funded-only drawdown
# lock that `eval_sim` was wrongly applying during evaluation (Tradeify article
# 10495897 - evaluations do not lock). That fix legitimately shortens the eval
# median. The FUNDED pins below are UNCHANGED and still reproduce exactly
# (first_pay_mo 5.5; mean_cash 32,903.8 vs 32,904.0 within tolerance), which is
# what confirms the funded-side harness did not drift. Tolerances are untouched.
CONTROL_PINS = {"eval_med_mo": 10.3, "first_pay_mo": 5.5, "mean_cash": 32_904.0}

# §4 dominance thresholds.
D1_MIN_MONTHS = 0.50
D2_MIN_REL = 0.10
D3_MAX_PP_WORSE = 2.0
D4_MAX_PP_WORSE = 2.0

# §6 row d — pre-committed sensitivity on the three unverified rule pins.
# The frozen text names the pins but not the alternative VALUES; the brackets
# below are this runner's disclosure, chosen to straddle the modeled value.
SENSITIVITY = [
    ("WIN_MIN", 100.0), ("WIN_MIN", 300.0),
    ("FUNDED_LADDER", "legacy"),
    ("PAYOUT_MIN", 500.0), ("PAYOUT_MIN", 2_000.0),
]


def enumerate_cells() -> list[dict]:
    """§5 frozen rule: distinct reserve pairs, canonical rep = MINIMUM cap_mym."""
    seen: dict[tuple[int, int], int] = {}
    for cm in range(9, 70):
        cn = CAP_FIRM - cm
        rm, rn = G.reserve(cm, 750.0), G.reserve(cn, 1000.0)
        if rm < 1 or rn < 1:
            continue
        if rm + math.floor(rm * 7.5) + rn + math.floor(rn * 10) > CAP_FIRM:
            continue
        seen.setdefault((rm, rn), cm)
    return [
        {"res": k, "cap_mym": v, "cap_mnq": CAP_FIRM - v,
         "label": f"{v}/{CAP_FIRM - v}", "res_label": f"{k[0]}/{k[1]}",
         "incumbent": k == (8, 1)}
        for k, v in sorted(seen.items())
    ]


def cell_series(cap_mym: int, cap_mnq: int, idx: pd.DatetimeIndex):
    """Daily rail-sized P&L + daily max combined stack for one cap split."""
    G.LEGS["MYM"]["cap_new"] = cap_mym
    G.LEGS["MNQ"]["cap_new"] = cap_mnq
    legs = []
    for nm, cfg in G.LEGS.items():
        import contextlib
        import io
        with contextlib.redirect_stdout(io.StringIO()):   # load_leg prints a summary
            legs.append(G.load_leg(nm, cfg))
    tr = pd.concat(legs, ignore_index=True)
    tr["exit_dt"] = tr["dt"]
    d = tr.groupby("exit_date")["pnl_rail"].sum().reindex(idx).fillna(0.0)
    q = G.day_stack(tr, "rail_q", idx)
    return d.values.astype(float), q, float(tr["pnl_rail"].sum())


def build_day_index(blocks, nb, n_paths, horizon, rng) -> np.ndarray:
    """Hoisted, cell-independent form of gap_stage2.build_paths (see docstring)."""
    di = np.zeros((n_paths, horizon), dtype=np.int32)
    max_blocks = horizon // 3 + 3
    picks = rng.integers(0, nb, size=(n_paths, max_blocks))
    for i in range(n_paths):
        seq, tot = [], 0
        for b in picks[i]:
            idxs = blocks[b]
            seq.append(idxs)
            tot += len(idxs)
            if tot >= horizon:
                break
        cat = np.concatenate(seq)
        if cat.size < horizon:                    # frozen engine cannot serve
            raise RuntimeError(                    # this partition; never silent
                f"block budget exhausted: {cat.size} < horizon {horizon}")
        di[i] = cat[:horizon]
    return di


def week_blocks(idx: pd.DatetimeIndex, positions: np.ndarray) -> list[np.ndarray]:
    """Mon-anchored week blocks over a partition, as LOCAL positions."""
    sub = idx[positions]
    keys = sub - pd.to_timedelta(sub.weekday, unit="D")
    local = np.arange(len(positions))
    return [
        local[keys == k] for k in pd.unique(keys)
    ]


def run_cell(pnl, qmax, di_eval, di_fund, m=0.50 / 0.50, funded_only=False):
    """One (cell, partition, seed). m=1.0: the panel already carries WATCH-1.

    funded_only skips the eval sim — used by the §6(d) sensitivity pass, where
    all three pins (WIN_MIN / CAP_LO / PAYOUT_MIN) are consumed by funded_sim
    ONLY, so the eval leg is pin-independent and is reused from the main sweep.
    """
    ev = None
    if not funded_only:
        p, q = pnl[di_eval], qmax[di_eval]
        passed, bust, t_pass = G.eval_sim(p, q, m)
        ev = dict(
            pass_pct=float(passed.mean() * 100),
            bust_pct=float(bust.mean() * 100),
            med_days=float(np.nanmedian(t_pass)) if passed.any() else float("nan"),
        )
    p2, q2 = pnl[di_fund], qmax[di_fund]
    cash, npay, t_first, t_dead, alive = G.funded_sim(p2, q2, m, di_fund.shape[1])
    fu = dict(
        dead_1y=float((t_dead <= 260).mean() * 100),
        med_first_pay_bd=(float(np.nanmedian(t_first))
                          if np.isfinite(t_first).any() else float("nan")),
        no_payout_pct=float(np.isnan(t_first).mean() * 100),
        mean_cash=float(cash.mean()),
    )
    return ev, fu


def agg(rows: list[dict]) -> dict:
    return {k: {"mean": float(np.nanmean([r[k] for r in rows])),
                "sd": float(np.nanstd([r[k] for r in rows]))}
            for k in rows[0]}


def score(cand: dict, inc: dict, floor_on_noninferiority: bool) -> dict:
    """§4 D1-D5 on one half. Returns per-condition pass/fail + margins."""
    def mo(x):
        return x["eval"]["med_days"]["mean"] / BD_PER_MO + \
            x["funded"]["med_first_pay_bd"]["mean"] / BD_PER_MO

    def mo_sd(x):
        return math.hypot(x["eval"]["med_days"]["sd"],
                          x["funded"]["med_first_pay_bd"]["sd"]) / BD_PER_MO

    d1_margin = mo(inc) - mo(cand)
    d1_noise = max(mo_sd(cand), mo_sd(inc))
    d1 = (d1_margin >= D1_MIN_MONTHS) and (d1_margin >= d1_noise)

    c_cash, i_cash = cand["funded"]["mean_cash"], inc["funded"]["mean_cash"]
    d2_margin = c_cash["mean"] - i_cash["mean"]
    d2_noise = max(c_cash["sd"], i_cash["sd"])
    d2 = (i_cash["mean"] > 0 and d2_margin / i_cash["mean"] >= D2_MIN_REL
          and d2_margin >= d2_noise)

    c_p, i_p = cand["eval"]["pass_pct"], inc["eval"]["pass_pct"]
    d3_head = (c_p["mean"] - i_p["mean"]) + D3_MAX_PP_WORSE
    d3 = d3_head >= 0
    if floor_on_noninferiority:
        d3 = d3 and d3_head >= max(c_p["sd"], i_p["sd"])

    c_d, i_d = cand["funded"]["dead_1y"], inc["funded"]["dead_1y"]
    d4_head = (i_d["mean"] - c_d["mean"]) + D4_MAX_PP_WORSE
    d4 = d4_head >= 0
    if floor_on_noninferiority:
        d4 = d4 and d4_head >= max(c_d["sd"], i_d["sd"])

    d5 = cand["max_stack"] <= CAP_FIRM

    return {"D1": bool(d1), "D2": bool(d2), "D3": bool(d3), "D4": bool(d4),
            "D5": bool(d5), "all": bool(d1 and d2 and d3 and d4 and d5),
            "d1_margin_mo": d1_margin, "d1_noise_mo": d1_noise,
            "d2_margin_usd": d2_margin, "d2_noise_usd": d2_noise,
            "d2_rel": d2_margin / i_cash["mean"] if i_cash["mean"] else float("nan"),
            "d3_headroom_pp": d3_head, "d4_headroom_pp": d4_head}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true",
                    help="fast wiring check (tiny n_paths/horizon); NO verdict")
    # The three unverified venue pins (book-comp brief §0 ⚠). Defaults ARE the
    # modeled values, so an unflagged run is byte-identical to the 2026-07-27
    # run of record. These exist so the pre-committed re-run after dashboard
    # verification (RESULTS §5) needs no hand-edit of gap_stage2_capbound.py --
    # editing a committed harness by hand to change an input is how a "re-run at
    # corrected inputs" silently becomes an unlogged variant.
    ap.add_argument("--win-min", type=float, default=G.WIN_MIN,
                    help="funded winning-day minimum $ (modeled 200; UNVERIFIED)")
    # --cap-lo RETIRED 2026-07-29: funded scaling is a four-rung EOD ladder, not a
    # single low rung, so a scalar cannot express it (spec
    # docs/superpowers/specs/2026-07-29-funded-contract-scaling-4step-design.md).
    ap.add_argument("--funded-ladder", type=str, default="verified",
                    help='"verified" (30->40@101.5k->50@102k->80@103k), "legacy" '
                         '(the modeled binary 40->80), or an explicit '
                         '"thr:cap,thr:cap,..." ladder')
    ap.add_argument("--payout-min", type=float, default=0.0,
                    help="Flex minimum payout $ (VERIFIED 2026-07-29: none exists "
                         "for Flex, so default 0; the modeled 1000 was an assumption)")
    args = ap.parse_args()

    if args.funded_ladder == "verified":
        ladder = FS.ladder_for(100_000.0)
    elif args.funded_ladder == "legacy":
        ladder = FS.legacy_two_step()
    else:
        ladder = FS.parse_ladder_flag(args.funded_ladder)
    G.WIN_MIN, G.PAYOUT_MIN = args.win_min, args.payout_min
    G.FUNDED_LADDER = ladder
    pins = {"WIN_MIN": G.WIN_MIN, "FUNDED_LADDER": FS.describe(ladder),
            "PAYOUT_MIN": G.PAYOUT_MIN}
    # The 2026-07-27 run of record used the MODELED (now falsified) pins.
    modeled = {"WIN_MIN": 200.0, "FUNDED_LADDER": FS.describe(FS.legacy_two_step()),
               "PAYOUT_MIN": 1_000.0}
    verified = {"WIN_MIN": 200.0, "FUNDED_LADDER": FS.describe(FS.ladder_for(100_000.0)),
                "PAYOUT_MIN": 0.0}
    pin_note = ("MODELED (falsified 2026-07-29 — reproduces the 07-27 run of record)"
                if pins == modeled else
                "VERIFIED venue pins (2026-07-29)" if pins == verified else
                f"CUSTOM — neither the 07-27 record nor the verified set")
    print(f"[pins] {pins} — {pin_note}")

    n_paths = 300 if args.smoke else N_PATHS
    h_eval = 260 if args.smoke else H_EVAL
    h_fund = 260 if args.smoke else H_FUND

    idx = pd.read_csv(DAILY_PANEL, index_col=0, parse_dates=True).index
    cells = enumerate_cells()

    # --- CONTROL 3: candidate set matches the frozen §5 table -----------------
    frozen = [(1, 5, 15), (1, 6, 9), (2, 5, 17), (3, 4, 26), (4, 3, 37),
              (4, 4, 34), (5, 2, 48), (5, 3, 43), (6, 1, 59), (6, 2, 51),
              (7, 1, 60), (8, 1, 68)]
    got = [(c["res"][0], c["res"][1], c["cap_mym"]) for c in cells]
    assert got == frozen, f"candidate set drift\n frozen={frozen}\n got   ={got}"
    print(f"[control 3] candidate set reproduces the frozen 12 cells exactly")

    # --- build every cell's series -------------------------------------------
    series = {}
    for c in cells:
        pnl, q, net = cell_series(c["cap_mym"], c["cap_mnq"], idx)
        series[c["label"]] = {"pnl": pnl, "q": q, "net": net,
                              "max_stack": float(q.max())}
        assert q.max() <= CAP_FIRM, f"[control 4] {c['label']} breaches cap"
    print(f"[control 4] all 12 cells respect the {CAP_FIRM}-micro account cap")

    # --- CONTROL 2: live 69/11 == canonical 68/12 ----------------------------
    live_pnl, live_q, _ = cell_series(69, 11, idx)
    inc_label = next(c["label"] for c in cells if c["incumbent"])
    assert np.array_equal(live_pnl, series[inc_label]["pnl"]), "69/11 != 68/12"
    assert np.array_equal(live_q, series[inc_label]["q"]), "69/11 stack != 68/12"
    print(f"[control 2] live 69/11 produces series identical to canonical {inc_label}")

    # --- partitions (index-midpoint, per run_class_s_c1_regime_gate.py) ------
    n = len(idx)
    mid = n // 2
    parts = {"full": np.arange(n), "H1": np.arange(mid), "H2": np.arange(mid, n)}
    assert len(parts["H1"]) + len(parts["H2"]) == n, "[control 5] halves do not sum"
    print(f"[control 5] panel n={n} bdays; mid={mid}; "
          f"H1={len(parts['H1'])} ({idx[0].date()}..{idx[mid - 1].date()})  "
          f"H2={len(parts['H2'])} ({idx[mid].date()}..{idx[-1].date()})")

    # --- main sweep -----------------------------------------------------------
    results: dict = {}
    for pname, pos in parts.items():
        blocks = week_blocks(idx, pos)
        nb = len(blocks)
        per_seed: dict[str, list] = {c["label"]: [] for c in cells}
        for s in SEEDS:
            rng = np.random.default_rng(s)
            di_e = build_day_index(blocks, nb, n_paths, h_eval, rng)
            di_f = build_day_index(blocks, nb, n_paths, h_fund, rng)
            for c in cells:
                sc = series[c["label"]]
                ev, fu = run_cell(sc["pnl"][pos], sc["q"][pos], di_e, di_f)
                per_seed[c["label"]].append((ev, fu))
            print(f"  [{pname}] seed {s} done ({nb} week-blocks)", flush=True)
        for c in cells:
            rows = per_seed[c["label"]]
            results.setdefault(c["label"], {})[pname] = {
                "eval": agg([r[0] for r in rows]),
                "funded": agg([r[1] for r in rows]),
                "max_stack": series[c["label"]]["max_stack"],
                "net": series[c["label"]]["net"],
            }

    if args.smoke:
        print("\nSMOKE OK — wiring valid, no verdict emitted.")
        return 0

    # --- CONTROL 1: incumbent reproduction (§6 row c) ------------------------
    inc_full = results[inc_label]["full"]
    got_pins = {
        "eval_med_mo": inc_full["eval"]["med_days"]["mean"] / BD_PER_MO,
        "first_pay_mo": inc_full["funded"]["med_first_pay_bd"]["mean"] / BD_PER_MO,
        "mean_cash": inc_full["funded"]["mean_cash"]["mean"],
    }
    sds = {
        "eval_med_mo": inc_full["eval"]["med_days"]["sd"] / BD_PER_MO,
        "first_pay_mo": inc_full["funded"]["med_first_pay_bd"]["sd"] / BD_PER_MO,
        "mean_cash": inc_full["funded"]["mean_cash"]["sd"],
    }
    # CONTROL 1 IS PINS-CONDITIONAL (2026-07-29, operator-approved).
    #
    # Its job is DRIFT DETECTION, and drift is only measurable against a recorded
    # run of record -- which exists solely for the MODELED pins. Asserting the
    # modeled baselines against a corrected-pin run is incoherent: those funded
    # metrics MUST move, because moving them is the point of the correction.
    # (Observed 2026-07-29 under verified pins: first_pay_mo 5.5 -> 5.3, mean_cash
    # 32,904 -> 30,428, while the paired legacy arm reproduced all three exactly.)
    #
    # When pins == modeled the control ASSERTS as before AND publishes a sentinel.
    # When pins are overridden, drift is delegated to that paired legacy run -- and
    # this is NOT a free pass: the override path FAILS CLOSED unless a passing
    # sentinel exists. Drift can never be skipped, only relocated to the arm where
    # it is meaningful.
    drift_sentinel = _HERE / "_drift_check_legacy.json"
    is_record_pins = (pins == modeled)

    ctrl_ok = True
    print("\n[control 1] incumbent reproduction vs the 2026-07-27 session:")
    if is_record_pins:
        for k, want in CONTROL_PINS.items():
            tol = max(sds[k], 0.05 if k != "mean_cash" else 1.0)
            ok = abs(got_pins[k] - want) <= tol
            ctrl_ok &= ok
            print(f"    {k:14s} want {want:>10,.1f}  got {got_pins[k]:>10,.1f}  "
                  f"tol(1sd) {tol:>8,.1f}  {'OK' if ok else 'MISS'}")
        drift_sentinel.write_text(json.dumps({
            "drift_ok": bool(ctrl_ok), "pins": pins,
            "observed": got_pins, "control_pins": CONTROL_PINS,
        }, indent=2, default=float) + "\n", encoding="utf-8")
        print(f"    -> drift sentinel written ({'OK' if ctrl_ok else 'FAILED'})")
    else:
        print("    N/A - pins overridden; the modeled baselines do not apply.")
        for k in CONTROL_PINS:
            print(f"    {k:14s} observed {got_pins[k]:>10,.1f}  (recorded, not asserted)")
        if not drift_sentinel.is_file():
            ctrl_ok = False
            print("    MISS - no paired legacy drift check on disk. Run first:")
            print("           run_capalloc.py --funded-ladder legacy --payout-min 1000")
        elif not json.loads(drift_sentinel.read_text(encoding="utf-8")).get("drift_ok"):
            ctrl_ok = False
            print("    MISS - the paired legacy drift check FAILED; fix the harness first.")
        else:
            print("    OK   - drift delegated to the paired legacy run, which PASSED.")

    # --- §4 scoring on both halves -------------------------------------------
    verdicts = {}
    for strict in (False, True):
        key = "floor_on_D1D2_only" if not strict else "floor_on_all_four"
        winners = []
        detail = {}
        for c in cells:
            if c["incumbent"]:
                continue
            per_half = {
                h: score(results[c["label"]][h], results[inc_label][h], strict)
                for h in ("H1", "H2")
            }
            detail[c["label"]] = per_half
            if per_half["H1"]["all"] and per_half["H2"]["all"]:
                winners.append(c["label"])
        verdicts[key] = {"winners": winners, "detail": detail}

    w_base = verdicts["floor_on_D1D2_only"]["winners"]
    w_strict = verdicts["floor_on_all_four"]["winners"]

    if not ctrl_ok:
        verdict = ("AMBIGUOUS (c) — drift check unsatisfied (record-pin control MISS, "
                   "or an override run with no passing paired legacy run); NO VERDICT")
    elif w_base and w_strict:
        verdict = "RESOLVED-INCUMBENT-DOMINATED"
    elif not w_base and not w_strict:
        verdict = "FALSIFIED-INCUMBENT-STANDS"
    else:
        verdict = ("AMBIGUOUS (b) — verdict depends on the seed-noise reading "
                   "the frozen §4 left under-specified")

    # --- §6 row d: sensitivity on the three unverified rule pins -------------
    sens = {}
    if ctrl_ok:
        base = {"WIN_MIN": G.WIN_MIN, "FUNDED_LADDER": G.FUNDED_LADDER,
                "PAYOUT_MIN": G.PAYOUT_MIN}
        for pin, val in SENSITIVITY:
            # FUNDED_LADDER alternatives are named ("legacy"), not scalars.
            setattr(G, pin, FS.legacy_two_step() if val == "legacy" else val)
            alt = {}
            for pname in ("H1", "H2"):
                pos = parts[pname]
                blocks = week_blocks(idx, pos)
                nb = len(blocks)
                rows = {c["label"]: [] for c in cells}
                for s in SEEDS:
                    rng = np.random.default_rng(s)
                    build_day_index(blocks, nb, n_paths, h_eval, rng)  # order
                    di_f = build_day_index(blocks, nb, n_paths, h_fund, rng)
                    for c in cells:
                        sc = series[c["label"]]
                        _, fu = run_cell(sc["pnl"][pos], sc["q"][pos], None, di_f,
                                         funded_only=True)
                        rows[c["label"]].append(fu)
                for c in cells:
                    alt.setdefault(c["label"], {})[pname] = {
                        "eval": results[c["label"]][pname]["eval"],   # pin-independent
                        "funded": agg(rows[c["label"]]),
                        "max_stack": series[c["label"]]["max_stack"],
                    }
            w = [c["label"] for c in cells if not c["incumbent"]
                 and score(alt[c["label"]]["H1"], alt[inc_label]["H1"], False)["all"]
                 and score(alt[c["label"]]["H2"], alt[inc_label]["H2"], False)["all"]]
            sens[f"{pin}={val:g}" if not isinstance(val, str) else f"{pin}={val}"] = w
            print(f"  [sensitivity] {pin}={val if isinstance(val, str) else format(val, 'g')}"
                  f" -> winners {w or '(none)'}", flush=True)
            setattr(G, pin, base[pin])

    flips = [k for k, v in sens.items() if bool(v) != bool(w_base)]
    if flips and verdict.startswith(("RESOLVED", "FALSIFIED")):
        verdict = (f"AMBIGUOUS (d) — verdict flips under unverified rule pin(s): "
                   f"{', '.join(flips)}")

    out = {
        "pre_registration": PREREG, "pre_registration_commit": PREREG_COMMIT,
        "date": "2026-07-27", "incumbent_cell": inc_label,
        "rule_pins": {"used": pins, "modeled": modeled,
                      "is_run_of_record": pins == modeled,
                      "verified_in_dashboard": False},
        "controls": {"candidate_set": True, "cap_invariant": True,
                     "split_identity": True, "incumbent_reproduction": ctrl_ok,
                     "reproduction_detail": {k: {"want": CONTROL_PINS[k],
                                                 "got": got_pins[k],
                                                 "sd": sds[k]} for k in CONTROL_PINS}},
        "partition": {"n_bdays": n, "mid_index": mid,
                      "h1": [str(idx[0].date()), str(idx[mid - 1].date())],
                      "h2": [str(idx[mid].date()), str(idx[-1].date())]},
        "cells": [{**c, "max_stack": series[c["label"]]["max_stack"],
                   "net": series[c["label"]]["net"]} for c in cells],
        "results": results, "scoring": verdicts, "sensitivity": sens,
        "verdict": verdict,
    }
    (_HERE / "measured.json").write_text(
        json.dumps(out, indent=2, default=float) + "\n", encoding="utf-8")

    # --- console summary ------------------------------------------------------
    print(f"\n{'cell':>8} {'res':>5} {'net':>10} | "
          f"{'H1 eval/pay/cash':>26} | {'H2 eval/pay/cash':>26}")
    for c in cells:
        r = results[c["label"]]
        row = f"{c['label']:>8} {c['res_label']:>5} {series[c['label']]['net']:>10,.0f} |"
        for h in ("H1", "H2"):
            row += (f" {r[h]['eval']['med_days']['mean'] / BD_PER_MO:>6.1f}"
                    f" {r[h]['funded']['med_first_pay_bd']['mean'] / BD_PER_MO:>6.1f}"
                    f" {r[h]['funded']['mean_cash']['mean']:>11,.0f} |")
        print(row + ("  <- INCUMBENT" if c["incumbent"] else ""))
    print(f"\nwinners (floor on D1/D2 only): {w_base or '(none)'}")
    print(f"winners (floor on all four)  : {w_strict or '(none)'}")
    print(f"\nVERDICT: {verdict}")
    print(f"saved -> {_HERE / 'measured.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
