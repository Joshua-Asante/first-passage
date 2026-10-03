"""O-4 Slice A — intraday-honest channel through ``score_candidate`` (red-first).

Frozen contract: docs/briefs/handoffs/2026-10-02-remc-o4-slice-a-build-card.md §2
(operator ruling 2026-10-02, O-3 RESOLVED / prereg I-12: the intraday-honest clock
is mandatory on every gating tier read; EOD-clock reads are reportable, never gate
a clear).

Eight tests, all written before the module edit: the failing (red) launcher record
must exist before ``lab/discovery/prop_survivor_scoring.py`` changes. Synthetic
inputs only — no candidate, calibration reference or venue data (prereg §R).
"""
from __future__ import annotations

import json
from collections import Counter

import numpy as np
import pandas as pd
import pytest

import discovery.prop_survivor_scoring as pss
from discovery.prop_survivor_scoring import load_scoring_thresholds

# ── Shared fixtures (card §2, "Red-first tests") ─────────────────────────────
# Gentle positive EOD P&L that never busts any frozen tier (equity rises 80/day),
# paired with a planted excursion channel deeper than any tier's drawdown: every
# excursion week that is drawn before the pass barrier busts intraday, so the
# honest clock moves while the EOD clock reads a flat zero.
_N_DAYS = 260
_N_SIMS = 40
_PNL = np.full(_N_DAYS, 80.0)
_TRADES = [80.0] * 120
_GROSS_EDGE_USD = 50_000.0
_LOW = np.zeros(_N_DAYS)
_LOW[::35] = -10_000.0

# The 10 keys to_dict emitted at d5d559b, plus exactly the three Slice A keys.
_EXISTING_DICT_KEYS = frozenset(
    {
        "strategy_label",
        "g1",
        "g2_by_tier",
        "tiers",
        "routing",
        "funded_ruin_tier_count",
        "discharges_falsifier",
        "halted_at",
        "thresholds_source",
        "regime_robustness_gate",
    }
)
_NEW_DICT_KEYS = frozenset({"breach_clock", "gate_grade", "gate_grade_reasons"})


def _thr():
    """v2 default gate (5.0% eval ceiling, frozen four tiers, seeds 42/123/2026)."""
    return load_scoring_thresholds()


def _score(intraday_low=None, envelope="YES", thr=None):
    return pss.score_candidate(
        strategy_label="o4-slice-a-fixture",
        candidate_daily_pnl=_PNL,
        full_res_trades=_TRADES,
        envelope_verdict=envelope,
        thresholds=thr if thr is not None else _thr(),
        n_sims=_N_SIMS,
        gross_edge_usd=_GROSS_EDGE_USD,
        intraday_low=intraday_low,
    )


# ── 1. channel threading ─────────────────────────────────────────────────────


def test_intraday_blocks_reach_every_g4_run(monkeypatch):
    """Every G4 run on every tier reaching G4 carries the paired channel, and the
    frozen non-vacuity guard runs once per gating tier at the gating depth."""
    thr = _thr()
    expected_low_blocks = pss.paired_blocks_from_daily(_PNL, _LOW)[1]
    expected_pnl_blocks = pss.blocks_from_daily_pnl(_PNL)
    real_remc = pss.run_tier_remc
    remc_calls: list[tuple[str, np.ndarray, dict]] = []

    def spy_remc(firm_key, blocks, thresholds, **kwargs):
        remc_calls.append((firm_key, blocks, kwargs))
        return real_remc(firm_key, blocks, thresholds, **kwargs)

    guard_calls: list[tuple[str, int]] = []

    def guard_recorder(blocks, intraday_blocks, *, thresholds, firm_key, n_sims, **kwargs):
        assert np.array_equal(blocks, expected_pnl_blocks), firm_key
        assert np.array_equal(intraday_blocks, expected_low_blocks), firm_key
        assert thresholds is thr, firm_key
        guard_calls.append((firm_key, int(n_sims)))

    monkeypatch.setattr(pss, "run_tier_remc", spy_remc)
    monkeypatch.setattr(pss, "assert_intraday_channel_nonvacuous", guard_recorder)

    _score(intraday_low=_LOW, thr=thr)

    # Call count per tier: Run-1 + Run-2 where a consistency rule exists, else
    # the degenerate single run (run1_degenerate).
    per_tier = Counter(firm_key for firm_key, _b, _kw in remc_calls)
    for firm_key in thr.tier_keys:
        assert per_tier[firm_key] == (
            2 if pss._consistency_frac(firm_key) is not None else 1
        ), firm_key

    # Every G4 run: channel present, paired blocks exact, P&L blocks exact.
    assert remc_calls, "no G4 run was recorded"
    for firm_key, blocks, kwargs in remc_calls:
        assert kwargs.get("intraday_blocks") is not None, firm_key
        assert np.array_equal(kwargs["intraday_blocks"], expected_low_blocks), firm_key
        assert np.array_equal(blocks, expected_pnl_blocks), firm_key

    # Guard: exactly once per non-G2-killed tier, that tier's firm_key, gating depth.
    assert Counter(fk for fk, _n in guard_calls) == Counter(
        {firm_key: 1 for firm_key in thr.tier_keys}
    )
    assert all(n == _N_SIMS for _fk, n in guard_calls)


