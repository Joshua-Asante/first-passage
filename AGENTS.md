# First Passage — agent instructions

**Mission (Joshua, 2026-11-09):** strategy research only: does any systematic futures
strategy have a real edge after costs? The prop operation is closed.
[Rulings](docs/notes/2026-11-09-rulings.md), [STATE](STATE.md),
[REPO_MAP](REPO_MAP.md).

**Method:** [The Order](docs/framework/the-order.md), adopted 2026-11-09 in witness mode. Its
state, [`order-state.json`](docs/framework/order-state.json), is shown at every session
start, and the `order-gates` check enforces it. Name each request's step and check
its gate. Without a hashed contract there is no programme work; stopping or shrinking
needs none.

**How to work:** do the task, verify it, and report the commands you ran and their real
results. Write no documents unless Joshua asks. A new rule here names who asked for it
and what fails without it.

## Roles

Joshua directs. He alone sets scope, writes the contract, rules, holds spend and the
money controls, and merges. Claude researches, builds and drafts. Codex
verifies every head and re-derives research claims by a separate route. Neither agent
verifies its own work, and a subagent's review doesn't count as the other agent's.

## Money controls (hard rules)

1. **No orders, arming, deployment or venue action of any kind.** Reopening needs a new
   ruling after a Codex-verified CONFIRMED result, under its own contract. The coda's
   exception ended before any session ([R13](docs/notes/2026-11-09-rulings.md)).
   Agents place, change, cancel or exit no eval order.
2. **Frozen parameters.** `DD_TRIGGER` (1.5%) and `DD_SCALE` (0.40×) in
   `core/dd_protection.py`, the locked allocations in `core/firm_rules.py`, and locked
   Pine sources are not edited without Joshua's explicit approval.
3. **Spending money** (subscriptions, data, compute, API) needs Joshua's approval.

## Data and credentials (hard rules)

This repository is **public**. Classify by meaning, not field name.

| Class | Contents | Agents | Public repo |
|---|---|---|---|
| **Secrets** | Tokens, passwords, keys, auth files, `.env` | By reference only | Never |
| **Private** | Pine, ports, `effective_inputs.json`, strategy settings, backtest figures, account data | When the task needs it, in place | Never |
| **Licensed** | Vendor bars, ticks, quotes, charts | Local code may run over them | Never |
| **Open** | Hashes, counts, firm and exchange rules | Yes | Yes |

- **Secrets** never enter agent context. Each agent uses its own scoped token; the
  agents' GitHub token is `FP_AGENT_GH_TOKEN`. If it is absent, stop; never fall back
  to stored or Joshua's credentials. A secret seen in a transcript is rotated.
- **Private sources** (Pine and the runtime ports listed in
  `core/strategies/BOOK_SOURCES.sha256`, and `effective_inputs.json`) are read only in
  place, in Joshua's primary checkout. Never copy, edit or upload them; his encrypted
  backup is the only exception.
- **Output.** Read private logs through tools that return approved fields; masking by
  value is only a backup. Never write strategy parameters or account data to logs or
  local files. No Private or Licensed content in commits, PR text or STATE. Backtest
  dollar figures go only in lab `RESULTS` files.
- **Licensed data.** Agents may receive counts, rates and performance statistics, on
  Joshua's acceptance of the licence risk (vendor permission is unconfirmed). Exclude
  per-bar series and timestamped price levels. Raw samples only on his word.
- **Reads are not acts.** Reading grants no authority. When Joshua directs an act, log
  what and on whose word, without values.
- **Writes.** A session may add a version-named text record under `local_artifacts`
  with no parameters or account data (temp file, then rename, failing if the name
  exists). Never touch what a process owns. Other writes go through a primary session.
- **Data changes** under `core/data/` carry a matching `SHA256SUMS` update. Don't bypass
  hooks with `--no-verify`.
- **Other services.** Nothing Secret, Private or Licensed goes to any service but Claude
  and Codex, except what Joshua sends himself. Never launch a delegated agent in a
  directory containing `.env`; use a worktree under `.claude/worktrees/`.
- **Isolation.** All agents run as one Windows user, so deny lists and guards are
  accident guards, not boundaries.

## Review and merge

- Land changes by PR. Never push to `main`, and never enable auto-merge.
- **Every PR, doc-only included:** merge only at a head the other agent has reviewed
  clean (Codex reviews Claude's work, Claude reviews Codex's), with CI green. The review
  evidence identifies that exact head.
- **CI green:** required verification for the reviewed head finished successfully;
  pending, failed or cancelled runs do not count. Explain intentional path-based skips.
- **PRs that touch credentials, hooks, guards, CI workflows, `core/strategies/` or
  `core/data/`** also get `@codex security review`. Joshua posts it, as a comment
  holding only that text; the author asks him to. Any other text in the comment gets a
  code review instead.
- **A recurring finding** is fixed as a class, with a test.
- **One writer per branch.** Each PR branch has one owning session and one writer at a
  time. Another session does not push to it without a handoff the owner accepts. Before
  editing a file another open branch or PR also changes, check them, then use a
  separate branch or send the change to the owner. The owner names the candidate head;
  the other agent reviews that exact head and does not push to it. Any later push needs
  a review of the new head.

## Code Review Rules

Report what changes behaviour or breaks a rule; skip style. Blocking:

- **Leaks:** anything the data rules forbid, including paraphrased strategy parameters.
- **Money-control breaches:** frozen-parameter edits without recorded approval; any code
  that can place, arm or route orders.
- **Order breaches:** a registration changed after its test started, a threshold
  loosened after an outcome, a successor during quarantine, or a weakened `order-gates`.
- **Fixes that hide failures:** broad exceptions, silent defaults, looser schemas, error
  exits reported as success, or a skipped or weakened test.
- **Unbacked claims:** a result with no command or output behind it.

On a re-review, review only commits since your last reviewed head.

## Running code

`.\fp.ps1 <command>` or `python -I scripts/fp.py <command>` (`doctor`, `check`, `test`).
`core/` imports nothing internal; `lab/` and `ops/` never import each other.
