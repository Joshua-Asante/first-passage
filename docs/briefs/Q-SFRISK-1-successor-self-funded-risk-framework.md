# [Q-SFRISK-1] — Successor self-funded risk framework

**Status:** `CLOSED-RESOLVED` (2026-07-15)
**Authored:** 2026-07-14 (scaffold → question freeze same session)
**Closed:** `2026-07-15` — [`docs/briefs/closures/Q-SFRISK-1-closure-resolved.md`](Q-SFRISK-1-closure-resolved.md); admitting ADR [`docs/adr/2026-07-15-sfrisk-1-t1-admitting-successor-risk-framework.md`](../adr/2026-07-15-sfrisk-1-t1-admitting-successor-risk-framework.md) (`Accepted`, ratified 2026-07-15)
**Authors:** Joshua (authority) + Cursor (structure + question architecture) — parent triage: claude.ai advisor 2026-07-13
**Parent question:** `N/A` (spawned by audit §5.2 / D1 under [`docs/adr/2026-07-11-challenge-era-claims-rescope.md`](../adr/2026-07-11-challenge-era-claims-rescope.md))
**Sub-questions opened:** none yet (D2 / D3 may now fork from this closed Pre-Q — §6 has fired)
**Loop:** Inquire-phase Pre-Q — gates the first self-funded risk question set before any successor-semantics MC number is produced
**Artifact path:** `docs/briefs/Q-SFRISK-1-successor-self-funded-risk-framework.md`
**Verdict pre-registration:** [`docs/briefs/pre-registration/Q-SFRISK-1-verdict-preregistration.md`](pre-registration/Q-SFRISK-1-verdict-preregistration.md)

> **Numbers discipline (binding):** this Pre-Q freezes the **question architecture** (what replaces P(pass)). It does **not** invent operator risk-tolerance numbers (max-DD %, TUW days, withdrawal rate). Those are declared in a Phase-0 amendment to the §8 pre-registration **before any successor-semantics MC run** — inventing them here would violate rescope ADR §5 ("numbers before question").

---

## §0 — Rule 0 reads (production-source verification)

Files read **before** authoring / freezing this brief (Phase 0, 2026-07-14, off `origin/main` @ `53c27fe`):

- `docs/adr/2026-07-11-challenge-era-claims-rescope.md` — anchor: `99b7854` (2026-07-11) — **§4 (Falsifier / completion falsifier)**, **§5 (Forbidden moves)**, **§7 Deferred (D1 line)** transcribed below
- `docs/notes/audits/programme-audit/2026-07-11-core-fxify-anchoring-audit.md` — anchor: `99b7854` (2026-07-11) — Class D / **D1** framing + §5.2 spawn text
- `lab/analysis/regime/decompound_remc_2026-06-07/` (+ `docs/adr/2026-06-07-decompound-remc-hold.md`) — closest existing instrument for self-funded / withdrawal-model semantics
- `docs/adr/2026-06-07-decompound-remc-hold.md` — standing HOLD; both historical lock gates breach on clean vintage; regime-split

---

## §1 — Context & motivation

The 2026-07-11 challenge-era claims rescope retired P(pass) / bust<1% / p99 DD<5% as *live* claims (venue gone; numbers retained as historical calibration + engine regression pins). That ADR's own **completion falsifier** hard-dates **2026-11-08**: without a successor risk-framework Pre-Q pre-registered, the re-scope is incomplete and D1 escalates to a mandatory blocker on any Aegis→M6J go-live. The programme audit framed D1 as: *what replaces P(pass)?* Candidates named (not chosen as thresholds): P(breach operator max-DD line), time-under-water, withdrawal sustainability — with the decompound-remc machinery (2026-06-07, +withdrawal/$200K-reset) as the closest existing instrument, on which **both old gates already breach** (clean vintage 98.53/1.47/5.32, hard regime-split). Retiring the challenge framing is therefore not a loosening.

Standing doctrine: rescope ADR §5 forbids running successor-semantics MC numbers before this Pre-Q freezes. This brief freezes the question; numeric tolerances wait for the §8 Phase-0 amendment before analysis.

---

## §2 — Prior art / lineage

