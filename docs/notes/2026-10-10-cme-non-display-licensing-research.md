# CME non-display licensing for the personal Tradovate lane: what CME's own documents say (research, 2026-10-10)

**Status:** research note for the Deployment Coordinator, at Joshua's request to find CME's answer while CME's written reply is pending. **A documented reading is not CME's written determination.** Whether to proceed on it with residual risk is Joshua's call at CP-7.
**Serves (Rule 7):** [ADR 2026-10-09](../adr/2026-10-09-self-funded-tradovate-lane-reopen.md) Decision 3 and owed item 4; the CME draft in the [narrowed note §4.0](2026-10-03-feed-provider-questions-narrowed-DRAFT.md#40-cme-group-market-data-licensing-send-first) (reframed by PR #767); the [#583 note §4.1](2026-10-01-feed-provider-questions-DRAFT.md#4-recording-the-answers) answer table (PR #768). It edits none of them.

**Evidence limit (read first).** This session's network policy denied `www.cmegroup.com`, `*.tradovate.com`, `vendor-support.ninjatrader.com` and `web.archive.org` (proxy CONNECT 403; WebFetch DNS failure). **No primary source was re-read on the page today.** The answers below therefore rest on:
- **[pdf-10-03]** CME documents CM1–CM8, read in full in a browser on 2026-10-03 and paraphrased with clause locators in the [matrix](2026-10-03-feed-provider-questions-narrowed-matrix.md#cme-group-licensor-cme-lic-and-direct-products-p7a-p7b). Quotes there are paraphrases except where marked; this note quotes only the one verbatim phrase the matrix holds.
- **[T1]** Tradovate support's AI-generated reply of 2026-10-04 (#583 §4.1), and the Tradovate KB lines TV1/TV2, which are search excerpts only.
- **[lead]** WebSearch excerpts retrieved today. Leads, never answers.

Because the 15-words-or-fewer quote standard needs the text on the page, every DOCUMENTED label below is **DOCUMENTED (10-03 paraphrase)**: the contract states it per the page-verified 10-03 read, and the exact wording is still to be quoted from the page.

Sources: CM1 [non-display policy guidelines and FAQ, Jan 2025](https://www.cmegroup.com/market-data/distributor/files/cme-group-data-licensing-policy-guidelines-and-non-display-licensing-faq.pdf); CM2 [Schedule 5 v5.04, Jan 2026](https://www.cmegroup.com/market-data/files/schedule-5-to-the-ila-january-2026.pdf) and CM2b [v5.06, Aug 2026, current](https://www.cmegroup.com/market-data/files/schedule-5-to-the-ila-august-2026.pdf); CM3 [fee list Jan 2026](https://www.cmegroup.com/market-data/files/january-2026-market-data-fee-list.pdf); CM4 [fee list Jan 2027](https://www.cmegroup.com/market-data/files/january-2027-market-data-fee-list.pdf); CM5 [fee list Jun 2026](https://www.cmegroup.com/market-data/files/june-2026-market-data-fee-list.pdf); CM6 [DS-45 licence updates, effective 2026-09-17](https://www.cmegroup.com/market-data/files/market-data-license-agreement-updates-june-2026.pdf); CM7 [ILA v5.02, Jun 2026](https://www.cmegroup.com/market-data/files/information-license-agreement-june-2026.pdf); CM8 [Information Policies v5.04](https://www.cmegroup.com/market-data/files/information-policies-v5-04.pdf). New lead CM9a [ILA Subscriber Addendum, Jun 2026](https://www.cmegroup.com/market-data/files/ILA-Subscriber-Addendum-june-2026.pdf) (not read).

## 1. Licence route and category

| Point | Answer | Clause (version, date) | Label |
|---|---|---|---|
| Is the use non-display, Category A? | Yes: automated trading systems are non-display use; Category A is automated use to trade | CM1 §"What is Non-Display?", §Categories (Jan 2025) | DOCUMENTED (10-03 paraphrase) |
| Does CME's contract require the non-pro subscriber's own licence? | Schedule 5 bars a distributor from supplying automated use to subscribers **other than** non-professionals without a direct CME licence. It is silent on whether a non-pro still needs one | CM2 §3.3 (v5.04; owner check: unchanged in v5.06) | DOCUMENTED (carve-out) / OPEN (whether a licence is still owed) |
| Conflicting CME text | CM1 says all non-display use is licensed directly with CME, whatever the source (FAQ Q10). **New lead:** the ILA Subscriber Addendum §4.2 reportedly says the same | CM1 §Licensing requirements, Q10; CM9a §4.2 [lead] | CONFLICT (FAQ and addendum vs §3.3) |
| What Tradovate requires | Real-time API data requires the user to sign the CME ILA as a sub-vendor; order-only use does not | TV1 [excerpt]; T1 (2026-10-04, AI-generated) | INFERENCE (excerpt + AI reply) |
| **Net route** | **Own ILA needed in practice.** Tradovate's own policy is stricter than §3.3's floor, and the FAQ and (reportedly) the addendum agree. The §3.3 carve-out does not help on this route | — | INFERENCE |
| Which category | A8 User Non-Display applies to a licensee who is a single natural user. A9 Managed User needs a CME-authorized distributor service for an individual, and the distributor must provide "the means to route automated orders" to CME markets. A1 is the general Category A licence | CM3 notes 8–9; CM2 definitions, §11.2 (v5.04/v5.06) | DOCUMENTED (10-03 paraphrase) for the tests; OPEN whether Tradovate's ILA flow is an authorized Managed User service |
| Fee basis | Per exchange (per DCM), monthly, not pro-rated. Three DCMs here: CME (6J, MNQ), CBOT (MYM), COMEX (MGC) | CM3 header; CM1 Q9, Q14 | DOCUMENTED (10-03 paraphrase) |
| Amounts per exchange per month | A8 $457 (Jan and Jun 2026), $472 (Jan 2027). A9 $208, $215 (Jan 2027). A1 Basic $609 (2026) | CM3, CM5, CM4 | DOCUMENTED (10-03 read) |

**CME must confirm:** whether a non-pro on a broker's data needs an own licence (FAQ/addendum vs §3.3); whether Tradovate's sub-vendor ILA flow is A8 or A9; any base ILA fee, setup, minimum term, deposit or audit duty.

## 2. The evaluation destination

| Point | Answer | Clause | Label |
|---|---|---|---|
| A1 vs A3 | A-1 is trading as principal on a CME Group exchange; A-3 is trading on venues other than a CME exchange | CM1 §Categories | DOCUMENTED (10-03 paraphrase) |
| Fit for a simulated evaluation | Neither fits literally: a simulated environment must prevent orders reaching the exchange, so evaluation orders reach no venue. The fee is per DCM whose data is used, not per destination (Q14), so an evaluation destination on the same data plausibly adds **no** category or fee. A3 Basic is $1,820 per exchange, so a wrong reading is costly | CM8 §7.1; CM1 Q14; CM3 | INFERENCE |
| §7.3 duty | A **distributor** needs CME's prior written consent to offer data in a simulated environment leading to capital allocation or profit sharing. On its face it binds the firm or platform running the evaluation, not a data subscriber's separate feed | CM8 §7.3 (v5.04) | DOCUMENTED (who it binds, 10-03 paraphrase) / INFERENCE (not the subscriber) |
| §7.1 | Defines simulated trading environments and the no-exchange-routing requirement; imposes nothing on the subscriber in the 10-03 read | CM8 §7.1 | DOCUMENTED (10-03 paraphrase) |

**CME must confirm:** the category (A1, A3 or none extra) when automated orders go to a simulated evaluation account; that §7.3 places no duty on the subscriber.

## 3. Non-professional status

| Point | Answer | Clause | Label |
|---|---|---|---|
| Own-assets trading | Meets §8.2: use is personal, limited to the subscriber's own assets, not managing third-party assets | CM2 §8.2 (v5.04; unchanged in substance, v5.06 per owner check) | DOCUMENTED (10-03 paraphrase) for the personal account |
| Other §8.1 conditions | Active futures account (yes), individual (yes), no membership or registration (operator to confirm), no financial-institution role, data through at most two order-routing devices from the distributor (an API session plus a platform login: count unknown) | CM2 §8.1 | DOCUMENTED test / OPEN on the device count |
| Effect of the evaluation destination | Unaddressed. The evaluation account is the firm's, and its capital is simulated, so §8.2's "third party's assets" may or may not reach it | CM2 §8.2(c) | OPEN |
| What status changes | In the text, §8 governs **fees**; it decides §3.3's carve-out only by inference. On the own-ILA route, status mainly moves the fee class | CM2 §3.3, §8 | INFERENCE |

**CME must confirm:** that orders into a third-party prop evaluation account do not make the subscriber professional under §8.2.

## 4. Internally built 15-minute bars and retention

| Point | Answer | Clause | Label |
|---|---|---|---|
| Direct ILA (A8/A1) | Limited derivative works for internal business purposes, disclosed internally only, are allowed, but never a Synthetic Feed: a feed or price stream that mimics, simulates or substitutes for a CME feed. Internal, undistributed bars that only feed decisions are plausibly not a Synthetic Feed | CM7 ILA §2.1(c) (v5.02, Jun 2026; effective 2026-09-17 per CM6) | DOCUMENTED rule / INFERENCE on the bars |
| A9 Managed User | Viewable display, distribution and **creation of derivative works** are not permitted under A9. Whether internal bars are "derivative works" there is not stated. **A9 may be incompatible with the design** unless CME rules otherwise | CM2/CM2b §11.3 (v5.04 and v5.06) | DOCUMENTED bar / OPEN on the bars |
| Retention after termination | Purge all data on termination, except data kept under law or regulation per pre-existing internal compliance requirements, or as the agreement expressly permits. Separately, records are kept during the term and at least 24 months after | CM7 §5.7, §5.7(a), §8.1 | DOCUMENTED (10-03 paraphrase). No express permission for audit copies: INFERENCE that raw data and bars must be purged |
| ML/AI clause | The ML/AI/LLM prohibition is wording for public-website terms of use | CM6 App. 2, Website Display §1.1(c); Schedule 5 §7 (v5.06) | DOCUMENTED location / INFERENCE that it does not reach non-display use |

**CME must confirm:** bars are an internal derivative work, not a Synthetic Feed; whether §11.3 excludes them under A9; whether audit copies may survive termination.

## 5. Tradovate's own requirements

| Point | Answer | Source | Label |
|---|---|---|---|
| Data licence | Tradovate's licence does not cover API data; the user signs the CME ILA (sub-vendor) | TV1 [excerpt]; T1 | INFERENCE (excerpt + AI reply) |
| Account eligibility | Prop and evaluation accounts cannot get API access; a live funded account is required | TV2 [excerpt] | INFERENCE (excerpt) |
| Costs (per reply, unverified) | API add-on $25/month (access and orders, **no** real-time data); $1,000 funded balance to create a key; Level I non-pro data $12/month bundle or $4 per exchange; CME ILA fee not stated | T1 | INFERENCE (unverified) |
| Is the API data package licensed for non-display automated use? | Not by Tradovate: the use rests on the subscriber's own CME ILA | TV1; T1 | INFERENCE |
| Sub-vendor ILA flow | Steps, and whether it yields A8 or A9: not found. Lead: a community thread on CME vendor registration for WebSocket data | [community.tradovate.com t/11320](https://community.tradovate.com/t/how-to-do-the-cme-vendor-registration-for-market-data-access-via-websocket/11320) [lead] | OPEN |

## 6. Reconciliation with the feed notes

No disagreement with the CM1–CM8 facts in the [narrowed note §Summary item 1](2026-10-03-feed-provider-questions-narrowed-DRAFT.md#summary) or the matrix CME-LIC rows; this note restates them. Differences:
1. **New conflicting source:** the ILA Subscriber Addendum (June 2026) §4.2 reportedly requires a direct CME licence for all non-display use [lead]. Neither note cites it. If confirmed, it strengthens the FAQ side of the §3.3 conflict.
2. **Emphasis:** the notes keep "own licence vs §3.3 carve-out" open. For the Tradovate route that question is moot: Tradovate requires the ILA regardless (TV1, T1). It stays live for other routes.
3. **A9 and bars:** the notes flag §11.3 as a gap. Read with ILA §2.1(c), A9 is the cheaper licence but may forbid the design; A8 is the safe reading.
4. **Fee lists:** the 10-03 read has no January 2027 A1 Basic figure; the A1 2027 amount below is unknown.

## 7. What CME must still confirm

1. Own licence for a non-pro on a broker's data: FAQ Q10 and Addendum §4.2 vs Schedule 5 §3.3.
2. Category: A8, A9 (does Tradovate's flow qualify under §11.2?) or A1.
3. The evaluation destination: extra category (A1/A3) or none; §7.3 not binding the subscriber.
4. Status: the evaluation destination and §8.2(c); the §8.1 device count.
5. Bars: internal derivative work under §2.1(c), not a Synthetic Feed; under A9, outside §11.3.
6. Retention of raw messages and bars after termination (§5.7).
7. Base ILA, setup, minimum term, deposit and audit terms for an individual.

## 8. Recommendation: minimum licence path

**Path:** Joshua signs the CME ILA through Tradovate's sub-vendor flow as a single natural user, **User Non-Display A8**, Category A, for the three DCMs (CME, CBOT, COMEX); declare the evaluation destination in the application. A9 only if CME confirms in writing that Tradovate's flow qualifies and that internal bars fall outside §11.3.

| Path | Per exchange | Three DCMs, 2026 | From Jan 2027 |
|---|---|---|---|
| A9 Managed User (only if confirmed) | $208 | $624 | $645 |
| **A8 User Non-Display (recommended)** | $457 | **$1,371** | **$1,416** |
| A1 Basic (if CME requires it) | $609 | $1,827 | not read |

Plus Tradovate's API add-on and data entitlements (T1, unverified). Feed fees are outside the $700 ceiling (D-Q1, D-Q7). **Monthly range: about $624–$1,827, most likely $1,371 ($1,416 from January 2027).** A wrong A3 reading would be $5,460.

## 9. Verification

- Network: `curl` to `www.cmegroup.com` → proxy CONNECT 403 (policy); WebFetch → `ENOTFOUND`; `*.tradovate.com`, `vendor-support.ninjatrader.com`, `web.archive.org` unreachable. No page read today. Owed: Joshua (or a session with `cmegroup.com` egress) quotes §3.3, §8.2, §11.2–§11.3, ILA §2.1(c)/§5.7, Information Policies §7.1/§7.3 and Addendum §4.2 from the page.
- Leads used (excerpts only): WebSearch for the Schedule 5 Managed User clause, the ILA Subscriber Addendum, and Tradovate sub-vendor threads.
- No login, form, chat, email or contact. No GLM.
