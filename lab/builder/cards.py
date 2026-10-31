"""Declarative YAML cards built from the ORB v1 block library only (spec: Card schema).

A card names one option per block; every numeric knob lives in ``params`` with its value and
grid step, which the plateau gate uses. Anything outside the library is rejected, so a card
cannot express lookahead: the compiler reads closed bars only.

    id: mcl-orb-001
    family: orb
    instrument: MCL
    bar: 15m
    session: day
    entry: {type: breakout, range: first_n_bars, side: both, order: stop}
    exit: {stop: range_opposite, target: none, flat_at: "14:30"}
    time: {entry_cutoff: "12:00"}          # optional; defaults to flat_at
    filters: [min_range_atr]               # optional; day_of_week also needs `days: [0..4]`
    params: {n_bars: {value: 2, step: 1}, min_range_atr: {value: 0.5, step: 0.25}}
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, replace

import yaml

from builder.instruments import DAY_END, INSTRUMENTS, minutes

RANGE = {"first_n_bars": ("n_bars",), "time_window": ("offset_bars", "n_bars")}
STOP = {"range_opposite": (), "atr_multiple": ("stop_atr",), "fixed_ticks": ("stop_ticks",)}
TARGET = {"none": (), "r_multiple": ("target_r",), "atr_multiple": ("target_atr",)}
FILTERS = {"day_of_week": (), "min_range_atr": ("min_range_atr",), "max_trades_per_day": ("max_trades_per_day",)}
SIDES = ("long", "short", "both")
INT_PARAMS = {"n_bars": 1, "offset_bars": 0, "stop_ticks": 1, "max_trades_per_day": 1}  # name -> minimum
FLOAT_MIN = {"stop_atr": 0.0, "target_r": 0.0, "target_atr": 0.0, "min_range_atr": 0.0}  # exclusive, except min_range_atr
TOP_KEYS = {"id", "family", "instrument", "bar", "session", "entry", "exit", "time", "filters", "days", "params"}
HHMM = re.compile(r"^([01]\d|2[0-3]):[0-5]\d$")
CARD_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")  # also the report file name


class CardError(ValueError):
    pass


@dataclass(frozen=True)
class Card:
    id: str
    family: str
    instrument: str
    range: str
    side: str
    stop: str
    target: str
    flat_at: str
    entry_cutoff: str
    filters: tuple[str, ...]
    days: tuple[int, ...]
    params: tuple[tuple[str, float, float], ...]  # (name, value, step), sorted by name
    source: str
    sha256: str

    def p(self, name: str, default=None):
        for n, v, _ in self.params:
            if n == name:
                return v
        return default

    def range_end(self) -> str:
        """HH:MM at which the range closes and entries go live."""
        m = minutes(INSTRUMENTS[self.instrument].session_open) + 15 * (int(self.p("offset_bars", 0)) + int(self.p("n_bars")))
        return f"{m // 60:02d}:{m % 60:02d}"

    def neighbours(self) -> list[tuple[str, int, "Card | None"]]:
        """Cards one grid step either side on each parameter; None where the value or the
        resulting timing is invalid (the plateau gate names those as skipped)."""
        out = []
        for i, (n, v, s) in enumerate(self.params):
            for sign in (-1, 1):
                w = v + sign * s
                nb = None
                if _valid_value(n, w):
                    ps = list(self.params)
                    ps[i] = (n, int(w) if n in INT_PARAMS else round(w, 10), s)
                    nb = replace(self, params=tuple(ps), sha256="", source="")
                    if _timing_error(nb):
                        nb = None
                out.append((n, sign, nb))
        return out


def _timing_error(c: Card) -> str | None:
    """Range must close before the entry cutoff; cutoff <= flat_at <= the end of the trading day."""
    if minutes(c.range_end()) >= 24 * 60 or not c.range_end() < c.entry_cutoff <= c.flat_at <= DAY_END:
        return f"timing needs range_end {c.range_end()} < entry_cutoff {c.entry_cutoff} <= flat_at {c.flat_at} <= {DAY_END}"
    return None


def _valid_value(name: str, v: float) -> bool:
    if name in INT_PARAMS:
        return float(v).is_integer() and v >= INT_PARAMS[name]
    return v >= 0 if name == "min_range_atr" else v > FLOAT_MIN[name]


def _need(d: dict, key: str, ctx: str):
    if not isinstance(d, dict) or key not in d:
        raise CardError(f"{ctx}: missing '{key}'")
    return d[key]


def _hhmm(v, ctx: str) -> str:
    if not isinstance(v, str) or not HHMM.match(v):
        raise CardError(f"{ctx}: expected quoted HH:MM, got {v!r}")
    return v


def parse(text: str) -> Card:
    try:
        d = yaml.safe_load(text)
    except yaml.YAMLError as e:
        raise CardError(f"card is not valid YAML: {e}") from None
    if not isinstance(d, dict):
        raise CardError("card must be a mapping")
    extra = set(d) - TOP_KEYS
    if extra:
        raise CardError(f"unknown card keys {sorted(extra)}")
    cid = _need(d, "id", "card")
    if not isinstance(cid, str) or not CARD_ID.match(cid):
        raise CardError(f"card id must match {CARD_ID.pattern}, got {cid!r}")
    if _need(d, "family", "card") != "orb":
        raise CardError("v1 library has the orb family only")
    inst = _need(d, "instrument", "card")
    if inst not in INSTRUMENTS:
        raise CardError(f"instrument {inst!r} not in builder.instruments")
    if d.get("bar", "15m") != "15m" or d.get("session", "day") != "day":
        raise CardError("v1 supports bar: 15m and session: day only")
    entry, exit_ = _need(d, "entry", "card"), _need(d, "exit", "card")
    if _need(entry, "type", "entry") != "breakout" or entry.get("order", "stop") != "stop":
        raise CardError("entry must be type: breakout, order: stop")
    rng, side = _need(entry, "range", "entry"), _need(entry, "side", "entry")
    stop, target = _need(exit_, "stop", "exit"), _need(exit_, "target", "exit")
    if rng not in RANGE or side not in SIDES or stop not in STOP or target not in TARGET:
        raise CardError(f"block option outside the library: range={rng} side={side} stop={stop} target={target}")
    flat_at = _hhmm(_need(exit_, "flat_at", "exit"), "exit.flat_at")
    cutoff = _hhmm((d.get("time") or {}).get("entry_cutoff", flat_at), "time.entry_cutoff")
    if set(d.get("time") or {}) - {"entry_cutoff"}:
        raise CardError("time block takes entry_cutoff only (flat_at lives in exit)")
    filters = tuple(d.get("filters") or ())
    if any(f not in FILTERS for f in filters) or len(set(filters)) != len(filters):
        raise CardError(f"filters outside the library or repeated: {filters}")
    days = tuple(d.get("days") or ())
    if ("day_of_week" in filters) != bool(days) or any(x not in range(5) for x in days):
        raise CardError("day_of_week filter needs days: a list of weekday numbers 0-4, and only with that filter")
    need = set(RANGE[rng] + STOP[stop] + TARGET[target] + sum((FILTERS[f] for f in filters), ()))
    raw = d.get("params") or {}
    if set(raw) != need:
        raise CardError(f"params must be exactly {sorted(need)}, got {sorted(raw)}")
    params = []
    for n in sorted(raw):
        spec = raw[n]
        if not isinstance(spec, dict) or set(spec) != {"value", "step"}:
            raise CardError(f"param {n}: needs exactly value and step")
        v, s = spec["value"], spec["step"]
        if isinstance(v, bool) or isinstance(s, bool) or not all(isinstance(x, (int, float)) for x in (v, s)) or s <= 0:
            raise CardError(f"param {n}: numeric value and positive step required")
        if not _valid_value(n, v) or (n in INT_PARAMS and not float(s).is_integer()):
            raise CardError(f"param {n}: invalid value {v} or step {s}")
        params.append((n, int(v) if n in INT_PARAMS else float(v), int(s) if n in INT_PARAMS else float(s)))
    canon = json.dumps(d, sort_keys=True, separators=(",", ":"))
    card = Card(id=cid, family="orb", instrument=inst, range=rng, side=side, stop=stop,
                target=target, flat_at=flat_at, entry_cutoff=cutoff, filters=filters, days=days,
                params=tuple(params), source=text, sha256=hashlib.sha256(canon.encode()).hexdigest())
    err = _timing_error(card)
    if err:
        raise CardError(f"{card.id}: {err}")
    return card
