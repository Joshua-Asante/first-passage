**Theme:** _inbox
**Status:** CLOSED — `FALSIFIED` (S1b conditioner-engineering branch parked)
# Q-CONDVAL-1 — RESULTS: FALSIFIED

**Date:** 2026-08-18 · **Verdict: `FALSIFIED`**
**Pre-registration:** [`Q-CONDVAL-1-verdict-preregistration.md`](../../../docs/briefs/pre-registration/Q-CONDVAL-1-verdict-preregistration.md)
**prereg_sha256 (printed before JSON substitute):** `d1265eb2b0fa328c18b8a744a6f438d06611238fd2ada14ca12d06645748b386`
**Parent:** [`Q-CONDVAL-1-range-state-r-terms.md`](../../../docs/briefs/Q-CONDVAL-1-range-state-r-terms.md)
**Spend:** $0.00 · K=0 · no manifest · no vendor bars read
**Runner:** [`run_condval.py`](run_condval.py) · full JSON: [`RESULTS.json`](RESULTS.json)

---

## 1. Frozen bar vs measured lift

| | value |
|---|---|
| gating host | rr=2.5 · WR=0.36 · `E_box`=0.26R |
| gating envelope | R=$75 · RT=$4.12 · `hurdle_4x`=0.2197R |
| material fraction | 0.50 → `bar_ΔE`=0.1099R |
| **`L_star`** | **0.422564** |
| `gateHit` | 0.628235 (committed `s1b_results.json`) |
| `p_up_unconditional` | 0.498541 |
| **`L` (C−U)** | **0.129694** |
| `ΔE = L × E_box` | 0.033721R |
| `L − L_star` | **−0.292870** |
| 0.60 used? | no |
| IAAFT-excess used? | no |

`L < L_star` → §6 `FALSIFIED`. Predicted in prereg §C.

The lift is 31% of the frozen bar (0.130 / 0.423). In R terms the conditioner adds **0.034R** at the gating cell against a **0.110R** material bar — about 3.3× short, even under the α=0 mapping that credits the conditioner with *all* of `E_box` on high-range days.

---

## 2. Disclosure (does not gate)

Every positive-gross slate-2 corner fails the **gating** bar (`bar_ΔE`=0.110R). The optimistic corner (WR=0.42, rr=3) reaches 0.088R.

Envelope ends, gating-center `ΔE`=0.034R held fixed:

| cell | `hurdle_4x` | 0.50× bar | center `ΔE` clears? |
|---|---|---|---|
| R=$75, RT=$4.12 (gating) | 0.220R | 0.110R | no |
| R=$200, RT=$2.82 (easy end) | 0.056R | 0.028R | **yes** |

The easy-end clear is why the cell was pre-declared. It does not rescue the verdict (prereg §B).

---

## 3. What this does not say

- SIGNAL-GENERIC stands. This is not a battery re-try and not a retraction of C−U 0.130.
- MCL mechanism-owed stands (A6).
- S2 / S3 are untouched (their un-pause conditions are spec-resident, not this Q).
- A different host geometry would be a new Q, with its three levers declared before a re-read.

---

## 4. Reproduce

```bash
python lab/analysis/_inbox/q_condval_1_2026-08/run_condval.py
# prereg_sha256 d1265eb2b0fa328c18b8a744a6f438d06611238fd2ada14ca12d06645748b386
# L 0.129694  L_star 0.422564  verdict FALSIFIED
```
