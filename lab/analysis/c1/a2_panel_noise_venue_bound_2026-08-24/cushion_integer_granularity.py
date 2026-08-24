"""Is cushion-proportional sizing implementable at 1-micro granularity?

pol_cushion (lab/analysis/c1/orbmnq1_cushion_sizing_probe_2026-08-20) returns
    m = 0.75 * min(1, max(cushion,0)/DD)
and the day loop applies `d = pnl_at_base_k * m`. With base_k in {1,2} the policy's
exposure is m*base_k in [0, 1.5] CONTRACTS -- i.e. below one micro contract for the
whole of base_k=1, and below one for most of base_k=2.

This script rebuilds an ORB-MNQ-1-shaped panel calibrated to the campaign's own
published Control-G moments, validates it against the published flat-k=1 bust rate,
then asks whether ANY integer-contract cushion ladder (>= 1 micro floor) clears the
frozen gate (bust <= 3% AND pass >= 50%).
"""
import numpy as np

# Published Control G (evalseq_orb_intraday_results.json, exact):
N_TRADES, N_BDAYS = 1846, 1878
MEAN_R, WR, STOPPED, NET_1LOT = 0.0626136067573826, 0.4637053087757313, 0.38028169014084506, 17779.78
R_DOLLARS = NET_1LOT / N_TRADES / MEAN_R          # $ per 1R at one micro contract
SIGMA_R = 1.19                                    # from t=+2.41 at n=1846 (RESULTS.md)
DD, START, TARGET = 3000.0, 100_000.0, 106_000.0
MIN_TD, CONS = 3, 0.40


def draw_panel(rng, n_days=N_BDAYS):
    """Per-trade R stream matching the published (mean, sd, win rate, stopped fraction)."""
    p_stop = STOPPED
    p_win = WR
    p_softloss = 1 - p_win - p_stop
    u = rng.random(n_days)
    R = np.empty(n_days)
    win = u < p_win
    stop = (u >= p_win) & (u < p_win + p_stop)
    soft = ~win & ~stop
    # solve win distribution for the target mean/sd  (see derivation in the report)
    soft_r = -rng.uniform(0.0, 0.6, soft.sum())
    e_soft = -0.3
    mw = (MEAN_R + p_stop * 1.0 - p_softloss * e_soft) / p_win
    e_r2 = SIGMA_R**2 + MEAN_R**2
    e_w2 = (e_r2 - p_stop * 1.0 - p_softloss * 0.12) / p_win
    sw = np.sqrt(max(e_w2 - mw*mw, 1e-6))
    a = max(mw - sw, 0.0)
    R[win] = a + rng.exponential(sw, win.sum())
    R[stop] = -1.0
    R[soft] = soft_r
    pnl = R * R_DOLLARS
    # intraday excursion, in $ (<=0). Stopped trades reach their stop; others give back.
    mae = np.where(R > 0, -rng.uniform(0.20, 0.80, n_days) * R_DOLLARS,
                   np.minimum(pnl, 0.0))
    mae = np.minimum(mae, 0.0)
    # ~1.7% of business days have no trade (1846 of 1878)
    idle = rng.random(n_days) < (1 - N_TRADES / N_BDAYS)
    pnl[idle] = 0.0; mae[idle] = 0.0
    return pnl, mae


