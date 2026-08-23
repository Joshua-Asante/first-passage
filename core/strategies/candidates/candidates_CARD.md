# candidates

**Family:** candidates
**Disposition:** MIXED — see per-file note below (Phase A cold-store body stays FALSIFIED_PARKED;
`expiry-oi-strike-convergence` operator-`PARKED` 2026-08-21)
**Body:** `core/strategies/_archive/candidates/`

## Live candidate — `PARKED` 2026-08-21 (hash-pinned 2026-08-23)

- `expiry_oi_strike_convergence_mgc_v0_1.pine` — MSL-S4 (`expiry-oi-strike-convergence` on MGC),
  G0 FROZEN 2026-08-21, `pine_lint` PASS 13/13 (re-verified 2026-08-23 on the durable local
  checkout, unchanged). Authored in an ephemeral cloud session and sent directly to the operator
  rather than committed — see `lab/analysis/c1/msl_s4_mgc_2026-08/RUNBOOK.md` §The Pine file for
  why (avoids the unrecoverable-pin-bytes failure mode `check_pine_manifest.py` exists to catch).
  **Hash-pinned 2026-08-23** from the operator's own durable Downloads copy — see Hash pins below.
  ⚠ **The RUNBOOK's own recommended next step (a manual TV backtest) is superseded, same-day —
  do not follow it.** The Explore-confirm the RUNBOOK described as deferred was, in fact, run
  later the same session (`_explore_confirm_2026-08-21_LOG.md`) and is what this PARK rests on.
  **`PARKED` 2026-08-21 (operator decision)**, following the pre-registered Explore-confirm's
  `AMBIGUOUS-HOLD` verdict —
  [`_explore_confirm_2026-08-21_LOG.md`](../../../lab/analysis/c1/msl_s4_mgc_2026-08/_explore_confirm_2026-08-21_LOG.md):
  real mean displacement reduction negative (net divergence, not convergence), `p_upper=0.5724`
  (not significant vs. an IAAFT-surrogate null), FLIP FAILs (divergence beat convergence
  empirically — the construct's own directional claim did not hold up). Not formally `FALSIFIED`
  under the frozen gate's literal `p_upper>0.95` line, hence `PARKED` rather than
  `FALSIFIED_PARKED` — distinct from the cold-store body below. **Re-proposal bar:** new mechanism
  evidence (a different OI-derived reference, a different displacement/direction rule) — not a
  re-tune of the arm-window width or displacement threshold, not a re-read of this same IAAFT
  result, not the operator's own TV backtest treated as a substitute score.

## Hash pins

- `cfd8c7fb29626d192b994a99ab0f9b7acecdf20b26acf32dcc8a92dba272c056  core/strategies/candidates/expiry_oi_strike_convergence_mgc_v0_1.pine` — pinned 2026-08-23 on the operator's durable local checkout, per `core/strategies/MANIFEST.sha256`. The Phase A cold-store body still has none.

## ADR

- `docs/adr/2026-08-04-strategy-coldstore-phase-a.md`
