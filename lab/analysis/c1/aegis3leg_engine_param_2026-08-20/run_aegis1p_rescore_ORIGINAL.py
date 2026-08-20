"""Aegis@1.00% 3-leg corrected-geometry re-MC (2026-07-27) — GEOMETRY question only.

Pre-registration (FROZEN 2026-07-27, operator directive "Run the fresh
pre-registered Aegis @ 1% test on corrected geometry"):
  docs/briefs/pre-registration/2026-07-27-aegis-1p-3leg-corrected-geometry-prereg.md

Book: Striker->MYM 0.70% + Striker->MNQ 0.37% (byte-pinned 15d8b/beabf) +
Aegis->6J @ 1.00% (fresh native-1% export ac331, 1R pin $2,163.57/n7 frozen
pre-run in inventory_aegis1p.json).

Cells (all corrected geometry, dd_lock_offset_usd -> 1_000_000.0, restored after):
  controls  : 2-leg full panel at T-100K/T-50K/MFFU-50K vs pins 4.74%/1.06%/0.96% (+/-0.15pp)
  gating    : 3-leg full panel at the same three tiers (floor bust<=3.0% AND pass>=50%)
  diagnostic: 3-leg H1/H2 halves; COST-TRUE full panel (Aegis leg -$3.60/RT/contract);
              bootstrap (n=100, block 126bd, seed 20260715) ONLY on full-panel passers.

Cap-feasibility is pre-declared FAIL on every cell (6J = 10 micro-equivalents;
no M6J at any FRIENDLY firm) — no outcome here can be a "clearer" claim.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[3]
_SCORING = _ROOT / "lab" / "analysis" / "c1" / "class_s_candidate1_scoring_2026-07-15"
_RECONCILE = _ROOT / ".claude" / "skills" / "trade-csv-reconcile" / "scripts"
for _p in (_ROOT / "core", _ROOT / "lab", str(_SCORING), str(_RECONCILE)):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import firm_rules  # noqa: E402
from discovery.prop_survivor_scoring import load_scoring_thresholds  # noqa: E402
from reconcile import load_csv  # noqa: E402

_ARGS = [a for a in sys.argv[1:]]
sys.argv = [sys.argv[0]]
import run_class_s_c1_scoring as S  # noqa: E402
import run_class_s_c1_regime_gate as R  # noqa: E402

PREREG = "docs/briefs/pre-registration/2026-07-27-aegis-1p-3leg-corrected-geometry-prereg.md"
AEGIS_LEG = "aegis_1p"
AEGIS_FILE = "Aegis_6J1_CME_6J1!_2026-07-27_ac331.csv"
AEGIS_SHA = "cbf57ac29a26bcfba2efed62fc3a30ab9309c4f51802e9765557d05b5e1e848f"
AEGIS_EXPECT_1R = {"dollars": 2163.57, "n": 7, "scale": 0.924398}
AEGIS_RISK = 0.0100
COST_TRUE_RT_DELTA = 3.60  # (3.10 - 1.30) x 2 per contract round trip (Tradeify 6J)

TIERS = ("Tradeify_Select_100K", "Tradeify_Select_50K", "MFFU_Rapid_50K")
CONTROL_PINS = {
    "Tradeify_Select_100K": 0.0474,
    "Tradeify_Select_50K": 0.0106,
    "MFFU_Rapid_50K": 0.0096,
}
CONTROL_TOL = 0.0015
UNREACHABLE = 1_000_000.0
NOISE_BAND_HI = 0.032

STRATS_3 = ("striker", "striker_nas100", AEGIS_LEG)
ALLOCS_3 = {"striker": 0.0070, "striker_nas100": 0.0037, AEGIS_LEG: AEGIS_RISK}

SMOKE = "--smoke" in _ARGS
N_SIMS = 200 if SMOKE else None  # None = frozen 10K/seed
N_PANELS = 5 if SMOKE else 100


def _tier_daily(panel: pd.DataFrame, tier: str) -> np.ndarray:
    bal = float(firm_rules.FIRM_RULES[tier]["starting_balance"])
    return (panel.sum(axis=1) * (bal / S.ACCOUNT)).to_numpy(dtype=float)


def _cell(daily: np.ndarray, tier: str, thr) -> dict:
    r = R.run_partition_mc(daily, tier, thr, n_sims=N_SIMS)
    r["floor_ok"] = bool(
        r["headline_bust"] <= thr.eval_bust_ceiling and r["pass_rate"] >= thr.pass_floor
    )
    return r


def build_cost_true_aegis_daily(scale: float) -> pd.Series:
    """Aegis leg daily P&L at $200K static with the Tradeify 6J commission delta
    applied per trade (diagnostic; same frozen scale, no re-pin)."""
    df = load_csv(_HERE / "inputs" / AEGIS_FILE)
    exits = df[df["Type"].astype(str).str.startswith("Exit")].sort_values("dt")
    trades = S.pair_trades(df)
    qty = (
        exits.groupby("Trade #")["Size (qty)"].max().astype(float)
    )
    t = S.reconstruct_static(trades, S.detect_initial(exits))
    t["qty"] = t["trade_no"].map(qty)
    assert t["qty"].notna().all(), "qty join failed"
    t["pnl_adj"] = t["net_pnl"] - COST_TRUE_RT_DELTA * t["qty"]
    t["pnl_static_adj"] = (t["pnl_adj"] / t["equity_before"]) * S.ACCOUNT
    t["pnl_scaled"] = t["pnl_static_adj"] * scale
    return (
        t.assign(d=t["exit_dt"].dt.normalize()).groupby("d")["pnl_scaled"].sum()
    )


def main() -> int:
    S.phase0_verify()
    # Register the fresh Aegis leg beside the frozen harness (runtime only).
    S.PANEL_FILES[AEGIS_LEG] = (AEGIS_FILE, AEGIS_SHA)
    for leg in STRATS_3:
        S.resolve_panel_path(leg)

    thr = load_scoring_thresholds(S.GATE_PREREG)
    expect3 = dict(S.EXPECTED_1R)
    expect3[AEGIS_LEG] = AEGIS_EXPECT_1R

    panel2, meta2, _ = S.build_scaled_panel(S.C1_STRATS, S.C1_ALLOCS, expect_1r=dict(S.EXPECTED_1R))
    panel3, meta3, _ = S.build_scaled_panel(STRATS_3, ALLOCS_3, expect_1r=expect3)
    aegis_scale = meta3["legs"][AEGIS_LEG]["scale"]

    # COST-TRUE variant panel: swap the Aegis column only.
    aegis_ct = build_cost_true_aegis_daily(aegis_scale)
    panel_ct = panel3.copy()
    ct = aegis_ct.reindex(panel_ct.index).fillna(0.0)
    panel_ct[AEGIS_LEG] = ct

    print(
        f"[a1p] 2-leg {meta2['panel_span']} n={meta2['n_bdays']} | "
        f"3-leg {meta3['panel_span']} n={meta3['n_bdays']} "
        f"aegis_scale={aegis_scale:.6f} smoke={SMOKE}",
        flush=True,
    )

    out: dict = {
        "date": "2026-07-27",
        "pre_reg": PREREG,
        "smoke": SMOKE,
        "geometry": "CORRECTED (dd_lock_offset_usd unreachable)",
        "floor": {"bust_ceiling": thr.eval_bust_ceiling, "pass_floor": thr.pass_floor},
        "panel_meta_2leg": meta2,
        "panel_meta_3leg": meta3,
        "cap_predeclared": "INFEASIBLE all cells (6J=10 micro-equiv; no M6J at FRIENDLY firms)",
        "controls": {},
        "gating": {},
        "halves": {},
        "cost_true": {},
        "bootstrap": {},
    }

    for t in TIERS:
        firm_rules.FIRM_RULES[t]["dd_lock_offset_usd"] = UNREACHABLE
    print(f"[a1p] patch: lock unreachable on {TIERS}", flush=True)

    try:
        controls_ok = True
        for tier in TIERS:
            t0 = time.time()
            r = _cell(_tier_daily(panel2, tier), tier, thr)
            ok = abs(r["headline_bust"] - CONTROL_PINS[tier]) <= CONTROL_TOL
            controls_ok = controls_ok and ok
            out["controls"][tier] = {
                **r, "pin": CONTROL_PINS[tier], "pin_ok": ok,
                "wall_s": round(time.time() - t0, 1),
            }
            print(
                f"[a1p] CONTROL {tier:22s} bust={r['headline_bust']:6.2%} "
                f"vs pin {CONTROL_PINS[tier]:.2%} -> {'MATCH' if ok else 'MISMATCH'}",
                flush=True,
            )

        for tier in TIERS:
            t0 = time.time()
            r = _cell(_tier_daily(panel3, tier), tier, thr)
            out["gating"][tier] = {
                **r,
                "noise_band": bool(thr.eval_bust_ceiling < r["headline_bust"] <= NOISE_BAND_HI),
                "wall_s": round(time.time() - t0, 1),
            }
            print(
                f"[a1p] 3LEG    {tier:22s} bust={r['headline_bust']:6.2%} "
                f"pass={r['pass_rate']:6.2%} floor={'PASS' if r['floor_ok'] else 'FAIL'}",
                flush=True,
            )

        daily3 = {t: _tier_daily(panel3, t) for t in TIERS}
        for tier in TIERS:
            h1, h2, mid = R.half_panel_split(daily3[tier])
            r1 = _cell(h1, tier, thr)
            r2 = _cell(h2, tier, thr)
            out["halves"][tier] = {"mid": mid, "H1": r1, "H2": r2}
            print(
                f"[a1p] HALVES  {tier:22s} H1 bust={r1['headline_bust']:6.2%} "
                f"{'PASS' if r1['floor_ok'] else 'FAIL'} | H2 bust={r2['headline_bust']:6.2%} "
                f"{'PASS' if r2['floor_ok'] else 'FAIL'}",
                flush=True,
            )

        for tier in TIERS:
            r = _cell(_tier_daily(panel_ct, tier), tier, thr)
            out["cost_true"][tier] = r
            print(
                f"[a1p] COSTTRUE {tier:21s} bust={r['headline_bust']:6.2%} "
                f"floor={'PASS' if r['floor_ok'] else 'FAIL'}",
                flush=True,
            )

        passers = [t for t in TIERS if out["gating"][t]["floor_ok"]]
        for tier in passers:
            b = R.part_a_bootstrap(
                daily3[tier], thr, n_panels=N_PANELS, n_sims=N_SIMS, tiers=(tier,),
            )
            bt = b["tiers"][tier]
            out["bootstrap"][tier] = {
                k: v for k, v in bt.items() if k != "panels"
            }
    finally:
        # 2026-08-07 W1: restore-to-100 RETIRED (08-04 default is UNREACHABLE).
        # docs/adr/2026-08-07-w1-intraday-honest-engine-remeasure.md
        for t in TIERS:
            firm_rules.FIRM_RULES[t]["dd_lock_offset_usd"] = UNREACHABLE

    noise = [t for t in TIERS if out["gating"][t]["noise_band"]]
    if not controls_ok:
        verdict = "AMBIGUOUS (control mismatch - harness defect, no verdict)"
    elif SMOKE:
        verdict = "SMOKE (wiring only - not read against §6)"
    elif [t for t in TIERS if out["gating"][t]["floor_ok"]]:
        verdict = "GEOMETRY-PASS (feasibility-blocked)"
    elif noise:
        verdict = "AMBIGUOUS (noise-band: " + ", ".join(noise) + ")"
    else:
        verdict = "GEOMETRY-FAIL"
    out["verdict"] = verdict

    dest = _HERE / ("smoke_report.json" if SMOKE else "aegis1p_report.json")
    dest.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"\n[a1p] VERDICT: {verdict}", flush=True)
    print(f"[written] {dest}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
