# T07 operator workflow: implementation admission and source-evidence closure proposal

**Date:** 2026-10-11. **Status:** PROPOSED; task-owned readiness packet and draft implementation handoff, not a dispatch or acceptance record.
**Recipient:** existing Deployment Coordinator. **Authority for this task:** Joshua's bounded cloud delegation; one new proposal file only. **Publication authorized 2026-10-11 20:22 UTC:** Joshua requested draft PRs; this file may be committed and pushed on its isolated branch and published as a documentation-only draft PR. This is the author's proposal, not coordinator admission or acceptance. The settlement contract, T07/H6 cards, CAP rows and deployment checklist retain ownership. This packet supplies decisions and executable scope; it does not recreate their specification.

**Recommendation:** admit a separate, two-file operator-workflow build that composes existing consumers, after certifying its writer and resolving the process/signing boundary below. In parallel, request the smallest local evidence inventory in §7. Initial T07 acceptance can use current-regime evidence; it is not yet established by these public sources. **The post-2026-11-01 T07 R3 repeat remains required before T16 unless explicitly superseded.** Historical records and synthetic tests do not waive it. [T07, lines 41–64][T07] [checklist, lines 853–865][CAL]

## 0. Refreshed sources and ownership

**Initial audit:** 2026-10-11, approximately 18:45–19:16 UTC, at **`b6fff029678992f753111134e30f94d85dd3b80b`**, then current main with an initially clean worktree. Main-file citations below retain that immutable audit pin. **Publication refresh:** approximately 20:24–20:27 UTC; `git fetch origin main` advanced to **`a1fd53d5c2882a25cd6bbae5014aefd9cd2acb4c`**. The only intervening file changes are `lab/research_utils/sfgrowth_margin.py` and `tests/lab/test_sfgrowth_margin.py` from #782; the cited main sources and six production hashes are unchanged. Publication branch `codex/t07-operator-workflow-readiness` starts from that refreshed main. Open **#788** remains at **`4edf5648c10dc1e9ab05037f7dac3e62f1929456`** (`origin/pr-788`).

Read `AGENTS.md`, `STATE.md`, `PIPELINES.md`, the relevant owners below, and the repository `verify-source`, `handoff-verify` and `brief-authoring` skills. For publication, `.agents/skills/babysit/SKILL.md` delegates to the canonical PR workflow; Joshua's explicit draft-only instruction governs its exit state. Source-state checks precede the proposal. The user directs a separate task-owned document, so no owner text was amended.

Open-PR refresh used the GitHub connector after both `gh pr list` (GraphQL) and `gh api .../pulls` returned `Forbidden` during the initial audit. The publication refresh returned **#746, #752, #776, #777, #783, #786, #787, #788, #789**; changed-file lists for all nine were inspected. #782 has merged; #789 is newly open. None is a dedicated T07 workflow implementation or changes the two proposed implementation paths. This is a bounded public-PR finding, **not certification that no unpushed/local owner exists**.

- **Related author proposal #789:** guided settlement R1 overlaps this packet's purpose. Its pinned [R1, lines 76–108](https://github.com/Joshua-Asante/first-passage/blob/cf6408b972f8b8085fc3f7819b0e72923298a081/docs/notes/2026-10-11-tradeify-operator-attention-proposal.md#L76-L108) keeps manual import first, operator signing and existing T07/DST gates. The coordinator should reconcile the proposals into one implementation owner, not launch duplicate wrappers. #789 is not an implementation dispatch or a superseding source/acceptance ruling. Its broader collection/attention scope is not added here.

- **Protection-health #780 is merged**, contrary to the older scope note's “building” summary: merge `2cfb3d728076cce7ede31c916eb5b2f214aeedd4`, 2026-10-11 00:57:02Z; included in this main. The owner module's last change is `aff6922cec0e76558d30946396fd00ffac6a4a83`. [#780](https://github.com/Joshua-Asante/first-passage/pull/780)
- **#788 remains open.** Its P-L2 card records code admission and freeze, but dispatch waits on its build gate, P-L1, GC-5-DISPLACED and the shared-file queue. Its order is protection-health → GC-5 → P-L2, with TB-I3 S2 ordered by readiness. That admission is specific to those edits, not T07. Do not edit `book_account_owner.py` or borrow that writer slot. [P-L2 at #788, lines 309–320][PL2]
- **H6 has an existing DRAFT harness card**, single-writer lane proposed as `claude/h6-rehearsal-harness`; it explicitly excludes the operator entry point. Its two proposed test files are not tracked at this main. Their local/remote-session status is UNKNOWN. Reuse that lane and accepted tests; do not recreate its harness here. [H6 card, lines 5–41, 96–129][H6CARD]

Production bytes read before drafting, SHA-256 at the main pin:

| Path | SHA-256 |
|---|---|
| `ops/c1_rail/account_close_assembler.py` | `803c4c4c663a1a3a83ba4d2754b52935123ed03e1c6df7c49c5c405e27aa1364` |
| `ops/c1_rail/account_close_evidence.py` | `e575fe860d2a9fbe55f6c9ab874ef67a627720681d6eb0e264a9876773fb5ec0` |
| `ops/c1_rail/book_account_owner.py` | `ad86a0e6c2663b996ef3d792f24e1a322320c18f5087548e9845a75d74d54b9a` |
| `ops/c1_rail/book_settlement.py` | `8ce440ff1de1200e8539bb498e8ced42d05ab5c2663178f12feab26c1c8fa930` |
| `ops/c1_rail/settlement_signing.py` | `1663a77b75646f54ae5f92cb38c3ef4a8166a850319d5bde6db3c01c8f3d259e` |
| `ops/c1_rail/qualification/trust_domain.py` | `e7e5128e226e101128a879b3fdea326c75f496c744ddcb8aee905de7302613cb` |

## 0.5. Exact admission and writer decisions

