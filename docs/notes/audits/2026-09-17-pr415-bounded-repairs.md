# PR 415 bounded qualification repairs

Acceptance remains paused pending PR 420 and real execution-boundary integration.
This change does not establish executor-completion provenance or same-process isolation.
No production qualification, production signing keys, deployment or host provisioning is involved.

## Follow-up review of 9923449

The four findings posted on the latest reviewed head were reproduced and repaired
in this same isolated worktree. This follow-up preserves the acceptance pause above.

| Related case | Disposition |
| --- | --- |
| Replaced CPU/wall origins | The public executor inventory is a read-only view. Budget checks use a privately owned issuance registry; rebinding the public view cannot change their authority. Issued bindings are immutable tuples, including against `object.__setattr__`. Duplicate initialization cannot restart the clocks. This is bounded mutation prevention, not protection against arbitrary interpreter introspection or execution-completion proof. |
| Signing dependency configuration | Hosted tests install the canonical `tools/local_verification/requirements-extra.txt`, also used by the local verification image. The workflow no longer owns a duplicate cryptography pin. |
| Completed-result identity | An identical manifest/outcome is insufficient: producer scope, authentication digest and ordered stage inventory must also match the durable receipt. Changed identities raise `AttemptConflict` without journal writes, including after reopen. |
| Public lost-receipt recovery | Independent review found the precommit snapshot check prevented every public retry. Snapshot checks now apply only before a result is committed; completed retries reach the transactional identity comparison. Exact authenticated retries survive journal reopen and boot rotation; a newly signed authentication for the same result conflicts. |
| Authentication object substitution | Claim, commit and seal boundaries require the exact `AuthenticatedResult` class and consume the freshly reauthenticated object. Tests reject subclass equality attacks independently at each boundary, and prove a caller-controlled digest field's equality cannot determine the claim digest. |

Reproduction records under `.cache/fp-verification/`: the original twelve cases
all failed as expected in `20260917T201645Z-3b2542c6f4bb`; fourteen focused cases
passed in `20260917T201950Z-ac6f98594451`. Public retry cases then reproduced the
related gap in `20260917T202217Z-371dc6905994` (two expected failures). Final
revision-bound verification and hosted results are reported in the PR follow-up.

## Baseline and workflow

Refreshed PR 415 head: `319ce56978d58156b13f0da474ce249f8e9e4d61`.
The qualification implementation still matched the reviewed `5e935c8` baseline.
An isolated `codex/pr415-bounded-repairs` worktree preserves the existing PR
checkout and unfinished N1 work. Main was merged using the PR's existing merge
workflow: PR 421 revision `31512368e6d1b9e1cc7acc6cf0baa752dea3bed7`, integration
merge `ed6f1ba9cc1015a5849ed55a0860f888b749f3f1`. No launcher implementations were
copied. PR 415's cryptography CI dependency and operations lock were preserved.

The checkout's `fp.ps1 doctor` passed with Python 3.13.2 at
`C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe`, all 62
locked packages matched, and cryptography 50.0.1. Launcher-selected pytest config,
root and advisory progress are retained in the verification records. Permanent
regressions are inside the checkout; diagnostic scratch scripts are not acceptance
checks. Source, index, HEAD and dependencies remain fixed during recorded runs.

## Related-case disposition

