# ADR 2026-08-20 — Mechanize `check_brief.py`'s §0 anchor check; name a separate triage-verification discipline (not a Rule 0 scope extension)

**Status:** `Proposed` — drafted at operator direction ("the tactical pattern is making the case for Rule 0, and perhaps this rule needs to be enforced more consistently"), ratification owed
**Decision date:** 2026-08-20
**Authors:** Joshua (direction) + Claude Code (Sonnet 5, drafter)
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Tier:** FULL (amends `check_brief.py`, a core methodology-enforcement script, and proposes a new standing discipline)
**Layer:** methodology enforcement. **$0 / K=0.** No `core/`, Pine, allocation, `dd_protection`, rail, or K ledger touched.

---

## §0 — Rule 0 reads (production source, this session)

- [`docs/rule_0.md`](../rule_0.md) — whole file, this session. Two load-bearing lines: §"Triggering failures" names exactly two documented incidents (2026-04-17, 2026-04-27), both about brief-authoring against risk controls; §"Scope" states explicitly *"New rules are written only against observed failures during execution phase, not hypothesized ones."* This last line is why this ADR does **not** propose extending Rule 0's own scope — see §3 Alternative 2.
- [`scripts/check_brief.py:364-373`](../../scripts/check_brief.py) (`_check_section0_paths`) — read directly, this session. The function's entire check is `_section0_cites_repo_path(body)` — a regex match for a path-shaped string (e.g. `dd_protection.py`). It contains **no check for a commit hash, `git log` timestamp, or any anchor at all.** Confirmed by reading the function body, not inferred from its docstring.
- `.claude/skills/brief-authoring/SKILL.md` (read via a research pass this session) — L32/L42 state the anchor requirement explicitly: *"§0 must list specific paths and a verification timestamp... commit hash, timestamp, line range, or last-modified date"* and that an anchor-less §0 *"decays to ceremony within weeks."* The skill's own Known Trap #3 ("Reconstructed §0 — post-hoc Rule 0") describes exactly the failure mode this gap leaves uncaught: §0 lists files claimed to be read but no commit/timestamp anchor, detectable today only by a human asking the author to paste `git log -1 -- <file>` output (SKILL.md's own stated verification step, never mechanized).
- `docs/lessons/2026-07-06-close-vocabulary-gap.md:59` — read this session (research pass). A sibling discipline (reachability) explicitly concluded the opposite direction for an adjacent gap: *"not mechanically enforceable as written... the discipline stays a human authoring-time pass."* Read as a caution against assuming every discipline gap is worth mechanizing — this ADR argues the §0 anchor gap specifically clears that bar (concrete regex check, two documented historical costs), not that every gap does.

---

## §1 — Context

