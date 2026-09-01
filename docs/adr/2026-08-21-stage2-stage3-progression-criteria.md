# ADR — Stage 2 → Stage 3 autonomy progression criteria

**Status:** `Accepted` — ratified 2026-08-21 by operator (Joshua)
**Decision date:** 2026-08-21
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Authors:** Joshua (direction + ruling) + claude.ai advisor (drafted, mobile session) + Claude Code (Rule-0 re-verification + landing, this session)
**Related:** [`2026-08-14-cc-cursor-autonomous-loop.md`](2026-08-14-cc-cursor-autonomous-loop.md) (defines the auto-merge-forbidden surface this ADR does not alter) · [`2026-08-06-candidate-call1-action-on-breach.md`](2026-08-06-candidate-call1-action-on-breach.md) (defines the "item 3" write-back this ADR keeps dormant through Phase 3, §3) · [`docs/notes/autonomy_staging/error_log.md`](../notes/autonomy_staging/error_log.md) (the companion Phase-1 log, seeded same-day)
**Layer:** infrastructure / governance

This does not modify risk-control code, locked parameters, or production strategy logic. It governs the *measurement and gating process* by which the existing autonomous CC/Cursor merge lane (`2026-08-14-cc-cursor-autonomous-loop.md`) may be widened toward a stage-three tier.

---

## §0 — Rule 0 reads (production-source verification)

Originally authored 2026-08-21 in a mobile advisory session without live GitHub/repo access; the §1 facts were as last verified in a same-day desktop session, not re-verified live at authoring time (disclosed in the original draft). Re-verified live in this session before landing:

