"""Validated chunked pulls for HARV-0 Wave 1. Skips parts whose date span is complete."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[3]
PY = REPO / ".venv-research" / "Scripts" / "python.exe"
DB = REPO / ".claude" / "skills" / "databento-data" / "scripts" / "db_fetch.py"
DATA = Path(__file__).resolve().parent / "data"
DATA.mkdir(parents=True, exist_ok=True)

# (symbol, start, end, part_year_tag, min_rows expected-ish)
CHUNKS: list[tuple[str, str, str, str]] = [
    ("ES.c.0", "2010-06-06", "2014-01-01", "2010"),
    ("ES.c.0", "2014-01-01", "2018-01-01", "2014"),
    ("ES.c.0", "2018-01-01", "2022-01-01", "2018"),
    ("ES.c.0", "2022-01-01", "2026-07-01", "2022"),
    ("YM.c.0", "2010-06-06", "2014-01-01", "2010"),
    ("YM.c.0", "2014-01-01", "2018-01-01", "2014"),
    ("YM.c.0", "2018-01-01", "2022-01-01", "2018"),
    ("YM.c.0", "2022-01-01", "2026-07-01", "2022"),
    ("ZN.c.0", "2010-06-06", "2014-01-01", "2010"),
    ("ZN.c.0", "2014-01-01", "2018-01-01", "2014"),
    ("ZN.c.0", "2018-01-01", "2022-01-01", "2018"),
    ("ZN.c.0", "2022-01-01", "2026-07-01", "2022"),
    ("GC.c.0", "2010-06-06", "2014-01-01", "2010"),
    ("GC.c.0", "2014-01-01", "2018-01-01", "2014"),
    ("GC.c.0", "2018-01-01", "2022-01-01", "2018"),
    ("GC.c.0", "2022-01-01", "2026-07-01", "2022"),
    ("MES.c.0", "2019-05-06", "2022-01-01", "2019"),
    ("MES.c.0", "2022-01-01", "2026-07-01", "2022"),
    ("MYM.c.0", "2019-05-06", "2022-01-01", "2019"),
    ("MYM.c.0", "2022-01-01", "2026-07-01", "2022"),
]


def part_path(symbol: str, tag: str) -> Path:
    return DATA / f"_part_{symbol.replace('.', '_')}_{tag}.parquet"


def ts_series(df: pd.DataFrame) -> pd.DatetimeIndex:
    if "ts_event" in df.columns:
        return pd.to_datetime(df["ts_event"], utc=True)
    return pd.to_datetime(df.index, utc=True)


def part_ok(path: Path, start: str, end: str) -> bool:
    if not path.exists() or path.stat().st_size < 1000:
        return False
    df = pd.read_parquet(path)
    if len(df) < 50:
        return False
    ts = ts_series(df)
    # Require coverage into the last year of the requested window
    end_ts = pd.Timestamp(end, tz="UTC") - pd.Timedelta(days=5)
    start_ts = pd.Timestamp(start, tz="UTC") + pd.Timedelta(days=5)
    return bool(ts.min() <= start_ts and ts.max() >= end_ts)


def pull(symbol: str, start: str, end: str, dest: Path) -> None:
    cmd = [
        str(PY),
        str(DB),
        "pull",
        "--symbols",
        symbol,
        "--stype",
        "continuous",
        "--schema",
        "ohlcv-1d",
        "--start",
        start,
        "--end",
        end,
        "--max-cost",
        "1.00",
        "--out",
        str(dest),
    ]
    print("[run]", symbol, start, end, "->", dest.name, flush=True)
    subprocess.check_call(cmd, cwd=str(REPO))


def main() -> None:
    for symbol, start, end, tag in CHUNKS:
        dest = part_path(symbol, tag)
        if part_ok(dest, start, end):
            print("[skip]", dest.name, flush=True)
            continue
        if dest.exists():
            bad = dest.with_name(dest.stem + "_BAD.parquet")
            dest.replace(bad)
            print("[moved-bad]", dest.name, "->", bad.name, flush=True)
        pull(symbol, start, end, dest)
        if not part_ok(dest, start, end):
            raise SystemExit(f"part still incomplete after pull: {dest}")
    print("ALL_PARTS_OK", flush=True)


if __name__ == "__main__":
    main()
