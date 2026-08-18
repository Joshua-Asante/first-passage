# Q-TRAINKILL-3 — Verdict pre-registration (H-TK3)

**Frozen:** 2026-08-18, **before any block geo-mean or concordance
winner is computed.**
Parent brief: [`Q-TRAINKILL-3-neg-vs-dep-discriminator.md`](../Q-TRAINKILL-3-neg-vs-dep-discriminator.md).
Parent closure: [`Q-TRAINKILL-2-closure-ambiguous-hold.md`](../closures/Q-TRAINKILL-2-closure-ambiguous-hold.md)
entry packet. Operator GO: this session ("commit and continue on
Q-TRAINKILL-3"). That GO does **not** name `NEG-FAMILIES` or
`KILLS-INFORMATIVE-DEP`, so the election limb does not fire.

A verdict computed after moving the block membership, the tie ratio, or
the concordance rule is void.

**Inherited, not retuned:** 15-set · μ_0=0 · μ_bar=+0.10R · μ_neg=−0.10R ·
Fréchet-hi · se=CI-width/3.92 · independence product on NEG · fit floor
0.05 · no bar-lowering · no one-arm re-read · no ρ→R · no third μ.
Carry-forward (already committed, not a substitute here): MSL-S2A
promoted; six still BOUNDED; g(NEG)=0.239; g(DEP-ZERO)=0.189;
g(+0.10)=0.000961; both-alternates-fit hold.

The input to this Q is the committed TK2 per-row P vectors
(`lab/analysis/_inbox/q_trainkill_2_2026-08/RESULTS.json` keys `P_neg`
and `P_dep_zero`). No new CIs. The *new* compute is the two block
geo-means and the concordance winner — that compute is forbidden until
this file is hashed.

---

## §A — Election limb (does not fire this GO)

`RESOLVED` the named DGP iff the operator GO text names **exactly one**
of `NEG-FAMILIES` or `KILLS-INFORMATIVE-DEP` as the working-model.
This GO names neither. Recording that now so a later election is a
fresh GO, not a silent re-read of this brief.

---

## §B — Blocks (frozen membership; event-class split)

Block membership is the TK2 scored-row **event**, not a post-hoc
se-shop.

**Block F** (FALSIFIED, both-arms) — n=4:

1. MSL-C1
2. MSL-C2
3. MSL-C3-K2
4. Q-MNQDTL-CON-1

**Block A** (AMBIGUOUS) — n=5:

1. Q-TNEC-CON-2
2. Q-TNEC-CON-3
3. Q-TNEC-CON-4
4. Q-TNEC-CON-5
5. MSL-S2A

Silent drop of any named id voids the read. CON-4 stays in Block A.

---

## §C — Winner and tie (declared before block g)

For a block, `g_NEG = exp(mean log P_neg)` and
`g_DEP = exp(mean log P_dep_zero)` on that block's rows.

| Winner | Trigger |
|---|---|
| `NEG` | g_NEG / g_DEP ≥ 2 |
| `DEP` | g_DEP / g_NEG ≥ 2 |
| `TIE` | ratio in (1/2, 2) |

The 2:1 bar is conventional (not fitted to TK2's joint g ratio). It is
**not** the 0.05 fit floor and does not retune it.

---

## §D — Concordance verdict

| Verdict | Trigger |
|---|---|
| `RESOLVED` — `NEG-FAMILIES` | both blocks `NEG` |
| `RESOLVED` — `KILLS-INFORMATIVE-DEP` | both blocks `DEP` |
| `AMBIGUOUS-HOLD` | blocks disagree, or either block is `TIE` |

---

## §E — Disposition

| Verdict | Disposition |
|---|---|
| `RESOLVED` — either named DGP | `INTEGRATE` — that DGP is the working-model; the other is not claimed falsified beyond this split; still no bar-lowering; drought quotes carry the named annotation |
| `AMBIGUOUS-HOLD` | `STOP` — the two DGPs are not concordant on committed mean-R cells; do not open Q-TRAINKILL-4; re-proposal is a new panel or an operator election |

STOP on a split is load-bearing. A fourth joint-likelihood Q on the
same P vectors would be naming rules until one DGP wins.

---

## §F — Pinned ex-ante expectation

**Predicted: `AMBIGUOUS-HOLD` (split).** Class, not a substitute of
block g: Block F is the four both-arms FALSIFIED cells (NEG raises
P(F); DEP leaves them at ~0.025); Block A contains the tight
zero-straddle (DEP leaves P(AMB) high; NEG does not). Concordance is
predicted to fail. The 2:1 bar is expected to make that split a pair of
named winners, not two ties — that last clause is a class guess, not a
number.

---

**Freeze note:** this file must exist on disk, with a recorded sha256,
**before** block geo-means are computed from the TK2 P vectors.
