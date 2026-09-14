# A7 attended agent capture supplement

Status: operator-approved design, local implementation reviewed; **not deployed or ready for a ceremony**. This supplement applies only to the new agent source. Preserve historical manual A7 records, including the expired September 14 attempt. Integration owner: current Codex A7 task; deployment/runtime acceptance remains with that separate task.

Joshua authorized Codex to capture, enable and inject while he remains present, approved the design, and subsequently allowed the selected candle timestamp and five OHLCV values in tool records. Account identifiers, balances, positions, credentials and unrelated page content remain excluded. Public evidence remains value-free. Neither authorization permits an order, arm, new account access or production feed qualification.

## Before activation

The approved ADR amendment and scoped notices reconcile this variant with the source disposition in the [S2b ADR](../../adr/2026-08-08-s2b-signal-daemon-build.md), item-5 attribution in the [M1 ADR](../../adr/2026-07-22-c1-venue-native-monitoring-maturity.md), the [A7 procedure](2026-09-10-track-a-a7-claude-attended-stage1-dry-run.md), and [A8 evidence requirements](2026-09-10-track-a-a8-claude-m1-resolution.md). Historical manual-input requirements must not classify the new event as Joshua-entered data or Joshua-executed commands. The user approved the actor change; no repeat actor approval is owed. The deployment owner must verify actual compatible revisions/images before booking the run. This document does not claim M1 signoff, RESOLVED, deployment or source entitlement.

## Agent input contract

The manifest uses source `{kind: agent_attended_browser_capture, schema: ohlcv-1m, symbol: MYM1!}` and adds `operator_authorization_sha256`: a SHA-256 digest of the retained session GO record. Keep the existing ceremony ID, target, expiry, contract digest, preflight digest, quantity one and venue contract fields. Choose a fresh ID only after readiness and a target at least five minutes ahead. Record the actual GO separately; a digest is not proof of attendance or actor identity.

Enable and inject use the existing control CLI with the additional argument `--actor codex`. Prepare does not enable. The new source requires that flag on both actions; old manual callers retain their existing interface. Enable records its time and actor once; failure or uncertainty is reconciled instead of invoking enable again blindly.

The browser upload contains five numeric OHLCV fields and a `capture` object:

```json
{
  "actor": "codex",
  "captured_at": "2026-09-14T15:47:01+00:00",
  "chart_timestamp": "2026-09-14T11:46:00-04:00",
  "venue_contract": "MYMZ6",
  "bar_period_s": 60
}
```

These example timestamps describe a schema, not an executable ceremony or approved target. Capture time must follow target close and precede injection; both capture and inject must fall in target+60 through target+120 seconds. Chart timestamp must contain an explicit UTC offset and equal the manifest target after conversion. Expiry remains target+150 seconds. Record metadata from the actual observation, never generate it merely to fit validation.

## Browser capture

1. Claim the actual Chrome Tradovate tab using supported browser APIs. Bind the visible active chart to the manifest contract and one-minute interval. Verify current account flatness/working orders and attendance separately without exposing account data.
2. Verify chart timezone independently from the application clock. September 14 observations found chart Eastern daylight time (UTC-04:00), while the application clock showed CDT (UTC-05:00). Thus 10:xx CDT corresponds to 11:xx on that observed chart. Re-establish that binding for each session; do not hardcode it for other dates or machines.
3. After target close, select the candle within the chart area, away from order controls. Read its databox timestamp. Chart auto-scroll changes the candle under a fixed cursor: reselect using observed timestamps and verify the final timestamp again in the same DOM observation as all five fields. Reject duplicate/missing fields, invalid numbers or inconsistent OHLC.
4. Emit only the approved timestamp and five values into tool records. Write the ceremony-bound upload with actual capture metadata in a private temporary directory, read it back, verify equality and its digest, and transfer only that file to the daemon. No page export, clipboard extraction or browser URL workaround is needed.
5. Perform one inject inside the existing deadline. Retain command/receipt evidence and the operator GO alongside the private journal. No timer loop may inject again on ambiguous output. Follow the canonical terminal-state, close, zero-allocation/RETIRED restoration, broker/CrossTrade checks and fresh inert-host verification on every outcome.

## Evidence and limitations

Successful projection retains the genuine listener UUID, unique request/decision/transport join, quantity one, `dry_run=true`, `sender_invoked=false`, `qualifying_live_source=false`. For this source it reports `agent_attended_input=true`, `operator_attended_input=false`, `offline_test_only=false`, the authorization digest, enable/inject actors and times, capture metadata and matching bar digest. Historical manual projections retain their previous keys/values.

The daemon records CLI declarations and capture metadata; it does not authenticate a human or prove that a browser was actually observed. Session GO, supported-tool observations and actual command receipts are required external evidence. Synthetic integration tests establish code behavior only.
