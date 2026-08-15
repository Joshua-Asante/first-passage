#!/usr/bin/env python3
"""selection_tests.py — selection-effect and robustness measurements for backtest panels.

Subcommands (all take a TV export CSV; --r sets dollar value of 1R, default 3000):

  bootstrap <csv> [--gate 0.25]          CI on expectancy, P(<=0), P(>=gate)
  dropk <csv> [--k 1 3 5]                concentration stress (drop top-k winners)
  halves <csv>                            first/second half + thirds stationarity
  bestof <csv> --by day                   best-of-K subset under demeaned (zero-edge) null
  perm <csv1> <csv2> ... --labels A B C   label-permutation test across separate single-subset runs
  costs <csv> --commission-pct 0.003 --slippage-ticks 2 --ticksize 0.00001
                                          empirical cost-in-R + doubled-cost expectancy

Provenance: 2026-06-11 USDCAD session. Permutation kills the random-labeling null ONLY —
it cannot see path-overfit. Keep a which-nulls-remain-alive ledger in the session record.
"""
import argparse
import numpy as np
import pandas as pd

def load(csv):
    df = pd.read_csv(csv, encoding='utf-8-sig')
    df.columns = [c.strip() for c in df.columns]
    netcol = [c for c in df.columns if c.startswith('Net PnL') or c.startswith('Net P&L')][0]
    df['Date and time'] = pd.to_datetime(df['Date and time'])
    ex = df[df['Type'].str.startswith('Exit')].copy()
    en = df[df['Type'].str.startswith('Entry')].copy().set_index(
        [c for c in df.columns if c.startswith('Trade')][0])
    ex['pnl'] = ex[netcol]
    tcol = [c for c in df.columns if c.startswith('Trade')][0]
    ex['entry_dt'] = pd.to_datetime(en.loc[ex[tcol], 'Date and time'].values)
    return df, ex

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['bootstrap','dropk','halves','bestof','perm','costs'])
    ap.add_argument('csvs', nargs='+')
    ap.add_argument('--r', type=float, default=3000.0)
    ap.add_argument('--gate', type=float, default=0.25)
    ap.add_argument('--k', nargs='*', type=int, default=[1,3,5])
    ap.add_argument('--by', default='day')
    ap.add_argument('--labels', nargs='*')
    ap.add_argument('--commission-pct', type=float, default=0.003)   # percent, per side
    ap.add_argument('--slippage-ticks', type=float, default=2)
    ap.add_argument('--ticksize', type=float, default=0.00001)
    ap.add_argument('--tz', default='America/New_York')
    ap.add_argument('--B', type=int, default=20000)
    a = ap.parse_args()
    rng = np.random.default_rng(7)
    R = a.r

    if a.cmd == 'bootstrap':
        _, ex = load(a.csvs[0]); p = ex.pnl.values; n = len(p)
        boots = np.array([rng.choice(p, n, True).mean() for _ in range(a.B)]) / R
        print(f"n={n} exp={p.mean()/R:+.3f}R | 95% CI [{np.percentile(boots,2.5):+.3f}, {np.percentile(boots,97.5):+.3f}]R")
        print(f"P(exp<=0)={float((boots<=0).mean()):.3f} | P(exp>=+{a.gate}R)={float((boots>=a.gate).mean()):.3f}")
        print(f"per-trade sigma={p.std()/R:.2f}R | SE@n=25 {p.std()/R/5:.3f}R | SE@n=50 {p.std()/R/np.sqrt(50):.3f}R")

    elif a.cmd == 'dropk':
        _, ex = load(a.csvs[0]); s = ex.pnl.sort_values(ascending=False)
        print(f"full: exp={s.mean()/R:+.3f}R net=${s.sum():,.0f}")
        for k in a.k:
            sub = s.iloc[k:]
            print(f"drop top {k}: exp={sub.mean()/R:+.3f}R net=${sub.sum():,.0f}")

    elif a.cmd == 'halves':
        _, ex = load(a.csvs[0]); ex = ex.sort_values('Date and time').reset_index(drop=True)
        n = len(ex); h = n // 2
        print(f"half1 exp={ex.pnl[:h].mean()/R:+.3f}R | half2 exp={ex.pnl[h:].mean()/R:+.3f}R")
        t = n // 3
        print("thirds:", " | ".join(f"{ex.pnl[i*t:(i+1)*t if i<2 else n].mean()/R:+.3f}R" for i in range(3)))

    elif a.cmd == 'bestof':
        _, ex = load(a.csvs[0])
        if a.by == 'day':
            lab = ex.entry_dt.dt.tz_localize('UTC').dt.tz_convert(a.tz).dt.day_name().values
        else:
            raise SystemExit(f"--by {a.by} not implemented")
        cats = sorted(set(lab)); p = ex.pnl.values
        obs = max(p[lab == c].mean() for c in cats) / R
        null = p - p.mean()
        hits = 0
        for _ in range(a.B):
            perm = rng.permutation(lab)
            if max(null[perm == c].mean() for c in cats) / R >= obs: hits += 1
        print(f"categories={cats}")
        print(f"observed best-subset exp={obs:+.3f}R | P(best-of-{len(cats)} >= obs | zero-edge)={hits/a.B:.3f}")

    elif a.cmd == 'perm':
        groups = [load(c)[1].pnl.values for c in a.csvs]
        labels = a.labels or [f"G{i}" for i in range(len(groups))]
        pool = np.concatenate(groups); sizes = [len(g) for g in groups]
        means = [g.mean() for g in groups]
        best_i = int(np.argmax(means))
        obs_best = means[best_i] / R
        rest = np.concatenate([g for i, g in enumerate(groups) if i != best_i])
        obs_spread = (means[best_i] - rest.mean()) / R
        gb = gs = 0
        for _ in range(a.B):
            p = rng.permutation(pool); idx = 0; ms = []
            for s in sizes:
                ms.append(p[idx:idx+s].mean()); idx += s
            bi = int(np.argmax(ms))
            rb = np.delete(np.arange(len(sizes)), bi)
            r_pool = np.concatenate([p[sum(sizes[:i]):sum(sizes[:i+1])] for i in rb])
            if max(ms)/R >= obs_best: gb += 1
            if (max(ms) - r_pool.mean())/R >= obs_spread: gs += 1
        print(f"best subset: {labels[best_i]} exp={obs_best:+.3f}R")
        print(f"P(best >= obs | H0 no subset effect) = {gb/a.B:.3f}")
        print(f"P(best-minus-rest >= {obs_spread:+.3f}R | H0) = {gs/a.B:.3f}")

    elif a.cmd == 'costs':
        df, ex = load(a.csvs[0])
        tcol = [c for c in df.columns if c.startswith('Trade')][0]
        en = df[df['Type'].str.startswith('Entry')].set_index(tcol)
        pcol = [c for c in en.columns if c.startswith('Price')][0]
        qty = ex['Size (qty)'].values
        price = en.loc[ex[tcol], pcol].values
        comm = qty * price * (a.commission_pct/100) * 2
        slip = qty * a.slippage_ticks * a.ticksize / price * 2
        cost = comm + slip
        print(f"mean RT cost ${cost.mean():.0f} = {cost.mean()/R:.3f}R | p90 {np.percentile(cost,90)/R:.3f}R")
        print(f"doubled-cost expectancy: {(ex.pnl.values - cost).mean()/R:+.3f}R "
              f"(vs {ex.pnl.mean()/R:+.3f}R as-traded)")

if __name__ == '__main__':
    main()
