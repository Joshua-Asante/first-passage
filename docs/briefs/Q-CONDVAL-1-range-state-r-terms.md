# Q-CONDVAL-1 — Does the validated CL range-state lift buy anything in R terms?

**Status:** `CLOSED-FALSIFIED 2026-08-18` — L=0.1297 < L_star=0.4226; conditioner-engineering branch parked. Closure: [`closures/Q-CONDVAL-1-closure-falsified.md`](closures/Q-CONDVAL-1-closure-falsified.md).
**Authored:** 2026-08-18
**Closed:** 2026-08-18
**Authors:** Joshua (operator GO: "GO on Q-CONDVAL-1") + Cursor (execution)
**Parent question:** [`N-2026-08-18-iteration2-identify-notice`](../notes/notice/N-2026-08-18-iteration2-identify-notice.md) observation D / §5 packet 1
**Sub-questions opened:** none
**Loop:** Inquire-phase Pre-Q — closure gated on whether committed CL C−U lift clears a pre-declared `L_star`
**Artifact path:** `docs/briefs/Q-CONDVAL-1-range-state-r-terms.md`
**Pre-registration:** [`pre-registration/Q-CONDVAL-1-verdict-preregistration.md`](pre-registration/Q-CONDVAL-1-verdict-preregistration.md)

**D-S-A domain:** data (already-committed S1b numbers → one R-term comparison)
**Pre-Q gate:**
```
D: deleted from this Q's working set — (i) the spec O2 0.60 DECLARED-NOT-DERIVED
   rate [test: known undeclared input; using it would launder the number this Q
   exists to derive]; (ii) IAAFT-excess (obs − surrogate-band center) [test:
   out of scope of the packet's "measured lift = conditional-minus-unconditional"
   form; excess is a different question]; (iii) S1a/GC lift [test: wrong
   instrument]. No forbidden D-test. Raw sources remain the Rule-0 anchor.
S: corpus is two committed scalars (gateHit, p_up_unconditional) plus the three
   frozen parameters. Compression preserves observation D (typed finding, zero
   demonstrated economics).
A: L vs L_star is one subtraction. Q-cost is O(read the prereg + run the runner).
```

---

## §0 — Rule 0 reads (production-source verification, executed 2026-08-18)

Worktree `main` fast-forwarded to `origin/main` `f9fcab5` this session, then branched
`cursor/q-condval-1`. Each path read before the prereg was written:

- `docs/notes/notice/N-2026-08-18-iteration2-identify-notice.md` — anchor `8f74f93` (2026-08-18). Packet 1: three free parameters before the lift is read; 0.60 forbidden; decision = conditioner-engineering GO or park.
- `docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md` — anchor `d3a0bc4` (2026-08-18). O2: 0.60 is DECLARED-NOT-DERIVED; connecting arithmetic owed here. A6: SIGNAL-GENERIC is not a conditioner license.
- `lab/analysis/_inbox/rangestate_corrected_2026-08/RESULTS_CORRECTED.md` — anchor `d3a0bc4`. Official S1b = SIGNAL-GENERIC; frozen obs carried verbatim; O2 still owed.
- `lab/analysis/_inbox/rangestate_mcl_2026-08/RESULTS_S1B.md` — anchor `d3a0bc4`. Object definition + addendum. **The lift scalars are not substituted in this brief; they are read only by the runner after the prereg sha256 is recorded.**
- `docs/adr/2026-08-13-msl-slate-2-design-box.md` — anchor `027a729` (public-release squash). Elected box: rr ∈ [2, 3], WR 0.30–0.42, hard stop, k=1.
- `docs/notes/notice/N-2026-08-13-msl-design-box-rederivation.md` — anchor `1f3a2bb` (2026-08-15 restore). §9 `solve()` and the $4.12 non-index pin.
- `docs/spec/2026-08-08-tradeify-necessary-conditions-target-spec.md` — anchor `027a729`. N-EDGE = net > 0 after Req-5 costs; 0.40R is disclosure-only. The +0.10R @$75 quantum lives in the seed-target RESULTS / 2026-08-08 necessity-retarget ADR, cited by the parent notice.
- `docs/adr/2026-08-08-edge-cohort-correction-and-necessity-retarget.md` — read this session. Admissibility reaches ≈ +0.10R at $75/trade.
- `ops/instruments/MCL.md` / `MECHANISMS.md` — read this session. Cell currently `AMBIGUOUS-PARKED` in the yaml (stale vs SIGNAL-GENERIC RESULTS); MECHANISMS still routes to an electable conditioner-engineering prereg.

**HANDOFF-VERIFY (this session):** PASS. toplevel `C:/Users/joshu/multi_firm_operations`; branch `cursor/q-condval-1` off `f9fcab5`; named packet paths exist; Q-CONDVAL-1 not already executed (see pasted searches); no live-book / Striker / armed-rail premise in the packet.

**Sub-rule 8 / 10 attestation (literal output, 2026-08-18, this worktree):**

