# Q-TRADECAP-1 — Verdict pre-registration

**Frozen:** 2026-08-23, before Phase 1 runs (operator GO given in chat: *"GO on Q-TRADECAP-1"*).
Byte-unedited from this point forward — amendments via a fresh Q, never an in-place edit
(brief-authoring Known Trap #12).

---

## Checks under test (frozen; exactly these four, no substitution)

| # | Limb | Check | Source |
|---|---|---|---|
| 1 | Sizing + Arming (absence) | Repo-wide grep for per-trade/loss-cap-shaped tokens across `core/ ops/ docs/adr/ docs/spec/ docs/notes/rail_build/`; classify every hit | parent brief §7 Phase 1 |
| 2 | Sizing (end-to-end) | Read `core/dd_protection.py`'s `calculate_protection()` (L190–226) for a per-trade-dollar-cap parameter | parent brief §0/§7 |
| 3 | Arming (end-to-end) | Read `ops/c1_rail/c1_rail_arm.py`'s `validate()`/`REQUIRED_DRILLS` chain (via `scripts/validate_c1_monitoring_acceptance.py`) for a risk-of-ruin-shaped drill | parent brief §0/§7 |
| 4 | Adjacent | Grep for `EM2` and `disaster.stop` wiring as a live arming precondition vs. a standalone doc | parent brief §0/§7 |

## Frozen classification categories (§5's forbidden-move list, restated as the closed set)

Every grep hit from check 1 must be sorted into exactly one of: **sizing-law-% input** / **account-level lock** (e.g. `firm_rules.py` "Max Loss Lock") / **daily-cadence target** (e.g. the MNQ daily-cadence spec's max-loss `L`) / **design-time screen** (EM2, candidate-admission only) / **genuine live per-trade-dollar bound**. No sixth category may be invented post-hoc to reclassify an inconvenient hit.

## Gate criteria (verbatim from parent brief §6; restated here as the frozen artifact of record)

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` | All four checks confirm no genuine bound exists — every classifiable hit sorts into a non-bound category | `INTEGRATE` — record A6 as formally confirmed; add a STATE.md OPERATOR QUEUE row naming a successor decision packet (per `1r_estimation.md`'s two staged options) for operator election. This brief authors no fix. |
| `FALSIFIED` | Any check surfaces a genuine live per-trade-dollar bound | `ITERATE` — name (not open) a successor packet to confirm the found bound's coverage against Tradeify_Select_100K's intraday-enforced geometry specifically |
| `AMBIGUOUS-HOLD` | A grep hit cannot be cleanly sorted into the frozen classification categories above without judgment this $0/K=0 brief cannot exercise | `ITERATE` — re-test once the ambiguous hit is resolved by its own owning artifact's next edit, or at the next c1-rail arming session, whichever is first |

## Explicit non-negotiables

- No classification category may be loosened, narrowed, or added once Phase 1 has run, for any hit. A hit that doesn't cleanly fit is `AMBIGUOUS-HOLD` for that hit, not a manufactured sixth category.
- All four checks run and report regardless of individual outcome — none may be dropped after seeing its result.
- The three already-classified near-misses from §0/§5 (daily max-loss `L`, EM2, account-level Max Loss Lock) are quoted as already-resolved false positives, not re-litigated as if newly found.

**Committed:** 2026-08-23. Phase 1 has not run as of this commit.
