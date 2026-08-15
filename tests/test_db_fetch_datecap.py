"""Track A — db_fetch.py campaign-scoped IS/OOS date-cap (structural enforcement).

A discovery-phase pull must be physically unable to read past the ratified IS
boundary (2018-12-31), and the DBN cache must be era-tagged so a discovery read
cannot silently include OOS bars — while the default (no-flag) path stays
byte-identical. These are pure-function unit tests (no network / no API key):
the boundary check fires BEFORE any databento call. `importorskip` skips where
databento is absent (ops venv / CI), same posture as the other research tests.
"""
from __future__ import annotations

import hashlib
from argparse import Namespace

import pytest

pytest.importorskip("databento")

# Canonical lab module (lab is on pytest pythonpath); the skill-dir db_fetch.py is
# a thin launcher that forwards to this.
from databento_fetch import db_fetch as dfetch  # noqa: E402


def _args(**kw) -> Namespace:
    base = dict(symbols="GC.FUT", stype="parent", schema="ohlcv-1h",
                start="2010-01-01", end="2018-12-31",
                campaign_id=None, phase=None, is_boundary=None)
    base.update(kw)
    return Namespace(**base)


# -------------------------------------------------- phase boundary enforcement

def test_discovery_aborts_past_is_boundary():
    """A discovery pull that would read OOS bars aborts (SystemExit) before billing."""
    with pytest.raises(SystemExit):
        dfetch._enforce_phase_boundary(_args(phase="discovery", end="2019-06-01"))


def test_discovery_allows_full_is_window_exclusive_end():
    """--end is EXCLUSIVE, so the full IS window through 2018-12-31 is --end 2019-01-01;
    that must NOT abort (the off-by-one a naive string compare would get wrong)."""
    dfetch._enforce_phase_boundary(_args(phase="discovery", end="2019-01-01"))  # no raise


def test_discovery_allows_within_is():
    dfetch._enforce_phase_boundary(_args(phase="discovery", end="2015-06-01"))  # no raise


def test_oos_phase_not_boundary_capped():
    """The OOS phase is the hold-out; it may (must) read past the IS boundary."""
    dfetch._enforce_phase_boundary(_args(phase="oos", end="2026-07-01"))  # no raise


def test_default_no_phase_no_enforcement():
    """No --phase => byte-identical legacy behavior: no boundary enforcement at all."""
    dfetch._enforce_phase_boundary(_args(phase=None, end="2026-07-01"))  # no raise


def test_is_boundary_override_respected():
    """A campaign may override the ratified boundary (with its own stated reason);
    enforcement uses the override when supplied."""
    with pytest.raises(SystemExit):
        dfetch._enforce_phase_boundary(
            _args(phase="discovery", is_boundary="2015-12-31", end="2016-06-01"))


# -------------------------------------------------- cache era-tagging

def _legacy_cache_path(args) -> Path:
    raw = "|".join([dfetch.DATASET, args.symbols, args.stype, args.schema, args.start, args.end])
    digest = hashlib.sha1(raw.encode()).hexdigest()[:16]
    return dfetch.CACHE_DIR / f"{args.schema}_{args.stype}_{digest}.dbn"


def test_cache_key_byte_identical_without_flags():
    """A call omitting the new flags produces the exact pre-change cache filename."""
    a = _args(campaign_id=None, phase=None)
    assert dfetch._cache_path(a) == _legacy_cache_path(a)


def test_cache_key_era_tagged_with_campaign_phase():
    """campaign_id + phase fold into the key so a discovery read and an oos read of
    the same window land in different cache entries (no silent era mix)."""
    plain = dfetch._cache_path(_args())
    disc = dfetch._cache_path(_args(campaign_id="disccamp0", phase="discovery"))
    oos = dfetch._cache_path(_args(campaign_id="disccamp0", phase="oos"))
    assert disc != plain
    assert disc != oos
