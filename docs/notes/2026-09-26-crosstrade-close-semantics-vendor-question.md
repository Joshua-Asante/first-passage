# CrossTrade close-semantics vendor question: final text for the operator (2026-09-26)

**Status:** **FINAL — to be sent by the operator.** Not sent by any agent; no agent contacts the vendor. **Sent:** §1 **not yet sent** to human support. Two chat attempts on 2026-10-01 are recorded in [§4](#4-chat-attempts-2026-10-01-not-a-send-of-1); neither is a send of §1, and the reply was the support chat's AI assistant, not a vendor statement.
**Authority:** operator ruling 2026-09-26, given in session by Joshua through a structured question. He selected "Finalize it for me to send", whose text was Astra's recommendation; it is recorded here as his decision (R-VENDORQ).
**Source:** the draft in the [close-semantics determination](2026-09-26-close-semantics-c-a.md) §6, which stays as drafted. The ruling keeps its nine questions and adds one short request, item 10 below. Nothing else is changed.
**Context:** the investigation of C-a (whole-leg broker liquidation) under the operator's close ruling of 2026-09-26 (R-CLOSE, [incident ADR §A11.1](../adr/2026-09-17-bounded-platform-protection-incident-contract.md#a111--operator-ruling-close-direction-2026-09-26)), investigation only. This is a separate question from the T08 vendor question sent on 2026-09-25 ([campaign §59 Ruling 2](../briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md#ruling-2--the-t08-vendor-question-has-been-sent)).
**Revision 2026-09-27 (operator ruling, in session; governs what is sent):** the operator answered "yes" to switching the vendor message to the updated text. The text to send is now the revised message in [§1](#1-text-to-send-revised-2026-09-27). It is the trimmed per-question message of the public-source research report (its §4), with items 1, 5 and 10 replaced by the browser pass's wording (its §4) and without that pass's optional item-8 append. Both reports are in the operator's primary checkout at `local_artifacts/crosstrade-close-research-2026-09-27/` (`REPORT.md`, `BROWSER-DELTA.md`; `SHA256SUMS.all` SHA-256 `8dd20292…70dbe6`), and the findings are recorded in the [close-semantics note's 2026-09-27 addendum](2026-09-26-close-semantics-c-a.md#addendum-2026-09-27--public-source-and-browser-research-governs-where-it-narrows-statuses-unchanged-unless-stated). All ten items are kept, because each still has an unanswered part. The ratified 2026-09-26 text is preserved unchanged in §1a below, **superseded for sending**. Status stays **FINAL — to be sent by the operator**; the operator still sends it himself, and no agent contacts the vendor. **Sent:** not yet recorded. Reply handling (§2) and what this authorizes (§3) are unchanged; §3's "the text above" now means §1 only (dated addendum under §3). The **Source** line above describes the 2026-09-26 text, now §1a: its "item 10 below" is §1a's item 10.

## 1. Text to send (revised 2026-09-27)

**To:** CrossTrade support, from the operator's own account. The text contains **no account identifiers**; `{account}` is the endpoint's documented path placeholder and is sent as written. Item numbers match Q1–Q10 in the close-semantics note's 2026-09-27 addendum.

> **Subject:** Full close (liquidate) behavior on a Tradovate account via the REST close endpoint
>
> We call `POST /v1/api/tv/accounts/{account}/positions/close` with no `qty` or `percent` on a Tradovate prop-firm evaluation account (Demo environment). Your webhook docs say a full `closeposition` uses Tradovate's liquidate endpoint, which also cancels the contract's working orders. The position was opened with `orders/place` carrying `stopLoss` and `takeProfit` (one OSO; the exits are OCO). We have read your public API docs and Tradovate's reference, so each question below says what we found and asks only what the documents leave open. Please answer in writing, for this endpoint and account type:
> 1. **Order of steps.** Your flatten_first note says Tradovate's server-side liquidation cancels the working orders and offsets the position. Tradovate's API reference gives no sequence. Tradovate's help centre says its platform Exit at Mkt & Cxl button cancels working orders and submits market orders, and Tradovate staff said in 2022 community posts that the platform flattens through the liquidate endpoint. Neither source gives an order of steps. For this endpoint, are the contract's working orders cancelled before the closing order is sent, at the same time, or after it fills? Is the closing order a market order?
> 2. **Quantity.** Tradovate's liquidate request carries no quantity, and your docs do not list a full `closeposition` among the commands that compute the live position. Is the closing quantity fixed when the request is accepted, or when the closing order executes? If the bracket stop fills while the liquidation is in progress, can the closing order still execute and leave an opposite position?
> 3. **Failure.** Your Tradovate API overview documents `400 tradovate_rejected` and `502 tradovate_unavailable` (the request may have reached Tradovate and is not resent), and says to reconcile after a 500. It does not say what happens to the orders. If the liquidation is rejected or fails, are the cancelled bracket orders restored, or can the position be left open without its stop? Can a close that returned success fail later? When Tradovate answers with HTTP 200 and a `failureReason` other than `Success`, what does this endpoint return? Does your late-rejection re-read cover the closing order?
> 4. **Partial.** For a multi-contract position, can the closing order fill partly? What happens to the rest, and is it protected?
> 5. **Already flat.** The "400 when nothing is open" text on your REST page is under the NinjaTrader tab. Tradovate's help centre says its scheduled Flatten Today feature leaves working orders in place on contracts with no open position. For a Tradovate account whose position is flat, what does this endpoint return, and does any "no position" result come from you or from Tradovate? Are working orders on that contract cancelled, or left working?
> 6. **Scope.** Your generic `closeposition` text says "account-level" orders. Its Tradovate note, your Tradovate order-types page, the indicator guide and the copier page say the contract's working orders. On Tradovate, does a full close send any cancel beyond the contract-scoped liquidation? That is, can it cancel working orders on other contracts in the account?
> 7. **Identity and overlap.** Your overview says REST requests have no per-account/instrument webhook lock, and that idempotency keys cover only `cancelreplace` and copier fan-out. Does the close response ever include the closing order's Tradovate id, and in which field? (The OpenAPI schema shows `data`; the page shows `response`.) If a second close for the same account and contract arrives while the first is in progress (from the API, a webhook or the Tradovate platform), what happens at CrossTrade, and at Tradovate?
> 8. **After the close.** Your docs say bracket coverage repair places a new OCO pair for uncovered quantity; the Sep 5, 2026 release note says uncovered quantity raises a critical alert. Which is current? Does tracking of a bracket family end at a full close? Can a resync or background-sweep re-check place or change orders on that contract after the close, including between the liquidation's cancel and its fill? Does repair watch OSOs placed through REST `orders/place`? Can any other CrossTrade process act on that contract after a full close when the account is used only through REST?
> 9. **REST path.** Your OpenAPI maps this endpoint to `CLOSEPOSITION` through the shared webhook parser and dispatcher. Your execution table gives a full close as `contract/find` then one `liquidateposition`, and calls that sequence typical. Please confirm that a REST full close sends exactly those broker requests, with no separate cancel, and say what "typical" can add. Your REST page labels a `percent` example `liquidate_position`: does a REST partial close use liquidation or an opposing market order?
> 10. Please distinguish documented guarantees from typical behavior, identify the applicable API/version and Demo environment, and provide supporting documentation where available. Tradovate's help centre says prop-firm and evaluation accounts are not eligible for its retail API add-on: which Tradovate integration do you use for these accounts? Please include the `admin` value you send on `liquidateposition` and any behavior specific to Demo (simulation) liquidation.
>
> If any answer depends on Tradovate rather than CrossTrade, please say so, and say whether you can obtain Tradovate's statement.

## 1a. ~~Text to send~~ Text ratified 2026-09-26 — superseded for sending (preserved)

*Superseded for sending by the operator ruling of 2026-09-27 (revision line above). Kept unchanged as ratified on 2026-09-26; do not send this version.*

**To:** CrossTrade support, from the operator's own account. The text contains **no account identifiers**; `{account}` is the endpoint's documented path placeholder and is sent as written.

> **Subject:** Full close (liquidate) behavior on a Tradovate account via the REST close endpoint
>
> We call `POST /v1/api/tv/accounts/{account}/positions/close` with no `qty` or `percent` on a Tradovate prop-firm evaluation account (Demo environment). Your webhook docs say a full `closeposition` uses Tradovate's liquidate endpoint, which also cancels the contract's working orders. The position was opened with `orders/place` carrying `stopLoss` and `takeProfit` (one OSO; the exits are OCO). Please answer in writing, for this endpoint and account type:
> 1. **Order of steps.** Are the contract's working orders cancelled before the closing order is sent, at the same time, or after it fills? What order type is the closing order?
> 2. **Quantity.** Is the closing quantity taken from the position when the closing order executes, or fixed when the request is accepted? If the bracket stop fills while the liquidation is in progress, can the closing order still execute and leave an opposite position?
> 3. **Failure.** If the liquidation is rejected or fails, are the cancelled bracket orders restored, or can the position be left open without its stop? Is a failure always in the immediate response, or can it arrive later?
> 4. **Partial.** For a multi-contract position, can the closing order fill partly? What happens to the rest?
> 5. **Already flat.** If the position is already flat, what does the endpoint return? Are working orders on that contract cancelled?
> 6. **Scope.** Does a full close cancel only that contract's working orders, or all working orders on the account? (Your generic `closeposition` text says "account-level" orders; its Tradovate note says the contract's working orders.)
> 7. **Identity and overlap.** Does the response include the closing order's Tradovate id? If a second close for the same account and contract (from the API, or from the Tradovate platform) arrives while the first is in progress, what happens?
> 8. **After the close.** Can bracket coverage repair, or any other CrossTrade process, place or change orders on that contract after a full close?
> 9. **REST path.** Does the REST close endpoint, with no `qty` or `percent`, send the same broker requests as the webhook `closeposition` (a contract lookup, then one `liquidateposition`, with no separate cancel)? Your REST page's example response for a `percent` close is labelled `liquidate_position`. Does a REST partial close use liquidation or an opposing market order?
> 10. Please distinguish documented guarantees from typical behavior, identify the applicable API/version and Demo environment, and provide supporting documentation where available.
>
> If any answer depends on Tradovate rather than CrossTrade, please say so, and say whether you can obtain Tradovate's statement.

## 2. Handling the reply (operator ruling 2026-09-26)

1. **Retain the original written reply** as original bytes, hashed (SHA-256), in the operator's primary checkout at `local_artifacts/crosstrade-close-semantics-reply-2026-09/` (gitignored).
2. **Experience is not a mechanism.** "We have not seen that happen" is experience, not a prevention mechanism.
3. **An incomplete reply leaves the corresponding questions OPEN.**
4. **Sending authorizes nothing else.** Sending this question authorizes no drill and accepts no residual risk.

As the close-semantics determination (§6) records, a written answer would be a vendor statement, subject to coordinator acceptance, and evidence for M1–M9, S (D-1), D-2 and the F1 inference; it would not be a trace.

*Addendum 2026-09-27:* rules 1–4 above are unchanged and apply to a reply to the revised text. Answers are now read against the [close-semantics note's 2026-09-27 addendum](2026-09-26-close-semantics-c-a.md#addendum-2026-09-27--public-source-and-browser-research-governs-where-it-narrows-statuses-unchanged-unless-stated), which records, for each item Q1–Q10 (the revised text's numbering), what public sources already establish, what stays open, and how the item maps to M1–M9, S, D-2 and F1.

## 3. What this authorizes

Nothing beyond the operator sending the text above. It authorizes no agent contact with the vendor, no drill (including X-3 and the deferred X-5), no order action, account access, purchase or route change, and no acceptance of the close-contract amendment or of any residual risk.

*Addendum 2026-09-27:* from 2026-09-27, "the text above" means the revised §1 text only. §1a is preserved as ratified and is not to be sent. What this section authorizes is otherwise unchanged.

## 4. Chat attempts, 2026-10-01 (not a send of §1)

*Recorded 2026-10-02 by the coordinator. Joshua reported the exchange directly, sharing a screenshot of the reply, and the Codex coordinator relayed the worker's provenance.*

**What was sent:**
- **First attempt.** The operator pasted §1 into the CrossTrade support chat. The composer has a 2,000-character limit, so the message was cut off partway through Q3, and Q4–Q10 were not sent.
- **Second attempt.** At the operator's direction, a worker prepared a 1,912-character shortened version of Q1–Q10, which the operator sent at about **23:05 America/New_York on 2026-10-01**. The UI shows "11:05 PM"; the time zone is not independently verified. The coordinator checked this text against §1 on 2026-10-02:
  - Q6 (scope) and Q9 (REST path) keep their meaning exactly.
  - Q1's citations, Q8's final question and Q10's explicit Demo identification are weakened.
  - It is a derivative, not the ratified text.

**The reply** came from the support chat, which labels itself an AI assistant.
- **What it claims:**
  - A full close (no `qty` or `percent`) resolves the contract and sends one Tradovate liquidate request, with no separate cancel step.
  - It cancels **only that contract's** resting orders, not other contracts' working orders.
  - A partial close sends an opposing market order and leaves the contract's working orders resting.
- **What it disclaims as unpublished:** the order of steps, whether the quantity is fixed at acceptance or at execution, partial fills, what a rejection or late response does to the brackets, and prop-eval/liquidate specifics.
- **What it directs:** a full written, sourced answer to all ten questions from support@crosstrade.io.
- **Sources:** it gives none.

**How it is treated (§2 rules 2–3; unchanged):**
- It is **corroboration only, not a vendor statement**. It is an unsourced AI answer that disclaims guarantees itself.
- **Q6 and Q9 stay unresolved for C-a selection.** Their canonical statuses in the [close-semantics record](2026-09-26-close-semantics-c-a.md) are unchanged: Q6 **CONFLICTING** (D-1 stands), Q9 **PARTLY_DOCUMENTED**. Every other question also keeps its prior status. Its contract-scope claim agrees with what X-3 is expected to show, but it is evidence to verify, not acceptance.
- **Vendor answers are not a C-a selection gate** (operator ruling 2026-10-02, quoted in the [C-a selection register §R.2a](2026-09-26-close-semantics-c-a.md)). The scope-extended X-3 discharges both questions: Q6 through its second-symbol evidence (register row S-V2a), and Q9 through its trace (S-V1). Vendor and AI answers are corroboration only (register row N-V0). Q6 and Q9 stay unresolved until X-3 runs.

**Still owed:** the operator emails §1 verbatim to support@crosstrade.io, as the reply itself directs. The prepared file is `unsent-human-support-inquiry.eml`. The dated **Sent:** line is added when he reports sending it.

**Retained privately** at `local_artifacts/crosstrade-close-semantics-reply-2026-09/` (gitignored):
- the sent message, `sent-shortened-chat-message-2026-10-01.txt`, SHA-256 `6abf6013…3849`;
- the reply, `ai-reply-to-shortened-message-2026-10-01.txt`, SHA-256 `9e92010f…8f3f6`;
- the manifest `SHA256SUMS-preparation.txt`, SHA-256 `de65b779…65b1`.
- the operator's own screenshot of the reply, Windows capture at 23:35 ET, copied byte-for-byte as `operator-screenshot-ai-reply-2026-10-01-233511.png`, SHA-256 `219f5749…e0d1`.

The two `.txt` files above are DOM transcriptions, not server exports.

**Retention defect, OPEN (§2 rule 1).** CrossTrade's support UI offers no export control, so the reply's original bytes were never retained. The screenshot is the best capture available. It is still a rendering, not the server's bytes, and a transcription is not sufficient (commissioning packet :537). This changes no status, because this reply is not evidence for any question. **The human-support reply must be retained as original bytes**: the received email saved as `.eml`, then hashed.
