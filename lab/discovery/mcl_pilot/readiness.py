"""MCL-1: phase-restricted input adapter and development-readiness preflight.

Spec rev 3 sections 2.1, 3, 3.1 and 8. Only the requested phase's bars are decoded: a row's
bar-open epoch (the Signal field's first token) is read first, and every out-of-phase
row is skipped before any price token is parsed. Replay has no entry point here.
The report holds counts, dates and timestamps only, never vendor prices.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import json
import math
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from bar_export_loader import SIGNAL_PIPE_V2_RE, price_tolerance

NY = ZoneInfo("America/New_York")
BAR_MS = 900_000
CLOCKS = ("09:45", "10:45", "11:45", "12:45", "13:45")
PHASES = {
    "calibration": (date(2022, 1, 3), date(2022, 12, 30)),
    "development": (date(2023, 1, 1), date(2025, 6, 30)),
}
DEV_BLOCKS = (("2023H1", date(2023, 1, 1), date(2023, 6, 30)), ("2023H2", date(2023, 7, 1), date(2023, 12, 31)),
              ("2024H1", date(2024, 1, 1), date(2024, 6, 30)), ("2024H2", date(2024, 7, 1), date(2024, 12, 31)),
              ("2025H1", date(2025, 1, 1), date(2025, 6, 30)))
MIN_BLOCK_SESSIONS = 20
EXPECTED_META = {"ticker": "MCL1!", "type": "futures", "quote_currency": "USD", "base_currency": "",
                 "mintick": 0.01, "pointvalue": 100.0, "timezone": "America/New_York", "timeframe": "15"}
PINNED = {  # repo-relative path -> SHA256 (spec rev 3, section 2.1)
    "docs/spec/2026-10-30-mcl-retain-mutate-pilot-rev3-DRAFT.md": "05ebd001cf86e72f4ba899caf40b0876359622a7178110014e94dfd8d186d312",
    "core/data/bar_data/MCL_M15.csv": "5aa504567b943ff68506b8b5c21df293c5a553543fdf1ac606adeb0f5bfbbd23",
    "core/data/tv_exports/cme/BAR_EXPORT_v0.2_NYMEX_MCL1_2026-08-13_3fd7c.csv":
        "5f44643c2d9ddab19885b35e81177d5614e99f96cc36fb08f359a9241889b37f",
}
SPEC, PANEL, RAW = PINNED


def _observed(d: date) -> date:
    return d - timedelta(1) if d.weekday() == 5 else d + timedelta(1) if d.weekday() == 6 else d


def _nth_weekday(y: int, m: int, wd: int, n: int) -> date:
    d = date(y, m, 1)
    return d + timedelta((wd - d.weekday()) % 7 + 7 * (n - 1))


def _last_monday(y: int, m: int) -> date:
    d = date(y, m + 1, 1) - timedelta(1)
    return d - timedelta(d.weekday())


def _easter(y: int) -> date:  # Gregorian (anonymous algorithm)
    a, (b, c) = y % 19, divmod(y, 100)
    d, e = divmod(b, 4)
    g = (b - (b + 8) // 25 + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mo, da = divmod(h + l - 7 * m + 114, 31)
    return date(y, mo, da + 1)


def calendar_excluded(year: int) -> set[date]:
    """Spec rev 3 section 3.1 set E for ``year`` (weekdays only), from civil rules, never bar presence."""
    tg = _nth_weekday(year, 11, 3, 4)
    days = {_observed(date(year, 1, 1)), _nth_weekday(year, 1, 0, 3), _nth_weekday(year, 2, 0, 3),
            _easter(year) - timedelta(2), _last_monday(year, 5), _observed(date(year, 6, 19)),
            _observed(date(year, 7, 4)), _nth_weekday(year, 9, 0, 1), tg, tg + timedelta(1),
            _observed(date(year, 12, 25)), date(year, 12, 24)}
    return {d for d in days if d.weekday() < 5 and d.year == year}


class InputError(ValueError):
    """Input defect that stops the phase (spec section 3 item 2)."""


@dataclass(frozen=True)
class Bar:
    o: float
    h: float
    l: float
    c: float
    v: int
    close_ms: int


def _ny_date(epoch_ms: int) -> date:
    return datetime.fromtimestamp(epoch_ms / 1000, timezone.utc).astimezone(NY).date()


def local_epoch_ms(d: date, hhmm: str) -> int:
    """New York civil time on date ``d`` -> bar-open epoch ms (IANA zone, never a fixed offset)."""
    h, m = map(int, hhmm.split(":"))
    return int(datetime(d.year, d.month, d.day, h, m, tzinfo=NY).timestamp() * 1000)


def _in_phase(epoch_ms: int, phase: str) -> bool:
    lo, hi = PHASES[phase]
    return lo <= _ny_date(epoch_ms) <= hi


def load_raw_phase(path: Path, phase: str) -> dict[int, Bar]:
    """Decode only ``phase``'s Entry bars; duplicates abort before any decoding."""
    staged: list[tuple[int, str, str]] = []
    with open(path, newline="", encoding="utf-8-sig") as fh:
        rows = csv.reader(fh)
        hdr = [h.strip() for h in next(rows)]
        i_type, i_sig, i_px = hdr.index("Type"), hdr.index("Signal"), hdr.index("Price USD")
        for row in rows:
            if not row[i_type].startswith("Entry"):
                continue
            head = row[i_sig].strip().split("|", 1)[0]
            if not head.isdigit():
                raise InputError(f"Entry row without a bar-open epoch: {head!r}")
            if _in_phase(int(head), phase):
                staged.append((int(head), row[i_sig], row[i_px]))
    dup = [e for e, n in Counter(e for e, _, _ in staged).items() if n > 1]
    if dup:
        raise InputError(f"duplicate raw bar-open timestamps (before decoding): {sorted(dup)[:5]}")
    bars: dict[int, Bar] = {}
    for epoch, sig, px in staged:
        m = SIGNAL_PIPE_V2_RE.match(sig.strip())
        if not m:
            raise InputError(f"malformed v0.2 Signal at epoch {epoch}")
        meta = {k: m.group(g) for k, g in (("ticker", "ticker"), ("type", "type"), ("quote_currency", "quote_ccy"),
                                            ("base_currency", "base_ccy"), ("timezone", "tz"), ("timeframe", "tf"))}
        meta.update(mintick=float(m.group("mintick")), pointvalue=float(m.group("pointvalue")))
        if meta != EXPECTED_META:
            raise InputError(f"instrument metadata drift at epoch {epoch}")
        bar = Bar(*(float(m.group(k)) for k in "ohlc"), int(m.group("v")), int(m.group("time_close")))
        if abs(float(px) - bar.c) > price_tolerance("MCL", bar.c):
            raise InputError(f"Entry price differs from encoded close at epoch {epoch}")
        bars[epoch] = bar
    return bars


