# Q-ORBCUSH-1 Phase 0-1 results — trailing mean-R classifier vs 2021-09-28 break

**Scope of this run:** Phase 0 (Rule-0 reads) + Phase 1 (the pre-registered test) only, per the
task that produced this artifact. Phase 2 (independent second-implementation re-derivation of the
classifier) and Phase 3 (verdict assertion) are **out of scope here** — this file reports raw
numbers, not an Accept/Reject verdict.

**Frozen spec (authoritative):**
[`docs/briefs/pre-registration/Q-ORBCUSH-1-verdict-preregistration.md`](../../../../docs/briefs/pre-registration/Q-ORBCUSH-1-verdict-preregistration.md)
**Brief (context):**
[`docs/briefs/Q-ORBCUSH-1-regime-break-mechanism.md`](../../../../docs/briefs/Q-ORBCUSH-1-regime-break-mechanism.md)

---

## Interpretation note (flagged per both the brief's and the task's own instruction)

The pre-registration specifies a **trade-indexed rolling window** classifier ("rolling window over
the trade sequence ... the classifier is trade-indexed") with an **expanding, causal running
median** as the bucket-split threshold ("never a full-sample statistic"). The orchestrating task
prompt's own restatement of Phase 1 ("build this at daily granularity ... using all realized trade
R's strictly before that day") reads, taken literally, as an *expanding* mean over all history
rather than a rolling W-trade mean. These are reconciled here, not treated as identical by
coincidence: the classifier VALUE is a rolling mean over the trailing W trades (W ∈ {20, 63, 126},
per the pre-registration's window table, which ties 1:1 to the prior vol-regime round's own
`rolling(W).mean().shift(1)` construction) — the pre-registration is treated as authoritative on
this point, since it is unambiguous and the task itself instructs deferring to it on conflict. That
value is then computed at trade granularity and mapped onto the full business-day panel by
date-indexing + forward-fill, which *is* "one classification value per calendar/session day" and
*is* strictly causal (ffill only ever copies a past value forward in time, never a future one into
the past) — satisfying the daily-granularity framing without changing what the rolling window
itself measures. Full implementation detail and an in-code empirical verification of the pandas
`expanding().median()` NaN-skip semantics are in the script's docstring and `build_classifier()`.

---

## (1) Fidelity control

Flat (non-cushion, m=1.0) policy, full panel, `day_loop_intraday` (imported unchanged from the
probe harness), against the published intraday-honest bust rates
(`lab/analysis/orb/orb_mnq_2026-07/RESULTS_t2_intraday_bust.md`):

| k | measured bust% | measured pass% | published bust% | delta (pp) | within 2.0pp tol |
|---|---|---|---|---|---|
| 1 | 67.6667% | 32.3333% | 67.67% | −0.0033 | **PASS** |
| 2 | 77.0100% | 22.9900% | 77.01% | −0.0000 | **PASS** |

**Fidelity control at k=1 (the required check): PASS.** Proceeded to Phase 1 on a validated harness.
(Control B — mirror of `orb_days_with_excursion` vs `orb_lib.orb_backtest` — also PASS, n=1846
triggering days, before this control ran.)

---

## (2) Full 3-window × 2-bucket results

Classifier: trailing rolling-W-trade mean-R, `.shift(1)`-lagged (trade i's classification value
uses only trades i−W..i−1), expanding causal running-median bucket threshold. n_triggering_days =
1846 total. Cutoff = 2021-09-28. K=1 throughout, gate = bust ≤ 3.0% **AND** pass ≥ 50.0%
(`docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md`: horizon=1500,
seeds=(42,123,2026), 10,000 sims/seed).

### Classifier composition (trade counts)

| Window | n trades total | WARMUP | HIGHER (n) | LOWER (n) | Sparsity flag (n<30) |
|---|---|---|---|---|---|
| W1 = 20 | 1846 | 20 | 1020 | 806 | No |
| W2 = 63 | 1846 | 63 | 1127 | 656 | No |
| W3 = 126 | 1846 | 126 | 1190 | 530 | No |

### Date-correlation (fraction of each bucket's DAYS, full panel post-ffill, that fall on/after
2021-09-28 — unrounded to 2 decimals; the pass/fail threshold is evaluated on the raw float, not
the printed rounding)

| Window | HIGHER n_days | HIGHER post-cutoff frac | needs ≥75.00% | LOWER n_days | LOWER post-cutoff frac | needs ≤40.00% | Window date-corr condition |
|---|---|---|---|---|---|---|---|
| W1 = 20 | 1036 | 69.02% | **FAIL** | 822 | 65.33% | **FAIL** | **does not fire** |
| W2 = 63 | 1142 | 74.96% | **FAIL** (0.04pp under) | 672 | 58.93% | **FAIL** | **does not fire** |
| W3 = 126 | 1208 | 80.55% | PASS | 543 | 51.38% | **FAIL** | **does not fire** |

