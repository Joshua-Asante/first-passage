# Tradeify Packet 1 — intake progress and replay correction

**Status: IN PROGRESS.** Seven diagnostic comparisons match after correcting O-N;
formal admission and shared session-input acceptance remain open. This is not
TB-F1, TB-E1, a portfolio change, or permission to deploy/arm.

## Authority and execution identity

Joshua directed “commit, push and continue to the next slice.” Packet 0 was
committed and pushed as `7c3ace8d6b52ff68d954b3352b9c3493d8c309cd` on
`codex/tradeify-attended-release`. Packet 1 starts there. The coordinator retains
integration ownership under the [attended-release plan](../superpowers/plans/2026-09-14-tradeify-attended-release.md).

After inspection found ORB capture inputs differing from its pinned source,
Joshua selected **“Keep pinned source; correct the export.”** The existing book
and private ports are unchanged. Historical manifests, reconstructed effective
inputs and original seven CSVs are preserved. A distinct corrected O-N CSV and
capture record live in the existing ignored private intake root.

## Verified findings

| Evidence | Result | Boundary |
|---|---|---|
| Original seven CSVs and 50 evidence files | Hashes, byte lengths and structural accounting diagnostics PASS | This does not establish source-state admission |
| Original four Pine bodies in Downloads | All four hashes match the adapter registry | Matching local bodies does not attest the body installed on each historical chart |
| Four local bar panels | Hashes match SHA256SUMS; timestamps strictly increase | Complete sessions, display-clock binding and exact startup coverage remain distinct checks |
| First fixed-settings source diagnostic | Five Striker bundles and O-P MATCH; O-N DIVERGENCE | No parameter search, rescaling or admission; all settings/results retained privately |
| ORB export-time Inputs inspection | Add trigger and add percentage differ from pinned defaults | The already-approved finite-margin choice is separate from these additional differences |
| Diagnostic using the captured ORB add settings | Every exported trade matches; three extra same-bar closing adds remain | Localizes a cancellation defect; does not approve captured settings as the book |
| Corrected O-N browser export plus emulator fix | All seven diagnostic comparisons MATCH, no excluded export trades | Shared-law qualification and finite-margin domain proof have not run |

The corrected chart uses the pinned ORB add inputs, the captured one-contract
sizing and finite leverage, and the original deep-backtest dates. Inputs,
Properties and completed-report captures are retained with the new CSV. The
browser reported CSV generation complete. No alert or broker order was created.
The original O-P capture still has inactive add-input differences; its
adds-disabled diagnostic match does not itself discharge source-state admission.

## Bounded emulator fix

