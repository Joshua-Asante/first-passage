# A7 attended agent capture and execution

**Status:** `Accepted` — operator decision; runtime activation pending deployment verification.
**Decision date:** 2026-09-14
**Authors:** Joshua (decision), Codex (implementation and record)
**Layer:** execution
**Supersedes:** `2026-08-08-s2b-signal-daemon-build.md` (in part) — controlled-input actor and candle transcript scope only
**Supersedes:** `2026-07-22-c1-venue-native-monitoring-maturity.md` (in part) — controlled-input actor and candle transcript scope only
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none

## §0 — Rule 0 reads

Read before recording this amendment: `ops/c1_rail/m1_stage1_contract.py`, `ops/c1_signal_daemon/m1_stage1_control.py`, `ops/c1_signal_daemon/operator_input_source.py`, `ops/c1_signal_daemon/m1_stage1.py`, and `ops/c1_rail/m1_stage1_control.py`. Anchor: base commit `f4d0d01657dc0f87d14429df2fa2633dda661238`, followed by the local `codex/a7-agent-capture` diff on September 14. The frozen contract remains `346387e565225d956da0f5b9696f211dee82ff9a823dda6e56b0ce32aba9d94f`; adding a source does not change its sizing or permanent dry-run enforcement.

The governing S2b/M1 September 11 addenda and A7/A8 handoffs were read directly. The prior deployed implementation accepts manual input only; local changes are not evidence of a compatible deployed image. Browser observations and file-write practice are recorded in the [readiness checks](../superpowers/plans/2026-09-14-a7-browser-readiness-checks.md).

## §1 — Context

The September 14 manual attempt expired before Joshua finished transcription and submission. He expressly authorized Codex to capture the candle and run enable/inject while he remains present, then approved the design. Chrome's advertised page-export method proved unsupported. Joshua therefore expressly allowed only the candle timestamp and five OHLCV values in tool records. A supported DOM capture was written to a private local file and read back with matching values.

## §2 — Decision

Permit the attended agent variant described in the [A7 supplement](../briefs/handoffs/2026-09-14-a7-agent-capture-supplement.md). Codex captures and executes enable/inject; Joshua supplies session GO, remains present, and confirms the required broker/route verdicts. Use a distinct source and retained action evidence, never label this variant as Joshua-entered or Joshua-executed input. The timestamp and five candle values may enter tool records, but raw account information, credentials and unrelated page contents remain excluded. Public evidence remains value-free.

Effective for internal source/actor acceptance on this decision date; actual activation requires reviewed compatible images and a fresh attended session. This changes who supplies the controlled input, not item 5's origin/sizing/dry-run limbs, M1 signoff requirements, deployment gates, one-shot controls or vendor entitlements. It does not qualify a production feed or authorize an order or arm.

## §3 — Alternatives considered

| Alternative | Disposition |
|---|---|
| Repeat manual transcription | Available fallback, but the operator selected automation after the expired attempt. |
| Private whole-page export | Explicitly approved, then found unsupported by Chrome. No export was created. |
| Reuse the manual source marker | Rejected: it would misattribute actor/source evidence. |

## §4 — Falsifier

If any attempt cannot establish the exact closed target, captures unrelated account information, accepts a late/duplicate input, or reaches a venue sender, then stop this variant and complete teardown; do not substitute a different candle or widen deadlines. Reassess the failed boundary before another session. Check at every practice and ceremony; otherwise proceed only when all readiness gates pass.

## §5 — Forbidden moves

- Do not reuse the manual source for an explicitly declared agent action. Both enable and inject reject that mismatch; historical manual evidence is not retroactively relabeled.
- Do not bypass the rejected browser URL test or infer that an advertised export capability exists. Use the supported candle-only tool-record path the operator actually approved.
- Do not reuse a fixed cursor coordinate across chart scrolling without checking the selected timestamp in the final capture observation.

## §6 — Consequences and gate

The input workflow removes operator transcription but requires compatible control/source/projector deployment and honest provenance. CLI actor declarations are not authentication: session GO and actual tool/command receipts remain necessary. Chart timestamp conversion is an operational risk; observed chart EDT and application CDT must not be conflated.

Code acceptance is PASS only when the targeted tests and independent review pass. Operational readiness is PASS only when the source/actor procedure, compatible deployed revisions, current host preflight, exact fresh candle binding and attendance are established; otherwise FAIL and do not enable. M1 acceptance stays unchanged until A8 obtains the required actual evidence and dated signoff.

Downstream updates: S2b and M1 receive scoped supersession notices; A7 and A8 point to this variant and its evidence semantics. No historical append-only return is overwritten.

## §7 — Implementation

The [implementation plan](../superpowers/plans/2026-09-14-a7-agent-source-implementation.md) covers the new source, manifest authorization digest, explicit actor arguments, capture validation, durable evidence and projector. Local code passed 188 targeted tests; independent review accepted the attribution fix. Deployment and actual ceremony evidence remain separate.

## §10 — Audit hooks

Run from the isolated worktree with the workspace Python 3.11 environment:

```powershell
& 'C:\Users\joshu\multi_firm_operations\.venv\Scripts\python.exe' -m pytest tests/ops/test_c1_signal_daemon_agent_input.py tests/ops/test_c1_signal_daemon_inject.py tests/ops/test_c1_signal_daemon_operator_input.py tests/ops/test_c1_signal_daemon_m1.py tests/ops/test_c1_signal_daemon_source_retirement.py tests/ops/test_m1_stage1_control.py tests/ops/test_m1_stage1_integration.py -q
rg -n '2026-09-14-a7-attended-agent-capture' docs/adr/2026-08-08-s2b-signal-daemon-build.md docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md docs/briefs/handoffs/2026-09-10-track-a-a7-claude-attended-stage1-dry-run.md docs/briefs/handoffs/2026-09-10-track-a-a8-claude-m1-resolution.md
git diff --check
```

Expected: 188 passing tests, all four scoped notices found, and no whitespace errors. Mechanical brief validation must also pass; no command above establishes deployed readiness.

## Change history

| Date | Change | By |
|---|---|---|
| 2026-09-14 | Approved attended agent variant and candle-only tool-record exception; record local implementation and operational gates | Joshua / Codex |
