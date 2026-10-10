# CME non-display licensing for the personal Tradovate lane: what CME's own documents say (research, 2026-10-10)

**Status:** research note for the Deployment Coordinator, at Joshua's request to find CME's answer while CME's written reply is pending. **A documented reading is not CME's written determination.** Whether to proceed on it with residual risk is Joshua's call at CP-7.
**Serves (Rule 7):** [ADR 2026-10-09](../adr/2026-10-09-self-funded-tradovate-lane-reopen.md) Decision 3 and owed item 4; the CME draft in the [narrowed note §4.0](2026-10-03-feed-provider-questions-narrowed-DRAFT.md#40-cme-group-market-data-licensing-send-first) (reframed by PR #767); the [#583 note §4.1](2026-10-01-feed-provider-questions-DRAFT.md#4-recording-the-answers) answer table (PR #768). It edits none of them.

**Evidence limit (read first).** After Joshua allowed the hosts, `www.cmegroup.com` itself answered HTTP 403: "This IP address is blocked due to suspected web scraping activity", citing CME's website terms, which prohibit automated access. The block was not circumvented. **No CME document was re-read on the page today.** The Tradovate knowledge-base pages were read in full on 2026-10-10 in headless Chromium. Sources:
- **[pdf-10-03]** CME documents CM1–CM8, read in full in a browser on 2026-10-03 and paraphrased with clause locators in the [matrix](2026-10-03-feed-provider-questions-narrowed-matrix.md#cme-group-licensor-cme-lic-and-direct-products-p7a-p7b). Quotes there are paraphrases except where marked; this note quotes only the one verbatim phrase the matrix holds.
- **[page-10-10]** TV1 [Tradovate API Access](https://vendor-support.ninjatrader.com/s/article/Tradovate-API-Access?language=en_US) (dated Sep 16, 2026); TV2 [Prop Firm and Evaluation Account Inquiries](https://vendor-support.ninjatrader.com/s/article/Prop-Firm-and-Evaluation-Account-Inquiries-Tradovate?language=en_US) (Sep 29, 2026); TV3 [Non-Professional Monthly Data Rates](https://vendor-support.ninjatrader.com/s/article/Non-Professional-Monthly-Data-Rates-Tradovate?language=en_US) (Nov 29, 2024).
- **[T1]** Tradovate support's AI-generated reply of 2026-10-04 (#583 §4.1).
- **[lead]** WebSearch excerpts and community threads. Leads, never answers.

Because the 15-words-or-fewer quote standard needs the text on the page, every DOCUMENTED label on a CME clause is **DOCUMENTED (10-03 paraphrase)**: the contract states it per the page-verified 10-03 read, and the exact wording is still to be quoted from the page. Tradovate rows marked "(Tradovate page, 10-10)" carry quotes copied from the page.

Sources: CM1 [non-display policy guidelines and FAQ, Jan 2025](https://www.cmegroup.com/market-data/distributor/files/cme-group-data-licensing-policy-guidelines-and-non-display-licensing-faq.pdf); CM2 [Schedule 5 v5.04, Jan 2026](https://www.cmegroup.com/market-data/files/schedule-5-to-the-ila-january-2026.pdf) and CM2b [v5.06, Aug 2026, current](https://www.cmegroup.com/market-data/files/schedule-5-to-the-ila-august-2026.pdf); CM3 [fee list Jan 2026](https://www.cmegroup.com/market-data/files/january-2026-market-data-fee-list.pdf); CM4 [fee list Jan 2027](https://www.cmegroup.com/market-data/files/january-2027-market-data-fee-list.pdf); CM5 [fee list Jun 2026](https://www.cmegroup.com/market-data/files/june-2026-market-data-fee-list.pdf); CM6 [DS-45 licence updates, effective 2026-09-17](https://www.cmegroup.com/market-data/files/market-data-license-agreement-updates-june-2026.pdf); CM7 [ILA v5.02, Jun 2026](https://www.cmegroup.com/market-data/files/information-license-agreement-june-2026.pdf); CM8 [Information Policies v5.04](https://www.cmegroup.com/market-data/files/information-policies-v5-04.pdf). New lead CM9a [ILA Subscriber Addendum, Jun 2026](https://www.cmegroup.com/market-data/files/ILA-Subscriber-Addendum-june-2026.pdf) (not read).

## 1. Licence route and category

| Point | Answer | Clause (version, date) | Label |
|---|---|---|---|
| Is the use non-display, Category A? | Yes: automated trading systems are non-display use; Category A is automated use to trade | CM1 §"What is Non-Display?", §Categories (Jan 2025) | DOCUMENTED (10-03 paraphrase) |
| Does CME's contract require the non-pro subscriber's own licence? | Schedule 5 bars a distributor from supplying automated use to subscribers **other than** non-professionals without a direct CME licence. It is silent on whether a non-pro still needs one | CM2 §3.3 (v5.04; owner check: unchanged in v5.06) | DOCUMENTED (carve-out) / OPEN (whether a licence is still owed) |
| Conflicting CME text | CM1 says all non-display use is licensed directly with CME, whatever the source (FAQ Q10). **New lead:** the ILA Subscriber Addendum §4.2 reportedly says the same | CM1 §Licensing requirements, Q10; CM9a §4.2 [lead] | CONFLICT (FAQ and addendum vs §3.3) |
| What Tradovate requires | Real-time API data: user "must become a sub-vendor with the CME by signing the CME Information License Agreement". Order-only use: "the sub-vendor requirement and ILA do not apply" | TV1 §Accessing Market Data (Sep 16, 2026) | DOCUMENTED (Tradovate page, 10-10) |
| **Net route** | **Own ILA needed in practice.** Tradovate's own policy (documented) is stricter than §3.3's floor, and the FAQ and (reportedly) the addendum agree. The §3.3 carve-out does not help on this route | TV1; CM1 | DOCUMENTED (Tradovate's requirement) / INFERENCE (that CME agrees) |
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
| Is the evaluation simulated? | Yes, per Tradovate: evaluation accounts sit in the simulation environment, "Simulation (paper trading) evaluation or prop firm accounts" | TV2 §Scope of Tradovate Support (Sep 29, 2026) | DOCUMENTED (Tradovate page, 10-10) |
| §7.1 | Defines simulated trading environments and the no-exchange-routing requirement; imposes nothing on the subscriber in the 10-03 read | CM8 §7.1 | DOCUMENTED (10-03 paraphrase) |

**CME must confirm:** the category (A1, A3 or none extra) when automated orders go to a simulated evaluation account; that §7.3 places no duty on the subscriber.

## 3. Non-professional status

| Point | Answer | Clause | Label |
|---|---|---|---|
| Own-assets trading | Meets §8.2: use is personal, limited to the subscriber's own assets, not managing third-party assets | CM2 §8.2 (v5.04; unchanged in substance, v5.06 per owner check) | DOCUMENTED (10-03 paraphrase) for the personal account |
| Other §8.1 conditions | Active futures account (yes), individual (yes), no membership or registration (operator to confirm), no financial-institution role, data through at most two order-routing devices from the distributor (an API session plus a platform login: count unknown) | CM2 §8.1 | DOCUMENTED test / OPEN on the device count |
| Effect of the evaluation destination | CME is silent. Tradovate says of prop accounts "your provider is the account owner", so the account is a third party's; its capital is simulated. Whether §8.2's "third party's assets" reaches simulated capital is not stated | CM2 §8.2(c); TV2 §Scope (Sep 29, 2026) | OPEN (ownership DOCUMENTED by Tradovate) |
| Status inside the evaluation | Separate from the personal account: on a prop login, the status chosen in Tradovate's Market Data Subscriber Certification "can only be changed by your account provider" | TV2 §Getting Started | DOCUMENTED (Tradovate page, 10-10) |
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
| Data licence | API data needs the user's own CME ILA as sub-vendor (§1 quote). "The Tradovate API Add-on does not provide access to real-time market data" | TV1 (Sep 16, 2026) | DOCUMENTED (Tradovate page, 10-10) |
| Account eligibility | "Prop firm and evaluation accounts are not eligible for API access." A live funded brokerage account is required, so the evaluation destination cannot itself use the API | TV1 §Important Notes | DOCUMENTED (Tradovate page, 10-10) |
| API costs | API Access add-on "$25/month"; key needs "a minimum balance of $1,000" and an active add-on; keys carry selectable permissions; an attestation and a digital agreement precede the key | TV1 §Subscribing, §Generating | DOCUMENTED (Tradovate page, 10-10). Whether the $1,000 must be held afterwards: not stated |
| Ordinary data fees (display) | Non-pro Level 1: $4.00 per exchange (CME, CBOT, COMEX), $12.00 for the four-exchange bundle | TV3 (Nov 29, 2024) | DOCUMENTED (Tradovate page, 10-10). Whether API use also needs this subscription: not stated |
| Is the API data package licensed for non-display automated use? | No Tradovate package covers it: the API data rests on the subscriber's own CME ILA | TV1 | DOCUMENTED (Tradovate page) |
| Sub-vendor ILA flow | Not described: TV1 links the ILA and refers questions to Tradovate's API support. Which category (A8 or A9) it yields, and the steps, are not stated. Users in a 2025 community thread report contacting CME directly and paying about $450/month [lead] | TV1; [community.tradovate.com t/11320](https://community.tradovate.com/t/how-to-do-the-cme-vendor-registration-for-market-data-access-via-websocket/11320) [lead] | OPEN |

## 6. Reconciliation with the feed notes

No disagreement with the CM1–CM8 facts in the [narrowed note §Summary item 1](2026-10-03-feed-provider-questions-narrowed-DRAFT.md#summary) or the matrix CME-LIC rows; this note restates them. Differences:
1. **New conflicting source:** the ILA Subscriber Addendum (June 2026) §4.2 reportedly requires a direct CME licence for all non-display use [lead]. Neither note cites it. If confirmed, it strengthens the FAQ side of the §3.3 conflict.
2. **Emphasis:** the notes keep "own licence vs §3.3 carve-out" open. For the Tradovate route that question is moot: Tradovate requires the ILA regardless (TV1, now page-verified). It stays live for other routes.
5. **Tradovate facts now page-verified (10-10):** T1's $25 add-on with no real-time data, the $1,000 key minimum, and the $4/$12 Level 1 rates match the pages. The matrix's TV2 excerpt put "prop and evaluation accounts are not eligible for API access" in the prop-firm article; on the page that line is in **TV1**. TV2 now documents that evaluation accounts are simulation (paper trading) and owned by the provider.
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

Plus Tradovate's $25/month API add-on and, if required for API use (not stated), $12/month Level 1 (TV1, TV3). Feed fees are outside the $700 ceiling (D-Q1, D-Q7). **Monthly range: about $624–$1,827, most likely $1,371 ($1,416 from January 2027).** A wrong A3 reading would be $5,460.

## 9. Verification

- First pass: the session's egress policy blocked every host. After the operator allowed them, `curl` to the Schedule 5 PDF returned CME's HTTP 403 IP block for "suspected web scraping"; not retried or circumvented. Owed: Joshua, in his own browser, quotes §3.3, §8.2, §11.2–§11.3, ILA §2.1(c)/§5.7, Information Policies §7.1/§7.3 and Addendum §4.2 from the page.
- Tradovate pages TV1–TV3 rendered in headless Chromium (`--dump-dom`) on 2026-10-10 and read in full; quotes are copied from the rendered text. `support.tradovate.com` failed TLS verification (incomplete chain); the same articles were read on `vendor-support.ninjatrader.com`. Community thread t/11320 read through its public JSON (lead).
- Leads used (excerpts only): WebSearch for the Schedule 5 Managed User clause, the ILA Subscriber Addendum, and Tradovate sub-vendor threads.
- No login, form, chat, email or contact. No GLM.
