---
name: blast-radius
description: After editing docs, ADRs, posture lines, STATE, skills, catalogs, or other linked judgments, surface the blast radius — owners and mirrors that may still restate the prior finding. Use when stopping after substantive edits, when the Cursor stop hook or Claude hookify nudge fires, or on "tidy", "blast radius", "propagate", "grep-sweep", "source-of-truth fracture". Report-first; repair only clear silent restatements owed by this turn. Sibling of fable-judge (claims vs artifacts), brief-authoring Phase 2 (ADR/lock authoring sweep), and Rule 6 skew-audit (lock windows). Does not touch Pine, dd_protection constants, or allocations.
---

# blast-radius — surface linked drift after a change

This repo links judgments across ADRs, posture pointers, boards, skills, and catalogs. Agents often update the primary artifact and leave silent restatements elsewhere. This skill is the **cheap post-edit sweep**: find the blast radius, triage it, report it. It is not `fable-judge` (adversarial claim verification) and not Rule 6 lock-window skew audit.

**Doctrine:** `docs/operational_rules.md` Rule 7 (one canonical owner; everyone else links or is a labeled mirror). Owner table detail: [references/owner-surfaces.md](references/owner-surfaces.md).

## When to use

- After any substantive edit to hot surfaces (docs/, CLAUDE.md, STATE.md, PIPELINES.md, REPO_MAP.md, `.claude/skills/`, lab/CATALOG.md, ops/instruments/, strategy LOCK/CHANGELOG mirrors).
- When a stop-hook / hookify nudge asks for it.
- On explicit "tidy" / "blast radius" / "propagate this finding".

**SKIP** read-only turns, pure code refactors with no judgment/posture prose, and edits confined to the blast-radius skill/hooks themselves.

## Procedure (minutes, not hours)

### 1. Ground truth — what changed

```bash
git status -sb
git diff --name-only
git diff --stat
```

List touched paths. For each load-bearing prose change, note **old token → new token** (value, status word, ADR slug, posture phrase, path). Prefer tokens from the diff, not memory.

### 2. Grep the hot surfaces

Search for each **old** token (and the decision slug if any) across:

- `CLAUDE.md` · `STATE.md` · `PIPELINES.md` · `REPO_MAP.md` · `README.md`
- `docs/adr/` · `docs/briefs/` · `docs/SESSIONS.md` · `docs/notes/`
- `.claude/skills/` · `lab/CATALOG.md` · `ops/instruments/`
- strategy doc mirrors under `core/strategies/**/*.md` (not `.pine`)

```bash
# adapt tokens from the diff
rg -n --hidden -g '!.git' -g '!.cursor/hooks/state' "<old-token>" \
  CLAUDE.md STATE.md PIPELINES.md REPO_MAP.md README.md \
  docs/ .claude/skills/ lab/CATALOG.md ops/instruments/ core/strategies/
```

Also run mechanical backstops when paths moved or status words flipped:

```bash
python scripts/check_root_doc_liveness.py
python scripts/check_path_liveness.py
python scripts/check_status_consistency.py
python scripts/sync_liveness_indexes.py --check
```

(Link/status gates only — they do not prove semantic currency. The liveness
script is **report-only**: stale INDEX Open rows whose named successor is
already Recently-closed, and CATALOG `ACTIVE` + “archive owed”. Repair clear
cases in-session. Do **not** auto-rewrite INDEX. CATALOG status flips go
through `archive_lab_analysis.py --regenerate-catalog`, not hand-edits.)

### 3. Triage each hit

| Class | Action |
|---|---|
| **Canonical owner** (this turn's primary write) | Already updated — cite it |
| **Labeled mirror / pointer** (STATE board, CLAUDE posture bullet, SESSIONS Open/next, INDEX row) | Update to **link**, or refresh the one-line pointer — never restate owned values |
| **Silent restatement** (prose repeats a value/status it does not own) | Fix in-session if clearly owed by this change; else list as owed |
| **Historical ADR / closure body** | Leave text; add parenthetical / Superseded-by only when this ADR's Phase 2 requires it |
| **False positive** (same string, different meaning) | Mark `n/a` with one-line why |

**Do not** edit Pine, `dd_protection` / `firm_rules` risk constants, or allocations under this skill.

### 4. Report shape (mandatory)

First line must be exactly one of:

```
BLAST-RADIUS: CLEAN
BLAST-RADIUS: OWED
BLAST-RADIUS: REPAIRED
```

Then a short table:

```
| path | old token | class | action |
|------|-----------|-------|--------|
| ...  | ...       | silent restatement / pointer / historical / n/a | fixed / owed / left / skip |
```

Close with:

- **Owners touched:** …
- **Still owed (operator):** … or `none`
- **Gates run:** liveness/status commands + exit codes, or `skipped — no path/status change`

`CLEAN` = grep found no silent restatements / stale pointers. `REPAIRED` = you fixed at least one in this turn. `OWED` = at least one remains for the operator or a follow-on.

### 5. Repair scope

Default after a hook nudge: **report + fix clear silent restatements and stale one-line pointers** that this turn's tokens prove. Stop and ask when:

- the hit is outside the ask's scope,
- fixing would edit a locked constant or Pine,
- historical ADR wording needs a judgment call beyond a Superseded-by / parenthetical.

## Sibling map

| Skill / rule | Owns |
|---|---|
| `brief-authoring` Phase 2 / lock §7 | Downstream sweep **while authoring** ADRs/locks |
| Rule 6 + `.claude/commands/skew-audit.md` | Lock-window `Code:`-pointer audit |
| `fable-judge` | Post-hoc claim verification (read-only) |
| `handoff-verify` | Pre-execution packet gate |
| `repo-hygiene` | Git/worktree debris |
| **blast-radius** | Post-edit linked-judgment surface |

## Rationalizations — STOP

| Thought | Reality |
|---|---|
| "I updated the ADR; mirrors can wait." | Stale pointers read as truth (Rule 7). Sweep now. |
| "grep was clean on the new phrase." | Search the **old** token and the decision slug. |
| "STATE already mentions it." | STATE may still carry the prior obligation as open — open the bytes. |
| "fable-judge will catch this." | Judge checks claims vs diff; it does not hunt undischarged mirrors. |
| "I'll note it in SESSIONS only." | A SESSIONS line is not a mirror repair. |

## Install surfaces

| Surface | Path | Notes |
|---|---|---|
| Skill (tracked) | `.claude/skills/blast-radius/` | Auto-discovered by CC/Cursor skill loaders |
| Cursor stop + edit ledger (tracked) | `.cursor/hooks.json` → `record_edit.py` + `blast_radius_stop.py` | `loop_limit: 1`; state under `.cursor/hooks/state/` (gitignored) |
| Claude hookify (local) | copy `references/hookify-blast-radius.local.md` → `.claude/hookify.blast-radius.local.md` | `.local.md` is gitignored by convention — install once per clone |