The blocking sub-condition at every single window is the **LOWER-bucket ceiling** (≤40%) — it
misses by 11–25 percentage points at all three windows and never comes close. The HIGHER-bucket
floor (≥75%) is the one that varies: fails at W1, fails narrowly at W2 (74.9562%, 0.0438pp under
threshold — reported to full precision per the "do not round favorably" non-negotiable), passes at
W3. Because both sub-conditions must hold simultaneously, **no window clears date-correlation.**

### Gate-clearance per bucket per window (k=1, cushion = `pol_cushion` imported unchanged; flat =
`pol_const(1.0)` imported unchanged, both run through `day_loop_intraday`/`run_policy_orb`
unchanged)

| Window | Bucket | n_blocks | flat bust% | flat pass% | flat gate | cushion bust% | cushion pass% | cushion gate |
|---|---|---|---|---|---|---|---|---|
| W1=20 | HIGHER | 148 | 30.72% | 69.28% | FAIL | 0.00% | 98.47% | **PASS** |
| W1=20 | LOWER | 99 | 93.88% | 6.12% | FAIL | 0.00% | 1.49% | **FAIL** |
| W2=63 | HIGHER | 194 | 45.40% | 54.60% | FAIL | 0.00% | 88.00% | **PASS** |
| W2=63 | LOWER | 102 | 98.26% | 1.74% | FAIL | 0.00% | 0.11% | **FAIL** |
| W3=126 | HIGHER | 218 | 37.00% | 63.00% | FAIL | 0.00% | 96.40% | **PASS** |
| W3=126 | LOWER | 84 | 96.56% | 3.44% | FAIL | 0.00% | 0.86% | **FAIL** |

**Direction (cushion-arm gate, higher-edge clears / lower-edge does not) at every window:
`HIGHER_CLEARS_LOWER_DOES_NOT`.** Consistent with the already-verified, regime-agnostic
bust-elimination finding (Phase 0 read): cushion sizing drives bust to 0.00% in **both** buckets at
every window — the gate failure in the LOWER bucket is driven entirely by the pass-floor
(0.11%–1.49%, far under 50%), not by bust.

---

## (3) Frozen trigger conditions — raw facts (no verdict computed here)

- **Date-correlation clears at ≥2 of 3 windows?** 0/3 windows clear → **does not fire.**
  Per-window: W1 fails (both sub-conditions), W2 fails (both sub-conditions, HIGHER narrowly),
  W3 fails (LOWER sub-condition only; HIGHER clears).
- **Direction-stability (same sign at all three windows, no sign-flip anywhere)?**
  `HIGHER_CLEARS_LOWER_DOES_NOT` at W1, W2, and W3 — **stable, no sign-flip.**
- These two raw facts are reported as-is per task scope; §6 of the brief's own gate table
  (Accept requires date-correlation ≥2/3 **AND** direction-stable; Reject requires date-correlation
  fails ≥2/3 **OR** any sign-flip) is a mechanical determination reserved for Phase 3, not made here.

---

## (4) Sparsity

No window is sparse under the pre-registered n<30-trades floor. Smallest bucket across all three
windows is W3's LOWER bucket at 530 trades (543 days) — nearly 18× the sparsity floor. The
Ambiguous-hold clause's trade-sparsity condition does **not** fire at any window; no fallback to
the secondary (cost-to-range) classifier is triggered by sparsity.

---

## (5) Script + rerun

- Script: `lab/analysis/c1/q_orbcush_1_2026-08/run_meanr_regime_gate.py`
- Raw JSON: `lab/analysis/c1/q_orbcush_1_2026-08/results_meanr_regime_gate.json`
- Imports unchanged (not retyped): `run_evalseq_orb_intraday.py`'s `day_loop_intraday`,
  `build_paths_orb`, `run_policy_orb`, `pol_cushion`, `pol_const`, `blocks_from_panel`,
  `build_k_panel`, `orb_days_with_excursion`, `resolve_panel`, `make_inst`,
  `assert_mirror_matches_engine`, `load_scoring_thresholds`, `firm_kwargs`, `assert_engine_ready`
  (from `lab/analysis/c1/orbmnq1_cushion_sizing_probe_2026-08-20/`); `stage2_regime_gate.py`'s
  `build_regime_blocks`/`contiguous_runs` (same directory).
- Runtime: ~94s wall-clock end-to-end (data load + Control B ~29s, fidelity control ~26s,
  3 windows × 2 buckets × 2 policies ~6s/call ≈ 72s).

```bash
python lab/analysis/c1/q_orbcush_1_2026-08/run_meanr_regime_gate.py
```

No repo-tracked file was modified. All output is confined to this directory (the brief's own
execution home) plus stdout.
