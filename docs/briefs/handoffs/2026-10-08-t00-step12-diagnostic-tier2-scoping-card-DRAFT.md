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
| `replay.py:635-639`; `model.py:148-157` | `SessionRecord` holds combined `pnl` and `intraday_low` only. No per-leg field and no intraday high. |
| `replay.py:180-182` | A fill's commission is taken from `cash`, so realized P&L reconciles only net of commission. |
| `replay.py:164-166`, `:520` | `_log` appends to `self.events`. `session_mode` is logged once per session. |
| `replay.py:213-219`, `:374`, `:438-446` | Fill events (with `commission`), `refused`, and `capacity_takeover_*` events carry the leg id. |
| `replay.py:408-451` | The port's intent quantity is replaced by `entry_quantities` / `add_quantity` (override at `:451`). The pre-override quantity is not logged. |
| `ops/c1_rail/book_policy.py:279-310` | `entry_quantities`: only the risk-sized leg has a size cap; the other legs are fixed-size. |
| `production_source.py:926-936` | `_seal` hashes the event stream into `events_sha256` and returns sessions without events. |
| `production_source.py:1232-1254` | `replay_bracket` returns `SourceOnlyBracket` for a source-only contract. No event stream escapes. |
| `production_source.py:61-63`, `:1201`, `:1252` | `_is_source_only` is `type(contract) is ValidatedSourceContract`. It decides sealing (`:1252`) and the `verify_for` refusal (`:1201`). |
| `t00_screen/worker.py:169-182` | `run_projection`: `digest` = hash of session rows plus `events_sha256`. |
| `t00_screen/journal.py:108-113`, `:124-130` | PATH run fields are fixed; no P&L series. |
| `runner.py:18-44` | `evaluate_replay` returns no bust session for a failure. Tier 1 derives a descriptive floor crossing from sealed `pnl` / `intraday_low`. |
| `contract.py:963-968`, `:1086-1088`, `:1189` | Source contract scope `APPROVE_T00_SOURCE_CONTRACT`, purpose `T00_P7_SOURCE_VERIFICATION`, evidence class `T00_P7_SOURCE_ONLY`. Purpose and refusals (incl. `SCREEN`, `MONTE_CARLO`, `DECISION_RULES`) must be exact; the approval scope is checked against `SOURCE_SCOPE` (`:1189`). |
| `screen_authority.py:47-56`, `:181-184`, `:854-857`, `:874-877` | The screen authority's purpose, refusals and evidence class are exact constants. Its grant is `T00_STEP3_SCREEN_ONCE`; a re-attempt appends a successor pre-registration. Two checks require `_is_source_only`. |
| `tests/ops/qualification/test_source_consumers.py:40-43`, `:84-86` | The A10b scan watches only `CAPABILITY_CALLS` (`replay`, `replay_bracket`, `proof`) and, outside `ops/`, only files in `EXTRA_SCANNED`. The Tier-1 driver is listed there. |
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

