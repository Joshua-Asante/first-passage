# CC Handoff — ORB + Aegis third-leg research, Experiment 1: pair-baseline readiness

**Must run locally** — reads the operator's local ORB/Aegis diagnostic and the accepted book's private read surface in place in the primary checkout (AGENTS.md §Public-clone posture); neither exists in a cloud clone.

**Date:** 2026-10-29
**Status:** DRAFT — not admitted, not frozen, not dispatched. Joshua asked for this draft only; admission items A1–A3 (§0.5) are his.
**Parent session:** Claude cloud session 2026-10-29, reviewing Codex's eight-experiment third-leg decomposition (Experiment 1 extended with existing-leg comparison arms and native feasibility).
**Spawn target:** Claude Code, `local`. Not Codex: the reads include a private diagnostic and the private read surface, which Codex may not receive (AGENTS.md §Data movement).
**Repo:** `first-passage`; base `origin/main` = `0d8e72b141a6f87a12e7d13f7d151eb44c0964cc` at drafting. Refresh at dispatch.
**Brief type:** CC handoff (multi-step)
**Parent question:** `N/A` — no owning record yet; A1 asks Joshua to name it.
**Authority:** Joshua (operator). The worker may commit and push its own `claude/` branch and open one PR (operator ruling 2026-10-24). Merge follows Rule 6. `DONE` grants nothing further.

**Question:** Can the intended ORB + Aegis pair be measured faithfully with existing evidence, together with the two existing-leg comparison arms, and could each leg run natively on a Tradeify 50K or 100K account?
**Decision changed:** Whether Experiment 2 (pair-only weakness map with Vanguard and Striker arms) can be dispatched as is, or which named blockers must clear first.
**Budget (Rule 2):** One inventory pass, one consistency check, at most one focused correction; at most two review rounds. $0, K = 0, no runs. Overrun → `BLOCKED — scope-problem`, not a third pass.

---

## §0 — Rule 0 reads (PHASE 0 — execute BEFORE any §2 work)

Report for each read: commit anchor (`git log -1 --format='%h %ad' --date=short -- <path>`), and the finding named. Anchors below were confirmed at drafting on 2026-10-29.

