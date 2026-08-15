# Deletion Ledger

**Created:** 2026-07-10 — Delete & Simplify pass (`cleanup/ds-pass-2026-07`), per operator adjudication.
**Convention:** append-only. One row per deleted or attic-quarantined path.
**Purpose:** restore hash + criteria-basis so a future D4 add-back metric (still PROPOSED, not ratified) can be computed without reconstructing intent from git archaeology alone.

## Schema

| Column | Meaning |
|--------|---------|
| date | ISO date of the deletion/quarantine commit |
| path | Repo-relative path removed or moved |
| action | `HARD-DELETE` / `ATTIC` / `REF-REPAIR` (dangling-cite fix, not a deletion) / `SIMPLIFY` (dead packaging/doc line) |
| reason | One-line why |
| sanctioning decision | ADR / brief / operator adjudication that authorized the row |
| criteria-basis | C1–C4 result summary (required — not just that it cleared) |
| restoring commit | `git` hash that introduced the deletion (or attic move); restore via `git show <hash>^:<path>` |

### Criteria (standing for this pass)

- **C1** Sanctioning provenance — named retirement ADR/decision, or genuine orphan with no C1 → attic not hard-delete
- **C2** Orphan test — zero inbound references; not in any MANIFEST/SHA256SUMS; not a closure record; not named in STATE.md forward triggers
- **C3** Load-bearing test — absence must not change any falsifier, budget, gate, or evidence chain
- **C4** Recoverability — tracked (git-recoverable) vs gitignored-local (IRRECOVERABLE — never `rm`; quarantine + individual adjudication only)

### Hybrid disposition (operator 2026-07-10)

- **Hard delete + ledger** when C1 (named retirement ADR) ∧ C2 (zero refs) ∧ ¬C3 ∧ C4-tracked
- **Attic quarantine** (`docs/attic/`) when orphan-only (C2, no explicit C1)
- **Gitignored vendor CSVs** — never `rm`; quarantine-only, per-file adjudication

## Entries

| date | path | action | reason | sanctioning decision | criteria-basis | restoring commit |
|------|------|--------|--------|----------------------|----------------|-------------------|
| 2026-07-10 | `.claude/skills/inqhiori/SKILL.md` + `docs/methodology/inqhiori-canon.md` (gate_audits cites) | REF-REPAIR | Dangling write-target `docs/methodology/gate_audits/` never existed at HEAD; repoint live writes to `docs/notes/audits/YYYY-MM-DD_gate_<slug>.md`; historical cites → `git show pre-prune-2026-06-05:archive/docs/methodology/archive/gate_audits/` | Operator adjudication 2026-07-10 (manifest S1); path archived 2026-04-29 / evicted 2026-06-05 | C1: sanctioned reference repair (not a deletion). C2: live write-target had zero resolvable path. C3: methodology audit-hook must point at a real location (repair preserves load-bearing intent). C4: tracked prose, git-recoverable | 032cd64 |
| 2026-07-10 | `pyproject.toml` `[project.optional-dependencies].ingest` | SIMPLIFY | Dead optional-extra: zero runtime consumers; comment referenced deleted notion_files/notion_client | Operator adjudication 2026-07-10 (manifest S2); Notion ingest retirement | C1: Notion ingest already retired (consumers gone). C2: `rg` for `[ingest]` / `pip install .[ingest]` consumers EMPTY. C3: no load-bearing install path. C4: tracked packaging line, git-recoverable | 4d9f71a |
