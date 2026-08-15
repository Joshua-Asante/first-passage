"""Stage-2 miner — STUMPY motifs/discords, catch22 covariates, ruptures labels.

Research-venv-only (stumpy / pycatch22 / ruptures). Catch22 is covariate-only
(§0.5(A)): contributes face-count to K_DSR, emits zero scored columns.
Regime labels are side-channel test conditions — never filters.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from discovery.k_count import DEFAULT_WINDOWS

# Optional research deps — importorskip in tests; fail loud at mine time.
try:
    import stumpy  # type: ignore
    _STUMPY_OK = True
except ImportError:  # pragma: no cover
    _STUMPY_OK = False

try:
    import ruptures as rpt  # type: ignore
    _RUPTURES_OK = True
except ImportError:  # pragma: no cover
    _RUPTURES_OK = False

# catch22 is covariate-only and optional; never block mining if absent/slow.
try:
    import pycatch22  # type: ignore
    _CATCH22_OK = True
except ImportError:  # pragma: no cover
    _CATCH22_OK = False


PELT_PENALTY = 10.0  # single fixed penalty (pre-registered; no sweep)


@dataclass(frozen=True)
class MotifHit:
    kind: str  # "motif" | "discord"
    m: int
    index: int
    mp_value: float
    shape: np.ndarray


@dataclass(frozen=True)
class MineResult:
    hits: list[MotifHit]
    regime_labels: np.ndarray  # int labels, length = len(series)
    catch22_covariates: dict[str, float]  # diagnostic only — not scored columns
    series_norm: np.ndarray


def vol_ushape_normalize(returns: np.ndarray, hours: np.ndarray) -> np.ndarray:
    """Pre-mining hygiene: divide returns by hour-of-day vol (U-shape)."""
    r = np.asarray(returns, dtype=float)
    out = np.zeros_like(r)
    for h in np.unique(hours):
        mask = hours == h
        sd = r[mask].std(ddof=1)
        out[mask] = r[mask] / sd if sd > 1e-12 else r[mask]
    return out


def zshape(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    sd = x.std(ddof=1)
    if sd <= 0:
        return x - x.mean()
    return (x - x.mean()) / sd


def mine_series(
    series: np.ndarray,
    *,
    hours: np.ndarray | None = None,
    windows: tuple[int, ...] = DEFAULT_WINDOWS,
    normalize: bool = True,
    run_catch22: bool = False,
    run_stumpy: bool = True,
    run_ruptures: bool = True,
) -> MineResult:
    """Run STUMPY (motif+discord per m) + optional catch22 covariates + ruptures PELT.

    ``run_catch22`` defaults False — catch22 is covariate-only (0 scored columns)
    and is opt-in so unit tests / short shakedowns are not blocked by it.
    ``run_stumpy`` / ``run_ruptures`` default True (byte-identical legacy path);
    a real campaign splits them because PELT-RBF needs an n^2 Gram matrix —
    tractable on the daily series, not on ~52K hourly bars — while STUMPY hits
    must come only from the pre-registered hourly series (K-budget discipline).
    """
    if run_stumpy and not _STUMPY_OK:
        raise RuntimeError("stumpy is not importable — run under .venv-research.")
    if run_ruptures and not _RUPTURES_OK:
        raise RuntimeError("ruptures is not importable — run under .venv-research.")

    x = np.asarray(series, dtype=float)
    if hours is None:
        hours = np.zeros(len(x), dtype=int)
    series_norm = vol_ushape_normalize(x, hours) if normalize else x.copy()

    hits: list[MotifHit] = []
    for m in windows if run_stumpy else ():
        if len(series_norm) < 2 * m:
            continue
        mp = stumpy.stump(series_norm, m=m)
        # Matrix profile column 0 = distance; motif = argmin, discord = argmax.
        motif_idx = int(np.argmin(mp[:, 0]))
        discord_idx = int(np.argmax(mp[:, 0]))
        hits.append(
            MotifHit(
                kind="motif",
                m=m,
                index=motif_idx,
                mp_value=float(mp[motif_idx, 0]),
                shape=zshape(series_norm[motif_idx : motif_idx + m]),
            )
        )
        hits.append(
            MotifHit(
                kind="discord",
                m=m,
                index=discord_idx,
                mp_value=float(mp[discord_idx, 0]),
                shape=zshape(series_norm[discord_idx : discord_idx + m]),
            )
        )

    # ruptures PELT on the normalized series — labels only.
    labels = np.zeros(len(series_norm), dtype=int)
    if run_ruptures:
        min_size = max(24, min(windows)) if windows else 24
        algo = rpt.Pelt(model="rbf", min_size=min_size).fit(series_norm)
        bkps = algo.predict(pen=PELT_PENALTY)
        start = 0
        for i, b in enumerate(bkps):
            labels[start:b] = i
            start = b

    covariates: dict[str, float] = {}
    if run_catch22 and _CATCH22_OK:
        try:
            feats = pycatch22.catch22_all(series_norm.tolist())
            names = feats.get("names") or feats.get("feature_names") or []
            values = feats.get("values") or feats.get("feature_values") or []
            covariates = {str(n): float(v) for n, v in zip(names, values)}
        except Exception:
            covariates = {"catch22_error": 1.0}
    elif run_catch22:
        covariates = {"catch22_unavailable": 1.0}
    else:
        covariates = {"catch22_skipped": 1.0}

    return MineResult(
        hits=hits,
        regime_labels=labels,
        catch22_covariates=covariates,
        series_norm=series_norm,
    )


def best_hit_distance_to_shape(
    hits: list[MotifHit], target: np.ndarray
) -> tuple[MotifHit | None, float]:
    """Return the hit whose shape is closest (z-EU) to ``target``."""
    target_z = zshape(target)
    best = None
    best_d = float("inf")
    for h in hits:
        if h.shape.size != target_z.size:
            continue
        d = float(np.linalg.norm(h.shape - target_z))
        if d < best_d:
            best_d = d
            best = h
    return best, best_d
