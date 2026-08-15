from __future__ import annotations
import subprocess
import time
from pathlib import Path
import pandas as pd

REPO = Path(r"c:\Users\joshu\multi_firm_operations")
PY = REPO / ".venv-research" / "Scripts" / "python.exe"
DB = REPO / ".claude" / "skills" / "databento-data" / "scripts" / "db_fetch.py"
DATA = REPO / "lab" / "analysis" / "harv_0_month_end_rebalance_es_2026-07" / "data"
DATA.mkdir(parents=True, exist_ok=True)

PARENTS = {
    "ES.c.0": ("2010-06-06", "2026-07-01"),
    "YM.c.0": ("2010-06-06", "2026-07-01"),
    "ZN.c.0": ("2010-06-06", "2026-07-01"),
    "GC.c.0": ("2010-06-06", "2026-07-01"),
}
MICROS = {
    "MES.c.0": ("2019-05-06", "2026-07-01"),
    "MYM.c.0": ("2019-05-06", "2026-07-01"),
}
SKIP_TOKENS = ("INCOMPLETE", "_BAD", ".bak", "YEARONLY")
MAX_RETRIES = 4


def part_files(symbol: str):
    safe = symbol.replace(".", "_")
    for p in sorted(DATA.glob(f"_part_{safe}_*.parquet")):
        if any(tok in p.name for tok in SKIP_TOKENS):
            continue
        if p.stat().st_size <= 0:
            continue
        yield p


def ts_of(df: pd.DataFrame) -> pd.DatetimeIndex:
    if "ts_event" in df.columns:
        return pd.to_datetime(df["ts_event"], utc=True)
    return pd.to_datetime(df.index, utc=True)


def covered_max(symbol: str):
    mx = None
    for p in part_files(symbol):
        df = pd.read_parquet(p)
        if len(df) == 0:
            continue
        ts = ts_of(df)
        if mx is None or ts.max() > mx:
            mx = ts.max()
    return mx


def year_windows(start: str, end: str):
    s = pd.Timestamp(start, tz="UTC")
    e = pd.Timestamp(end, tz="UTC")
    out = []
    for y in range(s.year, e.year + 1):
        a = pd.Timestamp(f"{y}-01-01", tz="UTC")
        b = pd.Timestamp(f"{y + 1}-01-01", tz="UTC")
        if a < s:
            a = s
        if b > e:
            b = e
        if a >= b:
            continue
        out.append((a.strftime("%Y-%m-%d"), b.strftime("%Y-%m-%d"), str(y)))
    return out


def pull(symbol, start, end, dest: Path):
    cmd = [
        str(PY), str(DB), "pull",
        "--symbols", symbol, "--stype", "continuous",
        "--schema", "ohlcv-1d", "--start", start, "--end", end,
        "--max-cost", "1.00", "--out", str(dest),
    ]
    print("[run]", symbol, start, end, "->", dest.name, flush=True)
    last_err = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            subprocess.check_call(cmd, cwd=str(REPO))
            return
        except subprocess.CalledProcessError as exc:
            last_err = exc
            print(f"[retry] {dest.name} attempt={attempt} rc={exc.returncode}", flush=True)
            time.sleep(5 * attempt)
    raise last_err


def ensure_symbol(symbol: str, start: str, end: str):
    end_need = pd.Timestamp(end, tz="UTC") - pd.Timedelta(days=3)
    mx = covered_max(symbol)
    if mx is not None and mx >= end_need:
        print(f"[complete] {symbol} through {mx.date()}", flush=True)
        return
    resume_from = None if mx is None else (mx + pd.Timedelta(days=1))
    print(f"[resume] {symbol} from {resume_from.date() if resume_from is not None else start}", flush=True)
    for a, b, tag in year_windows(start, end):
        a_ts = pd.Timestamp(a, tz="UTC")
        b_ts = pd.Timestamp(b, tz="UTC")
        if resume_from is not None and b_ts <= resume_from:
            print(f"[skip-covered] {symbol} {tag}", flush=True)
            continue
        if resume_from is not None and a_ts < resume_from:
            a_ts = resume_from
            a = a_ts.strftime("%Y-%m-%d")
        if (b_ts - a_ts).days < 7:
            print(f"[skip-short] {symbol} {a}->{b}", flush=True)
            continue
        dest = DATA / f"_part_{symbol.replace('.', '_')}_{tag}.parquet"
        if dest.exists() and dest.stat().st_size > 1000:
            df = pd.read_parquet(dest)
            if len(df) == 0:
                dest.unlink()
            else:
                ts = ts_of(df)
                if ts.max() >= (b_ts - pd.Timedelta(days=5)):
                    print(f"[skip] {dest.name} ({ts.min().date()}->{ts.max().date()})", flush=True)
                    continue
                bad = dest.with_name(dest.stem + "_INCOMPLETE.parquet")
                if bad.exists():
                    bad.unlink()
                dest.replace(bad)
                print(f"[moved-incomplete] -> {bad.name}", flush=True)
        pull(symbol, a, b, dest)
        mx2 = covered_max(symbol)
        if mx2 is not None:
            resume_from = mx2 + pd.Timedelta(days=1)


def main():
    for sym, (s, e) in {**PARENTS, **MICROS}.items():
        ensure_symbol(sym, s, e)
    print("PULL_PHASE_DONE", flush=True)


if __name__ == "__main__":
    main()
