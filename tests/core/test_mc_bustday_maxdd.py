"""Bust-path max_dd must include the terminating (breach) day.

Pre-fix, _simulate_path returned on bust_daily/bust_static/bust_trailing
BEFORE the underwater update ran, so the breach day's drawdown never entered
max_dd — a first-day -5.5% bust reported max_dd=0.0, and every bust path's
recorded max_dd was the pre-breach value. p99_dd pools max_dd across ALL
sims including busts (run_seed appends unconditionally), so the lock-gate
metric was biased downward, growing with bust rate — largest in exactly the
2020-23 chop regime the 2026-06-07 HOLD decision worries about.

Cursor-audit Issue 3, adversarially verified 2026-07-06; fix governed by
docs/adr/2026-07-06-bust-day-maxdd-inclusion.md (anchor re-run + re-pin).

Direct _simulate_path calls (Rule 0-T style, same idiom as
test_mc_anchors.test_simulate_path_direct_call_at_daily_loss_boundary).
dd_trigger=1.0 disables dd_protection scaling where hand-math needs raw
pnl; production DD_TRIGGER/DD_SCALE are irrelevant to day-1 paths.
"""

import numpy as np
import pytest

from dd_protection import DD_SCALE, DD_TRIGGER
from portfolio_mc import STARTING_EQUITY, STRATS, _simulate_path

N_STRATS = len(STRATS)


def _path(rows):
    """Build a (days, N_STRATS) path with the whole day's pnl on strat 0."""
    path = np.zeros((len(rows), N_STRATS))
    for i, pnl in enumerate(rows):
        path[i, 0] = pnl
    return path


def test_bust_daily_day1_includes_breach_day_dd():
    """Single-shot -5.5% on day 1: bust_daily with max_dd 0.055, not 0.0."""
    path = _path([-11_000.0])
    outcome, day, max_dd, culprit = _simulate_path(
        path, dd_trigger=DD_TRIGGER, dd_scale=DD_SCALE, horizon=1
    )
    assert outcome == "bust_daily"
    assert day == 1
    assert culprit == 0
    assert max_dd == pytest.approx(11_000.0 / STARTING_EQUITY)  # 0.055


def test_bust_static_grind_includes_breach_day_dd():
    """-0.9%/day grind: bust_static on day 6 with max_dd 5.4%, not 4.5%.

    dd_trigger=1.0 keeps sizing at 1.0x so the grind arithmetic is exact:
    eq after day 5 = 191,000 (dd 4.5%, no bust); day 6 eq_new = 189,200,
    (189,200 - 200,000)/200,000 = -0.054 <= -0.05 -> bust_static. The
    breach-day drawdown (200,000 - 189,200)/200,000 = 5.4% must be the
    recorded max_dd.
    """
    path = _path([-1_800.0] * 6)
    outcome, day, max_dd, culprit = _simulate_path(
        path, dd_trigger=1.0, dd_scale=1.0, horizon=6
    )
    assert outcome == "bust_static"
    assert day == 6
    assert max_dd == pytest.approx(10_800.0 / STARTING_EQUITY)  # 0.054


def test_bust_trailing_includes_breach_day_dd():
    """Trailing-DD firm (Bulenox-class): breach-day DD from peak recorded.

    Day 1 +8,000 (eq/peak 208,000 — below the 210,000 profit target);
    day 2 -14,000 -> eq_new 194,000, (194,000 - 208,000)/208,000 =
    -0.0673 <= -0.06 -> bust_trailing. max_dd must be 14,000/208,000,
    not the pre-breach 0.0.
    """
    path = _path([8_000.0, -14_000.0])
    outcome, day, max_dd, culprit = _simulate_path(
        path, dd_trigger=1.0, dd_scale=1.0, horizon=2,
        dd_type="trailing", trailing_dd_pct=-0.06, daily_loss_pct=None,
    )
    assert outcome == "bust_trailing"
    assert day == 2
    assert max_dd == pytest.approx(14_000.0 / 208_000.0)


def test_surviving_path_max_dd_unchanged():
    """Invariance guard: non-bust paths keep byte-identical max_dd.

    The fix hoists the underwater update above the bust checks; for
    surviving days that is the same arithmetic against the same (old)
    peak, so this hand-computed value must hold before AND after.
    """
    path = _path([-3_000.0, 1_000.0])
    outcome, day, max_dd, culprit = _simulate_path(
        path, dd_trigger=1.0, dd_scale=1.0, horizon=2
    )
    assert outcome == "horizon_cap"
    assert max_dd == pytest.approx(3_000.0 / STARTING_EQUITY)  # 0.015
