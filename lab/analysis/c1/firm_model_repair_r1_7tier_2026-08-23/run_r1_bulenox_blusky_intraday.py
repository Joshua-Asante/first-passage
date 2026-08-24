"""R1 -- intraday-honest re-run for Bulenox_100K / BluSky_Premium_100K (successor to W1).

Task: docs/superpowers/plans/2026-08-23-viable-strategy-parallel-s4-firm-repair.md
      "Task R1 -- 7-tier intraday-honest re-run".
Entry packet: docs/briefs/closures/Q-FIRMEOD-1-closure-falsified.md (CLOCK evidence,
Bulenox_100K bust_trailing 0->1 flip) + docs/adr/2026-08-07-w1-intraday-honest-engine-remeasure.md
(the fix pattern this script extends from Tradeify/MFFU to Bulenox/BluSky).

WHY A NEW SCRIPT, NOT AN EDIT TO run_w1_intraday_both_halves.py: that script is a frozen
Phase-4 Cursor packet (Trap #12 -- frozen artifacts are not edited in place). This script
is a sibling that imports its pure helper `build_book_intraday_low` (and reuses its
`_run_partition`) verbatim rather than re-deriving the bar-to-excursion construction --
same technique run_w1_intraday_both_halves.py itself uses for run_class_s_c1_scoring.py.

DEFECT FOUND (recorded, not fixed here): run_w1_intraday_both_halves.py's own sys.path
setup points `_SCORING` at `class_s_candidate1_scoring_2026-07-15/`, but
`run_class_s_c1_scoring.py` was pruned from that directory by the Great Prune
(commit 283d1de, 2026-08-08) and now lives only in `geofit_iid_sufficiency_power_2026-08-15/`
(vendored copy, byte-identical per that probe's own README). Importing
run_w1_intraday_both_halves.py directly today raises ModuleNotFoundError. This script
works around that by adding the geofit directory to sys.path FIRST, so the same-named
`run_class_s_c1_scoring` import resolves before W1's own (now-dead) path entry is tried.
Verified empirically this session (`python -c "import run_w1_intraday_both_halves"` fails
with the geofit path absent; succeeds with it present, and reuses the same cached module).
Not repaired in run_w1_intraday_both_halves.py itself -- that edit belongs to whoever next
touches that frozen packet, not to this sibling.

SCOPE: re-runs the two PUBLISHED Bulenox_100K / BluSky_Premium_100K bust/pass figures that
exist on the class_s candidate #1 (2-leg MYM+MNQ) book at full-panel (no H1/H2 was ever
published for these two tiers at either arm -- see RESULTS.md's own citation table):
  - 1.00x, no haircut  -- lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/RESULTS.md
    (Bulenox 3.51%/96.49%, BluSky 4.44%/95.54%), reproduced as a control in
    lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/CORRECTED_FULLPANEL.md.
  - 0.50x WATCH-1 haircut -- CORRECTED_FULLPANEL.md (Bulenox 0.08%/99.82%,
    BluSky 0.08%/99.80%).
Both dd_type="trailing" tiers never touch dd_lock_offset_usd (core/mc/preflight.py:169-171),
so no lock-unreachable patch is needed here (that patch is trailing_locking-only,
Tradeify/MFFU, and this script never scores those tiers).

Frozen inputs (no re-picking, per W1 ADR pattern): thresholds/seeds/sims/horizon all come
from load_scoring_thresholds() reading the SAME 2026-07-13 survivor-scoring pre-reg W1 read.
"""
from __future__ import annotations

import json
import sys
import time
from dataclasses import replace
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[3]
_GEOFIT = _ROOT / "lab" / "analysis" / "c1" / "geofit_iid_sufficiency_power_2026-08-15"
_W1DIR = _ROOT / "lab" / "analysis" / "c1" / "class_s_c1_haircut_regime_remc_2026-07-16"
for _p in (_ROOT / "core", _ROOT / "lab", str(_GEOFIT), str(_W1DIR)):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from discovery.prop_survivor_scoring import (  # noqa: E402
    assert_intraday_channel_nonvacuous,
    load_scoring_thresholds,
    paired_blocks_from_daily,
    score_part_a,
)

sys.argv = [sys.argv[0]]
import run_class_s_c1_scoring as S  # noqa: E402  (resolves via _GEOFIT on sys.path)
import run_class_s_c1_regime_gate as R  # noqa: E402
import run_w1_intraday_both_halves as W1  # noqa: E402  (reuses build_book_intraday_low, _run_partition)

TARGET_TIERS = ("Bulenox_100K", "BluSky_Premium_100K")
ARMS = {"1.00x": 1.00, "0.50x": 0.50}
NONVAC_HORIZON = 400
NONVAC_SIMS = 200

# Published EOD-clock pins this script re-runs honest-clock (see module docstring for source).
PUBLISHED_EOD = {
    "1.00x": {
        "Bulenox_100K": {"bust": 0.0351, "pass": 0.9649},
        "BluSky_Premium_100K": {"bust": 0.0444, "pass": 0.9554},
    },
    "0.50x": {
        "Bulenox_100K": {"bust": 0.0008, "pass": 0.9982},
        "BluSky_Premium_100K": {"bust": 0.0008, "pass": 0.9980},
    },
}


