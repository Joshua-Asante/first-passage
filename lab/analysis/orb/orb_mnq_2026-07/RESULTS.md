**Theme:** orb
**Status:** ACTIVE — NAS100-ORB-30 on native MNQ; Stage-2 cost-law PASS then T2 payability FIRED
# ORB-MNQ-1 Stage-2 RESULTS — NAS100-ORB-30 on native MNQ

**Campaign:** `orb_mnq_intraday_breakout` (manifest [`discovery_manifests/orb_mnq_intraday_breakout.json`](../../../discovery_manifests/orb_mnq_intraday_breakout.json), `open` 2026-07-16, mechanism-first, K_intrinsic=1, K_eff=2)
**Pre-reg:** [`docs/briefs/pre-registration/2026-07-16-orb-nas100-mnq-reconstruction-preregistration.md`](../../../docs/briefs/pre-registration/2026-07-16-orb-nas100-mnq-reconstruction-preregistration.md) (§8 GO signed 2026-07-16/JA)
**Harness:** [`run_stage2.py`](run_stage2.py) (reuses `orb_universe_2026-06-22/orb_lib.py` engine verbatim) · [`run_placebo.py`](run_placebo.py)
**Data:** native `MNQ.v.0` continuous 1m (D5 Stage-1 pull, $0.00 re-decode), 2019-05-06→2026-07-15, resampled to 15m ET.

---

## Verdict — Stage-2 cost-law **PASS** (first pass in the current pipeline)

D5 and H-OD-1 both died at this exact gate. ORB-MNQ-1 clears it with margin, and the
within-day placebo confirms the opening range is structurally special on native futures.

