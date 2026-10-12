"""Live 6J/MGC roll source and G4 gate (Q-SFCLEAR-2 pre-registration section 3 G4; OPEN-3/OPEN-11).

Calendar only: no price, bar or trade data. Stdlib only; imports no lab and no trust-domain module.

* ``build(first, last, compat=True)`` regenerates the bound replay roll list byte for byte from the same
  rule text (the lab header is carried here as data), so the live rule is proven equal to the replay
  route's (``COMPAT_SHA256``). ``forward()`` extends it by the same rule over the contracts that the
  pinned, operator-attended CME capture reproduces; selection past that horizon is refused.
* ``select_contract`` is the OPEN-3 per-leg selection object: the OPEN-11 contract of the session, which for
  6J and MGC switches exactly at the G4 window's 18:00 ET open (zero margin).
* ``g4_refusal`` and ``flatten_required`` are the entry/add gate and the carry check for 6J and MGC.
  MNQ and MYM are cash-settled and never G4-gated.

Sources load once and fail closed: the capture must match ``CAPTURE_SHA256`` and reproduce all 36 vectors,
and the compat build must hash to ``COMPAT_SHA256`` (so a changed D19 file also refuses).
"""
from __future__ import annotations

import calendar
import csv
import hashlib
import json
import re
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from functools import lru_cache
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
D19 = "ops/calendars/cme_holiday_calendar_2022_2026.json"
CAPTURE = "ops/calendars/roll_sources/cme_calendar_capture_20261012.tsv"
FORWARD = "ops/calendars/contract_roll_forward.json"
CAPTURE_SHA256 = "1afbcd9fe42b5237466837ed95e67a477ebb4a3b47812e8fc3b7fdc9e287efa6"
COMPAT_SHA256 = "72677d254045fd35ca3da7047c8b649f47d0ae283d3fc41a402467de8de4134c"
COMPAT_WINDOW = (date(2022, 9, 1), date(2026, 9, 2))
# Header data only: the bound list names the lab copy of the (byte-identical) capture.
COMPAT_CAPTURE_PATH = "lab/analysis/c1/sfclear_2026-10/schedule/sources/cme_calendar_capture_20261012.tsv"
FORWARD_FIRST = date(2026, 9, 3)
CAPTURE_VECTORS = 36
YEARS = range(2020, 2031)
ET = ZoneInfo("America/New_York")

LEGS = {"aegis_6j": "6J", "dj30_mym_p250": "MYM", "vanguard_mgc": "MGC", "orb_mnq_v7": "MNQ"}
GROUP = {"MGC": "metals", "6J": "fx", "MYM": "equity_index", "MNQ": "equity_index"}
CYCLE = {"MGC": (2, 4, 6, 8, 12), "6J": (3, 6, 9, 12), "MYM": (3, 6, 9, 12), "MNQ": (3, 6, 9, 12)}
LISTED = {"MGC": (2, 4, 6, 8, 10, 12), "6J": tuple(range(1, 13))}
G4_PRODUCTS = ("6J", "MGC")
MONTH_CODES = "FGHJKMNQUVXZ"

RULES = (
    "B1 business day (roll dates and seams only; G0 unchanged): a weekday that is not a US federal holiday "
    "(5 U.S.C. 6103, Juneteenth from 2021; observed Saturday->Friday and Sunday->Monday, except that a Saturday "
    "New Year's Day is not observed on the Friday before), not Good Friday (Gregorian Easter - 2 days) and not a "
    "D19 FULL_CLOSURE for the product's group (MGC metals, 6J fx, MYM equity_index)",
    "C1 MGC (even months): first notice = last business day of the month before the contract month; "
    "last trade = third-last business day of the contract month",
    "C2 6J (quarterly and serial months; no first notice): last trade = second business day before the "
    "third Wednesday of the contract month",
    "C3 contracts listed: every one whose G4 window intersects the replay window",
    "G4 window: from the start (18:00 ET open of its session) of the business day before min(first notice, "
    "last trade), through last trade",
    "S1 seams (OPEN-11, feed-equivalence spec 16.2/16.4): the panel switches to the next contract of its cycle "
    "at the 18:00 ET open of the session whose CME trade date is the switch date (opens the previous calendar day)",
    "S2 6J: cycle Mar/Jun/Sep/Dec; switch date = 1 business day before last trade",
    "S3 MGC: cycle Feb/Apr/Jun/Aug/Dec (October never selected); switch date = 1 business day before first notice",
    "S4 MYM: cycle Mar/Jun/Sep/Dec; last trading day = the 3rd Friday of the contract month (CME contract "
    "specification, 'Trading terminates at 9:30 a.m. ET on the 3rd Friday of the contract month', as recorded in "
    "docs/spec/2026-09-27-cme-execution-feed-equivalence-test-DRAFT.md 16.2, read 2026-10-04; applied as written, "
    "with no holiday adjustment); switch date = 3 business days before it",
    "S5 seams listed: every switch whose trade date lies in the replay window",
)
COMPAT_PURPOSE = ("Q-SFCLEAR-2 G4 roll-date list for the replay window; calendar only (no price, bar or trade "
                  "data)")
