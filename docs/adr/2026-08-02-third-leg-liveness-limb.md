# ADR 2026-08-02 — Third-leg screen: liveness-contribution limb (L1)

**Status:** `Accepted` — operator directive 2026-08-02, verbatim: *"add the liveness limb to the third-leg screen."*
**Decision date:** 2026-08-02

**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none

**Amends-in-part:** [`docs/spec/2026-07-27-third-leg-target-spec.md`](../spec/2026-07-27-third-leg-target-spec.md) — adds a new **§7.6 (L1)**, and corrects a **pre-existing S7-amendment omission** in §6.2 (its `SCREEN-PASS` trigger still read *"§7.1 (S1–S6)"* after S7 landed in §7.1, so a candidate could literally SCREEN-PASS while failing S7). This is the instrument that spec's change-control clause requires (*"§7 thresholds change only by a superseding ADR or by the §6.1 verdict firing"*); §6.1 has **not** fired.

---

## §0 — Rule 0 reads (production source, verified this session 2026-08-02)

| Path | What it grounds |
|---|---|
| [`lab/analysis/c1/c1_liveness_diversification_2026-08-02/RESULTS.md`](../../lab/analysis/c1/c1_liveness_diversification_2026-08-02/RESULTS.md) + `liveness.py` + `out/liveness.json` | Every number below. Anchors reproduce (312 weeks / 82 dead / run 4 / MYM 191 / MNQ 190); re-run byte-identical; fixed seeds 20260802 / 20260803 |
| `docs/spec/2026-07-27-third-leg-target-spec.md` §6.2, §7.1 S7, §7.4 M1 | The screen's existing force-levels; M1's day-agnostic requirement; §6.2's stale `S1–S6` trigger |
| [`docs/adr/2026-07-29-third-leg-symbol-occupancy-limb.md`](2026-07-29-third-leg-symbol-occupancy-limb.md) | The amendment precedent this ADR follows, and S7's *"never from observed trade frequency"* rule |
| [`TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md` §2 / §2a](../notes/rail_build/TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md) | Why liveness is worth scoring at all: ≥1 trade per Mon–Fri week, per account, enforced by **irreversible account deletion** |
| `lab/analysis/c1/tradeify_book_composition_2026-07-23/out/daily_panel.csv` | The committed panel L1 is computed on |

---

## §1 — Context

The screen has seven hard structural limbs, a risk-geometry pre-screen, statistical thresholds and
mechanism requirements. **None of them scores how often a candidate would trade** — verified absent
2026-08-02 (`rg` over §7 and the prop envelope returns nothing on frequency, cadence, or the
activity rule). That was tolerable while the idle rule read as *"soft-edged"*. It is not tolerable
now: enforcement is **irreversible account deletion** after an email warning, with no paused state.

The measurement that motivates this ([`c1_liveness_diversification_2026-08-02`](../../lab/analysis/c1/c1_liveness_diversification_2026-08-02/RESULTS.md)):

- The c1 book is **zero-trade in 82 of 312 Mon–Fri weeks (26.3%)**, longest run **4 weeks**.
- **The second leg was worth a lot on this axis, and it is measured, not modeled** — the two legs
  are each other's natural experiment. MYM alone: 150 dead weeks, longest run 9. MNQ alone: 151,
  run 10. Together: **82, run 4.** A ~45% cut in dead weeks and more than half the worst run.
- **And it is not a P&L effect.** On the 52 days both legs trade, corr(daily P&L) = **−0.13**.
  **Legs can diversify liveness without diversifying returns** — a property the screen has no
  vocabulary for.
- The obvious objection — *quiet weeks are quiet for everyone, so a third leg would be quiet too* —
  was tested and is **bounded at 1.13×** (P(MNQ dead) 0.484 vs P(MNQ dead | MYM dead) 0.547;
  permutation p = 0.022, n = 20,000). Real, detectable, small.
- **Wed and Thu are 622 of 1,556 business days (~40%) and the book has never traded one** — zero
  off-claim trades in six years, which also realized-confirms S7's occupancy pin.

**Decision driver (one sentence):** the screen can currently rank two otherwise-identical candidates
with no way to see that one of them would halve the book's dead weeks and the other would add
nothing — so a liveness limb is owed, **as a reported property, not as a bar**.

---

## §2 — Decision

**Add §7.6 to the third-leg spec: limb `L1 — liveness contribution`. It is REPORTED. It never
admits and never rejects.**

### 2-A — Why it must not be a bar

Every existing §7.1 limb is a hard structural FAIL. L1 must not join them, for three reasons:

1. **A leg with edge and no liveness benefit is still a good leg.** Rejecting it would trade a real
   edge for a cadence property that a **$1.82 token trade** already solves. That is a bad exchange
   and the screen should not be able to make it.
2. **Any threshold would be invented.** There is no pre-registered liveness floor to inherit, and
   `regime_robustness_gate.md` bars a separate invented floor as *"a hidden parameter through which
   post-hoc fitting could enter."* A reported number carries no such hazard.
3. **The measurement says a bar would be miscalibrated anyway** — see 2-D: liveness does not remove
   the tail at any realistic entry rate, so no threshold on it buys the thing that actually matters.

