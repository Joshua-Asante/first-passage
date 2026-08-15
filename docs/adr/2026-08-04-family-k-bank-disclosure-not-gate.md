# ADR 2026-08-04 — Family K-banks become a disclosure, not a gate; `K_eff` counts within-search selection only

**Status:** `Accepted` — **ratified by the operator 2026-08-04** (*"ratify it and execute §7"*), after directing the change (*"I also don't want to limit the discovery on any instrument. K=3 is an unnecessary requirement"*) and selecting option **(a)** (remove per-instrument ratcheting, keep within-search K) from two offered. **§7 executed the same session** — see the amendment log.
**Decision date:** 2026-08-04
**Authors:** Joshua (direction) + Claude Code (Opus 5, drafter)
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Amends-in-part:** [`2026-07-15-external-mechanism-harvest-intake.md`](2026-07-15-external-mechanism-harvest-intake.md) Requirement 3 · [`2026-07-11-discovery-campaign-defaults-ratified.md`](2026-07-11-discovery-campaign-defaults-ratified.md) Default #2 (K semantics) · [`2026-07-12-dsr-k-rule-and-variance-floor-supersession.md`](2026-07-12-dsr-k-rule-and-variance-floor-supersession.md) (the `K_DSR` *input*; its non-overlap floor and `V=1/n` pin are untouched) · [`2026-07-26-mechanism-counterparty-constraint-boundaries.md`](2026-07-26-mechanism-counterparty-constraint-boundaries.md) §2-C (executed-K banking survives, but what a bank *does* changes)
**Related:** [`Q-ICTEXP-1 results`](../../lab/analysis/_inbox/ict_mnq_2026-08/RESULTS_EXP.md) · [`Q-ICT-1MEXEC-1 draft prereg`](../briefs/pre-registration/2026-08-04-ict-1m-execution-mnq-preregistration.md) §2 (the reachability screen that surfaced this) · [`ORB cadence adjudication`](../notes/2026-08-04-orb-cadence-role-adjudication.md) (*"the K bank is NOT the terminator"*)
**Layer:** methodology (research rules of evidence only). No strategy parameter, allocation, `dd_protection` constant, lifecycle state, Pine source, or rail config is touched.

---

## §0 — Rule 0 reads (production source, verified this session 2026-08-04)

