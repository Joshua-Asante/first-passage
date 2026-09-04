#!/usr/bin/env python3
"""Certification-power calculator for a one-sided binomial bust-rate bound.

Stdlib only. Manual/local — not wired into gates.yml.

Identity (campaign tables): the one-sided (1-alpha) Clopper-Pearson upper
bound on k/n is <= ceiling iff BinomCDF(k; n, ceiling) <= alpha.
Certification power at true rate p is BinomCDF(k_max; n, p). Joint power
over L limbs is q**L under independence, or max(0, 1 - L*(1-q)) with no
dependence assumption (Fréchet).

``math.comb`` is the coefficient; the CDF is summed in log-space via
``math.lgamma`` so n up to n_max does not overflow float.
"""
from __future__ import annotations

import argparse
import math

DEFAULT_CEILING = 0.05
DEFAULT_ALPHA = 0.05
DEFAULT_LIMBS = 3
DEFAULT_STEP = 10
DEFAULT_N_MAX = 8000
DEPENDENCE_INDEPENDENT = "independent"
DEPENDENCE_FRECHET = "frechet"
DEPENDENCE_CHOICES = (DEPENDENCE_INDEPENDENT, DEPENDENCE_FRECHET)


def _log_comb(n: int, i: int) -> float:
    """log(math.comb(n, i)); lgamma fallback when the integer overflows float."""
    try:
        return math.log(math.comb(n, i))
    except (ValueError, OverflowError):
        return math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1)


def _log_binom_pmf(n: int, i: int, p: float) -> float:
    """log(C(n, i) * p**i * (1-p)**(n-i)); C(n, i) is math.comb(n, i)."""
    if p <= 0.0:
        return 0.0 if i == 0 else float("-inf")
    if p >= 1.0:
        return 0.0 if i == n else float("-inf")
    return _log_comb(n, i) + i * math.log(p) + (n - i) * math.log(1.0 - p)


def _binom_cdf(k: int, n: int, p: float) -> float:
    """P(X <= k) for X ~ Binomial(n, p)."""
    if k < 0:
        return 0.0
    if k >= n:
        return 1.0
    if p <= 0.0:
        return 1.0
    if p >= 1.0:
        return 1.0 if k >= n else 0.0
    logs = [_log_binom_pmf(n, i, p) for i in range(k + 1)]
    peak = max(logs)
    if peak == float("-inf"):
        return 0.0
    return math.fsum(math.exp(x - peak) for x in logs) * math.exp(peak)


def max_certifying_busts(
    n: int, ceiling: float = DEFAULT_CEILING, alpha: float = DEFAULT_ALPHA
) -> int:
    """Largest k with BinomCDF(k; n, ceiling) <= alpha, else -1.

    Equivalent to: the one-sided (1-alpha) Clopper-Pearson upper bound
    on k/n is <= ceiling.
    """
    if n < 1:
        return -1
    best = -1
    for k in range(n + 1):
        if _binom_cdf(k, n, ceiling) <= alpha:
            best = k
        else:
            break
    return best


def per_limb_power(
    n: int,
    true_rate: float,
    ceiling: float = DEFAULT_CEILING,
    alpha: float = DEFAULT_ALPHA,
) -> float:
    """BinomCDF(max_certifying_busts(n); n, true_rate); 0.0 when no count certifies."""
    k_max = max_certifying_busts(n, ceiling=ceiling, alpha=alpha)
    if k_max < 0:
        return 0.0
    return _binom_cdf(k_max, n, true_rate)


def joint_power(q: float, limbs: int, dependence: str) -> float:
    """independence -> q**limbs; frechet -> max(0, 1 - limbs*(1-q)); else ValueError."""
    if dependence == DEPENDENCE_INDEPENDENT:
        return q**limbs
    if dependence == DEPENDENCE_FRECHET:
        return max(0.0, 1.0 - limbs * (1.0 - q))
    raise ValueError(
        f"dependence must be one of {DEPENDENCE_CHOICES}, got {dependence!r}"
    )


