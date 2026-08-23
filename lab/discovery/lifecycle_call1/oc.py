"""Call-1 kill-line operating characteristics (synthetic / historical).

Reuses ``lifecycle.decay_breach``. Does **not** write ``lifecycle_state.json``.
T4 Task 3 (state writer) stays a separate GO; ``demote_writer`` is not called.
"""
from __future__ import annotations

from typing import Iterable

import numpy as np

from lifecycle import decay_breach


def oc_from_pf_paths(
    paths: Iterable[np.ndarray],
    *,
    baseline_pf: float,
    pf_sigma: float,
    k_sigma: float = 1.0,
    persist: int = 2,
) -> dict:
    """False-kill rate and mean detection lag on synthetic rolling-PF paths.

    A path "kills" when ``decay_breach`` is True for ``persist`` consecutive
    windows. Flat paths around baseline should not kill at ratified k=1.0.
    """
    if persist < 1:
        raise ValueError("persist must be >= 1")
    false_kills = 0
    lags: list[int] = []
    n_paths = 0
    for raw in paths:
        n_paths += 1
        path = np.asarray(raw, dtype=float)
        streak = 0
        killed_at: int | None = None
        for i, pf in enumerate(path):
            if decay_breach(float(pf), baseline_pf, pf_sigma, k_sigma=k_sigma):
                streak += 1
            else:
                streak = 0
            if streak >= persist:
                killed_at = i
                break
        if killed_at is not None:
            false_kills += 1
            lags.append(killed_at + 1)
    return {
        "n_paths": n_paths,
        "false_kill_rate": (false_kills / n_paths) if n_paths else float("nan"),
        "mean_detection_lag": float(np.mean(lags)) if lags else float("nan"),
        "n_detected": false_kills,
        "k_sigma": k_sigma,
        "persist": persist,
        "baseline_pf": baseline_pf,
        "pf_sigma": pf_sigma,
        "wrote_lifecycle_state": False,
    }
