# ADR 2026-08-13 — Dedup-first before new work: wire the existing search tool, generalize Rule 8, add a catalog-collision backstop

**Status:** `Accepted` — operator ruling recorded 2026-08-13 in session, verbatim: *"ratify it and I will spawn as suggested task."* **§7 Phases 1–5 (mechanical wiring) landed** on branch `cursor/dedup-first-mechanical-wiring-0813` the same day; see Change history for the implementation commit. §2's decision remains in force.
**Decision date:** 2026-08-13
**Authors:** Joshua (ruling) + Claude Code (investigation synthesis + drafter)
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Related:** this session's own two incidents (below); [`docs/methodology/strategy_harvest.md`](../methodology/strategy_harvest.md) §2 (the narrowly-scoped precedent this generalizes); [`docs/notes/notice/N-2026-07-26-forced-flow-census.md`](../notes/notice/N-2026-07-26-forced-flow-census.md) (source of the "paste the output" language lifted below); [`docs/briefs/pre-registration/2026-07-27-fts5-delete-falsifier-prereg.md`](../briefs/pre-registration/2026-07-27-fts5-delete-falsifier-prereg.md) / Q-XMEM-1 (a heavier, still-unbuilt adjacent fix — not superseded, not required by this ADR)
**Layer:** methodology

---

## §0 — Rule 0 reads (production-source verification, verified 2026-08-13 at `9bcf3cb`, worktree clean)

| Source | Anchor (`git log -1`) | What it grounds |
|---|---|---|
| [`docs/operational_rules.md`](../operational_rules.md) | `75e54ed` 2026-08-09 | Rule 8 currently has sub-rules 1–7 (§0 discipline for briefs); no sub-rule addresses "search before creating," only "search before deleting" (sub-rule 1) and adjacent moments. Edit-log convention (dated entries, bottom of file) confirmed. |
| [`scripts/check_advisor_dedup.py`](../../scripts/check_advisor_dedup.py) | `1ee6f4c` 2026-07-25 | Full source read. Confirmed: corpus = `docs/briefs/closures/*.md` + `docs/notes/audits/**/*.md` + `docs/SESSIONS.md` (per-`## ` entry) + `lab/CATALOG.md` (per-row) + `docs/rejected_candidates.md` (per-`### ` entry); term-overlap ranking (slug matches weighted ×20 over keyword matches); **always returns exit 0** (line 232, by design — "a search assistant, not a gate"); CLI signature (line 179) takes only a `staged_file: Path` positional argument — **no keyword-string mode exists today**. |
| `.claude/hookify.advisor-dedup-first.local.md` | **untracked** (`git ls-files` returns empty for this path) | The only invocation trigger for `check_advisor_dedup.py` anywhere in the repo. Full content read. Trigger regex: `(Downloads[\\/]\|web.?advisor\|advisor (said\|recommend\|suggest\|staged)\|staged (artifact\|brief\|closure\|gate.audit))` — matches Downloads/advisor-staged-content language only, never "implement X" build-intent phrasing. `.local.md` suffix per this repo's hookify convention means machine-local, never synced across sessions or agents. |
| [`CLAUDE.md`](../../CLAUDE.md) L81-82 | `6db1c29` 2026-08-12 (line introduced by `92b3b78`, 2026-08-09) | Verbatim: *"Open `docs/briefs/INDEX.md` and `lab/CATALOG.md` before searching; **an empty Grep is not evidence of no prior work** — archived bodies live in git history."* Already states the rule this ADR operationalizes, in the single most auto-loaded file in the repo, four days before this session's miss. |
| [`docs/methodology/strategy_harvest.md`](../methodology/strategy_harvest.md) L85 | `74ff47d` 2026-08-13 | Verbatim: *"**Dedup first, before any manifest work:** check `docs/rejected_candidates.md`, the closed discovery manifests, and `docs/methodology/rejected_signals.md`. A screened-dead **class** stays dead under a new citation... Re-proposal bar: new *mechanism evidence*, not new packaging."* The one place a dedup-first rule is already law — scoped exclusively to strategy-candidate harvest intake. |
| [`docs/notes/notice/N-2026-07-26-forced-flow-census.md`](../notes/notice/N-2026-07-26-forced-flow-census.md) L195-208 | `5563cf4` 2026-08-10 | Verbatim: *"The graveyard-adjacency attestation was a field I filled, not a check I ran... **Binding procedure for every future census entry:** Run, and paste the *command output*, for: `rejected_candidates.md` (by mechanism family..."* Source of the "attestation without executed output is void" standard this ADR generalizes past its harvest-only origin. |
| [`scripts/gates.yml`](../../scripts/gates.yml) L83-89 | `0c35fb3` 2026-08-11 | `lab-catalog` gate, `tier: always`, runs `archive_lab_analysis.py --check --catalog-only` on every pre-commit. Confirmed: this is a **structural freshness diff** (does every `lab/analysis/` dir have a matching, current `CATALOG.md` row) — zero semantic/duplication content. It is the mechanism that incidentally caught this session's own duplicate, at pre-commit time, after the engineering effort was already sunk. |
| [`scripts/archive_lab_analysis.py`](../../scripts/archive_lab_analysis.py) | `12126c5` 2026-08-13 | `scan_lab()` already walks every `lab/analysis/<theme>/<slug>/` directory and already knows each slug's theme; `render_catalog()` already derives one-liners. No existing function warns on a *new*, not-yet-committed slug sharing a theme with existing rows — this is additive, not a rewrite. |
| [`.claude/skills/brief-authoring/SKILL.md`](../../.claude/skills/brief-authoring/SKILL.md) | `103365f` 2026-08-11 | Confirmed: contains no reference to `operational_rules.md` §8 or "sub-rule" anywhere. A session reading only the skill (not the operational rules file directly) never sees Rule 8's sub-rules 1–7, including the new sub-rule 8 this ADR adds. |

