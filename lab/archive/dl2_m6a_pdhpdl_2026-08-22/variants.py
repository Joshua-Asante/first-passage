"""DL-2 prereg Sec2 -- the frozen variant set (K_intrinsic = 10). Closed set:
no variant may be added, retuned, or substituted after any train number is
seen (D-K1). This table is a verbatim transcription of the prereg Sec2 table."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Variant:
    v: int
    lookback: int             # 1 or 2 sessions
    drift: str                # "unconditional" | "aligned"
    entry_style: str          # "close_confirm" | "retest_limit"
    target_r: float           # 2.0 or 3.0


VARIANTS: tuple[Variant, ...] = (
    Variant(1, 1, "unconditional", "close_confirm", 2.0),
    Variant(2, 1, "unconditional", "close_confirm", 3.0),
    Variant(3, 1, "aligned",       "close_confirm", 2.0),
    Variant(4, 1, "aligned",       "close_confirm", 3.0),
    Variant(5, 2, "unconditional", "close_confirm", 2.0),
    Variant(6, 2, "unconditional", "close_confirm", 3.0),
    Variant(7, 2, "aligned",       "close_confirm", 3.0),
    Variant(8, 1, "aligned",       "retest_limit",  2.0),
    Variant(9, 2, "aligned",       "retest_limit",  3.0),
    Variant(10, 1, "unconditional", "retest_limit", 2.0),
)

assert len(VARIANTS) == 10, "K_intrinsic = 10 is frozen -- Sec2 closed set"
assert [v.v for v in VARIANTS] == list(range(1, 11))
