"""MSL P2 W-B — TV trade-list → N-SURV / book_score adapter (no new MC).

Adapter only: TradingView List-of-Trades CSV → daily panel
(``date``, ``pnl_usd``, ``intraday_low``) → ``nsurv_channel.score_nsurv`` /
``book_score.score_book`` → TNEC verdict JSON.

Honesty rule (charter / program plan §3): when ``intraday_low`` is reconstructed
from trade closes only (omitting within-trade open excursion), the JSON carries
the label ``LOWER BOUND``. When TV Run-up/Drawdown (or Favorable/Adverse
excursion) columns are present and used to bound within-trade excursion, that
label is omitted and ``honesty`` reads ``excursion-bounded``.

Consumes ``firm_rules`` as-is (verify ``dd_lock_offset_usd``; never re-patch).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

import numpy as np
import pandas as pd

from discovery.prop_survivor_scoring import ScoringThresholds
from firm_rules import FIRM_RULES
from research_utils.book_score import TOOLING_DISCLAIMER, score_book
from research_utils.nsurv_channel import (
    DEFAULT_FIRM_KEY,
    SIZING_BASIS_USD,
    NSurvReport,
    score_nsurv,
)

LOWER_BOUND_LABEL = "LOWER BOUND"
HONESTY_LOWER_BOUND = "LOWER BOUND"
HONESTY_EXCURSION = "excursion-bounded"

_REQUIRED_TV = frozenset({"Trade #", "Type", "Date and time", "Net P&L USD"})

# TradingView / reconcile aliases → canonical names (no clobber if both present).
_COLUMN_ALIASES = {
    "Trade number": "Trade #",
    "Net PnL USD": "Net P&L USD",
    "Net PnL %": "Net P&L %",
    "Return %": "Net P&L %",
    "Cumulative PnL USD": "Cumulative P&L USD",
    "Cumulative PnL %": "Cumulative P&L %",
}

# MAE / MFE column candidates (first hit wins). TV historically used Adverse/
# Favorable excursion; some exports use Drawdown / Run-up.
_MAE_CANDIDATES = (
    "Adverse excursion USD",
    "Drawdown USD",
    "Drawdown",
)
_MFE_CANDIDATES = (
    "Favorable excursion USD",
    "Run-up USD",
    "Run-up",
)

_PAREN_RE = re.compile(r"^\((.*)\)$")


def verify_firm_geometry(firm_key: str = DEFAULT_FIRM_KEY) -> float:
    """Read ``dd_lock_offset_usd`` as-is; refuse silently-stale optimistic geometry."""
    if firm_key not in FIRM_RULES:
        raise KeyError(firm_key)
    offset = float(FIRM_RULES[firm_key]["dd_lock_offset_usd"])
    # Eval Select rows must stay on the unreachable-lock encoding (ADR 2026-08-04).
    if firm_key.startswith("Tradeify_Select_") and offset < 1_000_000.0:
        raise ValueError(
            f"{firm_key}: dd_lock_offset_usd={offset} looks like pre-2026-08-04 "
            "optimistic eval lock; refuse to score (verify firm_rules, do not patch)"
        )
    return offset


def _parse_usd(value: Any) -> float:
    """Parse TV currency cells incl. accounting negatives ``($1,500.00)``."""
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return 0.0
    if isinstance(value, (int, float, np.floating, np.integer)):
        return float(value)
    text = str(value).strip().replace(",", "").replace("$", "").replace("USD", "")
    if not text or text.lower() in {"nan", "none", ""}:
        return 0.0
    m = _PAREN_RE.match(text)
    if m:
        return -float(m.group(1))
    return float(text)


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [str(c).strip().replace("\ufeff", "") for c in out.columns]
    rename = {
        src: dst
        for src, dst in _COLUMN_ALIASES.items()
        if src in out.columns and dst not in out.columns
    }
    if rename:
        out = out.rename(columns=rename)
    return out


def _first_present(columns: set[str], candidates: tuple[str, ...]) -> str | None:
    for name in candidates:
        if name in columns:
            return name
    return None


def load_tv_trade_list(path: Path | str) -> pd.DataFrame:
    """Load a TradingView List-of-Trades CSV (Entry + Exit rows)."""
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(p)
    raw = pd.read_csv(p, encoding="utf-8-sig")
    df = _normalize_columns(raw)
    missing = _REQUIRED_TV - set(df.columns)
    if missing:
        raise ValueError(
            f"TV trade list missing columns {sorted(missing)}; got {list(df.columns)}"
        )
    df = df.copy()
    df["dt"] = pd.to_datetime(df["Date and time"], errors="coerce")
    if df["dt"].isna().any():
        raise ValueError(f"unparseable Date and time rows in {p}")
    return df


def pair_exit_legs(df: pd.DataFrame) -> pd.DataFrame:
    """Pair Entry↔Exit by Trade #; realized P&L is the Exit ``Net P&L USD``.

    Mirrors score_cell / trade-csv-reconcile discipline: one Exit row per Trade #
    carries the trade's net. Multi-entry pyramids under one Trade # take the first
    Entry for side/timing metadata; MAE/MFE prefer the Exit cell, else Entry.
    """
    required = _REQUIRED_TV - set(df.columns)
    if required:
        raise ValueError(f"pair_exit_legs missing columns {sorted(required)}")

    work = df.copy()
    if "dt" not in work.columns:
        work["dt"] = pd.to_datetime(work["Date and time"], errors="coerce")

    entries = work[work["Type"].astype(str).str.startswith("Entry")].copy()
    exits = work[work["Type"].astype(str).str.startswith("Exit")].copy()
    if exits.empty:
        raise ValueError("TV trade list has no Exit rows")

    entry_by = entries.set_index("Trade #", drop=False)
    mae_col = _first_present(set(work.columns), _MAE_CANDIDATES)
    mfe_col = _first_present(set(work.columns), _MFE_CANDIDATES)

    rows: list[dict[str, Any]] = []
    for _, ex in exits.iterrows():
        tid = ex["Trade #"]
        if tid not in entry_by.index:
            continue
        en = entry_by.loc[tid]
        if isinstance(en, pd.DataFrame):
            en = en.iloc[0]

        mae_raw = None
        if mae_col is not None:
            for src in (ex, en):
                if mae_col in src.index and pd.notna(src[mae_col]):
                    mae_raw = _parse_usd(src[mae_col])
                    break
        mfe_raw = None
        if mfe_col is not None:
            for src in (ex, en):
                if mfe_col in src.index and pd.notna(src[mfe_col]):
                    mfe_raw = _parse_usd(src[mfe_col])
                    break

        mae_signed: float | None
        if mae_raw is None:
            mae_signed = None
        else:
            mae_signed = float(mae_raw) if mae_raw <= 0.0 else -abs(float(mae_raw))

        rows.append(
            {
                "trade_num": tid,
                "entry_ts": pd.Timestamp(en["dt"]),
                "exit_ts": pd.Timestamp(ex["dt"]),
                "net_pnl_usd": _parse_usd(ex["Net P&L USD"]),
                "mae_usd": mae_signed,
                "mfe_usd": None if mfe_raw is None else float(mfe_raw),
            }
        )

    if not rows:
        raise ValueError("no Entry/Exit pairs found (Trade # join empty)")
    out = pd.DataFrame(rows).sort_values("exit_ts").reset_index(drop=True)
    return out


@dataclass(frozen=True)
class DailyPanelResult:
    """Daily panel plus honesty metadata for the TNEC JSON envelope."""

    frame: pd.DataFrame
    honesty: str
    lower_bound: bool
    n_trades: int
    excursion_columns_used: tuple[str, ...]

    @property
    def honesty_label(self) -> str | None:
        return LOWER_BOUND_LABEL if self.lower_bound else None


def tv_trades_to_daily_panel(
    tv: pd.DataFrame,
    *,
    use_excursion_columns: bool = True,
) -> DailyPanelResult:
    """Build ``date`` / ``pnl_usd`` / ``intraday_low`` from a TV trade list.

    Close-only path: within each exit day, walk exits in time order; running
    realized P&L from the day's open; ``intraday_low = min(0, min(running))``.
    That omits within-trade open excursion → ``LOWER BOUND``.

    Excursion path: when MAE columns are present and ``use_excursion_columns``,
    dip ``running + mae`` before settling each exit's net (bounds within-trade
    adverse excursion in the daily walk).
    """
    legs = pair_exit_legs(tv)
    mae_col = _first_present(set(tv.columns), _MAE_CANDIDATES)
    mfe_col = _first_present(set(tv.columns), _MFE_CANDIDATES)
    have_usable_mae = bool(
        use_excursion_columns
        and mae_col is not None
        and legs["mae_usd"].notna().any()
    )
    used: list[str] = []
    if have_usable_mae and mae_col is not None:
        used.append(mae_col)
    if have_usable_mae and mfe_col is not None:
        used.append(mfe_col)

    legs = legs.copy()
    legs["exit_date"] = pd.to_datetime(legs["exit_ts"]).dt.normalize()

    daily_rows: list[dict[str, Any]] = []
    for day, group in legs.groupby("exit_date", sort=True):
        g = group.sort_values("exit_ts")
        running = 0.0
        day_low = 0.0
        for _, leg in g.iterrows():
            pnl = float(leg["net_pnl_usd"])
            if have_usable_mae and leg["mae_usd"] is not None and not (
                isinstance(leg["mae_usd"], float) and np.isnan(leg["mae_usd"])
            ):
                mae = float(leg["mae_usd"])
                day_low = min(day_low, running + mae)
            running += pnl
            day_low = min(day_low, running)
        daily_rows.append(
            {
                "date": pd.Timestamp(day).normalize(),
                "pnl_usd": float(g["net_pnl_usd"].sum()),
                "intraday_low": float(min(0.0, day_low)),
            }
        )

    frame = pd.DataFrame(daily_rows).sort_values("date").reset_index(drop=True)
    if frame.empty:
        raise ValueError("daily panel is empty after Exit aggregation")
    if np.any(frame["intraday_low"].to_numpy(dtype=float) > 0.0):
        raise ValueError("intraday_low entries must be ≤ 0.0")

    lower_bound = not have_usable_mae
    honesty = HONESTY_LOWER_BOUND if lower_bound else HONESTY_EXCURSION
    return DailyPanelResult(
        frame=frame,
        honesty=honesty,
        lower_bound=lower_bound,
        n_trades=int(len(legs)),
        excursion_columns_used=tuple(used),
    )


def load_tv_daily_panel(
    path: Path | str,
    *,
    use_excursion_columns: bool = True,
) -> DailyPanelResult:
    """Load TV CSV and convert to a daily N-SURV panel."""
    return tv_trades_to_daily_panel(
        load_tv_trade_list(path),
        use_excursion_columns=use_excursion_columns,
    )


def score_daily_panel(
    frame: pd.DataFrame,
    *,
    half_boundary_date: str | pd.Timestamp,
    firm_key: str = DEFAULT_FIRM_KEY,
    sizing_basis_usd: float = SIZING_BASIS_USD,
    thresholds: ScoringThresholds | None = None,
    n_sims: int | None = None,
) -> NSurvReport:
    """Thin pass-through to ``score_nsurv`` after firm-geometry verify."""
    verify_firm_geometry(firm_key)
    return score_nsurv(
        frame,
        half_boundary_date=half_boundary_date,
        firm_key=firm_key,
        sizing_basis_usd=sizing_basis_usd,
        thresholds=thresholds,
        n_sims=n_sims,
    )


def _envelope(
    *,
    nsurv: Mapping[str, Any] | None,
    book: Mapping[str, Any] | None,
    honesty: str,
    lower_bound: bool,
    panel_meta: Mapping[str, Any],
) -> dict[str, Any]:
    """TNEC verdict JSON: channel block + honesty label."""
    out: dict[str, Any] = {
        "disclaimer": TOOLING_DISCLAIMER,
        "honesty": honesty,
        "panel": dict(panel_meta),
    }
    if lower_bound:
        out["honesty_label"] = LOWER_BOUND_LABEL
        out["LOWER BOUND"] = True
    if nsurv is not None:
        out["nsurv"] = nsurv
        out["nsurv_line"] = nsurv.get("nsurv_line")
        out["tnec_nsurv"] = nsurv.get("nsurv")
    if book is not None:
        out["book"] = book
        composed = book.get("composed") or {}
        out["nsurv_line"] = composed.get("nsurv_line")
        out["tnec_nsurv"] = composed.get("nsurv")
    return out


def score_tv_export(
    path: Path | str,
    *,
    half_boundary_date: str | pd.Timestamp,
    firm_key: str = DEFAULT_FIRM_KEY,
    sizing_basis_usd: float = SIZING_BASIS_USD,
    thresholds: ScoringThresholds | None = None,
    n_sims: int | None = None,
    use_excursion_columns: bool = True,
) -> dict[str, Any]:
    """TV CSV → daily panel → ``score_nsurv`` → TNEC verdict JSON dict."""
    panel = load_tv_daily_panel(path, use_excursion_columns=use_excursion_columns)
    report = score_daily_panel(
        panel.frame,
        half_boundary_date=half_boundary_date,
        firm_key=firm_key,
        sizing_basis_usd=sizing_basis_usd,
        thresholds=thresholds,
        n_sims=n_sims,
    )
    return _envelope(
        nsurv=report.to_dict(),
        book=None,
        honesty=panel.honesty,
        lower_bound=panel.lower_bound,
        panel_meta={
            "n_days": int(len(panel.frame)),
            "n_trades": panel.n_trades,
            "excursion_columns_used": list(panel.excursion_columns_used),
            "source": str(path),
        },
    )


def score_tv_book(
    leg_paths: Mapping[str, Path | str],
    *,
    half_boundary_date: str | pd.Timestamp,
    marginal: str | None = None,
    firm_key: str = DEFAULT_FIRM_KEY,
    sizing_basis_usd: float = SIZING_BASIS_USD,
    thresholds: ScoringThresholds | None = None,
    n_sims: int | None = None,
    use_excursion_columns: bool = True,
) -> dict[str, Any]:
    """Convert each TV leg → daily panel → ``score_book`` → JSON dict."""
    verify_firm_geometry(firm_key)
    legs: dict[str, pd.DataFrame] = {}
    honesty_flags: list[bool] = []
    used_cols: list[str] = []
    n_trades = 0
    for name, path in leg_paths.items():
        panel = load_tv_daily_panel(path, use_excursion_columns=use_excursion_columns)
        legs[name] = panel.frame
        honesty_flags.append(panel.lower_bound)
        used_cols.extend(panel.excursion_columns_used)
        n_trades += panel.n_trades

    lower_bound = any(honesty_flags)
    honesty = HONESTY_LOWER_BOUND if lower_bound else HONESTY_EXCURSION
    report = score_book(
        legs,
        half_boundary_date=half_boundary_date,
        marginal=marginal,
        firm_key=firm_key,
        sizing_basis_usd=sizing_basis_usd,
        thresholds=thresholds,
        n_sims=n_sims,
    )
    return _envelope(
        nsurv=None,
        book=report.to_dict(),
        honesty=honesty,
        lower_bound=lower_bound,
        panel_meta={
            "n_legs": len(legs),
            "n_trades": n_trades,
            "excursion_columns_used": sorted(set(used_cols)),
            "leg_names": list(legs.keys()),
        },
    )


def _parse_leg_args(raw: list[str]) -> dict[str, Path]:
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
            "MSL TV→N-SURV adapter (computes, does not admit). "
            "TV List-of-Trades → daily panel → score_nsurv / score_book."
        )
    )
    ap.add_argument(
        "tv_csv",
        nargs="?",
        default=None,
        help="Single-construct TV trade-list CSV (omit when using --leg).",
    )
    ap.add_argument(
        "--leg",
        action="append",
        metavar="NAME=PATH",
        help="TV trade-list leg for composed book scoring; repeat for N≥1.",
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
        help="When N≥2 book legs, also score book-without LEG.",
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
        "--closes-only",
        action="store_true",
        help="Force close-only intraday_low (always LOWER BOUND), ignore MAE cols.",
    )
    ap.add_argument(
        "--json",
        action="store_true",
        default=True,
        help="Emit TNEC verdict JSON (default).",
    )
    ap.add_argument(
        "--text",
        action="store_true",
        help="Emit channel text block instead of JSON.",
    )
    args = ap.parse_args(argv)
    use_exc = not args.closes_only

    if args.leg:
        payload = score_tv_book(
            _parse_leg_args(args.leg),
            half_boundary_date=args.half_boundary,
            marginal=args.marginal,
            firm_key=args.firm,
            n_sims=args.n_sims,
            use_excursion_columns=use_exc,
        )
    elif args.tv_csv:
        payload = score_tv_export(
            args.tv_csv,
            half_boundary_date=args.half_boundary,
            firm_key=args.firm,
            n_sims=args.n_sims,
            use_excursion_columns=use_exc,
        )
    else:
        ap.error("provide a TV CSV path or one or more --leg NAME=PATH")

    if args.text:
        if payload.get("LOWER BOUND"):
            print(LOWER_BOUND_LABEL)
        print(payload.get("nsurv_line", ""))
        print(json.dumps(payload, indent=2, default=str))
    else:
        print(json.dumps(payload, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