COMPAT_RESIDUALS = (
    "rule-generated dates (Joshua 2026-10-12); the capture covers listed 2026-2028 contracts only, so "
    "historical contracts rest on the same rule",
    "D19 is secondary provenance (date membership only); capture rows after its coverage end use the "
    "federal and Good Friday rules alone",
    "no capture vector falls on Columbus Day, Veterans Day or Juneteenth; in the window Juneteenth moves "
    "the June 2023 6J last trade and seam and the June 2024 and June 2025 MYM seams (D19 has CME open, "
    "early close, on each Juneteenth, so a CME-open-day count would put those seams one session later)",
    "seams follow OPEN-11 by rule; the canonical panels' switch evidence is matched by name, not by hash",
    "MYM June 2026: the 3rd Friday (2026-06-19) is Juneteenth, not a B1 business day (D19: CME open, early "
    "close); S4 applies the cited rule as written, and the switch (2026-06-16) is the same under B1 and "
    "under CME-open-day counting; a holiday-adjusted last trading day would move it to 2026-06-15",
)
FORWARD_RULES = RULES[:3] + (
    "C3 forward: every 6J and MGC contract whose G4 window starts on or after the window's first day and whose "
    "first notice and last trade a capture vector reproduces",
) + RULES[4:8] + (
    "S5 forward: one seam per on-cycle contract listed (its to_month may lie past the horizon, where "
    "selection refuses)",
    "OPEN-3 live selection: the live contract of a session is the S1-S4 contract (MNQ as MYM, N = 3); "
    "6J and MGC entries and adds are refused inside a G4 window, for a contract that is not the selected one, "
    "for continuous or missing contracts, and from the refuse_from trade date of the horizon",
)


class RollSourceError(ValueError):
    """The roll sources are not the pinned bytes or do not reproduce the bound rule."""


class RollHorizonExceeded(ValueError):
    """The date or contract lies outside the capture-verified horizon."""


# Business days (B1) -------------------------------------------------------------------------------
def easter(y):
    a, b, c = y % 19, y // 100, y % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    return date(y, (h + l - 7 * m + 114) // 31, (h + l - 7 * m + 114) % 31 + 1)


def _nth(y, m, wd, n):
    d = date(y, m, 1)
    return d + timedelta((wd - d.weekday()) % 7 + 7 * (n - 1))


def _last(y, m, wd):
    d = date(y, m, calendar.monthrange(y, m)[1])
    return d - timedelta((d.weekday() - wd) % 7)


def _observed(d):
    return d - timedelta(1) if d.weekday() == 5 else d + timedelta(1) if d.weekday() == 6 else d


def federal_holidays(y):
    ny = date(y, 1, 1)
    days = {_nth(y, 1, 0, 3), _nth(y, 2, 0, 3), _last(y, 5, 0), _observed(date(y, 7, 4)), _nth(y, 9, 0, 1),
            _nth(y, 10, 0, 2), _observed(date(y, 11, 11)), _nth(y, 11, 3, 4), _observed(date(y, 12, 25))}
    if y >= 2021:   # Juneteenth
        days.add(_observed(date(y, 6, 19)))
    if ny.weekday() != 5:   # a Saturday New Year's Day is not observed on the Friday before
        days.add(_observed(ny))
    return days


