"""Contract tests for the promoted research permutation utilities."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import numpy as np


def test_promoted_module_imports_with_lab_pythonpath(tmp_path: Path) -> None:
    # Smoke-check that the promoted research_utils.permutation module and its
    # public API import cleanly under PYTHONPATH=lab (the isolation posture real
    # consumers run in). This originally imported a representative *consumer*
    # (analysis.oil_carry.f1_mechanism), but every analysis-layer consumer has
    # since been archived to lab/archive/ — analysis.usdcad_rdm.gate on
    # 2026-07-11 (commit b159ec7), analysis.oil_carry on study archival — and
    # analysis.oanda_stage1 retired with OANDA. With no active consumer left to
    # pin, exercise the promoted module directly; the import path (PYTHONPATH=lab,
    # subprocess) is preserved so a packaging/promotion regression still surfaces.
    repo_root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root / "lab")
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from research_utils.permutation import "
            "label_permutation_test, window_permutation_test",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )

    assert result.returncode == 0, result.stderr


def test_label_permutation_is_deterministic() -> None:
    from research_utils.permutation import label_permutation_test

    population = np.array([8.0, 7.0, 1.0, 2.0, 3.0, 4.0])

    first = label_permutation_test(population, 2, n_perm=50, seed=7)
    second = label_permutation_test(population, 2, n_perm=50, seed=7)

    assert first[0] == 7.5
    np.testing.assert_array_equal(first[1], second[1])
    assert first[2] == second[2]


def test_window_permutation_ignores_nan_observations() -> None:
    from research_utils.permutation import window_permutation_test

    observed, null, p_value = window_permutation_test(
        np.array([1.0, np.nan, 3.0]),
        np.array([0.0, 1.0, 2.0, 3.0, 4.0]),
        n_perm=25,
        seed=11,
    )

    assert observed == 2.0
    assert null.shape == (25,)
    assert 0.0 <= p_value <= 1.0
