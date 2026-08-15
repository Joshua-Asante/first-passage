"""K_DSR / K_raw bracket for matrix-profile discovery campaigns.

Implements the ADR 2026-07-12 non-overlap floor (binding) plus the raw
overlapping diagnostic the pre-reg §2 requires reported together:

    K_DSR = 22 (catch22 face) + 1 (ruptures face) + Σ_m ⌊T / m⌋
    K_raw = 22 + 3 · N_subseq     (diagnostic only — never the bound K)

The bound integer is computed from T (and the frozen window set) at
``register_search open`` time; this module never hardcodes a campaign K.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

CATCH22_FACE = 22
RUPTURES_FACE = 1
DEFAULT_WINDOWS: tuple[int, ...] = (30, 60, 90)


@dataclass(frozen=True)
class KBracket:
    """Binding floor + raw diagnostic for one IS bar count T."""

    T: int
    windows: tuple[int, ...]
    k_dsr: int
    k_raw: int
    n_subseq: int
    per_window_floor: dict[int, int]
    per_window_overlap: dict[int, int]

    def as_dict(self) -> dict:
        return {
            "T": self.T,
            "windows": list(self.windows),
            "k_dsr": self.k_dsr,
            "k_raw": self.k_raw,
            "n_subseq": self.n_subseq,
            "per_window_floor": {str(k): v for k, v in self.per_window_floor.items()},
            "per_window_overlap": {
                str(k): v for k, v in self.per_window_overlap.items()
            },
            "bracket": {
                "floor_binding": self.k_dsr,
                "raw_overlapping": self.k_raw,
            },
        }


def compute_k_bracket(
    T: int,
    windows: Sequence[int] | Iterable[int] = DEFAULT_WINDOWS,
) -> KBracket:
    """Compute the ADR §2.1 K_DSR non-overlap floor and the raw diagnostic.

    Parameters
    ----------
    T :
        IS bar count (e.g. GC 1h bars in 2010-01-01:2018-12-31).
    windows :
        Frozen STUMPY window set (default m ∈ {30, 60, 90}).
    """
    if T < 1:
        raise ValueError(f"T must be >= 1, got {T}")
    wins = tuple(int(m) for m in windows)
    if not wins:
        raise ValueError("windows must be non-empty")
    if any(m < 1 for m in wins):
        raise ValueError(f"window lengths must be >= 1, got {wins}")

    per_floor = {m: T // m for m in wins}
    per_overlap = {m: max(T - m + 1, 0) for m in wins}
    # N_subseq for the pre-reg raw form 22 + 3·N_subseq: subsequences at the
    # shortest frozen window (largest overlap count under the frozen set).
    m_min = min(wins)
    n_subseq = per_overlap[m_min]
    k_dsr = CATCH22_FACE + RUPTURES_FACE + sum(per_floor.values())
    # Literal pre-reg raw diagnostic (not a sum of per-window overlaps).
    k_raw = CATCH22_FACE + len(wins) * n_subseq
    return KBracket(
        T=T,
        windows=wins,
        k_dsr=k_dsr,
        k_raw=k_raw,
        n_subseq=n_subseq,
        per_window_floor=per_floor,
        per_window_overlap=per_overlap,
    )
