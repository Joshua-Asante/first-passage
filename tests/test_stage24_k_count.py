"""Step 2.1 — K_DSR non-overlap floor + raw diagnostic bracket."""
from __future__ import annotations

from discovery.k_count import (
    CATCH22_FACE,
    DEFAULT_WINDOWS,
    RUPTURES_FACE,
    compute_k_bracket,
)


def test_k_dsr_equals_hand_computed_non_overlap_floor():
    """For a synthetic T, K_DSR = 22 + 1 + Σ⌊T/m⌋ over m∈{30,60,90}."""
    T = 9000
    bracket = compute_k_bracket(T, DEFAULT_WINDOWS)
    hand = CATCH22_FACE + RUPTURES_FACE + (T // 30) + (T // 60) + (T // 90)
    assert bracket.k_dsr == hand
    assert bracket.k_dsr == 22 + 1 + 300 + 150 + 100
    assert bracket.T == T
    assert bracket.windows == (30, 60, 90)


def test_k_raw_diagnostic_is_22_plus_3_n_subseq_not_bound():
    """Raw overlapping count is reported; it must NOT equal the binding floor."""
    T = 9000
    bracket = compute_k_bracket(T)
    n_subseq = T - 30 + 1  # shortest window
    assert bracket.n_subseq == n_subseq
    assert bracket.k_raw == 22 + 3 * n_subseq
    assert bracket.k_raw != bracket.k_dsr
    assert bracket.k_raw > bracket.k_dsr


def test_campaign_scale_t_yields_approx_3200():
    """Sanity: T≈52k (GC 1h IS ballpark) → K_DSR ≈ 3,200."""
    T = 52_000
    bracket = compute_k_bracket(T)
    assert 3_000 <= bracket.k_dsr <= 3_400
    assert bracket.as_dict()["bracket"]["floor_binding"] == bracket.k_dsr
