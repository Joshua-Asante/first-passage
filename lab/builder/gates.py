"""Gate engine 5a-5f, the stage 8 holdout look and the 5g placement check (spec: Gate engine).

Gates 5a-5f run in order on the development sessions and a card stops at its first fail. Each gate
records its value, threshold and pass/fail in the report, so a verdict traces to a number.
THRESHOLDS are the spec's proposed defaults; they change only by PR with Joshua's approval, and
the pre-registration freezes them before any card runs. The card's development-window book
statistics (``_book``) are reported for every card, as a description, not a gate.

5g is portfolio fit (ten-step order, step 10; branch B, Joshua 2026-11-04). It is not a
development gate: ``holdout_look`` runs it only after a holdout pass, on the book statistics
already in the development report, and records ``placement: clear | fail`` beside the look's
verdict, with the pinned book's sha256. A placement fail rejects the placement, never the
candidate. A run that declares no book (``book: null``) gets ``placement: not_evaluated``, never
a clear (follow-up to the same ruling: no silent passes).

A card with an unresolved trade (an open position on a day with no bar at or after flat_at) in
its evaluated sessions, or a 5d neighbour with one, gets verdict ``unresolved``: never a
survivor, never killed, reported with the count and dates.
"""
from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass, replace
from pathlib import Path

import numpy as np

from builder import compile as C, data, ledger
from builder.cards import Card, _timing_error
from builder.instruments import DAY_END, INSTRUMENTS, minutes

K_SCOPES = ("instrument", "ledger")
PLACEBO_LABEL = "5e placebo_rank (timing-only, not the mechanism discriminator; same-day window slide of the clock frame)"
COSTS_LABEL = "5b costs applied (not a gate)"
PLACEMENT_LABEL = "5g placement (step 10; after a holdout pass, never a kill)"

