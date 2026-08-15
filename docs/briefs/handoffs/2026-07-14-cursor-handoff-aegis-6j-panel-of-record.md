# CC Handoff — Aegis→6J panel-of-record resolution + 1R-basis pin (prop-candidate pre-requisite)

**Date:** 2026-07-14
**Parent session:** Claude Code (Fable 5) + Joshua — Q-KBUDGET-1 Phase-1 session
**Spawn target:** Cursor (frozen-spec implementation per [`docs/adr/2026-07-14-cc-cursor-surface-allocation.md`](../../adr/2026-07-14-cc-cursor-surface-allocation.md))
**Repo:** `multi_firm_operations`
**Brief type:** CC handoff (multi-step)
**Parent question:** Q-KBUDGET-1 inventory §6 ask 4 (operator-ordered 2026-07-14); feeds the Class-S candidate pre-registration gated by ADR [`2026-07-14-prop-portfolio-existing-strategy-candidates.md`](../../adr/2026-07-14-prop-portfolio-existing-strategy-candidates.md) (`Proposed`)
**Authority:** Joshua. Parent authored this brief; executor executes. No commit/merge without Joshua's go.
**⚠ Local-machine dependency:** Steps 2.1–2.2 read `c:\Users\joshu\Downloads\*.csv` and gitignored vendor CSVs — a cloud/worktree executor without those bytes must return `NEEDS_CONTEXT` at Phase 0, not improvise.

---

## §0 — Rule 0 reads (PHASE 0 — execute BEFORE any §2 work)

Read each item and report contents in your first response. Do not modify anything until the Phase-0 read-report is delivered and §0.5 ambiguities are resolved.

