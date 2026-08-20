# Research Registry Analyst — Decision Log

Append-only. One entry per review. See
[design spec §5.3](../superpowers/specs/2026-08-18-loop-persona-hierarchy-design.md) for the format
contract and [`INDEX.md`](INDEX.md) for this persona's definition.

## 2026-08-19 — commits dd23588 / 72f8332 (the same-day governance-friction cut)

**Verdict:** CLEAR-WITH-CONCERNS -- one real CONCERN confirmed by independent search; one candidate
concern (archive-directory naming collision) checked and cleared.

**Confirmed findings:** 1 (CONCERN — `docs/notes/audits/2026-08-19-governance-friction-persona-panel-audit.md`
was minted without executing or citing the Rule 8 sub-rule 10 dedup-first attestation, despite the
same document approvingly citing sub-rule 10 elsewhere in its own text. The closest existing owner,
`docs/notes/audits/programme-audit/2026-08-15-governance-belt-meta-audit.md` — a formal
programme-audit-protocol run over the same meta/governance layer 4 days prior — was never named or
cross-referenced in either direction. Checked `git show dd23588` for any sub-rule-10 attestation
language: none found. The judgment call this attestation would have produced (new file is correct —
this is a lighter, non-programme-audit-protocol note on a narrower scope) is plausible and matches
local precedent, but was never made explicit or checked at authoring time, which is the actual
procedural failure sub-rule 10 exists to prevent regardless of whether the eventual call is right.)
Fixed in place, same day — the audit artifact now carries the attestation with real search output
and a stated disposition.

**Cleared, not a finding:** whether `docs/superpowers/specs/archive/` (new directory, created in
commit `dd23588`) collides with or duplicates the existing `docs/methodology/archive/` convention.
It doesn't — both are per-parent-directory `archive/` subfolders, the same already-established
pattern `docs/personas/archive/` (created in the same commit) also follows. Extending an existing
convention to a new parent directory is not a sibling-minting event sub-rule 10 governs.

**Cross-check against sibling review:** a separate Head of Governance pass on the same audit
document (`docs/personas/head-of-governance-log.md`) independently caught two other defects (an
off-by-one count, a timeline overstatement) but did not catch this dedup-attestation gap — passed
two prior review layers (self-synthesis, Head of Governance) uncaught until this pass.

**Ratified as recommended:** N/A — this is a retroactive test spawn of a persona archived same-day
for zero prior usage, not a real ratification-gate review; no proposal is submitted for accept/reject.

**Rehearsal:** yes — this is the first-ever spawn of this persona, run specifically to test whether
an archived-for-non-use seat would surface real value against existing repo evidence (per operator
instruction, "test them to see if they would earn their keep"). It found a real, previously-uncaught
dedup-discipline gap on first use — restored to `docs/personas/` on the strength of this result, per
`docs/notes/audits/2026-08-19-governance-friction-persona-panel-audit.md`. Marked rehearsal because
it did not run under this persona's own stated trigger (a dedup-first check arising in the normal
course of new-artifact authoring); it was operator-commissioned as a direct test, against work that
was already committed rather than pre-authoring.

**CRO hard block fired:** N/A — solo persona pass, not a wired multi-persona panel invocation.
