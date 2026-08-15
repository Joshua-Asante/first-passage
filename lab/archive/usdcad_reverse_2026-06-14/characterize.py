"""INQHIORI Notice-phase characterization of 15m USDCAD bars (BAR_EXPORT v0.1).

STRICTLY structural/statistical characterization of the INSTRUMENT.
NO strategy PnL, NO rule search, NO profit metric is computed here.
Its only job: tell us which search space is even worth pre-registering.

Run:
    python lab/analysis/usdcad_reverse_2026-06-14/characterize.py [path_to_csv]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

DEFAULT_CSV = Path(
    r"C:/Users/joshu/Downloads/BAR_EXPORT_v0.1_PEPPERSTONE_USDCAD_2026-06-14_506df.csv"
)
PRICE_COL = "Price CAD"
SIGNAL_PIPE_RE = re.compile(
    r"^(?P<epoch>\d+)\|(?P<o>[-\d.]+)\|(?P<h>[-\d.]+)\|(?P<l>[-\d.]+)\|(?P<c>[-\d.]+)\|(?P<v>\d+)$"
)


def hr(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


# ---------------------------------------------------------------- load + step-0
def load_bars(path: Path) -> pd.DataFrame:
    raw = pd.read_csv(path, encoding="utf-8-sig")
    raw.columns = [str(c).strip() for c in raw.columns]
    entries = raw[raw["Type"].astype(str).str.startswith("Entry")].copy()
    rows, skipped, xcheck_fail = [], 0, 0
    for _, row in entries.iterrows():
        sig = str(row.get("Signal", "")).strip()
        m = SIGNAL_PIPE_RE.match(sig)
        if not m:
            skipped += 1
            continue
        o, h, l, c = (float(m.group(k)) for k in ("o", "h", "l", "c"))
        v = float(m.group("v"))
        epoch_ms = int(m.group("epoch"))
        # cross-check: entry fill price (process_orders_on_close) == encoded close
        try:
            entry_px = float(row[PRICE_COL])
            if abs(entry_px - c) > max(1e-5, c * 1e-4):
                xcheck_fail += 1
        except (KeyError, ValueError):
            pass
        rows.append(
            {
                "epoch_ms": epoch_ms,
                # epoch == ET-wall-clock-as-UTC per user statement; read as naive ET
                "time": pd.to_datetime(epoch_ms, unit="ms"),
                "dt_str": str(row["Date and time"]),
                "open": o, "high": h, "low": l, "close": c, "volume": v,
            }
        )
    df = pd.DataFrame(rows).sort_values("time").reset_index(drop=True)
    df.attrs["skipped"] = skipped
    df.attrs["xcheck_fail"] = xcheck_fail
    return df


def step0(df: pd.DataFrame) -> None:
    hr("STEP-0  PANEL INTEGRITY")
    n = len(df)
    print(f"bars (Entry rows decoded): {n}")
    print(f"skipped (no pipe signal):  {df.attrs['skipped']}")
    print(f"span: {df['time'].min()}  ->  {df['time'].max()}")
    print(f"calendar days span:        {(df['time'].max() - df['time'].min()).days}")

    # epoch vs Date-and-time string agreement
    dts = pd.to_datetime(df["dt_str"])
    agree = (dts.values == df["time"].values).mean()
    print(f"epoch == 'Date and time' string agreement: {agree*100:.2f}%  "
          f"(=> epoch is ET-wall-clock-labelled, not true UTC)")

    # timeframe census
    minutes = df["time"].dt.minute.value_counts().sort_index()
    print(f"minute-of-hour census: {dict(minutes)}  (15m => only 0/15/30/45)")
    deltas = df["time"].diff().dropna()
    dmin = (deltas.dt.total_seconds() / 60)
    print(f"bar-delta census (min): {dict(dmin.value_counts().sort_index().head(10))}")
    print(f"  contiguous 15m steps: {(dmin == 15).sum()} / {len(dmin)} "
          f"({(dmin==15).mean()*100:.1f}%)")

    # OHLC sanity
    bad_hi = (df["high"] < df[["open", "close"]].max(axis=1)).sum()
    bad_lo = (df["low"] > df[["open", "close"]].min(axis=1)).sum()
    bad_hl = (df["high"] < df["low"]).sum()
    nonpos = (df[["open", "high", "low", "close"]] <= 0).sum().sum()
    print(f"OHLC sanity: high<max(o,c)={bad_hi}, low>min(o,c)={bad_lo}, "
          f"high<low={bad_hl}, nonpositive={nonpos}")
    print(f"price-vs-close cross-check failures: {df.attrs['xcheck_fail']}")

    # duplicates / monotonic
    print(f"duplicate timestamps: {df['time'].duplicated().sum()}")
    print(f"strictly increasing time: {df['time'].is_monotonic_increasing}")

    # weekday + hour census (ET assumed)
    print("\nweekday census (0=Mon..6=Sun):")
    print(df["time"].dt.dayofweek.value_counts().sort_index().to_string())
    print("\nbars-per-ET-day quantiles:",
          df.groupby(df["time"].dt.date).size().describe()[["min", "25%", "50%", "75%", "max"]].round(1).to_dict())

    # weekend gap structure -> confirm ET (FX: Fri 17:00 close -> Sun 17:00 open)
    hr("WEEKEND / SESSION GAP STRUCTURE (confirms timezone)")
    big = df.assign(gap=dmin.reindex(df.index).values)
    gaps = big[big["gap"] > 60].copy()
    gaps["prev_time"] = df["time"].shift(1).reindex(gaps.index).values
    print(f"gaps > 60min: {len(gaps)}")
    sample = gaps.head(12)
    for _, g in sample.iterrows():
        pt = pd.Timestamp(g["prev_time"])
        ct = pd.Timestamp(g["time"])
        print(f"  close {pt:%a %Y-%m-%d %H:%M} -> open {ct:%a %Y-%m-%d %H:%M}  "
              f"(gap {g['gap']/60:.1f}h)")
    # typical weekend close/open hour
    we = gaps[gaps["gap"] > 600]
    if len(we):
        cl = pd.to_datetime(we["prev_time"])
        op = pd.to_datetime(we["time"])
        print(f"\nweekend close hour mode: {cl.dt.hour.mode().tolist()} "
              f"(ET expect 17); open hour mode: {op.dt.hour.mode().tolist()} (ET expect 17)")

    # DST boundary check (US spring-forward 2026-03-08)
    hr("DST BOUNDARY CHECK (2026-03-08 US spring-forward)")
    for lbl, lo, hid in [("pre-DST  (Feb)", "2026-02-09", "2026-02-28"),
                         ("post-DST (Apr)", "2026-04-01", "2026-04-20")]:
        seg = df[(df["time"] >= lo) & (df["time"] < hid)]
        if not len(seg):
            continue
        daily = seg.groupby(seg["time"].dt.date)["time"]
        first_h = daily.min().dt.hour
        last_h = daily.max().dt.hour
        print(f"{lbl}: first-bar hr mode={first_h.mode().tolist()}, "
              f"last-bar hr mode={last_h.mode().tolist()}")
    print("(if first/last hour identical pre vs post => labels are fixed ET wall-clock)")


# ----------------------------------------------------- contiguous return series
def contiguous_logret(df: pd.DataFrame):
    """log returns over strictly-15min-contiguous pairs; cross-gap -> NaN."""
    lc = np.log(df["close"].to_numpy())
    r = np.diff(lc)
    dt = df["time"].diff().dt.total_seconds().to_numpy()[1:] / 60.0
    r = np.where(dt == 15.0, r, np.nan)
    return r  # length n-1, aligned to df index 1..n-1


def acf(x: np.ndarray, lags: int):
    x = x[~np.isnan(x)]
    x = x - x.mean()
    n = len(x)
    denom = np.dot(x, x)
    out = []
    for k in range(1, lags + 1):
        out.append(np.dot(x[:-k], x[k:]) / denom)
    return np.array(out), n


def variance_ratio(r: np.ndarray, q: int):
    """Lo-MacKinlay overlapping VR with heteroskedasticity-robust z.
    Only q-windows fully inside a contiguous (no-NaN) run are used."""
    mask = ~np.isnan(r)
    mu = np.nanmean(r)
    # 1-period variance (unbiased)
    r1 = r[mask] - mu
    var1 = np.dot(r1, r1) / (len(r1) - 1)
    # q-period overlapping sums where all q components valid
    valid_q = np.convolve(mask.astype(int), np.ones(q, int), mode="valid") == q
    # rolling sum of returns (NaN-safe: only where valid)
    rfill = np.where(mask, r - mu, 0.0)
    csum = np.cumsum(np.insert(rfill, 0, 0.0))
    qsum = csum[q:] - csum[:-q]
    qsum = qsum[valid_q]
    m = len(qsum)
    if m < 5 or var1 == 0:
        return np.nan, np.nan, m
    varq = np.dot(qsum, qsum) / m  # mean of squared (mean already removed)
    vr = (varq / q) / var1
    # heteroskedasticity-robust asymptotic variance (Lo-MacKinlay 1988)
    rr = r1
    nobs = len(rr)
    phi = 0.0
    for j in range(1, q):
        w = 2.0 * (q - j) / q
        delta = np.dot(rr[j:], rr[:-j]) ** 2 / (np.dot(rr, rr)) ** 2 * nobs
        phi += (w ** 2) * delta
    z = (vr - 1.0) / np.sqrt(phi / nobs) if phi > 0 else np.nan
    return vr, z, m


def hurst_rs(r: np.ndarray):
    """R/S Hurst on RETURNS (increments), NOT log prices (memory: log-price -> spurious H~1)."""
    x = r[~np.isnan(r)]
    n = len(x)
    if n < 256:
        return np.nan
    sizes = [2 ** k for k in range(4, int(np.log2(n)))]
    rs_means = []
    for w in sizes:
        nseg = n // w
        rs = []
        for s in range(nseg):
            seg = x[s * w:(s + 1) * w]
            z = seg - seg.mean()
            Z = np.cumsum(z)
            R = Z.max() - Z.min()
            S = seg.std(ddof=1)
            if S > 0:
                rs.append(R / S)
        if rs:
            rs_means.append((w, np.mean(rs)))
    if len(rs_means) < 4:
        return np.nan
    lw = np.log([w for w, _ in rs_means])
    lr = np.log([v for _, v in rs_means])
    H = np.polyfit(lw, lr, 1)[0]
    return H


def return_structure(df: pd.DataFrame) -> None:
    hr("RETURN STRUCTURE  (trend vs mean-reversion)  -- 15m log returns")
    r = contiguous_logret(df)
    rv = r[~np.isnan(r)]
    print(f"valid 15m returns: {len(rv)} (of {len(r)})")
    print(f"mean={rv.mean():.2e}  std={rv.std():.2e}  "
          f"skew={stats.skew(rv):.3f}  exkurt={stats.kurtosis(rv):.2f}")
    print(f"std in pips (~1e-4): {rv.std()/1e-4:.2f} pips/bar  "
          f"| daily(~96 bars) ~{rv.std()*np.sqrt(96)/1e-4:.0f} pips")

    a, n = acf(r, 20)
    ci = 1.96 / np.sqrt(n)
    print(f"\nACF of returns (CI +/-{ci:.4f}):")
    for k in [1, 2, 3, 4, 5, 8, 12, 16, 20]:
        flag = "*" if abs(a[k - 1]) > ci else " "
        print(f"  lag{k:>2}: {a[k-1]:+.4f} {flag}")

    print("\nVariance-Ratio test (VR<1 mean-revert, VR>1 trend; |z|>1.96 sig):")
    for q in [2, 4, 8, 16, 32, 48, 96]:
        vr, z, m = variance_ratio(r, q)
        tag = "MR" if vr < 1 else "TREND"
        sig = "SIG" if (not np.isnan(z) and abs(z) > 1.96) else ""
        print(f"  q={q:>3}: VR={vr:.3f}  z={z:+.2f}  [{tag} {sig}]  (m={m})")

    H = hurst_rs(r)
    print(f"\nHurst (R/S on returns): H={H:.3f}  "
          f"(<0.5 mean-revert, ~0.5 random, >0.5 trend)")

    # vol clustering
    aa, _ = acf(np.abs(r), 20)
    print(f"\nACF of |returns| (vol clustering) lag1={aa[0]:+.3f} "
          f"lag5={aa[4]:+.3f} lag20={aa[19]:+.3f}")


def higher_tf(df: pd.DataFrame) -> None:
    hr("HIGHER-TIMEFRAME PERSISTENCE (1H / 4H / daily close-to-close)")
    s = df.set_index("time")["close"]
    for rule, label in [("1h", "1H"), ("4h", "4H"), ("1D", "daily")]:
        c = s.resample(rule).last().dropna()
        r = np.diff(np.log(c.to_numpy()))
        if len(r) < 30:
            print(f"{label}: too few ({len(r)})")
            continue
        a, n = acf(r, 5)
        ci = 1.96 / np.sqrt(n)
        vr2, z2, _ = variance_ratio(r, 2)
        print(f"{label}: n={n}  ACF lag1={a[0]:+.3f}(CI{ci:.3f})  "
              f"lag2={a[1]:+.3f}  VR(2)={vr2:.3f} z={z2:+.2f}")


def session_profile(df: pd.DataFrame) -> None:
    hr("SESSION / HOUR STRUCTURE  (where do moves & range concentrate?)  ET")
    d = df.copy()
    d["ret"] = np.log(d["close"]) - np.log(d["open"])  # intrabar
    d["absret"] = d["ret"].abs()
    d["range_pips"] = (d["high"] - d["low"]) / 1e-4
    d["hour"] = d["time"].dt.hour
    by_h = d.groupby("hour").agg(
        n=("ret", "size"),
        mean_absret_pips=("absret", lambda x: x.mean() / 1e-4),
        mean_range_pips=("range_pips", "mean"),
        ret_std_pips=("ret", lambda x: x.std() / 1e-4),
    )
    print("hour(ET)  n   |ret|pips  range_pips  std_pips")
    for h, row in by_h.iterrows():
        bar = "#" * int(row["mean_range_pips"] / by_h["mean_range_pips"].max() * 30)
        print(f"  {h:>2}   {int(row['n']):>4}  {row['mean_absret_pips']:>7.2f}   "
              f"{row['mean_range_pips']:>7.2f}   {row['ret_std_pips']:>6.2f}  {bar}")

    # session buckets (ET): Asia 18-02, London 02-08, NY-AM overlap 08-12, NY-PM 12-17
    def bucket(h):
        if 2 <= h < 8:
            return "London 02-08"
        if 8 <= h < 12:
            return "NY-AM  08-12"
        if 12 <= h < 17:
            return "NY-PM  12-17"
        return "Asia   17-02"
    d["sess"] = d["hour"].map(bucket)
    print("\nby session bucket:")
    bs = d.groupby("sess").agg(
        n=("ret", "size"),
        mean_range_pips=("range_pips", "mean"),
        ret_std_pips=("ret", lambda x: x.std() / 1e-4),
    )
    print(bs.round(2).to_string())

    print("\nby weekday (0=Mon):")
    d["wd"] = d["time"].dt.dayofweek
    wd = d.groupby("wd").agg(
        n=("ret", "size"),
        mean_range_pips=("range_pips", "mean"),
        ret_std_pips=("ret", lambda x: x.std() / 1e-4),
    )
    print(wd.round(2).to_string())


def vol_and_range(df: pd.DataFrame) -> None:
    hr("VOLATILITY & DAILY RANGE")
    d = df.copy()
    tr = pd.concat([
        d["high"] - d["low"],
        (d["high"] - d["close"].shift()).abs(),
        (d["low"] - d["close"].shift()).abs(),
    ], axis=1).max(axis=1)
    atr = tr.rolling(14).mean()
    d["atr"] = atr
    print(f"ATR(14) pips: median={atr.median()/1e-4:.1f}  "
          f"p10={atr.quantile(.1)/1e-4:.1f}  p90={atr.quantile(.9)/1e-4:.1f}")
    print(f"ATR/price (relative): median={ (atr/d['close']).median()*1e4:.2f} bp")
    # daily range
    g = d.groupby(d["time"].dt.date)
    drange = (g["high"].max() - g["low"].min()) / 1e-4
    print(f"daily range pips: median={drange.median():.0f}  "
          f"p10={drange.quantile(.1):.0f}  p90={drange.quantile(.9):.0f}")
    # monthly vol (regime within window)
    d["ym"] = d["time"].dt.to_period("M")
    r = contiguous_logret(d)
    d = d.iloc[1:].assign(r=r)
    mv = d.groupby("ym")["r"].agg(lambda x: np.nanstd(x) / 1e-4)
    print("\nmonthly 15m return std (pips) -- intra-window regime drift:")
    print(mv.round(2).to_string())


def cost_law(df: pd.DataFrame) -> None:
    hr("COST-LAW HURDLE (durable finding #1: cost-in-R ~ price/stop_dist)")
    d = df.copy()
    tr = (d["high"] - d["low"])
    atr = tr.rolling(14).mean().median()
    price = d["close"].median()
    print(f"median price={price:.4f}  median ATR(15m)~{atr/1e-4:.1f} pips")
    # assumed round-trip explicit cost for USDCAD on Pepperstone (spread+commission)
    # raw-spread ~0.6 pip typical + commission ~0.7 pip/RT => ~1.0-1.6 pip RT; sweep it
    print("cost-in-R = RT_cost_price / stop_dist, stop = k*ATR")
    print(f"{'k*ATR':>6} {'stop_pips':>9}  " + "  ".join(f"RT={c}p" for c in (0.8, 1.2, 1.6, 2.4)))
    for k in (1.0, 1.5, 2.0, 2.5, 3.0):
        stop = k * atr
        cells = []
        for cpips in (0.8, 1.2, 1.6, 2.4):
            cost_price = cpips * 1e-4
            cells.append(f"{cost_price/stop:>5.3f}R")
        print(f"{k:>6.1f} {stop/1e-4:>9.1f}  " + "  ".join(cells))
    print("\nskill convention: target expectancy >= 4x hurdle. "
          "Tight stops (k<=1.5) pay a structural tax; this bounds the search.")


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_CSV
    print(f"FILE: {path}")
    df = load_bars(path)
    step0(df)
    return_structure(df)
    higher_tf(df)
    session_profile(df)
    vol_and_range(df)
    cost_law(df)
    hr("DONE  (characterization only -- no strategy PnL computed)")


if __name__ == "__main__":
    main()
