# Tradeify portfolio book protection and capacity contract (TB-S1)

**Status:** ACCEPTED TECHNICAL CONTRACT; policy admission remains gated by TB-P2 ratification and TB-D0.
**Owner:** Astra coordinator. **Implementation owner:** TB-I1.
**Scope:** sizing/protection/capacity behavior only. This document grants no qualification, deployment, arm, emission, or order authority.

## 1. Authority and current implementation debt

The operator-accepted instance is the combined `Tradeify_Select_100K` account's own running settled-close equity peak, a 1% drawdown trigger, and 0.40 protected scale. The session mode is selected once from the prior trading session's settled close and does not change intraday. The lifecycle authorization multiplier and protection multiplier compose before integerization.

`ops/c1_rail/book_policy.py` is an offline candidate implementation, not admission. Its current `leg_quantities` first rounds the normal base and add independently and then scales each result. That differs from the ruled **per executed tier** law below. TB-I1 owns the correction and regression tests; this closeout does not edit production sizing. `core/dd_geometry.py::POLICY_REGISTRY` must remain empty until TB-D0 lands the ratified TB-P2 row.

## 2. Quantity law

**Correction 2026-09-13:** the former generic quantity-floor equation incorrectly applied law A to Striker and included an on-rail beta multiplier. The [recorded O-1/O-5/O-6 rulings](../notes/2026-09-12-track-b-scaling-faithfulness-read.md#3--the-single-finite-export-menu-frozen-2026-09-12-under-the-ruled-defaults) already resolve both: Striker uses risk-scaled law B; Call-4 is an off-rail operator kill-switch / GO-NO-GO trigger, never an additional rail sizing multiplier. This correction implements those decisions in the technical contract and records no new ratification.

Let `p` be 1 in NORMAL and 0.40 in PROTECTED; `l` is the per-leg lifecycle multiplier (AUTHORIZED=1, WATCH-1=0.50, WATCH-2=0.25, RETIRED=0). Use exact rational arithmetic before flooring. Compute a **requested base** first; only confirmed fills establish the **executed base** used by an add. An emitted or accepted request is not an executed base.

1. **Aegis, fixed scaled:** requested base `floor(8 × p × l)`; no adds.
2. **Striker, risk ladder (law B):** requested base `min(floor(R × p × l / D), floor(C / 3.5))`, where `R` is the unscaled risk budget from the explicit account basis and accepted leg risk expression, `D = stop_dist_pts × dollars_per_pt` is positive per-contract risk, and `C` is the explicit leg allocation ceiling. For the ruled 80-micro candidate ceiling, base caps at 22. Add `floor(confirmed_executed_base × 2.5)`. Do not scale an already-rounded `qty_normal` or a normal add. Production `cap_alloc=0` remains inert until TB-V1; offline candidate fixtures explicitly supply the ruled ceiling. Account-wide capacity admission still applies after this per-leg computation.
3. **Vanguard, adapter quantity (law A):** requested base `floor(normal_base × p)` only at AUTHORIZED, with `normal_base` 1 or 2; WATCH-1, WATCH-2 and RETIRED always yield zero. Each of two add tiers is `max(1, pine_round(confirmed_executed_base × 0.8))` only for a positive confirmed base and currently authorized/unprotected add admission. Protected mode refuses new adds; carried positions are not resized. Preserve half-away-from-zero Pine rounding; do not apply Striker's floor globally.
4. **ORB, fixed base / gated adds:** requested base `floor(1 × l)`, unscaled by protection; each of two add tiers is one micro only with a confirmed positive base, AUTHORIZED lifecycle and NORMAL mode. Protected transition cancels resting ORB adds and refuses future ones. At zero lifecycle quantity, no new base or add order exists.
5. A zero requested base implies no prospective adds for that new entry. A carried confirmed position remains owned under §3; it is never erased by today's zero requested quantity. Zero-quantity actions are durable refusals/no-ops, never zero-quantity broker requests.

The same function must produce replay, adapter export-menu, sizing-host and rail quantities. `OrderIntent.qty` / `qty_normal` remain adapter-normal diagnostics on entry/add, not the broker-size authority. Striker additionally requires `R`, `D`, `C`, mode and lifecycle: the rounded normal integer loses information, particularly at the cap. The adapter supplies `stop_dist_pts`; the validated sizing configuration supplies account basis, leg risk expression, dollars-per-point and allocation; the durable account owner supplies active session/mode; lifecycle state supplies authorization. Missing or invalid required inputs halt, with no inverse reconstruction from `qty_normal` and no default authorization.

### 2.1 Literal mode/lifecycle acceptance rows

Each cell is `(requested base, prospective per-tier add)` after a full base fill. These are synthetic arithmetic vectors, not export parity. Vanguard columns cover both normal ladder inputs. Partial fills use their confirmed base instead and are tested separately. The Striker example uses `R=700`, `D=10`, `C=80` (unscaled ratio 70).

| Mode | Lifecycle | Aegis | Vanguard normal 1 | Vanguard normal 2 | ORB | Striker example |
|---|---|---|---|---|---|---|
| NORMAL | AUTHORIZED | 8/0 | 1/1 | 2/2 | 1/1 | 22/55 |
| PROTECTED | AUTHORIZED | 3/0 | 0/0 | 0/0 | 1/0 | 22/55 |
| NORMAL | WATCH-1 | 4/0 | 0/0 | 0/0 | 0/0 | 22/55 |
| PROTECTED | WATCH-1 | 1/0 | 0/0 | 0/0 | 0/0 | 14/35 |
| NORMAL | WATCH-2 | 2/0 | 0/0 | 0/0 | 0/0 | 17/42 |
| PROTECTED | WATCH-2 | 0/0 | 0/0 | 0/0 | 0/0 | 7/17 |
| NORMAL | RETIRED | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| PROTECTED | RETIRED | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |

Striker's reachable positive multiplier set is exactly `{1, 0.50, 0.25, 0.40, 0.20, 0.10}`. For any such multiplier `m=p×l` and unscaled ratio `x=R/D`, base `q<22` is selected by `q/m <= x < (q+1)/m`; base 22 is selected by `x >= 22/m` at `C=80`. RETIRED always selects zero. This interval partition covers every integer row under each mode/tier; the single example above is not a claim that every row is cap-bound.

| Striker confirmed base | Per-tier add |
|---|---|
| 0 | 0 |
| 1 | 2 |
| 2 | 5 |
| 3 | 7 |
| 4 | 10 |
| 5 | 12 |
| 6 | 15 |
| 7 | 17 |
| 8 | 20 |
| 9 | 22 |
| 10 | 25 |
| 11 | 27 |
| 12 | 30 |
| 13 | 32 |
| 14 | 35 |
| 15 | 37 |
| 16 | 40 |
| 17 | 42 |
| 18 | 45 |
| 19 | 47 |
| 20 | 50 |
| 21 | 52 |
| 22 | 55 |

TB-I1 must test each interval's lower boundary and a rational value immediately below it, plus cap saturation, every literal row above, and partial confirmed-base cases. A discriminating non-cap case is `R/D=5/2` in PROTECTED/AUTHORIZED: Striker law B yields base 1/add 2, while flooring normal base 2 and then multiplying by 0.40 incorrectly yields zero. Unknown policy, mode/tier, nonfinite values, invalid risk denominator and absent allocation must halt.

## 3. Settled-close state machine

One durable account state records `last_settled_session`, settled equity, historical EOD peak, `mode_next`, active mode/session and source snapshot seal. A settlement is accepted exactly once in exchange-session order. Duplicate or out-of-order closes halt. Missing, stale, non-finite, or unsealed account evidence leaves the next session blocked.

At the first startup for session D, atomically activate the mode derived from the last settled close before admitting risk. Intraday account observations are evidence only and cannot switch mode. Early-close sessions use their official settlement and the same transition. A position carried across a mode transition is never resized. Transition into PROTECTED first blocks ORB adds, then cancels every working ORB add, and remains blocked until each cancel has terminal broker evidence; existing positions and protective exits remain owned.

Restart loads the durable state and reconciles it with broker positions and working orders before admission. A mismatched or unavailable snapshot produces an account-wide risk-add block, never a default NORMAL mode.

## 4. Capacity and reconciliation

The hard account cap is 80 micro-equivalents: 6J=10; MGC, MYM and MNQ=1. Accounted usage is confirmed open quantity plus every outstanding entry/add reservation, including accepted, partially filled, unknown and recovery-pending requests. Reserve durably **before send** under the operation identity. Partial fills move only the filled quantity from reservation to confirmed exposure; cancellation/rejection releases only broker-confirmed unfilled remainder. A lost response or crash retains the full unresolved reservation until order-level reconciliation proves its disposition.

Requests are admitted whole or refused; never clip. Priority is Aegis 6J, Striker MYM, Vanguard MGC, ORB MNQ. Only Aegis may request a takeover. A takeover atomically blocks admissions, persists its plan, cancel-confirms lower-priority working risk, and close-confirms whole lower-priority legs from lowest priority upward. A partial, rejected, missing, stale, contended, or unknown result refuses Aegis and preserves the block/reservations. No requested capacity is admitted until fresh order-level and position evidence proves every displaced scope flat and free of working risk. Concurrent takeovers serialize through one durable account owner.

**Ruled protected-capacity consequences (O-6):** Aegis 3 full 6J contracts consume 30 micro-equivalents; Striker at its protected ceiling consumes 22+55=77. Their combined 107 exceeds 80. With Aegis already holding 30, Striker base 22 can fit at 52 used, but its full 55 add must be refused; it cannot displace Aegis or clip the add to 28. With Striker at 77 and Aegis requesting 30, Aegis may complete the specified whole-leg takeover; closing only 27 is not whole-leg displacement. With authorized ORB base plus two carried adds consuming 3, Striker 77 consumes the full cap; Aegis's takeover closes ORB first, then Striker, before admitting 30. A mode change never creates headroom by resizing a carried position, and an unresolved reservation consumes capacity in all these cases.

## 5. End-to-end evidence trace

The required trace is: adapter paper state and executed-base tier → sealed prior-settled-close account state → per-leg quantity row → durable capacity reservation → broker request/ack/order-level fill or terminal disposition → operation ledger and telemetry → reconciled next-session state. Every link carries `operation_id`, leg/order symbol, policy/fingerprint digest, mode/session, normal and executed quantities, reserved/confirmed micro-equivalents, evidence `as_of`, and reason/status.

HTTP acceptance proves transport only. Completion requires terminal broker evidence. Failed or uncertain operations remain visible after restart and have an attended recovery instruction; no ledger row is deleted merely because the process restarted.

## 6. Acceptance and ownership

### TB-I1 typed sizing boundary (Task 3b)

`C1SizingHostReference.process_book_signal(request, *, policy, context, binding, now)`
calls the pure boundary in `ops/c1_rail/book_sizing_context.py`, then the shared
`entry_quantities` or `add_quantity` implementation. All arguments are explicit.
The legacy `process_signal(payload, current_equity)` remains blocked for book IDs.

| Input | Required producer and contents |
|---|---|
| `BookSizingRequest` | Adapter-to-host integration: operation ID, fixed leg ID, order symbol, entry/add kind, adapter-normal base and explicit per-contract risk. Striker risk is not reconstructed from the integer base. |
| `BookSizingBinding` | Trusted integration owner: account identity, current owner/boot epoch, policy and snapshot digests, the complete verified `SettledClose`, calendar `BookSession`, explicit evidence-age limit, leg/order-symbol binding, micro-equivalent allocation ceiling and unscaled risk dollars from the accepted account basis/configuration. This is not adapter-supplied authority. |
| `BookAccountContext` | TB-I3 account owner: matching operation/account/session/leg/symbol/digests, active mode, settled record, lifecycle key/tier, observation and expiry times, intended/confirmed base and base-operation identity, gross confirmed/reserved contracts for exactly all four legs, pending operation IDs and active block reasons. Unknown exposure or unresolved protection-transition evidence must produce a block, not a zero row. |
| `BookSession` / `SettledClose` | TB-C1 supplies exact current/prior session identities and open/risk-add-cutoff/close times; no weekday arithmetic or hard-coded schedule. TB-T1 verifies the settlement seal, full contents and snapshot provenance. The host compares those verified contents with context, including the seal; it does not implement the verifier. |

The boundary checks identity and digest agreement, full settled-record agreement,
timezone-aware chronology, freshness, allocation/count types, lifecycle identity,
complete exposure accounting and the mode derived from the prior settled close.
It rejects pending reuse of the same operation and every supplied owner block.
Adds use confirmed base only; entry requires an empty leg. It never writes the
historical host's in-memory base map or resizes a carried position. Capacity is
checked using confirmed plus reserved gross contracts, with whole-request refusal.

`BookSizingDecision.submit` is always false. A positive demand and apparent
headroom do not reserve capacity, authenticate evidence, admit a policy or prove
execution readiness. Task 4 supplies canonical fingerprints; TB-I3 must persist
and serialize admission, recheck evidence, deduplicate completed operations,
reserve before send, handle takeover and release only on terminal evidence.
Repeated identical pure calls are deliberately identical; they are not durable
dedupe. Duplicate/out-of-order settlement persistence and transition cancellation
remain account-owner obligations. The method remains non-emitting. The Docker
recipe and build-context allowlist include its pure dependency closure, including
shared policy/geometry and protocol/feed types; packaging enables imports, not a
listener route or deployment. An isolated-process test loads the host using only
the recipe's copied Python files.

### Combined packet acceptance

TB-I1 owns `book_policy.py`, sizing-host, firm allocation/lifecycle keys and focused tests for §§2–4. TB-I3 owns durable persistence, listener/broker reconciliation, telemetry and the same-shape harness integration. TB-I2 must consume this contract in replay and remains blocked until all seven protected/WATCH/ORB-mode exports pass the TB-R3 intake/parity gate; captured-export parity alone does not discharge them. TB-T1 owns snapshot production and must provide the settled-close fields and seals in §3.

Acceptance cases include zero base/add, each reachable integer tier, partial entry/add fill, reject, cancel, persist-before-send crash at every cut, stale/missing evidence, carried position, protected transition with working ORB adds, ordinary cap refusal, successful takeover, partial/failed/contended takeover, restart, early close and next-session recovery. Synthetic fixtures may establish mechanics; qualification and live capability evidence remain separate gates.