**Contingency note:** none required — every claim above traces to a file read in full this session, with a fresh `git log -1` anchor at HEAD `9bcf3cb`.

---

## §1 — Context

Two incidents, same session, same day (2026-08-13). First: a large Tradeify-eval-passing research battery was designed; before executing it, a dedicated 5-cluster parallel dedup sweep was run and caught that most of the battery was already answered by three ACTIVE-but-never-closed studies, one of which was findable only by following a citation chain inside an unrelated brief's own §0 reads — a near-miss, caught because a sweep was deliberately run first. Second, immediately after: a task to implement Magdon-Ismail et al. (2004)'s closed-form maximum-drawdown distribution as a `core/mc/simulation.py` regression anchor proceeded straight to WebSearch and implementation with **no search of any kind** against the repo's own state. Roughly five files and real independent numerical engineering later (the build hit and had to solve, via Euler-transformation series acceleration, the same slowly-converging-alternating-series numerical trap the paper itself warns about), it surfaced — only when the pre-commit `lab-catalog` gate flagged `lab/CATALOG.md` as stale — that `lab/analysis/mc/mc_mdd_closed_form_2026-08/` already existed, merged via PR #790 roughly 90 minutes before the session's build began, implementing the identical closed form and already validated against the same Appendix B tables. About half the new work was redundant; it was reworked into an extension of the existing study rather than landed as a duplicate (PR #796).

A dedicated four-lens investigation commissioned the same day found the failure is not a documentation gap. `lab/CATALOG.md` and `docs/SESSIONS.md` both already carried complete, correctly-labeled, already-committed entries for the duplicated work — `git log --oneline -20` alone would have surfaced two commit subjects containing "Magdon" in seconds, before the first WebSearch. `CLAUDE.md` already states the rule in prose, added four days earlier. A purpose-built search tool (`check_advisor_dedup.py`) already indexes exactly the right corpus, but is advisory-only, invoked solely through an **uncommitted, machine-local** hookify trigger scoped to the wrong language ("advisor/Downloads-staged content," never "implement X"). The closest thing to a general dedup-first *rule* — `strategy_harvest.md`'s "dedup first" clause and a 2026-07-26 audit note's own "binding procedure" ("an attestation without executed searches behind it is void") — exists twice in the repo, written by two different incidents, and neither was ever generalized past its origin scope (strategy-candidate harvest intake; one census document class).

**Decision driver (one sentence):** the fix does not need to be invented — three already-designed, already-correct-shaped pieces (a working search tool, a working rule pattern, a working structural gate to extend) are sitting unassembled in the repo, and the cost of leaving them unassembled was just paid twice in one session.

---

## §2 — Decision

**Dedup-first becomes a required, checkable step before opening any new `lab/analysis/<theme>/<slug>/` directory, before scoping new `core/`-adjacent implementation work, and before acting on any task inherited from a "spawned as a separate task" pointer in a memory file or notice.** Operationalized by three additive legs, none of which is a new mechanism:

1. **Commit and broaden the hookify trigger.** Move `.claude/hookify.advisor-dedup-first.local.md` to a tracked path (dropping the `.local` scope) and widen its regex to also match build-intent phrasing (`implement`, `port`, `build .* (as\|for)`, `add .* (closed-form\|algorithm\|anchor) for`), not only advisor/Downloads-staged-content language.
2. **Add Rule 8 sub-rule 8** to `docs/operational_rules.md`, mirroring sub-rule 1's shape ("cross-reference grep before classifying isolated cruft") at the opposite moment — before creation, not before deletion — requiring any brief/session's §0 to paste literal search output (not a conclusion) against `lab/CATALOG.md` and `docs/briefs/INDEX.md` before new implementation work is scoped, using the already-written standard: *"an attestation without executed search output is void."*
3. **Extend `scripts/archive_lab_analysis.py`** with a report-only (fail-open, same posture as `check_advisor_dedup.py`) check that fires when a new, not-yet-committed `lab/analysis/<theme>/<slug>/` directory appears sharing a theme with existing `CATALOG.md` rows, printing those rows to stderr.

Additionally: extend `check_advisor_dedup.py` to accept a short keyword string (not only a staged file path), so it is runnable **before any code exists** — the point in this session's own incident where a check would have mattered.

**Effective:** immediately upon acceptance for the policy (§2 as prose); mechanical edits per §7.
**Scope:** any new `lab/analysis/<theme>/<slug>/` directory; any `core/`-adjacent implementation of an externally-sourced paper, algorithm, or technique; any task picked up on the strength of a "spawned as a separate task" / "TODO" pointer inherited from a memory file or notice, which must be re-checked against current repo state (not trusted on its own text) before being acted on.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Build a new semantic/hard duplicate-detection gate that blocks commits | Already tried and abandoned in this repo: a "C1" status-contradiction semantic join (`project_status_consistency_gate`) went 100% false-positive on its first real run and was dropped — "you cannot infer 'study X is dead' from a link to X inside a dead-section/rejection registry." A precise semantic dedup gate is a known dead end here. |
| Rely on `CLAUDE.md`'s existing prose instruction alone, unenforced | Already in place four days before this session's own miss (added `92b3b78`, 2026-08-09). Ambient prose that nothing checks was already proven insufficient by the incident this ADR is written against. |
| Build the FTS5 search sidecar Q-XMEM-1 pre-authorized (2026-07-27 DELETE-HOLDS) | Real, heavier infrastructure — but its own pre-registered recall floor (0.70) sits **inside** the measured 95% CI ([0.630, 0.792]); even a built, working version misses roughly one probe in four. Not a substitute for a cheap mandatory reflex, and it has sat unbuilt 17+ days past authorization. Out of scope here — not superseded, could layer on top later, does not block this ADR. |
| Status quo — leave `check_advisor_dedup.py` unwired, Rule 8 unextended | Measured cost is no longer hypothetical: two incidents in one session, one costing roughly five files of independently-reinvented numerical engineering. |

---

## §4 — Falsifier (revert trigger)

**H (what this ADR asserts, binary):** wiring the hookify trigger to build-intent language, adding Rule 8 sub-rule 8, and adding the catalog-collision WARN meaningfully reduces the "new work duplicates already-committed ACTIVE prior work" failure class — without reintroducing the false-positive-death mode a hard semantic gate already produced once.

**H is FALSIFIED if any trigger below fires:**

| # | Trigger | Threshold | Action |
|---|---|---|---|
| T1 | The same failure shape recurs after the wired mechanisms are in place and were actually consulted (not skipped) | any single dated incident where the hookify trigger fired, sub-rule 8's pasted-output step ran, and a real duplicate still landed | Diagnose whether the miss is a corpus-coverage gap (escalate toward the FTS5 sidecar) or a scoring/threshold gap (retune `check_advisor_dedup.py`'s `--min-score`) — supersede this ADR's §2 with the finding |
| T2 | The archive_lab_analysis.py WARN produces enough false positives that sessions start ignoring it | ≥3 dated instances of a WARN being dismissed as noise within one quarter | Narrow the theme-overlap heuristic or drop leg 3; sub-rules 1-2 stand regardless |
| T3 | The recurrence rate over the next 90 days matches or exceeds this session's own baseline (2 incidents / 1 session) despite the fix being live | measured at the next quarterly programme audit | Escalate: fund the FTS5 sidecar (Q-XMEM-1) rather than continue treating this as sufficient |