def load_panel_phase(path: Path, phase: str) -> dict[int, tuple[float, float, float, float, int]]:
    out: dict[int, tuple] = {}
    with open(path, newline="", encoding="utf-8") as fh:
        rows = csv.reader(fh)
        if next(rows) != ["time", "open", "high", "low", "close", "volume"]:
            raise InputError("panel header differs from time,open,high,low,close,volume")
        for row in rows:
            ts = int(datetime.strptime(row[0], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp() * 1000)
            if not _in_phase(ts, phase):
                continue
            if ts in out:
                raise InputError(f"duplicate panel timestamp {row[0]}")
            out[ts] = (*map(float, row[1:5]), int(row[5]))
    return out


def compare_panel(raw: dict[int, Bar], panel: dict[int, tuple]) -> dict:
    if raw.keys() != panel.keys():
        raise InputError(f"panel/raw timestamp sets differ: raw-only {len(raw.keys() - panel.keys())}, "
                         f"panel-only {len(panel.keys() - raw.keys())}")
    bad = sum((b.o, b.h, b.l, b.c, b.v) != panel[t] for t, b in raw.items())
    if bad:
        raise InputError(f"{bad} phase bars differ between decoded raw and panel")
    return {"bars": len(raw), "timestamp_sets_equal": True, "ohlcv_mismatches": 0}


def _valid_ohlc(b: Bar) -> bool:
    return all(map(math.isfinite, (b.o, b.h, b.l, b.c))) and b.l <= min(b.o, b.c) <= max(b.o, b.c) <= b.h


def signal_status(bars: dict[int, Bar], d: date, clock: str) -> tuple[str, list[str]]:
    """('eligible'|'missing_feature'|'zero_denominator', detail) from information available at ``clock``."""
    dec = local_epoch_ms(d, clock)
    opens = [dec - BAR_MS * k for k in range(5, 0, -1)]  # t-4..t; t closes exactly at the decision
    fb = [bars.get(t) for t in opens]
    for t, b in zip(opens, fb):  # every existing feature bar, even in a window that is unavailable
        if b is not None and not _valid_ohlc(b):
            raise InputError(f"invalid OHLC in feature bar at epoch {t}")
    missing = [datetime.fromtimestamp(t / 1000, NY).strftime("%H:%M") for t, b in zip(opens, fb)
               if b is None or b.close_ms - t != BAR_MS]
    if missing:
        return "missing_feature", missing
    r = [b.h - b.l for b in fb]
    last4 = fb[1:]
    den = {"F1": r[4], "F2": sum(r[1:]), "F3": max(b.h for b in last4) - min(b.l for b in last4),
           "F4": sum(r[:4]) / 4}
    zero = [k for k, v in den.items() if not v > 0]
    if zero:
        return "zero_denominator", zero
    t_ = fb[4]
    feats = ((t_.c - t_.o) / den["F1"], (t_.c - fb[1].o) / den["F2"],
             (t_.c - min(b.l for b in last4)) / den["F3"], r[4] / den["F4"])
    if not all(map(math.isfinite, feats)):
        return "zero_denominator", ["nonfinite_feature"]
    return "eligible", []


def endpoint_gaps(bars: dict[int, Bar], d: date, clock: str) -> list[dict]:
    """Scheduled entry (decision+15m) and exit (+75m) opens; existence and finiteness only."""
    dec = local_epoch_ms(d, clock)
    gaps = []
    for role, t in (("entry", dec + BAR_MS), ("exit", dec + 5 * BAR_MS)):
        b = bars.get(t)
        if b is None or not math.isfinite(b.o):
            gaps.append({"date": d.isoformat(), "clock": clock, "endpoint": role,
                         "local_open": datetime.fromtimestamp(t / 1000, NY).strftime("%H:%M"),
                         "utc_open": datetime.fromtimestamp(t / 1000, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                         "reason": "absent" if b is None else "nonfinite_open"})
    return gaps


def readiness(bars: dict[int, Bar], phase: str) -> dict:
    lo, hi = PHASES[phase]
    by_clock = {c: Counter() for c in CLOCKS}
    zero_by_feature, weekday = Counter(), defaultdict(Counter)
    per_quarter, eligible_days, gaps, empty_weekdays, excluded = defaultdict(Counter), set(), [], [], []
    d = lo
    while d <= hi:
        wd = d.strftime("%a")
        weekday[wd]["dates"] += 1
        if d.weekday() < 5 and d in calendar_excluded(d.year):
            excluded.append(d.isoformat())
            weekday[wd]["calendar_excluded"] += 1
        elif d.weekday() < 5:
            for c in CLOCKS:
                st, detail = signal_status(bars, d, c)
                by_clock[c][st] += 1
                if st == "zero_denominator":
                    zero_by_feature.update(detail)
                if st == "eligible":
                    eligible_days.add(d)
                    per_quarter[f"{d.year}Q{(d.month - 1) // 3 + 1}"][c] += 1
                    if phase == "development":  # calibration never requests endpoint prices
                        gaps += endpoint_gaps(bars, d, c)
            if d not in eligible_days:
                empty_weekdays.append(d.isoformat())
        weekday[wd]["dates_with_eligible_signal"] += d in eligible_days
        d += timedelta(days=1)
    rep = {"opportunities_by_clock": {c: dict(by_clock[c]) for c in CLOCKS},
           "zero_denominator_by_feature": dict(zero_by_feature),
           "weekday_dates": {k: dict(v) for k, v in weekday.items()},
           "eligible_sessions": len(eligible_days), "weekdays_without_eligible_signal": empty_weekdays,
           "calendar_excluded": excluded,
           "reasons": []}
    if phase == "calibration":
        rep["eligible_by_quarter_and_clock"] = {q: dict(v) for q, v in sorted(per_quarter.items())}
        if not eligible_days:
            rep["reasons"].append("no calibration observations for any feature")
    else:
        blocks = {n: sum(a <= x <= b for x in eligible_days) for n, a, b in DEV_BLOCKS}
        rep["eligible_sessions_by_block"] = blocks
        rep["missing_endpoints"] = gaps
        rep["reasons"] += [f"block {n} has {k} < {MIN_BLOCK_SESSIONS} eligible sessions"
                           for n, k in blocks.items() if k < MIN_BLOCK_SESSIONS]
        if gaps:
            rep["reasons"].append(f"{len(gaps)} scheduled endpoints missing for signal-eligible opportunities")
    rep["status"] = "READY" if not rep["reasons"] else (
        "INCONCLUSIVE-DATA" if phase == "development" else "BLOCKED")
    return rep


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run(data_root: Path, out_dir: Path, phases: list[str], spec_root: Path | None = None) -> dict:
    cpu0 = time.process_time()
    for rel, want in PINNED.items():
        if (got := sha256((spec_root or data_root) / rel if rel == SPEC else data_root / rel)) != want:
            raise InputError(f"hash mismatch for {rel}: {got}")
    manifest = {"inputs": PINNED, "code_sha256": sha256(Path(__file__)), "python": sys.version.split()[0],
                "tzdata": importlib.metadata.version("tzdata"), "phases": {}}
    for ph in phases:
        try:
            raw = load_raw_phase(data_root / RAW, ph)
            integrity = compare_panel(raw, load_panel_phase(data_root / PANEL, ph))
            manifest["phases"][ph] = {"integrity": integrity, **readiness(raw, ph)}
        except InputError as exc:
            manifest["phases"][ph] = {"status": "STOP-INPUT-ERROR", "reasons": [str(exc)]}
    ok = all(p["status"] == "READY" for p in manifest["phases"].values()) and set(phases) == set(PHASES)
    manifest["verdict"] = "READY-FOR-BUILD" if ok else "BLOCKED"
    manifest["cpu_seconds"] = round(time.process_time() - cpu0, 3)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "readiness.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--data-root", type=Path, required=True, help="checkout holding the pinned private inputs")
    ap.add_argument("--spec-root", type=Path, help="checkout holding the pinned spec (default: --data-root)")
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--phase", choices=sorted(PHASES), action="append", help="default: both")
    a = ap.parse_args(argv)
    out = a.data_root / "local_artifacts" / "mcl_pilot" / a.run_id
    m = run(a.data_root, out, a.phase or list(PHASES), a.spec_root)
    print(json.dumps({"verdict": m["verdict"], "cpu_seconds": m["cpu_seconds"],
                      **{p: v["status"] for p, v in m["phases"].items()}, "report": str(out / "readiness.json")}))
    return 0 if m["verdict"] == "READY-FOR-BUILD" else 2


if __name__ == "__main__":
    raise SystemExit(main())
