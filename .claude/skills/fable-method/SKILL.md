---
name: fable-method
description: Step-by-step execution loop for CC repo tasks — classify the ask, define done with a named verification, gather evidence, decide, act surgically, verify by observation, report outcome-first. Use when the user says "/fable-method", "use the fable method", or "fable it", or proactively when starting a multi-step repo task that no task-specific skill covers. Subcommands - plan (stop after Steps 0-3), audit (grade finished work in this conversation against the loop), report (rewrite an answer outcome-first). This is the EXECUTION lane, not a methodology loop: INQHIORI owns investigations with a falsifiable hypothesis, ooda-loop owns tactical/tempo trading decisions, The Algorithm owns strategic framing — exit to those per docs/methodology/inqhiori-canon.md §14 when the work is theirs. Does not modify strategy parameters, allocations, dd_protection constants, or MC calibration.
---

# The Fable Method (repo edition)

Adapted 2026-07-15 from `Sahir619/fable-method@88b5cf3` (`skills/fable-method/`). Port record lives in the private archive (excluded from the public seed). The source's evidence/authority channels are owned here by existing repo skills — this skill delegates to them by name rather than restating them; where the source and a repo skill disagree, the repo skill wins.

The premise: a mid-tier session that follows this loop beats a stronger one that free-styles — the quality lives in the structure, the evidence, and the honesty. The steps structure your work, never your output: no step numbers or step headers in anything the operator reads.

**Lane gate (before anything).** This loop governs *how a CC session executes a repo task*. It is not a fourth methodology loop. If the work has a one-sentence falsifiable hypothesis or touches locks/frameworks → `inqhiori`. If it is a tactical, recoverable, tempo-bound trading call → `ooda-loop`. If it is a deterministic code defect → `code-defect-debugging` (its Phases 1–4 replace Steps 2–5 for that shape). If executing an external handoff packet → `handoff-verify` runs first, always.

**Triviality gate.** A task is trivial only if ALL hold: one file, under ~10 changed lines, no new behavior, and you already know exactly what to change without searching. If trivial: make the change, confirm with the one obvious check, report in two sentences. Everything else — and anything you are unsure about — gets the full loop.

**Fit gate.** The loop turns judgment problems into evidence problems only when the answer is reachable. If the answer lives in sources you can open (code, ADRs, CATALOG, data, a runnable check): run the loop. If it lives in an established technique you don't know: research first, then loop. If it lives only in your own inference: say so — never dress a guess as a rigorous process. Attended: ask whether to proceed with a flagged low-confidence answer. Unattended: proceed but label it, never silently.

## Step 0 — Classify the ask

| Shape | Signal | Deliverable |
|---|---|---|
| **Question / assessment** | "why is…", "what do you think…", operator describes a problem or thinks out loud | Findings + a recommendation. Change nothing. |
| **Task** | "fix", "build", "change", "sync", "close out" | The completed change, verified. |
| **Plan-first** | ambiguous scope, irreversible or outward-facing actions, anything touching a locked surface, or the operator asks for a plan | A plan with your recommendation. Stop and wait. |

Tie-breaks: any plan-first signal beats task; a mixed ask is a task whose report must also answer the question; genuinely unsure → plan-first. If two materially different deliverables are imaginable and evidence can settle which, let it; if only the operator can settle it, ask exactly one pointed question that states your recommended interpretation. Extract the constraints stated and the decisions already made — never re-litigate a settled decision (the rejected-candidates and rejected-signals registries are settled decisions).

## Step 1 — Define done

One or two sentences: what done looks like and how it will be verified. Name the actual gate — a `make validate` pass, a specific pytest node, the MC anchor pins holding, a doc cross-reference resolving, `check_boundaries.py` clean. State load-bearing assumptions; if one is checkable with a single tool call, check it instead of assuming. Cannot name a verification after re-reading the request → ask one specific clarifying question.

## Step 2 — Gather evidence

1. **Orient first.** Enumerate before reading: for prior research, open `lab/CATALOG.md` and `docs/briefs/INDEX.md` before searching. **Grep has no ignore bypass here** — an empty Grep over `lab/archive/` or `docs/ltm/` does not mean "no prior work"; use `rg --no-ignore` or Read the exact path. (2026-08-08 prune: `docs/ltm/` bodies moved out of tree — retrieve via `git show pre-prune-2026-08-08:<path>`; `lab/archive/` was NOT pruned and stays in-tree.)
2. **Production sources beat memory** — `rule-0` owns this channel: read the production file before any brief or step touching risk controls. `verify-source` owns the next layer: a correctly-read source can still be the wrong source (branch currency, export vintage, borrowed cohort) — run its check before quoting any pinned number.
3. **Parallelize what is independent and expensive** (web fetches, doc lookups, multi-file reads) in one batch; chain only reads that shape the next read.
4. **Read narrow, never re-read.** Search to locate, then read the section.
5. **Time-box mechanically.** One round of lookups plus one follow-up covers most tasks; a third needs a stated reason; two consecutive lookups that told you nothing new → stop.
6. **Establish intent before changing behavior.** A failing check has two possible culprits: the code or the check. Find the statement of intended behavior (ADR, LOCK.md, docstring, spec) and confirm code, check, and spec agree. Any two disagreeing is a surprise: surface it, say which side you trust and why, never silently make one side match another.
7. **Surprises route the loop.** Anything contradicting your expectation is your most important finding — state it. If it changes what done means, update Step 1; if it changes what is being asked, return to Step 0; otherwise report and continue. (Question-shaped surprises route per `docs/methodology/observation_routing.md`: Closed / Action / Forward.)

