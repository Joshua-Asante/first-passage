"""Top-level Call-1 driver — baselines → σ → evaluate → track → demote → report."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Mapping

import numpy as np

try:
    from lifecycle import DEFAULT_TIER, STATE_FILE, STRATEGY_KEYS, load_lifecycle_state
except ImportError:  # pragma: no cover
    from core.lifecycle import DEFAULT_TIER, STATE_FILE, STRATEGY_KEYS, load_lifecycle_state

from .baselines import DEFAULT_BASELINES_PATH, load_baseline_pfs
from .breach_tracker import (
    DEFAULT_BREACH_STATE_PATH,
    load_breach_state,
    save_breach_state,
    update_consecutive,
)
from .demote_writer import apply_confirmed_demotion
from .evaluate import MIN_TRADE_COUNT, MIN_TRADE_COUNT_NOTE, evaluate_window
from .pf_sigma import pf_sigma_from_panel

DEMOTION_THRESHOLD = 2  # ratified consecutive count (strategy_lifecycle.md Call 1)


@dataclass
class StrategyInput:
    rolling_pf: float | None
    trade_count: int


@dataclass
class Call1StrategyReport:
    rolling_pf: float | None
    baseline_pf: float
    pf_sigma: float
    floor: float | None
    breached: bool
    consecutive_count: int
    window_result: str
    tier_before: str
    tier_after: str
    demoted: bool
    trade_count: int
    baseline_provenance: dict
    pf_sigma_provenance: dict
    ambiguous_reason: str | None = None


@dataclass
class Call1Report:
    strategies: dict[str, Call1StrategyReport] = field(default_factory=dict)
    state_file_written: bool = False
    lifecycle_state_delta: dict[str, str] = field(default_factory=dict)
    breach_state_path: str = ""
    lifecycle_state_path: str = ""
    min_trade_count: int = MIN_TRADE_COUNT
    min_trade_count_note: str = MIN_TRADE_COUNT_NOTE

    def to_dict(self) -> dict:
        return {
            "strategies": {k: asdict(v) for k, v in self.strategies.items()},
            "state_file_written": self.state_file_written,
            "lifecycle_state_delta": dict(self.lifecycle_state_delta),
            "breach_state_path": self.breach_state_path,
            "lifecycle_state_path": self.lifecycle_state_path,
            "min_trade_count": self.min_trade_count,
            "min_trade_count_note": self.min_trade_count_note,
        }


def _tier_map(lifecycle_path: Path) -> dict[str, str]:
    if lifecycle_path == Path(STATE_FILE):
        state = load_lifecycle_state()
    elif lifecycle_path.exists():
        raw = json.loads(lifecycle_path.read_text(encoding="utf-8"))
        state = {str(k): str(v) for k, v in raw.items()} if isinstance(raw, dict) else {}
    else:
        state = {}
    return {k: state.get(k, DEFAULT_TIER) for k in STRATEGY_KEYS}


def run_call1_harness(
    inputs: Mapping[str, StrategyInput | Mapping],
    panel_by_strategy: Mapping[str, np.ndarray],
    *,
    n_draws: int,
    seed: int,
    baselines_path: Path | None = None,
    breach_state_path: Path | None = None,
    lifecycle_state_path: Path | None = None,
    blocks_per_draw: int | None = None,
    min_trade_count: int = MIN_TRADE_COUNT,
) -> Call1Report:
    """Run one Call-1 review window across strategies.

    ``inputs`` keys must be a subset of STRATEGY_KEYS. Strategies omitted from
    ``inputs`` are skipped (not evaluated). ``panel_by_strategy`` supplies the
    synthetic/real week-block panel used only for ``pf_sigma`` (not live PF).
    """
    baselines = load_baseline_pfs(baselines_path)
    breach_path = Path(breach_state_path) if breach_state_path else DEFAULT_BREACH_STATE_PATH
    life_path = Path(lifecycle_state_path) if lifecycle_state_path else Path(STATE_FILE)

    breach_state = load_breach_state(breach_path)
    tiers = _tier_map(life_path)

    report = Call1Report(
        breach_state_path=str(breach_path),
        lifecycle_state_path=str(life_path),
        min_trade_count=min_trade_count,
    )
    delta: dict[str, str] = {}
    wrote = False

    for strategy, raw_inp in sorted(inputs.items()):
        if strategy not in STRATEGY_KEYS:
            raise ValueError(
                f"Unknown strategy {strategy!r}; valid: {sorted(STRATEGY_KEYS)}"
            )
        if isinstance(raw_inp, StrategyInput):
            inp = raw_inp
        else:
            inp = StrategyInput(
                rolling_pf=raw_inp.get("rolling_pf"),  # type: ignore[arg-type]
                trade_count=int(raw_inp["trade_count"]),  # type: ignore[index]
            )
        if strategy not in panel_by_strategy:
            raise ValueError(f"missing panel_by_strategy entry for {strategy!r}")

        baseline = baselines[strategy]
        sigma = pf_sigma_from_panel(
            panel_by_strategy[strategy],
            n_draws=n_draws,
            seed=seed,
            blocks_per_draw=blocks_per_draw,
        )
        ev = evaluate_window(
            inp.rolling_pf,
            inp.trade_count,
            baseline.pf,
            sigma,
            min_trade_count=min_trade_count,
        )
        breach_state = update_consecutive(breach_state, strategy, ev.outcome)
        consecutive = int(breach_state.get(strategy, 0))

        tier_before = tiers[strategy]
        tier_after = tier_before
        demoted = False

        if consecutive >= DEMOTION_THRESHOLD and ev.outcome == "BREACH":
            result = apply_confirmed_demotion(strategy, state_file=life_path)
            tier_after = result.tier_after
            demoted = result.demoted
            tiers[strategy] = tier_after
            if demoted:
                wrote = True
                delta[strategy] = tier_after
            # Reset consecutive counter after a demotion attempt (confirmed 2nd).
            breach_state[strategy] = 0
            consecutive = 0

        report.strategies[strategy] = Call1StrategyReport(
            rolling_pf=ev.rolling_pf,
            baseline_pf=baseline.pf,
            pf_sigma=sigma,
            floor=ev.floor,
            breached=ev.breached,
            consecutive_count=consecutive if not demoted else 0,
            window_result=ev.outcome,
            tier_before=tier_before,
            tier_after=tier_after,
            demoted=demoted,
            trade_count=inp.trade_count,
            baseline_provenance={
                "source_path": baseline.source_path,
                "section": baseline.section,
                "line_number": baseline.line_number,
            },
            pf_sigma_provenance={
                "method": "block_bootstrap_pf_std",
                "n_draws": n_draws,
                "seed": seed,
                "blocks_per_draw": blocks_per_draw,
            },
            ambiguous_reason=ev.ambiguous_reason,
        )

    save_breach_state(breach_state, breach_path)
    report.state_file_written = wrote
    report.lifecycle_state_delta = delta
    return report


def main(argv: list[str] | None = None) -> int:
    """Minimal CLI: JSON inputs on stdin or --demo-ambiguous (no demotion)."""
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Call-1 lifecycle σ-harness")
    parser.add_argument(
        "--demo-ambiguous",
        action="store_true",
        help="Run all strategies AMBIGUOUS on a synthetic panel (writes no lifecycle state)",
    )
    parser.add_argument("--n-draws", type=int, default=50)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--breach-state", type=Path, default=None)
    parser.add_argument("--lifecycle-state", type=Path, default=None)
    parser.add_argument("--baselines", type=Path, default=DEFAULT_BASELINES_PATH)
    args = parser.parse_args(argv)

    if not args.demo_ambiguous:
        print(
            "Provide --demo-ambiguous, or call run_call1_harness() from Python "
            "with rolling_pf/trade_count inputs + a panel.",
            file=sys.stderr,
        )
        return 2

    rng = np.random.default_rng(0)
    # Tiny synthetic panel with both wins and losses so σ is defined.
    panel = {
        k: rng.normal(loc=10.0, scale=50.0, size=(8, 5)) for k in sorted(STRATEGY_KEYS)
    }
    inputs = {
        k: StrategyInput(rolling_pf=None, trade_count=0) for k in sorted(STRATEGY_KEYS)
    }
    report = run_call1_harness(
        inputs,
        panel,
        n_draws=args.n_draws,
        seed=args.seed,
        baselines_path=args.baselines,
        breach_state_path=args.breach_state,
        lifecycle_state_path=args.lifecycle_state,
    )
    print(json.dumps(report.to_dict(), indent=2))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
