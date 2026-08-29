# SSOT Phase 2 — Running-count canonical/mirror consistency

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans. Steps use checkbox (`- [ ]`) syntax.
>
> **Authorization:** addendum on
> [`docs/adr/2026-08-27-ssot-data-lineage-remediation-program.md`](../../adr/2026-08-27-ssot-data-lineage-remediation-program.md)
> (limb-4: A8 is a new default-on `check_adr_graph` convention). Parent program plan
> [`2026-08-27-ssot-data-lineage-remediation.md`](2026-08-27-ssot-data-lineage-remediation.md)
> named this phase and refused bite-sized steps until recon (a)(b)(c) landed. This file
> is that scoped plan. **$0 / K=0.**

**Goal:** Keep the three ADR-canonical running-count lines consistent with their own
increment evidence. Do not invent a shared HTML-comment schema. Do not join
`STATE.md` or `ops/instruments/MNQ.md` (closed-row deletion is legal).

**Parent:** SSOT/data-lineage remediation program. Serves STATE queue #3. Independent
of #1/#2. This is the **program** Phase 2, not the parent ADR's §7 grep-sweep (already
done).

---

## Recon (answered 2026-08-29, this worktree, `87afe00`)

**(a) Does `check_adr_graph.py` already check running-count freshness?** No.
`DEFAULT_ENABLED_CHECKS` is `{A1..A7}` — Status vocabulary, supersession edges,
cold-store stubs, INDEX sync, age prune, STATE bullets that cite a superseded ADR
without naming the successor. Nothing parses a `Running count (canonical)` line.
The `adr-graph` gate already triggers on `docs/adr/` and `STATE.md`
([`scripts/gates.yml`](../../../scripts/gates.yml)), so A8 extends an existing
binding point.

```
$ git log --oneline -1 -- scripts/check_adr_graph.py
021a8c5 fix: 8 more high-confidence memory/gate defects from the follow-up list
```

**(b) Is there a fourth instance?** No. `rg "Authoritative surface|STATE.md is a mirror only" docs/adr/`
hits exactly three ADRs. Preregs/specs/logs cite those lines; they are not a fourth
convention.

| ADR | Canonical line (today) | Evidence shape |
|---|---|---|
| [`2026-07-15-external-mechanism-harvest-intake.md`](../../adr/2026-07-15-external-mechanism-harvest-intake.md) | `Running count (canonical): 0 / 2` | increment table, 0 `yes` rows |
| [`2026-08-15-no-counterparty-statistical-sourcing-channel.md`](../../adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md) | `2 / 3` | increment table, 2 `yes` rows (8-day lag incident) |
| [`2026-08-16-deep-iteration-lane-charter.md`](../../adr/2026-08-16-deep-iteration-lane-charter.md) | `campaigns abandoned **2**` | no table; two `*deep-lane*` preregs cited in the same paragraph |

