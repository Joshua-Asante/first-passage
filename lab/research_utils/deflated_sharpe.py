#!/usr/bin/env python3
"""
deflated_sharpe.py — Deflated Sharpe Ratio (Bailey & Lopez de Prado, 2014).

Consumes the trial count K from the discovery ledger (futures-anomaly-discovery)
and deflates an observed Sharpe for BOTH (a) selection under K trials and (b) the
non-normality (skew, kurtosis) of the return distribution.

DSR = PSR(SR0), where SR0 is the expected maximum Sharpe under K independent
zero-edge trials. DSR is the probability the strategy's TRUE Sharpe exceeds that
selection benchmark. Pre-register the pass threshold before you compute it.

Sharpe convention: NON-annualized / per-observation, consistent with n. If you
hold an annualized Sharpe, divide by sqrt(periods_per_year) first, and express the
across-trials variance V in the same per-observation units. Mixing units silently
breaks the result.

Examples
--------
  # scalars (sr/n/skew/kurt computed elsewhere; K and V from the ledger):
  python deflated_sharpe.py --sr 0.075 --n 1200 --skew -0.4 --kurt 6.0 \
      --trials 48000 --var-trials 0.0009 --threshold 0.95

  # or derive sr/n/skew/kurt straight from a returns file (one return per line):
  python deflated_sharpe.py --returns-file es_trade_returns.txt \
      --trials 48000 --var-trials 0.0009
"""
import argparse
import math
import sys

try:
    from scipy.stats import norm
    _ppf, _cdf = norm.ppf, norm.cdf
    _BACKEND = "scipy"
except ImportError:  # pure-python fallbacks so the tool runs without scipy
    _BACKEND = "pure-python"

    def _cdf(x):
        return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

    def _ppf(p):  # Acklam's rational approximation to the inverse normal CDF
        if not (0.0 < p < 1.0):
            raise ValueError("ppf domain error")
        a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
             1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
        b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
             6.680131188771972e+01, -1.328068155288572e+01]
        c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
             -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
        d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
             3.754408661907416e+00]
        plow, phigh = 0.02425, 1 - 0.02425
        if p < plow:
            q = math.sqrt(-2 * math.log(p))
            return ((((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) /
                    (((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)))
        if p > phigh:
            q = math.sqrt(-2 * math.log(1 - p))
            return -((((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) /
                     (((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)))
        q = p - 0.5
        r = q * q
        return ((((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q /
                (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1))

GAMMA = 0.5772156649015329  # Euler-Mascheroni constant
E = math.e


def moments_from_returns(returns):
    """Per-observation Sharpe + biased central-moment skew/kurtosis (LdP convention)."""
    n = len(returns)
    if n < 3:
        raise ValueError("need at least 3 returns")
    mean = sum(returns) / n
    m2 = sum((x - mean) ** 2 for x in returns) / n
    m3 = sum((x - mean) ** 3 for x in returns) / n
    m4 = sum((x - mean) ** 4 for x in returns) / n
    if m2 <= 0:
        raise ValueError("zero variance in returns")
    sd = math.sqrt(m2)
    sr = mean / sd
    skew = m3 / (m2 ** 1.5)
    kurt = m4 / (m2 ** 2)  # non-excess (normal = 3)
    return sr, n, skew, kurt


def expected_max_sharpe(k, var_trials):
    """SR0: expected maximum of K draws from N(0, var_trials) (Lopez de Prado)."""
    if k < 1:
        raise ValueError("trials K must be >= 1")
    if k == 1:
        return 0.0  # no selection benchmark from a single trial
    sd = math.sqrt(var_trials)
    z1 = _ppf(1.0 - 1.0 / k)
    z2 = _ppf(1.0 - 1.0 / (k * E))
    return sd * ((1.0 - GAMMA) * z1 + GAMMA * z2)


def deflated_sharpe(sr, n, skew, kurt, sr0):
    """DSR = PSR(sr0). Probability in [0, 1]."""
    denom = 1.0 - skew * sr + ((kurt - 1.0) / 4.0) * sr * sr
    if denom <= 0:
        raise ValueError("non-normality denominator <= 0; check skew/kurt/SR inputs")
    z = (sr - sr0) * math.sqrt(n - 1.0) / math.sqrt(denom)
    return _cdf(z)


def main():
    ap = argparse.ArgumentParser(description="Deflated Sharpe Ratio (LdP 2014).")
    ap.add_argument("--returns-file", help="One return per line; derives sr/n/skew/kurt.")
    ap.add_argument("--sr", type=float, help="Observed per-observation Sharpe.")
    ap.add_argument("--n", type=int, help="Number of return observations.")
    ap.add_argument("--skew", type=float, help="Return skewness (gamma3).")
    ap.add_argument("--kurt", type=float, help="Return kurtosis, non-excess (normal=3).")
    ap.add_argument("--trials", type=int, help="K: trials/configs searched (from the ledger).")
    ap.add_argument("--var-trials", type=float,
                    help="V: variance of the Sharpe estimates across the K trials "
                         "(per-observation units). Required unless --sr0 given.")
    ap.add_argument("--sr0", type=float, help="Deflation benchmark directly (bypass K/V).")
    ap.add_argument("--threshold", type=float, default=0.95,
                    help="Pre-registered DSR pass threshold (informational). Default 0.95.")
    args = ap.parse_args()

    if args.returns_file:
        with open(args.returns_file) as fh:
            rets = [float(x) for x in fh.read().split() if x.strip()]
        sr, n, skew, kurt = moments_from_returns(rets)
        print(f"[derived] sr={sr:.5f}  n={n}  skew={skew:.4f}  kurt={kurt:.4f}")
    else:
        if None in (args.sr, args.n, args.skew, args.kurt):
            sys.exit("Provide --returns-file, or all of --sr --n --skew --kurt.")
        sr, n, skew, kurt = args.sr, args.n, args.skew, args.kurt

    if args.sr0 is not None:
        sr0 = args.sr0
        k_note = "supplied directly"
    else:
        if args.trials is None or args.var_trials is None:
            sys.exit("Provide --sr0, or both --trials (K) and --var-trials (V).")
        sr0 = expected_max_sharpe(args.trials, args.var_trials)
        k_note = f"K={args.trials:,}, V={args.var_trials:g}"

    dsr = deflated_sharpe(sr, n, skew, kurt, sr0)
    passed = dsr >= args.threshold

    print(f"[backend]  {_BACKEND}")
    print(f"[SR0]      deflation benchmark: {sr0:.5f}  ({k_note})")
    print(f"[DSR]      {dsr:.4f}   (threshold {args.threshold:g}: "
          f"{'PASS' if passed else 'FAIL'})")
    if sr <= sr0:
        print(f"[note]     observed SR ({sr:.5f}) <= benchmark ({sr0:.5f}) — "
              f"the edge does not clear what {args.trials or '?'} trials produce by chance.")
    if kurt >= 5 or skew < 0:
        print(f"[note]     non-normal returns (skew={skew:.2f}, kurt={kurt:.2f}) deflate the DSR; "
              f"this is intended, not a bug.")


if __name__ == "__main__":
    main()
