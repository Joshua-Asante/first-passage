# GLM handoff — Protected Full E1 / S2 acceptance continuation (finish G3 + G4, integrate, Codex, accept PR #436)

**Type:** cc_handoff (continuation; coordinator-authored, operator-dispatched)
**Date:** 2026-09-20
**From:** the Claude coordinator session that resumed after GLM's first continuation (its state is the ledger entry "GLM continuation — S2 integration return, 2026-09-20" and the three entries after it in `docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md`).
**Status:** dispatch now. The operator stopped two in-flight Claude workers mid-task and handed the remainder to GLM. Their partial work is pushed; nothing is lost, nothing is verified.
**Authority:** implementation, tests, harness cases, the two packets' §7 sections, the integration branch `claude/s2-enforcement-gaps-fab5e6` and PR #436, and the ledger **return** entry. Not authorized: S2 acceptance itself (coordinator/operator writes the acceptance entry after reading your return), merge of #436, any S3 work, allowance/ceiling/profile/release/snapshot/DB version changes (a needed version bump is a `CHECKPOINT` back to the coordinator with the smallest change and its blast radius), production activation. A `DONE` status supplies no permission.

## 0. Read first (in this order)

1. `CLAUDE.md`.
2. `docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md` — the S2 slice, then every ledger entry from "Coordinator checkpoint — S2 enforcement gaps (G1/G2), 2026-09-19/20" to the end.
3. `docs/notes/audits/2026-09-20-pr436-s2-integrated-acceptance-review.md` — the independent acceptance review: VERIFIED WITH CAVEATS, 0 BLOCKING / 9 ADVISORY / 10 NOTE. A1, A2, A4, A5, A7, A9-3 are being repaired (below); A3, A6, A8 are S3 preconditions the acceptance entry will record — do not repair them.
4. `docs/briefs/handoffs/2026-09-20-full-e1-s2-g3-resume-before-exec.md` — the root cause of the 14/15 on run 35494972519 (the guardian's SIGUSR1 resume kills runc's Go init when it lands before `execve`; second defect: no exit code retained on the non-credited path) and its frozen repair; plus the coordinator addendum sent to the worker (folded into its commit): **A2 guardian half** (transition IN_DOUBT before settling a non-credited non-zero exit; update `test_nonzero_probe_exit_settles_without_completion`) and **A4** (in the poll-loop authority read only, treat the funding-pending `ValueError` as re-poll, bounded ~5 s; never relax `_assert_authority` for VOID/recovery/dispatch, never touch the `_transition` path).
5. `docs/briefs/handoffs/2026-09-20-full-e1-s2-g4-store-invariants.md` — the five store-side rulings (A1 terminal-but-VALID VOID authentication without a charge object; A2 store refusal of CAPTURED/SIGNING_INTENT/COMPLETED after settlement; A5 store-side payload-identity precondition + integrity rule; A7 `reserve_work`/feasibility consult the charged projection; A9-3 work-id prefix validator).
6. The G1/G2 packets (`…s2-g1-supervisor-enforcement.md`, `…s2-g2-service-metering.md`) §0.5 defaults and §7 returns for the designs you are extending.

## 1. State you inherit (verified by the coordinator at hand-off)

