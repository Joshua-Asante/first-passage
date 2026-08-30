# [Q-X] — [Short question name]

**Status:** `OPEN` | `OPEN — DRAFT (pre-lock)` | `CLOSED-RESOLVED` | `CLOSED-FALSIFIED` | `CLOSED-AMBIGUOUS-HOLD` | `SUPERSEDED`
**Authored:** YYYY-MM-DD
**Closed:** YYYY-MM-DD (or `N/A` while OPEN)
**Authors:** Joshua + claude.ai (advisor) | + CC (execution)
**Parent question:** Q-Y (if forked from a gated parent) or `N/A`
**Sub-questions opened:** Q-X.a, Q-X.b (if applicable)
**Loop:** Inquire-phase Pre-Q — [one-sentence statement of what gates closure]
**Artifact path:** `docs/briefs/Q-X-name.md`

---

## §0 — Rule 0 reads (production-source verification)

Files read **before** authoring this brief. Each line must include a verification anchor (commit hash, `last-modified` date from `stat`, or `git log -1 -- <file>` timestamp). If §0 is empty or "TBD", the brief fails Rule 0.

If authored in an environment without filesystem access to the repo (web-Claude session), mark each path `[§0-pending — read in Claude Code session before lock]` and the §0 reads become a Phase 0 task in the companion CC handoff. Do NOT proceed to lock without §0 anchors populated.

- `path/to/file.py` — anchor: `<commit_hash>` (verified `git log -1 -- path/to/file.py` on YYYY-MM-DD)
- `path/to/config.yaml` — anchor: `last-modified YYYY-MM-DD` (per `stat`)
- `Notion: <page_title>` — anchor: page ID `<id>` (verified existence on YYYY-MM-DD)
- `docs/adr/NNN-prior-decision.md` — anchor: `<commit_hash>` (verified on YYYY-MM-DD)

---

## §1 — Context & motivation

