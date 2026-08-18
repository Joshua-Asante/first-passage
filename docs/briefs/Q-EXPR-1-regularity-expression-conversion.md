# Q-EXPR-1 — What measurable property of the regularity→expression conversion accounts for the orphaning?

**Status:** `CLOSED-RESOLVED 2026-08-18` — H1 4/4; H2 1/5 misses; H3 cannot fire. Closure: [`closures/Q-EXPR-1-closure-resolved.md`](closures/Q-EXPR-1-closure-resolved.md).
**Authored:** 2026-08-18
**Closed:** 2026-08-18
**Authors:** Joshua (operator GO: "move on to GO Q-EXPR-1") + Cursor (execution)
**Parent question:** [`N-2026-08-18-iteration2-identify-notice`](../notes/notice/N-2026-08-18-iteration2-identify-notice.md) observation A / §5 packet 2
**Sub-questions opened:** none
**Loop:** Inquire-phase Pre-Q — closure gated on whether any of three pre-declared conversion readings meets a 0.50 share of its own class
**Artifact path:** `docs/briefs/Q-EXPR-1-regularity-expression-conversion.md`
**Pre-registration:** [`pre-registration/Q-EXPR-1-verdict-preregistration.md`](pre-registration/Q-EXPR-1-verdict-preregistration.md)

**D-S-A domain:** data (already-committed closures / ledgers → one conversion-step table)
**Pre-Q gate:**
```
D: deleted from this Q's working set — (i) Q-TRAINKILL-1's power-vs-empty
   discrimination [test: out of scope — different unit of analysis, separate
   packet]; (ii) sourcing-type admissibility deaths (WHO-dry, Clause-N, Req-2)
   [test: observation B — those are the other bottleneck; they are not
   regularity→expression conversions]; (iii) CATALOG "closed" column dates as
   first-measurement evidence [test: duplicated by higher-fidelity sources —
   RESULTS/ledger authored dates]. No forbidden D-test. Raw sources remain
   the Rule-0 anchor.
S: corpus compresses to two tables (regularity rows + attempt rows) and one
   H2 scoring class. Compression preserves observation A (conversion success
   = 0; death-stage distribution survives as columns).
A: each H is a share vs 0.50. Q-cost is O(read the prereg + score the table).
```

---

## §0 — Rule 0 reads (production-source verification, executed 2026-08-18)

Worktree on `cursor/q-expr-1` at `1632de9` (Q-CONDVAL-1 close), `origin/main`
has nothing not in HEAD. Each path read **before** the conversion table was
scored. The prereg's share / class / H-positive definitions were written
**before** closure numbers were substituted.

- `docs/notes/notice/N-2026-08-18-iteration2-identify-notice.md` — last touch
  `1632de9` (2026-08-18; authored `8f74f93`). Packet 2: tabulate every
  RESOLVED/validated regularity + TXG attempts; pre-declare all three readings
  before the table; E1 = flat-by-16:00 envelope.
- `docs/briefs/closures/Q-TXG-1-closure-falsified-at-walls.md` — anchor
  `027a729` (2026-08-14). Prior art: small-edge expressions fail the cost tax;
  large-edge expressions fail trailing-DD survival. Evidence rows + prior,
  not a rediscovery.
- `ops/instruments/MNQ.md` — last touch `4062562` (2026-08-18). N8 weekly
  structure RESOLVED; N9 pools anti-attractor + bear-FVG draw; MNQFVG-1 /
  MNQPOOL-1 / Q-WLEGB-1 expression deaths.
- `docs/briefs/INDEX.md` / `lab/CATALOG.md` / `docs/rejected_candidates.md`
  — scanned this session for an existing Q-EXPR owner (none; see attestation).
- `docs/operational_rules.md` §8 sub-rules 8/10 — paste-literal standard;
  `repo_retrieve.py` is ASSISTIVE-ONLY.

**HANDOFF-VERIFY (this session):** PASS. toplevel
`C:/Users/joshu/multi_firm_operations`; branch `cursor/q-expr-1` off
`1632de9`; named packet paths exist; Q-EXPR-1 not already executed (see
pasted searches); no live-book / Striker / armed-rail premise in the packet.

**Sub-rule 8 / 10 attestation (literal output, 2026-08-18, this worktree):**

