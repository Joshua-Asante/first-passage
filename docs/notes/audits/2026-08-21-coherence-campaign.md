# Audit Note — Repo-wide coherence campaign (generate → evaluate → deploy → measure → update)

**Audit ID:** AUDIT-2026-08-21-coherence-campaign
**Date:** 2026-08-21
**Triggered by:** operator direction — findings-first coherence walk of the five root docs then the mission pipeline; deletion allowed only after Rule 16 + inbound-reference index + operator GO (not a Great Prune retry)
**Authors:** Cursor Cloud Agent (bc-bb140041-6a2e-44b6-8ce3-04db2b24ea68) executing the ratified campaign plan
**Scope:** root orientation docs + P1 generate → P3 evaluate → P4/P5 deploy → P6 measure → X update
**Lives in:** `docs/notes/audits/2026-08-21-coherence-campaign.md`
**Domain (INQHIORI §2):** meta-process D-S-A
**Tier:** audit note (not a Pre-Q; no new `Q-*`)

---

## §0 — Source anchors

Amendment-first (Rule 8 sub-rule 10): nearest existing owners are
[`2026-08-11-rule7-dry-fact-audit.md`](2026-08-11-rule7-dry-fact-audit.md) (Option A **closed** — numeric DRY only),
[`2026-08-08-great-prune.md`](../../adr/2026-08-08-great-prune.md) §3.2 (halted classes; inbound-prose index required),
[`2026-08-07-loop-s7-repo-alignment-spec.md`](../../spec/2026-08-07-loop-s7-repo-alignment-spec.md) (Posture-A propagation).
None of those can hold a pipeline-walk register. New file is correct.

`rg` attestation (this session, before authoring):

```
# docs/briefs/INDEX.md — no "coherence-campaign" / Q-OBJCOHERE row in INDEX (Q-OBJCOHERE-1 exists as a closed instrument-composition Q; different mechanism)
# lab/CATALOG.md — no coherence-campaign
# docs/rejected_candidates.md — no coherence-campaign
```

Production reads at worktree HEAD `86e000c` (`2026-08-20 20:11:42 -0400`) after `git fetch origin main` (HEAD == `origin/main` at branch point):

- [`README.md`](../../../README.md) · [`CLAUDE.md`](../../../CLAUDE.md) · [`REPO_MAP.md`](../../../REPO_MAP.md) · [`PIPELINES.md`](../../../PIPELINES.md) · [`STATE.md`](../../../STATE.md)
- [`docs/operational_rules.md`](../../operational_rules.md) §7 / Rule 16
- [`docs/adr/2026-07-16-root-doc-charter-dedup.md`](../../adr/2026-07-16-root-doc-charter-dedup.md)
- [`docs/adr/2026-08-08-great-prune.md`](../../adr/2026-08-08-great-prune.md) §3.2 / F-2 addendum
- [`core/mc/modes.py`](../../../core/mc/modes.py) L102–126 (`PANELS_BY_BROKER["cme"]` live)
- [`ops/c1_rail/`](../../../ops/c1_rail/) (flat `ops/c1_rail_*.py` absent)
- [`lab/research_utils/universe_gate.py`](../../../lab/research_utils/universe_gate.py) · W4 ADR
- [`docs/briefs/INDEX.md`](../../briefs/INDEX.md)
- [`docs/spec/2026-08-07-loop-s7-repo-alignment-spec.md`](../../spec/2026-08-07-loop-s7-repo-alignment-spec.md)
- `git cat-file -t 45e3ceac` → `fatal: Not a valid object name` (public clone)

---

## §1 — Trigger (what prompted this audit)

Operator asked for a repo-wide coherence audit of inconsistencies, ambiguities, and hidden traps, starting at the root docs and walking generate → evaluate → deploy → measure → update, with a multi-phase plan that may delete or simplify. The 2026-08-08 Great Prune already used that mission sentence and halted `docs/briefs` / `notes` / `superpowers` / `spec` / `methodology` after 4.3% delete-classifier precision. This campaign is the next **layer**: walk owners, classify findings, repair by link/simplify, delete only as a classified exception.

