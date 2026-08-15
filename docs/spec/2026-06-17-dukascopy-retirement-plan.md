# Dukascopy Retirement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Retire the Dukascopy bar adapter entirely and make the TradingView/Pepperstone BAR EXPORT v0.1 comment-encoded export the canonical producer of `core/data/bar_data/<SYMBOL>_M15.csv`.

**Architecture:** Producer swap only. The feed-agnostic consumer `lab/validation/sweep/feed_loader.py:load_bar_feed` is unchanged. A new `core/bar_export_loader.py` decodes the TV List-of-Trades export (one reversal order per bar, OHLCV encoded in the Signal field) into the canonical bar CSV schema. The Dukascopy adapter + its test + Q-FEED-1's panel fetcher are deleted; five closed-investigation scripts that import the adapter get frozen-artifact banners; governance is recorded in a new ADR that supersedes/withdraws two 2026-06-12 ADRs and closes Q-FEED-1.

**Tech Stack:** Python 3, pandas, pytest. Repo conventions: `pyproject.toml` `testpaths=['tests']` + `pythonpath` adds `core/`, `lab/`, `ops/` (so `from bar_export_loader import …` and `from validation.sweep.feed_loader import …` resolve in tests). Boundary contract enforced by `scripts/check_boundaries.py` (`tests/` exempt; `core→core` legal). Vendor-data integrity by `scripts/check_data_manifests.py` + the `scripts/githooks/pre-commit` hash gate.

**Spec:** `docs/spec/2026-06-17-dukascopy-retirement-design.md`

---

### Task 0: Commit the design artifacts

**Files:**
- Commit: `docs/spec/2026-06-17-dukascopy-retirement-design.md`, `docs/spec/2026-06-17-dukascopy-retirement-plan.md`

- [ ] **Step 1: Stage and commit the spec + plan**

```bash
git add docs/spec/2026-06-17-dukascopy-retirement-design.md docs/spec/2026-06-17-dukascopy-retirement-plan.md
git commit -m "docs(spec): dukascopy retirement design + implementation plan

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

Expected: clean commit (no data trees touched → pre-commit manifest hook is a no-op).

---

### Task 1: Add GBPUSD to the shared price-column map

The new loader imports `PRICE_COL_BY_INSTRUMENT` from `core/tv_export_loader.py` (single source of truth — never fork the map). It already covers USDJPY/XAUUSD/XAGUSD/US30/US30USD/NAS100; GBPUSD (needed by the existing on-disk samples) is missing.

**Files:**
- Modify: `core/tv_export_loader.py:31-38`

- [ ] **Step 1: Add the GBPUSD entry**

In `core/tv_export_loader.py`, change the map from:

```python
PRICE_COL_BY_INSTRUMENT = {
    "USDJPY":  "Price JPY",
    "XAUUSD":  "Price USD",
    "XAGUSD":  "Price USD",
    "US30USD": "Price USD",
    "US30":    "Price USD",
    "NAS100":  "Price USD",
}
```

to:

```python
# Shared by core/tv_export_loader.py (trades) and core/bar_export_loader.py (bars).
# Both the decode contract (which price the cross-check reads) and the load contract
# (which Entry/Exit column exists). Extend here when a new symbol's TV export lands;
# never duplicate this map in the bars loader.
PRICE_COL_BY_INSTRUMENT = {
    "USDJPY":  "Price JPY",
    "GBPUSD":  "Price USD",
    "XAUUSD":  "Price USD",
    "XAGUSD":  "Price USD",
    "US30USD": "Price USD",
    "US30":    "Price USD",
    "NAS100":  "Price USD",
}
```

- [ ] **Step 2: Verify the trade-export tests still pass**

Run: `python -m pytest tests/test_tv_export_loader.py -q`
Expected: PASS (additive change; existing assertions untouched).

- [ ] **Step 3: Commit**

```bash
git add core/tv_export_loader.py
git commit -m "feat(core): add GBPUSD to shared PRICE_COL_BY_INSTRUMENT

Shared by the trades loader and the new bar-export loader (single source of truth).

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 2: `core/bar_export_loader.py` — decode functions (TDD)

**Files:**
- Create: `core/bar_export_loader.py`
- Test: `tests/test_bar_export_loader.py`

- [ ] **Step 1: Write the failing decode tests**

Create `tests/test_bar_export_loader.py`:

```python
"""Tests for core/bar_export_loader.py (BAR EXPORT v0.1 producer)."""
import pandas as pd
import pytest

from bar_export_loader import decode_bar_signal


def test_decode_bar_signal_pipe():
    enc = decode_bar_signal("1772409600000|156.64|156.806|156.572|156.574|3915")
    assert enc["epoch_ms"] == 1772409600000.0
    assert enc["o"] == 156.64
    assert enc["h"] == 156.806
    assert enc["l"] == 156.572
    assert enc["c"] == 156.574
    assert enc["v"] == 3915.0


def test_decode_bar_signal_legacy_comment():
    enc = decode_bar_signal("BAR|o=1.25|h=1.26|l=1.24|c=1.255|v=100")
    assert "epoch_ms" not in enc
    assert enc["o"] == 1.25
    assert enc["c"] == 1.255
    assert enc["v"] == 100.0


def test_decode_bar_signal_rejects_garbage():
    with pytest.raises(ValueError):
        decode_bar_signal("not a bar signal")
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest tests/test_bar_export_loader.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'bar_export_loader'`.

- [ ] **Step 3: Create the module with decode functions**

Create `core/bar_export_loader.py`:

```python
"""BAR EXPORT v0.1 producer — TradingView/Pepperstone broker-feed bars.

Canonical producer of ``core/data/bar_data/<SYMBOL>_M15.csv`` (the schema consumed by
``validation.sweep.feed_loader.load_bar_feed``). Replaces the retired Dukascopy adapter
(``docs/adr/2026-06-17-dukascopy-retirement.md``).

Mechanism (BAR EXPORT v0.1): a Pine strategy places one reversal order per confirmed M15
bar, encoding the bar's OHLCV in the order Signal field as
``{epoch_ms}|{open}|{high}|{low}|{close}|{volume}``. The TV List-of-Trades CSV is the
transport. ``epoch_ms`` is bar-open UTC (authoritative over the CSV ``Date and time``
column, avoiding chart-TZ ambiguity). The Entry ``Price`` equals the encoded ``close``
(``process_orders_on_close``); a mismatch is a hard fail = TV-export format-drift detector.

Output schema is ``feed_loader.REQUIRED_COLUMNS``-compliant by construction: columns
``time,open,high,low,close,volume`` with ``time`` ISO-8601 UTC ``Z``, float OHLC, int volume.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Sequence

import pandas as pd

from tv_export_loader import PRICE_COL_BY_INSTRUMENT

# Deployed BAR EXPORT v0.1: Signal = epoch_ms|open|high|low|close|volume
SIGNAL_PIPE_RE = re.compile(
    r"^(?P<epoch>\d+)\|(?P<o>[-\d.]+)\|(?P<h>[-\d.]+)\|(?P<l>[-\d.]+)\|(?P<c>[-\d.]+)\|(?P<v>\d+)$"
)
# Legacy comment-keyed format (lab Pine stub): BAR|o=..|h=..|l=..|c=..|v=..
COMMENT_RE = re.compile(
    r"^BAR\|o=(?P<o>[-\d.]+)\|h=(?P<h>[-\d.]+)\|l=(?P<l>[-\d.]+)\|c=(?P<c>[-\d.]+)\|v=(?P<v>\d+)$"
)


def decode_bar_signal(signal: str) -> dict[str, float]:
    """Decode a BAR EXPORT v0.1 Signal field (pipe-format preferred, legacy comment supported)."""
    text = str(signal).strip()
    m = SIGNAL_PIPE_RE.match(text)
    if m:
        return {
            "epoch_ms": float(m.group("epoch")),
            "o": float(m.group("o")),
            "h": float(m.group("h")),
            "l": float(m.group("l")),
            "c": float(m.group("c")),
            "v": float(m.group("v")),
        }
    m = COMMENT_RE.match(text)
    if m:
        return {k: float(m.group(k)) for k in ("o", "h", "l", "c", "v")}
    raise ValueError(f"BAR EXPORT signal decode fail: {text!r}")


def price_tolerance(symbol: str, price: float) -> float:
    """Per-symbol absolute tolerance for the Entry-price == encoded-close cross-check."""
    if symbol in ("US30", "US30USD"):
        return max(0.5, price * 1e-4)
    if "JPY" in symbol:
        return max(0.001, price * 1e-4)
    return max(1e-5, price * 1e-4)


def _trade_id_column(df: pd.DataFrame) -> str:
    for col in ("Trade #", "Trade number"):
        if col in df.columns:
            return col
    raise ValueError("TV export missing 'Trade #' / 'Trade number' column")
```

- [ ] **Step 4: Run to verify decode tests pass**

Run: `python -m pytest tests/test_bar_export_loader.py -q`
Expected: PASS (3 tests).

- [ ] **Step 5: Commit**

```bash
git add core/bar_export_loader.py tests/test_bar_export_loader.py
git commit -m "feat(core): bar_export_loader decode functions (BAR EXPORT v0.1)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 3: `parse_bar_export` — single-file parse + cross-check (TDD)

**Files:**
- Modify: `core/bar_export_loader.py`
- Test: `tests/test_bar_export_loader.py`

- [ ] **Step 1: Add the failing parse tests**

Append to `tests/test_bar_export_loader.py`:

```python
from bar_export_loader import parse_bar_export


def _make_tv_csv(path, price_col, rows):
    """rows: list of (trade_num, type, date_and_time, signal, price)."""
    df = pd.DataFrame(rows, columns=["Trade #", "Type", "Date and time", "Signal", price_col])
    df.to_csv(path, index=False, encoding="utf-8-sig")
    return path


def test_parse_bar_export_single(tmp_path):
    rows = [
        (1, "Entry long", "2026-03-02 00:00", "1772409600000|156.64|156.806|156.572|156.574|3915", 156.574),
        (2, "Entry long", "2026-03-02 00:15", "1772410500000|156.57|156.60|156.50|156.58|2000", 156.58),
    ]
    p = _make_tv_csv(tmp_path / "USDJPY_M15_pep.csv", "Price JPY", rows)
    df = parse_bar_export(p, symbol="USDJPY")
    assert list(df.columns) == ["time", "open", "high", "low", "close", "volume"]
    assert len(df) == 2
    assert df.iloc[0]["close"] == 156.574
    assert str(df.iloc[0]["time"]) == "2026-03-02 00:00:00+00:00"  # epoch_ms -> UTC bar-open


def test_parse_bar_export_rejects_price_mismatch(tmp_path):
    rows = [
        (1, "Entry long", "2026-03-02 00:00", "1772409600000|156.64|156.806|156.572|156.574|3915", 999.0),
    ]
    p = _make_tv_csv(tmp_path / "USDJPY_M15_pep.csv", "Price JPY", rows)
    with pytest.raises(ValueError, match="Cross-check fail"):
        parse_bar_export(p, symbol="USDJPY")