```
# lab/CATALOG.md
rg -n "CONDVAL|q_condval|range-state lift|conditioner-engineering" lab/CATALOG.md
→ no matches
# (CATALOG _inbox lists rangestate_mcl_2026-08 / rangestate_corrected_2026-08 as
#  the finding owners — SIGNAL-GENERIC / official re-score — not this Q)

# docs/briefs/INDEX.md
rg -n "CONDVAL|q_condval|range-state lift|conditioner-engineering" docs/briefs/INDEX.md
→ no matches

# docs/rejected_candidates.md
rg -n "CONDVAL|q_condval|range-state lift|conditioner-engineering" docs/rejected_candidates.md
→ no matches

# python scripts/check_advisor_dedup.py --keywords "CONDVAL conditioner range-state lift R-terms"
# slugs found: (none)
# top hits are keyword coincidences (range/state/terms/lift) — MNQBASE-1,
#  Q-CAPBAND-1, Q-EVALSEQ-1, 2026-08-18d SESSIONS. None is this Q.
```

**Sub-rule 10 — existing owner:** the notice *names* this Q as a GRADUATE packet
("named, not opened"). The finding owner is `RESULTS_S1B` / `RESULTS_CORRECTED`
(O2 owed). A new Inquire brief is the exception the notice itself specified;
amending the notice into a Pre-Q would mix types. No existing `docs/briefs/Q-CONDVAL-*`.

---

## §1 — Context & motivation

S1b's official verdict is SIGNAL-GENERIC: next-day True-Range is predictable at
the pooled construction from yesterday's top-quintile TR, and that predictability
is generic volatility clustering. ADDENDUM-1 A6 bars quoting it as a conditioner
license. Spec O2 recorded that L4's power math used a 0.60 "minimum-useful"
conditional rate with **no** connecting arithmetic from the 4× cost hurdle — and
explicitly owed that arithmetic to the conditioner-engineering lane.

Observation D of the iteration-2 notice: the branch's continuation is currently
justified by the verdict *string*, not by economics. This Q is the $0 kill-or-keep
that runs **before** any conditioner-engineering prereg. A park closes the S1b
engineering branch and discharges O2. A clear leaves that prereg electable, still
under A6 rails (calm-regime OPEN, O3 lift gate, L4 boundary, new K).

Standing clock: 82 days to 2026-11-08; base case is §4 FALSIFIED. This Q does not
pretend otherwise.

---

## §2 — Prior art / lineage

- **Parent notice** `N-2026-08-18-iteration2-identify-notice` — names the packet, the three levers, and the forbidden 0.60 input. ⚠ The notice's inline "+0.052 C−U, 41st percentile of its own surrogate lift band" is the **GC** lift from `RESULTS_CORRECTED` §1, attributed there to S1b. This brief does not use that number; the runner reads CL keys only.
- **Corrected-null spec O2 / A6** — this Q *is* the owed O2 arithmetic; A6 still binds after either verdict.
- **MSL slate-2 design box** (`Accepted` 2026-08-13) + rederivation §9 — default host geometry and the $4.12 non-index pin.
- **Q-POLFRONT-1 intraday-honest** — deleted the 5.1× EOD frontier from the question corpus (notice D-test i); envelope R ≈ $75–200 is the retained clock.
- **Necessity-retarget ADR / seed-target RESULTS** — ≈ +0.10R @$75 is the N-EDGE quantum the material fraction is pinned to.
- **Q-TXG-1** (`FALSIFIED-at-walls`) — adjacent prior art on cost-tax vs expression, **not** this unit of analysis (this Q is one finding × one host box, not the conversion-step census). Cited so it is not rediscovered.
- **No prior Q-CONDVAL-*.** Tail-methodology: new framing (economics of a typed GENERIC finding), not a 4th H on the same thread.

---

## §3 — Question (Q-CONDVAL-1)

**Pre-Q gate test (symptom-only rephrase):** "a typed range-state finding has no demonstrated R-term content at the envelope the estate actually sizes in; it is unknown whether the committed lift moves N-EDGE by a pre-declared fraction of the cost hurdle, or whether the conditioner branch is continuing on a verdict string." No fix baked in — the question does not say "build a conditioner" or "raise 0.60."

**Q-CONDVAL-1:** At the intraday-honest envelope, what C−U lift must a range-state conditioner deliver to move a slate-2 host's N-EDGE arithmetic by the pre-declared material fraction of `hurdle_4x` — and does CL's committed lift reach it?

---

## §4 — Falsifiable hypothesis (H-CONDVAL)

**H-CONDVAL:** If the committed CL lift `L = gateHit − p_up_unconditional` is
**≥** the pre-declared `L_star = 0.422564` (prereg §A), then the finding has
economic content at the N-EDGE reference cell and the conditioner-engineering
prereg stays electable. **Otherwise** the lift does not buy a material fraction
of the cost hurdle and the S1b conditioner-engineering branch parks.

**Accept H-CONDVAL → `RESOLVED` if:** `L ≥ L_star`.
**Reject H-CONDVAL → `FALSIFIED` if:** `L < L_star`.
**`AMBIGUOUS-HOLD` if:** either committed key is missing, or `E_box ≤ 0` at the gating cell.

---

## §5 — Forbidden moves

