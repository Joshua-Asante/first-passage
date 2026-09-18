# Combined PR425 verification, 2026-09-18

Selected outcome: integrate the qualification foundation and protected synthetic N1 route, close the observed lifecycle/CI findings, run actual two-host execution-boundary acceptance, obtain independent integration review, and make PR425 ready. PR415 is closed without merging; PR425 against main is the combined review unit. No production qualification, full E1 PASS/seal, deployment, or merge is authorized by this result.

Prerequisites and ownership: coordinator checkout `qualification-fault-verification` starts from PR425 head6590b61. Separate CI and invariant handoffs supply reviewed commits; combined acceptance remains with the coordinator. Preserve the original dirty structural-closure checkout and unrelated main-checkout work.

Verification and return boundary: operations launcher doctor/Python, combined qualification regressions and repository checks, hosted pytest/pylint/image checks, and both actual TEST_ONLY execution-boundary jobs must finish. Review findings must be addressed before draft removal. Required hosted evidence includes actual stop readiness, confirmed cgroup OOM, interrupted launch/capture, approval expiry, exact retries, immutable archives, invariant execution reports and successful owned cleanup. Return the open ready PR, not a merge or production acceptance claim.

| Finding or related case | Disposition |
|---|---|
| Stop marker buffered by supervisor | Per-chunk flush at shared capture owner; failing live-log regression then green. |
| Old host2 exit137 without OOM flag | Remains unconfirmed historically. New bounded256MB TEST_ONLY fixture requires OOMKilled and ordered OOM/die evidence. Run35302983875 passed19/19 on each host with exact-container kernel memcg OOM evidence. |
| Crash between archive link and temporary unlink | Serialized atomic rename preserves single-link object; real child death before/after publication and concurrent publishers verified. |
| Retry and newly created archive directory durability | Root and parent directory fsync before returning object identity; retry repeats fsync. |
| Incomplete/dripping RPC peer | Bounded16-handler dispatcher plus absolute frame deadline; journal uses separate per-thread connections. Real partial-peer test included in Linux inventory. |
| VOID races with first publication/commit | Separate SQLite writers exercise both durable orders; exact historical receipt remains authoritative after VOID. |
| Actual process interruption and stale approval | External TEST_ONLY trace driver stops genuine supervisor before container recording, before daemon start, and after output EOF; no injected outcome/journal changes. Expiry case deliberately permits a late Docker start and verifies rejection of execution authority. |
| Daemon/listener image dependency closure | Both include canonical policy modules; image inventory regression includes relative imports. |
| Linux credential schema regression | Private fixture uses protected home ancestry so wrong-schema assertion reaches schema validation. Production custody checks unchanged. |
| Pylint imports | Reads canonical pytest roots; existing8.0 threshold and diagnostics unchanged. Windows full lint could not print Unicode; Linux score required. |
| Invariant gate | Same-session exact collection plus executed JUnit; missing/failed/skipped nodes and failed cleanup reject. Both PR jobs always use --test-only. Three deliberate validation mutations were detected, then restored tests passed. |
| Seed/probability consumer vectors | Independent fixed constants exercise actual runner, retained plans, Part A and benchmark consumers; exact cutoff boundaries. No production statistical formula change. |

Independent review examined the combined policy/admission/evidence/execution contracts, follow-up archive/RPC fixes, lifecycle driver, CI gate/packaging and vector delta. It accepted the final code scope with no remaining finding, separately from still-pending hosted results. It does not claim a new line-by-line audit of every historical statistical-engine module.

Local verification uses `C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe`, Python3.13.2. Configured commit hooks separately use Python3.14.3 and are not substituted for launcher evidence. Private Pine/data/heavy artifacts absent from the public checkout remain unverified; repository checks retain their existing advisories and3 evidence-store skips.

GitHub main has no branch-protection configuration (API404: Branch not protected). Workflow jobs enforce actual execution as CI checks. Making those jobs administratively required for merging is separate repository configuration; this task does not alter it or claim it exists.

Local evidence before publication:

- Archive/RPC/store/assessment regression selection:54passed, record `20260918T154400Z-0eb1ca118dba` in `qualification-fault-verification`, completed/exit0/stable.
- Repository `./fp.ps1 check`: record `20260918T155102Z-573afe56d958` in that checkout, completed/exit0/stable;72 evidence-store tests with3 existing skips and absent-private-artifact advisories.
- Final assembly `7645a48` plus reviewed lifecycle/manifest changes: unique non-boundary manifest files run through `./fp.ps1 --workers 2 python -m pytest <files> -q --tb=short`, **471passed/33 Linux-host skips**, record `20260918T160338Z-c93a2812f528`, completed/exit0/stable. These skips do not satisfy Linux acceptance. Final manifest contains418 unique required nodes, including146 QPLAN selectors and all98 selected vector additions.
- Independent final assembly review confirmed the98 vector IDs, required lifecycle/archive/RPC/race cases and byte-equivalent reviewed production fixes. No remaining actionable code finding. The broader980-test local qualification selection remains running in the unchanged original checkout; final hosted checks and two-host acceptance remain pending at publication.
