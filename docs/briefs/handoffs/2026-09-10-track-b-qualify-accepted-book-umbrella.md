# CC Handoff — Track B: qualify the accepted Tradeify book (umbrella + claim manifest)

**Type:** cc_handoff
**Date:** 2026-09-10
**Parent session:** Claude Code orchestrator (worktree `claude/track-b-strategy-plan-b09f98`, Joshua + Claude)
**Spawn targets:** local Claude Code sessions (governance, specs, locked surfaces, private ports) · local Codex sessions (`codex/*` implementation + batch runs) · Codex native PR review · Cursor only if the operator confirms availability (§0.5 D-B6)
**Repo:** `Joshua-Asante/first-passage` (this checkout: `C:\Users\joshu\multi_firm_operations`)
**Brief type:** CC handoff (multi-step fleet umbrella; packets in the appendix)
**Parent question:** `N/A` — executes the operator-accepted configuration ([acceptance record](../../notes/2026-09-10-tradeify-protection-selection.md)) under the [governing plan](../../superpowers/plans/2026-09-02-seven-strategy-tradeify-select-configuration.md) once the operator releases the HOLD for Track B (§0.5 D-B1)
**Authority:** Joshua (operator). The orchestrator decomposes, freezes, reviews, integrates and adjudicates. Workers never merge, arm, or place trades. No commit reaches `main` without the operator.