The original T07 authority covers collection/rehearsal, not signing or a production entry point; H6 repeats that boundary. A source-fact stop is not permission to implement around it. The coordinator can prepare a synthetic tooling scope independently of collection, but must record its separate admission and freeze. [T07, lines 6–7, 29–38, 52][T07] [H6, lines 419–446][H6]

| Decision | Owner and recommended concrete disposition | State / blocker |
|---|---|---|
| **D1 — tooling admission** | Deployment Coordinator: place this wrapper in a **separate tooling slice serving T07**, with the §2 footprint, unchanged consumer semantics, §4 cases and synthetic-only build. Explicitly distinguish it from H6 and T09 route implementation. | PROPOSED; no implementation dispatch in this task. |
| **D2 — writer certification** | Coordinator: ask the existing T07/H6/local sessions for branch, head, dirty-file list and any unpushed implementation; name exactly one workflow writer and reserve only the two new paths. Prefer the existing settlement executor if free; use a Claude worker under a frozen card, as H6's trust-chain routing requires. | UNKNOWN outside this checkout. An empty public search is insufficient. |
| **D3 — owner lifetime / integration** | Adopt `run_session(owner, calendar, private_root, clock, input_stream, output_stream)` in the new module, handed an already booted, attached owner by an approved composition. Keep challenge through submit in that process. Coordinator names the actual composition root and its owner before private operational use. | The reviewed sources show in-process methods and tests, not an accepted operator host adapter. A production CLI that silently boots a second owner is inadmissible. A composition change, if needed, is a separately scoped handoff. |
| **D4 — signing boundary** | Adopt **prepare-sign + Joshua's detached Ed25519 signing + import/submit**. The wrapper constructs exact canonical envelope bytes and never loads, creates or invokes a private key. Joshua confirms the existing operator-device signer and key enrollment outside this build. | Signer invocation/device and operational readiness UNKNOWN. Public enrollment or a test key is not custody/access proof. |
| **D5 — code/freeze impact** | Coordinator rechecks import closure at dispatch. New wrapper is not in the compiled inventory at this pin; do not import it from a bound consumer or change inventory/pins. Any edit to owner, verifier, evidence, signing or trust-domain modules returns for Joshua's **specific bound-code admission**, queue allocation and freeze consequences. | Those modules are bound (`listener_account_owner` and runtime dependencies). #788 admission cannot be reused for T07. [trust policy, lines 140–184][TRUST] |
| **D6 — source acceptance** | Coordinator separately rules on R3 source admissibility (including browser-response option b), all three S2 facts, target identity, and S5/B7 continuity from the local packet. Joshua supplies account-only facts; coordinator records CAP dispositions in the existing owner. | Public commissioning record still says **Binding hash: OWED**. Whether Joshua privately supplied it later is UNKNOWN, not disproved. [commissioning §2.4][TARGET] |
| **D7 — second-regime equivalence** | Keep the repeat scheduled as a dependency. Consider §3.2 only if qualifying historical originals are later identified. Any replacement of the dated repeat requires an explicit Joshua ruling through the T07/checklist owners, naming evidence and exact superseded condition. | No superseding ruling identified. November 1 is not a promised release date. |

**Decision classification:** D1 is a new coordinator tooling-scope decision; D2 is existing-owner reconciliation. D3 is a concrete integration design and ownership decision, not permission to create a second account writer. D4 proposes the detached-signing interface; identifying an already approved signer/enrollment is setup reconciliation, not an inferred request for a new key. D5 applies existing change-control, with new Joshua admission needed only if bound-code edits are actually proposed. D6 is the existing T07/CP-2 source-evidence acceptance process, not a new blanket approval. D7 is an optional new operator ruling only if substitution is requested; otherwise the standing repeat needs no re-ratification.

Before the synthetic build, the coordinator freezes its D1/D2 scope/writer, D3 injected-owner interface, D4 detached-signature contract, D5 limits and named tests at a committed revision. Actual operational composition and signer readiness must be established before private operational use, but their absence need not block a separately admitted synthetic build. If a choice needed for the admitted slice remains open, return `NEEDS_CONTEXT`; do not invent a host, signer, predecessor or source semantics. Publishing this proposal grants none of those future implementation decisions.

## 1. Existing capability and the actual gap

| Stage | Exact existing capability | Missing wrapper responsibility / limitation |
|---|---|---|
| **Assemble** | `account_close_assembler.assemble(...) -> (package, sources, report)` consumes `SourceFile` objects plus explicit account, inception, close/predecessor, calendar/policy, report timezone, attestations and account-state inputs. Emits `account_close_package/v3`; library does not sign or accept. [assembler, lines 1–49, 144–199][ASSEMBLE] | Load an explicit private manifest, hash/read original bytes, call the library and retain canonical package plus figures-free report. No CSV regeneration. Caller-supplied timezone and query assumptions need independent source acceptance. |
| **Challenge** | `BookAccountOwner.issue_settlement_challenge(scope, target_session_id, proposed_session_id, package_sha256, calendar, now)` supplies actual permission/generation to the attached store inside the unified transaction. Store binds account, boot, predecessor, policy/calendar, scope and package; 300 s lifetime, also target risk-add cutoff for current scope. [owner, lines 633–647][OWNERSET] [store, lines 620–673][CHALLENGE] | Request only after evidence capture and package review; expose expiry and hash for operator review. Never accept caller-provided boot/generation as authority. |
| **Sign** | `settlement_signing.signing_envelope(challenge, signed_at=aware_datetime)` validates unsigned v2 shape and adds UTC `operator_signed_utc`. **It does not cryptographically sign.** `canonical_bytes` supplies the exact Ed25519 message; existing owner note shows the operator-device signing step. [signing, lines 1–18][SIGN] [owner note, lines 71–105][SIGNNOTE] | Prepare immutable envelope bytes immediately before operator signing; import detached signature and public key ID. No private-key argument or automatic signing. |
| **Submit** | `BookAccountOwner.submit_settlement(envelope, signature, key_id, package, sources, calendar, now, on_halt=None)` delegates to `SettlementStore.submit` within the single writer boundary. Store verifies signature, chronology, unchanged challenge/package, predecessor and original-byte calculation; success atomically retains package, source bytes, event, chain and receipt. [owner, lines 649–671][OWNERSET] [store, lines 679–817][SUBMIT] | Re-read/re-hash frozen input files, pass exact bytes once, retain receipt privately, surface the original refusal and halt requirement. No retry loop. |
| **Status** | `SettlementStore.status()` is a read-only validated projection: phase, restore/invalidated flags, row count, head, and false activation/resume grants. `BookAccountOwner.status()` reads owner state and binding. [store, lines 922–950][STATUS] [owner, lines 999–1014][OWNERSTATUS] | Combine safe summaries; retain full account/financial fields privately. A matching head session/package can reconcile an immediately lost reply; **status is not a receipt-ID lookup API** and cannot prove an arbitrary older package is current. Unresolved outcomes go to the owner. |
| **Anchor / restore** | `SettlementStore.bootstrap_b7(...)`, `reconcile_restore(now)`, and reviewed revision/resolution paths already exist. H6 records that the account owner has no direct wrapper for these and its existing integration tests call the attached store. [store, lines 468–504][RESTORE] [H6 card, lines 50–59][H6CARD] | Prerequisites or separately authorized recovery; exclude bootstrap/reset/reseal/resolve commands from this minimal forward workflow. Reuse H6 for reconstruction traces. |

