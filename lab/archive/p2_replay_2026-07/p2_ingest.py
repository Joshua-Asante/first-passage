"""P2 replay harness — ingest, ET normalization, grid alignment, sanity gates.

Part of ``lab/analysis/p2_replay_2026-07`` (CC handoff 2026-07-03, combined
K2+E1 implementation of ``docs/adr/2026-07-03-hardcore-p2-edge-transfer-gate.md``).

Parses paired TradingView list-of-trades exports (Pepperstone CFD leg and CME
micro continuous leg) per the ``trade-csv-reconcile`` skill conventions. The
canonical loader is REUSED from the skill (attribution:
``.claude/skills/trade-csv-reconcile/scripts/reconcile.py``, commit ``d72c58c``)
rather than re-derived — it already handles BOTH TV export schemas (legacy
"Trade #" and current "Trade number"/"Net PnL USD"/"Size (value)"), the BOM,
and the Q-A1-c Entry+Exit double-count trap.

FREEZE (handoff §5.3): the alignment rules in this module — grid assertion,
timezone normalization, signal-pairing key — are FROZEN at Phase-A
fixture-green. They must NOT be adjusted after real exports arrive to make
divergence counts drop. See NOTES.md §Freeze declaration.

No window is hardcoded anywhere in this module (handoff §0.5-b: window is a
CLI/config input, pinned by Joshua in the go-message).
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

# --- canonical-loader reuse (lab -> governance edge; legal per ADR 2026-06-05) --
_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parents[2]
_RECONCILE_SCRIPTS = _REPO_ROOT / ".claude" / "skills" / "trade-csv-reconcile" / "scripts"
if str(_RECONCILE_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_RECONCILE_SCRIPTS))

import reconcile  # noqa: E402  (canonical TV-trade-CSV loader, both schemas)

# ---------------------------------------------------------------------------
# Frozen constants
# ---------------------------------------------------------------------------

ET_TZ = "America/New_York"
#: Locked strategies are 15m (Striker DJ30 v4.5, Striker NAS100 v1). Frozen.
BAR_INTERVAL = pd.Timedelta(minutes=15)


class NeedsContextError(RuntimeError):
    """NEEDS_CONTEXT-class hard error (handoff §6): the harness refuses to
    guess. Message always starts with 'NEEDS_CONTEXT:'."""


class GridAlignmentError(NeedsContextError):
    """Misaligned bar grids are a hard error — never silently resampled
    (handoff §0.5-d)."""


class FirstTradeSanityError(NeedsContextError):
    """First-trade P&L inconsistent with price-move x size x point-value —
    the F-1 / JPY-153x defect class (ADR 2026-05-16 §1)."""


# ---------------------------------------------------------------------------
# Load + normalize
# ---------------------------------------------------------------------------

def load_export(path: str | Path, source_tz: str = ET_TZ) -> pd.DataFrame:
    """Load a TV list-of-trades export and normalize timestamps to ET.

    ``source_tz`` is the chart timezone the export was made with (EXPORT_SPEC
    mandates New York on both charts; the parameter exists so a declared
    deviation can be handled explicitly, never guessed).

    Frozen DST conventions (identical for both feeds, so pairing is
    unaffected): ambiguous fall-back times resolve to the DST occurrence
    (``ambiguous=True``); nonexistent spring-forward times shift forward.
    """
    df = reconcile.load_csv(path)  # canonical names, both schemas, BOM-safe
    if df["dt"].isna().any():
        bad = df[df["dt"].isna()]["Date and time"].head(3).tolist()
        raise NeedsContextError(
            f"NEEDS_CONTEXT: unparseable 'Date and time' values in {path}: {bad}"
        )
    df["dt_et"] = (
        df["dt"]
        .dt.tz_localize(source_tz, ambiguous=True, nonexistent="shift_forward")
        .dt.tz_convert(ET_TZ)
    )
    return df


def assert_bar_grid(df: pd.DataFrame, feed_label: str) -> None:
    """Hard-assert every timestamp sits on the 15m bar grid (:00/:15/:30/:45,
    zero seconds). Misalignment raises GridAlignmentError — the harness never
    silently resamples (handoff §0.5-d)."""
    ts = df["dt_et"]
    off_grid = (ts.dt.minute % 15 != 0) | (ts.dt.second != 0) | (ts.dt.microsecond != 0)
    if off_grid.any():
        offenders = ts[off_grid].head(5).tolist()
        raise GridAlignmentError(
            f"NEEDS_CONTEXT: {feed_label} export is off the 15m bar grid "
            f"(first offenders: {offenders}). Refusing to resample — re-export "
            f"on a 15m chart / correct timezone and re-run."
        )


def grid_warnings(df: pd.DataFrame, feed_label: str, min_n: int = 8) -> list[str]:
    """Advisory (non-fatal) grid checks. An hourly chart also passes the 15m
    modulo test, so flag when every timestamp is minute==0 over a
    non-trivial sample."""
    warnings: list[str] = []
    ts = df["dt_et"]
    if len(ts) >= min_n and (ts.dt.minute == 0).all():
        warnings.append(
            f"{feed_label}: all {len(ts)} timestamps are minute==0 — possible "
            f"non-15m (hourly) chart export; verify the chart timeframe."
        )
    return warnings


# ---------------------------------------------------------------------------
# Signal extraction (K2 input)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Signal:
    ts: pd.Timestamp      # ET, bar-grid aligned
    direction: str        # "long" | "short"
    is_add: bool          # pyramid add leg
    trade_no: object      # Trade # (schema-normalized)


def extract_signals(df: pd.DataFrame) -> list[Signal]:
    """One signal per Entry row, under BOTH schemas.

    Pyramid-add detection (per trade-csv-reconcile SKILL.md trap #14):
      - current schema: each add leg is its OWN Trade # whose Signal carries
        an "Add" tag ("Long Add") -> Signal-string detection;
      - legacy schema: 2nd+ Entry rows within the same Trade # are adds ->
        ordinal detection.
    Both detectors run; either marks the leg as an add.
    """
    entries = df[df["Type"].str.startswith("Entry", na=False)].copy()
    entries = entries.sort_values("dt_et", kind="stable")

    signals: list[Signal] = []
    for trade_no, grp in entries.groupby("Trade #", sort=False):
        for ordinal, (_, row) in enumerate(grp.sort_values("dt_et").iterrows()):
            sig_txt = str(row.get("Signal", ""))
            is_add = ("add" in sig_txt.lower()) or (ordinal > 0)
            direction = "long" if "long" in str(row["Type"]).lower() else "short"
            signals.append(Signal(ts=row["dt_et"], direction=direction,
                                  is_add=is_add, trade_no=trade_no))
    signals.sort(key=lambda s: (s.ts, str(s.trade_no)))
    return signals


def filter_signals_window(signals: list[Signal],
                          start_et: pd.Timestamp,
                          end_et: pd.Timestamp) -> list[Signal]:
    """Keep signals with start <= ts < end. Window is ALWAYS an explicit
    input (no defaults, no hardcoded dates)."""
    return [s for s in signals if start_et <= s.ts < end_et]


def to_et_boundary(value: str | pd.Timestamp) -> pd.Timestamp:
    """Parse a window boundary as ET (tz-aware passes through converted)."""
    ts = pd.Timestamp(value)
    if ts.tzinfo is None:
        return ts.tz_localize(ET_TZ)
    return ts.tz_convert(ET_TZ)


# ---------------------------------------------------------------------------
# First-trade sanity (handoff §0.5-e — F-1/JPY-153x defect class)
# ---------------------------------------------------------------------------

def first_trade_sanity(df: pd.DataFrame, point_value: float,
                       max_ratio: float = 3.0, feed_label: str = "?") -> float:
    """Assert the FIRST trade's realized P&L is magnitude-consistent with
    price-move x qty x point_value. Returns the actual/expected ratio.

    Convention (frozen): expected = sum over the first trade's entry legs of
    dir_sign x (last_exit_price - entry_leg_price) x entry_leg_qty x
    point_value. This covers the current per-leg schema (single entry leg)
    and the legacy multi-entry-per-Trade# schema (combined exit). It is a
    magnitude sanity (catches the ~153x class), not an exact fee model —
    hence the wide default tolerance band [1/max_ratio, max_ratio].
    """
    entries = df[df["Type"].str.startswith("Entry", na=False)]
    exits = df[df["Type"].str.startswith("Exit", na=False)]
    if entries.empty or exits.empty:
        raise NeedsContextError(
            f"NEEDS_CONTEXT: {feed_label}: cannot run first-trade sanity — "
            "no Entry or no Exit rows."
        )
    first_entry = entries.loc[entries["dt_et"].idxmin()]
    trade_no = first_entry["Trade #"]
    legs = entries[entries["Trade #"] == trade_no].sort_values("dt_et")
    trade_exits = exits[exits["Trade #"] == trade_no].sort_values("dt_et")
    if trade_exits.empty:
        raise NeedsContextError(
            f"NEEDS_CONTEXT: {feed_label}: first trade (Trade # {trade_no}) "
            "has no Exit row — cannot sanity-check."
        )
    dir_sign = 1.0 if "long" in str(first_entry["Type"]).lower() else -1.0
    last_exit_price = float(trade_exits.iloc[-1]["Price USD"])
    expected = sum(
        dir_sign * (last_exit_price - float(leg["Price USD"]))
        * float(leg["Size (qty)"]) * point_value
        for _, leg in legs.iterrows()
    )
    actual = float(trade_exits["Net P&L USD"].astype(float).sum())

    if abs(expected) < 1e-9:
        # Scratch/BE trade: only require the realized P&L is not absurdly large.
        bound = abs(point_value) * float(legs["Size (qty)"].astype(float).sum())
        if abs(actual) > max(bound, 1.0):
            raise FirstTradeSanityError(
                f"NEEDS_CONTEXT: {feed_label}: first-trade sanity FAILED — "
                f"zero expected price-move P&L but actual={actual:.2f}."
            )
        return 1.0

    ratio = abs(actual / expected)
    if not (1.0 / max_ratio <= ratio <= max_ratio):
        raise FirstTradeSanityError(
            f"NEEDS_CONTEXT: {feed_label}: first-trade sanity FAILED "
            f"(F-1/JPY-153x class) — Trade # {trade_no}: expected~{expected:.2f} "
            f"actual={actual:.2f} ratio={ratio:.1f}x outside "
            f"[{1.0/max_ratio:.2f}, {max_ratio:.2f}]. Check currency/contract "
            f"conversion and point value before ingesting this export."
        )
    return ratio
