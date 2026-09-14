# A7 agent source implementation plan

> **For agentic workers:** Execute with superpowers:executing-plans. Integration owner: current Codex A7 task. Steps use checkboxes for tracking.

**Goal:** Carry an expressly authorized attended browser capture through guarded input and truthful evidence projection.

**Architecture:** Add a distinct source while retaining the existing one-shot state machine and manual upload schema. Require an authorization digest in the browser manifest, explicit actor declarations at enable/inject, and timestamp/contract/interval capture metadata in its upload. Persist action evidence before publishing the bar; project it only after the existing unique dry-run ledger join succeeds.

**Tech Stack:** Existing Python 3.11, pytest, JSON journal and supported Chrome DOM inspection.

**Spec:** [Approved design](../specs/2026-09-14-a7-attended-browser-capture-design.md).

## Global constraints

- Keep current sizing, dry-run prohibition, input deadline, one-shot reservation, unknown-transport barrier and teardown requirements.
- Preserve old manual/offline records and the frozen trading contract digest.
- Joshua now permits the candle timestamp and five OHLCV values in tool records. Account and credential data remain excluded. Do not export the page or bypass the blocked browser URL.
- Local tests are not deployed readiness or actual actor authentication. CLI actor declarations, persisted receipts and the attended session transcript jointly support attribution; an actor string alone does not prove identity.
- No remote ceremony or deployment in this implementation step. A8 deployment coordination remains separate.

## Behavioral contract

Producer: current agent reads one visible MYMZ6 1m databox through the supported browser API and writes an upload. Capture metadata binds chart timestamp with explicit UTC offset, capture time, venue contract and 60-second period. Target equality and capture after close are checked again by the daemon. The local browser observation established chart EDT despite the application CDT clock; each selected timestamp must be rechecked because the chart scrolls.

Manifest: existing eight keys plus `operator_authorization_sha256` only for `AGENT_INPUT_SOURCE`. The digest points to separately retained operator GO evidence; it grants no account permissions. Control owns enable and inject action timestamps in `agent_evidence`; the journal survives close and is consumed by the evidence projector. Publication failure after evidence persistence retains the exclusive claim and prevents another input. No new bar-record format is required: the source-bound digest already distinguishes sources.

Interfaces:

```python
AGENT_INPUT_SOURCE = {"kind": "agent_attended_browser_capture", "schema": "ohlcv-1m", "symbol": "MYM1!"}
# Existing functions gain keyword-only actor=None, preserving manual callers.
enable(store, config_path, ceremony_id, *, boot_id, reviewed, now, actor=None)
inject(store, config_path, *, ceremony_id, boot_id, contract, time, bar_file, now, actor=None)
# Browser upload has five numeric fields plus capture:
capture = {"actor": "codex", "captured_at": "2026-09-14T15:47:01+00:00",
           "chart_timestamp": "2026-09-14T11:46:00-04:00",
           "venue_contract": "MYMZ6", "bar_period_s": 60}
```

### Task 1: Attended input cannot be mislabeled or submitted without capture evidence

Files: `ops/c1_rail/m1_stage1_contract.py`, new `ops/c1_rail/m1_stage1_agent_input.py`, `ops/c1_signal_daemon/m1_stage1_control.py`, `ops/c1_signal_daemon/operator_input_source.py`; tests in new `tests/ops/test_c1_signal_daemon_agent_input.py`.

- [x] Write a real temporary-journal test that prepares the new source with authorization digest, enables with actor `codex`, injects a closed synthetic candle with capture metadata and polls it once. Assert persisted enable/inject actors, timestamps and receipt digest. Missing actor, wrong chart time/contract/period, capture before close or after inject must leave no published bar.
- [x] Run that file and observe failure because the current manifest validator rejects the new source.
- [x] Add the constant and shared capture validation. Accept the ninth manifest key only for the new source; require a lowercase 64-hex authorization digest. Add `--actor codex` and required per-action checks for the new source. Persist `agent_evidence` under the same journal lock and exclusive claim before publication. Extend source activation to accept both attended bindings.
- [x] Run new tests plus the existing inject/operator/source-retirement tests with the workspace Python 3.11 environment; require all to pass.

### Task 2: End-to-end evidence distinguishes agent capture from manual input

Files: `ops/c1_rail/m1_stage1_control.py`, `tests/ops/test_m1_stage1_integration.py`.

- [x] Extend the real HTTP/ledger integration parametrization with `agent`. Produce its input through the actual prepare/enable/inject functions and source poll. Assert `agent_attended_input=True`, `operator_attended_input=False`, `offline_test_only=False`, venue MYMZ6, quantity one, dry-run true and sender never invoked. Removing actor/capture evidence must make projection refuse.
- [x] Run the agent integration case before extending the projector; require failure on unsupported source.
- [x] Validate persisted action/capture evidence and authorization digest before returning the public projection. Include only actor names, timestamps, capture metadata and authorization digest; exclude prices and account values. Keep legacy projection values unchanged.
- [x] Run the complete targeted M1 suite and review source binding, publication ordering, late/duplicate/restart behavior and corrupted evidence rejection.

### Task 3: Record readiness without claiming activation

- [x] Update the approved design/privacy exception and readiness results. Add an explicitly inactive A7 agent procedure supplement with file schema, `--actor codex`, target conversion, fresh capture checks and the unchanged teardown; identify corresponding S2b/M1/A8 amendments needed for deployed acceptance.
- [x] Review all changed interfaces together. Record exact test counts and local revision; do not label local code as deployed or choose a candle target until deployment and procedure acceptance are verified.

## Plan review

The producer is an actual supported Chrome DOM read followed by a local file write, successfully practiced after the candle-only transcript exception. Existing actor/source records remain historical. Deployment, source-use eligibility and attended route evidence remain separate acceptance dependencies; neither a synthetic fixture nor CLI declaration establishes them.

## Execution result

Local implementation and documentation complete: 188 targeted tests passed in 9.28 seconds. Independent reviewer accepted the correction that rejects declared agent actors on legacy sources. The governing ADR and four scoped notices reconcile internal actor/source acceptance; actual compatible deployment and attended execution remain unperformed. No commit, push, remote enable or inject was performed for this feature.
