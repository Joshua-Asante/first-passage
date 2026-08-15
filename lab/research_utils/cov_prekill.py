"""Covariance-space pre-kill calculator (TNEC-AU-1 kill-order step 2).

Measurement tooling only — decides nothing. The sole verdict is the sign of
``n_eff_risk_delta`` (PRE-KILL if <= 0, PASS-TO-MC if > 0). Always necessary-
never-sufficient: composed MC still binds (M-21 / envelope §2 item 6).

Inputs are daily P&L series at a declared $100K basis (caller-declared sizing;
this module does not re-scale). The book may be a single column or a multi-
column panel (summed for daily-$-std; columns kept separate for cov-space
N_eff).

``n_eff_risk`` is the participation ratio of the **weekly covariance** matrix
(PR(cov), never PR(corr)), transcribed from the Stage-8 ADR / ``breadth.py``:

    weekly = Mon-anchored 5-bday block sums of the daily panel
    cov    = np.cov(weekly, rowvar=False)
    PR(M)  = (sum(eigvals))**2 / sum(eigvals**2)

Connecting arithmetic (same as ``lab/research_utils/breadth.py``
``participation_ratio`` / ``compute_breadth``): clip eigvals at 0, then PR.
Cited: ``docs/adr/2026-07-20-stage8-variance-dominance-risk-neff-gate.md`` §0
(tool already emits ``n_eff_risk`` as PR of the weekly covariance matrix) and
the ADR decision text's risk-N_eff-delta floor.

Known-answer fixture (Q-COMPOSE-1 panel inputs not committed in-tree): quoted
figures from ``docs/briefs/closures/Q-COMPOSE-1-closure-falsified.md``.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
import pandas as pd

SIZING_BASIS_USD = 100_000.0
VERDICT_SUFFIX = "necessary-never-sufficient — composed MC still binds (M-21)"

Verdict = Literal["PRE-KILL", "PASS-TO-MC"]

# Q-COMPOSE-1 known-answer (closure-quoted; committed inputs absent).
# Source: docs/briefs/closures/Q-COMPOSE-1-closure-falsified.md
Q_COMPOSE_1_FIXTURE_SOURCE = (
    "docs/briefs/closures/Q-COMPOSE-1-closure-falsified.md"
)
Q_COMPOSE_1_LEG_DAILY_STD = 438.0
Q_COMPOSE_1_BOOK_DAILY_STD = 273.0
Q_COMPOSE_1_STD_RATIO = 438.0 / 273.0
Q_COMPOSE_1_N_EFF_RISK_BEFORE = 1.96
Q_COMPOSE_1_N_EFF_RISK_AFTER = 1.96
# Documentary only — this tool never emits PR(corr):
Q_COMPOSE_1_N_EFF_CORR_BEFORE = 1.9948
Q_COMPOSE_1_N_EFF_CORR_AFTER = 2.9502


@dataclass(frozen=True)
class CovPrekillReport:
    """Exact TNEC-AU-1 step-2 measurement block (no MC, no invented thresholds)."""

    sizing_basis_usd: float
    leg_daily_std: float
    book_daily_std: float
    std_ratio: float
    n_eff_risk_before: float
    n_eff_risk_after: float
    n_eff_risk_delta: float
    verdict: Verdict

    @property
    def verdict_line(self) -> str:
        return f"{self.verdict} — {VERDICT_SUFFIX}"


def participation_ratio(matrix: np.ndarray) -> float:
    """Effective breadth: PR(M) = (sum eigvals)^2 / sum(eigvals^2).

    Stage-8 ADR / breadth.py formula — covariance-space when ``matrix`` is cov.
    Scale-invariant in the positive-definite cone (PR(cM) == PR(M) for c > 0).
    """
    eigvals = np.clip(np.linalg.eigvalsh(matrix), 0, None)
    denom = float((eigvals ** 2).sum())
    if denom == 0.0:
        return 0.0
    return float(eigvals.sum() ** 2 / denom)


def _weekly_block_sums(panel: pd.DataFrame) -> np.ndarray:
    """Mon-anchored non-overlapping 5-bday block sums (breadth.py / ingest)."""
    values = panel.to_numpy(dtype=float)
    blocks: list[np.ndarray] = []
    for index, day in enumerate(panel.index):
        if day.weekday() == 0 and index + 5 <= len(panel):
            blocks.append(values[index : index + 5].sum(axis=0))
    if len(blocks) < 2:
        raise ValueError(
            f"need at least 2 weekly blocks for covariance N_eff; got {len(blocks)}"
        )
    return np.asarray(blocks, dtype=float)


def _n_eff_risk(panel: pd.DataFrame) -> float:
    """PR of the weekly covariance matrix (PR(cov), never PR(corr))."""
    weekly = _weekly_block_sums(panel)
    if weekly.ndim == 1:
        weekly = weekly.reshape(-1, 1)
    if weekly.shape[1] == 1:
        # 1x1 cov — PR is identically 1 when variance > 0.
        var = float(np.var(weekly[:, 0], ddof=1))
        return 1.0 if var > 0.0 else 0.0
    cov = np.cov(weekly, rowvar=False)
    if cov.ndim == 0:
        return 1.0 if float(cov) > 0.0 else 0.0
    return participation_ratio(np.atleast_2d(cov))


def _as_book_frame(book: pd.Series | pd.DataFrame) -> pd.DataFrame:
    if isinstance(book, pd.Series):
        name = book.name or "book"
        return book.to_frame(name=name)
    if isinstance(book, pd.DataFrame):
        if book.shape[1] < 1:
            raise ValueError("book DataFrame must have at least one column")
        return book.copy()
    raise TypeError("book must be a pandas Series or DataFrame of daily P&L")


def _align(
    leg: pd.Series, book: pd.DataFrame
) -> tuple[pd.Series, pd.DataFrame]:
    """Intersect on dates; zero-fill only inside the overlap window."""
    leg = leg.dropna()
    book = book.dropna(how="all")
    if leg.empty:
        raise ValueError("leg series is empty after dropping NaNs")
    if book.empty:
        raise ValueError("book panel is empty after dropping NaNs")

    start = max(leg.index.min(), book.index.min())
    end = min(leg.index.max(), book.index.max())
    if start > end:
        raise ValueError("leg and book date ranges do not overlap")

    window = pd.bdate_range(start, end)
    book_a = book.reindex(window).fillna(0.0)
    leg_a = leg.reindex(window).fillna(0.0)
    leg_name = leg.name or "candidate"
    if leg_name in book_a.columns:
        raise ValueError(f"leg name {leg_name!r} collides with a book column")
    return leg_a.rename(leg_name), book_a


def cov_prekill(
    leg: pd.Series,
    book: pd.Series | pd.DataFrame,
    *,
    sizing_basis_usd: float = SIZING_BASIS_USD,
) -> CovPrekillReport:
    """Compute daily-$-std ratio + covariance-space n_eff_risk delta.

    Parameters
    ----------
    leg :
        Candidate daily P&L at the declared $ basis.
    book :
        Existing book daily P&L — one column (composite) or multi-column panel.
        Multi-column: daily-$-std uses the row-sum; N_eff uses the columns.
    sizing_basis_usd :
        Declared basis (default $100K). Recorded on the report; not used to
        re-scale series (caller must already be at basis).
    """
    if not isinstance(leg, pd.Series):
        raise TypeError("leg must be a pandas Series of daily P&L")

    book_frame = _as_book_frame(book)
    leg_a, book_a = _align(leg, book_frame)

    book_daily = book_a.sum(axis=1)
    leg_std = float(leg_a.std(ddof=1))
    book_std = float(book_daily.std(ddof=1))
    if book_std == 0.0:
        raise ValueError("book daily-$-std is zero; ratio undefined")
    std_ratio = leg_std / book_std

    before = _n_eff_risk(book_a)
    after_panel = book_a.copy()
    after_panel[leg_a.name] = leg_a.to_numpy()
    after = _n_eff_risk(after_panel)
    delta = after - before

    verdict: Verdict = "PRE-KILL" if delta <= 0.0 else "PASS-TO-MC"
    return CovPrekillReport(
        sizing_basis_usd=float(sizing_basis_usd),
        leg_daily_std=leg_std,
        book_daily_std=book_std,
        std_ratio=std_ratio,
        n_eff_risk_before=before,
        n_eff_risk_after=after,
        n_eff_risk_delta=delta,
        verdict=verdict,
    )
