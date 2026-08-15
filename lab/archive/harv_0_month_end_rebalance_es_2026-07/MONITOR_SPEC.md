# MONITOR SPEC — HARV-2026-001 (template; fill if RESOLVED)

**Status:** TEMPLATE — mandatory closure deliverable iff verdict = RESOLVED
(brief §6). Invalid to close RESOLVED without a filled monitor.

**Operationalization:** identical to brief §4 (frozen). Do not retune windows or
the 100bp threshold in the monitor.

---

## Estimate

- **Metric:** rolling **24-month** mean signed window return under the frozen
  rule (qualifying months only; signal × close(T-3)→close(T-1) log return on
  the live expression instrument — parent ES for research continuity / MES if
  deployed on micro).
- **Refresh:** month-end, after CME session settle dates for the just-closed month.
- **Cost reference:** recompute empirical 1× single-RT hurdle from current MES
  (or live contract) specs at each refresh; store alongside the estimate.
- **Null / baseline:** the registration-era conditional mean is the admission
  reference; the monitor tracks *decay relative to cost*, not re-optimization.

## Pre-committed weakening trigger (Q-DECAY-1 payoff)

Trigger a **de-size / retire review** (operator GO/NO-GO; automation may only
move risk *down*) if **either**:

1. **Sign flip:** rolling 24m conditional-effect estimate changes sign vs the
   RESOLVED admission sign, **or**
2. **Below hurdle streak:** `|estimate| < 1× cost hurdle` for **12 consecutive**
   calendar months.

Both conditions are evaluated on the frozen operationalization. No widening of
windows or threshold nudges to "save" the monitor.

## Actions on trigger

1. Log the breach date, rolling estimate, hurdle, and which clause fired.
2. Demote authorization / size per strategy-lifecycle ladder (operator confirms
   irreversible retirement).
3. Do **not** re-fit parameters. A decayed candidate is retired to zero or
   forked under a **new** registered ID + K increment.

## Non-triggers (explicit)

- Single-month noise inside a still-positive 24m window.
- Unconditional TOM drift appearing/disappearing.
- Envelope / firm-rule overlays (those are deployment forks, not mechanism decay).

## Fill-in after RESOLVED

| Field | Value |
|---|---|
| Admission sign | _TBD_ |
| Admission 24m mean (bp) | _TBD_ |
| Admission 1× hurdle (bp) | _TBD_ |
| First monitor month | _TBD_ |
| Owner / review cadence | quarterly with 08-08 / 11-08 board |