| Branch | Head | State |
|---|---|---|
| `claude/s2-enforcement-gaps-fab5e6` (integration, = PR #436) | `03ef76a` | fifteen-green on runs 35487909157 / 35489657203 / 35493582848 (code-identical heads); 14/15 on docs-only `4281d2e` (run 35494972519, root-caused); carries the G3/G4 packets and the review note; PR is open, not draft, mergeable, **no Codex review yet** |
| `claude/s2-g3-resume-before-exec` | `0ba2775` | worker's single commit, message says it implements the packet + the A2/A4 folds (`campaign_supervisor.py` +158/−?, `test_campaign_supervision.py` +290, `test_campaign_supervision_linux.py` +67). **Stopped before §2.6 Windows verification; nothing run; no Linux run; §7 empty.** Treat every claim in that commit message as unverified. |
| `claude/s2-g4-store-invariants` | `8c764d8` | coordinator-pushed WIP commit of the worker's uncommitted edits (`campaign_store.py` +151, `campaign_budget.py` +23, `campaign_funding.py` +8; **no tests written, hooks bypassed for the WIP commit**). The worker was stopped mid-rewrite of `claim_void_authentication` ("the three-way outcome": charged / uncharged-terminal / refused). Expect it to be incomplete and possibly non-compiling. |

Both branches are off `03ef76a`/`915035c`; G3 touches only guardian-side files, G4 only store-side files — they should merge cleanly except possibly `invariant_manifest.json`/shared test helpers.

## 2. Work (in order)

1. **Finish G3.** Read the diff against `915035c` critically, then run its packet §2.5: G1-packet §2.6 lines 1–2 through `./fp.ps1` (zero skips in line 1), `git diff --check`, then ONE S2 workflow run on the branch (`gh workflow run qualification-s2-supervision.yml --ref claude/s2-g3-resume-before-exec`), fifteen green required. Verify the specific claims: resume sent only when the observed init pid's `/proc/<pid>/exe` (or `comm`) is the exec'd interpreter; `comm`/`exe` retained in PROCESS and RESUMED; `PAYLOAD_EXIT` retained on every settlement path; IN_DOUBT before settlement on the non-credited exit; bounded funding-pending tolerance in the poll read. Fill in the packet's §7.
2. **Finish G4.** Complete the five rulings per its packet §1 with Windows regressions for each (the WIP has none), packet §2 verification, one S2 run, §7. If a ruling cannot be met without a version bump, stop that item and return `CHECKPOINT` for it while finishing the others.
3. **Integrate:** merge G3 then G4 into `claude/s2-enforcement-gaps-fab5e6` (resolve `invariant_manifest.json` by semantic union if it conflicts; verify each side's owned files byte-identical to its branch head after the merge), run G1-packet §2.6 lines 1–3 + `check` on the merged tree, push. The push fires the S2 workflow on PR #436: fifteen green, `invariants.json passed`, cleanup ok, `source_stable=true` required; download the artifact and read it — do not trust the check mark.
4. **Codex review:** confirm whether Codex reviewed #436 automatically after your push; if not, trigger it the way this repo does (a PR comment; see PR #429/#434 history) and fold or explicitly disposition every finding in a ledger note (the "LLM-reviewer fold loop needs a stopping rule" lesson applies: after two rounds, stop folding and triage).
5. **Ledger return:** append "GLM continuation 2 — S2 acceptance candidate, 2026-09-20" with: G3/G4 dispositions and records, the merge SHA, the integrated run ID/record, Codex dispositions, and an explicit list of the review advisories closed (A1, A2, A4, A5, A7, A9-3) vs recorded-for-S3 (A3, A6, A8). Do not write "S2 ACCEPTED"; that is the coordinator's/operator's entry. Update the memory-relevant facts in the PR #436 description (it still says "G1 in progress").

## 3. Rules that bind you
- Root-cause before re-running: a failed Linux case on unchanged code is a finding, not flakiness. The artifacts are complete (journal.log, kernel.log, systemd-units.log, `boundary/journal.sqlite`); the 14/15 was diagnosed entirely from them.
- Never relax a Linux assertion to get green; never `xfail`/`skip`; never describe Windows/mock results as Linux evidence; never claim S2 acceptance.
- No `git stash`; `git diff --stat` before every commit; capture pytest exit codes (exit 4/5 is not a pass); if the pre-commit gate's child Python fails to start, `PATH=/c/Python314:$PATH`.
- Keep the tree frozen while a verification record is open (the recorder hashes it).
- The isolation bridge `tests/ops/test_qualification_isolation.py` exceeds its 1800 s limit on this box — the child selection in §2.6 line 3 is the substitute; say so, do not claim the bridge.

## 4. Return
One message: status (`RESOLVED` = steps 1–5 done and the integrated run is fifteen green; `DONE_WITH_CONCERNS`; `CHECKPOINT`; `BLOCKED`), the table above updated with final heads, every record and run ID with counts, the list of advisories closed vs deferred, and anything you disagree with in the rulings (say why; do not silently deviate).