- **[`lab/research_utils/axis_screen.py`](../../lab/research_utils/axis_screen.py) @ `8908121`** — **the live enforcement surface, and the thing this ADR actually changes.** `_REQUIRED_KEYS` includes `k_banked` (L39); validation at L91-92; **L161-162 `k_lo, k_hi = lo + a["k_banked"], hi + a["k_banked"]`** is the ratchet; `clause_k = "PASS" if f_lo <= CAP else "FAIL"` (L164) and the FAIL short-circuit (L169). Frozen constants `CAP = 1.0`, `DSR_MIN = 0.95` (L31-32) with an explicit no-override rule.
- **[`lab/discovery/register_search.py`](../../lab/discovery/register_search.py) @ `e0bbad8`** — **does NOT sum families.** It stores one `K` per manifest (`"K": args.search_space_size`, L292) and may only lower it to `executed_k` at close (L357-368). There is no `K_banked` computation anywhere in it. The family bank is assembled **by hand, by reading closed manifests**, per doctrine — so most of the ratchet is convention, and exactly one module enforces it.
- **[`docs/methodology/strategy_harvest.md`](../methodology/strategy_harvest.md) @ `1bafe6f`** — the doctrinal home. **Requirement 3** ("Unburned family K-bank … If the family bank pushes floor(K_eff) above Cap 1.0, the seed is dead regardless of quality"), the family snapshot (GC/MGC 3,177 · ES 2 · **MNQ 2** · MYM 1 · 6E 1 · CL 1), **§Clause K** (`K_eff = K_intrinsic + K_banked(family)`; PASS iff `K_eff ≤ 3`; floors 1→0.65 · 2→0.85 · 3→0.98 · 4→1.06), and **L37** — *"`K_banked(family)` only grows … a family-bank kill does not soften with time or new evidence. This is the one requirement where 'the bar is too high' is never the right diagnosis."*
- **[`lab/research_utils/deflated_sharpe.py`](../../lab/research_utils/deflated_sharpe.py) @ `48b8cef`** — `expected_max_sharpe(K, V)` supplies `SR0`, i.e. **the expected maximum over K trials**. This is the statistical fact §1 turns on: the correction prices *taking a max*.
- **[`2026-07-12-dsr-k-rule-and-variance-floor-supersession.md`](2026-07-12-dsr-k-rule-and-variance-floor-supersession.md) @ `ba943a1`** — the direct precedent. It re-baselined `K_DSR` because counting overlapping matrix-profile subsequences as independent trials over-deflated to unreachability, and its §4 pre-commits a re-baseline path when a gate is shown mis-calibrated. **Its non-overlap floor and unconditional `V = 1/n` pin are NOT touched here.**
- **[`2026-07-26-mechanism-counterparty-constraint-boundaries.md`](2026-07-26-mechanism-counterparty-constraint-boundaries.md) @ `0f36c3a`** §2-C — the executed-K closure rule and its first application. **ST-EH-1 closed `operator-stopped` banking executed `K=2` split 1 MNQ + 1 MYM against declared 84.**
- **`discovery_manifests/st_eh_supertrend_grid.json`** — read directly, not from prose: `status: closed`, `K: 2`, `declared_K: 84`, `results.n_submitted: 0`, `closure_mode: operator-stopped`, and a `verdict` field reading **"OPERATOR-STOPPED before declared reads executed. NO campaign verdict exists and none may be quoted."**
- **`discovery_manifests/d5_nq_intraday_mom.json`** — `status: closed`, `K: 1`, hypothesis = Baltussen intraday momentum. The other half of MNQ's bank.

---

## §1 — Context

The `Q-ICT-1MEXEC-1` reachability screen (2026-08-04) computed MNQ's admissible band under the current rule and found it **0.020 wide**: `K_banked(MNQ)=2` + `K_intrinsic=1` ⇒ `K_eff=3` ⇒ annSR floor **0.980** against **Cap 1.0**. The floor sits **above every result ever measured on the instrument** — `ORB-MNQ-1`, which cleared the full Gen-2 pipeline, realized **+0.890** (Bulenox) / **+0.835** (Tradeify). A second seed would reach `K_eff=4`, floor **1.060 > Cap**, closing MNQ outright and permanently.

Three facts make that outcome hard to defend:

1. **Half of MNQ's bank came from a campaign with no verdict, on an unrelated mechanism.** `st_eh_supertrend_grid` banked K=1 against MNQ from a Supertrend grid that executed **zero of its 80 declared reads** and whose own manifest says no verdict exists. The ICT chain was pre-registered independently; it was not selected because Supertrend failed. As a selection channel this is close to empty.
2. **The correction being applied is for taking a maximum.** `deflated_sharpe.expected_max_sharpe(K, V)` prices `E[max of K trials]`. That is exactly right for a grid of 84 configs and exactly wrong for a single pre-committed hypothesis, which maximizes over nothing. Pre-registration is the very act that removes the inflation the correction exists to remove, and the current rule gives it no credit.
3. **The rule contradicts another standing rule.** A finite, never-softening per-instrument budget means the instrument you know best becomes the one you are least allowed to research, and it pushes work toward instruments with the least evidence purely for statistical headroom. `CONFIRM-FREE-NODEPLOY-2026-08-03` separately forbids **instrument-shopping**. One rule manufactures the pressure another forbids.

