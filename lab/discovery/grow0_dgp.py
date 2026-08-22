"""GROW-0 synthetic data-generating process.

Frozen per docs/briefs/pre-registration/2026-08-22-grow-0-synthetic-calibration-prereg.md §3
(FROZEN, operator GO 2026-08-22) -- every constant below is copied verbatim from that prereg, not
re-derived. Do not change any value here without superseding the prereg with a fresh ledgered
PREREG first (prereg §5 forbidden moves).
"""
from __future__ import annotations

import numpy as np

N_TRAIN_DAYS = 1638  # round(252 * 6.5), prereg §3 "Partition"
EDGE_DOLLARS = 64.4412  # prereg §3 "Edge shape", solved via scipy.optimize.brentq for annSR=4.0
TRUE_EDGE_VARIANT_INDEX = 5  # prereg §2, grammar index 5 (session_offset_min=75)

NULL_PARAMS = {
    "p_active": 0.60,
    "p_win": 0.45,
    "win_mean": 200.0,
    "win_sd": 80.0,
    "loss_mean": -163.60,
    "loss_sd": 60.0,
}


def draw_daily_pnl(
    seed,
    *,
    n_days: int = N_TRAIN_DAYS,
    edge: bool = False,
) -> np.ndarray:
    """One draw of a daily P&L series under the frozen null (or edge) shape.

    ``seed`` is anything ``numpy.random.default_rng`` accepts -- an int, or (the harness's own
    usage) a ``numpy.random.SeedSequence`` leaf from the spawn tree in this module.

    Edge shape is a pure location shift on the null shape's win/loss means (prereg §3): variance
    is unchanged, isolating the detection problem to a mean shift.
    """
    rng = np.random.default_rng(seed)
    shift = EDGE_DOLLARS if edge else 0.0
    p = NULL_PARAMS
    active = rng.random(n_days) < p["p_active"]
    win = rng.random(n_days) < p["p_win"]
    win_draw = rng.normal(p["win_mean"] + shift, p["win_sd"], size=n_days)
    loss_draw = rng.normal(p["loss_mean"] + shift, p["loss_sd"], size=n_days)
    return np.where(active, np.where(win, win_draw, loss_draw), 0.0)


GROW0_ROOT_SEED = 20260822  # dated per repo convention; prereg §3 "Seeding scheme"

_BRANCH_NAMES = ("limb_a", "limb_b", "red_leak", "red_blind", "red_patch")


def build_root_branches() -> dict:
    """The five top-level SeedSequence branches, spawned in the exact order the
    prereg's §3 code block names them -- order matters, it fixes which branch
    each name maps to."""
    root = np.random.SeedSequence(GROW0_ROOT_SEED)
    branches = root.spawn(len(_BRANCH_NAMES))
    return dict(zip(_BRANCH_NAMES, branches))


def spawn_panel_streams(panel_seq, n_variants: int):
    """One panel's train/confirm leaf SeedSequences, ``n_variants`` each.

    Independent sub-branches (spawn(2) then spawn(n) on each) -- this is the
    structural property that makes TRAIN and CONFIRM independent draws, the
    thing RED-LEAK (prereg §6.3) deliberately violates by NOT calling this
    function for its own confirm value.
    """
    train_seq, confirm_seq = panel_seq.spawn(2)
    return train_seq.spawn(n_variants), confirm_seq.spawn(n_variants)
