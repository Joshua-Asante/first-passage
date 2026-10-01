# Tradeify simplification decision packet — 2026-09-30

**Status: DRAFT FOR OPERATOR DECISION. No decisions adopted or implementation dispatched.**

Recommend external liveness monitoring and notification delivery while retaining the protected qualification service. Evaluate detached signed deployment approval before committing to replacing the GO image rebuild. Retain the adopted same-sample recovery requirement unless a bounded comparison establishes that deferral is cheaper without compromising the campaign's no-redraw contract. These choices concern prospective work; this packet establishes no code deletion.

Joshua owns the decisions below. The deployment coordinator owns owner-document amendments, bounded handoffs and combined acceptance. This assignment prepares a reviewable packet; it grants no account operation, service purchase, deployment, arming or live-session GO.

**Review revision, October 1:** corrected the immutable-ADR change route, provider-review prerequisite and deployment-key scope. The original recommendation to defer recovery was premature: avoided implementation work was not compared with interruption loss or additional successor controls. The following priorities replace that blanket recommendation; no operator ruling is changed.

| Priority | Next reviewable outcome | Work avoided or deferred | Stop condition |
| --- | --- | --- | --- |
| 1 — D-MON | One external heartbeat service and one verified phone channel, with provider review | Internal missed-ping scheduler and delivery infrastructure | Provider/channel cannot meet the agreed notification deadline or dependency requirements |
| 2 — D-GO | Signed-approval contract and bounded cost comparison against reseal | Potential GO-only rebuild and layer-reseal ceremony | Secure activation requires more new authority/state machinery than the reseal it replaces |
| 3 — D-REC | Compare remaining H9 R2 work with conservative termination | Potential recovery implementation, at the cost of lost attempts | Deferral savings or lawful interruption disposition are unproven; retain D3 |
| Conditional — D-HIST | Map existing receipts and successor-admission controls | Avoid a parallel lineage database | No successor is authorized: no new successor machinery is needed for the current attempt |

For each comparison return the actual remaining modules, interfaces, verification cases and recurring operator steps on each path. Include applicable contract changes and requalification work; exclude already-built sunk cost. No hour estimates or net savings are established by this packet. A documented outcome that removes no required work is not a simplification.

## 1. Scope and evidence

The [deployment checklist](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md) remains the roadmap. This packet addresses R4–R6 from Claude's feasibility return and records the subsequent R1 TradingView comparison below. Both returns were pasted into this conversation. The complete returned report has not been located in this checkout; its conclusions are attributed inputs, not accepted repository evidence. Production sources and the owning contracts below were read independently.

Tradeify permission is not reopened. The [commissioning packet F-6(a)](2026-09-27-route-commissioning-session-packet.md) records the September 28 written conditional permission for the CrossTrade-mediated setup; Joshua confirmed on September 30 that hosting permission has already been established and recorded. The cited row does not itself reproduce a cloud-specific approval. The original private correspondence was not inspected for this packet. Claude's TradingView comparison has now returned; Joshua authorized recording the assessment directly on September 30.

Route commissioning is progressing separately. At preparation on September 30, the primary checkout's in-progress drill-plan update recorded X-1 acceptance and its separate X-4 draft was prepared for review. Those concurrent changes are not included in this packet's PR and are not accepted by it. The [committed commissioning packet](2026-09-27-route-commissioning-session-packet.md) and [drill plan](2026-09-26-tradeify-route-drill-plan-draft.md) remain the route owners; consult their latest accepted revisions for operational status. The earlier return's statement that no commissioning row had run must not be carried forward as current status. This packet discharges no route or deployment gate.

### R1 return — TradingView does not establish a cheaper equivalent host

**Recorded assessment, September 30:** retain the Python host for the current release. TradingView has not demonstrated a cheaper, behaviorally equivalent replacement; the published terms also restrict the proposed automated uses absent an applicable agreement. Recording this assessment grants no new feed, funding, deployment or strategy authority and does not amend the signal-host owner.