# ── 2. breach_clock / gate_grade labels ──────────────────────────────────────


def test_breach_clock_and_gate_grade_labels():
    # No channel: EOD clock, never gate-grade, exactly one explanatory reason.
    eod = _score(intraday_low=None)
    assert eod.breach_clock == "eod"
    assert eod.gate_grade is False
    assert len(eod.gate_grade_reasons) == 1
    assert "intraday_low" in eod.gate_grade_reasons[0]

    # Planted (non-vacuous) channel: honest clock, gate-grade, no reasons.
    honest = _score(intraday_low=_LOW)
    assert honest.breach_clock == "intraday_honest"
    assert honest.gate_grade is True
    assert honest.gate_grade_reasons == []

    # G1 halt: labels are set on the early return path too. With a channel, no
    # tier reached G4 so no breach-clock read exists to fail (card §0.5(C)).
    halted_with = _score(intraday_low=_LOW, envelope="NO")
    assert halted_with.halted_at == "G1"
    assert halted_with.breach_clock == "intraday_honest"
    assert halted_with.gate_grade is True

    halted_without = _score(intraday_low=None, envelope="NO")
    assert halted_without.halted_at == "G1"
    assert halted_without.breach_clock == "eod"
    assert halted_without.gate_grade is False


# ── 3. vacuous channel is reported, not raised ───────────────────────────────


def test_vacuous_channel_reports_not_gate_grade():
    vacuous = np.zeros(_N_DAYS)
    report = _score(intraday_low=vacuous)  # must NOT raise
    thr = _thr()
    assert report.breach_clock == "intraday_honest"
    assert report.gate_grade is False
    assert report.gate_grade_reasons, "a vacuous channel must record reasons"
    for firm_key in thr.tier_keys:
        tier_reasons = [
            r for r in report.gate_grade_reasons if r.startswith(f"{firm_key}:")
        ]
        assert tier_reasons, firm_key
        assert "non-vacuity" in tier_reasons[0], firm_key
        # Figures stay reportable — INSUFFICIENT, not a crash.
        ts = report.tiers[firm_key]
        assert "headline_bust" in ts.run1, firm_key
        assert "headline_bust" in ts.run2, firm_key


def test_engine_fault_in_guard_propagates(monkeypatch):
    """Only a "non-vacuity FAIL" AssertionError is a vacuity finding; any other
    AssertionError from the guard (an engine invariant) must escape (card §4)."""

    def _engine_fault(*args, **kwargs):
        raise AssertionError("bucket sum != n_sims")

    monkeypatch.setattr(pss, "assert_intraday_channel_nonvacuous", _engine_fault)
    with pytest.raises(AssertionError, match="bucket sum"):
        _score(intraday_low=_LOW)


# ── 4. invalid channel raises ValueError before G1 ───────────────────────────


