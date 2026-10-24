"""Generalized cross-instrument ORB harness (2026-06-22).

Faithful port of lab/analysis/legacy/us500_discovery_2026-06-22/{harness,probes,orb_robustness,
orb_validate}.py, generalized over:
  - TWO feed formats: BAR_EXPORT v0.1 (Signal=epoch|o|h|l|c|v, Pepperstone/Alchemy) and
    OANDA OHLCV (time,open,high,low,close,volume).
  - Per-instrument cost models + session-open definitions (INSTRUMENTS dict below).
  - A CONTINUOUS entry-slip parameter (the clean cross-instrument tradeability metric:
    slip-to-zero in instrument points / instrument spread reproduces the US500 fill cliff).

The ORB engine (orb_backtest), the within-day OR-window PLACEBO (the load-bearing
structural null), the OR-length plateau classifier, year/halves robustness, long/short
split, and the FXIFY first-passage MC are ported verbatim in mechanism.

CALIBRATION GATE: run_instrument("US500_pep") must reproduce the established US500 result
  (meanR +0.058, t +1.35, WR .419, PF 1.107, all-yr+, long +.069/short +.047, placebo
  p~0.012, slip-to-zero ~0.9pt). orb_lib_test.py asserts this.

DO NOT modify the us500_discovery_2026-06-22 files. This is an independent generalization.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DL = Path(r"C:\Users\joshu\Downloads")
BAR_DATA = Path(r"C:\Users\joshu\multi_firm_operations\core\data\bar_data")
# Canonical raw BAR_EXPORT v0.1 store (committed via SHA256SUMS; survives Downloads cleaning).
# Researched-instrument panels are filed here as <SYMBOL>_M15_pep.csv (see parse_bar_export.py).
BAR_EXPORT = BAR_DATA.parent / "tv_exports" / "pepperstone" / "bar_export"

SIG = re.compile(
    r"^(?P<epoch>\d+)\|(?P<o>[-\d.]+)\|(?P<h>[-\d.]+)\|(?P<l>[-\d.]+)\|(?P<c>[-\d.]+)\|(?P<v>\d+)$"
)

OPEN_TOD_US = 9 * 60 + 30      # 09:30 ET (US equity cash open)
CLOSE_TOD_US = 15 * 60 + 45    # 15:45 ET (last RTH bar-open; session ends 16:00)
OPEN_TOD_LON = 3 * 60          # 03:00 ET = 08:00 London (FX London-open variant)
CLOSE_TOD_LON = 11 * 60 + 45   # 11:45 ET (London/early-NY close-ish, 9h window)


# --------------------------------------------------------------------------- config
@dataclass
class Instrument:
    name: str
    path: Path
    loader: str                 # "bar_export" | "oanda"
    feed: str                   # "Pepperstone" | "Alchemy" | "OANDA"
    tick: float
    spread_pt: float            # full bid/ask spread in instrument points
    rt_cost_pt: float           # round-trip cost in instrument points (spread + slip)
    open_tod: int = OPEN_TOD_US
    close_tod: int = CLOSE_TOD_US
    tz: str = "America/New_York"  # session-tagging tz (Europe/Berlin for DAX, etc.)
    note: str = ""

    @property
    def cache(self) -> Path:
        return HERE / f"_cache_{self.name}.pkl"


# Provisional cost models — spread/rt_cost in INSTRUMENT POINTS. US500 is the locked
# anchor (0.8 spread + 0.2 slip = 1.0pt RT). Others are refined from repo grounding
# (ops/instruments/*.md, CLAUDE.md contractValue table) before final tradeability calls.
# rt_cost_pt is the headline cost; spread_pt is used for the slip-to-zero / spread ratio.
INSTRUMENTS: dict[str, Instrument] = {
    # --- Pepperstone BAR_EXPORT (same canonical feed as the US500 anchor) ---
    "US500_pep": Instrument(
        "US500_pep", BAR_EXPORT / "US500_M15_pep.csv",
        "bar_export", "Pepperstone", tick=0.1, spread_pt=0.8, rt_cost_pt=1.0,
        note="canonical store (filed 2026-06-25 e4fa8, 2020-2026; was DL 06-22 f9fa5 "
             "2022-start); SPX500.md W3/F7 cost lock; calibration anchors pinned to the "
             "f9fa5 vintage -> re-run differs marginally"),
    "NAS100_pep": Instrument(
        "NAS100_pep", BAR_EXPORT / "NAS100_M15_pep.csv",
        "bar_export", "Pepperstone", tick=0.1, spread_pt=1.25, rt_cost_pt=1.55,
        note="2020-2026 deep; canonical store (filed 2026-06-25 de06c re-export; was DL b39ba); "
             "spread ~1.0-1.5pt raw; contractValue=10 verified"),
    "NAS100_pep_early": Instrument(
        "NAS100_pep_early", DL / "BAR_EXPORT_v0.1_PEPPERSTONE_NAS100_2026-06-21_3774a.csv",
        "bar_export", "Pepperstone", tick=0.1, spread_pt=1.25, rt_cost_pt=1.55,
        note="2014-2020 OOS regime page (pre-COVID chop, 2018 vol)"),
    "XAUUSD_pep": Instrument(
        "XAUUSD_pep", BAR_EXPORT / "XAUUSD_M15_pep.csv",
        "bar_export", "Pepperstone", tick=0.01, spread_pt=0.24, rt_cost_pt=0.30,
        note="2020-2026 deep; canonical store (filed 2026-06-25 8bef6; was DL 06-21 "
             "bb820); cost-law $0.30 RT (XAUUSD ledger); contractValue=100"),
    # --- GER40 / DAX: the ONLY true-discrete-cash-open candidate (operator-supplied) ---
    "GER40_pep": Instrument(
        "GER40_pep", DL / "BAR_EXPORT_v0.1_PEPPERSTONE_GER40_2026-06-22_37fa8.csv",
        "bar_export", "Pepperstone", tick=0.1, spread_pt=1.4, rt_cost_pt=1.75,
        open_tod=9 * 60, close_tod=17 * 60 + 15, tz="Europe/Berlin",
        note="2020-2026; EUR-denom; Xetra cash 09:00-17:30 CET (TRUE discrete open); contractValue UNVERIFIED"),
    "US30_pep_early": Instrument(
        "US30_pep_early", DL / "BAR_EXPORT_v0.1_PEPPERSTONE_US30_2026-06-21_306d7.csv",
        "bar_export", "Pepperstone", tick=0.1, spread_pt=2.0, rt_cost_pt=2.5,
        note="2014-2020 ONLY (no recent Pepperstone DJ30 corpus)"),
    # --- OANDA OHLCV (different feed; Action-class ranking, flagged) ---
    "US30_oanda": Instrument(
        "US30_oanda", BAR_DATA / "US30USD.csv", "oanda", "OANDA",
        tick=0.1, spread_pt=2.0, rt_cost_pt=2.5, note="DJ30 2018-2026 recent"),
    "NAS100_oanda": Instrument(
        "NAS100_oanda", BAR_DATA / "NAS100USD.csv", "oanda", "OANDA",
        tick=0.1, spread_pt=1.5, rt_cost_pt=2.0, note="cross-feed check vs Pepperstone"),
    "XAUUSD_oanda": Instrument(
        "XAUUSD_oanda", BAR_DATA / "XAUUSD.csv", "oanda", "OANDA",
        tick=0.01, spread_pt=0.25, rt_cost_pt=0.35, note="cross-feed check vs Pepperstone"),
    "XAGUSD_oanda": Instrument(
        "XAGUSD_oanda", BAR_DATA / "XAGUSD.csv", "oanda", "OANDA",
        tick=0.001, spread_pt=0.03, rt_cost_pt=0.05, note="silver 2022-2026"),
    "USDJPY_oanda": Instrument(
        "USDJPY_oanda", BAR_DATA / "USDJPY.csv", "oanda", "OANDA",
        tick=0.001, spread_pt=0.012, rt_cost_pt=0.018, note="FX; 24h, no cash open"),
    "GBPUSD_oanda": Instrument(
        "GBPUSD_oanda", BAR_DATA / "GBPUSD_M15.csv", "oanda", "OANDA",
        tick=0.00001, spread_pt=0.00015, rt_cost_pt=0.00022, note="FX; 24h; ends 2023"),
}


# --------------------------------------------------------------------------- loaders
def _finalize(df: pd.DataFrame) -> pd.DataFrame:
    df["time"] = pd.to_datetime(df["epoch"], unit="ms", utc=True)
    df = df.sort_values("time").drop_duplicates("time", keep="last").reset_index(drop=True)
    df["et"] = df["time"].dt.tz_convert("America/New_York")
    df["d"] = df["et"].dt.date
    df["hour"] = df["et"].dt.hour
    df["minute"] = df["et"].dt.minute
    df["tod"] = df["hour"] * 60 + df["minute"]
    df["dow"] = df["et"].dt.dayofweek
    return df


def load_bar_export(path: Path) -> pd.DataFrame:
    """Vectorized BAR_EXPORT decode (Signal=epoch|o|h|l|c|v). Same semantics as the
    us500 harness.load_15m iterrows version but ~30x faster (str.split, not per-row regex)."""
    raw = pd.read_csv(path, encoding="utf-8-sig")
    raw.columns = [str(c).strip() for c in raw.columns]
    ent = raw[raw["Type"].astype(str).str.startswith("Entry")].copy()
    sig = ent["Signal"].astype(str).str.strip()
    parts = sig.str.split("|", expand=True)
    good = parts[5].notna() & parts[0].str.fullmatch(r"\d+")
    skipped = int((~good).sum())
    parts = parts[good]
    df = pd.DataFrame({
        "epoch": parts[0].astype("int64"),
        "open": parts[1].astype(float), "high": parts[2].astype(float),
        "low": parts[3].astype(float), "close": parts[4].astype(float),
        "volume": parts[5].astype("int64"),
    })
    # integrity cross-check: encoded close == the "Price <CCY>" column (USD/EUR/GBP/...)
    price_cols = [c for c in ent.columns if re.fullmatch(r"Price [A-Z]{3}", c)]
    if not price_cols:
        raise ValueError(f"no 'Price <CCY>' column in {path.name}: {list(ent.columns)}")
    price = pd.to_numeric(ent.loc[good, price_cols[0]], errors="coerce").to_numpy()
    xfail = int((np.abs(price - df["close"].to_numpy()) > np.maximum(1e-5, df["close"].to_numpy() * 1e-4)).sum())
    assert xfail == 0, f"integrity cross-check fails: {xfail}"
    if skipped:
        print(f"  [load] skipped {skipped} undecodable rows")
    return _finalize(df)


def load_oanda(path: Path) -> pd.DataFrame:
    raw = pd.read_csv(path)
    raw.columns = [str(c).strip().lower() for c in raw.columns]
    t = pd.to_datetime(raw["time"], utc=True, errors="coerce")
    # robust epoch-ms across pandas versions (avoid .view on tz-aware datetimes)
    epoch_ms = t.values.astype("datetime64[ms]").astype("int64")
    df = pd.DataFrame({
        "epoch": epoch_ms,
        "open": raw["open"].astype(float), "high": raw["high"].astype(float),
        "low": raw["low"].astype(float), "close": raw["close"].astype(float),
        "volume": raw.get("volume", 0),
    })
    df = df[df["epoch"].notna()].reset_index(drop=True)
    return _finalize(df)


def load(inst: Instrument, use_cache: bool = True) -> pd.DataFrame:
    if use_cache and inst.cache.exists() and inst.cache.stat().st_mtime >= inst.path.stat().st_mtime:
        return pd.read_pickle(inst.cache)
    df = load_bar_export(inst.path) if inst.loader == "bar_export" else load_oanda(inst.path)
    df.to_pickle(inst.cache)
    return df


# ----------------------------------------------------------------- tz tagging
def localize(df: pd.DataFrame, inst: Instrument) -> pd.DataFrame:
    """Return df with session-local tod/d columns in the instrument's tz (DST-aware).
    For US instruments (tz=America/New_York) this matches the cached ET columns; for
    DAX (Europe/Berlin) it re-tags to the 09:00 CET cash-open clock."""
    if inst.tz == "America/New_York":
        return df  # cached ET columns are already correct
    loc = df["time"].dt.tz_convert(inst.tz)
    out = df.copy()
    out["tod"] = loc.dt.hour * 60 + loc.dt.minute
    out["minute"] = loc.dt.minute
    out["d"] = loc.dt.date
    out["dow"] = loc.dt.dayofweek
    return out


# ----------------------------------------------------------------- Step-0 battery
def step0(df: pd.DataFrame, inst: Instrument) -> dict:
    df = localize(df, inst)
    rep = {"n_bars": len(df), "span": (str(df["et"].min()), str(df["et"].max())),
           "n_days": df["d"].nunique()}
    rep["minute_census"] = df["minute"].value_counts().sort_index().to_dict()
    dt = df["time"].diff().dropna().dt.total_seconds() / 60.0
    rep["spacing_top5"] = dt.round().value_counts().head(5).to_dict()
    rep["dup_times"] = int(df["time"].duplicated().sum())
    bad = ((df["high"] < df["low"]) | (df["high"] < df["open"]) | (df["high"] < df["close"]) |
           (df["low"] > df["open"]) | (df["low"] > df["close"]))
    rep["n_bad_ohlc"] = int(bad.sum())
    rep["price_range"] = (float(df["close"].min()), float(df["close"].max()))
    sess = df[(df["tod"] >= inst.open_tod) & (df["tod"] < inst.close_tod + 15)]
    rep["n_days_with_open_bar"] = int(df[df["tod"] == inst.open_tod]["d"].nunique())
    rep["bars_per_session_median"] = float(sess.groupby("d").size().median()) if len(sess) else 0.0
    return rep


# --------------------------------------------------------------- session panel
def session_panel(df: pd.DataFrame, inst: Instrument):
    """Wide per-date session panels (rows=date, cols=tod) for o/h/l/c + meta.
    Session = bars with open_tod <= tod <= close_tod (port of probes.session_panel,
    parametrized by the instrument's cash-open window + tz)."""
    df = localize(df, inst)
    sess = df[(df["tod"] >= inst.open_tod) & (df["tod"] <= inst.close_tod)].copy()
    piv = {f: sess.pivot_table(index="d", columns="tod", values=f, aggfunc="first")
           for f in ("open", "high", "low", "close")}
    for f in piv:
        piv[f] = piv[f].sort_index()
    idx = piv["close"].index
    rth_open = piv["open"].apply(lambda r: r.dropna().iloc[0] if r.notna().any() else np.nan, axis=1)
    rth_close = piv["close"].apply(lambda r: r.dropna().iloc[-1] if r.notna().any() else np.nan, axis=1)
    meta = pd.DataFrame({"rth_open": rth_open, "rth_close": rth_close}, index=idx)
    meta["prev_close"] = meta["rth_close"].shift(1)
    meta["dow"] = pd.to_datetime(pd.Series(idx, index=idx)).dt.dayofweek
    meta["year"] = pd.to_datetime(pd.Series(idx, index=idx)).dt.year
    return piv, meta


# --------------------------------------------------------------- ORB engine
def orb_backtest(piv, meta, inst: Instrument, *, or_bars=2, entry_slip_pt=0.0,
                 vol_filter=False, allowed_dows=None, blocked_hours=None):
    """Opening-range breakout, generalized. Port of orb_robustness.orb_backtest with a
    CONTINUOUS entry-slip parameter (entry = level +/- entry_slip_pt; RT cost ON TOP).

    OR = first `or_bars` session bars high/low. Enter on the first subsequent bar that
    breaks OR hi/lo (touch-fill at level + slip). Stop = opposite OR extreme. Exit at
    session close (no overnight -> no swap). R = (pnl_pt - rt_cost)/range, risk=range.
    Returns dict of arrays (incl. "entry_tod" = ET minute-of-day of the entry bar,
    and "day" = session date per trade — same length as "R").

    Toggleable filters (both default off -> exact parity with the prior behavior; these
    are the reliable-offline class per ops/instruments/NAS100.md N5/N7 — day-level
    selection that keeps the touch-fill):
      allowed_dows : frozenset[int] | None  -- None => all weekdays; else only trade days
                     where meta["dow"] in allowed_dows (skip at day level).
      blocked_hours: frozenset[int] | None  -- None/empty => no block; else skip any
                     candidate breakout bar whose ET hour (tod // 60) is blocked, and take
                     the first breakout on an *eligible* bar (C1, scan-next-eligible). The
                     OR window is never gated by blocked_hours -- it is structural.
    The stop/exit min/max over all `rest_tods` is the inherited approximation, unchanged;
    only entry-bar selection and day inclusion are gated here.
    """
    o, h, l, c = piv["open"], piv["high"], piv["low"], piv["close"]
    tods = sorted([t for t in c.columns if inst.open_tod <= t <= inst.close_tod])
    or_tods = tods[:or_bars]
    rest_tods = tods[or_bars:]
    rth_close = meta["rth_close"]
    rt = inst.rt_cost_pt

    Rs, years, sides, rngs, stops, entry_tods, days_out = [], [], [], [], [], [], []
    for day in c.index:
        if allowed_dows is not None and int(meta.loc[day, "dow"]) not in allowed_dows:
            continue
        or_hi = h.loc[day, or_tods].max()
        or_lo = l.loc[day, or_tods].min()
        if not np.isfinite(or_hi) or not np.isfinite(or_lo):
            continue
        rng = or_hi - or_lo
        if rng <= 0:
            continue
        side = None
        entry_t = None
        for t in rest_tods:
            if blocked_hours and (t // 60) in blocked_hours:
                continue
            bh, bl, bo = h.loc[day, t], l.loc[day, t], o.loc[day, t]
            if not np.isfinite(bh):
                continue
            up = bh >= or_hi
            dn = bl <= or_lo
            if up and dn:
                side = "long" if bo <= (or_hi + or_lo) / 2 else "short"
                entry_t = t; break
            if up:
                side = "long"; entry_t = t; break
            if dn:
                side = "short"; entry_t = t; break
        if side is None:
            continue
        level = or_hi if side == "long" else or_lo
        entry = level + entry_slip_pt if side == "long" else level - entry_slip_pt
        cl = rth_close.loc[day]
        if side == "long":
            stopped = l.loc[day, rest_tods].min() <= or_lo
            exit_px = or_lo if stopped else cl
            pnl = exit_px - entry
        else:
            stopped = h.loc[day, rest_tods].max() >= or_hi
            exit_px = or_hi if stopped else cl
            pnl = entry - exit_px
        Rs.append((pnl - rt) / rng)
        years.append(meta.loc[day, "year"]); sides.append(side)
        rngs.append(rng); stops.append(bool(stopped)); entry_tods.append(entry_t)
        days_out.append(day)

    Rs = np.array(Rs); years = np.array(years); sides = np.array(sides)
    rngs = np.array(rngs); stops = np.array(stops, bool); entry_tods = np.array(entry_tods)
    days_arr = np.array(days_out, dtype=object)
    if vol_filter and len(rngs):
        keep = rngs > np.median(rngs)
        Rs, years, sides, rngs, stops, entry_tods, days_arr = (
            Rs[keep], years[keep], sides[keep], rngs[keep], stops[keep],
            entry_tods[keep], days_arr[keep])
    return {"R": Rs, "year": years, "side": sides, "range": rngs,
            "stopped": stops, "entry_tod": entry_tods, "day": days_arr}


# --------------------------------------------------------------- stats / metrics
def summ(R, years=None):
    R = np.asarray(R, float)
    R = R[~np.isnan(R)]
    n = len(R)
    if n == 0:
        return dict(n=0, mean_R=np.nan, t=0.0, wr=np.nan, pf=np.nan, sumR=0.0,
                    h1=np.nan, h2=np.nan, by_year={}, all_years_pos=False)
    mu = R.mean(); sd = R.std(ddof=1) if n > 1 else 0.0
    t = mu / (sd / np.sqrt(n)) if sd > 0 else 0.0
    wins = R[R > 0].sum(); losses = -R[R < 0].sum()
    pf = wins / losses if losses > 0 else np.inf
    h = n // 2
    h1, h2 = (R[:h].mean(), R[h:].mean()) if n >= 2 else (np.nan, np.nan)
    by = {}
    if years is not None:
        for y in np.unique(years):
            by[int(y)] = float(R[years == y].mean())
    return dict(n=n, mean_R=float(mu), t=float(t), wr=float((R > 0).mean()), pf=float(pf),
                sumR=float(R.sum()), h1=float(h1), h2=float(h2), by_year=by,
                all_years_pos=bool(by and all(v > 0 for v in by.values())))


def block_bootstrap_ci(x, block=10, n=4000, seed=42, q=(2.5, 97.5)):
    rng = np.random.default_rng(seed)
    x = np.asarray(x, float); N = len(x)
    if N < block + 1:
        block = max(1, N // 2)
    nblocks = int(np.ceil(N / block))
    pool = np.arange(0, N - block + 1)
    stats = np.empty(n)
    for i in range(n):
        st = rng.choice(pool, size=nblocks)
        idx = (st[:, None] + np.arange(block)[None, :]).ravel()[:N]
        stats[i] = x[idx].mean()
    lo, hi = np.percentile(stats, q)
    return float(lo), float(hi), float((stats <= 0).mean())


def drop_top_k(r, k_list=(1, 3, 5)):
    r = np.asarray(r, float)
    order = np.argsort(-np.abs(r))
    out = {"mean_full": float(r.mean())}
    for k in k_list:
        keep = order[k:]
        out[f"d{k}"] = float(r[keep].mean()) if len(keep) else np.nan
    return out


def placebo_within_day(piv, meta, inst: Instrument, obs_mean, *, or_bars=2,
                       nperm=3000, seed=20260622):
    """Within-day OR-window placebo (port of orb_validate Null C, the HONEST null).
    Slide the OR-defining window to a random later 2-bar window on each day, trade the
    identical break/stop/exit-at-close rule. p = frac placebo panels with meanR >= obs.
    Isolates whether the OPENING range carries information vs an arbitrary intraday range.
    """
    rng = np.random.default_rng(seed)
    o, h, l, c = piv["open"], piv["high"], piv["low"], piv["close"]
    tods = sorted([t for t in c.columns if inst.open_tod <= t <= inst.close_tod])
    n_tods = len(tods)
    rt = inst.rt_cost_pt
    days = list(c.index)
    HH, LL, OO, CL = {}, {}, {}, {}
    for day in days:
        HH[day] = h.loc[day, tods].to_numpy()
        LL[day] = l.loc[day, tods].to_numpy()
        OO[day] = o.loc[day, tods].to_numpy()
        CL[day] = meta.loc[day, "rth_close"]

    def exec_win(day, w0):
        Ha, La, Oa, cl = HH[day], LL[day], OO[day], CL[day]
        or_idx = list(range(w0, w0 + or_bars))
        rest = range(w0 + or_bars, n_tods)
        or_hi = np.nanmax(Ha[or_idx]); or_lo = np.nanmin(La[or_idx])
        if not (np.isfinite(or_hi) and np.isfinite(or_lo)):
            return np.nan
        rng_ = or_hi - or_lo
        if rng_ <= 0:
            return np.nan
        entry = side = None
        for j in rest:
            bh, bl = Ha[j], La[j]
            if not np.isfinite(bh):
                continue
            up = bh >= or_hi; dn = bl <= or_lo
            if up and dn:
                side = 1 if Oa[j] <= (or_hi + or_lo) / 2 else -1
                entry = or_hi if side == 1 else or_lo; break
            if up:
                side, entry = 1, or_hi; break
            if dn:
                side, entry = -1, or_lo; break
        if entry is None:
            return np.nan
        rest_idx = list(rest)
        lo_rest = np.nanmin(La[rest_idx]); hi_rest = np.nanmax(Ha[rest_idx])
        if side == 1:
            stopped = lo_rest <= or_lo
            pnl = (or_lo if stopped else cl) - entry
        else:
            stopped = hi_rest >= or_hi
            pnl = entry - (or_hi if stopped else cl)
        return (pnl - rt) / rng_

    # parity at w0=0 (reproduces primary config)
    par = np.array([exec_win(day, 0) for day in days])
    par = par[~np.isnan(par)]
    parity_ok = abs(par.mean() - obs_mean) < 1e-9
    max_w0 = n_tods - (or_bars + 1)
    if max_w0 < 1:
        return dict(p=np.nan, parity_ok=parity_ok, placebo_mean=np.nan, placebo_p95=np.nan)
    ge = 0
    perm = np.empty(nperm)
    for i in range(nperm):
        ws = rng.integers(1, max_w0 + 1, size=len(days))
        rr = []
        for d, day in enumerate(days):
            v = exec_win(day, int(ws[d]))
            if not np.isnan(v):
                rr.append(v)
        m = float(np.mean(rr)) if rr else np.nan
        perm[i] = m
        if m >= obs_mean:
            ge += 1
    return dict(p=(ge + 1) / (nperm + 1), parity_ok=parity_ok,
                placebo_mean=float(np.nanmean(perm)), placebo_p95=float(np.nanpercentile(perm, 95)))


def slip_to_zero(piv, meta, inst: Instrument, *, or_bars=2,
                 grid=(0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0)):
    """Fill-cliff: meanR as a function of entry slip (instrument points). Returns the
    grid, the meanR at each slip, and the interpolated slip at which meanR crosses 0.
    The cross-instrument tradeability metric = slip_to_zero / spread."""
    means = []
    # scale the grid to the instrument: express grid in MULTIPLES of one spread so the
    # sweep is comparable across instruments of very different point scales.
    sgrid = [g * inst.spread_pt for g in grid] if inst.spread_pt > 0 else list(grid)
    for s in sgrid:
        bt = orb_backtest(piv, meta, inst, or_bars=or_bars, entry_slip_pt=s)
        means.append(float(bt["R"].mean()) if len(bt["R"]) else np.nan)
    means = np.array(means)
    sgrid = np.array(sgrid)
    # interpolate first zero-crossing
    cross = np.nan
    for i in range(len(means) - 1):
        if np.isfinite(means[i]) and np.isfinite(means[i + 1]) and means[i] >= 0 > means[i + 1]:
            frac = means[i] / (means[i] - means[i + 1])
            cross = sgrid[i] + frac * (sgrid[i + 1] - sgrid[i])
            break
    if means[0] < 0:
        cross = 0.0
    return dict(slip_pt=sgrid.tolist(), slip_in_spreads=list(grid), meanR=means.tolist(),
                cross_pt=float(cross) if np.isfinite(cross) else np.nan,
                cross_in_spreads=float(cross / inst.spread_pt) if (np.isfinite(cross) and inst.spread_pt > 0) else np.nan)


# --------------------------------------------------------- FXIFY first-passage MC
def first_passage_mc(trade_R, risk_pct, trades_per_day=1, target=0.05, dd=0.05,
                     daily_loss=0.05, min_days=5, horizon_days=120, n_paths=20_000,
                     block=10, seed=7):
    """Port of harness.first_passage_mc. trade_R = per-trade R series; converted to
    account-fraction via risk_pct (R units * risk_pct). Static FXIFY DD floor."""
    rng = np.random.default_rng(seed)
    trade_pct = np.asarray(trade_R, float) * risk_pct
    N = len(trade_pct)
    if N < block + 1:
        block = max(1, N // 2)
    pool = np.arange(0, N - block + 1)
    tpd = max(1, int(round(trades_per_day)))
    res = {"pass": 0, "bust_static": 0, "bust_daily": 0, "timeout": 0}
    dtp = []
    max_dd = np.empty(n_paths)
    floor = -dd
    for p in range(n_paths):
        need = horizon_days * tpd + tpd
        nblk = int(np.ceil(need / block))
        st = rng.choice(pool, size=nblk)
        stream = (trade_pct[(st[:, None] + np.arange(block)[None, :]).ravel()])[:need]
        eq = peak = 0.0; trough = 0.0; outcome = None; day = 0; i = 0
        while day < horizon_days:
            day += 1; day_start = eq
            for _ in range(tpd):
                eq += stream[i]; i += 1
                peak = max(peak, eq); trough = min(trough, eq - peak)
                if eq <= floor:
                    outcome = "bust_static"; break
                if eq - day_start <= -daily_loss:
                    outcome = "bust_daily"; break
                if eq >= target and day >= min_days:
                    outcome = "pass"; break
            if outcome:
                break
        if outcome is None:
            outcome = "timeout"
        res[outcome] += 1
        if outcome == "pass":
            dtp.append(day)
        max_dd[p] = -trough
    tot = float(n_paths)
    return {"pass": res["pass"] / tot, "bust_static": res["bust_static"] / tot,
            "bust_daily": res["bust_daily"] / tot, "timeout": res["timeout"] / tot,
            "p99_dd": float(np.percentile(max_dd, 99)), "p95_dd": float(np.percentile(max_dd, 95)),
            "median_days_to_pass": float(np.median(dtp)) if dtp else np.nan}
