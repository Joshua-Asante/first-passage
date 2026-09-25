# Handoff — Tradeify T00 step 1: faithful-producer inventory for the selected four-strategy book

**Type:** cc_handoff (inventory and verification; building a producer is explicitly out of scope)
**Date:** 2026-09-22
**Status:** RETURNED 2026-09-22 (INSUFFICIENT); **ACCEPTED 2026-09-23** by the operator, with condition 4 ruled no ([§7.8](#78-operator-rulings-on-the-return-2026-09-23)). Originally DISPATCHED 2026-09-22 to one Claude Code executor session (branch `claude/t00-step1-producer-inventory`; its return lands in §7). Authorized by **D-T00, ratified 2026-09-22 for step 1 only** ([amendment Addendum 2026-09-22, row D-T00](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#addendum-2026-09-22--4-dispositions-ratified-2026-09-22--all-five-adopted-as-recommended-and-the-5-correction-applied)). Parent packet: [amendment §T00](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#t00--feasibility-evidence-for-the-selected-book-new-investment-decision-not-a-gate-250k500k-may-return-early). T00 runs in parallel with the spine and **gates nothing**, including T02/S3.
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

**Status: DONE_WITH_CONCERNS.** Returned 2026-09-22 by the Claude Code executor (cloud session), branch `claude/t00-step1-producer-inventory` off `claude/sweet-mccarthy-mviy90` @ `082366c`. Revised at `4c1161c` (after merging `origin/main` @ `c19573c`) to score candidate 3′. Handoff-verify Phase-0: PASS. No cited owner differs between this base and `origin/main`. The D-T00 row is ratified. TB-I2's footprint is absent.

**How candidate 3′ came to be scored.** §3's candidate-4 search found `ops/c1_rail/qualification/`. It is a synchronized four-leg `BookReplay` that emits per-session `intraday_low` and feeds it to `simulate_path`, and it is TB-I2's engine, relocated. [`2026-09-15-phase3-qualification-tooling.md`](../../superpowers/plans/2026-09-15-phase3-qualification-tooling.md) line 5 says: "Package is `ops/c1_rail/qualification/`: this corrects the proposed lab placement because the accepted monorepo boundary prohibits lab importing ops." Its classes are the ones the [TB-S2 spec](../../spec/2026-09-12-tradeify-synchronized-replay-spec.md) interface table assigns to TB-I2. The first return held it unscored under §3.3. The operator then directed, in session 2026-09-22, verbatim: **"score the qualification replay too"**. That instruction is recorded here as the ruling that lifts the §3.3 hold, and 3′ is scored in §7.4.

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

| R5 | P6 probe on 3′ (source in §7.6), first attempt | **1 failed**: a probe defect. The direct `simulate_path` calls omitted `starting_equity`, so the kernel refused the mismatched `initial_state`. Not a producer result; fixed in R6. | `20260922T233732Z-88e61b835a52` · `d80b3801…cf1eb0c` |
| R6 | P6 probe on 3′, corrected | 1 passed; emitted series `[-20, 0, 0]`, SHA-256 (`<f8`) `175f9fbf0b8439fef904a669b6032ea4bfdaf47ac7f6fe70aa32868ac2fc3911` | `20260922T233749Z-fc506f3b0481` · `d5435a28…a13cadb` |
| R7 | P2 probe on 3′ (source in §7.6). The first attempt failed on a fixture that placed the add after the scheduled entry cutoff in both arms (`20260922T233817Z-cd530cc430b6`, not a producer result); this is the corrected run. | 1 passed. Control: ORB add filled (qty 1). After the 2% loss the session is PROTECTED and the add is rejected with `zero policy quantity`. | `20260922T233830Z-93d830992475` · `621662a1…e58713` |
| R8 | `python -m pytest -v` with the 11 named 3′ node ids cited in §7.4, plus `tests/ops/test_book_policy.py` | 45 passed | `20260922T233849Z-266a23691a44` · `01347666…fb3ef78a` |

Records sit under the ignored `.cache/fp-verification/` of the executing clone. R1–R4 were taken at `082366c` and R5–R8 at `4c1161c`, all with a clean tracked tree. The probe files live in the executor's scratch directory, outside the checkout; their sources are reproduced in §7.6.

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

The emulator's gap is not P5 alone; P1–P4 and P6 are also missing from it. The P1–P4 laws exist and are tested in `book_policy.py`. Composing them with the emulator on one clock is exactly what candidate 3′ does.

**Candidate 3: TB-I2 at its specified footprint.** **ABSENT.** `ls lab/analysis/c1/tradeify_book_replay_2026-09/` → "No such file or directory". No `lab/` file references the path.

**Candidate 3′ (found under §3.4, scored on the operator's instruction): `ops/c1_rail/qualification/`, TB-I2 relocated.**

| # | Score | Evidence |
|---|---|---|
| P1 | MET | `replay.py:357–365` sizes every admitted entry through `book_policy.entry_quantities` and every add through `add_quantity(confirmed base)`, never through uniform scaling. The production provider `production_source.py:70–89` supplies Striker's unrounded risk (Account Size × risk %, and stop distance × point value). Tests (R8): `test_production_source.py::test_sizing_uses_unrounded_risk_stop_and_explicit_frozen_lifecycle_cap`, `::test_striker_exact_risk_boundary_is_not_rounded_up_through_float`; `test_replay.py::test_striker_rounded_normal_quantity_is_not_risk_input`, `::test_c80_protected_striker_rounds_unscaled_risk_only_after_protection`; `test_book_policy.py::test_protected_and_lifecycle_integer_table`. |
| P2 | MET | Keyed on protection state: the mode comes from the prior settled close (`replay.py:467`); `add_quantity(mode=…)` returns 0 for ORB and Vanguard when PROTECTED (`book_policy.py:273–275`), and the replay then rejects the add (`replay.py:366–368`); mode transitions deliver the adapters' cancels (`:470–480`). The ORB base stays 1 (`book_policy.py:311–313`). R7 shows it on the replay with a control. Also R8: `test_mode_changes_from_prior_settled_path_close_only`, `test_book_policy.py::test_transition_cancels_only_resting_orb_adds_on_activation`. |
| P3 | MET | `CapacityLedger.request` (refuse, never clip) at `replay.py:372`; 6J = 10 micro-equivalents, cap 80. R8: `test_barrier_aegis_capacity_precedes_other_legs_and_rejects_without_clip` hits the cap: Aegis fills 8 (= 80 micro-equivalents) and the other three legs are rejected. |
| P4 | MET | Takeover at `replay.py:373–399`: cancel displaced pending orders, acknowledge, close the whole leg, confirm flat, then settle and admit; admission runs in priority order (`:534`). R8: `test_aegis_whole_leg_takeover_closes_striker_before_entry`, `test_protected_striker_77_displaced_by_protected_aegis_30`, `test_partial_takeover_close_refuses_aegis_and_preserves_remaining_truth`. |
| P5 | MET | One event loop over path bars for all four legs (`replay.py:489–559`), with one shared `self.cash` and a marked account equity per bar (`:556`). The protection clock settles on account cash (`:570`). R8: `test_crossleg_adverse_marks_sum_without_favorable_netting`. |
| P6 | MET | R6: the replay's `SessionRecord.intraday_low` series (`model.py:161` rejects values `> 0`) goes through `sessions.session_arrays` → `runner.evaluate_replay` → `simulate_path(dd_scale=1.0)` and is accepted. Absolute lows are refused (`<= 0` error) and a short series is refused (horizon error). **Hand recompute** of session 0 from the fixture bars: ORB and Vanguard each fill 1 contract at the bar-1 close of 100, so the close-only entry contributes 0 on that bar (RC-6 (c)). Bar 2 is (100, 110, 90, 100), with the long adverse mark at the low: 1 × (90 − 100) × point value 1 = −10 per leg, summed without netting = **−20**, equal to the emitted value. R8 also covers `test_runner.py::test_kernel_uses_intraday_and_no_second_scaling`. |
| P7 | **NOT MET** (public record) | (a) **Private, UNKNOWN from this session:** the four ports at runtime SHA-256 `book_adapters.py:39–62`, effective inputs `:72`, and the four M15 panels pinned in `core/data/bar_data/SHA256SUMS`, none present here. (b) **Reviewed retained artifacts the production path requires before any real replay** (`production_source.py:776–784`, fail-closed): `source_startup_policy`, `source_calendar` (+ review), `population_index` (+ review), `schedule_execution_evidence` (+ review), `cost_model`. The producer itself declares three of these capabilities missing (`PRODUCER_GAPS`, `production_source.py:38–45`: `SOURCE_CALENDAR_CAPABILITY_MISSING`, `SCHEDULE_INTRABAR_CAPABILITY_MISSING`, `STARTUP_POLICY_BINDING_MISSING`). (c) The [schedule-execution-evidence note](../phase3-preparation/2026-09-15/schedule-execution-evidence.md) (2026-09-15) states that real, outcome-bearing paths "remain blocked until provenance and any required model amendment are accepted". It names the only routes as "a newly ratified interpolation/model convention or finer historical execution evidence", and says "No feed purchase is authorized". No later public record of that evidence was found. S3's accepted N1 capture ran on synthetic sources (`composition_fixture`; S3 packet line 47). A private artifact could overturn (a) or (b); (c) is a recorded blocker. |

**What 3′ reproduces, per expression of the selected four** (the D-T00 wording asks for this; laws from `book_policy.py:179–197`, `:279–316`, with integer outcomes pinned by `test_protected_and_lifecycle_integer_table`):

| Expression | Integer sizing | ORB base/add | Capacity | Takeover |
|---|---|---|---|---|
| Aegis 6J (short, priority 1) | Fixed 8. PROTECTED gives floor(8 × 0.40) = 3. | n/a (no adds) | 10 micro-equivalents per contract (8 = 80) | The only leg that may displace others |
| Striker MYM p250 (priority 2) | min(floor(risk × scale / per-contract risk), floor(cap alloc / 3.5)). The scale is applied to unrounded risk before the floor. | Add floor(250%) of the confirmed base, max 1; not refused when protected | 1 per contract | Displaceable as a whole leg (the protected 77 case is tested) |
| Vanguard MGC (priority 3) | Captured base 1 or 2. PROTECTED gives floor(base × 0.40) = 0, so the leg is off under protection (the accepted D-B10 consequence). | Adds round(80%), max 2; off when protected | 1 per contract | Displaceable |
| ORB MNQ v7 (priority 4) | Base 1 in both modes | Adds round(100%), max 2, sized from the confirmed base; **0 when protected**, with resting adds cancelled on activation | 1 per contract | Displaceable, lowest priority first |

**Concerns carried with the P1–P6 scores.** They are shown with the real replay, policy, emulator and kernel code, but with **synthetic adapters** (`test_replay.py:17–31`) and synthetic bars. The strategies' own signal logic lives in the private ports and was not exercised; that is part of P7 and of the TB-A parity owed at protected and adds-off sizes. The module's own scope line reads "no loading or qualification authority" (`replay.py:1`).

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

**INSUFFICIENT.** No candidate has P1–P7 all MET; this follows mechanically from §7.4. The closest is candidate 3′, which meets **P1–P6** and fails only **P7**.

**Smallest missing set: candidate 3′ + its P7 inputs.** No producer code is identified as missing. What's missing, in order of lead time:
1. **Source-instant schedule execution evidence**, or a ratified convention replacing it: the recorded blocker. It needs either finer-than-M15 historical data (no feed purchase is authorized; Databento is retired with no approved replacement, per AGENTS.md "Data source disposition") or an operator-ratified interpolation/model amendment. This is a decision or acquisition, not agent work, so no token estimate is given for it.
2. **The reviewed source calendar, population index, startup policy and cost model** as retained, reviewed bytes. [T10](2026-09-21-tradeify-t10-source-and-freeze-packet.md) (source and freeze packet) is the packet on record for source/calendar acceptance.
3. **Private inputs verified against their public pins**: the four ports, effective inputs and the four M15 panels. Also TB-A adapter parity at protected and adds-off sizes; the [Stage-2 plan](../../superpowers/plans/2026-09-14-stage2-runtime-integration.md) line 21 records exports "collection 7/7, acceptance 0/7" as of #382, not re-verified here.

**Build estimate (an estimate, not a measurement):** once items 1–3 exist, scoring P7 and running P6's hand recompute on one real bar-level day is **one executor session on the operator's primary checkout, about 100k–250k tokens**, under whatever authority the attempt controller requires. The TB-S2 emulator route (candidate 2) is no longer the cheaper path. Rebuilding its synchronization would duplicate 3′, roughly 1.2k lines of engine and 1k lines of tests (sized by 3′ itself), and it would still need items 1–3.

**Owed to the coordinator:**
1. Acceptance of this return. The §3.3 hold was lifted by the operator's instruction rather than a coordinator ruling.
2. *Resolved on operator instruction ("fix the three stale statements too", 2026-09-22):* the D-T00 grounds carry a dated correction note (prior sentence preserved); the amendment §5 audit hook now distinguishes TB-I2's absent `lab/` footprint from the relocated `ops/c1_rail/qualification/` replay; and the handoffs README lists T00 as returned. This packet's header **Status** line, flagged as stale in an earlier revision of this item, was updated on `main` by #458 to "DISPATCHED 2026-09-22 … its return lands in §7" and arrived here by merge; it no longer contradicts this return.

### 7.6 Probe sources (synthetic; no screen, no MC)

**R4, the P6 probe on candidate 4a:**

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

**R6, the P6 probe on candidate 3′** (imports the fixtures of `tests/ops/qualification/test_replay.py`):

```python
"""T00 step-1 P6 probe for candidate 3' (synthetic fixtures only; no screen, no MC population)."""
import hashlib, sys
sys.path[:0] = ["tests/ops/qualification", "ops", "core"]
import numpy as np
import pytest
from test_replay import engine, path_session, first_entry
from c1_rail.qualification.sessions import session_arrays
from c1_rail.qualification.runner import evaluate_replay
from mc.simulation import EvaluationState, simulate_path


def test_p6_qualification_emitted_series():
    # Three contiguous path sessions; ORB and Vanguard enter once (bar close) in session 0.
    replay, _ = engine({"orb_mnq_v7": first_entry, "vanguard_mgc": first_entry})
    result = replay.run((path_session(0), path_session(1), path_session(2)))
    pnl, low = session_arrays(result.sessions)
    print("emitted intraday_low:", low.tolist(), "pnl:", pnl.ravel().tolist())
    # Hand recompute, session 0 from the fixture bars: entry fill at bar-1 close 100
    # (close-only lifetime -> 0 on the entry bar); bar 2 = (100, 110, 90, 100), long adverse at the
    # low: ORB 1 x (90-100) x pv 1 = -10; Vanguard 1 x (90-100) x pv 1 = -10; summed, no netting = -20.
    assert low[0] == -20.0 and low[1] == 0.0 and low[2] == 0.0
    state = EvaluationState(100000, 100000, 100000, 0, 0)
    # (a) the producer's own consumer path: session_arrays -> evaluate_replay -> simulate_path
    print("evaluate_replay ->", evaluate_replay(result, initial_state=state))
    # (b) the kernel's validation directly, dd_scale=1.0 as the runner passes it
    print("simulate_path ->", simulate_path(pnl, 0.01, 1.0, len(low), intraday_low=low, initial_state=state, starting_equity=100000.0))
    with pytest.raises(ValueError, match="<= 0.0"):
        simulate_path(pnl, 0.01, 1.0, len(low), intraday_low=100000.0 + low, initial_state=state, starting_equity=100000.0)
    with pytest.raises(ValueError, match="cover the horizon"):
        simulate_path(pnl, 0.01, 1.0, len(low), intraday_low=low[:-1], initial_state=state, starting_equity=100000.0)
    print("emitted_sha256:", hashlib.sha256(np.asarray(low, dtype="<f8").tobytes()).hexdigest())
```

**R7, the P2 probe on candidate 3′:**

```python
"""T00 step-1 P2 probe for candidate 3': ORB adds off while protected, on the replay (synthetic)."""
import sys
sys.path[:0] = ["tests/ops/qualification", "ops", "core"]
from test_replay import engine, path_session, entry
from c1_signal_daemon.book_protocol import OrderIntent, Side, FillTiming
from c1_rail.qualification.replay import Instrument
from c1_rail.book_policy import BOOK_LEGS


def run(loss):
    # Session 0: ORB base entry, then (loss=True) a 20-point drop at pv 100 -> -2000 = 2% of 100k.
    # Session 1: ORB base entry on its first bar, add on its second bar.
    def emit(a, b):
        n = len(a.bars)
        if n in (1, 4):
            return entry(a, b)
        if n == 5:
            return [OrderIntent("add1", a.leg_id, "add", Side.BUY, 1, timing=FillTiming.THIS_CLOSE, bar_time=b.ts)]
        return []
    inst = {s.leg_id: Instrument(1, 100, 0, 0) for s in BOOK_LEGS}
    p0 = [(100, 100, 100, 100), (100, 100, 80, 80)] if loss else [(100, 100, 100, 100), (100, 100, 100, 100)]
    last = p0[-1][-1]
    p1 = [(last,) * 4] * 4
    replay, adapters = engine({"orb_mnq_v7": emit}, instruments=inst, quotes=lambda *args: last)
    result = replay.run((path_session(0, prices=p0), path_session(1, prices=p1)))
    fb = adapters["orb_mnq_v7"].feedback
    adds = [e.fill.qty for e in fb if e.fill and e.fill.kind == "add"]
    rejects = [e.detail for e in fb if e.event == "reject"]
    return [m.value for m in adapters["orb_mnq_v7"].modes], adds, rejects, [r.pnl for r in result.sessions]


def test_p2_orb_add_refused_only_when_protected():
    normal = run(loss=False)
    protected = run(loss=True)
    print("control (no loss):", normal)
    print("after 2% loss   :", protected)
    assert normal[0] == ["normal", "normal"] and normal[1] == [1] and not normal[2]
    assert protected[0] == ["normal", "protected"] and protected[1] == [] and "zero policy quantity" in protected[2]
```

### 7.7 Condition 4, restated for the operator

**Is T00's screen §4 falsifier evidence for the 2026-11-08 trigger?** If yes, its ceiling, tiers and dating follow the four-firm ADR §4 as frozen. If no, the falsifier needs its own dated re-MC before 2026-11-08, regardless of T00. Step 1 does not bear on this ruling. No step-2 recommendation is made: the table supports none until candidate 3′ meets P7 with real inputs.

Not done, as scoped: no producer was built or patched; no screen, MC or re-MC was run; no pre-registration was drafted; no private artifact, account figure or Pine was committed; the seven-entry menu was not scored.

### 7.8 Operator rulings on the return (2026-09-23)

Recorded after the return merged ([#460](https://github.com/Joshua-Asante/first-passage/pull/460)); §7.1–§7.7 above are unchanged.

| Item | Ruling (operator, in session, verbatim) | Consequence |
|---|---|---|
| Acceptance | "I accept the T00 return" | The return is accepted as filed: verdict INSUFFICIENT, missing set = candidate 3′ plus its P7 inputs (§7.5). |
| Condition 4 | "A T00 screen does not count as falsifier evidence" | **No.** The four-firm §4 falsifier dated 2026-11-08 needs its own dated re-MC regardless of T00, per the ratified D-T00 wording. T00 no longer bears on that clock. |
| Timing convention | "I want to ratify a timing convention to unblock the replay" | Intent only; **no convention is ratified by this record.** A convention would replace one P7 blocker, source-instant schedule evidence (§7.5 item 1). The other P7 items stand (§7.4, candidate 3′ row P7 (a) and (b)). |

**Candidate 1, archive search (2026-09-23).** The operator granted access to `first-passage-archive`. Both of its relevant refs were searched:
- the default branch (`73971f1`, last commit 2026-08-15, before the campaign opened on 2026-09-03);
- `archive/preserve-2026-09-06` (`5d47b4d`, 1,542 files removed from this repo at `2d40dbeb`).

Neither holds the joint replay, the 125-test synthetic replay, canonical ledgers, private overrides or the `account-feedback-composition-2026-09-08` packet. The one public digest for that packet, the approval receipt `bad72266716a31782960c49deed0e25c8c2dc8256300cd8bbc2423d7778d73aa` (campaign record §53), appears on neither ref. No other archive branch name dates from September 2026. This is consistent with M-41: the evidence lived in gitignored `.worktrees/*`, which git never carried. Candidate 1 remains **UNKNOWN — operator input owed** for local backups and `local_artifacts/` only; the archive route is closed. The verdict is unchanged either way, because a surviving copy would still need scoring against P1–P7 for the selected four.

**Candidate 1, local search (2026-09-23).** The [local-search return](2026-09-23-seven-strategy-evidence-local-search.md#7--executor-return) found **no copy of the evidence** (approval receipt, ledgers, override maps, reconciliations, strategy reports, joint replay, 125-test suite) in any reachable root. The verdict is INCOMPLETE because shadow copies and some Codex-sandbox dirs were unreachable. All 7 export/Pine input pairs survive locally, digest-matched. The operator ruled on 2026-09-23 ("accept the recommended reading and merge 474"): the evidence verdict is **INCOMPLETE**, and the surviving inputs neither falsify H nor reopen candidate 1. Candidate 1 stays **UNKNOWN**. It closes as **UNREACHABLE** once the shadow-copy listing comes back empty and the Codex-sandbox root is closed (that return's §7.6). The T00 verdict is unchanged.


**Candidate 3′ P7 (a), primary-checkout hash check (2026-09-24).** After the operator's build GO for the bracket convention ([schedule-evidence addendum](../phase3-preparation/2026-09-15/schedule-execution-evidence.md#addendum-2026-09-23--path-position-bracket-convention-ratified-2026-09-23)), the private inputs on the primary checkout (`main` checkout, read-only) were hashed against their public pins:
- **Ports: MATCH, but only in the Step 3 root.** All four runtime pins (`book_adapters.py:39–62`) and `EFFECTIVE_INPUTS_SHA256` match the files in `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/inputs/private_overrides/op1/2026-09-14-seven/step3-coverage/corrected-ports/`. The default port root `ops/c1_signal_daemon/ports/` holds the preserved Striker original (`c81aa59c…`), which the loader must refuse, so a real-bar run needs `FP_PORT_ROOT` set to the corrected-ports directory.
- **Panels: MATCH.** The four panels that the Step 3 admission binds (MNQ `cceaac41…`, MYM `15b34615…`, MGC `c5487470…` per `core/data/bar_data/SHA256SUMS`; Aegis attested-prefix `8ae083d0…` per [identity ledger](../phase3-preparation/2026-09-15/identity-ledger.md) line 165) match on disk. All six `SHA256SUMS` rows pass.

P7 (a) is **MET** on the primary checkout. P7 (b), the reviewed source calendar, population index, startup policy and cost model, stays **NOT MET**: none exists. T10's phase-1 return (branch `claude/t10-source-freeze`, not merged) lists the panel-derived session-index producer run as phase 2 / step 4 work, and phase 2 has not started. The verdict stays **INSUFFICIENT** until P7 (b) is met.
