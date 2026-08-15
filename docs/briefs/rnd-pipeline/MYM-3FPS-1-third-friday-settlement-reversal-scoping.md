# Scoping — MYM-3FPS-1: third-Friday derivative-settlement reversal

**Status:** `CLOSED — FALSIFIED at Phase-0 2026-07-21`
**Authored:** 2026-07-21
**Authors:** Joshua + Cursor
**Loop:** Inquire-phase Pre-Q; a K=0 native-MYM delta extraction gates any campaign.
**Pre-registration:** [`MYM-3FPS-1-verdict-preregistration.md`](../pre-registration/MYM-3FPS-1-verdict-preregistration.md)
**Results:** [`lab/archive/mym_3fps_recon_2026-07/RESULTS.md`](../../../lab/archive/mym_3fps_recon_2026-07/RESULTS.md) — coverage passed; both mechanism/power gates and the cost-law gate failed. K=0.

## §0 — Rule 0 reads

Read before authoring, verified 2026-07-21:

- [`docs/rejected_candidates.md`](../../rejected_candidates.md) — `910dbe3` (2026-07-21): no Terstegge, 3FPS, derivative-payoff-bias, or open-to-noon settlement-reversal entry. The nearest third-Friday work tested locked-Striker/ORB calendar cells, not this trade.
- [`docs/methodology/strategy_harvest.md`](../../methodology/strategy_harvest.md) — `268851b` (2026-07-16): all five admission requirements bind; monthly bp-scale mechanisms are presumptively power-dead, so Phase 0 must measure Requirement 4 before K spend.
- [`ops/prop_envelope_default.md`](../../../ops/prop_envelope_default.md) — `7af4224` (2026-07-20): E1 requires flat by 16:00 ET; the 09:30→12:00 construct is compatible.
- [`core/firm_rules.py`](../../../core/firm_rules.py) — `a53ee99` (2026-07-13): current deployment target uses the Tradeify commission row; MFFU is co-reported as sensitivity.
- [`lab/archive/xindex_rv_recon_2026-07/run_probe.py`](../../../lab/archive/xindex_rv_recon_2026-07/run_probe.py) — `82e338e` (2026-07-21): cached MYM/MNQ bar paths referenced by prior work are absent in this checkout, so a cost-estimated native-MYM pull is required.
- [`lab/archive/ng_eia_recon_2026-07/run_phase0.py`](../../../lab/archive/ng_eia_recon_2026-07/run_phase0.py) — fixed-event K=0 extraction precedent: own-cohort delta, power, cost law, and non-gating diagnostics.

External source: Baltussen, Terstegge, and Whelan, *The Derivative Payoff Bias* ([SSRN 4562800](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4562800); AFA manuscript). It reports approximately +12 bp DJIA overnight into third-Friday a.m. settlement followed by a comparable reversal by noon. The paper attributes the spike to expiry-related market-maker charm/inventory hedging. The published NQ/YM rows do not provide target-cohort sigma or native-micro costs.

## §1 — Context and pre-Q gate

The c1 prop book is two equity-index trend/pyramid legs at WATCH-1. A sparse, scheduled reversal could add mechanism breadth without creating another ordinary-day trend strategy, but monthly frequency makes confirmation power the likely falsifier.

Pre-Q gate:

- **D:** Exclude the overnight long limb, MNQ, quarterly-only filtering, alternative entry/exit clocks, and the five-index CO-OC candidate. Test: outside the authorized MYM-only, intraday-flat, single-expression scope.
- **S:** Reduce each expiry event to three prices: Thursday 15:59 close, Friday 09:30 open, Friday 12:00 open.
- **A:** Deterministic third-Friday calendar plus machine-readable event/metric outputs makes every later gate replayable.

## §2 — Seed manifest

- **Requirement 1:** path 1a, provisional PASS. Forced a.m.-settlement hedging demand pushes the index into the open; the pressure disappears after settlement and reverses.
- **Requirement 2:** UNSCREENABLE before Phase 0. Published target delta is about 12 bp for DJIA, but target sigma is absent. Native MYM extraction supplies both.
- **Requirement 3:** MYM family bank is 0; Phase 0 consumes K=0. Any later campaign would declare one fixed expression at K_intrinsic=1.
- **Requirement 4:** 87 calendar events exist from 2019-05-06 through the latest included event on 2026-07-17; the break-even `delta/sigma = 1.96/sqrt(N)` is approximately 0.210 before missing-event attrition.
- **Requirement 5:** at an illustrative 40,000 MYM price, one tick of slippage each side plus Tradeify commission gives approximately 1.41 bp round trip and a 5.64 bp 4× hurdle. The published 12 bp effect is arithmetically reachable, not evidence that the native cohort passes.
- **Dedup:** CLEAR. Q-MECH-1 DJ30 third-Friday cells and Q-ORB-FRIDAY tested different strategies and did not enter at settlement to short through noon.
- **Screen status:** UNSCREENABLE pending this K=0 extraction.

