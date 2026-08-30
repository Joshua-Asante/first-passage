# ADR 2026-08-29 — Bar closing-location-value (CLV) autocorrelation's admission-route scope under the 2026-07-21 directional-timing raised bar

**Status:** `Accepted` — ratified 2026-08-29, withdrawn same day after a post-ratification review surfaced a real error in 2-B's Route 1 analysis, corrected 2026-08-30 (PR #209), **re-ratified 2026-08-30** ("I'll go ahead and re-ratify the md file"). See Change history for the full sequence.
**Decision date:** 2026-08-29
**Authors:** Claude Code (Sonnet 5, drafter) + Joshua (ratification, withdrawal, and re-ratification).
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Related:** [2026-07-21 index-futures-intraday-OHLCV directional-timing raised bar](../rejected_candidates.md) (the bar being read) · [2026-08-10 sibling scope ruling](2026-08-10-temporal-selectivity-outside-mapped-levers.md) (same raised bar, different lever — precedent for structure, not content) · [MNQ CLV notice](../notes/notice/N-2026-08-29-mnq-clv-autocorrelation.md) · [MYM CLV notice](../notes/notice/N-2026-08-29-mym-closing-location-autocorrelation.md) · `ops/instruments/MECHANISMS.md` `bar-closing-location-autocorrelation` heading
**Layer:** research-doctrine reading. **$0 / K=0.** No `core/`, Pine, allocation, `dd_protection`, lifecycle, or rail change. Nothing armed; no candidate admitted.

---

## §0 — Rule 0 reads (production-source verification)

