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
   Evidence (2026-10-10): [Tradeify exclusive-use replies](../notes/2026-10-10-tradeify-exclusive-use-replies.md); item stays open.
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

## Addendum 2026-10-11 — strategy split between lanes (option c)

**Ruling** (Joshua, 2026-10-11 UTC, directly to the Deployment Coordinator: "go with (c), split the strategies between lanes"):

- The Tradeify book's four strategies stay with the Tradeify lane only: aegis_6j, dj30_mym_p250 (Striker DJ30 MYM), vanguard_mgc and orb_mnq_v7, as named in the [venue edition](../../ops/venue_editions/Tradeify_Select_100K.md).
- Decision 2's candidate pool narrows accordingly: the personal Tradovate lane draws only from **other** locked strategies.
- **Reason.** Tradeify's 2026-10-08 reply says a bot must be used only within Tradeify, even with different sizing ([exclusive-use replies](../notes/2026-10-10-tradeify-exclusive-use-replies.md), #772).

**Effect on owed item 5.** The strategy-overlap part is resolved by construction: no chosen portfolio shares a strategy with the Tradeify book. The copy-trading, hedging and account-linking questions, and whether the CrossTrade route is permitted, stay **open** pending Tradeify compliance's written answer. Items 1–4, 6 and 7 are unchanged.

## Addendum 2026-10-11b — Tradeify book reused on the personal lane (supersedes the option-c split)

**Ruling** (Joshua, 2026-10-11 UTC, directly to the Deployment Coordinator): "reuse the Tradeify strategies, qualify their sizing for the personal capital, and finish the personal-account operating controls. The search for additional strategies can come off this deployment's critical path."

**Corrections** (Joshua, 2026-10-11, to the coordinator, on this addendum's first draft) are folded in below. He supports reusing the existing personal-account components, a cheap sizing, margin and risk pre-screen before expensive runs, and operating only one account at a time for the first deployment.

- **Supersedes** the [2026-10-11 option-c split](#addendum-2026-10-11--strategy-split-between-lanes-option-c). That addendum stays as history; its candidate-pool narrowing no longer applies.
- **Decision 2's pool** is the Tradeify book's strategies (aegis_6j, dj30_mym_p250, vanguard_mgc, orb_mnq_v7), sized for the personal starting capital `E_0` (value private). Sizing **starts from the retained successor configuration** (FLOOR-HALF, ruled 2026-10-10 in the T00 card §8; per-leg values private, bound by `size_vector_sha256` `139919cd…c271`). Legs it sets OFF stay OFF. Any change to a leg's state or quantity is an explicit operator choice with a stated justification. Each proposed rung names the quantity behaviour it represents (fixed quantity, risk multiplier, port map or on/off), so the portfolio tested is the one that would run. The earlier five-leg study (K = 2,375) is not restored. Searching for additional strategies is off this deployment's critical path.
- **Personal sizing and protection policy.** The current book path is bounded by Tradeify limits, not unbounded: 80 micro-equivalents per account, and at most 22 base + 55 add for Striker (`ops/c1_rail/book_policy.py:64-65,163-167,537-546,822`), with protection fixed at trailing 1%/0.40 (`:101-117`). A tier with no micro cap makes that path refuse to load rather than run unbounded. The personal tier therefore needs its own defined cap source, risk-dollar basis and protection policy (owed items 1–2).
- **Decision 4 is unchanged:** the portfolio and its sizing clear only on the intraday-honest p99 peak-to-trough drawdown ≤ 15% after Tradovate costs and whole-contract rounding, with the live 15% halt. A Tradeify screen result does not establish the personal-account drawdown, growth, fee or margin results; those are tested at `E_0`. Authoritative personal margin inputs (dated Tradovate per-contract margins for 6J, MYM, MGC and MNQ) are not yet recorded anywhere in the repo.
- **Evidence standing.** Every admitted panel is already fully exposed (book lineage manifest `exposure`), so a result is feasibility on exposed history, not out-of-sample evidence; excluding a configuration after another result has been read does not restore a holdout. Exposure history is retained, further choices are frozen before any `E_0` scoring output, and the trial accounting is justified in the study, not by a K count alone.
- **Owner:** the Deployment Coordinator owns #752 (Q-SFGROWTH-1) and re-scopes it in place by default. A new study ID is optional for clarity; closing #752 or opening a replacement is not a prerequisite. Existing implementation owners of #775–#777, #779, #782 and #783 are preserved.

**Agreement restrictions** (Tradeify Funded Trader Agreement, page marked last modified May 2026, read 2026-10-10):
- **Published exception, no permission gate.** §6.6 Exclusive Use says "the Trader may use the bot on the Trader's personal accounts". The same bullet bars use across multiple firms, and a personal brokerage account is not another firm. §6.6 sets no prior-permission step: its documentation duty arises only if Tradeify's risk measures flag an account (§6.6 Compliance & Verification; §6.7(g)). A Tradeify reply, including support's 2026-10-08 one, is weighed against that text; it does not by itself block personal-only deployment.
- **Ownership (binding).** §6.6: the trader must be able to prove sole ownership of the bot, with nobody else having access to it or using it, and the bot must not be high-frequency. §6.7(b): no team trading, third-party management, or copying or mirroring trades with any other person.
- **Opposing exposure (binding).** §6.7(c)–(e): opposing positions between a Tradeify account and an External Account (a personal brokerage account is one) in the same product or Product Group are prohibited at all times, regardless of intent, contract size or account type. A breach exists as soon as positions overlap; no cure window is published.

**First deployment: one account at a time.** Before the active account switches in either direction (Tradeify to personal or personal to Tradeify, weekly preservation trades included), the outgoing account is verified flat, with no working orders, and unable to submit delayed entries (its instance disarmed, with no queued, retrying or scheduled order path). Any uncertainty blocks the switch. Simultaneous operation is outside the first deployment and would need its own safeguard and operator ruling.

**Effect on owed items.** Item 1 is re-scoped as above. Item 5 covers the binding restrictions: the switch check, its Product Group mapping from Tradeify's own source, and retained evidence of sole ownership; its copy-trading, hedging and account-linking questions are answered against the published text above. A written Tradeify answer is not required to close it. Items 2–4, 6 and 7 are unchanged.
