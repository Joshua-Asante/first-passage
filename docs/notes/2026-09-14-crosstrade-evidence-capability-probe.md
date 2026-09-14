# CrossTrade E1–E3 read capability probe — 2026-09-14

Verdict: authenticated read access and durable fill pagination demonstrated;
E1–E3 production qualification remains NOT ESTABLISHED.

## Scope and method

Joshua requested testing CrossTrade capability. On 2026-09-14 at approximately
22:03–22:08 UTC, five bounded Python invocations used the existing credential
inside the running `c1-rail` Fly machine. Credentials and account identifiers
were not printed or copied locally. Each invocation asserted disarmed configuration;
the route was `tradovate`. Only documented HTTPS GET endpoints were called, with
redirects refused, response-size limits and request timeouts. No host files were
written, orders sent, configurations changed, links refreshed, or WebSockets opened.

Observed host image digest:
`sha256:07e3009264c5d4bf65da1ea2ebf07d9b8def32ad6018c541ff0b7d705e53ded0`.
The checked configuration had `dry_run=true`, no `armed_until`, and a configured
account and credential. This is configuration evidence, not a new host attestation.

There were 18 CrossTrade GET requests: 14 HTTP 200 responses and four HTTP 400
responses (two historical lifecycle samples plus two diagnostic repeats).
Fly printed `Error: The handle is invalid.` and exited 1 after each invocation's
output. Remote results and final completion markers were received; do not label
the SSH wrapper successful. The first invocation emitted its completed status
result; the following four emitted explicit completion markers.

## Observed results

| Read/check | Actual result | Limit |
|---|---|---|
| `/v1/api/tv/status` | HTTP 200, `success=true`; one identity in returned schema | Access demonstrated; no token renewal or relinking tested |
| `/v1/api/tv/accounts/snapshot` | HTTP 200; exactly one account matched configured name, no account error, zero positions and working orders | `asOf`/`asOfEpoch` are present; atomicity, completeness and broker causal ordering not established |
| Scoped `/positions` and `/orders` | HTTP 200, empty arrays | No nonempty gross-lot/protection shape exercised |
| `/v1/api/tv/orders` | HTTP 200, one identity envelope with empty order data | Current-session response, not complete request history |
| Scoped `/fills` | HTTP 200, empty array | No current-session execution sample |
| `/v1/api/tv/fills/history?account=…` | Four stored rows; all matched configured account; unique execution IDs; timestamps nondecreasing | Only stored rows, not proven complete account history |
| History repeat | Same economic identity/quantity/price/time fields on immediate repeat | Does not prove immutability across corrections or restarts |
| History cursor | Two pages of two rows, disjoint IDs, second page ended; replaying its cursor returned identical response | Pagination cursor is not a coverage watermark |
| Historical `/orders/{id}/lifecycle` | Both earliest/latest sampled history order IDs returned HTTP 400 | Cannot establish historical order/protection/request reconstruction from these samples |

Stored history timestamps span `2026-08-26T15:52:48.943000Z` through
`2026-09-10T16:28:12.070000Z`. These are observed extrema, not coverage bounds.
History exposed execution/fill/order/account IDs, environment, instrument/root,
action, quantity, price, commission, fees, timestamp and trade date. It exposed
no coverage watermark in the observed envelope.

The repeated lifecycle error had top-level fields `detail`, `error`, `success`.
A subsequent redacted diagnostic identified `error=tradovate_rejected`, with
generic detail saying Tradovate rejected the order and to check and try again.
This was a GET read failure; it is not evidence that any historical trade was
rejected. Cause remains unresolved: the response does not establish expiry,
permission failure, or absence of the order. No fabricated order IDs were queried.

## Digest anchors

Digests identify observed bytes, not independently reproducible acceptance evidence.
Raw private responses were not retained; output retained only summaries/schemas.

- Initial status response SHA-256:
  `b9c651373a663a56ee2e804968e65d7016a121ed1b83e1fab262e9ca84c4a836`.
- Initial snapshot response SHA-256:
  `23d9587b1796e4ed47bfb2e956075a6dbf5705bd5ce26bce482879cc18d7b14d`.