- `docs/rejected_candidates.md` §"Single-instrument index-futures intraday OHLCV directional timing — RAISED BAR" — anchor `0c305d7` (`git log -1 --date=short`, 2026-08-24). Read in full: scope line ("a *directional intraday timing* edge on a single liquid US equity-index future, from OHLCV structure alone, deployable flat-by-close"), all three re-proposal routes, and the 2026-08-10 scope-ruling blockquote already appended under route 1.
- `docs/adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md` — anchor `26c37f5` (2026-08-23). Read in full as the structural precedent for how a scope ruling on *this same raised bar* is authored, ratified (operator quote + Ratification block), and cross-referenced into `rejected_candidates.md`.
- `docs/notes/notice/N-2026-08-29-mnq-clv-autocorrelation.md` — anchor `6de26d5` (2026-08-29). Read in full, §1/§4/§5: rho=−0.0301 (n=141,540), block-shuffle null band [−0.0052, +0.0051], p_lower=0.0005; HOLD reason explicitly names the route question as unresolved and "not a call this session is positioned to make."
- `docs/notes/notice/N-2026-08-29-mym-closing-location-autocorrelation.md` — anchor `19d5ee0` (2026-08-29). Read in full, §1/§3/§4/§5: rho=−0.0370 (n_pairs=141,119), 95% CI [−0.0422, −0.0319], IAAFT p_two_sided=0.0050 (SIGNAL-EXCESS), and its own §5 already sketches the three-way reading this ADR resolves plus names the cost-law pre-screen as the cheap next step.
- `ops/instruments/MECHANISMS.md` `bar-closing-location-autocorrelation` heading (lines 286-336 at anchor `beaa98c`, 2026-08-29) — both instruments' class findings, and the `mean-reversion-fade` heading (line 453) checked for a pre-existing MNQ/MYM collision: none exists (its only class finding is USOIL, a different instrument, different mechanism shape — fading a price spike to a reference level, not a bar-shape serial-correlation claim).
- `ops/instruments/MNQ.md` N1/N6/N13 rows (anchor `0240ad9`, 2026-08-29) — `ORB-MNQ-1`'s own realized benchmark (annSR +0.890 Bulenox / +0.835 Tradeify; N13-corrected per-trade edge **+0.0626R**, n=1,846) and MNQ's own cost hurdle (N6: modern-era 4× hurdle ≈ **3.01 bp/session**).
- `ops/instruments/MYM.md` #M6 (anchor `beaa98c`, 2026-08-29) — MYM's own cost hurdle (4× Tradeify hurdle ≈ **6.57 bp/event**; pending re-pricing against the elected successor venue since Tradeify was de-scoped 2026-08-04).
- `docs/briefs/pre-registration/2026-08-22-mnq-tape-imbalance-prereg.md` §4 (anchor `3e351fc`, 2026-08-23) — the only tracked citation of `lesson_cost_law_pre_screen_mr_fade` (an agent-memory lesson, not a repo-tracked file): "Cost-geometry pre-screen is mandatory before any edge build on a mean-reversion/fade construction... the gross edge harvested per trade is characteristically a few bp — the same order of magnitude as round-trip cost, so a 5-minute geometry calculation kills it before any harness is built."
- `docs/briefs/rnd-pipeline/D5-RECOST-1-mnq-native-cost-law-rescope-scoping.md` (read in full this session, post-ratification-withdrawal correction) — re-read to establish precisely what the raised bar's "price" lever *is*: D5-RECOST re-derived the SAME Baltussen momentum construct's (`D5-NQ-intraday-momentum`) cost-hurdle-to-edge ratio at current (higher) MNQ notional instead of the original IS-era price level — a cost-geometry re-derivation of an *already-scored* signal, not a new signal search. Confirms "price" (and, by the same structure, "instrument-selection" via the cross-index-RV closure, and "hold-time" via `ORB-MNQ-1`'s own already-exploited exit-at-close) are three axes for re-deriving an *existing* construct's cost economics, not a taxonomy of possible signal mechanisms. `docs/rejected_candidates.md` line 996 (`es-nq-log-divergence-relative-contrarian` closure) independently confirms this reading in passing: "own-instrument momentum = C5/D5-RECOST-1, already dead" — D5-RECOST-1 is filed under the *momentum* mechanism family, not as a generic "price" mechanism category.

**Amendment-first search (sub-rule 10), executed output:**
```
$ grep -rln "closing-location\|CLV" docs/adr/
(no output — no existing ADR)
$ grep -n "closing-location-autocorrelation\|CLV" docs/rejected_candidates.md
(no output — raised bar has never been applied to this construct)
$ git log --oneline --all -- "*clv*" "*closing-location*"
46912cf merge: resolve origin/main conflicts (MNQ Phase-1 batch + instrument_profiles fixes)
19d5ee0 docs(instruments): MYM Phase-2 atheoretical bar-mechanism Notice batch
6de26d5 docs(notice): MNQ 5-candidate bars-only geometry Notice-phase screen
```
No existing owner. All three hits are the original Notice-phase authoring commits, not a prior ruling. New ADR is correct per amendment-first.

---

## §1 — Context

Both MNQ and MYM independently found a real, well-powered, sign-stable lag-1 serial autocorrelation in bar closing-location-value (CLV = where within its own high-low range a bar closed) during the 2026-08-29 atheoretical Notice-phase batch. Neither session self-adjudicated whether this finding, if pursued further, would need to clear the 2026-07-21 raised bar's admission routes — both explicitly and correctly declined, naming it "a call for whoever freezes a G0 on it" (MNQ) and "a scope ruling first, the same kind of ruling the 2026-08-10 ADR gave" (MYM). That ADR resolved a *different* routing question (whether "instrument-selection" means cross-instrument only) for the same raised bar; no equivalent ruling exists for a bar-shape statistic like CLV, and this exact ambiguity has now surfaced identically on two instruments and recurred across three separate governance mentions (both notices' §4/§5, and this session's own recap to the operator) without resolution.

**Decision driver (one sentence):** two HOLD notices are stuck on the same unanswered scope question, the question is answerable from documents already in the repo without spending K, and leaving it unanswered a third time just reproduces the same recurring ambiguity for the next session that finds a bar-shape statistic.

---

## §2 — Decision

**Decision:** A bar-shape statistic — an unconditional, no-entry-rule, no-session-window serial-correlation finding — is not yet a "directional intraday timing candidate" in the raised bar's own scope sense, and therefore does not require an admission-route ruling merely to be recorded in a Notice-log. If and when CLV (or a similar bar-shape finding) is converted into an actual entry/exit construct, **Route 1 is plausibly open to it** (its mechanism — bar-shape mean-reversion — is not a re-derivation of the raised bar's three specifically-mapped cost-geometry axes on an already-tried momentum construct) and **Route 3 remains separately available** if the effect proves economically real; **Route 2 does not apply** (same OHLCV modality). Route 1 eligibility is not a free pass — it still requires full G0 discipline (adversarial review, `K_intrinsic` charged, the F2 guard, and, if the construct is framed with any temporal-selectivity element, the 2026-08-10 ADR's own §2-B conditions). A **$0 cost-law pre-screen must run before any Pre-Q is authored** for either instrument's CLV finding, regardless of which route it would ultimately clear.

**2-A — Scope reading.** The raised bar's own text (`docs/rejected_candidates.md`) scopes itself to "a *directional intraday timing* edge... **deployable flat-by-close**" — language describing an entry/exit construct competing in the same design space as `ORB-MNQ-1`, not a bare statistical observation about price behavior. CLV as measured by both sessions is exactly the latter: a lag-1 correlation coefficient, with no direction rule, no position sizing, no stop, no exit. **The raised bar is not triggered by recording this statistic in a Notice-log.** Both HOLD notices' framing of the question as "genuinely unclear" is corrected here to: not unclear, *premature* — the gate fires at Pre-Q admission for an actual candidate, which does not yet exist.

**2-B — Route pre-analysis (so the question does not recur if someone tries to build the candidate). Corrected 2026-08-29 after ratification was withdrawn — the original version of this clause wrongly closed Route 1; see Change history.**

Route 1's actual text is "a mechanism **outside** the mapped cost-ratio-lever set (price / instrument-selection / hold-time)." The 2026-08-10 ADR opened that route for within-instrument temporal selectivity as **one worked example** of a mechanism outside the mapped set — it did not redefine Route 1 to mean *only* temporal selectivity, and the original draft of this ADR incorrectly tested CLV against that one example instead of against the actual mapped-lever definition. Re-reading the raised bar's own "Basis" line and each named lever's provenance (§0 reads, this session):

- **"price"** = `D5-RECOST-1`'s specific move: re-deriving the *same* Baltussen momentum construct's cost-hurdle-to-edge ratio at a different (current) price/notional era — a cost-geometry re-derivation of an already-scored signal.
- **"instrument-selection"** = the cross-index-RV-ranking closure's move: choosing which *instrument* to trade the *same* ORB construct on.
- **"hold-time"** = `ORB-MNQ-1`'s own already-exploited choice of exit-at-close (further re-falsified 2026-08-10 by the stop-width sweep).

All three are axes for re-deriving an **existing, already-tried momentum/breakout construct's** cost economics — none of them is a taxonomy of possible *signal mechanisms*, and none of them has anything to do with whether a construct is time-of-day-conditional. CLV's own mechanism — bar-shape mean-reversion via closing-location-value serial correlation — is not a re-pricing of D5's momentum construct, not an instrument-selection scheme, and not a hold-time retune; it is a freshly-mined, structurally different signal. On that reading, **Route 1 is plausibly open to CLV**, independent of and in addition to Route 3 — not because CLV happens to also be temporal-selectivity-shaped (it isn't), but because its mechanism is outside the three specifically-mapped re-derivation axes on their own terms.

