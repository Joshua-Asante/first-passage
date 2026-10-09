# ADR 2026-10-09 — Self-funded lane reopened: personal Tradovate account, maximum-growth objective, doubling as the CME data source

**Status:** Accepted (operator executive decision, chat 2026-10-09)
**Decision date:** 2026-10-09
**Supersedes:** 2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md in part — §2.1 "self-funded scale lane CLOSED (parked)" and §4 limb 1's re-open path, which this record discharges
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Format:** concise

## Decision

1. **Lane.** The operator reopens a self-funded lane. Venue: the operator's existing
   personal Tradovate account (broker chosen 2026-10-09 over Ironbeam, a Rithmic FCM,
   tastytrade and IBKR). Planned starting capital: $10,000.
2. **Objective and book.** The lane's objective is **maximum growth** of the
   account. The portfolio is **not yet selected**; it is not the Tradeify book by
   default (operator, 2026-10-09). Selection is owed against the growth objective,
   with candidates drawn from existing strategies under their locks; whatever is
   chosen gets its own (portfolio, venue) sizing binding under the
   [concept-not-constant ADR](2026-07-13-dd-protection-concept-not-constant.md),
   never an edit of the Tradeify binding or of `dd_protection` constants.
3. **Data.** The same personal account is the intended real-time CME source for the
   signal daemon, replacing the retired Databento path, subject to Tradovate's and
   CME's licensing answers (the P6 draft in the
   [feed-provider note](../notes/2026-10-03-feed-provider-questions-narrowed-DRAFT.md#46-p6-tradovate-api-personal-data-only-account)
   is reframed from data-only to own-assets trading).
4. **Capital clearance is redefined, not waived.** The operator will accept more risk
   than the current standard. The new standard for "cleared to trade the operator's
   own money" is owed as its own operator ruling before any live order; until it
   exists, this lane holds no capital authorization.

Effective 2026-10-09. Unchanged: R5/P2 FALSIFIED; the Tradeify program and its gates;
AGENTS.md live-execution rules (M1, arming, per-session GO); private-figure policy
(balances and P&L of the personal account stay out of the repo).

## Grounds

- The 2026-07-16 closure was an operator posture ("closed for now"), and its §4 limb 1
  names a dated operator GO as the only re-open path. This is that GO.
- Tradovate wins on integration cost: the account already exists, and the c1 rail already
  routes to Tradovate, so order semantics, drills and runtime ports carry over.
  IBKR fails unattended login by source (feed note §Summary item 4).
- A personal account trading the operator's own assets is the cleanest case for CME
  non-professional status (Schedule 5 §8.2 own-assets test), which is the weakest point
  of every prop-destination data route in the feed note.
- Tradeoff accepted: one broker carries both the prop evaluation and the personal
  account, so a Tradovate outage or policy change hits both.

**Owed before first live order** (each a separate record with its owner):

1. Portfolio selection for the growth objective, and the capital-clearance standard
   (operator ruling: the risk of ruin or the maximum drawdown accepted in exchange for growth)
   evaluated against it.
2. Personal-account tier in `core/firm_rules.py` with `starting_balance`, then the
   `core/mc/preflight.py` engine pre-flight and a re-MC under that tier.
3. Tradovate API access on the personal account: the $1,000 key requirement, the API
   add-on and the data entitlement (fees in the feed note are excerpt-grade; verify on the page).
4. CME data licensing answer for automated own-account use (feed-note CME and P6 drafts).
5. Tradeify rule check, if the chosen portfolio shares any strategy with the Tradeify
   book: whether the same signals in a personal account at the same broker breach any
   copy-trading, hedging or account-linking rule.
6. Rail binding: an account/instance binding for the personal account kept separate from
   the Tradeify instance (configuration-as-code; no shared credentials).

## Current owner

This ADR owns the lane's scope until a campaign or plan owner is named for items 1–6;
[STATE.md](../../STATE.md) carries the forward row. Venue rules stay with
[`core/firm_rules.py`](../../core/firm_rules.py); feed questions with the
[feed-provider note](../notes/2026-10-03-feed-provider-questions-narrowed-DRAFT.md).

## Verification

```bash
python .claude/skills/brief-authoring/scripts/check_brief.py docs/adr/2026-10-09-self-funded-tradovate-lane-reopen.md --type adr
python scripts/check_adr_graph.py --regenerate-index
python scripts/check_adr_graph.py
rg -n "2026-10-09-self-funded" docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md STATE.md
```
