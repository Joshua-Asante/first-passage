"""Engine pre-flight tests (constraint D None-tolerance + F1 bucket-sum).

Covers core/mc/preflight.py and the four None-tolerant import sites it depends
on. No vendor CSVs required — firm_rules configs + synthetic seed results +
tiny synthetic paths only, so this runs on a fresh public clone.

Ground truth for the two findings under test:
docs/briefs/2026-07-12-survivor-scoring-and-ddp-reframe-recommendation.md
(§0 constraint D, §1 F1, §2.1 G3).
"""

import numpy as np
import pytest

from firm_rules import AUTOMATION_FRIENDLY_PROP_FIRMS, FIRM_RULES
from mc.preflight import (
    BUST_KEYS,
    OUTCOME_KEYS,
    assert_engine_ready,
    firm_kwargs,
    summarize_outcomes,
)


def _mk_seed(pass_=0, bust_daily=0, bust_static=0, bust_trailing=0,
             bust_inactivity=0, horizon_cap=0):
    """A minimal run_seed-shaped result for summarize_outcomes tests."""
    return {
        "outcomes": {
            "pass": pass_,
            "bust_daily": bust_daily,
            "bust_static": bust_static,
            "bust_trailing": bust_trailing,
            "bust_inactivity": bust_inactivity,
            "horizon_cap": horizon_cap,
        },
        "days_to_pass": [],
        "max_dds": [],
        "bust_attribution": {},
    }


_ALL_PROP_TIERS = [t for tiers in AUTOMATION_FRIENDLY_PROP_FIRMS.values() for t in tiers]


# ── Constraint D: firm_kwargs threads None-safely + dispatches dd_type ────────

def test_firm_kwargs_prop_tier_daily_loss_is_none():
    # Every FRIENDLY prop tier carries daily_loss_pct=None (no daily loss limit).
    for tier in _ALL_PROP_TIERS:
        kw = firm_kwargs(tier)
        assert kw["daily_loss_pct"] is None, f"{tier} should thread None daily loss"


def test_firm_kwargs_historical_fixture_not_a_firm_rules_key():
    """FXIFY row deleted Phase 4 — historical semantics live in historical_challenge."""
    import historical_challenge as hc
    from mc.simulation import HISTORICAL_CHALLENGE_FIRM_KWARGS

    with pytest.raises(KeyError, match="FXIFY"):
        firm_kwargs("FXIFY")
    assert HISTORICAL_CHALLENGE_FIRM_KWARGS["daily_loss_pct"] == pytest.approx(-0.05)
    assert hc.STARTING_EQUITY == 200_000.0
    assert HISTORICAL_CHALLENGE_FIRM_KWARGS["dd_type"] == "static"


def test_firm_kwargs_dd_type_dispatch():
    # trailing (Bulenox) → trailing_dd_pct, no lock offset
    kw_t = firm_kwargs("Bulenox_100K")
    assert kw_t["dd_type"] == "trailing"
    assert kw_t["trailing_dd_pct"] == pytest.approx(-0.03)  # max_dd_pct 3.0
    assert "dd_lock_offset_usd" not in kw_t
    assert "static_dd_pct" not in kw_t

    # trailing_locking (Tradeify) → trailing_dd_pct + dd_lock_offset_usd.
    # Assert against the live FIRM_RULES value, not a hardcoded number: this is
    # a dispatch test (does trailing_locking thread BOTH keys through
    # faithfully), not a pin on the business fact of what the offset IS. A
    # hardcoded expectation here is exactly the "next consumer inherits the
    # stale default" trap that motivated the 2026-08-04 eval-lock fix (ADR
    # docs/adr/2026-08-04-firm-rules-eval-lock-fix-applied.md) in the first
    # place — this test asserted the pre-fix value (100.0) until it broke on
    # that fix landing, which is exactly the intended signal.
    kw_l = firm_kwargs("Tradeify_Select_100K")
    assert kw_l["dd_type"] == "trailing_locking"
    assert kw_l["trailing_dd_pct"] == pytest.approx(-0.03)
    assert kw_l["dd_lock_offset_usd"] == pytest.approx(
        FIRM_RULES["Tradeify_Select_100K"]["dd_lock_offset_usd"]
    )
    assert kw_l["dd_lock_offset_usd"] >= 1_000.0  # sanity: must be far from reachable at $100K
    assert kw_l["starting_equity"] == 100_000.0