def blocks(pnl, mae):
    n = (len(pnl) // 5) * 5
    return pnl[:n].reshape(-1, 5), mae[:n].reshape(-1, 5)


def run(bp, bl, sizer, *, seeds=(42, 123, 2026), n_paths=3000, horizon=1500):
    bust_t = pass_t = tot = 0
    for sd in seeds:
        rng = np.random.default_rng(sd)
        nb = len(bp); nw = horizon // 5
        idx = rng.integers(0, nb, size=(n_paths, nw))
        P = bp[idx].reshape(n_paths, -1)
        L = bl[idx].reshape(n_paths, -1)
        bal = np.full(n_paths, START); peak = bal.copy()
        tdays = np.zeros(n_paths); maxpos = np.zeros(n_paths)
        alive = np.ones(n_paths, bool); bust = np.zeros(n_paths, bool); passed = np.zeros(n_paths, bool)
        for t in range(P.shape[1]):
            bal_open = bal.copy()
            m = sizer(bal, peak)
            d = P[:, t] * m; dlow = L[:, t] * m
            bal[alive] += d[alive]
            traded = alive & (np.abs(P[:, t]) > 1e-9) & (m > 0)
            tdays[traded] += 1
            maxpos = np.where(traded, np.maximum(maxpos, d), maxpos)
            floor = peak - DD
            nbust = alive & ((bal_open + np.minimum(d, dlow)) <= floor)
            bust |= nbust; alive &= ~nbust
            ok = alive & (bal >= TARGET) & (tdays >= MIN_TD) & (maxpos <= CONS * (bal - START))
            passed |= ok; alive &= ~ok
            peak = np.where(alive, np.maximum(peak, bal), peak)
        bust_t += bust.sum(); pass_t += passed.sum(); tot += n_paths
    return 100*bust_t/tot, 100*pass_t/tot


if __name__ == '__main__':
    rng = np.random.default_rng(20260824)
    pnl, mae = draw_panel(rng)
    bp, bl = blocks(pnl, mae)
    print(f"panel: {len(pnl)} bdays, 1R = ${R_DOLLARS:.2f}/micro, realized meanR "
          f"{(pnl/R_DOLLARS).mean():+.4f}, WR {(pnl>0).mean():.3f}, net@1lot ${pnl.sum():,.0f}\n")

    print("VALIDATION -- flat sizing must reproduce the published intraday-honest figures")
    print(f"{'policy':44s} {'bust%':>8} {'pass%':>8}   published")
    for k, pub in ((1, '67.67 / 32.33'), (2, '77.01 / 22.99')):
        b, p = run(bp, bl, lambda bal, peak, k=k: np.full(bal.shape, float(k)))
        print(f"{'flat k=' + str(k):44s} {b:>8.2f} {p:>8.2f}   {pub}")

    print("\nTHE COMMITTED POLICY -- fractional contracts (as modelled)")
    for k in (1, 2):
        siz = lambda bal, peak, k=k: k * 0.75 * np.minimum(1.0, np.maximum(bal - (peak - DD), 0) / DD)
        b, p = run(bp, bl, siz)
        print(f"{'pol_cushion base_k=' + str(k) + '  (max ' + str(0.75*k) + ' contracts)':44s} {b:>8.2f} {p:>8.2f}")

    print("\nTHE SAME POLICY, ROUNDED TO WHOLE MICRO CONTRACTS (>=1 floor)")
    for k in (1, 2):
        siz = lambda bal, peak, k=k: np.maximum(1.0, np.round(
            k * 0.75 * np.minimum(1.0, np.maximum(bal - (peak - DD), 0) / DD)))
        b, p = run(bp, bl, siz)
        print(f"{'pol_cushion base_k=' + str(k) + ' -> integer':44s} {b:>8.2f} {p:>8.2f}")

    print("\nRE-PARAMETERISED integer cushion ladder: contracts = max(1, floor(f * cushion / 1R))")
    print(f"{'f':>6} {'max contracts':>14} {'bust%':>8} {'pass%':>8}   gate(bust<=3 & pass>=50)")
    for f in (0.02, 0.05, 0.10, 0.15, 0.20, 0.30, 0.50):
        siz = lambda bal, peak, f=f: np.maximum(1.0, np.floor(
            f * np.maximum(bal - (peak - DD), 0) / R_DOLLARS))
        b, p = run(bp, bl, siz)
        mx = int(np.floor(f * DD / R_DOLLARS))
        print(f"{f:>6.2f} {max(mx,1):>14d} {b:>8.2f} {p:>8.2f}   {'PASS' if (b<=3 and p>=50) else 'fail'}")

    print("\nSame ladder but STAND DOWN below a cushion threshold instead of a 1-contract floor")
    print(f"{'f':>6} {'stand-down $':>13} {'bust%':>8} {'pass%':>8}   gate")
    for f, thr_c in ((0.10, 400), (0.10, 800), (0.20, 400), (0.20, 800), (0.30, 800)):
        def siz(bal, peak, f=f, tc=thr_c):
            c = np.maximum(bal - (peak - DD), 0)
            n = np.floor(f * c / R_DOLLARS)
            return np.where(c < tc, 0.0, np.maximum(1.0, n))
        b, p = run(bp, bl, siz)
        print(f"{f:>6.2f} {thr_c:>13d} {b:>8.2f} {p:>8.2f}   {'PASS' if (b<=3 and p>=50) else 'fail'}")
