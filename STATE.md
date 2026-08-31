# STATE — First Passage

**Last curated:** 2026-08-31

This file is the **open-threads + forward-obligation register** — cross-session
items with no other home, plus the forward-trigger board. It is **not** a state
snapshot: it carries no risk %, MC anchor, strategy version, hash, working-tree
status, or canonical-owner table. Those live with their owners — see
[`docs/operational_rules.md`](docs/operational_rules.md) §7.

For uncommitted work: `git status`. For history: `git log`. For session narrative
and the live **Open / next**: [`docs/SESSIONS.md`](docs/SESSIONS.md) (read its top
entry first).

**Anti-accretion (standing):**

- New operator decision → **one line + owning ADR** (never a paragraph here) —
  [`docs/operational_rules.md`](docs/operational_rules.md) Rule 7.
- Item leaves the queue or closes → **delete the STATE row**; do not leave
  “Cleared …” footnotes.
- Forward triggers: date/criterion + owner link only; detail stays with the owner.
- Retention test for every row: *open or still owed, and no other home.* If either
  fails, it leaves.
- **Entry classes + ~40-word soft target (W5 direction, not an enforced cap):** Decision /
  Build / Measurement / Hygiene — see [`W5 ADR`](docs/adr/2026-08-07-w5-governance-diet.md);
  prefer links over prose.

**Standing base case:** absent an N-clear candidate, the 2026-11-08 §4 falsifier
(prop-portfolio program) reads **FALSIFIED** — the four-firms ADR's demotion clause is
the designed, legitimate outcome if the date passes without one. See
[`N-2026-08-18-iteration2-identify-notice.md`](docs/notes/notice/N-2026-08-18-iteration2-identify-notice.md) §0.

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
| 1 | **Acceptable strategy on the ruled host** — viable-strategy sequence; Phase A (A1+A2) executed 2026-08-23 (revival list empty, A3 voided; feasibility region published, FEASIBLE ≥~65-70% win rate). Phase B (mechanism supply) is now the next doable packet (GO unpaid). Queue placement is not a phase GO | [`overview`](docs/superpowers/plans/2026-08-23-viable-strategy-sequence-overview.md) · [`Phase B`](docs/superpowers/plans/2026-08-23-viable-strategy-phase-b-mechanism-supply.md) · [`A2 RESULTS`](lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS.md) | production book (not M1 item 5) |
| 2 | **B7-REFIRE Stage 1 + M1** — item 5 dated 2026-08-24; test strategy licensed. Does not wait on #1. No arm | [`M1 addendum`](docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md#addendum-2026-08-24--test-strategy-licensed-for-item-5-dated-08-24) · [`GO addendum`](docs/adr/2026-07-17-c1-rail-build-account-registration-go.md#addendum-2026-08-24--test-strategy-is-a-qualifying-strategy) · [`S2`](docs/adr/2026-08-07-loop-s2-signal-host-fork.md) | live-signal / arming path |

Off-queue leftovers stay on their owner artifacts. Re-entry is promote to a numbered queue row and drop something else (cap ≤5). When a doable row leaves, do not auto-open a replacement — cite remaining rows until the operator promotes one.

---

## Executed operator decisions — decision index

ADRs own the decision narrative ([`docs/operational_rules.md`](docs/operational_rules.md)
Rule 7; [`docs/adr/2026-07-16-root-doc-charter-dedup.md`](docs/adr/2026-07-16-root-doc-charter-dedup.md)).
One line per executed decision, newest first — consequence + owner. Posture summary:
[`CLAUDE.md`](CLAUDE.md) §Live-execution posture.

Newest **15** live here. Older bullets: [`archive`](docs/ltm/notes/archive/state/STATE-decision-index-pre-2026-08-23.md) (P8 keep-15 roll, 2026-08-23; rolled 2026-08-27, 2026-08-29, twice on 2026-08-30, and 2026-08-31).

