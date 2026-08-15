# ADR 2026-06-12 — Notion Surface Retirement

**Path:** `docs/adr/2026-06-12-notion-surface-retirement.md` *(repo convention is date-prefixed ADR filenames, not the sequential `NNN+1` assumed at authoring)*
**Status:** ACCEPTED — decision made 2026-06-12 by owner adjudication; execution phased (see §2). Phase 1 (FREEZE) 2026-06-12 · Phase 2 (MIGRATE) DONE 2026-06-13 · **Phase 3 (COLD ARCHIVE) executed 2026-08-10** — workspace **not** deleted (see Addendum 2026-08-10).
**Decision date:** 2026-06-12
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Date:** 2026-06-12
**Owner:** Joshua (adjudicating)
**Author:** Claude (Tech Advisor), claude.ai authoring role; landed to repo via Claude Code 2026-06-12
**Loop-of-Record:** STRATEGIC — surface/track retirement is a funding-and-attention verdict. Executed via D2 channel (c) of the three-loop binding ADR (`docs/adr/2026-06-12-three-loop-methodology-binding.md`; explicit owner adjudication, in-session, named). **This is the first STRATEGIC Delete recorded under the binding** — it is itself a datum for the binding's §4 hypothesis.
**D-S-A domain:** meta-process (a workflow surface), with an authorized cascade into data (the content that surface holds — migrated, not destroyed; per canon §8 cascade rule).

---

## §0 — Reads (Rule 0)

- Notion INQHIORI canon page `34ddc0b53c1181479d7bdecc61f47078` — fetched in full via Notion MCP, 2026-06-12 (this session). Confirmed: page is the only home of the INQHIORI canon ("no standalone in-repo mirror exists" per its own §12). Mirror authored same session: `docs/methodology/inqhiori-canon.md`.
- Memory registry — viewed in full this session (24 edits). Notion-referencing edits identified: #2 (MC Lock Details), #5 (Strategy Lock Reference), #8 (loop-selection canon), #9 (anchors), #13 (Q-roster), #16 (role map, three-surfaces), #24 (canon §14 read-surface clause).
- Session evidence base (conversation_search, this session): 2026-05-05/06 meta-process sweep (13 superseded pages deleted, CTA archive, drift corrections — hours of surface maintenance); 2026-05-14 closure cleanup session; brief-authoring SKILL.md trap #7 (stale Notion page IDs as a named recurring failure); memory #9 standing drift warning.
- `notion-mcp-api-patterns` skill — exists solely to manage the surface's API quirks (infrastructure-for-the-infrastructure marker).
- Operational fact from owner (2026-06-12, this session): daily execution databases (Pre-Trade Log, Daily Execution Log, Reviews) no longer apply — trading is automated end-to-end (TV → Copygram → DXTrade master → TradersConnect slaves); their function is succeeded by Plan T telemetry & reporting.
- `CLAUDE.md` (commit `6473809`, 2026-06-08; anchor populated by Claude Code at landing 2026-06-12) — confirms current methodology entry points reference Notion: The Algorithm URL `34ddc0b53c11811eb6a0d9192b63d252` at `CLAUDE.md:97`, Command Center hub `32cdc0b53c1181b8a18cce1401a4f8e8` at `CLAUDE.md:71`. No `inqhiori-canon.md` reference present yet (to be repointed in §2 Phase 2 — NOT done in this landing commit, which is canon-mirror + ADRs only).

## §1 — Context

