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

_Required shape (as authored): the ratified D-T00 wording quoted; the operator's §4 answer; the P1–P7 table per candidate with evidence; the verdict (PRODUCER FOUND / INSUFFICIENT); for INSUFFICIENT, the missing set and the build estimate; the condition-4 question restated. No recommendation on step 2 beyond what the table supports._

**Status: NEEDS_CONTEXT.** Returned 2026-09-22 by the Claude Code executor (cloud session), branch `claude/t00-step1-producer-inventory` off `claude/sweet-mccarthy-mviy90` @ `082366c`. Handoff-verify Phase-0: PASS. No cited owner differs between this base and `origin/main` @ `c19573c`. The D-T00 row is ratified. TB-I2's footprint is absent.

**Why NEEDS_CONTEXT, not a final verdict.** §3's candidate-4 search found `ops/c1_rail/qualification/`. It is a synchronized four-leg `BookReplay` that emits per-session `intraday_low` and feeds it to `simulate_path`. It is TB-I2's engine, relocated. [`2026-09-15-phase3-qualification-tooling.md`](../../superpowers/plans/2026-09-15-phase3-qualification-tooling.md) line 5 says: "Package is `ops/c1_rail/qualification/`: this corrects the proposed lab placement because the accepted monorepo boundary prohibits lab importing ops." Its classes are the ones the [TB-S2 spec](../../spec/2026-09-12-tradeify-synchronized-replay-spec.md) interface table assigns to TB-I2: `BookReplay`, `SessionRecord`, blocks, paths, `WeekClock`, and the `dd_scale == 1.0` runner. Under §3.3, a finding that TB-I2 exists changes this packet's premise and returns to the coordinator before scoring. That candidate is therefore **inventoried and its existing tests run, but it is not scored P1–P7**. Every other candidate is scored below.

### 7.1 Ratified D-T00 wording (verbatim, [amendment Addendum 2026-09-22](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md), row D-T00)

> "D-T00 TICKED for step 1 only. Step 1's producer test uses `simulate_path`'s definition of `intraday_low` — a per-day minimum-equity *excursion* from the day's opening equity, entries `<= 0`, unscaled (`core/mc/simulation.py:325–345`) — as a named acceptance criterion; a producer emitting absolute lows fails it. Step 1 states, per expression of the selected four, what the producer reproduces of integer sizing / ORB base-add / capacity / takeover. Step 2's pre-registration cites `2026-08-26-prop-survivor-scoring-prereg-v2.md` and either adopts it or states why the selected book falls outside it; no second pre-registration for the same falsifier. Condition 4 — the operator rules, before step 2, whether T00's screen is §4 falsifier evidence: if yes, its ceiling, tiers and dating follow the four-firm ADR §4 as frozen; if no, the falsifier needs its own dated re-MC before 2026-11-08 regardless of T00."

Operator ruling on the row, verbatim: "Adopt all five as recommended."

### 7.2 Operator's §4 answer

The §4 question was asked once, as the session's first message. The operator's reply, verbatim: **"you can't reach your local backups or the private archive. Meanwhile, score the other candidates without waiting"**. The reply confirms the session cannot reach the private stores. It does not say whether a copy survives, or where. **Owed:** whether any copy survives, and its location.

### 7.3 Evidence runs (interpreter: `python -I scripts/fp.py --env <scratch>/ops-env`, Python 3.11.15, venv built from `requirements-ops.lock` with `--require-hashes`, outside the checkout)

| Run | Command | Result | `record.json` (run dir · SHA-256) |
|---|---|---|---|
| R1 | `test-ops` (subcommand ignores path args; ran all of `tests/ops/`) | 2570 passed, 36 skipped, **1 failed**: `test_qualification_isolation::test_qualification_suite_in_clean_process`. The child pytest fails collection with `ModuleNotFoundError: cryptography`, an optional signing package absent from the lock (`scripts/fp.py:38–41` treats it as optional). Environmental; not about any candidate. | `20260922T231818Z-de49c066ad40` · `b3e75d4f…646a81` |
| R2 | `python -m pytest tests/ops/test_tv_broker_emulator.py tests/ops/test_book_policy.py tests/ops/test_book_adapters_parity.py` | 52 passed, 12 skipped (all four private ports and `effective_inputs.json` absent) | `20260922T231940Z-6fcb0b0c8d38` · `a4a7df76…0da5e` |
| R3 | `python -m pytest tests/ops/qualification/test_{replay,runner,sessions,model,paths,blocks}.py` | 85 passed | `20260922T231944Z-dd039131c404` · `a182fe79…d755e13` |
| R4 | P6 probe (source in §7.6), run as a pytest file | 1 passed; emitted series SHA-256 (`<f8` bytes) `4b2b460b00be3043843dc71e527ce0a9df6f8af1819ad112e1e7c01bbf1c937d` | `20260922T232026Z-6e5a8c525ac3` · `9ad1bc76…17f6d3` |

