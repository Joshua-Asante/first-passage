# ADR 2026-07-29 — Third-leg screen: order-symbol occupancy limb (S7)

**Status:** `Accepted` — operator directive 2026-07-29, verbatim: *"amend the third-leg spec with the symbol-occupancy limb."* **AMENDED 2026-08-06 (claim-alignment M29 / Rule 11):** both empirical §4 limbs are **dormant** — inputs cannot accrue until F3 registers a venue **and** a leg is deployed there; calendar checks still convene but only **record** unreachability (Addendum 2026-08-06). Slot-2 narrowing **not** shown dead (symbols retained-not-released). **AMENDED 2026-08-14:** the 2026-08-06 "retained-not-released" language for `MYM1!`/`MNQ1!` is superseded by [`2026-08-12-msl-mym-occupancy-release.md`](2026-08-12-msl-mym-occupancy-release.md) — released for new non-Striker research; Striker legs stay barred (Addendum 2026-08-14). S7 itself is untouched.
**Decision date:** 2026-07-29
**Authors:** Joshua (direction) + Claude Code (Fable 5, drafter)
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** [`2026-08-12-msl-mym-occupancy-release.md`](2026-08-12-msl-mym-occupancy-release.md) in part — the Addendum 2026-08-06 "Out of scope" claim that `MYM1!`/`MNQ1!` remain retained-not-released is superseded (see Addendum 2026-08-14 below). **S7 itself (the core §2 decision) is untouched.**
**Retain-until:** none
**Amends-in-part:** [`docs/spec/2026-07-27-third-leg-target-spec.md`](../spec/2026-07-27-third-leg-target-spec.md) — adds **S7** to §7.1, corrects §2.2's sufficiency claim, narrows §2.4 Slot 2, and adds a sixth failing row to the §7.5 negative control. This is the instrument that spec's own change-control clause requires (*"§7 thresholds change only by a superseding ADR or by the §6.1 verdict firing"*); §6.1 has **not** fired (no candidate has reached a composed re-MC).
**Related:** [`SLR-MYM-1 closure`](../briefs/closures/SLR-MYM-1-closure-falsified-stage0.md) F1 (the finding that produced this).
**Layer:** screening standard for a same-account third c1 leg. **No** strategy parameter, allocation, `dd_protection` constant, Pine source, rail code, or live constant is touched.

---

## §0 — Rule 0 reads (production source, verified this session 2026-07-29)

| Path | Anchor | What it grounds |
|---|---|---|
| `ops/c1_rail/crosstrade_payload.py:62-73, 86-87` | `54b1489` 2026-07-23 | **The decisive read.** Entry orders: `if leg == "entry": parts.append("flatten_first=true")` (L86-87), on a payload keyed `account=…;instrument=<symbol>`. Exit orders: `command=closeposition` with `account` + `instrument` and **quantity deliberately omitted** at the qty-0 sentinel — the comment states the intent verbatim: *"Omitting quantity lets closeposition flatten whatever is actually open, rather than trusting stale bookkeeping"* (L68-72) |
| `ops/c1_rail/c1_sizing_host_reference.py:85, 247-249, 284-290` | `c134060` 2026-07-24 | `LEG_MAP` is keyed by **`leg_id`**, validated `if leg_id not in LEG_MAP`, and `cap_alloc` is allocated per `leg_id`. **The host has no symbol-collision concept** — it would accept a third `leg_id` mapping to an already-traded instrument and size it independently. The host is therefore *not* the surface that prevents this |
| `docs/spec/2026-07-27-third-leg-target-spec.md` §2.2, §2.4, §7.1, §7.5 | `6502c7c` 2026-07-27 | The screen amended here. §2.2 asserts *"Session filters are locked Pine properties, so free capacity is deterministic"* and derives a per-day free-cap table; §2.4 defines Slot 1 (Wed+Thu) and Slot 2 (Mon+Fri); §7.5 scores ORB-MNQ SCREEN-FAIL on five grounds |
| `docs/notes/rail_build/RUNBOOK.md:116` | read this session | Independent restatement of the payload semantics (*"entries carry `flatten_first=true` (re-fires cannot stack)"*; flat = *"`closeposition` **without** quantity"*) — corroborates the source read above |
| `docs/briefs/closures/SLR-MYM-1-closure-falsified-stage0.md` §4 F1 | 2026-07-29 | The originating finding |

**Scope note on the read.** The payload is keyed on **`account` + `instrument`**. Everything below is therefore scoped to *the same account*; it says nothing about two strategies on the same symbol in **different** accounts (the separate-eval fork, spec §8), nor about two strategies on **different** symbols in the same account.

---

## §1 — Context

The ratified third-leg screen models same-account contention as a **contract-capacity** problem: §2.2 computes free micros per weekday from the incumbents' locked session filters, and §2.4 derives two admissible slots from that table. Every S-requirement in §7.1 is about venue rules, compliance, and cap.

