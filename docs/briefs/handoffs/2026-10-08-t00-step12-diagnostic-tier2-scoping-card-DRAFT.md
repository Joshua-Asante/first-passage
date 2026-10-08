# CC handoff — T00 step-12 diagnostic, Tier 2: per-leg attribution (scoping)

**Date:** 2026-10-08.
**Status:** `DRAFT — SCOPING, NOT ADMITTED`. Nothing in this card runs, builds or signs anything.
**Authority:** Joshua, 2026-10-08, to the Deployment Coordinator: "scope tier 2". That authorizes this scoping card only.
**Brief type:** CC handoff, scoping draft (diagnostic, non-decision-bearing).
**Parent:** [Tier-1 card](2026-10-08-t00-step12-diagnostic-tier1-card.md) §2 and "Why two tiers"; [T00 screen authority build card](2026-10-03-t00-screen-authority-build-card-DRAFT.md) §3.5 and §8.
**Subject:** the step-12 result `NO-GO-evidence-robust`, `VERIFIED` (#724; results `a5b985d0…42dc`, H `5d25f9c`).

## §0 — Production reads

Read at `origin/main` `93118ff` on 2026-10-08. Re-read at admission.

| Surface | Fact |
|---|---|
| `ops/c1_rail/qualification/replay.py:621-624` | Bar equity is `cash` plus every leg's `open_pnl`. Only the combined value is kept. |
| `replay.py:635-639`; `model.py:148-157` | `SessionRecord` holds combined `pnl` and `intraday_low` only. No per-leg field. |
| `replay.py:164-166`, `:520` | `_log` appends to `self.events`. `session_mode` is logged once per session. |
| `replay.py:213-219`, `:374`, `:438-446` | Fill events (with `commission`), `refused`, and `capacity_takeover_*` events carry the leg id. |
| `replay.py:408-451` | The port's intent quantity is replaced by `entry_quantities` / `add_quantity` (override at `:451`). The pre-override quantity is not logged. |
| `production_source.py:926-936` | `_seal` hashes the event stream into `events_sha256` and returns sessions without events. |
| `production_source.py:1232-1254` | `replay_bracket` returns `SourceOnlyBracket` for a source-only contract. No event stream escapes. |
| `t00_screen/worker.py:169-182` | `run_projection`: `digest` = hash of session rows plus `events_sha256`. |
| `t00_screen/journal.py:108-113`, `:124-130` | PATH run fields are fixed; no P&L series. |
| `runner.py:18-44` | `evaluate_replay` returns no bust session for a failure. Tier 1 derives a descriptive floor crossing from sealed `pnl` / `intraday_low`. |
| `contract.py:963-968`, `:1086-1088` | Source contract purpose `T00_P7_SOURCE_VERIFICATION`, evidence class `T00_P7_SOURCE_ONLY`. Purpose and refusals (incl. `SCREEN`, `MONTE_CARLO`, `DECISION_RULES`) must be exact. |
| `screen_authority.py:47-50`, `:181-184` | The screen authority's purpose, refusals and evidence class are also exact constants. |
| `tests/ops/qualification/test_source_consumers.py:40-43`, `:84-86` | The A10b scan lists `replay_bracket` consumers; the Tier-1 driver is allowlisted. |
| [Deployment checklist](../../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md) item 7.6.1, `:634-638` | No agent runs a candidate-configurable replay before its pre-registration is frozen. |

## §0.5 — Prerequisites before admission (otherwise BLOCKED)

1. The Tier-1 return is delivered and accepted. It may refine §2.
2. Joshua admits Tier 2 and picks the OWED fields (§8).
3. The capability PR (§3) is merged after Codex review, and Joshua accepts a new H.
4. P7 is re-run at the new H under a fresh operator-signed source approval.
5. A diagnostic evidence class and receipt purpose exist and are signed (§3.4).

## §1 — Purpose, non-goals and no back door

**Purpose.** Attribute the trailing-drawdown busts to legs and mechanisms, descriptively.

**Non-goals.**
- It selects nothing: no leg, size, input or book.
- No back door to the T00 verdict or #581. No output re-opens `NO-GO-evidence-robust`.
- Not qualification evidence. Not four-firm §4 evidence.
- Selected cases cannot estimate rates (§4).

**Why it is outside checklist 7.6.1.** It replays the book as declared: the r3c-equivalent contract, accepted ports, pinned effective inputs, no overrides. Nothing is candidate-configurable, so it is not a candidate replay.

**Counterfactuals are out of scope.** Leg off, rescale, adds off or any input change is a candidate replay. Each needs its own frozen pre-registration and a separate screen.

## §2 — Pre-stated questions

All quantities are per run (R1, R2), per path, from the sidecar (§3). "Busting run" = a run whose retained `kernel_outcome` is `bust_trailing`. "Breach session" = the first session whose descriptive floor crossing occurs (Tier-1 rule). "Peak-to-breach" = from the running equity peak before the breach to the breach session's intraday low.

| # | Question | Derived quantity |
|---|---|---|
| Q1 | Which legs carry the drawdown? | Per leg: realized P&L plus open-P&L change over peak-to-breach, ÷ total peak-to-breach drawdown. Same share on the breach session alone (realized plus intraday-low mark). |
| Q2 | Was protection on? | `session_mode` at breach and per session in the run-up. Count of add fills while `session_mode` is protected. |
| Q3 | Do sizes match intent? | Per leg, base and add: port-requested qty, policy qty, admitted qty, filled qty. Share of entries where the size cap binds (policy qty < uncapped law qty). |
| Q4 | Does capacity crowd legs out? | Per leg: capacity refusals, takeovers as winner and as displaced. Share of a leg's refused entries caused by another leg's fixed size. |
| Q5 | What do forced closes cost? | Count and P&L of scheduled flattens, takeover closes and deadline closes, per leg. Commissions per leg over peak-to-breach. |
| Q6 | Is attribution ordering-sensitive? | Q1 shares under R1 vs R2 at the breach session. Consumed intrabar splits on that session, per leg. |
| Q7 | Do halves differ? | Q1–Q4 contrasted between H1 and H2. |

**Patterns and the successor direction each points to.** These are pointers for a later pre-registration, not decisions.

| Pattern | Points to |
|---|---|
| Q1 share concentrated in the risk-sized index leg, single-session shocks, Q3 cap often binding | Per-leg size reduction of that leg, with its reserve cap cut together |
| Q2 shows adds filling in protected mode on busting runs, and add fills carry a large Q1 share | Turning adds off (in protected mode or always) |
| Q1 share concentrated in one leg across halves, or Q4 shows that leg's fixed size displacing others | Dropping or reshaping that leg |
| Q7 shows the Q1 pattern only in one half | Regime dependence; a regime question, not a sizing one |
| Shares spread across legs, grind not shock, no Q2–Q5 signal, or Q6 flips the leading leg | No evidence-supported successor |

## §3 — Capability (build)

### §3.1 Options

- **(i) Sidecar (recommended).** `BookReplay` accumulates, per session and per leg: realized P&L, open-P&L mark at close, intraday low of the leg's equity, `session_mode`, requested / policy / admitted / filled quantities, capacity and forced-close events, commissions. It is held outside `self.events`, `SessionRecord` and `ReplayResult`. It enters no digest.
- **(ii) Private raw event stream.** Return the full event list plus new per-leg mark events.

**Why (i).** The sealed boundary (`_seal`, `replay_bracket`) stays intact. New mark events in `self.events` would change `events_sha256`; a separate stream avoids that but still exports far more than §2 needs. (i) emits exactly the §2 inputs and nothing else.

### §3.2 Where the code goes

- `replay.py`: an opt-in accumulator on `BookReplay`, off by default. It writes nothing to `self.events` and adds no field to `SessionRecord`.
- `production_source.py`: a new gated method beside `replay_bracket` that returns the `SourceOnlyBracket` plus the per-run sidecar, only under the diagnostic evidence class.
- `test_source_consumers.py`: an A10b allowlist entry for the new method's single consumer.
- A Tier-2 driver script under `scripts/`, built like the Tier-1 driver (pinned hash, clean detached H, create-once writes, budget stops).

### §3.3 Acceptance

- Identity: re-running step-12 keys with the sidecar on gives byte-identical `digest`, `events_sha256`, `results.json` and verdict. Scope of "step-12 keys" is OWED (§8 item 4).
- Red/green tests: the sidecar off vs on gives equal sealed output; the sidecar is absent under any other evidence class; per-leg sums reconcile to combined `pnl` and to fill events.

### §3.4 Governance chain

1. Code PR, Codex review, coordinator acceptance.
2. New H, accepted by Joshua.
3. P7 re-run at the new H.
4. A fresh operator-signed source approval. The current r3c approval `2cc7195e…` expires 2026-10-14T02:08Z, so Tier 2 almost certainly needs a new one.
5. A diagnostic evidence class and receipt purpose.

**Contract fit.** `contract.py:1086-1088` requires the source contract's purpose and refusals to be exact. A diagnostic class therefore needs a code change: new constants (purpose, evidence class, scope) with the same refusals (`SCREEN`, `MONTE_CARLO`, `DECISION_RULES`, `QUALIFICATION_STAGES`, `SEAL`, `ADMISSION`, `DEPLOYMENT`, `BUDGET`). It fits those refusals as Tier 1 did: no verdict or tally, fixed previously drawn keys, no rate, no rule evaluated. Reusing `T00_P7_SOURCE_VERIFICATION` is weaker, because per-leg attribution is not source verification in kind.

### §3.5 Effort

About 2–3 agent-days for build, tests and one or two review rounds. The governance chain (§3.4) adds operator signing time and the P7 re-run.

## §4 — Sample, hypothesis and falsifier

**Sample options (OWED, operator).**
- (a) The frozen Tier-1 keys (`keys.json` `60c128a7…329e`).
- (b) A larger set, frozen before any replay, stratified like Tier 1 and weighted to agreed `FAILURE` and `UNDETERMINED` in H2.

Selected cases cannot estimate rates or prove a change helps. Say so in the report.

**Size: OWED (operator).** Cost ≈ paths × ~150 CPU-s (Tier-1 card §7 estimate) + ~3 min build, plus sidecar overhead measured at acceptance. Option (a): about 50 min. Option (b): about 2.5 CPU-h per 60 paths. Tier-1 actual per-path cost: OWED, filled from its return.

**H (non-interference):** with the sidecar on, each replayed path reproduces its retained sealed identities byte for byte.

**Falsifier:** any identity mismatch. The run stops there; no attribution is reported from a non-reproducing run.

§2's answers are descriptive and conditional on H. They are not gates.

## §5 — Forbidden moves

- Any counterfactual: leg off, rescale, adds off, input override, alternative book.
- Any change to the book, ports, parameters or protection.
- Sampling new paths, resampling, estimating rates, evaluating thresholds.
- Using any output against the T00 verdict, #581 or four-firm §4.
- Writing to the step-12 run directory.
- Any private value (counts, rates, P&L, keys, timings, port bodies, effective-input values) in a public surface. Pine is not read.
- GLM or any external service.

## §6 — Return and status

**Public return** (to the Deployment Coordinator): key-list SHA-256, driver SHA-256, sidecar-schema SHA-256, the H verdict, status, report SHA-256. No counts, values, timings or keys.
**Private report:** under the private root, outside every worktree. It answers Q1–Q7 and names one §2 pattern or none.

**Verdict on H:** RESOLVED (every selected path matched and the report is delivered); FALSIFIED (any identity mismatch or non-gate replay exception); AMBIGUOUS (any other stop before every path is replayed).

**Status (exactly one):**
- **DONE:** H holds and the report is delivered.
- **DONE_WITH_CONCERNS:** DONE plus a named concern. A mismatch is never this.
- **NEEDS_CONTEXT:** a missing fact or ruling. Name it.
- **BLOCKED:** a §0.5 prerequisite fails, H is falsified (integrity incident to Joshua), a refusal, a driver defect or a budget stop.

## §7 — Seats and dependencies

- **Scoping:** proceeds now (this card).
- **Admission:** waits for the Tier-1 return, now in flight.
- **Executor:** TBD at admission.
- **Acceptor:** the Deployment Coordinator.
- **Decisions:** Joshua keeps admission, sample, signing and every investment decision.
- **Exposure:** readers of Tier-2 output join the Tier-1 reader log. Any successor pre-registration names them (design §4.5). Tier-2 output is exposure for that pre-registration.

## §8 — OWED (operator)

1. Admit Tier 2 (after the Tier-1 return).
2. Capability option: (i) recommended.
3. Sample option and size (§4).
4. Acceptance scope: the full step-12 re-run (about 8.4 h wall at W = 8, per build card §8, and it needs screen authority), or identity on the sampled keys plus the sidecar-off/on tests.
5. Diagnostic purpose and evidence-class names; a new source approval.
6. Executor seat.
7. Tier-1 actual per-path cost (from its return).

## §10 — Audit hooks

```bash
# Card form (expect RESULT: well-formed).
python -I scripts/fp.py python scripts/check_brief.py --type handoff docs/briefs/handoffs/2026-10-08-t00-step12-diagnostic-tier2-scoping-card-DRAFT.md

# Combined-only session record and bar equity.
sed -n '621,624p;635,639p' ops/c1_rail/qualification/replay.py
sed -n '148,157p' ops/c1_rail/qualification/model.py

# Sealed boundary.
sed -n '926,936p;1232,1254p' ops/c1_rail/qualification/production_source.py

# Exact purpose and refusals.
sed -n '963,968p;1086,1088p' ops/c1_rail/qualification/contract.py

# No private value in this card (expect no output).
rg -n "P&L =|\\$[0-9]{2,}|account [0-9]" docs/briefs/handoffs/2026-10-08-t00-step12-diagnostic-tier2-scoping-card-DRAFT.md | grep -v 'rg -n'
```
