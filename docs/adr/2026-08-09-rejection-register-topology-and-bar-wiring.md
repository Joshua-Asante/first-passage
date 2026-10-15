# ADR 2026-08-09 — Rejection-register topology + the ratification-and-wiring rule

**Status:** `Accepted` — ratified by operator (JA) 2026-08-09, in-session direct instruction ("make your best calls on The SNAG register…"); D2 channel (c), explicit owner adjudication
**Decision date:** 2026-08-09
**Authors:** Joshua (direction) + Claude Code (measurement + draft)
**Supersedes:** `2026-06-14-rejected-candidate-patterns.md` in part - registry topology only.
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Revision:** 2026-10-15 — retention trim (ADR decay audit; operator direction 2026-10-15): §0 read detail (one decisive read kept), D5 per-correction detail, §7 implementation plan, §10 hooks other than the two D2 machine-consult checks, and the Verification block removed; D3's gate-tier claim, D4's §7 pointer and §6's hardening pointer corrected to what landed. No decision text changed. Pre-trim text at blob `0f4627ba1ea02dc24c5922e26528214da3e1a95a` (commit `4121e84c95f4990b71962e3b9570c4c3fad88426`).
**Related:** [`three-loop binding`](2026-06-12-three-loop-methodology-binding.md) (D4 add-back metric reads these registers) · [`GRAND tier`](2026-08-09-grand-tier-quintessentials-binding.md) (pursuit-layer sibling; this ADR is object-layer) · [`closure enforcement`](../../scripts/README.md#closure-enforcement) (the gate that checks closures) · [`2026-08-08 quarterly audit`](../notes/audits/programme-audit/2026-08-08-quarterly-audit.md) §1.2 diagnostic 4 (the RED this ADR answers)
**Layer:** governance convention + object-layer register topology. **$0 / K=0.** Tier: **FULL** (ceremony-tiering limb 4 — amends doctrine binding future work).
**Loop-of-Record:** STRATEGIC — this rules which register carries kill-record authority, i.e. governance of a stopping rule. D2 channel (c).

---

## §0 — Rule 0 reads (executed 2026-08-09, this worktree, all re-verified by an adversarial pass)

- `docs/rejected_candidates.md` read in full (anchor `baaab64` 2026-08-08), with `ops/instruments/profiles.json`, `python scripts/instrument_profiles.py cell MNQ ict-liquidity` (prints `BINDING BAR: index-intraday-ohlcv-directional-timing-2026-07-21` and blocks), the 2026-07-01 portfolio audit, the 2026-08-08 quarterly audit, `scripts/gate_manifest.py --list` and the `ops/instruments/MNQ.md` DEAD table. Per-read findings are at the pre-trim blob (see **Revision:**).

---

## §1 — Context

The 2026-08-08 quarterly audit graded the object layer **Degenerating** with diagnostic 4 (SNAG) **RED**:
*"repair authored, never operator-ratified, and `rejected_candidates.md` stopped being fed 2026-08-03 —
exactly when the densest kill run in estate history began (~15 campaigns, zero entries). Both stopping
rules non-operative."*

Measurement confirms the shape of the finding and **refutes one of its two limbs**:

1. **Feed:** the last entry landed `9b5ce43` 2026-08-03; nothing since. Confirmed. (That final entry is
   itself, by its own text `:364-369`, a **deployment-target** rejection explicitly *"NOT a mechanism
   rejection"*, which deliberately withheld its dedup record.)
2. **Ratification:** confirmed absent, and the contrast lives inside the file — both *later* domain
   entries carry operator stamps; the *mandated* one does not.
3. **Kill volume:** ~15–21 terminal-negative closures in the window depending on whether un-Q'd cheap
   falsifiers, never-ran power voids, and second dispositions of the same campaign are counted. The
   audit's "~15" is defensible; "densest kill run in estate history" is if anything understated.
4. **"Both stopping rules non-operative" is half wrong.** The **per-direction** rule is non-operative —
   confirmed, and worse than stated: *no gate enforces it at all*. The **domain** rule is **operative
   and machine-enforced**: four in-window pre-registrations read it by line number and argued past it,
   and `instrument_profiles.py` blocks on it today.
5. **The kills were not unrecorded.** They were routed to `ops/instruments/<SYM>.md` DEAD tables — a
   *competing* register that **was** fed through the window and whose rows carry the same
   re-proposal-bar discipline. The estate has three rejection surfaces
   (`rejected_candidates.md`, the instrument ledgers, `rejected_signals.md`) and **no ruling on which
   owns what**. That, not "the register stopped being fed", is the real defect.

**The pattern that explains it all — ratification and machine-wiring co-occur.** The 2026-07-21 raised
bar was ratified, got wired into `profiles.json`, and fires. The 2026-08-02 raised bar was ratified. The
2026-07-01 SNAG closure was never ratified, is wired into nothing, and has **zero recorded consults**.
An unratified bar is inert prose regardless of how well argued it is.

**Decision driver:** the audit ordered a mandatory repair whose authoring half was done and whose
ratifying half was not, and the missing half is precisely the half that determines whether a rule binds.

---

## §2 — Decision

**D1 — The 5th-leg / portfolio-expansion SNAG closure is RATIFIED**, effective 2026-08-09, stamped in
the same form as its two siblings. This discharges the 2026-07-01 audit §5.3 mandate.

**D2 — The ratification-and-wiring rule (new doctrine).** A domain-level bar is **operative** only when
both hold:
1. it carries an explicit **operator ratification stamp** with a date; and
2. it is **wired into a machine consult** — for instrument-scoped bars, an entry in
   `ops/instruments/profiles.json` whose `source` resolves to the bar's text.

A bar meeting neither is **inert prose and must not be cited as a binding constraint**. Authoring a bar
is a proposal; ratification+wiring is what makes it a stopping rule. *(Evidence: the two ratified bars
fire at a tier=always gate; the unratified one had zero consults across the estate's densest kill run.)*

**D3 — Register topology (rules the trifurcation).**

| Register | Owns | Machine consult |
|---|---|---|
| `ops/instruments/<SYM>.md` DEAD/REJECTED + `profiles.json` | **Per-direction, instrument-scoped** mechanism rejections | `instrument_profiles.py` (gate `instrument-profiles`: path-conditional on `ops/instruments/` at pre-commit, unconditional in `make check`/CI; the `cell` consult exits 1 on a binding bar) |
| `docs/rejected_candidates.md` | **Domain-level and cross-instrument** bars — the tier with no per-instrument home | via `profiles.json` `source` pointers |
| `docs/methodology/rejected_signals.md` | **Meta-layer** methodology signals (unchanged) | none; reviewed qualitatively at methodology audits |

**Consequence for the audit's owed-set.** Under D3 the ~7 genuine mechanism rejections in the
2026-08-03→09 window (MNQPOOL-1, Q-WLEGB-1, MNQFLOW-1, MNQFVG-1, Q-MNQDTL-CON-1, Q-R2AGRUN-1,
Q-ICT-MNQ-1) belong in the **instrument ledger**, which is where they were in fact written and where the
machine consult reads. **They are discharged there; they are not back-transcribed** into
`rejected_candidates.md`. The ~8 catalogue/cell nulls (the Route-B ρ-screens, whose own closures say
*"reopen = new G0"*, plus Q-OFCHAN-1 which died on 7.36% coverage — a measurement pathology, not
strategy grounds) and the ~6 power-voids/scoping-STOPs are **not registry-owed under the file's own
`:5` admission criterion**. The "zero entries" figure is therefore a **routing artifact, not a
discipline collapse** — with one real residual: ledger coverage is itself partial (see D4).

**D4 — The per-direction feed gets an enforcement instrument or an honest downgrade.** Rule (1) is
currently enforced by nothing. Until an instrument exists, no artifact may cite the per-direction feed
as an operative stopping rule. Building the check (does every terminal-negative closure with a named
instrument have a ledger DEAD row?) was **owed and dispatched**; landed 2026-08-27/28 as `scripts/check_instrument_rejection_coverage.py` (gate `instrument-rejection-coverage`, audit tier, `--exit-zero` until clean) — [SSOT program](2026-08-27-ssot-data-lineage-remediation-program.md) Phase 1 Task 2.

**D5 — Corrections landed with this ADR:** three stale or false claims in `rejected_candidates.md` (:455 slate record, :557 dead-consumer preamble, :141-143 missed hard-gate consumer) corrected at their point of use 2026-08-09.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Back-transcribe all ~15–21 in-window kills into `rejected_candidates.md` | Would write ~8 catalogue-nulls and ~6 power-voids into a register whose own `:5` criterion admits neither, inflating it with non-mechanism content and degrading the dedup signal — the exact failure the 08-03 ORB entry's author avoided deliberately. |
| Declare `rejected_candidates.md` the sole register and migrate the ledgers into it | Inverts the machine consult: the ledgers are what `instrument_profiles.py` reads at a tier=always gate. Would trade a working enforcement path for a prose one. |
| Ratify the 5th-leg closure and stop there | Leaves the trifurcation unruled, so the next dense kill run routes arbitrarily again and the same RED recurs at 2026-11-08. |
| Status quo | Second consecutive cycle of the same RED; both later bars ratified while the mandated one sat inert. |

---

## §4 — Falsifiable hypothesis (this ADR's own falsifier)

**H:** **If** D2/D3 are load-bearing, **then** at the 2026-11-08 quarterly gate (a) every domain-level
bar cited as binding in any in-window pre-registration carries both a ratification stamp and a
`profiles.json` wire, **and** (b) every terminal-negative closure naming an instrument has a ledger
DEAD row within the window. **Otherwise** the topology is ceremony as implemented and routes to the
falsifier below.

**Falsifier:** the ADR is **FALSIFIED** if at 2026-11-08 either — a bar is cited as binding in a
pre-registration while carrying no ratification stamp or no machine wire, **or** the ledger-coverage
rate for in-window instrument-scoped terminal-negative closures is below 100% with no dated exception.
Disposition on falsification is a superseding ADR, not a silent loosening of D2.

**Trigger check schedule:** quarterly programme audit, next **2026-11-08**.

---

## §5 — Forbidden moves (each genuinely tempting)

- **Citing the 5th-leg bar as though it had been binding before today.** It was not — zero consults.
  Its force runs forward from 2026-08-09, and any retrospective reading of it as having gated in-window
  work is false.
- **Treating a DEAD-table row as automatically a mechanism rejection.** The MNQ table mixes kills,
  `NOT-KILLED`, `VOID-POWER-anticipated`, and K-accounting annotations under one heading with no typed
  disposition column. D3 assigns the register role; it does not certify every existing row.
- **Using D3 to skip the registry for a genuinely cross-instrument mechanism kill** because "the ledger
  is easier". The domain tier exists precisely for kills no single instrument owns.
- **Quietly widening `:5`'s admission criterion** to absorb catalogue-nulls so the feed looks alive. A
  fed-but-meaningless register is the graveyard forbidden-move #4 already names.
- **Reading this ADR as closing the SNAG question.** It rules routing and operativeness; whether the
  underlying *search domain* is exhausted is a separate audit verdict.

---

## §6 — Consequences

**Positive:** the audit's RED is answered with a mechanism rather than a backlog; the mandated repair is
discharged; a rule that determines whether *any* bar binds (D2) is now explicit and testable; three
stale/false in-file claims are corrected at their point of use.

**Negative (real):** D3 formalizes a two-home topology, so a reader must now know which tier a kill sits
in. Mitigated by the table in D3 and by `profiles.json` pointers being the single machine path.

**Risk:** MNQ carries the 2026-07-21 bar under `inherited_bars`, **not** `bars` — its binding is
transitive through the parent class. Editing that inheritance edge would silently unbind the instrument
at the centre of the estate's densest kill run. Flagged here; hardening landed: `inherited_bars()` in `scripts/instrument_profiles.py`, tested by `tests/test_instrument_profiles.py::test_cell_inherited_bar_from_family_parent_forces_exit_one`.

**Downstream artifacts updated in this commit:** `docs/rejected_candidates.md` (D1 stamp + three D5
corrections); `docs/pursuits/a3-mnq-discovery-pipeline.md` (the open concern this ADR resolves).

---

## §10 — Audit hooks (runnable, each quarterly gate)

```bash
# D2 — every registry-sourced bar in profiles.json resolves into a ratified block
python scripts/instrument_profiles.py check

# D2 — the machine consult still blocks on the wired bar
python scripts/instrument_profiles.py cell MNQ ict-liquidity   # expect: BINDING BAR + exit 1
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-09 | Initial authoring + ratification (operator in-session instruction) | Joshua + Claude Code |