**(c) Is a shared HTML-comment schema cheaper than three prose conventions?** No.
N=3, schemas are heterogeneous (simple `n/N` vs deep-lane's five fields), and a
STATE-mirror join is the **wrong** check: all three ADRs say STATE rows are deleted
when items close. The motivating defect was the opposite — the canonical line lagged
while `STATE.md` / `ops/instruments/MNQ.md` were current (channel ADR 2026-08-23
addendum).

Amendment-first (sub-rule 10): owner is the parent program ADR. `rg` against
`lab/CATALOG.md`, `docs/briefs/INDEX.md`, `docs/rejected_candidates.md` for
`running-count|check_adr_graph A8|ssot-phase-2` — zero hits. No new ADR file.

---

## Design

**Build A8 — intra-ADR count consistency.**

Discovery: ADR bodies that contain the counting-machinery **(a) Authoritative surface**
sentence (existing prose; no new markup). Then:

1. **Table-backed** (harvest, blind): parse the first
   `Running count (canonical): N / D` or `Running … count (canonical): N / D` after
   that sentence. Count increment-table rows whose `Increments?` cell starts with
   `yes` after stripping leading `*`. HARD-fail if `N != yes_count`.
2. **Deep-lane** (no table): parse `campaigns completed **C**`,
   `survivors falsified **F / T**`, `campaigns abandoned **A**` from the
   `Running counts (canonical, this ADR):` paragraph. Cross-check `A` against
   `*deep-lane*` prereg paths cited in that same paragraph. Do not invent a fifth
   field parser for "active campaign" in v1. Unparseable canonical line → HARD.
3. Live corpus today is consistent (`0==0`, `2==2`, `A=2`). Flip A8 into
   `DEFAULT_ENABLED_CHECKS` / `VALID_CHECKS` after a clean live run — same
   "corpus clean then default-on" posture as A5/A7 (PR #170). `VALID_CHECKS`
   must include `A8` from the first implementation commit so `--enable A8` works.

**Out of this packet (stay on their owners):**

- D4 coverage 21.4% vs the 2026-11-08 100%-or-dated-exception bar
- M1 tree-skew wired report-only (real drift on 6/6 pinned files)
- Parent-plan Phase 1 checkboxes still unchecked (hygiene only)

Queue succession: when A8 ships, **delete** STATE row 3. Do not auto-open Phase 3.

---

## Global constraints (inherited)

No trade placement. No Pine / `dd_protection.py` / `firm_rules.py` / allocations.
Mutation-test A8 before trusting it. No hand-edit of `docs/adr/INDEX.md` or
`lab/CATALOG.md`. Retention test on any new artifact.

---

## Task 1: Author this plan + point the parent plan at it

**Files:**
- Create: this file
- Modify: [`2026-08-27-ssot-data-lineage-remediation.md`](2026-08-27-ssot-data-lineage-remediation.md) Phase 2 section

- [x] **Step 1:** Write this file with recon (a)(b)(c) pasted from live reads.
- [x] **Step 2:** Replace the parent plan's "scoped, not yet detailed" Phase 2
  stub with a pointer at this file. Do not delete Phases 3–4 stubs.
- [x] **Step 3:** Commit.

```bash
git add docs/superpowers/plans/2026-08-29-ssot-phase-2-running-count-mirror.md \
        docs/superpowers/plans/2026-08-27-ssot-data-lineage-remediation.md
git commit -m "docs(plan): scope SSOT Phase 2 running-count A8 check"
```

---

## Task 2: Parent-ADR addendum + STATE row 3 retarget

**Files:**
- Modify: `docs/adr/2026-08-27-ssot-data-lineage-remediation-program.md`
- Modify: `STATE.md` (row 3 text only; do not add a fourth row)

- [x] **Step 1:** Addendum authorizing A8. Record recon (a)(b)(c). Forbid
  STATE-join and HTML-comment schema. §10 hook:
  `python scripts/check_adr_graph.py --enable A8`.
- [x] **Step 2:** Retarget STATE row 3 from "Phase 1" to "Phase 2" pointing at
  this plan + the addendum. Decision-index: one new line, keep-15 roll if needed.
- [x] **Step 3:** `python scripts/check_brief.py docs/adr/2026-08-27-ssot-data-lineage-remediation-program.md --type adr`
  and `python scripts/check_adr_graph.py`. Do not hand-edit INDEX.
- [x] **Step 4:** Commit.

```bash
git add docs/adr/2026-08-27-ssot-data-lineage-remediation-program.md STATE.md
git commit -m "docs(adr): authorize SSOT Phase 2 A8 running-count check"
```

---

## Task 3: TDD A8

**Files:**
- Modify: `scripts/check_adr_graph.py`
- Modify: `tests/test_check_adr_graph.py`

**Interfaces:**
- `check_a8(adr_dir: Path) -> list[Finding]` — body-text walk, same skip list as
  `load_adr_headers` (`INDEX.md` / `TOMBSTONES.md` / `README.md`).
- `collect_findings` calls it when `"A8" in enabled`.
- `VALID_CHECKS` gains `A8`. Leave `DEFAULT_ENABLED_CHECKS` unchanged until Task 4.

- [x] **Step 1: Failing tests first** (fixtures, not live files):

  - (a)-sentence + `2 / 3` line + one `yes` table row → finding
  - matching `0 / 2` + zero yes-rows → clean
  - deep-lane line `abandoned **2**` citing two `*deep-lane*` paths → clean
  - same paragraph `abandoned **1**` with two citations → finding
  - mutation of the 8-day defect: table has two `yes` rows, line still `1 / 3` → finding
  - ADR without the (a) sentence is invisible to A8 even if it says `0 / 2`

- [x] **Step 2:** Implement `check_a8`. Confirm tests green.
- [x] **Step 3:** Live-corpus run **before** flipping default-on:

```bash
python scripts/check_adr_graph.py --enable A8
# Expected: OK, 0 findings on the three real ADRs
```

- [x] **Step 4:** Commit.

```bash
git add scripts/check_adr_graph.py tests/test_check_adr_graph.py
git commit -m "feat(gates): A8 intra-ADR running-count consistency

Catches the 8-day class where a canonical n/N line lags its own
increment table (or a deep-lane abandoned count lags cited preregs).
Opt-in via --enable A8 until the live corpus is confirmed clean."
```

---

## Task 4: Default-on + hygiene

- [x] **Step 1:** Add `A8` to `DEFAULT_ENABLED_CHECKS`. Re-run
  `python scripts/check_adr_graph.py` (no `--enable`) — OK.
- [x] **Step 2:** `python -m pytest tests/test_check_adr_graph.py -q`
- [x] **Step 3:** Delete STATE row 3 (Phase 2 shipped; succession: no auto-replace
  Phase 3). Blast-radius: `rg` for tokens that still claim Phase 1 is the live
  queue packet (`SSOT/data-lineage remediation, Phase 1`, "Phases 2-4 remain
  scoped-not-detailed"). Repair silent restatements owed by this turn. Leave
  historical SESSIONS entries untouched (append-only).
- [x] **Step 4:** `python scripts/roll_sessions.py --next-label 2026-08-29` then
  append a wrap-up citing every **remaining** live queue row (#1 · #2).
- [x] **Step 5:** Commit.

```bash
git add scripts/check_adr_graph.py STATE.md docs/SESSIONS.md
git commit -m "feat(gates): default-on A8; close SSOT Phase 2 queue row"
```

---

## Forbidden moves

- Reopen CATALOG hot/disposition or rejection-register topology
- Touch Pine, `dd_protection.py`, `firm_rules.py`, allocations
- Require STATE.md or `ops/instruments/MNQ.md` to carry a live `n/N`
- Rewrite the three canonical count lines into a new schema
- Fold D4 21.4% or M1 report-only into this PR
- Hand-edit `docs/adr/INDEX.md` or `lab/CATALOG.md`

---

## Verification

```bash
python scripts/check_adr_graph.py --enable A8
python scripts/check_adr_graph.py
python -m pytest tests/test_check_adr_graph.py -q
python scripts/check_brief.py docs/adr/2026-08-27-ssot-data-lineage-remediation-program.md --type adr
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-29 | Initial scoped plan; recon (a)(b)(c) answered against `87afe00` | Cursor Cloud Agent |
