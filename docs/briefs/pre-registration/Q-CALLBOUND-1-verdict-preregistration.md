# Q-CALLBOUND-1 — Verdict pre-registration (H-CALLBOUND)

**Frozen:** 2026-08-23, before any Phase-1/Phase-2 grep is read. Parent brief: [`Q-CALLBOUND-1-automation-boundary-symmetry.md`](../Q-CALLBOUND-1-automation-boundary-symmetry.md). Operator GO recorded in-session 2026-08-23 (parent-Q convention: naming is not opening; this GO opens it).

---

## §A — Pinned inputs (frozen; mirrored verbatim from the parent brief's §0/§4 — no substitutions)

| Input | Value | Source |
|---|---|---|
| D3 down-only citations (the floor to compare grep results against) | `core/lifecycle.py:21-23,149-166`; `docs/adr/2026-07-10-...:66,71,213`; `docs/methodology/strategy_lifecycle.md:86-94`; `docs/adr/2026-08-07-loop-s5-bounded-promotion-lane.md:23,55` | Parent brief §0 |
| D3 named exceptions (do NOT count as satisfying symmetry) | (a) undocumented hand-edit of gitignored `lifecycle_state.json`; (b) the ~6-month whole-ADR Type-I-dominance revert trigger | H-CALLBOUND-D3 |
| D6 sizing-host citation | `ops/c1_rail/c1_sizing_host_reference.py:280,286-300` — `qty_base_raw = floor(...)`, `qty_out = min(qty_base_raw, reserve_cap)`, no zero-guard, no distinct "floored to zero" code path | Parent brief §0 |
| D6 NOT-M8 citation | `ops/instruments/MNQ.md` (line drifts session to session — append-only log; content is the pin, not the line number) | Parent brief §0 |
| D3 grep (Phase 1, exact command) | `rg -i "promote\|re-authoriz\|reauthoriz\|restore.tier\|restore.authoriz\|WATCH.to.AUTHORIZED" core/ docs/adr/ docs/methodology/ STATE.md` | Parent brief §10 |
| D6 grep pair (Phase 2, exact commands) | `rg -in "zero.contract\|zero.fill\|NOT-M8\|qty_base" --type py --type md` **and** `rg -in "operator.GO\|sign.off\|RETIRED\|Call.5" docs/adr/ docs/methodology/ docs/rejected_candidates.md docs/briefs/INDEX.md STATE.md` | Parent brief §10 |

**The two grep commands are closed at exactly this text.** No pattern may be widened or narrowed at execution time — that would be selecting evidence after seeing the question.

## §B — Falsifiable hypothesis (verbatim from parent §4)

**H-CALLBOUND-D3 (symmetry):** No operator-executable, criteria-gated procedure anywhere in the corpus (code, ADR, or methodology doc) restores an autonomously demoted `AUTHORIZED` incumbent leg, short of an undocumented hand-edit of a gitignored state file or the ~6-month whole-ADR Type-I-dominance revert trigger.

**H-CALLBOUND-D6 (completeness):** No repo doc, ADR, code comment, or Q-roster entry anywhere connects the sizing host's routine integer-floor-to-zero outcome to Call 5's operator-GO/NO-GO boundary as requiring, or being exempt from, that same sign-off.

**Combined H-CALLBOUND:** the boundary holds as designed only if **both** limbs hold.

## §C — Method (mechanical grep classification; no free tolerance parameter)

For D3: every hit from the Phase-1 grep is read in full and classified as either (i) a citation of the already-known down-only/S5-exception statements, (ii) an unrelated-domain "promote" usage (methodology-lesson registry, other gate admission, ADR ratification, code-module graduation), or (iii) a genuine criteria-gated up-path for an already-demoted incumbent. Only (iii) falsifies.

For D6: intersect the Hook-A (zero-contract vocabulary, whole tree) file set against the Hook-B (operator-GO/sign-off/RETIRED/Call-5 vocabulary, five named locations) file set. Every file in the intersection is read at its matched lines and classified as: clean miss (different sense of the matched word — e.g. "zero-fills attestation," "zero contract benefit"), genuine connection (explicitly ties floor-to-zero to Call-5's sign-off, either direction), or topically-adjacent-inconclusive (co-locates the two vocabularies but on read refers to two distinct named gates, or is otherwise not conclusive).

## §D — Decision rule (verbatim from parent §6)

| Verdict | Trigger condition | Disposition (typed) |
|---|---|---|
| `RESOLVED` | D3 grep returns nothing beyond §A's down-only citations **AND** D6 diff returns zero overlap | `INTEGRATE` — record both gaps as confirmed-and-costless-today; discharge D3/D6 from the audit note's open-findings list; no constant or code moves. |
| `FALSIFIED` | Either grep/diff surfaces a genuine reverse-path procedure (D3) or a genuine floor-to-zero/Call-5 connection (D6) | `ITERATE` — the specific gap is priced with a citation; name (do not open) a successor. No constant or code moves under this brief. |
| `AMBIGUOUS-HOLD` | Either check returns a topically-adjacent but inconclusive hit (e.g. a generic "promote" hit in an unrelated context, or a zero-contract mention that doesn't reach Call-5 vocabulary) | `ITERATE` — record as unresolved-by-grep; re-test only if a future session needs the reverse path (D3) or a leg is actually floored to zero live (D6). |

**Neither RESOLVED nor AMBIGUOUS-HOLD moves any code, constant, or arming posture.** A `FALSIFIED` limb is priced, not repaired, under this brief.

## §E — Pinned ex-ante expectation (surprise marker)

**Predicted: `RESOLVED` on D3, `AMBIGUOUS-HOLD`-leaning on D6.** Reasoning recorded before the read: D3's grep pattern is narrow and core/lifecycle.py's own docstring (§0) already states no promote function exists — a clean corroboration is the expected outcome. D6 is the riskier limb: "zero-contract" and "RETIRED"/"sign-off" are both common enough repo vocabulary (RETIRED alone spans OANDA/dukascopy/CFD-estate/FXIFY retirements) that a same-file false-positive co-location is plausible even absent a genuine connection, and the c1 rail's own ADRs are the most likely place for the two vocabularies to naturally co-occur (they are the only place both a floor-to-zero mechanism and an operator-sign-off gate coexist in the same document) — making an AMBIGUOUS rather than a clean RESOLVED the more likely D6 outcome. A clean `RESOLVED` on D6 would be the mild surprise; a genuine `FALSIFIED` connection would be the large surprise.

## §F — Forbidden moves (inherited verbatim from parent §5)

1. Reading "no promote path exists" as itself a defect requiring a fix.
2. Treating S5's bounded sandbox-up lane as if it answers D3 (S5 admits only brand-new `CANDIDATE` packets, not incumbent restoration).
3. Collapsing D6 into "the zero is numerically correct, so it's fine" (NOT-M8 answers a different, already-closed question).
4. Scoring this Q on the c1 book's live risk today (no strategy deployed, `dry_run=true`; a `FALSIFIED` verdict prices a governance gap, not live exposure).

---

**Freeze note:** committed before Phase 1 of the parent brief reads any grep output this session. No D3 or D6 fact has been read at the time of this freeze.
