# P2 MEMORY demote (Approach A) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**AUTHORIZATION:** **GO 2026-08-23.** Operator: “proceed with P2 as the new #3, Approach A.” Charter: [`2026-08-23-repo-pain-point-packets.md`](2026-08-23-repo-pain-point-packets.md) §P2. Does not jump F1 (already ruled on `origin/main`) or B7/M1.

**Goal:** Rule 7 stops naming an out-of-tree `MEMORY.md` as the owner of durable atomic facts; those atoms live in owning ADRs / `docs/methodology/lessons/`; Claude-project MEMORY is assistive-only, never attestation.

**Architecture:** Amendment-first. Change the Rule 7 owner-table row (canonical). Addendum on the ADR that last assigned MEMORY that role versus STATE ([`2026-06-30-state-md-role-reduction.md`](../../adr/2026-06-30-state-md-role-reduction.md)). Rewrite the SESSIONS header plus the D1 audit/INDEX pointers. No corpus copy, no new gate, no sixth root file.

**Tech Stack:** markdown + existing `sessions-queue-bind` / path-liveness gates. No new Python.

## Global Constraints

- Approach A only. Not B (pointer index). Not C (copy the corpus into the public tree).
- Do not treat a MEMORY paste as Rule 0 / §0 evidence.
- Do not sync `C:\Users\joshu\.claude\projects\...\memory\`.
- Do not mint a sibling ADR (ceremony-tiering addendum 2026-08-15; Rule 8 sub-rule 10).
- Do not touch Rule 5, live `dd_protection` / `firm_rules`, or the Rule 7 lock-state path (that is P4).
- No hours figure. No `tier: soft`.
- Reconcile `origin/main` before writing STATE: main already closed F1 and added Q-TRADECAP-1 as queue #2.

---

## File Structure

| File | Change |
|---|---|
| `STATE.md` | After merge: keep main’s #1 B7/M1 and #2 Q-TRADECAP-1; add #3 P2; decision-index one-liner. Close #3 in the same land once Approach A is in the files. |
| `docs/operational_rules.md` | Rule 7 owner-table row + dated edit-log entry. |
| `docs/adr/2026-06-30-state-md-role-reduction.md` | Addendum: MEMORY is not the Rule 7 owner; §3 “do not fold STATE into MEMORY” still stands. |
| `docs/SESSIONS.md` | Header: drop “Complements MEMORY.md (durable atomic facts…)”. Prepend queue-led wrap-up. |
| `.cursor/rules/session-discipline.mdc` | One sentence: Claude-project MEMORY is assistive-only, never §0. |
| `docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md` | D1 disposition line (finding text stays). |
| `docs/briefs/INDEX.md` | D1 no longer “audit-note-resident open”. |
| `docs/superpowers/plans/2026-08-23-repo-pain-point-packets.md` | P2 Approach A GO / landed. |
| `docs/briefs/Q-XMEM-1-cross-surface-memory-sidecar-pilot.md` | Leave. Historical §0. Not this packet. |

---

### Task 1: Reconcile `origin/main` then cheap-falsify

**Files:** working tree only until the merge lands.

- [x] **Step 1: Merge `origin/main` into this branch**

```bash
git fetch origin
git merge origin/main
```

Expected: STATE / SESSIONS / possibly other docs conflict. Keep main’s live queue rows. Keep this branch’s bind addenda, decline addendum, P1 README, and `sessions-queue-bind`. Do **not** edit already-merged SESSIONS bodies — prepend only after the merge is clean.

- [x] **Step 2: Cheap falsifier (write the addendum against these numbers)**

```bash
# repo-root MEMORY.md must be absent
python -c "from pathlib import Path; p=Path('MEMORY.md'); print('repo MEMORY.md', p.exists())"
# Rule 7 still names MEMORY as owner
rg -n "Durable atomic facts" docs/operational_rules.md
# header still complements MEMORY as owner
rg -n "Complements \`MEMORY.md\`" docs/SESSIONS.md
```

Expected (pre-edit): `repo MEMORY.md False`; Rule 7 row is `` `MEMORY.md` + memory files ``; SESSIONS L5 still complements MEMORY as durable atoms.

- [x] **Step 3: Do not treat catalog greps as empty-prior-work**

Already run (this session): `lab/CATALOG.md` — no MEMORY-demote slug; `docs/briefs/INDEX.md` — Q-XMEM-1 closed SUBTRACT (Mem0 sidecar, not this row); D1 listed audit-note-resident; `docs/rejected_candidates.md` — no MEMORY hit.

---

### Task 2: Rule 7 + owner addendum

**Files:**
- Modify: `docs/operational_rules.md` (owner table ~L169 + edit log)
- Modify: `docs/adr/2026-06-30-state-md-role-reduction.md` (append addendum + change-history row)

**Interfaces:**
- Consumes: Task 1 falsifier counts
- Produces: Rule 7 row text later tasks must not restate; they link the addendum

- [x] **Step 1: Replace the Rule 7 row**

Replace:

```
| Durable atomic facts (by relevance) | `MEMORY.md` + memory files |
```

with:

```
| Durable atomic facts | Owning ADRs and [`docs/methodology/lessons/`](methodology/lessons/). Claude-project `MEMORY.md` + memory files (outside this worktree) are **assistive-only** — never a Rule 7 owner, never Rule 0 / §0 attestation. Same class as `repo_retrieve.py` ([Limb B](../lab/analysis/harvest/limb_b_remeasure_2026-08/RESULTS.md)). |
```

- [x] **Step 2: Edit-log entry (newest first under `### Edit log`)**

