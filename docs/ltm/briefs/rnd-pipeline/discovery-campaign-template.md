# Discovery campaign template

Reusable scaffold for a CME-futures anomaly-discovery campaign on the Databento
research stack (`docs/adr/2026-07-10-databento-research-stack.md`). A *campaign*
is one bounded run of the discovery→validation→admission pipeline against a
pre-registered search universe on one instrument family. This file defines the
**stage pipeline** and — in `§Campaign-defaults` — the **standing rules of
evidence** every campaign inherits.

The statistical *why* behind each stage and default lives in the field guide
`docs/methodology/references/statistics-of-tradable-anomalies.md` (Part II maps
one-to-one onto the stages below); this file is the operational *what*.

Discovery is Notice-phase mining that never blesses a candidate — the wall from
`futures-anomaly-discovery`. A survivor crosses into an Inquire-phase falsifiable
hypothesis only after it clears the gates here, and earns capital only through the
revocable lifecycle in `docs/methodology/strategy_lifecycle.md`.

---

## Stage pipeline

| Stage | Question | Gate / artifact | Owner skill |
|---|---|---|---|
| **0 Register** | Is the universe + frame fixed *before* looking? | Verdict pre-registration freeze (search universe, gate thresholds, K rule, block-size rule, cost gate) committed before the first `pull`. **Mechanism-first HARD gate ([ADR 2026-07-13 HARV lane](../../../adr/2026-07-13-harv-discovery-lane-ratification.md)):** every bundled clause carries a written **reachability attestation** (simulate under a plausible-true world; redesign/drop if structurally un-passable) **before** `register_search open` — H1-style power disclosure on the primary alone is insufficient (Q-HARV-0 scar). **Attestation specification ([ADR 2026-07-16 same-units supersession](../../../adr/2026-07-16-harv-attestation-same-units-supersession.md), `Accepted`):** §R must (§2.1) simulate **every** gate the campaign can die at in **that gate's own units** — a Sharpe-space argument discharges only a Sharpe-denominated gate, never a bp-space cost gate; (§2.2) exhibit the mandatory cost-law inequality `cohort δ (bp/event) ≥ 4 × RT_frac(panel-era median price, commissions included)` — UNREACHABLE if it fails, redesign or do not open; (§2.3) compute every reachability quantity at the basis the gate actually scores on (IS panel for Stage-2, OOS for Stage-6 — never present-day or convenience levels). D5 and H-OD-1 both closed Stage-2 cost-law KILLs under gates this specification would have caught at Stage-0 (M-20). | `strategy-validation` §6, this template |
| **1 Pull** | Get the data without over-spending or era-leaking | Cost-gated `db_fetch.py estimate`→`pull`; discovery phase physically capped at the IS boundary | `databento-data` |
| **2 Mine** | What might be true? | Candidate generation, least-overfit tool first (catch22 → STUMPY → ruptures); outputs are observations, never signals. Campaign runner: `lab/discovery/stage24_runner.py` (Stages 2–4 middle) | `futures-anomaly-discovery` |
| **3 Bind K** | How large was the search? | `register_search.py open` binds campaign-local K_DSR *before* any p-value is read (non-overlap floor per ADR 2026-07-12; formula in `discovery.k_count`). **Mechanism-first additionally requires the instrument-profile consult ([ADR 2026-07-25](../../../adr/2026-07-25-instrument-profile-index.md)):** declare the cell with `--profile-cell <SYMBOL>:<mechanism-id>` and attach the saved `scripts/instrument_profiles.py cell <SYMBOL> <mechanism-id>` output via `--profile-consult`. A nonzero consult exit means a prior binds the cell — a re-proposal bar, a parked concept sharing the anti-SNAG budget, or a running forward test — which the pre-registration must name and address. | `futures-anomaly-discovery` |
| **4 Score (IS)** | Each candidate's edge series on the IS window | Per-candidate edge/return series constructed on IS only; emits the Stage-4 option-(i) return matrix + trades sidecar (`stage24_runner` / `matrix_emit`) consumed by Stage 6 | `futures-anomaly-discovery` + `strategy-validation` |
| **5 Block size** | What dependence horizon must the bootstrap respect? | `block_size` set from the IS return-series ACF (never `sqrt(T)`), bound before any SPA p-value | `strategy-validation` §8 |
| **6 Confirm (OOS)** | Distinguishable from noise given the search, and stable? | Universe correction (`research_utils/universe_gate.py`: SPA/StepM, DSR, PBO/CPCV) + the temporal-consistency battery (`research_utils/temporal_consistency.py`), on the OOS era | `strategy-validation` §8 + Stage-6 battery |
| **7 Realism** | Does it survive on the tradeable contract? | Parent→micro 1:10 re-scale + native-micro fill re-parameterization (realism gate, *not* independence); engine `lab/discovery/realism_mgc.py` | `databento-data` proxy discipline + `realism_mgc` |
| **8 Breadth** | What does it do to the book? | 5th-column ENB / cross-leg-correlation delta vs the locked 4-leg frame (reproduces the Q-NEFF-1 4-leg anchor first). **Companion (mechanistic exposure — [ADR 2026-07-13](../../../adr/2026-07-13-stage8-mechanistic-exposure-companion.md)):** every Stage-8 candidate files an exposure declaration — {unconditional or regime-conditional side; entry session window (ET); expected in-market minutes/yr; per-book-leg structural overlap = expected simultaneous-in-market minutes/yr × sign-agreement} — and the campaign pre-registration binds a structural-overlap admission threshold at Stage 0. Realized-correlation/ENB deltas remain reported but are not sufficient for breadth admission for episodic candidates (in-market < 5% of session clock). **Companion (variance dominance — [ADR 2026-07-20](../../../adr/2026-07-20-stage8-variance-dominance-risk-neff-gate.md)):** a candidate proposed as a **book leg** is admissible only if it lifts **risk N_eff** (`participation_ratio` of the weekly *covariance* matrix — `n_eff_risk_delta > 0` in `research_utils/breadth.py`), never merely dependence N_eff / ENB / cross-leg-correlation delta; the compose pre-registration additionally surfaces `ρ = candidate daily-$std / existing-book daily-$std` at the intended weight and the adjudication panel's $-basis **before** any frozen-engine run, with `ρ ≥ 1.0` a presumptive reject. A positive dependence/correlation delta is necessary context, **never** the book-leg admission grant (Q-COMPOSE-1 falsified; lesson M-21). | `strategy-validation` (breadth) |
| **Admit** | Earn capital, revocably | `strategies-never-locked` lifecycle intake at CANDIDATE; the calibrated Stage-6d decay monitor ships as the death certificate | `docs/methodology/strategy_lifecycle.md` |

