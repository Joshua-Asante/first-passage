"""Guard: the MC anchor-evolution chart generator stays in sync with data.csv.

`docs/analytics/mc_anchor_evolution/plot.py` silently drifted from its own
`data.csv` between 2026-05-23 and 2026-06-05: the A9/O9 anchors were added to
data.csv (commit 5b8ff71, #112) but plot.py's hardcoded `short` x-labels and
`oanda_xmap` were not updated, so `python plot.py` crashed (KeyError on O9)
and the committed PNGs went stale without anyone noticing.

These invariants fail loudly the next time an anchor row is added to data.csv
without updating plot.py, instead of leaving a stale or un-regenerable chart.
No vendor data needed — reads only the committed data.csv.
"""

import importlib.util
from pathlib import Path

import pandas as pd

CHART_DIR = (Path(__file__).resolve().parents[1]
             / "docs" / "analytics" / "mc_anchor_evolution")
DATA_CSV = CHART_DIR / "data.csv"
PLOT_PY = CHART_DIR / "plot.py"


def _load_plot_module():
    """Import plot.py by path. Its rendering is gated under __main__, so this
    runs only the module-level data prep (no figures written)."""
    spec = importlib.util.spec_from_file_location("mc_anchor_plot", PLOT_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_xlabel_count_matches_pepperstone_anchors():
    plot = _load_plot_module()
    assert len(plot.short) == len(plot.pep), (
        f"plot.py `short` has {len(plot.short)} x-labels but data.csv has "
        f"{len(plot.pep)} alchemy/pepperstone anchors. matplotlib raises on "
        f"the mismatch — add/remove a `short` label to match."
    )


def test_every_oanda_row_is_mapped_or_excluded():
    plot = _load_plot_module()
    df = pd.read_csv(DATA_CSV)
    oanda_rows = {(r.date, r.anchor_id)
                  for r in df[df["panel"] == "oanda"].itertuples()}
    accounted = set(plot.oanda_xmap) | plot.oanda_excluded
    missing = oanda_rows - accounted
    assert not missing, (
        f"OANDA rows in data.csv neither mapped nor explicitly excluded: "
        f"{sorted(missing)}. Add each to plot.oanda_xmap (to plot it) or "
        f"plot.oanda_excluded (to omit it, e.g. superseded same-cycle)."
    )


def test_oanda_xmap_and_excluded_are_disjoint():
    plot = _load_plot_module()
    overlap = set(plot.oanda_xmap) & plot.oanda_excluded
    assert not overlap, f"OANDA anchors both mapped and excluded: {sorted(overlap)}"


def test_oanda_xmap_targets_valid_pepperstone_positions():
    plot = _load_plot_module()
    n = len(plot.pep)
    bad = {k: x for k, x in plot.oanda_xmap.items() if not 0 <= x < n}
    assert not bad, f"oanda_xmap targets outside the [0,{n}) anchor range: {bad}"