All quantities are per run (R1, R2), per path, from the sidecar (§3). Definitions:
- **Busting run:** retained `kernel_outcome` is `bust_trailing`, whatever the run's status or failure reason. Runs are classified by kernel outcome first.
- **Breach session:** the first session whose descriptive floor crossing occurs (Tier-1 rule).
- **Peak:** the highest end-of-session equity before the breach session, including the starting equity. Sessions carry no intraday high, so the peak is end-of-session only.
- **Breach bar:** the bar, or the settlement step after the last bar (`replay.py:634`), where the breach session's combined intraday low is set. Each run (R1, R2) uses its own breach bar.
- **Leg value:** cumulative realized P&L net of commission plus the open-P&L mark. Combined equity is cash plus every leg's open mark (`replay.py:621-622`), so leg values sum to the combined value at any bar.
- **Peak-to-breach drawdown:** combined value at the breach bar minus combined value at the peak close. A leg's share is its value change over the same span divided by that drawdown. Shares sum to one by construction.
- **Control runs:** runs whose retained status is not `FAILURE` (`PASS` or `UNRESOLVED`). They have no breach, so Q1 and Q6 use their deepest drawdown (deepest combined bar low against the prior end-of-session peak), measured up to the pass day for `PASS` runs and over the full horizon for `UNRESOLVED` runs. A control run with no drawdown is excluded from share statistics and counted. The **control is usable** when at least one control run has a drawdown. A leg's bust share means something only against its share in these drawdowns.
- **Other failures:** a `FAILURE` run whose kernel outcome is not `bust_trailing` (`runner.py:36-43`: daily, static, inactivity, own-flat deadline) is neither busting nor control. It is reported separately and never pooled.
- **Primary share:** a leg's share of the peak-to-breach drawdown. The breach-session share is secondary and used only by the shock rule.
- **Leading leg:** the leg with the largest primary share in a run.
- **Shock vs grind:** a busting run's breach-session fraction is the drawdown from the previous close to the breach bar, divided by the whole peak-to-breach drawdown. A run is a shock if that fraction is at least the §2.1 threshold, else grind. This sharpens the Tier-1 reading ([Tier-1 card](2026-10-08-t00-step12-diagnostic-tier1-card.md) §2), which is combined-only.

| # | Question | Derived quantity |
|---|---|---|
| Q1 | Which legs carry the drawdown? | Per leg: share of the peak-to-breach drawdown. Also the share over the breach session alone (previous close to breach bar). |
| Q2 | Was protection on? | `session_mode` at breach and per session in the run-up. Count of add fills while `session_mode` is protected. |
| Q3 | Do sizes match intent? | Per leg, base and add: port-requested qty, policy qty, admitted qty, filled qty. The policy qty is the value the production `entry_quantities` / `add_quantity` call returned, recorded, never re-implemented. For the risk-sized leg only: share of entries where its cap binds. N/A for fixed-size legs. |
| Q4 | Does capacity crowd legs out? | Per leg: capacity refusals, takeovers as winner and as displaced. Share of a leg's refused entries caused by another leg's fixed size. |
| Q5 | What do forced closes cost? | Count and P&L of scheduled flattens, takeover closes and deadline closes, per leg. Commissions per leg over peak-to-breach. |
| Q6 | Is attribution ordering-sensitive? | Q1 shares under R1 vs R2, each at its own breach bar. A path where only one run busts is reported as one-sided, not compared. Consumed intrabar splits on the breach session, per leg. |
| Q7 | Do halves differ? | Q1–Q4 contrasted between H1 and H2. Only under sample option (b) (§4). Under option (a) each half has at most two paths per class, so Q7 is not reported. |

**Patterns and the successor direction each points to.** These are pointers for a later pre-registration, not decisions.

**Shares are accounting, not cause.** A leg's share says where the loss was booked. It does not say what removing or shrinking the leg would do: the DD protection tier is book-wide, and capacity is shared, so changing one leg changes the others' sizes and the protection state. Every direction below is a hypothesis for a counterfactual screen, never a result.

### §2.1 Pattern criteria (frozen when this card merges)

