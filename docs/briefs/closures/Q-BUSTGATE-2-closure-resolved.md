# Q-BUSTGATE-2 — CLOSURE: `RESOLVED` (3.0% reconfirmed unchanged under the 2026-08-13 inputs)

**Verdict:** `RESOLVED` — the sole regime-admissible rung (0.50×) clears the 3.0% ceiling on the intraday-honest clock; neither the new population data nor the updated fee schedule moves it
**Closed:** 2026-08-15
**Lane:** UNASSIGNED
**Pre-registration:** [`Q-BUSTGATE-2-verdict-preregistration.md`](../pre-registration/Q-BUSTGATE-2-verdict-preregistration.md) — frozen after 2 adversarial stress-test rounds, ahead of Phase 2/3 execution
**Successor:** none named — pre-registration §E caps a third re-derivation absent a structurally new input class
**Spend / K:** $0.00 · K consumed: 0 (cost-side arithmetic + closed-artifact reads; no new MC run, no Databento spend)
**Live effect:** none — the frozen 2026-07-13 pre-registration's 3.0%/50% thresholds are byte-unedited; live rung stays WATCH-1 0.50×, rail stays disarmed
**Artifacts:** [parent brief](../Q-BUSTGATE-2-bust-gate-re-derivation-2026-08.md) · [pre-registration](../pre-registration/Q-BUSTGATE-2-verdict-preregistration.md)

---

## 1. Verdict (§6 asserted against actual numbers)

