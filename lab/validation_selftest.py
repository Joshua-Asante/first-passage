"""Gen-1 harness self-test generators — extracted from ``lab/validation/controls.py``.

These produce in-memory synthetic trial families for gate calibration. Gen-2
delegates DSR/PBO/CPCV to ``arch``/``skfolio`` (``strategy-validation`` §8);
DSR wiring for these controls landed 2026-07-11 in
``tests/test_validation_selftest_dsr_gate.py`` (stdlib DSR in
``lab/research_utils/deflated_sharpe.py``). SPA/PBO self-tests remain a
follow-on (research venv). See ADR
``docs/adr/2026-07-11-gen1-pipeline-retirement.md`` §2 (controls extraction).

* NEGATIVE — ``generate_negative_control``: pure-noise configs, IS-best selected.
  A correct gate must FAIL to reject the null.
* POSITIVE — ``generate_positive_control``: heterogeneous injected edge so
  best-of-N is real skill, not noise luck. A correct gate must reject the null.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ControlData:
    """A synthetic trial family for control testing."""

    trial_returns: list[np.ndarray]
    entry_times: np.ndarray
    exit_times: np.ndarray
    best_index: int
    label: str

    @property
    def best_returns(self) -> np.ndarray:
        return self.trial_returns[self.best_index]

    @property
    def n_trials(self) -> int:
        return len(self.trial_returns)


def _shared_spans(n_trades: int, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    start = np.datetime64("2022-01-04T08:00:00")
    day_offsets = np.sort(rng.integers(0, 1580, size=n_trades))
    minute_jit = rng.integers(0, 8 * 60, size=n_trades)
    exit_times = (
        start
        + day_offsets.astype("timedelta64[D]")
        + minute_jit.astype("timedelta64[m]")
    ).astype("datetime64[ns]")
    hold_minutes = rng.integers(30, 2 * 24 * 60, size=n_trades)
    entry_times = (exit_times - hold_minutes.astype("timedelta64[m]")).astype(
        "datetime64[ns]"
    )
    return entry_times, exit_times


def _select_is_best(trial_returns: list[np.ndarray]) -> int:
    def sr(r: np.ndarray) -> float:
        s = r.std(ddof=1)
        return float(r.mean() / s) if (len(r) > 1 and s > 0) else 0.0

    srs = [sr(r) for r in trial_returns]
    return int(np.argmax(srs))


def generate_negative_control(
    *,
    n_trials: int = 50,
    n_trades: int = 200,
    vol: float = 0.005,
    seed: int = 42,
) -> ControlData:
    rng = np.random.default_rng(seed)
    trial_returns = [
        rng.normal(0.0, vol, size=n_trades) for _ in range(n_trials)
    ]
    best = _select_is_best(trial_returns)
    entry_times, exit_times = _shared_spans(n_trades, np.random.default_rng(seed + 7))
    return ControlData(
        trial_returns=trial_returns,
        entry_times=entry_times,
        exit_times=exit_times,
        best_index=best,
        label="negative_control(random_entries)",
    )


def generate_positive_control(
    *,
    n_trials: int = 50,
    n_trades: int = 200,
    edge: float = 0.0025,
    vol: float = 0.005,
    seed: int = 7,
) -> ControlData:
    rng = np.random.default_rng(seed)
    drifts = np.linspace(0.0, edge, n_trials)
    trial_returns = [
        rng.normal(drifts[i], vol, size=n_trades) for i in range(n_trials)
    ]
    best = _select_is_best(trial_returns)
    entry_times, exit_times = _shared_spans(n_trades, np.random.default_rng(seed + 7))
    return ControlData(
        trial_returns=trial_returns,
        entry_times=entry_times,
        exit_times=exit_times,
        best_index=best,
        label="positive_control(injected_edge)",
    )
