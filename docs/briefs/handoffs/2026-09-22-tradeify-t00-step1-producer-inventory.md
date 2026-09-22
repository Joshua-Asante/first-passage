# Handoff — Tradeify T00 step 1: faithful-producer inventory for the selected four-strategy book

**Type:** cc_handoff (inventory and verification; building a producer is explicitly out of scope)
**Date:** 2026-09-22
**Status:** READY TO DISPATCH, not yet dispatched. Authorized by **D-T00, ratified 2026-09-22 for step 1 only** ([amendment Addendum 2026-09-22, row D-T00](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#addendum-2026-09-22--4-dispositions-ratified-2026-09-22--all-five-adopted-as-recommended-and-the-5-correction-applied)). Parent packet: [amendment §T00](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#t00--feasibility-evidence-for-the-selected-book-new-investment-decision-not-a-gate-250k500k-may-return-early). T00 runs in parallel with the spine and **gates nothing**, including T02/S3.
**Executor:** one executor (Claude Code; reading, tracing and running existing tests). **Coordinator:** dispatches, and receives the return. **Operator:** Joshua answers the private-artifact question in §4 and rules condition 4 after the return; he alone ratifies any step 2.
**Authority:** read the owners below; run existing tests and read-only probes; write §7 of this packet and nothing else in the repository. No new producer code, no screen, no pre-registration, no MC run. A `DONE` status supplies no permission for step 2.

## 0. Owners to read first (anchors: `git log -1 --format='%h %as' -- <path>` at dispatch; re-anchor if `main` has moved)
- Amendment §T00 (the three outcomes; step 1 wording) and the **D-T00 row of Addendum 2026-09-22** (the ratified wording, including conditions 1–4). Quote the ratified wording verbatim in the return.
- `core/mc/simulation.py::simulate_path` — the `intraday_low` parameter, its docstring and its validation (currently about `:309–366`). This is the **consumer**, not a producer. Its definition is the named acceptance criterion in §2.
- `docs/notes/2026-09-10-tradeify-protection-selection.md` — the selected configuration: the four expressions, 1% combined-drawdown trigger, 40% scale, full-size ORB base, ORB adds off during protection, 80-micro shared capacity and Aegis-priority takeover ordering; the "Feasibility screen closure" section (why the 09-09 screen is not accepted either way).
- `docs/notes/2026-09-12-tradeify-portfolio-coordinator-dispatch-1.md` — TB-S2 (per-leg TV-faithful replay broker, **not** the synchronized multi-leg replay, `:44`); TB-I2 synchronized replay **BLOCKED**, never built (`:53`, `:110`).
- `docs/adr/2026-09-05-tradeify-select-striker-expression-readmission.md` (joint-replay acceptance, about `:103`) and **M-41** in `docs/methodology/lessons/methodology_lessons.md` (the seven-strategy campaign's joint replay, 125-test synthetic replay and canonical ledgers lived under removed `.worktrees/*`; public records keep digests only).
- `docs/briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md` (status line) — read for context only; step 1 neither adopts nor amends it.
- `docs/load_bearing_numbers.md` — the EOD-clock lower-bound rule. The `lesson_tradeify_trail_enforced_intraday` entry in `docs/methodology/LESSONS_INDEX.jsonl`.

## 1. Selected outcome and return boundary
**Outcome:** a verified answer to "does a faithful producer exist today that can emit, for the selected four-strategy book under Tradeify Select's rules, a synchronized daily P&L path **and** the matching `intraday_low` excursion series?" **Return boundary:** either **PRODUCER FOUND** (named, located, tested, with its gaps listed) so the operator can rule condition 4 and consider step 2, or **INSUFFICIENT** with the exact blocker and a build-cost estimate. INSUFFICIENT is a legitimate, complete return, not a failure.

## 2. The acceptance criteria every candidate is scored against
A candidate is a faithful producer only if it meets **all** of these. Score each as MET / NOT MET / UNKNOWN, with a code line, a test, or a retained output as evidence.

| # | Criterion | Evidence required |
|---|---|---|
| P1 | Reproduces the selected book's **integer sizing** per leg (no uniform P&L scaling) | a test or code path that computes contracts from equity and risk |
| P2 | Reproduces **ORB base/add** behavior, including adds off while protection is active | a code path keyed on the protection state |
| P3 | Enforces the **80-micro shared capacity** | a code path; a test that hits the cap |
| P4 | Implements **takeover ordering** (Aegis priority; lower-priority whole legs closed to make room) | a code path; a test that forces a takeover |
| P5 | Legs are **synchronized on one intraday clock** (shared equity, not per-leg replays summed afterwards) | the event-loop or merge code |
| P6 | Emits `intraday_low` as `simulate_path` defines it: per day, the minimum-equity **excursion below that day's opening equity**, entries `<= 0`, **unscaled**, covering the horizon. A producer emitting absolute lows fails P6. | feed one emitted series to `simulate_path`'s validation (or a copy of its checks) and show it is accepted; show one day recomputed by hand from the bars |
| P7 | Its inputs exist and are reachable: the bar panels or trade ledgers it consumes are present (private root or archive), and their digests match the public records | `SHA256SUMS` / manifest match, or the digest recorded in the owning public record |

## 3. Candidates, in this order (return early on the first decisive result)
1. **The seven-strategy campaign's joint replay and canonical ledgers** (private). Per M-41 the working copies were removed with `.worktrees/*`. First ask the operator (§4) whether a copy survives in `first-passage-archive`, a local backup or `local_artifacts/`. If none survives, record **UNREACHABLE** with the public digests that prove what existed, and move on. If one survives, verify the bytes against the public digests (P7) before scoring anything else; then score P1–P6 **for the selected four**, not for the seven-entry menu it was built for.
2. **TB-S2 emulator.** Per dispatch-1 it is per-leg, not synchronized; expect P5 NOT MET. Score it anyway: if P1–P4 and P6 are met per leg, the gap to a faithful producer is P5 only, which sets the build cost.
3. **TB-I2 synchronized replay.** Expected absent (`lab/analysis/c1/tradeify_book_replay_2026-09/` did not exist on 2026-09-22). Confirm by search and record ABSENT; a claim that it exists changes this packet's premise and must return to the coordinator before scoring.
4. **Anything else found by search** (`rg` over `lab/`, `ops/`, `core/`, `tools/` for replay, `intraday_low`, capacity, takeover). An empty `rg` result is not evidence of absence (AGENTS.md: cold stores, removed bodies, gitignored inputs); check `lab/CATALOG.md` **In flight**, `lab/ARCHIVED.json` and the retrieval guidance in `docs/ltm/README.md` before declaring nothing exists.

## 4. Operator input (ask once, at the start)
"Does any copy of the seven-strategy campaign's private evidence base survive (joint replay, 125-test synthetic replay, canonical ledgers, private overrides) — in `first-passage-archive`, a local backup, or `local_artifacts/`? If so, where?" Record the answer verbatim (no account identifiers). If the answer is unavailable within the session, proceed with candidates 2–4 and mark candidate 1 **UNKNOWN — operator input owed**, not UNREACHABLE.

## 5. Verification of the return
- Every MET cites a file:line in the producer, a test the executor actually ran (command, interpreter, `record.json` from `.cache/fp-verification/`), or a retained output with its hash.
- P6 is shown by running the validation, not by reading the docstring.
- The verdict follows mechanically from the table: **PRODUCER FOUND** only if one candidate has P1–P7 all MET; otherwise **INSUFFICIENT**.
- For INSUFFICIENT: the smallest missing set (e.g. "TB-S2 + P5 synchronization + P6 emission"), what it would take to build (files, tests, rough agent-hours or tokens), and what inputs it needs that are not in hand. The estimate is labelled an estimate.

## 6. Forbidden
Building or patching a producer; running any screen, MC or re-MC; drafting or ratifying a pre-registration (step 2); carrying the 09-09 screen or any EOD-clock "zero bust" forward as survival or as a bound; re-optimizing or re-sizing any expression; changing `dd_protection`, MC calibration or allocations; committing private artifacts, account figures, Pine source or locked-logic ports (public-clone posture); scoring the seven-entry menu instead of the selected four.

## 7. Executor return
_Pending._ The ratified D-T00 wording quoted; the operator's §4 answer; the P1–P7 table per candidate with evidence; the verdict (PRODUCER FOUND / INSUFFICIENT); for INSUFFICIENT, the missing set and the build estimate; the condition-4 question restated for the operator's ruling ("is T00's screen §4 falsifier evidence for the 2026-11-08 trigger?"). No recommendation on step 2 beyond what the table supports.
