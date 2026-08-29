# ADR 2026-06-30 — STATE.md Role Reduction (4 → 2 via The Algorithm)

**Status:** ACCEPTED — decision made 2026-06-30 by owner authorization (in-session, named). Executed same session via Claude Code (STATE.md restructure + `operational_rules.md` §7 amendment landed in this commit).
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** `2026-08-09-survive-bound-is-the-queue-cap.md` - the "only 2 headers" hook, re: the OPERATOR QUEUE section it introduced.
**Retain-until:** none
**Decision date:** 2026-06-30
**Authors:** Joshua (authorizing) + Claude (Claude Code)
**Related:** extends the 2026-06-03 doc-taxonomy demotion (`docs/SESSIONS.md` 2026-06-03 entry — "demote STATE.md to in-flight-only"); companion to `docs/adr/2026-06-12-notion-surface-retirement.md` (§2 named STATE.md as the fold-destination for open-questions state).
**Layer:** infrastructure (governance / doc-taxonomy)
**D-S-A domain:** **meta-process** (a governance-doc + the `§7` rule that charters it), with an authorized cascade into **data** (the content the deleted roles held — *relocated to existing owners, not destroyed*: working-tree state → `git` + SESSIONS; owner table → `§7`). Per the inqhiori-algorithm §8 cascade rule, meta-process D authorizes the corresponding content move.

---

## §0 — Rule 0 reads (production-source verification)

Files read **in full** before authoring, this session (2026-06-30); anchors are the last pre-session commit touching each.

- `STATE.md` — anchor `74ef32c` (2026-06-24). Source of the 4-role inventory: (a) `## Uncommitted working tree`, (b) `## Dormant cross-session threads`, (c) `## Scheduled forward triggers`, (d) `## Canonical owners`.
- `docs/operational_rules.md` §7 (lines 142–180) — anchor `b5fd5fa` (2026-06-24). The rule being amended: line 167 charters STATE.md as *"in-flight only (uncommitted working-tree delta + dormant cross-session open threads)"* and its §7 owner-table (lines 153–164) is the higher-fidelity source that STATE.md's `## Canonical owners` table duplicates.
- `MEMORY.md` — read this session (in context). Confirmed the dormant threads **Q-CORR-1.2** and **Q-NAS-ECR-1** are **not** present → STATE.md is their only home (load-bearing test for role (b)).
- `docs/SESSIONS.md` — anchor `404a8df`/top entries + the 2026-06-03 entry. Confirmed dormant threads are **not** carried in any recent SESSIONS entry, and that the 2026-06-03 audit already demoted STATE.md (the prior decision this ADR extends).
- `core/strategies/nas/LOCK.md`, `core/strategies/striker/LOCK.md` — anchor `dd4e4aa` (2026-06-06). Both held dead `STATE.md §Open #1/#2` pointers (a section deleted at the 2026-06-03 demotion); repointed/removed earlier this session.
- `docs/briefs/INDEX.md` — anchor `37b40fc` (2026-06-17). Line 34 delegates forward-triggers to `STATE.md §Scheduled forward triggers` — a **kept** section → verified no-op.
- `docs/adr/2026-06-12-notion-surface-retirement.md` — anchor `e122582`. The analog meta-process Delete-via-The-Algorithm; its §2 residue table names STATE.md as the open-questions fold-destination (corroborates keeping role (b)/(c)).

---

## §1 — Context

The 2026-06-30 housekeeping audit found `STATE.md` bundling four roles, of which two are redundant against higher-fidelity owners. The 2026-06-03 doc-taxonomy audit had already demoted STATE.md to "in-flight only" to stop it **restating canonical values** (it had drifted 3 weeks stale on the strategy table + MC anchor), and wrote `operational_rules.md` §7 to prevent that class — but it left the redundant working-tree and owner-table *roles* in place. This session measured the cost of leaving them: a 27-day-stale "Copygram PR #119" line under `## Uncommitted working tree`, two dead `STATE.md §Open` pointers in the locked-strategy LOCK.md files, and a `Snapshot date:` header that reads as false-staleness (it caused this very audit to mis-flag STATE.md as neglected). Critically, STATE.md's `## Canonical owners` table **duplicates** §7's own owner table — STATE.md violating the no-restatement rule that governs it.

**Decision driver (one sentence):** §7 charters the working-tree role *and* STATE.md duplicates §7's owner table, so the redundancy is self-contradictory — it costs ongoing drift maintenance with zero offsetting value, and the only principled fix is to delete the duplicated roles and re-align §7.

