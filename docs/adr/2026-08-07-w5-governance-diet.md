# ADR 2026-08-07 — W5: governance diet (gate-manifest runner + tiered entries)

**Status:** `Accepted` — composition/tier owned by one runner; entry-class diet
**Decision date:** 2026-08-07
**Authors:** Joshua (Posture-A direction) + Cursor (drafter)
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Related:** [SPEC S7](../spec/2026-08-07-loop-s7-repo-alignment-spec.md) · [alignment manifest](../notes/2026-08-07-posture-a-alignment-manifest.md) · [`scripts/gates.yml`](../../scripts/gates.yml) · [`scripts/gate_manifest.py`](../../scripts/gate_manifest.py) · [root-doc charter](2026-07-16-root-doc-charter-dedup.md)
**Layer:** governance tooling + doc diet. **$0 / K=0** — no gate dropped; CI re-enable separately owed.

---

## §0 — Rule 0 reads (verified 2026-08-07)

| Source | Anchor | What it pins |
|---|---|---|
| `scripts/githooks/pre-commit` | gates 1–14 enumerated in shell | Composition duplicated vs `Makefile` targets |
| `Makefile` `check` / `validate` | parallel wrappers | Same battery, hand-kept |
| `docs/SESSIONS.md` / `STATE.md` headers | narrative vs open-board | Accretion risk without tier/cap |

---

## §1 — Context

Pre-commit and Make each hand-enumerate the same gate battery. Orientation docs restate the gate list. SESSIONS/STATE accrete without entry classes. Posture-A wants one manifest owning **which** gates run at **which** tier, and a diet for session/state prose.

---

## §2 — Decision

### Gate-manifest runner

1. **`scripts/gates.yml`** is the composition authority: each gate has `id`, `cmd`, `tier` (`always` | `data-conditional` | `soft`), and optional `when` (e.g. staged paths under `core/data/…`).
2. **`scripts/gate_manifest.py`** loads that file and runs the selected tier. Exit non-zero on any hard failure.
3. **`scripts/githooks/pre-commit`** becomes a thin caller: `python scripts/gate_manifest.py --tier pre-commit`.
4. **`make validate` / `make check`** call the same runner (equivalent behavior — **no gate dropped** in this land).
5. **CLAUDE.md** gate list collapses to a pointer at `scripts/gates.yml` + this ADR.

### Tiered SESSIONS / STATE entry classes (direction)

| Class | Surfaces | Cap / rule |
|---|---|---|
| **A — Decision** | ADR / brief Accept; lock; fork ruling | SESSIONS: Focus + link; ≤ **40 words** of prose beyond links |
| **B — Build** | Code land with tests; rail tooling | SESSIONS: Shipped links; no constant restatement |
| **C — Measurement** | RESULTS / closure | Link RESULTS; do not restate bust % |
| **D — Hygiene** | pointer sweeps, INDEX regen | Prefer skip SESSIONS; if needed, one line |

STATE stays open-board only (Rule 7 / anti-accretion). New decision-index lines remain one line + owning ADR. This ADR **directs** the 40-word cap; mechanical enforcement is optional later.

### Explicitly owed (not in this land if risky)

- GitHub Actions CI re-enable / deriving CI job list from `gates.yml` (workflows stay format-only / inert-as-shipped until a dedicated re-enable commit).
- Collapsing `check_brief.py` + template verification blocks to a single authoritative tool (templates may still name both until that pass).

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Keep dual hand-lists in sync by convention | Already drifted historically |
| Drop soft gates to shrink the battery | Out of scope; diet is ownership, not deletion |
| Enforce 40-word cap in a hook now | Premature; direction first |

---

## §4 — Falsifier

**H:** Adding/removing a pre-commit gate requires editing `gates.yml` (and tests if any), not a second hand-copy in the shell hook.

**FALSIFIED if:** a hard gate present in the pre-W5 hook is absent from `gates.yml` after land, or `make check` skips a gate the hook still ran.

