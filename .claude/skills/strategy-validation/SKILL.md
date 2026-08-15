---
name: strategy-validation
description: Test protocols for validating trading-strategy backtests against overfitting, selection bias, and relay defects. ALWAYS use this skill when Joshua uploads a TradingView backtest CSV, asks whether a backtest result is real or overfit, runs a parameter sweep or config grid, mentions robustness, plateau, placebo, permutation test, multiplicity, selection effect, Step-0, panel integrity, pre-registration, forward test design, day-of-week or subset effects, deflated Sharpe / DSR, probabilistic Sharpe, probability of backtest overfitting / PBO, reality check, SPA / superior predictive ability, Romano-Wolf / StepM, model confidence set, universe-level correction, combinatorial purged cross-validation / CPCV, or asks "what config should we test next" or "does the best of K survive". Also fires before ANY re-run is proposed (direction flip, exit redesign, new filter) — the excursion-bounded counterfactual and cost-law pre-flight may answer it for zero runs, and consumes the trial count K from the futures-anomaly-discovery ledger. Covers test mechanics only; hand off to inqhiori for when-to-investigate framing, brief-authoring for artifact structure, trade-csv-reconcile for metric definitions.
---

# Strategy Validation

Protocols proven 2026-06-11 (USDCAD investigation: Aegis→BPC→plateau→placebo→permutation chain). Provenance: SESSION-RECORD-USDCAD-BPC-2026-06-11 §Method lessons L1–L7.

## 0. Test-ordering principle (read first, every time)

Rank pending tests by **P(changes the verdict) ÷ cost** and run down that list. Selection-level tests (placebos, permutation, mechanism probes) almost always outrank parameter-level tests (grids, sweeps) — a parameter plateau around a spurious selection still passes, because perturbing *around* a lucky point confirms the point.

Canonical examples: SVRN cfg10-first (mechanism probe before parameter refinement — correct); BPC 10-run grid before 2-run day placebo (backwards — the placebo reframed everything).

**Plateau ≠ validity.** A plateau pass validates parameters *conditional on* the selection (day, session, instrument, direction). Test the selection itself with placebos/permutation, and remember what each test kills: permutation kills random-labeling, NOT path-overfit. Keep a "which nulls remain alive" ledger in the session record.

## 1. Step-0 panel-integrity battery (mandatory before any metrics)

Run `scripts/step0_battery.py` on every TV export before computing anything. Checks: entry-minute census vs declared timeframe (all-:00 on a 15m strategy = wrong chart TF); UTC→ET hour mapping inside the declared session window (DST-aware); day-of-week census vs allowed days; zero entries on event dates when blocks are ON; n within bounds vs prior runs; date-span coverage vs an optional full-period claim (`--expected-span`, catches a time-clustered/isolation export silently mislabeled as spanning the whole period); duplicate detection (exact n+net match vs stored runs); config-fingerprint tag parse if present.

Caught on 2026-06-11: a 4H chart masquerading as 15m, a duplicate export, a two-day subset mislabeled as one day. Three defects, one session, all machine-detectable. The date-span check was folded in from the Guardian filter-sweep hardening (2026-06-21) — a time-clustered export otherwise silently breaks any downstream stationarity split (§5(e) halves/thirds).

## 2. Cost-law pre-flight (before designing, not after failing)

Under risk-based sizing, **cost-in-R ∝ price / stop_distance** (tight stop → huge notional per $risk → commission on notional). Compute the round-trip hurdle from the intended stop width BEFORE building:

`cost_R ≈ [2·commission_pct·price + 2·slippage_ticks·ticksize] · (price/stop_dist) / price` — or just run the empirical version in `scripts/selection_tests.py costs` on any comparable panel. Convention: target expectancy ≥ 4× the hurdle. Reference points: 0.097R at 1.42×ATR(15m) USDCAD (crippling); 0.055–0.072R at 2.5×ATR.

## 3. Excursion-bounded counterfactuals (zero-run kill test)

Before ANY direction-flip or exit-redesign re-run: TV's Favorable/Adverse excursion columns bound the counterfactual. For an inverse-direction thesis, long AE = short FE. Bucket each trade per candidate (stop S, target T): certain-win (counter-FE≥T, counter-AE<S), certain-loss, ambiguous (both exceeded — path order unknown), scratch. Report best/worst expectancy bounds including costs. **State censoring limits explicitly:** excursions are censored at the original exits; targets beyond the original stop are unobservable.

This killed the entire BPC-inverse design space in one analysis, zero runs.

## 4. Plateau protocol (parameter robustness) — ARCHIVED (W4 2026-08-07)

> **Archived — not the standing validation path.** Re-arm only via a fresh
> pre-reg with the same-feed baseline rule + operator GO
> ([`W4 ADR`](../../../docs/adr/2026-08-07-w4-minimal-gate-set-dormancy.md)).

