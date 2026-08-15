# ADR 2026-08-09 — Rejection-register topology + the ratification-and-wiring rule

**Status:** `Accepted` — ratified by operator (JA) 2026-08-09, in-session direct instruction ("make your best calls on The SNAG register…"); D2 channel (c), explicit owner adjudication
**Decision date:** 2026-08-09
**Authors:** Joshua (direction) + Claude Code (measurement + draft)
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Related:** [`three-loop binding`](2026-06-12-three-loop-methodology-binding.md) (D4 add-back metric reads these registers) · [`GRAND tier`](2026-08-09-grand-tier-quintessentials-binding.md) (pursuit-layer sibling; this ADR is object-layer) · [`iterate-closure-exit`](2026-08-04-iterate-closure-exit-mandatory.md) (the gate that checks closures) · [`2026-08-08 quarterly audit`](../notes/audits/programme-audit/2026-08-08-quarterly-audit.md) §1.2 diagnostic 4 (the RED this ADR answers)
**Layer:** governance convention + object-layer register topology. **$0 / K=0.** Tier: **FULL** (ceremony-tiering limb 4 — amends doctrine binding future work).
**Loop-of-Record:** STRATEGIC — this rules which register carries kill-record authority, i.e. governance of a stopping rule. D2 channel (c).

---

## §0 — Rule 0 reads (executed 2026-08-09, this worktree, all re-verified by an adversarial pass)

- `docs/rejected_candidates.md` read in full — admission criterion `:5` ("at the close of any Pre-Q
  that closes FALSIFIED **on strategy grounds**, or… on SNAG-budget-exhaustion grounds"), per-direction
  bar `:3`, domain bar `:411-416`, 5th-leg SNAG closure `:418-455`, raised bars `:468`/`:482`.
  Anchor: `baaab64` 2026-08-08.
- `grep -i ratif docs/rejected_candidates.md` → **exactly two hits**, `:470` "**Operator-ratified
  2026-07-21**" and `:485` "**operator-ratified 2026-08-02**". The 5th-leg entry has **none**.
- `docs/notes/audits/programme-audit/2026-07-01-portfolio-audit.md` — `:153` Status
  "`PROPOSED verdict pending owner ratification`"; `:113` §5.3 "Owner: operator ratifies; CC authors";
  `:154` "SNAG repair (§5.3) is **mandatory** under signal #5".
- `git log -S 'Reviewed at the 2026-08-08 slate' -- docs/rejected_candidates.md` → only `13c01d0`
  (2026-07-01), the authoring commit — i.e. a forward instruction, never a record.
- `docs/notes/audits/programme-audit/2026-08-08-quarterly-audit.md` — grep `5th-leg|SNAG|rejected_candidates`
  returns only the diagnostic-4 RED cell (`:65`) and §4 (`:105`). **No review of the entry occurred.**
- `ops/instruments/profiles.json` — the only registry-sourced bar id is
  `index-intraday-ohlcv-directional-timing-2026-07-21`. Executed
  `python scripts/instrument_profiles.py cell MNQ ict-liquidity` → prints
  `BINDING BAR: index-intraday-ohlcv-directional-timing-2026-07-21 -> ../../docs/rejected_candidates.md`
  and blocks. Gate id `instrument-profiles`, **tier=always** (`scripts/gates.yml:91-92`).
- `ls validation/` → **No such file or directory**. Anchor for the dead-consumer finding below.
- `scripts/gate_manifest.py --list` → 15 gates. **None enforces the per-direction feed.**
  `check_closure_disposition.py` checks only Iterate-block tokens; `check_status_consistency.py`
  scans links; `check_advisor_dedup.py` is a manual CLI returning 0 unconditionally.
- `git log --since=2026-07-25 -- docs/methodology/rejected_signals.md` → one commit, `9c8fc83`
  2026-07-29; nothing in the 08-03→08-09 window.
- `ops/instruments/MNQ.md` DEAD/REJECTED table `:92-104` (13 data rows) + SESSION LOG `:119-134`;
  fed continuously through the window.

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
| `ops/instruments/<SYM>.md` DEAD/REJECTED + `profiles.json` | **Per-direction, instrument-scoped** mechanism rejections | `instrument_profiles.py` (gate `instrument-profiles`, tier=always) |
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
instrument have a ledger DEAD row?) is **owed and is dispatched, not assumed** — see §7.

**D5 — Corrections landed with this ADR** (each a `lesson_corrections_land_where_read` firing):
- `rejected_candidates.md:455` "Reviewed at the 2026-08-08 slate" — **false as a record**; rewritten to
  say what actually happened.
- `:557` the auto-append preamble still asserts in the **present tense** that
  `validation/concept_intake/feedback.py` appends and `dedup_check` reads it. `validation/` does not
  exist. The 2026-08-08 correction landed at `:138-149` — 400 lines above the place a future appender
  actually writes. Corrected **at the point of use**.
- `:141-143` names two live consumers and **misses a third that is a hard gate**: `instrument-profiles`
  (tier=always) resolves `source` paths into this file, so moving or deleting it **hard-fails CI today**.

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
at the centre of the estate's densest kill run. Flagged here; hardening is part of the §7 dispatch.

**Downstream artifacts updated in this commit:** `docs/rejected_candidates.md` (D1 stamp + three D5
corrections); `docs/pursuits/a3-mnq-discovery-pipeline.md` (the open concern this ADR resolves).

---

## §7 — Implementation plan

- **Phase 0** — §0 reads (done, adversarially re-verified).
- **Phase 1** — land D1 stamp + D5 corrections in `rejected_candidates.md`; update the a3 pursuit record.
- **Phase 2** — the D4 enforcement instrument and the `inherited_bars` hardening are **dispatched as a
  separate packet**, not built here (they are code+tests, and this ADR is the ruling).
- **Phase 3** — verification block below; status `Accepted` on ratification (this commit).

---

## §10 — Audit hooks (runnable, each quarterly gate)

```bash
# D1 — the mandated repair carries its stamp (expect 3 hits, not 2)
grep -c -i "ratif" docs/rejected_candidates.md

# D2 — every registry-sourced bar in profiles.json resolves into a ratified block
python scripts/instrument_profiles.py check
grep -n "operator-ratified\|Operator-ratified\|RATIFIED" docs/rejected_candidates.md

# D2 — the machine consult still blocks on the wired bar
python scripts/instrument_profiles.py cell MNQ ict-liquidity   # expect: BINDING BAR + exit 1

# D5 — the dead-consumer claim is not restated at the point of use
grep -n "Read by dedup_check at call time" docs/rejected_candidates.md   # expect: empty
ls validation/ 2>/dev/null || echo "validation/ absent (expected)"

# risk — MNQ's bar binding is still present (direct or inherited)
python -c "import json;d=json.load(open('ops/instruments/profiles.json'));print(json.dumps(d,indent=1))" | grep -n "index-intraday-ohlcv-directional-timing-2026-07-21"
```

---

## Verification

```bash
python scripts/check_brief.py docs/adr/2026-08-09-rejection-register-topology-and-bar-wiring.md --type adr
python ~/.claude/skills/brief-authoring/scripts/check_brief.py docs/adr/2026-08-09-rejection-register-topology-and-bar-wiring.md --type adr
python scripts/check_adr_graph.py
python scripts/instrument_profiles.py check
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-09 | Initial authoring + ratification (operator in-session instruction) | Joshua + Claude Code |