def test_parse_bar_export_unknown_symbol(tmp_path):
    rows = [(1, "Entry long", "2026-03-02 00:00", "1772409600000|1|1|1|1|1", 1.0)]
    p = _make_tv_csv(tmp_path / "ZZZ_M15_pep.csv", "Price USD", rows)
    with pytest.raises(ValueError, match="price column"):
        parse_bar_export(p, symbol="ZZZ")
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest tests/test_bar_export_loader.py -q`
Expected: FAIL — `ImportError: cannot import name 'parse_bar_export'`.

- [ ] **Step 3: Implement `_parse_one` + `parse_bar_export`**

Append to `core/bar_export_loader.py`:

```python
def _parse_one(path: Path, *, symbol: str) -> pd.DataFrame:
    """Decode one BAR EXPORT v0.1 List-of-Trades CSV into time/OHLCV rows."""
    raw = pd.read_csv(path, encoding="utf-8-sig")
    raw.columns = [str(c).strip() for c in raw.columns]
    if "Date and time" not in raw.columns:
        raise ValueError(f"TV export missing 'Date and time' column: {path}")

    price_col = PRICE_COL_BY_INSTRUMENT.get(symbol)
    if price_col is None:
        raise ValueError(
            f"No price column for symbol {symbol!r}; add it to "
            f"PRICE_COL_BY_INSTRUMENT in core/tv_export_loader.py."
        )
    if price_col not in raw.columns:
        raise ValueError(f"TV export missing price column {price_col!r} for {symbol}: {path}")

    trade_col = _trade_id_column(raw)
    entries = raw[raw["Type"].astype(str).str.startswith("Entry")].copy()
    entries = entries.sort_values(trade_col).reset_index(drop=True)

    rows: list[dict] = []
    skipped = 0
    for i in range(len(entries)):
        row = entries.iloc[i]
        signal = row.get("Signal", row.get("Comment", ""))
        try:
            enc = decode_bar_signal(signal)
        except ValueError:
            skipped += 1
            continue
        entry_px = float(row[price_col])
        tol = price_tolerance(symbol, enc["c"])
        if abs(entry_px - enc["c"]) > tol:
            raise ValueError(
                f"Cross-check fail {path} trade {row[trade_col]}: "
                f"entry px {entry_px} vs encoded close {enc['c']}"
            )
        if "epoch_ms" in enc:
            ts = pd.to_datetime(int(enc["epoch_ms"]), unit="ms", utc=True)
        else:
            ts = pd.to_datetime(row["Date and time"], utc=True)
        rows.append({
            "time": ts,
            "open": enc["o"],
            "high": enc["h"],
            "low": enc["l"],
            "close": enc["c"],
            "volume": int(enc["v"]),
        })

    if skipped:
        print(
            f"=== parse_bar_export: skipped {skipped} entry rows without decodable signal in {path} ===",
            file=sys.stderr,
        )
    if not rows:
        raise ValueError(f"No decodable bars in {path}")
    return pd.DataFrame(rows)


def parse_bar_export(paths: str | Path | Sequence[str | Path], *, symbol: str) -> pd.DataFrame:
    """Decode one or more BAR EXPORT v0.1 page CSVs into a single OHLCV bar DataFrame.

    Multi-page: TV caps the List-of-Trades export at ~9,000 bars. For windows beyond
    that, pass a list of page CSVs; pages are concatenated, deduplicated on bar-open
    ``time`` (``keep='last'`` — prefer the later re-export), and sorted.
    """
    if isinstance(paths, (str, Path)):
        paths = [paths]
    frames = [_parse_one(Path(p), symbol=symbol) for p in paths]
    df = pd.concat(frames, ignore_index=True)
    df = (
        df.sort_values("time")
        .drop_duplicates(subset="time", keep="last")
        .reset_index(drop=True)
    )
    return df
```

- [ ] **Step 4: Run to verify parse tests pass**

Run: `python -m pytest tests/test_bar_export_loader.py -q`
Expected: PASS (6 tests total).

- [ ] **Step 5: Commit**

```bash
git add core/bar_export_loader.py tests/test_bar_export_loader.py
git commit -m "feat(core): parse_bar_export single-file parse + cross-check

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 4: Multi-page dedup + `write_bar_data` + feed_loader round-trip (TDD)

**Files:**
- Modify: `core/bar_export_loader.py`
- Test: `tests/test_bar_export_loader.py`

- [ ] **Step 1: Add the failing multi-page + round-trip tests**

Append to `tests/test_bar_export_loader.py`:

