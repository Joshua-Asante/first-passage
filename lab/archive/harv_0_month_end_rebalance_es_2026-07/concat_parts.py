"""Concatenate completed _part_*.parquet into parents/micros panels."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parent / "data"

PARENT_SPEC = {
    "ES.c.0": ["2010", "2014", "2018", "2022"],
    "YM.c.0": ["2010", "2014", "2018", "2022"],
    "ZN.c.0": ["2010", "2014", "2018", "2022"],
    "GC.c.0": ["2010", "2014", "2018", "2022"],
}
MICRO_SPEC = {
    "MES.c.0": ["2019", "2022"],
    "MYM.c.0": ["2019", "2022"],
}


def _part_path(symbol: str, year: str) -> Path:
    safe = symbol.replace(".", "_")
    return DATA / f"_part_{safe}_{year}.parquet"


def _missing(spec: dict[str, list[str]]) -> list[str]:
    miss = []
    for sym, years in spec.items():
        for y in years:
            p = _part_path(sym, y)
            if not p.exists() or p.stat().st_size == 0:
                miss.append(p.name)
    return miss


def _normalize(df: pd.DataFrame, symbol: str) -> pd.DataFrame:
    out = df.copy()
    if "ts_event" not in out.columns:
        out = out.reset_index()
        if "index" in out.columns and "ts_event" not in out.columns:
            out = out.rename(columns={"index": "ts_event"})
    if "symbol" not in out.columns:
        out["symbol"] = symbol
    out["ts_event"] = pd.to_datetime(out["ts_event"], utc=True)
    return out


def _concat(spec: dict[str, list[str]], out_name: str) -> pd.DataFrame:
    frames = []
    for sym, years in spec.items():
        for y in years:
            p = _part_path(sym, y)
            frames.append(_normalize(pd.read_parquet(p), sym))
    out = pd.concat(frames, ignore_index=True)
    out = out.drop_duplicates(subset=["symbol", "ts_event"], keep="last")
    out = out.sort_values(["symbol", "ts_event"])
    dest = DATA / out_name
    out.to_parquet(dest, index=False)
    print(f"[wrote] {dest.name} rows={len(out)} symbols={out['symbol'].nunique()}")
    return out


def main(h1_only: bool = False) -> None:
    """Concat parts. h1_only=True: ES+ZN(+YM if present); skip GC/MES for Path A."""
    if h1_only:
        parent = {
            "ES.c.0": PARENT_SPEC["ES.c.0"],
            "ZN.c.0": PARENT_SPEC["ZN.c.0"],
        }
        # Include YM if all parts present (sunk cost; non-gating).
        ym_miss = [y for y in PARENT_SPEC["YM.c.0"] if not _part_path("YM.c.0", y).exists()]
        if not ym_miss:
            parent["YM.c.0"] = PARENT_SPEC["YM.c.0"]
        miss = _missing(parent)
        if miss:
            raise SystemExit(f"missing H1-critical parts ({len(miss)}): {miss}")
        _concat(parent, "parents_ohlcv_1d.parquet")
        print("CONCAT_OK h1_only")
        return

    miss = _missing(PARENT_SPEC) + _missing(MICRO_SPEC)
    if miss:
        raise SystemExit(f"missing parts ({len(miss)}): {miss}")
    _concat(PARENT_SPEC, "parents_ohlcv_1d.parquet")
    _concat(MICRO_SPEC, "micros_ohlcv_1d.parquet")
    print("CONCAT_OK")


if __name__ == "__main__":
    import sys

    main(h1_only="--h1-only" in sys.argv)
