# Q-TRAINKILL-1 — Are the train gates killing empty families, or killing true modest edges?

**Status:** `CLOSED` — `AMBIGUOUS-HOLD`
**Authored:** 2026-08-18
**Closed:** 2026-08-18
**Authors:** Joshua (operator GO: "GO on Q-TRAINKILL-1") + Cursor (execution)
**Parent question:** [`N-2026-08-18-iteration2-identify-notice`](../notes/notice/N-2026-08-18-iteration2-identify-notice.md) observation C / §5 packet 3
**Sub-questions opened:** none
**Loop:** Inquire-phase Pre-Q — closure gated on whether the joint kill record fits μ=0, μ=+0.10R, both, or neither
**Artifact path:** `docs/briefs/Q-TRAINKILL-1-train-gate-power.md`
**Pre-registration:** [`pre-registration/Q-TRAINKILL-1-verdict-preregistration.md`](pre-registration/Q-TRAINKILL-1-verdict-preregistration.md)

**D-S-A domain:** data (already-committed closure CIs → one joint likelihood)
**Pre-Q gate:**
```
D: deleted — (i) Q-EXPR-1's horizon-mismatch census [test: different unit;
   already closed]; (ii) admissibility deaths (WHO/Clause-N/Req-2) [test:
   observation B — other bottleneck]; (iii) reachability-audit family
   [test: different unit — can-the-gate-fire, not firing-rate]; (iv)
   CATALOG closed dates as n/CI evidence [test: duplicated by closures].
   No forbidden D-test.
S: each scored row collapses to (event, se). Compression preserves
   observation C (generous bar, nothing survives train).
A: g(0) vs g(0.10) vs 0.05. Q-cost is O(read the prereg + run the scorer).
```

---

## §0 — Rule 0 reads (production-source verification, executed 2026-08-18)

Worktree on `cursor/q-trainkill-1` at `dd2cc67` (Q-EXPR-1 close). Prereg
written **before** any n/CI substitute.

- `docs/notes/notice/N-2026-08-18-iteration2-identify-notice.md` — packet 3:
  three readings; set enumerated; μ=+0.10R; se = CI width/3.92; partial-table
  rule; no bar-lowering.
- `docs/SESSIONS.md` — GO-time sibling sweep (set frozen in prereg §A).
- `docs/notes/audits/2026-07-12-08-08-classA-reachability-audit.md` /
  `2026-07-12-disccamp0-gate-reachability-audit.md` — adjacent prior
  (can-fire / binds), not this unit.
- `docs/spec/2026-08-08-tradeify-necessary-conditions-target-spec.md` —
  N-EDGE / +0.10R @$75 quantum the bar is pinned to.
- `docs/briefs/INDEX.md` / `lab/CATALOG.md` / `docs/rejected_candidates.md`
  — no existing Q-TRAINKILL owner (attestation below).

**HANDOFF-VERIFY:** PASS. toplevel `C:/Users/joshu/multi_firm_operations`;
branch `cursor/q-trainkill-1` off `dd2cc67`; packet paths exist; Q not
already executed; no live-book / armed-rail premise.

**Sub-rule 8 / 10 attestation (literal output, 2026-08-18):**

```
# lab/CATALOG.md
rg -n "Q-TRAINKILL|train.kill|gates-underpowered|kills-are-informative" lab/CATALOG.md
CATALOG_EXIT:1
(no matches)

# docs/briefs/INDEX.md
rg -n "Q-TRAINKILL|train.kill|gates-underpowered|kills-are-informative" docs/briefs/INDEX.md
INDEX_EXIT:1
(no matches)

# docs/rejected_candidates.md
rg -n "Q-TRAINKILL|train.kill|gates-underpowered|kills-are-informative" docs/rejected_candidates.md
REJECTED_EXIT:1
(no matches)

# python scripts/check_advisor_dedup.py --keywords "TRAINKILL train kill underpowered modest edge explore kill rate"
  slugs found:    (none)
  top hits are the enumerated closures themselves (MSL-S2A, MNQDTL-CON-1,
  MSL-C1, …) plus CONDVAL/EXPR citing this packet — no prior Q-TRAINKILL.

# git log --oneline -20
dd2cc67 research(expr): Q-EXPR-1 RESOLVED -- …
(no TRAINKILL commit)
```

**Sub-rule 10 — existing owner:** the notice *names* this Q as a GRADUATE
packet. Reachability audits are adjacent, not an amend-in-place owner.
No `docs/briefs/Q-TRAINKILL-*`.

---

## §1 — Context & motivation

Observation C: the admissibility bar is generous (+0.10R @$75 clears
N-EDGE) yet the 08-08→08-16 window produced a stack of explore/train
deaths and zero confirm reads. Three explanations were unnamed as a
discrimination: empty families, underpowered gates on true modest edges,
or neither. This Q is the $0 census. Standing clock: base case is §4
FALSIFIED. KILLS-INFORMATIVE is affirmative evidence for letting that
fire; GATES-UNDERPOWERED is the only reading under which the remaining
window plausibly converts.

---

## §2 — Prior art / lineage

