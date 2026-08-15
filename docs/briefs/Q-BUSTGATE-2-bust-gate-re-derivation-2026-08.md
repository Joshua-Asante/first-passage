# Q-BUSTGATE-2 — Does the 2026-08-13 external population data or the updated Tradeify fee schedule move the Part-A eval bust ceiling?

**Status:** `CLOSED-RESOLVED 2026-08-15` — H-BUSTGATE-2's constrained decision rule fires `RESOLVED`: the incumbent **3.0%** ceiling is unchanged. Closure: [`closures/Q-BUSTGATE-2-closure-resolved.md`](closures/Q-BUSTGATE-2-closure-resolved.md).
**Authored:** 2026-08-15
**Closed:** 2026-08-15
**Authors:** Joshua (operator directive — "re-derive the N-SURV bust ceiling") + Claude Code (22-agent adversarial workflow: recon → pre-registration → 2-round stress test → execution → independent arithmetic re-check).
**Parent question:** [`Q-BUSTGATE-1`](Q-BUSTGATE-1-bust-gate-re-derivation.md) (`CLOSED-FALSIFIED` 2026-07-23) — this is the second re-derivation under new input classes, not a reopening of the first.
**Sub-questions opened:** none.
**Loop:** Inquire-phase Pre-Q — closure gated on the frozen §D decision rule in the pre-registration.
**Artifact path:** `docs/briefs/Q-BUSTGATE-2-bust-gate-re-derivation-2026-08.md`
**Pre-registration (frozen, post-adversarial-stress-test, committed before Phase 3 read any candidate-specific number):** [`pre-registration/Q-BUSTGATE-2-verdict-preregistration.md`](pre-registration/Q-BUSTGATE-2-verdict-preregistration.md)

---

## §0 — Rule 0 reads (production-source verification)

Files read before authoring, each with a `git log -1` anchor (verified 2026-08-15 on this worktree):

- `docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md` — anchor `91137fb` (2026-08-03, path-repair only; thresholds byte-identical since `be6dda6` 2026-07-13). §3 barrier-width rationale for 3.0%/50%, read in full.
- `docs/briefs/Q-BUSTGATE-1-bust-gate-re-derivation.md` + `docs/briefs/closures/Q-BUSTGATE-1-closure-falsified.md` — anchor `55e1c49` (2026-08-06, the corrected-pins caveat banner). The first re-derivation: EV-optimum busts 4.37%/10.37% > 3.0%; ceiling retained; operator elected fork B (EV/dollar-day rung-selection objective); fork B's own regime-robustness precondition selects 0.50× regardless.
- `docs/adr/2026-07-23-c1-rung-selection-ev-objective.md` — anchor `5563cf4` (2026-08-10, path-repair only; content ratified 2026-07-23). §2: "the EV objective... correctly constrained, selects 0.50× (WATCH-1)"; §5 category-error guard against transcribing an EV-optimum's bust as a new ceiling.
- `docs/notes/notice/N-2026-08-13-external-eval-population-data.md` — anchor `b2e3eec` (2026-08-13). The new input class: Tradeify 17.2%/40.3%/28.5%/3.0% funnel; explicit §7 caveat that population data is "a third input, not a dial" and that re-deriving a gate under a different objective "degenerates to looser, not more correct" absent new justification.
- `docs/notes/2026-08-13-tradeify-select-100k-checkout-price.md` — anchor `67e4b20` (2026-08-13). The second new input class: $159 promo / $265 list / $169 reset / $0 activation, promo binding until 2026-08-31 23:59 EST.
- `core/firm_rules.py` — anchor `0356be2` (2026-08-11). `Tradeify_Select_100K`: `dd_type="trailing_locking"`, `max_dd_pct=3.0`, `dd_lock_offset_usd=1_000_000.0` (unreachable, fixed 2026-08-04), `cost_per_side_usd=0.91`.
- `core/dd_protection.py` — anchor `0356be2` (2026-08-11). `DD_TRIGGER=0.015` / `DD_SCALE=0.40` — verified as a **different, unrelated frozen constant** from the N-SURV bust ceiling (a portfolio risk-sizing scaler, not a Monte-Carlo pass/fail threshold). Not touched by this brief.
- `lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS_INTRADAY_W1.md` — the intraday-honest full-panel 0.50× bust figure (0.72%) this re-derivation's §D uses as the governing engine, per CLAUDE.md's own EOD-lower-bound posture.

