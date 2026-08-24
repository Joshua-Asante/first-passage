"""Synthetic payoff-shape trade-generating process for the slate-2 DESIGN-BOX
extension of the A2 feasibility map.

Not a strategy, not a candidate, not a mechanism -- same status as
shape_generator.py's three shapes (see that module's own docstring). This
module is a DISCLOSED COVERAGE EXTENSION of the A2 map -- a sibling module,
never a silent edit to shape_generator.py's own frozen WIN_RATES / SHAPES /
RISK_USD grid or its committed region_data.jsonl. See RESULTS_DESIGNBOX_EXT.md
for the full write-up (dispatched this session: design-box vs A2-region
reconciliation, operator-GO'd 2026-08-24).

Generates one new shape archetype, "design_box", parametrizing the slate-2
hunting-region geometry ratified by
docs/adr/2026-08-13-msl-slate-2-design-box.md: `rr` in [2, 3] * target WR
0.30-0.42 * `R` at the bust<=3.0% diffusion frontier (provisional) * hard
stop mandatory * k=1 * no pyramiding.

Generative choices, disclosed
------------------------------
* **Win R ~ Uniform(2, 3)** -- the ADR's own `rr` range, taken literally as a
  maximally-uncertain (uniform) prior across it. No free parameter is chosen
  beyond "trust the box's own stated span"; the mean win is exactly 2.5R.
* **Loss R = -1.0 exactly** (hard stop, NO jitter) -- reuses
  `shape_generator.SHAPES`'s `"bounded_clustered"` loss convention, not
  `"symmetric"`/`"mild_right_skew"`'s jittered `-Uniform(0.7, 1.3)`: the
  ADR's box mandates "hard stop mandatory", and `bounded_clustered`'s exact
  `-1.0` is the one A2 shape that actually models a hard stop with no
  slippage. Every losing trade's MAE equals its realized loss exactly (same
  convention as ALL THREE existing A2 shapes -- no gap-through-stop tail
  modeled, same disclosed limitation as RESULTS.md Sec2/Sec11).
* **Winning-trade MAE band = Uniform(0.30, 0.80) of ONE STOP (1R)** -- reuses
  `shape_generator`'s `"mild_right_skew"` band verbatim, not a newly invented
  one. Rationale: a trade held open to a 2-3R target spends materially
  longer exposed than a ~1R takeout -- exactly the "let it run" reasoning
  RESULTS.md Sec2 gives for `mild_right_skew`'s own wider band (vs
  `symmetric`'s tighter one). Reusing that already-disclosed band keeps this
  new shape's excursion convention traceable to an existing A2 choice rather
  than an unaudited new number.
* **k=1 entries/day** is the ADR's own mandate for a real mechanism's entry
  rule. This module still sweeps A2's full cadence axis (1, 2, 3, 5, 8/week)
  UNCHANGED, per dispatch instruction ("A2's axis, unchanged") -- including
  `shape_generator.WEEKDAY_PATTERN[8]`'s same-calendar-day doubling
  (Mon x2/Tue x2/...). That is coverage of trade FREQUENCY, not a claim that
  a literal k=1-compliant mechanism would fire twice in one day; A2's own
  three shapes never made a k=1 claim for their cadence sweep either, and
  this extension inherits that same coverage-not-claim status. Disclosed as
  a limitation in RESULTS_DESIGNBOX_EXT.md, not silently smoothed over.
  **"No pyramiding"** is structurally satisfied: this DGP draws one scalar
  R-multiple per trade, never a stacked/pyramided position.

Win rates tested: {0.30, 0.35, 0.40} -- the design box's own span (0.42 is
the box's stated ceiling; the swept grid stops at 0.40, the shared row
against A2's own grid floor, per dispatch instruction).

Frontier-R
----------
See `_frontier_r_usd` / `risk_levels_for_win_rate` below -- computed via the
UNMODIFIED audit-hook formula from
docs/notes/notice/N-2026-08-13-msl-design-box-rederivation.md Sec9, with
`rr=2.5` (this shape's own `E[win_R]`, since `m0 = p*E[win_R] - (1-p)` is
EXACT under this substitution when losses are point-mass at -1R) and
`c=2.82` (the notice's own published "index micros" round-trip figure,
Sec9 -- reproduced verbatim in `test_design_box_shape.py` as a sanity check
against the notice's own worked table, which this module's formula matches
to the cent). Disclosed second-order approximation: the closed form's
variance term technically assumes a point-mass win side (a fixed `rr*R`
payoff), not this shape's actual Uniform(2,3) spread -- the true variance is
about 1% higher than the point-mass formula assumes (extra spread from the
win side itself), which makes this frontier-R very slightly optimistic
relative to a fully-exact closed form for this precise DGP. That is
second-order next to the note's own already-disclosed approximation layers
(i.i.d. trades, continuous diffusion, infinite horizon -- Sec8 item 2). The
ACTUAL feasibility verdict for every cell in this extension comes from the
real MC engine run on the real simulated panel, never from this closed
form -- the closed form is used exclusively to select which downward risk
level(s) enter the swept grid, per dispatch instruction ("Risk: ... PLUS the
computed frontier-R ... if it differs (downward only)").
"""
from __future__ import annotations