Records sit under the ignored `.cache/fp-verification/` of the executing clone. All four were taken at `082366c` with a clean tree.

### 7.4 P1–P7 per candidate (the selected four: Aegis 6J, Vanguard MGC, Striker MYM, ORB MNQ)

**Candidate 1: seven-strategy joint replay, 125-test synthetic replay, canonical ledgers.** **UNKNOWN — operator input owed** (not UNREACHABLE; the survival question is unanswered).

| P1 | P2 | P3 | P4 | P5 | P6 | P7 |
|---|---|---|---|---|---|---|
| UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN: no copy reachable; no `local_artifacts/` or `.worktrees/` in this clone |

Public digests that prove what existed: C1–C5 approval revision `bad72266716a31782960c49deed0e25c8c2dc8256300cd8bbc2423d7778d73aa` ([campaign state §53](../programs/2026-09-03-seven-strategy-select-campaign-state.md), line 3775). 125-test private disposition `6b88401332405d2c8e70ebe7bd6bb40999379f818304fdbef757005e1475e7f3` (§54, line 3818). Source-export digests for the five retained legs are in the same file, lines 956–960. The loss is recorded in M-41 (`methodology_lessons.md:1502–1508`). Two limits apply even if a copy survives. The 09-09 gate says "the full replay bundle is not accepted", and partial-leg support plus real bindings remain open ([governing plan](../../superpowers/plans/2026-09-02-seven-strategy-tradeify-select-configuration.md) lines 43–49). It was also built for the seven-entry menu.

**Candidate 2: TB-S2 emulator** (`ops/c1_signal_daemon/tv_broker_emulator.py`, with the per-leg private adapters loaded via `book_adapters.py`).

| # | Score | Evidence |
|---|---|---|
| P1 | NOT MET | The emulator fills whatever quantity an intent carries (`tv_broker_emulator.py:1–35` scope). The ruled integer law is `book_policy.entry_quantities` / `add_quantity` (`book_policy.py:255–333`), which the per-leg emulator path never calls. The law itself is tested: `test_book_policy.py:105 test_protected_and_lifecycle_integer_table`, `:109`, `:119` (R2). |
| P2 | NOT MET | Nothing in the emulator is keyed on protection state. The components exist: `book_policy.transition_cancels` (`:475`), with `test_book_policy.py:161` (R2), and `add_quantity` refuses protected ORB adds (`book_policy.py:25–27` docstring). |
| P3 | NOT MET | No account ledger in the emulator. The component exists: `CapacityLedger` (`book_policy.py:570–740`), with `test_book_policy.py:169 test_reservation_accounting_refuses_not_clips` (R2). |
| P4 | NOT MET | No takeover in the emulator. The component exists: `Takeover` (`book_policy.py:506–567`), with `test_book_policy.py:182`, `:203`, `:233` (R2). |
| P5 | NOT MET | One emulator per leg ("per-leg TV-faithful replay broker … **not** the synchronized multi-leg replay", `dispatch-1:44`). |
| P6 | NOT MET | Emits `ExecutionEvent`/`Fill` only. No equity or excursion series exists, so there is nothing to feed `simulate_path`. |
| P7 | UNKNOWN | Private ports absent here (R2 skips). Their pins are public: `book_adapters.py:39–62` (runtime SHA-256 per leg) and `:72` (`RUNTIME_EFFECTIVE_INPUTS_SHA256`). The four M15 panels are absent here; pins are in `core/data/bar_data/SHA256SUMS`. |

