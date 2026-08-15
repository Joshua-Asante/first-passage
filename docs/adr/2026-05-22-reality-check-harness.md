# ADR — Reality-Check Harness for EURUSD Pattern Enumeration

**Status:** Accepted - LOCKED 2026-05-22 — companion to Pre-Q EURUSD Pattern Enumeration; five open decisions baked 2026-05-21; Component E stationary-input + Davison-Hinkley sub-contracts added post-Phase-1; `block_length` → `avg_block_length` field rename 2026-05-22. **AMENDED 2026-08-14:** Component A (OANDA data loader) is **dormant**; Components B–H methodology remains live (Addendum 2026-08-14). This ADR as a whole is **not** dormant.
**Decision date:** 2026-05-22
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Type:** Architectural Decision Record (technical contract)
**Scope:** binds harness behavior for this Pre-Q; reusable if framework graduates
**Date authored:** 2026-05-21
**Decisions baked:** 2026-05-21 (Q-H1 through Q-H5; see §5)
**Author:** claude.ai (Tech Advisor); implementation by CC after Pre-Q RESOLVED

---

## §0 — Rule 0 production reads

| Path | Anchor | Why read |
|---|---|---|
| `lib/regime_bootstrap.py` | last commit `31110f5`, 2026-05-13 | **Calendar-month-fixed-block bootstrap on daily P&L** — NOT Politis-Romano stationary block bootstrap. Wrong shape (daily not bar-level; fixed not random block length). Component E (§2.3 below) requires NEW implementation; this utility is NOT modified per §3.7 forbidden move (no i.i.d. resampling) and per the broader scope-discipline rule. |
| `portfolio_mc.py` | last commit `43aa187`, 2026-05-16 | Challenge-outcome MC. Uses week-block bootstrap on daily P&L. NOT a reusable surface for bar-level pattern permutation. Reading it here so the harness scope is unambiguous: the new Component E is independent of this module. |
| `lib/oanda.py` + `scripts/fetch_oanda_bars.py` + `analysis/oanda_stage1/bar_loader.py` | commits `0f72836` / `d34b50b` / `a8b97a9` | OANDA data-loader surface (§2.3 Component A). `fetch_candles` is directly reusable for EUR_USD H4 behind a phase-flag import guard. |
| `tests/conftest.py` + `pyproject.toml` | b1d2a10 / current | Test conventions, pytest config, Python ≥3.11 confirmed, Pydantic v2 already in deps. |
| Per-codebase Repo Context | `docs/notion/repo_context.md`, refreshed 2026-05-08 | Architecture-truth surface. Initial draft of this §0 listed `multi_firm_operations/data/oanda_pipeline.py` + `multi_firm_operations/mc/portfolio_monte_carlo.py` — both non-existent in the flat py-modules layout. Corrected 2026-05-22 against Repo Context + CC Phase 0 reads. |

§0 paths verified against repo HEAD on 2026-05-22 via CC Phase 0 reads. Substantive finding — the existing `regime_bootstrap.py` is calendar-month-block on daily P&L, not Politis-Romano on bars — is recorded here so §2.3 Component E is unambiguously a new-implementation decision, not a reuse decision deferred to CC.

---

## §1 — Context

The Pre-Q gates whether mechanical pattern enumeration on EURUSD produces edge. The harness IS the gate — it is the artifact that distinguishes "found edge" from "ran K experiments and got K-times-5% false positives." If the harness is broken, the Pre-Q has no evidentiary weight regardless of what the enumeration outputs.

This ADR codifies harness behavior **before** any enumeration runs, so the gate's properties cannot drift based on what results emerge. This is the methodological equivalent of pre-registering a study.

---

## §2 — Decision

The harness ships with the following pre-committed properties. Each is binding; changing any after enumeration begins reopens the Pre-Q.

### 2.1 Data partition

