# Packet 1 calendar and account-evidence resolution

2026-09-15 UTC. Base `821ee9044712a766f03cb798fed32f29153d064c` with existing
uncommitted Packet 1 work. This turn changes documentation/evidence only.

## Initial investigation result (superseded scope; retained audit history)

**Current disposition:** Step 1 source feasibility/design is complete under the
bounded route below. The earlier archive investigation and proposed-status account
discussion remain below as history; their universal archive prerequisite and
pending-ratification status are superseded by this closure.

The investigated universal primary historical-calendar archive was **externally blocked, not complete**.
The [account contract proposal](../spec/2026-09-15-tradeify-attended-settlement-contract.md)
now specifies the producer, verifier, durable consumer, correction behavior and
acceptance cases. It still needs review/ratification of the identified contract
clarifications and actual source qualification. It is not a production capability.

## Exact calendar scope and retained evidence

Historical: September 1, 2022 through September 2, 2026. Forward: September 3–30,
2026. Products: 6J, MGC, MYM, MNQ. Immutable D19 remains unchanged.

The [coverage inventory](2026-09-15-calendar-coverage-inventory.json) expands the
secondary calendar's **74 candidate dates into 296 product/date checks**. It is
explicitly incomplete and is not a runtime calendar. The four September 7, 2026
product rows now have actual product-level event observations. The remaining 292
candidate checks lack complete primary product/session proof. The inventory also
keeps regular-session and exception-list completeness open: unlisted dates are
not assumed normal, and these counts are not the complete set of missing facts.

