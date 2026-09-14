# A7 attended browser capture and agent execution

Date: September 14, 2026. Owner: the current Codex A7 task.

Status: operator direction, actor authorization and implementation design approved in conversation on September 14, 2026. Execution readiness remains unproven. Joshua explicitly approved the design and requested a retry, subsequently proposing 10:35 CDT. This document records the authorization without pretending that the existing runtime already implements the new source.

## Approved operator decision

Joshua stated: "yes, I want to authorize you to run enable and inject too, as well as capture the candle, while i remain present".

For a future expressly started, attended A7 dry-run session, one session GO may authorize the agent to enable, capture the designated closed candle, privately transfer it and inject once. Joshua remains present and confirms account readiness and final no-order evidence. Manual transcription and manually typing the two commands are no longer the intended actor requirements for that future procedure. Do not ask Joshua to authorize these same actor roles again.

This does not start another ceremony, extend the expired appointment, reuse stage1-20260914-1, permit an order/arm, qualify a production feed, or reinterpret the failed September 14 attempt. Existing A7 remains failed/expired, with zero allocations and inert hosts verified in the [readiness return](../../notes/rail_build/M1_STAGE1_DEPLOYMENT_READINESS.md). PR 383 records that historical outcome independently.

## User experience and data flow

1. Joshua opens the signed-in Tradovate Chrome chart, remains present and confirms the relevant account is flat with no working orders. Agent completes readiness/preflight and agrees a fresh target before enabling.
2. Agent binds the exact chart contract, one-minute interval, date/timezone and target opening minute. At close, read all five OHLCV fields from the same selected-candle databox observation. Require a proven closed target candle; never infer identity from screen position alone.
3. Transfer values into the ceremony-bound private upload. September 14 amendment: Joshua explicitly allowed the candle timestamp and five OHLCV values in tool records, enabling supported DOM capture followed by ordinary local file creation. Account values, identifiers, credentials and unrelated page content remain excluded. Raw candles remain outside public artifacts. The earlier strict private-channel requirement is superseded only for these six candle fields; encoding is unnecessary.
4. Agent invokes the existing guarded submission path exactly once inside the approved window. Record operator session GO separately from capture/enable/inject actor evidence; the agent must not claim that Joshua transcribed or ran these commands.
5. Agent verifies terminal state, unique journal/ledger join and actual receipt; obtains the final broker/CrossTrade verdict; closes, restores zero/RETIRED and verifies both hosts inert. Abort, ambiguity, late input or missing attendance leads to teardown without blind retry.

## Grounded observations and unproven capabilities

Source inspected on f4d0d01657dc0f87d14429df2fa2633dda661238 (runtime source inherited from main 420ce3a): daemon m1_stage1_control.py inject enforces the operator marker, exact contract/time/boot, active config/journal gates, five positive finite values, OHLC consistency, exclusive claim and target+60 through target+120 timing. operator_input_source.py verifies the published record digest and yields once. Listener m1_stage1_control.py projects source identity and evidence; changing actor prose alone cannot honestly relabel this source.

Current Chrome supported claimTab/Playwright read-only DOM observations found a visible `.databox` with a `.header`, a date/time pattern and labelled open/high/low/close/volume rows. A filtered observation printed only the layout, with every numeric value replaced: date/time, open, high, low, close, volume, optional sma. This corrects the earlier limited page-wide label probe: labels elsewhere on the page did not establish selected-candle provenance. No real bar was captured for injection.

Still to establish before declaring capture ready:

- Reliably select and keep the target candle selected through a fresh bar transition using supported UI actions; bind the databox timestamp to the confirmed date, timezone, interval and contract.
- Demonstrate extraction is one consistent DOM observation and detect databox movement, missing fields, changed interval/contract, stale chart or lost page/attendance.
- Completed after the candle-only transcript exception: a supported DOM read was written to a private temporary JSON file and read back with all five values matching. Whole-page export was explicitly approved but Chrome does not implement it; no export was created. The ceremony-bound timed upload still requires its own execution evidence.
- Establish applicability of vendor/exchange permissions for this specific attended, one-bar, dry-run use. The operator's internal rule amendment is not a vendor entitlement grant. No conclusion of either permission or prohibition has been established for this exact use.

## Required implementation surfaces

The S2b source disposition, M1 item-5 input addendum, A7 actor/timing/evidence procedure, and downstream A8 evidence expectations must agree with the new actor/source attribution. Preserve the historical manual-input records.

Add a distinct source identity and explicit capture/enable/inject actor evidence through the manifest/control/source/projector interfaces, with backward-compatible interpretation of old evidence. Retain qualifying_live_source=false: a bounded browser ceremony does not certify unattended production-feed operation. Do not simply reuse the manual-source label or fabricate an operator receipt.

Keep current sizing, dry-run prohibition, input deadline, one-shot reservation, unknown-transport barrier and teardown requirements. Timing changes, if later required by measured capture performance, are a separate decision; do not silently widen the bounds. No live-source subscription, API credential staging or order-control automation is part of this design.

## Verification and activation

At 15:32:14 UTC (10:32:14 CDT), the proposed 10:35 CDT target no longer met the unchanged five-minute preparation requirement. No new ceremony was enabled or injected. A disconnected synthetic export probe attempted navigation to a data URL; browser URL security policy rejected the navigation and explicitly prohibited workarounds. The probe stopped without exporting real chart data. A supported private transfer path remains unproven; do not substitute a different navigation surface to circumvent that rejection.

First demonstrate timestamp/field binding and the private bridge in a disconnected practice environment with synthetic values. Then test wrong/stale candle, mismatched contract/interval/boot, missing volume, inconsistent values, lost UI, deadline miss, duplicate submission, uncertain transport and teardown. Prove capture-to-submission latency fits the unchanged window before booking a fresh attended ceremony.

Do not fabricate source acceptance, green tests or deployment evidence. Implementation/deployment, source-use eligibility and a new attended session each require their actual evidence. The already-approved agent actor roles do not need repeated confirmation.

## External sources inspected

- [Tradovate terms and EULA](https://www.tradovate.com/terms-and-eula/), accessed September 14: personal software-use rights and integration/use restrictions; does not by itself establish entitlement for this exact capture workflow.
- [CME non-display licensing FAQ](https://www.cmegroup.com/market-data/distributor/files/cme-group-data-licensing-policy-guidelines-and-non-display-licensing-faq-october-2024.pdf), accessed September 14: distinguishes display/non-display uses independently of technology. Applicability to this particular one-bar dry-run remains unverified; do not assert a fee or required license from broad examples alone.
