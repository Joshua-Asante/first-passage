"""Corrected-geometry haircut arms — full-panel + half-panel reference (2026-07-24).

Closes the c1 GO ADR §6 **open B7 input**: the WATCH-1 0.50x risk figures were
computed under the defective eval drawdown-lock geometry
(`docs/adr/2026-07-17-c1-rail-build-account-registration-go.md` §Addendum
2026-07-22; `docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md`).
Operator directive 2026-07-24: "proceed with the two unmeasured arms."

Combines, without editing any frozen artifact:
  - the 2026-07-22 eval-lock correction idiom: `dd_lock_offset_usd -> 1_000_000.0`
    on both `trailing_locking` tiers (engine's own no-lock idiom per
    `tests/core/test_trailing_locking_boundary.py`; NOT None — None disables the
    DD branch entirely). Same runtime patch as `remc_g8_discharge_check.py`.
  - the FROZEN 2026-07-16 haircut-arm injection (`daily_100k * mult`;
    `core/lifecycle.py` TIER_MULTIPLIER rungs — 1.00x control, 0.50x WATCH-1).
  - the FROZEN 2026-07-15 regime-gate primitives verbatim
    (`full_panel_reference` / `part_b_half_panel`; Run-2 consistency-on).

Scope: full-panel reference on ALL FOUR frozen $100K tiers + half-panel (H1/H2)
on the two discharge tiers. **NO bootstrap** — the withdrawal RESULTS §5 names
the n=100 bootstrap and regime rider as separable long poles; this is the
"~3 min, not an hour" close recommended before B7 arms.

Reproduction controls (corrected 1.00x must match the published corrected runs):
  full-panel: Tradeify 4.74% / MFFU 4.25% / Bulenox 3.51% / BluSky 4.44%
  H1:         Tradeify 6.78% / MFFU 6.28%
(`lab/analysis/c1/tradeify_eval_lock_correction_2026-07-22/RESULTS.md` §3-§4)

Governance: the 0.50x figures answer the GO §6 risk-framing input ONLY. Whether
any 0.50x Part A clearance bears on the §4 falsifier is an operator/ADR-level
question (the frozen gate scored the candidate at 1.00x) — this script makes no
discharge claim.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[3]
_SCORING = _ROOT / "lab" / "analysis" / "c1" / "class_s_candidate1_scoring_2026-07-15"
for _p in (_ROOT / "core", _ROOT / "lab", str(_SCORING), str(_HERE)):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import firm_rules  # noqa: E402
from discovery.prop_survivor_scoring import load_scoring_thresholds  # noqa: E402

sys.argv = [sys.argv[0]]
import run_class_s_c1_scoring as S  # noqa: E402
import run_class_s_c1_regime_gate as R  # noqa: E402

LOCKING_TIERS = ("Tradeify_Select_100K", "MFFU_Rapid_100K")
UNREACHABLE = 1_000_000.0
ARMS = {"1.00x": 1.00, "0.50x": 0.50}

# Published corrected 1.00x pins (tradeify_eval_lock_correction_2026-07-22/RESULTS.md).
PUB_FULL_1P00 = {
    "Bulenox_100K": 0.0351,
    "Tradeify_Select_100K": 0.0474,
    "MFFU_Rapid_100K": 0.0425,
    "BluSky_Premium_100K": 0.0444,
}
PUB_H1_1P00 = {"Tradeify_Select_100K": 0.0678, "MFFU_Rapid_100K": 0.0628}
FULL_TOL = 0.0015  # 0.15pp — seeded engine, near-exact expected
H1_TOL = 0.010     # 1.0pp — matches the haircut runner's repro band


def main() -> int:
    S.phase0_verify()
    for leg in S.C1_STRATS:
        S.resolve_panel_path(leg)
    panel, meta, _ = S.build_scaled_panel(
        S.C1_STRATS, S.C1_ALLOCS, expect_1r=dict(S.EXPECTED_1R)
    )
    daily = S.book_daily_at_100k(panel)
    thr = load_scoring_thresholds(S.GATE_PREREG)
    all_tiers = tuple(thr.tier_keys)
    print(
        f"[corr-haircut] panel {meta['panel_span']} n_bdays={meta['n_bdays']} "
        f"floor(bust<={thr.eval_bust_ceiling:.1%}, pass>={thr.pass_floor:.0%}) "
        f"tiers={list(all_tiers)}",
        flush=True,
    )

    for t in LOCKING_TIERS:
        firm_rules.FIRM_RULES[t]["dd_lock_offset_usd"] = UNREACHABLE
    print(f"[corr-haircut] patch: lock unreachable on {LOCKING_TIERS}", flush=True)

    out: dict = {
        "date": "2026-07-24",
        "authorization": "operator directive 2026-07-24 — proceed with the two unmeasured arms",
        "geometry": "CORRECTED (dd_lock_offset_usd unreachable on both trailing_locking tiers)",
        "scope": "full-panel all four frozen $100K tiers + half-panel on discharge tiers; NO bootstrap",
        "floor": {"bust_ceiling": thr.eval_bust_ceiling, "pass_floor": thr.pass_floor},
        "panel_meta": meta,
        "arms": {},
    }
    try:
        for name, mult in ARMS.items():
            t0 = time.time()
            dh = daily * mult
            print(f"[corr-haircut] ===== ARM {name} (x{mult}) =====", flush=True)
            full = R.full_panel_reference(dh, thr, tiers=all_tiers)
            half = R.part_b_half_panel(dh, thr)  # discharge tiers only
            out["arms"][name] = {
                "lifecycle_mult": mult,
                "full_panel": full,
                "half_panel": half,
                "wall_s": round(time.time() - t0, 1),
            }
    finally:
        # 2026-08-07 W1: restore-to-100 RETIRED (08-04 default is UNREACHABLE).
        # docs/adr/2026-08-07-w1-intraday-honest-engine-remeasure.md
        for t in LOCKING_TIERS:
            firm_rules.FIRM_RULES[t]["dd_lock_offset_usd"] = UNREACHABLE

    # Reproduction control — corrected 1.00x vs published corrected pins.
    repro = {"ok": True, "full": {}, "H1": {}}
    for tk, pub in PUB_FULL_1P00.items():
        got = float(out["arms"]["1.00x"]["full_panel"][tk]["headline_bust"])
        ok = abs(got - pub) <= FULL_TOL
        repro["full"][tk] = {"got": got, "published": pub, "ok": ok}
        repro["ok"] = repro["ok"] and ok
    for tk, pub in PUB_H1_1P00.items():
        got = float(out["arms"]["1.00x"]["half_panel"]["tiers"][tk]["H1"]["headline_bust"])
        ok = abs(got - pub) <= H1_TOL
        repro["H1"][tk] = {"got": got, "published": pub, "ok": ok}
        repro["ok"] = repro["ok"] and ok
    out["reproduction_control"] = repro
    out["trustworthy"] = bool(repro["ok"])

    dest = _HERE / "corrected_haircut_fullpanel_report.json"
    dest.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")

    print(f"\n[corr-haircut] reproduction control: "
          f"{'OK' if repro['ok'] else 'MISMATCH — 0.50x figures NOT trustworthy'}", flush=True)
    for name in ARMS:
        a = out["arms"][name]
        print(f"\n=== ARM {name} (corrected geometry) ===", flush=True)
        for tk in all_tiers:
            f = a["full_panel"][tk]
            line = (f"  {tk:24s} full bust={f['headline_bust']:.2%} "
                    f"pass={f['pass_rate']:.2%} floor={'PASS' if f['floor_ok'] else 'FAIL'}")
            h = a["half_panel"]["tiers"].get(tk)
            if h:
                line += (f" | H1 {h['H1']['headline_bust']:.2%}"
                         f"/{'PASS' if h['H1']['floor_ok'] else 'FAIL'}"
                         f" H2 {h['H2']['headline_bust']:.2%}"
                         f"/{'PASS' if h['H2']['floor_ok'] else 'FAIL'}")
            print(line, flush=True)
    print(f"\n[written] {dest}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
