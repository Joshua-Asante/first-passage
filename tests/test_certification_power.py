"""Pinned campaign-table tests for scripts/certification_power.py."""
from __future__ import annotations

import importlib.util
import math
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


def test_exact_cdf_boundary_still_certifies() -> None:
    # P(X <= 0) for X~Binom(1, 0.05) equals 0.95 exactly. Mode-relative
    # normalization must not overshoot that boundary and reject k=0.
    assert cp._binom_cdf(0, 1, 0.05) == 0.95
    assert cp.max_certifying_busts(1, ceiling=0.05, alpha=0.95) == 0


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


def test_max_certifying_busts_rejects_n_below_one() -> None:
    with pytest.raises(ValueError):
        cp.max_certifying_busts(0)


@pytest.mark.parametrize("true_rate", [-0.03, 1.5, float("nan")])
def test_per_limb_power_rejects_out_of_domain_true_rate(true_rate: float) -> None:
    with pytest.raises(ValueError):
        cp.per_limb_power(60, true_rate)


def test_joint_power_rejects_zero_limbs_and_q_outside_unit() -> None:
    with pytest.raises(ValueError):
        cp.joint_power(0.9, 0, "independent")
    with pytest.raises(ValueError):
        cp.joint_power(1.5, 3, "independent")


@pytest.mark.parametrize(
    "kwargs",
    [
        {"ceiling": 1.0},
        {"alpha": 2},
        {"target": 0},
        {"n_max": 5},
    ],
)
def test_size_for_power_rejects_out_of_domain_kwargs(kwargs: dict) -> None:
    call = {"true_rate": 0.03, "target": 0.8}
    if "target" in kwargs:
        call["target"] = kwargs.pop("target")
    call.update(kwargs)
    with pytest.raises(ValueError):
        cp.size_for_power(call.pop("true_rate"), call.pop("target"), **call)


def test_max_certifying_busts_n8000_regression_pin() -> None:
    assert cp.max_certifying_busts(8000) == 367


def test_per_limb_power_n8000_near_ceiling_regression_pin() -> None:
    assert cp.per_limb_power(8000, 0.049) == pytest.approx(0.1013, abs=PIN_ABS)


def test_size_for_power_unreachably_high_true_rate_raises() -> None:
    with pytest.raises(ValueError):
        cp.size_for_power(0.049, 0.80, n_max=2000)


@pytest.mark.parametrize(
    "args",
    [
        ("--true-rate=-0.03", "--power", ".8"),
        ("--limbs", "0", "--n", "630", "--true-rate", "0.03"),
        ("--alpha", "2", "--n", "60", "--true-rate", "0.03"),
    ],
)
def test_cli_out_of_domain_exits_2_empty_stdout(args: tuple[str, ...]) -> None:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 2, proc.stderr
    assert proc.stdout == ""
    assert proc.stderr
    assert "Traceback" not in proc.stderr


def test_perfect_power_rejects_positive_failure_probability() -> None:
    # Every finite binomial sample retains a positive chance of too many failures.
    with pytest.raises(ValueError):
        cp.size_for_power(0.001, 1.0, limbs=1)
    assert cp.size_for_power(0.0, 1.0) == 60


@pytest.mark.parametrize("args", [
    ("--true-rate", "0.03", "--power", "0.8", "--n", "630"),
    ("--true-rate", "0.03"),
])
def test_cli_requires_exactly_one_operation(args: tuple[str, ...]) -> None:
    proc = subprocess.run([sys.executable, str(SCRIPT), *args],
                          capture_output=True, text=True, check=False)
    assert proc.returncode == 2
    assert proc.stdout == ""
    assert "Traceback" not in proc.stderr


@pytest.mark.parametrize(("n", "p"), [(60, 0.05), (8000, 0.9), (8000, 0.049)])
def test_cdf_includes_all_probability_mass(n: int, p: float) -> None:
    assert list(cp._iter_lower_cdf(n, p))[-1] == (n, 1.0)


def test_near_one_alpha_matches_exact_integer_quantile() -> None:
    # Independent oracle: p=9/10 and alpha=999999999/10**9.
    # Avoid reproducing the floating-point recurrence under test.
    n = 8000
    denominator = 10 ** n
    total = 0
    term = 1  # C(n,0)*9**0
    expected = -1
    for k in range(n + 1):
        total += term
        if total * 10**9 > 999999999 * denominator:
            break
        expected = k
        term = term * (n - k) * 9 // (k + 1)
    assert expected == 7355
    assert cp.max_certifying_busts(n, 0.9, 0.999999999) == expected


@pytest.mark.parametrize("numerator", [1, 3, 7, 9])
def test_cdf_matches_small_exact_binomial_distribution(numerator: int) -> None:
    n = 25
    cumulative = 0
    for k, got in cp._iter_lower_cdf(n, numerator / 10):
        cumulative += math.comb(n, k) * numerator**k * (10 - numerator)**(n - k)
        assert got == pytest.approx(cumulative / 10**n, rel=2e-13, abs=1e-15)


# ── TB-P1 additive mode: pass-by-day speed limb (one-sided lower bound) ─────────
# Existing pins above are byte-identical; everything below is new surface only.

from fractions import Fraction  # noqa: E402


