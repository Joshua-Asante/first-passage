"""Ladder semantics for Tradeify Select funded contract scaling.

Guards the three properties the venue rule actually specifies, which the prior
binary `np.where(hi, CAP_HI, CAP_LO)` model got wrong:

  1. four rungs (30 -> 40 -> 50 -> 80 at the 100K tier), not two;
  2. rungs are cumulative / one-way (a retreat in balance never lowers the cap);
  3. a rung reached today takes effect the NEXT trading day.

Source: help.tradeify.co article 12853966, "Contract Scaling Plan (Funded
Accounts Only)", verified 2026-07-29. Spec:
docs/superpowers/specs/2026-07-29-funded-contract-scaling-4step-design.md
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

_STUDY = (
    Path(__file__).resolve().parents[2]
    / "lab" / "analysis" / "tradeify_book_composition_2026-07-23"
)
if str(_STUDY) not in sys.path:
    sys.path.insert(0, str(_STUDY))

FS = pytest.importorskip("funded_scaling")


def test_100k_ladder_matches_published_rungs():
    thr, cap = FS.as_arrays(FS.ladder_for(100_000.0))
    assert list(thr) == [0.0, 101_500.0, 102_000.0, 103_000.0]
    assert list(cap) == [30.0, 40.0, 50.0, 80.0]


@pytest.mark.parametrize(
    "start, thresholds, caps",
    [
        (25_000.0, [0.0, 26_500.0], [10.0, 20.0]),
        (50_000.0, [0.0, 51_500.0, 52_000.0], [20.0, 30.0, 40.0]),
        (150_000.0,
         [0.0, 151_500.0, 152_000.0, 153_000.0, 154_500.0],
         [30.0, 40.0, 50.0, 80.0, 120.0]),
    ],
)
def test_other_tiers_are_not_the_100k_ladder(start, thresholds, caps):
    thr, cap = FS.as_arrays(FS.ladder_for(start))
    assert list(thr) == thresholds
    assert list(cap) == caps


def test_start_rung_is_30_not_40_at_100k():
    """The specific defect this work fixed: the start tier was modelled as 40."""
    _, cap = FS.as_arrays(FS.ladder_for(100_000.0))
    assert cap[0] == 30.0, "funded start tier is 3 mini / 30 micro, not 4/40"


def test_rungs_climb_in_order_across_thresholds():
    thr, cap = FS.as_arrays(FS.ladder_for(100_000.0))
    rung = np.zeros(1, dtype=int)
    seen = []
    for bal in (100_000.0, 101_499.0, 101_500.0, 102_000.0, 102_999.0, 103_000.0):
        rung = FS.latch(np.array([bal]), rung, thr)
        seen.append(float(cap[rung][0]))
    assert seen == [30.0, 30.0, 40.0, 50.0, 50.0, 80.0]


def test_latch_is_one_way_on_retreat():
    thr, cap = FS.as_arrays(FS.ladder_for(100_000.0))
    rung = FS.latch(np.array([103_000.0]), np.zeros(1, dtype=int), thr)
    assert float(cap[rung][0]) == 80.0
    # Balance collapses back to start: the cap must NOT fall back.
    rung = FS.latch(np.array([100_000.0]), rung, thr)
    assert float(cap[rung][0]) == 80.0, "rungs are cumulative; caps never decrease"


def test_rung_takes_effect_the_next_day_not_the_same_day():
    """Latch is applied at END of day, so today's sizing uses today's rung."""
    thr, cap = FS.as_arrays(FS.ladder_for(100_000.0))
    rung = np.zeros(1, dtype=int)
    bal = np.array([101_500.0])  # threshold crossed during this day

    cap_used_today = float(cap[rung][0])
    rung = FS.latch(bal, rung, thr)          # end-of-day latch
    cap_used_tomorrow = float(cap[rung][0])

    assert cap_used_today == 30.0, "crossing the threshold must not raise the cap same-day"
    assert cap_used_tomorrow == 40.0


def test_legacy_two_step_reproduces_the_old_binary_shape():
    """The before/after arm must be able to reproduce pre-fix behaviour exactly."""
    thr, cap = FS.as_arrays(FS.legacy_two_step())
    assert list(thr) == [0.0, 103_000.0]
    assert list(cap) == [40.0, 80.0]
    # A bare (lo, hi) tuple is accepted and means the legacy shape.
    thr2, cap2 = FS.as_arrays((40.0, 80.0))
    assert list(thr2) == list(thr) and list(cap2) == list(cap)


def test_malformed_ladders_are_rejected():
    with pytest.raises(ValueError):
        FS.as_arrays(((0.0, 30.0), (100.0, 40.0), (50.0, 50.0)))  # not ascending
    with pytest.raises(ValueError):
        FS.as_arrays(((1_000.0, 30.0), (2_000.0, 40.0)))          # no rung at 0
    with pytest.raises(KeyError):
        FS.ladder_for(75_000.0)                                    # unknown tier


def test_parse_ladder_flag_roundtrip():
    parsed = FS.parse_ladder_flag("0:30,101500:40,102000:50,103000:80")
    assert parsed == FS.ladder_for(100_000.0)
