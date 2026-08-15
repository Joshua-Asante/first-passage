# Owner surfaces (Rule 7 — pointer, not a second owner)

Canonical table lives in [`docs/operational_rules.md`](../../../docs/operational_rules.md) §7. This file is a **sweep checklist** for blast-radius greps — if it drifts, trust Rule 7.

## Fact → owner (abbreviated)

| Fact class | Canonical owner |
|---|---|
| Strategy parameters | Pine (Rule 5) |
| Lock state + hashes | `core/strategies/_archive/<family>/LOCK.md` |
| `dd_protection` / allocations | `core/dd_protection.py` / `core/firm_rules.py` |
| MC anchors | `docs/mc_anchor_history.md` + synthetic engine tests |
| Decision rationale | `docs/adr/` |
| ADR lifecycle status | ADR header + `docs/adr/INDEX.md` |
| Session narrative / Open-next | `docs/SESSIONS.md` |
| Per-Q forward disposition | Closure `## Iterate` block |
| Derived param mirror | retired / labeled only — do not revive |

## Must-not-restate roles (scan these as mirrors)

- `STATE.md` — open threads + forward board; decision index is one line + owner link
- `docs/SESSIONS.md` — narrate + link; no duplicated constants
- `CLAUDE.md` §Live-execution posture — pointer lines + ADR links (Strategy Reference / Protection blocks are gated owners, not this note)
- `README.md` — entry index; links out
- `PIPELINES.md` / `REPO_MAP.md` — inventory / path maps; path moves → liveness gate
- `.claude/skills/**` — pointer-first; skills must not silently restate live constants
- `lab/CATALOG.md` — study status authority for catalog rows
- `ops/instruments/*.md` — instrument ledgers (findings / concept status only)

## Typical blast-radius tokens

Extract from the diff, then grep:

- Old status words: `AUTHORIZED`, `PARKED`, `DE-SCOPED`, `WITHDRAWN`, `DISCHARGED`, `OPEN`, `HOLD`
- Old posture phrases / venue names when a venue or rail disposition changes
- ADR / brief / closure slugs (`2026-08-04-…`, `Q-…`)
- Paths that moved (`lab/analysis/<slug>/` → `lab/archive/<slug>/`)
- Numeric restatements the change invalidated (only if this turn changed them — still prefer linking over rewriting numbers into mirrors)

## Mechanical backstops

| Script | Catches |
|---|---|
| `scripts/check_root_doc_liveness.py` | Dead markdown links in root orientation docs |
| `scripts/check_path_liveness.py` | MANIFEST parent paths missing on disk |
| `scripts/check_status_consistency.py` | CATALOG / rejected / instrument status join issues |
| `scripts/check_adr_graph.py` | ADR graph / INDEX drift (when ADRs touched) |
| `scripts/sync_liveness_indexes.py --check` | INDEX Open rows with terminal Status whose successor is already Recently-closed; CATALOG `ACTIVE` + “archive owed” |

None of these replace the old-token grep for silent restatements. Session-end:
run the liveness check; repair clear cases; do not auto-rewrite INDEX.
