# D9 recommendation: operator-recorded VOID for identity-recheck mismatches

**Status: PROPOSED design for the C′ card's D9; rulings R-1–R-8 are owed by the operator.** It was produced on 2026-10-02 by a coordinator design panel: three independent approaches (A: signed acknowledgement of a retained event; B: a VOID /v3 protocol; C: a store-chokepoint token), each scored by three judges. All three judges picked A. Their fixes are folded in: stickiness, store-derived boundness, and an uncharged queue pre-check. Source: `origin/codex/h9-t05-integration@f237178`. Nothing here is implemented.


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
- Pre-admission path: the guardian (`campaign_supervisor` ~1510) observes before `finish_diagnostic_admission`.

**B. Event (built by the store, never by the producer)**
- `CampaignStore.retain_void_recheck(attempt, request_bytes, entrypoint, observed|None)`:
  - Reads `expected` from the campaign's own retained context release. It never takes it from a caller argument.
  - Computes the verdict itself: MATCH, MISMATCH, or UNOBSERVABLE when `observed` is `None`.
  - Builds the C' §2.4 supervision-event version with kind `IDENTITY_RECHECK` and `data = {transition:'VALID_TO_VOID', request_sha256, release_sha256, entrypoint, expected, observed, verdict}`.
- The row is stored in `full_campaign_objects` under role `void_recheck_match_<sha256(event)>` or `void_recheck_mismatch_<sha256(event)>`.
  - The prefix deliberately avoids `supervision_event_` (whose integrity branch calls `_work()`) and `supervision_` (which the walk parses as an enrollment).
  - No RPC role can write these rows.
- Service path: committed in its own transaction before any refusal or commit.
- Pre-admission path: written in the admission transaction.

**C. Acknowledgement carrier**
- A closed grammar inside the existing signed `reason`: `^IDENTITY_MISMATCH_ACK:[0-9a-f]{64}( .*)?$`.
- The reason is already inside the signed subject (service 431–438 / 580–588; `campaign_store` 2436–2445), so the digest is operator-signed with unchanged signing tooling.
- It is parsed only in `campaign_store`, and only for **bound** campaigns, so a historical free-text reason that starts with the prefix can never fail reopen.

**D. Chokepoint: `CampaignStore.void(request_bytes, *, now, identity_recheck)`**
`identity_recheck` is required (no default): either an event digest or `NOT_BOUND`. Steps, in order:
1. `void_retry` first. An exact already-VOID retry returns the historical bytes. No observation, no event, no write.
2. Boundness comes from the campaign's retained release. Bound with `NOT_BOUND`, or unbound with a digest, is refused.
3. Bound campaigns: the digest must name a retained event of this attempt with all of:
   - `transition == VALID_TO_VOID`
   - `request_sha256 == sha256(request_bytes)`
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
  - Not MATCH and no valid acknowledgement: call the existing `refuse_void_authentication(raw, seq, 'VOID_IDENTITY_MISMATCH <d>', clock)`. A charged sequence writes `void_refusal_<seq>` (no refund); sequence 0 writes the terminal uncharged refusal. Then raise.
  - Otherwise: `complete_void_authentication(raw, seq, now=, identity_recheck=<d>)`, which re-validates inside `void()`.
- **Pre-admission (2464):** a mismatch goes to the existing `_refuse_admission_void(..., 'VOID_IDENTITY_MISMATCH <d>')`. Admission continues and the fence holds.
- **service:452:** passes `NOT_BOUND`. The C' release must be in the diagnostic routing tuple (~390–410). Under C' a bound campaign reaching 452 is refused, fail closed; a test pins this.

**F. Uncharged queue pre-check (`queue_diagnostic_void`, 1792)**
On a bound campaign, refuse uncharged when either:
- a mismatch row exists and the reason has no valid acknowledgement; or
- the acknowledgement is malformed, dangling, names a MATCH row, or names another attempt's row.

