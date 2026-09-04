"""Pinned campaign-table tests for scripts/certification_power.py."""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "certification_power.py"
_SPEC = importlib.util.spec_from_file_location("certification_power", SCRIPT)
cp = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
sys.modules[_SPEC.name] = cp
_SPEC.loader.exec_module(cp)

PIN_ABS = 5e-4


@pytest.mark.parametrize(
    ("n", "expected"),
    [(60, 0), (160, 3), (340, 10), (630, 22), (950, 36)],
)
def test_max_certifying_busts_campaign_pins(n: int, expected: int) -> None:
    assert cp.max_certifying_busts(n) == expected


@pytest.mark.parametrize(
    ("n", "true_rate", "expected"),
    [
        (60, 0.005, 0.7403),
        (160, 0.02, 0.6021),
        (340, 0.03, 0.5577),
    ],
)
def test_per_limb_power_campaign_pins(
    n: int, true_rate: float, expected: float
) -> None:
    assert cp.per_limb_power(n, true_rate) == pytest.approx(expected, abs=PIN_ABS)


def test_joint_power_at_n630_campaign_pins() -> None:
    q = cp.per_limb_power(630, 0.03)
    assert q == pytest.approx(0.8030, abs=PIN_ABS)
    assert cp.joint_power(0.8030, 3, "independent") == pytest.approx(
        0.5178, abs=PIN_ABS
    )
    assert cp.joint_power(0.8030, 3, "frechet") == pytest.approx(0.4090, abs=PIN_ABS)


@pytest.mark.parametrize(
    ("true_rate", "expected"),
    [(0.005, 130), (0.02, 370), (0.03, 950)],
)
def test_size_for_power_independent_campaign_pins(
    true_rate: float, expected: int
) -> None:
    assert cp.size_for_power(true_rate, 0.80) == expected


@pytest.mark.parametrize(
    ("true_rate", "expected"),
    [(0.005, 130), (0.02, 390), (0.03, 970)],
)
def test_size_for_power_frechet_campaign_pins(
    true_rate: float, expected: int
) -> None:
    assert cp.size_for_power(true_rate, 0.80, dependence="frechet") == expected


def test_size_for_power_single_limb_campaign_pin() -> None:
    assert cp.size_for_power(0.03, 0.80, limbs=1) == 630


def test_joint_power_rejects_unknown_dependence() -> None:
    with pytest.raises(ValueError):
        cp.joint_power(0.9, 3, "bogus")


def test_no_certifying_count_is_minus_one_and_zero_power() -> None:
    assert cp.max_certifying_busts(5) == -1
    assert cp.per_limb_power(5, 0.01) == 0.0


def test_cli_eval_n630_smoke() -> None:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--n", "630", "--true-rate", "0.03"],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert "per_limb=0.803" in proc.stdout