| Finding / related boundary | Repair and evidence |
| --- | --- |
| Coherently substituted seeds and source pools | G5 rederives the complete ordered stream inventory using the dispatcher's canonical seed producers and frozen contract. N1, N2/Part B and every Part A outer/inner address are checked, including unused expansion addresses. Source population hashes derive from the ordered frozen pool. Tests change declarations and dependent hashes together. A fixed seed vector preserves the existing stream. |
| Part A panel/source bindings | Retained panel indices, identities, source membership, lengths and path bindings are checked. Initial and expanded inventories and bootstrap repetitions remain valid. A complete G5 case with consistently rehashed foreign-source panel evidence is rejected. This is not proof that the sampler executed. |
| Result/seal key aliasing | OPERATOR registration rejects both intersecting key IDs and intersecting actual public-key fingerprints. Generic and production entry points share the rule. Issued-domain revalidation enforces it at contract, preflight, executor, result authentication, commit and seal consumers. Explicit TEST_ONLY fixture policy remains non-production. |
| Seal after VOID | G5 records the verified seal in the existing journal event chain under BEGIN IMMEDIATE, rechecking current validity and the committed PASS/authentication binding in that transaction. VOID uses the same writer lock. Identical retries while VALID reuse history; distinct externally verified seals remain permitted while VALID. VOID blocks reissuance without deleting historical results or seals. The governing invalidation contract still applies to historical seals; this change does not grant them continuing authority. |
| Concurrency/recovery | Real SQLite connections exercise both lock acquisition orders, with the second transaction observed attempting BEGIN while the first holds the lock. Tests cover early and late VOID through public G5, restart, retries, changed committed identities and rollback after an injected SQLite write failure. |
| Descriptor drift | Compare raw class namespace/layout, generated dataclass metadata and native slot descriptors, including arbitrary added descriptors. The per-class CPython ABC cache is a named mutable-state exception. Tests make FAILURE fields read as PASS, then require verification to reject; slotted journal claims are covered too. Introspection is only drift detection. |
| Consumed dispatch / fabricated completion | Still open. Caller-controlled consumption and manufactured outcomes remain possible in the existing authority architecture. No additional bit, receipt or constructor is presented as execution proof. |

## Development verification

Commands use this checkout's `fp.ps1`, with `--workers 2` before `python -m pytest`
for independent tests. Records live under `.cache/fp-verification/` and are local,
not repository artifacts. Red tests are evidence of reproduction, not acceptance.

- `20260917T190501Z-1335a0cee083/record.json`: 9 failed, 1 passed; signing aliases and descriptor gaps reproduced before production changes.
- `20260917T191027Z-ae0fd7589641/record.json`: 25 failed, 13 passed; coherent seed substitutions and incomplete/reordered plans reproduced.
- `20260917T191156Z-4d5c5456ce9b/record.json`: 1 failed; public G5 sealed after VOID before the transition repair.
- `20260917T191457Z-138e3e979be7/record.json`: 125 passed, no skips, completed and source-stable; focused validation, signing, descriptor, journal and G5 regressions.
- `20260917T192229Z-610acf225f6a/record.json`: 58 passed, 1 failed; additional complete-G5 and late-VOID cases passed; the new seal-history code unnecessarily rejected a distinct verified seal while VALID. That compatibility restriction was removed before final verification.

Earlier intermediate failures included an intentionally shared OPERATOR fixture,
the legitimate CPython ABC cache, and a restart test that used a superseded boot.
Those were diagnosed rather than treated as acceptance evidence. Final regression
and gate records, tested commit, CI and review dispositions are reported on PR 415.

## Deferred acceptance

PR 420 owns the Linux isolation environment and related provisioning/cleanup.
Real executor completion, protected output capture/attestation, execution-to-G5
acceptance and Linux permission/interruption/restart tests remain open for that
integration. Full qualification acceptance is not implied by these regression
results. The prior N1 prototype is preserved separately and is not integrated here.

The first combined regression run (`20260917T192526Z-3466bbd84c31`) completed with
626 passes, 58 failures, 15 setup errors and 3 Windows symlink skips. All 73
failures/errors had one cause: the existing calculator test imported the same
source as bare `certification_power`, violating the qualification runtime's
canonical-module rule during collection. The test now imports
`scripts.certification_power`; no calculator code or production alias check was
changed. The independent launcher run (`20260917T192949Z-e06cce52cb3b`) passed
62 tests with the same 3 Windows symlink skips. Repository gates passed in
`20260917T192513Z-c066d324a713`, with 3 unittest skips and disclosed absent
private-data/Pine checks. The final combined run follows the test-import repair.

The broader run on clean `69e59c9` completed with 622 passes and one failure
(`20260917T202904Z-4a86ddbcef5d`). The sole failure was the older full-composition
test explicitly expecting identical public commit retries to fail. Its assertion
now requires the same receipt and unchanged events before and after journal reopen,
while preserving the subsequent G5 sealing checks. The corrected full-composition
case passed in `20260917T204728Z-dd6ad4c363a1`, with completed, source-stable,
complete-capture evidence and no report errors. Its existing pytest `record_property`
/xunit2 warning remains advisory. No production code changed after `69e59c9`.
Hosted CI on that commit independently reported the same sole assertion failure,
with 6,132 passes, 57 skips and 48 passing subtests. Final hosted verification is
run on the follow-up test correction and reported on the PR.