**Failure class:** source-of-truth fracture (canonical artifact drift) plus hidden traps on the live pipeline.

---

## §2 — What actually happened

1. Plan frozen: findings-first; no Great Prune class 3/5–8 retry; historical ADR bodies stay; operator GO before file-collapse.
2. Seed findings verified on disk at `86e000c` (see Phase 0 table).
3. Pipeline walk executed (Phases 1–5). Highest-signal findings recorded below.
4. Packet A/B/C landed this session: root-doc + INDEX link/simplify; skill/methodology/script posture; S7 tombstone so live links no longer 404. No file deletes. No new gate. No new `Q-*`.
5. Remaining findings stay `LEFT` / `NAMED` / `OWED` for operator GO (CATALOG status, GO ADR §7 table, W5 CI roster, W6 lockfile, named-not-opened Qs).

---

## §3 — Root-doc owner map (Phase 0)

Charter: [root-doc ADR](../../adr/2026-07-16-root-doc-charter-dedup.md). Roles:

| Doc | Role | Must not silently restate |
|---|---|---|
| `README.md` | human entry index | risk %, MC numerals, live posture narrative |
| `CLAUDE.md` | agent orientation; gated lock surface (Strategy Reference / Protection / MC headline) **is an owner** | decision *narrative* (ADRs own why) |
| `REPO_MAP.md` | static layer/import map | live posture; MC numerals |
| `PIPELINES.md` | dynamic data-flow; ≤1-line disposition per row | arming gates, spend ceilings, fill history |
| `STATE.md` | open-threads + forward board + decision index | risk %, versions, hashes, owner table |

Mechanical baseline at campaign start (`86e000c`):

| Gate | Result |
|---|---|
| `check_root_doc_liveness.py` | run in Phase 7 after repairs |
| `check_path_liveness.py` | run in Phase 7 |
| `check_status_consistency.py` | run in Phase 7 |
| `check_adr_graph.py` | run in Phase 7 |

---

## §4 — Falsifiable hypothesis

**H:** Walking the five root docs then P1→P6+X against production bytes will surface load-bearing inconsistencies/ambiguities/traps that the 2026-08-11 Rule-7 DRY audit (numeric restatements) and the Great Prune (retention deletes) did not close — and a scoped inbound-reference index will show which of those can be repaired by link/simplify without a file delete.

**Falsified if:** the walk finds only already-closed Rule-7 DRY items and no live 404 / path / runnability fracture on a hot surface.

**Result:** **held.** Seed findings all verified; additional runnability (P3 `PANELS_BY_BROKER`) and Stage-6 dormancy (P1 vs W4) fractures are new relative to the 08-11 DRY audit.

---

## §5 — Forbidden moves

- Retry Great Prune classes 3, 5–8 as a bulk delete.
- Rewrite historical ADR / RESULTS / closure bodies for diet (GO ADR §2/§7 left; addenda-only).
- "Simplify" CLAUDE.md MC-anchor literals (`99.83% pass / 0.17% bust`, `p99 DD 4.37%`) — `ops/recall/guard.py` parses them.
- Touch Pine, `dd_protection` / `firm_rules` constants, allocations, or arm the rail.
- Open the 11 draft Qs from the 2026-08-18 assumptions sweep (name-Q only).
- Add a doc-budget gate (Great Prune F-2 declined).
- Reorder STATE queue rows 1–2 (F1, B7/M1).

---

## §6 — Gate

| Verdict | Criterion |
|---|---|
| `RESOLVED` (this note) | Register written; seed findings verified; inbound index scoped; Packet A/B/C landed; no file delete; S7 live links resolve to a tombstone; remaining items classified LEFT/NAMED/OWED |
| `FALSIFIED` | Walk found no new hot-surface fracture (H failed) |
| `AMBIGUOUS` | Could not verify a seed finding against disk |