The emulator's gap is not P5 alone; P1–P4 and P6 are also missing from it. The P1–P4 laws exist and are tested in `book_policy.py`. Composing them with the emulator on one clock is exactly what the unscored candidate 3′ does.

**Candidate 3: TB-I2 at its specified footprint.** **ABSENT.** `ls lab/analysis/c1/tradeify_book_replay_2026-09/` → "No such file or directory". No `lab/` file references the path.

**Candidate 3′ (found under §3.4): `ops/c1_rail/qualification/`, TB-I2 relocated.** **FOUND — NOT SCORED (premise change, §3.3).** Inventory only:
- `replay.py:89–574` `BookReplay`: one shared cash and one clock across the four legs (`:448–574`). It wires `book_policy` sizing (`:357–365`), `CapacityLedger` and `Takeover` (`:372–399`), `BookProtectionClock` mode per session (`:467`), and the `TVBrokerEmulator` per leg (`:118`). Each session's `low` uses lifetime-scoped adverse marks (`:57–86`, `:207–255`, `:517–569`).
- `model.py:149–163` `SessionRecord.intraday_low` rejects values `> 0`.
- `sessions.py:19–21` emits the per-session `pnl` / `intraday_low` arrays.
- `runner.py:20–32` calls `simulate_path(pnl, trigger, 1.0, horizon, intraday_low=low, initial_state=…, **firm_kwargs("Tradeify_Select_100K", …))`.
- `panel.py:33–37` loads M15 bars against an expected SHA-256.
- Relevant existing tests passed in R3, including: `test_replay.py:127`, `:226`, `:284`, `:355`, `:377`, `:278`, `:154`, `:639`; `test_runner.py:16 test_kernel_uses_intraday_and_no_second_scaling`.
- All of this is synthetic. The module docstring says "no loading or qualification authority" (`replay.py:1`), and production execution is gated by the attempt controller ([Phase 3 completion plan](../../superpowers/plans/2026-09-17-phase3-completion-handoff.md) line 31).
- Its real inputs are the same private ports and panels as candidate 2, none of them present here.

**Candidate 4a: `lab/analysis/c1/tradeify_book_composition_2026-09/book_grid.py::build_intraday_low_sequenced`.**

| # | Score | Evidence |
|---|---|---|
| P1 | NOT MET | Uniform per-contract × k scaling of recorded trades (`book_grid.py:186–187`); header: "NOT a bar-level replay" (`:7–9`). |
| P2 | NOT MET | No protection state. Recorded ORB trades are replayed as captured (`:10–21`). |
| P3 | NOT MET | Micro-equivalents are reported, not enforced (`:60`, `:346`). |
| P4 | NOT MET | No takeover path. |
| P5 | NOT MET | A trade-level sweep line over recorded trades (`:179–225`), not a shared-equity replay. |
| P6 | MET in form | R4: the emitted series was accepted by `simulate_path`'s validation. Day 2024-01-09 recomputed by hand gives −100: open 2×(−25), then open −50 → −100; close +80 → +30; close −30 → +50; minimum −100. Absolute lows (`100000 + low`) were refused with the `<= 0` error, and a series one day short was refused with the horizon error. |
| P7 | NOT MET | Built for a different book: ORB-MNQ, ORB-MYM and Aegis 6J1 (`:1–21`, `:60`), with no Vanguard MGC and no Striker MYM. Its TV trade-list inputs are uncommitted (`:11`). |

**Candidate 4b: `lab/research_utils/book_score.py` and `msl_score.py`.** Per-leg daily series composed by date-aligned summation (`book_score.py:87–110`); `msl_score.py:7`, `:227–280` build `intraday_low` from a TV trade list, a close-only lower bound when there are no MAE columns. **P1–P5 NOT MET** (no sizing, protection, capacity, takeover or shared clock). **P6 MET in form** (the `<= 0` checks at `book_score.py:78`, `:109` and `msl_score.py:279`). **P7 not applicable**: these are scorers of supplied series, not producers of the selected book.

**§3.4 cold-store checks.** `lab/CATALOG.md` In flight lists `tradeify_seven_strategy_phase1_2026-09` as ACTIVE (normalization only; its directory holds no replay engine). `lab/ARCHIVED.json` has no seven-strategy or book-replay entry. `docs/ltm/README.md` routes private history to `first-passage-archive` (not reachable here).

