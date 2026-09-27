# CrossTrade close-semantics vendor question: final text for the operator (2026-09-26)

**Status:** **FINAL — to be sent by the operator.** Not sent by any agent; no agent contacts the vendor. **Sent:** not yet recorded (a dated line is added here when the operator reports sending it).
**Authority:** operator ruling 2026-09-26, given in session by Joshua through a structured question. He selected "Finalize it for me to send", whose text was Astra's recommendation; it is recorded here as his decision (R-VENDORQ).
**Source:** the draft in the [close-semantics determination](2026-09-26-close-semantics-c-a.md) §6, which stays as drafted. The ruling keeps its nine questions and adds one short request, item 10 below. Nothing else is changed.
**Context:** the investigation of C-a (whole-leg broker liquidation) under the operator's close ruling of 2026-09-26 (R-CLOSE, [incident ADR §A11.1](../adr/2026-09-17-bounded-platform-protection-incident-contract.md#a111--operator-ruling-close-direction-2026-09-26)), investigation only. This is a separate question from the T08 vendor question sent on 2026-09-25 ([campaign §59 Ruling 2](../briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md#ruling-2--the-t08-vendor-question-has-been-sent)).

## 1. Text to send

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

## 3. What this authorizes

Nothing beyond the operator sending the text above. It authorizes no agent contact with the vendor, no drill (including X-3 and the deferred X-5), no order action, account access, purchase or route change, and no acceptance of the close-contract amendment or of any residual risk.