```python
from bar_export_loader import write_bar_data


def test_parse_bar_export_multipage_dedup(tmp_path):
    rows_a = [
        (1, "Entry long", "2026-03-02 00:00", "1772409600000|156.64|156.806|156.572|156.574|3915", 156.574),
        (2, "Entry long", "2026-03-02 00:15", "1772410500000|156.57|156.60|156.50|156.58|2000", 156.58),
    ]
    rows_b = [  # page B re-exports the 00:15 bar (different close) and adds 00:30
        (1, "Entry long", "2026-03-02 00:15", "1772410500000|156.57|156.60|156.50|156.99|2222", 156.99),
        (2, "Entry long", "2026-03-02 00:30", "1772411400000|156.99|157.00|156.90|156.95|1500", 156.95),
    ]
    pa = _make_tv_csv(tmp_path / "pageA.csv", "Price JPY", rows_a)
    pb = _make_tv_csv(tmp_path / "pageB.csv", "Price JPY", rows_b)
    df = parse_bar_export([pa, pb], symbol="USDJPY")
    assert len(df) == 3  # 00:00, 00:15 (deduped), 00:30
    bar_0015 = df[df["time"] == pd.Timestamp("2026-03-02 00:15", tz="UTC")]
    assert bar_0015.iloc[0]["close"] == 156.99  # keep='last' -> page B


def test_write_bar_data_and_feed_loader_round_trip(tmp_path):
    rows = [
        (1, "Entry long", "2026-03-02 00:00", "1772409600000|156.64|156.806|156.572|156.574|3915", 156.574),
        (2, "Entry long", "2026-03-02 00:15", "1772410500000|156.57|156.60|156.50|156.58|2000", 156.58),
    ]
    p = _make_tv_csv(tmp_path / "USDJPY_M15_pep.csv", "Price JPY", rows)
    df = parse_bar_export(p, symbol="USDJPY")
    out = write_bar_data(df, symbol="USDJPY", out_dir=tmp_path)
    assert out.name == "USDJPY_M15.csv"

    # Header is ISO-8601 'Z'; load through the unchanged sweep consumer.
    written = out.read_text(encoding="utf-8").splitlines()
    assert written[0] == "time,open,high,low,close,volume"
    assert written[1].startswith("2026-03-02T00:00:00Z,")

    from validation.sweep.feed_loader import load_bar_feed
    feed = load_bar_feed(out, symbol="USDJPY")
    assert feed.symbol == "USDJPY"
    assert len(feed.close) == 2
    assert feed.close[0] == 156.574
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest tests/test_bar_export_loader.py -q`
Expected: FAIL — `ImportError: cannot import name 'write_bar_data'` (the multi-page test will pass already; the round-trip fails on import).

- [ ] **Step 3: Implement `write_bar_data`**

Append to `core/bar_export_loader.py`:

```python
DEFAULT_BAR_DIR = Path(__file__).resolve().parent / "data" / "bar_data"


def write_bar_data(df: pd.DataFrame, *, symbol: str, out_dir: str | Path | None = None) -> Path:
    """Write the canonical ``core/data/bar_data/<SYMBOL>_M15.csv`` (feed_loader schema)."""
    target_dir = Path(out_dir) if out_dir is not None else DEFAULT_BAR_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    out_path = target_dir / f"{symbol}_M15.csv"

    out = df.copy()
    out["time"] = pd.to_datetime(out["time"], utc=True).dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    out = out[["time", "open", "high", "low", "close", "volume"]]
    out.to_csv(out_path, index=False)
    return out_path
```

- [ ] **Step 4: Run to verify all tests pass**

Run: `python -m pytest tests/test_bar_export_loader.py -q`
Expected: PASS (8 tests total).

- [ ] **Step 5: Confirm boundary contract holds**

Run: `python scripts/check_boundaries.py`
Expected: PASS — `core/bar_export_loader.py` imports only `core`-layer (`tv_export_loader`) + stdlib/pandas.

- [ ] **Step 6: Commit**

```bash
git add core/bar_export_loader.py tests/test_bar_export_loader.py
git commit -m "feat(core): multi-page dedup + write_bar_data + feed_loader round-trip

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 5: `scripts/parse_bar_export.py` CLI

**Files:**
- Create: `scripts/parse_bar_export.py`
- Test: `tests/test_parse_bar_export_cli.py`

- [ ] **Step 1: Write the failing CLI test**

Create `tests/test_parse_bar_export_cli.py`:

```python
"""Smoke test for scripts/parse_bar_export.py."""
import subprocess
import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI = REPO_ROOT / "scripts" / "parse_bar_export.py"


def _make_tv_csv(path, rows):
    df = pd.DataFrame(rows, columns=["Trade #", "Type", "Date and time", "Signal", "Price JPY"])
    df.to_csv(path, index=False, encoding="utf-8-sig")


