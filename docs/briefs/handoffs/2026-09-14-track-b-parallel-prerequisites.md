# Track B parallel prerequisites — reconciled ledger

Status: **E/P/U APPROVED; APPROVAL-RECORD PUBLICATION PENDING.** Updated 2026-09-14 UTC.
Stage 1 is closed at the bounded engineering/contract level. Remaining evidence
and Stage 2 implementation are not complete.

This task owns prerequisite evidence, intake/parity and specification proposals.
The runtime task **Complete TB-I1 acceptance** owns Stage 2 runtime, replay,
calendar, snapshots, recovery/resume and integration tests. Joshua owns merges
and operational approvals. No owning ADR addendum is copied or edited here.

## Verified revisions and publication

Branch `codex/tb-parallel-prereqs` was fast-forwarded from #379 to verified
`origin/main` at `c1dcb31730157c2895c258c9921b8d8164557335`, preserving this
uncommitted packet. GitHub fresh reads establish:

| PR | Verified merge revision | Merged UTC | Scope |
|---|---|---|---|
| [#379](https://github.com/Joshua-Asante/first-passage/pull/379) | `d53a06e3fa6018c6c36eb63771e5ad6d1ae961cf` | 2026-09-14 01:50:01 | TB-I1 foundations/fingerprints |
| [#380](https://github.com/Joshua-Asante/first-passage/pull/380) | `8101ba498aad812e79c3d80c45f963cd67b55de6` | 2026-09-14 02:20:27 | S3 rev8 design |
| [#381](https://github.com/Joshua-Asante/first-passage/pull/381) | `c1dcb31730157c2895c258c9921b8d8164557335` | 2026-09-14 02:58:41 | Persistent halt-only implementation |

The runtime task's local approval record was read at
`C:/Users/joshu/multi_firm_operations/.worktrees/tb-i1-fingerprints/docs/briefs/handoffs/2026-09-14-track-b-ratifications.md`.
SHA-256 of its observed working bytes:
`26a24db6faca10cf15d27887fb5e713ba339a36889a9f7708fdfc7d2e7c19adb`.
Its revised parallel packet beside it was also read. Both are untracked on
`codex/tb-ratifications`; S2b/P2 addenda and associated status edits are modified
but uncommitted. **None of those records/addenda is published by #381.**
The runtime owner publishes the single owning record; this ledger is a derived
status report. Replace the local reference with its published commit when available.
Joshua's explicit approval is received, regardless of this publication debt.

Approved content pins from that record: S3 rev8 blob
`190b7aa8879cb6f8f6e49d5841b3f8aa45cd41db`; halt/resume blob
`d619b00ed57ce99f209f175fc44aceafde4ccb78`; P2 rev9 blob
`f94be43e25a9f4e4c0b10ccf3bb115f41aded3ec`, all present at #380.
The owner's bounded TB-I1 acceptance binds #379 and its retained engineering
evidence. This task does not re-perform or independently broaden that acceptance.

Rule 0 production check: read [book_halt.py](../../../ops/c1_rail/book_halt.py)
and the typed session/settlement consumer at #381. The store accepts HALTED only,
retains incidents and rejects RUNNING. It does not dispatch broker recovery,
resume trading, execute schedules or attest flatness. Earlier source-read evidence
for unchanged book quantities remains historical evidence; no quantity law changes here.

## Prerequisite ledger

| Item | Governing revision | Evidence/digest | Status | Missing input | Owner | Blocked consumer |
|---|---|---|---|---|---|---|
| Bounded TB-I1 | #379 + approved #380 authority | Runtime acceptance record digest above | Accepted; Stage 1 closed | Publication of owning acceptance record | Runtime owner | No remaining E/P approval request for Stage 1 |
| E execution | S3 rev8 / halt-resume contract at #380 | Joshua explicit approval; owning record above | Approved; publication pending | Publish existing dated S2b addendum | Runtime owner records; Joshua merges | Published governance trace; dependent runtime evidence remains owed |
| P first ratification | P2 rev9 §7 | Same approval record; existing local first addendum | Approved; publication pending | Publish owning addendum | Runtime owner; Joshua merges | Published policy trace; TB-F1 retains other gates |
| U schedule | Rev8 §5 | Approved formula below | Approved | Per-session V, coverage/closures/DST, settlement producer and measured route timing | This task evidences; calendar/runtime owner implements | Calendar/replay integration; TB-F1; live schedule |
| Stage 2 halt | #381 | Fresh merge read; production HALTED-only store | Merged, bounded | Broker recovery, operator resume, schedule and snapshot integration | Runtime owner | Stage 2 combined acceptance |
| Seven bundles | Appendix parallel evidence track / scaling note §3 | Collection v2 and intake diagnostic digests below | 7/7 collected; integrity/schema/structural diagnostics PASS; 0/7 accepted | Chart body/export-state identity, admitted normalization, coverage/warmup, independent summary joins | Prerequisite task; runtime supplies admission tooling | TB-R3; parity; decision-bearing replay; TB-F1 |
| Corrected parity | S1 §2; S3 retained sizing/feedback | Existing book_parity entry points; #381 adds no parity runner | Not run / blocked on inputs and tooling | Intake identities, complete risk-input admission and confirmed feedback, seven-bundle runner | Runtime supplies tooling; this task verifies | All required parity PASS |
| Exact Part A | P2 second ratification | No frozen F1 depth/budget | Deferred, not due | Actual positive depth, deterministic measured budget, frozen digests | F1/runtime owner then Joshua | TB-E1 |
| M1 A7/A8 | Track A plan / M1 acceptance artifact | Prior CODE_LANDED record; no new ceremony evidence supplied | Evidence pending | Fresh attended ceremony or its completed evidence; A8 signoff/rebake | Joshua / Track A owner | M1 RESOLVED in deployed image; later live gates |
| Feed / TB-I5 | A9, O-4, TB-I5 | Provider deferred; no successor PASS evidence supplied | Gated | Six vendor facts, source ruling, approved adapter and frozen equivalence test/application | Joshua; source/runtime owner | Live integration |
| L1/L2, four symbols | S3 retained R-M/R-B3/R-B2 | Historical M1 chain only; no complete route packet | Unknown for full required behavior | Actual route evidence and current symbol mappings | This task inventories; Joshua attends; runtime integrates | Recovery/resume and live qualification |
| TB-I4 | Dedupe prereg §6 | M1 unresolved in last record; venue dedupe historically disproven | Gated | M1, separate GO, fresh disarmed host read and current-book key falsifier | Runtime owner / Joshua | Live integration |

## Approved execution and schedule

**E:** one durable account-wide halt, listener-owned qualified recovery and a
fresh bounded operator approval after reconciliation. Feed recovery, session
rollover and restart never grant trading permission. HALTED is not flat.
The old automatic session-clear and daemon-emitted feed-loss flat are withdrawn.
The revised S2b addendum is owned by the runtime approval branch.

**P:** first P2 rev9 decision is approved, including its fixed-policy qualification,
fingerprints, GO reseal and activation contract. Invalidation stops for Joshua;
no automatic replacement sample. The exact-depth supersession requires the
second approval after F1; no depth approval is requested now.

**U:** [rev8 §5](../../spec/2026-09-14-tb-s3-halt-resume-contract.md) owns the
single formula. In America/New_York, V is the earliest applicable source-backed
venue/symbol flat deadline. D = min(16:00, V − 15 minutes).

| Event | Formula | Covered regular session | Verified V=12:59 row |
|---|---|---|---|
| Risk-add cutoff; halt and cancel resting risk-adds | D − 15 minutes | 15:45 | 12:29 |
| Mandatory whole-book flatten start / evidence check | D − 5 minutes | 15:55 | 12:39 |
| Own-flat deadline | D | 16:00 | 12:44 |

16:30 is reconciliation/reporting only. Existing positions retain qualified
protection between scheduled cutoff and flatten start; an incident in that
interval starts immediate recovery. Earlier authorization expiry follows rev8's
immediate recovery rule. At/after D, exposure or unconfirmed state is a breach,
with retained halt and attended alert. A close request at flatten start is not
proof of completion by D. Measured insufficient recovery time returns a specific
conflict for coordinated amendment; it does not silently widen this schedule.
The earlier competing time tables and amendment drafts have been removed.

## Calendar, closure, DST and settlement evidence

Fresh primary reads on 2026-09-14 UTC support the facts below; they are source
observations, not an accepted complete calendar artifact.

| Evidence | Established fact | Remaining obligation |
|---|---|---|
| [Tradeify permitted times](https://help.tradeify.co/en/articles/10495876-rules-permitted-times-to-trade) | Dedicated rule: regular 16:45 ET, holiday-short 12:59 ET; ET follows EST/EDT | Dated holiday notices for the selected account/session; earlier symbol deadline still wins |
| [CME hours](https://www.cmegroup.com/trading-hours.html) | Hours are Central unless stated; product schedules, holiday notices and settlement are distinct; hours remain subject to change | Capture exact dated 6J/MGC/MYM/MNQ rows across the frozen horizon; the page's dynamic date link returned the same page, not the complete product table |
| [NIST DST](https://www.nist.gov/pml/time-and-frequency-division/popular-links/daylight-saving-time-dst) | 2026 transitions: March 8 and November 1 at 02:00 local; spring gap and fall repeated hour | Calendar owner pins timezone data/runtime and verifies conversions, source CT→ET→UTC, fold/gap rejection and session-date mapping |
| [D19 provenance](../../../ops/calendars/README.md) | Existing acceptance is secondary date membership over its declared window only | Preserve frozen bytes; provide distinct forward coverage/typed closure evidence and resolve source residuals |
| Tradeify permitted-times account-posting note | Rithmic holiday trading-day credit may appear at next full close | Actual account/route-specific settled-balance and history evidence; do not infer Rithmic use or equate credit posting with policy settlement |

The previous [common FAQ](https://help.tradeify.co/en/articles/12268494-common-faqs)
observation said 16:59 EST, conflicting with the dedicated rule. It provides no
basis to loosen approved U. Obtain account-specific clarification before affected
live use; missing/contradictory applicable deadline evidence remains blocking.

Calendar evidence request to its producer: return the intended historical and
forward coverage bounds and dated source records for all four symbols. Each record
must distinguish venue deadline, product last matching time, session open/close,
trade date, wall-clock date, source timezone/UTC offset, publication/as-of/expiry,
closure disposition and source URL/artifact digest. Compute V only after every
applicable row is verified. Explicitly cover full closures, sub-deadline overlay
dates (2023-04-07, 2025-01-09, 2026-04-03), evening reopen, ad-hoc halts and coverage
expiry. A market-closed label on a trade date does not by itself suppress its
next-session evening reopen. This task has not established complete coverage.

Settlement evidence request: identify the actual producer of the prior-session
settled account equity, full adjustment/fee history, historical EOD peak and seal.
Keep product settlement quote/time, market close, account posting and own-flat
completion separate. The typed consumer requires the sealed prior-session record
before the current session opens; missing/delayed evidence blocks progression.
Provide regular and holiday examples with acquisition time and immutable identity,
privately. No assumed 17:00 timestamp or last strategy bar can manufacture settlement.

Route timing request: provide measured cancellation/reconciliation/qualified
whole-book close and evidence-acquisition timing on the actual route, including
late fills, partial/unknown outcomes and restart. Demonstrate closure by D from
D−5 and cancellation from D−15. If that cannot be evidenced, return the exact
limiting case to the runtime owner for a coordinated amendment.

## Seven-bundle intake and parity

Inventory scope: approved primary roots only. The earlier missing-input inventory
is superseded by collection v2 and the resumed audit below. All seven exports and
their captured evidence are present; no seven-bundle acceptance manifest exists.
This remains **0/7 accepted**. No recollection is requested merely to resume work.

Primary paths: `C:/Users/joshu/multi_firm_operations/core/data/tv_exports/cme/`
for CSVs, and
`C:/Users/joshu/multi_firm_operations/lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/inputs/private_overrides/op1/`
for captures. `git check-ignore -v` confirms CSV exclusion by root `.gitignore:87`
and captures by the study `.gitignore:3`. Recheck each actual destination before
copying; the CSV directory itself need not be ignored for its CSV files to be ignored.

| Bundle | Only specified change from captured state | Intake | Parity |
|---|---|---|---|
| S-P | Striker Account Size × 0.40 | Collected; acceptance blocked | Not run |
| S-W1 | Striker Account Size × 0.50 | Collected; acceptance blocked | Not run |
| S-W1P | Striker Account Size × 0.20 | Collected; acceptance blocked | Not run |
| S-W2 | Striker Account Size × 0.25 | Collected; acceptance blocked | Not run |
| S-W2P | Striker Account Size × 0.10 | Collected; acceptance blocked | Not run |
| O-N | ORB contracts 1; authorized finite-margin substitute; scale-in on | Collected; amendment/binding owed | Not run |
| O-P | ORB contracts 1; authorized finite-margin substitute; scale-in off | Collected; amendment/binding owed | Not run |

For each, the collection supplies List of trades CSV plus Inputs and Properties
captures; binding them to the exact export state remains owed. Retain the pinned body, continuous symbol,
15-minute timeframe, Deep Backtesting **Sep 1, 2022 through Sep 2, 2026**,
100K USD chart initial capital, Default detalization, Script execution **2 for
Striker / 1 for ORB**, and every other captured input/commission/slippage
(campaign §47a/§47b and §18a; the scaling note's §47(e) shorthand is imprecise).
The Striker Account Size input change is distinct from chart initial capital.
Do not guess missing settings or multiply a rounded
trade quantity. Joshua reports O-9: original charts recaptured if available,
otherwise the already permitted RECONSTRUCTED branch. This is not restoration
of lost original overrides. The finite menu is unchanged.

Intake sequence: verify ignored destinations; SHA-256 body/CSV/captures and new
override record; bind export id to exact body and settings; run existing schema,
normalization and phase-1 reconciliation machinery into separate private outputs;
prove entry/exit pairing, side, timezone, fees, totals, coverage and warm-up;
publish only permitted digest/verdict records. Never edit the frozen phase-1
manifest or bypass its missing-original-override refusal. Differences return a
specific blocker before parity.

Existing `book_parity.parity_for` chooses the original export from phase1_config;
`run_leg` accepts overrides, mode and a normal-quantity callback. The Striker
callback cannot supply law B's complete risk/stop/allocation evidence, and the
current test deliberately rejects normal-integer-only protected parity. The
generic comparator can be reused after intake; `qty_scale` alone cannot establish
size-dependent halt behavior. Runtime owner must supply the corrected admission
and execution-feedback integration and seven-bundle runner/identity binding.
This task owns verification of that tooling, not another replay engine.

Acceptance requires all five Striker modes with their size-dependent paper P&L
and halt feedback, the ORB one-contract normal and adds-off paths (including
native exit changes and no protected stall exit), and retained Aegis timing/
quantity invariance and Vanguard zero-state obligations. Cover every required
reachable lifecycle/mode and quantity boundary; samples alone do not prove
reachability. All seven intake verdicts and every required parity check must PASS.

## Actual evidence requests and attended checklist

M1 observed in the repository: `CODE_LANDED`, absent
`dry_run_strategy_signal_event_id`, null `operator_signoff`. Historical SIM
`CHAIN_OK` event `7f80b4be-4b90-4097-bd3b-c927bc3200a5` and notification ack
`6ceffdec-c4b4-4bae-bd97-875020534a3b` are recorded. They do not establish
current deployment identity or the portfolio's L1/L2 guarantees. No host state
was read during this preparation task.

| Evidence request | Attended requirements / acceptance boundary |
|---|---|
| A7 ceremony under current Track A procedure | Refresh dated window and deployed identities; preflight expected quantity one, broker flatness and listener disarmed; Joshua enables and injects the just-closed dated-contract bar inside target+60s to target+120s; require one unique listener triad with qty_out=1, dry_run/test_only true, sender_invoked false and transport not_attempted; close and verify daemon inert/listener disarmed. An agent injection invalidates it. |
| A8 | Genuine A7 UUID and evidence join; Joshua name/date/statement; validator success; merge/redeploy and in-container pins under existing procedure, including any required re-bake. Only deployed RESOLVED closes M1; do not refresh deployment pins from this worktree. |
| A9/source approval | Obtain the existing six written facts: licensed headless algorithmic use; all-in cost/capital; enforceable data-only permissions; completed-bar/backfill/correction semantics; unattended token renewal/session limits; cloud/persistence rights. Confirm CME+CBOT+COMEX entitlements for 6J/MNQ, MYM, MGC. Keep questions prepared; no vendor message sent here. |
| A9 funding checkpoint | Source-independent qualification survives; provider-neutral build readiness; primary eligibility/terms; all entitlements; credential containment; immediate-use window. Joshua then selects/authorizes; shortlist is not approval. |
| TB-I5 | Frozen CME successor with aggregation, sessions/timezone, roll handling, bar-close timing, overlap, tolerances and binary verdict before observing provider comparison data; actual delivered source/config identities and per-symbol results. Existing locked XAUUSD/Pepperstone scope is inapplicable. |
| L1 | Actual coherent position/gross-lot/working-order/terminal-order acquisition, immutable complete executions, global symbol locations and ordered all-account request fence; freshness and causal order after prepare/latest dispatch; restart/history/reorder evidence. Dashboard net zero or an event-only overlay is insufficient. |
| L2(a)/(b) | Resting stop-entry and per-order entry brackets, verified on the actual route; identify supported order types and linkage. |
| L2(c) | Atomic native modify, retained old protection until effective, rejection/unknown outcome evidence. Cancel/replace cannot satisfy it. |
| L2(d)/(e) | Scoped and quantity-less close, attached-order removal, every partial fill's residual protection and no reversal; prove protection-owner/FIFO distinctions and surviving siblings. Concurrent cancel/close cannot satisfy it. |
| L2(f) | Attach protection to an existing bare fill with subsequent atomic close/partial guarantees. A standalone stop is insufficient. |
| L2(g) | Native activation/offset trail, OCO fixed siblings, retained anchor under fixed-component modification; explicit evidence of trailing-parameter modification behavior. No daemon-emulated extreme substitution. |
| Four symbol bindings | Per-route current ticket/dated contract evidence for 6J sell entry, MGC buy, MYM buy, MNQ buy; tick/point conventions and mapping/roll validity. Operator ticket attestation or separately authorized transmitted validation; a dry-run receipt does not verify a symbol. |
| TB-I4 | M1 RESOLVED, separate D-B13 GO and fresh host dry_run=true before implementation. Recheck collision-free legitimate traffic for the current four adapters; the historical two-leg minBars citation is not current-book proof. Preserve the frozen planted-defect/refusal tests and operation-id ownership for reductions. |

Evidence classification: historical market/SIM chain and notification are observed
only within their recorded scope. CrossTrade `order_id` deduplication is recorded
as **disproven**. Full L1 and L2(a)–(g) are **unknown here** until a route-specific
evidence record meets each contract; unknown does not mean vendor unsupported.
Models and endpoint names establish no actual route capability. Record unsupported
only from affirmative evidence, with the route/version and affected legs.

## Next actionable requests and runtime handoff

For Joshua:

1. Seven bundles are supplied. Resolve only the remaining chart-body/export-state
   provenance gap under O-9; names and settings do not prove script bytes.
   No approval of E/P/U or repeat collection is requested.
2. Supply dated Tradeify holiday/account notices and any broker deadline or
   settlement records already available, identifying the applicable account route.
   Keep account values and raw records private.
3. Supply existing A7/A8 evidence if the ceremony has since occurred; otherwise
   identify an attended window for the existing procedure. Scheduling a window
   does not substitute for its preflight or operator-only enable/inject.
4. Supply existing actual-route capability/symbol evidence. New transmitted
   validation remains separately gated; no test order is authorized here.
5. Review/merge the owning ratification publication when the runtime owner
   prepares it. This is publication of received approvals, not a new ratification.

Concrete dependencies returned to the runtime owner in this ledger:

- Publish the existing approval/acceptance record and owning ADR addenda once.
  The merged Stage 2 plan's pending-authority text is historical and must be
  reconciled by that publication; do not reopen Stage 1.
- Supply the calendar coverage horizon, source-row artifact interface and actual
  settlement producer. This task supplies evidence; calendar/snapshot code stays there.
- Supply reusable seven-bundle identity/intake and corrected-law feedback tooling.
  No replay engine is created here; all required exports/intake precede parity.
- Keep #381's HALTED-only result separate from recovery/resume/schedule acceptance.
  Full L1/L2, bounded operator authentication and causal recovery remain owed.
- Reconcile the existing TB-I5 neutral-authoring entry discrepancy (O-4 summary
  versus detailed M1-RESOLVED prerequisite) before freezing the successor.
- Recheck dedupe's current four-leg legitimate-key falsifier at its existing gate.

No qualification, registry admission, binding, final n3, deployment GO or initial
arm is initiated. Approved decisions stay approved; only a specific new conflict
can warrant returning to Joshua.

## Verification

### Native export collection update — 2026-09-14

Joshua confirmed that the supplied Striker chart's contract-cap override was
intentional and authorized collection from that effective chart configuration.
Code defaults must not replace this operator-confirmed override. Reconciliation
against the earlier reconstructed override record remains an intake obligation;
this does not rewrite the frozen capture manifest or establish source identity.

Seven native List of trades CSVs were downloaded through Chrome into the approved
primary ignored CSV root, with Inputs/Properties captures in the approved private
override root. Ignore rules were checked before copying. The in-app browser
reported CSV generation but did not deliver an observable downloaded file.

| Item | Evidence SHA-256 | Status | Missing input / owner | Blocked consumer |
|---|---|---|---|---|
| S-P | `0373f211f5e44fe89976d7bcea2b7252724dc717541116dccb59932dfabc710a` | COLLECTED; not accepted | Source/override reconciliation and intake / prerequisite task | TB-R3 parity |
| S-W1 | `1996a88569828fa7790306320709c0c0b9eab0586ead5dec03b5acb6435a4add` | COLLECTED; not accepted | Same | TB-R3 parity |
| S-W1P | `ce5e5c879942c3b339220c43b8f66a27d8e1b89389ae95e5b3f1d54c7b8ec9ff` | COLLECTED; not accepted | Same | TB-R3 parity |
| S-W2 | `8c18f1d82f2b82a804973dbc5b77ab1347c48f8328445509a9f82424bf3870aa` | COLLECTED; not accepted | Same | TB-R3 parity |
| S-W2P | `d2077b1c4bdcad2a17f84eab62ecb24a518b16b2aca185e5409f0191896fb09e` | COLLECTED; not accepted | Same | TB-R3 parity |
| O-N | `7e23e2e438af8780fa167f98ce75c72a53dc978dd8120ea8127d6a462325ce2d` | COLLECTED with operator-authorized finite-leverage substitute; not accepted | Source/override reconciliation, finite-margin model binding and intake / prerequisite + runtime tasks | TB-R3 parity |
| O-P | `2cb58fb6b0ec81f5859db527821a1701675ba6305553369d9096d5ee2bd93e40` | COLLECTED with same substitute; not accepted | Same | TB-R3 parity |

The current ORB UI labels the fields Long/Short leverage. It rejected an infinite
value; entering zero displayed zero leverage and yielded no trades. This is not
evidence of the required zero-margin contract. Both fields were restored to their
observed original values before the operator's subsequent ruling. Joshua then
explicitly authorized a reasonably high finite value as the substitute. The agent
selected and disclosed the value before action; the private manifest records the
exact long/short settings and effective nonzero margin. O-N/O-P were collected
under that revised instruction, with one contract and adds on/off respectively.
This resolves the collection blocker, not equivalence to the original zero-margin
requirement. Intake and replay must bind the actual margin setting. No owning ADR
addendum or runtime code was changed here.

Striker Account Size was restored to its observed baseline in both browsers.
ORB was returned to adds-on with the newly authorized finite leverage after O-P.

Private collection manifest v2 SHA-256:
`da7157517032b76179bd3c07850c5779f968298261db6b75bd0c3c1dca383adb`.
It supersedes the retained five-file manifest
`f9a0f81ad6aacb317d952a3b33aec3bb6c69157c6fab27b1ad27829042fb17cf`.
It binds file and screenshot digests and records the effective overrides.
Collection is **7/7; acceptance remains 0/7; parity has not run**.

This update is documentation only over #381. Governing addenda and the runtime
task's working files remain untouched. Production store/consumer inspection
supports the bounded capability statements; no runtime suite or private parity
result is claimed. Link and stale-proposal checks are run on this updated file.

### Resumed intake audit — 2026-09-14

Fresh `git ls-remote origin refs/heads/main` returned
`c1dcb31730157c2895c258c9921b8d8164557335`, equal to this worktree HEAD and
cached origin/main. Primary local main remains at `133f043`; it was not moved.
The runtime ratification working-file digest above still matches. Its addenda
remain uncommitted on the owning branch; no publication is inferred.

The private `intake-audit.py` uses the existing ledger's strict header, integer,
timestamp and unambiguous-localization helpers. It performs read-only diagnostics
without constructing a falsely admitted `VerifiedSource` or invoking the frozen
campaign publisher. Bundled Python executed successfully. Private report
`op1/2026-09-14-seven/intake-audit-v1.json` SHA-256:
`ffcf0ad93d72d8bdada1572b52881105368a4ac9d8a5bfea82b1dbb88d2c8f1c`.
The report also binds the diagnostic script digest. Both new files were verified
ignored in the primary evidence root; raw evidence and manifests were unchanged.

| Check | Verdict | Limit / next owner |
|---|---|---|
| Collection v2 digest; seven CSV digests and byte lengths | PASS | Integrity of supplied bytes only |
| All 50 manifest-listed PNG/text evidence digests | PASS | Presence is not full visual coverage or export-state identity |
| All seven CSV schemas; sequential trade identities; exactly one entry/exit; long side; positive integral matched quantity; entry-before-exit | PASS, diagnostic | Full admitted normalization still blocked on identity |
| Finite numeric cells; price/quantity/fee/net identity; captured commission; final cumulative net | PASS, diagnostic | Final cumulative uses exit-time/source-row order, consistent with existing accounting; independent TV summary reconciliation remains owed |
| Trade times within declared deep window; unambiguous ET localization | PASS, conditional | ET is a supplied assumption here, not proven chart display-clock identity; trades do not establish complete panel coverage or warmup |
| Source/body and effective override identity | BLOCKED | Manifest has no chart-body digest and no complete exact export-state join; prerequisite/runtime owners |
| Seven-bundle normalization and parity | NOT RUN | No admitted seven-bundle source inventory or corrected-law runner |

Visual spot checks covered S-P Chrome Inputs, S-W1 Properties and O-P margin
Properties. S-P's top Inputs viewport does not show its lower sizing controls;
the accessibility text contains them. This is incomplete visual coverage, not
a contradiction of the operator-confirmed override. Some settings text records
contain `The report is outdated`; later report evidence must be joined explicitly.
The O-N files marked `restored` remain post-O-P observations. No current chart
body or complete independent summary is supplied by any of these facts.

The first diagnostic incorrectly compared intermediate cumulative totals in
trade-number order. Inspection of existing `trade_reconciliation` showed the
final-total check uses exit time and source-row order; the corrected diagnostic
passes all seven. No CSV changed. This diagnostic repair grants no admission.

Runtime coordination was sent to **Complete TB-I1 acceptance** with the private
report location/digest and exact private override differences. Requested contract:
new bundle identity must bind CSV, body, settings, mode, chart clock, deep interval,
execution settings, panels/warmup and tool revisions; altered bytes must refuse.
Preserve historical phase1 config and effective-input pins. Bind Striker's actual
chart cap and scaled Account Size before floor/cap and confirmed-fill halt
feedback; account-wide capacity is a separate unchanged control. Bind ORB's
actual finite margin and adds setting; current zero-margin tests do not verify it.
The emulator explicitly omits margin calls, so finite-margin acceptance needs
supported semantics or evidence that the omitted behavior is unreachable under
the frozen criteria. No shared specification was edited before coordination.

Calendar preparation: fresh [CME schedule](https://www.cmegroup.com/trading-hours.html)
read confirms that holiday hours are generally finalized about two weeks before
the holiday and remain subject to change. A forward row therefore needs an as-of,
expiry and refresh disposition, not merely a calendar-year label. Its 2026 Labor
Day note also distinguishes Sunday order entry from Tuesday trade date and order
expiry. This is a concrete session-date/order-lifetime evidence case, not a
four-product deadline acceptance. The requested producer packet must provide
coverage bounds, four-product dated rows and settled-account producer identity.
The existing M1 A7/A8, A9, TB-I5, L1/L2, symbol and TB-I4 requests above remain
prepared under their gates; no actual route evidence was newly supplied.

Current exit position: collection 7/7, diagnostic structural checks 7/7 PASS,
accepted bundles 0/7, parity not run. Dependency requests are with the runtime
owner. No qualification or operational gate has been entered.