| Window | Boundary | Purpose | Access rule |
|---|---|---|---|
| **In-Sample (IS)** | 2018-01-01 → 2023-12-31 | Pattern enumeration + in-sample metric calculation | Free read during enumeration |
| **Out-of-Sample (OOS)** | 2024-01-01 → data fetch date | Gate evaluation only | **Locked file, write-protected, hash-checked at session start** |

OOS data is loaded once, hashed (SHA-256), and the hash written to a manifest. Every evaluation session re-verifies the hash; mismatch halts the harness with a leakage-suspicion error.

**No "validation set."** Two-way splits only. Three-way splits create the temptation to peek at OOS, justify it as "validation," and corrupt the gate. If hyperparameters need tuning, that's done via cross-validation *within* IS, never against OOS.

### 2.2 Pre-commitment registry

Before enumeration begins, a `harness_lock.json` file is committed to the repo containing:

```json
{
  "instrument": "EURUSD",
  "timeframe": "4H",
  "feature_space": "<formal enumeration of all features in scope; populated at Phase 3 lock>",
  "K_total_bound": [50, 500],
  "K_total": "<integer in K_total_bound, populated at Phase 3 lock>",
  "evaluation_metrics": ["PF", "N", "MaxDD", "Sharpe", "DSR"],
  "gate_thresholds": {"PF_min": 1.3, "N_min": 50, "DD_ratio_max": 1.5, "p_max": 0.05},
  "multiple_testing_method": "bonferroni",
  "sanity_metrics": ["DSR"],
  "bootstrap_method": "stationary_block_bootstrap_politis_romano",
  "avg_block_length": "<integer, populated at Phase 2 from IS ACF analysis. Politis-Romano parameterizes by AVERAGE block length (mean of the geometric distribution from which per-resample block lengths are drawn). Field was named `block_length` in pre-Phase-1 drafts; renamed for accuracy post-Phase-1.>",
  "n_permutations": 1000,
  "tx_cost_model": {
    "spread_pips": 1.0,
    "slippage_pips_per_side": 0.2,
    "commission_per_side_usd": 0.0
  },
  "position_sizing": {
    "method": "fixed_fractional",
    "fraction_per_trade": 0.01
  },
  "lock_hash": "<SHA-256 of this file at commit; populated at Phase 3>",
  "lock_timestamp": "<ISO-8601; populated at Phase 3>"
}
```

**SSOT rule:** the lock file is the source of truth. The prose example above is illustrative; if they diverge after Phase 3, the lock file wins and this ADR is updated to match.

**Three fields populated in stages, not at ADR-author time:**
- `feature_space` and `K_total` — populated when the pattern definition registry (Component B) is finalized, before Phase 3 lock commit.
- `avg_block_length` — populated in Phase 2 from ACF/PACF analysis of IS log returns. Justification appended to the lock file as a sibling document `avg_block_length_justification.md`. (Renamed from `block_length` post-Phase-1 for accuracy — Politis-Romano parameterizes by average block length, not a fixed integer.)

Any modification to this file post-lock invalidates the enumeration. The CI hook below enforces it.

### 2.3 Components and their contracts

> ⚠ **2026-08-14:** Component A is **dormant** (OANDA retired; no replacement loader specified). This ADR as a whole is **not** dormant — Components B–H remain live methodology. See Addendum 2026-08-14.

**Component A: Data Loader**
- Input: date range, instrument (EURUSD), timeframe (4H, per lock file)
- Output: OHLCV bars from OANDA
- Contract: deterministic for a given (date_range, instrument, timeframe) tuple. Same call returns byte-identical output.
- Test: fixture-based; small known date range → known SHA-256 of output frame.
- Note: 4H is the locked timeframe for this Pre-Q. 1H and 1D become separate Pre-Qs if this one closes FALSIFIED with budget remaining (per §5 decision Q-H3).

