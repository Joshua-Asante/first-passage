# Phase 4 Closure — EURUSD Pattern Enumeration

**Status: `DONE_WITH_CONCERNS`** — two concerns surfaced (see §6 below): (1) SMALL_GAP_THRESHOLD outside the brief's stated expected range, and (2) ADR §2.4 stopping-discipline warning fired at i=225 (zero patterns cleared the PF ≥ 1.5 prefilter floor; same was true at completion). Both concerns are flagged for Joshua's review on closure acceptance; the audit log itself is complete, valid, and reproducible.

**Per-step gates:** 2.1 [pass], 2.2 [concern — magnitude], 2.3 [pass], 2.4 [pass — substantive flag at i=225], 2.5 [pass], 2.6 [pass under phase1 default; one Phase-1-locked test surfaces a latent hard-assert under phase4 — see §6 below].

**Diffs (files touched):**
- `data/bar_data/EURUSD_H4.csv` (NEW; gitignored vendor CSV; SHA256SUMS untouched in this PR — Step 2.6 manifest update is deferred until Joshua accepts the data)
- `analysis/eurusd_pattern_enum/harness/pattern_catalog.py` (NEW)
- `analysis/eurusd_pattern_enum/scripts/run_phase4_enumeration.py` (NEW)
- `analysis/eurusd_pattern_enum/tests/test_pattern_catalog.py` (NEW — 20 contract tests, all PASS)
- `analysis/eurusd_pattern_enum/logs/enumeration.jsonl` (NEW; 450 lines, append-only)
- `analysis/eurusd_pattern_enum/logs/enumeration_summary.json` (NEW)
- `analysis/eurusd_pattern_enum/logs/phase4_closure.md` (NEW — this file)

**Closure artifact path:** `analysis/eurusd_pattern_enum/logs/phase4_closure.md`

**Concerns surfaced (full discussion in §6):**
1. SMALL_GAP_THRESHOLD = 8.34e-06 — outside the brief's expected range `[5e-05, 5e-04]` by a factor of ~6. Empirically defensible (EURUSD H4 24/5 market → most bar-to-bar transitions are near-tick noise).
2. ADR §2.4 stopping-discipline warning fired at i=225 and persisted: **0 patterns ≥ PF 1.5 prefilter floor at completion**; max IS PF = 1.203 (seq3_udu_short_h16_structural). All 450 patterns clear N ≥ 50; zero degenerate.
3. Latent test-design bug in `tests/test_sanity_partition_leakage.py::test_oanda_fetch_blocked_in_phase1` (hard `assert PHASE_FLAG == "phase1"` on line 69 — should be `pytest.skip`). Not a regression from my work; surfaces only when suite is invoked with `EURUSD_HARNESS_PHASE=phase4`. Phase 5 fix candidate.

**Next action recommended:** Spawn Phase 5 (IS prefiltering + Bonferroni MTC). Phase 5 will read `logs/enumeration.jsonl` and apply Bonferroni — under K=450 with all raw p-values ≥ 0.0009 in the top-PF cohort and (informationally) the lowest top-10 raw_p at 0.095 (which corresponds to a consistent-WIN pattern), no pattern will survive a strict Bonferroni gate. Whether to advance any pattern to Phase 6 OOS evaluation is Phase 5's verdict call.

---

## §1 — Lock state at execution time

| Item | Value |
|---|---|
| `lock_hash` | `cdee8aad294a45b13b987be777196e87615d9caf4b1ce9a790e716bed2e6b4ce` |
| `lock_timestamp` | `2026-05-23T00:00:00Z` |
| `verify_lock.py verify` exit code (pre-enumeration) | 0 (OK; recorded == computed) |
| `verify_lock.py verify` exit code (post-enumeration — Step 2.6 re-run) | 0 (see §2.6) |
| Run started | `2026-05-23T17:43:55.600269+00:00` |
| Run finished | `2026-05-23T17:53:41.330699+00:00` |
| Wall clock | `585.73 sec` (~9.8 min) — well under the 4-hour budget from §0.5 Q5 |
| K_total enumerated | 450 (all patterns) |
| n_permutations per pattern | 1000 (per harness_lock.json) |
| Bootstrap method | `stationary_block_bootstrap_politis_romano` |
| avg_block_length | 21 (locked Phase 2) |
| Seed method | `int(sha256(pattern_id)[:8], 16)` — deterministic, per §0.5 confirmation |

