# ADR 2026-08-07 — Loop S5: bounded promotion lane

**Status:** `Accepted` — implements [SPEC S5](../spec/2026-08-07-loop-s5-bounded-promotion-lane-spec.md); plan-execution GO 2026-08-07
**Decision date:** 2026-08-07
**Authors:** Joshua (plan GO) + Cursor (drafter)
**Supersedes:** `2026-07-10-strategies-never-locked-lifecycle-governance.md` in part — Call 5 absolute “no autonomous promotion” invariant only (bounded sandbox-up exception; demotion / retirement GO / RETIRED re-entry bar / re-optimization bar stand)
**Supersedes:** `2026-07-22-c1-venue-native-monitoring-maturity.md` in part — §5 forbidden move “autonomous promotion path” limb only (no second tier/state writer; arm-gate + reflex + unattended bar stand)
**Supersedes:** `2026-07-15-external-mechanism-harvest-intake.md` in part — per-candidate operator GO before capital/account action only as applied to in-ceiling sandbox admits (budget approval; Stage-0 / K / cost-law / ceiling-crossing GOs stand)
**Supersedes:** `2026-08-04-tradeify-venue-descope-eval-included.md` in part — Addendum 2026-08-04 “separate operator GO before any capital or account action” only for in-ceiling sandbox admits (clauses 1–2 + Striker redeploy bar stand)
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Related:** [SPEC S5](../spec/2026-08-07-loop-s5-bounded-promotion-lane-spec.md) · [S1 ADR](2026-08-07-loop-s1-environment-ratification.md) · [SPEC S4](../spec/2026-08-07-loop-s4-sensor-layer-spec.md) · [lifecycle owner](../methodology/strategy_lifecycle.md) · [alignment manifest](../notes/2026-08-07-posture-a-alignment-manifest.md)
**Layer:** authorization / discovery promotion only. **$0 / K=0** — authorizes the lane doctrine + validator; does **not** arm the rail, place trades, fund accounts, or authorize unattended operation.

---

## §0 — Rule 0 reads (verified 2026-08-07)

| Source | Anchor | What it pins |
|---|---|---|
| [SPEC S5](../spec/2026-08-07-loop-s5-bounded-promotion-lane-spec.md) | `aee4137` | Bounded sandbox; budgets not candidates; ceiling-crossings operator-only; demotion universal+instant; failure→requirement map; reflex untouchable |
| [`core/lifecycle.py`](../../core/lifecycle.py) | `ef4e89c` | `autonomous_demote` floors at WATCH-2; no promote path in code today |
| [lifecycle ADR Call 5](2026-07-10-strategies-never-locked-lifecycle-governance.md) | Accepted 2026-07-10 | Hard asymmetry: automation down-only; no autonomous promotion |
| [M1 ADR §5](2026-07-22-c1-venue-native-monitoring-maturity.md) | Accepted + Addendum 2026-07-31b | Forbidden autonomous promotion path; arm-gate; unattended barred |
| [strategy_harvest §1](../methodology/strategy_harvest.md) + de-scope Addendum | Accepted | Research ≠ deployment; separate operator GO before capital/account action |
| [S1 ADR](2026-08-07-loop-s1-environment-ratification.md) | Accepted same day | Environment = incumbent eval; rail warm/disarmed — lane does not arm |

---

## §1 — Context

Closed-loop SPEC S5 requires an authorization amendment: automation may admit a **gate-validated** candidate into a **capped sandbox** (micro size · fixed per-candidate loss/attempt budget · capped concurrency) without a fresh per-candidate capital GO, while the operator approves **budgets** and every ceiling-crossing stays operator-only. Demotion stays universal and instant. The up direction gains **exactly this bounded exception** to Call 5’s down-only rule — nothing wider.

The evidence for the packet contract is the measured failure→requirement map (not a greenfield design):

| Measured failure | Requirement locked into the packet |
|---|---|
| Confabulated handoffs (prose carrying the load) | **Artifact-only packets** — every claim cites a re-executable path; prose carries nothing |
| Wrong-units §R attestations (M-20, fired twice) | **Same-units schemas enforced at parse** (`GATE_REQUIRED_UNITS`) |
| Form-only intake gates | **Paired positive/negative self-tests in the same invocation** |
| Selection creep after freeze | **Freeze-commit hash match** (`freeze_commit` == `observed_freeze_commit`) |
| Residual confabulation / ceiling games | **Independent adversarial refuter** before any promote |

---

## §2 — Decision

**Bounded promotion lane — Accepted.**

