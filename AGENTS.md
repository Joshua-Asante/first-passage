# First Passage — agent instructions

**Mission:** pass and scale prop-firm futures accounts with automated strategies.
Today that means one account: the Tradeify Select 100K evaluation. Work loop:
generate → evaluate → deploy → measure → update. Current goal and obligations:
[STATE.md](STATE.md). Code layout: [REPO_MAP.md](REPO_MAP.md).

**How to work:** be effective, not ceremonial. Do the task, verify it, report plainly.
Don't write ADRs, briefs, cards, handoff packets, lessons or session logs unless
Joshua asks for one. Decisions and evidence go in the PR description, or the
results file next to the code. If something needs Joshua's call, ask him directly.
Docs removed in the 2026-11 governance cut are in git history at main commit
`b7eaff7`.

## Money controls (hard rules)

1. **No live orders without Joshua's direction.** Agents, Codex included, may act
   on the Tradeify eval (place, exit or cancel orders, including through computer
   use) only when he directs, under a GO that covers the 7 days after he gives it.
   He can revoke a GO at any time.
   **Exception:** the weekly account-preservation round trip runs under his
   standing, revocable GO (2026-10-25). An agent may place it with no per-trade
   direction.
2. **No arming, live spend or deployment without his explicit GO** covering that
   time (a weekly GO, as in rule 1).
   The c1 Python rail is retired (2026-10-29). Its Fly apps were destroyed
   2026-11-05. Nothing is rebuilt, redeployed, armed or bound to an account under it.
3. **Tradeify evaluation accounts allow native strategy logic only.** That means
   NinjaScript in NinjaTrader. No external engine, bridge, API signals or CrossTrade.
4. **Frozen risk parameters.** `DD_TRIGGER` (1.5%) and `DD_SCALE` (0.40×) in
   `core/dd_protection.py`, the locked allocations in `core/firm_rules.py`, and
   locked Pine sources are not edited without Joshua's explicit approval.
   `dd_protection` validates its constants at import.
5. **Eval sessions follow the forward stop rule** in
   `docs/briefs/pre-registration/2026-10-31-tradeify-forward-stop-rule-registration.md`.
   It stays as is, or changes only by a new registration before session 1.
6. **Spending money** (subscriptions, data, compute) needs Joshua's approval.

## Data and credentials (hard rules)

This repository is **public**.

- Never commit: account identifiers, balances or P&L; vendor-licensed CSVs; Pine
  source; executable Python ports of locked strategies; secrets.
- **Private sources** (Pine and the runtime ports listed in
  `core/strategies/BOOK_SOURCES.sha256`, and `effective_inputs.json`) are read only
  in place, in Joshua's primary checkout. Never copy, quote, edit or upload them.
- **Codex never receives** Pine, runtime ports, `effective_inputs.json`, strategy
  parameters or account data. Exception: it may see account data on screen while it
  acts on the eval; it writes none of it to logs or files.
- **Backtest dollar figures** go only in lab `RESULTS` files, never in PR text or
  STATE.
- **Data changes** under `core/data/` carry a matching `SHA256SUMS` update. Don't
  bypass the hooks with `--no-verify`.
- **Credentials.** Agents use only their own scoped credentials (a repo-scoped
  GitHub PAT). Never use Joshua's tokens, and hold no Fly or broker credential.

## Review and merge

- Land changes by PR. Never push to `main`, and never enable auto-merge.
- **Code, tests, gates, CI, or anything touching the controls above:** merge only at
  a head the other agent has reviewed clean (Codex reviews Claude's work, Claude
  reviews Codex's), with CI green.
- **Doc-only PRs** merge once CI is green.

## Running code

- Use the checkout's launcher. Check the environment with `python -I scripts/fp.py doctor`
  (or `.\fp.ps1 doctor`), run the tests with `fp test` / `fp test-ops`, and run
  Python with `fp python ...`. Setup is described in
  [scripts/README.md](scripts/README.md#local-operations-launcher).
- **Layer boundaries** (enforced by `scripts/check_boundaries.py`): `core/` imports
  nothing internal; `lab/` and `ops/` never import each other.
- Report what you ran and its actual result, including failures.