**Status:** PROPOSED — no packet may be dispatched until every §0.5 decision is answered. D-B0 (PRs #332 / #334 merged) was satisfied 2026-09-10; the remaining decisions are open. This file authorizes nothing by itself.

**Revision 3 (2026-09-11):** fifteen further Codex findings on revision 2 folded — see the PR threads. Substantive changes: D-B11 is now a real fork (run the concept ADR's §4 trigger×scale grid, or supersede §4 step 2 for this instance by a full-tier ADR) with no K=1 shortcut; new D-B12 on publication scope for validation numbers; side-aware adverse marking and gap-through stop fills; partial-fill state transitions with tests; flatten fills strictly before the deadline on a bar that exists; the three full-closure dates become no-trade blocks via a typed closure overlay; the replay/evidence fingerprint (frozen at TB-F1) is separated from the execution fingerprint (sealed at B7) with shared-component equality proven; TB-T1 binds sealed values to timestamped venue evidence; TB-R2 requires digest-matched overrides and adds a mode-dependent ORB adds-off export; continuous-roll obligations enter the freeze; TB-G0 and the manifest gate on D-B1..D-B12; the registry audit hook executes the module instead of grepping.

**Revision 2 (2026-09-10):** fourteen Codex findings on PR #336 folded — see the per-finding dispositions in the PR threads. Substantive changes: protection policy is a threaded candidate object until the `dd_geometry` admission chain completes (new D-B11); new TB-R2 scaling-faithfulness packet with the per-size export menu; per-leg entry-side enforcement; missing-bar and early-close rules in replay and rail; calendar-week idle-week counter; power sizing covers the speed limb; H1/H2 split derived from a stated rule, not the ledger note; parity failure blocks the wave; a withheld ORB GO is BLOCKED, not FALSIFIED; option (b) of D-B4 carries its added scope explicitly.

---

## §0 — Rule 0 reads (PHASE 0 — executed 2026-09-10 by the orchestrator before authoring)

All anchors at `origin/main` = `47972f6` (merge of #333, 2026-09-10) unless stated; `git log --oneline HEAD..origin/main` was empty at authoring time.

- `docs/notes/2026-09-10-tradeify-protection-selection.md` @ `47972f6` — the accepted book (Aegis 8 full 6J · Vanguard 2-micro base + adds · Striker MYM 30-max history · ORB recon v7 one micro + ≤2 adds at 0.08 spacing), the 1% combined-peak trigger with 40% scaling, ORB base full and adds off while protected, prior-close-selects-next-day timing, no latch. Lines 5–9: acceptance closed STATE item 1 and explicitly did **not** claim technical validation passed; "Do not automatically reopen the campaign, resume the simulator, or create a replacement validation task." Lines 57–67: the protection evidence is unregistered exploratory analysis; native ORB no-add exits and explicit integer rounding are the open validation questions.
- `docs/superpowers/plans/2026-09-02-seven-strategy-tradeify-select-configuration.md` @ `47972f6` — lines 30–41: **current gate HOLD**; "Each next execution scope needs a separate bounded release. Workers without the private packet must stop here." Lines 93–118: S1 (unconditional speed, lower bound on P(T≤200) ≥ 0.50) and S2 (n3 after parity and fresh snapshot) approved 2026-09-05. Lines 199–216 (Task 2 replay items), 218–262 (Task 3 freeze fields), 264–292 (Task 4 select-once + Phase 8), 294–316 (Task 5 final validation) are the source of B2–B10 below.
- `docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md` @ `47972f6` — §1 Roles (Codex is the recorded orchestrator since 2026-09-05; sole writer of that file, STATE and SESSIONS for the campaign); §49 (one bounded implementation attempt authorized 2026-09-05, **suspended** by the 2026-09-08 HOLD; kept only as the attempt ceiling); §53 (C1–C5 composition design approvals live in the private packet `account-feedback-composition-2026-09-08`, receipt SHA-256 `bad72266…`); §54 (private synthetic implementation passed 125 tests; clipped lot-coverage nomination and partial-leg support unresolved; disposition SHA-256 `6b884013…`).
- `STATE.md` @ `47972f6` — queue has one live item (B7-REFIRE Stage 1 + M1); weekly operator-placed preservation trade, next deadline 2026-09-11; PREREG-C1-DEDUPE-1 waits for M1 RESOLVED + separate GO.
- `CLAUDE.md` @ `47972f6` §Live-execution posture — c1 warm and disarmed; `dry_run=false` requires M1 RESOLVED; every armed session needs its own GO; no agent places a trade; `order_id` idempotency DISPROVEN; no Pine source or executable Python ports of locked strategy logic are committed.
- `ops/c1_rail/c1_sizing_host_reference.py` @ `47972f6` — `LEG_MAP` has two rows (`dj30_mym`, `nas100_mnq`) both `cap_alloc=0`; law `r_eff = base_risk × dd_scale × lifecycle_m`, `qty = floor(risk_dollars / per_contract)`, `reserve_cap = floor(cap_alloc / (1 + pyr_pct/100))`; `generate_constants` raises `KeyError` for any `leg_key` absent from `dd_protection.BASE_RISK`; unknown `leg_id` / lifecycle key halts.
- `ops/c1_rail/c1_rail_listener.py` @ `47972f6` — `INSTRUMENT_SYMBOLS` two entries; `_leg_action` hard-codes `"buy"` for entry/add (**rail is long-only by construction**; `core/firm_rules.py:296-305` treats that as the Equity-Index hedging compliance mechanism). `aegis_6j1` is **short-only** (`phase1_config.json` `direction_evidence`).
- `ops/c1_signal_daemon/{daemon,evaluate_loop,strategy_protocol,feed}.py` @ PR #332 head `811df7c` — one `BarSource`, one `Strategy` per loop; no registry; `Signal(leg_id, signal_type, close, stop_dist_pts, bar_time)`; after #332/#334 the entrypoint always constructs an unavailable source + `NullStrategy` with emission disabled; **no approved market-data source exists** (`docs/notes/rail_build/M1_STAGE1_TEST_CONTRACT.md` on that branch: a replacement "requires an explicit source decision, implementation, review and separate operational authorization").
- `core/dd_protection.py` @ `47972f6` — `DD_TRIGGER=0.015`, `DD_SCALE=0.40` frozen and import-guarded; `calculate_protection(equity, peak, lifecycle)` binary multiplier, `round(dd,6) >= DD_TRIGGER`; `BASE_RISK` = {Striker, Striker NAS100} only. `core/dd_geometry.py` `POLICY_REGISTRY` is **empty and unwired** (the concept-not-constant hook exists with zero rows and no production call site).
- `core/mc/simulation.py` @ `47972f6` — prior-close scale selection at lines 408–411; `EvaluationState` five-field kernel (inactivity-OFF only); opt-in `intraday_low` floor test; every bust figure without it is a lower bound.
- `core/lifecycle.py` @ `47972f6` — `STRATEGY_KEYS = {Guardian, Striker, Aegis, Striker NAS100}`; `load_lifecycle_state` rejects unknown keys; state file gitignored and absent.
- `core/firm_rules.py` @ `47972f6` — `Tradeify_Select_100K`: target 6%, trailing_locking 3% ($3,000), lock offset unreachable, `micro_contract_cap: 80` (account-aggregate, not per-instrument), consistency 40%, min days 3, `_BASE_RISK` two keys.
- `ops/venue_editions/Tradeify_Select_100K.md` @ `47972f6` — live edition set empty; states in use are `WITHDRAWN` / `SCREEN-DEAD` / `CANDIDATE`; the word `RESTING` appears nowhere in the repo; Aegis and Vanguard have no row; ORB-MNQ-1 row is `SCREEN-DEAD` (edition-only).
- `docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md` @ `47972f6` — §4 **R2**: unpark at Tradeify needs fresh operator GO + superseding ADR, "Not automatic"; campaign-state lines 1210–1227 (D20-c): ORB admitted to the deployable grammar, superseding ADR drafted on the book-level result at its integer size.
- `docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md` @ `47972f6` + `docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json` — `status: CODE_LANDED`, `operator_signoff: null`; item 5 (real strategy signal with expected non-zero sizing, Stage 1 unarmed) is the only open item; 2026-08-24 addendum licenses a test strategy for it. **Track A owns this.**
- `docs/adr/2026-07-14-cc-cursor-surface-allocation.md` @ `47972f6` — routing tests 0–3; test 1 locked surfaces → Claude Code; 2026-08-29 addenda (Codex native PR review; proactive dispatch); 2026-09-04 addendum (auto `@cursor` ping off).
- `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/phase1_config.json` @ `47972f6` — five source identities with `pine_sha256` / `export_sha256` / `pine_input_overrides_sha256`, all 15-minute bars, integer contracts, `contract_cap: 80`; `aegis_6j1` short-only, the other four long-only.
- PRs: #332 (`codex/m1-stage1-test`) **MERGED** 2026-09-10 22:58Z as `583294f`; #334 (`codex/databento-retirement`) **MERGED** 2026-09-10 22:31Z as `343bbd0`. Both are on `main`; this branch merged `origin/main` at `9b0e37e`. The §0 rail/daemon/core anchors above were re-checked against the post-merge tree: unchanged except where #332/#334 are cited explicitly.
- `ops/c1_rail/c1_rail_listener.py` lines 25–28 (post-merge) — `INSTRUMENT_SYMBOLS` is **provisional** ("verify against CrossTrade's actual accepted order-ticket symbol format at the B6 dry-fire; do not assume it is correct for a live order without that check"). Only `MYM1!` has live fill evidence.
- `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/cme_early_close_calendar.json` — D19 secondary wrapper, `coverage_start` 2022-09-01, `coverage_end` 2026-09-02, `coverage_status` COMPLETE; early-close sessions require flat by 12:59 ET. It does **not** cover the forward deployment period.
- `core/dd_geometry.py` lines 25–26, 44–45, 88–91 and `docs/adr/2026-07-13-dd-protection-concept-not-constant.md` §4 (lines 55–59) and §5 (line 74) — a `POLICY_REGISTRY` row is admitted **only** via pre-registration → re-MC/grid → both-halves regime-robustness gate → freeze + admitting ADR named in `provenance`; "never invent a default instance".
- Campaign-state §6 D22 (line 199) — operator ruled 2026-09-04 that the weekly token trade is **not modelled** (materiality), with the revisit condition "if a surviving configuration ... leaves many uncovered weeks, re-check the idle-week count before quoting its bust figure"; line 90 — the venue clock is calendar-week, the engine's `inactivity_limit` is consecutive idle business days, and "a calendar-week adapter ... is the only clock admitted in Phase 5".
- `scripts/certification_power.py` lines 1–13 and 253–266 — models only the one-sided Clopper-Pearson **upper** bound on a failure rate at a single `--true-rate`; `joint_power` applies that same limb power L times. It has no mode for the pass-by-200 **lower**-bound condition.
- `docs/adr/2026-07-13-dd-protection-concept-not-constant.md` §4 lines 55–59 (re-read 2026-09-11) — admission step 2 is "Running the (trigger × scale) grid through `simulate_path` via None-safe `firm_kwargs` threading"; step 1 pre-registers the objective (minimize P(bust) at least sizing intervention, subject to a productivity floor), the selection rule and the regime gate; step 3 is the both-halves gate; step 4 freezes the winning row. A K=1 confirmation of an already-selected cell is not step 2.
- `lab/research_utils/trade_reconciliation.py` `_deadline_timestamps` (line 909: `entry < deadline <= exit_`) and `docs/adr/2026-09-03-venue-legality-re-expression-lane.md` line 21 — an exit filled **at** the deadline instant is a `FORCE_FLAT_VIOLATION`; only a fill strictly before it is legal. Same ADR lines 166–170: 2023-04-07, 2026-04-03 and 2025-01-09 close **before** 12:59 ET and "need a no-trade block"; the D19 calendar carries all 40 rows as `deadline_local 12:59` with no type field.
- `phase1_config.json` `continuous_contract_roll_policy` — `ACCEPTED_UNMODELED` (D13(b), 2026-09-03) with two obligations: the Phase 3 pre-registration states the back-adjustment seam limitation on every campaign claim, and a seam-sensitivity check is pre-registered with a frozen severity.
- Campaign-state §17a–§17d and D23 — the accepted snapshot evidence class is the **Tradeify dashboard capture** (PRIMARY: trailing threshold, balance, highest profit day, trading days, consistency), with the relational check `threshold + $3,000 == balance`; `core/mc/simulation.py` lines 74–82: `EvaluationState` "cannot certify provenance" and the caller must establish flat / no pending orders / no adjustments.
- Filesystem (2026-09-10, this machine): `.worktrees/tradeify-phase1-population` and `.worktrees/tradeify-used-account-kernel` **do not exist**; `find` over the home directory, `C:\Temp`, OneDrive and the Recycle Bin finds no `canonical_trades.csv`, `results.json`, `approval-receipt.json`, `disposition.json` or `screen-config.json` matching the recorded digests (one non-matching draft `screen-config.json` survives in a Claude scratchpad). The daily-truth-sync transcript still listed the population worktree at 20:50Z on 2026-09-10; it was gone by the time this brief was authored.

---

## §0.5 — Operator decisions required BEFORE the first dispatch (HALT-ON-AMBIGUITY)

Every worker packet in the appendix assumes these are answered and recorded in the TB-G0 integration commit. A packet dispatched before its dependency here is answered must return `NEEDS_CONTEXT`. Recommended defaults are what the orchestrator will record if the operator says "defaults".

| ID | Decision the operator must make | Recommended default | Gates |
|---|---|---|---|
| **D-B0** | Merge #332 and #334; Track B branches cut from the post-merge `main`. | **SATISFIED 2026-09-10** (`583294f`, `343bbd0`). Track B branches cut from `main` at or after `583294f`. | everything |
| **D-B1** | Release the governing plan's HOLD for Track B as a **bounded release**: un-suspend the 2026-09-05 single implementation attempt (campaign-state §49) for the packets in this manifest, with wave gates owned by the orchestrator (a wave opens only when the prior wave's specs are accepted). The D3 attempt ceiling stays one; a failed final n3 ends the attempt. | Yes — recorded in the plan's status block and a campaign-state §55 checkpoint by the orchestrator, ratified by the operator at merge. | every packet |
| **D-B2** | Orchestrator role for Track B moves from Codex (§1 Roles, 2026-09-05) to this Claude Code session; Codex remains the implementation worker lane and the automatic PR reviewer; STATE / SESSIONS / campaign-state writes for Track B are orchestrator-only. | Yes — §1 Roles amended in TB-G0. | governance writes |
| **D-B3** | Where is the private packet? (canonical ledgers under `local_artifacts/population_2026-09-05`, private overrides, the 125-test synthetic replay implementation, the C1–C5 composition specification with its approval receipt, the feasibility-screen outputs, the `dd-orb-base-only-2026-09-10` weighting study). If it exists on another machine, a backup, or a Codex cloud workspace, restore it under the **primary checkout's** ignored roots before TB-R1 runs. | If nowhere: TB-R1 regenerates the ledgers from the pinned exports and records the rest as **LOST** (digests retained for provenance); C1–C5 design decisions are re-derived as fresh decisions inside TB-S2. Standing rule from today: private artifacts never live inside `.worktrees/*` or `.claude/worktrees/*`; operator zips the private root to an external location after every wave. | TB-R1, TB-S2, TB-I2 |
| **D-B4** | B4 mode. (a) **Single-candidate confirmation**: the catalogue is exactly the accepted book (K=1); the deterministic legality/cap screen, n1 screening and n2 bound run on that one cell; a failed screen or bound ends the attempt with "no qualifying configuration". (b) The full frozen catalogue search of plan Task 4 over all five retained expressions. **(b) is not free:** it adds a fifth adapter packet (TB-A5, `striker_nas100_mnq_dow_wed_excluded`), flips D-B9 so the multi-owner shared-MNQ controller is built and proven before any two-MNQ cell is replayed, and requires TB-R2's export menu to cover the fifth leg; the manifest carries those rows as CONDITIONAL on (b). | (a). (b) re-opens the configuration selection the operator closed on 2026-09-10, makes runner-up temptation structural, and adds the scope above. | TB-P1, TB-F1, TB-E1, TB-A5, TB-S2/TB-I2 multi-owner branch |
| **D-B5** | Track A / Track B interface: the daemon's replacement market-data source, its implementation, M1 item 5 discharge and `operator_signoff` are **Track A deliverables**. Track B builds everything that is offline-testable and consumes Track A's output for the live-feed integration test, B8's timing, B9 and B10. | Yes. Track B never chooses the feed. | TB-I3 live part, TB-E2, TB-D2 |
| **D-B6** | Is Cursor still an available lane? PR #334 removes Cursor from recurring spend. | Not used. Packets marked "Cursor-eligible" go to Codex local unless the operator says otherwise. | TB-T1 |
| **D-B7** | Build a short-side rail path so `aegis_6j1` (short-only, 6J) can be expressed, enforced **per leg**: every `LEG_MAP` row carries an `allowed_entry_side` (Aegis `sell` only; Vanguard MGC, Striker MYM and ORB MNQ `buy` only) and the listener refuses any entry/add on the other side; the Equity-Index product-group hedging bar stays as a second, independent check. A test proves each leg can open on exactly one side. | Yes, per leg as stated; product group alone is insufficient (it would let MGC sell-to-open and 6J buy-to-open). | TB-S3, TB-I3, TB-A1 |
| **D-B8** | Aegis account priority: restate the "previously studied ordering" (the study is in the missing packet) as an explicit priority list, and confirm the live semantic that lower-priority strategies' **open positions are force-closed** to make 80 micro-equivalents of room when Aegis enters (8 full 6J = 80 micro-equivalents). | No default — this is a live-risk semantic; the orchestrator escalates rather than guesses. | TB-S1, TB-S2, TB-S3 |
| **D-B9** | Shared-MNQ scope: the accepted book has exactly one strategy per order symbol (6J, MGC, MYM, MNQ), so the multi-owner same-symbol controller is **off the critical path**. Keep one controller per symbol with single ownership; specify the multi-owner branch in the contract but do not build it unless Striker NAS100 re-enters. | Yes — scope reduction recorded, not silently applied. | TB-S2, TB-S3 |
| **D-B10** | Integer rounding of the 40% protected sizes must be pre-registered before any replay result is read. Options: floor (Aegis 8→3, Vanguard 2→0, MYM per its size ladder) vs floor-with-minimum-one (Vanguard 2→1). Floor disables Vanguard base entries under protection. **Consequence:** for every leg TB-R2 classifies as size-dependent (dollar/equity stops, account-state feedback), the operator produces **one TradingView export per admitted protected size** from TB-R2's single finite menu (plan Task 1: "one matching source export per admitted size ... no adaptive second menu"); adapter parity under protection is validated against those exports, never by reweighting the normal-size ledger. | Floor, matching the sizing host's `math.floor` law; if the operator prefers minimum-one, say so now, not after replay. Confirm willingness to produce the per-size exports. | TB-S1, TB-R2, TB-A1..A4 |
| **D-B11** | The 1% / 40% protection policy is **not admitted** to `core/dd_geometry.py::POLICY_REGISTRY` until the concept ADR's §4 chain completes, and a K=1 confirmation of the already-selected cell **does not satisfy step 2** (the pre-registered trigger × scale grid). Two legal routes: **(a) run the chain** — TB-P1 pre-registers the objective, the grid (a small frozen trigger × scale set that contains 1% / 40%), the selection rule and the both-halves gate; TB-E1 runs the grid; the winning row is frozen and admitted with its ADR in TB-D2. This reopens the protection cell of the accepted configuration (the book itself is unchanged), spends K equal to the grid size, and may select a cell other than 1% / 40%. **(b) supersede step 2 for this instance** — a full-tier ADR, superseding the concept ADR in part, records that the instance was operator-selected from unregistered exploratory evidence and is admitted on pre-registration (step 1) + the both-halves gate at the accepted cell (step 3 via TB-E1 H1/H2) + freeze (step 4), without a grid; written and ratified before TB-D2 lands the row. Until either completes the policy exists only as a **threaded candidate `ProtectionPolicy` value** in replay and offline rail tests; the live sizing path reads no candidate policy. | No shortcut default. If the operator wants the accepted cell kept as is, (b) is the honest route and must be an explicit governance amendment, not a packet default; (a) is the methodologically stronger route at the cost of reopening the cell. State which. | TB-S1, TB-I1, TB-I3, TB-P1, TB-E1, TB-D2 |
| **D-B12** | Publication scope for Track B's validation outputs. The selection note's publication exception "does not release raw histories, other captured overrides, private reports, account snapshots or numerical results". The n1/n2/n3 bounds, the pass-by-day curve and the replay statistics are numerical results. Options: keep them in the private root and publish only digests and PASS/FAIL labels; or record a separate, explicit publication authorization naming exactly which figures may appear in the public tree. | Private with public digests and verdict labels only; TB-D2's public decision record carries no bound, curve or account figure unless this decision says otherwise. | TB-E1, TB-E2, TB-D2 |

Additional ambiguities a packet may surface are posted under `## §0.5 Response — ambiguities` with `Status: NEEDS_CONTEXT`; workers do not resolve them.

---

## §0.75 — Local-only dependency check

Every Track B packet is **local**. Each needs at least one of: private Pine bytes (`core/strategies/**/*.pine`, gitignored), vendor exports (`core/data/tv_exports/cme/**`), the four bar panels (§16h, gitignored), the regenerated ledgers (ignored), or private account values (B7/B8). None of these may be staged to a cloud workspace under the public-clone posture. `Confirmed present` is established per packet in its Phase 0 by hashing against `phase1_config.json` / `SHA256SUMS`; `NOT confirmed → NEEDS_CONTEXT`, never "assume".

Worktree pattern for every packet: one git worktree per packet under `.worktrees/tb-<packet>` (or the Claude app's `.claude/worktrees/`), branch `<lane>/tb-<packet>-<slug>` from post-D-B0 `origin/main`; **private inputs are read by absolute path from the primary checkout and private outputs are written under the primary checkout's ignored roots, never inside the worktree**. Compute-heavy runs stay single-process (budget laptop; no parallel simulation fan-out).

---

## §1 — Context

Track B is the operator's name for qualifying the accepted four-strategy Tradeify Select 100K book through production implementation, synchronized replay, a frozen validation contract, selection/qualification evidence, winner-specific Phase 8, the ORB disposition, a fresh account snapshot, the sole n3, and a separate deployment GO. Track A (sibling session) owns M1 / B7-REFIRE Stage 1, which now includes the replacement market-data source.

**What is built (tracked, tested):** Phase 1 normalization/reconciliation (`run_phase1.py` + `lab/research_utils/{trade_reconciliation,tv_trade_ledger,tv_summary_reconciliation,joint_trade_blocks}.py`, ~2,500 test lines); the used-account MC kernel (`core/mc/simulation.py` `EvaluationState`, inactivity-OFF); the certification-power calculator (`scripts/certification_power.py`, three acceptance limbs, no stage machinery); the two-leg long-only c1 rail and the single-strategy daemon with #332's offline M1 test scaffold.

**What is owed (no tracked code exists):** every simulator primitive named in B2 (bar-to-equity adapter, within-bar ordering, fees/marked equity, cross-leg alignment, symbol controller, reservations, stale/duplicate handling, strategy-local vs session-wide flatten); every B1 production item (four adapters exist only as private Pine; no `BASE_RISK`, lifecycle key, `LEG_MAP` row or venue-ledger row for Aegis, Vanguard or ORB v7; `POLICY_REGISTRY` empty; no short-side path; no capacity controller; no carried-position rule); every B5 rail item (registry, per-symbol sources, kill switch, EOD scheduler, reconnect, daily reset, runtime position truth, dedupe implementation, private-adapter packaging into the Fly image); the B3 freeze; the ORB R2 superseding ADR; B7–B10.

**Four findings that shape the plan:**
1. The governing plan is under HOLD; workers without a release must stop. The release is D-B1.
2. The private packet is absent from this machine (§0 last bullet). Ledgers are regenerable from pinned exports; the synthetic implementation, composition spec, screen outputs and weighting study are not, unless the operator has them elsewhere (D-B3).
3. The daemon has no approved market-data source after #332/#334. Live-feed-dependent work (the daemon integration test, n3 timing, GO, arm) waits on Track A (D-B5); everything else proceeds offline.
4. The rail cannot express the accepted book as built: long-only, two legs, no registry, no capacity controller, no policy row for a 1% trigger. B1/B5 are design work first (Claude Code, locked surfaces), then implementation (Codex).

**What the orchestrator is producing:** this umbrella, the TB-G0 governance commit after §0.5 is answered, the claim manifest, per-wave spec acceptance, PR review (spec-compliance pass, quality pass, consolidated read), integration commits, and the adjudication of every load-bearing claim (`fable-judge` posture).

**What is NOT being asked of anyone:** parameter changes to any locked strategy; edits to `DD_TRIGGER` / `DD_SCALE`; re-opening configuration selection; a second simulator; choosing the market-data feed; arming; placing trades; promoting a runner-up; committing Pine, ports, exports, bar panels or account values.

---

## §2 — Execution plan

### Dependency graph

```
D-B1..D-B12 answered ──► TB-G0 (orchestrator governance commit)   [D-B0 satisfied 2026-09-10]
        │
        ├─ wave 1 (parallel, all local, no live feed) ─────────────────────────────┐
        │   TB-R1 evidence base    TB-R2 scaling-faithfulness read + export menu    │
        │   TB-S1 protection/capacity spec   TB-S2 replay spec                     │
        │   TB-S3 rail/daemon extension spec                                        │
        │   TB-P1 validation-contract DRAFT + ORB R2 ADR skeleton                   │
        │   OP-1 operator: exports at protected sizes from TB-R2's menu             │
        │                                                                           ▼
        ├─ wave 2 (after spec acceptance) ───────────────────────────────────────────
        │   TB-A1..A4 private adapters + parity PASS (need TB-R1, TB-R2/OP-1, TB-S3)
        │   [TB-A5 only under D-B4 (b)]
        │   TB-I1 candidate-policy threading + capacity + sizing on locked surfaces
        │        (needs TB-S1; NO registry row — D-B11)
        │   TB-I2 replay engine (needs TB-S2, parity PASS on every adapter, TB-R1 panels)
        │   TB-I3 rail/daemon extension, offline scope (needs TB-S3, TB-I1)
        │   TB-T1 snapshot sealer tool (needs TB-P1 field list)
        │
        ├─ wave 3 (sequential) ─────────────────────────────────────────────────────
        │   TB-F1 freeze contract (fingerprints from wave 2) → TB-E1 screen + n1 + n2 + seal
        │   → TB-D1 ORB R2 superseding ADR on the book-level result → operator GO
        │        (no GO → BLOCKED pending the operator; attempt not consumed)
        │   ── Track A delivers live source + M1 RESOLVED ──► TB-I3 live-feed test
        │        + per-symbol CrossTrade ticket verification for 6J / MGC
        │   → TB-B7 operator snapshot (TB-T1, venue-evidence-bound) + execution fingerprint sealed
        │        (replay/evidence fingerprint frozen at TB-F1 must be unchanged; shared components equal)
        │   → TB-E2 sole n3
        │   → TB-D2 GO packet (public digests/labels only unless D-B12) + protection admission per D-B11
        │   → TB-B10 operator arms
```

### Sub-track → packet map

| Sub-track (operator's list) | Packets |
|---|---|
| B1 production implementation | TB-R2 (scaling read + export menu) → TB-S1 (spec) → TB-I1 (locked surfaces, candidate policy threaded) + TB-A1..A4 (adapters, parity at every admitted size) + TB-I3 (rail rows); registry row lands with TB-D2 (D-B11) |
| B2 synchronized replay | TB-S2 (spec) → TB-I2 (engine) with TB-R1 inputs and parity-PASS adapters |
| B3 validation contract | TB-P1 (draft) → TB-F1 (freeze) |
| B4 selection evidence | TB-E1 (D-B4 mode) |
| B5 winner-specific Phase 8 | TB-S3 (spec) → TB-I3 (offline) → live-feed test after Track A |
| B6 ORB disposition | TB-P1 (skeleton) → TB-D1 (fill on evidence) → operator GO |
| B7 account state | TB-T1 (tool) + operator capture |
| B8 sole n3 | TB-E2 |
| B9 deployment GO | TB-D2 |
| B10 arm + forward clock | operator; monitoring thresholds frozen in TB-F1 |

### Claim manifest (orchestrator-owned; the anti-duplication device)

| Packet | Lane | Branch | Footprint (exact) | Depends on | Status |
|---|---|---|---|---|---|
| TB-G0 | orchestrator | `claude/tb-g0-track-b-release` | plan status block · campaign-state §55 + §1 Roles · `STATE.md` queue row · `docs/SESSIONS.md` | D-B1..D-B12 (D-B0 satisfied) | QUEUED |
| TB-R1 | Claude Code local | none (no tracked output) | primary-checkout ignored roots only + a returned inventory | D-B3 | QUEUED |
| TB-R2 | Claude Code local | `claude/tb-r2-scaling-faithfulness` | `docs/notes/2026-09-1x-track-b-scaling-faithfulness-read.md` (new, only; classification + the single finite export menu, no source values) | D-B10, TB-R1 2.1 (Pine **and** effective overrides located by digest) | QUEUED |
| OP-1 | operator | none | private: one TradingView export per admitted protected size for each size-dependent leg, plus one ORB export with adds disabled (protection mode), same chart state as the captured export, delivered to the primary checkout's ignored export root with digests | TB-R2 menu | QUEUED |
| TB-S1 | Claude Code local | `claude/tb-s1-book-protection-spec` | `docs/spec/2026-09-1x-tradeify-book-protection-capacity-spec.md` (new, only) | D-B1, D-B8, D-B10 | QUEUED |
| TB-S2 | Claude Code local | `claude/tb-s2-replay-spec` | `docs/spec/2026-09-1x-tradeify-synchronized-replay-spec.md` (new, only) | D-B1, D-B3, D-B8, D-B9 | QUEUED |
| TB-S3 | Claude Code local | `claude/tb-s3-rail-extension-spec` | `docs/spec/2026-09-1x-c1-multi-leg-rail-extension-spec.md` (new, only) | D-B1, D-B5, D-B7, D-B8, D-B9 | QUEUED |
| TB-P1 | Claude Code local | `claude/tb-p1-validation-prereg-draft` | `docs/briefs/pre-registration/2026-09-1x-track-b-final-validation-prereg.md` (new) · `docs/adr/2026-09-1x-orb-mnq-r2-supersession-DRAFT.md` (new) · `scripts/certification_power.py` + `tests/test_certification_power.py` (only the additive pass-by-day lower-bound power mode; existing pins unchanged) | D-B1, D-B4, D-B11 | QUEUED |
| TB-A1..A4 | Claude Code local ×4 | `claude/tb-a<n>-<strategy>-adapter` | private port under the primary checkout's ignored port root + `core/strategies/PORT_MANIFEST.sha256` line + one parity test per adapter under `tests/ops/` (spec'd in TB-S3); parity at the captured size **and** at every admitted protected size for size-dependent legs (OP-1 exports) | TB-R1, TB-R2, OP-1, TB-S3 accepted | STUB |
| TB-A5 | Claude Code local | `claude/tb-a5-striker-nas100-mnq-adapter` | as TB-A1..A4 for `striker_nas100_mnq_dow_wed_excluded` | **CONDITIONAL on D-B4 (b)**; otherwise never opened | CONDITIONAL |
| TB-I1 | Claude Code local | `claude/tb-i1-book-protection-impl` | `core/firm_rules.py` (allocations) · `core/lifecycle.py` (keys) · `ops/c1_rail/c1_sizing_host_reference.py` (candidate-policy threading by explicit argument; **no `POLICY_REGISTRY` row** — D-B11) · tests | TB-S1 accepted | STUB |
| TB-I2 | Codex local | `codex/tb-i2-replay-engine` | `lab/analysis/c1/tradeify_book_replay_2026-09/` (new study dir, tracked code + synthetic fixtures only) · tests | TB-S2 accepted, parity PASS recorded for every adapter in the book, TB-R1 | STUB |
| TB-I3 | Codex local | `codex/tb-i3-rail-extension` | `ops/c1_signal_daemon/*` · `ops/c1_rail/{c1_rail_listener,c1_sizing_host_reference,crosstrade_payload,c1_rail_telemetry}.py` · `deploy/*` · tests | TB-S3 accepted, TB-I1 | STUB |
| TB-T1 | Codex local (Cursor-eligible) | `codex/tb-t1-snapshot-sealer` | `scripts/seal_account_snapshot.py` + test (values bound to timestamped venue-evidence files; refuses to seal without them) | TB-P1 field list | STUB |
| TB-F1 | Claude Code local | `claude/tb-f1-freeze` | the pre-registration file (freeze edit only) | wave 2 merged | STUB |
| TB-E1 | Codex local compute | `codex/tb-e1-selection-evidence` | study dir results + digests | TB-F1 | STUB |
| TB-D1 | Claude Code local | `claude/tb-d1-orb-r2-adr` | the ORB ADR (fill + status) | TB-E1 | STUB |
| TB-E2 | Codex local compute | `codex/tb-e2-n3` | study dir results + digests (numbers private per D-B12) | TB-B7 snapshot + execution fingerprint sealed, replay/evidence fingerprint unchanged since TB-F1, Track A RESOLVED, TB-D1 operator GO recorded | STUB |
| TB-D2 | Claude Code local | `claude/tb-d2-deployment-go-packet` | `docs/notes/<date>-track-b-deployment-decision.md` (digests + verdict labels only unless D-B12 authorizes figures) · the D-B11 admission artifacts: admitting ADR (route (a)) **or** the superseding-in-part ADR already ratified (route (b)) · `core/dd_geometry.py` (the registry row, provenance naming that ADR) · `tests/core/test_dd_geometry.py` | TB-E2, D-B11, D-B12 | STUB |

Reserved to the orchestrator's integration commits: `STATE.md`, `docs/SESSIONS.md`, the campaign-state record, the governing plan, `PIPELINES.md`, `CLAUDE.md`, this file. Workers never write them. No two live packets share a file.

### Division of labor (lane rules)

- **Claude Code local** — governance (release records, pre-registrations, ADRs), all specs, every locked-surface edit (`core/*`, `lifecycle`, `dd_geometry`, Pine, ports), private strategy adapters and parity, adjudication. Runs with the repo skill stack (`rule-0`, `c1-rail`, `prop-firm-challenge`, `pinescript-v6`, `strategy-validation`, `brief-authoring`, `fable-judge`).
- **Codex local** — frozen-spec implementation in `lab/` and `ops/` (replay engine, rail/daemon extension), batch runs (screen, n1/n2, n3) on checkpointed shards from immutable manifests, plus its native automatic PR review of every PR.
- **Cursor** — only if D-B6 says available: small frozen-spec tooling (TB-T1). Never locked surfaces, never private data.
- **Operator** — D-B1..D-B12 (D-B0 done); OP-1 exports; every merge; the private-root backup after each wave; weekly preservation trade; calendar and closure-overlay upkeep; account snapshot with its evidence files; ORB GO; deployment GO; the arm.

### Wave gates (orchestrator)

- Wave 1 → 2: each spec accepted after Pass 1 (spec compliance: exactly one new file, footprint respected) and Pass 2 (quality: Rule 0 reads anchored, binary gates, forbidden moves genuine, no result-driven choices), then operator ratification of any spec that touches live-risk semantics (TB-S1, TB-S3).
- Wave 2 → 3: all wave-2 PRs merged; **parity PASS recorded for every adapter in the book at every admitted size** (a parity failure blocks that adapter and the wave; no decision-bearing run uses a divergent adapter); consolidated read across TB-I1 + TB-I3 + adapters (one sizing law, one capacity accounting, one protection policy — integration, not per-PR correctness); TB-I2 test matrix green on synthetic fixtures **and** on the regenerated ledgers.
- Wave 3 internal: TB-F1 before TB-E1; TB-E1's seal before TB-D1; TB-D1's operator GO recorded before TB-E2 (a withheld or pending GO leaves Track B `BLOCKED` at TB-D1, attempt not consumed); Track A RESOLVED + TB-B7 before TB-E2; TB-E2 pass before TB-D2; nothing after a failed TB-E1 or TB-E2 except the closure record.

---

## §4 — Falsifiable hypothesis

No research hypothesis is under test: this umbrella executes an operator-accepted configuration against the governing plan's frozen acceptance conditions (S1/S2, full/H1/H2 ≤ 5% upper failure bound, P(T≤200) lower bound ≥ 0.50, one attempt, no runner-up). Any hypothesis tested inside a packet is restated verbatim in that packet from its owner.

**Umbrella-level falsifier (plan, not book):** if two packets in the same wave return `BLOCKED — plan-itself-wrong`, or if a wave-1 spec cannot be written without a value the accepted book does not fix and the operator declines to supply it, then this decomposition is **falsified** and Track B returns to the operator for a replacement plan rather than a patched packet. **Book-level falsifier:** if TB-E1's legality screen, n1 or n2, or TB-E2's sole n3 fails any acceptance bound, the accepted book is **falsified** for deployment under this attempt; the closure record is written and no runner-up, extra sample or re-selection follows.

---

## §5 — Forbidden moves (fleet-wide; each packet restates its own)

- **Guessing the priority order or force-close semantic (D-B8) because the study is lost.** Tempting because it unblocks three specs at once. Return `NEEDS_CONTEXT`.
- **Rounding rule chosen after seeing replay results (D-B10).** Tempting because floor visibly kills Vanguard under protection. Pre-register before TB-I2 produces a number.
- **Rebuilding the lost synthetic implementation "from memory" or from §54's prose and calling it the reviewed v6.** It is a new implementation under TB-S2/TB-I2 with its own review; digests of the lost artifacts are provenance only.
- **Editing `DD_TRIGGER` / `DD_SCALE` or `calculate_protection` to express the 1% policy.** A policy-threaded sizing path with an explicit candidate `ProtectionPolicy` value is the route; the frozen constants stay byte-identical.
- **Landing a `POLICY_REGISTRY` row before the concept ADR's §4 admission chain completes.** Tempting because the registry is the "proper" home and the row is one line; forbidden by `dd_geometry.py` lines 88–91 and concept ADR §5. The row lands only with its admitting ADR in TB-D2 (D-B11).
- **Treating a withheld operator GO (ORB R2, deployment) as negative technical evidence.** FALSIFIED is reserved for a failed screen, n1, n2 or n3; an authorization dependency is BLOCKED.
- **Committing Pine, ports, exports, bar panels, ledgers or account values** to make a packet reviewable. Commit manifests, digests, synthetic fixtures and tests only.
- **Letting a worker write STATE / SESSIONS / campaign-state / the plan.** Orchestrator only, at integration.
- **Widening B4 into a search (D-B4 (b)) or promoting a runner-up after a failed n1/n2/n3.**
- **Choosing or wiring a market-data feed inside Track B.** Track A's decision; Track B consumes it.
- **Arming, `emit_enabled=true` for a real adapter, or any agent-placed order.** Operator-only, and only after B9.
- **Dispatching a packet whose Phase-0 premises were verified at authoring time rather than at dispatch time.** Re-run `git fetch origin && git log --oneline origin/main --since="24 hours ago"` and `gh pr list --state open` immediately before every dispatch.

---

## §6 — Gate + status return taxonomy

Every worker reports exactly one of: `DONE` · `DONE_WITH_CONCERNS` · `NEEDS_CONTEXT` · `BLOCKED — {context-problem | capability-problem | scope-problem | plan-itself-wrong}`.

Closure report format (verbatim in the PR body or, for TB-R1, the returned inventory):

```
Status: <DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED — <sub-case>>
Packet: TB-xx   Branch: <name>   Base: <sha of origin/main at cut>
Per-step gates: 2.1 [pass/concern/skip], 2.2 [...], 2.N [...]
Diffs (files touched): <list — must equal the manifest footprint>
Private outputs (paths only, no values): <list or none>
Concerns surfaced (if any): <list>
Next action recommended: <one sentence>
```

Umbrella gate: Track B is `RESOLVED` when TB-E2 passes all four conditions on the frozen contract, TB-D2's decision record is filed (public digests and verdict labels; figures private unless D-B12 authorizes them), and the operator records a separate deployment GO; `FALSIFIED` when the legality screen, n1, n2 or n3 fails (closure record, no runner-up, attempt ceiling consumed); `AMBIGUOUS` only if a frozen field is found unfreezable after the freeze — then the attempt closes AMBIGUOUS and any successor needs a new operator decision.

---

## §7 — Parent-session (orchestrator) review

Per returned packet, three passes, never collapsed:

**Pass 1 — Spec compliance.** Diff touches exactly the manifest footprint; every Step 2.x produced its named output; no "while I was in there" edits; private outputs are paths, not values; the closure report uses the taxonomy.

**Pass 2 — Quality.** Rule 0 anchors resolve (`git log -1 -- <path>`); gates binary; forbidden moves genuine; numbers reproduce when the packet's §10 hooks are re-run; no outcome-conditional choice; for specs, every decision traces to an owner or to a §0.5 answer.

**Pass 3 — Consolidated read (wave 2 and wave 3).** One sizing law, one capacity accounting, one protection policy, one clock across TB-I1 / TB-I2 / TB-I3 / adapters; replay semantics equal rail semantics (quantity, rejection, flatten, priority). Escalate to `fable-judge` for any claim that would change a GO.

Only after all passes does the orchestrator recommend a merge; the operator merges.

---

## §10 — Audit hooks (runnable)

```bash
# Umbrella well-formedness
python scripts/check_brief.py docs/briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md --type cc_handoff
# Expected: RESULT: well-formed

# Preconditions (D-B0)
gh pr view 332 --json state,mergedAt ; gh pr view 334 --json state,mergedAt
# Expected before dispatch: both MERGED

# HOLD still in force until TB-G0 lands (must print the HOLD line)
grep -n "Current gate (2026-09-09): HOLD" docs/superpowers/plans/2026-09-02-seven-strategy-tradeify-select-configuration.md

# Manifest discipline: no worker PR touches a reserved file
for pr in $(gh pr list --state all --search "tb-" --json number --jq '.[].number'); do gh pr view $pr --json files --jq '.files[].path' | grep -E '^(STATE.md|docs/SESSIONS.md|docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md|docs/superpowers/plans/2026-09-02-seven-strategy-tradeify-select-configuration.md|CLAUDE.md|PIPELINES.md)$' && echo "VIOLATION in PR $pr"; done
# Expected: no VIOLATION lines

# Frozen constants untouched by any Track B branch
git diff origin/main -- core/dd_protection.py | grep -E "^[+-].*(DD_TRIGGER|DD_SCALE)\s*=" ; echo "exit=$?"
# Expected: no lines (exit=1)

# No private bytes committed on any Track B branch (commits not on main; tracked metadata excluded)
git fetch origin --quiet
for b in $(git branch -r --list 'origin/*/tb-*'); do
  git log "origin/main..$b" --name-only --pretty=format: -- '*.pine' 'core/data/tv_exports/**' 'core/data/bar_data/**' 'core/data/external/**' '**/local_artifacts/**' '**/inputs/private_overrides/**' ':(exclude)**/README.md' ':(exclude)**/SHA256SUMS' ':(exclude)**/*.md' | sort -u | sed "s|^|$b: |"
done
# Expected: empty

# No POLICY_REGISTRY row on any Track B branch before TB-D2 (D-B11) — executes the module from each
# branch's bytes, so dict-literal, indexed and helper-built rows are all caught
for b in $(git branch -r --list 'origin/*/tb-*' | grep -v 'tb-d2'); do
  git show "$b:core/dd_geometry.py" > /tmp/_ddg.py && python -c "
ns={}; exec(open('/tmp/_ddg.py').read(), ns); reg=ns['POLICY_REGISTRY']
assert reg == {}, 'VIOLATION: registry non-empty on branch: %r' % sorted(reg)" || echo "VIOLATION on $b"
done
# Expected: no VIOLATION lines

# Publication scope (D-B12): no bound, curve or account figure in the public decision record
grep -nE '[0-9]+\.[0-9]+ ?%|\$[0-9]' docs/notes/*track-b-deployment-decision*.md 2>/dev/null
# Expected: empty unless D-B12 authorized specific figures (then each match must be one of them)

# Private packet presence (D-B3) — names only
ls C:/Users/joshu/multi_firm_operations/lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/local_artifacts/ 2>&1
```

---

## Verification (orchestrator-side, before declaring this umbrella complete)

```bash
python scripts/check_brief.py docs/briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md --type cc_handoff
# Expected: RESULT: well-formed
python "$HOME/.claude/skills/brief-authoring/scripts/check_brief.py" docs/briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md --type cc_handoff
# Expected: RESULT: well-formed
git log -1 --format=%h -- docs/notes/2026-09-10-tradeify-protection-selection.md ops/c1_rail/c1_sizing_host_reference.py core/dd_protection.py core/dd_geometry.py
# Expected: anchors at or before 47972f6
```

---

# Appendix — packet instructions (self-contained; copy one packet into a fresh session)

Common preamble for every packet (restated, not referenced, because the worker has none of this conversation):

> You are executing packet **TB-xx** of `docs/briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md` in the public repository `Joshua-Asante/first-passage`. Run the `handoff-verify` checklist first: `git status -sb`, `git rev-parse --show-toplevel`, `git fetch origin`, `git log --oneline HEAD..origin/main`. Confirm your branch base is at or after `583294f` on `main` (PRs #332 and #334 merged). Confirm the TB-G0 release commit exists and that every one of D-B1..D-B12 your packet lists is recorded in the governing plan's status block or the campaign-state §55 checkpoint (`grep -n "Track B" docs/superpowers/plans/2026-09-02-seven-strategy-tradeify-select-configuration.md`); if any is missing, stop with `NEEDS_CONTEXT`. Work in your own worktree and branch; never `git add -A`; never `git stash`; never write `STATE.md`, `docs/SESSIONS.md`, the campaign-state record, the governing plan, `CLAUDE.md` or `PIPELINES.md`. Read private inputs by absolute path from `C:\Users\joshu\multi_firm_operations`; write private outputs only under that checkout's ignored roots, never inside your worktree. Commit no `.pine`, no port bodies, no exports, no bar panels, no ledgers, no account values. Report with the umbrella §6 closure format and exactly one status. Halt on any ambiguity your packet does not give a recommended default for.

---

## Packet TB-R1 — Private evidence base: recover, regenerate, inventory

**Lane:** Claude Code, local, primary checkout (no tracked output; no branch). **Depends on:** D-B0, D-B3. **No-op condition:** if `C:\Users\joshu\multi_firm_operations\lab\analysis\c1\tradeify_seven_strategy_phase1_2026-09\local_artifacts\population_2026-09-05\` exists and every digest in `reconciliation_manifest.json` verifies, return `DONE` citing the verification output, and skip Step 2.2.

### Phase 0 — reads and staleness (report before acting)
- `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/README.md`, `VERIFICATION.md`, `phase1_config.json`, `reconciliation_manifest.json` (report: the five `strategy_id`s with `pine_sha256`, `export_sha256`, `pine_input_overrides_sha256`; the manifest's `git_base_commit` and the list of artifact digests it records).
- `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/run_phase1.py` (report: CLI flags, especially `--source-dir` and any output-dir / regenerate flags, and where `local_artifacts/` is written).
- Campaign-state §15f, §16h, §47, §48, §52 (report: which private inputs the single v4 generation consumed; the four accepted bar panels' names and pins; the D26 private-override files).
- `git log -1 -- lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/run_phase1.py` (anchor).

### §0.5 — recommended defaults
- (A) The operator has answered D-B3. If the answer names a location, restore first; regeneration is only for what is still missing.
- (B) Regeneration uses the **current `main`** code (post #332/#334); if `run_phase1.py` changed since `git_base_commit`, record the diff and treat any digest mismatch as `DONE_WITH_CONCERNS`, not as a defect to repair.
- (C) Never regenerate with an unscoped `--regenerate` that rewrites manifests (campaign-state §15f trap); capture the existing `SHA256SUMS` first.

### §2 — steps
- **2.1 Locate private inputs by digest, not name.** Hash every `*.pine` under `C:\Users\joshu\multi_firm_operations\core\strategies\` (recursively, including `candidates/` and `_archive/`), every file under `core\data\tv_exports\cme\`, and every file under the study's documented override location `C:\Users\joshu\multi_firm_operations\lab\analysis\c1\tradeify_seven_strategy_phase1_2026-09\inputs\private_overrides\` (expected `<strategy_id>.json`, ignored by the study's `.gitignore`); match against the five `pine_sha256` / `export_sha256` / `pine_input_overrides_sha256` triples. Expected: five Pine, five exports, five override files found. Gate: any missing → `NEEDS_CONTEXT` naming the digest and the searched directories. The override files were part of the missing packet (campaign-state §48 lists them among the private capture artifacts), so their absence is a likely outcome, not a search error; report it as such.
- **2.2 Regenerate ledgers.** From the primary checkout's study directory, run `run_phase1.py` with the flags Phase 0 reported, pointing at the private source directory; write only under `local_artifacts/`. Verify every artifact digest against `reconciliation_manifest.json` and every net total against the five strategy reports to the cent. Expected: all digests MATCH. Gate: any mismatch → `DONE_WITH_CONCERNS` with the exact artifact and both digests. If the runner's D26 override verification (`verify_input_overrides`) refuses because override files are absent, stop there with `NEEDS_CONTEXT`: regeneration needs the operator to re-supply the overrides (the captured effective chart inputs per strategy) — never bypass the check.
- **2.3 Inventory bar panels.** Locate the four accepted bar panels (§16h names/pins) on disk by digest; record path, size, digest, coverage dates. Missing panels → list them; do not fabricate or re-export.
- **2.4 Inventory the lost set.** For each of: synthetic replay implementation (§54, disposition `6b884013…`), composition specification + approval receipt (§53, `bad72266…`), feasibility-screen outputs (`screen-config.json` `5d0b0d4d…`, `results.json` `a3151f86…`), weighting study `dd-orb-base-only-2026-09-10`: record FOUND (path, digest verified) or LOST. The Claude scratchpad `C:\Temp\claude\C--Users-joshu-multi-firm-operations--claude-worktrees-tradeify-feasibility-screen-4142c0\56b8ec86-548e-40a8-a1e0-a81cb80666fc\scratchpad\` holds a non-matching draft `screen-config.json`, `screen.py`, `test_screen.py`, `STAGING.md`, `disposition.md`; copy them to the private root as `feasibility-screen-recovered-draft/` and label them DRAFT, not the recorded outputs.
- **2.5 Backup instruction.** Print the exact private-root path list for the operator to zip externally. Do not zip to any synced or cloud location yourself.

### §5 — forbidden moves
- Regenerating inside a worktree, or writing any output under `.worktrees/*` / `.claude/worktrees/*`.
- Editing `phase1_config.json`, `reconciliation_manifest.json`, `SHA256SUMS`, or any Pine to "make digests match".
- Printing any account value, trade row, or Pine body in the returned report; paths and digests only.

### §6 — return
No branch, no PR. Return the umbrella §6 closure block plus a table: artifact · FOUND/REGENERATED/LOST · path · digest-verified (Y/N). `DONE` only if the five ledgers verify; otherwise `DONE_WITH_CONCERNS` (mismatch) or `NEEDS_CONTEXT` (input missing).

---

## Packet TB-R2 — Scaling-faithfulness read and the single export menu

**Lane:** Claude Code, local (skills: `pinescript-v6`, `rule-0`, `prop-firm-challenge`). **Branch:** `claude/tb-r2-scaling-faithfulness`. **Footprint:** exactly one new file `docs/notes/2026-09-1x-track-b-scaling-faithfulness-read.md` (classification per leg + the export menu; no Pine bodies, no parameter values beyond what `phase1_config.json` already publishes). **Depends on:** D-B10 (the protected integer table's inputs), TB-R1 Phase 0 (Pine located by digest). **No-op condition:** a note matching `docs/notes/*scaling-faithfulness*` on `origin/main` covering all five legs → `DONE` citing it.

### Phase 0 — reads
- Governing plan lines 153–160 (Task 1: "Read each pinned Pine together with its effective chart inputs. Classify quantity rounding, dollar/equity stops, pyramids, margin and account-state feedback. A coded default is not evidence that a branch was inactive in the captured run"; "For a size-dependent expression, require one matching source export per admitted size ... give the operator one finite size menu before asking for them; no adaptive second menu").
- Campaign-state §7 prerequisite 1 (lines 224–225) and §19e (the DJ30 halt does not gate the pyramid add), §19d (exports not reproducible from pinned Pine — read the disposition).
- `phase1_config.json` (each strategy's `pine_sha256`, `pine_input_overrides_sha256`, `pine_pyramiding_pct`, `quantity_convention`, `lineage_notes`).
- Each pinned Pine body located **by digest** at the primary checkout (TB-R1 2.1 output), read in full **together with its digest-matched effective-input override file** (`pine_input_overrides_sha256`). A leg whose override is absent or does not match its digest gets **no classification and no menu row**: return `NEEDS_CONTEXT` for that leg naming the digest, because plan Task 1 states that "a coded default is not evidence that a branch was inactive in the captured run" — Pine defaults may not be substituted even with a flag.
- `git log -1 -- lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/phase1_config.json` (anchor).

### §0.5 — recommended defaults
- (A) A leg is **size-dependent** if any of: quantity derived from equity or a dollar risk (not a fixed integer input); dollar- or percent-of-equity day stops or soft stops; margin/affordability checks; pyramid quantities derived from equity; any read of `strategy.equity` / `strategy.netprofit` / `strategy.position_size` that alters entries or exits. A fixed integer quantity with price-only stops is **size-invariant**.
- (B) The admitted protected sizes are TB-S1's integer table under D-B10 (Aegis, Vanguard base and each add tier, Striker MYM ladder). ORB's base quantity is invariant (fixed 1 micro) unless its Pine reads equity, but ORB is **mode-dependent**: protection disables its adds, which changes average price, trailing/stall exits and later orders (the selection note names native no-add exits as an open validation question). The menu therefore keys on **size- or mode-dependence**, and ORB always gets one export with adds disabled under the same chart state.
- (C) The export menu is one table: leg · captured size (already exported) · each admitted protected size · protected-mode variant (ORB adds-off; any other leg whose protected mode changes a branch) · required export (Y/N, with the chart-state attestation the operator must repeat). One menu; if a later decision changes a size, the menu is re-issued as a replacement, not extended after results.

### §2 — steps
- **2.1** For each of the five legs, classify: quantity rounding rule; dollar/equity stops (with the branch that fires in the captured run, per the override); pyramids; margin; account-state feedback; verdict SIZE-DEPENDENT / SIZE-INVARIANT with the Pine line references (line numbers only, no code).
- **2.2** Write the single finite export menu (per (C)), including the ORB adds-off export; state explicitly which legs need no additional export and why (size-invariant **and** mode-invariant, shown from the override-bound read, not from defaults).
- **2.3** `python scripts/check_md_relative_links.py --glob "docs/notes/2026-09-1x-track-b-scaling-faithfulness-read.md"`; `make check`.

### §5 — forbidden moves
- Reconstructing suppressed trades by reweighting the captured ledger (plan Task 1: "Reweighting realized trades cannot reconstruct suppressed trades").
- Quoting Pine parameter values or bodies in the tracked note.
- Issuing a second menu after any replay result exists.

### §6 — return
PR from `claude/tb-r2-scaling-faithfulness`; closure block per umbrella §6. The operator executes OP-1 from the menu; TB-A parity for size-dependent legs waits for those exports.

---

## Packet TB-S1 — Book protection, capacity, sizing and carried-position specification

**Lane:** Claude Code, local (skills: `rule-0`, `prop-firm-challenge`, `c1-rail`). **Branch:** `claude/tb-s1-book-protection-spec`. **Footprint:** exactly one new file `docs/spec/2026-09-1x-tradeify-book-protection-capacity-spec.md` (minimal-spec style per `docs/spec/TEMPLATE-minimal-spec.md`, extended with the tables below). **Depends on:** D-B1, D-B8 (priority list), D-B10 (rounding), D-B11 (candidate policy, not a registry row). **No-op condition:** if a file matching `docs/spec/*tradeify-book-protection*` already exists on `origin/main`, return `DONE` citing it.

### Phase 0 — reads (report contents/lines before writing)
- `docs/notes/2026-09-10-tradeify-protection-selection.md` in full (the selected book, the formula `protected = round((peak_equity - equity) / peak_equity, 6) >= 0.01`, the mode table, "no latch", prior-close timing, "A loss that first crosses the trigger is not retroactively reduced", the 80-micro-equivalent capacity and Aegis priority sentence).
- `core/dd_protection.py` in full; `core/dd_geometry.py` in full (`ProtectionPolicy`, `POLICY_REGISTRY`, `protection_policy()`, `_REFERENCE_MODE_BY_DD_TYPE`); `docs/adr/2026-07-13-dd-protection-concept-not-constant.md` §Decision; `docs/adr/2026-05-10-dd-protection-ulp-rounding.md` §Decision.
- `ops/c1_rail/c1_sizing_host_reference.py` in full (the law, `_read_dd_scale`, `_read_lifecycle_multiplier`, entry/add rounding, `reserve_cap`, halt doctrine, the 2025-10-14 153-micro breach note).
- `core/firm_rules.py` lines 255–340 and 385–398 (`Tradeify_Select_100K`, cap semantics, hedging rule); `core/lifecycle.py` lines 30–75 and 120–135.
- `core/mc/simulation.py` lines 400–460 (prior-close scale selection; where `dd_trigger`/`dd_scale` enter).
- PR #332's `docs/notes/rail_build/M1_STAGE1_TEST_CONTRACT.md` §Frozen identity and sizing (the precedent for expressing a fixed one-micro quantity through the existing law, and its binary64 floor hazard).
- `git log -1 -- core/dd_protection.py core/dd_geometry.py ops/c1_rail/c1_sizing_host_reference.py` (anchors).

### §0.5 — recommended defaults (apply unless Phase 0 contradicts; then `NEEDS_CONTEXT`)
- (A) Policy object, **not** a registry row: the candidate is `ProtectionPolicy(reference_mode=<the mode meaning "drawdown from the account's own running equity peak">, trigger=0.01, scale=0.40, provenance="CANDIDATE — unadmitted; selection note 2026-09-10; admission per umbrella D-B11")`, constructed by the caller and passed by explicit argument to the replay and to the sizing host's offline test path. `POLICY_REGISTRY` stays empty until TB-D2 lands the admitting ADR (D-B11; `core/dd_geometry.py` lines 88–91). The frozen FXIFY-C2 literals are untouched. If `dd_geometry`'s `reference_mode` vocabulary cannot express "running equity peak" without ambiguity, state the ambiguity and stop (`NEEDS_CONTEXT`). The spec must state how the live sizing path behaves when no policy is supplied: it halts (no protection instance → no risk-add), never defaults.
- (B) Timing: the mode for weekday D is computed once from the settled close of the prior trading day (equity and peak as of that close); intraday equity never changes the mode within D; the peak used is the account's own EOD equity peak, initialized from the B7 snapshot's `historical_eod_peak`.
- (C) Quantities: normal sizes are the captured settings (Aegis 8 full 6J; Vanguard 2-micro base + its captured adds; Striker MYM per its captured size ladder with 30-max; ORB 1 micro base, ≤2 adds of 1 micro each). Protected sizes for Aegis/Vanguard/MYM = `floor(0.40 × normal)` per D-B10 (write the resulting integer table explicitly, including every add tier); ORB base stays 1 micro; ORB adds are not placed while protected.
- (D) Carried positions: a position open at the transition keeps its size; no resize orders in either direction; adds already resting for ORB are cancelled when protection activates; strategy exits are unchanged by mode.
- (E) Capacity: micro-equivalents are 6J=10 each, MGC/MYM/MNQ=1 each; the account cap is 80 aggregate including pending adds (reservations); entries/adds that would exceed 80 are refused (not clipped) unless the priority rule (D-B8) applies; the priority rule's force-close is a coordinated account operation distinct from any strategy exit and must be logged as such.
- (F) Expression in the sizing host: normal quantities are fixed integers per leg (not risk-fraction derived); the spec must say how each leg's normal quantity is represented so `generate_constants` cannot silently size a leg differently (either a fixed-quantity leg type, or a `base_risk` chosen so that `floor()` yields the exact integer across the whole equity range that the eval can reach, with the binary64 hazard from #332 addressed).

### §2 — steps
- **2.1** Write the spec: Objective; Steps (candidate policy object and its threading, timing, quantity tables, carried-position rule, capacity accounting, priority/force-close, telemetry fields to be emitted at each transition, the D-B11 admission mapping stated as a dependency); Gate (RESOLVED if a failing-test list is enumerated for every rule and every number in the quantity table is derivable from the selection note plus D-B10; FALSIFIED if any rule needs a value the selection note does not fix); Boundary; Reads with anchors; Owner (the selection note + this umbrella).
- **2.2** Enumerate the failing tests TB-I1 must write first (names + one-line assertion each), covering: trigger at exactly 1.000000% after rounding; prior-close timing; peak initialization from a snapshot; each leg's protected integer; ORB add suppression; carried-position invariance; reservation accounting at the cap; priority force-close ordering; frozen constants byte-identical.
- **2.3** Run `python scripts/check_md_relative_links.py docs/spec/<file>` and `make check` (record any data-gate failure caused by absent vendor bytes as expected in a bare worktree).

### §5 — forbidden moves
- Editing `core/dd_protection.py`, `core/dd_geometry.py`, the sizing host, or any test in this packet (spec only).
- Filling D-B8's priority list from memory, the lost study, or "obvious" ordering.
- Choosing a rounding rule other than D-B10's answer, or leaving rounding "to the implementer".

### §6 — return
PR from `claude/tb-s1-book-protection-spec` with the single file; closure block per umbrella §6.

---

## Packet TB-S2 — Synchronized intraday replay specification

**Lane:** Claude Code, local (skills: `strategy-validation`, `trade-csv-reconcile`, `prop-firm-challenge`). **Branch:** `claude/tb-s2-replay-spec`. **Footprint:** exactly one new file `docs/spec/2026-09-1x-tradeify-synchronized-replay-spec.md`. **Depends on:** D-B1, D-B3, D-B8, D-B9. **No-op condition:** a file matching `docs/spec/*synchronized-replay*` on `origin/main` → `DONE` citing it.

### Phase 0 — reads
- Governing plan lines 199–216 (Task 2 replay bullets and the named test cases) and lines 76–83 (accepted boundaries, intraday-honest clock).
- `core/mc/simulation.py` (`EvaluationState`, `_drawdown_outcome`, `intraday_low` semantics, `run_seed` block pairing); `core/mc/preflight.py` (`firm_kwargs`).
- `lab/research_utils/joint_trade_blocks.py`, `lab/research_utils/trade_reconciliation.py` (`reconstruct_trades`, `detect_trade_overlap`, `calculate_accounting`, `analyze_venue`), `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/README.md` §joint-flat deferral.
- `lab/analysis/c1/tradeify_book_composition_2026-09/book_grid.py` (`build_intraday_low_sequenced`) — read as the nearest analogue and record why it is not a bar replay.
- `docs/adr/2026-09-05-tradeify-select-striker-expression-readmission.md` §Same-day amendment (shared-symbol ownership obligation); `docs/adr/2026-07-29-third-leg-symbol-occupancy-limb.md` §2-A.
- Campaign-state §53 (the C1–C5 approvals exist only as a digest; re-derive as fresh decisions and say so), §54 (clipped lot-coverage nomination and partial-leg support were the unresolved items).
- `phase1_config.json` (all five sources are 15-minute bars; `synchronized_intraday_path_available` per source; `continuous_contract_roll_policy` obligations).
- TB-R1's returned inventory (which bar panels exist, their bar size and coverage) — if TB-R1 has not returned, write the spec against the §16h panel names and mark the coverage field OWED-BY TB-R1.
- `git log -1 -- core/mc/simulation.py lab/research_utils/joint_trade_blocks.py` (anchors).

### §0.5 — recommended defaults
- (A) Replay mode: **adapter replay** — the TB-A1..A4 Python adapters run on the bar panels and generate orders; the regenerated TV ledgers are the parity oracle (trade-for-trade) at the captured size, and the OP-1 exports are the oracle at each admitted protected size for legs TB-R2 classifies as size-dependent. An adapter that has not recorded parity PASS at every size the replay will exercise may not feed a decision-bearing run. Recorded-trade replay (ledger trades marked against bars) is admissible only as a separately frozen fallback for a size-invariant leg in modes it can represent faithfully; never for ORB under protection (adds-off changes ORB's exits) and never for a size-dependent leg under protection.
- (B) Within-bar ordering (conservative): on a bar that touches both a stop and a target, the stop fills first; an entry and its stop in the same bar fill in that order; fills at the bar's touch price plus the pinned per-side slippage ticks; fees per side at fill from `tradeify_commission_schedule.json`. **Gap-through rule:** when a bar opens through a resting stop (open beyond the stop price on the adverse side), the stop fills at the **bar open** plus slippage, never at the stop price; the same rule applies to a stop that a session gap or a full-closure date jumps over. A named test covers a gap-through on each side.
- (C) Marked equity: cash + open PnL at bar close for the EOD peak ratchet; the floor is tested on every bar against the **side-aware adverse mark** of the combined book (intraday-honest): a long leg is marked at its bar low, a short leg (Aegis 6J) at its bar **high**, and the combined adverse mark is the sum of each leg's adverse mark within the same bar (the conservative cross-leg ordering: adverse extremes are assumed to coincide; no favourable netting across legs). A named test covers a short-only path whose highs breach the floor while lows and closes do not. **Missing bars:** in a decision-bearing run, a missing bar on any leg that holds a position is a coverage failure for that window — the window cannot qualify (plan line 80: "Missing timing evidence cannot qualify a book"); the contract states the pre-registered coverage rule (which windows are excluded, counted how) and the run reports the excluded count. Last-close imputation is permitted only in diagnostic runs and is labelled as such in every output.
- (D) Cross-leg alignment on one 15-minute clock in one timezone (state which, from the exports' `source_timezone`), joint-flat blocks for resampling where the plan requires them.
- (E) Symbol controller: one controller per order symbol; under D-B9 each symbol has one owner in the accepted book; the multi-owner branch is specified (allocations, exits reduce own allocation only, cancellation/fill races) but marked NOT BUILT.
- (F) Reservations: pending adds reserve micro-equivalents at submission; an entry/add that would exceed 80 is refused; Aegis priority force-close per D-B8 is modeled as a coordinated flatten of named legs at the bar's marked price, logged distinctly from strategy exits.
- (G) Session-wide flatten: every leg's flatten order must **fill strictly before** the venue deadline — 16:45 ET on regular sessions, 12:59 ET on early-close dates — because `trade_reconciliation._deadline_timestamps` flags `entry < deadline <= exit` and the venue-legality ADR says only a fill strictly before the deadline is legal. With 15-minute bars and next-bar-open fill semantics, the flatten signal is scheduled at a frozen pre-deadline buffer such that the **fill bar exists and closes before the deadline** (the CME 17:00–18:00 ET maintenance halt makes a 16:45 signal fill at 18:00 — `PORT_MANIFEST` Guardian v0.3 note); the buffer values per session type are frozen fields. `AccountClock` consumes the D19 early-close calendar (`cme_early_close_calendar.json`, digest pinned) **plus a typed closure overlay** frozen in TB-P1/TB-F1 that marks 2023-04-07, 2025-01-09 and 2026-04-03 (venue-legality ADR lines 166–170) as **full-closure / no-trade dates**: no entries, no session bars admitted, every leg flat before the prior session's deadline; the overlay is a separate digest-pinned artifact, not an edit to the frozen D19 file. A replay window that extends past the calendar's `coverage_end` fails closed (cannot qualify) rather than assuming regular sessions. Strategy-local exits never touch other legs.
- (H) Duplicate/stale orders: an order whose bar_time already produced an accepted order for the same (leg, type) is dropped; a resting order older than one bar for a leg that is now flat is cancelled.
- (I) Calendar-week idle counter: the replay tracks the venue's Mon–Fri week clock and counts weeks in which the book places no fill (campaign-state line 90: the venue clock is calendar-week, not consecutive idle business days). The count is a **descriptive statistic and a monitoring input**, reported per path and per window; it is **not** modelled as a bust, because the operator's standing weekly token trade is the accepted mitigation and D22 (2026-09-04) ruled the trade is not modelled. The contract states that assumption verbatim and carries D22's revisit condition: if the idle-week count is material for the accepted book, the orchestrator re-raises it before any bust figure is quoted.
- (J) Partial fills and positions (plan lines 199–200): the replay carries the **same state machine as the listener** — a leg's position is its confirmed filled quantity; an entry or add may fill `0 < q_filled ≤ q_requested` in integer contracts; the unfilled remainder is cancelled at bar end (no chasing) and its capacity reservation released; adds are sized from the confirmed base only (as `c1_sizing_host_reference` does), never from the requested base; an exit that fills partially leaves a residual position that keeps its stop and is flattened at the deadline; a partial fill can never create an unintended short. The decision-bearing run's fill model is a **frozen field** (recommended default: full fill at the conservative price of (B) for these micro sizes, with the partial-fill fraction as a pre-registered stress cell in the D20 battery); the state machine and tests exist regardless of the frozen value. Named tests: partial entry then add sized from confirmed base; partial exit leaving a residual flattened at the deadline; partial add releasing its reservation; partial fill at the capacity boundary.

### §2 — steps
- **2.1** Write the spec: Objective; Steps (interfaces: `BarPanel`, `Adapter.on_bar → orders`, `SymbolController`, `CapacityLedger`, `AccountClock` consuming the early-close calendar and the TB-S1 candidate policy read-only, `WeekClock` for (I), outputs = per-bar equity path + trade ledger + event log + coverage report); the test matrix from plan lines 199–208 restated as named cases with expected outcomes (same-bar stop/target ambiguity, gap-through stop on each side, short-leg adverse mark at the bar high, cross-leg excursion overlap, entry/add at the cap, early-close cancellation and a flatten that fills strictly before 12:59 ET, a full-closure overlay date admitting no session, one leg exiting while another stays long, simultaneous stops/targets, stale/duplicate exits, session-wide flatten filling strictly before 16:45 ET, priority force-close, the four partial-fill cases in (J), missing bar with an open position → window excluded, calendar `coverage_end` exceeded → fail closed, idle-week count on a synthetic path); Gate (RESOLVED if every case has a deterministic expected outcome and every interface names its owner file; FALSIFIED if any case needs a rule the accepted boundaries do not fix); Boundary; Reads; Owner.
- **2.2** State explicitly what the replay can and cannot certify (daily cashflow approximation limits from the selection note lines 65–67 must be closed by this design, item by item).
- **2.3** `python scripts/check_md_relative_links.py docs/spec/<file>`; `make check`.

### §5 — forbidden moves
- Writing engine code in this packet.
- Importing `dd_protection`'s frozen constants as the book policy, or resolving one from `POLICY_REGISTRY` (it is empty by design until TB-D2): consume TB-S1's explicitly threaded candidate `ProtectionPolicy` value.
- Choosing fill/ordering conventions that are result-driven ("optimistic where it helps"); every convention is the conservative one or is escalated.
- Treating §54's 125 tests as evidence for this design.

### §6 — return
PR from `claude/tb-s2-replay-spec`; closure block per umbrella §6.

---

## Packet TB-S3 — Multi-leg signal daemon and rail extension specification

**Lane:** Claude Code, local (skills: `c1-rail`, `rule-0`, `brief-authoring`). **Branch:** `claude/tb-s3-rail-extension-spec`. **Footprint:** exactly one new file `docs/spec/2026-09-1x-c1-multi-leg-rail-extension-spec.md`. **Depends on:** D-B1, D-B5, D-B7, D-B8, D-B9. **No-op condition:** a file matching `docs/spec/*multi-leg-rail*` on `origin/main` → `DONE` citing it.

### Phase 0 — reads
- `ops/c1_signal_daemon/{daemon,evaluate_loop,strategy_protocol,feed,b1_payload,listener_client,heartbeat,http_status}.py` and the #332 additions (`m1_stage1*.py`) as merged.
- `ops/c1_rail/{c1_rail_listener,c1_sizing_host_reference,c1_rail_http_server,crosstrade_payload,c1_rail_telemetry,c1_rail_arm}.py`; `deploy/c1_rail/README.md`, `deploy/c1_signal_daemon/README.md`, both Dockerfiles and `.dockerignore` (the COPY allow-list guarded by `tests/ops/test_c1_signal_daemon_image_manifest.py`).
- `docs/adr/2026-08-08-s2b-signal-daemon-build.md` (with the #334 addendum: feed unavailable, no replacement approved), `docs/spec/2026-08-07-loop-s2b-python-signal-daemon-spec.md`.
- `docs/spec/PREREG-C1-DEDUPE-1-intent-key-functional-property.md` §R1–R6 and §6 (gated on M1 RESOLVED + GO — inherit, do not re-specify).
- `docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md` §4 (M1 items; item 5 is Track A's) and `docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json` (note the fixture-pin skew and the missing `docs/notes/rail_build/RUNBOOK.md` — record both as Track A / deployment items, do not recreate them).
- `core/firm_rules.py` lines 255–340 (cap aggregate; hedging product groups; the 16:45 ET prose).
- `docs/adr/2026-09-05-tradeify-select-striker-expression-readmission.md` §Same-day amendment (shared-symbol obligation, `flatten_first=true` and quantity-less `closeposition` hazards).
- `git log -1 -- ops/c1_signal_daemon/daemon.py ops/c1_rail/c1_rail_listener.py` (anchors).

### §0.5 — recommended defaults
- (A) Topology: one daemon process, a **strategy registry** of four adapters keyed by `leg_id`, one `BarSource` per order symbol (6J, MGC, MYM, MNQ; all 15-minute), a per-leg evaluate loop sharing one listener client; the source implementation is a Track A deliverable behind the existing `BarSource` protocol.
- (B) New `leg_id`s: `aegis_6j`, `vanguard_mgc`, `dj30_mym_p250`, `orb_mnq_v7` — distinct from the retired `dj30_mym` / `nas100_mnq` rows, which stay at zero and are never reused. `INSTRUMENT_SYMBOLS` entries for 6J and MGC are **provisional strings** (the listener's own docstring, lines 25–28: continuous-contract notation must be verified against CrossTrade's accepted order-ticket format at a dry-fire; only `MYM1!` has live fill evidence). The spec adds a **per-symbol verification gate**, live-tagged: before TB-B10, each new symbol needs an operator-attested CrossTrade ticket-format confirmation or a dry-run receipt showing the symbol accepted, recorded in telemetry; until then the leg's `cap_alloc` stays 0. `LEG_MAP` rows created at `cap_alloc=0`, lifecycle keys added, allocations expressed per TB-S1 (F).
- (C) Direction: `Signal` gains an explicit `side`; every `LEG_MAP` row carries `allowed_entry_side` (`aegis_6j`: `sell`; `vanguard_mgc`, `dj30_mym_p250`, `orb_mnq_v7`: `buy`); the listener refuses an entry/add whose side differs from the leg's allowed side (halt, telemetry event), and the Equity-Index product-group hedging bar remains as an independent second check (D-B7). Tests prove: Aegis cannot buy-to-open; Vanguard, Striker MYM and ORB cannot sell-to-open; an Equity-Index leg can never reach a `sell` action even if misconfigured.
- (D) Exits: `Signal` supports `exit` with a quantity that reduces only the emitting leg's confirmed allocation; `flatten_first=true` on entry is removed for shared symbols (moot under D-B9 but specify), and a quantity-less `closeposition` is reserved for the coordinated account flatten.
- (E) Capacity controller in the listener: a durable micro-equivalent ledger (confirmed positions + outstanding reservations) with 80 as the account cap; refuse-not-clip; priority force-close per D-B8 as an explicit coordinated operation with its own telemetry event kind.
- (F) Kill switch: an operator-invoked coordinated flatten-all + disarm + emit-disable, callable without the daemon, logged as `arming_deviation`-class evidence; never automatic on a signal.
- (G) EOD flatten scheduler and daily reset: a clock-driven flatten whose orders are submitted early enough that the **fill lands strictly before** the venue deadline — 16:45 ET on regular sessions and 12:59 ET on early-close dates read from the frozen D19 calendar (same file and digest as the replay's `AccountClock`) — with the pre-deadline buffer values frozen identically to the replay's (G) (fill at the deadline instant is a `FORCE_FLAT_VIOLATION`; the 17:00–18:00 ET maintenance halt must not swallow the fill). The scheduler also consumes the **typed closure overlay**: on a full-closure / no-trade date it refuses every entry and add, verifies flatness before the prior session's deadline, and alerts if any position is open. It fails closed when the current date is past the calendar's `coverage_end` (flatten at the earliest possible deadline and alert), so keeping the calendar and overlay current through the deployment horizon is a named operator obligation. Daily reset of per-day state follows the flatten; peak ratchet unchanged.
- (H) Disconnect/restart: reconnect with backoff per source; on restart the listener rebuilds positions from `ExecutionStateStore` and requires broker-position truth (the equity GET is not position truth) before any risk-add; unknown state fails closed.
- (I) Duplicate suppression: inherit PREREG-C1-DEDUPE-1 unchanged; note that its preconditions (M1 RESOLVED + GO) are Track A's; Track B's live-feed test cannot run before them.
- (J) Private adapter packaging: adapters are gitignored port bodies; the daemon image includes them only through a build-time private overlay documented for the operator; the image-manifest tests are extended to assert the overlay's hashes match `PORT_MANIFEST.sha256`.
- (K) Split every requirement into **offline-testable now** (registry, rows, capacity ledger, side mapping, kill switch, scheduler, restart, telemetry kinds) vs **live-source-dependent** (feed health with a real source, the item-5-class dry-run signal, end-to-end SIM chain).

### §2 — steps
- **2.1** Write the spec (Objective; Steps per (A)–(K) with owner files named; Gate: RESOLVED if every B5 item in the umbrella maps to a numbered requirement with a named test and an offline/live tag, FALSIFIED if any live-risk requirement lacks a fail-closed default; Boundary; Reads; Owner).
- **2.2** Produce the `LEG_MAP` / `INSTRUMENT_SYMBOLS` / lifecycle / `BASE_RISK`-expression table TB-I1 and TB-I3 will implement, and the parity contract each adapter must satisfy (TB-A1..A4): same integer quantity and same rejection behavior as TB-S2's replay for identical inputs.
- **2.3** `python scripts/check_md_relative_links.py docs/spec/<file>`; `make check`.

### §5 — forbidden moves
- Choosing a market-data provider or writing a feed adapter.
- Re-specifying the dedupe design (inherit PREREG-C1-DEDUPE-1).
- Proposing `--acknowledge-m1-unresolved` or any arming path.
- Recreating `RUNBOOK.md` or refreshing deployed fixture pins from tree bytes.

### §6 — return
PR from `claude/tb-s3-rail-extension-spec`; closure block per umbrella §6.

---

## Packet TB-P1 — Final-validation contract DRAFT + ORB R2 superseding-ADR skeleton

**Lane:** Claude Code, local (skills: `brief-authoring`, `strategy-validation`, `prop-firm-challenge`). **Branch:** `claude/tb-p1-validation-prereg-draft`. **Footprint:** two new files: `docs/briefs/pre-registration/2026-09-1x-track-b-final-validation-prereg.md` (status DRAFT — NOT FROZEN) and `docs/adr/2026-09-1x-orb-mnq-r2-supersession-DRAFT.md` (status PROPOSED, evidence slots empty); plus, only if Step 2.0 finds it necessary, an **additive** mode in `scripts/certification_power.py` with tests in `tests/test_certification_power.py` (existing pins and CLI behaviour unchanged). **Depends on:** D-B1, D-B4, D-B11. **No-op condition:** either file already on `origin/main` → `DONE` for that file.

### Phase 0 — reads
- Governing plan lines 69–137 (accepted boundaries, S1/S2, budget/stop), 218–262 (Task 3 freeze fields), 294–316 (Task 5).
- Campaign-state §25a (D28), §28b (D31 n3), §38 (D32 overlap-keyed DD), §41 (D33 one attempt), §7's prerequisite block lines 222–252 (per-limb vs joint sizing notes).
- `scripts/certification_power.py` and `tests/test_certification_power.py` (run `--help`; note `--limbs 3` means full/H1/H2, not n1/n2/n3).
- `docs/notes/2026-09-10-tradeify-protection-selection.md` lines 55–69 (what the selection evidence is not).
- `docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md` §2, §4 (R2, R3), §5, and campaign-state lines 1205–1230 (D20-c).
- `docs/adr/2026-08-30-evaluation-order.md` (standing order; campaign-specific amendments stay with owners).
- `git log -1 -- scripts/certification_power.py` (anchor).

### §0.5 — recommended defaults
- (A) Under D-B4 (a): catalogue K=1 = the accepted book; the legality/cap screen is deterministic (integer quantities, cap, product-group legality, session legality); n1 = screening only with a frozen continuation cutoff; n2 = the screening bound on independent streams; n3 = the sole final sample on a third stream after parity and the fresh snapshot.
- (B) Acceptance bounds exactly as the plan: for each of full/H1/H2 the one-sided 95% exact upper failure bound ≤ 0.05; on the full sample the one-sided 95% exact lower bound on P(T ≤ 200 business days) ≥ 0.50; unresolved attempts count as failures and infinite pass time; descriptive pass-by-day curve reported from the same paths.
- (C) Sample sizes: the conjunction has **four** limbs on shared paths — three failure-rate upper bounds (full/H1/H2) and one pass-by-200 **lower** bound on the full sample. `certification_power.py` as it stands models only the failure-rate limb (docstring lines 1–13; single `--true-rate`; `joint_power` repeats that limb). Size n2 and n3 by: (i) failure-limb power from the existing calculator at explicit design alternatives; (ii) speed-limb power computed as the exact probability that the one-sided 95% Clopper-Pearson lower bound on the pass-by-200 proportion is ≥ 0.50 at explicit design alternatives (an additive calculator mode, or a stdlib script recorded verbatim in the pre-registration); (iii) a dependence-valid joint lower bound (Fréchet across the four limbs) or a justified joint model, per plan lines 248–253 ("the old equal-q three-limb `q**3` calculation is insufficient"). Record every command and output verbatim; do not present planning alternatives as measured rates.
- (D) Fields that depend on wave 2 are written as `OWED-BY: TB-F1` with the exact source that will fill them. Two fingerprints, kept distinct: the **replay/evidence fingerprint** (adapter port hashes from `PORT_MANIFEST.sha256`, replay-engine commit, bar-panel digests, D19 calendar digest, closure-overlay digest, commission schedule digest, the TB-S1 candidate policy value, capacity rules, fill model) is frozen at TB-F1 and must be **unchanged through n3**; the **execution fingerprint** (rail/daemon commit, image hashes, deployed config digests) is sealed at B7 after Track A's source lands and the TB-I3 live packet merges, and the B7 seal must **prove equality of the shared components** (adapter port hashes, rule tables, policy value, capacity rules, calendar and overlay digests) with the frozen replay fingerprint. The continuous-roll policy's two obligations enter the freeze verbatim: the back-adjustment seam limitation stated on every campaign claim (fills cannot be attributed to a contract month; a seam crossing is indistinguishable from a price move) and a seam-sensitivity check pre-registered with a frozen severity in the battery. Dates: propose full = the documented coverage (2022-09-01 → 2026-09-02, from every strategy report's `summary_source_note`, which records coverage only); propose the H1/H2 boundary from a **stated rule** — chronological midpoint of the weekday axis of that coverage, odd date to H2 — and show the derivation (the earlier 2024-08-30 figure came from the feasibility screen's own midpoint convention and is not a campaign authority; do not cite the ledger note as its source). The overall horizon is proposed, not inherited (the campaign record says it was never frozen). All marked for freeze in TB-F1.
- (E) Monitoring and down-only controls: restate D20's post-deployment battery (plan lines 239–244) as thresholds with named actions (WATCH-1 0.50× and WATCH-2 0.25× are the only sizes automation may move to; RETIRED is operator-only); the live time-to-pass predictive interval's quantiles and clock origin at deployment; the seam-sensitivity check with its frozen severity and down-only action; and two operational controls stated as frozen obligations, not modelled terms — the weekly operator token trade (D22: not modelled; a missed venue week is an operational alarm) and the early-close calendar plus closure overlay kept current through the horizon (the rail scheduler fails closed past `coverage_end`).
- (F2) Publication scope: the pre-registration states which outputs are public (digests, verdict labels, the frozen contract itself) and which stay in the private root (bounds, curves, replay statistics, snapshot values) per D-B12; a later publication of any figure needs the explicit authorization D-B12 names.
- (F) Tie-breaking: with K=1 there is no tie; write the rule anyway as the plan's recommended order so a future K>1 freeze inherits it.
- (G) ORB ADR skeleton: supersedes R2 of the 2026-08-03 ADR **conditionally**; Decision slot reads "on the book-level TB-E1 result at integer size: <slot>"; Grounds/Gate/Boundary per the light-ADR contract; explicitly does not unpark the standalone ORB-MNQ-1 book or its pursuit (b3 expires 2026-11-08 separately).

### §2 — steps
- **2.0** Determine whether `scripts/certification_power.py` can compute the speed-limb power of (C)(ii). If not, add it as a new, additive CLI mode (e.g. a lower-bound proportion mode with its own `--target` and `--true-rate`), test-first, leaving every existing pin in `tests/test_certification_power.py` byte-identical; include an independent exact-integer oracle for one case as the existing tests do.
- **2.1** Write the pre-registration DRAFT with every B3 field from the umbrella (source and code fingerprints, legal integer quantities, full/H1/H2 dates and the split rule with derivation, horizon, n1/n2/n3 streams and sizes with the four-limb power computation, acceptance bounds, tie-breaking and one-attempt rules, predictive interval, monitoring thresholds and down-only controls including the seam-sensitivity check and the two operational obligations in (E), the two-fingerprint structure and the continuous-roll obligations from (D), the typed closure overlay as a frozen artifact, the fill model, the publication scope from (F2), the protection admission route chosen under D-B11 — for route (a) the grid, objective, selection rule and gate; for route (b) the reference to the ratified superseding ADR — exact account-protection semantics by reference to TB-S1, exact shared-symbol and capacity rules by reference to TB-S2/TB-S3).
- **2.2** Write the ORB ADR skeleton (light tier if it fires no limb beyond the live-risk surface; otherwise full — state which and why).
- **2.3** Run `python "$HOME/.claude/skills/brief-authoring/scripts/check_brief.py" <adr> --type adr` and `python scripts/check_adr_graph.py`; `python scripts/check_md_relative_links.py` on both files; `make check`.

### §5 — forbidden moves
- Marking any field FROZEN in this packet.
- Sizing n3 from n1/n2 results (they do not exist yet and must never inform n3's size).
- Filling the ORB Decision slot, or citing the feasibility screen or the weighting study as acceptance evidence.
- Relaxing any acceptance bound or the one-attempt rule.

### §6 — return
PR from `claude/tb-p1-validation-prereg-draft` with the two files; closure block per umbrella §6.

---

## Wave-2 and wave-3 packet stubs (entry conditions; full packets are authored by the orchestrator only after the governing spec is accepted — never before, per surface-allocation test 2)

- **TB-A1..A4 (private adapters + parity, Claude Code local, one session per strategy; TB-A5 only under D-B4 (b)).** Entry: TB-S3 accepted (protocol, `leg_id`s, side, exits, parity contract), TB-R1 `DONE`, TB-R2 merged, and OP-1 delivered for every size the leg will be replayed at. Each: Phase 0 locates its Pine by `pine_sha256` from `phase1_config.json` (not by name) and its exports by digest; ports the signal/exit logic to the daemon protocol as a gitignored body under the port root; adds a `PORT_MANIFEST.sha256` line; writes tracked parity tests that replay the port on the bar panel and compare trade-for-trade with the captured-size ledger **and, for a size-dependent leg, with each OP-1 export at its protected size, and for ORB with the OP-1 adds-disabled export in protected mode**, at the frozen tolerance from TB-S3; no parameter deviates from the pinned Pine plus its pinned input overrides. **Parity failure at any size returns `BLOCKED — capability-problem` with the first divergent trade quoted by index; the adapter is not merged, TB-I2 does not open, and no tuning loop is run.** A recorded-trade fallback for that leg is admissible only if the orchestrator separately freezes it and only for modes it can represent faithfully (never ORB under protection, never a size-dependent leg under protection).
- **TB-I1 (locked surfaces, Claude Code local).** Entry: TB-S1 accepted + operator ratification. Test-first from TB-S1 §2.2; allocation/lifecycle keys; sizing-host threading of an explicit candidate `ProtectionPolicy` argument (halt when absent); **no `POLICY_REGISTRY` row** (D-B11); frozen constants byte-identical (assert in a test); `tests/core` and `tests/ops` green.
- **TB-I2 (replay engine, Codex local).** Entry: TB-S2 accepted, **parity PASS recorded for every adapter in the book at every size the runs exercise**, TB-R1 panels present. New study dir with tracked engine + synthetic fixtures + the TB-S2 test matrix; private runs write only under the primary checkout's ignored roots; RESULTS carries digests, coverage exclusions, idle-week counts and descriptive outputs, never account values; single-process runs.
- **TB-I3 (rail/daemon extension, offline scope, Codex local).** Entry: TB-S3 accepted, TB-I1 merged. Implements the offline-tagged requirements; live-tagged ones are a later packet opened only when Track A reports an approved source and M1 `RESOLVED`.
- **TB-T1 (snapshot sealer, Codex local; Cursor-eligible under D-B6).** Entry: TB-P1's field list. A script that seals the B7 snapshot **bound to venue evidence**, matching the campaign's accepted evidence class (§17/D23: the Tradeify dashboard capture is PRIMARY). Inputs: the operator-supplied field values (balance/equity, trailing threshold, highest profit day, trading days, consistency, token-trade history) **and** the evidence files they were read from — the dashboard capture and a Tradovate positions/orders export showing zero open positions and zero working orders — each with its capture timestamp. The sealer refuses to seal without every evidence file; checks the relational facts the evidence makes checkable (`threshold + $3,000 == balance` at the high-water mark, or `peak = threshold + $3,000` otherwise; equity equals balance when flat); requires the evidence timestamps to fall inside a frozen freshness window at a session boundary with no session activity between capture and seal; validates the five numeric fields with `EvaluationState`; and writes one private sealed JSON carrying the values, the evidence digests and timestamps, and the seal timestamp, printing digests only. It states plainly that the binding is attested-by-evidence, not machine-verified against the broker, because no read API exists for the dashboard.
- **TB-F1 (freeze, Claude Code local).** Entry: wave 2 merged and consolidated read passed. Fills every `OWED-BY` field, freezes the **replay/evidence fingerprint** and the typed closure overlay, flips the pre-registration to FROZEN in one commit, records K, streams and sizes; any later change to a frozen replay/evidence component is a replacement freeze and a new operator decision. Execution-only components (rail/daemon commit, image hashes) are expected to change afterwards and are sealed at B7, not here.
- **TB-E1 (screen + n1 + n2 + seal, Codex local compute).** Entry: TB-F1 merged. Runs exactly the frozen sequence; a failed screen/n1/n2 returns the closure record and ends the attempt; a pass seals the provisional winner identity (the accepted book) and its configuration digest.
- **TB-D1 (ORB R2 ADR, Claude Code local).** Entry: TB-E1 sealed. Fills the Decision slot from the book-level result at integer size; requests the fresh operator GO. A withheld or pending GO is an authorization dependency, not evidence: Track B is **`BLOCKED — context-problem` at TB-D1**, the attempt is not consumed, and nothing downstream opens until the operator decides. ORB stays research-scored meanwhile; the book without ORB is not a substitute (that would be re-selection).
- **TB-B7 (operator).** Entry: Track A `RESOLVED`, TB-I3 live test passed, account flat with no pending orders. Operator runs TB-T1's sealer with the evidence files; the orchestrator records the snapshot digest + timestamp and seals the **execution fingerprint** (rail/daemon commit, image hashes, deployed config digests) with a written proof that every shared component — adapter port hashes, rule tables, policy value, capacity rules, calendar and overlay digests — equals the replay/evidence fingerprint frozen at TB-F1.
- **TB-E2 (sole n3, Codex local compute).** Entry: TB-B7 sealed; replay/evidence fingerprint unchanged since TB-F1; execution fingerprint sealed with shared-component equality proven; TB-D1 GO recorded. One run; four conditions; unresolved = failure/infinite; no extra sample; result adjudicated by the orchestrator under `fable-judge`; numerical outputs stay in the private root per D-B12.
- **TB-D2 (deployment GO packet + protection admission, Claude Code local).** Entry: TB-E2 passed. Files the public decision record with **digests and verdict labels only** (bounds, curve and replay statistics stay in the private root unless D-B12 authorized specific figures), rechecks snapshot identity and both fingerprints, completes the D-B11 admission on the route the operator chose — route (a): the admitting ADR records the pre-registered grid, its winner, the both-halves gate and the freeze; route (b): cites the already-ratified superseding-in-part ADR — and lands the `POLICY_REGISTRY` row whose `provenance` names the admitting ADR, with the `tests/core/test_dd_geometry.py` governance-chain check exercised non-vacuously; then requests the separate operator deployment GO. Deployment authority is never inferred from acceptance, M1, the admission, or the publication decision.
- **TB-B10 (operator).** Arm per the rail runbook (Track A re-homes the missing runbook), start the frozen forward clock at actual deployment, apply only the frozen monitoring and down-only controls, continue the weekly preservation trade.
