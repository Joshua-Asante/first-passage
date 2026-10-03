# D9 recommendation: operator-recorded VOID for identity-recheck mismatches

**Status: design ADOPTED for the C′ card's D9. Operator rulings R-1–R-8 are all YES** *(Joshua, directly to the deployment coordinator, 2026-10-02: "yes to all eight")*. Implementation follows the C′ card under its review gate.

**Corrections of 2026-10-02**, after the Codex review of #614 at 7d6ef35 (one P1 and two P2). These fold in without changing the wording of R-1–R-8:
- **P1:** the refusal commits atomically with the event, and the event records its outcome and claim, so no crash leaves the VOID permanently stuck.
- **P2 (pre-admission):** a VOID body queued before admission is deferred, not identity-checked. Admission finishes with PASS fenced by the pending body, and the operator resends the same signed bytes after admission. This replaces R-8's pre-admission recheck premise for bound campaigns, and the operator **confirmed it** *(Joshua, directly to the deployment coordinator, 2026-10-02: "yes to R-8")*: admission finishes with PASS fenced by the pending body, and the operator resends the same signed VOID after admission. The funded v3 profile is required.
- **P2 (tests):** the test list is split into new red→green regressions and preservation cases.

The design was produced on 2026-10-02 by a coordinator design panel: three independent approaches (A: signed acknowledgement of a retained event; B: a VOID /v3 protocol; C: a store-chokepoint token), each scored by three judges. All three judges picked A. Their fixes are folded in: stickiness, store-derived boundness, and an uncharged queue pre-check. Source: `origin/codex/h9-t05-integration@f237178`. Nothing here is implemented.


Design only. No source was edited and no tests were run. I re-checked the VOID writer and barrier anchors at `f237178`:

- `campaign_store` `void` 2602, its single `UPDATE … validity='VOID'` at 2622 and `_save_budget(...,'VOID')` at 2632
- callers at 2183, 2190 and 2464
- `_cancellation_pending` at 1845 and `queue_diagnostic_void` at 1792
- `service` 362 (N1), 390 (diagnostic routing refusal) and 452

## 1. Recommendation

Use **Design A** (a signed acknowledgement of a retained mismatch event; no protocol change), with three judge-identified gaps closed:

- **Stickiness:** once a mismatch exists, every VOID needs an acknowledgement.
- **Store-derived binding:** the store, not the caller, decides whether a campaign is bound to the entrypoint map.
- **Uncharged pre-check:** a VOID that will be refused is refused at queue time, before any charge.

`CampaignStore.void` is the single chokepoint. A non-MATCH recheck becomes a content-addressed mismatch row written by the store. That row refuses the automatic commit and permanently trips `_cancellation_pending`, so the campaign cannot reach PASS. Only an operator-signed VOID whose signed reason names the mismatch digest can VOID it. That VOID uses the unchanged v1 receipt and the unchanged budget VOID accounting, plus a structured resolution row.

No request, receipt or approval family changes. The DB10 layout is unchanged. There is no key-policy change and no edit to a module in the 68-module measured closure.

## 2. Mechanism

**A. Observation (outside any DB transaction)**
- `runtime_identity.observe(entrypoint)` returns the observed tuple: executable, base interpreter, lock, wrapper and UID.
  - It is uncharged, has a fixed C' timeout, and is independent of budget and deadline.
  - It returns `None` on timeout or error.
- The producer never computes the verdict.
- Service path: runs after the existing claim and signature verification, so an unsigned body produces no event and no fence.
- Pre-admission path: **none.** No observation runs before a receipt exists. Before `finish_diagnostic_admission` retains the context (2529–2538) there is no retained release to read `expected` from. The body's signature is verified only inside that function's transaction (2431–2454), so an observation outside a transaction would come before signature verification. A bound campaign's validly signed plain body is deferred to the service path instead (§2.E).