±1-step neighbor per knob, one change per run, everything else frozen. **Pre-register pass criteria before run 1** (e.g., ≥8/10 neighbors positive AND median ≥ half of center expectancy). Track with `scripts/plateau_tracker.py` (dedups, prints running gate). Read pair shapes: dome = parameter well-placed; flat = insensitive; cliff = needle/overfit.

**Same-feed baseline is mandatory** — comparing neighbors on feed B against a center measured on feed A is forbidden (2026-06-11 flaw: OANDA neighbors vs Pepperstone center).

## 5. Selection & multiplicity accounting

When a config arrives post-hoc tuned (or any "best slice" is proposed), quantify before arguing: `scripts/selection_tests.py` provides (a) bootstrap CI on expectancy + P(≤0) + P(≥gate); (b) best-of-K subset under demeaned null ("how often does the best day look this good in a zero-edge panel?"); (c) label-permutation test (P(best ≥ obs), P(spread ≥ obs)); (d) drop-top-k concentration; (e) halves/thirds stationarity.

Convert governance objections into measurements — they get stronger when quantified, and they can be honestly overturned (the 2026-06-11 permutation result overruled the bootstrap-based "lucky bar" lean: Tue-minus-rest p=0.006).

**Null hygiene — name it, and handle drift (upstream of every test above).**

- **Name the null explicitly, every time** (joint-hypothesis problem). "Anomalous" is relative to a model of fair returns; an unnamed null defaults to zero-drift, and a long-only rule on a trending instrument beats *that* null trivially — you have rediscovered the drift, not an edge. State the benchmark the edge is measured against (zero-drift / buy-and-hold / time-series-momentum) before computing.
- **Permutation drift-handling.** Shuffling signals/labels against returns tests *timing skill*. Leave drift in a long-only-on-a-trending-series test and it beats its permutations by being long — the honest null includes the unconditional drift (detrend, or claim only timing). This is the most common way a permutation flatters a strategy. And **block-shuffle time-clustered signals** — naive shuffling destroys the clustering and overstates significance.

Rationale + the surrogate/bar-permutation designs this doesn't cover: `docs/methodology/references/statistics-of-tradable-anomalies.md` Domains 1, 3.

## 6. Pre-registration template (forward tests)

Required sections, all fixed before the first forward trade: frozen-config table; **power disclosure** (per-trade σ in R, SE at each checkpoint n — at typical 1.1R σ and n=25, SE≈±0.23R: decision rules are expectation-based stops, not significance tests, and the doc must say so); checkpoints with kill/extend/escalate rules; trade-rate clause (signal frequency is part of the hypothesis); forbidden moves; append-only audit hook ("was any criterion moved after data arrived? any yes voids the checkpoint").

**Path-independence phrasing:** validation/unpark conditions must name what must be independent (price path, period, instrument) — never just "a different feed." Pepperstone↔OANDA entry-date Jaccard was 0.96: a different source, the same path.

## 7. Epistemic-status metadata

Every input in a concept-stage Pine script declares its status in the tooltip: STARTING POINT (research-derived, unvalidated) / LOCKED (validated, do not touch) / OUT-OF-EVIDENCE-BASE (enabling = new hypothesis, not confirmation). The warning travels with the artifact to the moment of temptation.

## 8. Universe-level correction & selection-under-K

§5 tests selection WITHIN one panel (best day/slice under a demeaned null). §8
tests selection ACROSS K distinct candidates/configs, each with its own return
series — the case the `futures-anomaly-discovery` ledger is built to feed. Its
`register_search.py close` step emits K and a cheap Bonferroni/BH triage; §8 is the
rigorous version. **Trigger:** any candidate that is the winner of a search over K
strategies/configs (ledger output, grid winner, mined signal). If it came from a
search, its naive p-value and Sharpe are inflated until corrected here.

**8a. Universe-level data-snooping (arch — do not reimplement).** The whole
correction layer is in `arch.bootstrap`, the same package as the block bootstrap:
- `SPA` — White's Reality Check / Hansen's SPA; the snooping-adjusted p-value that
  the best model beats the benchmark ("SPA is also known as the Reality Check").
- `StepM` — Romano-Wolf; returns the *set* of models superior to the benchmark under
  family-wise error control (a wrapper around SPA).
- `MCS` — Model Confidence Set; the set statistically indistinguishable from the best.
Frame strategy returns as losses relative to a benchmark (zero-edge / buy-hold); pass
the benchmark loss series + the K-column model-loss matrix. **Use block bootstrap
(`bootstrap='stationary'` or `'circular'`) with `block_size` set to the return
autocorrelation scale — do NOT accept the default sqrt(T)** (arch's own docs say
block_size "should be provided"). This is the rigorous replacement for the ledger's
Bonferroni/BH floor, and it needs the returns of all K strategies — which is why the
ledger records K in the first place.

