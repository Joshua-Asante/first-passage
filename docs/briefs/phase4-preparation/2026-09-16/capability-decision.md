# Bounded account and route capability decision

Assessment ID: **CAP-20260916**. Inspected September 16, 2026 ET / September 17 UTC.
Disposition: **BLOCKED FOR LIVE RELEASE**. The execution update below supersedes
the initial-pass findings where stated. R1 is qualified only as a local engineering
property; actual settlement and route qualification remain incomplete. The
coordinating agent owns this record. No release acceptance is issued.

The executed assessment sequence is specified in the
[self-service closure plan](../../../superpowers/plans/2026-09-16-self-service-capability-closure.md).
It preserves this record as the sole capability verdict owner.

## Execution update — September 17 UTC

The operator authorized execution, commit and PR publication. PR 411 merged at
`7c317703869d252e35560e994d9bd11576152827` on September 17 at 00:50:46 UTC.
Fresh remote-main inspection selected that exact revision, containing PRs 409
and 413, in a new isolated branch. The accepted feasibility document has no
content delta from the previously inspected PR 411 head. **G0 is closed.**
Merging the design does not implement its proposed runtime restriction.

Completed work: accepted-baseline verification; two selected consumer runs;
read-only status and specifically approved metadata inspection of both known Fly
apps; bounded authenticated account/report UI inspection; a focused vendor-source
pass; and the interface/trace-gap handoff below. No runtime code was changed.
Actual-evidence consumer rehearsals and production integration remain blocked
by missing inputs, rather than by PR 411's former open status.

### Current capability disposition