def _invalid_channel_cases():
    positive = np.zeros(_N_DAYS)
    positive[7] = 1.0
    nan_low = np.zeros(_N_DAYS)
    nan_low[7] = np.nan
    pos_inf = np.zeros(_N_DAYS)
    pos_inf[7] = np.inf
    neg_inf = np.zeros(_N_DAYS)
    neg_inf[7] = -np.inf
    nan_pnl = _PNL.copy()
    nan_pnl[10] = np.nan
    return [
        pytest.param(_PNL.copy(), np.zeros(259), "length", id="length-259"),
        pytest.param(_PNL.copy(), positive, "0.0", id="positive-entry"),
        pytest.param(_PNL.copy(), nan_low, "finite", id="nan-low"),
        pytest.param(_PNL.copy(), pos_inf, "0.0|finite", id="pos-inf-low"),
        pytest.param(_PNL.copy(), neg_inf, "finite", id="neg-inf-low"),
        pytest.param(nan_pnl, _LOW.copy(), "finite", id="nan-pnl"),
    ]


@pytest.mark.parametrize("pnl,low,match", _invalid_channel_cases())
def test_invalid_intraday_low_raises(pnl, low, match):
    """Invalid channel (length, sign, non-finite in either channel) raises
    ValueError even when G1 would halt — validation precedes G1."""
    for envelope in ("YES", "NO"):
        with pytest.raises(ValueError, match=match):
            pss.score_candidate(
                strategy_label="invalid-channel",
                candidate_daily_pnl=pnl,
                full_res_trades=_TRADES,
                envelope_verdict=envelope,
                thresholds=_thr(),
                n_sims=_N_SIMS,
                gross_edge_usd=_GROSS_EDGE_USD,
                intraday_low=low,
            )


# ── 5. honest bust is never below the EOD bound ──────────────────────────────


def test_intraday_bust_not_below_eod_per_tier():
    """Same seeds, same sims: the honest clock can only add busts / remove passes,
    and on this fixture Run-2 actually busts (strictly) above the EOD read."""
    eod = _score(intraday_low=None)
    honest = _score(intraday_low=_LOW)
    assert set(eod.tiers) == set(honest.tiers)
    for firm_key, s_eod in eod.tiers.items():
        s_honest = honest.tiers[firm_key]
        assert s_honest.run1["headline_bust"] >= s_eod.run1["headline_bust"], firm_key
        assert s_honest.run2["headline_bust"] >= s_eod.run2["headline_bust"], firm_key
        assert s_honest.run1["pass_rate"] <= s_eod.run1["pass_rate"], firm_key
        assert s_honest.run2["pass_rate"] <= s_eod.run2["pass_rate"], firm_key
        assert s_honest.run2["headline_bust"] > s_eod.run2["headline_bust"], firm_key


# ── 6. EOD byte-identity ─────────────────────────────────────────────────────


def test_eod_path_identical(monkeypatch):
    """intraday_low=None is the legacy path: guard never runs, every tier figure
    equals a direct run_tier_remc call, and to_dict gains exactly three keys."""

    def _guard_must_not_run(*args, **kwargs):
        raise AssertionError("guard must not run on the EOD path")

    monkeypatch.setattr(pss, "assert_intraday_channel_nonvacuous", _guard_must_not_run)

    thr = _thr()
    real_remc = pss.run_tier_remc
    remc_calls: list[tuple[tuple, dict]] = []

    def spy_remc(*args, **kwargs):
        remc_calls.append((args, dict(kwargs)))
        return real_remc(*args, **kwargs)

    monkeypatch.setattr(pss, "run_tier_remc", spy_remc)
    report = _score(intraday_low=None, thr=thr)
    monkeypatch.setattr(pss, "run_tier_remc", real_remc)
    blocks = pss.blocks_from_daily_pnl(_PNL)

    # Call sequence and arguments are the d5d559b shape: positional
    # (firm_key, blocks, thr), keywords exactly {n_sims, consistency} — the
    # intraday_blocks keyword is never passed on the EOD path.
    expected_calls = []
    for firm_key in report.tiers:
        cons = pss._consistency_frac(firm_key)
        expected_calls.append((firm_key, {"n_sims": _N_SIMS, "consistency": None}))
        if cons is not None:
            expected_calls.append((firm_key, {"n_sims": _N_SIMS, "consistency": cons}))
    assert [(a[0], kw) for a, kw in remc_calls] == expected_calls
    for args, _kw in remc_calls:
        assert len(args) == 3 and args[2] is thr
        assert np.array_equal(args[1], blocks)

    # Omitting the keyword (every pre-Slice-A caller) and passing None give the
    # same full report.
    omitted = pss.score_candidate(
        strategy_label="o4-slice-a-fixture",
        candidate_daily_pnl=_PNL,
        full_res_trades=_TRADES,
        envelope_verdict="YES",
        thresholds=thr,
        n_sims=_N_SIMS,
        gross_edge_usd=_GROSS_EDGE_USD,
    )
    assert omitted.to_dict() == report.to_dict()
    for firm_key, ts in report.tiers.items():
        direct_run1 = pss.run_tier_remc(
            firm_key, blocks, thr, n_sims=_N_SIMS, consistency=None
        )
        cons = pss._consistency_frac(firm_key)
        direct_run2 = (
            direct_run1
            if cons is None
            else pss.run_tier_remc(
                firm_key, blocks, thr, n_sims=_N_SIMS, consistency=cons
            )
        )
        assert ts.run1["headline_bust"] == direct_run1["headline_bust"], firm_key
        assert ts.run1["pass_rate"] == direct_run1["pass_rate"], firm_key
        assert ts.run1["rates"] == direct_run1["summary"]["rates"], firm_key
        assert ts.run2["headline_bust"] == direct_run2["headline_bust"], firm_key
        assert ts.run2["pass_rate"] == direct_run2["pass_rate"], firm_key
        assert ts.run2["rates"] == direct_run2["summary"]["rates"], firm_key

    assert set(report.to_dict()) == _EXISTING_DICT_KEYS | _NEW_DICT_KEYS