**Process-lifetime trap:** `BookAccountOwner.boot` on an existing store rotates boot/generation, halts and invalidates bootstrap state; `open_settlement` calls `SettlementStore.boot`, whose restart marks outstanding challenges `VOIDED_RESTART` and sets restore-pending. Therefore five independent command invocations that each boot/open the store cannot implement the intended sequence. `status` must not secretly open a new settlement owner. A restart is explicit recovery, followed by a fresh reviewed challenge where appropriate. [owner, lines 375–454][BOOT] [owner, lines 613–631][OWNERSET] [store, lines 375–477][STOREBOOT]

## 2. Smallest implementation proposal

### 2.1 File footprint and process contract

Proposed new files only:

1. `ops/c1_rail/settlement_operator.py` — private manifest adapter, `OperatorWorkflow` using an injected owner/calendar, offline `assemble`/`prepare-sign` entry points, and the persistent `run_session(...)` command loop. Placing it in `ops` avoids a new governance-layer `tools`/`scripts` import exception; H6 already flags that distinction. [H6 card, lines 157–166][H6CARD]
2. `tests/ops/test_settlement_operator.py` — wrapper-specific synthetic cases in §4, importing existing synthetic generators and integration helpers without editing them.

**Neither proposed file, command nor new test has been implemented by this task.** `BookAccountOwner.boot()` and `open_settlement()` already exist in consumer code; the reviewed sources do not establish an accepted persistent operator-facing production composition. The proposed wrapper itself does not construct or boot an owner. Its initial proof is synthetic until an approved operational composition and operator signing procedure exist; an API facade cannot establish operational closure.

No existing source/test edits, new durable database/schema, HTTP service, account API, broker transport, key backend or production host wiring. The wrapper is not imported by the listener or trust-domain modules. Its fixture supplies an already booted owner; a real composition must be named under D3. If that composition cannot be supplied without changes, return its **exact missing adapter path and owner**, not a second standalone store or a made-up binding. This two-file slice yields a reviewable operator protocol plus synthetic implementation evidence; it does not by itself complete operational T07 acceptance.

### 2.2 Proposed command contract (not commands available today)

Offline entry point: `python -I scripts/fp.py python -m c1_rail.settlement_operator <command>`. Owner-bound verbs run inside the **same** `run_session(...)` process. Suggested shell-style command vocabulary:

```text
assemble --manifest <private-input.json> --out-dir <new-private-package-dir>
challenge --package-dir <private-package-dir> --scope submit_account_close --target-session <next-session> --out <challenge.json>
prepare-sign --challenge <challenge.json> --out <envelope.json>
submit --package-dir <private-package-dir> --envelope <envelope.json> --signature <signature.bin> --key-id-file <public-key-id.txt> --receipt-out <receipt.json>
status --out <private-status.json>
```

- `assemble` and `prepare-sign` may run without an owner. `challenge`, `submit`, `status` require the injected owner and attached store; a standalone invocation refuses `owner_session_required`, without creating/opening state. No `--owner-db` auto-boot shortcut.
- Manifest inputs map one-for-one to `assemble`/`SourceFile`: explicit source roles, safe relative filenames, original-byte SHA-256, account observed for each source, capture UTC, cash query labels/completion, inception, session/predecessor, calendar/policy identity, report timezone and required typed observations/attestations. Values stay in private files, never CLI arguments. Retain separate reviewed S2 evidence references in a sidecar; do not add fields to the settlement package or treat the sidecar as broker authentication.
- Before challenge, the coordinator-accepted source review and continuity decision must be available locally. Missing/unresolved S2 facts stop the operator procedure. A wrapper can check that a reference is present and matches bytes; it cannot decide that an undocumented broker semantic is true.
- `prepare-sign` uses the current aware operator-device clock and existing canonicalization. Joshua reviews package and challenge, then signs **those bytes** on his device. Preserve envelope, signature and key ID unchanged. A delay beyond expiry requires fresh review/challenge/signing; no timestamp patching. Real signer command is D4's remaining input, not an invented command here.
- Historical catch-up is explicit `--scope record_only`, with **no target**; delegate its HALTED, predecessor order and venue close-equity requirements unchanged. No automatic fallback from current scope to record-only.
- Retain full outputs in a verified private root; require collision-free new output paths and atomic complete writes. Reject path escape/symlink escape, duplicate manifest JSON keys, duplicate source names and output-over-input. Verify ignoring for repository-local private roots; `local_artifacts/` must not be assumed ignored (CAP found it unignored at its pass). [CAP, lines 531–534][CAP]
- Public console/log output: stage, package/envelope digest, accepted/refused/unknown result, safe refusal code, `halt_required`, and private artifact digest. Do not echo raw exception messages containing filenames, transaction IDs, account values or CSV rows. Owner receipts and status contain equity/account data; do not print their representations.
- The loop uses UTC wall time for protocol chronology and monotonic time for duration. It does not cache authority, change permission, invoke broker sends, or perform restore/boot automatically. After an uncertain submit, stop and inspect status; never resend to discover whether it worked.

