"""Motif → frozen IS-derived trading rule (candidate → return-series interface).

All rule parameters (shape, trigger, direction, horizon) are frozen from IS.
OOS bars are evaluated only — never re-fit. (§5 forbidden: OOS re-optimization.)
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass

import numpy as np

from discovery.miner import MotifHit, zshape


@dataclass(frozen=True)
class FrozenRule:
    """IS-derived rule: match trailing window to frozen shape; trade frozen dir."""

    candidate_id: str
    kind: str
    m: int
    shape: np.ndarray
    trigger: float
    direction: int
    horizon: int
    shape_hash: str
    source_index: int

    def as_provenance(self) -> dict:
        return {
            "candidate_id": self.candidate_id,
            "kind": self.kind,
            "m": self.m,
            "trigger": self.trigger,
            "direction": self.direction,
            "horizon": self.horizon,
            "shape_hash": self.shape_hash,
            "source_index": self.source_index,
        }


def _shape_hash(shape: np.ndarray) -> str:
    raw = np.asarray(shape, dtype=np.float64).tobytes()
    return hashlib.sha256(raw).hexdigest()[:16]


def _rolling_z_distance(series: np.ndarray, shape: np.ndarray) -> np.ndarray:
    """Z-normalized Euclidean distance of each trailing window to ``shape``."""
    x = np.asarray(series, dtype=float)
    s = zshape(shape)
    m = s.size
    n = x.size
    out = np.full(n, np.nan)
    for i in range(m - 1, n):
        w = x[i - m + 1 : i + 1]
        out[i] = float(np.linalg.norm(zshape(w) - s))
    return out


def freeze_rule_from_hit(
    hit: MotifHit,
    series_is: np.ndarray,
    *,
    horizon: int,
    trigger_quantile: float = 0.05,
    candidate_id: str | None = None,
) -> FrozenRule:
    """Freeze trigger + direction from IS only (forward-return sign at hit)."""
    x = np.asarray(series_is, dtype=float)
    m = hit.m
    # Direction = sign of mean IS forward return after the mined index.
    end = min(hit.index + m + horizon, len(x))
    start = hit.index + m
    fwd = x[start:end]
    direction = 1 if (fwd.mean() if fwd.size else 0.0) >= 0 else -1
    dists = _rolling_z_distance(x, hit.shape)
    valid = dists[np.isfinite(dists)]
    trigger = float(np.quantile(valid, trigger_quantile)) if valid.size else 0.0
    cid = candidate_id or f"{hit.kind}_m{hit.m}_{hit.index}"
    return FrozenRule(
        candidate_id=cid,
        kind=hit.kind,
        m=m,
        shape=np.asarray(hit.shape, dtype=float).copy(),
        trigger=trigger,
        direction=direction,
        horizon=int(horizon),
        shape_hash=_shape_hash(hit.shape),
        source_index=hit.index,
    )


def freeze_rule_from_spec(
    shape: np.ndarray,
    *,
    direction: int,
    horizon: int,
    trigger: float,
    m: int | None = None,
    candidate_id: str = "planted_motif",
    kind: str = "motif",
) -> FrozenRule:
    """Build a frozen rule from a known shape (synthetic / oracle path)."""
    s = zshape(shape)
    return FrozenRule(
        candidate_id=candidate_id,
        kind=kind,
        m=int(m or s.size),
        shape=s,
        trigger=float(trigger),
        direction=int(direction),
        horizon=int(horizon),
        shape_hash=_shape_hash(s),
        source_index=-1,
    )


@dataclass
class RuleEval:
    bar_returns: np.ndarray  # per-bar strategy return (net later)
    trade_returns: list[float]
    entry_indices: list[int]
    n_trades: int


def evaluate_rule(
    rule: FrozenRule,
    series: np.ndarray,
    *,
    cost_frac_per_rt: float = 0.0,
) -> RuleEval:
    """Evaluate a frozen rule on an era series (IS or OOS). No parameter updates."""
    x = np.asarray(series, dtype=float)
    n = x.size
    bar_ret = np.zeros(n, dtype=float)
    trade_returns: list[float] = []
    entries: list[int] = []
    dists = _rolling_z_distance(x, rule.shape)
    i = rule.m - 1
    while i < n - rule.horizon:
        if np.isfinite(dists[i]) and dists[i] < rule.trigger:
            # Entry at next bar; hold ``horizon`` bars of underlying simple returns.
            entry = i + 1
            exit_i = entry + rule.horizon
            if exit_i > n:
                break
            # series here is returns; sum over hold = simple approx for small r.
            seg = x[entry:exit_i]
            gross = float(rule.direction * seg.sum())
            net = gross - cost_frac_per_rt
            trade_returns.append(net)
            entries.append(entry)
            # Attribute trade PnL evenly across hold bars for the bar matrix.
            bar_ret[entry:exit_i] += net / rule.horizon
            i = exit_i  # no overlapping re-entry
        else:
            i += 1
    return RuleEval(
        bar_returns=bar_ret,
        trade_returns=trade_returns,
        entry_indices=entries,
        n_trades=len(trade_returns),
    )
