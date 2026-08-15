"""Q-COMPOSE-1 — composed-book (2-leg Class-S c1 + ORB-MNQ-1 @0.37%) regime-breadth re-MC.

Pre-reg (FROZEN 2026-07-16, operator-signed §9):
  docs/briefs/pre-registration/Q-COMPOSE-1-verdict-preregistration.md
Parent Pre-Q: docs/briefs/Q-COMPOSE-1-orb-classs-book-regime-breadth.md
Gate of record (cited, not re-decided): docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md

Book (§2, FIXED): MYM-Striker @0.70% + MNQ-Striker @0.37% (byte-pinned from candidate #1,
not re-weighted) + ORB-MNQ-1 @0.37% (SINGLE frozen weight; not a sweep). ORB at neutral
1.00x lifecycle; the 2-leg sub-book runs UN-haircut (the 0.50x/0.25x arms belong to the
sibling haircut pre-reg and are forbidden from being folded in — §5 / Trap #11).

Phase-0 injection-shape determination (pre-reg §2 / §8 Phase 0):
  `build_scaled_panel` itself cannot ingest ORB — it is TV-export-CSV-specific (sha-pinned
  PANEL_FILES; §8.3 full-stop 1R guard) and ORB's R is definitionally OR-range-normalized
  (no fill-derived full-stop cohort exists, by construction not by defect). The pre-reg's
  own clause is a disjunction — "into `build_scaled_panel` / book-daily construction" —
  and this driver takes the book-daily-construction site with ZERO edits to any frozen
  primitive: the 2-leg panel is built by the untouched frozen `build_scaled_panel`
  (EXPECTED_1R guards intact), ORB daily R converts to USD at the allocation layer
  (R x 0.0037 x 200_000, the same arithmetic as Stage-8's committed precedent in
  `run_stage8_neff.py`, which pre-reg §0 itself cites as the ORB-series ground), the ORB
  column is reindexed onto the 2-leg panel's frozen business-day index (fillna 0.0 = flat
  no-trade days, the same treatment the book legs receive), and only THEN does
  `book_daily_at_100k(panel3)` collapse the composed panel. The Run-2 consistency clause
  (`core/mc/simulation.py` L119-124: `max_day_profit - consistency_frac * total_profit`)
  therefore operates on the TRUE composed daily series — exactly what §2's
  "NOT post-hoc on `daily_100k`" protects. NEEDS_CONTEXT would fire only under a
  strict-literal "inside build_scaled_panel" reading, which is impossible without a
  forbidden workaround (synthetic CSV or 1R-guard bypass); the disjunction reading is
  ratified in the Phase-0 report this driver prints and PHASE0.md records.

Engine-faithfulness: the ORB daily series is produced by `run_stage8_neff.orb_daily_dated`
and asserted R-multiset-identical to `orb_lib.orb_backtest` before use (same self-check as
Stage-8). The frozen 2-leg H1/H2 midpoint and bootstrap parameters are inherited by
construction: the composed panel keeps the 2-leg panel's OWN index (2020-01-06 ->
2026-06-30, 1692 bdays), so partitions are identical to the c1 rider; ORB's data span
(2019-05-06 -> 2026-07-15) fully covers it (no out-of-window zero-fill arises), and ORB
enters H1 with its 2020 death intact (§5).

median_days_to_pass (§2 diagnostic) is NOT surfaced by `summarize_outcomes`; pass_rate is
reported as the practicality proxy (same documented non-gating Phase-0 deviation as the
haircut sibling).

Reproduction control: not mandated by the compose pre-reg. The frozen 2-leg baseline
(REGIME_GATE.md @163b0b5) was exactly reproduced by the haircut sibling's 1.00x control on
this same machine/venv on 2026-07-17; this driver cites those frozen numbers instead of
re-running the ~2h control.

Exit codes: 0 = completed (any verdict); 2 = NEEDS_CONTEXT; 3 = Phase-0 failure.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[2]
_SCORING = _ROOT / "lab" / "analysis" / "class_s_candidate1_scoring_2026-07-15"
_ORB = _ROOT / "lab" / "analysis" / "orb_mnq_2026-07"
_ORBLIB = _ROOT / "lab" / "analysis" / "orb_universe_2026-06-22"
for _p in (_ROOT / "core", _ROOT / "lab", _SCORING, _ORB, _ORBLIB, _HERE):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from firm_rules import FIRM_RULES  # noqa: E402
from discovery.prop_survivor_scoring import load_scoring_thresholds  # noqa: E402
import run_class_s_c1_scoring as S  # noqa: E402  (frozen panel build + phase0)
import run_class_s_c1_regime_gate as R  # noqa: E402  (frozen regime primitives)
import orb_lib as ol  # noqa: E402
from run_stage2 import load_mnq_15m, MNQ  # noqa: E402
from run_stage8_neff import orb_daily_dated, weekly  # noqa: E402
from research_utils.breadth import (  # noqa: E402
    effective_number_of_bets,
    participation_ratio,
)

# §2 frozen composition — the SOLE new frozen input is ORB @ 0.37% (operator §9).
ORB_ALLOC = 0.0037
ACCOUNT = 200_000.0
ORB_COL = "orb_mnq"

PREREG = (
    "docs/briefs/pre-registration/Q-COMPOSE-1-verdict-preregistration.md"
)

# Frozen 2-leg baseline (REGIME_GATE.md @163b0b5) — cited for the delta table; the
# haircut sibling's 1.00x control reproduced these on this machine/venv 2026-07-17.
BASELINE_2LEG = {
    "Tradeify_Select_100K": {"H1_bust": 0.0437, "boot_bust_95th": 0.1037},
    "MFFU_Rapid_100K": {"H1_bust": 0.0436, "boot_bust_95th": 0.1033},
}

# Machine-local databento DBN cache backing the ORB series (integrity record, not a gate —
# no pre-registered hash exists; the engine-faithfulness gate is the R-multiset assert).
DBN_PATH = (
    Path.home() / ".databento_cache" / "ohlcv-1m_continuous_ce119c1e8f923316.dbn"
)


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def build_orb_usd_column(panel_index: pd.DatetimeIndex) -> tuple[pd.Series, dict]:
    """ORB daily R (engine-faithful, self-checked) -> USD at the §2 allocation layer."""
    df = load_mnq_15m()
    piv, meta = ol.session_panel(df, MNQ)
    dates, r_arr = orb_daily_dated(piv, meta)
    bt = ol.orb_backtest(piv, meta, MNQ, or_bars=2)
    engine_r = np.asarray(bt["R"], float)
    engine_r = engine_r[np.isfinite(engine_r)]
    if not (len(r_arr) == len(engine_r) and np.allclose(np.sort(r_arr), np.sort(engine_r))):
        raise S.NeedsContext(
            "ORB dated series diverges from orb_lib.orb_backtest R multiset — "
            "engine-faithfulness assert failed; do not improvise."
        )
    orb_r = pd.Series(r_arr, index=dates).groupby(level=0).sum()
    orb_usd = orb_r * ORB_ALLOC * ACCOUNT
    in_window = orb_usd.index.isin(panel_index)
    col = orb_usd.reindex(panel_index).fillna(0.0).rename(ORB_COL)
    diag = {
        "n_orb_trade_days": int(orb_usd.size),
        "orb_span": f"{orb_usd.index.min().date()}->{orb_usd.index.max().date()}",
        "n_inside_panel_window": int(in_window.sum()),
        "n_dropped_outside_window": int((~in_window).sum()),
        "orb_alloc": ORB_ALLOC,
        "account_basis": ACCOUNT,
        "usd_per_R": ORB_ALLOC * ACCOUNT,
        "net_usd_in_window": float(col.sum()),
        "self_check": "R multiset identical to orb_lib.orb_backtest",
        "dbn_cache": {
            "path": str(DBN_PATH),
            "sha256": _sha256(DBN_PATH) if DBN_PATH.is_file() else None,
        },
    }
    return col, diag


def compose_verdict_4tier(full: dict, half: dict, boot: dict, thr) -> dict:
    """§4/§6 tri-state over all four frozen tiers.

    RESOLVED       — full ∧ H1 ∧ H2 ∧ bootstrap clear on >=2 tiers incl >=1 trailing_locking.
    FALSIFIED      — H1 bust > ceiling OR bootstrap-95th > ceiling on EVERY tier.
    AMBIGUOUS-HOLD — all-four clear on exactly 1 tier, or any outcome shape not
                     pre-committed as pass/fail (never silently mapped to a verdict).
    """
    tiers: dict = {}
    for fk in thr.tier_keys:
        f = full[fk]
        h = half["tiers"][fk]
        b = boot["tiers"][fk]
        all_four = bool(
            f["floor_ok"] and h["H1"]["floor_ok"] and h["H2"]["floor_ok"] and b["bootstrap_ok"]
        )
        falsified_limb = bool(
            float(h["H1"]["headline_bust"]) > thr.eval_bust_ceiling
            or float(b["bust_95th"]) > thr.eval_bust_ceiling
        )
        tiers[fk] = {
            "dd_type": FIRM_RULES[fk].get("dd_type"),
            "full_panel_ok": f["floor_ok"],
            "H1_ok": h["H1"]["floor_ok"],
            "H2_ok": h["H2"]["floor_ok"],
            "bootstrap_ok": b["bootstrap_ok"],
            "all_four_clear": all_four,
            "falsified_limb": falsified_limb,
            "full": f,
            "half": h,
            "bootstrap_summary": {
                "pass_5th": b["pass_5th"],
                "pass_mean": b["pass_mean"],
                "bust_95th": b["bust_95th"],
                "bust_mean": b["bust_mean"],
            },
        }
    clearers = [fk for fk in thr.tier_keys if tiers[fk]["all_four_clear"]]
    locking_clearers = [
        fk for fk in clearers if FIRM_RULES[fk].get("dd_type") == "trailing_locking"
    ]
    if len(clearers) >= 2 and locking_clearers:
        verdict, reason = "RESOLVED", (
            f"all four partitions clear on {clearers} incl trailing_locking "
            f"{locking_clearers} at ORB @ {ORB_ALLOC:.2%}"
        )
    elif all(tiers[fk]["falsified_limb"] for fk in thr.tier_keys):
        verdict, reason = "FALSIFIED", (
            "H1 bust > ceiling OR bootstrap-95th > ceiling on EVERY tier at the "
            "frozen weight — breadth does not rescue regime-fragility"
        )
    elif len(clearers) == 1:
        verdict, reason = "AMBIGUOUS-HOLD", (
            f"all-four clear on exactly 1 tier ({clearers[0]}) — §6 pre-committed "
            "AMBIGUOUS limb; fresh pre-reg required, re-test rides 2026-08-08"
        )
    else:
        verdict, reason = "AMBIGUOUS-HOLD", (
            f"outcome shape not pre-committed as pass/fail (clearers={clearers}, "
            f"trailing_locking clearers={locking_clearers}, "
            f"falsified_limb per tier="
            f"{ {fk: tiers[fk]['falsified_limb'] for fk in thr.tier_keys} }) — "
            "routes to AMBIGUOUS-HOLD, never silently to a verdict"
        )
    return {
        "floor_bust": thr.eval_bust_ceiling,
        "floor_pass": thr.pass_floor,
        "orb_weight": ORB_ALLOC,
        "clearers": clearers,
        "trailing_locking_clearers": locking_clearers,
        "verdict": verdict,
        "reason": reason,
        "tiers": tiers,
    }


def breadth_declaration(panel3: pd.DataFrame) -> dict:
    """§2-required 3-leg breadth declaration (weekly Mon-anchored frame).

    Correlation is scale-invariant, so the USD panel gives the same dependence
    N_eff as Stage-8's R-column variant; cov uses the same all-USD frame as Stage-8.
    """
    legs2 = [c for c in panel3.columns if c != ORB_COL]
    wk = weekly(panel3)
    m2 = wk[legs2].to_numpy()
    m3 = wk[legs2 + [ORB_COL]].to_numpy()
    out = {}
    for label, m in (("2leg", m2), ("3leg", m3)):
        corr = np.corrcoef(m, rowvar=False)
        cov = np.cov(m, rowvar=False)
        out[label] = {
            "dependence_neff_pr_corr": float(participation_ratio(corr)),
            "risk_neff_pr_cov": float(participation_ratio(cov)),
            "enb": float(effective_number_of_bets(corr)),
        }
    out["n_weeks"] = int(len(wk))
    out["delta_dependence"] = (
        out["3leg"]["dependence_neff_pr_corr"] - out["2leg"]["dependence_neff_pr_corr"]
    )
    out["delta_risk"] = out["3leg"]["risk_neff_pr_cov"] - out["2leg"]["risk_neff_pr_cov"]
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--smoke", action="store_true", help="n_panels=5, n_sims=200 wiring check")
    ap.add_argument("--n-panels", type=int, default=None)
    ap.add_argument("--n-sims", type=int, default=None)
    ap.add_argument("--n-jobs", type=int, default=-1)
    ap.add_argument("--out-dir", type=Path, default=_HERE)
    args = ap.parse_args(argv)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    n_sims = 200 if (args.smoke and args.n_sims is None) else args.n_sims
    n_panels = (5 if args.smoke else 100) if args.n_panels is None else args.n_panels

    # ---- Phase 0 (pre-reg §8): anchors + injection shape + composed-series faithfulness.
    try:
        S.phase0_verify()
        for leg in S.C1_STRATS:
            S.resolve_panel_path(leg)
    except S.Phase0Error as e:
        print(f"[compose] PHASE0_FAIL: {e}", file=sys.stderr)
        return 3
    except S.NeedsContext as e:
        print(f"[compose] NEEDS_CONTEXT: {e}", file=sys.stderr)
        return 2

    thr = load_scoring_thresholds(S.GATE_PREREG)
    all_tiers = tuple(thr.tier_keys)

    try:
        panel2, meta2, _trades = S.build_scaled_panel(
            S.C1_STRATS, S.C1_ALLOCS, expect_1r=dict(S.EXPECTED_1R)
        )
        orb_col, orb_diag = build_orb_usd_column(panel2.index)
    except S.NeedsContext as e:
        print(f"[compose] NEEDS_CONTEXT: {e}", file=sys.stderr)
        return 2

    panel3 = pd.concat([panel2, orb_col], axis=1)
    assert list(panel3.columns) == list(S.C1_STRATS) + [ORB_COL]
    assert panel3.index.equals(panel2.index) and len(panel3) == meta2["n_bdays"]
    daily = S.book_daily_at_100k(panel3)

    print(
        f"[compose] PHASE-0 CONFIRMED: injection = book-daily construction (pre-reg §2 "
        f"disjunction; Stage-8 precedent). 2-leg panel {meta2['panel_span']} "
        f"n_bdays={meta2['n_bdays']} via frozen build_scaled_panel (guards intact); "
        f"ORB column R x {ORB_ALLOC} x {ACCOUNT:.0f} reindexed onto the frozen index "
        f"({orb_diag['n_inside_panel_window']} trade days in-window, "
        f"{orb_diag['n_dropped_outside_window']} dropped outside); "
        f"book_daily_at_100k on the composed 3-col panel -> Run-2 consistency clause "
        f"sees the true composed series. NOT post-hoc on daily_100k.",
        flush=True,
    )
    print(
        f"[compose] floor(bust<={thr.eval_bust_ceiling:.1%}, pass>={thr.pass_floor:.0%}) "
        f"tiers={list(all_tiers)} n_sims={n_sims or thr.sims_per_seed} "
        f"n_panels={n_panels} smoke={args.smoke}",
        flush=True,
    )

    # ---- Phase 1: full/H1/H2 (cheap cells first — early H1 signal), then bootstrap per tier.
    t0 = time.time()
    full = R.full_panel_reference(daily, thr, n_sims=n_sims, tiers=all_tiers)
    half = R.part_b_half_panel(daily, thr, n_sims=n_sims, tiers=all_tiers)
    (args.out_dir / "partitions_full_half.json").write_text(
        json.dumps({"full": full, "half": half}, indent=2) + "\n", encoding="utf-8"
    )
    boot: dict = {
        "n_panels": int(n_panels),
        "block_size_bdays": R.BLOCK_SIZE_BDAYS,
        "boot_seed": R.BOOT_SEED,
        "tiers": {},
    }
    for fk in all_tiers:
        b1 = R.part_a_bootstrap(
            daily, thr, n_panels=n_panels, n_sims=n_sims,
            n_jobs=args.n_jobs, tiers=(fk,),
        )
        boot["tiers"][fk] = b1["tiers"][fk]
        (args.out_dir / f"boot_{fk}.json").write_text(
            json.dumps(
                {k: v for k, v in b1["tiers"][fk].items() if k != "panels"},
                indent=2,
            ) + "\n",
            encoding="utf-8",
        )

    # ---- Phase 2 inputs: verdict + breadth declaration.
    verdict = compose_verdict_4tier(full, half, boot, thr)
    breadth = breadth_declaration(panel3)

    report = {
        "pre_reg": PREREG,
        "parent_pre_q": "docs/briefs/Q-COMPOSE-1-orb-classs-book-regime-breadth.md",
        "gate_prereg": str(S.GATE_PREREG.relative_to(_ROOT)).replace("\\", "/"),
        "candidate_prereg": str(S.CANDIDATE_PREREG.relative_to(_ROOT)).replace("\\", "/"),
        "book": {
            "legs": {**{k: S.C1_ALLOCS[k] for k in S.C1_STRATS}, ORB_COL: ORB_ALLOC},
            "orb_lifecycle_mult": 1.00,
            "sub_book_haircut": "NONE (haircut arms forbidden here — sibling pre-reg)",
        },
        "n_sims": n_sims or thr.sims_per_seed,
        "n_panels": n_panels,
        "smoke": bool(args.smoke),
        "floor": {"bust_ceiling": thr.eval_bust_ceiling, "pass_floor": thr.pass_floor},
        "panel_meta": meta2,
        "orb_series": orb_diag,
        "baseline_2leg_cited": BASELINE_2LEG,
        "reproduction_control": (
            "skipped — not mandated by the compose pre-reg; frozen 2-leg baseline "
            "(REGIME_GATE.md @163b0b5) reproduced by the haircut sibling's 1.00x "
            "control on this machine/venv 2026-07-17"
        ),
        "median_days_note": (
            "median_days_to_pass not surfaced by summarize_outcomes; pass_rate reported "
            "as the practicality proxy (non-gating deviation, same as haircut sibling)."
        ),
        "breadth_declaration": breadth,
        "verdict": verdict,
        "wall_s": round(time.time() - t0, 1),
    }
    (args.out_dir / "compose_remc_report.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )

    print(f"[compose] ===== VERDICT {verdict['verdict']} =====", flush=True)
    print(f"[compose] reason: {verdict['reason']}", flush=True)
    for fk in all_tiers:
        t = verdict["tiers"][fk]
        bs = t["bootstrap_summary"]
        base = BASELINE_2LEG.get(fk)
        delta = (
            f" (2-leg H1 {base['H1_bust']:.2%} boot95 {base['boot_bust_95th']:.2%})"
            if base
            else ""
        )
        print(
            f"[compose]   {fk} [{t['dd_type']}]: "
            f"full {t['full']['headline_bust']:.2%}/{t['full']['pass_rate']:.1%} "
            f"| H1 {t['half']['H1']['headline_bust']:.2%}/{t['half']['H1']['pass_rate']:.1%} "
            f"| H2 {t['half']['H2']['headline_bust']:.2%} "
            f"| boot95 {bs['bust_95th']:.2%} pass5 {bs['pass_5th']:.1%} "
            f"-> all_four={'YES' if t['all_four_clear'] else 'no'}{delta}",
            flush=True,
        )
    b2, b3 = breadth["2leg"], breadth["3leg"]
    print(
        f"[compose] breadth (weekly, n={breadth['n_weeks']}): dependence N_eff "
        f"{b2['dependence_neff_pr_corr']:.4f} -> {b3['dependence_neff_pr_corr']:.4f} "
        f"({breadth['delta_dependence']:+.4f}); risk N_eff "
        f"{b2['risk_neff_pr_cov']:.4f} -> {b3['risk_neff_pr_cov']:.4f} "
        f"({breadth['delta_risk']:+.4f})",
        flush=True,
    )
    print(f"[compose] DONE wall={report['wall_s']:.0f}s -> compose_remc_report.json", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
