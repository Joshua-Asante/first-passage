"""B2.2 placebo/orthogonality battery -- London-fix wake (6E, 6B), 11:10-13:00 ET.

Task B2.2 of Lane B2 (docs/superpowers/plans/2026-08-23-viable-strategy-phase-b-mechanism-supply.md).
Adapts the orthogonality-partial methodology of the gamma-family precedent
(lab/analysis/orb/orb_universe_2026-06-22/nas100_orb_gex_gate.py -- pruned from the worktree by the
2026-08-08 Great Prune but preserved in history, retrieved via
`git show pre-prune-2026-08-08:lab/analysis/orb/orb_universe_2026-06-22/nas100_orb_gex_gate.py`)
to this lane's own named controls (trailing-vol + prior-hour-return) in place of that precedent's
(|gap| + OR-range).

Mechanism under test (from the B2 notice, `docs/notes/notice/N-2026-08-24-b2-london-fix-wake-cost-
arithmetic.md` Sec4): benchmark-mandated fix flow (10:58-11:04 ET cluster) creates dealer inventory
whose normalization is faded 11:10-13:00 ET; sign read from the mechanically-defined fix-window
impulse.

Full methodology, results, and the frozen-kill-criterion application are written up in
RESULTS.md (this directory). This module is the runnable harness; see RESULTS.md Sec"Verification"
for the exact commands to reproduce every number quoted there.

Data: Databento GLBX.MDP3, continuous `.v.0` (volume-rolled -- NEVER `.c.0` for these FX futures,
per the repo's own roll-rule lesson: `.c.0` maps CME currency futures to a near-dead front monthly
serial and produces coverage artifacts), 2024-08-24 -> 2026-08-24 (2 years), 6E and 6B, scored
SEPARATELY per the B2.1 ruling (both symbols stay in scope; never pooled). Two schemas, both
Rule-1 dry-run confirmed $0.0000 before pulling (`databento-data` skill discipline):
  - ohlcv-1h (23,619 records, ~1.3MB) -- controls (trailing-vol, prior-hour-return) + the
    hourly-clock-family placebo battery.
  - ohlcv-1m (1,337,317 records, ~75MB) -- precise impulse-window resolution (hourly bars cannot
    resolve the literal 6-minute 10:58-11:04 ET cluster: it straddles the 10:00-11:00 and 11:00-
    12:00 hourly bars) and a precise 11:10 ET entry anchor.

To reproduce (from the repo root, research venv, DATABENTO_API_KEY set):
    PYTHONPATH=lab python -m databento_fetch.db_fetch pull \\
        --symbols 6E.v.0,6B.v.0 --stype continuous --schema ohlcv-1h \\
        --start 2024-08-24 --end 2026-08-24 --max-cost 0.01 \\
        --out lab/analysis/_inbox/b2_london_fix_wake_2026-08-24/data/6E_6B_ohlcv1h_2y.parquet
    PYTHONPATH=lab python -m databento_fetch.db_fetch pull \\
        --symbols 6E.v.0,6B.v.0 --stype continuous --schema ohlcv-1m \\
        --start 2024-08-24 --end 2026-08-24 --max-cost 0.01 \\
        --out lab/analysis/_inbox/b2_london_fix_wake_2026-08-24/data/6E_6B_ohlcv1m_2y.parquet
    python lab/analysis/_inbox/b2_london_fix_wake_2026-08-24/run_b22_placebo_battery.py
Both pulls hit the local Databento DBN cache (~/.databento_cache) after the first run -- no
re-billing on rerun. `data/` is gitignored (regenerable, $0-class, vendor-licensed bytes stay out
of git per the repo's public-clone posture, CLAUDE.md SecPublic-clone posture).

Clock-resolution design (stated per the task brief's explicit ask -- hourly bars cannot resolve
the literal 6-minute fix cluster):
  PRIMARY (precise) impulse  = open(11:04 1m bar) - open(10:58 1m bar)   [literal 10:58-11:04 ET]
  PRIMARY (precise) target   = open(13:00 1m bar) - open(11:10 1m bar)   [literal 11:10-13:00 ET]
  ROBUSTNESS (hourly-proxy) impulse = open(11:00h) - open(10:00h)  [== "prior_hour_return" control
    below -- this is the brief's own suggested coarse proxy, and it is IDENTICAL to the
    prior-hour-return control, so it cannot be used as a distinct regressor in the orthogonality
    regression (perfect collinearity) -- it is used only for the placebo-comparable statistic and
    as a cross-check of the precise version's sign/magnitude.]
  ROBUSTNESS (hourly-proxy) outcome = open(13:00h) - open(11:00h)  [11:00-13:00 ET, 2h]

Orthogonality regression (adapted from the precedent's `partial_out_t`):
    target_precise ~ 1 + trailing_vol + prior_hour_return + imp_sign
  imp_sign in {-1,+1} = sign of the PRECISE impulse. Fade hypothesis => imp_sign's coefficient
  should be NEGATIVE (a positive impulse predicts a subsequent NEGATIVE 11:10-13:00 return) with
  |t|>=2, controlling for trailing_vol and prior_hour_return (the generic-reversal proxy). This
  mirrors the precedent's `ortho_ok = abs(ind_t) >= 2.0 and ind_coef > 0` gate, sign-flipped
  because this lane's mechanism is a REVERSAL (fade), not the precedent's momentum-continuation
  hypothesis.

Placebo null -- TWO resolutions, both drawn from the SAME 6-candidate menu of ET anchor hours
structurally clear of the real fix window (06:00,07:00,08:00,09:00,12:00,13:00 ET -- 14:00 was
dropped: its +3h hourly outcome-end needs h17, which is absent for ALL 624 calendar dates in the
panel = the CME Globex daily trading-halt hour, 16:00-17:00 CT / 17:00-18:00 ET, confirmed
empirically, not a data gap):
  (a) HOURLY-PROXY null (R_hourly, 1000 replicates): each candidate's placebo return uses the
      coarse hour-bar construction (open[hh+1]-open[hh] impulse, open[hh+3]-open[hh+1] outcome).
      Apples-to-apples with the ROBUSTNESS/cross-check R_hourly real statistic.
  (b) MINUTE-RESOLUTION null (R_precise, 1000 replicates) -- added per adversarial review of the
      first B2.2 pass: the original (a)-only design compared the DECISIVE orthogonality leg's
      R_precise (built from 1m bars) against a placebo null built only from R_hourly (1h bars) --
      disclosed as a design choice, but a strictly tighter test was feasible (the 1m panel was
      already pulled) and had not been run. (b) mirrors the LITERAL minute-offset structure of
      the real precise window (-2min/+4min impulse relative to the anchor hour, +10min/+2h00m
      outcome) at each of the same 6 candidate anchor hours, using 1m bar opens throughout, so the
      DECISIVE real statistic (R_precise.mean()) is now ranked against a same-resolution null.
      This is the primary/decisive placebo comparison as of this revision; (a) is retained as a
      documented cross-check, not removed.
Each replicate (both nulls) draws, INDEPENDENTLY PER TRADING DAY, a random candidate-hour offset.
"Matched on day-of-week + trailing vol": because every replicate is built from the SAME set of
real trading days (only the CLOCK is randomized, never the day), the day-of-week and trailing-vol
composition of every placebo replicate's day-set is identical to the real sample's BY
CONSTRUCTION -- the strongest possible form of matching, and this holds identically for (b) since
it draws from the same per-day index set as (a) (verified once, applies to both by the same
construction argument -- the day-of-week/trailing-vol match check therefore is not re-run in
duplicate for (b)). The verification step checks this is not silently broken by differential
NaN-dropping (a placebo offset missing data on a day the real construction has, or vice versa).

Kill criterion (frozen, plan's own text): "Kill if the fix dummy adds nothing over generic
reversal or sits <= placebo 60th percentile." Applied per symbol (6E, 6B scored separately, per
the B2.1 ruling scope -- one could survive while the other dies; both died, see RESULTS.md). The
placebo leg is decided on null (b) (R_precise, minute-resolution) as of this revision; the
orthogonality leg (target_precise ~ ...) already used R_precise and is unchanged -- both legs now
share the same clock resolution.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
SYMBOLS = ["6E.v.0", "6B.v.0"]
SEED = 20260824
NREP = 1000
TRAILING_VOL_WINDOW = 20  # trading days

# Placebo candidate impulse-hour starts (ET). Each excludes >=1h buffer from the real 10:58-13:00
# ET span. CME Globex runs a daily trading halt 16:00-17:00 CT = 17:00-18:00 ET (confirmed
# empirically: the h17 column is absent for ALL 624 calendar dates in the pulled panel -- a
# genuine, consistent daily halt, not a data gap) -- so 14 (whose +3h outcome-end would need h17)
# is EXCLUDED from the candidate menu; every remaining candidate's full [h,h+1,h+3] triple stays
# clear of both the real fix window and the halt hour.
PLACEBO_HOURS = [6, 7, 8, 9, 12, 13]

DEGRADED_DAYS = {"2024-09-18", "2025-09-17", "2025-09-24"}  # Databento BentoWarning at pull time


def _precise_hm(anchor_hour: int) -> tuple[str, str, str, str]:
    """The 4 clock-minutes the real precise window needs, generalized to any anchor hour.

    Real anchor = 11 (11:00 ET): impulse_start=10:58, impulse_end=11:04, target_start=11:10,
    target_end=13:00 -- i.e. (-2min, +4min, +10min, +2h00m) relative to the anchor hour. Applying
    the SAME literal offsets to a placebo candidate anchor hour keeps the placebo minute-resolution
    construction structurally identical to the real one (no new researcher degree of freedom).
    """
    imp_start = f"{(anchor_hour - 1) % 24:02d}:58"
    imp_end = f"{anchor_hour % 24:02d}:04"
    tgt_start = f"{anchor_hour % 24:02d}:10"
    tgt_end = f"{(anchor_hour + 2) % 24:02d}:00"
    return imp_start, imp_end, tgt_start, tgt_end


def _precise_hm_needed(anchor_hours: list[int]) -> list[str]:
    hms: set[str] = set()
    for hh in anchor_hours:
        hms.update(_precise_hm(hh))
    return sorted(hms)


def ols(y, X):
    """OLS via lstsq (mirrors the precedent's `_ind_t` helper). Returns beta, se, t, dof."""
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    dof = len(y) - X.shape[1]
    sigma2 = float(resid @ resid) / dof
    cov = sigma2 * np.linalg.inv(X.T @ X)
    se = np.sqrt(np.diag(cov))
    t = beta / se
    return beta, se, t, dof


def load():
    h_path = DATA / "6E_6B_ohlcv1h_2y.parquet"
    m_path = DATA / "6E_6B_ohlcv1m_2y.parquet"
    if not h_path.exists() or not m_path.exists():
        raise FileNotFoundError(
            f"Missing local data cache under {DATA}.\n"
            "Restore (both pulls Rule-1 dry-run confirmed $0.0000; hit the Databento DBN cache "
            "if already pulled once on this machine -- no re-billing):\n\n"
            "  PYTHONPATH=lab python -m databento_fetch.db_fetch pull \\\n"
            "      --symbols 6E.v.0,6B.v.0 --stype continuous --schema ohlcv-1h \\\n"
            "      --start 2024-08-24 --end 2026-08-24 --max-cost 0.01 \\\n"
            f"      --out {h_path}\n\n"
            "  PYTHONPATH=lab python -m databento_fetch.db_fetch pull \\\n"
            "      --symbols 6E.v.0,6B.v.0 --stype continuous --schema ohlcv-1m \\\n"
            "      --start 2024-08-24 --end 2026-08-24 --max-cost 0.01 \\\n"
            f"      --out {m_path}\n"
        )
    hourly = pd.read_parquet(h_path).reset_index()
    minute = pd.read_parquet(m_path).reset_index()
    for df in (hourly, minute):
        df["ts_et"] = df["ts_event"].dt.tz_convert("America/New_York")
        df["date_et"] = df["ts_et"].dt.date
        df["hour"] = df["ts_et"].dt.hour
        df["hm"] = df["ts_et"].dt.strftime("%H:%M")
    return hourly, minute


def build_daily_panel(hourly: pd.DataFrame, minute: pd.DataFrame, symbol: str) -> pd.DataFrame:
    h = hourly[hourly["symbol"] == symbol]
    m = minute[minute["symbol"] == symbol]

    # Hourly wide: open price at each integer ET hour, per date.
    hopen = h.pivot_table(index="date_et", columns="hour", values="open", aggfunc="first")
    hopen.columns = [f"h{c}" for c in hopen.columns]

    # Minute wide: open price at every clock-minute needed for the precise impulse/target,
    # real (anchor=11) plus every placebo candidate anchor (minute-resolution placebo, Step 4b).
    need_hm = _precise_hm_needed([11] + PLACEBO_HOURS)
    msub = m[m["hm"].isin(need_hm)]
    mopen = msub.pivot_table(index="date_et", columns="hm", values="open", aggfunc="first")

    daily = hopen.join(mopen, how="outer")
    daily = daily.reset_index()
    daily["dow"] = pd.to_datetime(daily["date_et"]).dt.dayofweek
    daily["dow_name"] = pd.to_datetime(daily["date_et"]).dt.day_name()
    daily["degraded"] = daily["date_et"].astype(str).isin(DEGRADED_DAYS)

    # Daily close (last observed hourly close of the ET calendar date) -> trailing vol.
    dclose = h.sort_values("ts_et").groupby("date_et")["close"].last()
    dret = dclose.pct_change()
    tvol = dret.rolling(TRAILING_VOL_WINDOW).std().shift(1)  # strictly-prior, no lookahead
    tvol.name = "trailing_vol"
    daily = daily.merge(tvol.reset_index(), on="date_et", how="left")

    # Named quantities.
    daily["prior_hour_return"] = daily.get("h11") - daily.get("h10")  # 10:00-11:00 ET hourly bar
    daily["impulse_precise"] = daily.get("11:04") - daily.get("10:58")  # literal 10:58-11:04 ET
    daily["target_precise"] = daily.get("13:00") - daily.get("11:10")  # literal 11:10-13:00 ET
    daily["robust_outcome_2h"] = daily.get("h13") - daily.get("h11")  # 11:00-13:00 ET (hourly-proxy)

    return daily


def placebo_matrix(daily: pd.DataFrame):
    """For each candidate offset hour, the per-day strategy-signed placebo return R_h.
    Returns R_matrix [n_days, n_candidates]."""
    cols = []
    for hh in PLACEBO_HOURS:
        for need in (hh, hh + 1, hh + 3):
            assert f"h{need}" in daily.columns, (
                f"placebo candidate hour={hh} needs column h{need}, absent from the panel "
                f"(likely the CME daily-halt hour) -- drop this candidate")
        imp = daily[f"h{hh+1}"] - daily[f"h{hh}"]
        out = daily[f"h{hh+3}"] - daily[f"h{hh+1}"]
        R = -np.sign(imp) * out
        cols.append(R.to_numpy(dtype=float))
    return np.column_stack(cols)


def placebo_matrix_precise(daily: pd.DataFrame):
    """Minute-resolution analogue of placebo_matrix (Step 4b, added per adversarial review):
    for each candidate anchor hour, the per-day strategy-signed placebo return built from 1m bar
    opens at the SAME literal minute offsets as the real precise window (see `_precise_hm`), not
    the coarse hourly proxy. Returns R_matrix [n_days, n_candidates] -- same shape/candidate order
    as placebo_matrix, so the two nulls are directly comparable."""
    cols = []
    for hh in PLACEBO_HOURS:
        imp_start, imp_end, tgt_start, tgt_end = _precise_hm(hh)
        for c in (imp_start, imp_end, tgt_start, tgt_end):
            assert c in daily.columns, (
                f"placebo candidate anchor={hh} needs minute column {c}, absent from the panel "
                f"(likely the CME daily-halt hour) -- drop this candidate")
        imp = daily[imp_end] - daily[imp_start]
        out = daily[tgt_end] - daily[tgt_start]
        R = -np.sign(imp) * out
        cols.append(R.to_numpy(dtype=float))
    return np.column_stack(cols)


def run_symbol(hourly, minute, symbol):
    print("=" * 100)
    print(f"SYMBOL: {symbol}")
    print("=" * 100)
    daily = build_daily_panel(hourly, minute, symbol)
    n_all = len(daily)

    req_cols = ["trailing_vol", "prior_hour_return", "impulse_precise", "target_precise",
                "robust_outcome_2h"]
    valid = daily.dropna(subset=req_cols).copy()
    valid = valid[valid["impulse_precise"] != 0]  # guard exact-zero tie (should not occur on FX)
    n_valid = len(valid)
    n_degraded = int(valid["degraded"].sum())
    print(f"panel: {n_all} ET calendar dates in range; {n_valid} valid fix-observations "
          f"({n_degraded} flagged degraded-quality by Databento, included -- see robustness note)")

    imp_sign = np.sign(valid["impulse_precise"].to_numpy())
    target = valid["target_precise"].to_numpy()
    R_precise = -imp_sign * target

    hourly_imp_sign = np.sign(valid["prior_hour_return"].to_numpy())
    R_hourly = -hourly_imp_sign * valid["robust_outcome_2h"].to_numpy()

    # ---- Step 3: mean 11:10-13:00 return conditioned on impulse sign (not pooled across symbols) ----
    print("\n--- Step 3: mean target_precise (11:10-13:00 ET) conditioned on precise impulse sign ---")
    for s, tag in [(1, "impulse UP (10:58-11:04 rose)"), (-1, "impulse DOWN (10:58-11:04 fell)")]:
        m = imp_sign == s
        vals = target[m]
        print(f"  {tag:<32} n={m.sum():4d}  mean_target={vals.mean():+.6f}  "
              f"std={vals.std(ddof=1):.6f}  t={vals.mean()/(vals.std(ddof=1)/np.sqrt(len(vals))):+.2f}")
    print(f"  strategy-signed R_precise (fade the impulse): n={len(R_precise)} "
          f"mean={R_precise.mean():+.6f} t={R_precise.mean()/(R_precise.std(ddof=1)/np.sqrt(len(R_precise))):+.2f}")
    print(f"  [cross-check, hourly-proxy clock] R_hourly: n={len(R_hourly)} "
          f"mean={R_hourly.mean():+.6f} t={R_hourly.mean()/(R_hourly.std(ddof=1)/np.sqrt(len(R_hourly))):+.2f}")

    # ---- Step 5: orthogonality regression (adapted from the gamma-family precedent) ----
    print("\n--- Step 5: orthogonality regression (trailing-vol + prior-hour-return controls) ---")
    tv = valid["trailing_vol"].to_numpy()
    phr = valid["prior_hour_return"].to_numpy()

    Xa = np.column_stack([np.ones(n_valid), imp_sign])
    betaA, seA, tA, dofA = ols(target, Xa)
    print(f"  Model A  target ~ 1 + imp_sign                         : "
          f"coef(imp_sign)={betaA[1]:+.6f}  t={tA[1]:+.2f}  (n={n_valid}, dof={dofA})")

    Xb = np.column_stack([np.ones(n_valid), phr])
    betaB, seB, tB, dofB = ols(target, Xb)
    print(f"  Model B  target ~ 1 + prior_hour_return                 : "
          f"coef(phr)={betaB[1]:+.6f}  t={tB[1]:+.2f}  (n={n_valid}, dof={dofB})  "
          f"[generic-reversal baseline]")

    Xc = np.column_stack([np.ones(n_valid), tv, phr, imp_sign])
    betaC, seC, tC, dofC = ols(target, Xc)
    ind_t, ind_coef = tC[3], betaC[3]
    ortho_ok = abs(ind_t) >= 2.0 and ind_coef < 0  # fade hypothesis: NEGATIVE sign required
    print(f"  Model C  target ~ 1 + trailing_vol + prior_hour_return + imp_sign  [THE DECISIVE GATE]")
    print(f"           coef(trailing_vol)   ={betaC[1]:+.6f}  t={tC[1]:+.2f}")
    print(f"           coef(prior_hour_ret) ={betaC[2]:+.6f}  t={tC[2]:+.2f}")
    print(f"           coef(imp_sign)       ={betaC[3]:+.6f}  t={tC[3]:+.2f}  "
          f"(n={n_valid}, dof={dofC})")
    corr_phr = float(np.corrcoef(imp_sign, phr)[0, 1])
    print(f"           corr(imp_sign, prior_hour_return) = {corr_phr:+.3f}")
    print(f"  -> imp_sign after partialling trailing_vol+prior_hour_return: "
          f"{'ORTHOGONAL (adds signal, |t|>=2, correct fade sign)' if ortho_ok else 'PROXY/NULL (fix dummy adds nothing over generic reversal)'}")

    # ---- Step 4 + placebo comparison: hourly-clock-family null, 1000 replicates ----
    print("\n--- Step 4: placebo null (1000 replicates, hourly-clock family, day-of-week + "
          "trailing-vol matched by construction) ---")
    R_matrix = placebo_matrix(valid)
    n_cand = R_matrix.shape[1]
    finite_frac = np.isfinite(R_matrix).mean()
    print(f"  candidate offsets (ET): {PLACEBO_HOURS}  finite-cell coverage={finite_frac:.3f}")

    rng = np.random.default_rng(SEED)
    idx_days = np.arange(n_valid)
    null_stats = np.empty(NREP)
    pooled_dow = []
    pooled_tv = []
    real_dow = valid["dow"].to_numpy()
    for r in range(NREP):
        offset_idx = rng.integers(0, n_cand, size=n_valid)
        vals = R_matrix[idx_days, offset_idx]
        ok = np.isfinite(vals)
        null_stats[r] = np.nanmean(vals)
        if r < 50:  # sample the first 50 replicates' realized day-sets for the composition check
            pooled_dow.append(real_dow[ok])
            pooled_tv.append(tv[ok])
    pooled_dow = np.concatenate(pooled_dow)
    pooled_tv = np.concatenate(pooled_tv)

    real_stat = R_hourly.mean()
    p60_value = np.percentile(null_stats, 60)
    rank_pct = float((null_stats < real_stat).mean() * 100)
    placebo_kill = real_stat <= p60_value
    print(f"  REAL hourly-clock statistic mean(R_hourly) = {real_stat:+.6f}")
    print(f"  placebo null: mean={null_stats.mean():+.6f} std={null_stats.std():.6f} "
          f"p10={np.percentile(null_stats,10):+.6f} p50={np.percentile(null_stats,50):+.6f} "
          f"p60={p60_value:+.6f} p90={np.percentile(null_stats,90):+.6f}")
    print(f"  real stat's percentile RANK within the 1000-draw null distribution = {rank_pct:.1f}")
    print(f"  -> {'KILL (real <= placebo 60th pct)' if placebo_kill else 'clears placebo 60th pct'}")

    # ---- Step 4b: MINUTE-RESOLUTION placebo null, 1000 replicates (added per adversarial review:
    # the decisive orthogonality leg uses R_precise (1m bars) but Step 4 above ranks it against a
    # null built only from R_hourly (1h bars) -- disclosed as a design choice, not silently
    # assumed, but a strictly tighter test was feasible since the 1m panel was already pulled.
    # This makes the placebo leg use the SAME clock resolution as the decisive orthogonality leg.
    # `rng` continues the same stream started above (not reseeded) -- same day-index sampling
    # mechanism, so day-of-week/trailing-vol matching holds by the identical construction argument
    # verified below for Step 4; not re-verified in duplicate for this resolution.) ----
    print("\n--- Step 4b: placebo null (1000 replicates, MINUTE-RESOLUTION clock family -- same "
          "literal -2min/+4min/+10min/+2h00m minute-offset structure as the real precise window "
          "-- PRIMARY/decisive placebo comparison as of this revision) ---")
    Rp_matrix = placebo_matrix_precise(valid)
    finite_frac_p = np.isfinite(Rp_matrix).mean()
    print(f"  candidate anchor hours (ET): {PLACEBO_HOURS}  finite-cell coverage={finite_frac_p:.3f}")

    null_stats_p = np.empty(NREP)
    for r in range(NREP):
        offset_idx = rng.integers(0, n_cand, size=n_valid)
        vals = Rp_matrix[idx_days, offset_idx]
        null_stats_p[r] = np.nanmean(vals)

    real_stat_p = R_precise.mean()
    p60_value_p = np.percentile(null_stats_p, 60)
    rank_pct_p = float((null_stats_p < real_stat_p).mean() * 100)
    placebo_kill_p = real_stat_p <= p60_value_p
    print(f"  REAL precise (1m) statistic mean(R_precise) = {real_stat_p:+.6f}")
    print(f"  placebo null: mean={null_stats_p.mean():+.6f} std={null_stats_p.std():.6f} "
          f"p10={np.percentile(null_stats_p,10):+.6f} p50={np.percentile(null_stats_p,50):+.6f} "
          f"p60={p60_value_p:+.6f} p90={np.percentile(null_stats_p,90):+.6f}")
    print(f"  real stat's percentile RANK within the 1000-draw MINUTE-RESOLUTION null = {rank_pct_p:.1f}")
    print(f"  -> {'KILL (real <= placebo 60th pct)' if placebo_kill_p else 'clears placebo 60th pct'}")

    # ---- Verification: placebo day-of-week / trailing-vol composition matches the real sample ----
    print("\n--- verification: placebo-window day-of-week + trailing-vol match check ---")
    real_dow_freq = pd.Series(real_dow).value_counts(normalize=True).sort_index()
    plac_dow_freq = pd.Series(pooled_dow).value_counts(normalize=True).sort_index()
    dow_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    max_dow_dev = 0.0
    for d in real_dow_freq.index:
        rv = real_dow_freq.get(d, 0.0)
        pv = plac_dow_freq.get(d, 0.0)
        max_dow_dev = max(max_dow_dev, abs(rv - pv))
        print(f"    dow={dow_names[d]:<4} real={rv:.3f}  placebo-pooled={pv:.3f}  "
              f"delta={rv-pv:+.3f}")
    real_tv_q = np.percentile(tv, [25, 50, 75])
    plac_tv_q = np.percentile(pooled_tv, [25, 50, 75])
    print(f"    trailing_vol quartiles: real={real_tv_q}  placebo-pooled={plac_tv_q}")
    match_ok = max_dow_dev < 0.03 and np.all(np.abs(real_tv_q - plac_tv_q) / real_tv_q < 0.05)
    print(f"    -> {'MATCH CONFIRMED' if match_ok else 'MATCH FAILED -- investigate before trusting the null'}"
          f" (max dow delta={max_dow_dev:.3f}, tv quartile rel-dev="
          f"{np.max(np.abs(real_tv_q - plac_tv_q) / real_tv_q):.3f})")

    # ---- Robustness: exclude degraded-quality days, recompute the decisive number ----
    if n_degraded:
        clean = valid[~valid["degraded"]]
        c_imp_sign = np.sign(clean["impulse_precise"].to_numpy())
        c_target = clean["target_precise"].to_numpy()
        c_tv = clean["trailing_vol"].to_numpy()
        c_phr = clean["prior_hour_return"].to_numpy()
        Xc2 = np.column_stack([np.ones(len(clean)), c_tv, c_phr, c_imp_sign])
        betaC2, seC2, tC2, _ = ols(c_target, Xc2)
        print(f"\n  robustness (excl. {n_degraded} degraded days): coef(imp_sign)={betaC2[3]:+.6f} "
              f"t={tC2[3]:+.2f}  (was {ind_coef:+.6f} / t={ind_t:+.2f} with them included)")

    # ---- Kill criterion ----
    # Placebo leg is decided on the MINUTE-RESOLUTION null (Step 4b, placebo_kill_p) as of this
    # revision -- same clock resolution as the decisive orthogonality leg. The hourly-proxy null
    # (Step 4, placebo_kill) is reported alongside as a cross-check, not dropped.
    print("\n--- FROZEN KILL CRITERION ---")
    print('  "Kill if the fix dummy adds nothing over generic reversal OR sits <= placebo 60th '
          'percentile."')
    reversal_kill = not ortho_ok
    dies = reversal_kill or placebo_kill_p
    print(f"  orthogonality leg : {'FAIL -> kill-eligible' if reversal_kill else 'PASS'} "
          f"(imp_sign |t|={abs(ind_t):.2f}, sign={'neg (correct)' if ind_coef<0 else 'pos (wrong)'})")
    print(f"  placebo leg (b)   : {'FAIL -> kill-eligible' if placebo_kill_p else 'PASS'} "
          f"(minute-resolution real rank pct={rank_pct_p:.1f}, need > 60)  [DECISIVE]")
    print(f"  placebo leg (a)   : {'FAIL -> kill-eligible' if placebo_kill else 'PASS'} "
          f"(hourly-proxy real rank pct={rank_pct:.1f}, need > 60)  [cross-check]")
    print(f"  VERDICT ({symbol}): {'DEAD' if dies else 'SURVIVES'}")

    return dict(
        symbol=symbol, n_valid=n_valid, n_degraded=n_degraded,
        mean_target_up=target[imp_sign == 1].mean(), mean_target_down=target[imp_sign == -1].mean(),
        R_precise_mean=R_precise.mean(), R_hourly_mean=R_hourly.mean(),
        modelA_t=tA[1], modelB_t=tB[1], modelC_imp_t=ind_t, modelC_imp_coef=ind_coef,
        corr_imp_phr=corr_phr, ortho_ok=ortho_ok,
        placebo_real_stat=real_stat, placebo_p60=p60_value, placebo_rank_pct=rank_pct,
        placebo_kill=placebo_kill,
        placebo_real_stat_precise=real_stat_p, placebo_p60_precise=p60_value_p,
        placebo_rank_pct_precise=rank_pct_p, placebo_kill_precise=placebo_kill_p,
        match_ok=match_ok, dies=dies,
    )


def main():
    hourly, minute = load()
    results = {}
    for sym in SYMBOLS:
        results[sym] = run_symbol(hourly, minute, sym)

    print("\n" + "=" * 100)
    print("SUMMARY (per B2.1 ruling: 6E and 6B scored separately, never pooled)")
    print("=" * 100)
    for sym, r in results.items():
        print(f"{sym}: n={r['n_valid']}  imp_sign t(orthogonal)={r['modelC_imp_t']:+.2f} "
              f"coef={r['modelC_imp_coef']:+.6f}  "
              f"placebo_rank(b:minute,DECISIVE)={r['placebo_rank_pct_precise']:.1f}pct  "
              f"placebo_rank(a:hourly,x-check)={r['placebo_rank_pct']:.1f}pct  "
              f"-> {'DEAD' if r['dies'] else 'SURVIVES'}")
    return results


if __name__ == "__main__":
    main()
