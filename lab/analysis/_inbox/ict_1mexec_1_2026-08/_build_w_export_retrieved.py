"""Q-ICT-MNQ-1 / Layer W -- OHLC -> gateBias adapter.

Reconstructs the Weekly indicator's data-window export columns directly from raw
Weekly OHLC bars, so the ARCHIVED, UNMODIFIED `harness_w.evaluate_weekly()` can
produce the verdict. The original `ict_weekly_bias_DRAFT.pine` is lost, but
PREREG-W.md sec 0 transcribes the object formula in PROSE (not merely by line
citation), so the reconstruction is faithful without the .pine bytes:

    L28  vStruct = close > wEma ? 1 : close < wEma ? -1 : 0,  wEma = ta.ema(close, emaLen)
    L29  emaLen = 20 (LOCKED; must equal the 1M wEmaLen)
    L30  gateBias = vStruct                       <- the object under test
    L32  realized = close > close[1] ? 1 : ...    (sign of week-over-week close change)
         priorGateBias = gateBias[1]
         gateScored = priorGateBias != 0 AND realized != 0
         gateHit    = priorGateBias == realized

Frozen by: lab/analysis/ict_mnq_2026-08/PREREG_D_W.md sec 4 + sec 5 (commit is the
firewall-lift). This module computes INPUT COLUMNS ONLY -- it contains no verdict
logic, no thresholds, and no statistics. Every gate lives in the archived harness.

Roll exclusion (PREREG_D_W sec 2): weeks whose bar falls within +-4 calendar days
of a 3rd-Friday-of-{Mar,Jun,Sep,Dec} CME expiry are forced gateScored=0 (never
imputed, never dropped from the frame -- the frame must stay contiguous because
harness_w pairs against the prior CALENDAR week, not the prior scored row).

ASCII only. TV BAR_EXPORT epoch is UTC.
"""
from __future__ import annotations

import datetime as _dt
import re
from pathlib import Path

import numpy as np
import pandas as pd

# ---- FROZEN (PREREG_D_W sec 4; inherited verbatim from PREREG-W.md) ----------
EMA_LEN = 20                 # LOCKED; PREREG-W frozen-config + forbidden move #5
ROLL_BUFFER_DAYS = 4         # PREREG_D_W sec 2 (+-4 calendar days)
ROLL_MONTHS = (3, 6, 9, 12)  # CME quarterly expiry months

# BAR_EXPORT pipe field: epoch_ms|open|high|low|close|volume|...
_SIGNAL_PIPE_RE = re.compile(
    r"^(?P<e>\d+)\|(?P<o>[-\d.]+)\|(?P<h>[-\d.]+)\|(?P<l>[-\d.]+)\|(?P<c>[-\d.]+)\|(?P<v>\d+)"
)


def pine_ema(values, length: int = EMA_LEN) -> np.ndarray:
    """TV `ta.ema` convention: plain recursive EMA seeded at the first bar.

    ema[0] = close[0]; ema[i] = a*close[i] + (1-a)*ema[i-1], a = 2/(length+1).

    NOT SMA-seeded and NOT Wilder/RMA -- those are different functions (`ta.rma`,
    used for ATR elsewhere in this codebase). PREREG_D_W sec 5 item 1 discloses
    that the first ~4*length bars carry a converging EMA; that warmup is REPORTED,
    never excluded (PREREG-W declares no warmup rule and inventing one post-hoc
    would be an undeclared criterion).
    """
    v = np.asarray(values, dtype=float)
    out = np.empty(len(v), dtype=float)
    if len(v) == 0:
        return out
    alpha = 2.0 / (length + 1.0)
    out[0] = v[0]
    for i in range(1, len(v)):
        out[i] = alpha * v[i] + (1.0 - alpha) * out[i - 1]
    return out


def third_friday(year: int, month: int) -> _dt.date:
    """The 3rd Friday of the given month (CME quarterly expiry anchor)."""
    fridays = [
        _dt.date(year, month, day)
        for day in range(1, 32)
        if _is_valid(year, month, day) and _dt.date(year, month, day).weekday() == 4
    ]
    return fridays[2]


def _is_valid(year: int, month: int, day: int) -> bool:
    try:
        _dt.date(year, month, day)
        return True
    except ValueError:
        return False


def in_roll_window(day: _dt.date, buffer_days: int = ROLL_BUFFER_DAYS) -> bool:
    """True when `day` is within +-buffer_days of a quarterly 3rd-Friday expiry.

    Checks the expiry of every quarterly month in the adjacent year span so a
    window straddling a year boundary (mid-December) is still caught.
    """
    for yr in (day.year - 1, day.year, day.year + 1):
        for mo in ROLL_MONTHS:
            if abs((day - third_friday(yr, mo)).days) <= buffer_days:
                return True
    return False


