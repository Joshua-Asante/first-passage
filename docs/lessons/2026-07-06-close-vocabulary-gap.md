# Lesson M-19 — Close-vocabulary gap: pre-registration freezes the map before the data, but does not guarantee the map *covers* the eventual finding

**Lesson ID:** M-19 (methodology) · file-slug `2026-07-06-close-vocabulary-gap`
**Status:** `Candidate` (registered now via structural-argument bypass — see Promotion gate; **not** promoted to Standing rule)
**Captured:** 2026-07-06
**Promoted to standing rule:** N/A (Candidate)
**Author:** claude.ai (advisor) · CC (execution)
**Registry file:** `docs/methodology/lessons/methodology_lessons.md` (canonical M-N home — **not edited by this diff**; the M-19 pointer there is a parent-owned follow-up if/when this promotes, so this Candidate lives as a standalone `docs/lessons/` doc in the 2026-05-27-traps precedent's style until then)

---

## Pattern (one sentence)

A register's pre-registered close-vocabulary can become unsatisfiable mid-investigation when an early discriminator's result forecloses the specific close label written for a later branch, and this is only caught if someone checks the label against the branch's own eventual finding rather than assuming pre-registration guarantees coverage.

---

## The two firings (distinct mechanisms, one class)

Both are the same failure class — **the §3 outcome→standing map was frozen before the data (good), but the freezing did not guarantee the map's close labels *cover* the finding that actually occurred (the gap)** — surfacing in two mirror-image forms:

- **DJ30 (first instance) — permissive-criteria form.** The §4 read criteria as originally authored carried **no small-cell/multiplicity guard**: three primary Friday-type reads at 1.5× thresholds meant a single spurious `ELEVATED` could have false-graduated a candidate. Caught and **repaired in-design during adjudication** — T1 was rebuilt as a read-*tuple* and the §3 map made to require cross-read coherence (never a single-read win), so the map assumes one spurious ELEVATED is expected. The map, as first written, could have *graduated a mechanism the evidence did not support*. Source: [`docs/ltm/briefs/Q-MECH-1.DJ30_h_register.md`](../ltm/briefs/Q-MECH-1.DJ30_h_register.md) §Fragility-governance ¶2 (`2873fcf`).

- **NAS (second instance) — foreclosed-label form.** The register's **sole D-close label `ENGINEERED-BETA-CONFIRMED` had a firing condition (T1 = by-construction)** that the actual T1 result (`GENUINE-CONTINUATION-DOMINATED`) **permanently foreclosed**. D still leads on preponderance — but the pre-registered label for D's own close can never fire, so the 2026-08-08 preponderance close requires a one-line disclosed vocabulary amendment (candidate: `REGIME-CARRIED-CONFIRMED`, borrowed from the XAU register). The map, as written, *cannot name the result that actually occurred*. Source: [`docs/ltm/briefs/Q-MECH-1.NAS_h_register.md`](../ltm/briefs/Q-MECH-1.NAS_h_register.md) §Terminal-standing "Close-vocabulary gap" bullet (`046e48f`) — which itself labels this the "second instance of the close-vocabulary-gap lesson class (first: DJ30 multiplicity-guard gap)."

The unifying root: **pre-registration guarantees the map was authored *before* the data, not that the map *covers* the data.** In both firings the gap was caught only because someone checked the pre-registered vocabulary against the branch's own eventual finding — DJ30 mid-adjudication (repaired in-design), NAS at the terminal read (flagged for 08-08). Trusting "pre-registration ⇒ coverage" would have missed both.

---

## Anchor incidents

Per Known Trap #9: a lesson without a dated incident AND a dollar cost / counterfactual does not graduate empirically. This one bypasses the empirical gate by structural argument (below); the incidents are dated and their counterfactual named, but there is deliberately **no dollar anchor** because both legs are non-live.

| Date | Incident | Cost / counterfactual | Source brief |
|---|---|---|---|
| 2026-07-06 | **DJ30** register's §4 criteria lacked a multiplicity/small-cell guard (permissive form); a lone spurious `ELEVATED` could have false-graduated a candidate. Repaired ad hoc in-design during adjudication. | No dollar cost — leg is parked/non-live. Counterfactual: a spuriously-graduated Friday mechanism, i.e. a monitor built on noise. | `Q-MECH-1.DJ30_h_register.md` (`2873fcf`) |
| 2026-07-06 | **NAS** register's sole D-close label `ENGINEERED-BETA-CONFIRMED` became permanently unsatisfiable once T1 returned `GENUINE-CONTINUATION-DOMINATED` (foreclosed form). | No dollar cost — leg is parked/non-live. Counterfactual: a confused or silently-improvised 2026-08-08 close if the gap is not named now. | `Q-MECH-1.NAS_h_register.md` (`046e48f`) |

**Promotion gate status:**
- [ ] Single incident >$3K dollar anchor (promotes immediately) — **not met** (both legs non-live; no dollar impact by construction)
- [ ] OR three firings across separate windows (promotes on third) — **not met** (2 firings, and they fired in the *same* window — the 2026-07-06 Q-MECH-1 family adjudication — not three separate ones)
- [x] **OR structural argument** (rare — must explicitly justify why the empirical gate is bypassed; precedent: CC-handoff-hygiene 2026-05-15 structural bypass)

  **Structural-argument justification (why register this as a named Candidate now, despite failing E1/E2):** The pattern is **about to be used** — at the 2026-08-08 quarterly touch, *both* parked legs (DJ30 and NAS) close, and NAS's close specifically requires the one-line vocabulary amendment this gap identifies. Naming the class now, while the two firings and their repair shapes are fresh and committed, is strictly lower-cost than reconstructing the pattern under time pressure at the touch — where the risk is exactly a "confused or silently-improvised close." The empirical gate (3 firings / $3K) exists to stop *speculative* lessons from accreting as noise; this lesson is neither speculative (2 committed firings, both with named repair shapes) nor idle (it has a scheduled use-date 33 days out). The structural argument bypasses the empirical *count* gate — it does **not** promote to Standing rule. Promotion remains a Joshua decision per the Promotion Record section (deliberately left blank).

---

## Repair / discipline rule

**Rule (present-tense imperative):** When authoring a §3 outcome→standing map for an H-register, run a **close-label reachability check** before freezing the map: for each pre-registered terminal close label, confirm (a) at least one reachable discriminator-outcome tuple *satisfies* it, and (b) no single upstream discriminator result can render it *unsatisfiable* (foreclosed form) or *trivially/falsely satisfiable* (permissive form). If a close label depends on one discriminator's outcome, verify that outcome is not already foreclosed by an earlier discriminator's design. A close label that cannot be reached, or that can be reached by noise alone, is a map defect — fix it at authoring time, not at the terminal read.

**Where the rule lives (candidate enforcement point):**
- [x] Brief-authoring / register-authoring discipline — the natural home is the H-register §3-map guidance (brief-authoring SKILL.md and/or the inqhiori register template). **Wiring it in is deferred** until/if this Candidate promotes (per this handoff's no-promotion + no-scope-creep bounds; SKILL.md is not edited by this diff).
- [ ] check_brief.py — **not** mechanically enforceable as written (reachability is a semantic property of the specific discriminator design, not a regex-detectable structural one). If promoted, the mechanical proxy is weak; the discipline stays a human authoring-time pass.
- [x] Calendar trigger — the 2026-08-08 quarterly touch is the first scheduled *use* of this lesson (NAS's vocabulary amendment); see Audit hooks.

Until promotion wires it into a canonical authoring surface, this is a named Candidate with a scheduled use-date, not yet a standing discipline. Flagged honestly.

---

## Cross-references

- **Briefs citing this lesson:** `docs/ltm/briefs/Q-MECH-1.DJ30_h_register.md` (`2873fcf`), `docs/ltm/briefs/Q-MECH-1.NAS_h_register.md` (`046e48f`) — both reference "the close-vocabulary-gap lesson class / candidate"; `docs/ltm/briefs/Q-MECH-1_SC-XLEG_family_synthesis.md` §1/§4 notes the NAS gap.
- **Related lessons:** the 2026-05-27 brief-authoring traps #13/#14/#15 (`docs/lessons/2026-05-27-brief-authoring-traps-13-14-15.md`) — sibling in the "pre-registration doesn't guarantee X" family; #13 (precision exceeds grounding) and #15 (verdict-subset existence not verified) are the *authoring-time-assumption* cousins of this map-coverage gap. Related Pre-Q-hygiene lesson: freeze-then-verify-coverage.
- **Skills enforcing this lesson:** none yet (Candidate; enforcement deferred per Repair section).
- **Superseded lesson:** none.

---

## Promotion record (if applicable)

Skip — Status is `Candidate`. Promotion to Standing rule is a Joshua decision (do not fill this in without it; §0.5 of the authoring handoff and the template both reserve it).

---

## Retirement (if applicable)

Skip — not retired.

---

## Audit hooks

```bash
# 1. This lesson capture committed
ls docs/lessons/2026-07-06-close-vocabulary-gap.md

# 2. Both firing registers still reference the close-vocabulary-gap class
grep -c "close-vocabulary" docs/ltm/briefs/Q-MECH-1.NAS_h_register.md   # expect >= 1
grep -in "multiplicity" docs/ltm/briefs/Q-MECH-1.DJ30_h_register.md      # DJ30's permissive-form firing

# 3. Source anchors still resolve
git log -1 --format='%H' -- docs/ltm/briefs/Q-MECH-1.DJ30_h_register.md  # expect 2873fcf (or later; content anchor above)
git log -1 --format='%H' -- docs/ltm/briefs/Q-MECH-1.NAS_h_register.md   # expect 046e48f (or later)

# 4. Scheduled USE-date check (2026-08-08 quarterly touch): confirm NAS's close
#    used an amended, disclosed close label (not ENGINEERED-BETA-CONFIRMED, which
#    is unsatisfiable) and did NOT silently improvise. Manual review at the touch.
grep -n "REGIME-CARRIED-CONFIRMED\|ENGINEERED-BETA-CONFIRMED" docs/ltm/briefs/Q-MECH-1.NAS_h_register.md

# 5. Forward coverage check: any NEW H-register authored after 2026-07-06 should
#    show a close-label reachability pass in its §3 map (grep for the phrase or an
#    equivalent per-label satisfiability note). Manual, at map-authoring review.

# 6. Promotion check (quarterly): a third firing in a SEPARATE window, or a $3K
#    dollar-anchored firing, meets the empirical gate → escalate to Joshua for
#    Standing-rule promotion + registry (M-19) + SKILL.md wiring.
```

---

## Verification

```bash
$ python /c/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py docs/lessons/2026-07-06-close-vocabulary-gap.md --type lesson
# Expected (canonical skill-side checker): Pattern / Anchor incidents / Repair / Audit hooks all PASS
# Note: the repo-side scripts/check_brief.py does NOT model the 'lesson' type (it
# maps lesson→generic and demands numbered §0/§4/§5/§6/§10 sections a lesson does
# not have); a red run there is a known-divergence of the mechanical subset, not a
# malformed lesson. The skill-side checker is canonical for lesson-type docs.
```

The check: can the §Audit-hooks grep mechanically detect the failure mode next time? Partially — hooks 4/5 detect the *symptom* (an unsatisfiable close label surviving to the terminal read, or a new register lacking a reachability pass), but the reachability property itself is semantic, not regex-detectable. Hence Candidate, with the discipline held as a human authoring-time pass.
