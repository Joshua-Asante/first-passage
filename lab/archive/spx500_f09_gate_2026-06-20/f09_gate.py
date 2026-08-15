"""Q-SPX-F09 gate falsification harness (PREREG-F09.md, 2026-06-20).

Tests whether a STRICTLY-CAUSAL trailing regime-state estimator predictively separates
forward daily momentum payoff (the lead-time question that gates the entire US500
directional-family axis).

LEAKAGE DISCIPLINE (the load-bearing invariant — M-15 / offset-faithfulness):
  - r_t        = ln(close_t / close_{t-1})                 daily log return
  - m_t        = sign(r_{t-1}) * r_t                        1-day TS-momentum payoff (position known at open of t)
  - S_t        = sign( AC1( r over [t-L .. t-1] ) )         regime state — uses returns THROUGH t-1 ONLY
  S_t is the rolling-AC1 ending at index i, SHIFTED +1 so the value at t excludes r_t.
  Any path where S_t sees r_t makes F09 spuriously PASS -> that is the defect the audit hunts.

Primary (PREREG §4): L=63 (calendar-day-last-close daily mark). d = E[m|S=mom] - E[m|S=rev].
Echoes (descriptive ONLY, cannot change verdict): L in {42,126}; ER-sign state; RTH-close daily mark.
Permutation: cyclic rotation (preserves each series' autocorrelation, breaks S<->m alignment).
"""
import argparse
import re
from pathlib import Path
import numpy as np
import pandas as pd

SIG = re.compile(r"^(?P<epoch>\d+)\|(?P<o>[-\d.]+)\|(?P<h>[-\d.]+)\|(?P<l>[-\d.]+)\|(?P<c>[-\d.]+)\|(?P<v>\d+)$")
DL = Path(r"C:\Users\joshu\Downloads")
FILES_5M = ["BAR_EXPORT_v0.1_PEPPERSTONE_US500_2026-06-20_ebb84.csv",
            "BAR_EXPORT_v0.1_PEPPERSTONE_US500_2026-06-20_93919.csv"]
L_PRIMARY = 63
PERM_N = 10_000
PERM_SEED = 42
DROP_K = (5, 10)


def load_5m():
    frames = []
    for fn in FILES_5M:
        raw = pd.read_csv(DL / fn, encoding="utf-8-sig")
        raw.columns = [str(c).strip() for c in raw.columns]
        ent = raw[raw["Type"].astype(str).str.startswith("Entry")]
        recs, xfail = [], 0
        for _, row in ent.iterrows():
            m = SIG.match(str(row["Signal"]).strip())
            if not m:
                continue
            c = float(m["c"])
            if abs(float(row["Price USD"]) - c) > max(1e-5, c * 1e-4):
                xfail += 1
            recs.append((int(m["epoch"]), c))
        assert xfail == 0, f"integrity cross-check fails in {fn}: {xfail}"
        frames.append(pd.DataFrame(recs, columns=["epoch", "c"]))
    df = pd.concat(frames, ignore_index=True)
    df["time"] = pd.to_datetime(df["epoch"], unit="ms", utc=True)
    # Overlap integrity: the two pages overlap at the 2023-06 seam; assert overlapping
    # bar-open epochs carry identical close before deduping (a re-exported page with revised
    # overlap bars must not be silently masked). keep='last' = prefer the later re-export.
    dup = df[df.duplicated("time", keep=False)]
    for t, g in dup.groupby("time"):
        assert g["c"].nunique() == 1, f"overlap close mismatch at {t}: {sorted(g['c'].unique())}"
    df = df.sort_values("time").drop_duplicates("time", keep="last").reset_index(drop=True)
    df["et"] = df["time"].dt.tz_convert("America/New_York")
    return df


def daily_marks(df, mark="calendar"):
    """Daily close series.

    mark='calendar' (PREREG primary) = last 5m close per ET calendar date. AUDIT MAJOR (2026-06-20):
      on the ~23h CFD this is the ~23:55 ET evening-session bar (NOT a settlement/cash close); the
      18:00-23:55 ET evening session (economically the next futures day) bins to the current ET date,
      and Sundays are ~6h phantom marks abutting the weekend gap. This is strictly CAUSAL (each date's
      mark uses only same-date bars) and is identical in the observed stat AND the permutation null, so
      it does not corrupt a FALSIFIED-direction verdict. STANDING TRIPWIRE: if a future page flips the
      calendar mark to RESOLVED while the RTH-close echo stays FALSIFIED, this binning is the prime
      suspect and must be re-audited before the verdict is trusted.
    mark='rth' (echo / corroborator) = last bar with ET hour < 16 per date (~15:55 ET cash-session close)."""
    d = df.copy()
    d["date"] = d["et"].dt.date
    if mark == "rth":
        d = d[d["et"].dt.hour < 16]
    daily = d.groupby("date")["c"].last().reset_index()
    daily["date"] = pd.to_datetime(daily["date"])
    daily = daily.sort_values("date").reset_index(drop=True)
    daily["r"] = np.log(daily["c"]).diff()
    return daily


