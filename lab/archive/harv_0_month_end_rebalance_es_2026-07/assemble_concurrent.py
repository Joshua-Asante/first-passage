"""Fast concurrent Databento assembler for HARV-0 panels.

Why: the per-chunk cost is dominated by python-startup + `import databento` +
four sequential metadata round-trips (dataset-range/cost/billable/record-count),
~15 s/chunk even on a cache hit. Large/multi-symbol requests stall outright. So the
speedup is NOT bigger requests — it is (a) one process (databento imported once)
and (b) overlapping the network waits with a thread pool. Each request stays the
only reliable size: single-symbol, single-year.

Discipline preserved: pulls go through db_fetch.pull() (imported, not shelled),
so the cost-gate + `timeseries.get_range` stay inside db_fetch.py (audit hook 4
stays clean) and every chunk is still estimate-gated under --max-cost.

MYM dropped: run_harv0.py consumes only MES for the micro-OOS gate; MYM is unused.
"""
from __future__ import annotations

import importlib.util
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from types import SimpleNamespace

import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
MAIN_REPO = Path("C:/Users/joshu/multi_firm_operations")
DB_PATH = MAIN_REPO / ".claude" / "skills" / "databento-data" / "scripts" / "db_fetch.py"

_spec = importlib.util.spec_from_file_location("db_fetch", DB_PATH)
db_fetch = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(db_fetch)

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
    },
}
MAX_COST = 1.00
WORKERS = 6
_print_lock = threading.Lock()


def _log(msg: str) -> None:
    with _print_lock:
        print(msg, flush=True)


def _yr_path(symbol: str, year: int) -> Path:
    return DATA / f"_yr_{symbol.replace('.', '_')}_{year}.parquet"


def _chunks(symbol: str, start: str, end: str) -> list[tuple[str, str, str, Path]]:
    s, e = pd.Timestamp(start), pd.Timestamp(end)
    out = []
    for year in range(s.year, e.year + 1):
        a = max(s, pd.Timestamp(f"{year}-01-01"))
        b = min(e, pd.Timestamp(f"{year + 1}-01-01"))
        if a >= b:
            continue
        out.append((symbol, a.strftime("%Y-%m-%d"), b.strftime("%Y-%m-%d"), _yr_path(symbol, year)))
    return out


def _pull_one(symbol: str, start: str, end: str, dest: Path) -> tuple[Path, str]:
    if dest.exists() and dest.stat().st_size > 1500:
        return dest, "skip"
    ns = SimpleNamespace(
        symbols=symbol, stype="continuous", schema="ohlcv-1d",
        start=start, end=end, max_cost=MAX_COST, force=False, out=str(dest),
    )
    for attempt in range(1, 4):
        try:
            db_fetch.pull(ns)
            if dest.exists() and dest.stat().st_size > 1500:
                return dest, "ok"
        except SystemExit as exc:  # cost-gate abort — should never trip for $0 daily bars
            return dest, f"ABORT:{exc}"
        except Exception as exc:  # noqa: BLE001 — network hiccup; retry
            _log(f"[retry] {symbol} {start} attempt {attempt}: {exc!r}")
    return dest, "FAIL"


def _normalize(df: pd.DataFrame, symbol: str) -> pd.DataFrame:
    out = df.copy()
    if "ts_event" not in out.columns:
        out = out.reset_index()
        if "index" in out.columns and "ts_event" not in out.columns:
            out = out.rename(columns={"index": "ts_event"})
    out["symbol"] = symbol
    out["ts_event"] = pd.to_datetime(out["ts_event"], utc=True)
    keep = [c for c in ("ts_event", "symbol", "open", "high", "low", "close") if c in out.columns]
    return out[keep]


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    # 1) collect every needed chunk across all groups
    jobs: list[tuple[str, str, str, str, Path]] = []
    for out_name, spec in GROUPS.items():
        for sym, (s, e) in spec.items():
            for symbol, a, b, dest in _chunks(sym, s, e):
                jobs.append((out_name, symbol, a, b, dest))

    todo = [j for j in jobs if not (j[4].exists() and j[4].stat().st_size > 1500)]
    _log(f"[plan] {len(jobs)} chunks total; {len(todo)} to pull; {len(jobs) - len(todo)} cached; workers={WORKERS}")

    # 2) pull missing chunks concurrently
    failures = []
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(_pull_one, sym, a, b, dest): (sym, a) for (_, sym, a, b, dest) in todo}
        done = 0
        for fut in as_completed(futs):
            sym, a = futs[fut]
            dest, status = fut.result()
            done += 1
            if status not in ("ok", "skip"):
                failures.append((sym, a, status))
            _log(f"[{done}/{len(todo)}] {sym} {a} -> {status}")
    if failures:
        _log(f"[FAILURES] {failures}")
        raise SystemExit(f"{len(failures)} chunk(s) failed: {failures}")

    # 3) concat per group
    for out_name, spec in GROUPS.items():
        frames = []
        for sym, (s, e) in spec.items():
            for _, a, b, dest in _chunks(sym, s, e):
                frames.append(_normalize(pd.read_parquet(dest), sym))
        panel = pd.concat(frames, ignore_index=True)
        panel = panel.drop_duplicates(subset=["symbol", "ts_event"], keep="last")
        panel = panel.sort_values(["symbol", "ts_event"]).reset_index(drop=True)
        panel.to_parquet(DATA / out_name, index=False)
        per = panel.groupby("symbol")["ts_event"].agg(["min", "max", "count"])
        _log(f"[wrote] {out_name} rows={len(panel)}")
        _log(per.to_string())
    _log("ASSEMBLE_DONE")


if __name__ == "__main__":
    main()
