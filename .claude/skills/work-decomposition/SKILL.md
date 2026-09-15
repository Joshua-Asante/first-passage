---
name: work-decomposition
description: Use when a unit of work — a handoff brief, a lightweight dispatch issue, a campaign-plan step, a PR, or this session's own task — is too big for one focused session or one packet, or when the input to be read is too big for one context (10+ files, 50k+ tokens, or pairwise/multi-hop reasoning across scattered sources). Triggers on "break this down", "split this", "too big for one session", "decompose the work", "chunk this", a brief with more than 5 gate conditions or more than 3 unrelated code areas, a `BLOCKED — scope-problem` return, a second `NEEDS_CONTEXT` bounce on the same packet, or a task whose worst-case iteration count exceeds its Rule 2 budget. Produces sized child units each with its own gate plus a parent manifest (work-shaped), or a sized batch plan with depth-1 sub-agents and a source spot-check (input-shaped). Sibling of question-decomposition (a question with too many axes, not work with too many parts). Does not dispatch implementation workers (the coordinator does, under the surface-allocation ADR's orchestration rules), pick environments (task-routing), author the packets (brief-authoring), or verify returns (fable-judge); its input-shaped protocol does run read-only sub-agent waves in-session, which is evidence gathering, not work dispatch; changes no strategy parameters, allocations, dd_protection constants, or MC calibration.
---

# work-decomposition — size it before you start it

## Overview

Large units of work fail in large ways: the session compacts and the detail the gate needs is
gone, one packet bounces `NEEDS_CONTEXT` twice, a nine-item task quietly ships seven. Decomposed
units fail in small, fixable ways — one child returns `BLOCKED`, the other four merge. This skill
owns two protocols the repo otherwise gestures at without criteria: **work-shaped** (cut the work
into children that each fit one session or one packet) and **input-shaped** (cut the reading when
the input does not fit one context). It produces sized units and a manifest; it does not build,
dispatch implementation workers, or adjudicate; the input-shaped protocol below does run read-only
sub-agent waves inside the session, which is evidence gathering, not work dispatch. Worker surfaces
are Claude Code sessions and Codex tasks; Cursor was retired as a worker surface by operator
instruction on 2026-09-15. The record is the
[surface-allocation ADR](../../../docs/adr/2026-07-14-cc-cursor-surface-allocation.md)'s
2026-09-15 revision, whose §Decision clause "Orchestrating more than one worker at a time" now
owns the surviving fleet-orchestration rules — claim manifest, disjoint footprints (single-writer
rule), dispatch-time Phase-0 re-check, review-round-as-freeze, frozen-SHA dispatch pointer —
surface-agnostically. The `cursor-fleet` skill that stated them is deleted by that revision;
[TOMBSTONES](../../../docs/adr/TOMBSTONES.md) pins its body and names where each surviving
clause now lives.

Provenance: adapted 2026-09-15 from three external drafts — `troykelly/claude-skills`
issue-decomposition (oversize thresholds, child-quality checklist, dependency status),
`DevelopersGlobal/ai-agent-skills` task-decomposition (atomic-task test, verb-object-outcome
naming, ordering for incremental integration) and `massimodeluisa/recursive-decomposition-skill`
(size → filter → chunk → recurse → verify → synthesise, after Zhang, Kraska & Khattab, *Recursive
Language Models*, arXiv:2512.24601). Every imported rule has to justify itself here on repo
grounds; §Provenance lists what was dropped and why.

## Which kind of too big

| Shape | Tell | Owner |
|---|---|---|
| **Question-shaped** | One yes/no that two people with the same facts answer differently; a verdict that would drive reporting, escalation and precedent at once | `question-decomposition` |
| **Work-shaped** | One brief / issue / plan step / PR whose deliverables, gates or footprint exceed what one session or one packet can carry to a verified return | §Work-shaped, below |
| **Input-shaped** | The evidence to read exceeds one context, or the answer needs pairwise / multi-hop reasoning across scattered files | §Input-shaped, below |

Both work- and input-shaped at once → size the input first; the work cannot be sized until the
reading it takes is known.