def rolling_ac1_causal(r, L):
    """S_t = sign(AC1 over [t-L .. t-1]); strictly causal (excludes r_t).
    rolling-AC1 ending at i (uses r_i), then .shift(1) so value at t ends at t-1."""
    def ac1(w):
        w = np.asarray(w, float)
        if np.std(w[:-1]) == 0 or np.std(w[1:]) == 0:
            return np.nan
        return np.corrcoef(w[1:], w[:-1])[0, 1]
    ac = r.rolling(L).apply(ac1, raw=True)
    return ac.shift(1)  # <-- THE causal lag: state at t uses returns through t-1 only


def efficiency_ratio_causal(r, close, L):
    """Kaufman ER sign as an alt state (echo). ER = |net move| / sum|moves| over [t-L..t-1].
    High ER -> trending(+momentum); low ER is ambiguous in sign, so ER-sign here = sign of the
    net directional move's persistence: we use sign(rolling-AC1 of |r|>median) is NOT it; instead
    use the standard regime read: ER above its own trailing median => momentum(+1) else reversion(-1)."""
    er = (close.diff(L).abs()) / (close.diff().abs().rolling(L).sum())
    er = er.shift(1)
    med = er.rolling(L, min_periods=L).median().shift(1)
    state = np.where(er > med, 1.0, -1.0)
    state = pd.Series(state, index=er.index)
    state[er.isna() | med.isna()] = np.nan
    return state


def conditional_delta(m, S):
    """d = E[m|S>0] - E[m|S<0]; returns (delta, e_mom, e_rev, n_mom, n_rev)."""
    mom = m[S > 0]
    rev = m[S < 0]
    e_mom, e_rev = mom.mean(), rev.mean()
    return e_mom - e_rev, e_mom, e_rev, len(mom), len(rev)


def cyclic_perm_p(m_arr, S_arr, delta_obs, n=PERM_N, seed=PERM_SEED):
    """One-sided p via cyclic rotation of m vs fixed S (preserves both autocorrelations)."""
    rng = np.random.default_rng(seed)
    N = len(m_arr)
    pos = S_arr > 0
    neg = S_arr < 0
    npos, nneg = pos.sum(), neg.sum()
    ge = 0
    offs = rng.integers(1, N, size=n)
    for k in offs:
        mr = np.roll(m_arr, k)
        d = mr[pos].sum() / npos - mr[neg].sum() / nneg
        if d >= delta_obs:
            ge += 1
    return (ge + 1) / (n + 1)


def score(daily, L, label, do_perm=True):
    d = daily.dropna(subset=["r"]).reset_index(drop=True)
    r = d["r"]
    m = np.sign(r.shift(1)) * r                       # m_t = sign(r_{t-1}) * r_t
    S = rolling_ac1_causal(r, L)                       # strictly-causal state
    aligned = pd.DataFrame({"date": d["date"], "m": m, "S": S}).dropna()
    aligned = aligned[aligned["S"] != 0].reset_index(drop=True)
    m_a, S_a = aligned["m"].to_numpy(), aligned["S"].to_numpy()

    delta, e_mom, e_rev, n_mom, n_rev = conditional_delta(aligned["m"], aligned["S"])
    assert n_mom > 0 and n_rev > 0, f"degenerate state ({label}): n_mom={n_mom} n_rev={n_rev}"
    out = {"label": label, "L": L, "N": len(aligned), "delta": delta,
           "e_mom": e_mom, "e_rev": e_rev, "n_mom": n_mom, "n_rev": n_rev}

    # payoffs (interpretability)
    G = np.where(S_a > 0, 1.0, -1.0)
    out["pay_mom"] = m_a.mean()
    out["pay_rev"] = (-m_a).mean()
    out["pay_gate"] = (G * m_a).mean()

    if do_perm:
        out["perm_p"] = cyclic_perm_p(m_a, S_a, delta)
        # halves
        h = len(aligned) // 2
        out["delta_h1"] = conditional_delta(aligned["m"][:h], aligned["S"][:h])[0]
        out["delta_h2"] = conditional_delta(aligned["m"][h:], aligned["S"][h:])[0]
        # drop-top-k by |m|
        for k in DROP_K:
            idx = np.argsort(-np.abs(m_a))[k:]
            mk, Sk = m_a[idx], S_a[idx]
            dk = mk[Sk > 0].mean() - mk[Sk < 0].mean()
            out[f"delta_drop{k}"] = dk
        # per-year d
        aligned["year"] = pd.to_datetime(aligned["date"]).dt.year
        out["by_year"] = {int(y): conditional_delta(g["m"], g["S"])[0]
                          for y, g in aligned.groupby("year")}
    return out


