# GLM steering — two remaining S2 Linux failures

Read this alongside `2026-09-19-glm-s2-enforcement-continuation.md`. It supplements that assignment; it does not restart it or authorize broader work. Apply now if useful, or after the current run finishes. Do not cancel an informative run or duplicate fixes already made: first compare this evidence with your current source and results.

**Selected outcome:** Resolve or explicitly disprove the two test-coordination findings below, then obtain meaningful Linux evidence for payload CPU enforcement and refusal of unobserved payload completion.

**Prerequisites:** Findings are bound to integrated run [35482452099](https://github.com/Joshua-Asante/first-passage/actions/runs/35482452099), PR #436 head `b0300e15c15f6d66838cf5e851c4ff050b2f08a0` (13 passed, 2 failed). Refresh your current branch and any newer run before acting. Codex downloaded the original artifact unchanged to `C:/Users/joshu/multi_firm_operations/tmp/codex-s2-run35482452099`; inspect it read-only.

**Ownership:** GLM retains implementation and integration ownership under the existing continuation. Codex retains independent review and final S2 acceptance.

**Verification:** Demonstrate the targeted behavior, not merely a green assertion. Preserve the original failures, new discriminating regression results, exact tested revision, launcher/interpreter, Linux run/artifact identities, invariant results and cleanup results. Existing combined verification and manifest requirements remain in force.

**Checkpoint:** Record each finding as confirmed/repaired, already fixed, disproved, or unresolved, with source and evidence. If a current run already resolves one, reuse its revision-bound evidence. Return a consequential contract conflict before changing the expected behavior.

**Return boundary:** Return through the existing PR #436 continuation packet after verification, or with a concrete blocker. Keep S2 incomplete pending Codex review. No merge to main, activation, S3 dispatch, quota/allowance increase or weakening of the Linux proof is assigned.

## Finding 1 — the payload-start check can mistake interpreter startup for the intended CPU load

### Observed facts

Artifact: `boundary/linux-8da7e8f9785c4ba9a7ad2fce71eb27e9-payload-bound.json`.

- `cpu_max`: `33343 100000`.
- Payload budget: 100 CPU seconds.
- Baseline when stopping the guardian: **0.271984 CPU seconds**.
- Peak over the stopped window: **0.553112 CPU seconds**.
- Stopped window: **296.502749756 seconds**.
- Populated samples: **31 of 295**.
- Final `nr_periods=22`, `nr_throttled=15`; nonzero throttling alone therefore does not establish sustained burner execution.
- Guardian ended with `ActiveState=failed`, `ExecMainStatus=9`; the failure was the payload-population assertion, after the upper-bound assertion passed.

The journal database retains these events for `work_id=unpolled`:

- CONTAINER at `2026-09-20T02:08:51.149267Z`, container `396f6826e2ba7d1b3a760168dd5ade7a9905b76beacbd34acbeefa9dce5bcf9a`.
- Payload PROCESS at `02:08:51.300830Z`, host PID 6437, UID 65532, in that container's payload scope.
- RESUMED at `02:08:51.311535Z`. This proves the send, not receipt.
- `journal.log` records the container scope deactivating at **02:09:22**, approximately 31 seconds later.

Source on the tested branch: `campaign_probe.py` uses a **30-second** `sigtimedwait` and exits with `supervisor resume signal absent` if no signal arrives. In `test_s2_payload_cpu_is_kernel_bounded_without_guardian`, the pre-STOP loop accepts a CPU delta of at least 150 ms; its success branch does not itself require an elapsed one-second interval or identify the burner children. A burst of Python startup can satisfy it.

### Interpretation and remaining uncertainty

These facts strongly support a lost/unconsumed resume followed by timeout, and show that the current startup heuristic does not prove the intended workload is running. They do **not** yet prove the container's exit reason: Codex has not found retained container stderr or a final Docker exit inspection for this container. Do not report the timeout cause as conclusively established without that evidence.

There is no evidence here that buying more runner CPU would fix the failure. Deliberate throttling may expose startup timing, but the immediate proof gap is readiness of the payload before the guardian is stopped.

### Required response

- [ ] Check whether newer work already corrects this mechanism.
- [ ] Prove resume receipt and execution of the intended descendant burners before SIGSTOP. Prefer host-observed descendant identities/cgroup membership plus sustained CPU growth across multiple intervals, or a narrowly justified readiness handshake. Do not treat a guardian SEND event or a single interpreter-CPU burst as receipt.
- [ ] Preserve the security ordering: retain alive-verified identity before permitting execution; a test readiness marker must not become an authority bypass. If the handshake itself is repaired, review normal and repeated resume behavior too.
- [ ] Retain pre-STOP and post-STOP process/cgroup samples, timestamped CPU/throttling deltas, container exit status and bounded stderr before cleanup. Keep evidence within the existing non-secret export contract.
- [ ] Verify payload activity throughout the relevant stopped interval and independent kernel enforcement. Account explicitly for the fact that quota is a ceiling, not a guaranteed CPU allocation under host contention. Do not replace the failed proof with another arbitrary lower bound or relax the reservation upper bound.

## Finding 2 — guardian PROCESS events are being mistaken for payload observation

### Observed facts

In the tested source, `_kill_before_observation` returns a lost attempt when:

```python
if supervision_events(boundary, attempt, 'PROCESS', work_id):
    return None
```

The final case also asserts the work has no PROCESS events. However, the same event kind/work ID records both guardian identity and payload identity.

The artifact's `boundary/journal.sqlite` contains a concrete counterexample for attempt `linux-4b6b50779d2a44f39f42153d96468a33`, work `unseen0`:

- PROCESS at `02:05:49.513187Z`: **guardian** PID 5691, UID 61001, cgroup ending in the guardian `.service`.
- CONTAINER at `02:05:50.405001Z`.
- PROCESS_UNOBSERVED at `02:05:50.700739Z`: the matching container exited with code 137.
- FAILURE at `02:05:50.747764Z`: `ValueError: payload exited before any alive-verified process identity; completion refused`.

Thus a guardian PROCESS event can cause the test to discard an attempt that actually exercised the intended unobserved-payload refusal. This is a concrete test-predicate defect. It does not alone explain the later timeout: that timeout occurred after retries and still requires its own last-state/event diagnosis.

The exported final snapshots show `unseen0` through `unseen5` as IN_DOUBT with observations present. Those snapshots were exported after later cleanup/recovery; they must not be presented as proof of the state at the 120-second timeout.

### Required response

- [ ] Distinguish guardian identity from payload identity using the actual retained event contract and trusted enrollment/container cgroup binding. Inspect any existing identity helper before introducing a second classifier. Do not merely filter by a guessed PID or count events.
- [ ] Fix both the retry predicate and the final no-payload-observation assertion. Check the suite's positive `COMPLETED` identity assertions too: a guardian-only event must not satisfy proof that the payload was observed alive.
- [ ] Add a deterministic regression with a guardian PROCESS event, no payload PROCESS event, and a matching PROCESS_UNOBSERVED refusal. This must count as the intended successful race outcome, not a retry. Add the complementary payload-observed case.
- [ ] On an actual timeout, capture the exact work state, transitions, relevant supervision events, guardian/container status and timestamps **before** cleanup or service restart alters them. Determine whether a legitimate terminal state is absent from the wait predicate or the supervisor actually failed to terminate/record state.
- [ ] Preserve the governing ABORTED/IN_DOUBT distinction. Do not broaden state predecessors or relabel uncertainty merely to satisfy this test.

## Integration and return

Avoid duplicating GLM's concurrent work. Review the current diff before edits and keep all fifteen registered S2 cases (twelve supervisor plus three service cases) and non-S2 invariants intact. Run focused local regressions first, then obtain the required Linux evidence on final integrated bytes. Existing launcher rules, verification caveats and PR boundaries remain unchanged.

In the return packet, state what the artifacts actually prove, which hypotheses were confirmed, what changed, and whether each test now discriminates the intended failure. Codex's investigation was read-only: no implementation or running job was changed.
