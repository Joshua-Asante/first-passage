"""P2 replay harness — K2 diff module: signal-set divergence + cause taxonomy.

Implements handoff §2.3 for ``docs/adr/2026-07-03-hardcore-p2-edge-transfer-gate.md``
K2: per leg, fire/no-fire divergence % over the union signal set (signals
paired by ET bar timestamp), with per-divergent-signal cause classification:

  ROLL-SEAM  — within +/-2 bars of a roll-seam bar (seams derived by REUSING
               ``lab/analysis/futures_conversion_2026-07-01/roll_mask.py``,
               commit ``5dcdbea`` — no new roll calendar is written here).
  SESSION    — a 15m bar exists on exactly one feed at that timestamp.
  BASIS      — both bars exist; the entry condition flips (incl. a
               direction flip when both feeds fire).
  DATA-GAP   — a signal fired but the bar exists on neither feed's index
               (inconsistent/holey data).

Classification precedence is ROLL-SEAM > SESSION > BASIS > DATA-GAP and is
FROZEN at Phase-A fixture-green (handoff §5.3).

Both roll treatments are always emitted (§0.5-c — present both, decide
nothing): "with-roll" counts ROLL-SEAM divergences in numerator and
denominator; "ex-roll" removes ROLL-SEAM-classified divergent signals from
BOTH numerator and denominator (the carve-out removes those signal points
from the set entirely).

Scoring against the kill threshold is a SEPARATE explicit step: the 10%
value is [RATIFY]-pending in the parent ADR, so ``score_k2`` takes the
threshold as a required argument — there is no default and nothing in this
module scores anything on import.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from p2_ingest import (  # noqa: E402
    BAR_INTERVAL,
    ET_TZ,
    GridAlignmentError,
    NeedsContextError,
    Signal,
)

# --- roll_mask reuse (lab -> lab edge; legal per ADR 2026-06-05) -------------
_ROLL_MASK_DIR = _HERE.parent / "futures_conversion_2026-07-01"
if str(_ROLL_MASK_DIR) not in sys.path:
    sys.path.insert(0, str(_ROLL_MASK_DIR))

import roll_mask  # noqa: E402  (CME roll-seam masking, floors work, 5dcdbea)

#: [RATIFY]-pending value from the parent ADR §2 K2 — reference only, never a
#: default. Confirm ratified in the go-message before scoring anything.
K2_KILL_DIVERGENCE_PCT_RATIFY_PENDING = 10.0

#: Handoff §2.3: a divergence within +/-2 bars of a roll seam is ROLL-SEAM.
ROLL_SEAM_BAR_WINDOW = 2

#: Micro contracts share the parent contract's roll cycle. roll_mask registers
#: NQ/YM/J7/QO; map the P2 CME continuous symbols onto those entries instead
#: of duplicating the calendar (minimal adaptation with attribution).
SYMBOL_TO_ROLL_KEY = {
    "MNQ": "NQ", "MNQ1!": "NQ", "NQ": "NQ", "NQ1!": "NQ",
    "MYM": "YM", "MYM1!": "YM", "YM": "YM", "YM1!": "YM",
}


# ---------------------------------------------------------------------------
# Bar-index + seam helpers
# ---------------------------------------------------------------------------

def bar_index_et(bars: pd.DataFrame) -> set[pd.Timestamp]:
    """Set of ET bar timestamps from a bar panel with a UTC-parseable ``time``
    column (same convention roll_mask.py consumes). Used ONLY as a
    classification aid (SESSION/BASIS/DATA-GAP labels) — never as a canonical
    price input (ADR 2026-06-12: TV CSVs are the canonical feed; bar panels
    are staging-only)."""
    t = pd.to_datetime(bars["time"], utc=True).dt.tz_convert(ET_TZ)
    return set(t.tolist())


def seam_timestamps_from_bars(bars: pd.DataFrame, symbol: str,
                              threshold_pct: float = 0.5) -> list[pd.Timestamp]:
    """ET timestamps of roll-seam bars, via roll_mask.flag_roll_seams (REUSED).

    ``symbol`` may be a P2 CME continuous ticker (MYM1!/MNQ1!) — it is mapped
    to roll_mask's registered parent-cycle key."""
    key = SYMBOL_TO_ROLL_KEY.get(symbol.upper())
    if key is None:
        raise NeedsContextError(
            f"NEEDS_CONTEXT: no roll-cycle mapping for symbol {symbol!r}; "
            f"known: {sorted(SYMBOL_TO_ROLL_KEY)}"
        )
    flagged = roll_mask.flag_roll_seams(bars, symbol=key, threshold_pct=threshold_pct)
    t = pd.to_datetime(flagged.loc[flagged["roll_seam"], "time"], utc=True)
    return sorted(t.dt.tz_convert(ET_TZ).tolist())


# ---------------------------------------------------------------------------
# Pairing + classification
# ---------------------------------------------------------------------------

CAUSES = ("ROLL-SEAM", "SESSION", "BASIS", "DATA-GAP")


@dataclass(frozen=True)
class Divergence:
    ts: pd.Timestamp
    kind: str      # "pep-only" | "cme-only" | "direction-flip"
    cause: str     # one of CAUSES


