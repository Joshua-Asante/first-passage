# Tradeify exclusive-use replies, 2026-10-08/09

**Status:** evidence record. Recorded 2026-10-10 from the operator's Gmail thread, read with his authorization. **Verified by operator: no.** Changes no status, binding or authorization.
**Serves:** [lane-reopen ADR](../adr/2026-10-09-self-funded-tradovate-lane-reopen.md) owed item 5 (input only; the item stays open) and the Tradeify book's exclusive-use constraint ([rail GO](../adr/2026-07-17-c1-rail-build-account-registration-go.md), FTA §6.6).

## 1. Exchange

| # | When (UTC) | From → to | Content |
|---|---|---|---|
| Q | 2026-10-08 21:45 | operator → Tradeify support | Question (§2) |
| R1 | 2026-10-08 21:47 | Tradeify help desk → operator | Answer (§3), 71 s after Q |
| R2 | 2026-10-09 09:47 | Tradeify help desk → operator | Follow-up offering further discussion; no new rule content |

**Retained privately** at `local_artifacts/tradeify-exclusive-use-2026-10/` (gitignored): one `.txt` per message with headers. These are transcriptions of the Gmail API plain-text body, not the original MIME bytes.
- Q `1-question-sent-2026-10-08T214555Z.txt`, SHA-256 `a2d3fa18…ba49`
- R1 `2-reply-2026-10-08T214706Z.txt`, SHA-256 `056bfa28…8136`
- R2 `3-followup-2026-10-09T094708Z.txt`, SHA-256 `f7040573…c908`
- manifest `SHA256SUMS`, SHA-256 `25abfa7d…f951`

## 2. Question as asked (paraphrased)

The operator described a privately owned Python engine for his own Tradeify evaluation, unshared with other traders, and asked, citing the Guidelines for Traders and FTA §6.6:
1. Is "same bot or strategy" defined by shared software/infrastructure, shared signal logic, or the resulting trades?
2. Is the same engine and strategy logic at another firm still prohibited when risk limits, sizing and weights differ?
3. Is any software reuse across firms allowed for genuinely separate strategies, and with what separation?

He asked how it applies to evaluation, simulated funded and live funded accounts, for the governing clauses, and for a risk/compliance confirmation or review.

## 3. Answers (R1, paraphrased per point)

- **Ownership:** the trader must be the "sole owner of the bot or strategy" and able to prove it on request.
- **Exclusive use:** "The bot or algorithm must be used only within Tradeify." The same bot across multiple firms is prohibited.
- **HFT:** HFT bots are not allowed.
- **Compliance review:** Tradeify may ask for documentation or verification if activity is flagged.
- **Q1 (what is "same"):** not defined. The reply says the policy turns on ownership and exclusivity: owned by the trader, not shared with other traders or firms.
- **Q2 (different sizing/weights):** still prohibited, "even if risk limits, sizing, or weights differ".
- **Q3 (software reuse with separate strategies):** the reply restates that the same bot may not be reused across firms; it does not address separate strategies on shared software.
- **Account phases:** not addressed per phase.
- **Unprompted:** the Tradovate API is "only available for live funded accounts, not evaluation or simulated funded accounts".
- **Clauses / compliance review:** none cited beyond linked help articles; no risk/compliance confirmation or review offered.

R2 restates the topic and invites further questions; it adds no rule content.

## 4. Assessment — INFERENCE

**Provenance.** A 71-second turnaround and generic structure suggest a template or assisted help-desk reply, not a compliance ruling. Treat it as the venue's stated current guidance, weaker than a clause.

**(1) ADR item 5: same signals in a personal account at the same broker.** The reply speaks of "firms", and a self-funded Tradovate account is not a firm. But its wording, "used only within Tradeify", read literally, excludes any use outside Tradeify, a personal account included. Varying sizing or weights does not help (Q2). So a portfolio that shares a strategy with the Tradeify book should be presumed in breach until Tradeify says otherwise in writing. Copy-trading, hedging and account-linking were not asked and not answered. A personal account at the same broker is still the configuration those rules usually target, so this is not cleared. Lowest-risk reading: item 5 is avoided only if the personal portfolio shares no strategy, and no engine or bot, with the Tradeify book. "Shares no engine" is unconfirmed (Q3 unanswered).

**(2) The Tradeify book itself.** Sole ownership and Tradeify-only use are consistent with the recorded posture: one firm, no MFFU concurrency ([rail GO](../adr/2026-07-17-c1-rail-build-account-registration-go.md)). The book's sources being the operator's own is not yet a provable-ownership file. The Tradovate-API remark is the new risk. The rail reaches the evaluation through CrossTrade, not a direct API key the operator holds, and canned-payload trades have filled. So the remark does not show the route fails technically. Whether Tradeify treats a third-party route into an evaluation as permitted, though, is unanswered.

## 5. Still unanswered

1. What makes a bot "the same": shared engine/infrastructure vs signal logic vs trades (Q1).
2. Whether separate strategies on one shared engine are allowed, and what separation counts (Q3).
3. Whether "only within Tradeify" covers a self-funded personal account, not just other firms.
4. Copy-trading, hedging and account-linking with a personal account at the same broker (ADR item 5's own terms).
5. Per-phase application: evaluation, simulated funded, live funded.
6. Whether the CrossTrade → Tradovate route into an evaluation is permitted, given the API remark.
7. The governing clause text, and a risk/compliance confirmation; the reply cites neither.
8. What evidence of sole ownership Tradeify would accept.