This is a scope reading, not a clearance: an actual Route-1 opening still requires the same G0 discipline every route does (adversarial review, `K_intrinsic` charged per the futures-anomaly-discovery skill, the F2 guard unchanged), and if the eventual construct frames itself with *any* temporal-selectivity element on top of the base CLV signal, the 2026-08-10 ADR's own §2-B conditions (a-priori-named criterion, frozen at G0, never read off a scored list) bind on that element specifically.

- **Route 1 (mechanism outside the mapped cost-ratio-lever set)** — plausibly open, per the reasoning above. Not yet exercised; needs its own G0 if a Pre-Q is authored.
- **Route 2 (different modality / venue)** does not apply. CLV is computed from close/high/low alone — the exact "OHLCV structure alone" modality the raised bar targets, not order-flow, microstructure, or a different venue.
- **Route 3 (beat `ORB-MNQ-1` net-of-cost)** remains separately available if the effect proves economically real. The bar for this route is `ORB-MNQ-1`'s own realized edge — **+0.0626R per trade** (n=1,846) and **annSR +0.890 (Bulenox) / +0.835 (Tradeify)** — not merely clearing a generic cost floor. See 2-C for why this comparison cannot be fully executed yet (CLV has no defined entry/exit, hence no R of its own).

**2-C — The cheap gate that must run before any Pre-Q. Corrected 2026-08-29: the pre-screen is a necessary-condition cost-floor check only; it cannot execute the full Route 3 comparison, and the MYM leg is provisional.**