def _exact_min_passes(n: int, target: Fraction, alpha: Fraction) -> int:
    """Smallest k with P(X >= k; n, target) <= alpha, exact rationals."""
    for k in range(n + 2):
        upper = sum(
            Fraction(math.comb(n, i)) * target**i * (1 - target) ** (n - i)
            for i in range(k, n + 1)
        )
        if upper <= alpha:
            return k
    return -1


def test_min_certifying_passes_matches_exact_oracle() -> None:
    n = 100
    expected = _exact_min_passes(n, Fraction(1, 2), Fraction(1, 20))
    assert cp.min_certifying_passes(n, target=0.5, alpha=0.05) == expected
    assert expected == 59


def test_min_certifying_passes_preserves_inclusive_boundary() -> None:
    assert cp.min_certifying_passes(1, target=0.05, alpha=0.05) == 1
    assert cp.speed_limb_power(1, 1.0, target=0.05, alpha=0.05) == 1.0


def test_min_certifying_passes_none_when_n_too_small() -> None:
    assert cp.min_certifying_passes(3, target=0.5, alpha=0.05) == -1
    assert cp.speed_limb_power(3, 0.9, target=0.5, alpha=0.05) == 0.0


def test_speed_limb_power_matches_exact_small_binomial() -> None:
    n, q = 25, Fraction(7, 10)
    k_min = _exact_min_passes(n, Fraction(1, 2), Fraction(1, 20))
    exact = sum(
        Fraction(math.comb(n, i)) * q**i * (1 - q) ** (n - i) for i in range(k_min, n + 1)
    )
    got = cp.speed_limb_power(n, float(q), target=0.5, alpha=0.05)
    assert got == pytest.approx(float(exact), rel=2e-12, abs=1e-15)


def test_speed_limb_power_is_the_complement_of_the_failure_limb() -> None:
    # A lower bound on passes >= t is the upper bound on failures <= 1 - t.
    assert cp.speed_limb_power(300, 0.65, target=0.5) == pytest.approx(
        cp.per_limb_power(300, 0.35, ceiling=0.5), abs=1e-15
    )


def test_joint_power_four_formulas() -> None:
    assert cp.joint_power_four(0.9, 0.8, "independent") == pytest.approx(0.9**3 * 0.8)
    assert cp.joint_power_four(0.9, 0.8, "frechet") == pytest.approx(1 - 3 * 0.1 - 0.2)
    assert cp.joint_power_four(0.5, 0.5, "frechet") == 0.0
    with pytest.raises(ValueError):
        cp.joint_power_four(0.9, 0.8, "gaussian")


def test_size_for_joint_four_returns_first_grid_n_meeting_target() -> None:
    n = cp.size_for_joint_four(0.03, 0.65, 0.80, dependence="frechet")
    assert n % cp.DEFAULT_STEP == 0

    def joint(m: int) -> float:
        return cp.joint_power_four(
            cp.per_limb_power(m, 0.03), cp.speed_limb_power(m, 0.65), "frechet"
        )

    assert joint(n) >= 0.80
    assert all(joint(m) < 0.80 for m in range(cp.DEFAULT_STEP, n, cp.DEFAULT_STEP))


def test_size_for_joint_four_rejects_unattainable_perfect_power() -> None:
    with pytest.raises(ValueError, match="target_power 1.0 requires"):
        cp.size_for_joint_four(0.01, 0.9, 1.0)
    with pytest.raises(ValueError, match="target_power 1.0 requires"):
        cp.size_for_joint_four(0.0, 0.9, 1.0)


@pytest.mark.parametrize("kwargs", [{"target": 0.0}, {"target": 1.0}, {"alpha": 0.0}])
def test_speed_limb_rejects_out_of_domain(kwargs: dict) -> None:
    with pytest.raises(ValueError):
        cp.min_certifying_passes(100, **kwargs)


def test_cli_speed_mode_smoke_and_legacy_line_unchanged() -> None:
    legacy = subprocess.run(
        [sys.executable, str(SCRIPT), "--true-rate", "0.03", "--n", "630"],
        capture_output=True, text=True, check=False,
    )
    assert legacy.returncode == 0 and "per_limb=0.803" in legacy.stdout
    assert "speed_limb" not in legacy.stdout
    speed = subprocess.run(
        [sys.executable, str(SCRIPT), "--true-rate", "0.03", "--true-pass-rate", "0.65",
         "--n", "950"],
        capture_output=True, text=True, check=False,
    )
    assert speed.returncode == 0, speed.stderr
    assert "speed_limb=" in speed.stdout and "joint4_frechet=" in speed.stdout
    sized = subprocess.run(
        [sys.executable, str(SCRIPT), "--true-rate", "0.03", "--true-pass-rate", "0.65",
         "--power", "0.80", "--dependence", "frechet"],
        capture_output=True, text=True, check=False,
    )
    assert sized.returncode == 0, sized.stderr
    assert sized.stdout.startswith("n=") and "joint4=" in sized.stdout


def test_cli_speed_mode_rejects_bad_pass_target() -> None:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--true-rate", "0.03", "--true-pass-rate", "0.65",
         "--pass-target", "1.5", "--n", "100"],
        capture_output=True, text=True, check=False,
    )
    assert proc.returncode == 2 and proc.stdout == "" and "Traceback" not in proc.stderr