def test_firm_kwargs_consistency_and_inactivity_flags():
    kw_off = firm_kwargs("MFFU_Rapid_100K", inactivity_off=True, consistency=None)
    assert kw_off["consistency_frac"] is None
    assert kw_off["inactivity_limit"] > 1500  # disabled sentinel

    kw_on = firm_kwargs("MFFU_Rapid_100K", inactivity_off=False, consistency=0.50)
    assert kw_on["consistency_frac"] == 0.50
    assert kw_on["inactivity_limit"] == 5  # the tier's real rule


def test_firm_kwargs_unknown_firm_raises():
    with pytest.raises(KeyError):
        firm_kwargs("NotAFirm_99K")


# --- inactivity provenance + unsourced guard ---------------------------------
# ADR 2026-08-05  containment: BluSky's 30 was a subscription-renewal window.
# ADR 2026-08-05b sourcing:    the real rule is ToU art. 11490284 s3.3 ("inactive
#   for 30 consecutive days"), trade-based per art. 12434442, unit-corrected to
#   22 idle BUSINESS days because the engine counts bdays and the clause counts
#   calendar days. The guard machinery stays tested against a synthetic tier so
#   it cannot rot now that no shipped tier carries the flag.


def test_blusky_inactivity_is_sourced_and_unit_corrected():
    """Pins both halves of the 2026-08-05b correction.

    If either moves, the F3 BluSky arms and the ADR's §4 need revisiting —
    this field carries the whole cross-venue cadence verdict.
    """
    for tier in ("BluSky_Premium_50K", "BluSky_Premium_100K"):
        assert FIRM_RULES[tier]["inactivity_rule_sourced"] is True
        assert FIRM_RULES[tier]["inactivity_max_idle_days"] == 22, (
            "BluSky's limit is 22 idle BDAYS = the ToU's '30 consecutive "
            "[calendar] days'. A literal 30 here models ~42 calendar days and is "
            "~40% too lenient — that was the 2026-08-05b defect."
        )


def test_unsourced_inactivity_on_raises_without_ack(monkeypatch):
    """Guard machinery, exercised on a synthetic unsourced tier."""
    tier = dict(FIRM_RULES["BluSky_Premium_100K"])
    tier["inactivity_rule_sourced"] = False
    monkeypatch.setitem(FIRM_RULES, "_Synthetic_Unsourced_100K", tier)
    with pytest.raises(ValueError, match="inactivity_rule_sourced=False"):
        firm_kwargs("_Synthetic_Unsourced_100K", inactivity_off=False)


def test_unsourced_inactivity_on_allowed_with_explicit_ack(monkeypatch):
    tier = dict(FIRM_RULES["BluSky_Premium_100K"])
    tier["inactivity_rule_sourced"] = False
    monkeypatch.setitem(FIRM_RULES, "_Synthetic_Unsourced_100K", tier)
    kw = firm_kwargs(
        "_Synthetic_Unsourced_100K",
        inactivity_off=False,
        allow_unsourced_inactivity=True,
    )
    assert kw["inactivity_limit"] == tier["inactivity_max_idle_days"]


def test_unsourced_flag_never_affects_inactivity_off(monkeypatch):
    """The default path — and every published figure — must be untouched."""
    tier = dict(FIRM_RULES["BluSky_Premium_100K"])
    tier["inactivity_rule_sourced"] = False
    monkeypatch.setitem(FIRM_RULES, "_Synthetic_Unsourced_100K", tier)
    kw = firm_kwargs("_Synthetic_Unsourced_100K", inactivity_off=True)
    assert kw["inactivity_limit"] > 1500  # disabled sentinel, no raise


def test_sourced_tiers_run_inactivity_on_without_ack():
    """Guard must be narrow: every shipped tier is sourced and needs no ack."""
    for tier in (
        "Tradeify_Select_100K", "Bulenox_100K", "MFFU_Rapid_100K",
        "BluSky_Premium_100K",
    ):
        kw = firm_kwargs(tier, inactivity_off=False)
        assert kw["inactivity_limit"] == FIRM_RULES[tier]["inactivity_max_idle_days"]


def test_blusky_is_bulenox_apart_from_the_inactivity_limit():
    """The identity that makes this one field carry the F3 verdict (ADR §1).

    If these two tiers ever diverge on any other field, the 'BluSky's entire
    advantage is one integer' claim stops holding and the ADRs need revisiting.
    """
    a = firm_kwargs("Bulenox_100K", inactivity_off=True)
    b = firm_kwargs("BluSky_Premium_100K", inactivity_off=True)
    assert a == b
    # ...and with inactivity ON they differ in exactly one key.
    a_on = firm_kwargs("Bulenox_100K", inactivity_off=False)
    b_on = firm_kwargs("BluSky_Premium_100K", inactivity_off=False)
    assert {k for k in a_on if a_on[k] != b_on[k]} == {"inactivity_limit"}