def size_for_power(
    true_rate: float,
    target: float,
    *,
    limbs: int = DEFAULT_LIMBS,
    dependence: str = DEPENDENCE_INDEPENDENT,
    ceiling: float = DEFAULT_CEILING,
    alpha: float = DEFAULT_ALPHA,
    step: int = DEFAULT_STEP,
    n_max: int = DEFAULT_N_MAX,
) -> int:
    """Smallest n on range(step, n_max+1, step) meeting the joint-power target.

    Raises ValueError if none by n_max.
    """
    if step < 1:
        raise ValueError(f"step must be >= 1, got {step}")
    for n in range(step, n_max + 1, step):
        q = per_limb_power(n, true_rate, ceiling=ceiling, alpha=alpha)
        if joint_power(q, limbs, dependence) >= target:
            return n
    raise ValueError(
        f"no n <= {n_max} on step {step} meets joint power {target} "
        f"(true_rate={true_rate}, limbs={limbs}, dependence={dependence})"
    )


def _fmt_prob(value: float) -> str:
    return f"{value:.3f}"


def _fmt_param(value: float) -> str:
    return f"{value:g}"


def format_size_line(
    n: int,
    true_rate: float,
    *,
    limbs: int,
    dependence: str,
    ceiling: float,
    alpha: float,
    step: int,
) -> str:
    q = per_limb_power(n, true_rate, ceiling=ceiling, alpha=alpha)
    joint = joint_power(q, limbs, dependence)
    k_max = max_certifying_busts(n, ceiling=ceiling, alpha=alpha)
    return (
        f"n={n} per_limb={_fmt_prob(q)} joint={_fmt_prob(joint)} "
        f"max_busts={k_max} (ceiling={_fmt_param(ceiling)} "
        f"alpha={_fmt_param(alpha)} limbs={limbs} dependence={dependence} "
        f"step={step})"
    )


def format_eval_line(
    n: int,
    true_rate: float,
    *,
    ceiling: float,
    alpha: float,
    limbs: int,
) -> str:
    q = per_limb_power(n, true_rate, ceiling=ceiling, alpha=alpha)
    k_max = max_certifying_busts(n, ceiling=ceiling, alpha=alpha)
    j_ind = joint_power(q, limbs, DEPENDENCE_INDEPENDENT)
    j_fr = joint_power(q, limbs, DEPENDENCE_FRECHET)
    return (
        f"n={n} per_limb={_fmt_prob(q)} "
        f"joint_independent={_fmt_prob(j_ind)} "
        f"joint_frechet={_fmt_prob(j_fr)} max_busts={k_max}"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--true-rate", type=float, required=True)
    parser.add_argument("--power", type=float, default=None)
    parser.add_argument("--n", type=int, default=None)
    parser.add_argument("--limbs", type=int, default=DEFAULT_LIMBS)
    parser.add_argument(
        "--dependence",
        choices=DEPENDENCE_CHOICES,
        default=DEPENDENCE_INDEPENDENT,
    )
    parser.add_argument("--ceiling", type=float, default=DEFAULT_CEILING)
    parser.add_argument("--alpha", type=float, default=DEFAULT_ALPHA)
    parser.add_argument("--step", type=int, default=DEFAULT_STEP)
    parser.add_argument("--n-max", type=int, default=DEFAULT_N_MAX)
    args = parser.parse_args(argv)

    if args.power is not None:
        n = size_for_power(
            args.true_rate,
            args.power,
            limbs=args.limbs,
            dependence=args.dependence,
            ceiling=args.ceiling,
            alpha=args.alpha,
            step=args.step,
            n_max=args.n_max,
        )
        print(
            format_size_line(
                n,
                args.true_rate,
                limbs=args.limbs,
                dependence=args.dependence,
                ceiling=args.ceiling,
                alpha=args.alpha,
                step=args.step,
            )
        )
        return 0
    if args.n is not None:
        print(
            format_eval_line(
                args.n,
                args.true_rate,
                ceiling=args.ceiling,
                alpha=args.alpha,
                limbs=args.limbs,
            )
        )
        return 0
    parser.error("one of --power or --n is required")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
