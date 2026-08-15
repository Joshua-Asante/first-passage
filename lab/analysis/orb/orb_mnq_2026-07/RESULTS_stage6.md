# ORB-MNQ-1 Stage-5/6 RESULTS — confirm gate (DSR + temporal battery)

**Campaign:** `orb_mnq_intraday_breakout` · **Pre-reg:** [`docs/briefs/pre-registration/2026-07-16-orb-nas100-mnq-reconstruction-preregistration.md`](../../../docs/briefs/pre-registration/2026-07-16-orb-nas100-mnq-reconstruction-preregistration.md) (§8 GO 2026-07-16/JA)
**Harness:** [`run_stage6.py`](run_stage6.py) — uses production `research_utils.{deflated_sharpe,universe_gate,temporal_consistency}` verbatim.
**Precedes:** [`RESULTS.md`](RESULTS.md) (Stage-2 cost-law PASS + placebo p=0.0040).

---

## Verdict — Stage-6 **RESOLVED** per the frozen gate (first venue-native reconstruction survivor) — but a **marginal, cost-fragile, Bulenox-specific** pass; read the caveats

All three frozen §6 limbs clear at the frozen cost model, including on the harder full
confirm window (not only the favorable 2021+ slice):

| Limb (frozen gate) | Result |
|---|---|
| **Sharpe (FULL window 2019-05→present)** | DSR **0.9754** ≥ 0.95 ✓ · annualized SR **+0.890** ≥ 0.85 ✓ (cumulative_k=2, V=1/n, n=1846) |
| **Temporal battery (2021+, §3 override)** | **PASS** — 6a 5/6 yrs+ (thr ⌈0.7·6⌉=5), 6b drop-2024 remaining +83.9>0, 6c SKIPPED, 6d CUSUM 33.8 < null 56.3 |
| **Placebo (within-day, 2021+)** | PASS (p=0.0040) |

Stage-5 block size (ACF, not √T): **2** (both windows — the R series is near-iid, expected for
daily ORB). 2021+ transparency read is comfortable: DSR **0.9922**, annualized SR **+1.185**.
Full-window temporal battery also passes (6/8 yrs+). Return moments: skew **+1.43**, kurt 6.92
(right-skewed — capped losses, trend-day winners; the right-skew *helps* the DSR, legitimately).

---

## The load-bearing caveats (why this is RESOLVED-but-marginal, not a blowout)

### 1. The full-window pass is cost-fragile and **Bulenox-specific**

The frozen gate is defined at the §R.1 economics: Bulenox **$0.61/side** + 1-tick ($0.50) slip
→ RT 1.11 index pt. Stress-testing the RT cost:

| RT cost | annualized SR | DSR | Sharpe limb |
|---|---|---|---|
| 1.11 pt (Bulenox $0.61/side + 1 tick, **frozen**) | +0.890 | 0.9754 | **PASS** |
| 1.39 pt (1.25×) | +0.839 | 0.9654 | **FAIL** |
| 1.67 pt (1.5×) | +0.787 | 0.9523 | FAIL |

A **25% higher round-trip cost flips the full-window gate to FAIL.** The other three FRIENDLY
firms are costlier — Tradeify $0.91/side → RT ≈1.41pt (~1.27×), MFFU/BluSky $0.95/side → RT
≈1.45pt (~1.31×) — so **the full-window pass likely does NOT hold at the three costlier firms.**
The 2021+ window (annSR +1.19, DSR 0.992) has more cushion and may survive the costlier firms;
the full window does not. This is a deployment-fork fact (which firm), and it makes **Stage-7
realism the decisive next gate** — because Stage 7 validates the 1-tick-slip assumption against
real exchange stop-fills, which is exactly the input the pass is most sensitive to.

### 2. This is a confirmation of a **pre-selected** construct, not a blind OOS discovery

Per Default #1 the native-micro re-run is a **realism gate, not an independence axis** — and that
applies with full force here. The construct (OR=2, both-sides, exit-at-close) was frozen from the
2026-06-22 **CFD** ORB study, which itself came out of an extensive CFD-side search (OR-length,
side, exit variants, the N6/N8/N9/N10 cut families). The DSR `cumulative_k=2` deflates for the
**MNQ-family** trials (D5 + this ORB) — it does **not** price the original CFD-side selection K.
The mechanism-first / harvest logic (the original study paid the mining cost; this campaign pays
only the confirmation cost) is the pre-registered justification for entering at low K, and the
within-day placebo + both-sides + regime-robustness were all established CFD-side — but a fully
honest reading is: **this RESOLVED means "the pre-selected CFD construct survives the native-MNQ
feed, costs, and a K=2 deflation," not "a fresh out-of-sample discovery."**

### 3. 6a sits exactly at threshold; 2026 is the watch item

2021+ sign-consistency is **5/6 = exactly** the ⌈0.7·6⌉ threshold. The sole negative sub-era is
**2026-partial** (n=136, meanR −0.0118, ~half a year). At n=136 it is not distinguishable from
zero, but it is the single thing between "at threshold" and "comfortable," and it is the natural
early-regime-fade tripwire for the next quarterly re-eval. Note the same N2/N-series post-2020
regime-conditionality is fully intact here (2019/2020 individually negative).

### 4. Stages 7–8 unrun

- **Stage 7 realism:** integer micro-contract sizing at the $100K prop tiers + native fill
  re-parameterization (exchange stop/limit fills vs the 15m touch-fill). This is now the decisive
  gate (see caveat 1). Force-flat (E1) is trivially satisfied (exit-at-close).
- **Stage 8 breadth:** ENB / correlation-delta vs the book + exposure declaration. Comparison
  target (CFD 4-leg anchor vs the emerging prop-portfolio book) still unresolved (pre-reg §3 flag).

---

## Disposition

- **Stage-6:** RESOLVED per the frozen §6 gate (all three limbs pass at the frozen Bulenox cost
  model, full window included). ORB-MNQ-1 is the **first venue-native reconstruction candidate to
  clear its full confirm gate** — the ORB mechanism transferred to native CME futures where
  locked-Pine R5/P2 did not.
- **Honest headline:** a **marginal, cost-fragile (Bulenox-specific), pre-selected-construct**
  confirmation — comfortable only on 2021+. Not a deployment authorization.
- **Manifest:** stays **open** (Stages 7–8 pending; lifecycle CANDIDATE admission is downstream of
  Stage 8, per the campaign template).
- **Next:** Stage-7 realism is load-bearing precisely because caveat 1 makes the pass sensitive to
  the fill assumption it validates; run it at all four FRIENDLY firms' commissions to map which
  firms the full-window vs 2021+ edge survives at.

Reproduce:

```bash
PYTHONPATH=lab .venv-research/Scripts/python.exe lab/analysis/orb_mnq_2026-07/run_stage6.py
```
