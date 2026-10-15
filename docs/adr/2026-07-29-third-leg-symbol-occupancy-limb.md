# ADR 2026-07-29 — Third-leg screen: order-symbol occupancy limb (S7)

**Status:** `Accepted` — operator directive 2026-07-29, verbatim: *"amend the third-leg spec with the symbol-occupancy limb."* §4 empirical limbs DORMANT since 2026-08-06 (Rule 11; record in §4). The 2026-08-06 "MYM1!/MNQ1! retained-not-released" claim is superseded by [`2026-08-12-msl-mym-occupancy-release.md`](2026-08-12-msl-mym-occupancy-release.md) (released for new non-Striker research; Striker legs stay barred). S7 itself is untouched.
**Decision date:** 2026-07-29
**Authors:** Joshua (direction) + Claude Code (Fable 5, drafter)
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** [`2026-08-12-msl-mym-occupancy-release.md`](2026-08-12-msl-mym-occupancy-release.md) in part — the Addendum 2026-08-06 "Out of scope" claim that `MYM1!`/`MNQ1!` remain retained-not-released is superseded (see the §4 dormancy record). **S7 itself (the core §2 decision) is untouched.**
**Retain-until:** none
**Revision:** 2026-10-15 — retention trim (ADR decay audit; operator direction 2026-10-15): §0 anchor table, §7, §10 hooks other than the decisive production read, Verification, change history and the 2026-08-06/2026-08-14 addenda removed; their dormancy record and supersession note are kept in the status line and §4. Pre-trim text at blob `b9c6447cfddbec91dfb98367adde39a7be71c1e7` (commit `4121e84c95f4990b71962e3b9570c4c3fad88426`).
**Amends-in-part:** [`docs/spec/2026-07-27-third-leg-target-spec.md`](../spec/2026-07-27-third-leg-target-spec.md) — adds **S7** to §7.1, corrects §2.2's sufficiency claim, narrows §2.4 Slot 2, and adds a sixth failing row to the §7.5 negative control. This is the instrument that spec's own change-control clause requires (*"§7 thresholds change only by a superseding ADR or by the §6.1 verdict firing"*); §6.1 has **not** fired (no candidate has reached a composed re-MC).
**Related:** [`SLR-MYM-1 closure`](../briefs/closures/SLR-MYM-1-closure-falsified-stage0.md) F1 (the finding that produced this).
**Layer:** screening standard for a same-account third c1 leg. **No** strategy parameter, allocation, `dd_protection` constant, Pine source, rail code, or live constant is touched.

---

## §0 — Source read

Decisive read (verified 2026-07-29 at `54b1489`): `ops/c1_rail/crosstrade_payload.py` (`flatten_first=true` on entries; quantity-less `closeposition` on exits, both keyed `account` + `instrument`); full anchor table at the pinned prior version (`4121e84c`).

**Scope note on the read.** The payload is keyed on **`account` + `instrument`**. Everything below is therefore scoped to *the same account*; it says nothing about two strategies on the same symbol in **different** accounts (the separate-eval fork, spec §8), nor about two strategies on **different** symbols in the same account.

---

## §1 — Context

The ratified third-leg screen models same-account contention as a **contract-capacity** problem: §2.2 computes free micros per weekday from the incumbents' locked session filters, and §2.4 derives two admissible slots from that table. Every S-requirement in §7.1 is about venue rules, compliance, and cap.

`SLR-MYM-1` was screened against exactly that surface, passed the cap arithmetic on four weekdays, and was only then found to be structurally impossible on two of those days — for a reason the screen does not model. Both the incumbent Striker DJ30→MYM leg and the candidate resolve to the **same order symbol `MYM1!`**, and our own rail's payload construction makes two strategies on one symbol **destructively interfere**:

- A second strategy's **entry** carries `flatten_first=true` → it **closes the incumbent's open position** before entering.
- A second strategy's **exit** issues `closeposition` with **no quantity** → it flattens **whatever is open**, including the incumbent's position.

This is not a sizing bug to be fixed downstream, and it is not contingent on venue netting semantics — it is a property of the rail as built, and it is bidirectional. Contract cap is divisible; an open position is not.

**Decision driver (one sentence):** the screen's whole purpose is to reject a candidate before K or spend, and it currently passes candidates that cannot physically coexist with the incumbent book — so cap arithmetic must be joined by a symbol-occupancy limb.

---

## §2 — Decision