### 2.3 Refusal and exit behavior

Proposed wrapper exit classes: **0** command completed (submission accepted only if `Receipt`); **2** input/assembly/preflight refusal; **3** consumer `Refusal`; **4** owner/storage failure or uncertain completion. Within a persistent session, return the same code in the per-command result. Source/private details stay in private output. These wrapper classes do not rename consumer reasons or change durable effects.

Preserve, for example, `restore_reconciliation_required`, `chain_not_seated`, `chain_invalidated`, `record_only_requires_halted`, `target_cutoff_passed`, `unknown_key_or_scope`, `bad_signature`, `challenge_mismatch`, `challenge_consumed`, `challenge_expired`, `stale_boot_generation_or_digest`, `evidence_changed`, `predecessor_advanced`, `duplicate_settlement`, and chronology/source refusals. Do not promise “no writes on every refusal”: correction detection may durably quarantine evidence and halt, and expiry/refusal events may persist. Refusal must not advance an accepted close. Preserve `halt_required`; notification failure must not hide committed quarantine. [challenge/submit][CHALLENGE] [submission/refusal effects][SUBMIT] [contract, lines 194–212][CONTRACT]

## 3. Source-evidence closure packet

### 3.1 Current-regime checklist — independent facts and private evidence

Every row below is **OWED IN THE PUBLIC RECORD / PRIVATE STATUS UNKNOWN**, except the explicitly dated existing evidence. Absence in this cloud checkout does not prove that Joshua lacks the private confirmation. Original records, exact transaction IDs and financial/account values remain on the operator's machine. Public return uses manifest hashes and dispositions only.

| Order / obligation | Smallest sufficient evidence to inspect locally | What does not discharge it |
|---|---|---|
| **1. Qualifying target binding** | Joshua's private binding for one **completed** qualifying preservation trade, its original record/transaction identity, event time, post-rollover discrimination and R3 zone-explicit counterpart; return binding-manifest SHA-256. Reuse the Oct 2 binding if already supplied. The public record says due during 10-05→10-09 and hash OWED; that is not a finding that the operator failed. [§2.4][TARGET] | An undated screenshot, approximate time/amount match, or an invented target hash. “After 17:00 ET” must mean an actual tradable post-reopen event, e.g. Mon–Thu after 18:00 ET, not the 17:00–18:00 break. No new trading activity merely to obtain evidence. |
| **2. S5 / chain continuity first** | Reconfirm any accepted owner/B7 location and retained receipt since the **2026-09-24** bounded “no accepted chain” attestation/search. If a chain now exists, use its exact accepted predecessor. If still none, coordinator records the initial-B7 route. Retain the bounded search scope and any uninspected locations. [T07, lines 20, 43][T07] [CAP, lines 540–552][CAP] | Calling the historical search a fresh global proof; treating the old rehearsal database as production; silently starting over. |
| **3a. S2 / R3 — Cash History `Timestamp` zone and offset** | Original Cash History row matched by **exact transaction ID** to an admissible zone-explicit source instant for that same event, with source/export capture times, report surface, timezone setting and original-byte hashes. Record raw naive timestamp, reference `Z`/numeric offset, derived numeric offset at that instant and separately the proposed IANA zone/rule. Coordinator accepts the mapping and option-b admissibility if used. [CAP, lines 582–586][CAP] [R3 read][READS] | UI `CDT`, ticker preference, admin API offset parameter, a merely nearby alert, or an order receipt timestamp assumed equal to the cash transaction event. One offset does not uniquely identify an IANA zone or prove another DST regime. |
| **3b. S2 / R1 — Cash History `Date` meaning** | Authoritative definition for this exact report, or discriminating post-rollover row whose calendar date and session/trade date differ: original exports covering both dates and accepted source/session comparison (`tradeDate` if available). Retain explicit account-session/calendar mapping, including holidays where relevant. [CAP, lines 587–592][CAP] | Ordinary daytime row; inference from Account Balance History `Trade Date` (a different field/report); blindly using CSV `Date` as the account-session key. |
| **3c. S2 / R2 — query-bound clock AND inclusivity** | Preserve entered labels, timezone, request/capture time, filters and completion state; export calendar-date-only and session-date-only queries for the same discriminating transaction, plus both-date control. Separately establish start/end inclusion with authoritative report-specific wording or retained queries/edge rows that distinguish competing endpoint rules. Record lower and upper behavior separately, overlap and UTC spans. [CAP, lines 593–599][CAP] [R2 read][READS] | The R2 two-single-day comparison can discriminate a date clock but need not prove either endpoint's exact inclusion. No rows near an edge is inconclusive. Empty CSV is not proof of no activity. Do not trade to generate edge rows. |
| **4. S1 / inception and full coverage** | Lifecycle inception evidence; original account-wide bounded Cash History windows from inception through capture with overlaps, query completion including empty ranges, Account Balance History, and comparison against retained old inventory. Classify nominal establishment funding, transaction-linked costs, other adjustments, revisions, additions and deletions under existing consumers. Demonstrate the chosen query range, including the existing 14-day cap, on this report. [contract, lines 53–87][CONTRACT] | First zero-P&L row as inception; an annual request assumed complete; matched totals without original bytes; net-zero adjustments; treating the code's cap or cost strings as vendor documentation. |
| **5. S3 / initial B7** | Where no accepted chain is reconfirmed: E1 dashboard, E2 account-wide flat/no-working-order evidence, E3 inception-backed history, source captures and authenticated seal/tool hashes under the existing C1–C10 procedure. Retain parseable E3 with explicit accepted report timezone for the first later close. [B7][B7] [contract, lines 76–82][CONTRACT] | A fabricated earlier anchor, inferred peak, or promoting a disposable rehearsal seat into production. A historical rehearsal does not supply fresh B7/n3 evidence at release. |
| **6. S3 / subsequent close or flatness** | Exact effective account close and predecessor; venue close equity with valuation basis, or the permitted balance plus evidence of flatness at **that boundary**. For the assembler's current-close route: complete history, current flat/no-working-order captures and no later fills; historical `record_only` requires its separate close-equity source and venue balance row. Capture dashboard after its relevant update and reconcile it. [assembler, lines 77–131][ASSEMBLE] | Later empty positions alone, current marks reconstructing past equity, or assumed daily flatten. Historical exporter-equivalence evidence cannot replace fresh close-supporting reports. |
| **7. S4 / actual original-byte consumers** | On the operator machine after source acceptance: original-byte anchor and subsequent-close traces through existing verifier and unified owner, exact package/predecessor hashes, challenge, signature/receipt references, `settled_close` consumer result, correction refusal and restore outcome in disposable rehearsal stores. Reuse the H6 procedure if built; preserve originals and mutate only disposable derivatives for negative cases. [T07, lines 23–29][T07] [H6][H6] | A generated package accepted on synthetic bytes; a signature over unsupported facts; original-byte assembly without actual verifier/owner consumption; rewriting originals to make a test pass. |
| **8. Procedure / operator timing** | Record export start/end, source publication if supplied, capture per source, review, challenge issue, actual signing, server receipt/status and total operator elapsed time. Record timezone-aware wall times and step durations. Assess the existing **30-minute freshness**, **300-second challenge** and risk-add cutoff bounds, plus B7's separate limits; report blocked/expired honestly. [contract, lines 134–188][CONTRACT] | Machine-test duration as operator effort; predicted signing time; backdated receipt; a successful HTTP reply or elapsed time as broker finality. |
| **9. Second regime / T16** | Retain current-regime acceptance separately. After 2026-11-01 obtain the qualifying R3 second-regime observation under the standing operator procedure and coordinator acceptance, unless D7 is expressly re-ruled. Prefer existing qualifying records/reads; no extra trade requirement is introduced. [calendar gate][CAL] | Synthetic fall-back case, historical export alone, current-regime acceptance, or an assumed November 1 release date. |