`SLR-MYM-1` was screened against exactly that surface, passed the cap arithmetic on Mon/Wed/Thu/Fri, and was only then found to be structurally impossible on two of those days — for a reason the screen does not model. Both the incumbent Striker DJ30→MYM leg and the candidate resolve to the **same order symbol `MYM1!`**, and our own rail's payload construction makes two strategies on one symbol **destructively interfere**:

- A second strategy's **entry** carries `flatten_first=true` → it **closes the incumbent's open position** before entering.
- A second strategy's **exit** issues `closeposition` with **no quantity** → it flattens **whatever is open**, including the incumbent's position.

This is not a sizing bug to be fixed downstream, and it is not contingent on venue netting semantics — it is a property of the rail as built, and it is bidirectional. Contract cap is divisible; an open position is not.

**Decision driver (one sentence):** the screen's whole purpose is to reject a candidate before K or spend, and it currently passes candidates that cannot physically coexist with the incumbent book — so cap arithmetic must be joined by a symbol-occupancy limb.

---

## §2 — Decision

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

**2-C. §2.4 Slot 2 narrowed.** Slot 2 (Mon + Fri) was derived on cap grounds alone. Under S7 it is **unavailable to a candidate on an occupied symbol**: the incumbent MNQ leg can fire **Monday**, and the incumbent MYM leg can fire **Friday**. Slot 2 therefore survives **only for a candidate on an unoccupied symbol**. Slot 1 (Wed + Thu) is **unaffected** — neither incumbent can fire on those days, so no symbol is occupied.

**2-D. §7.5 negative control gains a sixth failing row.** ORB-MNQ-1 trades **MNQ daily**; the incumbent Striker NAS100→MNQ leg can fire **Mon and Tue**. ORB therefore **fails S7** in addition to S5, R1, R3, M2 and the S4 directionality question. The known-bad candidate is re-rejected by the new limb, which is the non-vacuity check this ADR owes.

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

> ⚠ **READ FIRST — both empirical limbs DORMANT (Rule 11; 2026-08-06).**
> §4 text below is **byte-unchanged**; §6 Consequences is a frozen dated body and is **not** edited.
> **(a) Dormant limbs:** false-positive and false-negative.
> **(b) Why the input cannot accrue:** the false-positive limb needs demonstration
> "on the venue, not in argument"; the false-negative limb needs a dry-fire or live
> session; the third trigger names a mooted B7 sequence — none can accrue while no
> leg is deployed at any venue.
> **(c) Re-arm condition:** F3 registers a venue **and** a leg is deployed there.
> **(d) Surviving coverage:** calendar checks (2026-11-08, 2027-02-08) still convene
> but can only **record** the falsifier as unreachable — *do not read an unfired
> calendar check as evidence the limb held.*
> Slot-2 narrowing is **not** shown dead (symbols retained-not-released under O-B / F2).
> Full record: §Addendum 2026-08-06.

> ⚠ **2026-08-14:** the "retained-not-released" sentence in the banner above is **superseded** — see Addendum 2026-08-14. The dormancy record for both empirical limbs stands. S7 is untouched.

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

**Negative (real).** Slot 2 is materially narrowed for same-symbol candidates, so the admissible design space on MYM/MNQ shrinks to Slot 1 (Wed+Thu, ~104 sessions/yr) — and the spec already flags that slot's session count as a **power** constraint. For an occupied symbol, S7 and the Clause-N power floor now squeeze from both sides; SLR-MYM died in exactly that squeeze. This is an honest narrowing of what the same-account fork can host, not a cost this ADR introduces.

**Risk.** The decisive read is our own payload construction, not a venue-published rule. If CrossTrade/Tradovate semantics differ from what the payload implies, S7 could be over-broad — that is the §4 false-positive limb, and the cheap way to settle it is an attended dry-fire observation, not an argument.

---

## §7 — Implementation

- **Phase 0 — DONE 2026-07-29.** This ADR authored on a verified production read.
- **Phase 1 — DONE 2026-07-29.** Spec amended: S7 added to §7.1; §2.2 sufficiency correction; §2.4 Slot-2 narrowing; §7.5 negative control gains the S7 row; spec header records this ADR as amending-in-part.
- **Phase 2 — owed at next use.** The next third-leg proposal scores S7 explicitly in its §7.1 table. No retroactive re-scoring is owed: the only prior candidates are ORB-MNQ (already SCREEN-FAIL on five other grounds) and SLR-MYM (closed).
- **Phase 3.** §4 checks ride the programme-audit dates.

---

## §10 — Audit hooks (runnable)

```bash
# The decisive production read -- if either changes, re-derive S7 (or revert it)
grep -n "flatten_first=true" ops/c1_rail/crosstrade_payload.py
grep -n "command=closeposition" ops/c1_rail/crosstrade_payload.py
grep -n "Omitting quantity lets closeposition flatten" ops/c1_rail/crosstrade_payload.py

# The host still keys on leg_id and still has no symbol-collision concept
grep -n "leg_id not in LEG_MAP" ops/c1_rail/c1_sizing_host_reference.py
grep -c "symbol" ops/c1_rail/c1_sizing_host_reference.py   # expect 0 symbol-collision logic

# S7 landed in the spec and the negative control re-fails on it
grep -n "S7" docs/spec/2026-07-27-third-leg-target-spec.md
grep -n "six independent grounds\|FAIL — MNQ1! occupied" docs/spec/2026-07-27-third-leg-target-spec.md

# Occupancy is defined by which legs CAN fire -- the incumbent session map
grep -n "Mon | MNQ\|Tue | MYM + MNQ\|Fri | MYM" docs/spec/2026-07-27-third-leg-target-spec.md

# 2-E: the unoccupied-symbol escape must remain true (LEG_MAP holds only the two incumbents)
grep -n "LEG_MAP: dict" -A 12 ops/c1_rail/c1_sizing_host_reference.py | grep -c "MYM1!\|MNQ1!"
```

