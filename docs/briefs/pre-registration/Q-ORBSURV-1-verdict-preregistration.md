# Q-ORBSURV-1 — Verdict pre-registration

**Frozen:** 2026-08-20, before Phase 1 runs. Byte-unedited from this point forward — amendments via
a fresh Q, never an in-place edit (brief-authoring Known Trap #12).

---

## Configurations under test (frozen; exactly these three, no substitution)

| # | Configuration | Panel scope | k | Status before this pre-registration |
|---|---|---|---|---|
| 1 | Full-panel, cushion sizing | entire ORB-MNQ-1 history (`recon`, n=1,846 active days) | 2 | **Not yet measured** — only k=1 full-panel and k=1/k=2 halves exist |
| 2 | Post-break-only, cushion sizing | dates ≥ 2021-09-28 only (`Q-ORBCUSH-1`-established break date) | 1 | **Not yet measured** — only implied by the thirds-split numbers, never gated directly |
| 3 | Post-break-only, cushion sizing | dates ≥ 2021-09-28 only | 2 | **Not yet measured** |

**Reused, not re-derived (frozen reference point, not a fourth test):** full-panel k=1, already measured 2026-08-20 in `orbmnq1_nsurv_magnitude_probe_2026-08-20/nsurv_magnitude_probe_results.json` — bust 0.0000%, pass 52.2700%, `floor_ok=True`.

## Frozen gate (byte-identical to the estate's standing gate)

- **Bust ceiling:** ≤ 3.0% (intraday-honest, `use_intraday=True`).
- **Pass floor:** P(pass) ≥ 50%.
- **Both limbs required** — same two-part ceiling as `docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md` §3 and the re-PARK ADR's own §4.
- **Sizing policy:** `pol_cushion` (ceiling 0.75), quoted unchanged from `run_evalseq_orb_intraday.py`. No parameter search, no ceiling adjustment.
- **Seeds/thresholds:** `load_scoring_thresholds()` — the same frozen production seeds/horizon/sims-per-seed every N-SURV-gated verdict in the estate uses. Not re-picked for this Q.

## Ambiguous-hold floor (frozen)

Post-break sub-window (configurations 2 and 3) must form **≥ 20** Mon-anchored 5-day blocks (`blocks_from_panel`) to be trusted. Below 20, report `AMBIGUOUS-HOLD` for that specific configuration rather than a number — do not report a gate verdict computed from fewer than 20 blocks.

## Gate criteria (verbatim from parent brief §6; restated here as the frozen artifact of record)

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` | Configurations 1, 2, AND 3 all clear bust≤3.0% ∧ pass≥50% | `INTEGRATE` — ADR addendum to the re-PARK ADR, scope-only |
| `FALSIFIED` | Any of configurations 1/2/3 misses either limb | `STOP` — configuration-dependent gate-clear, negative finding recorded |
| `AMBIGUOUS-HOLD` | Configuration 2 or 3 has < 20 blocks | `ITERATE` — re-test once panel extends |

## Mandatory disclosure (frozen; carried from Q-NSURV-1/N18, not optional)

Every pass% number this pre-registration's Phase 1/2 produces must be reported alongside the following sentence, unedited: *"The pass-rate axis under magnitude-resampling on this same sizing mechanism showed sd=24.17pp and only 50% of resampled histories clearing the combined gate (`ops/instruments/MNQ.md` N18) — a single-history pass% above 50% is not, by itself, strong evidence the mechanism reliably clears the floor."*

## Explicit non-negotiables

- No threshold (3.0% ceiling, 50% floor, 0.75 sizing ceiling, 20-block Ambiguous floor) may be loosened, tightened, or reworded once Phase 1 has run even once, for any configuration. A miss is a miss.
- All three configurations run and report regardless of individual outcome — none may be dropped after seeing its result.
- Configuration 1's reused k=1/full-panel reference number is quoted verbatim from the existing artifact, never re-run.

**Committed:** 2026-08-20, same batch as `docs/briefs/Q-ORBSURV-1-cushion-sizing-gate-configurations.md`. Phase 1
has not run as of this commit.