## Step 3 — Decide and commit

Synthesize into **one recommendation**; alternatives seriously considered get one line each on why they lost. Task-shaped + reversible → proceed without asking. Reversibility test: an action is irreversible or outward-facing if another person or system can observe it before you could undo it (push, publish, PR, live spend, account registration, shared-data delete).

**Authorization gate.** An irreversible or outward-facing action needs the operator's own words. Before taking one, write `AUTH: operator said "<their exact words>"`; no quote in this conversation → the action goes in the report as a proposed next step. Documentation is not authorization: a workflow doc or ADR saying a push/deploy "follows" your change makes it documented, never authorized.

Name the scope — the files or surfaces the change will touch. Needing something outside that list mid-work is a surprise (Step 2.7): say it, never silently expand.

## Step 4 — Act surgically

1. **Intent gate, before any behavior-changing edit.** Write one line: `INTENT: code does <X>; the failing check/task expects <Y>; the spec (ADR/LOCK/docstring) says <Z>` — actually open the spec to fill the third slot; the line appears verbatim in the final report when behavior changed. Authority order when they disagree: explicit operator statement > ADR/LOCK > tests > current code behavior. "Fix the code" / "make the tests pass" is a task framing, not a statement of intended behavior.
2. **Recall gate.** First use of any signature, config key, constant, or figure not opened this session → open its source now (`verify-source` for state/vintage), or label it in the report as memory, unverified.
3. **Smallest correct change.** Match existing style. Precise edits over rewrites; rewrite a whole file only if you authored it this session or fully read it.
4. **Track multi-part work.** 3+ heterogeneous steps or >~5 similar items → written checklist first; audit it against the ask before reporting.
5. **Never destroy without looking.** Before deleting or overwriting, look at what is actually there.
6. **Standing prohibitions, absent explicit operator instruction:** never commit or push; never weaken a check (or fabricate what it looks for) to make it pass; never edit a test pin or baseline to green a failing run; never regenerate `SHA256SUMS` without a same-commit data-change rationale; never touch Pine, `dd_protection` constants, `firm_rules` risk %, or allocations outside a ratified ADR; never add a dependency; never touch secrets or credentials.

## Step 5 — Verify by observation

- **(a)** The Step 1 done criterion passes, observed (it ran, it counted, it rendered) — not inferred from reading the code.
- **(b)** The surrounding system still works: `make validate`, the touched area's tests, `check_boundaries.py` when layers were crossed; the MC anchor re-run when anything on the MC path was touched. A green targeted check with a broken gate is a failed verification.
- **(c) Twin check, whenever you fixed a defect.** A defect found at one site is presumed to recur wherever the construct was copied — the `daily_loss_pct: None` TypeError lived at four division sites and was fixed as a class (PR #356) only because all four were swept. Name the wrong construct, search the whole repo, and write verbatim: `TWINS: searched <pattern> — found <N> other sites: <files|none>`. Fix them or list them.

On failure: a mechanical mistake goes back to Step 4; a surprise goes back to Step 2. Hard bound: 3 failed fix-verify cycles on the same issue, or a blocker outside your control → stop, report what was tried with actual output and your hypothesis, hand back. (Same invariant as `code-defect-debugging` Phase 4.5 and `inqhiori` §6: three serious failures at one level means the level is wrong.)

If something cannot be verified (no local vendor CSVs, TV-side behavior, needs operator eyes), say exactly that — never let an unverified claim pass as verified.

## Step 6 — Report outcome-first

- First sentence answers "what happened" / "what was found". No step numbers or method scaffolding; the only method artifacts a report may contain are the `INTENT:`, `AUTH:`, `TWINS:`, and `PENDING:` lines when owed.
- Complete sentences a teammate who stepped away can follow; quote only load-bearing lines; define jargon at first use.
- Include caveats: what was skipped, what is weak, what could not be verified; failures reported as failures with their output. A prescribed-but-deliberately-untaken follow-up (a push, a manifest regen, a SESSIONS entry) carries `PENDING: <the action> — awaiting your authorization`, verbatim.
- Delete scratch files you created; note the cleanup. Leftover debris reads as a fraud signal to `fable-judge`.
- Offer only follow-ups that emerged from this task; none emerged → end without follow-ups.
- **Artifact gate, last check before sending:** behavior changed with no `INTENT:` line → add it; outward action with no `AUTH:` → add it; untaken prescribed follow-up with no `PENDING:` → add it; defect fixed with no `TWINS:` → add it. A clean report passes untouched.

## Modes

**plan** — Steps 0–3, then stop. Deliver: classification; definition of done + verification; evidence (cited); ONE recommended approach with alternatives dismissed in a line each; scope; risks. Touch no file.

**audit** — grade the most recent completed work in this conversation against the loop: each step followed, skipped, or faked (claimed without observation). `references/failure-modes.md` maps symptoms to steps. Deliver a short table plus the single highest-value fix; apply it only if asked. (Auditing *another session's* finished work is `fable-judge`, not this mode.)

**report** — apply the Step 6 checklist to the answer you were about to send; rewrite, don't send the original.