import math
from collections import Counter
from typing import Dict, List, Tuple

import numpy as np

import shape_generator as sg

# --- Reused, unchanged, from shape_generator.py (never re-typed) ----------
N_WEEKS = sg.N_WEEKS  # 520 synthetic weeks, same base panel length as A2
WEEKDAY_PATTERN = sg.WEEKDAY_PATTERN  # cadence -> weekday tuple, A2's own axis unchanged
CADENCES: Tuple[int, ...] = sg.CADENCES  # (1, 2, 3, 5, 8) -- "A2's axis, unchanged" (dispatch)

# --- New, design-box-specific ----------------------------------------------
SHAPE_NAME = "design_box"
DESIGNBOX_MASTER_SEED = 20260824  # today's dispatch date; deliberately distinct from
                                   # shape_generator.DGP_MASTER_SEED (20260823) so the
                                   # two DGPs' RNG streams never collide or get confused.

WIN_RATES: Tuple[float, ...] = (0.30, 0.35, 0.40)  # the design box's own span, floored
                                                     # at the shared row against A2 (dispatch)

_WIN_LO, _WIN_HI = 2.0, 3.0   # win R ~ Uniform(2,3) -- the ADR's own rr range, literal
_LOSS_R = -1.0                 # hard stop, exact, no jitter (bounded_clustered convention)
_MAE_LO, _MAE_HI = 0.30, 0.80  # winning-trade giveback band, reusing mild_right_skew's band

# EM2's own $250/$275 axis (A2's axis) -- $325 deliberately never tested here: the box's
# own R-sizing logic points down, not up (dispatch instruction); see risk_levels_for_win_rate.
EM2_RISK_USD: Tuple[float, ...] = (250.0, 275.0)

# Frontier closed-form constants, verbatim from N-2026-08-13 notice Sec9's own audit hook.
_ROPE_USD = 3000.0     # both Tradeify_Select_100K and MFFU_Rapid_100K share this trail
                        # (core/firm_rules.py max_dd_pct=3.0 on $100K, both firms -- Rule-0 read)
_TARGET_USD = 6000.0   # profit_target_pct=6.0 on $100K, both firms (disclosure only, unused
                        # in the R_max solve itself, kept for parity with the notice's solve())
_BUST_CEILING = 0.03
FRONTIER_RR = 2.5        # this shape's own E[win_R] -- see module docstring
FRONTIER_C_USD = 2.82    # notice Sec9's own published "index micros" RT figure, verbatim


def _frontier_r_usd(
    win_rate: float,
    *,
    rope_usd: float = _ROPE_USD,
    bust_ceiling: float = _BUST_CEILING,
    rr: float = FRONTIER_RR,
    cost_usd: float = FRONTIER_C_USD,
) -> float | None:
    """Bust<=3% diffusion frontier R, via N-2026-08-13 notice Sec9's own closed
    form (`m0`/`K`/`disc`/`R`), unmodified. Returns `None` exactly where the
    notice's own script returns `None`: non-positive gross expectancy, or a
    negative discriminant (cost exceeds any bust-compliant R at this
    `(win_rate, rr)` pair).
    """
    m0 = win_rate * rr - (1.0 - win_rate)
    if m0 <= 0:
        return None
    x = -math.log(bust_ceiling)
    k = (2.0 * rope_usd / x) / ((rr + 1.0) ** 2 * win_rate * (1.0 - win_rate))
    disc = (k * m0) ** 2 - 4.0 * k * cost_usd
    if disc < 0:
        return None
    return (k * m0 + math.sqrt(disc)) / 2.0


def risk_levels_for_win_rate(win_rate: float) -> Tuple[float, ...]:
    """A2's own $250/$275 axis, plus the computed frontier-R IF it is finite
    and strictly below $250 (downward only -- dispatch instruction and the
    EM2 spec's own "interpolate down, never up" rule). Never adds $325: the
    box's own R-sizing logic points down, not up, for every win rate tested
    here (the frontier for WR>=0.40 already sits at or below the EM2 floor).
    """
    levels = list(EM2_RISK_USD)
    fr = _frontier_r_usd(win_rate)
    if fr is not None and fr < min(EM2_RISK_USD):
        levels.append(round(fr, 2))
    return tuple(sorted(levels))


