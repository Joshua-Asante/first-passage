"""DL-1 prereg Sec2 -- the frozen variant set (K_intrinsic = 10). Closed set:
no variant may be added, retuned, or substituted after any train number is
seen (D-K1). This table is a verbatim transcription of the prereg Sec2 table."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Variant:
    v: int
    or_minutes: int          # OR window: 30 or 60
    drift: str                # "unconditional" | "aligned"
    entry_style: str          # "breakout" | "retest"
    target_r: float           # 2.0 or 3.0


VARIANTS: tuple[Variant, ...] = (
    Variant(1, 30, "unconditional", "breakout", 2.0),
    Variant(2, 30, "unconditional", "breakout", 3.0),
    Variant(3, 30, "aligned",       "breakout", 2.0),
    Variant(4, 30, "aligned",       "breakout", 3.0),
    Variant(5, 60, "unconditional", "breakout", 2.0),
    Variant(6, 60, "unconditional", "breakout", 3.0),
    Variant(7, 60, "aligned",       "breakout", 3.0),
    Variant(8, 30, "aligned",       "retest",   2.0),
    Variant(9, 60, "aligned",       "retest",   3.0),
    Variant(10, 30, "unconditional", "retest",  2.0),
)

assert len(VARIANTS) == 10, "K_intrinsic = 10 is frozen -- Sec2 closed set"
assert [v.v for v in VARIANTS] == list(range(1, 11))
