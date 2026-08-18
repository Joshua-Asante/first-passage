# Q-TRAINKILL-2 — Do recovered mean-R CIs, or a pre-declared alternate DGP, resolve the TRAINKILL hold?

**Status:** `CLOSED` — `AMBIGUOUS-HOLD`
**Authored:** 2026-08-18
**Closed:** 2026-08-18
**Authors:** Joshua (operator GO: "commit and continue with Q-TRAINKILL-2") + Cursor (execution)
**Parent question:** [`Q-TRAINKILL-1-train-gate-power.md`](Q-TRAINKILL-1-train-gate-power.md) / [`closure`](closures/Q-TRAINKILL-1-closure-ambiguous-hold.md) Iterate entry packet
**Sub-questions opened:** none
**Loop:** Inquire-phase Pre-Q — closure gated on Limb 1 (recovery) or Limb 2 (named alternates)
**Artifact path:** `docs/briefs/Q-TRAINKILL-2-bounded-recovery-alt-dgp.md`
**Pre-registration:** [`pre-registration/Q-TRAINKILL-2-verdict-preregistration.md`](pre-registration/Q-TRAINKILL-2-verdict-preregistration.md)

**D-S-A domain:** data (committed closure CIs → recovery census + two named g's)
**Pre-Q gate:**
```
D: deleted — (i) retuning TK1 independence / floor / μ_bar [test: TK1
   forbidden re-open]; (ii) one-arm re-read of a both-arms cell [test:
   TK1 stop rule]; (iii) ρ→R translation [test: TK1 §5]; (iv) naming a
   third μ after seeing g [test: §E STOP clause].
S: seven BOUNDED rows → {promoted, still-BOUNDED}; scored core → g on
   {0, +0.10, −0.10, DEP-ZERO}. Compression preserves the hold's residue.
A: Limb 1 then Limb 2, first-fire except multi-fit HOLD. Q-cost is
   O(read the seven named sources + run the scorer).
```

---

## §0 — Rule 0 reads (production-source verification, executed 2026-08-18)

Worktree on `cursor/q-trainkill-2` at `13c0915` (Q-TRAINKILL-1 close). Prereg
written **before** any of the seven BOUNDED sources was opened for a number.

- `docs/briefs/closures/Q-TRAINKILL-1-closure-ambiguous-hold.md` — entry
  packet: recover BOUNDED mean-R CIs **or** name an alternate DGP before
  re-score; no bar-lowering; one-arm re-read is not a re-proposal.
- `docs/briefs/pre-registration/Q-TRAINKILL-1-verdict-preregistration.md` —
  inherited constants (set / μ / se / product / floor / event map).
- `lab/analysis/_inbox/q_trainkill_1_2026-08/TABLE.json` — recovery corpus
  paths (named, not opened for new numbers at freeze).
- `docs/briefs/INDEX.md` / `lab/CATALOG.md` / `docs/rejected_candidates.md`
  — no existing Q-TRAINKILL-2 owner (attestation below).

**HANDOFF-VERIFY:** PASS. toplevel `C:/Users/joshu/multi_firm_operations`;
branch `cursor/q-trainkill-2` off `13c0915`; packet paths exist; Q named
not previously executed; no live-book / armed-rail premise.

**Sub-rule 8 / 10 attestation (literal output, 2026-08-18):**

```
# lab/CATALOG.md
rg -n "Q-TRAINKILL-2|trainkill.2|recover-BOUNDED|alternate-DGP|NEG-FAMILIES" lab/CATALOG.md
CATALOG_EXIT:1
(no matches)

# docs/briefs/INDEX.md
rg -n "Q-TRAINKILL-2|trainkill.2|recover-BOUNDED|alternate-DGP|NEG-FAMILIES" docs/briefs/INDEX.md
INDEX_EXIT:1
(no matches)

# docs/rejected_candidates.md
rg -n "Q-TRAINKILL-2|trainkill.2|recover-BOUNDED|alternate-DGP|NEG-FAMILIES" docs/rejected_candidates.md
REJECTED_EXIT:1
(no matches)

# python scripts/check_advisor_dedup.py --keywords "TRAINKILL-2 recover BOUNDED NEG-FAMILIES Fréchet alternate DGP"
  slugs found:    ['TRAINKILL-2']
  top hits are Q-TRAINKILL-1 closure / SESSIONS 18g naming this successor
  — existing owner is the TK1 Iterate packet, not a prior TRAINKILL-2.

# git fetch origin && git log --oneline origin/main ^HEAD
(empty — no unseen origin/main commits)

# git log --oneline -5
13c0915 research(trainkill): Q-TRAINKILL-1 AMBIGUOUS-HOLD -- …
```

**Sub-rule 10 — existing owner:** TK1 Iterate names this successor. This
file executes that packet; it does not restate TK1's hold as a new finding.

---

## §1 — Context & motivation

TK1 closed `AMBIGUOUS-HOLD`: BOUNDED extremes disagree; scored core
`MISCALIBRATED`. The hold exists because seven rows were not mean-R
events under the +0.10R bar, and the eight that were jointly fit neither
μ=0 nor μ=+0.10R. The named next step is recover those CIs or accept the
core as miscalibrated under a **pre-declared** alternate DGP. Standing
clock: base case is §4 FALSIFIED. No gate number moves.

---

## §2 — Prior art / lineage

- **Q-TRAINKILL-1** `AMBIGUOUS-HOLD` — this Q is the entry packet, not
  rediscovery.
- **Gate-reachability audits (2026-07-12 family)** — still a different unit.
- **No prior Q-TRAINKILL-2.**

---

## §3 — Question (Q-TRAINKILL-2)

**Pre-Q gate test (symptom-only):** "the joint kill-record likelihood
could not discriminate empty families from +0.10R under-power because
seven rows had no mean-R CI and the eight that did fit neither DGP; it
is unknown whether committed mean-R CIs exist for those seven, or
whether a pre-declared alternate DGP fits the scored core."

**Q-TRAINKILL-2:** After recovery of any committed mean-R CIs on the
seven TK1-BOUNDED rows, does the inherited {0, +0.10} pair resolve, or
does a pre-declared −0.10R or Fréchet-hi-zero DGP fit the scored core?

---

## §4 — Falsifiable hypothesis (H-TK2)

**H-TK2:** If recovery promotes ≥1 row and BOUNDED extremes then agree
on a TK1 §E reading, that reading is the verdict. Otherwise the scored
core is tested against `NEG` (μ=−0.10R, independence) and `DEP-ZERO`
(μ=0, Fréchet-hi). Exactly one of those two fits → that named reading;
both → `AMBIGUOUS-HOLD`; neither → `MISCALIBRATED`.

**Accept → `RESOLVED` (named reading) if:** Limb 1 named reading, or
Limb 2 singleton.
**`AMBIGUOUS-HOLD` if:** both alternates fit, or n*=0.
**`MISCALIBRATED` if:** Limb 2 neither fits.

---

## §5 — Forbidden moves

- **Lowering any gate threshold.** Inherited.
- **One-arm re-read of a both-arms cell.** TK1 stop rule.
- **Retuning the independence product inside TK1.** Dependence is a
  *new* named DGP (Fréchet-hi), not a silent TK1 edit.
- **Translating ρ / annSR / gateHit into +0.10R.** Recovery rule §B.
- **Naming a third μ after seeing g.** §E STOP.
- **Dropping CON-4 or any named row** because its se is inconvenient.
- **Quoting Limb-2 as a TK1 amendment.** Separate Q.

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger | Disposition (typed) |
|---|---|---|
| `RESOLVED` — Limb-1 TK1 reading | ≥1 promotion and extremes agree | `INTEGRATE` — TK1 §E for that reading |
| `RESOLVED` — `NEG-FAMILIES` | Limb 2: only NEG fits | `INTEGRATE` — FALSIFIED cells as true-negative; no drought-as-empty; no bar-lowering |
| `RESOLVED` — `KILLS-INFORMATIVE-DEP` | Limb 2: only DEP-ZERO fits | `INTEGRATE` — drought quotes need the dependence annotation |
| `AMBIGUOUS-HOLD` | both alternates fit, or n*=0 | `ITERATE` — do not pick after seeing g |
| `MISCALIBRATED` | neither alternate fits | `STOP` — do not keep naming μ |

Pre-registered before substitute. Trap #12: if the floor must move, close
and open a fresh brief.

---

## §7 — Execution plan (self-executing, this session)

- **Phase 0 — Rule-0 / freeze.** This §0 + prereg. Done. sha256 printed
  before any of the seven sources was opened for a number.
- **Phase 1 — Recover.** Named TABLE.json paths only.
- **Phase 2 — Score.** Limb 1 then Limb 2.
- **Phase 3 — Verdict.** RESULTS + closure + boards.

---

## §8 — Verdict pre-registration

File: [`pre-registration/Q-TRAINKILL-2-verdict-preregistration.md`](pre-registration/Q-TRAINKILL-2-verdict-preregistration.md)

Pre-registration sha256 (printed before recovery):
`86049b89b413b33430e7dfe31d9fc5de5cc46b81c0f23f3ea7877d78c7605b5d`
Pre-registration date: 2026-08-18

---

## §9 — Closure record format

- `docs/briefs/closures/Q-TRAINKILL-2-closure-<slug>.md`
Mandatory Iterate. **Registry:** `n/a` — power census / methodology; not
a strategy-grounds seed kill. No gate numbers move.

---

## §10 — Audit hooks

```bash
rg -n "Q-TRAINKILL-1-closure-ambiguous-hold" docs/briefs/Q-TRAINKILL-2-bounded-recovery-alt-dgp.md
rg -n "Fréchet-hi|−0.10R|one-arm re-read" docs/briefs/pre-registration/Q-TRAINKILL-2-verdict-preregistration.md
rg -n "prereg_sha256" lab/analysis/_inbox/q_trainkill_2_2026-08/RESULTS.md
python lab/analysis/_inbox/q_trainkill_2_2026-08/score_trainkill2.py
python scripts/check_brief.py docs/briefs/Q-TRAINKILL-2-bounded-recovery-alt-dgp.md --type inquire
```

---

## Verification

```bash
python scripts/check_brief.py docs/briefs/Q-TRAINKILL-2-bounded-recovery-alt-dgp.md --type inquire
rg -n "Q-TRAINKILL-2" lab/CATALOG.md docs/briefs/INDEX.md docs/rejected_candidates.md
```
