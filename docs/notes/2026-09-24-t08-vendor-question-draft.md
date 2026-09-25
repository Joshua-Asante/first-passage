# T08 vendor question: draft for the operator to send (2026-09-24)

**Status:** DRAFT. Authorized by the operator's 2026-09-24 ruling ([T08 §7.8](../briefs/handoffs/2026-09-21-tradeify-t08-broker-protection-feasibility.md#78-operator-ruling-on-the-return-2026-09-24), part 2). **Joshua sends it; no agent contacts a vendor.** Remove nothing that makes the question narrower; add no account identifier, account size, P&L or strategy detail.

**Recipient:** CrossTrade support. The blocker being tested is CrossTrade's deferred work (T08 §7.3 row 5), so the bound, if one exists, has to come from CrossTrade. Tradovate is not asked: its side matters only if CrossTrade gives a bound, and §7.4 already records that evaluation accounts have no native API access.

**What counts as an answer:** a written reply, kept as original bytes (email source or exported ticket) under `local_artifacts/t08-vendor-question-2026-09/` on the primary checkout and hashed into that root's index. Paste the SHA-256 into T08 §7 when it arrives. A "yes" with no stated bound, a bound that covers only some of the listed mechanisms, or a reply that points to docs T08 already read is recorded as-is and does not by itself close R3.

---

## Message

Subject: Upper bound on when an accepted Tradovate webhook request can still act

Hello,

I send orders to a Tradovate account through CrossTrade webhooks and need a precise answer on one narrow point for my risk procedures.

**The request shape (nothing else):** one webhook that places a single market or stop entry on one futures contract, with its own native Tradovate OSO/bracket stop attached in the same request. It is sent **without** `delay=`, without any ATM strategy or ATM fields, without `cancel_after`, and without copier or multi-account fan-out. I send it from my own client, not from TradingView.

**The situation:** my client sends that request and gets **no response** (connection error or timeout), so I don't know whether CrossTrade received, queued or forwarded it.

**My question:** For that request shape, is there a guaranteed maximum time after which CrossTrade will never send it, or anything derived from it, to Tradovate? That covers first transmission and every later action, including:

1. durable recovery or any retry after a CrossTrade restart or outage;
2. OCO or bracket coverage repair;
3. any internal queue, timer or background job.

If there is such a bound, please state it in seconds and confirm it covers all three of the above. If there isn't one, or if any mechanism can act on the request without a time limit, please say so.

A related question, only if it's easy to answer: does CrossTrade discard a webhook request that arrives, or is recovered, after some age, as documented for the NinjaTrader path? If so, what is the age, and does it apply to the Tradovate path?

Thank you.

---

## Why these exact words (for the operator; not sent)

- **The narrowed shape** is T08 §7.7's. Each exclusion removes one documented deferred-work class: `delay=` (the ≤300 s timer), ATM fields (24 h managed-ATM retries), `cancel_after` (the watchers), fan-out (copier retries). What's left is durable recovery and OCO repair, the two items the question lists by name.
- **"No response"** is the only case that matters. #479 records that for non-TradingView senders a successful response means Tradovate accepted the order, so an answered request is not unknown.
- **"Never send it, or anything derived from it"** is the no-future-effect property E3 needs. A bound on first transmission alone would miss recovery and repair.
- **The NT8 late-discard question** is optional. T08 found a documented late-request discard for the NT8 path only; a Tradovate equivalent would be the cheapest form of bound.
- **A GTC bracket exit that a bounded entry legitimately placed** is not an unknown request; once observed it is an identified working order under E3's ownership transfer. The question therefore doesn't ask about GTC exits, but the amendment still has to cover the case where the entry's own effect is never observed (scope note, question Q2).
