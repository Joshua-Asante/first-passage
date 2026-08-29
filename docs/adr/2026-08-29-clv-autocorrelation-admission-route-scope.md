# ADR 2026-08-29 — Bar closing-location-value (CLV) autocorrelation's admission-route scope under the 2026-07-21 directional-timing raised bar

**Status:** `Proposed` — drafted by Claude Code at Joshua's request; pending operator ratification, ratification date TBD. Do not treat as binding until Status flips to `Accepted`.
**Decision date:** 2026-08-29
**Authors:** Claude Code (Sonnet 5, drafter) — decision pending Joshua's ratification.
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

**Decision:** A bar-shape statistic — an unconditional, no-entry-rule, no-session-window serial-correlation finding — is not yet a "directional intraday timing candidate" in the raised bar's own scope sense, and therefore does not require an admission-route ruling merely to be recorded in a Notice-log. If and when CLV (or a similar bar-shape finding) is converted into an actual entry/exit construct, only **Route 3** (beat `ORB-MNQ-1` net-of-cost) is structurally available to it as currently measured; Routes 1 and 2 are foreclosed by the construct's own shape, not by a lack of ruling. A **$0 cost-law pre-screen must run before any Pre-Q is authored** for either instrument's CLV finding.

**2-A — Scope reading.** The raised bar's own text (`docs/rejected_candidates.md`) scopes itself to "a *directional intraday timing* edge... **deployable flat-by-close**" — language describing an entry/exit construct competing in the same design space as `ORB-MNQ-1`, not a bare statistical observation about price behavior. CLV as measured by both sessions is exactly the latter: a lag-1 correlation coefficient, with no direction rule, no position sizing, no stop, no exit. **The raised bar is not triggered by recording this statistic in a Notice-log.** Both HOLD notices' framing of the question as "genuinely unclear" is corrected here to: not unclear, *premature* — the gate fires at Pre-Q admission for an actual candidate, which does not yet exist.

**2-B — Route pre-analysis (so the question does not recur if someone tries to build the candidate).**
- **Route 1 (within-instrument temporal selectivity)** is not naturally available to *this* finding. Per MNQ's own MECHANISMS.md framing, CLV is "an unconditional shape-persistence statistic, no level or window involved" — it makes no claim restricted to any time-of-day or session window, which is exactly the shape Route 1 requires (a causally-named, G0-frozen, a-priori criterion for *which moment* to act, per the 2026-08-10 ADR §2-B). Bolting a temporal-selectivity criterion onto CLV after the fact to manufacture Route 1 eligibility would be exactly the "read off a scored list" laundering pattern that ADR's §2-B(1) forbids, and would in any case make it a **different candidate** — a genuinely time-conditioned CLV variant — not this one.
- **Route 2 (different modality / venue)** does not apply. CLV is computed from close/high/low alone — the exact "OHLCV structure alone" modality the raised bar targets, not order-flow, microstructure, or a different venue.
- **Route 3 (beat `ORB-MNQ-1` net-of-cost)** is the only route structurally open. The bar for this route is `ORB-MNQ-1`'s own realized edge — **+0.0626R per trade** (n=1,846) and **annSR +0.890 (Bulenox) / +0.835 (Tradeify)** — not merely clearing a generic cost floor.

**2-C — The cheap gate that must run before any Pre-Q.** Per both notices' own §3/§5 (this was not invented here — both sessions proposed it themselves) and the standing lesson `lesson_cost_law_pre_screen_mr_fade` ("cost-geometry pre-screen is mandatory before any edge build on a mean-reversion/fade construction... a 5-minute geometry calculation kills it before any harness is built"), convert rho into a decile-conditioned expected-value read (e.g., P(next-bar CLV in an extreme tercile | this-bar CLV in the opposite extreme decile) vs. base rate, or an implied gross edge in bp/event) and check it against **(a)** each instrument's own cost hurdle — MNQ's N6 (≈3.01 bp/session) and MYM's #M6 (≈6.57 bp/event, pending F3 re-pricing) — and **(b)** `ORB-MNQ-1`'s own net-of-cost edge from 2-B, since Route 3's bar is beating the incumbent, not merely clearing the floor. Given the effect's tiny magnitude (rho ≈ −0.03 to −0.037 — MNQ's own notice: "well under 0.1% of variance") and the negative/mean-reverting shape both notices independently flagged as adjacent to `mean-reversion-fade`, the standing lesson's own prior strongly favors a clean DROP — **but the pre-screen must actually run and be recorded; a predicted outcome is not a substitute for the $0 check.**

