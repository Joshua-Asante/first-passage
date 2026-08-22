# CC Handoff — Draft catalog hot-vs-disposition ADR

**Date:** 2026-08-22
**Parent session:** Cursor Cloud Agent (nav structural follow-on)
**Spawn target:** Claude Code (ADR authoring — locked surface per [`docs/adr/2026-07-14-cc-cursor-surface-allocation.md`](../../adr/2026-07-14-cc-cursor-surface-allocation.md))
**Repo:** `first-passage`
**Brief type:** CC handoff (multi-step)
**Parent question:** `N/A` — commissioning a new doctrine ADR, not executing an already-Accepted one
**Authority:** Joshua (CEO), in-session: plan the structural-nav follow-on, open a PR, ping Claude Code to draft the ADR and comment back on that PR. No commit/merge of parser/C2 code without a later operator GO after the ADR is `Accepted`.

---

## §0 — Rule 0 reads (PHASE 0 — execute BEFORE any §2 work)

CC: read each file below and report the stated range in your first response. Do not write the ADR, do not edit parser/C2, do not `--slug` anything until this Phase 0 read-report has been posted **on the GitHub PR** and any §0.5 halt is resolved.

- [`scripts/archive_lab_analysis.py`](../../../scripts/archive_lab_analysis.py) — report: `_NON_TERMINAL_DOMINANT` (L93–96), `parse_disposition` (L282–304), `is_archiveable` (L212–213), `_hot_sys_path_dependent` signature + first 40 lines (L796–). Anchor: `git log -1 --format='%h %ci' -- scripts/archive_lab_analysis.py` (expected `b36d350` 2026-08-16 or later on `origin/main`).
- [`scripts/check_status_consistency.py`](../../../scripts/check_status_consistency.py) — report: `LIVE_STATUS` / `TERMINAL_STATUS` (L101–102) and `check_catalog_internal` (L204–225). Anchor: `git log -1 --format='%h %ci' -- scripts/check_status_consistency.py` (expected `b36d350` 2026-08-16 or later).
- [`lab/CATALOG.md`](../../../lab/CATALOG.md) — report: header through the Active table column line (L1–25) and one Active row + one Archived row. Anchor: `1e40b11` 2026-08-22 (Phase 2 `dstruct_mnq` `--slug`).
- [`lab/analysis/README.md`](../../../lab/analysis/README.md) — report: full file (Phase 2 leftovers table). Anchor: `1e40b11` 2026-08-22.
- [`docs/adr/2026-08-08-adr-ceremony-tiering.md`](../../adr/2026-08-08-adr-ceremony-tiering.md) — report: limb-4 test + light-vs-full rule. Anchor: `91e6caa` 2026-08-15.
- [`docs/adr/2026-07-16-root-doc-charter-dedup.md`](../../adr/2026-07-16-root-doc-charter-dedup.md) — report: §2 Decision (five root docs; no sixth). Anchor: `027a729` 2026-08-14 (public-seed).
- [`docs/notes/audits/2026-08-21-coherence-campaign.md`](../../notes/audits/2026-08-21-coherence-campaign.md) — report: C-P1-10 row only. Pointer, not a second owner.
- Amendment-first (Rule 8 sub-rule 10) paste, run on `origin/main` before authoring:

```text
$ rg -n "hot vs disposition|catalog-hot-vs|ACTIVE no longer masks|hot-vs-verdict" docs/adr docs/briefs docs/notes
# expected: no matches (handoff path excepted once this file exists)
```

**No-op condition:** if `docs/adr/2026-08-22-catalog-hot-vs-disposition.md` already exists on `origin/main` at dispatch time, this packet has been overtaken — return `DONE` citing that commit; do not mint a sibling.

---

## §0.75 — Local-only dependency check

`N/A` — Spawn target is Claude Code, not Cursor. ADR-only; no vendor CSVs, no secrets.

---

## §0.5 — Clarifying questions (HALT-ON-AMBIGUITY)

Do not invent a third model. If Phase 0 contradicts a frozen default below, post `## §0.5 Response — ambiguities` on the PR and set `Status: NEEDS_CONTEXT`. Do not guess.

**(A) Column names on Active.** **Recommended default:** `hot` + `disposition`. Keeping the existing `status` cell as the disposition word and adding `hot` is acceptable if Phase 0 shows less C2 blast. Pick one in the ADR; do not ship both schemas.

**(B) Same-PR mechanical delta?** **Recommended default:** **ADR only.** Do not edit `archive_lab_analysis.py` / `check_status_consistency.py` / regenerate `lab/CATALOG.md` in this PR. Parser + C2 is a separate GO after `Accepted`.