---

## Verification

```bash
python scripts/check_brief.py docs/adr/2026-07-29-third-leg-symbol-occupancy-limb.md --type adr
python ~/.claude/skills/brief-authoring/scripts/check_brief.py docs/adr/2026-07-29-third-leg-symbol-occupancy-limb.md --type adr
python scripts/check_adr_graph.py
python scripts/check_path_liveness.py

# §0 anchors
git log -1 --format='%h %ci' -- ops/c1_rail/crosstrade_payload.py            # 54b1489
git log -1 --format='%h %ci' -- ops/c1_rail/c1_sizing_host_reference.py      # c134060
git log -1 --format='%h %ci' -- docs/spec/2026-07-27-third-leg-target-spec.md
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-29 | Authored and `Accepted` on operator directive ("amend the third-leg spec with the symbol-occupancy limb"), following the SLR-MYM-1 closure's F1 finding. Decisive evidence is a production read of `ops/c1_rail/crosstrade_payload.py` (`flatten_first=true` on entries; quantity-less `closeposition` on exits, both keyed account+instrument) — stronger and more checkable than the venue-netting argument F1 originally rested on. | Joshua (direction) + Claude Code |

## Addendum 2026-08-06 — §4 empirical limbs DORMANT (Rule 11; claim-alignment M29)

**Type:** back-propagation under operational-rules **Rule 11** (retirement / de-scope events
back-propagate to standing falsifiers). **§4 wording and §6 Consequences are not edited.**

### (a) Dormant limbs

Both empirical limbs of §4 (false-positive; false-negative).

### (b) Why the input cannot accrue

- **False-positive** — requires demonstration *on the venue, not in argument* that two strategies
  can hold independent positions on one symbol in one account under the rail as configured.
- **False-negative** — requires a dry-fire or live session exhibiting destructive interference
  after an S7 pass.
- The trigger schedule also names any B7 session that routes a non-incumbent leg — the B7
  sequence that would have supplied that path is **mooted** by the 2026-08-04 venue de-scope.

With both Striker legs withdrawn and no successor venue registered, **none of those inputs can accrue**.

### (c) Re-arm condition

Fork **F3** registers a venue **and** a leg is deployed there. The limbs do not re-arm by
argument, by calendar alone, or by research-only Tradeify-shaped work.

### (d) Surviving coverage

Programme-audit calendar checks (2026-11-08, 2027-02-08) still convene. While dormant they
may only **record** that the falsifier was unreachable. **Do not read an unfired calendar
check as evidence the limb held.**

> ⚠ **2026-08-14:** the "retained-not-released" sentence below is **superseded** — see Addendum 2026-08-14. S7 is untouched.

### Out of scope

The Slot-2 narrowing (same-symbol design space) is **not** shown dead — incumbent symbols
remain **retained-not-released** pending F2; this addendum does not free `MYM1!` / `MNQ1!`.

| Date | Change | By |
|---|---|---|
| 2026-08-06 | Addendum 2026-08-06 — Rule-11 dormancy record for both empirical §4 limbs; Status gloss; §4 READ FIRST banner. §4/§6 bodies byte-unchanged. | claim-alignment Phase 2 (M29) |

## Addendum 2026-08-14 — MYM1!/MNQ1! "retained-not-released" superseded

**Type:** dated correction under Rule 14. **§2 S7 requirement and §4/§6 bodies are not edited.**

Addendum 2026-08-06's "Out of scope" asserted incumbent symbols remain **retained-not-released** pending F2, and that the addendum does not free `MYM1!` / `MNQ1!`. That occupancy-posture claim is **superseded** by [`2026-08-12-msl-mym-occupancy-release.md`](2026-08-12-msl-mym-occupancy-release.md): `MYM1!`/`MNQ1!` occupancy is released for **new non-Striker** research. This is not a full release — withdrawn Striker legs stay barred (de-scope clauses 1–2; occupancy-release Boundary). S7 remains live, generally-applicable doctrine (cited by [`2026-08-02-third-leg-liveness-limb.md`](2026-08-02-third-leg-liveness-limb.md)).

The 08-06 Rule-11 dormancy record for both empirical §4 limbs is **not** reopened by this addendum.

| Date | Change | By |
|---|---|---|
| 2026-08-14 | Addendum 2026-08-14 — 08-06 "retained-not-released" superseded by occupancy-release ADR; S7 untouched. | claim-alignment reconciliation |

