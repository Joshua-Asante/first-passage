# M1 Stage 1 test infrastructure - source unavailable

**Offline M1 Stage 1 test infrastructure only - no deployment, no signal emission, no arm.**

## Current disposition (operator report 2026-09-10)

The operator retired Databento as an information source for First Passage and
reported unsubscribing. No replacement source is approved. This supersedes this
PR's earlier Databento-specific implementation and attended ceremony instructions.
The Databento adapter, its SDK dependencies, Docker entries and mapping tests have
been removed. No source connection, account access, deployment or signal occurred.

The daemon entrypoint always constructs `NullStrategy` with an unavailable,
disconnected bar source and emission disabled. Previously enabled configuration
cannot restore a source or install the test strategy. Existing journal tombstones
are preserved. The prepare/enable CLI refuses before writing state; close and
status remain available. Status reports effective emission false and source
unavailable. A replacement is not a config-only change: it requires an explicit
source decision, implementation, review and separate operational authorization.

## What M1 does and does not require

The accepted M1 item-5 addendum licenses a test strategy through
`Strategy.on_bar` -> ordinary daemon B1 client -> listener -> expected nonzero
structured dry-run decision. It does not intrinsically require Databento.
The current S2b build ADR separately specifies a live CME feed. Retirement removes
that provider selection; it does not silently approve fixtures or replay as
qualifying acceptance evidence. An explicit amendment could define a controlled
replay wiring test while keeping live-feed readiness separate. None is approved
in this change. Item 5 and operator signoff remain owed; M1 stays `CODE_LANDED`.

## Frozen identity and sizing

| Input | Value |
|---|---|
| Identity / lifecycle key | `m1_stage1_test` / `M1 Stage1 Test` |
| Instrument / listener route | MYM / `MYM1!` |
| Tier / starting-balance sizing basis | `Tradeify_Select_100K` / 100000 |
| Base risk fraction | `0.0000125` (0.00125%) |
| Stop | 1.0 point, one MYM tick |
| Dollars per point / pyramid | 0.5 / 0.0 |
| Dedicated cap | At most one micro; generated default zero |
| Lifecycle default / test harness | `RETIRED` / `AUTHORIZED` |

Source owners: `core/firm_rules.py`, `core/dd_protection.py`, `core/lifecycle.py`,
`ops/c1_rail/c1_sizing_host_reference.py`, and MYM tick handling in
`ops/c1_rail/c1_rail_slippage.py`. These production controls are unchanged.
Normal arithmetic floors 1.25/0.5 to two contracts, capped to one. At the 40% DD
multiplier it floors 0.5/0.5 to one. Current equity determines the DD regime;
the risk basis remains starting balance. Smaller DD multipliers are not covered
by the one-micro promise. The immediately preceding binary64 risk produces
0.49999999999999994 dollars under 40% DD and floors to zero. One point is the
smallest native stop; sub-tick stops are rejected.

The listener samples mode once and requires explicit Boolean `dry_run=true` for
this identity before sizing or payload construction. Non-entry requests halt.
Malformed/drifting test constants, lifecycle, DD or allocation inputs fail closed.
The one-micro cap never borrows withdrawn reservations. These protections remain
even though source retirement prevents attended emission.

## Retained offline components

The strategy, coordinator and journal are exercised only by injected synthetic
fixtures in tests. The source marker is explicitly
`{kind: offline_fixture, schema: ohlcv-1m, symbol: MYM1!}`. It is not a provider
selection or live-data claim and is not connected to the runtime entrypoint.
The ordinary B1 serializer, client and actual HTTP handler/response writer remain
in the integration test; no socket or external service is used.

The journal reserves durably before the single HTTP attempt, rejects redirects,
disables the ceremony after reservation, and retains receipts through concurrent
close. Restarts, duplicate bars and spent IDs cannot renew it. Unresolved
EVALUATED/SEND_RESERVED/EMITTED/TRANSPORT_UNKNOWN checkpoints anywhere in history,
including CLOSED.previous_state, block a fresh ceremony ID. No reconciliation or
reset bypass is supplied: preserve state and stop pending a separately reviewed
operator reconciliation procedure.

The evidence helper accepts only a closed RESPONSE_RECORDED attempt with a valid
200 dry-run receipt and original body fingerprint, then joins its request to a
unique authenticated listener ledger triad. A closed unresolved send cannot
produce a positive projection. Output is explicitly `offline_test_only=true`,
`qualifying_live_source=false`, and uses `listener_event_id`; it never provides
`dry_run_strategy_signal_event_id`. It does not write acceptance, fabricate broker
CHAIN_OK, or provide operator signoff. Raw bar/account/response values stay private.

The listener migration/preflight helpers remain available for offline review.
Migration defaults to plan-only; apply requires disarm, reviewed preimage hashes
and flat verification. It backs up state and writes cap zero before lifecycle
and any requested cap one. Releasing old 69/11 reservations requires the explicit
accepted-release flag; no silent reallocation. Preflight uses the same sizing host
and does not POST, append ledger events or ratchet DD. None of these commands is
an instruction to operate on a live volume under this PR.

## Readiness and review

All deployment/ceremony work remains blocked pending an approved source or an
explicit acceptance amendment, plus authenticated private crash-loop recovery
and the canonical deployment preconditions. Do not reconstruct or waive that
recovery procedure. Future deployments require reviewed integrated source,
import/COPY checks, actual in-container fixture hashes and boot/disarm/health
verification. Existing deployed M1 pins, evidence IDs, status and signoff remain
unchanged; local tree bytes never refresh deployed pins.

The separate retirement documentation PR records the wider source decision.
This PR changes no accepted-book, production-protection, allocation, venue-edition
or unrelated strategy file. No core or lab implementation is changed. The MYM
instrument appendix describes this test identity only. No subscription renewal,
replacement source, arming, order, deployment or merge is authorized.

## Verification history

The earlier source-bearing implementation passed 387 focused tests after its
review corrections. Those results are historical and do not certify the revised
source-free runtime. The retirement/evidence regressions failed before their fixes.
The revised suite passes **374 tests** on Python 3.12: rail, daemon, M1, sizing,
acceptance validation and CrossTrade regression selections. Removed provider tests
are replaced by unavailable-source/runtime activation tests; fixture integration
still verifies normal and 40% DD sizing and the permanent live-send prohibition.
Docker builds/native live-feed behavior are not claimed as tested. Both images
now contain only the stdlib runtime subset; no Databento package is installed.
