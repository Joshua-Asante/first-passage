# Pre-Q Brief — Q-JOINT-TAIL-WEEKLY

**Brief ID:** `2026-05-27-q-joint-tail-weekly-pre-q`
**Q-ID:** `Q-JOINT-TAIL-WEEKLY`
**Domain:** Portfolio
**Reversibility:** Medium (Inquire-phase; produces evidence, not changes)
**Authored by:** claude.ai (Tech Advisor)
**Date authored:** 2026-05-27
**Phase:** Pre-Q gate (D-S-A check before authoring CC handoff execution brief)
**Predecessor closure:** `archive/docs/briefs/Q-JOINT-TAIL-1-closure.md` (BLOCKED-RETIRED at daily resolution)

---

## §0 Production Reads (Rule-0)

Same Tier 1 / Tier 2 set as Q-JOINT-TAIL-1 rev 3, with one addition for the weekly aggregation. CC handoff brief (authored if Pre-Q PASSes) will re-anchor hashes at that point.

### Tier 1

| File | Verified hash (carried from Q-JOINT-TAIL-1 rev 3) | Why |
|---|---|---|
| `config/params.toml` | `92da2c986f...` | Allocation manifest |
| `portfolio_mc.py` | `63ed41e51a...` | MC anchor source. **New required read for this brief:** `:354-361` (`build_week_blocks`) — Monday-anchored 5-day block construction confirms weekly is the *natural* MC aggregation unit |
| `dd_protection.py` | `5b8ff716fc...` | C2 protection context |
| `docs/adr/2026-05-23-allocation-refresh-2.md` | `5b8ff716fc...` | Current canonical lock |
| `docs/adr/2026-05-16-fixture-test-requirement.md` | `b1d2a10a3c...` | Fixture mandate |
| `CLAUDE.md` (§Strategy Reference + §Protection + panel range) | (commit head) | 227 week-blocks confirmed |

### Tier 2

Same 4 CSVs at the 2026-05-24 hashes (per Q-JOINT-TAIL-1 rev 3 Tier 2 table).

### Tier 3

- claude.ai artifact: "Strategy-Output Relationship Analysis: Four Locked Systematic Strategies Inquire-Phase Q-Pack" (2026-05-22)
- Notion Methodology Canon (`34ddc0b53c1181479d7bdecc61f47078`)
- Q-JOINT-TAIL-1 closure note (`archive/docs/briefs/Q-JOINT-TAIL-1-closure.md`) — **load-bearing for context**

### Tier 4

- 2026-04-25 panel analysis (lag-5 volatility clustering in gold and US30) — tests MC's I1 temporal independence; directly relevant context for why weekly resolution matters

---

## §1 Context: Why this Q, why now

Q-JOINT-TAIL-1 was BLOCKED-RETIRED 2026-05-27 (CC Phase 0) because the four-strategy portfolio is temporally diversified at the day-of-week level by construction: only 1 of 1141 bdays had all four strategies active, and 0 of 115 bottom-decile days. The daily-resolution version of the hedge-need question is structurally non-falsifiable for this allocation.

But this surfaces the sharper question at the resolution where MC's max_dd statistic actually compounds losses: **week-block resolution.** A bad week can have all four strategies contributing losses on different weekdays without sharing a single day — Guardian Monday, NAS100 Tuesday, DJ30 Friday, Aegis Wednesday. That is invisible at daily resolution and exactly what MC's max_dd captures across simulated paths.

The 2026-04-25 panel-analysis found lag-5 volatility clustering in gold and US30 — that's autocorrelation evidence that bad days cluster within weeks. Combined with Q-JOINT-TAIL-1's finding (daily co-failure is unmeasurable), the picture motivates testing joint-tail at weekly resolution, where:

