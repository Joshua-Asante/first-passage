# Q-ORBCUSH-1 — Does a trailing edge/cost-fraction classifier explain ORB-MNQ-1's 2021-09-28 cushion-sizing regime break?

**Status:** `OPEN — DRAFT (pre-lock)`
**Authored:** 2026-08-20
**Closed:** N/A
**Authors:** Joshua + Claude Code (Sonnet 5) — informal probe work 2026-08-19/20, this brief drafted 2026-08-20
**Parent question:** N/A — not forked from a gated parent, but see §2 for the Q-EVALSEQ-1/Q-POLFRONT-1 relationship this pivots away from
**Sub-questions opened:** N/A
**Loop:** Inquire-phase Pre-Q — gates whether a real, causally-tested mechanism exists behind ORB-MNQ-1's 2021-09-28 cushion-sizing regime break, before any deployment-adjacent decision treats that break as more than an unexplained historical pattern
**Artifact path:** `docs/briefs/Q-ORBCUSH-1-regime-break-mechanism.md`

---

## §0 — Rule 0 reads (production-source verification)

- `lab/analysis/c1/q_evalseq_1_2026-08/run_evalseq.py` — anchor `a7c6f7b` (`git log -1`, 2026-08-16). Source of `pol_cushion`, the cushion-proportional sizing policy this whole thread tests.
- `core/mc/simulation.py` — anchor `027a729` (2026-08-14). `simulate_path`'s `intraday_low=` mechanism, the already-validated intraday-honest engine ORB-MNQ-1's own bust figures use.
- `lab/analysis/orb/orb_mnq_2026-07/RESULTS_t2_intraday_bust.md` — anchor `027a729` (2026-08-14). Published intraday-honest bust rates (k=1 67.67%, k=2 77.01%) this thread's fidelity control reproduces to ~0.00pp.
- `lab/analysis/orb/orb_mnq_2026-07/RESULTS.md` — anchor `027a729` (2026-08-14). ORB-MNQ-1's own per-year meanR table and Stage-2 cost-law figures (5.31×/8.10×).
- `docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md` — anchor `027a729` (2026-08-14). The frozen survivor-scoring gate (bust ≤ 3.0% AND P(pass) ≥ 50%) this whole investigation's gate-clearance checks are measured against; the ADR that re-`PARK`ed ORB-MNQ-1 as a payable Tradeify leg on exactly this bar.
- `docs/briefs/closures/Q-EVALSEQ-1-closure-falsified.md` — anchor `a7c6f7b` (2026-08-16). Source of the surviving finding (cushion sizing eliminated bust 20.18%→0.00% on a different, 2-leg pyramided book) and the commissioned-but-unopened `Q-POLFRONT-1` successor this Q pivots away from — see §2.
- `docs/briefs/closures/Q-GEOFIT-1-closure-ambiguous-parameterization.md` — anchor `027a729` (2026-08-14). Source of the skew methodology this thread's earlier probe step reused, and the standing lesson that trailing-DD survival is governed by loss-tail shape.

---

## §1 — Context & motivation

An informal, three-round $0/K=0 probe (2026-08-19/20, this session — not itself pre-registered; see §2) applied Q-EVALSEQ-1's cushion-proportional sizing policy to ORB-MNQ-1's own already-validated intraday-honest bust engine. Two things came out triple-independently-verified: (1) bust elimination is mathematically real and regime-agnostic — a direct consequence of the sizing throttle's ceiling versus ORB's hard-stopped worst-day loss, holding in every time slice and every volatility bucket tested; (2) a real, non-boundary-luck regime break in the *pass rate* sits at approximately 2021-09-28 — before that date the construct fails the frozen Tradeify survivor-scoring gate badly (pass 0.5–2.9%), after it, every sub-window tested clears the gate independently (pass 54–90%). A trailing, causally-computed (no look-ahead) volatility-regime classifier was tested against this break and **REFUTED** as the mechanism — clean at long windows only because long windows increasingly just re-smooth toward the calendar cut (circular), and the separation direction sign-flips at a shorter, equally defensible window (20 trading days).