def main() -> int:
    S.phase0_verify()
    for leg in S.C1_STRATS:
        S.resolve_panel_path(leg)
    panel, meta, _ = S.build_scaled_panel(
        S.C1_STRATS, S.C1_ALLOCS, expect_1r=dict(S.EXPECTED_1R)
    )
    daily = S.book_daily_at_100k(panel)
    thr = load_scoring_thresholds(S.GATE_PREREG)
    print(
        f"[r1] panel {meta['panel_span']} n={meta['n_bdays']} "
        f"floor bust<={thr.eval_bust_ceiling:.1%} pass>={thr.pass_floor:.0%} "
        f"targets={TARGET_TIERS}",
        flush=True,
    )

    print("[r1] deriving bar-level intraday_low (same construction as W1) ...", flush=True)
    t0 = time.time()
    intraday, cov = W1.build_book_intraday_low(panel, meta)
    print(
        f"[r1] intraday_low ready in {time.time()-t0:.1f}s "
        f"min={float(intraday.min()):.2f} neg_days={int(np.sum(intraday < 0))}",
        flush=True,
    )
    assert len(intraday) == len(daily)

    out: dict = {
        "date": "2026-08-23",
        "task": "R1 -- lab/analysis/c1/firm_model_repair_r1_7tier_2026-08-23",
        "parent_plan": "docs/superpowers/plans/2026-08-23-viable-strategy-parallel-s4-firm-repair.md",
        "predecessor": "docs/briefs/closures/Q-FIRMEOD-1-closure-falsified.md",
        "geometry": "intraday_low from 15m bars (same book as W1); dd_lock_offset_usd N/A (trailing, not trailing_locking)",
        "floor": {"bust_ceiling": thr.eval_bust_ceiling, "pass_floor": thr.pass_floor},
        "panel_meta": meta,
        "intraday_coverage": cov,
        "nonvacuity": {},
        "arms": {},
    }

    # Non-vacuity guard PER TARGET TIER (not inherited from Tradeify's W1 proof) --
    # proves the intraday channel is load-bearing for Bulenox/BluSky's OWN dd_type="trailing"
    # (%-of-peak) branch specifically, not assumed from the trailing_locking (fixed-$) branch.
    thr_nv = replace(thr, horizon=NONVAC_HORIZON)
    blocks_p, blocks_l = paired_blocks_from_daily(daily, intraday)
    for firm_key in TARGET_TIERS:
        print(f"[r1] non-vacuity guard ({firm_key}, 1.00x book, horizon={NONVAC_HORIZON}) ...", flush=True)
        nv = assert_intraday_channel_nonvacuous(
            blocks_p,
            blocks_l,
            thresholds=thr_nv,
            firm_key=firm_key,
            n_sims=NONVAC_SIMS,
            horizon=NONVAC_HORIZON,
        )
        out["nonvacuity"][firm_key] = {
            "eod_bust": float(nv["eod"]["headline_bust"]),
            "eod_pass": float(nv["eod"]["pass_rate"]),
            "real_bust": float(nv["real"]["headline_bust"]),
            "real_pass": float(nv["real"]["pass_rate"]),
            "ok": True,
        }
        print(
            f"[r1]   non-vacuity OK -- eod bust={nv['eod']['headline_bust']:.4f} "
            f"real bust={nv['real']['headline_bust']:.4f}",
            flush=True,
        )

    for arm_name, mult in ARMS.items():
        print(f"[r1] ===== ARM {arm_name} (x{mult}) =====", flush=True)
        dh = daily * mult
        ih = intraday * mult
        out["arms"][arm_name] = {"lifecycle_mult": mult, "tiers": {}}
        for firm_key in TARGET_TIERS:
            t1 = time.time()
            res = W1._run_partition(dh, ih, firm_key, thr, n_sims=None)
            wall = time.time() - t1
            pub = PUBLISHED_EOD[arm_name][firm_key]
            delta_bust_pp = (res["headline_bust"] - pub["bust"]) * 100.0
            flipped = bool(pub["bust"] <= thr.eval_bust_ceiling and not res["floor_ok"])
            print(
                f"[r1]   {firm_key:22s} honest bust={res['headline_bust']:.4%} "
                f"pass={res['pass_rate']:.4%} {'PASS' if res['floor_ok'] else 'FAIL'} "
                f"(EOD was {pub['bust']:.4%}, delta={delta_bust_pp:+.3f}pp) "
                f"flipped={flipped} ({wall:.0f}s)",
                flush=True,
            )
            out["arms"][arm_name]["tiers"][firm_key] = {
                **res,
                "published_eod_bust": pub["bust"],
                "published_eod_pass": pub["pass"],
                "delta_bust_pp": delta_bust_pp,
                "verdict_flipped_pass_to_fail": flipped,
            }

    dest = _HERE / "r1_bulenox_blusky_intraday_report.json"
    dest.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"[r1] written {dest}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
