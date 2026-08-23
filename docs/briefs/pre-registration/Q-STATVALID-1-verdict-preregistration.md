# Q-STATVALID-1 — Verdict pre-registration

**Frozen before either Phase 1 read runs.** Per brief §8. Committed in spirit ahead of any
result — the criteria below are copied verbatim from the brief's own §4/§6 plus the exact
operational thresholds this session commits to before opening a single file's numeric content.

---

## Gate table (verbatim from brief §6)

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED` | Both limbs Reject: B — no lag 1-4 autocorrelation breaches ±2/√n and Ljung-Box p ≥ 0.05 at lags 1-4; AND C — deflated winner margin exceeds the noise floor in both grids | `INTEGRATE` |
| `FALSIFIED` | Either limb Accepts: B — any lag 1-4 breach or Ljung-Box p<0.05; OR C — deflated margin collapses into noise floor, or losing-candidate scores are unrecoverable | `ITERATE` |
| `AMBIGUOUS-HOLD` | Panel data or logged grid scores for either limb are not locatable at $0/K=0 | `ITERATE` — named absence-finding |

## Limb B — exact frozen threshold

- Test: Ljung-Box on the weekly-aggregated P&L series produced by `core/mc/ingest.py::build_week_blocks`, lags 1-4, plus a bare ACF-vs-band cross-check.
- Reject (clean) iff: Ljung-Box p ≥ 0.05 at **all** of lags 1, 2, 3, 4, **and** |ACF(k)| ≤ 2/√n for **all** of k=1,2,3,4 (n = number of weekly blocks in the series actually read).
- Accept (fires) iff: **any** lag in {1,2,3,4} has Ljung-Box p < 0.05, **or** |ACF(k)| > 2/√n for **any** k in {1,2,3,4}.
- Ambiguous-hold iff: the panel this session is meant to read (i.e., the locked panel underlying the `dd_protection` calibration / MC anchor figures cited in brief §1) is not loadable at $0 without a new data pull/re-export. A different, non-equivalent panel being loadable does **not** discharge this — it is recorded as a separate, explicitly-labeled supplementary check only.

## Limb C — exact frozen deflation/margin formula

Applied per grid (DD_TRIGGER/DD_SCALE 5-config grid, `docs/adr/2026-04-17-dd-trigger-calibration.md`; allocation 8-config grid, `core/mc/modes.py` `SWEEP_CONFIGS`):

1. Identify the winner's headline metric (bust rate) and the closest-ranked runner-up(s) among candidates that carry an exact retained numeric score.
2. If fewer than 2 candidates in a grid carry retained exact numeric scores sufficient for step 3 — **Accept fires immediately for that grid** ("losing-candidate scores never retained"), independent of step 3.
3. Otherwise, compute the cheaper proxy explicitly licensed by brief §7: treat each candidate's bust rate as a Bernoulli proportion, `SE = sqrt(p(1-p)/N)`, where `N` = the MC path count feeding the scored run (this session uses the currently-registered `core/mc/modes.py` constants `SIMS_PER_SEED=10,000 × len(SEEDS)=3 → N=30,000` as the documented proxy where the historical run's own N is not independently restated in its ADR/closure — flagged as an assumption, not re-derived).
4. `SE_diff = sqrt(SE_winner² + SE_runner²)`; `margin = |p_winner − p_runner|`; `z = margin / SE_diff`.
5. Collapse-into-noise-floor (Accept) iff `z < 2` (conventional 2-sigma bar — the same order of magnitude as the Ljung-Box companion band's own ±2/√n convention). Exceeds-noise-floor (contributes toward Reject) iff `z ≥ 2`.
6. This is a **lower bound** on the correction, not the full deflation: applying any positive E[max of N] multiplicity discount on top of step 5 can only raise the bar further, never lower it. If `z < 2` on the raw (undeflated) margin already, the fully-deflated comparison necessarily also collapses — this session will state the raw-margin result and note the multiplicity discount is directionally conservative, without needing to compute the exact order-statistic constant for N=5 / N=8.

## Overall verdict resolution rule (frozen)

Per brief §4's own text, a limb whose data is unlocatable ("Ambiguous-hold") converts **that limb** to a named absence-finding, not a null Reject — it does not by itself force the top-level verdict to `AMBIGUOUS-HOLD` if the **other** limb reaches a decisive Accept/Reject on data that **is** locatable. `AMBIGUOUS-HOLD` as the overall verdict is reserved for the case where no limb reaches a decisive read. If Limb C decisively Accepts (fires) while Limb B is blocked on missing data, the overall verdict is `FALSIFIED`, and Limb B's blocked status is carried into the closure as its own named absence-finding requiring an independent re-test trigger — not folded into a top-level `AMBIGUOUS-HOLD`.

This resolution rule is stated here, before either read runs, precisely because brief §6's two non-RESOLVED rows have overlapping literal trigger text ("panel data ... not locatable" could describe a sub-condition of either row) and Known Trap #12 forbids re-deriving this rule after seeing which condition actually fires.
