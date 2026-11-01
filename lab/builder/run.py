"""One builder run: ``python -m builder.run <run.yaml>`` (spec stages 0-7, locally).

run.yaml (exactly these keys; commission_per_side is the only optional one):
    run_id: mcl-orb-r1
    ledger: <path to ledger.jsonl>         # outside the repo for real runs
    firm: Tradeify_Select_100K
    data: {MCL: {path: <BAR_EXPORT_v0.2 csv>, sha256: <pinned>,
                 split: {dev_end: 2025-06-30, holdout_end: 2026-06-30}}}
    roll: "TV 1! continuous series as exported; no roll reconstructed"
    book: {path: <JSON {date: book P&L per session}>, sha256: <pinned>, min_overlap: 500}
                                           # or null: an empty book, declared
    calendar: {path: ops/calendars/cme_holiday_calendar_2022_2026.json, sha256: <pinned>}
    k_scope: ledger                        # or instrument: K for 5f across the ledger or per instrument
    cards: [<card yaml paths>]
    out: <report directory>
    commission_per_side: {XYZ: 1.00}      # only where FIRM_RULES has no row (refused otherwise); cite it in the prereg

Order: the spec, cards, costs, book and calendar are validated, then every card is appended to
the ledger before any bar is read, then the data is loaded and checked, the split resolved on
its session dates, and the book must cover ``min_overlap`` development sessions of every
instrument before any card is evaluated. Reports land in ``out/<card id>.report.json`` with a
one-line verdict each, and each report's sha256, in ``out/verdict.json``: deleted before the
cards are ledgered and written last, so it marks a finished attempt (builder.holdout reads it).
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import math
import sys
from pathlib import Path

import yaml

from builder import cards, data, gates, ledger

REQUIRED = {"run_id", "ledger", "firm", "data", "roll", "cards", "out", "book", "calendar", "k_scope"}
OPTIONAL = {"commission_per_side"}


class RunError(ValueError):
    pass


def _positive(v) -> bool:
    return not isinstance(v, bool) and isinstance(v, (int, float)) and math.isfinite(v) and v > 0


def _costs(firm: str, instrument: str, override) -> gates.Costs:
    """FIRM_RULES first; an override is allowed only where the firm has no row, and must be > 0."""
    try:
        firm_costs = gates.Costs.for_firm(firm, instrument)
    except ValueError:
        if not _positive(override):
            raise RunError(f"{instrument}: no {firm} commission row; a positive commission_per_side is required") from None
        return gates.Costs(float(override))
    if override is not None:
        raise RunError(f"{instrument}: {firm} has a commission row; remove the commission_per_side override")
    if not _positive(firm_costs.commission_per_side):
        raise RunError(f"{instrument}: {firm} commission {firm_costs.commission_per_side} is not positive")
    return firm_costs


def _date(v, ctx: str) -> str:
    """A YYYY-MM-DD string, or the date YAML parses an unquoted one into."""
    if type(v) is dt.date:
        v = v.isoformat()
    if not data._iso(v):
        raise RunError(f"{ctx} must be a YYYY-MM-DD date, got {v!r}")
    return v


def _split(inst: str, v) -> dict:
    if not isinstance(v, dict) or set(v) != {"dev_end", "holdout_end"}:
        raise RunError(f"data.{inst}.split must be {{dev_end, holdout_end}}")
    s = {k: _date(v[k], f"data.{inst}.split.{k}") for k in ("dev_end", "holdout_end")}
    if not s["dev_end"] < s["holdout_end"]:
        raise RunError(f"data.{inst}.split: dev_end must be before holdout_end")
    return s


def spec(path: Path) -> dict:
    s = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(s, dict) or not REQUIRED <= set(s) or set(s) - REQUIRED - OPTIONAL:
        got = sorted(s) if isinstance(s, dict) else s
        raise RunError(f"run.yaml needs keys {sorted(REQUIRED)} (optional {sorted(OPTIONAL)}); got {got}")
    if not isinstance(s["run_id"], str) or not s["run_id"]:
        raise RunError("run_id must be a non-empty string")
    if not isinstance(s["data"], dict) or any(not isinstance(v, dict) or set(v) != {"path", "sha256", "split"}
                                               for v in s["data"].values()):
        raise RunError("data must map each instrument to {path, sha256, split}")
    for i, v in s["data"].items():
        v["split"] = _split(i, v["split"])
    b = s["book"]
    if b is not None and (not isinstance(b, dict) or set(b) != {"path", "sha256", "min_overlap"}
                          or isinstance(b["min_overlap"], bool) or not isinstance(b["min_overlap"], int)
                          or b["min_overlap"] < 1):
        raise RunError("book must be null or {path, sha256, min_overlap: int >= 1}")
    if not isinstance(s["calendar"], dict) or set(s["calendar"]) != {"path", "sha256"}:
        raise RunError("calendar must be {path, sha256}")
    if s["k_scope"] not in gates.K_SCOPES:
        raise RunError(f"k_scope must be one of {list(gates.K_SCOPES)}")
    if not isinstance(s["cards"], list) or not s["cards"]:
        raise RunError("cards must be a non-empty list")
    return s


def load_cards(s: dict) -> list[cards.Card]:
    cs = [cards.parse(Path(p).read_text(encoding="utf-8")) for p in s["cards"]]
    for what, vals in (("ids", [c.id for c in cs]), ("hashes", [c.sha256 for c in cs])):
        if len(set(vals)) != len(vals):
            raise RunError(f"duplicate card {what}: {sorted({v for v in vals if vals.count(v) > 1})}")
    missing = {c.instrument for c in cs} - set(s["data"])
    if missing:
        raise RunError(f"no data for {sorted(missing)}")
    return cs


def costs(s: dict, instruments) -> dict[str, gates.Costs]:
    overrides = s.get("commission_per_side") or {}
    return {i: _costs(s["firm"], i, overrides.get(i)) for i in instruments}


def load_data(s: dict, instrument: str, calendar: data.Calendar):
    """(bars, development sessions, holdout sessions, load summary) under the pinned split."""
    d = s["data"][instrument]
    bars, summary = data.load_bars(Path(d["path"]), instrument, d["sha256"])
    dev, hold = data.pinned_split(data.session_dates(bars, instrument), d["split"]["dev_end"], d["split"]["holdout_end"])
    calendar.check_covers(dev + hold, instrument)
    return bars, dev, hold, summary


def main(argv: list[str]) -> int:
    s = spec(Path(argv[0]))
    cs = load_cards(s)
    instruments = sorted({c.instrument for c in cs})
    cost = costs(s, instruments)
    book = None if s["book"] is None else data.load_book(Path(s["book"]["path"]), s["book"]["sha256"])
    cal = data.load_calendar(Path(s["calendar"]["path"]), s["calendar"]["sha256"])
    out = Path(s["out"])
    (out / "verdict.json").unlink(missing_ok=True)  # no completion marker survives an interrupted rerun
    ledger.append_cards(Path(s["ledger"]), s["run_id"], cs)  # before any bar is read
    loaded = {}
    for i in instruments:
        bars, dev, _, summary = load_data(s, i, cal)
        if book is not None and len(set(dev) & set(book)) < s["book"]["min_overlap"]:
            raise data.BookError(f"book covers {len(set(dev) & set(book))} {i} development sessions; "
                                 f"min_overlap is {s['book']['min_overlap']}")
        loaded[i] = (bars, dev, summary)
    out.mkdir(parents=True, exist_ok=True)
    verdicts = []
    for c in cs:
        bars, dev, summary = loaded[c.instrument]
        rep = gates.evaluate(c, bars, dev, Path(s["ledger"]), cost[c.instrument], summary["sha256"], book,
                             closed=cal.closed, k_scope=s["k_scope"])
        rep.update(run_id=s["run_id"], roll=s["roll"], firm=s["firm"], data=summary,
                   split=s["data"][c.instrument]["split"], calendar_sha256=cal.sha256)
        body = json.dumps(rep, indent=1).encode("utf-8")
        (out / f"{c.id}.report.json").write_bytes(body)
        verdicts.append({"card": c.id, "card_sha256": c.sha256, "report_sha256": hashlib.sha256(body).hexdigest(),
                         "verdict": rep["verdict"],
                         "stopped_at": rep["stopped_at"], "book_s": rep["book"].get("book_s"),
                         "book_s_with_card": rep["book"].get("book_s_with_card")})
    (out / "verdict.json").write_text(json.dumps(verdicts, indent=1), encoding="utf-8")
    for v in verdicts:
        print(v)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
