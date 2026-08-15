# PRE-REGISTRATION — Q-REGIME-COND-1 (re-scoped, Option B) — FROZEN 2026-06-30

**Status:** FROZEN on the commit that adds this file. Append-only hereafter; any §1–§6 change
after a forward return is inspected VOIDS the run (brief §5 #1, §9; INQHIORI gate).
**Brief:** Q-REGIME-COND-1 (Pre-Q, 2026-06-29). Disposition chosen by operator 2026-06-30:
**run only the genuinely-new angle** — composite vs **SPY** forward second-moment at daily power,
with the trailing-realized-vol orthogonalization as the load-bearing null — on free-fetchable data,
**explicitly de-coupling Q1-RESOLVED from authorizing any Q2 book-level overlay** (see §7).
**Audit anchor:** this commit must precede the first commit that reads/joins SPY forward returns
(`conditional.py`). `panel.py`/`panel.csv`/`coverage.json` (composite + states only, NO forward
returns) are frozen with it.

## 0. Why re-scoped (the Phase-0 finding this run is built on)

The brief's assumed multi-axis daily panel does not exist on disk; the free credit axis is FRED-capped
at ~3y (pre-2023 OAS needs paid ICE/ALFRED); and the question family was already attacked across
**14 free candidates + Hurst + the VIX-brake**, all closed NULL/FALSIFIED 2026-06-22/25/26
(`lab/analysis/regime_signal_research_2026-06-25/CLOSURE.md` + `extension_newfree_2026-06-26/`;
`docs/ltm/briefs/Q-REGIME-ADAPT-1-closure-falsified.md`). Those closures tested **individual** signals
against the **book's** episode-level co-drawdown (N=33, underpowered to |ρ|≈0.36), residualized on
vol+calendar. This run is the one genuinely-new, decision-relevant angle they did NOT cover: does a
**composite** carry conditional forward second-moment information **on the broad equity index at high
daily power**, surviving orthogonalization against trailing realized vol? A clean NULL here strengthens
the closure at high power; a RESOLVED is the (known) variance-risk-premium effect on SPY and is **still
de-coupled from the book** (§7).

## 1. Frozen composite (built by `panel.py`, frozen in `panel.csv`)

Four axes, one representative free proxy each (avoids intra-axis double-count), each oriented so
**higher oriented-z = more risk-off**. Normalization is **EXPANDING / point-in-time** (warmup 252
trading days); full-sample z/PCA is forbidden (§5).

| axis | proxy | source | orient | raw span |
|---|---|---|--:|---|
| volatility | VIX | CBOE CDN `VIX_History.csv` | +1 | 1990→ |
| credit | HYG/LQD ratio | Yahoo HYG, LQD | −1 (high HY/IG = risk-on) | 2007-04-11→ (binding) |
| rates / cross-asset | MOVE | Yahoo `^MOVE` | +1 | 2002-11→ |
| FX | DXY | Yahoo `DX-Y.NYB` | +1 (broad USD strength = risk-off) | 1996→ |

- **Common sample:** 2007-04-11 → 2026-06-30 (4866 rows; binding = HYG inception). Pre-2008 is
  warmup → **states emit 2009-04-07 onward** (n≈4364). 2008 GFC is in warmup, NOT in the analysis
  window (logged limitation; consequence of strict point-in-time double warmup).
- **PRIMARY composite** = equal-weight mean of the 4 oriented expanding-z (requires all 4 present).
- **SECONDARY composite** = expanding PCA-1 (loadings refit point-in-time every 5 days, sign-aligned
  to the equal-weight composite using data ≤ t). Reported for comparison; NOT primary.

## 2. Frozen states — K=3 (pre-registered; brief §0.5 #4)

States = **point-in-time tercile cuts** on the composite (thresholds at t use only composite values
≤ t; warmup 252). Labels: `off` (risk-off, composite ≥ running q67), `neutral`, `on` (risk-on, ≤ q33).
K=3 is fixed blind and may not change after returns are seen (§5).

## 3. Frozen forward asset, horizons, returns

- **Forward asset:** SPY **adjusted close** (total return). Fetched in `conditional.py` (post-freeze).
- **Horizons:** {1d, 5d, 20d} (no post-hoc additions — §5 #4).
- **Forward return** at date t, horizon h: `r_fwd(t,h) = log(adj[t+h] / adj[t])`, conditioned on the
  **state at t** (state uses data ≤ t; forward uses t+1..t+h → no leakage).
- **Sampling:** **non-overlapping** (stride h, offset 0) is PRIMARY. Overlapping daily-sampled with
  Newey-West(h-1) SEs is reported as SECONDARY only (brief §5 #4).

## 4. Frozen conditional metrics (per state × horizon)

mean; **stdev**; **max drawdown** (worst peak-to-trough within each forward window's cumulative path,
summarized as mean and p95 across windows in the bucket); **downside semideviation**
(`sqrt(mean(min(r,0)^2))`); skew; **5% CVaR** and **1% CVaR** (mean of the worst 5% / 1% forward
returns); hit rate (fraction > 0). Second-moment metrics (stdev, maxDD, semidev, CVaR) are the
hypothesis-bearing ones; mean/skew/hit-rate are recorded, **non-gating** (§7 brief: directional/mean
separation is secondary and a null mean does NOT falsify H).

## 5. The load-bearing null (brief Step 2.6) — frozen procedure

1. Trailing realized vol `RV(t)` = 20d rolling std of SPY daily log-returns (trailing, available at t).
2. **Residual composite** = residual of an **expanding OLS** of `composite_t` on `[1, RV_t]`
   (coefficients use data ≤ t → point-in-time). A full-sample-OLS residual is reported as a labeled
   non-point-in-time cross-check only.
3. **Re-derive states from the residual** via the SAME expanding-tercile procedure (§2). This is a
   genuine re-derivation, not a re-label of raw states (brief §7 Pass B).
4. Re-run §4 on the residual-states; emit the residual-state table **side-by-side** with the raw-state
   table. **Skipping this step does not RESOLVE the brief** (§5 #5).

## 6. Frozen test statistics, robustness, and significance

**Separation statistics** (pre-registered sign: risk-off worse ⇒ all expected > 0), per horizon h:
- `SEP_vol(h)  = stdev(r_fwd|off) − stdev(r_fwd|on)`
- `SEP_cvar(h) = |CVaR5(r_fwd|off)| − |CVaR5(r_fwd|on)|`
- **Monotonicity** required for an (a)-pass: `stdev(off) > stdev(neutral) > stdev(on)` (and likewise
  for CVaR), i.e. neutral sits strictly between.

**Placebo (brief §2.7):** block-shuffle the **state labels** with a **21-trading-day circular block**
(preserves autocorrelation), B=2000, recompute SEP. Real SEP must exceed the **95th percentile** of the
shuffled distribution (one-sided). Report the percentile.

**Block-bootstrap CIs (brief §2.7):** 21-day circular block bootstrap (B=2000) on the (state, r_fwd)
daily series; recompute each per-state metric; report 5/50/95. **iid bootstrap is forbidden** (§5 #7).

**Drop-one-axis jackknife:** recompute composite leaving out each axis; report SEP sensitivity.

**Subperiod stability:** halves of the emitted window (2009–2017 vs 2018–2026) and **COVID-in/out**
(drop 2020-02→2020-06). **pre-2008 is infeasible** (warmup; logged). Report sign/separation stability.

**Multiplicity discount (brief §2.7):** the **primary family** = equal-weight composite × residual
states × {5d, 20d} × {SEP_vol, SEP_cvar} = **4 tests**. FWER via **max-statistic permutation**
(Westfall-Young) across that family on the shared block-shuffles. PCA-1, 1d, and raw-state results are
secondary/robustness, not in the primary multiplicity family.

## 7. De-coupling clause (operator-mandated; binding)

A **RESOLVED** verdict here establishes ONLY that the composite carries beyond-trailing-vol
second-moment information **on the broad equity index (SPY)** — which is the well-known
variance-risk-premium effect and which the brief itself (§4 secondary) says warrants heightened
overfitting suspicion if treated as novel. It **does NOT authorize a Q2 book-level overlay**: the
2026-06-25/26 battery already FALSIFIED equity→book transfer (the same axes did not rank the book's
gold/FX/index co-drawdown beyond vol+calendar at N=33). Q2 remains gated on a SEPARATE **book-level**
characterization, never on this SPY result. This clause may not be weakened post-hoc.

## 8. Gate (binary closure — brief §6)

- **RESOLVED** — residual-state separation (§6) satisfies (a) monotone in expected direction, (b)
  beats placebo ≥95th pct, (c) survives the multiplicity discount, for ≥1 of {vol, CVaR} at 5d and/or
  20d. → Q1 answered YES *on SPY*; Q2 still gated by §7 (a book-level brief, not auto-authorized).
- **FALSIFIED** — raw separation collapses in residual states, OR fails placebo, OR vanishes under
  multiplicity. → composite is (at the index level) substantially repackaged trailing vol; vol-target
  directly; book "composite is repackaged volatility on SPY" + strengthens the existing closure.
- **AMBIGUOUS** — residual separation present but non-monotone, horizon-fragile, or CI-straddles-zero;
  OR a forbidden move detected. → record blocker.

## 9. Forbidden moves (brief §5; binding)

Inspecting any SPY forward return before this file is committed; full-sample z / PCA loadings;
state boundaries from any return-derived quantity; overlapping-return t-stats as primary; skipping
§5 (the vol-orthogonalization null); HMM/Markov-switching in v1; iid bootstrap; building any
overlay/sizing logic; changing K / horizons / cuts / metric list / signs after seeing returns;
weakening §7.

## 10. Reproduce

```bash
cd lab/analysis/regime_cond_2026-06-30
python panel.py --selftest && python panel.py     # FROZEN at this commit (no forward returns)
# --- pre-registration commit boundary ---
python conditional.py    # post-freeze: fetches SPY, forward returns, raw+residual conditional tables
python robustness.py     # placebo, block-bootstrap CIs, jackknife, subperiod, multiplicity
```
