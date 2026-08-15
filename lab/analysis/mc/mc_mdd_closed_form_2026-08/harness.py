"""Drive production simulate_path with BM increments approximating Magdon-Ismail."""

from __future__ import annotations

import math
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

_ROOT = Path(__file__).resolve().parents[4]
for _p in (_ROOT, _ROOT / "core", Path(__file__).resolve().parent):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from mc.simulation import simulate_path  # noqa: E402

from closed_form import g_d  # noqa: E402

S0 = 100_000.0
UNREACHABLE_LOCK = 1_000_000.0
DD_TRIGGER_INERT = 999.0
DD_SCALE_ONE = 1.0
_N_WORKERS = 4


def firm_kwargs_absolute_trail(h: float, starting_equity: float = S0) -> dict:
    """Fixed-dollar trailing barrier h via trailing_locking + unreachable lock."""
    return dict(
        starting_equity=starting_equity,
        daily_loss_pct=None,
        dd_type="trailing_locking",
        trailing_dd_pct=-h / starting_equity,
        dd_lock_offset_usd=UNREACHABLE_LOCK,
        profit_target=starting_equity * 1_000.0,
        min_trading_days=0,
        inactivity_limit=10_000_000,
        consistency_frac=None,
    )


def bm_increments(
    mu: float,
    sigma: float,
    T: float,
    n_steps: int,
    rng: np.random.Generator,
) -> np.ndarray:
    dt = T / n_steps
    z = rng.standard_normal(n_steps)
    return mu * dt + sigma * math.sqrt(dt) * z


def path_from_increments(increments: np.ndarray) -> np.ndarray:
    return np.asarray(increments, dtype=float).reshape(-1, 1)


def simulate_bust(
    increments: np.ndarray,
    h: float,
    starting_equity: float = S0,
) -> bool:
    path = path_from_increments(increments)
    kw = firm_kwargs_absolute_trail(h, starting_equity)
    outcome, _day, _mdd, _culprit = simulate_path(
        path,
        DD_TRIGGER_INERT,
        DD_SCALE_ONE,
        len(increments),
        **kw,
    )
    return outcome == "bust_trailing"


def _worker_batch(args: tuple) -> int:
    """Return bust count for a contiguous seed-offset batch (picklable)."""
    mu, sigma, h, T, n_steps, n_paths, seed = args
    import math as _math
    import sys as _sys
    from pathlib import Path as _Path

    import numpy as _np

    root = _Path(__file__).resolve().parents[4]
    for p in (root, root / "core", _Path(__file__).resolve().parent):
        if str(p) not in _sys.path:
            _sys.path.insert(0, str(p))
    from mc.simulation import simulate_path as _sp  # noqa: PLC0415

    s0 = 100_000.0
    kw = dict(
        starting_equity=s0,
        daily_loss_pct=None,
        dd_type="trailing_locking",
        trailing_dd_pct=-h / s0,
        dd_lock_offset_usd=1_000_000.0,
        profit_target=s0 * 1_000.0,
        min_trading_days=0,
        inactivity_limit=10_000_000,
        consistency_frac=None,
    )
    rng = _np.random.default_rng(seed)
    dt = T / n_steps
    busts = 0
    for _ in range(n_paths):
        incr = mu * dt + sigma * _math.sqrt(dt) * rng.standard_normal(n_steps)
        path = _np.asarray(incr, dtype=float).reshape(-1, 1)
        outcome, *_rest = _sp(path, 999.0, 1.0, n_steps, **kw)
        if outcome == "bust_trailing":
            busts += 1
    return busts


def mc_bust_rate(
    mu: float,
    sigma: float,
    h: float,
    T: float,
    n_steps: int,
    n_paths: int,
    seed: int,
    n_workers: int = _N_WORKERS,
) -> dict:
    if n_workers <= 1 or n_paths < n_workers * 10:
        rng = np.random.default_rng(seed)
        busts = 0
        for _ in range(n_paths):
            incr = bm_increments(mu, sigma, T, n_steps, rng)
            if simulate_bust(incr, h):
                busts += 1
    else:
        base = n_paths // n_workers
        rem = n_paths % n_workers
        batches = []
        offset = 0
        for w in range(n_workers):
            n = base + (1 if w < rem else 0)
            batches.append((mu, sigma, h, T, n_steps, n, seed + 1_000_003 * w + offset))
            offset += n
        with ProcessPoolExecutor(max_workers=n_workers) as pool:
            busts = sum(pool.map(_worker_batch, batches))

    p = busts / n_paths
    se = math.sqrt(p * (1.0 - p) / n_paths)
    g = g_d(h, mu, sigma, T)
    abs_err = abs(p - g)
    tol = max(0.02, 3.0 * se)
    return {
        "mu": mu,
        "sigma": sigma,
        "h": h,
        "T": T,
        "n_steps": n_steps,
        "n_paths": n_paths,
        "seed": seed,
        "p_mc": p,
        "se": se,
        "G_D": g,
        "abs_err": abs_err,
        "tol": tol,
        "agree": abs_err <= tol,
        "signed_err": p - g,
        "dt": T / n_steps,
        "sigma_sqrt_dt_over_h": (sigma * math.sqrt(T / n_steps)) / h,
    }


# Default validation grid from the plan
GRID = (
    {"name": "driftless_A", "mu": 0.0, "sigma": 1.0, "h": 2.0, "T": 1.0, "n_steps": 2000, "n_paths": 20_000, "seed": 20260813},
    {"name": "driftless_B", "mu": 0.0, "sigma": 1.0, "h": 3.0, "T": 4.0, "n_steps": 4000, "n_paths": 20_000, "seed": 20260814},
    {"name": "pos_drift_A", "mu": 0.5, "sigma": 1.0, "h": 2.0, "T": 4.0, "n_steps": 4000, "n_paths": 20_000, "seed": 20260815},
    {"name": "pos_drift_B", "mu": 1.0, "sigma": 1.0, "h": 3.0, "T": 9.0, "n_steps": 5000, "n_paths": 20_000, "seed": 20260816},
)