1. Strategies overlap by construction (every strategy trades within most weeks)
2. MC's block bootstrap operates (5-day Monday-anchored blocks; weeks are the natural unit)
3. Sample size is comfortable (227 week-blocks; bottom decile = 23 weeks, well above N=30 floor for primary metric)
4. The hedge-need question is empirically answerable: if joint-tail-present, the response under prop-firm constraints is *subtraction* (reduce concentrated allocation) per Delete-before-Accelerate; if concentration-driven, the AUDJPY-as-hedge intuition was structurally misframed at any resolution.

---

## §2 Falsifiable Hypothesis (binary, draft for Pre-Q gate)

**Question:** On the worst portfolio *weeks* in the historical panel, do strategies contribute losses jointly (joint-tail-present) or do a small number of strategies dominate (concentration-driven)?

**H1 (joint-tail-present):** On the worst-decile portfolio weeks (N≈23 of 227), the mean number of strategies contributing net-negative weekly PnL is ≥ 3.0, with 95% bootstrap CI lower bound ≥ 2.5.

**H0 (concentration-driven):** On the worst-decile portfolio weeks, the mean number of strategies contributing net-negative weekly PnL is ≤ 2.0, with 95% bootstrap CI upper bound ≤ 2.5.

**AMBIGUOUS:** Mean between bounds OR CI straddles 2.5.

The threshold structure mirrors Q-JOINT-TAIL-1 rev 3's primary `n_active=4` formulation — but at weekly resolution, `n_active ≈ 4` is no longer rare; it is the norm. Authoring-time sanity check (§9 below) verifies this before threshold-locking.

---

## §3 Methodology Sketch (high-level; CC handoff would specify in detail)