**Code assumptions are not source facts.** `parse_cash_windows` admits rows by `Timestamp`'s local calendar date within inclusive UI labels, using a caller-provided `ZoneInfo`; it parses `Date` separately. The assembler converts those labels to UTC midnight-to-next-midnight spans capped at capture. `verify_history_coverage` checks those spans and bound sources. Existing tests verify that consumer convention, including a fall-back window; none establishes Tradovate's undocumented filter/export semantics. A contradictory source finding returns to the owner before any code fix or signing. [evidence, lines 147–221][PARSE] [coverage, lines 304–353][COVERAGE] [assembler, lines 135–141][ASSEMBLE] [tests, lines 39–44 and 126–140][TIMETEST]

### 3.2 Narrow dual-regime evidence-equivalence proposal (not an exemption)

The useful hypothesis is limited: **the same identified report exporter, configuration and timestamp rule interpret the same broker event consistently in both regimes**. If Joshua later identifies original historical broker records, a local reviewer could assess this without new trading. Their existence, completeness, private location and suitability are **UNKNOWN here**; no archive was inspected.

For each proposed regime, retain a private row-level evidence tuple:

```text
report-original SHA-256 + capture UTC + report/exporter/version/settings evidence
exact Transaction ID + raw Cash History Timestamp + raw Date
reference-original SHA-256 + source/field identity + same exact Transaction ID
reference event instant with explicit zone/offset + reference capture UTC
computed event-offset result + Date/query findings kept separate
```

The reference must timestamp the **same event**, not merely the same order or a nearby notification. Resolve any order-ID-to-cash-ID linkage explicitly; without an exact evidenced link and time-field meaning, return UNPROVEN. Retain token-free original business response bytes; strip credential-bearing transport material before retention. A transformed business payload is a derivative with disclosed provenance, never silently labelled the original. Browser-source admissibility remains the coordinator's.

Distinguish two independent axes:

| Evidence available later | Narrow claim it can support | Residual |
|---|---|---|
| October export containing historical winter and summer event rows, each exactly matched to zone-explicit originals | Event-date conversion in **that October capture** for those rows, if offsets discriminate the alternatives | Does not exercise exporter-at-capture behavior in the standard-time regime. |
| Original export actually captured in a prior standard-time regime, with its exact-ID source reference and settings/version provenance | Historical standard-time capture behavior on that surface/version | Does not establish that the current exporter/configuration is equivalent or unchanged. |
| Originals captured in both regimes, ideally re-exporting an identical event across captures, with exact references and accepted continuity of interface/version/settings | Stronger evidence separating event-time conversion from capture-time offset, browser locale/zone or exporter changes | Observational scope remains bounded; it still does not itself supersede the dated repeat. |

**Proposed use now:** accept qualified historical pairs only as supporting S2 interpretation/reconstruction evidence with their exact scope recorded. Do not count them as fresh settlement source files or as closure of the current target, `Date`, query bounds, B7 or T16. A historically dated event processed by Python `ZoneInfo` is not evidence about the broker exporter.

**Only if requesting substitution later:** submit the two-regime tuple inventory, interface/version/settings continuity argument, competing explanations eliminated (event-time zone versus fixed/capture-time offset), remaining uncertainty, and the exact Oct 2/§CAL condition to be replaced. Joshua must explicitly accept that equivalence and supersede the dated-repeat requirement; the coordinator then records it at the existing owners. If original provenance, a regime, continuity or exact linkage is absent, reject equivalence and perform the standing repeat. This is a possible decision request, not a conclusion that historical evidence is sufficient. [Oct 2 ruling][TARGET] [binding calendar condition][CAL]