- [`docs/adr/2026-07-11-challenge-era-claims-rescope.md`](../adr/2026-07-11-challenge-era-claims-rescope.md) — `Accepted`; owns the completion falsifier + forbidden "numbers before question"; **this Pre-Q is its D1 discharge**
- [`docs/notes/audits/programme-audit/2026-07-11-core-fxify-anchoring-audit.md`](../notes/audits/programme-audit/2026-07-11-core-fxify-anchoring-audit.md) — Class D / D1 + §5.2 spawn; D2 and D3 feed *from* a frozen D1
- [`docs/adr/2026-06-07-decompound-remc-hold.md`](../adr/2026-06-07-decompound-remc-hold.md) + [`lab/analysis/regime/decompound_remc_2026-06-07/`](../../lab/analysis/regime/decompound_remc_2026-06-07/) — closest instrument; HOLD, not a successor framework
- [`docs/adr/2026-07-13-dd-protection-concept-not-constant.md`](../adr/2026-07-13-dd-protection-concept-not-constant.md) — D2 *frame*; does not define the self-funded risk *question*
- [`docs/adr/2026-07-10-r6-nogo-futures-residual-disposition.md`](../adr/2026-07-10-r6-nogo-futures-residual-disposition.md) — futures-prop NO-GO; Aegis→M6J go-live separately gated (blocked by incomplete D1 per rescope §4 until this Pre-Q is pre-registered)
- No prior Q-SFRISK-* brief — genuinely novel Pre-Q ID

---

## §3 — Question (Q-SFRISK-1)