Campaign-close (Phase 7 of the plan): every finding is `REPAIRED` / `LEFT` / `NAMED` / `BLOCKED`. This note closes **immediate** repair for Packets A–C; structural leftovers stay OWED.

---

## Findings register

Classes: **inconsistency** · **ambiguity** · **trap**. Dispositions: `link` · `simplify` · `delete` · `leave-historical` · `name-Q`.

### Phase 0 — Root docs (verified)

| ID | Class | Claim | Disposition | Status |
|---|---|---|---|---|
| C-P0-01 | trap | S7 owner `docs/notes/2026-08-07-posture-a-alignment-manifest.md` absent; `git show 45e3ceac:…` invalid in this public clone; ~10 live ADR/spec links 404 | tombstone at original path (Phase 7) | **REPAIRED** |
| C-P0-02 | inconsistency | `PIPELINES.md` P5 inventory lists `ops/c1_rail_*.py`; tree is `ops/c1_rail/` | simplify inventory | **REPAIRED** |
| C-P0-03 | trap | `REPO_MAP.md` admits `check_boundaries.py` never opens it; no compare-gate | leave — known coupling; do not invent a gate this campaign | **LEFT** |
| C-P0-04 | inconsistency | `PIPELINES.md` data-stores lists `ops/data/audits/`; dir gone; `reconciles/` remains | simplify | **REPAIRED** |
| C-P0-05 | inconsistency | `INDEX.md` header says closures live in `docs/ltm/briefs/`; hot closures are `docs/briefs/closures/` | simplify header | **REPAIRED** |
| C-P0-06 | inconsistency | `Q-GATESTACK-1` still in INDEX Open table with `CLOSED` status | simplify — move to Recently closed | **REPAIRED** |

### Phase 1 — Generate (P1)

| ID | Class | Claim | Disposition | Status |
|---|---|---|---|---|
| C-P1-01 | inconsistency | P1 Stage 6 lists SPA/StepM/PBO as the live CONFIRM stack; W4 + strategy-validation §8 mark SPA/StepM/PBO **dormant** | link W4 under P1 | **REPAIRED** |
| C-P1-02 | inconsistency | P1 Stage 8 BREADTH as a live step; W4 tombstoned breadth as live producer | link in same P1 note | **REPAIRED** |
| C-P1-03 | inconsistency | P1 lists MCS; `universe_gate.py` never calls MCS | simplify — drop MCS from P1 flow line | **REPAIRED** |
| C-P1-04 | inconsistency | W4 ADR §0 still says `var_trials` empirical; addendum + code flipped to `1/n` | leave-historical (ADR body); named | **LEFT** |
| C-P1-05 | trap | `universe_gate` comment says IS-best; selection uses OOS Sharpe | name-Q | **NAMED** (do not open) |
| C-P1-06 | trap | `prereg_paths.DISC_CAMP_0_PREREG` points at missing LTM body; CLI `--self-test` FileNotFound | name-Q / restore-owed | **OWED** |
| C-P1-07 | inconsistency | INDEX LTM path | = C-P0-05 | **REPAIRED** |
| C-P1-08 | inconsistency | Q-GATESTACK in Open | = C-P0-06 | **REPAIRED** |
| C-P1-09 | ambiguity | P1 "every OTHER axis unfunded" stricter than `axis_screen.py` / Q-KBUDGET-1 | simplify constraint #2 | **REPAIRED** |
| C-P1-10 | inconsistency | `lab/CATALOG.md` ACTIVE rows on closed/falsified camps | do not hand-edit CATALOG (regenerate path) | **OWED** — H2 dry-run 2026-08-21: `--check --catalog-only` OK; Status tokens unchanged; regenerate would clobber committed one-liners. Flips need `--slug` archive, not regenerate. |
| C-P1-11 | trap | P1 Stages 5–7 look like a generic runner; hot generic runner is Stages 2–4 only | simplify P1 flow caveat | **REPAIRED** |
| C-P1-12 | ambiguity | manifest `close` hands to skill §8 vs `universe_gate.py` | left — P1 W4 pointer is the cheap fix | **LEFT** |
| C-P1-16 | omission | P1 omitted W4 live floor (G0–G5+G8) | link | **REPAIRED** |

