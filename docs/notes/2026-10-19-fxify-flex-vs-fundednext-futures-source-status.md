# FXIFY Futures Flex vs FundedNext Futures: source, stage and status (2026-10-19)

**Status:** DRAFT for review; documentation only; not an admission, authorization or clearance.

A sanitized research note for the [firm-eligibility register](2026-10-19-firm-eligibility-register-first-cut.md) (handoff EMERY-RESEARCH-DOCS-1). It checks the claims Hyper/Emery reported on 2026-10-19 against the firms' public pages. It changes no rule sheet, row, strategy or gate.

**Related:** [Tradeify checklist addendum 2026-10-19](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-10-19--no-book-lineage-configuration-has-an-evidence-case-for-the-tradeify-evaluation) (merged [#876](https://github.com/Joshua-Asante/first-passage/pull/876)) · [four-firm ADR](../adr/2026-07-12-prop-portfolio-four-friendly-firms.md#addendum-2026-10-16--operator-rulings-50-ceiling-fresh-4-candidate-orb-mnq-v7-fxify-futures-flex-registration-accepted) (addendum 2026-10-16).

**Provenance:** claim wording is taken from the EMERY-RESEARCH-DOCS-1 handoff summary (Joshua confirmed the documentation-only relay; the relay did not independently verify the claims), not the originals; the labels test that wording. The originals are reportedly held in Hyper AgentMail and were not available. Every page cited was seen 2026-10-19. A second read that day re-checked the FundedNext terms (1.2.15, 1.2.17, 1.2.21, 2.2.6, 2.2.13; no page date) and help articles 17229807, 16522296 and 15430139. The GTC PDF hash comes from the first 10-19 read, whose fetch method was not recorded; a later scripted fetch got HTTP 403, so the hash was not re-checked.

**Status labels:**
- **SUPPORTED:** the page says it.
- **NARROWER:** the page supports a narrower statement than the claim.
- **CONTRADICTED:** the page contradicts the claim, or the firm's pages contradict each other.
- **UNVERIFIABLE:** no public page read on 2026-10-19 settles it.

**Stage codes:** E is evaluation, F is sim-funded, L is live.

FN = `https://helpfutures.fundednext.com/en/articles/`; FX = `https://fxifyfutures.com/faqs/general-rules/`.

## 1. Claims and items

| ID | Claim or item | Source | Seen | Stage | Status | What the source says (paraphrase) |
|---|---|---|---|---|---|---|
| C1 | The FundedNext Flex funded account concludes after the 5th Performance Reward; no automatic live transition | FN `17229848-fundednext-futures-flex-fundednext-account-all-rules` (modified 2026-09-30); FN `17229807` | 2026-10-19 | F | SUPPORTED | The account concludes after five rewards, and the page says nothing about what follows. Live entry is through a review pool at the firm's sole discretion. The MLL locks at initial balance + $100 |
| C2 | The FXIFY MLL locks at the starting balance when profit reaches the initial cushion, or when a payout is processed | FX `what-is-the-maximum-loss-limit-mll/` (updated 2026-09-28) | 2026-10-19 | E | SUPPORTED | EOD trailing limit. Either trigger locks it permanently at the starting balance. The value tables cover Flex (Evaluation) and Direct; the lock section names no plan. The FXIFY sheet (#867/#869 §A2, B1) already reads both triggers |
| C2f | The same lock on Flex funded accounts | FX `funded-account-parameters-overview/` (updated 2026-09-28) | 2026-10-19 | F | UNVERIFIABLE | The funded page gives the Flex funded limit as EOD trailing and says nothing about a lock. The payout trigger can fire only at a stage that has payouts. FX-8 asks whether the lock applies in the evaluation or only on Flex Funded; it does not ask the payout limb |
| C3a | FundedNext terms 2.1.7: a different dashboard or trading IP needs prior approval | https://fundednext.com/futures-challenge-terms | 2026-10-19 | E, F (live not mentioned) | SUPPORTED | Using different IPs for dashboard and trading needs prior approval. Mismatches may be treated as account sharing and restricted. No approval process is described |
| C3b-i | Terms 2.2.6: automation is allowed; the firm may require the execution system and materials for review | same | 2026-10-19 | E, F | SUPPORTED | Bots, AI and high-speed execution are allowed, and violating systems are disabled. The firm may ask to review the system used to execute trades, and the trader must share necessary materials |
| C3b-ii | 2.2.6 is not a blanket source-code disclosure | same | 2026-10-19 | E, F | UNVERIFIABLE | Code is neither named nor excluded. "System" and "materials" are undefined, so the firm's possible reach is broader than the claim. FN-9 asks |
| C3c | The terms were updated 2026-09-25 | same | 2026-10-19 | — | UNVERIFIABLE | The page shows no updated or effective date and carries no date metadata. A dated capture is needed before a row cites it |
| U1a | Live-pool entry: five cycles on one account, or 15 rewards across the profile | FN `17229807` (modified 2026-10-14); FN `16522296` (modified 2026-10-07); FN `15430139` (dated 2026-08-15, unlabelled) | 2026-10-19 | F→L | CONTRADICTED | 17229807 gives three alternative routes, one of which is five cycles from one account, with no guarantee of entry. The other two pages require 15 rewards across the profile, with transitions only at the end of a cycle and no guarantee |
| U1b | What happens to accounts at transition | same three | 2026-10-19 | E, F→L | CONTRADICTED | 17229807 says all existing funded accounts conclude. The other two say Challenge accounts and zero-payout funded accounts close, and accounts with a withdrawal convert to live |
| U1c | Refund at transition | FN `16522296`; FN `15430139` (dated 2026-08-15, unlabelled); terms §4 | 2026-10-19 | F→L | CONTRADICTED | One page says zero-payout funded accounts are refunded in 3–5 business days; another says within 24 hours. Terms §4 says all transactions are final, with no carve-out |
| U1d | Simulated profit is forfeited at transition | FN `17229807` | 2026-10-19 | F→L | SUPPORTED | Stated on a single page; the other two pages say nothing about it. Do not combine this with U1b or U1c |
| U1e | Live deposit cap | FN `17229807`; FN `16522296`; FN `15430139` | 2026-10-19 | L | SUPPORTED (single page); fit with the 5-account / $4,500 balances UNVERIFIABLE | A single page caps cumulative live deposits across combined Flex accounts at $10,000. The others list live starting balances ($4,500 at 150K) and up to five live accounts; five at $4,500 would exceed the cap unless "deposit" means something else. How they fit is not stated |
| U2-i | Correlated-hedging ban, within and across accounts and with other firms | FN `14298337` (modified 2026-09-30); terms 1.2.21, 2.2.13 | 2026-10-19 | All | SUPPORTED | Opposing positions on co-moving instruments in one Asset Group are barred, within one account or across accounts, at any stage. Terms 2.2.13 bars hedging correlated instruments across accounts; 1.2.21 bars cross-account hedging within FundedNext or with other firms. The rule is about opposing positions, not about holding several instruments |
| U2-ii | Asset Group and correlated-instrument membership | same | 2026-10-19 | All | UNVERIFIABLE | Neither "Asset Group" nor "correlated instruments" is defined, and no page lists group membership |
| U3 | FXIFY news policy vs the EA ban | FX `news-trading-policy/`; FX `can-i-use-eas-expert-advisors-to-trade/` (both updated 2026-09-28); https://fxifyfutures.com/terms-and-conditions/ (PDF) | 2026-10-19 | Stages not separated | CONTRADICTED | The news page allows news trading, defines no window and does not mention EAs. The EA page lists news trading among EA behaviours that breach immediately, and says EAs need no prior permission on Flex or Direct. The GTC 5.4.1.6 gap clause is present, and the PDF sha256 matched the sheet's `c25d2fa8…abfc72f` (fetch method not recorded; not re-checked). This matches sheet D1 |
| U4a | FXIFY same-owner copying vs independent execution | FX `does-fxify-futures-allow-copy-trading/` (updated 2026-09-28) | 2026-10-19 | Stages not separated | NARROWER | Copying among the owner's own accounts, including from a personal or other-firm account, is allowed; third-party copying is an immediate breach. No account limit is given. Running the same strategy independently is not addressed, and copying in does not establish copying out |
| U4b | FundedNext same-owner copying | FN `17230319` (modified 2026-09-30); terms 2.1.3, 2.2.5 | 2026-10-19 | Stages not separated | NARROWER | The article allows copying your own trades, including across firms, if you own every account and the names match. Third-party copying, group trading and signal services are barred. Terms 2.2.5 forbids coordinating trades among multiple accounts without mentioning other people, which may conflict with the article. Independent execution is not addressed |
| U5a | NinjaScript automation through a Tradovate prop login | https://prop.ninjatrader.com/tradovate-prop-to-ninjatrader-login/ (no date) | 2026-10-19 | Not stated | NARROWER | The page says the login unlocks NinjaTrader interfaces, including NinjaScript strategy automation, with no new plan. It names no firm, stage or licence key. It shows what the platform can do, not what a firm permits. No paid-key blocker is stated, and none is inferred |
| U5b | NinjaTrader support articles on licence keys and evaluation connections | https://support.ninjatrader.com/s/article/How-Migrate-License-Key-Into-Latest-Version-NinjaTrader-Desktop; https://support.ninjatrader.com/s/article/Connecting-To-Evaluation-Services-via-Tradovate-Connection | 2026-10-19 | — | UNVERIFIABLE | Both returned only an error shell, and search found no official copy. Search-index results and forum posts are not evidence. This needs an operator browser read or a vendor or firm answer |
| F1 | FXIFY sheet freshness (sheet D2) | The FX pages above and the GTC PDF | 2026-10-19 | E | SUPPORTED | The MLL, EA, news, copy-trading and funded-parameters pages are still stamped 2026-09-28, and the PDF hash is unchanged (fetch method as in U3). The fee, DLL, time-limit and hours pages were not re-read. A re-read is still owed at the freeze of any pre-registration that uses this tier |

## 2. Side by side

| Item | FXIFY Futures Flex | FundedNext Futures Flex |
|---|---|---|
| Automation | Enabled by default on supported platforms; no permission needed (U3) | Allowed; the system and materials may be reviewed, scope undefined (C3b-i, C3b-ii) |
| Hosting / IP | VPS not addressed on the EA page; no page read addresses it (#869 §A5, PR) | A different dashboard and trading IP needs prior approval (C3a) |
| News | Conflict: general page allows it, EA page makes it a breach (U3) | No public news rule read; deferred question FN-7 |
| Opposing positions | Reverse trading across accounts banned (sheet §A5, PR) | Correlated hedging banned within and across accounts, and with other firms (1.2.21); groups undefined (U2-i, U2-ii) |
| Own-account copying | Allowed (U4a) | Allowed by the article; terms 2.2.5 unclear (U4b) |
| Same strategy run independently | Not addressed (U4a) | Not addressed (U4b) |
| Drawdown lock | Starting balance, either trigger; funded lock not stated (C2, C2f) | Trails on EOD high and stops at starting balance + $100, on both the Flex Challenge (terms §1.2, seen 2026-10-19) and the funded account (C1); FN-4 (intraday vs EOD high) stays open |
| End state | Funded agreement unread (FX-N8) | Funded account concludes after 5 rewards; live entry discretionary, pages conflict (C1, U1a–U1e) |
| Page dating | FAQ stamps 2026-09-28; GTC Dec 2024 | Help articles dated (15430139 unlabelled); terms page undated (C3c) |

## 3. Repo consistency

- The FXIFY rule sheet (#867/#869) and the provisional row `FXIFY_Futures_Flex_150K` (#867) do not conflict with any source above. The row's `dd_lock_offset_usd 0.0` matches C2.
- Narrow wording corrections are routed to the sheet writers: freshness (F1), copy scope (U4a), funded-lock silence (C2f), and a remap of the sheet's venue-note Q references to #877's FX- IDs. This note does not edit the sheet.
- FundedNext has no row and no sheet. The venue note's generic-permission label is consistent with C3b-i.

## 4. Not checked in this pass

- **FundedNext figures in #877 §3:** the MLL amount, the target, consistency, the cap, the 16:10 ET flat, fees (the fee pages reportedly conflict) and the reward ceiling. The terms' Challenge MLL basis is in the side by side; FN-4 stays open.
- **FXIFY pages last read 2026-10-17 (#869 §E):** fee, target, DLL, time limit and hours.

## 5. CME clarification

The CME classification of automated (non-display) data use is pending with CME Data Sales. The last repo-recorded send is 2026-10-12 ([feed-provider-questions :354](2026-10-01-feed-provider-questions-DRAFT.md)). A further follow-up is operator-reported, sent 2026-10-18 (not in repo); send nothing further. This note uses no cost figure, and the withdrawn per-exchange estimate is not used. The answer decides which maximum evaluation duration D (252 or 126 sessions) binds in #877, and the economics on every basis.

## 6. Interpretation boundaries

Interpretation boundaries stated in the EMERY-RESEARCH-DOCS-1 handoff (Joshua via Session Relay); not verified here, except the ORB line, which cites its owner records.

- ORB MNQ v7 solo is paused by Joshua (checklist 10-19 :978); S4 stopped at its freeze (ORB owner's ledger, PRIVATE).
- No fixed leg count or contract size is required.
- Native engineering and lawful offline qualification need not wait for every live or scale issue to be settled.
- IP and portfolio conditions gate actual pilots.
- A firm that publishes no account end state is not promising the account runs indefinitely.
- Research continues during deployment.
- TradingView Premium is a conditional research feature, not a runtime dependency.
- CrossTrade is outside the native order chain.
- Live, warmup, reconnect, replay, parity and offline data rights are separate questions, and each needs its own answer.

## 7. What this does not clear

This note and the Emery reports do not clear any of the following:
- actual-live automation at either firm;
- qualification of any strategy or configuration;
- parity, protection or recovery;
- data licensing;
- venue admission (S1) or deployment.

A firm's yes on running the same strategy elsewhere does not clear Tradeify. Simulated evidence is not live clearance.
