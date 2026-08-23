# ADR 2026-08-23 — Ratify the `adr-decay-audit` skill: a periodic/triggered sweep of the Accepted-ADR corpus for continued applicability

**Status:** `Proposed` — authored by Claude Code in an autonomous PR-based session; ratification is the operator's PR review/merge decision, not asserted here.
**Decision date:** 2026-08-23
**Authors:** Joshua (direction: asked which of the ~150 Accepted ADRs still hold, and whether a process exists to catch decay) + Claude Code (audit execution, skill draft, this ADR)
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Related:** [Rule 6 skew-audit](../operational_rules.md#6-doccode-skew-audit-fires-on-every-version-lock) ·
[`.claude/commands/skew-audit.md`](../../.claude/commands/skew-audit.md) ·
[`.claude/skills/programme-audit/SKILL.md`](../../.claude/skills/programme-audit/SKILL.md) ·
[`.claude/skills/blast-radius/SKILL.md`](../../.claude/skills/blast-radius/SKILL.md) ·
[ADR ceremony tiering](2026-08-08-adr-ceremony-tiering.md) ·
[ox-alpha adversarial lens scope](2026-08-22-ox-alpha-adversarial-lens-scope.md) (the intended
second-opinion pass on the skill draft; not completed this round — see §1)
**Layer:** governance convention (documentation/process). **$0 spend / K=0** — no live-risk
surface, no strategy parameter, no `dd_protection`/allocation constant, no Pine source is touched.

---

## §0 — Rule 0 reads (production-source verification)

Files read before authoring this ADR (this session):

- `CLAUDE.md` — anchor `0723587` (2026-08-22). Confirms "ADRs are canonical for every decision" and
  the retention-test doctrine this new skill's own output artifacts must satisfy.
- `docs/operational_rules.md` §6 (doc/code skew audit) — anchor `e159743` (2026-08-22), full section
  read. Confirms Rule 6 is event-triggered (fires on a strategy version-lock) and scoped to a narrow
  target list (`CLAUDE.md`, ADR `Code:` pointers, methodology docs) — not a general per-ADR
  applicability sweep.
- `.claude/skills/programme-audit/SKILL.md` — anchor `31fd642` (2026-08-19), full file read. Confirms
  it runs a Lakatos diagnostic on *programmes* (methodologies as a whole, the portfolio as a whole)
  on a quarterly/semi-annual cadence, not a per-ADR sweep — and supplied the AMBIGUOUS-is-a-verdict,
  cadence-ceremony, and belt-churn discipline this new skill borrows directly.
- `.claude/commands/skew-audit.md` — anchor `31fd642` (2026-08-19), full file read. Confirms the
  skew-audit's own scope statement: a per-commit table for a bounded lock-to-fix window, output to
  chat only, not persisted.
- `.claude/skills/blast-radius/SKILL.md` — anchor `31fd642` (2026-08-19), read through its procedure
  section. Confirms it is a reactive post-edit sweep (grep old→new tokens across hot surfaces after
  a specific change), not a standing sweep over ADRs no recent edit touched.
- `docs/adr/2026-08-08-adr-ceremony-tiering.md` — anchor `31fd642` (2026-08-19), full file read. The
  tier test's limb 4 ("creates or amends doctrine — a rule, gate, falsifier threshold, or convention
  that binds future work") is why this decision takes the FULL template rather than a light record:
  a new standing audit skill is exactly a convention binding future work.
- `docs/adr/2026-08-22-ox-alpha-adversarial-lens-scope.md` — anchor `b2e5f15` (2026-08-22), full file
  read. Confirms the ratified pattern (Claude Code drafts, sanitizes, sends `stealth/ox-alpha` a
  genericized artifact for adversarial objections, reconciles before finalizing) and that this
  session had neither an `OPENROUTER_API_KEY` nor any existing invocation wrapper — matching the
  ADR's own §10 audit hook expectation that no such wrapper should exist. The operator's attempt to
  supply the key via `setx` did not reach this session (a local Windows persistent-env-var command
  cannot populate a remote container's environment). Given the choice between waiting on a key, the
  operator running the sanitized prompt manually, or proceeding without the external pass, the
  operator chose to proceed without it this round.
- `scripts/check_adr_graph.py` — anchor `d7a8a7f` (2026-08-22), read for required header fields
  (`Status`, `Decision date`, `Supersedes`, `Superseded-by`, `Superseded-in-part-by`,
  `Retain-until`) and the closed Status vocabulary (`Proposed`/`Accepted`/`Superseded`/
  `Withdrawn`/`Retired`) this ADR's header conforms to.
- `docs/adr/2026-04-17-portfolio-allocations.md`, `docs/adr/2026-06-23-tv-backtest-egress-automation.md`,
  `docs/adr/2026-08-08-great-prune.md` — anchor `31fd642` (2026-08-19) for all three (pre-dating this
  session's edits — none were modified). These are the three concrete findings cited in §1 as the
  motivating evidence; full text read and cross-checked against current repo state during the audit
  this ADR ratifies a standing process for.

---

## §1 — Context

The operator asked, of the ADR corpus (151 files with a primary `Status: Accepted` header, verified
by script against every file in `docs/adr/` this session — not assumed from a prior count): which
still hold, which have decayed, and whether a process exists to catch decay going forward. No such
process existed (§0). To answer the first two questions, this session ran a one-off two-phase audit
(15 batches of ~10 ADRs each, independently scanned for decay signals, then every flagged ADR
independently re-verified by a second reviewer briefed to refute rather than confirm the flag).

**Result of the one-off audit (the evidence base for this ADR, not restated in full here — see the
session's own chat record for the complete finding list):**

| Verdict | Count |
|---|---|
| Still fully applicable | 107 |
| Decayed, but already documented somewhere in the repo | 42 |
| Decayed with no documentation anywhere | 2 |

The two undocumented cases are the concrete argument for standing this up as a repeatable process
rather than a one-off:

1. `docs/adr/2026-04-17-portfolio-allocations.md` still asserts in its own Status line that a
   locked allocation figure "remains in force," when two later ADRs moved it twice without either
   linking back — and `docs/adr/INDEX.md` mirrors the same stale figure.
2. `docs/adr/2026-06-23-tv-backtest-egress-automation.md`'s 2026-07-27 addendum defended a scope
   decision on a premise that a *later*, unrelated ADR (`2026-08-07-loop-s2-signal-host-fork.md`,
   11 days after) silently invalidated — nothing links the two.

A third finding worth naming even though it counted as "documented elsewhere": `docs/adr/
2026-08-08-great-prune.md` and `CLAUDE.md`'s own top-line pointer both still state, unqualified,
that every pruned artifact is "retrievable via `git show pre-prune-2026-08-08:<path>`." That tag
does not exist on this public clone or its origin (verified directly this session: `git tag -l`,
`git ls-remote --tags origin` both empty) — the 2026-08-14 fresh-repo transplant left it only in the
private archive. `docs/ltm/README.md` already carries the correct caveat, but the Great Prune ADR
and the CLAUDE.md pointer every session reads first do not.

Existing mechanisms (§0) each cover a different slice: Rule 6 fires on version locks with a narrow
target list; `programme-audit` diagnoses programmes as wholes, not individual decisions; `blast-
radius` is reactive to a specific edit. None periodically re-reads an already-Accepted ADR to check
whether its factual claim is still true. The gap is structural, not a one-time oversight: a mature,
fast-moving ADR corpus (151 files in under six months) will keep producing this pattern as later
decisions overtake earlier ones without a forced reconciliation step.

**Decision driver (one sentence):** the one-off audit found real, previously-unknown decay and no
standing mechanism would have caught it, so the audit method itself — proven effective on this
corpus — should become a named, repeatable skill rather than a finding that ages out the same way
the ADRs it found did.

---

## §2 — Decision

**Ratify `.claude/skills/adr-decay-audit/SKILL.md`** (full text landed alongside this ADR) as a
standing skill in this repo's skill set, with the scope, method, and triggers defined in that file.
Summary (the skill file is canonical; this is a pointer, not a retelling):

1. **Scope:** periodic/triggered sweep of the Accepted-ADR corpus for continued applicability,
   distinct from and complementary to Rule 6 skew-audit, `programme-audit`, and `blast-radius`.
2. **Method:** two-phase batch-scan-then-adversarial-verify (inline for small corpora, fan-out
   workflow above a rough 30-ADR threshold), producing a four-way verdict per ADR
   (`STILL_APPLICABLE` / `DECAYED_DOCUMENTED` / `DECAYED_UNDOCUMENTED` / `UNCERTAIN`).
3. **Triggers:** piggybacks on `programme-audit`'s existing quarterly cadence (no new standing
   calendar trigger) plus named event triggers (pre-snapshot/handoff, large ADR-volume growth since
   last sweep, operator request, a discovered undischarged falsifier on any single ADR).
4. **Discipline carried over from `programme-audit`:** `UNCERTAIN` is a verdict requiring a named
   re-test condition and date, not an open-ended punt; a finding is not closed until it has a named
   remediation and owner; the audit itself is watched for going ceremonial across consecutive
   clean runs.
5. **Remediation weight:** per the ceremony-tiering ADR, a discharge addendum recording drift on an
   existing ADR does not itself require a fresh full-ceremony ADR — only a remediation that changes
   a rule/gate/convention going forward does.

**Effective:** immediately upon acceptance (i.e., upon this PR's merge — see §Status).

**Not decided here:** remediation of the specific findings in §1. Those are the operator's/session's
own follow-up (a short discharge addendum on each of the two undocumented ADRs, and a correction to
the Great Prune ADR / CLAUDE.md pointer), tracked separately from this process ratification.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Extend `programme-audit` to cover per-ADR applicability directly**, rather than a new sibling skill | `programme-audit`'s own two-layer architecture rule (meta vs. object layer, each judged on its own evidence, no cross-layer citation) is load-bearing to how it stays disciplined. A per-decision applicability check is a different question shape (binary per-file fact-check vs. Lakatos programme diagnostic) and would either dilute that discipline or get bolted on as an eighth diagnostic question that doesn't fit the other seven's structure. A sibling skill that explicitly defers programme-level verdicts to `programme-audit` (§Boundary in the skill file) keeps both clean. |
| **Fold this into Rule 6 skew-audit** | Rule 6's trigger (a version-lock event) and scope (Code:-pointer/version-mention hygiene inside a bounded commit window) are both narrower by design, and that narrowness is what keeps it cheap enough to run on every lock. Widening its scope to full-corpus applicability would turn a fast, targeted check into a slow, broad one and blur why it exists. |
| **No standing skill — treat this as a one-off** | This is what the gap already was, and it is exactly the failure mode that produced the two undocumented findings in §1: a decision's accuracy checked once, at authoring time, and never again unless someone happens to reread it. Declining to name a repeatable process here reproduces the problem this ADR exists to close. |
| **Wait for `stealth/ox-alpha` review before ratifying the skill** | Attempted this session (§0); no credential reached this remote container, and the operator elected to proceed without it rather than block on external-tool access. The skill draft got a documented adversarial self-review instead (see the skill file's traps #1, #6, #7, and the scale/UNCERTAIN-discipline additions, all added during that self-review, not present in the first draft). This is a real, if lesser, substitute — logged honestly rather than presented as equivalent to the external pass. |

---

## §4 — Falsifier (revert trigger)

**H:** a periodic/triggered two-phase sweep of the Accepted-ADR corpus catches real, otherwise-
undetected decay (undocumented drift between an ADR's claim and current repo state) at a rate that
justifies its running cost, without producing a high rate of false positives that erode trust in its
verdicts.

**Revert trigger:** if either (a) three consecutive full runs each find zero `DECAYED_UNDOCUMENTED`
cases *and* a hand spot-check of one run's Phase-1 evidence (per the skill's own trap #7) finds the
scan was still genuinely reading files (i.e., true negative, not a rubber-stamped run) — at that
point the cadence should be stretched, not the skill killed, so this is a tuning trigger, not a
falsifier — or (b) two consecutive runs each produce a `DECAYED_UNDOCUMENTED` or `DECAYED_DOCUMENTED`
verdict that a subsequent hand-check shows was wrong (a real false positive/negative, not a
close-call `UNCERTAIN`), the method needs revision before a third run.

**Revert action:** if (b) fires twice, author a new ADR superseding this one with a corrected
method (tighter Phase-2 framing, a different verdict taxonomy, or a smaller/larger batch default),
citing the two dated false verdicts as evidence. Do not silently patch the skill file without a
superseding ADR — per this ADR's own limb-4 logic, a method change is itself a convention change.

**Trigger check schedule:** reviewed at the third full run of this skill (whichever comes first —
cadence or event trigger), and at every quarterly `programme-audit` cycle thereafter, per the
skill's own "audit itself going ceremonial" trap.

---

## §5 — Forbidden moves (under this ADR)

- **Running this skill's Phase 2 (verify) fan-out across the *entire* corpus instead of only the
  Phase-1-flagged subset** — defeats the barrier-cost discipline the skill file names explicitly;
  most of a healthy corpus should clear Phase 1 without needing independent re-verification.
- **Treating a `DECAYED_UNDOCUMENTED` finding as closed on discovery alone** — per the skill's trap
  #6, it needs a named remediation and owner (fixed same-session, or logged forward), not just a
  report.
- **Escalating every remediation addendum into its own full ADR** — per §2 item 5 and the ceremony-
  tiering ADR, a fact-recording discharge addendum is not itself new doctrine; only escalate if the
  remediation changes a rule/gate/convention.
- **Adding a second standing calendar trigger alongside `programme-audit`'s** — the skill file is
  explicit that this creates the drift-prone independent-clocks problem it exists partly to avoid
  reproducing elsewhere in the repo's own audit apparatus.
- **Treating a schema-valid but content-degenerate Phase-2 result as a real verification** — this
  session's own run produced exactly one such case (a verify call whose reasoning/action fields were
  literally placeholder text while still carrying a verdict); the skill's trap #1 exists because of
  that concrete incident, not a hypothetical one.
- **Presenting a future self-review as an external adversarial pass, or vice versa** — this ADR
  itself did not get the `ox-alpha` pass its sibling ADR's pattern calls for (§0, §3); that is
  recorded plainly here rather than elided. The same standard applies to this skill's own future
  outputs: if a run substitutes self-review for an intended external check, say so in the artifact.

---

## §6 — Consequences

**Positive consequences:**
- Closes a real, demonstrated gap: two previously-undocumented decayed decisions were found in the
  corpus's very first full sweep, one of them (the Great Prune retrieval-command claim) sitting in
  the file every session reads first.
- Reuses `programme-audit`'s existing quarterly cadence rather than adding a new clock, and reuses
  `brief-authoring`'s audit-note template rather than inventing a new artifact shape.
- Names the exact operational failure modes this session actually hit while building it (a
  degenerate structured-output result, an ungrounded batch-size default, an unbounded `UNCERTAIN`)
  as traps in the skill file itself, rather than leaving them to be rediscovered by the next run.

**Negative consequences (real cost, not theatrical):**
- Adds a recurring review obligation (piggybacked on an existing cadence, but not zero-cost — a
  full-corpus sweep at this repo's current size is a genuine multi-agent workflow run, not a quick
  grep).
- The one-off audit's own three `DECAYED_UNDOCUMENTED`/`DECAYED_DOCUMENTED`-adjacent findings named
  in §1 are not remediated by this ADR — ratifying the *process* does not retroactively fix the
  *findings*. Left undone, that gap looks the same as the problem this ADR names.

**Risks (probabilistic):**
- The skill could itself go ceremonial after a few clean runs (named directly as trap #7); mitigated
  only by the spot-check discipline in §4's tuning trigger, which depends on someone actually doing
  it.
- Without the `ox-alpha` adversarial pass, this skill draft carries a lower-confidence review than
  its sibling ADR's own validated pattern — mitigated by the self-review documented in §3, not
  eliminated. Revert trigger (b) in §4 is the backstop if that lower confidence manifests as real
  method errors.

**Downstream artifacts that need updating (this session):**
- `.claude/skills/adr-decay-audit/SKILL.md` — new file, landed alongside this ADR.
- `docs/adr/INDEX.md` — regenerate via `python scripts/check_adr_graph.py --regenerate-index`
  (index is derived; do not hand-edit).
- `docs/SESSIONS.md` — this session's entry.
- **Not** in this ADR's scope: the three §1 findings' own remediation (separate short addenda, not
  bundled here to keep this ADR's diff reviewable as a process decision on its own).

---

## §7 — Implementation plan

- **Phase 0** — §0 reads verified this session (anchors above).
- **Phase 1** — author this ADR + the skill file.
- **Phase 2** — regenerate `docs/adr/INDEX.md`; add `docs/SESSIONS.md` entry.
- **Phase 3** — verification block below executes; status stays `Proposed` pending operator
  PR review/merge (see §Status) — this ADR does not self-ratify.

---

## §10 — Audit hooks (runnable)

```bash
# Discipline check
python scripts/check_brief.py docs/adr/2026-08-23-adr-decay-audit-skill-ratification.md --type adr

# ADR lifecycle graph -- header fields, edges, INDEX sync
python scripts/check_adr_graph.py

# Skill file landed
test -f .claude/skills/adr-decay-audit/SKILL.md && echo "OK: skill present"

# This ADR changed no locked/live-risk surface
git diff --stat HEAD -- core/ ops/ | grep -E "dd_protection|firm_rules|c1_rail" && echo "UNEXPECTED" || echo "OK: none touched"

# The two §1 undocumented findings remain open until separately remediated (tracked, not silently closed here)
grep -n "Striker 1.00%" docs/adr/2026-04-17-portfolio-allocations.md docs/adr/INDEX.md
grep -n "sits at the head" docs/adr/2026-06-23-tv-backtest-egress-automation.md

# §4 trigger reminder -- re-check at the skill's own third full run, and every quarterly programme audit thereafter
```

---

## Verification

```bash
# Discipline checks (mechanical)
python scripts/check_brief.py docs/adr/2026-08-23-adr-decay-audit-skill-ratification.md --type adr
# Expected: exit 0 / no HARD violations

python scripts/check_adr_graph.py
# Expected: exit 0

# Production-source verification (§0 anchors)
git log -1 --format='%h %ad' --date=short -- CLAUDE.md                                            # 0723587 2026-08-22
git log -1 --format='%h %ad' --date=short -- docs/operational_rules.md                            # e159743 2026-08-22
git log -1 --format='%h %ad' --date=short -- .claude/skills/programme-audit/SKILL.md              # 31fd642 2026-08-19
git log -1 --format='%h %ad' --date=short -- docs/adr/2026-08-08-adr-ceremony-tiering.md          # 31fd642 2026-08-19
git log -1 --format='%h %ad' --date=short -- docs/adr/2026-08-22-ox-alpha-adversarial-lens-scope.md  # b2e5f15 2026-08-22

# No live-risk/locked source touched
git diff --stat HEAD -- core/ | grep -E "dd_protection|firm_rules|params.toml" || echo "none (expected)"
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-23 | Initial authoring — process ratification for the `adr-decay-audit` skill, following the one-off audit this session ran on operator request; `ox-alpha` external adversarial pass attempted, not completed (no credential reachable this session), self-review substituted and documented | Joshua (direction) + Claude Code |