class Calendar:
    def __init__(self, d19):
        groups = set(GROUP.values())
        self.closed = set()
        for y in YEARS:
            self.closed |= {(g, d) for g in groups for d in federal_holidays(y) | {easter(y) - timedelta(2)}}
        for e in d19["entries"]:
            for g in groups:
                if e[f"{g}_status"] == "FULL_CLOSURE":
                    self.closed.add((g, date.fromisoformat(e["date"])))

    def is_bd(self, d, product):
        return d.weekday() < 5 and (GROUP[product], d) not in self.closed

    def prev_bd(self, d, product, n):
        while n:
            d -= timedelta(1)
            n -= self.is_bd(d, product)
        return d

    def last_bd(self, y, m, product, k):
        """k-th last business day of month (y, m)."""
        return self.prev_bd(date(y, m, calendar.monthrange(y, m)[1]) + timedelta(1), product, k)


# Contract rules (C1, C2, S2-S4, G4) -----------------------------------------------------------------
def _prev_month(y, m):
    return (y, m - 1) if m > 1 else (y - 1, 12)


def mgc_first_notice(cal, y, m):
    return cal.last_bd(*_prev_month(y, m), "MGC", 1)


def mgc_last_trade(cal, y, m):
    return cal.last_bd(y, m, "MGC", 3)


def j6_last_trade(cal, y, m):
    return cal.prev_bd(_nth(y, m, 2, 3), "6J", 2)


def contract_dates(cal, product, y, m):
    """first_notice, last_trade, g4_start (6J/MGC) and switch (on-cycle contracts) under the bound rules."""
    fn = mgc_first_notice(cal, y, m) if product == "MGC" else None
    lt = {"MGC": mgc_last_trade, "6J": j6_last_trade}.get(product, lambda _c, yy, mm: _nth(yy, mm, 4, 3))(cal, y, m)
    out = {"first_notice": fn, "last_trade": lt, "g4_start": None, "switch": None}
    if product in G4_PRODUCTS:
        out["g4_start"] = cal.prev_bd(min(lt, fn or lt), product, 1)
    if m in CYCLE[product]:
        out["switch"] = cal.prev_bd(fn if product == "MGC" else lt, product, 3 if product in ("MYM", "MNQ") else 1)
    return out


def _open(trade_date):
    local = datetime.combine(trade_date - timedelta(1), time(18), ET)
    return local.isoformat(), local.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _open_utc(trade_date):
    return datetime.combine(trade_date - timedelta(1), time(18), ET).astimezone(timezone.utc)


def _next_in_cycle(product, y, m):
    nxt = [mm for mm in CYCLE[product] if mm > m]
    return (y, nxt[0]) if nxt else (y + 1, CYCLE[product][0])


# Sources ------------------------------------------------------------------------------------------
def capture_rows(text):
    return list(csv.DictReader((l for l in text.splitlines() if not l.startswith("#")), delimiter="\t"))


def _check_capture(cal, rows):
    n = bad = 0
    for r in rows:
        y, m = map(int, r["month"].split("-"))
        d = contract_dates(cal, r["product"], y, m)
        got = {"last_trade": d["last_trade"]}
        if r["product"] == "MGC":
            got["first_notice"] = d["first_notice"]
        for k, v in got.items():
            n += 1
            bad += v.isoformat() != r[k]
    return n, bad


@dataclass(frozen=True)
class Sources:
    calendar: Calendar
    d19_src: dict
    capture_src: dict
    capture: tuple
    vectors_checked: int
    vectors_bad: int
    horizon: dict        # product -> last capture-confirmed (year, month)
    refuse_from: dict    # product -> first trade date whose selection needs an unconfirmed contract