**Component B: Pattern Definition Registry**
- Input: pattern_id (string)
- Output: a callable `pattern_fn(bars) → trade_list` where trade_list is `[(entry_idx, exit_idx, direction), ...]`
- Contract: every pattern_id in the enumeration is registered before search begins. Registry is append-only during enumeration (additions allowed only via lock-amendment, which invalidates prior work).

**Component C: Pattern Executor**
- Input: pattern_fn, bars, tx_cost_model
- Output: equity_curve, trade_list, raw_metrics
- Contract: pure function. No global state. No randomness unless seed-injected.

**Component D: Metric Computer**
- Input: equity_curve, trade_list
- Output: dict of {PF, N, MaxDD, Sharpe, DSR, ...}
- Contract: matches the locked `evaluation_metrics` list exactly. Adding a metric post-lock is a §5 violation.

**Component E: Permutation Generator (block bootstrap)**
- Input: a **stationary input series** (typically log returns; see sub-contract below), `avg_block_length`, `n_permutations`, seed
- Output: n_permutations of resampled series preserving block-level serial dependence
- Contract: stationary block bootstrap (Politis-Romano), NOT i.i.d. resampling. Block length is locked in `harness_lock.json` (`avg_block_length`) and justified by ACF/PACF analysis of IS log returns at the relevant timeframe.

**Sub-contract — stationary-input requirement** (added post-Phase-1 surface):
The Politis-Romano bootstrap is defined for stationary series. EUR_USD bar **closes** are non-stationary (unit-root random walk); block-bootstrapping closes directly produces cross-block price-level discontinuities that the downstream "implied return" computation interprets as outsized per-bar moves, inflating the null distribution and biasing p-values. The bootstrap is invoked on the **log-return series** of the bars, and the resampled bars are reconstructed by cumulative sum + exponentiation. Phase 1 surfaced this via Test 1 clustering p ≈ 0.93 under price-bootstrap; switching to return-bootstrap restored uniform-under-H0 behavior. The `bootstrap_resample_bars` helper in `tests/conftest.py` encodes the correct invocation; production Phase 4 enumeration uses the same helper or its equivalent.

**Sub-contract — p-value formulation** (Davison-Hinkley centering, added post-Phase-1 surface):
Bootstrap distributions are centered on the *observed* statistic (CLT), not on the null mean. To obtain p-values that are uniform on [0,1] under H0, the bootstrap is **recentered** before comparison: `null_centered = null - mean(null)`, then `p = (1 + sum(|null_centered| ≥ |observed|)) / (1 + n_permutations)` (two-sided) or the one-sided analogue. Phase 1 Test 1 surfaced this; the uncentered formulation gives p ≈ 0.5 clustered (not uniform), invalidating the sanity check. Production Phase 4-5 code uses the centered formulation.

**Component F: Multiple-Testing Corrector**
- Input: K p-values from the K-pattern enumeration
- Output: corrected p-values OR rejection decisions
- Contract: method (Bonferroni / Romano-Wolf / DSR) is locked; only the locked method's output is consulted for the gate.

**Component G: OOS Evaluator**
- Input: a pattern_fn that survived IS prefiltering AND IS MTC; the OOS bars
- Output: OOS metrics dict + p-value from OOS-only permutation test
- Contract: this component reads the OOS data file. It is the **only** component that does. All other components import from a module that raises ImportError if OOS dates are accessed during IS-phase code paths.

**Component H: Audit Logger**
- Every pattern enumeration writes one line to `logs/enumeration.jsonl`:
  ```
  {"pattern_id": "...", "lock_hash": "...", "is_metrics": {...}, "timestamp": "..."}
  ```
- This file is append-only; CI rejects PRs that modify or delete past lines.
- The Bonferroni / RW denominator must equal `wc -l < logs/enumeration.jsonl`. Mismatch halts the harness.

### 2.4 Stopping discipline (in harness, not just doctrine)

