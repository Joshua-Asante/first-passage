# STATE — First Passage

**Last curated:** 2026-09-12

Current priorities, dormant cross-session work, and outstanding obligations.
Read the queue first, then the linked executable plan; campaign records own
evidence and decisions. Routine updates need no separate ADR; follow the
[ADR retention policy](docs/adr/2026-08-08-adr-ceremony-tiering.md). [SESSIONS](docs/SESSIONS.md) is history, `git status`
owns uncommitted work, and [Rule 7](docs/operational_rules.md) assigns fact ownership.

**Anti-accretion:** decision index = consequence + owner; forward row = action,
date/wake condition + owner. Delete closed rows after confirming their record
exists with the owner. Keep results, account figures, parameters, and narrative
with their owners. `state-currency` checks Last curated and recurring deadlines.
Missing evidence is not completion; do not roll an obligation away without its
required record. The [root-doc charter](docs/adr/2026-07-16-root-doc-charter-dedup.md)
owns this division of responsibilities.

## OPERATOR QUEUE — strictly ordered, ≤5 live items

**Agent-hours are cheap and budgeted (K-ledger, cost dry-runs, $700 spend ceiling);
operator-hours are the binding resource and were the only unrationed one.**
Serve the numbered priorities in dependency order; a priority number is not an
assertion that independent work must wait. New decision packets, advisor triage,
and sizing questions queue behind these items unless the operator directs otherwise.