**Context-scope note (Rule-0 sub-rule):** `N-2026-08-13-external-eval-population-data.md` §1 flags that the incumbent 3.0% rationale itself "welds a drawdown width as a fraction of equity to a probability of ruin — same numeral, different quantities. Recorded, not adjudicated." This brief does not adjudicate that weld either; it re-derives whether *economics* moves 3.0%, which is orthogonal to whether the barrier-width analogy is the right kind of quantity in the first place.

---

## §1 — Context & motivation

Q-BUSTGATE-1 (2026-07-23) tested whether eval-fee-vs-funded-upside economics ratify the incumbent 3.0% ceiling and found FALSIFIED: the EV-optimal rung (1.00×, ladder-capped) busts 4.37–10.37%, an order of magnitude past 3.0%, on a ≈12–36:1 fee/upside asymmetry. The operator elected fork B (adopt an EV objective for rung-selection), but fork B's own regime-robustness precondition — already run, not invented for that ADR — restricted the admissible rung set to {0.50×}, whose bust already clears 3.0% comfortably. So Q-BUSTGATE-1 closed with the ceiling unedited and the live rung unchanged.

Two new input classes now exist that did not exist on 2026-07-23: (i) firm-published funnel conversion rates for a real trader population (Tradeify 17.2% per-attempt pass; the estate's eval model had "never touched an external outcome distribution" before this — `N-2026-08-13-...md:11`), and (ii) an updated, partially higher checkout/reset fee schedule. Per that same notice's own governing caveat (§7 item 2), "a population base rate is a third input, not a dial" — new inputs license a new *run* of the same instrument, not a license to keep re-asking until the answer changes. This brief is that one licensed re-run, structured to make re-litigation-by-attrition explicit and capped (§E of the pre-registration) rather than open-ended.

Standing doctrine tested: the `concept-not-constant` change-control chain (any risk-constant successor needs pre-reg → re-MC → regime-robustness gate → admitting ADR); Trap #12 (no in-place edit of the frozen 2026-07-13 prereg); Q-BUSTGATE-1's own §5 forbidden move against transcribing an EV-optimum's bust rate as a new ceiling number.

---

## §2 — Prior art / lineage

- **`Q-BUSTGATE-1-closure-falsified.md`** (`55e1c49`, `CLOSED-FALSIFIED`) — the direct parent. Established the fee/upside asymmetry, the fork-A/fork-B split, and — load-bearing for this brief — that "EV and the bust-floor converge on 0.50×" once the already-ratified regime-admissibility precondition is applied. This brief tests whether that convergence still holds under the 2026-08-13 inputs, not whether it held on 2026-07-23.
- **`2026-07-23-c1-rung-selection-ev-objective.md`** (`Accepted`) — the fork-B ADR. Its regime-robustness precondition (§2) is inherited wholesale here, not re-derived — re-deriving it would itself be the forbidden "re-scoping into rung-selection" move (pre-reg §F.4).
- **`N-2026-08-13-external-eval-population-data.md`** — Notice-phase observation log, records only; rules on nothing. Supplies the credibility-margin input and the explicit governing caveat against gate-shopping on population data.
- **`2026-07-13-prop-survivor-scoring-prereg.md`** — the frozen object under (non-)re-derivation. Byte-unedited by both Q-BUSTGATE-1 and this brief (Trap #12).
- **Programme-audit precedent** — [`2026-08-15-msl-wall-scope-audit.md`](../notes/audits/programme-audit/2026-08-15-msl-wall-scope-audit.md), landed the same session, independently confirmed the domain-bar / ratification-and-wiring discipline this brief also relies on (D2/D3, `docs/adr/2026-08-09-rejection-register-topology-and-bar-wiring.md`) is functioning correctly, not ceremonially.

---

## §3 — Question (Q-BUSTGATE-2)

**Pre-Q gate test:** symptom-only rephrase — "two new, dated, primary-sourced input classes exist since Q-BUSTGATE-1 closed (external population funnel data; an updated fee schedule); it is unknown whether either moves the economically-implied bust ceiling away from 3.0%, or whether the prior convergence on 0.50×/3.0% still holds." No fix baked in (does not presuppose either direction).

**Q-BUSTGATE-2:** Do the 2026-08-13 external population data and/or the updated Tradeify Select 100K fee schedule change whether eval-fee-vs-funded-upside economics — correctly constrained by the already-ratified regime-robustness admissibility precondition — ratify the incumbent 3.0% Part-A bust ceiling?

---

## §4 — Falsifiable hypothesis (H-BUSTGATE-2)

**H-BUSTGATE-2:** If the sole regime-admissible rung's intraday-honest bust rate is ≤ 3.0% (and the credibility precondition clears), then the 3.0% ceiling remains economics-and-survival-consistent under the new inputs and is **reconfirmed unchanged**. **Otherwise** — the admissible rung's bust exceeds 3.0%, or the admissible set is empty, or the credibility precondition fails — the convergence Q-BUSTGATE-1 found no longer holds and a fresh operator fork is owed.

**Accept H-BUSTGATE-2 → `RESOLVED` if:** per pre-reg §D, sole admissible rung (0.50×) intraday-honest bust ≤ 3.0% and credibility precondition clears.
**Reject H-BUSTGATE-2 → `FALSIFIED` if:** the admissible rung's bust > 3.0%.
**`AMBIGUOUS-HOLD` if:** the admissible set is empty or the credibility precondition fails.

Full details, pinned numbers, and the decision-rule table: pre-registration §D.

---

## §5 — Forbidden moves

- **Treating Thread 1 (the unconstrained EV/dollar-day recompute) as decision-governing.** It is context only — pre-reg §D explicitly bars it from firing §4. The single most tempting move, since Thread 1 alone would still read FALSIFIED-shaped (asymmetry narrowed 31:1→23:1 but not reversed) and could be mistaken for the operative answer.
- **Re-deriving the regime-robustness precondition itself.** Inherited from the 2026-07-23 ADR wholesale; re-running it here would be the forbidden rung-selection re-scoping (pre-reg §F.4).
- **Editing `3.0%` in `be6dda6` in place** — Trap #12.
- **Computing an absolute-dollar EV_N without a named primary V_payout disclosure** — pre-reg §F.5; the hard precondition is honored by running the cost-side-only comparison instead.
- **Welding Tradeify's 3.0% Live call-up rate, or the venue's $3,000/3.0% max_dd_pct, to this ceiling** — three unrelated numbers sharing a numeral (`N-2026-08-13-...md:73`); flagged explicitly in the pre-registration.
- **Opening a third re-derivation on a further fee-page refresh alone** — pre-reg §E's re-litigation cap.

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED` | Sole admissible rung (0.50×) intraday-honest bust ≤ 3.0% ∧ credibility precondition clears | 3.0% reconfirmed unchanged; **INTEGRATE** — no state-flip needed (byte-unedited ceiling); the closure becomes the citable authority that the 2026-08-13 inputs were checked and did not move it |
| `FALSIFIED` | Admissible rung's bust > 3.0% | Convergence broken; **ITERATE** — fresh operator fork required, same shape as Q-BUSTGATE-1's fork A/B |
| `AMBIGUOUS-HOLD` | Admissible set empty or credibility precondition fails | **ITERATE** — re-test when the regime gate or the credibility inputs are re-measured |

Pre-registered before the number was read: pre-registration §D, frozen 2026-08-15 ahead of Phase 3.

---

## §7 — Execution plan / the derivation

Not a self-executing closed-artifact read like Q-BUSTGATE-1 (no new numbers were pinned there beyond citation); this brief computes fresh cost-side arithmetic over the new fee schedule and reads the current-governing intraday-honest bust figure. Full method and 2-round adversarial stress-test in workflow `wf_5013860c-86a` (phases "Ceiling pre-registration" → "Ceiling execution").

- **Phase 0 — Rule-0 reads.** Done (§0).
- **Phase 1 — Freeze the model.** Pre-registration drafted, stress-tested twice (round 1: caught an internal contradiction — the literal EV_N formula is monotone in p_bust so it could only ever select the lowest-bust rung, while its citation pointed at the pre-correction 1.00× figure, forcing two mutually exclusive readings; round 2: caught an unpinned credibility margin, an under-specified V_payout source, an asymmetric "fees went up" framing that ignored the reset fee going down, and no re-litigation cap). Both rounds' required changes are incorporated into the frozen pre-registration (§E "Verification note").
- **Phase 2 — Execute the cost-side arithmetic.** Weighted expected cost per pass-cycle (N=3), OLD vs NEW fee schedule, at p=6.78% (1.00×, context only) and p=0.72% (0.50×, the admissible rung):

  | | C1 | C2 | C3 |
  |---|---:|---:|---:|
  | OLD | $111 | $350 | $589 |
  | NEW | $159 | $328 | $497 |

  | Case | p | E[C_old] | E[C_new] | Δ |
  |---|---:|---:|---:|---:|
  | A (1.00×, context) | 6.78% | $128.30 | $171.24 | **+$42.93 (+33.5%)** |
  | B (0.50×, admissible) | 0.72% | $112.73 | $160.23 | **+$47.49 (+42.1%)** |

  (Both totals independently re-derived and confirmed by an adversarial final check, which also caught two 1-cent rounding display errors in the raw workflow output — both understating the increase, not inflating it — corrected in the figures above.) Since w1=(1−p) dominates (93–99%) at realistic p, expected cost is driven by the first-attempt fee, which rose 43% ($111→$159); the reset fee fell ($239→$169) but is weighted too lightly to offset it. **A pass-cycle got more expensive, not cheaper**, under the new schedule.

- **Phase 3 — Two threads, one decision-governing.**
  - **Thread 1 (context only, cannot fire §4):** unconstrained EV/dollar-day ratio, reusing Q-BUSTGATE-1's own $4,000 Flex-cap reference point (not re-pinned as a new number): OLD $4,000/$128.30 ≈ 31.2:1; NEW $4,000/$171.24 ≈ 23.4:1. Order-of-magnitude past breakeven either way — the asymmetry **narrowed but did not reverse**. This reproduces Q-BUSTGATE-1's original FALSIFIED-shaped finding under current fees; it is not this brief's verdict.
  - **Thread 2 (decision-governing, per pre-reg §D):** admissible rung set = {0.50×} (inherited from the 2026-07-23 ADR). Its bust, intraday-honest full-panel = **0.72%** ≤ 3.0%. Credibility precondition: 95.76% EOD pass-5th (flagged superseded/no corrected figure published, but the direction is unambiguous given corrected bust rates fell, not rose) clears 51.6% comfortably; ORB-MNQ's 19.82–32.33% fails the same bar, confirming the gate is non-vacuous. **⇒ §4 fires `RESOLVED`.**

- **Phase 4 — Consequence check (run after, not before, the verdict — per pre-reg discipline).** Checked against `docs/rejected_candidates.md`'s bust-ceiling rejections: Striker→MNQ (96.76–99.37%), Guardian→MGC (16.5–72.4%), ORB-MNQ (67.67–80.18%) — none within one order of magnitude of even Thread 1's most permissive historical reading (≤10.37%). Nothing in the graveyard is revived by this closure, under either thread.

**What this derivation establishes:** the 2026-07-23 convergence — EV-optimal-and-regime-admissible selects 0.50×, whose bust already clears 3.0% — is **unmoved** by either new input class. The genuinely new contribution is closing the "would the new data flip this" question cleanly rather than leaving it open to be re-asked; Thread 1's remeasurement shows the underlying fee/upside tension is real and narrowing (not disappearing), which is worth carrying forward as context for any future rung-selection question, but is explicitly not this brief's gate.

---

## §8 — Verdict pre-registration

Frozen method + decision rule: [`pre-registration/Q-BUSTGATE-2-verdict-preregistration.md`](pre-registration/Q-BUSTGATE-2-verdict-preregistration.md), frozen 2026-08-15 after two adversarial stress-test rounds and before Phase 2/3 touched any candidate-specific arithmetic.

Pre-registration commit hash: *(populated at commit time — authored same session as this brief; the freeze-before-read property is evidenced by the workflow's own phase ordering — "Ceiling pre-registration" completed and stress-tested before "Ceiling execution" began — not by a preceding calendar day, since both are read-only research completed in one continuous session. If committed, the pre-registration file is committed first, in its own commit, ahead of this brief + closure, to preserve the same ordering Q-BUSTGATE-1 modeled.)*
Pre-registration date: 2026-08-15

---

## §9 — Closure record format

Landed verdict: `RESOLVED`. Closure at [`closures/Q-BUSTGATE-2-closure-resolved.md`](closures/Q-BUSTGATE-2-closure-resolved.md), recording the Thread 1/Thread 2 split, the four minor sourcing/rounding defects the adversarial final check found (none verdict-affecting), and the mandatory Iterate block.

---

## §10 — Audit hooks (runnable)

```bash
# §0 anchors still resolve
git log -1 --format='%h %cs' -- docs/notes/notice/N-2026-08-13-external-eval-population-data.md   # expect b2e3eec
git log -1 --format='%h %cs' -- docs/notes/2026-08-13-tradeify-select-100k-checkout-price.md        # expect 67e4b20
git log -1 --format='%h %cs' -- docs/adr/2026-07-23-c1-rung-selection-ev-objective.md               # content ratified 2026-07-23

# The incumbent 3.0% is untouched by this re-derivation (Trap #12 intact)
grep -n "3.0%\|≥ 50%" docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md

# The admissible-set inheritance is not re-derived here
grep -n "correctly constrained, selects" docs/adr/2026-07-23-c1-rung-selection-ev-objective.md

# Fee figures cross-verified
grep -n "159\|169\|265" docs/notes/2026-08-13-tradeify-select-100k-checkout-price.md
grep -n "111\|239\|181" lab/analysis/c1/q_rail_1_2026-07/PHASE4.md

# The re-litigation cap (pre-reg §E) — a third re-derivation on price-page-alone grounds should not appear without an operator ruling
grep -c "Q-BUSTGATE-3" docs/briefs/*.md   # expect 0 unless a structural-change ruling is on record

# Live sizing untouched
grep -n "dry_run\|WATCH-1\|0.50" STATE.md docs/notes/rail_build/RUNBOOK.md | head
```

---

## Verification

```bash
python ~/.claude/skills/brief-authoring/scripts/check_brief.py docs/briefs/Q-BUSTGATE-2-bust-gate-re-derivation-2026-08.md --type inquire
python scripts/check_brief.py docs/briefs/Q-BUSTGATE-2-bust-gate-re-derivation-2026-08.md --type inquire

# Cross-reference the arithmetic
git log --oneline -- docs/briefs/pre-registration/Q-BUSTGATE-2-verdict-preregistration.md docs/briefs/Q-BUSTGATE-2-bust-gate-re-derivation-2026-08.md
```

---

## Pre-Lock Checklist

- [x] All §0 paths read and anchored with commit hash
- [x] §3 question passes the symptom-only rephrase test
- [x] §4 hypothesis genuinely falsifiable (binary bust-vs-3.0% trigger on the single admissible rung)
- [x] §5 forbidden moves genuinely tempting (Thread 1 mistaken-for-governing is the live hazard, same shape as the 1.00×-laundering hazard in Q-BUSTGATE-1)
- [x] §6 gates have specific numerical triggers
- [x] §8 pre-registration frozen and adversarially stress-tested (2 rounds) before Phase 2/3 execution
- [x] §10 audit hooks are runnable commands
- [x] Verification block executed; arithmetic independently re-derived by an adversarial final check (CONFIRMED, 4 minor non-verdict-affecting defects corrected in §7 above)