1. Aggregate per-strategy daily PnL to weekly using Monday-anchored 5-day blocks (matching MC's `build_week_blocks` convention).
2. Compute portfolio-week PnL = sum across strategies per week.
3. Identify bottom decile of portfolio-week PnL (N≈23).
4. For each worst week, compute `n_strategies_negative` (count of strategies with net-negative weekly PnL) and `n_strategies_active` (count with any trades that week).
5. Verdict subset selection per the Trap #15 fix: use weeks where `n_active = 4` (sanity check at §9 confirms this is the dominant subset, not the rare one).
6. Compute mean `n_strategies_negative` + bootstrap CI; apply §2 thresholds.
7. Secondary: per-pair conditional correlation on weekly PnL (bottom-decile weeks vs. full panel).

CC handoff brief will spell out all 8+ steps with deliverables.

---

## §4 Pre-Q Gate: The Algorithm

Pre-Q gating per `inqhiori-algorithm` skill: Question / Delete / Simplify / Accelerate.

### Question

Framed in §2 above. Names a symptom (does the book co-fail at week resolution?), not a fix. Falsifiable binary. Passes Pre-Q check #5 (question-not-solution).

### Delete

*Can this Q be deleted?* Three sub-checks:

- **Already-known?** Partial. 2026-04-25 found temporal clustering at lag-5 (autocorrelation within strategy series). Q-JOINT-TAIL-1 closure found daily co-failure unmeasurable. Neither answers the *weekly cross-strategy co-failure* question directly. Not deletable on already-known grounds.
- **Wrong question?** The hedge-need question motivated Q-JOINT-TAIL-1. Q-JOINT-TAIL-1 closure (B.5) noted that the AUDJPY hedge rejection stands regardless, and under prop-firm constraints, a joint-tail-present verdict produces *subtraction* response not *addition*. So is this Q load-bearing? **Yes** — it answers whether subtraction is even warranted. Concentration-driven verdict means current allocation is the structurally-correct response to current risk profile; no allocation change needed. Joint-tail-present verdict means structural rebalance is warranted. The Q is decision-load-bearing.
- **Sunk-cost framing?** Q-JOINT-TAIL-1 went through 3 brief revisions + Phase 0 BLOCKED. Is authoring a follow-up sunk-cost-driven? **Test:** if Q-JOINT-TAIL-1 had been BLOCKED-RETIRED on the first authoring (with the same panel-shape finding), would we still author this weekly follow-up? **Yes** — the panel-shape finding directly motivates the weekly-resolution Q; the daily framing was the misstep, not the underlying hedge-need question. Not sunk-cost.

**Delete verdict: does not delete.**

### Simplify

*Can the Q be simplified to learn the same thing more cheaply?*

- **Use MC sim output instead of historical panel?** MC outputs aggregate p99 max_dd, not per-strategy-per-week decomposition. Can't substitute.
- **Use existing 2026-04-25 panel analysis output?** That analysis tested temporal autocorrelation within strategy series, not cross-strategy co-failure. Different data product.
- **Reduce scope to just 2 strategies (highest-allocation pair)?** Loses joint-4 structure. The question is specifically about the locked 4-strategy book.
- **Use weekly returns rather than weekly PnL?** Equivalent for the falsifier (sign of net contribution is the metric, scale-invariant). PnL chosen to match MC convention; returns adds an unnecessary normalization step.

**Simplify verdict: no cheaper substitute exists.**

### Accelerate

*Can the investigation be run faster?*

- Same 4 CSVs as Q-JOINT-TAIL-1 — no new data acquisition.
- Weekly aggregation is one step less than daily (no `n_active` conditioning needed because weeks are the natural multi-strategy unit per §9 sanity check).
- Estimated execution: ≤1 session of CC time. Comparable or faster than Q-JOINT-TAIL-1.
- No further acceleration available without dropping rigor.

**Accelerate verdict: already at minimum cost.**

### Automate

*Does this need recurring automation?*

The question is one-shot for the 2026-05-23 lock. If the lock changes (Q-SWAP-4 RESOLVED → v5.6, or future allocation refresh), the question would re-fire with the new locked allocation. That's not automation, that's "re-run on lock change" — flag at audit hook level, not automate.

**Automate verdict: no recurring automation needed; quarterly regime-check calendar already covers re-trigger.**

---

## §5 Forbidden Moves

Inherits from Q-JOINT-TAIL-1 rev 3 §5 (9 moves), with weekly-resolution-specific additions:

1. **Solving the problem inside this Q.** Inquire-only. No allocation recommendations, no MC re-runs.
2. **Extending scope to 5-strategy hypotheticals.** AUDJPY out of scope.
3. **Substituting v5.6 Guardian.** Q-SWAP-4 staged separately.
4. **Conflating with I1 temporal-independence question.** 2026-04-25 finding's territory.
5. **Ad-hoc regime conditioning mid-analysis.** Pre-registered only.
6. **Re-defining tail mid-analysis.** If sample BLOCKED, return BLOCKED.
7. **Substituting instrument-level for strategy-level correlation.** Q-CORR-2 belt finding.
8. **Computing alternate correlation methods if Pearson is unsatisfying.** Pre-registered: Pearson.
9. **Re-introducing daily-resolution as the verdict unit.** Q-JOINT-TAIL-1 closure resolved that resolution non-falsifiably; this Q operates at weekly resolution exclusively.
10. **(NEW) Mixing 5-day-block aggregation conventions mid-analysis.** Monday-anchored to match MC. Do NOT pivot to ISO-week or Sun-Sat conventions mid-investigation.
11. **(NEW) Treating "bad week" identification as derivative of Q-JOINT-TAIL-1 worst-day list.** Worst weeks are computed fresh from weekly PnL aggregation; not by summing daily worst-days. The day-level worst-day list was structurally biased toward single-strategy-active days (per Q-JOINT-TAIL-1 closure B.1); weekly worst-week list is independent.

---

## §6 Pre-Q Verdict

```
[x] Question stated, falsifiable, names symptom (§2)
[x] Delete check passed (§4 Delete)
[x] Simplify check passed (§4 Simplify)
[x] Accelerate check passed (§4 Accelerate)
[x] Automate check passed (§4 Automate)
[x] Forbidden moves explicit and tempting (§5, 11 moves with rationale)
[x] Standing doctrine connections explicit (§1)
[x] Predecessor closure read and referenced (Q-JOINT-TAIL-1 closure)
[x] Authoring-time sanity check structurally required (§9 below; NEW per Trap #15 candidate)
```

**Pre-Q verdict: PASS** — proceed to author CC handoff brief, conditional on §9 sanity check executing first and confirming the verdict-subset assumption.

---

## §7 Next Action

If §9 sanity check confirms `n_active = 4 weeks` constitute the dominant pattern in the bottom-decile (≥30 weeks, expected ~20+):

1. Author CC handoff brief `docs/briefs/programs/2026-05-XX-q-joint-tail-weekly-cc-handoff.md` (date when authored).
2. Brief inherits the structure of Q-JOINT-TAIL-1 rev 3 with weekly-resolution adaptations.
3. Apply Trap #13/#14/#15 procedural fixes at authoring time (consult `CLAUDE.md` at authoring, distinguish input-panel-property vs. MC-assumption claims, run panel-shape sanity check before threshold-locking).
4. Hand off to CC.

If §9 sanity check returns unexpected results (e.g., `n_active = 4 weeks` are rare, or weekly aggregation produces sample-size issues):

- Return to Pre-Q stage. Do NOT author CC handoff against an unverified assumption.
- Re-pose the question or close this line.

---

## §8 Cost Estimate

| Stage | Estimated effort |
|---|---|
| §9 panel-shape sanity check | ≤30 min (cheap script + 4 CSVs already on disk) |
| CC handoff brief authoring | 1 claude.ai session |
| CC Phase 0 dry-run | 1 CC session |
| CC Phase 1 full execution | ≤1 CC session |
| Parent review + closure | 1 claude.ai session |
| **Total** | **~4 sessions across claude.ai + CC; ≤2 calendar days** |

Within forward-asymmetry doctrine. Same order-of-magnitude as Q-JOINT-TAIL-1 (whose total cost across 3 revs + Phase 0 was probably 5 sessions).

---

## §9 Authoring-Time Panel-Shape Sanity Check (NEW — Trap #15 fix)

**The lesson Q-JOINT-TAIL-1 paid for.** Before threshold-locking §2 hypotheses, run a panel-shape sanity check on the data the brief is about to test, at authoring time, not at Phase 0 time.

### Required check

Aggregate the 4 CSVs to weekly PnL using Monday-anchored 5-day blocks. Compute:

```
1. Total week-blocks in panel (expected ~227 per CLAUDE.md)
2. Distribution of n_active (count of strategies with ≥1 trade per week-block)
3. Bottom decile of portfolio_week_pnl (expected N ≈ 23)
4. Within bottom decile: distribution of n_active

Expected (hypothesis to verify before locking thresholds):
- n_active = 4 weeks: dominant pattern in panel (>50% of weeks)
- n_active = 4 weeks in bottom decile: dominant pattern (≥15 of ~23)
- Verdict-subset N ≥ 15 even if n_active strictly = 4 (well above N≥30 only at primary;
  fallback to n_active ≥ 3 still available as in Q-JOINT-TAIL-1 rev 3)
```

### Disposition based on sanity check result

- **If expected pattern holds:** PASS. Proceed to CC handoff brief authoring. Thresholds in §2 are appropriate.
- **If expected pattern fails (e.g., n_active = 4 weeks are still rare):** RETURN TO PRE-Q. Do not author CC handoff. Investigate panel-shape further; possibly Q-JOINT-TAIL-WEEKLY is also non-falsifiable for this allocation, in which case the closure-note-then-RETIRED disposition mirrors Q-JOINT-TAIL-1.

### Why this check exists at authoring time

Q-JOINT-TAIL-1's Phase 0 BLOCKED was an avoidable cycle: had the panel-shape (n_active=4 occurring once in 1141 bdays) been checked before authoring, the brief would have framed at weekly resolution from inception. Three claude.ai revisions + one CC Phase 0 cycle would have been compressed to zero.

This §9 step is the procedural fix per the candidate-status Trap #15 lesson. It is *load-bearing* for this brief (the verdict can't be locked until §9 executes), and it is *transferable* — future Pre-Q briefs that depend on a panel-shape assumption should include the equivalent step.

**§9 status:** **EXECUTED 2026-07-14 → FAIL → Q RETIRED.** Script: [`lab/archive/q_joint_tail_weekly_2026-07/sanity_check.py`](../../../lab/archive/q_joint_tail_weekly_2026-07/sanity_check.py) (227 week-blocks, matching expected ~227). Both gate limbs failed: `n_active=4` share overall = **9.7%** (needed >50%); `n_active=4` in the 23-week bottom decile = **4 of 23** (needed ≥15) — the modal week has two strategies active, and the worst portfolio-weeks are concentration events, not 4-way co-failure. The book is temporally diversified at weekly resolution too, so the joint-tail question is non-falsifiable for this allocation at the weekly scale (as it was at the daily scale — Q-JOINT-TAIL-1). Per this §9's own FAIL disposition + the roster next-action, the Q is **RETIRED** (no CC handoff authored). Closure: [`docs/briefs/closures/Q-JOINT-TAIL-WEEKLY-closure-retired.md`](../closures/Q-JOINT-TAIL-WEEKLY-closure-retired.md).

---

## §10 Audit Hooks (Runnable)

```bash
# 1. Predecessor closure exists and references this Pre-Q
grep -l "Q-JOINT-TAIL-WEEKLY" archive/docs/briefs/Q-JOINT-TAIL-1-closure.md

# 2. §9 sanity check executed before CC handoff authoring
# (manual — Joshua confirms the check ran and produced numbers)

# 3. If CC handoff authored, it references this Pre-Q's §9 result
grep -F "Pre-Q §9 sanity check" docs/briefs/programs/2026-05-*-q-joint-tail-weekly-cc-handoff.md

# 4. Lesson capture exists
ls docs/lessons/2026-05-27-brief-authoring-traps-13-14-15.md

# 5. Q-JOINT-TAIL-WEEKLY closure (if/when produced) cross-references this Pre-Q
# (audit at closure time, not at Pre-Q time)
```

---

## Discipline check summary

```
General (1–6):
[x] §0 Rule 0 reads populated with file paths + verification anchors (inherited from Q-JOINT-TAIL-1 rev 3)
[x] Falsifiable hypothesis stated in §2 (binary at weekly resolution)
[x] Forbidden moves explicit and genuinely tempting (11 moves; 2 new for weekly resolution)
[x] Gate criteria binary (RESOLVED-JOINT-TAIL-PRESENT / RESOLVED-CONCENTRATION-DRIVEN / AMBIGUOUS)
[x] Question names symptom not fix (does book co-fail at week resolution?)
[x] Audit hooks runnable (§10 contains 5 hooks)

Pre-Q specific:
[x] §4 The Algorithm applied (Q/D/S/A/Au all addressed)
[x] §6 Pre-Q verdict reached (PASS with §9 prerequisite)
[x] §7 next action specified
[x] §8 cost estimate provided

Trap #13/#14/#15 fixes applied:
[x] §0 grounded in current canonical state (2026-05-23 ADR; CLAUDE.md at authoring time)
[x] §2 framing scoped to input-panel property at week resolution (not MC assumption test)
[x] §9 panel-shape sanity check structurally required before CC handoff authoring (Trap #15 fix)
[x] §5 forbidden moves #4 and #9 specifically prevent conflation with I1 or daily resolution

Doctrine connections:
[x] §1 Q-JOINT-TAIL-1 closure read; weekly resolution motivated by closure B.4
[x] §4 The Algorithm Delete-before-Accelerate doctrine invoked for hedge-need decision logic
[x] §1 + §5 AUDJPY hedge rejection preserved; not re-opened
```

---

**End of Pre-Q brief.**
