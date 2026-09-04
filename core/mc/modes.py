"""
portfolio_mc — challenge-outcome simulator (single-tier)
========================================================
Answers one question: given the locked strategies and DD-protection config,
what is the challenge pass/bust distribution?

Not in scope: per-strategy diagnostics, allocation tuning, live integration.
See the FINAL decision page: https://www.notion.so/346dc0b53c11816085bbf2292be934cc

Invocation (top-level module — pyproject declares flat py-modules, no
package namespace):
    python -m pytest tests/core/test_mc_synthetic_engine.py  # engine owner
    python core/portfolio_mc.py --panel cme                  # registered; MVD gate
                                                             # fails on CME export names
    # Pepperstone default run is retired (substrate Phase 3).
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import pandas as pd

try:
    from ..dd_protection import DD_TRIGGER, DD_SCALE
    from ..lib.mvd import assert_min_rows, assert_window, assert_no_fallback, assert_tv_export
    from ..historical_challenge import (
        DAILY_LOSS_PCT_SIGNED,
        HISTORICAL_CHALLENGE_BASE_RISK,
        INACTIVITY_LIMIT,
        MIN_TRADING_DAYS,
        PROFIT_TARGET_ABS,
        STARTING_EQUITY,
        STATIC_DD_PCT_SIGNED,
    )
    from . import ingest as _mc_ingest
    from . import simulation as _mc_simulation
    from ..tv_schema import (
        TV_COLUMN_ALIASES,
        normalize_tv_columns as _canonical_normalize_tv_columns,
    )
except ImportError:
    from dd_protection import DD_TRIGGER, DD_SCALE
    from lib.mvd import assert_min_rows, assert_window, assert_no_fallback, assert_tv_export
    from historical_challenge import (
        DAILY_LOSS_PCT_SIGNED,
        HISTORICAL_CHALLENGE_BASE_RISK,
        INACTIVITY_LIMIT,
        MIN_TRADING_DAYS,
        PROFIT_TARGET_ABS,
        STARTING_EQUITY,
        STATIC_DD_PCT_SIGNED,
    )
    from mc import ingest as _mc_ingest
    from mc import simulation as _mc_simulation
    from tv_schema import (
        TV_COLUMN_ALIASES,
        normalize_tv_columns as _canonical_normalize_tv_columns,
    )

# Historical challenge fixture (substrate Phase 4) — not a FIRM_RULES row.
PROFIT_TARGET = PROFIT_TARGET_ABS
DAILY_LOSS_PCT = DAILY_LOSS_PCT_SIGNED
STATIC_DD_PCT = STATIC_DD_PCT_SIGNED
# FXIFY-correct timeout semantic, locked 2026-05-16 — see
# docs/adr/2026-05-16-fxify-correct-timeout-semantic.md (closes Q-MCTO-1).
# INACTIVITY_LIMIT models the retired FXIFY challenge-fail rule
# (60 consecutive idle bdays). HORIZON_CAP = 1500 is a runtime-tractability
# safety; bootstrap-of-week-blocks structure makes both 60-day and 1500-day
# runouts vanishingly rare (empirically 0.00% on the 2026-05-14 panel under
# C2 + 0.75/0.45 allocations).
HORIZON_CAP = 1500
SIMS_PER_SEED = 10_000
SEEDS = (42, 123, 2026)

# Default MC book — historical 4-leg lock (Phase C: not living firm_rules._BASE_RISK).
ALLOCATIONS: Dict[str, float] = dict(HISTORICAL_CHALLENGE_BASE_RISK)
STRATS = tuple(ALLOCATIONS.keys())

# Filename token used by the MVD identity gate. Both Striker variants (DJ30 + NAS100)
# share the "Striker" strategy token; differentiation is via symbol (US30 vs NAS100).
STRATEGY_FILENAME_TOKEN: Dict[str, str] = {
    "guardian":       "Guardian",
    "striker":        "Striker",
    "aegis":          "Aegis",
    "striker_nas100": "Striker",
}

PEPPERSTONE_DIR = Path(__file__).parents[1] / "data" / "tv_exports" / "pepperstone"
CME_DIR = Path(__file__).parents[1] / "data" / "tv_exports" / "cme"

# Q-SWAP-4 Phase 2 candidate Guardian CSV path (historical; not a registered
# default panel). Substrate Phase 3 retired the Pepperstone executable-anchor
# map — research loads panels via panels_override with explicit Paths.
GUARDIAN_V56_CSV = PEPPERSTONE_DIR / "Guardian_Gold_v5.6_PEPPERSTONE_XAUUSD_2026-05-27_9a871.csv"

# Broker panel registry — Pepperstone map empty after substrate Phase 3
# (ADR 2026-07-22 §2-C). The four 2026-05-24 Pepperstone anchor CSVs and
# PEPPERSTONE_PANELS / DEFAULT_PANEL contract are retired. Engine
# correctness lives in tests/core/test_mc_synthetic_engine.py (+ planted
# defects). New panels require an admitting ADR + explicit registration
# here. The "cme" key below is a later admission, not a revival of the
# Pepperstone CLI.
#
# "cme" admitted by ADR 2026-08-19-cme-broker-panel-admission-for-breadth-revival:
# a 2-leg baseline scoped to the two AUTHORIZED futures legs only (Striker DJ30/MYM,
# Striker NAS100/MNQ). Guardian (MGC, SUBTRACT/DEAD) and Aegis (6J, PARK) are
# deliberately excluded from this panel, not merely unpopulated — see that ADR §2.
# Consumed by lab/research_utils/breadth.py's Stage-8 portfolio-breadth tool;
# NOT wired into this module's own _load_all/MC-engine panel path, which is a
# separate, currently-unexercised-for-"cme" consumer, out of that ADR's scope.
PANELS_BY_BROKER: Dict[str, Dict[str, Path]] = {
    "cme": {
        # NOT the "pin latest MYM strategy export" commit's file (2026-07-21_73182.csv) --
        # measured this session at only 343 days' trade-date span, well under the
        # 4yr MVD assert_window floor (core/mc/ingest.py::load_trades). "Latest
        # pinned" turned out to mean a short recency-check re-export, not a full
        # backtest. 2026-07-11_15d8b.csv measured at 2020-01-14..2026-06-30
        # (2359 days, 534 rows) -- the longer of two same-span exports 3 days apart.
        "striker": CME_DIR / "Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-07-11_15d8b.csv",
        "striker_nas100": CME_DIR / "Striker_NAS100_MNQ_CME_MINI_MNQ1!_2026-08-19_3ad92.csv",
    },
}

EXPECTED_SYMBOLS_BY_BROKER: Dict[str, Dict[str, str]] = {
    "cme": {
        "striker": "MYM1!",
        "striker_nas100": "MNQ1!",
    },
}

# Recorded for documentation parity with STRATEGY_FILENAME_TOKEN; the "cme"
# loader path (breadth.py::load_baseline_panel) does not positionally parse a
# version token out of these filenames (CME TV-exports don't follow one
# consistent 7-field pattern the way OANDA/Pepperstone's did — see that
# function's docstring). "v1" for striker_nas100 is sourced from the locked
# parameter record in core/strategies/CATALOG.md (Striker NAS100 v1 LOCKED;
# moved there from CLAUDE.md 2026-09-04); the filename itself carries no
# version token to check against.
EXPECTED_VERSIONS_BY_BROKER: Dict[str, Dict[str, str]] = {
    "cme": {
        "striker": "v4.5",
        "striker_nas100": "v1",
    },
}


# ── Swap modeling (Q-SWAP-1; FXIFY rates per docs/external/fxify_swap_rates_2026-05-25.md) ──

SWAP_RATES_PER_UNIT_PER_NIGHT = _mc_ingest.SWAP_RATES_PER_UNIT_PER_NIGHT
_ROLLOVER_HOUR_ET = _mc_ingest.ROLLOVER_HOUR_ET
_TV_COLUMN_NORMALIZATION = _mc_ingest.TV_COLUMN_NORMALIZATION
_count_rollovers = _mc_ingest.count_rollovers
_compute_per_trade_swap = _mc_ingest.compute_per_trade_swap
_normalize_tv_columns = _mc_ingest.normalize_tv_columns
load_trades = _mc_ingest.load_trades
implied_1r = _mc_ingest.implied_1r
build_daily_panel = _mc_ingest.build_daily_panel
build_week_blocks = _mc_ingest.build_week_blocks


# ── Simulation ────────────────────────────────────────────────────────────

# Compatibility aliases: implementation ownership lives in core/mc/simulation.py.
_simulate_path = _mc_simulation.simulate_path
run_seed = _mc_simulation.run_seed


# ── Reporting ─────────────────────────────────────────────────────────────

def _fmt_config(dd_trigger: float, dd_scale: float, no_protection: bool) -> str:
    if no_protection:
        return "no protection (--no-protection)"
    return f"DD {dd_trigger:.1%} / {dd_scale}× (single-tier)"


_ALLOC_LABEL = {
    "guardian":       "G",
    "striker":        "S",
    "aegis":          "A",
    "striker_nas100": "N",
}


def _fmt_alloc(allocs: Dict[str, float]) -> str:
    parts = [f"{_ALLOC_LABEL.get(s, s)} {v:.2%}" for s, v in allocs.items()]
    return " / ".join(parts)


def _serial_grid_with_progress(blocks: np.ndarray, all_trigs: list,
                                dd_scale: float,
                                strats: Tuple[str, ...] = STRATS,
                                *,
                                firm_kwargs: dict | None = None) -> dict:
    """Run the sensitivity-grid serial path with a Rich progress bar when
    Rich is installed; fall back to plain iteration otherwise.

    The bar advances per (trig, seed) cell — granular feedback during a
    multi-minute run. Numerically inert: same loop, same SEEDS, same numbers.
    """
    try:
        from rich.progress import (
            BarColumn,
            MofNCompleteColumn,
            Progress,
            TextColumn,
            TimeElapsedColumn,
        )
    except ImportError:
        return {
            trig: [
                run_seed(
                    seed, SIMS_PER_SEED, blocks, trig, dd_scale,
                    strats=strats, firm_kwargs=firm_kwargs,
                )
                for seed in SEEDS
            ]
            for trig in all_trigs
        }

    out: dict = {trig: [] for trig in all_trigs}
    total_cells = len(all_trigs) * len(SEEDS)
    columns = [
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        TextColumn("•"),
        TimeElapsedColumn(),
    ]
    with Progress(*columns, transient=True) as progress:
        task = progress.add_task("Sensitivity grid", total=total_cells)
        for trig in all_trigs:
            for seed in SEEDS:
                out[trig].append(
                    run_seed(
                        seed, SIMS_PER_SEED, blocks, trig, dd_scale,
                        strats=strats, firm_kwargs=firm_kwargs,
                    )
                )
                progress.update(task, advance=1)
    return out


def _run_seeds(blocks: np.ndarray, effective_trigger: float, dd_scale: float,
               seeds=SEEDS, parallel: bool = False,
               strats: Tuple[str, ...] = STRATS, *,
               firm_kwargs: dict | None = None,
               sims_per_seed: int | None = None) -> list:
    """Run all seeds. Sequential by default; joblib-parallel when requested.

    Each seed is independent (RNG seeded inside run_seed) so the parallel
    path is byte-identical to the sequential path. The seeds list is preserved
    in order so downstream aggregation is deterministic regardless of mode.

    `firm_kwargs` (added 2026-07-01) passes through to `run_seed` unchanged —
    see its docstring. `None` reproduces today's FXIFY/static behavior.

    `sims_per_seed=None` resolves to this implementation module's current
    `SIMS_PER_SEED`; compatibility facades may pass their own value explicitly.
    """
    if sims_per_seed is None:
        sims_per_seed = SIMS_PER_SEED
    if not parallel:
        return [run_seed(seed, sims_per_seed, blocks, effective_trigger, dd_scale,
                          strats=strats, firm_kwargs=firm_kwargs)
                for seed in seeds]
    try:
        from joblib import Parallel, delayed
    except ImportError as e:
        raise ImportError(
            "--parallel requires joblib. Install with: pip install -e .[mc]"
        ) from e
    return list(Parallel(n_jobs=len(seeds), backend="loky")(
        delayed(run_seed)(seed, sims_per_seed, blocks, effective_trigger, dd_scale,
                           strats=strats, firm_kwargs=firm_kwargs)
        for seed in seeds
    ))


def compute_default_config(dd_trigger: float, dd_scale: float, no_protection: bool,
                           allocs: Dict[str, float],
                           panel_name: str | None = None,
                           parallel: bool = False,
                           apply_swap: bool = False,
                           fixed_1r_reference: Dict[str, float] | None = None,
                           *,
                           firm_kwargs: Dict[str, object] | None = None,
                           account_basis: float | None = None) -> dict:
    """Pure compute path for default MC mode. Returns aggregated metrics dict.

    Consumed by mode_default (printout layered on top). Numerically
    deterministic given fixed SEEDS = (42, 123, 2026) regardless of
    `parallel` mode. Requires a registered panel_name or an explicit
    panels_override path — the Pepperstone executable default was retired
    in substrate Phase 3 (ADR 2026-07-22 §2-C). Engine correctness lives in
    tests/core/test_mc_synthetic_engine.py.

    Q-SWAP-1: apply_swap=False (default) preserves historical swap-OFF
    semantics when a panel is supplied. apply_swap=True applies FXIFY
    DXTrade overnight rates to each trade before aggregation.

    Q-SWAP-2: fixed_1r_reference=None (default) uses adaptive implied_1r.
    When supplied (dict per panel_strats), bypasses adaptive recalibration.

    Phase-1 decoupling (ADR 2026-07-22): ``firm_kwargs`` / ``account_basis``
    default to the historical challenge fixture. Callers construct named-firm
    specs themselves (preflight stays OFF the default import path).
    """
    fk = (
        dict(_mc_simulation.HISTORICAL_CHALLENGE_FIRM_KWARGS)
        if firm_kwargs is None
        else dict(firm_kwargs)
    )
    basis = (
        _mc_simulation.HISTORICAL_CHALLENGE_BASIS
        if account_basis is None
        else account_basis
    )
    trades_by_strat, panel, blocks, scale_info, panel_strats = _load_all(
        allocs, panel_name=panel_name, apply_swap=apply_swap,
        fixed_1r_reference=fixed_1r_reference,
        account_basis=basis,
    )

    fallback_count = sum(1 for info in scale_info.values() if info["fell_back"])
    assert_no_fallback(
        fallback_count,
        label="portfolio_mc implied_1r (Striker/Aegis full-stop cohort)",
    )

    effective_trigger = 10.0 if no_protection else dd_trigger
    seeds_results = _run_seeds(blocks, effective_trigger, dd_scale, parallel=parallel,
                               strats=panel_strats, firm_kwargs=fk)

    per_seed = SIMS_PER_SEED
    pass_r = [r["outcomes"]["pass"] / per_seed for r in seeds_results]
    bd_r   = [r["outcomes"]["bust_daily"] / per_seed for r in seeds_results]
    bs_r   = [r["outcomes"]["bust_static"] / per_seed for r in seeds_results]
    bi_r   = [r["outcomes"]["bust_inactivity"] / per_seed for r in seeds_results]
    hc_r   = [r["outcomes"]["horizon_cap"] / per_seed for r in seeds_results]
    # Headline bust rate stays daily+static for lock-gate continuity with prior
    # anchors; bust_inactivity is reported separately. See ADR §Decision.
    bust_r = [d + s for d, s in zip(bd_r, bs_r)]

    all_days = [d for r in seeds_results for d in r["days_to_pass"]]
    all_dds  = [d for r in seeds_results for d in r["max_dds"]]

    attrib = {s: sum(r["bust_attribution"][s] for r in seeds_results) for s in panel_strats}

    return {
        "panel_name": panel_name,
        "panel_start": panel.index.min(),
        "panel_end": panel.index.max(),
        "n_bdays": len(panel),
        "n_blocks": len(blocks),
        "panel_strats": panel_strats,
        "scale_info": scale_info,
        "seeds_results": seeds_results,
        "pass_rate": float(np.mean(pass_r)),
        "pass_sigma": float(np.std(pass_r)),
        "bust_rate": float(np.mean(bust_r)),
        "bust_sigma": float(np.std(bust_r)),
        "bust_daily_rate": float(np.mean(bd_r)),
        "bust_static_rate": float(np.mean(bs_r)),
        "bust_inactivity_rate": float(np.mean(bi_r)),
        "horizon_cap_rate": float(np.mean(hc_r)),
        "median_days_to_pass": int(np.median(all_days)) if all_days else None,
        "p50_dd": float(np.percentile(all_dds, 50)),
        "p95_dd": float(np.percentile(all_dds, 95)),
        "p99_dd": float(np.percentile(all_dds, 99)),
        "bust_attribution": attrib,
        "apply_swap": apply_swap,
        "fixed_1r_reference": dict(fixed_1r_reference) if fixed_1r_reference is not None else None,
    }


def report_default(result: dict, dd_trigger: float, dd_scale: float,
                   allocs: Dict[str, float], no_protection: bool):
    """Print the default MC output block from a compute_default_config() result."""
    n_seeds = len(result["seeds_results"])
    per_seed = SIMS_PER_SEED

    panel_strats = result.get("panel_strats", tuple(allocs.keys()))
    panel_allocs = {s: allocs[s] for s in panel_strats}

    print("=== Portfolio MC ===")
    print(f"Config: {_fmt_config(dd_trigger, dd_scale, no_protection)}")
    print(f"Allocations: {_fmt_alloc(panel_allocs)}")
    print(f"Swap: {'ON (FXIFY rates, Q-SWAP-1)' if result.get('apply_swap') else 'OFF (backtest as-published)'}")
    print(f"1R source: {'FIXED (pre-shock reference, Q-SWAP-2)' if result.get('fixed_1r_reference') is not None else 'ADAPTIVE (current panel)'}")
    print(f"Sims: {per_seed:,} × {n_seeds} seeds, inactivity {INACTIVITY_LIMIT}d / horizon-cap {HORIZON_CAP}d")
    print()
    print(f"Pass:               {result['pass_rate']:>6.2%} (sigma {result['pass_sigma']:.2%})")
    print(f"Bust:               {result['bust_rate']:>6.2%} (sigma {result['bust_sigma']:.2%})")
    print(f"  Daily:            {result['bust_daily_rate']:>6.2%}")
    print(f"  Static:           {result['bust_static_rate']:>6.2%}")
    print(f"Bust inactivity:    {result['bust_inactivity_rate']:>6.2%}")
    print(f"Horizon cap:        {result['horizon_cap_rate']:>6.2%}")
    if result["median_days_to_pass"] is not None:
        print(f"Median days to pass: {result['median_days_to_pass']}")
    print(f"p50 DD:       {result['p50_dd']:.2%}")
    print(f"p95 DD:       {result['p95_dd']:.2%}")
    print(f"p99 DD:       {result['p99_dd']:.2%}")
    print()
    print("Bust attribution:")
    total_busts = sum(result["bust_attribution"].values())
    if total_busts > 0:
        # Print in descending share order so the marginal contributor reads first.
        ranked = sorted(result["bust_attribution"].items(), key=lambda kv: kv[1], reverse=True)
        for s, n in ranked:
            pct = n / total_busts
            print(f"  {s:<14} {pct:>5.1%}")
    else:
        print("  (no busts)")


# ── CLI modes ─────────────────────────────────────────────────────────────

_NO_REGISTERED_PANEL_MSG = (
    "No registered broker panel{suffix}. The Pepperstone executable anchor was "
    "retired (ADR 2026-07-22 Phase 3). Pass panels_override with explicit CSV "
    "paths plus expected_symbols_override / expected_versions_override, or use "
    "tests/core/test_mc_synthetic_engine.py for engine correctness."
)


def _load_all(allocs: Dict[str, float], panel_name: str | None = None,
              apply_swap: bool = False,
              fixed_1r_reference: Dict[str, float] | None = None,
              panels_override: Dict[str, Path] | None = None,
              expected_versions_override: Dict[str, str] | None = None,
              expected_symbols_override: Dict[str, str] | None = None,
              *,
              account_basis: float | None = None):
    # MVD identity gate on each loaded CSV — catches the 'wrong CSV in load
    # slot' class. Pepperstone default is gone; a named panel (today: "cme")
    # loads PANELS_BY_BROKER[panel_name]. That "cme" path is breadth-admitted
    # and still hits the strict 7-field MVD filename gate here. Callers may
    # also supply panels_override (+ expected symbol/version maps) explicitly.
    registered = panel_name is not None and panel_name in PANELS_BY_BROKER
    if registered:
        panels = dict(PANELS_BY_BROKER[panel_name])
        if panels_override:
            panels.update(panels_override)
        expected_broker = panel_name.upper()
        expected_symbols = dict(EXPECTED_SYMBOLS_BY_BROKER[panel_name])
        if expected_symbols_override:
            expected_symbols.update(expected_symbols_override)
        expected_versions = dict(EXPECTED_VERSIONS_BY_BROKER[panel_name])
        if expected_versions_override:
            expected_versions.update(expected_versions_override)
    elif panels_override:
        if expected_symbols_override is None or expected_versions_override is None:
            raise ValueError(
                "panels_override without a registered panel_name requires "
                "expected_symbols_override and expected_versions_override."
            )
        panels = dict(panels_override)
        expected_broker = (panel_name or "OVERRIDE").upper()
        expected_symbols = dict(expected_symbols_override)
        expected_versions = dict(expected_versions_override)
    else:
        suffix = f" named {panel_name!r}" if panel_name else ""
        raise ValueError(_NO_REGISTERED_PANEL_MSG.format(suffix=suffix))
    panel_strats = tuple(panels.keys())
    for s in panel_strats:
        assert_tv_export(
            panels[s],
            expected_strategy=STRATEGY_FILENAME_TOKEN[s],
            expected_version=expected_versions[s],
            expected_broker=expected_broker,
            expected_symbol=expected_symbols[s],
        )
    trades_by_strat = {s: load_trades(panels[s], strategy=s, apply_swap=apply_swap) for s in panel_strats}
    panel_allocs = {s: allocs[s] for s in panel_strats}
    # Q-SWAP-2: validate fixed_1r_reference keys against panel_strats when supplied.
    # Reject early with a clear error rather than KeyError mid-build_daily_panel.
    if fixed_1r_reference is not None:
        ref_keys = set(fixed_1r_reference.keys())
        panel_keys = set(panel_strats)
        missing = panel_keys - ref_keys
        extra = ref_keys - panel_keys
        if missing or extra:
            parts = []
            if missing:
                parts.append(f"missing keys (in panel, not in --fixed-1r): {sorted(missing)}")
            if extra:
                parts.append(f"extra keys (in --fixed-1r, not in panel): {sorted(extra)}")
            raise ValueError(
                f"--fixed-1r reference key mismatch for panel '{panel_name}': "
                + "; ".join(parts)
                + f". Panel strategies are: {list(panel_strats)}."
            )
    panel, scale_info = build_daily_panel(
        trades_by_strat, panel_allocs,
        fixed_1r_reference=fixed_1r_reference,
        account_basis=account_basis,
    )
    blocks = build_week_blocks(panel)
    return trades_by_strat, panel, blocks, scale_info, panel_strats


def mode_default(dd_trigger: float, dd_scale: float, no_protection: bool,
                 allocs: Dict[str, float], panel_name: str | None = None,
                 parallel: bool = False, verbose: bool = True,
                 apply_swap: bool = False,
                 fixed_1r_reference: Dict[str, float] | None = None,
                 *,
                 firm_kwargs: Dict[str, object] | None = None,
                 account_basis: float | None = None):
    result = compute_default_config(dd_trigger, dd_scale, no_protection, allocs,
                                    panel_name=panel_name, parallel=parallel,
                                    apply_swap=apply_swap,
                                    fixed_1r_reference=fixed_1r_reference,
                                    firm_kwargs=firm_kwargs,
                                    account_basis=account_basis)

    if verbose:
        print("Scale factors:")
        for s, info in result["scale_info"].items():
            tag = "  [fallback: median]" if info["fell_back"] else ""
            print(f"  {s:<9} 1R=${info['implied_1r']:>7,.2f}  scale={info['scale']:>6.3f}  n={info['n_trades']}{tag}")
        print(f"Panel ({result['panel_name']}): {result['panel_start'].date()} -> {result['panel_end'].date()}  "
              f"({result['n_bdays']} bdays, {result['n_blocks']} week-blocks)")
        print()

    report_default(result, dd_trigger, dd_scale, allocs, no_protection)


def mode_historical(dd_trigger: float, dd_scale: float, no_protection: bool,
                    allocs: Dict[str, float], panel_name: str | None = None,
                    *,
                    firm_kwargs: Dict[str, object] | None = None,
                    account_basis: float | None = None):
    fk = (
        dict(_mc_simulation.HISTORICAL_CHALLENGE_FIRM_KWARGS)
        if firm_kwargs is None
        else dict(firm_kwargs)
    )
    basis = (
        _mc_simulation.HISTORICAL_CHALLENGE_BASIS
        if account_basis is None
        else account_basis
    )
    _, panel, _, scale_info, panel_strats = _load_all(
        allocs, panel_name=panel_name, account_basis=basis,
    )
    path = panel.values

    effective_trigger = 10.0 if no_protection else dd_trigger
    # Thread the same firm kwargs the Monte Carlo path uses so the walk and
    # the post-hoc equity/profit-target re-walk cannot silently desync
    # (previously modes.STARTING_EQUITY / PROFIT_TARGET vs simulation defaults).
    outcome, day, max_dd, culprit = _simulate_path(
        path, effective_trigger, dd_scale, len(path), **fk
    )

    # Count protection trigger days across the walk
    eq = peak = float(fk["starting_equity"])
    trigger_days = 0
    for i in range(min(day, len(path))):
        dd_from_peak = (eq - peak) / peak if peak > 0 else 0.0
        # ULP-precision rounding mirrors _simulate_path; see Q-MCFP-1
        if not no_protection and round(dd_from_peak, 6) <= -dd_trigger:
            trigger_days += 1
            scale = dd_scale
        else:
            scale = 1.0
        pnl = float((path[i] * scale).sum())
        eq = eq + pnl
        if eq > peak:
            peak = eq
        if outcome == "pass" and round(eq, 2) >= fk["profit_target"]:
            break

    print("=== Portfolio MC — Historical (deterministic) ===")
    print(f"Config: {_fmt_config(dd_trigger, dd_scale, no_protection)}")
    print(f"Allocations: {_fmt_alloc({s: allocs[s] for s in panel_strats})}")
    print(f"Panel ({panel_name}): {panel.index.min().date()} -> {panel.index.max().date()}  ({len(panel)} bdays)")
    print()
    print(f"Outcome:         {outcome.upper()}")
    print(f"Day terminated:  {day} ({panel.index[min(day - 1, len(panel) - 1)].date()})")
    print(f"Max DD:          {max_dd:.2%}")
    print(f"DD tier trigger days (through terminating day): {trigger_days}")
    if culprit is not None:
        print(f"Bust culprit:    {panel_strats[culprit]}")


def mode_sensitivity(dd_scale: float, allocs: Dict[str, float],
                     panel_name: str | None = None,
                     parallel: bool = False,
                     *,
                     firm_kwargs: Dict[str, object] | None = None,
                     account_basis: float | None = None):
    fk = (
        dict(_mc_simulation.HISTORICAL_CHALLENGE_FIRM_KWARGS)
        if firm_kwargs is None
        else dict(firm_kwargs)
    )
    basis = (
        _mc_simulation.HISTORICAL_CHALLENGE_BASIS
        if account_basis is None
        else account_basis
    )
    _, _, blocks, _, panel_strats = _load_all(
        allocs, panel_name=panel_name, account_basis=basis,
    )
    grid = [0.005, 0.010, 0.015, 0.020, 0.025]
    NO_PROTECT_TRIG = 10.0
    all_trigs = grid + [NO_PROTECT_TRIG]

    print("=== Portfolio MC — Sensitivity grid ===")
    print(f"Panel: {panel_name}")
    print(f"Allocations: {_fmt_alloc({s: allocs[s] for s in panel_strats})}")
    print(f"Sims: {SIMS_PER_SEED:,} × {len(SEEDS)} seeds (DD_SCALE fixed at {dd_scale}×)")
    print()
    print(f"{'DD_TRIGGER':<12} {'Pass':>8} {'Bust':>8} {'Timeout':>9} {'p99 DD':>8}")
    print("-" * 48)

    # Compute all (trig, seed) cells. Order-stable: by_trig[trig] holds seed
    # results in SEEDS order regardless of execution mode.
    if parallel:
        try:
            from joblib import Parallel, delayed
        except ImportError as e:
            raise ImportError(
                "--parallel requires joblib. Install with: pip install -e .[mc]"
            ) from e
        pairs = [(trig, seed) for trig in all_trigs for seed in SEEDS]
        flat = list(Parallel(n_jobs=-1, backend="loky")(
            delayed(run_seed)(seed, SIMS_PER_SEED, blocks, trig, dd_scale, strats=panel_strats)
            for trig, seed in pairs
        ))
        by_trig: Dict[float, list] = {trig: [] for trig in all_trigs}
        for (trig, _seed), result in zip(pairs, flat):
            by_trig[trig].append(result)
    else:
        by_trig = _serial_grid_with_progress(blocks, all_trigs, dd_scale, strats=panel_strats)

    def _row(label: str, results: list) -> str:
        pass_r = np.mean([r["outcomes"]["pass"] / SIMS_PER_SEED for r in results])
        bust_r = np.mean([(r["outcomes"]["bust_daily"] + r["outcomes"]["bust_static"]) / SIMS_PER_SEED for r in results])
        # Inactivity + horizon_cap together replace the old "timeout" bucket
        # under FXIFY-correct semantics (locked 2026-05-16).
        nt_r   = np.mean([(r["outcomes"]["bust_inactivity"] + r["outcomes"]["horizon_cap"]) / SIMS_PER_SEED for r in results])
        dds    = [d for r in results for d in r["max_dds"]]
        p99    = np.percentile(dds, 99)
        return f"{label:<12} {pass_r:>8.2%} {bust_r:>8.2%} {nt_r:>9.2%} {p99:>8.2%}"

    for trig in grid:
        print(_row(f"{trig:.3%}", by_trig[trig]))
    print(_row("no-protect", by_trig[NO_PROTECT_TRIG]))


# ── Q-SWAP-3 allocation sweep ────────────────────────────────────────────

# Pre-shock per-strategy 1R reference (Q-SWAP-2 §4 canonical anchor, derived
# from the 2026-05-24 Pepperstone swap-OFF adaptive baseline). Allocation-
# invariant by construction: implied_1r depends on (pnl, strategy, account)
# only, not on allocations — so the same reference dict feeds every sweep
# config. Note the panel key 'striker_nas100' (not the CLI alias 'nas100').
PRE_SHOCK_1R: Dict[str, float] = {
    "guardian":       1208.0,
    "striker":        4229.0,
    "aegis":          3293.0,
    "striker_nas100": 3940.0,
}

# Q-SWAP-3 pre-registered 8-config search space. Frozen at brief §7. ML-3
# (revert candidate) carries an inline note about pyramid mismatch: the
# 2026-05-14 allocations are tested on 2026-05-24 CSVs which were exported
# at pyramid 750%, so the MC sees the *allocation* set without the Pine
# pyramid effect; pure ML-3 reproduction would require CSV re-export at
# pyramid 500%. Surfaced as a DONE_WITH_CONCERNS note in closure.
#
# Variant cells override only the legs that differ from the locked book;
# unchanged legs come from ALLOCATIONS (= historical 4-leg book). REG is the
# lock itself — do not re-literal the lock bytes here.
_LOCK_ALLOC = dict(ALLOCATIONS)
SWEEP_CONFIGS: list = [
    ("GA-1", {**_LOCK_ALLOC, "guardian": 0.0030}),
    ("GA-2", {**_LOCK_ALLOC, "guardian": 0.0028}),
    ("GA-3", {**_LOCK_ALLOC, "guardian": 0.0026}),
    ("GA-4", {**_LOCK_ALLOC, "guardian": 0.0024}),
    ("ML-1", {**_LOCK_ALLOC, "guardian": 0.0030, "striker": 0.0060}),
    ("ML-2", {**_LOCK_ALLOC, "guardian": 0.0030, "aegis": 0.0135}),
    ("ML-3", {**_LOCK_ALLOC, "striker": 0.0075, "striker_nas100": 0.0045}),
    ("REG",  dict(_LOCK_ALLOC)),
]

# Q-SWAP-3 §6 verdict thresholds — load-bearing per-config gate criteria.
# (a) p99 DD < 4.50%, (b) bust < 1.00%, (c) median days-to-pass ≤ 30d.
_GATE_P99_DD = 0.0450
_GATE_BUST = 0.0100
_GATE_MEDIAN = 30


def mode_alloc_sweep(dd_trigger: float, dd_scale: float,
                     panel_name: str | None = None,
                     parallel: bool = False) -> None:
    """Q-SWAP-3 allocation-rebalance sweep under fixed-1R swap-aware MC.

    Iterates SWEEP_CONFIGS, calling compute_default_config(..., apply_swap=True,
    fixed_1r_reference=PRE_SHOCK_1R) per (label, allocs) tuple. REG runs first
    so any harness-introduced regression aborts before the other 7 fire.

    Verdict gate (per Q-SWAP-3 §6): a config RESOLVED iff (a) p99 DD < 4.50%
    AND (b) bust < 1.00% AND (c) median ≤ 30d. Threshold flags reported per
    config; RESOLVED candidate is the passing config with greatest p99 DD
    margin (post-verdict selection rule).
    """
    print("=== Portfolio MC — Q-SWAP-3 Allocation Sweep (fixed-1R swap-aware) ===")
    print(f"Panel: {panel_name}")
    print(f"Protection: {_fmt_config(dd_trigger, dd_scale, no_protection=False)}")
    print(f"Swap: ON (FXIFY rates, Q-SWAP-1)")
    print(f"1R source: FIXED (pre-shock reference, Q-SWAP-2)")
    pre_shock_str = " / ".join(f"{k}=${v:,.0f}" for k, v in PRE_SHOCK_1R.items())
    print(f"Pre-shock 1R: {pre_shock_str}")
    print(f"Sims: {SIMS_PER_SEED:,} × {len(SEEDS)} seeds per config, "
          f"inactivity {INACTIVITY_LIMIT}d / horizon-cap {HORIZON_CAP}d")
    print(f"Verdict gate: (a) p99 DD < {_GATE_P99_DD:.2%}  (b) bust < {_GATE_BUST:.2%}  "
          f"(c) median <= {_GATE_MEDIAN}d")
    print()

    # Reorder so REG fires first (regression sanity).
    ordered = [c for c in SWEEP_CONFIGS if c[0] == "REG"] + \
              [c for c in SWEEP_CONFIGS if c[0] != "REG"]

    results_by_label: Dict[str, dict] = {}
    for label, allocs in ordered:
        # Fresh dict copy per iteration (defensive — compute_default_config
        # threads allocs into multiple layers and we don't want shared refs).
        allocs_copy = dict(allocs)
        result = compute_default_config(
            dd_trigger=dd_trigger,
            dd_scale=dd_scale,
            no_protection=False,
            allocs=allocs_copy,
            panel_name=panel_name,
            parallel=parallel,
            apply_swap=True,
            fixed_1r_reference=PRE_SHOCK_1R,
        )
        results_by_label[label] = result

    # Header
    print(f"{'Label':<6} {'Allocs (G/S/A/N)':<30} {'Pass':>7} {'Bust':>7} "
          f"{'p99 DD':>8} {'Median':>7}  Flags  Margin")
    print("-" * 92)

    # Print in canonical SWEEP_CONFIGS order (GA-1..GA-4, ML-1..ML-3, REG)
    passing: list = []
    for label, allocs in SWEEP_CONFIGS:
        r = results_by_label[label]
        pass_r = r["pass_rate"]
        bust_r = r["bust_rate"]
        p99_dd = r["p99_dd"]
        median = r["median_days_to_pass"] if r["median_days_to_pass"] is not None else 9999

        # Threshold flags: (a) p99 DD < 4.50%, (b) bust < 1.00%, (c) median ≤ 30d
        flag_a = p99_dd < _GATE_P99_DD
        flag_b = bust_r < _GATE_BUST
        flag_c = median <= _GATE_MEDIAN
        flags_str = ("Y" if flag_a else "N") + ("Y" if flag_b else "N") + ("Y" if flag_c else "N")
        margin_pp = (_GATE_P99_DD - p99_dd) * 100.0  # in percentage points (signed)

        alloc_str = (f"{allocs['guardian']*100:.2f}/{allocs['striker']*100:.2f}/"
                     f"{allocs['aegis']*100:.2f}/{allocs['striker_nas100']*100:.2f}")
        print(f"{label:<6} {alloc_str:<30} {pass_r:>7.2%} {bust_r:>7.2%} "
              f"{p99_dd:>8.2%} {median:>7}  {flags_str:<5}  {margin_pp:+.2f}pp")

        if flag_a and flag_b and flag_c and label != "REG":
            passing.append((label, margin_pp, p99_dd, bust_r, median))

    print()

    # REG byte-identity gate vs Q-SWAP-2 canonical (99.80/0.20/4.55, median 27).
    reg = results_by_label["REG"]
    reg_match = (
        abs(reg["pass_rate"] - 0.9980) < 1e-4 and
        abs(reg["bust_rate"] - 0.0020) < 1e-4 and
        abs(reg["p99_dd"]    - 0.0455) < 1e-4 and
        reg["median_days_to_pass"] == 27
    )
    print(f"REG regression sanity vs Q-SWAP-2 fixed-1R Pepperstone canonical "
          f"(99.80/0.20/4.55, median 27): "
          f"{'HELD' if reg_match else 'DRIFTED'}")
    if not reg_match:
        print(f"  Got: pass={reg['pass_rate']:.4%} bust={reg['bust_rate']:.4%} "
              f"p99={reg['p99_dd']:.4%} median={reg['median_days_to_pass']}")

    print()
    print("Per-config bust attribution (descending share):")
    for label, _ in SWEEP_CONFIGS:
        r = results_by_label[label]
        total = sum(r["bust_attribution"].values())
        if total == 0:
            print(f"  {label:<6}  (no busts)")
            continue
        ranked = sorted(r["bust_attribution"].items(), key=lambda kv: kv[1], reverse=True)
        parts = [f"{s} {n/total:.1%}" for s, n in ranked]
        print(f"  {label:<6}  {' / '.join(parts)}  (n={total})")

    print()
    print("Per-config scale factors (verifies implied_1r allocation-invariance):")
    for label, _ in SWEEP_CONFIGS:
        r = results_by_label[label]
        scale_parts = [f"{s} {info['scale']:.3f}" for s, info in r["scale_info"].items()]
        print(f"  {label:<6}  {' / '.join(scale_parts)}")

    print()

    # Verdict summary
    if passing:
        passing.sort(key=lambda x: x[1], reverse=True)  # greatest margin first
        top_label, top_margin, top_p99, top_bust, top_median = passing[0]
        # Ambiguous-tie check: within 0.05pp margin
        ties = [p for p in passing if abs(p[1] - top_margin) < 0.05]
        if len(ties) > 1:
            tie_labels = ", ".join(t[0] for t in ties)
            print(f"VERDICT (provisional): {len(passing)} config(s) clear all three thresholds; "
                  f"{len(ties)} tied within 0.05pp margin at top ({tie_labels}) — "
                  f"AMBIGUOUS RESOLVED CANDIDATE; escalate.")
        else:
            print(f"VERDICT (provisional): RESOLVED candidate = {top_label} "
                  f"(p99 DD margin = {top_margin:+.2f}pp; bust = {top_bust:.2%}; "
                  f"median = {top_median}d). Phase 4 regime-robustness gate required.")
    else:
        print("VERDICT (provisional): FALSIFIED — no config in the pre-registered "
              "search space satisfies all three thresholds simultaneously.")


# ── Q-REGIME-1 boundary sweep ────────────────────────────────────────────

# Q-REGIME-1 §4 pre-registered boundary dates (frozen at brief; see
# docs/briefs/Q-REGIME-1-2024-boundary-h1-h2-split-artifact.md). Each
# boundary date partitions the panel into H1 = [panel_start, boundary)
# and H2 = [boundary, panel_end]. The 2024-04-30 row reproduces the
# Q-SWAP-3 Phase 4 H1/H2 baseline (H1 p99 DD 4.90% / H2 3.81% / spread
# 1.09pp at GA-4 fixed-1R swap-aware). The other four dates produce
# the comparison distribution for the verdict statistic.
BOUNDARY_SWEEP_DATES: list = [
    "2023-07-31",
    "2024-01-31",
    "2024-04-30",
    "2024-07-31",
    "2025-01-31",
]

# GA-4 allocations (Q-SWAP-3 most-conservative passing config; Guardian
# 0.24%, others at canonical 2026-05-23 ADR values). Q-REGIME-1 §5
# forbidden-move #4 pins this as the verdict-input config.
# Same bytes as SWEEP_CONFIGS["GA-4"] — derived, not re-literalized.
GA4_ALLOCATIONS: Dict[str, float] = dict(dict(SWEEP_CONFIGS)["GA-4"])


def _run_half_panel(half_label: str, h_panel: pd.DataFrame,
                    dd_trigger: float, dd_scale: float,
                    parallel: bool, panel_strats: Tuple[str, ...]) -> dict:
    """Run fixed-1R swap-aware seeds on one half panel; return aggregate dict.

    Mirrors archive/docs/briefs/Q-DDP-1/_run_regime_robustness.py and
    docs/briefs/Q-SWAP-3/_run_regime_robustness.py half-panel patterns.
    The half panel arrives already filtered to its date range; this
    helper rebuilds week-blocks and aggregates the per-seed outputs.
    """
    blocks_h = build_week_blocks(h_panel)
    seeds_results = _run_seeds(
        blocks_h, dd_trigger, dd_scale,
        parallel=parallel, strats=panel_strats,
    )
    per_seed = SIMS_PER_SEED
    pass_r = float(np.mean([r["outcomes"]["pass"] / per_seed for r in seeds_results]))
    bust_r = float(np.mean([
        (r["outcomes"]["bust_daily"] + r["outcomes"]["bust_static"]) / per_seed
        for r in seeds_results
    ]))
    all_days = [d for r in seeds_results for d in r["days_to_pass"]]
    all_dds = [d for r in seeds_results for d in r["max_dds"]]
    return {
        "half_label": half_label,
        "window_start": str(h_panel.index.min().date()),
        "window_end": str(h_panel.index.max().date()),
        "n_bdays": len(h_panel),
        "n_blocks": len(blocks_h),
        "pass_rate": pass_r,
        "bust_rate": bust_r,
        "p99_dd": float(np.percentile(all_dds, 99)) if all_dds else float("nan"),
        "median_days_to_pass": int(np.median(all_days)) if all_days else None,
    }


def mode_boundary_sweep(dd_trigger: float, dd_scale: float,
                        panel_name: str | None = None,
                        parallel: bool = False,
                        boundary_dates: list | None = None,
                        allocations: Dict[str, float] | None = None) -> None:
    """Q-REGIME-1 boundary-date sweep at GA-4 fixed-1R swap-aware.

    For each pre-registered boundary date, slices the panel into H1 =
    [panel_start, boundary) and H2 = [boundary, panel_end], builds
    independent week-blocks per half, runs the canonical (SIMS_PER_SEED,
    SEEDS) MC at GA-4 + PRE_SHOCK_1R + swap-on, and emits a per-boundary
    row: {H1, H2} × {pass, bust, p99 DD, median} plus the verdict statistic
    `|H1 p99 DD − H2 p99 DD|`.

    This mode does NOT compute the verdict (mean/σ across the four non-
    2024-04-30 boundaries, z-score of 2024-04-30). That aggregation is
    Phase 4 of the Pre-Q and runs after pre-registration commits.

    Default-path byte-identity: this mode is reached only via --boundary-
    sweep; it does NOT alter default, --historical, --sensitivity, --swap,
    --fixed-1r, or --alloc-sweep paths.
    """
    if boundary_dates is None:
        boundary_dates = list(BOUNDARY_SWEEP_DATES)
    if allocations is None:
        allocations = dict(GA4_ALLOCATIONS)

    print("=== Portfolio MC — Q-REGIME-1 Boundary Sweep (fixed-1R swap-aware, GA-4) ===")
    print(f"Panel: {panel_name}")
    print(f"Protection: {_fmt_config(dd_trigger, dd_scale, no_protection=False)}")
    print(f"Swap: ON (FXIFY rates, Q-SWAP-1)")
    print(f"1R source: FIXED (pre-shock reference, Q-SWAP-2)")
    print(f"Allocations: {_fmt_alloc(allocations)}")
    pre_shock_str = " / ".join(f"{k}=${v:,.0f}" for k, v in PRE_SHOCK_1R.items())
    print(f"Pre-shock 1R: {pre_shock_str}")
    print(f"Sims: {SIMS_PER_SEED:,} × {len(SEEDS)} seeds per half, "
          f"inactivity {INACTIVITY_LIMIT}d / horizon-cap {HORIZON_CAP}d")
    print(f"Boundary dates ({len(boundary_dates)}): {', '.join(boundary_dates)}")
    print()

    # Load the full panel once at GA-4 + fixed-1R + swap-on. The same
    # daily panel feeds every boundary; only the H1/H2 row mask changes.
    trades_by_strat, panel, _blocks_full, scale_info, panel_strats = _load_all(
        allocations, panel_name=panel_name, apply_swap=True,
        fixed_1r_reference=PRE_SHOCK_1R,
    )
    fallback_count = sum(1 for info in scale_info.values() if info["fell_back"])
    assert_no_fallback(
        fallback_count,
        label="portfolio_mc implied_1r (Q-REGIME-1 boundary sweep)",
    )

    print(f"Panel ({panel_name}): {panel.index.min().date()} -> "
          f"{panel.index.max().date()}  "
          f"({len(panel)} bdays)")
    print("Scale factors (allocation-invariant pre-shock 1R):")
    for s, info in scale_info.items():
        print(f"  {s:<14} 1R=${info['implied_1r']:>7,.2f}  "
              f"scale={info['scale']:>6.3f}  n={info['n_trades']}")
    print()

    # Header
    print(f"{'Boundary':<12} {'H1 bdays':>9} {'H1 wb':>6} {'H1 pass':>8} "
          f"{'H1 bust':>8} {'H1 p99':>7} {'H1 med':>7}  "
          f"{'H2 bdays':>9} {'H2 wb':>6} {'H2 pass':>8} {'H2 bust':>8} "
          f"{'H2 p99':>7} {'H2 med':>7}  {'|spread|':>8}")
    print("-" * 142)

    rows: list = []
    for boundary in boundary_dates:
        ts = pd.Timestamp(boundary)
        h1_mask = panel.index < ts
        h2_mask = panel.index >= ts
        h1_panel = panel.loc[h1_mask]
        h2_panel = panel.loc[h2_mask]

        h1 = _run_half_panel("H1", h1_panel, dd_trigger, dd_scale,
                              parallel, panel_strats)
        h2 = _run_half_panel("H2", h2_panel, dd_trigger, dd_scale,
                              parallel, panel_strats)

        spread = abs(h1["p99_dd"] - h2["p99_dd"])
        rows.append({"boundary": boundary, "h1": h1, "h2": h2, "spread": spread})

        h1_med = h1["median_days_to_pass"] if h1["median_days_to_pass"] is not None else 9999
        h2_med = h2["median_days_to_pass"] if h2["median_days_to_pass"] is not None else 9999
        print(
            f"{boundary:<12} {h1['n_bdays']:>9} {h1['n_blocks']:>6} "
            f"{h1['pass_rate']:>8.2%} {h1['bust_rate']:>8.2%} "
            f"{h1['p99_dd']:>7.2%} {h1_med:>7}  "
            f"{h2['n_bdays']:>9} {h2['n_blocks']:>6} "
            f"{h2['pass_rate']:>8.2%} {h2['bust_rate']:>8.2%} "
            f"{h2['p99_dd']:>7.2%} {h2_med:>7}  "
            f"{spread*100:>7.2f}pp"
        )

    print()
    print("Spread statistic (|H1 p99 DD − H2 p99 DD|) by boundary, pp:")
    for r in rows:
        marker = "  <-- 2024-04-30 anchor (Q-SWAP-3 baseline)" if r["boundary"] == "2024-04-30" else ""
        print(f"  {r['boundary']}  {r['spread']*100:>5.2f}pp{marker}")
    print()

    # Q-SWAP-3 byte-identity check: 2024-04-30 row must reproduce
    # H1 p99 DD 4.90% / H2 3.81% / spread 1.09pp (within rounding).
    anchor_row = next((r for r in rows if r["boundary"] == "2024-04-30"), None)
    if anchor_row is not None:
        h1_p99 = anchor_row["h1"]["p99_dd"]
        h2_p99 = anchor_row["h2"]["p99_dd"]
        spread_pp = anchor_row["spread"] * 100.0
        anchor_match = (
            abs(h1_p99 - 0.0490) < 5e-4 and
            abs(h2_p99 - 0.0381) < 5e-4 and
            abs(spread_pp - 1.09) < 0.05
        )
        print(
            f"Q-SWAP-3 anchor reproduction (2024-04-30 row vs H1 4.90% / "
            f"H2 3.81% / spread 1.09pp): "
            f"{'HELD' if anchor_match else 'DRIFTED'}"
        )
        if not anchor_match:
            print(f"  Got: H1 p99 DD = {h1_p99:.4%}  "
                  f"H2 p99 DD = {h2_p99:.4%}  "
                  f"spread = {spread_pp:.2f}pp")

    print()
    print("Verdict aggregation (mean/σ of non-2024-04-30 boundaries; z-score of 2024-04-30) "
          "is NOT computed here — runs as Phase 4 closure step after pre-registration commits.")


# ── Q-SWAP-4 Phase 1 pine-shrink sweep ───────────────────────────────────

# Q-SWAP-4 Phase 1 pre-registered search space. Frozen at
# docs/briefs/pre-registration/Q-SWAP-4-phase-1-preregistration.md (commit
# cf64a26). Search-space expansion mid-execution is forbidden per pre-reg
# anti-p-hacking commitment #2.
#
# T_threshold ∈ {12, 13, 14, 15, 16} ET hours; entries with hour >= T_threshold
# qualify (when also held overnight across 17:00 ET rollover).
# shrink_factor ∈ {0.25, 0.50, 0.75, 1.00} — "fraction REMOVED" convention
# (pnl_modified = pnl_original × (1 - shrink_factor), and ditto for swap_cost).
PINE_SHRINK_T_THRESHOLDS: Tuple[int, ...] = (12, 13, 14, 15, 16)
PINE_SHRINK_FACTORS: Tuple[float, ...] = (0.25, 0.50, 0.75, 1.00)

# Canonical 2026-05-23 ADR allocations (pinned by pre-reg §"Reference anchor";
# every sweep cell runs at these allocations; only the Guardian pnl panel is
# modified per cell). Derived — same bytes as ALLOCATIONS / historical 4-leg book.
PINE_SHRINK_ALLOCATIONS: Dict[str, float] = dict(ALLOCATIONS)

# Phase 1 feasibility threshold (pre-reg §"Phase 1 verdict triggers"). A cell
# is FEASIBLE iff full-panel p99 DD < 4.50% under fixed-1R swap-aware MC at
# PINE_SHRINK_ALLOCATIONS using PRE_SHOCK_1R. (Phase 1 is feasibility only;
# bust and median are reported as diagnostics, not Phase 1 gates.)
_PINE_SHRINK_FEASIBILITY_P99_DD = 0.0450


def _load_guardian_with_shrink(path: Path, T_threshold: int,
                                shrink_factor: float) -> Tuple[pd.DataFrame, int]:
    """Load Guardian CSV and return (exit_date, pnl) panel with the Pine-shrink
    post-hoc modification applied.

    Strict pre-reg "overnight-hold-likely" definition (all three required):
      1. Entry hour (chart-TZ ET, from CSV `Date and time`) ≥ T_threshold
      2. Exit `Date and time` calendar date strictly > entry calendar date
      3. The 17:00 ET DXTrade rollover boundary fell between entry and exit
         (i.e. ``_count_rollovers(entry_dt, exit_dt) >= 1``)

    For each affected Trade #, both the Net P&L AND the per-trade swap cost
    are scaled by ``(1 - shrink_factor)``. This linearly approximates "smaller
    ATR-multiplier ⇒ smaller position size ⇒ proportionally smaller P&L and
    proportionally smaller swap cost" — the cheap-falsifier model (NOT a
    Pine-implementation stand-in; brief §5 forbidden-move #8).

    Returns (panel_df, affected_n) where panel_df has columns
    ['exit_date', 'pnl'] (swap already folded into pnl) and affected_n is
    the number of Guardian trades that satisfied the overnight-hold-likely
    filter (reported as a diagnostic; not a Phase 1 verdict gate).
    """
    df = pd.read_csv(path, encoding="utf-8-sig")
    assert_min_rows(len(df), 100, label=f"MC input panel {path.name}")

    df = df.copy()
    df["_dt"] = pd.to_datetime(df["Date and time"])
    entries = df[df["Type"].astype(str).str.startswith("Entry")]
    exits_full = df[df["Type"].astype(str).str.startswith("Exit")]

    # Per-Trade# swap cost (FXIFY rates; reuses Q-SWAP-1 helper).
    swap_df = _compute_per_trade_swap(df, "guardian")
    swap_map = dict(zip(swap_df["Trade #"].tolist(), swap_df["swap_cost"].tolist()))

    # Identify affected Trade #s by applying the three pre-reg conditions.
    affected_trade_ids: set = set()
    for tnum in entries["Trade #"].unique():
        e = entries[entries["Trade #"] == tnum]
        x = exits_full[exits_full["Type"].astype(str).str.startswith("Exit") &
                       (exits_full["Trade #"] == tnum)]
        if e.empty or x.empty:
            continue
        e_dt = e["_dt"].min()
        x_dt = x["_dt"].max()
        # Cond 1: entry hour ≥ T_threshold
        if e_dt.hour < T_threshold:
            continue
        # Cond 2: exit calendar date strictly > entry calendar date
        if x_dt.date() <= e_dt.date():
            continue
        # Cond 3: 17:00 ET rollover crossed
        if _count_rollovers(e_dt, x_dt) < 1:
            continue
        affected_trade_ids.add(tnum)

    # Build the exit-row panel with swap folded in (mirrors load_trades(apply_swap=True)).
    exits = exits_full.copy()
    exits["exit_date"] = pd.to_datetime(exits["Date and time"]).dt.normalize()
    exits = exits.rename(columns={"Net P&L USD": "pnl"})
    exits["swap_cost"] = exits["Trade #"].map(swap_map).fillna(0.0)
    # Apply shrink: affected trades scale both pnl AND swap by (1 - shrink_factor).
    factor = exits["Trade #"].apply(
        lambda t: (1.0 - shrink_factor) if t in affected_trade_ids else 1.0
    )
    exits["pnl"] = (exits["pnl"] + exits["swap_cost"]) * factor

    out = exits[["exit_date", "pnl"]].sort_values("exit_date").reset_index(drop=True)
    if not out.empty:
        assert_window(
            out["exit_date"].iloc[0].to_pydatetime(),
            out["exit_date"].iloc[-1].to_pydatetime(),
            expected_min_days=4 * 365,
            label=f"MC input panel {path.name}",
            tolerance_days=100,
        )
    return out, len(affected_trade_ids)


def _load_all_with_pine_shrink(allocs: Dict[str, float], panel_name: str,
                                 T_threshold: int, shrink_factor: float):
    """Variant of ``_load_all`` that substitutes a Pine-shrink-modified Guardian
    panel; Striker/Aegis/NAS100 load canonically with apply_swap=True.

    Returns (trades_by_strat, panel, blocks, scale_info, panel_strats, affected_n).
    """
    panels = PANELS_BY_BROKER[panel_name]
    expected_broker = panel_name.upper()
    expected_symbols = EXPECTED_SYMBOLS_BY_BROKER[panel_name]
    expected_versions = EXPECTED_VERSIONS_BY_BROKER[panel_name]
    panel_strats = tuple(panels.keys())
    for s in panel_strats:
        assert_tv_export(
            panels[s],
            expected_strategy=STRATEGY_FILENAME_TOKEN[s],
            expected_version=expected_versions[s],
            expected_broker=expected_broker,
            expected_symbol=expected_symbols[s],
        )

    trades_by_strat: Dict[str, pd.DataFrame] = {}
    affected_n = 0
    for s in panel_strats:
        if s == "guardian":
            gp, affected_n = _load_guardian_with_shrink(
                panels[s], T_threshold=T_threshold, shrink_factor=shrink_factor,
            )
            trades_by_strat[s] = gp
        else:
            trades_by_strat[s] = load_trades(panels[s], strategy=s, apply_swap=True)

    panel_allocs = {s: allocs[s] for s in panel_strats}
    panel, scale_info = build_daily_panel(
        trades_by_strat, panel_allocs,
        fixed_1r_reference=PRE_SHOCK_1R,
    )
    blocks = build_week_blocks(panel)
    return trades_by_strat, panel, blocks, scale_info, panel_strats, affected_n


def _run_pine_shrink_cell(T_threshold: int, shrink_factor: float,
                            dd_trigger: float, dd_scale: float,
                            panel_name: str, parallel: bool) -> dict:
    """Run a single (T_threshold, shrink_factor) sweep cell under fixed-1R
    swap-aware MC at PINE_SHRINK_ALLOCATIONS with PRE_SHOCK_1R pinned.
    """
    trades_by_strat, panel, blocks, scale_info, panel_strats, affected_n = (
        _load_all_with_pine_shrink(
            PINE_SHRINK_ALLOCATIONS, panel_name=panel_name,
            T_threshold=T_threshold, shrink_factor=shrink_factor,
        )
    )
    # fell_back is always False under fixed-1R; no assert_no_fallback call
    # needed (mirrors compute_default_config under fixed_1r_reference).
    seeds_results = _run_seeds(blocks, dd_trigger, dd_scale,
                                parallel=parallel, strats=panel_strats)
    per_seed = SIMS_PER_SEED
    pass_r = float(np.mean([r["outcomes"]["pass"] / per_seed for r in seeds_results]))
    bd_r = float(np.mean([r["outcomes"]["bust_daily"] / per_seed for r in seeds_results]))
    bs_r = float(np.mean([r["outcomes"]["bust_static"] / per_seed for r in seeds_results]))
    bust_r = bd_r + bs_r
    all_days = [d for r in seeds_results for d in r["days_to_pass"]]
    all_dds = [d for r in seeds_results for d in r["max_dds"]]
    p99 = float(np.percentile(all_dds, 99)) if all_dds else float("nan")
    median = int(np.median(all_days)) if all_days else None
    return {
        "T": T_threshold,
        "shrink": shrink_factor,
        "affected_n": affected_n,
        "pass_rate": pass_r,
        "bust_rate": bust_r,
        "bust_daily_rate": bd_r,
        "bust_static_rate": bs_r,
        "p99_dd": p99,
        "median_days_to_pass": median,
        "scale_guardian": float(scale_info["guardian"]["scale"]),
    }


def mode_pine_shrink_sweep(dd_trigger: float, dd_scale: float,
                            panel_name: str | None = None,
                            parallel: bool = False) -> None:
    """Q-SWAP-4 Phase 1 cheap-falsifier sweep.

    For each (T_threshold, shrink_factor) cell in the 20-cell pre-registered
    grid (PINE_SHRINK_T_THRESHOLDS × PINE_SHRINK_FACTORS), runs fixed-1R
    swap-aware Pepperstone MC at PINE_SHRINK_ALLOCATIONS with PRE_SHOCK_1R
    pinned, using a Guardian panel where overnight-hold-likely trades have
    both pnl and swap_cost scaled by (1 - shrink_factor).

    Adds a REG row (shrink=0 ⇒ unmodified Guardian) for byte-identity gating
    against Q-SWAP-2 fixed-1R Pepperstone canonical (99.80/0.20/4.55/27).

    Phase 1 verdict is FEASIBILITY ONLY (binary p99 DD < 4.50%); bust and
    median are reported as diagnostics. Cell-level FEASIBLE flag emitted per
    pre-reg §"Phase 1 verdict triggers". Whole-investigation FEASIBLE/INFEASIBLE
    verdict is NOT computed here — pre-reg disposition rule routes to Joshua
    for greenlight on a specific (T*, shrink*) candidate.
    """
    print("=== Portfolio MC — Q-SWAP-4 Phase 1 Pine-Shrink Sweep (fixed-1R swap-aware) ===")
    print(f"Panel: {panel_name}")
    print(f"Protection: {_fmt_config(dd_trigger, dd_scale, no_protection=False)}")
    print(f"Swap: ON (FXIFY rates, Q-SWAP-1)")
    print(f"1R source: FIXED (pre-shock reference, Q-SWAP-2)")
    print(f"Allocations: {_fmt_alloc(PINE_SHRINK_ALLOCATIONS)}")
    pre_shock_str = " / ".join(f"{k}=${v:,.0f}" for k, v in PRE_SHOCK_1R.items())
    print(f"Pre-shock 1R: {pre_shock_str}")
    print(f"Sims: {SIMS_PER_SEED:,} × {len(SEEDS)} seeds per cell, "
          f"inactivity {INACTIVITY_LIMIT}d / horizon-cap {HORIZON_CAP}d")
    print(f"T_threshold (ET): {list(PINE_SHRINK_T_THRESHOLDS)}")
    print(f"shrink_factor: {list(PINE_SHRINK_FACTORS)} (fraction REMOVED)")
    print(f"Phase 1 feasibility gate: p99 DD < {_PINE_SHRINK_FEASIBILITY_P99_DD:.2%}  "
          f"(bust and median reported as diagnostics, NOT Phase 1 gates)")
    print()

    # REG row: shrink_factor=0 on any T_threshold yields zero modification.
    # We choose T_threshold=12 (smallest in grid) for the REG row so the
    # affected-trade count reflects the most-permissive overnight-hold filter
    # (diagnostic only; the modification factor is identically 1.0).
    print("Running REG (shrink=0, no modification) for regression byte-identity check ...")
    reg = _run_pine_shrink_cell(
        T_threshold=12, shrink_factor=0.0,
        dd_trigger=dd_trigger, dd_scale=dd_scale,
        panel_name=panel_name, parallel=parallel,
    )

    # Run the 20 sweep cells in deterministic order.
    cells: list = []
    total_cells = len(PINE_SHRINK_T_THRESHOLDS) * len(PINE_SHRINK_FACTORS)
    print(f"Running {total_cells} sweep cells ...")
    for T in PINE_SHRINK_T_THRESHOLDS:
        for sh in PINE_SHRINK_FACTORS:
            cell_id = f"T{T}-S{int(sh*100):03d}"
            res = _run_pine_shrink_cell(
                T_threshold=T, shrink_factor=sh,
                dd_trigger=dd_trigger, dd_scale=dd_scale,
                panel_name=panel_name, parallel=parallel,
            )
            res["cell_id"] = cell_id
            cells.append(res)

    # ── Output table ────────────────────────────────────────────────────
    print()
    print(f"{'Cell':<10} {'T':>3} {'shrink':>7} {'aff_n':>5} {'Pass':>7} {'Bust':>7} "
          f"{'Daily':>7} {'Static':>7} {'p99 DD':>8} {'Median':>7} {'Scale_G':>8}  FEASIBLE")
    print("-" * 100)

    # REG row first
    reg_feasible = reg["p99_dd"] < _PINE_SHRINK_FEASIBILITY_P99_DD
    reg_median = reg["median_days_to_pass"] if reg["median_days_to_pass"] is not None else 9999
    print(
        f"{'REG':<10} {reg['T']:>3} {reg['shrink']:>7.2f} {reg['affected_n']:>5} "
        f"{reg['pass_rate']:>7.2%} {reg['bust_rate']:>7.2%} "
        f"{reg['bust_daily_rate']:>7.2%} {reg['bust_static_rate']:>7.2%} "
        f"{reg['p99_dd']:>8.2%} {reg_median:>7} {reg['scale_guardian']:>8.3f}  "
        f"{'Y' if reg_feasible else 'N'}"
    )

    feasible_cells: list = []
    for c in cells:
        feasible = c["p99_dd"] < _PINE_SHRINK_FEASIBILITY_P99_DD
        if feasible:
            feasible_cells.append(c)
        med = c["median_days_to_pass"] if c["median_days_to_pass"] is not None else 9999
        print(
            f"{c['cell_id']:<10} {c['T']:>3} {c['shrink']:>7.2f} {c['affected_n']:>5} "
            f"{c['pass_rate']:>7.2%} {c['bust_rate']:>7.2%} "
            f"{c['bust_daily_rate']:>7.2%} {c['bust_static_rate']:>7.2%} "
            f"{c['p99_dd']:>8.2%} {med:>7} {c['scale_guardian']:>8.3f}  "
            f"{'Y' if feasible else 'N'}"
        )

    print()

    # ── REG byte-identity gate vs Q-SWAP-2 fixed-1R Pepperstone canonical ──
    reg_match = (
        abs(reg["pass_rate"] - 0.9980) < 1e-4 and
        abs(reg["bust_rate"] - 0.0020) < 1e-4 and
        abs(reg["p99_dd"]    - 0.0455) < 1e-4 and
        reg["median_days_to_pass"] == 27
    )
    print(f"REG regression sanity vs Q-SWAP-2 fixed-1R Pepperstone canonical "
          f"(99.80/0.20/4.55, median 27): "
          f"{'HELD' if reg_match else 'DRIFTED'}")
    if not reg_match:
        print(f"  Got: pass={reg['pass_rate']:.4%} bust={reg['bust_rate']:.4%} "
              f"p99={reg['p99_dd']:.4%} median={reg['median_days_to_pass']}")

    print()

    # ── Phase 1 disposition rule (pre-reg §"Disposition selection rule") ──
    # Among FEASIBLE cells, the LEAST-aggressive shrink at the LATEST
    # T_threshold is the "minimum-intervention candidate". Surface near-ties
    # (within 0.05pp p99 DD margin of each other at the conservative end) as
    # DONE_WITH_CONCERNS.
    print(f"FEASIBLE cells (p99 DD < {_PINE_SHRINK_FEASIBILITY_P99_DD:.2%}): "
          f"{len(feasible_cells)} / {total_cells}")
    if feasible_cells:
        # Sort by (latest T desc, smallest shrink asc) — pre-reg conservative end.
        ranked = sorted(feasible_cells, key=lambda c: (-c["T"], c["shrink"]))
        mic = ranked[0]
        print(f"  Minimum-intervention candidate (largest T, smallest shrink): "
              f"{mic['cell_id']} "
              f"(T={mic['T']}, shrink={mic['shrink']:.2f}, "
              f"p99 DD={mic['p99_dd']:.2%}, affected_n={mic['affected_n']})")

        # Near-tie detection: any FEASIBLE cell with p99 DD within 0.05pp of MIC's.
        mic_p99 = mic["p99_dd"]
        ties = [c for c in feasible_cells
                if abs(c["p99_dd"] - mic_p99) < 0.0005 and c["cell_id"] != mic["cell_id"]]
        if ties:
            print(f"  DONE_WITH_CONCERNS — {len(ties)} FEASIBLE cell(s) within "
                  f"0.05pp p99 DD of minimum-intervention candidate:")
            for t in ties:
                print(f"    {t['cell_id']} (T={t['T']}, shrink={t['shrink']:.2f}, "
                      f"p99 DD={t['p99_dd']:.2%}, affected_n={t['affected_n']})")
    else:
        print("  No FEASIBLE cells — Phase 1 INFEASIBLE candidate per pre-reg "
              "§'Phase 1 verdict triggers'. Joshua reviews per disposition rule.")

    # Diagnostic: low-affected-trade cells (<10 trades) are DONE_WITH_CONCERNS.
    low_n_cells = [c for c in cells if c["affected_n"] < 10]
    if low_n_cells:
        print()
        print(f"DONE_WITH_CONCERNS — {len(low_n_cells)} cell(s) with affected_n < 10 "
              f"(thin sample; cheap-falsifier signal-to-noise concern):")
        for c in low_n_cells:
            print(f"  {c['cell_id']} affected_n={c['affected_n']}  p99 DD={c['p99_dd']:.2%}")

    print()
    print("VERDICT (Phase 1, provisional): Per-cell FEASIBLE flags above. "
          "Whole-investigation FEASIBLE/INFEASIBLE call is Joshua's review per "
          "pre-reg §'Disposition selection rule' — NOT auto-decided.")


# ── Entry ─────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(
        prog="portfolio_mc",
        description=(
            "Parameterized challenge-outcome simulator. Pepperstone default "
            "retired; --panel cme is registered for breadth only and is not a "
            "working 4-leg MC re-run. Engine correctness is synthetic-fixture "
            "gated."
        ),
    )
    p.add_argument("--dd-trigger", type=float, default=DD_TRIGGER,
                   help=f"DD trigger (default {DD_TRIGGER} from dd_protection.py)")
    p.add_argument("--dd-scale", type=float, default=DD_SCALE,
                   help=f"DD scale (default {DD_SCALE} from dd_protection.py)")
    p.add_argument("--no-protection", action="store_true",
                   help="Run without DD protection")
    p.add_argument("--historical", action="store_true",
                   help="Deterministic walk through the historical panel")
    p.add_argument("--sensitivity", action="store_true",
                   help="DD-trigger sensitivity grid")
    p.add_argument("--guardian-risk", type=float, default=None,
                   help="Override Guardian allocation for what-if MC (e.g. 0.0025 to simulate a reduced-risk overlay)")
    _panel_choices = list(PANELS_BY_BROKER.keys())
    if _panel_choices:
        p.add_argument(
            "--panel", choices=_panel_choices, required=True,
            help="Registered broker panel to load",
        )
    else:
        p.add_argument(
            "--panel", default=None,
            help="No registered panels (Pepperstone executable anchor retired)",
        )
    p.add_argument("--parallel", action="store_true",
                   help="Parallelize seed loop with joblib (faster on multi-core; default: sequential).")
    p.add_argument("--swap", action="store_true",
                   help="Apply FXIFY DXTrade overnight swap rates to each trade before MC (Q-SWAP-1 Phase 3). "
                        "Default OFF preserves the 2026-05-23 anchor byte-identically.")
    p.add_argument("--fixed-1r", dest="fixed_1r", nargs="+", default=None, metavar="STRAT=VALUE",
                   help="Q-SWAP-2: hold implied_1r fixed at the supplied per-strategy reference values "
                        "(USD per 1R) instead of recalibrating from the panel's loss distribution. "
                        "Format: --fixed-1r guardian=1208 striker=4229 aegis=3293 nas100=3940 "
                        "(nas100 is an accepted alias for the panel key striker_nas100). "
                        "Keys must match the loaded panel's strategy set; missing/extra keys hard-fail. "
                        "REQUIRES --swap (fixed-1R without swap is the swap-OFF anchor by construction).")
    p.add_argument("--alloc-sweep", action="store_true",
                   help="Q-SWAP-3: run the pre-registered 8-config allocation search space under "
                        "fixed-1R swap-aware MC. Internally sets apply_swap=True and uses the "
                        "canonical PRE_SHOCK_1R reference; --swap and --fixed-1r are NOT required "
                        "(they are implicit in the sweep design) and are mutually exclusive with "
                        "this flag along with --historical and --sensitivity.")
    p.add_argument("--boundary-sweep", action="store_true",
                   help="Q-REGIME-1: run the pre-registered 5-boundary-date sweep under fixed-1R "
                        "swap-aware MC. For each boundary date, slices the panel into H1 = "
                        "[panel_start, boundary) and H2 = [boundary, panel_end] and runs the "
                        "canonical MC at GA-4 allocations (requires --ga4 to make the allocation "
                        "explicit). Emits per-boundary {H1, H2} × {pass, bust, p99 DD, median} "
                        "and the verdict statistic |H1 p99 DD − H2 p99 DD|. Mutually exclusive "
                        "with --alloc-sweep, --historical, --sensitivity, --fixed-1r, --swap.")
    p.add_argument("--ga4", action="store_true",
                   help="Q-REGIME-1: apply GA-4 allocations (Guardian 0.24%% / DJ30 0.70%% / "
                        "Aegis 1.50%% / NAS100 0.37%%). Required as an explicit acknowledgement "
                        "of the verdict-input config when --boundary-sweep is set; the brief's "
                        "section 5 forbidden-move-4 pins GA-4 as the only permitted allocation "
                        "for the boundary sweep, so the flag must be explicit.")
    p.add_argument("--pine-shrink-sweep", dest="pine_shrink_sweep", action="store_true",
                   help="Q-SWAP-4 Phase 1: run the pre-registered 20-cell (T, shrink) cheap-"
                        "falsifier sweep under fixed-1R swap-aware MC at canonical 2026-05-23 "
                        "ADR allocations with PRE_SHOCK_1R pinned. Modifies the Guardian panel "
                        "post-hoc by scaling overnight-hold-likely trades' pnl and swap_cost by "
                        "(1 - shrink_factor). Mutually exclusive with --alloc-sweep, "
                        "--boundary-sweep, --historical, --sensitivity, --fixed-1r, --swap.")
    args = p.parse_args()

    if not PANELS_BY_BROKER:
        raise SystemExit(
            "portfolio_mc CLI: no registered broker panel. "
            "Pepperstone executable anchor retired 2026-07-24 "
            "(docs/adr/2026-07-22-challenge-era-substrate-retirement.md "
            "section 7 Phase 3). "
            "Engine correctness: pytest tests/core/test_mc_synthetic_engine.py "
            "tests/core/test_planted_defects.py"
        )

    # Q-SWAP-3: --alloc-sweep is mutually exclusive with other modes / flags.
    if args.alloc_sweep:
        conflicts = []
        if args.fixed_1r is not None:
            conflicts.append("--fixed-1r")
        if args.historical:
            conflicts.append("--historical")
        if args.sensitivity:
            conflicts.append("--sensitivity")
        if args.boundary_sweep:
            conflicts.append("--boundary-sweep")
        if conflicts:
            p.error(f"--alloc-sweep is mutually exclusive with: {', '.join(conflicts)}. "
                    f"The sweep mode internally uses fixed-1R + swap-aware MC against the "
                    f"pre-registered 8-config search space; it is structurally distinct from "
                    f"the other modes.")

    # Q-REGIME-1: --boundary-sweep is mutually exclusive with other modes / flags
    # and REQUIRES --ga4 (to make the allocation-config decision explicit per
    # brief §5 forbidden-move-4).
    if args.boundary_sweep:
        conflicts = []
        if args.fixed_1r is not None:
            conflicts.append("--fixed-1r")
        if args.swap:
            conflicts.append("--swap (implicit in boundary-sweep mode)")
        if args.historical:
            conflicts.append("--historical")
        if args.sensitivity:
            conflicts.append("--sensitivity")
        if args.alloc_sweep:
            conflicts.append("--alloc-sweep")
        if args.pine_shrink_sweep:
            conflicts.append("--pine-shrink-sweep")
        if conflicts:
            p.error(f"--boundary-sweep is mutually exclusive with: {', '.join(conflicts)}. "
                    f"The boundary-sweep mode internally uses fixed-1R + swap-aware MC at GA-4 "
                    f"allocations; it is structurally distinct from the other modes.")
        if not args.ga4:
            p.error("--boundary-sweep requires --ga4. The brief's §5 forbidden-move-4 pins GA-4 "
                    "as the only permitted allocation config for this sweep; the flag must be "
                    "explicit to acknowledge the verdict-input config.")

    # Q-SWAP-4: --pine-shrink-sweep is mutually exclusive with other modes/flags.
    if args.pine_shrink_sweep:
        conflicts = []
        if args.fixed_1r is not None:
            conflicts.append("--fixed-1r")
        if args.swap:
            conflicts.append("--swap (implicit in pine-shrink-sweep mode)")
        if args.historical:
            conflicts.append("--historical")
        if args.sensitivity:
            conflicts.append("--sensitivity")
        if args.alloc_sweep:
            conflicts.append("--alloc-sweep")
        if args.boundary_sweep:
            conflicts.append("--boundary-sweep")
        if conflicts:
            p.error(f"--pine-shrink-sweep is mutually exclusive with: {', '.join(conflicts)}. "
                    f"The pine-shrink-sweep mode internally uses fixed-1R + swap-aware MC at "
                    f"canonical 2026-05-23 ADR allocations with PRE_SHOCK_1R pinned; it is "
                    f"structurally distinct from the other modes.")

    allocs = dict(ALLOCATIONS)
    if args.guardian_risk is not None:
        allocs["guardian"] = args.guardian_risk

    fixed_1r_reference: Dict[str, float] | None = None
    if args.fixed_1r is not None:
        if not args.swap:
            p.error("--fixed-1r requires --swap. Fixed-1R modeling without swap is the "
                    "swap-OFF anchor by construction; the combination is the Q-SWAP-2 verdict run.")
        fixed_1r_reference = {}
        # CLI alias: 'nas100' maps to the panel key 'striker_nas100'. The handoff
        # brief's audit-hook CLI uses 'nas100' for brevity; the panel internally
        # carries the longer key. No other aliases — strict parity beyond that.
        ALIAS = {"nas100": "striker_nas100"}
        for pair in args.fixed_1r:
            if "=" not in pair:
                p.error(f"--fixed-1r entry '{pair}' missing '='. Use form STRAT=VALUE "
                        f"(e.g. guardian=1208).")
            key, _, raw_value = pair.partition("=")
            key = key.strip()
            try:
                value = float(raw_value)
            except ValueError:
                p.error(f"--fixed-1r entry '{pair}' has non-numeric value '{raw_value}'.")
            if value <= 0:
                p.error(f"--fixed-1r entry '{pair}' has non-positive value {value}; "
                        f"1R reference must be > 0.")
            key = ALIAS.get(key, key)
            if key in fixed_1r_reference:
                p.error(f"--fixed-1r duplicate key '{key}'.")
            fixed_1r_reference[key] = value

    if args.alloc_sweep:
        mode_alloc_sweep(args.dd_trigger, args.dd_scale, panel_name=args.panel,
                         parallel=args.parallel)
    elif args.boundary_sweep:
        mode_boundary_sweep(args.dd_trigger, args.dd_scale, panel_name=args.panel,
                            parallel=args.parallel)
    elif args.pine_shrink_sweep:
        mode_pine_shrink_sweep(args.dd_trigger, args.dd_scale, panel_name=args.panel,
                                parallel=args.parallel)
    elif args.sensitivity:
        mode_sensitivity(args.dd_scale, allocs, panel_name=args.panel, parallel=args.parallel)
    elif args.historical:
        mode_historical(args.dd_trigger, args.dd_scale, args.no_protection, allocs, panel_name=args.panel)
    else:
        mode_default(args.dd_trigger, args.dd_scale, args.no_protection, allocs,
                     panel_name=args.panel, parallel=args.parallel,
                     apply_swap=args.swap,
                     fixed_1r_reference=fixed_1r_reference)


if __name__ == "__main__":
    main()