# ── 7. CLI round trip ────────────────────────────────────────────────────────


def test_cli_intraday_low_csv_round_trip(tmp_path, capsys):
    pnl_csv = tmp_path / "daily_pnl.csv"
    trades_csv = tmp_path / "trades.csv"
    low_csv = tmp_path / "intraday_low.csv"
    pd.DataFrame({"pnl": _PNL}).to_csv(pnl_csv, index=False)
    pd.DataFrame({"pnl": _TRADES}).to_csv(trades_csv, index=False)
    pd.DataFrame({"intraday_low": _LOW}).to_csv(low_csv, index=False)
    base = [
        "--label",
        "o4-slice-a-cli",
        "--daily-pnl-csv",
        str(pnl_csv),
        "--trades-csv",
        str(trades_csv),
        "--envelope",
        "YES",
        "--n-sims",
        str(_N_SIMS),
    ]

    out_intraday = tmp_path / "out_intraday.json"
    assert pss.main([*base, "--intraday-low-csv", str(low_csv), "--out", str(out_intraday)]) == 0
    payload = json.loads(out_intraday.read_text(encoding="utf-8"))
    assert payload["breach_clock"] == "intraday_honest"
    assert isinstance(payload["gate_grade"], bool)
    assert payload["gate_grade"] is True
    printed = capsys.readouterr().out
    assert "breach_clock=intraday_honest" in printed
    assert "gate_grade=True" in printed

    out_eod = tmp_path / "out_eod.json"
    assert pss.main([*base, "--out", str(out_eod)]) == 0
    payload_eod = json.loads(out_eod.read_text(encoding="utf-8"))
    assert payload_eod["breach_clock"] == "eod"
    assert payload_eod["gate_grade"] is False
    printed_eod = capsys.readouterr().out
    assert "breach_clock=eod" in printed_eod
    assert "gate_grade=False" in printed_eod

    short_csv = tmp_path / "intraday_low_short.csv"
    pd.DataFrame({"intraday_low": np.zeros(259)}).to_csv(short_csv, index=False)
    out_short = tmp_path / "out_short.json"
    with pytest.raises(ValueError, match="length"):
        pss.main([*base, "--intraday-low-csv", str(short_csv), "--out", str(out_short)])


# ── 8. discharge rule unchanged on the intraday path ─────────────────────────


def test_discharge_rule_unchanged_on_intraday_path():
    """discharges_falsifier keeps its own definition on the channel path; a
    gate-grade discharge reads `discharges_falsifier and gate_grade` (I-12) — the
    module reports both and never combines them."""
    thr = _thr()
    planted = _score(intraday_low=_LOW)
    assert planted.discharges_falsifier == pss.discharges_falsifier(planted.tiers, thr)

    vacuous = _score(intraday_low=np.zeros(_N_DAYS))
    assert vacuous.discharges_falsifier == pss.discharges_falsifier(vacuous.tiers, thr)
    assert (vacuous.discharges_falsifier and vacuous.gate_grade) is False