## 4. Named synthetic acceptance and reuse

**Hypothesis:** N/A — implementation of existing consumer behavior, not a new settlement law. **Accept if** the wrapper composes those consumers unchanged and each named boundary below is demonstrated. **Reject if** it creates authority, reboots between challenge/submit, masks a consumer refusal, or treats synthetic data as broker-semantic evidence. **Revert trigger:** any edit outside the two admitted files, an owner-ledger/acceptance change, or required weakening of a bound consumer.

Proposed new nodes in `tests/ops/test_settlement_operator.py` (names frozen before dispatch):

| Node | Required falsification case |
|---|---|
| `test_one_owner_session_accepts_exactly_one_synthetic_close` | Assemble → challenge → prepare-sign → disposable fixture signer → owner submit → status; one receipt/head advance, matching package and unchanged permission. Use existing B7/owner fixtures. |
| `test_commands_never_boot_or_reattach_owner` | Spy on boot/open: zero calls by every verb; no injected owner yields `owner_session_required` and no database. |
| `test_changed_original_or_package_after_challenge_refuses` | Change one bound source byte or canonical package byte; no acceptance; original consumer reason preserved when reached. |
| `test_expiry_and_signed_chronology_are_not_extended` | Submit at expiry, sign before issue, sign after receipt, alter signed field; fail using existing chronology rules; prepare-sign cannot renew the challenge. |
| `test_refusal_preserves_durable_halt_and_safe_output` | Signed historical correction through the actual owner returns the named halt-required refusal; quarantine survives notification/output failure; no accepted-close advance. |
| `test_record_only_requires_halt_and_no_target` | Explicit historical scope with target or non-HALTED owner refuses; missing historical close-equity evidence refuses; no scope fallback. |
| `test_lost_submit_reply_uses_status_without_resend` | Discard committed reply, inspect matching head; no second submit/challenge, no second receipt; unresolved/mismatched head reports unknown. |
| `test_private_io_rejects_aliases_and_redacts_output` | Path/symlink escape, duplicate JSON keys/names, source/output collision, missing original hash and failed write refuse; account/financial/transaction text and raw source paths absent from console. |
| `test_report_semantics_are_explicit_not_defaults` | Missing timezone/source-review references cannot proceed toward challenge; a syntactically valid reference is labelled a prerequisite, not automatic source qualification. |
| `test_workflow_has_no_broker_or_activation_side_effect` | Broker-send and activation/resume spies remain untouched on success, refusal and error; no real key loader exists. |

Reuse these **existing** nodes/fixtures; do not recreate their coverage:

- `test_account_close_assembler.py::test_exports_reconcile_into_a_package_the_verifier_and_consumer_accept`, `::test_overlapping_windows_dedupe_by_id_and_revisions_refuse`, `::test_export_row_and_window_order_do_not_change_the_collected_ledger` (lines 119, 152, 169). [assembler tests][ASSEMBLETEST]
- `test_account_close_evidence.py::test_full_window_binding_survives_fall_back`, `::test_query_coverage_uses_report_timestamp_not_cme_business_date` (lines 39, 131). [time tests][TIMETEST]
- `test_book_settlement.py::test_restart_begins_restore_pending_voids_open_challenges_and_keeps_the_chain`, `::test_crash_before_commit_accepts_nothing_and_a_restart_needs_a_fresh_challenge`, `::test_lost_receipt_after_commit_is_read_only_and_a_fresh_resubmission_refuses` (lines 358, 382, 410); `::test_revision_of_an_accepted_record_invalidates_dependents_and_halts`, `::test_defective_packages_are_refused_by_name_without_state_advance` (lines 328, 686). [settlement tests][SETTEST]
- `test_account_close_calculation.py::test_source_history_correction_cannot_hide_behind_unchanged_inventory_claims`, `::test_retained_source_deletion_requires_halt_even_with_stale_claimed_counts` (lines 205, 249). [calculation tests][CALCTEST]
- `test_book_owner_settlement_integration.py::test_signed_synthetic_close_flows_through_unified_owner_into_listener_sizing` (line 176), using the existing disposable `Operator`, `seat`, `package`, `binding` helpers. This is synthetic consumer evidence, not a production transport. [integration test][INTEGTEST]

The T07 return records **325 passed** at `31502c6` plus its then-working changes, with `.cache/fp-verification/20260924T163613Z-4fee32191553/record.json`. That is a **source-reported prior result**, not a fresh run or inspected record here. This document-only task does not rerun settlement, ops, qualification, Linux or cloud suites. At implementation, run the new wrapper nodes and the unchanged related nodes above through the launcher; satisfy the coordinator's required gates without duplicating H6's broad evidence campaign. Accepted G10/Q7 and other evidence remain preserved. [T07, lines 46–51][T07] [checklist G10/Q7][PRESERVE]

## 5. Boundaries

- This task changes only this proposal. Its isolated commit/push and documentation-only draft PR are authorized by Joshua's publication instruction above. No production code, governing card, acceptance rule, ledger or private evidence changes; no merge or implementation dispatch.
- No private archive inspection, broker connection, live acquisition, credentials, signing-key access, provider outreach, spending or Azure provisioning. No additional trade to create evidence.
- A source mismatch is a finding for the coordinator, not a repair through changed timezone defaults, CSV rewriting, alternate scope, reseal or reset.
- Preserve completed G10/Q7 and other accepted evidence. Feed policy and CP-7 collection readiness remain with the sibling session; this packet supplies no feed decisions.

## 6. Return and completion criteria

**Proposal return: DONE_WITH_CONCERNS.** The reviewable proposal, source pins, public ownership refresh, wrapper boundary, evidence checklist and next handoffs are complete. This author status is not coordinator acceptance. Concerns are the exact unresolved decisions in §0.5 and private evidence unknowns in §3, not an assertion that private evidence is absent.

