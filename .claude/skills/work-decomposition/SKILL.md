---
name: work-decomposition
description: Use when a unit of work — a handoff brief, a lightweight dispatch issue, a campaign-plan step, a PR, or this session's own task — is too big for one focused session or one packet, or when the input to be read is too big for one context (10+ files, 50k+ tokens, or pairwise/multi-hop reasoning across scattered sources). Triggers on "break this down", "split this", "too big for one session", "decompose the work", "chunk this", a brief with more than 5 gate conditions or more than 3 unrelated code areas, a `BLOCKED — scope-problem` return, a second `NEEDS_CONTEXT` bounce on the same packet, or a task whose worst-case iteration count exceeds its Rule 2 budget. Produces sized child units each with its own gate plus a parent manifest (work-shaped), or a sized batch plan with depth-1 sub-agents and a source spot-check (input-shaped). Sibling of inqhiori §14 (contested-question decomposition) (a question with too many axes, not work with too many parts). Does not dispatch implementation workers (the coordinator does, under the surface-allocation ADR's orchestration rules), pick environments (task-routing), author the packets (brief-authoring), or verify returns (handoff-verify post-execution judging); its input-shaped protocol does run read-only sub-agent waves in-session, which is evidence gathering, not work dispatch; changes no strategy parameters, allocations, dd_protection constants, or MC calibration.
---

# work-decomposition — size it before you start it

## Overview

Large units fail in large ways; decomposed units fail in small, fixable ones. This skill owns two protocols: **work-shaped** (cut the work into children that each fit one session or one packet) and **input-shaped** (cut the reading when the input does not fit one context). It produces sized units and a manifest; it does not build, dispatch implementation workers, or adjudicate. The input-shaped protocol does run read-only sub-agent waves in-session, which is evidence gathering, not work dispatch. Worker surfaces are Claude Code sessions and Codex tasks, dispatched by the coordinator (`coordinator` skill) under the [surface-allocation ADR](../../../docs/adr/2026-07-14-cc-cursor-surface-allocation.md)'s §Decision clause "Orchestrating more than one worker at a time".

## Which kind of too big

| Shape | Tell | Owner |
|---|---|---|
| **Question-shaped** | One yes/no that two people with the same facts answer differently; a verdict that would drive reporting, escalation and precedent at once | `inqhiori` §14 (contested-question decomposition) |
| **Work-shaped** | One brief / issue / plan step / PR whose deliverables, gates or footprint exceed what one session or one packet can carry to a verified return | §Work-shaped, below |
| **Input-shaped** | The evidence to read exceeds one context, or the answer needs pairwise / multi-hop reasoning across scattered files | §Input-shaped, below |

Both work- and input-shaped → size the input first; the work cannot be sized until the reading it takes is known.

## Work-shaped — cut the work

### Oversize tells

Any one means the unit is presumptively too big. The numeric thresholds are calibration candidates, not ratified constants: record the firing when one bites, per AGENTS.md §Continuous improvement.

