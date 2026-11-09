# First Passage — agent instructions

**Mission (Joshua, 2026-11-09):** strategy research only. Find out, with honest
evidence, whether any systematic futures strategy has a real edge after costs. The prop
operation is closed. Rulings: [2026-11-09](docs/notes/2026-11-09-rulings.md). State:
[STATE.md](STATE.md). Code layout: [REPO_MAP.md](REPO_MAP.md).

**Method:** [The Order](docs/framework/the-order.md) governs every piece of programme
work: aim, ask, subtract, choose the test, register, run and verify, rule, stop. Its
state is [`order-state.json`](docs/framework/order-state.json), shown at the start of
every session and enforced by the `order-gates` check. Before acting on a request, name
its step and check that step's gate. Without a hashed contract there is no programme
work; stopping or shrinking needs none.

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
   ruling after a Codex-verified CONFIRMED result, under its own contract.
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
  place, in Joshua's primary checkout. Never copy, edit or upload them.
- **Output.** No Private or Licensed content in commits, PR text or STATE. Backtest
  dollar figures go only in lab `RESULTS` files. Exclude per-bar series and timestamped
  price levels from anything agents report.
- **Data changes** under `core/data/` carry a matching `SHA256SUMS` update. Don't bypass
  hooks with `--no-verify`.
- **Other services.** Nothing Secret, Private or Licensed goes to any service but Claude
  and Codex, except what Joshua sends himself.

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
- **One writer per branch.** The owning session names the candidate head; the other
  agent reviews that exact head and does not push to it.

## Code Review Rules

Report what changes behaviour or breaks a rule; skip style. Blocking:

- **Leaks:** anything the data rules forbid, including paraphrased strategy parameters.
- **Money-control breaches:** frozen-parameter edits without recorded approval; any code
  that can place, arm or route orders.
- **Order breaches:** a registration changed after its test started, a threshold
  loosened after an outcome, a successor during quarantine, or a weakened `order-gates`.
- **Fixes that hide failures:** broad exceptions, silent defaults, looser schemas,
  success exits on error, a skipped or weakened test, or "not checked" read as clean.
- **Unbacked claims:** a result with no command or output behind it.

On a re-review, review only commits since your last reviewed head.

## Running code

`.\fp.ps1 <command>` in PowerShell or `python -I scripts/fp.py <command>` (`doctor`,
`check`, `test`, `python ...`). Layer boundaries: `core/` imports nothing internal, and
`lab/` and `ops/` never import each other.