The Pine body issues an add and later cancels pending entries in the same EOD
calculation. `run_adapter` passes the complete action list to `submit`, but a
THIS_CLOSE market entry previously filled immediately, before the later cancel.
That created an extra fill and round-trip commission. TradingView permits market
order cancellation within the creating script execution.
[Pine order cancellation](https://www.tradingview.com/pine-script-docs/concepts/strategies/#order-placement-and-cancellation)

The emulator now retains a market entry/add cancelled later in that same batch
as pending until the existing cancellation handler emits its terminal event.
Earlier cancels, unrelated IDs and subsequent submissions do not retract fills.
Uncancelled order/close ordering is preserved. This is offline Pine emulation;
it grants no live sender any right to retract an already transmitted request.

Regression first failed with an unwanted add fill, then passed after the fix.
It checks cancellation, fills, fees, flatness and absence of pending orders;
a companion case covers cancellation scope and prior fills.

## Private evidence identities

All figures, source bodies, settings and detailed divergences remain private in
`inputs/private_overrides/op1/2026-09-14-seven/` beneath the existing campaign root.

| Artifact | SHA-256 |
|---|---|
| Original collection manifest v2 | `da7157517032b76179bd3c07850c5779f968298261db6b75bd0c3c1dca383adb` |
| Fresh original intake audit v2 | `020a7ebd1b2a362522586f144ae62cdd9aefccc5ade9bf996a94c05cfb925048` |
| Initial source diagnostic | `3d8022db47a6dab72c15d5c62e2eabfd53b1980fb9e0ee02c5b9bb27596da3fb` |
| Captured-settings ORB diagnostic | `8e4a21a60efdc06668a8abe34d113f204f1d83afc6be80cb2bbcc841d08d6cee` |
| Corrected O-N CSV | `8e4902c3ee6224f57e29c8e1e0491c5c70695978d38036cfdc380eaded15e861` |
| Corrected seven-comparison report | `30984982449a182141b5fc9abe9af3a7755cb270e068848912dd623c413f981f` |
| Corrected intake structural audit | `513da0ced195a2f4a4dd4966fff499602333511bae8c702ec7bc74f51c2fdd70` |
| Corrected capture evidence manifest | `7646720c7be6f9b2edbba16e5e60e3cd5ddd8871024fdfffe6c77ffc6b75d171` |
| Original four-export regression | `f705d482268e8b11393400d555a07cfbcec3f4f1c1f21fcc76cab0d797a20655` |

Each diagnostic script is retained. Corrected comparison binds the emulator's
on-disk digest and explicitly selects the new CSV; it does not redirect historical
`parity_for` or alter `effective_inputs.json`. A later reviewed admission manifest
must explicitly supersede original O-N rather than rewriting its provenance.

## Work still required for Packet 1 acceptance

1. **Source-state admission:** bind each actual chart body, complete effective
   inputs/properties and export state to the intended contract. Finish independent
   report reconciliation and normalization. A strategy title or replay match alone
   cannot supply the missing historical attestation.
2. **Striker contract binding:** the pinned body computes base quantity as the
   minimum of floored risk/per-contract risk and floored chart-cap divided by
   one plus its add multiplier. Bind the actual chart cap separately from runtime
   `cap_alloc` and the account cap. The collected capped cases match their actual
   Account Size settings; they do not prove the complete runtime allocation domain.
3. **ORB finite margin:** retain affordability and prove unsupported margin-call
   paths unreachable over a predeclared acceptance domain, or implement/verify
   those semantics. A matching CSV does not resolve this.
4. **Shared-law integration:** implement admission and feedback ports from the
   [interface proposal](../briefs/handoffs/2026-09-14-seven-bundle-runtime-interface-plan.md)
   using the real sizing owner and confirmed execution state. These diagnostic
   runs use source sizing, not a new substitute implementation of shared law B.
5. **Calendar:** retain D19 as date membership only. Acquire product-specific
   historical trading sessions/closures and explicitly bounded forward coverage,
   then validate cutoff/deadline, DST and missing-coverage refusals. The private
   warm-up inventory distinguishes cold historical replay from live restart;
   its recommendations do not alone freeze either startup contract.
6. **Settlement:** name and qualify an authenticated statement/history plus
   attestation producer; bind session, completeness, corrections, freshness and
   replay/live provenance. The snapshot proposal and observation collector do
   not already implement this producer. Duplicate/out-of-order/stale-seal tests
   remain owed at that actual consumer boundary.

### Fresh calendar-source findings

The official CME trading-hours page was accessible on 2026-09-15 UTC. It exposes
product/date schedules and warns that holiday hours can change; the text obtained
here is not a complete four-product session table. Its day-order/trade-date carry
notes reinforce the need to distinguish calendar dates from venue sessions.
[CME trading hours](https://www.cmegroup.com/trading-hours.html)

Tradeify's current page states normal and shortened-day flat deadlines and directs
users to its holiday announcements. Those account-level rules do not replace the
earliest applicable product closure. No frozen D19 artifact was edited and no
weekday or settlement-time fallback was admitted.
[Tradeify permitted times](https://help.tradeify.co/en/articles/10495876-rules-permitted-times-to-trade)

## Verification and review

- Focused emulator and review-followup suites: **37 passed**.
- Complete `tests/ops`: **1618 passed, 12 skipped**, two existing dependency
  deprecation warnings. The default worktree run lacks private inputs; separate
  explicit private diagnostic runs above supply their own evidence, not skipped
  test credit.
- Independent reviewer: **accepted the bounded emulator fix, no blocking
  findings**. Reviewer inspected behavior and tests; its initial independent test
  attempt lacked pytest, so that review did not independently reproduce the run.
- Original four-export regression: **4/4 PASS**, using the preserved effective
  inputs, pinned exports and primary-checkout panels explicitly.
- Repository `scripts/gate_manifest.py --tier check`: **PASS, exit 0**, including
  72 evidence-store tests (three skips). Private-artifact absence and existing
  catalog/session advisories are reported, not promoted to evidence.
- Python 3.11.9 via the primary checkout's virtual environment; public suites run
  from the isolated worktree. Private scripts set the approved primary input
  roots explicitly and retain their script/input/output digests.
- `git diff --check`: PASS. Private correction evidence is confirmed ignored.

**Disposition:** continue Packet 1 from these artifacts. Do not mark the seven
bundles admitted, skip into decision-bearing qualification, or infer live readiness.