THRESHOLDS = {
    "5a_min_trades": 200,
    "5b_slippage_ticks_per_side": 1,
    "5c_min_pf_each_half": 1.1,
    "5d_min_profit_kept": 0.70,
    "5e_min_beaten_share": 0.95,
    "5e_placebo_runs": 1000,
    "5e_seed": 20261030,
    "5f_min_dsr": 0.95,
    "5g_max_shared_loss_share": 0.50,  # placement backstop: share of the card's losing days that are also book losing days
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


# D7 (generation-phase note §9.2): the benchmarks of the report-only reachability line; not gates
REACH = {"sessions_per_year": 252, "true_sharpe": (0.85, 0.89), "reachable_at": 0.89}


def reachability(k: int, n: int) -> dict:
    """D7's report-only reach of gate 5f at K trials over n development sessions (ADR 2026-07-12
    §2.4 power disclosure). Under near-normal moments 5f passes when the per-session Sharpe is at
    least SR0 + z/sqrt(n-1), with SR0 the same ``expected_max_sharpe(k, 1/(n-1))`` that ``dsr``
    uses and z the normal quantile of the 5f threshold. P(pass) at a true annual Sharpe S is the
    normal approximation Phi((S - floor_annual) * sqrt((n-1)/252)). Both drop the PSR
    denominator's (1 + SR^2/2) term, so at the floor the exact DSR sits a few 1e-4 below the
    threshold. ``reachable`` means floor_annual <= 0.89 (the futures-native best). It never
    changes a gate, a threshold or a verdict."""
    from statistics import NormalDist
    from research_utils.deflated_sharpe import expected_max_sharpe
    if n < 2:
        raise ValueError(f"reachability needs at least 2 development sessions, got {n}")
    nd, py = NormalDist(), REACH["sessions_per_year"]
    sr0 = float(expected_max_sharpe(k, 1.0 / (n - 1)))
    floor = sr0 + nd.inv_cdf(THRESHOLDS["5f_min_dsr"]) / math.sqrt(n - 1)
    ann = floor * math.sqrt(py)
    p_pass = {f"{s:.2f}": nd.cdf((s - ann) * math.sqrt((n - 1) / py)) for s in REACH["true_sharpe"]}
    return {"k": k, "dev_sessions": n, "floor_per_session": floor, "floor_annual": ann, "p_pass": p_pass,
            "reachable": bool(ann <= REACH["reachable_at"]), "reachable_at": REACH["reachable_at"],
            "basis": "5f only, normal approximation; a description, not a gate"}


# 5e null size (lesson M-17): the fewest valid slides (delta != 0) 5e accepts. Each run draws the
# real window (delta 0) as well as the slides, so under per-session exchangeability of the window
# nets the card's total and a run's total are identically distributed, and the zero-edge false
# pass is the nominal 1 - 5e_min_beaten_share for any |S| >= 1. Two slides is the floor so that
# the null rests on more than one alternative anchor.
SLIDE_MIN = 2


def slid(card: Card, delta: int) -> Card | None:
    """The card with its whole clock frame moved ``delta`` 15m bars on the same day: the range's
    offset (a first_n_bars range becomes the equivalent time_window), entry_cutoff and flat_at.
    Every other rule is the card's. None for delta 0, a negative offset, an invalid timing, or a
    flat_at at DAY_END: the trading day has no bar there, so every slid trade a stop does not end
    is unresolved, and scoring those 0 would keep only the stopped losers."""
    off = int(card.p("offset_bars", 0)) + delta
    cut, flat = minutes(card.entry_cutoff) + C.BAR_MIN * delta, minutes(card.flat_at) + C.BAR_MIN * delta
    if delta == 0 or off < 0 or cut < 0 or flat >= minutes(DAY_END):
        return None
    step = next((s for n, _, s in card.params if n == "offset_bars"), 1)
    ps = tuple(sorted([q for q in card.params if q[0] != "offset_bars"] + [("offset_bars", off, step)]))
    c = replace(card, range="time_window", params=ps, entry_cutoff=f"{cut // 60:02d}:{cut % 60:02d}",
                flat_at=f"{flat // 60:02d}:{flat % 60:02d}", sha256="", source="")
    return None if _timing_error(c) else c


def slides(card: Card) -> list[tuple[int, Card]]:
    """5e's slide set S: every valid same-day shift of the card's clock frame, by delta."""
    span = 24 * 60 // C.BAR_MIN
    return [(d, c) for d in range(-span, span + 1) if (c := slid(card, d)) is not None]


def slide_line(card: Card) -> dict:
    """5e's null size, printed at registration beside D7's line: |S| (slides other than delta 0)
    and the slid span. A description; 5e fails closed below SLIDE_MIN."""
    s = slides(card)
    return {"slides": len(s), "min_slides": SLIDE_MIN, "meets_min": len(s) >= SLIDE_MIN,
            "windows_drawn": len(s) + 1,
            "delta_bars": [s[0][0], s[-1][0]] if s else None,
            "range_start": [s[0][1].range_start(), s[-1][1].range_start()] if s else None,
            "flat_at": [s[0][1].flat_at, s[-1][1].flat_at] if s else None}


def slide_matrix(S: list[tuple[int, Card]], bars, dev: list[str], costs: Costs,
                 closed: frozenset[str] = frozenset()) -> tuple[np.ndarray, int, int]:
    """net[session][slide] over the development sessions, with the counts of slid sessions that
    were unresolved and skipped. Both contribute 0; neither raises."""
    pos = {d: i for i, d in enumerate(dev)}
    m = np.zeros((len(dev), len(S)))
    unresolved = skipped = 0
    for j, (_, c) in enumerate(S):
        sk: dict[str, int] = {}
        for day in C.days(c, bars, dev, sk, closed):
            tr = C.simulate_day(c, day)
            if any(t.unresolved for t in tr):
                unresolved += 1
            elif tr:
                m[pos[day.date], j] = net(c, tr, costs).sum()
        skipped += sum(sk.values())
    return m, unresolved, skipped


def placebo_beaten_share(card: Card, bars, dev: list[str], trades: list[C.Trade], costs: Costs,
                         runs: int, seed: int, closed: frozenset[str] = frozenset()) -> dict:
    """5e, the same-day window-slide placebo (lesson M-17). For each slide in S the shifted card
    runs through compile.py on the development sessions, so each slid trade's side and entry use
    only that day's bars up to its entry bar. Each run draws one window per session from S and the
    card's own (delta 0), uniformly and independently, and sums the sessions' net; ``beaten_share`` is the share of runs below the
    card's net. A session the slide skips, or whose slid trade is unresolved, contributes 0 (the
    unresolved ones are counted). Fails closed (``beaten_share`` None, with ``reason``) below
    SLIDE_MIN slides or on a zero-variance null."""
    line = slide_line(card)
    real = float(net(card, trades, costs).sum())
    out = {**line, "real_net": real}
    if not trades:
        return {**out, "beaten_share": 0.0, "reason": "no trades"}
    S = slides(card)
    if len(S) < SLIDE_MIN:
        return {**out, "beaten_share": None,
                "reason": f"{len(S)} valid slide(s), fewer than {SLIDE_MIN}: the 5e null is too small"}
    m, unresolved, skipped = slide_matrix(S, bars, dev, costs, closed)
    m = np.column_stack([daily(card, trades, dev, costs), m])  # delta 0, the card itself, is drawn too
    pick = np.random.default_rng(seed).integers(0, len(S) + 1, size=(runs, len(dev)))
    # USD at 1e-6: summation order must not split ties with the card or give a degenerate null variance
    tot, real = np.round(m[np.arange(len(dev)), pick].sum(axis=1), 6), round(real, 6)
    out.update(slid_unresolved_sessions=unresolved, slid_skipped_sessions=skipped,
               null_mean=float(tot.mean()), null_sd=float(tot.std()))
    if np.ptp(tot) == 0:
        return {**out, "beaten_share": None, "reason": "the slide null has zero variance"}
    return {**out, "beaten_share": float((tot < real).mean())}


def _gate(gates: list, name: str, value, threshold, ok: bool) -> bool:
    gates.append({"gate": name, "value": value, "threshold": threshold, "pass": bool(ok)})
    return ok


def k_for(ledger_path: Path, instrument: str, k_scope: str) -> int:
    """The K gate 5f deflates against: the instrument's distinct ledgered cards, or the ledger's."""
    return ledger.k(ledger_path, instrument if k_scope == "instrument" else None)


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
    T, k = THRESHOLDS, k_for(ledger_path, card.instrument, k_scope)
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
        lambda: _gate(g, COSTS_LABEL, rep["cost_per_trade_usd"], "firm commission + 1 tick/side, applied", True),
        lambda: _halves(g, card, trades, costs, h1, h2),
        lambda: _plateau(g, card, bars, dev, costs, float(v.sum()), closed),
        lambda: _gate(g, PLACEBO_LABEL, (s := placebo_beaten_share(card, bars, dev, trades, costs, T["5e_placebo_runs"],
                                                                    T["5e_seed"], closed)), T["5e_min_beaten_share"],
                      s["beaten_share"] is not None and s["beaten_share"] >= T["5e_min_beaten_share"]),
        lambda: _dsr_gate(g, x, k),
    ]  # 5g is not here: it is placement, run after a holdout pass (holdout_look)
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