@dataclass
class K2Report:
    leg: str
    n_union: int
    n_agree: int
    divergences: list[Divergence] = field(default_factory=list)

    @property
    def n_divergent(self) -> int:
        return len(self.divergences)

    @property
    def cause_counts(self) -> dict[str, int]:
        counts = {c: 0 for c in CAUSES}
        for d in self.divergences:
            counts[d.cause] += 1
        return counts

    @property
    def pct_with_roll(self) -> float:
        return 100.0 * self.n_divergent / self.n_union

    @property
    def pct_ex_roll(self) -> float:
        n_roll = self.cause_counts["ROLL-SEAM"]
        denom = self.n_union - n_roll
        if denom == 0:
            return 0.0
        return 100.0 * (self.n_divergent - n_roll) / denom


def _signal_map(signals: list[Signal]) -> dict[pd.Timestamp, str]:
    """ts -> direction; first occurrence wins (deterministic after the sort
    in extract_signals). Pyramid adds are signals in their own right and
    participate in the union set."""
    out: dict[pd.Timestamp, str] = {}
    for s in signals:
        out.setdefault(s.ts, s.direction)
    return out


def _assert_signal_grid(signals: list[Signal], label: str) -> None:
    off = [s.ts for s in signals
           if (s.ts.minute % 15 != 0) or s.ts.second or s.ts.microsecond]
    if off:
        raise GridAlignmentError(
            f"NEEDS_CONTEXT: {label} signal timestamps off the 15m grid "
            f"(first offenders: {off[:5]}). Never silently resampled."
        )


def classify_divergence(
    ts: pd.Timestamp,
    seam_timestamps: list[pd.Timestamp],
    bars_pep: set[pd.Timestamp] | None,
    bars_cme: set[pd.Timestamp] | None,
) -> str:
    """Cause classification, frozen precedence ROLL-SEAM > SESSION > BASIS >
    DATA-GAP. Bar-existence context is REQUIRED for the non-roll branches —
    without it the harness refuses to guess (NEEDS_CONTEXT), keeping the
    four-bucket taxonomy honest."""
    window = ROLL_SEAM_BAR_WINDOW * BAR_INTERVAL
    if any(abs(ts - seam) <= window for seam in seam_timestamps):
        return "ROLL-SEAM"
    if bars_pep is None or bars_cme is None:
        raise NeedsContextError(
            "NEEDS_CONTEXT: SESSION/BASIS/DATA-GAP classification requires "
            "per-feed bar-timestamp indexes (bars_pep/bars_cme); supply them "
            "via --pep-bars/--cme-bars."
        )
    in_pep, in_cme = ts in bars_pep, ts in bars_cme
    if in_pep != in_cme:
        return "SESSION"
    if in_pep and in_cme:
        return "BASIS"
    return "DATA-GAP"


def k2_report(
    leg: str,
    signals_pep: list[Signal],
    signals_cme: list[Signal],
    seam_timestamps: list[pd.Timestamp],
    bars_pep: set[pd.Timestamp] | None,
    bars_cme: set[pd.Timestamp] | None,
) -> K2Report:
    """Fire/no-fire (and direction-flip) divergence over the union signal
    set, signals paired by ET bar timestamp."""
    _assert_signal_grid(signals_pep, "pepperstone")
    _assert_signal_grid(signals_cme, "cme")

    pep = _signal_map(signals_pep)
    cme = _signal_map(signals_cme)
    union = sorted(set(pep) | set(cme))
    if not union:
        raise NeedsContextError(
            "NEEDS_CONTEXT: empty union signal set — check the window pin and "
            "that both exports cover it."
        )

    report = K2Report(leg=leg, n_union=len(union), n_agree=0)
    for ts in union:
        fired_pep, fired_cme = ts in pep, ts in cme
        if fired_pep and fired_cme:
            if pep[ts] == cme[ts]:
                report.n_agree += 1
                continue
            kind = "direction-flip"
        else:
            kind = "pep-only" if fired_pep else "cme-only"
        cause = classify_divergence(ts, seam_timestamps, bars_pep, bars_cme)
        report.divergences.append(Divergence(ts=ts, kind=kind, cause=cause))
    return report


def score_k2(report: K2Report, kill_threshold_pct: float,
             treatment: str) -> str:
    """PASS/KILL against an EXPLICIT threshold (no default — the 10% value is
    [RATIFY]-pending in the parent ADR). ``treatment`` picks which of the two
    always-emitted numbers is scored; that choice is Joshua's §0.5-c call at
    scoring time, never this module's."""
    if treatment == "with-roll":
        pct = report.pct_with_roll
    elif treatment == "ex-roll":
        pct = report.pct_ex_roll
    else:
        raise ValueError(f"treatment must be 'with-roll' or 'ex-roll', got {treatment!r}")
    return "KILL" if pct > kill_threshold_pct else "PASS"


def format_report(report: K2Report) -> str:
    counts = report.cause_counts
    assert sum(counts.values()) == report.n_divergent, "taxonomy must sum to total"
    lines = [
        f"=== K2 signal-set divergence — leg {report.leg} ===",
        f"union signals      : {report.n_union}",
        f"agree              : {report.n_agree}",
        f"divergent          : {report.n_divergent}",
        f"divergence with-roll : {report.pct_with_roll:.2f}%",
        f"divergence ex-roll   : {report.pct_ex_roll:.2f}%  "
        f"(ROLL-SEAM bucket carved from numerator and denominator)",
        "taxonomy:",
    ]
    for cause in CAUSES:
        lines.append(f"  {cause:<9} : {counts[cause]}")
    for d in report.divergences:
        lines.append(f"    {d.ts}  {d.kind:<14} {d.cause}")
    lines.append("NOTE: both roll treatments presented; carve-out decision is "
                 "operator-ratified at scoring time (§0.5-c) — not decided here.")
    return "\n".join(lines)