> ⚠ **R3 SUPERSEDED 2026-09-24** — see [Addendum 2026-09-24](#addendum-2026-09-24--t08-step-1-r3-return-no-documented-fence) (R3 stays UNPROVEN, now with a documentary NONE). All other rows are current.

This table is authoritative for the execution update. The original table later
in this record preserves the earlier assessment. All source/coverage/entitlement
fields not established below remain explicitly unknown as recorded there.

| Row | Current verdict | Execution evidence / remaining gap | One next disposition / owner |
|---|---|---|---|
| S1 | UNPROVEN | Authenticated report access exists; authoritative inception and fresh original full-history bytes remain absent | Joshua supplies lifecycle inception evidence and original bounded cash exports through capture |
| S2 | UNPROVEN | UI displays CDT; source-backed report-offset/date-to-calendar mapping still absent | Coordinator verifies the specific report/session mapping from a primary source |
| S3 | UNPROVEN | Historical position rows and current account summary observed; neither establishes required close equity or continuous boundary flatness | Joshua supplies the exact predecessor's close-equity/valuation record after chain disposition |
| S4 | UNPROVEN | No complete fresh finished-close package or authenticated actual submission | Joshua reviews/signs the exact admissible package once S1–S3 are established |
| S5 | UNPROVEN | No owner/settlement module at inspected host paths and no database artifact found in inspected data trees; global accepted-chain status remains unknown | Joshua confirms whether any other production owner/B7 acceptance location exists, with its retained receipt reference |
| R1 | QUALIFIED — local engineering only | Accepted code at `7c31770`; crash/transport uncertainty tests and signed consumer integration executed successfully below | Coordinator re-runs affected durability cases if the later real transport changes dispatch/persistence boundaries |
| R2 | UNPROVEN | Four actual historical order rows observed; no original report bytes or runtime-attempt/protection linkage accepted by a consumer | Coordinator acquires the original nonempty order/fill export through a working download path |
| R3 | UNPROVEN | Documented positive-correlation recipe found; absent-match terminal closure and all-actor delayed-effect fence remain unsupported by examined evidence | Coordinator obtains a source-backed terminal/no-future-effect protocol for the original request scope before any resend logic |
| R4 | UNPROVEN | Current-session reads and periodic history do not supply accepted complete causal history | Coordinator identifies one entitled producer with complete history and common causal acquisition/dispatch bounds |
| R5 | UNPROVEN | Local config flags observed; current external managers/copiers/manual/queued requests not fully inventoried | Joshua supplies the enabled external-actor and outstanding-request inventory |
| N1 | UNPROVEN for whole route | No four-leg production binding; specific inline triggered-trail and cancel/replace realizations are incompatible as scoped below | Coordinator produces an exact source-backed realization for the missing L2 primitives, or an explicit contract-change proposal |

### Deployment and chain evidence

Fresh Fly status showed one started machine for each known app. The specifically
approved stdlib-only metadata script inspected their data trees and selected
source paths without importing account code or opening state through a boot API.
Both remote captures contain JSON plus `READ_ONLY_INSPECTION_COMPLETE`; each SSH
wrapper nevertheless exited 1 with `The handle is invalid`. The follow-up route
read also returned its completion marker with wrapper exit 1. These are retained
remote observations, not successful SSH-wrapper claims.

- Listener config had `dry_run=true`, no arming expiry, and `destination=tradovate`.
- Daemon config had `emit_enabled=false`.
- Neither inspected data tree contained files with `.db`, `.sqlite` or `.sqlite3`
  suffixes, or names matching account/settlement/B7/seal. No account-owner or
  settlement module existed at the inspected application-relative paths.
- These observations cover the two inspected deployments only. They do not
  exclude a differently named file, external state location, earlier accepted
  receipt or other deployment. They do not establish effective runtime fencing,
  broker flatness or global no-chain status. No replacement B7 was selected.

Host/config digests and original output are indexed privately in capture batch
`CAP-20260916/execution-20260917`. No account identifiers, secret values or raw
state were copied into this public record. Automatic approval review initially
rejected the metadata transfer; the operator then explicitly approved the exact
payload/destination before execution. No host file or setting was changed.

### Actual account observations and capture limitation

After operator sign-in, the bounded Tradovate report menu exposed Performance,
Orders, Position History, Cash History, Order Details, Fills and Account Balance
History. Activity Log, User Sessions and Client Statements were not present in
that observed menu; this is not a universal entitlement denial.

The current-month Orders query (September 1–16, no optional instrument filter)
displayed four filled market-order rows, on September 2 and 10, with Chart/Exit
origin labels. Order Details for one of those real filled order IDs displayed
headers without detail rows. Position History over the same bounds displayed
two closed-position records. This establishes nonempty historical UI access,
not an original runtime request trace, continuous coverage or historical flatness
at another session's boundary. Account identity matched visually between the
Tradeify and Tradovate pages; host-config identity was not compared.

Tradeify details showed a current summary and update-age label, with no account
inception or historical close-valuation source found in the inspected view.
No full-history cash reread or exact-predecessor capture was claimed.

The Orders Download action did not yield a downloadable artifact through the
available browser interface; a download-event wait timed out and content export
reported unsupported. Further unchanged download attempts stopped. Original CSV
or rendered-page bytes were **not retained** for these new UI observations.
The private observer-authored log is explicitly labeled as such and cannot
substitute for original-byte evidence or a consumer rehearsal. No account/order
setting was changed; a Reports panel was added for read-only queries.

### R3 source result and N1 incompatible realizations

The [Tradovate API overview](https://crosstrade.io/docs/api/tradovate/overview#reconciling-an-ambiguous-placement)
provides a positive-correlation path for ordinary placement: persist a client
order identity, inspect working/all-session orders, inspect candidate lifecycle
New commands for that identity, then inspect positions. Plain placements are
not deduplicated. The recipe excludes inline ATM, which lacks that client-ID
binding and an exposed strategy-child lookup. Its absence-based resend step
does not establish this contract's required no-future-effect fence, especially
across session reset; we do not adopt that step. R3 remains UNPROVEN, with a
concrete positive lookup candidate and a precise negative-closure gap.

The [Tradovate execution internals](https://crosstrade.io/docs/webhooks/tradovate-advanced)
distinguish native continuous trailing from an ordinary inline OSO bracket's
profit-triggered trail, whose stop is managed by CrossTrade using its own pricing.
That **inline triggered-trail realization is UNSUPPORTED for retained L2(g)'s
native activated-trail requirement**. This is not a conclusion that every
Tradovate route is incapable. The separate ATM path still needs its own identity,
activation, owner/FIFO, OCO and anchor evidence; it is not silently substituted.

[Cancel Replace](https://crosstrade.io/docs/webhooks/commands/cancel-replace)
describes guarded cancellation followed by placement rather than a broker-atomic
edit. It is **UNSUPPORTED as an L2(c) atomic-amend realization**. Ordinary native
modify remains a candidate, requiring actual rejection/unknown-outcome and old-
protection evidence. Endpoint availability alone closes none of N1(a)–(g).

Original public-page bytes were retained privately. SHA-256: API overview
`dd7f839a7ddb2cd70579e5df09ef1f8585772907dd032fd573122ec6ae7e093d`;
execution internals `ebba0572199fefe4904c557612f3597cc4cebfd9dc467bc939608f69236c1502`;
cancel/replace `a0000d0d7f47ab62db0e3c27b81ced73a9bec6002fbbfa6e5b133d864d82365c`.
Captured September 17 at approximately 01:04:32 UTC; publication/effective revision
times unknown. These are documentary evidence, not account observations.

### Local verification and coverage handoff

From the isolated checkout at `7c317703869d252e35560e994d9bd11576152827`:

```powershell
pwsh -NoProfile -File ./fp.ps1 doctor
pwsh -NoProfile -File ./fp.ps1 --workers 2 python -m pytest tests/ops/test_book_account_owner.py tests/ops/test_book_owner_settlement_integration.py tests/ops/test_account_close_evidence.py tests/ops/test_account_close_calculation.py tests/ops/test_book_settlement.py
pwsh -NoProfile -File ./fp.ps1 --workers 2 python -m pytest tests/ops/test_book_protection_identity.py tests/ops/test_book_protection_allocations.py tests/ops/test_book_protection_evidence.py tests/ops/test_book_protection_lifecycle.py tests/ops/test_book_takeover_phases.py
```

Interpreter: primary checkout's validated `tmp/ops-env/Scripts/python.exe`, Python
3.13.2; 62 locked distributions matched; signing dependency 50.0.1. Results:
**316 passed** and **119 passed**, zero failures/errors/skips. Required signed
synthetic close and owner/listener cases executed. No production data or keys
were supplied to pytest. The full repository gate suite was not run.

Automatic records relative to the execution checkout:

- `.cache/fp-verification/20260917T005955Z-fb4e4251c18f/record.json`
- `.cache/fp-verification/20260917T010055Z-202cbe6b5bab/record.json`

Both records: completed, verification exit 0, stable source, complete capture,
valid JUnit and no capture/report errors. Docker not applicable. Test source
fingerprint before/after was
`83196429c1627876d61424492ae67c9e398c11d910ed480ed5ecff517ac0027b`:
base code plus the three untracked task documents, before this execution update.
Subsequent changes are documentation only. Global Git-ignore access warnings did
not invalidate those records; no environment or test failure is hidden.

| Trace | Executed evidence or exact remaining test task |
|---|---|
| Before/after-send crash | `test_book_account_owner.py::test_crash_cuts_retain_obligation_and_never_retry_on_boot` passed |
| Partial fill/cancel race | `test_book_takeover_phases.py::test_producer_cancel_removes_remainder_and_retains_late_fill` passed as producer-only characterization; raced terminal/fill evidence is not ingested back into the owner. Add that consumer trace and assert reservation, block and ownership outcomes |
| Restart/rollover | `test_book_account_owner.py::test_protected_session_restart_preserves_carried_fill_and_pending_add_without_rearm` passed |
| Residual scoped protection | `test_book_protection_allocations.py::test_scoped_close_adjusts_only_target_owner` passed |
| Correction/restore | Settlement revision/invalidation and restore-pending chain tests passed |
| Signed close into listener | `test_book_owner_settlement_integration.py::test_signed_synthetic_close_flows_through_unified_owner_into_listener_sizing` passed |
| Two unknowns, one resolved | Exact trace not established by selected runs: retain A and B, resolve only A, assert B still owns its reservation/block and neither is resent |
| Manual close, then old delayed request | Exact trace not established: retain unknown entry, observe manual flatten, deliver its delayed fill, assert retained ownership/intervention and no runtime resend |
| Remote effect after local halt | Exact trace not established: halt first, provider effect second, observation third; assert accounting update without new send. Late observation of a pre-halt effect is insufficient |

The consumer-bound cancel race and last three traces are bounded engineering tasks, not demonstrated defects. The
integration owner must supply those exact synthetic traces before claiming full
sequence coverage. No additional implementation was commissioned around an
imaginary source to make this record pass.

### Integration disposition and remaining work

The later production packet cannot yet be buildable: actual causal/history and
request-terminal producers, account bindings and normal primitive realizations
are missing. Existing listener seams (`handle_book_fact`, `handle_book_protection`
and typed runtime takeover ingestion) demonstrate consumer entry points, not
qualified network producers. The Python-only SyntheticBroker must remain a test
seam. A serializer/parser cannot invent its missing causal/fence inputs.

Next bounded work is the current matrix's acquisitions and exact synthetic
coverage tasks. In particular, obtain original report artifacts through a working
export route and resolve whether a production acceptance location exists outside
the inspected deployments. The account/route rows stay blocked until their actual
sources and consumers satisfy the retained contracts. Operator effort and usable
settlement/recovery latency remain unknown; test durations are not those measures.
No seal, signing action, broker order, provider message, deployment or activation
occurred. Commit/PR publication contains only public-safe assessment documents.

Independent documentary/source review accepted this execution update after correcting the cancel-race coverage claim to producer-only characterization and retaining four exact consumer-trace gaps. The reviewer verified links, unchanged runtime code, retained test records and cited vendor sources. Private host/UI observations were not independently reobserved. Documentary acceptance is not live capability or release acceptance.

## Initial pass — historical authority and revision gate

Everything below preserves the initial pass. Its open gate, unrun tests and
all-unproven verdicts are historical; the execution update above is current.


The operator instructed execution of the bounded assessment after its draft-only
handoff. The restrictions on production actions, signing, spending, contact,
implementation and activation remain. The plan separately requires a final
accepted PR 411 successor before dependent execution.

Fresh authenticated GitHub reads established:

| Reference | Observed identity and status |
|---|---|
| PR 411 | OPEN, head `72050e4a7d5248fb895bd736e4f446283e6d94b6`; no merge commit |
| PR 409 | MERGED at `845fb13ed2141482649627f5b78a51f4cadbd61d`, September 16 22:20:26 UTC |
| PR 413 | MERGED at `b4aa8efb0ee8f6d40b5aa332d5bb850bfa8b68ac`, September 16 23:56:40 UTC |
| Remote main | `b4aa8efb0ee8f6d40b5aa332d5bb850bfa8b68ac`; includes PR 409 (ancestry check exit 0) |
| Primary checkout | `c2e6eb2`, with pre-existing untracked work; not the runtime assessment baseline |

Code and contracts were read using `git show b4aa8ef:<path>`, avoiding unrelated
edits in the existing Phase 3 integration worktree. Its HEAD matches remote main,
but its working tree is dirty. No rehearsal was run on that tree or the older
primary checkout. PR 411 remains a proposed matrix; its accepted successor is
still owed. Its proposed incident-session restriction is not treated as an
implemented or ratified runtime behavior.

**Gate G0:** coordinator pins the final accepted PR 411 design, reviews its delta
against this record, and selects a clean baseline containing PR 409 and PR 413
before qualification/rehearsals. This is the next action for the execution gate;
the row actions below are conditional on that gate where applicable.

## Initial pass — Governing consumers and integration boundary

All repository references in this section are at `b4aa8efb0ee8f6d40b5aa332d5bb850bfa8b68ac`:

- `docs/spec/2026-09-15-tradeify-attended-settlement-contract.md`: evidence-backed
  authenticated close, full-history comparison, receipt, correction and restore.
- `docs/spec/2026-09-12-tradeify-account-snapshot-seal-contract.md`: initial B7
  C1–C10, E1–E3 evidence and consumption expiry. Its historical PROPOSED header
  remains visible; no production B7 approval is inferred from code availability.
- `docs/spec/2026-09-12-c1-multi-leg-rail-extension-spec.md`: section 2e E1/E2/E3,
  K1/K2 and R-B3 L2(a)–(g), with the rev9 attended amendment.
- `docs/spec/2026-09-14-tb-s3-halt-resume-contract.md`: governing attended owner;
  PR 411's further proposed restriction grants no substitute authority.
- `ops/c1_rail/account_close_evidence.py`, `account_close_calculation.py`,
  `book_settlement.py`, `book_account_owner.py`, `book_sizing_context.py` and
  `book_policy.py`: named implementation consumers. Production policy code was
  read before making the initial/subsequent peak distinction; no constants change.

The required path is original source facts → settlement verifier → durable
account owner → listener sizing → durable attempt → supported route outcome →
normal closure or attended intervention → complete reconciliation → ordinary
disarm. Missing producers block that path even when a local consumer exists.

The inspected `book_account_owner.py` explicitly accepts only its Python-only
`SyntheticBroker` seam. It persists an UNKNOWN attempt before transport, but
without that seam returns `production_route_unavailable`. This is an existing
production integration gap, not evidence of broker incompatibility. No adapter
is implemented by this assessment.

## Initial pass — Evidence register and provenance

Private index **CAP-20260916**, capture tag `20260917T003151Z`, is stored in the
established ignored primary-checkout evidence area. `git check-ignore` succeeded
before creation. It indexes five existing original files, with SHA-256 and
inspection times, without overwriting or moving them. Public references below
do not expose account values, identifiers or private filesystem locations.

| ID / class | What was inspected | Bounds and limitations |
|---|---|---|
| E01 / retained actual report | Balance CSV, SHA-256 `175fd26f04a6da194b5a9c89b15a5b9d3a9a4a062d5b1f6eaebb9c28cfcafced` | Bytes match the September 15 producer note. Original capture approximately September 14 22:24–22:29 ET. Report effective close and publication time not established. |
| E02 / retained actual report | Cash CSV, SHA-256 `a18cd70b710453d1cd39889602c1a0f080fa81292e9bf11268a6d22f849739b4` | September 1–14 selection in prior probe; incomplete inception-to-capture coverage. Same original capture window; not fresh evidence. |
| E03 / retained UI captures | Three original report UI text captures, indexed privately | No new account query; source ordering, correction and retention guarantees remain unproven. |
| E04 / documentary observation summary | September 14 CrossTrade probe at `39f47682208b21c28dd7abda9baac73e99e6be6b` | Successful read access and nonempty stored fills reported; raw broker responses were explicitly NOT retained. Digests/summaries cannot replace replayable original bytes. Historical order-item/lifecycle GETs failed. |
| E05 / operator statement and prior UI note | September 15 timezone/account inspection note | Supplied Tradovate label CDT and inclusive report dates do not establish universal endpoint semantics or historical flatness. Prior Tradeify journal inspection did not find the missing close evidence. |
| E06 / current operator statement | During this assessment: “none exists” in response to the combined status/export and actor-inventory request | No existing production B7/receipt/request export/status interface or current actor inventory identified. Does not prove there is no production chain or no actor. |
| E07 / fresh documentary evidence | Primary vendor pages listed below | Inspected this assessment; publication/effective revision times unknown. Documentation is not current account entitlement or consumer acceptance. |
| E08 / code and revision evidence | Exact Git blobs and fresh GitHub metadata above | No synthetic or actual consumer run in this assessment. No production route/config digest obtained. |

Prior report observations come from
`docs/notes/2026-09-15-packet1-producer-feasibility.md` at the runtime baseline;
the source capture predates that baseline. Its then-missing implementation claims
are historical and do not override the merged consumers. Cash-history annual
selection failed; one bounded selection succeeded. That does not establish a
general maximum query size or full-history completeness.

Fresh primary-source checks:

- [CrossTrade fill history](https://crosstrade.io/docs/api/tradovate/get-fill-history):
  periodic capture has no deadline guarantee, earlier sessions cannot be backfilled
  through this endpoint, and an exhausted cursor covers stored matching rows only.
  Its UTC query uses an inclusive lower and exclusive upper bound. The report UI's
  operator-supplied inclusive dates must not be copied to this API.
- [CrossTrade order lifecycle](https://crosstrade.io/docs/api/orders/get-order-lifecycle):
  examine the Tradovate surface separately from NT8; an order-ID read is not by
  itself a no-returned-ID request-resolution protocol.
- [CrossTrade account summary](https://crosstrade.io/docs/api/accounts/get-accounts-summary):
  snapshot availability does not establish the contract's common causal domain.
- [Tradovate partner reports](https://partner.tradovate.com/resources/admin-dashboards/reports)
  identify candidate report sources, not entitlement on this account.
- [Tradeify trading day](https://help.tradeify.co/en/articles/10468225-what-is-a-trading-day)
  describes an account-day convention, not a particular report's valuation time.

## Initial pass — Chain and actor finding

**Accepted production chain: UNKNOWN. Exact mandatory predecessor: UNKNOWN.**
Neither historical dates in tests nor absence of a located export establish an
accepted origin. September 14 cannot be promoted to a mandatory anchor, and a
later date cannot bypass a real predecessor. No live owner was opened through a
boot/migration API, no database initialized and no settlement submitted.

If a later read-only export establishes no accepted chain, use the existing B7
path: fresh separate E1 dashboard, E2 flat/no-working-order evidence and complete
E3 inception history, C1–C10, then the authenticated owner binding. Initial peak
uses the existing B7 derivation; subsequent accepted closes use the existing
ratchet. If a chain exists, retrieve its precise predecessor and receipts first.
Prospective capture cannot mend an established historical gap.

| Actor | Identity/history presently supported | Control and delayed effects |
|---|---|---|
| Runtime sender / listener | E04 identifies an earlier disarmed Tradovate route; current deployed code/config and request journal unknown | Current sender fence and queued requests unknown; historic disarm is not current evidence |
| Manual platform access | Earlier authenticated report access demonstrated | Enabled sessions, prior manual submissions and late effects unknown |
| Broker working orders | Earlier empty observations only | Current gross positions, orders, remainders and protection ownership unknown |
| Provider managers and triggers | No current inventory available | Enabled state and queued/conditional effects unknown |
| Copiers / signal shares | No current inventory available | Enabled destinations and delayed sends unknown |
| Scheduled / queued actions | No current inventory available | Local schedule state and remote accepted work unknown |

One acquisition packet, owned by Joshua with coordinator interpretation, must
provide a read-only chain/status export and a timestamped account-wide inventory
of these actors and retained request histories. Account values stay private.
Stop after that packet or an explicit unavailable finding; do not poll unchanged
empty snapshots. E06 currently supplies the unavailable finding.

## Initial pass — Capability dispositions

Common fields apply to **each** row: candidate account/environment is the incumbent
Tradeify account previously inspected through Tradovate DEMO; current binding and
entitlement are **unverified**. Execution route candidate is CrossTrade/Tradovate;
current route/config identity is **unknown**. Code identity is E08. Original-byte
digests/times are E01–E03 where relevant; no original broker trace is available
from E04. Source publication times, complete coverage, correction retention and
usable latency are unknown unless explicitly stated. Actual consumer result is
**not run / not accepted** for every row. No verdict below implies a consumer
failure. All next acquisitions have a single-pass stopping condition: return
the required source-backed fact or record that it is unavailable.

| Row | Requirement / consumer | Producer, evidence and precise gap | Verdict | Exactly one next disposition / owner |
|---|---|---|---|---|
| S1 | Inception and complete adjustments; B7 C8 and close calculation | Lifecycle record plus bounded Tradovate cash reports. E02 verifies retained bytes, not inception/full coverage or unchanged history. | UNPROVEN | Joshua supplies one inception-backed, account-wide bounded full-history package through capture, retaining overlap and revision comparisons. |
| S2 | Exact account session/close; accepted calendar and evidence verifier | Report-specific timezone/date semantics plus account/calendar mapping; E05's CDT label is insufficient across offsets and report types. | UNPROVEN | Coordinator obtains a source-backed mapping for the precise report and required session, including raw zone/offset and endpoint semantics. |
| S3 | Equity at close or balance plus contemporaneous flatness; verifier | E01 is balance history, with no established valuation or same-boundary flatness. Later empty views cannot substitute. | UNPROVEN | Joshua retrieves one account-accessible historical close-equity/valuation record for the predecessor determined by the chain packet. |
| S4 | Finished close, costs and no-known-correction assertion; verifier/authenticated submit | Reports plus exact-subject operator assertion; no fresh finished-close package or signing action. | UNPROVEN | Joshua reviews and authenticates one evidence-backed finished-close package once S1–S3 are satisfied. |
| S5 | Chain, challenge/receipt, correction and restored binding; SettlementStore/account owner/listener | Current B7, receipts and export unavailable (E06); predecessor unknown. | UNPROVEN | Joshua provides the one read-only accepted-chain/status packet described above; coordinator determines exact continuity. |
| R1 | Durable attempt before transport and crash uncertainty; account owner | E08 code journals UNKNOWN before send and provides crash cuts; no exact-revision consumer run retained here. Local engineering only. | UNPROVEN | Coordinator runs the named isolated durability tests below after G0, retaining launcher and revision-bound evidence. |
| R2 | Actual request/order/execution correlation; owner observation consumers | E04 describes nonempty fills but raw originals are absent; request/protection relationships and consumer ingestion unverified. | UNPROVEN | Coordinator captures one authorized nonempty, account/environment-bound request/order/fill trace with original bytes and tests its identity through the isolated consumer. |
| R3 | Resolve possibly effective request with no returned broker ID; E3 request ownership | Examined order-ID and stored-fill surfaces do not supply a proven request correlation/fence protocol for this route. | UNPROVEN | Coordinator examines one entitled platform request-history source for original-request lookup and delayed-effect closure; stop if it cannot supply them. |
| R4 | Complete coherent causal reconciliation; rail E1/E2 | Stored fill endpoint explicitly cannot certify complete history; snapshot and ID reads do not establish common causal ordering, gross lots or revisions. | UNPROVEN | Coordinator obtains one supported account-wide acquisition/history protocol with coverage and causal boundaries from the same entitled platform source. |
| R5 | Account-wide request closure/quiescence; E3/K1 | Current actor inventory and request obligations unavailable (E06); zero net position is insufficient. | UNPROVEN | Joshua provides one timestamped all-actor/request inventory with terminal evidence or explicit outstanding ownership for each actor. |
| N1 | All used normal primitives; R-B3 L2 and admission/execution consumers | No actual qualified primitive trace or current route capability binding; production owner transport is not implemented at E08. | UNPROVEN | Coordinator assembles the per-primitive source/trace packet below before proposing a bounded production adapter task. |

The fill-history endpoint **alone is unsupported as a complete-history producer**
for R4 under its documented scope. That bounded incompatibility does not establish
that the entire account/route is unsupported. No row is upgraded to QUALIFIED,
nor is a weaker protocol adopted as an amendment.

## Initial pass — R3 no-returned-ID disposition

No supported executable resolution protocol was established. Preserve the
original attempt and its account block; do not resend, release its reservation,
or infer failure from timeout/absence. A valid candidate must bind the original
attempt's account/environment, action, symbol, side, quantity and relationships
to a supported request-status record or remote fence. Query scope must include
all possibly effective earlier requests and deferred provider work. A terminal
result must exclude later effect, or transfer ownership to identified orders,
executions/gross lots or quarantine before clearing the request owner.

Consumer: the existing account owner's observation/reconciliation boundary under
rail E3/K1. Source identity, retention, lookup key without broker ID, causal fence
and terminal guarantee are all currently unknown. The next source examination
is one entitled platform request-history facility; neither support contact nor
route migration is authorized. If unavailable, retain R3 UNPROVEN and return
that exact capability choice. Repeat inquiry only on a named new source,
entitlement change or relevant observation. NT8 documentation cannot qualify the
incumbent Tradovate route.

## Initial pass — Per-primitive N1 packet

The mappings below are governing R-B3/S1–S5/S7/S10 requirements, not verified
declarations from a current sealed private-port/candidate manifest. That manifest
and its actual admission binding are still owed. Every subrow is **UNPROVEN**;
current actual consumer acceptance is absent. Each has one next packet item,
owned by the coordinator with Joshua supplying account-bound captures.

| Subrow | Required use and semantics | One next packet item |
|---|---|---|
| N1-entry | Market entry/add for applicable legs; transport acceptance differs from fill | Nonempty request-to-partial/full-fill identity trace with supported action semantics |
| N1-a | ORB resting stop entry, L2(a) | Supported resting-stop lifecycle and actual trace, including remainder identity |
| N1-b | Bracket on each bracketed entry, L2(b) | Entry/protective-child linkage evidence from a used port |
| N1-c | Atomic native modify, L2(c); old protection retained until effective replacement | Supported modify/rejection semantics and actual parameter/identity trace |
| N1-d | Scoped close plus attached-order removal, L2(d); explicit scope distinct from triggered owner/FIFO | Supported atomic close/removal and residual-owner trace, including unknown-quantity semantics where required |
| N1-e | Partial fills preserve correctly sized residual protection, L2(e) | Source-backed partial-fill/residual-protection sequence excluding reverse orphans |
| N1-f | First attach to bare lot, including Striker, L2(f) | Supported attach-to-existing-fill linkage and trace satisfying subsequent close/partial-fill rules |
| N1-g | Native activated trailing/OCO, including ORB, L2(g) | Supported activation/offset/anchor rules and trace preserving surviving sibling anchors; record trailing-parameter modification behavior |
| N1-cancel | Cancel a known entry/add remainder; fill/cancel race retains execution ownership | Actual terminal cancellation and any intervening fill trace for that request |
| N1-close-time | Port-defined crossed-level close-time exit | Triggering protection-owner/FIFO trace, without substituting explicit-lot closure |
| N1-takeover | Aegis displacement only after required cancellation/close/quiescence | Composite trace preserving every displaced obligation before new admission |
| N1-schedule | Ordinary cutoff/flatten, residual protection and confirmed closure | Supported scheduled sequence through final reconciliation and disarm |

Endpoint names or one market-order success cannot satisfy these items. An atomic
modify cannot be replaced by cancel/replace; scoped closure cannot be replaced
by concurrent cancel/market close. A locally tracked extreme is not native trail.

## Initial pass — Bounded collection and rehearsal procedure

For settlement, retain separate original reports and query-result evidence for
every bounded range from proven inception through new capture, with overlaps.
Compare transaction IDs and full contents for additions, removals and revisions;
never overwrite the earlier bytes. Map the exact required account session before
selecting any historical close. If the historical S3 acquisition fails, prepare
a prospective protocol as the subsequent disposition: qualified coverage across
the accepted boundary for positions, orders, request uncertainty, balance/equity,
and the finished-close package. Two bracketing snapshots alone are insufficient.
Determine whether that protocol can serve initial B7 or leaves a real predecessor
gap before scheduling capture.

Freshness/authority remain the existing owners' rules: ongoing reports/current
views at most 30 minutes old at receipt, separate effective/published/captured/
signed/received times, and the 300-second one-use challenge subject to its other
bounds. Initial B7 retains its separate boundary/expiry checks. Signing never
supplies missing source facts. Measured operator effort, acquisition time,
usable submission latency and latest usable production submission are **unknown**.

No actual order procedure is executable yet: precise account/environment binding,
starting state and supported expected outcomes are unavailable. The following is
the conditional operator handoff, not an approval request or transmit instruction:

| Required field | Condition to make the procedure reviewable |
|---|---|
| Account/environment | Privately bind incumbent account, environment, route/config digest and all enabled actors |
| Exact starting state | Evidence-backed gross positions, working orders, protection owners and outstanding requests; no unexplained effects |
| Action/scope | Select only the named N1 gap and exact existing port primitive; exact quantity/symbol/limits require separate scoped approval |
| Expected identity | Original attempt → provider request → order/children → executions and immutable protection/FIFO relationships |
| Original capture | Account-bound supported request/order/execution records, original bytes plus query bounds/times and digest |
| Supported result | Source statement and consumer expectation for that subrow, established before action |
| Stop/intervention | Any identity conflict, partial/unknown effect, missing coverage or protection uncertainty ends testing and invokes the existing attended procedure |
| Teardown | Supported terminal evidence for each request, no gross lots/remainders/orphans, and ordinary disarm; flat snapshot alone insufficient |
| Authority | Joshua performs separately approved platform actions; existing owner retains unresolved effects after test window |

No artificial live lost response or transport failure is proposed. Prefer existing
nonempty traces. Tests cannot turn an undocumented guarantee into a supported one.

Selected existing tests for the eventual isolated baseline, not run here:

```powershell
.\fp.ps1 doctor
.\fp.ps1 python -m pytest tests/ops/test_book_account_owner.py tests/ops/test_book_owner_settlement_integration.py tests/ops/test_account_close_evidence.py tests/ops/test_account_close_calculation.py tests/ops/test_book_settlement.py
```

R1 specifically includes `test_crash_cuts_retain_obligation_and_never_retry_on_boot`
and `test_transport_acceptance_never_creates_fill_credit_and_restart_retains_reservation`.
Settlement integration includes
`test_signed_synthetic_close_flows_through_unified_owner_into_listener_sizing`
and `test_revision_and_account_intervention_commit_before_failing_notification`.
Use the accepted launcher's documented bootstrap if PowerShell 7.3+ is unavailable.
Record interpreter, exact revision/dirty state, command, results and automatic
verification records. Signing cases must execute. No production paths or keys
go to pytest; synthetic keys do not authenticate actual operator submissions.

These selected suites are a starting set, not an assertion that every decisive
trace is covered. After G0, map two unknowns/one resolved, operator close with an
older unknown, delayed provider work, partial-fill/cancel race, rollover/restart
and residual protection to exact existing cases; retain any missing test as a
bounded engineering task. Synthetic success can qualify local behavior only.

## Initial pass — Verification, review and exit

Performed: fresh GitHub metadata and remote-main read, PR 409 ancestry check,
revision-pinned code/contract inspection, primary-source documentation checks,
original report hash comparison, and ignore verification before private indexing.
The first sandboxed GitHub read failed because its configuration was inaccessible;
the authorized escalated read succeeded. No secrets were printed or staged.

No project Python ran: interpreter/test counts/verification-run paths are **not
applicable**. Doctor and rehearsals were not attempted because G0 is unresolved.
This is not an environment failure or a passing gate-suite claim. No actual
consumer qualification, host inspection, account acquisition, signing, order,
deployment, code edit, commit or PR publication occurred in this assessment.

Independent documentary review by `review_capability_record` returned no actionable
findings and accepted this blocked record within its stated limits. It inspected
the pinned consumers/contracts and independently rechecked the narrow fill-history
limitation. Private artifact integrity and fresh GitHub metadata were supplied by
the coordinator, not independently reverified by the reviewer. No tests or account
actions occurred in review. This is not capability or release acceptance.
The initial bounded pass has precise gaps for every
row, but the accepted-design prerequisite and dependent rehearsal/qualification
work remain incomplete. Phase 4 is not complete.

Requalify affected rows after changes to accepted design/contracts, code or
consumer binding, account/environment, route/config, enabled actors, report
semantics/coverage, corrections, history retention, symbol/contract rollover or
port primitive declarations. Preserve prior evidence and refusals. G0 closure
alone qualifies no S/R/N row and grants no production permission.

## Addendum 2026-09-24 — T08 step 1 (R3) return: no documented fence

Append-only. The only edit above is a one-line reader intercept on the current
table (operational Rule 14). Source: the
[T08 return, §7](../../handoffs/2026-09-21-tradeify-t08-broker-protection-feasibility.md#7-executor-return).

**R3 — UNPROVEN, now with a documentary NONE.** A refute-first primary-source
search covered CrossTrade and Tradovate documentation, the public API specs,
vendor staff posts and support articles: 1,802 retained files, evidence-index
SHA-256 `974ea080aaa3dc0a3d421dea7a1dcd15af2786922b2ca8d239513a40edba065a`.
It tested 24 candidate protocols, and none survived. No source documents a
terminal / no-future-effect fence for an original request whose outcome is
unknown on the CrossTrade-webhook → Tradovate route, across the session reset,
with all-actor scope. The standing R3 consumer outcome therefore applies to
every unknown request: **preserve and block, no resend, no reservation release.**
The positive in-session correlation recipe recorded above remains a correlation
aid, not a fence.

**September 17 pages re-read.** The three CrossTrade pages retained on
September 17 (SHA-256 `dd7f839a…`, `ebba0572…`, `a0000d0d…`) have new bytes
(`f84d10c1…`, `adaa513e…`, `21a8e8c7…`) because the vendor rebuilt its docs on
2026-09-21, and bytes change with every site build. Compared as text:
- the API overview and cancel/replace are unchanged;
- the internals page dropped its "Trailing protective stops" section, while
  its CrossTrade-managed triggered-trail wording remains.

The September 17 statements, including the L2(g) and L2(c) incompatibilities,
therefore still stand (T08 §7.4).

**Also recorded.** Tradovate's support article states that prop-firm and
evaluation accounts are not eligible for native API access
(`F4__tvsf_Tradovate-API-Access__record.json` `4a91db885f44d8ce`). No
native-Tradovate read route is available for the incumbent eval.

**Consequence.** Under the ratified D-broker wording (deployment-checklist
amendment, Addendum 2026-09-22), the conditional grant is void. T09 stays
unspecifiable until the operator decides among contract or route options, which
are listed in the T08 return §7.6. No row here is qualified or released by this
addendum.

**One next disposition / owner.** The operator decides among the T08 §7.6
options. The review recommends (T08 §7.7): hold live release, authorize one
narrow vendor question on bounding deferred work, and scope an ADR-level
bounded-exposure amendment in parallel.
