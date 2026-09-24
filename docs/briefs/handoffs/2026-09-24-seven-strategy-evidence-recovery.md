# CC Handoff — recover the seven-strategy campaign evidence locally (shadow copies and agent transcripts)

**Type:** cc_handoff (read-only recovery attempt on the operator's Windows machine)
**Date:** 2026-09-24 (executed 2026-09-23 local)
**Status:** RETURNED 2026-09-23 — `DONE`, verdict **RECOVERED** (H falsified) by exactly one evidence file: the Aegis private override map (`strategies[aegis_6j1].pine_input_overrides_sha256`). Every other evidence digest remains unrecovered; see §7.1 for the reading the operator is asked to rule on.
**Executor:** one local Claude Code session on the operator's machine. **Operator:** owns the machine, answers §0.5, and receives the return.
**Authority:** write recovered files only under the primary checkout's `local_artifacts/recovery-2026-09-24/` (M-41); the only repo change is §7 of this packet. No private file contents are printed, quoted or committed; the return reports paths, sizes and hashes only.

## §0 — Rule 0 reads (before any search)
- The previous search, [2026-09-23-seven-strategy-evidence-local-search.md](2026-09-23-seven-strategy-evidence-local-search.md), especially §2.1 and §7.2–§7.4.
- [M-41](../../methodology/lessons/methodology_lessons.md) (private artifacts inside a worktree die with the worktree).
- [Campaign record](../programs/2026-09-03-seven-strategy-select-campaign-state.md) §53–§54.
- [Tradeify protection selection](../../notes/2026-09-10-tradeify-protection-selection.md).

## §0.5 — Ask the operator once, before starting
1. May the session run one elevated, read-only `vssadmin list shadows`, and read a qualifying shadow copy read-only?
2. May the session read agent session transcripts (`%USERPROFILE%\.claude\projects\**\*.jsonl`, `%USERPROFILE%\.codex\sessions\**`, Cursor agent transcripts including the 34,937-byte 2026-09-08 transcript)? Default yes; search and reconstruct only, show no contents.
3. Should the 245 access-denied Codex sandbox folders stay closed? Default yes; opening them needs an ACL change.

## §1 — Why
The campaign's private evidence lived in two `.worktrees/*` paths that cleanup deleted (M-41). The 2026-09-23 search hashed every reachable file and found only 14 inputs, no evidence. Two sources remained untried: shadow copies taken before the deletion, and agent transcripts, which often contain the full text of files an agent wrote. A recovery counts only when its SHA-256 equals a published digest.

## §2 — Steps
**Step 1, preserve first.** Copy the 14 files from the previous search's §7.2 into `local_artifacts/recovery-2026-09-24/surviving-inputs/`; re-hash each copy against §7.2. Do not delete or move the originals; remove no worktree.

**Step 2, match keys.** A file is RECOVERED only if its SHA-256 equals one of: the 38 digests in `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/reconciliation_manifest.json` and `phase1_config.json`, plus the §53 approval receipt `bad72266716a31782960c49deed0e25c8c2dc8256300cd8bbc2423d7778d73aa`; new: the §54 disposition `6b88401332405d2c8e70ebe7bd6bb40999379f818304fdbef757005e1475e7f3` (`repair-v6-disposition/disposition.json`). Without a published digest, and so reportable only as UNVERIFIED candidates: the joint replay code, the 125-test synthetic suite, the C1–C5 specification and manifest, the feasibility-screen report, and the `dd-orb-base-only-2026-09-10` weighting-study reports.

**Step 3, shadow copies (if approved).** Run `vssadmin list shadows` elevated; record each shadow's creation time and volume. A shadow qualifies only if created after 2026-09-08 and before the worktrees were removed (pin the removal time from `git reflog`, the worktree admin directory or a folder timestamp; if it cannot be pinned, treat any shadow after 09-08 as a candidate). Walk each qualifying shadow read-only through its `\\?\GLOBALROOT\Device\HarddiskVolumeShadowCopyN\` path; never mount, restore or revert. Hash against Step 2; copy matches and named candidates into `recovery-2026-09-24/shadow/`, keeping the relative path.

**Step 4, transcripts (if approved).** Stream the transcripts for tool calls that wrote or displayed files whose paths contain `account-feedback-composition`, `approval-receipt`, `c5-approved-design-revision`, `repair-v6-disposition`, `canonical_`, `private_overrides`, `tradeify-phase1-population`, `tradeify_seven_strategy`, `feasibility`, `dd-orb-base-only` or `joint`. Rebuild only complete-content writes (Claude `Write`, Codex `apply_patch` "Add File" blocks, a full-file `cat`/`Get-Content` output). For each rebuilt file try LF and CRLF, with and without a trailing newline; RECOVERED on a digest match, otherwise an UNVERIFIED candidate under `…/transcripts/<source>/<original-relative-path>`. Keep every version of a path written several times, labelled with its transcript timestamp.

**Step 5, the weighting study.** Search the checkout's ignored roots and the Step 3–4 results for `dd-orb-base-only-2026-09-10` and for reports, figures or scripts tied to the 2026-09-10 selection; report survivors by path and hash only.

## §4 — Hypothesis
**H:** no byte-identical copy of any Step 2 artifact is recoverable from shadow copies or transcripts. **Falsified (RECOVERED):** any digest matches. **Stands (NONE):** every approved source was read with no matches and no UNVERIFIED candidates. **Otherwise:** INCOMPLETE.

## §5 — Forbidden
Committing, printing or quoting private contents; restoring or reverting a shadow copy, changing ACLs, deleting or moving originals; removing worktrees; treating an UNVERIFIED rebuild as evidence; scoring or running anything (re-scoring candidate 1 against P1–P7 is a separate, operator-authorized step).

## §6 — Return
Exactly one of `DONE` (with RECOVERED or NONE), `DONE_WITH_CONCERNS` (INCOMPLETE), `NEEDS_CONTEXT` or `BLOCKED — <reason>`, written as §7 below.

## §7 — Executor return

Executed 2026-09-23 (local evening) by one Claude Code session on the operator's machine, from worktree `.claude/worktrees/pr-363-babysit-671b91` writing by absolute path into the primary checkout's `local_artifacts/recovery-2026-09-24/`. Read-only Python walkers (`C:\Python314\python.exe`, SHA-256 over exact bytes) printed paths, sizes and digests only. No private content was printed, quoted or committed; nothing was moved, deleted, restored, run or scored; no worktree was removed. **§0.5 answers (operator):** (1) "Yes, list and read"; (2) "Yes (default)"; (3) "Open them" — see §7.5 item 1 for why they stayed closed.

**Setup deviation (disclosed).** The handoff's premise that the primary checkout's root `local_artifacts/` is gitignored is **false**: `.gitignore` ignores only `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/local_artifacts/`. Before writing any byte, the session appended `/local_artifacts/recovery-2026-09-24/` to the primary checkout's local, uncommitted `.git/info/exclude` and confirmed `git check-ignore` on a probe and on a recovered file. Remove that line to undo it. Whether root `local_artifacts/` should be ignored in `.gitignore` (as M-41 assumes) is an open question for the operator.

**Match keys.** The two manifests carry **37 distinct** digests (62 occurrences; the handoff's "38" double-counts one shared value). The §53 receipt and §54 disposition digests bring that to 39. The session added **2 more** that the handoff lists as "no published digest": the [protection-selection note](../../notes/2026-09-10-tradeify-protection-selection.md) §Evidence publishes `screen-config.json` `5d0b0d4d5dab84faf9beb930cfc6bbe12a06ed886b45337e761885ab58d324e5` and `results.json` `a3151f86123487ccacbb40c70562d47ad5446edbe685aa287512f9c1c61d5e6c` for `dd-orb-base-only-2026-09-10`. Total **41 keys**.

### 7.1 Status and verdict
**`DONE` — RECOVERED.** One file's SHA-256 equals a Step 2 evidence digest, which falsifies H under §4. Recommended reading for the operator's ruling:
- **Recovered:** 1 of the 5 private override maps (Aegis). **Not recovered:** the other 4 override maps, the 3 canonical ledgers, the 5 monthly reconciliations, the 5 strategy reports, the C5 approval receipt, the repair-v6 disposition, and both weighting-study files. One override map cannot reconstruct the ledgers, so this does **not** by itself reopen candidate 1 for P1–P7 scoring. That remains a separate operator step (§5).
- **UNVERIFIED rebuilds exist for every named undigested artifact:** C1–C5 specification and manifest, the joint/shared replay code, synthetic-suite tests, the feasibility-screen report, and the weighting-study report and script (§7.3). They carry no digest, so none is evidence. Several are early versions, since later partial edits were not replayed (§2 Step 4).

### 7.2 Step 1 — surviving inputs preserved
All 14 files from the 2026-09-23 search's §7.2 were copied (not moved) into `local_artifacts/recovery-2026-09-24/surviving-inputs/`, with the `Downloads/` prefix dropped and the `strategies/` subfolder kept. Each original and each copy was re-hashed: **14 of 14** match §7.2 in bytes and SHA-256. The originals remain in `~/Downloads`.

### 7.3 Step 3 — shadow copies
`vssadmin list shadows` (elevated, read-only) lists **two** shadows, both on `C:` (`\\?\Volume{d2f804c0-0971-4f61-9928-7d9224b4f092}\`), provider "Microsoft Software Shadow Copy provider 1.0", type ClientAccessibleWriters:

| Shadow volume | Created (local) | Qualifies? |
|---|---|---|
| `HarddiskVolumeShadowCopy4` | 2026-09-23 18:01:59 | No |
| `HarddiskVolumeShadowCopy5` | 2026-09-23 18:02:41 | No |

**Removal time pinned:** `.worktrees/tradeify-phase1-population` was still listed in a transcript at 20:50Z on 2026-09-10 and is recorded as absent, together with `.worktrees/tradeify-used-account-kernel`, by the [2026-09-10 Track B umbrella brief](2026-09-10-track-b-qualify-accepted-book-umbrella.md) (its "Filesystem (2026-09-10, this machine)" line). Neither worktree has a `.git/worktrees/` admin entry left. The last reflog trace is the `origin/codex/tradeify-phase1-population` push on 2026-09-05. Both shadows postdate removal by about 13 days, so **none qualifies and none was walked**. Shadow copies 1–3 no longer exist.

### 7.4 Step 4 — transcripts

**Stores read, with counts per tool:**

| Store | Files / rows | Complete-content tool calls parsed | Partial edits (not replayed) |
|---|---|---|---|
| Claude `~/.claude/projects/**/*.jsonl` (includes subagents) | 4,288 files, 589,442 records | `Write` 2,424; `Read` 20,744 (full-file results only); `Bash` 67,862 (single-path `cat`/`Get-Content` only) | `Edit` 7,205 |
| Codex `~/.codex/sessions` + `archived_sessions` | 795 rollouts, 310,886 records | `exec` 25,036, holding 3,933 `apply_patch` bodies → 981 "Add File" blocks; single-command `cat`/`Get-Content` outputs | `apply_patch` "Update File" hunks |
| Codex SQLite (`thread_history_1`, `logs_2`, `state_5`, `memories_1`) | 272,667 rows | every string value, plus "Add File" blocks | — |
| Cursor `~/.cursor/projects/**/agent-transcripts` (incl. the 34,937-byte 09-08 transcript) | 711 files, 28,150 records | `Write` 1,387; `ApplyPatch` 384 → 64 "Add File" blocks | `StrReplace` 4,136 |

Besides the named-path rebuild, **every string value of 20+ characters** in every record (about 11.7M strings) was hashed in LF and CRLF forms, each with and without a trailing newline, against all 41 keys. That catches a full-file display anywhere in a transcript, whatever the tool.

The **Cursor transcripts store tool inputs only, never tool results**. The 09-08 transcript made 22 `ReadFile`, 7 `Shell`, 4 `Glob` and 4 `rg` calls and no writes. It names the packet's files (`specification.md`, `change-manifest.json`, `joint-account-code-handoff.md`, `RESUME-CURRENT.md`, several receipts and reviews) but holds none of their bytes.

**RECOVERED (digest match):**

| Source | Original path | Bytes | SHA-256 | Matched key |
|---|---|---|---|---|
| Codex sub-agent `size_intake_review`, thread `01a07334-986d-7da1-b0fa-889bf53f4557`, command output 2026-09-05 20:15:27Z; the same bytes are in `thread_history_1.sqlite` | `.worktrees/tradeify-used-account-kernel/lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/inputs/private_overrides/aegis_6j1.json` | 3,588 | `460f40fa079c00a97711d743aa0a5acee62f1c8f2cc33972b8a92b7948e42d08` | `strategies[aegis_6j1].source_identity.pine_input_overrides_sha256` (= `phase1_config.json` `pine_input_overrides_sha256`) |

The file is saved at `recovery-2026-09-24/transcripts/codex/multi_firm_operations/.worktrees/tradeify-used-account-kernel/lab/…/private_overrides/aegis_6j1.json`. It matches as LF with a trailing newline; the raw transcript form (3,590 bytes, `4fc14061…`) does not. After placement it was re-hashed independently against the manifest.

**Other digest matches (not evidence).** These are the same kinds the 2026-09-23 search excluded. Public manifest inputs tracked on `main`: `config` (9,548 B), `tradeify_commission_schedule` (428 B), `cme_early_close_calendar` (3,809 B), the `source_calendar` metadata (109,816 B) and `tv_summary_anchors` (4,111 B). Also `strategies[aegis_6j1].pine_sha256` (52,092 B, CRLF), an identity-only input that already survives (§7.2). These are displayed in Codex rollouts dated 09-03 to 09-16 and in two Claude subagent transcripts of the `tradeify-feasibility-screen-4142c0` session.

**Where the unrecovered digests surface as text only.** The following hex strings appear in Codex `thread_history_1.sqlite` as text, typically printed next to a path by a hashing command, but no content-bearing output there matches them: the receipt digest 85×, the disposition 34×, each weighting-study digest 18×, and each ledger, reconciliation and report digest 44–219×. This shows which Codex threads created those files. Recovering from them would mean replaying partial edits, which §2 Step 4 excludes.

**UNVERIFIED candidates.** 546 distinct rebuilds (source × path × SHA-256) were saved as exact transcribed bytes. Each is stored as `recovery-2026-09-24/transcripts/<source>/<original-relative-path>` with `__<timestamp>__<kind>__<sha8>` inserted before the extension, so every version of a path written more than once survives; the LF/CRLF/newline variant digests are in the index. Excluded: 36 at paths tracked on `origin/main`, 7 empty, and 5 partial `-Tail`/`-TotalCount` outputs. That leaves 498. Why they can't be verified: none has a published digest, and each is one transcript moment, possibly superseded by later unreplayed edits. The named-artifact classes:

| Class (Step 2 name) | Source · kind | Bytes | SHA-256 | Transcript time (UTC) | Path (under `.worktrees/tradeify-phase1-population/.superpowers/sdd/2026-09-02-seven-strategy-tradeify-select-configuration/` unless stated) |
|---|---|---|---|---|---|
| C1–C5 specification | Codex · apply_patch Add | 40,289 | `828e15c29cf5d56cac9bc01ccf30272f202a79cbcff3b6ab82b6092795efab26` | 2026-09-08 23:11 | `account-feedback-composition-2026-09-08/specification.md` |
| C1–C5 specification | Claude · full Read | 44,612 | `3b2f83d584a00f9d34602f4a1d29e405fe04a342c2084b9494a23c4dff77a176` | 2026-09-08 23:31 | same path, later version |
| C1–C5 manifest | Claude · full Read | 17,092 | `cc2641d3d0164fbf28a52ef82e83cf1c744ae0495f29b9fd3857bc1c3c24d1f8` | 2026-09-08 23:31 | `account-feedback-composition-2026-09-08/change-manifest.json` |
| Feasibility-screen report | Codex · full `Get-Content` | 28,754 | `c164664819a8853c8bf380aacf323d7a60d085958641a258803eddf6820fe6ca` | 2026-09-10 03:26 | `feasibility-screen/REPORT.md` |
| Feasibility-screen config | Claude · Write | 13,747 | `13bd8f5e5e9f9cfbfb978098172a9f62965a4a723ec0a0fe0ef58946ab64277e` | 2026-09-10 02:51 | `feasibility-screen/screen-config.json` |
| Feasibility-screen session scratch | Claude · Write | 12,679 | `a11d000846b687c275fb45c3ddb483d5b316490729f840ad740b731f1fdde790` | 2026-09-10 02:32 | `C:\Temp\claude\…tradeify-feasibility-screen-4142c0\…\scratchpad\STAGING.md` (that scratchpad is now empty on disk) |
| Feasibility-screen session scratch | Claude · Write | 3,198 | `0e57fe9476054bba72c2c7f4423fffa49c271a3d6d384f0665d7b020c941de80` | 2026-09-10 03:05 | same scratchpad, `corrections.md` |
| Feasibility-screen session scratch | Claude · Write | 5,199 | `43ba5f0326eacb84e29acb1e9efa3151c7b3d1597719e5db9294d654796e8765` | 2026-09-10 03:05 | same scratchpad, `disposition.md` |
| Feasibility-screen session scratch | Claude · Write | 13,739 | `64f92dee726aba6a1e23c9c9e4f7277135b9aaf995bd783cf1d282ff927b61eb` | 2026-09-10 02:54 | same scratchpad, `screen-config.json` |
| Feasibility-screen session scratch | Claude · Write | 26,889 | `b4056b5b77856a414478f64df601eccc50e05cb7968123ccd33e8ca58b9e1a2c` | 2026-09-10 02:57 | same scratchpad, `screen.py` |
| Feasibility-screen session scratch | Claude · Write | 20,225 | `7c8496081a76be15a2b2dc306fb24a19d478ed2d584a01762ba3aab95e1de776` | 2026-09-10 02:59 | same scratchpad, `test_screen.py` |
| Weighting study | Codex · apply_patch Add | 6,998 | `57d475fe74f120280f99ea87aafdccf3558ece006b893f5b6e88e30074938b5f` | 2026-09-10 05:22 | `dd-orb-base-only-2026-09-10/REPORT.md` |
| Weighting study | Codex · apply_patch Add | 7,120 | `3b04d7c5d7368d243cc8e7054cff10f05ee4507b322f0559ce167e29083d3df5` | 2026-09-10 05:19 | `dd-orb-base-only-2026-09-10/compare.py` |
| Weighting study | Codex · full `Get-Content` | 4,622 | `027ba0c6409d6e6512156d931b11f0dde265498107501597736de14cf337acec` | 2026-09-10 05:21 | `dd-orb-base-only-2026-09-10/run.log` |
| Joint replay (named dir) | Codex · apply_patch Add | 15,046 | `a679a3bfefbd6d77cfb445a730ae653370203070fb09c344d7176507c51a6aee` | 2026-09-05 18:11 | `.worktrees/tradeify-used-account-kernel/.superpowers/sdd/2026-09-05-tradeify-joint-replay/audit_pine_capture_defaults.py` |
| Joint replay (named dir) | Codex · apply_patch Add | 4,639 | `b57039e6ae66114d6a0bf9548590140f4ff031736f1024af19a221ae4200d212` | 2026-09-05 18:29 | same dir, `finalize_population_evidence.py` |
| Joint replay (named dir) | Codex · apply_patch Add | 8,672 | `54e446403a071463111c44d01e0d096dc96c87ab899375879136444ac4784654` | 2026-09-05 18:07 | same dir, `update_private_captures.py` |
| Joint/shared replay code | 91 rebuilds (Cursor Write 46, Claude Read 29 + Write 1, Codex Add 13 + cat 1, SQLite 1) | — | per-file in index | 2026-09-05 → 09-10 (28 on 09-09, 46 on 09-10) | mostly `offline-shared-replay-2026-09-09/composition_replay/` (31) and `/ports/` (15), `orb-replay/orb_replay/` (13), `offline-shared-replay-2026-09-09/` (13), plus `joint-account-code-handoff.md` (Claude Read, 4,352 B, `678854fe…`) |
| 125-test synthetic suite | 43 test-file rebuilds (Cursor Write 26, Codex Add 9, Claude Read 8) | — | per-file in index | 2026-09-06 → 09-10 | `offline-shared-replay-2026-09-09/tests/` (27), `orb-replay/tests/` (9), `parallel-work/cursor-aegis-vanguard-calculators/tests/` (7) |

The remaining 350 UNVERIFIED rebuilds fall outside the named classes: other `tradeify-phase1-population` packet files 251, `private_overrides/op1/2026-09-14-seven` intake scripts and attestations 37, other `account-feedback-composition-2026-09-08/` evidence and reviews 13, unrelated "joint" work (the 08-30 joint-surrogation study and others) 31, "feasibility" elsewhere 11, other 7. **No rebuild exists for** `c5-approved-design-revision/approval-receipt.json`, `repair-v6-disposition/disposition.json`, any `canonical_*` ledger, the other four override maps, or the weighting study's `screen-config.json` / `results.json`.

**Full per-file listing (private, local):** `recovery-2026-09-24/transcripts/candidates-classified.json` (295,590 B, `bf9803484e9b6e83dfce0781f7ee83a09b50c547c7883b9dc7e554f26b0d9a5d`) and `candidates-untracked.json` (935,321 B, `a8a2f887b9ebb8eaa3ea8160792d2784830224d1a8a049c78b64df0a22068906`). Scan indexes: `index-cursor-codex-claude.json` (`bd975134…04c66`), `index-codex.json` (`500c2836…d59d8`), `index-sqlite.json` (`31fa8918…03dd4`), `index-apps.json` (`45a43acc…132ce`). The 498 rows are kept out of this public file: they are private path names with no evidential status, and the local index holds each row's source, path, bytes, SHA-256, variant digests, timestamp and transcript.

**Additional agent/editor stores (added by the executor, same read-only method).** VS Code and Windsurf `User/` (including Local History), ZCode, opencode (`%APPDATA%` and `~/.local/share`), Claude desktop `%APPDATA%\Claude`, `%APPDATA%\Claude Code`, `%LOCALAPPDATA%\Cursor` and `cursor-agent`: 19,616 files, 1.61 GB, 85 SQLite databases. Every file was exact-hashed and every string value brute-forced. **0 matches.**

### 7.5 Step 5 — weighting study (`dd-orb-base-only-2026-09-10`)
- **On disk:** none. A name sweep over `~`, `C:\Temp` and `C:\tmp` (784,119 files, excluding `AppData`, `.git`, venvs and `node_modules`) hashed all 2,244 files whose names matched the study, screen-config, results, disposition, receipt or feasibility-screen patterns, against all 41 keys: **0 matches**. No directory named `dd-orb-base-only*` exists. The only related directories are the empty `C:\Temp\claude\…tradeify-feasibility-screen-4142c0` scratchpad, that session's Claude transcript directory, and the 09-08 Cursor transcript directory.
- **From transcripts:** UNVERIFIED `REPORT.md`, `compare.py` and `run.log` (§7.4 table). The two published digests (`screen-config.json`, `results.json`) match nothing; their bytes were never displayed in full in any transcript.

### 7.6 Still unreachable
1. **155 access-denied Codex sandbox directories** under `~/.codex/visualizations/2026/09/{02,06}` (the earlier "245" counted a wider set; 155 is today's access-denied frontier). The operator answered "Open them". The session tried an elevated read with backup semantics, which changes no ACL, but the auto-mode permission classifier blocked it as a security weakening, and it was not retried. Opening them needs the operator either to change their ACLs or to allow that read. They predate the 09-08 packet.
2. **Shadow copies 1–3:** deleted before 2026-09-23; the surviving two postdate the removal (§7.3).
3. **Partial edits:** Claude `Edit` (7,205), Cursor `StrReplace` (4,136) and Codex "Update File" hunks were not replayed (§2 Step 4). So later versions of the UNVERIFIED files, and anything built only by edits, are out of reach by this method.
4. **Cursor tool results:** not stored by Cursor; reads cannot be rebuilt.
5. **Script-written artifacts:** ledgers, reconciliations, reports, the receipt and the disposition were produced by programs, not shown by agents; the transcripts hold their digests (text), not their bytes.
6. **Minor:** 24 locked browser-cache files in the app stores; text files over 64 MiB in the app stores were exact-hashed but not string-scanned; about 160 Codex-sandbox test directories inside the primary checkout (2026-09-23 search §7.4 item 3), outside this task's scope; OneDrive's cloud side, unchanged from 2026-09-23.

### 7.7 Operator follow-ups (none taken)
1. Rule on the reading in §7.1: RECOVERED under §4's letter, for one override map only; candidate 1 is not reopened.
2. Decide whether to open §7.6 item 1, by an ACL change you make yourself or by allowing the elevated read-only walk.
3. Decide whether the UNVERIFIED C1–C5 specification, manifest, reports and replay code are worth your identification. They cannot become evidence without a digest.
4. Decide whether to add root `local_artifacts/` to `.gitignore`, since M-41 names it as an ignored root but it is not.

## §10 — Audit hooks (runnable)
```
# The two new keys the executor added; expect one hit each in the protection note
grep -n "5d0b0d4d5dab84faf9beb930cfc6bbe12a06ed886b45337e761885ab58d324e5\|a3151f86123487ccacbb40c70562d47ad5446edbe685aa287512f9c1c61d5e6c" docs/notes/2026-09-10-tradeify-protection-selection.md
# The recovered file's key; expect one hit in the manifest
grep -c "460f40fa079c00a97711d743aa0a5acee62f1c8f2cc33972b8a92b7948e42d08" lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/reconciliation_manifest.json
# No private artifact committed; expect no output
git ls-files local_artifacts lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/inputs lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/local_artifacts
```
