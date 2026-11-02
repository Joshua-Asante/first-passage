"""Gate engine 5a-5g and the stage 8 holdout look (spec: Gate engine).

Gates run in order on the development sessions and a card stops at its first fail. Each gate
records its value, threshold and pass/fail in the report, so a verdict traces to a number.
THRESHOLDS are the spec's proposed defaults; they change only by PR with Joshua's approval, and
the pre-registration freezes them before any card runs. The book's per-session Sharpe with the
candidate added is reported for every card, as a description, not a gate.

A card with an unresolved trade (an open position on a day with no bar at or after flat_at) in
its evaluated sessions, or a 5d neighbour with one, gets verdict ``unresolved``: never a
survivor, never killed, reported with the count and dates.
"""
from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from builder import compile as C, data, ledger
from builder.cards import Card
from builder.instruments import INSTRUMENTS

K_SCOPES = ("instrument", "ledger")
PLACEBO_LABEL = "5e placebo_rank (descriptive; timing shuffle with realised side and hold)"

THRESHOLDS = {
    "5a_min_trades": 200,
    "5b_slippage_ticks_per_side": 1,
    "5c_min_pf_each_half": 1.1,
    "5d_min_profit_kept": 0.70,
    "5e_min_beaten_share": 0.95,
    "5e_placebo_runs": 1000,
    "5e_seed": 20261030,
    "5f_min_dsr": 0.95,
    "5g_max_shared_loss_share": 0.50,  # backstop: share of the card's losing days that are also book losing days
    "8_min_pf": 1.0,
}


class GateError(RuntimeError):
    pass


class Unresolved(GateError):
    def __init__(self, source: str, trades: list):
        self.source, self.dates, self.count = source, sorted({t.date for t in trades}), len(trades)
        super().__init__(f"{source}: {self.count} unresolved trade(s) on {self.dates[:5]}")

    def report(self) -> dict:
        return {"source": self.source, "count": self.count, "dates": self.dates}


def resolved(trades: list, source: str) -> list:
    """The trades, or Unresolved when any has no causal exit price."""
    bad = [t for t in trades if t.unresolved]
    if bad:
        raise Unresolved(source, bad)
    return trades


@dataclass(frozen=True)
class Costs:
    commission_per_side: float  # USD per contract per side, from the firm config
    slippage_ticks_per_side: float = THRESHOLDS["5b_slippage_ticks_per_side"]

    @classmethod
    def for_firm(cls, firm_key: str, instrument: str) -> "Costs":
        """Commission from FIRM_RULES via the discovery cost model; raises where no row exists."""
        from discovery.cost_model import resolve_commission
        return cls(resolve_commission(firm_key, instrument))

    def per_trade(self, instrument: str) -> float:
        i = INSTRUMENTS[instrument]
        return 2 * (self.commission_per_side + self.slippage_ticks_per_side * i.tick * i.point_value)


def engine_version() -> str:
    h = hashlib.sha256()
    for p in sorted(Path(__file__).parent.glob("*.py")):
        h.update(p.name.encode() + p.read_bytes().replace(b"\r\n", b"\n"))
    return h.hexdigest()


def net(card: Card, trades: list[C.Trade], costs: Costs) -> np.ndarray:
    pv, c = INSTRUMENTS[card.instrument].point_value, costs.per_trade(card.instrument)
    return np.array([t.points * pv - c for t in trades])


def daily(card: Card, trades: list[C.Trade], dates: list[str], costs: Costs) -> np.ndarray:
    pos = {d: i for i, d in enumerate(dates)}
    stray = sorted({t.date for t in trades} - set(pos))
    if stray:
        raise GateError(f"trades dated outside the evaluated sessions: {stray[:5]}")
    x = np.zeros(len(dates))
    for t, v in zip(trades, net(card, trades, costs)):
        x[pos[t.date]] += v
    return x


def check_dates(card: Card, bars, dates: list[str]) -> None:
    """Evaluated dates are non-empty, sorted, unique sessions of the loaded bars."""
    if not dates or list(dates) != sorted(set(dates)):
        raise GateError(f"{card.id}: evaluated dates must be non-empty, sorted and unique")
    unknown = sorted(set(dates) - set(data.session_dates(bars, card.instrument)))
    if unknown:
        raise GateError(f"{card.id}: dates that are not sessions of the bars: {unknown[:5]}")


def pf(v: np.ndarray) -> float:
    loss = -v[v < 0].sum()
    return math.inf if loss == 0 else float(v[v > 0].sum() / loss)


def sharpe(x: np.ndarray) -> float:
    sd = x.std(ddof=1) if len(x) > 1 else 0.0
    return float(x.mean() / sd) if sd > 0 else 0.0


def dsr(x: np.ndarray, k: int) -> tuple[float, float]:
    """Deflated Sharpe of the per-session series at K trials. The across-trial variance is the
    null sampling variance of a per-session Sharpe, 1/(n-1), so it does not depend on results."""
    from research_utils.deflated_sharpe import deflated_sharpe, expected_max_sharpe, moments_from_returns
    sr, n, skew, kurt = moments_from_returns(list(x))
    sr0 = expected_max_sharpe(k, 1.0 / (n - 1))
    return deflated_sharpe(sr, n, skew, kurt, sr0), sr0