def load_bar_export_ohlc(path) -> pd.DataFrame:
    """Load OHLC bars from a BAR_EXPORT pipe CSV or a plain OHLC CSV.

    Timeframe-agnostic (the pipe format is identical for 1D and 1W).

    Handles **BAR_EXPORT v0.2**, whose `Signal` field appends metadata after
    volume (`...|volume|epoch2|N|M|SYMBOL|futures|USD||tick|pointval|tz|tf`).
    The archived `harness_d.SIGNAL_PIPE_RE` anchors on `volume$` and therefore
    matches v0.1 only -- on a v0.2 file it drops every row and the harness
    reports a spurious INSUFFICIENT-N (it does emit a loud WARN naming the drop
    count, which is how this was caught). `_SIGNAL_PIPE_RE` here is deliberately
    un-anchored so both generations parse. This is the schema-adapter fix the
    campaign README prescribes for TV format drift -- it touches no verdict logic.

    Returns a chronological, epoch-deduped frame with columns
    ['epoch_ms', 'open', 'high', 'low', 'close'].
    """
    raw = pd.read_csv(Path(path), encoding="utf-8-sig")
    raw.columns = [str(c).strip() for c in raw.columns]
    cols = {c.lower(): c for c in raw.columns}

    if "signal" in cols and "type" in cols:
        entries = raw[raw[cols["type"]].astype(str).str.startswith("Entry")]
        recs = []
        for _, r in entries.iterrows():
            m = _SIGNAL_PIPE_RE.match(str(r[cols["signal"]]).strip())
            if m:
                recs.append(
                    (
                        int(m.group("e")),
                        float(m.group("o")),
                        float(m.group("h")),
                        float(m.group("l")),
                        float(m.group("c")),
                    )
                )
        df = pd.DataFrame(recs, columns=["epoch_ms", "open", "high", "low", "close"])
    else:
        def pick(*names):
            for nm in names:
                if nm in cols:
                    return cols[nm]
            raise KeyError(f"CSV missing any of {names}; have {list(raw.columns)}")

        tcol = None
        for nm in ("epoch", "epoch_ms", "time", "timestamp", "datetime", "date"):
            if nm in cols:
                tcol = cols[nm]
                break
        if tcol is None:
            raise KeyError("CSV missing a time/date/epoch column")
        tser = raw[tcol]
        if pd.api.types.is_numeric_dtype(tser):
            epoch = tser.to_numpy(dtype="int64")
            if np.nanmedian(epoch) < 1e12:  # seconds, not ms
                epoch = epoch * 1000
        else:
            epoch = (
                pd.to_datetime(tser, utc=True).astype("int64") // 1_000_000
            ).to_numpy()
        df = pd.DataFrame(
            {
                "epoch_ms": epoch,
                "open": raw[pick("open")].astype(float),
                "high": raw[pick("high")].astype(float),
                "low": raw[pick("low")].astype(float),
                "close": raw[pick("close")].astype(float),
            }
        )

    return (
        df.drop_duplicates("epoch_ms")
        .sort_values("epoch_ms", kind="stable")
        .reset_index(drop=True)
    )


def build_w_export(bars: pd.DataFrame, *, apply_roll_exclusion: bool = True) -> pd.DataFrame:
    """Build the harness_w-compatible export frame from Weekly OHLC bars.

    Emits exactly harness_w's REQUIRED_CANON columns
    (time, gateBias, gateHit, gateScored, outcome) plus `vStruct` (== gateBias,
    the only reconstructable vote) and `roll_excluded` for reporting.

    The live/last bar is NOT dropped here -- harness_w.de_overlap_scored drops it
    downstream, and dropping it twice would silently discard a real week.
    """
    close = bars["close"].to_numpy(dtype=float)
    n = len(close)

    wema = pine_ema(close, EMA_LEN)
    gate_bias = np.sign(close - wema)                       # vStruct: +1 / -1 / 0

    realized = np.zeros(n, dtype=float)                     # sign(close - close[1])
    if n > 1:
        realized[1:] = np.sign(close[1:] - close[:-1])

    prior_gate_bias = np.zeros(n, dtype=float)              # gateBias[1]
    if n > 1:
        prior_gate_bias[1:] = gate_bias[:-1]

    gate_scored = (prior_gate_bias != 0) & (realized != 0)
    gate_scored[0] = False                                  # no prior week exists

    days = [
        _dt.datetime.fromtimestamp(int(e) / 1000, _dt.timezone.utc).date()
        for e in bars["epoch_ms"].to_numpy()
    ]
    roll_excluded = np.array([in_roll_window(d) for d in days], dtype=bool)
    if apply_roll_exclusion:
        gate_scored = gate_scored & (~roll_excluded)

    gate_hit = (prior_gate_bias == realized) & gate_scored

    return pd.DataFrame(
        {
            "time": bars["epoch_ms"].to_numpy(),
            "vStruct": gate_bias,
            "gateBias": gate_bias,
            "gateHit": gate_hit.astype(int),
            "gateScored": gate_scored.astype(int),
            "outcome": realized,
            "roll_excluded": roll_excluded.astype(int),
        }
    )


# Back-compat alias: this loader is timeframe-agnostic despite the original name.
load_weekly_ohlc = load_bar_export_ohlc


def build_from_csv(path, *, apply_roll_exclusion: bool = True) -> pd.DataFrame:
    """Convenience: load a Weekly CSV and build the export frame in one call."""
    return build_w_export(
        load_bar_export_ohlc(path), apply_roll_exclusion=apply_roll_exclusion
    )
