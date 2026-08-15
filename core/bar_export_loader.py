"""BAR EXPORT v0.1/v0.2 producer — TradingView/Pepperstone broker-feed bars.

Canonical producer of ``core/data/bar_data/<SYMBOL>_M15.csv`` (the schema consumed by
``validation.sweep.feed_loader.load_bar_feed``). Replaces the retired Dukascopy adapter
(``docs/adr/2026-06-17-dukascopy-retirement.md``).

Mechanism (BAR EXPORT v0.1): a Pine strategy places one reversal order per confirmed M15
bar, encoding the bar's OHLCV in the order Signal field as
``{epoch_ms}|{open}|{high}|{low}|{close}|{volume}``. The TV List-of-Trades CSV is the
transport. ``epoch_ms`` is bar-open UTC (authoritative over the CSV ``Date and time``
column, avoiding chart-TZ ambiguity). The Entry ``Price`` equals the encoded ``close``
(``process_orders_on_close``); a mismatch is a hard fail = TV-export format-drift detector.

BAR EXPORT v0.2 appends per-bar (``time_close|dayofweek|session``) and instrument-constant
(``ticker|type|quoteCcy|baseCcy|mintick|pointvalue|timezone|timeframe``) fields after the
OHLCV prefix. The prefix is byte-compatible with v0.1, so ``decode_bar_signal`` and the
canonical CSV output are unchanged; the metadata is surfaced via ``decode_bar_meta`` /
``parse_bar_export_with_meta`` and persisted to a ``<SYMBOL>_M15.meta.json`` sidecar by
``write_bar_meta``. The appended fields are shape-validated (drift detector extends to them).

Output schema is ``feed_loader.REQUIRED_COLUMNS``-compliant by construction: columns
``time,open,high,low,close,volume`` with ``time`` ISO-8601 UTC ``Z``, float OHLC, int volume.
"""
from __future__ import annotations

import json
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
# BAR EXPORT v0.2: the v0.1 OHLCV prefix + appended per-bar + instrument metadata.
#   epoch|O|H|L|C|V | time_close|dow|sess | ticker|type|qCcy|bCcy|mintick|pointval|tz|tf
# Strict-by-design: the suffix shape is validated, not slurped with `.*`, so the
# field stays a TV-export format-drift detector (module docstring) for the new
# columns too. A malformed v0.2 row matches NEITHER this nor SIGNAL_PIPE_RE and
# is rejected, never silently truncated to its prefix.
SIGNAL_PIPE_V2_RE = re.compile(
    r"^(?P<epoch>\d+)\|(?P<o>[-\d.]+)\|(?P<h>[-\d.]+)\|(?P<l>[-\d.]+)\|(?P<c>[-\d.]+)\|(?P<v>\d+)"
    r"\|(?P<time_close>\d+)\|(?P<dow>[1-7])\|(?P<sess>M|PRE|POST|X)"
    r"\|(?P<ticker>[^|]*)\|(?P<type>[^|]*)\|(?P<quote_ccy>[^|]*)\|(?P<base_ccy>[^|]*)"
    r"\|(?P<mintick>[\d.]+)\|(?P<pointvalue>[\d.]+)\|(?P<tz>[^|]*)\|(?P<tf>[^|]*)$"
)
# Legacy comment-keyed format (lab Pine stub): BAR|o=..|h=..|l=..|c=..|v=..
COMMENT_RE = re.compile(
    r"^BAR\|o=(?P<o>[-\d.]+)\|h=(?P<h>[-\d.]+)\|l=(?P<l>[-\d.]+)\|c=(?P<c>[-\d.]+)\|v=(?P<v>\d+)$"
)

META_SCHEMA = "BAR_EXPORT_meta_v0.2"


def decode_bar_signal(signal: str) -> dict[str, float]:
    """Decode a BAR EXPORT Signal field into OHLCV (v0.1 pipe, v0.2 pipe, or legacy comment).

    Returns the same six numeric keys for every format; v0.2's appended metadata
    is ignored here (use :func:`decode_bar_meta` for it), so existing callers are
    unaffected by the schema bump.
    """
    text = str(signal).strip()
    m = SIGNAL_PIPE_RE.match(text) or SIGNAL_PIPE_V2_RE.match(text)
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


