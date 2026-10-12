# Conditional native NinjaTrader runtime proposal

**Status:** PROPOSED — docs-only review; not an adopted architecture or deployment gate.

**Date:** 2026-10-12. **Decision owner:** Joshua. **Integration owner:** the existing Deployment Coordinator.

**Companion:** [Aegis disconnected decision experiment plan](../superpowers/plans/2026-10-12-aegis-disconnected-decision-experiment-PROPOSAL.md).

**Disposition:** retain for the coordinator's next native-runtime decision; supersedes no accepted owner record.

A self-contained C# runtime is a plausible alternative for the Tradeify lane: Python remains offline for research, selection and preparation; NinjaScript performs every live calculation, signal, risk decision and order operation. The difficult question is preserving the data, sizing, fill, account and recovery contracts. Translating entry conditions alone does not answer it.

The smallest proposed next step is a read-only dependency/toolchain assessment. A disconnected, order-incapable Aegis prototype would need a later implementation grant. Existing personal-account Python work continues under its current owners.

## §0 — Source grounding

Reviewed dependency source is pinned to `0a0c2a86e4d2e7a07e4b9adede7fea739406b5d1` on 2026-10-12. The earlier October 9 checkout used for initial inspection is not current authority. The reconciliation through #803 covered the source and decisions below; #804 subsequently changed licensing records, not the implementation dependencies. Publication was refreshed onto main `158bf2a871540bb8cd78353c2996662ce216cdd9` (#806): only STATE and its archive changed, confirming current owners and the frozen personal run path; dependency pins and conclusions remain unchanged.

| Source | Relevance |
|---|---|
| [AGENTS.md][agents], [Rule 0][rule0] | Public disclosure, private-read restrictions, source-first assessment and owner boundaries |
| `ops/c1_rail/book_policy.py` [source][policy] | Canonical per-leg sizing and OFF/add rules; protection and capacity laws |
| [book_sizing_context][sizing], [book_bundle_execution][bundle], [book_account_owner][accountowner] | Landed P-L1/P-L3 seams and remaining account-owner binding work |
| [BookProtocol][protocol], [pine_ta][ta], [book_adapters][adapters] | Decision/fill interfaces, arithmetic and accepted source/settings identity |
| [BOOK_SOURCES][manifest] | Already-public pins for accepted private strategy bodies; no bodies or values reproduced here |
| [Synchronized replay][replayspec], [reference emulator][emulator] | Existing ordering and modeled execution contracts |
| [Protection/capacity][riskcontract], [halt/resume][haltcontract], [feed equivalence][feedspec] | Existing safety, schedule, recovery and data requirements |
| [Personal lane ADR][personal], [Q-SFCLEAR-2][personalprereg], [run-path rulings][runpacket] | Successor reuse, personal policy and frozen study boundaries |
| [T00 record][t00], [live-wiring rulings][wiring], [firm_rules][firmrules] | Accepted-risk standing, current sizing migration and public cap source |
| [Route assessment][route], [licensing update][licensing] | Recorded bridge rejection and unresolved data classification |

Private sources were previously read in place under the existing authorization and checked against the public manifest. No private source, settings, quantities, account figures or study output belongs in this PR. The manifest and owning records, rather than copied private provenance, identify later authorized inputs.

### Current decisions preserved