```
# lab/CATALOG.md
rg -n "Q-EXPR|horizon.mismatch|expression.orphan|conversion.step|regularity.+expression" lab/CATALOG.md
CATALOG_EXIT:1
(no matches)

# docs/briefs/INDEX.md
rg -n "Q-EXPR|horizon.mismatch|expression.orphan|conversion.step|regularity.+expression" docs/briefs/INDEX.md
INDEX_EXIT:1
(no matches)

# docs/rejected_candidates.md
rg -n "Q-EXPR|horizon.mismatch|expression.orphan|conversion.step|regularity.+expression" docs/rejected_candidates.md
REJECTED_EXIT:1
(no matches)

# notice-guard (docs/)
rg -n -i "horizon.mismatch|expression.orphan|conversion.step|regularity.+expression" docs/
→ hits only in:
  docs/notes/notice/N-2026-08-18-iteration2-identify-notice.md (the parent packet)
  docs/briefs/Q-CONDVAL-1-range-state-r-terms.md:104 (cites "conversion-step census"
    as the unit this Q owns — adjacent prior, not this Q executed)

# python scripts/check_advisor_dedup.py --keywords "EXPR expression orphan conversion step horizon mismatch regularity"
check_advisor_dedup: keywords: 'EXPR expression orphan conversion step horizon mismatch regularity'
  slugs found:    (none)
  keywords found: 8 significant terms
POSSIBLE PRIOR ART — top hits are keyword coincidences:
  [5] docs/notes/audits/programme-audit/2026-08-05-claim-alignment/03-agent-facing.md
  [3] docs/briefs/closures/Q-RAIL-1-closure-resolved.md
  [3] docs/notes/audits/programme-audit/2026-08-05-claim-alignment/05-cosmetic.md
  [3] docs/notes/audits/programme-audit/2026-08-05-claim-alignment/08-hooks.md
(script then UnicodeEncodeError on cp1252 — remainder not needed; no Q-EXPR slug)

# git log --oneline -20
1632de9 research(condval): Q-CONDVAL-1 FALSIFIED -- CL range-state lift misses the R-term bar
f9fcab5 Merge pull request #39 from Joshua-Asante/claude/iteration2-identify-notice
… (no Q-EXPR commit)

# git log --oneline origin/main ^HEAD
(empty)
```

**Sub-rule 10 — existing owner:** the notice *names* this Q as a GRADUATE
packet ("named, not opened"). Q-TXG-1 is prior art on a *locked-book transfer*
lane, different unit (cells vs conversion-step census). No existing
`docs/briefs/Q-EXPR-*`. A new Inquire brief is the exception the notice
specified; amending the notice into a Pre-Q would mix types.

---

## §1 — Context & motivation

Observation A of the iteration-2 notice: the estate has validated true
regularities (W-layer weekly structure, D-layer bear-FVG, CL range-state
SIGNAL-GENERIC) and every one is expression-orphaned. Conversion success
count = 0, ever. Three informal mechanisms were named — horizon mismatch,
cost-quantization, survivor artifact — with no discriminating table.

This Q is the $0 census that scores those three readings **before** any new
expression is built, and before B2 priced spends elect (expiry 2026-09-01).
Q-CONDVAL-1 already parked the conditioner-engineering branch; it does not
answer why conversion fails as a class.

Standing clock: 82 days to 2026-11-08; base case is §4 FALSIFIED. This Q
does not pretend otherwise.

---

## §2 — Prior art / lineage

- **Parent notice** `N-2026-08-18-iteration2-identify-notice` — names the
  packet, the three Hs, the H2 class, and the TXG prior-art guard.
- **Q-TXG-1** `FALSIFIED-at-walls` — locked-book transfers died at cost tax
  vs trailing-DD survival. **Evidence rows + prior, not rediscovery.**
- **Q-CONDVAL-1** `FALSIFIED` — CL finding is economically empty at the
  N-EDGE cell; conversion of that finding as a host conditioner was
  never-attempted and stays so. Not this unit of analysis.
- **Q-WLEGB-1 / WSTRUCT-M2K / MNQFVG-1 / MNQPOOL-1** — named expression
  deaths of the headline regularities. Attempt rows.
- **TNEC-CON-2/3/4/5 + Q-R2AGRUN-1** — H2 scoring class (INDEX
  AMBIGUOUS-HOLD window).
- **No prior Q-EXPR-*.** Tail-methodology: conversion step as unit of
  analysis is NEW (notice-guard greps at GO: zero hits outside the notice
  + one CONDVAL pointer). Not a 4th H on TXG.

---

## §3 — Question (Q-EXPR-1)

**Pre-Q gate test (symptom-only rephrase):** "every validated regularity is
expression-orphaned and conversion success is zero; it is unknown which
measurable property of the conversion step accounts for that, or whether
any such property can be scored per regularity before an expression is
built." No fix baked in — the question does not say "add a horizon filter"
or "lower the cost hurdle."

**Q-EXPR-1:** What measurable property of the regularity→expression
conversion accounts for the orphaning, and can it be scored per regularity
before any expression is built?

---

## §4 — Falsifiable hypothesis (H-EXPR)

**H-EXPR:** If at least one of H1 / H2 / H3 meets the pre-declared 0.50
share of its own class (prereg §A–§C), then the conversion step is
modeled and the firing branch(es)' admission-rule change is authorized.
**Otherwise** (NO-DOMINANT) the conversion step stays unmodeled.

