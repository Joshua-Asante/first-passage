# CC Handoff — search the operator's machine for the seven-strategy private evidence (T00 candidate 1)

**Type:** cc_handoff (read-only search and hash comparison on the operator's Windows machine)
**Date:** 2026-09-23
**Status:** RETURNED 2026-09-23 — `DONE_WITH_CONCERNS`, evidence **INCOMPLETE** (AMBIGUOUS); the identity-only inputs (Step 2.1 row 5) survive locally. **Ruled 2026-09-23** (operator: "accept the recommended reading and merge 474"): INCOMPLETE for the evidence; the row-5 inputs are recorded as surviving and neither falsify H nor reopen candidate 1 (§7.6). Drafted 2026-09-23 at the operator's direction ("Draft a handoff for a local session to find a copy").
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
Executed 2026-09-23 by one local Claude Code session. Nothing was moved, copied, renamed, deleted, opened for content, run or committed apart from this section (transcribed here by the coordinator from the return as pasted into the coordinator session; no private content). §0.5 answers (operator): drives "C: only" (plus an unlettered 1 GB recovery partition); OneDrive, version history and Recycle Bin "Yes, all".

### 7.1 Status and verdict
**`DONE_WITH_CONCERNS`.** The verdict splits along a line §4 and §6 do not draw:
- **Evidence (Step 2.1 rows 1–4) and the two undigested artifacts: INCOMPLETE.** No file matched the approval receipt, any of the 3 ledgers, the 5 override maps, the 5 monthly reconciliations or the 5 strategy reports. No UNVERIFIED candidate was found for the joint replay or the 125-test suite. Not NONE, because the roots in §7.4 were unreachable.
- **Identity-only row 5 (TV exports and Pine bodies): FOUND** for all 7 export/Pine pairs (the 5 phase-1 strategies and the 2 dropped sources). Under §4's letter H is falsified; these are the campaign's inputs, not its evidence, and cannot reconstruct the ledgers without the absent override maps and joint replay code.
- Executor's recommended reading: candidate 1 is AMBIGUOUS (INCOMPLETE) for the evidence, with the row-5 inputs recorded as surviving.

### 7.2 FOUND rows (Step 2.1 row 5 only)
| Path (relative to `~`) | Bytes | SHA-256 | Step 2.1 key |
|---|---|---|---|
| `Downloads/Aegis_6J1_VB_CME_6J1!_2026-09-03_cc310.csv` | 28364 | `71e732fc92d28a56fbc1e4aa358e10b68f317a110f3facc95ed34508fad96eaa` | `strategies[aegis_6j1].export_sha256` |
| `Downloads/aegis_6J1_venue_bound.pine` | 52092 | `db78ecba95ae78aca14501a5eaccfda2a42164d83cac12321cb7f293a9adca7c` | `strategies[aegis_6j1].pine_sha256` |
| `Downloads/ORB-MNQ-1_recon_v7_VB_CME_MINI_MNQ1!_2026-09-03_d03ac.csv` | 160557 | `bff235ea0934dace8a000dbad7eeede8673506718bd020f54f2c04cbae304568` | `strategies[orb_mnq_recon_v7].export_sha256` |
| `Downloads/orb_mnq_7_reconstruction_venue_bound.pine` | 23765 | `176c4f70c67d58053c4d3b8170d0a9be3733bc6b76b1e2f928bd7a877be052a3` | `strategies[orb_mnq_recon_v7].pine_sha256` |
| `Downloads/Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-09-03_9d7ea.csv` | 47348 | `5a5006588fa5c87628df7b1c15c8af8d8ae2250be0abb0371ea4d93665ef998e` | `strategies[striker_dj30_mym_pyramid_250].export_sha256` |
| `Downloads/striker_dj30_v4.5_mym_pyramid_250_cap100k.pine` | 27497 | `712cf395396568ce22ae43f1f15b085eaba23acf1b85502abb92129f277fffd7` | `strategies[striker_dj30_mym_pyramid_250].pine_sha256` |
| `Downloads/Striker_NAS100_MNQ_CME_MINI_MNQ1!_2026-09-03_30a74.csv` | 88221 | `f6a93bb653d710a77f8ebde8e64639ed913171c814cd13de5f00f76d0c3d1513` | `strategies[striker_nas100_mnq_dow_wed_excluded].export_sha256` |
| `Downloads/striker_nas100_v1_mnq_dow_wed_excluded_cap100k.pine` | 33013 | `fa6a70cde002131bbd266bee70defb01e32deae2de79fdc327d661f829115c39` | `strategies[striker_nas100_mnq_dow_wed_excluded].pine_sha256` |
| `Downloads/Vanguard_Gold_Futures_v0.4_VB_(MGC)_COMEX_MINI_MGC1!_2026-09-03_0e3e3.csv` | 74473 | `7b9cc65c98945055f35d55cdd43f049efc4b5924e2caa59f36d50b3eb872f9f2` | `strategies[vanguard_mgc_v04].export_sha256` |
| `Downloads/Vanguard_Gold_MGC_v0.4_venue_bound.pine` | 44177 | `af26899ca94bb0e9ee26d09e0176b6b94bba2f5da252399ce4d899fe7e3bad15` | `strategies[vanguard_mgc_v04].pine_sha256` |
| `Downloads/strategies/Striker_DJ30_MNQ_Q-TXG-1_PROTOTYPE_CBOT_MINI_MYM1!_2026-09-02_82cba.csv` | 45330 | `2c2d893ba0daa127f1c857e81ec436b535e4e8eb85f0c728e2ba39dc6485826d` | `dropped_sources[0].export_sha256` |
| `Downloads/strategies/striker_dj30_v4.5_mnq_qtxg1_prototype.pine` | 25856 | `178a2a8e1c78e45a5142749f92284c09d286907a7e096883e1133297cb8a806d` | `dropped_sources[0].pine_sha256` |
| `Downloads/strategies/Striker_NAS100_MYM_QTXG1_CME_MINI_MNQ1!_2026-09-02_304f8.csv` | 44177 | `f1e35c4ee1c9735c3ebbed99648a42034d9b3f57b53960f9e41f6e6c09b25f9c` | `dropped_sources[1].export_sha256` |
| `Downloads/strategies/striker_nas100_v1_mym_qtxg1_prototype.pine` | 30715 | `19264da29a3d9a30200600689e1950931f1abfb648e9071a232ee83fdec2756c` | `dropped_sources[1].pine_sha256` |

The primary checkout also holds Pine copies with the same digests: `…/inputs/private_overrides/op1/2026-09-14-seven/step3-coverage/Aegis-installed-body.pine` (Aegis), `…/step6-admission/pine/` (ORB, Striker DJ30), and `core/strategies/_archive/{striker,nas}/…qtxg1_prototype.pine` (both dropped sources). Excluded from the count: 3,035 matches against public manifest-input digests (config, early-close calendar, commission schedule, TV anchors, holiday calendar), all committed files in clones and worktrees.

### 7.3 Roots searched
A read-only Python walker hashed every file ≤ 2 GB (SHA-256, 1 MiB chunks; `.git`, `node_modules`, `.venv`, `__pycache__` pruned) against the 38 digests in `reconciliation_manifest.json` and `phase1_config.json` plus the §53 receipt digest, recording paths, sizes and digests only.
- **r1, the primary checkout, whole tree (232,204 files):** `local_artifacts/`, the lab dir's `inputs/` and `local_artifacts/`, `.superpowers/`, all 73 `.worktrees/*`, the 7 `.claude/worktrees/*`, `tmp/`. `git worktree list` shows 81 worktrees; the 15 outside the checkout are covered by r2/r3. The lab dir's `inputs/private_overrides/` (345 files) is the 2026-09-14 intake packet, not the 2026-09-08 one, and holds none of the 5 override-map digests; its `local_artifacts/` (27 files) holds 09-15 to 09-17 artifacts.
- **r2, other clones and user folders (15,898 files):** the six other local clones/worktrees, Downloads, Documents, OneDrive, and the operator's own Recycle Bin.
- **r3, profile backups and tool stores (600,576 files):** the private-backup and backup roots (including a `first-passage-local-main-2026-09-20` backup), older asides, data and scratch dirs, and the `.codex`, `.cursor`, `.agents`, `.claude`, `.cache`, `.local` stores and `C:\Temp`.
- **r4, misc (34 files):** `C:\tmp`, `.config`.
- **Name sweep** over all of C: for `*first-passage*`, `*multi_firm_operations*`, `*account-feedback-composition*`, `*approval-receipt*`, `*private_overrides*`, `*tradeify_seven_strategy*` (1,191 hits) surfaced no root outside r1–r4.
- **Joint-replay / 125-test name candidates:** 18 distinct hits; 17 are tracked files on `main`, the 18th is the gitignored `private_overrides/` directory. `Downloads/c24_joint_gate.py` (2026-08-29) is a pre-campaign MYM c24 gate. `canonical_*.csv` hits under `.codex/visualizations/2026/09/{02,06}` are pytest temp outputs of the runner's synthetic fixtures and match no ledger digest.
- **Noted, not a candidate:** a 34,937-byte Cursor agent transcript dated 2026-09-08 (not opened) whose directory name shows the packet lived at `.worktrees/tradeify-phase1-population/.superpowers/sdd/2026-09-02-seven-strategy-tradeify-select-configuration/account-feedback-composition-2026-09-08/`. That worktree no longer exists, consistent with M-41.

### 7.4 Roots unreachable
1. **Volume shadow copies:** `vssadmin list shadows` needs elevation. File History is not configured; no Windows Server Backup.
2. **245 access-denied Codex-sandbox pytest dirs** under `.codex/visualizations/2026/09/{02,06}`, dated before the 09-08 packet. Changing their ACLs is a security-settings change and was not attempted.
3. About 160 Codex-sandbox test dirs (`.superpowers/sdd/*/pytest-*`, `.cache/skill-review-tests-*`) in the primary checkout; other SIDs' Recycle Bins; locked `C:\Temp\*.tmp` files.
4. OneDrive cloud side: 18 cloud-only placeholders (2025 personal files, no repo-related names); online recycle bin and version history need a web sign-in and were not accessed.
5. One file over 2 GB in the primary checkout, skipped under §2.3.

### 7.5 Operator follow-ups the executor raised (none taken)
1. Rule how the split verdict in §7.1 reads.
2. Say whether to open §7.4 roots 1–2, the only places the 09-08 evidence could still sit unseen.
3. Consider preserving the 14 row-5 files: they are the only surviving local copies of the campaign's inputs outside the gitignored checkout paths.

### 7.6 Coordinator reaction (2026-09-23) and operator ruling
**Operator ruling (2026-09-23, verbatim):** "accept the recommended reading and merge 474". This adopts the first bullet below. The remaining bullets are recommended operator actions, not yet taken: the shadow-copy listing, closing root 2, and copying the inputs.

- **The split is a drafting defect in this packet, not an executor error.** Step 2.1 listed row 5 as "identity only", but §4 falsified H on *any* Step 2.1 digest. The executor applied the letter and flagged it correctly. §1 is the governing purpose: only the evidence would reopen candidate 1. **Recommended ruling:** read the verdict as **INCOMPLETE (AMBIGUOUS)** for the evidence, and record the row-5 inputs as *surviving inputs*, which neither falsify H nor reopen candidate 1.
- **§7.4 root 1 (shadow copies): worth one elevated, read-only `vssadmin list shadows`.** It is a listing, not a restore. If it shows no shadow copy created on or after 2026-09-08, root 1 closes empty. **§7.4 root 2 (Codex sandbox dirs): recommend closing without opening.** They predate the 09-08 packet, the readable siblings held only synthetic-fixture pytest output, and opening them needs an ACL change. If root 1 closes empty and root 2 is closed by ruling, the evidence verdict becomes **NONE**, and candidate 1 is **UNREACHABLE** in the T00 sense (§7.8 of the T00 return), with the public digests proving what existed.
- **Preserving the row-5 inputs: agree, but copy, don't move.** A move within the same disk adds no durability. Copying into the existing private-backup root keeps the Downloads originals and adds a second location; the digests above pin both. Pine bodies and vendor CSVs stay out of git either way (public-clone posture).

## §10 — Audit hooks (runnable)
```
# The approval-receipt digest the search matches; expect one hit in §53
grep -n "bad72266716a31782960c49deed0e25c8c2dc8256300cd8bbc2423d7778d73aa" docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md
# The manifests carrying the other keys; expect both files present
ls lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/reconciliation_manifest.json lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/phase1_config.json
# No private artifact committed by the return; expect no output
git ls-files lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/inputs lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/local_artifacts
```
