# Q-GATESTACK-1 — verdict pre-registration

**Frozen:** 2026-08-19, before Phase 1 result inspection — the gate criteria below are
transcribed verbatim from `Q-GATESTACK-1-gate-stack-enforcement.md` §6, which was itself
written and locked on 2026-08-18, one session before this pre-registration and Phase 1
execution. No criterion here was chosen or adjusted after seeing `gh api` output.

**Process note (honest disclosure, not a gap-paper):** the brief's §7 sequencing calls for
this pre-registration to be committed, then Phase 1 run, as two separate steps. Under
operator GO ("close the loop, I ratify," 2026-08-19) this file and the Phase 1 execution
happened inside the same turn rather than across two — the criteria were already frozen in
the brief's own §6 the day before, so there was no opportunity for the *content* of this
pre-registration to be shaped by the results, but the letter of "committed before any `gh`
call runs under this brief" was not observed as two distinct turns. Recorded here rather
than silently presented as clean two-step sequencing.

---

## Frozen gate (verbatim from §6)

| Verdict | Trigger condition | Disposition (typed) |
|---|---|---|
| `RESOLVED` | Limb-A accepts (main platform-enforced) AND Limb-D accepts (CI-status docs match live state) | `INTEGRATE` — record both claims as evidence-ratified; discharge A1/D7 in the audit note's own routing table. No config or doc changes made under this brief. |
| `FALSIFIED` | Limb-A rejects and/or Limb-D rejects (reproduces the audit's 404/`[]`/`push:true` state and/or `enabled:true`-with-green-runs state) | `ITERATE` — name (do not open) two successor decision packets: (1) branch-protection/ruleset authoring for `main`; (2) a doc correction to `CLAUDE.md:218`, `manifest-check.yml:82-88`, `post-merge:34-38` flipping the "disabled" claim. Operator GO required for either. |
| `AMBIGUOUS-HOLD` | A `gh` call returns an auth/rate-limit/scope error, or an intermediate state neither limb's binary test can resolve at $0 | `ITERATE` — re-test when operator-level GitHub admin access is available. |

## Reject conditions (verbatim from §4)

- **Limb-A rejects if:** re-check returns 404 / `[]` / `push:true`-present.
- **Limb-D rejects if:** re-check returns `enabled:true` with ≥1 `success` run on
  `manifest-check.yml` since 2026-08-15.
- Overall verdict is `FALSIFIED` if either or both limbs reject.

**Commitment:** the verdict below will be read mechanically off these rows against the
Phase 1 output — no re-framing after the fact.