**Not admissible as a revert route:** converting leg 3 (the CATALOG-collision WARN) into a hard commit-blocking gate — that is precisely the dead end §3 already ruled out; a recurrence does not license re-trying it.

**Revert action:** author a superseding ADR naming which leg failed and why. Never edit this ADR's §2 in place.

**Trigger check schedule:** next quarterly programme audit, or immediately on the next dated incident of this exact class, whichever is first.

---

## §5 — Forbidden moves (under this ADR)

- **Building a hard, commit-blocking semantic duplicate gate.** Genuinely the most tempting fix — it would feel more thorough than an advisory warning. Ruled out because it has already been tried in this exact repo and false-positived to death (§3). Stay advisory, always exit 0, same posture as `check_advisor_dedup.py` today.
- **Treating this ADR as closing Q-XMEM-1 / the FTS5 sidecar pre-registration.** It doesn't. Q-XMEM-1 stays `OPEN`, T0 still not started, gated on its own decision.
- **Widening leg 3's WARN into a blocking check "since it's cheap to add `--strict` later."** T2 exists precisely to catch this drift before it happens by accident under time pressure.
- **Loosening the hookify trigger regex or Rule 8 sub-rule 8's requirement without a dated changelog entry.** Silent amendment of a revert-trigger-adjacent mechanism is the same `p`-hacking-at-the-methodology-layer trap Rule 8's own edit log exists to prevent.