### Phase 2 — Evaluate (P3 + intake)

| ID | Class | Claim | Disposition | Status |
|---|---|---|---|---|
| C-P2-01 | inconsistency | `PIPELINES.md` / `README.md` say `PANELS_BY_BROKER` is empty; `modes.py` registers `cme` (2-leg, 2026-08-19 breadth ADR) | simplify posture | **REPAIRED** |
| C-P2-02 | trap | `modes.py` comments still say registry empty above the live dict | simplify comments | **REPAIRED** |
| C-P2-03 | trap | CLI does not exit "no registered broker panel"; `--panel cme` fails MVD filename assert | posture now names the real failure | **REPAIRED** |
| C-P2-05 | trap | `lab/analysis/time_to_pass.py` structurally dead | leave — no delete this campaign | **LEFT** |
| C-P2-07 | ambiguity | P3 (legacy book MC) vs P4 (`prop_survivor_scoring.py`) both read as "the" evaluate path | one-line P3/P4 split | **REPAIRED** |
| C-P2-08 | trap | CLAUDE lifecycle warning reads as current deployed 0.50× while no book is deployed | tense fix | **REPAIRED** |
| C-P2-11 | trap | survivor-scoring prereg §10 greps deleted `ACTIVE_FIRM` | leave-historical (frozen prereg) | **LEFT** |
| C-P2-13 | trap | `.cursor/rules/locked-params.mdc` still mandates re-running `portfolio_mc` | simplify rule | **REPAIRED** |

### Phase 3 — Deploy (P4/P5)

| ID | Class | Claim | Disposition | Status |
|---|---|---|---|---|
| C-P3-01 | inconsistency | flat `ops/c1_rail_*.py` | = C-P0-02 | **REPAIRED** |
| C-P3-02 | omission | P5 inventory omitted daemon + `deploy/c1_signal_daemon/` | simplify | **REPAIRED** |
| C-P3-03 | inconsistency | P5 substrate "Strategy alerts" (TV framing) vs S2 Python host | simplify | **REPAIRED** |
| C-P3-04 | inconsistency | P2 "Pine remains the execution language of the P5 rail" vs S2 | simplify | **REPAIRED** |
| C-P3-05 | trap | `docs/notes/rail_build/RUNBOOK.md` 404; public owners still cite it | live owners → `deploy/c1_rail/README.md`; historical briefs left | **REPAIRED** (live) |
| C-P3-06 | inconsistency | GO ADR §7 still B6 PENDING vs header B6 PASSED | leave-historical (ADR body) | **REPAIRED** — addendum 2026-08-21 (table left; header owns this-build B6) |
| C-P3-08 | inconsistency | c1-rail skill L10 "daemon … specified, not built" vs tree + L8 | simplify | **REPAIRED** |
| C-P3-09 | inconsistency | deploy README "fork F2 (08-08)" reads open; S1 ruled F2 | simplify banner | **REPAIRED** |
| C-P3-10 | inconsistency | `strategy_lifecycle.md` "automated rail unbuilt" | simplify | **REPAIRED** |
| C-P3-11 | trap | `scripts/m1_item5_dump.ps1` calls `ops/c1_rail_arm.py` | simplify path | **REPAIRED** |
| C-P3-15 | inconsistency | c1-rail skill "symbols RETAINED, not released" vs MYM occupancy-release ADR | simplify | **REPAIRED** |

### Phase 4 — Measure (P6)