**(C) Existing STM/LTM archive design spec.** Retrieve via `git log --follow -- docs/superpowers/specs/2026-07-11-lab-analysis-stm-ltm-archive-design.md` or `git show pre-prune-2026-08-08:…` (absent on this public clone). **Recommended default:** one pointer line in the ADR; do not restore the pruned body.

**(D) HOLD vs ACTIVE dominance.** If a card’s Verdict clause is `AMBIGUOUS-HOLD` and a Status line says `ACTIVE`, **HOLD wins** (do not archive). If Verdict is `NULL` and Status is `ACTIVE`, **NULL wins** (disposition is terminal; `hot` may still be yes).

---

## §1 — Context

Phase 2 left CATALOG honest about leftovers: 0 archiveable as stamped because `parse_disposition` returns on the first `Status:`/`Verdict:`/`Disposition:` line, and house style is `**Status:** ACTIVE — NULL: …`. C2 then forbids a terminal token in the Active table. Stay-hot FALSIFIED bodies cannot be listed honestly.

**What CC is being asked to produce:**
- [`docs/adr/2026-08-22-catalog-hot-vs-disposition.md`](../../adr/2026-08-22-catalog-hot-vs-disposition.md) — `Proposed`, **full tier** (limb 4: doctrine), `$0/K=0`.
- Regenerated [`docs/adr/INDEX.md`](../../adr/INDEX.md) via `python scripts/check_adr_graph.py --regenerate-index` in the same commit as the ADR.
- A comment on **this PR** with the four-state status line and the ADR path, pinging the Cursor session to resume.

**What CC is NOT being asked to do:** implement the parser or C2; mass-stamp `**Verdict:**`; mass `--slug`; STATE rolloff; `find-owner`; ADR `Topic:`; `gates.yml`; unify `ops/` imports; a sixth root doc; hand-edit CATALOG Status cells; retire `time_to_pass.py`.

---

## §2 — Execution plan

### Step 2.1 — Phase 0 read-report

- **Inputs:** §0 paths.
- **Action:** Read and post the report on the PR (or as the first commit message body / PR comment). Halt on §0.5 conflict.
- **Expected output:** read-report comment.
- **Per-step gate:** every §0 path exists; no-op condition false; amendment-first paste empty of prior owners.

### Step 2.2 — Draft the ADR

- **Inputs:** frozen decision below; [ADR template](../../../.claude/skills/brief-authoring/references/adr.md); ceremony-tiering ADR.
- **Action:** write the named ADR. Full §0–§7. Status token `Proposed`. Pointer to C-P1-10 and the STM/LTM design spec; do not restate their bodies.
- **Expected output:** `docs/adr/2026-08-22-catalog-hot-vs-disposition.md`.
- **Per-step gate:** `python scripts/check_brief.py docs/adr/2026-08-22-catalog-hot-vs-disposition.md --type adr` green enough to commit; `python scripts/check_adr_graph.py` green after `--regenerate-index`.

**Frozen decision (do not invent a third model):**

- Two orthogonal axes: **`hot`** (body still under `lab/analysis/` — what Active vs Archived tables mean) and **`disposition`** (campaign verdict from `**Verdict:**` when present).
- Parser: if both `**Verdict:**` and `**Status:**` exist, Verdict wins. `ACTIVE` on a Status line must not dominate a Verdict on the same card. HOLD in a Verdict clause still dominates. Keep the verdict-clause split so prose naming other statuses cannot flip the row.
- C2: join Active/Archived to **body-path / `hot`**, not to `disposition ∈ {ACTIVE, HOLD}`. A `FALSIFIED` (or `NULL`) disposition in the Active table is legal when `hot=yes`. Unrecognised tokens stay non-class-checked.
- `--slug` still requires archiveable disposition (`CLOSED` / `FALSIFIED` / `RETIRED` / `NULL`) **and** not stay-hot (`_hot_sys_path_dependent` + named inbound pins). Parser honesty does not auto-move bodies.
- Regenerator in `archive_lab_analysis.py` remains the only CATALOG writer. Do not clobber authored one-liners (Phase 2 lesson).

### Step 2.3 — Index + PR ping-back

- **Inputs:** new ADR.
- **Action:** `python scripts/check_adr_graph.py --regenerate-index`. Commit ADR + INDEX only. Comment on this PR.
- **Expected output:** INDEX delta; PR comment using the §6 closure report format.
- **Per-step gate:** diff name-only is ADR + `docs/adr/INDEX.md` (+ this handoff already on the branch). No `scripts/` edits.

