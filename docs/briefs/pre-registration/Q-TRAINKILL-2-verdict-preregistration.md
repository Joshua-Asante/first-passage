# Q-TRAINKILL-2 — Verdict pre-registration (H-TK2)

**Frozen:** 2026-08-18, **before any BOUNDED-row file is opened for a mean-R CI
or any alternate-DGP g is computed.**
Parent brief: [`Q-TRAINKILL-2-bounded-recovery-alt-dgp.md`](../Q-TRAINKILL-2-bounded-recovery-alt-dgp.md).
Parent closure: [`Q-TRAINKILL-1-closure-ambiguous-hold.md`](../closures/Q-TRAINKILL-1-closure-ambiguous-hold.md)
entry packet. Operator GO: this session ("commit and continue with Q-TRAINKILL-2").

A verdict computed after moving the recovery rule, the alternate μ, the
Fréchet convention, the fit floor, or the event map is void.

**Inherited, not retuned:** 15-set · μ_0=0 · μ_bar=+0.10R · se=CI-width/3.92 ·
both-arms independence product · fit floor 0.05 · TK1 §C event map · no
bar-lowering. Carry-forward (already committed, not a substitute here):
scored g(0)=0.024365, g(+0.10)=1.807e-05; four both-arms P(F|μ=0)≈0.000625;
CON-4 P(AMB|μ=+0.10)=0.00272.

**Forbidden regardless of outcome:** no gate threshold moves. A one-arm
re-read of a both-arms cell is not a re-proposal (TK1 stop rule).

---

## §A — Recovery corpus (the seven TK1 BOUNDED ids)

Search **only** the committed source path already named on that row in
`lab/analysis/_inbox/q_trainkill_1_2026-08/TABLE.json`. Silent substitution
from a different file voids the row.

1. MSL-S2A
2. Q-R2VBUCK-1
3. Q-R2FLOW-1
4. Q-R2AGRUN-1
5. DL-1
6. Q-CAPFLOW-1
7. H-DSTRUCT-MNQ-1

---

## §B — Recovery rule (what counts as a mean-R CI)

A BOUNDED row **promotes to scored** iff the named source quotes a numeric
session-block interval on the **per-trade mean in R** (labels: mean R,
mean_r, CI on R, session-block mean-R) that the TK1 §C event map can
consume (FALSIFIED / AMBIGUOUS / CLEARED from CI vs 0).

**Does not promote** (ρ→R translation remains forbidden):

- ρ / association CIs
- annSR / SPA / nomination-gate p-values
- N-ACT / cadence / abandonment flags
- gateHit vs 0.50 (or any non-R rate)

Two-arm mean-R CIs: same both-arms product as TK1 if the source's binding
gate required both arms; else the binding arm the source named.

If the source has no such interval, the row **stays BOUNDED**. Partial-table
ε-brackets inherited from TK1 §D.

---

## §C — Alternate DGPs (named now; scored-core only)

Evaluated on the scored set after recovery (original 8 plus any promotions).
BOUNDED rows do **not** enter these g's.

| DGP | μ | both-arms joint |
|---|---|---|
| zero (inherited) | 0 | independence product |
| bar (inherited) | +0.10R | independence product |
| `NEG` | **−0.10R** (symmetric counterpart of the admissibility bar) | independence product |
| `DEP-ZERO` | 0 | Fréchet-hi: `P = min(P_arm1, P_arm2)` on both-arms rows; one-arm unchanged |

`g(μ, joint) = exp(mean log P_i)`. A DGP **fits** iff `g ≥ 0.05`.

Fréchet-hi is the named dependence DGP from the TK1 entry packet. It is
**not** a one-arm re-read: both arms must still be FALSIFIED; only the
joint changes. Fréchet-lo is disclosed, not a fire (it is more extreme
than independence and cannot rescue g(0)).

---

## §D — Verdict routes (ordered; first fire wins except the multi-fit clause)

**Limb 1 — recovery (inherited {0, +0.10} readings, TK1 §E):**

| Reading | Trigger |
|---|---|
| `GATES-UNDERPOWERED` | after recovery, bar fits; BOUNDED extremes **agree** |
| `KILLS-INFORMATIVE` | after recovery, zero fits and bar does not; extremes **agree** |
| `MISCALIBRATED` | after recovery, neither {0, +0.10} fits; extremes **agree** |
| (no Limb-1 fire) | 0 promotions, **or** extremes still disagree |

Limb 1 fires only on a **change** from TK1's hold: at least one promotion
**and** extremes now agree. Zero promotions cannot re-assert TK1's hold as
a new Limb-1 verdict.

**Limb 2 — alternates (scored-core only; runs iff Limb 1 did not fire):**

Let S = {`NEG` fits, `DEP-ZERO` fits}. Inherited {0, +0.10} under
independence are **not** re-opened as Limb-2 fires (they already missed
on the original 8; they may be recomputed after promotions and still
do not fire Limb 1 if extremes disagree).

| Reading | Trigger |
|---|---|
| `NEG-FAMILIES` | S = {`NEG`} only |
| `KILLS-INFORMATIVE-DEP` | S = {`DEP-ZERO`} only |
| `AMBIGUOUS-HOLD` | both members of S fit, or n*=0 |
| `MISCALIBRATED` | neither member of S fits |

---

## §E — Disposition

| Verdict | Disposition |
|---|---|
| any Limb-1 named reading | `INTEGRATE` — same as TK1 §E for that reading |
| `NEG-FAMILIES` | `INTEGRATE` — FALSIFIED both-arms cells read as true-negative families, not empty or +0.10; still no bar-lowering; drought quotes still not licensed as empty-family evidence |
| `KILLS-INFORMATIVE-DEP` | `INTEGRATE` — zero-edge fits only under Fréchet-hi; independence product was the TK1 miscalibration; drought quotes require this dependence annotation |
| `AMBIGUOUS-HOLD` | `ITERATE` — two alternates fit, or n*=0; do not pick one after seeing g |
| `MISCALIBRATED` | `STOP` — recovery found nothing and both named alternates miss; do not keep naming μ until one fits |

---

## §F — Pinned ex-ante expectation

**Predicted: 0 promotions** (class: the seven were BOUNDED because they are
not mean-R events). **Predicted Limb-2: `MISCALIBRATED` or `NEG-FAMILIES`.**
Class: −0.10R raises P(FALSIFIED) on the four both-arms cells, but CON-4's
tight zero-straddle is also unlikely under −0.10R (same shape that killed
+0.10R). `DEP-ZERO` may lift g(0) by replacing 0.000625 with ~0.025.
Substituting CIs / computing g is the compute step, not this freeze.

---

**Freeze note:** this file must exist on disk, with a recorded sha256,
**before** any of the seven source files is opened for a number and
**before** `TABLE.json` for this Q is assembled.