**B. Event (built by the store, never by the producer)**
- `CampaignStore.retain_void_recheck(attempt, request_bytes, entrypoint, observed|None, *, void_claim, clock_bytes)`:
  - `void_claim` is one of:
    - `{path:'CHARGED', sequence:N}` for a charged claim;
    - `{path:'TERMINAL', sequence:0}` for the uncharged terminal attempt;
    - `{path:'ADMISSION', sequence:<next admission-refusal slot>}` on the pre-admission path.
  - For CHARGED, the store re-checks the existing `_charged_attempt` conditions: `void_authentication_<N>` exists, has `request_sha256 == sha256(request_bytes)` and has no refusal. For TERMINAL, it re-checks that `pending_void` equals `request_bytes`.
  - Reads `expected` from the campaign's own retained context release. It never takes it from a caller argument.
  - Computes the verdict itself: MATCH, MISMATCH, or UNOBSERVABLE when `observed` is `None`.
  - Builds the C' §2.4 supervision-event version with kind `IDENTITY_RECHECK` and `data = {transition:'VALID_TO_VOID', request_sha256, release_sha256, entrypoint, expected, observed, verdict, void_claim, acknowledged_event_sha256, outcome}`.
    - `acknowledged_event_sha256` is the retained mismatch digest that the request's reason validly acknowledges (§2.C/§2.F), or `null`.
    - `outcome` is computed by the store, never the caller:
      - **REFUSE** when `acknowledged_event_sha256` is `null` and any of these holds: the verdict is not MATCH; a `void_recheck_mismatch_*` row already exists for the attempt (sticky); or the reason carries the acknowledgement prefix without validly acknowledging (mirrors §2.F and `void()`).
      - **PROCEED** otherwise, whatever the verdict (R-4).
    - `void_claim` makes CHARGED and ADMISSION event bytes unique per claim. An identical sequence-0 retry on the TERMINAL path (after a PROCEED crash) rebuilds byte-identical bytes, so the insert is absent-only: a present role must be byte-equal (it is content-addressed) and is reused, never re-inserted. This avoids a `PRIMARY KEY(attempt_id, role)` collision under a plain `INSERT`.
- The row is stored in `full_campaign_objects` under role `void_recheck_match_<sha256(event)>` or `void_recheck_mismatch_<sha256(event)>`.
  - The prefix deliberately avoids `supervision_event_` (whose integrity branch calls `_work()`) and `supervision_` (which the walk parses as an enrollment).
  - No RPC role can write these rows.
- Service path: one transaction. On **REFUSE**, the same `BEGIN IMMEDIATE` transaction writes:
  1. the event row;
  2. the existing v1 refusal for the claimed sequence, with reason `VOID_IDENTITY_MISMATCH <d>`. For CHARGED this is `void_refusal_<N>`, charge retained, no refund. For TERMINAL it is the terminal refusal keyed by the body digest, uncharged;
  3. the delete of `pending_void`.

  `<d>` is this event's digest when it is a mismatch row. On a sticky or invalid-acknowledgement MATCH it is the lowest-sorted retained mismatch digest. The refusal bytes come from the existing builders unchanged, factored out of `refuse_void_authentication` so both callers share them. On **PROCEED**, the event row commits alone and completion follows.
- No committed state therefore holds a REFUSE event without its refusal, or a mismatch row whose unacknowledged request is still pending with its claim unrefused (see §2.F, Interrupted authentication).
- Pre-admission path: none. No event is written before the receipt (§2.E).

**C. Acknowledgement carrier**
- A closed grammar inside the existing signed `reason`: `^IDENTITY_MISMATCH_ACK:[0-9a-f]{64}( .*)?$`.
- The reason is already inside the signed subject (service 431–438 / 580–588; `campaign_store` 2436–2445), so the digest is operator-signed with unchanged signing tooling.
- It is parsed only in `campaign_store`, and only for **bound** campaigns, so a historical free-text reason that starts with the prefix can never fail reopen.

**D. Chokepoint: `CampaignStore.void(request_bytes, *, now, identity_recheck)`**
`identity_recheck` is required (no default): either an event digest or `NOT_BOUND`. Steps, in order:
1. `void_retry` first. An exact already-VOID retry returns the historical bytes. No observation, no event, no write.
2. Boundness comes from the campaign's retained release (`context_execution_release`, retained at 2529–2538). Bound with `NOT_BOUND`, or unbound with a digest, is refused. An attempt with no `diagnostic_receipt` has no retained release and is unbound for `void()`. Its only production caller is `finish_diagnostic_admission` 2464, which under §2.E reaches `void()` only when the context it is retaining in the same transaction is unbound. T15 pins this.
3. Bound campaigns: the digest must name a retained event of this attempt with all of:
   - `transition == VALID_TO_VOID`
   - `request_sha256 == sha256(request_bytes)`
   - `void_claim` equal to the completing claim (`{CHARGED, seq}` or `{TERMINAL, 0}`; `{ADMISSION, slot}` at 2464), and `outcome == 'PROCEED'`
   - `release_sha256` and `expected` equal to the retained release
   - a verdict consistent with expected vs observed
4. **Sticky rule:**
   - If any `void_recheck_mismatch_*` row exists for the attempt, the reason must carry a valid acknowledgement naming one of those rows. This holds even when the fresh verdict is MATCH.
   - If the fresh verdict is not MATCH and there is no acknowledgement, refuse with `VOID_IDENTITY_MISMATCH <d>`.
