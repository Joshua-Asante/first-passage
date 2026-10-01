# Staged acceptance handoff set — bounded next steps toward deployment (2026-09-27)

**Status:** PREPARED 2026-09-27 under the operator direction recorded in the [deployment-checklist addendum 2026-09-27](../../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-09-27--staged-acceptance-evidence-proportional-to-the-next-step). None is dispatched by this file. **Revised the same day** after the operator's review of `9448373`:
- H1, H3 and H4 now continue [#519](https://github.com/Joshua-Asante/first-passage/pull/519)'s returns instead of redoing them.
- H1 separates proposal correction from measurement execution.
- H4 waits on an accepted classification contract.
- H5 returns a policy choice.
- H9 keeps its full-S5 dependency, with two checkpoints.

**Operator rulings of 2026-09-27 applied here:**
- ORB L1 and the fence classification contract ([§59 Ruling 7](../programs/2026-09-03-seven-strategy-select-campaign-state.md#ruling-7--orb-lifecycle-l1-reaffirmed-and-the-account-fence-classification-contract-2026-09-27));
- no same-session restart after an incident ([incident ADR §A11.2](../../adr/2026-09-17-bounded-platform-protection-incident-contract.md#a112--operator-ruling-no-same-session-restart-of-automation-after-an-incident-2026-09-27));
- the S5 staged gates with Part A-only rule scope, hold kept ([ledger](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--s5-staged-gates-approved-part-a-only-rule-scope-hold-kept-2026-09-27));
- preservation-trade read targets ([incident ADR §A11.3](../../adr/2026-09-17-bounded-platform-protection-incident-contract.md#a113--operator-ruling-preservation-trade-evidence-as-the-target-of-authorized-reads-2026-09-27)).

The operator also directed that H1(a), H2, H3, H5(a), H7 and H8 proceed now, reusing #519's returns, and that each commissioning row return as a ready-to-run row for explicit execution approval.

**Pinned inputs from #519.** The returns are unmerged and are read at the PR head `8c15f1853e64f14f50995e3f1c55a620a0f674b7`, for example `git show 8c15f18:<path>`:
- `docs/notes/2026-09-26-s5-part-a-measurement-proposal.md` and its card `docs/briefs/handoffs/2026-09-26-s5-part-a-measurement-proposal.md` (fix round and coordinator review);
- `docs/notes/2026-09-26-orb-lifecycle-evidence.md` and `docs/notes/2026-09-26-account-fence-four-state-trace.md`, with the card `docs/briefs/handoffs/2026-09-26-orb-lifecycle-and-fence-trace.md`;
- `docs/notes/2026-09-26-close-semantics-c-a.md` and its card.

If #519 merges before dispatch, the same paths on `main` are used, once they are confirmed byte-identical.

**Ownership:**
- The campaign coordinator dispatches each card under the committed-handoff rule. At dispatch the coordinator copies the card into its own file with its `yaml authority` block and runs the pre-dispatch read ([surface-allocation ADR](../../adr/2026-07-14-cc-cursor-surface-allocation.md#decision), *Action classes and the authority block*). This set carries no authority block because a file holds only one.
- **A card never grants what its dispatcher lacks.** Capabilities listed under "Grants at dispatch" narrow the dispatching seat's own grants. Any CI-configuration change, Linux dispatch, artifact download, account action or spend also needs the operator approval named on the card; the card only records that approval.
- The addendum owns sequencing and the checkpoints CP-1a..CP-9. Each card's named owners keep their outcomes.

**Common rules:**
- Read `AGENTS.md` first.
- No agent places, amends or cancels an order. No merge, spend, arm, deploy, vendor contact or account access by an agent.
- No private source, account figure, P&L or credential is committed, quoted or sent to an external service. The book's Pine and runtime ports are read only in place in the operator's primary checkout ([§60](../programs/2026-09-03-seven-strategy-select-campaign-state.md#60--agent-read-access-to-the-accepted-books-pine-and-runtime-ports-2026-09-25)).
- Commissioning results are labelled `COMMISSIONING_OBSERVATION` and state their scope. After review they may support capability acceptance for that scope. They are never production E1/n3 results, portfolio admission or whole-route acceptance (addendum §2).
- A synthetic result never marks an obligation that needs a real producer as resolved.
- A finding that changes behavior returns to its owner decision before the freeze (addendum §5).

**Dispatch states:**
- **READY:** existing authorization covers it now.
- **READY ON <event>:** dispatch when that event is recorded.
- **LATER:** requirements recorded, not yet a card.

| Card | Workstream | State | Unlocks |
|---|---|---|---|
| H1 | S5 and resource limits | Step (a) **RETURNED and ACCEPTED 2026-09-27** ([r2 CP-1a packet](../../notes/2026-09-27-s5-part-a-measurement-proposal-r2.md)); step (b) **RETURNED 2026-09-27; tooling accepted as PRELIMINARY** ([#526](https://github.com/Joshua-Asante/first-passage/pull/526) at `27df508f`: the harness, its README and the dispatch-only workflow). **Re-opened narrowly 2026-09-27 by operator ruling** ([r2 §12.9](../../notes/2026-09-27-s5-part-a-measurement-proposal-r2.md#129-operator-ruling-2026-09-27-completion-fields-legacy-bundles-and-incomplete-stage-1b-evidence); [dispatch amendment](#h1-steps-b-and-c-dispatch-record-frozen-2026-09-27)). The ruling covers explicit completion fields, retained legacy bundles, the Stage 1b `INCOMPLETE_EVIDENCE` verdict with exit 3 and the committed regression suite. The acceptance evidence below covers `27df508f` only. **Revision returned 2026-09-27 at `11e15c6b`** ([#526](https://github.com/Joshua-Asante/first-passage/pull/526)). It implements r2 §12.9 and commits `tests/test_s5_part_a_measurement_harness.py`: 94 tests, the 75 migrated from the scratchpad plus 19 new ones that exercise the exit semantics through the real `--summarize` and combine entry points. Its diff touches only the four allowed files. Coordinator re-check in a clean detached worktree at `11e15c6b` (Linux; ops environment interpreter CPython 3.11.15, GCC 13.3.0, the same as each record's `recorder_python`, including the worker's; run through `python3 -I scripts/fp.py --env <ops-env>`), each run with status completed, exit 0 and `source_stable: true`: module pytest, 94 passed (record `20260927T210947Z-53e23ce81e78`, `record.json` SHA-256 `bd502c79a4c72fe78face4bb0bb9d654261d2723cbc77eccd5f7b3d5e369081e`); the same with `--workers 2`, 94 passed (record `20260927T210956Z-99b581cb9a21`, SHA-256 `721f3686a80c1e252c08cf98b30902ec6993f43b6583a6455dec873e15e6e0a8`); and `check` (record `20260927T211010Z-4757d619e6c3`, SHA-256 `ae57234b4497aa0500e454541dc6b46decdd349e9628a8aa7fd633ba0e16ce5d`). The worker's own records have matching hashes: `60d81651…`, `7ab40660…` and `2089180d…`. Its before-state record against the `b55958c8` harness (`9a21b5c9…`) failed on all 16 new §12.9 cases, as the amendment requires. All seven record directories, together with the package `h1b-526-r8-verification-evidence-2026-09-27.tar.gz` (SHA-256 `1e225d328e651ee08755a2d7794ba888680f3b92aa01bcfcaeeaf8b41d97fb1d`, with a `MANIFEST.tsv`), are **retained** in `first-passage-archive` commit `7e6b5232` ([first-passage-archive#840](https://github.com/Joshua-Asante/first-passage-archive/pull/840)). The coordinator re-hashed every new blob from a fresh clone and verified the package against its manifest. actionlint 1.7.7 (binary SHA-256 `9f7dedb4e23f89f2922073d1a6720405b7b520d4f5832ebb96f0d55a2958886c`) exited 0 on the workflow at `11e15c6b` (file SHA-256 `c7883ce45c9cc9efa99772e9280661d0346505b143e0818cd4a06d34c4b7c0b5`), with shellcheck disabled and with no shellcheck on `PATH`. `check` has no actionlint gate, so this is separate evidence. The output file `actionlint-11e15c6b.txt` (SHA-256 `757cf2935d8fdf8be19f272e19b6b927964d4032c147a7f26136908e5bdfd7b3`) is archived on the same archive PR at `b74d6399`. The nine pins are registered in `docs/evidence/PRIVATE_EVIDENCE.sha256`. *[Corrected 2026-09-27 (Codex review of 158a7d75): the 137-pin audit above predates these pins.]* `scripts/evidence_archive.py audit --verify`, run from this tree against the archive clone, reports **146 pins: 49 ARCHIVED, 9 UNPUSHED, 88 MISSING, 0 CORRUPT**. The 9 UNPUSHED are exactly this revision's nine pins: they are pushed to the archive branch of first-passage-archive#840 and count as ARCHIVED only once it merges into the archive's `main`. The audit after that merge is recorded on [#523](https://github.com/Joshua-Asante/first-passage/pull/523), and measurement execution waits for it. The 88 MISSING predate this work. **Re-verified 2026-09-27 at the Codex-clean head `6010cb50`**, after r2 §12.9 plus Codex rounds 9–10, with 138 regression tests. Coordinator re-check in a clean detached worktree (CPython 3.11.15, ops environment), each run with status completed, exit 0 and `source_stable: true`: module pytest, 138 passed (record `20260927T215236Z-6635ade5a6a1`, SHA-256 `83f7d8bf8efb2816380674f920ad17e69f71b92b2cfd1a3aa57bbabc1659abec`); `--workers 2`, 138 passed (`20260927T215249Z-98f5326b3eb8`, `1687bf3bc590947de7e3c3e39c29643af78ff75f4ec2510fcc181ae61f7485a2`); `check` (`20260927T215304Z-3259777d365c`, `d256f1211b0b6bfffb16a7b0a0cf01c26989f944a4278cda9471e1a9a0e07107`). actionlint 1.7.7 exited 0 on the workflow at `6010cb50` (file SHA-256 `0c5ef761…`; output `1f82405e59a63fc629aae879822aa1e64b7532500bd0c33a8ed6a29baf35fcb3`). The worker's records have matching hashes: `e9ee3344…`, `6c4f5535…`, `1c9cf820…` and actionlint output `b1975dee…`. Its before-state record against `73526d6d` (`2b8f73d4…`) failed on all 23 new cases, as required. *[Corrected 2026-09-28 (helper review of #523, B6): #526's own record table gives that record as "status failed, exit 1: 25 failed (23 new cases plus the 2 updated dry-run reason tests), 113 passed". Its baseline is `73526d6d`, round 10's pre-fix head. The dispatch record's baseline ("Records", below) is `b55958c8`, and this row cites no before-state against that head.]* All seven record directories, both actionlint outputs and the package `h1b-526-r10-verification-evidence-2026-09-27.tar.gz` (SHA-256 `e17e69af7ee93dbc4d75ab83cbf2cd54b8a637119374973e7fe6962a9c826995`) are **retained** in `first-passage-archive` commit `71da82ed` ([first-passage-archive#841](https://github.com/Joshua-Asante/first-passage-archive/pull/841)). Their ten pins are registered in `docs/evidence/PRIVATE_EVIDENCE.sha256`. `audit --verify` from this tree now reports **156 pins: 58 ARCHIVED, 10 UNPUSHED, 88 MISSING, 0 CORRUPT**. The 10 UNPUSHED are exactly these pins. The `11e15c6b` pins are ARCHIVED since first-passage-archive#840 merged (post-merge audit on #523), which supersedes the 146-pin count above. They count as ARCHIVED only after #841 merges into the archive's `main`, and measurement execution also waits for that post-merge audit, recorded in this row (r2 "Current authority"; the audit output is also posted on #523). **Post-merge audit** (`scripts/evidence_archive.py audit --verify` against the archive's `main`, which re-hashes every archived blob; #841 merged at `758364aa`): 156 pins, **68 ARCHIVED, 0 UNPUSHED, 88 MISSING, 0 CORRUPT**; all ten `6010cb50` pins are ARCHIVED. **Updated from main 2026-09-27 at the operator's approval: head `3b321768`** (parents `6010cb50` and main `ed3e476f`). The four harness files are byte-identical to `6010cb50` (workflow SHA-256 `0c5ef761…`); the merge brings in only main's four files. Coordinator re-check in a clean detached worktree at `3b321768` (CPython 3.11.15, ops environment), each run with status completed, exit 0 and `source_stable: true`: module pytest, 138 passed (record `20260927T222523Z-28d209052e97`, SHA-256 `5de0ed31d489fa4e8efb3721729c4f29cda5a065f2d50adf789f4fe954343714`); `--workers 2`, 138 passed (`20260927T222541Z-2b38f39c0270`, `24d497c84efd67f505c8dcf92d5e0ffd23a961280d7c8b73e0855278f31db67c`); `check` (`20260927T222556Z-50f5f3823f83`, `c53c65a8e417b6968d5777ed0e8d4d7b2bd4c5903acef782c7a1e53d872ad06e`); actionlint 1.7.7 exit 0 (output `677344df7df26b9ae7cc7849573029e09dc583f4afe16e0ed4bd3c22b99cc67d`). The three record directories, the actionlint output and the package `h1b-526-r11-verification-evidence-2026-09-27.tar.gz` (SHA-256 `1b135897d0f503ec6173fddb7bbcb8e3d0e8c7de52aecb983fb761dfe5a9b9c8`, with a `MANIFEST.tsv`) are **retained** in `first-passage-archive` commit `2816a182` ([first-passage-archive#842](https://github.com/Joshua-Asante/first-passage-archive/pull/842)). Their five pins are registered, and the `6010cb50` evidence and pins are preserved unchanged. **Updated from main again at `a6b43bdb`** under the same approval, after #522 merged (parents `3b321768` and main `38e62eed`; harness files unchanged). Coordinator re-check at `a6b43bdb`, same conditions: module pytest, 138 passed (`20260927T223137Z-ed89b8bcc575`, `8e3d5d3cf5ed891240601563fdc3b04dc8334a415ac696b4d07e4f148e60ea4c`); `--workers 2`, 138 passed (`20260927T223149Z-a2022cd47ecf`, `850d2ae4304bec8b3c04a430a22588075a305f14f17a9225140cb7db538c181b`); `check` (`20260927T223204Z-526df770fa53`, `2a06f3b46094e43f7909ca9c48fdebe26dda2392cf77589ffec090934b886eee`); actionlint exit 0 (`09b92ac2065b1fe010afc39be8ff9b7e64434d62d7f0be310245f22dc6d14bfb`); package `h1b-526-r12-verification-evidence-2026-09-27.tar.gz` (`6728d84ee39029a233ea751e7eeb7d1573c25a82e4a17d9f34420a8ab6236176`), retained in `first-passage-archive` commit `148d857e` on the same PR. `audit --verify` reports **166 pins: 68 ARCHIVED, 10 UNPUSHED, 88 MISSING, 0 CORRUPT**; the 10 UNPUSHED are exactly the `3b321768` and `a6b43bdb` pins, ARCHIVED once #842 merges into the archive's `main`. **Post-merge audit** (`scripts/evidence_archive.py audit --verify` against the archive's `main`, which re-hashes every archived blob; #842 merged at `53cde303`): 166 pins, **78 ARCHIVED, 0 UNPUSHED, 88 MISSING, 0 CORRUPT**; all ten `3b321768` and `a6b43bdb` pins are ARCHIVED. **Updated from main a third time at `77b916f7`** under the same approval. The operator's update-branch made it after #523 merged (parents `a6b43bdb` and main `c918cad5`; harness files unchanged). Coordinator re-check at `77b916f7`, same conditions, each run completed with exit 0 and `source_stable: true`: module pytest, 138 passed (`20260927T233808Z-c5adc9c18463`, `d9c6f99c4407a4bf98092f3e7e606d40149626006ae05ce3fb2cc718f25a3b47`); `--workers 2`, 138 passed (`20260927T233821Z-5cf67b73287c`, `481283abce889235f7e1fd2f0dbe309fb63f36869056a3cd846f57ff15ae864d`); `check` (`20260927T233836Z-1005f7b5bf2f`, `f79c76236120b49a81f2fcb2ccca0ebaa8e499e7119e5661fa2b412e462796e0`); actionlint exit 0 (`846e81d84f6333cb788b4a17459f192e04bf3332dab0b706c198ff4d2b9bf842`). The package `h1b-526-r13-verification-evidence-2026-09-27.tar.gz` (`04eda1246ac875cfdde4553e87e6bb4e2f2c9387936e7213387d68ced3c084f4`) and the records are retained in `first-passage-archive` commit `5802a900` ([first-passage-archive#843](https://github.com/Joshua-Asante/first-passage-archive/pull/843)). `audit --verify` reports **171 pins: 78 ARCHIVED, 5 UNPUSHED, 88 MISSING, 0 CORRUPT**; the 5 UNPUSHED are exactly the `77b916f7` pins, ARCHIVED once #843 merges into the archive's `main`. **Post-merge audit** (`scripts/evidence_archive.py audit --verify` against the archive's `main`, which re-hashes every archived blob; #843 merged at `b560ac2a`): 171 pins, **83 ARCHIVED, 0 UNPUSHED, 88 MISSING, 0 CORRUPT**; all five `77b916f7` pins are ARCHIVED. **The operator merged #526 at `77b916f7`** (merge commit `0dcceb08`). That is the head verified above, and its evidence is on the archive's `main`. This entry records the post-merge audit that r2's "Current authority" gate requires before measurement. The gate is met once this record is on `main`. Measurement then proceeds only within r2's bounded authority (§12.7 caps; S5 HELD until CP-1b). **Measurement readiness is still not established**: Stage 1a and the Linux probe and dry run remain. S5 stays HELD. Coordinator re-check in a clean detached worktree at `27df508f` (Linux; ops environment, CPython 3.11.15, through `python3 -I scripts/fp.py --env <ops-env>`), repeated 2026-09-27 18:06 UTC to retain the records: `python -m pytest tests/ops/qualification/test_part_a.py -q` gave 11 passed (record `20260927T180621Z-71bad46c8b99`, `record.json` SHA-256 `3148c330b5f8c81ba08f28dec0d8b60382a5028be924b5fd91ae44063414da7f`), re-run 19:27 UTC in the conforming form with AGENTS.md's xdist option, `--workers 2`: 11 passed (record `20260927T192748Z-83497246ddaf`, workers 2, `record.json` SHA-256 `9c54f2d460d653789edb5cf35ba6cf282c39a691d11caae7486092c1ae3dd414`), which is the acceptance evidence for these tests; `check` exited 0 (record `20260927T180630Z-2534fb8215cf`, SHA-256 `c36bb4c4a09dbf4c1f6be6d2fec05e3ba75bf2a0f87f681be7c4168ee55aca79`, with the vendor-data absent-tree skips). *[Disclosed 2026-09-28 (helper review of #523, B5): every `check` record this row cites ran in a cloud container. There the `skill-deploy-sync` gate prints "SKIP … NOT CHECKED, not a pass", because the harness-owned `~/.claude/skills` holds none of this repository's skills. The retained `2534…`, `3259…` and `1005…` records show that line; `4757…`, `50f5…` and `526d…` ran in the same container. In none of them is that gate a pass.]* Both records show `status: completed`, verification exit 0, `source_stable: true`, complete capture and no report errors. *[Corrected 2026-09-28 (helper review of #523, B3): three records precede that sentence, not two. All three were re-read from their retained copies, and the hashes match the pins. Each shows `status: completed`, exit 0, verification exit 0, `source_stable: true`, `capture_complete: true` and empty `report_errors` and `capture_errors`. That includes the acceptance record `20260927T192748Z-83497246ddaf` (`--workers 2`), whose test summary is 11 collected, 11 passed, 0 failed, 0 errors, 0 skipped.]* **Retained 2026-09-27** in the private `first-passage-archive` by content address (`evidence/sha256/<aa>/<digest>`, one `evidence/INDEX.tsv` row each), commit `41eab925`, merged into the archive's `main` at `0a38b0f3` ([first-passage-archive#837](https://github.com/Joshua-Asante/first-passage-archive/pull/837)): both directories' files byte for byte, plus the package `h1b-526-verification-evidence-2026-09-27.tar.gz` (SHA-256 `45cd25db6031e259b11bc272c8ad9bb98fbc1e3741507f8ec0f5138057950823`; both directories and a `MANIFEST.tsv` of paths, sizes and hashes). The coordinator re-hashed every archived blob from a fresh clone of that pushed branch, and the package extracted from it verifies against its manifest. The pins are registered in `docs/evidence/PRIVATE_EVIDENCE.sha256`; The `--workers 2` record's directory is archived the same way (commit `821966f5`, merged at `59e21fac`, [first-passage-archive#839](https://github.com/Joshua-Asante/first-passage-archive/pull/839)) and its pin is registered too. `scripts/evidence_archive.py audit --verify`, run from this tree against the merged archive, reports all four of these pins ARCHIVED. Its complete counts across the registry are 137 pins: 49 ARCHIVED, 0 UNPUSHED, 88 MISSING, 0 CORRUPT. *[2026-09-28: the counts as they stood then. The registry has grown since; the latest complete counts are the #843 post-merge audit below (171 pins).]* The 88 MISSING pins predate this work and are not H1 evidence. The harness compiles and calls no production entry point. Image-first finding (static inspection): the worker image's build context cannot carry the harness (`image.py`, `runtime.py` import closure), so `host_venv` is the expected runtime under CP-1a (2)(d). That inspection is an input, not proof: the runtime is decided only when the Linux probe and dry run record image-first feasibility ([dispatch record](#h1-steps-b-and-c-dispatch-record-frozen-2026-09-27)). *[Corrected 2026-09-27 (pre-merge review): the workflow refuses `runtime=worker_image`, so no dry run exercises the image. The probe and dry run establish `host_venv` readiness; the image-first decision is this recorded static finding under CP-1a (2)(d).]* If Stage 1b runs on `host_venv`, PA-5 validates the mismatch at C3. **Measurement readiness is not established.** It still needs Windows Stage 1a and the Linux accounting probe and dry run, including failure handling and cleanup ([dispatch record](#h1-steps-b-and-c-dispatch-record-frozen-2026-09-27)). After the operator merges: Stage 1a, the optional Stage 0 and then the Stage 1b dispatch, within the §12.7 caps; step (c) **RETURNED, REVISED twice and ACCEPTED 2026-09-27** ([#525](https://github.com/Joshua-Asante/first-passage/pull/525) at `011ce9e4`). *[2026-09-28 (helper review of #523, B7): #525 merged (merge commit `ed3e476f`) carrying post-acceptance corrections 1–11 made after `011ce9e4`. Those corrections **await the operator's acceptance**, as the note's dated status update says.]* The first revision carries the same-day rulings on its open questions and drafter's additions ([ledger](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--h1c-draft-open-questions-and-drafters-additions-2026-09-27)). The second applies the operator's three review corrections, made before full-text acceptance: the S5 run-tooling scope covers the workflow validators, the subset handling, `guard_s2_runs.py` and the regression tests; the C3 order is explicit (review, grant, run, then Stage 2/PA-5); and the build-entry text is applied against a pinned head that CP-1b then names. The coordinator verified all three at `875ecf29`. **Full text ACCEPTED by the operator at `011ce9e4`** ([ledger](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-acceptance--h1c-full-text-accepted-build-entry-sections-to-be-applied-2026-09-27)). The build-entry sections are **applied in [#527](https://github.com/Joshua-Asante/first-passage/pull/527) at `afa26a66`**, against the pinned head `875ecf29`. That PR changes only two files: the S5 packet (RC-6 re-anchor) and the slices plan (§3.4(d)). The coordinator verified all 96 added lines against the accepted note at `011ce9e4`: the only differences are the filled placeholders. RC-6 is met once #527 is merged and reviewed and CP-1b names that revision. *[2026-09-28 (helper review of #523, B4): #527 merged at `6380dcb4`. Its commits after `afa26a66` (`8da41f91`, `f9a7ccdd`, `36b79e1b`, `b6c38a80` and `7b6df3fa`) mirror the owner text's post-acceptance corrections into the S5 packet. The 96-line verification above therefore covers `afa26a66` only, and those corrections await the operator's acceptance. The merged revision needs the review that CP-1b names.]* The RC-2 sections wait for C3. Still open: OQ-1, plus Q1, Q7 and Q9 to C3; the operator's acceptance of the owner text's post-acceptance corrections 1–11 *[added 2026-09-28, B7]* *[2026-09-28, after the B4/B7 markers: the operator accepted corrections 1, 2, 4–7 and 9–11 as build-entry text; 3 and 8 stay at C3 ([ledger](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-acceptance--h1c-post-acceptance-corrections-1-2-47-and-911-2026-09-28)).]* **Step (b) EXECUTED 2026-09-28** by the coordinator named in the [execution dispatch](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md#coordinator-transfer-and-execution-dispatch--h1-step-b-measurement-2026-09-28), at `7675c088`, before #536's dispatch markers. Stage 0 coverage holds and Stage 1a is valid. The Stage 1b dry run (36364714432) and measure run (36364854404) are valid. The measure run's memory is VERIFIED; the dry run's memory is complete but UNVERIFIED by design, as for any dry run. No re-run was used. The rule is applied as provisional PART_A TEST_ONLY ceilings of 120 s / 300 s, the shared values, with no profile edit. The CP-1b packet, with the build-entry table, is [in the ledger](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md#coordinator-cp-1b-packet--build-entry-status-2026-09-28). S5 stays HELD until CP-1b. *[**CP-1b RULED 2026-09-28:** the hold is released for the TEST_ONLY build at release head `05f3788` ([ledger](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--cp-1b-s5-hold-released-for-the-test_only-build-2026-09-28)). H1 step (b) is complete.]* | RC-3a for CP-1b |
| H2 | Broker route commissioning | **RETURNED and ACCEPTED 2026-09-27**: [packet](../../notes/2026-09-27-route-commissioning-session-packet.md). ~~Owed before any CP-3: the §3.7 request-body step (primary checkout).~~ *The §3.7 request-body step was discharged 2026-09-28 from the current public CrossTrade documentation ([§3.7 closure](../../notes/2026-09-27-route-commissioning-session-packet.md#37-closure-2026-09-28--request-shapes-from-the-current-public-crosstrade-documentation), PR #540; captures preserved under the primary checkout's `local_artifacts/route-drills-2026-09/vendor-docs/`). The cross-check against the retained 2026-09-25 captures (R-3.7a; `local_artifacts/t08-rest-route-assessment-2026-09-25/`) is owed in the primary checkout and does not block a CP-3 request.* The M2 dispatch (X-2) is carded 2026-09-27 ([M2 card](2026-09-27-m2-modify-semantics.md)) and DISPATCH-READY; its execution needs a local session in the primary checkout | CP-2 now; then CP-3 per row |
| H3 | ORB lifecycle and fence: disposition, owner text for Ruling 7, H4 card | **RETURNED and ACCEPTED 2026-09-27** ([disposition](../../notes/2026-09-27-orb-fence-ruling6-disposition.md)); operator answers applied (§5 addendum entry; inclusive stale boundary) | H4 |
| H4 | Fence classification: synthetic repair plus ORB L1 replay correction | **RETURNED and ACCEPTED 2026-09-27**, synthetic scope ([PR #522](https://github.com/Joshua-Asante/first-passage/pull/522) at `9e18d85`; [card](2026-09-27-h4-fence-classification-orb-l1-repair.md), *Coordinator acceptance of the return*; the real producer, route integration and the CC-3 halt are still owed) | Synthetic half of the fence obligation; the replay correction before freeze; CP-5 input |
| H5 | Attended operations | Step (a) **RETURNED and ACCEPTED 2026-09-27** (halt/resume amendment, with the O-6/O-7 clarifications applied); step (b) **RETURNED and ACCEPTED (PARTIAL, §7 (B)) 2026-09-27** ([PR #521](https://github.com/Joshua-Asante/first-passage/pull/521) at `32e0863`; [card](2026-09-27-h5b-attended-incident-rehearsal.md), *Coordinator acceptance of the return*; CC-3 stays open); the stale-individual-signal node was removed by a recorded variance (§10), and the operator ruled the classification the same day (a late bar is a source incident; halt/resume §4.1) | T13 construction |
| H6 | Settlement evidence | Collection READY ON CP-2; rehearsal harness READY | CAP S1/S2 toward QUALIFIED |
| H7 | Production qualification host | **RETURNED and ACCEPTED 2026-09-27** ([note](../../notes/2026-09-27-host-obligations-assignment.md)); RC-5 recorded in the ledger; RC-4 slice accepted at CP-1a (5), so the RC-4/RC-5 assignment at build entry is met ([ledger](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--cp-1a-decisions-16-adopted-as-recommended-hold-kept-2026-09-27)); host cost owed before CP-8 | RC-4/RC-5 assignment (S5 build entry); later CP-8 |
| H8 | Feed (provider-neutral) | Step (a) **RETURNED and ACCEPTED 2026-09-27** ([note](../../notes/2026-09-27-feed-provider-neutral-preparation.md); [draft spec](../../spec/2026-09-27-cme-execution-feed-equivalence-test-DRAFT.md)); step (b) **RETURNED and ACCEPTED 2026-09-27** as documentary classification ([PR #524](https://github.com/Joshua-Asante/first-passage/pull/524) at `a1a3c3e`; [note](../../notes/2026-09-27-h8b-feed-gap-classification.md), *Coordinator acceptance*; Q-1 PROPOSED in spec §4.3, Q-2 parked, Q-3/Q-4 ruled into halt/resume §4.1); step (c) PREPARED, READY ON this card's merge and #521 ([card](2026-09-27-h8c-omission-incident-session-end.md)) | CP-7 inputs; the F1 feed section; the empty-interval rule before CP-6; verification of the omitted-slot ruling |
| H9 | Result/seal and recovery | Preparation READY ON S5 C3 accepted *(C3 accepted 2026-10-01: preparation is READY)*; R1 ON S5 acceptance and **both D-S5 fix slices merged, each with its own full S4-plus-Part-A Linux run read ok and its own acceptance: #586 (D-S5-1/D-S5-2), then the D-S5-3 slice from `claude/capture-retry-noop`** ([defects ruling](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--land-s5-with-two-named-test_only-defects-fix-before-t05-2026-10-01) · [D-S5-3 ruling](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--d-s5-3-capture-exact-retry-demotion-also-gates-t05-r1-2026-10-01)); R2 ON D3 text and R1 | T06/S8 |
| H10 | Final launch | LATER | CP-9 |

---

## H1 — S5 measurement: correct the #519 proposal, return a measurement dispatch

**Continues:** the #519 S5 Part A measurement proposal at `8c15f18`, which carries its coordinator review ("ACCEPTED AS INPUT; nothing approved; S5 stays HELD"). It is not redone.

**Uncertainty resolved:** (a) whether the proposal, corrected for the 2026-09-27 split, is ready for the operator's approval as a rule plus a concrete measurement dispatch. (b) After approval: the measured CPU, wall time and memory of PART_A at forced maximum expansion on the existing engine, and the provisional ceiling that follows.

**Prerequisites and existing authorization:**
- Step (a): operator ruling 2026-09-26 §6, which authorizes *preparing* the proposal only.
- Step (b): **CP-1a approval of the dispatch returned by (a)**. Preparation authority does not authorize any measurement, CI-configuration change, Linux dispatch or artifact download.

**Step (a) work: amend the #519 proposal; write a corrected revision, not a new analysis.**
- **Carry forward unchanged, as findings:**
  - the (2, 4, 2) fixture cannot expand, so maximum expansion needs the forced arm (§0.1);
  - no existing measurement covers maximum expansion;
  - `verify_for` dominates;
  - the engine's pilot predicate needs the PA-2b term;
  - no host factor is evidenced;
  - the three `/v7` `diagnostic_budget_profile` pitfalls and the fixture-cap tuple.
- **Keep every review correction:**
  - the cold repeat is included;
  - setup CPU is excluded from Ĉ;
  - D̂ stays uncovered until Stage 1c;
  - Windows figures validate the harness only;
  - host venv versus worker image is disclosed;
  - Stage 0 is calibration only;
  - the D2 falsifier stays open until a valid Stage 1b record.
- **Preserve the requirements:**
  - maximum expansion (forced arm, 4 panels);
  - the reference runtime (the `ubuntu-24.04` qualification runner class, identity recorded per run);
  - aggregate memory: PA-3 is a check against the one shared campaign footprint, never a per-phase value;
  - measurement validity: PA-4 (digests identical, prefix byte-identical to the prescribed arm, spread ≤ 1.30 with one re-run).
- **Update for 2026-09-27:**
  - RC-1 is met on `main` (#517 merged at `5ad04cf`).
  - The RC table is restated on the build-entry, C3 and before-F1 split ([ledger](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-direction--s5-build-entry-separated-from-checkpoint-c3-acceptance-2026-09-27)).
  - Pre-build feasibility is §5's arithmetic on the proposed `/v7` values; the executed `bind_budget` check moves to C3 (RC-3b).
  - RC-4/RC-5 are assigned via H7 and do not wait on F1.
  - **Rule scope: PART_A only, TEST_ONLY** (ruling 2026-09-27). Drop Stage 1b-N2 and the phase-generic option. `/v7`'s N2 ceiling is returned as a separate operator decision (for example, extending the M13 "/v6 only" ruling). The multipliers stay candidates.
- **Return a concrete measurement dispatch, as one approval packet.** For each step it gives the exact commands, the files created, the grants it needs, its limits, stop conditions and outputs:
  - Stage 0: download the S4 run artifacts, calibration only. It must run before the logs expire around **2026-10-09**. *[2026-09-27: the download was done on 2026-09-26 (ledger, conditional ruling entry). The read step is optional calibration, and the expiry binds only if the preserved set does not cover its inputs ([r2 §16.4](../../notes/2026-09-27-s5-part-a-measurement-proposal-r2.md#164-stage-0)).]*
  - Stage 1a: Windows harness validation.
  - Stage 1b: a new `workflow_dispatch` measurement workflow file, which is a CI-configuration change, and its two-job Linux run.
  - Stage 1c at C3.
  - The host-venv or worker-image choice.

  Also give the total expected runner time and the re-run limit (one per failed validity check).
- **Operator decisions for CP-1a:** *[2026-09-27: superseded by the six decisions in [r2 §14.1](../../notes/2026-09-27-s5-part-a-measurement-proposal-r2.md#141-refreshed-decision-list-2026-09-27), which fold in #519's decisions 1–7.]* #519 proposal §8 decisions 1 and 4 (the rule's parameters, and the measurement steps including host venv versus worker image). Decision 2 (scope) and decision 5 (arithmetic as pre-build feasibility) were **ruled 2026-09-27**. Decision 3 (the `/v7` N2 ceiling) returns as a separate ruling, not under the rule.

**Acceptance conditions for the corrected proposal (operator, 2026-09-27).** Step (a) is not accepted unless both hold.
1. **Stage 1c forces maximum expansion through the built adapter.** The dispatch specifies exactly how the Stage 1c run reaches `expanded_panels` through the S5 adapter's own Part A compute (`compute.run_part_a_compute` or its accepted successor). The run includes the **real N2 FULL baseline derivation from staged N2 capture bytes** and the **real S5-D1 two-artifact writing with its fsync**, all inside the measured workload boundary. Forcing uses a TEST_ONLY measurement override whose existence and scope are stated: which parameter, where it is injected, and proof that no production or signed route can reach it. A harness-level stand-in or a prescribed (non-expanding) arm does not satisfy this. If the adapter cannot be forced without a production-reachable seam, return BLOCKED with the proposed seam.
2. **Complete aggregate-memory evidence.** The memory input is the peak for the whole measured unit, every descendant included: cgroup `memory.peak` / systemd `MemoryPeak` with swap off, taken on each timed repeat. It is compared against the one shared campaign footprint (PA-3). If any repeat lacks it and only a lower-bound fallback exists (`ru_maxrss` of one process, or a Windows working set), **memory feasibility is recorded as UNVERIFIED**, the rule is not applied to that record, and the dispatch says so. A lower bound never satisfies PA-3.

**Step (b) work (after CP-1a only):** execute exactly the approved steps. Then apply the approved rule per #519 proposal §6 as a **provisional** TEST_ONLY ceiling, recorded in a ledger entry. Nothing outside the approval.

**Limits:**
- Step (a) is documentary: no measurement or dispatch, and no edit under `ops/`, `tests/`, `tools/` or `.github/`.
- Step (b): only the approved workflow file and harness files; no profile, ceiling or release-literal edit (those land with the S5 build).
- No production value, ever.

**Stop conditions (b):**
- a PA-4 validity failure twice;
- digests differ between repeats;
- Σ arithmetic fails at every admissible value.

Each of these returns at once; the last is the D2 falsifier.

**Recovery:** measurements are side-effect-free. A failed repeat is retained, never dropped.

**Evidence retained:**
- (a) the corrected proposal revision and the dispatch packet;
- (b) `docs/notes/<date>-s5-part-a-measurement/` in #519 proposal §3.5 schema, with run IDs and records;
- class `TEST_ONLY_SYNTHETIC_REDUCED_DEPTH_NOT_DECISION_BEARING`.

**Decision unlocked:** (a) → **CP-1a**. (b) → RC-3a, and with the other build-entry conditions, **CP-1b** (hold release for the build).

**Step (c), added at the acceptance of step (a) (2026-09-27; owner assigned for the cross-handoff critic's finding X-02):** draft, for the operator's acceptance, the S5 owner text that build entry and C3 need:
- the §3.4(d) text (S5 draft §4 and the consistency correction), a build-entry condition;
- the RC-6 re-anchor of the S5 packet at the release head, carrying #519's findings, the three `/v7` pitfalls and the SR/P set approved at CP-1a (with the SR-7 exception only if approved);
- the RC-2 owner-text set (boundary spec §3.1; full-E1 spec §2.2a, §2.4, §2.5, §2.6 and §5; slices plan contract decisions 3 and 6 and the S5 text), a C3 condition.

Drafting may start now. Owner documents are amended only after the operator accepts the text. The RC-6 re-anchor waits for CP-1a's SR/P decision.

**Grants at dispatch:**
- (a) and (c) coordinator: `repository.read`, `worktree.write`, `governance.author`, `branch.push`, `pr.open`. Acceptance: `make check` clean.
- (b) worker: `repository.read`, `tests.run`, `worktree.write`, `branch.push`, `pr.open`, plus `ci.dispatch` only for the CP-1a-approved workflow. Acceptance: the approved harness's validity checks and `tests/ops/qualification/test_part_a.py` passing unchanged.

### H1 steps (b) and (c): dispatch record (frozen 2026-09-27)

**Instruction.** On 2026-09-27 the operator directed, in session:
- "Continue preparing the approved H1(b) harness and dispatch-only workflow; CP-1a already authorizes that work";
- "Prepare the H1(c) owner-text and RC-6 draft alongside it, returning that draft for acceptance";
- "Keep the ruling PR separate from implementation".

Its follow-up direction: freeze each worker's instructions; treat H1(b)'s checks as preliminary; correct the H8(b) file ownership.

**Frozen inputs** (both steps):
- **Ruling:** the CP-1a ruling at commit `baa09ffd`, the ledger entry "Operator ruling — CP-1a decisions (1)–(6) adopted as recommended, hold kept, 2026-09-27". Each worker reads it as `git show baa09ffd:docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md` while [#523](https://github.com/Joshua-Asante/first-passage/pull/523) is pending.
- **Packet:** r2 at `origin/main` `875ecf29`, including its §16 reconciliation.
- **Branch base:** `origin/main` `875ecf29`.
- **This record:** the commit that adds it. Where the inline worker briefs and this record differ, this record governs.

**Step (b): the harness and the dispatch-only workflow** (branch `claude/h1b-part-a-measurement-harness`; one PR).
- **Allowed files:**
  - the harness directory `docs/notes/2026-09-27-s5-part-a-measurement/`: `measure_part_a_max.py.txt`, the support files r2 names, and a `README.md`;
  - one new dispatch-only workflow under `.github/workflows/`, triggered by `workflow_dispatch` only.

  Nothing else. That excludes any profile, ceiling, release literal, anything under `ops/` or `core/`, and every owner or governance document.
- **Acceptance checks, which are PRELIMINARY: they establish basic tooling behavior only.**
  - `check` exit 0;
  - any workflow inventory or lint tests pass;
  - `py_compile` of the harness;
  - `--help`;
  - `--summarize` on synthetic rows;
  - the diff limited to the allowed files.

  **Measurement readiness is established later, not by these checks**:
  - Windows **Stage 1a** on the operator's host (r2 §12.2);
  - the approved Linux accounting **probe and dry run** (r2 §12.3), including the I-1/I-6 failure handling, unit and artifact cleanup, and the **image-first feasibility** that step (b) records first (CP-1a decision (2)(d)).

  The static image-context inspection is an input to that feasibility, not proof of it.
- **Return boundary:**
  - one ready-for-review PR against `main`, with the status, the files, an r2 requirement map, the image-first finding and what was not run;
  - no measurement, engine run, dispatch, re-run or artifact download;
  - the operator merges.

  The Stage 1a, Stage 0 and Stage 1b execution that follows stays under the CP-1a dispatch approval and its §12.7 caps.

**Step (c): the owner-text and RC-6 draft** (branch `claude/h1c-s5-owner-text-draft`; one PR).
- **Allowed file:** `docs/notes/2026-09-27-s5-owner-text-and-rc6-draft.md` only.
- **Acceptance checks:**
  - the link check reports `bad 0`;
  - `check` exit 0;
  - the diff is only that note.
- **Return boundary:**
  - a DRAFT returned for the operator's acceptance: the §3.4(d) text, the RC-6 re-anchor carrying the CP-1a SR-1..SR-9/P-1..P-7 set, and the RC-2 owner-text set;
  - open questions stay listed, not decided;
  - **no owner document is amended** until the operator accepts the text.

**Exclusions, corrected 2026-09-27.** H8(b)'s deliverable is its classification note, `docs/notes/2026-09-27-h8b-feed-gap-classification.md` ([#524](https://github.com/Joshua-Asante/first-passage/pull/524)). Neither step touches it. The feed-preparation note and the feed-equivalence spec draft are **not assigned to the H8(b) worker**. They stay out of both steps because they are outside scope. Any edits to them are follow-up owner work, assigned separately. Status rows in this handoff set are coordinator-owned; neither worker edits them.

**Amendment 2026-09-27: step (b) re-opened narrowly by operator ruling.** The operator ruled on the returned harness. The ruling, quoted in full, and the contract text it produced are [r2 §12.9](../../notes/2026-09-27-s5-part-a-measurement-proposal-r2.md#129-operator-ruling-2026-09-27-completion-fields-legacy-bundles-and-incomplete-stage-1b-evidence). This amendment changes step (b) only. Where it and the step (b) text above differ, it governs.
- **Allowed files:** the three step (b) files, plus **one new regression module, `tests/test_s5_part_a_measurement_harness.py`**. The module loads the harness from its `.py.txt` path and exercises it on synthetic inputs only. It has no private reads, vendor data, engine run or network, and imports nothing from `lab/`. Nothing else under `tests/`, and no other file.
- **Implementation:** r2 §12.9 items (1)–(6). This covers:
  - the explicit completion fields;
  - the retained `LEGACY_UNACCEPTED` bundles;
  - the Stage 1b `INCOMPLETE_EVIDENCE` verdict with exit 3 and `rerun_eligible`, inside the single `--failed` re-run;
  - record generation, owned cleanup and artifact upload still running after an exit 3;
  - Stage 1a and dry runs never rule-applicable;
  - the schema additions.

  The README states the same rules.
- **Acceptance, replacing the PRELIMINARY checks for this revision:**
  - **The regression suite is committed.** All 75 regression tests move from the scratchpad into the module, with any fixture changes the ruling needs. Passing scratchpad tests alone is **not** acceptance.
  - **Exit semantics are exercised through the real summarizer.** New tests run the harness's `--summarize` and combine entry points as a subprocess on synthetic record directories, and assert the exit code and verdict for each of:
    - a Stage 1b job and a combined record missing a ceiling input on each arm in turn (`INCOMPLETE_EVIDENCE`, `rule_applicable = false`, exit 3; `rerun_eligible` true on attempt 1 and false on attempt 2);
    - a complete Stage 1b record (exit 0, rule-applicable);
    - a Stage 1a bundle without complete aggregate memory, which passes its own checks, exits 0 and is never rule-applicable;
    - a dry run that meets its own requirements (exit 0, never rule-applicable);
    - a legacy bundle (`LEGACY_UNACCEPTED`, exit 4, the file unmodified);
    - a missing completion field (I-6).
  - **Workflow check.** A test or static check shows that the workflow's record-generation, cleanup and upload steps run after the summarize step exits 3 (`if: always()` or equivalent), and actionlint passes.
  - **Records.** These run through the launcher on the final head, each with `status: completed`, exit 0 and `source_stable: true`:
    - `python -m pytest tests/test_s5_part_a_measurement_harness.py -q`;
    - the same command with `--workers 2`;
    - `check`.

    The before-state is also recorded: the new module against the harness at `b55958c8` fails on the ruling's new cases.
  - **Diff:** the four allowed files only.
- **Evidence retention before any measurement execution.** The coordinator archives each record directory in `first-passage-archive` by content address and registers the pins in `docs/evidence/PRIVATE_EVIDENCE.sha256`. It records the archive commit, and the H1 row cites them.
- **Unchanged:** no measurement, engine run, workflow dispatch, re-run or artifact download. The operator merges. S5 stays **HELD**.

**Unchanged:** S5 stays **HELD** until RC-3a and the remaining build-entry requirements support CP-1b.

## H2 — Route commissioning session packet (operator-run, automation disarmed)

**Uncertainty resolved:** what the exact route actually does, one micro contract at a time, for:
- an entry carrying its stop;
- the stop `Working` at the filled quantity;
- a cancel of a resting entry and its children;
- a rejected change;
- the normal case of whole-leg liquidation (C-a, investigation only);
- same-session and prior-session reconciliation reads.

**Prerequisites and existing authorization:**
- Gate A accepted (REST §6.11).
- The [drill plan](../../notes/2026-09-26-tradeify-route-drill-plan-draft.md) owns the rows. This packet sequences them and does not become a second owner.
- [Incident ADR §A11.1](../../adr/2026-09-17-bounded-platform-protection-incident-contract.md#a111--operator-ruling-close-direction-2026-09-26) authorizes R-1/R-2 only, once entitlement is confirmed. It requires each order-producing row to be prepared individually with its environment, actions, exposure limits and abort/recovery. The race drill X-5 is deferred. There is no automatic fallback to the live eval.
- **Consumed, not redone:** the #519 close-semantics return. M questions and §1.1a (a)–(e) are all OPEN or CONFLICTING. It also supplies the draft vendor question (note §6), two actor-inventory candidates (the platform timed exit and firm-side auto-liquidation), a packet §1.1 wording correction, and the X-3 read addition.

**Work:** write `docs/notes/<date>-route-commissioning-session-packet.md`.
- **Stage 0 (read-only; before it: CP-2):**
  - host confirmation that the rail is disarmed (`dry_run=true`, `emit_enabled=false`);
  - the §0.1 actor inventory as a checklist, with every Account Manager function disabled (CR-12) and #519's two candidates added;
  - the entitlement record;
  - the known-order confirmation;
  - R-2 and the T07 reads on a completed preservation trade where it meets their evidence requirements;
  - R-1 only in the same session as a preservation trade the operator places anyway (addendum §1.3).
- **Stage 1 (order-producing; before each row: its own CP-3 written authorization):**
  - X-1, X-4 and X-2 (the last after M2).
  - X-3 only as part of the operator's residual-risk decision (CR-3), because #519 left M OPEN/CONFLICTING. It includes #519's X-3 read addition.

  Each row gets:
  - its environment;
  - exact actions;
  - one micro contract per request and in total, with the stop in the same request;
  - placeholders for the operator-fixed stop distance, time in market, window and cost ceiling (no figures in the repo);
  - its stop conditions;
  - the drill plan's five-step recovery;
  - its evidence entries.
- **Session rule:** one row at a time; its traces return and are reviewed before the next row is authorized.
- **Operator-sent text:** #519's vendor-question draft, and the one permitted T08 follow-up. Vendor contact is the operator's.
- **CP-2 fact list:** entitlement, sim/demo availability, the known-order definition and read target, whether drill costs count against the $700 ceiling, and preservation-trade treatment (drill plan q9, OPEN).

**Limits:**
- Documentary only: no account access, vendor contact, order or figure.
- Nothing wider than the drill plan's one-contract limit.
- X-5, C-b rows and the GC-5 takeover composite are excluded.

**Stop conditions to write into the packet:**
- any `unknown` outcome: no resend, read first;
- a stop not `Working` at quantity 1 within the wait;
- an unexpected position or working order;
- competing-actor activity;
- a rail state other than disarmed;
- the time limit reached.

**Evidence retained:**
- the packet itself;
- after a session: original bytes under the drill plan's private manifest (hashes only in the repo), plus one outcome line per step, recorded against CAP R2–R5 / T08 §7 behavior rows as `COMMISSIONING_OBSERVATION` with scope.

**Decision unlocked:** **CP-2**, then **CP-3** row by row. Reviewed traces support capability acceptance for their scope and feed CP-5.

**Grants at dispatch (coordinator):** `repository.read`, `worktree.write`, `governance.author`, `branch.push`, `pr.open`. Acceptance: `python scripts/check_handoff_authority.py --all` and `make check` clean on the branch.

## H3 — ORB lifecycle and fence: disposition, owner text for Ruling 7, H4 card

**Continues:** the #519 ORB lifecycle evidence and four-state trace at `8c15f18`, each "ACCEPTED AS INPUT". No new source read or trace. The decisions are made ([§59 Ruling 7](../programs/2026-09-03-seven-strategy-select-campaign-state.md#ruling-7--orb-lifecycle-l1-reaffirmed-and-the-account-fence-classification-contract-2026-09-27): L1 with the earlier operational cutoff, and the fresh-evidence classification contract).

**Uncertainty resolved:** the exact owner text that implements Ruling 7, and a bounded, verifiable repair card.

**Prerequisites and existing authorization:** Ruling 7, which authorizes "the bounded synthetic repair and corresponding specification/replay corrections, retaining real-producer and route acceptance obligations".

**Work:**
1. **Coordinator disposition.** For each lifecycle-note conflict C1–C5 and each trace defect and ambiguity, record whether it is resolved by Ruling 7 or still open, with the owner.
2. **Owner text, applied as dated amendments under each owner's own convention:**
   - **Rail spec:** the §1 `pending` clarification (trace §6.1) worded to Ruling 7(b). S2's one-bar sentence per L1. S4's "stale resting entries" and AC-8 aligned to L1. The halt/resume §5 cutoff overlay is unchanged.
   - **Replay spec:** RC-9 amended so the one-bar cancel does not end ORB's base entry. RC-4's parity basis is kept.
   - **Edition pre-registration:** ORB-1 states the L1 lifecycle in words (it is DRAFT, with a dated marker).
   - Where #519's §6.2 text and Ruling 7(b)'s "stale at one bar" differ at the boundary, **the ruling's words govern**. The divergence is recorded, and the boundary is pinned as the ruling states it.
3. **H4 dispatch card,** in its own file with its `yaml authority` block:
   - **Scope:** trace §6.2–§6.4 against the synthetic seam, plus the qualification replay correction (`replay.py:507-509` and its pinned test), as separate checkpoints.
   - **Owed items:** the real evidence producer, route integration and the ordinary-unknown halt (packet CC-3; T09/TB-I3).
   - **Freeze-inventory effect** of the replay change.

**Limits:**
- No code change.
- No private source read.
- No wording beyond what Ruling 7 decides. Any extra choice (for example strict versus inclusive, if the ruling's words leave it open) is returned, not made.

**Stop conditions:**
- An owner's change-control forbids the amendment form.
- Ruling 7 does not decide a point the text needs.

In either case return with the question.

**Recovery:** not applicable (documentary).

**Evidence retained:** the disposition note, the owner-text diffs and the H4 card, citing `8c15f18` line anchors.

**Decision unlocked:** coordinator acceptance of the owner text and the card, which makes H4 dispatchable.

**Grants at dispatch (coordinator):** `repository.read`, `worktree.write`, `governance.author`, `branch.push`, `pr.open`. Acceptance: `make check` clean and `python scripts/check_handoff_authority.py --all` clean.

## H4 — Fence classification: synthetic repair plus the ORB L1 replay correction

**Uncertainty resolved:**
- Whether the owner and its consumers classify and act on states (i)–(iv) as Ruling 7(b) says, before any real producer exists.
- Whether the qualification replay keeps ORB's base entry working per L1.

**Prerequisites and existing authorization:** Ruling 7, which authorizes the bounded synthetic repair and the replay correction. H3's owner text and this card's final form must be accepted by the coordinator before dispatch.

**Work, in two checkpoints returned separately:**
- **(F) Fence**, tests first. Cover trace §6.4 cases 1–12 as Ruling 7(b) words them:
  - stale at one bar, pinned;
  - a positive lookup does not resolve state (iii);
  - terminal evidence resolves only the request it covers;
  - refreshed evidence never restores permission after a halt.

  These run against the `SyntheticBroker` seam with synthetic evidence acquisitions. Then the change in `book_account_owner.py` and each traced consumer: admission, loosening amends (`book_protection_owner.py`), takeover fence and quiescence (`book_takeover_owner.py`), with the unchanged consumers re-pinned. The pinned behavior at `tests/ops/test_book_feedback_journal.py:41-55` changes only as the ruling requires, and is listed explicitly.
- **(R) Replay:** correct the one-bar cancel so ORB's base entry follows L1, with `test_replay.py:214-223` re-pinned and parity with the emulator shown. This is an E1 freeze-inventory change. Its record goes to the freeze inventory, and qualification Linux evidence is refreshed as the coordinator directs.

**The return must separate:**
- **(1) Verified synthetically:** classification and consumer behavior per case, and the replay correction, each with node IDs.
- **(2) Still owed:** production of real order-level evidence (the producer), route integration, and the rev9 halt for ordinary unknowns (T09/TB-I3). It must also state that **the fence obligation is not resolved** until (2) is accepted.

**Limits:**
- No production transport (T09).
- No `lab↔ops` import, locked parameter or DD constant.
- No private port run.
- Branch and PR; the operator merges.

**Stop conditions:**
- a consumer the trace missed;
- a needed change outside the owner, its consumers and the replay;
- an emulator-parity break.

In each case return to the coordinator.

**Recovery:** a branch revert. No shared state is touched.

**Evidence retained:** the node IDs per case, the launcher `record.json`, `make check`, and the replay's before/after parity record.

**Decision unlocked:**
- The synthetic half of the fence obligation and the replay correction are accepted before the freeze inventory is fixed.
- Both are input to **CP-5**.
- The remaining half is named in T09's scope.

**Grants at dispatch (worker):** `repository.read`, `tests.run`, `worktree.write`, `branch.push`, `pr.open`. Acceptance: the node set named in H3's card.

## H5 — Attended operations: apply the resumption ruling, then synthetic incident rehearsal

**Uncertainty resolved:**
- (a) The halt/resume owner text that implements §A11.2.
- (b) Whether alerts, escalation, heartbeat, fencing, manual intervention and restart behave as ruled, tested with synthetic incidents.

**What is ruled:**
- [§A11.2](../../adr/2026-09-17-bounded-platform-protection-incident-contract.md#a112--operator-ruling-no-same-session-restart-of-automation-after-an-incident-2026-09-27) (2026-09-27): for commissioning and the first attended release, an incident ends automated trading for that session. Operator recovery and evidence collection continue, and review comes before another session. It applies to incidents, not to correctly handled signal or capacity refusals.
- §A11 items 1, 2 and 4 stand.
- Rev9 §4's conditional same-session resumption remains the text for other contexts. The ruling does not decide later releases.

**Work:**
- **(a)** A dated amendment to the [halt/resume contract](../../spec/2026-09-14-tb-s3-halt-resume-contract.md) §4 applying §A11.2 to those two contexts, following that contract's amendment convention. Also a pointer in the [Phase 5 plan](../../superpowers/plans/2026-09-16-phase5-attended-operations.md) stating that its proposed restriction is now ruled for these contexts. Then a step (b) dispatch card with its `yaml authority` block.
- **(b)** After (a) is accepted: a synthetic incident script (lost response, stale evidence, missed alert, restart during halt, ambiguous protection). Show that no automation restart path exists within the session after an incident, including a deliberate operator stop (O-6), and that a correctly handled refusal does not end the session. *Amended at acceptance 2026-09-27 (cross-handoff critic X-06):* real delivery and 60 s escalation are measured in T13 (Phase 5 WP2). The exception is if the operator runs the delivery leg on an existing, no-spend channel at dispatch.

**Limits:**
- No rail deploy or arm, and no account traffic.
- A notification channel that needs spend or a new account returns to the operator before use.
- (a) adds no rule beyond §A11.2.

**Stop conditions:** any path that restarts automation in the same session after an incident, or that ends a session on a correctly handled refusal. Stop and return; it is a defect.

**Recovery:** rehearsal state lives in disposable stores and is discarded after its evidence is retained.

**Evidence retained:** (a) the owner-text diff and the (b) card. (b) Delivery and escalation timing traces, restart and restore traces, and the incident-versus-refusal cases.

**Decision unlocked:** (a) → coordinator acceptance, then (b). (b) → T13 construction, with H2's commissioning traces folded in before any session that could produce an unresolved request.

**Grants at dispatch:**
- (a) coordinator: `repository.read`, `worktree.write`, `governance.author`, `branch.push`, `pr.open`.
- (b) worker: `repository.read`, `tests.run`, `worktree.write`, `branch.push`, `pr.open`.
- Acceptance for (b): the rehearsal test nodes named in the (b) card.

## H6 — Settlement collection and reconstruction rehearsal

**Uncertainty resolved:**
- Actual report coverage.
- The three S2 source facts: the `Timestamp` offset, the `Date` meaning after the rollover and the query-bound semantics ([CAP addendum 2026-09-24](../phase4-preparation/2026-09-16/capability-decision.md)).
- Missing-data detection.
- Whether the verifier and account owner reconstruct an anchor and a subsequent close from original bytes.

**Prerequisites and existing authorization:**
- The 2026-09-25 account-side read authorization (T07).
- The target is ruled ([incident ADR §A11.3](../../adr/2026-09-17-bounded-platform-protection-incident-contract.md#a113--operator-ruling-preservation-trade-evidence-as-the-target-of-authorized-reads-2026-09-27), 2026-09-27): a completed operator-placed preservation trade, where it meets the reads' evidence requirements, in place of the D1 transaction. CP-2 confirms the transaction identity. A completed trade cannot supply a new same-session observation. No additional trade is authorized.
- The rehearsal harness may be prepared before CP-2.

**Work:**
- **Operator collection.** Report originals covering the target transaction, with the report context captured: timezone setting, query bounds, and a row after the rollover. Stored in the private root and hashed into its manifest.
- **Agent rehearsal**, on the operator's machine for private bytes:
  - isolated anchor ingestion and a subsequent-close ingestion;
  - correction refusal and restoration;
  - a missing-data case;
  - the time the procedure takes.

**Limits:**
- Read-only exports; no account reset; no API use while API entitlement is unverified.
- Private bytes never committed.

**Stop conditions:** an unsupported decisive source fact. Return promptly and continue only independent collection (T07 checkpoint).

**Recovery:** the rehearsal stores are disposable. No silent predecessor reset.

**Evidence retained:** manifest hashes, consumer traces with record IDs, and the timed procedure. CAP S1/S2 rows are proposed for coordinator acceptance.

**Decision unlocked:**
- The S3/B7 predecessor decision.
- The requirement for an operator-facing sign/submit entry point, scoped to T09 or tooling.

**Grants at dispatch (worker, for the harness):** `repository.read`, `tests.run`, `worktree.write`, `branch.push`, `pr.open`. Acceptance: the reconstruction consumer test nodes named at dispatch. Collection is operator-performed.

## H7 — Production qualification host: specification and OF assignment

**Uncertainty resolved:**
- Who verifies each of OF-1..OF-7, at which gate, and where the record lands (RC-5).
- Which gate set governs OF-5..OF-7 (S5 draft §6 Q12).
- The owner and slice of the client plan-view seed change (RC-4).
- What a production-class host needs, and what it costs.

**Prerequisites and existing authorization:** the 2026-09-26 direction to "assign seed-view implementation and host attestations to their specified gates". The seat does not choose the owner itself; it proposes.

**Work:**
- **Proposed owner text.** Recommend the stricter reading of Q12: every OF at provisioning, before any production-authority release and after any access change, plus the specific OF-5/OF-6/OF-7 gates.
- **Host specification:**
  - OS and cgroup v2 / systemd features;
  - the `qclient`/`qexec`/`qg5`/`qseal` principals;
  - key storage and custody;
  - enrollment inputs;
  - K3 salt custody.
- An itemized cost line if provisioning needs spend.
- A named slice for the RC-4 seed view, with its F1 admission check.

**Limits:** documentary only. No host rental, credential creation or key generation.

**Stop conditions:** an OF that cannot be verified by an attended read. Return it as a contract question.

**Recovery:** not applicable.

**Evidence retained:** the proposal note and the owner-text diffs, pending acceptance.

**Decision unlocked:**
- The RC-4/RC-5 assignment, which is a build-entry condition for S5 (ledger 2026-09-27). The implementation and the attestations stay before F1. *[Corrected 2026-09-27: the implementation stays before F1; the attestations fall due at the RC-5 gates: OF-7 before F1 admission, the full OF-1..OF-7 set at CP-8 (ledger RC-5 entry).]*
- Later, **CP-8**: provisioning and admission.

**Grants at dispatch (coordinator):** `repository.read`, `worktree.write`, `governance.author`, `branch.push`, `pr.open`. Acceptance: `make check` clean.

## H8 — Feed: provider-neutral preparation

**Uncertainty resolved:** what the funded provider must satisfy for all four symbols before trading use, stated before any provider is chosen.

**Prerequisites and existing authorization:** STATE's source disposition, which allows provider-neutral preparation. D-feed bars signup, subscription and credential staging.

**Work:**
- The TB-I5 successor, a CME execution-feed equivalence test specification (no such spec is on disk).
- Symbol, roll and session mapping for the four legs.
- Gap, reconnect, correction/backfill, duplicate/out-of-order, stale-symbol and DST/early-close handling, specified against the canonical panels.
- The **later-binding rule** text for the F1 packet (addendum §1.4).
- A shadow-collection design with emission disabled.

**Limits:** no provider contact, account, credential or spend. No equivalence tolerance set after seeing data.

**Stop conditions:** a requirement that only a specific provider can answer. Record it as a funding-decision question.

**Recovery:** not applicable.

**Evidence retained:** the spec drafts and the rule text.

**Decision unlocked:** inputs to **CP-7** (funding) and to the T10 phase-2 F1 packet.

**Grants at dispatch (coordinator):** `repository.read`, `worktree.write`, `governance.author`, `branch.push`, `pr.open`. Acceptance: `make check` clean.

**Step (b), added at the acceptance of step (a) (2026-09-27; owner assigned for the cross-handoff critic's finding X-05).**
- **What:** classify the private gap queue (`calendar-gap-queue.json`, digest `509346d6…`; execution domain `:485–:502`) against the consumer's contiguity and four-leg barrier rules (`book_runtime.py:376–:391`). That includes the 171 residual regular-session gaps (`:689–:691`): are they no-trade quiet slots or missing input?
- **Where:** documentary, run on the operator's machine, because the queue is private. No data is committed; only counts, classes and digests return.
- **Returns to:** the operator, for the spec §4.3 empty-interval rule. If an omitted in-session slot would halt the book, it also goes to TB-I3 and to the halt/resume owner (the §A11.2 incident question).
- **When:** before CP-6.
- **Grants (coordinator, on the operator's machine):** `repository.read`, `worktree.write`, `governance.author`, `branch.push`, `pr.open`. Acceptance: `make check` clean.

**Step (b) acceptance (2026-09-27).** Step (b) is ACCEPTED as a documentary classification. The return is [PR #524](https://github.com/Joshua-Asante/first-passage/pull/524), merged at `a1a3c3e`. The acceptance establishes the classification result: one observed affected permitted session in the reconciled common window, and 170 of the 171 residual gaps on holiday account days. It does not settle the cause of the omission, give a rate, or qualify a live feed ([note](../../notes/2026-09-27-h8b-feed-gap-classification.md#coordinator-acceptance-2026-09-27)). Carried forward:
- **Q-1:** PROPOSED text in the draft equivalence spec §4.3. The operator adopts it at freeze, before CP-6.
- **Q-2:** parked until an exchange record or an independent source can corroborate the event.
- **Q-3 and Q-4:** ruled by the operator on 2026-09-27, in session. The ruling is recorded in the [halt/resume contract §4.1](../../spec/2026-09-14-tb-s3-halt-resume-contract.md#41-amendment-2026-09-27-incident-versus-correctly-handled-refusal), *Qualifications*.
- **Outstanding:** a later-session re-arming design, for TB-I3 and the resume decision. No handoff builds it now.

**Step (c), added at the acceptance of step (b) (2026-09-27).** [Worker card H8(c)](2026-09-27-h8c-omission-incident-session-end.md) verifies the omitted-slot ruling against the existing owners, synthetically. It covers three things:
- the three omission detectors, and the late-bar regression kept separate;
- recovered bars, repeated activation and a reopened journal, through real entry points only;
- duplicate ids kept distinct from separate detector records.

The card changes no production code and invents no resume interface. It is READY ON its own merge and on #521's. The coordinator keeps acceptance of its results.

## H9 — Result/seal integration and bounded same-sample recovery (two checkpoints)

**Uncertainty resolved:** whether S1–S5 and the frozen T05 build hold as one integrated identity under interruption and exhaustion. Two checkpoints, returned separately. The coordinator keeps combined acceptance.

**Prerequisites and existing authorization:**
- **Integration preparation:** S5 Checkpoint C3 accepted (the PART_A field sets, the `/v8` snapshot and the capture contract are stable), and the existing T05 build acceptance.
- **Carried obligation (operator, S5 C3 step 1, 2026-09-29):** B4 was accepted for TEST_ONLY only. Strengthening pilot identity from plan agreement to an independently observed pilot draw is **due with T05, before CP-6**. The T05 integration owner tracks it ([ledger](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md)).
- **Checkpoint R1, integration acceptance:** full S5 acceptance. *2026-10-01:* also **both D-S5 fix slices merged, each with its own full S4-plus-Part-A Linux run read ok and its own acceptance: #586 (D-S5-1/D-S5-2), then the D-S5-3 slice from `claude/capture-retry-noop`**, and the integration branch rebuilt on a `main` that includes it ([defects ruling](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--land-s5-with-two-named-test_only-defects-fix-before-t05-2026-10-01) · [D-S5-3 ruling](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--d-s5-3-capture-exact-retry-demotion-also-gates-t05-r1-2026-10-01)). This is the existing dependency ("Integrate the frozen head `6cf2732` after S5 acceptance"); it is not replaced.
- **Checkpoint R2, recovery-slice acceptance:** the D3 owner text (S5 draft §3.4) accepted, and R1 accepted.

**Work:**
- **Preparation**, from S5 C3: a branch integrating `claude/t05-result-seal@6cf2732` onto the S5 head, with the interface diff:
  - unify `_settlement_terminal`;
  - take main's `031d79a` roll, "never a fresh one";
  - seam row 11: the real seal principal and its host-provisioning change.

  No acceptance-grade run until S5 is accepted.
- **R1:** re-base the prepared integration on the accepted S5 head *(2026-10-01: that is, on a `main` that includes both the S5 landing (#578) and the merged D-S5 fix slice)* and run the acceptance-grade Linux result/seal node set. Return it on its own.
- **R2:** the D3 slice (R1–R10). The recovery retains every failed attempt and never renews the allowance or deadline. It allocates no attempt ID, salt, seed or plan, and makes no public reveal while recovery remains possible. Return it on its own.

**Limits:**
- No production authority, no route-enabling release literal before T06, and no accepted formula or tolerance change.
- No push while a Linux run is in flight.

**Stop conditions:**
- An integration conflict that changes an accepted interface.
- An S5 change after C3 that invalidates the prepared branch.
- Any path that redraws or renews allowance.

In each case return to the coordinator.

**Recovery:** branch-level only. Retained attempts are never deleted.

**Evidence retained:**
- R1: Linux qseal and result-G5 cases, and exhaustion and receipt-history cases (a receipt is history, not authority), plus Windows lines and `check`.
- R2: interruption and retry cases, retained-attempt history, and the no-renewal assertions.

**Decision unlocked:** R1 and R2, each accepted separately, then the coordinator's combined acceptance and T06/S8 dispatch on one identity.

**Grants at dispatch (worker):** `repository.read`, `tests.run`, `worktree.write`, `branch.push`, `pr.open`. The coordinator holds `ci.dispatch` for the Linux runs under its own grants. Acceptance: the R1 and R2 node sets named at each dispatch.

## H10 — Final launch: exact-candidate rehearsal and one attended session (LATER)

**Recorded now so it is not rediscovered:**
- The timed rehearsal runs on the exact T16 candidate with synthetic inputs: B7 capture → sole n3 → verdict/expiry/void rules → GO/reseal → restart → activation acknowledgment.
- Deployment GO and initial-session authority are separate operator acts at **CP-9**.
- The session is one attended session under preserve-and-block. Explicit review follows before any extension (§A11 item 1).
- Failure leaves the candidate disarmed or halted as prescribed. Elapsed time is never approval.
- The card is written when T16 is accepted.