---

## §6 — Consequences

**Positive consequences:**
- Closes a class that cost real, measured engineering effort twice in one session, by wiring together pieces that already exist rather than inventing new ones.
- Makes `CLAUDE.md`'s already-stated instruction ("open CATALOG.md and INDEX.md before searching") enforceable — Rule-0-style teeth instead of unenforced ambient prose, mirroring how Rule 0 itself earned its place after the 2026-04-17 dd_protection cycle.
- Generalizes a fix (`strategy_harvest.md`'s dedup-first clause; the 2026-07-26 "paste the output" standard) that has already independently proven itself twice at narrower scope, rather than waiting for a third narrow-scope reinvention.

**Negative consequences (real cost, not theatrical):**
- Adds reading/search time at the start of every new `lab/analysis/` directory or `core/`-adjacent implementation task — the deliberate cost this ADR asks to pay, sized against the alternative (this session's own ~5-file redundant build).
- `archive_lab_analysis.py` gains new maintenance surface (the theme-overlap WARN heuristic) that could itself need tuning.

**Risks (probabilistic, distinct from costs):**
- The broadened hookify regex is still a finite pattern list — it can miss task-shapes nobody has written yet. Mitigated by making Rule 8 sub-rule 8 (a self-directed reflex, not a trigger-dependent catch) the primary mechanism, with the hookify trigger as a secondary backstop, not the sole line of defense.
- `check_advisor_dedup.py`'s term-overlap scoring could still miss a duplicate that shares no vocabulary with its own one-liner (this session's own near-miss found `grep -i drawdown` misses the Magdon-Ismail row entirely, because that row's one-liner uses `G_D`/`MDD` instead of the word "drawdown") — mitigated by sub-rule 8 requiring `git log --oneline -20` as a cheap, vocabulary-independent companion check, not search-tool output alone.

**Downstream artifacts needing update (gated on acceptance — §7):**
- [x] `.claude/hookify.advisor-dedup-first.local.md` → tracked as `.claude/hookify.advisor-dedup-first.md`; trigger regex widened for build-intent phrasing.
- [x] `scripts/check_advisor_dedup.py` — `--keywords` input mode alongside the existing staged-file mode; exit 0 always.
- [x] `docs/operational_rules.md` — Rule 8 sub-rule 8 added; dated edit-log entry appended.
- [x] `scripts/archive_lab_analysis.py` — report-only same-theme-collision WARN on `--check` / `--catalog-only` (never hard-fails).
- [x] `.claude/skills/brief-authoring/SKILL.md` — explicit link to `operational_rules.md` §8.

---

## §7 — Implementation plan

- **Phase 0** — re-verify §0 anchors current at implementation time (`git log -1` on the seven cited targets).
- **Phase 1** — commit the hookify rule under a tracked path; widen its regex per §2 leg 1.
- **Phase 2** — extend `check_advisor_dedup.py` with a `--keywords "..."` input mode (in addition to, not replacing, the existing staged-file mode); exit code stays 0 always.
- **Phase 3** — add Rule 8 sub-rule 8 to `docs/operational_rules.md` plus a dated edit-log entry naming this ADR.
- **Phase 4** — extend `scripts/archive_lab_analysis.py` with the new-slug/same-theme WARN (report-only, wired into the existing `--check` path so it rides the already-mandatory `lab-catalog` gate rather than adding a new gate entry).
- **Phase 5** — add the missing link from `.claude/skills/brief-authoring/SKILL.md` to `docs/operational_rules.md` §8.
- **Phase 6** — verification block (below) executes clean; status moves to `Accepted`.

---

## §10 — Audit hooks (runnable)

```bash
# 1. Hookify rule is committed, not local-only.
git ls-files .claude/ | grep -i dedup
# Expected: a tracked path, NOT ending in .local.md

# 2. check_advisor_dedup.py accepts a keyword-string mode.
python scripts/check_advisor_dedup.py --help | grep -i keyword
# Expected: a --keywords (or equivalent) option documented

# 3. Rule 8 sub-rule 8 exists and is dated in the edit log.
grep -n "sub-rule 8" docs/operational_rules.md
grep -n "2026-08-13.*[Ss]ub-rule 8\|dedup-first" docs/operational_rules.md

# 4. archive_lab_analysis.py carries the new-slug collision WARN.
grep -n "same.theme\|new.slug\|collision" scripts/archive_lab_analysis.py

# 5. brief-authoring skill links to operational_rules.md Rule 8.
grep -n "operational_rules" .claude/skills/brief-authoring/SKILL.md

# 6. Live re-test against this ADR's own motivating incident (should still surface it).
python scripts/check_advisor_dedup.py --keywords "Magdon-Ismail closed-form drawdown simulate_path" 2>&1 | grep -i "mc_mdd_closed_form"
# Expected: a hit, confirming the keyword-mode addition actually would have caught the incident this ADR is written against
```

---

## Verification

```bash
# Discipline checks (mechanical)
$ python "$HOME/.claude/skills/brief-authoring/scripts/check_brief.py" \
  docs/adr/2026-08-13-dedup-first-before-new-work.md --type adr
# Expected: all 6 checks PASS

# Production-source verification (Rule 0 confirmation) — Phase 1-5 complete
$ git ls-files .claude/ | grep -i dedup
# Expected: .claude/hookify.advisor-dedup-first.md  (tracked; NOT .local.md)

$ git ls-files .claude/hookify.advisor-dedup-first.local.md
# Expected: empty (gitignored .local form retired for this rule)

$ for f in docs/operational_rules.md scripts/check_advisor_dedup.py CLAUDE.md \
    docs/methodology/strategy_harvest.md scripts/gates.yml scripts/archive_lab_analysis.py; do
    git log -1 --format="%h %cs -- $f" -- "$f"; done
# Expected: anchors unchanged from §0, or a newer commit if this ADR's own Phase 1-5 already landed

# §10 audit hooks all run clean (2026-08-13 implementation session — all 6 PASS)
```

Phase 1–5 complete; Status remains `Accepted` (ratified before the mechanical sweep per operator instruction). Mechanisms are live once this implementation commit is on `main`.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-13 | Initial authoring — `Proposed`. Drafted from a dedicated 4-lens investigation commissioned the same session, against two dated incidents (Tradeify eval-battery near-miss, caught; Magdon-Ismail closed-form duplicate, uncaught until pre-commit). No mechanical edits applied yet — policy + implementation plan only. | Joshua (direction) + Claude Code (investigation + drafter) |
| 2026-08-13 | **Ratified same day.** Operator ruling *"ratify it and I will spawn as suggested task"* — Status `Proposed` → `Accepted`. §2's decision is now in force; §7 Phases 1-6 (the mechanical wiring) are explicitly NOT yet done and are tracked via a separately-created `spawn_task` chip rather than gating this status flip, per direct operator instruction. Per §0/Verification: re-run §10's audit hooks once the spawned implementation lands, and confirm the §6 downstream-artifact list is fully current before treating this ADR's mechanisms as live. | Joshua (ruling) + Claude Code (recorder) |
| 2026-08-13 | **§7 Phases 1–5 landed** (`8a60c92`). Hookify rule tracked + build-intent regex; `--keywords` mode on `check_advisor_dedup.py`; Rule 8 sub-rule 8 + edit log; report-only same-theme WARN in `archive_lab_analysis.py`; brief-authoring → Rule 8 link. §10 audit hooks all PASS. No `gates.yml` blocking change; no `core/` / `dd_protection` / Pine touch. | Cursor agent (spawned mechanical wiring) |

## Addendum 2026-08-15 — Registry feed + amendment-first (Rule 8.9 / 8.10)

**Does not amend §2's three mechanical legs.** Extends the same "search before create" decision to two moments this ADR's original scope left as checklist:

1. **Registry feed.** A new closure must carry `Registry:` (`rejected_candidates.md — ### heading` or `n/a — <reason>`). Token-gated in `scripts/check_closure_disposition.py`; every closure on disk at land is grandfathered. The 2026-08-03→08-11 hole is **not** backfilled here (operator pass; each row is a re-proposal-bar judgment).
2. **Amendment-first.** Before minting a sibling ADR/brief/notice/lab slug, paste search output naming the existing owner or stating none exists. Default is addendum-on-owner. Companion addendum on the ceremony-tiering ADR.

Owner of the rule text: [`docs/operational_rules.md`](../operational_rules.md) Rule 8 sub-rules 9–10.