## Work-shaped — cut the work

### Oversize tells

Any one of these means the unit is presumptively too big. The first five rows are imported
defaults (issue-decomposition) mapped to repo units; the last two are repo-native. Treat the
imported numbers as calibration candidates — record the firing when one bites, per CLAUDE.md
§Continuous improvement — not as ratified constants.

| Tell | Repo unit | Cut line it usually reveals |
|---|---|---|
| More than **5 gate conditions** in the return contract | §6 gate rows, `PASS <id>` check ids, acceptance bullets | One child per gate cluster that can be verified alone |
| More than **3 unrelated code areas** | `REPO_MAP.md` owner rows; the `core` / `lab` / `ops` layers — `lab↔ops` imports are forbidden, so a unit touching both is already two units | One child per layer or owner |
| More than **one context window** of work | One CC session; after compaction the summary keeps the plan and loses the detail the gate needs | One child per session-sized deliverable, each with its own resume handoff |
| **Multiple independent deliverables** | §1 "What CC is being asked to produce" bullets that do not consume each other's outputs | One child per deliverable |
| **Internal sequencing** — step N's input is step N−1's output, which does not exist yet | §2 Step 2.x chains whose later specs cannot be frozen until earlier steps return | Cut at the first output that must exist before the next spec can be frozen |
| **Worst-case iterations exceed the Rule 2 budget** — *INQHIORI-loop work only*, i.e. a unit with a declared Loop-of-Record (INNER 3 / OUTER 8 / STRATEGIC 3 constituent OUTER investigations — [canon §15](../../../docs/methodology/inqhiori-canon.md)); the [Rule 2 ADR](../../../docs/adr/2026-06-16-rule-2-budget-before-acting.md)'s 2026-08-15 addendum instructs budget declaration from INQHIORI entry only, so this row never turns a non-loop task into a budgeted one | Attempt-and-check cycles (INNER / OUTER); constituent OUTER investigations (STRATEGIC) | The tripwire would fire mid-unit. Cutting does not mint budget: an INNER or OUTER parent's iterations are allocated across its children and their worst cases must sum inside it; a STRATEGIC parent's budget is a *count* of OUTER children (at most three), each carrying its own full OUTER budget. A sum or count that exceeds the parent's is the parent's tripwire firing at cut time — a structured stop and, for OUTER / STRATEGIC, the owner's extension authority before anything is dispatched |
| A `BLOCKED — scope-problem` return, or a **second** `NEEDS_CONTEXT` bounce on the same packet | brief-authoring check 8; the surface-allocation ADR's return contract ("two bounces means the spec was not freezable and the packet was mis-routed") | The packet was mis-sized or mis-routed; re-cut before any re-dispatch |

Dated repo instances of the output this skill prescribes: the 2026-08-25 first-look residuals
were cut into five plans P6–P10 and, on operator follow-up, re-landed one commit per packet
([Q3 archive](../../../docs/ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) `2026-08-25b` /
`2026-08-25f`; charter
[`2026-08-23-repo-pain-point-packets.md`](../../../docs/superpowers/plans/2026-08-23-repo-pain-point-packets.md));
Track A was cut into per-packet briefs A1–A8 under one plan, A2 as a lightweight dispatch issue
([`2026-09-10-track-a-m1-stage1-completion.md`](../../../docs/superpowers/plans/2026-09-10-track-a-m1-stage1-completion.md));
Track B carries an umbrella with a dependency graph, a sub-track → packet map, wave gates and a
claim manifest
([umbrella §2](../../../docs/briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md)).
That umbrella is the reference shape for this skill's work-shaped output.

### The atomic-unit test (every child must pass all six)

1. **One named output** — a file, a PR, a RESULTS artifact, a decision record. Never "progress on".
2. **One named verification** the child's own return can run — a gate id, a pytest node,
   `check_brief` on a path, a `--check` mode (fable-method Step 1: name the actual gate). A child
   that cannot name its gate is not a unit yet.