---

## §5 — Forbidden moves

- Dropping a gate under cover of “diet.”
- Restating operational constants in SESSIONS/STATE under class A–D.
- Flipping CI from format-only without a dedicated commit.

---

## §6 — Gate

Same-PR: `gates.yml` + `gate_manifest.py` + wired pre-commit + Makefile + CLAUDE.md pointer + SESSIONS/STATE/Rule-7 header notes. CI re-enable = owed.

---

## §7 — Audit hooks

```bash
python scripts/gate_manifest.py --list
python scripts/gate_manifest.py --tier pre-commit --dry-run
grep -n "gates.yml\|gate_manifest" CLAUDE.md scripts/githooks/pre-commit Makefile
```

## Addendum 2026-08-15 — path-conditional pre-commit is not a drop

**Does not amend §2 / §4 / §5.** Diet = *when* a gate runs, not whether it exists.

New tier `path-conditional`: pre-commit runs the gate only if staged paths match `when.staged_regex`. `make check` / `--tier check` still runs every `always` + `path-conditional` gate (plus forced `data-manifests`). Always-on pre-commit stays: `skills-no-constants`, `skill-refs`, `pine-manifest`, `pine-pin-provenance`, `boundaries`.

CI companion (same diet class, not a `gates.yml` drop): pytest matrix is 3.11-only; `validation-controls` is path-filtered to `lab/`. Deriving CI jobs from `gates.yml` remains owed by this ADR and is **not** this addendum.

Forbidden here: moving a hard gate to `soft` (still a silent disable — see `gates.yml` header).

## Addendum 2026-08-15 (later same day) — `path-liveness` / `root-doc-liveness` reverted to `always`

**Does not amend §2 / §4 / §5, or the addendum above.** The re-tier itself was sound; two of the ten `path-conditional` gates were mis-scoped.

Both gates detect **dead links** in root orientation docs. Their `staged_regex` (`^(scripts/|docs/|CLAUDE.md|STATE.md|REPO_MAP.md|PIPELINES.md|README.md)` and `^(CLAUDE.md|STATE.md|README.md|REPO_MAP.md|PIPELINES.md|docs/)`) matched edits to the *link*, never to the *target* — neither ever matched `lab/|core/|ops/`. A commit that moves or deletes a `lab/analysis/` body a root doc links to skipped both gates at pre-commit, even though that is exactly the drift class they exist to catch. Found by the 2026-08-15 governance-belt programme audit (§3.1) as a repeat of a pattern that audit's own object layer had already been graded RED on once: "drift arrived as removed inputs, not moved thresholds."

**Fix:** both gates reverted to `tier: always`. Measured cost: `check_path_liveness.py` ≈0.7s, `check_root_doc_liveness.py` ≈1.4s — small, and the cheaper of the two failure modes (a slower pre-commit vs. a link no one catches going dead).

**Reachability rule for the gates that stay `path-conditional`:** a `staged_regex` is correctly scoped only if staging **every** path class that can cause the gate's violation selects it — not merely the file the gate's own command reads. `tests/test_gate_manifest.py::test_path_conditional_gates_are_reachable` checks this mechanically for the nine gates that remain conditional (`status-consistency`, `adr-graph`, `lab-catalog`, `instrument-profiles`, `sessions-order`, `sessions-append-only`, `supersession-placement`, `closure-disposition`, `governance-prose-control-chars`) — each is self-referential (the violation is introduced by editing the same file class the regex matches), unlike the two reverted gates, which checked a claim about a *different* file than the one the regex scoped. A future re-tier of any gate to `path-conditional` should add a probe to that test before landing, not after.

## Addendum 2026-08-21 — `make validate` is not `make check`