| Metric (full confirm panel 2019-05-06→present) | Value |
|---|---|
| RTH session-days / entries | 1,857 / **1,846** (99.4% entry rate — matches N1's ~100%) |
| Median OR range | 90.8 index pt |
| Mean **gross** edge | **+0.0823 R** (t **+2.97**) |
| Mean cost_R (rt=1.11 pt / OR range) | 0.0155 R |
| 4× cost hurdle | 0.0620 R |
| **edge / cost ratio** | **5.31×** (PASS iff ≥ 4.0×) |
| Net-of-cost meanR | +0.0668 R (t +2.41) · WR 0.464 · PF 1.151 |

| 2021+ regime window (§3 override) | Value |
|---|---|
| n | 1,420 |
| Mean gross edge | **+0.1020 R** (t +3.21) |
| **edge / cost ratio** | **8.10×** |
| Net-of-cost meanR | +0.0894 R (t +2.81) · WR 0.473 · PF 1.207 |

**Within-day OR-window placebo (2021+, n=1,420, 1,000 perms):** **p = 0.0040** — the opening
range is structurally special vs arbitrary intraday windows (arbitrary-window placebo mean
+0.0029, p95 +0.0532; observed +0.0894 sits far above). parity_ok=True.

---

## The load-bearing finding — the mechanism TRANSFERRED where locked-Pine did not

The native-MNQ numbers reproduce the CFD anchor (N1, `ops/instruments/NAS100.md`) almost exactly:

| | N1 (Pepperstone CFD, 2020-26) | ORB-MNQ-1 (native MNQ, 2019-26) |
|---|---|---|
| gross meanR | +0.0872 R (t 2.94, n 1663) | **+0.0823 R (t 2.97, n 1846)** |
| within-day placebo | p 0.014 | **p 0.0040** |
| long / short | +0.102 / +0.070 | **+0.070 / +0.063** (both positive) |
| entry rate | ~100% | 99.4% |

This is the **opposite** of R5 (Striker DJ30→MYM PF-ratio 0.559, edge did not transfer) and P2
(NAS100→MNQ K2-kill). The ORB mechanism survives the CFD→native-futures venue shift because it
is cost-cheap by construction (OR-range/spread ≈ 77:1, the fill-cliff headroom N1 measured) and
intraday-complete (exit-at-close, no force-flat truncation, no overnight roll-seam exposure) —
exactly the surviving-band properties that made it the pre-registered candidate.

## Regime split faithfully reproduces N2 (per-year net meanR, full window)

```
2019 +0.0224   2020 -0.0285   2021 +0.0634   2022 +0.1017
2023 +0.0999   2024 +0.1661   2025 +0.0687   2026 -0.0118 (partial yr)
```

Dead pre-2021, strongly positive 2021-2025 (incl. the 2022 bear), 2026-partial marginally
negative. This is N2 exactly — and it is why §3 pre-registered the 2021+ temporal-consistency
override (the 2019/2020 sub-eras are known-adverse for a documented, dated reason, not a sign the
mechanism is false). The per-window Stage-2 confirms it mechanically: 2019 and 2020 individually
**KILL** the cost-law (ratio 1.60× / −0.64×); 2021+ **passes at 8.10×**.

---

## What this is NOT (honest scope)

- **Stage-2 PASS is not the campaign verdict.** The frozen §6 RESOLVED gate is Stage-6:
  net-of-cost annualized Sharpe ≥ 0.85 (DSR ≥ 0.95 at K_eff=2, V=1/n) + the temporal-consistency
  battery + the placebo battery, **not yet run**. Stage-2 is the hard *kill* gate; clearing it
  licenses Stages 5/6/7/8, nothing more.
- **Indicative Stage-6 preview (NOT the adjudicated DSR gate):** rough annualized net Sharpe
  ≈ **0.90 full window / ≈ 1.20 on 2021+** (from t/√n × √trades-per-yr). The full-window ~0.90 is
  only *marginally* above the 0.85 floor and will deflate somewhat under the real DSR(K_eff=2,
  V=1/n) computation — genuinely borderline. The 2021+ window (~1.20) is where it has cushion,
  which is the whole point of the §3 override. **Do not quote 0.90/1.20 as a pass.**
- **Realism (Stage 7) unchecked:** integer micro-contract sizing at the $100K prop tiers and the
  native fill re-parameterization are not yet run; force-flat (E1) is trivially satisfied by
  exit-at-close.
- **Still a transfer at heart:** the bar-level economics now *confirm* on native MNQ (unlike
  R5/P2), but live exchange fill quality (stop/limit fills vs a CFD desk quote) is a separate
  future question — the construct is the reliable-offline class (touch-fill preserved, no
  give-back exit — the N5/N7 fragility does not apply), so the offline number is trustworthy as
  far as offline goes.

## Faithfulness notes

- **Engine reused verbatim** — `orb_lib.orb_backtest` / `session_panel` / `placebo_within_day`
  (the calibrated CFD harness), not reimplemented. Only the loader is new (databento 1m → 15m ET).
- **ts_event = bar-open** verified empirically (09:30 bar opens at the cash open, volume spikes
  there); `resample(label='left', closed='left')` preserves it.
- **RTH session count 1,857** is the correct trading-day count (no weekends; ~257/yr; 66 thin
  holiday half-days). The "2,243" printed as `df['d'].nunique()` is all-calendar-dates-with-any-bar
  (Sunday Globex + overnight) and is not used by the ORB — `session_panel` correctly filters to
  09:30-15:45 ET.
- MNQ economics: Bulenox $0.61/side + 1-tick ($0.50) slip → RT $2.22 → 1.11 index pt (frozen §R.1).

## Disposition

- **Stage-2:** PASS (full 5.31×, 2021+ 8.10×) + within-day placebo p=0.0040.
- **Stage-5/6:** **RESOLVED** per the frozen gate — see [`RESULTS_stage6.md`](RESULTS_stage6.md).
  DSR full-window 0.9754 + annSR +0.890 (both clear); temporal battery (2021+) PASS; placebo PASS.
  **But marginal + cost-fragile + Bulenox-specific:** a 1.25× RT cost flips the full-window gate to
  FAIL, so the three costlier FRIENDLY firms likely fail the full window (2021+ has cushion). Also a
  confirmation of a *pre-selected* CFD construct (K=2 deflates the MNQ-family K, not the CFD search),
  6a exactly at threshold with 2026-partial the watch item. Not a deployment authorization.
- **Stage-7 realism:** mapped at all four firms + slip stress — see [`RESULTS_stage7.md`](RESULTS_stage7.md).
  **Edge survives all four FRIENDLY firms on the 2021+ regime** (up to 3-tick slip, DSR ≥0.97);
  **full-window survival is Bulenox-and-≤1-tick-specific**. Sign-limb cost-robust.
- **Stage-8 breadth (vs prop-portfolio book):** structural read [`RESULTS_stage8.md`](RESULTS_stage8.md);
  **realized N_eff (legs procured) [`RESULTS_stage8_neff.md`](RESULTS_stage8_neff.md) — CORRECTS the
  structural claim.** Measured weekly corr(ORB, same-instrument MNQ-Striker) = **+0.15**; dependence
  N_eff **1.99→2.95** (near-independent bet — belt finding confirmed) → ORB **is NOT instrument-
  concentrating** (my pre-data hypothesis was wrong on the correlation axis). The concentration is
  narrower: **regime-common-mode** (dead 2020, the chop the book busts in) **+ high-variance/risk-
  dominant** (weekly $ vol ~2× each book leg). Net: adds correlation breadth, not a risk/regime
  diversifier.
- **Campaign status: confirm gates CLEARED (Stage 2/5/6/7); Stage-8 flags instrument+regime
  concentration.** Net = a real edge, admissible as lifecycle CANDIDATE **with a standing
  breadth/concentration caveat** (symmetric to the Class-S book's own regime-fragile caveat), NOT a
  portfolio diversifier. Manifest stays **open**; lifecycle admission + rail/account/live-spend
  separately gated; regime-dependence (2021+ carries it, 2026-partial the tripwire) is the dominant
  standing risk.

Reproduce:

```bash
PYTHONPATH=lab .venv-research/Scripts/python.exe lab/analysis/orb_mnq_2026-07/run_stage2.py
PYTHONPATH=lab .venv-research/Scripts/python.exe lab/analysis/orb_mnq_2026-07/run_placebo.py
```
