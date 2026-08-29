"""Sanity checks for the null-calibrated circular-shift p-value retrofitted
into the 2026-08-29 mechanism-harvest scripts (PR #205 convention).

Does not re-run the harvest scripts against vendor bars. Checks that each
target module exports `circular_shift_null_p` and that the statistic behaves
as a Type-I test: planted association → small p; independent series → not
small.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parent.parent
TARGETS = (
    REPO / "lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c24_joint_gate.py",
    REPO / "lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c2_c4_stratified_rerun.py",
    REPO / "lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c3_stratified_rerun.py",
    REPO / "lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate24_joint_gate.py",
)


def _load(path: Path):
    # These inbox scripts import siblings (`load_sessions`, `data_lib`) from
    # their own directory; put that dir on sys.path for the duration of load.
    script_dir = str(path.parent)
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    name = f"circshift_{path.stem}"
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.mark.parametrize("path", TARGETS, ids=lambda p: p.stem)
def test_circular_shift_null_p_exported(path):
    mod = _load(path)
    assert hasattr(mod, "circular_shift_null_p")
    fn = mod.circular_shift_null_p
    assert fn.__code__.co_argcount >= 3


@pytest.mark.parametrize("path", TARGETS, ids=lambda p: p.stem)
def test_circular_shift_null_p_planted_association_is_small(path):
    mod = _load(path)
    rng = np.random.default_rng(0)
    n = 400
    other = rng.integers(0, 2, size=n)
    y = other.copy()  # perfect pairing
    fixed = np.ones(n, dtype=bool)
    _draws, p, obs = mod.circular_shift_null_p(y, fixed, other, draws=400, seed=1)
    assert obs > 0.5
    assert p < 0.05


@pytest.mark.parametrize("path", TARGETS, ids=lambda p: p.stem)
def test_circular_shift_null_p_independent_is_not_tiny(path):
    mod = _load(path)
    rng = np.random.default_rng(1)
    n = 400
    other = rng.integers(0, 2, size=n)
    y = rng.integers(0, 2, size=n)
    fixed = np.ones(n, dtype=bool)
    _draws, p, _obs = mod.circular_shift_null_p(y, fixed, other, draws=400, seed=2)
    # Under a true null the one-sided p should not concentrate near 0.
    assert p > 0.05


# The three 207-retrofit scripts (not the already-merged MYM c24 reference)
# implement Codex P1/P2: within-stratum roll + enumerate distinct rotations.
RETROFIT_TARGETS = tuple(p for p in TARGETS if p.stem != "c24_joint_gate")


@pytest.mark.parametrize("path", RETROFIT_TARGETS, ids=lambda p: p.stem)
def test_within_stratum_roll_preserves_class_balance_and_complement(path):
    mod = _load(path)
    assert hasattr(mod, "roll_other_within_stratum")
    n = 200
    fixed = np.zeros(n, dtype=bool)
    fixed[:100] = True
    other = np.zeros(n, dtype=int)
    other[:80] = 1          # 80/100 ones inside the stratum
    other[100:120] = 1      # 20/100 ones outside — correlated with the mask
    rolled = mod.roll_other_within_stratum(other, fixed, k=17)
    assert int(rolled[fixed].sum()) == int(other[fixed].sum())
    assert np.array_equal(rolled[~fixed], other[~fixed])


def test_candidate24_prefers_vendor_bars_over_committed_cache():
    src = (
        REPO / "lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate24_joint_gate.py"
    ).read_text()
    main = src[src.index("def main():"):]
    assert "CSV.exists()" in main
    assert main.index("from_bars = CSV.exists()") < main.index("load_cached_frame()")
    assert "if from_bars:" in main


@pytest.mark.parametrize("path", RETROFIT_TARGETS, ids=lambda p: p.stem)
def test_enumerated_p_respects_rotation_floor(path):
    """n=80 stratum → at most 80 distinct rotations; p cannot be 1/4001."""
    mod = _load(path)
    rng = np.random.default_rng(3)
    n = 80
    other = rng.integers(0, 2, size=n)
    y = other.copy()
    fixed = np.ones(n, dtype=bool)
    draws, p, _obs = mod.circular_shift_null_p(y, fixed, other, draws=4000, seed=4)
    n_valid = len(draws)
    assert n_valid <= n
    assert n_valid > 0
    # Identity is included: minimum attainable p is 1/n_valid, never 1/4001.
    assert p >= 1.0 / n_valid - 1e-12
    assert abs(p * n_valid - round(p * n_valid)) < 1e-9