This repo's standing doctrine (`lesson_regime_directional_graveyard.md`, `lesson_regime_detectability_wall.md`) treats an unexplained regime split as real but non-actionable until a plausible mechanism is proposed and survives the same falsification discipline. The probe's own synthesis named the next candidate: ORB-MNQ-1's own mean-R goes from near-zero (+0.0076R) pre-break to solidly positive (+0.0901R) post-break — edge itself tracks era far more tightly than instantaneous trailing volatility does. That candidate has not been tested. This brief opens that test formally.

---

## §2 — Prior art / lineage

- **Q-EVALSEQ-1** (`CLOSED-FALSIFIED` on its own headline question; `docs/briefs/closures/Q-EVALSEQ-1-closure-falsified.md`) — surviving finding: cushion-proportional sizing eliminated trailing-DD bust (20.18%→0.00%) on a 2-leg pyramided Striker DJ30/MYM + NAS100/MNQ book, on an EOD-clock-only simulator. Commissioned `Q-POLFRONT-1` as its successor, reframed around that book's own admissible-region widening.
- **[CORRECTED 2026-08-20]** An earlier version of this bullet stated "`Q-POLFRONT-1` remains unopened" and described this probe's own `NOT-REACHABLE-AT-$0` finding as belonging to `Q-POLFRONT-1`. Both were wrong. `Q-POLFRONT-1` (`docs/briefs/closures/Q-POLFRONT-1-closure-resolved-quantified.md`) opened, ran, and **closed `RESOLVED-QUANTIFIED` on 2026-08-16** — it tested whether cushion-proportional sizing widens the admissible base-R frontier on a **synthetic, candidate-independent `(w,b,r,k)` geometry grid**, not the real 2-leg book's actual historical data. Median widening: 5.1× on the EOD clock. **A 2026-08-17 addendum (operator GO) executed the intraday-honest remeasurement named-but-unopened in that closure's own §7, and found the 5.1× ratio does NOT survive** — policy-arm median bust delta +98.1pp, only 1/26 cells still clear the 3.0% ceiling; independently reproduced and adversarially verified `SAFE_WITH_CAVEATS` (no coding defect; two confirmed calibration biases both push toward *overstating* risk, so read as a credible upper bound). This is directly relevant caution for the whole cushion-sizing thread: a state-dependent throttle's admissible-region gain and its EOD-clock fragility "move in the same direction... both scale with how close to the barrier the policy operates by design" (that closure's own §5). What this probe actually attempted and found `NOT-REACHABLE-AT-$0` was a *different*, never-formally-opened thing: a literal re-derivation of Q-EVALSEQ-1's own specific historical result on the real 2-leg book's real data, intraday-honestly — that book has no per-day intraday-excursion data and would need position-ladder reconstruction across two pyramided, cross-instrument legs, correctly declined rather than faked. **Why this Q's own ORB-MNQ-1 bust-elimination finding is not automatically subject to Q-POLFRONT-1's collapse:** every bust-rate figure in this probe was computed on the intraday-honest engine from the start (fidelity-gated against `RESULTS_t2_intraday_bust.md`'s own published *intraday-honest* numbers), not an EOD number later found to erode — the opposite order of operations from `Q-POLFRONT-1`'s original sweep. The underlying mathematical bound (§B5 of the probe's earlier draft artifact) also holds under the *theoretical* worst-day-loss estimate (~$1,250/contract, from an unstopped held day, per the first probe round's own verification) as well as the *empirical* one (−$783.82/contract): `0.75 × 1250 × 2 / 3000 ≈ 0.625 < 1` even at k=2. This reasoning is the author's own re-derivation from already-twice-verified numbers, not itself a fresh independently-verified round — flagged at that confidence level rather than asserted flatly.
- **`docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md`** (`Accepted`) — the frozen gate (bust ≤ 3.0% AND P(pass) ≥ 50%) every gate-clearance check in this thread is measured against. Re-opening ORB-MNQ-1 as a payable Tradeify leg needs a fresh operator GO plus a superseding ADR "not automatic" (§4 R2) — nothing in this Q licenses that on its own, regardless of verdict.
- **`Q-GEOFIT-1`** (`CLOSED-AMBIGUOUS-PARAMETERIZATION`) — established that trailing-DD survival is governed by the loss-tail *shape* of the daily distribution, not mean/vol, and supplied the skew methodology this probe's earlier step reused to confirm ORB-MNQ-1's own distribution (+2.09 skew, ~42% weaker than the book Q-EVALSEQ-1's original headline came from) is in the same qualitative family but quantitatively thinner.
- **This Q's own immediate lineage is the informal probe itself** (2026-08-19/20, three rounds, each independently adversarially verified — build+measure → thirds robustness split → trailing-vol mechanism test), preserved at `lab/analysis/c1/orbmnq1_cushion_sizing_probe_2026-08-20/`. That probe was exploratory and iterative, not pre-registered before it ran — appropriate for informal $0 characterization work, but it means none of its own findings are being treated here as more than motivating context. Only the specific test opened below is pre-registered before execution.
- **Empty-lineage note:** N/A — real prior art exists and is cited above.

---

## §3 — Question (Q-ORBCUSH-1)

**Pre-Q gate test:** symptom-only rephrase — "what explains the pass-rate regime break, and is there a real, causally-tested mechanism behind it" — names the symptom (an unexplained break) and the missing thing (a tested mechanism), not a specific fix. Passes.

**Q-ORBCUSH-1:** Does a trailing, causally-computed classifier of ORB-MNQ-1's own realized trade-level edge (mean-R) or its cost-to-range fraction — as opposed to volatility level, which was already refuted — produce regime buckets whose date composition and gate-clearance direction track the observed 2021-09-28 break, or does the break remain mechanistically unexplained?

---

## §4 — Falsifiable hypothesis (H-ORBCUSH)

**H-ORBCUSH:** If a trailing (strictly causal — computed only from trades/days at or before the point being classified, `.shift(1)`-equivalent, no full-sample or global-percentile threshold), pre-registered-window classifier of ORB-MNQ-1's own realized mean-R (primary) or cost-to-range fraction (secondary, if mean-R is ambiguous) produces two regime buckets such that, at **at least 2 of 3 pre-registered window lengths**: (a) the higher-edge bucket's post-2021-09-28 date fraction is **≥ 75%**, (b) the lower-edge bucket's post-2021-09-28 date fraction is **≤ 40%**, and (c) the gate-clearance direction (higher-edge bucket clears the frozen bust≤3.0%/pass≥50% gate under cushion sizing, lower-edge bucket does not) is the **same sign at every window tested, no exceptions** — **then** the mechanism is SUPPORTED, and the 2021-09-28 break has a real, edge-level explanation, not just a date; **otherwise** (date-correlation fails threshold at ≥2 of 3 windows, OR the gate-clearance direction sign-flips between any two tested windows, mirroring exactly what refuted the volatility hypothesis) the mechanism is REFUTED, and the break stays an unexplained historical pattern.

**Reject H-ORBCUSH if:** the direction sign-flips between any two of the three pre-registered windows (a single sign-flip is disqualifying, regardless of what the other windows show — this is the exact criterion that correctly refuted the volatility hypothesis and must not be loosened here), OR date-correlation fails the (a)/(b) thresholds at 2 or more of the 3 windows.

**Accept H-ORBCUSH if:** date-correlation clears (a)/(b) at ≥2 of 3 windows AND the direction is stable (no sign-flip) across all three.

**Ambiguous-hold if:** a trade-level classifier (mean-R is measured per-trade, not per-day like volatility was — ORB-MNQ-1 trades on ~99% of sessions, so this is a minor distinction, but if session count within any pre-registered window is too sparse — n < 30 trades — for a stable rolling mean-R estimate) makes any of the three pre-registered windows structurally unreliable. Re-test window: fall back to cost-to-range fraction (computable at daily/session granularity, not trade-sparsity-limited) as the primary classifier instead, re-run this same H against thresholds unchanged, within the same brief (does not require a fresh Q).

---

## §5 — Forbidden moves

- **Picking the reported window after seeing which one "works."** Tonight's vol-regime test already demonstrated why this matters directly: 20d inverted the separation direction that 63d/126d showed, and 126d's apparent strength was itself circular (too few independent segments). All three windows are pre-registered below (§8) before Phase 1 runs; the verdict uses all three, not the best of three. Ruled out because it is the exact SNAG best-of-K pattern this repo already has a graveyard for.
- **Using a full-sample or global-percentile threshold to define the regime buckets.** Tempting because it's simpler to code and (per tonight's vol test) tends to produce a *cleaner*-looking date-correlation — but that cleanliness is itself the look-ahead artifact, not evidence. Ruled out; every classifier here must be strictly trailing, verified the same way tonight's vol classifier was (a second, independent implementation reproducing it bit-for-bit, per-window spot checks confirming no future data enters any day's value).
- **Treating a SUPPORTED verdict as license to open `Q-POLFRONT-1`, propose re-opening the `Accepted` 2026-08-03 re-`PARK` ADR, or take any deployment-adjacent action.** This Q is explanatory only — even a clean SUPPORTED result establishes a mechanism for a *historical* pattern, not a forward-looking, tradeable rule, and does not by itself license anything past what §6 states.
- **Treating a REFUTED verdict here as casting doubt on the bust-elimination finding or the 2021-09-28 break's own reality.** Those are separately, already triple-verified and regime-agnostic (bust) or robust-to-finer-splitting (the break itself). This Q tests one specific candidate *explanation* for the break; refuting it leaves the break exactly as real and exactly as unexplained as it was before this Q opened — not less real.
- **Forbidden D-test:** filtering to only the trades/days that fit a preferred mean-R story, then testing whether the filtered subset shows the regime pattern more cleanly. Categorically forbidden — it encodes the conclusion into the analysis.

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED` | H-ORBCUSH's Accept condition fires (§4) | `INTEGRATE — record the mechanism (mean-R or cost-fraction regime) in ops/instruments/MNQ.md as a new durable finding, cross-referenced from this closure; does NOT reopen Q-POLFRONT-1 or the re-PARK ADR by itself (§5)` |
| `FALSIFIED` | H-ORBCUSH's Reject condition fires (§4) | `STOP — the 2021-09-28 break stays recorded as a real, triple-verified, mechanistically-unexplained historical pattern in ops/instruments/MNQ.md; re-proposal bar = a genuinely different candidate mechanism, not a re-tuned window on mean-R/cost-fraction` |
| `AMBIGUOUS-HOLD` | Trade-sparsity condition fires per §4's Ambiguous-hold clause and the cost-fraction fallback also proves unreliable | `ITERATE — return target: a fresh Q naming a different classifier family entirely (not a re-tune of this one); re-test window 2026-11-08 (co-scheduled with the quarterly programme audit, per this repo's standing cadence)` |

---

## §7 — Execution plan

Self-executing — small, mechanical, reuses the already-verified harness at `lab/analysis/c1/orbmnq1_cushion_sizing_probe_2026-08-20/run_evalseq_orb_intraday.py` (imported unchanged, not retyped, per §5).

- **Phase 0 — Rule-0 reads.** Confirm §0 anchors still resolve (§10 hook). Confirm the probe directory's harness and JSON results are present and match this brief's cited numbers.
- **Phase 1 — Trailing mean-R classifier.** Compute ORB-MNQ-1's own realized per-trade R at three pre-registered windows (§8). Build regime buckets, strictly causal. Re-run the cushion-sizing gate-clearance check (import `day_loop_intraday`/`build_paths_orb`/`run_policy_orb`/`pol_cushion`/`pol_const` unchanged) per bucket, per window, at k=1 (the source-faithful base per the probe's own prior finding).
- **Phase 2 — Verification.** Independent adversarial re-derivation of the classifier (a second, separate implementation, not just a re-read — matching both prior rounds' discipline) and a fresh end-to-end re-run, before any verdict is trusted.
- **Phase 3 — Verdict assertion.** Run §6 against the actual §8-frozen thresholds; produce the closure artifact per §9.

---

## §8 — Verdict pre-registration (mandatory before Phase 1)

A separate file at `docs/briefs/pre-registration/Q-ORBCUSH-1-verdict-preregistration.md` contains the §6 table above plus the exact threshold numbers and the three pre-registered window lengths, committed **before** Phase 1 runs.

Pre-registration commit hash: `<populated at pre-registration commit time — see companion file, committed in the same batch as this brief>`
Pre-registration date: 2026-08-20

---

## §9 — Closure record format

- **If RESOLVED:** `docs/briefs/closures/Q-ORBCUSH-1-closure-resolved.md`
- **If FALSIFIED:** `docs/briefs/closures/Q-ORBCUSH-1-closure-falsified.md`
- **If AMBIGUOUS-HOLD:** `docs/briefs/closures/Q-ORBCUSH-1-closure-ambiguous.md`, explicit re-test trigger 2026-11-08

Closure must include the mandatory typed `## Iterate` block per `docs/adr/2026-08-04-iterate-closure-exit-mandatory.md`.

---

## §10 — Audit hooks (runnable)

```bash
# Confirm §0 anchors still resolve
git log -1 --format='%h' -- lab/analysis/c1/q_evalseq_1_2026-08/run_evalseq.py   # expect a7c6f7b
git log -1 --format='%h' -- core/mc/simulation.py                                # expect 027a729
git log -1 --format='%h' -- docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md  # expect 027a729

# Confirm the probe harness this brief builds on is present and untouched
git log -1 --format='%h' -- lab/analysis/c1/orbmnq1_cushion_sizing_probe_2026-08-20/run_evalseq_orb_intraday.py

# Confirm the frozen gate this thread measures against
grep -n "bust.*3.0%\|P(pass).*50%" docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md

# Re-run the gate-firing assertion once Phase 1 lands (path TBD at Phase 1 authoring time)
# python lab/analysis/c1/q_orbcush_1_2026-08/run_mean_r_regime_gate.py --reproduce-q-orbcush-1

# Pre-registration commit predates Phase 1 — check ordering once Phase 1 has run
git log --oneline -- docs/briefs/pre-registration/Q-ORBCUSH-1-verdict-preregistration.md
```

---

## Verification

```bash
$ python C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py docs/briefs/Q-ORBCUSH-1-regime-break-mechanism.md --type inquire
# Expected: all 6 checks PASS

# §0 anchors
git log -1 --format='%h' -- lab/analysis/c1/q_evalseq_1_2026-08/run_evalseq.py
git log -1 --format='%h' -- core/mc/simulation.py
git log -1 --format='%h' -- lab/analysis/orb/orb_mnq_2026-07/RESULTS_t2_intraday_bust.md
git log -1 --format='%h' -- docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md
git log -1 --format='%h' -- docs/briefs/closures/Q-EVALSEQ-1-closure-falsified.md
git log -1 --format='%h' -- docs/briefs/closures/Q-GEOFIT-1-closure-ambiguous-parameterization.md

# Pre-registration commit verification (run after the pre-reg file is committed)
git log --oneline docs/briefs/pre-registration/Q-ORBCUSH-1-verdict-preregistration.md
```

---

## Pre-Lock Checklist (DRAFT — remove once locked)

- [x] All §0 paths read and anchored with commit hash
- [x] §3 question passes the symptom-only rephrase test
- [x] §4 hypothesis is genuinely falsifiable (binary triggers in §6, same discipline already proven out tonight)
- [x] §5 forbidden moves are genuinely tempting (each one is a trap this exact investigation already hit or narrowly avoided)
- [x] §6 gates have specific numerical triggers
- [ ] §8 pre-registration committed BEFORE Phase 1 runs — **companion file authored in this same batch, not yet executed against**
- [x] §10 audit hooks are runnable commands
- [ ] Verification block executed and passing — run `check_brief.py` before treating this as locked
