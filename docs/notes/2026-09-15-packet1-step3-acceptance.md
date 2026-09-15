# Packet 1 Step 3 — provider coverage and captured cold state

Status: **STEP 3 COMPLETE — independently accepted**. Base `3dbb75b` plus the
corrections recorded here.
The [calendar/parity amendment](2026-09-15-calendar-parity-separation-amendment.md)
controls this decision. Earlier OPEN records remain historical evidence.

## Accepted domain

The retained four provider panels cover September 1, 2022, 00:00Z through
September 3, 2026, 00:00Z, including both endpoints. The 6J input is the separately
attested 88-bar-prefix derivative. All original panels and exports are preserved.
The nine references comprise the seven collected ORB/Striker variants and the
older Aegis/Vanguard references. Qualification is for their pinned bodies,
captured settings and full-origin cold replay.

Joshua confirmed that the original MGC/MYM/MNQ bar exports used Deep Backtesting,
the same full interval and 15-minute continuous-contract charts as the strategy
reports, the unchanged precision-corrected harness, electronic trading hours and
back-adjustment off. Earlier source-body and 6J attestations remain in force.

Every original nonterminal harness trade spans **one calculation bar**, with
contiguous trade identities, quantity one and zero commission. Terminal entries
are retained; terminal synthetic closes have zero duration. With the attested
one-reversal-per-bar harness, endpoint/seam checks and exact raw-to-panel decimal
comparison, this supplies completeness evidence beyond matching trade outcomes.
Even an uninterrupted 15-minute grid has only **140,449 inclusive slots** in this
interval, below the documented Deep limits. The retained reports also show ample
capital relative to recorded notional and drawdown. [TradingView limits](https://www.tradingview.com/support/solutions/43000666265-how-deep-backtesting-works/)

The September 15 captures contain **eight volume differences** across 6J, MGC and
MNQ; their cause remains unknown. The decision selects the retained original
generation, whose raw-to-panel comparison is exact. It does not replace its data,
apply tolerance to the differences, or claim the latest provider generation is
unchanged. Fresh timestamps/prices and MYM OHLCV agree completely. Reference
linkage rests on retained source/settings/capture provenance and the full trade
comparisons, not an asserted atomic snapshot of TradingView's internal memory.

Shared absent intervals mean absent input in this qualified provider generation.
They do not establish exchange closures, session legality or trading permission.

## Corrections found by direct state observations

A separate diagnostic exports each calculation bar's index, timestamp, provider
daily-open value and reset marker. It has no signal filtering. Its installed
source matches the retained source after newline normalization. MGC and MYM
captures contain contiguous indices from zero through the terminal bar.

The original helpers disagreed with **one MGC reset and 28 MYM resets**. The
corrected provider grouping model matches all **189,116 observed bars**. Three
inappropriate merge dates were removed, and the candidate Striker adapter uses
the qualified grouping helper. The saved MGC/MYM strategy charts have the same
relevant symbol, 15-minute ETH, adjustment and settlement settings as the probes.
Their timeframes were restored after read-only settlement-setting inspection.
The helper models reset equivalence classes; it is not an exchange calendar or
qualification of later dates. D19 and the separate early-close policy list remain
unchanged.

A second Pine oracle confirms that paid entry commissions reduce equity while
positions are still open. The candidate Striker adapter now subtracts remaining
open-lot entry fees. A synthetic commission-triggered DD-limit regression and
partial-close allocation check cover the correction. Captured strategy settings
and source bodies were not tuned.

Candidate private ports live in the ignored evidence directory's
`corrected-ports/` generation. Only Striker differs from the original private
ports. The primary checkout's frozen ports remain preserved. Step 6 must consume
the candidate hashes in the reviewed contract, rather than inadvertently loading
the older Striker port. No live process or deployment was changed.

## Verification

- **9/9 reference replays pass**, **3,632 matched trades**, zero exclusions,
  **851,011 ordered bar calls**, and flat terminal state with no pending orders.
  Existing trade-price/PnL comparison rules are unchanged; provider OHLCV checks
  remain exact decimal comparisons.
- All nine complete candidate cold adapter/emulator objects match the retained
  reviewed initializers. The updated runtime and private port hashes bind the
  new replay. This does not certify arbitrary warm restarts.
- Independent corrected Striker replay: **472,495 evaluations / 1,005 closes**,
  zero reset/new-close collisions, zero source-order daily-PnL mirror differences,
  zero fee-adjusted equity differences, and identical retained trade traces.
- **30 focused and related regression tests pass.** New regressions first failed
  on the observed reset/fee defects, then passed against the isolated candidate.
  Captured Striker runs have no partial closes; the partial-close check is synthetic.

The bounded source mapping retains its conditions: inactive display/account
branches are not claimed equivalent for arbitrary settings, ORB's initial-volume
representation is overwritten before active use, and the full cold origin is
preserved for recursive indicators. Corrected replay does not qualify live
account settlement or recovery state.

## Evidence contract and downstream boundary

Private `step3-evidence-index-v4.json` binds **44 artifacts** and links immutable
v3 evidence. SHA-256:
`95ac6dcb18c37a2e5809c567cd1795f86fc324b21690b45108501505f06e7538`.

The separate `packet1-step3-evidence-admission-v1` contract binds this retained
provider generation, active captured cold-state scope, runtime/port/panel/export
identities and all nine comparisons. It is a Step 3 evidence decision, not a
`book-bundle-admissions-v1` contract. It cannot admit a bundle through the existing
intake or bypass finite-margin/shared-law checks in Step 6.

Independent reviewer `packet0_review` accepted Step 3 under the amendment with
no blocking findings. The reviewed proposed contract is preserved unchanged;
its SHA-256 is
`acfa7920fe025443dd321057f4e1c192d8bc7ccbabd66c94bb25bef6233b6e6d`.
Separate private `step3-independent-acceptance.json` records the approval:
`ebcb2efb73042d2e86f46db146246a6a84ff04230b37a47f77d5951994c14f1e`.
The reviewer verified all 44 artifact identities and contract pins, original and
prefix export-duration checks, and independently passed all 30 tests. It
independently reproduced both daily-marker domains and the five corrected
Striker replays; it reviewed the other four full replays without rerunning them.

Step 4 calendar permission, Step 5 settlement and Step 6 combined admission remain
required. Production provider selection, attended recovery, deployment and each
session's activation retain their separate gates.
