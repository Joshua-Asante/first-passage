# NOTICE 2026-08-23 — ox-alpha sanitized review: MSL WHO-sourcing methodology

**Notice ID:** N-2026-08-23-ox-alpha-msl-who-sourcing-methodology-review
**Observed:** 2026-08-23
**Author:** Claude Code (Sonnet 5), operator direction ("ask ox-alpha how to approach sourcing a
new WHO for MSL")
**Type:** Notice-phase. External adversarial-lens review, reconciled against real repo state.
$0 · K=0 · no camp · no card. No live-risk surface touched.
**Status:** `RESOLVED` — reconciliation complete; several objections survive, several do not.

---

## §0 — Governance basis

Sent under [`docs/adr/2026-08-22-ox-alpha-adversarial-lens-scope.md`](../../adr/2026-08-22-ox-alpha-adversarial-lens-scope.md)
§2's **base scope** (adversarial second-opinion lens on a drafted artifact) — not the separate,
already-used-once bounded-extension addendum (candidate generation). The ask was framed and sent
as a critique of the existing MSL WHO-sourcing methodology/coverage (the WHO-track sweep,
`N-2026-08-14-msl-who-track.md`, and the Req 1a WHO/WHEN/WHY/HOW admission bar) for structural
blind spots — not as a request to generate new strategy ideas directly. No fresh bounded-extension
authorization was invoked.

**Sanitization applied:** no firm name, instrument ticker, dollar figure, or named-construct
identifier (e.g. no "Tradeify," "MYM/MNQ/MGC/M2K," "$0.91/side," "pdh-pdl-failed-break-reclaim,"
"expiry-oi-strike-convergence") appears in the sent prompt. The constraint set (trailing-DD
budget, consistency/payoff-concentration rule, weekly-activity rule), the WHO/WHEN/WHY/HOW
admission bar, the delete/flip test, and the already-killed mechanism *categories* were described
generically. No proprietary content is reconstructable from the sent prompt or the response.

**Send/receive record:** `stealth/ox-alpha` via OpenRouter chat-completions, 2026-08-23.
prompt_tokens=1,490 / completion_tokens=18,224 (72,366-char hidden-reasoning channel, not stored
— matches this ADR's own prior no-transcript-for-reasoning-channel precedent). finish_reason=stop.

---

## §1 — Reconciliation table (objection vs. real repo state)

| ox-alpha objection | Real repo state | Survives reconciliation? |
|---|---|---|
| "Macro-print (CPI/NFP/FOMC) kills on equity index were probably a mis-generalized 'size' argument — MES/MNQ exist for small accounts." | `docs/briefs/closures/MNQBASE-1-closure-intake-dry.md`: **Event-day trend (FOMC/CPI/NFP/PCE) — FAIL.** Killed on drift-persistence (T=0.14–0.69 decaying from bar+6) and an RTH-timing mismatch (NFP/CPI print at 08:30 ET, outside the eval's regular session) — not on instrument size at all. | **No** — the actual kill reason is unrelated to and independent of what ox-alpha assumed. |
| "Index-methodology events (rebalance add/delete, index-roll) are a distinct, cleaner-signed mechanism the sweep missed." | GSCI/BCOM roll: explicitly tested and `BARRED (spread-shaped)` (`cheap_falsifiers_2026-08/_probe_stage0_RESULTS_2026-08-11.md`). Russell reconstitution: explicitly tested and `FAIL Req 2 + Req 4` — the published cohort is a cross-sectional *stock* effect, transplanting it to a futures-index directional bet is the forbidden cross-domain move, **and** it's annual (N≈5 over the whole panel — fails frequency by orders of magnitude) (`lab/analysis/c1/wstruct_cost_geometry_2026-07-28/RESULTS.md`). | **No** — both named sub-mechanisms already tested and killed, on stronger/more specific grounds than the objection assumed. |
| "Gamma sign is estimable from public OI/strike data — the 'dealer can be long or short gamma' kill treated an estimable state as a discretionary assumption." | Tested repeatedly and independently: `docs/rejected_candidates.md` — *"the signal must also be orthogonal to \|gap\|+OR-range, and dealer-gamma-sign is not. Even the strongest exogenous flow candidate collapsed to a realized-vol proxy under the orthogonality partial."* Separately, `D5-NQ-intraday-momentum-scoping.md` / `Q-KBUDGET-1` closures record the gamma-sign construct **declined/UNSCREENABLE** (no admissible cohort). And this session's own MSL-S4 (an OI-by-strike construct) just closed `AMBIGUOUS-HOLD`/`PARKED` — negative-signed, FLIP-FAILs — direct, fresh empirical evidence against the optimistic read. | **No** — "estimable" turned out true but not load-bearing; the estimated signal collapses to a vol proxy, empirically, more than once. |
| "Swap 'retail stop-hunting' for 'mechanical margin-call/trailing-DD liquidation' — same WHO test, cleaner constraint." (crude form) | `SLR-MYM-1-liquidity-sweep-reclaim-scoping.md` explicitly ran this exact substitution and rejected it: *"Every mechanical rule in that population is account-equity-triggered: it determines whether a position closes, never where... Swapping 'retail with stops' for 'accounts under mechanical liquidation' changes the vocabulary and not the load-bearing content. That substitution IS the §5 laundering move."* | **No**, in this crude form. |
| "...but sign the direction using published SPAN parameter files + COT positioning, not vocabulary alone." (refined form, using two real public data sources) | Not tested in this specific combined form anywhere found. The standing repo objection (constraint determines *whether*, not *where*) still has to be answered by any refinement — COT is aggregate positioning, not a hard mandate naming a level or window. | **Open — genuinely untested, not yet refuted.** Worth a real look, with the WHERE-not-WHETHER bar as the falsifier to beat. |
| WM/Reuters FX fixing (an "off-venue constraint origin" example) | Already tested and killed: `event-window-reversal` family, F3 *"not a different fix"* re-proposal bar; `MULTI-FIX-FX` already bundled the NY-cut window. | **No** (this specific example) — but see §2 on the general point. |
| Buyback blackouts / compelled abstention as a mechanism class | Zero hits anywhere in the repo — genuinely never considered. | **Open — novel, unvetted.** Needs translation into a futures-expressible, sufficiently frequent proxy before it clears even the pre-G0 screens; not yet run through Req 1a. |
| Statistical power / underpowered acceptance region generating false kills | General methodological claim; not independently checkable from a grep sweep. No repo artifact found either confirming or refuting it directly. | **Open — plausible, unverified.** Would need per-class minimum-detectable-effect arithmetic to actually test. |
| Regime-pooling dilutes currently-live (post-2020) mechanisms | Same — plausible, general, not checked here. | **Open — plausible, unverified.** |
| Size screen should measure impact-persistence / "trade the wake," not raw flow size vs. account size | No repo artifact found articulating or rejecting this specific reframing of the size screen. | **Open — not previously considered as a methodology.** Distinct from any single mechanism; would change how the *screen itself* is written. |
| Bounded-duration compulsion (deadline-boxed events) as the payoff-shape sweet spot for the consistency/DD constraint | Consistent with, and a plausible explanation for, the 2026-08-22 consistency/payoff-shape finding (pyramided/skewed payoffs fail the 40%-per-day rule) — no repo artifact contradicts it, none previously articulated it as a *selection heuristic* for sourcing. | **Open — a genuinely new synthesis**, not previously stated in this form. |
| Rule-feasibility Monte-Carlo simulator (screen mechanisms by simulated P(pass) against the actual rulebook, not narrative objection alone) | The MSL charter's own step 8 already runs survivor MC, but only *after* Pine authorship and a TV backtest (step 6–7) — this suggestion is for a *pre-G0* simulated feasibility check, earlier in the pipeline than anything currently gates on. Not currently present at that stage. | **Open — a real process gap**, worth considering independent of any specific mechanism. |

## §2 — What actually survives, net

Every ox-alpha suggestion **concrete enough to name a specific already-considered mechanism**
(macro-print-on-index, index-roll, index-reconstitution, gamma-sign-from-OI, crude margin-call
substitution, WM/Reuters fix) turned out to already be tested and killed internally, several on
sharper grounds than the objection itself assumed. This is a real, useful confirmation that the
internal sweep's rigor holds up under a genuinely independent, well-informed adversarial pass —
not merely a sanitization artifact (per the model's own general capability, and per the parent
ADR's `§4` falsifier logic, this counts as a "zero-value" data point on the three concrete
examples, but not overall — see below).

What **does** survive, as live, unvetted, worth-pursuing threads:

1. **SPAN-file + COT-signed margin/liquidation cascades** — a refined version of an already-killed
   idea, using two real public data sources the crude version didn't have. Falls to the same
   WHERE-not-WHETHER bar unless the refinement actually clears it.
2. **Compelled-abstention mechanisms** (buyback blackouts and similar) — a genuinely novel class,
   never run through the WHO/WHEN/WHY/HOW + delete/flip screens.
3. **Impact-persistence / "trade the wake" reframing of the size screen** — a methodology change,
   not a mechanism, that could re-open cells the current flow-size-vs-account-size screen closes.
4. **Bounded-duration compulsion as a payoff-shape selection heuristic** — connects the 2026-08-22
   consistency-constraint finding to a *class-level* filter for future sourcing passes, rather than
   scoring each candidate's payoff shape only after it's built.
5. **A pre-G0 rule-feasibility Monte-Carlo simulator** — process suggestion, not a mechanism;
   would convert qualitative screen objections into a quantitative P(pass) ranking earlier in the
   pipeline than anything currently does.

**Since this Use produced objections that survive reconciliation, revert trigger (b) (three
consecutive zero-value uses) does not tick.**

---

## §3 — What this does NOT license

- Does not open a slate-4 card, scaffold a new camp, or name a WHO. E1's stop rule
  (`MSL-S7-closure-resolved-e1-hold.md`) is unchanged — a slate-4 card still needs a WHO that
  clears all four Req 1a clauses and an executed rejected-nearest sweep, neither of which this
  notice performs.
- Does not touch the WHO-track notice's own `RESOLVED (STILL DRY)` verdict — that stands.
- Carries zero authority over any admission decision, per the parent ADR §2/§5.
- The five surviving threads in §2 are candidate-objection-grade input, not pre-registered
  mechanisms — each would need its own WHO/WHEN/WHY/HOW clauses, dedup/door-check, and $0 screens
  before it's a card, exactly like any other MSL idea.

---

## §10 — Audit hooks (runnable)

```bash
grep -n "Event-day trend (FOMC/CPI/NFP/PCE)" docs/briefs/closures/MNQBASE-1-closure-intake-dry.md
grep -n "Russell annual reconstitution" lab/analysis/c1/wstruct_cost_geometry_2026-07-28/RESULTS.md
grep -n "collapsed to a realized-vol proxy" docs/rejected_candidates.md
grep -n "CANNOT BE WRITTEN" docs/briefs/rnd-pipeline/SLR-MYM-1-liquidity-sweep-reclaim-scoping.md
grep -rln "buyback\|10b-18\|blackout" docs/ ops/ lab/   # expect: empty (still novel)
```

## Verification

```bash
python scripts/check_brief.py docs/notes/notice/N-2026-08-23-ox-alpha-msl-who-sourcing-methodology-review.md --type notice
```