**Accept → `RESOLVED` if:** ≥1 of H1, H2, H3 ≥ 0.50.
**Reject → `FALSIFIED` if:** no H ≥ 0.50 and no voiding BOUNDED disagreement.
**`AMBIGUOUS-HOLD` if:** prereg §E third row (BOUNDED disagreement, or
H1/H2 miss and H3 cannot-fire is the only remaining modeling path).

---

## §5 — Forbidden moves

- **Tuning 0.50 or the H2 class after seeing the table.** Tempting because
  CON-3/4/5 sit near the "gross present" line. Ruled out by prereg §A/§B3.
- **Dropping R2AGRUN because it is association-not-hurdle.** Tempting
  (it cannot help H2). Partial-table rule: it stays; it scores H2-negative
  if that is what the definition says.
- **Treating TXG as this Q's discovery.** Tempting (its model update is
  already H2-shaped). The packet forbade rediscovery; TXG is rows + prior.
- **Conflating E1 envelope with MSL E1 HOLD.** Same token, different
  object. Would mis-label every slate-pause as a horizon kill.
- **Opening Q-TRAINKILL-1 from this close.** Separate packet; observation
  C, different unit.
- **Re-diagnosing a death stage to fit an H.** Labels come from the
  committed closure/RESULTS language.

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition (typed) |
|---|---|---|
| `RESOLVED` | ≥1 of H1, H2, H3 meets 0.50 | `INTEGRATE` — fire only the winning branch(es)' packet admission-rule change; disclose the rest |
| `FALSIFIED` | no H meets 0.50; no voiding BOUNDED disagreement | `STOP` — conversion unmodeled; B2 elects on admissibility/power alone |
| `AMBIGUOUS-HOLD` | BOUNDED extremes disagree on whether any H meets 0.50, or H1/H2 miss and H3 cannot-fire is the only remaining modeling path | `ITERATE` — recover the missing stamp; do not invent |

**Pre-registered before the table is assembled.** Trap #12: if the share
or class must move, close this brief and open a fresh one.

---

## §7 — Execution plan (self-executing, this session)

- **Phase 0 — Rule-0 reads.** This §0. Done before the table is scored.
- **Phase 1 — Freeze.** Prereg on disk. Record sha256 of the prereg bytes
  **before** assembling the RESULTS table from closures.
- **Phase 2 — Tabulate.** Committed closures / ledgers / RESULTS only.
  $0 / K=0. No new market data.
- **Phase 3 — Verdict assertion.** Apply §6. Write RESULTS + closure.
  Propagate notice packet 2, INDEX, CATALOG, STATE, SESSIONS.

---

## §8 — Verdict pre-registration

File: [`pre-registration/Q-EXPR-1-verdict-preregistration.md`](pre-registration/Q-EXPR-1-verdict-preregistration.md)

Pre-registration commit hash: *(same-session freeze; sha256 `27c366f4f7e7a924a8e91ba549c8ade25eadd2024add1e827d70a31828e6441a` recorded by the scorer before `TABLE.json` was opened; git hash lands at operator commit)*
Pre-registration date: 2026-08-18

---

## §9 — Closure record format

- **If RESOLVED:** `docs/briefs/closures/Q-EXPR-1-closure-resolved.md`
- **If FALSIFIED:** `docs/briefs/closures/Q-EXPR-1-closure-falsified.md`
- **If AMBIGUOUS-HOLD:** `docs/briefs/closures/Q-EXPR-1-closure-ambiguous.md`

Mandatory typed `## Iterate` block. **Registry:** `n/a` — conversion
census / methodology; not a strategy-grounds seed kill. (If H2 fires,
TNEC-CON re-reads route through *those* closures' own bars — this Q
does not mint registry rows for them.)

---

## §10 — Audit hooks

```bash
# Graduation lineage
rg -n "N-2026-08-18-iteration2-identify-notice" docs/briefs/Q-EXPR-1-regularity-expression-conversion.md

# E1 not conflated with MSL E1 HOLD
rg -n "E1 HOLD|flat-by-16:00" docs/briefs/pre-registration/Q-EXPR-1-verdict-preregistration.md

# Freeze-before-table
rg -n "prereg_sha256" lab/analysis/_inbox/q_expr_1_2026-08/RESULTS.md

# Reproduce the share arithmetic from RESULTS.json
python lab/analysis/_inbox/q_expr_1_2026-08/score_expr.py

# Discipline
python scripts/check_brief.py docs/briefs/Q-EXPR-1-regularity-expression-conversion.md --type inquire
```

---

## Verification

```bash
python scripts/check_brief.py docs/briefs/Q-EXPR-1-regularity-expression-conversion.md --type inquire
rg -n "Q-EXPR" lab/CATALOG.md docs/briefs/INDEX.md docs/rejected_candidates.md
# expected at authoring: no owner row yet
```