- **Parent notice** packet 3 — names the readings, the set, the bar, the
  se formula, the forbidden bar-move.
- **Q-EXPR-1** `RESOLVED` (H1) — conversion orphaning is horizon-mismatch;
  this Q is the *other* bottleneck (power vs empty). Not rediscovery.
- **Gate-reachability audits (2026-07-12 family, 5 firings)** — can the
  gate fire / does it bind. Different unit.
- **No prior Q-TRAINKILL-*.** Tail-methodology: firing-rate discrimination
  is NEW.

---

## §3 — Question (Q-TRAINKILL-1)

**Pre-Q gate test (symptom-only):** "explore/train kills keep landing and
nothing reaches confirm, even though the admissibility bar is generous;
it is unknown whether that record is what empty families produce, what
true +0.10R edges produce under these n's, or neither."

**Q-TRAINKILL-1:** Is the observed kill record consistent with zero edge,
with true +0.10R@$75 edges the explore designs are underpowered to pass,
or with neither?

---

## §4 — Falsifiable hypothesis (H-TRAINKILL)

**H-TRAINKILL:** If `g(0.10) ≥ 0.05` (prereg §E), the gates are
underpowered for the bar-edge (GATES-UNDERPOWERED). If only `g(0) ≥ 0.05`,
the kills are informative of empty families. If neither, the record is
miscalibrated relative to both DGPs.

**Accept → `RESOLVED` (named reading) if:** prereg §E first or second row.
**`AMBIGUOUS-HOLD` if:** BOUNDED extremes disagree or n*=0.
**`MISCALIBRATED` (third §6 row) if:** neither DGP fits and brackets agree.

---

## §5 — Forbidden moves

- **Lowering any gate threshold.** Tempting if GATES-UNDERPOWERED fires.
  Packet forbade it; remedy is n/panel, not a softer bar.
- **Tuning 0.05 / μ_bar / the event map after seeing se.** Same Trap #12.
- **Dropping a named row because its se is inconvenient.** Partial-table.
- **Translating +0.10R into a ρ bar after seeing R2 cells.** Undeclared
  mapping; those rows stay BOUNDED.
- **Quoting the reachability-audit family as this answer.** Different unit.
- **Reading KILLS-INFORMATIVE as a license to skip the power annotation**
  on the next zero-yield streak.

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger | Disposition (typed) |
|---|---|---|
| `RESOLVED` — `KILLS-INFORMATIVE` | g(0)≥0.05 and g(0.10)<0.05 | `INTEGRATE` — drought quotes require this annotation; §4-fire evidence |
| `RESOLVED` — `GATES-UNDERPOWERED` | g(0.10)≥0.05 | `INTEGRATE` — change n/panel before more screens; drought quotes require the annotation |
| `MISCALIBRATED` | neither fits; BOUNDED extremes agree | `ITERATE` — different DGP or recover se; do not lower bars |
| `AMBIGUOUS-HOLD` | BOUNDED extremes disagree or n*=0 | `ITERATE` — recover the missing CI; do not invent |

Pre-registered before substitute. Trap #12: if the floor must move, close
and open a fresh brief.

---

## §7 — Execution plan (self-executing, this session)

- **Phase 0 — Rule-0 / set freeze.** This §0 + prereg §A. Done.
- **Phase 1 — Freeze.** Prereg on disk. Scorer prints sha256 **before**
  opening `TABLE.json`.
- **Phase 2 — Tabulate + score.** Committed closures only. $0 / K=0.
- **Phase 3 — Verdict.** Apply §6. RESULTS + closure + boards.

---

## §8 — Verdict pre-registration

File: [`pre-registration/Q-TRAINKILL-1-verdict-preregistration.md`](pre-registration/Q-TRAINKILL-1-verdict-preregistration.md)

Pre-registration commit hash: *(same-session freeze; sha256 recorded
before table assembly)*
Pre-registration date: 2026-08-18

---

## §9 — Closure record format

- `docs/briefs/closures/Q-TRAINKILL-1-closure-<slug>.md`
Mandatory Iterate. **Registry:** `n/a` — power census / methodology; not
a strategy-grounds seed kill. No gate numbers move.

---

## §10 — Audit hooks

```bash
rg -n "N-2026-08-18-iteration2-identify-notice" docs/briefs/Q-TRAINKILL-1-train-gate-power.md
rg -n "no gate threshold|bar-lowering" docs/briefs/pre-registration/Q-TRAINKILL-1-verdict-preregistration.md
rg -n "prereg_sha256" lab/analysis/_inbox/q_trainkill_1_2026-08/RESULTS.md
python lab/analysis/_inbox/q_trainkill_1_2026-08/score_trainkill.py
python scripts/check_brief.py docs/briefs/Q-TRAINKILL-1-train-gate-power.md --type inquire
```

---

## Verification

```bash
python scripts/check_brief.py docs/briefs/Q-TRAINKILL-1-train-gate-power.md --type inquire
rg -n "Q-TRAINKILL" lab/CATALOG.md docs/briefs/INDEX.md docs/rejected_candidates.md
```