The thresholds below and pattern rows 1–4 and 6 are blind because their text was fixed at `34c31c4` (2026-10-08 ~07:04Z), before anyone outside the Tier-1 executor read Tier-1 findings. They stay blind as long as that text is unchanged when the card merges, whoever has read Tier 1 by then. A later change to that text by a Tier-1 reader is a change made at admission (below). Tier 1 already reads shock versus grind on those keys, so option (a) is not fully blind; the report says so. Joshua may change a criterion at admission, after the Tier-1 report. A change made then is recorded as exposure, and the changed criterion is evaluated only on option (b) keys that exclude the Tier-1 keys.
- **Concentrated:** one leg's primary share is at least 0.5 in at least two-thirds of busting runs, and its median busting share exceeds its median control share by at least 0.25 (a difference, so a zero or negative control median does not break it). With no usable control run, Concentrated is not evaluable; rows 1, 4 and 5 do not hold, and row 3 holds only through crowding.
- **Busts are shocks:** at least two-thirds of busting runs are shocks, with a breach-session fraction of at least 0.5. **Busts are grind:** at least two-thirds are grind. Otherwise mixed.
- **Cap often binds:** the risk-sized leg's cap binds on at least a quarter of its entries in busting runs.
- **Protected adds matter:** add fills placed while protected carry at least a quarter of the peak-to-breach drawdown in at least a third of busting runs.
- **Crowding:** at least a quarter of a leg's refused entries in busting runs are caused by another leg's fixed size.
- **Ordering flips:** the leading leg under R1 differs from R2's on more than a third of the paths where both runs bust. It qualifies rows 1 and 3: a row that holds with ordering flips is reported as ordering-dependent.

| Pattern | Points to |
|---|---|
| The risk-sized index leg is concentrated, busts are shocks, and its cap often binds | Per-leg size reduction of that leg, with its reserve cap cut together |
| Protected adds matter | Turning adds off (in protected mode or always) |
| One leg is concentrated, or crowding holds for a leg's fixed size | Dropping or reshaping that leg |
| (Option (b) only) the concentration holds in one half and not the other | Regime dependence; a regime question, not a sizing one |
| (Option (b) keys excluding the Tier-1 keys only; added after Tier 1, see below) Busts are grind, no leg is concentrated, and the control is usable | Per-session risk reduction while the cushion is thin: a uniform or early-phase size cut across legs |
| None of rows 1–5 holds | No evidence-supported successor |

Rows 1–5 may hold together; the report names each, in table order. Row 6 holds only when none of them does. Mixed or shock busts with no leg concentrated fall to row 6 unless row 2 or 3 holds. When row 5 was not checked (option (a), or no option (b) keys outside the Tier-1 keys), the report says so next to any row 6 result.

**Row 5 provenance.** Joshua chose to add row 5 on 2026-10-08, after he and the Deployment Coordinator had read the Tier-1 findings (§7). It is an admission-time change under §2.1: it uses only the frozen thresholds above (grind, Concentrated, control), adds no threshold and changes none, is fixed now and never changed after Tier-2 data exist, and is evaluated only on option (b) keys that exclude the Tier-1 keys. Rows 1–4 and every §2.1 threshold are unchanged since `34c31c4`.

## §3 — Capability (build)

### §3.1 Options

- **(i) Sidecar (recommended).** `BookReplay` accumulates, per session and per leg: realized P&L net of commission and the open-P&L mark at the close and at the bar where the combined low is set, `session_mode`, requested / policy / admitted / filled quantities, capacity and forced-close events, commissions. It is held outside `self.events`, `SessionRecord` and `ReplayResult`. It enters no digest.
- **(ii) Private raw event stream.** Return the full event list plus new per-leg mark events.
- **(iii) Driver-side instrumentation at the current H (rejected).** It would avoid a new H and a P7 re-run. But the driver can reach `BookReplay` only through the capability calls (`replay_bracket`, `replay`, `proof`), and each seals its result under a source-only contract. The Tier-1 card forbids every other route (`screen_bracket`, `screen_epoch`, `_engine`, `_replay_raw`, and `replay` itself); the remaining option is patching code at run time. That bypasses exactly the boundary the capability review exists to control.

**Why (i).** The sealed boundary (`_seal`, `replay_bracket`) stays intact. New mark events in `self.events` would change `events_sha256`; a separate stream avoids that but still exports far more than §2 needs. (i) emits exactly the §2 inputs and nothing else.

### §3.2 Where the code goes

