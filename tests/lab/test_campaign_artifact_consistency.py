"""Cross-artifact consistency guard for `tradeify_book_composition_2026-09`.

Some committed artifacts are DERIVED from others. `third_leg_shape.py::characterize`
copies each finalist tier's bust, pass, median-days, p75-days and bust-attribution
straight out of `grid_final.json` into `base_characterization.json`, so the two can only
agree if the characterization was produced AFTER the grid it quotes.

On 2026-09-02 they did not agree. The finals grid was regenerated at 19:00 with the
non-session-P&L fix; the characterization had been regenerated at 16:33, before it. The
committed pair therefore published two different risk estimates for the same book --
Select 14.843% vs 15.25% bust, Growth 7.837% vs 8.093%, with bust attribution 3023/1430
against 3114/1461 -- while the PR claimed all six artifacts had been "regenerated end to
end and verified mutually consistent". Every artifact HAD been regenerated; they were
regenerated in the wrong dependency order, and nothing checked the derived one against
its source. Caught by Codex on PR #271 (round 4), not by me.

MISSING DERIVED CONTENT IS A FAILURE, NOT A SKIP. The first version of this file skipped
whenever a `final_*` entry was absent, which made it blind to the very ordering it exists
to detect: `characterize` swallows `FileNotFoundError` on the grid and writes NO `final_*`
entries at all, so a characterization built with the grid missing would have sailed
through a gate designed to catch exactly that. Codex caught this too (round 5). Skips are
now confined to the artifact FILES being absent, matching the campaign's other
vendor-dependent tests; once both load, every derived entry and field is required.

Values are compared, never mtimes: git does not preserve those, so any ordering assertion
based on them would be meaningless in a fresh clone or after a rebase.
"""
from __future__ import annotations

import json
import pathlib

import pytest

_CAMPAIGN = (pathlib.Path(__file__).resolve().parents[2] / "lab" / "analysis" / "c1"
             / "tradeify_book_composition_2026-09")
_DATA = _CAMPAIGN / "data"

# The book `characterize` reports on, and every field it copies verbatim out of the grid,
# as {name in base_characterization: name in grid_final's boot_intraday}.
_BOOK = {"mnq": 1, "mym": 0, "aegis": 2}
_TIERS = ("Tradeify_Select_100K", "Tradeify_Growth_100K")
_COPIED = {
    "bust": "bust_pct",
    "pass": "pass_pct",
    "median_days": "median_days_to_pass",
    "p75_days": "p75_days_to_pass",
}


def _load(name):
    p = _DATA / name
    if not p.exists():
        pytest.skip(f"absent: {p}")          # the ONLY legitimate skip in this file
    with p.open(encoding="utf-8") as fh:
        return json.load(fh)


@pytest.fixture(scope="module")
def grid():
    return _load("grid_final.json")


@pytest.fixture(scope="module")
def char():
    return _load("base_characterization.json")


def _cell(grid, tier):
    for r in grid["results"]:
        if r["sizing"] == _BOOK and r["tier"] == tier:
            return r
    return None


def test_grid_carries_the_book_the_characterization_quotes(grid):
    """Anchors the rest: if this book vanished from the grid, say so loudly.

    Without this, a grid that stopped containing the book would make every comparison
    below trivially satisfiable.
    """
    missing = [t for t in _TIERS if _cell(grid, t) is None]
    assert not missing, (
        f"grid_final.json has no {_BOOK} cell for {missing}; the consistency checks below "
        f"cannot bind, so fix the grid or update _BOOK/_TIERS deliberately")


@pytest.mark.parametrize("tier", _TIERS)
def test_characterization_has_an_entry_for_every_finalist_tier(grid, char, tier):
    """A committed characterization must not be missing derived content.

    `characterize` swallows FileNotFoundError on `grid_final.json` and simply writes no
    `final_*` key, so absence here is the signature of the wrong dependency ordering --
    the thing this file exists to catch.
    """
    if _cell(grid, tier) is None:
        pytest.skip(f"grid has no {_BOOK} cell for {tier} (see the anchor test)")
    assert f"final_{tier}" in char, (
        f"base_characterization.json has no final_{tier} although grid_final.json carries "
        f"that cell -- rerun `third_leg_shape.py --stage characterize` AFTER the final grid")


@pytest.mark.parametrize("tier", _TIERS)
def test_characterization_matches_the_finalist_grid_it_quotes(grid, char, tier):
    cell = _cell(grid, tier)
    if cell is None:
        pytest.skip(f"grid has no {_BOOK} cell for {tier} (see the anchor test)")
    key = f"final_{tier}"
    assert key in char, f"missing {key} (see the entry-presence test)"
    src, got = cell["boot_intraday"], char[key]

    for char_field, grid_field in _COPIED.items():
        assert char_field in got, f"{key} is missing the copied field {char_field!r}"
        a, b = src[grid_field], got[char_field]
        if a is None or b is None:
            assert a == b, f"{tier} {char_field}: grid_final {a!r} vs characterization {b!r}"
            continue
        assert abs(float(a) - float(b)) < 1e-9, (
            f"{tier} {char_field}: grid_final says {a}, base_characterization says {b} -- "
            f"rerun `third_leg_shape.py --stage characterize` AFTER the final grid")


@pytest.mark.parametrize("tier", _TIERS)
def test_bust_attribution_matches_the_finalist_grid(grid, char, tier):
    cell = _cell(grid, tier)
    if cell is None:
        pytest.skip(f"grid has no {_BOOK} cell for {tier} (see the anchor test)")
    key = f"final_{tier}"
    assert key in char, f"missing {key} (see the entry-presence test)"
    assert "bust_attribution" in char[key], f"{key} is missing bust_attribution"
    src = cell["boot_intraday"]["bust_attribution"]
    assert char[key]["bust_attribution"] == src, (
        f"{tier} bust attribution: grid_final {src} vs base_characterization "
        f"{char[key]['bust_attribution']}")


def test_grid_final_declares_the_seeds_and_sims_it_was_run_at(grid):
    """Cheap header sanity: a truncated or hand-edited grid should not pass silently."""
    assert grid.get("stage") == "final"
    assert grid.get("n_sims", 0) >= 1
    assert isinstance(grid.get("seeds"), list) and grid["seeds"], "seeds must be recorded"
    assert grid.get("results"), "no cells in grid_final.json"
    for r in grid["results"]:
        assert "boot_intraday" in r and "tier" in r and "sizing" in r
