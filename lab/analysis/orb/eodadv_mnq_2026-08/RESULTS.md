**Theme:** orb
**Status:** ACTIVE — no pre-registered mechanism survives; 15:30 exit stays barred
# Q-EODADV-1 — RESULTS: **FALSIFIED**. No pre-registered mechanism survives; the 15:30 exit stays barred.

**Pre-registration:** [`Q-EODADV-1`](../../../docs/briefs/rnd-pipeline/Q-EODADV-1-mnq-final-half-hour-adversity-scoping.md), frozen `43cdde0` **before** this ran (§4 hypotheses, §6 gate, 60% channel threshold).
**Harness:** [`run_eodadv.py`](run_eodadv.py) — `orb_backtest` called verbatim; day mapping imported from the already-asserted `run_v02_native_clock_kgrid.trade_days`.
**Spend:** **$0.00 · K=0 · no manifest · no pull.** MNQ Cap seat **UNSPENT**.
**Provenance:** panel `81c05e9a…`, engine `dcfe83e1…`.

---

## Verdict — FALSIFIED

The dominant channel clears its threshold, but **its independent test fails**. Per the frozen §6,
that is FALSIFIED, not RESOLVED.

| | Result | Gate |
|---|---|---|
| Dominant channel | **stop-out, 76.3%** | ≥ 60% ✓ |
| Independent test for that channel (H-B, variance expansion) | **NOT CONFIRMED** (ratio 1.06×, z = +0.21) | needs elevated range ✗ |
| Independent test for H-A (directional reversal) | **NOT CONFIRMED** (corr +0.0127, NW t = +0.321) | needs significantly negative ✗ |

**Consequence: `ADR 2026-07-31 §5` stands unamended. The 15:30 exit remains barred.** No mechanism
was established, so there is no mechanism-derived exit time to license.

---

## Phase 1 — channel decomposition (common days n=1,841; 5 days exist only with the longer window)

| Component | n | contribution | share of adverse |
|---|---:|---:|---:|
| **control** — stopped in BOTH worlds | 660 | **+0.00000** | — (must be 0 ✓) |
| **(i) stop-out** — newly stopped 15:30→16:00 | 42 | **−0.01110** | **76.3%** |
| **(ii) give-back** — never stopped, closes worse | 1,139 | −0.00345 | 23.7% |
| residual — composition / 5 extra trades | 5 | −0.00062 | — |
| **sum** | | **−0.01517** | = `delta_total` exactly |

The control term is **identically zero** and the components sum to `delta_total` to five decimals —
the decomposition is exact, not approximate. Stop-out rate on common days: **35.850% → 38.131%
(+2.28pp)**, reproducing the ADR's published +2.1pp.

---

## Phase 2 — independent bar-level tests (raw panel only; **no ORB P&L enters this phase**)

**(a) Directional reversal — refuted.** `corr(r_10:00→15:30, r_15:30→16:00) = +0.0127` (n=1,791);
Newey-West(5) slope +0.00498, **t = +0.321**. Weakly *positive* and insignificant. This **replicates
the D5-RECOST OOS prior of +0.024** that §2 recorded *before* testing precisely so this could not be
reverse-fitted. The intuitive "the day's move reverses into the close" story is wrong on this
instrument.

**(b) Variance expansion — not supported.** Realized range per minute is a clean decaying U:
09:30 **3.575 bp** → midday trough ~**1.51–1.60** → 15:30 bar **1.776**, 15:45 bar **2.369**.
Final block mean **2.073 vs 1.961** for the rest (frozen comparator) — **1.06×, z = +0.21**.

*Design weakness, disclosed:* the frozen comparator includes the opening bars, which are the most
volatile of the session and inflate the baseline. Against the exposure-relevant window only
(10:00–15:15, the period the position actually exists), the final block is **1.12×** and the last
15-minute bar alone **1.28×**. **The verdict is robust to this weakness** — neither comparator shows
the elevation H-B requires.

---

## What actually produces the adversity (EXPLORATORY — post-verdict, NOT gate-bearing)

The gate has fired; this section is interpretation and is **not** promoted to a finding.

The final block is not anomalous in either pre-registered sense, and it is not even anomalous in
stop frequency:

| | |
|---|---:|
| Survivors at 15:30 | 1,181 (S = 0.6415) |
| Implied constant hazard, 10:00–15:30 | 0.001345 /min |
| **Expected** final-block stop rate under constant hazard | **3.96%** |
| **Observed** final-block stop rate | **3.56%** |

The final 30 minutes is **less** dangerous than a constant-hazard extrapolation predicts. What makes
it costly is the **payoff asymmetry**, not the hazard: a newly-stopped trade loses **−0.488 R**,
while a surviving trade gives back only **−0.0056 R**.

Combined with Phase 2a, this reads as **drift exhaustion against a constant hazard** — the ORB edge
is front-loaded in the session; by the final block the conditional drift is ~zero (that is exactly
what `corr ≈ +0.013` says), while the fixed stop keeps charging its normal hazard against a −1R
payoff. Net per-minute contribution goes negative. That explains the Q-SESSCONF-1 ladder's
rise-then-drop shape **without any end-of-day market mechanism at all**, and it re-reads Phase 2a's
null as the *affirmative* explanation rather than merely a failed test.

**This is a third mechanism and it was NOT pre-registered.** Promoting it to "confirmed" here would
be the exact rationalized-overlay failure this brief exists to prevent. It is recorded as a
**candidate for a future pre-registration**, needing its own independent test.

**Even sympathetically read, it does not hand back the 15:30 exit.** "Exit when drift is exhausted"
does not locate 15:30 — finding that point is itself a search, with the K cost that implies.

---

## Disposition

- **Q-EODADV-1: FALSIFIED.** No pre-registered mechanism established.
- **The 15:30 exit stays barred**; ADR 2026-07-31 §5 unamended; D5 and the 16:00 clock stand.
- **The give-back is real and mechanism-less** — strengthening MNQ.md **N3**'s "real but unharvestable."
- **§8 operator rulings do not arise** (they were conditional on RESOLVED). Cap seat **UNSPENT**.

Reproduce:

```bash
/c/Users/joshu/multi_firm_operations/.venv-research/Scripts/python.exe \
  lab/analysis/eodadv_mnq_2026-08/run_eodadv.py
```