**2026-09-05 applicability pointer:** §2-D below describes the historical incumbent
book. The Select configuration campaign has no live incumbent edition and admits
joint candidates subject to shared-symbol implementation and parity obligations;
see the [campaign admission ADR](2026-09-05-tradeify-select-striker-expression-readmission.md#same-day-amendment--long-only-co-exposure).
This scope clarification does not amend S7 or discharge its execution concern by
long-only directionality.

**2-A. New hard-structural requirement S7 (added to spec §7.1).**

> **S7 — Order-symbol occupancy.** The candidate must not require an **order symbol already traded by
> an incumbent c1 leg in the same account** on any session that incumbent can fire. Satisfied
> **trivially** by an unoccupied symbol. Otherwise it requires **session-disjointness from the
> incumbent on that symbol** — and the disjointness must be established from **locked Pine session
> filters**, not from observed trade frequency (an incumbent that *can* fire occupies the symbol
> whether or not it did).
>
> Rationale: `ops/c1_rail/crosstrade_payload.py:86-87` sends `flatten_first=true` on every entry, and
> `:62-73` sends `closeposition` without quantity on every exit — both keyed `account` + `instrument`.
> Two strategies on one symbol in one account destroy each other's positions in both directions.

**2-B. §2.2 sufficiency correction.** The free-cap table is **necessary, not sufficient**. A weekday with free contract cap may still be unusable, because cap and symbol are independent constraints. §2.2 gains a pointer to S7 and the standing sentence: *"free cap on a day does not imply the day is available; check symbol occupancy first."*

**Redaction 2026-10-09 (operator decision 2026-10-09, option 2):** the Striker DJ30 v4.5 day-of-week set and session window are Pine-only (`core/strategies/CATALOG.md` §Locked parameter record). In this document weekdays are therefore named by **class** — the *MNQ-only weekday*, the *shared weekday* (both incumbents can fire), the *MYM-only weekday* and the *two free weekdays* — and entry windows by reference to the locked Pine filters. Every number, gate, slot and verdict is unchanged. Original preserved in first-passage-archive `archive/preserve-exposure-2026-10-09` `f5f978ab90855e0b64d5981d7d8ffd4a0bbe8e26`.

**2-C. §2.4 Slot 2 narrowed.** Slot 2 (the two single-incumbent weekdays) was derived on cap grounds alone. Under S7 it is **unavailable to a candidate on an occupied symbol**: the incumbent MNQ leg can fire on **the MNQ-only weekday**, and the incumbent MYM leg on **the MYM-only weekday**. Slot 2 therefore survives **only for a candidate on an unoccupied symbol**. Slot 1 (the two free weekdays) is **unaffected** — neither incumbent can fire on those days, so no symbol is occupied.

**2-D. §7.5 negative control gains a sixth failing row.** ORB-MNQ-1 trades **MNQ daily**; the incumbent Striker NAS100→MNQ leg can fire on **its locked weekdays**. ORB therefore **fails S7** in addition to S5, R1, R3, M2 and the S4 directionality question. The known-bad candidate is re-rejected by the new limb, which is the non-vacuity check this ADR owes.

**2-E. The escape hatch is named, because it is the useful half of this decision.** S7 is satisfied *trivially* by any venue-tradable symbol the book does not occupy — **MES**, **M2K**, **MGC** and the micro-FX pair (M6A/M6E) are all unoccupied today. A candidate on an unoccupied symbol gets the **full** §2.2 cap table with no session-disjointness argument required. **S7 is therefore a redirect, not only a bar** — it makes "pick an unoccupied instrument" a first-class design move rather than an afterthought, and it is the single cheapest way for a future proposal to clear it.

**Effective:** 2026-07-29.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Fix the rail so two strategies can share a symbol (per-leg position tracking) | A rail redesign on the critical path of the first live fill, in the same period the rail produced an unintended fill and disproved `order_id` idempotency. It also fights the qty-0 exit sentinel's *deliberate* design (L68-72: not trusting stale bookkeeping is the safety property). Cost is high, benefit accrues only to a candidate that does not exist |
| Put the constraint in §2 only, as a derivation | §2 corrections need no ADR, which is exactly why they cannot carry a *binding* gate. A candidate is screened against §7; a fact recorded only in §2 would not reject anything |
| Fold it into S5 (the cap limb) | Conflates two independent constraints and would make the negative control's failure reasons unreadable. Cap is divisible and per-day; symbol occupancy is binary and per-instrument. Separate limbs keep a SCREEN-FAIL diagnosable |
| Leave the screen unchanged and rely on reviewers | This screen exists *because* the previous candidate reached a 1.5-hour frozen-engine run on a defect a reviewer should have caught. Relying on reviewers is the failure mode the artifact was created to replace |
| Treat it as guidance rather than a hard requirement | It is a physical impossibility, not a preference. A "soft" limb would admit candidates that cannot be deployed at any weight |

---

## §4 — Falsifier (revert trigger)

> ⚠ **DORMANT (Rule 11; 2026-08-06, claim-alignment M29).** Both empirical limbs below are dormant. The false-positive limb needs demonstration on the venue, not in argument; the false-negative limb needs a dry-fire or live session; the B7 path in the schedule is mooted by the 2026-08-04 de-scope. None can accrue while no leg is deployed. **Re-arm:** F3 registers a venue **and** a leg is deployed there (not by argument, calendar alone, or research-only Tradeify-shaped work). **Surviving coverage:** the calendar checks convene but may only record that the falsifier was unreachable; *do not read an unfired calendar check as evidence the limb held.* The 2026-08-06 addendum's "MYM1!/MNQ1! retained-not-released" sentence is superseded by `2026-08-12-msl-mym-occupancy-release.md` (released for new non-Striker research; withdrawn Striker legs stay barred).

**H:** S7 rejects candidates that genuinely cannot coexist with the incumbent book, and rejects nothing else.

**Falsified if either fires:**

- **False-positive limb** — a candidate is rejected on S7, and it is subsequently demonstrated (on the venue, not in argument) that two strategies **can** hold independent positions on one symbol in one account under the rail as configured. Then S7 is over-broad: revert to a cap-only screen and record the venue evidence.
- **False-negative limb** — a candidate **passes** S7 and then exhibits destructive interference with an incumbent in a dry-fire or live session. Then S7 is under-specified (most likely because session-disjointness was established from observed frequency rather than locked Pine filters — the failure mode 2-A's second sentence exists to prevent).

**Trigger check schedule:** rides the programme-audit dates (2026-11-08, 2027-02-08), and any B7 session that routes a non-incumbent leg.

---

## §5 — Forbidden moves

- **Establishing session-disjointness from observed trade frequency.** The spec's own §2.2 measures ~30% entry rates for both incumbents; a symbol is occupied on every session the incumbent **can** fire, not the ~30% it did. Reasoning from realized entries would pass a candidate that collides three days in ten.
- **Using cap donation to "free" an occupied day.** Cap and symbol are independent; donating contracts cannot manufacture a second net position. This was the live temptation in the SLR-MYM cap-reallocation rider and it is arithmetically void.
- **Reading S7 as licence to re-open cap re-allocation.** Cap remains owned by Q-CAPALLOC-1's successor ADR, never by a third-leg proposal (spec §5, unchanged).
- **Weakening S7 to admit a specific candidate.** The limb is binary. A candidate that needs it softened needs a different instrument instead — see 2-E.
- **Treating 2-E's unoccupied symbols as pre-cleared.** S7 is one of seven S-requirements; MES/M2K/MGC each still face S4 (long-only if Equity Index), their own instrument-ledger bars and K banks, and every R/T/M limb. M2K in particular carries a binding class bar and a $0 K bank that is spendable exactly once.

---

## §6 — Consequences

**Positive.** The screen now rejects physically-impossible candidates at zero cost. The rejection is *diagnosable* (a distinct limb, not a muddied S5). And 2-E converts the finding into design guidance — the cheapest route to a viable third leg is now explicitly "use a symbol the book does not occupy," which also sidesteps the Slot-2 narrowing entirely.

**Negative (real).** Slot 2 is materially narrowed for same-symbol candidates, so the admissible design space on MYM/MNQ shrinks to Slot 1 (the two free weekdays, ~104 sessions/yr) — and the spec already flags that slot's session count as a **power** constraint. For an occupied symbol, S7 and the Clause-N power floor now squeeze from both sides; SLR-MYM died in exactly that squeeze. This is an honest narrowing of what the same-account fork can host, not a cost this ADR introduces.

**Risk.** The decisive read is our own payload construction, not a venue-published rule. If CrossTrade/Tradovate semantics differ from what the payload implies, S7 could be over-broad — that is the §4 false-positive limb, and the cheap way to settle it is an attended dry-fire observation, not an argument.

---

## §10 — Audit hooks (runnable)

```bash
# The decisive production read -- if either changes, re-derive S7 (or revert it)
grep -n "flatten_first=true" ops/c1_rail/crosstrade_payload.py
grep -n "command=closeposition" ops/c1_rail/crosstrade_payload.py
grep -n "Omitting quantity lets closeposition flatten" ops/c1_rail/crosstrade_payload.py
```
