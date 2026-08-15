"""W1 RED-first: paired `intraday_low` channel through the survivor-scoring chain.

Frozen contract: docs/spec/2026-08-04-phase4-both-halves-intraday-rerun-spec.md §1 + §5.
Two load-bearing tests — watch both FAIL before the build lands:

  (a) pairing INVARIANT — same indices through contiguous-block AND week-block resamples
  (b) non-vacuity guard — a silently dropped channel must FAIL loudly (M-23 shape)
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from discovery.prop_survivor_scoring import (
    DD_SCALE,
    NO_PROTECTION_TRIGGER,
    assert_intraday_channel_nonvacuous,
    blocks_from_daily_pnl,
    load_scoring_thresholds,
    make_alt_panel_paired,
    paired_blocks_from_daily,
    run_tier_remc,
)
from mc.preflight import firm_kwargs
from mc.simulation import run_seed

REPO = Path(__file__).resolve().parents[1]
PREREG = REPO / "docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md"

_HORIZON = 400
_N_SIMS = 200
_SEED = 42


def _synthetic_paired_days(n: int = 260) -> tuple[np.ndarray, np.ndarray]:
    """Daily P&L + deeper same-day excursion (≤ 0, dominates close)."""
    rng = np.random.default_rng(7)
    pnl = rng.normal(15.0, 220.0, size=n)
    # Excursion strictly ≤ min(0, pnl) — deeper than the close on losing days.
    deep = pnl - np.abs(rng.normal(400.0, 200.0, size=n))
    low = np.minimum(0.0, deep)
    return pnl.astype(float), low.astype(float)


def test_paired_blocks_share_calendar_indices():
    """INVARIANT (week-block resample prep): low[i] is day i's excursion for pnl[i]."""
    pnl, low = _synthetic_paired_days(60)
    # Plant a unique fingerprint on one business day and require it survive blocking.
    pnl[12] = 1234.0
    low[12] = -5678.0
    blocks_pnl, blocks_low = paired_blocks_from_daily(pnl, low)
    assert blocks_pnl.shape == blocks_low.shape
    assert blocks_pnl.ndim == 3 and blocks_pnl.shape[1:] == (5, 1)
    # Flatten week-major → day order matching the Mon-anchored build.
    flat_p = blocks_pnl.reshape(-1)
    flat_l = blocks_low.reshape(-1)
    hits = np.where(np.isclose(flat_p, 1234.0))[0]
    assert hits.size >= 1
    assert np.allclose(flat_l[hits], -5678.0)


def test_make_alt_panel_paired_uses_one_rng_draw():
    """INVARIANT (contiguous-block resample): one `st` draw, two slices — never two draws."""
    pnl, low = _synthetic_paired_days(300)
    # Tag every day so a mismatched slice is obvious.
    pnl = np.arange(pnl.size, dtype=float)
    low = -pnl * 10.0
    rng_a = np.random.default_rng(99)
    rng_b = np.random.default_rng(99)
    alt_p, alt_l = make_alt_panel_paired(
        pnl, low, target_len=pnl.size, block_size=126, rng=rng_a
    )
    # Replaying the same seed through two independent single-channel draws would
    # consume RNG differently if the helper drew twice — pin structural equality.
    assert alt_p.shape == alt_l.shape == (pnl.size,)
    assert np.allclose(alt_l, -alt_p * 10.0)
    # Control: a second call with a fresh twin seed must reproduce byte-identical.
    alt_p2, alt_l2 = make_alt_panel_paired(
        pnl, low, target_len=pnl.size, block_size=126, rng=rng_b
    )
    assert np.array_equal(alt_p, alt_p2) and np.array_equal(alt_l, alt_l2)


