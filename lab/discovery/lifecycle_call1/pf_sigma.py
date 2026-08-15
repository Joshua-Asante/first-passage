"""PF-per-bootstrap-draw σ over a supplied week-block panel (no core/mc state)."""
from __future__ import annotations

import numpy as np

# Zero-loss (all-wins / flat) draws are undefined for PF; they are skipped, not
# coerced to inf/nan that would poison decay_breach. Named so tests pin the
# convention explicitly.
ZERO_LOSS_SKIP = None


def pf_from_daily_pnl(daily_pnl: np.ndarray) -> float | None:
    """Gross profit factor from a 1-D daily P&L path.

    ``PF = Σ(positive) / |Σ(negative)|``. When there are no losses (all wins or
    flat), returns ``None`` (``ZERO_LOSS_SKIP``) — caller must not feed that
    into ``np.std`` as inf/nan.
    """
    arr = np.asarray(daily_pnl, dtype=float).ravel()
    if arr.size == 0:
        return ZERO_LOSS_SKIP
    wins = float(np.sum(arr[arr > 0.0]))
    losses = float(np.sum(arr[arr < 0.0]))
    if losses == 0.0:
        return ZERO_LOSS_SKIP
    return wins / abs(losses)


def pf_sigma_from_panel(
    daily_pnl_blocks: np.ndarray,
    n_draws: int,
    seed: int,
    *,
    blocks_per_draw: int | None = None,
) -> float:
    """σ of PF across block-bootstrap draws of a single-strategy panel.

    Parameters
    ----------
    daily_pnl_blocks
        Array shaped ``(n_blocks, days_per_block)`` — one strategy's week-block
        daily P&L. Reads only this argument; imports no MC engine module state.
    n_draws
        Number of bootstrap draws.
    seed
        RNG seed (deterministic).
    blocks_per_draw
        Blocks concatenated per draw; default = ``n_blocks`` (panel-length path).

    Returns
    -------
    float
        ``np.std`` of finite PF draws (ddof=0).

    Raises
    ------
    ValueError
        If fewer than 2 finite PF draws remain after skipping zero-loss paths.
    """
    blocks = np.asarray(daily_pnl_blocks, dtype=float)
    if blocks.ndim != 2:
        raise ValueError(
            f"daily_pnl_blocks must be 2-D (n_blocks, days_per_block); got {blocks.shape}"
        )
    n_blocks = blocks.shape[0]
    if n_blocks < 1:
        raise ValueError("daily_pnl_blocks has zero blocks")
    if n_draws < 1:
        raise ValueError(f"n_draws must be >= 1; got {n_draws}")

    path_len = n_blocks if blocks_per_draw is None else int(blocks_per_draw)
    if path_len < 1:
        raise ValueError(f"blocks_per_draw must be >= 1; got {path_len}")

    rng = np.random.default_rng(seed)
    pfs: list[float] = []
    for _ in range(n_draws):
        indices = rng.integers(0, n_blocks, path_len)
        path = np.concatenate([blocks[i] for i in indices])
        pf = pf_from_daily_pnl(path)
        if pf is not ZERO_LOSS_SKIP:
            pfs.append(float(pf))

    if len(pfs) < 2:
        raise ValueError(
            f"insufficient finite PF draws for sigma: {len(pfs)} finite of "
            f"{n_draws} draws (zero-loss paths are skipped, not coerced to inf/nan)"
        )
    return float(np.std(np.asarray(pfs, dtype=float), ddof=0))