- [`ops/instruments/6J.md`](../../../ops/instruments/6J.md) — report: J1 row (panel of record), J5 (sizing reality), COST MODEL, ACTIVE/OPEN. Anchor at authoring: `fad8984`.
- [`lab/analysis/c1/tradeify_futures3_bustcut_2026-07-11/RESULTS.md`](../../../lab/analysis/c1/tradeify_futures3_bustcut_2026-07-11/RESULTS.md) + `NOTES.md` + `_diag_aegis_1r.py` — report: the AEGIS INVENTORY block (ae744 vs 5274c), the SENSITIVITY block (pin-fallback artifact), and what `_diag_aegis_1r.py` already measured. Anchor: `eba5030`.
- [`lab/analysis/c1/tradeify_futures3_remc_2026-07-11/run_tradeify_futures3_remc.py`](../../../lab/analysis/c1/tradeify_futures3_remc_2026-07-11/run_tradeify_futures3_remc.py) — report: the input-path block (lines ~50–62) — it reads raw `Downloads\` paths.
- `core/data/tv_exports/cme/SHA256SUMS` + directory listing — report: confirm `Aegis_JPY-Futures_v0.3_PROTOTYPE_(MJY_6J)_CME_6J1!_2026-07-05_8e269.csv` present with sha `c3b34162…801946a6`; confirm ae744 / 5274c / `…MYM…2026-07-11_15d8b.csv` / `…MNQ…2026-07-11_beabf.csv` are ABSENT from the manifest tree (they were at authoring).
- File-presence probe (no content read needed): the four `c:\Users\joshu\Downloads\` CSVs named in the harness paths above — report exists/size/sha256 for each.
- `lab/analysis/aegis/aegis_6j_transfer_2026-07-05/inputs/` listing — report the four BEPAD/PROTOTYPE CSVs present (gitignored lane inputs).
- Vendor-data gate doctrine: `CLAUDE.md` §Vendor-data integrity gate — report the regenerate command sequence (dry-run first; SHA delta in the SAME commit as the data change).

**Citation chain for gitignored inputs (per brief-authoring §0 sub-rule):** the panel-of-record identity claim rests on Tier-1 citations already verified parent-side 2026-07-14 — `6J.md` J1 (n=129 / PF 2.318 / CSV sha `c3b34162…`) and the `SHA256SUMS` line quoted above. If your on-disk reads disagree with either, STOP → `NEEDS_CONTEXT` with the disagreement quoted.

---

## §0.5 — Clarifying questions (HALT-ON-AMBIGUITY required)

- **Data availability:** if any of the four Downloads CSVs no longer exists, return `NEEDS_CONTEXT` naming the missing file(s) — Joshua re-exports or supplies; do NOT substitute a different export.
- **Scope:** "panel of record for prop-candidate use" means the 6J trade-list CSV a *future* candidate pre-registration will cite. It does NOT reopen J1 (the self-funded lane's panel of record stays as 6J.md says).
- **Provenance ambiguity:** "BEPAD-TEST" in the 07-11 filenames vs the CLOSED-FALSIFIED Q-AEGIS-6J-BEPAD-1 experiment — if you cannot determine each file's Pine input set (esp. BE-pad k, account size, max_contracts) from headers/NOTES/CSV internals, say so explicitly in the report; classification then falls to Joshua (who ran the exports), not to inference.

---

## §1 — Context

The prop-portfolio Class-S track (existing-strategy books at the frozen survivor-scoring gate) is blocked on a data defect: the 2026-07-11 Tradeify runs consumed **two materially different Aegis 6J CSVs** (ae744: PF 2.042 / exit-qty mean 11.36 vs 5274c: PF 2.212 / exit-qty mean 7.29 / net Δ −$21.7K, same N=152/WR/span) read from **raw Downloads paths**, bypassing the manifest-governed vendor tree; and 5274c triggered the known 1R median-fallback trap (0 full-stops after decompound → 1R $166.56 → spurious 9× scale). No Aegis-bearing candidate can pre-register until exactly one of-record 6J panel + a pinned 1R basis exists.

**What the executor produces:**
- `lab/analysis/aegis/aegis_6j_transfer_2026-07-05/PANEL_OF_RECORD.md` — a decision table (§2.3) for Joshua's pick; NOT a unilateral pick.
- The 07-11 CSVs copied into `core/data/tv_exports/cme/` + regenerated `SHA256SUMS` in the same commit (§2.2) — preserving the evidence regardless of which panel is picked.
- A reported (not landed) guard proposal for the 1R fallback trap in the prop-scoring path (§2.4).

**What the executor is NOT asked to do:** no Pine edits; no re-export; no scoring/MC runs; no edits to `6J.md` J1; no candidate pre-registration; no changes to `lab/discovery/` code (§2.4 is report-only).

---

## §2 — Execution plan

### Step 2.1 — Inventory + diff diagnosis (ae744 vs 5274c vs pinned 8e269)

- **Inputs:** the four Downloads CSVs (if present), `inputs/` lane CSVs, the pinned `…_8e269.csv`, `_diag_aegis_1r.py`.
- **Action:** extend/run the existing diag: per-file — N, PF, WR, net@static-basis, exit-qty distribution, loss cohort (|loss| buckets), first/last stamps, and any header/metadata rows identifying Pine inputs. Difference hypothesis to test mechanically: the two 07-11 files differ in **sizing inputs** (account size / max_contracts / risk basis), not in signal set (same N, same WR ⇒ same entries).
- **Expected output:** a diff table + one-paragraph classification per file (which Pine configuration each plausibly is; UNKNOWN is acceptable, flagged per §0.5).
- **Per-step gate:** every number in the bustcut AEGIS INVENTORY block reproduces from bytes; otherwise `DONE_WITH_CONCERNS` with the delta quoted.

### Step 2.2 — Manifest-tree repair (Downloads → vendor tree)

- **Inputs:** the four 07-11 Downloads CSVs (Aegis ae744, Aegis 5274c, MYM 15d8b, MNQ beabf).
- **Action:** copy into `core/data/tv_exports/cme/` (naming unchanged); `python scripts/check_data_manifests.py --regenerate --dry-run` → review → `--regenerate`; stage the `SHA256SUMS` delta **in the same commit** as the copies. Per the standing Downloads→copy workflow; all six manifest dirs must be present locally first (CLAUDE.md gate) — if any is missing, `NEEDS_CONTEXT`.
- **Expected output:** 4 files + manifest delta, one commit (no other changes in it).
- **Per-step gate:** `python scripts/check_data_manifests.py` exits clean post-commit.

### Step 2.3 — PANEL_OF_RECORD.md decision table

- **Inputs:** 2.1 output + 6J.md J1/J5 + the bustcut SENSITIVITY block.
- **Action:** author the decision table: rows = {pinned 8e269 (J1), ae744, 5274c}; columns = {provenance/Pine-config (or UNKNOWN), N/PF/net, 1R by `full_stop_mean` (report n of the cohort; state explicitly whether the n<5 median fallback WOULD fire), suitability caveats}. End with a **recommendation line + explicit "operator picks"** — the pick is Joshua's, recorded by him in the file.
- **Expected output:** `lab/analysis/aegis/aegis_6j_transfer_2026-07-05/PANEL_OF_RECORD.md`.
- **Per-step gate:** every 1R figure carries its cohort n (metric-cohort binding); no figure without a reproducible command.

### Step 2.4 — 1R fallback-guard proposal (REPORT-ONLY)

- **Inputs:** the 1R pin call chain as actually implemented — locate where `pin_r_basis`/`implied_1r` threads into the prop-scoring path (`lab/discovery/prop_survivor_scoring.py` and whatever it imports; read, do not edit).
- **Action:** report the exact call chain + whether the n<5 median fallback can fire silently there; propose (as a diff-shaped suggestion in the report, NOT landed) a hard-fail assertion for candidate-scoring runs.
- **Expected output:** a §"Guard proposal" section in PANEL_OF_RECORD.md.
- **Per-step gate:** the chain is quoted from read code (file:line), not inferred.

### Step 2.5 — Closure report

Per §6 taxonomy. Diff list must be exactly: 4 copied CSVs + `SHA256SUMS` + `PANEL_OF_RECORD.md`.

---

## §4 — Falsifiable hypothesis

`N/A — executing ordered mechanicals (Q-KBUDGET-1 inventory §6 ask 4); no hypothesis under test.` The one testable sub-claim (2.1: the ae744↔5274c delta is sizing-borne, not signal-borne) is reported as CONFIRMED / REFUTED / UNDETERMINED inside 2.1's output; it gates nothing beyond its own row in the decision table.

---

## §5 — Forbidden moves

- **Picking the panel of record yourself.** The decision table ends at a recommendation; the pick is Joshua's (it anchors every future Aegis-bearing candidate).
- **Editing `6J.md` J1 or re-pinning any Pine hash** — J1 is the self-funded lane's panel of record and is not in question here.
- **Landing the 2.4 guard "while you're in there"** — `lab/discovery/` is the frozen scoring harness; a code change there needs its own reviewed handoff.
- **Substituting a fresh TV export for a missing Downloads file** — provenance is the whole point; `NEEDS_CONTEXT` instead.
- **Committing CSVs without the same-commit manifest delta** — the vendor-data integrity gate is load-bearing (M-9); `--no-verify` is not the standing path.

---

## §6 — Gate + status return taxonomy

| Status | Meaning | Parent action |
|---|---|---|
| `DONE` | All steps green; diff list exact | Parent review §7, then Joshua picks the panel |
| `DONE_WITH_CONCERNS` | Completed; classification UNKNOWN somewhere or a number failed to reproduce | Parent adjudicates before the pick |
| `NEEDS_CONTEXT` | Missing Downloads file(s) / manifest dir / unreadable input | Joshua supplies; re-dispatch |
| `BLOCKED — <sub-case>` | Structural obstruction | Escalate per sub-case |

**`BLOCKED` sub-cases (mandatory):** `BLOCKED — context-problem` (re-dispatch with more context) · `BLOCKED — capability-problem` (re-dispatch with a stronger model or escalate to Joshua) · `BLOCKED — scope-problem` (decompose into smaller tasks) · `BLOCKED — plan-itself-wrong` (escalate to parent; the §2 plan is structurally broken — do not amend it in place).

Closure report format: per the standard four-state block (Status / per-step gates / diffs / artifact path / concerns / next action).

---

## §7 — Parent-session review (after return)

Pass 1 — spec compliance: diff list exactly §2.5's; no scoring runs; no `lab/discovery/` edits; PANEL_OF_RECORD.md ends with "operator picks". Pass 2 — quality: bustcut numbers reproduce; every 1R carries cohort n; manifest check exits clean. Pass 3 — consolidated read across the data commit + the report.

---

## §10 — Audit hooks (runnable)

```bash
# Manifest tree now carries the 07-11 inputs (post-2.2)
grep -c "2026-07-11" core/data/tv_exports/cme/SHA256SUMS       # expect >= 4
python scripts/check_data_manifests.py                          # expect clean

# Decision table exists and defers the pick
grep -n "operator picks" lab/analysis/aegis/aegis_6j_transfer_2026-07-05/PANEL_OF_RECORD.md

# No lab/discovery edits slipped in
git diff <pre-spawn-commit>..HEAD --name-only -- lab/discovery/  # expect empty

# J1 untouched
git diff <pre-spawn-commit>..HEAD -- ops/instruments/6J.md       # expect empty
```

---

## Verification (parent-side, before dispatch)

```bash
PYTHONIOENCODING=utf-8 python "C:\Users\joshu\.claude\skills\brief-authoring\scripts\check_brief.py" \
  docs/briefs/handoffs/2026-07-14-cursor-handoff-aegis-6j-panel-of-record.md --type cc_handoff
# Expected: PASS

# §0 anchors current at dispatch
git log -1 --format='%h' -- ops/instruments/6J.md                                          # fad8984 (or later — re-read if later)
git log -1 --format='%h' -- lab/analysis/c1/tradeify_futures3_bustcut_2026-07-11/RESULTS.md   # eba5030
grep -c "c3b34162" core/data/tv_exports/cme/SHA256SUMS                                     # expect 1
```
