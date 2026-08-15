# Q-FUNNEL-1 — CLOSURE: `RESOLVED` (funnel EV varies materially, but half the evidence is horizon-fragile)

**Closed:** 2026-07-22
**Parent brief:** [`../rnd-pipeline/Q-FUNNEL-1-contract-funnel-ev-scoping.md`](../rnd-pipeline/Q-FUNNEL-1-contract-funnel-ev-scoping.md) (now `CLOSED-RESOLVED`)
**Pre-reg (FROZEN before any run):** [`../pre-registration/Q-FUNNEL-1-verdict-preregistration.md`](../pre-registration/Q-FUNNEL-1-verdict-preregistration.md) — commit `b430a59`
**Cursor handoff (executed as specified):** [`../handoffs/2026-07-21-cursor-handoff-q-funnel-1-funnel-wrapper.md`](../handoffs/2026-07-21-cursor-handoff-q-funnel-1-funnel-wrapper.md) — commit `044cec5`
**Run artifacts:** [`lab/archive/q_funnel_1_2026-07/`](../../../lab/archive/q_funnel_1_2026-07/) — `funnel.py`, `run_funnel_sweep.py`, `RESULTS.md`, `sweep_results.json`, `test_funnel.py` (anchor `b4520b3`, PR #471, merged `1814edc`)
**Adjudication:** fable-judge pass this session — `VERIFIED WITH CAVEATS`, no frauds, diff scope exactly `lab/archive/q_funnel_1_2026-07/**` (`core/` diff = 0 lines), all four frozen docs byte-identical to their freeze commits, `check_boundaries` clean, audit greps clean. Judge's own independent wrapper-path check: 999/1000 lineages pass at 0.50× full-panel (0.10% bust vs ratified 0.08%) — no wrapper-level defect in the eval-path mechanics.
**Execution invariants held:** zero `core/` edits; zero `register_search open`; `K=0` throughout (contract-state-conditioned, not market-data); no rail/account/lifecycle touch.

## Verdict (§6 asserted against actual numbers)

**`RESOLVED`** — per the pre-registration's mechanical gate, EV/day varies materially (§3(a) ≥25% relative lift, §3(b) non-overlapping bootstrap bands, §3(c) same-sign across H1/H2) at 4 of the 6 (edge, retry-policy) grid points, all favoring the **1.00×** rung over 0.25×/0.50× — i.e., at the delivered `FUNDED_HORIZON_DAYS=252` config, funnel-EV strictly prefers running the book at full authorization over the ratified WATCH-1 0.50× haircut. The remaining 2 points (`edge_0`, both retry policies) landed `AMBIGUOUS-HOLD` (direction reverses H1↔H2) — expected, since `edge_0`'s per-leg de-meaning does not fully zero H2's residual drift (adjudication caveat, not a defect).

| Edge scenario | Retry policy | Trigger | Better rung | H1 lift | H2 lift |
|---|---|---|---|---:|---:|
| `edge_panel_historical` | no_retry | RESOLVED | 1.00× | +923.3% | +309.7% |
| `edge_panel_historical` | retry_to_cap | RESOLVED | 1.00× | +1016.8% | +275.6% |
| `edge_half_panel` | no_retry | RESOLVED | 1.00× | +405.4% | +379.5% |
| `edge_half_panel` | retry_to_cap | RESOLVED | 1.00× | +471.9% | +368.2% |
| `edge_0` | no_retry | AMBIGUOUS-HOLD | reverses | 0.25× better | 1.00× better |
| `edge_0` | retry_to_cap | AMBIGUOUS-HOLD | reverses | 0.25× better | 1.00× better |

## Load-bearing caveat this closure adds — the four RESOLVED points are not equally reliable

`FUNDED_HORIZON_DAYS=252` was a free parameter the delivered work fixed in code without disclosing in `RESULTS.md` or bouncing as a §0.5 question (adjudication finding). Post-merge, a sensitivity sweep at `FUNDED_HORIZON_DAYS ∈ {126, 252, 504}` on all four RESOLVED trigger points (300 lineages/cell, same `funnel.py` mechanics, no reimplementation) found the verdict splits into two reliability classes:

- **`edge_panel_historical` (both retry policies) — horizon-robust.** 1.00× beats 0.25× at every tested horizon in both regime halves. Lift magnitude swings widely (H1: +171%→+859%→+334% across 126/252/504) but the **direction never flips**. This is the trustworthy half of the RESOLVED verdict.
- **`edge_half_panel` (both retry policies) — horizon-fragile.** At 252 (delivered) and 504, 1.00× wins both halves. **At 126, H1 reverses sign** (lift −149%/−130%, bands still non-overlapping — a confident reversal, not noise). Had the undisclosed default been 126 instead of 252, these two trigger points would have moved from RESOLVED to AMBIGUOUS-HOLD.

**Net effect on the verdict: RESOLVED still stands**, because the gate only requires ≥1 robust trigger point and `edge_panel_historical` clears it at every horizon tested — but this closure explicitly does not claim the verdict is uniformly robust. Half its supporting evidence (`edge_half_panel`) is contingent on an arbitrary 1-year funded-continuation assumption that was never pre-registered.

## What the pre-registration predicted vs what actually happened

The pre-registration (§2) fixed the formula shape and the accept/reject thresholds without predicting a direction — it was genuinely agnostic on whether flat WATCH-1 0.50× sizing was already near-funnel-optimal (the null the design doc flagged as a live possibility, citing the Boyd-group result that fractional-Kelly haircuts are often already near-optimal for drawdown control). The actual result is a clear rejection of that null in the two robust grid points: **funnel-EV strongly prefers 1.00× over the ratified bust/pass-optimized 0.50× rung**, because at $328/reset the eval-fee cost of busting more often is cheap relative to the funded-payout upside forfeited by under-sizing. This is the retry-EV question named-and-deferred four times since 2026-07-11 (`tradeify_futures3_remc`, Bulenox C5, `tradeify_selectflex_remc`, the survivor-scoring-and-ddp-reframe recommendation's §3.4) — now quantified, not merely flagged.

**This does not mean 1.00× should replace WATCH-1 0.50× today.** The two objectives are genuinely different: WATCH-1 0.50× was ratified against the survivor-scoring bust≤3%/pass≥50% gate (a P(pass) objective), and 1.00× fails that gate decisively (H1 bust 4.37%, bootstrap-95th bust 10.37%, both well over the 3% ceiling). Q-FUNNEL-1 answers a different question — EV-per-dollar-day inclusive of resets and funded-phase payouts — and a real tension between the two objectives is exactly what this study was built to surface.

## Additional caveats (adjudication, not gate-affecting)

- **Floor lock-on-first-payout-request is not modeled** — the funded-phase continuation locks the floor only via the equity trigger, not the "or immediately on first payout request, whichever first" clause in the primary Tradeify source. Mildly optimistic in the narrow pre-lock payout window; does not affect which rung wins.
- **`edge_0` is not literally zero-edge in H2** — per-leg de-meaning uses the full-panel mean, so the H2 slice retains positive residual drift (visible as +4.48 EV/day at 1.00× in the delivered cell table). Harmless to the verdict (those cells are the AMBIGUOUS ones already), but the finding must never be quoted as "contract value at zero edge, H2."
- **Eval fee reused, not re-verified against live checkout pricing** — Q-RAIL-1 Phase 4's $328/$258-promo pin (2026-07-17) was used per the pre-registration's own explicit non-blocking allowance; not re-checked this session.

## Dispositions

- **Q-FUNNEL-1 CLOSED-RESOLVED.** The finding — funnel-EV materially prefers full authorization over the ratified bust/pass-optimized haircut, robustly on at least one edge-scenario axis — routes to the **2026-08-08 D1 packet** as a decision item: should the c1 book's rung selection weigh funnel-EV alongside (not instead of) the bust≤3% survivor-scoring floor? This is an operator/ADR-level question, not resolved here.
- **No change to live sizing.** WATCH-1 0.50× remains the GO-ADR-pinned, ratified configuration. Any rung change is a fresh operator ratification, a new `dd_geometry`-class admission (pre-registered re-MC + both-halves regime gate + admitting ADR per the concept-not-constant doctrine), and very likely a B6 dry-fire re-run — none of that is authorized or attempted by this closure.
- **The deferred policy layer (design doc §7)** — cushion-proportional day-policy, pass-banking, day-quit rules — now has a stronger GO case than before this study (funnel-EV shows real magnitude, not just theoretical possibility), but remains gated on a fresh operator decision and its own governance chain. Not opened here.
- **K-accounting:** zero K consumed or banked (contract-state-conditioned throughout).
- **Accept-idle intact for the discovery-manifest ledger:** `discovery_manifests/` count unchanged by this study.

## Lesson candidates

1. **Undisclosed free parameters in a frozen-spec build need their own pre-registration line, not a code default.** `FUNDED_HORIZON_DAYS=252` materially changed which trigger points were robust vs fragile, and it was never surfaced as a §0.5 question despite the handoff explicitly modeling §0.5 as the halt-on-ambiguity mechanism for exactly this class of decision. Candidate fix for future Cursor handoffs of this shape: require every numeric constant introduced during implementation (not present in the frozen pre-registration) to be logged in the closure report by name, even if the build never treats it as ambiguous. One incident; below the two-incident bar for promoting to a load-bearing methodology lesson — watch for a second instance before registering formally.
2. **A regression pin that reproduces via the same primitives the wrapper is supposed to test can look stronger than it is.** The delivered pin calls `run_class_s_c1_scoring`/`run_class_s_c1_regime_gate` directly rather than routing through `simulate_lineage`'s own eval-path sampling — technically faithful to the frozen spec's "regime-gate primitives, never reimplemented" instruction, but it leaves the wrapper's own bust/pass-detection path unpinned. This adjudication's independent 1000-lineage wrapper-path check closed the gap this time (999/1000 pass, 0.10% bust vs 0.08% ratified — consistent). Candidate future handoff language: the regression pin should exercise the actual code path under test, with a documented rationale if it deliberately doesn't.

## §10 audit-hook discharge (run this session)

- Pre-reg commit `b430a59` predates first analysis script run (`funnel.py`/`run_funnel_sweep.py` land at `b4520b3`, later) ✔
- `core/` diff across the full PR = 0 lines ✔
- No `register_search` anywhere in `lab/archive/q_funnel_1_2026-07/` ✔
- `MAX_RETRIES = 5` and `0.25` (materiality threshold) appear literally, not re-derived ✔
- Sibling-primitive imports present (`run_class_s_c1_scoring`, `run_class_s_c1_regime_gate`), no reimplementation ✔
- `check_boundaries.py`: clean, 25 first-party modules, no illegal edges ✔
- Frozen docs (design/scoping/pre-reg/handoff) byte-identical to their freeze commits at merge time ✔
