#!/usr/bin/env python3
"""EXPLORATORY: 5-strategy MC probe — locked book + Guardian Silver v1.0.

Answers ONE question, research-grade: if Guardian Silver v1.0 (no-BE baseline
or be4.8 config) were added to the locked 4-strategy book at a small
allocation, what happens to challenge pass/bust/p99 DD on the canonical
Pepperstone panel?

This is NOT a lock artifact and NOT an admission decision (brief §5 forbidden
move 5; Guardian-family-on-XAGUSD remains registry-rejected for admission —
docs/rejected_candidates.md). It quantifies the bust-risk half of "is it
deployable?" so the structural answer has numbers attached.

Zero-fork: imports the locked portfolio_mc primitives (_load_all, _run_seeds,
implied_1r, SIMS_PER_SEED, SEEDS) and uses the Q-SWAP-4 panels_override +
Q-SWAP-2 fixed_1r_reference extension points. The four locked legs' 1R values
are pinned to their own adaptive implied_1r results (byte-equal calibration to
the anchor); Silver's 1R is its median |loss| (Guardian-family pinning).

Caveats (state with any quoted number):
* Canonical panel = 2022-26 compounded, benign-regime-weighted (the same
  caveat the 2026-06-07 HOLD ADR owns). Silver's weak half is H1 2022-23
  (PF 1.57-1.86 vs 3.4-3.6 in H2) — a regime-split amplifier this panel
  under-expresses by construction.
* Silver CSVs are prototype evidence: no lock, Pine not in-repo, BE question
  unresolved (see RESULTS.md — the +50.7% BE claim inverted vs the true
  no-BE baseline).

Run: python lab/analysis/guardian_silver_be_2026-06-10/portfolio_mc_silver_probe.py
Skips with a message if the gitignored CSVs are absent (public clone).
"""
from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "core"))

import portfolio_mc as pmc  # noqa: E402
from dd_protection import DD_TRIGGER, DD_SCALE  # noqa: E402

PEP_DIR = REPO_ROOT / "core/data/tv_exports/pepperstone"
BASELINE_CSV = PEP_DIR / "Guardian_Silver_v1.0_PEPPERSTONE_XAGUSD_2026-06-10_d87c2.csv"
BE48_CSV = PEP_DIR / "Guardian_Silver_v1.0_PEPPERSTONE_XAGUSD_2026-06-10_7c8c2_be4.8.csv"

# Allocation grid: 0.15% (parent-session-studied size) and 0.34%
# (the Guardian-equivalent full slot).
SILVER_ALLOCS = (0.0015, 0.0034)


def stage_be48_copy() -> Path:
    """The be4.8 export's config suffix makes an 8-field filename; the MVD
    identity gate requires exactly 7. Stage a copy with the config tag folded
    into the (identity-unchecked) instrument token."""
    staging = Path(tempfile.gettempdir()) / "gs_mc_staging"
    staging.mkdir(exist_ok=True)
    dst = staging / "Guardian_SilverBE48_v1.0_PEPPERSTONE_XAGUSD_2026-06-10_7c8c2.csv"
    shutil.copy2(BE48_CSV, dst)
    return dst


def silver_r1(csv_path: Path) -> float:
    """Guardian-family 1R: median |loss| on the raw CSV pnl (same series
    load_trades feeds implied_1r)."""
    trades = pmc.load_trades(csv_path)
    losses = trades["pnl"][trades["pnl"] < 0].abs()
    return float(losses.median())


