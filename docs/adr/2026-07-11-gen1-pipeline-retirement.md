# ADR 2026-07-11 — Retire the Gen-1 CFD-era discovery→admission pipeline (validation harness + sweep engine + Path-B WFO + concept-intake); park codification

**Status:** `Accepted` — **operator STRATEGIC-LoR ratification recorded 2026-07-11 (Joshua).** Retiring a whole research subsystem is a subsystem/track-tier Delete, which the three-loop binding ADR (`docs/adr/2026-06-12-three-loop-methodology-binding.md`) reserves to STRATEGIC-LoR authority. The advisor session drafts and justifies; the operator ratifies (or rejects) and only then does this ADR become `Accepted` and land with the retirement commit. Phases 0–2 were executed in an isolated worktree (§7) to de-risk ratification; **ratification is now recorded (operator, 2026-07-11); the retirement and the Phase-3 REPO_MAP provenance rows are already merged to `main` (`bdc45a3`, PR #317), so this flip closes the formal Proposed to Accepted gap.**
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Decision date:** 2026-07-11
**Authors:** Joshua (decision — pending) + claude.ai advisor (drafting) + Claude Code (execution, post-ratification)
**Supersedes:** none directly. Retires the CFD-era research pipeline that `docs/adr/2026-07-10-databento-research-stack.md` (Gen-2) functionally replaced.
**Related:** `docs/adr/2026-07-10-databento-research-stack.md` (Gen-2 discovery stack — the supersessor; §3 of it *forbids* hand-rolling the DSR/PBO/CPCV layer, which retroactively frames the Gen-1 harness); `docs/adr/2026-07-10-r6-nogo-futures-residual-disposition.md` (R6 = NO-GO — no prop rail exit for any Gen-1 output); `docs/adr/2026-07-03-hardcore-p2-edge-transfer-gate.md` (P2 edge-transfer FALSIFIED — no ported CFD edges enter); `docs/adr/2026-06-30-no-manual-trading-cfd-retirement.md` (2026-07-10 addendum — FXIFY/DXTrade closed, no CFD candidates enter); `docs/adr/2026-06-05-monorepo-layer-boundaries.md` + `REPO_MAP.md` (the boundary contract + tier map the retirement must survive; `sweep/` and `scripts/wfo/` already classified lab/P3); `docs/adr/2026-06-05-concept-admissibility.md` (the concept-intake contract being retired); `docs/adr/2026-06-05-sweep-engine.md` (the two-tier sweep engine being retired); the three prior retirement ADRs whose pattern this copies — `docs/adr/2026-06-12-notion-surface-retirement.md`, `docs/adr/2026-06-17-dukascopy-retirement.md`, `docs/adr/2026-06-24-oanda-retirement.md`.
**Layer:** methodology + research tooling (`lab/validation/**`, `scripts/wfo/**`). **Not** strategy/risk-control: no Pine source, no `dd_protection`/`firm_rules`/`portfolio_mc` constant, no allocation, no MC anchor (99.83/0.17/4.37) is touched. `core/` is untouched.

---

## §0 — Rule 0 reads (production-source verification)

**Honesty preamble (load-bearing — do not strip at ratification).** These files were **content-read via the Windows filesystem on 2026-07-11**, during the session that authored this draft, and **re-verified in worktree `claude/gen1-pipeline-retirement-2026-07-11` at implementation.** Git-log anchors below are populated (`git log -1 --format='%h %ci' -- <path>` in the worktree).

1. **§0 anchors populated.** Every path below carries a commit hash. Ratification still requires confirming anchors against the merge-base commit that lands this ADR.
2. **The reverse-dependency (import) audit WAS performed at implementation (Phase 0a).** The draft's "not performed" caveat is resolved: `git grep` across `core/ lab/ ops/ tests/ scripts/` enumerated every importer of the retired modules; `codification → validation` was severed; `validate_candidate.py` and `run_corpus_fdr.py` retired with the harness. Phase 0a is recorded in §7.

Files content-read (2026-07-11), anchors:

- `REPO_MAP.md` — anchor `f2be990` (2026-07-11). Confirms: `lab/validation/sweep/` and `scripts/wfo/` classified **lab / P3** (candidate-for-review); `lab/codification/` "imports `validation`" (§4 Q-e — the critical edge, severed at Phase 0a); `scripts/validate_candidate.py` classified lab, "imports `validation`" (retired with harness); the retirement-provenance row pattern (weekly-review-feeder kept as a struck-through row for move history).
- `docs/adr/2026-07-10-databento-research-stack.md` — anchor `7814ec6` (2026-07-10). §3 alternative "Hand-roll the multiplicity/DSR/PBO layer instead of `arch`/`skfolio`" ruled out ("subtle correctness traps … Re-implementation is forbidden (§5)"); Gen-2 owns SPA/StepM/MCS (`arch`), DSR (`deflated_sharpe.py`), PBO/CPCV (`skfolio`).
- `STATE.md` (2026-07-10 curation) — anchor `04fee2e` (2026-07-11). R6 = NO-GO; FXIFY $200K DXTrade formally CLOSED; P2 FALSIFIED; DJ30→MYM prototype FALSIFIED 2026-07-09 (structural venue cost, not tunable); external-sourcing customer closed.
- `docs/methodology/strategy_lifecycle.md` — anchor `ce9b69f` (2026-07-10). Gen-2 admission axis (LOCKED × authorization, MECHANISM/SURVIVAL-ONLY, decay-monitor-at-admission) — the customer the Gen-1 harness's disposition step was meant to feed, now served by the lifecycle ADR.
- `.claude/skills/strategy-validation/SKILL.md` §8 — anchor `7814ec6` (2026-07-10). Confirms the Gen-1 harness's four load-bearing design invariants (full trial set, config-first metric, path-distribution-not-boolean, block-not-IID) are **already restated in prose** in §8 — so they survive the code's retirement.
- `lab/validation/__init__.py` — anchor `6bf0dff` (2026-06-06; retired; anchor is pre-retirement). Enumerates the hand-rolled modules: `ingest, cpcv, pbo, dsr, permutation, controls, disposition, config`. Docstring self-describes as "R&D pipeline stage 4" consuming TV trade CSVs via `portfolio_mc.load_trades`.
- `lab/validation/sweep/__init__.py` — anchor `6bf0dff` (2026-06-06; retired). Two-tier Pine sweep engine; authoritative tier = **manual paste into TradingView Strategy Tester**; the novel invariant `PREFILTER_RANK_RHO_FLOOR = 0.70` + `PARITY_NET_PF_BAND = 0.02`.
- `lab/validation/concept_intake/__init__.py` — anchor `6bf0dff` (2026-06-06; retired). Package entry for `admissibility_contract.yaml`, `check_concept.py`, `dedup.py`, `feedback.py`, `schema.py`, `contract.py`; example `negative_rediscovery_xagusd.yaml`.
- `scripts/wfo/run_path_b.py` — anchor `08e236b` (2026-05-13; retired). Path-B WFO runner entry point; REPO_MAP classifies `scripts/wfo/` lab, in the `check_boundaries` name-collision index.
- `lab/research/external_sourcing_2026-06-30/CLOSURE.md` — anchor `96470f3` (2026-06-30). Confirms the external-strategy-sourcing intake closed (null triage) — one of the three dead intake mouths.

**Files verified at implementation (Phase-0 gates, not assumed):**
- `docs/rejected_candidates.md` **body** — Phase 0c: XAGUSD guardian-family mirror confirmed (Guardian-on-XAGUSD entry present; `negative_rediscovery_xagusd.yaml` coverage verified).
- `lab/validation/corpus/` **contents** — Phase 0b: held only FDR machinery atop the retired harness; retired with the harness (no load-bearing evidence beyond what evidence dirs already carry).

**Files NOT read this session (not load-bearing for this retirement):**
- `docs/adr/2026-07-10-strategies-never-locked-lifecycle-governance.md` **full text** (read `strategy_lifecycle.md` summary only).
- `docs/methodology/regime_robustness_gate.md` (read attempt failed when MCP died at drafting) — noted for completeness.

---

## §1 — Context

The repo now carries **two complete generations** of the discovery→admission pipeline. Gen-2 landed 2026-07-10 (`databento-research-stack`): Databento GLBX.MDP3 data → `register_search.py` pre-registered trial-count K → `strategy-validation` §8 universe gate (SPA/StepM/MCS via `arch`, DSR via `deflated_sharpe.py`, PBO/CPCV via `skfolio`) → temporal-consistency battery → native-micro realism gate → `strategy_lifecycle` admission. Gen-1 is the CFD-era pipeline it replaced: `concept_intake` (YAML admissibility contract) → `codification` (concept → Pine) → `sweep` (two-tier Pine grid, authoritative tier = manual TradingView paste) → a **hand-rolled** validation `harness` (DSR/PBO/CPCV/permutation re-implemented in `lab/validation/`) → disposition.

**Gen-1's intake is now dead on all three mouths, and its exit is closed:**
- **CFD / manual candidates** — FXIFY $200K DXTrade formally CLOSED, manual trading retired (`2026-06-30` ADR, 2026-07-10 addendum). None enter.
- **Ported CFD edges** — P2 edge-transfer gate FALSIFIED (`2026-07-03`); the DJ30→MYM rebuild died on structural venue cost 2026-07-09. None enter.
- **External-sourced strategies** — `external_sourcing_2026-06-30` closed null. None enter.
- **Exit (a prop rail for anything admitted)** — R6 = NO-GO (`2026-07-10`). Nothing Gen-1 could admit has a live venue to reach.

A pipeline with no live producer, no live consumer, and a supersessor already merged is not dormant infrastructure — it is standing maintenance surface. `check_boundaries` scans it, the test suite exercises it, and every session that opens `lab/validation/` is tempted to "fix" a second, now-forbidden implementation of the exact statistics Gen-2 delegates to vetted libraries. The `databento-research-stack` ADR §3 already ruled that hand-rolling this layer is a correctness hazard; leaving the Gen-1 hand-roll in place is that ruled-out alternative, live in the tree.

**Decision driver (one sentence):** with all three Gen-1 intakes closed, the prop-rail exit NO-GO, and Gen-2 merged as the canonical replacement, the Gen-1 pipeline is dead weight whose continued presence is a maintenance and correctness liability — retire it (preserving three named invariants and the one bridge Gen-2 will still need), rather than carry a second, forbidden implementation of Gen-2's own gate.

---

## §2 — Decision

**Decision (proposed):** Retire the Gen-1 CFD-era discovery→admission pipeline from the active tree — `git rm` the validation harness, the sweep engine, the Path-B WFO runner, and the concept-intake registry — **after** three extractions and a reverse-dependency audit (§7 Phase 0). **Park** `lab/codification/` (do not delete). Record the retirement in `REPO_MAP.md` with struck-through provenance rows, matching the weekly-review-feeder pattern. Git history preserves every retired byte; retirement is `git`-reversible by construction.

Per-subsystem disposition:

| Subsystem | Disposition | Why | Extract first |
|---|---|---|---|
| `lab/validation/{dsr,pbo,cpcv,permutation,harness,metrics,disposition,ingest,run_candidate}.py` + `config.py` + `gate_config.yaml` | **RETIRE** | Hand-rolled DSR/PBO/CPCV — the exact layer `databento-research-stack` §3 forbids hand-rolling and Gen-2 delegates to `arch`/`skfolio`. Ingests TV trade CSVs only (wrong Gen-2 substrate). No live producer. | `controls.py` → `lab/` (see below); confirm §8 already carries invariants #1–#4 (it does, §0). |
| `lab/validation/controls.py` | **EXTRACT, then keep** | §2.6 synthetic positive/negative self-test (known-overfit must fail the gate; known-real must pass). **Gen-2 has no equivalent** — nothing self-tests the SPA/DSR/PBO chain against a planted candidate. This is the one Gen-1 idea Gen-2 lacks. | Relocate + re-point at the §8 `arch`/`skfolio` gate; wire as a `strategy-validation` self-test. |
| `lab/validation/sweep/**` | **RETIRE** | Authoritative tier = manual TradingView paste; Gen-2 sweeps in `vectorbt` under the K-ledger. Already lab/P3. | The rank-ρ parity invariant (`PREFILTER_RANK_RHO_FLOOR = 0.70`: a pre-filter has **no gate authority** until it clears a rank-correlation floor against the authoritative engine) → pre-register the same falsifier for the Gen-2 `vectorbt`(triage)↔`Nautilus`(fill-realism) pair, in the campaign template §5 or a one-page methodology note. |
| `scripts/wfo/**` | **RETIRE** | Its only admission customer (Q-CORR-1.2 Silver WFO) closed SUPERSEDED 2026-07-01; doctrine moved to CPCV-over-walk-forward for overfitting control (walk-forward survives only as a turnover/latency realism check, which `Nautilus` now owns). Already lab/P3. | Nothing (Q-CORR-1.2 closure already records the lesson). |
| `lab/validation/concept_intake/**` | **RETIRE (most-hedged)** | Intake role → the discovery ledger (every candidate is born with a `register_search` manifest); negative-rediscovery/dedup role → `rejected_candidates.md` + campaign-template §2 lineage ("re-proposal requires new mechanism, not new parameters"). Customer (`external_sourcing`) closed. | **Verify first** (Phase-0 gates 0b/0c): that `corpus/` holds nothing load-bearing AND that the `dedup`/negative-rediscovery registry is fully mirrored into `rejected_candidates.md`. If either fails, this row downgrades to PARK. |
| `lab/codification/**` | **PARK — do NOT delete** | Pine is still the execution language of the **KEEP** rail (TV → CrossTrade → NT8 → Bulenox). A Gen-2 survivor that ever goes live must cross Python→Pine with an identity check (the Aegis→6J 129/129 pattern). Codification is the only machinery pointed at that bridge. Wrong *input format* today (concept YAML, not a Python strategy spec), so park with a re-point trigger, don't maintain or delete. | Re-point trigger: "first DISC-CAMP survivor reaches admission." Until then: sever its dead `→validation` import (Phase-0 0a) so it is inert-and-import-clean. |
| `scripts/validate_candidate.py` | **RETIRE or re-point** (Phase-0 decides) | Imports `validation` (REPO_MAP). If it only invokes the retired harness, it retires with it; if a live caller exists, re-point to the §8 gate. | — |

**Explicitly NOT retired:** any `lab/analysis/**` closure directory, any `docs/briefs/pre-registration/**`, any `docs/rejected_candidates.md` entry, any banked K, any PREREG-* artifact. These are **evidence**, governed by the repo's annotate-never-delete discipline; they are what makes cumulative-K and the rejected registry honest. Retirement touches *machinery*, never *evidence*.

**Effective:** on the ratification commit, **and** only after §7 Phase 0 passes. **Scope:** `lab/validation/**`, `scripts/wfo/**`, `scripts/validate_candidate.py`, plus REPO_MAP/CLAUDE/STATE provenance edits. No `core/`, no Pine, no locked constant.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Status quo — keep both generations** | Two live implementations of DSR/PBO/CPCV is the correctness hazard `databento-research-stack` §3 explicitly named; the Gen-1 hand-roll is the ruled-out "hand-roll instead of `arch`/`skfolio`" alternative, sitting in the tree. Standing maintenance + a magnet for forbidden "fixes." |
| **Delete Gen-1 wholesale, no extraction** | Loses `controls.py` (the one self-test Gen-2 lacks) and the rank-ρ parity invariant (the sweep layer's genuinely novel discipline). Extraction is three cheap moves; losing them is not recoverable without re-deriving. |
| **Delete codification too** | Discards the only Python→Pine bridge, which the KEEP rail (TV/CrossTrade/NT8) will need the moment a Gen-2 survivor goes live. Parking costs nothing (git-inert); deleting forces a from-scratch rebuild at exactly the wrong time. |
| **Soft-deprecate in place (leave, mark "deprecated")** | Deprecated-in-tree code still gets scanned by `check_boundaries`, still runs in the suite, still tempts fixes, and rots silently. The repo's own precedent (dukascopy, oanda, notion retirements) is clean removal with provenance, not soft-deprecation. |
| **Retire now, skip the import audit** | A retirement ADR that deletes modules without knowing what imports them will break the build (the known `codification → validation` and `validate_candidate → validation` edges alone guarantee it). The audit is non-negotiable Phase 0. |

---

## §4 — Falsifier (revert trigger)

A retirement's falsifier is: *did removing this break or lose something the replacement does not cover?* Because git preserves every byte, the revert is cheap (`git revert` / restore from history) — so the bar for firing it is deliberately low.

- **Extraction-incompleteness falsifier:** if within **two quarterly cycles (by 2027-01-11)** a Gen-2 discovery campaign reaches admission and needs a capability that lived only in the retired Gen-1 code and was *not* captured by the three extractions (controls, rank-ρ parity invariant, §8 invariants #1–#4) → the extraction was incomplete; restore the specific module from git history and amend this ADR. Concretely checkable: a `DISC-CAMP` survivor blocked at Stage 5–8 citing a missing harness capability.
- **Codification-bridge falsifier:** if the parked `codification/` cannot be re-pointed to a Python-strategy-spec input when the first survivor needs it (i.e., parking should have been a rebuild) → the PARK verdict was wrong; open a fresh codification-rebuild ADR. Checkable at the re-point trigger.
- **Premise falsifier (would un-retire the whole ADR):** if any of the three closed intakes re-opens — a CFD/manual venue returns, P2 edge-transfer is re-litigated and passes, or a prop rail is built (R6 flips GO) — then Gen-1's customer base is no longer dead and this retirement's §1 premise is void; re-evaluate before executing (if pre-ratification) or restore (if post).

**Trigger check schedule:** rides the standing quarterly review (2026-08-08 → 2026-11-08; extraction-incompleteness check due 2027-01-11). Check: `git ls-files lab/validation/sweep scripts/wfo` empty; `controls` self-test present and green in the §8 gate; `codification/` still present and import-clean.

---

## §5 — Forbidden moves (under this ADR)

- **Executing any `git rm` before §7 Phase 0 passes.** The reverse-dependency audit + the three extractions + the two concept-intake verification gates are blocking. Deleting first and fixing imports after is the build-breaking move this ADR exists to prevent.
- **Deleting `codification/`.** It is the KEEP rail's only Python→Pine bridge. Park, sever its dead import, re-point later — never delete.
- **Deleting evidence.** No `lab/analysis/**` closure dir, no pre-registration, no `rejected_candidates.md` entry, no banked K. Retirement is machinery-only; evidence is annotate-never-delete.
- **"Improving" a subsystem while extracting it.** `controls.py` and the rank-ρ invariant move **as-is** (re-pointed, not rewritten). A cleanup-during-extraction is scope creep and a fresh overfitting surface (mirrors `databento-research-stack` §5 "improving the delivered skills during integration").
- **Retiring `concept_intake` before verifying `corpus/` and the `rejected_candidates.md` mirror.** The most-hedged row; skipping its two gates risks silently dropping the dedup/negative-rediscovery registry. Gates 0b/0c are hard.
- **Letting the retirement touch `core/`, any Pine source, any locked constant, or the MC anchor.** Research-layer only. A diff that touches `core/dd_protection.py`/`firm_rules.py`/`portfolio_mc.py`/`config/params.toml` or any `.pine` is an integrity failure of this change.
- **Marking this ADR `Accepted` without operator STRATEGIC-LoR sign-off.** Subsystem-tier Delete authority is reserved (three-loop binding ADR). The advisor draft cannot self-ratify.

---

## §6 — Consequences

**Positive:**
- **Pruning yield:** on the order of **25–30 source files** leave the active surface (the `lab/validation` package minus `controls`, plus `sweep/`, plus `scripts/wfo/`, plus `concept_intake/`) — converted into either vetted-library calls (Gen-2) or extracted one-page invariants. Less `check_boundaries` scan surface, fewer suite fixtures, one fewer magnet for forbidden "fixes."
- **Single implementation of the gate statistics.** DSR/PBO/CPCV live once, in `arch`/`skfolio` behind `strategy-validation` §8, matching `databento-research-stack` §3. The correctness hazard of a divergent second implementation is removed.
- **Three disciplines preserved, not lost:** the self-test (`controls`), the pre-filter-has-no-authority-until-rank-ρ invariant, and (already in §8 prose) the full-trial-set / config-first / path-distribution / block-not-IID invariants.
- **The Python→Pine bridge is kept** (parked), ready for the first survivor that needs to reach the KEEP rail.

**Negative (real costs):**
- **Git-archaeology cost** to recover anything under-extracted (mitigated: the falsifier window + the three named extractions).
- **The extraction + audit work itself** — one focused CC session (Phase 0 + 1 + 2), not free.
- **Concept-intake's dedup registry** must be confirmed-mirrored before deletion; if the mirror is incomplete, that merge is additional work (or the row downgrades to PARK).

**Risks:**
- **Untraced import edge breaks the build.** Mitigation: Phase-0 0a enumerates the known edges (`codification → validation`, `validate_candidate → validation`, `sweep/tests → codification`) as the *starting* set and greps for the rest before any `rm`.
- **A parked-but-import-dirty `codification`** (still importing retired `validation`) would fail `check_boundaries` or import at runtime. Mitigation: Phase-0 0a severs that edge as part of parking.

**Downstream artifacts:** `REPO_MAP.md` retirement rows (struck-through provenance); `STATE.md` open-threads note if any retired subsystem is referenced there; `CLAUDE.md` only if it names a retired path. The three-prior-retirement ADRs are the format precedent.

---

## §7 — Implementation plan and record

### Implementation record (2026-07-11)

**Worktree:** `claude/gen1-pipeline-retirement-2026-07-11` (isolated; Phases 0–2 executed; Phase 3 provenance commit pending operator STRATEGIC-LoR ratification).

| Phase | Status | Record |
|---|---|---|
| **0a — Reverse-dependency audit** | **PASS** | Import audit completed across `core/ lab/ ops/ tests/ scripts/`. `codification → validation` severed. `scripts/validate_candidate.py` and `scripts/run_corpus_fdr.py` retired with the harness (harness-only callers; no live re-point needed). |
| **0b — `corpus/` inspection** | **PASS** | `lab/validation/corpus/` held only FDR machinery atop the retired harness — no load-bearing evidence beyond what evidence dirs already carry. Retired with the harness. |
| **0c — `rejected_candidates.md` mirror** | **PASS** | XAGUSD guardian-family mirror confirmed in `docs/rejected_candidates.md` (Guardian-on-XAGUSD entry; `negative_rediscovery_xagusd.yaml` coverage). `concept_intake` row stays **RETIRE** (not downgraded to PARK). |
| **1 — Extractions** | **DONE** | `controls.py` → `lab/validation_selftest.py` (planted-overfit / planted-real generators). Rank-ρ invariant → `docs/methodology/prefilter_rank_correlation_gate.md`. §8 invariants #1–#4 confirmed present in `strategy-validation` SKILL (no rewrite; cross-reference only). Wiring `validation_selftest.py` into the §8 gate is dispatched: [`gate-orchestrator handoff`](docs/ltm/briefs/rnd-pipeline/2026-07-11-cc-handoff-gate-orchestrator.md). |
| **2 — Retire** | **DONE** | `git rm` of `lab/validation/` (harness modules), `lab/validation/sweep/`, `scripts/wfo/`, `lab/validation/concept_intake/`, `lab/validation/corpus/`, `scripts/validate_candidate.py`, `scripts/run_corpus_fdr.py`. `lab/codification/` parked with `engine_types.py` + `concept_schema.py` extracted from retired sweep/concept layers; `compose.py` / `emit.py` import-clean. |
| **3 — Provenance** | **DONE** | `REPO_MAP.md` struck-through retirement rows merged to `main` (L50-52, L94, L132-133). Operator ratification recorded 2026-07-11. |

### Implementation plan (reference — Phases 0–3)

**Phase 0 — BLOCKING pre-conditions (no `git rm` until all pass).**
- **0a — Reverse-dependency (import) audit.** Grep every import of each retired module across `core/ lab/ ops/ tests/ scripts/`:
  ```bash
  git grep -nE 'from (lab\.)?validation|import validation|from validation' -- core lab ops tests scripts
  git grep -nE 'validation\.sweep|from sweep|scripts\.wfo|from wfo|concept_intake' -- core lab ops tests scripts
  git grep -nE 'codification' -- core lab ops tests scripts   # who still calls the parked bridge
  ```
  Known starting edges to resolve: `codification → validation` (**critical** — sever so codification parks import-clean; fallback: retire codification too only if severing is non-trivial *and* the operator accepts losing the bridge — default is sever+keep); `scripts/validate_candidate.py → validation` (retire-with-harness or re-point); `validation/sweep/tests → codification` (internal to the retired set — fine). Any *live* (non-test, non-retired) importer of a retired module must be re-pointed to §8 or itself retired **before** proceeding.
- **0b — `corpus/` inspection.** Confirm `lab/validation/corpus/` holds nothing load-bearing beyond what evidence dirs already carry. If it does, that content is preserved (moved to an evidence dir) before deletion.
- **0c — `rejected_candidates.md` mirror check.** Confirm the `concept_intake` `dedup`/negative-rediscovery registry (e.g. `negative_rediscovery_xagusd.yaml`) is fully represented in `docs/rejected_candidates.md`. Merge any gaps first. **If 0b or 0c cannot be cleared, downgrade the `concept_intake` row from RETIRE to PARK** and proceed with the rest.

**Phase 1 — Extractions (as-is; no rewrites).**
1. `controls.py` → `lab/` (e.g. `lab/validation_selftest.py` or fold into the §8 gate path); re-point at the `arch`/`skfolio` chain; wire as a `strategy-validation` self-test (planted-overfit-must-fail / planted-real-must-pass).
2. Rank-ρ parity invariant (`PREFILTER_RANK_RHO_FLOOR = 0.70`, `PARITY_NET_PF_BAND`) → pre-register the same falsifier for the Gen-2 `vectorbt`↔`Nautilus` pair in the campaign template §5 (or a one-page `docs/methodology/` note).
3. Confirm §8 already carries harness invariants #1–#4 (verified §0 — no action beyond a one-line cross-reference in the retirement commit message).

**Phase 2 — Retire.** `git rm` the RETIRE rows; re-point/retire `validate_candidate.py`; sever `codification → validation`. Then: `check_boundaries` green, `validate_params` green, full `pytest` green (retired fixtures removed, not skipped).

**Phase 3 — Provenance.** `REPO_MAP.md` struck-through retirement rows (weekly-review-feeder pattern); `STATE.md`/`CLAUDE.md` edits only where a retired path is named. Commit on a branch; PR for operator confirmation — **no self-merge** (mirrors `databento-research-stack` Phase 3).

---

## §10 — Audit hooks (runnable)

```bash
cd "C:/Users/joshu/multi_firm_operations"

# RETIRE targets are gone from the active tree (post-execution → expect empty)
git ls-files lab/validation/sweep scripts/wfo
git ls-files lab/validation | grep -vE 'controls|__init__|corpus'   # harness modules gone

# The three extractions survived
git ls-files | grep -E 'validation_selftest|controls'               # self-test kept
grep -rn 'PREFILTER_RANK_RHO_FLOOR\|rank-ρ\|rank correlation floor' docs/briefs/rnd-pipeline docs/methodology
grep -n 'full trial set\|path distribution\|block.*not.*IID\|config-first' .claude/skills/strategy-validation/SKILL.md

# The bridge is PARKED (present, not deleted) and import-clean
git ls-files lab/codification | head -1                              # non-empty ⇒ parked, not deleted
git grep -nE 'from (lab\.)?validation|import validation' -- lab/codification  # expect EMPTY (edge severed)

# No live importer of a retired module remains
git grep -nE 'from (lab\.)?validation|validation\.sweep|scripts\.wfo|concept_intake' -- core lab ops scripts \
  | grep -vE '^lab/codification|_selftest'   # expect empty (only the extracted self-test references validation)

# Retirement touched NO locked constant / Pine / core (expect empty)
git diff --stat <ratification>~1..<ratification> -- core/ '*.pine' core/config/params.toml core/dd_protection.py

# Provenance recorded
grep -n 'RETIRED\|retirement' REPO_MAP.md | grep -iE 'validation|sweep|wfo|concept_intake'

# Evidence preserved (expect NON-empty — retirement must not have touched these)
git ls-files docs/briefs/pre-registration lab/analysis | head
grep -c '.' docs/rejected_candidates.md

# Falsifier check (quarterly; extraction-incompleteness due 2027-01-11)
ls discovery_manifests/*.json 2>/dev/null && echo "if any survivor blocked citing a retired-harness capability → §4 fires"
```

---

## Verification

```bash
# Discipline check (mechanical)
python scripts/check_brief.py docs/adr/2026-07-11-gen1-pipeline-retirement.md --type adr
# Expected: no HARD violations (§0 anchors populated 2026-07-11)

# Rule 0: no pending anchors remain
grep -n '\[§0-pending' docs/adr/2026-07-11-gen1-pipeline-retirement.md   # expect EMPTY
for f in lab/validation/__init__.py lab/validation/sweep/__init__.py \
         scripts/wfo/run_path_b.py REPO_MAP.md \
         docs/adr/2026-07-10-databento-research-stack.md ; do
  git log -1 --format='%h %ci  '"$f" -- "$f"
done

# Phase-0 gates cleared before execution
git grep -nE 'codification' -- core lab ops tests scripts   # 0a: the critical edge resolved
```

---

## Addendum (2026-07-24, operator ruling) — parked codification bridge RETIRED

The Gen-1 retirement parked `lab/codification/` ("inert, import-severed") with a
re-point trigger of "first DISC-CAMP survivor reaches admission" and a do-not-delete
note. The trigger's premise did not survive contact: the first admitted candidate
(ORB-MNQ, lifecycle CANDIDATE 2026-07-16) arrived via the Class-S / venue-native
route with no DISC-CAMP composer step, and the bridge's input format (concept-YAML)
was already wrong for any current pipeline. On 2026-07-24 the operator ruled
"retire the bridge" (Algorithm repo review ruling #3 —
`docs/notes/2026-07-24-algorithm-repo-review-handoff-series.md`). `lab/codification/`
(12 files) is deleted; bytes remain in git history; a future Python→Pine bridge is a
fresh build against the then-current survivor format, not a restore.


## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-11 | Initial draft — `Proposed`, awaiting operator STRATEGIC-LoR ratification; §0 anchors pending (MCP down at authoring); reverse-dependency audit deferred to Phase 0 | claude.ai advisor |
| 2026-07-11 | §0 anchors populated; reverse-dependency audit performed (Phase 0a); Phases 0–2 executed in worktree `claude/gen1-pipeline-retirement-2026-07-11`; §7 implementation record added; Phase 3 provenance commit pending ratification | Claude Code |
| 2026-07-11 | **Operator STRATEGIC-LoR ratification** (Status to Accepted); retirement + Phase-3 provenance confirmed already on main (bdc45a3 / PR #317); gate-orchestrator follow-on dispatched | Joshua (operator) + claude.ai advisor |
