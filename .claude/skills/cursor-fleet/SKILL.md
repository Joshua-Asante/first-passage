---
name: cursor-fleet
description: Use when a task decomposes into 2+ independent, spec-freezable IMPLEMENTATION packets — CC stays the ORCHESTRATOR (decompose, freeze specs, own the claim manifest, review, integrate, adjudicate) and Cursor agents are the WORKERS (their tokens, not Claude's). Triggers on "cursor fleet", "fan out to cursor", "team of agents", "parallel implementation", or any multi-packet build where solo CC execution would burn context on mechanical work. NOT for read-only research/verification fan-out (that is Claude-side Workflow/subagents), NOT for single builds (plain CC/Cursor handoff per the surface-allocation ADR), NOT for locked-surface work (ADR test 1 routes core/Pine/doctrine to CC solo, always).
---

# Cursor Fleet — CC orchestrates, Cursor implements in parallel

Extends `docs/adr/2026-07-14-cc-cursor-surface-allocation.md` from one-build-at-a-time to N parallel workers under one orchestrator. **Every ADR clause still binds per packet** — this skill adds the orchestration layer, it never relaxes the routing tests, the handoff contract, or "no commit/merge without operator go." Every rule below exists because of a dated failure — the week of 2026-07-18→24 unless the ledger dates it otherwise; the friction ledger at the bottom is the why.

## Routing — three lanes, pick one

| Work shape | Lane | Why |
|---|---|---|
| Read-only research / verification / review fan-out | **Claude subagents (Workflow/Agent tool)** — protocol: `work-decomposition` §Input-shaped (size, filter, batch, depth-1 wave, spot-check) | No branch overhead, results return in-context; e.g. the 14-agent Algorithm review (2026-07-24) |
| One implementation build | **Single Cursor handoff** (ADR flow) or CC solo below the test-3 threshold | Fleet overhead is pure waste at N=1 |
| 2+ independent, spec-freezable implementation packets, each ADR-tests-0–2 clean, jointly clearing test 3 | **THIS SKILL** | CC context goes to judgment (decompose/freeze/review); Cursor tokens go to mechanical build |

Hard disqualifiers for any packet: touches ADR test-1 locked surfaces (core anchor code, Pine, ADRs/pre-regs/CLAUDE.md/STATE.md); spec cannot be frozen without judgment calls mid-build; needs gitignored vendor bytes or secrets in a cloud environment (test 0 → local dispatch or CC).

## The orchestration loop

**1. Decompose into packets with DISJOINT file footprints.** Whether a task is oversize, where it cuts, and the six-point atomic test each packet must pass (one output, one gate, revertible, one session, disjoint footprint, frozen) are `work-decomposition`'s; this step applies its footprint rule at dispatch. No two packets may touch the same file — file overlap is how parallel branches manufacture merge conflicts and semantic auto-merge contradictions. `docs/SESSIONS.md`, `STATE.md`, the umbrella note, and all board/index files are RESERVED to the orchestrator's integration commit; workers never write them (also keeps the merge=union phantom-conflict class to one writer).

**2. One umbrella handoff brief, N packet appendices.** The umbrella is a real `docs/briefs/handoffs/` brief passing `check_brief` (satisfies the ADR handoff contract once, amortizing test-3 overhead across the fleet). Each packet appendix carries exactly four load-bearing elements, nothing more:
   - **Phase-0 staleness check** — the packet's premises as runnable commands, with the explicit no-op condition ("if already fixed on main → return DONE, cite the commit"). This is what caught all three overtakes on 2026-07-24; it is the single most load-bearing line in the packet.
   - **Frozen scope** — exact files, exact edits or acceptance tests; §0.5-style recommended defaults for any ambiguity (Cursor never resolves ambiguity — it bounces `NEEDS_CONTEXT`).
   - **Forbidden moves** — the locked surfaces this packet runs near, plus "no writes outside your file footprint."
   - **Return contract** — `cursor/*` branch named `cursor/<fleet-slug>-p<N>`, PR per packet, tests green, four-state status (`DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED`).

**3. Claim manifest before dispatch.** The umbrella brief carries a dispatch table: packet → branch → files → status (QUEUED / DISPATCHED / RETURNED / MERGED / OVERTAKEN). The orchestrator owns it; it is the anti-duplication device — before ANY session (including a future you) opens work in this area, the manifest says who holds it.

**4. Pre-dispatch gate, per packet, at dispatch time (not fleet-authoring time):**
   - `git fetch origin && git log --oneline origin/main --since="24 hours ago"` — re-verify the packet's Phase-0 premises against CURRENT main. Overtaken → mark OVERTAKEN in the manifest, do not dispatch. (Three artifacts were overtaken between authoring and dispatch on 2026-07-24 alone; the daily-repo-truth-sync task reports this each morning, but the dispatch-moment check is still mandatory.)
   - `gh pr list --state open` — no open PR already touches the packet's files.
   - Test 0 per packet: vendor bytes / secrets → route that packet LOCAL (worktree on this machine), never cloud. This is the `task-routing` skill's local-only checklist, re-applied per packet at dispatch time rather than once at fleet-authoring time — if that checklist changes, this step changes with it.
   - The umbrella brief's review round (Codex, or whatever pre-dispatch review the operator runs on it) has COMPLETED and any re-freeze it produced is merged to `main` before the FIRST packet is dispatched. The review round is part of the freeze, not a track that runs alongside the builds; dispatching from the brief as first opened is a forbidden move. (2026-09-04f: all three workers were fired from `af0203f` while Codex was still reviewing; the re-freeze withdrew packet B and moved packet C's guard after the builds had started.)

