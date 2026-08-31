# `docs/pursuits/` + `docs/personas/` reversed-evidence audit — 2026-08-31

**Audit ID:** AUDIT-2026-08-31-PURSUITS-PERSONAS-REVERSED-EVIDENCE · **Date:** 2026-08-31 · **Trigger:**
operator direction ("take a look at `docs/pursuits` and `docs/personas` next"), following the two
earlier same-day audits (mirror docs, [`audit note`](2026-08-31-reversed-evidence-docs-audit.md);
`ops/instruments/*.md`, [`audit note`](2026-08-31-ops-instruments-reversed-evidence-audit.md)),
both of which had explicitly logged `docs/pursuits/*.md` and `docs/personas/*.md` as unswept in
`STATE.md`'s forward-obligation row.

**Scope:** all 41 `docs/pursuits/*.md` files and all 34 `docs/personas/*.md` files (22 top-level +
12 under `docs/personas/archive/`). Same targeted (known-reversal-propagation) method as the two
companion audits, not a blind full-corpus scan.

**Method:**

1. Reused the ~20-item reversal reference sheet compiled for the two companion audits (ADR
   supersession graph, closure ledger, `CLAUDE.md`'s own flagged reversals), extended with a
   pursuits/personas-specific item: `check_pursuit_records.py` was de-wired from `scripts/gates.yml`
   as of 2026-08-24 (Rule 16 R5) — learned from `docs/pursuits/README.md` itself while scoping.
2. Ran one scan agent per batch of ~4 files (10 batches for pursuits, 9 for personas — 19 scan
   agents total, 75 files), each checked against the reference sheet and free to surface any other
   verifiable reversal — chosen over one-agent-per-file (the prior audits' pattern) because these
   files average 23-35 lines, far shorter than the ops/instruments ledgers.
3. Ran an independent, refute-first adversarial verify pass on every flag (20/20) — each verifier
   re-derived the claim and the reversal from primary source, not the scan pass's own wording.
   Result: 16 `CONFIRMED_STALE`, 4 `FALSE_POSITIVE`, 0 `UNCERTAIN`.
4. Applied minimal, pointer-based fixes across 15 files (16 confirmed findings, consolidated where
   one file carried multiple), one agent per file. Two verify agents (on `cio-log.md` and
   `coo-log.md`) independently surfaced that `docs/personas/cro-log.md` carries the identical stale
   pattern as a collateral observation — confirmed directly via `grep` before adding it as a 17th
   fix target (self-verified, not scan-flagged).
5. One fix landed outside the two named directories: `docs/briefs/GSUB-1-inventory-and-dispositions.md`
   row 152 carries the exact same stale "checker-canon split UNRULED" claim as
   `docs/pursuits/d2-brief-authoring-user-skill.md` (both authored from the same GSUB-1 batch) —
   fixed in the same pass since it's the identical drift, not a new scope expansion.

## §1 — Result

| Metric | Count |
|---|---|
| Files scanned | 75 (41 pursuits + 34 personas) |
| Scan batches | 19 |
| Raw findings | 20 |
| Verified `CONFIRMED_STALE` | 16 |
| Verified `FALSE_POSITIVE` | 4 |
| Verified `UNCERTAIN` | 0 |
| Files fixed | 15 (16 confirmed findings + 1 self-verified collateral + 1 same-drift bonus fix outside scope) |

## §2 — Findings by theme

**Campaign progress frozen at ratification-day snapshot (2 findings).** `a6-cursor-fleet-worker-
capability.md` named "three frozen packets pending dispatch" as of 2026-08-09 with no update —
all three have since run to a closure or ADR-acceptance (dense-1m CON-2 through CON-5, the W1
intraday-honest-engine ADR Accepted 2026-08-22, the MCL/MES/MGC instrument lane). `head-of-research-
log.md`'s final entry said Q-ORBCUSH-1 was "named, not opened" — it opened and closed the same day
(2026-08-20, verdict FALSIFIED).

**A residual/follow-up already executed, but the pursuit record still reads as open (2 findings).**
`b4-q-usoil-1.md` named an un-archived lab body as a follow-up — it was archived 2026-08-09/11, and
the path named (`lab/analysis/legacy/usoil_regime_capture/`) never existed. `d2-brief-authoring-
user-skill.md` (and the identically-worded `docs/briefs/GSUB-1-inventory-and-dispositions.md` row
152) named a checker-canon split as "UNRULED" — it was ruled the same day via a same-day-dated ADR.

**A superseded pre-registration ceiling cited without the supersession pointer (1 finding).**
`b8-guardian-mgc-transfer-lane.md` cited the 3.0% Part A eval bust ceiling — superseded to 5.0% on
2026-08-26. This exact reversal event had already been fixed in 3 other files across the two prior
audits (`b3-orb-mnq-payability-line.md`, `objective_composition_map.md`) — `b8` was simply not
among the files those audits checked (`docs/pursuits/*.md` was only 5-of-41 swept before this pass).

**A same-day self-contradiction, independently rediscovered elsewhere but never fixed at its own
source (1 finding).** `d10-plugin-duplicate-set.md` claims all 7 named skills have a live repo copy
— sibling record `d6` (ratified the same GSUB-1 batch) documents that `notion-mcp-api-patterns`
never had one. The 2026-08-29 ADR-decay audit already caught and fixed this exact contradiction —
but only on the parent ADR, never on `d10.md` itself.

**Belt-size / status snapshots stale by a wide margin (2 findings in one file).**
`d1-repo-belt-19-skills.md`'s title cites "19 skills" (now 23) and its belt-churn status cites a
2026-08-08 YELLOW reading superseded 7 days later by a DEGENERATING verdict from a scope-matching
audit — neither reflected in the record.

**A private-archive-only recovery tag cited without the public-clone caveat (1 finding).**
`c6-notion-estate.md` names `pre-prune-2026-08-08` as a recovery instruction; `CLAUDE.md` and
`docs/ltm/README.md` both already state that tag doesn't resolve on this public clone — `c6` didn't
carry the caveat.

**Governance-log "Pending" fields never updated after the ratification landed (3 findings, same
pattern across 3 files).** `cio-log.md`, `coo-log.md`, and (self-verified collateral) `cro-log.md`
each recorded "Ratified as recommended: Pending" for the 2026-08-19 GSUB-2 review — GSUB-2 was
ratified the same day with zero divergence, and none of the three append-only logs ever recorded
the outcome.

**A closed ruling still named as a live domain item (1 finding).** `cfo.md`'s Domain bullet lists
"capital-allocation rulings (F1)" with no indication F1 was ruled 2026-08-23 — the file has never
reflected the ruling since it entered the repo one day *after* that ruling.

**An ownership table with three stale Standing cells (1 finding, 3 rows).** `ownership-map.md`'s
Layer 2 pursuit table shows `b2`, `c1`, and `b7` all as `PARK` — each pursuit record's own Standing
field (and the closures that ratified them) already show `SUBTRACT`. All three flips happened on or
around the table's own "done 2026-08-19" snapshot date and were never backported.

**A roster list eight names wide when only three remain live (1 finding).**
`research-analyst.md`'s independence-rule sentence names 8 sibling Staff personas as the peer-review
set — 5 of the 8 were archived or retired to mechanical gates by 2026-08-21, per `INDEX.md`
(already correct) and the narrowing ADR. The file entered the public repo in the *same commit* as
`INDEX.md` and the narrowing ADR, so it has been internally inconsistent with its own sibling index
since the moment it existed.

## §3 — Refuted false positives (all 4, same file class)

All 4 refuted findings were on the same pattern: `docs/personas/archive/{cro,documentation-analyst,
head-of-engineering,head-of-governance}.md` each say `**Spawned:** Yes` and describe their charter
in the present tense, with no inline retirement note. Verify agents confirmed this is the repo's
*deliberate* convention — `docs/personas/archive/README.md` states charters are "preserved, not
deleted," and `docs/personas/INDEX.md` (the canonical roster pointer) already lists each of these
seats under "Retired 2026-08-21" with a link into `archive/` and its mechanical-gate replacement.
An archived charter narrating what the role did *while active*, in present tense, is historical
record — not a live claim — exactly as this repo's own `docs/pursuits/*.md` frozen-measurement
convention (Known Trap #12, see the companion `b8` finding above) treats a frozen number. Correctly
not flagged.

## §4 — Fixes applied

All 15 fixes are additive, dated pointers next to the original text — nothing rewritten or deleted,
per this repo's Rule 7 (one canonical owner, everyone else links). Persona logs (`cio-log.md`,
`coo-log.md`, `cro-log.md`, `head-of-research-log.md`) respected their own append-only convention:
a new dated line/entry was added, the frozen original line was never edited.

| File | Fix |
|---|---|
| `docs/pursuits/a6-cursor-fleet-worker-capability.md` | Dated status update naming all three packets' actual outcomes |
| `docs/pursuits/b4-q-usoil-1.md` | Dated archival update + path correction |
| `docs/pursuits/b8-guardian-mgc-transfer-lane.md` | Superseded-ceiling pointer (×2 — the measured figure and the forward-looking re-entry bar) |
| `docs/pursuits/d10-plugin-duplicate-set.md` | Correction narrowing the "7/7 repo copies" claim to 6/7 |
| `docs/pursuits/d1-repo-belt-19-skills.md` | Two dated addenda — belt-churn status supersession, skill-count growth |
| `docs/pursuits/c6-notion-estate.md` | Public-clone caveat on the recovery tag |
| `docs/pursuits/d2-brief-authoring-user-skill.md` | Ruling pointer + dead `../../MEMORY.md` link removed |
| `docs/briefs/GSUB-1-inventory-and-dispositions.md` | Same ruling pointer at row 152 (identical drift to d2, same batch) |
| `docs/personas/cio-log.md` | Append-only ratification-outcome addendum |
| `docs/personas/coo-log.md` | Append-only ratification-outcome addendum |
| `docs/personas/cro-log.md` | Append-only ratification-outcome addendum (self-verified collateral finding) |
| `docs/personas/cfo.md` | Dated parenthetical noting F1 is ruled, not live |
| `docs/personas/head-of-research-log.md` | Append-only addendum recording Q-ORBCUSH-1's actual outcome |
| `docs/personas/ownership-map.md` | 3 Standing cells corrected (b2, b7, c1: PARK → SUBTRACT) + dated note |
| `docs/personas/research-analyst.md` | Dated roster-note narrowing the 8-name list to the 3 still-live seats |

## §5 — Scope limitations (not covered this pass)

Per this repo's no-silent-caps convention: this was a targeted pass, not a blind full-corpus scan.
Still unswept for this failure class, per `STATE.md`'s forward-obligation row: 21 of 23
`.claude/skills/*/SKILL.md`, and most `core/strategies/**/*.md` card mirrors.

## §6 — Discipline check

```
[x] Reference sheet reused from companion audits + extended with one pursuits-specific item
[x] Full scope enumerated up front (75 files), none silently dropped from the scan
[x] Scan batches sized to file length (4/batch, not 1/file) — justified given ~30-line file average
[x] Every flag independently re-verified (refute-first), not trusted from the scan pass
[x] False positives explained, not just counted (§3) — same-pattern, same-root-cause across all 4
[x] A collateral finding outside the scan's own flags (cro-log.md) self-verified before fixing, not assumed
[x] One fix landed one file outside the two named directories — logged as identical-drift, not scope creep
[x] Persona-log append-only convention respected in every log fix — no frozen entry edited in place
[x] Generated-mirror discipline: no generated file in this scope (docs/pursuits has no derived INDEX; docs/personas/INDEX.md was itself never touched, since none of its own claims were found stale)
[x] STATE.md forward-obligation row updated to reflect this sweep + the already-merged ops/instruments sweep it had not yet recorded
[x] Full gate suite run before commit
```