5. Commit:
   - the unchanged v1 receipt, the `UPDATE` and `_save_budget('VOID')`;
   - if acknowledged, also a singleton `void_identity_resolution` row: `{schema:'qualification_campaign_void_identity_resolution/v1', attempt_id, acked_event_sha256, fresh_event_sha256, request_sha256, approval_sha256, receipt_sha256}`.

**E. Callers**
- **Service diagnostic path (~545–611):** after the claim, signature check and observation:
  - The recheck runs **after** the existing signature `try/except (ValueError, KeyError)` (service 570-609), never inside it. A bad signature therefore causes no observation, and the identity refusal is never refused a second time through `refuse_void_authentication`.
  - Observe outside any transaction, then sample `observe_campaign_clock()` (the refusal clock, as at service 608). Then call `retain_void_recheck(..., void_claim={CHARGED,seq} or {TERMINAL,0}, clock_bytes=clock)`.
  - REFUSE: the store has already committed the event, the refusal and the pending delete in one transaction. The service only raises `VOID_IDENTITY_MISMATCH <d>`.
  - Otherwise: `complete_void_authentication(raw, seq, now=, identity_recheck=<d>)`, which re-validates inside `void()`.
- **Pre-admission (`finish_diagnostic_admission` 2416–2464): a bound campaign authenticates and refuses here but never VOIDs here; an unbound campaign is unchanged.**
  - **Boundness source.** Boundness is taken from `context.release`. The guardian verified that release against the installed release and its signed approval (`admission._verify_bundle` 157–159). This same transaction retains it as `context_*` (2533) and binds it into the receipt (2519). It is therefore the authenticated, immutable binding that §2.D step 2 and §2.B later read. Nothing reads a caller-supplied `expected`.
  - **Funded only.** A bound context whose `campaign_budget_profile` schema is not `qualification_campaign_budget_profile/v3` raises before any write. A deferred body can be resolved only through a funding projection (`claim_void_authentication` 2030).
  - **Bound, bad signature or unenrolled key (2431–2454).** Unchanged: `_refuse_admission_void` under the admission work, and the body is cleared. There is no observation, no event and no fence.
  - **Bound, valid signature, reason matches the §2.C acknowledgement grammar.** Refused the same way with `VOID_IDENTITY_ACK_DANGLING`, and the body is cleared. No event can exist before the receipt, so the acknowledgement necessarily dangles. There is no observation.
  - **Bound, valid signature, plain reason.**
    - There is no observation, no event and no `void()`. The body stays as `pending_void`.
    - Admission binds, settles and writes its receipt as today. The general barrier is scoped to admitted campaigns (1871–1885), and the receipt is inserted after 2486, so 2742 passes.
    - From the receipt onward `_cancellation_pending` fences PASS. STATUS reads `void_pending: true` with a non-null receipt.
    - The admission-time verification is neither authority nor reused.
  - **Resolution.** The operator resends the exact bytes, and `queue_diagnostic_void` accepts them as the same pending body (1816).
    - The §2.F pre-check passes, because no mismatch row can exist while this body is pending: 1816 refuses any other body, so no other service VOID can run.
    - The existing service sequence then runs: charged claim (1988–2076; sequence 0 when the budget is terminal), signature verification, observation outside any transaction, event, then refuse or complete.
  - **Unbound (releases v3–v7).** 2416–2464 are unchanged, and 2464 passes `NOT_BOUND`.
  - **Residual.**
    - If finish returns before the receipt (2469, 2471, 2483, 2504) and no later finish writes one, a valid deferred body stays queued, and `claim_void_authentication` refuses it (2020–2023).
    - The operator's VOID is then not recorded, whereas f237178 would VOID the body at 2464.
    - No authority is granted: with no receipt there is no PASS, result or seal, and new work refuses at 3021.
    - This widens the existing no-receipt stranding: a body queued after such an outcome is stranded at f237178 too.
- **service:452:** passes `NOT_BOUND`. The C' release must be in the diagnostic routing tuple (~390–410). Under C' a bound campaign reaching 452 is refused, fail closed; a test pins this.

**F. Uncharged queue pre-check (`queue_diagnostic_void`, 1792)**
On a bound campaign, refuse uncharged when either:
- a mismatch row exists and the reason has no valid acknowledgement; or
- the acknowledgement is malformed, dangling, names a MATCH row, or names another attempt's row.

This also covers a re-queue of an identity-refused body, so a doomed VOID never spends a charge.

Before the receipt there is no retained release, so the pre-check has nothing to check and the body queues as today. Bound admission refuses an acknowledgement-bearing body and clears it (§2.E). A deferred plain body passes the pre-check when it is resent, because no mismatch row can exist while it is pending.

**Interrupted authentication (crash recovery)**

Pending removal happens only in:
- `_refuse_admission_void` (1979);
- `refuse_void_authentication` (2133-2136, 2160-2163);
- `complete_void_authentication` (2184-2194).