Notion entered the workflow as the shared surface when claude.ai could not read the repo. That constraint died 2026-06-06 (repo privatized + pinned-Project sync gives claude.ai live reads; CC and Cursor always had direct access). Since then Notion's role reduced to (a) a read-surface convenience and (b) host of the manual-trading daily-execution databases. With (b) declared vestigial by the owner — automation removed the manual loop those databases served, and Plan T telemetry is the named successor — the surface's remaining function is duplicating repo truth, at a measured cost: recurring drift incidents (n=209 vs 201t; the masquerading page-ID in memory #9; brief-authoring trap #7), multi-hour maintenance sweeps (May 5–6, May 14), a dedicated quirks skill, and write friction (2026-06-12: two consecutive approval-gate failures on a routine canon amendment).

The migration was already happening unnamed: ADRs → repo, gate audits → repo, OODA canon → skill file (2026-05-09, "no Notion mirror," zero regret events since), state → STATE.md. This ADR names the trend and completes it.

**The Algorithm pass:** Question — requirement owner is Joshua; the requirement ("a shared cross-team surface") is real but already satisfied by repo + skills + memory. Delete — the surface, not the content; content migrates. Simplify — two surfaces (repo = truth, memory = advisor context), down from three. Accelerate — none; nothing about a dead surface needs speeding up.

## §2 — Decision (three phases)

**Phase 1 — FREEZE (effective 2026-06-12, immediately).**
Notion is read-only. No new writes of methodology, state, decisions, or briefs. Repo + skills are the sole canon; memory carries pointers. The pending INQHIORI-canon §14 amendment is CANCELLED (superseded by the repo mirror). The staged amendment artifact is withdrawn.

**Phase 2 — MIGRATE (one CC walk-away dispatch, ~half day; target window Jun 15–19 alongside the T2 build, or first free slot).**
Per the residue disposition table:

| Notion artifact | Disposition |
|---|---|
| INQHIORI canon page | DONE 2026-06-12 — mirrored to `docs/methodology/inqhiori-canon.md` (port provenance header; §14 added). **Landed to repo by Claude Code 2026-06-12, same commit as this ADR** — the one Phase-2 row completed early (the rest of Phase 2 is the separate gated dispatch). |
| Parent-framework pages (INQHIORI definitional `34cdc0b5…0d5e`, The Algorithm `34ddc0b5…d252`), Rule 1 page, Iran-Hormuz hard-lesson page, other `[LEGACY-NOTION]` targets in the mirror | Export → `docs/methodology/archive/notion/` (markdown), verbatim, with page-ID in each file header |
| Command Center: challenge parameters, MC Lock Details, Strategy Lock Reference | Verify repo equivalents exist and match (STATE.md / locks / MC docs); export-then-confirm; flag any Notion-only load-bearing fact as NEEDS_CONTEXT — do not silently reconcile |
| Q-roster / open-questions state | Fold into `STATE.md` or `docs/briefs/INDEX.md` |
| Daily Execution System databases (Action Library, Daily Execution Log, Pre-Trade Log, Operational Risk Register, Reviews) | Export historical rows → CSV at `lab/data/behavioral_archive/` (pre-automation behavioral baseline has analytical value for ECR work); no live replacement — Plan T telemetry is the successor |
| Loop records / decision-findings back-catalog | Bulk export → `docs/ltm/notes/archive/notion/`; no per-page curation |
| Everything else | Inventory, list in the migration report, default = archive export |

Plus: **redirect map** at `docs/governance/notion-redirect-map.md` (page-ID → repo path or ARCHIVED-AT path, one line each — resolves every `[LEGACY-NOTION]` tag and every memory/brief anchor); **CLAUDE.md repoint** to `docs/methodology/inqhiori-canon.md`; post-migration **memory pointer updates** (#2, #5, #8, #13, #16 location clauses).

**Phase 3 — DELETE/ARCHIVE (next programme audit).**
Workspace deletion or cold archival decided at the audit, after one full cycle's add-back window. Until then the frozen workspace is the rollback reserve.

## §4 — Falsifiable hypothesis

**H:** If, through the next programme audit, (a) no workflow requires a Notion write, AND (b) no load-bearing fact is discovered to exist only in Notion after Phase 2 reports DONE, **then** the retirement holds and Phase 3 executes.
**Otherwise:** a re-emergent daily-ops tooling need is the add-back signal — disposition order is rebuild-as-repo-artifact (or small app) FIRST; return to Notion only if the rebuild demonstrably fails. A Phase-2 NEEDS_CONTEXT on a load-bearing Notion-only fact pauses Phase 3 but does not by itself reverse Phase 1.
**Falsifier:** the retirement is **falsified** if, before the next programme audit, any live workflow requires a Notion write, OR Phase 2 surfaces a load-bearing fact that exists only in Notion after reporting DONE — either routes to the add-back branch above.

## §5 — Forbidden moves (each genuinely tempting)

1. **Deleting the workspace before Phase 2 verifies.** Freeze ≠ delete; the canon-only-in-Notion discovery this session is exactly why. Phase 3 waits for the audit.
2. **Migrating from memory instead of export.** Rule 0: the CC spawn reads pages via MCP/export, never reconstructs content from summaries. (This ADR's canon mirror used the full same-session fetch — the one legitimate shortcut, provenance-stamped.)
3. **Retrying the §14 Notion write.** Cancelled, not pending. Writing to a frozen surface to "complete" a superseded task is the tidy-up reflex that re-opens the surface.
4. **Leaving memory/brief anchors dangling.** Trap #7's failure mode inverted — dead IDs without a redirect map become silent drift sources. The map is a Phase-2 gate item, not a nice-to-have.
5. **Curating the back-catalog during migration.** Export is mechanical; "while I'm here" cleanup is scope creep (handoff check #9 territory). Curation, if ever, is a separate decision.

## §6 — Gate (binary)

- **Phase 1:** ACTIVE as of 2026-06-12 (this ADR's acceptance).
- **Phase 2:** DONE when (i) every residue-table row reports its disposition, (ii) redirect map committed and resolves all `[LEGACY-NOTION]` tags + memory anchors, (iii) CLAUDE.md repointed, (iv) memory edits #2/#5/#8/#13/#16 updated, (v) zero NEEDS_CONTEXT items open. CC returns DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED per handoff taxonomy.
- **Phase 3:** executed or explicitly deferred at next programme audit, recorded against this ADR.

## §10 — Audit hooks (runnable)

```bash
# 1. Canon mirror is canonical and carries §14
grep -n "Methodology-to-Loop Binding" docs/methodology/inqhiori-canon.md

# 2. Redirect map exists and is non-trivial (Phase 2)
wc -l docs/governance/notion-redirect-map.md   # expected: > 15 lines

# 3. No unresolved legacy tags after Phase 2
grep -rn "LEGACY-NOTION" docs/ --include="*.md" | grep -v notion-redirect-map.md
# Expected: empty (every tag resolved by the map or rewritten to repo path)

# 4. No NEW Notion references in artifacts authored after 2026-06-12
grep -rln "notion.so\|notion.com" docs/adr/ docs/briefs/ --include="*.md" | \
  xargs grep -l "2026-06-1[3-9]\|2026-06-2\|2026-07" 2>/dev/null
# Expected: empty (legacy references in pre-retirement artifacts are exempt)

# 5. CLAUDE.md repointed
grep -n "inqhiori-canon.md" CLAUDE.md   # expected: present; no live notion link as entry point

# 6. Add-back ledger check (run at audit, feeds the binding ADR's D4 metric — docs/adr/2026-06-12-three-loop-methodology-binding.md)
grep -in "notion" docs/notes/audits/programme-audit/*.md | grep -i "add-back\|reversal\|re-open"
# Expected: empty if retirement held; any hit routes to the D4 add-back count
```

## Verification (landing, Claude Code 2026-06-12)

```bash
python scripts/check_brief.py docs/adr/2026-06-12-notion-surface-retirement.md --type adr
# Expected: RESULT: well-formed. A §6 WARN (no RESOLVED/FALSIFIED/AMBIGUOUS keyword) is
# expected and accepted — §6 here is a phased FREEZE/MIGRATE/DELETE gate, not a verdict gate.
git log -1 -- CLAUDE.md   # §0 anchor: 6473809 2026-06-08 (populated at landing)
```

---

## Addendum 2026-08-10 — Phase 3 executed: cold archival (not workspace deletion)

**Status: executed** — operator GO in Cursor Cloud Agent session 2026-08-10
(*"cold archive, proceed with next steps"*). Closes the §2 / §6 Phase-3 gate that sat
undecided through both the 2026-07-01 and 2026-08-08 quarterly programme audits.

**Authority chain (do not re-derive):**

1. This ADR §4 **H held** through both audits — no workflow required a Notion write; no
   load-bearing fact surfaced Notion-only after Phase 2 reported DONE (2026-06-13).
2. GSUB-1 (first GRAND-Subtract pass) ruled the pending Phase-3 sub-option as **cold
   archival**, not workspace deletion — pursuit record
   [`docs/pursuits/c6-notion-estate.md`](../pursuits/c6-notion-estate.md) (landed via
   [PR #708](https://github.com/Joshua-Asante/first-passage/pull/708), merged 2026-08-10;
   closure `RESOLVED-LOADBEARING`; mechanical Notion action deliberately left as a named
   follow-up outside that run's jurisdiction).
3. Operator GO this session authorizes and records the follow-up.

**What Phase 3 means (cold archive):**

| Do | Do not |
|---|---|
| Keep the workspace alive as the historical / rollback reserve | **Settings → Workspace → General → Danger zone → Delete entire workspace** |
| Archive hub / root pages out of daily view (`•••` → **Archive** on Business/Enterprise; hide from sidebar / favorites otherwise) | Empty Trash of retired content as a substitute for archival |
| Leave Phase-1 freeze intact (no methodology / state / decision / brief writes) | Re-open the surface for live workflow writes |
| Treat `docs/governance/notion-redirect-map.md` + Phase-2 exports as the repo read path | Cite live Notion URLs as authority |

**Notion-side mechanical steps (operator-owned — this recording session has no Notion MCP):**

1. Open the First Passage / Trading Plan Notion workspace.
2. Confirm you will **not** use Danger-zone workspace deletion.
3. For each structural hub still in the sidebar (Trading Plan root, Command Center,
   Methodology Canon hub, Framework references, Dev-phase archive — IDs in the redirect
   map): `•••` → **Archive** when the plan exposes it; otherwise remove from sidebar /
   favorites and leave pages untouched.
4. Optional but recommended before any future plan downgrade: native **Export** of any
   still-unexported Daily Execution System databases into
   `lab/data/behavioral_archive/` (Phase-2 `DONE_WITH_CONCERNS` residual — CSVs were never
   landed; operator accepted proceeding without them on this GO).
5. Leave the workspace itself in place — cold archive ≠ delete.

**Repo-side recording (this addendum's commit):**

- Status line above updated to Phase 3 cold-archived 2026-08-10 (decision text in §2
  left byte-unchanged — append-only discipline).
- [`docs/governance/notion-redirect-map.md`](../governance/notion-redirect-map.md) header
  retargeted from "until Phase 3" to cold-archived.
- [`docs/adr/INDEX.md`](INDEX.md) gloss updated.
- §2 Phase-3 prose, §4 H, §5 forbidden moves, and §10 hooks are **not** silently rewritten;
  hook 4 remains the standing "no NEW live Notion dependency" check.

**What this addendum does NOT do:**

- Does **not** delete the Notion workspace.
- Does **not** reopen Phase 1 freeze or authorize Notion writes.
- Does **not** migrate new content — Phase 2 remains the migration record.
- Does **not** perform the remaining GSUB-1 mechanical follow-up (lab archival of
  `usoil_regime_capture`) — that is a separate residual.
