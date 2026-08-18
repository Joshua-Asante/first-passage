# Q-TRAINKILL-3 — Do the two surviving DGPs concord across event-class blocks?

**Status:** `CLOSED` — `AMBIGUOUS-HOLD`
**Authored:** 2026-08-18
**Closed:** 2026-08-18
**Authors:** Joshua (operator GO: "commit and continue on Q-TRAINKILL-3") + Cursor (execution)
**Parent question:** [`Q-TRAINKILL-2-bounded-recovery-alt-dgp.md`](Q-TRAINKILL-2-bounded-recovery-alt-dgp.md) / [`closure`](closures/Q-TRAINKILL-2-closure-ambiguous-hold.md) Iterate entry packet
**Sub-questions opened:** none
**Loop:** Inquire-phase Pre-Q — closure gated on two-block concordance (or an election this GO did not make)
**Artifact path:** `docs/briefs/Q-TRAINKILL-3-neg-vs-dep-discriminator.md`
**Pre-registration:** [`pre-registration/Q-TRAINKILL-3-verdict-preregistration.md`](pre-registration/Q-TRAINKILL-3-verdict-preregistration.md)

**D-S-A domain:** data (committed TK2 P vectors → two block g's)
**Pre-Q gate:**
```
D: deleted — (i) operator election (GO did not name a DGP)
   [test: §A]; (ii) a third μ [test: TK2 stop rule]; (iii) dropping
   CON-4 from Block A [test: silent drop voids]; (iv) Q-TRAINKILL-4
   on the same vectors [test: §E STOP].
S: nine scored rows → Block F (4 FALSIFIED) + Block A (5 AMBIGUOUS).
A: 2:1 winner per block; concordance. Q-cost is O(run the scorer).
```

---

## §0 — Rule 0 reads (production-source verification, executed 2026-08-18)

Worktree on `cursor/q-trainkill-3` at `be694ca` (Q-TRAINKILL-2 close). Prereg
written **before** any block geo-mean was computed.

- `docs/briefs/closures/Q-TRAINKILL-2-closure-ambiguous-hold.md` — entry
  packet: discriminator the two DGPs split, or an election; no third μ.
- `docs/briefs/pre-registration/Q-TRAINKILL-2-verdict-preregistration.md` —
  inherited NEG / DEP-ZERO definitions.
- `lab/analysis/_inbox/q_trainkill_2_2026-08/RESULTS.json` — named as the
  P-vector source at freeze; block g's not computed until after hash.
- `docs/briefs/INDEX.md` / `lab/CATALOG.md` / `docs/rejected_candidates.md`
  — no existing Q-TRAINKILL-3 owner (attestation below).

**HANDOFF-VERIFY:** PASS. toplevel `C:/Users/joshu/multi_firm_operations`;
branch `cursor/q-trainkill-3` off `be694ca`; packet paths exist; Q named
not previously executed; GO is not an election; no live-book premise.

**Sub-rule 8 / 10 attestation (literal output, 2026-08-18):**

```
# lab/CATALOG.md
rg -n "Q-TRAINKILL-3|NEG-vs-DEP|two-block concordance" lab/CATALOG.md
CATALOG_EXIT:1
(no matches)

# docs/briefs/INDEX.md
rg -n "Q-TRAINKILL-3|NEG-vs-DEP|two-block concordance" docs/briefs/INDEX.md
INDEX_EXIT:1
(no matches)

# docs/rejected_candidates.md
rg -n "Q-TRAINKILL-3|NEG-vs-DEP|two-block concordance" docs/rejected_candidates.md
REJECTED_EXIT:1
(no matches)

# python scripts/check_advisor_dedup.py --keywords "TRAINKILL-3 NEG-vs-DEP discriminator concordance election"
  slugs found:    ['TRAINKILL-3']
  top hits are Q-TRAINKILL-2 closure / SESSIONS 18h naming this successor.

# git fetch origin && git log --oneline origin/main ^HEAD
(empty)

# git log --oneline -3
be694ca research(trainkill): Q-TRAINKILL-2 AMBIGUOUS-HOLD -- …
13c0915 research(trainkill): Q-TRAINKILL-1 AMBIGUOUS-HOLD -- …
```

**Sub-rule 10 — existing owner:** TK2 Iterate names this successor.

---

## §1 — Context & motivation

TK2 closed `AMBIGUOUS-HOLD` because both named alternates fit the joint
scored core. The hold is a missing discriminator, not a missing DGP.
This Q is the $0 concordance test: do the two event classes name the
same winner? Standing clock: base case is §4 FALSIFIED. No gate number
moves.

---

## §2 — Prior art / lineage

- **Q-TRAINKILL-2** `AMBIGUOUS-HOLD` — this Q is the entry packet.
- **Q-TRAINKILL-1** `AMBIGUOUS-HOLD` — grandparent; not reopened.
- **No prior Q-TRAINKILL-3.**

---

## §3 — Question (Q-TRAINKILL-3)

**Pre-Q gate test (symptom-only):** "two pre-declared DGPs both fit the
same nine mean-R cells; it is unknown whether they agree when those
cells are split by the event the original gates actually fired."

**Q-TRAINKILL-3:** On the committed TK2 P vectors, do Block F (FALSIFIED)
and Block A (AMBIGUOUS) name the same 2:1 winner between `NEG` and
`DEP`?

---

## §4 — Falsifiable hypothesis (H-TK3)

**H-TK3:** If both blocks name `NEG` (ratio ≥ 2), the working-model is
`NEG-FAMILIES`. If both name `DEP`, it is `KILLS-INFORMATIVE-DEP`. If
they disagree or either is a 2:1 tie, the DGPs are not concordant.

**Accept → `RESOLVED` if:** both blocks the same named winner.
**`AMBIGUOUS-HOLD` if:** split or tie.

---

## §5 — Forbidden moves

- **Treating this GO as an election.** It did not name a DGP.
- **A third μ** to break a split.
- **Dropping CON-4** from Block A.
- **Retuning the 2:1 bar** after seeing block g.
- **Reopening TK1/TK2 floors or joints.**
- **Opening Q-TRAINKILL-4** on the same P vectors if this holds.
- **Lowering any gate threshold.**

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger | Disposition (typed) |
|---|---|---|
| `RESOLVED` — `NEG-FAMILIES` | both blocks `NEG` | `INTEGRATE` — working-model NEG; no bar-lowering |
| `RESOLVED` — `KILLS-INFORMATIVE-DEP` | both blocks `DEP` | `INTEGRATE` — working-model DEP; drought quotes need the dependence annotation |
| `AMBIGUOUS-HOLD` | split or tie | `STOP` — no Q-TRAINKILL-4; re-proposal is a new panel or an election |

---

## §7 — Execution plan (self-executing, this session)

- **Phase 0 — Freeze.** This §0 + prereg. sha256 before block g.
- **Phase 1 — Score.** Scorer reads committed TK2 P vectors only.
- **Phase 2 — Verdict.** RESULTS + closure + boards.

---

## §8 — Verdict pre-registration

File: [`pre-registration/Q-TRAINKILL-3-verdict-preregistration.md`](pre-registration/Q-TRAINKILL-3-verdict-preregistration.md)

Pre-registration sha256 (printed before block g):
`93c21d21eb0fd2d0e580a384a586dbf10d19d8a23a593dea6e147f63ad57e7f6`
Pre-registration date: 2026-08-18

---

## §9 — Closure record format

- `docs/briefs/closures/Q-TRAINKILL-3-closure-<slug>.md`
Mandatory Iterate. **Registry:** `n/a`. No gate numbers move.

---

## §10 — Audit hooks

```bash
rg -n "Q-TRAINKILL-2-closure-ambiguous-hold" docs/briefs/Q-TRAINKILL-3-neg-vs-dep-discriminator.md
rg -n "2:1|Block F|election limb" docs/briefs/pre-registration/Q-TRAINKILL-3-verdict-preregistration.md
rg -n "prereg_sha256" lab/analysis/_inbox/q_trainkill_3_2026-08/RESULTS.md
python lab/analysis/_inbox/q_trainkill_3_2026-08/score_trainkill3.py
python scripts/check_brief.py docs/briefs/Q-TRAINKILL-3-neg-vs-dep-discriminator.md --type inquire
```

---

## Verification

```bash
python scripts/check_brief.py docs/briefs/Q-TRAINKILL-3-neg-vs-dep-discriminator.md --type inquire
```