- Four history rows, Python `json.dumps(rows, sort_keys=True)` SHA-256:
  `d52983404afefcb3228d135fdd86006ce30bfc6f9bf826389f872265e39a9f98`.
- Diagnostic lifecycle error, sorted JSON SHA-256:
  `1ef6ee58ba7290cef56a375e14c5bf4c1ae395d5c25cece2d6d0bea5d5f7c9dd`.

## Qualification implications and next test

E1 is partially observable: account binding and reads work, but no coherent
broker boundary or gross accounting proof was demonstrated. E2 has a real durable
fill input, but complete capture, historical protection ownership and immutable
reduction accounting remain unproven. E3 was not demonstrated: the documented
read surface inspected provides no accepted account-wide unresolved-request fence.
Empty reads cannot prove that no request remains in flight.

This refines the prior continuation audit: durable fill storage exists and was
queried successfully. It does not close the audit's complete-history requirement.
[Fill-history documentation](https://crosstrade.io/docs/api/tradovate/get-fill-history)
explicitly describes periodic capture without guaranteed deadlines, no coverage
watermark or revision cursor, and no prior-session backfill. End-of-pagination
means the end of stored matching rows. Fee fields can change. The
[API overview](https://crosstrade.io/docs/api/tradovate/overview) distinguishes
current-session reads from durable history. These limitations are documented
provider semantics, separate from this probe's observations.

Next resolve the generic lifecycle 400 with the provider and obtain a supported
contract for coherent acquisition, complete-history coverage and the global
request fence. No provider message was sent. Only after those capabilities are
identified can controlled nonempty order/fill, external-request, reconnect and
session-rollover tests qualify them. Such tests are not satisfied by this flat
account probe. Production RecoveryOwner dispatch remains unavailable.

## Support-free continuation — 2026-09-14

Joshua subsequently directed continuation without contacting support, using the
documented limits. This supersedes the support inquiry as the immediate next step;
it does not supply E1–E3 qualification or authorize changing recovery guarantees.

Five additional HTTPS GET requests ran at 23:09:07–23:09:13 UTC using the same
in-place credential and disarmed-configuration assertions. Three returned HTTP
200 and two returned HTTP 400. No host files, configuration, orders or streams
were changed. A completion marker was received before the same Fly client
`The handle is invalid` exit-1 error.

- Retrieved one actual historical fill and verified its account against the
  configured account before using its order ID.
- Both the basic order-item GET and lifecycle GET returned
  `400 tradovate_rejected`. The failure therefore also affects the basic lookup;
  it is not isolated to lifecycle's optional command/report enrichment. The
  upstream cause remains unknown; expiry is not established by this comparison.
- Two account snapshots separated by five seconds both succeeded, each matched
  exactly one configured account without account errors, and their `asOf` values
  differed. This demonstrates timestamp refresh in this sample, not an atomic
  account boundary or complete request accounting.

### Documented limits carried forward

The [snapshot reference](https://crosstrade.io/docs/api/accounts/get-accounts-summary)
documents a three-second cache and recommends polling at five seconds or slower.
Order-version enrichment is limited to 20 lookups across a snapshot; missing
fields remain null. Version-derived fields can reflect rejected modifications.
Neither a fresh timestamp nor a populated snapshot establishes the required E1
broker causal boundary.

The [lifecycle reference](https://crosstrade.io/docs/api/orders/get-order-lifecycle)
documents concurrent order/version/command reads, followed by report reads for
IDs in the last ten returned commands. HTTP 200 can carry `partial` and
`unavailable` markers for failed optional reads. The mandatory order read fails
the request when unavailable. A successful lifecycle response is therefore not
automatically a complete command history, and its latest version is not proof of
an accepted modification.

The documented fill-history cursor enumerates stored rows without certifying
capture coverage. Observed execution identities can support deduplication;
overlapping rereads must preserve revisions rather than silently overwriting
earlier economic facts or mistaking fee updates for new executions.

Support-free disposition: use these endpoints for observations and diagnostics.
E1 coherence, E2 complete history and E3 global unresolved-request accounting
remain unestablished. API errors and absent data must remain visible limitations.
Do not convert local collection sequence numbers, stable repeated reads, empty
positions/orders or exhausted pagination into those missing guarantees. No
automatic recovery-complete or resume decision is justified by this packet.
