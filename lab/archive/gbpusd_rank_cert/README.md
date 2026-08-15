# GBPUSD rank-ρ certification (representative window)

**Disposition:** RETIRED — UNCERTIFIED — manual TV step never run; not carried (2026-07-10)

> **NON-RUNNABLE 2026-07-11.** Scripts still import retired Gen-1
> `validation.sweep.*` / `validation.concept_intake.*` (harness deleted with
> ADR `2026-07-11-gen1-pipeline-retirement`). CI ignores this directory. Evidence
> + verdict stay; re-open needs a re-point ADR, not a silent re-run.

> **RETIRED 2026-07-10 (operator).** The manual TradingView rank-cert step (cfg01–11)
> that this harness gates on was never run, and the operator has retired the cert:
> the verdict stays **UNCERTIFIED** (ρ=0.714 on the 0.70 floor, N too small to certify),
> and the effort is not carried forward. The `pin, not remove` decision on
> `core/data/bar_data/GBPUSD_M15.csv` (SESSIONS 2026-06-11) is unaffected — other
> consumers may still read the feed; only this cert is retired. Re-opening requires a
> fresh operator decision, not a resumption of the parked manual step.

Executes the **candidate cert path** left open by SESSIONS.md 2026-06-07
("High-level code review + parity-gate / feed-soundness"): the ADR
`2026-06-05-sweep-engine` §4 pre-filter rank-correlation falsifier came back
**ρ=0.714 on the matched-feed window — ON the 0.70 floor, UNCERTIFIED** (2–6
trades/config made per-trade Sharpe a ddof artifact; TV's chart-OHLC export
bar-cap limits any matched-feed window to ~weeks).

## Design

| Tier | Source | Window |
|------|--------|--------|
| Native | TV Strategy Tester (NOT bar-capped), OANDA chart, UTC TZ | 2018-01-01 → 2024-01-01 (baked) |
| Python | `core/data/bar_data/GBPUSD_M15.csv` (OANDA REST, 149,293 bars) | whole feed (ends 2023-12-29) |

**Cross-feed by design.** Exact anchor parity is unattainable cross-feed
(symmetric-gross-drop fingerprint, memory `parity_gate_feed_and_pf_calibration`);
the §4 falsifier needs config *ordering* only, and rank-ρ is robust to a
roughly-uniform feed offset. The cross-feed anchor comparison is reported
**informationally** in the verdict JSON.

**n=12, seed=0** (the `parity_run` CLI default): under H0 the one-sided 5%
critical value for Spearman ρ is ≈0.829 at n=6 (above the 0.70 floor → a pass
is noise-indistinguishable) but ≈0.50 at n=12 (below it → the floor
discriminates). cfg00–05 are byte-identical to the prior matched-window
runbook sample (deterministic-prefix property of `make_config_sample`,
asserted at runtime), so the existing full-window cfg00 native export
(894 trades, 2026-06-06) seeds the new sample's anchor unchanged.

**ρ-stability diagnostics** (disposition inputs, NOT gates — no new threshold
has authority): leave-one-out ρ range, time-split halves (2021-01-01), the
net-profit score axis, py-score ties, per-config trade floors. The
pre-registered floor `PREFILTER_RANK_RHO_FLOOR = 0.70` is consumed verbatim.

**Scope guard:** certifies/revokes the pre-filter's ADR §4 rank authority
ONLY. `runner.run_sweep`'s `_emit_guard` still hard-requires same-feed anchor
parity for authoritative trial-set emits — untouched.

## State (2026-06-10)

- `prepare` run: python side staged (`py_scores.json`, 12 configs, 39–892
  trades/config — no ties, score spread −0.128 → +0.191 Sharpe), 11 baked
  paste-and-run `.pine` files + `RANK_CERT_RUNBOOK.md` written to
  `core/data/tv_exports/candidates/concept-gbpusd-vbr-001/full_2018_2024/`
  (gitignored, main checkout), cfg00 anchor seeded from the 2026-06-06 export.
- `verdict` smoke: **PENDING** (1/12 paired); cross-feed anchor info reproduces
  the known 892-vs-894 / net-137% / PF-1.7% characterization exactly.
- **Manual step (Joshua):** run cfg01–11 per the runbook (paste each baked
  pine — all inputs baked, change nothing), export each List of Trades CSV,
  then re-run `verdict`. Partial progress works (≥2 pairs → a ρ; full 12 for
  the discriminating read).

Control tests: `python -m pytest lab/analysis/gbpusd_rank_cert/test_rank_cert.py`
(bake self-verification, half-split scoring, unrankable-exclusion guards).
