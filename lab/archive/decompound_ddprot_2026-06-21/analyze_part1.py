"""CC-handoff §2.1-§2.5 driver (2026-06-21) — decompound + dd_protection + MC.

Reuses the LOCKED production primitives with ZERO fork:
  * lab/analysis/decompound_remc_2026-06-07/decompound.py  (load_file,
    reconstruct_roe, rebank, run_mc, ACCOUNT, ALLOC, FIXED_1R)
  * core/portfolio_mc.py  (build_daily_panel, build_week_blocks, _run_seeds,
    _simulate_path)  — imported transitively by decompound.py
  * core/dd_protection.py (DD_TRIGGER, DD_SCALE)  — the live C2 constants

Inputs: the four FRESH 2026-06-21 Pepperstone full-history (2020-01 -> 2026-06)
single-file exports in ~/Downloads (vendor-licensed, NOT committed). Pyramid
adds appear as separate Trade #s tagged "Add" in the Signal (new TV header
convention: Trade number / Net PnL USD / Cumulative PnL USD).

This is RESEARCH (lab/). It does not touch core/, canonical panels, the locked
anchor, dd_protection constants, or any manifest. Read-only on all locked
artifacts.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

try:
    sys.stdout.reconfigure(encoding="utf-8")  # Windows console is cp1252 by default
except Exception:
    pass

# ── wire in the locked production decompounder (which itself wires in core/) ──
_DECOMP_DIR = Path(__file__).resolve().parents[1] / "decompound_remc_2026-06-07"
sys.path.insert(0, str(_DECOMP_DIR))

from decompound import (  # noqa: E402
    load_file,
    reconstruct_roe,
    rebank,
    run_mc,
    ACCOUNT,
    ALLOC,
    FIXED_1R,
)
from portfolio_mc import build_daily_panel  # noqa: E402
from dd_protection import DD_TRIGGER, DD_SCALE  # noqa: E402

OUT = Path(__file__).resolve().parent
DL = Path.home() / "Downloads"

# Fresh 2026-06-21 single-file exports. Filename token order: strat / version /
# broker / symbol — sanity-checked against EXPECTED below (the §2.1 HALT gate).
FILES = {
    "guardian":       DL / "Guardian_Gold_v5.5_PEPPERSTONE_XAUUSD_2026-06-21_6c8b2.csv",
    "striker":        DL / "Striker_DJ30_v4.5_PEPPERSTONE_US30_2026-06-21_99e26.csv",
    "aegis":          DL / "Aegis_USDJPY_v4.3_PEPPERSTONE_USDJPY_2026-06-21_7f750.csv",
    "striker_nas100": DL / "Striker_NAS100_v1_PEPPERSTONE_NAS100_2026-06-21_76dbf.csv",
}
EXPECTED_TOKENS = {
    "guardian":       ("Guardian", "v5.5", "PEPPERSTONE", "XAUUSD"),
    "striker":        ("Striker_DJ30", "v4.5", "PEPPERSTONE", "US30"),
    "aegis":          ("Aegis", "v4.3", "PEPPERSTONE", "USDJPY"),
    "striker_nas100": ("Striker_NAS100", "v1", "PEPPERSTONE", "NAS100"),
}
# Cross-check anchors from the independently-computed 2026-06-07 decompounded run
# (lab/analysis/decompound_remc_2026-06-07/RESULTS.md). Same strategies / broker /
# window -> reproduction within ~1-2% verifies the new vintage + the pipeline.
PRIOR_2026_06_07 = {
    # strat: (N, WR%, comp_net, static_net, compounding_x, flat_DD%)
    "guardian":       (309, 17.2, 553828, 269651, 2.05, 9.58),
    "striker":        (264, 70.8, 441428, 239729, 1.84, 9.03),
    "aegis":          (149, 58.4, 195032, 139565, 1.40, 6.12),
    "striker_nas100": (280, 54.6, 423063, 236899, 1.79, 5.18),
}
LOCKED_BASE_RISK = {  # firm_rules _BASE_RISK / portfolio_mc ALLOCATIONS (current lock)
    "guardian": 0.0034, "striker": 0.0070, "aegis": 0.0150, "striker_nas100": 0.0037,
}
LABEL = {"guardian": "Guardian", "striker": "Striker DJ30",
         "aegis": "Aegis", "striker_nas100": "Striker NAS100"}


def _fname_gate(strat: str, path: Path) -> str:
    name = path.name
    s_tok, ver, brk, sym = EXPECTED_TOKENS[strat]
    ok = all(tok in name for tok in (s_tok.split("_")[0], ver, brk, sym))
    return "OK" if ok else f"!! token mismatch ({name})"


# ── §2.1 reconcile (provenance + sanity) ───────────────────────────────────
def reconcile():
    print("=" * 92)
    print("§2.1 RECONCILE  (provenance + sanity; HALT only on symbol mislabel or")
    print("                 decompounded base-risk >10% off _BASE_RISK)")
    print("=" * 92)
    # Base-risk GATE estimator per leg (the §2.1 provenance check):
    #   Guardian/DJ30/NAS -> MEDIAN |loss| (= base-entry risk; for pyramid legs the
    #     many base entries dominate the median, so it ~ the Pine base risk%).
    #   Aegis -> full-stop MEAN (BE strategy: median is BE-clipped tiny, NOT 1R).
    # The pyramid full-stop MEAN (~2%, add-inclusive) is reported separately and is
    # EXPECTED/do-not-halt per the handoff §2.1.
    GATE_BASIS = {"guardian": "median", "striker": "median",
                  "striker_nas100": "median", "aegis": "fs-mean"}
    per = {}
    rows = []
    for s, path in FILES.items():
        t = reconstruct_roe(load_file(path)).sort_values("exit_dt").reset_index(drop=True)
        per[s] = t
        net = t["net_pnl"]
        n = len(t)
        wr = 100.0 * (net > 0).sum() / n
        gp = net[net > 0].sum()
        gl = net[net < 0].abs().sum()
        pf = gp / gl if gl > 0 else float("inf")
        comp_net = float(net.sum())
        eq = ACCOUNT + t["cum_after"]
        peak = eq.cummax()
        dd_pct = float(((peak - eq) / peak).max() * 100)
        static_net = float((t["roe"] * ACCOUNT).sum())
        comp_x = comp_net / static_net if static_net != 0 else float("nan")
        # estimators on the DECOMPOUNDED stream (roe*200K)
        dec_pnl = t["roe"] * ACCOUNT
        abs_losses = dec_pnl[dec_pnl < 0].abs()
        full_stops = abs_losses[abs_losses > 0.01 * ACCOUNT]
        median_r = float(abs_losses.median())                       # base-entry proxy
        fs_mean = float(full_stops.mean()) if len(full_stops) else float("nan")  # add-incl 1R
        gate_r = median_r if GATE_BASIS[s] == "median" else fs_mean
        gate_risk = gate_r / ACCOUNT
        dev = 100.0 * (gate_risk - LOCKED_BASE_RISK[s]) / LOCKED_BASE_RISK[s]
        halt = "HALT" if abs(dev) > 10.0 else "ok"
        rows.append((s, n, wr, pf, comp_net, static_net, comp_x, dd_pct,
                     median_r, fs_mean, len(full_stops), gate_risk * 100, dev, halt,
                     _fname_gate(s, path)))
    print(f"{'leg':<16}{'N':>4}{'WR%':>7}{'PF':>7}{'comp$':>11}{'static$':>11}"
          f"{'cmp×':>6}{'DD%':>7}{'medR$':>8}{'fsMean$':>9}{'baseR%':>8}{'devΔ%':>7} gate")
    for (s, n, wr, pf, cn, sn, cx, dd, mr, fsm, nfs, br, dev, halt, fg) in rows:
        print(f"{LABEL[s]:<16}{n:>4}{wr:>7.1f}{pf:>7.2f}{cn:>11,.0f}{sn:>11,.0f}"
              f"{cx:>6.2f}{dd:>7.2f}{mr:>8,.0f}{fsm:>9,.0f}{br:>8.3f}{dev:>+7.1f} {halt}/{fg}")
        print(f"{'':16}gate basis: {GATE_BASIS[s]} vs locked {LOCKED_BASE_RISK[s]*100:.2f}%  "
              f"| pyramid fs-mean (add-incl, EXPECTED) n={nfs}")
    print()
    # consistency vs 2026-06-07
    print("Consistency vs independently-computed 2026-06-07 run (RESULTS.md):")
    print(f"{'leg':<16}{'N now/prior':>16}{'static$ now/prior':>26}{'Δstatic%':>10}{'cmp× now/prior':>18}")
    for (s, n, wr, pf, cn, sn, cx, dd, *_rest) in rows:
        pN, pWR, pcn, psn, pcx, pdd = PRIOR_2026_06_07[s]
        dsn = 100.0 * (sn - psn) / psn
        print(f"{LABEL[s]:<16}{f'{n}/{pN}':>16}{f'{sn:,.0f}/{psn:,.0f}':>26}"
              f"{dsn:>+10.1f}{f'{cx:.2f}/{pcx:.2f}':>18}")
    print()
    return per


# ── §2.2 decompound + build daily panel ────────────────────────────────────
def decompound_panel(per):
    print("=" * 92)
    print("§2.2 DECOMPOUND to fixed $200K base (production decompounder, mode='static':")
    print("     dp_i = roe_i × 200K = (NetPnL_i / equity_before_i) × 200K).  Aegis verdict below.")
    print("=" * 92)
    # static streams [exit_date, pnl] per leg via the production rebank()
    trades_by_strat = {s: rebank(t, "static") for s, t in per.items()}
    # banded supplement (Joshua's withdrawal model) for the §2.3 real-life curve
    banded_by_strat = {s: rebank(t, "banded") for s, t in per.items()}

    # Aegis decompound coherence verdict
    a = per["aegis"]
    comp_net = float(a["net_pnl"].sum())
    static_net = float((a["roe"] * ACCOUNT).sum())
    print(f"Aegis: compounded Net ${comp_net:,.0f} -> static-decompounded Net ${static_net:,.0f} "
          f"(×{comp_net/static_net:.2f}).")
    if comp_net / static_net > 1.05:
        print("  VERDICT: Aegis COMPOUNDED (net shrinks under decompounding) -> decompounding is")
        print("  COHERENT. The ~flat early-vs-late full-stop $loss is the BE-manufactured")
        print("  small-loss distribution, not fixed-lot sizing. (Matches 2026-06-07 ×1.40.)")
    else:
        print("  VERDICT: Aegis net ~unchanged -> leg may be FIXED-LOT; decompounding suspect. REVIEW.")
    print()

    # production build_daily_panel: scale = (alloc*200K)/FIXED_1R = 1.0 exactly on
    # static streams, so panel values == raw static daily pnl (per-leg columns).
    panel, scale_info = build_daily_panel(trades_by_strat, ALLOC, fixed_1r_reference=FIXED_1R)
    bpanel, _ = build_daily_panel(banded_by_strat, ALLOC, fixed_1r_reference=FIXED_1R)
    print("Daily panel built: index", panel.index.min().date(), "->", panel.index.max().date(),
          f"({len(panel)} bdays).  build_daily_panel scale factors (expect 1.000):")
    for s, info in scale_info.items():
        print(f"  {LABEL[s]:<16} scale={info['scale']:.4f}  1R=${info['implied_1r']:,.0f}  n={info['n_trades']}")
    print()
    return trades_by_strat, banded_by_strat, panel, bpanel


# ── §2.3 combined equity curves: raw vs dd_protection ──────────────────────
def dd_protection_walk(combined_daily: np.ndarray):
    """Replicate _simulate_path's dd_protection semantics EXACTLY on a single
    historical path: scale day's combined pnl by DD_SCALE when
    round(dd_from_peak, 6) <= -DD_TRIGGER, else 1.0. Returns (equity_series,
    scale_flags)."""
    eq = peak = ACCOUNT
    eqs, flags = [], []
    for pnl in combined_daily:
        dd_from_peak = (eq - peak) / peak if peak > 0 else 0.0
        scale = DD_SCALE if round(dd_from_peak, 6) <= -DD_TRIGGER else 1.0
        eq = eq + pnl * scale
        if eq > peak:
            peak = eq
        eqs.append(eq)
        flags.append(scale)
    return np.array(eqs), np.array(flags)


def _max_dd(equity: np.ndarray):
    peak = np.maximum.accumulate(equity)
    dd = (peak - equity)
    i = int(np.argmax(dd))
    j = int(np.argmax(equity[:i + 1])) if i > 0 else 0
    return float(dd[i]), float(dd[i] / peak[i] * 100), j, i


def equity_curves(panel: pd.DataFrame, bpanel: pd.DataFrame):
    print("=" * 92)
    print("§2.3 COMBINED EQUITY CURVE — raw vs dd_protection (C2 1.5%/0.40×, live semantics)")
    print("=" * 92)
    legs = list(panel.columns)
    idx = panel.index
    combined = panel.sum(axis=1).to_numpy()

    raw_eq = ACCOUNT + np.cumsum(combined)
    prot_eq, flags = dd_protection_walk(combined)

    raw_dd, raw_ddp, rj, ri = _max_dd(raw_eq)
    prot_dd, prot_ddp, pj, pi = _max_dd(prot_eq)
    n_brake_days = int((flags < 1.0).sum())

    # per-leg DD contribution across the protected-curve max-DD window (peak, trough].
    # NB: exclude the peak day pj itself — the drawdown accrues on days AFTER the peak;
    # including pj captures the (often large, e.g. DJ30 pyramid) winner that CREATED
    # the peak and inverts the sign. Scaled by the same dd_protection flags the
    # live walk applied, so Σ(leg_contrib) == equity[pi]-equity[pj] == -maxDD$.
    win = panel.iloc[pj + 1:pi + 1]
    win_flags = flags[pj + 1:pi + 1]
    leg_contrib = (win.to_numpy() * win_flags[:, None]).sum(axis=0)
    _recon = float(leg_contrib.sum()); _expect = float(prot_eq[pi] - prot_eq[pj])
    assert abs(_recon - _expect) < 1.0, f"attribution mismatch {_recon} vs {_expect}"

    def _calmar(equity):
        total_ret = (equity[-1] - ACCOUNT) / ACCOUNT
        yrs = (idx[-1] - idx[0]).days / 365.25
        cagr_lin = total_ret / yrs  # simple annualized (non-compounded, static base)
        dd = _max_dd(equity)[1] / 100
        return total_ret, cagr_lin, (cagr_lin / dd if dd > 0 else float("nan")), (
            (equity[-1] - ACCOUNT) / (_max_dd(equity)[0]) if _max_dd(equity)[0] > 0 else float("nan"))

    for label, equity in (("RAW (static, no protection)", raw_eq),
                          ("dd_protection (C2)", prot_eq)):
        dd_d, dd_p, j, i = _max_dd(equity)
        tr, cagr, calmar, rf = _calmar(equity)
        print(f"{label:<30} final ${equity[-1]:,.0f}  net ${equity[-1]-ACCOUNT:,.0f}  "
              f"maxDD ${dd_d:,.0f} ({dd_p:.2f}%)  RF {rf:.2f}  Calmar {calmar:.2f}")
        print(f"{'':30} maxDD window {idx[j].date()} -> {idx[i].date()}")
    dd_reduction_pp = raw_ddp - prot_ddp
    dd_reduction_pct = 100.0 * (raw_dd - prot_dd) / raw_dd
    print(f"\nDD reduction (raw -> protected):  {raw_ddp:.2f}% -> {prot_ddp:.2f}%  "
          f"({dd_reduction_pp:+.2f}pp, {dd_reduction_pct:+.1f}% of $DD)")
    print(f"dd_protection brake-active days: {n_brake_days} / {len(idx)} "
          f"({100*n_brake_days/len(idx):.1f}%)")
    print(f"\nPer-leg $ contribution across the PROTECTED max-DD window "
          f"[{idx[pj].date()} -> {idx[pi].date()}]:")
    for leg, c in sorted(zip(legs, leg_contrib), key=lambda kv: kv[1]):
        print(f"  {LABEL[leg]:<16} ${c:,.0f}")
    print()

    # banded (withdrawal-model) supplement
    bcombined = bpanel.sum(axis=1).to_numpy()
    beq = ACCOUNT + np.cumsum(bcombined)  # NB: banded pnl already path-built in rebank
    bdd_d, bdd_p, bj, bi = _max_dd(beq)
    print(f"[supplement] BANDED withdrawal model (skim +5% to $200K, Joshua's real-life model):")
    print(f"             final ${beq[-1]:,.0f}  maxDD ${bdd_d:,.0f} ({bdd_p:.2f}%)  "
          f"resets to $200K each +5% — DD is the *funded-phase* picture, not pass/bust.")
    print()

    # persist series for the record + part 2
    df = pd.DataFrame({"date": idx, "combined_daily_pnl": combined,
                       "equity_raw": raw_eq, "equity_ddprot": prot_eq,
                       "ddprot_scale": flags}, )
    for leg in legs:
        df[f"pnl_{leg}"] = panel[leg].to_numpy()
    df.to_csv(OUT / "equity_series.csv", index=False)
    panel.to_pickle(OUT / "panel_static.pkl")

    # PNG
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 8), height_ratios=[3, 1], sharex=True)
        ax1.plot(idx, raw_eq, label=f"raw (maxDD {raw_ddp:.2f}%)", lw=1.1, color="#c44")
        ax1.plot(idx, prot_eq, label=f"dd_protection C2 (maxDD {prot_ddp:.2f}%)", lw=1.1, color="#246")
        ax1.axhline(ACCOUNT, color="#999", lw=0.7, ls="--")
        ax1.axhline(ACCOUNT * 1.05, color="#4a4", lw=0.7, ls=":", label="+5% pass")
        ax1.axhline(ACCOUNT * 0.95, color="#a44", lw=0.7, ls=":", label="-5% static bust")
        ax1.set_ylabel("equity $ (fixed $200K base, static decompound)")
        ax1.set_title("Decompounded 4-leg combined equity — raw vs dd_protection (2020-01 → 2026-06, Pepperstone)")
        ax1.legend(loc="upper left", fontsize=8)
        ax1.grid(alpha=0.25)
        # drawdown panel
        for equity, c, lab in ((raw_eq, "#c44", "raw"), (prot_eq, "#246", "protected")):
            peak = np.maximum.accumulate(equity)
            ax2.fill_between(idx, -(peak - equity) / peak * 100, 0, alpha=0.35, color=c, label=lab)
        ax2.set_ylabel("DD %")
        ax2.grid(alpha=0.25)
        ax2.legend(loc="lower left", fontsize=8)
        fig.tight_layout()
        fig.savefig(OUT / "equity_curves.png", dpi=110)
        print(f"Saved {OUT/'equity_curves.png'} and {OUT/'equity_series.csv'}")
    except Exception as e:  # pragma: no cover
        print(f"[plot skipped: {e}]")
    print()
    return raw_ddp, prot_ddp


# ── §2.4 portfolio MC at current lock (production run_mc on decompounded streams) ──
def portfolio_mc(trades_by_strat):
    print("=" * 92)
    print("§2.4 PORTFOLIO MC — production run_mc on decompounded-static streams, locked C2")
    print("=" * 92)
    res = run_mc(trades_by_strat, ALLOC, FIXED_1R, dd_trigger=DD_TRIGGER, dd_scale=DD_SCALE)
    print(f"Panel: {res['n_bdays']} bdays / {res['n_blocks']} week-blocks")
    print(f"Pass:            {res['pass_rate']:.2%}")
    print(f"Bust:            {res['bust_rate']:.2%}  "
          f"(daily {res['bust_daily_rate']:.2%} / static {res['bust_static_rate']:.2%})")
    print(f"Bust inactivity: {res['bust_inactivity_rate']:.2%}")
    print(f"p99 DD:          {res['p99_dd']:.2%}   p95 DD: {res['p95_dd']:.2%}")
    print(f"Median days:     {res['median_days_to_pass']}")
    tot = sum(res["bust_attribution"].values())
    print("Bust attribution:", {k: f"{100*v/tot:.1f}%" for k, v in
                                 sorted(res["bust_attribution"].items(), key=lambda kv: -kv[1])} if tot else "(none)")
    print()
    print("Compare to anchors:")
    print("  locked anchor (compounded 2022-26):        99.83% / 0.17% / 4.37% / 26d  [BOTH gates clear]")
    print("  2026-06-07 S_2020 (decompound static):     97.04% / 2.96% / 5.93% / 31d  [BOTH gates breach]")
    print(f"  THIS run (decompound static 2020-26):      {res['pass_rate']:.2%} / "
          f"{res['bust_rate']:.2%} / {res['p99_dd']:.2%} / {res['median_days_to_pass']}d")
    print("  -> drift from locked anchor is EXPECTED & already characterized by the")
    print("     2026-06-07 HOLD ADR (decompound + 2020-21 window). Drift driver order:")
    print("     panel-length (5.5yr vs 52mo) > decompounding > methodology. NOT re-baselined.")
    print()
    json.dump({
        "n_bdays": res["n_bdays"], "n_blocks": res["n_blocks"],
        "pass": res["pass_rate"], "bust": res["bust_rate"],
        "bust_daily": res["bust_daily_rate"], "bust_static": res["bust_static_rate"],
        "bust_inactivity": res["bust_inactivity_rate"],
        "p99_dd": res["p99_dd"], "p95_dd": res["p95_dd"],
        "median": res["median_days_to_pass"],
        "bust_attribution": res["bust_attribution"],
    }, open(OUT / "mc_4leg_baseline.json", "w"), indent=2)
    return res


# ── §2.5 covariance + ENB + worst windows ──────────────────────────────────
def covariance_enb(panel: pd.DataFrame, raw_or_prot="prot"):
    print("=" * 92)
    print("§2.5 COVARIANCE STRUCTURE + ENB + worst drawdown windows")
    print("=" * 92)
    legs = list(panel.columns)
    X = panel.to_numpy()

    # all-day correlation
    corr_all = np.corrcoef(X.T)
    # active-day-only: for each pair, days where BOTH legs nonzero
    n = len(legs)
    corr_act = np.full((n, n), np.nan)
    for i in range(n):
        for j in range(n):
            mask = (X[:, i] != 0) & (X[:, j] != 0)
            if mask.sum() > 2:
                corr_act[i, j] = np.corrcoef(X[mask, i], X[mask, j])[0, 1]
    print("Pairwise correlation (all-day / active-day-only):")
    print(f"{'':16}" + "".join(f"{LABEL[l][:9]:>11}" for l in legs))
    for i, li in enumerate(legs):
        cells = []
        for j in range(n):
            a = corr_all[i, j]
            b = corr_act[i, j]
            cells.append(f"{a:+.2f}/{b:+.2f}" if not np.isnan(b) else f"{a:+.2f}/  - ")
        print(f"{LABEL[li]:<16}" + "".join(f"{c:>11}" for c in cells))
    print()

    # ENB = (Σw)² / (wᵀ R w) using the CORRELATION matrix R (bounded in [1, n];
    # the dollar-covariance form is scale-unbounded and meaningless here).
    R = np.corrcoef(X.T)
    w_locked = np.array([ALLOC[l] for l in legs])
    w_eq = np.ones(n)
    def enb(w):
        w = np.asarray(w, float)
        return float((w.sum() ** 2) / (w @ R @ w))
    # Cross-check: diversification ratio on the as-traded (risk-normalized) panel —
    # ENB_dr = (Σ σ_i)² / Var(Σ x_i), the effective independent-bet count of the
    # ACTUAL dollar portfolio (captures both correlation AND per-leg σ dispersion).
    sig = X.std(axis=0, ddof=1)
    var_port = float(np.var(X.sum(axis=1), ddof=1))
    enb_dr = float((sig.sum() ** 2) / var_port)
    print(f"Effective number of bets (ENB = (Σw)²/wᵀRw, R=correlation), max = {n} (uncorrelated):")
    print(f"  equal weights:           ENB = {enb(w_eq):.3f}   (leg-level diversification; legs ~uncorrelated -> near {n})")
    print(f"  locked risk weights:     ENB = {enb(w_locked):.3f}   (Aegis 1.50% concentration pulls effective bets below {n})")
    print(f"  as-traded div-ratio:     ENB_dr = {enb_dr:.3f}   ((Σσ)²/Var(Σx); per-leg σ dispersion + correlation)")
    print(f"  -> legs are near-uncorrelated; the smoothing ceiling is set by weight/σ concentration,")
    print(f"     so a 5th UNCORRELATED leg raises the ceiling (adds an independent bet).")
    print()

    # K=10 worst protected-curve drawdown windows
    combined = panel.sum(axis=1).to_numpy()
    eq, flags = dd_protection_walk(combined)
    peak = np.maximum.accumulate(eq)
    underwater = eq < peak * (1 - 1e-9)
    # segment contiguous underwater stretches, rank by depth
    idx = panel.index
    windows = []
    in_dd = False
    start = 0
    run_peak = peak[0]
    for k in range(len(eq)):
        if underwater[k] and not in_dd:
            in_dd = True; start = k; run_peak = peak[k]
        if in_dd and (not underwater[k] or k == len(eq) - 1):
            end = k
            seg = eq[start:end + 1]
            depth = (run_peak - seg.min()) / run_peak * 100
            trough = start + int(np.argmin(seg))
            windows.append((depth, start, trough, end))
            in_dd = False
    windows.sort(reverse=True)
    print("K=10 worst PROTECTED-curve drawdown windows (depth%, peak→trough→recover, red legs):")
    print(f"{'#':>2}{'depth%':>8}{'peak date':>13}{'trough':>13}{'recover':>13}   red legs (Σ$ over window)")
    worst_windows = []
    for rank, (depth, s, tr, e) in enumerate(windows[:10], 1):
        win = panel.iloc[s:tr + 1]
        leg_sum = win.sum(axis=0)
        reds = [(LABEL[l], leg_sum[l]) for l in legs if leg_sum[l] < 0]
        reds.sort(key=lambda kv: kv[1])
        red_str = ", ".join(f"{nm} ${v:,.0f}" for nm, v in reds) or "(none)"
        print(f"{rank:>2}{depth:>8.2f}{idx[s].date().isoformat():>13}{idx[tr].date().isoformat():>13}"
              f"{idx[e].date().isoformat():>13}   {red_str}")
        worst_windows.append({"rank": rank, "depth_pct": depth,
                              "peak": idx[s].date().isoformat(),
                              "trough": idx[tr].date().isoformat(),
                              "recover": idx[e].date().isoformat(),
                              "red_legs": {nm: float(v) for nm, v in reds}})
    print()
    json.dump({
        "corr_all": {LABEL[legs[i]]: {LABEL[legs[j]]: float(corr_all[i, j]) for j in range(n)} for i in range(n)},
        "enb_locked": enb(w_locked), "enb_equal": enb(w_eq), "enb_dr": enb_dr, "enb_max": n,
        "worst_windows": worst_windows,
    }, open(OUT / "covariance_enb.json", "w"), indent=2)
    return worst_windows


def main():
    per = reconcile()
    trades_by_strat, banded_by_strat, panel, bpanel = decompound_panel(per)
    equity_curves(panel, bpanel)
    portfolio_mc(trades_by_strat)
    covariance_enb(panel)
    print("PART 1 COMPLETE. Panel persisted to panel_static.pkl for the §2.6 sweep (part 2).")


if __name__ == "__main__":
    main()
