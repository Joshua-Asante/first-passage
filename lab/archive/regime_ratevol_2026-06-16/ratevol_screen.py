"""Q-REGIME-RATEVOL-1 Phase-1 screen — does exogenous rate-vol add regime coverage BEYOND gold?

Pre-registration: docs/briefs/pre-registration/Q-REGIME-RATEVOL-1-verdict-preregistration.md
(committed c30b287, BEFORE this script ran). Parent brief: docs/briefs/Q-REGIME-RATEVOL-1.md.

The test (the only thing the n=2 realized history can resolve): rate-vol's MARGINAL separation of
the regime is expected to be high and uninformative (any slow macro variable separates 2 blocks). The
PRIMARY gate is the CONDITIONAL AUC on the gold-DEPLOY subset — does rate-vol carry regime-hardness
info where the frozen gold gate already says "clear"? With 2022-shock-exclusion + leave-one-year-out
guards against the tautology. RESOLVED earns only a 2nd shadow signal, never a live change.

Inputs (all gitignored / local; reproducible):
  - participation dependent variable: decompound forward-start sweep (lab/analysis/decompound_remc_2026-06-07
    inputs/, LOCKED allocs, C2) — reused verbatim from participation_check.py.
  - gold gate calls: XAUUSD daily (OANDA D candles, fetched + cached here) -> KER_126>=0.12 AND TSMOM_252>0.
  - rate-vol feature: FRED DGS10 (+DGS2) daily, causal 63-bd realized vol of dyield (annualized).

Run:  PYTHONPATH=core python lab/analysis/regime_ratevol_2026-06-16/ratevol_screen.py
"""
from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

# ── repo wiring (mirror participation_check.py) ──
_HERE = Path(__file__).resolve().parent
_REPO = next(p for p in _HERE.parents if (p / "CLAUDE.md").exists())
_DECOMP = _REPO / "lab" / "analysis" / "decompound_remc_2026-06-07"
for p in (str(_REPO / "core"), str(_DECOMP)):
    if p not in sys.path:
        sys.path.insert(0, p)

import decompound as D  # noqa: E402
from decompound import build_daily_panel  # noqa: E402
from portfolio_mc import _simulate_path, DD_TRIGGER, DD_SCALE  # noqa: E402

# ── pre-registered constants (frozen; see §8 pre-registration) ──
HOSTILE_CUTOFF_BD = 45          # days-to-pass > 45 (or bust) => hostile-ahead (oracle viability ceiling)
RATEVOL_WINDOW = 63             # primary: trailing 63-bd realized vol of dDGS10 (annualized)
RATEVOL_WINDOWS_REPORT = [21, 63, 126]
AUC_BAR = 0.70                  # separation bar (matches detector-screen)
AUC_ROBUST_FLOOR = 0.65         # must hold under 2022-exclusion + LOYO
EXCLUDE_YEAR = 2022             # rate-hiking shock exclusion (adversarial robustness, NOT cherry-pick)
GOLD_THR_KER126 = 0.12          # frozen gold gate
GOLD_REQUIRE_TSMOM252_POS = True

_CACHE = _HERE  # raw fetched series cached here (local-only)


# ─────────────────────────── data acquisition (cached) ───────────────────────────
def fred_series(series_id: str) -> pd.Series:
    cache = _CACHE / f"fred_{series_id}.csv"
    if not cache.exists():
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
        cache.write_bytes(urllib.request.urlopen(url, timeout=60).read())
    df = pd.read_csv(cache)
    df.columns = ["date", "val"]
    df["date"] = pd.to_datetime(df["date"])
    df["val"] = pd.to_numeric(df["val"], errors="coerce")  # "." -> NaN
    return pd.Series(df["val"].to_numpy(), index=df["date"]).dropna().sort_index()


