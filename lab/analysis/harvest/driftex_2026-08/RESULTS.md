**Theme:** harvest
**Status:** ACTIVE — drift exhaustion falsified; phenomenon is equity-index-specific
# Q-DRIFTEX-1 — RESULTS: **FALSIFIED**. Drift exhaustion is not the mechanism; the phenomenon is equity-index-specific.

> ⚠ **The headline cliff does NOT survive multiplicity — read [Addendum 2026-08-01] before citing
> any figure below.** The published figure is corrected there and the successor question is
> **withdrawn**. Body unedited (Trap #12); this banner is the reader-intercept
> (operational_rules.md Rule 14).

**Pre-registration:** [`2026-08-01-drift-exhaustion-mechanism-preregistration.md`](../../../docs/briefs/pre-registration/2026-08-01-drift-exhaustion-mechanism-preregistration.md), frozen `26cad59` **before** any phase ran.
**Harnesses:** [`run_phase123_freeze_tstar.py`](run_phase123_freeze_tstar.py) → [`TSTAR_FROZEN.json`](TSTAR_FROZEN.json) → [`run_phase456_ladder_verdict.py`](run_phase456_ladder_verdict.py) · [`run_phase5_scope_probes.py`](run_phase5_scope_probes.py)
**Spend:** **$0.00 · K=0 · no manifest · no pull.** MNQ Cap seat **UNSPENT**.
**Provenance:** MYM panel sha256 `24e169528f7ea6693b75c71c3195edf6`, span 2020-07-02 → 2026-07-02, 1,548 days / 1,538 breakout days. Engine `dcfe83e1…`. MYM cost: $0.50/pt, 1 tick = 1.0 pt ⇒ Tradeify `rt_pt` 5.64.

**Order-of-operations honoured.** `t*` was computed and written to `TSTAR_FROZEN.json` by the Phase-0–3
script; the Phase-4 script **reads** that file and never recomputes it. The two ran as separate
invocations, so the §4 "single-pass artifact is void" clause is satisfied.

---

## Verdict — FALSIFIED

| Limb | Result | Gate |
|---|---|---|
| **L1** drift decay on MYM | NW(5) slope **−7.015e-05/min, t = −2.522** | t < −1.96 ✓ **PASS** |
| **L2** flat hazard on MYM | expected 4.07% vs observed **3.91%**, dev **−3.9%** | \|dev\| ≤ 25% ✓ **PASS** |
| signal-sufficiency guard | lift **+0.1014** | ≥ 0.10 ✓ **PASS** (by 0.0014) |
| **P3** `t*` locates the turnover | **\|t\* − argmax\| = 719.5 min** | ≤ 45 min ✗ **FAIL** |

Two limbs replicated out-of-sample and the conjunction still failed — by **16×** the tolerance, not
narrowly.

**Why P3 failed: `t*` is degenerate.** `drift_hat(t) = +0.05437 − 7.015e-05·t` against a
hazard-per-block of 0.04066 solves to **t\* = 195.5 min = 03:15 ET** — *before the session opens*. At
the session's own start (10:00) fitted drift is already 0.0123 against a 0.0407 hazard cost. The
mechanism's own arithmetic, calibrated on MYM, says **no holding horizon on MYM is ever net-positive**
— which is consistent with MYM opening-range-continuation being DEAD, but it means the model never
produces the interior crossing §2 claims.

---

## Phase 4 — MYM exit-time ladder

| close_tod | n | best annSR | | close_tod | n | best annSR |
|---|---:|---:|---|---|---:|---:|
| 10:45 | 1370 | −0.573 | | 13:45 | 1515 | −0.332 |
| 11:00 | 1411 | −0.726 | | 14:15 | 1527 | −0.154 |
| 11:15 | 1441 | −0.593 | | 14:45 | 1533 | −0.153 |
| 11:45 | 1476 | −0.445 | | **15:15** | 1536 | **+0.001** ← argmax |
| 12:15 | 1490 | −0.450 | | 15:45 | 1538 | −0.101 ← full session |
| 12:45 | 1499 | −0.383 | | | | |
| 13:15 | 1510 | −0.289 | | | | |

**Two findings here, and the second is the important one.**

1. **The signal guard passed by 0.0014 and the verdict hinges on it.** Had lift been 0.0986 instead
   of 0.1014, the verdict would have been AMBIGUOUS-HOLD. **Disclosed design weakness:** the guard was
   written in terms of *lift* (max − full-session) but not *positivity*. MYM ORB is **negative at every
   horizon** except a single cell at +0.001, so "sufficient signal" here means *least-bad*, not real
   edge. A better guard would have required the ladder max to be positive. The frozen gate is applied
   as written — FALSIFIED — but a reader should know the AMBIGUOUS branch was one basis point away.
2. **MYM's argmax is 15:15 — the same cell as MNQ's.** The final 30 minutes is adverse on *both*
   index futures. **The phenomenon replicates out-of-sample even though the mechanism does not.**

---

## Phase 5 — cross-asset scope probes (NON-GATING, and they are the most informative result)

| Instrument | breakout days | NW(5) drift slope t | final block 15:30–16:00 driftR |
|---|---:|---:|---:|
| MNQ (generating) | 1,846 | — | strongly adverse |
| **MYM** (confirmatory) | 1,538 | **−2.522** | **−0.02999** |
| XAUUSD | 1,648 | +0.144 | **+0.00003** |
| 6J | 1,509 | −0.565 | **+0.00546** |

**The final-block cliff is equity-index-specific.** It is large and negative on both MNQ and MYM, and
absent on gold and JPY futures — where the same window shows nil-to-mildly-positive drift and no
significant decay. This is non-gating by pre-registration, and it points somewhere: a *general*
position-geometry property (drift decaying against a flat hazard) should not care what the underlying
is. An effect that appears only on US equity indices, only in the last half hour, is far more
consistent with something tied to the **16:00 ET cash close** — closing-auction imbalance, index
rebalancing, cash-futures convergence — than with the geometry story this brief pre-registered.

*Caveat as frozen:* the 09:30–16:00 window is an equity-cash construct, so its use on XAUUSD/6J is
arbitrary by design and these probes are weak evidence individually. Their agreement with each other,
and their contrast with both index futures, is what carries the reading.

---

## Disclosed weaknesses in the frozen design

- **L1's proxy does not test what §2 claims.** §2 asserts drift *"declines monotonically"*; the frozen
  limb tests a **linear slope**. MYM's actual profile is noise around zero (+0.0156, −0.0067, +0.0057,
  −0.0014, +0.0028, +0.0047, +0.0074, +0.0090, −0.0053, −0.0056) followed by a **cliff** at −0.02999.
  A single terminal block drives much of the significant slope. L1 "passed" on a statistic that a
  cliff satisfies just as well as a decay — arguably better.