Each claim allocates the next charge sequence (2039), and an unresolved charge is a permitted retained state (walk 3638-3662). D9 adds no recovery writer. It makes each crash point land in a state that already resolves:

| Crash point | Durable state after reopen | Resolution |
|---|---|---|
| After the claim commit, before the recheck transaction commits (during signature verification or observation, or inside the transaction, which `store.transaction()` rolls back on `BaseException`, store.py 183-186) | Claim N charged and unresolved; original `pending_void`; no event; fence = `pending_void` only | Pre-D9 behaviour, unchanged. The exact retry passes the pre-check (no mismatch row), claims N+1 (or 0 again on TERMINAL) and re-observes. No ACK body is needed or queueable (1816). |
| After the REFUSE commit | Event; refusal naming `<d>` (`void_refusal_<N>` charged with no refund, or the terminal refusal); pending deleted; fence held by the mismatch row; validity VALID | The ACK body queues: there is no pending body, the pre-check finds a valid acknowledgement, and the terminal re-queue bar (1822-1826) keys only the original digest. It is then claimed, and VOID commits with the resolution row. |
| After a PROCEED commit, before completion | Event bound to its `void_claim` and `sha256(pending)`; claim unresolved; `pending_void` is the acknowledged (or clean plain) body, so the pre-check passes | The exact retry claims N+1 (or 0 again), retains a fresh event (an identical TERMINAL event is reused) and completes. A charged claim N stays charged (existing rule; R-5). |

On the pre-admission path, the event, `_refuse_admission_void` or `void()`, and admission share one transaction, so it has no window.

**G. No-PASS fence**
- `_cancellation_pending` becomes: VALID and (`pending_void` exists, or any `void_recheck_mismatch_*` row exists). One indexed GLOB.
- Existing barrier sites then refuse:
  - `campaign_store` 2742 and 3021
  - `campaign_funding` 593
  - `campaign_result` 722, 797, 867 and 1095
  - `campaign_seal` 134, 169 and 289
- Historical RESULT/SEAL retries return before these checks.
- The fence clears only at VOID.

**H. Reopen (integrity walk, metered branch only)**
- Each `void_recheck_*` role must:
  - match `sha256(body)`;
  - match its verdict prefix;
  - belong to the attempt;
  - pass the closed parse;
  - carry `expected` equal to the retained release.
- A VOID row on an attempt that holds any mismatch row must carry an acknowledging `void_request` and a resolution row whose digests equal `sha256(void_request)`, `sha256(void_receipt)`, the approval digest, and retained events.
- A bound v1/v2 VOID without a mismatch must have a MATCH event bound to `sha256(void_request)`.
- These roles on a dormant row are refused by the closed inventory.
- An attempt without `diagnostic_receipt` has no retained release and is read as unbound. A bound VOID before the receipt is unreachable in code (§2.E, T15, T17). A forged one is host-level row forgery, the residual R-1 accepts. `void_admission_refusal_*` rows keep their existing checks on bound and unbound attempts alike.
- `outcome` must be consistent with the event:
  - a non-null `acknowledged_event_sha256` requires PROCEED and must name a retained `void_recheck_mismatch_*` row of the attempt;
  - PROCEED with a null acknowledgement requires verdict MATCH;
  - REFUSE with verdict MATCH requires the attempt to hold a mismatch row.
- Every `outcome == 'REFUSE'` event must pair with the refusal for its `void_claim`:
  - CHARGED: `void_refusal_<N>`;
  - TERMINAL: the terminal refusal keyed by `request_sha256`;
  - ADMISSION: the admission refusal at that slot.

  The pair needs an equal `request_sha256` and reason `VOID_IDENTITY_MISMATCH <d>` naming a retained mismatch digest, and no `pending_void` may carry that request. Otherwise reopen refuses with `identity recheck refusal binding differs`. The state is unreachable by construction (§2.B), so this is a forged-state refusal, not a recovery path. The walk stays read-only.
- A CHARGED event's claim must exist with an equal `request_sha256`.

## 3. Schema and protocol changes

**Unchanged:**
- campaign request v1/v2 and the VOID fields `{reason, operator_approval_bytes}`
- approval scope `VOID_QUALIFICATION_ATTEMPT` and its subject preimage
- `qualification_campaign_void_receipt/v1`
- the refusal records v1 (the digest travels in their existing reason text)
- RESULT/SEAL v1, supervision v1/v2, release v1–v7
- DB10 two-table layout and `user_version`
- `campaign_protocol.py`

