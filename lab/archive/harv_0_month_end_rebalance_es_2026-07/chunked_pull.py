"""Chunked Databento ohlcv-1d pull for HARV-0 (avoids 504 on long multi-symbol streams)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[3]
PY = REPO / ".venv-research" / "Scripts" / "python.exe"
DB = REPO / ".claude" / "skills" / "databento-data" / "scripts" / "db_fetch.py"
OUT = Path(__file__).resolve().parent / "data"
OUT.mkdir(parents=True, exist_ok=True)


def pull_one(symbol: str, start: str, end: str, dest: Path) -> None:
    if dest.exists() and dest.stat().st_size > 0:
        print(f"[skip] {dest.name}")
        return
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
    print("[run]", " ".join(cmd[-12:]))
    subprocess.check_call(cmd, cwd=str(REPO))


def year_chunks(start_year: int, end_year: int) -> list[tuple[str, str]]:
    chunks = []
    for y in range(start_year, end_year + 1):
        s = f"{y}-01-01"
        e = f"{y + 1}-01-01"
        if y == start_year and start_year == 2010:
            s = "2010-06-06"
        if y == end_year:
            e = "2026-07-01"
        chunks.append((s, e))
    return chunks


def concat_symbol(symbol: str, parts: list[Path], out: Path) -> None:
    frames = [pd.read_parquet(p) for p in parts if p.exists()]
    if not frames:
        raise SystemExit(f"no parts for {symbol}")
    df = pd.concat(frames, ignore_index=True)
    if "ts_event" in df.columns:
        df = df.drop_duplicates(subset=["ts_event"], keep="last")
        df = df.sort_values("ts_event")
    df.to_parquet(out, index=False)
    print(f"[wrote] {out.name} rows={len(df)}")


def main() -> None:
    parents = ["ES.c.0", "YM.c.0", "ZN.c.0", "GC.c.0"]
    micros = ["MES.c.0", "MYM.c.0"]

    parent_parts: dict[str, list[Path]] = {s: [] for s in parents}
    for symbol in parents:
        for start, end in year_chunks(2010, 2026):
            tag = f"{symbol.replace('.', '_')}_{start[:4]}"
            dest = OUT / f"_part_{tag}.parquet"
            pull_one(symbol, start, end, dest)
            parent_parts[symbol].append(dest)

    micro_parts: dict[str, list[Path]] = {s: [] for s in micros}
    for symbol in micros:
        for start, end in year_chunks(2019, 2026):
            if start < "2019-05-06":
                start = "2019-05-06"
            tag = f"{symbol.replace('.', '_')}_{start[:4]}"
            dest = OUT / f"_part_{tag}.parquet"
            pull_one(symbol, start, end, dest)
            micro_parts[symbol].append(dest)

    parent_frames = []
    for symbol, parts in parent_parts.items():
        out = OUT / f"{symbol.replace('.', '_')}_full.parquet"
        concat_symbol(symbol, parts, out)
        parent_frames.append(pd.read_parquet(out))
    parents_df = pd.concat(parent_frames, ignore_index=True)
    parents_df.to_parquet(OUT / "parents_ohlcv_1d.parquet", index=False)
    print("[wrote] parents_ohlcv_1d.parquet", len(parents_df))

    micro_frames = []
    for symbol, parts in micro_parts.items():
        out = OUT / f"{symbol.replace('.', '_')}_full.parquet"
        concat_symbol(symbol, parts, out)
        micro_frames.append(pd.read_parquet(out))
    micros_df = pd.concat(micro_frames, ignore_index=True)
    micros_df.to_parquet(OUT / "micros_ohlcv_1d.parquet", index=False)
    print("[wrote] micros_ohlcv_1d.parquet", len(micros_df))


if __name__ == "__main__":
    main()