- **Personal reuse:** ADR addendum 2026-10-11b (#784) supersedes the unselected-book statement and strategy split. Personal sizing starts from the retained successor; OFF legs stay OFF unless Joshua explicitly changes them. Personal R1 is separately bound and cleared.
- **Tradeify standing:** #792 records FLOOR-HALF as `NO-GO-evidence-UNDETERMINED-dependent`, VERIFIED, with separate risk acceptance into T15 F1 and the expressly confirmed tension with the preregistration's non-adoption clause. D-feed(a) is met for FLOOR-HALF on accepted risk. Neither the successor verdict nor the original robust NO-GO becomes PASS.
- **Sizing implementation:** #794 and #797 pass an optional `LegSize` through the live sizing and offline emulator seams and refuse leg-identity mismatches. Their `None` path preserves legacy quantities. At the reviewed main, account-owner vector wiring is still owed; these merges do not prove retained-vector operation end-to-end.
- **Personal study:** Q-SFCLEAR-2 is frozen at public commit `83867f0d362931c2a516a62b990bb1c209372527`. Its P0, retained native guards, adds-OFF/zero-refusal fidelity and exposed-history standing remain with its owner. #798 selects port replay for all legs, live-predicate P0 halt behavior, lab-side fee parsing and scoring of post-latch zero days as produced.
- **Cap and ownership:** #800 supplies the public 80-micro personal book safety cap, not a venue maximum; its consumers remain separate work. #802 changes sequencing without transferring owners. #803 permits historical identity interpretation only at specified legacy-record comparisons; a missing live vector is still refused.
- **Private execution exception:** #799's narrow existing VM exception is for its named evidence work. It is not native-prototype or private-transfer authorization.

## §1 — Context and support boundary

**Attributed support clarification:** the coordinating agent independently verified an authenticated Tradeify support reply dated **2026-10-12 20:19 UTC**. For evaluation/sim-funded accounts it requires strategy logic, calculations and signal generation to run inside supported platforms, names NinjaTrader/NinjaScript, and prohibits external Python-generated signals, including Add-On/SDK and direct API routes, without exceptions. This paragraph records the supplied support boundary; it does not reproduce private correspondence or publish mailbox identifiers.

This is stronger than the earlier bridge-rejection record in the [route assessment][route]. Native NinjaScript has been identified as a direction. The reply does not address offline Python research/backtesting or the exact static artifact, supply a governing clause or named compliance approval, settle data rights, or approve this implementation. Specific questions stay with the existing owners; this proposal creates no new blanket permission gate for personal-only deployment.

CME/provider rights for automated use, retention, replay and comparison remain distinct from platform support. Native platform data is not automatically licensed for every proposed use. The [current licensing record][licensing], [CME licensing page][cme] and [non-display guidance][cmefaq] are inputs to the existing licensing work, not an eligibility determination here.

TradingView content/data automation is excluded from the live chain. Any future use of retained reference inputs needs its own applicable authorization.

The [personal ADR][personal] keeps its adopted personal-use reading and first-deployment one-account-at-a-time rule. Before switching either way, the outgoing account must be gross-flat, have no working orders, be disarmed and unable to submit delayed, queued, retrying or scheduled entries. Uncertainty blocks the switch. Preserve opposing-exposure/Product Group and ownership evidence. This native proposal neither pauses nor duplicates the admitted personal work.

## §2 — Candidate architecture and behavioral contract

### 2.1 Genuine separation

```text
Offline Python research / selection / qualification
           |
           | reviewed immutable pre-session configuration
           v
Native startup validation + compiled fixed topology
           |
Platform data -> native leg decisions -> native account risk owner
                                               |
                                  native execution / reconciliation
                                               |
                                    durable state + audit output
```

One native account owner serializes admissions, reservations, dispatch, fills, protection, halt state and reconciliation across the four logical legs. Python prepares a candidate; operator authority binds its exact release/configuration. Account/platform evidence supplies broker truth. Post-session Python analysis cannot feed instructions back into the running session.

No live Python process, embedded interpreter, webhook, socket, REST signal service, named pipe, queue, database command table, desired-position file, dynamic assembly or watched/reloaded configuration is allowed. A once-loaded file of time-keyed signals or future target positions is still a signal channel. The artifact describes algorithms and their qualified inputs, not a trade tape.

Read-only outbound audit/monitoring may be designed and qualified. It cannot become a second trading owner. Native operator controls must share the account serializer and authority checks.

**Proposed changes:** relocating listener authority into C#, replacing daemon-control liveness with an accepted native equivalent, and defining native configuration, execution and evidence producers. These require owner review; removing a Python channel does not discharge its safety obligation.

### 2.2 Aegis dependency map and portfolio extension

Use **Aegis 6J** as the representative accepted strategy. It avoids pyramiding in the first experiment while exercising incremental indicators, time filters, rounding, intent generation and fill-dependent state. Only dependency categories are described.

| Dependency | Reusable as specification/test evidence | Native work owed |
|---|---|---|
| Accepted strategy/settings | Public manifest/loader identity; authorized private behavior inventory | Separately authorized private C# translation; exact effective settings distinct from deployment sizing |
| Completed bars/actions | BookProtocol and bar-validation contract | Explicit platform symbol, dated contract, UTC-open time, session, completeness and OHLCV normalization |
| Arithmetic | Public pine_ta semantics and synthetic edge vectors | Indicator seeds/windows/missing values, order of operations and rounding; no presumed NT-built-in equivalence |
| Stateful feedback | Existing fill/reject/cancel and mode interfaces | Incremental state and paper-equity/guard behavior; existing checkpoints are not presumed restart-complete |
| Sizing | Canonical LegSize and shared entry/add laws | Exact encoding/identity, rational/floor/round order, zero/OFF feedback and per-leg binding |
| Execution model | Existing emulator/replay as an offline oracle | Native order/fill/cost semantics established separately |
| Portfolio safety | Existing capacity and halt/recovery requirements | Native serializer, journal, liveness, account evidence and attended recovery |

The small experiment has no takeover capability and proves none. Preserve the current first-release takeover disposition; later native changes must return to its owner.

Extension to four logical legs adds:
- **Striker:** corrected accepted generation; size-dependent paper-equity, daily/total DD and day soft-stop behavior. P&L rescaling cannot prove another sizing regime's guard behavior.
- **Vanguard:** port quantity map, paper-equity-dependent risk, adds and stop behavior. The personal study records that the rail can admit conditional stop loosening; a blanket native prohibition would be a behavior change.
- **ORB:** resting-entry/cancellation, volume and add lifecycle, including generate-and-refuse feedback where the reference uses it while OFF.
- **Book:** simultaneous decisions, shared reservations, partial fills, protection incidents and calendar boundaries under one serializer.

Four logical legs do not imply four enabled trading legs. Original fixed quantities cannot replace successor sizing; OFF states are never silently re-enabled.

### 2.3 Static artifact concept

| Group | Binding and validation |
|---|---|
| Identity | Closed schema/version, artifact ID, permitted session/expiry, intended instance/environment/account class; no credentials |
| Provenance | Immutable public source/build pins and private dependency digests kept in the authorized private artifact; qualification scope and owner-approved settings/vector |
| Native release | Source/compiler/dependency/binary identities; supported installed NT build; adapter and compiled-topology ID |
| Topology | Ordered series, dated contracts, BarsPeriod/type/value, data type, Trading Hours templates, timezone, tick/point-value definitions |
| Algorithm | Closed typed inputs only; no code, expressions, dynamic plugins, signals or arbitrary executable paths |
| Sizing/policy | All four canonical entries including OFF behavior; instance-specific risk basis, caps, allocations, lifecycle and native-guard identities |
| Data/schedule | Provider/entitlement reference, qualified feed binding, bar-construction rule and calendar/roll digests/coverage |
| Recovery/approval | Journal schema/state anchor; evidence and liveness requirements; independently trusted operator-approved release/config/vector and one-use session authorization |

Canonical UTF-8 bytes, closed keys, no duplicates, finite typed numbers, stable encoding and exact rational fields are proposed. Preserve the existing canonical `size_vector_sha256` domain; do not invent a different formula with the same name. The complete artifact binds its dependencies. Hashes establish integrity, not authority: an expected hash cannot be derived from the untrusted file being checked.

The operator places the artifact before startup. Read/validate once, hold immutable. No missing-size fallback; explicit identity selection differs from absence. #803's historical comparison exception is not a live default.

External runtime changes to parameters, leg states, contracts, sizing, calendars or approvals are forbidden. Native state transitions under the bound rules still occur and are journaled. A file edit cannot affect the session. Reconfiguration requires stop/reconciliation, validation and fresh applicable authority; identity loss/tampering is an incident, not a reload.

### 2.4 Fixed supported topology

Proposed initial portfolio topology: one compiled NinjaScript, BIP 0 = 6J, 1 = MYM, 2 = MGC, 3 = MNQ; each a specified dated contract, M15 Last series and bound session template/timezone. An Aegis-only experiment is a separate topology.

[AddDataSeries][ntadd] restricts configuration to State.Configure and warns against runtime-dependent/dynamic arguments. JSON must not drive arbitrary AddDataSeries calls. Use literal, build-tested declarations, or a separately verified supported mechanism. The artifact asserts the compiled topology; mismatched host chart, period, template or contract refuses startup. A roll needs a reviewed release binding unless a supported alternative is separately established.

[Multi-series documentation][ntmulti] describes historical/realtime ordering and session interactions. Keep an OFF leg in the fixed data/barrier topology for this first proposal. Dropping its source would change the frozen four-symbol domain and needs review; the personal study also keeps the common calendar independent of OFF status. A continuous chart symbol cannot silently replace the dated execution contract.

### 2.5 Sizing, survival and startup

**Retained instances are distinct.** Tradeify FLOOR-HALF keeps its exact successor vector, OFF states, applicable protection/lifecycle/capacity and accepted-risk F1 standing. Personal R1 keeps P0, retained native guards, its adds-OFF choices, ORB OFF and zero-refusal behavior. It does not inherit the Tradeify protection overlay. The legacy identity vector is regression context, never a fallback.

[Shared sizing][policy] uses unscaled risk dollars/per-contract risk and exact multipliers/cap terms before flooring for Striker; the accepted port map for Vanguard; and the appropriate fixed-base/mode/lifecycle laws for the other legs. Adds derive from confirmed base fills; do not haircut the executed base twice. Adds OFF does not authorize relaxing the reference reservation formula.

Count confirmed and reserved/uncertain exposure account-wide in micro-equivalents; enforce allocations/cap before dispatch. Reject excess rather than clipping or substituting minimum-one orders. Zero is a refusal with the required feedback, not an order or automatic incident. Release reservations only on accepted causal evidence. The public personal cap is a book safety source, not proof of affordable margin.

Retain frozen survival/feed rules and exact evidence standing. A Tradeify result does not clear personal capital, and a native trace does not replace Q-SFCLEAR-2's drawdown/growth/margin/drift/guard tests, costs, exposed-history label or chronology. Its ruled P0-latch zero-day treatment and distinct live/scorer predicates remain with the owner. Do not tune criteria after seeing native output.

Every native launch starts HALTED without send authority. Validate release/artifact/vector/policy/calendar/connection identity, complete warm-up and synchronized data. Historical processing cannot send. Reconcile actual account positions, working orders, partial remainders, protection, executions and unresolved previous attempts. [Strategy.Position differs from account position][ntpositions]; startup synchronization itself may order. Qualify a non-submitting boot path, with no automatic adoption/flatten/sync or buffered-intent replay.

Invalid state, unknown orders, unexpected exposure, stale evidence or failed approval keeps HALTED. Modeled warm-up cannot repair real account facts. Persist the boot identity and one-use bounded authority before dispatch; a concurrent halt wins.

### 2.6 Data and event equivalence

The [feed specification][feedspec] is frozen with all eleven parameters bound, despite retained draft language. Preserve existence/timestamp equality, adopted exact tick-precision OHLC incidence, bound MNQ volume handling, delivery/silence/barrier limits and zero revised bars forwarded. The unadopted 0.5% relaxation is not a tolerance available to this proposal. OFF status does not waive the frozen source domain.

Normalize M15 interval-open timestamps from qualified source time; record receipt time separately. Establish open/close stamping and completion behavior. NT OnBarClose may depend on a following tick; do not manufacture a timely completion. [Multi-series][ntmulti], [Calculate][ntcalculate]

Retain delivery at bar-open + 15 minutes + 30 seconds; silence over 30 minutes 30 seconds in required coverage; and the existing bar-period-plus-slack barrier deadline measured from its defined boundary. No incomplete-boundary dispatch or extra discretionary grace period. Identical duplicates are idempotent; conflicting revisions latch unhealthy. No interpolation, fill-forward, silent correction or replay of late bars into live decisions.

Native elapsed-time/watchdog checks must work without ticks. Test monotonic versus wall/session clocks, DST, early close, missing/corrected data, out-of-order/overtaking boundaries and calendar/roll coverage. Buffer required symbols, then preserve the reference decision/action order rather than callback arrival order. The personal margin scorer's conservative entries-before-exits timestamp ties are a separate contract, not the decision dispatcher order.

For deterministic comparison, bind identical authorized input bytes, settings, vector, calendar and explicit feedback. Compare normalized bars, relevant numeric/guard state, eligibility, ordered actions/refusals, quantities, prices, reservations, fills/costs, paper state and halts. Distinguish:
1. Decision parity under the same modeled feedback.
2. Native source normalization/feed equivalence.
3. Native execution/account-safety qualification.

Matching signals establishes only part of the first. [NT fill documentation][ntfills] distinguishes historical, Playback/simulation and live models. OHLC alone cannot prove intrabar sequencing, stop gaps, latency, partial fills or queue position. Retain reference friction where it drives guards and frozen personal fee-only stress in its scorer.

The companion's bit-identical intermediate floating-point rule is a **proposed finite-experiment criterion requiring review before a run**, not an adopted deployment gate. Any broader numeric policy belongs to an explicitly reviewed comparison contract.

### 2.7 Execution and recovery

Managed versus unmanaged execution remains a design choice. [Managed order rules][ntmanaged] may ignore conflicting entry/bracket/exit requests; convenient Set methods do not establish correct protection. Select primitives only after lifecycle evidence.

[Execution callbacks][ntexec] carry partial fills and may be reentrant; [order callbacks][ntorder] can occur before submission returns. Serialize copied event values and stable identities; do not assume a universal callback sequence. A partial base grants only confirmed exposure, retaining remainder reservations. Test bracket creation/replacement, rejected modifies, cancel/fill races, OCO siblings, partial exits, orphan protection and late fills. Preserve accepted first-protection timing rather than silently improving the strategy.

Journal intent before transport and returned/uncertain outcome afterward. Crash cuts retain original identity and uncertainty. Unknown submit/close is not safe to retry. New tags do not establish broker idempotency; no blind resend or remainder close.

Preserve [halt/resume][haltcontract]:
- HALTED is durable permission state, not proof of flatness.
- NORMAL permits qualified running operations; SCHEDULED_EXIT permits only the retained cutoff/closure sequence.
- An incident enters INTERVENTION and fences all new runtime mutations, including cancel/amend/exit/emergency close. Previously sent/uncertain requests remain owned.
- Operator recovery, read-only evidence and notification continue. Feed recovery, restart, day rollover or terminal status does not restore authority.
- During commissioning and first attended release, an incident ends automation for that session.

NT default [StopCancelClose][nterror] and [connection-loss behavior][ntconnection] may conflict with that incident contract. Neither accepting defaults nor disabling them without equivalent detection/evidence resolves the conflict.

**CloseStrategy uncertainty:** its [dedicated page][ntclose] describes all-series handling, while the [multi-instrument guide][ntmulti] says primary-only. Assume neither. Verify the installed build across every series, positions, pending/partially filled entries, protection and cancellation races. A returned call is not account-wide flatness.

All-leg emergency evidence must show account-wide fencing and attended recovery across every controlled/observed location. Under the retained contract that does not mean automatic panic-flatten after INTERVENTION. A different automatic emergency policy is a separate proposed amendment.

Preserve the bound schedule: own-flat D = min(16:00 ET, applicable venue/session close minus 15 minutes), cutoff D minus 15 minutes and flatten start D minus 5 minutes. Calendar holes, deadline breach or incident revoke scheduled authority; no assumed holding extension or post-deadline retry.

Recovery needs fresh coherent evidence covering the last potentially effective runtime, operator and provider request: zero gross positions, no working/protective orphan orders, no unresolved requests and complete locations/history. Net zero, cached reads, elapsed time, exhausted pagination or acknowledgment is insufficient. Reconcile OFF-leg residuals too.

Durable state includes halt generation, invalidated approvals, reservations, operation/order/execution identities, partials, relevant guard/paper state, scheduled actions and reconciliation evidence. Restore halted, retain uncertainty, persist/read back disarm after recovery. Storage failure stops sends; do not claim a durable write or confirmed fence that failed.

Independent monitoring must detect silent process/notifier failure; a local timer cannot detect its own death. Preserve attendance, escalation and notification obligations. Monitoring remains read-only. Even a confirmed local fence cannot retract previously transmitted work.

## §3 — Alternatives and unresolved changes

| Option | Assessment |
|---|---|
| Continue current personal Python work; no native implementation yet | Current operational path; preserves existing owners |
| Small native dependency assessment, then separately granted disconnected experiment | Proposed next evidence, with bounded cost |
| Immediate four-leg execution port | Premature: platform/event/recovery and implementation-specific permission/data questions remain |
| Python decisions through Add-On, socket or changing file | Violates the reported support boundary and genuine separation |
| Four independent chart strategies | Cannot establish one portfolio cap/fence without a separately designed account owner |

Owner review is needed for the native authority/liveness replacement, artifact schema/approval, fixed topology including OFF feeds, native order/error handling and account-evidence producer. Existing survival/feed/incident requirements do not disappear because the API differs.

## §4 — Falsifier and stop conditions

If the design requires external live decisions, cannot preserve applicable accepted data/risk/recovery requirements, or its specific use is disallowed, then reject this native execution alternative or return a concrete amendment to the relevant owner. Do not silently weaken a contract.

If the disconnected experiment disagrees on the frozen decision/state slice, then it fails that comparison; missing coverage or isolation evidence is BLOCKED. Fix translation defects against unchanged expectations or obtain review for a new experiment contract. Synthetic agreement alone never establishes execution feasibility.

## §5 — Forbidden moves

- Restore original quantities, infer private successor values, enable an OFF leg or use absent sizing as identity.
- Rename a live Python bridge or encode future signals in the static artifact.
- Replace the frozen personal study, alter its gates/routes, or displace current implementation owners.
- Treat accepted-risk standing as a passing screen, or synthetic agreement as strategy validation.
- Waive account evidence, fills/costs, all-leg recovery or feed equivalence because native code exists.
- Transfer private source/settings/traces, install platforms, build prototypes or send orders under this documentation proposal.

## §6 — Proposed acceptance matrix

These are review/evidence requirements for this candidate, not newly adopted live gates.

| Evidence | Requirement | Current status |
|---|---|---|
| Source/decision mapping | Current pins, successor/P0/OFF distinctions, preserved owners | Documented |
| Support and data scope | Support boundary recorded; exact artifact/use and applicable entitlements handled by owners | Native direction identified; specific questions remain |
| Capability separation | Prototype has no reachable order path; live design has no Python decision channel | Design only |
| Configuration/topology | Reject invalid identity, vector, account/build, schema, expiry, approval or unsupported series; no reload | Unbuilt |
| Decision/sizing parity | Frozen identical-input comparison including zeros/OFF, guards, clocks and feedback | Not run |
| Feed equivalence | Existing frozen test applied to actual authorized source | Not demonstrated here |
| Order lifecycle | Partials, rejects, races, protection and uncertainty under native primitives | Not run |
| Account truth | Non-submitting boot; manual/external/provider effects and complete recovery evidence | Producer capability unresolved |
| Installed-build emergency | Resolve CloseStrategy uncertainty and verify every leg/location | Not run |
| Durable incidents | No post-fence mutation, retained unknowns, failed storage, silent host and no same-session restart | Not run |
| Release | Applicable owner acceptance, exact configuration/evidence and session authority | Outside this proposal |

## §7 — Evidence stages and effort

1. **Read-only dependency/toolchain assessment:** select the smallest state slice, audited source closure, available toolchains and feasible disconnected boundary. Return blockers and an implementation card; no compilation, test or prototype run.
2. **Separately authorized platform-neutral prototype:** independent Python/C# batch traces on a finite synthetic corpus, with an inert output schema and no execution capability. Private translation/fixtures remain private.
3. **Separately authorized deterministic extension:** exact approved profiles, authorized inputs and full four-leg interactions, preserving OFF states and owner requirements.
4. **Separately authorized installed-NT integration and execution/recovery qualification:** platform callbacks/data normalization first; account/build/route behavior only in specifically permitted drills. These stages have independent acceptance.

Pure decision portability is plausible. Exact execution/reconciliation under the retained incident contract is uncertain. A small assessment should take focused engineering time rather than a campaign run; a useful Aegis translation may take days to a few weeks after its inputs/location are authorized. Four-leg state, platform data and durable execution/recovery are potentially multi-week to multi-month work. These are uncertain planning ranges, not measured estimates. Provider rights or missing evidence capabilities can stop the lane.

## §8 — Questions for the existing coordinator

- Which smallest dependency/state slice and existing isolated toolchains should the assessment name?
- Which exact settings/profile identity and private authoring location would a later prototype use?
- Can native platform error/reconnect behavior preserve the retained incident fence?
- What installed-build/account evidence can prove all-leg recovery, including external effects?
- Can the fixed four-series topology retain OFF-leg feeds, or is an explicit amendment needed?
- Which owners will accept later native implementation evidence while current personal work continues?

## §10 — Document verification and publication boundary

Only documentation preparation, scoped publication checks and draft PR publication are authorized by the current request. A draft is not acceptance. No prototype, market-data collection or execution evidence is claimed.

Relevant repository-local document checks:

```powershell
.\fp.ps1 doctor
.\fp.ps1 python scripts/check_brief.py docs/notes/2026-10-12-native-ninjatrader-runtime-PROPOSAL.md --type brief
git diff --check
```

The normal staged pre-commit/pre-push hooks and required PR checks remain in force. Record their actual results in the PR. Review both documents for local paths, correspondence identifiers, private source/settings locations, quantities, account data and strategy-revealing traces before publication. This artifact contains only prose and source references.

[agents]: https://github.com/Joshua-Asante/first-passage/blob/0a0c2a86e4d2e7a07e4b9adede7fea739406b5d1/AGENTS.md
[rule0]: https://github.com/Joshua-Asante/first-passage/blob/0a0c2a86e4d2e7a07e4b9adede7fea739406b5d1/docs/rule_0.md
[policy]: https://github.com/Joshua-Asante/first-passage/blob/0a0c2a86e4d2e7a07e4b9adede7fea739406b5d1/ops/c1_rail/book_policy.py
[sizing]: https://github.com/Joshua-Asante/first-passage/blob/0a0c2a86e4d2e7a07e4b9adede7fea739406b5d1/ops/c1_rail/book_sizing_context.py
[bundle]: https://github.com/Joshua-Asante/first-passage/blob/0a0c2a86e4d2e7a07e4b9adede7fea739406b5d1/ops/c1_signal_daemon/book_bundle_execution.py
[accountowner]: https://github.com/Joshua-Asante/first-passage/blob/0a0c2a86e4d2e7a07e4b9adede7fea739406b5d1/ops/c1_rail/book_account_owner.py
[protocol]: https://github.com/Joshua-Asante/first-passage/blob/0a0c2a86e4d2e7a07e4b9adede7fea739406b5d1/ops/c1_signal_daemon/book_protocol.py
[ta]: https://github.com/Joshua-Asante/first-passage/blob/0a0c2a86e4d2e7a07e4b9adede7fea739406b5d1/ops/c1_signal_daemon/pine_ta.py
[adapters]: https://github.com/Joshua-Asante/first-passage/blob/0a0c2a86e4d2e7a07e4b9adede7fea739406b5d1/ops/c1_signal_daemon/book_adapters.py
[manifest]: https://github.com/Joshua-Asante/first-passage/blob/0a0c2a86e4d2e7a07e4b9adede7fea739406b5d1/core/strategies/BOOK_SOURCES.sha256
[replayspec]: https://github.com/Joshua-Asante/first-passage/blob/0a0c2a86e4d2e7a07e4b9adede7fea739406b5d1/docs/spec/2026-09-12-tradeify-synchronized-replay-spec.md
[emulator]: https://github.com/Joshua-Asante/first-passage/blob/0a0c2a86e4d2e7a07e4b9adede7fea739406b5d1/ops/c1_signal_daemon/tv_broker_emulator.py
[riskcontract]: https://github.com/Joshua-Asante/first-passage/blob/0a0c2a86e4d2e7a07e4b9adede7fea739406b5d1/docs/spec/2026-09-12-tradeify-book-protection-capacity-spec.md
[haltcontract]: https://github.com/Joshua-Asante/first-passage/blob/0a0c2a86e4d2e7a07e4b9adede7fea739406b5d1/docs/spec/2026-09-14-tb-s3-halt-resume-contract.md
[feedspec]: https://github.com/Joshua-Asante/first-passage/blob/0a0c2a86e4d2e7a07e4b9adede7fea739406b5d1/docs/spec/2026-09-27-cme-execution-feed-equivalence-test-DRAFT.md
[personal]: https://github.com/Joshua-Asante/first-passage/blob/0a0c2a86e4d2e7a07e4b9adede7fea739406b5d1/docs/adr/2026-10-09-self-funded-tradovate-lane-reopen.md
[personalprereg]: https://github.com/Joshua-Asante/first-passage/blob/0a0c2a86e4d2e7a07e4b9adede7fea739406b5d1/docs/briefs/pre-registration/Q-SFCLEAR-2-verdict-preregistration.md
[runpacket]: https://github.com/Joshua-Asante/first-passage/blob/0a0c2a86e4d2e7a07e4b9adede7fea739406b5d1/docs/notes/2026-10-12-q-sfclear-2-run-path-decision-packet.md
[t00]: https://github.com/Joshua-Asante/first-passage/blob/0a0c2a86e4d2e7a07e4b9adede7fea739406b5d1/docs/briefs/handoffs/2026-10-03-t00-screen-authority-build-card-DRAFT.md
[wiring]: https://github.com/Joshua-Asante/first-passage/blob/0a0c2a86e4d2e7a07e4b9adede7fea739406b5d1/docs/notes/2026-10-11-live-wiring-decision-packet.md
[firmrules]: https://github.com/Joshua-Asante/first-passage/blob/0a0c2a86e4d2e7a07e4b9adede7fea739406b5d1/core/firm_rules.py
[route]: https://github.com/Joshua-Asante/first-passage/blob/0a0c2a86e4d2e7a07e4b9adede7fea739406b5d1/docs/briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md
[licensing]: https://github.com/Joshua-Asante/first-passage/blob/0a0c2a86e4d2e7a07e4b9adede7fea739406b5d1/docs/notes/2026-10-10-cme-non-display-licensing-research.md
[ntadd]: https://static.ninjatrader.com/support/helpGuides/nt8/adddataseries.htm
[ntmulti]: https://static.ninjatrader.com/support/helpGuides/nt8/multi-time_frame__instruments.htm
[ntmanaged]: https://static.ninjatrader.com/support/helpGuides/nt8/managed_approach.htm
[ntpositions]: https://static.ninjatrader.com/support/helpGuides/nt8/strategy_position_vs_account_p.htm
[ntclose]: https://static.ninjatrader.com/support/helpGuides/nt8/closestrategy.htm
[ntexec]: https://static.ninjatrader.com/support/helpGuides/nt8/onexecutionupdate.htm
[ntorder]: https://static.ninjatrader.com/support/helpGuides/nt8/onorderupdate.htm
[nterror]: https://static.ninjatrader.com/support/helpGuides/nt8/realtimeerrorhandling.htm
[ntconnection]: https://static.ninjatrader.com/support/helpGuides/nt8/connectionlosshandling.htm
[ntfills]: https://static.ninjatrader.com/support/helpGuides/nt8/discrepancies_real-time_vs_bac.htm
[ntcalculate]: https://static.ninjatrader.com/support/helpGuides/nt8/calculate.htm
[cme]: https://www.cmegroup.com/market-data/license-data.html
[cmefaq]: https://www.cmegroup.com/market-data/distributor/files/cme-group-data-licensing-policy-guidelines-and-non-display-licensing-faq.pdf