@pytest.mark.parametrize("tier", _ALL_PROP_TIERS)
def test_assert_engine_ready_threads_without_typeerror(tier):
    # Constraint D across every configured prop tier: a None daily_loss_pct (and each
    # dd_type geometry) threads into simulate_path without raising.
    kw = assert_engine_ready(tier)
    assert kw["starting_equity"] > 0


# ── F1: summarize_outcomes surfaces trailing busts + asserts bucket-sum ───────

def test_summarize_bucket_sum_and_headline_bust():
    seeds = [
        _mk_seed(pass_=90, bust_daily=2, bust_static=1, bust_trailing=3, horizon_cap=4),
        _mk_seed(pass_=88, bust_daily=1, bust_static=1, bust_trailing=6, horizon_cap=4),
    ]
    out = summarize_outcomes(seeds, sims_per_seed=100)
    # headline bust = mean over seeds of (daily+static+trailing) = mean(6, 8)/100
    assert out["headline_bust"] == pytest.approx(0.07)
    assert out["pass_rate"] == pytest.approx(0.89)
    assert set(out["rates"]) == set(OUTCOME_KEYS)


def test_summarize_headline_bust_includes_trailing_the_f1_trap():
    # The exact F1 failure mode: all busts route to bust_trailing. A naive
    # daily+static headline reads 0.0; summarize_outcomes must read 0.05.
    seeds = [_mk_seed(pass_=95, bust_trailing=5)]
    out = summarize_outcomes(seeds, sims_per_seed=100)
    naive_daily_static = out["rates"]["bust_daily"] + out["rates"]["bust_static"]
    assert naive_daily_static == 0.0
    assert out["headline_bust"] == pytest.approx(0.05)
    assert "bust_trailing" in BUST_KEYS


def test_summarize_bucket_sum_violation_raises():
    seeds = [_mk_seed(pass_=90, bust_trailing=5, horizon_cap=4)]  # sums to 99, not 100
    with pytest.raises(AssertionError, match="bucket-sum"):
        summarize_outcomes(seeds, sims_per_seed=100)


def test_summarize_bucket_key_drift_raises():
    bad = _mk_seed(pass_=100)
    del bad["outcomes"]["horizon_cap"]  # drop a canonical bucket
    with pytest.raises(AssertionError, match="outcome keys"):
        summarize_outcomes([bad], sims_per_seed=100)


def test_summarize_empty_raises():
    with pytest.raises(ValueError):
        summarize_outcomes([], sims_per_seed=100)


# ── Historical-fixture byte-identity (substrate Phase 4) ─────────────────────

def test_import_site_constants_byte_identical_under_historical_fixture():
    """MC/dd_protection defaults match core/historical_challenge.py literals."""
    import dd_protection
    from mc import modes, simulation
    assert dd_protection.DAILY_LOSS_LIMIT == pytest.approx(0.05)
    assert modes.DAILY_LOSS_PCT == pytest.approx(-0.05)
    assert simulation.DAILY_LOSS_PCT == pytest.approx(-0.05)


# ── Constraint D: prop tiers thread None-safe via preflight ──────────────────

def test_prop_tier_none_daily_loss_threads_via_preflight():
    """None-tolerance for prop tiers is proven through preflight.firm_kwargs."""
    from mc.preflight import assert_engine_ready, firm_kwargs

    assert_engine_ready("Tradeify_Select_100K")
    kw = firm_kwargs("Tradeify_Select_100K", inactivity_off=True)
    assert kw["daily_loss_pct"] is None
    assert kw["dd_type"] == "trailing_locking"


def test_active_firm_symbol_removed():
    """ACTIVE_FIRM deleted Phase 4 — historical defaults are fixture literals."""
    import firm_rules
    assert not hasattr(firm_rules, "ACTIVE_FIRM")
    assert "FXIFY" not in firm_rules.FIRM_RULES
    import dd_protection
    from mc import modes, simulation
    assert dd_protection.DAILY_LOSS_LIMIT == pytest.approx(0.05)
    assert simulation.DAILY_LOSS_PCT == pytest.approx(-0.05)
    assert modes.DAILY_LOSS_PCT == pytest.approx(-0.05)
