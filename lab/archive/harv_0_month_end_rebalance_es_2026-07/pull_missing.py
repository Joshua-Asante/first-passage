"""Pull only the missing HARV-0 parts listed by audit_parts logic."""
from __future__ import annotations

import subprocess
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
PY = REPO / ".venv-research" / "Scripts" / "python.exe"
DB = REPO / ".claude" / "skills" / "databento-data" / "scripts" / "db_fetch.py"
DATA = Path(__file__).resolve().parent / "data"

# (symbol, start, end, tag)
MISSING = [
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


def pull_once(symbol: str, start: str, end: str, dest: Path) -> bool:
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
    print("[run]", symbol, start, end, flush=True)
    try:
        subprocess.check_call(cmd, cwd=str(REPO))
    except subprocess.CalledProcessError as e:
        print("[err]", e.returncode, flush=True)
        return False
    return dest.exists() and dest.stat().st_size > 10000


def main() -> None:
    for symbol, start, end, tag in MISSING:
        dest = DATA / f"_part_{symbol.replace('.', '_')}_{tag}.parquet"
        if dest.exists() and dest.stat().st_size > 20000:
            print("[skip]", dest.name, flush=True)
            continue
        ok = False
        for attempt in range(1, 4):
            print(f"[attempt {attempt}] {dest.name}", flush=True)
            if pull_once(symbol, start, end, dest):
                ok = True
                break
            time.sleep(8)
        if not ok:
            raise SystemExit(f"failed {dest.name}")
    print("MISSING_DONE", flush=True)


if __name__ == "__main__":
    main()
