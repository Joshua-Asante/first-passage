# Q-NSURV-2 — Verdict pre-registration

**Frozen:** 2026-08-20, before Phase 1 runs. Byte-unedited from this point forward — amendments via
a fresh Q, never an in-place edit (brief-authoring Known Trap #12).

---

## Reproduction targets (frozen; the two numbers any wrapper must hit)

| Candidate | Source artifact | Headline metric | Frozen target value |
|---|---|---|---|
| c1 book (2-leg) | `lab/analysis/c1/geofit_skewed_family_construction_2026-08-15/characterize.json` | single-history bust% | `bust_mean` field read directly from the artifact — the wrapper's OWN independent computation over the same fitted-family draws must land within 2.0pp of whatever that field currently reads |
| ORB-MNQ-1 | `lab/analysis/c1/orbmnq1_nsurv_magnitude_probe_2026-08-20/nsurv_magnitude_probe_results.json` | real single-history bust% / pass% (`real_single_history_cushion`) | bust **0.0000%**, pass **52.2700%** (both conventions — `equivalence_ok: true`) |

**Fidelity tolerance:** 2.0pp absolute, matching the estate's existing convention (`docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md` §4 fidelity-control precedent, restated in `run_evalseq_orb_intraday.py`'s own docstring).

## Reproduction method (frozen; what "additive, no internals touched" means operationally)

The wrapper script MAY:
- Read the two candidates' already-committed JSON artifacts.
- Compute percentile statistics (mean/median/sd/percentiles) over the resampled distributions already stored in those artifacts.
- Independently recompute each candidate's headline point estimate from the artifact's own stored per-realization data (not by re-calling `run_partition_mc`/`family_skewed_gamma`/`family_skewed_gamma_orb` with new draws) — this is the bit-identical-reproduction check.

The wrapper MUST NOT:
- Call `run_partition_mc`, `blocks_from_daily_pnl`, or `simulate_path` with arguments that differ from what production already passes for either candidate.
- Draw fresh MC realizations (would not be "reproduction" — would be a new, unregistered measurement).
- Modify any file under `lab/discovery/` or `core/`.

**Pass/fail rule for Phase 1's own bit-identical check:** if the wrapper's independently-recomputed headline for either candidate differs from the frozen target value above by more than 2.0pp, Phase 1 halts and reports `FALSIFIED` per §6 of the parent brief — no further Phase 1 steps run.

## Gate criteria (verbatim from parent brief §6; restated here as the frozen artifact of record)

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` | Both candidates reproduce within 2.0pp, zero `run_partition_mc`/`blocks_from_daily_pnl` internals touched, resampled bands additively emitted | `INTEGRATE` — draft disclosure-only ADR |
| `FALSIFIED` | Either candidate fails to reproduce within 2.0pp without touching internals | `STOP` — additive shape not achievable; heavier ADR is a separate future decision |
| `AMBIGUOUS-HOLD` | One candidate reproduces, the other does not | `ITERATE` — re-test scoped to the failing candidate |

## Explicit non-negotiables

- No reproduction tolerance may be loosened, tightened, or reworded once Phase 1 has run even once, for either candidate. A miss is a miss.
- The wrapper's independence from `run_partition_mc`/`blocks_from_daily_pnl` internals is checked by static inspection of the wrapper script's own imports/calls (audit hook below) — not by developer assertion.
- Both candidates are tested regardless of which one is easier; neither may be dropped from the reported verdict after seeing its result.

## Audit hook (frozen; confirms no internals were touched)

```bash
# The wrapper script must not import run_partition_mc, blocks_from_daily_pnl, or simulate_path
# with call signatures differing from production's own existing call sites.
grep -n "run_partition_mc\|blocks_from_daily_pnl\|simulate_path" \
  lab/analysis/c1/nsurv_layer_design_2026-08-20/run_wrapper_reproduction_check.py
# Expected: either no matches (pure JSON-artifact consumption), or matches with args identical
# to the production call sites already in lab/discovery/prop_survivor_scoring.py /
# lab/analysis/c1/orbmnq1_cushion_sizing_probe_2026-08-20/run_evalseq_orb_intraday.py
```

**Committed:** 2026-08-20, same batch as `docs/briefs/Q-NSURV-2-second-uncertainty-layer-design.md`. Phase 1
has not run as of this commit.