**The Algorithm pass.** Question — requirement owner is the 2026-06-03 audit; the parent requirement ("a home for cross-session items not in code/git/owners") is real, but two of STATE.md's four jobs duplicate higher-fidelity owners (permitted D-test: *"duplicated by a higher-fidelity source already in the corpus?"*). Delete — (a) working-tree delta (git + SESSIONS Open/next) and (d) owner table (§7). Keep — (b) dormant threads (verified unique: not in MEMORY, not in recent SESSIONS) and (c) forward-trigger aggregation. Simplify — STATE.md collapses to one coherent purpose: the open-threads + forward-obligation register; §7's charter shrinks to match. Accelerate — the forward triggers (c) become scheduled reminders (the deferred tail, §7 Phase 3 here).

---

## §2 — Decision

**Decision:** Reduce `STATE.md` from four sections to two — `## Dormant cross-session threads` + `## Scheduled forward triggers` — and redefine it as the **open-threads + forward-obligation register**. Delete `## Uncommitted working tree` (→ `git status` + the SESSIONS "Open / next" top entry) and `## Canonical owners` (→ a pointer to `operational_rules.md` §7). Amend §7's STATE.md charter to match: drop "uncommitted working-tree delta," and state that STATE.md carries no owner table (points to §7 for ownership).

**Effective:** immediately upon acceptance.
**Scope:** `STATE.md` and `docs/operational_rules.md` §7 only. No strategy, allocation, `dd_protection`, MC-anchor, or lock change.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Delete STATE.md entirely** (fold dormant threads → `MEMORY.md`, triggers → SESSIONS pinned block) | MEMORY is *relevance-recalled atomic facts*; the dormant-threads register is a *consolidated single-scan view* — different access pattern. Atomizing loses the "show me every open thread at once" scan. This is the "add-back 10%": the consolidated view is the value role (b) provides, so the file survives on (b) alone. |
| **Status quo (keep all 4 roles)** | The redundant roles generate measured drift (stale PR line, dead `§Open` pointers, false-staleness header), and STATE.md duplicating §7's owner table is a live violation of §7's own no-restatement rule. |
| **Trim stale content only, keep all 4 section-headers** (the first-pass half-measure) | Leaves the *structural* redundancy (owner-table dup of §7; chartered-but-vestigial working-tree section) that will simply re-drift. Deletes too little (inqhiori-algorithm: "the most common error is to delete too little"). |
| **Rename STATE.md → `OPEN.md` / `THREADS.md`** | The name is now technically a misnomer, but renaming is pure cross-ref churn (§7, `briefs/INDEX.md`, the notion-retirement ADR, the redirect-map) that reduces **zero** drift surface — the drift came from roles (a)+(d), which we delete regardless of name. Charter-redefine-in-place is the cheaper Simplify. **Deferred**, not rejected. |

---

## §4 — Falsifier (revert trigger)

**H:** If, through the next programme audit, no workflow needs STATE.md to carry working-tree state or an owner table that `git` / SESSIONS / §7 cannot serve, **and** no dormant cross-session thread is lost for lack of a home, **then** the 4→2 reduction holds and the deleted roles stay deleted.

**Revert trigger (falsifier):** the reduction is **falsified** if, before the next programme audit, (i) a load-bearing need re-emerges for STATE.md to carry working-tree state or a canonical-owner table that `git` / SESSIONS / §7 demonstrably **cannot** serve, OR (ii) a dormant cross-session thread is lost because it had no home.
**Revert action:** restore the specific deleted role to STATE.md **and** re-amend §7 to match (never restore one without the other — that re-creates the STATE↔§7 inconsistency this ADR removes). Restoration is role-specific, not a wholesale revert.
**Trigger check schedule:** next programme audit (semi-annual/triggered) + opportunistically at each standing quarterly forward-trigger review (2026-07-19 / 07-29 / 08-08).

---

## §5 — Forbidden moves (under this ADR)

