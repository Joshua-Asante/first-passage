"""USDCAD 15m volatility-breakout search harness.

Pre-registered by docs/briefs/pre-registration/PREREG-USDCAD-BREAKOUT-2026-06-14.md.
Python pre-filter ONLY — NO gate authority (sweep ADR 2026-06-05). Look-ahead-free
(signal at close t, fill at open t+1, STOP-FIRST). All PnL is net of cost, in R.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

PIP = 1e-4
SIGNAL_PIPE_RE = re.compile(
    r"^(?P<e>\d+)\|(?P<o>[-\d.]+)\|(?P<h>[-\d.]+)\|(?P<l>[-\d.]+)\|(?P<c>[-\d.]+)\|(?P<v>\d+)$"
)
# Canonical committed store (survives Downloads cleaning). NOTE: this is the
# 2026-06-25 810ef re-export (2020 -> 2026, ~150k bars); the original NULL loops
# ran on the 2026-06-14 506df 2026-H1 window (~11k bars, gone from Downloads),
# so a re-run covers far more history than the pre-registered single-window study.
DEFAULT_CSV = (
    Path(__file__).resolve().parents[3]
    / "core/data/tv_exports/pepperstone/bar_export/USDCAD_M15_pep.csv"
)
DON_N = (12, 24, 48, 96)
ORB_M = (4, 8)
SESSIONS = {  # ET hour windows; None = all-day control
    "ny0811": (8, 11),
    "ny0812": (8, 12),
    "ln0312": (3, 12),
    "allday": None,
}
K_STOPS = (1.5, 2.0, 2.5, 3.0)
EXITS = (("tp", 1.5), ("tp", 2.0), ("tp", 3.0), ("trail", 2.0), ("trail", 3.0))
VOLFLOOR = (False, True)
EMA_FAST = (9, 20)
EMA_SLOW = (50, 100, 200)
EMA_SPANS = (9, 20, 50, 100, 200)
VOLFLOOR_LB = 480
VOLFLOOR_Q = 0.50
RT_COST_PIP = 0.8
MAX_HOLD = 24
ET = "America/New_York"


# --------------------------------------------------------------------- bars
@dataclass
class Bars:
    open: np.ndarray
    high: np.ndarray
    low: np.ndarray
    close: np.ndarray
    atr: np.ndarray
    et_hour: np.ndarray
    et_min: np.ndarray
    et_date: np.ndarray      # int ordinal per ET calendar day
    contig: np.ndarray       # bool: bar t is 15min after t-1
    don_high: dict           # N -> rolling highest(high, N) excl current
    don_low: dict
    volfloor_ok: np.ndarray  # atr[t] >= trailing median(atr)
    n: int
    ema: dict = field(default_factory=dict)   # span -> EMA(close), warmup-masked


def _rma(x: np.ndarray, length: int) -> np.ndarray:
    """Wilder RMA (== TV ta.atr smoothing)."""
    out = np.full_like(x, np.nan, dtype=float)
    if len(x) < length:
        return out
    seed = np.nanmean(x[:length])
    out[length - 1] = seed
    for i in range(length, len(x)):
        prev = out[i - 1]
        out[i] = (x[i] + (length - 1) * prev) / length if not np.isnan(prev) else x[i]
    return out


def load_and_prep(path: Path = DEFAULT_CSV) -> Bars:
    raw = pd.read_csv(path, encoding="utf-8-sig")
    raw.columns = [str(c).strip() for c in raw.columns]
    e = raw[raw["Type"].astype(str).str.startswith("Entry")]
    recs = []
    for _, r in e.iterrows():
        m = SIGNAL_PIPE_RE.match(str(r["Signal"]).strip())
        if m:
            recs.append((int(m.group("e")), float(m.group("o")), float(m.group("h")),
                         float(m.group("l")), float(m.group("c"))))
    df = pd.DataFrame(recs, columns=["e", "open", "high", "low", "close"]).sort_values("e")
    df = df.reset_index(drop=True)
    t_utc = pd.to_datetime(df["e"], unit="ms", utc=True)
    t_et = t_utc.dt.tz_convert(ET)
    o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    # ATR(14) Wilder
    prev_c = np.concatenate([[np.nan], c[:-1]])
    tr = np.maximum(h - l, np.maximum(np.abs(h - prev_c), np.abs(l - prev_c)))
    atr = _rma(tr, 14)
    # Donchian channels (exclude current bar)
    hs, ls = pd.Series(h), pd.Series(l)
    don_high = {N: hs.rolling(N).max().shift(1).to_numpy() for N in DON_N}
    don_low = {N: ls.rolling(N).min().shift(1).to_numpy() for N in DON_N}
    # vol floor: atr >= trailing median(atr), shifted to avoid look-ahead
    atr_s = pd.Series(atr)
    vthr = atr_s.rolling(VOLFLOOR_LB).quantile(VOLFLOOR_Q).shift(1).to_numpy()
    volfloor_ok = atr >= vthr  # NaN -> False
    volfloor_ok = np.where(np.isnan(vthr), False, volfloor_ok)
    contig = np.concatenate([[False], (np.diff(df["e"].to_numpy()) == 15 * 60 * 1000)])
    et_date = pd.factorize(t_et.dt.date)[0]
    # EMAs (TV ta.ema == ewm adjust=False), warmup-masked to NaN for t < span
    cs = pd.Series(c)
    ema = {}
    for span in EMA_SPANS:
        e_arr = np.array(cs.ewm(span=span, adjust=False).mean().to_numpy(), dtype=float)
        e_arr[:span] = np.nan
        ema[span] = e_arr
    return Bars(o, h, l, c, atr,
                t_et.dt.hour.to_numpy(), t_et.dt.minute.to_numpy(),
                et_date.astype(int), contig, don_high, don_low,
                volfloor_ok.astype(bool), len(df), ema)


# --------------------------------------------------------------- signal build
def _session_ok(bars: Bars, session) -> np.ndarray:
    if session is None:
        return np.ones(bars.n, bool)
    lo, hi = session
    return (bars.et_hour >= lo) & (bars.et_hour < hi)


def build_signals(bars: Bars, family: str, param: int, session, volfloor: bool):
    sess = _session_ok(bars, session)
    vf = bars.volfloor_ok if volfloor else np.ones(bars.n, bool)
    base = sess & vf & ~np.isnan(bars.atr)
    long_sig = np.zeros(bars.n, bool)
    short_sig = np.zeros(bars.n, bool)
    if family == "donchian":
        dh, dl = bars.don_high[param], bars.don_low[param]
        ok = base & ~np.isnan(dh)
        long_sig = ok & (bars.close > dh)
        short_sig = ok & (bars.close < dl)
    elif family == "orb":
        M = param
        # per ET day, within session window: OR over first M in-window bars
        for d in np.unique(bars.et_date):
            idx = np.where((bars.et_date == d) & sess)[0]
            if len(idx) <= M:
                continue
            or_h = bars.high[idx[:M]].max()
            or_l = bars.low[idx[:M]].min()
            for t in idx[M:]:
                if not base[t]:
                    continue
                if bars.close[t] > or_h:
                    long_sig[t] = True
                elif bars.close[t] < or_l:
                    short_sig[t] = True
    elif family == "pullback":
        ema_f, ema_s = param            # (fast_span, slow_span)
        ef, es = bars.ema[ema_f], bars.ema[ema_s]
        ok = base & ~np.isnan(es) & ~np.isnan(ef)
        up = ok & (ef > es)             # uptrend: fast above slow
        dn = ok & (ef < es)            # downtrend
        # long: dip touched fast EMA (low<=ef) but closed back above it (rebound)
        long_sig = up & (bars.low <= ef) & (bars.close > ef)
        # short: rally touched fast EMA (high>=ef) but closed back below it
        short_sig = dn & (bars.high >= ef) & (bars.close < ef)
    else:
        raise ValueError(family)
    return long_sig, short_sig


# --------------------------------------------------------------- simulator
def simulate(bars: Bars, long_sig, short_sig, k: float, exit_mode: str,
             exit_param: float, rt_cost_pip: float = RT_COST_PIP,
             side_mode: str = "both") -> np.ndarray:
    """Return net-R per trade. Look-ahead-free; STOP-FIRST; one position at a time."""
    o, h, l, c, atr = bars.open, bars.high, bars.low, bars.close, bars.atr
    n = bars.n
    rt_cost = rt_cost_pip * PIP
    out = []
    t = 0
    while t < n - 1:
        sig_long = long_sig[t]
        sig_short = short_sig[t]
        if not (sig_long or sig_short):
            t += 1
            continue
        # resolve side under side_mode
        if side_mode == "long":
            side = 1 if sig_long else 0
        elif side_mode == "short":
            side = -1 if sig_short else 0
        elif side_mode == "reversion":      # negative control: trade against breakout
            side = -1 if sig_long else (1 if sig_short else 0)
        else:                                # both: long takes precedence
            side = 1 if sig_long else -1
        if side == 0:
            t += 1
            continue
        # fill at next bar open; require contiguity (no fill across a gap)
        ti = t + 1
        if ti >= n or not bars.contig[ti]:
            t += 1
            continue
        entry = o[ti]
        stop_dist = k * atr[t]
        if not (stop_dist > 0):
            t += 1
            continue
        stop = entry - side * stop_dist
        tp = entry + side * exit_param * stop_dist if exit_mode == "tp" else np.nan
        exit_px = None
        j = ti
        held = 0
        while j < n:
            # STOP-FIRST on bar j
            if side == 1:
                if l[j] <= stop:
                    exit_px = stop; break
                if exit_mode == "tp" and h[j] >= tp:
                    exit_px = tp; break
            else:
                if h[j] >= stop:
                    exit_px = stop; break
                if exit_mode == "tp" and l[j] <= tp:
                    exit_px = tp; break
            # forced exits: ET 16:00 bar, max-hold, or gap before next bar
            gap_next = (j + 1 >= n) or (not bars.contig[j + 1])
            if (bars.et_hour[j] == 16 and bars.et_min[j] == 0) or held >= MAX_HOLD or gap_next:
                exit_px = c[j]; break
            # trailing ratchet for next bar (off current close)
            if exit_mode == "trail":
                if side == 1:
                    stop = max(stop, c[j] - exit_param * atr[j])
                else:
                    stop = min(stop, c[j] + exit_param * atr[j])
            j += 1
            held += 1
        if exit_px is None:
            exit_px = c[n - 1]
        net_r = side * (exit_px - entry) / stop_dist - rt_cost / stop_dist
        out.append(net_r)
        t = j + 1  # flat again after exit bar
    return np.array(out, float)


# ------------------------------------------------ stop-entry (level fill) variant
def build_levels(bars: Bars, family: str, param: int, session, volfloor: bool):
    """Per-bar breakout LEVELS (channel/OR high & low) + valid mask, for stop-entry."""
    sess = _session_ok(bars, session)
    vf = bars.volfloor_ok if volfloor else np.ones(bars.n, bool)
    base = sess & vf & ~np.isnan(bars.atr)
    long_lvl = np.full(bars.n, np.nan)
    short_lvl = np.full(bars.n, np.nan)
    if family == "donchian":
        long_lvl = bars.don_high[param].copy()
        short_lvl = bars.don_low[param].copy()
        valid = base & ~np.isnan(long_lvl)
    elif family == "orb":
        M = param
        valid = np.zeros(bars.n, bool)
        for d in np.unique(bars.et_date):
            idx = np.where((bars.et_date == d) & sess)[0]
            if len(idx) <= M:
                continue
            or_h = bars.high[idx[:M]].max()
            or_l = bars.low[idx[:M]].min()
            post = idx[M:]
            long_lvl[post] = or_h
            short_lvl[post] = or_l
            valid[post] = base[post]
    else:
        raise ValueError(family)
    return long_lvl, short_lvl, valid


def simulate_stop_entry(bars: Bars, long_lvl, short_lvl, valid, k: float,
                        exit_mode: str, exit_param: float,
                        rt_cost_pip: float = RT_COST_PIP, side_mode: str = "both") -> np.ndarray:
    """Breakout via intrabar STOP order filled AT the level (turtle-style). Look-ahead-free:
    level known from prior bars; sizing uses atr[t-1]; STOP-FIRST incl. entry bar."""
    o, h, l, c, atr = bars.open, bars.high, bars.low, bars.close, bars.atr
    n = bars.n
    rt_cost = rt_cost_pip * PIP
    out = []
    t = 1
    while t < n:
        if not valid[t] or np.isnan(atr[t - 1]) or atr[t - 1] <= 0:
            t += 1
            continue
        ll, sl = long_lvl[t], short_lvl[t]
        trig_long = (not np.isnan(ll)) and h[t] >= ll
        trig_short = (not np.isnan(sl)) and l[t] <= sl
        if not (trig_long or trig_short):
            t += 1
            continue
        # choose side (long precedence; both rare -> bar net direction)
        if trig_long and trig_short:
            base_long = c[t] >= o[t]
        else:
            base_long = trig_long
        if side_mode == "long" and not base_long:
            t += 1; continue
        if side_mode == "short" and base_long:
            t += 1; continue
        if side_mode == "reversion":
            side = -1 if base_long else 1   # fade the breakout
        else:
            side = 1 if base_long else -1
        if base_long:
            entry = max(o[t], ll)
        else:
            entry = min(o[t], sl)
        stop_dist = k * atr[t - 1]
        stop = entry - side * stop_dist
        tp = entry + side * exit_param * stop_dist if exit_mode == "tp" else np.nan
        exit_px = None
        j = t
        held = 0
        while j < n:
            if side == 1:
                if l[j] <= stop:
                    exit_px = stop; break
                if exit_mode == "tp" and h[j] >= tp:
                    exit_px = tp; break
            else:
                if h[j] >= stop:
                    exit_px = stop; break
                if exit_mode == "tp" and l[j] <= tp:
                    exit_px = tp; break
            gap_next = (j + 1 >= n) or (not bars.contig[j + 1])
            if (bars.et_hour[j] == 16 and bars.et_min[j] == 0) or held >= MAX_HOLD or gap_next:
                exit_px = c[j]; break
            if exit_mode == "trail":
                if side == 1:
                    stop = max(stop, c[j] - exit_param * atr[j])
                else:
                    stop = min(stop, c[j] + exit_param * atr[j])
            j += 1
            held += 1
        if exit_px is None:
            exit_px = c[n - 1]
        out.append(side * (exit_px - entry) / stop_dist - rt_cost / stop_dist)
        t = j + 1
    return np.array(out, float)


# --------------------------------------------------------------- metrics
def metrics(net_r: np.ndarray) -> dict:
    n = len(net_r)
    if n == 0:
        return dict(n=0, exp=np.nan, pf=np.nan, wr=np.nan, profitR=0.0, maxddR=np.nan)
    wins = net_r[net_r > 0].sum()
    losses = -net_r[net_r < 0].sum()
    eq = np.cumsum(net_r)
    dd = (np.maximum.accumulate(eq) - eq).max()
    return dict(
        n=n, exp=float(net_r.mean()),
        pf=float(wins / losses) if losses > 0 else np.inf,
        wr=float((net_r > 0).mean()), profitR=float(net_r.sum()), maxddR=float(dd),
    )