def decode_bar_meta(signal: str) -> dict | None:
    """Decode the BAR EXPORT v0.2 metadata suffix; ``None`` for v0.1/legacy rows.

    The instrument constants (``ticker``..``timeframe``) are identical on every
    row; the per-bar fields are nested under ``_bar``. ``parse_bar_export_with_meta``
    keeps only the constants at file level.
    """
    m = SIGNAL_PIPE_V2_RE.match(str(signal).strip())
    if not m:
        return None
    return {
        "ticker": m.group("ticker"),
        "type": m.group("type"),
        "quote_currency": m.group("quote_ccy"),
        "base_currency": m.group("base_ccy"),
        "mintick": float(m.group("mintick")),
        "pointvalue": float(m.group("pointvalue")),
        "timezone": m.group("tz"),
        "timeframe": m.group("tf"),
        "_bar": {
            "time_close_ms": int(m.group("time_close")),
            "dayofweek": int(m.group("dow")),
            "session": m.group("sess"),
        },
    }


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


def _instrument_constants(bar_meta: dict) -> dict:
    """The file-level (non per-bar) subset of a decoded v0.2 metadata dict."""
    return {k: v for k, v in bar_meta.items() if not k.startswith("_")}


def _parse_one(path: Path, *, symbol: str) -> tuple[pd.DataFrame, dict | None]:
    """Decode one BAR EXPORT List-of-Trades CSV into (time/OHLCV rows, instrument meta).

    ``meta`` is the v0.2 instrument-constant dict (``None`` for a v0.1 export). Rows
    that disagree on the constants are a format-drift hard fail.
    """
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
    meta: dict | None = None
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
        bar_meta = decode_bar_meta(signal)
        if bar_meta is not None:
            const = _instrument_constants(bar_meta)
            if meta is None:
                meta = const
            elif const != meta:
                raise ValueError(
                    f"BAR EXPORT meta drift {path} trade {row[trade_col]}: "
                    f"{meta} vs {const}"
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
    return pd.DataFrame(rows), meta


def _parse_pages(
    paths: str | Path | Sequence[str | Path], *, symbol: str
) -> tuple[pd.DataFrame, dict | None]:
    """Shared core for :func:`parse_bar_export` / :func:`parse_bar_export_with_meta`."""
    if isinstance(paths, (str, Path)):
        paths = [paths]
    results = [_parse_one(Path(p), symbol=symbol) for p in paths]
    df = pd.concat([r[0] for r in results], ignore_index=True)
    df = (
        df.sort_values("time")
        .drop_duplicates(subset="time", keep="last")
        .reset_index(drop=True)
    )
    metas = [r[1] for r in results if r[1] is not None]
    meta: dict | None = None
    if metas:
        meta = metas[0]
        for other in metas[1:]:
            if other != meta:
                raise ValueError(f"BAR EXPORT meta drift across pages: {meta} vs {other}")
    return df, meta


def parse_bar_export(paths: str | Path | Sequence[str | Path], *, symbol: str) -> pd.DataFrame:
    """Decode one or more BAR EXPORT page CSVs into a single OHLCV bar DataFrame.

    Multi-page: TV caps the List-of-Trades export at ~9,000 bars. For windows beyond
    that, pass a list of page CSVs; pages are concatenated, deduplicated on bar-open
    ``time`` (``keep='last'`` — prefer the later re-export), and sorted. v0.2 metadata
    is ignored here; use :func:`parse_bar_export_with_meta` to capture it.
    """
    df, _ = _parse_pages(paths, symbol=symbol)
    return df


def parse_bar_export_with_meta(
    paths: str | Path | Sequence[str | Path], *, symbol: str
) -> tuple[pd.DataFrame, dict | None]:
    """Like :func:`parse_bar_export`, but also return the v0.2 instrument-constant
    metadata (``None`` for a v0.1 export). The OHLCV DataFrame is identical either way."""
    return _parse_pages(paths, symbol=symbol)


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


def write_bar_meta(
    meta: dict | None, *, symbol: str, out_dir: str | Path | None = None
) -> Path | None:
    """Write the v0.2 instrument sidecar ``<SYMBOL>_M15.meta.json`` next to the bar CSV.

    ``None`` meta (a v0.1 export) writes nothing and returns ``None``. The sidecar is
    derived from gitignored vendor bytes — gitignored, and skipped by the ``*.csv``-only
    SHA256SUMS manifest gate, so it adds no manifest churn.
    """
    if meta is None:
        return None
    target_dir = Path(out_dir) if out_dir is not None else DEFAULT_BAR_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    out_path = target_dir / f"{symbol}_M15.meta.json"

    payload = {"schema": META_SCHEMA, "symbol": symbol}
    payload.update({k: v for k, v in meta.items() if not k.startswith("_")})
    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return out_path