Per both notices' own §3/§5 (this was not invented here — both sessions proposed it themselves) and the standing lesson `lesson_cost_law_pre_screen_mr_fade` ("cost-geometry pre-screen is mandatory before any edge build on a mean-reversion/fade construction... a 5-minute geometry calculation kills it before any harness is built"), convert rho into a decile-conditioned expected-value read (e.g., P(next-bar CLV in an extreme tercile | this-bar CLV in the opposite extreme decile) vs. base rate) and express it as an implied gross edge in bp/event. Check that figure against each instrument's own cost hurdle:

- **MNQ:** N6, ≈3.01 bp/session — a live, current basis.
- **MYM:** #M6, ≈6.57 bp/event — **provisional only.** `MYM.md` #M6 itself discloses Tradeify is no longer the program's binding venue (de-scoped 2026-08-04) and this hurdle is pending re-pricing against whatever successor venue F3 eventually rules. A pass or fail against this specific number must be read as "against the last-known basis," not as a final MYM verdict — do not treat a marginal result here as dispositive; re-run against the F3-ruled hurdle once one exists.

**This bp/event check is a necessary-condition floor only — it is not the full Route 3 comparison.** Route 3's actual bar (2-B) is `ORB-MNQ-1`'s own **+0.0626R per trade**, an R-figure computed from a defined entry, stop, and exit. CLV as currently measured has none of those — there is no trade construction to normalize into R, so a bp/event implied-edge figure and an R-per-trade figure are not the same unit and cannot be directly compared. **The full Route 3 comparison against `ORB-MNQ-1`'s net-of-cost edge is deferred until an actual entry/exit construct exists for CLV** (at which point that construct's own R, computed the same way ORB-MNQ-1's is, becomes comparable). Clearing the cost-floor check above is therefore necessary but not sufficient for either Route 1 or Route 3 admission — it only tells a future session whether the raw statistic is economically worth converting into a trade construction at all.

Given the effect's tiny magnitude (rho ≈ −0.03 to −0.037 — MNQ's own notice: "well under 0.1% of variance") and the negative/mean-reverting shape both notices independently flagged as adjacent to `mean-reversion-fade`, the standing lesson's own prior strongly favors a clean DROP at the cost-floor check alone — **but the pre-screen must actually run and be recorded; a predicted outcome is not a substitute for the $0 check.**