Stage numbering is canonical and referenced by campaign pre-registrations
(e.g. "bound at Stage 3", "Stage 6a sign consistency", "route survivor to Stage 8").

---

## §Campaign-defaults

**Status:** RATIFIED (operator, 2026-07-11) per
`docs/adr/2026-07-11-discovery-campaign-defaults-ratified.md`.
**Default #3 amended 2026-07-12** (`Accepted`, operator ratified 2026-07-12) per
`docs/adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md` — the K and V
inputs DSR consumes for overlapping-window/matrix-profile search terms, following a
pre-freeze gate-reachability audit that found the naive raw-subsequence-count K rule
effectively unreachable. The DSR **threshold value** (0.95) is unchanged.

**Default #1 extended 2026-08-21** (`Accepted`, operator ratified 2026-08-21) per
`docs/adr/2026-07-26-regime-candidate-flag-lane.md` — any campaign whose search
involves config/cell selection MAY pre-register an optional dual-track structure
alongside Default #1: Track-1 promotion is unchanged; Track-2 is a non-promoting
**REGIME-CANDIDATE flag lane** scoring Track-1-failing cells on a declared flag
window truncated before a declared `holdout_start`, authorizing (never itself
constituting) a follow-up pre-registration confirmed on the untouched reserved
holdout. A flag never promotes. A campaign that omits this simply runs the
unamended Default #1. Restored to this file 2026-08-21 after this file was pruned
from the archive 2026-08-08 (`prune(T1)`) before the extension could be recorded —
see the ADR's own Addendum 2026-08-21.

