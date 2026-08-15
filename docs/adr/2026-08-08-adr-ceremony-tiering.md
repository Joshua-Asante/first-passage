# ADR 2026-08-08 — Stakes-tiered ADR ceremony: full apparatus only where stakes are

**Status:** `Accepted` — ratified by operator (JA) 2026-08-08 after the 118-ADR retrospective sweep (annex in session; limb-3 deletion amendment + ⅕ falsifier calibration applied pre-ratification)
**Decision date:** 2026-08-08
**Authors:** Joshua (direction: "conventions may be introducing undue friction") + Claude Code (measurement + draft)
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Related:** [minimal-spec template](../spec/TEMPLATE-minimal-spec.md) (ratified 2026-08-07 — this ADR extends that style from specs to low-stakes decisions) · [W5 governance diet](2026-08-07-w5-governance-diet.md) · [root-doc charter](2026-07-16-root-doc-charter-dedup.md)
**Layer:** governance convention. **$0 / K=0.** Applies forward only; no existing ADR is rewritten.

**Reads (2026-08-08, this worktree):** `docs/adr/` census — 119 ADRs, monthly 8→15→22→46→26 (Aug = 7 days), 10/26 August ADRs are `$0/K=0` · `scripts/check_adr_graph.py:31` — required header fields enumerated; unknown fields tolerated · `docs/spec/TEMPLATE-minimal-spec.md` — ratified minimal form, but "ratification still runs through an ADR" · pre-commit battery timed 137 s.

## Decision

**Tier test.** A decision gets the FULL template (§0–§7) iff any limb holds:

1. Spends K or money (research runs, venue fees, live orders).
2. Touches a live-risk surface: `dd_protection`, allocations, lifecycle state, arming/`dry_run` invariants, spend ceilings, or a `firm_rules` field consumed by sizing or by an open fork.
3. Alters a LOCKED/frozen surface (Pine, locked params, frozen prereg) — including via supersession — or irreversibly deletes a non-regenerable surface (vendor data, production-code estates). *(Amended 2026-08-08 after the retrospective sweep: deletion ADRs like the substrate retirement and the bar-data wipe were light by the original letter — wrongly.)*
4. Creates or amends doctrine: a rule, gate, falsifier threshold, or convention that binds future work.

Otherwise it is a **LIGHT decision record**: same file location, same header field block (keeps `check_adr_graph` green), plus `**Tier:** light`, body capped at **300 words** in the minimal-spec style —

```
Decision: <≤3 sentences>          Grounds: <links, never retellings>
Reads: <path> @ <anchor> · …      Gate: <binary, or "none — record only">
Boundary: <genuinely tempting forbidden move, or "none">
```

**Escalation.** Ambiguous tier → FULL. A light record later found to gate a full-tier matter is **superseded by a full ADR** (marker: `escalated-from-light`), never padded in place. Rule 0 is tier-independent — the read always happens; only the table format is dropped.

This ADR is limb-4 full-tier, written compact deliberately: ceremony is the six discipline checks, not the word count.

## Falsifier

**H:** ≥⅕ of post-ratification ADRs land light-tier with no loss of decision recoverability. *(Calibrated to the measured retrospective base rate — 22/118 ≈ 19% of the existing corpus classifies light; the original ⅓ draft figure sat above base rate and risked an unreachable gate.)*

**FALSIFIED if:** two dated incidents where a light record's omitted apparatus (falsifier / forbidden moves / §0 table) is causally implicated in a wrong downstream action or a re-litigated decision. **RESOLVED at** the first quarterly programme audit after 2026-08-08 if light share ≥⅕ and zero such incidents; **AMBIGUOUS** (extend one quarter) if fewer than 6 light records exist by then.

## Forbidden moves

- Classifying a limb-1/2/3 decision light "because the change is small" — size ≠ stakes.
- Using the light tier to skip the Rule 0 *read* (vs. the table).
- Retro-converting existing full ADRs to light.
- Padding light records back toward full — the 300-word cap is a cap.

## Gate

**RESOLVED** when: operator ratifies + first light record lands with gate battery green + falsifier review passes at the audit above. Binary per §Falsifier.

## Audit hooks

```bash
grep -rl '^\*\*Tier:\*\* light' docs/adr/ | wc -l                      # adoption count
for f in $(grep -rl '^\*\*Tier:\*\* light' docs/adr/); do awk '/^## /{b=1} b{w+=NF} END{print w, FILENAME}' "$f"; done   # ≤300-word body cap
grep -rn 'escalated-from-light' docs/adr/                              # escalation incidents
```

## Addendum 2026-08-14 — Candidate omitted-apparatus incident (implied-SR)

**Dated note (audit corpus; does not amend §Decision / §Falsifier).** Two post-ratification light records each created or amended a binding assumed-edge admission gate — ceremony-tiering **limb 4** ("creates/amends doctrine — a rule, gate, falsifier threshold, or convention that binds future work") — and were reversed within days by a full-tier ADR that itself cites "limb 4 fires: amends a gate":

- [`docs/adr/2026-08-10-implied-sr-plausibility-gate.md`](2026-08-10-implied-sr-plausibility-gate.md) (body under [`docs/ltm/adr/`](../ltm/adr/2026-08-10-implied-sr-plausibility-gate.md)) — light; promoted `implied_annualized_sr` to a freeze-time gate and closed the fade design-region.
- [`docs/adr/2026-08-12-msl-implied-sr-disclosure-not-kill.md`](2026-08-12-msl-implied-sr-disclosure-not-kill.md) (body under [`docs/ltm/adr/`](../ltm/adr/2026-08-12-msl-implied-sr-disclosure-not-kill.md)) — light; interim amend of the MSL pre-G0 kill wiring.
- Reversal: [`docs/adr/2026-08-13-implied-sr-report-only-fade-reopen.md`](2026-08-13-implied-sr-report-only-fade-reopen.md) (full; demotes to report-only, reopens fade geometry).

Bodies of the two light records are **not** rewritten (this ADR is forward-only). Surfaced as a **candidate incident** against this ADR's two-incident FALSIFIED threshold (§Falsifier). Whether the pair counts as one incident or two is an operator/audit call at the first quarterly programme audit after 2026-08-08. Forward pointer: [`STATE.md` §2026-11-08](../../STATE.md).
