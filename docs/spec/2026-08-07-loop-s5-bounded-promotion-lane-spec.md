# SPEC S5: bounded promotion lane

Status: RESOLVED · 2026-08-07 · ADR Accepted + validator fixtures · authorizes nothing beyond the lane doctrine ($0 · K=0) · depends: S1, S4
Objective: Amend authorization by ADR — automation may promote a gate-validated candidate
into a capped sandbox (micro size · fixed per-candidate loss/attempt budget · capped
concurrency), the operator approving budgets rather than candidates, every
ceiling-crossing staying operator-only, demotion staying universal and instant, and the
up direction gaining **exactly this bounded exception** to down-only.

Steps:
1. Author the ADR; evidence section = the measured failure→requirement map: confabulated
   handoffs → artifact-only packets (every claim re-executed, prose carries nothing) ·
   wrong-units §R attestations (M-20, fired twice) → same-units schemas enforced at parse ·
   form-only intake gates → paired positive/negative self-test in the same invocation ·
   selection creep → freeze-commit hash match required · plus an independent adversarial
   refuter stage before any promotion. The ADR carries Supersedes-in-part edges naming
   what the budget lane replaces: lifecycle ADR Call 5 (no autonomous promotion), M1 ADR
   §5 (no autonomous promotion path), harvest §1 / de-scope-Addendum per-candidate
   operator GO — nothing is superseded until this ADR is Accepted.
2. Build the packet validator + refuter stage.
3. Wire ceilings as hard config read at promotion time; log every promotion/demotion to
   S4's ledger.

Gate: RESOLVED if ADR Accepted AND the validator rejects a synthetic confabulated packet
while passing a clean one (both fixtures committed); FALSIFIED if the ADR is rejected or
the validator passes the confabulated fixture.
Boundary: automation never crosses a ceiling, funds an account, sizes up past the sandbox,
or edits gates/budgets/its own validator; the reflex layer (`dry_run` interlock ·
`armed_until` · fresh idempotency tags) is untouchable; attended-only posture and the
per-armed-session operator GO stand — unattended-loop authorization is a separate ADR
requiring automated downstream truth (M1 ADR).
Reads (at HEAD `a6a5fe6` 2026-08-07): `core/lifecycle.py` ·
[strategy_harvest §1](../methodology/strategy_harvest.md) ·
[lifecycle ADR](../adr/2026-07-10-strategies-never-locked-lifecycle-governance.md) ·
[M1 ADR Addendum 2026-07-31b](../adr/2026-07-22-c1-venue-native-monitoring-maturity.md)
Owner: new ADR.