## §3 — Question

**Q-MYM-3FPS-1:** Does the published third-Friday settlement-flow reversal exist on native MYM with enough power and post-cost magnitude to justify a K-bearing confirmation campaign?

## §4 — Falsifiable hypothesis

**H-MYM-3FPS-1:** If native MYM third Fridays show both a positive, powered Thursday-close→Friday-open spike and a positive, powered 09:30→12:00 short reversal, and the reversal is at least 4× the Tradeify round-trip hurdle, then the candidate may advance to separately frozen confirmation; otherwise the construct closes FALSIFIED. If fewer than 90% of calendar events have exact checkpoints, close AMBIGUOUS without reading a return verdict.

## §5 — Forbidden moves

- **No timing search:** 09:30 entry and 12:00 exit are copied from the source mechanism. A 09:15/09:20 or close exit is a new hypothesis.
- **No quarterly/triple-witch rescue:** selecting the stronger expiry subtype after a monthly failure adds K and destroys the stated power basis.
- **No MNQ rescue or pooling:** NQ has a different family bank and volatility; it cannot rescue a MYM failure.
- **No absolute-value gate:** the published direction is short after settlement. A large wrong-sign result is FALSIFIED.
- **No overnight deployment limb:** c1 must remain intraday flat; the overnight move is a mechanism-faithfulness measurement only.
- **No campaign on Phase-0 PASS:** PASS licenses a new pre-registration and operator GO, not Pine, rail, allocation, lifecycle, or live trading.
- **No approximate timestamps:** the event is defined by settlement time. Missing exact 15:59/09:30/12:00 bars are missing events, not nearest-bar substitutions.

## §6 — Gate criteria

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` | coverage ≥90%; overnight mean >0 and `delta/sigma ≥ 1.96/sqrt(N)`; short-reversal mean >0 and same power floor; short-reversal mean ≥4× Tradeify RT cost | Author a separate K=1 confirmation pre-registration; fresh operator GO required |
| `FALSIFIED` | coverage passes but any mechanism, power, direction, or cost gate fails | Close and add the measured construct to `docs/rejected_candidates.md`; MYM K bank remains 0 |
| `AMBIGUOUS` | exact-checkpoint coverage <90% | Diagnose data/contract-calendar coverage; no threshold or nearest-bar repair in place |

## §7 — Execution protocol

1. Freeze this brief, the companion pre-registration, the runner, and unit tests in a commit before reading MYM returns.
2. Run the mandatory Databento estimate for `MYM.v.0`, continuous `ohlcv-1m`, 2019-05-06→2026-07-21 exclusive. Pull only if the estimate is within the authorized minimal-data scope. The cap was narrowed pre-pull from July 22 after the metadata range gate reported July 21 23:30 UTC as the latest available bar; the 87-event set is unchanged.
3. Execute the frozen runner once. It emits `primary_events.csv`, `phase0_results.json`, and `RESULTS.md`.
4. Apply §6 without modification. On FALSIFIED, update the rejection registry and session log; on RESOLVED, stop before any K-bearing work.

## §8 — Operator GO

```
PHASE-0 GO: 2026-07-21 / Joshua (chat: "proceed")
Authorizes: MYM-only K=0 delta extraction, mandatory cost estimate, minimal native
            ohlcv-1m pull, frozen 09:30->12:00 construct, and closure artifacts.
Does not authorize: register_search, K spend, MNQ/ES/RTY variants, Pine, rail,
                    account changes, allocation, lifecycle promotion, or live trading.
```

## §10 — Audit hooks

```bash
# Freeze-before-result ordering.
git log --format='%h %ci %s' -- \
  docs/briefs/pre-registration/MYM-3FPS-1-verdict-preregistration.md \
  lab/archive/mym_3fps_recon_2026-07/run_phase0.py \
  lab/archive/mym_3fps_recon_2026-07/RESULTS.md

# Exactly one direction and one time window.
rg -n "09:30|12:00|short_reversal" lab/archive/mym_3fps_recon_2026-07/run_phase0.py

# No K-bearing manifest may be opened by Phase 0.
rg -n "mym.*3fps|3fps.*mym" discovery_manifests/ || echo "K=0 confirmed"

# Reproduce after the DBN cache path is recorded in RESULTS.
PYTHONPATH=lab python3 lab/archive/mym_3fps_recon_2026-07/run_phase0.py --dbn <cache.dbn>
```

## Verification

```bash
python3 .claude/skills/brief-authoring/scripts/check_brief.py \
  docs/briefs/rnd-pipeline/MYM-3FPS-1-third-friday-settlement-reversal-scoping.md \
  --type inquire
pytest -q lab/archive/mym_3fps_recon_2026-07/test_run_phase0.py
git log -1 --format='%h %cI' -- docs/rejected_candidates.md
git log -1 --format='%h %cI' -- docs/methodology/strategy_harvest.md
```
