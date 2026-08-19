# Q-INTAKEGOV-1 — Does the discovery-intake and rejected-registry governance tooling actually cover what it is relied on to cover?

**Status:** `OPEN — DRAFT (pre-lock)` — execution requires a separate operator GO (parent-Q convention: naming is not opening)
**Authored:** 2026-08-18
**Closed:** N/A
**Authors:** Joshua + Claude Code
**Parent question:** N/A — opened from the assumption-sweep audit note
**Sub-questions opened:** none
**Loop:** Inquire-phase Pre-Q — closure gated on three $0 pure-read audits against the governance surfaces named in each limb
**Artifact path:** docs/briefs/Q-INTAKEGOV-1-intake-registry-governance-coverage.md

---

## Section 0 — Rule 0 reads (production-source verification)

- `docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md:56` — the family K-bank downgrade table: `K_banked(family)` goes from "hard gate; never softens" to "mandatory disclosure ... not a FAIL condition."
- `docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md:102` — §5 Forbidden Moves names "the single largest exposure created here" (quietly under-declaring `K_intrinsic`) and follows it with a procedural expectation only — "a pre-registration must enumerate every axis it varied" — no structural cross-check named. §6:123 cross-references this as an acknowledged Negative consequence ("`K_intrinsic` becomes a single point of failure for multiplicity control") without adding one.
- `docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md` amendment log, 2026-08-18 entry — the addendum confirmed live: closed Notice-phase manifests and Cap-seat spends now bank against the family tally (MNQ figure 6 + 14 + 1 = 21); explicitly changes **only how already-declared K gets summed**, not how `K_intrinsic` gets declared or checked.
- `lab/discovery/register_search.py:599-601` — `--search-space-size` (K) is a plain `type=int` CLI argument on `register open`, free-typed by whichever session runs it; no cross-check against a parameter grid, code diff, or session history anywhere in the file.
- `scripts/check_advisor_dedup.py:126-171` (`load_corpus`) — hardcoded five-surface corpus: `docs/briefs/closures/`, `docs/notes/audits/`, `docs/SESSIONS.md`, `lab/CATALOG.md`, `docs/rejected_candidates.md`. `docs/adr/` is not a member.
- `docs/methodology/strategy_harvest.md:85` — "Dedup first" instruction names exactly three surfaces (`rejected_candidates.md`, closed discovery manifests, `rejected_signals.md`); `docs/adr/` is absent here too.
- `docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md:240-324` — MNQ-ANALOGUE-1 killed here (pre-G0 falsifier, ratified 2026-08-15; disclosure + running kill-count table). The six-lead pursuit's P1-CF/P2-CF legs are ruled in a *different* ADR — `docs/adr/2026-07-15-external-mechanism-harvest-intake.md:166-202,368` (pre-admission cheap-falsifier FAIL, never reached intake-class status; its own dedup sweep at line 183 finds the one `rejected_candidates.md`-adjacent hit is actually `lab/CATALOG.md`, not the registry). Both constructs re-confirmed absent from `docs/rejected_candidates.md` directly this session — dead only in `docs/adr/` files, which the dedup script's corpus does not index.
- `docs/methodology/rejected_signals.md` — exactly two entries, both `REJECTED`, both carrying a "Re-proposal bar: a dated incident the existing machinery would have missed" clause (verbatim in the file's own intake-bar language), zero add-backs.
- `docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md:56` (cross-ref) — the lived precedent: `K_banked(family)` sat as an explicitly "never softens" hard gate for weeks before an operator-directed change surfaced it; not a scheduled re-check.
- `.claude/skills/programme-audit/SKILL.md:58,78,101,113,145,169` — seven diagnostic questions, all shaped to catch unauthorized *loosening* (belt-patches without corroboration, drifting falsifiers, rationalized revisions; question 5's own object-example names "a rejected candidate quietly re-proposed without new mechanism evidence" as the thing to catch, not license). No diagnostic is shaped to prompt reopening a standing `REJECTED` verdict. ⚠ One literal string hit exists — L101's "re-examine cadence" under the **Stable** disposition verdict (portfolio-audit continuity) — unrelated to the rejected-registries; a bare `grep -i re-examine` returns it as a false positive (see Section 10 hook, corrected).

---

## Section 1 — Context and motivation

This Q covers findings **B2**, **D2**, and **C4** of the 2026-08-18 assumption-sweep audit note (`docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md`). All three land on the same governance layer: the tooling and doctrine that is supposed to keep discovery intake honest and dead constructs dead. B2 is the multiplicity brake since the 2026-08-04 K-bank ADR converted a hard gate to disclosure-only, leaving `K_intrinsic` self-report as the sole remaining check. D2 is the dedup corpus's blind spot for `docs/adr/`, where dead constructs increasingly live. C4 is the reactive-only re-proposal trigger governing both rejection registries — a pattern the K-bank episode itself already lived through once. Standing doctrine tested: the K-bank ADR's own named "largest exposure," `strategy_harvest.md`'s dedup-first requirement, and the rejected-registries' re-proposal-bar convention.

---

## Section 2 — Prior art / lineage

- Cites the audit note directly: `docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md` §4 B2, D2, C4; §3 D-gate deletions did **not** remove any of these three (all three survived Verify with novel, uncited exposure).
- Adjacent but out of scope: §3 item 5 (Harvest Requirement 5's cost-law hurdle) is a different constant (`SLIPPAGE_TICKS_PER_SIDE`) already closed via Q-COSTGEO; not re-opened here. §4 A5 (M1 tree-skew audit gap) and D10 (INQHIORI canon staleness) are governance-coverage-shaped but scoped to the c1-rail and methodology-canon surfaces respectively — separate Qs if promoted, not folded in here to keep this brief's falsifiers uniformly $0 pure-read.
- The K-bank ADR's own 2026-08-18 addendum is read fresh per the supplied-findings note: it resolves *bookkeeping* (how declared K sums across Notice/harvest/Cap-seat lanes), not the *validation* gap this Q names (whether a declared K was ever true in the first place).

---

## Section 3 — Question (Q-INTAKEGOV-1)

**Pre-Q gate test (symptom-only rephrase):** Across the three surfaces that discovery intake and dead-candidate dedup rely on — the self-reported `K_intrinsic` multiplicity brake, the dedup corpus consulted before authoring a new seed, and the re-proposal gate on standing `REJECTED` verdicts — does each mechanism's actual reach match the reach it is credited with, or does each have a live, evidenceable gap between what it is relied on to catch and what it structurally can catch? No fix is named or implied.

---

## Section 4 — Falsifiable hypothesis (H-INTAKEGOV)

**H-INTAKEGOV:** Combined across three limbs —

- **Limb B2 (self-report validation):** at least one ledgered `K_intrinsic` declaration, cross-checked against its own seed-manifest's "what we tried" prose or available commit history, is undercounted.
- **Limb D2 (dedup corpus coverage):** a mechanism-level (non-slug) keyword query against `check_advisor_dedup.py` for a construct killed only in a `docs/adr/` file (MNQ-ANALOGUE-1 or a six-lead P1-CF/P2-CF leg) returns zero or near-zero hits, while the same terms hit directly against `docs/adr/*.md`.
- **Limb C4 (re-proposal reactivity):** no hook or script touching `rejected_signals.md` / `rejected_candidates.md` does more than count entries, and `programme-audit/SKILL.md` names no re-examine/reconsider/revisit-shaped diagnostic.

**If all three limb checks confirm** → the self-report brake is already leaking in practice (not merely theoretically exploitable), the dedup corpus has a real blind spot dead constructs are already falling into, and no scheduled symmetric process exists anywhere to catch either drift or a stale `REJECTED` verdict — i.e., "written strict" is not "enforced," on live evidence, not inference.
**If any limb check fails to confirm** (no undercount found / dedup returns real hits / a genuine re-examination hook exists) — that limb is scored `holds`, not folded into the combined verdict as failure.

**Reject H-INTAKEGOV if:** all three limbs confirm (undercount found; ADR-only dead construct returns zero/near-zero dedup hits; no re-examine hook found in either registry's consumers or in `programme-audit/SKILL.md`).
**Accept H-INTAKEGOV if:** all three limbs hold (no undercount in the sampled runs; dedup query returns real hits against the ADR-only construct; a genuine scheduled/symmetric re-examination mechanism is found).
**Ambiguous-hold if:** limbs split (some confirm, some hold) — record the per-limb split verbatim; no averaging into a single score.

---

## Section 5 — Forbidden moves

- **Treating "never softens" language anywhere in the current doctrine as self-enforcing because it is written strict.** This is the exact comfort the family K-bank episode already disproved — a written-strict rule with no scheduled check sat unexamined for weeks until an operator happened to bump into it, not because a mechanism caught it. Ruled out: this brief must test for a *mechanism*, not accept doctrine text as evidence of enforcement.
- **Reading the 2026-08-18 K-bank addendum as closing B2.** It is tempting because it is dated the same day and touches the same ADR — but it resolves summation bookkeeping across lanes, not whether a declared `K_intrinsic` was ever cross-checked against what was actually tried. Conflating the two would falsely close a limb that is still open.
- **Scoring `check_advisor_dedup.py`'s corpus gap by reading its source code alone.** Reading the five-surface list (§0) proves the *structural* gap; only running the actual `--keywords` query against a real ADR-only construct proves it *bites in practice* — the falsifiable H requires the latter, not just the code read.
- **Proposing to add `docs/adr/` to the dedup corpus, or a re-examination cadence to `programme-audit`, under this brief.** Both are tempting immediate fixes once the gaps are confirmed — but this is inventory + triage depth by design (rule 6 of this brief's authoring discipline); any remediation is a separate decision packet requiring its own operator GO, not smuggled into this Q's execution.

---

## Section 6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition (typed) |
|---|---|---|
| RESOLVED | All three limbs `hold` per Section 4 | INTEGRATE — record self-report brake, dedup corpus, and re-proposal gate as evidence-checked and adequate for now; discharge B2/D2/C4 as audit-note-resident findings that did not reproduce under a live probe. |
| FALSIFIED | All three limbs `confirm` per Section 4 | STOP — the combined governance-coverage gap is live, not theoretical; name (do not open) successor decision packets: one per limb, each carrying its own remediation scope, for a separate operator GO. |
| AMBIGUOUS-HOLD | Limbs split (mixed confirm/hold), or any limb's check cannot be completed at $0 with available data | ITERATE — record the per-limb split verbatim; re-test only the still-open limb(s) at the next relevant touch (next discovery run for B2, next new seed for D2, next REJECTED-verdict-adjacent session for C4). |

---

## Section 7 — Execution plan (self-executing, $0/K=0 — reuse the cheap-falsifier sketches supplied)

- Phase 0 — Rule-0 reads. Done (Section 0).
- Phase 1 — Limb B2: `ls`/read every JSON manifest in `register_search.py`'s ledger dir; for each run's declared `search_space_size`/`K_intrinsic`, open that run's own seed-manifest (per `docs/methodology/strategy_harvest.md` Section 5 template) and count enumerated axes/variants in its own prose; where a commit history exists, `git log` the relevant param/config file between search-start and freeze and count distinct parameter states touched. Flag any run where manifest/commit count exceeds declared `K_intrinsic`.
- Phase 1 — Limb D2: run `python scripts/check_advisor_dedup.py --keywords` with mechanism-level terms only (no retired slug) for MNQ-ANALOGUE-1's actual mechanism; confirm zero/near-zero hits; then `rg` the same terms against `docs/adr/*.md` directly to confirm the file that would have caught it sits outside every corpus the pipeline consults.
- Phase 1 — Limb C4: grep every audit note touching `rejected_signals.md`/`rejected_candidates.md` and check whether any hook does more than count entries (the known candidate is a bare `grep -c` census against the `REJECTED` heading); grep `.claude/skills/programme-audit/SKILL.md` for re-examine/reconsider/revisit language.
- Phase 2 — Verdict assertion per Section 6, per-limb then combined.

---

## Section 8 — Verdict pre-registration

Owed at operator GO, committed before Phase 1 executes. Not yet authored — this Q is named, not opened.

---

## Section 9 — Closure record format

Per `references/closure_record.md` (`.claude/skills/brief-authoring/references/closure_record.md`), with the mandatory typed Iterate block. `RESOLVED` → `docs/briefs/closures/Q-INTAKEGOV-1-closure-resolved.md`; `FALSIFIED` → `…-closure-falsified.md`; `AMBIGUOUS-HOLD` → `…-closure-ambiguous-hold.md` with the still-open limb(s) and re-test trigger named.

---

## Section 10 — Audit hooks (runnable)

```bash
# Limb B2 — K_intrinsic self-report vs actual axes explored (manual per-run read; no single command)
# ls/cat every JSON in register_search.py's ledger dir; open each run's seed-manifest
# (docs/methodology/strategy_harvest.md Section 5 template); count enumerated axes;
# where commit history exists: git log <config-path> --since=<search-start> --until=<freeze-date>
# Flag any run where manifest/commit count > declared K_intrinsic.

# Limb D2 — dedup corpus blind spot for ADR-only dead constructs
python scripts/check_advisor_dedup.py --keywords "<MNQ-ANALOGUE-1 mechanism terms, no retired slug>"
rg -i "<same mechanism terms>" docs/adr/*.md

# Limb C4 — reactive-only re-proposal gate
grep -rn "rejected_signals.md\|rejected_candidates.md" docs/notes/audits/
grep -n "REJECTED" docs/methodology/rejected_signals.md docs/rejected_candidates.md | wc -l   # census-only check
grep -inE "re-examine|reconsider|revisit" .claude/skills/programme-audit/SKILL.md              # expect exactly 1 (L101 "re-examine cadence" — Stable-verdict portfolio-audit continuity, not a REJECTED-reopening diagnostic; read the line, don't just count it)
```

---

## Verification

```bash
python scripts/check_brief.py docs/briefs/Q-INTAKEGOV-1-intake-registry-governance-coverage.md --type inquire

# Section 0 anchor spot-checks
sed -n '599,601p' lab/discovery/register_search.py
sed -n '126,171p' scripts/check_advisor_dedup.py
grep -n "Dedup first" docs/methodology/strategy_harvest.md
grep -n "K_banked(family)" docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md
grep -n "single largest exposure" docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md
grep -n "Re-proposal bar" docs/methodology/rejected_signals.md
```

---

## Pre-Lock Checklist (DRAFT briefs only)

- [x] Section 0 paths read with anchors
- [x] Section 3 passes the symptom-only rephrase
- [x] Section 4 hypothesis binary
- [x] Section 5 forbidden moves genuinely tempting
- [x] Section 6 triggers specific
- [x] Section 8 pre-registration owed at operator GO
- [x] Section 10 hooks runnable
- [ ] Operator GO owed before Phase 1 — this brief is named, not opened