1. **Automation may promote** a packet that Passes `validate_promotion_packet` **and** `refute_promotion_packet` into the sandbox defined by hard ceilings in [`lab/discovery/promotion_ceilings.json`](../../lab/discovery/promotion_ceilings.json) (read at promotion time).
2. **Operator approves budgets, not candidates.** The packet carries `operator_budget_approval_id`; per-candidate GO is not required inside ceilings.
3. **Ceiling-crossings are operator-only.** Automation never edits ceilings, funds accounts, sizes past sandbox, or edits gates/budgets/its own validator.
4. **Demotion is universal and instant** — Call 5 down-path unchanged; any demotion event is immediate.
5. **Up-direction exception is exact.** Call 5’s “never promotes” gains only this sandbox admit. No autonomous path to full AUTHORIZED book size, no RETIRED re-entry, no re-optimization.
6. **Reflex layer untouchable:** `dry_run` interlock · `armed_until` · fresh idempotency tags — unchanged. This ADR does not set `dry_run=false`, does not arm, and does not authorize unattended loops (separate ADR requiring automated downstream truth per M1).

**Effective:** immediately upon Accept (2026-08-07).
**Spend:** $0 / K=0 / no arming / no agent trade.

**Implementation artifacts (same change-set):**
- [`lab/discovery/promotion_packet.py`](../../lab/discovery/promotion_packet.py) — validator + event TypedDict stubs for S4 ledger
- [`lab/discovery/promotion_refuter.py`](../../lab/discovery/promotion_refuter.py) — adversarial stage
- Fixtures: `tests/fixtures/promotion/clean_packet.json` (Pass) · `confabulated_packet.json` (Fail)
- Tests: `tests/test_promotion_packet.py`

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Keep absolute no-promote (Call 5 as-is) | Blocks closed-loop sandbox learning; SPEC S5 plan default is the bounded exception |
| Full autonomous promotion to AUTHORIZED | Violates reversibility boundary; retirement/re-entry asymmetry |
| Per-candidate operator GO for every sandbox admit | Re-imports operator as the bottleneck the lane is meant to remove; budgets are the right approval object |
| Soft / advisory ceilings | Ceiling-crossings must be hard-fail; soft ceilings are confabulation |
| Wire EventLedger append + arm under this ADR | M1 not RESOLVED; reflex untouchable; stub events only |

---

## §4 — Falsifier (revert trigger)

**H:** After Accept, sandbox admits require Pass validator + Pass refuter against committed fixtures; automation never crosses a ceiling; CLAUDE.md / lifecycle owner name the bounded up-exception; rail remains disarmed under this ADR alone.

**Revert / FALSIFIED (any limb):**
1. Validator Passes `tests/fixtures/promotion/confabulated_packet.json` → lane DEAD; tear back.
2. Automation crosses a ceiling, funds an account, or sizes past sandbox without operator GO → supersede + disarm.
3. Silent re-read that restores absolute “never promotes” *or* widens to full AUTHORIZED auto-promote without a superseding ADR → supersede.
4. This ADR used to set `dry_run=false` or authorize unattended operation → unauthorized; tear back.

**Trigger check schedule:** first sandbox admit attempt, or 2026-08-08 programme audit — run `pytest tests/test_promotion_packet.py`.

---

## §5 — Forbidden moves

- Arming the rail or setting `dry_run=false` under this ADR.
- Unattended-loop authorization (separate ADR; requires automated downstream truth).
- Automation editing ceilings, budgets, gates, or the validator/refuter to admit a packet.
- Promoting without freeze-commit match, without paired self-tests, or on prose-only claims.
- Treating sandbox admit as full AUTHORIZED book membership or as M1 `RESOLVED`.
- Redeploying withdrawn Striker legs.
- Touching the reflex layer (`dry_run` interlock · `armed_until` · idempotency tags).

---

## §6 — Consequences

- Call 5 / lifecycle owner / CLAUDE.md gain the bounded up-exception pointer (S7 S5-ADR sweep).
- M1 §5 autonomous-promotion limb superseded in part; monitoring arm-gate stands.
- Harvest §1 / de-scope Addendum per-candidate capital GO superseded **only** for in-ceiling sandbox admits; budget approval replaces candidate GO there.
- S4 ledger: `PromotionEvent` / `DemotionEvent` TypedDict stubs documented; append wiring waits on M1 `RESOLVED`.
- Unblocks closed-loop sandbox learning after S4 sensor path exists; does not itself create fills.

---

## §7 — Propagation (S7 S5-ADR section)

Discharged in the same change-set as Accept — see [alignment manifest](../notes/2026-08-07-posture-a-alignment-manifest.md) §S5-ADR.
