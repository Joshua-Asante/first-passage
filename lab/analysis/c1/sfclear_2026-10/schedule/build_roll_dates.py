"""Q-SFCLEAR-2 G4 roll-date list (pre-registration §3 G4; build card v3 §3): calendar only, no prices.

Generates by rule the 6J and MGC contract dates (first notice, last trade, G4 window start) and the
6J, MGC and MYM panel roll seams (feed-equivalence spec OPEN-11), and regenerates every row of the
2026-10-12 CME calendar capture as a test vector; any mismatch fails the build.

Run: python -I scripts/fp.py python lab/analysis/c1/sfclear_2026-10/schedule/build_roll_dates.py [--check]
"""
import argparse
import calendar
import csv
import hashlib
import json
import sys
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[5]
D19 = "ops/calendars/cme_holiday_calendar_2022_2026.json"
CAPTURE = "lab/analysis/c1/sfclear_2026-10/schedule/sources/cme_calendar_capture_20261012.tsv"
CAPTURE_SHA256 = "1afbcd9fe42b5237466837ed95e67a477ebb4a3b47812e8fc3b7fdc9e287efa6"
OUT = Path(__file__).parent / "roll_dates_6J_MGC_2022-09-01_2026-09-02.json"
FIRST, LAST = date(2022, 9, 1), date(2026, 9, 2)
ET = ZoneInfo("America/New_York")
GROUP = {"MGC": "metals", "6J": "fx", "MYM": "equity_index"}
SEAM_MONTHS = {"MGC": (2, 4, 6, 8, 12), "6J": (3, 6, 9, 12), "MYM": (3, 6, 9, 12)}
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


def federal_holidays(y, juneteenth=True):
    ny = date(y, 1, 1)
    days = {_nth(y, 1, 0, 3), _nth(y, 2, 0, 3), _last(y, 5, 0), _observed(date(y, 7, 4)), _nth(y, 9, 0, 1),
            _nth(y, 10, 0, 2), _observed(date(y, 11, 11)), _nth(y, 11, 3, 4), _observed(date(y, 12, 25))}
    if ny.weekday() != 5:   # a Saturday New Year's Day is not observed on the Friday before
        days.add(_observed(ny))
    if juneteenth and y >= 2021:
        days.add(_observed(date(y, 6, 19)))
    return days


class Calendar:
    def __init__(self, d19, federal=True, good_friday=True, juneteenth=True, years=range(2020, 2031)):
        self.closed = set()
        for y in years:
            if federal:
                self.closed |= {(g, d) for g in GROUP.values() for d in federal_holidays(y, juneteenth)}
            if good_friday:
                self.closed |= {(g, easter(y) - timedelta(2)) for g in GROUP.values()}
        for e in d19["entries"]:
            for g in GROUP.values():
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


def _prev_month(y, m):
    return (y, m - 1) if m > 1 else (y - 1, 12)


def mgc_first_notice(cal, y, m, k_last=1):
    return cal.last_bd(*_prev_month(y, m), "MGC", k_last)


def mgc_last_trade(cal, y, m):
    return cal.last_bd(y, m, "MGC", 3)


def j6_last_trade(cal, y, m, before=2):
    return cal.prev_bd(_nth(y, m, 2, 3), "6J", before)


def mym_last_trade(cal, y, m):
    return _nth(y, m, 4, 3)   # calendar rule as cited (S4); B1 is used only to count back from it


def _open(trade_date):
    local = datetime.combine(trade_date - timedelta(1), time(18), ET)
    return local.isoformat(), local.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _next_in_cycle(product, y, m):
    months = SEAM_MONTHS[product]
    nxt = [mm for mm in months if mm > m]
    return (y, nxt[0]) if nxt else (y + 1, months[0])


def _read(rel):
    raw = (ROOT / rel).read_bytes()
    return raw, {"path": rel, "sha256": hashlib.sha256(raw).hexdigest()}


def check_capture(cal, text):
    n = bad = 0
    rows = csv.DictReader((l for l in text.splitlines() if not l.startswith("#")), delimiter="\t")
    for r in rows:
        y, m = map(int, r["month"].split("-"))
        got = ({"first_notice": mgc_first_notice(cal, y, m), "last_trade": mgc_last_trade(cal, y, m)}
               if r["product"] == "MGC" else {"last_trade": j6_last_trade(cal, y, m)})
        for k, v in got.items():
            n += 1
            if v.isoformat() != r[k]:
                bad += 1
                print(f"MISMATCH {r['code']} {k}: rule {v} capture {r[k]}", file=sys.stderr)
    return n, bad