- `replay.py`: an opt-in accumulator on `BookReplay`, off by default. It writes nothing to `self.events` and adds no field to `SessionRecord`.
- `production_source.py`: a new gated method beside `replay_bracket` that returns the `SourceOnlyBracket` plus the per-run sidecar, only under the diagnostic evidence class.
- `test_source_consumers.py`: add the new method to `CAPABILITY_CALLS` and the Tier-2 driver to `EXTRA_SCANNED`, then allowlist its one owner. An allowlist entry alone is not gated, because the scan watches only listed calls and files.
- A Tier-2 driver script under `scripts/`, built like the Tier-1 driver (pinned hash, clean detached H, create-once writes, budget stops).

### §3.3 Acceptance

- Identity: each sampled run, replayed with the sidecar on, reproduces its retained PATH record byte for byte (`digest`, `events_sha256`, consumed-split count and SHA-256, `deadline_failure`), as Tier 1 does.
- **No full step-12 re-run.** It would compute a second verdict. The screen grant is once-only (`screen_authority.py:48`) and a re-attempt needs a successor pre-registration (`:55-56`), so it would be a back door to the T00 verdict.
- Red/green tests: the sidecar off vs on gives equal sealed output; the sidecar is absent under any other evidence class; per-leg sums reconcile to combined `pnl` and to fill events.

### §3.4 Governance chain

1. Code PR, Codex review, coordinator acceptance.
2. New H, accepted by Joshua.
3. P7 re-run at the new H.
4. A fresh operator-signed source approval. The current r3c approval `2cc7195e…` expires 2026-10-14T02:08Z, so Tier 2 almost certainly needs a new one.
5. A diagnostic evidence class and receipt purpose.

**Contract fit.** `contract.py:1086-1088` requires the source contract's purpose and refusals to be exact. A diagnostic class therefore needs a code change: new constants (purpose, evidence class, scope) with the same refusals (`SCREEN`, `MONTE_CARLO`, `DECISION_RULES`, `QUALIFICATION_STAGES`, `SEAL`, `ADMISSION`, `DEPLOYMENT`, `BUDGET`). It fits those refusals as Tier 1 did: no verdict or tally, fixed previously drawn keys, no rate, no rule evaluated. Reusing `T00_P7_SOURCE_VERIFICATION` is weaker, because per-leg attribution is not source verification in kind.

Two more code points must change with it:
- **Contract type.** `_is_source_only` checks the exact type `ValidatedSourceContract` (`production_source.py:61-63`). A diagnostic contract of a new type would get the raw, unsealed result (`:1252`), would not be refused by `verify_for` (`:1201`), and would change both screen-authority checks (`screen_authority.py:856`, `:876`). Either keep the diagnostic receipt a `ValidatedSourceContract`, or extend `_is_source_only` to the new type. Tests: the diagnostic contract gets sealed output, is refused by `verify_for`, and is refused by the screen authority.
- **Approval scope.** The scope is hard-coded (`contract.py:963`, checked at `:1189`). A diagnostic scope needs that check extended, with a test that each scope accepts only its own contract.

### §3.5 Effort

About 2–3 agent-days for build, tests and one or two review rounds. The governance chain (§3.4) adds operator signing time and the P7 re-run.

## §4 — Sample, hypothesis and falsifier

**Sample options (OWED, operator).**
- (a) The frozen Tier-1 keys (`keys.json` `60c128a7…329e`).
- (b) A larger set, frozen before any replay, stratified like Tier 1 and weighted to agreed `FAILURE` and `UNDETERMINED` in H2. When row 5 is to be read, or any criterion was changed at admission, the whole set excludes the Tier-1 keys, so every row is evaluated on the same keys.

Selected cases cannot estimate rates or prove a change helps. Say so in the report.

**Size: OWED (operator).** Cost ≈ paths × ~150 CPU-s (Tier-1 card §7 estimate) + ~3 min build, plus sidecar overhead measured at acceptance. Option (a): about 50 min. Option (b): about 2.5 CPU-h per 60 paths. Tier-1 actual per-path cost: OWED, filled from its return.

