"""Q-SFCLEAR-2 historical session schedule (ruling (c), 2026-10-11): calendar only, no prices.

Reads three repo calendar sources as data and writes one canonical JSON schedule of the
2022-09-01..2026-09-02 weekdays with PERMITTED/DENIED flags and the G0 times (rules H1-H6 in RULES).

Run: python -I scripts/fp.py python lab/analysis/c1/sfclear_2026-10/build_historical_schedule.py [--check]
"""
import argparse
import hashlib
import json
import sys
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[4]
D19 = "ops/calendars/cme_holiday_calendar_2022_2026.json"
OVERLAY = "ops/calendars/book_closure_overlay.json"
RULE = "ops/calendars/book_session_calendar_2026-10.json"
OUT = Path(__file__).parent / "schedule" / "historical_schedule_2022-09-01_2026-09-02.json"
FIRST, LAST = date(2022, 9, 1), date(2026, 9, 2)
ET = ZoneInfo("America/New_York")
GROUPS = ("equity_index", "metals", "fx")
RULES = (
    "H1 universe: every Monday-Friday account date in the window (account date = CME trade date; "
    "the session opens 18:00 ET on the previous calendar day)",
    "H2 DENIED OVERLAY_CLOSURE: date in book_closure_overlay.json (the whole session is blocked)",
    "H3 DENIED HOLIDAY: any D19 product group FULL_CLOSURE on that trade date",
    "H4 DENIED SHORTENED: any D19 product group EARLY_CLOSE (first_release_policy denies HOLIDAY and SHORTENED)",
    "H5 PERMITTED otherwise, including a D19 row whose three groups are NORMAL; the first-release evidence "
    "classes UNCERTAIN_ADJACENT and MISSING_SOURCE are not applied (D19 is date membership only and qualifies "
    "no session), so this schedule permits sessions the live first-release policy may deny",
    "H6 G0 on PERMITTED rows by the 2026-10 calendar schedule_rule (TB-S3 section 5): V = the four products' "
    "regular matching close, D = min(own_flat_cap, V - 15 min), cutoff = D - 15 min, flatten start = D - 5 min; "
    "DENIED rows carry no executable times",
)


def _read(rel):
    raw = (ROOT / rel).read_bytes()
    return json.loads(raw), {"path": rel, "sha256": hashlib.sha256(raw).hexdigest()}


def _hm(text):
    return time.fromisoformat(text)


def _stamp(day, clock):
    local = datetime.combine(day, clock, ET)
    return local.isoformat(), local.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def build():
    d19, d19_src = _read(D19)
    overlay, overlay_src = _read(OVERLAY)
    cal, rule_src = _read(RULE)
    if overlay["d19_source"]["sha256"] != d19_src["sha256"]:
        raise SystemExit("overlay d19_source digest differs from the D19 bytes read")
    rule, policy = cal["schedule_rule"], cal["first_release_policy"]
    if not {"HOLIDAY", "SHORTENED"} <= set(policy["deny"]):
        raise SystemExit("first_release_policy no longer denies HOLIDAY and SHORTENED")
    closes = {p["regular_matching_close_local"] for p in cal["products"].values()}
    if len(closes) != 1:
        raise SystemExit("products disagree on the regular matching close")
    v = _hm(closes.pop())
    cap = _hm(rule["own_flat_cap_local"])
    own = min(datetime.combine(FIRST, cap), datetime.combine(FIRST, v) - timedelta(minutes=rule["own_flat_before_v_minutes"])).time()
    cutoff = (datetime.combine(FIRST, own) - timedelta(minutes=rule["cutoff_before_own_flat_minutes"])).time()
    flat_start = (datetime.combine(FIRST, own) - timedelta(minutes=rule["flatten_start_before_own_flat_minutes"])).time()
    entries = {e["date"]: e for e in d19["entries"]}
    blocked = {row["date"] for row in overlay["dates"]}
    if not (date.fromisoformat(d19["coverage_start"]) <= FIRST and LAST <= date.fromisoformat(d19["coverage_end"])):
        raise SystemExit("D19 coverage does not span the window")
    rows, counts = [], {}
    day = FIRST
    while day <= LAST:
        if day.weekday() < 5:
            key = day.isoformat()
            row = {"account_date": key}
            entry = entries.get(key)
            status = {g: entry[f"{g}_status"] for g in GROUPS} if entry else None
            if key in blocked:
                reason = "OVERLAY_CLOSURE"
            elif status and "FULL_CLOSURE" in status.values():
                reason = "HOLIDAY"
            elif status and "EARLY_CLOSE" in status.values():
                reason = "SHORTENED"
            else:
                reason = None
            if status:
                row["d19_status"] = status
            if reason:
                row.update(permission="DENIED", denial_reason=reason)
            else:
                row["permission"] = "PERMITTED"
                for name, d, clock in (("opens", day - timedelta(days=1), time(18)),
                                       ("risk_add_cutoff", day, cutoff),
                                       ("flatten_start", day, flat_start),
                                       ("own_flat_deadline", day, own)):
                    row[f"{name}_local"], row[f"{name}_utc"] = _stamp(d, clock)
            counts[reason or "PERMITTED"] = counts.get(reason or "PERMITTED", 0) + 1
            rows.append(row)
        day += timedelta(days=1)
    header = {
        "schema": "sfclear_historical_schedule/v1",
        "purpose": "Q-SFCLEAR-2 G0 schedule for the replay window; calendar only (no price, bar or trade data)",
        "window": [FIRST.isoformat(), LAST.isoformat()],
        "day_basis": "account date = CME trade date; session opens 18:00 ET on the previous calendar day",
        "rules": list(RULES),
        "g0_local": {"v": v.strftime("%H:%M"), "own_flat": own.strftime("%H:%M"),
                     "risk_add_cutoff": cutoff.strftime("%H:%M"), "flatten_start": flat_start.strftime("%H:%M")},
        "sources": [d19_src, overlay_src, rule_src],
        "residuals": [
            "D19 is secondary provenance accepted for date membership only (ops/calendars/README.md, D19)",
            "D19 records an unruled-out ad hoc closure interval 2026-05-28..2026-09-02 (not conservative)",
            "2025-11-28 Globex outage day is EARLY_CLOSE in D19 and is denied here either way",
        ],
        "counts": dict(sorted(counts.items())),
    }
    dumps = lambda o: json.dumps(o, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    text = '{"header":' + dumps(header) + ',\n"sessions":[\n' + ",\n".join(dumps(r) for r in rows) + "\n]}\n"
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
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(data)
    print(f"{digest}  {OUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
