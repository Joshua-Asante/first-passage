---
description: Post-merge housekeeping checklist (CATALOG/STATE/SESSIONS/make check)
allowed-tools: Bash(git:*), Bash(python:*), Bash(make:*), Read, Grep
---

After a PR merges (or a topic branch lands on `main`), run this checklist. Do **not** invent extra doc rewrites; only surface what the merge actually requires. Owners per `docs/operational_rules.md` Rule 7.

## 0. Orient

```bash
git fetch --prune
git status -sb
git log --oneline -5
git rev-parse --abbrev-ref HEAD
```

Prefer operating on an up-to-date `main` checkout (or the worktree that owns the follow-up). If the primary tree is still on the spent topic branch, say so and recommend `git checkout main && git pull` before edits.

## 1. Mechanical gates

```bash
make check
```

If `make` is unavailable:

No `make`? Ask the manifest — **never a copied list.** Composition is owned by `scripts/gates.yml`
via `scripts/gate_manifest.py` (W5 ADR 2026-08-07), so the roster is a query, not a transcription:

```bash
python scripts/gate_manifest.py --list          # hard-gate roster (blocking tiers)
python scripts/gate_manifest.py --list --all-tiers
python scripts/gate_manifest.py --tier check    # run it
make audit                                      # report-only diagnostics
```

The previous copied `grep` alternation is **deleted (2026-08-08)**: it enumerated 11 of the 15
live gate ids, and it drifted twice (five gates missing 2026-08; four missing 2026-08-08) while
sitting directly beneath the words "do NOT work from a copied list". `Makefile:check` is now a
single runner line, so grepping recipe names returns nothing useful.

Report failures; do not `--no-verify` anything.

## 2. Lab catalog (only if an analysis slug landed or archived)

- New/changed `lab/analysis/<slug>/` or archive move → regenerate or verify `lab/CATALOG.md` via the archive tool / `scripts/archive_lab_analysis.py` conventions.
- Quick drift peek: `python scripts/archive_lab_analysis.py --check` when that entrypoint exists; otherwise grep CATALOG for the slug.

Skip if the merge touched no `lab/analysis` / `lab/archive` paths.

## 3. STATE.md forward board

Open `STATE.md`. If the merge closed, parked, or unblocked a forward item (campaign freeze, ADR ratification, lane status), propose a **minimal** STATE edit — do not restyle the file. If nothing on the board changed, say "STATE: no change".

## 4. SESSIONS.md entry

If this merge was a real session outcome and no entry exists yet, draft a newest-first `docs/SESSIONS.md` entry (template at top of that file): Focus / Shipped / Decisions-defects / Open-next / Live-ops posture line. Do **not** write the file unless the operator asks to persist it — paste the draft in chat first when unsure.

Optional rolloff (only if SESSIONS is long and operator wants it):

```bash
python scripts/roll_sessions.py --dry-run
```

## 5. Skills deploy (optional; main checkout only)

`make sync-skills` is **not** a required post-merge tax. Run it only when (a) you are on the durable **main** checkout (not a Cloud agent / `.claude/worktrees/` session), and (b) you intentionally want the cloud-synced deployed bundle updated after a skill merge.

```bash
# optional — main checkout only
make sync-skills
# or: python scripts/sync_skills.py
```

Skip on worktrees and Cloud checkouts (would clobber the shared bundle or deploy branch state) — `scripts/sync_skills_hook.py` already skips worktrees; keep that invariant. Scoreboard `skipped (worktree|cloud)` means **not attempted here** — record it as such, not as a
success. (Corrected 2026-08-08: `sync_skills.py --check` exits **1** on real drift, and drift is
present today. A skip defers that check to a non-worktree session; it does not discharge it, and
no gates.yml entry covers skill-bundle sync.)

## 6. Hygiene handoff

If many topic branches/worktrees remain after the merge batch:

```bash
python scripts/repo_hygiene.py
```

Then follow the `repo-hygiene` skill (report → operator confirm → delete). Do not auto-prune.

## 7. Closeout

Return a short scoreboard:

| Item | Status |
|---|---|
| gates (branch: make check / Makefile-recipe fallback) | pass/fail — name the branch |
| CATALOG | n/a / ok / needs edit |
| STATE | n/a / ok / draft proposed |
| SESSIONS | n/a / draft in chat / written |
| sync-skills | n/a / done / skipped (worktree) |
| hygiene scout | n/a / report summarized |