**2-D — What this does NOT open.** Does not admit CLV to a Pre-Q. Does not authorize any entry-rule authoring, backtest, or K spend. Route 1 being plausibly open (2-B) is a scope reading, not a clearance — it does not waive G0 discipline, adversarial review, `K_intrinsic`, or the F2 guard, and does not pre-judge whether a specific future CLV-based construct actually survives that discipline. Does not rule on a *future*, differently-shaped CLV construct (e.g., one with a genuine, freshly-G0'd temporal-selectivity criterion layered on top) — that would be a new candidate under its own G0, not a re-reading of this one.

**Effective:** upon acceptance.
**Scope:** the two 2026-08-29 CLV Notice-log entries (MNQ, MYM) specifically; the reasoning in 2-A/2-B generalizes to any future bar-shape (as opposed to entry-shaped) Notice-phase statistical finding on any instrument, but this ADR rules only on CLV — a future finding needing the same reasoning cites this ADR rather than re-deriving it, and gets its own route pre-analysis if its shape differs.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Rule CLV in-scope now and force an immediate route pick | Would manufacture a false choice among three routes none of which naturally fits an unconverted statistic — the actual answer is "not yet a candidate," and picking a route prematurely would misdescribe what was measured. |
| Rule the raised bar categorically exempts all bar-shape statistics forever | Too broad — a future bar-shape finding that *is* effectively a disguised directional-timing claim (e.g., one that already implies a specific entry rule) should not get a blanket exemption just by being labeled "a statistic." §2 scopes the exemption to *this* finding's actual shape (unconditional, no entry rule), not to a category name. |
| DROP both CLV notices outright now, without running the pre-screen | Discards the strongest statistical result in the MYM batch (SIGNAL-EXCESS, p=0.005) without the $0 check that could settle it either way; both notices' own §4 already rejected this as "discarding a real, well-powered, directionally stable effect for no principled reason." |
| Leave both notices HOLD indefinitely on the same open question | The status quo this ADR is written to resolve — it has already recurred three times (both notices' own text, plus this session's recap to the operator) without a decision closing it. |
| Read the 2026-08-10 ADR's temporal-selectivity worked example as the full definition of Route 1, and test CLV only against that one example | This was this ADR's own original (pre-correction) mistake in 2-B, caught by Codex's review of the pre-ratification-withdrawal commit and independently re-verified against `D5-RECOST-1`'s scoping doc (§0). The 2026-08-10 ADR opens Route 1 for temporal selectivity as **one worked example** of a mechanism outside the mapped set, not an exhaustive redefinition of Route 1 itself; testing CLV only against that example wrongly closed a route that the actual mapped-lever definition (price / instrument-selection / hold-time, each a cost-re-derivation axis on an already-tried momentum construct) leaves open. Corrected in 2-B; recorded here because this table's own function includes naming considered-and-rejected readings, including one this ADR briefly held itself — see Change history. |

---

## §4 — Falsifier (revert trigger)

**H (corrected 2026-08-29 after ratification was withdrawn — see Change history):** *the scope reading in 2-A correctly separates "recording a statistic" from "proposing a directional-timing candidate" (so the raised bar's gate does not fire on a bar-shape statistic with no entry rule), and the route pre-analysis in 2-B correctly identifies Route 1 as plausibly open (CLV's mechanism sits outside the three specifically-mapped cost-re-derivation axes, not merely outside the 2026-08-10 ADR's one temporal-selectivity example) and Route 3 as separately available, with Route 2 inapplicable.*

**Revert trigger:** any one of T1–T3 below firing falsifies this ADR's scope/route reading and triggers a supersede, per the edge rules in `docs/adr/2026-08-08-adr-ceremony-tiering.md`'s parent template. These test the ADR's own claim about scope and routes — **not** whether CLV itself turns out to be economically tradeable, which is a separate disposition question (below) that does not bear on whether this ADR's reasoning is correct.

| # | Trigger | Threshold | Action |
|---|---|---|---|
| T1 | A future adversarial review or G0 determines CLV's mechanism is, in fact, a re-derivation of one of the three mapped axes (price / instrument-selection / hold-time) rather than outside them | a write-up substantiates this with reasoning as concrete as §0's `D5-RECOST-1` read | 2-B's Route 1 opening is wrong; supersede, close Route 1 for this finding, fall back to Route 3 only |
| T2 | A future ruling determines the raised bar's gate DOES fire on a bare statistic with no entry rule (2-A's scope reading is wrong) | a citable re-reading of the raised bar's own text, or an operator ruling, contradicts 2-A | supersede; both CLV notices need a route ruling immediately, not merely before Pre-Q |
| T3 | A future session invokes Route 1 for CLV (or cites this ADR to invoke it for a different bar-shape finding) without doing its own G0 work | any G0 or pre-registration cites 2-B to claim Route 1 clearance without a fresh, causally-named, G0-frozen criterion of its own | void that opening; the 2026-08-10 ADR's own T1 (laundered re-tune) applies by the same logic |

**Revert action:** author a new ADR that fully or in-part supersedes this one, per the edge rules in `docs/adr/2026-08-08-adr-ceremony-tiering.md`'s parent template. Never silently edit this file's decision text — the one exception already exercised is the operator's own explicit withdrawal-and-correction of their own ratification (see Change history); that is not a precedent for anyone else, including a future Claude Code session acting alone, to silently edit this file.
**Trigger check schedule:** T1/T2/T3 at every future G0 or adversarial review that touches this ADR's reasoning; no calendar date.

**Disposition (separate from falsification) — the $0 cost-law pre-screen named in 2-C.** Clearing or failing the pre-screen does not falsify or confirm the H above; it only determines whether either CLV finding is worth converting into an entry/exit construct at all.

| # | Outcome | Threshold | Disposition |
|---|---|---|---|
| D1 | Pre-screen clears the relevant cost hurdle on either instrument at some decile conditioning | implied gross edge exceeds the instrument's own N6/#M6 hurdle | does **not** auto-admit to a Pre-Q — still needs to separately beat `ORB-MNQ-1` net-of-cost per Route 3 (2-C); author a fresh ADR or light record with the actual numbers before any Pre-Q is opened |
| D2 | Pre-screen fails cleanly on both instruments | implied edge below both hurdles, consistent with the standing lesson's prior | both CLV notices close DROP citing this ADR + the pre-screen result; no Pre-Q authored |

**Disposition check schedule:** whenever the cost-law pre-screen is run (no calendar date — operator/D-S-A-triggered, matching both source notices' own §5).

---

## §5 — Forbidden moves (under this ADR)

- **Treating "Route 1 doesn't fit the unconditional finding" as "Route 1 is closed to CLV forever."** A genuinely different, freshly-G0'd, time-conditioned CLV variant is a *different candidate* this ADR does not foreclose — see 2-D.
- **Skipping the cost-law pre-screen and jumping straight to a full backtest or entry-rule authoring.** The entire point of the raised bar's design (and the standing MR/fade lesson) is cheapest-falsification-first; 2-C is a $0 gate, not a formality to route around.
- **Treating a marginal pass of the generic cost hurdle (N6/#M6) as clearing Route 3.** Route 3's own text in the raised bar is explicit: "beats the incumbent ORB-MNQ net-of-cost, **not merely clears the cost floor**" — the bar is `ORB-MNQ-1`'s own +0.0626R / +0.890 annSR, not zero.
- **Reading this ADR as a GO for any Pre-Q, campaign, or K spend.** It rules on scope only; ratification itself is not a GO for anything beyond running the named $0 pre-screen.
- **Re-narrowing Route 1 to "only what the 2026-08-10 ADR's worked example covered."** That was this ADR's own original mistake (§3, Change history): Route 1's text is the mapped-lever definition itself (price / instrument-selection / hold-time), not any one instantiation of an opening within it. Testing a future finding only against the temporal-selectivity example repeats the same error this ADR was corrected for.
- **Treating the pre-screen's D1/D2 disposition outcome (§4) as evidence for or against this ADR's T1/T2/T3 falsifiers.** They test different claims — economic viability of CLV vs. correctness of the scope/route reading — and conflating them was part of the original error.

---

## §6 — Consequences

**Positive consequences:**
- Closes a recurring open question (raised independently by both instrument sessions, and again in this session's own recap) with a citable ruling instead of leaving it to recur a fourth time.
- Gives both HOLD notices a concrete, falsifiable, $0 next action instead of an unresolved "needs a ruling" status.
- Establishes a reusable template for the next bar-shape (vs. entry-shape) Notice-phase finding on any instrument: name whether it's a candidate yet, and if not, pre-analyze which routes would/wouldn't apply if it becomes one.

**Negative consequences (real cost, not theatrical):**
- None identified — this is a documentation/scope ruling; it commits no spend and arms nothing.

**Risks (probabilistic, distinct from costs):**
- The route pre-analysis in 2-B could be wrong if a future re-reading of "temporal selectivity," "modality," or the mapped-lever provenance turns out different than argued here — mitigated by T1/T2's explicit revert path and by 2-B citing the exact `D5-RECOST-1` scoping doc it leans on rather than asserting the reading without a source. (This risk already materialized once, in this ADR's own first draft — see Change history — which is direct evidence the risk is real, not merely theoretical.)

**Downstream artifacts that need updating (this PR):**
- `docs/notes/notice/N-2026-08-29-mnq-clv-autocorrelation.md` — §4/§5 updated to cite this ADR and replace "not a call this session is positioned to make" with the ruling + named next step; updated again to match the corrected 2-B (Route 1 plausibly open, not merely Route 3).
- `docs/notes/notice/N-2026-08-29-mym-closing-location-autocorrelation.md` — §4/§5 updated the same way, plus the #M6 provisionality caveat from 2-C.
- `ops/instruments/MECHANISMS.md` `bar-closing-location-autocorrelation` heading — both instruments' bullets gain a cross-reference to this ADR in place of "admission-route status... unresolved."
- `ops/instruments/MYM.md` (durable-findings row, ~line 139) — still reads "admission-route status under the directional-timing raised bar is unresolved; not GRADUATEd on this session's own authority"; update to cite this ADR's ruling instead of restating the question as open.
- `ops/instruments/MNQ.md` (session-log entry, ~lines 202-205) — `closing-location-autocorrelation` row still reads "this candidate's raised-bar admission-route is explicitly unresolved. **HOLD** pending a route ruling"; same update.

---

## §7 — Implementation plan

- **Phase 0** — §0 reads re-verified at authoring time (all anchors above pulled live this session via `git log`, not recalled).
- **Phase 1** — edit the downstream artifacts listed in §6, same PR.
- **Phase 2** — grep-sweep for other stale restatements of "admission-route status is unresolved" tied to CLV: `grep -rn "admission.route\|admission-route" docs/notes/notice/N-2026-08-29-m*-clv* docs/notes/notice/N-2026-08-29-m*-closing-location* ops/instruments/MECHANISMS.md ops/instruments/MYM.md ops/instruments/MNQ.md` (pasted in §10). Supersedes no predecessor (`Supersedes: none`), so no accept+retire checklist applies.
- **Phase 3** — verification block executed; Status flipped to `Accepted` 2026-08-29 per Joshua's ratification.
- **Phase 4** (2026-08-29, same day) — ratification withdrawn by Joshua after a post-ratification review (Codex, PR #209) correctly identified that Phase 3's 2-B wrongly closed Route 1 by testing CLV only against the 2026-08-10 ADR's one worked example instead of the mapped-lever definition itself. Corrected in place per Joshua's explicit instruction ("Update the original ADR I ratified," not a superseding ADR): 2-B/2-C/2-D rewritten, §3/§4/§5/§6/§10 updated to match, `ops/instruments/MYM.md`/`MNQ.md` ledger entries fixed, Status reverted `Accepted` → `Proposed` pending re-ratification. See Change history.

---

## §10 — Audit hooks (runnable)

```bash
# Confirm every cited figure still matches its source (re-run before treating this ADR as current)
grep -n "rho\|Spearman" docs/notes/notice/N-2026-08-29-mnq-clv-autocorrelation.md | head -3
# Expected: -0.0301

grep -n "obs = " docs/notes/notice/N-2026-08-29-mym-closing-location-autocorrelation.md
# Expected: -0.0370

grep -n "N13\|+0.0626R" ops/instruments/MNQ.md
# Expected: ORB-MNQ-1's realized per-trade edge +0.0626R, n=1,846

grep -n "M6.*Cost hurdle\|6.57 bp" ops/instruments/MYM.md
# Expected: 4x Tradeify hurdle ~6.57 bp/event

grep -n "N6.*Cost hurdle\|3.01 bp" ops/instruments/MNQ.md
# Expected: modern MNQ 4x hurdle ~3.01 bp/session

# Phase-2 sweep (paste real output, not a recalled conclusion)
grep -rn "admission.route" docs/notes/notice/N-2026-08-29-mnq-clv-autocorrelation.md docs/notes/notice/N-2026-08-29-mym-closing-location-autocorrelation.md ops/instruments/MECHANISMS.md
# Expected after this PR: only cross-references to this ADR, no remaining "unresolved" language

grep -n "admission-route\|raised-bar" ops/instruments/MYM.md ops/instruments/MNQ.md
# Expected after this PR: no remaining "unresolved"/"pending a route ruling" language on the CLV rows —
# only a cross-reference to this ADR

# Confirm this ADR's own corrected Route 1 reading is internally consistent (no leftover "only Route 3" language)
grep -n "only.*route\|only one.*open\|structurally open" docs/adr/2026-08-29-clv-autocorrelation-admission-route-scope.md
# Expected: Route 3 described as "remains separately available" / "separately open," never as the sole route

# Amendment-first: still no other ADR owns this question
grep -rln "closing-location\|CLV" docs/adr/ | grep -v "2026-08-29-clv-autocorrelation-admission-route-scope.md"
# Expected: empty
```

---

## Verification

```bash
$ python scripts/check_brief.py docs/adr/2026-08-29-clv-autocorrelation-admission-route-scope.md --type adr
# Expected: RESULT: well-formed

$ python .claude/skills/brief-authoring/scripts/check_brief.py docs/adr/2026-08-29-clv-autocorrelation-admission-route-scope.md --type adr
# Expected: RESULT: well-formed

$ python scripts/check_adr_graph.py
# Expected: exit 0
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-29 | Initial authoring (Proposed, pending ratification) | Claude Code, at Joshua's request |
| 2026-08-29 | Ratified — Status `Proposed` → `Accepted`, no amendments to §2 | Joshua ("Flip it to accepted") |
| 2026-08-29 | Ratification withdrawn; 2-B corrected — original text tested CLV only against the 2026-08-10 ADR's one temporal-selectivity worked example and wrongly concluded Route 1 was closed. Corrected reading: Route 1 is plausibly open on its own terms (mechanism outside the mapped price/instrument-selection/hold-time re-derivation axes), independent of Route 3. Correction verified against `D5-RECOST-1`'s scoping doc and `rejected_candidates.md` line 996 (§0). 2-C, 2-D, §3, §4, §5, §6, §7, §10 updated to match; Status reverted `Accepted` → `Proposed` pending re-ratification. | Joshua (withdrawal: "I take back my ratification. Update the original ADR I ratified.") + Claude Code (correction, crediting Codex's PR #209 review for the initial catch) |
| 2026-08-30 | Re-ratified — Status `Proposed` → `Accepted`, the corrected §2 (2-A/2-B/2-C/2-D) as landed in PR #209, no further amendments made at ratification time. | Joshua ("I'll go ahead and re-ratify the md file") |