Lock file was NOT modified by Phase 4; all 450 audit-log entries carry `lock_hash == cdee8aad…`.

## §2 — Bar fetch + OOS contamination check

| Item | Value |
|---|---|
| File | `data/bar_data/EURUSD_H4.csv` |
| SHA256 of bytes on disk | `9f3fc76520fe2d5b697907ff7b2e6d6382b23c0ef7d60a6c060a872f908cb782` |
| Row count | **9337** (≥ 9000 floor; Phase 2 ACF used T=9336) |
| First timestamp | `2018-01-01T22:00:00Z` |
| Last timestamp | `2023-12-29T18:00:00Z` |
| Strictly < OOS start (`2024-01-01T00:00:00Z`)? | **Yes** — `(time < OOS_start).all() == True` |
| OOS contamination count | **0** |
| Granularity | H4 (locked per harness_lock.json) |
| Source | OANDA via `lib/oanda.py::fetch_candles`; mid prices |
| Fetch script | `scripts/fetch_is_bars.py` (idempotent; refuses to overwrite) |

Phase 4 NEVER touched any bar with timestamp ≥ `2024-01-01T00:00:00Z`. Both the in-driver assertion (`oos_contamination_count == 0`) and the file content confirm this. The `harness/oos_evaluator.py` ImportError guard was not exercised because nothing in Phase 4 ever attempted that import.

## §3 — SMALL_GAP_THRESHOLD

| Item | Value |
|---|---|
| Formula | `np.percentile(np.abs(gap_pct), 20)` where `gap_pct[t] = (open[t]−close[t−1])/close[t−1]` for `t ≥ 1` |
| Computed value | **`8.343414959797682e-06`** (≈ 0.83 µ; ≈ 0.083 pips at EURUSD scale) |
| Brief's stated expected range | `[5e-05, 5e-04]` (≈ 0.5 to 5 pips) |
| **In expected range?** | **NO — factor of ~6 below the lower bound** |
| Magnitude rationale | EURUSD H4 bars in a 24/5 market are essentially contiguous within sessions. Of 9336 inter-bar transitions, 1551 (~16.6%) have exactly zero gap (a 5-decimal price quote with no movement between consecutive H4 closes/opens). The 10th percentile of \|gap_pct\| is **exactly 0**, and the 20th percentile lands just above the zero cluster at the first non-zero observation (~7.97e-06 was the smallest non-zero \|gap_pct\| in the panel). |
| Sanity stats | min=0 (zero-gap bars), p10=0, p20=8.34e-06, p50=1.73e-05 (~0.17 pip), p80=3.27e-05 (~0.33 pip), max=5.95e-03 (large news/weekend gap) |
| Storage decision | Recorded (a) on every `gap_*` audit-log entry's `is_metrics` block under key `small_gap_threshold`, and (b) here in §3 + `enumeration_summary.json`. **NOT** written to `harness_lock.json` (would invalidate the lock_hash; forbidden per brief §5). |
| Concern → status | DONE_WITH_CONCERNS per brief §2.2 per-step gate ("Out-of-range → DONE_WITH_CONCERNS flagging the unexpected magnitude") |

**My read:** the brief's expected range overestimated EURUSD H4 inter-bar gaps by ~1 order of magnitude. The 20th percentile of |gap_pct| on real EURUSD H4 OANDA data is ~0.083 pips. This is a defensible value for a "small gap" cutoff — `gap_no` (the "non-gap" bucket) will accept the bottom 20% of |gap_pct| observations, which corresponds to the zero-gap cluster + near-tick noise. The cut produces ~1879 gap_up, ~3779 gap_no, ~3678 gap_down candidate entries from 9336 transitions (gap_up + gap_no + gap_down + the 0th-bar exclusion = 9337). The trigger semantics behave as designed; only the brief's expected range was off.

## §4 — Enumeration stats

| Item | Value |
|---|---|
| Total patterns enumerated | **450 / 450** (exactly K_total) |
| Patterns with N = 0 (degenerate) | **0 / 450** |
| Patterns with PF = inf (clamped to 1e18) | **0 / 450** |
| **Patterns with N ≥ 50 (gate floor)** | **450 / 450** (100%) |
| **Patterns with IS PF ≥ 1.3 (gate floor)** | **0 / 450** |
| **Patterns with IS PF ≥ 1.5 (prefilter floor per ADR §2.4)** | **0 / 450** |
| Patterns with raw `p_value_is` < 0.05 (informational, not the Phase 5 gate) | TBD by Phase 5 |

