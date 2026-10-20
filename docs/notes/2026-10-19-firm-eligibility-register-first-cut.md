# Firm-eligibility register: first cut for the 11-08 sitting

**Status:** DRAFT for review; documentation only; not an admission, authorization or clearance.

First cut, due 2026-10-23; final 2026-10-30 (drafted 2026-10-19). It is not §4 evidence. Owner: the Claude deployment coordinator ([ledger, 2026-10-17](../superpowers/plans/2026-09-18-full-e1-execution-slices.md#coordinator-transfer--claude-deployment-coordinator-2026-10-17)).

**Related:** [FXIFY Flex vs FundedNext source note](2026-10-19-fxify-flex-vs-fundednext-futures-source-status.md) · [Tradeify checklist addendum 2026-10-19](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-10-19--no-book-lineage-configuration-has-an-evidence-case-for-the-tradeify-evaluation) (merged [#876](https://github.com/Joshua-Asante/first-passage/pull/876)) · [four-firm ADR](../adr/2026-07-12-prop-portfolio-four-friendly-firms.md#addendum-2026-10-16--operator-rulings-50-ceiling-fresh-4-candidate-orb-mnq-v7-fxify-futures-flex-registration-accepted) (addendum 2026-10-16).

**Where things stand:** no firm tier has a strategy that is qualified and admitted to run. Tradeify is the only registered venue with a chosen native route, but no strategy is bound to it and its licence and admission questions are open. FXIFY Futures Flex has been directed into the registry but does not count toward §4. FundedNext Futures is only a comparison basis, with no registry row and no rule sheet. Questions to both firms are drafted and have not been sent. ORB MNQ v7 solo is paused (checklist 10-19 :978).

**Grades:** facts come from merged owner records on `main` (3fcccf9) unless marked as follows:
- **PR**: an open, unmerged PR.
- **WEB**: a public page seen 2026-10-19 (see the [source note](2026-10-19-fxify-flex-vs-fundednext-futures-source-status.md)).
- **PRIVATE**: a coordinator or owner record kept outside the repo, sanitized here.
- **Operator-reported**: Joshua's report, not in the repo.

This register holds no account figures, P&L or strategy details.

## 1. Firm table

| Firm / tier | Registry | Automation permission | Native route | Eligibility status | Blocking gates | Owner | Sources |
|---|---|---|---|---|---|---|---|
| **Tradeify Select 100K** | Yes, `tradeify` family (unchanged since 10-16) | Native NinjaScript is allowed on eval and sim-funded (support reply, 10-12, no clause cited). External signal engines, bridges and the same bot across firms are barred. PRIVATE flag: the replies may have been automated | NinjaScript in NinjaTrader Desktop on the existing eval, attended, with no strategy bound (Joshua, 10-18; PRIVATE) | Track B is SUPERSEDED (10-16). No book-lineage configuration has an evidence case (ruling 10-19, [#876](https://github.com/Joshua-Asante/first-passage/pull/876)). The live edition set is empty. The eval is retained and disarmed, and the weekly trade continues. This is an optional native lane for a Tradeify-only strategy. One of the four ORB §4 tiers (pristine-start MC; prereg :80). The contract's 10-30 verdict reports it separately (prereg :427). A non-gating used-account forecast is ratified as a proposal but not released (prereg :440; RATIFICATION.md:17). None of this binds a strategy to the eval | §4 rows T1–T10 | Joshua (lane decisions); coordinator (lane record, question set); Codex NT executor (computer use) | [checklist 10-16](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-10-16--track-b-superseded-for-tradeify), [checklist 10-19](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-10-19--no-book-lineage-configuration-has-an-evidence-case-for-the-tradeify-evaluation), [route record 10-12](../briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md#addendum-2026-10-12-later--tradeify-support-strategy-logic-must-be-native-for-evaluation-accounts), [replies record](2026-10-10-tradeify-exclusive-use-replies.md), [ORB prereg](../briefs/pre-registration/2026-10-17-orb-mnq-v7-s4-prereg-DRAFT.md), [RATIFICATION](../briefs/pre-registration/2026-10-18-orb-mnq-v7-s4-RATIFICATION.md) |
| **FXIFY Futures Flex 150K** | Directed 10-16 under its own key `fxify_futures`, never `ACTIVE_FIRM="FXIFY"`. A provisional row `FXIFY_Futures_Flex_150K` exists only on open [#867](https://github.com/Joshua-Asante/first-passage/pull/867) (PR). Default preflight is blocked, cost is `None`, and the code is on hold | WEB: EAs are enabled by default on Flex and Direct, on NinjaTrader, Tradovate and TradingView. An EA that trades news is an immediate breach. API, bridges and VPS are not addressed on the EA page (WEB); no page read addresses them (#869 §A5, PR) | Planned: NinjaScript in NT8 on the FXIFY-issued Tradovate connection (#877, PR). Hosting and unattended use are unassessed (FX-N1) | In the program firm set but **not counting toward §4**: (a) the row is not on main; (b) default preflight fails; (c) is argued met (#869 §E2), with coordinator acceptance pending. Outside S1. Excluded from the ratified, merged four-tier ORB contract (prereg :80, :105; RATIFICATION.md:17). No result exists at any tier; #877's step-2 labels (UNCLEAR at D=252, NOT PROMISING at D=126; PR) carry no evidential weight | §4 rows X1–X7 | Coordinator (row-field acceptance); #867/#869 writers (sheet); Codex (code, on hold); Joshua (outreach) | [ADR addendum 10-16 §3](../adr/2026-07-12-prop-portfolio-four-friendly-firms.md#addendum-2026-10-16--operator-rulings-50-ceiling-fresh-4-candidate-orb-mnq-v7-fxify-futures-flex-registration-accepted); #867, [#869](https://github.com/Joshua-Asante/first-passage/pull/869) sheet (PR); source note |
| **FundedNext Futures Flex 150K** | No row. `core/firm_rules.py:473` has only a commented onboarding placeholder. A futures row needs its own key plus the Firm Expansion chain (ADR, preflight, re-MC) | WEB: bots and AI are allowed (terms 2.2.6). The firm may ask to review the execution system and "necessary materials", with scope undefined. A different dashboard or trading IP needs prior approval (2.1.7). Cross-account hedging is barred, including with other firms (1.2.21) | Not assessed. FN-3 asks about automation and hosting | A provisional comparison basis in [#877](https://github.com/Joshua-Asante/first-passage/pull/877) (PR), not a selection. **No rule sheet exists**: the inputs are #877 §3 and the source note. Outside the registry and S1. No evidence at any tier; #877's step-2 labels (UNCLEAR at D=252, NOT PROMISING at D=126; PR) carry no evidential weight. Parked 10-19 pending the CME and firm answers (#877, PR) | §4 rows N1–N5 | #877 author (proposal); coordinator (firm facts); registration writer not named; Joshua (outreach) | #877 (PR); source note |
| **LucidPro 150K** | No row | Not re-read since the 10-14 venue note | Tradovate family (venue note) | Joshua chose it as the 10-16 fallback, but that choice exists only in uncommitted form (#877 §8). It is not one of #877's comparison bases | O1 | Joshua | [venue note §1, §8](2026-10-14-funded-venue-alternatives-assessment.md) |
| **Personal_Tradovate** | Row exists. It is not a prop tier, and preflight raises on `profit_target` None | Self-funded; no firm permission involved | Personal lane | Supports multi-firm testing and qualification; it is not an alternative destination (10-16 ledger). FG has not run. P4/P-SW admission is pending. Q-SFCLEAR-3 is frozen and its dispatch is paused (10-19). #873 closed unmerged | FG option (pending Joshua); P4/P-SW restart defect; Q-SFCLEAR-3 dispatch; owed exposure entry (P6) | Joshua; coordinator | ledger :2308-2309; checklist 10-19 :985; #877 step-2 addendum (PR) |
| **MFFU Rapid 100K** | Yes | Unchanged | Unchanged | One of the four ORB §4 tiers, with the 16:10 ET I-24 check: any lot spanning or exiting at or after 16:10 makes the tier inadmissible | Plan identity (EOD or Intraday Rapid); per-plan consistency; O2 | Coordinator | [ORB prereg :79-80](../briefs/pre-registration/2026-10-17-orb-mnq-v7-s4-prereg-DRAFT.md) |
| **Bulenox 100K** | Yes | Unchanged | Unchanged | One of the four ORB §4 tiers (single run; the F2 optimistic-lower-bound label is kept) | FAQ-vs-ToS conflict; dead URLs; Rates PDF drift; no Fast Track 150K row | Coordinator | ORB prereg :80-83 |
| **BluSky Premium 100K** | Yes | The 07-12 fact has not been re-read | Unchanged | One of the four ORB §4 tiers | Cost-proxy decision; 404 citation; O2 | Coordinator | ORB prereg :80; `core/firm_rules.py:388-406` |
| **Others:** FundYourEdge Prime 150K; the ADR-conditional group (Apex, Topstep, TradeDay, Earn2Trade); screen classes | No rows | No change since 10-16 | — | No change | — | Coordinator | venue note §§4, 8, 10 |

**Tradeify decision record.** A future Tradeify-only strategy is decided through the coordinator's Tradeify unattended-operation roadmap (r2, 2026-10-19). It is PRIVATE and kept outside the repo. Its public owners are the checklist addenda of 10-16 and 10-19. The first decision on it is Joshua's: fund the lane or park it. Its exact open blockers are §4 rows T1–T10. The roadmap expects the 10-30 strategy gate to read NO-GO; that is an inference, not a verdict.

## 2. Firm questions (drafted, not sent)

The questions are in #877, `docs/notes/2026-10-19-flex-firm-questions-DRAFT.md` (PR, unmerged). Joshua funded them on 2026-10-19 as Step 3 item 1. Joshua sends both emails from his own account; agents send nothing. Replies come to this register, keyed by question ID.

**Email 1, FundedNext (7):**
- FN-3: automation and hosting on Challenge and Funded; approval when the host IP differs from the dashboard IP (2.1.7).
- FN-2: whether the planned position mix counts as correlated hedging (2.2.13); the Asset Group list.
- FN-1: how one product counts against the 8-mini/80-micro cap.
- FN-9: whether 2.2.6 review reaches source code.
- FN-4: whether the MLL trails the intraday high or the EOD balance, and whether funded is the same.
- FN-10: the withdrawal basis.
- FN-11: what follows the 5th reward, and whether automation is allowed there.

**Email 2, FXIFY (8):**
- FX-2: news trading by automated strategies.
- FX-1: evaluation extensions.
- FX-N1: native NinjaScript hosting, notice, VPS and code disclosure.
- FX-3: whether two named products are tradable, and how they count against the cap.
- FX-N3: hedging, "one-sided bets" and "overexposure" (GTC 5.4.1.4/5.4.1.7).
- FX-8: whether the drawdown lock applies during the evaluation or only on Flex Funded.
- FX-6/FX-4: the payout basis, and which add-ons carry over.
- FX-N8: the funded agreement before purchase, and the account end state.

**Deferred (16):**
- FundedNext: FN-5, FN-6, FN-7, FN-8, FN-12, FN-13, FN-14.
- FXIFY: FX-5a, FX-5b, FX-7, FX-N2, FX-N4, FX-N5, FX-N6, FX-N7, FX-N9.
- FN-13 and FX-N5 (data for automated use) wait on the CME clarification.

**Proposed additions (for the #877 author; not yet in the draft).** These close source-note gaps:
1. **FXIFY copy-out:** may the same owner run a strategy independently, not copied, on a personal account or other own accounts? This is source-note U4a. It restores the reuse half of venue-note Q8, which FX-N8 drops.
2. **FX-8 payout limb:** does the lock also apply when a payout is processed on a Flex funded account? This is C2f; the funded page says nothing about it, and FX-8 does not ask it.
3. **FN-11 detail:** which live-pool rule governs Flex, five cycles on one account or 15 rewards across the profile? What happens to accounts and simulated profit at transition, and when are refunds paid? Does the $10,000 cap limit how many live accounts follow 5 eligible funded accounts? This covers U1a–U1e.
4. **Un-defer FN-12:** does terms 2.2.5 bar one owner from running the same strategy on several own accounts? This is U4b.

**Reading rules (draft, for coordinator adoption):**
1. **Silence counts as no.** At the first cut, an unanswered item reads "pending" and planning treats it as no. At the final cut (10-30) it reads "no". Only written answers count, preferably clause-cited. A chat or phone answer counts only once the firm confirms it by email. A yes that cites no clause, or that answers a different question or stage, is recorded as unresolved. If a reply conflicts with a published page, record both; the more conservative reading governs modelling until the firm reconciles them in writing.
2. **Raw replies stay private,** in Joshua's mailbox or a gitignored store recorded by SHA-256. The public register carries only: firm, stage, question ID, date received, a paraphrase, the cited clause, and quotes under 15 words. It never carries ticket or thread numbers (vendor ticket numbers already on main may appear), names, addresses, account identifiers, figures, P&L or strategy details. The source map behind the IDs stays with the coordinator.
3. **A yes elsewhere does not clear Tradeify.** Tradeify bars the same bot across firms ([replies record](2026-10-10-tradeify-exclusive-use-replies.md); STATE.md:40). A strategy routed to FXIFY or FundedNext is presumed barred at Tradeify, and the reverse, until Tradeify says otherwise in writing.
4. **A reply settles only the item and stage it answers.** No reply clears automation, qualification, parity, protection or recovery, licensing or deployment.
5. **The weekly Tradeify trade is not asked about;** its placement against other firms' hedging rules is Joshua's choice (P5).

**Open check: venue-note §12 Q1–Q8.** The sent status is **UNVERIFIED**:
- No repo record shows a send. #869 §E4 found no sent copy or reply.
- #867's head says "already sent" at sheet :91, :92 and :114 without evidence. That correction has been routed, along with a remap of the #869 sheet's venue-note Q references to #877 IDs.
- #877 supersedes these questions:
  - Q1–Q3 are moot on the native route.
  - Q4 maps to FX-5b, Q5 to FX-3, Q6 to FX-2, and Q7 to FX-7/FX-N2.
  - Q8 maps to FX-N8 only in part: FX-N8 drops Q8's personal-account reuse half.
- Before Email 2 goes out, Joshua confirms whether any of Q1–Q8 went out and by what channel. If any did, Email 2 cites that thread.

**Disclosure check.** #877's open PR already shows the planned instruments and long/short mix in public. Merging adds no new exposure. Joshua decides whether to accept it or to have the #877 author replace those lines with placeholders in a new commit (earlier commits stay visible).

## 3. What changed since 10-16

- **§4 ceiling** is 5.0% (accepted 10-16), which resolves the 3.0%/5.0% conflict. Unchanged: the 50% pass floor, `trailing_locking`, the intraday-honest clock and barrier OFF. "Four FRIENDLY tiers" now reads as the `AUTOMATION_FRIENDLY_PROP_FIRMS` families, five once FXIFY counts.
- **ORB MNQ v7 solo:**
  - Authorized 10-16.
  - Re-ratified 10-18 on all four existing tiers, including Tradeify; FXIFY is excluded (RATIFICATION.md:17). [#868](https://github.com/Joshua-Asante/first-passage/pull/868) merged the exact re-ratified bytes on 10-18, which is the effective-freeze condition (RATIFICATION.md:15).
  - Paused by Joshua (checklist 10-19 :978); S4 stopped at its freeze (ORB owner's ledger, PRIVATE).
  - Whether the 10-30 dated re-MC still runs is an open question for Joshua (P1).
- **Coordination** moved to the Claude deployment coordinator on 10-17. Codex keeps technical execution.
- **Tradeify:**
  - Track B went from SUSPENDED to SUPERSEDED, and D5 closed as a gate (10-16).
  - The native route was chosen, attended, with no strategy bound (10-18; PRIVATE).
  - The book lineage has no evidence case (10-19, #876).
- **FXIFY:**
  - Registration was directed (10-16).
  - The provisional row and rule sheet went up on open #867/#869, with a second agreeing read on 10-17.
  - A 10-19 read found the page stamps and the GTC hash unchanged (source note F1).
- **FundedNext** went from screen-class only to a provisional comparison basis (#877). Its official pages were read 10-19 and several conflict (source note).
- **#877 parked (10-19, PR):** dedicated FLOOR-HALF work is parked pending the CME and firm answers. Joshua approved one two-hour, zero-spend desk reassessment under #877's unchanged criteria. Its decision rule: a CME fee above $500/month selects the NOT PROMISING result on both bases and a stop. Answers return through this register. NinjaTrader execution, protection and recovery work continues through its existing owners.
- **Firm questions** were drafted in #877 and are unsent. They supersede venue-note Q1–Q8.
- **MFFU, Bulenox and BluSky** have no rule changes. The ORB contract covers all four existing tiers, including Tradeify (prereg :80).
- **Personal lane:**
  - FG has not run.
  - Q-SFCLEAR-3 dispatch is paused, and #873 closed unmerged (10-19).
  - #877's step-2 read (10-19) left a Q-SFCLEAR-3 / T00 exposure entry owed (P6).
  - Earlier, on 10-15: #861 and #839 merged.

## 4. Unresolved blockers

Rows T1–T10 come from the coordinator's route-blocker and roadmap records (PRIVATE) unless a row cites otherwise.

| ID | Blocker | Owner | Who can answer |
|---|---|---|---|
| P1 | ORB is paused by Joshua (checklist 10-19 :978); S4 stopped at its freeze (ORB owner's ledger, PRIVATE). #868 merged the exact re-ratified bytes (`16ce2298…`) on 10-18, and the prereg on main hashes to them (checked 10-19). Per RATIFICATION.md:15 that merge is the effective-freeze condition, and the prereg header's wording is immutable history. Open: does the 10-30 dated re-MC, and any scoring release, still run? All scoring and execution holds remain (RATIFICATION.md:17). With no verdict by 11-08, the standing deadline rule applies | Coordinator | Joshua |
| P2 | Draft 11-08 rules are unratified. Branch (a) is withdrawn, (b)'s condition is supported, (c) should point at Q-SFCLEAR-3, and (d) is left to the sitting | Coordinator | Joshua at the sitting |
| P3 | Exclusivity across Tradeify, FXIFY, FundedNext and the personal lane. FundedNext's hedging ban reaches other firms (1.2.21; source note U2-i) | Joshua | Joshua |
| P4 | CME classification for automated (non-display) use. It decides #877's binding D (252 or 126 sessions) and the economics on every basis. No cost figure is used until it is answered | Coordinator (tracking) | CME Data Sales. Last repo-recorded send: 2026-10-12 ([feed-provider-questions :354](2026-10-01-feed-provider-questions-DRAFT.md)). A further follow-up is operator-reported, sent 2026-10-18 (not in repo). Send nothing further |
| P5 | Weekly-trade placement, given FundedNext's hedging bans (1.2.21, 2.2.13) and FXIFY's reverse-trading ban | Joshua | Joshua |
| P6 | Q-SFCLEAR-3 / T00 exposure entry owed from #877's step-2 read (2026-10-19T22:59:59Z), to the T00 lineage manifest and Q-SFCLEAR-3's exposure log (#877 step-2 addendum, PR) | Q-SFCLEAR-3 and T00 owners (coordinator seat holds Q-SFCLEAR-3; Joshua to confirm who writes) | Joshua (confirms the writer) |
| T1 | L1, the CME question for the eval (= P4) | Coordinator | CME |
| T2 | L2: is there a direct-licence clause in the signed Tradovate agreement, and is Managed User Non-Display available for a strategy on a prop-eval login? | Joshua | Joshua (reads the agreement), then Tradovate (draft unsent) |
| T3 | L3: may a strategy submit orders on the eval connection under Tradeify's company NinjaTrader licence, and does Global Simulation Mode hide the account? | Coordinator | Tradeify or NinjaTrader, or an empirical check that needs a GO |
| T4 | L4–L5: licence and connection type, and data status | Joshua | Joshua's screen reads, recording no identifiers |
| T5 | The native-only basis is a support reply with no clause cited | Coordinator (consolidated question set, not started) | Tradeify, in writing |
| T6 | A1–A2: native port (Grant B unapproved) and the instance's own M1; FTA §6.7 hedging, news terms, host hygiene | Joshua | Joshua (the host check is an operator act) |
| T7 | Strategy binding; used-start gate (pristine-start refusal, or a fresh eval); halt-at-pass rule | Joshua | Joshua |
| T8 | Parity v2 (not drafted); broker-side protection proofs (none exist); unattended-operation ADR | Coordinator | Not started |
| T9 | A second order path is still open (c1 rail warm; a third-party order authorization not yet revoked; details in the coordinator's record) | Joshua | Joshua |
| T10 | Dated, durable copies of the FTA and Help Center terms | Coordinator | Not started |
| X1 | #867 merge order: the ledger :2301 rule says #867 does not merge before "the ORB freeze commit". Is #868's 10-18 merge that commit? #867 also conflicts with main (STATE files) | Coordinator | Joshua and the coordinator |
| X2 | Acceptance of §4 condition (c), and the row's byte-verified hold | Coordinator | Coordinator |
| X3 | Commission is unpublished | Any prereg that uses the tier | FXIFY in writing, or a disclosed assumption (conditional research only) |
| X4 | 30-day horizon and extension fee (FX-1); DLL treatment; inactivity not modelled | Prereg owner | FXIFY (FX-1); prereg choice |
| X5 | News conflict D1 (FX-2); B1 eval lock (FX-8); product tradability and cap (FX-3); hedging (FX-N3); funded agreement (FX-N8) | Coordinator | FXIFY (Email 2) |
| X6 | Venue-note Q1–Q8 sent status | Coordinator | Joshua |
| X7 | S1 venue admission; own M1; native port; CME licence | Joshua | Joshua; CME (P4) |
| N1 | Admission path (full expansion ADR, or an addendum like FXIFY's) and the registration writer | Coordinator | Joshua |
| N2 | Email 1 answers (FN-1 to FN-4, FN-9 to FN-11) | Coordinator | FundedNext |
| N3 | Help pages conflict on live-pool entry, account closure and refunds; the terms page has no date | Coordinator | FundedNext; an operator browser save for a dated capture |
| N4 | 16:10 ET flat ruling; an intraday-high MLL trail would need a kernel packet (FN-4); Gate E economics | #877 author | Joshua; FundedNext |
| N5 | Asset Group membership is not published | Coordinator | FundedNext |
| O1 | Is LucidPro still the fallback? | Coordinator | Joshua |
| O2 | MFFU and BluSky facts (07-12/13) are past 90 days. Which date governs staleness, `firm_rules` or the 10-02 envelope? | Coordinator | Coordinator |
| O3 | Does a Tradovate-prop login entitle NinjaScript automation on a firm's eval or funded accounts? The official support articles would not load | Coordinator | NinjaTrader or the firm; an operator browser read |
| O4 | The open #877 PR already publishes instruments and directions; accept, or redact the head | #877 author | Joshua |
| O5 | The Emery originals are reportedly in Hyper AgentMail, which is not available here. Claim wording comes from the EMERY-RESEARCH-DOCS-1 handoff summary; only the 10-19 public re-reads are used | Coordinator | — |

## 5. Stale records (routed to their writers, not edited here)

- `full-e1-execution-slices.md:2287` and `:2295` say #868 is open; it merged 2026-10-18. `:2295` also still reads NOT_READY with "Freeze 10-23; dated re-MC 10-30" and does not record S4's stop at its freeze.
- The checklist (:985, the 10-19 addendum) says #873 is open; it closed unmerged.
- `STATE.md:101` still lists card B (c) and card E as next, and ties T09/T14 to Track B, which is now superseded.
- The #869 sheet :151-152 and the #869 PR body route ownership "under Codex" and to the 10-23 frozen set. Both were changed by the 10-17 transfer and the ratified, merged ORB contract, which excludes FXIFY.
- The #867 sheet :91, :92 and :114 say "already sent"; the status is unverified.
- The #869 sheet (:91, :92, :114, :139, :141, :143, :158) cites venue-note Q numbers that #877 supersedes; remap to FX- IDs.
- `full-e1-execution-slices.md:2295` also says the prereg bytes `7e48d87c…` differ from the ratified contract and are reconciled at the freeze; #868's merge of `16ce2298…` superseded this.
