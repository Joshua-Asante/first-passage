"""Step 2(c): per-tier series through ``score_candidate`` (card 2026-10-06). Synthetic only."""
from __future__ import annotations


import numpy as np
import pytest

from discovery import prop_survivor_scoring as pss
from discovery.prop_survivor_scoring import TierSeries, load_scoring_thresholds, score_candidate

N_DAYS = 60
SIMS = 8


def _series(offset: float) -> TierSeries:
    rng = np.random.default_rng(7)
    pnl = rng.normal(150.0, 400.0, N_DAYS) - offset
    low = np.minimum(0.0, pnl) - 100.0 - offset
    return TierSeries(daily_pnl=pnl, intraday_low=low)


def _mapping(thr):
    return {tier: _series(10.0 * i) for i, tier in enumerate(thr.tier_keys)}


def _call(**kw):
    thr = load_scoring_thresholds()
    base = dict(
        strategy_label="synthetic",
        candidate_daily_pnl=np.full(N_DAYS, 100.0),
        full_res_trades=[200.0, -100.0] * 30,
        envelope_verdict="YES",
        n_sims=SIMS,
        gross_edge_usd=1.0e9,
    )
    base.update(kw)
    return score_candidate(**base)


def test_each_tier_runs_on_its_own_series(monkeypatch):
    thr = load_scoring_thresholds()
    mapping = _mapping(thr)
    seen: dict[str, list[float]] = {}
    real = pss.run_tier_remc

    def spy(firm_key, blocks, thresholds, **kw):
        seen.setdefault(firm_key, []).append(float(np.asarray(blocks).sum()))
        return real(firm_key, blocks, thresholds, **kw)

    monkeypatch.setattr(pss, "run_tier_remc", spy)
    monkeypatch.setattr(pss, "assert_intraday_channel_nonvacuous", lambda *a, **k: {})
    report = _call(tier_series=mapping)
    assert set(seen) == set(thr.tier_keys)
    for tier, sums in seen.items():
        expected, _ = pss.paired_blocks_from_daily(mapping[tier].daily_pnl, mapping[tier].intraday_low)
        assert all(s == pytest.approx(float(expected.sum())) for s in sums), tier
    assert report.breach_clock == "intraday_honest"
    assert set(report.tiers) == set(thr.tier_keys)


def test_missing_or_extra_tier_fails_closed():
    thr = load_scoring_thresholds()
    mapping = _mapping(thr)
    dropped = dict(mapping)
    dropped.pop(thr.tier_keys[0])
    with pytest.raises(ValueError, match="every tier"):
        _call(tier_series=dropped)
    extra = dict(mapping, Unknown_Tier=mapping[thr.tier_keys[0]])
    with pytest.raises(ValueError, match="every tier"):
        _call(tier_series=extra)


def test_tier_series_excludes_the_single_intraday_argument():
    thr = load_scoring_thresholds()
    with pytest.raises(ValueError, match="intraday_low"):
        _call(tier_series=_mapping(thr), intraday_low=np.zeros(N_DAYS))


def test_mixed_or_mismatched_channels_fail_closed():
    thr = load_scoring_thresholds()
    mapping = _mapping(thr)
    first = thr.tier_keys[0]
    mixed = dict(mapping)
    mixed[first] = TierSeries(daily_pnl=mapping[first].daily_pnl, intraday_low=None)
    with pytest.raises(ValueError, match="intraday_low"):
        _call(tier_series=mixed)
    short = dict(mapping)
    short[first] = TierSeries(daily_pnl=mapping[first].daily_pnl[:-5], intraday_low=mapping[first].intraday_low[:-5])
    with pytest.raises(ValueError, match="same length"):
        _call(tier_series=short)


def test_protected_channels_fail_closed_without_kernel_support_or_when_incomplete():
    thr = load_scoring_thresholds()
    mapping = {
        t: TierSeries(daily_pnl=s.daily_pnl, intraday_low=s.intraday_low,
                      protected_pnl=s.daily_pnl * 0.4, protected_low=s.intraday_low * 0.4)
        for t, s in _mapping(thr).items()
    }
    supported = pss._mode_switching_supported()
    if not supported:
        with pytest.raises(ValueError, match="mode-switching"):
            _call(tier_series=mapping, mode_trigger=0.01)
    with pytest.raises(ValueError, match="mode_trigger"):
        _call(tier_series=mapping)  # protected channels without a trigger
    with pytest.raises(ValueError, match="protected"):
        _call(tier_series=_mapping(thr), mode_trigger=0.01)  # trigger without channels


