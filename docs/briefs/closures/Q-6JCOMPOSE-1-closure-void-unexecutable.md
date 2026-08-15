# Closure — Q-6JCOMPOSE-1: `VOID — UNEXECUTABLE AS FROZEN`

**Date:** 2026-07-29 · **Pre-reg:** [`Q-6JCOMPOSE-1-verdict-preregistration.md`](../pre-registration/Q-6JCOMPOSE-1-verdict-preregistration.md)
(`SIGNED / FROZEN 2026-07-29 / JA`, commit `daf8f11`)
**Verdict:** **VOID.** Not `RESOLVED`, not `FALSIFIED`, not `AMBIGUOUS` — **no 6J composed number was
ever read.** The frozen method could not be executed as written.
**Successor:** [`Q-6JCOMPOSE-2-verdict-preregistration.md`](../pre-registration/Q-6JCOMPOSE-2-verdict-preregistration.md)
(close-and-reopen-fresh; precedent [`aegis-6j v1→v2 window-realigned`](../pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2-window-realigned-prereg.md),
adjudicated `FRESH-PREREG-OK` for the same class of defect).
**Spend:** $0.00. **K:** unchanged (no discovery search; the candidate is pre-existing).

---

## §1 — What passed before the halt

Phase 0 was executed in full and **all runnable §10 hooks passed**:

| Hook | Result |
|---|---|
| 1 — freeze precedes execution | **PASS** — freeze `2026-07-29 17:55:31`, strictly before any artifact |
| 2 — engine unmodified | **PASS** — empty diff on `run_compose_regime_remc.py` |
| 3 — baseline current | **PASS** — returns line 15, `0.11% / 99.80%` |
| 4 — S5 collision reproduces | **PASS** — Mon 44 / Tue 25 / Wed 60 / Thu 0 / Fri 0, exact |
| 5 — no cap re-allocation | **PASS** — MYM 69 / MNQ 11 |
| 7 — lock untouched | **PASS** — 0 HARD, empty diff on `core/` + sizing host |
| 6 — single-cell discipline | n/a — requires a run artifact that was never produced |

Engine wiring was additionally proven end-to-end (smoke, 20 s): the composed path runs and its
Tradeify row brackets the published C1 target at reduced sim counts.

## §2 — Why it is VOID: three frozen elements are unexecutable

**(1) The decisive one — P4 and §2 are mutually unsatisfiable (M-SWAP-1 recurrence).**
P4 *requires* the 6J series enter on the incumbents' de-compounded basis. The only faithful route is
the frozen `build_scaled_panel`, which computes

```python
scale = (alloc * ACCOUNT) / r_dollars        # r_dollars = full-stop mean OF THAT SERIES
pnl_scaled = pnl_static * scale
```

This is **exactly scale-invariant**: multiplying the input by any constant leaves `pnl_scaled`
unchanged. So the primitive **absorbs §2's cap-8 row entirely** and **largely absorbs the $3.10/side
commission** (a per-contract additive shift on a near-constant `qty`, which also moves `r_dollars`
and partially cancels). Those are the two inputs §2 froze as load-bearing — and commission was the
single most decisive input in the standalone work (it moved breach 3.88% → 12.40%).

This is [**M-SWAP-1**](../../methodology/lessons/methodology_lessons.md) reproducing on new data:
*the `implied_1r` normalization absorbs additive cost shocks as reduced position size, so a
1R-normalized MC is the wrong instrument for costing them.* The lesson was recorded for swap cost in
June; it applies unchanged to commission and contract caps.

**Direction of the error was knowable and adverse.** Had the run proceeded, the normalized leg would
have been **0.515×** of `ae744` (`1500 / 2912.96`) against §2's arm at **0.352×** (cap 8 × 0.50 /
avg qty 11.36) — **+46.2% larger**, hence more variance, hence **biased toward FALSIFIED, which was
the disclosed §4 prior.** Running it would have manufactured the expected answer.

**(2) §7 C3 and §10 hook 4 were not propagated when §2 was amended.** The pre-signature §2
correction (`8e269` → `ae744`, disclosed in §9) left C3 expecting **dropped 25 / retained 104** and
hook 4 pinned to `c3b34162…` — both `8e269`-derived. Under `ae744` the counts are **28 / 124**, so C3
fails as literally written against the panel §2 names. **Author defect (mine), recorded not edited.**

**(3) Post-signature amendment is forbidden.** Trap #12 permits no in-place edit of a frozen
artifact; the pre-signature window that made the §2 correction legal closed at `daf8f11`.

## §3 — What survives, and is carried forward unchanged

- **All Phase-0 results** (§1) — re-usable; the successor need not re-derive them.
- **Control C1** (engine equivalence, ORB row) — **independent of the 6J input**, launched and
  running; its result carries to the successor.
- **P5's discharge and ledger J11** — `ae744` is KNOWN-config and H1-covering. Unaffected.
- **§4's falsifiable H and its disclosed prior (FALSIFIED expected)** — carried verbatim.
- **The S5 Mon+Wed variant** — structurally identical on both panels (`8e269` 80.6% retained,
  `ae744` 81.6%), so the variant is not a panel artifact.

## §4 — Lesson candidates

1. **A pre-registration must state the *basis* of every load-bearing input, not just its value.**
   §2 froze "cap 8" and "$3.10/side" as if they were free parameters of the composed gate; they are
   properties the gate's own normalization cannot see. The defect was latent from authoring and only
   surfaced by reading the primitive's arithmetic at Phase 0.
2. **Amending one frozen section requires sweeping every section that cites it.** The §2 correction
   was right; failing to propagate to §7/§10 is what made the brief internally inconsistent.
3. **M-SWAP-1 generalizes beyond swap cost.** Any additive per-contract cost — commission,
   slippage — and any uniform size constraint is invisible to a 1R-normalized gate. Cost and cap
   questions belong to the standalone survival measurement; the composed gate answers variance
   composition only.

## §5 — Disposition

**D2 (Aegis-6J) remains PARKED, unchanged.** Nothing was measured, so nothing moved. Nothing armed;
no `core/`, allocation, `dd_protection`, Pine, rung, or rail byte touched. The composed question is
**re-opened, not abandoned** — see the successor.