- `docs/adr/2026-08-14-cc-cursor-autonomous-loop.md` — read in full this session, anchor `2e4d063` (2026-08-18 12:01:23 -0400). Confirmed `Status: Accepted`; confirmed its auto-merge-forbidden surface list (§2) literally includes `core/lifecycle.py` and `docs/adr/**` — both cited by this ADR and by the error log's row 1.
- `docs/adr/2026-08-06-candidate-call1-action-on-breach.md` — anchor `fc95425` (2026-08-21 19:14:51 +0000, this session's own Accept commit). `lab/discovery/lifecycle_call1/demote_writer.py`'s dormant status (no live caller anywhere in the repo) reconfirmed this session via repo-wide grep before this ADR was authored.
- PR [#86](https://github.com/Joshua-Asante/first-passage/pull/86) — `gh pr view`-equivalent this session: merged, `merged_at: 2026-08-21T19:46:...Z`, merged by Joshua.
- PR [#87](https://github.com/Joshua-Asante/first-passage/pull/87) — `gh pr view`-equivalent this session: merged 2026-08-21T19:40:47Z. Its own body independently corroborates the error log's row 3 (`validation-controls` red since PR #78, surfaced again on #83/#84/#86 — confirms the drift was pre-existing and repo-wide, not specific to any one PR).
- `docs/notes/autonomy_staging/error_log.md` — created this session (did not exist before), seeded with the three rows named in §2 below, each independently re-verified (row 1's citation was re-traced to its root cause — a merge-commit misattribution — and corrected on the public PR #86 record: [comment](https://github.com/Joshua-Asante/first-passage/pull/86#issuecomment-5377130526)).
- `.claude/skills/brief-authoring/references/adr.md` — read this session to confirm section structure and the tier test. This ADR clears FULL-tier limb 4 (creates doctrine: a phased gate binding future autonomous-lane work).
- Downstream sweep (template §7 Phase 2, run this session): `grep -rln "autonomy.staging\|Stage 2.*Stage 3\|stage2.*stage3\|autonomy_staging"` across the repo returned two hits, both false positives on inspection — `STATE.md` (regex over-match, no actual "autonomy" occurrence) and `docs/briefs/rnd-pipeline/2026-07-12-cursor-handoff-stage-2-4-runner.md` (an unrelated discovery-pipeline "stage" numbering). No existing artifact restates or needs updating for this decision; §6's downstream list is this ADR plus the new log file, both landed in this commit.

**Gitignore pre-flight:** no `.pine` read; governance/process ADR only.

---

## §1 — Context

Stage two (current): reversible, narrow-surface autonomy without human oversight; anything risk-adjacent stays human-gated. Stage three (target): autonomous action inside pre-authorized bounds on risk-adjacent work — still hard-stopped, still fully audited.

Trigger: the 2026-08-21 PR #86/#87 audit surfaced three human-caught errors in one session — a fabricated PR-#37 citation in CC's closure report, a redundant-build belief CC held before self-correcting, and a `validation-controls` CI gate silently drifted to exactly its 0.80 failure boundary on `main`, unnoticed pre-PR. All three were caught by manual, tool-based cross-checking (`gh` CLI / GitHub API against actual repo state), not by the autonomous process catching itself.

This is one session's anecdote, not a track record. This ADR exists to convert it into one before stage three is considered.

**Decision driver (one sentence):** three catches in one session is a live prompt to measure the error rate before authorizing anything wider, not a reason to either panic-freeze the current lane or wave the anecdote through as sufficient evidence either way.

---

## §2 — Decision

**Decision:** Establish a three-phase, criteria-gated progression from the current (stage-two) lane to stage-three eligibility. A phase advances only when its §6 exit criteria are met — calendar time alone never advances a phase (§5).

**Effective:** immediately upon acceptance.
**Scope:** the autonomous CC/Cursor dispatch/merge lane defined in `2026-08-14-cc-cursor-autonomous-loop.md`; any future proposal to widen that lane's forbidden-surface list or gate conditions.

**Phase 1 — Measurement.** No new capability. Every autonomous CC/Cursor PR gets the same audit-first review already in practice. New requirement: every audited session — including clean ones — gets logged in [`docs/notes/autonomy_staging/error_log.md`](../notes/autonomy_staging/error_log.md) (date, artifact, claim checked, caught Y/N, error type, how caught). Seed data: 2026-08-21's three catches, logged as rows 1–3 in the companion file (row 1 independently re-verified and corrected this session).

**Phase 2 — Cheap verification tooling.** Begins only once Phase 1 exits. Deliverable: lightweight automated cross-checks targeting whatever error categories Phase 1 actually produced (e.g., an automated claimed-PR-vs-`gh pr view` check, if citation errors recur). Left deliberately unspecified here — building it before the taxonomy exists risks building the wrong checks.

**Phase 3 — Gradual lane expansion.** Begins only once Phase 1 and Phase 2 both exit. Widen the autonomous lane by one increment at a time (e.g., one new file-class), re-measuring after each before widening further. The forbidden-surface list in `2026-08-14-cc-cursor-autonomous-loop.md` stays completely frozen through all of Phase 3 (§5) — including the `core/lifecycle.py` docstring fix flagged during the PR #86 work, which stays a manual edit like any other forbidden-surface change regardless of triviality.

---

## §3 — Explicitly out of scope

This ADR does not authorize wiring `lab/discovery/lifecycle_call1/demote_writer.py` live, does not authorize a live PF source into that harness, and is not itself stage three. Meeting Phase 3's exit criteria makes the write-back an *eligible topic* for its own future ADR — not an automatic green light.

---

## §4 — Falsifiable hypothesis

**H:** Ten consecutive Phase-1-logged sessions with no *new* error category appearing (only already-catalogued categories recur, or zero errors) is sufficient evidence that the current lane's error surface is understood well enough to start building targeted verification tooling (Phase 2).

**Falsifier / revert trigger:** if a novel error category appears at session N before ten consecutive clean sessions accrue, H is not yet supported — the consecutive-clean count resets from N+1 (prior data is retained; only the streak resets) and Phase 1 continues. There is no revert *action* beyond staying in Phase 1 — this is a not-yet-met condition, not a decision to unwind.

**Trigger check schedule:** every Phase-1-logged session (the log itself is the running check); rides the 2026-11-08 programme-audit cadence for a standing review regardless of streak state.

---

## §5 — Forbidden moves

- **Advancing a phase on calendar time alone without §6 criteria met.**
- **Skipping the log entry for a clean session** — destroys the denominator, silently inflates the apparent catch rate.
- **Building Phase 2 tooling before Phase 1 produces a real error taxonomy.**
- **Widening more than one lane-increment at a time in Phase 3.**
- **Touching any forbidden-surface-list file (`2026-08-14-cc-cursor-autonomous-loop.md` §2) through the autonomous lane during Phases 1–3, including trivial/docstring-only edits** — the list is mechanical/file-based specifically so it isn't subject to case-by-case rationalization.
- **Editing an error-log row in place once logged** — corrections land as a new row citing the row they correct (per the log file's own header), never a silent in-place edit; this mirrors the repo's standing "corrected, not silently changed" convention.

---

## §6 — Gate criteria (binary)

- **Phase 1 → 2:** EXITED when §4's ten-consecutive-clean condition is met. Otherwise not yet.
- **Phase 2 → 3:** EXITED when the verification tooling, replayed against every logged Phase 1 case, independently flags 100% of them (no false negatives on historical cases). Any miss on replay → repair the tooling, do not lower the bar.
- **Phase 3 (per increment):** EXITED for that increment when ~10 sessions at the new surface show an error rate not measurably worse than the Phase 1 baseline (same §4 logic, applied to the new surface). Phase 3 is fully exited once all planned increments have individually exited.

---

## §7 — Consequences

**Positive consequences:**
- The informal "caught it tonight" pattern becomes a dated, logged practice — phase transitions become auditable rather than felt.
- A future stage-three proposal has a real denominator to cite instead of an anecdote.

**Negative consequences (real cost, not theatrical):**
- Phase 1 adds real overhead — logging every session, clean or not — the same cost as any Rule-0 discipline, in exchange for not advancing autonomy on vibes.

**Risks:**
- The log itself could be skipped or under-logged if it isn't load-bearing to any gate a session actually has to clear before finishing — mitigated by making the log a named §5 forbidden-move-to-skip, and by this ADR's own §10 audit hook checking its line count grows.

**Downstream artifacts updated (this commit):**
- [`docs/notes/autonomy_staging/error_log.md`](../notes/autonomy_staging/error_log.md) — created, seeded with rows 1–3.
- [`docs/adr/INDEX.md`](INDEX.md) — regenerated.

What doesn't change: the forbidden-surface list, the human gate on risk-adjacent work, and `demote_writer.py`'s dormant status — all remain exactly as ratified in `2026-08-14-cc-cursor-autonomous-loop.md` until this framework's own criteria say otherwise.

---

## §8 — Open questions (non-gating)

- Exact Phase 3 increment sequence — deferred until Phase 1's taxonomy exists.
- Whether Phase 2 tooling itself gets built inside the autonomous lane or stays human-authored — deferred, likely its own CC handoff brief.
- `docs/briefs/programs/2026-07-17-0808-packet-delta-and-sequence.md`'s relevance to `lifecycle_call1/`'s provenance — **resolved this session, not open**: the file first enters this repo's tracked git history at commit `2e4d063` (a large, unrelated bulk-merge, PR #37, 2026-08-18); the doc-internal "2026-07-14" dating is a content-level claim from `docs/briefs/rnd-pipeline/2026-07-14-cursor-handoff-lifecycle-call1-sigma-harness.md` that predates the 2026-08-14 public-visibility git-history squash and is not independently git-verifiable in this checkout. See error-log row 1.

---

## §9 — Implementation plan

Policy plus one mechanical artifact — no code edits, no forbidden-surface touch.

- **Phase 0** — this ADR + the companion log file, landed together (this commit).
- **Phase 1** — ongoing: every future audited autonomous session logs a row per §2.
- **Phase 2** — grep-sweep (template Known Trap #7), run this session: no downstream consumer found (§0).
- **Phase 3** — `docs/adr/INDEX.md` regenerated; ADR status `Accepted` on landing (no separate Proposed period — authored and ratified in one operator-directed motion, per the change-history table below).

---

## §10 — Audit hooks (runnable)

```bash
# Confirm this ADR's status
grep -m1 "^\*\*Status:\*\*" docs/adr/2026-08-21-stage2-stage3-progression-criteria.md

# Confirm the forbidden-surface list is unchanged since 2026-08-14
git diff 2e4d063..HEAD -- docs/adr/2026-08-14-cc-cursor-autonomous-loop.md
# Expected: empty (no edits since the ADR's own anchor commit)

# Check Phase 1 progress
wc -l docs/notes/autonomy_staging/error_log.md
tail -n 10 docs/notes/autonomy_staging/error_log.md

# Confirm demote_writer.py is still dormant (Phase 3 hasn't silently begun)
grep -rn "demote_writer" core/ ops/ --include="*.py" | grep -v lab/discovery/lifecycle_call1
# Expected: no matches outside lab/discovery/lifecycle_call1/

# Downstream sweep (re-run at any future audit)
grep -rln "autonomy.staging\|Stage 2.*Stage 3\|stage2.*stage3\|autonomy_staging" --include="*.md" . | grep -v docs/adr/2026-08-21-stage2-stage3-progression-criteria.md | grep -v docs/notes/autonomy_staging/error_log.md
```

---

## Verification

```bash
python scripts/check_brief.py docs/adr/2026-08-21-stage2-stage3-progression-criteria.md --type adr
# Expected: PASS (or WARN-only, no HARD)

python scripts/check_adr_graph.py --regenerate-index
python scripts/check_adr_graph.py
# Expected: exit 0

git log -1 -- docs/adr/2026-08-14-cc-cursor-autonomous-loop.md
git log -1 -- docs/adr/2026-08-06-candidate-call1-action-on-breach.md
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-21 | Initial authoring (mobile advisory session, `Proposed` in the working draft, no live repo access) | Joshua + claude.ai advisor |
| 2026-08-21 | Landed and `Accepted` in one motion per direct operator instruction ("log this in the error log for real, and accept the ADR"): Rule-0 re-verified live, error log created + seeded, downstream sweep run, drafting-note artifacts resolved and removed | Joshua + Claude Code |

---

## Addendum 2026-09-01 — Phase 1 logging is dormant

**Diagnostic fact, re-verified via this ADR's own §10 hook:** `docs/notes/autonomy_staging/error_log.md` has received exactly **one** commit in its entire history — `451f56f`, 2026-08-22, the commit that seeded rows 1–3. Zero rows have been logged since. Ten days on, `wc -l` on the file is unchanged (18 lines) and `tail -n 10` still shows only the three 2026-08-21 seed rows and the original "Consecutive-clean streak: 0" tally.

In that same window the autonomous CC/Cursor lane this ADR governs kept producing PR merges across both the `cursor/*` and `claude/*` branch families. §4's falsifiable hypothesis depends on a running consecutive-clean-session count that only the log can supply; with the log static, that count cannot advance in either direction, and §6's Phase 1 → 2 gate cannot be evaluated from current data. §5 already forbids "skipping the log entry for a clean session" — as written, that forbidden move is what appears to be happening across effectively every session since seeding.

**This addendum states the fact only.** Per the audit that surfaced it (`docs/notes/audits/programme-audit/2026-08-31-adr-corpus-audit.md` §6), the disposition — re-arm the logging discipline, narrow the log's scope, or withdraw the Phase-1 measurement gate — is an operator ruling not made here. `demote_writer.py` stays dormant and the forbidden-surface list stays frozen regardless of which way this ruling goes (§3, §5).

**Operator ruling:** _pending — re-arm / narrow / withdraw (fill in when ratified)._
