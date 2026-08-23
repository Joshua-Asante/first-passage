# Pre-registration — Q-INTAKEGOV-1 governance-coverage verdict gate

**Status:** FROZEN — operator GO 2026-08-23, committed before Phase 1 results are read into this file.
**Parent brief:** [`docs/briefs/Q-INTAKEGOV-1-intake-registry-governance-coverage.md`](../Q-INTAKEGOV-1-intake-registry-governance-coverage.md)
**Authored:** 2026-08-23 · Claude Code, operator-directed GO.

---

## §A — Why freeze before Phase 1

This Q's own Section 5 forbidden-move #1 bars accepting "written strict" doctrine text as
self-enforcing; the whole point of Phase 1 is a live mechanism probe, not a documentation read.
This file freezes the falsifiable hypothesis, the per-limb confirm/hold criteria, and the combined
gate table verbatim from the parent brief's own Section 4/Section 6 before any ledger file, dedup
query, or grep result is read.

## §B — Falsifiable hypothesis (verbatim from parent §4)

**H-INTAKEGOV**, combined across three limbs:

- **Limb B2 (self-report validation):** at least one ledgered `K_intrinsic` declaration,
  cross-checked against its own seed-manifest's "what we tried" prose or available commit
  history, is undercounted.
- **Limb D2 (dedup corpus coverage):** a mechanism-level (non-slug) keyword query against
  `check_advisor_dedup.py` for a construct killed only in a `docs/adr/` file (MNQ-ANALOGUE-1 or a
  six-lead P1-CF/P2-CF leg) returns zero or near-zero hits, while the same terms hit directly
  against `docs/adr/*.md`.
- **Limb C4 (re-proposal reactivity):** no hook or script touching `rejected_signals.md` /
  `rejected_candidates.md` does more than count entries, and `programme-audit/SKILL.md` names no
  re-examine/reconsider/revisit-shaped diagnostic.

## §C — Gate criteria (verbatim from parent §6)

| Verdict | Trigger condition | Disposition (typed) |
|---|---|---|
| RESOLVED | All three limbs `hold` | INTEGRATE — record self-report brake, dedup corpus, and re-proposal gate as evidence-checked and adequate for now; discharge B2/D2/C4 as audit-note-resident findings that did not reproduce under a live probe. |
| FALSIFIED | All three limbs `confirm` | STOP — the combined governance-coverage gap is live, not theoretical; name (do not open) successor decision packets: one per limb, each carrying its own remediation scope, for a separate operator GO. |
| AMBIGUOUS-HOLD | Limbs split (mixed confirm/hold), or any limb's check cannot be completed at $0 with available data | ITERATE — record the per-limb split verbatim; re-test only the still-open limb(s) at the next relevant touch (next discovery run for B2, next new seed for D2, next REJECTED-verdict-adjacent session for C4). |

No averaging into a single score. A limb that fails to confirm (no undercount found / dedup
returns real hits / a genuine re-examination hook exists) is scored `holds`, not folded into
`confirm`.

## §D — Execution plan (verbatim from parent §7 / §10, frozen before results)

- **B2:** `ls`/read every JSON manifest in `register_search.py`'s ledger dir (`discovery_manifests/`
  by default). For each closed run's declared `K`/`K_intrinsic`, open the run's own seed-manifest
  (prereg / params prose) and compare against enumerated axes/variants; where commit history
  exists, `git log` the relevant config file between search-start and freeze. Flag any run where
  the manifest/commit count exceeds the declared `K_intrinsic`.
- **D2:** run `python scripts/check_advisor_dedup.py --keywords "<MNQ-ANALOGUE-1 mechanism terms,
  no retired slug>"`; confirm zero/near-zero hits; then `rg` the same terms against
  `docs/adr/*.md` directly.
- **C4:** grep every audit note touching `rejected_signals.md`/`rejected_candidates.md` and check
  whether any hook does more than count entries; grep `.claude/skills/programme-audit/SKILL.md`
  for re-examine/reconsider/revisit language.
- Assert the verdict per §C, per-limb then combined.

## §E — Audit hooks (frozen, verbatim from parent §10)

```bash
python scripts/check_advisor_dedup.py --keywords "<MNQ-ANALOGUE-1 mechanism terms, no retired slug>"
rg -i "<same mechanism terms>" docs/adr/*.md
grep -rn "rejected_signals.md\|rejected_candidates.md" docs/notes/audits/
grep -n "REJECTED" docs/methodology/rejected_signals.md docs/rejected_candidates.md | wc -l
grep -inE "re-examine|reconsider|revisit" .claude/skills/programme-audit/SKILL.md
```

## §F — History

| Date | Event | Who |
|---|---|---|
| 2026-08-18 | Parent Pre-Q drafted (`OPEN — DRAFT (pre-lock)`) | Joshua + Claude Code |
| 2026-08-23 | Operator GO recorded in-session. This file FROZEN before Phase 1 results are read. | Joshua (GO) + Claude Code |
