# STATE — First Passage

**Last curated:** 2026-08-15

This file is the **open-threads + forward-obligation register** — cross-session
items with no other home, plus the forward-trigger board. It is **not** a state
snapshot: it carries no risk %, MC anchor, strategy version, hash, working-tree
status, or canonical-owner table. Those live with their owners — see
[`docs/operational_rules.md`](docs/operational_rules.md) §7.

For uncommitted work: `git status`. For history: `git log`. For session narrative
and the live **Open / next**: [`docs/SESSIONS.md`](docs/SESSIONS.md) (read its top
entry first).

**Anti-accretion (standing):**

- New operator decision → **one decision-index line** + owning ADR (never a
  paragraph here).
- Item leaves the queue or closes → **delete the STATE row**; do not leave
  “Cleared …” footnotes.
- Forward triggers: date/criterion + owner link only; detail stays with the owner.
- Retention test for every row: *open or still owed, and no other home.* If either
  fails, it leaves.
- **Entry classes + 40-word cap (W5 direction):** Decision / Build / Measurement /
  Hygiene — see [`W5 ADR`](docs/adr/2026-08-07-w5-governance-diet.md); prefer links
  over prose.

---

## OPERATOR QUEUE — strictly ordered, ≤5 live items

**Agent-hours are cheap and budgeted (K-ledger, cost dry-runs, $700 spend ceiling);
operator-hours are the binding resource and were the only unrationed one.** This
board is the sequencing fix: the next operator-attention items in dependency order,
so they are not served in whatever order the week happens to present them.
**Pointers only** — each item's owner artifact holds the detail (Rule 7).

**Standing rule: new decision packets, advisor triage, and sizing questions queue
BEHIND this list.** Items leave when done; it stays ≤5 so it cannot decay into a backlog.