3. **Independently revertible** — one PR, one revert, and every *parallel* sibling still passes
   its own gate. A child on an explicit *depends-on* edge reverts leaf-first: reverting an upstream
   child means reverting its dependents first, in reverse dependency order, which the manifest's
   edges make explicit. A revert that would silently break a sibling with no edge to it means the
   footprint or the edge is wrong.
4. **Fits one session with margin** — no step whose detail must survive a compaction. For
   INQHIORI-loop work only: an INNER or OUTER child's worst-case iterations fit the share
   allocated to it from the parent's Rule 2 budget, never a fresh budget of its own; a STRATEGIC
   parent's children are whole OUTER investigations, each with its own OUTER budget, and the
   parent's budget bounds how many of them there are.
5. **Disjoint file footprint** from every parallel sibling (the surface-allocation ADR's disjoint-footprints rule), or an
   explicit *depends-on* edge that makes it sequential. `docs/SESSIONS.md`, `STATE.md`, boards and
   index files are reserved to the parent's integration commit.
6. **Frozen, or explicitly judgment-owned** — a child that needs a judgment call mid-build stays
   with the orchestrating Claude session; a child on a locked surface (core anchor code, Pine,
   ADRs / pre-registrations / `CLAUDE.md` / `STATE.md`) stays there regardless of size. The
   [surface-allocation ADR](../../../docs/adr/2026-07-14-cc-cursor-surface-allocation.md) tests 1–2
   record the rule; its Cursor lane is retired (2026-09-15 revision), the rule is not. Never launder a judgment task into
   a "small packet".

Name each child `<verb> <object> so that <observable outcome>` — "Add the closure-overlay test so
that an overlay row cannot silently override a frozen D19 row", not "work on the calendar
stuff". If the outcome clause cannot be written, the child has no gate (point 2) and is not cut
yet.

Lower bound: do not cut below the handoff-overhead threshold (the surface-allocation ADR's test 3)
— a build smaller than its brief stays in the session that is already open. A child too small to amortise a handoff is folded into a sibling or run
inline under the session's own checklist (fable-method Step 4.4).

### Procedure

1. **State the parent's done** in two sentences plus its gate. Cannot → `refine-question` first;
   the parent is not yet a unit of work either.
2. **List candidate children** along natural boundaries: deliverable, layer/owner, file
   footprint, gate cluster. Run the six-point test on each; cut further or merge back until every
   child passes. A child inherits nothing wholesale — its gate is its own, specialised from the
   parent's, never the parent's list pasted in.
3. **Map dependencies.** For each child: `READY` (no open dependency; dispatch now),
   `BLOCKED-BY <child>` (queued until that return merges), `BLOCKS <child>` (dispatch first). No
   cycles — a cycle means one boundary is wrong. Sequence for **incremental integration**: merge in
   dependency order with the fast gates between merges, never one end-of-track consolidation.
4. **Write the parent manifest** before anything is dispatched — one row per child:
   `child · owner/lane · branch · footprint · depends-on · budget · status`. Lifecycle statuses
   `STUB / QUEUED / DISPATCHED / RETURNED / MERGED / OVERTAKEN / WITHDRAWN` (`STUB` = not yet
   freezable; nothing is dispatched from a stub). `RETURNED` always carries the four-state return
   and its disposition — `RETURNED (DONE)`, `RETURNED (DONE_WITH_CONCERNS — <concern>)`,
   `RETURNED (NEEDS_CONTEXT — re-anchor 1 of 1 | re-cut)`, `RETURNED (BLOCKED — <sub-case>)` — so
   the row says whether work is still owed; a child never stays `DISPATCHED` after its return, and
   a `NEEDS_CONTEXT` child goes back to `QUEUED` only once, then is re-cut. The `budget` column
   is filled only for INQHIORI-loop parents (a declared Loop-of-Record): each child's share of an
   INNER / OUTER parent's iterations, summing inside the parent's, or `OUTER (own 8)` under a
   STRATEGIC parent; for every other unit it reads `n/a — one session`, per the Rule 2 ADR's
   2026-08-15 propagation limit. The
   parent lists every child; a child absent from the manifest does not exist. This is the
   anti-duplication device: before any session opens work in the area, the manifest says who holds
   it.
5. **Route each child** to the lane its size and shape earn: 2+ frozen implementation packets →
   parallel worker sessions (Claude Code or Codex) under one umbrella brief and claim manifest,
   per the surface-allocation ADR's §Decision clause "Orchestrating more than one worker at a
   time"; one frozen build above the handoff-overhead
   threshold → a single `cc_handoff` brief for a Claude Code session, or a Codex task carrying the
   same §0 / §0.5 / §0.75 / §5 / §6 content; judgment or locked-surface work → the orchestrating Claude
   session; work that still fits one session but needs ordering → the session's own checklist.
   Environment per child → the local-only checklist in `task-routing`.
6. **Hand the children off.** Packet authoring is `brief-authoring` (cc_handoff template),
   pre-dispatch verification is `handoff-verify`, returns are adjudicated by `fable-judge`. This
   skill's deliverable ends at the manifest and the child specs.

### Child quality checklist

- [ ] Title names the parent and reads `<verb> <object> so that <outcome>`
- [ ] Own gate / verification steps, specialised — not the parent's criteria copied wholesale
- [ ] Own Phase-0 premises with an explicit no-op condition ("already on main → return `DONE`, cite the commit")
- [ ] Depends-on / blocks edges written down; status set from them
- [ ] Footprint listed and disjoint from parallel siblings; reserved files named as forbidden
- [ ] Return contract carries the four-state taxonomy (`DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED`)
- [ ] Row present in the parent manifest

## Input-shaped — cut the reading

Context rot is real here: a session that loads twenty files "to get context" reasons from a
blur of them. The protocol treats the input as an environment to query, not a document to load.

| Situation | Approach |
|---|---|
| One file, one function, one needle | Read directly |
| Localised answer, well under one context | Read directly, by line range |
| **10+ files or 50k+ tokens** | Decompose |
| **Pairwise, quadratic or multi-hop** reasoning across scattered sources — "which ADRs contradict each other", "every caller of X and what each passes" | Decompose **even if it would fit** — the case the RLM paper measures the largest gain on |
| A list-everything / aggregate task (every TODO, every kill-record citation, every pin) | Decompose |

### Protocol (six steps, in order)

1. **Size before reading.** Count files, lines and bytes of the candidate set before opening
   anything, with the candidates passed explicitly: `git ls-files <dir-or-glob> | wc -l` (files),
   `git ls-files -z <dir-or-glob> | xargs -0 wc -l` (lines, with a total), and
   `git ls-files -z <dir-or-glob> | xargs -0 wc -c` (bytes, with a total). A bare `wc` or `ls`
   measures stdin or the working directory, not the candidates. Cold stores are search-excluded —
   an empty `rg` is not "nothing there"; use `rg --no-ignore` or `git show` per fable-method
   Step 2.1.
2. **Filter.** Search before reading a directory; never list a tree recursively as a substitute
   for a query. Chain filters (path glob → content pattern → file type) until what remains is the
   candidate set.
3. **Chunk** the candidate set into natural units — a file, a module, a section, an ADR series,
   a date range, or a line range of one file — in **disjoint batches**. When the trigger is file
   count, batches of 5–10 files; when the trigger is one oversized file, batches are its sections
   or line ranges; when the trigger is a pairwise or multi-hop question over two to four sources,
   one batch per source is correct — the pairs are formed in the cross-batch join (step 6), never
   by a batch that re-reads a source another batch holds — and no batch is padded with unrelated
   files to reach a count. Write the batch count down before launching anything.
4. **Recurse at depth 1.** One sub-agent (`Agent` / `Explore`, or a `Workflow` script) per batch,
   each with a self-contained brief — the files, the question, the output schema. Launch **one
   parallel wave**, then merge. Sub-agents answer; they never spawn sub-agents, and no two
   sub-agents query the same content. For a **pairwise or multi-hop** question the batch brief
   asks for a *comparable claim inventory* under one schema (each ADR's rulings on the shared
   axis, each caller's argument values), never the final verdict — two conflicting sources in
   different batches would otherwise both return "no finding" and the contradiction would vanish
   in the merge.
5. **Verify** the merged answer on a smaller window: extract the minimal evidence behind each
   load-bearing line and re-open it. Settle a disagreement between batches with a targeted
   re-read of the disputed span — never by raising depth or re-running the wave.
6. **Synthesise** programmatically — aggregate the structured returns, deduplicate, categorise —
   then write the answer with `file:line` references. For pairwise or multi-hop questions the
   synthesis includes a **cross-batch join**: compare the inventories against each other (in the
   orchestrator's context, or by one further agent that reads only the inventories, never the
   sources — depth stays 1 relative to the sources) and adjudicate every pair the join flags with
   a targeted re-read of both endpoints.

Sub-agent brief, minimum viable:

```
Files: <the batch — exact paths, nothing else>
Question: <one question, the same wording for every batch>
Return: <schema — e.g. one row per finding: path, line, claim, verbatim quote>
Do not: open files outside the batch; spawn agents; summarise beyond the schema
```

### Hard rules

The partition rules (batches, one wave, no duplicate queries, the cross-batch join) govern
partition fan-outs; replication fan-outs are exempt from them as described below.

- MUST size before reading; MUST search before opening a directory.
- MUST read a file over ~2,000 lines or ~50 KB by line range, never whole.
- NEVER load more than ~5 files into the main context without a written batch plan.
- MUST keep depth at 1; MUST write the batch count before launch; one wave, then merge.
- MUST spot-check the synthesis against sources before answering.
- NEVER run the same query over the same content in two sub-agents; partition once.
- MUST, for a pairwise or multi-hop question, collect per-batch inventories and run the cross-batch
  join; disjoint batches alone cannot see a relationship whose endpoints sit in different batches.

Two fan-out shapes, one protocol each. **Partition fan-outs** join disjoint evidence: the batch
and inventory rules above apply in full — `adr-decay-audit`'s batch-scan-then-adversarial-verify
and the 14-agent Algorithm review of 2026-07-24 (recorded in the deleted `cursor-fleet` skill's
routing table — body pinned in [TOMBSTONES](../../../docs/adr/TOMBSTONES.md)) are instances.
**Replication fan-outs** deliberately have every agent read the *same* target through a different
lens, because independent duplicate review is the verification mechanism:
[`pre-ratification-adversarial-panel`](../../workflows/pre-ratification-adversarial-panel.js)
(six lenses, each told to read the entire target, then skeptics re-reading it),
[`handoff-verify-panel`](../../workflows/handoff-verify-panel.js) and
[`gate-reachability-audit`](../../workflows/gate-reachability-audit.js). They partition the
*question*, not the content; the disjoint-partition and one-wave rules do not apply to them, and
only the depth-1 and self-contained-brief rules carry over. Prefer the existing workflow when one
fits the question; author an ad-hoc wave only when none does.

## Rationalizations — STOP if you think one

| Rationalization | Reality |
|---|---|
| "I'll work out the cut as I go." | Sizing costs one pass; a mid-unit compaction or a second `NEEDS_CONTEXT` bounce costs the unit. |
| "It's too tangled to break down." | Everything cuts at its outputs. Start from the deliverable that must exist first; the rest sequence behind it. |
| "Too granular — that's five PRs for one feature." | Five children that each merge beat one that never returns; fold only the ones below the handoff-overhead threshold. |
| "The parent's acceptance list is good enough for the children." | Copied-wholesale criteria are the top anti-pattern: no child can pass or fail alone, so nothing is verifiable until everything is. |
| "Just read all the files first for context." | That is the input-shaped tell. Size, filter, batch. |
| "The merge looks thin — spawn another level." | Depth 2 is never the fix; re-read the disputed span. |
| "This packet is small, it can carry a judgment call." | Size does not move a judgment task off CC — surface-allocation test 2, no exception. |
| "I'll keep the manifest in my head." | The manifest is the anti-duplication device; unwritten means two sessions answer the same question (the Q-SFRISK-1 collision, recorded in the deleted `cursor-fleet` skill's friction ledger — body pinned in [TOMBSTONES](../../../docs/adr/TOMBSTONES.md)). |

## Red flags

- A brief whose §2 steps consume earlier steps' outputs, all dispatched at once.
- A return contract with more gate ids than one PR could plausibly leave green together.
- "Progress on X" as a deliverable; a child with no outcome clause.
- Children whose acceptance sections are byte-identical to the parent's.
- A child touching `docs/SESSIONS.md` or `STATE.md`, or two parallel children sharing a file.
- A session that has opened more than five files and has not written a batch plan.
- A sub-agent brief without a schema, or two sub-agents pointed at the same paths.
- Anyone proposing depth 2.

## Relationship to other skills

| Skill | Boundary with this one |
|---|---|
| `question-decomposition` | A question with too many axes → that skill; work with too many parts → this one. A bundled question inside an oversize brief goes there first — the cut lines often follow the axes. |
| `refine-question` | If the parent's done cannot be stated in two sentences, refine before decomposing. |
| [surface-allocation ADR](../../../docs/adr/2026-07-14-cc-cursor-surface-allocation.md) §Decision "Orchestrating more than one worker at a time" | Owns the orchestration rules that consume this skill's manifest and children when 2+ packets are frozen implementation — claim manifest, disjoint footprints (single-writer rule), dispatch-time Phase-0 re-check, review-round-as-freeze, frozen-SHA dispatch pointer. Its disjoint-footprints rule is the atomic test's point 5 applied at dispatch. Worker surfaces are Claude Code sessions and Codex tasks; the `cursor-fleet` skill that stated the loop is deleted by the ADR's 2026-09-15 revision (body pinned in [TOMBSTONES](../../../docs/adr/TOMBSTONES.md)). |
| `brief-authoring` | Authors each child as a `cc_handoff` brief; check 8's `BLOCKED — scope-problem` sub-case sends the packet back here for re-cutting. |
| `handoff-verify` / `handoff-verify-panel` | Pre-dispatch verification of a child; the panel is the input-shaped protocol applied to a many-claim packet. |
| `task-routing` | Picks local vs cloud per child after the cut. |
| `fable-method` | Step 2 owns evidence gathering and points here when the input is oversize; Step 4.4's checklist is the in-session lane for work that still fits one session. |
| `fable-judge` | Adjudicates each child's return; this skill renders no verdict on returned work. |
| Rule 2 ([ADR](../../../docs/adr/2026-06-16-rule-2-budget-before-acting.md)) | Sets the per-child iteration budget; this skill is how a unit is cut so the tripwire fires at a child boundary rather than mid-unit. |

## Provenance — what was imported, what was dropped

| Source rule | Disposition here |
|---|---|
| issue-decomposition thresholds (>5 criteria, >3 areas, >1 context window, multiple deliverables, complex sequencing) | Imported as presumptive tells with repo units; calibration pending firings |
| issue-decomposition sub-issue checklist, dependency status mapping, parent-lists-children | Imported as the child checklist, `READY / BLOCKED-BY / BLOCKS`, and the manifest rule |
| issue-decomposition GitHub sub-issue labels, Projects board, knowledge-graph step | **Dropped** — this repo's children are brief packets, dispatch issues and PRs under a manifest; it runs no Projects board or knowledge graph |
| task-decomposition "under 4 hours" per task | **Transformed** — Rule 2 forbids minute-denominated budgets; the unit here is iterations within the loop-class budget, and "one session" |
| task-decomposition atomic criteria, verb-object-outcome naming, dependency graph, incremental integration | Imported |
| recursive-decomposition six-step protocol, thresholds, depth-1 rule, hard rules, anti-patterns | Imported |
| recursive-decomposition PDF / Office conversion tooling (`anydoc`, `firecrawl`) | **Dropped** — no new dependency; convert with what the session already has, then apply the protocol to the text |
| External frontmatter (`model:`, `allowed-tools:`, `version:`) | **Dropped** — not this repo's skill contract |
