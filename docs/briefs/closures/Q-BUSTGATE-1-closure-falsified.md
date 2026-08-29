# Q-BUSTGATE-1 — CLOSURE: `FALSIFIED` (eval-fee-vs-funded-upside economics do not ratify the 3.0% ceiling; operator elected fork B)

**Closed:** 2026-07-23
**Parent brief:** [`../Q-BUSTGATE-1-bust-gate-re-derivation.md`](../Q-BUSTGATE-1-bust-gate-re-derivation.md) (anchor `a3a7d71`) — now `CLOSED-FALSIFIED`
**Pre-registration (FROZEN before the derivation was read):** [`../pre-registration/Q-BUSTGATE-1-verdict-preregistration.md`](../pre-registration/Q-BUSTGATE-1-verdict-preregistration.md) — commit `98d0fa6`
**Fork-B artifact:** [`../../adr/2026-07-23-c1-rung-selection-ev-objective.md`](../../adr/2026-07-23-c1-rung-selection-ev-objective.md) (`Proposed`)
**Directive:** 08-08 packet §0.5 directive (1) / §3 P0 (operator, 2026-07-23)
**Execution invariants held:** zero `core/` edits; zero live-sizing / rail / lifecycle change; the incumbent 3.0% survivor-scoring pre-reg (`be6dda6`) byte-unedited (Trap #12); K = 0 (locational read of closed artifacts, no new run).

> ⚠ **Correction 2026-08-29:** the three `Proposed` tags on the Fork-B ADR below (header, Operator-fork-election §, §10 audit-hook line) are stale — the ADR was ratified Accepted the same day (2026-07-23; see its Status line and Change history). Correct status: Accepted, as already stated in Dispositions below. Body text is left byte-unedited per Trap #12.

> ⚠ **Figure caveat 2026-08-06 (claim-alignment LAB-1):** bust cells sourced from
> `lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS.md` were computed under
> defective `dd_lock_offset_usd: 100`. Corrected pins: full-panel **0.11%**, H1 **0.22%**,
> boot-95th **1.20%** (0.50×); H1 **6.78%** (1.00×). See that RESULTS banner +
> `CORRECTED_FULLPANEL.md`. Verdicts unchanged (0.50× PASS / 1.00× FAIL).

## Verdict (§6 asserted against actual numbers)

**`FALSIFIED`** — per the frozen pre-registration's §D locational rule, the eval-fee-vs-funded-upside-**optimal admissible rung** (Q-FUNNEL-1's horizon-robust `edge_panel_historical` cell prefers **1.00×**, ladder-capped) busts **4.37% (H1) / 10.37% (bootstrap-95th) > 3.0%** on the Tradeify Select 100K deployable expression. The EV optimum sits **outside** the incumbent ceiling → H-BUSTGATE's ratification claim ("economics ratifies 3.0%") is **rejected**. This matched the pre-reg §E pinned expectation exactly (no surprise; the read was deterministic from the closed Q-FUNNEL-1 artifact `b56c5b3`).

**The finding:** the fee/upside asymmetry is ≈**12–36:1** (one Flex payout ≤ $4,000 vs one eval re-attempt $111 promo / $328 all-in), so eval-fee economics tolerate a bust rate far above 3.0%. The 3.0% ceiling is therefore **not** a fee/upside quantity — it is a **survival / P(pass) / firm-relations** gate, sitting between the 1%-null-by-construction and 17.70%-falsified-book poles the survivor-scoring pre-reg §3 named. Economics do not reproduce 3.0% and do not point to a tighter number; they point looser.

## What the pre-registration predicted vs what happened

The pre-registration deliberately fixed a **binary locational** method (inside/outside 3.0%) with **no free tolerance parameter**, precisely to bar a derivation tuned to clear the operator's parallel 1.00× aim (directive 2). It recorded the pinned expectation (§E: middle row `FALSIFIED` fires) so a different outcome would be a visible surprise. Outcome = exactly the pinned expectation. No amendment; no in-place edit of any frozen number (Trap #12 intact).

## Operator fork election

Presented with the two-option fork the `FALSIFIED` verdict routes, the operator **elected fork B** (2026-07-23): adopt an **EV-per-dollar-day rung-selection objective** for the c1 book via a fresh superseding ADR. Recorded in [`../../adr/2026-07-23-c1-rung-selection-ev-objective.md`](../../adr/2026-07-23-c1-rung-selection-ev-objective.md) (`Proposed`).