```
- **2026-08-23 — Rule 7 durable-atoms owner demoted (P2 Approach A).**
  D1 of the 2026-08-18 assumptions sweep: the prior owner path lives
  outside the worktree (no retention test, no gate). Durable atoms that
  bind future work live in owning ADRs / `docs/methodology/lessons/`.
  Claude-project MEMORY stays as a private injection surface,
  assistive-only. Does not copy the corpus in-tree. Does not touch
  Rule 5, lock-state paths (P4), or live sizing constants.
  [`state-md role-reduction addendum`](adr/2026-06-30-state-md-role-reduction.md#addendum-2026-08-23--memory-is-assistive-only-not-the-rule-7-owner).
```

- [x] **Step 3: Addendum on the 2026-06-30 ADR**

Append after `## Change history` (do not rewrite §2 / §3 / §4 / §5):

```markdown
## Addendum 2026-08-23 — MEMORY is assistive-only, not the Rule 7 owner

**Does not amend** the 4→2 STATE reduction, the two kept register sections, or §3 / §5 (“do not fold STATE into MEMORY”; “do not revive delete-STATE”). **$0 / K=0.** Limb 4 (doctrine): the Rule 7 owner-table row.

**Rule 0 (this addendum):** `docs/operational_rules.md` §7 owner table @ `e159743` (2026-08-22) — row still reads `| Durable atomic facts (by relevance) | MEMORY.md + memory files |`. Cheap falsifier (plan Task 1): repo-root `MEMORY.md` absent; SESSIONS header still names MEMORY as the complementary atom store.

**Decision:** Durable atoms that bind future work are owned by the ADR / methodology-lesson that already holds them. Claude-project `MEMORY.md` is assistive-only (outside the clone). A MEMORY paste is not a Rule 0 read and is not a sub-rule 8/10 attestation.

**Boundary:** Do not copy the Claude project memory directory into this public tree (Approach C). Do not stand up `docs/memory_index.md` (Approach B — separate GO). Do not treat this addendum as a Q-XMEM-1 re-verdict (Mem0 sidecar stays SUBTRACT).
```

- [x] **Step 4: Change-history row** on that ADR: `2026-08-23 | Addendum: MEMORY assistive-only; Rule 7 owner demoted | Joshua + Cursor`

