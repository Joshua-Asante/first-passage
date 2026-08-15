"""Report which HARV-0 part files are missing or incomplete."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parent / "data"
NEEDED = {
    "ES.c.0": [
        ("2010", "2010-06-06", "2013-12-20"),
        ("2014", "2014-01-05", "2017-12-20"),
        ("2018", "2018-01-05", "2021-12-20"),
        ("2022", "2022-01-05", "2026-06-20"),
    ],
    "YM.c.0": [
        ("2010", "2010-06-06", "2013-12-20"),
        ("2014", "2014-01-05", "2017-12-20"),
        ("2018", "2018-01-05", "2021-12-20"),
        ("2022", "2022-01-05", "2026-06-20"),
    ],
    "ZN.c.0": [
        ("2010", "2010-06-06", "2013-12-20"),
        ("2014", "2014-01-05", "2017-12-20"),
        ("2018", "2018-01-05", "2021-12-20"),
        ("2022", "2022-01-05", "2026-06-20"),
    ],
    "GC.c.0": [
        ("2010", "2010-06-06", "2013-12-20"),
        ("2014", "2014-01-05", "2017-12-20"),
        ("2018", "2018-01-05", "2021-12-20"),
        ("2022", "2022-01-05", "2026-06-20"),
    ],
    "MES.c.0": [
        ("2019", "2019-05-10", "2021-12-20"),
        ("2022", "2022-01-05", "2026-06-20"),
    ],
    "MYM.c.0": [
        ("2019", "2019-05-10", "2021-12-20"),
        ("2022", "2022-01-05", "2026-06-20"),
    ],
}


def main() -> None:
    miss: list[str] = []
    for sym, chunks in NEEDED.items():
        for tag, start, end in chunks:
            p = DATA / f"_part_{sym.replace('.', '_')}_{tag}.parquet"
            if not p.exists() or p.stat().st_size < 1000:
                print(f"MISSING {p.name}")
                miss.append(f"{sym}|{tag}|{start}|{end}")
                continue
            df = pd.read_parquet(p)
            ts = pd.to_datetime(
                df["ts_event"] if "ts_event" in df.columns else df.index, utc=True
            )
            ok = ts.min() <= pd.Timestamp(start, tz="UTC") + pd.Timedelta(
                days=10
            ) and ts.max() >= pd.Timestamp(end, tz="UTC")
            status = "OK" if ok else "BAD"
            print(f"{status} {p.name} {ts.min().date()}->{ts.max().date()} n={len(df)}")
            if not ok:
                miss.append(f"{sym}|{tag}|{start}|{end}")
    print(f"NEED_PULLS={len(miss)}")
    for m in miss:
        print(f"PULL {m}")


if __name__ == "__main__":
    main()