def test_legacy_single_series_call_unchanged(monkeypatch):
    """Without tier_series the call is the existing single-series path."""
    calls = []
    real = pss.run_tier_remc
    monkeypatch.setattr(pss, "run_tier_remc", lambda *a, **k: calls.append(k) or real(*a, **k))
    _call()
    assert calls and all("protected_blocks" not in k for k in calls)


def test_protected_channels_must_pair_and_need_intraday():
    thr = load_scoring_thresholds()
    half = {t: TierSeries(daily_pnl=s.daily_pnl, intraday_low=s.intraday_low, protected_pnl=s.daily_pnl)
            for t, s in _mapping(thr).items()}
    with pytest.raises(ValueError, match="given together"):
        _call(tier_series=half, mode_trigger=0.01)
    eod = {t: TierSeries(daily_pnl=s.daily_pnl, protected_pnl=s.daily_pnl, protected_low=s.intraday_low)
           for t, s in _mapping(thr).items()}
    with pytest.raises(ValueError, match="require intraday_low"):
        _call(tier_series=eod, mode_trigger=0.01)


def _protected_mapping(thr):
    return {
        t: TierSeries(daily_pnl=s.daily_pnl, intraday_low=s.intraday_low,
                      protected_pnl=s.daily_pnl * 0.4, protected_low=s.intraday_low * 0.4)
        for t, s in _mapping(thr).items()
    }


def test_protected_channels_reach_runs_and_guard(monkeypatch):
    """With #708 merged, each tier's protected channels and the trigger reach every G4 run and the guard."""
    if not pss._mode_switching_supported():
        pytest.skip("kernel mode-switching not present (pre-#708 main)")
    thr = load_scoring_thresholds()
    mapping = _protected_mapping(thr)
    runs, guards = [], []
    real_run, real_guard = pss.run_tier_remc, pss.assert_intraday_channel_nonvacuous

    def run_spy(firm_key, blocks, thresholds, **kw):
        runs.append((firm_key, kw))
        return real_run(firm_key, blocks, thresholds, **kw)

    def guard_spy(blocks, intraday_blocks, **kw):
        guards.append(kw)
        return real_guard(blocks, intraday_blocks, **kw)

    monkeypatch.setattr(pss, "run_tier_remc", run_spy)
    monkeypatch.setattr(pss, "assert_intraday_channel_nonvacuous", guard_spy)
    _call(tier_series=mapping, mode_trigger=0.01)
    assert {k for k, _ in runs} == set(thr.tier_keys)
    for firm_key, kw in runs + [(g["firm_key"], g) for g in guards]:
        exp_b, exp_l = pss.paired_blocks_from_daily(mapping[firm_key].protected_pnl, mapping[firm_key].protected_low)
        assert kw["mode_trigger"] == 0.01
        assert np.array_equal(kw["protected_blocks"], exp_b), firm_key
        assert np.array_equal(kw["protected_intraday_blocks"], exp_l), firm_key
    assert len(guards) == len(thr.tier_keys)


def test_protected_length_must_match_normal_length_before_blocking():
    """Codex 4190889391: 60 normal days vs 64 protected days must raise, not truncate to equal weeks."""
    thr = load_scoring_thresholds()
    rng = np.random.default_rng(11)
    long_p = rng.normal(100.0, 300.0, N_DAYS + 4)
    long_l = np.minimum(0.0, long_p) - 50.0
    mapping = {
        t: TierSeries(daily_pnl=s.daily_pnl, intraday_low=s.intraday_low,
                      protected_pnl=long_p, protected_low=long_l)
        for t, s in _mapping(thr).items()
    }
    with pytest.raises(ValueError, match="same length"):
        _call(tier_series=mapping, mode_trigger=0.01)
