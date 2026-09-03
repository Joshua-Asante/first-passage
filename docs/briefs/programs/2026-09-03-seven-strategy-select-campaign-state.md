# Seven-strategy Select configuration campaign — campaign state (orchestrator-only writes)

**Status:** `PHASE 0 SKIPPED (operator override) · PHASE 1 IN PROGRESS — Task 4/8 on origin (4c186e7), incremental gate read; G1.6 FINDING RELAYED (force-flat = daily 16:45 ET, not weekends only) · D8 + D9 RESOLVED (native editions w/ pyramid down; America/New_York), Codex config re-freeze pending · PLAN + THIS FILE ON MAIN (#272, #273 merged) · STATE QUEUE #1 (D2/D4 resolved — PR #275) · OLD VENDOR-BYTE REF DELETED, OBJECT PURGE PENDING (§6 D7)`
**Last curated:** 2026-09-03 (orchestrator session `claude/orchestrator-role-takeover-yza7vp`; queue-placement reconciliation by `claude/state-pipelines-alignment-ng62y9`, PR #275)
**Parent plan:** [`2026-09-02-seven-strategy-tradeify-select-configuration.md`](../../superpowers/plans/2026-09-02-seven-strategy-tradeify-select-configuration.md)
(PR [#272](https://github.com/Joshua-Asante/first-passage/pull/272) — **merged 2026-09-03** together
with #273; four Codex passes `459421b`, `78c82de`, `e8694a9`, `6aa7ff8`, the operator's ruling and
override `11d22e2`, and the Phase 7 simplification `1fe4600` are all on `main`).
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
| Plan | Codex review folded; operator merge | **MERGED** (#272 + #273, 2026-09-03) | operator | `main` @ `5eff0ec` |
| 0 — Receive and inventory | — | **SKIPPED** (operator override 2026-09-03), after the first return (`codex/mym-breakout-research` @ `706a03e`) failed the gate: no intake, ~100 MB vendor bytes. Inventory duties fold into Phase 1 (G1.2) | — | §8 ledger |
| 1 — Normalize and reproduce (+ folded Phase 0 inventory) | §4 Phase 1 gate G1.1–G1.10, verdict `PASS` | **IN PROGRESS** — `codex/tradeify-stage1-normalization` @ `4c186e7` (base `11d22e2`, 35 behind `main`) carries **Task 4 of 8** (identity + strict normalization + reconstruction/accounting + venue audit; 55 tests). Incremental gate read 2026-09-03: G1.1 ✓ · G1.5 ✓ · G1.8 ✓ · G1.4 tolerances pre-committed ✓ · G1.3 partial (no repair path on synthetic tests — orphans, duplicates, identity mismatches are blockers; the canonical ledger, its mandated fields, and the committed ledger hash await the runner) · **G1.6 red — force-flat modeled as Friday-to-Sunday only; the venue rule is a daily 16:45 ET deadline (§4 note)** · G1.2 partial (D8/D9 not yet applied: `source_timezone` still `null`, prototypes' intent unflipped, no pyramid field) · G1.7 partial (adapter + block builder are Task 5) · **G1.9 red — study dir not in `lab/CATALOG.md`** · G1.10 pending. No PR yet | Codex → orchestrator review | §8 ledger, §9 |
| 2 — Standalone quality (joint-book limbs moved to Phase 4, after the freeze) | eliminations recorded with reasons on standalone evidence; no portfolio result computed | QUEUED | Codex + orchestrator | — |
| 3 — Freeze search + validation design | pre-registration committed **before** any Phase 4 run; **all 14 contract items** frozen (1–9 numeric; 10 multiplicity; 11 `N_conf`; 12 Phase 6 severities; 13 Rule 2 iterations; 14 the seven per-template candidate contracts); operator ratifies | QUEUED (orchestrator authors; `pre-ratification-adversarial-panel` before ratification) | orchestrator → operator | — |
| 4 — Joint-book audit + deterministic screen (development segment only) | trial ledger complete incl. failures | QUEUED | Codex / local | — |
| 5 — Coarse joint MC (joint-flat weekly blocks over the export) | frontier kept; checkpoints resumable | QUEUED | local compute | — |
| 6 — Robustness / falsification | every listed challenge run; failures typed | QUEUED | local compute | — |
| 7 — Locked confirmation | per slot: selection-inclusive outer bootstrap at the `1 − α/M` quantile **and** the worst Phase 6 partition both < 5%, forward-interval falsifier not tripped; per-candidate verdicts in terminal-taxonomy vocabulary; else `no qualifying configuration` | QUEUED | orchestrator adjudicates | — |
| 8 — Shadow-operational | dry-run parity through the c1 sizing/rule path; M1 + operator GO stay separate | QUEUED | c1-rail lane | — |

Findings label vocabulary (plan): `EXPLORATORY` · `CONFIRMATORY` · `BLOCKED` — **nonterminal
evidence labels** for this artifact only; terminal per-candidate verdicts use the
[terminal taxonomy](../../adr/2026-08-30-terminal-taxonomy.md) (`CONFIRMED` / `MARKET-NULL` /
`EXPRESSION-FAIL` / `EVIDENCE-VOID`) and the book-level `no qualifying configuration`. **No
finding of any label exists yet.** Nothing numerical may be carried forward without its provenance tuple
(code commit · input hashes · config hash · seed range · environment · output hash).

## §3 Canonical authorities — reuse, never re-implement

The plan's one-simulator rule ("do not let three assistants create three incompatible
simulators") binds to these existing owners. A worker PR that re-derives any of them is
`REFUTED` at review regardless of its numbers.

| Concern | Owner (read before writing) | Note |
|---|---|---|
| Venue rules snapshot | [`core/firm_rules.py`](../../../core/firm_rules.py) `FIRM_RULES["Tradeify_Select_100K"]` — `trailing_locking`, 3.0% EOD trailing DD, 6.0% target, min 3 trading days, `inactivity_max_idle_days: 5` (venue fact: ≥1 trade per Mon–Fri week), micro cap 80, `cost_per_side_usd` 0.91 (**index-micro row only** — MNQ/MYM/MES/M2K; the same file prices MGC at 1.06), 40% consistency, `weekend_holds: False`, `dd_lock_offset_usd` unreachable (fixed 2026-08-04) | Phase 0's primary-source capture must reconcile to this snapshot; any delta is a **venue-fact** correction under Rule 13, filed by the orchestrator, never patched in a worker branch. **Two caveats bind workers:** (a) fees resolve **per instrument** through the hashed Tradeify commission table Phase 1 delivers from the venue's published schedule — [`lab/discovery/cost_model.py`](../../../lab/discovery/cost_model.py) `resolve_commission` deliberately **raises** for every non-index micro and its specs hold tick geometry, so it is not the resolver — never the tier scalar; (b) the engine's `inactivity_limit` counts *consecutive idle business days* (`simulate_path`), while the venue clock is calendar-week — a **calendar-week adapter** is a Phase 1 deliverable and the only clock admitted in Phase 5 (divergence already flagged in `SESSIONS 2026-09-02c`) |
| Path engine + clocks | [`core/mc/simulation.py`](../../../core/mc/simulation.py) `simulate_path` (`intraday_low` optional → honest clock; absent → EOD lower bound), `HORIZON_CAP = 1500`, `horizon_cap` outcome for unresolved paths; [`core/mc/preflight.py`](../../../core/mc/preflight.py) firm kwargs; [`core/dd_geometry.py`](../../../core/dd_geometry.py) | Unresolved paths count as busts in every safety statistic (plan contract item 5) |
| Survivor scoring + week blocks | [`lab/discovery/prop_survivor_scoring.py`](../../../lab/discovery/prop_survivor_scoring.py) (`run_tier_remc`, `paired_blocks_from_daily`, `score_part_a`; thresholds parsed from the frozen prereg, never restated) | `paired_blocks_from_daily` is **single-series** (synthetic business-day index, `(n_weeks, 5, 1)`) — precedent, not tool; the multi-strategy, real-timestamp joint block builder with joint-flat assertions is a Phase 1 deliverable (plan Phase 3) |
| Single-series / composed scoring | [`lab/research_utils/nsurv_channel.py`](../../../lab/research_utils/nsurv_channel.py) `score_nsurv` · [`book_score.py`](../../../lab/research_utils/book_score.py) `score_book` | "computes, does not admit" |
| TV trade-list adapter + honesty label | [`lab/research_utils/msl_score.py`](../../../lab/research_utils/msl_score.py) (`LOWER BOUND` vs `excursion-bounded`) | The plan's `LOWER BOUND` rule is this label, not a new one |
| Loaders | [`core/tv_export_loader.py`](../../../core/tv_export_loader.py) (paired trades, MAE/MFE columns) · [`core/bar_export_loader.py`](../../../core/bar_export_loader.py) / [`scripts/parse_bar_export.py`](../../../scripts/parse_bar_export.py) (BAR EXPORT v0.2 + sidecar) | No ad-hoc CSV interpretation (G0.4). `pair_tv_export_dataframe` **raises on non-long entries** (the locked book is long-only): a short or two-sided export needs the loader extended — `core/` is a locked surface, so that extension is CC-solo under ADR test 1, never a worker patch |
| Two-level bootstrap precedent | [`lab/analysis/c1/class_s_w1_bootstrap_honest_2026-09-02/`](../../../lab/analysis/c1/class_s_w1_bootstrap_honest_2026-09-02/) (`_boot_paired.py`, `READING.md`) | The plan's Phase 7 qualifying bound is this design |
| Eval bust ceiling of record | [`prop-survivor-scoring prereg v2`](../pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md) §3 Part A: bust ≤ 5.0% | Plan's 5% aligns; the 2026-07-22 §4-withdrawal ADR §5 collision flagged in `SESSIONS 2026-09-02c` is still **unruled** (§6 D5) — a `Proposed` ruling now exists at [Addendum 2026-09-03](../../adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md#addendum-2026-09-03--the-50-ceiling-does-not-re-admit-candidate-1-proposed), and the collision is sharper than first logged: **all four** frozen tiers (3.51 / 4.74 / 4.25 / 4.44) clear 5.0%, so the raise re-admits candidate #1 by arithmetic |
| Candidate / campaign governance | [`candidate-contract`](../../adr/2026-08-30-candidate-contract.md) · [`evaluation-order`](../../adr/2026-08-30-evaluation-order.md) · [`operator-approvals-campaign-envelope`](../../adr/2026-08-30-operator-approvals-campaign-envelope.md) · [`terminal-taxonomy`](../../adr/2026-08-30-terminal-taxonomy.md) · [`tradeable-reachable-gate`](../../adr/2026-08-30-tradeable-reachable-gate.md) | Terminal wording in this campaign uses the taxonomy's vocabulary |
| Deployment gates (Phase 8 and beyond) | [`M1`](../../adr/2026-07-22-c1-venue-native-monitoring-maturity.md) · [`rail GO`](../../adr/2026-07-17-c1-rail-build-account-registration-go.md) | Untouched by this campaign |

## §4 Phase gates

**Phase 0 gate (G0.1–G0.10)** — frozen 2026-09-03, applied once (verdict `FAIL`, §8), then
superseded the same day by the operator's Phase 0 skip. Its text is retrievable from this file's
history at `f0bc2ac`; the inventory checks it carried now live in G1.2.

**Phase 1 acceptance gate — FROZEN 2026-09-03 before any Phase 1 output was read.** Applied by the
orchestrator to Codex's Phase 1 PR as a diff-plus-CI read, never opening vendor bytes. Verdicts:
**`PASS`** (Phase 2 unlocked) · **`NEEDS_CONTEXT`** (one re-anchor round for cheap missing items) ·
**`FAIL`** (Phase 1 re-run).

| # | Check | Verdict on miss |
|---|---|---|
| G1.1 | **No vendor bytes committed.** The seven attachments and the row-level ledger stay local/gitignored; the PR commits implementation, tests, SHA-256 of every source and of the canonical ledger, and aggregate reconciliation reports only. `git ls-tree -r -l` on the head shows no file > 1 MB and no `*.csv` under a non-ignored path. | `FAIL` |
| G1.2 | **Folded Phase 0 inventory** per strategy: source hash, byte size, row count, first/last timestamp, instrument, direction, session, bar size, quantity convention, gross/net, exported commission/slippage settings, **export timezone resolved** — operator ruled `America/New_York` for all seven (§6 D9); a config still carrying `null` caps the Phase 1 verdict at `NEEDS_CONTEXT`, since the plan's Phase 1 ledger is canonical UTC with exchange-local session dates, and whether synchronized intraday bars or timestamped intratrade paths exist — scalar MAE/MFE is inventory only. | `NEEDS_CONTEXT` |
| G1.3 | **Strict ingestion:** duplicate, missing, or malformed legs flagged, never repaired; the canonical event ledger keeps source timestamps, prices, quantities, P&L, commissions, MAE/MFE, row hashes, and a deterministic event order; ledger hash committed. | `FAIL` on any silent repair |
| G1.4 | **Seven reconciliation reports** against each source report (trade count, net P&L, win rate, profit factor, drawdown, commissions, monthly totals) with tolerances **committed before reconciliation ran**; a material mismatch blocks that strategy. | `FAIL` if tolerances post-date the run |
| G1.5 | **Per-instrument commission table** delivered and hashed; every non-index micro (MGC included) carries an explicit basis — the index-micro `$0.91/side` row is never substituted. | `NEEDS_CONTEXT` |
| G1.6 | **Venue-legality flags, not repairs:** weekend/overnight holds (Codex named three ORB-MNQ weekend trades at dispatch), contract-cap and session-boundary breaches are flagged as Phase 2 blockers, never altered. | `FAIL` if altered |
| G1.7 | **Tests first, all present:** strict pairing, money parsing, timezone handling, stable timestamp ordering, tick alignment, cost resolution, position overlap, force-flat violations, deterministic output — plus the calendar-week inactivity adapter and the multi-strategy joint block builder (plan Phase 1 deliverables), or an explicit deferral of those two to Phase 3 with the reason. | `NEEDS_CONTEXT` |
| G1.8 | **Labels and scope:** every result `EXPLORATORY`; no ranking, cross-strategy comparison, composition, Monte Carlo, or Pine re-run — reproduction of the exports' accounting and event structure only. | `FAIL` on any ranking or scoring |
| G1.9 | **Repo integration:** study directory under `lab/analysis/` (Codex named `tradeify_seven_strategy_phase1_2026-09`) registered in [`lab/CATALOG.md`](../../../lab/CATALOG.md); `__init__.py`; `python scripts/gate_manifest.py --tier pre-commit` exit 0 pasted; required check `skills (3.12)` green. | `NEEDS_CONTEXT` |
| G1.10 | **Rule 2 line** in the PR description: `$0 · K=0 · MC=none` and the iteration count consumed against constituent (i) of plan contract item 13. | `NEEDS_CONTEXT` |

**Gate interpretations recorded on the `4c186e7` read (orchestrator, 2026-09-03). The frozen rows above are
unchanged; these bind how two of them are applied:**

- **G1.6 — "force-flat" is the venue's daily deadline, not weekends.** The repo's venue record is a **daily
  16:45 ET flat deadline** (12:59 ET holiday-short; session 18:00 ET → 16:45 ET next day across the
  17:00–18:00 ET maintenance break; auto-flatten non-fatal, slippage only) — `core/firm_rules.py` Tradeify
  comment block (re-verification pass 2026-07-22, articles 10495876 + 12268167) and
  [`ops/prop_envelope_default.md`](../../../ops/prop_envelope_default.md) E1 + Tradeify row; `weekend_holds:
  False` is that rule's engine field name. Codex's spec §4.4 and `analyze_venue` (`4c186e7`) emit
  `FORCE_FLAT_VIOLATION` (BLOCKER) only for Friday-to-Sunday holds and `CROSS_DATE_HOLD` (WARNING) for every
  other date change. Under the venue rule every hold spanning a 16:45 ET instant is a position the venue
  would have flattened — the export's exit for that trade is one the venue could never have produced — so it
  is a Phase 2 blocker for that strategy (G1.6: "weekend/overnight holds … session-boundary breaches"). A
  naive cross-date test is also the wrong proxy: 15:00 → 18:30 ET same date spans the deadline; 23:00 →
  01:00 ET does not. With D9 resolved the exact test is cheap: localize to `America/New_York` and flag any
  trade with a 16:45 ET instant in `(entry, exit]`; keep `friday_to_sunday_holds` as a sub-count. For the
  12:59 ET holiday-short deadline, capture the CME early-close calendar over the export span from a primary
  source as a hashed campaign-local file (the commission-schedule pattern; Rule 13) and apply 12:59 ET on
  those dates — until that capture lands, this dimension **caps the Phase 1 verdict at `NEEDS_CONTEXT`**,
  since an unmodeled early close could pass a session-boundary breach into Phase 2. Spec anchor §7.7 ("exactly three ORB-MNQ force-flat violations") becomes a **sub-count anchor** and
  must be re-frozen before the runner runs — still a pre-commitment, since no run exists.
- **G1.4 / G1.5 — "commission mismatch" is export-implied vs venue schedule.** Aegis 6J1's Pine declares
  `$1.30`/side but the export was produced at `$3.10`/side, which **matches** the venue row (6J `$6.20`
  round trip). Under the whole-export-viewed ruling the export is the object; the Pine default it did not
  run with is provenance. So `EXPORT_VENUE_COMMISSION_MISMATCH` stays a BLOCKER, while
  `PINE_EXPORT_COMMISSION_MISMATCH` / `PINE_VENUE_COMMISSION_MISMATCH` are inventory (WARNING) whenever the
  export-implied fee matches the venue. At `4c186e7` all three default to BLOCKER and spec §4.6 rolls the
  most severe status up, which would block Aegis at Phase 1 for a default it never ran with. Operator may
  veto this reading.

## §5 Claim manifest

| Item | Holder | Status | PR / commit | Note |
|---|---|---|---|---|
| Campaign plan | Codex (operator task) | **REVIEWED** — three passes folded | #272 @ `e8694a9` | pass 1: six P1 + one P2 (Phases 0/3/4/5/7, contract items 3/5/8/9); pass 2: four P1 (multiplicity `α`/`M`/procedure, pre-confirmation integrity check, one-path falsifier semantics + `N_conf`, holdout reserved at intake — contract items 10/11, Phases 0/1/2/7); pass 3 (Codex review of #273): eight plan-binding findings — last-inspection date, selection-inclusive outer bootstrap, Phase 2 standalone-only, numeric Phase 6, calendar-week inactivity adapter, joint block builder, per-instrument fees, Rule 2 in iterations (contract items 12/13); three reconciliation tables in the plan |
| Orchestrator takeover; this file; Phase 0 gate | orchestrator session 2026-09-03 | **MERGED** | #273 @ `5eff0ec` | gate frozen before any Phase 0 output was read; superseded by the Phase 1 gate the same day |
| Phase 0 intake (first return) | Codex, `codex/mym-breakout-research` @ `706a03e` | **RETURNED — FAIL** (G0.1, G0.3); phase then **SKIPPED** by operator override | no PR | pushed by the operator 2026-09-03: one commit on a base **68 commits behind `main`** (pre-dates PR #259's merge). Content: vet-intake notes for `ORB-MYM-SCALE-1` (`docs/notes/2026-09-01-orb-mym-scale-vet-intake.md`, `2026-09-02-next-vet-candidate-assessment.md`, a three-speed-spec paragraph) plus the raw TV bar export, the parsed `MYM_M15.csv`, and the 60-cell trade ledger. Not a seven-strategy intake |
| Phase 0 gate review | orchestrator | **DONE — `FAIL`** (this session) | — | §4 applied as a diff read; vendor files were opened only to two header lines each for content-class identification, no statistic computed |
| Phase 0 re-dispatch packet | orchestrator | **SUPERSEDED** — Phase 0 skipped | — | replaced by the §9 Phase 1 dispatch record |
| Phase 1 normalization (+ folded inventory) | Codex, `codex/tradeify-stage1-normalization` @ `4c186e7` (base `11d22e2`) | **IN PROGRESS** — Task 4/8 on `origin` | no PR yet | Tasks 1–4 landed (identity, strict normalization, reconstruction + accounting, venue audit; 55 tests); Task 5 (joint ledger + calendar-week adapter), 6 (runner + reports), 7–8 remain; D8/D9 config re-freeze, the CATALOG row, and the G1.6 force-flat re-freeze still outstanding |
| Phase 1 gate review | orchestrator | **PARTIAL READS DONE** 2026-09-03 on `a51bc60` and `4c186e7`; full verdict when the runner, reports, and PR land | — | worktree re-run at `4c186e7`: 55/55 tests pass, `lab/discovery/cost_model.py` byte-unchanged, `check_boundaries` OK, CI composition (`--tier check`) red on `lab-catalog` only; one G1.6 finding and one G1.4 interpretation recorded in §4 |
| Campaign pre-registration (contract items 1–14 + seven candidate contracts; Phase 3 deliverable) | orchestrator authors → adversarial panel → operator ratifies | **QUEUED** | — | must exist before any Phase 4 run |
| Phases 1–8 | per §2 | **QUEUED** | — | — |

**Hashes:** the seven Pine and seven export SHA-256 pins are committed in `phase1_config.json` on `codex/tradeify-stage1-normalization` @ `a51bc60` and listed in the design spec §2; this session read the pins, never the bytes. Code commits reviewed: `a51bc60`, `4c186e7`. Config and ledger hashes: runner deliverables, not yet recorded. **Compute:** completed 0 · remaining
undetermined until §6 D3. **Defects / invalidations:** none; no prior output exists to invalidate.

## §6 Decisions requiring operator input

| # | Decision | Why it is the operator's | Orchestrator recommendation |
|---|---|---|---|
| D1 | Merge #272 / #273 | — | **Done 2026-09-03** — both merged; plan and this file on `main` |
| D2 | `STATE.md` queue placement | Queue cap ≤5, 2 rows live; promotion is an operator act (STATE standing rule: "do not auto-open a replacement") | **RESOLVED 2026-09-03** ([PR #275](https://github.com/Joshua-Asante/first-passage/pull/275)) — promoted to queue **#1** (not Row 3): the operator ruled this campaign the live/turning one, replacing the portable-edge cultivation row rather than adding a third. `#2` (B7-REFIRE/M1) unchanged |
| D3 | Rule 2 budget — confirm the classification | Rule 2 counts complete attempt-and-check iterations under the INNER/OUTER/STRATEGIC 3/8/3 limits ([canon §15](../../methodology/inqhiori-canon.md)); a core-hour figure is not a budget. Plan contract item 13 now proposes **STRATEGIC, ≤3 constituent OUTER investigations × 8 iterations, no self-extension** | Confirm item 13's three constituents; keep $0 external data and any core-hour figure as disclosure lines only. Phase 0 is iteration 1 of constituent (i) |
| D4 | Relation to queue row 1 (portable-edge cultivation, 2–3 day clock from 2026-09-02, ≤1 candidate contract, ≤3 seats) | Seven *supplied* strategies are complete expressions — the cultivation plan's seats B/C class — but the configuration search is a book-composition objective the cultivation envelope does not name | **RESOLVED 2026-09-03** (with D2) — ruled a **separate program** under its own envelope (this file), and per D2 now the higher-priority one: cultivation is demoted off-queue (stays open on its own ADR/plan, no queue row) |
| D5 | 5% ceiling vs 2026-07-22 §4-withdrawal ADR §5 | Flagged unruled in `SESSIONS 2026-09-02c`; Phase 7 cannot call a pass while the ceiling's own provenance is contested. **2026-09-03: a one-line ruling is now drafted and awaiting operator ratification** — [`withdrawal ADR` Addendum 2026-09-03](../../adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md#addendum-2026-09-03--the-50-ceiling-does-not-re-admit-candidate-1-proposed) (`Proposed`): the 5.0% ceiling is prospective-only and does not re-admit candidate #1. Still **unruled** until ratified, so D5 does not clear yet | Operator ratifies (or elects the opposite, which needs a superseding ADR) before Phase 3 ratification |
| D7 | **Purge the vendor bytes from the public remote** — **OPEN** | `706a03e` on the old `codex/mym-breakout-research` carried the raw TV bar export, the parsed `MYM_M15.csv`, and the local-only trade ledger. The ref is deleted (Cursor, 2026-09-03), but a deleted ref does not purge the objects: anyone holding the commit hash can still fetch them until GitHub removes or garbage-collects them | Request the unreachable-object purge from GitHub support; this row closes only when the purge is confirmed (the `706a03e` objects return 404) |
| D8 | **Two instrument mismatches** in the supplied set | `striker_dj30_mnq_prototype` (export on a MYM chart) and `striker_nas100_mym_prototype` (export on an MNQ chart) were declared on the other instrument, because Codex read the Q-TXG-1 sibling-swap target out of the Pine filenames | **Resolved 2026-09-03 (operator ruling): they are the native editions with the pyramid turned down** — DJ30 on MYM and NAS100 on MNQ, not the Q-TXG-1 swap cells. The exports are on the right chart; the declared intent and the names were wrong. Codex: flip `intended_instrument` to the export's chart (MYM, MNQ), rename the two IDs and lineage notes to say *native edition, pyramid reduced from the locked 750% / 1000% to the Pine's value* (a new expression, not the locked strategy), and add the Pine pyramiding setting to every config entry so the inventory records it. **Structural consequence:** each pyramid-down variant is a parameterization of the same entry/exit template as its locked sibling (`striker_dj30_mym_v45`, `striker_nas100_mnq_v1`), so per the candidate-contract ADR it is a **cell inside that template's contract**, not a separate template — the set holds **five templates**, and the configuration catalogue must treat each pyramid pair as a mutually exclusive cell choice, never two independent legs |
| D9 | **TradingView chart timezone** of the seven exports | Was `null` for all seven, which capped the Phase 1 verdict at `NEEDS_CONTEXT` (the plan's Phase 1 ledger is canonical UTC with exchange-local session dates) | **Resolved 2026-09-03 (operator ruling): `America/New_York` for all seven exports.** Codex sets `source_timezone` to `America/New_York` in every `phase1_config.json` entry (the config fingerprint changes), updates the test that currently asserts `source_timezone is None`, and the runner localizes with `zoneinfo` → UTC plus the exchange-local session date; DST-ambiguous or nonexistent timestamps stay hard errors (spec §4.2). The verdict cap lifts when the re-frozen config lands |
| D6 | The seven strategies' identities and the intake path | Plan §Immediate next action; only the operator holds the files | **Done 2026-09-03** — seven TradingView exports attached to Codex's local session; identities and hashes land through G1.2 |
| D10 | **`pine_filename` cited the locked names for two entries whose `pine_sha256` was already the modified body** | `striker_dj30_mym_pyramid_down` and `striker_nas100_mnq_v1` were exported from Pine files the operator had edited in place under the two locked-strategy filenames (`striker_dj30_v4.5_mym.pine`, `striker_nas100_v1_mnq.pine`); `phase1_config.json` recorded the correct modified `pine_sha256` but still cited the locked filename, not a distinct one — separate from D8 (that pair concerns `intended_instrument`/naming on the two Q-TXG-1-adjacent entries, not this citation) | **Done 2026-09-03** ([first-passage#286](https://github.com/Joshua-Asante/first-passage/pull/286)) — on the durable checkout, both locked files independently verified to still equal their existing `PORT_MANIFEST.sha256` pins (`bb921399…` NAS100 MNQ, `2b895317…` DJ30 MYM); no restore write needed, locked pins unchanged. Each modified body was reconstructed byte-exact from the restored locked file by applying only the single parameter edit its lineage note already described, verified equal to the already-recorded `pine_sha256`, then saved under a new filename and hash-pinned as a research variant (`striker_nas100_v1_mnq_dow_wed_excluded.pine`, `striker_dj30_v4.5_mym_pyramid_250.pine`). `phase1_config.json`'s two `pine_filename` fields now cite those variant names (`pine_sha256` unchanged); both variants confirmed present under the new basenames in the operator's `--source-dir`, and `verify_source_pair` re-run 7/7 clean against it |

## §7 Next exact commands (orchestrator, next session)

```bash
git fetch origin && git log --oneline origin/main..origin/codex/tradeify-stage1-normalization   # new Task commits?
# When the Phase 1 PR exists: apply §4 G1.1–G1.10 as a diff read (never open vendor bytes). In a worktree of
# its head run `python scripts/gate_manifest.py --tier check` and the four Phase 1 test modules, then check the
# committed reconciliation manifest against the spec §7.5–7.7 anchors frozen at a51bc60 (row/trade counts,
# net P&L to the cent, exactly three ORB-MNQ force-flat violations).
# ⚠ §7.7 is a Friday-to-Sunday SUB-COUNT once the daily 16:45 ET deadline is modeled (§4 note) — Codex re-freezes
# it before the runner runs; the violation total is whatever the deadline test yields.
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
| 2026-09-03 | Fourth Codex pass (re-review of #273 at `7edebae`): six P1 + two P2 — five bind the plan (`6aa7ff8`: per-template candidate contracts, per-slot bootstrap bounds, fee table, atomic confirmation read, terminal vocabulary), three bind this file (Phase 3 gate = all items; Phase 7 quantile; handoff labels nonterminal) | plan `REVIEW FOLDED ×4` |
| 2026-09-03 | **Operator ruling:** all seven strategies treated as tuned and viewed on the whole export → confirmation forward-only, historical results model-fitted; per-strategy dates and intake-time reservation dropped (plan `11d22e2`) | simplification |
| 2026-09-03 | **Operator override:** Phase 0 skipped; Phase 1 dispatched to Codex on local worktree `codex/tradeify-stage1-normalization` (base `e8694a9`) with the seven attached exports; §4 Phase 1 gate frozen before any output was read; §9 packet superseded by the dispatch record | Phase 1 `IN FLIGHT` |
| 2026-09-03 | Remote-ref deletion attempted per operator instruction — HTTP 403 from this session's git credential; operator to delete | D7 open |
| 2026-09-03 | **Operator ruling (D9):** the TradingView chart timezone is `America/New_York` for all seven exports. Codex re-freezes `source_timezone` in `phase1_config.json` and the asserting test; the Phase 1 verdict cap lifts on that push | D9 resolved |
| 2026-09-03 | **Operator ruling (D8):** the two "prototype" exports are the **native editions with the pyramid turned down** (DJ30 on MYM, NAS100 on MNQ), not Q-TXG-1 swap cells — exports are on the correct chart; declared intent and names were wrong. Codex flips `intended_instrument`, renames IDs/lineage, adds the Pine pyramiding field. Consequence: five templates, not seven (each pyramid variant is a cell of its locked sibling's template); plan contract item 14 and Phase 3/7 wording corrected in this PR | D8 resolved |
| 2026-09-03 | #272 and #273 merged; old vendor-byte ref deleted (Cursor); orchestrator branch restarted from `main` | plan + this file on `main`; D1 done; D7 stays open until the object purge is confirmed |
| 2026-09-03 | Codex pushed `codex/tradeify-stage1-normalization` @ `a51bc60` (5 commits on `11d22e2`): operator-approved design spec, 8-task plan (0/49 steps checked), `phase1_config.json` — seven strategies (Aegis 6J1 short-only; ORB-MNQ recon v7; Striker DJ30 MNQ-prototype and MYM v4.5; Striker NAS100 MNQ v1 and MYM-prototype; Vanguard MGC v0.4), hashes, tz `null`, intraday-path `false`, two intended-vs-encoded instrument mismatches — primary-source Tradeify fee capture (6J 6.20 / MNQ 1.82 / MYM 1.82 / MGC 2.12 round trip), `tv_trade_ledger.py` (identity + fee loader), 6 tests. **Partial gate read:** G1.1 ✓ (no vendor bytes; `local_artifacts/` ignored; basenames + SHA-256 only); G1.5 ✓; G1.8 ✓ (loader rejects any claim class but `EXPLORATORY`); G1.4 tolerances pre-committed ✓ (spec §5); G1.2 partial (counts/bounds await the runner — spec §7.5–7.6 pre-commits row/trade counts and net P&L to the cent, verifiable later); G1.7 partial (6 tests; adapter + block builder designed); **G1.9 red** (`lab-catalog`: study dir absent from `lab/CATALOG.md`); G1.3 / G1.6 / G1.10 pending. Worktree re-run: 6/6 tests pass, boundaries OK, 6J tick value 12.5M × 0.0000005 = $6.25 confirmed. **Verdict: IN PROGRESS, not a Phase 1 return** | Phase 1 `IN PROGRESS`; D8, D9 raised |
| 2026-09-03 | Codex review of #273 (`6ca5577`): six P1 + four P2 — eight bind the plan (folded at `e8694a9`), two bind this file (D1 merge order; D3 in iterations). §3/§4 corrected on verified source: engine inactivity is consecutive-idle-days vs the venue's calendar week; `cost_per_side_usd` is the index-micro row; `paired_blocks_from_daily` is single-series; `pair_tv_export_dataframe` raises on shorts; G0.2 gains the last-inspection field | plan `REVIEW FOLDED ×3` |
| 2026-09-03 | Both #272 and #273 confirmed merged (D1 resolved). Separate session ([PR #275](https://github.com/Joshua-Asante/first-passage/pull/275)) reconciled `STATE.md`'s queue with this campaign: promoted to queue **#1** (D2 resolved — not Row 3, replaces the cultivation row); D4 resolved with it (separate program, now the higher-priority one; cultivation demoted off-queue). `PIPELINES.md`'s P1/P4 dispositions corrected to name this campaign with the same links. Flagged by Codex review as a stale-artifact P2 finding on #275, then fixed here in the same pass | queue placement `RESOLVED` |
| 2026-09-03 | Codex pushed `codex/tradeify-stage1-normalization` @ `4c186e7` (Task 4/8: venue audit — separate commission bases, tick grid, exposure bounds under both tie orders, holds, roll/spread status; 55 tests). Incremental gate read: no vendor bytes, `cost_model.py` byte-unchanged, no orchestrator-surface edits, CI red on `lab-catalog` only. **G1.6 finding:** force-flat modeled as Friday-to-Sunday only vs the venue's daily 16:45 ET deadline (`firm_rules.py` re-verification 2026-07-22; `prop_envelope_default.md` E1) — spec §4.4, anchor §7.7, code and test to be re-frozen before the runner. **G1.4 interpretation:** Pine-default-vs-export commission codes are inventory when the export matches the venue (Aegis `$3.10`/side). Task 5 to carry micro-equivalent quantities for the account-aggregate cap. D8/D9 config re-freeze and the CATALOG row still pending | Phase 1 `IN PROGRESS`; findings relayed via operator prompt |
| 2026-09-03 | Codex review of [#279](https://github.com/Joshua-Asante/first-passage/pull/279) (`83b17e9`): three P2 — (i) the 12:59 ET holiday-short deadline cannot stay an unmodeled dimension under G1.6 → capture the CME early-close calendar as a hashed primary-source file, and until then it caps the Phase 1 verdict at `NEEDS_CONTEXT`; (ii) per-strategy contract-cap breaches stay Phase 1 blockers (only the joint cap verdict waits for Phase 4); (iii) G1.3 is partial until the canonical ledger and its committed hash exist. All three folded in the same PR | plan unchanged; §2/§4/§9 corrected |
| 2026-09-03 | **D10 raised and resolved same-day** (separate Claude Code session, `first-passage#286`): the two locked Striker futures venue editions had been edited in place on the operator's machine under their locked filenames to produce two of the seven exports. Durable-checkout verification found both locked files already equal their `PORT_MANIFEST.sha256` pins (no restore write needed); the modified bodies were reconstructed byte-exact from the restored locked files by applying only the single parameter each entry's lineage note already named, confirmed equal to the already-recorded `pine_sha256`, and pinned under new filenames as research variants. `phase1_config.json`'s two `pine_filename` fields repointed to those variants in this PR; `verify_source_pair` re-run 7/7 clean against the operator's `--source-dir` | D10 resolved |

## §9 Phase 1 dispatch record (Codex, operator-relayed 2026-09-03)

Codex's declared Phase 1 design, as relayed by the operator (worker claims, not yet verified — the
§4 gate is the verification):

- dedicated campaign `tradeify_seven_strategy_phase1_2026-09`; strict ingestion of all seven
  TradingView exports, no silent repair of duplicate/missing/malformed legs;
- canonical event ledger with source timestamps, prices, quantities, P&L, commissions, MAE/MFE, row
  hashes, deterministic order; per-strategy reconciliation on trade count, net P&L, win rate, profit
  factor, drawdown, commissions, monthly totals;
- validation of instrument, tick/point conversion, overlapping positions, contract caps, partial
  exits, pyramiding, timestamp collisions, weekend/overnight holds — the **three ORB-MNQ weekend
  trades flagged as venue-rule blockers**, not altered;
- UTC/session-date fields left `UNRESOLVED` while the export timezone is unknown; explicit MGC
  commission basis required, no index-micro substitution; scalar MAE/MFE inventory-only;
- every result `EXPLORATORY`; reproduction of the exports' accounting and event structure only (no
  Pine re-run — the attached set lacks the TV execution engine and complete bar inputs);
- tests first: pairing, money parsing, timezone, ordering, tick alignment, cost resolution, overlap,
  force-flat, determinism; attachments and the row-level ledger kept local/gitignored, with
  implementation, tests, source hashes, aggregate reports, and the ledger hash committed.

Orchestrator read at dispatch: G1.1, G1.3, G1.4, G1.5, G1.6, G1.8 are declared; G1.2's timezone
row is declared `UNRESOLVED` (acceptable with the consequence stated); G1.7's calendar-week
inactivity adapter and joint block builder are **not** declared — expect one `NEEDS_CONTEXT`
re-anchor or an explicit deferral to Phase 3.

Orchestrator read at `a51bc60` (Task 1 of 8, 2026-09-03): the identity boundary and fee capture are
as declared. G1.7's two designed deliverables (calendar-week adapter, joint block builder) are in
the spec §4.5, so the anticipated re-anchor is withdrawn. Outstanding before a full gate:
`trade_reconciliation.py`, `joint_trade_blocks.py`, `run_phase1.py`, README, the runner tests, the
seven aggregate reports and ledger hashes, the `lab/CATALOG.md` row (**add it by hand** —
`archive_lab_analysis.py --regenerate-catalog` also rewrites other rows' heavy-column notes), a
merge of `main` (the branch is 24 commits behind), and a PR whose first description line carries
the Rule 2 line. One operator input stays open on the source set itself: §6 D8 (instrument
mismatches). D9 (chart timezone) is resolved — `America/New_York` — and is now an implementation
follow-up for Codex, not an operator escalation.
**D9 resolved 2026-09-03:** chart timezone `America/New_York` for all seven — Codex's next push should
carry the re-frozen config (all seven `source_timezone` set), the updated identity test, and UTC /
session-date columns populated by the runner.
**D8 resolved 2026-09-03:** the two prototypes are native editions with the pyramid turned down. Codex's
next push should also flip their `intended_instrument` (DJ30 → MYM, NAS100 → MNQ), rename the IDs and
lineage notes accordingly, and add `pine_pyramiding` (the Strategy Properties value) to all seven
entries. With that, the set is **five templates**: Aegis 6J1; ORB-MNQ recon v7; DJ30-MYM {locked
750%, pyramid-down}; NAS100-MNQ {locked 1000%, pyramid-down}; Vanguard MGC v0.4.

**Orchestrator read at `4c186e7` (Task 4 of 8, 2026-09-03, incremental):** one commit on `fe35529` —
`analyze_venue` + `VenueMetrics` in `trade_reconciliation.py` (Pine / export-implied / venue commission
bases kept separate; tick-grid check against `INSTRUMENT_SPECS` plus campaign-local 6J geometry;
peak-open-quantity bounds under both tie orders vs `contract_cap`; cross-date and Friday-to-Sunday holds;
`CONTINUOUS_CONTRACT_ROLL_UNRESOLVED` for every `1!` symbol; spread `NOT_SEPARATELY_OBSERVABLE`) and 16
new tests. Worktree: 55/55 pass; `lab/discovery/cost_model.py` byte-unchanged (spec §7.2 ✓); no vendor
bytes; no orchestrator-surface edits; CI composition red on `lab-catalog` only. Findings, all cheap before
the runner exists: (1) **G1.6** force-flat definition (§4 note) — spec §4.4, anchor §7.7, `analyze_venue`,
and the test `test_cross_date_hold_is_reported_without_force_flat_false_positive` all encode weekends-only;
(2) **G1.4 interpretation** — Pine-vs-export/venue commission codes are inventory, not blockers, when the
export-implied fee equals the venue's (§4 note); (3) **Task 5 carry-forward** — the Tradeify cap is
**account-aggregate**, counted 10 micros = 1 mini (`firm_rules.py` comment; article 12268167), so the joint
ledger should carry `micro_equivalent_quantity` per event (6J = 10; MNQ/MYM/MGC = 1). The per-strategy check
already in `analyze_venue` (`CONTRACT_CAP_BREACH` against the 80-micro-equivalent account cap) stays a Phase 1
blocker — a single strategy over the account cap on its own is unconditionally illegal; only the **joint**
(book-level) cap verdict waits for Phase 4; (4) `VenueMetrics.overnight_holds` is assigned the cross-date count — after (1) it
should be the deadline-spanning count. Still outstanding from the `a51bc60` read: D9 `source_timezone`
(all seven still `null`), D8 intent flip / renames / `pine_pyramiding`, the `lab/CATALOG.md` row (by hand),
a merge of `main` (35 behind), Tasks 5–8, and the PR with the Rule 2 line. Verdict unchanged:
**IN PROGRESS, not a Phase 1 return.**