def placebo_beaten_share(card: Card, days: list[C.Day], trades: list[C.Trade], costs: Costs,
                         runs: int, seed: int) -> float:
    """Share of timing-shuffled runs whose net profit is below the card's. Each run keeps every
    trade's day, side and holding length in bars, and redraws its entry bar uniformly from that
    day's live entry bars; entry at that bar's open, exit at the open `hold` bars later (capped
    at the flat bar), or the last close when the day has no flat bar."""
    if not trades:
        return 0.0
    by = {d.date: d for d in days}
    pv, c = INSTRUMENTS[card.instrument].point_value, costs.per_trade(card.instrument)
    rng = np.random.default_rng(seed)
    tot = np.zeros(runs)
    for t in trades:
        d = by[t.date]
        e = rng.integers(d.first, d.cutoff, size=runs)
        x = np.minimum(e + (t.exit_i - t.entry_i), d.flat)
        n = len(d.times)
        exit_px = np.where(x < n, d.o[np.minimum(x, n - 1)], d.c[n - 1])
        exit_px = np.where(x == e, d.c[e], exit_px)
        tot += t.side * (exit_px - d.o[e]) * pv - c
    real = net(card, trades, costs).sum()
    return float((tot < real).mean())


def _gate(gates: list, name: str, value, threshold, ok: bool) -> bool:
    gates.append({"gate": name, "value": value, "threshold": threshold, "pass": bool(ok)})
    return ok


def evaluate(card: Card, bars, dev: list[str], ledger_path: Path, costs: Costs, data_sha256: str,
             book: dict[str, float] | None = None, *, closed: frozenset[str], k_scope: str) -> dict:
    """``closed`` is the frozen calendar's dates; ``k_scope`` picks K for 5f (see ledger.k)."""
    if not ledger.contains(ledger_path, card.sha256):
        raise GateError(f"card {card.id} ({card.sha256[:12]}) is not in the ledger")
    if k_scope not in K_SCOPES:
        raise GateError(f"k_scope must be one of {K_SCOPES}, got {k_scope!r}")
    check_dates(card, bars, dev)
    if len(dev) < 2:
        raise GateError(f"{card.id}: 5c needs two development halves; got {len(dev)} session(s)")
    T, k = THRESHOLDS, ledger.k(ledger_path, card.instrument if k_scope == "instrument" else None)
    skipped: dict[str, int] = {}
    days = C.days(card, bars, dev, skipped, closed)
    trades = [t for d in days for t in C.simulate_day(card, d)]
    rep = {"card_id": card.id, "card_sha256": card.sha256, "instrument": card.instrument,
           "engine_sha256": engine_version(), "data_sha256": data_sha256, "k": k, "k_scope": k_scope,
           "thresholds": T, "dev_sessions": [dev[0], dev[-1], len(dev)], "trades": len(trades),
           "cost_per_trade_usd": costs.per_trade(card.instrument), "skipped_days": skipped, "gates": []}
    try:
        resolved(trades, "card")
    except Unresolved as u:
        return {**rep, "verdict": "unresolved", "stopped_at": None, "unresolved": u.report(), "book": {}}
    x = daily(card, trades, dev, costs)
    v = net(card, trades, costs)
    rep.update(net_usd_per_contract=float(v.sum()), session_sharpe=sharpe(x), book=_book(dev, x, book))
    g = rep["gates"]
    half = len(dev) // 2
    h1, h2 = set(dev[:half]), set(dev[half:])
    checks = [
        lambda: _gate(g, "5a sample", len(trades), T["5a_min_trades"], len(trades) >= T["5a_min_trades"]),
        lambda: _gate(g, "5b costs", rep["cost_per_trade_usd"], "firm commission + 1 tick/side, applied", True),
        lambda: _halves(g, card, trades, costs, h1, h2),
        lambda: _plateau(g, card, bars, dev, costs, float(v.sum()), closed),
        lambda: _gate(g, PLACEBO_LABEL, (s := placebo_beaten_share(card, days, trades, costs, T["5e_placebo_runs"],
                                                                    T["5e_seed"])), T["5e_min_beaten_share"],
                      s >= T["5e_min_beaten_share"]),
        lambda: _dsr_gate(g, x, k),
        lambda: _book_gate(g, rep["book"]),
    ]
    try:
        rep["stopped_at"] = next((g[-1]["gate"] for ch in checks if not ch()), None)
    except Unresolved as u:  # a 5d neighbour has no causal exit on some day
        return {**rep, "verdict": "unresolved", "stopped_at": "5d plateau", "unresolved": u.report()}
    rep["verdict"] = "survivor" if rep["stopped_at"] is None else "killed"
    return rep


