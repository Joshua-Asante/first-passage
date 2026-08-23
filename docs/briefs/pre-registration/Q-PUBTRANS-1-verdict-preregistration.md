# Q-PUBTRANS-1 — Verdict pre-registration (H-PUBTRANS)

**Frozen:** 2026-08-18, at brief-authoring time, before any limb was read — per the parent
brief's own §8 ("§4 above **is** the frozen decision rule... No separate pre-registration file
is needed beyond it"). This file is a mechanical backfill of that already-satisfied requirement,
authored 2026-08-23 at Phase 1 execution time, to give the artifact the same discoverable
sibling-path shape as every other Q's `pre-registration/` file (Q-CAPBAND-1 precedent) — it
freezes nothing that was not already frozen in the brief itself on 2026-08-18. Parent brief:
[`../Q-PUBTRANS-1-public-transition-completeness.md`](../Q-PUBTRANS-1-public-transition-completeness.md).
**Execution requires a separate operator GO** (recorded 2026-08-23 — see closure).

---

## §A — Pinned inputs (frozen; no substitutions)

| Input | Value | Source |
|---|---|---|
| Limb-B5 test | zero occurrences of the real account identifier / account numeric ID / real dollar balance-fill figures in the public repo's working tree + full git history | Brief §4 |
| Limb-D8 test | zero of {SL type/level, TP type/level, ATR multiplier, session window, BE trigger, trail rule} concretely/trivially recoverable for any of the 4 locked legs, in the tracked non-gitignored corpus | Brief §4 |
| Limb-D9 test | all pre-transition open sentinel Action items (brief states 11: 7 PREREG-RUNEDIT + 4 PREREG-SAMECOMMIT) have a retrievable disposition record (this repo, private archive, or operator confirmation) | Brief §4 |
| D8 grep corpus | `CLAUDE.md core/firm_rules.py core/strategies/_archive/*/LOCK.md docs/methodology/ docs/adr/` | Brief §10 |
| D9 audit hooks | `git log --all -- docs/notes/sentinel/queue.md`; `git merge-base --is-ancestor 19beee2 HEAD` (expect exit 1); ID-stem greps of STATE.md/SESSIONS.md/closures | Brief §10 |
| B5 audit hooks | coarse regex pre-check (agent-doable); literal-value greps (operator-only, needs withheld values) | ADR §10 + Brief §10 |

**The three limbs are closed at these three.** No limb may be added, swapped, or reframed at execution time.

## §B — Decision rule (verbatim mirror of Brief §6)

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED` | All three limbs individually clear: B5 clean (0 literal-value hits), D8 clean (0/6 concrete fields found), D9 clean (all items have a retrievable disposition record) | INTEGRATE |
| `FALSIFIED` | Any one limb fails: B5 finds ≥1 real literal, OR D8 finds ≥1 of the six fields concretely recoverable, OR D9 finds ≥1 item with no disposition record anywhere reachable | STOP (failed limb's gap) + ITERATE (brief as a whole) |
| `AMBIGUOUS-HOLD` | D8 checked and clean, but B5 and/or D9's remaining step has not been executed | ITERATE — name, don't open, the resolving operator step |

**Any single limb failure means the transition did not complete cleanly** (Brief §4, verbatim).

## §C — Method

Binary locational reads of already-recorded facts plus the agent-executable greps named in
Brief §10 / ADR §10. No new spend, no guessing at withheld values (Brief §5 forbidden move #2).

## §D — Pinned ex-ante expectation (surprise marker)

**Predicted (as framed by the brief and the orchestrating task at GO time): `BLOCKED-NEEDS-OPERATOR-INPUT`** — Limb-D8 was framed in Brief §7 as "fully agent-executable ($0, ~20-30 min)" and expected to hold, matching the ADR's own accepted residual-risk framing ("sizing/instrument/version only"); the anticipated wall was purely B5 (withheld literal) and D9 (private-archive access). A D8 failure, or a finding that D9's "private archive" premise was itself wrong, would be a **genuine surprise** — recording the prediction so neither outcome can be retrofitted as expected.

## §E — Forbidden moves (inherited from Brief §5, restated for the frozen record)

1. Treating observable publicness / an ADR status flip as proof the B5 safety sweep was re-run.
2. Guessing or reconstructing the real account ID / dollar figures to run Limb-B5.
3. Reading D8's accepted sizing/instrument/version disclosure as evidence about the other six fields.
4. Treating D9's negative greps in this repo as proof of non-disposition (private-archive / operator-confirmation channels are separate).
5. Editing the ADR's Status field, the §10 hooks, or backfilling STATE.md under this brief.

---

**Freeze note:** no limb fact had been read under this brief at the time its §4/§6 were fixed
(2026-08-18). This file's existence does not reopen or re-time that freeze.