Future implementation return uses **DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED**. `DONE` requires the admitted two-file diff, source/base identity, named tests with completed launcher records, safe synthetic sample outputs, and no production-side effects. Proposed coordinator build disposition: **RESOLVED** only when those checks and §4 pass; **FALSIFIED** if a required consumer property fails. `NEEDS_CONTEXT` means missing owner composition/signing interface or an unresolved admission; `BLOCKED` names a capability/scope/plan conflict. Code acceptance does not qualify CAP rows. Local evidence closes a row only with its specific source/consumer proof and coordinator disposition; otherwise leave it UNPROVEN with the producer fact named.

## 7. Smallest next handoffs to the existing coordinator

### 7.1 Local evidence inventory first (no new collection implied)

Give Joshua/the existing local settlement executor this bounded request, under the existing privacy limits:

> Identify already retained T07 target confirmation and original records only in the authorized local locations; do not search new private archives or perform new account actions. Return a private index with: (1) target-binding SHA-256 and qualification facts; (2) separate R3 Timestamp, R1 Date and R2 query-clock/endpoint evidence references; (3) current accepted-chain/predecessor status or bounded confirmation of the initial-B7 path; (4) inception, E1/E2/E3 and subsequent-close/flatness availability; (5) any existing original-byte consumer trace and operator timing record; (6) any historically captured second-regime originals, labelled optional and unverified until reviewed. For every missing item say UNKNOWN/NOT LOCATED IN THE INSPECTED SCOPE. Return to the coordinator only manifest hashes, row dispositions, inspected-scope description without private paths, and exact missing fact. Stop on unsupported decisive semantics; continue independent inventory. Do not obtain additional trades, credentials or new account data to fill gaps.

This first handoff need not wait for the wrapper. It can reveal already completed operator work without asserting its absence. If a qualifying source is unavailable, return the smallest further operator collection request under T07/H6. Original-byte rehearsal follows only when its source prerequisites and local scope are satisfied; use disposable stores and the existing H6 owner. A real review/sign/submit session is distinct from this inventory.

### 7.2 Executable implementation scope after D1–D5

Coordinator dispatch text, to be frozen with the actual writer/base and D3 composition decision:

> Build only `ops/c1_rail/settlement_operator.py` and `tests/ops/test_settlement_operator.py` as §2 specifies. Start from refreshed main after checking all current PRs and local writer reservations. Import the unchanged assembler, signing-envelope/canonicalization helpers and attached owner methods; use an injected owner for the persistent session, with synthetic fixture composition only in tests. Implement safe private file handling and the command/refusal contract. Reuse existing synthetic fixtures. Do not add production host wiring, B7/reset/recovery commands or a private-key backend. Write and verify §4 wrapper cases, then run the selected existing related cases unchanged. Return the two-file patch, exact source hashes/revision, command/interpreter/record IDs and any missing operational composition interface. Stop if existing code, a frozen rule or another writer's file must change.

The test invocation is small and executable once those two files exist:

```bash
python -I scripts/fp.py doctor
python -I scripts/fp.py python -m pytest tests/ops/test_settlement_operator.py
python -I scripts/fp.py python -m pytest \
  tests/ops/test_book_owner_settlement_integration.py::test_signed_synthetic_close_flows_through_unified_owner_into_listener_sizing \
  tests/ops/test_book_settlement.py::test_crash_before_commit_accepts_nothing_and_a_restart_needs_a_fresh_challenge \
  tests/ops/test_book_settlement.py::test_lost_receipt_after_commit_is_read_only_and_a_fresh_resubmission_refuses
```

Run the rest of §4's named related nodes where the touched wrapper boundary consumes them; do not rewrite or rerun broad suites merely to claim readiness. Coordinator freeze review precedes any private operational evidence. Two failed corrections of the same issue return to the coordinator per AGENTS.md. Build record must name tested working-tree state, interpreter, exit, capture/source stability and record path; synthetic machine durations are labelled as such.

## 10. Verification

Document checks only; no consumer tests executed for this proposal. `python -I scripts/fp.py doctor` succeeded: `/workspace/first-passage/tmp/ops-env/bin/python`, Python **3.12.14**, 62 locked packages matched. Verification commands:

```bash
git rev-parse HEAD origin/main origin/pr-788
git diff --check
git status --short
python -I scripts/fp.py python scripts/check_brief.py --type handoff docs/notes/2026-10-11-t07-operator-workflow-readiness-PROPOSAL.md
python -I scripts/fp.py check
rg -n 'Binding hash: OWED|T07-TARGET' docs/notes/2026-09-27-route-commissioning-session-packet.md
rg -n 'post-November-1|repeat after 2026-11-01|Initial T07 acceptance' docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md
```

**Initial document results (2026-10-11 19:16 UTC):** `check_brief.py --type handoff` returned **well-formed, 0 HARD / 0 WARN, exit 0**. A read-only consistency check through the same launcher verified **30 pinned source links and line ranges, 30 reference labels, six production-file hashes, and all 13 cited existing test definitions** using `git show`, SHA-256 and AST reads; it returned `CONSISTENT`, exit 0. Whitespace and sole-changed-file checks passed. Those documentation commands emitted no automatic `record.json`.

**Publication validation:** rerun the brief/citation/scope checks on this updated file and the repository's supported `fp.py check` gate composition; retain its printed `record.json`, interpreter, source-stability/capture result and actual exit in the PR body/task return. Installed pre-commit/pre-push hooks remain enabled. No full engineering suites are selected. These checks validate documentation/repository consistency, not broker semantics, operational readiness or T07 acceptance. Before reuse, refresh main/PR ownership and recheck D1–D7; this packet's immutable pins remain the source for what was inspected here.

