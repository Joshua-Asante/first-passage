# First Passage — agent instructions

**Mission:** pass and scale prop-firm futures accounts with automated strategies.
Today that means one account: the Tradeify Select 100K evaluation. Work loop:
generate → evaluate → deploy → measure → update. Current goal and obligations:
[STATE.md](STATE.md). Code layout: [REPO_MAP.md](REPO_MAP.md).

**How to work:** be effective, not ceremonial. Do the task, verify it, report plainly.
Don't write ADRs, briefs, cards, handoff packets, lessons or session logs unless
Joshua asks for one. Decisions and evidence go in the PR description, or the
results file next to the code. If something needs Joshua's call, ask him directly.
Before implementation, check the current base and overlapping PRs; stage only intended
files. Be concise and clear. Keep code simple and batch independent calls. Never trade
away correctness, required confirmations or honest verification reporting.
Pre-cut documents: `git show f2c4ae3:<path>`; historical rules are not current
authorization.

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
   The c1 Python rail is retired. Nothing is rebuilt, redeployed, armed or bound to
   an account under it.
3. **Tradeify evaluation accounts allow native strategy logic only.** That means
   NinjaScript in NinjaTrader. No external engine, bridge, API signals or CrossTrade.
4. **Frozen risk parameters.** `DD_TRIGGER` (1.5%) and `DD_SCALE` (0.40×) in
   `core/dd_protection.py`, the locked allocations in `core/firm_rules.py`, and
   locked Pine sources are not edited without Joshua's explicit approval.
5. **Eval sessions follow the forward stop rule** in
   `docs/briefs/pre-registration/2026-10-31-tradeify-forward-stop-rule-registration.md`.
   It stays as is, or changes only by a new registration before session 1.
6. **Spending money** (subscriptions, data, compute) needs Joshua's approval.

For computer-use observation, navigation, verification and recovery, follow
[the computer-use skill](.claude/skills/computer-use/SKILL.md); it does not expand
authorization or alter accepted session procedures.

## Data and credentials (hard rules)

This repository is **public**.

| Class | Contents | Claude and Codex | Public repo |
|---|---|---|---|
| **Secrets** | Tokens, passwords, keys, auth files, `.env` | By reference only | Never |
| **Private** | Pine, ports, `effective_inputs.json`, strategy settings, locked-book backtest figures, account identifiers, balances, P&L, fills, raw logs, LedgerIds | When the task needs it, in place | Never |
| **Licensed** | Vendor bars, ticks, live quotes, charts | Local code may run over them. See **Licensed data** below | Never |
| **Open** | Hashes, counts, firm and exchange rules | Yes | Yes |

Classify by meaning, not field name. Text already public stays.

- **Secrets.** Agents may know where a secret is and let tools use it through an environment variable, file path or credential store. The value never enters agent context. Each agent uses only its own scoped token; using it through the environment is not reading a secret. Never use Joshua's tokens. A secret seen in any transcript is rotated. The agents' GitHub token is `FP_AGENT_GH_TOKEN`. If it is absent or blank, stop; never fall back to stored credentials. Agents hold no Fly or broker credential.
- **Private sources** (Pine and the runtime ports listed in `core/strategies/BOOK_SOURCES.sha256`, and `effective_inputs.json`) are read only in place, in Joshua's primary checkout. Never copy, edit or upload them; his encrypted backup is the only exception.
- **Output.** Read private logs through tools that return approved fields. Mask by value only as backup. Never put Private or Licensed content in commits, PR text or STATE, and never write strategy parameters or account data to logs or local files.
- **Reads are not acts.** Reading grants no authority over orders, row dialogs or the money controls. When Joshua directs an act in the moment, log what and on whose word, without values.
- **Licensed data.** Agents may receive counts, rates and performance statistics, on Joshua's stated acceptance of the licence risk; vendor permission is unconfirmed and this is not a finding that it is allowed. Exclude per-bar series and timestamped price levels. Account and strategy results stay Private. Raw samples and other vendor-data outputs only on Joshua's word. No chart or quote screenshots on the live eval until Tradeify answers on terms. His own orders and fills may reach providers.
- **Writes.** Any session may add a version-named text record under `local_artifacts`, holding no strategy parameters or account data: write a temp file in the same folder, then rename it, failing if the name exists. Never touch anything a process owns. All other writes go through a primary session.
- **Isolation.** All agents run as one Windows user. Deny lists and guards are accident guards, not boundaries.
- **Backtest dollar figures** go only in lab `RESULTS` files, never in PR text or STATE.
- **Data changes** under `core/data/` carry a matching `SHA256SUMS` update. Don't bypass the hooks with `--no-verify`.
- **Other services.** Beyond Claude and Codex, nothing in the Secrets, Private or Licensed classes goes to any service or agent, except what Joshua sends himself. Never launch a delegated agent in a directory containing `.env`: use a worktree under `.claude/worktrees/` and read private sources in place by absolute path.

## Review and merge

- Land changes by PR. Never push to `main`, and never enable auto-merge.
- **Every PR, doc-only included:** merge only at a head the other agent has reviewed
  clean (Codex reviews Claude's work, Claude reviews Codex's), with CI green. The
  review evidence identifies that exact head.
- **CI green:** required verification for the reviewed head finished successfully;
  pending, failed or cancelled runs do not count. Explain intentional path-based skips.
- **Before asking for review**, the author runs the checks for what it changed and
  lists the commands and their actual results in the PR description.
- **PRs that touch credentials, hooks, guards, CI workflows, `core/strategies/` or
  `core/data/`** also get `@codex security review`.
- **A finding that recurs** on a second PR gets fixed as a class: a test, or a gate
  in `scripts/gates.yml`, not another one-off fix.

## Code Review Rules

For the reviewing agent (Codex reads this section on GitHub reviews; Claude follows
it when reviewing Codex). Report what changes behaviour or breaks a rule; skip style.
Treat these as blocking:

- **Public-repo leaks:** anything the Data and credentials rules forbid, in files,
  tests, fixtures, logs or PR text, including paraphrased strategy parameters.
- **Money-control breaches:** an edit to the frozen risk parameters without Joshua's
  recorded approval; new code that can place, arm or route orders; an external engine
  or bridge on the Tradeify path.
- **Fixes that hide failures:** broad exceptions, silent defaults, looser schemas,
  success exits on error, or a skipped or weakened test.
- **Unbacked claims:** a result in the PR description with no command or output
  behind it.

On a re-review, review the commits since your last reviewed commit and what they
affect. Don't re-raise a resolved finding unless new code reopens it.

## Running code

- Use `.\fp.ps1 <command>` in PowerShell or `python -I scripts/fp.py <command>`;
  commands are `doctor`, `check`, `test`, `test-ops` and `python ...`. For UTF-8
  Python output on Windows, pass `python -X utf8 ...` through the launcher. Setup:
  [scripts/README.md](scripts/README.md#local-operations-launcher).
- **Layer boundaries** (enforced by `scripts/check_boundaries.py`): `core/` imports
  nothing internal; `lab/` and `ops/` never import each other.
- Report what you ran and its actual result, including failures.

## Agent routing (Claude and Codex only)

Delegate bounded implementation with the goal, allowed/forbidden files, acceptance
checks and exclusions in the prompt. Keep open design decisions, sensitive work,
integration and merge with the delegating session. Review returned diffs and checks.
A subagent can't supply the other agent's required review.
