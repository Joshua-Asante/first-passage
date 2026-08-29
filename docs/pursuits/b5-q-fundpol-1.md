# Q-FUNDPOL-1 funded-phase policy inheritance — PARK

**Class:** (b) parked lane · **Standing:** PARK
**re-entry:** F3 registers a successor venue → the thread's own note already states this requires
a fresh derivation, not this brief rescheduled
**expiry:** 2026-11-08 (converts to SUBTRACT absent explicit operator renewal — ADR §2.3)
**Aim served (if re-entered):** A1
**Residuals:** §1–§5 analysis retained as worked method (explicitly, in the thread's own dormancy
note); §8 pre-registration (K frozen = 4) and P1/P2 discharges stay unspent, not carried forward
to any successor — a fresh derivation starts its own K accounting
**Test applied:** already-dormant per its own §6 gate retirement (2026-08-04); this record supplies
the missing re-entry+expiry fields

**Ratified:** 2026-08-09 (GSUB-1 Phase 3)
**Source:** [`GSUB-1 inventory`](../briefs/GSUB-1-inventory-and-dispositions.md) row b5

> **RENEWED 2026-08-16 (once)** — elected with the state-policy packet's P2 mark (the packet's
> §7 conditional; [closure §2.4](../briefs/closures/STATE-POLICY-closure-resolved-p2.md)).
> **Corrected wake condition** (replaces the stale F3-successor clause, which S1's no-migration
> ruling made unreachable): re-enter when **Q-POLFRONT-1 reads positive on funded-relevant
> cells** OR **a candidate reaches funded-phase modeling**. Re-entry still requires the fresh
> derivation this record already mandates — the renewal keeps the worked method and the frozen
> A2 state-dependent arm warm, nothing more. **New expiry: 2027-02-08** (converts to SUBTRACT
> absent explicit operator renewal, ADR §2.3 unchanged).

> **Note 2026-08-29 (brief-decay-audit) — wake condition's first disjunct has no literal
> referent.** Verified against source:
> [`Q-POLFRONT-1`](../briefs/Q-POLFRONT-1-policy-augmented-seed-frontier.md) §6's frozen grid
> scores synthetic constant-R edge geometry against the **eval-phase** gate only (bust ≤3.0% /
> pass ≥50%) — zero funded-phase dimension. The brief's sole "funded" occurrence is its own §7,
> which names funded-phase policy inheritance as a fork explicitly **not** opened there and
> points back to this pursuit; [its closure](../briefs/closures/Q-POLFRONT-1-closure-resolved-quantified.md)
> carries zero "funded" mentions at all. So the first disjunct above — "Q-POLFRONT-1 reads
> positive on funded-relevant cells" — cannot fire as written; there is no funded-relevant cell
> for it to read. **Read the wake condition going forward as governed solely by the second,
> well-formed disjunct** — "a candidate reaches funded-phase modeling" — which has not fired.
> **This does not reopen b5: PARK stands, expiry 2027-02-08 unchanged.**