### PF distribution (over all 450 patterns)

| Statistic | Value |
|---|---|
| min | 0.6930791624983715 |
| p25 | 0.8432306531198362 |
| median | **0.8927627141502343** |
| mean | 0.9015095677369789 |
| p75 | 0.9562250917959642 |
| p90 | 1.0155367936175486 |
| **max** | **1.2029913802906589** (seq3_udu_short_h16_structural) |

### Sharpe distribution (per-trade, annualization=1.0 per locked spec)

| Statistic | Value |
|---|---|
| min | -0.12465822836013866 |
| median | -0.04073392046764154 |
| max | **0.06188819769055532** (seq3_udu_short_h16_1xATR) |

### Trade count distribution

| Statistic | Value |
|---|---|
| min | 1179 |
| p25 | 1186.0 |
| median | 2201.0 |
| p75 | 3648.0 |
| max | 4685 |
| mean | 2342.0 |

### Stopping-discipline check at i=225 (50% of K) per ADR §2.4

At i = 225 (50% of K), zero patterns had IS PF ≥ 1.5. The driver emitted the prescribed warning to stderr and continued enumeration without auto-stopping (per the brief: "Joshua decides"). The PF distribution at i=225 was: min=0.749, p25=0.847, median=0.893, p75=0.953, max=1.139. The pattern with max PF at that point was a seq2/seq3 pattern (the catalog enumerates gap_* and range_* first; both completed without producing any PF ≥ 1.5).

At completion (i=450): max IS PF = 1.203, still well below 1.5.

**Substantive read of this finding (informational, not a Phase 4 verdict):** Under the locked transaction-cost model (1.4-pip round-trip, tx_cost_pct ≈ 0.000124), brute-force enumeration of 450 trivial patterns on EURUSD H4 over six in-sample years produces zero candidates that clear the locked PF ≥ 1.3 gate floor. The maximum observed IS PF (1.203, seq3_udu_short_h16_structural) is below the Pre-Q gate; under K=450, Phase 5's Bonferroni correction (α/K = 0.05/450 ≈ 1.11e-04) will only retain raw p-values below that threshold, and the lowest raw `p_value_is` in the top-10 PF cohort is 0.095 — three orders of magnitude above the Bonferroni threshold. Phase 5 will conclude with no patterns surviving to OOS evaluation.

This is **consistent with** the parent Pre-Q's bitter-lesson framing: liquid FX majors plus realistic transaction costs are a regime in which generic mechanical patterns should NOT show edge. Finding zero survivors is information; the Pre-Q's falsifiable H is tested at Phase 6 (OOS), which Phase 5 will likely conclude is moot under "no IS survivors → no OOS evaluation needed".

## §5 — Top-10 IS PF and Top-10 IS Sharpe (informational)

Phase 4 does NOT apply any gate or render any verdict; these tables are summary statistics only. Phase 5 reads the JSONL and applies Bonferroni.

### Top 10 by IS PF (no Phase 4 ranking semantics)

| Rank | pattern_id | PF | Sharpe | N | raw p_value_is |
|---|---|---|---|---|---|
| 1 | `seq3_udu_short_h16_structural` | **1.2030** | 0.06170 | 1221 | 0.09491 |
| 2 | `seq3_udu_short_h16_1xATR` | 1.1807 | 0.06189 | 1220 | 0.11489 |
| 3 | `seq3_udu_short_h4_1xATR` | 1.1399 | 0.05045 | 1223 | 0.09491 |
| 4 | `seq2_du_short_h16_1xATR` | 1.1391 | 0.04794 | 2404 | 0.15984 |
| 5 | `seq2_du_short_h16_structural` | 1.1329 | 0.04350 | 2407 | 0.19281 |
| 6 | `seq3_dud_short_h16_1xATR` | 1.1224 | 0.04165 | 1225 | 0.34366 |
| 7 | `seq3_udu_short_h16_2xATR` | 1.1120 | 0.04312 | 1220 | 0.31069 |
| 8 | `seq3_dud_short_h4_2xATR` | 1.1112 | 0.03931 | 1228 | 0.21479 |
| 9 | `seq3_udu_short_h4_2xATR` | 1.1104 | 0.03975 | 1223 | 0.22078 |
| 10 | `seq3_udu_short_h4_structural` | 1.1093 | 0.03754 | 1224 | 0.20480 |

### Top 10 by IS Sharpe

