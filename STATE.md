# STATE — First Passage

**Last curated:** 2026-09-25

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

**Source disposition (2026-09-11):** Databento retired/unsubscribed by operator report ([owner record](docs/adr/2026-07-10-databento-research-stack.md#addendum-2026-09-10---operator-retirement-of-databento)); no live feed approved. The Stage 1 input is an **operator-attended controlled input**, ratified 2026-09-11 as the explicit acceptance amendment ([S2b build ADR Addendum 2026-09-11](docs/adr/2026-08-08-s2b-signal-daemon-build.md#addendum-2026-09-11--stage-1-input-source-options-and-ratified-selection-option-d) option D · [M1 ADR Addendum 2026-09-11](docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md#addendum-2026-09-11--item-5-input-for-stage-1-operator-attended-controlled-input-express)). The attended ceremony (A7) and signed M1 acceptance/re-bake (A8) are complete ([deployment record](docs/notes/rail_build/M1_STAGE1_DEPLOYMENT_READINESS.md#a8--signed-acceptance-deployed-re-bake-verified-2026-09-14)); live-feed readiness remains separate and owed; no arm. **Production feed deferred 2026-09-11 (Track B open item O-4):** no provider is selected, funded or connected; option A′ is shortlisted only. Provider-neutral preparation may proceed, but provider-specific implementation and spend wait until the fixed book clears every source-independent gate and the operator returns for the funding decision.

| # | Item | Owner artifact | Blocks |
|---|---|---|---|
| 1 | **Track B — qualify the accepted Tradeify book** (the operator's **Tradeify portfolio**: K=1 confirmation of the accepted four-strategy book under the fixed 1% trigger / 40% scale / full ORB base / ORB adds-off policy; M1 `RESOLVED` consumed). **Phase (2026-09-26):** Protected Full E1 engineering — S1 accepted; S2 **ACCEPTED as the enforced work boundary** (coordinator entry 2026-09-21; [#436](https://github.com/Joshua-Asante/first-passage/pull/436) merged, merge-gate run 35557000399 fifteen green) — the accepted boundary is the accounting, enforcement, interruption-recovery and cancellation behavior of admission and supervised test work on a real Linux host, and authorizes no statistical dispatch, no installed-release activation on a non-disposable host and no S3 work by itself; S3 **ACCEPTED** 2026-09-22 (#455); S4 **ACCEPTED** 2026-09-25 at C2 close (#501 merged); S5 freeze **HELD** by the operator pending the [contract-delta](docs/notes/audits/2026-09-25-qualification-assurance-contract-delta.md) decisions (§5.1 boundary list, N1, N2); T05 accepted as a build only; S8 not started. Per-packet outcome, blocker, owner and next decision: [checklist current state](docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#current-state--september-26-2026-refreshed-from-the-acceptance-ledger). Production feed O-4 deferred (2026-09-11); no deployment or arm authority. **Routing (Rule 7, ruled 2026-09-20):** [umbrella](docs/briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md) = campaign scope, authority and governing gates · [deployment checklist](docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md) = current cross-workstream sequence and dependencies (adopted via #440) · [execution-slices plan](docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md) = qualification engineering requirements and acceptance ledger · bounded handoffs = individual assignments and returns. Detailed repair lists stay in the ledger and handoffs, not here. Dispatch-1 heads and the TB-I/TB-T packets remain in the [closeout](docs/briefs/handoffs/2026-09-13-tradeify-contract-closeout.md). | [Track B umbrella](docs/briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md) · [deployment checklist](docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md) · [execution-slices ledger](docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md#progress-ledger-and-present-disposition) · [campaign record §55](docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md#55--track-b-release--d-b1d-b15-recorded-2026-09-11) · [acceptance](docs/notes/2026-09-10-tradeify-protection-selection.md) | Deployment GO / arm |

**Campaign owner (2026-09-20):** the current coordinating task — the Claude coordinator session for Protected Full E1 — under [campaign record §58](docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md#58--campaign-ownership-the-current-coordinating-task-2026-09-20), which supersedes §57's Astra assignment. **Handoff obligation:** ownership passes only by a recorded handoff entry in the execution-slices ledger naming the successor; a session ending without one leaves the role with the operator. The S2 delegation (GLM executor under the [acceptance continuation](https://github.com/Joshua-Asante/first-passage/blob/12d6a6f/docs/briefs/handoffs/2026-09-20-glm-s2-acceptance-continuation.md) and [T01](docs/briefs/handoffs/2026-09-20-glm-t01-s2-closeout-g3-worker-launch.md)) is discharged by the 2026-09-21 acceptance and the merge of #436; no successor delegation is open. Joshua retains ratifications, merges and operational GOs. No dedupe, incident-exception, ORB, feed-funding, production-qualification, deployment or arming GO is granted by the 2026-09-20 refresh or by the 2026-09-21 S2 acceptance.

## Executed operator decisions — decision index

Newest 15 consequences; decision rationale remains with the owner. Older index:
[archive](docs/ltm/notes/archive/state/STATE-decision-index-pre-2026-08-23.md).
Retracted verdicts leave this index; their correction stands with its owner.

- **2026-09-25** — Agents may **read** the accepted book's four Pine sources and their accepted runtime ports, in place in the primary checkout (pinned in `core/strategies/BOOK_SOURCES.sha256`); §59's no-read clause is lifted for those files only. Never copy them into a worktree, commit or quote them, edit them, or send them to GLM/Z.ai or any external service. No drill, requalification or GO. [Campaign record §60](docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md#60--agent-read-access-to-the-accepted-books-pine-and-runtime-ports-2026-09-25)
- **2026-09-25** — Three rulings on the route: Vanguard/Aegis attested to fit the narrowed shape; the T08 vendor question sent (no reply yet); **route-native editions adopted for ORB MNQ (fixed-stop bracket, no trailing) and Striker MYM (entry carrying its stop; one-contract requests)** as a pre-registered K=1 requalification — D-B4 (a) amended to that extent only. Pre-registration owed from the port owner; requalification through the owed production E1. R3 stays NONE, D-broker void, live release held; no drill, access, spend or GO. [Campaign record §59](docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md#59--route-native-expressions-for-the-accepted-book-three-operator-rulings-2026-09-25). Same day: the edition pre-registration was drafted (not frozen). The T08 drills and T07 account reads were authorized; the operator performs them ([session plan](docs/notes/2026-09-25-t08-drills-t07-reads-operator-session.md)). The bounded-exposure addendum was revised as §A8 (still Proposed).
- **2026-09-24** — Build GO for the ratified path-position bracket convention, so T00 can finish P7. Production-feed work stays blocked until T00 returns other than INSUFFICIENT and T10 has assembled the F1 packet. Built at the engine layer only; no G1 artifact role, production source, stage-runner, F1, T00 step 2 or spend is granted. [Build GO and implementation](docs/briefs/phase3-preparation/2026-09-15/schedule-execution-evidence.md#addendum-2026-09-23--path-position-bracket-convention-ratified-2026-09-23)
- **2026-09-24** — T08 R3 = NONE (no documented unknown-request fence; D-broker void; T09 unspecifiable). Operator adopted the T08 §7.7 recommendation: **hold live release**; one narrow CrossTrade question authorized (operator-sent, written answer retained as evidence); the ADR-level bounded-exposure amendment scoped in parallel. No contract change, broker access, route change, drill or spend. [T08 §7.8](docs/briefs/handoffs/2026-09-21-tradeify-t08-broker-protection-feasibility.md#78-operator-ruling-on-the-return-2026-09-24) · [scope](docs/superpowers/specs/2026-09-24-bounded-exposure-unknown-request-amendment-scope.md)
- **2026-09-23** — T00 step-1 return accepted (INSUFFICIENT). Condition 4 ruled **no**: a T00 screen is not four-firm §4 falsifier evidence, so the 2026-11-08 falsifier needs its own dated re-MC regardless of T00. The path-position bracket timing convention for the qualification replay was ratified the same day ([schedule-evidence addendum](docs/briefs/phase3-preparation/2026-09-15/schedule-execution-evidence.md#addendum-2026-09-23--path-position-bracket-convention-ratified-2026-09-23)); it replaces one P7 blocker only and authorizes no build. No step 2, screen, MC, provider or spend is granted. [T00 rulings](docs/briefs/handoffs/2026-09-22-tradeify-t00-step1-producer-inventory.md#78-operator-rulings-on-the-return-2026-09-23)
- **2026-09-22** — Deployment-checklist amendment (2026-09-21) §4 ratified: all five decisions adopted as recommended — T00 step 1 authorized (not dispatched); D-feed as a gate on the T00 verdict and the T10 F1 packet; D-broker conditional on T08 R3; D-codex as the review hybrid; D-sequence with a versioned T02 freeze. No provider, access, spend, deployment or arming granted. [Addendum](docs/superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#addendum-2026-09-22--4-dispositions-ratified-2026-09-22--all-five-adopted-as-recommended-and-the-5-correction-applied)
- **2026-09-21** — S2 accepted as the enforced work boundary (admission and supervised test work on a real Linux host); five enforcement gaps and two external-review P2 findings closed, #436 merged. No statistical dispatch, installed-release activation or S3 work is authorized by it. [Ledger](docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md#coordinator-acceptance--s2-budgeted-admission-and-real-linux-work-supervision-2026-09-21)
- **2026-09-19** — S2-R2b accepted as the funded-scheduler integration only (closed private route, materialized-intent launch, release v4, owned timer; restart ownership ruled auto-recover). S2 overall remains INCOMPLETE / NOT ACCEPTED; R3/R4 untouched. [Ledger](docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md#coordinator-acceptance--s2-r2b-funded-scheduler-integration-2026-09-19)
- **2026-09-19** — B0: the protected qualification service is retained; the operator-launched batch is not adopted. R2b dispatched under that narrowing. [B0 decision](docs/superpowers/plans/2026-09-19-attended-batch-qualification.md#b0-decision--2026-09-19)
- **2026-09-15** — Cursor retired as a worker surface; workers are Claude Code and Codex. [ADR revision](docs/adr/2026-07-14-cc-cursor-surface-allocation.md) · [first-passage#405](https://github.com/Joshua-Asante/first-passage/pull/405)
- **2026-09-14** — B7-REFIRE Stage 1 + M1 completed: signed acceptance and matching pin record verified in disarmed listener v11; Track A leaves the queue. Live-feed/strategy readiness and arming remain separate. [A8 record](docs/notes/rail_build/M1_STAGE1_DEPLOYMENT_READINESS.md#a8--signed-acceptance-deployed-re-bake-verified-2026-09-14)
- **2026-09-11** — Production market-data feed decision deferred: provider unselected; option A′ shortlisted only; no account, spend, provider-specific implementation, feed connection or arm. [S2b build ADR §2 row + Addendum](docs/adr/2026-08-08-s2b-signal-daemon-build.md#addendum-2026-09-11--stage-1-input-source-options-and-ratified-selection-option-d) · [Track A plan §3.2](docs/superpowers/plans/2026-09-10-track-a-m1-stage1-completion.md#32-a9--production-feed-verification-record-and-funding-checkpoint-added-2026-09-11)
- **2026-09-11** — Stage 1 input source ruled: operator-attended controlled input (option D); no live feed; A1b implementation owed; no arm. [Addendum](docs/adr/2026-08-08-s2b-signal-daemon-build.md#addendum-2026-09-11--stage-1-input-source-options-and-ratified-selection-option-d) · [M1 addendum](docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md#addendum-2026-09-11--item-5-input-for-stage-1-operator-attended-controlled-input-express)
- **2026-09-10** — Operator accepted the selected Tradeify configuration as satisfying queue item 1; configuration-selection work closed and removed from the live queue. Deployment remains separate. [Acceptance](docs/notes/2026-09-10-tradeify-protection-selection.md#operator-acceptance-and-state-item-1-closure)
- **2026-09-06** — Root docs narrowed to current routing; STATE owns priorities, campaign plans executable steps, SESSIONS history. [Charter](docs/adr/2026-07-16-root-doc-charter-dedup.md#decision)

## Dormant cross-session threads

PARK threads b1, b3 and b6 remain with [their pursuit records](docs/pursuits/);
expiry below. Off-queue campaign work remains with its current owner, not a
second queue here. Registry backfill debt is enumerated by
`python scripts/check_closure_disposition.py --list-debt`.

## Scheduled forward triggers

Owners retain canonical criteria; rows below are pointers. Delete discharged
rows rather than retaining completion narratives. A gated row does not grant GO.

### Weekly — recurring (rolling; next deadline **2026-09-25**, bucket 09-21→09-25)

- **Operator-placed account-preservation trade:** at least one per Mon–Fri week.
  No agent places it; the rail stays disarmed. A missed venue week risks account
  deletion; venue-session boundaries apply. [S1](docs/adr/2026-08-07-loop-s1-environment-ratification.md)
  · [idle-clock audit](docs/notes/audits/programme-audit/2026-08-05-post-descope-claim-alignment-audit.md).
- **Coverage evidence:** week 09-07→09-11 is operator-attested: on 2026-09-12,
  the operator confirmed placement on Thursday, 2026-09-10, and reported that
  it had already been recorded with Claude. This is the operator's attestation;
  the private compliance record is unavailable in this checkout and was not
  independently verified. On 2026-09-19, the operator confirmed that no
  preservation trade was placed during 09-14→09-18 and reported that the
  account remains active. That week is recorded as missed, not covered;
  active status is operator-reported and not independently verified.
  Week 09-21→09-25 is operator-attested: on 2026-09-23, the operator reported
  placing the trade and shared an order-screen capture in session (a filled
  MYM market round trip; the capture shows no date and is not committed). This
  is the operator's attestation; the private compliance record was not
  independently verified. The 09-21→09-25 obligation is covered; the next
  bucket is 09-28→10-02 (deadline 10-02), advanced once 09-25 passes.
- **Earlier record still owed:** week 08-31→09-04 was operator-attested on
  09-04 and restated on 09-05; the exact trade day remains unresolved between
  09-02/09-03, and its private ledger row remains unverified.
  [Campaign record §15](docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md#15-d20--the-acceleration-ruling-2026-09-04-deploy-at-the-phase-3-commit)
  retains that history. Preserve missed-week records when advancing the
  recurring schedule; record coverage only when it is
  attested; `daily-repo-truth-sync` reads this board's dated obligations.

### Monthly — recurring (rolling; next deadline **2026-10-21**)

- **Subscription reconfirm:** recheck [ledger](docs/pursuits/SUBSCRIPTION_LEDGER.md)
  rows d11–d18, record confirmation even when unchanged, and resolve Fly.io/Tradeify
  unknowns if evidence becomes available. Roll monthly on the 21st; the operator
  confirms the figures. [Owner ADR](docs/adr/2026-08-21-cfo-subscription-ledger-consolidation.md).
- **Coverage record:** the 2026-09-21 reconfirm is **not attested** as of 2026-09-22 —
  recorded as missed, not confirmed. The operator's confirmation of rows d11–d18
  (unchanged or updated) remains owed and is recorded here when given; no figure is
  asserted by this roll. The schedule advanced on 2026-09-22 so the currency gate
  reflects the next obligation rather than a stale one (the Weekly row's convention:
  preserve missed records when advancing; record coverage only when attested).

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
- **PREREG-C1-DEDUPE-1:** M1 prerequisite satisfied 2026-09-14; awaits the
  separate operator GO (none granted by the 2026-09-20 refresh).
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
  qualifying clearance, demote to research-only. T00 cannot discharge it: on
  2026-09-23 the operator ruled a T00 screen is not §4 falsifier evidence
  ([D-T00 condition 4](docs/briefs/handoffs/2026-09-22-tradeify-t00-step1-producer-inventory.md#78-operator-rulings-on-the-return-2026-09-23)), so discharge needs its own dated re-MC. [Four-firm owner](docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md)
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