### 2-B — What L1 requires (the reporting contract)

A candidate's L1 report carries three numbers, computed on the committed daily panel:

| Field | Definition | Source rule |
|---|---|---|
| **L1.a — disjoint eligible sessions** | Weekday sessions the candidate **can** fire that **no incumbent can** | From **locked Pine session filters, never observed trade frequency** (S7's rule, inherited) |
| **L1.b — dead-week reduction** | Modeled fall in the book's 82 dead weeks at the candidate's **measured** per-eligible-session entry rate, with the **1.13× common-mode discount applied** | Rate from the measured panel; discount from `liveness.json` |
| **L1.c — tail effect** | Effect on the **p95 longest consecutive dead run** (baseline 4 weeks) | Seeded MC, same harness |

**The two source rules are asymmetric and both are load-bearing.** Eligible sessions come from Pine
filters because a leg that *can* fire covers the session as a matter of schedule (same rule as S7,
same reason). But **the firing rate must be measured**, because a leg that is eligible Wed/Thu and
fires 5% of the time covers almost nothing. Using eligibility alone would overstate L1.b; using
observed days alone would understate L1.a. **L1 requires both, and a report giving only one is
incomplete, not conservative.**

### 2-C — Verdict values (none of which gate)

`LIVENESS-POSITIVE` / `LIVENESS-NEUTRAL` / `LIVENESS-NEGATIVE` (the last meaning: fires only on
sessions the incumbents already cover, so it adds no liveness).

**L1 does not enter §6.2.** It cannot produce `SCREEN-PASS` or `SCREEN-FAIL`. Its only decision role
is as a **tie-break between candidates that have already passed everything else** — prefer the one
with the larger L1.b and the better L1.c.

### 2-D — What L1 is explicitly NOT a substitute for

Measured, and this is the reason L1 is a preference rather than a solution: at the incumbents' own
entry rate (~30.7%) a Wed/Thu leg cuts dead weeks **82 → ~40–45**, but the **p95 longest consecutive
run stays at 4 weeks**. Only near-daily firing removes it. The idle rule's exposure unit is the
*run*, not the count.

**So L1 reduces how often the obligation bites; the token mechanism is what closes the tail.**
A candidate scoring `LIVENESS-POSITIVE` does not discharge the token-trade disposition, and must not
be cited to defer it.

### 2-E — Relationship to M1 (the constraint that keeps L1 safe)

§7.4 **M1** requires the mechanism be *"day-agnostic by construction and merely scheduled into the
free days"*, because a day-of-week-selected edge is a fitted-calendar artifact.

**L1 scores the schedule, never the edge, and M1 governs on any conflict.** If a candidate's edge
exists *only* on Wed/Thu, **M1 fails it and L1 is irrelevant** — L1 must never be the reason such a
candidate survives. Ordering is explicit: M1 is evaluated first; L1 is computed only for candidates
that already satisfy M1.

### 2-F — Consequential fix: §6.2's `SCREEN-PASS` trigger

The S7 amendment added S7 to §7.1 but left §6.2's trigger reading *"All of §7.1 (**S1–S6**)"*. Under
the literal text a candidate failing S7 could still SCREEN-PASS. **Corrected to `S1–S7`** in the same
motion, with L1 named as excluded. This is a defect repair, not a threshold change.

---

## §3 — Alternatives considered

1. **Add it as S8, a hard structural bar.** Rejected per 2-A: it would reject good legs over a
   property a token trade solves, and would require an invented threshold.
2. **Add it to §7.2 as a risk-geometry limb.** Rejected — liveness is not risk geometry; R1–R5 are
   all daily-$ variance objects and L1 would be a category error in that table.
3. **Fold it into S7.** Rejected — S7 is a *prohibition* (do not collide) and L1 is a *preference*
   (prefer to cover). Merging them would give S7's hard-FAIL force to a preference, which is 2-A's
   error by another route. They share a source rule and a session map; that is not the same as
   sharing a force level.
4. **Write nothing and rely on the harness.** Rejected — the measurement exists but nothing routes
   it into candidate screening, which is exactly how the gap arose.

---

## §4 — Falsifier (revert trigger)

**H:** L1 identifies real, non-illusory liveness differences between candidates, and the common-mode
discount is the right correction.

**Revert trigger (binary):** if a third leg is ever deployed and its **realized** dead-week
reduction over ≥52 weeks lands outside **[0.5×, 2×]** of its L1.b projection, L1's construction is
wrong — re-derive the discount from the realized joint distribution before L1 is used to rank
another candidate. A miss inside that band is noise, not a falsification.

**Second limb:** if the measured common-mode lift on a **three**-leg book exceeds **1.5×** (vs the
1.13× measured on two), the independence-based curve is too optimistic to rank with; L1.b must be
recomputed on the realized three-way structure.

**Not a falsifier:** L1 failing to prevent a dead week. It was never a bar.

**Verdicts (binary, at the first ≥52-week realized window):**

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` | Realized dead-week reduction within **[0.5×, 2×]** of L1.b **and** three-leg common-mode lift **≤1.5×** | L1's construction holds; it stays the standing liveness limb |
| `FALSIFIED` | Realized reduction **outside** [0.5×, 2×] of L1.b | Construction is wrong. **L1 may not rank another candidate** until the discount is re-derived from the realized joint distribution |
| `AMBIGUOUS` | Lift **>1.5×** but reduction inside the band, **or** fewer than 52 realized weeks | Recompute L1.b on the realized three-way structure; carry to the next window, **never silently extend** |

---

## §5 — Forbidden moves

1. **Using a liveness benefit to rescue a candidate that fails any S-, R-, T-, or M-limb.** This is
   the rationalized-overlay class (*"but it fixes cadence"*). L1 is a tie-break among survivors and
   nothing else.
2. **Loosening R1, T5, or any other threshold because a candidate scores `LIVENESS-POSITIVE`.**
3. **Letting L1 motivate a day-of-week-selected edge.** M1 governs (2-E). Scheduling a day-agnostic
   mechanism is permitted; selecting an edge because it lives on Wed/Thu is the artifact class the
   gates exist to kill.
4. **Claiming L1.b from eligible-but-unfired sessions** — the rate must be measured and the 1.13×
   discount applied. Eligibility is not coverage.
5. **Citing `LIVENESS-POSITIVE` to defer or discharge the token-trade disposition** — measured, the
   tail survives (2-D).
6. **Reading L1 as a reason to compose.** Q-COMPOSE-1 stands: composing raised bust 2.65% → 38.75%
   via variance dominance. **A liveness argument does not answer a variance argument.**
7. **Treating the Wed/Thu window as a search instruction.** It is where liveness would *pay*, not
   evidence that edge exists there. The constraint **narrows** the space and may well be empty.

---

## §6 — Consequences

**Positive:** the screen can finally distinguish two candidates that differ only in when they trade;
the S7 session map gains a second consumer, so keeping it current has double the value; and a real
measured property of the existing book (liveness diversification at ~zero P&L correlation) stops
being invisible to candidate selection.

**Negative (real cost):** one more thing to compute per candidate — bounded, since it reuses the
committed harness and needs no new data, no pull, and no K. And a genuine hazard this ADR spends
most of its §5 on: **a reported property adjacent to a hard screen is exactly the shape that gets
quietly promoted into a justification.** L1's force level must be re-asserted whenever it is cited.

---

## §7 — Implementation

1. New **§7.6** in the spec with the L1 row and its force-level statement.
2. **§6.2** `SCREEN-PASS` trigger `S1–S6` → `S1–S7`, with L1 explicitly excluded.
3. Spec header **Amended-in-part-by** extended to name this ADR.
4. **No change** to §7.1–§7.5 thresholds, to any S/R/T/M requirement, or to §6.1.
5. `liveness.py` is the reference implementation; a candidate's L1 report re-runs it with the
   candidate's session mask and measured entry rate.

**Not implemented here:** no candidate is scored, no search is opened, no screen threshold moves.

---

## §10 — Audit hooks (runnable)

```bash
# L1 landed in the spec, and is stated as REPORTED (never a bar)
rg -n "L1|§7.6|liveness" docs/spec/2026-07-27-third-leg-target-spec.md | head

# The §6.2 trigger now reads S1-S7 and excludes L1.
# NOTE: do NOT grep for absence of "S1-S6" — the header's amendment note QUOTES the old
# text, so an absence test false-positives. Assert the repaired row instead (M-AHF: test
# the stored form, not the mental form).
rg -n '^\| `SCREEN-PASS` \|' docs/spec/2026-07-27-third-leg-target-spec.md \
  | rg -q 'S1.S7' && echo "6.2 repaired" || echo "6.2 TRIGGER REGRESSED"
rg -n '^\| `SCREEN-PASS` \|' docs/spec/2026-07-27-third-leg-target-spec.md \
  | rg -q 'L1 is REPORTED' && echo "L1 excluded" || echo "L1 EXCLUSION LOST"

# M1 still governs day-selection (2-E's premise)
rg -n "day-agnostic by construction" docs/spec/2026-07-27-third-leg-target-spec.md

# The numbers L1 is calibrated on still reproduce (anchors + byte-identical re-run)
python lab/analysis/c1_liveness_diversification_2026-08-02/liveness.py | rg "ANCHORS|common-mode LIFT|p95"

# The occupancy map L1 shares with S7 is unchanged
rg -n "MNQ1! Mon\+Tue|MYM1! Tue\+Fri" docs/spec/2026-07-27-third-leg-target-spec.md
```

## Verification

```bash
python scripts/check_brief.py docs/adr/2026-08-02-third-leg-liveness-limb.md --type adr
git log -1 --format='%h %cs' -- docs/spec/2026-07-27-third-leg-target-spec.md
```

## Change history

| Date | Change |
|---|---|
| 2026-08-02 | Initial ADR. Adds L1 (reported, never a bar) as §7.6; repairs §6.2's stale `S1–S6` trigger left by the S7 amendment. Calibrated on `c1_liveness_diversification_2026-08-02` (anchors reproduce, re-run byte-identical). No threshold moved, no candidate scored, nothing armed |
