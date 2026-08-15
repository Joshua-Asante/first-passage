"""Minimal Databento Historical HTTP client (stdlib + requests, zero-install).

Used by the Helios F1 probe to pull CME crude-oil daily bars. We deliberately
avoid the `databento` SDK so Joshua's environment is not mutated; the historical
timeseries endpoint is a simple HTTP GET with HTTP-Basic auth (key as username,
empty password).

The API key is read at use-time from ``~/.keys/databento.txt`` and is NEVER
printed or returned in any log line (memory: reference_github_pat discipline,
generalized to all credentials).
"""
from __future__ import annotations

import io
import re
from pathlib import Path

import pandas as pd
import requests

_HIST_BASE = "https://hist.databento.com/v0"
_KEY_FILE = Path.home() / ".keys" / "databento.txt"
_KEY_RE = re.compile(r"db-[A-Za-z0-9]+")


def load_key() -> str:
    """Load the Databento API key. Raises if absent. Never logs the value."""
    if not _KEY_FILE.exists():
        raise FileNotFoundError(f"Databento key file not found at {_KEY_FILE}")
    raw = _KEY_FILE.read_text(encoding="utf-8")
    m = _KEY_RE.search(raw)
    if not m:
        # Fall back to a stripped single-token file.
        tok = raw.strip().splitlines()[0].strip() if raw.strip() else ""
        if not tok:
            raise ValueError(f"No Databento key parsed from {_KEY_FILE}")
        return tok
    return m.group(0)


def fetch_ohlcv_1d(
    symbols: list[str] | str,
    start: str,
    end: str,
    *,
    dataset: str = "GLBX.MDP3",
    stype_in: str = "continuous",
    timeout: int = 120,
) -> pd.DataFrame:
    """Fetch daily OHLCV bars for ``symbols`` over [start, end).

    Returns a DataFrame with human-readable prices (pretty_px) and ISO
    timestamps (pretty_ts), with the requested symbol mapped into a ``symbol``
    column (map_symbols). ``instrument_id`` is retained for roll detection.
    """
    if isinstance(symbols, str):
        symbols = [symbols]
    key = load_key()
    params = {
        "dataset": dataset,
        "symbols": ",".join(symbols),
        "schema": "ohlcv-1d",
        "stype_in": stype_in,
        "start": start,
        "end": end,
        "encoding": "csv",
        "pretty_px": "true",
        "pretty_ts": "true",
        "map_symbols": "true",
    }
    resp = requests.get(
        f"{_HIST_BASE}/timeseries.get_range",
        params=params,
        auth=(key, ""),
        timeout=timeout,
    )
    if resp.status_code != 200:
        # Surface the API error body (it never contains the key) for diagnosis.
        raise RuntimeError(
            f"Databento HTTP {resp.status_code}: {resp.text[:500]}"
        )
    df = pd.read_csv(io.StringIO(resp.text))
    return df