def xauusd_daily_close() -> pd.Series:
    cache = _CACHE / "xauusd_daily.csv"
    if not cache.exists():
        from lib.oanda import fetch_candles  # noqa: E402
        rows = list(fetch_candles("XAU_USD", "2019-01-01T00:00:00Z", "2026-06-16T00:00:00Z",
                                  granularity="D", price="M"))
        pd.DataFrame(rows).to_csv(cache, index=False)
    df = pd.read_csv(cache, usecols=["time", "close"])
    t = pd.to_datetime(df["time"], format="ISO8601", utc=True).dt.tz_localize(None).dt.normalize()
    return pd.Series(df["close"].to_numpy(), index=t).sort_index().groupby(level=0).last()


# ─────────────────────────── features ───────────────────────────
def ratevol_feature(yields: pd.Series, window: int) -> pd.Series:
    """Causal trailing realized vol of daily yield CHANGES, annualized. Uses data through t only."""
    dchg = yields.diff()
    return dchg.rolling(window).std() * np.sqrt(252.0)


def ker(close: pd.Series, n: int) -> pd.Series:
    return (close.diff(n).abs() / close.diff().abs().rolling(n).sum()).replace([np.inf, -np.inf], np.nan)


def tsmom(close: pd.Series, n: int) -> pd.Series:
    return close / close.shift(n) - 1.0


def auc_hostile(score: np.ndarray, hostile: np.ndarray) -> tuple[float, int, int]:
    """P[score higher on a hostile-ahead start than a benign-ahead start]. (auc, n_hostile, n_benign)."""
    m = ~np.isnan(score)
    s, h = score[m], hostile[m]
    nh, nb = int((h == 1).sum()), int((h == 0).sum())
    if nh == 0 or nb == 0:
        return float("nan"), nh, nb
    order = np.argsort(s, kind="mergesort")
    ranks = np.empty(len(s)); ranks[order] = np.arange(1, len(s) + 1)
    # average ties
    ss = s[order]; i = 0
    while i < len(s):
        j = i
        while j + 1 < len(s) and ss[j + 1] == ss[i]:
            j += 1
        if j > i:
            ranks[order[i:j + 1]] = (i + 1 + j + 1) / 2.0
        i = j + 1
    auc = (ranks[h == 1].sum() - nh * (nh + 1) / 2.0) / (nh * nb)
    return float(auc), nh, nb