[T07]: https://github.com/Joshua-Asante/first-passage/blob/b6fff029678992f753111134e30f94d85dd3b80b/docs/briefs/handoffs/2026-09-21-tradeify-t07-manual-settlement-procedure.md#L1-L64
[CAL]: https://github.com/Joshua-Asante/first-passage/blob/b6fff029678992f753111134e30f94d85dd3b80b/docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#L853-L865
[TARGET]: https://github.com/Joshua-Asante/first-passage/blob/b6fff029678992f753111134e30f94d85dd3b80b/docs/notes/2026-09-27-route-commissioning-session-packet.md#L207-L219
[CAP]: https://github.com/Joshua-Asante/first-passage/blob/b6fff029678992f753111134e30f94d85dd3b80b/docs/briefs/phase4-preparation/2026-09-16/capability-decision.md#L522-L602
[CONTRACT]: https://github.com/Joshua-Asante/first-passage/blob/b6fff029678992f753111134e30f94d85dd3b80b/docs/spec/2026-09-15-tradeify-attended-settlement-contract.md#L18-L248
[B7]: https://github.com/Joshua-Asante/first-passage/blob/b6fff029678992f753111134e30f94d85dd3b80b/docs/spec/2026-09-12-tradeify-account-snapshot-seal-contract.md#L24-L56
[READS]: https://github.com/Joshua-Asante/first-passage/blob/b6fff029678992f753111134e30f94d85dd3b80b/docs/notes/2026-09-25-t08-drills-t07-reads-operator-session.md#L61-L74
[H6]: https://github.com/Joshua-Asante/first-passage/blob/b6fff029678992f753111134e30f94d85dd3b80b/docs/briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md#L411-L446
[H6CARD]: https://github.com/Joshua-Asante/first-passage/blob/b6fff029678992f753111134e30f94d85dd3b80b/docs/briefs/handoffs/2026-10-02-h6-reconstruction-rehearsal-harness-DRAFT.md#L1-L166
[PL2]: https://github.com/Joshua-Asante/first-passage/blob/4edf5648c10dc1e9ab05037f7dac3e62f1929456/docs/briefs/handoffs/2026-10-11-live-size-vector-p-l2-owner-binding-card-DRAFT.md#L309-L320
[TRUST]: https://github.com/Joshua-Asante/first-passage/blob/b6fff029678992f753111134e30f94d85dd3b80b/ops/c1_rail/qualification/trust_domain.py#L140-L184
[ASSEMBLE]: https://github.com/Joshua-Asante/first-passage/blob/b6fff029678992f753111134e30f94d85dd3b80b/ops/c1_rail/account_close_assembler.py#L1-L199
[PARSE]: https://github.com/Joshua-Asante/first-passage/blob/b6fff029678992f753111134e30f94d85dd3b80b/ops/c1_rail/account_close_evidence.py#L134-L221
[COVERAGE]: https://github.com/Joshua-Asante/first-passage/blob/b6fff029678992f753111134e30f94d85dd3b80b/ops/c1_rail/account_close_evidence.py#L304-L353
[OWNERSET]: https://github.com/Joshua-Asante/first-passage/blob/b6fff029678992f753111134e30f94d85dd3b80b/ops/c1_rail/book_account_owner.py#L613-L687
[OWNERSTATUS]: https://github.com/Joshua-Asante/first-passage/blob/b6fff029678992f753111134e30f94d85dd3b80b/ops/c1_rail/book_account_owner.py#L999-L1014
[BOOT]: https://github.com/Joshua-Asante/first-passage/blob/b6fff029678992f753111134e30f94d85dd3b80b/ops/c1_rail/book_account_owner.py#L375-L454
[STOREBOOT]: https://github.com/Joshua-Asante/first-passage/blob/b6fff029678992f753111134e30f94d85dd3b80b/ops/c1_rail/book_settlement.py#L375-L477
[RESTORE]: https://github.com/Joshua-Asante/first-passage/blob/b6fff029678992f753111134e30f94d85dd3b80b/ops/c1_rail/book_settlement.py#L468-L504
[CHALLENGE]: https://github.com/Joshua-Asante/first-passage/blob/b6fff029678992f753111134e30f94d85dd3b80b/ops/c1_rail/book_settlement.py#L620-L673
[SUBMIT]: https://github.com/Joshua-Asante/first-passage/blob/b6fff029678992f753111134e30f94d85dd3b80b/ops/c1_rail/book_settlement.py#L679-L817
[SIGN]: https://github.com/Joshua-Asante/first-passage/blob/b6fff029678992f753111134e30f94d85dd3b80b/ops/c1_rail/settlement_signing.py#L1-L18
[SIGNNOTE]: https://github.com/Joshua-Asante/first-passage/blob/b6fff029678992f753111134e30f94d85dd3b80b/docs/notes/2026-09-15-account-close-owner-component.md#L71-L105
[STATUS]: https://github.com/Joshua-Asante/first-passage/blob/b6fff029678992f753111134e30f94d85dd3b80b/ops/c1_rail/book_settlement.py#L922-L950
[TIMETEST]: https://github.com/Joshua-Asante/first-passage/blob/b6fff029678992f753111134e30f94d85dd3b80b/tests/ops/test_account_close_evidence.py#L39-L140
[ASSEMBLETEST]: https://github.com/Joshua-Asante/first-passage/blob/b6fff029678992f753111134e30f94d85dd3b80b/tests/ops/test_account_close_assembler.py#L119-L184
[SETTEST]: https://github.com/Joshua-Asante/first-passage/blob/b6fff029678992f753111134e30f94d85dd3b80b/tests/ops/test_book_settlement.py#L328-L717
[CALCTEST]: https://github.com/Joshua-Asante/first-passage/blob/b6fff029678992f753111134e30f94d85dd3b80b/tests/ops/test_account_close_calculation.py#L196-L264
[INTEGTEST]: https://github.com/Joshua-Asante/first-passage/blob/b6fff029678992f753111134e30f94d85dd3b80b/tests/ops/test_book_owner_settlement_integration.py#L176-L240
[PRESERVE]: https://github.com/Joshua-Asante/first-passage/blob/b6fff029678992f753111134e30f94d85dd3b80b/docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#L603-L605
