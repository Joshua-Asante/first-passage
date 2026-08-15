"""Call-1 rolling-PF σ-harness + tier-demotion state writer.

Build-ahead-of-data: there are no live fills. Callers supply ``rolling_pf`` /
``trade_count``; thin or missing data → AMBIGUOUS (never a fabricated demotion).

Imports ``core.lifecycle`` read-only. Writes ``lifecycle_state.json`` (gitignored
runtime state) only on a confirmed 2nd consecutive breach via
``autonomous_demote``. Consecutive-breach counters live in a separate
harness-owned file — never widen the ``{strategy: tier}`` schema.

Canonical owner: ``docs/methodology/strategy_lifecycle.md`` Call 1.
Handoff: ``docs/briefs/rnd-pipeline/2026-07-14-cursor-handoff-lifecycle-call1-sigma-harness.md``.
"""
from __future__ import annotations

from .baselines import (
    DEFAULT_BASELINES_PATH,
    BaselineDataUnavailable,
    BaselinePF,
    load_baseline_pfs,
)
from .breach_tracker import (
    DEFAULT_BREACH_STATE_PATH,
    load_breach_state,
    save_breach_state,
    update_consecutive,
)
from .demote_writer import apply_confirmed_demotion
from .evaluate import MIN_TRADE_COUNT, WindowOutcome, evaluate_window
from .harness import Call1StrategyReport, run_call1_harness
from .pf_sigma import pf_from_daily_pnl, pf_sigma_from_panel

__all__ = [
    "DEFAULT_BASELINES_PATH",
    "DEFAULT_BREACH_STATE_PATH",
    "MIN_TRADE_COUNT",
    "BaselineDataUnavailable",
    "BaselinePF",
    "Call1StrategyReport",
    "WindowOutcome",
    "apply_confirmed_demotion",
    "evaluate_window",
    "load_baseline_pfs",
    "load_breach_state",
    "pf_from_daily_pnl",
    "pf_sigma_from_panel",
    "run_call1_harness",
    "save_breach_state",
    "update_consecutive",
]