def test_cli_parses_to_bar_data(tmp_path):
    src = tmp_path / "USDJPY_M15_pep.csv"
    _make_tv_csv(src, [
        (1, "Entry long", "2026-03-02 00:00", "1772409600000|156.64|156.806|156.572|156.574|3915", 156.574),
        (2, "Entry long", "2026-03-02 00:15", "1772410500000|156.57|156.60|156.50|156.58|2000", 156.58),
    ])
    out = tmp_path / "USDJPY_M15.csv"
    result = subprocess.run(
        [sys.executable, str(CLI), "--symbol", "USDJPY", "--in", str(src), "--out", str(out)],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    assert out.exists()
    lines = out.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "time,open,high,low,close,volume"
    assert len(lines) == 3  # header + 2 bars
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest tests/test_parse_bar_export_cli.py -q`
Expected: FAIL — CLI file does not exist (non-zero return; assertion on `out.exists()`).

- [ ] **Step 3: Create the CLI**

Create `scripts/parse_bar_export.py`:

```python
#!/usr/bin/env python3
"""Parse BAR EXPORT v0.1 List-of-Trades CSV(s) into core/data/bar_data/<SYMBOL>_M15.csv.

Usage:
    python scripts/parse_bar_export.py --symbol USDJPY
    python scripts/parse_bar_export.py --symbol USDJPY --in pageA.csv pageB.csv
    python scripts/parse_bar_export.py --symbol USDJPY --in raw.csv --out /tmp/USDJPY_M15.csv

After landing vendor bytes, regenerate manifests:
    python scripts/check_data_manifests.py --regenerate
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "core"))

from bar_export_loader import DEFAULT_BAR_DIR, parse_bar_export, write_bar_data  # noqa: E402

DEFAULT_EXPORT_DIR = REPO_ROOT / "core" / "data" / "tv_exports" / "pepperstone" / "bar_export"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Parse BAR EXPORT v0.1 CSV(s) to a canonical bar CSV.")
    ap.add_argument("--symbol", required=True, help="e.g. USDJPY, GBPUSD, US30, XAUUSD, NAS100")
    ap.add_argument(
        "--in", dest="in_paths", nargs="+", default=None,
        help="Input List-of-Trades CSV page(s). Default: "
             "core/data/tv_exports/pepperstone/bar_export/<SYMBOL>_M15_pep.csv",
    )
    ap.add_argument("--out", default=None, help="Output CSV (default: core/data/bar_data/<SYMBOL>_M15.csv)")
    a = ap.parse_args(argv)

    if a.in_paths:
        in_paths = [Path(p) for p in a.in_paths]
    else:
        in_paths = [DEFAULT_EXPORT_DIR / f"{a.symbol}_M15_pep.csv"]

    missing = [p for p in in_paths if not p.exists()]
    if missing:
        for p in missing:
            print(f"=== missing TV export: {p} ===", file=sys.stderr)
        return 2

    df = parse_bar_export(in_paths, symbol=a.symbol)

    if a.out:
        out_path = Path(a.out)
        out_path = write_bar_data(df, symbol=a.symbol, out_dir=out_path.parent)
        if out_path.name != Path(a.out).name:
            out_path.replace(Path(a.out))
            out_path = Path(a.out)
    else:
        out_path = write_bar_data(df, symbol=a.symbol, out_dir=DEFAULT_BAR_DIR)

    print(f"=== parsed {len(df)} bars from {len(in_paths)} page(s) -> {out_path} ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run to verify the CLI test passes**

Run: `python -m pytest tests/test_parse_bar_export_cli.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/parse_bar_export.py tests/test_parse_bar_export_cli.py
git commit -m "feat(scripts): parse_bar_export CLI (bar-export -> bar_data)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 6: Delete the Dukascopy adapter + test + Q-FEED-1 fetcher

**Files:**
- Delete: `core/lib/dukascopy.py`
- Delete: `tests/test_dukascopy.py`
- Delete: `lab/archive/feed_divergence_2026-06/fetch_duka_panels.py`

- [ ] **Step 1: Delete the three files**

```bash
git rm core/lib/dukascopy.py tests/test_dukascopy.py lab/archive/feed_divergence_2026-06/fetch_duka_panels.py
```

- [ ] **Step 2: Verify no live import breaks**

Run: `python scripts/check_boundaries.py`
Expected: PASS (no module references a deleted `core/lib/dukascopy`).

Run: `python -m pytest tests/ -q`
Expected: PASS — `test_dukascopy.py` is gone; verification confirmed it was the only test importing the adapter, and `lab/analysis/` is never collected (`testpaths=['tests']`).

- [ ] **Step 3: Confirm `measure_divergence.py` was NOT removed**

Run: `git status --porcelain lab/archive/feed_divergence_2026-06/measure_divergence.py`
Expected: empty output (file untouched — it has no Dukascopy import).

- [ ] **Step 4: Commit**

```bash
git commit -m "refactor: delete Dukascopy adapter, its test, and Q-FEED-1 panel fetcher

Retired per docs/spec/2026-06-17-dukascopy-retirement-design.md.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 7: Frozen-artifact banners on closed-Q scripts

Add the banner as the **first line** of each file (above the existing shebang/docstring). Five verified live-import scripts + the feed_divergence README.

**Files:**
- Modify: `lab/archive/noct_spx/fetch_panel.py`
- Modify: `lab/analysis/tom_spx/fetch_daily.py`
- Modify: `lab/archive/custodian_eurusd/fetch_panel.py`
- Modify: `lab/analysis/silver_regime_2026-06-10/dukascopy_runner_check.py`
- Modify: `lab/analysis/silver_regime_2026-06-10/dukascopy_feed_equiv.py`
- Modify: `lab/archive/feed_divergence_2026-06/README.md`

- [ ] **Step 1: Add the Python banner to each of the 5 scripts**

Insert as the very first line of each `.py` file:

```python
# Dukascopy retired 2026-06-17 (docs/adr/2026-06-17-dukascopy-retirement.md) — frozen historical artifact; no longer runs.
```

(Place it above any shebang/`from __future__` line; a leading comment line is valid before `from __future__` imports only if no code precedes — to be safe, place it immediately after a shebang if present, otherwise as line 1. For files starting with `from __future__ import annotations`, put the banner on line 1 and keep `from __future__` as the first *statement*.)

- [ ] **Step 2: Add a banner to the feed_divergence README**

At the top of `lab/archive/feed_divergence_2026-06/README.md`, add:

```markdown
> **FROZEN 2026-06-17** — Dukascopy retired (`docs/adr/2026-06-17-dukascopy-retirement.md`). This Q-FEED-1 directory is a historical record; `fetch_duka_panels.py` was deleted, `measure_divergence.py` / `_lib.py` remain as the frozen analysis artifact and no longer run.
```

- [ ] **Step 3: Verify tests + boundaries still clean**

Run: `python scripts/check_boundaries.py && python -m pytest tests/ -q`
Expected: PASS (banners are comments; no behavior change; lab not collected).

- [ ] **Step 4: Commit**

```bash
git add lab/archive/noct_spx/fetch_panel.py lab/analysis/tom_spx/fetch_daily.py \
        lab/archive/custodian_eurusd/fetch_panel.py \
        lab/analysis/silver_regime_2026-06-10/dukascopy_runner_check.py \
        lab/analysis/silver_regime_2026-06-10/dukascopy_feed_equiv.py \
        lab/archive/feed_divergence_2026-06/README.md
git commit -m "docs: frozen-artifact banners on closed-Q Dukascopy scripts

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 8: Manifest gate — govern the bar_export input dir

> **Worktree note (2026-06-17):** this worktree is a fresh-clone w.r.t. vendor data — `bar_export/` and all `*.csv` are gitignored and absent here. So `--regenerate` creates an **empty** `bar_export/SHA256SUMS` (legitimate per the checker), and the `.bars.csv` deletion (Step 2) is a **main-working-copy** action (no-op here). The empty seeded manifest is what makes `make validate` pass in the worktree once `bar_export` is added to `MANIFEST_DIRS`; the real hashes are populated in the main copy (Task 9).

**Files:**
- Modify: `scripts/check_data_manifests.py:29-34` (MANIFEST_DIRS)
- Resolve (main copy only): the 3 stale `*_M15_pep.bars.csv` intermediates in `core/data/tv_exports/pepperstone/bar_export/`
- Create (via --regenerate): `core/data/tv_exports/pepperstone/bar_export/SHA256SUMS` (empty in the worktree)

- [ ] **Step 1: Add bar_export to MANIFEST_DIRS**

In `scripts/check_data_manifests.py`, add the bar_export dir to the `MANIFEST_DIRS` list (keep the existing four). Example shape (match the file's actual `REPO_ROOT` variable and list style):

```python
MANIFEST_DIRS = [
    REPO_ROOT / "core" / "data" / "tv_exports" / "pepperstone",
    REPO_ROOT / "core" / "data" / "tv_exports" / "pepperstone" / "bar_export",
    REPO_ROOT / "core" / "data" / "tv_exports" / "oanda",
    REPO_ROOT / "core" / "data" / "bar_data",
    REPO_ROOT / "core" / "data" / "external",
]
```

- [ ] **Step 2: Retire the stale `.bars.csv` intermediates**

The producer now writes canonical output to `bar_data/`, so the `.bars.csv` siblings in `bar_export/` are obsolete. Remove them so the new manifest pins only raw inputs:

```bash
rm core/data/tv_exports/pepperstone/bar_export/GBPUSD_M15_pep.bars.csv \
   core/data/tv_exports/pepperstone/bar_export/US30_M15_pep.bars.csv \
   core/data/tv_exports/pepperstone/bar_export/USDJPY_M15_pep.bars.csv
```

(These are gitignored vendor bytes, so this is a working-tree cleanup, not a tracked delete.)

- [ ] **Step 3: Dry-run then regenerate manifests**

Run: `python scripts/check_data_manifests.py --regenerate --dry-run`
Expected: shows a new `bar_export/SHA256SUMS` with the 3 `*_M15_pep.csv` raw inputs; no errors.

Run: `python scripts/check_data_manifests.py --regenerate`
Expected: writes `core/data/tv_exports/pepperstone/bar_export/SHA256SUMS`.

- [ ] **Step 4: Verify the full gate**

Run: `python scripts/check_data_manifests.py`
Expected: PASS (all manifest dirs consistent).

- [ ] **Step 5: Commit (data + manifest together, per the pre-commit hook)**

```bash
git add scripts/check_data_manifests.py core/data/tv_exports/pepperstone/bar_export/SHA256SUMS
git commit -m "feat(manifest): govern bar_export input dir under the M-9 hash gate

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

Expected: pre-commit hook passes (manifest now present for bar_export).

---

### Task 9: Produce canonical bar_data for the 3 existing sample symbols (acceptance)

> **Runs in the MAIN working copy (`C:\Users\joshu\multi_firm_operations\`), not the worktree** — it needs the gitignored sample CSVs that exist only there, and the new `core/bar_export_loader.py` + `scripts/parse_bar_export.py` (so run it after this branch is checked out / merged into the main copy). In the worktree, the producer is exercised only by the synthetic tests (Tasks 2–5) + the verification-pass round-trip already validated against the real `USDJPY_M15_pep.bars.csv` bytes. This task is an **operator step**, recorded here with exact commands; it is NOT executed during the worktree implementation.

This demonstrates the producer end-to-end and lands the first canonical bar-export outputs. Vendor `*.csv` bytes are gitignored; only the `bar_data/SHA256SUMS` delta is tracked.

**Files:**
- Create (vendor, gitignored): `core/data/bar_data/{USDJPY,GBPUSD,US30}_M15.csv`
- Modify (via --regenerate): `core/data/bar_data/SHA256SUMS`

- [ ] **Step 1: Run the producer for each sample symbol**

```bash
python scripts/parse_bar_export.py --symbol USDJPY
python scripts/parse_bar_export.py --symbol GBPUSD
python scripts/parse_bar_export.py --symbol US30
```

Expected: each prints `=== parsed N bars from 1 page(s) -> .../bar_data/<SYMBOL>_M15.csv ===` (N ≈ 6,000+ for the 2026-03→06 window).

- [ ] **Step 2: Confirm the outputs load through the sweep consumer**

```bash
python -c "import sys; sys.path.insert(0,'lab'); from validation.sweep.feed_loader import load_bar_feed; \
[print(s, len(load_bar_feed(f'core/data/bar_data/{s}_M15.csv', symbol=s).close)) for s in ('USDJPY','GBPUSD','US30')]"
```

Expected: three lines, each with a positive bar count, no exception.

- [ ] **Step 3: Regenerate + verify manifests**

Run: `python scripts/check_data_manifests.py --regenerate && python scripts/check_data_manifests.py`
Expected: `bar_data/SHA256SUMS` gains `USDJPY_M15.csv`, `GBPUSD_M15.csv`, `US30_M15.csv` lines; gate PASS. (Existing `*_duka.csv` / `*_oanda.csv` lines untouched.)

- [ ] **Step 4: Commit the manifest delta**

```bash
git add core/data/bar_data/SHA256SUMS
git commit -m "data: canonical bar-export outputs for USDJPY/GBPUSD/US30

First bar_data produced by the BAR EXPORT v0.1 pipeline (vendor CSVs gitignored).

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 10: Governance — retirement ADR + dispositions

Author via the **brief-authoring** skill (ADR type). This is the load-bearing governance record (spec §2).

**Files:**
- Create: `docs/adr/2026-06-17-dukascopy-retirement.md`
- Modify: `docs/adr/2026-06-12-tv-csv-canonical-feed-policy.md` (supersession header note)
- Modify: `docs/adr/2026-06-12-rnd-feed-instrument-class-split.md` (status → Withdrawn/Superseded)
- Modify: `docs/ltm/briefs/Q-FEED-1-dukascopy-tv-feed-divergence.md` (status → CLOSED)
- Modify: `docs/ltm/briefs/pre-registration/Q-FEED-1-verdict-preregistration.md` (moot note)

- [ ] **Step 1: Author `docs/adr/2026-06-17-dukascopy-retirement.md`**

Use brief-authoring (ADR). Required content:
- **Status:** Accepted (operator executive decision, recorded). **Date:** 2026-06-17.
- **§0 Rule-0 reads:** the files in spec §0 (cite anchors via `git log -1 --format='%h' -- <file>`).
- **§1 Context:** retirement of the Dukascopy bar adapter; canonical bars now from BAR EXPORT v0.1 (broker-feed via TV); operator grounds = interpretability + broker-execution fidelity.
- **§2 Decision:** (a) delete the adapter + test + Q-FEED-1 fetcher; (b) `core/bar_export_loader.py` is the canonical bar producer; (c) the 5 closed-Q scripts are frozen with banners; (d) cached `*_duka.csv` and OANDA tooling out of scope.
- **§3 Supersession:** explicitly supersede `2026-06-12-tv-csv-canonical-feed-policy.md` §2.3 + §4#3 (retention/don't-delete), and withdraw `2026-06-12-rnd-feed-instrument-class-split.md` (PROPOSED, gated on Q-FEED-1). Note this is an operator override of that ADR's §3(A) ruled-out alternative + §5 forbidden move.
- **§4 Recorded cost + falsifier:** deep multi-year FX/metals history becomes manual/plan-capped/multi-pass (the rnd-feed §3(A) cost). Accepted mitigation: operator-supplied multi-page exports (producer concatenates). Falsifier: if a pre-registered deep-history FX/metals gate (N≥100 or regime-robustness half-panel) can't be assembled from operator exports within a working session, reopen the programmatic-feed question with that dated incident; supersede, never edit §4 in place.
- **§5 Forbidden moves:** re-introducing a programmatic bar feed by convention without an ADR; citing the retired adapter's cached bars as canonical-fresh; editing the falsifier in place.
- **§10 Audit hooks:** `grep -rin dukascopy` returns only banners + frozen records + this ADR; `python scripts/check_boundaries.py`; `make validate`.

- [ ] **Step 2: Disposition the two 2026-06-12 ADRs + Q-FEED-1**

- In `docs/adr/2026-06-12-tv-csv-canonical-feed-policy.md`: add a header note under **Status** — `§2.3 + §4 Forbidden-move #3 SUPERSEDED 2026-06-17 by docs/adr/2026-06-17-dukascopy-retirement.md`. Do not edit §4 body in place; annotate only.
- In `docs/adr/2026-06-12-rnd-feed-instrument-class-split.md`: change `**Status:** Proposed …` to `**Status:** Withdrawn/Superseded 2026-06-17 by docs/adr/2026-06-17-dukascopy-retirement.md (premise mooted by Dukascopy retirement; Q-FEED-1 closed)`. Add a change-history line.
- In `docs/ltm/briefs/Q-FEED-1-dukascopy-tv-feed-divergence.md`: change status line to `CLOSED — RESOLVED-BY-RETIREMENT (2026-06-17)`; add a closing paragraph: cross-feed transfer-validity dissolves; link the retirement ADR.
- In `docs/ltm/briefs/pre-registration/Q-FEED-1-verdict-preregistration.md`: add a top note — pre-registration moot (Q-FEED-1 closed by retirement 2026-06-17).

- [ ] **Step 3: Validate ADR discipline**

Run: `python scripts/check_brief.py docs/adr/2026-06-17-dukascopy-retirement.md --type adr`
Expected: all checks PASS.

- [ ] **Step 4: Commit**

```bash
git add docs/adr/2026-06-17-dukascopy-retirement.md \
        docs/adr/2026-06-12-tv-csv-canonical-feed-policy.md \
        docs/adr/2026-06-12-rnd-feed-instrument-class-split.md \
        docs/ltm/briefs/Q-FEED-1-dukascopy-tv-feed-divergence.md \
        docs/ltm/briefs/pre-registration/Q-FEED-1-verdict-preregistration.md
git commit -m "governance(dukascopy): retirement ADR; supersede/withdraw 2026-06-12 ADRs; close Q-FEED-1

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 11: Doc + memory updates

**Files:**
- Modify: `CLAUDE.md` (Public-clone posture; any Dukascopy-feed framing)
- Modify: `REPO_MAP.md` (data-sources note)
- Modify: `docs/SESSIONS.md` (reverse-chron entry)
- Modify memory: `C:\Users\joshu\.claude\projects\C--Users-joshu-multi-firm-operations\memory\reference_dukascopy_adapter.md`, `project_tv_csv_canonical_feed_policy.md`, `project_rnd_pipeline_state.md`, and `MEMORY.md` index

- [ ] **Step 1: Update CLAUDE.md**

In the **Public-clone posture** / vendor-data section: name `core/data/tv_exports/pepperstone/bar_export/` as a manifest dir, and add a short "Bar-data restoration" note: for the Pepperstone feed, `bar_data/<SYMBOL>_M15.csv` is produced by `python scripts/parse_bar_export.py --symbol <SYMBOL>` from a BAR EXPORT v0.1 List-of-Trades CSV (replaces the retired Dukascopy fetch; OANDA still via `scripts/fetch_oanda_bars.py`). Remove/relabel any line presenting Dukascopy as a live feed source. Cite `docs/adr/2026-06-17-dukascopy-retirement.md`.

- [ ] **Step 2: Update REPO_MAP.md**

Add a one-line data-sources note: `core/data/bar_data/` = BAR EXPORT v0.1 producer output (canonical) + historical `*_duka.csv` / `*_oanda.csv` (manifest-pinned). Cross-link the retirement ADR.

- [ ] **Step 3: Add a SESSIONS.md entry**

Prepend a reverse-chron entry (5 fields per the session-log discipline): date 2026-06-17, what (Dukascopy retired; bar_export_loader canonical; ADR + dispositions; Q-FEED-1 closed), result, open/next.

- [ ] **Step 4: Update memory files**

- `reference_dukascopy_adapter.md`: rewrite to record the adapter was retired 2026-06-17; point to `core/bar_export_loader.py` + the retirement ADR. (Or delete and create `reference_bar_export_producer.md`; update the `MEMORY.md` index line either way.)
- `project_tv_csv_canonical_feed_policy.md` + `project_rnd_pipeline_state.md`: note Dukascopy fully retired; bar-export #1 canonical; class-split ADR withdrawn.

- [ ] **Step 5: Commit (CLAUDE.md / REPO_MAP / SESSIONS only — memory is outside the repo)**

```bash
git add CLAUDE.md REPO_MAP.md docs/SESSIONS.md
git commit -m "docs: retire Dukascopy in CLAUDE.md/REPO_MAP/SESSIONS; bar-export canonical

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 12: Final verification gate

**Files:** none (verification only)

- [ ] **Step 1: Full validate**

Run: `make validate`
Expected: params + data manifests + pine manifest all PASS (incl. the new bar_export manifest entry).

- [ ] **Step 2: Boundary + full test suite**

Run: `python scripts/check_boundaries.py && python -m pytest tests/ -q`
Expected: both PASS; `test_bar_export_loader.py` + `test_parse_bar_export_cli.py` green; no `test_dukascopy.py`.

- [ ] **Step 3: Grep sweep — no live Dukascopy code remains**

Run: `grep -rin dukascopy --include=*.py .`
Expected: only the 5 frozen-artifact banners + `measure_divergence.py`/`_lib.py` (frozen Q-FEED-1) + closed-Q script bodies. **No live import of a deleted `core/lib/dukascopy`.**

Run: `grep -rin "core/lib/dukascopy\|from lib import dukascopy\|from lib.dukascopy" --include=*.py . | grep -v "^./lab/analysis"`
Expected: empty (no live importer outside frozen lab dirs).

- [ ] **Step 4: Report results**

Summarize: tests green, boundaries clean, manifests consistent, governance recorded, grep sweep clean. Note anything skipped (e.g. real-CSV cases that skip on a fresh clone).

---

## Self-Review

**Spec coverage:** §2 governance → Task 10. §3 architecture (producer swap) → Tasks 2-5,9. §4 new module → Tasks 2-4 (incl. shared PRICE_COL Task 1, multi-page, filename contract, cross-check). §5 CLI → Task 5. §6 deletions → Task 6. §7 banners → Task 7. §8 manifest → Task 8. §9 doc updates → Tasks 10-11. §10 tests → Tasks 2-5. §11 verification gate → Task 12. §13 open items: `.bars.csv` resolved (Task 8 deletes intermediates); EURUSD deferred (no task — correct, no sample). All covered.

**Placeholder scan:** ADR prose (Task 10) is authored via brief-authoring with concrete required-content bullets, not a placeholder. All code steps show complete code. No TBD/TODO.

**Type consistency:** `parse_bar_export(paths, *, symbol)`, `write_bar_data(df, *, symbol, out_dir)`, `decode_bar_signal(signal)`, `DEFAULT_BAR_DIR` used consistently across module, CLI, and tests. Output columns `time,open,high,low,close,volume` consistent everywhere. `PRICE_COL_BY_INSTRUMENT` imported from `tv_export_loader` (Task 1) and used in Task 3 — names match.
