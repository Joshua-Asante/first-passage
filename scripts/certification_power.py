#!/usr/bin/env python3
"""Certification-power calculator for a one-sided binomial bust-rate bound.

Stdlib only. Manual/local — not wired into gates.yml.

Identity (campaign tables): the one-sided (1-alpha) Clopper-Pearson upper
bound on k/n is <= ceiling iff BinomCDF(k; n, ceiling) <= alpha.
Certification power at true rate p is BinomCDF(k_max; n, p). Joint power
over L limbs is q**L under independence, or max(0, 1 - L*(1-q)) with no
dependence assumption (Fréchet).

``math.comb`` is the coefficient; the lower-tail CDF is accumulated once
in log space (peak-shifted recurrence) so n up to n_max stays in float.
"""
from __future__ import annotations

import argparse
import math
from collections.abc import Iterator

DEFAULT_CEILING = 0.05
DEFAULT_ALPHA = 0.05
DEFAULT_LIMBS = 3
DEFAULT_STEP = 10
DEFAULT_N_MAX = 8000
DEPENDENCE_INDEPENDENT = "independent"
DEPENDENCE_FRECHET = "frechet"
DEPENDENCE_CHOICES = (DEPENDENCE_INDEPENDENT, DEPENDENCE_FRECHET)


def _require_n(n: int) -> None:
    if n < 1:
        raise ValueError(f"n must be >= 1, got {n}")


def _require_unit_interval(name: str, value: float) -> None:
    if not math.isfinite(value) or value < 0.0 or value > 1.0:
        raise ValueError(f"{name} must be a finite value in [0, 1], got {value!r}")


def _require_open_unit(name: str, value: float) -> None:
    if not math.isfinite(value) or value <= 0.0 or value >= 1.0:
        raise ValueError(f"{name} must be in (0, 1), got {value!r}")


def _require_target(value: float) -> None:
    if not math.isfinite(value) or value <= 0.0 or value > 1.0:
        raise ValueError(f"target must be in (0, 1], got {value!r}")


def _require_limbs(limbs: int) -> None:
    if limbs < 1:
        raise ValueError(f"limbs must be >= 1, got {limbs}")


def _iter_lower_cdf(n: int, p: float) -> Iterator[tuple[int, float]]:
    """Yield (k, BinomCDF(k; n, p)) incrementally in one left-to-right pass."""
    if p <= 0.0:
        for k in range(n + 1):
            yield k, 1.0
        return
    if p >= 1.0:
        for k in range(n):
            yield k, 0.0
        yield n, 1.0
        return

    log_odds = math.log(p) - math.log(1.0 - p)
    log_term = n * math.log(1.0 - p)
    peak = log_term
    scaled = 1.0
    for k in range(n + 1):
        cdf = scaled * math.exp(peak)
        if cdf > 1.0:
            cdf = 1.0
        yield k, cdf
        if k == n:
            return
        log_term = log_term + math.log(n - k) - math.log(k + 1) + log_odds
        if log_term > peak:
            scaled *= math.exp(peak - log_term)
            peak = log_term
        scaled += math.exp(log_term - peak)


def _binom_cdf(k: int, n: int, p: float) -> float:
    """P(X <= k) for X ~ Binomial(n, p). One incremental pass."""
    if k < 0:
        return 0.0
    if k >= n:
        return 1.0
    last = 0.0
    for i, cdf in _iter_lower_cdf(n, p):
        last = cdf
        if i >= k:
            return cdf
    return last


def max_certifying_busts(
    n: int, ceiling: float = DEFAULT_CEILING, alpha: float = DEFAULT_ALPHA
) -> int:
    """Largest k with BinomCDF(k; n, ceiling) <= alpha, else -1.

    Equivalent to: the one-sided (1-alpha) Clopper-Pearson upper bound
    on k/n is <= ceiling. Accumulates the lower tail once and stops at
    the first k whose CDF exceeds alpha.
    """
    _require_n(n)
    _require_open_unit("ceiling", ceiling)
    _require_open_unit("alpha", alpha)
    best = -1
    for k, cdf in _iter_lower_cdf(n, ceiling):
        if cdf <= alpha:
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
    _require_unit_interval("true_rate", true_rate)
    k_max = max_certifying_busts(n, ceiling=ceiling, alpha=alpha)
    if k_max < 0:
        return 0.0
    return _binom_cdf(k_max, n, true_rate)


def joint_power(q: float, limbs: int, dependence: str) -> float:
    """independence -> q**limbs; frechet -> max(0, 1 - limbs*(1-q)); else ValueError."""
    _require_unit_interval("q", q)
    _require_limbs(limbs)
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

    Linear grid scan — joint power is not guaranteed monotone, so no
    binary search over n. Raises ValueError if none by n_max.
    """
    _require_unit_interval("true_rate", true_rate)
    _require_target(target)
    _require_limbs(limbs)
    _require_open_unit("ceiling", ceiling)
    _require_open_unit("alpha", alpha)
    if step < 1:
        raise ValueError(f"step must be >= 1, got {step}")
    if n_max < step:
        raise ValueError(f"n_max must be >= step, got n_max={n_max} step={step}")
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

    try:
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
    except ValueError as exc:
        parser.error(str(exc))
    parser.error("one of --power or --n is required")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