This is the concurrency-denominated [Survive bound](docs/adr/2026-07-16-root-doc-charter-dedup.md#queue-attention-review),
not an hours budget. Completed items leave; do not automatically open replacements.
Off-queue work stays with its owner until promoted or explicitly directed.
Queue position does not grant phase GO or authorize a new generation channel.

**Source disposition (2026-09-11):** Databento retired/unsubscribed by operator report ([owner record](docs/adr/2026-07-10-databento-research-stack.md#addendum-2026-09-10---operator-retirement-of-databento)); no live feed approved. The Stage 1 input is an **operator-attended controlled input**, ratified 2026-09-11 as the explicit acceptance amendment ([S2b build ADR Addendum 2026-09-11](docs/adr/2026-08-08-s2b-signal-daemon-build.md#addendum-2026-09-11--stage-1-input-source-options-and-ratified-selection-option-d) option D · [M1 ADR Addendum 2026-09-11](docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md#addendum-2026-09-11--item-5-input-for-stage-1-operator-attended-controlled-input-express)). The attended ceremony (A7) and acceptance closeout (A8) remain owed; completed implementation, validation and deployment evidence is linked from queue item 1; live-feed readiness remains separate and owed; no arm. **Production feed deferred 2026-09-11 (Track B open item O-4):** no provider is selected, funded or connected; option A′ is shortlisted only. Provider-neutral preparation may proceed, but provider-specific implementation and spend wait until the fixed book clears every source-independent gate and the operator returns for the funding decision.

| # | Item | Owner artifact | Blocks |
|---|---|---|---|
| 1 | **B7-REFIRE Stage 1 + M1** — licensed test strategy; offline `m1_stage1_test` implementation on `codex/m1-stage1-test` ([contract](docs/notes/rail_build/M1_STAGE1_TEST_CONTRACT.md)); item 5 dated 2026-08-24 remains owed; Stage 1 input ruled 2026-09-11 (option D, operator-attended controlled input); A1b implemented and Linux-validated (#349, 2026-09-12); readiness record §A3, §A4-L, §A5, §A4-D, §A6 landed (#348, #350, #352, #354, #355): listener and daemon deployed disarmed/inert 2026-09-12 (evidence in the readiness record); A7 (the one attended ceremony) prepared for Sunday 2026-09-13 (§A7-P), then A8. Former queue item 2; unchanged scope and no arm. | [Track A plan](docs/superpowers/plans/2026-09-10-track-a-m1-stage1-completion.md) · [M1 addendum](docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md#addendum-2026-08-24--test-strategy-licensed-for-item-5-dated-08-24) · [GO addendum](docs/adr/2026-07-17-c1-rail-build-account-registration-go.md#addendum-2026-08-24--test-strategy-is-a-qualifying-strategy) | Live-signal / arming path |
| 2 | **Track B — qualify the accepted Tradeify book** — K=1 confirmation of the operator-accepted four-strategy book under the fixed 1% trigger / 40% scale / full ORB base / ORB adds-off policy; HOLD released 2026-09-11 for the umbrella's packets only (TB-G0, D-B1..D-B15 recorded); wave 1a dispatchable, later waves per the umbrella's wave gates. Consumes Track A's M1 `RESOLVED`; the production feed for the four adapters is a separate open operator decision (umbrella O-4). No deployment or arm authority. | [Track B umbrella](docs/briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md) · [campaign record §55](docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md#55--track-b-release--d-b1d-b15-recorded-2026-09-11) · [acceptance](docs/notes/2026-09-10-tradeify-protection-selection.md) | Deployment GO / arm |

## Executed operator decisions — decision index

Newest 15 consequences; decision rationale remains with the owner. Older index:
[archive](docs/ltm/notes/archive/state/STATE-decision-index-pre-2026-08-23.md).
Retracted verdicts leave this index; their correction stands with its owner.

- **2026-09-11** — Production market-data feed decision deferred: provider unselected; option A′ shortlisted only; no account, spend, provider-specific implementation, feed connection or arm. [S2b build ADR §2 row + Addendum](docs/adr/2026-08-08-s2b-signal-daemon-build.md#addendum-2026-09-11--stage-1-input-source-options-and-ratified-selection-option-d) · [Track A plan §3.2](docs/superpowers/plans/2026-09-10-track-a-m1-stage1-completion.md#32-a9--production-feed-verification-record-and-funding-checkpoint-added-2026-09-11)
- **2026-09-11** — Stage 1 input source ruled: operator-attended controlled input (option D); no live feed; A1b implementation owed; no arm. [Addendum](docs/adr/2026-08-08-s2b-signal-daemon-build.md#addendum-2026-09-11--stage-1-input-source-options-and-ratified-selection-option-d) · [M1 addendum](docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md#addendum-2026-09-11--item-5-input-for-stage-1-operator-attended-controlled-input-express)
- **2026-09-10** — Operator accepted the selected Tradeify configuration as satisfying queue item 1; configuration-selection work closed and removed from the live queue. Deployment remains separate. [Acceptance](docs/notes/2026-09-10-tradeify-protection-selection.md#operator-acceptance-and-state-item-1-closure)
- **2026-09-06** — Root docs narrowed to current routing; STATE owns priorities, campaign plans executable steps, SESSIONS history. [Charter](docs/adr/2026-07-16-root-doc-charter-dedup.md#decision)
- **2026-09-03** — Off-queue VOLREGIME translation closed at T0, PRE-CONTRACT DROP; no contract. [Ruling](docs/adr/2026-09-02-portable-edge-cultivation-campaign-objective.md#addendum-2026-09-03b--t0-pre-contract-drop)
- **2026-09-03** — Select configuration campaign promoted to queue #1; cultivation remains off-queue. [Campaign record](docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md)
- **2026-09-02** — Portable-edge objective and bounded cultivation campaign approved; no candidate/capital authority. [ADR](docs/adr/2026-09-02-portable-edge-cultivation-campaign-objective.md)
- **2026-09-01** — MOC-wake strategy and source-liveness pursuits closed; no candidate opened. [Closure](docs/notes/2026-09-01-next-vet-intake-decision.md)
- **2026-09-01** — F1 reversed: a Tradeify discharge counts toward the four-firm program again. [Addendum](docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md#addendum-2026-09-01--f1-reversed-a-tradeify-resting-discharge-now-counts-toward-4)
- **2026-08-31** — ADR-corpus audit fixes and simplifications applied. [Audit](docs/notes/audits/programme-audit/2026-08-31-adr-corpus-audit.md)
- **2026-08-31** — Q-RANGECOND-1 retracted to FALSIFIED; separate MNQ/MYM window defects corrected. [Closure](docs/briefs/closures/Q-RANGECOND-1-closure-falsified.md) · [MYM audit](docs/notes/audits/2026-08-31-mym-overnight-window-scope-gap-defect.md)
- **2026-08-30** — Q-RANGEXFER-1 closed MIXED with per-hypothesis AMBIGUOUS-DESIGN routing. [Closure](docs/briefs/closures/Q-RANGEXFER-1-closure-ambiguous-design.md)
- **2026-08-29** — SSOT Phase 3 cost-model partition authorized. [Addendum](docs/adr/2026-08-27-ssot-data-lineage-remediation-program.md#addendum-2026-08-29--phase-3-authorized-cost-model-closed-world-partition)
- **2026-08-29** — SSOT Phase 2 running-count consistency authorized. [Addendum](docs/adr/2026-08-27-ssot-data-lineage-remediation-program.md#addendum-2026-08-29--phase-2-authorized-a8-intra-adr-running-count-consistency)
- **2026-08-27** — SSOT/data-lineage remediation Phase 1 authorized. [ADR](docs/adr/2026-08-27-ssot-data-lineage-remediation-program.md)

## Dormant cross-session threads

PARK threads b1, b3 and b6 remain with [their pursuit records](docs/pursuits/);
expiry below. Off-queue campaign work remains with its current owner, not a
second queue here. Registry backfill debt is enumerated by
`python scripts/check_closure_disposition.py --list-debt`.

## Scheduled forward triggers

Owners retain canonical criteria; rows below are pointers. Delete discharged
rows rather than retaining completion narratives. A gated row does not grant GO.

### Weekly — recurring (rolling; next deadline **2026-09-18**, bucket 09-14→09-18)

- **Operator-placed account-preservation trade:** at least one per Mon–Fri week.
  No agent places it; the rail stays disarmed. A missed venue week risks account
  deletion; venue-session boundaries apply. [S1](docs/adr/2026-08-07-loop-s1-environment-ratification.md)
  · [idle-clock audit](docs/notes/audits/programme-audit/2026-08-05-post-descope-claim-alignment-audit.md).
- **Coverage evidence:** week 08-31→09-04 was operator-attested on 09-04 and
  restated on 09-05; the exact trade day is unresolved between 09-02/09-03.
  The private compliance ledger row remains owed; its session hook still reads
  NOT RECORDED until written. [Campaign record §15](docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md#15-d20--the-acceleration-ruling-2026-09-04-deploy-at-the-phase-3-commit)
  retains the attestation history. Week 09-07→09-11: placement **not verified from
  this clone** as of 2026-09-12 (the session hook reads UNAVAILABLE — the coverage
  record is redacted here; this is not a coverage verdict) — the operator's attestation
  for that week is owed. Week 09-14→09-18 is open. Roll the deadline each Monday;
  `daily-repo-truth-sync` reads this board's dated obligations.

### Monthly — recurring (rolling; next deadline **2026-09-21**)

- **Subscription reconfirm:** recheck [ledger](docs/pursuits/SUBSCRIPTION_LEDGER.md)
  rows d11–d18, record confirmation even when unchanged, and resolve Fly.io/Tradeify
  unknowns if evidence becomes available. Roll monthly on the 21st; the operator
  confirms the figures. [Owner ADR](docs/adr/2026-08-21-cfo-subscription-ledger-consolidation.md).

### No fixed date / gated

- **M-B idle-clock monitor:** built/registration-ready, but gated on F3 successor
  registration; S1 currently elects no migration. Re-freeze venue semantics and
  wire only on that trigger. [Q-MONSURF-1](docs/briefs/closures/Q-MONSURF-1-closure-resolved.md).
- **M-C per-fill add-slippage capture:** waits for the first strategy-signal add
  fill; prerequisite ledger capture landed. [Q-COSTGEO-3](docs/briefs/closures/Q-COSTGEO-3-closure-ambiguous-needs-depth.md)
  · [monitor triage](docs/briefs/closures/Q-MONSURF-1-closure-resolved.md).
- **M-C ECR live-edge capture / b6:** re-entry is a NAS100/MNQ-shaped leg's first
  live fill on the incumbent eval or a future F3 successor; it remains PARK until
  that trigger. [Pursuit record](docs/pursuits/b6-q-nas-ecr-1.md); expiry below.
- **M-A regime observer / decompound limb-2 successor:** elective; operator ruling
  still owed on whether its build gate requires a live fill. [Monitor triage](docs/briefs/closures/Q-MONSURF-1-closure-resolved.md)
  · [dependent risk-framework obligation](docs/adr/2026-07-15-sfrisk-1-t1-admitting-successor-risk-framework.md).
- **Lifecycle Call-1 / T4 Task 3:** rolling-PF sigma-source and state writer remain
  fill/data-gated; synthetic tooling completion is not live evidence.
  [Statistics ADR §7](docs/adr/2026-07-11-tradable-anomalies-statistics-adoption.md)
  · [T4 record](docs/notes/research/2026-08-23-call1-oc-synthetic.md).
- **ORB decay re-scope:** remains open without deployed-book data.
  [Originating obligation](docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md#6--consequences)
  · [current incumbent environment](docs/adr/2026-08-07-loop-s1-environment-ratification.md)
  · [ORB pursuit](docs/pursuits/b3-orb-mnq-payability-line.md).
- **Sentinel Tier-2/3 promotion, limb B1:** before the next quarterly slate;
  promotion, not a new build. [Design](docs/spec/2026-06-23-inqhiori-sentinel-design.md)
  · [Hermes closure](docs/briefs/closures/2026-07-27-hermes-agent-adoption-closure-resolved.md).
- **PREREG-C1-DEDUPE-1:** waits for M1 RESOLVED plus separate operator GO.
  [Pre-registration](docs/spec/PREREG-C1-DEDUPE-1-intent-key-functional-property.md)
  · [implementation plan](docs/spec/PREREG-C1-DEDUPE-1-implementation-plan.md).
- **CFD data-estate class-wide deletion:** awaits T1 / F3 FUTURES_LOCK and
  substrate Phase-6 confirmation. [Estate ADR](docs/adr/2026-07-11-ops-cfd-estate-retirement.md)
  · [superseding substrate ADR](docs/adr/2026-07-22-challenge-era-substrate-retirement.md)
  · [gate audit](docs/notes/audits/2026-07-17_gate_cfd-estate-classwide-delete.md).
- **Mechanism-sourcing radar:** on demand; progress/idle checkpoint 2026-11-08.
  [Harvest method](docs/methodology/strategy_harvest.md).
- **Reversed-evidence propagation sweep:** pursuit fixes from the closed, unmerged
  pass remain owed; most skills and strategy-card mirrors remain unswept.
  [Unlanded findings](docs/notes/audits/2026-08-31-pursuits-personas-reversed-evidence-audit.md)
  · [first audit](docs/notes/audits/2026-08-31-reversed-evidence-docs-audit.md)
  · [instrument audit](docs/notes/audits/2026-08-31-ops-instruments-reversed-evidence-audit.md).
- **MNQFLOW-1-DEPTH:** operator HOLD on value of spend, not a cost-only block or
  decline. Revisit at operator initiative or 2026-11-08; alternate supply routes
  do not depend on resolving it. [S2B status](lab/analysis/c1/mnq_orb_flow_depth_2026-08-18/PREREG_S2B.md)
  · [deep-lane charter](docs/adr/2026-08-16-deep-iteration-lane-charter.md)
  · [superseding K ruling](docs/adr/2026-08-22-grow0-two-ledger-k-question.md).

### 2026-10-11 (approx.)

- **Prop-envelope overlay:** reverify the 90-day venue facts.
  [Envelope §4](ops/prop_envelope_default.md) · [ratification](docs/adr/2026-07-13-prop-envelope-v1-ratification.md).

### 2026-11-08

- **Queue attention/order review:** first check of the ≤5 concurrency cap and
  repeated out-of-order serving; retain dependency order/operator direction and
  assess the two-consecutive-quarter cap condition. [Charter](docs/adr/2026-07-16-root-doc-charter-dedup.md#queue-attention-review).
- **GRAND-tier ADR §4:** scheduled re-read; initial binding was satisfied, not sunset.
  [Owner](docs/adr/2026-08-09-grand-tier-quintessentials-binding.md).
- **GSUB-1 PARK expiries:** b1 Aegis→6J, b3 ORB-MNQ, b6 Q-NAS-ECR convert to SUBTRACT
  absent explicit renewal. [Pursuit records](docs/pursuits/). b5's renewed date is below.
- **Prop-portfolio §4 primary falsifier:** still undischarged; absent the required
  qualifying clearance, demote to research-only. [Four-firm owner](docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md)
  · [withdrawal](docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md).
- **Mechanism boundaries:** check clauses 2-A/2-C; 2-B discharged under the
  [channel-retirement decision](docs/adr/2026-08-24-sourcing-phase-channel-retirement.md).
  [Owner](docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md).
- **Sourcing-channel retirement §4 limb 2:** first starvation check; second is
  2027-02-08. [Owner](docs/adr/2026-08-24-sourcing-phase-channel-retirement.md).
- **Harvest intake §4:** doctrine falsifier and idle guard. Read owner counts and
  evidence; do not infer discharge from a root summary.
  [Owner](docs/adr/2026-07-15-external-mechanism-harvest-intake.md)
  · [partial supersession](docs/adr/2026-08-07-loop-s5-bounded-promotion-lane.md).
- **Regime-monitor successor:** if no live fill, re-raise the standing-unfalsifiable
  gap at the audit. [Decompound owner](docs/adr/2026-06-07-decompound-remc-hold.md).
- **Blind channel:** check sourced-vs-empty status, pre-G0 count, N firing and any
  analogue-manifest re-test. [Channel](docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md)
  · [analogue ruling](docs/adr/2026-08-15-analogue-modality-route-ruling.md).
- **Regime-candidate flag lane:** two-strikes check against new confirm closures.
  [Owner](docs/adr/2026-07-26-regime-candidate-flag-lane.md).
- **Candidate contract and channel review:** initial consolidated review of freezes,
  field sufficiency, inclusive probe spend, fixed confirm family and fresh-attempt authority
  under [candidate review](docs/adr/2026-08-30-candidate-contract.md#first-review-and-unresolved-obligations).
  Five artifact adoptions and five liveness reconciliations remain owed at their channel
  owners; [candidate owner](docs/adr/2026-08-30-candidate-contract.md#current-owner)
  and [channel liveness](docs/methodology/strategy_harvest.md#channel-liveness-contract) route them.
  Review fired ceilings for reachability, bindingness and operator consequence; no firing
  leaves the first post-firing check owed. Missing examples are inconclusive, not PASS.
- **Evaluation and rejection review:** initial consolidated ordering, role-scope,
  reachability, verdict and N_expr review under
  [evaluation review](docs/adr/2026-08-30-evaluation-order.md#first-review-and-unresolved-obligations).
  Full contract/K/M/selection/role/reachability enforcement and the rejection parser/ladder
  remain incomplete; [evaluation owner](docs/adr/2026-08-30-evaluation-order.md#current-owner)
  and [rejection patterns](docs/adr/2026-06-14-rejected-candidate-patterns.md#expression-ladder-and-register-routing)
  retain the limits under [D3 scope routing](docs/adr/2026-08-09-rejection-register-topology-and-bar-wiring.md#2--decision).
  Cost-authority/scope changes trigger an immediate review. The six
  documents' redundant recurring maintenance reviews are retired; useful unresolved work remains.

### 2027-02-08

- **b5 Q-FUNDPOL-1 PARK expiry:** renewed once; converts to SUBTRACT absent renewal.
  Wake when a candidate reaches funded-phase modeling; the alternative Q-POLFRONT-1
  funded-cell trigger has no referent in its eval-only grid.
  [Pursuit record](docs/pursuits/b5-q-fundpol-1.md).
- **Sourcing-channel retirement §4 limb 2:** second starvation check.
  [Owner](docs/adr/2026-08-24-sourcing-phase-channel-retirement.md).
- **Sourcing-channel retirement §4 limb 3:** independently re-examine whether the
  evidence supporting early closure was complete at authoring.
  [Owner](docs/adr/2026-08-24-sourcing-phase-channel-retirement.md).
