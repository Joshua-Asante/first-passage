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

DBN = r"C:\Users\joshu\.databento_cache\ohlcv-1m_continuous_4421daf2a29d7cd8.dbn"
CSV = "moc_imbalance_daily.csv"
GRID = r"C:\Users\joshu\multi_firm_operations\lab\analysis\c1\tradeify_book_composition_2026-09"
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
           pess=True, use_target=True, explicit_only=False):
    """-> DataFrame, one row per taken session."""
    entry_b = 16 * 60 + tf_min                    # bar whose OPEN is the fill
    flat_b = 16 * 60 + 44 - ((16 * 60 + 44 - entry_b) % tf_min) - (tf_min - 1) % tf_min
    # flatten fill bar: first bar B with (B + tf) + tf > 16:44  =>  B > 1004 - 2*tf
    flat_b = min(b for b in sorted(bars.bucket.unique()) if b > (16 * 60 + 44) - 2 * tf_min)
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
        for b in [x for x in gi.index if first_exit_b <= x < flat_b]:
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


def shape(t, stop_pts=6.0, label=""):
    if not len(t):
        return {"label": label, "n": 0}
    n = len(t)
    for col, tag in (("gross_pts", "gross"), ("net_pts", "net"), ("net_slip_pts", "net_slip")):
        pass
    d = {"label": label, "n": n,
         "per_week": round(n / (len(t.day.unique()) / 5.0) if n else 0, 2)}
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


def main():
    sig = load_signal()
    print(f"signal rows: {len(sig)}  span {sig.day.min().date()}..{sig.day.max().date()}")
    res = {}
    for tf in (5, 1):
        bars = load_bars(tf)
        for pess in (True, False):
            for use_target in (True, False):
                for mn in (500.0, 0.0):
                    t = replay(bars, sig, tf, pess=pess, use_target=use_target, min_abs_mln=mn)
                    key = f"tf{tf}m_{'pess' if pess else 'optim'}_{'tgt' if use_target else 'notgt'}_flt{int(mn)}"
                    res[key] = {"shape": shape(t, label=key), "trades": t}
                    s = res[key]["shape"]
                    print(f"{key:34} n={s['n']:4} WR(net)={s.get('net_wr')}%  meanR={s.get('net_mean_R')}  "
                          f"PF={s.get('net_pf')}  t={s.get('net_t')}  ${s.get('net_total_usd')}")
    # halves + correlation on the headline cell
    hl = "tf5m_pess_tgt_flt500"
    t = res[hl]["trades"]
    mid = t.day.quantile(0.5)
    h1, h2 = t[t.day <= mid], t[t.day > mid]
    print(f"\nHEADLINE {hl}")
    print(json.dumps(res[hl]["shape"], indent=1, default=str))
    print("H1", json.dumps(shape(h1, label=f"H1 <= {mid.date()}"), indent=1, default=str))
    print("H2", json.dumps(shape(h2, label=f"H2 > {mid.date()}"), indent=1, default=str))
    # Pure directional-information test on the raw window return (no stop, no target,
    # no filter): does the imbalance sign predict 16:05 -> 16:40 at all?
    bars5 = load_bars(5)
    by_day = {d: g.set_index("bucket") for d, g in bars5.groupby("day")}
    raw = []
    for _, s in sig.iterrows():
        gi = by_day.get(s.day)
        if gi is None or (16 * 60 + 5) not in gi.index or (16 * 60 + 40) not in gi.index:
            continue
        a = float(gi.at[16 * 60 + 5, "open"]); b = float(gi.at[16 * 60 + 40, "open"])
        raw.append((s.day, s.imb_mln, b - a))
    R = pd.DataFrame(raw, columns=["day", "imb_mln", "ret_pts"])
    faded = -np.sign(R.imb_mln) * R.ret_pts
    print(f"\nDIRECTIONAL INFO TEST (n={len(R)}, raw 16:05->16:40 pts, no stop/target/filter)")
    print(f"  mean faded return  {faded.mean():+.4f} pts  t={faded.mean()/(faded.std(ddof=1)/np.sqrt(len(faded))):+.2f}")
    print(f"  mean followed      {-faded.mean():+.4f} pts   (exact mirror)")
    print(f"  corr(imb_mln, ret_pts) = {float(np.corrcoef(R.imb_mln, R.ret_pts)[0,1]):+.4f}")
    print(f"  window sigma {R.ret_pts.std():.2f} pts; cost hurdle 4x RT = {4*COMM_RT_PTS:.2f} pts")
    big = R[R.imb_mln.abs() >= 2000]
    if len(big) > 10:
        fb = -np.sign(big.imb_mln) * big.ret_pts
        print(f"  |imb| >= $2bn (n={len(big)}): mean faded {fb.mean():+.3f} pts  t={fb.mean()/(fb.std(ddof=1)/np.sqrt(len(fb))):+.2f}")

    # correlation with the MNQ recon leg's daily P&L (per contract), parsed directly
    # from the same export the book grid used (no engine import needed)
    mnq_csv = os.path.join(r"C:\Users\joshu\Downloads",
                           "ORB-MNQ-1_recon_v7_CME_MINI_MNQ1!_2026-08-31_70648.csv")
    acc = {}
    for r in csv.DictReader(open(mnq_csv, encoding="utf-8-sig")):
        if not r["Type"].startswith("Exit"):
            continue
        dd = pd.Timestamp(r["Date and time"].split(" ")[0])
        acc[dd] = acc.get(dd, 0.0) + float(r["Net PnL USD"]) / float(r["Size (qty)"])
    mnq = pd.Series(acc).sort_index()
    moc = t.set_index("day")["net_pts"] * PT_USD
    idx = pd.bdate_range(min(moc.index.min(), mnq.index.min()), max(moc.index.max(), mnq.index.max()))
    a = moc.reindex(idx, fill_value=0.0); b = mnq.reindex(idx, fill_value=0.0)
    both = (a != 0) & (b != 0)
    corr_active = float(np.corrcoef(a[both], b[both])[0, 1]) if both.sum() > 10 else None
    la, lb = (a < 0), (b < 0)
    print(f"\ncorr with MNQ recon (days both traded, n={int(both.sum())}): {corr_active:+.3f}"
          if corr_active is not None else "corr: n/a")
    print(f"joint-loss days {float((la & lb).mean()):.4f} vs independence {float(la.mean()*lb.mean()):.4f}")
    out = {k: v["shape"] for k, v in res.items()}
    out["halves"] = {"mid": str(mid.date()), "h1": shape(h1), "h2": shape(h2)}
    out["corr_mnq_active_days"] = corr_active
    json.dump(out, open("moc_fade_replay_results.json", "w"), indent=1, default=str)
    res[hl]["trades"].to_csv("moc_fade_trades_headline.csv", index=False)
    print("\nwrote moc_fade_replay_results.json, moc_fade_trades_headline.csv")


if __name__ == "__main__":
    main()
