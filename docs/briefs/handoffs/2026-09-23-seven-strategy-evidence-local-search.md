# CC Handoff — search the operator's machine for the seven-strategy private evidence (T00 candidate 1)

**Type:** cc_handoff (read-only search and hash comparison on the operator's Windows machine)
**Date:** 2026-09-23
**Status:** DRAFTED 2026-09-23 at the operator's direction ("Draft a handoff for a local session to find a copy"). Dispatch to one local Claude Code session on the operator's machine. Its return lands in §7.
**Executor:** one local Claude Code session with read access to the operator's drives. **Operator:** owns the machine, approves each search root outside the checkout (§0.5), and receives the return.
**Authority:** read, list and hash files; write §7 of this packet and nothing else. Moving, copying, deleting, uploading or committing any private byte is forbidden (§5).

## §0 — Rule 0 reads (before any search)
- [T00 step-1 return](2026-09-22-tradeify-t00-step1-producer-inventory.md) §3 (candidate 1), §7.4 and §7.8 (the archive search found no copy in `first-passage-archive`).
- [M-41](../../methodology/lessons/methodology_lessons.md) (the evidence lived in gitignored `.worktrees/*` and died with those worktrees).
- [Campaign record](../programs/2026-09-03-seven-strategy-select-campaign-state.md) §53 (the approval-receipt digest) and §54 (the 125-test synthetic implementation).
- The public manifests that carry the match keys (§2): `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/reconciliation_manifest.json` and `phase1_config.json`.

## §0.5 — Clarifying questions (ask the operator once, before searching)
1. Which drives and external volumes are in scope? The default is every fixed drive, plus any external drive the operator names.
2. May the session read OneDrive or Dropbox version history and the Recycle Bin? The default is yes, list-and-hash only.

## §1 — Context
T00 step 1 returned INSUFFICIENT. Candidate 1, the seven-strategy campaign's joint replay and private evidence, is UNKNOWN for local backups only: the archive route is closed. A byte-identical copy would reopen candidate 1 for scoring against P1–P7. It would not change the verdict by itself, since scoring is a separate, operator-authorized step.

## §2 — Execution plan
### Step 2.1 — Match keys: a file counts only if its SHA-256 equals a published digest
| Artifact | Published digest (owner) |
|---|---|
| C5 approval receipt (`c5-approved-design-revision/approval-receipt.json`, in private packet `account-feedback-composition-2026-09-08`) | `bad72266716a31782960c49deed0e25c8c2dc8256300cd8bbc2423d7778d73aa` (campaign record §53) |
| Canonical ledgers (events, trades, weekly exit blocks) | `reconciliation_manifest.json` → `ledgers.*` |
| Private override maps `inputs/private_overrides/<strategy_id>.json` | `phase1_config.json` → `strategies[*].pine_input_overrides_sha256` |
| Monthly reconciliations and strategy reports | `reconciliation_manifest.json` → `local_monthly_reconciliation_sha256.*`, `local_strategy_report_sha256.*` |
| TV exports and Pine bodies (identity only; never commit) | `phase1_config.json` → `strategies[*].export_sha256`, `pine_sha256` |

The joint replay code and the 125-test synthetic suite have **no published digest**. Report candidate paths for those by name, marked **UNVERIFIED**; they need the operator's judgement.

### Step 2.2 — Search roots (each approved per §0.5)
1. The primary checkout's ignored roots: `local_artifacts/`, `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/inputs/private_overrides/` and `.../local_artifacts/`, and `.superpowers/`.
2. Surviving worktree remnants: `.worktrees/*` and `.claude/worktrees/*` in every clone of `first-passage` on the machine; also run `git worktree list` in each clone.
3. Other clones or copies of the repo: directories named `first-passage*`.
4. The Recycle Bin, Windows File History / backup volumes, OneDrive/Dropbox folders and their version history, and any named external drive.
5. Download and staging folders, for names containing `account-feedback-composition`, `approval-receipt`, `canonical_`, `private_overrides`, `joint` or `synthetic`.

### Step 2.3 — Hash and compare
List first, then hash only candidate files of 2 GB or less. Use `Get-FileHash -Algorithm SHA256 <path>` or `python -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" <path>`. Compare each hash against Step 2.1: record matches exactly, and non-matches by count only. Print no private content into the session or the return.

## §4 — Falsifiable hypothesis
**H:** no byte-identical copy of the seven-strategy private evidence survives on the operator's machine. **Falsified if** any file's SHA-256 equals a Step 2.1 digest, and the return is then FOUND. The hypothesis stands (NONE) only when every approved root was searched **and no UNVERIFIED candidate was found**. The joint replay and the 125-test suite have no published digest, so a candidate for either cannot be ruled out by hashing. An unreachable root, or any UNVERIFIED candidate awaiting the operator's identification, makes the return INCOMPLETE, not NONE.

## §5 — Forbidden moves
- Moving, copying, renaming or deleting any file; writing hash output into new files beside the originals.
- `git add`, commit or push of any private artifact; `git worktree remove` or any cleanup.
- Uploading, pasting, quoting or summarizing private contents.
- Scoring, running or importing the evidence. Scoring against P1–P7 for the selected four is a separate step the operator authorizes after FOUND.

## §6 — Gate + status return
Report exactly one of `DONE` / `DONE_WITH_CONCERNS` / `NEEDS_CONTEXT` / `BLOCKED — <sub-case>`. `DONE` carries a verdict of **FOUND** or **NONE**. NONE means no published-digest match *and* no UNVERIFIED candidate. `DONE_WITH_CONCERNS` carries **INCOMPLETE**, naming the unreachable roots and every UNVERIFIED candidate that awaits the operator's identification. The investigation verdict maps as FOUND → FALSIFIED (H), NONE → RESOLVED (H stands), INCOMPLETE → AMBIGUOUS.

## §7 — Executor return
_Pending._ Required: the status; the verdict; per FOUND row, the path, size, SHA-256 and the Step 2.1 key it matches; UNVERIFIED candidates by path; the roots searched, with commands; the roots unreachable.

## §10 — Audit hooks (runnable)
```
# The approval-receipt digest the search matches; expect one hit in §53
grep -n "bad72266716a31782960c49deed0e25c8c2dc8256300cd8bbc2423d7778d73aa" docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md
# The manifests carrying the other keys; expect both files present
ls lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/reconciliation_manifest.json lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/phase1_config.json
# No private artifact committed by the return; expect no output
git ls-files lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/inputs lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/local_artifacts
```
