"""Cross-index relative-volume ranking — cheapest-falsifier necessary-condition pre-screen.

Thread (2026-07-21 prop-fundable-archetype deep-search, open question #3): recover the
Zarattini "Stocks in Play" cross-sectional ORB selection edge by ranking a small universe
of US equity-index futures (ES/NQ/YM/RTY) on opening relative volume and trading the ORB
only on the most "in-play" index each day.

Two NECESSARY conditions for the mechanism to transfer:
  (A) DISPERSION      — the indices' daily relative volume must NOT be near-coincident
                        (if they go in-play/quiet together, a ranking has no material).
  (B) PREDICTIVENESS  — the higher-RV index must, paired within-day, have a bigger move
                        AND a better ORB edge than the lower-RV index (the Stocks-in-Play
                        claim: in-play => better directional follow-through).

Universe we hold intraday = 2 distinct indices (Nasdaq MNQ, Dow MYM) — the widest-spread
US large-cap pair. No ES or RTY intraday (only daily ES cached). If even this pair fails,
adding ES (between them) won't rescue it; RTY (small-cap) would need a real pull.

Notice-phase reconnaissance on cached data — ONE pre-specified necessary condition, not a
mining sweep; no K bound. Routes DROP / DEFER-procurement / GO.
Verdict + numbers: RESULTS.md. Run from repo root.
"""
import numpy as np
import pandas as pd

ET = "America/New_York"
RV_LOOKBACK = 14  # trailing sessions for the relative-volume baseline (Zarattini ~14d)


def load(path):
    df = pd.read_csv(path, parse_dates=["time"]).set_index("time")
    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC")
    df.index = df.index.tz_convert(ET)
    df["day"] = df.index.date
    df["tod"] = df.index.hour * 60 + df.index.minute
    return df


def daily_features(df):
    """One row/session: opening-30m volume, relative volume, ORB edge, post-OR move."""
    rows = []
    for day, g in df.groupby("day", sort=True):
        rth = g[(g["tod"] >= 9 * 60 + 30) & (g["tod"] < 16 * 60)].sort_index()
        if len(rth) < 10:  # half/holiday session
            continue
        opn = rth[rth["tod"].isin([9 * 60 + 30, 9 * 60 + 45])]  # first 30 min = 2 M15 bars
        if len(opn) < 2:
            continue
        or_high, or_low = float(opn["high"].max()), float(opn["low"].min())
        or_end = float(opn.iloc[-1]["close"])
        opening_vol = float(opn["volume"].sum())
        post = rth[rth["tod"] >= 10 * 60].sort_index()
        if len(post) < 2 or or_end <= 0:
            continue
        close = float(post.iloc[-1]["close"])
        signal, entry = 0, np.nan
        for _, b in post.iterrows():
            if b["high"] >= or_high:
                signal, entry = 1, or_high
                break
            if b["low"] <= or_low:
                signal, entry = -1, or_low
                break
        orb_edge = signal * (close / entry - 1.0) if (signal != 0 and entry > 0) else np.nan
        rows.append({"day": pd.Timestamp(day), "opening_vol": opening_vol,
                     "orb_edge": orb_edge, "post_or_abs_move": abs(close / or_end - 1.0)})
    d = pd.DataFrame(rows).set_index("day").sort_index()
    base = d["opening_vol"].rolling(RV_LOOKBACK, min_periods=RV_LOOKBACK).median().shift(1)
    d["rv"] = d["opening_vol"] / base
    return d.dropna(subset=["rv"])


def sign_p(win, n):
    from math import erfc, sqrt
    z = (win - 0.5) / np.sqrt(0.25 / n)
    return erfc(abs(z) / sqrt(2))


def main():
    nq = daily_features(load("core/data/bar_data/MNQ_M15.csv"))
    ym = daily_features(load("core/data/bar_data/MYM_M15.csv"))
    j = nq.join(ym, lsuffix="_nq", rsuffix="_ym", how="inner").dropna(subset=["rv_nq", "rv_ym"])
    print(f"common sessions: {len(j)}  ({j.index.min().date()}..{j.index.max().date()})")

    corr = j["rv_nq"].corr(j["rv_ym"])
    ratio = j["rv_nq"] / j["rv_ym"]
    print("\n(A) DISPERSION")
    print(f"  corr(RV_nq, RV_ym)         = {corr:.3f}")
    print(f"  frac days RV within +/-25% = {((ratio >= 0.8) & (ratio <= 1.25)).mean():.3f}")

    hi_nq = j["rv_nq"] >= j["rv_ym"]
    hi_move = np.where(hi_nq, j["post_or_abs_move_nq"], j["post_or_abs_move_ym"])
    lo_move = np.where(hi_nq, j["post_or_abs_move_ym"], j["post_or_abs_move_nq"])
    hi_edge = np.where(hi_nq, j["orb_edge_nq"], j["orb_edge_ym"])
    lo_edge = np.where(hi_nq, j["orb_edge_ym"], j["orb_edge_nq"])
    md = (hi_move - lo_move)[~(np.isnan(hi_move) | np.isnan(lo_move))]
    ed = (hi_edge - lo_edge)[~(np.isnan(hi_edge) | np.isnan(lo_edge))]
    print("\n(B) PREDICTIVENESS (higher-RV index, paired by day)")
    print(f"  bigger |move|:  win {(md > 0).mean():.3f}  diff {md.mean()*1e4:+.2f} bp  "
          f"(n={md.size}, sign-p={sign_p((md > 0).mean(), md.size):.3f})")
    print(f"  better ORB edge: win {(ed > 0).mean():.3f}  diff {ed.mean()*1e4:+.2f} bp  "
          f"(n={ed.size}, sign-p={sign_p((ed > 0).mean(), ed.size):.3f})")

    print("\n(killer) mean ORB edge by selection rule:")
    print(f"  RV-selected = {np.nanmean(hi_edge)*1e4:+.2f} bp   "
          f"alternating(random) = {np.nanmean(np.where(np.arange(len(j)) % 2 == 0, j['orb_edge_nq'], j['orb_edge_ym']))*1e4:+.2f} bp")
    print(f"  always-MNQ  = {j['orb_edge_nq'].mean()*1e4:+.2f} bp   "
          f"always-MYM = {j['orb_edge_ym'].mean()*1e4:+.2f} bp")


if __name__ == "__main__":
    main()
