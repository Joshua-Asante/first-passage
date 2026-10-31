---
name: strategy-validation
description: Plan, reproduce or assess First Passage backtests, TradingView inspection and offline/native research. ALWAYS use for Joshua's TradingView backtest CSV uploads; real-or-overfit questions; parameter sweeps/config grids; robustness, plateau, placebo, permutation, multiplicity, selection effects, Step-0, panel integrity, pre-registration, forward tests, day-of-week/subset effects; deflated/probabilistic Sharpe (DSR), PBO, reality check, SPA, Romano-Wolf/StepM, model confidence set (MCS), universe correction, CPCV; "what config next" or "does the best of K survive". Also fires before ANY proposed re-run (direction flip, exit redesign, new filter); excursion counterfactuals, cost pre-flight and futures-anomaly-discovery K accounting. Use for execution/fill assumptions, costs, chronology and reproducibility; reuse existing engines. Route investigation framing to inqhiori, artifact structure to brief-authoring, CSV metrics to trade-csv-reconcile and generation to futures-anomaly-discovery.
---

# Strategy Validation

## Backtesting entrypoint

Use this skill to plan, reproduce or assess First Passage backtests, including
TradingView inspection and offline/native-oriented research. Before a run, read
[execution and reproducibility](references/backtesting-execution.md); it routes to
existing engines and commands and identifies what their evidence can support.
For selection, overfitting, counterfactuals or statistical tests, continue below.
Load only the route needed for the current claim.

The owning campaign and [AGENTS.md](../../../AGENTS.md) retain project rules,
protected windows and frozen configurations. This skill grants no market-data,
trading, account or spending authority. Within an approved research scope, proceed
without routine reapproval; changes to protected scope still follow its owner.
Evidence sufficiency depends on the claim: there is no universal cost multiple,
component Sharpe hurdle, sample size or mandatory multi-agent review for every run.
Campaign-specific requirements and dormant-test restrictions below still apply.

Protocols proven 2026-06-11 (USDCAD investigation: Aegis→BPC→plateau→placebo→permutation chain). Provenance: SESSION-RECORD-USDCAD-BPC-2026-06-11 §Method lessons L1–L7.

## 0. Test-ordering principle (read first, every time)

Rank pending tests by **P(changes the verdict) ÷ cost** and run down that list. Selection-level tests (placebos, permutation, mechanism probes) almost always outrank parameter-level tests (grids, sweeps) — a parameter plateau around a spurious selection still passes, because perturbing *around* a lucky point confirms the point.

Canonical examples: SVRN cfg10-first (mechanism probe before parameter refinement — correct); BPC 10-run grid before 2-run day placebo (backwards — the placebo reframed everything).

**Plateau ≠ validity.** A plateau pass validates parameters *conditional on* the selection (day, session, instrument, direction). Test the selection itself with placebos/permutation, and remember what each test kills: permutation kills random-labeling, NOT path-overfit. Keep a "which nulls remain alive" ledger in the session record.

## 1. Step-0 panel-integrity battery (mandatory before any metrics)

Run `scripts/step0_battery.py` on every TV export before computing anything. Checks: entry-minute census vs declared timeframe (all-:00 on a 15m strategy = wrong chart TF); UTC→ET hour mapping inside the declared session window (DST-aware); day-of-week census vs allowed days; zero entries on event dates when blocks are ON; n within bounds vs prior runs; date-span coverage vs an optional full-period claim (`--expected-span`, catches a time-clustered/isolation export silently mislabeled as spanning the whole period); duplicate detection (exact n+net match vs stored runs); config-fingerprint tag parse if present.

Caught on 2026-06-11: a 4H chart masquerading as 15m, a duplicate export, a two-day subset mislabeled as one day. Three defects, one session, all machine-detectable. The date-span check was folded in from the Guardian filter-sweep hardening (2026-06-21) — a time-clustered export otherwise silently breaks any downstream stationarity split (§5(e) halves/thirds).

## 2. Cost-law pre-flight (before designing, not after failing)

Compute explicit round-trip commissions and slippage for the intended instrument,
quantity and stop width before designing a rerun. Under risk-based sizing, tight
stops increase cost per unit of risk; percentage-notional commissions and futures
per-contract fees require different calculations. The empirical helper
`scripts/selection_tests.py costs` supports percentage commissions; inspect its
units and pass explicit inputs rather than applying its FX defaults to futures.
Use the campaign's existing cost model for per-contract fees.