**Does not amend §2's no-gate-dropped land, §4, or §5.** §2 item 4's "equivalent behavior" sentence over-claims. Production `scripts/gate_manifest.py::select_gates` @ `91e6caa` (2026-08-15): `--tier validate` / `make validate` runs `data-manifests` + `pine-manifest` only; `--tier check` / `make check` runs every `always` + `path-conditional` gate (plus forced `data-manifests`). CLAUDE.md already points at the runner. Deriving CI jobs from `gates.yml` remains owed and is **not** this addendum.

## Addendum 2026-08-23 — SESSIONS class D tightened to a judgment-call gate

**Does not amend §2's class table.** `docs/SESSIONS.md`'s own header now gates a *full* entry on a real judgment call rather than "skip Hygiene-only"; a no-judgment session that still needs to update Open/next writes a stub entry (heading + Open/next only, gate-compatible with `sessions-append-only`) instead of a full one — see the SESSIONS.md header for the rule.

## Addendum 2026-08-23 — Open/next lead is the STATE queue

**Does not amend the A–D class table**, the 2026-08-23 judgment-gate (full vs stub), or H6 HOLD (CI-from-`gates.yml`). This addendum owns the *content* of Open/next.

**Rule 0 (this addendum):** this file @ `d8ef99e` (judgment-gate addendum). Cheap falsifier same as the [Survive-bound addendum](2026-08-09-survive-bound-is-the-queue-cap.md#addendum-2026-08-23--out-of-order-serving-is-the-live-defect): three wrap-up surfaces still copy the prior Open/next.

Lead line: `STATE queue: #1 … · #2 … · #3 …` (titles + owner links). Default wrap-up does **not** copy leftover names from the prior top entry. Residue after the lead only with `queue-exception: <reason>` and an existing owner.

## Addendum 2026-08-23 — H6 HOLD lifted: CI composition from `gates.yml`

**Does not amend §4 or §5's forbidden moves** (no gate dropped; no branch protection / required checks). This **is** the dedicated CI-composition land §2 / §5 owed.

`.github/workflows/gate-manifest.yml` runs `python scripts/gate_manifest.py --tier check` on `pull_request` + `push` to `main`. The hand-list in `.github/workflows/skills-check.yml` is deleted. Job id remains `skills` + Python 3.12 so the existing required check name `skills (3.12)` keeps matching (ruleset unchanged — not a Limb-A reopen). `tests.yml` no longer re-lists `check_boundaries.py`.

**Dated exceptions (not silent drops):**

- `pursuit-records` — `data-conditional`; not in `--tier check` (same as `make check`).
- `pine-pin-provenance --base` — stronger CI-only form stays in `manifest-check.yml`; the runner still runs the no-`--base` argv from `gates.yml`.
- `data-manifests` — forced in `--tier check`; CI absent-tree WARN-skip is the existing public-clone soft-degrade.

Owner plan: [`docs/superpowers/plans/2026-08-23-w5-ci-from-gates-yml-implementation.md`](../superpowers/plans/2026-08-23-w5-ci-from-gates-yml-implementation.md). Coherence leftover C-P5-04 / H6 discharged.

## Addendum 2026-08-29 — same-day SESSIONS label collisions are designed, not a defect

**Does not amend §2's class table or any prior addendum.** Elevated same-day agent count
(2026-08-29: ~40 commits / ~30 PRs across Claude sessions, Cursor cloud agents, and Codex review)
produced two same-day-letter collisions on label `29j`, claimed independently by two un-synced
clones and renumbered in each to `29k` and `29l` (self-documented inline in both entries).
`roll_sessions.py --next-label`'s own collision guard is explicitly scoped to "a second concurrent
`--next-label` in **this clone**" — cross-clone prevention is architecturally out of scope without a
network round-trip the tool deliberately avoids ("No network"). `check_push_collision.py`
independently confirms this is by design: two branches each *adding* a new top heading is "the
designed `merge=union` merge, not a contradiction," exempted from its collision check. Renumber-
on-detect at the point of merge is the intended steady state as same-day agent concurrency rises —
no new procedure is owed.