**Hypothesis N (non-interference):** with the sidecar on, each replayed path reproduces its retained sealed identities byte for byte. ("N" avoids a clash with H, the head commit.)

**Falsifier:** any identity mismatch. The run stops there; no attribution is reported from a non-reproducing run.

§2's answers are descriptive and conditional on N. They are not gates.

## §5 — Forbidden moves

- Any counterfactual: leg off, rescale, adds off, input override, alternative book.
- Any change to the book, ports, parameters or protection.
- Sampling new paths, resampling, estimating rates, evaluating thresholds.
- Using any output against the T00 verdict, #581 or four-firm §4.
- Writing to the step-12 run directory.
- Any private value (counts, rates, P&L, keys, timings, port bodies, effective-input values) in a public surface. Pine is not read.
- GLM or any external service.

## §6 — Return and status

**Public return** (to the Deployment Coordinator): key-list SHA-256, driver SHA-256, sidecar-schema SHA-256, the N verdict, status, report SHA-256. No counts, values, timings or keys.
**Private report:** under the private root, outside every worktree. It answers Q1–Q7 and names one §2 pattern or none.

**Verdict on N:** RESOLVED (every selected path matched and the report is delivered); FALSIFIED (any identity mismatch or non-gate replay exception); AMBIGUOUS (any other stop before every path is replayed).

**Status (exactly one):**
- **DONE:** N holds and the report is delivered.
- **DONE_WITH_CONCERNS:** DONE plus a named concern. A mismatch is never this.
- **NEEDS_CONTEXT:** a missing fact or ruling. Name it.
- **BLOCKED:** a §0.5 prerequisite fails, N is falsified (integrity incident to Joshua), a refusal, a driver defect or a budget stop.

## §7 — Seats and dependencies

- **Scoping:** proceeds now (this card).
- **Admission:** waits for the Tier-1 return, now in flight.
- **Executor:** TBD at admission.
- **Acceptor:** the Deployment Coordinator.
- **Decisions:** Joshua keeps admission, sample, signing and every investment decision.
- **Exposure:** readers of Tier-2 output join the Tier-1 reader log. Any successor pre-registration names them (design §4.5). Tier-2 output is exposure for that pre-registration.
- **Exposure before merge (2026-10-08).** Joshua saw the Tier-1 findings summary at about 07:12Z (no series, no keys), before this card merged. The §2.1 thresholds and rows 1–4 and 6 were written and reviewed by readers who had not seen the Tier-1 report, and their text is unchanged since `34c31c4`; that text, not the merge time, is what keeps them blind. Any later edit to that text by a Tier-1 reader is an admission-time change (§2.1). The Deployment Coordinator read the Tier-1 report at about 08:10Z, after `34c31c4`. Row 5 of the pattern table is the one such change (§2.1, row 5 provenance). The shock/grind reading under option (a) is partly known to Joshua; the report says so.
- **Selection count.** Choosing a §2 pattern from the sampled paths is a selection. It counts as one trial (K + 1) for any successor it points to. That successor's test discloses or excludes the sampled paths.

## §8 — OWED (operator)

1. Admit Tier 2 (after the Tier-1 return).
2. Capability option: (i) recommended.
3. Sample option and size (§4).
4. Diagnostic purpose, evidence-class and scope names; keep the receipt type or extend `_is_source_only` (§3.4); a new source approval.
5. Executor seat.
6. Tier-1 actual per-path cost (from its return).
7. The §2.1 pattern criteria: the `34c31c4` text is blind and freezes at merge. A change at admission is exposure and runs only on option (b) keys excluding the Tier-1 keys. Row 5 is such a change (Joshua, 2026-10-08); because of it, any admission that wants row 5 read needs option (b) with the whole set excluding the Tier-1 keys.

Acceptance scope is not owed: identity on the sampled runs plus the sidecar off/on tests (§3.3).

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