def _dsr_gate(g, x: np.ndarray, k: int) -> bool:
    try:
        d, _ = dsr(x, k)
    except ValueError as e:  # e.g. zero variance: DSR undefined, so the gate fails closed
        return _gate(g, "5f deflated Sharpe", f"undefined ({e})", THRESHOLDS["5f_min_dsr"], False)
    return _gate(g, "5f deflated Sharpe", d, THRESHOLDS["5f_min_dsr"], d >= THRESHOLDS["5f_min_dsr"])


def _halves(g, card, trades, costs, h1, h2) -> bool:
    v1 = net(card, [t for t in trades if t.date in h1], costs)
    v2 = net(card, [t for t in trades if t.date in h2], costs)
    p = [pf(v1), pf(v2)]
    ok = len(v1) > 0 and len(v2) > 0 and min(p) >= THRESHOLDS["5c_min_pf_each_half"]  # an empty half fails
    return _gate(g, "5c halves", {"pf": p, "trades": [len(v1), len(v2)]}, THRESHOLDS["5c_min_pf_each_half"], ok)


def _plateau(g, card, bars, dev, costs, base: float, closed: frozenset[str] = frozenset()) -> bool:
    """Every valid +-1 step neighbour keeps the threshold share of a positive base net; invalid
    neighbours (value or timing) are named as skipped. A neighbour with an unresolved trade raises
    Unresolved."""
    nbs = [(f"{n}{'+' if s > 0 else '-'}", nb) for n, s, nb in card.neighbours()]
    if base <= 0:
        return _gate(g, "5d plateau", {"base_net": base}, "base net > 0", False)
    kept = {name: float(net(card, resolved(C.simulate(nb, bars, dev, closed), f"neighbour {name}"), costs).sum() / base)
            for name, nb in nbs if nb}
    ok = all(r >= THRESHOLDS["5d_min_profit_kept"] for r in kept.values())
    return _gate(g, "5d plateau", {"kept": kept, "skipped_invalid": [name for name, nb in nbs if not nb]},
                 THRESHOLDS["5d_min_profit_kept"], ok)


def _book(dev: list[str], x: np.ndarray, book: dict[str, float] | None) -> dict:
    common = [i for i, d in enumerate(dev) if book is not None and d in book]
    if not common:
        return {"sessions": 0, "supplied": book is not None}  # {} supplied is not "no book"
    b = np.array([book[dev[i]] for i in common])
    c = x[common]
    lose = b < 0
    closs = c < 0
    return {"sessions": len(common), "supplied": True, "book_s": sharpe(b), "book_s_with_card": sharpe(b + c),
            "corr": float(np.corrcoef(b, c)[0, 1]) if c.std() > 0 and b.std() > 0 else 0.0,
            "mean_on_book_losing_days": float(c[lose].mean()) if lose.any() else None,  # undefined: 5g fails
            "shared_loss_share": float((closs & lose).sum() / closs.sum()) if closs.any() else 0.0,
            # independence baseline: the book's losing-day share on the card's active days
            "book_losing_share_on_active_days": float(lose[c != 0].mean()) if (c != 0).any() else 0.0}


def _book_gate(g, b: dict) -> bool:
    if not b["sessions"]:
        if b["supplied"]:  # fail closed: a book was given but covers no development session
            return _gate(g, "5g book", "book supplied, no overlapping development sessions", "overlap required", False)
        return _gate(g, "5g book", "book empty", "passes while the book is empty", True)
    m = b["mean_on_book_losing_days"]
    ok = m is not None and m > 0 and b["shared_loss_share"] <= THRESHOLDS["5g_max_shared_loss_share"]
    keys = ("mean_on_book_losing_days", "shared_loss_share", "book_losing_share_on_active_days")
    return _gate(g, "5g book", {k: b[k] for k in keys},
                 {"mean_on_book_losing_days": "> 0", "shared_loss_share": THRESHOLDS["5g_max_shared_loss_share"]}, ok)


def holdout_look(card: Card, bars, holdout: list[str], ledger_path: Path, run_id: str, costs: Costs,
                 *, closed: frozenset[str]) -> dict:
    """Stage 8: one logged look per survivor. The look is ledgered before any holdout bar is read.
    An unresolved holdout trade spends the look and fails it, reported with its count and dates."""
    check_dates(card, bars, holdout)
    ledger.append_holdout_look(ledger_path, run_id, card)
    rep = {"card_sha256": card.sha256, "holdout_sessions": [holdout[0], holdout[-1], len(holdout)]}
    try:
        v = net(card, resolved(C.simulate(card, bars, holdout, closed), "holdout"), costs)
    except Unresolved as u:
        return {**rep, "verdict": "unresolved", "unresolved": u.report(), "pass": False}
    ok = v.sum() > 0 and pf(v) >= THRESHOLDS["8_min_pf"]
    return {**rep, "verdict": "pass" if ok else "fail", "trades": len(v), "net_usd_per_contract": float(v.sum()),
            "pf": pf(v), "pass": bool(ok)}