def test_run_seed_applies_same_indices_to_intraday_blocks():
    """INVARIANT (week-block resample inside run_seed): one index draw, both channels."""
    pnl, low = _synthetic_paired_days(200)
    blocks_pnl, blocks_low = paired_blocks_from_daily(pnl, low)
    fkw = firm_kwargs(
        "Tradeify_Select_100K", inactivity_off=True, consistency=0.40
    )
    # With intraday OFF (None), must stay bucket-identical to legacy run_seed.
    legacy = run_seed(
        _SEED,
        _N_SIMS,
        blocks_pnl,
        NO_PROTECTION_TRIGGER,
        DD_SCALE,
        horizon=_HORIZON,
        strats=("candidate",),
        firm_kwargs=fkw,
    )
    paired_off = run_seed(
        _SEED,
        _N_SIMS,
        blocks_pnl,
        NO_PROTECTION_TRIGGER,
        DD_SCALE,
        horizon=_HORIZON,
        strats=("candidate",),
        firm_kwargs=fkw,
        intraday_blocks=None,
    )
    assert paired_off["outcomes"] == legacy["outcomes"]
    assert paired_off["days_to_pass"] == legacy["days_to_pass"]

    # With a real channel, the barrier can only get stricter (never fewer busts).
    paired_on = run_seed(
        _SEED,
        _N_SIMS,
        blocks_pnl,
        NO_PROTECTION_TRIGGER,
        DD_SCALE,
        horizon=_HORIZON,
        strats=("candidate",),
        firm_kwargs=fkw,
        intraday_blocks=blocks_low,
    )

    def _bust(r: dict) -> int:
        o = r["outcomes"]
        return int(o["bust_daily"] + o["bust_static"] + o["bust_trailing"])

    assert _bust(paired_on) >= _bust(legacy)
    assert paired_on["outcomes"]["pass"] <= legacy["outcomes"]["pass"]


def test_nonvacuity_guard_zeros_match_eod_and_real_differs():
    """Non-vacuity: zeros-channel == EOD byte-for-byte; real channel MUST differ.

    A silently dropped `intraday_low` reproduces the flattering EOD numbers — the
    M-23-shaped failure the frozen Phase-4 spec exists to prevent.
    """
    pnl, low = _synthetic_paired_days(200)
    # Amplify excursions so the honest clock is non-vacuous under Tradeify geometry.
    low = np.minimum(low, -3_500.0)
    blocks_pnl, blocks_low = paired_blocks_from_daily(pnl, low)
    zeros = np.zeros_like(blocks_low)
    thr = load_scoring_thresholds(PREREG)
    fkw = firm_kwargs(
        "Tradeify_Select_100K", inactivity_off=True, consistency=0.40
    )
    # Guard itself — raises if the channel is dropped / vacuous.
    assert_intraday_channel_nonvacuous(
        blocks_pnl,
        blocks_low,
        thresholds=thr,
        firm_key="Tradeify_Select_100K",
        n_sims=_N_SIMS,
        firm_kwargs_override=fkw,
        horizon=_HORIZON,
    )
    # Planted defect: feeding zeros as the "real" channel must FAIL the guard.
    with pytest.raises(AssertionError, match="non-vacuous|vacuous|differ"):
        assert_intraday_channel_nonvacuous(
            blocks_pnl,
            zeros,
            thresholds=thr,
            firm_key="Tradeify_Select_100K",
            n_sims=_N_SIMS,
            firm_kwargs_override=fkw,
            horizon=_HORIZON,
        )


def test_run_tier_remc_threads_intraday_blocks():
    """Scoring-chain surface: run_tier_remc accepts + forwards the paired channel."""
    from dataclasses import replace

    pnl, low = _synthetic_paired_days(200)
    # Mostly shallow closes; plant deep same-day excursions so the honest clock moves.
    pnl = np.clip(pnl, -800.0, 800.0)
    low = np.minimum(low, -3_500.0)
    blocks_pnl, blocks_low = paired_blocks_from_daily(pnl, low)
    # Short horizon — full prereg 1500 makes synthetic catastrophic under both clocks.
    thr = replace(load_scoring_thresholds(PREREG), horizon=_HORIZON)
    eod = run_tier_remc(
        "Tradeify_Select_100K",
        blocks_pnl,
        thr,
        n_sims=_N_SIMS,
        consistency=0.40,
    )
    zeros = run_tier_remc(
        "Tradeify_Select_100K",
        blocks_pnl,
        thr,
        n_sims=_N_SIMS,
        consistency=0.40,
        intraday_blocks=np.zeros_like(blocks_low),
    )
    honest = run_tier_remc(
        "Tradeify_Select_100K",
        blocks_pnl,
        thr,
        n_sims=_N_SIMS,
        consistency=0.40,
        intraday_blocks=blocks_low,
    )
    assert zeros["headline_bust"] == pytest.approx(eod["headline_bust"])
    assert zeros["pass_rate"] == pytest.approx(eod["pass_rate"])
    assert honest["intraday_low"] is True
    assert honest["headline_bust"] != eod["headline_bust"] or honest["pass_rate"] != eod[
        "pass_rate"
    ]


def test_blocks_from_daily_pnl_unchanged_without_channel():
    """Legacy single-channel helper stays the close-only path (no silent rewrite)."""
    pnl, _ = _synthetic_paired_days(40)
    blocks = blocks_from_daily_pnl(pnl)
    assert blocks.shape[1:] == (5, 1)
    assert blocks.shape[0] >= 1
