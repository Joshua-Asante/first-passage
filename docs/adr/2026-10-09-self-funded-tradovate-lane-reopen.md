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
   tastytrade and IBKR). Planned starting capital is recorded privately (the public record names it `E_0`).
2. **Objective and book.** The lane's objective is **maximum growth** of the
   account. The portfolio is **not yet selected**; it is not the Tradeify book by
   default (operator, 2026-10-09). Selection is owed against the growth objective,
   with candidates drawn from existing strategies under their locks; whatever is
   chosen gets its own (portfolio, firm-tier) protection and sizing binding, keyed to the
   personal-account tier (owed item 2), under the
   [concept-not-constant ADR](2026-07-13-dd-protection-concept-not-constant.md),
   never an edit of the Tradeify binding or of `dd_protection` constants.
3. **Data.** The same personal account is the intended real-time CME source for the
   signal daemon, replacing the retired Databento path, subject to Tradovate's and
   CME's licensing answers (the P6 draft in the
   [feed-provider note](../notes/2026-10-03-feed-provider-questions-narrowed-DRAFT.md#46-p6-tradovate-api-personal-data-only-account)
   is reframed from data-only to own-assets trading).
4. **Capital clearance: maximum peak-to-trough drawdown 15%** (operator ruling
   2026-10-09: "I'd accept a 15% drop", measured peak to trough). Within that bound the
   lane sizes for maximum growth. Selection test and live stop (operator confirmed
   2026-10-09, "99 in 100, confirmed"):
   - *Selection:* a portfolio and its sizing clear only if the intraday-honest simulated
     p99 peak-to-trough drawdown is ≤ 15%, after Tradovate costs and whole-contract
     rounding; among clearing candidates, the highest median growth rate wins.
   - *Live:* equity 15% below its running peak halts new entries and flattens; resumption
     needs an operator GO.
   No capital authorization until a portfolio clears this standard.

Effective 2026-10-09. Unchanged: R5/P2 FALSIFIED; the Tradeify program and its gates;
AGENTS.md live-execution rules (M1, arming, per-session GO); private-figure policy
(balances and P&L of the personal account stay out of the repo).

## Revision

- 2026-10-09 (same day): portfolio unselected and maximum-growth objective (commit `87d12a0`); 15% peak-to-trough clearance standard recorded (`8a5e42c`); its p99 selection test and live stop confirmed by the operator (`f63a19c`); Codex review of PR #743: venue/parity checklist reading, (portfolio, firm-tier) keying, feed gating on items 3–4, and owed item 7 (this revision).

## Grounds

- The 2026-07-16 closure was an operator posture ("closed for now"), and its §4 limb 1
  names a dated operator GO with a fresh venue/parity checklist as the re-open path. This
  is that GO; the checklist is the owed list below. The lane is reopened as a posture and
  a research target now; capital authorization and any live use wait on that checklist.
- Tradovate wins on integration cost: the account already exists, and the c1 rail already
  routes to Tradovate, so order semantics, drills and runtime ports carry over.
  IBKR fails unattended login by source (feed note §Summary item 4).
- A personal account trading the operator's own assets is the cleanest case for CME
  non-professional status (Schedule 5 §8.2 own-assets test), which is the weakest point
  of every prop-destination data route in the feed note.
- Tradeoff accepted: one broker carries both the prop evaluation and the personal
  account, so a Tradovate outage or policy change hits both.

**Owed** (each a separate record with its owner). Items 3 and 4 gate **any** activation of
the personal account as a data feed, dry-run included, and cover every order destination
that feed drives (the personal account and the Tradeify evaluation). All seven gate the
first live order on the personal account:

1. Portfolio selection and sizing that clear the 15% drawdown standard (Decision 4).
2. Personal-account tier in `core/firm_rules.py` with `starting_balance`, then the
   `core/mc/preflight.py` engine pre-flight and a re-MC under that tier.
3. Tradovate API access on the personal account: the $1,000 key requirement, the API
   add-on and the data entitlement (fees in the feed note are excerpt-grade; verify on the page).
4. CME data licensing answer for automated use with orders at every destination the feed
   drives: the personal account and the Tradeify evaluation (feed-note CME and P6 drafts).
5. Tradeify rule check, if the chosen portfolio shares any strategy with the Tradeify
   book: whether the same signals in a personal account at the same broker breach any
   copy-trading, hedging or account-linking rule.
6. Rail binding: an account/instance binding for the personal account kept separate from
   the Tradeify instance (configuration-as-code; no shared credentials).
7. The 15% live halt (Decision 4): a fail-closed running-peak halt-and-flatten control for
   the personal account, with tests and an activation check that refuses to arm without it.
   Nothing in `ops/c1_rail` or `core` implements it today.

## Current owner

This ADR owns the lane's scope until a campaign or plan owner is named for items 1–7;
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
