# Seven-strategy Select configuration campaign — campaign state (orchestrator-only writes)

**Status:** `PHASE 0 GATE: FAIL — re-dispatch owed (§9) · VENDOR BYTES ON A PUBLIC REF (§6 D7) · PLAN REVIEW FOLDED ×3 (PR #272 open)`
**Last curated:** 2026-09-03 (orchestrator session `claude/orchestrator-role-takeover-yza7vp`)
**Parent plan:** [`2026-09-02-seven-strategy-tradeify-select-configuration.md`](../../superpowers/plans/2026-09-02-seven-strategy-tradeify-select-configuration.md)
(PR [#272](https://github.com/Joshua-Asante/first-passage/pull/272) — **open, not merged** as of
this curation; three Codex passes are folded in — six P1 + one P2 at `459421b`, four P1 at
`78c82de`, and the eight plan-binding findings from the review of PR #273 at `e8694a9`. This
branch integrates the plan by merge, so either PR may merge first — §6 D1).
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
| Plan | Codex review folded; operator merge | **REVIEW FOLDED ×3** — merge pending (§6 D1) | operator | PR #272 @ `e8694a9` (also carried by this branch) |
| 0 — Receive and inventory | §4 gate below, verdict `PASS` | **FAIL** (2026-09-03 gate review of `codex/mym-breakout-research` @ `706a03e`) — **G0.1:** no `INTAKE.md`, manifest, or discrepancy report; zero of seven strategies inventoried. **G0.3:** three vendor-derived CSVs (~100 MB) committed under `workspace_inputs/` / `workspace_outputs/` on a public ref. Re-dispatch per §9 after §6 D7 | Codex → orchestrator review | §8 ledger, 2026-09-03 gate review |
| 1 — Normalize and reproduce | seven reconciliation reports within frozen tolerances; joint ledger; tests | QUEUED (blocked on 0) | Codex | — |
| 2 — Standalone quality (joint-book limbs moved to Phase 4, after the freeze) | eliminations recorded with reasons on standalone evidence; no portfolio result computed | QUEUED | Codex + orchestrator | — |
| 3 — Freeze search + validation design | pre-registration committed **before** any Phase 4 run; contract items 1–9 all numeric; operator ratifies | QUEUED (orchestrator authors; `pre-ratification-adversarial-panel` before ratification) | orchestrator → operator | — |
| 4 — Joint-book audit + deterministic screen (development segment only) | trial ledger complete incl. failures | QUEUED | Codex / local | — |
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
| Venue rules snapshot | [`core/firm_rules.py`](../../../core/firm_rules.py) `FIRM_RULES["Tradeify_Select_100K"]` — `trailing_locking`, 3.0% EOD trailing DD, 6.0% target, min 3 trading days, `inactivity_max_idle_days: 5` (venue fact: ≥1 trade per Mon–Fri week), micro cap 80, `cost_per_side_usd` 0.91 (**index-micro row only** — MNQ/MYM/MES/M2K; the same file prices MGC at 1.06), 40% consistency, `weekend_holds: False`, `dd_lock_offset_usd` unreachable (fixed 2026-08-04) | Phase 0's primary-source capture must reconcile to this snapshot; any delta is a **venue-fact** correction under Rule 13, filed by the orchestrator, never patched in a worker branch. **Two caveats bind workers:** (a) fees resolve **per instrument** through the specs in [`lab/discovery/cost_model.py`](../../../lab/discovery/cost_model.py), never the tier scalar; (b) the engine's `inactivity_limit` counts *consecutive idle business days* (`simulate_path`), while the venue clock is calendar-week — a **calendar-week adapter** is a Phase 1 deliverable and the only clock admitted in Phase 5 (divergence already flagged in `SESSIONS 2026-09-02c`) |
| Path engine + clocks | [`core/mc/simulation.py`](../../../core/mc/simulation.py) `simulate_path` (`intraday_low` optional → honest clock; absent → EOD lower bound), `HORIZON_CAP = 1500`, `horizon_cap` outcome for unresolved paths; [`core/mc/preflight.py`](../../../core/mc/preflight.py) firm kwargs; [`core/dd_geometry.py`](../../../core/dd_geometry.py) | Unresolved paths count as busts in every safety statistic (plan contract item 5) |
| Survivor scoring + week blocks | [`lab/discovery/prop_survivor_scoring.py`](../../../lab/discovery/prop_survivor_scoring.py) (`run_tier_remc`, `paired_blocks_from_daily`, `score_part_a`; thresholds parsed from the frozen prereg, never restated) | `paired_blocks_from_daily` is **single-series** (synthetic business-day index, `(n_weeks, 5, 1)`) — precedent, not tool; the multi-strategy, real-timestamp joint block builder with joint-flat assertions is a Phase 1 deliverable (plan Phase 3) |
| Single-series / composed scoring | [`lab/research_utils/nsurv_channel.py`](../../../lab/research_utils/nsurv_channel.py) `score_nsurv` · [`book_score.py`](../../../lab/research_utils/book_score.py) `score_book` | "computes, does not admit" |
| TV trade-list adapter + honesty label | [`lab/research_utils/msl_score.py`](../../../lab/research_utils/msl_score.py) (`LOWER BOUND` vs `excursion-bounded`) | The plan's `LOWER BOUND` rule is this label, not a new one |
| Loaders | [`core/tv_export_loader.py`](../../../core/tv_export_loader.py) (paired trades, MAE/MFE columns) · [`core/bar_export_loader.py`](../../../core/bar_export_loader.py) / [`scripts/parse_bar_export.py`](../../../scripts/parse_bar_export.py) (BAR EXPORT v0.2 + sidecar) | No ad-hoc CSV interpretation (G0.4). `pair_tv_export_dataframe` **raises on non-long entries** (the locked book is long-only): a short or two-sided export needs the loader extended — `core/` is a locked surface, so that extension is CC-solo under ADR test 1, never a worker patch |
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
| G0.2 | Every plan Phase 0 field per strategy, including the two added at review: **final design-decision date** and **last result-inspection date** (`UNKNOWN` allowed, never guessed), and **synchronized intraday bars / timestamped intratrade paths available: yes/no**. | `NEEDS_CONTEXT` (fields only) |
| G0.3 | SHA-256, row count, first/last timestamp for every input, hashed from working-tree bytes. **Zero vendor CSVs or Pine bodies committed** — inputs live under a gitignored path (`lab/analysis/**/inputs/*.csv`, `**/*.pine`); manifest carries hashes only. | `FAIL` (public repo) |
| G0.4 | **Long-only** TV trade exports parsed through `core/tv_export_loader.py`; bars through `scripts/parse_bar_export.py`. A short or two-sided export (direction is a Phase 0 field) is recorded `LOADER-BLOCKED` with a hand-paired fixture proving the Entry/Exit pairing, and the loader extension is queued CC-solo for Phase 1. A non-TV export names its loader and why. No ad-hoc parser in the worker branch. | `NEEDS_CONTEXT` |
| G0.5 | Hard stop applied per strategy: labelled decision-grade-capable or `LOWER BOUND`-capable; no "EOD-safe ⇒ intraday-safe" inference anywhere in `INTAKE.md`. | `FAIL` |
| G0.6 | Contamination record: development/tuning overlap **and** repo-history cross-check. The branch name `codex/mym-breakout-research` is reused from PR [#259](https://github.com/Joshua-Asante/first-passage/pull/259) (merged 2026-09-02), whose study [`mym_breakout_entry_2026_09`](../../../lab/analysis/mym_breakout_entry_2026_09/RESULTS.md) **consumed its 2025-01-01→2026-07-31 holdout** for five ORB-MYM entry families; the ORB-MYM v0.4 P50 panel (`orb_mym_volume_gate_2026-09-02`) is fully viewed. Any supplied strategy in those families must say so, and the consumed interval cannot serve as its confirmation segment. | `NEEDS_CONTEXT` → `FAIL` if omitted after re-anchor |
| G0.7 | Discrepancy report lists every strategy-file ↔ export mismatch (symbol, session, quantity convention, gross/net, commission/slippage settings). An empty report states the checks run. | `NEEDS_CONTEXT` |
| G0.8 | Study directory under `lab/analysis/<theme>/<slug>/` registered in [`lab/CATALOG.md`](../../../lab/CATALOG.md) (`lab-catalog` gate); `__init__.py` if tests ship; required CI check `skills (3.12)` green. Recommended slug `lab/analysis/c1/seven_strategy_select_config_2026-09/`; the actual path is recorded in §5 at review. | `NEEDS_CONTEXT` |
| G0.9 | Rule 2 accounting: $0 external spend, no MC compute, K=0 declared in the PR description. | `FAIL` if any cell scored |
| G0.10 | **Reserved-window record** (added 2026-09-03 after the second Codex pass, still before any Phase 0 output was read): derived confirmation boundary per strategy, quarantined-file SHA-256s under a gitignored path, and a loader-assertion test that Phase 1–6 code cannot open them. No P&L, drawdown, cadence, or trade statistic computed on the reserved bytes. | `NEEDS_CONTEXT`; `FAIL` if any statistic was computed on the reserved segment |

## §5 Claim manifest

| Item | Holder | Status | PR / commit | Note |
|---|---|---|---|---|
| Campaign plan | Codex (operator task) | **REVIEWED** — three passes folded | #272 @ `e8694a9` | pass 1: six P1 + one P2 (Phases 0/3/4/5/7, contract items 3/5/8/9); pass 2: four P1 (multiplicity `α`/`M`/procedure, pre-confirmation integrity check, one-path falsifier semantics + `N_conf`, holdout reserved at intake — contract items 10/11, Phases 0/1/2/7); pass 3 (Codex review of #273): eight plan-binding findings — last-inspection date, selection-inclusive outer bootstrap, Phase 2 standalone-only, numeric Phase 6, calendar-week inactivity adapter, joint block builder, per-instrument fees, Rule 2 in iterations (contract items 12/13); three reconciliation tables in the plan |
| Orchestrator takeover; this file; Phase 0 gate | orchestrator session 2026-09-03 | **DONE** (pending merge) | this branch | gate frozen before any Phase 0 output was read |
| Phase 0 intake (first return) | Codex, `codex/mym-breakout-research` @ `706a03e` | **RETURNED — FAIL** (G0.1, G0.3) | no PR | pushed by the operator 2026-09-03: one commit on a base **68 commits behind `main`** (pre-dates PR #259's merge). Content: vet-intake notes for `ORB-MYM-SCALE-1` (`docs/notes/2026-09-01-orb-mym-scale-vet-intake.md`, `2026-09-02-next-vet-candidate-assessment.md`, a three-speed-spec paragraph) plus the raw TV bar export, the parsed `MYM_M15.csv`, and the 60-cell trade ledger. Not a seven-strategy intake |
| Phase 0 gate review | orchestrator | **DONE — `FAIL`** (this session) | — | §4 applied as a diff read; vendor files were opened only to two header lines each for content-class identification, no statistic computed |
| Phase 0 re-dispatch packet | orchestrator | **AUTHORED** (§9) — blocked on §6 D7 | — | operator pastes to Codex; the packet carries its own Phase-0 staleness check and the intake-directory rule |
| Campaign pre-registration (contract items 1–9; Phase 3 deliverable) | orchestrator authors → adversarial panel → operator ratifies | **QUEUED** | — | must exist before any Phase 4 run |
| Phases 1–8 | per §2 | **QUEUED** | — | — |

**Hashes:** none — no input has been received by this session. **Compute:** completed 0 · remaining
undetermined until §6 D3. **Defects / invalidations:** none; no prior output exists to invalidate.

## §6 Decisions requiring operator input

| # | Decision | Why it is the operator's | Orchestrator recommendation |
|---|---|---|---|
| D1 | Merge order for #272 (plan) and #273 (this file) | Merge is operator-only for non-packet PRs. #273 integrates the plan by merge, so **either order works**: #272 first leaves #273 as the two artifacts; #273 first lands the plan too and #272 becomes a no-op to close | Merge #272 then #273; or #273 alone and close #272 — never edit the plan on both as independent branches |
| D2 | `STATE.md` queue placement | Queue cap ≤5, 2 rows live; promotion is an operator act (STATE standing rule: "do not auto-open a replacement") | Row 3: *"Seven-strategy Select configuration campaign — Phase 0 (Codex) → Phase 0 gate → prereg; no capital"* with this file as owner. Alternative: fold under row 1's owner set if D4 rules it inside the cultivation envelope |
| D3 | Rule 2 budget — confirm the classification | Rule 2 counts complete attempt-and-check iterations under the INNER/OUTER/STRATEGIC 3/8/3 limits ([canon §15](../../methodology/inqhiori-canon.md)); a core-hour figure is not a budget. Plan contract item 13 now proposes **STRATEGIC, ≤3 constituent OUTER investigations × 8 iterations, no self-extension** | Confirm item 13's three constituents; keep $0 external data and any core-hour figure as disclosure lines only. Phase 0 is iteration 1 of constituent (i) |
| D4 | Relation to queue row 1 (portable-edge cultivation, 2–3 day clock from 2026-09-02, ≤1 candidate contract, ≤3 seats) | Seven *supplied* strategies are complete expressions — the cultivation plan's seats B/C class — but the configuration search is a book-composition objective the cultivation envelope does not name | Rule it a **separate program** under its own envelope (this file); Phase 0 is inventory-only and safe under either reading, so no work waits on D4 |
| D5 | 5% ceiling vs 2026-07-22 §4-withdrawal ADR §5 | Flagged unruled in `SESSIONS 2026-09-02c`; Phase 7 cannot call a pass while the ceiling's own provenance is contested | One-line ruling before Phase 3 ratification |
| D7 | **Purge the vendor bytes from the public remote** | `706a03e` on `origin/codex/mym-breakout-research` carries the raw TV bar export (`BAR_EXPORT_v0.2_CBOT_MINI_MYM1!_2026-09-01_1b59b.csv`, sha256 `16e8ded6…`, pinned in no tracked manifest), the parsed `MYM_M15.csv`, and `all_declared_trades.csv` (which PR #259's RESULTS declared local-only for carrying vendor-derived prices/timestamps). The orchestrator does not rewrite another author's branch | Delete the remote ref, or force-push the branch without `workspace_inputs/` and `workspace_outputs/`; then ask GitHub support to purge the unreachable objects. #273 lands the `.gitignore` hardening so those roots can never be committed again. Confirm where Codex's actual seven-strategy intake lives (likely uncommitted in its sandbox) before re-dispatching |
| D6 | The seven strategies' identities and the intake path | Plan §Immediate next action; only the operator holds the files | Deliver to Codex's intake dir (gitignored); the Phase 0 manifest carries hashes into this file |

## §7 Next exact commands (orchestrator, next session)

```bash
git fetch origin
git ls-remote --heads origin | grep -E 'codex/'                               # re-dispatched Phase 0 branch?
# D7 first: confirm the vendor bytes are gone from origin/codex/mym-breakout-research (or the ref is deleted):
git fetch origin && git ls-tree -r -l origin/codex/mym-breakout-research | awk '$4 > 1000000'   # expect empty
# When the re-dispatched Phase 0 PR exists: read its file list + CI, apply §4 G0.1–G0.10 as a diff read,
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
| 2026-09-03 | Second Codex pass on `459421b` — four P1 (shortlist multiplicity; pre-confirmation integrity check; one realized path is not a 5% test; holdout must be reserved before Phase 2) folded at `78c82de`; G0.10 added to the Phase 0 gate, still before any Phase 0 output was read | plan `REVIEW FOLDED ×2` |
| 2026-09-03 | Operator pushed `codex/mym-breakout-research` @ `706a03e`. Gate review: **FAIL** — G0.1 (no intake deliverables; zero strategies) and G0.3 (vendor bytes committed: raw export 67 MB, parsed panel 10 MB, trade ledger 23 MB — all three roots un-ignored on `main`). Base 68 commits behind `main`; its doc changes concern the `ORB-MYM-SCALE-1` vet intake and the three-speed spec, not this campaign | Phase 0 `FAIL`; D7 raised; `.gitignore` hardened in #273; §9 re-dispatch packet authored |
| 2026-09-03 | Codex review of #273 (`6ca5577`): six P1 + four P2 — eight bind the plan (folded at `e8694a9`), two bind this file (D1 merge order; D3 in iterations). §3/§4 corrected on verified source: engine inactivity is consecutive-idle-days vs the venue's calendar week; `cost_per_side_usd` is the index-micro row; `paired_blocks_from_daily` is single-series; `pair_tv_export_dataframe` raises on shorts; G0.2 gains the last-inspection field | plan `REVIEW FOLDED ×3` |

## §9 Phase 0 dispatch packet (Codex) — copy/paste after §6 D7 clears

```text
You are executing Phase 0 ONLY of docs/superpowers/plans/2026-09-02-seven-strategy-tradeify-select-configuration.md
(read it from disk at the current head of codex/plan-phases-for-tradeify-select-evaluation or main — whichever
carries commit e8694a9 or later; if neither does, stop and return NEEDS_CONTEXT). The acceptance gate you will be
judged against is §4 G0.1–G0.10 of docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md — read
it in full before writing anything.

PHASE-0 STALENESS CHECK (run first; stop with NEEDS_CONTEXT on any miss)
- git fetch origin && git log --oneline -1 origin/main ; branch from CURRENT origin/main, never from an old sandbox base.
- The seven strategy files and seven backtest exports are visible at the intake path the operator gives you.
  If fewer than 14 inputs are visible, return NEEDS_CONTEXT naming exactly which are missing. Do not substitute.

INTAKE DIRECTORY RULE (G0.3 — a miss is FAIL and a public-repo breach)
- Stage every input under lab/analysis/c1/seven_strategy_select_config_2026-09/inputs/ . That path is gitignored for
  *.csv and *.pine by the repository's standing rules. Never write inputs under workspace_inputs/, workspace_outputs/,
  or any other root; never `git add -f`; before committing run `git ls-tree -r -l --cached HEAD | awk '$4 > 1000000'`
  and `git status --short | grep -E '\.(csv|pine)$'` — both must be empty.
- The manifest carries SHA-256, byte size, row count, first/last timestamp for every input. Hashes, never bytes.

DELIVERABLES (all four, or the phase is not complete)
1. INTAKE.md — one section per strategy with every plan Phase 0 field, including: final design-decision date,
   last result-inspection date (UNKNOWN allowed, never guessed), direction, and whether synchronized intraday bars
   or timestamped intratrade paths exist. Label each strategy decision-grade-capable or LOWER BOUND-capable.
2. intake_manifest.json — machine-readable mirror of (1) plus input hashes and the loader used per input.
3. DISCREPANCIES.md — every strategy-file ↔ export mismatch (symbol, session, quantity convention, gross/net,
   commission/slippage settings); if none, list the checks run.
4. The reserved-window record (G0.10): the derived confirmation boundary per strategy (later of the two dates),
   the quarantined confirmation files under inputs/reserved/ with their hashes, and a loader-assertion test proving
   Phase 1–6 code cannot open them.

LOADERS (G0.4): long-only TV trade exports through core/tv_export_loader.py; bars through scripts/parse_bar_export.py.
A short or two-sided export is recorded LOADER-BLOCKED with a hand-paired fixture; do not write an alternative parser.

CONTAMINATION RECORD (G0.6): for each strategy, state development/tuning overlap with the export AND whether it belongs
to a family already studied in this repository (lab/analysis/mym_breakout_entry_2026_09/ consumed its 2025→2026-07
holdout; lab/analysis/orb/orb_mym_volume_gate_2026-09-02/ is fully viewed). A consumed interval cannot be reserved.

FORBIDDEN (any one is FAIL)
- Ranking, ordering, or comparing strategies by return/PF/drawdown; scoring any payoff cell; any Monte Carlo run.
- Computing any P&L, drawdown, cadence, or trade statistic on the reserved (confirmation) segment.
- Editing STATE.md, docs/SESSIONS.md, any ADR, the plan, or the campaign-state artifact (orchestrator-only).
- Repairing or "cleaning" source rows; inferring EOD-safe ⇒ intraday-safe.

RETURN CONTRACT
- Register the study directory in lab/CATALOG.md; add __init__.py if tests ship; run
  `python scripts/gate_manifest.py --tier pre-commit` and paste its exit code.
- Open a PR from a fresh codex/* branch off current origin/main, titled
  "research(c1): seven-strategy Select — Phase 0 intake". First line of the description:
  `PHASE0 <DONE|DONE_WITH_CONCERNS|NEEDS_CONTEXT|BLOCKED> — $0 · K=0 · MC=none — <one-clause outcome>`.
```
