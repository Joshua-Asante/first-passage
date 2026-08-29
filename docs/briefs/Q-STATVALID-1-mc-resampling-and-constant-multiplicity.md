# Q-STATVALID-1 — Has the same statistical rigor the repo applies to strategy-candidate discovery ever been applied to the risk-control layer's own constants?

**Status:** `CLOSED-FALSIFIED 2026-08-23` — Limb C fires on both grids (winner-margin z≈0.8-1.2 vs the 2-sigma bar; 3 of 5 DD-trigger-grid losing scores unrecoverable); Limb B independently `AMBIGUOUS` (Pepperstone 4-strategy panel retired 2026-08-03, unrecoverable at $0). Closure: [`closures/Q-STATVALID-1-closure-falsified.md`](closures/Q-STATVALID-1-closure-falsified.md).
**Authored:** 2026-08-18
**Closed:** N/A
**Authors:** Joshua + Claude Code
**Parent question:** N/A — opened from the assumption-sweep audit note
**Sub-questions opened:** none
**Loop:** Inquire-phase Pre-Q — closure gated on two $0/K=0 arithmetic reads of the panel and the already-logged grid-search scores
**Artifact path:** `docs/briefs/Q-STATVALID-1-mc-resampling-and-constant-multiplicity.md`

---

## Section 0 — Rule 0 reads (production-source verification)

- `core/mc/ingest.py:191-198` — `build_week_blocks`, the 5-business-day block constructor consumed by every MC run.
- `core/mc/simulation.py:221,249` — IID block draws with replacement from the `build_week_blocks` output.
- `docs/methodology/references/statistics-of-tradable-anomalies.md:96-98` — names the Politis–White (2004) automatic block-length selector as the rigorous alternative, adjacent to a qualitative endorsement of the repo's fixed 5-day choice, without ever running the selector.
- `docs/methodology/references/statistics-of-tradable-anomalies.md:105-128` (Domain 4) — states the E[max of N] / best-of-N correction is mandatory whenever a best-of-N config is picked from noisy trials.
- `docs/methodology/regime_robustness_gate.md:46` — the 6-month "outer" bootstrap that nests the same unvalidated 5-day "inner" block unit; zero DSR/PBO/multiplicity hits anywhere in this file.
- `docs/adr/2026-04-17-dd-trigger-calibration.md:34-40` — the 5-config `DD_TRIGGER`/`DD_SCALE` grid search, scored on the same historical panel it then reports the winner against.
- `core/mc/modes.py:643-658` — `SWEEP_CONFIGS`, the 8-config allocation-weight grid, same pattern.
- `docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md` — scopes K/DSR correction exclusively to strategy-candidate discovery/harvest intake; silent on constant-selection grids.