| ID | Class | Claim | Disposition | Status |
|---|---|---|---|---|
| C-P4-01 | ambiguity | M1 `CODE_LANDED` vs `RESOLVED` arm gate | one-line P6 cross-link | **REPAIRED** |
| C-P4-02 | trap | M1 item 5 undischargeable without a deployed strategy | ACK — STATE queue #2 | **LEFT** |
| C-P4-03 | trap | Q-NAS-ECR first-fill release unreachable | leave; P6 already accurate | **LEFT** |
| C-P4-04 | inconsistency | INDEX Q-SIGID "STRANDED" vs S2b built | simplify INDEX next-action | **REPAIRED** |
| C-P4-08 | trap | M1 tree-skew check not in `gates.yml` | name-Q (`Q-M1WIRE-1`) | **NAMED** |

### Phase 5 — Update (X)

| ID | Class | Claim | Disposition | Status |
|---|---|---|---|---|
| C-P5-01 | trap | SESSIONS Open/next does not echo STATE queue | this session's SESSIONS entry echoes queue | **REPAIRED** |
| C-P5-02 | inconsistency | STATE "Last curated: 2026-08-18" with 2026-08-20 index rows | leave (no STATE decision-index for this campaign) | **LEFT** |
| C-P5-03 | trap | S7 manifest 404 | = C-P0-01 | **REPAIRED** |
| C-P5-04 | trap | W5 CI jobs from `gates.yml` still owed | name — do not open | **OWED** |
| C-P5-05 | trap | `requirements-research.lock` OWED (W6) | name — do not invent | **OWED** |
| C-P5-06 | inconsistency | W5 claims `make validate` ≡ `make check`; `gate_manifest.py` validate tier is 2 gates | leave (CLAUDE already correct; ADR addendum owed) | **REPAIRED** — W5 addendum 2026-08-21 |
| C-P5-07 | trap | R5 unfireable ceremony (quarterly-only falsifiers) | programme-audit cadence; not this campaign | **LEFT** |

---

## Inbound-reference index (scoped)

Great Prune §3.2 instrument. Scoped to paths this campaign might collapse or repoint — **not** a whole-tree delete feed. Citations include markdown links, backticks, and hook commands.

### `docs/notes/2026-08-07-posture-a-alignment-manifest.md`

| Surface | Form |
|---|---|
| S7 spec L6, L30 | markdown link |
| `docs/adr/2026-08-07-loop-s{1,2,5}*.md` · W1/W4/W5/W6 | markdown `Related` / §7 |
| `docs/operational_rules.md` ~L749 | markdown link |
| `STATE.md` decision-index 2026-08-07 | `git show 45e3ceac:…` (object **absent** here) |

**Ruling:** restore-as-tombstone at the original path so links resolve. Do not treat tombstone rows as S7 discharges. Full ~70-row body is not in this public clone.

### `ops/c1_rail_*.py` (flat glob)

| Surface | Form |
|---|---|
| `PIPELINES.md` L15 | backtick glob |
| M1 ADR audit hook | backtick glob (historical ADR — **left**) |
| `scripts/m1_item5_dump.ps1` L34 | runtime command |

**Ruling:** repoint hot operational surfaces; leave frozen ADR hook text.

### `docs/notes/rail_build/RUNBOOK.md`

| Surface | Form |
|---|---|
| GO ADR §7, deploy README, `c1_rail_slippage.py`, c1-rail skill | markdown / prose |
| On-disk public tree | **missing** (only `M1_MONITORING_ACCEPTANCE.json`) |

**Ruling:** live owners point at `deploy/c1_rail/README.md` + GO ADR. Frozen briefs left.

### `ops/data/audits/`

| Surface | Form |
|---|---|
| `PIPELINES.md` data-stores | table cell |
| `REPO_MAP.md` | already records deletion |

**Ruling:** drop `audits/` from PIPELINES data-stores.

### `docs/ltm/briefs/` as live closure home

| Surface | Form |
|---|---|
| `INDEX.md` L5–9, L220 | convention prose |
| Actual hot closures | `docs/briefs/closures/` (84 files) |
| A few restored LTM closures | still valid historical retrieval |

**Ruling:** INDEX convention names `docs/briefs/closures/` as the hot home; LTM as archive/history.

