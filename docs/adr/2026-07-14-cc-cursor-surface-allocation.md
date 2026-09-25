# ADR — Worker-surface allocation: the coordinator designs and adjudicates, workers implement frozen specs

**Status:** Accepted (ratified 2026-07-14)
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Format:** concise — converted from the original full format by the 2026-09-15 revision, which consolidated §0–§10 and six addenda into Decision / Grounds / Current owner plus the §8 disposition table. Prior full-format text at the blob pinned below.
**Decision date:** 2026-07-14
**Revision:** 2026-09-25 — action classes (low / medium / operator act / forbidden) with a
machine-read authority block on cards (handoff contract item 7), approval bound to the exact
object and by acts the operator already performs, the `IN_DOUBT` rule for side effects, the
operator decision-packet format, the enforcement-point table, and the seat-name mapping for
imported organisation proposals. Operator-directed in-session 2026-09-25 ("proceed with your
recommended sequence in full", after a review of three external drafts); ratification pending
operator merge of the PR that carries it. Prior (2026-09-20) effective text, in full and unedited,
at blob `cbe2a5886e3b6588b68294ac801f88acde3637b5`
(`git show cbe2a5886e3b6588b68294ac801f88acde3637b5`), commit `d7af57013b88e11099f5a4b69fdcef7e751597a7`.
**Prior revision (2026-09-20):** three-seat delegation (executive / coordinator / worker) with a Fable
escalation lane, the committed-handoff rule, acceptance tests named in the card, and the
quality-then-attention priority. Operator-directed in-session 2026-09-20 (items 1, 2, 4, 5, 6 of the
delegation review); ratification pending operator merge of the PR that carries it. Prior (2026-09-15)
effective text, in full and unedited, at blob `9a55a9c71e5ebebad87bb0bc8cf6332a486f7541`
(`git show 9a55a9c71e5ebebad87bb0bc8cf6332a486f7541`), commit `4a8067dcba5fe99c27396a61a1aa2043cc9383f7`.
**Prior revision:** 2026-09-15 — **RATIFIED** by the operator in-session ("execute my decisions").
Retires Cursor as a worker surface and rescopes this decision to the surviving surfaces
(Claude Code, Codex); consolidates the six 2026-07-16 → 2026-09-04 addenda into the §8
disposition table. This revised text is the effective decision. Prior decision text, in full
and unedited, at blob `0bcd6699fd683a18b9493e25bb053797dcf4fafe`
(`git show 0bcd6699fd683a18b9493e25bb053797dcf4fafe`), commit
`b448e2b6f852a49c2a46e278ade95a4c4e2c4c54`.
**Supersedes:** `2026-08-14-cc-cursor-autonomous-loop.md` full — its entire subject (Cursor
dispatch without chip approval, `cursor/*` webhook detection, and auto-merge on a binary gate)
retires with the Cursor lane; the surviving general rule is restated in §2 below.
**Authors:** Joshua + Claude Code (2026-07-14); revisions Joshua + Claude Code (2026-09-15, 2026-09-20)
**Related:** [`handoff-verify`](../../.claude/skills/handoff-verify/SKILL.md) (consumer-side gate) ·
[`task-routing`](../../.claude/skills/task-routing/SKILL.md) (canonical local-vs-cloud checklist) ·
[`cc_handoff` template](../../.claude/skills/brief-authoring/references/cc_handoff.md) (producer-side contract)
**Layer:** infrastructure

> ⚠ **REVISED 2026-09-25 — action classes, authority blocks, decision packets** (on top of the
> 2026-09-20 three seats, one escalation lane and committed handoffs, and the 2026-09-15 rescoping
> that retired Cursor). The body below is the effective decision text. The clause-by-clause record of what each revision kept, restated or retired is
> §8. Each revision's pre-revision text is pinned at a blob in the header.

---

<a id="2--decision"></a>

## Decision

Work is routed between **seats** by a four-question test, with an authored handoff brief as
the mechanical eligibility gate. The **executive** sets the goal and the next milestone and
accepts or rejects on evidence; the **coordinator** decomposes, specifies, steers the worker,
integrates and writes the evidence pack; **workers** implement frozen specs and never merge;
the **escalation lane** is a budgeted interrupt, not a standing seat; the **operator** owns
merge and everything irreversible. **Priority order for every routing choice: quality of the
landed change first, operator attention second. Throughput is not a metric.**

**Seats, as of the 2026-09-20 revision** (operator's org chart, in-session 2026-09-20):

| Seat | Model / surface | Allowed to do | Not allowed to do |
|---|---|---|---|
| **Executive** | Codex ("Astra") | Goal, constraints, next milestone; accept/reject on the evidence pack (diff, test log, reviewer dissent) — never on the coordinator's synthesis alone; independent PR review of the diff against the *goal* (the 2026-08-29 addendum #1 review path, retained) | Author tickets, implement, merge |
| **Coordinator** | Claude Code, Opus (default effort; raise effort before changing model) | Decompose the milestone into frozen cards, dispatch, steer, adjudicate `DONE_WITH_CONCERNS`, integrate, write the evidence pack and the campaign record | Be the sole signer on a diff whose card it wrote; implement the hard 20 % by default instead of escalating; touch `main` |
| **Worker** | Z Code (GLM 5.3) sessions; a Claude Code or Codex session may take a packet when the operator routes one there | Bounded implementation, tests, docs and refactors in a worktree against a frozen card; return the four-state status with the evidence the card names | Change architecture, expand scope, resolve a spec ambiguity, write reserved files, merge |
| **Escalation** | Claude Code, Fable 5.1 | Only on a named trigger (below): milestone adjudication, the rebuild after a second failed round, load-bearing contract authoring | Daily decomposition, worker supervision, a second executive |
| **Operator** | Joshua | Merge, GO/NO-GO, every irreversible act, arming | — (no model owns these) |

Worker branches use `glm/`, `codex/` or `claude/`. **Cursor stays retired** (2026-09-15) — no
Cursor lane, no `@cursor` dispatch, no `cursor/*` branches, no `cursor[bot]` allow-listing; that
election carries no falsifier and no review cadence. The 2026-09-15 text described the
coordinator as a Claude Code session with Claude Code and Codex as workers; this revision does not
retire either surface, it names the seat each normally occupies.

**Reviewer ≠ planner.** Whoever wrote the card is never the only signer on the diff it produced.
The executive's PR review and the operator's merge are the independent signatures; the
coordinator's adjudication of a worker return is an input to them, not a substitute. The executive
reviews against its own stated goal, not against the coordinator's cards.

**Committed-handoff rule.** Nothing crosses a seat boundary except as a committed, dated file:
an executive direction lands in `STATE.md`'s operator queue or the owning campaign plan; a
coordinator → worker card lands under `docs/briefs/handoffs/**` (or the lightweight issue below)
at a pinned SHA; a worker return is a pushed branch plus its PR; the coordinator's synthesis lands
in the campaign record or `docs/SESSIONS.md`. A direction that exists only in a chat, or a packet
that exists only untracked on a disk, has not been given and is not dispatchable —
`AGENTS.md` already forbids inferring work from historical dispatches, and a worker cannot tell a
current chat direction from a stale one. Private evidence follows M-41 (primary checkout, never a
worktree). This extends the single-writer rule below to every seat boundary. **One permitted
non-file card:** the lightweight dispatch issue (below), whose freeze is a content hash rather
than a commit SHA; nothing else is exempt.

**Routing test (apply in order).** The tests are about the *work* and the *environment*, not
about which vendor runs the session, so all four survive the retirement unchanged:

0. **Does Phase-0 reading require bytes or credentials not verifiably present in the dispatch
   environment?** Specifically (a) any path under `core/data/tv_exports/**`,
   `core/data/bar_data/**`, `core/data/external/**` (gitignored vendor data), or (b) any API
   key or secret. If yes and unconfirmed-present in the target environment → **local**, full
   stop, regardless of how 1–3 resolve. This binds every remaining surface: Claude Code and
   Codex each have local and cloud modes, and a cloud checkout structurally lacks gitignored
   bytes unless staged for *that* dispatch. Canonical checklist owner:
   [`task-routing`](../../.claude/skills/task-routing/SKILL.md).
1. **Does the task author doctrine or touch a locked/governed surface?** (ADRs, Pre-Qs,
   pre-registrations, closures, lifecycle state, `AGENTS.md`/`STATE.md`/memory; any *edit* to
   `core/` anchor-path code — `dd_protection.py`, `firm_rules.py`, `portfolio_mc.py`,
   `core/mc/*`, `lifecycle.py`, `dd_geometry.py` — or Pine.) → **coordinator**, full stop.
   Read-only imports of `core/` from `lab/` code are fine on any surface. The coordinator may
   perform that authoring on the escalation lane (trigger 3 below); that changes the model it
   works on, never the seat that owns the work.
2. **Is the spec frozen?** Binary acceptance gates, resolved ambiguities, enumerated forbidden
   moves, no judgment calls expected mid-build. If not → the coordinator either does the work
   or freezes the spec first. A worker never resolves a spec ambiguity unilaterally; it bounces
   `NEEDS_CONTEXT`.
3. **Does the build clear the handoff-overhead threshold?** If the build is smaller than the
   brief (rule of thumb: < ~1 focused hour, or fewer than ~3 files touched), it stays on
   whichever surface is already open. Above threshold and spec-frozen → dispatch to a worker.

**Handoff contract (all seven required for worker eligibility):**

- A handoff brief under `docs/briefs/**` passing `check_brief.py`.
- §0 Phase-0 reads with a **read-report-before-code** requirement and a `NEEDS_CONTEXT` bounce
  on any contradiction; the worker runs the [`handoff-verify`](../../.claude/skills/handoff-verify/SKILL.md)
  checklist as that Phase 0.
- §5 forbidden moves naming the locked surfaces the task runs near.
- §0 states explicitly whether any read touches a gitignored vendor-data path or a secret
  (test 0), and if so names the confirmed-present staging/credential check performed for *this*
  dispatch — not a prior one, not a general belief the bytes or key exist "somewhere."
- **Acceptance tests named in the card, before the worker starts.** The card lists the acceptance
  tests by name and, for each, the property it must violate to fail (falsifier-first, as briefs
  already do). Tests the worker writes are additional evidence, never the acceptance basis — a
  worker that writes both the feature and its only tests can encode the defect into green.
  For contract-driven code the card carries the invariant table (M-38); for anything with orders,
  positions or shutdown semantics it carries the state model (M-39).
- **Return contract:** a worker branch (`glm/*`, `codex/*` or `claude/*`), a PR with tests green, and a
  four-state status — `DONE` / `DONE_WITH_CONCERNS` / `NEEDS_CONTEXT` / `BLOCKED`. **No commit
  or merge without the operator.** `DONE_WITH_CONCERNS` is adjudicated by the coordinator before
  merge; `NEEDS_CONTEXT` gets one re-anchor and re-dispatch, then returns to the coordinator
  (two bounces means the spec was not freezable and the packet was mis-routed). The coordinator
  owns that return and performs the restart on the escalation lane (trigger 1 below) rather than
  re-dispatching a third time; see *Ownership and precedence* there.
- **Authority block (added 2026-09-25):** one fenced block whose info string is `yaml authority`, naming the
  `seat`, the `parent` card, `max_risk`, the granted `capabilities`, the `constraints` (every
  parent constraint restated) and the `acceptance` test names from item 5. Capability names come
  from [`scripts/seat_authority.yml`](../../scripts/seat_authority.yml);
  [`scripts/check_handoff_authority.py`](../../scripts/check_handoff_authority.py) enforces the
  rules under *Action classes* below. Required of every worker card authored after this revision
  is ratified; historical cards are not retrofitted and the checker skips a card with no block.

**Scoped exception — the lightweight dispatch issue** (2026-08-29 addendum #2, retained in shape
by §8; scoped 2026-09-16 after post-merge review; re-scoped 2026-09-20 to the six-item contract).
For a small, precedented fix, a complete GitHub-issue body stands in place of item 1's
`docs/briefs/**` brief only when it carries items 2–6 in full: the §0 read-report-before-code
requirement with the `NEEDS_CONTEXT` bounce, the §5 forbidden moves naming the nearby locked
surfaces, the test-0 vendor-bytes/secret declaration with its confirmed-present check, **the
acceptance tests named before the worker starts — each with the property it must violate to
fail — exactly as item 5 requires of a brief**, and the four-state return contract. Since
2026-09-25 it also carries item 7's authority block; the checker does not run on an issue, so the
coordinator's read comment records that the block passes the same rules by hand.
`check_brief.py` does not run on an issue; its place is taken by the coordinator's own
pre-dispatch read of the issue body against
[`handoff-verify`](../../.claude/skills/handoff-verify/SKILL.md), recorded in the issue.

*How an issue's frozen content is preserved.* An issue body is editable and lives outside git, so
its freeze is a **content hash, not a commit SHA**: the coordinator's pre-dispatch read comment
records `sha256` of the issue body exactly as read (`gh issue view <n> --json body -q .body |
sha256sum`) with the read date; the worker recomputes the hash at Phase 0 and returns
`NEEDS_CONTEXT` on any mismatch, exactly as a stale brief-pointer SHA does; the return PR body and
the coordinator's integration record cite `#<n> @ sha256:<hash>`. GitHub retains the issue's edit
history, so the hashed text stays retrievable; an issue edited after the read comment is a new
card that needs a new read. An issue missing any of items 2–6, or lacking the read comment with
its hash, is not a lightweight brief but an unfrozen spec, and test 2 keeps it with the
coordinator. The launch action is the coordinator opening a worker session against the issue; an
issue with no session opened on it dispatches nothing.

**Proactive dispatch and the environment GO compose; neither removes the other** (2026-09-16
clarification). Test 3's proactive reading — act, don't merely label — is authority over the
*dispatch decision*: an eligible packet is dispatched without a per-task "dispatch this"
confirmation. It is not authority over the *environment*. A worker routed to a cloud environment
still needs [`task-routing`](../../.claude/skills/task-routing/SKILL.md)'s GO (its step 3) unless
the operator already chose the environment for that work (its step 1); a proactive dispatch to a
worker session on the operator's own machine needs neither.

**Escalation lane (Fable 5.1) — named triggers only.** Fable is not a seat; it is an interrupt
with a budget (one milestone review per milestone, one unstick per day, unless the operator
raises it). It fires on exactly these triggers, and the coordinator states the trigger in the
dispatch:

1. **Two-failure rule.** The same card, or the same module, has failed twice under
   coordinator + worker (a second `NEEDS_CONTEXT`, a second red acceptance run, or a second
   review round whose finding count did not fall — M-37/M-38). The restart that `AGENTS.md`
   §Continuous improvement already requires ("stop, summarize, restart with a cleaner prompt")
   is taken on Fable as a **rebuild from invariants or from the state model**, not as a third
   worker retry and not as a third fold. Raising Opus effort is tried first when the failure is
   a reasoning gap rather than a missing model.
2. **Milestone adjudication.** Before the operator ratifies a campaign gate, an ADR, a
   pre-registration or a closure, the refute-first pass that M-42 requires (`fable-judge`,
   `pre-ratification-adversarial-panel`) runs on Fable. The diff reviewer does not cover this
   gate (M-47).
3. **Load-bearing contract authoring.** A card or spec that touches routing test 1's locked
   surfaces or the rail is authored (or rebuilt after a failed round) on Fable; daily cards are
   not.

**Ownership and precedence.** The escalation lane is not a seat. Dispatching to it is an act of
the coordinator, the item stays on the coordinator's board, and the result returns to the
coordinator for integration and to the executive for the next direction like any other return.
Wherever older wording in this ADR sends an event to the coordinator — routing test 1's
"→ coordinator, full stop", the return contract's second `NEEDS_CONTEXT` bounce — and a trigger
above names Fable for the same event, both hold and this paragraph governs: **the coordinator owns
the item and executes the named rebuild or authoring on Fable instead of in its default session.**
No trigger transfers ownership, and none of the three triggers may be read as a worker retry on a
stronger model.

Fable never takes the coordinator seat, never supervises the worker day to day, and never
sits beside the executive as a second planner.

**Merge authority is the operator's, with no automated exception.** The 2026-08-14 binary
auto-merge gate is retired with the mechanism it drove (§8). Neither a green CI run, nor a clean
automated review, nor an adjudication verdict is merge authority.

**Orchestrating more than one worker at a time.** When work decomposes into 2+ independent
spec-freezable packets, the coordinator owns the claim manifest and every packet still clears
tests 0–3 individually. How the work is cut — the oversize tells, the six-point atomic-unit
test, the parent manifest and its lifecycle, and the re-cut after a second `NEEDS_CONTEXT` — is
owned by [`work-decomposition`](../../.claude/skills/work-decomposition/SKILL.md) (back-pointer
added 2026-09-16); this clause governs what happens to the children it produces. Three rules
carried enough dated failure evidence to survive the
retirement of the skill that stated them:

- **Disjoint file footprints.** No two packets touch the same file. `docs/SESSIONS.md`,
  `STATE.md`, campaign-state files, and all board/index files are **reserved to the
  coordinator's integration commit** — the single-writer rule. Workers never write them.
- **Dispatch-moment Phase-0 re-check, not authoring-moment.** Re-verify each packet's premises
  against current `origin/main` at dispatch, with an explicit no-op condition ("if already fixed
  on main → return DONE, cite the commit"). Three artifacts were overtaken between authoring and
  dispatch on 2026-07-24 alone.
- **A brief's review round is part of the freeze, not a track running alongside the builds.** The
  umbrella brief's pre-dispatch review must have COMPLETED and any re-freeze it produced must be
  merged to `main` **before the first packet is dispatched**. Dispatching from the brief as first
  opened is a forbidden move.
- **The dispatch pointer carries the brief's frozen SHA** — the post-review-round freeze, never
  the as-first-opened commit. A worker whose pointer SHA no longer matches the brief on `main`
  returns `NEEDS_CONTEXT` rather than building: a stale pointer is a stale spec, and building it
  anyway is how a withdrawn packet gets built.

  Both rules are paid for by SESSIONS `2026-09-04f`: all three workers were fired from `af0203f`
  while the review was still running; the re-freeze withdrew packet B (built anyway, #304 closed
  without merge) and moved packet C's guard mid-build (C falsified, fix round C1 owed). Relay lag,
  not worker error — the workers had no SHA to notice the drift by. Ratified as
  [#402](https://github.com/Joshua-Asante/first-passage/pull/402) against the `cursor-fleet`
  skill on 2026-09-15 and carried here verbatim in substance when that skill was deleted the same
  day; nothing of #402 is lost.

<a id="action-classes-and-the-authority-block"></a>
**Action classes and the authority block (2026-09-25).** Every consequential act falls in one
class. The registry [`scripts/seat_authority.yml`](../../scripts/seat_authority.yml) is the one
canonical list of capability names, their class and which seat a card may grant them to.

| Class (registry name) | Meaning | Examples | Who may do it |
|---|---|---|---|
| **low** (`low`) | Read-only or isolated | read the repo, local tests, edits in the card's own worktree, lab research inside its campaign contract | any seat the card grants it to |
| **medium** (`medium`) | Reversible change to shared development state | push a `glm/`/`codex/`/`claude/` branch, open a PR, dispatch the S2 workflow, a cloud dispatch (with task-routing's GO), governance drafting (coordinator only, routing test 1) | the highest class a card may grant an agent seat |
| **operator act** (`high`) | Irreversible, external, financial or ratifying | merge, ratify, spend, deploy the rail, arm the rail | the operator, through an act they already perform — never delegated by a card |
| **forbidden** (`forbidden:` map) | Un-grantable to every seat; no approval unlocks it for an agent | place a trade, auto-merge, a direct push to `main`, TV login automation, edit a locked parameter, edit the frozen protection constants, commit private data | nobody among the agents; the frozen protection constants keep their own governed route (pre-registration → re-MC → both-halves gate → admitting ADR, ratified by the operator) |

Rules:

1. **A card only narrows.** No card grants an operator act or a forbidden capability; a card's
   capabilities are within its seat's grant and its `max_risk`, and within its parent card's
   capabilities, risk and constraints. A child may add constraints; it never drops one silently —
   a needed relaxation is an escalation, not an edit.
2. **Approval is an act the operator already performs, bound to the exact object.** A merge
   approves one head SHA; an arming GO is for one armed session and its absolute `armed_until`;
   a ratification is the merge of the PR that carries the text. A change after the act is a new
   request. There is no second approval inbox, and agent text reporting that the operator
   approved something is not an approval. When a harness prompt stands in (the operator-act
   hook below), the operator answering that prompt is the act, and for a merge the prompt is
   only offered on a call pinned to the full head SHA it names — GitHub then refuses the merge
   if the head moved, so the answer covers exactly those bytes.
3. **`IN_DOUBT` side effects.** A side effect whose request left but whose outcome was not
   observed is recorded as in doubt, reconciled against the external system, and never retried
   automatically. A local idempotency key proves nothing about an external effect — `order_id`
   idempotency is disproven at the venue. This is the qualification service's START_INTENT /
   IN_DOUBT rule stated for every seat.
4. **Enforcement points, not a new service.** The runtime is the set of points below plus git
   as the event log (committed-handoff rule). An orchestrator service is built only if a
   recorded failure shows these points are insufficient.

| Act | Enforcement point | Status 2026-09-25 |
|---|---|---|
| card grants | `check_handoff_authority.py` (`handoff-authority` gate): a worker card must name its parent; parents must be inside the repository, are checked recursively, and a cycle is refused | enforced for cards with a block |
| merge | the operator merges on GitHub; [`scripts/guard_operator_acts.py`](../../scripts/guard_operator_acts.py) asks before a Claude Code session merges (MCP tool; `gh pr merge` or a `gh api` merge from the Bash or PowerShell tool) and only when the call pins the head SHA, naming every pinned SHA in the prompt; an unpinned merge, or a `gh api` body the hook cannot read, is refused; a deny anywhere in one command wins over an ask | Claude Code harness enforced; Codex / Z Code harnesses rely on the operator not giving them a merge-capable credential (operator-held) |
| auto-merge | the same hook denies; CI holds no write credential (2026-08-29 addendum #1 bar) | Claude Code harness enforced and CI credential-free; the repository's own "allow auto-merge" setting and the Codex / Z Code harnesses are operator-held |
| push to `main` | GitHub ruleset (PR + `skills (3.12)` required); the hook denies a `git push` whose destination is `main`, including a bulk (`--all` / `--branches` / `--mirror`), matching (`:`) or glob push that covers it | ruleset enforced for non-bypass credentials (bypass list not verified from an agent session); Claude Code harness enforced for named, bulk and glob destinations; a bare `git push` from a `main` checkout is the ruleset's alone |
| rail deploy | Fly credential on the operator's machine; the hook asks on `fly deploy` | operator-held + Claude Code harness |
| rail arm | `c1_rail_arm.py` interlock (`validate(require_resolved=True)`); the hook asks on `--arm` (never on `--disarm` / `--status`) | enforced |
| trade | CrossTrade / Tradovate credentials never present in an agent environment; no hook can see it | operator-held |
| spend | the operator's payment method; task-routing GO for a cloud dispatch | operator-held |
| statistical dispatch | qualification service admission and budget (Full E1 S2) | enforced |

<a id="operator-decision-packets"></a>
**Operator decision packets (2026-09-25).** Anything that needs the operator arrives as one
packet, on the PR or behind `STATE.md`'s operator queue in the order that file's own rule sets
(packets queue behind the numbered items and do not become items; the queue stays ≤5 live
items, and overflow is a prioritisation defect of the executive and coordinator seats, not the
operator's backlog). A packet carries:
the question; the options, each with its consequence; the recommendation; the evidence one link
away (diff, the `.cache/fp-verification` record, reviewer dissent); what is unresolved or
dissented; what was deliberately not done (M-36); and what happens without a decision. For a
reversible (medium) item the packet names the default the coordinator will take and when — silence
is consent only there. For an operator act there is no default: without the act nothing happens.
A green `DONE` return is not a packet; it goes to the coordinator and the executive, and reaches
the operator as a merge.

**Seat names across imported proposals (2026-09-25).** Organisation proposals written outside the
repo use other names; they are translated at the boundary and never adopted as a second chart.

| Imported name | Seat here |
|---|---|
| Executive / Principal (human) | **Operator** |
| Chief of Staff | **Executive** (Codex "Astra") — may author the mandate (goal, constraints, milestone, success criteria), never cards, so its PR review against its goal stays independent |
| COO | **Coordinator** (Opus); Fable stays the escalation lane and never takes this seat |
| Execution teams | **Workers** |
| Review / verification | reviewer ≠ planner signatures plus deterministic gates |

**Measure and falsifier for the three-seat model.** The existing §4 limbs stand (judgment-defect
worker PRs; overhead exceeding value). Added: the model is measured on **operator-minutes per
accepted change** and **defects found after merge**, never on cards closed. If, over a rolling
8-week window, the Fable lane fires on more than a third of cards, the cards are not being
frozen and the coordinator seat — not the lane — is the defect to fix; if it never fires while
post-merge defects recur, the two-failure rule is not being applied. Added 2026-09-25, logged by
the coordinator in the campaign record and read at the quarterly check: packets the operator
returns as *not mine* (over-escalation) and packets returned as *under-evidenced*. If either
exceeds a third of packets over a rolling 8 weeks, the escalation line or the packet format is
the defect to fix. Any operator act that happened without the operator's act — a merge, arm or
deploy by an agent without the operator — is a failed enforcement point: fix it at the cheapest
layer (test → hook → credential) before other work on that surface.

**Effective:** the 2026-07-14 decision on acceptance; the 2026-09-15 rescoping on the
operator's same-day in-session ratification; the 2026-09-20 and 2026-09-25 revisions each on
operator merge of the PR that carries it.
**Scope:** task routing between the coordinator and worker surfaces on this repo. Other external
surfaces (web advisors, claude.ai) keep their existing gates; this ADR does not re-govern them.

## Grounds

**For the original allocation (2026-07-14, unchanged in substance).** Since 2026-07-06 the repo
ran a two-surface workflow without a written rule, producing four clean lands in eight days and
zero locked-surface incidents. The counter-pattern is also documented: external instruction
packets confabulate repo state when not gated
(`feedback_web_advisor_handoff_confabulates_repo_state`, multi-fire through 2026-07-11), which is
why `handoff-verify` exists. Unwritten, the allocation would drift under speed pressure until a
judgment-heavy or locked-surface task crossed a line. Routing by "code vs docs" was rejected as
the wrong axis in both directions: a mechanical `SESSIONS.md` entry was successfully handed off,
while `dd_geometry.py` — code — was correctly kept in-session because it sits on a governed
surface. Spec-completeness and surface-proximity predict outcomes; artifact type does not. A
vendor-supplied CC-vs-Cursor performance comparison offered at the time was treated as
unverified marketing material and is explicitly non-load-bearing: the decision would stand
unchanged if every vendor claim were false.

**For the 2026-09-15 retirement.** The operator removed Cursor from recurring spend on
2026-09-10 ([`d16`](../pursuits/d16-cursor-subscription.md), `SUBTRACT`;
[subscription ledger](../pursuits/SUBSCRIPTION_LEDGER.md)), and on 2026-09-11 ruled for Track B
that "Cursor is not a lane… packets marked Cursor-eligible go to Codex local"
([D-B6](../briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md)). The
2026-09-15 instruction generalises that to the repo. A surface with no subscription cannot be
dispatched to, so leaving the lane documented as live would leave the routing test describing a
destination that does not exist — the drift this ADR was written to prevent, pointing the other
way.

**For the 2026-09-20 three-seat revision.** The operator's working arrangement (Codex executive,
Opus coordinator, GLM worker) had diverged from this record, which still described Codex as a
worker and named no GLM surface — so every agent reading the repo followed a chart the operator
no longer used. The specific gaps were named in-session on 2026-09-20 and ruled on: the record
mismatch (item 1); the committed-file boundary (item 2, "keeping this boundary is satisfactory");
cross-harness memory, discharged by migrating M-26 … M-48 into `methodology_lessons.md` (item 3);
quality before operator attention as the priority (item 4); acceptance tests named before the
worker starts (item 5); the committed-handoff rule and Fable triggers (item 6). The
self-grading risk — the coordinator writing the cards, reviewing against them and writing the
synthesis the executive steers by — is the documented fold-loop failure (M-37, M-38, M-40) seen
on PRs #360, #395 and #401; reviewer ≠ planner is its structural fix (M-46). Fable is placed as a
lane rather than a seat because its cost is per-instance and its edge is on long, messy,
high-reasoning work; vendor benchmark and pricing claims about it were treated as unverified
and are non-load-bearing, as the 2026-07-14 text did for the Cursor comparison. The fifteen untracked
handoff packets found in the main checkout's `docs/briefs/handoffs/` on 2026-09-20 (two GLM, one
Astra, twelve coordinator/operator packets; `git status --short -- docs/briefs/handoffs/`) are the
committed-handoff rule's first application: each is committed or tombstoned before the next
dispatch that would rely on it.

**Why this is a revision and not a new ADR.** The subject of this record *is* surface
allocation; retiring one of the two surfaces is a change of scope to this decision, not a
different decision. [ADR ceremony tiering](2026-08-08-adr-ceremony-tiering.md) (revised
2026-09-08) provides exactly this mechanism — "approved changes update effective decision text
with a dated revision and immutable prior version" — and explicitly retired the rule requiring
"new sibling ADRs for every amendment." A third file on this subject would have continued the
corpus growth that policy revision exists to stop, and would have created a second owner for
rules Rule 7 assigns to one.

**For the 2026-09-25 revision.** On 2026-09-25 the operator asked for a review of three external
drafts — an "Orchestrator Runtime Contract v1", a "Typed Delegation and Evidence Protocol" ADR and a
"Hierarchical Agent Organization" ADR (operator uploads to the session; not committed) — for how
they would change the time the operator spends managing agent teams, then directed the review's
recommended sequence "in full". The review kept the drafts' central boundary (models propose;
deterministic code authorises and records), their escalation format (options, consequences,
recommendation, evidence) and their ask that authority only narrow. It did not adopt: a second
seat chart whose "Executive" means the human (this ADR's executive is Astra); Fable as COO (Fable
is a lane); `trade.submit` as an approvable high-risk act (here no agent may place a trade); five
runtime schema levels (STATE, the umbrella, the plan and the card already carry them, and git
already records them); a new orchestrator service (the enforcement points above already exist);
and two new ADRs (they would be second owners of this record's seat table — Rule 7). Operator
attention is the binding resource (`STATE.md`), so approvals were designed as fewer, larger acts
bound to evidence rather than a per-action approval queue, which would turn the operator into a
rubber stamp.

## Current owner

- **This ADR** owns the seat table, the routing test, the handoff contract (including the
  acceptance-tests-in-the-card item), the committed-handoff rule, the escalation-lane triggers,
  the return contract and merge authority.
- [`methodology_lessons.md`](../methodology/lessons/methodology_lessons.md) M-26 … M-48 own the
  dated failure evidence the seat rules cite; this ADR states the rules, not the incidents.
- [`task-routing`](../../.claude/skills/task-routing/SKILL.md) owns the canonical local-only
  (test 0) checklist. One owner: this ADR states the test, that skill holds the list.
- [`cc_handoff.md`](../../.claude/skills/brief-authoring/references/cc_handoff.md) owns the
  producer-side brief template, including the §0.75 local-only dependency block and the
  recommended-defaults pattern for resolving ambiguity ahead of a frozen-spec dispatch.
- [`handoff-verify`](../../.claude/skills/handoff-verify/SKILL.md) owns the consumer-side
  Phase-0 gate.
- [`TOMBSTONES.md`](TOMBSTONES.md#2026-09-15-cursor-agent-retirement) owns retrieval of the
  artifacts removed by the retirement sweep.
- `docs/SESSIONS.md` and the programme audits own the dated failure evidence behind the
  orchestration rules; this ADR states the rules, not the incident log.
- [`scripts/seat_authority.yml`](../../scripts/seat_authority.yml) owns the capability registry
  (names, class, per-seat grants) that the action-class rules consume; this ADR owns the rules.
- [`scripts/check_handoff_authority.py`](../../scripts/check_handoff_authority.py) and
  [`scripts/guard_operator_acts.py`](../../scripts/guard_operator_acts.py) own the mechanical
  enforcement of item 7 and of the operator-act prompt for the Claude Code harness.

## §8 — Disposition of the prior decision's clauses and addenda

> **Two HTML anchors in this file are load-bearing and must not be removed:**
> `#2--decision` (the slug of the pre-revision `## §2 — Decision` heading) and
> `#addendum-2026-09-04-disable-notify-cursor`. The 2026-09-15 revision dropped both
> headings and broke two live incoming links — `docs/SESSIONS.md:424` and the Track B
> [campaign state](../briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md).
> The SESSIONS citation sits in a merged entry that `sessions-append-only` forbids
> editing, so the anchor is pinned here rather than the caller repointed.

Every clause of the 2026-07-14 body and its six addenda, dispositioned per
[ceremony tiering](2026-08-08-adr-ceremony-tiering.md) ("disposition each obligation as retained,
discharged, superseded or explicitly retired"). Full prior text at blob
`0bcd6699fd683a18b9493e25bb053797dcf4fafe`.

| Prior clause | Disposition |
|---|---|
| §2 routing test 0 (local-only dependency pre-check, 2026-07-16 addendum) | **Retained**, surface-agnostic. Binds Claude Code and Codex equally; checklist owner is `task-routing`. |
| §2 routing test 1 (locked/governed surface → coordinator) | **Retained** verbatim in substance. No surface exception, no size exception. |
| §2 routing test 2 (spec frozen; never resolve ambiguity unilaterally) | **Retained**, "Cursor" → "a worker". |
| §2 routing test 3 (handoff-overhead threshold) | **Retained**. Its 2026-08-29 reading as *proactive dispatch authority* (act, don't merely label) is also retained. |
| §2 handoff contract, items 1–3 and 5 (brief passing `check_brief`; §0 read-report + `NEEDS_CONTEXT`; §5 forbidden moves; vendor-bytes/secret declaration) | **Retained** unchanged. |
| §2 return contract, "no commit/merge without operator go" | **Retained, and restored to its unnarrowed form** — the 2026-08-14 narrowing retires with its mechanism. |
| §2 return contract, `cursor/*` branch | **Superseded** — worker branches are `codex/*` or `claude/*`. |
| Four-state return taxonomy (`DONE`/`DONE_WITH_CONCERNS`/`NEEDS_CONTEXT`/`BLOCKED`) | **Retained** and promoted into §Decision; it was previously stated only by the deleted `cursor-fleet` skill. |
| §4 falsifier limb 1 (≥2 judgment-defect PRs in 8 weeks) | **Retained**, re-scoped to worker PRs on any surviving surface. |
| §4 falsifier limb 2 (overhead exceeds value, ≥3 consecutive handoffs) | **Retained**, surface-agnostic. |
| §5 forbidden move — verbal-spec handoffs | **Retained**. The containment is the brief, whatever the worker. |
| §5 forbidden move — scope-creep via adjacency | **Retained**. |
| §5 forbidden move — merging on green tests without review | **Retained**, unnarrowed (see above). |
| §5 forbidden move — retro-fitting a brief after the build | **Retained**. |
| §5 forbidden move — quoting the vendor comparison's numbers in routing arguments | **Explicitly retired** — the comparison was Cursor-vs-CC and has no remaining referent. Its *principle* (don't ground routing doctrine in vendor marketing) is generic and survives under `verify-source`. |
| §6 downstream artifacts; §7 implementation plan (Phases 0–3) | **Discharged** 2026-07-14/16. Completed maintenance acts; no standing obligation. |
| §10 audit hooks (cursor-branch merge/locked-surface sweeps) | **Superseded** by §10 below — the old hooks scan a branch namespace that no longer exists. |
| Addendum 2026-07-16 (Step 0 + 5th contract item) | **Folded into §Decision above**; binding, not an appendix. |
| Addendum 2026-08-14 (auto-merge narrowing) | **Explicitly retired** with its parent mechanism. See the `2026-08-14` ADR's own retirement. |
| Addendum 2026-08-23 (automatic Claude judgment review) | **Already self-superseded 2026-08-29** — the mechanism never fired (`GITHUB_TOKEN`-authored comments do not trigger workflow runs) and its files were deleted then. No live obligation. |
| Addendum 2026-08-29 #1 (Codex native GitHub review) | **Retained and now load-bearing** — Codex's account-level review is a surviving surface's review path. Its standing bar — *this repo's CI grants Codex no write/push credential without a superseding ADR* — **survives the Cursor retirement unchanged**; nothing here relaxes it. |
| Addendum 2026-08-29 #1 — **its revert trigger**: a rolling 8-week window in which Codex's native review is demonstrably lower-signal than Claude's on the same class of PR, or the operator disables the `chatgpt.com/codex/settings/code-review` toggle for this repo (operator-judged, logged in `docs/SESSIONS.md`) | **Retained.** Revert action unchanged and still correct: none in this tree — the mechanism is account-level, so reverting is toggling that setting off, not editing this repo. |
| Addendum 2026-08-29 #2 — **its revert trigger**: two proactively-dispatched tasks in a rolling 8-week window turn out to have needed operator judgment the coordinator lacked (wrong root cause, misjudged scope, a spec that was not actually frozen) | **Retained**, re-scoped to the surviving worker surfaces. Revert action: back to per-task "dispatch this" confirmation before any worker dispatch. |
| Addendum 2026-08-29 #1, "relay findings to Cursor's Cloud Agent" | **Explicitly retired** — the relay target is gone. Findings are addressed by the coordinator or a Codex/Claude Code worker. |
| Addendum 2026-08-29 #2 (proactive dispatch; lightweight GitHub-issue + `@cursor` format) | **Split.** Proactive-dispatch authority is **retained** (above). The lightweight issue format is **retained in shape** — a complete issue body in place of a full brief for small precedented fixes — but its `@cursor` dispatch step is **explicitly retired**; dispatch is to a Codex or Claude Code worker. |
| <a id="addendum-2026-09-04-disable-notify-cursor"></a>Addendum 2026-09-04 (`notify-cursor.yml` auto-ping disabled) and its revert trigger ("operator asks to turn the ping back on"; restore `on:` events from `4f3ddc6`) | **Explicitly retired, not left standing.** The workflow is deleted by this revision's sweep; the revert trigger is unreachable and is discharged rather than carried as a dead obligation. Retrieval via [`TOMBSTONES.md`](TOMBSTONES.md#2026-09-15-cursor-agent-retirement). |

### 2026-09-20 revision — disposition of the 2026-09-15 clauses it touches

| 2026-09-15 clause | Disposition |
|---|---|
| "Surfaces" paragraph (coordinator = Claude Code; workers = Claude Code and Codex; Cursor retired) | **Superseded** by the seat table. Cursor's retirement and its no-falsifier election are **retained** verbatim in substance. |
| Routing tests 0–3 | **Retained** unchanged; test 1's `CLAUDE.md` reference updated to `AGENTS.md` (the file was retired the same day). |
| Handoff contract, five items | **Retained**; a sixth item (acceptance tests named in the card) **added**. |
| Lightweight dispatch issue (items 2–5 in place of a brief) | **Retained in shape, re-scoped**: must carry items 2–6 including the predeclared acceptance tests; its freeze is the body hash in the coordinator's read comment, the one permitted non-file card under the committed-handoff rule. |
| Routing test 1 "→ coordinator, full stop"; return contract "two bounces fall back to the coordinator" | **Retained**; *Ownership and precedence* under the escalation lane governs the overlap — the coordinator keeps ownership and performs the named authoring/rebuild on Fable. |
| Return contract branches `codex/*` / `claude/*` | **Retained**, `glm/*` **added**. |
| Merge authority is the operator's | **Retained** verbatim. |
| Orchestration rules (disjoint footprints, dispatch-moment Phase-0, review round part of the freeze, pointer SHA) | **Retained** verbatim; the committed-handoff rule generalises the single-writer rule to every seat boundary. |
| Addendum 2026-08-29 #1 (Codex native review, retained) | **Retained and re-seated** — it is now the executive's independent signature under reviewer ≠ planner. |
| `AGENTS.md` §Continuous improvement, "after two failed corrections… restart with a cleaner prompt" (external rule, not this ADR's) | **Bound, not changed** — the restart is where the Fable lane's trigger 1 fires. |

### 2026-09-25 revision — disposition of the 2026-09-20 clauses it touches

| 2026-09-20 clause | Disposition |
|---|---|
| Seat table | **Retained** unchanged; imported names map onto it (seat-name table). |
| Handoff contract, six items | **Retained**; a seventh item (authority block) **added**. |
| Lightweight dispatch issue | **Retained**; it carries item 7 too, checked by hand in the read comment. |
| Merge authority is the operator's, no automated exception | **Retained** verbatim; now prompted for Claude Code sessions and auto-merge refused by `guard_operator_acts.py`. |
| Measure and falsifier | **Retained**; packet-return measures and the failed-enforcement-point rule **added**. |
| Committed-handoff rule | **Retained**; named as the event log under *Enforcement points*. |

### Deliberately retained (not over-swept)

Three Cursor-named things survive on purpose; a future reader should not treat them as a
missed sweep:

- **`scripts/check_pine_manifest.py`'s `cursoragent@cursor.com` author denylist.** Dormant —
  that identity can no longer appear — but retained as cheap anti-re-entry armor for the
  incident it encodes (commit `66c2a14`/PR #574: a Pine manifest pin authored from a
  disposable Cursor cloud checkout, bytes lost). The guard costs nothing and still fires if
  the lane is ever restored. `.github/workflows/manifest-check.yml`'s matching comment is
  that incident's record.
- **The `cursor` alternation in both copies of `check_brief.py`'s type-inference regex.**
  Retained as inert tolerance for two frozen historical briefs that self-declare
  `**Brief type:** Cursor handoff`. **Correction (2026-09-15, adversarial review):** an earlier
  draft of this section claimed removing the alternation "would silently reclassify those
  records." That was **false** and is corrected here rather than quietly dropped — `infer_type`
  also matches on filename, and both briefs carry `cursor-handoff` in their names, so removal was
  measured to change zero classifications across all 858 markdown files. The alternation stays
  because it is harmless and costs nothing, not because anything depends on it. The regex reads
  history; it authorizes nothing.
- **`lab/research_utils/msl_preflight.py`'s ripgrep fallback** to a Cursor *editor* install
  path. It is a guarded filesystem probe reached only when `rg` is absent from `PATH`, with no
  agent semantics; removing it could only reduce robustness on a host that still has the editor.

Dated Cursor attributions in instrument ledgers, `lab/CATALOG.md`, `PORT_MANIFEST.sha256`,
`docs/SESSIONS.md`, closures and superseded specs are historical record and are **not** swept —
history stays, per the reader-intercept principle this revision relies on.

## §4 — Falsifier (revert trigger), restated surface-agnostically

Both limbs survive the retirement; only "Cursor" becomes "a worker". Restored here
because the 2026-09-15 consolidation carried their *thresholds* into the §8 table but
dropped their revert **actions** and their check schedule — a falsifier without a
stated consequence is the failure mode this repo has a lesson for.

**Revert trigger (either limb):**

1. **Allocation-caused defects** — over any rolling 8-week window, ≥2 merged
   worker-built PRs carry defects traceable to *spec-interpretation judgment* (the
   worker resolved an ambiguity instead of bouncing `NEEDS_CONTEXT`) rather than to
   spec error.
2. **Overhead exceeds value** — ≥3 consecutive handoffs where authoring and verifying
   the brief demonstrably cost more session time than the gated build
   (operator-judged, logged in `docs/SESSIONS.md`).

**Revert action:** limb 1 → supersede with a tightened rule (narrower worker scope, or
mandatory coordinator re-verification of every worker diff hunk); limb 2 → carve the
affected task class back to the coordinator by superseding ADR — **do not silently stop
writing briefs.**

**Trigger check schedule:** rides the standing quarterly programme review.

## §9 — Operator actions this repo cannot perform

Three Cursor residues sit outside what a file edit can reach, so merging the sweep could not touch
them. Recorded here, in the hot record, so the retirement is not mistaken for complete at the
account level. **Items 1 and 2 verified already gone on 2026-09-15** (same-day follow-up session,
run on the operator's machine and account):

1. **The GitHub webhook trigger** created under the now-superseded autonomous-loop ADR (routine
   `trig_012nvuH7jqmjFUFgoFVpZ6RP`, firing unfiltered on `pull_request: opened`) — an
   account-level routine, not a repo file. **Deleted.** `RemoteTrigger get` on the id returns
   HTTP 404 `Trigger not found` from the same account whose 2026-08-15 session transcript holds
   the routine's API record; `list_runs` shows zero sessions against a `52 */6 * * *` cron that
   would have produced ~4/day; and all 30 `cursor/*` PRs opened after 2026-08-14 were merged by
   the operator or `app/cursor`, never by the routine. The API's `list` returns only the 20
   newest routines and does not page, so the earlier "not in the listing" was uninformative
   either way — the resource-level 404 is the evidence. Nothing to disable. One residual check
   only the operator can make: the routines page at `claude.ai/code/routines`, confirming no
   *other* routine carries a GitHub event source on `first-passage` (a routine object exposes no
   event-source field, so the API cannot answer this).
2. **`daily-repo-truth-sync`**, the operator-machine scheduled task whose step 2 classified
   `cursor/*` branches SPENT / CARRIES-WORK / UNKNOWN. **Deleted.** The desktop scheduler
   reports `taskDeleted: true` (42 runs; last 2026-09-14 00:59Z). Its `SKILL.md` remains under
   `~/.claude/scheduled-tasks/` as the scheduler's documented post-delete residue, not a live
   task. Nothing to prune.
3. **Four spent `cursor/*` refs still on `origin`** — a remote deletion, not a file edit, so the
   sweep could not perform it (and §10 hook 3 read "empty" from an unfetched checkout):
   `cursor/research-asset-registry-0ba4` (#315 merged), `cursor/scripts-side-2026-09-04-p3`
   (#303 merged), `cursor/windows-handoff-job-accounting-7785` (#326 merged) — each an ancestor
   of `main` — and `cursor/scripts-side-2026-09-04-p2` (#304 closed unmerged, "Packet B was
   withdrawn before dispatch"), one commit ahead holding the withdrawn diff, which stays
   reachable from the PR after deletion. Operator: `git push origin --delete <ref>` ×4.

None of this blocks ratification. A fourth item is the operator's alone: the **Cursor row in the
[subscription ledger](../pursuits/SUBSCRIPTION_LEDGER.md)** still records a cancellation date and
final charges as not supplied. That is an operator reconfirmation, not an agent edit.

### In-flight work this revision interacts with (2026-09-15)

Two PRs were open against `main` when this revision landed. Neither is editable from this
branch; both need a pass at merge time:

- **[#402](https://github.com/Joshua-Asante/first-passage/pull/402)** amends
  `.claude/skills/cursor-fleet/SKILL.md`, which this revision **deletes** at operator
  instruction. Whichever lands second conflicts. The deletion is the operator's ruling and
  should win; #402's substance (a brief's review round is part of the freeze, and the dispatch
  pointer carries the frozen SHA) is **already carried** in §Decision's orchestration rules, so
  nothing of it is lost by closing it against the deletion. **Resolved 2026-09-16:** #402 had
  merged first (`c86a0a0`, 2026-09-15); the conflict was settled at this revision's merge by
  carrying its two rules here and deleting the skill (`a9f3a9f`). TOMBSTONES now pins the final
  body `main` held (`c47af22…`, with #402's rules) — the `56f728a…` first pinned predated #402.
- **[#401](https://github.com/Joshua-Asante/first-passage/pull/401)** adds a
  `work-decomposition` skill whose line 19 reads "retired by operator instruction on 2026-09-15
  (**retirement record pending**)". **This revision is that record** — the pointer resolves here
  once both land. #401 also makes pointer edits to `cursor-fleet`, which will need re-homing to
  this ADR for the same reason. **Resolved 2026-09-16:** #401 was re-pointed to this clause and
  TOMBSTONES before merge (its `cursor-fleet` edits dropped in `430eefe`) and merged as
  `b8e4034`; the back-pointer in §Decision closes the loop.

## §10 — Audit hooks (runnable)

```bash
# 1. No Cursor harness, dispatch script or workflow survives in the tree.
git ls-files .cursor scripts/dispatch_cursor.ps1 scripts/test_dispatch_cursor.ps1 \
             .github/workflows/notify-cursor.yml .claude/skills/cursor-fleet
# Expected after ratification: empty.

# 2. No live agent-facing surface still names a Cursor lane, dispatch or branch namespace.
#    Three carriers are deliberately excluded and are the ONLY permitted hits:
#      - comment lines recording why the lane is gone;
#      - scripts/agent_handoff.md's retirement note in prose;
#      - scripts/check_pine_manifest.py's `cursoragent@cursor.com` author denylist, retained as
#        dormant anti-re-entry armor for the PR #574 incident (bytes lost to a Cursor cloud agent).
#    Any OTHER hit is a finding.
rg -n -i "@cursor|cursor/\*|dispatch_cursor|cursor\[bot\]|cursor-agent" .claude scripts .github \
  | grep -vE ':[0-9]+: *#' \
  | grep -v '^scripts/agent_handoff.md:' \
  | grep -v '^scripts/check_pine_manifest.py:'
# Verified empty at authoring (2026-09-15). The workflow half is additionally pinned
# mechanically by tests/test_claude_review_workflows.py::test_no_workflow_dispatches_cursor.
# Historical citations in docs/adr/, docs/SESSIONS.md, docs/notes/ and lab/ARCHIVED.json are
# deliberately out of scope — history is not swept.

# 2b. No LIVE handoff brief still offers the retired surface as a spawn target.
#     Scope widened 2026-09-15 after a Codex review found
#     docs/briefs/handoffs/2026-09-11-track-a-a1b-... at "Status: dispatch now" still reading
#     "Spawn target: Codex (or Cursor)" while hooks 1-2 reported clean: they scan only
#     .claude/ scripts/ .github/, so a dispatchable brief was outside them.
rg -n -i '^\*\*spawn target:\*\*.*cursor' docs/briefs docs/superpowers \
  | grep -viE 'not cursor|not a lane|retire|re-?target'
# The FIELD VALUE is what is audited. The bare pattern matched six lines on 2026-09-16 — the two
# historical targets below plus four explanatory carriers (briefs re-targeted away from Cursor
# that say so, and one that says "NOT Cursor-eligible"); the filter drops the carriers. A brief
# that still OFFERS Cursor — "Codex (or Cursor)" — carries none of those words and stays a hit.
# Expected, as of 2026-09-16, exactly two hits, both spent and both verified as such:
#   docs/briefs/handoffs/2026-07-24-cursor-handoff-agent-surface-posture-sync.md
#     -- its own banner reads "STATUS 2026-07-24: DISCHARGED - DO NOT DISPATCH";
#   docs/briefs/rnd-pipeline/2026-07-14-cursor-handoff-lifecycle-call1-sigma-harness.md
#     -- no DISCHARGED line, but discharged BY DELIVERY: its deliverable exists at
#     lab/discovery/lifecycle_call1/, whose __init__.py:12 cites this brief as its handoff.
# Any hit on a brief that is still dispatchable is a finding.

# 3. Worker branches use a surviving namespace. Ask the remote: `git branch -a` sees only refs
#    this checkout has fetched, which is how the authoring pass read "empty" while origin held
#    four (the same unfetched-branch trap the #401 search fell into — SESSIONS 2026-09-15a).
git ls-remote --heads origin 'cursor/*'
# Expected: empty once the §9 item-3 refs are deleted. Verified 2026-09-15: exactly the four
# spent refs named in §9 item 3. Any ref not in that list is a finding.

# 4. The retirement did not silently drop the surviving clauses' owners.
test -f .claude/skills/task-routing/SKILL.md \
  && test -f .claude/skills/brief-authoring/references/cc_handoff.md \
  && test -f .claude/skills/handoff-verify/SKILL.md && echo "owners present"
python scripts/check_skill_refs.py --all
# Expected: "owners present" and a clean skill-refs pass.

# 5. Falsifier limb-1 evidence sweep (at each quarterly check).
grep -in "worker\|packet" docs/SESSIONS.md | grep -in "defect\|redesign\|NEEDS_CONTEXT"
# Adjudicate hits against the two §4 limbs; log the verdict in the review entry.

# 6. (2026-09-25) Card grants only narrow; operator acts prompt; auto-merge is refused.
python scripts/check_handoff_authority.py --all
python -m pytest -q tests/scripts/test_check_handoff_authority.py tests/scripts/test_guard_operator_acts.py
# Expected: 0 violation(s); all tests pass.
```

## Verification

```bash
python .claude/skills/brief-authoring/scripts/check_brief.py docs/adr/2026-07-14-cc-cursor-surface-allocation.md --type adr
python scripts/check_adr_graph.py
python scripts/check_skill_refs.py --all
git show 0bcd6699fd683a18b9493e25bb053797dcf4fafe   # prior decision text, unedited
```

Mechanical form checks do not establish semantic equivalence or ratification.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-14 | Initial authoring | Joshua + Claude Code |
| 2026-07-14 | Ratified — status `Proposed` → `Accepted`; §6 downstream sweep executed | Joshua |
| 2026-07-16 | Addendum RATIFIED — routing-test Step 0 + handoff-contract 5th item | Joshua |
| 2026-08-14 | Addendum RATIFIED — auto-merge narrowing (sibling ADR) | Joshua |
| 2026-08-23 | Addendum RATIFIED — automatic Claude judgment review (review-only) | Joshua |
| 2026-08-29 | Addendum RATIFIED — Codex second look via its native GitHub integration | Joshua |
| 2026-08-29 | Second addendum RATIFIED — proactive dispatch; lightweight issue format | Joshua |
| 2026-09-04 | Addendum RATIFIED — `notify-cursor.yml` auto-ping disabled | Joshua |
| 2026-09-15 | **Revision RATIFIED** — Cursor retired as a worker surface; decision rescoped to Claude Code + Codex; six addenda consolidated into the §8 disposition table; `2026-08-14-cc-cursor-autonomous-loop.md` superseded in full. Prior text at blob `0bcd6699fd683a18b9493e25bb053797dcf4fafe`. §4 falsifier restated; two 2026-08-29 revert triggers restored and one false retention claim corrected after adversarial review. | Joshua (in-session ratification) + Claude Code |
| 2026-09-25 | Revision proposed — action classes, authority block (item 7), approval bound to its object, `IN_DOUBT`, decision packets, enforcement-point table, seat-name mapping. Prior text at blob `cbe2a5886e3b6588b68294ac801f88acde3637b5`. Ratifies on operator merge. | Joshua (direction) + Claude Code |
