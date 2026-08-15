"""Year-by-year pulls for remaining HARV-0 symbols, then stitch to 4y part tags."""
from __future__ import annotations

import subprocess
import time
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[3]
PY = REPO / ".venv-research" / "Scripts" / "python.exe"
DB = REPO / ".claude" / "skills" / "databento-data" / "scripts" / "db_fetch.py"
DATA = Path(__file__).resolve().parent / "data"


def pull_year(symbol: str, year: int, start: str | None = None, end: str | None = None) -> Path:
    s = start or f"{year}-01-01"
    e = end or f"{year + 1}-01-01"
    dest = DATA / f"_yr_{symbol.replace('.', '_')}_{year}.parquet"
    if dest.exists() and dest.stat().st_size > 5000:
        print("[skip-yr]", dest.name, flush=True)
        return dest
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
        s,
        "--end",
        e,
        "--max-cost",
        "1.00",
        "--out",
        str(dest),
    ]
    for attempt in range(1, 4):
        print(f"[yr attempt {attempt}] {symbol} {s}->{e}", flush=True)
        try:
            subprocess.check_call(cmd, cwd=str(REPO))
            if dest.exists() and dest.stat().st_size > 3000:
                return dest
        except subprocess.CalledProcessError as exc:
            print("[err]", exc.returncode, flush=True)
            time.sleep(5)
    raise SystemExit(f"year pull failed {symbol} {year}")


def stitch(symbol: str, years: list[int], tag: str, paths: list[Path]) -> None:
    frames = []
    for p in paths:
        df = pd.read_parquet(p)
        if "ts_event" not in df.columns:
            df = df.reset_index()
            if "index" in df.columns and "ts_event" not in df.columns:
                df = df.rename(columns={"index": "ts_event"})
        if "symbol" not in df.columns:
            df["symbol"] = symbol
        frames.append(df)
    out = pd.concat(frames, ignore_index=True)
    out["ts_event"] = pd.to_datetime(out["ts_event"], utc=True)
    out = out.drop_duplicates(subset=["ts_event"], keep="last").sort_values("ts_event")
    dest = DATA / f"_part_{symbol.replace('.', '_')}_{tag}.parquet"
    # write with ts_event as index to match db_fetch style
    out = out.set_index("ts_event")
    out.to_parquet(dest)
    print(f"[stitched] {dest.name} n={len(out)}", flush=True)


def main() -> None:
    # ZN 2022-2026
    zn_paths = [
        pull_year("ZN.c.0", 2022),
        pull_year("ZN.c.0", 2023),
        pull_year("ZN.c.0", 2024),
        pull_year("ZN.c.0", 2025),
        pull_year("ZN.c.0", 2026, "2026-01-01", "2026-07-01"),
    ]
    stitch("ZN.c.0", [2022, 2023, 2024, 2025, 2026], "2022", zn_paths)

    # GC full history year-by-year then stitch into 4 tags
    gc_blocks = {
        "2010": list(range(2010, 2014)),
        "2014": list(range(2014, 2018)),
        "2018": list(range(2018, 2022)),
        "2022": list(range(2022, 2027)),
    }
    for tag, years in gc_blocks.items():
        paths = []
        for y in years:
            if y == 2010:
                paths.append(pull_year("GC.c.0", y, "2010-06-06", "2011-01-01"))
            elif y == 2026:
                paths.append(pull_year("GC.c.0", y, "2026-01-01", "2026-07-01"))
            else:
                paths.append(pull_year("GC.c.0", y))
        stitch("GC.c.0", years, tag, paths)

    # Micros
    for sym in ("MES.c.0", "MYM.c.0"):
        p2019 = [
            pull_year(sym, 2019, "2019-05-06", "2020-01-01"),
            pull_year(sym, 2020),
            pull_year(sym, 2021),
        ]
        stitch(sym, [2019, 2020, 2021], "2019", p2019)
        p2022 = [
            pull_year(sym, 2022),
            pull_year(sym, 2023),
            pull_year(sym, 2024),
            pull_year(sym, 2025),
            pull_year(sym, 2026, "2026-01-01", "2026-07-01"),
        ]
        stitch(sym, [2022, 2023, 2024, 2025, 2026], "2022", p2022)

    print("YEARLY_DONE", flush=True)


if __name__ == "__main__":
    main()