def verdict(p):
    """Apply PREREG §6 gate to the primary result dict."""
    # Degenerate guard: any nan in a gate input -> explicit FALSIFIED (never rely on nan-compare).
    for k in ("delta", "perm_p", "delta_h1", "delta_h2", "delta_drop5", "e_mom", "e_rev"):
        v = p.get(k)
        if v is None or (isinstance(v, float) and np.isnan(v)):
            return "FALSIFIED", [f"{k} is nan/degenerate"]
    fail = []
    if p["delta"] <= 0:
        fail.append("delta<=0")
    if p["perm_p"] >= 0.10:
        fail.append(f"perm_p>=0.10 ({p['perm_p']:.3f})")
    if p["delta_h1"] * p["delta_h2"] < 0:   # strict sign-FLIP per PREREG §6 (not sign(0)!=sign)
        fail.append("halves sign-flip")
    if fail:
        return "FALSIFIED", fail
    robust_ok = (p["e_mom"] > 0 and p["e_rev"] < 0 and
                 p["delta_drop5"] > 0 and p["delta_h1"] > 0 and p["delta_h2"] > 0)
    if robust_ok:
        return "RESOLVED", []
    soft = []
    if not (p["e_mom"] > 0 and p["e_rev"] < 0):
        soft.append("conditional means not both correctly signed")
    if p["delta_drop5"] <= 0:
        soft.append("drop-top-5 <= 0 (few-day-carried)")
    if not (p["delta_h1"] > 0 and p["delta_h2"] > 0):
        soft.append("a half is non-positive (not sign-flipped)")
    return "AMBIGUOUS-HOLD", soft


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reproduce", action="store_true")
    ap.parse_args()

    df = load_5m()
    daily = daily_marks(df, "calendar")
    print("=" * 92)
    print(f"Q-SPX-F09 gate  |  daily marks: {len(daily)}  span {daily['date'].min().date()} -> {daily['date'].max().date()}")
    print(f"PRIMARY: L={L_PRIMARY}, calendar-day-last-close, perm={PERM_N} cyclic rot seed={PERM_SEED}")
    print("=" * 92)

    prim = score(daily, L_PRIMARY, f"PRIMARY L={L_PRIMARY} calendar")
    v, notes = verdict(prim)

    def fmt(p):
        print(f"\n[{p['label']}]  N={p['N']}  n_mom={p['n_mom']} n_rev={p['n_rev']}")
        print(f"  d = E[m|mom]-E[m|rev] = {p['delta']*1e4:+.3f} bps   "
              f"(E[m|mom]={p['e_mom']*1e4:+.3f}  E[m|rev]={p['e_rev']*1e4:+.3f} bps)")
        print(f"  payoffs/day: pure-mom={p['pay_mom']*1e4:+.3f}  pure-rev={p['pay_rev']*1e4:+.3f}  GATED={p['pay_gate']*1e4:+.3f} bps")
        if "perm_p" in p:
            print(f"  cyclic-rotation perm p = {p['perm_p']:.4f}   (one-sided, P[d_perm >= d_obs])")
            print(f"  halves: d_h1={p['delta_h1']*1e4:+.3f}  d_h2={p['delta_h2']*1e4:+.3f} bps")
            print(f"  drop-top: d_drop5={p['delta_drop5']*1e4:+.3f}  d_drop10={p['delta_drop10']*1e4:+.3f} bps")
            print(f"  d by year (bps): " + "  ".join(f"{y}:{d*1e4:+.2f}" for y, d in p["by_year"].items()))

    fmt(prim)
    print(f"\n  >>> PRIMARY VERDICT: {v}" + (f"   [{'; '.join(notes)}]" if notes else ""))

    print("\n" + "-" * 92)
    print("ROBUSTNESS ECHOES (descriptive only — cannot change the verdict per PREREG §5)")
    print("-" * 92)
    for L in (42, 126):
        fmt(score(daily, L, f"echo L={L} calendar"))
    # RTH-close daily mark echo
    daily_rth = daily_marks(df, "rth")
    fmt(score(daily_rth, L_PRIMARY, f"echo L={L_PRIMARY} RTH-close"))
    # efficiency-ratio state echo (primary L, calendar)
    d2 = daily.dropna(subset=["r"]).reset_index(drop=True)
    rr = d2["r"]
    mm = np.sign(rr.shift(1)) * rr
    SS = efficiency_ratio_causal(rr, d2["c"], L_PRIMARY)
    al = pd.DataFrame({"m": mm, "S": SS}).dropna()
    al = al[al["S"] != 0]
    de, em, er_, nm, nr = conditional_delta(al["m"], al["S"])
    print(f"\n[echo ER-sign state L={L_PRIMARY} calendar]  N={len(al)}  n_mom={nm} n_rev={nr}")
    print(f"  d = {de*1e4:+.3f} bps   (E[m|mom]={em*1e4:+.3f}  E[m|rev]={er_*1e4:+.3f} bps)")

    print("\n" + "=" * 92)
    print(f"FINAL PREREG-F09 VERDICT (primary, L=63, calendar): {v}")
    print("=" * 92)


if __name__ == "__main__":
    main()
