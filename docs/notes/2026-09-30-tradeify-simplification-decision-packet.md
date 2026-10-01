# Tradeify simplification decision packet — 2026-09-30

**Status: DRAFT FOR OPERATOR DECISION. No decisions adopted or implementation dispatched.**

Recommend buying external liveness monitoring and notification delivery, replacing the planned GO image rebuild with a detached signed approval, and retaining the protected qualification service. Recommend deferring same-sample recovery only through an explicit contract amendment, paired with protected cross-attempt history. These choices reduce prospective work; this packet establishes no code deletion.

Joshua owns the decisions below. The deployment coordinator owns owner-document amendments, bounded handoffs and combined acceptance. This assignment prepares a reviewable packet; it grants no account operation, service purchase, deployment, arming or live-session GO.

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

Retain local detection of unknown sends, protection failures and other semantic incidents, durable incident records, and operator acknowledgment. External delivery receipts do not clear an incident. A monitoring outage must have a defined local response and operator procedure; outsourcing must not silently weaken M1 or permit unattended operation.

**Acceptance evidence:** a killed publisher produces a phone notification within the agreed deadline; an explicit rail incident reaches the phone; delivery failure remains visible locally; recovery does not acknowledge or rearm automatically; acknowledgment remains associated with the correct incident across restart. Record measured latency and the accepted deadline in the M1 owner, rather than inventing a threshold here. Verify that a healthy publisher cannot mask the dead execution component it is supposed to monitor.

**Unresolved:** notification channel, latency requirement and loss-of-monitoring response need to be fixed in the bounded handoff. Without a decision, current monitoring obligations remain; file logging alone is not newly accepted as delivery.

## 3. D-GO — detached signed deployment approval

**Question:** Replace the unbuilt artifact-only GO commit, image rebuild and reseal with an operator-signed approval of the already qualified release?

| Option | Consequence |
| --- | --- |
| Adopt a detached signed approval — recommended, subject to contract amendment | Avoid rebuilding the executable image solely to insert approval. Implement signature, identity, freshness and activation checks against the exact qualified release. |
| Retain the baked GO design | Implement the artifact-only commit and strict image-layer reseal proof currently required by the admission contract. |

The [admission ADR §2b and §2c](../adr/2026-09-12-tradeify-book-protection-instance-admission.md) currently requires baked GO and rejects volume-based approval. This proposal changes that accepted contract; a coordinator cannot substitute it silently. The [Dockerfile](../../deploy/c1_rail/Dockerfile) packages the [Ed25519 verifier](../../ops/c1_rail/ed25519_verify.py), operator-key enrollment and qualification verification code. Static packaging does not establish the running host's identity or a working deployment gate. [Settlement signing](../../ops/c1_rail/settlement_signing.py) supplies a related signing pattern, not a deployment authorization schema.

**Proposed decision:** authorize an amendment replacing the GO-only rebuild/reseal with a purpose-specific, canonical signed approval. Bind it to the fixed-book replay fingerprint, complete execution image/config manifest, account snapshot seal and validity, qualifying n3 result, decision record, operator key identity and deployment authorization identity. Preserve the existing initial-activation freshness and no-intervening-account-activity requirements. Keep private account bindings private.

Reuse the verifier and key enrollment after compatibility review; do not reuse a settlement signature as deployment authority. Pin the trusted key set and validator in the qualified release. Signed bytes may travel through mutable storage, but their authenticity does not prevent rollback: the design must define durable consumption/revocation and fresh boot/session binding, and refuse old approval or activation evidence after restart. State the trusted storage and operator-attestation assumptions explicitly.

The host's effective activation path must enforce the gate, including config edits and delayed restart. The arm helper alone is insufficient. Missing, expired, revoked, wrong-purpose, wrong-release, wrong-config, wrong-seal and replayed approvals must start disarmed and admit no risk-add. Approval does not replace M1, current-state reconciliation or separate session GO. Later-session authority remains separately defined by its owner.

**Acceptance evidence:** synthetic valid and invalid signatures; every identity mismatch; direct config-write/restart bypass; expiry between preparation and activation; replay after consumption, revocation or restart; changed key set; and missing durable state. Demonstrate that qualification identities are unchanged when approval is issued. Resolve the anti-rollback mechanism before treating this as cheaper than resealing.

**Owner amendments:** admission ADR §2b/§2c/§5, TB-I3/TB-D2/TB-O1 obligations, deployment roadmap and affected release-spec consumers. Keep the current contract in force until those amendments are accepted. Without a decision, baked GO and reseal remain required. No existing verifier or signing code is proposed for deletion.

## 4. D-REC — defer same-sample recovery

**Question:** Should the first qualification release stop conservatively after an interrupted execution rather than implement bounded same-sample recovery before S8?

| Option | Consequence |
| --- | --- |
| Explicitly defer recovery — recommended for the first attended release | Avoid the additional recovery slice now. An interrupted attempt can become terminal and consume its authority/budget; convenience and compute availability are sacrificed. |
| Retain the adopted recovery requirement | Complete H9 R2 and its recovery acceptance before the downstream qualification release. |

