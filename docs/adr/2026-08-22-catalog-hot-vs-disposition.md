# ADR — CATALOG splits `hot` (body location) from `disposition` (campaign verdict); Verdict wins over Status; C2 joins to `hot`

Filename: `docs/adr/2026-08-22-catalog-hot-vs-disposition.md`

**Status:** `Accepted` — ratified by operator (Joshua) 2026-08-22, in-session ("accepted. GO"); Phase 1 (parser + C2 + `hot` column) lands in the same GO.
**Decision date:** 2026-08-22
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Authors:** Cursor Cloud Agent (commission, PR #98) + Claude Code (draft)
**Related:** [`2026-08-08-adr-ceremony-tiering.md`](2026-08-08-adr-ceremony-tiering.md) (limb-4 tier test) · [`2026-07-16-root-doc-charter-dedup.md`](2026-07-16-root-doc-charter-dedup.md) (no sixth root/index doc) · [`docs/notes/audits/2026-08-21-coherence-campaign.md`](../notes/audits/2026-08-21-coherence-campaign.md) C-P1-10 (regenerator-only CATALOG writer) · `docs/superpowers/specs/2026-07-11-lab-analysis-stm-ltm-archive-design.md` (pointer only — pruned from the public tree; retrievable via `git show pre-prune-2026-08-08:docs/superpowers/specs/2026-07-11-lab-analysis-stm-ltm-archive-design.md`, confirmed retrievable this session)
**Layer:** governance convention (lab hygiene tooling). **$0 / K=0.**
**Tier:** full — limb 4 fires (creates a parsing/gating convention — Verdict-wins precedence, the `hot`/`disposition` axis split, the C2 join key — that binds `archive_lab_analysis.py`, `check_status_consistency.py`, and every future CATALOG-consuming script).

---

## §0 — Rule 0 reads (production-source verification)

All read this session on 2026-08-22, before authoring, per the commissioning handoff
([`docs/briefs/handoffs/2026-08-22-cc-handoff-catalog-hot-vs-disposition.md`](../briefs/handoffs/2026-08-22-cc-handoff-catalog-hot-vs-disposition.md)):

- `scripts/archive_lab_analysis.py` — anchor `b36d350` (2026-08-16 23:40:04 -0400, confirmed via `git log -1 --format='%h %ci' -- scripts/archive_lab_analysis.py`). `_NON_TERMINAL_DOMINANT` (L93–96): case-sensitive `HOLD`/`ACTIVE` regexes, deliberately upper-only so lowercase prose can't hijack a closure. `parse_disposition` (L282–304): scans the card's head lines top-to-bottom and **returns on the first line** that matches a `Disposition:`/`Status:`/`Verdict:` field — field *type* does not currently arbitrate; line *order* does. `is_archiveable` (L212–213): `status in _ARCHIVEABLE` — a plain set-membership test, unaffected by this ADR. `_hot_sys_path_dependent` (L796–817): walks every other hot slug's `.py` files for a `sys.path`-style import of the candidate slug; returns the consuming slug's name if found, `None` otherwise — this is the existing stay-hot pin mechanism `--slug` already respects.
- `scripts/check_status_consistency.py` — anchor `b36d350` (same commit as above). `LIVE_STATUS`/`TERMINAL_STATUS` (L101–102): `{"ACTIVE", "HOLD"}` / `{"CLOSED", "FALSIFIED", "RETIRED"}` — closed vocab, unrecognised tokens never class-checked. `check_catalog_internal` (C2, L204–225): for each row, `expected_tier = "live" if table == "active" else "archived"` (checked against `body_tier`, untouched by this ADR), then `status_class = live|terminal|None` from the two frozenset above, compared against `expected_class = live if table == "active" else terminal` — **this is the clause this ADR retargets**: it currently joins table membership to status-word *class*, which is exactly what forbids a terminal disposition from sitting in the Active table. The parser above it (`col_map.get("status")`, L181) is **name-keyed**, not positional, when the header row contains `theme` — confirmed by reading the column-detection block (L140–200).
- `lab/CATALOG.md` — anchor `1e40b11` (2026-08-22 02:59:09 +0000, Phase 2 `dstruct_mnq` `--slug`). Header (L1–19): "Do not glob `lab/analysis/` alone to infer what is live." Active table header (L20–25): `| slug | theme | status | one-liner | body | heavy |` — six columns, no `hot` column today.
- `lab/analysis/README.md` — anchor `1e40b11` (same commit). Full file read: Phase 2 leftovers table names 20 held-back slugs with reasons (`HOLD`, stay-hot imports, frozen prereg, `AMBIGUOUS-HOLD`, `SCREEN-FAIL`, no-source-card) — every one of them is exactly the "stay-hot terminal body" class this ADR's `hot`/`disposition` split makes listable.
- `docs/adr/2026-08-08-adr-ceremony-tiering.md` — anchor `91e6caa` (2026-08-15 04:10:56 +0000). Limb-4 test: "creates or amends doctrine — a rule, gate, falsifier threshold, or convention that binds future work" → full tier. Confirms this ADR's tier.
- `docs/adr/2026-07-16-root-doc-charter-dedup.md` — anchor `027a729` (2026-08-14 22:48:01 -0400). §2: five root docs, no sixth; extends Rule 7 (one canonical owner per fact) to decision narrative. This ADR adds no new index/root doc — it amends the CATALOG's existing two-table (Active/Archived) shape only.
- `docs/notes/audits/2026-08-21-coherence-campaign.md` — anchor `cd0b4c4` (2026-08-21 05:07:04 +0000). C-P1-10 row: "do not hand-edit CATALOG (regenerate path)" — `archive_lab_analysis.py --regenerate-catalog` is confirmed the sole CATALOG writer; this ADR's decision preserves that (§2, last clause).

**Amendment-first (Rule 8 sub-rule 10), run on this branch before authoring:**

```
$ rg -n "hot vs disposition|catalog-hot-vs|ACTIVE no longer masks|hot-vs-verdict" docs/adr docs/briefs docs/notes
# 0 hits outside the commissioning handoff itself (which the no-op condition excepts) — no prior owner found.
```

**No-op condition:** `docs/adr/2026-08-22-catalog-hot-vs-disposition.md` did not exist on `origin/main` at dispatch — this ADR is not a sibling of an existing one.

---

## §1 — Context

Phase 2 CATALOG hygiene ([`2026-08-22d` session](../SESSIONS.md)) inventoried the Active table and found **0 slugs archiveable as stamped** against 88 `ACTIVE` / 11 `HOLD` rows, even though `lab/analysis/README.md`'s Phase 2 leftovers table names at least a dozen bodies whose research question is already decided (`FALSIFIED`, `NULL`, `SCREEN-FAIL`, `CLOSED`) but that must legitimately stay under `lab/analysis/<theme>/<slug>/` — because another live camp imports them (`_hot_sys_path_dependent`), because a frozen prereg or `rejected_candidates` entry pins the path, or because a sentinel path reference would break.

The mechanism is `parse_disposition` returning on the **first** field line in a card's head, combined with house style writing the verdict inline on the `**Status:**` line itself (`**Status:** ACTIVE — NULL: <one-liner>`, per the Phase 2 leftovers table entries). `check_status_consistency.py`'s C2 then reads that same value, splits it at the verdict-clause dash, and checks `_NON_TERMINAL_DOMINANT` against the clause **before** the dash — so `ACTIVE` (the pre-dash clause) wins the class check even when a terminal verdict (`NULL`, `FALSIFIED`) follows it on the same line. C2 is a HARD gate that "forbids a terminal token in the Active table" (join: table membership vs. status-word class) — so a card can never honestly carry both "still under `lab/analysis/`" and "the campaign is decided" at once. The corpus's own leftovers table is the proof: every held-back stay-hot body in it is, in truth, disposition-terminal.

**Decision driver (one sentence):** CATALOG conflates two independent facts — where a body lives (`hot`) and what its campaign concluded (`disposition`) — into one status word gated by one HARD check, so the Active table cannot list a stay-hot terminal body without either lying about the disposition or tripping C2; splitting the two axes lets both be told truthfully in the same row.

---

## §2 — Decision

**Decision:** CATALOG rows carry two orthogonal, independently-truthful facts. Neither the parser's field-precedence rule nor C2's join key may collapse them back into one.

1. **Two axes.**
   - **`hot`** — is the body still under `lab/analysis/<theme>/<slug>/`? This, and only this, is what the Active-vs-Archived table membership means.
   - **`disposition`** — the campaign verdict, read from the card's `**Verdict:**` field when one is present.
   These are independent: `hot=yes` + a terminal `disposition` is a legal, common row (every Phase 2 leftover). `hot=no` + a non-terminal `disposition` is not expected under current practice but is not itself an error this ADR polices.

2. **Column naming: keep `status`, add `hot`.** Do not rename the existing `status` table column to `disposition`. Phase 0 confirms `check_status_consistency.py:181` reads it by name (`col_map.get("status")`, name-keyed since the Active table header carries `theme`) and `sync_liveness_indexes.py` carries 11 further `status`-keyed references — a rename touches both call sites plus every doc that names the column, for a purely cosmetic gain, since the cell's actual content (the disposition word) does not change under this decision. The lower-blast path — confirmed by this Phase-0 evidence, not asserted — is: `status` keeps its header text and continues to hold the disposition word (`ACTIVE`/`HOLD`/`FALSIFIED`/`NULL`/…); a new `hot` column (`yes`/`no`) is added alongside it. This is the one column-naming model this ADR ships; a mixed schema (some tables renamed, others not) is not authorized.

3. **Parser: Verdict wins.** When a card's head carries both a `**Verdict:**` field and a `**Status:**` field (as two separate lines, not one inline value), `parse_disposition` must resolve `disposition` from the `**Verdict:**` field, not from whichever field line happens to appear first. `**Status:** ACTIVE` on a card that also carries a decided `**Verdict:**` line does not mask it. Dominance inside a single value (the existing `_NON_TERMINAL_DOMINANT` verdict-clause-split logic) is unaffected and composes with this: **`HOLD` in the verdict clause still dominates** a later terminal-looking token (do not archive an `AMBIGUOUS-HOLD` card); **`NULL` in the verdict clause dominates** a co-occurring `ACTIVE` (the disposition is terminal; `hot` may still legitimately be `yes`).

4. **C2 joins to `hot`, not to disposition class.** `check_catalog_internal`'s status-class limb currently checks `status_class(disposition) == expected_class(table)`. That limb is retargeted to check `hot == (table == "active")` instead. A `FALSIFIED` or `NULL` disposition sitting in the Active table is legal exactly when `hot=yes`. Unrecognised disposition tokens stay non-class-checked, unchanged from today.

5. **`--slug` eligibility is unchanged and still two-part.** Archiving via `archive_lab_analysis.py --slug` continues to require **both** an archiveable disposition (`CLOSED`/`FALSIFIED`/`RETIRED`/`NULL` — `is_archiveable`, untouched) **and** the absence of a stay-hot pin (`_hot_sys_path_dependent` plus the named inbound-reference pins already carried in `lab/analysis/README.md`'s leftovers table). Parser/C2 honesty under this ADR does **not** auto-move any body; a row can be `hot=yes` + terminal `disposition` indefinitely if a pin holds.

6. **Regenerator stays the sole CATALOG writer.** `archive_lab_analysis.py --regenerate-catalog` remains the only path that touches `lab/CATALOG.md`'s table rows (C-P1-10). This ADR does not authorize hand-editing a `status` or `hot` cell.

**Effective:** upon `Accepted` (operator 2026-08-22). Phase 1 mechanical edits (parser, C2, `hot` column) land in the same GO; they do not wait on a later Status flip.
**Scope:** `lab/CATALOG.md` Active/Archived tables, `scripts/archive_lab_analysis.py` (`parse_disposition`, `--slug` gating unchanged), `scripts/check_status_consistency.py` (C2 only — the tier limb is untouched), and `lab/analysis/README.md`'s Phase 2 leftovers table (which becomes partially obsolete once implementation lands, since several of its held-back rows will list honestly).

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Rename `status` → `disposition`, add `hot` (the handoff's first-listed default) | Phase 0 shows concrete extra blast for no semantic gain: `check_status_consistency.py:181`'s name-keyed `col_map.get("status")` and 11 further `status`-keyed references in `sync_liveness_indexes.py` would all need updating, plus every doc/comment naming the column — while the cell's actual content is unchanged by this decision either way. |
| Encode both facts in one cell (e.g. `FALSIFIED (hot)`) — no second column | Reinvents a compound-token grammar the corpus has already been burned by (`**Status:** ACTIVE — NULL: …` is precisely today's masking bug). A dedicated boolean `hot` column is a strictly simpler parse than a second embedded clause inside `status`, and keeps `is_archiveable`/`LIVE_STATUS`/`TERMINAL_STATUS` as clean closed-vocab checks on one field. |
| Status quo — C2 continues joining table membership to disposition-status class | This is the bug, not an alternative: it is what currently forbids a decided (terminal) campaign from being listed truthfully while its body legitimately stays hot, and is why Phase 2 measured 0/99 archiveable against a leftovers table naming ~20 stay-hot terminal bodies. |
| A third table/section ("hot-but-terminal") instead of a `hot` column on the existing two tables | Creates a third CATALOG surface the root-doc charter's "no sixth root doc, no new index" discipline argues against by extension — `lab/CATALOG.md`'s two-table (Active/Archived) shape is itself already a charter-level convention (`lab/analysis/README.md` header), and a third table doubles the join surface C2 has to reason about instead of retargeting one join key. |

---

## §4 — Falsifier (revert trigger)

**H:** Retargeting C2's join key from disposition-status-class to `hot`, and making the parser resolve `disposition` by field type (Verdict wins) rather than by line order, will let the Active table list stay-hot terminal bodies truthfully without losing C2's ability to catch genuine table/body mismatches, and without producing new false positives against the stay-hot pins `lab/analysis/README.md` already names.

**Revert trigger:** After the parser/C2 implementation lands (Phase 1, this GO — see §7) and `python scripts/check_status_consistency.py` is re-run against the full corpus, **either** (a) C2 raises a HARD finding on any row whose `hot=yes` matches a pin already named in `lab/analysis/README.md`'s Phase 2 leftovers "Hold / leave" table (a false positive this ADR's join was supposed to clear), **or** (b) C2 fails to flag a row where `hot` and table membership genuinely disagree (a case the pre-ADR status-class join would have caught) — either one falsifies H for that clause.

**Revert action:** author a superseding ADR (full or in-part per the standard edge rules) that restores some blend of the two join keys or repairs the specific parser/C2 defect; never hand-edit `check_status_consistency.py`'s C2 logic or this ADR's decision text silently.

**Trigger check schedule:** the first full-corpus `check_status_consistency.py` run immediately after the parser/C2 implementation lands (Phase 1 landed in this PR under the 2026-08-22 operator GO — see §7; that check is this GO's `check_status_consistency.py` pass); re-checked again at the next quarterly programme audit.

---

## §5 — Forbidden moves (under this ADR)

- **Implementing the parser/C2 change, or regenerating `lab/CATALOG.md` with a `hot` column, in this same commission.** The handoff commissioning this ADR is explicit: ADR only, no `scripts/` edit, no CATALOG regen. Tempting because the fix is now fully specified and small — ruled out because `Proposed → Accepted` is the operator ratification gate this decision needs before it binds `archive_lab_analysis.py` and `check_status_consistency.py`. (Discharged: the later 2026-08-22 operator GO authorized Phase 1 in this PR; see §7.)
- **Mass-stamping `**Verdict:**` fields or mass `--slug`-ing now that the leftovers are enumerated.** Out of scope for this ADR; a separate GO per the handoff and per standing dedup-first discipline.
- **Renaming `status` → `disposition` "while in the file" for symmetry with the axis names.** §2 item 2 makes a specific blast-radius call against this; revisiting it requires new Phase-0 evidence that the blast estimate above was wrong, not a naming preference.
- **A third schema (e.g., encoding `hot` as a third status token instead of a column, or inventing a third table).** §3 already weighed and ruled out both; do not re-litigate without new evidence.
- **Silently loosening the `--slug` eligibility rule (item 5) "since honesty is now restored."** Parser/C2 honesty and archival eligibility are deliberately decoupled — a row can be truthfully `hot=yes` + terminal forever if a pin holds; this ADR does not authorize moving bodies.

---

## §6 — Consequences

**Positive consequences:**
- The Active table can list a stay-hot `FALSIFIED`/`NULL`/`CLOSED` body without either masking its disposition or tripping C2 — closing the gap Phase 2 measured (0/99 archiveable against ~20 named stay-hot terminals).
- C2 becomes a check on the fact it can actually verify mechanically (does the body live where the table says) rather than a check that conflates body location with campaign outcome.
- `lab/analysis/README.md`'s Phase 2 leftovers table stops being the only honest record of stay-hot terminal bodies once the `hot` column lands — that information moves from a hand-maintained prose table back into the machine-readable CATALOG.

**Negative consequences (real cost):**
- One more column in a table already carrying six; every future CATALOG-reading script (human or tooling) must understand that `status`/`disposition` alone no longer implies Active-table membership.
- `status` keeps a column name that undersells what it now formally means (a disposition, not a lifecycle status) — an accepted cost of the lower-blast naming call in §2 item 2, not a free win.
- Anything currently relying on C2's old behavior (table membership implies non-terminal disposition) as an implicit invariant, if any exists beyond `check_status_consistency.py` itself, silently stops being true once implemented — Phase 2 of §7 is where that gets swept.

**Risks:**
- Implementation drift: if the parser rewrite (item 3) and the C2 retarget (item 4) land in separate, uncoordinated changes, the two could disagree on what "Verdict wins" means in an edge case. Mitigation: §7 Phase 1 requires both land in the same implementation PR, sharing one column-detection/field-precedence understanding.
- The `hot` column, once added, is only as correct as `_hot_sys_path_dependent`'s import-detection plus the manually-named inbound pins — a body could be `hot=no` and still be depended on by something the scanner can't see (e.g. a non-Python reference). This is an existing risk of the current stay-hot mechanism, not new; unaffected by this ADR.

**Downstream artifacts that need updating (Phase 1, landed this GO — see §7):**
- `scripts/archive_lab_analysis.py` — `parse_disposition` field-precedence rewrite (Verdict wins over Status when both present as separate lines); `--slug` gating (`is_archiveable`, `_hot_sys_path_dependent`) is read, not rewritten.
- `scripts/check_status_consistency.py` — C2's status-class join in `check_catalog_internal` retargeted to the `hot` column.
- `lab/CATALOG.md` — regenerated (regenerator only) to add the `hot` column to the Active table header and rows.
- `lab/analysis/README.md` — Phase 2 leftovers table gets a follow-up note once implementation lands (which of its ~20 named holds now list honestly in CATALOG vs. which still need a pin); not rewritten by this ADR.

---

## §7 — Implementation plan

**Phase 0 (done):** §0 reads above; ADR authored `Proposed`.

**Phase 1 (this GO, 2026-08-22):** Verdict-wins `parse_disposition`; C2 join retargeted to `hot`; `lab/CATALOG.md` regenerated with a `hot` column. `--slug` gating unread-as-rewritten.

**Phase 2 (with Phase 1):** grep-sweep — (i) `check_status_consistency.py` C2 docstring retargeted; (ii) `sync_liveness_indexes.py` `archive_owed_active` is header-name-keyed so the new `hot` column does not steal the one-liner index. §1 above is the pre-implementation defect record.

**Phase 3 (with Phase 1):** `check_status_consistency.py` full-corpus pass is the §4 falsifier check. Status is already `Accepted` by operator ratification; this phase does not flip it.

Phase 1 is authorized by the 2026-08-22 operator GO, not by this file's original "ADR only" commission.

---

## §10 — Audit hooks (runnable)

```bash
# This ADR exists and is well-formed
test -f docs/adr/2026-08-22-catalog-hot-vs-disposition.md
python scripts/check_brief.py docs/adr/2026-08-22-catalog-hot-vs-disposition.md --type adr
python scripts/check_adr_graph.py

# ADR-only commission file set (historical of the draft pass; Phase 1 later
# landed in this PR under the 2026-08-22 operator GO — see §7)
git diff origin/main --name-only
# draft-pass expected: docs/adr/2026-08-22-catalog-hot-vs-disposition.md
#                      docs/adr/INDEX.md
#                      docs/briefs/handoffs/2026-08-22-cc-handoff-catalog-hot-vs-disposition.md
#                      docs/SESSIONS.md
# Phase 1 also touched: scripts/archive_lab_analysis.py
#                       scripts/check_status_consistency.py
#                       lab/CATALOG.md
#                       lab/analysis/README.md

# Frozen-decision vocabulary present (not silently narrowed)
rg -n "hot|disposition|Verdict wins" docs/adr/2026-08-22-catalog-hot-vs-disposition.md

# Phase 1 readiness check (historical of the draft pass; Phase 1 landed — see §7)
rg -n 'col_map.get\("status"\)' scripts/check_status_consistency.py
rg -c 'status' scripts/sync_liveness_indexes.py

# §4 falsifier re-check (run after Phase 1 implementation lands)
python scripts/check_status_consistency.py
```

---

## Verification

```bash
python scripts/check_brief.py docs/adr/2026-08-22-catalog-hot-vs-disposition.md --type adr
# Expected: all 6 checks PASS

python scripts/check_adr_graph.py
# Expected: exit 0; A1/A2 (skipped while Proposed)/A3/A6 pass

# Production-source verification (Rule 0 confirmation)
git log -1 --format='%h %ci' -- scripts/archive_lab_analysis.py scripts/check_status_consistency.py lab/CATALOG.md lab/analysis/README.md docs/adr/2026-08-08-adr-ceremony-tiering.md docs/adr/2026-07-16-root-doc-charter-dedup.md docs/notes/audits/2026-08-21-coherence-campaign.md

# ADR-only commission expected empty scripts/CATALOG delta; Phase 1 later
# landed those paths in this PR (see §7)
git diff origin/main --name-only -- scripts/ lab/CATALOG.md
```

---

## Addendum — 2026-08-29

**Operator-ratified** (Joshua, in-session GO on the drafted content of this addendum, 2026-08-29 —
same ratification pattern as §2's own "accepted. GO"; recorded here per this ADR's own
Change-history convention rather than left implicit). **Does not amend §2's two-axis decision, the
parser/C2 retarget, or `--slug` eligibility (item 5).**

**Worktree-isolated single-row hand-insert is a sanctioned exception to §2 item 6** ("Regenerator
stays the sole CATALOG writer... This ADR does not authorize hand-editing a `status` or `hot`
cell."). Item 6 is under repeated real tension with lived practice, distinct from C-P1-10's own
already-repaired defect (misclassified *existing* rows, closed 2026-08-21 via `--slug` archive):

- A [2026-08-20 Cursor handoff](../briefs/handoffs/2026-08-20-cursor-handoff-aegis-3leg-risk-parameterization.md)
  §2 step 6 explicitly instructed adding one new `lab/CATALOG.md` row by hand rather than running
  `--regenerate-catalog`, "known to clobber unrelated hand-curated rows from a worktree; hand-insert
  only."
- The 2026-08-29 `db91a21` commit did the identical thing — one slug-sorted row for
  `lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/` — each instance verified via
  `git diff --stat` showing `+1` line only.

The tension in both cases is a **brand-new row under active worktree concurrency**, where a full
regen would clobber a concurrent worktree's uncommitted heavy-artifact-column values — a different
failure mode than C-P1-10's stale-classification defect.

**The sanctioned exception, narrowly scoped:** a single new row, appended in slug-sorted position
and verified by `git diff --stat` to add exactly that one line — no existing `status`/`hot`/other
cell touched — is the sanctioned path when `--regenerate-catalog` would clobber concurrent worktree
state. This is **not** a general hand-edit license: any edit to an existing row's cells still
requires the regenerator per item 6, unchanged.

---

## Addendum — 2026-09-03

**Commissioned** this session (`queue-exception: P1 falsifier fired; catalogs are being read as
the work list`). Does **not** amend §2's two-axis split (`hot` = body location; `status` =
disposition), Verdict-wins, C2-joins-to-`hot`, or `--slug` eligibility. Authorizes the
presentation + stamp GO that P1 deferred and that §5 forbade as a silent mass-stamp.

**Cheap falsifier (parent-side, 2026-09-03, before this addendum):**

```
$ rg -c '\| ACTIVE \|' lab/CATALOG.md
# 103
$ rg -n 'class_s_candidate1_scoring|aegis_orbmnq_combined_book|mnq_orb_flow_depth' lab/CATALOG.md
# all three sit in ## Active; first two status=ACTIVE; flow-depth status=HOLD
$ rg -n '^### _inbox' lab/CATALOG.md
# already a cataloged theme — buried last
$ rg -n 'cannot tell .ACTIVE. from' docs/superpowers/plans/2026-08-23-repo-pain-point-packets.md
# P1 falsifier still the live claim
```

P1's README glossary ("these tokens do not mean English") is **falsified** as a repair: a
newcomer still treats `## Active` + 103 `ACTIVE` rows as a work list. Successor is this
addendum, not a reopened P1 packet and not a `LIVE` status token (another glossary row).

**Locks:**

1. **`## Active` → `## Hot bodies`.** Internal table id stays `active`. Parsers accept both
   headings. Hot means "keep the body," not "in flight."
2. **Generated `## In flight` first.** Membership is derived, not "every leftover `ACTIVE`":
   lab slugs in the `STATE.md` operator-queue **Owner artifact** column, lab slugs in
   `docs/briefs/INDEX.md` `## Open` **Home (canonical)** (legacy header `Home` also
   accepted), and any head card (`RESULTS*` / `verdict.md` / `CLOSURE.md` / `README.md`)
   carrying `**In-flight:** yes`. Blocks / Next action / question prose do not name a
   camp. **Exclude `HOLD` and archiveable statuses (`CLOSED` / `FALSIFIED` / `RETIRED` /
   `NULL`).** Not the operator work list (that remains `STATE.md`).
3. **`ACTIVE` is forbidden on a decided campaign.** Stamp `**Verdict:**` as a separate line
   (Verdict-wins already landed). Do not `--slug`. This is the mass-Verdict GO §5 deferred.
4. Regenerator remains the sole CATALOG writer (2026-08-29 single-row exception unchanged).
5. `_inbox` stays a cataloged theme, rendered first under Hot bodies. Outcome-bearing work
   must carry a Verdict and leave `_inbox` before `--slug`. Do not mass-relocate trees.

**Forbidden under this addendum:** a sixth root doc; a `LIVE` token; mass `--slug`; hand-editing
`status`/`hot` cells.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-22 | Initial authoring (`Proposed`) | Cursor Cloud Agent (commission) + Claude Code (draft) |
| 2026-08-22 | Operator `Accepted` + Phase 1 GO (parser / C2 / `hot` column) | Joshua (in-session) + Cursor Cloud Agent |
| 2026-08-22 | Blast-radius parentheticals: Phase 1 landed (this GO); §0/§1 left as defect record | Cursor Cloud Agent |
| 2026-08-29 | Addendum: worktree-isolated single-new-row hand-insert sanctioned as a narrow exception to §2 item 6, distinct from C-P1-10's repaired defect. | Joshua (operator GO, in-session) + Claude Code |
| 2026-09-03 | Addendum: `## Hot bodies` + derived `## In flight`; Verdict-stamp GO on spent `ACTIVE`; P1 glossary falsified. | Cursor Cloud Agent (this commission) |
| 2026-09-03 | In-flight membership also excludes archiveable statuses (Codex P1 on #276). | Cursor Cloud Agent |
| 2026-09-03 | In-flight derivation reads only Owner artifact / Home cells; any head card may stamp `In-flight: yes`; `--slug` refuses `_inbox` (Codex P2 on #276). | Cursor Cloud Agent |