def all_tuples() -> List[Tuple[float, int, float]]:
    """(win_rate, cadence, risk_usd) coverage grid. Risk levels are WR-dependent
    (`risk_levels_for_win_rate`), so this is NOT a fixed-size rectangular
    product the way A2's own `all_tuples()` is -- it is still a fixed,
    pre-registered, documented enumeration order (WR outer, risk middle,
    cadence inner), reproducible byte-for-byte on every call.
    """
    out: List[Tuple[float, int, float]] = []
    for wr in WIN_RATES:
        for rk in risk_levels_for_win_rate(wr):
            for cd in CADENCES:
                out.append((wr, cd, rk))
    return out


_TUPLE_INDEX: Dict[Tuple[float, int, float], int] = {
    t: i for i, t in enumerate(all_tuples())
}  # module-load-time, pure function of the grid's own fixed definition above


def tuple_index(win_rate: float, cadence: int, risk: float) -> int:
    """Deterministic enumeration index for one grid tuple -- drives the DGP seed.
    Pure function of the tuple's own coordinates (never of any prior result),
    so re-running this module reproduces byte-identical panels.
    """
    key = (win_rate, cadence, risk)
    if key not in _TUPLE_INDEX:
        raise KeyError(f"not a design_box grid tuple: {key!r}")
    return _TUPLE_INDEX[key]


def _draw_trade_r(rng: np.random.Generator, is_win: bool) -> float:
    """One trade's realized R-multiple (signed; win in [2,3]R, loss = -1R)."""
    if is_win:
        return float(rng.uniform(_WIN_LO, _WIN_HI))
    return _LOSS_R


def _draw_trade_mae_r(rng: np.random.Generator, is_win: bool, realized_r: float) -> float:
    """Worst intraday mark-against before this trade's close, in R-units, <= 0.
    Same intraday-honest role as shape_generator._draw_trade_mae_r (W1 pattern,
    docs/adr/2026-08-07-w1-intraday-honest-engine-remeasure.md)."""
    if not is_win:
        return realized_r  # hard-stop reached, not slipped past (disclosed limitation)
    return -min(0.95, float(rng.uniform(_MAE_LO, _MAE_HI)))


def build_panel(win_rate: float, cadence: int, risk: float) -> Tuple[np.ndarray, np.ndarray]:
    """Return (daily_pnl, intraday_low) arrays, N_WEEKS*5 business days long.

    Structurally identical to shape_generator.build_panel: `intraday_low[d]`
    is the day's worst mark-to-market excursion below that day's OPENING
    equity (<=0, dollars), composed SEQUENTIALLY across however many trades
    land on that day -- never a naive sum-of-independent-lows.
    """
    if cadence not in WEEKDAY_PATTERN:
        raise ValueError(f"no weekday pattern registered for cadence={cadence}")
    seed = DESIGNBOX_MASTER_SEED + tuple_index(win_rate, cadence, risk)
    rng = np.random.default_rng(seed)
    counts = Counter(WEEKDAY_PATTERN[cadence])

    n_days = N_WEEKS * 5
    daily = np.zeros(n_days, dtype=float)
    intraday = np.zeros(n_days, dtype=float)

    for w in range(N_WEEKS):
        for wd, n_trades in counts.items():
            cum = 0.0
            day_low = 0.0
            for _ in range(n_trades):
                is_win = bool(rng.random() < win_rate)
                r = _draw_trade_r(rng, is_win)
                mae_r = _draw_trade_mae_r(rng, is_win, r)
                trade_low = cum + mae_r * risk
                if trade_low < day_low:
                    day_low = trade_low
                cum += r * risk
            idx = w * 5 + wd
            daily[idx] = cum
            intraday[idx] = min(0.0, day_low)
    return daily, intraday


def expectancy_r(win_rate: float, *, n_draw: int = 200_000, seed: int = 778) -> float:
    """Monte-Carlo expectancy in R-units -- disclosure only. Independent of
    `build_panel`'s own seeding (fixed diagnostic seed, distinct from
    shape_generator.expectancy_r's own seed=777) so this is stable regardless
    of which tuple calls it. Not used by the scoring path.
    """
    rng = np.random.default_rng(seed)
    is_win = rng.random(n_draw) < win_rate
    r = np.empty(n_draw, dtype=float)
    n_win = int(is_win.sum())
    n_loss = n_draw - n_win
    r[is_win] = rng.uniform(_WIN_LO, _WIN_HI, n_win)
    r[~is_win] = _LOSS_R
    assert n_loss >= 0
    return float(r.mean())


__all__ = [
    "N_WEEKS",
    "WEEKDAY_PATTERN",
    "CADENCES",
    "SHAPE_NAME",
    "DESIGNBOX_MASTER_SEED",
    "WIN_RATES",
    "EM2_RISK_USD",
    "FRONTIER_RR",
    "FRONTIER_C_USD",
    "_frontier_r_usd",
    "risk_levels_for_win_rate",
    "all_tuples",
    "tuple_index",
    "build_panel",
    "expectancy_r",
]
