"""P2 replay harness — E1 envelope module: PF ratio + net ratio per leg.

Implements handoff §2.4 for ``docs/adr/2026-07-03-hardcore-p2-edge-transfer-gate.md``
E1: per leg, PF ratio and net ratio of the CME replay vs the Pepperstone
baseline over the SAME pinned window.

The baseline is the PAIRED same-window Pepperstone export — NEVER the pinned
MC anchors (handoff §5.5). Metric conventions follow the trade-csv-reconcile
skill (attribution: ``.claude/skills/trade-csv-reconcile/scripts/reconcile.py``,
commit ``d72c58c``): realized P&L on Exit rows ONLY (Q-A1-c double-count
trap); PF = gross_win / |gross_loss|.

The envelope floors (PF >= 0.8x AND net >= 0.7x) are [RATIFY]-pending in the
parent ADR: ``score_e1`` takes them as REQUIRED arguments — no defaults, and
nothing is scored in Phase A.

No window is hardcoded anywhere (handoff §0.5-b): ``filter_window`` requires
explicit boundaries.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from p2_ingest import NeedsContextError, to_et_boundary  # noqa: E402

#: [RATIFY]-pending values from the parent ADR §2 E1 — reference only, never
#: defaults. Confirm ratified in the go-message before scoring anything.
E1_PF_RATIO_FLOOR_RATIFY_PENDING = 0.8
E1_NET_RATIO_FLOOR_RATIFY_PENDING = 0.7


@dataclass
class LegMetrics:
    n_trades: int
    gross_win: float
    gross_loss: float   # negative or 0
    pf: float
    net: float


@dataclass
class E1Ratios:
    leg: str
    pep: LegMetrics
    cme: LegMetrics
    pf_ratio: float
    net_ratio: float


def filter_window(df: pd.DataFrame,
                  start: str | pd.Timestamp,
                  end: str | pd.Timestamp) -> pd.DataFrame:
    """Trades whose FIRST entry timestamp falls in [start, end) — all rows of
    an included trade are kept (a trade entered inside the window keeps its
    full realized P&L even if the exit lands after ``end``; frozen
    convention, identical for both feeds). Boundaries are REQUIRED explicit
    inputs, interpreted in ET when naive."""
    start_et, end_et = to_et_boundary(start), to_et_boundary(end)
    if end_et <= start_et:
        raise NeedsContextError(
            f"NEEDS_CONTEXT: window end {end_et} <= start {start_et}."
        )
    entries = df[df["Type"].str.startswith("Entry", na=False)]
    first_entry = entries.groupby("Trade #")["dt_et"].min()
    included = first_entry[(first_entry >= start_et) & (first_entry < end_et)].index
    return df[df["Trade #"].isin(included)].copy()


def pf_net(df: pd.DataFrame) -> LegMetrics:
    """Headline PF + net, exits-only (trade-csv-reconcile convention)."""
    exits = df[df["Type"].str.startswith("Exit", na=False)]
    if exits.empty:
        raise NeedsContextError(
            "NEEDS_CONTEXT: no Exit rows in (window-filtered) export — check "
            "the window pin and CSV provenance."
        )
    pnl = exits["Net P&L USD"].astype(float)
    gross_win = float(pnl[pnl > 0].sum())
    gross_loss = float(pnl[pnl <= 0].sum())
    if gross_loss == 0:
        # Zero-loss PF is fragile/ill-conditioned (PF-spike lesson) — a ratio
        # over an infinite baseline decides nothing; refuse to guess.
        raise NeedsContextError(
            "NEEDS_CONTEXT: zero-loss cohort — PF is infinite/ill-conditioned; "
            "an E1 PF ratio cannot be computed from this window."
        )
    return LegMetrics(
        n_trades=int(df[df["Type"].str.startswith("Entry", na=False)]["Trade #"].nunique()),
        gross_win=gross_win,
        gross_loss=gross_loss,
        pf=gross_win / abs(gross_loss),
        net=float(pnl.sum()),
    )


def e1_ratios(leg: str, df_pep: pd.DataFrame, df_cme: pd.DataFrame,
              start: str | pd.Timestamp, end: str | pd.Timestamp) -> E1Ratios:
    """CME-replay vs paired Pepperstone baseline over the identical window.
    Both frames are window-filtered HERE with the same boundaries so the
    two sides can never drift onto different windows (§7 quality check)."""
    pep = pf_net(filter_window(df_pep, start, end))
    cme = pf_net(filter_window(df_cme, start, end))
    if pep.net <= 0:
        raise NeedsContextError(
            f"NEEDS_CONTEXT: Pepperstone baseline net is non-positive "
            f"({pep.net:.2f}) — a net ratio against it is ill-defined; "
            f"score E1 AMBIGUOUS with a written cause instead."
        )
    return E1Ratios(
        leg=leg, pep=pep, cme=cme,
        pf_ratio=cme.pf / pep.pf,
        net_ratio=cme.net / pep.net,
    )


def score_e1(ratios: E1Ratios, pf_floor: float, net_floor: float) -> str:
    """PASS or MISS-AMBIGUOUS against EXPLICIT ratified floors (no defaults —
    the 0.8x/0.7x values are [RATIFY]-pending). A miss closes E1 AMBIGUOUS
    with the K2 divergence taxonomy as the written cause; NO re-run with a
    shifted window (handoff §4, P2 §5.5)."""
    if ratios.pf_ratio >= pf_floor and ratios.net_ratio >= net_floor:
        return "PASS"
    return "MISS-AMBIGUOUS"


def format_ratios(r: E1Ratios) -> str:
    return "\n".join([
        f"=== E1 envelope inputs — leg {r.leg} (same-window paired exports) ===",
        f"pepperstone baseline : n={r.pep.n_trades}  PF={r.pep.pf:.3f}  net={r.pep.net:,.2f}",
        f"cme replay           : n={r.cme.n_trades}  PF={r.cme.pf:.3f}  net={r.cme.net:,.2f}",
        f"PF ratio  (cme/pep)  : {r.pf_ratio:.3f}",
        f"net ratio (cme/pep)  : {r.net_ratio:.3f}",
        "NOTE: envelope floors are [RATIFY]-pending — scoring requires explicit "
        "ratified values (score_e1).",
    ])