### 7.5 Verdict

**Over the scored candidates (1, 2, 3, 4a, 4b): INSUFFICIENT.** No candidate has P1–P7 all MET. This follows mechanically from §7.4. **It is not final.** Candidate 3′ is unscored under §3.3, and its inventory matches the producer's shape. The coordinator must rule on the premise before this verdict can stand.

**Smallest missing set, by coordinator ruling (estimates, labelled as such):**
- **If 3′ is admitted as the step-1 candidate:** no new producer code is identified as missing. What's missing is **P7 inputs plus a real-input scoring run**: the four private ports at the pinned runtime digests; `effective_inputs.json` at `9d4d4e1d…`; the four M15 panels matching `SHA256SUMS`; and adapter parity at protected and adds-off sizes. The [Stage-2 plan](../../superpowers/plans/2026-09-14-stage2-runtime-integration.md) line 21 records export "collection 7/7, acceptance 0/7" as of #382, not re-verified here. The run happens on the operator's primary checkout, under whatever authority the attempt controller requires. **Estimate:** one executor session on that checkout, about 100k–250k tokens, to score P1–P7 with real inputs. P6's hand recompute there needs one real bar-level day.
- **If 3′ is ruled out of scope:** **TB-S2 emulator + P1–P4 wiring + P5 synchronization + P6 emission**, i.e. building TB-I2 per the spec. **Estimate:** sized by the existing analogue, about 1.2k lines of engine and about 1k lines of tests (`qualification/{replay,paths,blocks,sessions,runner,clock,panel,model}.py`; four test files). Roughly 3–6 agent sessions, 0.5M–1.5M tokens, plus the same P7 inputs. Duplicating 3′ would be the main cost risk.

**Owed to the coordinator:**
1. The premise ruling on 3′.
2. The D-T00 grounds ("the only in-repo replay artifact is the TB-S2 emulator") and the amendment §5 audit hook (`ls lab/analysis/c1/tradeify_book_replay_2026-09/`) are stale with respect to 3′. This executor edits only §7, so both are left for the coordinator.

### 7.6 P6 probe source (synthetic; no screen, no MC; run as R4)

```python
import sys, numpy as np, pandas as pd
sys.path[:0] = ["lab/analysis/c1/tradeify_book_composition_2026-09", "core"]
import book_grid as bg
from mc.simulation import simulate_path
T = pd.Timestamp
trades = {"mnq": [dict(entry_time=T("2024-01-09 10:00"), exit_time=T("2024-01-09 11:00"), entry_date=T("2024-01-09"), exit_date=T("2024-01-09"), net_pnl_per_contract=40.0, mae_per_contract=-25.0)],
          "aegis": [dict(entry_time=T("2024-01-09 10:30"), exit_time=T("2024-01-09 12:00"), entry_date=T("2024-01-09"), exit_date=T("2024-01-09"), net_pnl_per_contract=-30.0, mae_per_contract=-50.0)]}
idx = pd.bdate_range("2024-01-08", "2024-01-10")
low, realized = bg.build_intraday_low_sequenced(trades, {"mnq": 2, "aegis": 1}, idx)   # -> [0, -100, 0], [0, 50, 0]
assert low[1] == -100.0
simulate_path(realized.reshape(-1, 1), 0.01, 1.0, 3, intraday_low=low)          # accepted
simulate_path(realized.reshape(-1, 1), 0.01, 1.0, 3, intraday_low=100_000.0 + low)  # ValueError (<= 0)
simulate_path(realized.reshape(-1, 1), 0.01, 1.0, 3, intraday_low=low[:-1])      # ValueError (horizon)
```

### 7.7 Condition 4, restated for the operator

**Is T00's screen §4 falsifier evidence for the 2026-11-08 trigger?** If yes, its ceiling, tiers and dating follow the four-firm ADR §4 as frozen. If no, the falsifier needs its own dated re-MC before 2026-11-08, regardless of T00. Step 1 does not bear on this ruling. No step-2 recommendation is made: the table supports none until the coordinator rules on 3′ and P7 is scored with real inputs.

Not done, as scoped: no producer was built or patched; no screen, MC or re-MC was run; no pre-registration was drafted; no private artifact, account figure or Pine was committed; the seven-entry menu was not scored.