> **This cap IS the portfolio-level Survive bound** (ruled 2026-08-09,
> [`ADR`](docs/adr/2026-08-09-survive-bound-is-the-queue-cap.md)). The bound is
> **concurrency-denominated, not hours-denominated** — Rule 2's §5 forbidden move #2
> bars expressing a budget in wall-clock "anywhere in canon or ADR" (*"neither client
> can meter wall-clock"*), and nothing in the estate meters operator time. The
> rationale paragraph above was deleted 2026-08-03 and **restored 2026-08-09**; four
> surfaces cite it, one with a runnable command
> (`docs/notes/2026-07-29-comparative-advantage-thesis.md:369`).

| # | Item | Owner artifact | Blocks |
|---|---|---|---|
| 0 | ⏳ **Activity-week coverage — RECURRENCE UNRULED.** No standing weekly licence (compliance limb 5 = one named week; S1 only constrains *who* may place). Each further week = fresh operator decision. **Operator-placed at venue — not the rail** (no agent). Idle-clock observer booked under §Scheduled forward triggers → *Weekly — recurring* (radar reads it). Detail / "R8" misnomer correction stay with owners | `compliance §2a` · [`S1`](docs/adr/2026-08-07-loop-s1-environment-ratification.md) · `idle-clock spec` · [audit FU-1](docs/notes/audits/programme-audit/2026-08-05-post-descope-claim-alignment-audit.md) | keeps the account alive; unrecoverable if missed |
| 1 | **F1 — how §4 reads a Tradeify-resting discharge** (2026-11-08). Eval is live ([`S1`](docs/adr/2026-08-07-loop-s1-environment-ratification.md)); locked Striker book barred. §4 still scores the frozen $100K×4 set with Tradeify in it. Ruling owed: whether a discharge resting *on Tradeify* (or the withdrawn Striker book) discharges the four-firms program. **Deciding it early would pre-empt §4** | [`ADR 2026-08-04`](docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md) §7 F1 · [four-firms §4](docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md) | 2026-11-08 §4 verdict reading |
| 2 | **B7-REFIRE Stage 1 + M1** — both wait on an acceptable strategy on the ruled (Python-native) host. Eval live; no book deployed | [`GO ADR Addendum`](docs/adr/2026-07-17-c1-rail-build-account-registration-go.md) · [`S2`](docs/adr/2026-08-07-loop-s2-signal-host-fork.md) · [`M1`](docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md) | live-signal / arming path |

---

## Executed operator decisions — decision index

ADRs own the decision narrative ([`docs/operational_rules.md`](docs/operational_rules.md)
Rule 7; [`docs/adr/2026-07-16-root-doc-charter-dedup.md`](docs/adr/2026-07-16-root-doc-charter-dedup.md)).
One line per executed decision, newest first — consequence only. Posture summary:
[`CLAUDE.md`](CLAUDE.md) §Live-execution posture.

- **2026-08-15** — **`Q-CAPBAND-1` closed `RESOLVED` — Cap 1.0 evidence-ratified on the named axes.** Both band axes die on non-Cap gates: **D6** venue-dead (EURUSD `NOT TRADABLE` — CFD venue closed 2026-07-10); **D2-low** bar-bound (ES/NQ/YM all return the tier=always `index-intraday-ohlcv-directional-timing-2026-07-21`). So even at Cap 2.0 neither becomes fundable. Discharges [2026-08-03 audit](docs/notes/audits/programme-audit/2026-08-03-gate-stack-audit.md) §5.4 item 3. ⚠ Ratified **on the named axes only**; gates 1–2 stayed `unevaluable`. `CAP` byte-unedited; $0/K=0. [`closure`](docs/briefs/closures/Q-CAPBAND-1-closure-resolved.md)
- **2026-08-15** — **Aegis 1.83 WITHDRAWN as a reachability ceiling; `Q-CAPBAND-1` opened.** M-19 requires benchmarking a DSR floor against **both** the in-house edge (1.83) **and** the corrected published top decile (**S_B 0.85**), firing only when it exceeds *both*; only the first had been carried. 1.83 is also cohort-bound, **K-undeclared** and **un-deflated**. Operative bound relocates to **`CAP = 1.0`**. $0/K=0. [`brief`](docs/briefs/Q-CAPBAND-1-cap-band-counterfactual.md)
- **2026-08-15** — **Pre-G0 kills are NOT §4 strikes (blind channel).** Boundary is `register_search open`. Ratified alongside: **mandatory pre-G0 kill counting + disclosure** with every §4 reading (count now **1**), because the ruling makes §4 harder to fire. Consecutive-kill threshold left uncovered. $0/K=0. [`addendum`](docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md)
- **2026-08-15** — **Blind-channel cost geometry measured; `MNQ-ANALOGUE-1` killed pre-G0 at $0/K=0.** 5-instrument cost map primary-sourced (MNQ 3.65bp / MGC 6.68 / MYM 6.42 / M2K 11.03 / MCL 21.47 at panel medians); cost wall is a **frequency** wall (MNQ 2.27% capture @1/sess → 13.65% @6/sess). Operator ruled algorithmic-analogue a **new modality**; the authorized candidate then died — hit rate 0.5160 < base 0.5453, +0.837bp vs 3.64bp required, CI straddles 0. **Feasible set empty at $0.** No manifest, no Q-ID, **not** a §4 strike. notice (`git show dea3af9:docs/notes/notice/N-2026-08-15-blind-channel-cost-geometry-and-first-candidate-kill.md`) · [`route ruling`](docs/adr/2026-08-15-analogue-modality-route-ruling.md)
- **2026-08-15** — **No-counterparty statistical sourcing channel `Accepted` (full-tier ADR) + declared-K ceiling.** Opens a `futures-anomaly-discovery`-owned `--lane blind` channel for no-counterparty candidates, gated by K-accounting + mandatory frozen train/confirm split + DSR≥0.95 + cost-law + own-series half-split DSR + N-SURV unchanged. K-cap addendum refuses an open when `floor_at_k(K) > CAP` (⇒ K≤3), closing the blind-lane no-admission-gate asymmetry. Req-1a and MSL untouched. $0/K=0. [`ADR`](docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md)
- **2026-08-15** — **`Q-BUSTGATE-2` closed `RESOLVED` — bust ceiling reconfirmed unchanged.** Sole regime-admissible rung (0.50×) intraday-honest bust 0.72% ≤ 3.0%; 2026-08-13 population data + updated fee schedule checked, neither moves the ceiling. No third re-derivation absent a structural-change ruling. $0/K=0. [`closure`](docs/briefs/closures/Q-BUSTGATE-2-closure-resolved.md)
- **2026-08-15** — **F1/F2/Board-lite discharged (3 light ADRs).** F1: 2026-08-02 regime-gate scope narrowing ratified as-is. F2: allocation-refresh-2 forward-monitor absence accepted explicitly (blocked — no live-fill route). Board-lite: label papered as shorthand for two already-ratified rules. $0/K=0. [`F1`](docs/adr/2026-08-15-regime-gate-scope-ratification.md) · [`F2`](docs/adr/2026-05-23-allocation-refresh-2.md) · [`Board-lite`](docs/adr/2026-08-15-board-lite-label-ratification.md)
- **2026-08-15** — **MSL-era wall-scope audit + 08-03 follow-up verification landed.** 14 walls mapped, 4 flagged, 3 refuted on adversarial re-check (13/14 legitimately scoped — no over-tight composition found); 1 confirmed (`Board-lite` label unratified/unwired). Of the 08-03 audit's F1–F3/R1–R11: 3 DONE, 3 partial, 7 owed. [`audit`](docs/notes/audits/programme-audit/2026-08-15-msl-wall-scope-audit.md)
- **2026-08-14** — **MSL WHO-track `STILL DRY` (estate-wide).** Every Tradeify product group + census backlog walked; no WHO outside INTAKE-DRY / C1–S2B; no slate-4 card; camp not scaffolded. E1 stop rule stands. $0/K=0. notice (`git show 14d71c93:docs/notes/notice/N-2026-08-14-msl-who-track.md`)
- **2026-08-14** — **MSL §7 E1 HOLD recorded.** Phase 3 HOLD; no slate-4 card until NEW WHO; charter stays RATIFIED; yield not fired. $0/K=0. [`closure`](docs/briefs/closures/MSL-S7-closure-resolved-e1-hold.md) · [`packet`](docs/briefs/2026-08-14-msl-slate-generation-review.md)
- **2026-08-14** — **MSL §7 slate-generation review packet authored; election then recorded E1 (line above).** Yield not fired. $0/K=0. [`packet`](docs/briefs/2026-08-14-msl-slate-generation-review.md)
- **2026-08-14** — **MSL slate-3 `BLOCKED` (mechanism-dry).** Board-lite constraints frozen; no fade WHO outside 2026-08-10 INTAKE-DRY; camp not scaffolded; functional 3/3. $0/K=0. notice (`git show ef48b015:docs/notes/notice/N-2026-08-14-msl-slate-3-constraints.md`)
- **2026-08-14** — **MSL-S2B Stage-0/1 `STAGE-1 FAIL` (route; pre-G0).** Raised bar unbound for continuation *entry*; SLR route ① filter-only; temporal-selectivity paused; composite refused. G0 never frozen; slate-2 exhausted; Stage-1 deaths **2/3**. $0/K=0. [`closure`](docs/briefs/closures/MSL-S2B-closure-stage1-fail-route.md) · [`STAGE1`](lab/analysis/c1/msl_s2b_mym_2026-08/STAGE1.md)
- **2026-08-13** — **Dedup-first-before-new-work `Accepted`; §7 mechanical wiring merged (PR #800).** Rule 8 sub-rule 8 (paste search output before new `lab/analysis/` or `core/`-adjacent work); advisor-dedup hookify trigger committed + broadened to build-intent language; `check_advisor_dedup.py` gains a `--keywords` mode; `archive_lab_analysis.py` gains a same-theme collision WARN. Prompted by two same-session dedup misses. $0/K=0. [`ADR`](docs/adr/2026-08-13-dedup-first-before-new-work.md)
- **2026-08-13** — **Tradeify Select 100K checkout price re-sourced (PR #801).** Current: $265 list / $159 checkout (code AUG, expires 2026-08-31) / $169 reset / no activation fee — primary-sourced in-browser 2026-08-13 (WebFetch 403s the host). Historical $159 paid 2026-07-18 (GO ADR §B4) left untouched as the purchase record; this is the forward-modeling figure. $0/K=0. note (`git show 67e4b209:docs/notes/2026-08-13-tradeify-select-100k-checkout-price.md`)
- **2026-08-13** — **MSL-C3-K2 dual-axis explore FALSIFIED.** Both axes IS CI entirely &lt; 0; panel `M2K_M15` landed (TV); CONFIRM unread; S2B unblocked; $0/K spent=0. [`closure`](docs/briefs/closures/MSL-C3-K2-closure-falsified.md) · [`RESULTS_g2`](lab/archive/msl_c3_m2k_2026-08/RESULTS_g2.md) · [`PREREG_G0`](lab/archive/msl_c3_m2k_2026-08/PREREG_G0.md)
- **2026-08-13** — **MSL-C3-K2 dual-axis G0 FROZEN.** B4 paid after Stage-1 PASS; `K_intrinsic=2` (PDH/PDL + overnight); DSR floor 0.850; explore unpaid at freeze (superseded by FALSIFIED line above). [`ADR`](docs/adr/2026-08-13-msl-c3-k2-dual-axis-revive.md) · [`STAGE1_K2`](lab/archive/msl_c3_m2k_2026-08/STAGE1_K2.md) · [`PREREG_G0`](lab/archive/msl_c3_m2k_2026-08/PREREG_G0.md)
- **2026-08-13** — **MSL-C3-K2 dual-axis Stage-1 revive ELECTED.** Fresh Stage-1 PASS licensing `K_intrinsic=2` (PDH/PDL + overnight both scored); DSR floor 0.850; board ahead of S2B; B4 was unpaid at election (superseded by G0 freeze line above). [`ADR`](docs/adr/2026-08-13-msl-c3-k2-dual-axis-revive.md) · [`STAGE1_K2`](lab/archive/msl_c3_m2k_2026-08/STAGE1_K2.md)
- **2026-08-13** — **MSL-S2A explore GO → `FALSIFIED` (N-ACT).** IS trades/week 0.511; long FLIP FAIL; CONFIRM unread; STOP G0. $0/K=0. [`RESULTS_g2`](lab/archive/msl_s2a_mcl_2026-08/RESULTS_g2.md) · [closure](docs/briefs/closures/MSL-S2A-closure-falsified.md)
- **2026-08-13** — **MSL-S2A B4 GO → G0 FROZEN.** MCL `pullback-failure-resumption`; `K_intrinsic=1`; CONFIRM `2025-07-01→2026-07-02` unread; explore later FALSIFIED 2026-08-13. $0/K=0. [`PREREG_G0`](lab/archive/msl_s2a_mcl_2026-08/PREREG_G0.md)
- **2026-08-13** — **MSL slate-2 box ELECTED + P3.4 S2A Stage-1 PASS (B4 unpaid).** `rr`∈[2,3] / WR 0.30–0.42 / R-at-frontier; S2A MCL `pullback-failure-resumption`; SNAG registered; Magdon-Ismail not calibration; sprint lane not opened. $0/K=0. [`ADR`](docs/adr/2026-08-13-msl-slate-2-design-box.md) · [STAGE1](lab/archive/msl_s2a_mcl_2026-08/STAGE1.md)
- **2026-08-13** — **MSL-C2 explore GO → `FALSIFIED` (both-arms CI&lt;0).** IS mean ≈ −0.18R; DELETE FAIL; CONFIRM unread; STOP G0 → P3.2 C3 next. $0/K=0. [`RESULTS_g2`](lab/archive/msl_c2_mgc_2026-08/RESULTS_g2.md) · [closure](docs/briefs/closures/MSL-C2-closure-falsified.md)
- **2026-08-13** — **`implied_annualized_sr` DEMOTED gate → report-only (`IMPLIED-SR-REPORT-ONLY-2026-08-13`); Tradeify-native fade design-region REOPENED as geometry.** 1.83 is a cohort disclosure, not a FAIL. Measured-edge still gates on DSR-at-K. No mechanism admitted. $0/K=0. [`ADR`](docs/adr/2026-08-13-implied-sr-report-only-fade-reopen.md)
- **2026-08-12** — **MSL-C2 B4 GO → G0 FROZEN.** London-range failed-extension fade on MGC; K_intrinsic=1; CONFIRM 2025-09-01→2026-08-12 unread; explore/Pine unpaid (later explore FALSIFIED 2026-08-13). $0/K=0. [`PREREG_G0`](lab/archive/msl_c2_mgc_2026-08/PREREG_G0.md)
- **2026-08-12** — **MSL implied-SR off kill list (interim; now Superseded).** Absorbed by 2026-08-13 report-only ADR. [ADR](docs/adr/2026-08-12-msl-implied-sr-disclosure-not-kill.md)
- **2026-08-12** — **MSL Board B1–B3 + B8 ratified.** Channel Accepted (R-CHANNEL ☑ · R-FRAMING ☑ §2.1 · R-REQSCOPE ☑ do-not-bind); slate **C2→C3→C1**; Cursor wrapper allow-rule; `MYM1!`/`MNQ1!` occupancy released for new non-Striker research. S1 keep-warm + Striker redeploy bar stand. $0/K=0. [ratification](docs/adr/2026-08-12-msl-sourcing-channel-ratification.md) · [occupancy](docs/adr/2026-08-12-msl-mym-occupancy-release.md) · [plan](docs/briefs/2026-08-12-msl-program-plan.md)
- **2026-08-12** — **Q-TXG-1 CLOSED — FALSIFIED-at-walls (operator A).** H_A re-argument ruled CLOSE; third election barred; registry lane row filed. Re-proposal = different loss-side shape or different venue-class survival geometry (not new cells/ATR). [packet](docs/briefs/Q-TXG-1-ha-reargument.md) · [lane closure](docs/briefs/closures/Q-TXG-1-closure-falsified-at-walls.md) · [registry](docs/rejected_candidates.md)
- **2026-08-12** — **Q-TXG-1 cell #2 striker×MNQ → DEAD(N-SURV).** Cost PASS (mean_net_r 0.042 > 0.03); N-SURV FAIL full/H1/H2 bust ~98%/97%/99% vs ≤3.0%. K actual=declared=1. Cell #1 striker_nas100×MYM still open at authoring — lane H_A re-argument **not** fired. [closure](docs/briefs/closures/2026-08-12-q-txg-1-striker-mnq-cell-dead-nsurv.md) · [PANEL_SCORE](lab/archive/transfer_expression_grid_2026-08/cells/striker_mnq/PANEL_SCORE.json)
- **2026-08-12** — **Q-TXG-1 Blocks 2–3 frozen at .** Elected striker_nas100×MYM then striker×MNQ; cell PREREGs + ports hash-pinned + RUNSPECs authored. **HARD STOP before scoring** (Block 4 gated on operator native-TV exports). [ELECTION](lab/archive/transfer_expression_grid_2026-08/ELECTION.md) · [
as×MYM PREREG](docs/briefs/pre-registration/2026-08-12-q-txg-1-striker-nas100-mym-cell-prereg.md) · [striker×MNQ PREREG](docs/briefs/pre-registration/2026-08-12-q-txg-1-striker-mnq-cell-prereg.md)
- **2026-08-12** — **Q-TNEC-CON-5 Branch A STOP elected** (operator election via task start). Catalogue non-promotable; CONFIRM unread forever; dense-1m **OHLCV temporal-selectivity lane default paused** pending new modality / non-route-① thesis. Cite: 8 consecutive zero-yield closes since 2026-08-08 (Q-R2VBUCK-1 … Q-TNEC-CON-5) vs SNAG 3. Lane FALSIFIED counter **unchanged 1/3**. /K=0. [closure](docs/briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md)
- **2026-08-11** — **`Q-TXG-1` Block 1 executed at $0.** Transfer/expression grid compiled (4 mechanisms × ENV-1 7-micro pool); H_A **OPEN — 25 OPEN cells**. Block 2 election packet authorized. [`GRID_RESULTS`](lab/archive/transfer_expression_grid_2026-08/GRID_RESULTS.md) · [`PREREG`](lab/archive/transfer_expression_grid_2026-08/PREREG.md)
- **2026-08-11** — **`Q-SCORE-1` Block 1 H_A FALSIFIED at $0.** Assignability 37/53 (69.8%) under frozen Closed: grammar; grandfather-concentration **recent-spread** (7/15 undated not in GRANDFATHERED). Residue **RATIFIED 2026-08-11** (operator GO via task start): forward `Lane:`/`Closed:` fields in [`closure_record.md`](.claude/skills/brief-authoring/references/closure_record.md) (notice `git show 103365f5:docs/notes/notice/N-2026-08-11-q-score-1-forward-fields.md`); same grammar serves queued coverage-limb promote-to-HARD ADR. Block 2 still gated — re-entry needs fresh recount ≥80% under a new campaign id. No retro-edits of undated closures. [`BLOCK1_RESULTS`](lab/archive/approach_scoreboard_2026-08/BLOCK1_RESULTS.md) · [`PREREG`](lab/archive/approach_scoreboard_2026-08/PREREG.md) · [`closure`](docs/briefs/closures/Q-SCORE-1-closure-falsified.md)
- **2026-08-11** — **`Q-MCLTAS-1` closed `FALSIFIED` (Wall B magnitude) at $0/K=0 — the probe was never run.** Operator-authorized Stage 0a+0b (both free) against a pre-registered two-wall gate. **Wall B dispositive:** Req-5 hurdle 11.60 ticks = **14.87 bp** vs the estate causal-public δ ceiling **3.21 bp** (4.63×; floor 3.01×; 3.04× under the forbidden bare-commission ablation); in cohort-bound δ/σ against MCL's own **measured** σ surface, required 0.62–1.35 vs D5's committed 0.113/0.194 → **floor 3.2×, defensible 7.0×**. **Wall A:** {free ∧ signed ∧ exogenous ∧ window-aligned} sign sources **EMPTY** (TAS volume gross by construction; no CME settlement-window imbalance print — the structural asymmetry vs equity closing auctions); one entitled-costed route unverified and unable to reach Wall B. **Corrects the ENV-1 reading in both halves** — non-circularity is scoped to decay observables, and the cell was never "blocked on δ alone". Discharges the 2026-08-11 item-(b) ruling's probe requirement negatively. Registry row filed; MCL the instrument NOT rejected. [`closure`](docs/briefs/closures/Q-MCLTAS-1-closure-falsified.md) · [`RESULTS`](lab/analysis/c1/cheap_falsifiers_2026-08/_probe_stage0_RESULTS_2026-08-11.md)
- **2026-08-11** — **`Q-TNEC-ENV-1` post-closure rulings (JA, light record).** (a) MGC calibration row **KEPT** — calibration/known-answer, not re-litigation; R8 re-proposal bar unmodified. (b) MCL TAS re-open **CONFIRMED, narrow** — BE3's fade-scoped kill does not bar a TNEC-limb-scored TAS candidate; direction re-opens **only through a completed δ-extraction probe** (free CME TAS volumes, non-circular) — live, unowned next step; full intake chain still applies. [`closure`](docs/briefs/closures/Q-TNEC-ENV-1-closure.md)
- **2026-08-11** — **`Q-TNEC-ENV-1` closed `NULL` (H_B=0, STOP per PREREG F7) at $0.** Census pass (56 cells, 19 entries scored: 2 authored + 17 prior-census re-scores) found 0 SEED-GRADE; envelope (RESULTS.md §2) stands as documentation only. Key findings: mandated flows mostly name a spread direction an outright envelope can't admit; the re-scored 2026-07-26 census is δ-blind by its own construction; MCL settlement-window replication has a non-circular δ-probe route (CME TAS, free). Two items flagged for operator ruling, not adjudicated. Re-entry bar: new flow class or newly measured instrument, never a re-pass. [`closure`](docs/briefs/closures/Q-TNEC-ENV-1-closure.md) · [`RESULTS`](lab/archive/tnec_envelope_compile_2026-08/RESULTS.md)
- **2026-08-11** — **`Q-TNEC-ENV-1` Phase A executed at $0.** TNEC envelope compiled for {MNQ, MYM, MES, MGC, M2K, MCL, M6A}; H_A **NON-EMPTY**. Phase B census pass authorized (PREREG F7). [`RESULTS`](lab/archive/tnec_envelope_compile_2026-08/RESULTS.md) · [`PREREG`](lab/archive/tnec_envelope_compile_2026-08/PREREG.md)
- **2026-08-10** — **Temporal selectivity ruled OUTSIDE the mapped cost-ratio levers (`TEMPORAL-SELECTIVITY-OPEN-2026-08-10`, JA); dense-1m lane door-check REPAIRED.** "instrument-selection" = **cross**-instrument (provenance: cross-index RV dilution, +2.64 vs +5.19 bp) — within-instrument *moment* choice was never mapped ⇒ route ① open, under a priori-criterion + K-per-axis + F2-guard conditions. Price/hold-time stay exhausted; cross-index stays closed. Lane step **1a** now requires the executed profile consult (exit 1 when a prior binds) with every `BINDING BAR` answered by route — unanswered blocks the G0 freeze. Cell #3 is unblocked but **unauthored**; fresh Q-ID + G0 + explore GO is the path. [`ADR`](docs/adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md) · [`lane spec`](docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md)
- **2026-08-10** — **Dense-1m cell #3 cheap falsifier → `FALSIFIED` (exit-geometry lever) at $0; no G0 authored, no Q-ID spent — and the lane WAS blocked on an unbinding-gate finding (ruled + repaired same day, above).** Stop width cannot rescue the family (0.02–0.10× the 5.64-pt 4× bar across the whole ratified 5–20 pt band; CON-2's own basis 0.16–0.17×). Surviving lever is **trade count** — a once-per-session rule needs only **3.3%** of the perfect-foresight oracle (170 pt/session) vs ~20% at CON-2's ~6/day. ⚠ **The lane spec / CON-1 / CON-2 never cite the live `tier=always` [index-intraday-OHLCV raised bar](docs/rejected_candidates.md)** — both prior campaigns ran unbound (`lesson_gate_reachability_preregistration`, unbinding form, **5th firing**). Cell #3's only surviving design is OHLCV price-selectivity ⇒ fails the bar's route ①; route ② PAUSED (L1); route ③ unclearable ex ante. **Two operator items owed: a domain-bar ruling on within-instrument temporal selectivity, and the step-1 door-check repair.** [`falsifier`](lab/analysis/c1/cheap_falsifiers_2026-08/_cheap_falsifier_cost_geometry_2026-08-10_LOG.md) · [`lane spec intercept`](docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md)
- **2026-08-10** — **`Q-TNEC-CON-2` explore GO → `AMBIGUOUS-HOLD` (non-promotable) at $0.** Compression→break, dense-1m MNQ @ G=10: long net **−0.0507R** (n=4,321) / short **−0.0440R** (n=4,108), CIs straddle 0; **gross +0.90/+0.97 pt/trade eaten by the 1.41-pt RT** (0.65× vs 4×); halves sign-flip both arms. CONFIRM (2025-09-01→2026-08-05) reserved+unread; split+placebo+downgrades declared at GO pre-score; Cap not claimed; K=1 disclosure. Cell #3 needs a fresh G0 aimed at cost geometry. [`closure`](docs/briefs/closures/Q-TNEC-CON-2-closure-ambiguous-hold.md) · [`RESULTS_g2`](lab/analysis/c1/mnq_tnec_con2_compression_break_2026-08/RESULTS_g2.md)
- **2026-08-10** — **`implied_annualized_sr` PROMOTED report-only → gate (`IMPLIED-SR-GATE-2026-08-10`, JA in-session); Tradeify-native fade design-region CLOSED on its own arithmetic.** Freeze-time limb for any assumed-edge region (ceiling 1.83 CFD-era, futures-native 0.89 disclosed); measured-edge candidates untouched (DSR-at-K governs). Floor 2.98 as-ruled / 2.11 elective-ablated — zero admissible cells either way. $0/K=0. [`ADR`](docs/adr/2026-08-10-implied-sr-plausibility-gate.md)
- **2026-08-09** — **GRAND tier `Accepted` + GSUB-1 CLOSED `RESOLVED-LOADBEARING` (JA in-session, same day).** Quintessentials bound above STRATEGIC (pursuit domain; PARK re-entry+expiry; SUBTRACT armor; intake rule). 37-row inventory → **19 dispositions ratified** (8 PARK · 9 SUBTRACT · 2 MERGE) → 37 records at `docs/pursuits/`; 3 user-skill dirs archived+removed; ADR §4 satisfied (sunset did not arm). $0/K=0; no live-risk surface touched. [`ADR`](docs/adr/2026-08-09-grand-tier-quintessentials-binding.md) · [`closure`](docs/briefs/closures/GSUB-1-closure-resolved-loadbearing.md)
- **2026-08-09** — **`Q-MNQDTL-CON-1` explore GO → `FALSIFIED` (STOP catalogue) at $0.** ES−NQ 5m log divergence @ G=10 session-flat: long mean_R **−0.106** CI entirely &lt;0 (n=10,093); short **−0.111** (n=9,000); stop ~91%; TNEC `U U U F U`. Cap not claimed. [`closure`](docs/briefs/closures/Q-MNQDTL-CON-1-closure-falsified.md) · [`RESULTS`](lab/archive/mnq_con1_dense1m_stage0_2026-08/RESULTS.md)
- **2026-08-09** — **`Q-MNQDTL-CON-1` ENTRY named + explore harness wired.** ES−NQ 5m log-return divergence (relative contrarian) frozen in [`PREREG_G0`](lab/archive/mnq_con1_dense1m_stage0_2026-08/PREREG_G0.md); cheap falsifier `CHEAP_FALSIFIER_OK`; path-PnL scorer GO-gated (now discharged). Cap not claimed. PR [#699](https://github.com/Joshua-Asante/first-passage-archive/pull/699).
- **2026-08-08** — **PR693 parallel integrate:** CapFLOW Cap-spend path **BLOCKED** on join (estimate ~USD1.47 OK; Cap held). Construct Stage-0 geometry frozen; ENTRY later named 2026-08-09 (see above). [Cap RESULTS](lab/analysis/c1/mnq_capflow_orb_r_2026-08/RESULTS.md) · [Con PREREG_G0](lab/archive/mnq_con1_dense1m_stage0_2026-08/PREREG_G0.md) · PRs #695/#697/#696/#699
- **2026-08-08** — **TNEC-1 intake gate `RATIFIED` + edge-cohort ADR `Accepted` (§8 JA).** TNEC supersedes MNQDTL-1 **as intake gate** (MNQDTL stays RATIFIED historical; C1–C11 stand). `Q-CAPRES-2` reservation GO signed; Cap-spend / CapFLOW unpaid. Construct Stage-0 geometry frozen; ENTRY named 2026-08-09 (see board top). [`ADR`](docs/adr/2026-08-08-edge-cohort-correction-and-necessity-retarget.md) · [`TNEC-1`](docs/spec/2026-08-08-tradeify-necessary-conditions-target-spec.md) · [`Q-CAPRES-2`](docs/briefs/Q-CAPRES-2-mnq-cap-seat-reservation.md) · [`Q-MNQDTL-CON-1`](docs/briefs/Q-MNQDTL-CON-1-dense-1m-em-construct-scoping.md)
- **2026-08-08** — **Absolute path items 1–3 landed:** `Q-MNQSEL-2` Phase-0 `RESOLVED` (dense 1m G=10; S3 ≈0.858 both arms); `Q-CAPRES-2` Cap reservation unpaid + CapFLOW PREREG frozen unpaid; `Q-MNQDTL-CON-1` construct scoping unpaid; `Q-R2FLOW-1` closed FALSIFIED. $0 / Cap not re-spent. [`MNQSEL-2 RESULTS`](lab/analysis/c1/mnq_selection_ceiling_allbars_2026-08/RESULTS.md) · [`Q-CAPRES-2`](docs/briefs/Q-CAPRES-2-mnq-cap-seat-reservation.md) · [`Q-MNQDTL-CON-1`](docs/briefs/Q-MNQDTL-CON-1-dense-1m-em-construct-scoping.md)
- **2026-08-08** — **`Q-R2FLOW-1` explore GO → G2 `FALSIFIED` (STOP catalogue) at $0.** Clock-minute net signed aggressor size→60s mid: n **48,360**/48,360 coverage **100%**; ρ **−0.000701** CI includes 0; empty candidates. CONFIRM untouched; Cap not claimed. Re-proposal = new G0. [`RESULTS_g2`](lab/archive/mnq_r2flow_routeb_2026-08/RESULTS_g2.md) · [`brief`](docs/briefs/Q-R2FLOW-1-signed-minute-flow-route-b-scoping.md)
- **2026-08-08** — **`Q-R2AGRUN-1` CLOSED non-promotable (`AMBIGUOUS-HOLD`); `Q-R2FLOW-1` G0 frozen — explore GO unpaid.** Clock-minute net signed aggressor size → 60 s mid; K=1; OFCHAN cache; S6 ADMIT; Cap not claimed. [`closure`](docs/briefs/closures/Q-R2AGRUN-1-closure-ambiguous-hold.md) · [`brief`](docs/briefs/Q-R2FLOW-1-signed-minute-flow-route-b-scoping.md) · [`PREREG_G0`](lab/archive/mnq_r2flow_routeb_2026-08/PREREG_G0.md)
- **2026-08-08** — **`Q-R2AGRUN-1` explore GO → G2 `AMBIGUOUS-HOLD` (ITERATE) at $0.** Aggressor-run→60s mid: n **22,304,297**/22,304,297 coverage **100%**; ρ **−0.001306** CI excludes 0 / placebo PASS; \|ρ\| < 0.02 → empty candidates. CONFIRM untouched; Cap not claimed. [`RESULTS_g2`](lab/analysis/c1/mnq_r2agrun_routeb_2026-08/RESULTS_g2.md) · [`brief`](docs/briefs/Q-R2AGRUN-1-aggressor-run-length-route-b-scoping.md)
- **2026-08-08** — **`Q-R2AGRUN-1` G0 frozen (MNQDTL R2) — signed aggressor-run trade-count → 60 s mid; explore GO unpaid.** K=1; `N_min=2` a priori; OFCHAN `tbbo` cache reuse; CONFIRM `2025-09-01→2026-02-06`; S6 ADMIT; Cap not claimed. [`brief`](docs/briefs/Q-R2AGRUN-1-aggressor-run-length-route-b-scoping.md) · [`PREREG_G0`](lab/analysis/c1/mnq_r2agrun_routeb_2026-08/PREREG_G0.md)
- **2026-08-08** — **Quarterly dd_protection/regime review run: item 1 (C2→C0 revert check) confirmed dead, removed from the `fwd-quarterly-regime-ddrevert` cron.** Re-verified via direct execution: `time_to_pass.py --regime-check` now hard-errors (Pepperstone anchor retired), consistent with the 2026-07-22 D2 retirement — not a new decision, just closing the loop the cron kept re-asking. Item 2 (H1 HOLD §4 regime trigger) re-run: limb-2 reachability still `NOT_EXECUTABLE`; full-panel de-risk candidates re-confirmed `GATE FAIL` byte-identical to the ADR. HOLD unchanged; no `core/` edits. [`decompound ADR`](docs/adr/2026-06-07-decompound-remc-hold.md) · [`claims-rescope ADR`](docs/adr/2026-07-11-challenge-era-claims-rescope.md)
- **2026-08-08** — **ADR ceremony stakes-tiering `Accepted` (JA).** Full §0–§7 only when a limb fires (K/$ · live-risk · locked/non-regenerable · doctrine); else ≤300-word light record, same header block. Falsifier ≥⅕ light share + zero omitted-apparatus incidents, review rides first quarterly audit after 08-08. Forward-only. [`ADR`](docs/adr/2026-08-08-adr-ceremony-tiering.md)
- **2026-08-08** — **`Q-R2VBUCK-1` explore GO ratified (MNQDTL R2) → G2 `FALSIFIED` (STOP catalogue) at $0.** Volume-bucket aggressor→60s mid on OFCHAN EXPLORATION cache: n **77,656**/77,656 coverage **100%**; ρ **−0.005478** CI includes 0; empty candidates. CONFIRM untouched; Cap not claimed. Re-proposal = new G0. [`RESULTS_g2`](lab/archive/mnq_r2vbuck_routeb_2026-08/RESULTS_g2.md) · [`brief`](docs/briefs/Q-R2VBUCK-1-volume-bucket-aggressor-route-b-scoping.md)
- **2026-08-08** — **SPEC S2b `Accepted` + S2b build ADR `Accepted` + operator build GO.** Daemon minimal spec Accepted as-is ($0); build ADR locks Databento Live `ohlcv-1m`, `2×bar_period+30s` staleness, fail-closed-all, second Fly app `c1-signal-daemon`, emit-disabled default. Build GO licenses code + warm deploy only — no arming, no Striker redeploy, no M1 fabrication. [`SPEC S2b`](docs/spec/2026-08-07-loop-s2b-python-signal-daemon-spec.md) · [`build ADR`](docs/adr/2026-08-08-s2b-signal-daemon-build.md)
- **2026-08-07** — **Loop S1 environment ratification `Accepted` — F2+F3 ruled.** Incumbent `Tradeify_Select_100K` eval = environment for **new** strategies; rail kept warm/disarmed there; no successor migration now; Q-VENUEGEO-1 evidence recorded, unconsumed; withdrawn Striker legs stay barred. Board F2/F3 rows cleared. MNQDTL-1 R1 foreclosed; R2 live. $0/K=0/no arming. [`S1 ADR`](docs/adr/2026-08-07-loop-s1-environment-ratification.md) · [SPEC S1](docs/spec/2026-08-07-loop-s1-environment-ratification-spec.md)
- **2026-08-07** — **Closed-loop programme spec series S1–S6 `PROPOSED` + minimal-spec style ratified as the standing `docs/spec/` convention (JA).** Eight files: [template](docs/spec/TEMPLATE-minimal-spec.md) · [index](docs/spec/2026-08-07-loop-spec-index.md) · S1–S6 (environment ratification → signal-host fork → two-tier arbiter → sensor layer → bounded promotion lane → K-aware generation). Commissions only — admits nothing, arms nothing, spends nothing; $0/K=0. S1 direction (same day) later Accepted as the F2/F3 ADR above. S5 commissions a supersedes-in-part ADR on lifecycle Call 5 / M1 §5 / harvest §1 — **nothing is superseded until that ADR is Accepted**. 9-agent adversarial verification (25 findings, 5 BLOCKERs) applied pre-commit. **Same day: blast-radius sweep (7 agents) → [S7 alignment spec](docs/spec/2026-08-07-loop-s7-repo-alignment-spec.md) + propagation manifest (`git show 45e3ceac:docs/notes/2026-08-07-posture-a-alignment-manifest.md`) (~70 rows, 12 triggers); NOW repairs landed — S1 pointers on board rows 1/3, minimal-spec row in brief-authoring, gate-14 §4 friction datum #1 logged (Iterate ADR ledger) + Q-CAPA-1 `Board write:` token fixed.**
- **2026-08-07** — **`Q-MNQSEL-1` Phase-0 RUN → `FALSIFIED` (C2) at $0/K=0 — STOP this restart-clock universe.** Oracle top-1/day S3 long **0.3998** / short **0.3984** (both &lt; 0.40); S1 ≈ **−0.036** both arms; S5 median target-hits ≈ **97–98**/day; S6 ≈ **99.7–99.9%**. Pre-registered C4 expectation wrong. Re-proposal = different causal candidate set. Cap untouched. [`RESULTS`](lab/archive/mnq_selection_ceiling_2026-08/RESULTS.md) · [`brief`](docs/briefs/rnd-pipeline/Q-MNQSEL-1-selection-value-ceiling-scoping.md)
- **2026-08-06** — **EM0–EM5 mechanism-shape screen `RATIFIED`; §7 dispositions locked; first Route B G0 drafted as `Q-OFCHAN-1` — G2 `VOID-COVERAGE` (empty candidates; STOP).** Screen [`docs/spec/2026-08-05-eval-mechanism-shape-screen.md`](docs/spec/2026-08-05-eval-mechanism-shape-screen.md) Status `PROPOSED` → `RATIFIED 2026-08-06` / JA; §7 rows 1–9 ruled. First Avenue A Route B campaign: [`Q-OFCHAN-1`](docs/briefs/Q-OFCHAN-1-orderflow-channel-route-b-scoping.md) + [`PREREG_G0`](lab/analysis/c1/mnq_ofchan_routeb_2026-08/PREREG_G0.md) — K=1 L1 flicker-filtered imbalance → 60s mid return on `MNQ.v.0` RTH grid; EXPLORATION batch complete; **G2** [`RESULTS_g2`](lab/analysis/c1/mnq_ofchan_routeb_2026-08/RESULTS_g2.md) coverage **7.36%** → VOID-COVERAGE → empty list → STOP this catalogue (new G0 to reopen). Cap seat not claimed. CONFIRM untouched.

> ⚠ **Truncated to the newest 15 at the 2026-08-08 Great Prune.** Older executed decisions are
> owned by their ADRs (`docs/adr/`, tombstoned rows in [`TOMBSTONES.md`](docs/adr/TOMBSTONES.md));
> full prior index: `git show pre-prune-2026-08-08:STATE.md`.

## Dormant cross-session threads

Open investigations with no current session home. Closed threads leave (owners =
closures/ADRs).

Dormant threads b6/b7 (PARK — open) → [`docs/pursuits/`](docs/pursuits/) (ratified 2026-08-09, GSUB-1
Phase 3). c5/Q-MSCHAN-1 (SUBTRACT — dead) left this section per its own rule above; its record
stands alone at [`c5`](docs/pursuits/c5-q-mschan-1.md).

**Registry backfill debt (2026-08-15).** 33 closures classified as strategy-grounds kills
(read against each one's actual `**Verdict:**` line, not filename) never got a
`rejected_candidates.md` row — the 2026-08-03→08-11 feed-stop the registry-feed sub-rule
(9) was written to close. Forward-only: nothing new accretes here. Backfill is one
judgment call per row (which heading, how it's worded) and stays operator-paced —
`python scripts/check_closure_disposition.py --list-debt` lists the current set;
rows leave this debt only by landing in `docs/rejected_candidates.md`, not by editing
`REGISTRY_DEBT_2026_08` directly.

---

## Scheduled forward triggers

Canonical dates/criteria live with their owners; this board is a pointer so
obligations are not lost between sessions. Closed/retired/discharged rows are
deleted (not struck).

### Weekly — recurring (rolling; next deadline **2026-08-21**, bucket 08-17→08-21)

> Prior week 08-10→08-14 satisfied (operator-placed 2026-08-12). New week unpaid. Row stays
> live — roll this date forward each Monday.

- **Venue idle-clock — ≥1 operator-placed trade per Mon–Fri week on the live account (identifier
  redacted from the public tree).**
  Consequence of a miss is account **DELETION, not a warning** (Tradeify art. 10468318; venue day
  is 6pm-anchored, so a Fri 18:30 ET fill belongs to the *next* session). ⚠ **No agent may place
  it** — operator-placed at the venue; the rail is not the instrument (`dry_run` stays `true`).
  **Roll this date forward each Monday.** Booked here 2026-08-09 *specifically so the existing
  daily 07:04 `daily-repo-truth-sync` forward-obligation radar surfaces it* — that task reads this
  section for obligations dated within 7 days, and row 0's queue-table placement was invisible to
  it.   [`S1`](docs/adr/2026-08-07-loop-s1-environment-ratification.md) ·
  [audit FU-1](docs/notes/audits/programme-audit/2026-08-05-post-descope-claim-alignment-audit.md)

### No fixed date / gated

> ⚠ **Five threads are gated on first strategy-signal fill.** That gate is **an acceptable
> strategy**, not a missing venue. [`S1`](docs/adr/2026-08-07-loop-s1-environment-ratification.md)
> kept the incumbent `Tradeify_Select_100K` eval as the environment; the weekly idle-clock is
> live; there is no c1 book (locked Striker legs stay barred). **Q-SIGID-1** is **not** among
> them — pursuit standing **KEEP**, resolving via the S2b daemon; see [`c2`](docs/pursuits/c2-q-sigid-1.md).
> **Three have rows in the list below** — **PREREG-C1-DEDUPE-1**, **per-fill add-slippage
> capture (B7 Stage 2b)**, and the **forward regime-monitor successor**. **Two do not, and
> are re-homed here** because their only prior home was the deleted operator-queue row 3:
>
> - **lifecycle Call-1** — rolling-PF σ-source has no live data until a strategy is on the
>   book. Its 2026-08-08 review row below still stands but can only return AMBIGUOUS on thin data.
> - **ORB decay re-scope** — no other row in this file; recorded here so the deletion of queue
>   row 3 does not silently lose it.
>
> All five wait on the same thing as queue row 2 (B7 / M1). They are not closed, not
> discharged, and not re-homed to a successor venue — F3 was no-migration (S1).
> [`S1`](docs/adr/2026-08-07-loop-s1-environment-ratification.md) ·
> [`ADR 2026-08-04`](docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md) (Striker-book bar)

- **Sentinel Tier-2/3 promotion (limb B1)** — before next quarterly slate; promotion not a build. [`sentinel design`](docs/spec/2026-06-23-inqhiori-sentinel-design.md) · [`Hermes closure`](docs/briefs/closures/2026-07-27-hermes-agent-adoption-closure-resolved.md)
- **PREREG-C1-DEDUPE-1** — gated on M1 `RESOLVED` + separate operator GO. [`pre-reg`](docs/spec/PREREG-C1-DEDUPE-1-intent-key-functional-property.md) · [`impl plan`](docs/spec/PREREG-C1-DEDUPE-1-implementation-plan.md)
- **R&D tooling T2 / T3 / T4** — adoption ADR §7 (T4 rides 2026-08-08 Call-1 OC). [`ADR §7`](docs/adr/2026-07-11-tradable-anomalies-statistics-adoption.md)
- **A4 crowd-vs-death footprint diagnostic** — handoff authored, not yet dispatched. [`handoff`](docs/briefs/handoffs/2026-07-14-cursor-handoff-a4-crowd-vs-death-diagnostic.md)
- **Per-fill add-slippage capture (B7 Stage 2b)** — waits first strategy-signal **add** fill; prerequisite ledger price-capture landed. [`Q-COSTGEO-3`](docs/briefs/closures/Q-COSTGEO-3-closure-ambiguous-needs-depth.md) · B7 procedure in the private archive
- **Forward regime monitor / decompound limb-2 successor** — ORPHANED same hole: CFD limb-2 cannot fire; venue-native design landed (not ratified); gated on first live fill. [`decompound ADR §Addendum 2026-08-03`](docs/adr/2026-06-07-decompound-remc-hold.md) · [`Pepperstone retirement`](docs/adr/2026-08-02-pepperstone-feed-retirement.md)
- **CFD data-estate class-wide delete** — trigger-dated; blocked on T1 (F3 FUTURES_LOCK) + substrate Phase-6 confirm. [`CFD estate ADR`](docs/adr/2026-07-11-ops-cfd-estate-retirement.md) · [gate audit](docs/notes/audits/2026-07-17_gate_cfd-estate-classwide-delete.md)
- **Mechanism-sourcing radar** — on-demand cadence; 08-08/11-08 = progress/idle checkpoints; idle guard 2026-11-08. [`harvest §2`](docs/methodology/strategy_harvest.md)
### 2026-08-08 — DISCHARGED

> ✅ **The quarterly vehicle ran 2026-08-08.** Verdicts, the full rider partition
> (2 discharged / 37 owed / 3 moot / 5 unfalsifiable of 47), the unfalsifiable-check census, and
> every named follow-up now live in
> [`2026-08-08-quarterly-audit.md`](docs/notes/audits/programme-audit/2026-08-08-quarterly-audit.md).
> The former ~90-line rider blockquote is deleted per the retention test — it restated obligations
> the audit note now owns. **Operator rulings still open** are carried as queue rows, not here.

### 2026-10-11 (approx.)

- **prop_envelope §4 overlay 90-day re-verify** — rows verified 2026-07-13; stale after ~2026-10-11. [`prop_envelope`](ops/prop_envelope_default.md) · [`ratification ADR`](docs/adr/2026-07-13-prop-envelope-v1-ratification.md)

### 2026-11-08

- **ADR ceremony-tiering §Falsifier review** — first quarterly programme audit after 2026-08-08; check light share ≥⅕ and dated omitted-apparatus incidents (incl. 2026-08-14 candidate: implied-SR light records). Count 1-vs-2 is operator/audit. [`ADR addendum`](docs/adr/2026-08-08-adr-ceremony-tiering.md)
- **GRAND-tier ADR §4 scheduled re-read** — H already satisfied 2026-08-09 (19 ratified differences; tier load-bearing, sunset did **not** arm). This slate is the first scheduled re-check, not a sunset. [`ADR addendum`](docs/adr/2026-08-09-grand-tier-quintessentials-binding.md) · [`closure`](docs/briefs/closures/GSUB-1-closure-resolved-loadbearing.md)
- **GSUB-1 PARK expiries (8)** — b1 Aegis→6J · b2 Striker-MYM · b3 ORB-MNQ line · b5 Q-FUNDPOL-1 · b6 Q-NAS-ECR-1 · b7 ICT line · c1 Q-XMEM-1 · c3 Q-TOM-SPX-1. Each converts to SUBTRACT absent explicit operator renewal (ADR §2.3). [`docs/pursuits/`](docs/pursuits/)
- **Guardian-MGC (R7) transfer lane — SUBTRACT / DEAD(N-SURV) 2026-08-11** — exploratory N-SURV FAIL (full 42.2% / H1 72.4% / H2 16.5% bust vs ≤3.0%); margin-decisive; retroactive cell PREREG + typed closure filed. Re-entry = new mechanism evidence (not param retune). [`b8`](docs/pursuits/b8-guardian-mgc-transfer-lane.md) · [`closure`](docs/briefs/closures/2026-08-11-guardian-mgc-transfer-cell-dead-nsurv.md)
- **Prop-portfolio §4 primary falsifier (HARD)** — ≥1 candidate clears bust ceiling on ≥2 of 4 FRIENDLY firms; else demote program to research-only. Status undischarged (2026-07-22 withdrawal). [`four-firms ADR §4`](docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md) · [`withdrawal ADR`](docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md)
- **Mechanism-boundaries ADR §4** — clauses 2-A / 2-B / 2-C first check. [`ADR`](docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md)
- **Harvest-intake §4 doctrine falsifier + idle guard** — doctrine count still open (0-of-2 counting); idle = zero screen-PASS seeds beyond D5. [`harvest ADR §4`](docs/adr/2026-07-15-external-mechanism-harvest-intake.md)
- **Regime-monitor successor §6 gate** — if no live fill by 11-08, gap is ≥3 months; re-raise as standing-unfalsifiable in that programme audit. [`decompound ADR`](docs/adr/2026-06-07-decompound-remc-hold.md)