| §6 route | Trigger | Actual | Fired? |
|---|---|---|---|
| `RESOLVED` | Sole admissible rung (0.50×) intraday-honest bust ≤ 3.0% ∧ credibility precondition clears | 0.50× intraday-honest full-panel bust = **0.72%**; credibility precondition clears (95.76% EOD pass-5th, superseded-figure caveat noted, ≫ 51.6% floor; ORB-MNQ's 19.82–32.33% correctly fails the same bar) | ✓ |
| `FALSIFIED` | Admissible rung's bust > 3.0% | not reached | — |
| `AMBIGUOUS-HOLD` | Admissible set empty or credibility precondition fails | not reached (admissible set = {0.50×}, non-empty; precondition clears) | — |

**Thread 1 (context, non-decision-governing, reported per pre-reg §D):** the unconstrained EV/dollar-day objective — Q-BUSTGATE-1's original framing, ignoring the regime-admissibility precondition — still points looser than 3.0% under the new fee schedule: expected cost per pass-cycle (N=3) rose from $128.30 to $171.24 (+33.5%) at the 1.00× rung's context-only bust rate (6.78%, EOD-corrected, no intraday-honest full remeasure exists), narrowing the fee/upside ratio from ≈31.2:1 to ≈23.4:1 — still an order of magnitude past breakeven, unreversed. This reproduces, not overturns, Q-BUSTGATE-1's original finding; it is explicitly barred from firing §4 (pre-reg §F.6).

## 2. What the pre-registration predicted vs what happened

The pre-registration's own "pinned ex-ante expectation" (§D) stated: given the admissible set collapses to a single member whose bust is already an order of magnitude inside 3.0%, the expected outcome is RESOLVED by construction of the already-ratified 2026-07-23 regime-robustness precondition, "not because this artifact discovers anything new about economics." That is exactly what happened — no surprise. The two things that *could* have surprised (a material intraday-honest bust increase at 0.50×, or a change to the admissible set itself) did not occur.

## 3. What this closure does NOT license

- Treating Thread 1's narrowed-but-unreversed asymmetry as grounds to revisit rung selection — that question is owned by the 2026-07-23 ADR, not reopened here.
- Reading this closure as new economic justification for 1.00× — the regime-robustness precondition that excludes it from the admissible set is untouched.
- A third re-derivation triggered by a further fee-page refresh alone (pre-reg §E).
- Citing this closure as evidence that eval-fee-vs-funded-upside economics *generally* favor tight ceilings — the opposite is true (Thread 1); this closure's RESOLVED verdict is entirely a consequence of the regime-admissibility inheritance, not of the economics recomputation.
- Any state-flip to `core/`, `dd_protection.py`, `firm_rules.py`, or the live rail — none occurred, none is licensed by a RESOLVED-and-unedited verdict.

## 4. Defects found in the frozen brief (recorded, not repaired)

Four minor sourcing/rounding defects, caught by the adversarial final-check stage, none verdict-affecting:

1. Two 1-cent display-rounding errors in the raw execution's E[C_new] totals ($171.23 displayed vs. $171.235066 precise → $171.24; $160.22 vs. $160.225561 → $160.23) — corrected in the parent brief's §7 table. Both errors understated, not inflated, the "fees got more expensive" finding.
2. A wrong line-number citation for the 4.37%/10.37% figures (cited at Q-BUSTGATE-1 closure line 13; the figures are actually at line 18 — line 13 carries the *corrected*-pins banner instead). The numbers themselves are real and unaffected.
3. The 51.6% credibility-margin floor was initially stated without an inline citation in the raw execution trace; traced to `N-2026-08-13-external-eval-population-data.md:25` and now cited explicitly in the frozen pre-registration.
4. The 0.50×'s 95.76% pass-5th figure is sourced from a campaign RESULTS.md that carries its own `⛔ SUPERSEDED` banner (defective `dd_lock_offset_usd` input); no corrected pass-5th is published anywhere in that campaign. The direction is unambiguous (corrected bust rates fell, not rose, so the true corrected pass-5th almost certainly still clears comfortably) but the specific cited figure is not currently clean — flagged explicitly in both the pre-registration and this closure rather than passed silently.

## 5. Lesson candidates

Below the two-incident bar — watch: a second consecutive instance (after Q-BUSTGATE-1) of "the unconstrained EV objective always reads looser than the survival gate, and the regime-robustness precondition is what actually resolves the tension, not the economics recomputation itself." If a third re-derivation is ever licensed under pre-reg §E's structural-change bar, this pattern is worth stating as a standing expectation up front rather than re-discovering.

## Iterate — loop exit

- **Verdict used:** `RESOLVED`
- **Model update:** Q-BUSTGATE-1 left the ceiling-vs-economics tension formally open pending a fresh fork if new inputs arrived. This closure shows the tension was already resolved *structurally* by the 2026-07-23 regime-robustness precondition, and that resolution is robust to two independent new input classes (population data, fee schedule) — the prior finding was not a fragile coincidence of 2026-07-23's specific numbers.
- **Next:** INTEGRATE
- **Routing:** INTEGRATE → no commit beyond this closure record itself. No ADR, no state-flip, no `core/` edit — the 3.0% ceiling and the WATCH-1 0.50× rung both stand exactly as before. The closure record becomes the citable authority that the 2026-08-13 inputs were checked and did not move the ceiling, closing off informal re-litigation via those specific inputs without requiring a fresh ADR to say so.
- **Entry packet:** n/a — no successor opened. If a genuinely new input class (new venue, new instrument, new mechanism-level evidence — not another price-page refresh) later licenses a third re-derivation, its entry packet must carry forward: the regime-admissibility inheritance (do not re-derive it), the estimand-mismatch firewall (population data is never a p_bust substitute), and Thread 1's narrowed-not-reversed asymmetry as prior context.
- **Stop rule / re-proposal bar:** per pre-reg §E — a further re-derivation on price-page or population-data-refresh grounds alone is out of scope absent an explicit operator ruling naming a structural change (new venue, new instrument, new mechanism class). This is the SNAG-exhaustion pattern applied prospectively: two clean re-derivations (Q-BUSTGATE-1, Q-BUSTGATE-2) both converging on the same answer is itself evidence the question is answered for now, not evidence to keep re-asking it.
- **Board write:** `SESSIONS Open/next: Q-BUSTGATE-2 RESOLVED — 3.0% ceiling reconfirmed unchanged under 2026-08-13 population/fee data; no third re-derivation absent a structural-change ruling (pre-reg §E).` Owner: this closure · [parent brief](../Q-BUSTGATE-2-bust-gate-re-derivation-2026-08.md)
- **Registry:** n/a — threshold re-derivation, not a strategy-grounds kill. No candidate was scored or rejected; the 3.0% ceiling was reconfirmed **unchanged**, so nothing is added to or removed from `rejected_candidates.md`. The Phase-4 consequence check confirmed no existing graveyard entry flips disposition.

## §10 audit-hook discharge

```
git log -1 --format='%h %cs' -- docs/notes/notice/N-2026-08-13-external-eval-population-data.md
b2e3eec 2026-08-13

git log -1 --format='%h %cs' -- docs/notes/2026-08-13-tradeify-select-100k-checkout-price.md
67e4b20 2026-08-13

grep -n "3.0%\|≥ 50%" docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md
# 3.0% / 50% still there, unedited — Trap #12 intact

grep -n "correctly constrained, selects" docs/adr/2026-07-23-c1-rung-selection-ev-objective.md
# regime-admissibility inheritance confirmed cited, not re-derived
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-15 | Closure authored | Joshua + Claude Code |

---

## Verification

```bash
python scripts/check_closure_disposition.py docs/briefs/closures/Q-BUSTGATE-2-closure-resolved.md
grep -c "Fired?" docs/briefs/closures/Q-BUSTGATE-2-closure-resolved.md
```