| Read | Anchor at drafting | Report |
|---|---|---|
| `STATE.md` (queue item 1; decision index 10-19, 10-28) | `2701796` 2026-10-29 | Current standing of the ORB/Aegis shared native account and the "no evidence case" ruling |
| `docs/superpowers/specs/2026-10-28-orb-aegis-workshop-design.md` (§Evidence and ownership boundary; §Adaptive exploration and confirmation) | `d6a4780` 2026-10-28 | The three ORB identities that must not be conflated; exposure-inventory rule |
| `lab/analysis/c1/strategy_data_inventory_2026-10/INVENTORY.md` | `631f6b6` 2026-10-28 | The existing 51-row dataset × study inventory. **This card extends it; it does not redo it** |
| `core/strategies/BOOK_SOURCES.sha256` | `5516554` 2026-10-09 | Accepted pins: ORB v7 reconstruction, Aegis 6J1, Vanguard MGC v0.4, Striker DJ30 pyramid-250 (hashes only) |
| `docs/briefs/pre-registration/2026-10-26-tradeify-native-lane-prereg-DRAFT.md` (§11 item 2) | `9e86312` 2026-10-29 | The open 100K-versus-50K choice and the candidate editions it binds |
| `docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md` (addenda 10-16, 10-19, 10-28) | `5c5bd54` 2026-10-29 | Native-only rule; ORB/Aegis shared account needs its own evidence case |
| `core/firm_rules.py` (`Tradeify_Select_50K`, `Tradeify_Select_100K` rows, line ~490) | `6f59f50` 2026-10-12 | Starting balance, drawdown and micro cap per tier — identities, not sizing |
| `lab/analysis/c1/aegis_orbmnq_combined_book_2026-08-26/RESULTS.md` | `5516554` 2026-10-09 | Prior pair study: verdict FALSIFIED; editions (ORB-MNQ-1 v6, Aegis v3) |
| `lab/analysis/c1/tradeify_book_composition_2026-09/THIRD_LEG_MINIMUM.md`, `MOC_FADE_REPLAY.md`, `README.md` | `5516554` 2026-10-09 | Prior synthetic third-leg shape sweep beside MNQ×1 + Aegis×2 and the one real candidate tested |
| `docs/rejected_candidates.md` | `a852cc3` 2026-10-25 | Rejections touching continuation, failed-break and settlement mechanisms |
| `core/data/tv_exports/cme/SHA256SUMS` | `5516554` 2026-10-09 | Which canonical bar panels exist (MNQ, MYM, M2K, MGC, MCL; no 6J/MJY bar panel listed) |
| Operator-local Codex diagnostic `local_artifacts/orb-aegis-diagnostic-20261029/REPORT.md` (operator's checkout) | not in git | SHA-256, inputs, editions, account configuration and windows. Read in place only; quote no figures |

After Phase 0, post the read-report and the paste-search output (Rule 8) of:

```bash
grep -n -i -E "third.leg|pair.only|orb.?aegis|complement" lab/CATALOG.md docs/briefs/INDEX.md
python -I scripts/check_advisor_dedup.py --keywords "third leg ORB Aegis pair baseline"
```

---

## §0.75 — Local-only dependency check (required for every dispatch)

- **Gitignored vendor data:** yes — Step 2.3 reads `core/data/tv_exports/cme/` and `core/data/bar_data/` presence and hashes. `NOT confirmed` for any cloud environment → route local. The worker confirms presence by `sha256sum -c` against `SHA256SUMS` in the operator's checkout.
- **Private read surface / private artifact:** yes — the diagnostic and the `BOOK_SOURCES.sha256` sources are read in place in the operator's primary checkout. Never copied into the worktree.
- **Secrets/API keys:** none needed.

---

## §0.5 — Clarifying questions (HALT-ON-AMBIGUITY required)

**Admission — Joshua, before freeze:**

- **A1 Owner and decision.** Which record owns third-leg research, and which decision does it feed (the 11-08 sitting, the native-lane pre-registration's account choice, or the self-funded lane)? **Recommended default:** a new campaign-plan entry under the native-lane owner. The decision fed: whether a third leg beside the shared native ORB/Aegis account is worth a research campaign. The §5.1 `parent` is a placeholder pending this answer.
- **A2 Diagnostic read.** Grant the worker an in-place read of the local diagnostic. **Recommended default:** granted, read-only, hash and identities reported only.
- **A3 Pair identity.** Which ORB and Aegis expressions are "the intended pair"? **Recommended default:** the accepted pins in `BOOK_SOURCES.sha256` (ORB v7 reconstruction venue-bound, Aegis 6J1 venue-bound), the editions the native-lane draft names. Earlier pair studies use different editions (ORB-MNQ-1 v6, Aegis v3) and are context, not baseline.

**Worker — apply these defaults unless Phase 0 contradicts them, then return `NEEDS_CONTEXT` with the conflict quoted:**

- **(A) Scope of "ready".** Ready means every row in Step 2.2 has a cited identity or an explicit `UNKNOWN`, never that performance was checked. **Recommended default:** inventory only.
- **(B) Two ORB identities.** If an export cannot be tied to the accepted ORB v7 pin, record it under its own identity (workshop spec's three-row rule); never relabel it.
- **(C) Synchronized excursion.** Experiment 2 needs same-instant adverse excursion for both legs. **Recommended default:** report per leg whether timestamped trades plus an admitted bar panel exist. Aegis has no listed 6J/MJY panel; record what `lab/analysis/c1/aegis_orbmnq_combined_book_2026-08-26/recover_6j_bars.py` established, do not run it.
- **(D) Arms eligibility.** Report Vanguard MGC v0.4 and Striker DJ30 pyramid-250 standing from their owners (withdrawal and readmission ADRs, campaign state). Do not rule on eligibility.

Post ambiguities under `## §0.5 Response — ambiguities`; status `NEEDS_CONTEXT` until resolved.

---

## §1 — Context

Codex's 2026-10-29 diagnostic located long weak stretches for ORB and Aegis, but measured them inside a four-leg account. Before any third-leg mechanism is studied, the pair must be measurable on its own. The repo already holds most of the raw material (the 10-28 data inventory, one falsified pair study, a third-leg shape sweep, one candidate non-result). This card collects it against the pair question rather than re-deriving it.

**What CC is being asked to produce:**

- `lab/analysis/c1/orb_aegis_third_leg_2026-10/READINESS.md`: rows R1–R10 (Step 2.2), each cell cited or `UNKNOWN`, then a verdict and a blocker list.
- One PR from a `claude/` branch carrying only that file (plus generated catalog files if a gate requires them).

**What CC is NOT being asked to do:** run any replay, simulation, bootstrap or statistic; pick a third-leg family; propose thresholds for later experiments; edit the native-lane pre-registration, the 10-28 inventory or any owner record; register the diagnostic in a private hash index.

---

## §2 — Execution plan

### Step 2.1 — Read and dedup

- **Inputs:** §0 reads.
- **Action:** Read-report plus paste-search output.
- **Expected output:** First response.
- **Per-step gate:** Every §0 anchor resolves; mismatch → `NEEDS_CONTEXT`.

### Step 2.2 — Inventory pass

- **Inputs:** INVENTORY.md rows, BOOK_SOURCES pins, prior studies, diagnostic.
- **Action:** Fill one row per item, citing an INVENTORY.md anchor (`F-…`) or a file:line wherever one exists:
  - **R1 Pair identity:** for ORB and Aegis, which exports bind to the accepted pins (code hash, export hash).
  - **R2 Common coverage:** date window per bound export, common window, trade counts, known gaps.
  - **R3 Clock:** EOD, proxy or intraday-honest per export; timestamp availability; bar panel for same-instant excursion (default (C)).
  - **R4 Cost basis:** label per leg as recorded, no rates; note campaign §62's Aegis zero-slippage issue.
  - **R5 Account dependencies:** for 50K and 100K, the firm_rules row identity and whether the native-lane draft binds a tier; whether integer quantities of each leg are recorded as executable (cite, do not compute).
  - **R6 Comparison arms:** R1–R4 for Vanguard MGC v0.4 and Striker DJ30 pyramid-250, plus standing (default (D)).
  - **R7 Native feasibility:** per leg and arm, whether a native source or configuration exists, is planned (native plan DRAFT), or is `UNKNOWN`.
  - **R8 Prior evidence:** the combined-book study, book-composition third-leg sweep, MOC fade and relevant rejections. For each: editions, tier, verdict, and what it can and cannot be reused for in Experiments 2–3.
  - **R9 Diagnostic provenance:** SHA-256, editions, account configuration, input hashes, windows; whether the three difficult windows come from the four-leg account.
  - **R10 Exposure:** per dataset, which windows earlier studies and the diagnostic already viewed (counts and windows only), per the workshop spec.
- **Expected output:** READINESS.md rows.
- **Per-step gate:** No empty cell; every non-`UNKNOWN` cell cited; every `UNKNOWN` cell names its owner.

### Step 2.3 — Consistency check

- **Inputs:** READINESS.md.
- **Action:** Re-verify every quoted hash against its index (`sha256sum`, `grep` in `BOOK_SOURCES.sha256` / `SHA256SUMS` / INVENTORY.md). Confirm vendor panels present via `sha256sum -c`. Run the §6.0 scans.
- **Expected output:** Pass list; at most one focused correction.
- **Per-step gate:** Any mismatch after the correction → `DONE_WITH_CONCERNS` with the row named.

### Step 2.4 — Verdict and return

- **Inputs:** Rows R1–R10.
- **Action:** Assign the §6 verdict; list blockers, each with the owner that can clear it; commit, push, open the PR.
- **Expected output:** PR plus §6 closure report.
- **Per-step gate:** Verdict follows §6 mechanically.

---

## §4 — Falsifiable hypothesis

`N/A — no hypothesis under test`; this is a no-run inventory. The readiness claim is decided mechanically: **if** R1, R2, R3 and R9 each resolve to cited identities for both pair legs on a common window, **then** Experiment 2 is dispatchable (READY when no cell is `UNKNOWN`, else READY_WITH_GAPS, per the §6 precedence); **otherwise** the claim is falsified for now and the return is the blocker list (NOT_READY).

---

## §5 — Forbidden moves

- **"Just a quick pair replay" to fill R2/R3.** Tempting because the simulator exists; it is Experiment 2 and spends exposure. Forbidden.
- **Reusing the 08-26 or 09-02 pair figures as the baseline.** Different editions, and the 08-26 study is FALSIFIED; R8 records them as context only.
- **Relabelling an unbound ORB export as v7.** Workshop spec three-row rule.
- **Quoting the diagnostic's figures.** Only hash, identities, windows and counts leave it. No prices, P&L, sizes, parameter values or per-trade timestamps anywhere (AGENTS.md §Derived outputs).
- **Copying private sources or the diagnostic into the worktree**, or passing them to Codex or any external service.
- **Ruling on Vanguard/Striker eligibility or the 50K/100K choice.** Report the owners' standing; the choice is Joshua's.
- **Editing INVENTORY.md or the native-lane draft to fix a gap found.** Record it as a blocker with its owner.
- **Scope creep.** Unrelated findings go to `DONE_WITH_CONCERNS`, unfixed.
- **Amending §6 after reading the evidence.** Return `BLOCKED — plan-itself-wrong`.

### §5.1 — Authority block

```yaml authority
seat: worker
parent: docs/superpowers/specs/2026-10-28-orb-aegis-workshop-design.md
max_risk: medium
capabilities: [repository.read, worktree.write, branch.push, pr.open]
constraints: [no_main_write, no_runs, private_data_not_committed, single_output_folder, reserved_files_untouched]
acceptance: [AC1_hash_citations_reproduce, AC2_public_class_scan_clean, AC3_folder_only_diff, AC4_launcher_check]
```

`parent` is a placeholder for A1: the workshop spec is the nearest existing ORB/Aegis research owner. Its evidence boundary and exposure rules apply here. This card is not a workshop session.

---

## §6 — Gate + status return taxonomy

The return carries one verdict from rows R1–R10 (READY / READY_WITH_GAPS / NOT_READY, mapped to RESOLVED / AMBIGUOUS / FALSIFIED below) and exactly one status: DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT or BLOCKED.

### §6.0 — Acceptance tests

| Test | Property it must violate to FAIL | Owner |
|---|---|---|
| `AC1_hash_citations_reproduce`: every SHA-256 in READINESS.md is found by `grep` in the index it cites, or reproduced by `sha256sum` in the operator's checkout | A quoted hash that does not match its owner | parent |
| `AC2_public_class_scan_clean`: `grep -nE '\$ ?[0-9]\|[A-Z]:[/\\\\]Users\|/home/\|/Users/' READINESS.md` returns nothing; manual read finds no price, P&L, size, parameter value or per-trade timestamp | Private-class content in a public file | parent |
| `AC3_folder_only_diff`: `git diff --name-only origin/main...HEAD` lists only `lab/analysis/c1/orb_aegis_third_leg_2026-10/` (plus generated catalog files a gate requires) | A write outside the single output folder | parent |
| `AC4_launcher_check`: `.\fp.ps1 check` (or `python -I scripts/fp.py check`); cite `record.json` | Gate failure introduced by the change; pre-existing failures disclosed | parent |

### Verdict (mechanical, from rows)

Apply in order; the first matching row is the verdict, so exactly one applies. "Core" means R1, R2, R3 and R9 resolved for both pair legs on a common window.

| Verdict | Trigger | Maps to |
|---|---|---|
| **NOT_READY** | Core does not hold | FALSIFIED (for now) |
| **READY_WITH_GAPS** | Core holds and at least one cell in R4–R8 or R10 is `UNKNOWN` | AMBIGUOUS |
| **READY** | Core holds and no cell in any row is `UNKNOWN` | RESOLVED |

Every `UNKNOWN` cell names the owner that can clear it (Step 2.2 gate); an `UNKNOWN` without an owner is a `DONE_WITH_CONCERNS` item, not a verdict change.

### Return status

| Status | Meaning | Parent action |
|---|---|---|
| `DONE` | All steps passed, AC1–AC4 green, no concerns | Review under §7 |
| `DONE_WITH_CONCERNS` | Completed; a correctness, scope or provenance doubt is flagged | Resolve before accepting |
| `NEEDS_CONTEXT` | Missing input that can be supplied (A1–A3, a §0 anchor mismatch, a file not on disk) | Supply once; a second bounce is re-cut |
| `BLOCKED` | Structural obstruction; sub-case required | See below |

`BLOCKED` sub-cases: `context-problem` (re-dispatch with context) · `capability-problem` (stronger model, or Joshua) · `scope-problem` (split, e.g. R10 into its own card) · `plan-itself-wrong` (coordinator rebuilds in a fresh session, Rule 7).

**Closure report format:**

```
Status: <DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED — <sub-case>>
Verdict: <READY | READY_WITH_GAPS | NOT_READY>
Per-step gates: 2.1 [..], 2.2 [..], 2.3 [..], 2.4 [..]
Acceptance: AC1 [..], AC2 [..], AC3 [..], AC4 [.. record.json path]
Diffs (files touched): <list>
Blockers (row → owner): <list>
Concerns surfaced: <list>
Next action recommended: <one sentence>
Measure: wall time, passes, corrections
```

---

## §7 — Parent-session review (after CC returns)

**Pass 1 — Spec compliance.** All ten rows present; nothing run; the diff is one folder; no owner record edited; no "while I was in there" change.

**Pass 2 — Quality.** Re-run AC1 and AC2 independently. Spot-check three cited INVENTORY.md anchors and the R9 hash in place. Confirm the verdict follows the §6 table mechanically, and that R8 doesn't present a prior figure as baseline.

**Pass 3 — Consolidated read.** Read R1–R10 together: does the common window in R2 match the windows in R9 and R10, and does R7's native status agree with R5's tier binding?

---

## §10 — Audit hooks (runnable)

```bash
F=lab/analysis/c1/orb_aegis_third_leg_2026-10/READINESS.md
# Anchors still resolve
git log -1 --format=%h -- lab/analysis/c1/strategy_data_inventory_2026-10/INVENTORY.md   # expect 631f6b6 or a later reviewed change
git log -1 --format=%h -- core/strategies/BOOK_SOURCES.sha256                             # expect 5516554 or later
# Every hash in the return appears in an index or is reproduced locally
grep -oE '[0-9a-f]{64}' "$F" | sort -u | while read h; do grep -rqs "$h" core/strategies/BOOK_SOURCES.sha256 core/data/tv_exports/cme/SHA256SUMS lab/analysis/c1/strategy_data_inventory_2026-10/INVENTORY.md || echo "NOT INDEXED: $h"; done
# Public-class scan
grep -nE '\$ ?[0-9]|[A-Z]:[/\\]Users|/home/|/Users/' "$F" && echo FAIL || echo clean
# Scope
git diff --name-only origin/main...HEAD
# This card
python -I scripts/check_brief.py docs/briefs/handoffs/2026-10-29-orb-aegis-third-leg-exp1-baseline-readiness-card-DRAFT.md --type cc_handoff
python -I scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-29-orb-aegis-third-leg-exp1-baseline-readiness-card-DRAFT.md
```

`NOT INDEXED` lines are expected only for the R9 diagnostic hash, which has no public index; AC1 covers it by in-place `sha256sum`.