def load_sources(d19_path=None, capture_path=None):
    d19_path, capture_path = Path(d19_path or ROOT / D19), Path(capture_path or ROOT / CAPTURE)
    d19_raw, cap_raw = d19_path.read_bytes(), capture_path.read_bytes()
    cap_sha = hashlib.sha256(cap_raw).hexdigest()
    if cap_sha != CAPTURE_SHA256:
        raise RollSourceError(f"capture sha256 {cap_sha} is not the pinned {CAPTURE_SHA256}")
    cal = Calendar(json.loads(d19_raw))
    rows = tuple(capture_rows(cap_raw.decode("utf-8")))
    n, bad = _check_capture(cal, rows)
    if n != CAPTURE_VECTORS or bad:
        raise RollSourceError(f"capture check failed: {bad} of {n} vectors mismatch")
    horizon, refuse_from = {}, {}
    for product in G4_PRODUCTS:
        months = sorted(tuple(map(int, r["month"].split("-"))) for r in rows if r["product"] == product)
        horizon[product] = months[-1]
        y, m = max(ym for ym in months if ym[1] in CYCLE[product])
        refuse_from[product] = contract_dates(cal, product, y, m)["switch"]
    return Sources(cal, {"path": D19, "sha256": hashlib.sha256(d19_raw).hexdigest()},
                   {"path": CAPTURE, "sha256": cap_sha}, rows, n, bad, horizon, refuse_from)


@lru_cache(maxsize=1)
def _sources():
    src = load_sources()
    digest = hashlib.sha256(_build(src, *COMPAT_WINDOW, compat=True)).hexdigest()
    if digest != COMPAT_SHA256:
        raise RollSourceError(f"compat build {digest} is not the bound list {COMPAT_SHA256}")
    return src


