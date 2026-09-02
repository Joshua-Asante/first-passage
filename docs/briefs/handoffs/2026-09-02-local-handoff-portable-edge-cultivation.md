# Local-session handoff — portable-edge cultivation campaign

**Date:** 2026-09-02  
**Owner:** next local research session  
**Parent:** [`portable-edge cultivation campaign`](../../superpowers/plans/2026-09-02-portable-edge-cultivation-campaign.md)  
**Purpose:** copy/paste prompt for starting outcome-bearing local work after this PR merges.

## Prompt

```text
You are continuing the First Passage portable-edge cultivation campaign in the local checkout.
This is an execution session, not another planning or documentation-only session.

OBJECTIVE
Cultivate and identify one satisfactory portable trading-edge candidate within the already-approved
2–3 day campaign, preferably deployable on Tradeify Select. Manual weekly account-preservation is
acceptable. Preserve a genuine confirmed edge even if it later fails the selected Tradeify edition.
A strategy may begin incomplete and be cultivated on development evidence, but it may not become a
candidate or touch Confirm until its exact trade identity is complete and frozen.

AUTHORITATIVE STARTUP READS — READ FROM DISK, DO NOT USE A CACHED SUMMARY
1. AGENTS.md files that govern the repo and every file you may touch.
2. STATE.md queue row #1.
3. docs/superpowers/plans/2026-09-02-portable-edge-cultivation-campaign.md in full.
4. lab/analysis/orb/orb_mym_volume_gate_2026-09-02/RESULTS.md.
5. docs/adr/2026-08-30-candidate-contract.md.
6. docs/adr/2026-08-30-tradeable-reachable-gate.md.
7. docs/adr/2026-08-30-evaluation-order.md.
8. docs/adr/2026-08-30-operator-approvals-campaign-envelope.md.
9. docs/adr/2026-08-30-terminal-taxonomy.md.
10. ops/instruments/MYM.md and the current Tradeify Select rules/profile owners.
11. docs/adr/2026-09-02-portable-edge-cultivation-campaign-objective.md.

FIXED OPERATOR ELECTIONS — DO NOT RE-ASK OR REINTERPRET
- Primary objective: portable genuine edge; Tradeify Select preferred.
- Manual weekly preservation trade: acceptable, so alpha need not manufacture weekly activity.
- Research clock: 2–3 days.
- Spend: flexible, but Rule 2 still requires a priced ceiling before any paid pull or cloud run.
- A genuine edge survives a failed Tradeify edition.
- Campaign cap: at most 3 cultivation seats, at most 1 candidate contract, M=1 Confirm,
  alpha=0.05 Bonferroni, no capital authority.
- Rule 2: seats A/B/C are the three STRATEGIC constituent OUTER investigations; each seat trips at
  8 complete attempt-and-check iterations, with no self-extension.

FIRST ACTION — SEAT A IDENTITY CAPTURE
Find the private `orb_mym_4_edition.pine`, full TradingView Strategy Properties, and P50
List-of-Trades export in the local inputs/Downloads surfaces. Do not assume the prior remote search
proved they are absent locally. Search likely input roots without using `ls -R` or `grep -R`.

The Pine must hash exactly:
9292bd4ec0ca9074d6d6523491dcdde3709424bd53edf9c75dea79f3b9f65071

Before reading or generating any new payoff comparison:
- copy the exact Pine into an appropriate private/local evidence surface or record its hash/path
  without committing proprietary source if repo policy forbids it;
- retain symbol, timeframe, date span, every Strategy Property, weekday toggles, quantity,
  pyramiding, commission, and slippage;
- export the complete List of Trades for the already-selected P50 setting only;
- hash every input and record source path, size, and timestamp;
- verify that P50 is the sole changed setting relative to the recorded control configuration.

Do NOT test P55/P60/P65, alternate weekdays, another stop, another target, or another exit. The
historical surface is fully viewed. A source/config repair is allowed; a payoff-defining change is
a different cultivation seat.

P50 PROSPECTIVE-STATUS RESTRICTION
P50 was selected after the Off/P50/P80 outcomes were viewed, before any candidate contract or K
manifest. This campaign may reconstruct it as source/development evidence only. Do not open a
candidate contract retroactively around exact P50, call a new P50 window Confirm, or imply the
three-cell selection was preregistered. Exact P50 needs a separate operator-ratified legacy-intake
ruling before it can have any candidate-admission path.

IF A0 CAPTURE CLEARS — BUILD AND RUN A1
Create a deterministic, tested reconstruction tool rather than hand-calculating results. It must:
- parse the TradingView export defensively and fail on unknown/missing columns;
- preserve raw rows and emit a machine-readable normalized ledger;
- aggregate pyramided entry/add/exit legs into the true flat-to-flat position and trading-day risk
  units using the Pine's actual order semantics;
- report N, trades/week, idle-week distribution, net expectancy after the repository-authoritative
  Tradeify costs, win rate, mean/median/quantile win and loss, payoff ratio, loss runs, worst day,
  drawdown, exposure, and integer contract quantities;
- separate gross P&L, TradingView-modeled costs, and independently recomputed authoritative costs;
- reconstruct intraday MAE only if bars and order semantics make it honest; otherwise print
  UNSCREENABLE and name the smallest missing artifact;
- include tests for pyramiding, partial exits, reversals, same-timestamp fills, and malformed export
  rows.

Write the results beside the existing P50 analysis as a new dated packet. Do not overwrite the
source-stage RESULTS.md. Add a dated campaign-ledger row with exact hashes and commands.

THEN RUN A2 — CHEAP REACHABILITY FOR SOURCE DISPOSITION
Using the reconstructed risk unit:
- run the authoritative cost checks and the existing Tradeify shape/first-passage machinery by
  delegation; do not invent a new cost or venue formula;
- keep portable-edge evidence and Tradeify Select placement as separate verdict axes;
- treat manual weekly preservation as the elected account-level control rather than an alpha gate;
- if generous assumptions clearly fail cost, bounded-loss, integer-size, or first-passage geometry,
  close seat A PRE-CONTRACT DROP (venue/cost-constraint-shaped); do not increment N_expr or write a
  candidate rejection;
- if MAE or another identity-changing input is missing, mark the relevant limb UNSCREENABLE or
  EVIDENCE-BLOCKED and price/name the smallest recovery step;
- if plausible and complete, retain P50 as source evidence and present the legacy-intake ruling
  required by the owning ADR. Do not freeze exact P50 under this campaign.

The historical P50 panel provides development priors only. Never manufacture a retrospective
Confirm slice from it.

DO NOT STOP IF SEAT A IS LOCALLY BLOCKED
In the same session, inventory the repository for seats B/C and use current primary-source research
where available. Search for complete expressions or cultivatable strategies, not unsigned
predictors. An eligible seat needs a plausible path to exact side/entry/stop/exit/horizon rules,
reproducible code or trades, a cost-aware positive prior, hard loss containment, a Tradeify-legal
future at integer size, and an untouched interval. Existing executable expressions with genuinely
new information outrank another generic OHLCV window. Q-VOLREGIME may improve/cultivate a strategy,
but it is research infrastructure and confers no candidate validation by itself.

For B/C, structural/source cultivation may fill missing rules before payoff access. Once a complete
catalogue exists, open the candidate contract and K manifest before scoring its first payoff cell.
Do not cultivate on outcomes first and freeze afterward.

Every B/C contract must founding-freeze an independent mechanism discriminator, not only a payoff
test: observable/statistic, null hypothesis, expected direction, decision threshold, and
coverage/power requirement. The discriminator must be adjudicable independently of the exact
entry/exit implementation; a valid CONFIRMED verdict requires both it and the payoff/temporal test
to pass.

Commit the Confirm boundaries prospectively on the draft contract, but set the first eligible bar
strictly after the founding-freeze commit. Exclude all bars that occurred between the last source
read and the freeze; they are already historical even if nobody inspected their payoff yet.

For each possible B/C object, emit a compact intake table with:
- source and mechanism;
- exact fields present/missing;
- development/Confirm contamination state;
- cost and shape prior;
- Tradeify legality/integer-size path;
- cheapest decisive next action; and
- ADMIT-TO-CULTIVATION / DROP / DUPLICATE disposition.

Do not consume a cultivation seat for a screenshot, discretionary setup, parameter menu, or range
predictor with no direction and payoff object. Do not reopen a dead family merely to fill the slate.

SESSION DISCIPLINE
- Inspect the current branch/worktree before editing; do not overwrite unrelated changes.
- Use existing parsers, firm rules, scoring code, and cost authorities; do not reimplement them.
- Budget commands before expensive runs. Initial campaign tranche is $0 external data and <=48
  local core-hours; price any extension and obtain a new explicit operator GO before execution.
- Count Rule-2 iterations in the campaign ledger. At a seat's 8/8 OUTER tripwire, stop and emit
  spent/remaining/state/extend-or-stop; do not self-extend.
- Preserve a development nursery for cultivation, but freeze all candidate-defining fields before
  Confirm. No outcome-conditional rescue.
- Keep the campaign ledger current as work happens, not retrospectively.
- Run the narrow relevant tests first, then repository governance/link/status checks for touched
  artifacts.
- Commit coherent progress on the current branch and create/update the PR with exact commands and
  honest limitations.

REQUIRED END-OF-SESSION OUTPUT
Do not return only a plan. Return concrete evidence and one of these states:
1. CONTRACT-FROZEN — for a prospectively valid B/C object only: candidate id, founding hash,
   K-manifest id, frozen mechanism discriminator, reserved forward span beginning strictly after
   that founding-freeze commit, and reachability results;
2. CAMPAIGN-ACTIVE — completed empirical work, current seat dispositions, exact next executable
   action, and why continued work can still meet the 2–3 day objective; or
3. EVIDENCE-BLOCKED / DRY-CAMPAIGN only when the campaign plan's terminal conditions are actually
   met, with every seat typed and an add-back condition.

Do not call P50 or any alternative a confirmed edge merely because it improved a viewed development
panel. Do not retroactively contract exact P50. Do not call the campaign complete until the
satisfactory-candidate definition in the parent plan is proven field by field.
```

## Expected first local commands

These commands are examples, not substitutes for reading local `AGENTS.md` instructions:

```bash
pwd
find .. -name AGENTS.md -print
git status --short --branch
git log -3 --oneline

sed -n '1,260p' docs/superpowers/plans/2026-09-02-portable-edge-cultivation-campaign.md
sed -n '1,220p' lab/analysis/orb/orb_mym_volume_gate_2026-09-02/RESULTS.md

find "$HOME" /workspace /tmp -type f \
  \( -iname 'orb_mym_4_edition.pine' -o -iname '*orb*mym*.pine' \
     -o -iname '*list*trades*.csv' -o -iname '*orb*mym*.csv' \) \
  2>/dev/null | sed -n '1,240p'

sha256sum /path/to/orb_mym_4_edition.pine
```

Do not run the final `sha256sum` until the actual local path is known.