These are the standing rules of evidence. A campaign **inherits them by reference**
("inherits ratified Campaign defaults per ADR 2026-07-11") and does **not**
re-ratify. This table is the **single source of truth for the values** — the ADR
is the dated ratification event and does not restate them; a campaign that needs
a different value **overrides a single default only with its reason stated in that
campaign's §8 pre-registration** (an in-place edit of a value here is forbidden —
it goes through a superseding ADR + re-baseline).

| # | Default | Value (FROZEN) | Rationale (see field guide) |
|---|---|---|---|
| 1 | **Temporal-not-instrument OOS axis** | Discovery + **all** tuning on **IS `2010-01-01 : 2018-12-31`** (parent); statistical OOS = **`2019-05-06 : present`** (native-micro era). The native-micro re-run on the OOS era is a **realism** gate, not an independence gate. | Instrument/feed is *not* an independent axis — same order book, arbitraged path (Jaccard-0.96 same-path scar, Domain 5). Independence must be temporal. Consciously accepts the pre-2019-viability selection bias, on the record. |
| 2 | **Two-level K** | **Campaign-local K** (feeds SPA/StepM — needs the within-campaign return series) + **`K_eff = K_intrinsic`** (within-search trial count; feeds DSR / Clause K). **`K_banked(family)`** is still read from closed manifests and **must be disclosed** in every pre-registration and screen row, but it **does not** enter `K_eff` or gate admission ([ADR 2026-08-04](../../../adr/2026-08-04-family-k-bank-disclosure-not-gate.md), `Accepted`; same wording as [`strategy_harvest.md`](../../../methodology/strategy_harvest.md) §Clause K / Requirement 3). Abandoned campaigns still bank their K (disclosure ledger only). | `K=1` understates overfitting by construction; within-search multiplicity is the honest DSR denominator. Family banks stay visible for reviewer judgment but no longer sum into Clause K. Domain 4. |
| 3 | **Universe correction** | **SPA** (family gate, adjusted `p < 0.05`) + **StepM** (superior set), block bootstrap with an **explicitly-chosen `block_size`** (never `sqrt(T)`); **DSR ≥ 0.95**; **PBO < 0.5** via CPCV (`n_folds=10, n_test_folds=8` → 36 paths) wherever config selection occurred. **K/V-rule for DSR (amended 2026-07-12, `docs/adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md`):** for overlapping-window search terms (matrix-profile/STUMPY-class), the K contribution is the **non-overlap tiling floor** `Σ⌊T/m⌋`, never the raw overlapping-subsequence count; report the `{floor (binding), raw}` bracket together. `V` (across-trial Sharpe variance) is pinned **unconditionally to `V=1/n`** (n = the candidate's OOS trade count) — the module's default empirical estimator is biased upward by the edge it scores and, tested, does not converge even at 100 candidates. Every campaign must disclose the minimum-detectable per-trade Sharpe its bound `(K,V,n)` requires, before freeze. | The best-of-K max-statistic null, not the per-candidate null (Domain 4). Vetted libraries only — `arch.bootstrap` (SPA/StepM/MCS) + `skfolio` CPCV; re-implementation forbidden (`strategy-validation` §8). **K/V amendment rationale:** the raw overlapping-subsequence count assumes independence LdP's `SR0` formula requires but overlapping windows do not have; the naive empirical-V estimator degenerates toward 0 (DSR toward vacuous) at low scored-candidate counts — both found via the 2026-07-12 pre-freeze gate-reachability audit (`docs/notes/audits/2026-07-12-disccamp0-gate-reachability-audit.md`), the Q-HARV-0-lesson obligation applied structurally. |
| 4 | **Temporal-consistency battery** | Sub-era **sign** consistency **≥ ⌈0.7·Y⌉ of Y** calendar-year OOS sub-eras positive; **drop-top-year** concentration (edge stays > gate with its single best year removed); **regime-slice survival** (ruptures/HMM labels are **test conditions, never filters**); **CUSUM** on the candidate's own edge series over the OOS era. | Sign stability, not magnitude stability, distinguishes a real effect from a one-era artifact (Domain 5). Regime labels as filters is the Q-REGIME-COND-1 scar. |
| 5 | **Decay-monitor-at-admission** | A candidate is **inadmissible** unless it ships with a CUSUM decay-monitor spec **whose null was calibrated during validation** (the Stage-6d artifact). **Extended 2026-07-26 ([`mechanism-counterparty-constraint-boundaries`](../../../adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md) §2-A(iv), `Accepted`):** a **constraint-flow** candidate (Requirement-1a Path) must additionally monitor its **constraint observable** — the AUM, fix volume, imbalance size, or OI whose disappearance ends the flow — alongside the edge-series CUSUM. | P&L decay detection is slow by arithmetic necessity (Domain 5); a monitor designed *at admission* is the death certificate. Q-DECAY-1: live decay coverage ≈ 0 precisely because detectors were never designed at admission. **Constraint-observable rationale:** for a mandate-driven flow the constraint vanishing is the *cause* and PnL decay is only the symptom — the observable leads the equity curve by however long the detection lag is, which is exactly the lag Q-DECAY-1 measured as fatal. |
| 6 | **Per-campaign cost gate** | A declared `--max-cost` total, checked against the **summed `estimate`** before any `pull`; first campaigns run inside the **$125 free-credit** window. | Every pull metadata-priced and ceiling-gated; the databento ADR's cost falsifier (§4) is program-level, this is per-campaign. Domain 7. |

**Inheritance / override:** a campaign brief names the inheritance line, freezes its
own instance of these values in its pre-registration (a snapshot of an inherited
value is fine — it is not a competing canonical source), and states any override
+ reason in §8. Silent override defeats the ratification and voids the campaign.

---

## Authoring a new campaign

1. Copy the pipeline above; write a campaign brief (`docs/briefs/rnd-pipeline/<CAMP-ID>.md`)
   naming the instrument family, the frozen tool ladder, and the inheritance line.
2. Author the verdict pre-registration (`docs/briefs/pre-registration/<CAMP-ID>-preregistration.md`)
   — Stage-0 freeze of the search universe, the gate thresholds (from `§Campaign-defaults`),
   and the *rules* for every data-derived integer (campaign-local K, `block_size`,
   summed estimate), each bound at its own pre-result step and back-filled.
   **If mechanism-first (HARV-shaped):** include a **reachability attestation per bundled
   clause** (HARD gate per ADR 2026-07-13) — simulate each clause under a plausible-true
   world; do not open the search until every clause is reachable or redesigned. Per
   [ADR 2026-07-16](../../../adr/2026-07-16-harv-attestation-same-units-supersession.md)
   (`Accepted`): simulate **every** gate in **that gate's own units** (not just the
   confirm-floor gate in Sharpe space), exhibit the cost-law inequality explicitly for
   any cost/kill gate, and price every quantity at the basis that gate actually scores
   on — not present-day or convenience levels.