**Fork A** (retain 3.0% re-justified as a survival gate) was declined; it stands as the ADR §4 revert target, not vacated.

## Dispositions

- **Q-BUSTGATE-1 CLOSED-FALSIFIED.** The derivation-layer question is answered; the operator fork is elected.
- **The 3.0% survivor-scoring gate is RETAINED, unedited, as the candidate-ADMISSION falsifier** (four-firms ADR §4). Fork B's ADR is scoped to the c1 **rung-selection** objective only — not admission, not the frozen pre-reg.
- **A0b resolved NO-GO on 1.00× (2026-07-23).** The both-halves regime-robustness gate — A0b's core safety check — was **already run** under a frozen operator-signed pre-reg (`class_s_c1_haircut_regime_remc`, 2026-07-17): **1.00× FAILS** (regime-fragile — H1 chop-half bust 4.37%, bootstrap-95th 10.37%, both > the 3.0% floor), **0.50× PASSES** both halves. So the fork-B EV objective, correctly constrained by the retained regime gate, selects **0.50× (WATCH-1)** — the current rung. Operator chose **"keep 0.50× / accept NO-GO"**. The **08-08 calendar dependency is removed** (the regime result, not the date, was the real gate). A higher rung requires a **fresh** both-halves regime PASS — which the current evidence contradicts.
- **No change to live sizing.** The c1 rung stays WATCH-1 0.50× / disarmed. Fork B's ADR ([`../../adr/2026-07-23-c1-rung-selection-ev-objective.md`](../../adr/2026-07-23-c1-rung-selection-ev-objective.md), `Accepted`) authorizes no sizing change and does not override the failed regime gate.
- **08-08 packet:** P0 discharged (this brief + pre-reg + ADR); A0 = fork B elected; **A0b = NO-GO on 1.00×** on the already-run regime gate.
- **K-accounting:** zero K consumed or banked (locational read of closed artifacts).

- **Registry:** n/a — threshold/gate re-derivation, not a strategy-grounds kill. H-BUSTGATE tested whether the incumbent 3.0% Part-A bust ceiling is economically ratified for an already-admitted book's (c1, MYM+MNQ) lifecycle rung, not a new strategy/instrument/parameter portfolio addition (`docs/rejected_candidates.md`'s own scope line 3: "strategy / instrument / parameter combinations investigated and rejected as portfolio additions"). No candidate was scored, admitted, or rejected; WATCH-1 0.50× (the deployed rung) stands unaffected and PASSES the ceiling; the 3.0%/50% ceiling itself stands unedited (Trap #12 intact). Nothing is added to or removed from `rejected_candidates.md` (cf. Q-BUSTGATE-2's identical self-classification, `docs/briefs/closures/Q-BUSTGATE-2-closure-resolved.md` L58: "threshold re-derivation, not a strategy-grounds kill").

## Lesson candidate

1. **A survival gate re-derived from pure EV economics degenerates to "looser," not "more correct."** The 3.0% barrier-width heuristic was easy to read as un-economic and therefore suspect; but re-pricing it against fee/upside doesn't tighten or refine it — it reveals the gate was never an EV quantity. When a gate's stated rationale is a proxy (barrier-width) for an unstated objective (survival), re-deriving it under a *different* objective (EV) will always loosen it, because the objectives disagree. The methodologically load-bearing move was pinning a **binary locational** read (inside/outside) with no tolerance knob, so the re-derivation could not be bent toward the parallel 1.00× aim. One incident; watch for a second before promoting to a load-bearing lesson.

## §10 audit-hook discharge (run this session)

- Pre-reg commit `98d0fa6` predates the brief's admission (`a3a7d71`, later) — freeze-before-derivation ordering holds ✔
- Locational numbers (4.37% / 10.37% / 3.0%) quoted verbatim from `b56c5b3` / `be6dda6`, not re-derived ✔
- Incumbent 3.0% pre-reg (`be6dda6`) byte-unedited ✔
- `check_brief.py --type inquire` on the parent brief: 6/6 PASS ✔
- ⚠ 2026-08-29: the "Fork-B ADR `Proposed`" read below was a same-session snapshot taken before ratification, not a verified current-state check — see the correction banner near the top of this file.
- Fork-B ADR `Proposed`, live rung unchanged (WATCH-1 0.50× / disarmed) ✔