All eight anchors carried forward verbatim from `docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md` findings B1 and C1 — gathered via direct tool reads during that sweep (several independently spot-checked live per the audit note's Sources Read block), not re-derived here.

---

## Section 1 — Context and motivation

The 2026-08-18 assumption-sweep audit note (`docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md`, findings **B1** and **C1**) surfaced that the risk-control layer's own load-bearing constants — the MC engine's resampling unit, and the `dd_protection`/allocation grid winners — have never been put through the statistical validation the repo requires everywhere else in the pipeline. Every published pass-rate/bust-rate/p99-DD figure, every `dd_protection` lock, every allocation ADR, and the live c1 rail's WATCH-1 0.50× sizing decision traces through the IID week-block resampling unit (B1); the same panel that scores the `DD_TRIGGER`/`DD_SCALE` and allocation grids also reports their winners' headline numbers with no multiplicity correction (C1). The repo runs DSR/PBO-style correction religiously for strategy-candidate discovery (`docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md`) — this Q asks whether that same discipline was ever extended one layer down, to the constants that decide how those candidates get sized and gated.

---

## Section 2 — Prior art / lineage

- `docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md` §4 Tier B/C — origin of both limbs; each survived the audit's D-gate (adversarial-novelty verify pass) as genuinely unexamined, distinct from the 5 items deleted at §3 as `ALREADY_COVERED`.
- Audit §3 D-gate deletions were checked for overlap with this Q's scope: none of the 5 deleted items (DD-multiplier firm-mismatch, CI manifest-check gap, sessions-gate CI mirror, Sentinel Tier 2-3 non-firing, Harvest Req-5 slippage constant) touch resampling-unit validity or grid-search multiplicity. No overlap; this Q is clean of already-closed ground.
- `docs/methodology/regime_robustness_gate.md` — the standing half-panel-split doctrine this Q deliberately does **not** re-litigate or re-derive; see Section 5 for the conflation this Q exists to separate from it.
- `docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md` — the K-bank/DSR scoping ADR; its silence on constant-selection grids is the gap this Q's C-limb prices.
- `docs/mc_anchor_history.md` — the 99.83%/0.17% historical-record anchor; downstream of the resampling unit this Q's B-limb interrogates, cited here only to bound blast radius, not re-opened.

---

## Section 3 — Question (Q-STATVALID-1)

**Q-STATVALID-1:** Do the risk-control layer's own load-bearing constants — the MC engine's resampling unit, and the `dd_protection`/allocation grid-search winners — carry the same resampling-independence validation and multiplicity correction the repo requires of strategy-candidate discovery, or have they never been checked?

Symptom-only rephrase check: the question names what is unchecked (resampling-unit validity; grid-search multiplicity correction) and asks whether it was ever checked — it does not propose a block-length selector, a DSR formula, or any specific fix.

---

## Section 4 — Falsifiable hypothesis (H-STATVALID)

**H-STATVALID (combining limb B — resampling independence, and limb C — grid-search multiplicity):**

- **Limb B:** If the 4-strategy portfolio's weekly-aggregated P&L series exhibits statistically significant serial dependence at lags 1-4 weeks (Ljung-Box or the ±2/√n band), the MC engine's IID week-block draw understates the panel's true dependence horizon, and every bust-rate/p99-DD figure downstream of it is optimistically biased.
- **Limb C:** If a closed-form best-of-N / DSR deflation applied to the already-logged per-config scores in the 5-config `DD_TRIGGER`/`DD_SCALE` grid and the 8-config allocation grid shrinks the winner's margin over the runner-up to within the trial-count noise floor, the reported headline pass/bust figures do not survive formal multiplicity correction even though they survive the (different-purpose) regime-robustness half-panel gate.

**Reject H-STATVALID if:** both limbs come back clean — B: no lag 1-4 autocorrelation exceeds the ±2/√n band and Ljung-Box p ≥ 0.05 at all four lags; C: the winner's margin over the runner-up in both grids exceeds the trial-count noise floor (i.e. survives best-of-N deflation) for both the DD-trigger/scale grid and the allocation grid.

**Accept H-STATVALID if:** either limb fires — B: any lag 1-4 autocorrelation exceeds ±2/√n or Ljung-Box p < 0.05 at any of lags 1-4; OR C: the deflated margin collapses into the noise floor for either grid, OR the losing-candidate scores were never retained (an absence that itself independently confirms the correction was never applied and cannot now be applied retroactively at $0).

**Ambiguous-hold if:** the panel data or logged grid scores needed for either limb's read are not locatable at the cited paths/ADR tables without new spend (i.e. the $0/K=0 read itself fails) — this converts that limb to a named absence-finding rather than a null result, and the overall verdict holds pending a scoped re-check of where the missing artifact lives.

---

## Section 5 — Forbidden moves

- **Treating the regime-robustness half-panel gate as already covering this Q — including reading a grid winner's regime-robustness PASS as evidence the multiplicity question is moot.** This is the specific conflation the Q exists to separate: regime-robustness tests whether an edge survives a *different half of history*; it says nothing about whether the resampling *unit* used to compute pass/bust rates is validated (limb B), or whether the *constant-selection search itself* was multiplicity-corrected (limb C). A grid winner clearing the half-panel split after an uncorrected search is exactly the SNAG/best-of-K pattern (per-cut PASS after search = biased) the repo's own lessons registry already names as a graveyard trap. Ruled out because `docs/methodology/regime_robustness_gate.md` has zero DSR/PBO/multiplicity hits and its 6-month outer bootstrap nests the same unvalidated 5-day inner unit it would need to validate independently — the gate cannot certify what it never tests.
- **Re-deriving or re-tuning `DD_TRIGGER`/`DD_SCALE` or the allocation weights under this brief.** Both are frozen constants under change-control (pre-registration → re-MC → regime-robustness gate → admitting ADR per CLAUDE.md Protection section). This Q reads whether the original selection was multiplicity-corrected; it has no authority to move either constant regardless of verdict.
- **Running a fresh MC simulation with a Politis–White block-length selector to "just check."** That is new K/compute spend disguised as a cheap falsifier, and it pre-empts the actual decision this Q is scoped to price (whether the unvalidated unit *matters enough* to warrant that spend) — the cheap falsifier is a Ljung-Box read on the existing panel, not a re-run of the engine.
- **Treating a `FALSIFIED`/Accept verdict as license to immediately widen the block length or add a multiplicity correction.** Per the `concept-not-constant` discipline, any resulting change needs its own pre-registration → re-derivation → admitting ADR. This Q prices the gap; it does not close it.

---

## Section 6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition (typed) |
|---|---|---|
| `RESOLVED` | Both limbs Reject: B — no lag 1-4 autocorrelation breaches ±2/√n and Ljung-Box p ≥ 0.05 at lags 1-4; AND C — deflated winner margin exceeds the noise floor in both grids | `INTEGRATE` — record the resampling unit and both grid-search winners as evidence-validated; discharge audit findings B1 and C1 as closed. No constant moves. |
| `FALSIFIED` | Either limb Accepts: B — any lag 1-4 breach or Ljung-Box p<0.05; OR C — deflated margin collapses into noise floor, or losing-candidate scores are unrecoverable | `ITERATE` — name (do not open) a successor decision packet scoping a Politis–White block-length re-derivation (if B fired) and/or a formal DSR/PBO correction pass on the two grids (if C fired), each requiring its own pre-registration before any constant moves. |
| `AMBIGUOUS-HOLD` | Panel data or logged grid scores for either limb are not locatable at $0/K=0 | `ITERATE` — record the specific missing artifact as a named absence-finding; re-test when that artifact is located or reconstructed, independent of any other campaign. |

**Pre-registered before either limb's data is read** — per Known Trap #12, §6 is not amended to match what the reads return.

---

## Section 7 — Execution plan (self-executing, $0/K=0 — reuse the cheap-falsifier sketches supplied)

- **Phase 0 — Rule-0 reads.** Done (Section 0).
- **Phase 1a — Limb B.** Run `core/mc/ingest.py::build_week_blocks(panel)` on the existing locked panel; sum each 5-day block to a single weekly P&L scalar per strategy and portfolio aggregate; run `statsmodels.stats.diagnostic.acorr_ljungbox` (or a bare lag-1..4 autocorrelation vs the ±2/√n band) on that series. ~15 lines of Python, one existing CSV, no MC run.
- **Phase 1b — Limb C.** Locate the per-config pass/bust scores for all 5 DD-trigger/scale grid candidates and all 8 allocation-grid candidates — the 2026-04-17 ADR table, Q-DDP-1/Q-SWAP-3 closure artifacts, or logged sweep output near `core/mc/modes.py:643-658` (retrievable via `git show pre-prune-2026-08-08:PATH` if pruned). Apply closed-form E[max of N]/DSR deflation directly to the logged numbers, or the cheaper proxy: diff winner-vs-runner-up margin against the standard error implied by N and trade count. If losing-candidate scores were never retained, record that absence as the C-limb's own finding (routes to Accept per Section 4).
- **Phase 2 — Verdict assertion.** Apply Section 6 mechanically against Phase 1a/1b outputs; produce the closure artifact per Section 9.

Estimated cost: **$0, K = 0**, zero new backtests, zero new data pulls — both phases read existing CSVs and existing logged/ADR numbers only.

---

## Section 8 — Verdict pre-registration

Owed at operator GO, committed before Phase 1 executes, at `docs/briefs/pre-registration/Q-STATVALID-1-verdict-preregistration.md` — the Section 6 table plus the exact Ljung-Box lag/p threshold and the exact deflation formula, frozen before either read runs. Not yet authored: this Q is named, not opened.

---

## Section 9 — Closure record format

Per `references/closure_record.md`, with the mandatory typed `## Iterate` block discharging this brief's Section 6 disposition column. `RESOLVED` → `docs/briefs/closures/Q-STATVALID-1-closure-resolved.md`; `FALSIFIED` → `…-closure-falsified.md`; `AMBIGUOUS-HOLD` → `…-closure-ambiguous-hold.md` with the missing-artifact re-test trigger named. No `recommendation.md` for non-RESOLVED verdicts (sentinel-format convention).

---

## Section 10 — Audit hooks (runnable)

```bash
# Limb B — resampling-unit autocorrelation (the exact cheap-falsifier from the audit note)
python -c "
import pandas as pd, numpy as np
from statsmodels.stats.diagnostic import acorr_ljungbox
# panel/build_week_blocks per core/mc/ingest.py:191-198
from core.mc.ingest import build_week_blocks
blocks = build_week_blocks(panel)  # panel = existing locked 4-strategy CSV
weekly = pd.Series([b.sum() for b in blocks])
print(acorr_ljungbox(weekly, lags=[1,2,3,4], return_df=True))
"

# Confirm the resampling unit is still IID-with-replacement as cited
grep -n "build_week_blocks" core/mc/ingest.py
grep -n -A5 "def build_week_blocks" core/mc/ingest.py
sed -n '215,255p' core/mc/simulation.py

# Confirm the statistics doctrine still names Politis-White without running it
grep -n -B2 -A2 "Politis" docs/methodology/references/statistics-of-tradable-anomalies.md

# Limb C — locate the logged per-config grid scores
sed -n '30,45p' docs/adr/2026-04-17-dd-trigger-calibration.md
sed -n '640,660p' core/mc/modes.py
git show pre-prune-2026-08-08:docs/adr/2026-04-17-dd-trigger-calibration.md 2>/dev/null | sed -n '1,80p'

# Confirm K/DSR scoping is silent on constant-selection grids
grep -n -i "DSR\|PBO\|multiplicity" docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md docs/methodology/regime_robustness_gate.md
# Expected: zero hits in regime_robustness_gate.md; scope-only language in the K-bank ADR
```

---

## Verification

```bash
python scripts/check_brief.py docs/briefs/Q-STATVALID-1-mc-resampling-and-constant-multiplicity.md --type inquire
# Expected: all 6 checks PASS

# Section 0 anchors resolve
grep -n "def build_week_blocks" core/mc/ingest.py
sed -n '215,255p' core/mc/simulation.py
grep -n "Politis" docs/methodology/references/statistics-of-tradable-anomalies.md
sed -n '640,660p' core/mc/modes.py
grep -n -i "multiplicity" docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md

# Cross-reference against the source audit note (findings B1/C1 verbatim origin)
grep -n "^\*\*B1\.\|^\*\*C1\." docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md
```

If any verification command fails, the brief is not complete. Re-author the section that broke; do not handwave.

---

## Pre-Lock Checklist (DRAFT briefs only)

- [ ] Section 0 paths read with anchors
- [ ] Section 3 passes the symptom-only rephrase
- [ ] Section 4 hypothesis binary
- [ ] Section 5 forbidden moves genuinely tempting
- [ ] Section 6 triggers specific
- [ ] Section 8 pre-registration owed at operator GO
- [ ] Section 10 hooks runnable
- [ ] Operator GO given; Phase 1 ran 2026-08-23 per the closure's pre-registration record — see [`Q-STATVALID-1-closure-falsified.md`](closures/Q-STATVALID-1-closure-falsified.md). No discrete pre-Phase-1 tick of this checklist is on record (the other boxes above were never individually checked before Phase 1 executed) — that gap is recorded here rather than retroactively checked off.
