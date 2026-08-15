#!/usr/bin/env python3
"""Assemble the CONCEPT-USDCAD-RDM-001 ("Sovereign") F1 input panel.

Feed policy (operator executive decision 2026-06-11, ADR pending): canonical
analyses run on TV CSV exports — no canonical reliance on programmatic bar
feeds (Dukascopy/REST staging only, and not used here at all). The two price
series are therefore OPERATOR-SUPPLIED TradingView chart exports; this script
validates their presence and coverage rather than fetching them.

Inputs:

1. USDCAD D1 2018-01 -> 2026-06 — TV chart export (Pepperstone feed preferred,
   matching the composite's feed family), dropped at inputs/USDCAD_D1_TV.csv.
2. WTI control D1, same span — TV chart export of the operator's chosen WTI
   symbol (e.g. Pepperstone SpotCrude / TVC:USOIL), at inputs/WTI_D1_TV.csv.
3. US 2yr — treasury.gov daily par-yield CSV ("2 Yr" column; same series FRED
   republishes as DGS2 — FRED itself blocked again, the Helios failure mode).
   Official rate data, not a bar feed: unaffected by the feed policy.
4. CA 2yr — Bank of Canada Valet BD.CDN.2YR.DQ.YLD (benchmark bond yield).
5. BoC FXUSDCAD official daily rate — cross-check series for the USDCAD export
   (different fixing time; the check is price-level agreement, not equality).
6. Constellation composite daily P&L — allocation-weighted static-$200K P&L
   from the six 2020-01->2026-06 decompound TV exports (operator-selected over
   the 2022+ canonical panels), reusing the decompound.py loader (stitch +
   static rebank), NOT re-derived. Vendor-licensed + gitignored; copied from
   ~/Downloads into the decompound inputs/ dir when absent.

Everything lands in inputs/ (gitignored via lab/analysis/**/inputs/*.csv).
Counts reported, never silent.
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import io
import json
import shutil
import sys
import time
import urllib.request
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parents[2]

INPUTS = _HERE / "inputs"

USDCAD_CSV = INPUTS / "USDCAD_D1_TV.csv"
WTI_CSV = INPUTS / "WTI_D1_TV.csv"
UST2Y_CSV = INPUTS / "UST_2Y.csv"
CA2Y_CSV = INPUTS / "CA_2Y.csv"
FXUSDCAD_CSV = INPUTS / "FXUSDCAD_BOC.csv"
COMPOSITE_CSV = INPUTS / "constellation_daily.csv"

_DECOMP_DIR = _REPO_ROOT / "lab" / "analysis" / "decompound_remc_2026-06-07"
_DOWNLOADS = Path.home() / "Downloads"

_TREASURY_URL = (
    "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/"
    "daily-treasury-rates.csv/{year}/all?type=daily_treasury_yield_curve"
    "&field_tdr_date_value={year}&page&_format=csv"
)
_BOC_URL = (
    "https://www.bankofcanada.ca/valet/observations/{series}/json"
    "?start_date=2017-12-01&end_date=2026-06-11"
)

# Coverage floors for the operator-supplied TV exports (2018-01 -> 2026-06 D1
# is ~2,200 trading days; require most of it so a truncated export cannot
# silently shrink the episode panel).
TV_MIN_ROWS = 2000
TV_REQUIRED_SPAN = ("2018-01-15", "2026-05-15")


def _get(url: str, *, retries: int = 3) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    last: Exception | None = None
    for i in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001 — retry then surface
            last = e
            time.sleep(2 * (i + 1))
    raise RuntimeError(f"GET failed after {retries} tries: {url}") from last


# ── operator-supplied TV exports: stage + validate, never fetch ─────────────

def stage_bar_export(src: Path, dst: Path, label: str) -> None:
    """Decode a BAR_EXPORT_v0.1 TV Strategy-Tester trade-list CSV into a D1
    close series.

    The export is the trade-list of a dummy strategy that trades every bar;
    each row's Signal column carries the bar as ``epoch_ms|o|h|l|c|v`` (the
    displayed "Date and time" is chart-TZ; the epoch is authoritative UTC).
    Bars are deduped by epoch, the daily close is the last bar of each UTC
    day. Counts reported, never silent."""
    import pandas as pd
    df = pd.read_csv(src, encoding="utf-8-sig")
    sig = df["Signal"].astype(str)
    parts = sig.str.split("|")
    ok = parts.str.len() >= 5
    n_open = int((sig == "Open").sum())
    n_bad = int((~ok).sum()) - n_open
    epochs = parts[ok].str[0].astype("int64")
    closes = parts[ok].str[4].astype(float)
    bars = (pd.DataFrame({"epoch": epochs, "close": closes})
            .drop_duplicates("epoch").sort_values("epoch"))
    dt = pd.to_datetime(bars["epoch"], unit="ms", utc=True)
    daily = (pd.DataFrame({"date": dt.dt.tz_localize(None).dt.normalize(),
                           "close": bars["close"].to_numpy()})
             .groupby("date")["close"].last())
    INPUTS.mkdir(parents=True, exist_ok=True)
    daily.to_csv(dst, header=["close"])
    print(f"  staged {label}: {len(df)} rows -> {len(bars)} unique 15m bars "
          f"-> {len(daily)} D1 closes {daily.index.min():%Y-%m-%d} -> "
          f"{daily.index.max():%Y-%m-%d} (skipped: {n_open} 'Open' rows, "
          f"{n_bad} unparseable) -> {dst.name}")


# ── operator-supplied TV exports: validate, never fetch ─────────────────────

def check_tv_export(path: Path, label: str) -> bool:
    """Presence + coverage check for an operator-dropped TV chart export.
    Schema-tolerant (gate.py does the real parsing); here we only need a date
    column and row count."""
    if not path.exists():
        print(f"!! MISSING {label}: drop a TradingView D1 chart export at\n"
              f"   {path}\n"
              f"   (symbol per README; window {TV_REQUIRED_SPAN[0]} -> "
              f"{TV_REQUIRED_SPAN[1]}+, ~2,200 rows expected)")
        return False
    import pandas as pd
    df = pd.read_csv(path)
    tcol = next((c for c in df.columns
                 if c.strip().lower() in ("time", "date", "datetime")), None)
    if tcol is None:
        print(f"!! {label}: no time/date column in {path.name} "
              f"(columns: {list(df.columns)})")
        return False
    t = pd.to_datetime(df[tcol], unit="s", errors="coerce")
    if t.isna().all():
        t = pd.to_datetime(df[tcol], errors="coerce", utc=True)
    t = t.dropna()
    lo, hi = t.min(), t.max()
    ok = (len(df) >= TV_MIN_ROWS
          and lo <= pd.Timestamp(TV_REQUIRED_SPAN[0], tz=lo.tz)
          and hi >= pd.Timestamp(TV_REQUIRED_SPAN[1], tz=hi.tz))
    print(f"  {label}: {len(df)} rows {lo:%Y-%m-%d} -> {hi:%Y-%m-%d} "
          f"{'OK' if ok else f'!! INSUFFICIENT (need >={TV_MIN_ROWS} rows covering '+TV_REQUIRED_SPAN[0]+' -> '+TV_REQUIRED_SPAN[1]+')'}")
    return bool(ok)


# ── Treasury 2yr ────────────────────────────────────────────────────────────

def fetch_us2y() -> None:
    if UST2Y_CSV.exists():
        print(f"=== {UST2Y_CSV.name} exists — skipping ===")
        return
    rows: list[tuple[str, float]] = []
    for year in range(2018, 2027):
        body = _get(_TREASURY_URL.format(year=year)).decode("utf-8-sig")
        rdr = csv.DictReader(io.StringIO(body))
        n = 0
        for rec in rdr:
            v = (rec.get("2 Yr") or "").strip()
            if not v:
                continue
            mm, dd, yyyy = rec["Date"].split("/")
            rows.append((f"{yyyy}-{mm}-{dd}", float(v)))
            n += 1
        print(f"  UST 2Yr {year}: {n} rows")
    rows.sort()
    INPUTS.mkdir(parents=True, exist_ok=True)
    with UST2Y_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["date", "us2y"])
        w.writerows(rows)
    print(f"=== UST 2Yr: {len(rows)} rows -> {UST2Y_CSV.name} ===")


# ── Bank of Canada Valet ────────────────────────────────────────────────────

def _fetch_boc(series: str, out: Path, col: str) -> None:
    if out.exists():
        print(f"=== {out.name} exists — skipping ===")
        return
    data = json.loads(_get(_BOC_URL.format(series=series)))
    rows = [(o["d"], float(o[series]["v"]))
            for o in data["observations"] if o.get(series, {}).get("v")]
    rows.sort()
    INPUTS.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["date", col])
        w.writerows(rows)
    print(f"=== BoC {series}: {len(rows)} rows -> {out.name} ===")


# ── Constellation composite (decompound.py reuse) ──────────────────────────

def build_composite() -> None:
    if COMPOSITE_CSV.exists():
        print(f"=== {COMPOSITE_CSV.name} exists — skipping ===")
        return
    spec = importlib.util.spec_from_file_location(
        "decompound", _DECOMP_DIR / "decompound.py")
    decomp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(decomp)

    missing = []
    for fnames in decomp.FILES.values():
        for fname in fnames:
            tgt = _DECOMP_DIR / "inputs" / fname
            if tgt.exists():
                continue
            src = _DOWNLOADS / fname
            if src.exists():
                tgt.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, tgt)
                print(f"  staged {fname} from ~/Downloads")
            else:
                missing.append(fname)
    if missing:
        raise SystemExit(f"composite inputs missing (not in decompound inputs/ "
                         f"nor ~/Downloads): {missing}")

    import pandas as pd
    daily: dict = {}
    for strat in decomp.FILES:
        t = decomp.stitch(strat)
        exp = decomp.EXPECTED_RAW_COUNTS[strat]
        if len(t) != exp:
            raise SystemExit(f"{strat}: {len(t)} trades post-dedup, expected {exp} "
                             f"(decompound.py inventory) — refusing to continue")
        static = decomp.rebank(t, "static")          # [exit_date, pnl] static-$200K
        g = static.groupby("exit_date")["pnl"].sum()
        daily[strat] = g
        print(f"  {strat}: {len(t)} trades, {len(g)} active days, "
              f"net ${g.sum():,.0f} static")
    df = pd.DataFrame(daily).fillna(0.0)
    df["composite"] = df.sum(axis=1)
    df.index.name = "date"
    INPUTS.mkdir(parents=True, exist_ok=True)
    df.to_csv(COMPOSITE_CSV, float_format="%.2f")
    print(f"=== composite: {len(df)} active days "
          f"{df.index.min()} -> {df.index.max()}, "
          f"net ${df['composite'].sum():,.0f} -> {COMPOSITE_CSV.name} ===")


# ── main ────────────────────────────────────────────────────────────────────

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--only", choices=["rates", "composite", "tv-check"],
                    help="run a single component (default: all)")
    a = ap.parse_args(argv)

    if a.only in (None, "rates"):
        fetch_us2y()
        _fetch_boc("BD.CDN.2YR.DQ.YLD", CA2Y_CSV, "ca2y")
        _fetch_boc("FXUSDCAD", FXUSDCAD_CSV, "fxusdcad")
    if a.only in (None, "composite"):
        build_composite()
    ok = True
    if a.only in (None, "tv-check"):
        ok = check_tv_export(USDCAD_CSV, "USDCAD D1 (TV export)")
        ok = check_tv_export(WTI_CSV, "WTI D1 (TV export)") and ok
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