| Tell | Repo unit | Cut line it usually reveals |
|---|---|---|
| More than **5 gate conditions** in the return contract | §6 gate rows, `PASS <id>` check ids, acceptance bullets | One child per gate cluster that can be verified alone |
| More than **3 unrelated code areas** | `REPO_MAP.md` owner rows; `core` / `lab` / `ops` layers — `lab↔ops` imports are forbidden, so a unit touching both is already two units | One child per layer or owner |
| More than **one context window** of work | One CC session; compaction keeps the plan and loses the detail the gate needs | One child per session-sized deliverable, each with its own resume handoff |
| **Multiple independent deliverables** | §1 "What CC is being asked to produce" bullets that do not consume each other's outputs | One child per deliverable |
| **Internal sequencing** — step N's input is step N−1's output, which does not exist yet | §2 Step 2.x chains whose later specs cannot be frozen until earlier steps return | Cut at the first output that must exist before the next spec can be frozen |
| **Worst-case iterations exceed the Rule 2 budget** — any unit carrying one (INNER 3 / OUTER 8 / STRATEGIC 3 constituent OUTER investigations — [canon §15](../../../docs/methodology/inqhiori-canon.md)); the [Rule 2 ADR](../../../docs/adr/2026-06-16-rule-2-budget-before-acting.md#addendum-2026-10-24--scope-widened-to-all-substantial-work) budgets all substantial work, routine fixes excluded | Attempt-and-check cycles (INNER / OUTER); constituent OUTER investigations (STRATEGIC) | The tripwire would fire mid-unit. Cutting does not mint budget: an INNER or OUTER parent's iterations are allocated across its children and their worst cases must sum inside it; a STRATEGIC parent's budget is a *count* of OUTER children (at most three), each with its own full OUTER budget. A sum or count over the parent's is the parent's tripwire firing at cut time: a structured stop and, for OUTER / STRATEGIC, the owner's extension authority before anything is dispatched |
| A `BLOCKED — scope-problem` return, or a **second** `NEEDS_CONTEXT` bounce on the same packet | brief-authoring check 8; the surface-allocation ADR's return contract | The packet was mis-sized or mis-routed; re-cut before any re-dispatch |

Reference shape for work-shaped output: Track B's umbrella, with a dependency graph, a sub-track → packet map, wave gates and a claim manifest ([umbrella §2](../../../docs/briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md)).

### The atomic-unit test (every child must pass all six)

1. **One named output** — a file, a PR, a RESULTS artifact, a decision record. Never "progress on".
2. **One named verification** the child's own return can run — a gate id, a pytest node, `check_brief` on a path, a `--check` mode (fable-method Step 1). A child that cannot name its gate is not a unit yet.
3. **Independently revertible** — one PR, one revert, and every *parallel* sibling still passes its own gate. A child on a *depends-on* edge reverts leaf-first: dependents first, in reverse dependency order. A revert that would silently break a sibling with no edge to it means the footprint or the edge is wrong.
4. **Fits one session with margin** — no step whose detail must survive a compaction. An INNER or OUTER child's worst-case iterations fit the share allocated from the parent's Rule 2 budget, never a fresh budget; a STRATEGIC parent's children are whole OUTER investigations with their own OUTER budgets, and its budget bounds how many there are.
5. **Disjoint file footprint** from every parallel sibling (the surface-allocation ADR's disjoint-footprints rule), or an explicit *depends-on* edge that makes it sequential. `docs/SESSIONS.md`, `STATE.md`, boards and index files are reserved to the parent's integration commit.
6. **Frozen, or explicitly judgment-owned** — a child that needs a judgment call mid-build stays with the coordinator; a child on a locked surface (core anchor code, Pine, ADRs / pre-registrations / `AGENTS.md` / `STATE.md`) stays there regardless of size ([surface-allocation ADR](../../../docs/adr/2026-07-14-cc-cursor-surface-allocation.md) tests 1–2; its Cursor lane is retired, the rule is not). Never launder a judgment task into a "small packet".

Name each child `<verb> <object> so that <observable outcome>` — "Add the closure-overlay test so that an overlay row cannot silently override a frozen D19 row", not "work on the calendar stuff". If the outcome clause cannot be written, the child has no gate and is not cut yet.

Lower bound: do not cut below the handoff-overhead threshold (the surface-allocation ADR's test 3). A build smaller than its brief stays in the open session: fold it into a sibling or run it inline under the session's checklist (fable-method Step 4.4).

### Procedure

1. **State the parent's done** in two sentences plus its gate. Cannot → `inqhiori` §14 first; the parent is not yet a unit of work either.
2. **List candidate children** along natural boundaries: deliverable, layer/owner, file footprint, gate cluster. Run the six-point test on each; cut further or merge back until every child passes. A child's gate is its own, specialised from the parent's, never the parent's list pasted in.
3. **Map dependencies.** For each child: `READY` (no open dependency; dispatch now), `BLOCKED-BY <child>` (queued until that return merges), `BLOCKS <child>` (dispatch first). No cycles: a cycle means one boundary is wrong. Sequence for **incremental integration**: merge in dependency order with the fast gates between merges, never one end-of-track consolidation.
4. **Write the parent manifest** before anything is dispatched, one row per child: `child · owner/lane · branch · card @ frozen hash | head SHA · footprint · depends-on · budget · status`.
   - Statuses: `STUB / QUEUED / DISPATCHED / RETURNED / MERGED / OVERTAKEN / WITHDRAWN`. `STUB` = not yet freezable; nothing is dispatched from a stub.
   - `RETURNED` always carries the four-state return and its disposition, so the row says whether work is still owed: `RETURNED (DONE)`, `RETURNED (DONE_WITH_CONCERNS — <concern>)`, `RETURNED (NEEDS_CONTEXT — re-anchor 1 of 1 | re-cut)`, `RETURNED (BLOCKED — <sub-case>)`. A child never stays `DISPATCHED` after its return; a `NEEDS_CONTEXT` child goes back to `QUEUED` only once, then is re-cut.
   - `budget` is filled for every budgeted parent: each child's share of an INNER / OUTER parent's iterations, summing inside the parent's, or `OUTER (own 8)` under a STRATEGIC parent; a routine-fix child reads `n/a — routine`.
   - The parent lists every child; a child absent from the manifest does not exist. Before any session opens work in the area, the manifest says who holds it.
5. **Route each child** by size and shape: 2+ frozen implementation packets → parallel worker sessions (Claude Code or Codex) under one umbrella brief and claim manifest, per the ADR clause above; one frozen build above the handoff-overhead threshold → a single `cc_handoff` brief for a Claude Code session, or a Codex task carrying the same §0 / §0.5 / §0.75 / §5 / §6 content; judgment or locked-surface work → the coordinator; work that fits one session but needs ordering → the session's own checklist. Environment per child → the local-only checklist in `task-routing`.
6. **Hand the children off.** Packets: `brief-authoring` (cc_handoff template). Pre-dispatch verification and return adjudication: `handoff-verify`. This skill's deliverable ends at the manifest and the child specs.

### Child quality checklist

- [ ] Title names the parent and reads `<verb> <object> so that <outcome>`
- [ ] Own gate / verification steps, specialised
- [ ] Own Phase-0 premises with an explicit no-op condition ("already on main → return `DONE`, cite the commit")
- [ ] Depends-on / blocks edges written down; status set from them
- [ ] Footprint listed and disjoint from parallel siblings; reserved files named as forbidden
- [ ] Return contract carries the four-state taxonomy (`DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED`)
- [ ] Row present in the parent manifest

## Input-shaped — cut the reading

Treat the input as an environment to query, not a document to load: a session that loads twenty files "to get context" reasons from a blur.

| Situation | Approach |
|---|---|
| One file, one function, one needle | Read directly |
| Localised answer, well under one context | Read directly, by line range |
| **10+ files or 50k+ tokens** | Decompose |
| **Pairwise, quadratic or multi-hop** reasoning across scattered sources — "which ADRs contradict each other", "every caller of X and what each passes" | Decompose **even if it would fit** |
| A list-everything / aggregate task (every TODO, every kill-record citation, every pin) | Decompose |

### Protocol (six steps, in order)

1. **Size before reading.** Count files, lines and bytes of the candidate set before opening anything, candidates passed explicitly and enumerated from the working tree: `git ls-files -c -o -- <dir-or-glob> | wc -l` (files), `git ls-files -c -o -z -- <dir-or-glob> | xargs -0 wc -l` (lines), `git ls-files -c -o -z -- <dir-or-glob> | xargs -0 wc -c` (bytes). `-c -o` without `--exclude-standard` lists tracked, untracked *and* gitignored files. A plain `git ls-files` lists only the index, which omits the inputs this repo keeps local (`core/data/tv_exports/**`, `core/data/bar_data/`, `core/data/external/`, research `inputs/` under `lab/analysis/`), so it undercounts and skips decomposition. If the operand sweeps build debris (`__pycache__`, `.venv`), narrow the glob; never add `--exclude-standard`. A bare `wc` or `ls` measures stdin or the working directory, not the candidates. Cold stores are search-excluded: an empty `rg` is not "nothing there"; use `rg --no-ignore` or `git show` per fable-method Step 2.1.
2. **Filter.** Search before reading a directory; never list a tree recursively as a substitute for a query. Chain filters (path glob → content pattern → file type) until what remains is the candidate set.
3. **Chunk** into natural units (a file, module, section, ADR series, date range, line range) in **disjoint batches**. Trigger is file count: 5–10 files per batch. Trigger is one oversized file: its sections or line ranges. Trigger is a pairwise or multi-hop question over two to four sources: one batch per source, with pairs formed in the cross-batch join (step 6), never by a batch re-reading a source another holds. Never pad a batch with unrelated files to reach a count. Write the batch count down before launching.
4. **Recurse at depth 1.** One sub-agent (`Agent` / `Explore`, or a `Workflow` script) per batch, each with a self-contained brief. Launch **one parallel wave**, then merge. Sub-agents answer; they never spawn sub-agents, and no two query the same content. For a **pairwise or multi-hop** question the brief asks for a *comparable claim inventory* under one schema (each ADR's rulings on the shared axis, each caller's argument values), never the final verdict: two conflicting sources in different batches would both return "no finding".
5. **Verify** the merged answer on a smaller window: re-open the minimal evidence behind each load-bearing line. Settle a disagreement between batches with a targeted re-read of the disputed span, never by raising depth or re-running the wave.
6. **Synthesise** programmatically (aggregate, deduplicate, categorise), then write the answer with `file:line` references. For pairwise or multi-hop questions include a **cross-batch join**: compare the inventories (in the orchestrator's context, or by one further agent that reads only the inventories, never the sources, so depth stays 1) and adjudicate every flagged pair with a targeted re-read of both endpoints.

Sub-agent brief, minimum viable:

```
Files: <the batch — exact paths, nothing else>
Question: <one question, the same wording for every batch>
Return: <schema — e.g. one row per finding: path, line, claim, verbatim quote>
Do not: open files outside the batch; spawn agents; summarise beyond the schema
```

### Hard rules

Beyond the protocol, which is mandatory for partition fan-outs:

- MUST read a file over ~2,000 lines or ~50 KB by line range, never whole.
- NEVER load more than ~5 files into the main context without a written batch plan.
- MUST spot-check the synthesis against sources before answering.

Two fan-out shapes. **Partition fan-outs** join disjoint evidence: batch and inventory rules apply in full (e.g. the `programme-audit` ADR decay sweep). **Replication fan-outs** deliberately have every agent read the *same* target through a different lens, because independent duplicate review is the verification mechanism: [`pre-ratification-adversarial-panel`](../../workflows/pre-ratification-adversarial-panel.js), [`handoff-verify-panel`](../../workflows/handoff-verify-panel.js), [`gate-reachability-audit`](../../workflows/gate-reachability-audit.js). They partition the *question*, not the content: the disjoint-partition, one-wave, no-duplicate-query and join rules do not apply; only depth-1 and the self-contained brief carry over. Prefer the existing workflow when one fits; author an ad-hoc wave only when none does.

## Rationalizations — STOP if you think one

| Rationalization | Reality |
|---|---|
| "I'll work out the cut as I go." | Sizing costs one pass; a mid-unit compaction or a second `NEEDS_CONTEXT` bounce costs the unit. |
| "It's too tangled to break down." | Everything cuts at its outputs. Start from the deliverable that must exist first. |
| "Too granular — that's five PRs for one feature." | Five children that each merge beat one that never returns; fold only those below the handoff-overhead threshold. |
| "The parent's acceptance list is good enough for the children." | No child can pass or fail alone, so nothing is verifiable until everything is. |
| "Just read all the files first for context." | That is the input-shaped tell. Size, filter, batch. |
| "The merge looks thin — spawn another level." | Depth 2 is never the fix; re-read the disputed span. |
| "This packet is small, it can carry a judgment call." | Size does not move a judgment task off the coordinator — surface-allocation test 2, no exception. |
| "I'll keep the manifest in my head." | Unwritten means two sessions answer the same question (the Q-SFRISK-1 collision, pinned in [TOMBSTONES](../../../docs/adr/TOMBSTONES.md)). |

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
| `inqhiori` §14 (contested-question decomposition) | A question with too many axes → that skill; work with too many parts → this one. A bundled question inside an oversize brief goes there first — the cut lines often follow the axes. If the parent's done cannot be stated in two sentences, refine before decomposing. |
| [surface-allocation ADR](../../../docs/adr/2026-07-14-cc-cursor-surface-allocation.md) §Decision "Orchestrating more than one worker at a time" | Owns the orchestration rules that consume the manifest and children when 2+ packets are frozen implementation: claim manifest, disjoint footprints (single-writer rule), dispatch-time Phase-0 re-check, review-round-as-freeze, frozen-SHA dispatch pointer. |
| `brief-authoring` | Authors each child as a `cc_handoff` brief; check 8's `BLOCKED — scope-problem` sub-case sends the packet back here for re-cutting. |
| `handoff-verify` / `handoff-verify-panel` | Pre-dispatch verification of a child; post-execution judging of its return (this skill renders no verdict on returned work). The panel is the input-shaped protocol applied to a many-claim packet. |
| `task-routing` | Picks local vs cloud per child after the cut. |
| `fable-method` | Step 2 owns evidence gathering and points here when the input is oversize; Step 4.4's checklist is the in-session lane for work that still fits one session. |
| Rule 2 ([ADR](../../../docs/adr/2026-06-16-rule-2-budget-before-acting.md)) | Sets the per-child iteration budget; this skill cuts so the tripwire fires at a child boundary rather than mid-unit. |

## Imported rules

Adapted 2026-09-15 from external drafts (`troykelly/claude-skills` issue-decomposition, `DevelopersGlobal/ai-agent-skills` task-decomposition, `massimodeluisa/recursive-decomposition-skill`). Every imported rule must justify itself on repo grounds. Standing consequences:

- Budgets are never in minutes or hours (Rule 2): the unit is iterations within the loop-class budget, and "one session".
- No new document-conversion dependency (`anydoc`, `firecrawl`): convert PDF / Office input with what the session already has, then apply the protocol to the text.
- Children are brief packets, dispatch issues and PRs under a manifest: no GitHub sub-issue labels, Projects board or knowledge graph.