**What the family bank was standing in for** — the file-drawer channel: run campaigns until one passes, report that one. **This repo already defeats that channel by construction**: nulls are recorded, prominently and permanently (`GC/MGC 3,177`, D5 FALSIFIED, OPENPRESS FALSIFIED, four ICT layers falsified, the MNQ DEAD list whose ledger says *"The DEAD list is the point"*). The multiplicity information is preserved and visible. It does not *also* need to be a hard gate that eventually closes instruments — and the ORB cadence adjudication (2026-08-04) already ruled, independently, that *"the K bank is NOT the terminator."*

**Decision driver (one sentence):** the family-K ratchet is a max-over-K correction applied where no max is taken, it is about to close the repo's most-instrumented instrument on the strength of a verdict-less Supertrend grid, and the channel it protects against is already handled by recorded nulls.

---

## §2 — Decision

**Decision:** `K_eff` counts **within-search selection only** — `K_eff = K_intrinsic`, the trial count of the seed's own search. `K_banked(family)` is **retained, computed, and reported as a mandatory disclosure**, and **no longer enters the Clause-K arithmetic or gates admission**.

Concretely:

| | Before | After |
|---|---|---|
| `K_eff` | `K_intrinsic + K_banked(family)` | **`K_intrinsic`** |
| `K_DSR` | same sum | the seed's own within-search count (non-overlap floor rule from ADR 2026-07-12 **unchanged**) |
| Clause K | PASS iff `floor(K_eff) ≤ Cap 1.0` ⇔ `K_eff ≤ 3` | **unchanged in form**, now evaluated at `K_eff = K_intrinsic` |
| `K_banked(family)` | hard gate; "only grows"; never softens | **mandatory disclosure** — still computed from closed manifests, still printed by the screen, still required in every pre-registration §K block; **not a FAIL condition** |
| Cap `1.0`, `DSR ≥ 0.95`, `V = 1/n` | frozen | **frozen, untouched** |

**A grid still pays in full.** Any design that selects among variants after seeing results — parameter sweeps, conditioning-gate variants, exit alternatives, best-of-K — carries those variants in its own `K_intrinsic`. Nothing about within-search multiplicity control is relaxed. `ORB-MNQ-1`'s standing rule that "any filtered variant raises `K_eff`" survives verbatim; it just no longer inherits an unrelated campaign's history.

