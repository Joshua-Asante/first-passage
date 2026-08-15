# Q-OBJCOHERE-1 — Verdict pre-registration

**Status:** `FROZEN` (operator-signed via ratification 2026-07-30, "I ratify OBJCOHERE-1. Proceed
with it"). No item below changes after any tension is adjudicated or any instrument-inventory row
is read — amendments require closing this pre-registration and opening a fresh one (Known Trap
#12). This file's commit strictly precedes any Phase 1 read.

**Parent brief:** [`docs/briefs/Q-OBJCOHERE-1-objective-coherence-audit.md`](../Q-OBJCOHERE-1-objective-coherence-audit.md)
**Frozen:** 2026-07-30

---

## §4 — Contradiction definition (verbatim from the parent brief)

**H-OBJCOHERE-1:** If the audit constructs **≥1 concrete decision object** (a candidate, rung,
allocation cell, or composition move, specified with actual numbers drawn from
currently-admissible ranges) for which **instrument A mandates disposition X and instrument B
mandates ¬X**, both instruments live and ratified, and **no ratified text assigns precedence**,
then the estate is objective-fragmented and the repair is a charter ADR draft (operator ratifies
or declines). Otherwise — every candidate tension, including T1–T4, resolves to an explicit
written precedence rule — the estate is coherent, the fragmentation clause of the thesis's H-EDGE
is FALSIFIED, and the correct output is the composition map alone (no charter).

**Definition notes (pre-committed, verbatim):** "live and ratified" = Accepted ADRs, RATIFIED
specs, and FROZEN operator-signed pre-registrations currently in force (the parent brief's §0 list
is the census; the audit may add to it but not subtract). "Contradictory dispositions" excludes
cases where one instrument is explicitly scoped out of the decision class (e.g. the fork-B ADR's
L46 scope clause already cedes admission) — those are precedence rules, and finding them is the
point.

**Constructibility clause:** a contradiction only counts if it is decidable **on paper** — i.e. the
decision object can be fully specified from numbers already in the estate (no new measurement, no
K>0). If deciding whether the contradictory case is reachable requires a new run, the tension goes
to `AMBIGUOUS-HOLD`, not `RESOLVED-INCOHERENT`.

---

## §6 — Gate table (verbatim from the parent brief)

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED-INCOHERENT` | ≥1 constructed decision object meets the §4 contradiction definition AND the precedence sweep for that pair comes back empty (sweep documented: artifacts searched, quotes absent) | Close; author charter-ADR **draft** enumerating the contradiction(s) + candidate precedence rules as operator options; thesis H-EDGE fragmentation clause CONFIRMED on the record |
| `FALSIFIED-COHERENT` | Zero constructible contradictions: T1–T4 and every audit-found pair each resolve to quoted precedence text in a ratified artifact — H-OBJCOHERE-1's fragmentation claim is falsified | Close; publish the composition map (instrument → decision class → precedence citations) as a standing reference doc; append falsification addendum to the thesis §4 |
| `AMBIGUOUS-HOLD` | Every unresolved tension lands in the "constructibility undecidable on paper" branch (needs measurement/K>0), and zero paper-decidable contradictions exist | Close AMBIGUOUS; record each blocked tension + the measurement that would decide it; re-test only if/when that measurement is separately authorized (no date — this brief creates no obligation) |

**Mixed-outcome precedence (pre-committed):** any single paper-decidable contradiction ⇒
`RESOLVED-INCOHERENT` regardless of how many other tensions are blocked or resolved. A mix of
`FALSIFIED-COHERENT`-class resolutions and `AMBIGUOUS-HOLD`-class blocks, with zero
paper-decidable contradictions, closes `AMBIGUOUS-HOLD` (not `FALSIFIED-COHERENT`) — coherence is
claimed only when nothing is left unresolved for a non-evidentiary reason.

---

## Fixed scope (frozen — cannot be widened after Phase 1 starts)

1. **Named tensions to adjudicate:** T1 (rung-vs-admission bust band), T2 (Stage-8
   necessary-not-sufficient), T3 (69/11 unpriced execution), T4 (envelope decorrelation-vs-hedging
   conflict) — all four as stated in the parent brief §1, verbatim.
2. **Instrument universe for the inventory + pairwise sweep:** `docs/adr/*.md` filtered to
   `Status: Accepted`, `docs/spec/*.md` filtered to `RATIFIED`, and pre-registrations filtered to
   `FROZEN` + operator-signed. No other artifact class (memory files, closures, notes) counts as a
   "live instrument" for the contradiction test — closures and notes may be read for context but
   cannot themselves be instrument A or B.
3. **Pairwise sweep is bounded, not open-ended:** candidate pairs are drawn only from rows sharing
   a decision class in the Phase-1 inventory table. No fresh literature or code search beyond that
   table.
4. **No new decision objects beyond what's constructible from currently-published numbers.** The
   §5 forbidden-move against "constructing T1's rung as a proposal" stands: the hypothetical is
   used only to test whether precedence text exists, never manufactured as a real candidate.

---

## Verification

```bash
$ git log --oneline -- docs/briefs/pre-registration/Q-OBJCOHERE-1-verdict-preregistration.md
# Expected: this commit predates any Phase 1 instrument-inventory or Phase 2 adjudication commit
```
