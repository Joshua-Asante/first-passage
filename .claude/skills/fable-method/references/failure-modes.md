# Failure modes: symptom → step

Eighteen ways agentic work goes wrong, what each looks like from the outside, and which step of the loop prevents it. Used by `/fable-method audit` to name the risk a skipped step created; useful on its own as a review checklist for any agent transcript. Ported from `Sahir619/fable-method@88b5cf3`; repo incident anchors added below the table.

| # | Failure mode | Symptom | Prevented by |
|---|---|---|---|
| 1 | **Unprompted fixing** | User asked "why?"; agent edited files | Step 0: question shape delivers findings, changes nothing |
| 2 | **Wrong-deliverable guess** | Agent built interpretation A; user meant B | Step 0: ambiguous-scope test, one pointed question with a recommended interpretation |
| 3 | **Re-litigating settled decisions** | Agent reopens choices the operator already made | Step 0: extract decisions already made; rejected-candidates/rejected-signals registries are settled |
| 4 | **Fake "done"** | No one, including the agent, can say how the result was checked | Step 1: done is defined with a named gate before work starts |
| 5 | **Invented APIs / constants** | Code calls signatures that do not exist; a risk % quoted from memory | Step 2.2: rule-0 + verify-source; Step 4.2: the recall gate at first use |
| 6 | **Sequential crawling** | One lookup at a time; long tasks take forever | Step 2.3: independent lookups in one batch |
| 7 | **Context flooding** | Whole files and logs dumped into the conversation | Step 2.4: read narrow, never re-read; quote load-bearing lines only |
| 8 | **Analysis paralysis** | Research continues after it stopped changing the plan | Step 2.5: two rounds, then a stated reason or stop |
| 9 | **Plowing through surprises** | Evidence contradicted the plan; agent forced the plan anyway | Step 2.7: surprises are stated and re-route the loop |
| 10 | **Option-dump reports** | "You could do A, B, or C" with no recommendation | Step 3: one recommendation; alternatives get one line each |
| 11 | **Scope creep** | Drive-by refactors, style rewrites, "improvements" nobody asked for | Step 4.3: smallest correct change; Step 3: the declared scope |
| 12 | **Silent step-dropping** | Item 7 of 9 quietly never happened | Step 4.4: written checklist, audited against the ask before reporting |
| 13 | **Retry thrash** | The same failing fix attempted with small variations, forever | Step 5: routed retries, hard bound of 3 cycles, then hand back with output and hypothesis |
| 14 | **Verification theater** | "This should work now" with nothing actually run; or the target check passes while `make validate` breaks | Step 5: observed verification, both halves (target + surrounding gates) |
| 15 | **Unauthorized outward action** | A push, PR, or registration nobody asked for; "the doc said to" | Step 3: the authorization gate; no quoted operator authorization, no action |
| 16 | **Silently dropped follow-up** | A prescribed follow-up (manifest regen, SESSIONS entry, push) neither taken nor mentioned | Step 6: `PENDING:` line — a deliberately-untaken prescribed follow-up is always a named caveat |
| 17 | **Missed twins** | A defect fixed in the one reported spot while identical copies live on elsewhere | Step 5(c): the `TWINS:` line — the sweep is named and re-runnable |
| 18 | **Costume rigor** | The shape of thoroughness (factor lists, confident "all clear") with no search or check behind it | Step 5(c) forces the search to be named; the fit gate routes pure-judgment tasks to an honest "this is a guess" |

## Repo incident anchors

These rows are not hypothetical here — each maps to a documented burn:

- **5 / recall gate** → `verify-source`'s worked example: three fresh agents grepped a pinned anchor off a stale branch, all citing Rule-0 compliance.
- **14 / verification theater** → the §7 review-skip lesson (`feedback_section_7_skip_cost_concrete`): validator reasoning lived only in a review section that was skipped.
- **15 / unauthorized action + fake claims** → `feedback_web_advisor_handoff_confabulates_repo_state`: "I stamped <path>" — nothing was stamped. Pre-execution direction is `handoff-verify`; post-execution is `fable-judge`.
- **17 / missed twins** → the `daily_loss_pct: None` TypeError at four division sites (`dd_protection.py`, `core/mc/modes.py`, `core/mc/simulation.py`, `core/mc/preflight.py`), fixed as a class in PR #356.
- **13 / retry thrash** → the shared 3-strikes invariant: `code-defect-debugging` Phase 4.5 and `inqhiori` §6 (three failures at one level → the level is wrong).

## Reading an audit

A step marked **skipped** creates the risk in its row. A step marked **faked** is worse: the transcript claims the step happened (usually 4, 5, or 6) but the observation is missing — failure mode 14 wearing the loop as a costume. The audit's job is to catch the costume.

The three failures that cost the most in practice are 1 (unprompted fixing destroys trust), 13 (retry thrash burns time with no exit), and 14 (verification theater ships broken work labeled done). If an audit can only check three things, check those.