### Step 2.N — Closure artifact

N/A — this handoff drafts a `Proposed` ADR; no Q-closure. The PR comment **is** the return artifact.

---

## §4 — Falsifiable hypothesis

**H:** After Phase 0, either (a) no existing ADR/brief owns the hot-vs-disposition split and the drafted ADR at the named path is `Proposed`, full-tier, and matches the frozen decision with no third model; or (b) an existing owner is found and the spawn returns `NEEDS_CONTEXT` without minting a sibling.

**Falsified if:** the spawn lands parser/C2 implementation, a mass `--slug`, a sixth root doc, an ADR that keeps `ACTIVE` on `Status:` decisive over `Verdict:`, or a C2 rule that still forbids terminal disposition in the Active table when `hot=yes`.

---

## §5 — Forbidden moves

- **Scope creep — implement the parser “while drafting.”** Log it under `DONE_WITH_CONCERNS`; do not edit `scripts/`.
- **Mass-stamp `**Verdict:**` or mass `--slug`.** Names leftovers; fights stay-hot pins. Out of this ADR.
- **Hand-edit `lab/CATALOG.md` Status cells.** Regenerator only.
- **Sixth root doc / new methodology/pursuits/spec INDEX.md.**
- **Re-deriving §0.** If an on-disk hash disagrees with the expected anchor, `NEEDS_CONTEXT` — do not proceed on the stale number.
- **Amending the frozen decision** to a third column model without asking.

---

## §6 — Gate + status return taxonomy

Spawn gate (binary for this handoff, not a Q-closure): `DONE` = RESOLVED (ADR landed per §2); `NEEDS_CONTEXT` = AMBIGUOUS (missing input); `BLOCKED` = FALSIFIED as cannot-proceed. `DONE_WITH_CONCERNS` is RESOLVED-with-flag.

Report on **this GitHub PR** with EXACTLY one of:

| Status | Meaning |
|---|---|
| `DONE` | ADR + INDEX landed; gates green; no `scripts/` touch; frozen decision matched. |
| `DONE_WITH_CONCERNS` | ADR landed but a Phase-0 tension was documented, not silently resolved. |
| `NEEDS_CONTEXT` | Existing owner found, or a §0.5 conflict. Do not mint a sibling. |
| `BLOCKED` | Structural obstruction. Sub-case required: `context-problem` / `capability-problem` / `scope-problem` / `plan-itself-wrong`. |

```
Status: <DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED — <sub-case>>
Per-step gates: 2.1 [pass/concern/skip], 2.2 [...], 2.3 [...], 2.N [skip]
Diffs (files touched): <list>
Closure artifact path: docs/adr/2026-08-22-catalog-hot-vs-disposition.md
Concerns surfaced (if any): <list>
Next action recommended: ping Cursor on this PR to review; do not implement parser/C2 until Accepted + GO
```

---

## §7 — Parent-session review (after CC returns)

**Pass 1 — Spec-compliance.** ADR path and Status token match §2; no parser/C2; no extra files beyond ADR + INDEX.

**Pass 2 — Quality.** Frozen decision present; limb 4 justified; C-P1-10 / STM-LTM are pointers; `check_adr_graph` green.

**Pass 3 — Consolidated read.** ADR + INDEX agree on Status `Proposed` and the filename slug.

---

## §10 — Audit hooks (runnable)

```bash
test -f docs/adr/2026-08-22-catalog-hot-vs-disposition.md
python scripts/check_brief.py docs/adr/2026-08-22-catalog-hot-vs-disposition.md --type adr
python scripts/check_adr_graph.py
git diff origin/main --name-only
# expected: docs/adr/2026-08-22-catalog-hot-vs-disposition.md
#           docs/adr/INDEX.md
#           docs/briefs/handoffs/2026-08-22-cc-handoff-catalog-hot-vs-disposition.md
#           docs/SESSIONS.md
# forbidden in CC's commit: scripts/archive_lab_analysis.py scripts/check_status_consistency.py lab/CATALOG.md
rg -n "hot|disposition|Verdict wins" docs/adr/2026-08-22-catalog-hot-vs-disposition.md
```

---

## Verification (parent-side, before declaring handoff complete)

```bash
python scripts/check_brief.py docs/briefs/handoffs/2026-08-22-cc-handoff-catalog-hot-vs-disposition.md --type cc_handoff
# Expected: mechanical checks PASS
```