The [S5 decision draft D3](2026-09-26-s5-decision-draft.md) records Joshua's adoption of recovery after S5 and before S8. [H9](../briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md) separates result/seal integration R1 from recovery R2 and retains combined acceptance. The [protected campaign specification](../superpowers/specs/2026-09-17-protected-full-e1-campaign.md) and [execution slices](../superpowers/plans/2026-09-18-full-e1-execution-slices.md) govern sampling, budgets, evidence and retries. Deferral therefore needs an explicit amendment to D3 and downstream prerequisites.

**Proposed decision:** retain the protected service and its accepted assurance boundaries; defer H9 R2 for the first attended release. Keep H9 R1 result/seal integration and all applicable acceptance checks. On an uncertain execution, preserve the conservative terminal/IN_DOUBT disposition and its evidence; do not clear it by restart, renew its budget or deadline, generate another sample, or conceal it in a successful successor.

This decision grants no additional draw or replacement attempt. Any successor requires separate authority under the campaign contract, with the earlier outcome retained. Failed qualification remains failed. Deferral does not change statistical gates, qualification depth, locked controls or execution semantics. Record the exact remaining release prerequisites after amendment; do not declare S8 ready merely because R2 was removed.

**Acceptance evidence:** interruption and restart remain closed; result/seal handling distinguishes failure from missing evidence; budget/deadline cannot reset; no public reveal while a retry is still authorized; and no successor can silently bypass the predecessor disposition. Preserve existing evidence, including failures. Recovery may be reconsidered if observed interruption losses justify its implementation.

**Unresolved/dissent:** recovery was already deliberately adopted, and the cost of lost attempts is not quantified here. The recommendation favors less first-release engineering at the expense of recoverability. Without a decision, the adopted before-S8 recovery requirement remains.

## 5. D-HIST — retain a protected cross-attempt history

**Question:** Establish a minimal protected lineage record before any separately authorized successor attempt, without creating another general workflow service?

| Option | Consequence |
| --- | --- |
| Reuse the protected store and add only missing lineage checks — recommended | Make predecessor outcomes and successor authority reviewable and enforceable without duplicating existing journals. |
| Rely on disconnected attempt records and manual reconstruction | Save a small amount of integration work, but make selective reporting and unauthorized replacement harder to detect. |

The existing [campaign store](../../ops/c1_rail/qualification/execution/campaign_store.py) already retains per-attempt objects, validity and budget history, with unique attempt/campaign identities. That is evidence against building a parallel logging system. It does not, by itself, establish a complete cross-attempt admission policy. Existing funding predecessor checks concern funding work and must not be mistaken for research-attempt lineage.

**Proposed decision:** require retained lineage at the protected admission boundary. First map existing records and consumers; add only the missing links/checks. Each successor must identify its predecessor(s), their terminal disposition and retained evidence, the explicit successor authorization and reason, and the unchanged or separately admitted contract identity. Distinguish operational interruption, qualification failure, void/revocation and successful completion. Preserve failed results in the campaign's reported history; a successor cannot rewrite them.

Keep secrets, seeds and unrevealed sample material inside their existing protected boundaries. A public summary can carry permitted identities/digests and dispositions; it must not expose private book/account data. A reporting-only log is insufficient if admission can bypass it. An unresolved predecessor needs an explicit contract ruling; this packet does not make it eligible for replacement.

**Acceptance evidence:** multiple retained attempts survive restart; history cannot omit an earlier failed attempt; duplicate identities are refused; unauthorized successor admission is refused; missing/tampered predecessor evidence fails closed; existing receipts and budget history remain valid. If existing machinery already meets these obligations, return conformance evidence and avoid a new store.

Without a decision, this packet grants no successor authority and does not accept disconnected records as sufficient lineage. If D-REC is adopted, resolve this obligation before any successor is admitted.

## 6. Decision return and next bounded handoff

Joshua can decide each item separately: **D-MON adopt/retain; D-GO amend/retain; D-REC defer/retain; D-HIST require/retain**, with any conditions. Silence adopts none. There is no combined implementation GO in this packet.

After D-MON adoption, the first bounded handoff should deliver **verified phone notification for rail liveness and one semantic incident**, with configuration, secret handling, measured delivery evidence and updated M1 acceptance evidence. Return to the coordinator after offline/dry-run verification; stop before purchase, host activation, arming or live execution unless separately authorized. Existing incident gates remain in force. This outcome can proceed independently of changing the GO contract.

After D-GO or D-REC adoption, first return the precise amendments and affected-consumer inventory for coordinator acceptance. Only then freeze the corresponding implementation handoff. D-HIST starts with a bounded conformance/gap assessment of existing storage and admission consumers; it does not authorize a qualification-engine rewrite.

Deliberately not done: TradingView implementation or owner-contract amendment, renewed vendor contact, route-drill execution, data-feed selection, live host inspection, qualification-service migration, legacy rail restart repair, code deletion, purchases or standing-guidance changes. No numerical risk or qualification setting is changed.

**Preparation verification:** source and owner-document review; relative-file links and whitespace checks. No runtime behavior has been implemented or tested by this packet. Final preparation check results are reported with delivery.
