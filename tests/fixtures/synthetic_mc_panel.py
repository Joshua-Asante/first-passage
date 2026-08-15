"""Committed synthetic MC panel — vendor-free engine-correctness fixture.

ADR 2026-07-22 §2-C / §7 Phase 1: replaces the Pepperstone anchor's *engine*
role with deterministic trade tables that exercise implied_1r cohort
selection, week-block construction, all six outcome buckets (incl.
bust_inactivity), and firm_kwargs threading — no vendor bytes.
"""

from __future__ import annotations

from typing import Dict, Tuple

import numpy as np
import pandas as pd

STRATS: Tuple[str, ...] = ("guardian", "striker", "aegis", "striker_nas100")
DEFAULT_SEED = 20260722
DEFAULT_START = "2022-01-03"
DEFAULT_N_BDAYS = 1141  # matches Pepperstone panel cardinality (pin shape)
ACCOUNT_BASIS = 200_000.0
FULL_STOP_FLOOR = 0.01 * ACCOUNT_BASIS  # $2,000 — ingest cohort selector


def make_synthetic_trades(
    seed: int = DEFAULT_SEED,
    strats: Tuple[str, ...] = STRATS,
    start: str = DEFAULT_START,
    n_bdays: int = DEFAULT_N_BDAYS,
) -> Dict[str, pd.DataFrame]:
    """Deterministic per-strategy trade tables (exit_date, pnl).

    Hard properties (each backs a pin):
    - Non-Guardian legs have ≥5 full-stop losses (> 0.01 * basis) so
      implied_1r's cohort selector is live and fell_back is False.
    - Guardian has a distinct median-vs-mean loss profile (early-return path).
    - Coverage is Monday-anchored over n_bdays so week-block counts pin.
    - Long idle stretches leave all-zero Mon-anchored weeks in the panel so
      bootstrap can produce bust_inactivity > 0.
    """
    rng = np.random.default_rng(seed)
    bdays = pd.bdate_range(start, periods=n_bdays)
    trades: Dict[str, pd.DataFrame] = {}

    for strat_i, strategy in enumerate(strats):
        rows: list[dict] = []
        # Active windows: ~every 3rd week has trades; other weeks stay idle
        # so build_week_blocks yields a non-trivial zero-block population.
        for week_start in range(0, n_bdays - 4, 5):
            if (week_start // 5 + strat_i) % 3 != 0:
                continue
            day = bdays[week_start + int(rng.integers(0, 5))]
            # Full-stop losses (cohort selector input) — ≥5 per non-Guardian.
            if strategy == "guardian":
                # Median path: mix of small and large losses; mean ≠ median.
                loss = float(rng.choice([800.0, 900.0, 1100.0, 5000.0]))
                rows.append({"exit_date": day, "pnl": -loss})
                if rng.random() < 0.55:
                    rows.append(
                        {
                            "exit_date": day + pd.Timedelta(days=1),
                            "pnl": float(rng.uniform(1500.0, 4000.0)),
                        }
                    )
            else:
                # Deterministic full stops + winners; strat_i shifts magnitudes.
                base_stop = FULL_STOP_FLOOR + 500.0 * (strat_i + 1)
                rows.append({"exit_date": day, "pnl": -base_stop})
                if rng.random() < 0.6:
                    rows.append(
                        {
                            "exit_date": day,
                            "pnl": float(base_stop * rng.uniform(1.2, 2.5)),
                        }
                    )
                # Sub-threshold noise so the 0.01*account selector is meaningful.
                if rng.random() < 0.4:
                    rows.append(
                        {
                            "exit_date": day + pd.Timedelta(days=2),
                            "pnl": -float(rng.uniform(50.0, 500.0)),
                        }
                    )

        # Guarantee ≥5 full stops for non-Guardian even on unlucky seeds.
        if strategy != "guardian":
            full_stops = [
                r for r in rows if r["pnl"] < 0 and abs(r["pnl"]) > FULL_STOP_FLOOR
            ]
            while len(full_stops) < 5:
                day = bdays[int(rng.integers(0, n_bdays))]
                row = {
                    "exit_date": day,
                    "pnl": -(FULL_STOP_FLOOR + 1000.0 + 100.0 * len(full_stops)),
                }
                rows.append(row)
                full_stops.append(row)

        df = pd.DataFrame(rows)
        if df.empty:
            raise RuntimeError(f"synthetic trades empty for {strategy}")
        df["exit_date"] = pd.to_datetime(df["exit_date"]).dt.normalize()
        trades[strategy] = df.sort_values("exit_date").reset_index(drop=True)

    return trades


def make_synthetic_panel(
    allocations: Dict[str, float],
    *,
    seed: int = DEFAULT_SEED,
    account_basis: float | None = None,
    force_idle_weeks: bool = True,
    force_daily_bust_days: bool = True,
):
    """Build (trades, panel, blocks, scale_info) via production ingest helpers.

    ``force_idle_weeks`` zeros every 4th Mon-anchored week so ``build_week_blocks``
    yields a non-empty zero-block population — required for non-zero
    ``bust_inactivity`` under the historical 60-day limit.

    ``force_daily_bust_days`` plants a few −6% single-day portfolio losses so
    ``bust_daily`` is reachable under the historical −5% daily-loss rule.
    """
    from mc.ingest import build_daily_panel, build_week_blocks

    trades = make_synthetic_trades(seed=seed)
    panel, scale_info = build_daily_panel(
        trades, allocations, account_basis=account_basis
    )

    if force_idle_weeks or force_daily_bust_days:
        values = panel.values.copy()
        n_strats = values.shape[1]
        if force_idle_weeks:
            for index, day in enumerate(panel.index):
                if day.weekday() == 0 and index + 5 <= len(panel):
                    week_i = index // 5
                    # Keep ~1/5 of weeks live so zero-block density ≈ 0.8 —
                    # required for random bootstrap to reach 60 consecutive
                    # idle days with non-trivial frequency (p^12 under p≈0.8).
                    if week_i % 5 != 1:
                        values[index:index + 5, :] = 0.0
        if force_daily_bust_days:
            # Plant three −6% of basis days (well past the −5% daily-loss gate).
            basis = ACCOUNT_BASIS if account_basis is None else account_basis
            loss_per_strat = -0.06 * basis / n_strats
            for idx in (50, 250, 500):
                if idx < len(values):
                    values[idx, :] = loss_per_strat
        panel = panel.copy()
        panel.iloc[:, :] = values

    blocks = build_week_blocks(panel)
    return trades, panel, blocks, scale_info