- **The signal guard measured lift, not edge** (above).
- Both are recorded rather than repaired: amending a frozen gate after seeing results is Trap #12.

---

## Disposition

- **Q-DRIFTEX-1: FALSIFIED.** Drift exhaustion against a constant hazard is **not** the mechanism.
- **The 15:30 exit stays barred.** ADR 2026-07-31 §5 unamended; D5 and the 16:00 clock stand.
- **The give-back is now mechanism-less after TWO pre-registered attempts** (Q-EODADV-1, Q-DRIFTEX-1),
  further strengthening MNQ.md **N3**'s *"real but unharvestable."*
- **What survives as a live question:** the final-block cliff is **real, cross-index, and
  equity-specific**. Any successor must pre-register an *equity-close-flow* mechanism and test it on
  evidence neither of these two studies used. It does not license an exit change on its own.
- **MNQ Cap seat UNSPENT.** §8 operator rulings do not arise (conditional on RESOLVED).

---

## Addendum 2026-08-01 — the cliff does NOT survive multiplicity. A published figure of mine is corrected, and the successor question is withdrawn.

Run as the gate-reachability pre-flight for a proposed **Q-EQCLOSE-1** (equity-close-flow)
pre-registration, *before* authoring it. The pre-flight killed the brief. $0, K=0.

### 1. Every date-conditional design is underpowered by 2–5×

MYM final-block signed `driftR`: n=1,484, mean **−0.02999**, **sd 0.52910**. The cross-day SD is
**17.6× the mean**, so:

| subgroup | n | SE | MDE (95%) | detects −0.030? |
|---|---:|---:|---:|---|
| early-close sessions | 53 | 0.0727 | 0.1425 | **NO** (4.7× short) |
| early-close @ 12:45 only | 41 | 0.0826 | 0.1620 | **NO** |
| monthly OPEX | 72 | 0.0624 | 0.1222 | **NO** |
| ordinary Fridays (control) | 240 | 0.0342 | 0.0669 | **NO** |