What observation triggered this question? What is the standing doctrine that bears on it (Core Principles, prior ADRs, lessons registries)? Connect to existing structure — orphan briefs accumulate as noise (Known Trap #8).

[2–4 sentences. Name the dated incident or finding that prompted the question. Cite the doctrine line being tested.]

---

## §2 — Prior art / lineage

Related questions, prior briefs, doctrine that bears on this. Include:
- Prior Q-X briefs touching the same surface (with closure verdict)
- Relevant ADRs (with status)
- Relevant lessons (E1, E2, methodology lesson registry — with dollar anchor where applicable)
- If forked from Q-Y: state the fork condition and what the parent gate concluded

[Bulleted list. One sentence justification each. Empty lineage is acceptable IF the question is genuinely novel; state this explicitly rather than leaving the section blank.]

---

## §3 — Question (Q-X)

**Pre-Q gate test (Discipline Check #5):** rephrase the question to name only the symptom, not the fix. If the symptom-only rephrase is impossible, the question itself bakes in a solution — return to inqhiori.

- **Bad form:** "Should we add an X filter to capture Y?"
- **Good form:** "What is the cost of the current pattern Y, and what alternative architectures could address it?"

**Q-X:** [The question, in good form. One sentence.]

---

## §4 — Falsifiable hypothesis (H-X)

A specific, testable claim. The required form: "If [observation], then [conclusion]; otherwise [alternative conclusion]." Briefs that conclude "look further" without a binary outcome fail Discipline Check #2.

**H-X:** [The hypothesis.]

**Reject H-X if:** [specific numerical / statistical condition that triggers FALSIFIED]
**Accept H-X if:** [specific numerical / statistical condition that triggers RESOLVED]
**Ambiguous-hold if:** [specific condition that triggers CLOSED-AMBIGUOUS-HOLD with re-test window]

---

## §5 — Forbidden moves

Moves that are tempting but ruled out, with the reason each is ruled out. §5 must list moves the author genuinely considered or was tempted by — not theatrical lists of things never on the table (Discipline Check #3, Known Trap #4).

The check: would removing this section change behavior? If no, it's ceremony; rewrite.

- **[Forbidden move 1]** — ruled out because [specific methodological reason, with citation to prior lesson or doctrine where applicable].
- **[Forbidden move 2]** — ruled out because [reason].
- **[Forbidden D-test]** — outcome-conditional D-tests (e.g., "filter out tail losses, then test if tail risk improves") are categorically forbidden; they encode the conclusion into the analysis.

---

## §6 — Gate criteria (closure verdict)

Verdicts must be binary in trigger; "when we know more" is not a gate (Discipline Check #4, Known Trap #5).

| Verdict | Trigger condition | Disposition (typed: INTEGRATE \| ITERATE \| STOP) |
|---|---|---|
| `RESOLVED` | [specific condition, e.g., "Fisher exact p<0.05 AND Rule-1 bootstrap lift >0 AND regime-robustness gate passes H1↔H2 PF spread <10pp"] | `INTEGRATE — [the commit: promote / lock / state-flip + re-validation]` |
| `FALSIFIED` | [specific condition, e.g., "anchor row sits at <50th percentile of mechanism distribution"] | `STOP — [re-proposal bar: new mechanism evidence, not new parameters]` |
| `AMBIGUOUS-HOLD` | [specific condition, e.g., "primary gate passes but regime-robustness gate fails decisively"] | `ITERATE — [return target: Q / H / Investigate / Identify / dated packet; re-test window YYYY-MM-DD]` |

**Disposition column is typed** per `docs/adr/2026-08-04-iterate-closure-exit-mandatory.md`: each verdict row pre-registers exactly one of `INTEGRATE` / `ITERATE` / `STOP` plus its concrete action. Default map (guidance, not law): RESOLVED → INTEGRATE; FALSIFIED → STOP; AMBIGUOUS / VOID / ABORT → ITERATE; MOOT → STOP (operator-stopped closures are not pre-registrable and default with MOOT). The closure discharges this column in its mandatory Iterate block (§9) — by default the pre-registered branch; electing a different branch at closure is legitimate judgment, not a Trap-#12 amendment, provided the block quotes the frozen row and states why the other branch fired. Where routing is unknowable at pre-registration (AMBIGUOUS especially), pre-register the branch coarsely and choose the return target at closure.

**Pre-registered before any data touches analysis.** If §6 is amended mid-investigation to match emerging evidence, this is `p`-hacking at the methodology layer (Known Trap #12). Repair: close the current brief AMBIGUOUS, capture why, open fresh brief with new criteria stated up front. The cross-brief form — re-opening a sibling Q with the same H and looser gates — is the same trap and equally forbidden.

---

## §7 — Execution plan (if applicable; otherwise hand to CC handoff)

If this brief is self-executing (small, mechanical, single session), enumerate the steps below. If execution requires a fresh Claude Code session, this section reads "See companion CC handoff brief at `docs/briefs/handoffs/YYYY-MM-DD-cc-handoff-Q-X.md`" and the steps live there.

- **Phase 0 — Rule-0 reads.** [Specific files to `cat`/`git log` before any analysis.]
- **Phase 1 — [analysis step].** [Specific script, specific output expected.]
- **Phase 2 — [analysis step].** [Specific script, specific output expected.]
- **Phase 3 — Verdict assertion.** [Run the §6 gate against actual numbers; produce closure artifact per §9.]

---

## §8 — Verdict pre-registration (mandatory before Phase 1)

A separate file at `docs/briefs/pre-registration/Q-X-verdict-preregistration.md` containing the §6 table above plus the exact threshold numbers, written and committed BEFORE any analysis script runs. The closure record in §9 references this file by commit hash.

**Completeness check (two-implementer test):** before committing this file, ask — would two
independent implementers compute identical numbers from the §6 table + threshold prose alone? If
not (an ambiguous conditioning/aggregation phrase, a statistic with more than one defensible
reading), the pre-registration must also ship reference code or a worked numeric example on
synthetic data; prose alone does not satisfy this section. Standing doctrine:
`docs/adr/2026-07-11-tradable-anomalies-statistics-adoption.md` Addendum 2026-08-29.

Pre-registration commit hash: `<populated at pre-registration commit time>`
Pre-registration date: YYYY-MM-DD

---

## §9 — Closure record format

When the verdict gate fires, produce the closure artifact from the canonical template `references/closure_record.md`. Sentinel-format convention: do NOT produce a `recommendation.md` for non-PROMOTE verdicts. The closure record is required regardless.

- **If RESOLVED:** `docs/briefs/closures/Q-X-closure-resolved.md` + (if PROMOTE) `recommendation.md`
- **If FALSIFIED:** `docs/briefs/closures/Q-X-closure-falsified.md` (no recommendation.md)
- **If AMBIGUOUS-HOLD:** `docs/briefs/closures/Q-X-closure-ambiguous.md` with explicit re-test trigger and date

Closure record must include: verdict, anchor numbers vs gate thresholds, what the pre-registration predicted vs what actually happened, lesson candidates (with dollar anchor or dated incident — Known Trap #9), **and the mandatory typed `## Iterate` block** discharging this brief's §6 Disposition column (Next: INTEGRATE | ITERATE | STOP, entry packet, stop rule, board write) — a closure without it is incomplete, same weight as a missing §6 assertion (`docs/adr/2026-08-04-iterate-closure-exit-mandatory.md`; pre-commit gate 14 checks the tokens).

---

## §10 — Audit hooks (runnable, not vague)

Commands or checks that can be mechanically executed later. "Review at quarterly check-in" is not an audit hook (Discipline Check #6, Known Trap #6).

```bash
# Confirm §0 anchors still resolve
git log -1 -- path/to/file.py | grep <commit_hash>

# Cross-reference cited Notion page IDs (Known Trap #7)
# Manually verify page <id> exists with title "<title>" on YYYY-MM-DD

# Re-run the gate-firing assertion (if RESOLVED/FALSIFIED)
python scripts/<analysis_script>.py --reproduce-q-x

# Regime-robustness re-test trigger (if AMBIGUOUS-HOLD)
# Re-run on YYYY-MM-DD when N>= [threshold] additional trades accumulate
```

---

## Verification

```bash
# Discipline checks (mechanical) — inquire
$ python scripts/check_brief.py <this-file>.md --type inquire
# Expected: RESULT: well-formed  (applicable mechanical checks for this type)

# Production-source verification (Rule 0 confirmation)
$ <grep / cat / git log commands that confirm §0 anchors>

# Cross-reference verification (cited facts match canonical sources)
$ <grep commands that verify cited numbers / commit hashes / page IDs>

# Pre-registration commit verification
$ git log --oneline docs/briefs/pre-registration/Q-X-verdict-preregistration.md
# Expected: pre-registration commit predates first analysis script run
```

If any verification command fails, the brief is not complete. Re-author the section that broke; do not handwave.

---

## Pre-Lock Checklist (DRAFT briefs only)

Remove this section once the brief is locked.

- [ ] All §0 paths read and anchored with commit hash / `last-modified` date
- [ ] §3 question passes the symptom-only rephrase test
- [ ] §4 hypothesis is genuinely falsifiable (binary triggers in §6)
- [ ] §5 forbidden moves are genuinely tempting, not strawmen
- [ ] §6 gates have specific numerical triggers (no "when we know more")
- [ ] §8 pre-registration committed BEFORE Phase 1 runs
- [ ] §10 audit hooks are runnable commands, not review notes
- [ ] Verification block executed and passing