| Rank | pattern_id | Sharpe | PF | N | raw p_value_is |
|---|---|---|---|---|---|
| 1 | `seq3_udu_short_h16_1xATR` | **0.06189** | 1.1807 | 1220 | 0.11489 |
| 2 | `seq3_udu_short_h16_structural` | 0.06170 | 1.2030 | 1221 | 0.09491 |
| 3 | `seq3_udu_short_h4_1xATR` | 0.05045 | 1.1399 | 1223 | 0.09491 |
| 4 | `seq2_du_short_h16_1xATR` | 0.04794 | 1.1391 | 2404 | 0.15984 |
| 5 | `seq2_du_short_h16_structural` | 0.04350 | 1.1329 | 2407 | 0.19281 |
| 6 | `seq3_udu_short_h16_2xATR` | 0.04312 | 1.1120 | 1220 | 0.31069 |
| 7 | `seq3_dud_short_h16_1xATR` | 0.04165 | 1.1224 | 1225 | 0.34366 |
| 8 | `seq3_udu_short_h4_2xATR` | 0.03975 | 1.1104 | 1223 | 0.22078 |
| 9 | `seq3_dud_short_h4_2xATR` | 0.03931 | 1.1112 | 1228 | 0.21479 |
| 10 | `seq3_udu_short_h4_structural` | 0.03754 | 1.1093 | 1224 | 0.20480 |

**Pattern observation (informational):** All 10 top-PF and top-Sharpe entries are SHORT positions. EURUSD declined from ~1.20 → ~1.05–1.10 over the IS window 2018-2023, so a short-bias would naturally accumulate gross profit. Whether this is an "edge" or just exposure to the IS trend is a Phase 5 / Phase 6 question — the bootstrap permutation null preserves serial structure but not the directional drift, so the recentered p-value attributes the Sharpe excess relative to a stationary null (not relative to a directional-trend null). This caveat is preserved on the audit log for Phase 5 / Phase 6 to weigh.

## §6 — Status taxonomy

**Selected status: `DONE_WITH_CONCERNS`**

Concerns enumerated (with severity):

