"""score_rules() near-duplicate wiring (2026-08-19) -- advisory only.

Reuses the known-good synthetic-motif fixture from test_stage4_7_drivers.py
("fixture must yield a cost-law survivor"). Two rules built from the
IDENTICAL shape/direction/horizon/trigger produce identical bar_returns when
evaluated on the same series -- a deterministic positive case with no need to
mock correlation math. A single-survivor run and a mismatched-shape second
rule cover the negative/no-op cases.
"""
from __future__ import annotations

import pytest

from discovery.motif_rules import freeze_rule_from_spec
from discovery.scorer import score_rules
from discovery.synthetic_bars import MotifSpec, default_motif_shape, generate_synthetic_bars


def _fixture(seed_shape=5, seed_bars=11):
    m = 20
    shape = default_motif_shape(m, seed=seed_shape)
    motif = MotifSpec(
        shape=shape,
        horizon=3,
        direction=1,
        per_trade_sr=0.35,
        trade_vol=0.008,
        period=25,
        max_oos_trades=120,
    )
    synth = generate_synthetic_bars(
        seed=seed_bars,
        motif=motif,
        is_start="2016-01-01",
        is_end="2016-06-30",
        oos_start="2019-05-06",
        oos_end="2019-12-31",
    )
    is_ret = synth.bars["ret"].to_numpy()[synth.is_mask]
    oos_ret = synth.bars["ret"].to_numpy()[synth.oos_mask]
    return shape, is_ret, oos_ret


def test_single_survivor_has_no_near_duplicates():
    shape, is_ret, oos_ret = _fixture()
    rule = freeze_rule_from_spec(shape, direction=1, horizon=3, trigger=5.0, candidate_id="planted")
    bundle = score_rules([rule], is_ret, oos_ret, mgc_price=1800.0)
    assert bundle.survivors, "fixture must yield a cost-law survivor"
    assert bundle.near_duplicates == []


def test_identical_shape_rules_report_as_near_duplicate():
    """Two candidate_ids, same shape/trigger/direction/horizon -> identical
    bar_returns when evaluated on the same series -> reported, not filtered."""
    shape, is_ret, oos_ret = _fixture()
    rule_a = freeze_rule_from_spec(shape, direction=1, horizon=3, trigger=5.0, candidate_id="a")
    rule_b = freeze_rule_from_spec(shape, direction=1, horizon=3, trigger=5.0, candidate_id="b")
    bundle = score_rules([rule_a, rule_b], is_ret, oos_ret, mgc_price=1800.0)
    assert len(bundle.survivors) == 2, "both identical rules must survive identically"
    assert len(bundle.near_duplicates) == 1
    finding = bundle.near_duplicates[0]
    assert {finding.candidate_a, finding.candidate_b} == {"a", "b"}
    assert finding.correlation > 0.999

    # Advisory only -- neither candidate was filtered or dropped from survivors.
    survivor_ids = {c.rule.candidate_id for c in bundle.survivors}
    assert survivor_ids == {"a", "b"}


def test_distinct_shapes_do_not_report_as_near_duplicate():
    shape_a, is_ret, oos_ret = _fixture(seed_shape=5)
    shape_b, _, _ = _fixture(seed_shape=42)
    rule_a = freeze_rule_from_spec(shape_a, direction=1, horizon=3, trigger=5.0, candidate_id="a")
    rule_b = freeze_rule_from_spec(shape_b, direction=1, horizon=3, trigger=5.0, candidate_id="b")
    bundle = score_rules([rule_a, rule_b], is_ret, oos_ret, mgc_price=1800.0)
    if len(bundle.survivors) < 2:
        pytest.skip("distinct shapes did not both clear cost-law in this fixture")
    assert bundle.near_duplicates == []


def test_ic_threshold_is_configurable_via_score_rules():
    shape, is_ret, oos_ret = _fixture()
    rule_a = freeze_rule_from_spec(shape, direction=1, horizon=3, trigger=5.0, candidate_id="a")
    rule_b = freeze_rule_from_spec(shape, direction=1, horizon=3, trigger=5.0, candidate_id="b")
    bundle = score_rules(
        [rule_a, rule_b], is_ret, oos_ret, mgc_price=1800.0, ic_threshold=1.0 + 1e-9
    )
    assert bundle.near_duplicates == []
