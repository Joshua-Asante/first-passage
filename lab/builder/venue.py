"""Gate 5h: venue Monte Carlo of the combined book (spec: "Bust <= ceiling at >= 2 firm configs;
reports P(pass), P(payout)").

The book (one column, used as given: its embedded costs do not change per config), a
preservation leg (the operator's weekly preservation trade: minus one micro MNQ round trip at the
config's costs on the first weekday of each complete Mon-Fri week) and at most one candidate (one
column, priced per config) form a Mon-Fri panel over the weekdays inside both the book's date
range and the candidate's supplied window; a leg with no session that day is zero. Only complete
Mon-Fri weeks become blocks (``mc.ingest.build_week_blocks``). Each config runs
``mc.simulation.run_seed`` over the pinned seeds from a fresh account, at fixed size, with no
protection (``dd_trigger=10.0``, ``dd_scale=1.0``): 10,000 paths. ``gating_bust`` = headline bust
(daily + static + trailing) + inactivity bust; horizon-cap paths are reported, not counted as bust.

The gate is relative. Book alone and book plus candidate run on the same seeds and the same weeks,
so ``run_seed`` draws the same week sequence for both (common random numbers). A candidate passes
when, in every config, it raises ``gating_bust`` by at most 0.01 and lowers P(pass) by at most 0.01.
``book_bust_target`` (0.05) is reported as ``book_target_met`` for the book alone and with the
candidate; it never gates a candidate. A book-alone run's verdict is ``baseline``. A config the
preflight or the cost table refuses yields a ``refused`` result, never an override.

Settings are pinned by the research coordinator's ticket; thresholds approved by Joshua 2026-11-01.
Not wired into ``gates.py`` or ``run.py`` yet.

Book-alone baseline: ``python -m builder.venue --book <json> --sha256 <hex> --out <json>``.
"""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from builder import data, gates
from builder.instruments import INSTRUMENTS
from mc import preflight
from mc.ingest import build_week_blocks
from mc.simulation import HORIZON_CAP, run_seed

VENUE_THRESHOLDS = {"book_bust_target": 0.05, "5h_max_bust_increase": 0.01, "5h_max_pass_decrease": 0.01}
THRESHOLD_STATUS = "approved by Joshua 2026-11-01"
CONFIGS = {"Tradeify_Select_100K": 0.40, "MFFU_Rapid_100K": 0.50}  # firm -> eval consistency fraction
ACCOUNT = 100_000
SEEDS = tuple(range(20261101, 20261111))
SIMS_PER_SEED = 1000
DD_TRIGGER, DD_SCALE = 10.0, 1.0  # unreachable trigger, unit scale: fixed size, no protection
PRESERVATION_SYMBOL = "MNQ"
LABEL = ("end-of-day research screen: venues enforce drawdown intraday; this panel has no intraday path. "
         "Includes a preservation leg: minus one micro MNQ round trip at the config's costs on the first "
         "weekday of each complete Mon-Fri week, the operator's weekly preservation trade")
ACTIVITY = ("a day is active when any leg has nonzero P&L; inactivity counts consecutive idle rows, "
            "as simulate_path does")


class VenueError(ValueError):
    pass


class Refused(Exception):
    pass


@dataclass(frozen=True)
class Trade:
    exit_date: str  # YYYY-MM-DD
    points: float   # signed, per contract
    symbol: str


@dataclass(frozen=True)
class Candidate:
    trades: tuple[Trade, ...]
    window: tuple[str, str]  # first and last date the candidate was evaluated on, inclusive


def round_trip(firm: str, symbol: str) -> float:
    """2 x (per-symbol commission + 1 tick x point value) at ``firm``'s costs, the same cost as gate
    5b. Raises Refused when the config has no commission for the symbol."""
    try:
        return gates.Costs.for_firm(firm, symbol).per_trade(symbol)
    except (KeyError, ValueError) as e:
        raise Refused(f"{firm}: no commission for {symbol}: {e}") from None


