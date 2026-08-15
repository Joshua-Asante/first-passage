# Closure-disposition coverage limb — promote advisory to self-arming HARD — `2026-08-12-closure-disposition-coverage-hard`

**D-S-A domain:** meta-process (framework edit — gate-severity doctrine; no data-corpus or system-artifact D/S/A rides this)
**Loop-of-Record:** STRATEGIC — framework edit governing gate 14's coverage limb; ratified via operator adjudication (canon §14 channel (c)); no Delete verdict rides this.

**Status:** `Accepted` — ratified 2026-08-12 (operator GO); coverage limb self-armed HARD
**Decision date:** 2026-08-12
**Supersedes:** `2026-08-04-iterate-closure-exit-mandatory.md` in part — advisory-coverage clause only (docstring COVERAGE LIMB "never flips the exit code" / "Promote to HARD only after…")
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none

---

## §0 — Rule 0 reads (production-source verification)

Read before authoring, this session (2026-08-12), with `git log -1 --format='%h %cs' -- <path>` anchors:

- `scripts/check_closure_disposition.py` — anchor `052d4a98` 2026-08-09. Full docstring + coverage limb + `report_missing_closure_coverage` (always returned 0) + `OWNING_ADR` pointed only at the 2026-08-04 Iterate ADR. M-8 narrowness stated: mechanical token presence only; dropped C1/C4 in `check_status_consistency.py` named as proof that semantic completeness has no reachable gate. Self-arming severity: Proposed ⇒ WARN, Accepted ⇒ HARD. Coverage limb docstring named the promotion path this ADR is.
- `docs/adr/2026-08-04-iterate-closure-exit-mandatory.md` — anchor `029a546a` 2026-08-07. **Whole-file read** before superseding any part (adversarial-review-before-ratification). §2 item 6 owns Iterate-token enforcement + self-arming; §5 forbids retro-editing grandfathered closures and semantic gate expansion; no separate coverage-limb severity owner existed — coverage was added later as advisory (SESSIONS 2026-08-10d / commit `052d4a98`).
- `.claude/skills/brief-authoring/references/closure_record.md` — anchor `103365f5` 2026-08-11 (PR #755). Confirmed amended grammar: `**Closed:** YYYY-MM-DD` + `**Lane:** <F2|UNASSIGNED>` present on `origin/main` before this ADR was authored (precondition).
- `docs/notes/notice/N-2026-08-11-q-score-1-forward-fields.md` — anchor `103365f5` 2026-08-11. Dual-use note: Lane:/Closed: grammar also serves this promote-to-HARD ADR; notice does not author or ratify it.
- `docs/SESSIONS.md` entry `2026-08-11v` — PR #745 triage: backlog 9 → 0 (6 restored LTM pointers, 3 authored, 0 mislabels); declared coverage limb "ready for promote-to-HARD ADR".
- Cheap falsifier (this session): `python3 -X utf8 -c "…missing_closure_campaigns()…"` → **missing_count = 0** on `origin/main` at `587609f3` (post-#755). Promoting with a non-empty backlog would brick unrelated commits — falsifier held.

---

## §1 — Context

Gate 14 (`scripts/check_closure_disposition.py`) has two limbs. The typed-Iterate limb is already HARD (owning ADR `2026-08-04-iterate-closure-exit-mandatory` Accepted 2026-08-04). The coverage limb — campaigns claiming a terminal verdict in INDEX/CATALOG with no joinable closure under `docs/briefs/closures/` or `docs/ltm/briefs/` — shipped WARN/advisory by design (SESSIONS 2026-08-10d; `lesson_green_gate_is_not_coverage`; belt-churn YELLOW 2026-08-08). Its docstring deferred HARD promotion until (1) backlog clear and (2) an ADR supersedes the gate in part.

Both substance preconditions are now met: PR #745 cleared 9 → 0 and named this ADR as the next step; PR #755 merged the forward `Lane:`/`Closed:` closure-template amendment so any future date-aware reads (out of this ADR's scope) sit on the amended grammar, not the pre-amendment one. Leaving coverage advisory forever re-opens the blind spot the limb exists to close: Iterate can stay green while a campaign claims CLOSED with no record.

**Decision driver (one sentence):** the coverage blind spot is cleared and templated; the remaining risk is re-accumulation, which only a self-arming HARD limb prevents without a second wiring step.

---

## §2 — Decision

**Decision:** The coverage limb of gate 14 self-arms HARD from this ADR's Status token. Specifically:

1. **Severity owner split.** Iterate-token violations continue to read `OWNING_ADR` = `2026-08-04-iterate-closure-exit-mandatory.md`. Coverage violations read `COVERAGE_OWNING_ADR` = this file. Proposed ⇒ WARN + exit 0 for that limb; Accepted ⇒ HARD + exit 1 for that limb. Missing/unparseable ADR ⇒ that limb degrades to WARN (M-22 fail-open).
2. **What fires HARD (once Accepted).** A campaign ID that newly claims a terminal verdict (INDEX Open terminal Status; INDEX Recently closed; CATALOG Q-ID ∧ archive-owed/CLOSED/FALSIFIED/…) with no joinable closure filename under `docs/briefs/closures/` or `docs/ltm/briefs/`.
3. **Historical / grandfathered gaps stay excluded.** `COVERAGE_GRANDFATHERED` is the permanent forward-only boundary (same posture as the Iterate `GRANDFATHERED` filename set). Snapshot at authoring: **empty** — PR #745 cleared the backlog. A HARD fire on pre-promotion gaps would block unrelated work (the belt-churn concern the prior docstring recorded). Never append IDs to dodge; a genuine newly discovered pre-promotion gap requires a superseding ADR.
4. **Narrowness preserved (M-8).** This ADR does **not** add semantic completeness checks, does **not** enforce `Lane:`/`Closed:` header tokens (those are authoring-template grammar from PR #755; a separate decision would be needed to gate them), and does **not** reopen the dropped C1/C4 class.
5. **Arming is the Status flip.** Merging this ADR while `Proposed` lands the wiring and keeps coverage WARN. Operator ratification = flip Status to `Accepted` (and add the reverse `Superseded-in-part-by` on the 2026-08-04 ADR in the same commit). No second hook edit.

**Effective:** immediately upon acceptance (self-arming). Forward-only for coverage debt.
**Scope:** gate 14 coverage limb only. Iterate limb, grandfathered Iterate filenames, lab `RESULTS*`, and adjudication notes unchanged.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Keep coverage forever advisory | Re-accumulation is free; PR #745's clear is a one-shot. The docstring already named HARD promotion as the end state once backlog + ADR exist. |
| HARD-fire including historical gaps / no grandfather set | Belt-churn YELLOW concern is load-bearing — a latent pre-promotion ID resurfacing (or an INDEX prose join the limb newly recognizes) would block unrelated commits. Empty grandfather set + forbidden silent append is the safer boundary. |
| Single owning ADR (flip language inside 2026-08-04) | Silent in-place amendment of an Accepted ADR's enforcement clause is Trap-#12-adjacent; supersede-in-part keeps the Iterate decision intact and gives coverage its own arming token. |
| Also HARD-enforce `Lane:`/`Closed:` in this ADR | Out of scope — existence coverage ≠ header-token presence; mixing them conflates two failure modes and expands past the docstring's named promotion path. |
| Status quo until a Rule 15 | Paid incident class is already gated (Iterate); coverage is the same gate's second limb. A new numbered rule fails the rule-maintenance bar when a supersede-in-part + self-arming token suffice. |

---

## §4 — Falsifier (revert trigger)

**H:** once Accepted, the coverage limb prevents re-accumulation of terminal-verdict claims without closure records at near-zero marginal cost; grandfather emptiness stays honest (no silent dodge-appends); the limb does not become ceremony or friction theater.

**H is falsified — and this decision reverts (supersede in part or full) — if any limb below fires** (checked at the first methodology audit ≥3 months after acceptance, then quarterly with the Iterate ADR's §4 cadence):
- **Friction limb:** ≥2 legitimate commits resolve a coverage HARD fire by `--no-verify` or by appending to `COVERAGE_GRANDFATHERED` without a superseding ADR.
- **False-positive limb:** ≥2 HARD fires on campaigns that demonstrably have a closure record the join failed to see (filename grammar drift) — join is wrong, not the author.
- **Ceremony limb:** coverage stays green solely because authors stop writing terminal Status into INDEX/CATALOG (hiding closes) rather than filing closures — measured as ≥3 terminal closes evidenced only in SESSIONS/RESULTS with no INDEX/CATALOG claim in the same window.

**Revert action:** author a superseding ADR; never edit this decision text in place; never silent-append the grandfather set.
**Trigger check schedule:** ride the standing quarterly methodology-audit cadence; first eligible check = first audit ≥3 months post-acceptance.

---

## §5 — Forbidden moves (under this ADR)

- **Flipping Status to `Accepted` in the same PR that lands this ADR as a drive-by** — arming is a separate operator GO; the PR body must say so in plain language.
- **Appending campaign IDs to `COVERAGE_GRANDFATHERED` to clear a HARD fire** — dodge. A real pre-promotion gap needs a superseding ADR that extends the set with evidence.
- **HARD-firing on the Iterate `GRANDFATHERED` filename set for missing Iterate tokens via this limb** — orthogonal; those files count as closure *records* for coverage. Iterate exemption ≠ coverage exemption.
- **Adding semantic / `Lane:` / `Closed:` checks under this ADR's umbrella** — scope creep past M-8; separate ADR if those tokens become mechanical.
- **Editing the 2026-08-04 ADR's Iterate decision text in place** — this ADR supersedes only the advisory-coverage clause; Iterate §2/§5 stand.
- **Loosening §4 triggers without a superseding ADR** — Trap #12 at the methodology layer.

---

## §6 — Consequences

**Positive:**
- Terminal-verdict claims without a closure record re-accumulate under a HARD backstop once Accepted.
- Iterate and coverage severities arm independently — coverage can stay Proposed while Iterate remains HARD.
- Empty grandfather set + explicit forbid-append keeps the promotion honest after PR #745's clear.

**Negative (real cost):**
- One more Status token operators must remember when diagnosing gate 14 exits.
- A mis-joined filename (coverage false positive) can block unrelated commits once Accepted — mitigated by §4 false-positive limb + fail-open on missing ADR.

**Risks:**
- Authors hide closes from INDEX/CATALOG to dodge the limb (§4 ceremony limb).
- Premature Accept before a latent gap is found — mitigated by the live falsifier (missing_count = 0) at authoring and by keeping Status Proposed through merge.

**Downstream artifacts (this PR — constraint-scoped):**
- `scripts/check_closure_disposition.py` — `COVERAGE_OWNING_ADR`, `COVERAGE_GRANDFATHERED`, severity split, `report_missing_closure_coverage(hard=…)`.
- `tests/scripts/test_check_closure_disposition.py` — Proposed⇒WARN+0 / Accepted⇒HARD+1 / violating fixture fires.
- `docs/adr/INDEX.md` — regenerate to list this Proposed ADR.
- `docs/SESSIONS.md` — session entry (roll_sessions label); Open/next drops "promote-to-HARD ADR owed".

**Downstream deferred to Accept (not this PR):**
- `docs/adr/2026-08-04-iterate-closure-exit-mandatory.md` — add `Superseded-in-part-by: 2026-08-12-closure-disposition-coverage-hard.md — advisory-coverage clause` (pending while this ADR is Proposed).
- Pointer prose in `docs/notes/notice/N-2026-08-11-q-score-1-forward-fields.md`, `docs/briefs/closures/Q-SCORE-1-closure-falsified.md`, SESSIONS 11v/10d — historical narrative; no silent restatement of "advisory forever"; blast-radius: ruled unaffected until Accept changes the live claim.

**Gate (binary):** **RESOLVED** when Status is `Accepted`, the reverse `Superseded-in-part-by` is on the 2026-08-04 ADR, live `missing_closure_campaigns()` is still empty, and a violating fixture under `tests/scripts/test_check_closure_disposition.py` exits 1 with `HARD closure-disposition coverage:`. **FALSIFIED** if any §4 limb fires post-Accept. **AMBIGUOUS** is not a landing state for this promote — either the limb arms cleanly or a superseding ADR retreats.

---

## §7 — Implementation plan

- **Phase 0** — §0 anchors + missing_count=0 falsifier (done this session; precondition PR #755 on main).
- **Phase 1** — land this ADR as `Proposed`; wire checker + adversarial tests; regenerate ADR INDEX; SESSIONS entry.
- **Phase 2** — grep-sweep dispositions recorded in §6 (no out-of-constraint edits this PR).
- **Phase 3 (operator, separate commit/PR)** — flip Status → `Accepted`; add reverse `Superseded-in-part-by` on the 2026-08-04 ADR; re-run checker (expect exit 0 at Accept iff backlog still clear); gate self-arms.

---

## §10 — Audit hooks (runnable)

```bash
# Coverage ADR exists and is Accepted (limb armed)
python3 -X utf8 -c "
from pathlib import Path
import scripts.check_closure_disposition as c
print(c.adr_status(c.COVERAGE_OWNING_ADR))
print('grandfather_empty', c.COVERAGE_GRANDFATHERED == frozenset())
"
# Expected: Accepted / True

# Live coverage backlog still clear
python3 -X utf8 -c "
import scripts.check_closure_disposition as c
print(len(c.missing_closure_campaigns()))
"
# Expected: 0

# Checker self-run (coverage HARD-armed; exit 0 iff backlog clear)
python3 -X utf8 scripts/check_closure_disposition.py
# Expected: exit 0; no 'HARD closure-disposition coverage:' line while backlog empty

# Adversarial tests (violating fixture + both severity paths)
python3 -X utf8 -m pytest tests/scripts/test_check_closure_disposition.py -q
# Expected: all pass

# Reverse edge present after Accept
grep -n 'Superseded-in-part-by' docs/adr/2026-08-04-iterate-closure-exit-mandatory.md
# Expected: points at 2026-08-12-closure-disposition-coverage-hard.md
```

---

## Verification

```bash
python3 -X utf8 scripts/check_brief.py docs/adr/2026-08-12-closure-disposition-coverage-hard.md --type adr
# Expected: RESULT: well-formed

python3 -X utf8 scripts/check_adr_graph.py
# Expected: exit 0 (Proposed Supersedes edges pending — reverse check skipped)

python3 -X utf8 scripts/check_closure_disposition.py
# Expected: exit 0

python3 -X utf8 -m pytest tests/scripts/test_check_closure_disposition.py -q
# Expected: all pass
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-12 | Initial authoring (`Proposed`); checker severity split + adversarial coverage fixtures; grandfather set empty post-#745 | Cursor Cloud Agent |
| 2026-08-12 | **Ratified — Status → `Accepted`.** Coverage limb self-armed HARD; reverse `Superseded-in-part-by` on 2026-08-04 ADR same commit (§7 Phase 3) | Operator GO via task |
