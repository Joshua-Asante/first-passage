# Cursor Handoff — dead-surface retirements (Copygram validator estate + 4 orphans + codification bridge + notion-skill move)

**Date:** 2026-07-24
**Parent session:** Claude Code operator session — Algorithm repo review (umbrella: `docs/notes/2026-07-24-algorithm-repo-review-handoff-series.md`).
**Spawn target:** Cursor
**Repo:** `multi_firm_operations`
**Brief type:** Cursor handoff (multi-step)
**Parent question:** N/A — executes an operator-authorized Delete slate.
**Authority:** Joshua (CEO). **DO NOT DISPATCH UNTIL THE OPERATOR RECORDS GO ON THIS BRIEF** — deletions are user-gated (INQHIORI: the gate is user-gated at D). On GO, the frozen scope below executes verbatim; no commit/merge without Joshua's go.
**Dispatch order:** after briefs #1–#3 land (the extended `check_skill_refs` gate from #3 then verifies no skill cites the deleted paths).

**OPERATOR GO LINE (fill before dispatch):** `GO recorded: 2026-08-02 (JA)` — **PARTIAL, scoped to item 1 only** (PR #612 / Copygram estate).

> **Scope of this GO (recorded 2026-08-02, operator chat: *"fill the GO line and merge it"*, said of PR #612).**
> **AUTHORIZED:** the Copygram-era **alert-validator estate** — `core/config/symbol_inventory.toml` ·
> `scripts/validate_alert_payloads.py` · `tests/test_validate_alert_payloads.py`, plus the registry-row
> updates and the frozen ADR addendum that ship with them. That is the whole of PR #612.
> **NOT AUTHORIZED *at the time this entry was written* — ⚠ SUPERSEDED SAME DAY by GO (2) below,
> which authorizes all four. Retained unedited as the record of what GO (1) did and did not cover:**
> `scripts/inactivity_simulator.py` ·
> `scripts/migrate_adr_headers_m1.py` · the `mc-anchors` command · the GBPUSD RUNBOOKs (incl. the §5(A)
> evidence-JSON sub-decision). The operator approved a PR, not the residual slate; reading one merge as
> blanket authority over four unexecuted deletions would over-record the GO. Each remaining item needs
> its own GO line entry — append here, do not edit this one.
> (The two pre-authorized items below — `lab/codification/`, `notion-mcp-api-patterns` — are unaffected
> and retain their standing 2026-07-24 GO.)

**GO (2) — remaining four items:** `GO recorded: 2026-08-02 (JA)` — operator chat, *"fill the GO line
for the remaining four items"*. **The slate's GO line is now fully satisfied.** Execution vehicle: prune brief Packet D / PR #614 (`cursor/prune-packets-a-e-mission-alignment`), including standing pre-authorized `lab/codification/` + repo `notion-mcp-api-patterns` removals.

> **AUTHORIZED by this entry:** `scripts/inactivity_simulator.py` · `scripts/migrate_adr_headers_m1.py` ·
> `.claude/commands/mc-anchors.md` · the two GBPUSD RUNBOOKs
> (`…/matched_pep_2026/RANK_RHO_RUNBOOK.md`, `…/full_2018_2024/RANK_CERT_RUNBOOK.md`).
> Plus the §2.3 registry-row updates that must ship in the same commit.
>
> **§0.5 clarifying questions — resolved by this GO note (it governs, per §0.5(A)):**
> - **(A) GBPUSD evidence JSONs — recommended default ADOPTED.** Delete **only** the two
>   `RUNBOOK.md` files. `py_scores.json` + `rank_cert_verdict.json` **STAY** — evidence of the 1/12
>   PENDING terminal state.
> - **(B) `core/` prose comment — LEAVE untouched**, per the recommended default (core edits route to
>   CC under ADR test 1). ⚠ **Brief premise corrected:** §0.5(B) names *two* mentions; only **one**
>   survives — `core/mc/preflight.py:18`. The `core/firm_rules.py:19` mention is **gone** (substrate
>   Phase 4, `fc14682`). Do not go looking for it.
> - **(C) `check_boundaries.py` layer-table rows — DELETE in the same commit**, gate on
>   `python scripts/check_boundaries.py` green.
>
> **Phase-0 sweeps re-run 2026-08-02 at `aca9ed1`, all four clear** (recorded so this GO rests on
> evidence, not on the 07-24 read alone):
> - `inactivity_simulator` — no executable consumer. `tests/core/test_inactivity_boundary.py` was
>   **re-pointed 2026-05-16** and imports `portfolio_mc` (`from portfolio_mc import …`, line 22); its
>   mention of the script is a historical comment. Remaining hits are the `core/` prose line (B) and
>   the `check_boundaries` row (C).
> - `migrate_adr_headers_m1` — **zero** `.py` consumers; `check_adr_graph.py` does **not** import the
>   migrator, so the dependency runs migrator→checker only and deleting the migrator cannot break the
>   gate.
> - `mc-anchors` — confirmed hard-dead: `core/mc/modes.py:108` has `PANELS_BY_BROKER = {}`, and the
>   command's step-1 panel run exits with *"portfolio_mc CLI: no registered broker panel"*.
> - GBPUSD RUNBOOKs — both tracked and present; the two evidence JSONs sit in `full_2018_2024/` and
>   are untouched by (A).
>
> ⚠ **One consequence of (A) worth seeing before it happens:** `matched_pep_2026/` contains
> **exactly one tracked file** — the RUNBOOK being deleted — so that directory disappears entirely
> and the rank-rho arm's record becomes git-history-only. `full_2018_2024/` is unaffected (it keeps
> both JSONs). This does not change the ruling — the brief classifies both RUNBOOKs as paste-into-TV
> work instructions, not results — but the asymmetry between the two arms is real and is recorded
> here rather than discovered afterwards.
>
> **Still NOT authorized by either GO entry:** widening the slate. §5's forbidden move stands —
> *"one candidate, one review, one GO"*. A newly-noticed dead file needs a fresh entry here.

> **Pre-authorized items (2026-07-24, operator chat — Algorithm-review rulings #3 and #4):** the `lab/codification/` bridge retirement ("retire the bridge") and the `notion-mcp-api-patterns` repo-skill removal ("move out of the repo skill set" — user-level copy preserved at `C:/Users/joshu/.claude/skills/notion-mcp-api-patterns/` 2026-07-24) carry standing GO already. The GO line above still gates the ORIGINAL five-item slate; if it stays unfilled, dispatch may proceed on the two pre-authorized items alone (drop the others from §2 in that case and say so in the closure report).

---

## Routing-test self-check (per `docs/adr/2026-07-14-cc-cursor-surface-allocation.md`)

- **Test 0:** no vendor bytes, no secrets. Cloud or local eligible (all targets are tracked files).
- **Test 1:** No locked surface. Targets: `core/config/symbol_inventory.toml` (config data — NOT in the ADR's enumerated anchor set: dd_protection/firm_rules/portfolio_mc/core-mc/lifecycle/dd_geometry/Pine), two tracked `.md` runbooks under `core/data/tv_exports/candidates/`, three `scripts/` files, one test file, one `.claude/commands/` file, plus mechanical row updates in `REPO_MAP.md`, `PIPELINES.md`, `scripts/check_boundaries.py`'s scripts-layer table, and a pre-drafted FROZEN ADR addendum applied verbatim (authored parent-side; applying frozen text is not doctrine authoring).
- **Test 2:** Yes — file list closed, addendum text frozen, doc-row edits enumerated by Phase-0 grep.
- **Test 3:** Clears (~10 files).

---

## §0 — Rule 0 reads (PHASE 0 — read-report before any deletion)

Anchors verified at `33356ea` (2026-07-24). Report each; `NEEDS_CONTEXT` on contradiction.

- **Consumer sweeps (re-run each, report hit lists):**
  ```bash
  rg --no-ignore -l "symbol_inventory|validate_alert" --type py
  rg --no-ignore -l "inactivity_simulator" --type py
  rg --no-ignore -l "migrate_adr_headers" --type py
  rg -n "validate_alert|inactivity_simulator|migrate_adr_headers" Makefile scripts/githooks/ .github/
  ```
  Expected (parent-verified): the only `.py` hits are the target files themselves plus prose/registry rows (`core/mc/preflight.py:18` and `core/firm_rules.py:19` comments; `scripts/check_boundaries.py` layer table); zero Makefile/hook/CI wiring. ANY new executable consumer → `NEEDS_CONTEXT`.
- `scripts/validate_alert_payloads.py` (309 lines) + `core/config/symbol_inventory.toml` + `tests/test_validate_alert_payloads.py` — confirm the validator targets the TV→Copygram→DXTrade alert contract (read its docstring) and that `ops/c1_rail/crosstrade_payload.py` (the c1 payload builder) imports none of it.
- `scripts/inactivity_simulator.py` (175 lines) — confirm it is the Q-MCTO-1 Phase-1 shadow of FXIFY inactivity semantics and that production `bust_inactivity` lives in `core/mc/simulation.py` (~lines 149/194); confirm `tests/core/test_inactivity_boundary.py` imports `portfolio_mc`, not this script.
- `scripts/migrate_adr_headers_m1.py` (574 lines) — confirm `scripts/check_adr_graph.py` enforces the header grammar independently (the migrator imports FROM it, never the reverse) and nothing re-runs the migrator.
- `.claude/commands/mc-anchors.md` — confirm its step 1 invokes a `portfolio_mc` panel run and `core/mc/modes.py` (~lines 96–98, 1400–1408) shows `PANELS_BY_BROKER` empty + unconditional `SystemExit` at CLI entry (post-substrate-Phase-3).
- `core/data/tv_exports/candidates/concept-gbpusd-vbr-001/matched_pep_2026/RANK_RHO_RUNBOOK.md` + `.../full_2018_2024/RANK_CERT_RUNBOOK.md` — confirm both are paste-into-TV work instructions (not results); the sibling `py_scores.json` + `rank_cert_verdict.json` are EVIDENCE and stay.
- `REPO_MAP.md` §2.1 + `PIPELINES.md` + `scripts/check_boundaries.py` — `rg -n "validate_alert_payloads|inactivity_simulator|migrate_adr_headers|mc-anchors" REPO_MAP.md PIPELINES.md scripts/check_boundaries.py` — report every row that must be updated in the same commit.
- `docs/adr/2026-07-11-fxify-ops-surface-retirement.md` — read §Decision + current end-of-file, so the addendum in §2.2 lands in the right place; confirm the ADR nowhere mentions `validate_alert_payloads`/`symbol_inventory` (the estate it missed).
- **Codification bridge (ruling #3):** `git ls-files lab/codification/` (expect 12 files incl. `tests/`); `rg --no-ignore -l "from codification|import codification|codification\." --type py`. **Parent-verified 2026-07-24 — the importer list is NOT empty, and that is expected:** besides `lab/codification/` itself, the hits are `lab/archive/gbpusd_rank_cert/rank_cert.py` (archived) and **five files under `lab/analysis/legacy/usoil_regime_capture/`** (`gate_b0_parity`, `gate_b_deflation_preview`, `gate_b_full_advisory`, `gate_b_grid_preview`, `reconcile_b0`). That study sits on this brief's §5 keep-list (PARKED, 2026-08-08 Q-USOIL-1 revisit) — **but it is already non-runnable independent of the bridge**: the same files also import `validation.sweep` / `validation.dsr` / `validation.cpcv`, and `lab/validation/` has **zero tracked files** (retired 2026-07-11). Deleting the bridge therefore adds a second broken import to files that already cannot execute, and any 08-08 USOIL revisit needs a `git`-restore of Gen-1 `validation/` regardless. **Do not treat these five as live consumers, do not edit them, and do not let them block the delete** — list them in the closure report so the 08-08 revisit knows both packages are gone. Read `PIPELINES.md` rows: line ~14 (P2 inventory row "PARKED (inert, import-severed)"), line ~100 (the park block with "Do **not** delete (rebuild-at-the-wrong-time hazard)" — SUPERSEDED by ruling #3), line ~192 ("One parked (P2 codification, trigger-armed)"); `REPO_MAP.md` lines ~57 (lab/codification row), ~110+118 (PYTHONPATH examples using `codification`), ~148 (seam-disposition row). Also `docs/notes/2026-06-06-codifier-signal-fn-bridge-sketch.md` — cited BY `lab/codification/compose.py`; once the bridge is deleted that note loses its live consumer (roll it in the same PR or flag for brief #5).
- **Notion skill (ruling #4):** `git ls-files .claude/skills/notion-mcp-api-patterns/` (expect 1 file, SKILL.md); confirm the user-level copy exists at `C:/Users/joshu/.claude/skills/notion-mcp-api-patterns/SKILL.md` (preserved 2026-07-24 — if ABSENT, `NEEDS_CONTEXT`, do not delete without the copy). The two read-only `notion-*` MCP allows in `.claude/settings.json` STAY (operator personal use).

---

## §0.5 — Clarifying questions (Cursor variant — parent-recommended defaults)

- **(A) The GBPUSD evidence JSONs.** **Recommended default:** delete ONLY the two RUNBOOK.md files; `py_scores.json` + `rank_cert_verdict.json` stay (evidence of the 1/12 PENDING terminal state). If the operator's GO note says otherwise, follow the GO note.
- **(B) Prose mentions in `core/mc/preflight.py:18` / `core/firm_rules.py:19`.** **Recommended default:** LEAVE those comment lines untouched — they are `core/` files (ADR test 1: any core anchor edit routes to CC), and a stale comment naming a deleted script is historical prose, not a live reference. Report them as §6 concerns for the CC-routed core-prune brief.
- **(C) `check_boundaries.py` scripts-layer table rows.** **Recommended default:** delete the table rows for the removed scripts in the same commit (the scanner's source-of-truth mapping must not name nonexistent files); run `python scripts/check_boundaries.py` green as the gate.

---

## §1 — Context

The Algorithm review's adversarial cross-check confirmed five artifacts that serve none of R1–R5 (c1 rail / venue-native research / governance / historical record / locked-book protection), have zero executable consumers, and are owned by NO standing ADR, forward-board line, or operator directive: the Copygram-era alert-validator estate fell through the cracks between the 2026-07-11 retirement ADRs and the 2026-07-22 substrate ADR; the other four are spent one-shots (superseded shadow simulator, completed migrator, hard-failing command, stranded cert runbooks). Deliberately-retained lookalikes are OUT of scope and named in §5.

**Deliverable:** one `cursor/*` PR: `git rm` of the slate, same-commit doc-row updates, the frozen ADR addendum, green gates.
**NOT asked:** touching `lab/analysis/time_to_pass.py`, `scripts/mc_user_guardian.py`, `core/dd_geometry.py`, the tearsheet chain, anything under `core/mc/`, or any CFD vendor data (T1-blocked class).

---

## §2 — Execution plan

### Step 2.1 — Delete slate

- **Action:**
  ```bash
  git rm core/config/symbol_inventory.toml scripts/validate_alert_payloads.py tests/test_validate_alert_payloads.py
  git rm scripts/inactivity_simulator.py scripts/migrate_adr_headers_m1.py .claude/commands/mc-anchors.md
  git rm "core/data/tv_exports/candidates/concept-gbpusd-vbr-001/matched_pep_2026/RANK_RHO_RUNBOOK.md"
  git rm "core/data/tv_exports/candidates/concept-gbpusd-vbr-001/full_2018_2024/RANK_CERT_RUNBOOK.md"
  git rm -r lab/codification/                       # ruling #3 (pre-authorized 2026-07-24)
  git rm -r .claude/skills/notion-mcp-api-patterns/ # ruling #4 (pre-authorized; user-level copy verified in Phase 0)
  ```
- **Per-step gate:** `pytest tests/ -q` green (the deleted test file's suite goes with it; zero other failures); `python scripts/check_boundaries.py` green after Step 2.2's row updates.

### Step 2.2 — Same-commit doc/registry updates

- **Action:** apply every row update the Phase-0 grep enumerated in `REPO_MAP.md` §2.1, `PIPELINES.md`, `scripts/check_boundaries.py` (strike-through-with-retirement-pointer style for REPO_MAP rows, matching the file's existing convention for retired scripts; plain row deletion in check_boundaries' mapping). For the codification bridge: PIPELINES P2 inventory row + line-100 park block + line-192 summary flip from PARKED to **RETIRED 2026-07-24 (operator ruling #3 — the 2026-07-11 "do not delete" park is superseded; retrieve via git history; a future Python→Pine bridge is a fresh build)**; REPO_MAP lines ~57/~118/~148 get the same retirement-pointer treatment (keep the `from codification import emit` phrase at line ~110 only if rewording, it is an illustrative example — replace with a live module example, e.g. `from research_utils import breadth`).
- **Per-step gate:** `rg -n "validate_alert_payloads|inactivity_simulator|migrate_adr_headers|mc-anchors" REPO_MAP.md PIPELINES.md scripts/check_boundaries.py Makefile .github/` → hits only in retirement-pointer prose.

### Step 2.3 — Frozen ADR addendum (apply VERBATIM to `docs/adr/2026-07-11-fxify-ops-surface-retirement.md`, end of file)

> ## Addendum (2026-07-24) — Copygram alert-validator estate retired; orphan one-shots pruned
>
> The 2026-07-24 Algorithm repo review (14-agent adversarial survey;
> `docs/notes/2026-07-24-algorithm-repo-review-handoff-series.md`) found the
> TV->Copygram->DXTrade alert-validation estate — `core/config/symbol_inventory.toml`
> + `scripts/validate_alert_payloads.py` + `tests/test_validate_alert_payloads.py` —
> survived both this ADR and the 2026-07-22 substrate ADR unenumerated: a
> fail-closed gate for a rail closed 2026-07-10, with zero executable consumers
> (the c1 rail's `ops/c1_rail/crosstrade_payload.py` never imported it). Deleted on
> operator GO recorded in the handoff brief
> `docs/briefs/handoffs/2026-07-24-cursor-handoff-dead-surface-retirements.md`.
> The same GO pruned four unowned spent one-shots: `scripts/inactivity_simulator.py`
> (Q-MCTO-1 shadow, superseded into `core/mc/simulation.py` 2026-05-16),
> `scripts/migrate_adr_headers_m1.py` (migration complete; `check_adr_graph.py`
> is the durable gate), `.claude/commands/mc-anchors.md` (hard-fails
> post-substrate-Phase-3), and the two GBPUSD-VBR cert RUNBOOK work-instruction
> files (cert permanently 1/12 PENDING; evidence JSONs retained). Bytes remain
> in git history; restore requires a fresh decision, not a revert.

- **Per-step gate:** addendum applied byte-verbatim; `python scripts/check_adr_graph.py` (if wired) green.

### Step 2.3b — Frozen ADR addendum (apply VERBATIM to `docs/adr/2026-07-11-gen1-pipeline-retirement.md`, end of file, before its Change history if the file convention places addenda there)

> ## Addendum (2026-07-24, operator ruling) — parked codification bridge RETIRED
>
> The Gen-1 retirement parked `lab/codification/` ("inert, import-severed") with a
> re-point trigger of "first DISC-CAMP survivor reaches admission" and a do-not-delete
> note. The trigger's premise did not survive contact: the first admitted candidate
> (ORB-MNQ, lifecycle CANDIDATE 2026-07-16) arrived via the Class-S / venue-native
> route with no DISC-CAMP composer step, and the bridge's input format (concept-YAML)
> was already wrong for any current pipeline. On 2026-07-24 the operator ruled
> "retire the bridge" (Algorithm repo review ruling #3 —
> `docs/notes/2026-07-24-algorithm-repo-review-handoff-series.md`). `lab/codification/`
> (12 files) is deleted; bytes remain in git history; a future Python→Pine bridge is a
> fresh build against the then-current survivor format, not a restore.

- **Per-step gate:** addendum byte-verbatim; `python scripts/check_boundaries.py` green post-delete.

### Step 2.4 — Closure

Report per §6. PR body: the delete list, the doc-row diff summary, and the sentence "No deliberately-retained lookalike (§5 list) was touched."

---

## §4 — Falsifiable hypothesis

**H (premise, not an investigation):** every slate item has zero executable consumers and no owning obligation. **Falsified if** any Phase-0 sweep surfaces a live consumer or an owning ADR/board line — that item leaves the slate and the discrepancy bounces `NEEDS_CONTEXT`; the rest of the slate proceeds only on parent confirmation.

---

## §5 — Forbidden moves

- **Deleting the deliberately-retained lookalikes** (each was a review candidate KILLED by cross-check): `lab/analysis/time_to_pass.py` (STATE.md: "Harness retained on disk; do not schedule"), `scripts/mc_user_guardian.py` (2026-07-22 condition-4 disposition: "BANNER-MARKED, kept"), `core/dd_geometry.py` + its test (substrate ADR Phase-1 explicit retention), the tearsheet chain (`ops/cli.py`/`core/csv_parser.py`/`core/lib/tearsheet.py` — ADR §2-D retention with its own disposal condition), `lab/analysis/legacy/usoil_regime_capture/` (PARKED, 08-08 revisit).
- **Touching gitignored CFD vendor data** — class-wide delete is trigger-dated + BLOCKED on T1 (`docs/notes/notice/N-2026-07-17-cfd-data-estate-trigger-dated-disposition.md`).
- **Editing `core/mc/preflight.py` / `core/firm_rules.py` comment lines** (§0.5(B)) — core files route to CC.
- **Widening the slate** ("this other script also looks dead") — one candidate, one review, one GO. Log as §6 concern.
- **Dispatching without the operator GO line filled.**

---

## §6 — Gate + status return

Report EXACTLY one of `DONE` / `DONE_WITH_CONCERNS` / `NEEDS_CONTEXT` / `BLOCKED — <sub-case>` per `references/cc_handoff.md` §6, with the standard closure-report format (status, per-step gates, diff list, concerns, next action). This handoff produces no investigation verdict (no RESOLVED / FALSIFIED / AMBIGUOUS claim) — the four-state return plus the per-step gates is the entire closure.

---

## §7 — Parent-session review (after return)

Pass 1: diff = exactly the 8 deletions + the enumerated doc/registry files + the ADR addendum. Pass 2: addendum byte-verbatim; full `pytest` + `make check` green; §5 lookalikes untouched (`git log --stat` scan). Pass 3: read REPO_MAP/PIPELINES/check_boundaries diffs together — the three registries must agree on what exists.

---

## §10 — Audit hooks (runnable)

```bash
git ls-files core/config/symbol_inventory.toml scripts/validate_alert_payloads.py \
  scripts/inactivity_simulator.py scripts/migrate_adr_headers_m1.py .claude/commands/mc-anchors.md
# Expected: empty.
git ls-files lab/analysis/time_to_pass.py scripts/mc_user_guardian.py core/dd_geometry.py
# Expected: all three still present (retained lookalikes).
grep -n "Addendum (2026-07-24)" docs/adr/2026-07-11-fxify-ops-surface-retirement.md docs/adr/2026-07-11-gen1-pipeline-retirement.md
# Expected: 1 hit each.
git ls-files lab/codification/ .claude/skills/notion-mcp-api-patterns/
# Expected: empty.
ls "C:/Users/joshu/.claude/skills/notion-mcp-api-patterns/SKILL.md"
# Expected: present (user-level copy preserved).
```

---

## Verification (parent-side)

```bash
python scripts/check_brief.py docs/briefs/handoffs/2026-07-24-cursor-handoff-dead-surface-retirements.md
grep -n "GO recorded" docs/briefs/handoffs/2026-07-24-cursor-handoff-dead-surface-retirements.md  # must be filled before dispatch
```
