# Tradeify portfolio book protection and capacity contract (TB-S1)

**Status:** ACCEPTED TECHNICAL CONTRACT; policy admission remains gated by TB-P2 ratification and TB-D0.
**Owner:** Astra coordinator. **Implementation owner:** TB-I1.
**Scope:** sizing/protection/capacity behavior only. This document grants no qualification, deployment, arm, emission, or order authority.

## 1. Authority and current implementation debt

The operator-accepted instance is the combined `Tradeify_Select_100K` account's own running settled-close equity peak, a 1% drawdown trigger, and 0.40 protected scale. The session mode is selected once from the prior trading session's settled close and does not change intraday. The lifecycle authorization multiplier and protection multiplier compose before integerization.

`ops/c1_rail/book_policy.py` is an offline candidate implementation, not admission. Its current `leg_quantities` first rounds the normal base and add independently and then scales each result. That differs from the ruled **per executed tier** law below. TB-I1 owns the correction and regression tests; this closeout does not edit production sizing. `core/dd_geometry.py::POLICY_REGISTRY` must remain empty until TB-D0 lands the ratified TB-P2 row.

## 2. Quantity law

For each entry tier, derive the tier from the **executed base** after protection and lifecycle composition, not from the independently rounded normal add:

1. `executed_base = floor(normal_base × policy_multiplier × lifecycle_multiplier × beta_multiplier)`.
2. Aegis has no add. Striker add is `floor(executed_base × 250%)`.
3. Vanguard add is `max(1, pine_round(executed_base × 80%))` only when `executed_base > 0`; each of its two add tiers uses that quantity. Vanguard is disabled at WATCH-1, WATCH-2 and RETIRED, so base and adds are zero there.
4. ORB base remains one micro in PROTECTED mode subject to lifecycle authorization; all resting and future ORB adds are cancelled/refused while protected. At a zero lifecycle quantity, no base or add order exists.
5. A zero base always implies zero adds. Zero-quantity actions are durable refusals/no-ops, never zero-quantity broker requests.

The same function must produce replay, adapter export-menu, sizing-host and rail quantities. Every reachable normal/protected × lifecycle row must have an explicit expected integer fixture, including boundary rows that become zero.

## 3. Settled-close state machine

One durable account state records `last_settled_session`, settled equity, historical EOD peak, `mode_next`, active mode/session and source snapshot seal. A settlement is accepted exactly once in exchange-session order. Duplicate or out-of-order closes halt. Missing, stale, non-finite, or unsealed account evidence leaves the next session blocked.

At the first startup for session D, atomically activate the mode derived from the last settled close before admitting risk. Intraday account observations are evidence only and cannot switch mode. Early-close sessions use their official settlement and the same transition. A position carried across a mode transition is never resized. Transition into PROTECTED first blocks ORB adds, then cancels every working ORB add, and remains blocked until each cancel has terminal broker evidence; existing positions and protective exits remain owned.

Restart loads the durable state and reconciles it with broker positions and working orders before admission. A mismatched or unavailable snapshot produces an account-wide risk-add block, never a default NORMAL mode.

## 4. Capacity and reconciliation

The hard account cap is 80 micro-equivalents: 6J=10; MGC, MYM and MNQ=1. Accounted usage is confirmed open quantity plus every outstanding entry/add reservation, including accepted, partially filled, unknown and recovery-pending requests. Reserve durably **before send** under the operation identity. Partial fills move only the filled quantity from reservation to confirmed exposure; cancellation/rejection releases only broker-confirmed unfilled remainder. A lost response or crash retains the full unresolved reservation until order-level reconciliation proves its disposition.

Requests are admitted whole or refused; never clip. Priority is Aegis 6J, Striker MYM, Vanguard MGC, ORB MNQ. Only Aegis may request a takeover. A takeover atomically blocks admissions, persists its plan, cancel-confirms lower-priority working risk, and close-confirms whole lower-priority legs from lowest priority upward. A partial, rejected, missing, stale, contended, or unknown result refuses Aegis and preserves the block/reservations. No requested capacity is admitted until fresh order-level and position evidence proves every displaced scope flat and free of working risk. Concurrent takeovers serialize through one durable account owner.

## 5. End-to-end evidence trace

The required trace is: adapter paper state and executed-base tier → sealed prior-settled-close account state → per-leg quantity row → durable capacity reservation → broker request/ack/order-level fill or terminal disposition → operation ledger and telemetry → reconciled next-session state. Every link carries `operation_id`, leg/order symbol, policy/fingerprint digest, mode/session, normal and executed quantities, reserved/confirmed micro-equivalents, evidence `as_of`, and reason/status.

HTTP acceptance proves transport only. Completion requires terminal broker evidence. Failed or uncertain operations remain visible after restart and have an attended recovery instruction; no ledger row is deleted merely because the process restarted.

## 6. Acceptance and ownership

TB-I1 owns `book_policy.py`, sizing-host, firm allocation/lifecycle keys and focused tests for §§2–4. TB-I3 owns durable persistence, listener/broker reconciliation, telemetry and the same-shape harness integration. TB-I2 must consume this contract in replay and remains blocked until all seven protected/WATCH/ORB-mode exports pass the TB-R3 intake/parity gate; captured-export parity alone does not discharge them. TB-T1 owns snapshot production and must provide the settled-close fields and seals in §3.

Acceptance cases include zero base/add, each reachable integer tier, partial entry/add fill, reject, cancel, persist-before-send crash at every cut, stale/missing evidence, carried position, protected transition with working ORB adds, ordinary cap refusal, successful takeover, partial/failed/contended takeover, restart, early close and next-session recovery. Synthetic fixtures may establish mechanics; qualification and live capability evidence remain separate gates.
