# Q-NSURV-2 — Verdict pre-registration

**Frozen:** 2026-08-20, before Phase 1 runs. Byte-unedited from this point forward — amendments via
a fresh Q, never an in-place edit (brief-authoring Known Trap #12).

---

## Correction (pre-Phase-1, 2026-08-20)

The first draft of this table named the c1 reproduction target "single-history bust%" but pointed
at the `bust_mean` field, which is actually the **resampled-distribution mean** (7.46%), not the
single real-history draw (`real_bust_reference`, 4.7433%) — two different numbers this Q's own
parent brief (§1) elsewhere keeps distinct. Caught before Phase 1 ran (no result seen yet), so this
is a drafting fix, not a Known-Trap-#12 amendment. Corrected below: this pre-registration now
separates the two kinds of number the wrapper touches — the fixed single-history headline (echoed,
never recomputed, since there is only one real history to echo) and the resampled-distribution
statistics (independently recomputed from `runs[]`, the genuine reproduction test).

## Reproduction targets (frozen; two distinct kinds of number per candidate)

**(A) Single-history headline — echoed unchanged, not recomputed** (there is exactly one real
history; nothing to independently re-derive from multiple realizations):

| Candidate | Source field | Frozen value |
|---|---|---|
| c1 book (2-leg) | `characterize.json` → `real_bust_reference` | bust **4.7433%** |
| ORB-MNQ-1 | `nsurv_magnitude_probe_results.json` → `real_single_history_cushion.intraday_honest` | bust **0.0000%**, pass **52.2700%** (`equivalence_ok: true`) |

**(B) Resampled-distribution statistics — independently recomputed from `runs[]`, checked against
the artifact's own already-stored summary** (this is the actual reproduction test):

| Candidate | Per-realization field in `runs[]` | Artifact's own stored summary to match |
|---|---|---|
| c1 book (2-leg) | `runs[i].headline_bust` (n=50) | `bust_mean` **0.074637**, `bust_sd` **0.070689** |
| ORB-MNQ-1 | `runs[i].bust_pct`, `runs[i].pass_pct` (n=50) | `distribution.bust_mean` **0.0**, `distribution.pass_mean` **50.6927**, `distribution.pass_sd` **24.1700** |

**Fidelity tolerance:** 2.0pp absolute (on the (B) recomputation only — (A) is a direct field read,
either it matches exactly or the artifact was edited), matching the estate's existing convention
(`docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md` §4 fidelity-control precedent,
restated in `run_evalseq_orb_intraday.py`'s own docstring).

## Reproduction method (frozen; what "additive, no internals touched" means operationally)

The wrapper script MAY:
- Read the two candidates' already-committed JSON artifacts.
- Echo each candidate's (A) single-history headline value verbatim (string/number read, no computation).
- Independently compute (B) mean/median/sd/percentiles over each candidate's `runs[]` array and compare to the artifact's own stored summary — this is the bit-identical-reproduction check.

The wrapper MUST NOT:
- Call `run_partition_mc`, `blocks_from_daily_pnl`, or `simulate_path` with arguments that differ from what production already passes for either candidate.
- Draw fresh MC realizations (would not be "reproduction" — would be a new, unregistered measurement).
- Modify any file under `lab/discovery/` or `core/`.

**Pass/fail rule for Phase 1's own bit-identical check:** if (A) fails to match exactly for either candidate, OR the wrapper's independently-recomputed (B) statistics for either candidate differ from the artifact's own stored summary by more than 2.0pp, Phase 1 halts and reports `FALSIFIED` per §6 of the parent brief — no further Phase 1 steps run.

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
  lab/archive/nsurv_layer_design_2026-08-20/run_wrapper_reproduction_check.py
# Expected: either no matches (pure JSON-artifact consumption), or matches with args identical
# to the production call sites already in lab/discovery/prop_survivor_scoring.py /
# lab/analysis/c1/orbmnq1_cushion_sizing_probe_2026-08-20/run_evalseq_orb_intraday.py
```

**Committed:** 2026-08-20, same batch as `docs/briefs/Q-NSURV-2-second-uncertainty-layer-design.md`. Phase 1
has not run as of this commit.