**Added:**
1. VALID_TO_VOID fields inside the C'-owned new supervision-event version. Its closed parser sits beside v1/v2, and unknown versions are refused.
2. Roles `void_recheck_match_<sha>` and `void_recheck_mismatch_<sha>`.
3. `qualification_campaign_void_identity_resolution/v1` (singleton role), with a closed parser.
4. The acknowledgement grammar, bound campaigns only.
5. Optional `diagnostic_status` key `identity_void_mismatch` (latest mismatch digest, expected, observed). It is present only when a mismatch row exists, so historical STATUS bytes are unchanged. This needs ruling R-7.

## 4. Files

| File | Change | In the 68-module measured closure? |
|---|---|---|
| `ops/c1_rail/qualification/execution/campaign_store.py` | chokepoint, `retain_void_recheck`, `parse_mismatch_ack`, queue pre-check, `_cancellation_pending`, 2183/2190/2464 pass-through, resolution parser, integrity walk, optional status key | No (two judges ran the stage-1c script) |
| `ops/c1_rail/qualification/execution/service.py` | observe, retain, refuse-or-complete at ~545–611; `NOT_BOUND` at 452 | No |
| `ops/c1_rail/qualification/execution/campaign_supervisor.py` | event-version parser shape only; no guardian observation and no `runtime_identity` import (§2.E) | No |
| `ops/c1_rail/qualification/execution/runtime_identity.py` | `observe`, `expected_identity` (C'-owned, new) | New; must not be imported by a closure module through D9 code |
| `tests/ops/qualification/execution/test_campaign_cancellation.py`, `test_campaign_supervision.py` | extended in place, never replaced | n/a |
| `tests/ops/qualification/execution/test_runtime_identity_rechecks.py` | new (absent at `f237178`) | n/a |

**Untouched:** `campaign_protocol.py`, `protocol.py` and `attempt.py` (all closure members), plus `contract.py`, `store.py`, `campaign_result.py`, `campaign_seal.py` and `campaign_funding.py`.

**Phase-0 must re-run the closure script.** Codex's statement that "all five D5 files are inside the 68" refers to `release_schema`, `runtime`, `worker`, `campaign_probe` and `protocol`, not to D9's files. Any closure movement caused by C' itself stays a D5 matter: a fresh S5 after the final closure change, with nothing carried over.

## 5. VOID writer coverage

| Writer / caller | Treatment |
|---|---|
| `CampaignStore.void` (2602–2633; sole `validity='VOID'` + budget VOID writer) | Chokepoint; `identity_recheck` required |
| `service:452` (non-diagnostic FULL_E1) | `NOT_BOUND`; refused if the store finds the campaign bound; unreachable under C' routing (pinned) |
| `complete_void_authentication` 2183 (seq 0) / 2190 (charged), from service ~611 | Observe → retain → refuse via the existing record, or complete with the digest |
| `finish_diagnostic_admission` 2416–2464 | **Bound:** the funded profile is required; a bad signature or an acknowledgement-bearing reason is refused via `_refuse_admission_void` with no observation; a valid plain body is deferred to the service path, and admission finishes fenced by `pending_void` (§2.E). **Unbound:** unchanged; 2464 passes `NOT_BOUND`. No guardian observation in either case |
| Exact already-VOID retry (service 419/553, `void_retry` 2593) | No write; byte-identical; zero observations |
| `ExecutionStore.void` (`store.py` 430–441, caller service:362) | **Exempt (R-6).** N1_ONLY, separate table, disjoint attempt namespace (`campaign_store` 1284/2821/3610), no PASS/seal path. Pinned: an N1 VOID naming a FULL_E1 attempt fails at `store.status` (KeyError) with no write |
| `AttemptJournal.void` (`attempt.py` ~1003–1015) | **Exempt (R-6).** No production caller; editing it is a closure change |

Enforcement: an AST/SQL inventory test fixes the exact set of writers, including every SQL `validity='VOID'` and `_save_budget(...'VOID')`. It also requires `identity_recheck=` at every `CampaignStore.void` call.

## 6. Fail-closed cases and the test lists

**Fail-closed cases:**
- `void()` called without `identity_recheck` → `TypeError`.
- A boundness mismatch in either direction → refuse.
- The event is absent, belongs to another attempt, has the wrong transition, request digest, release digest or `expected`, or has an inconsistent verdict → refuse.
- Fresh MISMATCH or UNOBSERVABLE with no acknowledgement → automatic VOID refused. The event survives, validity stays VALID, the existing refusal record names the digest, and the charge is not refunded.
- Any mismatch row with no acknowledgement, **even when the fresh verdict is MATCH** → refuse (sticky).
- Malformed or dangling acknowledgement, or one naming a MATCH row or another attempt's row → refused uncharged at queue, and again at `void()`.
- Bad signature → no observation and no event on any path. The existing refusal clears the body, so there is no fence. Post-admission this is the charged refusal; before the receipt it is the admission refusal.
- Bound pre-admission:
  - `finish_diagnostic_admission` never observes, writes an event or calls `void()`.
  - A validly signed body with an acknowledgement-bearing reason is refused there as dangling.
  - A bound context without the funded profile raises before any write.
- Mismatch row on a VALID campaign → `_cancellation_pending` is true, so result, seal, funding, new work and positive transitions refuse.
- Reopen: the integrity violations listed in §2.H; unknown event or resolution versions → refuse.
- Crash during authentication: there is no in-doubt recovery for a claimed authentication, and D9 needs none. On the refusing path, the event, the refusal and the pending delete are one commit. A crash before that commit leaves the pre-D9 interrupted-claim state, and the exact retry claims the next sequence. A crash after a PROCEED commit leaves an acknowledged or clean body that the exact retry completes. Charged claims are never refunded (R-5), and the fence never drops before VOID. See §2.F, Interrupted authentication.

**Test lists.**
- **Recording:** every case is launcher-recorded on the build.
- **List (a), red evidence:** each case is also run unchanged against `f237178` source, and that record is the red evidence.
- **List (b), preservation:** each case runs at both revisions and must pass at both.
- **Fixtures:**
  - A C′-bound campaign cannot be built at `f237178`: `release_schema` 16–30 ends at v7, and boundness is derived by the store (§2.D.2).
  - Preservation cases therefore use v1–v7 fixtures, which both revisions can construct.
  - A bound variant is build-only evidence, recorded separately, and is never cited as preservation.
- **Red cause:** each list (a) case names its cause.
  - *behavioral:* a base-constructible fixture reaches the base code path, which does the opposite; the line is cited.
  - *absent:* the bound release, `runtime_identity`, the event or the asserted row does not exist at `f237178`.
  - An absent red is reported as absent. The base path it cites is a reference only, never behavioral evidence.
- **Collection:** new cases import build-only symbols inside the test body, so the extended files still collect at `f237178`.
- **Misclassification:** a list (a) case that passes at `f237178` is misclassified and moves to list (b).

**(a) Red→green regressions** (fail at `f237178`, pass on the build):
- **T2 (absent):** bound MATCH on each path (charged, seq-0, pre-admission).
  - VOID commits and retains exactly one `void_recheck_match_*` row bound to `sha256(request)`.
  - The v1 receipt and the budget VOID bytes equal the build's unbound baseline for the same request and clock.
  - Base reference: `void` 2602–2633 writes only the row update, the receipt and the budget.
- **T3 (absent):** MISMATCH, one case per tuple field, on charged, seq-0 (BUDGET_UNCERTAIN, IN_DOUBT, past deadline) and pre-admission paths.
  - Refused with the digest.
  - The event is retained after the raise.
  - The charge is unchanged, and the recheck leaves `remaining_cpu_ns` unchanged.
  - Base reference: commits at 2183, 2190 and 2464.
- **T4 (behavioral):** fence.
  - Setup: insert a `void_recheck_mismatch_*` row directly into a VALID v1–v7 fixture with no `pending_void`.
  - Expected: every §2.G barrier site refuses, and STATUS `void_pending` reads true.
  - Base: `_cancellation_pending` 1845–1859 reads only `pending_void`, so 1882 and the other sites proceed, and 2301 reads false.
- **T5 (absent):** stickiness. A later MATCH plain VOID is refused; an acknowledged VOID then commits.
- **T6 (absent):** acknowledged VOID while still MISMATCH or UNOBSERVABLE.
  - Commits with the v1 receipt plus a resolution row, and reopen passes.
  - Deleting the event or the resolution makes reopen fail.
- **T7 (absent):** bad acknowledgements on a bound campaign are refused at queue with zero charge.
  - Covers: malformed, dangling, naming a MATCH row, or naming another attempt's row.
  - On a v1–v7 fixture both revisions queue the body (§2.C), so no behavioral red exists.
  - Base reference: 1792–1821 queues any bounded v2 VOID body, and the claim then charges it (2036–2039).
- **T10-bound (absent):** bad signature on a bound campaign, on the service and pre-admission paths.
  - Expected: zero observations, no event and no fence.
- **T11 (absent):** producer timeout or exception → the UNOBSERVABLE path.
- **T12a (absent):** forged-shape rows on a bound campaign are refused at the chokepoint.
  - Base reference: `void` 2613–2633 never reads retained rows.
- **T13 (absent):** crash injection after the event commit, at the store/supervisor seam.
  - The fence is up, validity is VALID, and the original charge and authentication record are kept (R-5).
  - The claim is closed by the P1 interrupted-authentication resolution, not left as an unacknowledged `pending_void`.
- **T15a (behavioral):** AST test: every `CampaignStore.void` call passes `identity_recheck=`.
  - Base: callers 2183, 2190 and 2464 and service 452 pass only `now=`.
**P1 crash cases (new red→green; supersede the earlier T13 single line; the refusal now commits atomically with the event, so there is no separate recovery writer):**
- T13a: service queue -> mismatch -> crash after the retain_void_recheck commit -> reopen. Assert:
  - no pending_void;
  - void_refusal_<1> with VOID_IDENTITY_MISMATCH <d> and the original request_sha256;
  - charge 1 retained, no refund;
  - void_pending true, and RESULT/SEAL/funding refuse;
  - validity VALID;
  - the original body's re-queue is refused uncharged.
  
  Then the ACK queue is accepted uncharged, and VOID commits as charge 2 with resolution acked_event_sha256 == d, total 2 x bound, the fence cleared and a clean reopen.
- T13a-terminal: the same on a sequence-0 (terminal-budget) campaign: a terminal refusal keyed by the original digest; the ACK body queues and VOIDs uncharged.
- T13b: crash after the claim commit, before the recheck commit, both during observation and inside the transaction (rolled back). Reopen shows charge 1 unresolved, the original pending and no event. An ACK body is refused 'pending cancellation differs'. The exact retry is refused with charge 2 and a mismatch; then the ACK commits VOID with charge 3. No refund.
- T13c: crash after a PROCEED event commit for an ACK body, before complete_void_authentication. The exact ACK retry claims the next sequence and commits VOID; the earlier event and claim are retained and reopen passes.
- T13d: forged stuck states, each refused by reopen with 'identity recheck refusal binding differs' (or an outcome inconsistency):
  - a REFUSE event, mismatch or sticky MATCH, with no paired refusal;
  - a REFUSE event with pending_void still carrying its request;
  - an event whose outcome is inconsistent with its verdict and acknowledgement.
- T13e: two charged claims on the same body with an identical observation produce distinct void_recheck_* roles; a TERMINAL PROCEED crash then exact retry with an identical observation reuses the byte-equal role and completes. No PRIMARY KEY error in either case.
**P2 pre-admission case (new red→green; replaces the earlier pre-admission MISMATCH case, since bound pre-admission runs no identity recheck and the VOID is deferred to after admission):**
- T17 (fail-first), real bound pre-admission through the campaign_supervisor admission branch (1464-1517) with a counting observe spy. (a) A bad-signature body and (b) a validly signed body with an ACK-grammar reason are each refused inside admission: void_admission_refusal_* row, body cleared, zero observations, zero void_recheck_* rows, receipt written unfenced. (c) A validly signed plain body: the receipt is written with zero observations, pending_void is retained, void_pending is true and the T4 barriers refuse. Reopen between admission and resend passes the walk with the body still pending. The exact bytes are resent through the service: one charged claim and exactly one observation after verification; MATCH completes; MISMATCH is refused with the digest, the charge is retained and the fence stays. Fails at f237178 (2374-2381 binding; body consumed at 2416-2464).

**(b) Preservation cases** (v1–v7 fixtures; pass at `f237178` and on the build):
- **T1:** changing the reason, including an acknowledgement-shaped digest, under the same approval → subject mismatch, refused, no VOID.
  - Base: the reason is in the signed subject (service 336–344 for N1, 583–590 for diagnostic; `campaign_store` 2436–2445 for pre-admission).
  - Build-only bound variant: the changed digest names a second retained mismatch row of the same attempt, so the queue pre-check passes. The subject check then refuses with a charged refusal and no VOID.
- **T4-history:** historical RESULT/SEAL retry bytes are unchanged, and retries return before the barrier, including after a directly inserted mismatch row.
- **T8:** exact retry → byte-identical, with no claim, no charge and no rows.
  - Base: service 553–555 calls `void_retry` 2593–2600, as in existing test 175–197.
  - Build-only bound variant: zero observations.
- **T9:** pre-C′ releases v1–v7, including path 452 → journals and receipts byte-identical, zero new rows. A historical reason that starts with the prefix still reopens.
- **T10:** bad signature on the service and pre-admission paths → refusal retained, VALID, no `pending_void`. Base: existing tests 147–172 and 408–445.
- **T12b:** a forged `void_recheck_*` row inserted directly makes reopen raise.
  - Base refuses it through the closed inventory (3577–3580, or 3755–3756 before admission). The build refuses it through §2.H.
  - Assert only that reopen raises, not the message.
- **T14:** an N1 VOID naming a FULL_E1 attempt fails at service 284 → `store.status` 469 → `_status` 443–446 (`KeyError('unknown attempt')`), before the N1 VOID branch (331–362), with no write.
- **T15b:** the VOID writer set is exactly `campaign_store` 2622 and 2632, `store.py` 437 and `attempt.py` 1013.
- **T16:** comparing the closure table at `f237178` with the build shows zero D9-contributed rows.
- **T20:** existing test `test_campaign_cancellation.py` 466–488 is unchanged: an interruption with no event keeps the body and the charge, and the retry is charged again.
- T18 (preservation, P2), three cases. (1) Unbound v3-v7: pre-admission 2416-2464 bytes are identical to f237178, including the bad-signature void_admission_refusal_* row. (2) A bound context whose campaign_budget_profile is not v3 raises in finish_diagnostic_admission with no row written. (3) A bound admission that returns before the receipt leaves a valid body queued; claim_void_authentication refuses it (2020-2023); zero observations.
- **Reworded by P2:** T10 now covers zero observations and zero `void_recheck_*` rows on both the post-admission and bound pre-admission paths. T15 adds that 2464 is the only no-receipt `void()` caller and is unreachable once the finish context is bound.

## 7. Rulings Joshua must give (each answer is yes or no)

- **R-1:** "Yes, I accept that mismatch provenance is host-attested by protected store code, content-addressed, and countersigned by my signature over its digest. It is not host-unforgeable. A forged mismatch can only remove authority, and a forged MATCH is the accepted C' host-drift residual."
- **R-2:** "Yes, the operator-recorded VOID is a signed VOID whose reason carries `IDENTITY_MISMATCH_ACK:<event digest>`, interpreted only on runtime-identity-bound campaigns, with no new request, receipt or scope."
  - If no: use the fallback, a distinct approval scope `VOID_QUALIFICATION_ATTEMPT_IDENTITY_MISMATCH` whose subject adds the event digest. That also needs no `campaign_protocol` or key-policy change, but the signing tooling changes.
- **R-3:** "Yes, any retained mismatch is sticky. It permanently bars PASS through the existing cancellation barrier until VOID, STATUS `void_pending` reads true, and every later VOID requires my acknowledgement even if a later recheck matches."
- **R-4:** "Yes, my acknowledged VOID commits whatever the fresh recheck says; that verdict is recorded, not gating. A timeout or measurement error counts as UNOBSERVABLE and takes the mismatch path."
- **R-5:** "Yes, original accounting stands. A mismatch refusal consumes the authentication charge already claimed, with no refund. The sequence-0 terminal path stays uncharged. The acknowledged VOID is charged under the existing rules, and the budget VOID transition is unchanged."
- **R-6:** "Yes, `ExecutionStore.void` (N1_ONLY) and `AttemptJournal.void` are exempt from the identity recheck, for the stated reasons."
- **R-7:** "Yes, `diagnostic_status` v2 may carry an optional `identity_void_mismatch` key, present only when a mismatch row exists, without a status version bump."
- **R-8:** "Yes, a pre-admission identity-mismatch refusal lets admission finish, with PASS fenced, mirroring the existing admission-refusal semantics."
  - *Revised and confirmed 2026-10-02 ("yes to R-8"):* for runtime-identity-bound campaigns there is no pre-admission identity recheck. A VOID queued before admission is deferred, admission finishes with PASS fenced by the pending body, and the operator resends the same signed bytes after admission, when the recheck runs. The funded v3 profile is required.

## 8. Rejected alternatives

- **B, VOID request /v3 plus receipt /v2:** it edits `campaign_protocol.py`, which is in the closure (a C3 return). A new wire family is the card's own stop condition, and `service:390` would refuse v3 before it reaches routing.
- **C, `VoidAuthority` token and shared minter:** the sentinel is in-process ceremony with no security value, and refactoring three verification sites puts historical refusal bytes at risk.
- **Recheck inside the store transaction (B and C):** it holds the DB10 write lock for up to the probe timeout.
- **A's caller-supplied `release` / `NOT_BOUND`:** a caller could pass a pre-C' release and skip the recheck. The store now derives boundness itself.
- **A without stickiness:** a later MATCH would let a plain VOID bypass the operator-recorded path the ruling requires.
- **A host signing key for events:** new key policy and provisioning, which is excluded.
- **Covering service only:** it leaves the store writers 2183, 2190 and 2464 unguarded. Under §2.E the chokepoint still guards 2464, which reaches `void()` only for an unbound context.
- **Refunding the charge on a mismatch refusal:** it changes the original VOID accounting.
- **Refusing N1 VOID under C' (B's guard):** it can strand VOID for any surviving N1 execution. The KeyError pin plus the disjoint namespace already makes the exemption structural.

Sources read: `origin/codex/h9-t05-integration` at `f237178`, under `ops/c1_rail/qualification/execution/` (`campaign_store.py`, `service.py`).