def candidate_daily(c: Candidate, firm: str) -> dict[str, float]:
    """{exit date: sum of points x point value - round trip} at ``firm``'s costs."""
    out: dict[str, float] = {}
    for t in c.trades:
        cost = round_trip(firm, t.symbol)
        out[t.exit_date] = out.get(t.exit_date, 0.0) + t.points * INSTRUMENTS[t.symbol].point_value - cost
    return out


def preservation_daily(firm: str, lo: str, hi: str) -> dict[str, float]:
    """{Monday: minus one MNQ round trip} for each complete Mon-Fri week in lo..hi."""
    cost, end = round_trip(firm, PRESERVATION_SYMBOL), pd.Timestamp(hi)
    return {d.strftime("%Y-%m-%d"): -cost for d in pd.bdate_range(lo, hi)
            if d.weekday() == 0 and d + pd.Timedelta(days=4) <= end}


def window(book: dict[str, float], c: Candidate | None) -> tuple[str, str]:
    lo, hi = min(book), max(book)
    if c is not None:
        lo, hi = max(lo, c.window[0]), min(hi, c.window[1])
    if lo > hi:
        raise VenueError(f"book and candidate windows do not overlap ({lo} > {hi})")
    return lo, hi


def _finite(v) -> bool:
    return not isinstance(v, bool) and isinstance(v, (int, float)) and math.isfinite(v)


def _check(c: Candidate | None, book: dict[str, float]) -> None:
    """Inputs fail closed: a non-finite amount would otherwise become NaN and be zero-filled."""
    bad_amounts = sorted(d for d, v in book.items() if not _finite(v))
    if bad_amounts:
        raise VenueError(f"book has non-finite amounts on: {bad_amounts[:5]}")
    weekend = sorted(d for d in book if pd.Timestamp(d).weekday() > 4)
    if weekend:
        raise VenueError(f"book has weekend dates: {weekend[:5]}")
    if c is None:
        return
    bad_points = sorted({t.exit_date for t in c.trades if not _finite(t.points)})
    if bad_points:
        raise VenueError(f"candidate has non-finite points on: {bad_points[:5]}")
    lo, hi = c.window
    if not (data.DATE.match(lo) and data.DATE.match(hi)) or lo > hi:
        raise VenueError(f"candidate window must be two ordered YYYY-MM-DD dates: {c.window}")
    bad = sorted({t.exit_date for t in c.trades
                  if not data.DATE.match(t.exit_date) or not lo <= t.exit_date <= hi
                  or pd.Timestamp(t.exit_date).weekday() > 4})
    if bad:
        raise VenueError(f"candidate exit dates outside its window or not weekdays: {bad[:5]}")


def panel(columns: dict[str, dict[str, float]], lo: str, hi: str) -> pd.DataFrame:
    """Every weekday lo..hi, one column per leg, zero where a leg has no session."""
    days = pd.bdate_range(lo, hi)
    return pd.DataFrame({name: pd.Series({pd.Timestamp(d): v for d, v in col.items()}, dtype=float)
                         .reindex(days).fillna(0.0) for name, col in columns.items()}, index=days)


def blocks(p: pd.DataFrame) -> np.ndarray:
    b = build_week_blocks(p)
    if not len(b):
        raise VenueError(f"no complete Mon-Fri week in {p.index[0].date()}..{p.index[-1].date()}")
    return b


def simulate(firm: str, p: pd.DataFrame) -> dict:
    """One config over the panel: every outcome bucket, P(pass), gating bust; or refused."""
    try:
        kw = preflight.firm_kwargs(firm, inactivity_off=False, consistency=CONFIGS[firm], account=ACCOUNT,
                                   allow_unsourced_inactivity=False, allow_provisional_rules=False)
    except (KeyError, ValueError) as e:  # EngineUnsupported is a ValueError
        return {"status": "refused", "reason": str(e)}
    b = blocks(p)
    runs = [run_seed(s, SIMS_PER_SEED, b, dd_trigger=DD_TRIGGER, dd_scale=DD_SCALE, horizon=HORIZON_CAP,
                     strats=tuple(p.columns), firm_kwargs=kw, intraday_blocks=None, initial_state=None)
            for s in SEEDS]
    s = preflight.summarize_outcomes(runs, SIMS_PER_SEED)
    n = SIMS_PER_SEED * len(SEEDS)
    counts = {k: sum(r["outcomes"][k] for r in runs) for k in preflight.OUTCOME_KEYS}
    if sum(counts.values()) != n:
        raise VenueError(f"{firm}: outcome counts sum to {sum(counts.values())}, expected {n}")
    g = _gating(counts) / n
    return {"status": "ok", "paths": n, "counts": counts, "rates": s["rates"],
            "headline_bust": s["headline_bust"], "gating_bust": g, "p_pass": counts["pass"] / n,
            "horizon_cap": counts["horizon_cap"] / n, "p_payout": "not encoded",
            "book_target_met": g <= VENUE_THRESHOLDS["book_bust_target"]}