Today's session surfaced a tactical pattern worth naming honestly: three separate times, a leverage/triage judgment (Aegis→6J composed gap, the Tradeify-native fade, an initial read of temporal-selectivity's status) was formed from a survey-agent summary or a plan-doc one-liner and turned out wrong on primary-source read — the real blocker lived one or two documents deeper than the summary. None of these were formal brief-authoring against risk controls (Rule 0's own literal scope), and none produced a bad brief — each was caught before anything was written, by going and reading source. So today's session does **not** supply a fresh "triggering failure" in Rule 0's own sense (§0 above); it supplies evidence that Rule-0-*style* discipline (verify against source before acting, not summary or memory) has real value in an adjacent activity — triage/leverage-ranking across candidates — that Rule 0's stated scope does not cover and was never meant to cover.

Separately, and independent of today's triage pattern, a real mechanical gap already exists and is already evidenced by the two historical incidents Rule 0 itself names: `check_brief.py`'s §0 check verifies a brief cites *some* file path, never that the cited anchor (commit hash / timestamp) is real or that the read happened before authoring. This is the exact shape of Known Trap #3, already named in the brief-authoring skill's own discipline text, currently caught only by a human manually asking for `git log -1` output.

**Decision driver (one sentence):** two independent things are true at once — an already-evidenced mechanical gap in `check_brief.py` is worth closing on its own historical record, and today's session evidences a *different*, currently-uncovered discipline gap in triage/ranking work that deserves its own named rule rather than being folded into Rule 0's scope.

---

## §2 — Decision

**2-A — Mechanize the §0 anchor check.** `_check_section0_paths` gains a second check: for each cited repo path in §0, the section body must also contain an anchor pattern (a commit hash matching `[0-9a-f]{7,40}`, or a `last-modified`/date string) in reasonable proximity to that path citation. This does **not** verify the hash is *current* (a stale-but-real anchor is legitimate — files change after a brief is authored) — it verifies an anchor of *some* form is present, closing the gap between what `SKILL.md` already requires in prose and what the mechanical gate actually checks. A missing anchor on an otherwise-path-citing §0 becomes a new `HARD` violation, distinct from the existing missing-path violation.

**2-B — Name a separate, non-Rule-0 discipline for triage/leverage-ranking work.** Per §0's read of Rule 0's own scope line, this is **not** a Rule 0 amendment. It is a new, narrower rule scoped to a different activity: before presenting or acting on a leverage/priority ranking across multiple research-thread candidates, each candidate's *actual current blocker* must be verified against its owning primary source (ledger, CARD, closest ADR/closure) before ranking — a survey-agent summary or CATALOG one-liner is not sufficient grounding to rank on. This is a **human/agent authoring-time discipline**, not a mechanical gate (per §0's Alternative-2 caution — there is no brief artifact for a triage exercise that a script could inspect the way `check_brief.py` inspects a Q-brief's §0).

**Effective:** on operator ratification.
**Scope:** `scripts/check_brief.py`'s §0 anchor check (2-A); a new discipline note, not a Rule 0 text edit (2-B).

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **1 — Do nothing; today's pattern doesn't rise to a new rule.** | Rejected on the historical record alone: the §0 anchor gap (2-A) is *already* evidenced by two documented incidents independent of today, and leaving `SKILL.md`'s own stated requirement unmechanized is the exact ceremony-decay risk the skill's own text warns about. |
| **2 — Extend Rule 0's literal scope to cover triage/leverage-ranking work.** | Rejected against Rule 0's own stated discipline: *"new rules are written only against observed failures during execution phase, not hypothesized ones"* (§0). Today's triage failures are real but are a different *activity* (survey-summary triage, not risk-control brief authoring) than what Rule 0's two named incidents cover — folding them in would blur a scope line Rule 0 draws deliberately, for a gain (one shared name) that doesn't require merging the two disciplines. |
| **3 — Mechanize the triage-verification discipline too (2-B) as a script check.** | No artifact exists for a triage exercise the way a Q-brief file exists for `check_brief.py` to inspect — the same reasoning `docs/lessons/2026-07-06-close-vocabulary-gap.md` already reached for a sibling discipline. Stays a human/agent authoring-time pass; revisit only if a triage-exercise artifact format gets standardized later. |
| **4 — Verify the cited commit hash is current (matches `git log -1` exactly), not just present.** | Too strict — a legitimately-authored brief's anchor goes stale the moment the cited file changes again, which happens constantly in an active repo. Rejected in favor of the weaker, still-load-bearing check (anchor present, not necessarily current) that catches Known Trap #3's actual failure mode (no anchor at all, or an obviously fabricated one) without generating false positives on ordinary drift. |

---

## §4 — Falsifiable hypothesis

**H:** requiring an anchor pattern (not just a path citation) in §0 catches a materially different, real class of Known-Trap-#3 briefs than the existing path-only check, without generating enough false positives to make authors route around it.

**Accept H if:** over the next quarterly methodology audit window, at least one brief that would have passed the old path-only check fails the new anchor check, AND the false-positive rate (well-anchored briefs incorrectly flagged) stays low enough that no author reports routing around the check.
**Reject H if:** the new check fires zero true positives in that window (no brief was ever missing an anchor once forced to have *a* path — i.e., the gap was ceremonial, not load-bearing) OR generates enough false positives that authors start padding §0 with junk anchor-shaped text to pass the gate mechanically (the check becomes exactly the ceremony `docs/lessons/2026-07-06-close-vocabulary-gap.md` warns about).
**Re-test:** next quarterly programme audit (2026-11-08), or sooner if either trigger is observed.

---

## §5 — Forbidden moves

- **Reading 2-A as retroactively invalidating any already-committed brief.** No frozen pre-registration or closed brief is re-checked; this binds new briefs only, from ratification forward.
- **Treating a passing anchor check as proof the read happened.** The check verifies an anchor-shaped string is present, not that it's true — it closes the "no anchor at all" gap (Known Trap #3's literal form), not the deeper "fabricated anchor" case, which stays a human-judgment catch.
- **Folding 2-B into Rule 0's own text file** (`docs/rule_0.md`) — per §3 Alternative 2, this stays a separate, named discipline. Rule 0's own "new rules against observed failures" scope line is the reason this ADR itself doesn't touch that file.
- **Treating 2-B as mechanically enforced** — it isn't, and per §3 Alternative 3 shouldn't be forced to be until a triage-artifact format exists to check.

---

## §6 — Consequences

**Positive:** closes a gap that's already cost two documented incidents, using the exact mechanism (`check_brief.py`) the estate already trusts for this class of check. Names the triage-verification lesson as a citable discipline rather than leaving it as an unreferenced private observation.

**Negative / watched:** a new HARD violation class means some currently-passing briefs may need a one-line anchor addition on their next edit — cheap, but real friction; §4's falsifier is designed specifically to catch if this becomes ceremony rather than signal.

**Risks:** the regex for "anchor pattern" could be too loose (accepts junk) or too strict (rejects legitimate date formats) — mitigated by keeping the pattern permissive (hash-shaped OR date-shaped OR "last-modified") and reviewing false-positive reports at the same quarterly cadence as §4.

---

## §7 — Implementation plan

- **Phase 0** — this ADR ships as the ruling; ratification owed.
- **Phase 1** — `scripts/check_brief.py`: extend `_check_section0_paths` with an anchor-pattern check adjacent to each cited path; add a regression test pinning both the pass case (path + anchor) and the new fail case (path, no anchor).
- **Phase 2** — no `docs/rule_0.md` edit (per §5). A short discipline note is added to the `brief-authoring` skill's Known Traps section, cross-referencing this ADR, for 2-B.
- **Phase 3** — `check_brief.py --self-test` (if one exists) or a manual regression pass on 2-3 existing frozen briefs to confirm no false positives on already-anchored §0 sections.

---

## §10 — Audit hooks (runnable)

```bash
# The gap this ADR closes, confirmed present pre-ratification
grep -n "_check_section0_paths" -A 10 scripts/check_brief.py
# Expected pre-Phase-1: only _section0_cites_repo_path, no anchor regex

# Post-Phase-1: confirm the new check exists and fires on a path-only, anchor-less §0
python -c "
import sys; sys.path.insert(0, 'scripts')
from check_brief import _check_section0_paths
v = _check_section0_paths({'0': 'Read core/dd_protection.py before authoring.'})
print(v)
"
# Expected post-Phase-1: a HARD violation for missing anchor

# Rule 0's own text is unedited by this ADR (per Forbidden Moves)
git diff main -- docs/rule_0.md
# Expected: empty
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-20 | Initial authoring, drafted at operator direction, ratification owed | Joshua (direction) + Claude Code (Sonnet 5) |