**Pre-Q gate test (Discipline Check #5):** symptom-only rephrase holds — the vacuum of live risk claims is the symptom; no max-DD % or withdrawal rate is baked into the question.

**Q-SFRISK-1:** After challenge-era P(pass) was retired, what is the cost of operating with **no live self-funded risk claim**, and what falsifiable claim-set architecture can replace P(pass) for Aegis→M6J go-live design?

**Claim-set architecture (frozen — dimensions named, thresholds not invented):**

| Dimension | Role in the successor claim set | Threshold status |
|---|---|---|
| Operator max-DD line (breach definition) | Replaces challenge bust / static-DD as the capital-ruin gate | Declared in §8 Phase-0 amendment before any MC — **not invented here** |
| Time-under-water tolerance | Captures duration risk the challenge pass-timeout proxyed poorly | Declared in §8 Phase-0 amendment before any MC — **not invented here** |
| Withdrawal / reset model | Self-funded cashflow reality; decompound +5%/$200K-reset is the **reference instrument**, not a pre-chosen answer | Declared in §8 Phase-0 amendment before any MC — **not invented here** |

---

## §4 — Falsifiable hypothesis (H-SFRISK-1)

**H-SFRISK-1:** If a successor framework that jointly specifies the three §3 dimensions is evaluated on the decompound-remc instrument against the locked book, **requiring both regime halves (2020–2023 and 2023–2026) to clear the declared bars**, then either (a) at least one §8-declared triple is go-live-admissible without making the lane operationally impractical, or (b) every declared triple is shown unreachable / vacuous for stated geometric reasons — a binary outcome either way. Otherwise the framework is malformed (one half vacuous, or structurally un-passable before data — the Q-HARV-0 class of miss applied to risk gates).

**Reject H-SFRISK-1 if:** after the §8 Phase-0 numeric amendment and the pre-registered decompound run, **every** declared triple either (i) fails at least one regime half, or (ii) clears only by making the lane operationally impractical under the §8-declared impracticality bar — and no coherent admitting ADR can be written.

**Accept H-SFRISK-1 if:** at least one §8-declared triple clears **both** regime halves under the declared bars without crossing the §8 impracticality bar, and an admitting ADR (or HOLD with dated next action) can be written from the result.

**Ambiguous-hold if:** the leading triple clears one half and fails the other, or the instrument cannot discriminate (vacuous pass on a half) — re-test window named in the closure; no mid-investigation §6 edit.

**Structural falsifier already binding on this Pre-Q's existence** (transcribed verbatim from rescope ADR §4):

> **Completion falsifier (this ADR's own success bar):** if by **2026-11-08** (second quarterly) no successor risk-framework Pre-Q has been pre-registered (audit §5.2 / D1), the re-scope is judged **incomplete** — the historical label without a successor question is just a renamed vacuum — and D1 escalates to a mandatory blocker on any Aegis→M6J go-live decision.

*This OPEN brief + architecture §8 pre-registration discharges the existence half of that falsifier. Numeric freeze + MC remain gated on the Phase-0 amendment (rescope §5).*

---

## §5 — Forbidden moves

**Transcribed verbatim from [`docs/adr/2026-07-11-challenge-era-claims-rescope.md`](../adr/2026-07-11-challenge-era-claims-rescope.md) §5:**

- **Editing `dd_protection` constants, the display banner, or any executable line "while we're here."** Genuinely tempting (the FXIFY banner is now anachronistic; C2's grounds are void) — but constants are frozen re-MC-gated, and the zero-behavior-change scope is what makes this ADR safe to accept without a re-MC. D2 owns the calibration question at 08-08.
- **Deleting or weakening the anchor test pins / lock-criteria test.** They are re-scoped to engine regression pins, not removed — deleting them severs byte-reproducibility of the engine against its only validated benchmark.
- **Treating the re-scope as license to re-open rejected candidates or re-optimize.** Venue retirement is not new mechanism evidence; every `docs/rejected_candidates.md` bar stands (audit K7).
- **Switching `ACTIVE_FIRM` or patching the `None/100` crash without an onboarding ADR.** The fixture is load-bearing for anchor reproduction; a speculative fix has no validation target.
- **Running successor-semantics MC numbers before the D1 Pre-Q freeze.** Numbers-before-question is the family's own pre-registration violation; the first self-funded MC result must land against a frozen question set.
- **Letting the 08-08 diagnostic output be quoted as a live pass-claim.** The run is a fixed-benchmark health read; quoting its pass-rate as a live probability re-creates exactly the unfalsifiable claim this ADR retires.

**Pre-Q-local:**

- **Inventing numeric max-DD / TUW / withdrawal thresholds in this brief to look "locked"** — violates rescope §5; declare them only in the §8 Phase-0 amendment immediately before analysis.
- **Running decompound / successor MC before that Phase-0 numeric amendment is committed.**
- **Re-deriving D2 or D3 inside this brief** — sibling Class-D items; do not merge questions (Known Trap #11).
- **Quietly editing §6 after seeing MC output** — Known Trap #12; close AMBIGUOUS and open a fresh brief instead.

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED` | §8 Phase-0 numeric amendment committed **and** ≥1 declared triple clears both regime halves without crossing the §8 impracticality bar | Promote to admitting ADR / go-live risk artifact |
| `FALSIFIED` | §8 Phase-0 numeric amendment committed **and** every declared triple fails ≥1 half or only "clears" by crossing the impracticality bar | Close; capture lesson; go-live remains blocked pending a fresh Pre-Q |
| `AMBIGUOUS-HOLD` | Leading triple splits halves, or a half is vacuous / instrument cannot discriminate | Closure names re-test window; no §6 edit |

**Existence gate (rescope §4):** this Pre-Q + architecture §8 count as pre-registered for the 2026-11-08 completion falsifier. **Analysis gate (rescope §5):** no successor-semantics MC until the Phase-0 numeric amendment exists.

---

## §7 — Execution plan

1. **DONE** — freeze §3/§4 architecture + commit architecture §8 (2026-07-14).
2. **DONE** — Phase 0: §8 amended with T1 (F1/F3/F4), operator-confirmed "confirm T1" (2026-07-14).
3. **DONE** — Phase 1: `lab/analysis/regime/decompound_remc_2026-06-07/run_sfrisk_t1_phase1.py`, merged `936a9e0`, independently cross-validated (2026-07-15).
4. **DONE** — Phase 2: §6 asserted `RESOLVED`; [`docs/briefs/closures/Q-SFRISK-1-closure-resolved.md`](Q-SFRISK-1-closure-resolved.md) (2026-07-15).
5. **DONE** — Phase 3: admitting ADR drafted and ratified, [`docs/adr/2026-07-15-sfrisk-1-t1-admitting-successor-risk-framework.md`](../adr/2026-07-15-sfrisk-1-t1-admitting-successor-risk-framework.md) (`Accepted`, 2026-07-15). D2/D3 may now fork.

---

## §8 — Verdict pre-registration (mandatory before Phase 1)

**Architecture freeze:** [`docs/briefs/pre-registration/Q-SFRISK-1-verdict-preregistration.md`](pre-registration/Q-SFRISK-1-verdict-preregistration.md)

Pre-registration commit hash: `9b219ab` (numeric Phase-0 freeze)
Pre-registration date: 2026-07-14 (architecture); numeric Phase-0 amendment: **FROZEN 2026-07-14** — single triple T1 (F1 max-DD ≤10%/half + F3 ADOPT decompound withdrawal model + F4 impracticality >252bd; F2 TUW explicitly deferred, out of scope for this freeze). All halves of the rescope ADR §4 completion falsifier now discharged (existence, numeric, analysis, and verdict) — see [`docs/briefs/closures/Q-SFRISK-1-closure-resolved.md`](Q-SFRISK-1-closure-resolved.md).

---

## §9 — Closure record format

- **If RESOLVED:** `docs/briefs/closures/Q-SFRISK-1-closure-resolved.md` + admitting ADR / recommendation — **DONE 2026-07-15**: [`docs/briefs/closures/Q-SFRISK-1-closure-resolved.md`](Q-SFRISK-1-closure-resolved.md) + [`docs/adr/2026-07-15-sfrisk-1-t1-admitting-successor-risk-framework.md`](../adr/2026-07-15-sfrisk-1-t1-admitting-successor-risk-framework.md)
- **If FALSIFIED:** `docs/briefs/Q-SFRISK-1-closure-falsified.md`
- **If AMBIGUOUS-HOLD:** `docs/briefs/Q-SFRISK-1-closure-ambiguous.md` with explicit re-test trigger and date

---

## §10 — Audit hooks (runnable, not vague)

```bash
# Status CLOSED-RESOLVED (§6 fired, closure + admitting ADR landed)
grep -n "^\*\*Status:\*\*" docs/briefs/Q-SFRISK-1-successor-self-funded-risk-framework.md
# Expected: CLOSED-RESOLVED

# Closure + admitting ADR both present
test -f docs/briefs/closures/Q-SFRISK-1-closure-resolved.md
test -f docs/adr/2026-07-15-sfrisk-1-t1-admitting-successor-risk-framework.md

# Rescope §10-style hook — successor / self-funded Pre-Q present
ls docs/briefs/ docs/briefs/pre-registration/ | grep -iE "selffunded|self-funded|successor|SFRISK"

# Completion falsifier hard date still cited (now discharged, not just pending)
grep -n "2026-11-08" docs/briefs/Q-SFRISK-1-successor-self-funded-risk-framework.md docs/adr/2026-07-11-challenge-era-claims-rescope.md
grep -n "D1 completion falsifier discharged" docs/adr/2026-07-11-challenge-era-claims-rescope.md

# Reference instrument present
test -d lab/analysis/regime/decompound_remc_2026-06-07
test -f docs/adr/2026-06-07-decompound-remc-hold.md

# Architecture §8 exists; numeric amendment RATIFIED and run
test -f docs/briefs/pre-registration/Q-SFRISK-1-verdict-preregistration.md
grep -n "NUMERIC FROZEN" docs/briefs/pre-registration/Q-SFRISK-1-verdict-preregistration.md
test -f lab/analysis/regime/decompound_remc_2026-06-07/RESULTS_sfrisk_t1_phase1_2026-07-15.md

# Validators untouched (docs-only)
python scripts/verify_lock_anchors.py
# Expected: ROUTING: Closed
```

---

## Verification

```bash
python scripts/check_brief.py docs/briefs/Q-SFRISK-1-successor-self-funded-risk-framework.md --type inquire
# Expected: 0 HARD

git log -1 --format='%h %ci' -- docs/adr/2026-07-11-challenge-era-claims-rescope.md
# Expected: 99b7854 …
```