- **2026-08-31** — `Q-RANGECOND-1`'s `RESOLVED` verdict **retracted, corrected to `FALSIFIED`**. Codex's [PR #227](https://github.com/Joshua-Asante/first-passage/pull/227) review found `data_lib.py::overnight_ohlc` (MNQ-side only) had a look-ahead defect — it included bars from after the outcome it was meant to predict. Corrected: WR diff +24.75pp → +0.75pp (CI now includes 0), mean-win diff +0.711R → -0.058R (sign-flipped). Root cause fixed; addendum on `b3-orb-mnq-payability-line.md` retracted; `ORB-MNQ-1` stays `PARKED`, no new evidence. `Q-RANGEXFER-1`'s own closure verdict is unaffected (MYM's conditioner never had this defect; MNQ's presence battery still passes both affected hypotheses at corrected, weaker magnitudes). [`corrected closure`](docs/briefs/closures/Q-RANGECOND-1-closure-falsified.md) · [`defect audit`](docs/notes/audits/2026-08-31-mnq-overnight-window-lookahead-defect.md)
- **2026-08-30** — `Q-RANGECOND-1` closed `RESOLVED` — overnight-range-conditioned `ORB-MNQ-1` win rate 66.47% vs unconditioned 41.72% (+24.75pp, CI excludes 0), mean win +0.711R lift (CI excludes 0), n_conditioned=340. New payability evidence at Tradeify on `ORB-MNQ-1` as a standalone leg (the estate's top queue priority, `#1`); disclosed panel-vintage caveat (current `MNQ_M15.csv` ~300 days shorter than the strategy's own original G8 admission panel). Addendum filed on `b3-orb-mnq-payability-line.md`; full re-MC named as next step, needs its own operator GO + K + panel-vintage decision. No entry construct licensed yet; no `core/`/Pine/allocation/`dd_protection`/rail change. $0/K_intrinsic=1. [`closure`](docs/briefs/closures/Q-RANGECOND-1-closure-resolved.md) · [`pursuit addendum`](docs/pursuits/b3-orb-mnq-payability-line.md)
- **2026-08-30** — `Q-RANGEXFER-1` closed `MIXED` (4× `AMBIGUOUS-DESIGN`, 1× `FALSIFIED` on `H-RANGEXFER-1.a-MYM`). Operator ratified L5-gates-`FALSIFIED` (Option A) + a per-hypothesis `AMBIGUOUS-DESIGN` closure row; the joint-surrogation null's hard stop (measured 26% Type-I vs nominal 5%, Round 4) made this the correct route rather than force-fitting `AMBIGUOUS-HOLD`. Presence battery (L1–L3) adversarially verified before scoring. No entry construct licensed; `Q-VOLREGIME-1` independently assessed, not closed by inheritance. $0/K=0. [`closure`](docs/briefs/closures/Q-RANGEXFER-1-closure-ambiguous-design.md) · [`pre-reg §H`](docs/briefs/pre-registration/Q-RANGEXFER-1-verdict-preregistration.md)
- **2026-08-29** — SSOT Phase 3 authorized (cost-model closed-world partition). Bars checker voided; ledger join and firm_rules dollars declined. No queue row. $0/K=0. [`ADR addendum`](docs/adr/2026-08-27-ssot-data-lineage-remediation-program.md#addendum-2026-08-29--phase-3-authorized-cost-model-closed-world-partition) · [`plan`](docs/superpowers/plans/2026-08-29-ssot-phase-3-cost-model-closed-world.md)
- **2026-08-29** — SSOT Phase 2 authorized (A8 intra-ADR running-count consistency). Recon (a)(b)(c) answered: no fourth instance; STATE-join and HTML-comment schema declined. No code/risk-constant/allocation touched. $0/K=0. [`ADR addendum`](docs/adr/2026-08-27-ssot-data-lineage-remediation-program.md#addendum-2026-08-29--phase-2-authorized-a8-intra-adr-running-count-consistency) · [`plan`](docs/superpowers/plans/2026-08-29-ssot-phase-2-running-count-mirror.md)
- **2026-08-27** — SSOT/data-lineage remediation program ratified (operator GO); Phase 1 (4 gate/tooling tasks) authorized and dispatched. No code/risk-constant/allocation touched. $0/K=0. [`ADR`](docs/adr/2026-08-27-ssot-data-lineage-remediation-program.md) · [`plan`](docs/superpowers/plans/2026-08-27-ssot-data-lineage-remediation.md)
- **2026-08-24** — Regime-gate scope ratified + F1 discharged; validation-battery K-tiering, cost-law split, `pursuit-records` retired. Worked non-example lands on the Class-S candidate-1 rider chain, not ORB-MNQ-1 as originally proposed (verified against production). No code/risk-constant/allocation touched. $0/K=0. [`ADR-A`](docs/adr/2026-08-24-regime-gate-scope-worked-nonexample-f1-discharge.md) · [`ADR-B`](docs/adr/2026-08-24-validation-battery-k-tiering-and-gate-retirement.md) · [`PR #163`](https://github.com/Joshua-Asante/first-passage/pull/163)
- **2026-08-24** — A2 disclosed-N reduction accepted (consistency-plan Packet 0). Published region is the screen. Not a Phase B GO. [`A2 RESULTS §4`](lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS.md) [`plan`](docs/superpowers/plans/2026-08-24-viable-strategy-surface-consistency.md)
- **2026-08-24** — M1 item 5 dated 08-24; test strategy licensed (evaluate-hook → B1, `dry_run`). `#2` no longer waits on `#1`. No arm. [`M1 addendum`](docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md#addendum-2026-08-24--test-strategy-licensed-for-item-5-dated-08-24) [`Survive-bound addendum`](docs/adr/2026-08-09-survive-bound-is-the-queue-cap.md#addendum-2026-08-24--m1-item-5-no-longer-waits-on-queue-1)
- **2026-08-24** — Operator queue: mechanism supply is `#1`; B7/M1 is `#2` (waits on #1). Placement is not a phase GO. [`Survive-bound addendum`](docs/adr/2026-08-09-survive-bound-is-the-queue-cap.md#addendum-2026-08-24--the-blocker-of-b7m1-is-queue-1) [`overview`](docs/superpowers/plans/2026-08-23-viable-strategy-sequence-overview.md)
- **2026-08-24** — `Q-TRADECAP-2` closed `RESOLVED` — licensed close is frozen ID **2** (observe-only). Queue row 2 deleted (no auto-replace). No tripwire wire. [`elect-2`](docs/adr/2026-08-24-q-tradecap-2-elect-alert-tripwire.md) [`closure`](docs/briefs/closures/Q-TRADECAP-2-closure-resolved.md)
- **2026-08-23** — R1's `RESOLVED — WITH NAMED RESIDUAL` disposition ratified by operator, real-time GO ("done for what's live, openly incomplete for what isn't") — `Bulenox_100K`/`BluSky_Premium_100K` (what R3 actually consumes) are fully re-measured; the archived-campaign PASS-side residual stays un-re-run, not authorized for revival by this ratification. One item from the row below still open: A2's `sims_per_seed` reduction. [`ratification`](docs/superpowers/plans/2026-08-23-viable-strategy-parallel-s4-firm-repair.md)
- **2026-08-23** — Phase A GO executed (A1 kill-register audit: revival list empty, **A3 voided**; A2 payoff-shape feasibility map: region `FEASIBLE` from ~65-70% win rate up, Bulenox/BluSky `BLOCKED`) alongside the §4 firm-model-repair Q (R2: Bulenox Master lock does not bite the modeled horizon, comment-only fix; R1: `RESOLVED — WITH NAMED RESIDUAL`, WATCH-1 0.50× still clears despite a ~7.4× honest-clock deepening). Ox-alpha sanitized review of the three hardest judgment calls reconciled — one concrete objection (a possible scorer bug) independently checked and does not survive. Two items await operator sign-off: R1's self-rewritten Gate line; A2's disclosed `sims_per_seed` reduction under a compute-budget wall. [`SESSIONS 2026-08-23h`](docs/SESSIONS.md) [`A1 audit`](docs/notes/audits/2026-08-23-kill-register-attribution-audit.md) [`R1 RESULTS`](lab/analysis/c1/firm_model_repair_r1_7tier_2026-08-23/RESULTS.md)
- **2026-08-23** — Pain-point residuals P6–P10 landed (README lead · identifier table · STATE keep-15 · withdrawn-book tense · Q-TOM-SPX-1 DEAD). [`impl plan`](docs/superpowers/plans/2026-08-23-p6-p10-residuals-implementation.md)
- **2026-08-23** — Automatic Claude judgment review on non-draft Cursor-first (or opted-in) PRs that touch a governed surface; review-only, not merge. [`07-14 addendum`](docs/adr/2026-07-14-cc-cursor-surface-allocation.md#addendum-2026-08-23-judgment-review)
> ⚠ **Truncated to the newest 15 at the 2026-08-08 Great Prune.** Older executed decisions are
> owned by their ADRs (`docs/adr/`, tombstoned rows in [`TOMBSTONES.md`](docs/adr/TOMBSTONES.md));
> full prior index: `git show pre-prune-2026-08-08:STATE.md`.

## Dormant cross-session threads

Open investigations with no current session home. Closed threads leave (owners =
closures/ADRs).

Dormant threads b1/b3/b6 (PARK — open) → [`docs/pursuits/`](docs/pursuits/) (ratified 2026-08-09,
GSUB-1 Phase 3). b7 (ICT line) resolved to SUBTRACT 2026-08-20 and left this section (see the
2026-11-08 GSUB-1 PARK-expiries row below for the current count). c5/Q-MSCHAN-1 (SUBTRACT — dead)
left this section per its own rule above; its record stands alone at
[`c5`](docs/pursuits/c5-q-mschan-1.md).

**Registry backfill (2026-08-15).** Snapshot + unpaid enumerator:
[`scripts/check_closure_disposition.py`](scripts/check_closure_disposition.py)
(`--list-debt`).

---

## Scheduled forward triggers

Canonical dates/criteria live with their owners; this board is a pointer so
obligations are not lost between sessions. Closed/retired/discharged rows are
deleted (not struck).

### Weekly — recurring (rolling; next deadline **2026-08-28**, bucket 08-24→08-28)

> ✅ **This week's trade placed 2026-08-26** (round-trip, MNQU6, both legs filled; bucket
> 08-24→08-28 satisfied). Prior week 08-17→08-21 satisfied (operator-confirmed 2026-08-22). Row
> stays live — roll this date forward each Monday. **Recurrence ruled 2026-08-16** (decision
> index, above): re-electing coverage every week is the standing design, not an open question —
> this row's own weekly cadence is that design in practice, not a symptom of anything unresolved.

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

### Monthly — recurring (rolling; next deadline **2026-09-21**)

> **Recurrence ruled 2026-08-21** ([`ADR`](docs/adr/2026-08-21-cfo-subscription-ledger-consolidation.md)
> D3, operator: "reconfirm ledger once a month"): the same recurring-obligation shape as the weekly
> row above, reusing the same radar rather than standing up a second scheduling surface. **Roll this
> date forward each occurrence** (same day-of-month as this row's own creation, 21st).

- **Subscription-ledger reconfirm — `docs/pursuits/SUBSCRIPTION_LEDGER.md`'s seven d11-d17 rows
  re-checked against current reality.**
  Confirm each "Last confirmed" date and $/mo figure still holds; update any that changed; chase the
  two still-open rows (Fly.io, Tradeify) if a figure has since surfaced. A null result (nothing
  changed) is still a reconfirm — record it, don't skip it (CFO 2026-08-21 recommendation #4: silence
  is not evidence of currency). Booked here *specifically so the existing daily `daily-repo-truth-sync`
  forward-obligation radar surfaces it*, same mechanism as the weekly row above — no new
  infrastructure. [`ADR`](docs/adr/2026-08-21-cfo-subscription-ledger-consolidation.md) ·
  [`cfo.md`](docs/personas/cfo.md) (standing check + Writes field, D3) ·
  [`cfo-log.md`](docs/personas/cfo-log.md) (source recommendations, 2026-08-21)

### No fixed date / gated

> ⚠ **Monitoring obligations were recorded as one stranded "first live fill" class; `Q-MONSURF-1`
> (`RESOLVED` 2026-08-23) found they sit at three distinct gate depths — corrected here, not
> restated as before.** [`S1`](docs/adr/2026-08-07-loop-s1-environment-ratification.md) kept the
> incumbent `Tradeify_Select_100K` eval as the environment; the weekly idle-clock is live; there
> is no c1 book (locked Striker legs stay barred). **Q-SIGID-1** is **not** among any of the below
> — pursuit standing **KEEP**, resolving via the S2b daemon; see [`c2`](docs/pursuits/c2-q-sigid-1.md).
>
> - **M-B (idle-clock monitor) — gated on F3 (a registered account), NOT first live fill.**
>   `RESOLVED`/registration-ready: acceptance battery passed 0 missed / 0 spurious across all 312
>   real historical weeks, mutation-tested. No further design work owed — deploys alert-only the
>   moment F3 registers a successor venue (Phase 5: re-freeze idle-clock semantics against that
>   venue's own DP2-verified rules if they differ from the Tradeify-shaped provisional freeze used
>   here, then wire to the live account). [`closure`](docs/briefs/closures/Q-MONSURF-1-closure-resolved.md)
> - **M-C (ECR live-edge-capture monitor + per-fill add-slippage capture) — genuinely fill-gated.**
>   Correctly waits on first strategy-signal fill; row below, pointing at its own prereg.
> - **M-A (shadow market-data regime observer) — elective, not scheduled, gate itself unruled.**
>   Venue-free but low-consequence (alerts on a book that isn't trading). Whether the design's
>   own "first live fill" build gate binds a pure market-data observer (vs. only a fill-coupled
>   monitor) is an **explicit operator ruling still owed** — not assumed either way. Row below.
>
> **Two other threads share the same prior home** (deleted operator-queue row 3), unrelated to
> the monitoring triage above:
>
> - **lifecycle Call-1** — rolling-PF σ-source has no live data until a strategy is on the
>   book. Its 2026-08-08 review row below still stands but can only return AMBIGUOUS on thin data.
> - **ORB decay re-scope** — no other row in this file; recorded here so the deletion of queue
>   row 3 does not silently lose it.
>
> `PREREG-C1-DEDUPE-1` (row below) is unrelated to monitoring — waits on M1 `RESOLVED` + a
> separate operator GO, not on a live fill. Everything above except M-B waits on the same thing as
> queue #2 (B7 / M1); M-B alone is now gated on F3 only. Not closed, not discharged, not
> re-homed to a successor venue — F3 was no-migration (S1).
> [`S1`](docs/adr/2026-08-07-loop-s1-environment-ratification.md) ·
> [`ADR 2026-08-04`](docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md) (Striker-book bar)

- **Idle-clock monitor (M-B) — registration-ready, gated on F3 only** — Q-MONSURF-1 `RESOLVED`; standalone module built and acceptance-tested (0 missed / 0 spurious, all 312 real historical weeks, mutation-verified). No design work owed; wire to the live account at F3 registration (Phase 5 — re-freeze idle-clock semantics against the actual successor's DP2-verified rules first if they differ from the Tradeify-shaped provisional freeze). [`module`](lab/analysis/c1/msl_monsurf_1_idle_clock_2026-08/idle_clock_monitor.py) · [`closure`](docs/briefs/closures/Q-MONSURF-1-closure-resolved.md)
- **Sentinel Tier-2/3 promotion (limb B1)** — before next quarterly slate; promotion not a build. [`sentinel design`](docs/spec/2026-06-23-inqhiori-sentinel-design.md) · [`Hermes closure`](docs/briefs/closures/2026-07-27-hermes-agent-adoption-closure-resolved.md)
- **PREREG-C1-DEDUPE-1** — gated on M1 `RESOLVED` + separate operator GO. [`pre-reg`](docs/spec/PREREG-C1-DEDUPE-1-intent-key-functional-property.md) · [`impl plan`](docs/spec/PREREG-C1-DEDUPE-1-implementation-plan.md)
- **R&D tooling T2 / T3 / T4** — GO 2026-08-23 executed (kit + breadth calibration + synthetic Call-1 OC). T4 Task 3 state writer still fill-gated. [`ADR §7`](docs/adr/2026-07-11-tradable-anomalies-statistics-adoption.md) · [T4 RESULTS](docs/notes/research/2026-08-23-call1-oc-synthetic.md)
- **Per-fill add-slippage capture (B7 Stage 2b) — Q-MONSURF-1 M-C** — waits first strategy-signal **add** fill; prerequisite ledger price-capture landed. [`Q-COSTGEO-3`](docs/briefs/closures/Q-COSTGEO-3-closure-ambiguous-needs-depth.md) · B7 procedure in the private archive
- **Forward regime monitor / decompound limb-2 successor — Q-MONSURF-1 M-A (elective, not scheduled)** — ORPHANED same hole: CFD limb-2 cannot fire; venue-native design landed (not ratified); build-gate scope ruling owed (does "first live fill" bind a pure market-data observer?) before this is even buildable. Affected dependent: [`2026-07-15-sfrisk-1-t1-admitting-successor-risk-framework.md`](docs/adr/2026-07-15-sfrisk-1-t1-admitting-successor-risk-framework.md) §4 limb 2 (see its Addendum 2026-08-29). [`decompound ADR §Addendum 2026-08-03`](docs/adr/2026-06-07-decompound-remc-hold.md) · [`Pepperstone retirement`](docs/adr/2026-08-02-pepperstone-feed-retirement.md) (superseded by [`bar-data CFD+candidates retirement`](docs/adr/2026-08-03-bar-data-cfd-and-candidates-retirement.md)) · [`Q-MONSURF-1 closure`](docs/briefs/closures/Q-MONSURF-1-closure-resolved.md)
- **CFD data-estate class-wide delete** — trigger-dated; blocked on T1 (F3 FUTURES_LOCK) + substrate Phase-6 confirm. [`CFD estate ADR`](docs/adr/2026-07-11-ops-cfd-estate-retirement.md) (superseded by [`challenge-era substrate retirement`](docs/adr/2026-07-22-challenge-era-substrate-retirement.md)) · [gate audit](docs/notes/audits/2026-07-17_gate_cfd-estate-classwide-delete.md)
- **Mechanism-sourcing radar** — on-demand cadence; 08-08/11-08 = progress/idle checkpoints; idle guard 2026-11-08. [`harvest §2`](docs/methodology/strategy_harvest.md)
- **Deep-iteration lane — §4(c) supply-side audit DELIVERED 2026-08-23 (`AMBIGUOUS`); its named nearest supply lead, `MNQFLOW-1-DEPTH`, is now `HOLD` (operator, value-uncertain — not cost-blocked, not declined).** The audit ([note](docs/notes/audits/programme-audit/2026-08-23-deep-lane-supply-audit.md)) named `MNQFLOW-1-DEPTH` (order-flow) as the nearest reachable supply lead, "one sign-off away." Two independent, non-overlapping 30-day systematic samples of its own frozen 255-trigger population were each P0-priced and each blocked (original **$148.04**, redraw **$154.73**, both vs the **$125.00** ceiling) — reading as structural (~$150 true cost, not $125), not unlucky draws. Presented with three named forward paths (raise the ceiling to ≈$160–175; a smaller-N fresh pre-registration; decline), the **operator held**: *"I am not ruling it out but I do not know if it is worth the spend"* — recorded verbatim in [`PREREG_S2B.md`](lab/analysis/c1/mnq_orb_flow_depth_2026-08-18/PREREG_S2B.md)'s own Status block. No forced re-test date; naturally revisited at 2026-11-08 alongside the lane's own broader supply question, or sooner at the operator's initiative. $0 spent across both pricing attempts. The free alternate (a published MOC-imbalance cohort δ) and the blind channel (unsourced, 1/3) remain the estate's other two named supply routes — **neither requires any further action on the order-flow route to stay available.** Background: DL-2's construction retired for M6A (geometric-feasibility diagnostic, median R=1.0/0.687, 85–97% of fired trades never reach 1R); DL-1 is a separate candidate-level failure — no shared template defect. [`PREREG.md`§9.2](lab/analysis/c1/mnq_orb_flow_depth_2026-08-18/PREREG.md) · [`charter`](docs/adr/2026-08-16-deep-iteration-lane-charter.md) (superseded by [`GROW0 two-ledger K question`](docs/adr/2026-08-22-grow0-two-ledger-k-question.md))
### 2026-08-08 — DISCHARGED

> ✅ **The quarterly vehicle ran 2026-08-08.** Verdicts, the full rider partition
> (2 discharged / 37 owed / 3 moot / 5 unfalsifiable of 47), the unfalsifiable-check census, and
> every named follow-up now live in
> [`2026-08-08-quarterly-audit.md`](docs/notes/audits/programme-audit/2026-08-08-quarterly-audit.md).
> The former ~90-line rider blockquote is deleted per the retention test — it restated obligations
> the audit note now owns. **Operator rulings still open** are carried as queue rows, not here.

### 2026-08-24 (Monday)

- **Disaster-stop Phase 0a — attended real-account SIM.** Operator will attend and run the
  `stop_loss=` / `closeposition` observation on the real (non-paper) Tradeify eval account this
  session (committed 2026-08-23). Only a recorded PASS unlocks Phase 1 (`sl=` wiring into
  `ops/c1_rail/c1_rail_listener.py`); the prior unattended attempt came back BLOCKED. [`plan`](docs/superpowers/plans/2026-08-23-disaster-stop-phase-0-1-implementation.md) · [`BLOCKED note`](docs/notes/rail_build/2026-08-23-disaster-stop-phase-0.md)
- **M1 item 5 — attended test-strategy emit.** Operator will attend and discharge item 5 with a
  test strategy on the ruled host (`Strategy.on_bar` → daemon B1 POST → expected non-zero sizing
  at `dry_run=true`). Not a canned hand-POST. Not an arm. `operator_signoff` still owed after a
  recorded event id. [`M1 addendum`](docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md#addendum-2026-08-24--test-strategy-licensed-for-item-5-dated-08-24) (in-part superseded by [`S2 signal-host fork`](docs/adr/2026-08-07-loop-s2-signal-host-fork.md) and [`S5 bounded promotion lane`](docs/adr/2026-08-07-loop-s5-bounded-promotion-lane.md)) · [`S2b addendum`](docs/adr/2026-08-08-s2b-signal-daemon-build.md#addendum-2026-08-24--test-strategy-emit-go-for-m1-item-5)

### 2026-10-11 (approx.)

- **prop_envelope §4 overlay 90-day re-verify** — rows verified 2026-07-13; stale after ~2026-10-11. [`prop_envelope`](ops/prop_envelope_default.md) · [`ratification ADR`](docs/adr/2026-07-13-prop-envelope-v1-ratification.md)

### 2026-11-08

- **ADR ceremony-tiering §Falsifier review** — first quarterly programme audit after 2026-08-08; check light share ≥⅕ and dated omitted-apparatus incidents (incl. 2026-08-14 candidate: implied-SR light records). Count 1-vs-2 is operator/audit. [`ADR addendum`](docs/adr/2026-08-08-adr-ceremony-tiering.md)
- **GRAND-tier ADR §4 scheduled re-read** — H already satisfied 2026-08-09 (19 ratified differences; tier load-bearing, sunset did **not** arm). This slate is the first scheduled re-check, not a sunset. [`ADR addendum`](docs/adr/2026-08-09-grand-tier-quintessentials-binding.md) · [`closure`](docs/briefs/closures/GSUB-1-closure-resolved-loadbearing.md)
- **GSUB-1 PARK expiries (3)** — b1 Aegis→6J · b3 ORB-MNQ line · b6 Q-NAS-ECR-1. Each converts to SUBTRACT absent explicit operator renewal (ADR §2.3). b2 (Striker-MYM) and c1 (Q-XMEM-1) already resolved to `SUBTRACT` early via GSUB-2 (2026-08-19, ~80 days ahead of this expiry); b7 (ICT line) also already resolved to `SUBTRACT` — its own named re-entry step had already fired 2026-08-04, ~96 days ahead of this expiry, corrected this session (2026-08-20); **c3 Q-TOM-SPX-1** resolved to `SUBTRACT` / formal `DEAD` 2026-08-23 (P10 — reserved Pine unpaid, operator did not reserve it); **b5 Q-FUNDPOL-1** RENEWED once 2026-08-16 with a corrected wake condition, new expiry **2027-02-08** (see that date's row below) — five of the original set are no longer pending here, only b1/b3/b6 remain. [`docs/pursuits/`](docs/pursuits/)
- **Guardian-MGC (R7) transfer lane — SUBTRACT / DEAD(N-SURV) 2026-08-11** — exploratory N-SURV FAIL (full 42.2% / H1 72.4% / H2 16.5% bust vs ≤3.0%); margin-decisive; retroactive cell PREREG + typed closure filed. Re-entry = new mechanism evidence (not param retune). [`b8`](docs/pursuits/b8-guardian-mgc-transfer-lane.md) · [`closure`](docs/briefs/closures/2026-08-11-guardian-mgc-transfer-cell-dead-nsurv.md)
- **Prop-portfolio §4 primary falsifier (HARD)** — ≥1 candidate clears bust ceiling on ≥2 of 4 FRIENDLY firms; else demote program to research-only. Status undischarged (2026-07-22 withdrawal). [`four-firms ADR §4`](docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md) · [`withdrawal ADR`](docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md)
- **Mechanism-boundaries ADR §4** — clauses 2-A / 2-C first check (2-B discharged early 2026-08-24 by [`sourcing-phase channel retirement ADR`](docs/adr/2026-08-24-sourcing-phase-channel-retirement.md) — its own falsifier substantively met, operator elected to act ahead of this date). [`ADR`](docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md)
- **Sourcing-phase channel retirement ADR §4 limb 2 (starvation check)** — first of two checks: surviving sourcing channels (harvest, deep-iteration lane) must not be themselves found zero-yield/degenerating with no successor-ADR redesign authored in the interim, or this and the 2027-02-08 check must rule on whether channel starvation is now the binding constraint. [`ADR §4`](docs/adr/2026-08-24-sourcing-phase-channel-retirement.md)
- **Harvest-intake §4 doctrine falsifier + idle guard** — limb 1 still 0-of-2; limb 2 `Accepted` (R10 GO); pin marked `no`; post-mark count 0/2 (not fired). Idle = zero screen-PASS seeds beyond D5. [`harvest ADR §4`](docs/adr/2026-07-15-external-mechanism-harvest-intake.md) (superseded by [`S5 bounded promotion lane`](docs/adr/2026-08-07-loop-s5-bounded-promotion-lane.md))
- **Regime-monitor successor §6 gate** — if no live fill by 11-08, gap is ≥3 months; re-raise as standing-unfalsifiable in that programme audit. [`decompound ADR`](docs/adr/2026-06-07-decompound-remc-hold.md)
- **Blind-channel §4 reading** — sourced-vs-empty (`AMBIGUOUS-HOLD` if still unsourced); disclose pre-G0 count and whether N fired; analogue-modality ruling re-test (inert if no analogue manifest). Owner: [channel ADR](docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md) · [analogue ruling](docs/adr/2026-08-15-analogue-modality-route-ruling.md)
- **Regime-candidate flag lane §4 two-strikes check** — any flag-lane follow-up closures since ratification + their confirm verdicts. [`ADR`](docs/adr/2026-07-26-regime-candidate-flag-lane.md)
- **CLAUDE.md Live-execution posture size-hook exception** — `2026-07-16-root-doc-charter-dedup.md`'s own §10 hook expects that section at ≤25 lines; it's 54 today (Safety invariants block, Account-state paragraph, Eval-bust-figures warning all accreted post-2026-08-03, each individually safety-relevant). Operator call owed: accept as a bounded safety-content exception (revise the hook's ceiling) or trim back to pointer form with detail pushed to the owning ADRs/RUNBOOK. [`ADR`](docs/adr/2026-07-16-root-doc-charter-dedup.md) · [`adr-decay-audit`](docs/notes/audits/adr-corpus/2026-08-29-adr-decay-audit.md) §7

### 2027-02-08

- **GSUB-1 PARK expiry — b5 Q-FUNDPOL-1 (renewed 2026-08-16)** — converts to SUBTRACT absent explicit operator renewal (ADR §2.3), unless renewed again. Corrected wake condition (replaces the stale F3-successor clause, which S1's no-migration ruling made unreachable): re-enter when Q-POLFRONT-1 reads positive on funded-relevant cells OR a candidate reaches funded-phase modeling. **Note 2026-08-29:** the first disjunct has no literal referent — Q-POLFRONT-1's frozen grid is confirmed eval-phase-only synthetic geometry with zero funded-phase dimension (its sole "funded" text is its own §7 naming that scope as an unopened fork); the wake condition now reads as governed solely by the second disjunct ("a candidate reaches funded-phase modeling"), not yet fired. PARK/expiry unchanged. [`b5 pursuit record`](docs/pursuits/b5-q-fundpol-1.md)
- **Mechanism-boundaries ADR §4** — clause 2-B's own literal "second quarterly audit" trigger date (2-B itself already discharged early 2026-08-24; this date is now owned by the retirement ADR's limb 3 below, not a live re-check of 2-B). [`ADR`](docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md) (2-B superseded by [`sourcing-phase channel retirement`](docs/adr/2026-08-24-sourcing-phase-channel-retirement.md))
- **Sourcing-phase channel retirement ADR §4 limb 2 (starvation check)** — second of two checks (see 2026-11-08 row). [`ADR §4`](docs/adr/2026-08-24-sourcing-phase-channel-retirement.md)
- **Sourcing-phase channel retirement ADR §4 limb 3 (early-closure legitimacy)** — independent re-examination of whether the 0-for-4/0-for-4 record the 2026-08-24 ADR relied on to close ahead of this schedule was in fact complete at authoring time (distinct from limb 1's narrower "an admitted seed was missed" test — this asks whether the *process* of closing early on judgment, not new evidence, was sound). [`ADR §4`](docs/adr/2026-08-24-sourcing-phase-channel-retirement.md)