Detecting the pooled effect needs **n ≈ 1,194 days**. No flow-date subgroup comes close, so a
date-conditional mechanism test cannot be run on panels held here.

### 2. The pooled effect itself is not significant once blocks are counted

Measured identically on both instruments for the first time (same statistic, per-day SEs):

| block | MNQ t | | block | MNQ t |
|---|---:|---|---|---:|
| 10:30 | +1.77 | | 13:30 | +1.44 |
| 11:00 | +1.15 | | **14:00** | **−1.84** |
| 11:30 | +0.70 | | 14:30 | +0.22 |
| 12:00 | +1.64 | | 15:00 | +0.74 |
| 12:30 | +0.48 | | **15:30 (final)** | **−1.78** |
| 13:00 | −0.49 | | | |

- **MNQ:** final block **t = −1.78**; **max \|t\| across all 11 blocks = 1.84**, which is *below* the
  expected max of 11 draws under the null (≈ 2.2–2.4). The profile is **indistinguishable from noise**.
- **MYM:** final block **t = −2.18** — right *at* the expected max of 11. Unremarkable as a maximum.
- **The 14:00 MNQ block (−1.84) is as negative as the final block (−1.78)**, so "the final block is
  special" does not hold even descriptively.

### 3. Correction to a figure published earlier today

Q-SESSCONF-1's exposure control reported the final block as a **z = −2.90** outlier. That statistic
**differenced the ladder** and estimated its dispersion from the same 11 differenced points, treating
them as independent draws. The direct per-day test above — proper standard errors, no differencing —
is the better instrument, and it returns **t = −1.78**. **The z = −2.90 overstates the anomaly and
should not be quoted.** Q-SESSCONF-1's *verdict* is unaffected (it was FALSIFIED on the Δ\* ceiling,
which this does not touch).

### 4. What survives, and what is withdrawn

**Survives:** the exit-policy P&L difference is real arithmetic — holding longer exposes a fixed stop
to more −1R events (Q-EODADV-1: 76.3% stop-out channel, −0.488R per event). That is *exposure with an
asymmetric payoff*, not an end-of-day effect.

**Withdrawn:** the premise that the final half-hour is anomalous. It is not anomalous in drift
(t = −1.78, below the null max), not in hazard (**below** constant-hazard: 3.56% vs 3.96%), and not in
range (1.06–1.12×). Three separate signatures, all ordinary.

**Consequently no Q-EQCLOSE-1 pre-registration was authored.** Writing one would have spent operator
attention on a mechanism study for a phenomenon that does not survive its own multiplicity — and
would have burned the MNQ family's last Cap seat chasing it. The equity-index-specificity noted in
Phase 5 is a real *descriptive* contrast, but with the pooled effect at the null maximum it is not a
foundation for a mechanism claim.

**Disposition — ✅ RULED 2026-08-02 (operator): the end-of-day-adversity line is CLOSED as
tail-exhausted, and the raised bar is recorded.** Four mechanism attempts (reversal, variance
expansion, drift exhaustion, equity-close flow), all closed at **$0 / K=0**. Landed as a
domain-level tail-exhaustion entry in
[`docs/rejected_candidates.md`](../../../docs/rejected_candidates.md) §Domain-level tail-exhaustion
raised bars, with a three-clause re-proposal bar (different modality / evidence the phenomenon
survives multiplicity / a panel beyond n ≈ 1,200 per subgroup). The 07-21 entry's stale
"session-confluence longer-hold — untested" preservation is marked **DISCHARGED** in the same pass.
Dated dispositions appended to [`MNQ.md`](../../../ops/instruments/MNQ.md) (as **N8**) and
[`MYM.md`](../../../ops/instruments/MYM.md). **Not** a SNAG closure; `ORB-MNQ-1` and the MNQ Cap seat
are explicitly preserved.

---

Reproduce (in order — the freeze is load-bearing):

```bash
V=/c/Users/joshu/multi_firm_operations/.venv-research/Scripts/python.exe
$V lab/analysis/driftex_2026-08/run_phase123_freeze_tstar.py
$V lab/analysis/driftex_2026-08/run_phase456_ladder_verdict.py
$V lab/analysis/driftex_2026-08/run_phase5_scope_probes.py
```