# Artifacts ----------------------------------------------------------------------------------------
def _dumps(o):
    return json.dumps(o, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _contract_row(cal, product, y, m):
    d = contract_dates(cal, product, y, m)
    row = {"product": product, "contract_month": f"{y:04d}-{m:02d}", "on_seam_cycle": m in CYCLE[product]}
    if d["first_notice"]:
        row["first_notice"] = d["first_notice"].isoformat()
    row["last_trade"] = d["last_trade"].isoformat()
    row["g4_start_trade_date"] = d["g4_start"].isoformat()
    row["g4_start_open_local"], row["g4_start_open_utc"] = _open(d["g4_start"])
    return row, d


def _seam_row(cal, product, y, m):
    d = contract_dates(cal, product, y, m)
    ref_name = "first_notice" if product == "MGC" else "last_trade"
    ny, nm = _next_in_cycle(product, y, m)
    seam = {"product": product, "from_month": f"{y:04d}-{m:02d}", "to_month": f"{ny:04d}-{nm:02d}",
            ref_name: d[ref_name].isoformat(), "switch_trade_date": d["switch"].isoformat()}
    seam["switch_open_local"], seam["switch_open_utc"] = _open(d["switch"])
    return seam, d["switch"]


def _render(header, contracts, seams):
    contracts.sort(key=lambda r: (r["product"], r["contract_month"]))
    seams.sort(key=lambda r: (r["product"], r["from_month"]))
    text = ('{"header":' + _dumps(header) + ',\n"contracts":[\n' + ",\n".join(_dumps(r) for r in contracts)
            + '\n],\n"seams":[\n' + ",\n".join(_dumps(r) for r in seams) + "\n]}\n")
    json.loads(text)
    return text.encode("ascii")


def _build(src, first, last, *, compat):
    cal = src.calendar
    contracts, seams = [], []
    if compat:
        d19 = json.loads((ROOT / D19).read_bytes())
        if not (date.fromisoformat(d19["coverage_start"]) <= first - timedelta(60)
                and last + timedelta(60) <= date.fromisoformat(d19["coverage_end"])):
            raise RollSourceError("D19 coverage does not span the window")
        for y in range(first.year, last.year + 2):
            for m in range(1, 13):
                for product in ("MGC", "6J"):
                    if m not in LISTED[product]:
                        continue
                    row, d = _contract_row(cal, product, y, m)
                    if d["g4_start"] <= last and d["last_trade"] >= first:
                        contracts.append(row)
                for product in ("6J", "MGC", "MYM"):
                    if m in CYCLE[product]:
                        seam, switch = _seam_row(cal, product, y, m)
                        if first <= switch <= last:
                            seams.append(seam)
        header = {
            "schema": "sfclear_roll_dates/v1", "purpose": COMPAT_PURPOSE,
            "window": [first.isoformat(), last.isoformat()],
            "day_basis": "CME trade date; its session opens 18:00 ET on the previous calendar day",
            "rules": list(RULES),
            "sources": [src.d19_src, {"path": COMPAT_CAPTURE_PATH, "sha256": src.capture_src["sha256"]}],
            "capture_vectors": {"checked": src.vectors_checked, "mismatches": src.vectors_bad},
            "residuals": list(COMPAT_RESIDUALS),
            "counts": {"contracts": len(contracts), "seams": len(seams)},
        }
        return _render(header, contracts, seams)
    captured = {(r["product"], r["month"]) for r in src.capture}
    excluded = []
    for y in range(first.year, last.year + 1):
        for m in range(1, 13):
            for product in G4_PRODUCTS:
                if m not in LISTED[product] or (y, m) > src.horizon[product]:
                    continue
                row, d = _contract_row(cal, product, y, m)
                if not first <= d["g4_start"] <= last:
                    continue
                if (product, row["contract_month"]) not in captured:
                    excluded.append(f"{product} {row['contract_month']}")
                    continue
                contracts.append(row)
                if row["on_seam_cycle"]:
                    seams.append(_seam_row(cal, product, y, m)[0])
    header = {
        "schema": "contract_roll_forward/v1",
        "purpose": ("live G4 roll source, forward rows (ops/c1_rail/contract_roll.py): the bound replay list's "
                    "rule extended over the contracts the pinned CME capture reproduces; calendar only"),
        "window": [first.isoformat(), last.isoformat()],
        "day_basis": "CME trade date; its session opens 18:00 ET on the previous calendar day",
        "rules": list(FORWARD_RULES),
        "sources": [src.d19_src, src.capture_src],
        "capture_vectors": {"checked": src.vectors_checked, "mismatches": src.vectors_bad},
        "compat_sha256": COMPAT_SHA256,
        "compat_window": [d.isoformat() for d in COMPAT_WINDOW],
        "horizon": {p: {"last_contract": f"{src.horizon[p][0]:04d}-{src.horizon[p][1]:02d}",
                        "refuse_from_trade_date": src.refuse_from[p].isoformat()} for p in G4_PRODUCTS},
        "excluded_uncaptured": excluded,
        "refresh": ("bind a new operator-attended CME calendar capture under ops/calendars/roll_sources/ with its "
                    "sha256 pinned in contract_roll.py, then run scripts/author_contract_roll.py --forward; "
                    "--forward --check compares bytes"),
        "residuals": [
            "D19 covers 2022-01-01..2026-12-31; later business days use the federal and Good Friday rules alone",
            "excluded_uncaptured contracts rest on the rule only (no capture vector) and are not listed here",
            "MNQ and MYM are selected by rule with no capture horizon; they are cash-settled and never G4-gated",
        ],
        "counts": {"contracts": len(contracts), "seams": len(seams)},
    }
    return _render(header, contracts, seams)


def build(first, last, *, compat=False):
    """compat=True: the bound list's algorithm and header; otherwise capture-confirmed 6J/MGC rows."""
    return _build(_sources() if not compat else load_sources(), first, last, compat=compat)


def forward():
    src = _sources()
    last = max(date(y, m, 28) for y, m in src.horizon.values())
    return _build(src, FORWARD_FIRST, last, compat=False)


# Live selection and gate (OPEN-3) ---------------------------------------------------------------------
@dataclass(frozen=True)
class ContractRef:
    leg_id: str
    product: str
    contract_month: str
    code: str
    first_notice: date | None
    last_trade: date
    g4_start_trade_date: date | None
    g4_start_open_utc: datetime | None
    switch_trade_date: date | None
    switch_open_utc: datetime | None


def _product(leg_id):
    if leg_id not in LEGS:
        raise ValueError(f"unknown leg {leg_id!r}")
    return LEGS[leg_id]


def _ref(leg_id, product, y, m):
    d = contract_dates(_sources().calendar, product, y, m)
    return ContractRef(leg_id, product, f"{y:04d}-{m:02d}", f"{product}{MONTH_CODES[m - 1]}{y % 100:02d}",
                       d["first_notice"], d["last_trade"], d["g4_start"],
                       d["g4_start"] and _open_utc(d["g4_start"]), d["switch"],
                       d["switch"] and _open_utc(d["switch"]))


def trade_date_of(now):
    """CME trade date of an aware instant: the session opening 18:00 ET belongs to the next calendar day."""
    if not isinstance(now, datetime) or now.utcoffset() is None:
        raise ValueError("now must be a timezone-aware datetime")
    return (now.astimezone(ET) + timedelta(hours=6)).date()


def select_contract(leg_id, trade_date) -> ContractRef:
    """OPEN-3: the leg's live dated contract for a CME trade date (the OPEN-11 contract of that session)."""
    product = _product(leg_id)
    if isinstance(trade_date, datetime) or not isinstance(trade_date, date):
        raise ValueError("trade_date must be a date")
    src = _sources()
    if trade_date < COMPAT_WINDOW[0] or trade_date.year >= YEARS.stop - 1:
        raise RollHorizonExceeded(f"{trade_date} is outside the verified range")
    if product in G4_PRODUCTS and trade_date >= src.refuse_from[product]:
        raise RollHorizonExceeded(f"{product} selection on {trade_date} needs a contract past the capture horizon")
    y, m = trade_date.year, trade_date.month
    while True:
        if m in CYCLE[product] and contract_dates(src.calendar, product, y, m)["switch"] > trade_date:
            return _ref(leg_id, product, y, m)
        y, m = (y, m + 1) if m < 12 else (y + 1, 1)


def _parse(product, contract):
    code = contract.code if isinstance(contract, ContractRef) else contract
    match = isinstance(code, str) and re.fullmatch(re.escape(product) + r"([FGHJKMNQUVXZ])(\d{2})", code)
    return (2000 + int(match[2]), MONTH_CODES.index(match[1]) + 1) if match else None


def _verdict(leg_id, contract, now):
    """None when admissible, else the refusal reason (6J/MGC only)."""
    product = _product(leg_id)
    trade_date = trade_date_of(now)
    if product not in G4_PRODUCTS:
        return None
    parsed = _parse(product, contract)
    if parsed is None:
        return "contract_unbound"
    if parsed > _sources().horizon[product] or parsed[0] < COMPAT_WINDOW[0].year - 1:
        return "roll_horizon_exceeded"
    try:
        selected = select_contract(leg_id, trade_date)
    except RollHorizonExceeded:
        return "roll_horizon_exceeded"
    if parsed[1] not in LISTED[product]:
        return "contract_not_selected"
    if now >= _ref(leg_id, product, *parsed).g4_start_open_utc:
        return "g4_window"
    return None if selected.code == f"{product}{MONTH_CODES[parsed[1] - 1]}{parsed[0] % 100:02d}" \
        else "contract_not_selected"


def g4_refusal(leg_id, contract, now) -> str | None:
    """Entry/add gate: None, or g4_window | contract_not_selected | contract_unbound | roll_horizon_exceeded.

    ``contract`` is the dated contract the route will send (a ``ContractRef`` or a code such as ``6JZ26``);
    continuous notation such as ``6J1!`` is unbound. Exits, flats and cancels are never refused.
    """
    return _verdict(leg_id, contract, now)


def flatten_required(leg_id, contract, now) -> bool:
    """True when a 6J/MGC position in ``contract`` must be flat: at or after its window start, or not selected."""
    return _verdict(leg_id, contract, now) is not None


def contract_ref(leg_id, code) -> ContractRef:
    """The rule dates of a listed, capture-horizon dated contract code for a leg."""
    product = _product(leg_id)
    parsed = _parse(product, code)
    if parsed is None or (product in LISTED and parsed[1] not in LISTED[product]):
        raise ValueError(f"{code!r} is not a listed {product} contract")
    if product in G4_PRODUCTS and parsed > _sources().horizon[product]:
        raise RollHorizonExceeded(f"{code} is past the capture horizon")
    return _ref(leg_id, product, *parsed)