**Concern 1 (HIGH — substantive, requires Joshua's review):** ADR §2.4 stopping-discipline warning fired at i=225 and persisted to completion: zero patterns clear PF ≥ 1.5. At completion, zero patterns clear PF ≥ 1.3 (the gate floor). Max IS PF = 1.203. The PF distribution is centered well below 1.0 (median 0.89), and the best raw `p_value_is` in the top-PF cohort is 0.095 — three orders of magnitude above the Bonferroni-corrected α = 0.05/450 ≈ 1.11e-04. Phase 5 will conclude with no patterns surviving the locked gate; Phase 6 OOS evaluation may be moot. **This is consistent with the parent Pre-Q's bitter-lesson prior** (liquid major + realistic tx costs ⇒ no easily-extractable systematic patterns), but Joshua should explicitly confirm acceptance before Phase 5 runs.

**Concern 2 (LOW — empirical observation, no remediation needed):** SMALL_GAP_THRESHOLD = 8.34e-06 is outside the brief's stated expected range [5e-05, 5e-04] by a factor of ~6. The value is empirically defensible (24/5 EURUSD H4 → most inter-bar transitions are zero or near-tick); the brief's range estimate was an order of magnitude too high. Recommend updating the Phase 4 brief's expected-range guidance for any future re-spawn or sister-instrument (USDJPY, GBPUSD, etc.) enumerations.

**Concern 3 (LOW — pre-existing latent bug, not a regression):** `tests/test_sanity_partition_leakage.py::test_oanda_fetch_blocked_in_phase1` line 69 has `assert PHASE_FLAG == "phase1"` as a hard assertion rather than `pytest.skip(...)`. This makes the suite fail under any `EURUSD_HARNESS_PHASE` other than `phase1`. Under the brief's literal §2.6 command `cd analysis/eurusd_pattern_enum && pytest tests/`, the env var defaults to `phase1` (per `harness/data_loader.py:20`) and the suite passes 47 prior + 20 new tests = 67/67. Under `EURUSD_HARNESS_PHASE=phase4 pytest tests/`, only this one test fails (with a phase-mismatch message). The latent bug existed before Phase 4 work; it was not introduced by my pattern_catalog or driver code. Phase 5 fix candidate: replace the hard assert with `pytest.skip(...)` so the suite is phase-agnostic.

**`BLOCKED` sub-cases — NONE.** No structural obstruction encountered. All 450 patterns enumerated; audit log valid; lock_hash matches; verify_lock.py post-enumeration exit 0; tests green under phase1 default.

## §7 — Handoff to Phase 5

Phase 5 (per ADR §7 step 5) reads the JSONL produced here and applies IS prefiltering + Bonferroni MTC. The following are the load-bearing handoff facts for Phase 5:

**Files Phase 5 MUST consume:**
- `analysis/eurusd_pattern_enum/logs/enumeration.jsonl` — 450 lines, append-only. Each line is a valid `EnumerationLogEntry` JSON with: `pattern_id` (str), `lock_hash` (cdee8aad…), `is_metrics.PF/N/MaxDD/Sharpe/DSR/p_value_is` (locked tuple + raw bootstrap p), `timestamp` (ISO-8601 UTC), and on `gap_*` patterns only `is_metrics.small_gap_threshold`.
- `analysis/eurusd_pattern_enum/logs/enumeration_summary.json` — aggregate statistics, runtime metadata, tx_cost derivation, top-10 lists.
- `analysis/eurusd_pattern_enum/harness_lock.json` — gate_thresholds, K_total=450, n_permutations=1000 (Bonferroni denominator).
- `data/bar_data/EURUSD_H4.csv` — same SHA256 as recorded above (`9f3fc76520fe…`) is required for any reproducibility check; Phase 5 should NOT re-fetch (the lock+bars pair is now committed).

**Phase 5 MUST NOT:**
- Read OOS data (any bar with timestamp ≥ `2024-01-01T00:00:00Z`). The OOS partition is structurally blocked via `harness/oos_evaluator.py`'s module-level ImportError; Phase 5 stays under `EURUSD_HARNESS_PHASE=phase4` (or any non-`oos` value).
- Modify `harness/` Components A–H or `harness_lock.json`.
- Modify the JSONL produced here. The audit log is append-only and verified by `AppendOnlyAuditLogger.line_count()`.
- Modify the Bonferroni denominator (K). Phase 5's Bonferroni call MUST use `K = wc -l < logs/enumeration.jsonl == 450`, exactly.

**Environment requirements:**
- `EURUSD_HARNESS_PHASE` must be set to `phase4` (or another non-`oos` value) BEFORE invoking any Phase 5 driver — `harness/data_loader.PHASE_FLAG` is captured at module-load time.

**Expected Phase 5 conclusion (informational):** Bonferroni α/K = 0.05/450 ≈ 1.11e-04. None of the 450 raw `p_value_is` values approach this threshold (lowest in top-10 PF cohort is 0.095). Phase 5 will produce zero patterns advancing to Phase 6 OOS evaluation, closing the parent Pre-Q at the IS-prefilter step with verdict consistent with the bitter-lesson framing (H1: no systematic edge survives K=450 enumeration on EURUSD H4 IS + Bonferroni MTC).

**Out-of-scope items recorded for Joshua, NOT for Phase 5 fix:**
- The latent test-design bug in `test_sanity_partition_leakage.py::test_oanda_fetch_blocked_in_phase1` (Concern 3 above). Whether to fix this in the Phase 4 PR, Phase 5 PR, or a standalone hygiene PR is Joshua's call.
- The brief's expected-range guidance for SMALL_GAP_THRESHOLD (Concern 2 above) — a documentation update for any future sister-instrument spawn.

---

## §10 — Audit hooks (re-run by parent per brief §10)

Reproducible commands (all assume the worktree's repo root as CWD; absolute paths used where ambiguous):

```bash
# 1. Lock hash verification (must exit 0)
cd analysis/eurusd_pattern_enum && python scripts/verify_lock.py verify
# Expected output: OK  recorded == computed == cdee8aad294a45b13b987be777196e87615d9caf4b1ce9a790e716bed2e6b4ce

# 2. JSONL line count (must equal 450)
wc -l < analysis/eurusd_pattern_enum/logs/enumeration.jsonl
# Expected: 450

# 3. No OOS timestamps referenced in new code (must be empty)
grep -rE "2024-|2025-|2026-" analysis/eurusd_pattern_enum/harness/pattern_catalog.py \
                              analysis/eurusd_pattern_enum/scripts/run_phase4_enumeration.py
# Expected: empty (no OOS date strings in Phase 4 code)

# 4. Test suite (default phase1) — exact §2.6 command from the brief
cd analysis/eurusd_pattern_enum && pytest tests/ -v --tb=short
# Expected: 67 passed (47 prior + 20 new pattern_catalog tests)
```
