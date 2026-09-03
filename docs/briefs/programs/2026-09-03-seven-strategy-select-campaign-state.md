# Seven-strategy Select configuration campaign — campaign state (orchestrator-only writes)

**Status:** `PHASE 0 SKIPPED (operator override) · PHASE 1 RETURNED — PR #283 @ 809bbb4, GATE VERDICT NEEDS_CONTEXT; #283 MERGED BY THE OPERATOR (39530d4, 17:12Z) BEFORE THE RE-ANCHOR ROUND — FOLLOW-UP CODEX PR PENDING (TWELVE RE-ANCHOR ITEMS + D13 ROLL DISPOSITION; G1.3/G1.4 BACK TO PARTIAL AFTER CODEX'S RE-REVIEW OF #284) (one re-anchor round: Striker source identities vs repo pins — D10; CME early-close rows — D12; Codex-bot P1 tie-order fix + re-run; joint-flat block builder deferral; __init__.py; Rule 2 iteration line) · VENUE-LEGALITY SCALE FLAGGED (ORB-MNQ 310/681, MGC 226/343, Aegis 9/122 trades span the 16:45 ET deadline — D11) · D8 SUPERSEDED BY D10; D10 RESOLVED (NAS100 = DOW CELL; TWO SWAP-PORT EXPORTS DROPPED — POINT VALUE NOT OVERRIDDEN) → FIVE STRATEGIES, FIVE TEMPLATES, ONE CELL EACH · D9 APPLIED · PLAN + THIS FILE ON MAIN · STATE QUEUE #1 · OLD VENDOR-BYTE REF DELETED, OBJECT PURGE PENDING (§6 D7)`
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
| 1 — Normalize and reproduce (+ folded Phase 0 inventory) | §4 Phase 1 gate G1.1–G1.10, verdict `PASS` | **RETURNED — verdict `NEEDS_CONTEXT`** (2026-09-03, full gate read on [PR #283](https://github.com/Joshua-Asante/first-passage/pull/283) @ `809bbb4`, base `3522d63`; 19 files, +5,953; study `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/`). G1.1 ✓ · G1.2 **red on identity** (§6 D10: the four Striker Pine hashes match the Q-TXG-1 swap-prototype pins or no pin at all — none is a pinned locked venue edition — **D10 now resolved: the two swap-port exports are dropped (point value not overridden), leaving five strategies / five templates / one cell each**; timezone / pyramid / intent fields ✓; **no source byte sizes** anywhere in config, manifest or report — item 12) · G1.3 **partial** (no repair path; whole-ledger hashes committed; **no per-row source hash** in the event ledger — item 10) · G1.4 **partial** (row/trade counts and net P&L reproduce to the cent against the anchors frozen at `a51bc60`, §5 tolerances unchanged; **win rate, profit factor, drawdown, commissions and monthly totals have no independent source anchor** — the reports carry only identity and issues — item 11) · G1.5 ✓ · G1.6 ✓ flags-not-repairs with the daily 16:45 ET audit in; **early-close capture holds zero rows → `NEEDS_CONTEXT` cap** (Codex's own label; D12) · G1.7 partial (125 tests incl. the joint union with micro-equivalents and the calendar-week zero-fill; **no joint-flat block builder and no explicit Phase 3 deferral**) · G1.8 ✓ · G1.9 partial (both CATALOG rows ✓, gate battery exit 0 ✓, required check green ✓; `__init__.py` missing) · G1.10 partial (Rule 2 line ✓; iteration count absent) · **all seven reports carry `CONTINUOUS_CONTRACT_ROLL_UNRESOLVED` (BLOCKER), so every strategy stays `BLOCKED_EXPLORATORY` whatever else lands — disposition is an operator ruling, D13**. Codex bot on #283: 1 P1 (tie-order causality in `_exposure_bounds`) + 7 P2 (two added by the operator's re-request at `809bbb4`: zero-trade typed ledger; `COMPLETE` calendar needs evidence) — worker fixes, re-runs, re-freezes hashes. **#283 was merged by the operator at `39530d4` (17:12Z; head `0d3e20f`, a pure merge of `main` over `809bbb4`) before the re-anchor round** — Phase 1 code and the `NEEDS_CONTEXT`-capped manifest are on `main`; the nine §9 items land through a follow-up Codex PR, which gets the delta read. The verdict is unchanged until then | Codex → orchestrator review | §8 ledger, §9 |
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
- **Verdict on [#283](https://github.com/Joshua-Asante/first-passage/pull/283) @ `809bbb4` (2026-09-03): `NEEDS_CONTEXT`** — the re-anchor list is in §9; the frozen rows are unchanged.

## §5 Claim manifest

| Item | Holder | Status | PR / commit | Note |
|---|---|---|---|---|
| Campaign plan | Codex (operator task) | **REVIEWED** — three passes folded | #272 @ `e8694a9` | pass 1: six P1 + one P2 (Phases 0/3/4/5/7, contract items 3/5/8/9); pass 2: four P1 (multiplicity `α`/`M`/procedure, pre-confirmation integrity check, one-path falsifier semantics + `N_conf`, holdout reserved at intake — contract items 10/11, Phases 0/1/2/7); pass 3 (Codex review of #273): eight plan-binding findings — last-inspection date, selection-inclusive outer bootstrap, Phase 2 standalone-only, numeric Phase 6, calendar-week inactivity adapter, joint block builder, per-instrument fees, Rule 2 in iterations (contract items 12/13); three reconciliation tables in the plan |
| Orchestrator takeover; this file; Phase 0 gate | orchestrator session 2026-09-03 | **MERGED** | #273 @ `5eff0ec` | gate frozen before any Phase 0 output was read; superseded by the Phase 1 gate the same day |
| Phase 0 intake (first return) | Codex, `codex/mym-breakout-research` @ `706a03e` | **RETURNED — FAIL** (G0.1, G0.3); phase then **SKIPPED** by operator override | no PR | pushed by the operator 2026-09-03: one commit on a base **68 commits behind `main`** (pre-dates PR #259's merge). Content: vet-intake notes for `ORB-MYM-SCALE-1` (`docs/notes/2026-09-01-orb-mym-scale-vet-intake.md`, `2026-09-02-next-vet-candidate-assessment.md`, a three-speed-spec paragraph) plus the raw TV bar export, the parsed `MYM_M15.csv`, and the 60-cell trade ledger. Not a seven-strategy intake |
| Phase 0 gate review | orchestrator | **DONE — `FAIL`** (this session) | — | §4 applied as a diff read; vendor files were opened only to two header lines each for content-class identification, no statistic computed |
| Phase 0 re-dispatch packet | orchestrator | **SUPERSEDED** — Phase 0 skipped | — | replaced by the §9 Phase 1 dispatch record |
| Phase 1 normalization (+ folded inventory) | Codex, [PR #283](https://github.com/Joshua-Asante/first-passage/pull/283) @ `809bbb4` (base `3522d63`) | **RETURNED — `NEEDS_CONTEXT`** | #283 **merged by the operator** (`39530d4`, 17:12Z) before the re-anchor round; follow-up Codex PR pending | 19 files: spec + plan, study dir (config, fee + early-close captures, runner, manifest, RESULTS, VERIFICATION, README), three `lab/research_utils` modules, four test modules. Frozen hashes on the branch: config `8881a2af…`, events `03efac85…`, trades `900002b8…`, weekly `5bdcef07…`, calendar `a368dc61…` |
| Phase 1 gate review | orchestrator | **FULL READ DONE** 2026-09-03 on `809bbb4` — **`NEEDS_CONTEXT`**; one re-anchor round, then re-verdict on the delta | — | worktree: 125/125 tests, `lab/discovery/cost_model.py` byte-unchanged, `--tier check` exit 0; spec §7.5–7.6 anchors reproduce; identity finding D10; re-anchor list §9 |
| Campaign pre-registration (contract items 1–14 + seven candidate contracts; Phase 3 deliverable) | orchestrator authors → adversarial panel → operator ratifies | **QUEUED** | — | must exist before any Phase 4 run |
| Phases 1–8 | per §2 | **QUEUED** | — | — |

**Hashes:** the seven Pine and seven export SHA-256 pins are committed in `phase1_config.json` on `codex/tradeify-stage1-normalization` @ `a51bc60` and listed in the design spec §2; this session read the pins, never the bytes. Code commits reviewed: `a51bc60`, `4c186e7`, `809bbb4`. Config `8881a2af…`, events `03efac85…`, trades `900002b8…`, weekly `5bdcef07…`, early-close `a368dc61…` — as committed on #283 @ `809bbb4`; the read verified the aggregate manifest against the spec anchors, never the bytes. They re-freeze after the re-anchor round. **Compute:** completed 0 · remaining
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
| D8 | **Two instrument mismatches** in the supplied set | `striker_dj30_mnq_prototype` (export on a MYM chart) and `striker_nas100_mym_prototype` (export on an MNQ chart) were declared on the other instrument, because Codex read the Q-TXG-1 sibling-swap target out of the Pine filenames | **SUPERSEDED (provisional) by D10, 2026-09-03** — the "native editions with the pyramid down" description and the five-template count no longer hold: two exports are the pinned Q-TXG-1 swap-port bodies and two are un-pinned modified bodies; the template count is unsettled until D10 closes. Historical ruling as recorded: **they are the native editions with the pyramid turned down** — DJ30 on MYM and NAS100 on MNQ, not the Q-TXG-1 swap cells. The exports are on the right chart; the declared intent and the names were wrong. Codex: flip `intended_instrument` to the export's chart (MYM, MNQ), rename the two IDs and lineage notes to say *native edition, pyramid reduced from the locked 750% / 1000% to the Pine's value* (a new expression, not the locked strategy), and add the Pine pyramiding setting to every config entry so the inventory records it. **Structural consequence:** each pyramid-down variant is a parameterization of the same entry/exit template as its locked sibling (`striker_dj30_mym_v45`, `striker_nas100_mnq_v1`), so per the candidate-contract ADR it is a **cell inside that template's contract**, not a separate template — the set holds **five templates**, and the configuration catalogue must treat each pyramid pair as a mutually exclusive cell choice, never two independent legs |
| D9 | **TradingView chart timezone** of the seven exports | Was `null` for all seven, which capped the Phase 1 verdict at `NEEDS_CONTEXT` (the plan's Phase 1 ledger is canonical UTC with exchange-local session dates) | **Resolved 2026-09-03 (operator ruling): `America/New_York` for all seven exports.** Codex sets `source_timezone` to `America/New_York` in every `phase1_config.json` entry (the config fingerprint changes), updates the test that currently asserts `source_timezone is None`, and the runner localizes with `zoneinfo` → UTC plus the exchange-local session date; DST-ambiguous or nonexistent timestamps stay hard errors (spec §4.2). The verdict cap lifts when the re-frozen config lands |
| D6 | The seven strategies' identities and the intake path | Plan §Immediate next action; only the operator holds the files | **Done 2026-09-03** — seven TradingView exports attached to Codex's local session; identities and hashes land through G1.2 |
| D10 | **Striker source identities — reopens D8** | Rule 0 read of `core/strategies/PORT_MANIFEST.sha256` against the four Striker `pine_sha256` pins in `phase1_config.json`: `178a2a8e…` **is** the pinned Q-TXG-1 sibling-swap body `striker_dj30_v4.5_mnq_qtxg1_prototype.pine` (DJ30 logic ported to MNQ, carrying the port's own point-value / session inputs), exported here on a **MYM** chart at pyramid 750 — Codex labeled it `striker_dj30_mym_v45`; `19264da2…` **is** the pinned swap body `striker_nas100_v1_mym_qtxg1_prototype.pine`, exported on an **MNQ** chart at 1000 — labeled `striker_nas100_mnq_native_variant`; `5c4b1026…` (file named `striker_dj30_v4.5_mym.pine`, pyramid 250) ≠ its pin `2b895317…`; `d18c2699…` (file named `striker_nas100_v1_mnq.pine`, pyramid 1000) ≠ its pin `bb921399…`. **None of the four is a pinned locked venue edition**: the two named as locked are modified bodies of unknown diff, and the two "native variants" are swap ports run back on the native chart, whose port-inserted point-value defaults (`mymPointValue` / the MNQ analogue) may not match the chart they ran on | Operator: (i) diff the two modified native files against the pinned bodies locally and state every change (pyramid only → a cell of the same template; anything else → say what); (ii) state whether the two swap-port exports ran with chart-input overrides matching the native instrument, or drop them; (iii) Codex renames the four IDs so no un-pinned body carries a locked name (`_v45` / `_v1`), adds `pine_pin_status` per entry (`PINNED_SWAP_PROTOTYPE` / `UNPINNED_MODIFIED`), and re-freezes. **Partial ruling 2026-09-03 (operator):** the modified `striker_nas100_v1_mnq.pine` body (`d18c2699…`) differs from its pin by the **day-of-week set** — exclude Wednesday only, i.e. {Mon, Tue, Thu, Fri}, versus the locked **Mon + Tue** (`core/strategies/_archive/nas/striker_nas100_CHANGELOG.md`: "Mon+Tue only"). That is a parameter-axis change on a locked strategy, so the export is a **day-of-week cell of the NAS100 template**, never the locked edition; the doubled trade count (378 vs 184 for the swap-port body at the lock-identical Mon + Tue filter) follows. Codex: rename it (e.g. `striker_nas100_mnq_dow_wed_excluded`), `pine_pin_status: UNPINNED_MODIFIED` with `pin_divergence: "day-of-week set {Mon,Tue,Thu,Fri} vs locked {Mon,Tue}"`. **Still open:** (i-b) the DJ30 modified body's full diff (pyramid 250 confirmed; anything else?), and (ii) whether the two swap-port exports ran with chart inputs matching the native instrument. **Lock hygiene:** the on-disk locked files no longer match their pins (`bb921399…`, `2b895317…`) — restore the pinned bytes and keep each variant under its own filename with its own pin; a locked edition is never edited in place. **Orchestrator naming rulings (2026-09-03, on the local session's request; provenance names only, no locked names):** `5c4b1026…` → `striker_dj30_mym_pyramid_250` (`UNPINNED_MODIFIED`, divergence "pyramid 250% vs locked 750%; full diff unconfirmed"); `178a2a8e…` → `striker_dj30_qtxg1_port_on_mym` and `19264da2…` → `striker_nas100_qtxg1_port_on_mnq` (`PINNED_SWAP_PROTOTYPE`, `pin_ref` to the PORT_MANIFEST line). **(ii) RESOLVED 2026-09-03 (operator): the point-value input was NOT overridden.** Each swap-port body therefore sized with the other instrument's point value (the NAS100→MYM port's `$0.50`/pt default on a `$2.00`/pt MNQ chart, and the mirror case for DJ30 on MYM) — a 4× sizing error interacting with the micro cap and the pyramid, not rescalable after the fact and never repaired. **Both swap-port exports (`178a2a8e…` on MYM, `19264da2…` on MNQ) are DROPPED from the campaign set**, recorded in the config as `dropped_sources` with reason `SWAP_PORT_BODY_POINT_VALUE_NOT_OVERRIDDEN` (their hashes and the reason stay in the inventory; nothing is silently deleted). **The set is five strategies — Aegis 6J1, ORB-MNQ recon v7, DJ30-MYM pyramid-250, NAS100-MNQ DOW-Wednesday-excluded, Vanguard MGC v0.4 — five templates, one cell each; no locked venue edition is in the set.** Remaining D10 residue: the DJ30 modified body's full diff (pyramid 250 confirmed; anything else unconfirmed) |
| D13 | **Continuous-contract roll blocker** | Every one of the seven reports carries `CONTINUOUS_CONTRACT_ROLL_UNRESOLVED` (BLOCKER): all exports come from `1!` continuous charts, so no fill can be attributed to a contract month or checked against a back-adjustment seam (spec §4.4, §4.6). The design keeps it a blocker, so all seven stay `BLOCKED_EXPLORATORY` however the other re-anchor items land; it is not a worker fix | Operator rules one of: (a) supply per-contract exports or a roll ledger (contract months + roll dates + back-adjustment offsets) for the seven charts, letting Codex attribute fills and flag seam-crossing trades; or (b) accept the continuous-symbol basis for Phases 2–4 with the seam risk stated in the pre-registration and a seam-sensitivity check pre-registered for Phase 6. Recommendation: (b) unless per-contract exports are cheap — the continuous series is the chart the strategies were tuned on |
| D11 | **Venue-illegality scale of the exported set** | The daily-deadline audit shows ORB-MNQ **310 of 681** trades, Vanguard MGC **226 of 343**, and Aegis 6J1 **9 of 122** spanning the 16:45 ET force-flat instant (ORB-MNQ also 3 Friday→Sunday). As exported these three cannot pass Phase 2 (plan: venue flags block that strategy; never a tuning opportunity). Aegis's Pine declares its own 16:30 ET flatten, so its 9 are a Pine-side defect or a chart-session artefact. Standalone headroom under the 80-micro-equivalent account cap: Aegis **0** (peak 80/80), each Striker **3–4** (76–77/80), ORB-MNQ and MGC 74–76 — recorded as inventory only; whether those peaks coincide is the Phase 4 joint-chronology question (plan §Phase 4), so no aggregate-cap verdict is drawn here | Operator rules per strategy: **re-express** as a session-bounded venue edition (exits filled **strictly before** 16:45 ET, and before 12:59 ET on early-close dates, with a bar buffer — on 15-minute bars the last exit bar closes 16:30 ET, because the audit flags any deadline instant in `(entry, exit]` — a new expression whose export is again development data under the whole-export ruling) or **drop**. Recommendation: re-express ORB-MNQ and MGC once, before Phase 2, and fix Aegis's flatten in Pine the same way, so Phase 2 eliminates on venue-legal evidence rather than on exports the venue would have flattened |
| D12 | **CME early-close calendar (holiday-short 12:59 ET)** | Codex's capture `cme_early_close_calendar.json` holds **zero rows**: cmegroup.com's trading-hours page shows only the current year and the Reference Data API needs an OAuth ID. Per §4 the missing dimension caps Phase 1 at `NEEDS_CONTEXT` | Supply the per-year CME holiday calendars 2022–2026 (yearly PDFs on cmegroup.com; roughly ten early-close dates a year) for Codex to freeze as rows, or rule the dimension accepted-unmodeled with its consequence stated (an early-close hold goes undetected). Recommendation: supply the PDFs; an hour of legwork lifts the cap |

## §7 Next exact commands (orchestrator, next session)

```bash
git fetch origin && git log --oneline origin/main..origin/codex/tradeify-stage1-normalization   # new Task commits?
# When the Phase 1 PR exists: apply §4 G1.1–G1.10 as a diff read (never open vendor bytes). In a worktree of
# its head run `python scripts/gate_manifest.py --tier check` and the four Phase 1 test modules, then check the
# committed reconciliation manifest against the spec §7.5–7.7 anchors frozen at a51bc60 (row/trade counts,
# net P&L to the cent, exactly three ORB-MNQ force-flat violations).
# ⚠ §7.7 is a Friday-to-Sunday SUB-COUNT once the daily 16:45 ET deadline is modeled (§4 note) — Codex re-freezes
# it before the runner runs; the violation total is whatever the deadline test yields.
# #283 is MERGED (operator, 39530d4) — the re-anchor round now arrives as a follow-up Codex PR off main.
# Re-anchor round (verdict NEEDS_CONTEXT, 2026-09-03): on that follow-up PR re-read only the delta — renamed IDs + pin status (D10),
# early-close rows (D12), the _exposure_bounds causality fix + regenerated manifest hashes, the joint-flat deferral
# note, __init__.py, the iteration line, the zero-trade typed ledger, the COMPLETE-calendar evidence check — then
# re-verdict. Still: never open vendor bytes; never merge a worker PR.
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
| 2026-09-03 | **Phase 1 returned:** Codex opened [#283](https://github.com/Joshua-Asante/first-passage/pull/283) @ `809bbb4` (`ca6748a`…`809bbb4` on a merge of `main`; 19 files, +5,953). Full gate read, no vendor bytes: G1.1 ✓, G1.3 ✓, G1.4 ✓ (seven counts + net P&L to the cent vs the `a51bc60` anchors; tolerances unchanged), G1.5 ✓, G1.6 ✓ mechanics with the early-close capture empty, G1.8 ✓; G1.2 red on Striker identity (D10: two exports are the pinned Q-TXG-1 swap bodies run on the native charts, two are un-pinned modified bodies carrying locked names), G1.7 no joint-flat block builder and no deferral, G1.9 `__init__.py`, G1.10 iteration count; Codex bot 1 P1 (tie-order causality) + 5 P2. **Verdict `NEEDS_CONTEXT`** — one re-anchor round. The venue audit surfaced ORB-MNQ 310/681, MGC 226/343, Aegis 9/122 deadline-spanning trades (D11); standalone cap headroom 0–4 micro-equivalents for Aegis and each Striker recorded as inventory, aggregate-cap verdict deferred to Phase 4 | Phase 1 `RETURNED — NEEDS_CONTEXT`; D10, D11, D12 raised; #283 left to the operator |
| 2026-09-03 | Operator re-requested Codex on #283 (`@codex take a look`, still `809bbb4`): two more P2 — a zero-trade export crashes the ledger builder (typed empty ledger needed); a calendar marked `COMPLETE` with zero rows is accepted and would lift the D12 cap on the status string alone. Both added to the §9 re-anchor list (items 8–9). Operator relayed the orchestrator's re-anchor prompt to the local Codex session; no push yet | re-anchor list now nine items; #283 unchanged |
| 2026-09-03 | **Operator (D10, partial):** the modified NAS100 MNQ body's divergence from its pin is the day-of-week filter — exclude Wednesday only vs the locked Mon + Tue — a parameter-axis change; that export is a DOW cell of the NAS100 template, not the locked edition (explains 378 vs 184 trades). DJ30 modified-body diff and the swap-port chart-input question stay open; on-disk locked files must be restored to their pinned bytes | D10 partially resolved; naming instruction relayed to Codex |
| 2026-09-03 | **Operator merged #283** at `39530d4` (17:12Z; head `0d3e20f` = `809bbb4` + a merge of `main`) before the re-anchor round. Phase 1 code, tests, both CATALOG rows and the `NEEDS_CONTEXT`-capped manifest are on `main`; the study is `In flight`. The nine §9 items (D10 renames + pin status, D12 rows, `_exposure_bounds` fix + re-freeze, joint-flat deferral, `__init__.py`, iteration line, zero-trade ledger, `COMPLETE`-calendar evidence, merge of main) now arrive as a follow-up Codex PR off `main`, which receives the delta read | Phase 1 code merged; verdict still `NEEDS_CONTEXT`; re-anchor follow-up pending |
| 2026-09-03 | **Operator (D10 ii): the point-value input was not overridden** when the two Q-TXG-1 swap-port bodies ran on the native charts, so both exports are mis-sized by the other instrument's point value and are **dropped** from the set (recorded as `dropped_sources`, never silently deleted). The set is five strategies, five templates, one cell each; contract item 14's per-template contracts count is five. Prompt to the local session adjusted | D10 (ii) resolved — drop; D8 fully superseded |
| 2026-09-03 | Cross-session edit noticed on merge: [PR #282](https://github.com/Joshua-Asante/first-passage/pull/282) (a separate Claude session) wired this file's §3 ceiling row and §6 D5 to a `Proposed` addendum on the 2026-07-22 withdrawal ADR — the 5.0% ceiling as prospective-only, not re-admitting candidate #1; all four frozen tiers clear 5.0%. Kept as written (accurate; single-writer rule bent by a governance session, not a worker). D5 stays unruled until the operator ratifies | D5 drafted, awaiting ratification |
| 2026-09-03 | Local session (via operator) asked for the three pending identity decisions. Orchestrator ruled the IDs (D10 naming, provenance-only) and the holding rule for the two swap-port exports (kept, flagged, operator-pending); the chart-input question was put to the operator | D10 naming resolved; D10 (ii) operator-pending |
| 2026-09-03 | **Codex re-review of #284 at `fbed9d3`** (operator re-request): 2 P1 + 4 P2, all verified on `main` and accepted — no per-row source hash (G1.3 back to partial); only counts and net P&L have independent anchors (G1.4 back to partial); no byte sizes (G1.2); D8 superseded by D10 and the five-template premise withdrawn; every report's `CONTINUOUS_CONTRACT_ROLL_UNRESOLVED` blocker needs an operator disposition (D13); D11's re-expression must exit strictly before 16:45 ET. Re-anchor list now twelve items plus D13 | folded in this PR |
| 2026-09-03 | Codex review of [#279](https://github.com/Joshua-Asante/first-passage/pull/279) (`83b17e9`): three P2 — (i) the 12:59 ET holiday-short deadline cannot stay an unmodeled dimension under G1.6 → capture the CME early-close calendar as a hashed primary-source file, and until then it caps the Phase 1 verdict at `NEEDS_CONTEXT`; (ii) per-strategy contract-cap breaches stay Phase 1 blockers (only the joint cap verdict waits for Phase 4); (iii) G1.3 is partial until the canonical ledger and its committed hash exist. All three folded in the same PR | plan unchanged; §2/§4/§9 corrected |

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
entries. With that, the set was read as **five templates** (superseded 2026-09-03 by D10 — template count unsettled): Aegis 6J1; ORB-MNQ recon v7; DJ30-MYM {locked
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

**Orchestrator full gate read at `809bbb4` — [PR #283](https://github.com/Joshua-Asante/first-passage/pull/283) (2026-09-03): verdict `NEEDS_CONTEXT`.**
Read as a diff-plus-CI read with a worktree run; no vendor bytes opened. Verified: no blob over 1 MB and no
`.csv` / `.pine` added anywhere on the tip; `local_artifacts/` ignored; no orchestrator-surface edits;
`lab/discovery/cost_model.py` byte-unchanged; 125/125 tests (four Phase 1 modules + cost model);
`gate_manifest.py --tier check` exit 0; required check `skills (3.12)` green, `pytest` and
`validation-controls` green; both CATALOG rows present under the restructured catalog; D9 applied
(`America/New_York` on all seven); `pine_pyramiding_pct` on all seven; the daily 16:45 ET deadline test with
`(entry, exit]` semantics, `friday_to_sunday_holds` as a sub-count, `overnight_holds` as the deadline count;
micro-equivalent quantities on the joint events; commission severities as interpreted in §4; the manifest's
seven row/trade counts and net P&L figures equal the spec §7.5–7.6 anchors frozen at `a51bc60` to the cent,
with the §5 tolerances unchanged since that commit; ledger hashes committed. Rule 2 count (orchestrator,
provisional pending D3): constituent (i) iteration **2** of ≤8 — iteration 1 was the failed Phase 0 return.

Re-anchor list for Codex (the verdict lifts on a delta read of exactly these):

1. **Identity (G1.2, D10):** rename the four Striker IDs so no un-pinned body carries a locked name; add
   `pine_pin_status` per entry from `core/strategies/PORT_MANIFEST.sha256` (`PINNED_SWAP_PROTOTYPE` for
   `178a2a8e…` / `19264da2…`, `UNPINNED_MODIFIED` for `5c4b1026…` / `d18c2699…` with the pinned hash they
   diverge from); apply the operator's D10 ruling on what the modified bodies changed and whether the swap-port
   exports stand; re-freeze the config. **Ruled so far:** the NAS100 modified body is a day-of-week cell
   (exclude Wednesday only vs the locked Mon + Tue) — name it as such, never as `_v1`. Final IDs ruled: `striker_dj30_mym_pyramid_250`, `striker_dj30_qtxg1_port_on_mym`, `striker_nas100_qtxg1_port_on_mnq` (D10); **D10 (ii) answered: the point value was not overridden — drop both swap-port entries** (`striker_dj30_qtxg1_port_on_mym`, `striker_nas100_qtxg1_port_on_mnq`) from the strategy list, record them under `dropped_sources` with reason `SWAP_PORT_BODY_POINT_VALUE_NOT_OVERRIDDEN` (hash, filename, pin ref, reason), remove their two rows from spec anchors §7.5–7.6, and re-freeze a five-strategy config; RESULTS and the manifest list five strategies plus the two dropped sources.
2. **Codex-bot P1:** `_exposure_bounds` must keep each trade's entry before its own exit at a timestamp tie
   (lower bound: exits of earlier-entered trades, then entries, then exits of zero-duration trades); then the
   five P2s (atomic publish of the output set; `duration_bars` in the trade ledger; fee schedule validated
   for the exact 6J/MNQ/MYM/MGC set at load; hash the same bytes that are parsed; malformed UTF-8 → intake
   failure status 3). Re-run the runner and re-freeze every hash in the manifest, RESULTS, and the PR body.
3. **Early-close rows (G1.6, D12):** freeze the operator-supplied 2022–2026 CME early-close dates into
   `cme_early_close_calendar.json` (`page_date`, source per year) and re-run; or carry the operator's
   accepted-unmodeled ruling verbatim in the file's `coverage_note` and the reports.
4. **Joint-flat block builder (G1.7):** either deliver it (real timestamps; every included leg flat at every
   block edge; ORB-MNQ's Friday→Sunday holds will fail the assertion at those weeks — report, do not repair)
   or write an explicit deferral to Phase 3 with the reason in spec §4.5 and the README.
5. **Repo integration (G1.9):** add the empty `__init__.py` camp marker to the study directory.
6. **Rule 2 (G1.10):** first line of the PR description carries the iteration count against constituent (i)
   of plan contract item 13 (iteration 2 of ≤8, provisional pending D3).
7. Merge `origin/main` again before the push; keep the Rule 2 line first; touch no orchestrator surface.
8. **Codex re-review at `809bbb4` (operator's `@codex take a look`, 16:35Z), P2:** a hash-pinned export with the full
   header but zero data rows builds a column-less frame and the runner dies on `frame["timestamp_naive"]` — return
   a typed empty ledger with the canonical columns (instrument from the source spec) so a zero-trade export yields
   a zero-trade report or a documented intake failure, never a traceback.
9. **Same re-review, P2 — binds D12:** `load_early_close_calendar` accepts `coverage_status: COMPLETE` with an
   empty `rows` list and the runner then reports `phase1_verdict_cap: COMPLETE` while applying 16:45 ET to every
   date. Reject `COMPLETE` unless the rows carry the historical early-close evidence over the coverage span; the
   status string alone must never lift the cap.
10. **Per-row source hash (G1.3; Codex re-review of #284, P1):** the canonical events ledger carries a
    `source_row_sha256` per event — the digest of the raw CSV row bytes as read — so row-level traceability
    exists independently of the whole-ledger hash; the manifest names the column.
11. **Full G1.4 reconciliation (Codex re-review of #284, P1):** counts and net P&L are the only anchored
    metrics today. The operator supplies each export's TradingView performance summary (net profit, win
    rate, profit factor, max drawdown, total commissions, monthly net) frozen as `tv_summary_anchors.json`
    before the re-run; the runner compares every metric within the §5 tolerances and each strategy report
    carries the comparison rows. Without the anchors G1.4 stays partial.
12. **Byte sizes (G1.2; Codex re-review of #284, P2):** `export_bytes` and `pine_bytes` per config entry,
    verified at load with the hash and echoed in the manifest inventory.
The **continuous-contract roll blocker** is not a worker item: it clears only by the operator's D13 ruling.

Venue-legality result the operator must see before Phase 2 (D11): ORB-MNQ 310/681, MGC 226/343, Aegis 9/122
trades span the deadline — as exported, those three are venue-illegal. Standalone peak exposure 80/80 (Aegis),
76–77/80 (each Striker), 4–6/80 (ORB-MNQ, MGC) is inventory only; whether the peaks coincide is decided by the
Phase 4 joint chronology, not here (Codex review of #284, accepted).