- **Using the spec's 0.60 as an input.** Tempting because it sits next to obs_CL 0.6282 and was already used for L4 power. It is DECLARED-NOT-DERIVED; this Q exists to replace it. Ruled out by the parent packet.
- **Choosing `rr` / `WR` / `R` / `RT` / the 0.50 fraction after seeing `L`.** Each lever swings the verdict (the packet said so). Ruled out by prereg §A freeze + sha256-before-substitute.
- **Substituting IAAFT-excess for raw C−U.** Tempting because GENERIC means the raw lift is mostly clustering. That is a different question ("does *excess* buy anything?"). The packet asked whether the *validated lift a conditioner actually delivers* (yesterday-TR filter → today's range-state) buys anything. Clustering is what you get when you filter.
- **Gating on a disclosure corner to rescue a miss.** The center is the declared cell. Corners are disclosure.
- **Reading KEEP as a mechanism, or PARK as a retraction of SIGNAL-GENERIC.** A6 rails: the finding stays GENERIC; this Q prices it, it does not re-try the battery.
- **Opening the conditioner-engineering prereg from a `FALSIFIED` close.** That is the decision this Q exists to refuse.

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition (typed) |
|---|---|---|
| `RESOLVED` | `L ≥ L_star` (0.422564), keys present, `E_box = 0.26 > 0` | `INTEGRATE` — O2 discharged as "lift clears at the N-EDGE cell"; conditioner-engineering prereg remains electable under A6 (calm-regime, O3, L4 boundary, new GO / new K) |
| `FALSIFIED` | `L < L_star`, keys present | `STOP` — park the S1b conditioner-engineering branch; O2 discharged as "required lift derived; measured lift misses"; re-proposal = a *different* host geometry declared *before* a re-read, or a new finding, not a θ move of `L_star` |
| `AMBIGUOUS-HOLD` | missing keys or `E_box ≤ 0` | `ITERATE` — recover `L` from another committed source; do not invent |

**Pre-registered before the runner substitutes `L`.** Trap #12: if the bar must move, close this brief and open a fresh one.

---

## §7 — Execution plan (self-executing, this session)

- **Phase 0 — Rule-0 reads.** This §0. Done before the prereg was written.
- **Phase 1 — Freeze.** Prereg on disk. Runner records sha256 of the prereg bytes **before** opening `s1b_results.json`.
- **Phase 2 — Arithmetic.** `lab/analysis/_inbox/q_condval_1_2026-08/run_condval.py` reads the two keys, computes `L`, `ΔE`, compares to `L_star`. Stdlib + the committed JSON only. $0 / K=0.
- **Phase 3 — Verdict assertion.** Apply §6. Write RESULTS + closure. Propagate MECHANISMS / MCL pointer / INDEX / STATE / SESSIONS.

---

## §8 — Verdict pre-registration

File: [`pre-registration/Q-CONDVAL-1-verdict-preregistration.md`](pre-registration/Q-CONDVAL-1-verdict-preregistration.md)

Pre-registration commit hash: *(same-session freeze; sha256 `d1265eb2b0fa328c18b8a744a6f438d06611238fd2ada14ca12d06645748b386` recorded by the runner before substitute; git hash lands at operator commit)*
Pre-registration date: 2026-08-18

---

## §9 — Closure record format

- **If RESOLVED:** `docs/briefs/closures/Q-CONDVAL-1-closure-resolved.md`
- **If FALSIFIED:** `docs/briefs/closures/Q-CONDVAL-1-closure-falsified.md`
- **If AMBIGUOUS-HOLD:** `docs/briefs/closures/Q-CONDVAL-1-closure-ambiguous.md`

Mandatory typed `## Iterate` block. Registry: `n/a` on RESOLVED (not a strategy-grounds kill) or `rejected_candidates.md` only if the close is a strategy-grounds STOP of a *candidate* — this Q parks an engineering *branch* of a GENERIC finding, not a harvest seed; default `n/a — conditioner-branch park, finding stands`.

---

## §10 — Audit hooks

```bash
# Graduation lineage
rg -n "N-2026-08-18-iteration2-identify-notice" docs/briefs/Q-CONDVAL-1-range-state-r-terms.md

# 0.60 never used as an input (may appear only as FORBIDDEN)
rg -n "0\.60" docs/briefs/pre-registration/Q-CONDVAL-1-verdict-preregistration.md lab/analysis/_inbox/q_condval_1_2026-08/

# Freeze-before-substitute: runner printed prereg sha256 before the JSON lift
rg -n "prereg_sha256" lab/analysis/_inbox/q_condval_1_2026-08/RESULTS.md

# Reproduce
python lab/analysis/_inbox/q_condval_1_2026-08/run_condval.py
# Expected: bit-identical L, L_star, verdict vs RESULTS.json

# Discipline
python scripts/check_brief.py docs/briefs/Q-CONDVAL-1-range-state-r-terms.md --type inquire
```

---

## Verification

```bash
python scripts/check_brief.py docs/briefs/Q-CONDVAL-1-range-state-r-terms.md --type inquire
git log -1 --format=%h -- docs/notes/notice/N-2026-08-18-iteration2-identify-notice.md
# expected: 8f74f93
```
