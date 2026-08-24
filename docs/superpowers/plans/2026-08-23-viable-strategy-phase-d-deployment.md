# Phase D — Deployment (survivor → S2b signal → M1 RESOLVED → B7-REFIRE → armed sessions)

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:executing-plans. Checkbox (`- [ ]`)
> syntax. ⚠ This phase touches the live rail's governance chain — every arming-adjacent step is
> operator-only by standing ADR; no task below may be reinterpreted as agent-executable if its
> owner says operator.

**AUTHORIZATION:** starts automatically in its non-arming tasks the moment a Phase-C survivor
enters TNEC-1 intake; every arming step keeps its own operator GO. Safety invariants
(CLAUDE.md §Live-execution posture) bind throughout: `dry_run=false` never while M1 is not
`RESOLVED` (trigger = ARM); disarm before `armed_until` expiry; live spend = M1 `RESOLVED` +
separate operator GO per session; **no agent places any trade**.
**Parent:** [`sequence overview`](2026-08-23-viable-strategy-sequence-overview.md) ·
**Input:** a Phase-C survivor through TNEC-1 intake.

**The chain, stated once:** the whole reason the rail exists has been blocked on "an acceptable
strategy on the ruled host" (STATE queue row 1). A survivor un-blocks it in order: S2b emits its
signal → M1 item 5 discharges → operator signoff → M1 `RESOLVED` → B7-REFIRE Stage 1 → armed
sessions under per-session GO. Five fill-gated threads (lifecycle Call-1 σ-source, per-fill
add-slippage capture, forward regime-monitor successor, ECR discharge, ORB decay re-scope)
unblock downstream of the first strategy-signal fill.

---

## Task D1 — Venue-edition registration (doc + config, no arming)

- [ ] Register the survivor as a venue edition in
  [`ops/venue_editions/Tradeify_Select_100K.md`](../../../ops/venue_editions/Tradeify_Select_100K.md)
  (live set currently empty) — book → venue-edition → deployment axes per the venue-binding ADR.
- [ ] Lifecycle/authorization state named explicitly (CANDIDATE-track lead per
  `strategy_lifecycle.md`; the sizing rung it deploys at is its own decision artifact — the
  historical WATCH-1 0.50× figure is the *withdrawn Striker book's* record, never inherited).
- [ ] `LEG_MAP`/sizing-host wiring for the new leg is a **code change on the live rail** —
  CC-solo surface, its own PR, reviewed against `c1-rail` skill invariants; the deliberately
  untouched Striker code path stays untouched.

## Task D2 — S2b daemon signal (discharges M1 item 5)

- [ ] Survivor's signal implemented on the ruled Python-native host (`ops/c1_signal_daemon/`,
  S2b) — TV login automation stays prohibited (S2); TV remains research/export only.
- [ ] `emit_enabled` flip is an operator action. Daemon emits the real strategy signal as B1 JSON
  → listener, `dry_run=true`, **expected non-zero sizing** (the floored-to-zero 2026-07-28
  precedent is pre-judged inadmissible for item 5 — a qty-0 decision never exercises the payload
  builder).
- [ ] Record `dry_run_strategy_signal_event_id` in
  `docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json` only from this real event — the
  validator checks presence, but the arming gate's spirit requires provenance; no canned payload.

## Task D3 — M1 `RESOLVED` (operator)

- [ ] `operator_signoff` — the last open field. Pre-signoff sanity: fixture-hash tree-skew note
  re-read (the 2026-08-21 skew entry says pins refresh only from in-container hashes at a real
  redeploy — if a redeploy is needed to land D1's wiring, refresh the pin in the same motion).
- [ ] `python scripts/validate_c1_monitoring_acceptance.py --require-resolved` green — the arming
  interlock validates this artifact fail-closed; a status-only flip fails ~19 checks by design.

## Task D4 — Pre-arming hygiene (parallel, cheap, before first armed session)

- [x] **Per-trade loss-bound election** — [`elect-2`](../../adr/2026-08-24-q-tradecap-2-elect-alert-tripwire.md)
  `Accepted` 2026-08-24 (ID **2**, observe-only). Threshold later. Do not treat as a wire.
  Do not elect from the CFD-era fork in `1r_estimation.md`.
- [ ] **Disaster-stop Phase 0a** — attended real-account SIM observation (operator-committed
  2026-08-24 forward trigger). Only a recorded PASS unlocks Phase 1 (`sl=` wiring into the
  listener). If it lands, the survivor's first armed sessions carry a broker-side stop; if not,
  the gap is a named risk on the arming card, not a silent one.
- [ ] **Weekly idle-clock continuity:** the operator token-trade discipline continues unchanged
  (rolling STATE row; deletion consequence). The M-B monitor is built/acceptance-passed and
  could be pointed at the live account's event stream as an alert-only layer — optional operator
  election, alert-only, never an order path.
- [ ] **Q-SIGID-1 §2b clean re-measure** (pursuit c2, KEEP): the live↔backtest signal-identity
  gap measurement needs no fill/order/arming and de-risks the read on early live sessions — run
  it during D2's dry_run window.

## Task D5 — B7-REFIRE Stage 1 → armed sessions

- [ ] B7-REFIRE Stage 1 per the GO-ADR addendum: first real strategy entry at non-zero size,
  attended, on the ruled host — operator desk card, per-session GO, `armed_until` hours-scoped,
  **disarm before expiry** (the 2026-07-31 lapse self-bricked the host — the recovery sequence
  stays pre-read before every armed session).
- [ ] Every payload's `order_id`/`bar_time` freshly generated (idempotency DISPROVEN — a re-sent
  file is a live order).
- [ ] First strategy-signal fill → EventLedger EQ fields (S4 schema, landed) begin capturing;
  the five fill-gated threads move from gated to live on their own artifacts.

## Task D6 — Post-deploy observation frame (first weeks)

- [ ] Execution-quality reads (fills/exits vs backtest assumptions) through the EventLedger —
  the standing research interest suspended at the de-scope resumes with a live data source.
- [ ] Lifecycle Call-1 σ-source starts accumulating (rolling live PF) — thin-data AMBIGUOUS is
  the expected early state, recorded as such.
- [ ] No mid-flight parameter or sizing edits — decay/de-risk moves only through the lifecycle
  ladder's pre-registered triggers, down-only automation, operator GO for anything else.

## Exit criteria

M1 `RESOLVED` on real-signal evidence · B7-REFIRE Stage 1 complete · ≥1 armed session with a
strategy-signal fill, disarmed cleanly, reconciled `CHAIN_OK`, and the deployment recorded in the
venue-edition ledger. From there, live operation is governed by the standing ops posture, not
this plan.