def build():
    d19_raw, d19_src = _read(D19)
    cap_raw, cap_src = _read(CAPTURE)
    if cap_src["sha256"] != CAPTURE_SHA256:
        raise SystemExit("capture bytes differ from the bound sha256")
    d19 = json.loads(d19_raw)
    if not (date.fromisoformat(d19["coverage_start"]) <= FIRST - timedelta(60)
            and LAST + timedelta(60) <= date.fromisoformat(d19["coverage_end"])):
        raise SystemExit("D19 coverage does not span the window")
    cal = Calendar(d19)
    n, bad = check_capture(cal, cap_raw.decode("utf-8"))
    if n != 36 or bad:
        raise SystemExit(f"capture check failed: {bad} of {n} vectors mismatch")
    contracts, seams = [], []
    for y in range(FIRST.year, LAST.year + 2):
        for m in range(1, 13):
            for product in ("MGC", "6J"):
                if product == "MGC" and m % 2:
                    continue
                row = {"product": product, "contract_month": f"{y:04d}-{m:02d}",
                       "on_seam_cycle": m in SEAM_MONTHS[product]}
                if product == "MGC":
                    fn, lt = mgc_first_notice(cal, y, m), mgc_last_trade(cal, y, m)
                    row["first_notice"] = fn.isoformat()
                else:
                    fn, lt = None, j6_last_trade(cal, y, m)
                start = cal.prev_bd(min(lt, fn or lt), product, 1)
                if start > LAST or lt < FIRST:
                    continue
                row["last_trade"] = lt.isoformat()
                row["g4_start_trade_date"] = start.isoformat()
                row["g4_start_open_local"], row["g4_start_open_utc"] = _open(start)
                contracts.append(row)
            for product in ("6J", "MGC", "MYM"):
                if m not in SEAM_MONTHS[product]:
                    continue
                if product == "MGC":
                    ref_name, ref = "first_notice", mgc_first_notice(cal, y, m)
                    switch = cal.prev_bd(ref, product, 1)
                elif product == "6J":
                    ref_name, ref = "last_trade", j6_last_trade(cal, y, m)
                    switch = cal.prev_bd(ref, product, 1)
                else:
                    ref_name, ref = "last_trade", mym_last_trade(cal, y, m)
                    switch = cal.prev_bd(ref, product, 3)
                if not FIRST <= switch <= LAST:
                    continue
                ny, nm = _next_in_cycle(product, y, m)
                seam = {"product": product, "from_month": f"{y:04d}-{m:02d}", "to_month": f"{ny:04d}-{nm:02d}",
                        ref_name: ref.isoformat(), "switch_trade_date": switch.isoformat()}
                seam["switch_open_local"], seam["switch_open_utc"] = _open(switch)
                seams.append(seam)
    contracts.sort(key=lambda r: (r["product"], r["contract_month"]))
    seams.sort(key=lambda r: (r["product"], r["from_month"]))
    header = {
        "schema": "sfclear_roll_dates/v1",
        "purpose": "Q-SFCLEAR-2 G4 roll-date list for the replay window; calendar only (no price, bar or trade data)",
        "window": [FIRST.isoformat(), LAST.isoformat()],
        "day_basis": "CME trade date; its session opens 18:00 ET on the previous calendar day",
        "rules": list(RULES),
        "sources": [d19_src, cap_src],
        "capture_vectors": {"checked": n, "mismatches": bad},
        "residuals": [
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
        ],
        "counts": {"contracts": len(contracts), "seams": len(seams)},
    }
    dumps = lambda o: json.dumps(o, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    text = ('{"header":' + dumps(header) + ',\n"contracts":[\n' + ",\n".join(dumps(r) for r in contracts)
            + '\n],\n"seams":[\n' + ",\n".join(dumps(r) for r in seams) + "\n]}\n")
    json.loads(text)
    return text.encode("ascii")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="compare with the committed file; write nothing")
    args = ap.parse_args(argv)
    data = build()
    digest = hashlib.sha256(data).hexdigest()
    if args.check:
        same = OUT.is_file() and OUT.read_bytes() == data
        print(f"{digest}  {'MATCH' if same else 'DIFFERS'}")
        return 0 if same else 1
    OUT.write_bytes(data)
    print(f"{digest}  {OUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
