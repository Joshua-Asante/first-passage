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
