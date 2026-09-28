# M2: rejected-modify semantics for L2(c): documentary determination (2026-09-28)

**Status:** RETURNED for coordinator review. Documentary only. This is **not** a trace, a qualification, an L2(c) acceptance or an edition decision. It accepts, authorizes, qualifies or releases nothing.
**Card:** [M2 handoff](../briefs/handoffs/2026-09-27-m2-modify-semantics.md). **Dispatch revision:** `48c178aa7c2bf9010ad66f28483a4c7c7dd84689` (`origin/main`, which descends from #532's merge `6da1b2b`). The worktree `HEAD` was verified to descend from it before any research. **Executor:** Claude Code (Opus 5.5) in its own worktree of the operator's primary checkout (`.claude/worktrees/first-passage-background-mastery-a17b3c`), branch `claude/m2-modify-semantics`.
**Route examined:** our client → CrossTrade REST `PUT /v1/api/tv/accounts/{account}/orders/{id}/change` → Tradovate `POST /order/modifyorder`, on a working stop child of an OSO bracket placed by CrossTrade `orders/place` with `stopLoss`. That the REST `change` issues `modifyorder` is documented for the webhook `change` command. For REST it is an **inference** from the REST page's "shared dispatcher" wording (MR01; §1.3 F1).

**Result.**
- **None of Q1–Q4 is documented.** All four are `OPEN`; none is `CONFLICTING`. The GC-3 record is `DOCUMENTED` for the existence of broker timestamps on commands and command reports, and `OPEN` on whether they can be compared with our local send time and on how versions are ordered.
- **What is documented:**
  - A Tradovate modify is a request with "no guarantee" of taking effect (MT01, MS01).
  - Its refusal is reported through a command report carrying `commandStatus`, `rejectReason`, a timestamp and an optional `ordStatus` (MT05, MR07).
  - **Tradovate can create an order version for a command it later rejects.** CrossTrade says that version "is not proof that a modification took effect" (Q21, MR05). It also says the snapshot's version-derived price fields "can reflect a subsequently rejected modification" (MS03).
- **What X-2 can actually observe is narrower than its pass criterion.** No documented CrossTrade read returns the order's **effective** price after a rejected modify:
  - the status read and order rows carry no prices (MR10–MR12);
  - the lifecycle returns only the highest-id version, which may belong to the rejected command (MR06, MR05);
  - versions carry neither a timestamp nor a command link (MT06), and the snapshot does not return version ids (MS04).

  X-2 can show that the modify was refused and that the order stayed `Working`. "At its original price" rests on inference (§3).
- **Contradictions:** there is no trace, so there is no trace contradiction. Four documentary items are reported for the coordinator and operator (§4). One of them corrects PR #540: the "only nonterminal orders can be changed" sentence it cites is **NT8-tab** text, and the Tradovate tab has no rejection statement at all (D-1).
- **Card §8 applies:** Q1 is not `DOCUMENTED`, so the GC-2b consequence (Striker and Aegis: OPERATOR DECISION, with alternatives) may be put to the operator now, on this documentary result, before any trace.

---

## 1. Read report

### 1.1 Inputs read

| Input | Used for |
|---|---|
| Card (in full) | Questions Q1–Q4, the GC-3 record, method, output and limits |
| [Drill plan draft](2026-09-26-tradeify-route-drill-plan-draft.md) §2.2 (M2, X-2) and §2.5 (M, the method precedent) | The questions verbatim; X-2's expected identity, pass and fail text |
| [B–D packet](2026-09-26-tradeify-bd-decision-packet.md) GC-2b, GC-3; B-4, B-5, B-8 | Failure consequences; the noop-amend dependency on GC-3 |
| [REST assessment](../briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md) §6 (incl. the unknown-change row) and §6.11 (Gate A A4: L2(c) `K`) | Q-IDs; the accepted "change is Tradovate modify … resolution is by command report (Q21)" reading |
| [T08 handoff](../briefs/handoffs/2026-09-21-tradeify-t08-broker-protection-feasibility.md) §7 | The one-question, one-follow-up vendor-contact limit |
| [CAP-20260916](../briefs/phase4-preparation/2026-09-16/capability-decision.md) N1-c | What L2(c) qualification would need: supported modify and rejection semantics, then an actual trace |
| [Rail spec](../spec/2026-09-12-c1-multi-leg-rail-extension-spec.md) `AMEND`, R-B3 L-2 | L2(c): broker-native atomic modify with the old protection effective until replaced; a cancel/replace cannot satisfy it |
| [Close-semantics M return](2026-09-26-close-semantics-c-a.md) | Method and output shape (card precedent) |

### 1.2 Evidence and method

**Premise check (card §9), reported before research.** Results:
- `HEAD` descends from `48c178a`, and the card at that revision matches the working tree.
- Drill plan §2.2's Questions row is unchanged.
- The close-research index verifies against its pinned digest `8dd20292…`, and all 637 captures verify.
- REST assessment captures: the pinned index prefixes `d069ae7e`/`c0fd2c95` match. `sha256sum -c` gives **218 verified, 0 mismatched**; the card expected 222.
  - The index has 227 lines: 4 comment lines, 5 documented note entries (hash-only references), and 218 file entries.
  - The card's "222 = 227 − 5" counted the 4 comment lines as file entries.
  - Under the card's rule (§0, a contradiction between the card and what the executor reads), the executor did not choose a reading. It put the question to the operator.
  - **Operator ruling 2026-09-28 (in session): "Accept 218; proceed."** Research began only after the ruling.

**Reuse first, read in place in the primary checkout:**
- **R25:** `local_artifacts/t08-rest-route-assessment-2026-09-25/`, cited by Q01–Q30 and by new MR-IDs.
- **R27:** `local_artifacts/crosstrade-close-research-2026-09-27/`, cited by new MT-IDs. It holds the Tradovate OpenAPI schemas embedded in the `api.tradovate.com` bundle, Tradovate partner-docs pages and Tradovate help-centre articles.
- **P28:** `local_artifacts/route-drills-2026-09/vendor-docs/`, the 2026-09-28 public captures of the change, cancel, place, overview and order-types pages (commissioning packet §3.7 closure, C.1, in [PR #540](https://github.com/Joshua-Asante/first-passage/pull/540), not yet merged at the dispatch revision).

**Targeted public retrieval, only for named gaps.** Four URLs were fetched on 2026-09-28 at 04:36:42–04:36:45 UTC, all HTTP 200, with no login and no account access.

| Named gap | Fetched |
|---|---|
| Q1/Q3: Tradovate's own modify endpoint text, current version | Tradovate partner `modify-order` page (MS01) |
| GC-3: whether all versions of an order can be read | Tradovate partner `order-version-dependents` page (MS02) |
| Q1: which read, if any, returns a working order's prices ("limited version enrichment", MR11) | CrossTrade `get-accounts-summary` (the Tradovate accounts snapshot; MS03–MS05) and `get-accounts` (captured, not cited) |

**Currency check.** The five pages the §3.7 closure relies on (P28: change, cancel, place, overview, order types) were compared as tag-stripped text with their R25 captures of 2026-09-25. **All five are text-identical.** Their byte hashes differ because the HTML is regenerated. That is a by-product of this read, and it bears on commissioning packet residual R-3.7a (§6).

**Evidence directory.** `local_artifacts/modify-semantics-2026-09-27/` in this worktree, gitignored (`.gitignore:291`). It holds:
- the four new captures;
- `MANIFEST.tsv` (URL, HTTP code, bytes, SHA-256, capture UTC, file), SHA-256 `8cb975e48cf6f1e80c8dc9de5a3d91a6de186eb84c1985ce91d995e8b8979372`;
- `QUOTE_INDEX.txt` (MR01–MR18 for R25, MT01–MT12 for R27, MS01–MS05 for the new captures), SHA-256 `0aae89ecae95f0b109163f94074739d944117a6669659fa9256057602a790b5a`;
- `SHA256SUMS` over every file.

Each quote-index row gives the root, file, line or character offset, and the file's SHA-256 prefix. The coordinator or operator relocates the directory to the primary checkout's `local_artifacts/` (card §3 item 2).

**Rules applied.**
- NT8 semantics are never read as Tradovate semantics. Where a CrossTrade page has NT8 and Tradovate tabs, the tab boundary was checked; this is what found D-1.
- CrossTrade-managed behavior (field restoration, snapshot enrichment, non-resend) is kept apart from broker-native Tradovate behavior.
- Webhook command text is used for the REST `change` only as a labelled inference.
- An example in a vendor page is not semantics: MT09's example is cited as an example only.
- Silence is recorded as `OPEN`, never as a positive or negative finding.

### 1.3 Documented facts used

| # | Fact | Whose behavior | Sources |
|---|---|---|---|
| F1 | **Webhook (documented):** `change` reads `/orderVersion/deps` "whenever needed" to restore omitted fields, then sends `POST /order/modifyorder`. A fully specified, account-scoped change can skip that version read.<br>**REST (inference):** the REST `change` "changes … a working Tradovate order in place". Its partial changes are completed by "the shared dispatcher" from "the current live order version", which is inferred to be the same dispatcher and broker call | CrossTrade dispatch; the REST mapping is an inference | MR13, MR14; MR01, MR02, MR15 |
| F2 | `modifyorder` requires `orderId`, `orderQty` and `orderType`. It carries `stopPrice` and optional `clOrdId`. It carries "no guarantee that the order can be modified in the way requests. Market, exchange and logical rules apply" | Tradovate native | MT02, MT01, MS01 |
| F3 | **Synchronous result:** `CommandResult` with an optional `failureReason`, `failureText` and `commandId`. Tradovate reports business-level errors as 200-level responses. CrossTrade surfaces a broker refusal as `400 tradovate_rejected` with the broker's reason, and a failed change as `{"success": false, "error": …}`. A successful change returns `api: "modify_order"` with an **empty** `response` object | Tradovate native; CrossTrade envelope | MT03, MT11, MR18, MR03 |
| F4 | **Later reports:** a `Command` (type `Modify`; required timestamp; `commandStatus` including `ExecutionRejected`, `RiskRejected`, `Replaced`) and its `CommandReport`s (required timestamp and `commandStatus`; optional `rejectReason`, `text` and **optional `ordStatus`**). CrossTrade's lifecycle read returns command reports "with `rejectReason` and human-readable text for refused commands", bounded to the last 10 commands. Tradovate's reject reasons include `AnotherCommandPending`, `InvalidPrice` and `TrailingStopNonOrderQtyModify` | Tradovate native; CrossTrade read | MT04, MT05, MR07, MR08, MT12 |
| F5 | **Versions:** an `OrderVersion` holds `id`, `orderId`, `orderQty`, `orderType`, `price`, `stopPrice`, `timeInForce` and a few more. It has **no timestamp and no command reference**. Tradovate exposes all versions of an order (`/orderVersion/deps`). CrossTrade's lifecycle read returns only "the highest-id version". **Tradovate can create a version for a command it later rejects**, and that version "is not proof that a modification took effect" | Tradovate native; CrossTrade read | MT06, MS02, MR06, Q21, MR05 |
| F6 | **Prices in reads:** the status read has no prices ("a Working status alone does not confirm that a requested modification took effect"). Order rows and the single-order read carry no quantity, type or prices. The accounts snapshot enriches prices from at most 20 version lookups, returns no version ids, and its "version-derived fields can reflect a subsequently rejected modification" | CrossTrade reads of Tradovate entities | MR10, MR11, MR12, MS05, MS04, MS03 |
| F7 | **Order state:** `Order.timestamp` is the creation time. `ordStatus` includes `PendingReplace` as well as `Working`, `Suspended` and the terminal states. Execution reports (required timestamp) include `execType` values `PendingReplace`, `Replaced` and `Rejected`. Tradovate's help centre: a `Working` order can be modified or cancelled "at any time before it is filled" | Tradovate native | MT07, MT08, MT10 |
| F8 | **Ambiguity:** "ambiguous order mutations are not blindly resent". For CANCELREPLACE, an ambiguous cancel or placement returns `reconciliation_required` and is not resent. Reconciliation of a change is by command outcomes in the lifecycle | CrossTrade | Q18, MR16, MR05 |
| F9 | **Contrast:** CANCELREPLACE is "guarded cancel then place, not a broker-atomic edit". `change` is described as an in-place modify of the same order id | CrossTrade | Q28; MR01 |
| F10 | **Timestamps:** order and fill list rows carry Tradovate server timestamps. Command, command-report and execution-report entities each carry a required timestamp | Tradovate native; CrossTrade read | MR17; MT04, MT05, MT08 |

---

## 2. Classification

Each row states what the vendor documents, whether it covers a **stop child of a working OSO bracket** (not only a standalone order), and what completion evidence the documents make available (card §3 item 4).

| # | Question (drill plan §2.2) | Class | Documented (source) | Covers an OSO stop child? | Completion evidence the documents make available | Not documented |
|---|---|---|---|---|---|---|
| Q1 | After a rejected modify of a working stop, does the original order stay `Working` at its original price? | **OPEN** | A modify is a request that may not take effect (F2). A refusal is reported synchronously (`failureReason`, F3) or later in a command report (F4). A new version can exist for the refused command (F5) | **No source distinguishes** a bracket child from a standalone order for modify | Command report: `commandStatus`, `rejectReason`, timestamp, optional `ordStatus` (F4). Order status: `Working`, but "a Working status alone does not confirm" a modification (F6). **Effective price: no documented read.** Version-derived fields "can reflect a subsequently rejected modification", the lifecycle returns only the highest-id version, and versions carry no command link (F5, F6) | Whether the order stays `Working`; whether its price stays at the pre-modify value; how the effective version is identified after a refusal |
| Q2 | A version can exist for a command Tradovate later rejects (Q21): what state does the order show in that interval, and after the rejection? | **OPEN** | That such a version can exist, and that it is not proof (F5). `PendingReplace` exists as an `ordStatus` and `execType` value (F7) | Not distinguished | Command reports, with `ordStatus` optional (F4); execution reports with `execType` (F7), which CrossTrade does not expose through the lifecycle read. The lifecycle's version may show the refused request's values (F5, inference from MR05 with MR06; stated directly for the snapshot, MS03) | Which `ordStatus` the order shows during the interval and after; whether `PendingReplace` is used; whether the refused version persists as the highest-id version |
| Q3 | Is an accepted modify atomic, with the old stop effective until the new one is? | **OPEN** | The same order id is modified in place (F1, F9); CrossTrade contrasts this with CANCELREPLACE, which it calls "not a broker-atomic edit" (Q28). `PendingReplace` and `Replaced` values exist (F7) | Not distinguished | An accepted command's report (`commandStatus`, e.g. `Replaced`) and a new version (F4, F5). Neither states when the old trigger stopped being effective | Whether the old trigger remains effective until the new one is in force; any interval without a working stop |
| Q4 | What does a modify with an unknown outcome leave working? | **OPEN** | Ambiguous mutations are not blindly resent; reconciliation is by command outcomes (F8) | Not distinguished | Lifecycle commands and reports, bounded to the last 10 commands; a lifecycle read can be `partial` with sections `unavailable` (MR08, MR09) | What is working after an unknown outcome; whether CrossTrade ever retries a change (the `reconciliation_required` text is scoped to CANCELREPLACE, MR16) |
| GC-3 | Do the command report and the lifecycle or version reads carry broker timestamps or versions that could postdate a send? | **DOCUMENTED** (fields) / **OPEN** (comparability, ordering) | Command, command-report and execution-report timestamps are required fields; list rows carry Tradovate server timestamps (F10). Versions have ids but **no timestamp** (F5) | — | A command-report timestamp can be compared with the recorded local send time only if the clocks are comparable | Whether Tradovate server time is comparable with the local `prepared_at` clock; whether version ids increase with time (CrossTrade orders by "highest-id"; Tradovate does not state monotonicity) |

---

## 3. What X-2 could and could not add

A pass validates only what M2 documents (drill plan §2.2). M2 leaves Q1 undocumented, so **a pass shows only that one attempt did not fail**.

**What a strict X-2 trace can observe with documented reads:**
- the refusal: a `Modify` command with a rejected `commandStatus`, its `rejectReason` and its timestamp (F4);
- the order's status afterwards (`Working`, or not) on a read taken after the send (F6, F7);
- whether a position changed or a fill occurred (fills and fill-reconciled positions; PR #540's §3.7 closure, F-c).

**What it cannot observe directly:**
- **The effective price after the refusal.** The drill plan's pass reads "the stop is `Working` at its original price". No documented CrossTrade read returns that price unambiguously (F5, F6). An X-2 record can support "original price" only by inference: for example, from the version sequence (whose ordering is undocumented, GC-3), or from the absence of any trigger at the refused level.
- **Atomicity of an accepted modify** (Q3), and **an unknown outcome** (Q4). X-2's own "Does NOT establish" row already names both.
- **Other rejection reasons**, and **other symbols or environments**.

**Design observations, for X-2's CP-3 (not applied; the drill plan and packet are read-only here):**
1. X-2's expected identity ends "the stop's lifecycle, status and version, unchanged". A new version after the refused command is **documented as possible** (Q21, MS03), so "version unchanged" cannot be a pass condition, and a new version is not by itself a fail (§4 D-2).
2. The refusal level (`<OP: rejected-modify level>`) decides which refusal channel is exercised. Late risk-layer rejection is documented for **placements** (PR #540's §3.7 closure, F-g) and not stated for modifies. Whatever channel occurs is recorded as observed.
3. A partial change triggers CrossTrade's restore read of "the current live order version". A fully specified change (quantity, order type and stop price) can skip that read on the webhook path (F1; for REST an inference). Which version the restore read uses after a refused modify is not stated (§4 D-3).

**GC-2b decision available now (card §8).** Q1 is `OPEN`. The GC-2b consequence can therefore go to the operator on this documentary result, before any trace: Striker and Aegis, OPERATOR DECISION with alternatives, and no automatic replacement edition (R-EDITIONS, B-8). The alternatives are named in packet GC-2b. They are unchanged here, and none is recommended by this note.

---

## 4. Contradictions found

There is no trace, so there is no trace contradiction. Only a trace contradicts a mechanism. Four documentary items are reported:

- **D-1 (repository text vs vendor tab):** PR #540's commissioning packet cites "Only nonterminal orders can be changed. A terminal order returns an error" as CT-CH's statement on the change surface (§3.7 closure C.4 and C.6). In both the 2026-09-25 and 2026-09-28 captures, that sentence sits in the page's **NT8 tab**, before the Tradovate tab heading (MR04). The Tradovate tab contains **no rejection statement at all**. The packet's conclusion, that the public documentation does not answer GC-2b, stands and is strengthened. The attribution needs correcting by the packet's owner (#540). It is not edited here (card §5).
- **D-2 (drill plan vs vendor semantics):** drill plan X-2's expected identity ("… version, unchanged") conflicts with the documented possibility of a version for a refused command (Q21, MR05, MS03). Returned to the drill-plan owner for X-2's preparation.
- **D-3 (within CrossTrade's documents, unresolved rather than contradictory):** partial changes restore omitted fields "from the current live order version" (MR02, MR15). Separately, version-derived fields "can reflect a subsequently rejected modification" (MS03). Neither text says whether "current live order version" means the last accepted version or the highest-id version. If it is the latter, a partial change sent after a refused modify could carry the refused values forward. That reading is an inference, recorded for the vendor question (§5 item 6).
- **D-4 (repository design note vs vendor text):** the §3.7 closure's X-2 body guidance ("send only the field that changes: `stopPrice`") triggers the restore read that a fully specified change can skip (F1). This is not a contradiction of vendor semantics. It is a design choice that interacts with D-3, returned to X-2's CP-3.

---

## 5. Draft vendor question (for the operator to send; not sent)

Q1 stays `OPEN`, so card §6 item 5 applies. Sending is the operator's decision, including whether it uses the one permitted T08 follow-up (T08 §7). Whether that follow-up has already been used is **UNVERIFIED**.

> **To CrossTrade support: REST `change` on a Tradovate bracket stop.** We place one contract through `POST /v1/api/tv/accounts/{account}/orders/place` with `stopLoss` (one native OSO), then send `PUT …/orders/{id}/change` to move the working stop child. We need documented answers, not a test, on the following. Please say where Tradovate's behavior is involved.
> 1. If Tradovate refuses the change (for example `ExecutionRejected` or `RiskRejected`), does the stop child remain `Working` at its pre-change `stopPrice`?
> 2. After a refused change, which REST read returns the stop's **effective** `stopPrice`? Your docs say version-derived fields can reflect a rejected modification, the lifecycle returns the highest-id version, and `OrderVersion` has no command reference or timestamp. How do we identify the version in force?
> 3. During and after a change, which `ordStatus` does the order show (for example `PendingReplace`), for an accepted change and for a refused one?
> 4. For an accepted change, does the old stop price stay in force until the new one is? Is there any interval with no working stop?
> 5. If a change's outcome is unknown (timeout, 502), what remains working, and does CrossTrade ever retry a change?
> 6. When a partial change omits fields, is "the current live order version" the last accepted version or the highest-id one? On REST, does sending `qty`, `orderType` and `stopPrice` skip the version read, as your webhook table says a fully specified change can?

---

## 6. Limitations

- **No trace.** Every class above is documentary. Nothing here is a `COMMISSIONING_OBSERVATION`.
- **Public and retained sources only.** CrossTrade and Tradovate pages are living documents, and a capture is evidence of the page on its date, not a vendor commitment. Tradovate's schemas were read from two sources: the OpenAPI embedded in the `api.tradovate.com` bundle (R27, captured 2026-09-27) and the partner pages (MS01–MS02, 2026-09-28). They differ slightly: the partner page's `orderType` enum adds `LimitIfTouched`. No class depends on that difference.
- **Inferences are labelled:** the REST-to-`modifyorder` mapping (F1); the lifecycle version possibly showing a refused request (Q2, from MR05 with MR06); D-3's carry-forward reading.
- **Demo versus live:** CrossTrade says Tradovate's Demo environment hosts most prop-firm evaluation accounts (PR #540's §3.7 closure, C.3). Nothing read says whether modify semantics differ there.
- **Community and third-party material was not used.** The close-research set contains some; card §3 item 3 keeps it out of the classification.
- **By-product for commissioning packet residual R-3.7a** (PR #540): the five §3.7 pages are text-identical to their retained 2026-09-25 captures (§1.2). Recording that against R-3.7a is the packet owner's decision. This note does not edit the packet.
- **Relocation owed:** the evidence directory lives in this worktree until the coordinator or operator relocates it.