BOOK_KEYS = ("mean_on_book_losing_days", "shared_loss_share", "book_losing_share_on_active_days")


def check_book_stats(b) -> None:
    """The development report's ``book`` block has the shape ``_book`` writes, or GateError."""
    ok = isinstance(b, dict) and type(b.get("sessions")) is int and b["sessions"] >= 0 \
        and type(b.get("supplied")) is bool and (b["supplied"] or not b["sessions"])
    if ok and b["sessions"]:  # only the mean is undefined (None) when the book has no losing day
        ok = all(k in b for k in BOOK_KEYS) and all(
            (k == "mean_on_book_losing_days" and b[k] is None)
            or (not isinstance(b[k], bool) and isinstance(b[k], (int, float)) and math.isfinite(b[k]))
            for k in BOOK_KEYS) and all(0 <= b[k] <= 1 for k in BOOK_KEYS[1:])  # the two shares
    if not ok:
        raise GateError(f"development report book statistics are malformed: {b!r}"[:300])


def check_book_identity(b: dict, book_sha256: str | None) -> None:
    """A supplied book comes with its pinned sha256 and a declared-empty one with None, or GateError."""
    if b["supplied"] != (book_sha256 is not None):
        raise GateError(f"book statistics (supplied={b['supplied']}) do not match the pinned book sha256 {book_sha256!r}")