### Delete candidates considered and **not** deleted

| Path | Why not |
|---|---|
| `lab/analysis/time_to_pass.py` | inbound from lifecycle Call 4; Rule 16 not run for delete |
| `lab/CATALOG.md` ACTIVE rows | generated; `archive_lab_analysis.py --regenerate-catalog` is the owner path |
| Any ADR body | S7 boundary + Great Prune F-2 |

---

## Phase 6 — Disposition packets

### Packet A — root docs + INDEX (link/simplify; no delete)

In scope: C-P0-02, C-P0-04, C-P0-05, C-P0-06, C-P1-01/02/03/09/11/16, C-P2-01/03/07, C-P3-01/02/03/04, C-P4-01, C-P4-04.

### Packet B — skills / methodology / scripts / comments

In scope: C-P2-02, C-P2-08, C-P2-13, C-P3-08/09/10/11/15, C-P5-01.

### Packet C — S7 tombstone

In scope: C-P0-01 / C-P5-03. File created at the original path. Historical ADR Related lines now resolve; they are **not** rewritten.

Operator GO for this session = the implement-the-plan instruction. File-collapse and bulk CATALOG/ADR deletes remain **not** GO'd.

---

## §7 — Programme-audit signal check

- [ ] Belt-patches without independent corroboration?
- [x] Belt that only grows, never prunes? — campaign **simplifies** hot prose; does not prune the ADR corpus (F-2 already ruled that count ≠ ceremony).
- [ ] Falsifier thresholds drifting?
- [ ] Methodology invoked to rationalize a decision already made?
- [ ] SNAG?
- [ ] Cross-layer contamination? — this note cites pipeline docs and code, not portfolio P&L.
- [ ] Negative heuristic crossed without repair?

No programme-audit escalation. Belt-growth flag is informational (we did not prune ADRs, by standing law).

---

## §10 — Audit hooks

```bash
# S7 tombstone exists (must not 404)
test -f docs/notes/2026-08-07-posture-a-alignment-manifest.md

# Flat rail glob stays empty
! ls ops/c1_rail_*.py 2>/dev/null

# INDEX Open table must not carry Q-GATESTACK-1
! rg -n "Q-GATESTACK-1" docs/briefs/INDEX.md | rg "Open" -n  # Open section only — Recently closed may cite it
python -c "
from pathlib import Path
p = Path('docs/briefs/INDEX.md').read_text()
open_sec = p.split('## Recently closed')[0]
assert 'Q-GATESTACK-1' not in open_sec, 'GATESTACK still in Open section'
"

# P3 empty-registry claim gone from hot orientation docs
! rg -n 'PANELS_BY_BROKER\` is empty' PIPELINES.md README.md

# Mechanical
python scripts/check_root_doc_liveness.py
python scripts/check_path_liveness.py
python scripts/check_status_consistency.py
python scripts/check_adr_graph.py
```

Recurrence: next quarterly programme audit, or any session that edits PIPELINES/INDEX/S7.

---

## §11 — Closure

- **Status:** `Closed (immediate + structural complete for Packets A–C; leftovers OWED)`
- **Immediate repair completed:** 2026-08-21
- **Structural leftovers:** CATALOG ACTIVE-on-closed needs `--slug` archive (C-P1-10; regenerate withheld 2026-08-21); W5 CI roster + W6 lockfile (H6/H7 HOLD); `Q-M1WIRE-1` / C-P1-05 / C-P1-06 named not opened; `time_to_pass.py` retire GO
- **Follow-up audits:** none spawned

---

## Verification

```bash
python scripts/check_brief.py docs/notes/audits/2026-08-21-coherence-campaign.md --type audit
# Expected: mechanical subset PASS (skill-side audit type maps to generic)

# Production-source verification
git log -1 --format='%h %ci'   # 86e000c at branch point
test -f docs/notes/2026-08-07-posture-a-alignment-manifest.md
test ! -e ops/data/audits
```
