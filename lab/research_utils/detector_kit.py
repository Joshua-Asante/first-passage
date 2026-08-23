"""Cheap detector kit for tradable-anomalies T2 (constraint/flow family first).

Lo–MacKinlay overlapping variance ratio, Ljung-Box on r vs |r|, HAC-t on the
mean, and AR(1) autocorrelation-corrected n_eff. Report-only: no lock write.

Does not restore guardian_signal.py. Does not touch dd_protection.
"""
from __future__ import annotations

from typing import Any

import numpy as np
from statsmodels.regression.linear_model import OLS
from statsmodels.stats.diagnostic import acorr_ljungbox


def _finite(returns) -> np.ndarray:
    x = np.asarray(returns, dtype=float)
    return x[np.isfinite(x)]


def lo_mackinlay_vr(returns, q: int = 2) -> float:
    """Overlapping Lo–MacKinlay variance ratio VR(q). White noise → ≈ 1."""
    if q < 2:
        raise ValueError("q must be >= 2")
    x = _finite(returns)
    n = len(x)
    if n < q * 2:
        raise ValueError(f"need at least {q * 2} observations, got {n}")
    mu = float(x.mean())
    m1 = float(np.sum((x - mu) ** 2) / (n - 1))
    if m1 <= 0:
        return 1.0
    q_rets = np.convolve(x, np.ones(q), mode="valid")
    mq = float(np.sum((q_rets - q * mu) ** 2) / (q * (n - q + 1)))
    return mq / m1


def ljung_box_r_and_abs(returns, lags: int = 10) -> dict[str, Any]:
    """Ljung-Box on signed returns and on |r| (volatility clustering)."""
    x = _finite(returns)
    if len(x) <= lags + 2:
        raise ValueError("series shorter than lags+2")
    signed = acorr_ljungbox(x, lags=[lags], return_df=True)
    abs_r = acorr_ljungbox(np.abs(x), lags=[lags], return_df=True)
    return {
        "lags": lags,
        "r_stat": float(signed["lb_stat"].iloc[0]),
        "r_pvalue": float(signed["lb_pvalue"].iloc[0]),
        "abs_r_stat": float(abs_r["lb_stat"].iloc[0]),
        "abs_r_pvalue": float(abs_r["lb_pvalue"].iloc[0]),
    }


def hac_t_mean(returns, maxlags: int | None = None) -> dict[str, float]:
    """HAC-t for H0: E[r] = 0."""
    x = _finite(returns)
    if len(x) < 8:
        raise ValueError("need at least 8 observations for HAC-t")
    if maxlags is None:
        maxlags = max(1, int(np.floor(4 * (len(x) / 100.0) ** (2 / 9))))
    y = x
    design = np.ones((len(y), 1))
    fit = OLS(y, design).fit(cov_type="HAC", cov_kwds={"maxlags": maxlags})
    return {
        "mean": float(fit.params[0]),
        "tstat": float(fit.tvalues[0]),
        "pvalue": float(fit.pvalues[0]),
        "maxlags": float(maxlags),
    }


def n_eff_autocorr(returns) -> float:
    """Bartlett AR(1) n_eff = n (1-ρ)/(1+ρ). Known-AR → n_eff < n."""
    x = _finite(returns)
    n = len(x)
    if n < 3:
        return float(n)
    xc = x - x.mean()
    denom = float(np.dot(xc, xc))
    if denom <= 0:
        return float(n)
    rho = float(np.dot(xc[1:], xc[:-1]) / denom)
    if not np.isfinite(rho) or abs(rho) >= 1.0:
        return 1.0
    return float(n * (1.0 - rho) / (1.0 + rho))


def detector_report(returns, q: int = 2, lb_lags: int = 10) -> dict[str, Any]:
    """JSON-ready kit summary. Does not emit a lock decision."""
    x = _finite(returns)
    return {
        "n": int(len(x)),
        "vr_q": q,
        "variance_ratio": lo_mackinlay_vr(x, q=q),
        "ljung_box": ljung_box_r_and_abs(x, lags=lb_lags),
        "hac_t": hac_t_mean(x),
        "n_eff": n_eff_autocorr(x),
        "lock_decision": None,
    }