**2-D — What this does NOT open.** Does not admit CLV to a Pre-Q. Does not authorize any entry-rule authoring, backtest, or K spend. Does not rule on a *future*, differently-shaped CLV construct (e.g., one with a genuine, freshly-G0'd temporal-selectivity criterion) — that would be a new candidate under its own G0, not a re-reading of this one.

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

---

## §4 — Falsifier (revert trigger)

**H:** *the scope reading in 2-A correctly separates "recording a statistic" from "proposing a directional-timing candidate," and the route pre-analysis in 2-B correctly identifies Route 3 as the only one structurally open to CLV as currently measured.*

**Revert trigger:** any one of T1–T3 below firing falsifies this ADR's reading and triggers a supersede, per the edge rules in `docs/adr/2026-08-08-adr-ceremony-tiering.md`'s parent template.

| # | Trigger | Threshold | Action |
|---|---|---|---|
| T1 | The cost-law pre-screen (2-C) clears the relevant cost hurdle on either instrument at some decile conditioning | implied gross edge exceeds the instrument's own N6/#M6 hurdle | does **not** auto-admit to a Pre-Q — still needs to separately beat `ORB-MNQ-1` net-of-cost per Route 3; author a fresh ADR or light record with the actual numbers before any Pre-Q is opened |
| T2 | The pre-screen fails cleanly on both instruments | implied edge below both hurdles, consistent with the standing lesson's prior | both CLV notices close DROP citing this ADR + the pre-screen result; no Pre-Q authored |
| T3 | A future session invokes Route 1 for CLV without a fresh, causally-named, G0-frozen temporal criterion | any G0 or pre-registration cites this ADR's 2-A/2-B to claim Route 1 clearance for the *unconditional* finding as-is | void that opening; the 2026-08-10 ADR's own T1 (laundered re-tune) applies by the same logic |

**Revert action:** author a new ADR that fully or in-part supersedes this one, per the edge rules in `docs/adr/2026-08-08-adr-ceremony-tiering.md`'s parent template. Never silently edit this file's decision text.
**Trigger check schedule:** T1/T2 whenever the cost-law pre-screen is run (no calendar date — operator/D-S-A-triggered, matching both source notices' own §5); T3 at every future G0 that cites this ADR.

---

## §5 — Forbidden moves (under this ADR)

- **Treating "Route 1 doesn't fit the unconditional finding" as "Route 1 is closed to CLV forever."** A genuinely different, freshly-G0'd, time-conditioned CLV variant is a *different candidate* this ADR does not foreclose — see 2-D.
- **Skipping the cost-law pre-screen and jumping straight to a full backtest or entry-rule authoring.** The entire point of the raised bar's design (and the standing MR/fade lesson) is cheapest-falsification-first; 2-C is a $0 gate, not a formality to route around.
- **Treating a marginal pass of the generic cost hurdle (N6/#M6) as clearing Route 3.** Route 3's own text in the raised bar is explicit: "beats the incumbent ORB-MNQ net-of-cost, **not merely clears the cost floor**" — the bar is `ORB-MNQ-1`'s own +0.0626R / +0.890 annSR, not zero.
- **Reading this ADR as a GO for any Pre-Q, campaign, or K spend.** It rules on scope only; `Status: Proposed` until an operator ratifies it, and ratification itself is not a GO for anything beyond running the named $0 pre-screen.

---

## §6 — Consequences

**Positive consequences:**
- Closes a recurring open question (raised independently by both instrument sessions, and again in this session's own recap) with a citable ruling instead of leaving it to recur a fourth time.
- Gives both HOLD notices a concrete, falsifiable, $0 next action instead of an unresolved "needs a ruling" status.
- Establishes a reusable template for the next bar-shape (vs. entry-shape) Notice-phase finding on any instrument: name whether it's a candidate yet, and if not, pre-analyze which routes would/wouldn't apply if it becomes one.

**Negative consequences (real cost, not theatrical):**
- None identified — this is a documentation/scope ruling; it commits no spend and arms nothing.

**Risks (probabilistic, distinct from costs):**
- The route pre-analysis in 2-B could be wrong if a future re-reading of "temporal selectivity" or "modality" turns out broader than argued here — mitigated by T3's explicit revert path and by 2-B citing the exact language of the 2026-08-10 ADR it leans on rather than inventing new scope language.

**Downstream artifacts that need updating (this PR):**
- `docs/notes/notice/N-2026-08-29-mnq-clv-autocorrelation.md` — §4/§5 updated to cite this ADR and replace "not a call this session is positioned to make" with the ruling + named next step.
- `docs/notes/notice/N-2026-08-29-mym-closing-location-autocorrelation.md` — §4/§5 updated the same way.
- `ops/instruments/MECHANISMS.md` `bar-closing-location-autocorrelation` heading — both instruments' bullets gain a cross-reference to this ADR in place of "admission-route status... unresolved."

---

## §7 — Implementation plan

- **Phase 0** — §0 reads re-verified at authoring time (all anchors above pulled live this session via `git log`, not recalled).
- **Phase 1** — edit the three downstream artifacts listed in §6, same PR.
- **Phase 2** — grep-sweep for other stale restatements of "admission-route status is unresolved" tied to CLV: `grep -rn "admission.route" docs/notes/notice/N-2026-08-29-m*-clv* docs/notes/notice/N-2026-08-29-m*-closing-location* ops/instruments/MECHANISMS.md` (pasted in §10). Supersedes no predecessor (`Supersedes: none`), so no accept+retire checklist applies.
- **Phase 3** — verification block executes; Status stays `Proposed` until Joshua ratifies (this ADR does not flip its own status).

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
# Expected: exit 0; A2 edge-reverse-match skipped while Status is Proposed
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-29 | Initial authoring (Proposed, pending ratification) | Claude Code, at Joshua's request |
