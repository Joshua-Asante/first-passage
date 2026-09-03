"""Book-composed N-SURV scorer (TNEC-AU-1 kill-order step 3 tooling).

Compose ≥1 daily P&L legs at declared $100K-basis integer sizing, then score the
composed series on the frozen Part-A path via ``nsurv_channel.score_nsurv``
(intraday-honest, full + both regime halves). When ``N ≥ 2`` and a marginal leg
is named, also score book-without-that-leg and emit the step-3 comparison lines
(composed bust vs ceiling; composed P(pass) vs book-without).

**Computes, does not admit.** PASS/FAIL lines follow whatever
``prop_survivor_scoring.load_scoring_thresholds()`` resolves at call time — i.e.
``DEFAULT_PREREG``, which since 2026-08-26 is **v2: bust ≤ 5.0% ∧ P(pass) ≥ 50%**
(non-strict). ⚠ This docstring previously named the frozen 2026-07-13 v1 thresholds
(bust ≤ 3.0%), which ``score_book`` has not used since that date — a 3–5% composed
bust was being described with the opposite verdict at this API surface. Callers may
still pass an explicit ``thresholds=`` to reproduce a historical run against its own
frozen ceiling. Never authorizes capital either way.
Sibling of ``cov_prekill.py`` (step 2) and reshaped successor to the single-series
``nsurv_channel`` P2 idea — Q-TXG-1 already scores SINGLE cells via that channel;
this module owns the COMPOSED book case.

Input contract matches ``nsurv_channel``: CSV/JSON rows with ``date``, ``pnl_usd``,
and ``intraday_low`` (≤ 0). Composition is date-aligned summation; missing days
fill 0 (house daily-panel convention).
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

import numpy as np
import pandas as pd

from discovery.prop_survivor_scoring import ScoringThresholds, load_scoring_thresholds
from research_utils.nsurv_channel import (
    DEFAULT_FIRM_KEY,
    SIZING_BASIS_USD,
    NSurvReport,
    load_candidate_daily_pnl,
    score_nsurv,
)

TOOLING_DISCLAIMER = "computes, does not admit"

_REQUIRED = frozenset({"date", "pnl_usd", "intraday_low"})


def clears_bust_ceiling(headline_bust: float, thresholds: ScoringThresholds) -> bool:
    """Part A bust limb — bust ≤ ceiling (non-strict)."""
    return float(headline_bust) <= float(thresholds.eval_bust_ceiling)


def clears_pass_floor(pass_rate: float, thresholds: ScoringThresholds) -> bool:
    """Part A pass limb — P(pass) ≥ floor (non-strict)."""
    return float(pass_rate) >= float(thresholds.pass_floor)


def _normalize_leg(frame: pd.DataFrame, *, name: str) -> pd.DataFrame:
    missing = _REQUIRED - set(frame.columns)
    if missing:
        raise ValueError(f"leg {name!r} missing columns {sorted(missing)}")
    out = pd.DataFrame(
        {
            "date": pd.to_datetime(frame["date"]).dt.normalize(),
            "pnl_usd": pd.to_numeric(frame["pnl_usd"], errors="raise").astype(float),
            "intraday_low": pd.to_numeric(
                frame["intraday_low"], errors="raise"
            ).astype(float),
        }
    )
    if out.empty:
        raise ValueError(f"leg {name!r} is empty")
    if out["date"].duplicated().any():
        raise ValueError(f"leg {name!r} has duplicate dates")
    if np.any(out["intraday_low"].to_numpy(dtype=float) > 0.0):
        raise ValueError(
            f"leg {name!r}: intraday_low entries must be ≤ 0.0 "
            "(excursion from day's opening equity)"
        )
    return out.sort_values("date").reset_index(drop=True)


def compose_book(legs: Mapping[str, pd.DataFrame]) -> pd.DataFrame:
    """Date-aligned sum of N ≥ 1 legs; missing days = 0 for pnl and intraday_low."""
    if not legs:
        raise ValueError("compose_book requires at least one leg")
    normalized = {name: _normalize_leg(frame, name=name) for name, frame in legs.items()}
    all_dates = sorted(
        {d for frame in normalized.values() for d in frame["date"].tolist()}
    )
    index = pd.DatetimeIndex(all_dates)
    pnl_sum = pd.Series(0.0, index=index, dtype=float)
    low_sum = pd.Series(0.0, index=index, dtype=float)
    for frame in normalized.values():
        series_pnl = frame.set_index("date")["pnl_usd"].reindex(index).fillna(0.0)
        series_low = frame.set_index("date")["intraday_low"].reindex(index).fillna(0.0)
        pnl_sum = pnl_sum + series_pnl
        low_sum = low_sum + series_low
    out = pd.DataFrame(
        {
            "date": index,
            "pnl_usd": pnl_sum.to_numpy(dtype=float),
            "intraday_low": low_sum.to_numpy(dtype=float),
        }
    )
    if np.any(out["intraday_low"].to_numpy(dtype=float) > 0.0):
        raise ValueError("composed intraday_low entries must be ≤ 0.0")
    return out.reset_index(drop=True)


@dataclass(frozen=True)
class BookScoreReport:
    """Composed N-SURV block (+ optional book-without / step-3 comparisons)."""

    leg_names: tuple[str, ...]
    half_boundary_date: str
    composed: NSurvReport
    marginal_leg: str | None
    without_marginal: NSurvReport | None
    step3_bust_vs_ceiling: bool | None
    step3_pass_vs_without: bool | None

    def to_dict(self) -> dict:
        d: dict = {
            "disclaimer": TOOLING_DISCLAIMER,
            "leg_names": list(self.leg_names),
            "half_boundary_date": self.half_boundary_date,
            "composed": self.composed.to_dict(),
            "marginal_leg": self.marginal_leg,
        }
        if self.without_marginal is not None:
            d["without_marginal"] = self.without_marginal.to_dict()
            d["step3_bust_vs_ceiling"] = self.step3_bust_vs_ceiling
            d["step3_pass_vs_without"] = self.step3_pass_vs_without
        return d

    def format_block(self) -> str:
        """Human-readable composed block; labeled tooling, not an admission gate."""
        lines = [
            f"book-composed N-SURV ({TOOLING_DISCLAIMER})",
            f"legs={','.join(self.leg_names)} n={len(self.leg_names)}",
            self.composed.format_block(),
        ]
        if self.without_marginal is not None and self.marginal_leg is not None:
            thr_bust = self.composed.eval_bust_ceiling
            thr_pass = self.composed.pass_floor
            c, w = self.composed, self.without_marginal
            lines.extend(
                [
                    f"--- book-without:{self.marginal_leg} ---",
                    self.without_marginal.format_block(),
                    "--- TNEC-AU-1 step-3 comparison "
                    f"({TOOLING_DISCLAIMER}) ---",
                    (
                        f"composed bust vs ceiling≤{thr_bust:.1%}: "
                        f"full={c.full.headline_bust:.2%} "
                        f"H1={c.h1.headline_bust:.2%} "
                        f"H2={c.h2.headline_bust:.2%} "
                        f"{'PASS' if self.step3_bust_vs_ceiling else 'FAIL'}"
                    ),
                    (
                        f"composed P(pass) vs book-without "
                        f"(floor≥{thr_pass:.0%} is separate): "
                        f"composed={c.full.pass_rate:.2%} "
                        f"without={w.full.pass_rate:.2%} "
                        f"{'PASS' if self.step3_pass_vs_without else 'FAIL'}"
                    ),
                    (
                        "step-3 joint (bust ceiling ∧ pass≥without): "
                        f"{'PASS' if (self.step3_bust_vs_ceiling and self.step3_pass_vs_without) else 'FAIL'} "
                        f"— {TOOLING_DISCLAIMER}"
                    ),
                ]
            )
        else:
            lines.append(f"label: {TOOLING_DISCLAIMER}")
        return "\n".join(lines)


def score_book(
    legs: Mapping[str, pd.DataFrame],
    *,
    half_boundary_date: str | pd.Timestamp,
    marginal: str | None = None,
    firm_key: str = DEFAULT_FIRM_KEY,
    sizing_basis_usd: float = SIZING_BASIS_USD,
    thresholds: ScoringThresholds | None = None,
    n_sims: int | None = None,
) -> BookScoreReport:
    """Compose legs, score via ``score_nsurv``; optional book-without marginal."""
    if not legs:
        raise ValueError("score_book requires at least one leg")
    names = tuple(legs.keys())
    if marginal is not None:
        if len(legs) < 2:
            raise ValueError(
                "--marginal / marginal= requires N ≥ 2 legs "
                f"(got N={len(legs)})"
            )
        if marginal not in legs:
            raise ValueError(
                f"marginal leg {marginal!r} not in legs {list(names)}"
            )

    thr = thresholds if thresholds is not None else load_scoring_thresholds()
    composed_frame = compose_book(legs)
    composed = score_nsurv(
        composed_frame,
        half_boundary_date=half_boundary_date,
        firm_key=firm_key,
        sizing_basis_usd=sizing_basis_usd,
        thresholds=thr,
        n_sims=n_sims,
    )

    without: NSurvReport | None = None
    bust_ok: bool | None = None
    pass_ok: bool | None = None
    if marginal is not None:
        remainder = {k: v for k, v in legs.items() if k != marginal}
        without = score_nsurv(
            compose_book(remainder),
            half_boundary_date=half_boundary_date,
            firm_key=firm_key,
            sizing_basis_usd=sizing_basis_usd,
            thresholds=thr,
            n_sims=n_sims,
        )
        bust_ok = bool(
            clears_bust_ceiling(composed.full.headline_bust, thr)
            and clears_bust_ceiling(composed.h1.headline_bust, thr)
            and clears_bust_ceiling(composed.h2.headline_bust, thr)
        )
        # TNEC-AU-1 step 3 pass limb: composed P(pass) ≥ book-without (full panel).
        pass_ok = bool(composed.full.pass_rate >= without.full.pass_rate)

    boundary = pd.Timestamp(half_boundary_date).normalize().date().isoformat()
    return BookScoreReport(
        leg_names=names,
        half_boundary_date=boundary,
        composed=composed,
        marginal_leg=marginal,
        without_marginal=without,
        step3_bust_vs_ceiling=bust_ok,
        step3_pass_vs_without=pass_ok,
    )


def score_book_from_paths(
    leg_paths: Mapping[str, Path | str],
    *,
    half_boundary_date: str | pd.Timestamp,
    marginal: str | None = None,
    firm_key: str = DEFAULT_FIRM_KEY,
    sizing_basis_usd: float = SIZING_BASIS_USD,
    thresholds: ScoringThresholds | None = None,
    n_sims: int | None = None,
) -> BookScoreReport:
    """Load each leg from CSV/JSON then ``score_book``."""
    legs = {
        name: load_candidate_daily_pnl(path) for name, path in leg_paths.items()
    }
    return score_book(
        legs,
        half_boundary_date=half_boundary_date,
        marginal=marginal,
        firm_key=firm_key,
        sizing_basis_usd=sizing_basis_usd,
        thresholds=thresholds,
        n_sims=n_sims,
    )


def q_txg1_striker_mnq_inputs_present() -> tuple[bool, list[str]]:
    """Return (ok, missing) for the committed Q-TXG-1 striker×MNQ scoring inputs."""
    from research_utils.repo_root import repo_root

    cell = (
        repo_root()
        / "lab"
        / "analysis"
        / "c1"
        / "transfer_expression_grid_2026-08"
        / "cells"
        / "striker_mnq"
    )
    missing: list[str] = []
    for name in ("daily_pnl_nsurv.csv", "PANEL_SCORE.json"):
        path = cell / name
        if not path.is_file():
            missing.append(str(path))
    return (len(missing) == 0, missing)


def _parse_leg_args(raw: list[str]) -> dict[str, Path]:
    """Parse ``NAME=PATH`` leg specs."""
    out: dict[str, Path] = {}
    for item in raw:
        if "=" not in item:
            raise SystemExit(f"--leg expects NAME=PATH, got {item!r}")
        name, path_s = item.split("=", 1)
        name = name.strip()
        if not name:
            raise SystemExit(f"--leg name empty in {item!r}")
        if name in out:
            raise SystemExit(f"duplicate leg name {name!r}")
        out[name] = Path(path_s)
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=(
            "Book-composed N-SURV scorer (TNEC-AU-1 step-3 tooling; "
            f"{TOOLING_DISCLAIMER})."
        )
    )
    ap.add_argument(
        "--leg",
        action="append",
        required=True,
        metavar="NAME=PATH",
        help="Daily P&L series (CSV/JSON) at $100K-basis; repeat for N≥1 legs.",
    )
    ap.add_argument(
        "--half-boundary",
        required=True,
        help="Regime-half boundary date (ISO); H1 < boundary ≤ H2.",
    )
    ap.add_argument(
        "--marginal",
        default=None,
        metavar="LEG",
        help="When N≥2, also score book-without LEG and emit step-3 lines.",
    )
    ap.add_argument(
        "--firm",
        default=DEFAULT_FIRM_KEY,
        help=f"Firm tier key (default {DEFAULT_FIRM_KEY}).",
    )
    ap.add_argument(
        "--n-sims",
        type=int,
        default=None,
        help="Optional remc sims override (default: frozen prereg).",
    )
    ap.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON report to stdout instead of the text block.",
    )
    args = ap.parse_args(argv)
    legs = _parse_leg_args(args.leg)
    report = score_book_from_paths(
        legs,
        half_boundary_date=args.half_boundary,
        marginal=args.marginal,
        firm_key=args.firm,
        n_sims=args.n_sims,
    )
    if args.json:
        print(json.dumps(report.to_dict(), indent=2, default=str))
    else:
        print(report.format_block())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
