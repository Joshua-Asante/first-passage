# Packet 1 step 1: producer feasibility

Date: 2026-09-15 UTC (2026-09-14 America/New_York).
Execution base: `821ee9044712a766f03cb798fed32f29153d064c`, branch
`codex/tradeify-packet1-completion`, with the pre-existing Packet 1 working changes.

## Disposition

Subsequent disposition: [Step 1 closure](2026-09-15-calendar-account-contract-resolution.md#step-1-closure--approved-design-and-bounded-calendar-route)
records the operator-approved design and corrects the universal historical-archive
prerequisite to D19's accepted date-membership scope plus a bounded forward route.
The observations and actual producer-qualification limits below remain valid.

Read-only investigation completed; **producer acceptance remains blocked**.
Actual account report access is demonstrated. No complete official historical
schedule source has yet been established for the entire replay window. This note
does not admit a bundle, seal an account, implement authentication, or authorize
activation. No account commands, settings changes, subscriptions or purchases
were made.

## Account source: demonstrated access, bounded capability

Used the already authenticated Tradeify account in Tradovate's DEMO interface,
Reports menu, on 2026-09-14 around 22:24–22:29 ET. Private account identifiers and
financial amounts are excluded from this record.

| Probe | Actual result | Interpretation |
|---|---|---|
| Account Balance History, This year | Downloaded 25 CSV rows; observed trade dates 2026-07-18 through 2026-09-12 | Usable retained balance-history source; observed endpoints do not prove account inception or complete session coverage |
| Cash History, This year | `Too long range` | Annual query cannot be the collection protocol; maximum supported range not established |
| Cash History, This month (09/01–09/14) | Downloaded 18 transactions, dated September 2 and 10 | A bounded cash-ledger query works for this account |
| Client Statements | No such option in the observed report menu | Retail documentation alone does not establish this account's entitlement |

Balance CSV columns: Account ID, Account Name, Trade Date, Total Amount, Total
Realized PNL. Cash CSV columns: Account, Transaction ID, Timestamp, Date, Delta,
Amount, Cash Change Type, Currency, Contract. Cash rows include exchange fee,
clearing fee, NFA fee, commission and trade paired. These identify real fee and
P&L records, not an assurance that all adjustments or revisions were returned.
Neither export contains an explicit completeness watermark, finalized flag or
revision sequence. Timestamp timezone also needs qualification. Balance history
is not a demonstrated one-row-per-venue-session feed: it includes weekend dates
and lacks some weekdays. No missing date may be silently carried forward.

[Tradovate's report instructions](https://tradovate.zendesk.com/hc/en-us/articles/16653178768275-How-Can-I-Run-a-Report-Within-Tradovate-s-Platform)
describe report generation and download. Its
[partner report documentation](https://partner.tradovate.com/resources/admin-dashboards/reports)
describes cash-ledger and account-balance reports; partner capabilities are not
assumed to be this account's entitlements. In particular, its EOD balance guidance
cannot turn this after-hours feasibility capture into a finalized close.

### Private evidence

Retained under the primary checkout's ignored
`lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/inputs/private_overrides/op1/2026-09-14-seven/producer-feasibility/`.
Original downloads remain in Downloads. Raw report captures are private too.

| File | SHA-256 |
|---|---|
| `account-balance-history.csv` | `175fd26f04a6da194b5a9c89b15a5b9d3a9a4a062d5b1f6eaebb9c28cfcafced` |
| `cash-history-september.csv` | `a18cd70b710453d1cd39889602c1a0f080fa81292e9bf11268a6d22f849739b4` |

The AX records retain the balance report, rejected annual cash query, and successful
September cash query. Hashes bind captured bytes; they do not authenticate future
operator submissions or prove report completeness.

### Governing contract and producer boundary

Read `ops/c1_rail/book_sizing_context.py`, the working offline sealer and
`docs/spec/2026-09-12-tradeify-account-snapshot-seal-contract.md` rev4.
Under D23, **initial historical EOD peak comes from the Tradeify dashboard trailing
threshold plus the kernel width, never reconstruction from statements**. E1 is
dashboard evidence; E2 is position/order evidence; E3 is venue history covering
evaluation inception through capture for cash-adjustment checks. These labels
belong to the snapshot contract, not recovery qualification E1–E3.

Concrete candidate for the attended producer: retain account-bound balance and
cash exports, pair them with the required Tradeify dashboard evidence, and submit
them through the separately authenticated operator boundary. Before producing a
`SettledClose`, establish exact prior venue-session identity, account inception
and complete bounded history coverage, fee/adjustment classification, close
finality, timezone, freshness and correction disposition. Retain submission
identity and source digests. Unknown types, gaps, stale or conflicting evidence
must refuse production. This is a proposed implementation boundary, not accepted
settlement evidence from today's samples.

Remaining account blockers: dashboard capture not obtained in this probe;
inception-to-capture cash history not collected; finality/correction semantics
not established; authenticated ongoing settlement contract and consumer binding
not implemented. The offline B7 sealer cannot supply ongoing session authority.
CrossTrade observation snapshots/history remain diagnostic evidence, with their
previously recorded coverage limitations.

## Calendar source: reachable partial archives, full history unproven

| Source | Established capability | Remaining gap |
|---|---|---|
| [CME trading-hours page](https://www.cmegroup.com/trading-hours.html) | Public current/forward schedule interface | Historical URL selection does not establish archived rows; full four-product replay coverage remains unproven |
| [CME reference schedule API](https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/457217339) | Documents one year backward and one year forward, business trade dates and market-state event times | Cannot alone cover 2022–2026; production access not exercised |
| [CME Reference Data Warehouse](https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/457315502/Reference+Data+Warehouse+on+Google+Cloud) | General reference-product history from August 2022, with licensing/onboarding | This is not a guarantee of dated holiday-event history; no account entitlement or actual query established |
| [RDW field catalog](https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/457217280/Comprehensive+RDW+Datasets) | Lists product-specification `trading_hours_json` | Does not establish complete historical holiday exceptions for the four products |
| [Christmas 2023 Globex PDF](https://www.cmegroup.com/trading-hours/files/christmas-day-2023.pdf) | Reachable official group schedule | Described as a general overview; instrument mapping and remaining dates required |
| [Day of Mourning Globex notice](https://www.cmegroup.com/content/dam/cmegroup/trading-hours/files/day-of-mourning-january-9-2024.pdf) | Content concerns January 9, **2025**, despite the filename; equities and FX/metals differ | Product-specific overlay evidence, not a whole-book closure rule |

Do not treat clearing advisories as Globex matching hours, current regular hours
as historical defaults, or generic RDW retention as proof of holiday coverage.
Do not buy/onboard an API on the assumption it closes this gap.

Calendar unblock requirement: an official source set with explicit product and
date coverage for the full frozen historical interval, or a reviewed alternate
evidence contract. The public archives are a concrete collection route, but their
completeness is not yet demonstrated. Forward coverage remains bounded by the
accepted September 30, 2026 end date. Existing D19 and typed overlay rules remain
unchanged.

## Next actions and acceptance boundary

1. Build the calendar source coverage matrix against the exact frozen interval;
   retain official documents and identify remaining product/date holes. Escalate
   the concrete missing coverage before adopting another contract or paid source.
2. Complete bounded account history collection from established inception and
   obtain the required dashboard evidence. Resolve close finality/corrections
   and the authenticated submission contract before settlement implementation.
3. Independent ORB reconciliation work can proceed. Steps 4/5 cannot claim producer
   acceptance on the strength of this feasibility probe.

Verification in this step: successful rendered report results, original CSV
downloads, header/row-count inspection and SHA-256 calculation; official source
and governing local contract review. No runtime code was changed in this step.