---

### Task 3: Pointer surfaces (no silent restatement)

**Files:**
- Modify: `docs/SESSIONS.md` header only (L5)
- Modify: `.cursor/rules/session-discipline.mdc` (Retrieve section)
- Modify: `docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md` (D1)
- Modify: `docs/briefs/INDEX.md` (the “3 stay audit-note-resident” sentence)
- Modify: `docs/superpowers/plans/2026-08-23-repo-pain-point-packets.md` (P2 start-when)

- [x] **Step 1: SESSIONS header**

Replace:

```
Complements `MEMORY.md` (durable atomic facts, recalled by relevance);
```

with:

```
Durable atoms live with their owners (ADRs / `docs/methodology/lessons/`);
Claude-project `MEMORY.md` is assistive-only, never attestation;
```

- [x] **Step 2: session-discipline Retrieve section**

After the Limb B `ASSISTIVE-ONLY` paragraph, add:

```
Claude-project `MEMORY.md` (outside this worktree) is the same class:
assistive-only, never a Rule 7 owner, never a pasted §0 attestation.
Owner: [`Rule 7`](../../docs/operational_rules.md) ·
[state-md addendum](../../docs/adr/2026-06-30-state-md-role-reduction.md).
```

- [x] **Step 3: D1 disposition (do not rewrite the finding)**

Immediately after the D1 paragraph, add:

```
**Disposition 2026-08-23 (P2 Approach A):** Rule 7 owner demoted — see
[`addendum`](../../adr/2026-06-30-state-md-role-reduction.md#addendum-2026-08-23--memory-is-assistive-only-not-the-rule-7-owner).
Finding text left as the measured defect.
```

- [x] **Step 4: INDEX sentence**

Replace `3 stay audit-note-resident: D1 MEMORY.md governance reach, D5 …` with `2 stay audit-note-resident: D5 Notice-phase 5-tool coverage, D10 D-S-A canon staleness … (D1 MEMORY reach closed 2026-08-23, P2 Approach A).`

- [x] **Step 5: Charter P2** — set **Start when:** GO landed 2026-08-23, Approach A. Leave P3–P5 parked.

- [x] **Step 6: Leave `Q-XMEM-1` §0.** Historical. Blast-radius class = historical.

---

### Task 4: STATE queue + SESSIONS wrap-up

**Files:**
- Modify: `STATE.md` operator table + decision index
- Modify: `docs/SESSIONS.md` (prepend only)

- [x] **Step 1: Add row 3 (then delete it in Step 3 once the files match Approach A)**

```
| 3 | **P2 — MEMORY reach (Approach A)** — demote Rule 7 owner; MEMORY assistive-only | [`charter P2`](docs/superpowers/plans/2026-08-23-repo-pain-point-packets.md) · [`Rule 7`](docs/operational_rules.md) · [D1](docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md) | Rule 7 names an out-of-tree path as owner |
```

- [x] **Step 2: Verify the demote is in the files** — `rg -n "Durable atomic facts" docs/operational_rules.md` no longer names MEMORY as owner; the assistive-only mark is present.

- [x] **Step 3: Delete row 3** (succession: do not auto-open P3–P5). Decision-index one-liner + addendum link. Parking sentence unchanged.

- [x] **Step 4: SESSIONS entry** via `python scripts/roll_sessions.py --next-label` (PowerShell: no `head`). Open/next cites every live `#N` after the delete (`#1` `#2` only if those two remain).

- [x] **Step 5: Bind + liveness**

```bash
python scripts/check_sessions_queue_bind.py
python scripts/check_path_liveness.py
python scripts/check_root_doc_liveness.py
```

Expected: all OK.

---

## Success / falsifier

Packet fails if Rule 7 still names an unreadable-from-clone path as canonical owner with no assistive-only mark. Packet succeeds when that row is demoted and the SESSIONS header no longer calls MEMORY the complementary atom store.