`scripts/cost_geometry_pregate.py` is the canonical implementation
(`round_trip_cost_price()` and `cost_r()`) of per-trade, stop-distance-normalized
cost. It owns the formula; do not restate it from memory. Its Phase-0 report is
report-only; use explicit price-unit inputs and retain the fee-unit caveats above.

Estimate net expectancy and its cost sensitivity; there is no universal multiple
to clear (the 4x convention was deleted by operator ruling 2026-10-24). Do not
reinstate a fixed cost-in-R ceiling or the deleted harvest cost gate. Follow any
remaining campaign-specific cost assumptions without generalizing them to every
backtest.

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
- **Autocorrelation/persistence confound (the drift warning's magnitude analogue).** A shuffle that holds the outcome series fixed only controls directional/base-rate confounds; on a magnitude-persistence claim over an autocorrelated continuous series (range, volatility, volume), a zero-mechanism surrogate carrying the outcome's own ACF clears that placebo — anchor: AUDIT-2026-08-18-tr-placebo-misspecified, where 20/20 AR(1) surrogates calibrated to lag-1 alone beat both real datasets through the full frozen battery. The honest null carries the series's own dependence structure: constrained surrogates (IAAFT / phase-randomized, or parametric matched to the measured ACF *profile*, not just lag-1 — long-memory series make an AR(1) null a strawman) run through the identical pipeline. A frozen battery's fitness is per claim family, not global — before reusing one on a new family, re-derive which confound that family is exposed to and confirm the null controls it. And keep the two questions separate: "is there predictability usable at this construction" (presence — gates) vs "does it exceed the series's own linear structure" (attribution — types the finding); conflating them is how a mundane effect gets dressed as a mechanism, and how a useful generic conditioner gets killed for novelty it never claimed. Standing instantiation: [`docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md`](../../../docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md).

Rationale + the surrogate/bar-permutation designs this doesn't cover: `docs/methodology/references/statistics-of-tradable-anomalies.md` Domains 1, 3.

**Pre-registration completeness (two-implementer test).** Before freezing a spec's prose, ask: would two independent implementers compute identical numbers from it alone? Ambiguous conditioning/aggregation language ("matched day-session-history conditioning") can admit both a marginal and a within-stratum reading — it did, producing divergent verdicts (one sign-flipped) across three scripts before adversarial review caught it (2026-08-29, MYM candidates 2–4; `docs/adr/2026-07-11-tradable-anomalies-statistics-adoption.md` Addendum 2026-08-29). If the prose doesn't pass that test, ship reference code or a worked numeric example on synthetic data alongside the freeze — prose alone is not sufficient. Applies to every `docs/spec/` FROZEN battery and every `docs/briefs/pre-registration/` file.

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

**K-tiering (declared, not silently skipped — 2026-08-24).** §8a (SPA/StepM/MCS) and §8c
(PBO-via-CPCV) are gated on the declared search-space size K:
- **K∈{0,1}** — no real multiplicity to correct for (a single candidate, or a trivial one-trial
  "search"). The correction is a **declared no-op**: log "K≤1, correction not applicable" rather
  than silently never invoking §8a/§8c — the audit trail should show this was a considered
  decision, not an omission.
- **K∈{2,3}** — the correction **runs**. This is the only band that is both reachable and
  load-bearing under the current admission ceiling: in the standard (mechanism-first) lane,
  `lab/discovery/admission_schema.py` refuses to open a manifest once
  `research_utils.axis_screen.floor_at_k(K) > CAP` (`CAP = 1.0`), which the code's own comment
  states occurs at **K≥4** for the standard 6.5-year confirm window — a candidate cannot reach
  this section with K≥4 in that lane at all (`ABORT-NO-MANIFEST`, Phase 3). The separate
  charter-governed deep lane has its own `K_CEILING = 33` and is out of scope for this tiering.
- §8b (deflated Sharpe / DSR) needs no separate tiering — it is already K-aware by construction
  (`SR0` is a function of K); this convention is scoped to §8a/§8c only.

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
The skill-side breadth launcher was removed 2026-10-15; for self-test or re-arm use `PYTHONPATH=lab python -m research_utils.breadth` — not a standing Stage-8 step.

**Integration (minimal live set — W4).** Campaign preregs name their live limbs.
Standing defaults: mechanism-first admission + DSR-cap refuse (S6), temporal
consistency where prereg requires it, realism limbs named by the campaign.
**SPA/StepM (8a) and PBO (8c) are DORMANT** — re-arm only when a campaign prereg
explicitly names thresholds **and** an operator GO lifts dormancy. DSR (8b)
remains available; module default is `var_trials=1/n` (audit R5, flipped
2026-08-15). An explicit pin still overrides.

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