This also covers a re-queue of an identity-refused body, so a doomed VOID never spends a charge.

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
| `ops/c1_rail/qualification/execution/campaign_supervisor.py` | event-version parser shape; guardian observation at ~1510 | No |
| `ops/c1_rail/qualification/execution/runtime_identity.py` | `observe`, `expected_identity` (C'-owned, new) | New; must not be imported by a closure module through D9 code |
| `tests/.../test_runtime_identity_rechecks.py`, `test_campaign_cancellation.py`, `test_campaign_supervision.py` | extended in place, never replaced | n/a |

**Untouched:** `campaign_protocol.py`, `protocol.py` and `attempt.py` (all closure members), plus `contract.py`, `store.py`, `campaign_result.py`, `campaign_seal.py` and `campaign_funding.py`.

**Phase-0 must re-run the closure script.** Codex's statement that "all five D5 files are inside the 68" refers to `release_schema`, `runtime`, `worker`, `campaign_probe` and `protocol`, not to D9's files. Any closure movement caused by C' itself stays a D5 matter: a fresh S5 after the final closure change, with nothing carried over.

## 5. VOID writer coverage

| Writer / caller | Treatment |
|---|---|
| `CampaignStore.void` (2602–2633; sole `validity='VOID'` + budget VOID writer) | Chokepoint; `identity_recheck` required |
| `service:452` (non-diagnostic FULL_E1) | `NOT_BOUND`; refused if the store finds the campaign bound; unreachable under C' routing (pinned) |
| `complete_void_authentication` 2183 (seq 0) / 2190 (charged), from service ~611 | Observe → retain → refuse via the existing record, or complete with the digest |
| `finish_diagnostic_admission` 2464, guardian ~1510 | Guardian observation; mismatch → `_refuse_admission_void`; admission proceeds fenced |
| Exact already-VOID retry (service 419/553, `void_retry` 2593) | No write; byte-identical; zero observations |
| `ExecutionStore.void` (`store.py` 430–441, caller service:362) | **Exempt (R-6).** N1_ONLY, separate table, disjoint attempt namespace (`campaign_store` 1284/2821/3610), no PASS/seal path. Pinned: an N1 VOID naming a FULL_E1 attempt fails at `store.status` (KeyError) with no write |
| `AttemptJournal.void` (`attempt.py` ~1003–1015) | **Exempt (R-6).** No production caller; editing it is a closure change |

Enforcement: an AST/SQL inventory test fixes the exact set of writers, including every SQL `validity='VOID'` and `_save_budget(...'VOID')`. It also requires `identity_recheck=` at every `CampaignStore.void` call.

## 6. Fail-closed cases and the fail-first test list

**Fail-closed cases:**
- `void()` called without `identity_recheck` → `TypeError`.
- A boundness mismatch in either direction → refuse.
- The event is absent, belongs to another attempt, has the wrong transition, request digest, release digest or `expected`, or has an inconsistent verdict → refuse.
- Fresh MISMATCH or UNOBSERVABLE with no acknowledgement → automatic VOID refused. The event survives, validity stays VALID, the existing refusal record names the digest, and the charge is not refunded.
- Any mismatch row with no acknowledgement, **even when the fresh verdict is MATCH** → refuse (sticky).
- Malformed or dangling acknowledgement, or one naming a MATCH row or another attempt's row → refused uncharged at queue, and again at `void()`.
- Bad signature → no observation, no event, no fence.
- Mismatch row on a VALID campaign → `_cancellation_pending` is true, so result, seal, funding, new work and positive transitions refuse.
- Reopen: the integrity violations listed in §2.H; unknown event or resolution versions → refuse.
- Crash between the event commit and refuse/complete → fence up, validity VALID, the claim is recovered by the existing in-doubt path.

**Fail-first tests** (each fails at `f237178` and passes on the build; launcher-recorded):
- **T1:** changing the acknowledgement digest under the same approval → subject mismatch.
- **T2:** bound MATCH on each path → v1 receipt and budget bytes equal the unbound baseline, plus one MATCH row.
- **T3:** MISMATCH, one case per tuple field, on charged, seq-0 (BUDGET_UNCERTAIN, IN_DOUBT, past deadline) and pre-admission paths.
  - Refused with the digest; event retained after the raise; charge unchanged; `remaining_cpu_ns` unchanged by the recheck.
- **T4:** fence. All barrier sites refuse; historical RESULT/SEAL retry bytes unchanged.
- **T5:** stickiness. A later MATCH plain VOID is refused, and an acknowledged VOID then commits.
- **T6:** acknowledged VOID while still mismatching or UNOBSERVABLE.
  - Commits with the v1 receipt plus a resolution row; reopen passes.
  - Deleting the event or the resolution makes reopen fail.
- **T7:** bad acknowledgements are refused at queue with zero charge.
- **T8:** exact retry → byte-identical, zero observations, no rows.
- **T9:** pre-C' releases v1–v7 including path 452 → journals and receipts byte-identical, zero new rows. A historical reason that starts with the prefix still reopens.
- **T10:** bad signature → zero observations.
- **T11:** producer timeout or exception → UNOBSERVABLE path.
- **T12:** forged-shape rows refused at the chokepoint and at reopen.
- **T13:** crash injection after the event commit.
- **T14:** N1 KeyError pin.
- **T15:** writer and inventory AST test.
- **T16:** closure table at `f237178` vs the build shows zero D9-contributed rows.

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

## 8. Rejected alternatives

- **B, VOID request /v3 plus receipt /v2:** it edits `campaign_protocol.py`, which is in the closure (a C3 return). A new wire family is the card's own stop condition, and `service:390` would refuse v3 before it reaches routing.
- **C, `VoidAuthority` token and shared minter:** the sentinel is in-process ceremony with no security value, and refactoring three verification sites puts historical refusal bytes at risk.
- **Recheck inside the store transaction (B and C):** it holds the DB10 write lock for up to the probe timeout.
- **A's caller-supplied `release` / `NOT_BOUND`:** a caller could pass a pre-C' release and skip the recheck. The store now derives boundness itself.
- **A without stickiness:** a later MATCH would let a plain VOID bypass the operator-recorded path the ruling requires.
- **A host signing key for events:** new key policy and provisioning, which is excluded.
- **Covering service only:** it misses 2183, 2190 and 2464.
- **Refunding the charge on a mismatch refusal:** it changes the original VOID accounting.
- **Refusing N1 VOID under C' (B's guard):** it can strand VOID for any surviving N1 execution. The KeyError pin plus the disjoint namespace already makes the exemption structural.

Sources read: `origin/codex/h9-t05-integration` at `f237178`, under `ops/c1_rail/qualification/execution/` (`campaign_store.py`, `service.py`).