def _book_gate(g, b: dict) -> bool:
    """5g on a supplied book's statistics. There is no rule for no book: that is not evaluated."""
    if not b["supplied"]:
        raise GateError("5g needs a supplied book; without one placement is not evaluated")
    if not b["sessions"]:  # fail closed: a book was given but covers no development session
        return _gate(g, PLACEMENT_LABEL, "book supplied, no overlapping development sessions", "overlap required",
                     False)
    m = b["mean_on_book_losing_days"]
    ok = m is not None and m > 0 and b["shared_loss_share"] <= THRESHOLDS["5g_max_shared_loss_share"]
    return _gate(g, PLACEMENT_LABEL, {k: b[k] for k in BOOK_KEYS},
                 {"mean_on_book_losing_days": "> 0", "shared_loss_share": THRESHOLDS["5g_max_shared_loss_share"]}, ok)


def placement(b: dict) -> dict:
    """Step 10 portfolio fit on the development-window book statistics: ``placement`` is
    ``clear`` or ``fail``, with the 5g record, or ``not_evaluated`` (no gate record) when the run
    declares no book. It reads no data and never changes a verdict."""
    check_book_stats(b)
    if not b["supplied"]:
        return {"placement": "not_evaluated", "placement_gate": None}
    g: list = []
    return {"placement": "clear" if _book_gate(g, b) else "fail", "placement_gate": g[0]}


def holdout_look(card: Card, bars, holdout: list[str], ledger_path: Path, run_id: str, costs: Costs,
                 *, closed: frozenset[str], book: dict, book_sha256: str | None) -> dict:
    """Stage 8: one logged look per survivor. The look is ledgered before any holdout bar is read.
    An unresolved holdout trade spends the look and fails it, reported with its count and dates.
    ``book`` is the development report's book statistics; after a pass, 5g runs on them and sets
    ``placement`` (``clear`` | ``fail``, or ``not_evaluated`` without a book) beside the verdict.
    Without a pass ``placement`` is None. ``book_sha256`` is the run's pinned book (None for
    ``book: null``) and is recorded as ``placement_book_sha256``."""
    check_dates(card, bars, holdout)
    check_book_stats(book)  # before the look is spent
    check_book_identity(book, book_sha256)
    ledger.append_holdout_look(ledger_path, run_id, card)
    rep = {"card_sha256": card.sha256, "holdout_sessions": [holdout[0], holdout[-1], len(holdout)],
           "placement": None, "placement_gate": None, "placement_book_sha256": book_sha256}
    try:
        v = net(card, resolved(C.simulate(card, bars, holdout, closed), "holdout"), costs)
    except Unresolved as u:
        return {**rep, "verdict": "unresolved", "unresolved": u.report(), "pass": False}
    ok = v.sum() > 0 and pf(v) >= THRESHOLDS["8_min_pf"]
    if ok:
        rep.update(placement(book))
    return {**rep, "verdict": "pass" if ok else "fail", "trades": len(v), "net_usd_per_contract": float(v.sum()),
            "pf": pf(v), "pass": bool(ok)}