Actual [CME product lookup](https://www.cmegroup.com/trading-hours.html) observations
on the wall-clock date September 7, 2026, all in Central Time:

| Product | PREOPEN / no matching | OPEN | CME business trade date |
|---|---|---|---|
| 6J | 16:00 | 17:00 | September 8 |
| MGC | 13:30 | 17:00 | September 8 |
| MYM | 12:00 | 17:00 | September 8 |
| MNQ | 12:00 | 17:00 | September 8 |

These events establish the halt/reopen distinction for the observed wall date;
they do not alone establish the preceding open or following final close. Do not
label PREOPEN as a final CME close, delete day orders based on that label, or
manufacture a settled September 7 broker record.

Raw rendered table extracts, URLs, symbols and capture instants are retained under
the primary checkout's ignored
`lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/local_artifacts/calendar_producer_2026-09-15/labor-day-products.json`.
SHA-256: `3dafe4b7cb926e60a07575792604a12af5872bedb91dd53394bce5e4c5baeba1`.

## Archive boundary

Search-accessible official group documents provide leads for
[Labor Day 2023](https://www.cmegroup.com/trading-hours/files/labor-day-2023.pdf),
[Christmas 2023](https://www.cmegroup.com/trading-hours/files/christmas-day-2023.pdf),
[New Year's 2024](https://www.cmegroup.com/trading-hours/files/new-years-day-2024.pdf),
and [January 9, 2025](https://www.cmegroup.com/content/dam/cmegroup/trading-hours/files/day-of-mourning-january-9-2024.pdf).
These do not establish all four product mappings and the full historical interval.
No successful raw PDF download/hash is claimed in this turn.

The direct retention attempt failed: CME returned an IP block identifying
automated scraping and directed archive/data inquiries to its Global Command
Center. No alternate IP, cookie, proxy or access-control workaround was attempted.
This was a source-side refusal, not an automatic approval-review rejection.
The [reference schedule API](https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/457217339)
documents only one historical year. Generic RDW product-history retention does
not prove historical holiday-event availability. Paying for either service is
not justified without a positive coverage answer.

### Prepared source request — not sent

Recipient: CME Global Command Center, `gcc@cmegroup.com` (named by the source's
access response). Subject: Historical Globex schedule coverage for four futures
products, September 2022–September 2026.

> Please identify an authorized source or export for historical CME Globex market
> state schedules for Japanese Yen futures (6J), Micro Gold (MGC), Micro E-mini
> Dow (MYM), and Micro E-mini Nasdaq-100 (MNQ), covering September 1, 2022 through
> September 30, 2026. We need regular sessions, holiday halts/closures/reopens,
> business trade dates, event timestamps/timezones, applicable product or group
> codes, and historical schedule revisions. Please distinguish scheduled events
> from actual unscheduled interruptions. Can you confirm the earliest available
> date and complete coverage for these products, the access/export mechanism,
> and any licensing or cost? The documented reference schedule API's one-year
> history does not cover this interval. We are seeking an authorized retrieval
> route, not an exception to website access controls.

No private account information is required for this request. No message was sent,
new access granted, or service purchased. Until an authorized archive/source is
available, the historical primary-calendar gate remains open. Retaining D19's
existing historical evidence class is not itself a replacement for the newly
required product/session matching evidence, and changing that requirement needs
an explicit reviewed decision.

## Account contract decisions made concrete

The proposal resolves initial versus ongoing peak, transaction costs versus
external adjustments, effective close versus report capture, immutable revisions,
and the authenticated submission-to-durable-receipt sequence. It identifies the
required TB-S1 account-session clarification and B7 C8 cost classification instead
of silently changing either owner. Separate activation and resumption remain.

Official [Tradeify session guidance](https://help.tradeify.co/en/articles/10468225-what-is-a-trading-day)
and [permitted-time guidance](https://help.tradeify.co/en/articles/10495876-rules-permitted-times-to-trade)
establish an account-day boundary separate from the observed CME holiday business
date. The [fee schedule](https://help.tradeify.co/en/articles/10468315-trading-commission-fees)
identifies the all-in trading-cost components. The
[dashboard FAQ](https://help.tradeify.co/en/articles/12268494-common-faqs) distinguishes
real-time balance from daily trailing-threshold updates; it does not establish
irreversible broker finality or an account-specific completion timestamp.

Thus an operator signature authenticates review of supplied facts; it cannot
convert an unknown close, missing history or unresolved correction into evidence.
The actual producer qualification must demonstrate those facts on the account.

## Verification

Checked inventory cardinality/unique product-date pairs, exact symbol set,
historical/forward bounds, observed-source digest and explicit incomplete status.
Compared the contract with the actual policy clock, sizing consumer and governing
B7/TB-S1 requirements. Runtime tests from prior work are not represented as new
evidence for this documentation-only change. Independent contract review is
recorded below; no deployment or producer acceptance is implied.

Independent reviewer `packet0_review` found two implementation-blocking gaps:
historical balance was paired only with current flatness, and historical catch-up
could require challenges whose cutoffs had already expired. Both were corrected:
effective-close equity/flatness is now required, and a distinct HALTED record-only
path uses fresh challenges without historical trading permission. The reviewer
re-read the revised contract, including the explicitly proposed 300-second
challenge, 30-minute evidence freshness and full-history re-query requirements,
and accepted it as a coherent reviewable proposal with no remaining blocking
contradictions. Ratification, reconciliation into the governing owners and actual
source qualification remain open. No independent runtime tests were claimed.

## Step 1 closure — approved design and bounded calendar route

Joshua's subsequent instruction: “yes, i approve the design. let's find a simple
solution to the calendar coverage and finish step 1”. The account contract is now
operator-approved design, reconciled into TB-S1's account-session ordering, B7's
C8 trading-cost classification and the Track B umbrella. Its dedicated signing
key, 300-second challenge, 30-minute evidence freshness, full-history re-query,
HALTED record-only catch-up and separate resumption requirements remain intact.

### Simple calendar solution

1. **Keep accepted history.** D19 accepted secondary **date membership**, including
   the explicitly recorded membership residuals; it did not accept product close
   times. See [D19's owning clarification](../adr/2026-09-03-venue-legality-re-expression-lane.md)
   and the umbrella's original TB-C1 forward-calendar scope. The later demand for
   a complete primary archive for every historical product/date overreached these
   authorities. No new acceptance of historical market hours is granted here.
2. **Freeze those bytes.** Private `cme_early_close_calendar.json`, September 1,
   2022–September 2, 2026, contains 40 early-close date rows. SHA-256:
   `6eeb3b9d198eabf0a5a2115c4648f69629720a500616f38e219dff7bc57d0334`.
   Its account-level deadline is not a product exchange close. Preserve D19's
   known residuals, including the unruled-out ad hoc closure interval; do not
   describe all residuals as conservative.
3. **Use a small, separately pinned forward calendar.** September 3–30, 2026,
   for 6J/MGC/MYM/MNQ. Source: public CME product schedules plus Tradeify account-day
   and permitted-time guidance linked above. The four retained September 7
   product observations prove the source route is reachable. No new paid service
   or four-year archive is a prerequisite to establishing that route.
4. **Keep restrictions typed.** Book no-trade overlays on 2023-04-07, 2025-01-09
   and 2026-04-03 remain separate digest-pinned policy restrictions. They do not
   assert that every product's exchange was closed. D19 never explains missing
   bars, provides matching intervals or licenses invented/forward-filled bars.

The 296-check archival inventory remains **INCOMPLETE_NOT_RUNTIME_INPUT**. Its
292 gaps are real gaps in that broader inquiry, not 292 silently accepted product
schedules. A specific historical matching/coverage claim still needs its own
evidence before replay acceptance. If that evidence is unavailable, the affected
acceptance remains blocked. The prepared archive request is optional unless such
a claim actually requires it; no request has been sent.

### What completion means and what remains

**Step 1 is complete for source feasibility and approved contract design.**
Actual balance/cash reports demonstrate account-source access; their limits are
retained in the producer probe. Approval cannot create inception, effective-close
equity/flatness, query completeness or broker finality facts.

- **Step 2 next:** reconcile the O-N/O-P summary panels and inactive O-P add inputs.
- **Steps 3/4:** prove startup and actual panel coverage; implement the calendar
  through `BookSession`, retaining official regular-session rules, exception
  coverage, adjacent holiday matching boundaries, account/CME date mappings,
  deadline semantics and DST. Test missing/expired coverage refusals. The four
  observed event rows alone do not satisfy this exit; no weekday fallback.
- **Step 5:** implement authenticated evidence ingestion and durable consumption,
  then qualify actual inception/full-history, timezone, effective-close equity
  or boundary flatness, revisions and freshness. No inferred balances or finality.
- **Step 6:** independent combined acceptance and seven admitted parity bundles.

This closes neither Packet 1 nor any live activation, deployment or resumption
gate. No runtime behavior, calendar bytes, strategy or sizing constant changed
in this closure.

### Closure verification

At base/head `821ee9044712a766f03cb798fed32f29153d064c` plus the existing
uncommitted Packet 1 work, `git diff --check` passed and local Markdown file
targets in all eight affected documents resolved. Rechecked D19's 40 rows,
coverage bounds and unchanged digest, and the unchanged retained forward-probe
digest. No runtime suite was rerun for this documentation-only closure.

Independent reviewer `packet0_review` accepted Step 1 closure with no blocking
contradictions: owner reconciliation is consistent, D19 remains date-membership
only, and original TB-C1 scope supports removing the universal archive prerequisite
from feasibility. Historical matching/coverage evidence and actual calendar/account
producer qualification remain downstream gates. The inventory is not runtime input.
