# ADR 2026-08-15 — Algorithmic-analogue constructs are a "new modality" for the CON-5 pause

**Status:** `Accepted` — operator election 2026-08-15 (in-session, presented as a blocking route ruling with three options; "New modality — proceed" elected)
**Decision date:** 2026-08-15
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Tier:** light
**Layer:** methodology (research rules of evidence). **$0 / K=0.** No live-risk surface, no locked surface, no threshold moved.

## Decision

An **algorithmic-analogue construct** — a direction rule supplied by pattern-matching over price geometry (e.g. k-NN analogue forecasting) with **no named entry geometry** and no θ-parameterised trigger — is a **"new modality"** within the meaning of the [Q-TNEC-CON-5 closure](../briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md)'s pause condition, and therefore lifts that pause **for this construct class only**. Separately, a geometry-sourced direction rule is **outside** the [index raised bar](../rejected_candidates.md)'s mapped cost-ratio-lever set (price / instrument-selection / hold-time), so route ① admits it.

Scope: the modality class, not any individual candidate. The first candidate authorized under this ruling (`MNQ-ANALOGUE-1`) was **killed the same day** at its pre-G0 cheap falsifier (notice (`git show dea3af9:docs/notes/notice/N-2026-08-15-blind-channel-cost-geometry-and-first-candidate-kill.md` — private-class, not in the public seed)); this ruling survives that kill because it rules on the class.

## Grounds

The CON-5 closure paused the lane "pending a **new modality** or non-route-① thesis" — it pre-registered its own lift conditions rather than closing the lane. What was paused is legible from what ran: CON-1…CON-5 were θ-parameterised **entry-geometry** rules (ES−NQ divergence, compression→break, HTF-native break, PDH/PDL break, impulse→pullback→VWAP-reclaim), each dying on the same shape — gross eaten by RT with θ as the only surviving lever. An analogue forecaster shares none of that: it names no level, no session structure, and no trigger geometry; the algorithm supplies direction on every observation. Treating it as the same modality would make "modality" mean "uses OHLCV," which would render the closure's own lift condition unreachable — the [gate-reachability defect](../methodology/lessons/methodology_lessons.md) this estate has recorded 5 firings of.

On route ①: [ADR 2026-08-10](2026-08-10-temporal-selectivity-outside-mapped-levers.md) §2-A already ruled the mapped "instrument-selection" lever means **cross**-instrument choice. A direction rule sourced from return geometry is not price, not cross-instrument selection, and not a hold-time re-tune (its holding period is *forced* by the EM5 flat-by-16:00 envelope, not chosen).

## Reads

`docs/briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md` (pause text, 7 occurrences) · `docs/rejected_candidates.md:718-744` (bar scope + three routes) · `docs/adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md` §2-A · `docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md` + its K-cap addendum (`91b8344`) · `ops/instruments/NQ.md:49` (route ③ "no basis is privileged").

## Gate

RESOLVED on election. Re-test rides the channel ADR's own 2026-11-08 falsifier: if no algorithmic-analogue construct ever opens a manifest, this ruling was inert and should be recorded as such at that audit rather than carried as live doctrine.

## Boundary

Do **not** read this as un-pausing the dense-1m OHLCV temporal-selectivity lane generally — θ-parameterised entry-geometry constructs stay paused on their own terms. Do **not** use it to re-admit CON-1…CON-5 or a sibling under an "analogue" relabel; the test is the *absence* of named entry geometry, not the presence of the word. Do **not** cite route ③ (arithmetically false on both limbs: incumbent DSR 0.9644 vs the 0.950 floor; headline +0.890 vs the 0.850 floor).
