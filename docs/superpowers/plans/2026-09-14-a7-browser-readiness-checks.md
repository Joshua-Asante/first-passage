# A7 browser readiness check results

Checked September 14, 2026 against local revision f4d0d01657dc0f87d14429df2fa2633dda661238. This is a readiness assessment, not ceremony execution or deployed-version acceptance. The approved [design](../specs/2026-09-14-a7-attended-browser-capture-design.md) remains authorized.

## Browser observations

- PASS: the claimed Chrome Tradovate tab has active chart tab `MYMZ6 1m`.
- PASS: one visible databox contains labelled open, high, low, close and volume rows. One read-only DOM evaluation parsed all five values privately, found them positive and finite, and verified low <= min(open, close) <= max(open, close) <= high. Only verdicts were returned; no raw OHLCV was exported or submitted.
- BLOCKED: exact candle/timezone binding. Databox headers read September 14 at 11:25 and subsequently 11:27, while the current UTC clock was 15:34:43 and the application later displayed 10:36:51 AM CDT. Application clock timezone alone does not prove chart/databox timezone. The chart settings menu was inspected, but no authoritative chart timezone setting was obtained. Do not label these observations as fresh CDT target bars.
- NOT PROVEN: controlled selection and retention of a specified target through a minute transition. Changes in the displayed databox timestamp alone are insufficient.

## Private transfer

BLOCKED. The documented browser surface provides read-only DOM evaluation, clipboard operations, whole-tab content export and page-asset bundling. No candle-only persistence interface has been demonstrated. Whole-tab export would collect unrelated account information and is not evidence of a scoped candle bridge. Clipboard access alone does not demonstrate file persistence. No real chart export was attempted.

The earlier synthetic data-URL probe was rejected by browser URL security policy, with an explicit prohibition on workarounds. That test was not repeated through another URL, browser surface or shell. No encoding of private values into tool output was used as a substitute.

## Runtime safeguards

PASS for the existing implementation: 166 local tests passed in 10.40 seconds using the workspace Python 3.11 virtual environment. The first default-Python attempt had no pytest; the virtual environment required sandbox escalation to launch its interpreter. The successful test invocation was:

```powershell
& 'C:\Users\joshu\multi_firm_operations\.venv\Scripts\python.exe' -m pytest tests/ops/test_c1_signal_daemon_inject.py tests/ops/test_c1_signal_daemon_operator_input.py tests/ops/test_c1_signal_daemon_m1.py tests/ops/test_c1_signal_daemon_source_retirement.py tests/ops/test_m1_stage1_control.py tests/ops/test_m1_stage1_integration.py -q
```

Coverage includes input time boundaries, identity mismatch, enablement gates, invalid OHLCV, duplicate/concurrent injectors, uncertain publication, cleanup, restart behavior, dry-run HTTP decision and closed evidence projection. These synthetic tests do not establish browser capture capability or deployed readiness.

NOT IMPLEMENTED: distinct browser-capture source and actor evidence. `ops/c1_signal_daemon/m1_stage1_control.py:70` accepts exactly eight manifest keys and only the existing operator/offline source bindings; inject requires the operator binding. `ops/c1_signal_daemon/operator_input_source.py:44` activates only that binding. `ops/c1_rail/m1_stage1_control.py:198` accepts the same two sources and infers operator-input classification from the marker. Merely changing a source string or procedure would not implement the approved evidence contract.

## Result

### Follow-up after authorization to continue

The Windows timezone is `Eastern Standard Time` (Eastern Time with daylight saving). At 15:51:40 UTC, selecting the chart's right edge displayed 11:51; at 15:52:32 UTC the chart selection displayed 11:52. The application clock independently displayed CDT. These direct observations support mapping chart timestamps as Eastern daylight time (UTC-04:00), rather than copying the application's CDT clock setting. No timezone preference was changed. This is observational evidence, not a vendor documentation claim.

Supported chart-area clicks selected displayed timestamps 11:39 at x=600, 11:46 at x=650, 11:52 at x=685, and 11:51 at x=678 (y=400). The previously selected databox later advanced to 11:52 without another click. Therefore selection can drift with a minute transition; every capture must validate its timestamp afresh and reselect by observed timestamp, not retain an old coordinate assumption. The active chart remained MYMZ6 1m.

The supported whole-tab export was first rejected by automatic approval review for exceeding candle-only scope. Joshua then explicitly approved a private temporary page export, extraction of the candle only, and deletion of the export, acknowledging temporary local account/financial content. The same supported export call was retried under that authorization and Chrome reported that it does not support `tab_content_export`. No export file was created. This is a demonstrated backend limitation, not merely an untested API.

A narrow question is pending: may only the candle timestamp and five OHLCV values appear in recorded tool input/output, allowing ordinary capture and local-file creation? The question explicitly excludes accounts, balances, positions, credentials and unrelated page content. Until answered, the original no-candle-values-in-transcript rule remains in force. No raw candle values have been emitted by this follow-up.

Not ready for an attended automatic retry. No new ceremony identity, remote enable, inject, allocation change or deployment was performed in these checks. Previous teardown is historical evidence; these checks did not refresh remote host posture. Resolve the chart-time binding and supported private producer first, then implement and test source/actor propagation across control, source and projector, and verify the deployed revisions before choosing a target at least five minutes ahead.

## Final local readiness update

Joshua explicitly allowed the candle timestamp and five OHLCV values in tool records. The resulting supported Chrome DOM capture was written to C:/Temp/a7-browser-capture-practice/captured-candle.json and read back with all five values matching. The practice candle is not an executable target and was not uploaded or injected.

The local agent source, authorization digest, explicit actor flags, capture metadata checks and truthful projector are implemented on codex/a7-agent-capture. The full targeted suite passed 188 tests in 9.28 seconds, and independent code review accepted the attribution correction. The earlier NOT IMPLEMENTED and private-transfer blockers above describe historical stages and are superseded by this update. The governing ADR amendment and A7 supplement are linked from S2b, M1, A7 and A8. Browser auto-scroll still requires per-capture timestamp validation. Compatible image deployment, fresh host readiness and a timed attended run remain outstanding. No new remote ceremony or deployment occurred.
