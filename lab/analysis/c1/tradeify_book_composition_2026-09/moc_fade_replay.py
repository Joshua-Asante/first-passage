"""Bar-level replay of MES_MOC_fade_v0_1.pine Table mode on real MES bars.

Data   : Databento GLBX.MDP3 MES.v.0 ohlcv-1m (volume-rolled = TV MES1! equivalent,
         per lesson_roll_rule_changes_bar_existence), 2025-03-02..2026-09-01, $0 pull.
         Decoded with map_symbols=False; verified interval-START stamps, one
         instrument_id per session inside 16:00-16:45 ET (no roll in-window).
Signal : moc_imbalance_daily.csv -- FinancialJuice S&P 500 MOC imbalance, $mln,
         + = buy-side. Fade: buy-side -> SHORT, sell-side -> LONG.

Execution, matched to the Pine on 5m bars (bar stamped T covers T..T+5, closes T+5):
  signal bar   = first bar closing >= 16:01  -> bar stamped 16:00
  entry fill   = OPEN of bar stamped 16:05   (market order fills at next bar's open)
  stop/target  = generated at the close of the bar the entry executes on, so first
                 fillable on the bar stamped 16:10 (PESSIMISTIC, the repo's standing
                 rule -- lesson_tv_exit_cannot_fill_on_entry_bar). An OPTIMISTIC
                 variant (live from the entry bar) is reported alongside.
  flatten      = close_all at the close of the bar stamped 16:35 -> fills at the
                 OPEN of the bar stamped 16:40
  same bar holding both stop and target -> STOP fills (adverse-first)
  a stop gapped through fills at the worse of the level and that bar's open
Costs  : $0.91/side commission ($1.82 RT = 0.364 MES pts). Slippage variant: 1 tick
         ($0.25) on entry and on any market/stop exit; limit-target fills take none.
Specs  : MES $5/point, tick 0.25 ($1.25). Stop 6.0 pts = $30/contract = 1R.
"""
from __future__ import annotations

import csv, json, os, sys
import numpy as np
import pandas as pd
import databento as db

HERE = os.path.dirname(os.path.abspath(__file__))
DBN = r"C:\Users\joshu\.databento_cache\ohlcv-1m_continuous_4421daf2a29d7cd8.dbn"
# The scraped signal lives in the campaign's gitignored inputs/ (see scrape/README.md), which
# is where the documented workflow puts it -- resolve it there, not from the caller's cwd.
CSV = os.path.join(HERE, "inputs", "moc_imbalance_daily.csv")
DOWNLOADS = r"C:\Users\joshu\Downloads"   # vendor TV exports, uncommitted (see README)
TZ = "America/New_York"
PT_USD = 5.0
TICK = 0.25
COMM_RT_PTS = 1.82 / PT_USD          # 0.364 pts
SLIP_PTS = TICK                      # per market/stop side


