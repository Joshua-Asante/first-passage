# Seven-strategy Select configuration campaign — campaign state (orchestrator-only writes)

**Status:** `PHASE 0 IN FLIGHT (Codex) · PHASE-0 GATE FROZEN · PLAN REVIEW FOLDED (PR #272 open)`
**Last curated:** 2026-09-03 (orchestrator session `claude/orchestrator-role-takeover-yza7vp`)
**Parent plan:** [`2026-09-02-seven-strategy-tradeify-select-configuration.md`](../../superpowers/plans/2026-09-02-seven-strategy-tradeify-select-configuration.md)
(PR [#272](https://github.com/Joshua-Asante/first-passage/pull/272) — **open, not merged** as of
this curation; the Codex review's six P1 + one P2 findings are folded in at `459421b`).
**Role:** this file is the plan's *compact campaign state artifact* (plan §Session handoff protocol)
**and the claim manifest**. One writer — the orchestrating Claude Code session — per the MSL
precedent ([`2026-08-12-msl-program-plan.md`](2026-08-12-msl-program-plan.md) §6) and the
`cursor-fleet` single-writer rule. Workers (Codex / Cursor / local compute) never edit it; they
report via PR description and the orchestrator transcribes.
**Authorizes:** nothing. $0 · K=0 · no candidate contract · no capital · c1 rail stays disarmed.

---

## §1 Roles (plan §Compute and collaboration model, bound to this repo's ADRs)

| Role | Holder | Owns | May not |
|---|---|---|---|
| **Orchestrator** | Claude Code (this lineage) | decompose / freeze gates before outputs are read / review claims against artifacts / integrate / adjudicate; sole writer of this file, `STATE.md`, `docs/SESSIONS.md` for this campaign | merge to `main` (operator; [surface-allocation ADR](../../adr/2026-07-14-cc-cursor-surface-allocation.md) return contract — the [auto-merge gate](../../adr/2026-08-14-cc-cursor-autonomous-loop.md) applies to Cursor packets with a handoff brief, which Phase 0 is not) |
| **Worker — ingestion / engine integration / batch runner** | Codex (`codex/*` branches) | Phase 0 intake; Phase 1 ledger + reconciliation; runner + tests | rank, score a payoff cell, or write any governance surface; fork a simulator that duplicates §3 |
| **Worker — IDE assist** | Cursor | targeted implementation/review on frozen specs (ADR tests 0–3) | locked surfaces (ADR test 1) |
| **Local compute** | operator machine | checkpointed shards from immutable manifests | change seeds mid-run |
| **Board** | operator (Joshua) | every §6 decision; merge; GO for spend | — |

Agreement between assistants is not evidence (plan). The orchestrator's review of a Codex phase is
a `fable-judge`-posture read: claims vs artifacts, re-run what is cheap, `VERIFIED / VERIFIED WITH
CAVEATS / REFUTED`.

## §2 Phase and gate board

| Phase | Gate to leave it | Status | Holder | Evidence |
|---|---|---|---|---|
| Plan | Codex review folded; operator merge | **REVIEW FOLDED** — merge pending (§6 D1) | operator | PR #272 @ `459421b` |
| 0 — Receive and inventory | §4 gate below, verdict `PASS` | **IN FLIGHT** (Codex, `codex/mym-breakout-research`, operator-reported 2026-09-03; branch not yet on `origin` at curation) | Codex → orchestrator review | — |
| 1 — Normalize and reproduce | seven reconciliation reports within frozen tolerances; joint ledger; tests | QUEUED (blocked on 0) | Codex | — |
| 2 — Standalone quality and dependence | eliminations recorded with reasons; no portfolio pick | QUEUED | Codex + orchestrator | — |
| 3 — Freeze search + validation design | pre-registration committed **before** any Phase 4 run; contract items 1–9 all numeric; operator ratifies | QUEUED (orchestrator authors; `pre-ratification-adversarial-panel` before ratification) | orchestrator → operator | — |
| 4 — Deterministic screen (development segment only) | trial ledger complete incl. failures | QUEUED | Codex / local | — |
| 5 — Coarse joint MC (joint-flat weekly blocks, dev segment) | frontier kept; checkpoints resumable | QUEUED | local compute | — |
| 6 — Robustness / falsification | every listed challenge run; failures typed | QUEUED | local compute | — |
| 7 — Locked confirmation | qualifying bound (outer bootstrap 95th + worst partition + realized confirmation path) all < 5%, or `no qualifying configuration` | QUEUED | orchestrator adjudicates | — |
| 8 — Shadow-operational | dry-run parity through the c1 sizing/rule path; M1 + operator GO stay separate | QUEUED | c1-rail lane | — |

Findings label vocabulary (plan): `EXPLORATORY` · `CONFIRMATORY` · `BLOCKED`. **No finding of any
label exists yet.** Nothing numerical may be carried forward without its provenance tuple
(code commit · input hashes · config hash · seed range · environment · output hash).

## §3 Canonical authorities — reuse, never re-implement

The plan's one-simulator rule ("do not let three assistants create three incompatible
simulators") binds to these existing owners. A worker PR that re-derives any of them is
`REFUTED` at review regardless of its numbers.

| Concern | Owner (read before writing) | Note |
|---|---|---|
| Venue rules snapshot | [`core/firm_rules.py`](../../../core/firm_rules.py) `FIRM_RULES["Tradeify_Select_100K"]` — `trailing_locking`, 3.0% EOD trailing DD, 6.0% target, min 3 trading days, inactivity 5 idle days, micro cap 80, $0.91/side, 40% consistency, `weekend_holds: False`, `dd_lock_offset_usd` unreachable (fixed 2026-08-04) | Phase 0's primary-source capture must reconcile to this snapshot; any delta is a **venue-fact** correction under Rule 13, filed by the orchestrator, never patched in a worker branch |
| Path engine + clocks | [`core/mc/simulation.py`](../../../core/mc/simulation.py) `simulate_path` (`intraday_low` optional → honest clock; absent → EOD lower bound), `HORIZON_CAP = 1500`, `horizon_cap` outcome for unresolved paths; [`core/mc/preflight.py`](../../../core/mc/preflight.py) firm kwargs; [`core/dd_geometry.py`](../../../core/dd_geometry.py) | Unresolved paths count as busts in every safety statistic (plan contract item 5) |
| Survivor scoring + week blocks | [`lab/discovery/prop_survivor_scoring.py`](../../../lab/discovery/prop_survivor_scoring.py) (`run_tier_remc`, `paired_blocks_from_daily`, `score_part_a`; thresholds parsed from the frozen prereg, never restated) | Joint-flat integer-week blocks (plan Phase 3) |
| Single-series / composed scoring | [`lab/research_utils/nsurv_channel.py`](../../../lab/research_utils/nsurv_channel.py) `score_nsurv` · [`book_score.py`](../../../lab/research_utils/book_score.py) `score_book` | "computes, does not admit" |
| TV trade-list adapter + honesty label | [`lab/research_utils/msl_score.py`](../../../lab/research_utils/msl_score.py) (`LOWER BOUND` vs `excursion-bounded`) | The plan's `LOWER BOUND` rule is this label, not a new one |
| Loaders | [`core/tv_export_loader.py`](../../../core/tv_export_loader.py) (paired trades, MAE/MFE columns) · [`core/bar_export_loader.py`](../../../core/bar_export_loader.py) / [`scripts/parse_bar_export.py`](../../../scripts/parse_bar_export.py) (BAR EXPORT v0.2 + sidecar) | No ad-hoc CSV interpretation (Phase 0 gate G0.4) |
| Two-level bootstrap precedent | [`lab/analysis/c1/class_s_w1_bootstrap_honest_2026-09-02/`](../../../lab/analysis/c1/class_s_w1_bootstrap_honest_2026-09-02/) (`_boot_paired.py`, `READING.md`) | The plan's Phase 7 qualifying bound is this design |
| Eval bust ceiling of record | [`prop-survivor-scoring prereg v2`](../pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md) §3 Part A: bust ≤ 5.0% | Plan's 5% aligns; the 2026-07-22 §4-withdrawal ADR §5 collision flagged in `SESSIONS 2026-09-02c` is **unruled** (§6 D5) |
| Candidate / campaign governance | [`candidate-contract`](../../adr/2026-08-30-candidate-contract.md) · [`evaluation-order`](../../adr/2026-08-30-evaluation-order.md) · [`operator-approvals-campaign-envelope`](../../adr/2026-08-30-operator-approvals-campaign-envelope.md) · [`terminal-taxonomy`](../../adr/2026-08-30-terminal-taxonomy.md) · [`tradeable-reachable-gate`](../../adr/2026-08-30-tradeable-reachable-gate.md) | Terminal wording in this campaign uses the taxonomy's vocabulary |
| Deployment gates (Phase 8 and beyond) | [`M1`](../../adr/2026-07-22-c1-venue-native-monitoring-maturity.md) · [`rail GO`](../../adr/2026-07-17-c1-rail-build-account-registration-go.md) | Untouched by this campaign |

## §4 Phase 0 acceptance gate — FROZEN 2026-09-03 before any Codex output was read

Applied by the orchestrator to the Phase 0 PR as a diff-plus-gate-output read (whole-file re-reads
only where a claim matters if wrong). Verdicts: **`PASS`** (Phase 1 unlocked) · **`NEEDS_CONTEXT`**
(one re-anchor round for cheap missing fields, then `PASS`/`FAIL`) · **`FAIL`** (Phase 0 re-run).

| # | Check | Verdict on miss |
|---|---|---|
| G0.1 | Exactly seven strategies and seven exports inventoried; `INTAKE.md` + a machine-readable manifest (JSON) + a discrepancy report present. **No ranking, no cross-strategy payoff comparison, no scored cell** (a table ordering strategies by return/PF/DD is a ranking). | `FAIL` |
| G0.2 | Every plan Phase 0 field per strategy, including the two added at review: **final design-decision date** (`UNKNOWN` allowed, never guessed) and **synchronized intraday bars / timestamped intratrade paths available: yes/no**. | `NEEDS_CONTEXT` (fields only) |
| G0.3 | SHA-256, row count, first/last timestamp for every input, hashed from working-tree bytes. **Zero vendor CSVs or Pine bodies committed** — inputs live under a gitignored path (`lab/analysis/**/inputs/*.csv`, `**/*.pine`); manifest carries hashes only. | `FAIL` (public repo) |
| G0.4 | TV trade exports parsed through `core/tv_export_loader.py`, bars through `scripts/parse_bar_export.py`; a non-TV export names its loader and why. | `NEEDS_CONTEXT` |
| G0.5 | Hard stop applied per strategy: labelled decision-grade-capable or `LOWER BOUND`-capable; no "EOD-safe ⇒ intraday-safe" inference anywhere in `INTAKE.md`. | `FAIL` |
| G0.6 | Contamination record: development/tuning overlap **and** repo-history cross-check. The branch name `codex/mym-breakout-research` is reused from PR [#259](https://github.com/Joshua-Asante/first-passage/pull/259) (merged 2026-09-02), whose study [`mym_breakout_entry_2026_09`](../../../lab/analysis/mym_breakout_entry_2026_09/RESULTS.md) **consumed its 2025-01-01→2026-07-31 holdout** for five ORB-MYM entry families; the ORB-MYM v0.4 P50 panel (`orb_mym_volume_gate_2026-09-02`) is fully viewed. Any supplied strategy in those families must say so, and the consumed interval cannot serve as its confirmation segment. | `NEEDS_CONTEXT` → `FAIL` if omitted after re-anchor |
| G0.7 | Discrepancy report lists every strategy-file ↔ export mismatch (symbol, session, quantity convention, gross/net, commission/slippage settings). An empty report states the checks run. | `NEEDS_CONTEXT` |
| G0.8 | Study directory under `lab/analysis/<theme>/<slug>/` registered in [`lab/CATALOG.md`](../../../lab/CATALOG.md) (`lab-catalog` gate); `__init__.py` if tests ship; required CI check `skills (3.12)` green. Recommended slug `lab/analysis/c1/seven_strategy_select_config_2026-09/`; the actual path is recorded in §5 at review. | `NEEDS_CONTEXT` |
| G0.9 | Rule 2 accounting: $0 external spend, no MC compute, K=0 declared in the PR description. | `FAIL` if any cell scored |

## §5 Claim manifest

| Item | Holder | Status | PR / commit | Note |
|---|---|---|---|---|
| Campaign plan | Codex (operator task) | **REVIEWED** — review folded | #272 @ `459421b` | six P1 + one P2 folded into Phases 0/3/4/5/7 + contract items 3/5/8/9; reconciliation table in the plan |
| Orchestrator takeover; this file; Phase 0 gate | orchestrator session 2026-09-03 | **DONE** (pending merge) | this branch | gate frozen before any Phase 0 output was read |
| Phase 0 intake | Codex, `codex/mym-breakout-research` | **DISPATCHED** (operator-reported; pre-dates the review fixes — expect G0.2's two new fields to need a re-anchor) | pending | branch not on `origin` at curation |
| Phase 0 gate review | orchestrator | **QUEUED** — fires when the Codex PR appears | — | check-in scheduled from the takeover session |
| Campaign pre-registration (contract items 1–9; Phase 3 deliverable) | orchestrator authors → adversarial panel → operator ratifies | **QUEUED** | — | must exist before any Phase 4 run |
| Phases 1–8 | per §2 | **QUEUED** | — | — |

**Hashes:** none — no input has been received by this session. **Compute:** completed 0 · remaining
undetermined until §6 D3. **Defects / invalidations:** none; no prior output exists to invalidate.

## §6 Decisions requiring operator input

| # | Decision | Why it is the operator's | Orchestrator recommendation |
|---|---|---|---|
| D1 | Merge PR #272 (`459421b`) | Merge to `main` is operator-only for non-packet PRs; the handoff described it as merged, it is open | Merge; nothing downstream can cite the plan from `main` until then |
| D2 | `STATE.md` queue placement | Queue cap ≤5, 2 rows live; promotion is an operator act (STATE standing rule: "do not auto-open a replacement") | Row 3: *"Seven-strategy Select configuration campaign — Phase 0 (Codex) → Phase 0 gate → prereg; no capital"* with this file as owner. Alternative: fold under row 1's owner set if D4 rules it inside the cultivation envelope |
| D3 | Rule 2 budget line | The plan freezes seeds and a "search budget" but names no spend/compute ceiling; Rule 2 requires the budget before acting | $0 external data; Phases 0–4 ≤ 24 local core-hours; Phases 5–7 priced at Phase 3 with a fresh GO |
| D4 | Relation to queue row 1 (portable-edge cultivation, 2–3 day clock from 2026-09-02, ≤1 candidate contract, ≤3 seats) | Seven *supplied* strategies are complete expressions — the cultivation plan's seats B/C class — but the configuration search is a book-composition objective the cultivation envelope does not name | Rule it a **separate program** under its own envelope (this file); Phase 0 is inventory-only and safe under either reading, so no work waits on D4 |
| D5 | 5% ceiling vs 2026-07-22 §4-withdrawal ADR §5 | Flagged unruled in `SESSIONS 2026-09-02c`; Phase 7 cannot call a pass while the ceiling's own provenance is contested | One-line ruling before Phase 3 ratification |
| D6 | The seven strategies' identities and the intake path | Plan §Immediate next action; only the operator holds the files | Deliver to Codex's intake dir (gitignored); the Phase 0 manifest carries hashes into this file |

## §7 Next exact commands (orchestrator, next session)

```bash
git fetch origin
git ls-remote --heads origin | grep -E 'codex/mym-breakout-research'          # Phase 0 branch landed?
# When the Phase 0 PR exists: read its file list + CI, apply §4 G0.1–G0.9 as a diff read,
# then record verdict + actual study path in §2/§5 and (on PASS) unlock Phase 1.
python scripts/gate_manifest.py --tier pre-commit                            # before any integration commit
```

## §8 Ledger

| Date | Event | Disposition |
|---|---|---|
| 2026-09-02 | Codex authored the campaign plan; PR #272 opened; Codex native review returned six P1 + one P2 | plan `INTAKE-BLOCKED` |
| 2026-09-03 | Operator: Claude Code takes the orchestrator role; Phase 0 in flight on `codex/mym-breakout-research` | takeover |
| 2026-09-03 | PR #272 found **open**, not merged; `codex/mym-breakout-research` found absent on `origin` and identified as PR #259's reused head name | recorded, not blocking |
| 2026-09-03 | Review findings folded at `459421b`; threads resolved; summary comment posted | plan `REVIEW FOLDED` |
| 2026-09-03 | §4 Phase 0 gate frozen before any Phase 0 output was read; §3 authorities pinned; §6 D1–D6 raised | state `PHASE 0 IN FLIGHT` |
