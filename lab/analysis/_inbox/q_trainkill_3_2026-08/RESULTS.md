**Theme:** _inbox
**Status:** AMBIGUOUS-HOLD — Block F NEG and Block A DEP (split)
# Q-TRAINKILL-3 — NEG vs DEP two-block concordance

**Verdict:** `AMBIGUOUS-HOLD`. Block F winner `NEG` (ratio 9.83). Block A winner `DEP` (ratio 0.246 = DEP at 4.06:1). Split.
**Date:** 2026-08-18
**Spend / K:** $0 / K=0
**Parent:** [`Q-TRAINKILL-3-neg-vs-dep-discriminator.md`](../../../../docs/briefs/Q-TRAINKILL-3-neg-vs-dep-discriminator.md)
**Prereg (hashed before TK2 RESULTS.json was opened by the scorer):**
`93c21d21eb0fd2d0e580a384a586dbf10d19d8a23a593dea6e147f63ad57e7f6`

Reproduce:

```bash
python lab/analysis/_inbox/q_trainkill_3_2026-08/score_trainkill3.py
```

The runner prints the prereg sha256 **before** reading the TK2 P vectors.

---

## Concordance vs the frozen 2:1 bar

| Block | n | g(NEG) | g(DEP) | ratio NEG/DEP | Winner |
|---|---|---|---|---|---|
| F (FALSIFIED both-arms) | 4 | **0.246** | 0.0250 | **9.83** | **NEG** |
| A (AMBIGUOUS) | 5 | 0.234 | **0.950** | 0.246 | **DEP** |

Election limb did not fire (GO named no DGP).

`AMBIGUOUS-HOLD` because the blocks **disagree**. The 2:1 bar was not moved.

---

## What this does not license

- A singleton working-model (`NEG-FAMILIES` or `KILLS-INFORMATIVE-DEP`).
- Quoting `GATES-UNDERPOWERED` (bar still missed at TK2).
- Q-TRAINKILL-4 on these same P vectors.
- A third μ, a one-arm re-read, ρ→R, or any gate-threshold move.
- Treating this GO as an election.