def _gating(counts: dict) -> int:
    return sum(counts[k] for k in preflight.BUST_KEYS) + counts["bust_inactivity"]


def vs_book_alone(r: dict, alone: dict) -> dict:
    """Paired change from count differences, so a change of exactly 100 paths in 10,000 is 0.01."""
    n = r["paths"]
    if alone["paths"] != n:
        raise VenueError(f"unpaired runs: {n} vs {alone['paths']} paths")
    return {"gating_bust": (_gating(r["counts"]) - _gating(alone["counts"])) / n,
            "p_pass": (r["counts"]["pass"] - alone["counts"]["pass"]) / n}


def passes(delta: dict) -> bool:
    return (delta["gating_bust"] <= VENUE_THRESHOLDS["5h_max_bust_increase"]
            and delta["p_pass"] >= -VENUE_THRESHOLDS["5h_max_pass_decrease"])


def evaluate(book: dict[str, float], candidate: Candidate | None = None) -> dict:
    """Gate 5h for the book alone (candidate None) or the book plus one candidate."""
    if not book:
        raise VenueError("book is empty")
    _check(candidate, book)
    lo, hi = window(book, candidate)
    weeks = blocks(panel({"book": book}, lo, hi))
    configs = {}
    for firm in CONFIGS:
        try:
            legs = {"book": book, "preservation": preservation_daily(firm, lo, hi)}
            cand = None if candidate is None else candidate_daily(candidate, firm)
        except Refused as e:
            configs[firm] = {"status": "refused", "reason": str(e)}
            continue
        alone = simulate(firm, panel(legs, lo, hi))
        if cand is None:
            configs[firm] = alone
            continue
        # Same window, seeds and week count as the book-alone run: common random numbers.
        r = simulate(firm, panel({**legs, "candidate": cand}, lo, hi))
        if r["status"] == "ok" and alone["status"] == "ok":
            r["vs_book_alone"] = vs_book_alone(r, alone)
            r["relative_pass"] = passes(r["vs_book_alone"])
        r["book_alone"] = alone
        configs[firm] = r
    if any(c["status"] != "ok" for c in configs.values()):
        verdict = "refused"
    elif candidate is None:
        verdict = "baseline"
    else:
        verdict = "pass" if all(c["relative_pass"] for c in configs.values()) else "fail"
    return {"gate": "5h venue MC", "label": LABEL, "activity_convention": ACTIVITY,
            "thresholds": VENUE_THRESHOLDS, "threshold_status": THRESHOLD_STATUS,
            "settings": {"seeds": [SEEDS[0], SEEDS[-1]], "sims_per_seed": SIMS_PER_SEED, "account": ACCOUNT,
                         "dd_trigger": DD_TRIGGER, "dd_scale": DD_SCALE, "horizon": HORIZON_CAP,
                         "inactivity_off": False, "consistency": CONFIGS, "intraday_blocks": None,
                         "initial_state": None},
            "legs": ["book", "preservation"] + ([] if candidate is None else ["candidate"]),
            "window": [lo, hi], "complete_weeks": len(weeks), "configs": configs, "verdict": verdict}


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description="Gate 5h, book alone.")
    ap.add_argument("--book", type=Path, required=True)
    ap.add_argument("--sha256", required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args(argv)
    rep = {"book_sha256": a.sha256, "engine_sha256": gates.engine_version(),
           **evaluate(data.load_book(a.book, a.sha256))}
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(rep, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {a.out} verdict={rep['verdict']}")


if __name__ == "__main__":
    main()
