"""Clean full-range Databento assembler for HARV-0 panels.

Supersedes the ad-hoc chunked/pull_missing/pull_yearly_remaining/concat scripts:
one cost-gated full-range pull per symbol (daily bars are ~$0 and the global
~/.databento_cache re-serves prior pulls free), normalized and concatenated into
the two panels build_panel.py / run_harv0.py consume.

Every pull goes through db_fetch.py (estimate-gated, --max-cost) — never a bare
timeseries.get_range (databento Rule 1 + brief §10 audit hook 4).
"""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
REPO = HERE.parents[2]  # worktree root (holds db_fetch.py under .claude/skills)
# The research venv lives in the MAIN checkout, not the worktree.
MAIN_REPO = Path("C:/Users/joshu/multi_firm_operations")
PY = MAIN_REPO / ".venv-research" / "Scripts" / "python.exe"
DB = REPO / ".claude" / "skills" / "databento-data" / "scripts" / "db_fetch.py"

PARENT_END = "2026-07-01"
GROUPS: dict[str, dict[str, tuple[str, str]]] = {
    "parents_ohlcv_1d.parquet": {
        "ES.c.0": ("2010-06-06", PARENT_END),
        "YM.c.0": ("2010-06-06", PARENT_END),
        "ZN.c.0": ("2010-06-06", PARENT_END),
        "GC.c.0": ("2010-06-06", PARENT_END),
    },
    "micros_ohlcv_1d.parquet": {
        "MES.c.0": ("2019-05-06", PARENT_END),
        "MYM.c.0": ("2019-05-06", PARENT_END),
    },
}
MAX_COST = "1.00"  # daily bars estimate at $0; ceiling is a hard guard.


def _yr_path(symbol: str, year: int) -> Path:
    return DATA / f"_yr_{symbol.replace('.', '_')}_{year}.parquet"


def _pull_chunk(symbol: str, start: str, end: str, dest: Path) -> bool:
    """One cost-gated yearly pull via db_fetch. Returns True on success."""
    cmd = [
        str(PY), str(DB), "pull",
        "--symbols", symbol, "--stype", "continuous", "--schema", "ohlcv-1d",
        "--start", start, "--end", end, "--max-cost", MAX_COST, "--out", str(dest),
    ]
    for attempt in range(1, 4):
        try:
            subprocess.check_call(cmd, cwd=str(REPO))
            if dest.exists() and dest.stat().st_size > 1500:
                return True
        except subprocess.CalledProcessError as exc:
            print(f"[err] {symbol} {start} rc={exc.returncode}", flush=True)
            time.sleep(4)
    return False


def pull_symbol(symbol: str, start: str, end: str) -> list[Path]:
    """Yearly chunks over [start, end). Full-range streaming was unreliable; small
    daily-bar chunks complete in seconds and are individually resumable."""
    s = pd.Timestamp(start)
    e = pd.Timestamp(end)
    paths: list[Path] = []
    for year in range(s.year, e.year + 1):
        a = max(s, pd.Timestamp(f"{year}-01-01"))
        b = min(e, pd.Timestamp(f"{year + 1}-01-01"))
        if a >= b:
            continue
        dest = _yr_path(symbol, year)
        if dest.exists() and dest.stat().st_size > 1500:
            print(f"[skip] {dest.name}", flush=True)
            paths.append(dest)
            continue
        astr, bstr = a.strftime("%Y-%m-%d"), b.strftime("%Y-%m-%d")
        print(f"[pull] {symbol} {astr}->{bstr}", flush=True)
        if _pull_chunk(symbol, astr, bstr, dest):
            paths.append(dest)
        else:
            raise SystemExit(f"pull failed: {symbol} {astr}->{bstr}")
    return paths


def _normalize(df: pd.DataFrame, symbol: str) -> pd.DataFrame:
    out = df.copy()
    if "ts_event" not in out.columns:
        out = out.reset_index()
        if "index" in out.columns and "ts_event" not in out.columns:
            out = out.rename(columns={"index": "ts_event"})
    if "symbol" not in out.columns:
        out["symbol"] = symbol
    else:
        # continuous pulls carry the continuous symbol already; force-consistent.
        out["symbol"] = symbol
    out["ts_event"] = pd.to_datetime(out["ts_event"], utc=True)
    keep = ["ts_event", "symbol", "open", "high", "low", "close"]
    keep = [c for c in keep if c in out.columns]
    return out[keep]


def assemble_group(out_name: str, spec: dict[str, tuple[str, str]]) -> None:
    frames = []
    for sym, (s, e) in spec.items():
        for p in pull_symbol(sym, s, e):
            frames.append(_normalize(pd.read_parquet(p), sym))
    out = pd.concat(frames, ignore_index=True)
    out = out.drop_duplicates(subset=["symbol", "ts_event"], keep="last")
    out = out.sort_values(["symbol", "ts_event"]).reset_index(drop=True)
    dest = DATA / out_name
    out.to_parquet(dest, index=False)
    per = out.groupby("symbol")["ts_event"].agg(["min", "max", "count"])
    print(f"[wrote] {dest.name} rows={len(out)}", flush=True)
    print(per.to_string(), flush=True)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for out_name, spec in GROUPS.items():
        if only and only not in out_name:
            continue
        assemble_group(out_name, spec)
    print("ASSEMBLE_DONE", flush=True)


if __name__ == "__main__":
    main()