def load_bars(tf_min: int) -> pd.DataFrame:
    d = db.DBNStore.from_file(DBN).to_df(map_symbols=False)
    et = d.index.tz_convert(TZ)
    d = d.assign(et=et, day=et.normalize().tz_localize(None),
                 mins=et.hour * 60 + et.minute)
    d = d[(d.mins >= 16 * 60) & (d.mins < 17 * 60)]
    if tf_min == 1:
        d = d.assign(bucket=d.mins)
        g = d
    else:
        d = d.assign(bucket=(d.mins // tf_min) * tf_min)
        g = (d.groupby(["day", "bucket"])
               .agg(open=("open", "first"), high=("high", "max"),
                    low=("low", "min"), close=("close", "last"),
                    volume=("volume", "sum"), n1m=("close", "size"))
               .reset_index())
    if tf_min == 1:
        g = g.reset_index()[["day", "bucket", "open", "high", "low", "close", "volume"]]
        g["n1m"] = 1
    return g.sort_values(["day", "bucket"]).reset_index(drop=True)


def load_signal():
    rows = []
    for r in csv.DictReader(open(CSV, encoding="utf-8")):
        if not r["sp500_mln"]:
            continue
        rows.append((pd.Timestamp(r["date"]), float(r["sp500_mln"]), r["sign_source"]))
    return pd.DataFrame(rows, columns=["day", "imb_mln", "sign_source"])


def replay(bars, sig, tf_min, stop_pts=6.0, target_r=0.75, min_abs_mln=500.0,
           pess=True, use_target=True, explicit_only=True):
    """-> DataFrame, one row per taken session.

    `explicit_only` defaults TRUE: rows whose sign came from the colour marker the Telegram
    mirror drops are unusable, and a default that traded them regenerated contaminated
    results (Codex review, PR #260). Pass False only to reproduce that contamination
    deliberately.
    """
    entry_b = 16 * 60 + tf_min                    # bar whose OPEN is the fill
    # Pine: close_all is submitted at the CLOSE of the first bar B whose (close + one bar)
    # would pass flat-by, i.e. (B + tf) + tf > 16:44, and it fills at the NEXT bar's OPEN.
    # So the submit bar is still exposed (stop/target live) and the fill is one bar later.
    # The earlier `> 1004 - 2*tf` expression returned the SUBMIT bar and priced the exit at
    # its open -- one bar (5 min) early on every time exit, and it also dropped the submit
    # bar from the stop/target window. Fixed 2026-09-02.
    submit_b = min(b for b in sorted(bars.bucket.unique()) if (b + tf_min) + tf_min > 16 * 60 + 44)
    flat_b = submit_b + tf_min                    # bar whose OPEN is the flatten fill
    first_exit_b = entry_b + (tf_min if pess else 0)
    by_day = {d: g for d, g in bars.groupby("day")}
    out = []
    for _, s in sig.iterrows():
        if explicit_only and s.sign_source != "explicit":
            continue
        if abs(s.imb_mln) < min_abs_mln:
            continue
        g = by_day.get(s.day)
        if g is None:
            continue
        gi = g.set_index("bucket")
        if entry_b not in gi.index or flat_b not in gi.index:
            continue
        side = -1 if s.imb_mln > 0 else 1        # fade: buy-side imbalance -> short
        fill = float(gi.at[entry_b, "open"])
        stop = fill - side * stop_pts
        tgt = fill + side * stop_pts * target_r
        exit_px, exit_kind, exit_b = None, None, None
        for b in [x for x in gi.index if first_exit_b <= x <= submit_b]:
            hi, lo, op = float(gi.at[b, "high"]), float(gi.at[b, "low"]), float(gi.at[b, "open"])
            hit_stop = (lo <= stop) if side > 0 else (hi >= stop)
            hit_tgt = use_target and ((hi >= tgt) if side > 0 else (lo <= tgt))
            if hit_stop:                          # adverse-first
                exit_px = min(stop, op) if side > 0 else max(stop, op)
                exit_kind, exit_b = "stop", b
                break
            if hit_tgt:
                exit_px, exit_kind, exit_b = tgt, "target", b
                break
        if exit_px is None:
            exit_px, exit_kind, exit_b = float(gi.at[flat_b, "open"]), "time", flat_b
        gross = side * (exit_px - fill)
        slip = SLIP_PTS * (1 if exit_kind == "target" else 2)   # entry always; exit unless limit
        out.append(dict(day=s.day, imb_mln=s.imb_mln, sign_source=s.sign_source, side=side,
                        fill=fill, exit_px=exit_px, exit_kind=exit_kind, exit_bucket=exit_b,
                        gross_pts=gross, net_pts=gross - COMM_RT_PTS,
                        net_slip_pts=gross - COMM_RT_PTS - slip))
    return pd.DataFrame(out)


def shape(t, stop_pts=6.0, label="", span_weekdays=None):
    if not len(t):
        return {"label": label, "n": 0}
    n = len(t)
    # Cadence must be measured over the OBSERVATION SPAN, not over the traded days: there is
    # one row per traded day, so n / (unique days / 5) is identically 5.0 and told us nothing
    # (Codex review, PR #260). span_weekdays = weekdays between the first and last signal.
    d = {"label": label, "n": n,
         "per_week": (round(5.0 * n / span_weekdays, 2) if span_weekdays else None),
         "span_weekdays": span_weekdays}
    for col, tag in (("gross_pts", "gross"), ("net_pts", "net"), ("net_slip_pts", "netslip")):
        v = t[col].to_numpy()
        w, l = v[v > 0], v[v <= 0]
        d[f"{tag}_wr"] = round(100 * len(w) / n, 1)
        d[f"{tag}_mean_R"] = round(float(v.mean()) / stop_pts, 4)
        d[f"{tag}_meanwin_R"] = round(float(w.mean()) / stop_pts, 3) if len(w) else None
        d[f"{tag}_meanloss_R"] = round(float(l.mean()) / stop_pts, 3) if len(l) else None
        d[f"{tag}_pf"] = round(float(w.sum() / -l.sum()), 3) if len(l) and l.sum() < 0 else None
        d[f"{tag}_total_usd"] = round(float(v.sum()) * PT_USD, 0)
        d[f"{tag}_t"] = round(float(v.mean() / (v.std(ddof=1) / np.sqrt(n))), 2) if n > 2 and v.std() > 0 else None
    d["exit_mix"] = dict(t.exit_kind.value_counts())
    d["long_short"] = {"long": int((t.side > 0).sum()), "short": int((t.side < 0).sum())}
    return d


def _span_weekdays(a, b):
    return int(len(pd.bdate_range(a, b)))


def main():
    sig_all = load_signal()
    sig = sig_all[sig_all.sign_source == "explicit"].reset_index(drop=True)
    span = _span_weekdays(sig_all.day.min(), sig_all.day.max())
    print(f"signal rows: {len(sig_all)} scraped, {len(sig)} VERIFIED-SIGN (used); "
          f"{len(sig_all) - len(sig)} dropped -- their sign lived in a colour marker the "
          f"Telegram mirror renders as a plain exclamation mark")
    print(f"span {sig_all.day.min().date()}..{sig_all.day.max().date()} = {span} weekdays")
    res = {}
    for tf in (5, 1):
        bars = load_bars(tf)
        for pess in (True, False):
            for use_target in (True, False):
                for mn in (500.0, 0.0):
                    t = replay(bars, sig, tf, pess=pess, use_target=use_target, min_abs_mln=mn)
                    key = (f"tf{tf}m_{'pess' if pess else 'optim'}"
                           f"_{'tgt' if use_target else 'notgt'}_flt{int(mn)}")
                    res[key] = {"shape": shape(t, label=key, span_weekdays=span), "trades": t}
                    s = res[key]["shape"]
                    print(f"{key:34} n={s['n']:4} {s['per_week']:.2f}/wk  "
                          f"WR(net)={s.get('net_wr')}%  meanR={s.get('net_mean_R'):+.4f}  "
                          f"PF={s.get('net_pf')}  t={s.get('net_t')}  ${s.get('net_total_usd')}")

    hl = "tf5m_pess_tgt_flt500"
    t = res[hl]["trades"]
    mid = t.day.quantile(0.5)
    h1, h2 = t[t.day <= mid], t[t.day > mid]
    print(f"\nHEADLINE {hl}")
    print(json.dumps(res[hl]["shape"], indent=1, default=str))
    sh1 = shape(h1, label=f"H1 <= {mid.date()}",
                span_weekdays=_span_weekdays(h1.day.min(), h1.day.max()))
    sh2 = shape(h2, label=f"H2 > {mid.date()}",
                span_weekdays=_span_weekdays(h2.day.min(), h2.day.max()))
    print("H1", json.dumps(sh1, indent=1, default=str))
    print("H2", json.dumps(sh2, indent=1, default=str))

    # Pure directional-information test on the raw window return (no stop, no target, no size
    # filter) over the VERIFIED-SIGN sessions: does the imbalance sign predict 16:05 -> 16:40?
    bars5 = load_bars(5)
    by_day = {d: g.set_index("bucket") for d, g in bars5.groupby("day")}
    raw = []
    for _, s in sig.iterrows():
        gi = by_day.get(s.day)
        if gi is None or (16 * 60 + 5) not in gi.index or (16 * 60 + 40) not in gi.index:
            continue
        a = float(gi.at[16 * 60 + 5, "open"])
        b = float(gi.at[16 * 60 + 40, "open"])
        raw.append((s.day, s.imb_mln, b - a))
    R = pd.DataFrame(raw, columns=["day", "imb_mln", "ret_pts"])
    faded = -np.sign(R.imb_mln) * R.ret_pts
    n = len(R)
    m = float(faded.mean())
    sd = float(faded.std(ddof=1))
    se = sd / np.sqrt(n)
    STOP = 6.0
    info = {"n": n, "mean_faded_pts": round(m, 4), "t": round(m / se, 2),
            "mean_faded_R": round(m / STOP, 4),
            "ci95_R": [round((m - 1.96 * se) / STOP, 4), round((m + 1.96 * se) / STOP, 4)],
            "sigma_pts": round(sd, 2),
            "cost_hurdle_4x_commission_pts": round(4 * COMM_RT_PTS, 2),
            "cost_hurdle_b1_crossing_model_pts": 3.46,
            "corr_signed_imb_vs_ret": round(float(np.corrcoef(R.imb_mln, R.ret_pts)[0, 1]), 4),
            "corr_absimb_vs_faded": round(float(np.corrcoef(R.imb_mln.abs(), faded)[0, 1]), 4),
            "n_for_80pct_power_at_0.10R": int((2.8 * sd / (0.10 * STOP)) ** 2)}
    print(f"\nDIRECTIONAL INFO TEST (verified-sign, n={n}, raw 16:05->16:40, no stop/target/filter)")
    print(json.dumps(info, indent=1))

    print("  scaling by |imbalance| -- a forced dealer unwind must strengthen with size:")
    buckets = {}
    for lo, hi in ((0, 500), (500, 1000), (1000, 2000), (2000, 10 ** 9)):
        q = R[(R.imb_mln.abs() >= lo) & (R.imb_mln.abs() < hi)]
        if len(q) > 5:
            f2 = -np.sign(q.imb_mln) * q.ret_pts
            key = f"{lo}-{hi if hi < 10 ** 9 else 'inf'}"
            buckets[key] = {"n": int(len(q)), "mean_faded_pts": round(float(f2.mean()), 3),
                            "t": round(float(f2.mean() / (f2.std(ddof=1) / np.sqrt(len(q)))), 2)}
            print(f"    |imb| {key:>10} $mln: n={len(q):3} "
                  f"mean {f2.mean():+.3f} pts  t={buckets[key]['t']:+.2f}")

    halves_info = {}
    h = n // 2
    for nm, part in (("h1", R.iloc[:h]), ("h2", R.iloc[h:])):
        f2 = -np.sign(part.imb_mln) * part.ret_pts
        halves_info[nm] = {"n": int(len(part)), "start": str(part.day.min().date()),
                           "end": str(part.day.max().date()),
                           "mean_faded_pts": round(float(f2.mean()), 3),
                           "t": round(float(f2.mean() / (f2.std(ddof=1) / np.sqrt(len(part)))), 2)}
        print(f"    {nm} {halves_info[nm]['start']}..{halves_info[nm]['end']}: "
              f"mean {halves_info[nm]['mean_faded_pts']:+.3f} pts t={halves_info[nm]['t']:+.2f}")

    # correlation with the MNQ recon leg's daily P&L (per contract), parsed directly from the
    # same export the book grid used (no engine import needed)
    mnq_csv = os.path.join(DOWNLOADS, "ORB-MNQ-1_recon_v7_CME_MINI_MNQ1!_2026-08-31_70648.csv")
    acc = {}
    for r in csv.DictReader(open(mnq_csv, encoding="utf-8-sig")):
        if not r["Type"].startswith("Exit"):
            continue
        dd = pd.Timestamp(r["Date and time"].split(" ")[0])
        acc[dd] = acc.get(dd, 0.0) + float(r["Net PnL USD"]) / float(r["Size (qty)"])
    mnq = pd.Series(acc).sort_index()
    moc = t.set_index("day")["net_pts"] * PT_USD
    idx = pd.bdate_range(min(moc.index.min(), mnq.index.min()),
                        max(moc.index.max(), mnq.index.max()))
    a = moc.reindex(idx, fill_value=0.0)
    b = mnq.reindex(idx, fill_value=0.0)
    both = (a != 0) & (b != 0)
    corr_active = float(np.corrcoef(a[both], b[both])[0, 1]) if both.sum() > 10 else None
    la, lb = (a < 0), (b < 0)
    print(f"\ncorr with MNQ recon (days both traded, n={int(both.sum())}): {corr_active:+.3f}")
    print(f"joint-loss days {float((la & lb).mean()):.4f} "
          f"vs independence {float(la.mean() * lb.mean()):.4f}")

    out = {k: v["shape"] for k, v in res.items()}
    out["verified_sign_only"] = True
    out["signal_rows_scraped"] = int(len(sig_all))
    out["signal_rows_used"] = int(len(sig))
    out["span_weekdays"] = span
    out["halves"] = {"mid": str(mid.date()), "h1": sh1, "h2": sh2}
    out["directional_info_test"] = info
    out["imbalance_size_buckets"] = buckets
    out["directional_halves"] = halves_info
    out["corr_mnq_active_days"] = corr_active
    json.dump(out, open(os.path.join(HERE, "data", "moc_fade_replay_results.json"), "w"),
              indent=1, default=str)
    t.to_csv(os.path.join(HERE, "data", "moc_fade_trades_headline.csv"), index=False)
    print("\nwrote data/moc_fade_replay_results.json, data/moc_fade_trades_headline.csv")


if __name__ == "__main__":
    main()
