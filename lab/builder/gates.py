"""Gate engine 5a-5g and the stage 8 holdout look (spec: Gate engine).

Gates run in order on the development sessions and a card stops at its first fail. Each gate
records its value, threshold and pass/fail in the report, so a verdict traces to a number.
THRESHOLDS are the spec's proposed defaults; they change only by PR with Joshua's approval, and
the pre-registration freezes them before any card runs. The book's per-session Sharpe with the
candidate added is reported for every card, as a description, not a gate.
"""
from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from builder import compile as C, ledger
from builder.cards import Card
from builder.instruments import INSTRUMENTS

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
    x = np.zeros(len(dates))
    for t, v in zip(trades, net(card, trades, costs)):
        x[pos[t.date]] += v
    return x


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
             book: dict[str, float] | None = None) -> dict:
    if not ledger.contains(ledger_path, card.sha256):
        raise GateError(f"card {card.id} ({card.sha256[:12]}) is not in the ledger")
    T, k = THRESHOLDS, ledger.k(ledger_path, card.instrument)
    days = C.days(card, bars, dev)
    trades = [t for d in days for t in C.simulate_day(card, d)]
    x = daily(card, trades, dev, costs)
    v = net(card, trades, costs)
    rep = {"card_id": card.id, "card_sha256": card.sha256, "instrument": card.instrument,
           "engine_sha256": engine_version(), "data_sha256": data_sha256, "k": k, "thresholds": T,
           "dev_sessions": [dev[0], dev[-1], len(dev)], "trades": len(trades), "net_usd_per_contract": float(v.sum()),
           "session_sharpe": sharpe(x), "cost_per_trade_usd": costs.per_trade(card.instrument), "gates": []}
    rep["book"] = _book(dev, x, book)
    g = rep["gates"]
    half = len(dev) // 2
    h1, h2 = set(dev[:half]), set(dev[half:])
    checks = [
        lambda: _gate(g, "5a sample", len(trades), T["5a_min_trades"], len(trades) >= T["5a_min_trades"]),
        lambda: _gate(g, "5b costs", rep["cost_per_trade_usd"], "firm commission + 1 tick/side, applied", True),
        lambda: _halves(g, card, trades, costs, h1, h2),
        lambda: _plateau(g, card, bars, dev, costs, float(v.sum())),
        lambda: _gate(g, "5e placebo", (s := placebo_beaten_share(card, days, trades, costs, T["5e_placebo_runs"],
                                                                    T["5e_seed"])), T["5e_min_beaten_share"],
                      s >= T["5e_min_beaten_share"]),
        lambda: _gate(g, "5f deflated Sharpe", (r := dsr(x, k))[0], T["5f_min_dsr"], r[0] >= T["5f_min_dsr"]),
        lambda: _book_gate(g, rep["book"]),
    ]
    rep["stopped_at"] = next((g[-1]["gate"] for ch in checks if not ch()), None)
    rep["verdict"] = "survivor" if rep["stopped_at"] is None else "killed"
    return rep


def _halves(g, card, trades, costs, h1, h2) -> bool:
    v1 = net(card, [t for t in trades if t.date in h1], costs)
    v2 = net(card, [t for t in trades if t.date in h2], costs)
    p = [pf(v1), pf(v2)]
    ok = len(v1) > 0 and len(v2) > 0 and min(p) >= THRESHOLDS["5c_min_pf_each_half"]  # an empty half fails
    return _gate(g, "5c halves", {"pf": p, "trades": [len(v1), len(v2)]}, THRESHOLDS["5c_min_pf_each_half"], ok)


def _plateau(g, card, bars, dev, costs, base: float) -> bool:
    kept = {f"{n}{'+' if s > 0 else '-'}": float(net(card, C.simulate(nb, bars, dev), costs).sum() / base)
            if base > 0 else None for n, s, nb in card.neighbours()}
    vals = [r for r in kept.values() if r is not None]
    ok = base > 0 and all(r >= THRESHOLDS["5d_min_profit_kept"] for r in vals)
    return _gate(g, "5d plateau", kept, THRESHOLDS["5d_min_profit_kept"], ok)


def _book(dev: list[str], x: np.ndarray, book: dict[str, float] | None) -> dict:
    common = [i for i, d in enumerate(dev) if book and d in book]
    if not common:
        return {"sessions": 0, "supplied": bool(book)}
    b = np.array([book[dev[i]] for i in common])
    c = x[common]
    lose = b < 0
    closs = c < 0
    return {"sessions": len(common), "supplied": True, "book_s": sharpe(b), "book_s_with_card": sharpe(b + c),
            "corr": float(np.corrcoef(b, c)[0, 1]) if c.std() > 0 and b.std() > 0 else 0.0,
            "mean_on_book_losing_days": float(c[lose].mean()) if lose.any() else 0.0,
            "shared_loss_share": float((closs & lose).sum() / closs.sum()) if closs.any() else 0.0,
            # independence baseline: the book's losing-day share on the card's active days
            "book_losing_share_on_active_days": float(lose[c != 0].mean()) if (c != 0).any() else 0.0}


def _book_gate(g, b: dict) -> bool:
    if not b["sessions"]:
        if b["supplied"]:  # fail closed: a book was given but covers no development session
            return _gate(g, "5g book", "book supplied, no overlapping development sessions", "overlap required", False)
        return _gate(g, "5g book", "book empty", "passes while the book is empty", True)
    ok = b["mean_on_book_losing_days"] > 0 and b["shared_loss_share"] <= THRESHOLDS["5g_max_shared_loss_share"]
    keys = ("mean_on_book_losing_days", "shared_loss_share", "book_losing_share_on_active_days")
    return _gate(g, "5g book", {k: b[k] for k in keys},
                 {"mean_on_book_losing_days": "> 0", "shared_loss_share": THRESHOLDS["5g_max_shared_loss_share"]}, ok)


def holdout_look(card: Card, bars, holdout: list[str], ledger_path: Path, run_id: str, costs: Costs) -> dict:
    """Stage 8: one logged look per survivor. The look is ledgered before any holdout bar is read."""
    ledger.append_holdout_look(ledger_path, run_id, card)
    v = net(card, C.simulate(card, bars, holdout), costs)
    ok = v.sum() > 0 and pf(v) >= THRESHOLDS["8_min_pf"]
    return {"card_sha256": card.sha256, "holdout_sessions": [holdout[0], holdout[-1], len(holdout)],
            "trades": len(v), "net_usd_per_contract": float(v.sum()), "pf": pf(v), "pass": bool(ok)}