3. Commit the pre-registration **before** the first `db_fetch.py pull` (freeze
   ordering is checkable via git — see `strategy-validation` §6). For mechanism-first,
   also before `register_search open`.
4. Run the stages; a survivor exits to `strategy_lifecycle` admission, a clean
   all-null close banks the family's cumulative K and the process-defect log.

First instance: `docs/ltm/briefs/rnd-pipeline/DISC-CAMP-0-shakedown.md` (GC parent →
MGC micro pipeline shakedown), frozen at
`docs/ltm/briefs/pre-registration/DISC-CAMP-0-preregistration.md`.

## Related

- `docs/adr/2026-07-11-discovery-campaign-defaults-ratified.md` — ratifies `§Campaign-defaults`.
- `docs/adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md` — amends Default #3's DSR K/V inputs.
- `docs/adr/2026-07-13-harv-discovery-lane-ratification.md` — mechanism-first lane + HARD reachability gate before `register_search open`.
- `docs/adr/2026-07-10-databento-research-stack.md` — the data + discovery + validation stack these campaigns run on.
- `docs/adr/2026-07-10-strategies-never-locked-lifecycle-governance.md` — the admission route a survivor exits into.
- `docs/methodology/references/statistics-of-tradable-anomalies.md` — the field guide (Part II = these stages; Domains 1–8 = the rationale column).
- `.claude/skills/futures-anomaly-discovery/` · `.claude/skills/strategy-validation/` · `.claude/skills/databento-data/` — the executing skills.