def run_config(allocs: dict, panels_override: dict | None,
               versions_override: dict | None,
               fixed_1r: dict | None, label: str) -> dict:
    """compute_default_config's aggregation, re-implemented only because the
    production wrapper does not expose panels_override (it exists one level
    down in _load_all, Q-SWAP-4)."""
    trades_by_strat, panel, blocks, scale_info, panel_strats = pmc._load_all(
        allocs,
        panel_name="pepperstone",
        fixed_1r_reference=fixed_1r,
        panels_override=panels_override,
        expected_versions_override=versions_override,
    )
    fallback_count = sum(1 for info in scale_info.values() if info["fell_back"])
    pmc.assert_no_fallback(fallback_count, label=f"silver probe {label}")

    seeds_results = pmc._run_seeds(blocks, DD_TRIGGER, DD_SCALE, strats=panel_strats)
    per_seed = pmc.SIMS_PER_SEED
    pass_r = [r["outcomes"]["pass"] / per_seed for r in seeds_results]
    bust_r = [(r["outcomes"]["bust_daily"] + r["outcomes"]["bust_static"]) / per_seed
              for r in seeds_results]
    inact_r = [r["outcomes"]["bust_inactivity"] / per_seed for r in seeds_results]
    all_days = [d for r in seeds_results for d in r["days_to_pass"]]
    all_dds = [d for r in seeds_results for d in r["max_dds"]]
    attrib = {s: sum(r["bust_attribution"][s] for r in seeds_results) for s in panel_strats}
    total_attrib = sum(attrib.values()) or 1

    out = {
        "label": label,
        "pass": float(np.mean(pass_r)) * 100,
        "bust": float(np.mean(bust_r)) * 100,
        "inact": float(np.mean(inact_r)) * 100,
        "p99_dd": float(np.percentile(all_dds, 99)) * 100,
        "median_days": int(np.median(all_days)) if all_days else None,
        "attrib": {s: attrib[s] / total_attrib * 100 for s in panel_strats},
        "scale_info": scale_info,
        "n_blocks": len(blocks),
        "panel_span": f"{panel.index.min().date()} -> {panel.index.max().date()}",
    }
    print(f"\n=== {label} ===")
    print(f"  pass {out['pass']:.2f}%  bust {out['bust']:.2f}%  "
          f"inactivity {out['inact']:.2f}%  p99 DD {out['p99_dd']:.2f}%  "
          f"median days {out['median_days']}")
    print(f"  bust attribution: " + "  ".join(f"{s} {v:.1f}%" for s, v in out["attrib"].items()))
    for s, info in scale_info.items():
        print(f"  1R {s}: ${info['implied_1r']:,.2f} (scale {info['scale']:.3f}, n={info['n_trades']})")
    return out


def main() -> int:
    for p in (BASELINE_CSV, BE48_CSV):
        if not p.exists():
            print(f"SKIP — gitignored vendor CSV absent (public clone?): {p}")
            return 0

    # 1) Anchor reproduction — validates the environment before any 5-leg read.
    anchor = run_config(dict(pmc.ALLOCATIONS), None, None, None,
                        "anchor 4-strategy (expect ~99.83/0.17/4.37)")
    drift = abs(anchor["pass"] - 99.83) > 0.15 or abs(anchor["p99_dd"] - 4.37) > 0.25
    if drift:
        print("\nHALT — anchor did not reproduce within tolerance; "
              "no 5-strategy read is valid from this environment.")
        return 1

    # 2) Pin the four locked legs' 1R at their adaptive values so the silver
    #    runs differ from the anchor ONLY by the added leg.
    locked_1r = {s: anchor["scale_info"][s]["implied_1r"] for s in pmc.ALLOCATIONS}

    be48_staged = stage_be48_copy()
    silver_cfgs = {
        "silver=no-BE baseline": (BASELINE_CSV, silver_r1(BASELINE_CSV)),
        "silver=be4.8": (be48_staged, silver_r1(be48_staged)),
    }

    results = [anchor]
    for cfg_label, (csv_path, r1) in silver_cfgs.items():
        for alloc in SILVER_ALLOCS:
            allocs = dict(pmc.ALLOCATIONS) | {"silver": alloc}
            # Runtime-additive registry entries for the 5th leg (lab-side only;
            # module dicts reset on process exit — core untouched on disk).
            pmc.STRATEGY_FILENAME_TOKEN["silver"] = "Guardian"
            pmc.EXPECTED_SYMBOLS_BY_BROKER["pepperstone"]["silver"] = "XAGUSD"
            results.append(run_config(
                allocs,
                panels_override={"silver": csv_path},
                versions_override={"silver": "v1.0"},
                fixed_1r=locked_1r | {"silver": r1},
                label=f"{cfg_label} @ {alloc * 100:.2f}%",
            ))

    print("\n\n=== SUMMARY (lock gates: bust < 1.00%, p99 DD < 5.00%) ===")
    print(f"{'config':42s} {'pass%':>7s} {'bust%':>7s} {'p99DD%':>7s} {'med.days':>8s} {'silver attrib%':>14s}")
    for r in results:
        sa = r["attrib"].get("silver", float("nan"))
        sa_s = f"{sa:.1f}" if sa == sa else "-"
        print(f"{r['label']:42s} {r['pass']:7.2f} {r['bust']:7.2f} "
              f"{r['p99_dd']:7.2f} {str(r['median_days']):>8s} {sa_s:>14s}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