- **Re-adding a "current state" snapshot** (`Snapshot date` / `Repo state: clean` / working-tree mirror) to STATE.md — that is exactly the 2026-06-03 drift class and the whole point of this ADR. Working-tree/branch state lives with `git`; canonical state with its owners.
- **Restating §7's owner table inside STATE.md** — duplicating a canonical owner table is the §7 violation being removed here.
- **Silently editing the §4 trigger to match emerging evidence** instead of superseding with a fresh ADR — `p`-hacking at the methodology layer (brief-authoring Trap #12).
- **Reviving "delete STATE.md entirely"** without new evidence — the §3 reason (consolidated-scan ≠ relevance-recall; the threads are not in MEMORY) stands until a real consolidated home exists elsewhere.

---

## §6 — Consequences

**Positive:**
- −22 lines in STATE.md; a single-purpose doc whose name-vs-content mismatch is the only residue (deferred rename).
- STATE.md and §7 are now mutually consistent — the owner table has exactly one home (§7).
- The two roles that produced this session's drift (stale PR line, dead `§Open` pointers) are deleted at the source.

**Negative (real cost):**
- Two owner-table navigation rows dropped that §7's table lacks — *public-clone posture → `CLAUDE.md` §Public-clone* and *active methodology rules → `operational_rules.md` + `docs/methodology/`*. Accepted as redundant with CLAUDE.md's own structure (both are one section-jump away in a session-loaded doc). Fold into §7 if a navigation gap is later felt.

**Risks:**
- A reader habituated to STATE.md's owner table must re-home to §7. Low: §7 is the governing rule and a strict superset of STATE.md's table (minus the two accepted-dropped rows).

**Downstream artifacts:**
- `STATE.md` — restructured (this commit).
- `docs/operational_rules.md` §7 — charter amended (this commit).
- `docs/briefs/INDEX.md` line 34 — verified no-op (delegates to the kept `§Scheduled forward triggers`).
- `core/strategies/{nas,striker}/LOCK.md` — dead `§Open` pointers fixed earlier this session (same branch).

---

## §7 — Implementation plan

- **Phase 0** — §0 reads confirmed current this session (anchors above).
- **Phase 1** — STATE.md restructure + §7 charter amendment. **DONE** (this commit).
- **Phase 2** — grep-sweep for stale references to the deleted sections. **DONE** (zero orphaned `STATE.md §Open` / `Canonical owners` / `Uncommitted working tree` refs; `check_path_liveness` OK).
- **Phase 3** — verification block executes, status `ACCEPTED`; the forward-trigger reminders (the Accelerate tail) stood up as scheduled tasks (2026-07-19 / 07-29 / quarterly-08-08).

---

## §10 — Audit hooks (runnable)

```bash
# 1. STATE.md holds exactly the two register sections (no working-tree / owner-table section)
grep -nE '^## ' STATE.md
# Expected: '## Dormant cross-session threads' and '## Scheduled forward triggers' ONLY

# 2. No re-introduced state-snapshot framing
grep -niE 'Snapshot date|Repo state.*clean|Uncommitted working tree|^## Canonical owners' STATE.md
# Expected: empty

# 3. No orphaned references to the deleted sections / dead anchors
grep -rniE 'STATE\.md.{0,40}(Canonical owners|Uncommitted working tree)|STATE\.md §Open' --include='*.md' . | grep -v '/archive/'
# Expected: empty

# 4. §7 charter matches the register definition (no 'in-flight only' / 'working-tree delta')
grep -nA3 'STATE\.md`\*\* —' docs/operational_rules.md
# Expected: 'open-threads + forward-obligation register'; NOT 'in-flight only' / 'working-tree delta'

# 5. Path liveness intact
python scripts/check_path_liveness.py   # Expected: OK
```

---

## Verification

```bash
# Discipline checks (mechanical)
python scripts/check_brief.py docs/adr/2026-06-30-state-md-role-reduction.md --type adr
# Expected: well-formed (a §6/gate WARN for no RESOLVED/FALSIFIED keyword is expected and
# accepted — §4 is the binary revert trigger; this ADR records a decision, not a verdict).

# §0 anchor confirmation
git log -1 --format='%h %cs' -- docs/operational_rules.md   # expected b5fd5fa 2026-06-24 (pre-edit)
git log -1 --format='%h %cs' -- STATE.md                    # expected 74ef32c 2026-06-24 (pre-edit)

# Downstream sweep (§10 hooks 1–5) all pass
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-23 | Addendum: MEMORY assistive-only; Rule 7 owner demoted | Joshua + Cursor |
| 2026-06-30 | Initial authoring + execution (STATE.md 4→2 roles; §7 charter amended) | Joshua + Claude Code |

## Addendum 2026-08-23 — MEMORY is assistive-only, not the Rule 7 owner

**Does not amend** the 4→2 STATE reduction, the two kept register sections, or §3 / §5 (“do not fold STATE into MEMORY”; “do not revive delete-STATE”). **$0 / K=0.** Limb 4 (doctrine): the Rule 7 owner-table row.

**Rule 0 (this addendum):** `docs/operational_rules.md` §7 owner table @ `e159743` (2026-08-22) — row still read `| Durable atomic facts (by relevance) | MEMORY.md + memory files |`. Cheap falsifier (plan Task 1): repo-root `MEMORY.md` absent; SESSIONS header still named MEMORY as the complementary atom store.

**Decision:** Durable atoms that bind future work are owned by the ADR / methodology-lesson that already holds them. Claude-project `MEMORY.md` is assistive-only (outside the clone). A MEMORY paste is not a Rule 0 read and is not a sub-rule 8/10 attestation.

**Boundary:** Do not copy the Claude project memory directory into this public tree (Approach C). Do not stand up `docs/memory_index.md` (Approach B — separate GO). Do not treat this addendum as a Q-XMEM-1 re-verdict (Mem0 sidecar stays SUBTRACT).