**Effective:** on operator ratification.
**Scope:** discovery/harvest intake and the K-ledger semantics that feed DSR. Research rules of evidence only.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Status quo** (family ratchet stays) | Closes MNQ permanently on the strength of a verdict-less Supertrend grid, contradicts the instrument-shopping prohibition, and applies a max-over-K correction where no max is taken. §1. |
| **Drop K as a gate entirely** (the operator's option (b)) | Explicitly offered and **declined by the operator in favour of (a)**. It would remove within-search protection, which is the single most reliable way a backtest lies: 200 variants, report the winner. That protection earns its place. |
| **Keep the ratchet, raise the Cap** | Launders a mis-specified K through a believability ceiling that is doing a different job. The Cap answers "what annSR claim is credible"; K answers "how much selection happened". Moving the wrong dial is the exact pattern ADR 2026-07-12 §3 rejected ("arbitrarily softening the threshold to fit a known-flawed K"). |
| **Keep the ratchet, exempt no-verdict banks only** | Fixes the ST-EH-1 case and nothing else. MNQ would sit at `K_eff=2` (floor 0.85) and close again after one more seed. It treats the symptom (one bad bank entry) rather than the unit error. |
| **Graded family term** (e.g. `K_eff = K_intrinsic + log₂(1+K_banked)`) | Genuinely attractive and **not ruled out on principle — ruled out on evidence**. There is no measurement here calibrating how much cross-campaign selection actually inflates a pre-registered seed, and inventing a functional form to fit the desired answer would be the same unprincipled move as raising the Cap. §4 names the evidence that would license it. |

---

## §4 — Falsifier (revert trigger)

**Hypothesis this ADR bets on (H):** for a **pre-registered, single-hypothesis** seed, the
cross-campaign selection inflation contributed by its family's prior closed campaigns is small
enough that pricing it via a hard `E[max of K]` floor does more harm (permanently foreclosing
instruments) than good — **given** that the repo records its nulls rather than filing them away.
The whole decision rests on that clause; if nulls ever stopped being recorded, H fails
immediately and the family term should return.

**Revert trigger:** if a seed promoted under this ADR at `K_eff = K_intrinsic` **subsequently fails out-of-sample replication**, AND its instrument family carried **≥ 3 prior recorded nulls** at promotion time, then the cross-campaign selection channel is real and materially priced, and this ADR is falsified.

**Revert action:** supersede with a **graded** family term (the §3 alternative deferred for lack of evidence), calibrated on the observed replication failures — **not** a return to the hard ratchet, which the same evidence would not support either. The superseding ADR must cite the specific failed replication.

**Second, independent trigger:** if any seed is admitted under this ADR whose pre-registration **omits** the `K_banked(family)` disclosure, the disclosure has decayed to ceremony and the mechanical enforcement in §7 Phase 2 has failed. That is an implementation defect, not a doctrine defect — repair the screen, do not revert the doctrine.

**Trigger check schedule:** the standing quarterly programme audit — next **2026-08-08**, then **2026-11-08**. Checked alongside ADR 2026-07-12's own trigger, which rides the same date.

**Honest statement of what does *not* fire here.** ADR 2026-07-12 §4 pre-commits a re-baseline when "DSR is still un-passable for an edge independently corroborated at high confidence by ≥2 other gates." `ORB-MNQ-1` is corroborated by ≥2 gates (within-day placebo p=0.0040, temporal 2021+ PASS, Stage-8 N_eff) and **would** fail at `K_eff=3` — but it was admitted at its actual `K_eff=2` and passed. **So that falsifier has not cleanly fired, and this ADR does not claim it has.** This ADR rests on the §1 argument, not on a triggered gate. A reader who finds the argument unpersuasive should reject it on that basis rather than looking for a trigger that is not there.

---

## §5 — Forbidden moves (under this ADR)

- **Re-reading this ADR as "K no longer matters."** Within-search K is untouched and still gates. A sweep, grid, conditioning-variant set, or any post-hoc choice among alternatives carries its full count in `K_intrinsic`. This is the move most likely to be attempted and it is the one this ADR most specifically does not license.
- **Quietly declaring `K_intrinsic = 1` for a design that actually searched.** The single largest exposure created here: with the family term gone, `K_intrinsic` is the *only* remaining brake, so understating it is now strictly more consequential than before. A pre-registration must enumerate every axis it varied, and a design that tried and discarded variants before freezing declares them.
- **Dropping the `K_banked(family)` disclosure** because it no longer gates. It is mandatory precisely so a reviewer can see a heavily-mined family and exercise judgment the arithmetic no longer exercises for them.
- **Re-proposing a mechanism the family record already falsified**, on the grounds that K no longer blocks it. Mechanism-level foreclosure is owned by [`docs/rejected_candidates.md`](../rejected_candidates.md) and the re-proposal bars, which are **unchanged and still binding**. K was never the right instrument for that job; removing it as a gate does not reopen anything the mechanism record closed.
- **Loosening Cap 1.0, `DSR ≥ 0.95`, or the ADR 2026-07-12 `V = 1/n` pin** under cover of this change. All three are frozen and out of scope.
- **Editing §4's trigger instead of superseding** if it proves wrong (Known Trap #12).
- Any `core/`, lock, allocation, `dd_protection`, lifecycle, Pine, rail, or `LEG_MAP` change.

---

## §6 — Consequences

**Positive:**

- **No instrument is permanently closed to discovery by accumulated history.** MNQ returns to `K_eff = 1`, floor **0.650**, headroom 0.350 — as do ES (bank 2), MYM, 6E, CL. **GC/MGC's 3,177 no longer forecloses it either**, which is the largest single unlock and also the one most deserving of reviewer scrutiny via the retained disclosure.
- **The perverse gradient is removed.** Research can go where the evidence and the venue fit are, not where the statistical headroom happens to be.
- **Pre-registration is finally rewarded.** Freezing a single hypothesis before looking now materially lowers the bar versus running a grid — which is the incentive the whole discipline is meant to create.

**Negative (real, not theatrical):**

- **Sequential single-hypothesis campaigns on one family are no longer priced at all.** Ten consecutive `K_eff=1` campaigns on MNQ, each pre-registered, produce a tenth winner that is genuinely inflated relative to a true single test — and this ADR does not charge for it. The disclosure makes it *visible*; nothing makes it *costly*. This is the honest price of the change and §4's first trigger is aimed squarely at it.
- **More weight lands on human review.** An arithmetic FAIL is auditable and unarguable; "the reviewer should have noticed the family had six nulls" is neither.
- **`K_intrinsic` becomes a single point of failure** for multiplicity control (see §5, move 2).

**Risks:**

- The cross-campaign channel may be larger than §1 argues. Mitigation: §4 trigger 1 plus the retained disclosure; the graded-term alternative is pre-staged in §3 so the repair path is already designed.
- Reviewers may read the family snapshot as decorative once it stops gating. Mitigation: §4 trigger 2 makes an omitted disclosure a detectable implementation defect.

**Downstream artifacts needing update (enumerated for §7):**

- `docs/methodology/strategy_harvest.md` — Requirement 3, §Clause K formula, the L37 "never softens" note.
- `lab/research_utils/axis_screen.py` + `tests/test_axis_screen.py` — the L161-162 sum, and tests that pin it.
- `ops/instruments/MNQ.md` **N10** — asserts MNQ's band is effectively closed. **That finding becomes false on ratification** and must be amended, not deleted (its arithmetic was correct under the prior rule).
- `docs/briefs/pre-registration/2026-08-04-ict-1m-execution-mnq-preregistration.md` §2 — its `FAIL-AS-WRITTEN` reachability screen is superseded; **its §8 NO-GO recommendation is not** (three of four reasons never depended on K, and `Q-ICTEXP-1` since measured the expectancy at ≈0).
- `docs/adr/INDEX.md`, `STATE.md` decision index.

---

## §7 — Implementation plan

- **Phase 0** — re-verify the §0 anchors (`axis_screen.py` @ `8908121`, `strategy_harvest.md` @ `1bafe6f`) still current; abort if either moved.
- **Phase 1 — doctrine.** `strategy_harvest.md`: rewrite Requirement 3 from gate to disclosure; change §Clause K to `K_eff = K_intrinsic`; replace the L37 "never softens" paragraph with the disclosure rule. Retain the family snapshot verbatim (it is now the disclosure's reference).
- **Phase 2 — code.** `axis_screen.py`: keep `k_banked` in `_REQUIRED_KEYS` and in the emitted row/table (disclosure preserved); change L161-162 so `k_eff = k_intrinsic` and `k_banked` is reported alongside rather than summed. Add a regression test asserting a row with a large `k_banked` and `k_intrinsic=1` now **PASSES** Clause K while still **reporting** the bank — and an adversarial test that a `k_intrinsic` of 5 still FAILs, so the change cannot be mistaken for disabling the clause.
- **Phase 3 — sweep.** `rg --no-ignore "K_intrinsic \+ K_banked|K_eff = K_intrinsic \+"` across `docs/` and `lab/` and repair every restatement; frozen pre-registrations are **historical record and must not be edited** — they get a reader-intercept only where they state the rule as current doctrine.
- **Phase 4 — ledger.** Amend `MNQ.md` **N10** (and the MYM/M2K sibling lines that quote floors) to record the arithmetic as correct-under-the-prior-rule and superseded here.
- **Phase 5** — verification block below executes; status → `Accepted` on operator ratification.

---

## §10 — Audit hooks (runnable)

```bash
# The enforcement surface this ADR changes (expect the SUM before Phase 2, k_intrinsic-only after):
grep -n "k_banked" lab/research_utils/axis_screen.py

# Doctrine must not still state the summed form as current:
grep -n "K_intrinsic + K_banked" docs/methodology/strategy_harvest.md

# The disclosure must survive as a REQUIRED key (guards the FM-3 decay-to-ceremony risk):
grep -n "_REQUIRED_KEYS" -A 4 lab/research_utils/axis_screen.py

# register_search must still never sum families (it did not before; it must not start):
grep -c "K_banked" lab/discovery/register_search.py        # expect 0

# The frozen constants this ADR does NOT touch (expect CAP 1.0 / DSR_MIN 0.95):
grep -n "^CAP\|^DSR_MIN" lab/research_utils/axis_screen.py

# The no-verdict bank this ADR cites (expect operator-stopped, n_submitted 0, declared 84):
python -c "import json;d=json.load(open('discovery_manifests/st_eh_supertrend_grid.json'));print(d['closure_mode'], d['results']['n_submitted'], d['declared_K'], d['K'])"

# N10 must not still assert MNQ is closed once this is Accepted:
grep -n "N10" ops/instruments/MNQ.md
```

---

## Amendment log (append-only)

- **2026-08-04 — PROPOSED.** Drafted at operator direction after the `Q-ICT-1MEXEC-1` reachability screen surfaced the 0.020-wide MNQ band. Operator selected option (a) (remove per-instrument ratcheting, keep within-search K) over (b) (drop K as a gate). **Not in force until ratified**; §7 is unexecuted, so `axis_screen.py` and `strategy_harvest.md` still carry the summed form.
- **2026-08-04 — RATIFIED and §7 EXECUTED** (operator: *"ratify it and execute §7"*). Phase 0 re-verified both anchors unmoved (`axis_screen.py` @ `8908121`, `strategy_harvest.md` @ `1bafe6f`). **Phase 1** — `strategy_harvest.md`: Requirement 3 rewritten gate→disclosure, §Clause K set to `K_eff = K_intrinsic` with the grid-still-pays clause, the "never softens / not a judgment call" paragraph explicitly **withdrawn**, and the pre-registration §K block re-worded so `K_intrinsic` carries an enumerate-every-axis instruction. **Phase 2** — `axis_screen.py` L161-162 no longer sums; `k_banked` stays a `_REQUIRED_KEYS` member, stays in the emitted row, and was **added to the rendered table** (it was JSON-only, which would have let the disclosure decay unseen — §4 trigger 2). Tests 21 → **25**: the fixture test's superseded expectations are recorded in-place rather than silently flipped, plus four new pins including the adversarial `k_intrinsic=5` still-FAILs case and a `k_banked`-still-required case. **Phase 3** — sweep repaired the live deference in `strategy_harvest.md` (it named a *frozen* pre-registration as source-of-truth for a formula that has now diverged), added a reader-intercept to `Q-KBUDGET-1-screen-preregistration.md` §B at the point of reading, and left `instrument_map.py` on the old formula **by design** with a docstring explaining why (closed-study reproducibility). **Phase 4** — `MNQ.md` **N10**, `MYM.md` K-bank bullet, and `M2K.md` **M4** amended as correct-under-the-prior-rule and superseded, none deleted. **Measured effect on the standing fixture:** GC/MGC's 3,177-bank axes (D1, D4) stop being K-killed and fall through to UNSCREENABLE on their own merits, while the genuine wide searches (D2 at `K_intrinsic` 1000-10000, D6 at 450) still **FAIL Clause K** — which is the intended shape in one table.