**8b. Deflated Sharpe / PSR (`lab/research_utils/deflated_sharpe.py`; skill
`scripts/deflated_sharpe.py` is a thin launcher).** Deflate the headline
Sharpe for selection under K AND non-normality. Consumes K (from the ledger) + V
(variance of the K trial Sharpes) → SR0 (expected max Sharpe under K zero-edge
trials) → DSR = P(true SR > SR0), penalizing negative skew and fat tails.
**Pre-register the DSR pass threshold before computing** (reference default 0.95).
Sharpe must be per-observation, consistent with n — deannualize first if needed, and
express V in the same units. Anchors: sr=SR0 → DSR 0.5; the same SR at K=100 vs
K=10k drops DSR from ~0.15 to ~0.0002. K is not optional — K=1 understates
overfitting by construction. **Self-test:** planted controls in
`lab/validation_selftest.py` must fail (negative) / pass (positive) DSR at 0.95 —
see `tests/test_validation_selftest_dsr_gate.py`. Invoke:
`PYTHONPATH=lab python -m research_utils.deflated_sharpe …`.

**8c. PBO via CPCV (skfolio — leakage-controlled).** Probability of Backtest
Overfitting: over combinatorial train/test splits, the fraction where the
in-sample-best config lands in the bottom half out-of-sample. Use
`skfolio.model_selection.CombinatorialPurgedCV(n_folds, n_test_folds, purged_size,
embargo_size)` to generate the paths — purging (drop train obs whose labels overlap
the test set) + embargoing (drop train obs immediately after test obs, for serial
correlation) control the leakage §4's plateau and §5's halves/thirds do not. Rank IS
vs OOS per path; **PBO = P(OOS rank of the IS-best config in the bottom half); PBO >
0.5 = overfit.** Config: n_folds=10, n_test_folds=8 → 36 paths (LdP-style); keep path
counts in the tens–hundreds (skfolio warns that large counts signal misconfiguration,
since each split is a full refit).

**8d. Block, not IID.** If §5(a)'s bootstrap in `selection_tests.py` resamples trades
IID, upgrade it: futures returns are autocorrelated and path-dependent, so use arch's
stationary/circular block bootstrap (same engine as 8a). IID resampling understates
the CI on an autocorrelated series.

**8e. Incremental breadth — TOMBSTONED as live producer (W4 2026-08-07).**
Code retained at `lab/research_utils/breadth.py` for re-arm / self-test; **not**
the default Stage-8 path. Envelope §2 item 6 coordinates stay doctrine without
a sole live producer until a re-arm ADR
([`W4 ADR`](../../../docs/adr/2026-08-07-w4-minimal-gate-set-dormancy.md)).
Do not launch via skill `scripts/breadth.py` as standing procedure.

**Integration (minimal live set — W4).** Campaign preregs name their live limbs.
Standing defaults: mechanism-first admission + DSR-cap refuse (S6), temporal
consistency where prereg requires it, realism limbs named by the campaign.
**SPA/StepM (8a) and PBO (8c) are DORMANT** — re-arm only when a campaign prereg
explicitly names thresholds **and** an operator GO lifts dormancy. DSR (8b)
remains available; pass `var_trials=1/n` (or pin V) until the module default
flips (audit R5 / 2026-09-01).

**Orchestrator (dormant as default promote/reject — W4).**
`lab/research_utils/universe_gate.py` still composes 8a+8b+8c and retains
`--self-test`, but is **not** the default promotion path. Re-arm conditions in
the W4 ADR. Sibling temporal-consistency
(`research_utils/temporal_consistency.py`) remains the Stage-6 companion when
prereg requires it.

## Boundaries

- Metric definitions (R-pinning, DD reconstruction, column shims) → trade-csv-reconcile.
- Whether to investigate at all, SNAG budgets, gate philosophy → inqhiori / programme-audit.
- Artifact structure for records/pre-regs/handoffs → brief-authoring.
- Instrument-level state (active concepts, dead lists, durable findings) → `ops/instruments/<SYMBOL>.md` ledger; read it before deriving.
- Trial count K that §8 consumes, and the pre-registration of the search space →
  `futures-anomaly-discovery` ledger
  (`lab/discovery/register_search.py`; skill
  `.claude/skills/futures-anomaly-discovery/scripts/register_search.py` is a
  thin launcher — `PYTHONPATH=lab python -m discovery.register_search …`).
- Statistical rationale — why each test exists, the 8 domains, the staged pipeline →
  `docs/methodology/references/statistics-of-tradable-anomalies.md` (reference, not gating).
- Universe-level tests (SPA/RealityCheck/StepM/MCS) live in `arch.bootstrap`; CPCV in
  `skfolio.model_selection`. Do not reimplement the bootstrap re-centering — subtle
  correctness lives in the vetted library.
