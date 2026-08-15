# Pre-filter rank-correlation gate (Gen-2)

**Status:** Pre-registered invariant — extracted from Gen-1 sweep layer at retirement (ADR `docs/adr/2026-07-11-gen1-pipeline-retirement.md`, 2026-07-11).

## Invariant

A **pre-filter tier has no gate authority** until it clears a rank-correlation floor against the authoritative engine.

Gen-1 constants (frozen at retirement, not tunable post-hoc):

| Constant | Value | Role |
|---|---|---|
| `PREFILTER_RANK_RHO_FLOOR` | **0.70** | Spearman ρ floor — below this, the pre-filter is invalid and the design reverts to authoritative-only |
| `PARITY_NET_PF_BAND` | **0.02** | Net profit & profit factor within ≤2% at parity anchor |

## Gen-2 application

Apply the same falsifier to the **`vectorbt` (triage) ↔ `Nautilus` (fill-realism)** pair in every DISC-CAMP:

1. Run both engines on the same pre-registered config grid.
2. Compute Spearman rank correlation of a pre-registered ranking metric (e.g. net PF or Sharpe) across configs.
3. If ρ < 0.70 at the parity anchor config(s), the triage tier is **invalid** — no shortlist authority; revert to Nautilus-only (or manual authoritative confirm).
4. Record ρ + parity band outcome in the campaign manifest §5 evidence block.

## Provenance

- Gen-1 source: `lab/validation/sweep/__init__.py` @ `6bf0dff` (retired 2026-07-11).
- Superseding admission path: `strategy-validation` SKILL §8 + `docs/adr/2026-07-10-databento-research-stack.md`.

## Falsifier

If a DISC-CAMP survivor is blocked solely because triage↔fill-realism rank order diverges below 0.70 on structural (not data-bug) grounds, re-evaluate whether 0.70 is too strict for micro futures — but **do not tune ρ after seeing campaign results**; any threshold change requires a fresh pre-registration.
