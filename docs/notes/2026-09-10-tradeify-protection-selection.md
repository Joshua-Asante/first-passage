# Tradeify working configuration — operator selection, 2026-09-10

The operator selected the **1% combined drawdown trigger with full-size ORB base entries and no ORB adds during protection**, then authorized recording, committing and pushing that decision. This records the working research configuration. It is not a production parameter change, accepted final validation, or permission to deploy.

## Operator acceptance and STATE item 1 closure

On 2026-09-10, after the selection was recorded and pushed, the operator explicitly accepted this configuration as satisfying item 1 on the STATE board. **The configuration-selection objective is accepted and closed.** Remove that completed item from the live queue; the existing B7-REFIRE Stage 1 + M1 item advances from position 2 to position 1 without changing its scope.

This acceptance supersedes the earlier routing that kept configuration selection open pending native exits and integer sizing. The documented approximation and execution gaps remain factual limitations, but are not outstanding conditions for this operator-accepted queue item. Do not automatically reopen the campaign, resume the simulator, or create a replacement validation task. This closure records operator acceptance of the configuration, not a claim that the unperformed technical validation passed or authorization to deploy.

## Explicit publication authorization

On 2026-09-10, before the first push of selection commit `eeaf8aa`, the operator
was told that `Joshua-Asante/first-passage` is public and asked to authorize
publishing that commit, including the selected strategy names, sizing and 1%
protection policy. The operator replied: **"Yes you may."** This is an explicit,
narrow publication exception to the campaign's earlier private-override boundary
for the selected configuration values recorded in this note, including its normal
ORB configuration and protected-mode behavior. It does not release raw histories,
other captured overrides, private reports, account snapshots or numerical results.
The existing public selection commit is retained under this authorization.

## Selected book

| Strategy | Normal setting retained |
|---|---|
| Aegis | Captured 8-full-contract setting; account priority |
| Vanguard | Captured 2-micro base setting; existing adds retained |
| Striker MYM | Supplied 30-max-contract-setting history |
| ORB MNQ | Original reconstruction v7: one micro per base/add, up to two adds, 0.08 opening-range scale-in spacing |

The 0.25 ORB-spacing variant and Striker MNQ replacement are not selected. Vanguard's base setting is not an additional strict two-contract total-position cap. Shared account capacity remains 80 micro equivalents; Aegis takes priority and existing lower-priority whole legs are closed as necessary to make room under the previously studied ordering. The selection does not replace the account's own drawdown or consistency rules.

## Protection behavior selected

Use drawdown from the **combined account's own equity peak**, not separate strategy drawdowns:

`protected = round((peak_equity - equity) / peak_equity, 6) >= 0.01`

At a $100,000 peak this is approximately $1,000 of drawdown; the dollar trigger changes as the peak changes. The research decision uses the preceding close to select the following weekday's mode. A loss that first crosses the trigger is not retroactively reduced.

| Mode | Aegis / Vanguard / MYM | ORB base | ORB adds |
|---|---|---|---|
| Below 1% drawdown | Normal recorded exposure | One micro | Normal recorded adds |
| At or above 1% drawdown | 40% of normal exposure | One micro, not reduced | Disabled |

Re-evaluate daily. Full exposure and normal ORB adds resume when drawdown falls below the trigger. There is no latch until a new equity peak, cooldown, or automatic account liquidation. This follows the executable threshold behavior in `core/dd_protection.py::calculate_protection` and the prior-state timing in `core/mc/simulation.py`; a comment suggesting recovery must reach the peak is not the selected behavior. The frozen historical 1.5% production constant is **not edited** by this record.

## Feasibility screen closure

The fixed-menu [feasibility screen](../superpowers/plans/2026-09-10-tradeify-feasibility-screen.md) returned a private report and its execution is closed. Subsequent interpretation review identified an incorrect all-halves speed requirement and unsupported lower-bound language; the report's disposition is not an accepted qualification or rejection. The operator paused the full simulator and requested a separate exploratory Aegis/Vanguard/ORB weighting study. Preserve the screen's menu and outputs; the weighting study is new development-data analysis, not a rerun of that menu.

The closure narrative previously added to the frozen plan in `eeaf8aa` is moved here to correct the broader-than-status edit. The current plan differs from plan-only commit `69be794bdecc86248942f789c75bd9f83dd0702e` only in its single `**Status:**` line; this correction does not erase the earlier edit from history. PR #329 must use a merge commit, not a squash merge, to preserve that exact pre-execution ancestor independently of the later closure and selection commits.

## Evidence and limits

The selected policy was compared with uniform 40% scaling at the 0.75% and 1.00% triggers, using the existing full/H1/H2 historical partitions, cashflow stresses and forced-exit pricing probes. This separate weighting/protection study is **unregistered exploratory analysis**, not preregistered selection evidence. Its identifier first appears in git in `eeaf8aa` together with the selection; the ignored private configuration and its digest do not establish an earlier git-verifiable freeze. The seven-entry feasibility plan at `69be794` does not preregister these protection cells or the ORB-base-only comparison. The earlier description of these triggers as "predeclared" is withdrawn; no retrospective preregistration is claimed. Supporting reports, figures, histories and analysis scripts remain in the ignored private audit area. This record publishes the operator's selected configuration and routing, not those private results.

Private evidence identifiers, verified when recording this decision:

- Study: `dd-orb-base-only-2026-09-10`.
- `screen-config.json` SHA-256: `5d0b0d4d5dab84faf9beb930cfc6bbe12a06ed886b45337e761885ab58d324e5`.
- `results.json` SHA-256: `a3151f86123487ccacbb40c70562d47ad5446edbe685aa287512f9c1c61d5e6c`.

The evidence is a **daily cashflow approximation**. It retains ORB base exits generated with adds enabled even when add cashflows are suppressed; actual average price, trailing stops, stall exits and subsequent orders can change when adds are disabled. Aegis/Vanguard/MYM remain continuously scaled at 40%, without an executable integer-contract rounding, conversion or carried-position resizing policy. The original cap/forced-exit schedule is retained rather than recalculated for freed capacity. Daily realized cashflows do not establish synchronized marked equity or intraday enforcement.

Consequently, native ORB no-add exits and an explicit integer-contract implementation are the remaining validation questions. Zero observed breaches in a particular historical case is not proof of future failure below 5%. The original 200-day speed objective and overall-horizon failure requirement are not replaced by the screening criteria; the overall campaign horizon remains unfrozen. Selecting this working configuration does not close those gaps or authorize another simulator build.

The full simulator remains paused under the [governing plan](../superpowers/plans/2026-09-02-seven-strategy-tradeify-select-configuration.md). Production qualification, final account-specific validation and deployment remain separate from this research selection.
