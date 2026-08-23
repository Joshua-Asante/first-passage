# Q-CALLBOUND-1 — Closure: `AMBIGUOUS-HOLD` (D3 clean, D6 inconclusive-adjacent hit)

**Verdict:** `AMBIGUOUS-HOLD`
**Closed:** 2026-08-23 (same session as operator GO + Phase 1 execution)
**Lane:** `UNASSIGNED`
**Brief:** [`Q-CALLBOUND-1-automation-boundary-symmetry.md`](../Q-CALLBOUND-1-automation-boundary-symmetry.md)
**Pre-registration:** [`Q-CALLBOUND-1-verdict-preregistration.md`](../pre-registration/Q-CALLBOUND-1-verdict-preregistration.md) — frozen 2026-08-23, before Phase 1 ran
**Spend / K:** $0.00 · K consumed: 0 (grep-and-read sweep only, per the brief's own Loop line)
**Live effect:** none. c1 rail stays built/warm/**disarmed** (`dry_run=true`); no strategy deployed; no line of `core/lifecycle.py`, `dd_protection.py`, `firm_rules.py`, or `ops/c1_rail/` touched.
**Artifacts:** this file; the pre-registration above; no code/constant/ADR edited under this brief.

---

## 1. Verdict (§6 asserted against actual numbers)

| §6 route | Trigger (frozen) | Actual | Fired? |
|---|---|---|---|
| `RESOLVED` | D3 grep clean **AND** D6 diff zero overlap | D3 clean; D6 diff has **one** non-trivial file-level overlap (docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md) — not zero | — |
| `FALSIFIED` | Genuine reverse-path (D3) **or** genuine floor-to-zero/Call-5 connection (D6) | D3: none found (124 hits, all classified, none a criteria-gated up-path). D6: the one overlap co-locates the vocabularies but, on read, ties floor-to-zero to the **M1 arming gate's** sign-off, not to **Call-5's** — not a genuine Call-5 connection | — |
| `AMBIGUOUS-HOLD` | Either check returns a topically-adjacent but inconclusive hit | D6 matches the Section-4 example verbatim ("a zero-contract mention that doesn't reach Call-5 vocabulary") | **✓** |

D3 alone would have closed `RESOLVED`-eligible; the Combined-H structure (§4: "holds only if both limbs hold") means D6's inconclusive hit controls the overall verdict.

## 2. What the pre-registration predicted vs what happened

§E predicted `RESOLVED` on D3 and an `AMBIGUOUS-HOLD`-leaning D6, on the reasoning that the c1 rail's own ADRs are "the only place both a floor-to-zero mechanism and an operator-sign-off gate coexist in the same document." That prediction landed exactly: `docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md` is the one file that surfaces the overlap, and reading it in full confirms it is adjacent-not-connecting — the document discusses two different named operator sign-offs (M1's arming interlock at L547/764, Call-5's lifecycle boundary at L272-274) and one floor-to-zero mechanism (L699-702, L803-805), but never states the floor-to-zero fact requires or is exempt from Call-5's sign-off specifically. No surprise fired.

## 3. What this closure does NOT license

- **Not** a finding that the Call-system boundary is broken. D3 is clean; D6 is unresolved, not falsified — no genuine gap is priced.
- **Not** grounds to build a promote function, add a Call-5 sign-off to the sizing host, or wire any warning. Section 5's forbidden moves bind this closure exactly as they bound the brief.
- **Not** live-risk news. No strategy is deployed and `dry_run=true`; the ambiguity is about corpus vocabulary, not an active exposure.
- **Not** a claim that `docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md` is defective — it correctly scopes its own "operator sign-off" to the M1 gate it is about; the ambiguity is that no *other* document has yet said whether Call-5's WATCH-2->RETIRED boundary has anything to say about a routine per-trade `qty_out=0`, and this closure does not manufacture that statement.

## 4. Defects found in the frozen brief (recorded, not repaired)

None. The brief's Section 4 Ambiguous-hold clause anticipated and named the exact scenario found ("a zero-contract mention that doesn't reach Call-5 vocabulary") before any grep ran — the pre-registration and gate table needed no reinterpretation to route this result.

## 5. Lesson candidates

**Candidate (methodology, first instance — below the two-incident promotion bar, watch only):** a $0/K=0 vocabulary-diff instrument, run over broad single-word patterns (`RETIRED`, `sign.off`, `zero.fill`), reliably produces same-file-but-different-referent false-adjacency (here: two distinct operator-sign-off gates, M1 and Call-5, sharing generic phrasing in one omnibus ADR). The pre-registered Ambiguous-hold clause absorbed this correctly on the first firing; no repair is owed unless a second instance shows the clause under-specified. No dollar anchor — $0 spend, no live effect.

## Iterate — loop exit (MANDATORY)

- **Verdict used:** `AMBIGUOUS-HOLD`
- **Model update:** D3 confirms the down-only asymmetry is real and total in code — `core/lifecycle.py` has exactly two state-movers and both go down; the "cheap because reversible" reasoning behind sigma=1.0 (the governance ADR's own driver) is *unexercised*, not *false* — there is no operator-executable reverse path to test whether reversal is actually cheap, but nothing in the corpus claims one exists either, so D3 finds an honest gap in exercise, not a misrepresentation. D6 shows the repo's two operator-sign-off gates (M1 arming, Call-5 lifecycle) are architecturally adjacent — both live in the c1 rail's orbit, both use "operator sign-off" as generic phrasing, and one ADR discusses a floored-to-zero decision's evidentiary weight for M1 without ever asking the analogous Call-5 question. The gap D6 was built to find (audit note D6) is not resolved in either direction — it remains open exactly as the audit note stated it, now with a citation trail instead of an assertion.
- **Next:** ITERATE
- **Routing:** ITERATE — Investigate (tighter test), not Q-reframe or H-rewrite. A successor is named, not opened: a follow-up would need to either (a) find or write an explicit statement of whether a routine `qty_out=0` at the sizing host should carry Call-5 weight, or (b) treat the silence as a considered non-issue (a floored trade does not change the strategy's *authorization tier* — it stays AUTHORIZED/WATCH-1 at 1.0x/0.5x; only the tier multiplier, not any single trade's size, is what Call-5 governs) and close the audit note's D6 finding as a documented-non-issue via a light ADR addendum, not a fresh Q.
- **Entry packet:** frozen quotes and line numbers from `docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md` (L272-274, L547, L699-706, L764, L803-805); the D3 confirmed-clean 124-hit classification; the two named D3 exceptions (gitignored hand-edit; whole-ADR Type-I revert trigger, `docs/adr/2026-07-10-...` §4 L195-200); this closure's §1 verdict table.
- **Stop rule / re-proposal bar:** re-test only if (a) a leg is actually floored to zero **live** (not hypothetical — D6 becomes a real-money question, not a corpus-silence question), or (b) a future session genuinely needs the D3 reverse path (e.g. a demoted incumbent's restoration becomes operationally relevant). Absent either trigger, this thread stays dormant — do not re-run the same $0 grep expecting a different vocabulary-adjacency result.
- **Board write:** `STATE.md` — Dormant cross-session threads / No fixed date-gated: "Q-CALLBOUND-1 (Call-system automation-boundary symmetry) — CLOSED AMBIGUOUS-HOLD 2026-08-23. D3 (reverse-path symmetry) CONFIRMED clean. D6 (floor-to-zero/Call-5 completeness) inconclusive — docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md co-locates floor-to-zero language with a *different* gate's (M1) operator sign-off, not Call-5's. Re-test only if a leg floors to zero live, or a session needs the D3 reverse path. Closure: docs/briefs/closures/Q-CALLBOUND-1-closure-ambiguous-hold.md."
- **Registry:** `n/a — governance/completeness Q, not a strategy-grounds kill; no rejected_candidates.md row owed.`

## §10 audit-hook discharge

```text
$ python scripts/check_brief.py docs/briefs/Q-CALLBOUND-1-automation-boundary-symmetry.md --type inquire
note: 'inquire' is a skill-side brief type; ran repo-side mechanical subset (type=brief)
Summary: 0 HARD violation(s), 0 WARN violation(s)
RESULT: well-formed

$ sed -n '149,166p' core/lifecycle.py                                          -> matches Section 0 verbatim
$ sed -n '66p;71p;213p' docs/adr/2026-07-10-...lifecycle-governance.md          -> matches Section 0 verbatim
$ sed -n '86,94p' docs/methodology/strategy_lifecycle.md                        -> matches Section 0 verbatim (extended read to :96-97, no drift)
$ sed -n '23p;55p' docs/adr/2026-08-07-loop-s5-bounded-promotion-lane.md        -> matches Section 0 verbatim
$ sed -n '280p;286,300p' ops/c1_rail/c1_sizing_host_reference.py                -> matches Section 0 verbatim
$ grep -n "NOT-M8" ops/instruments/MNQ.md                                       -> now line 149 (was :143 at authoring; append-only log growth, content unchanged, consistent with the brief's own note)

$ rg -i "promote|re-authoriz|reauthoriz|restore.tier|restore.authoriz|WATCH.to.AUTHORIZED" core/ docs/adr/ docs/methodology/ STATE.md
-> 124 hits, all read and classified; 0 genuine reverse-path procedures (D3 CONFIRMED)

$ rg -n "def next_tier_down|def autonomous_demote" core/lifecycle.py
-> exactly 2 defs, both down-only movers; no third mover

$ rg -in "zero.contract|zero.fill|NOT-M8|qty_base" --type py --type md
-> 43 files; intersected against the 5-location Hook-B scope -> 7 candidate files, 1 self-referential (excluded), 6 read in full

$ rg -in "operator.GO|sign.off|RETIRED|Call.5" docs/adr/ docs/methodology/ docs/rejected_candidates.md docs/briefs/INDEX.md STATE.md
-> ~90 files (broad vocabulary); intersection with Hook-A yields the same 7-file candidate set above
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-23 | Closure authored `AMBIGUOUS-HOLD` — D3 CONFIRMED clean (no reverse-path beyond the two named exceptions); D6 inconclusive (one topically-adjacent, non-conclusive hit at `docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md`, co-locating floor-to-zero language with the M1 gate's — not Call-5's — operator sign-off). $0.00 spend, K=0, no live effect. Pre-registration frozen same session before Phase 1 ran; prediction landed on both limbs. | Joshua (GO) + Claude Code |
