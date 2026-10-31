# First Passage agent instructions

## Purpose

Research and operations for automated futures strategies at
`core/firm_rules.AUTOMATION_FRIENDLY_PROP_FIRMS`. Mission:
**generate → evaluate → deploy → measure → update**.

Start with [STATE.md](STATE.md) for priorities and obligations, then the owning
campaign plan (steps) and record (evidence); [PIPELINES.md](PIPELINES.md) covers
handoffs, [REPO_MAP.md](REPO_MAP.md) code, [SESSIONS.md](docs/SESSIONS.md) history.
Direct operator instructions govern the current task; do not infer new work or
authorization from historical dispatches.

This is the only agent instruction file; a dated record's `CLAUDE.md §X` means
`AGENTS.md §X` ([charter addendum](docs/adr/2026-07-16-root-doc-charter-dedup.md#addendum-2026-09-20--the-agent-constraints-root-is-agentsmd-claudemd-retired)).
The [surface-allocation ADR](docs/adr/2026-07-14-cc-cursor-surface-allocation.md) owns
seats and escalation-lane triggers
([M-26 … M-48](docs/methodology/lessons/methodology_lessons.md) hold the evidence).
Chip tasks, handoffs and dispatch cards run in the cloud by default. One that must
run locally says **"Must run locally"** near its top, with the reason (for example
the private read surface below, the operator's machine or VM, or private evidence
writes). Operator direction 2026-10-13.

Decisions live with their owning specification, campaign, plan or PR; ADRs follow the
[admission rule](docs/adr/2026-08-08-adr-ceremony-tiering.md); other documents link the
owner or label a derived mirror ([operational_rules §7](docs/operational_rules.md)). Documents must
serve the pipeline and pass the [retention test](docs/operational_rules.md#16-retention--an-artifact-must-earn-its-place-and-deletion-is-classified-by-execution-not-by-folder);
removed evidence is retrievable via [archive guidance](docs/ltm/README.md) and
[lab/ARCHIVED.json](lab/ARCHIVED.json).

## Core rules

"Rule N" means only this list. Each line is a gist; the full ruled statement and its owners are in
[operational_rules §Core rules](docs/operational_rules.md#core-rules--full-statements), and older
records resolve through the [legacy citation map](docs/operational_rules.md#legacy-citation-map).

**Authority, review and orientation**

- **Rule 0 — Audit first.** Read the source or primary artifact before any claim, brief, decision or edit; verify premises and returned work; no review round on an unobserved, unnamed external fact. [→](docs/operational_rules.md#rule-0--audit-first)
- **Rule 1 — Small-cell variance prior.** Small samples and streaks are variance: no change, override or regime overlay on them. [→](docs/operational_rules.md#rule-1--small-cell-variance-prior)
- **Rule 2 — Budget before acting.** Budget substantial work in one line (iterations including review rounds, plus $ and K); stop structurally at the bound. [→](docs/operational_rules.md#rule-2--budget-before-acting)
- **Rule 3 — The operator decides; grants are literal.** Operator instructions govern; grants are literal; operator acts need direction or a named standing GO; refusals are reported; scope cuts, new assumptions, evidence-claim changes and account permissions are his. [→](docs/operational_rules.md#rule-3--the-operator-decides-grants-are-literal)
- **Rule 4 — Seats, action classes and cards.** Act within seat grants and the card's authority block; cards only narrow; frozen cards return contradictions. [→](docs/operational_rules.md#rule-4--seats-action-classes-and-cards)
- **Rule 5 — A separate reviewer.** Codex reviews Claude's work and Claude reviews Codex's; neither reviews its own, including the pre-ratification adjudication. [→](docs/operational_rules.md#rule-5--a-separate-reviewer)
- **Rule 6 — PRs and merges.** Land by PR; merge pinned to a head the other agent reviewed clean (within three, or a clean fourth, counted per reviewer) with all checks green. [→](docs/operational_rules.md#rule-6--prs-and-merges)
- **Rule 7 — Stop after two failed corrections.** After two failed corrections of one failure family, stop and restart cleaner in a fresh coordinator session; at a review stop, ship only reviewer-marked non-blocking residuals, or ask the operator. [→](docs/operational_rules.md#rule-7--stop-after-two-failed-corrections)
- **Rule 8 — Orient and dedup first.** Orient from STATE and the owner; dedup with pasted search output before new work. [→](docs/operational_rules.md#rule-8--orient-and-dedup-first)
- **Rule 9 — Name the question; pick the loop.** Name the question and the decision it changes; pick the loop tier by reversibility. [→](docs/operational_rules.md#rule-9--name-the-question-pick-the-loop)

**Frozen controls (point to, never weaken)**

- **Rule 10 — Live-execution gates.** Arm, spend, trade, deploy and reach hosts only as the gates and operator direction allow. [→](docs/operational_rules.md#rule-10--live-execution-gates)
- **Rule 11 — Rail operating invariants.** Fresh tags, sends are not fills, IN_DOUBT reconciled, protective actions never wait, attended only. [→](docs/operational_rules.md#rule-11--rail-operating-invariants)
- **Rule 12 — Credentials.** Own scoped credentials only; no operator tokens, no Fly or broker credentials; never embed secrets. [→](docs/operational_rules.md#rule-12--credentials)
- **Rule 13 — Private data and the public clone.** No account data, locked figures, vendor CSVs, Pine or ports in commits; private surface read in place only; data moves by class, and Codex never receives Pine, ports or account data. [→](docs/operational_rules.md#rule-13--private-data-and-the-public-clone)
- **Rule 14 — Locked parameters and protection.** Locked parameters, allocations and Pine are immutable; protection changes only through its gate chain. [→](docs/operational_rules.md#rule-14--locked-parameters-and-protection)
- **Rule 15 — Capital authorization is separate and revocable.** Lock, capital authorization and deployment are separate axes; authorization moves down only; nothing grants capital. [→](docs/operational_rules.md#rule-15--capital-authorization-is-separate-and-revocable)

**Firms, venues, data and figures**

- **Rule 16 — Firm rules: one source and a pre-flight.** Firm rules live once in core/firm_rules.py, carry starting_balance, pass the pre-flight. [→](docs/operational_rules.md#rule-16--firm-rules-one-source-and-a-pre-flight)
- **Rule 17 — Venue facts: quote, source, date, scope.** Record venue obligations verbatim with source, date and scope; silence reads broad. [→](docs/operational_rules.md#rule-17--venue-facts-quote-source-date-scope)
- **Rule 18 — Feeds are admitted, never assumed.** Only the admitted canonical feed; retired feeds stay retired; research never wires to live. [→](docs/operational_rules.md#rule-18--feeds-are-admitted-never-assumed)
- **Rule 19 — Vendor-data integrity.** SHA256SUMS delta with each data change; hooks installed; no --no-verify as routine. [→](docs/operational_rules.md#rule-19--vendor-data-integrity)
- **Rule 20 — Figures come from their owner.** Quote figures only from their owner; never invent, extrapolate or transplant them. [→](docs/operational_rules.md#rule-20--figures-come-from-their-owner)

**Verification**

- **Rule 21 — Report verification honestly.** Report verification exactly; a pass needs a completed clean record; disclose failures. [→](docs/operational_rules.md#rule-21--report-verification-honestly)
- **Rule 22 — Use the checkout's launcher.** Run project Python through the checkout's fp launcher; no silent fallback or new dependency. [→](docs/operational_rules.md#rule-22--use-the-checkouts-launcher)

**Research**

- **Rule 23 — Pre-register; count K honestly.** Freeze criteria before results; count K honestly; frozen gates reachable and binding. [→](docs/operational_rules.md#rule-23--pre-register-count-k-honestly)
- **Rule 24 — Verdicts from the pre-registered gates, in order.** Verdicts come mechanically from the pre-registered gates, in the evaluation order. [→](docs/operational_rules.md#rule-24--verdicts-from-the-pre-registered-gates-in-order)
- **Rule 25 — Generation never blesses.** Discovery and harvest produce candidates only; intake, manifest and K carry into validation. [→](docs/operational_rules.md#rule-25--generation-never-blesses)
- **Rule 26 — Rejections bar re-proposal.** Re-propose a rejection only with new mechanism evidence; every closure names its Registry line. [→](docs/operational_rules.md#rule-26--rejections-bar-re-proposal)
- **Rule 27 — Instrument ledgers.** Read the instrument ledger before work on it; append a dated disposition after. [→](docs/operational_rules.md#rule-27--instrument-ledgers)
- **Rule 28 — Closures, falsifiers and audits.** Typed Iterate exits; falsifiers never move; retired inputs migrate their falsifiers; audits on cadence. [→](docs/operational_rules.md#rule-28--closures-falsifiers-and-audits)

**Records and communication**

- **Rule 29 — One canonical owner per fact.** One canonical owner per fact; link or label mirrors; amend the owner before minting. [→](docs/operational_rules.md#rule-29--one-canonical-owner-per-fact)
- **Rule 30 — Correct where the error is read.** Delete superseded wording on living surfaces; correct frozen evidence by addendum where read. [→](docs/operational_rules.md#rule-30--correct-where-the-error-is-read)
- **Rule 31 — Artifacts earn their place.** Keep only what passes the retention test; migrate obligations before deleting; verify retrieval. [→](docs/operational_rules.md#rule-31--artifacts-earn-their-place)
- **Rule 32 — ADRs only under the admission rule.** ADRs only under the admission rule; approved revisions keep the prior; Proposed decides nothing. [→](docs/operational_rules.md#rule-32--adrs-only-under-the-admission-rule)
- **Rule 33 — Cards, briefs, notices and lessons follow their form.** Cards carry the full contract; observations route through the notice log; lessons are cited. [→](docs/operational_rules.md#rule-33--cards-briefs-notices-and-lessons-follow-their-form)
- **Rule 34 — STATE, SESSIONS and CATALOG stay current and thin.** STATE points to owners and stays current; SESSIONS append-only; CATALOG and INDEX generated. [→](docs/operational_rules.md#rule-34--state-sessions-and-catalog-stay-current-and-thin)
- **Rule 35 — Fewest words.** Fewest words; link the owner; keep a verdict's reading limits. [→](docs/operational_rules.md#rule-35--fewest-words)
- **Rule 36 — Subtract, then improve once.** Cheapest trustworthy evidence; add no new layer without a decision; one durable fix per mechanism. [→](docs/operational_rules.md#rule-36--subtract-then-improve-once)

**Engineering and routing**

- **Rule 37 — Layer boundaries.** core imports nothing internal; lab and ops never import each other. [→](docs/operational_rules.md#rule-37--layer-boundaries)
- **Rule 38 — Gates and tooling.** gates.yml alone composes gates; checkers fail closed; skills publish only by release. [→](docs/operational_rules.md#rule-38--gates-and-tooling)
- **Rule 39 — Configuration as code.** Configuration as code: define once, layer explicitly, validate where consumed. [→](docs/operational_rules.md#rule-39--configuration-as-code)
- **Rule 40 — Root cause and contract first.** Name the root cause before a fix; no band-aids; design from an invariant table. [→](docs/operational_rules.md#rule-40--root-cause-and-contract-first)
- **Rule 41 — Route, host and delegate deliberately.** Cloud by default unless 'Must run locally'; always-on hosts; split oversized work; relays only relay. [→](docs/operational_rules.md#rule-41--route-host-and-delegate-deliberately)

## Live-execution posture

**Recorded posture:** the incumbent `Tradeify_Select_100K` eval exists; c1 is warm and **disarmed** (`dry_run=true`) with no deployed book; daemon `emit_enabled=false`. Confirm actual host state before operational work. M1 is recorded `RESOLVED` (`docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json`; [A8 record](docs/notes/rail_build/M1_STAGE1_DEPLOYMENT_READINESS.md#a8--signed-acceptance-deployed-re-bake-verified-2026-09-14), 2026-09-14), so `fp check` printing `status=RESOLVED` is expected, not a posture conflict; it covers the incumbent's Stage 1 monitoring only, and arming still needs every other gate below. A new instance (for example the personal account) needs its own M1 acceptance.

**Data source (operator report 2026-09-10):** Databento is [retired](docs/adr/2026-07-10-databento-research-stack.md#addendum-2026-09-10---operator-retirement-of-databento) and unsubscribed; no replacement is approved; daemon emission stays blocked.

- `dry_run=false` requires M1 `RESOLVED`: the gate's object is the **arm**, not the send.
- Disarm **before** absolute `armed_until` expiry; lapse-while-armed previously caused a host crash-loop.
- Live spend requires M1 `RESOLVED` **and** separate operator GO; every armed session needs its own GO.
- **Agents may place orders, exit positions and cancel orders when directed by the operator**, including through computer use ([operator amendment 2026-09-30](docs/adr/2026-07-14-cc-cursor-surface-allocation.md#addendum-2026-09-30b)); arming, live-spend and per-session operator GO requirements still apply. Weekly account-preservation trades may be operator- or agent-placed; under the operator's standing, revocable GO (2026-10-25, same addendum) an agent needs no per-trade direction for them; deadline in [STATE](STATE.md#scheduled-forward-triggers).
- The arming interlock (`ops/c1_rail/c1_rail_arm.py` calling `validate_c1_monitoring_acceptance.validate(require_resolved=True)`) gates only the arm helper. It checks structure, `RESOLVED` status and `operator_signoff` presence, not a signature: a status-only file fails; a complete forged `RESOLVED` file passes. The rail host's boot gate (`c1_rail_http_server.load_config`) does not check M1, so editing the `/data` config bypasses it; the host-side activation gate is owed ([self-funded lane ADR item 8](docs/adr/2026-10-09-self-funded-tradovate-lane-reopen.md#addendum-2026-10-25--owed-item-8-host-side-activation-gate-from-tb-i3), from TB-I3). `--acknowledge-m1-unresolved` overrides a structurally valid unresolved artifact (operator-ratified discretion; writes an `arming_deviation` record); agents may invoke it only through the operator-act prompt ([ruling 2026-09-26](docs/adr/2026-07-14-cc-cursor-surface-allocation.md#addendum-2026-09-26)).

**Account:** used, not pristine; canned-payload and weekly token trades have filled, but no strategy-signal fill has occurred. `order_id` idempotency is **DISPROVEN**; every payload gets a fresh tag. Private account figures stay private.

| Standing consequence | Owner |
|---|---|
| Incumbent environment retained; no successor migration | [S1](docs/adr/2026-08-07-loop-s1-environment-ratification.md) |
| Python daemon → listener; TV login automation prohibited | [S2](docs/adr/2026-08-07-loop-s2-signal-host-fork.md), [daemon build](docs/adr/2026-08-08-s2b-signal-daemon-build.md) |
| Withdrawn Striker editions stay barred; separate campaign expressions are conditionally eval-eligible | [withdrawal](docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md), [readmission](docs/adr/2026-09-05-tradeify-select-striker-expression-readmission.md) |
| Rail build/account registration GO; spend ceiling $700 | [rail GO](docs/adr/2026-07-17-c1-rail-build-account-registration-go.md) |
| Licensed test strategy can discharge M1 item 5 / B7 Stage 1 independently of strategy selection | [M1 addendum](docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md#addendum-2026-08-24--test-strategy-licensed-for-item-5-dated-08-24) |
| Four-firm program falsifier remains dated 2026-11-08; Tradeify counts again | [program](docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md), [F1 reversal](docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md#addendum-2026-09-01--f1-reversed-a-tradeify-resting-discharge-now-counts-toward-4) |
| Tradeify eval accounts: strategy logic must be native, with no external engine, bridge or direct API (support, 2026-10-12); Track B superseded for Tradeify 2026-10-16; the weekly trade (supported platform only, never CrossTrade or the API) and the personal lane continue, with Q-SFCLEAR-3 dispatch paused (2026-10-19) | [route record](docs/briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md#addendum-2026-10-12-later--tradeify-support-strategy-logic-must-be-native-for-evaluation-accounts), [supersession](docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-10-16--track-b-superseded-for-tradeify), [pause](docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-10-19--no-book-lineage-configuration-has-an-evidence-case-for-the-tradeify-evaluation) |

## Strategy Reference (LOCKED legacy book — do not modify)

Locked parameters: [`core/strategies/CATALOG.md`](core/strategies/CATALOG.md) §Locked
parameter record. **No live venue, not a live book;** live sizing authority is
`dd_protection.BASE_RISK` / `firm_rules._BASE_RISK`; every other strategy parameter
lives in **Pine only**.

MC calibration — **99.83% pass / 0.17% bust, p99 DD 4.37%** — is **historical record, not a
live claim** ([`docs/mc_anchor_history.md`](docs/mc_anchor_history.md)). ⚠ Keep these literals **here**:
`ops/recall/guard.py` regex-reads them from this file for its denylist; `mc_anchor_history.md`'s
first match is a *different* (Q-SWAP) triple, so moving them denylists the wrong numbers.
Reword only alongside that parser.
Read effective lifecycle multipliers from `core/lifecycle.py` and its state, never from historical rail
operation; [strategy_lifecycle.md](docs/methodology/strategy_lifecycle.md) owns the lifecycle and
[venue editions](ops/venue_editions/Tradeify_Select_100K.md) the venue binding.
Engine regression is vendor-free (`tests/core/test_mc_synthetic_engine.py`). Canonical feed: CME
futures TV exports (`core/data/tv_exports/cme/`); OANDA and Pepperstone are retired.

## Protection

Single rule in `dd_protection.py`, consumed by the rail's sizing path. **Unused today**: no
strategy is deployed.

* **DD tier:** if `(equity − peak) / peak ≤ −0.015`, multiply the day's sizing by **0.40×**.
  Clears automatically when equity returns to peak.
* **`DD_TRIGGER` 1.5% / `DD_SCALE` 0.40× are frozen** and guarded at import
  (`_validate_protection_rule`). Change-control runs **only** through: pre-registration → re-MC →
  **both-halves** regime-robustness gate → admitting ADR.
  Lock provenance: [C2 relock](docs/adr/2026-05-08-dd-trigger-c2-relock.md) ·
  [ULP rounding](docs/adr/2026-05-10-dd-protection-ulp-rounding.md).
* **Concept-not-constant:** the mechanism is invariant; `(trigger, scale, reference_mode)` are
  per-(portfolio, firm-tier) variables ([ADR](docs/adr/2026-07-13-dd-protection-concept-not-constant.md)).
* ⚠ The prior equity tier was deleted 2026-04-17 and **its revert triggers are LOST**.
  Reintroducing a second tier needs **fresh pre-registration**, not a lookup.

## Continuous improvement

During authorized work, actively notice concrete plan flaws, preventable mistakes,
recurring failures and evidenced waste; at planning, correction and completion moments
use [agent-improvement](.claude/skills/agent-improvement/SKILL.md) when such an
opportunity appears (read its source if the harness does not list it); no opportunity
means no extra reflection artifact or task. Implement and verify a local, reversible,
evidence-supported improvement that fits the current task and seat without changing
outcome or acceptance criteria; existing authorization carries forward, so do not ask
again merely because it is an improvement. This includes repairing an agent-owned
execution sequence before it fails. Bounds:

1. Authority is the task's existing authorization, bounded by the seat's grants in
   [`scripts/seat_authority.yml`](scripts/seat_authority.yml) and any authority block on
   the current card, under the surface-allocation ADR's
   [action classes](docs/adr/2026-07-14-cc-cursor-surface-allocation.md#action-classes-and-the-authority-block).
   An improvement is never an operator act or a forbidden capability.
2. A frozen worker card stays frozen: a worker returns contradictions, scope changes
   and improvement evidence to its coordinator; other seats route out-of-scope changes
   by seat under that ADR.
3. At most one durable intervention per failure mechanism, at the cheapest reliable layer:
   source fix or test (`tests/`) → hook ([`scripts/gates.yml`](scripts/gates.yml),
   `scripts/githooks/`, `.claude/hookify.*.local.md`, harness hooks in
   [`.claude/settings.json`](.claude/settings.json)) → skill (`.claude/skills/`) →
   AGENTS.md → ADR/lesson ([`docs/adr/`](docs/adr/),
   [`docs/methodology/lessons/`](docs/methodology/lessons/), indexed in
   `docs/methodology/LESSONS_INDEX.jsonl`).
4. Retain evidence with the existing task/plan/PR/campaign owner, writing into an owner
   record only when the current card's authority block grants `governance.author` (no
   card: only an owner the direct operator instruction puts in scope); otherwise route
   evidence through the task return.
5. Promote one-off feedback into standing guidance only when high-severity or
   independently recurring.
6. Do not edit standing instructions unless the user requests it. Registering or
   changing a harness hook in `.claude/settings.json` counts: unasked, propose it;
   requested, implement it within item 1's authority.

After two failed corrections of the same issue, stop, summarize what was learned,
and restart with a cleaner prompt and explicit verification criteria — on the
escalation lane the surface-allocation ADR names, not as a third retry.

## Public-clone posture

This repository is public ([transition ADR](docs/adr/2026-08-14-repo-public-visibility-transition.md));
private history is in `first-passage-archive` ([retrieval guidance](docs/ltm/README.md)).
Do not commit account identifiers/P&L, vendor-licensed CSVs, Pine source, or
executable Python ports of locked strategy logic. `SHA256SUMS`,
`core/strategies/MANIFEST.sha256` and `core/strategies/PORT_MANIFEST.sha256` pin
private sources; new locked ports follow the same policy. Vendor-dependent tests skip
when inputs are absent. `core/data/bar_data/` is retained: usable panels that change
only by a fresh operator CME export plus its SHA256SUMS delta.

**Private read surface.** Agents may read the accepted book's four Pine sources and
accepted runtime ports listed in `core/strategies/BOOK_SOURCES.sha256`, and the effective-input
file `ops/c1_signal_daemon/ports/effective_inputs.json` (§60 addendum 2026-10-02), in place in
the operator's primary checkout (from a worktree, by that checkout's absolute path).
Never copy them into a worktree, commit or quote their bodies or values, edit them,
or pass them to any external service
([campaign §60](docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md#60--agent-read-access-to-the-accepted-books-pine-and-runtime-ports-2026-09-25)).
The single exception covers the ports and `effective_inputs.json` (not Pine), copied to the Joshua-controlled Windows VM only for the runs, and on the terms, that the [§60 VM addenda](docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md#60--agent-read-access-to-the-accepted-books-pine-and-runtime-ports-2026-09-25) (2026-10-07 onward) admit; the [VM policy](docs/governance/azure-compute-vm-policy.md) owns the standing host rules.

**Data movement (Joshua, 2026-10-28).** These rules apply by data class, whatever the
source: a private local area, the archive, the VM or this repository.

- *Providers.* Whatever an agent may read may reach that agent's own provider (Anthropic
  for Claude, OpenAI for Codex). Handing data to another agent or service follows that
  recipient's permissions.
- *Codex.* Codex never receives Pine, runtime ports, `effective_inputs.json` or account
  data, and does not read them in place. Public research figures in PRs it reviews are exempt.
- *Archive.* Claude may read `first-passage-archive`. Anything extracted from it follows
  these class rules, and a Codex ticket carries only identities, hashes, windows and counts.
- *Research backtest dollars.* Allowed in lab `RESULTS` files only, never in PR text, cards,
  STATE or briefs; elsewhere cite the RESULTS file or a hash.
- *Account data.* Agents read it only for a task that names it, and never quote it or hand it off.
- *Private inputs.* An input a frozen run binds lives in a registered location with a hash
  index (`SHA256SUMS`, `BOOK_SOURCES.sha256` or `docs/evidence/PRIVATE_EVIDENCE.sha256`).
  New public text cites private inputs by repo-relative path and hash, never by an absolute
  home path. Archive links in public docs are fine.
- *Derived outputs (Joshua, 2026-10-28).* A figure derived from a private export keeps that
  export's class, except these fields, which lab analysis files may publish with the source
  hash: the hash match, trade count, date window, and aggregate counts of venue-rule breaches
  (e.g. trades held past a flat deadline or over a weekend). Never prices, P&L, sizes,
  parameter values, per-trade timestamps or trade lists.
- *Existing text.* These rules apply from now on. Editing a file does not remove the content
  from git history, and rewriting history is a separate operator decision.

### Gate composition authority

[scripts/gates.yml](scripts/gates.yml) and its runner own gate composition,
[scripts/README.md](scripts/README.md) the command entry points; do not maintain a
parallel gate list. `main` requires a PR and the `skills (3.12)` status ([Q-GATESTACK-1's addendum](docs/briefs/closures/Q-GATESTACK-1-closure-falsified.md)
records the ruleset); other path-filtered checks are not required merge checks.

**Merges and credentials (Joshua, 2026-10-24).** An agent may merge a PR, pinned to its head SHA, once the other agent's review at that head (Codex for Claude's PRs, Claude for Codex's) comes back clean and every CI check is completed and green; auto-merge stays forbidden. After fixing Codex findings, push and comment `@codex review` for a fresh review of the new head. A PR may merge only if a review is clean within three reviews, or on a clean fourth (amended 2026-10-25); Claude reviews count toward that limit as Codex reviews do, and on a mixed-author PR each agent's reviews have their own count (rulings 2026-10-29: [Claude reviews](docs/adr/2026-07-14-cc-cursor-surface-allocation.md#addendum-2026-10-26--operator-ruling-cross-agent-review), [mixed-author PRs](docs/adr/2026-07-14-cc-cursor-surface-allocation.md#addendum-2026-10-29--operator-ruling-mixed-author-prs)); otherwise stop fixing and return it to its original owner for a rewrite. Review is cross-agent: Codex reviews Claude's work and Claude reviews Codex's ([ruling 2026-10-25](docs/adr/2026-07-14-cc-cursor-surface-allocation.md#addendum-2026-10-25--operator-ruling-claude-does-not-review-its-own-work), [2026-10-26](docs/adr/2026-07-14-cc-cursor-surface-allocation.md#addendum-2026-10-26--operator-ruling-cross-agent-review)). Agents act under their own scoped credentials (a repo-scoped GitHub PAT), never the operator's tokens, and hold no Fly or broker credential ([Addendum 2026-10-24b](docs/adr/2026-07-14-cc-cursor-surface-allocation.md#addendum-2026-10-24b--operator-rulings-conditioned-merge-go-and-credential-custody)).

## Python environment and local checks

- Use the launcher of the checkout being tested: `.\fp.ps1 doctor` before project Python work; `.\fp.ps1 python ...` for operations Python; `.\fp.ps1 test`, `test-ops` and `check` for the standard suites and gates; `.\fp.ps1 python -m pytest <paths>` for selected tests. Without PowerShell 7.3+: `python -I scripts/fp.py <command>`.
- If validation fails, diagnose it ([launcher setup](scripts/README.md#local-operations-launcher)); never silently fall back to system Python or bypass validation. Keep the separately pinned research environment separate.
- When project Python starts another Python process, use `sys.executable`, not bare `python`.
- Report the command, interpreter, tested revision or working-tree state, and actual results. Disclose any pre-existing gate failure; do not describe the complete gate suite as passing.
- Cite the printed `record.json` and keep source and Git state unchanged while a recorded check runs. A verification claim needs `status: completed`, exit zero, stable source, complete capture, valid expected reports and, where applicable, successful Docker cleanup ([record format](scripts/README.md#automatic-verification-evidence)); `not_started`, `running`, `failed` and `interrupted` are not acceptance. Never infer a pass from a record merely existing.
- **Standing CI substitution (Joshua, 2026-10-16):** when a local full suite (`fp test` or `test-ops`) does not complete only because a qualification child hits the local 3,600 s timeout, the PR's CI at the same head, with every check COMPLETED and green, substitutes for that local run. No per-PR ruling is needed. The return still discloses the timeout and cites the incomplete record, so the local run never counts as a pass. Any other local failure needs a clean-base reproduction, or else a fix.
- For independent pytest cases, select the affected tests first, then add workers: `.\fp.ps1 --workers 2 python -m pytest <paths>`; worker count does not replace related-case coverage. Docker sequence checks use `tools/local_verification/run.ps1` and are recorded too.

## Configuration as code

Default to configuration as code for new or changed configuration, especially when
reused; apply it only to configuration the work already touches, preserving accepted
policy behavior. Define reusable objects once in a canonical source that consumers reference or
compose, never copy. Separate shared configuration, product/environment variants and
instance bindings; make overrides explicit; validate the resolved configuration where it
is consumed. Reference credentials; never embed secrets in versioned configuration.
Deployments preserve the resolved configuration's identity/version so validation and
activation refer to the same configuration.