# ─────────────────────────── main ───────────────────────────
def main() -> dict:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    # 1) dependent variable: participation forward-start sweep (reuse participation_check recipe verbatim)
    LOCKED = dict(D.ALLOC)
    NATIVE_1R = {s: LOCKED[s] * D.ACCOUNT for s in LOCKED}
    STATIC = {s: D.rebank(D.stitch(s), "static") for s in LOCKED}
    panel, _ = build_daily_panel(STATIC, LOCKED, fixed_1r_reference=NATIVE_1R)
    vals, dates, n = panel.values, panel.index, len(panel)

    outcome, days = [], []
    for t in range(n):
        path = vals[t:]
        oc, day, _dd, _c = _simulate_path(path, DD_TRIGGER, DD_SCALE, len(path))
        outcome.append(oc); days.append(day)
    outcome = np.array(outcome, dtype=object); days = np.array(days)

    is_cens = outcome == "horizon_cap"
    noncens = ~is_cens
    is_bust = np.isin(outcome, ["bust_daily", "bust_static"])
    is_pass = outcome == "pass"
    # pre-registered label: hostile-ahead iff days>45 OR bust; else benign-ahead. (over non-censored)
    hostile_ahead = ((is_pass & (days > HOSTILE_CUTOFF_BD)) | is_bust).astype(int)

    # 2) gold gate calls per panel date (frozen rule on XAUUSD daily, asof t -> causal)
    gold = xauusd_daily_close()
    g_ker = ker(gold, 126); g_t252 = tsmom(gold, 252)
    gdf = pd.DataFrame({"ker126": g_ker, "tsmom252": g_t252}).sort_index()
    gdf = gdf.reindex(gdf.index.union(dates)).ffill().reindex(dates)
    deploy = ((gdf["ker126"] >= GOLD_THR_KER126) &
              ((gdf["tsmom252"] > 0) if GOLD_REQUIRE_TSMOM252_POS else True)).to_numpy()
    gold_valid = (~gdf["ker126"].isna() & ~gdf["tsmom252"].isna()).to_numpy()

    # 3) rate-vol feature(s) per panel date (FRED DGS10/DGS2, asof t -> causal)
    dgs10 = fred_series("DGS10"); dgs2 = fred_series("DGS2")
    feats = {}
    for w in RATEVOL_WINDOWS_REPORT:
        rv = ratevol_feature(dgs10, w)
        feats[f"dgs10_{w}"] = rv.reindex(rv.index.union(dates)).ffill().reindex(dates).to_numpy()
    rv2 = ratevol_feature(dgs2, RATEVOL_WINDOW)
    feats[f"dgs2_{RATEVOL_WINDOW}"] = rv2.reindex(rv2.index.union(dates)).ffill().reindex(dates).to_numpy()
    PRIMARY = f"dgs10_{RATEVOL_WINDOW}"
    primary = feats[PRIMARY]

    yr = np.array([d.year for d in dates])
    print("=" * 100)
    print("Q-REGIME-RATEVOL-1 PHASE-1 SCREEN — rate-vol incremental coverage vs the gold gate")
    print(f"panel {dates.min().date()}->{dates.max().date()} | {n} starts | noncens {int(noncens.sum())} | "
          f"hostile-ahead {int(hostile_ahead[noncens].sum())} | gold-DEPLOY {int((deploy & noncens & gold_valid).sum())}")
    print(f"primary feature: {PRIMARY} (trailing {RATEVOL_WINDOW}-bd realized vol of dDGS10, annualized)")
    print("=" * 100)

    # ── marginal AUC (reported, NOT a pass criterion — n=2 tautology) ──
    base = noncens & gold_valid
    print("\n[reported, non-gating] MARGINAL AUC (rate-vol vs hostile-ahead label, all valid starts):")
    marg = {}
    for name, f in feats.items():
        a, nh, nb = auc_hostile(f[base], hostile_ahead[base])
        marg[name] = a
        print(f"   {name:12s} AUC {a:.3f}  (n_hostile {nh} / n_benign {nb})")

    # ── PRIMARY: conditional AUC on the gold-DEPLOY subset ──
    dep = base & deploy
    cond_auc, cond_nh, cond_nb = auc_hostile(primary[dep], hostile_ahead[dep])
    print(f"\n[PRIMARY GATE] CONDITIONAL AUC on gold-DEPLOY subset ({PRIMARY}):")
    print(f"   AUC {cond_auc:.3f}  (gold-DEPLOY starts: hostile-ahead {cond_nh} / benign-ahead {cond_nb})")

    # ── robustness 1: 2022 excluded ──
    dep_ex22 = dep & (yr != EXCLUDE_YEAR)
    auc_ex22, nh22, nb22 = auc_hostile(primary[dep_ex22], hostile_ahead[dep_ex22])
    print(f"   2022-excluded: AUC {auc_ex22:.3f}  (hostile {nh22} / benign {nb22})")

    # ── robustness 2: leave-one-year-out (min across folds with both classes present) ──
    loyo = {}
    for y in sorted(set(yr[dep].tolist())):
        fold = dep & (yr != y)
        a, nh, nb = auc_hostile(primary[fold], hostile_ahead[fold])
        if not np.isnan(a):
            loyo[int(y)] = a
    loyo_min = min(loyo.values()) if loyo else float("nan")
    print(f"   LOYO AUC by dropped-year: " + ", ".join(f"{y}:{a:.3f}" for y, a in loyo.items()))
    print(f"   LOYO min: {loyo_min:.3f}")

    # ── blind-spot-covered set (parameter-free median split for the rate-vol flag) ──
    rv_med = float(np.nanmedian(primary[base]))
    rv_hostile_flag = primary > rv_med  # parameter-free; NOT outcome-fitted
    gold_deploy_hostile = dep & (hostile_ahead == 1)
    covered = gold_deploy_hostile & rv_hostile_flag
    n_gdh = int(gold_deploy_hostile.sum())
    n_cov = int(covered.sum())
    cov_frac = (n_cov / n_gdh) if n_gdh else 0.0
    # redundancy: are rate-vol hostile flags effectively a subset of gold WAIT?
    wait = base & ~deploy
    rv_flag_on_deploy = int((dep & rv_hostile_flag).sum())
    print(f"\n[blind-spot coverage]  rate-vol flag = ratevol > in-sample median ({rv_med:.3f}, parameter-free)")
    print(f"   gold-DEPLOY & hostile-ahead starts (the blind spot): {n_gdh}")
    print(f"   of those, rate-vol flags hostile: {n_cov}  ({cov_frac:.1%})")
    print(f"   rate-vol hostile-flags landing on gold-DEPLOY starts: {rv_flag_on_deploy} "
          f"(if ~0 => rate-vol flags are a subset of gold WAIT = no new coverage)")

    # ── verdict (§6, pre-registered) ──
    resolved = (cond_auc >= AUC_BAR and auc_ex22 >= AUC_ROBUST_FLOOR and loyo_min >= AUC_ROBUST_FLOOR
                and n_cov >= 10 and cov_frac >= 0.05)
    falsified = (0.40 <= cond_auc <= 0.60) or (auc_ex22 < 0.60) or (rv_flag_on_deploy == 0)
    if resolved:
        verdict = "RESOLVED"
    elif falsified:
        verdict = "FALSIFIED"
    else:
        verdict = "AMBIGUOUS-HOLD"
    # guard: RESOLVED dominates if both somehow trip; report conflict
    conflict = resolved and falsified

    print("\n" + "=" * 100)
    print(f"## VERDICT (pre-registered §6): {verdict}" + ("  [CONFLICT — manual review]" if conflict else ""))
    print(f"   conditional AUC {cond_auc:.3f} (bar {AUC_BAR}) | ex-2022 {auc_ex22:.3f} | LOYO-min {loyo_min:.3f} "
          f"(robust floor {AUC_ROBUST_FLOOR})")
    print(f"   blind-spot covered {n_cov}/{n_gdh} ({cov_frac:.1%}); thresholds >=10 and >=5%")
    print("=" * 100)

    out = {
        "investigation": "Q-REGIME-RATEVOL-1 Phase-1 screen",
        "prereg_commit": "c30b287",
        "primary_feature": PRIMARY,
        "panel": {"start": str(dates.min().date()), "end": str(dates.max().date()),
                  "n_starts": n, "n_noncensored": int(noncens.sum()),
                  "n_hostile_ahead": int(hostile_ahead[noncens].sum())},
        "marginal_auc": marg,
        "conditional_auc_gold_deploy": {"auc": cond_auc, "n_hostile": cond_nh, "n_benign": cond_nb},
        "robustness": {"ex_2022_auc": auc_ex22, "loyo": loyo, "loyo_min": loyo_min},
        "blind_spot": {"gold_deploy_hostile": n_gdh, "ratevol_covered": n_cov, "covered_frac": cov_frac,
                       "ratevol_median": rv_med, "ratevol_flags_on_deploy": rv_flag_on_deploy},
        "gates": {"AUC_BAR": AUC_BAR, "ROBUST_FLOOR": AUC_ROBUST_FLOOR,
                  "cutoff_bd": HOSTILE_CUTOFF_BD, "exclude_year": EXCLUDE_YEAR},
        "verdict": verdict, "conflict": conflict,
    }
    (_HERE / "ratevol_screen.json").write_text(json.dumps(out, indent=2, default=str))
    print(f"\nwrote {_HERE / 'ratevol_screen.json'}")
    return out


if __name__ == "__main__":
    main()