Claude compared Python-hosted ports (A), stateful Pine order proposals (B), raw-bar alerts into unchanged ports (C1), and Pine indicator values consumed by rewritten ports (C2). Independent checks support the main engineering concern: [BookStrategy](../../ops/c1_signal_daemon/book_protocol.py) separates completed-bar evaluation from confirmed execution feedback, and [qualification's trust domain](../../ops/c1_rail/qualification/trust_domain.py) binds port code, feed and indicator code. TradingView's [alert documentation](https://www.tradingview.com/pine-script-docs/concepts/alerts/) describes strategy-fill alerts from its broker emulator and running alerts as frozen snapshots of script, inputs, symbol and timeframe. Stateful Pine proposals therefore need additional handling for divergence from real fills, rejects, cancels and externally initiated closes. No per-strategy outcome in Claude's table is independently certified here.

Raw-bar alerts retain local execution feedback but exchange a provider integration for webhook ingress and alert operations. The [runtime](../../ops/c1_signal_daemon/book_runtime.py) refuses noncontiguous bar boundaries. TradingView documents realtime alert triggering; the proposed one-bar alert transport supplies no demonstrated historical replay or correction channel. Claims of net engineering savings remain qualitative, without a workload comparison. An indicator-value interface adds a parity and qualification surface. Stateless entry proposals are also possible: B need not become C2, but moving real-position decisions back into the controller leaves the claimed savings unproven.

TradingView's [terms §3](https://www.tradingview.com/policies/) explicitly restrict non-display use of alerts and webhooks, including automated trading and algorithmic decisions. Its alert documentation nevertheless describes custom alert messages routing actual orders to a third-party execution engine. Record that documentation conflict; the product example does not itself establish permission overriding the terms. These are published-document findings checked September 30, not a legal determination. Detection or enforcement likelihood was not established and must remain separate from the permission conclusion.

Tradeify hosting permission is treated as established by Joshua's confirmation above; Claude's repeated open-hosting question is superseded for this assessment. Exchange/provider licensing for an eventual automated feed remains unverified here and belongs in the existing feed/funding decision. No new vendor inquiry is required by this packet. CrossTrade webhook compatibility does not establish TradingView permission.

**Disposition:** no TradingView replacement work is proposed for this release. Keep licensed market-data selection with its existing owner and funding decision. Reopen only with materially different engineering evidence or applicable permission; no special licence is assumed available. Continue the R4–R6 simplifications below. This records the assessment without declaring TradingView technically impossible or universally unsuitable for other strategies.

## 2. D-MON — buy liveness monitoring and alert delivery

**Question:** Should an external service detect missed rail heartbeats and deliver notifications, while the rail retains semantic incident handling?

| Option | Consequence |
| --- | --- |
| Adopt external heartbeat monitoring and proven phone delivery — recommended | Avoid building scheduling, missed-ping detection, delivery integrations and their operational maintenance. Retain a small internal publisher and trading-specific incident logic. |
| Build those capabilities internally | Own detection and delivery availability, testing and maintenance in addition to the rail. |

The current [FileAckNotifier](../../ops/c1_rail/c1_rail_telemetry.py) writes alerts and acknowledgment files; the [server wiring](../../ops/c1_rail/c1_rail_http_server.py) selects it or LoggingNotifier. Those paths do not demonstrate delivery to a person. [Healthchecks documentation](https://healthchecks.io/docs/) supports scheduled HTTP pings, grace periods, failure signals and notification integrations. It is suitable for external liveness detection; a ping is not evidence that positions, orders or trading authority are safe. Provider documentation was checked September 30.

**Proposed decision:** use Healthchecks for the first monitored release, with a delivery integration verified on Joshua's phone. Start with a no-cost configuration if it supplies the required channel; any paid plan or additional push service needs separate purchase authorization. Store ping credentials outside version control. Keep provider settings reproducible as configuration, with secret references.

Keep the first release to one monitoring provider and one proven delivery channel; a second paid push service is not a default. Complete the M1 owner's provider dependency and secret-handling review before integration acceptance: provider availability/outage behavior, credential permissions and rotation, retained/exported data, channel dependency and delivery limits. Do not export raw account, order or strategy details; send a permitted incident identifier and minimal status. M1 is already recorded RESOLVED: this is an additional delivery capability, not a claim that accepted attended monitoring was never valid. Amend the acceptance evidence only for the added dependency and behavior.

Retain local detection of unknown sends, protection failures and other semantic incidents, durable incident records, and operator acknowledgment. External delivery receipts do not clear an incident. A monitoring outage must have a defined local response and operator procedure; outsourcing must not silently weaken M1 or permit unattended operation.

**Acceptance evidence:** a killed publisher produces a phone notification within the agreed deadline; an explicit rail incident reaches the phone; delivery failure remains visible locally; recovery does not acknowledge or rearm automatically; acknowledgment remains associated with the correct incident across restart. Record measured latency and the accepted deadline in the M1 owner, rather than inventing a threshold here. Verify that a healthy publisher cannot mask the dead execution component it is supposed to monitor.

Bind heartbeat publication to observed rail/daemon progress under defined idle/session states, rather than an independent always-running timer. Keep feed freshness and semantic incidents locally authoritative. Notification network calls must be bounded and outside the order/protection path; a provider timeout cannot delay a protective action. Ordinary heartbeat recovery cannot clear a latched incident. If one provider carries both signals, demonstrate that separation. The [Healthchecks ping API](https://healthchecks.io/docs/http_api/) documents success/failure signals, rate limits, and HTTP 200 responses even for ignored pings; verify the response body as well as the status and set a cadence within provider limits (checked October 1). Return phone delivery evidence, not merely an accepted ping.

**Unresolved:** notification channel, latency requirement and loss-of-monitoring response need to be fixed in the bounded handoff. Without a decision, current monitoring obligations remain; file logging alone is not newly accepted as delivery.

## 3. D-GO — detached signed deployment approval

**Question:** Replace the unbuilt artifact-only GO commit, image rebuild and reseal with an operator-signed approval of the already qualified release?

| Option | Consequence |
| --- | --- |
| Evaluate a detached signed approval — recommended next step | Establish whether avoiding the GO-only rebuild saves work after signature, identity, freshness and activation obligations are included. Adopt only by a superseding contract decision. |
| Retain the baked GO design | Implement the artifact-only commit and strict image-layer reseal proof currently required by the admission contract. |

The [admission ADR §2b and §2c](../adr/2026-09-12-tradeify-book-protection-instance-admission.md) currently requires baked GO and rejects volume-based approval. Its revert instruction forbids editing the decision text: a change must supersede it. The [Dockerfile](../../deploy/c1_rail/Dockerfile) packages the [Ed25519 verifier](../../ops/c1_rail/ed25519_verify.py), operator-key enrollment and qualification verification code. Static packaging does not establish the running host's identity or a working deployment gate. [Settlement signing](../../ops/c1_rail/settlement_signing.py) supplies a related signing pattern, not a deployment authorization schema.

**Proposed next decision:** authorize preparation of a distinct ADR that would supersede only the GO delivery/reseal obligations if its bounded comparison supports adoption. Leave qualification, fingerprints, seal and effective-activation requirements intact. Bind a purpose-specific canonical signed approval to the fixed-book replay fingerprint, complete execution image/config manifest, account snapshot seal and validity, qualifying n3 result, decision record, operator key identity and deployment authorization identity. Preserve the existing initial-activation freshness and no-intervening-account-activity requirements. Keep private account bindings private.

Reuse the verifier and enrollment pattern after compatibility review; existing settlement enrollment is not deployment authority. The [settlement consumer](../../ops/c1_rail/book_settlement.py) limits scopes to account-close submission and record-only. Require separately enrolled deployment authority, or an explicit enrollment-schema/scope contract change; settlement-only keys must be refused. Pin the deployment trust root and validator in the qualified release. Signed bytes may travel through mutable storage, but their authenticity does not prevent rollback: the design must define durable consumption/revocation and fresh boot/session binding, and refuse old approval or activation evidence after restart. State the trusted storage and operator-attestation assumptions explicitly. Distinguish ordinary restart/config replay from privileged rollback of the entire host or volume; a signature alone protects neither mutable state nor a compromised verifier. Compare both options against the same admitted threat model, without assuming a new remote authority service is necessary.

The host's effective activation path must enforce the gate, including config edits and delayed restart. The arm helper alone is insufficient. Missing, expired, revoked, wrong-purpose, wrong-release, wrong-config, wrong-seal and replayed approvals must start disarmed and admit no risk-add. Approval does not replace M1, current-state reconciliation or separate session GO. Later-session authority remains separately defined by its owner.

**Acceptance evidence:** synthetic valid and invalid signatures; refusal of settlement-only enrollment; every identity mismatch; direct config-write/restart bypass; expiry between preparation and activation; replay after consumption, revocation or restart; changed key set; and missing durable state. Demonstrate that qualification identities are unchanged when approval is issued. Resolve the anti-rollback mechanism before treating this as cheaper than resealing.

**Owner change route:** a distinct superseding ADR with explicit scope covering the admission ADR's GO delivery/reseal obligations (§2b/§2c/§5); retain the original decision text and add the appropriate supersession pointers/index edges. Update TB-I3/TB-D2/TB-O1 obligations, the deployment roadmap and affected release-spec consumers after adoption. Keep the current contract in force until its successor is accepted. Without a decision, baked GO and reseal remain required. No existing verifier or signing code is proposed for deletion.

## 4. D-REC — defer same-sample recovery

**Question:** Should the first qualification release stop conservatively after an interrupted execution rather than implement bounded same-sample recovery before S8?

| Option | Consequence |
| --- | --- |
| Retain the adopted recovery requirement — default pending comparison | Complete the remaining H9 R2 work and its recovery acceptance before the downstream qualification release. |
| Explicitly defer recovery if the comparison supports it | Avoid the remaining recovery slice now. An interrupted attempt can become terminal and consume its authority/budget; convenience and compute availability are sacrificed. |

The [S5 decision draft D3](2026-09-26-s5-decision-draft.md) records Joshua's adoption of recovery after S5 and before S8. [H9](../briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md) separates result/seal integration R1 from recovery R2 and retains combined acceptance. The [protected campaign specification](../superpowers/specs/2026-09-17-protected-full-e1-campaign.md) and [execution slices](../superpowers/plans/2026-09-18-full-e1-execution-slices.md) govern sampling, budgets, evidence and retries. Deferral therefore needs an explicit amendment to D3 and downstream prerequisites.

**Proposed next decision:** compare the remaining H9 R2 implementation/acceptance work with a terminal-only release before ruling on deferral. Include probability or observed frequency of interruption where evidence exists, compute/operator cost of a lost attempt, and the actual successor-control gaps under D-HIST. Where these costs are unknown, report the uncertainty rather than claiming a saving. Retain the protected service and its accepted assurance boundaries. If deferral is adopted explicitly, keep H9 R1 result/seal integration and all applicable acceptance checks. On an uncertain execution, preserve the conservative terminal/IN_DOUBT disposition and its evidence; do not clear it by restart, renew its budget or deadline, generate another sample, or conceal it in a successful successor.

This decision grants no additional draw or replacement attempt. Any successor requires separate authority under the campaign contract, with the earlier outcome retained. Failed qualification remains failed. Deferral does not change statistical gates, qualification depth, locked controls or execution semantics. Record the exact remaining release prerequisites after amendment; do not declare S8 ready merely because R2 was removed.

**Acceptance evidence:** interruption and restart remain closed; result/seal handling distinguishes failure from missing evidence; budget/deadline cannot reset; no public reveal while a retry is still authorized; and no successor can silently bypass the predecessor disposition. Preserve existing evidence, including failures. Recovery may be reconsidered if observed interruption losses justify its implementation.

**Unresolved/dissent:** recovery was already deliberately adopted, and the cost of lost attempts is not quantified here. Deferral may reduce engineering but make the only authorized qualification attempt more fragile. Same-sample recovery cannot be replaced by an assumed fresh attempt: no replacement draw is granted. Without an explicit deferral ruling supported by the comparison, the adopted before-S8 recovery requirement remains. The qualification-release boundary (S8) is distinct from an attended trading session; the no-same-session restart trading rule does not itself decide qualification recovery.

## 5. D-HIST — retain a protected cross-attempt history

**Question:** Establish a minimal protected lineage record before any separately authorized successor attempt, without creating another general workflow service?

| Option | Consequence |
| --- | --- |
| Reuse the protected store and add only missing lineage checks — recommended | Make predecessor outcomes and successor authority reviewable and enforceable without duplicating existing journals. |
| Rely on disconnected attempt records and manual reconstruction | Save a small amount of integration work, but make selective reporting and unauthorized replacement harder to detect. |

The existing [campaign store](../../ops/c1_rail/qualification/execution/campaign_store.py) already retains per-attempt objects, validity and budget history, with unique attempt/campaign identities. That is evidence against building a parallel logging system. It does not, by itself, establish a complete cross-attempt admission policy. Existing funding predecessor checks concern funding work and must not be mistaken for research-attempt lineage.

**Proposed decision:** require retained lineage at the protected admission boundary before any separately authorized successor. First map existing records and consumers; add only demonstrated missing links/checks. Do not make hypothetical successor machinery a new gate on the sole current attempt when no successor is authorized. Existing per-attempt retention and no-redraw gates remain required. Each authorized successor must identify its predecessor(s), their terminal disposition and retained evidence, the explicit successor authorization and reason, and the unchanged or separately admitted contract identity. Distinguish operational interruption, qualification failure, void/revocation and successful completion. Preserve failed results in the campaign's reported history; a successor cannot rewrite them.

Keep secrets, seeds and unrevealed sample material inside their existing protected boundaries. A public summary can carry permitted identities/digests and dispositions; it must not expose private book/account data. A reporting-only log is insufficient if admission can bypass it. An unresolved predecessor needs an explicit contract ruling; this packet does not make it eligible for replacement.

**Acceptance evidence:** multiple retained attempts survive restart; history cannot omit an earlier failed attempt; duplicate identities are refused; unauthorized successor admission is refused; missing/tampered predecessor evidence fails closed; existing receipts and budget history remain valid. If existing machinery already meets these obligations, return conformance evidence and avoid a new store.

Without a decision, this packet grants no successor authority and does not accept disconnected records as sufficient lineage. If D-REC is adopted, resolve this obligation before any successor is admitted.

## 6. Decision return and next bounded handoff

Joshua can decide each item separately: **D-MON adopt/retain; D-GO evaluate/retain; D-REC compare/retain (deferral is a later explicit ruling); D-HIST assess existing coverage/retain**, with any conditions. Silence adopts none. There is no combined implementation GO in this packet.

After D-MON adoption, the first bounded handoff should deliver **verified phone notification for rail liveness and one semantic incident**, with the required provider dependency and secret-handling review, configuration, measured delivery evidence and an acceptance delta for the added monitoring capability. Separate offline integration checks from a real phone-delivery probe using synthetic incident data: an offline mock cannot establish phone reachability. Return to the coordinator after those bounded checks; stop before purchase, host activation, arming or live execution unless separately authorized. Existing incident gates remain in force. This outcome can proceed independently of changing the GO contract.

For D-GO evaluation, return the exact superseding-ADR proposal, key-authority design, threat model, cost comparison and affected-consumer inventory before an adoption ruling. For D-REC comparison, return the remaining-work/attempt-loss comparison and exact D3/H9/S8 prerequisite changes that deferral would need. Only after operator adoption and coordinator acceptance of the owner changes should the corresponding implementation handoff be frozen. D-HIST starts with a bounded conformance/gap assessment of existing storage and admission consumers; it does not authorize a qualification-engine rewrite or an extra release gate for an unauthorized successor.

Deliberately not done: TradingView implementation or owner-contract amendment, renewed vendor contact, route-drill execution, data-feed selection, live host inspection, qualification-service migration, legacy rail restart repair, code deletion, purchases or standing-guidance changes. No numerical risk or qualification setting is changed.

**Preparation verification:** source and owner-document review; relative-file links and whitespace checks. No runtime behavior has been implemented or tested by this packet. Final preparation check results are reported with delivery.

## 7. October 1 brainstorming — shorten the path to a full-portfolio eval

**Operator constraint:** Joshua selected “Deploy all four strategies together, preserving the full portfolio behavior.” A subset, altered sizing, disabled required strategy behavior or a different portfolio is outside this proposal. Joshua authorized adding this discussion to the PR; that authorizes recording the proposals, not adopting them or executing an eval session.

**Target to evaluate:** one bounded, attended eval release with all four strategies and conservative incident termination. The current roadmap already provides one attended session; the proposed saving is a narrower maturity requirement for that session, not a new claim that attendance alone makes deployment safe. Learn delivery performance, operator workload and operational reliability during the eval where failures can be contained. Keep behavior, portfolio qualification and release authority unchanged unless their specific owners accept a change.

This section challenges whether D-MON and D-GO should be first-session prerequisites at all. It does not adopt them as extra gates. D-REC concerns qualification execution, not live trading restart; the existing prohibition on same-session restart after a trading incident does not decide same-sample compute recovery.

### 7.1 Candidates to remove, defer or resequence

| Existing work or requirement | Candidate first-eval treatment | Evidence and owner decision needed |
| --- | --- | --- |
| Automatic operational recovery, reconnect and restoration | Halt on uncertainty and end automation for the session; defer automatic repair and resumption | T09/T13 and incident/halt owners establish detection, fencing, continuing protection, attended reconciliation and disarmed restart. Ordinary transport reconnection must be distinguished from resuming a halted strategy. |
| External heartbeat, phone escalation and additional delivery infrastructure | Assess whether the accepted attended M1 channel can cover the first bounded session; add external delivery later if it is not essential to that session | M1 and T13 owners reconcile the exact first-session monitoring/escalation obligations with the accepted channel. File-based reachability alone does not prove every required response time. Do not withdraw an existing accepted capability. |
| Cross-attempt successor machinery | Preserve existing per-attempt evidence; build additional successor controls only before a successor is separately authorized | D-HIST conformance assessment; current attempt retention and no-redraw obligations remain. |
| Detached signed GO redesign | Finish the current release mechanism if its remaining work is cheaper than the replacement | D-GO comparison includes both implementation and recurring operator steps. No bypass of the host activation gate; any architecture change follows a superseding ADR. |
| Feed backfill and correction automation | Evaluate a halt-only live-feed path, with no repair or replay during the incident session | T14/TB-I5 and halt owners distinguish historical warm-up, delivered-bar equivalence, detectable gaps/corrections and automatic repair. Keep sufficient warm-up and initial identity/equivalence evidence. Unobservable corrections cannot be claimed contained simply by promising a halt. |
| Long-term operational maturity | Defer routine upgrade automation, multi-host support, automated daily settlement and broader unattended operation where they are not needed by the first session | Map actual planned work before claiming savings; these are not established current launch blockers. Retain an accepted attended settlement procedure for every authorized subsequent session. |
| Provider selection/funding delayed behind source-independent gates | Consider an earlier bounded feed decision and adapter/shadow work alongside qualification engineering | Explicit change to the O-4/CP-7 sequencing restriction; permitted budget, provider scope and cancellation consequence. No provider selection, contact or spend is authorized here. |
| Repeated acceptance/review ceremonies | Reuse source-bound unchanged evidence and combine overlapping review into one candidate acceptance | Coordinator identifies duplication versus checks of distinct guarantees. Retain required CI and independent review; combine records, not incompatible acceptance identities. |

These are hypotheses, not verified net savings. Halt-only behavior is useful only when the failure is detectable soon enough and stopping leaves the account in an accepted state. Stopping new entries does not resolve an unknown request or guarantee protection of an existing position. If a required lifecycle depends on a deferred capability, retain it before launch or return an explicit incompatibility; do not silently suppress the behavior.

### 7.2 Outcomes to retain before first orders

The release must establish the following through the real supported boundaries and relevant failure traces:

- Confirmed broker fills, cancels and rejects reach the ports; simulated positions are not substituted.
- Every enabled strategy's required entry, protection, amendment and exit lifecycle works on the chosen route.
- Unknown requests preserve reservations, fence further risk-add and cannot produce duplicate entries through retries or restart.
- Shared capacity, takeover and cutoff behavior remain consistent across all four strategies.
- The feed provides correctly identified and timely inputs, required warm-up and the admitted equivalence evidence.
- Current account/settlement state, sizing authority, exact release identity and host activation checks are valid.
- The operator can intervene through a proven procedure; incidents retain evidence and end automation, and restart begins disarmed.

These are a scoping aid, not a replacement acceptance checklist. [Book policy](../../ops/c1_rail/book_policy.py) rejects absent/mismatched protection authority; the [policy registry](../../core/dd_geometry.py) requires admitted instances. Neither an eval designation nor attendance supplies that authority. No protection constants, portfolio parameters or admission defaults are changed here.

### 7.3 Challenge qualification and final n3 explicitly

Statistical prerequisites should also be evaluated for decision value. For each E1/n3 stage, identify the uncertainty resolved, the acceptance claim it supports, whether existing evidence covers it and what an alternative would leave unproven. Operational observations during an eval do not automatically replace regime qualification or account-state-conditioned evidence. Any removal/substitution needs a distinct operator-owned admission decision under the existing change-control route; qualification remains required until then. Preserve failed results and no-redraw rules throughout the comparison.

### 7.4 Proposed next reviewable outcome

Prepare one requirement audit against the current T07–T17 roadmap and remaining qualification work. For each prerequisite return: concrete first-session failure prevented; current source/evidence; retain/defer/remove/resequence recommendation; exact containment and residual exposure; affected owner; remaining engineering and operator steps; decision needed; and the later event that would require a deferred capability. Use the current accepted implementation, not a generic best-practice checklist.

Prioritize (1) a halt-only operational scope, (2) earlier bounded feed integration, and (3) qualification/release evidence versus repeated ceremony. The audit returns to Joshua and the coordinator before any implementation or owner-contract change. It is not a fresh full-system redesign. Remove a requirement only when its first-session guarantee is unnecessary or has a demonstrated replacement; do not move mandatory correctness testing into live exposure and call it learning.

The earlier 4–8 week launch estimate assumed the existing roadmap and was provisional. No revised delivery date or time saving is established by this discussion. The simplification packet must support the shortest defensible eval release, rather than become another project that must be completed before trading.

## 8. October 1 follow-up — remove serial waits and duplicated machinery

Joshua requested a further review of deletions, simplifications and optimizations, then authorized recording these recommendations and requesting Codex review. This section refines §7's audit priorities; it adopts no sequencing, CI, authority or admission change. Preserve all four strategies and their full behavior. Distinguish elapsed-time savings for this release from recurring savings after launch.

| Priority / opportunity | Concrete proposed investigation | Current evidence, boundary and decision owner |
| --- | --- | --- |
| 1 — earlier result/seal integration evidence | Allow a bounded acceptance-grade integration run once the relevant S5 interfaces are stable, while withholding combined acceptance until S5 is accepted | [H9](../briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md) permits integration preparation but explicitly prohibits acceptance-grade runs before full S5 acceptance. Changing that restriction needs a coordinator-owned handoff amendment within the operator's authority. It is not permission to run now. A source change that affects the evidence invalidates it; pending S5 findings must be reconciled before acceptance. |
| 1 — earlier actual-feed work | Prepare an earlier bounded provider/funding decision, then adapter and emission-disabled shadow collection alongside qualification | O-4/CP-7 in the [deployment roadmap](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md) currently restrict provider-specific work. Joshua must change that sequence and approve applicable spend/contact. Return the wasted-work/cancellation consequence if qualification fails. Do not relax equivalence, licensing, warm-up or feed identity requirements. |
| 2 — shared n3 implementation | Determine whether final n3 can use shared execution/capture machinery under a separately authorized invocation instead of duplicating an execution subsystem | T12 requires separate n3 authorization, capture and adjudication; this does not establish that duplicate implementation is required or currently planned. Trace actual reusable interfaces first. Retain distinct sample identities, permissions, result binding and no-redraw semantics; E1 must not acquire n3 authority. T12 and qualification owners accept the resulting design before implementation. |
| 2 — stop-only first-session operations | Complete fault detection, fencing, continuing protection and attended intervention; defer automatic restoration and later-session resumption where not needed | T09/T13 and incident/halt owners determine the reduced scope. Keep ordinary strategy lifecycles and confirmed execution feedback. A halted session cannot resume; unresolved requests remain obligations. Stopping new entries is not evidence that existing positions are protected. |
| 3 — reusable integrated evidence | Use one candidate manifest referencing accepted route, feed, settlement and qualification evidence; repeat only affected checks plus required combined acceptance | T10/T16 and the coordinator map provenance, source/configuration identity, dependencies and invalidation rules. Do not replace independent evidence with summaries or treat unchanged source as proof of unchanged external state. Existing manifests are reuse candidates; avoid a new orchestration system. |
| 3 — avoid added launch prerequisites | Determine whether external phone delivery, signed-GO redesign and additional successor machinery are necessary for the first-session contract | D-MON/D-GO/D-HIST comparisons apply. Retain existing accepted capabilities and current obligations until the relevant owner adopts a change. The packet is not itself a checklist of additional mandatory builds. |

### 8.1 Smaller optimizations with bounded claims

**Documentation CI:** [.github/workflows/qualification-execution-boundary.yml](../../.github/workflows/qualification-execution-boundary.yml) currently provisions two Linux hosts on every pull request. Investigate skipping that expensive workflow only for explanatory prose changes that demonstrably leave its protected execution inputs and authority contracts unchanged. Do not use a blanket `docs/**` exclusion: documentation can define policy, prerequisites and runtime authority. Any trigger/composition change goes through the gate owner, [scripts/gates.yml](../../scripts/gates.yml), its admission process and required branch-check behavior. Retain required CI and exact-head review. This is a proposed configuration change, not standing permission to edit workflow settings. Its likely benefit is shorter review cycles and lower runner use; no weeks of deployment savings are established.

**Launch-window readiness:** investigate admitting a precisely bounded calendar/contract window rather than building automated rollover, all holiday operation or routine upgrades before the first session. First inventory whether those are actual remaining requirements; do not claim savings from imaginary blockers. The window must cover all four strategies' intended behavior during the admitted session and be enforced at activation and runtime. Correct symbols, historical warm-up, source/session calendars and cutoffs remain prerequisites. An unsupported date outside the window stays unavailable until qualified. Calendar/feed and lifecycle owners must assess whether the restriction is a new expression requiring pre-registration or requalification; it cannot silently alter full-portfolio behavior.

### 8.2 Exclude work that does not accelerate this launch

Exclude general unused-code cleanup unless it causes a launch defect, qualification-service migration, new dashboards, generalized orchestration, a parallel lineage database, unnecessary delivery infrastructure, and new documentation duplicating accepted owner records. These are prospective scope exclusions, not established safe code deletions. A real deletion still needs a producer/consumer and deployment-reachability check, replacement evidence where applicable, and the owning change decision. Do not delete accepted evidence or frozen/private strategy artifacts.

### 8.3 Separate statistical decision value from execution correctness

For production E1 and final n3, state what decision could change because of each result. Separate evidence about the portfolio/protection policy, current account state, and implementation parity. A stage that repeats the same accepted claim may be a candidate for removal or replacement; stages establishing different claims cannot be eliminated by combining their paperwork. Current requirements remain binding during the audit. Removing statistical evidence needs an explicit replacement admission decision; an eval designation does not supply one. Preserve no-redraw rules and failed results.

**Recommended order:** remove avoidable sequencing barriers first; define the minimum first-session operating scope; require demonstrated reuse before building new n3/manifest/notification machinery; challenge E1/n3 for duplicated decision value; leave cosmetic cleanup and platform improvements until after deployment. Fold these rows into §7.4's single requirement-audit return, rather than opening another general review project. No revised launch date is claimed.