**5. Dispatch mechanics (the honest constraints):**
   - Follow the [shared CLI execution contract](../brief-authoring/references/cc_handoff.md#cli-execution-contract-when-dispatching-through-a-cli). Check the installed CLI and current approval result; historical classifier failures are not a universal ban on direct dispatch. A wrapper does not grant authority or bypass a denial. Carry applicable operator authorization forward and capture each worker's process result before retrying.
   - One worktree per packet; workers branch `cursor/<fleet-slug>-p<N>` from CURRENT `origin/main`, never from another packet's branch.
   - Worktree gotchas apply to workers: bare worktrees fail catalog/data gates (doc-only packets commit via doc sub-gates); CRLF pins matter for `.dockerignore`/hash-gated files; `sync_skills` never runs from a worktree.
   - Point each worker at the umbrella brief path + its packet letter + **the commit SHA at which the brief was frozen** (the post-review-round freeze, never the as-first-opened commit). A worker whose pointer SHA no longer matches the brief on `main` returns `NEEDS_CONTEXT` rather than building — a stale pointer is a stale spec, and building it anyway is how a withdrawn packet gets built (2026-09-04f, packet B). The packet must be self-contained enough to survive `handoff-verify` (the 2026-07-24 price-capture handoff bounced `NEEDS_CONTEXT` once for exactly this; re-anchoring cost a round-trip).

**6. Integration — the orchestrator's half of the token savings:**
   - Review each returned PR as **diffs + gate output, never whole-file re-reads** (Pass 1 spec-compliance: diff touches exactly the packet footprint; Pass 2 quality: gates green, no forbidden-move violations). Escalate to `fable-judge` only for claims that matter if wrong.
   - Merge in dependency order, one packet at a time, re-running the fast gates between merges.
   - THEN write the single integration commit: SESSIONS entry, manifest statuses → MERGED, board updates. One writer, one union-merge surface, zero phantom conflicts.
   - A packet returning `DONE_WITH_CONCERNS` gets its concern adjudicated by CC before merge; `NEEDS_CONTEXT` gets ONE re-anchor + re-dispatch, then falls back to CC solo (two bounces means the spec wasn't freezable — that packet was mis-routed).

**7. Fleet-level falsifier (same shape as the ADR's §4):** if 2 fleets in a rolling 8-week window end with integration cost exceeding the estimated solo-build cost (operator-judged, logged in SESSIONS), or any worker lands a spec-interpretation judgment defect, stop fleeting that task class and revert to single-dispatch ADR flow. Do not silently keep fleeting.

## Friction ledger (why each rule exists — week of 2026-07-18→24 unless dated otherwise)

| Rule | Dated failure it encodes |
|---|---|
| Phase-0 staleness + no-op condition per packet | 3 artifacts overtaken in one day (briefs #1/#2 landed independently; Q-C1FILL-1 superseded mid-authoring) — the no-op conditions were what caught them (memory: check-origin-main firing 4) |
| Dispatch-moment re-fetch, not authoring-moment | The overtakes happened DURING the session, after a clean session-start check |
| Disjoint footprints + orchestrator-only SESSIONS/STATE writes | merge=union phantom conflicts on every parallel SESSIONS touch (PR #496); firing-3's clean-auto-merge contradiction class |
| Self-contained packets | Price-capture handoff `NEEDS_CONTEXT` bounce + re-anchor round-trip (commits `e6fab6c`/`c06ae65`) |
| Test-0 local routing per packet | Three cloud→local bounces in 48h (ADR Step-0 addendum, 2026-07-15/16) |
| Wrapper/allow-rule honesty | `cursor-agent` CLI dispatch classifier-blocked; working around it is forbidden, asking once is cheap |
| Umbrella-brief amortization | ADR §6's recorded cost: a full brief per dispatch "costs a real fraction of a session" — at N packets that overhead compounds unless amortized |
| Claim manifest | Q-SFRISK-1 collision (firing 2): two sessions independently answered the same question; a registry of who-holds-what prevents the re-derivation |
| Review round is part of the freeze; dispatch pointer carries the brief's frozen SHA | SESSIONS `2026-09-04f` (fleet dispositioned 2026-09-05): all three workers fired from the brief as first opened (`af0203f`) before Codex's pre-dispatch review re-froze it (`9914dd8e`…`70f1c47c`) — packet B was withdrawn by the re-freeze and built anyway (#304 closed without merge); packet C's guard moved mid-build (C falsified, fix round C1 owed). Relay lag, not worker error — the workers had no SHA to notice the drift by |

## Forbidden moves

- **Fleeting locked-surface work** because "it's just mechanical" — test 1 has no fleet exception.
- **Workers writing SESSIONS/STATE/boards** — one writer, at integration.
- **Dispatching a packet whose Phase-0 premises you verified at fleet-authoring time instead of dispatch time.**
- **Retro-fitting the umbrella brief after workers started** — same class as retro-fitted handoffs (ADR §5).
- **Dispatching from the umbrella brief as first opened, before its review round has completed and its re-freeze is on `main`** — the review round is part of the freeze (2026-09-04f: three workers built against a brief that then withdrew one packet and moved another's guard).
- **Using the fleet to parallelize a judgment task** (design, adjudication, threshold-setting) — judgment stays in CC; if a packet needs judgment mid-build, it was mis-routed.

## Hand-offs

- Sizing an oversize task into packets, the per-packet atomic test, and re-cutting after a second `NEEDS_CONTEXT` bounce → `work-decomposition`
- Packet authoring structure → `brief-authoring` (cc_handoff template, §0.5 Cursor variant)
- Consuming/verifying any packet before dispatch → `handoff-verify`
- Post-return adjudication of load-bearing claims → `fable-judge`
- Routing doubt on any single packet → the ADR's tests 0–3, verbatim
