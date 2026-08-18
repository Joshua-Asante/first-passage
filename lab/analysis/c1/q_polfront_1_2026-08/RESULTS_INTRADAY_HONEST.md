# Q-POLFRONT-1 — intraday-honest remeasurement RESULTS (closure §7 fork, executed)

**Run:** 2026-08-17 · fork of [Q-POLFRONT-1](../../../../docs/briefs/closures/Q-POLFRONT-1-closure-resolved-quantified.md) §7
**Method:** [`OPERATIONALIZATION_INTRADAY_HONEST.md`](OPERATIONALIZATION_INTRADAY_HONEST.md) §6 (v3, deterministic
real-trade-calibrated median multiplier) — v1 (instrument-price-shape) and v2 (resampled real-trade
ratio) both invalidated pre-write-up, full postmortem in that file's §4/§5.
**Verdict: SAFE_WITH_CAVEATS** — adversarially verified (2026-08-17, 4 independent reviewers +
synthesis). No coding-level defect found; two confirmed calibration biases, **both pushing toward
overstating risk**, with no offsetting bias found. **Read every number below as a credible upper
bound / conservative proxy, not a tight point estimate** — see §3.
**Spend / K:** $0 · K=0 · measurement only · no candidate, no admission, no deployment surface, no
re-sweep (re-evaluated only at each cell's already-claimed EOD-clock `R_max`).

---

## 1. Headline: the EOD-clock frontier does not survive real intraday excursion — for either arm

| Statistic | Flat arm | Policy arm |
|---|---|---|
| Cells with a defined EOD-clock `R_max` | 24 | 26 |
| **Median bust-rate delta (EOD → intraday-honest)** | **+18.0pp** | **+98.1pp** |
| Min / max delta | +0.61pp / +98.47pp | 0.0pp / +100.0pp |
| **Cells still clearing the 3.0% ceiling** | **2 / 24** | **1 / 26** |

The two flat-arm survivors are both low-R cells: `(w=0.4,b=2.0,k=1)` R=$75 (0.63%→1.32%) and
`(w=0.5,b=1.2,k=1)` R=$75 (1.37%→1.98%). The one policy survivor,
`(w=0.35,b=2.0,k=2)` R=$200 (0.0%→0.0%), is one of the two cells the original EOD measurement
flagged as "newly admitted by policy" at a very small R.

**Delta is monotonic in `R_max` relative to `ROPE`** ($3,000), not a uniform artifact — this is
the load-bearing structural signal that separates this measurement from v1/v2's uniform, arm-
insensitive collapses:

| `R_flat_max` | deltas observed at that R (across the k∈{1,2,4} cells sharing it) |
|---|---|
| $75 | 0.61, 0.69, 1.45, 2.99 |
| $100 | 6.84, 13.0 |
| $175 | 2.32, 6.27, 6.69, 14.46, 21.52, 54.36 |
| $225 | 6.58, 14.48, 50.48 |
| $250 | 45.93, 97.12 |
| $275 | 86.98 |
| $350 | 24.22, 73.8, 98.47 |
| $475 | 40.56, 97.95, 98.23 |

## 2. Why the policy arm collapses near-uniformly: a closed-form mechanism, not an MC artifact

The independent-reimplementation adversarial reviewer derived this from the breach formula
directly (not just observed it empirically): under the deterministic injection, **any winning
day breaches once `r_base > ROPE / (|win_mult| × b)`** — independent of the path's current
drawdown level, because the cushion-dependent terms cancel algebraically. For `(w=0.55,b=2.0)`
that threshold is **≈$732**; the claimed `R_policy_max=$1,825` sits **2.5×** over it. The policy
arm's own EOD-clock admissibility depends on `m_t` throttling size down as cushion shrinks — but
`m_t` is set at the **start** of the day, before that day's real excursion is known. A real
winning day's typical dip (median `win_mult=−2.049`, i.e., the day trades ~2× its eventual gain
underwater before recovering) routinely exceeds the remaining cushion at the R levels the EOD-only
measurement judged admissible. This is exactly the mechanism the parent closure's own caveat
named ("the policy's near-zero-bust result depends on the multiplier reacting to a drawdown
*before* the day's worst excursion happens") — this measurement quantifies it and shows it is
close to deterministic, not a tail risk.

## 3. ⚠ The load-bearing caveat: both confirmed biases push toward overstating risk

Adversarial review (methodology/units lens) confirmed two calibration biases in the real-trade
ratio source, **neither corrected in the numbers above**:

1. **Pyramiding contamination (dominant).** The reused `_leg_daily_excursion` (W1's own method)
   applies one constant $/point rate — calibrated to each trade's *final, pyramid-inflated*
   realized P&L — across the entire price path, including the early low where the account
   actually carried only base size (Striker pyramids up to 750%/1000% on continued favorable
   movement, landing **late** in a winning trade's life). This retroactively inflates measured
   excursion at the point a smaller position was actually on. In-repo corroboration: NAS100's
   base-only (non-pyramided) PF is 0.31 — the edge is structurally inseparable from pyramiding in
   this specific trade record, so no clean "fixed-1R" reading exists to correct this from the
   available data. **Inflates `win_mult` specifically** — `−2.049` is very likely an overstatement
   of the true fixed-size risk a non-pyramided synthetic trade would carry.
2. **Multi-trade-day additive summing.** ~Half of the real trades (267/284 total, only 197/206
   distinct trade-days) share an exit day with a second trade; the reused excursion function sums
   each trade's own dip additively into one day-level figure, overstating the true combined-equity
   worst point (two trades' worst moments rarely coincide exactly). **Inflates both `loss_mult`
   and `win_mult`.**

Both biases push the **same direction** and no offsetting bias was found. A bias-corrected
re-measurement was not attempted this session — the pyramiding contamination may not be cleanly
separable from this trade record at all (per the PF-0.31 finding) — and is named as a further,
unopened fork, not resolved here.

**Read this as:** the *qualitative* finding (both arms fail this test far more than the crude ×2
stress arm suggested; the policy arm is dramatically and structurally more fragile than the flat
arm; the failure has an analytic mechanism, not just an empirical one) is well-corroborated and
should carry weight. The *quantitative* severity (only 1–2 cells surviving; near-total policy
collapse) is a **credible upper bound**, not a precise estimate — a bias-corrected version would
likely show somewhat better survival, particularly on the policy arm's win-day exposure.

## 4. What this does NOT establish

Per the parent brief's §5 (frozen, inherited): no cell here is an admission, a candidate, or a
WATCH-rung change. No new R_max sweep was opened under the intraday-honest clock — only the
already-claimed EOD-clock frontier was tested for survival. Does not touch `core/`,
`dd_protection.py`, or any locked/allocation constant.

## 5. Recommendation for the deep-iteration lane (GO-1 / campaign 2)

The Q-POLFRONT-1 closure's own routing said any campaign leaning materially on the policy
frontier should open this remeasurement first, "with the intraday-clock caveat carried into the
campaign's own prereg as a named risk, not silently." That caveat is no longer a named-but-
unopened risk — it is now quantified and mechanistically explained: **the policy-augmented
frontier should not be relied on for family selection or R sizing.** The flat-arm frontier is
usable but only at low R relative to ROPE (the two surviving cells: R≤$75) — this narrows, not
widens, the admissible design space the deep-lane's campaign 2 should target, the opposite
direction of the original 5.1× headline. DL-1's own family selection did not lean on the policy
frontier (N-SURV primary scoring was flat-R; the Q-POLFRONT-1 caveat was carried as disclosure
only), so this finding does not retroactively implicate DL-1's abandonment — but it does mean
campaign 2 should treat the flat-R frontier itself with the same R-relative-to-ROPE caution this
measurement surfaces, not just the policy arm.

## Files

`OPERATIONALIZATION_INTRADAY_HONEST.md` (frozen method + full v1/v2/v3 postmortem) ·
`run_polfront_intraday_honest.py` (runner) · `out/real_mae_ratios.json` (derived ratio
distribution, non-vendor) · `out/polfront_intraday_honest_results.json` (full 30-cell raw output)
· derivation script (scratchpad, not committed — real-trade CSVs are gitignored vendor data;
re-run from the primary checkout to reproduce).
