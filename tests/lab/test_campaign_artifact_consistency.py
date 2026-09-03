"""Cross-artifact consistency guard for `tradeify_book_composition_2026-09`.

Some committed artifacts are DERIVED from others. `third_leg_shape.py::characterize`
copies each finalist tier's bust, pass, median-days and bust-attribution straight out of
`grid_final.json` into `base_characterization.json`, so the two can only agree if the
characterization was produced AFTER the grid it quotes.

On 2026-09-02 they did not agree. The finals grid was regenerated at 19:00 with the
non-session-P&L fix; the characterization had been regenerated at 16:33, before it. The
committed pair therefore published two different risk estimates for the same book --
Select 14.843% vs 15.25% bust, Growth 7.837% vs 8.093%, with bust attribution 3023/1430
against 3114/1461 -- while the PR claimed all six artifacts had been "regenerated end to
end and verified mutually consistent". Every artifact HAD been regenerated; they were
regenerated in the wrong dependency order, and nothing checked the derived one against
its source. Caught by Codex on PR #271 (round 4), not by me.

This test is that missing check. It compares values only, never timestamps: mtimes are
not preserved by git, so a fresh clone or a rebase would make any ordering assertion
based on them meaningless.

Skips when the artifacts are absent, matching the campaign's other vendor-dependent tests.
"""
from __future__ import annotations

import json
import pathlib

import pytest

_CAMPAIGN = (pathlib.Path(__file__).resolve().parents[2] / "lab" / "analysis" / "c1"
             / "tradeify_book_composition_2026-09")
_DATA = _CAMPAIGN / "data"

# The book `characterize` reports on, and the fields it copies verbatim from grid_final.
_BOOK = {"mnq": 1, "mym": 0, "aegis": 2}
_FIELDS = (("bust", "bust_pct"), ("pass", "pass_pct"), ("median_days", "median_days_to_pass"))


def _load(name):
    p = _DATA / name
    if not p.exists():
        pytest.skip(f"absent: {p}")
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
    pytest.skip(f"grid_final.json carries no {_BOOK} cell for {tier}")


@pytest.mark.parametrize("tier", ["Tradeify_Select_100K", "Tradeify_Growth_100K"])
def test_characterization_matches_the_finalist_grid_it_quotes(grid, char, tier):
    key = f"final_{tier}"
    if key not in char:
        pytest.skip(f"base_characterization.json carries no {key}")
    src, got = _cell(grid, tier)["boot_intraday"], char[key]

    for char_field, grid_field in _FIELDS:
        if char_field not in got:
            continue
        a, b = float(src[grid_field]), float(got[char_field])
        assert abs(a - b) < 1e-9, (
            f"{tier} {char_field}: grid_final says {a}, base_characterization says {b} -- "
            f"rerun `third_leg_shape.py --stage characterize` AFTER the final grid")


@pytest.mark.parametrize("tier", ["Tradeify_Select_100K", "Tradeify_Growth_100K"])
def test_bust_attribution_matches_the_finalist_grid(grid, char, tier):
    key = f"final_{tier}"
    if key not in char or "bust_attribution" not in char[key]:
        pytest.skip(f"no bust_attribution for {tier}")
    src = _cell(grid, tier)["boot_intraday"]["bust_attribution"]
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