Beyond §9 of the Pre-Q (training-day session budget), the harness enforces:
- After every N=50 patterns enumerated, the harness prints in-sample PF distribution stats. If after 50% of K enumerated, **zero** patterns have IS PF ≥ 1.5, the harness emits a warning that triggers human early-stop review.
- The harness will not auto-stop (Joshua decides), but it surfaces the prior update visibly.

### 2.5 Sanity tests (must pass before any EURUSD data touches the harness)

These are blocking fixture tests. The Pre-Q gate is void unless these are green:

**Test 1 — Null series, single pattern:** synthetic random-walk series, single non-edge pattern. Permutation p-value must be uniformly distributed across multiple seed runs (sanity-check: the test isn't generating false positives at the null).

**Test 2 — Null series, K=1000 patterns:** synthetic random-walk series, K=1000 random patterns. After Bonferroni correction, expect 0 patterns to pass at p<0.05 in expectation; tolerance threshold: 0–2 false positives across 10 seed runs. If consistently >2, the corrector is broken.

**Test 3 — Known-edge synthetic series:** synthetic series with a hand-injected edge (e.g., consistent post-gap mean reversion of known magnitude). The harness must detect it; if it doesn't, the harness is under-powered and the FALSIFIED verdict is uninformative.

**Test 4 — Data partition leakage:** attempt to access OOS dates from within IS-phase code; harness must raise ImportError, not silently allow it.

**Test 5 — Append-only log:** attempt to delete or modify a past line in `enumeration.jsonl`; CI hook must reject.

---

## §3 — Forbidden moves

1. **Adding a third "validation" split** between IS and OOS. Two splits only.
2. **Re-running the harness with a different RNG seed after seeing OOS results** to "stress-test." Seeds are locked in the lock file.
3. **Skipping a sanity test because "it's slow."** All five tests gate every harness-run session, not just the first.
4. **Hand-tuning block length** mid-enumeration. Block length is set from IS ACF analysis ONCE, before search.
5. **Selecting which metric to gate on after seeing results.** Gate is defined in `harness_lock.json` (§2.2).
6. **Computing DSR / Sharpe ratios without verifying the higher-moments correction.** The Bailey-López de Prado formula must be unit-tested against their published worked examples.
7. **Using a non-block bootstrap "because the series looks i.i.d."** EURUSD returns are not i.i.d. Permutation must preserve serial structure or the p-values are wrong.

---

## §4 — Audit hooks

1. **Lock-file integrity:** `sha256sum harness_lock.json` must match the value recorded in §2.2 at lock time. Drift = harness is unlocked, gate is void.
2. **CI hook for append-only:** `git diff` on `enumeration.jsonl` must show only additions; CI rejects diffs with deletions or modifications.
3. **OOS access audit:** `grep -r "load_oos\|2024-01-01\|2024-12-31\|2025-\|2026-" eurusd-research/ --include="*.py" | grep -v "oos_evaluator.py"` must return zero matches. Only the OOS evaluator may reference OOS dates.
4. **Fixture-test gate:** `pytest eurusd-research/tests/ -v --tb=short` must show 100% pass before any session that touches enumeration. Stale failing tests = harness condemned.
5. **Bonferroni denominator check:** every final report cites `K = $(wc -l < logs/enumeration.jsonl)` directly, not a remembered number.

---

## §5 — Decisions baked (with rationale preserved for audit)

The five open questions are closed as of 2026-05-21. Rationale is retained verbatim below so future audit can verify the choice was made on argument, not on intuition or convenience. **Changing any of these post-Phase-3-lock requires a new ADR**, not an inline edit.

**Q-H1: MTC method → BONFERRONI as gate; DSR as sanity-check metric alongside.**

*Rationale:* Bonferroni is simple, conservative, and easy to defend. Romano-Wolf is more powerful but adds bootstrap-of-bootstrap implementation complexity that doubles the surface area where the harness can be subtly wrong (and a subtly wrong harness invalidates the gate). DSR (Bailey-López de Prado) is designed for this domain but produces one number per backtest, not a per-pattern decision — useful as a corroborating signal, not as the gate itself.

*Diagnostic value of starting strict:* if zero patterns clear Bonferroni but several would have cleared RW, that's an informative AMBIGUOUS verdict (and motivates a separate Pre-Q on whether the regime warrants the more powerful test). If patterns clear Bonferroni, the result is robust to MTC-choice and we don't have to defend the choice post-hoc.

**Q-H2: Feature space → SMALL enumeration, K in [50, 500].**

*Rationale:* Bonferroni at K=500 with p=0.05 requires per-pattern p ≤ 0.0001 — defensible against challenge. Larger K makes the gate effectively unclearable and motivates switching MTC frame mid-investigation (trap #5).

*Feature space scope (binding for this Pre-Q):* gap classes (gap-up / gap-down / no-gap, quantile-bucketed by gap size) × range classes (current-bar range quantile vs trailing-N median) × short bar-sequence patterns (2–4 bar sequences of direction/range/close-position signs). Holding periods enumerated within {1, 2, 4, 8, 16} bars. Stop conventions enumerated within {1×ATR, 2×ATR, structural}. **Exact K populated at Phase 3** from cartesian-product count of the locked enumeration.

*Escalation rule (pre-committed):* if this Pre-Q closes FALSIFIED, do NOT auto-escalate to medium-K within the same thread. Open a fresh Pre-Q with explicit framing of "did the small-K null update our prior enough to justify a more expensive enumeration?" The null result IS informative; treating it as "not enough patterns tried" is the SNAG failure mode.

**Q-H3: Timeframe → 4H, single timeframe for this Pre-Q.**

*Rationale:* 4H balances bar count (~3500+ bars on IS, ~700+ on OOS — supports N≥50 trades per pattern at reasonable signal rates) against per-bar noise (1H is noisier; 1D produces too few OOS trades for the §4 N-floor). Single-timeframe-per-Pre-Q keeps K bounded and makes multi-timeframe "robustness" claims an explicit cross-test, not an embedded confound.

*If FALSIFIED with budget remaining:* 1H and 1D become separate Pre-Q candidates, each with their own lock file and K. They do NOT extend this Pre-Q.

**Q-H4: Transaction-cost model → 1.0 pip spread + 0.2 pip slippage per side; $0 commission.**

*Rationale:* OANDA retail EURUSD typical spread runs 0.6–1.0 pip; 1.0 pip is the conservative end and protects against backtest-vs-live spread drift. 0.2 pip slippage per side is a reasonable approximation for market-on-close fills in liquid hours; it does NOT model adverse-selection slippage during news events or illiquid Asian-session hours.

*Known weakness:* this model is constant-cost. Real EURUSD spread widens at Asian open and around scheduled releases. If a candidate pattern's edge concentrates in those windows, the constant-cost model overestimates its real-world edge. The follow-up Pre-Q (§12 of Pre-Q) includes a transaction-cost-stress phase precisely to surface this.

*Pending verification (non-blocking):* if a recent OANDA fills sample exists for EURUSD, compare modeled vs realized costs before Phase 3 lock and adjust if the modeled costs are materially lower than realized. If no sample exists, the model stands.

**Q-H5: Position sizing → fixed-fractional 1% of equity per trade.**

*Rationale:* sizing optimization is a separate problem from edge discovery. Letting sizing vary during enumeration adds a degree of freedom that inflates the in-sample search space invisibly. Fixed-fractional 1% is the standard "neutral" sizing — it isolates edge as the variable being measured.

*Interaction with §4 gate condition (c) DD-ratio:* MaxDD on OOS will be measured at the same 1% sizing as IS, so the DD-ratio comparison is apples-to-apples. If sizing optimization is pursued later, it happens in a separate Pre-Q after edge is established, not folded into edge discovery.

---

## §5b — Lock readiness summary

| Field | Status | Populated at |
|---|---|---|
| `instrument` | ✅ EURUSD | now |
| `timeframe` | ✅ 4H | now |
| `feature_space` | ⏳ scope defined; exact enumeration pending | Phase 3 |
| `K_total` | ⏳ bound [50, 500]; exact value pending | Phase 3 |
| `evaluation_metrics` | ✅ [PF, N, MaxDD, Sharpe, DSR] | now |
| `gate_thresholds` | ✅ {PF:1.3, N:50, DD_ratio:1.5, p:0.05} | now |
| `multiple_testing_method` | ✅ bonferroni | now |
| `sanity_metrics` | ✅ [DSR] | now |
| `bootstrap_method` | ✅ stationary_block_bootstrap | now |
| `avg_block_length` | ⏳ pending ACF analysis (renamed from `block_length` post-Phase-1) | Phase 2 |
| `n_permutations` | ✅ 1000 | now |
| `tx_cost_model` | ✅ {spread:1.0, slippage:0.2, commission:0} | now |
| `position_sizing` | ✅ {fixed_fractional, 0.01} | now |
| `lock_hash`, `lock_timestamp` | ⏳ commit-time | Phase 3 |

---

## §6 — Verification block

```
[ ] §2.2 lock file: all "now" fields concrete (no placeholders for instrument, timeframe, metrics, gate, MTC, bootstrap, n_permutations, tx_cost, sizing)
[ ] §2.2 lock file: Phase-2 and Phase-3 fields explicitly marked pending (no silent TBDs)
[ ] §2.3 components A–H each have an explicit contract
[ ] §2.5 sanity tests are runnable and gate harness sessions
[ ] §3 forbidden moves are genuinely tempting (not strawmen)
[ ] §4 audit hooks are runnable commands
[ ] §5 decisions baked retain rationale (audit-readable)
[ ] §5b lock readiness summary matches §2.2 status
[ ] OOS access is structurally enforced (ImportError on misuse), not just doctrinally forbidden
[ ] Append-only enumeration log is CI-enforced
[ ] DSR computation has a unit test against published worked examples
[ ] Block bootstrap (not i.i.d. resampling) is locked in §2.2
```

---

## §7 — Implementation sequence (when CC handoff is authored)

1. **Phase 0:** read existing OANDA loader + MC bootstrap utility; report contents and identify reuse.
2. **Phase 1:** implement and pass all five sanity tests (Test 1–5 above) on synthetic data. **No EURUSD data touched yet.**
3. **Phase 2:** ACF/PACF analysis on IS EURUSD returns; choose block length; write to lock file; commit.
4. **Phase 3:** lock `harness_lock.json` (hash + commit). After this commit, the harness is gate-active; subsequent changes require a new ADR.
5. **Phase 4:** enumeration runs. Audit logger writes every pattern. No OOS access.
6. **Phase 5:** IS prefiltering + MTC. Patterns surviving move to OOS.
7. **Phase 6:** OOS evaluation. Gate decision recorded.
8. **Phase 7:** verdict written to Pre-Q closure; if FALSIFIED, registry update + lesson capture.

Phases 1 and 3 are blocking; the rest cannot start until they pass.

## Addendum 2026-08-14 — Component A dormant; B–H methodology remains live

**Type:** dated correction under Rule 14. **§2 decision text is not edited.** This ADR is **not** marked dormant as a whole.

[`2026-06-24-oanda-retirement.md`](2026-06-24-oanda-retirement.md) deleted the OANDA REST loader Component A named. No replacement data-loader is specified here. Components B–H (pattern registry, executor, metrics, Politis-Romano stationary block bootstrap, Davison-Hinkley p-value centering, multiple-testing correction, structural IS/OOS enforcement, audit log) are feed-agnostic methodology and remain reusable doctrine for any future feed.

| Date | Change | By |
|---|---|---|
| 2026-08-14 | Addendum 2026-08-14 — Component A dormant (OANDA retired); B–H live. §2 body byte-unchanged. | claim-alignment reconciliation |
