# Phase A — Derive the Target (audit + feasibility map + conditional doctrine ruling)

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development or
> superpowers:executing-plans. Checkbox (`- [ ]`) syntax for tracking.

**AUTHORIZATION:** `AWAITING GO`. A1+A2 were offered for GO in-session 2026-08-23; not yet given.
A3 is conditional and carries its own separate operator ruling regardless.
**Cost:** $0 · K=0 throughout. No locked surface, Pine, allocation, `dd_protection` constant, or
rail state is touched by any A task.
**Parent:** [`sequence overview`](2026-08-23-viable-strategy-sequence-overview.md)

**Goal:** convert "find a viable strategy" into "find a mechanism whose natural payoff shape lands
inside a published feasible region," and determine empirically whether the two screen amendments
(size re-aim, WHEN amendment) have any payoff before spending governance effort on them.

---

## Task A1 — Kill-register constraint-attribution audit

**What:** walk every strategy-grounds kill in the estate and tag it with (a) its actual kill
reason, classed; (b) whether the kill was demonstrated in that cell or inherited from a category
sibling; (c) whether an amended screen would re-open it.

- [ ] **Inputs (read, not re-derived):** `docs/rejected_candidates.md` (now complete — 30-row
  backfill landed 2026-08-23, debt 0); the WHO-track notice
  ([`N-2026-08-14-msl-who-track.md`](../../notes/notice/N-2026-08-14-msl-who-track.md)) §3 door
  tables; the forced-flow census (`N-2026-07-26-forced-flow-census.md`, pruned at the Great Prune; retrieve via `git show pre-prune-2026-08-08:docs/notes/notice/N-2026-07-26-forced-flow-census.md`; tag is private-archive-only on this public clone — [`docs/ltm/README.md`](../../ltm/README.md)) passes 1–4; the
  INTAKE-DRY entries on `ops/instruments/MCL.md`; `lab/CATALOG.md` closed rows;
  `docs/briefs/closures/` verdict lines (read each `**Verdict:**` line, not filenames — standing
  lesson).
- [ ] **Kill-reason classes (frozen before tagging):** `SIZE` (full-institutional-flow /
  capacity), `DIRECTION` (constraint does not entail sign — BE1/WHERE-not-WHETHER),
  `CADENCE` (frequency below activity/validation floor), `COST` (fails 4×RT arithmetic),
  `TRANSFER` (same mechanism, new ticker), `REGISTRY` (blocked by a prior family kill),
  `POWER` (statistically undetectable at our N), `VENUE` (instrument not legal/available),
  `SPREAD` (two-legged expression), `EVIDENCE` (cross-domain cohort transplant), `OTHER` (must
  be named, never a dumping ground).
- [ ] **Per-row tags:** kill class(es) · cell-demonstrated vs category-inherited ·
  would-revive-under: {impact-persistence size re-aim, threshold-parameterized WHEN, neither}.
- [ ] **Output:** `docs/notes/audits/2026-08-XX-kill-register-attribution-audit.md` — the matrix,
  plus the **revival list** (the only cells A3 may touch) and a count of category-inherited kills
  re-tested vs confirmed.
- [ ] **Fold-in:** the compelled-abstention arithmetic falsifier (Phase B, candidate B3) — a
  ~5-minute check executed here so a likely-dead idea never consumes an MSL card slot: blackout
  aggregate cadence (clustered, ~60–90 sessions/yr) vs the activity floor, and the implied
  per-session δ vs the power-wall precedent (F5/D3 rows: power 0.24–0.30 at single-digit bp).
  Record kill-or-survive in the audit note.

**Gate (A1):** `RESOLVED` when the matrix is complete over the registry + door tables and the
revival list is published (an **empty revival list is a valid, decisive outcome** — it kills A3
and the B-revive lane at $0). `FALSIFIED` (process) if any tag is assigned without reading the
underlying closure's own verdict line.

**Falsifiable H (A1):** ≥1 registry kill rests on a category-inherited `SIZE` or `DIRECTION`
ground that the amended screens would re-open. Reject if the revival list is empty — that outcome
retires threads 1/3 of the ox-alpha review at $0 and Phase B proceeds with candidates B1/B2 only.

**Forbidden moves (A1):** re-scoring any cell (this is attribution, not re-testing); editing any
closure or registry row; treating an `OTHER` tag as satisfied without a written reason;
"completing the matrix" with new instrument ledgers (ADR 2026-07-25 §5).

---

## Task A2 — Payoff-shape feasibility map (the target spec)

**What:** parameterize the existing survivor-MC machinery over payoff-shape tuples and publish the
region that clears every Tradeify gate simultaneously, so Phase B sources against a quantified
target instead of an open search.

- [ ] **Engine reuse (Rule 0 reads before any code):** `core/mc/simulation.py` (`simulate_path`,
  intraday-honest limb), `core/mc/preflight.py::firm_kwargs`, the 2026-08-22
  consistency-constraint quantification engine (memory:
  `project_tradeify_consistency_payoff_shape_constraint_2026_08_22`; locate its committed harness
  before writing anything new), `lab/discovery/prop_survivor_scoring.py::load_scoring_thresholds`
  (frozen seeds/sims/horizon — reused, never re-picked).
- [ ] **Parameter axes (synthetic trade-generating process, not a strategy):** win rate
  {40…70% by 5}, R-multiple distribution shape {symmetric, mild-right-skew, bounded-loss/
  clustered-win (the bounded-duration profile)}, trades/week {1, 2, 3, 5, 8}, per-trade risk
  {frozen from EM2's edge-indexed frontier — interpolate down, never up}. Axes are **coverage,
  not selection** — pre-registered as such.
- [ ] **Scored gates, jointly, per tuple:** trailing-DD bust ≤ 3.0% (intraday-honest limb — the
  synthetic process must generate within-day excursion, not close-only P&L); P(pass) ≥ 50%;
  consistency (no day > 40% of cumulative — including early-path breach, when cumulative is
  small); activity (≥1 trade/week satisfied structurally or via the operator token-trade,
  disclosed which); time-to-target distribution (disclosure).
- [ ] **Firms scored now:** `Tradeify_Select_100K` (deployment venue — model repaired: W1 +
  eval-lock fix) and `MFFU_Rapid_100K` (engine-faithful `trailing_locking`). **Bulenox/BluSky
  columns are BLOCKED** pending the parallel firm-repair plan — per the Q-FIRMEOD-1 closure bar,
  no Bulenox/BluSky bust figure may be produced for cross-firm comparison until that successor
  lands. The map ships with those columns explicitly marked BLOCKED, not silently absent.
- [ ] **Statistical discipline (Q-STATVALID-1, binding):** output is a **feasible region with
  SE-of-proportion bars at the frozen path count** — cells within 2σ of a gate line are marked
  `MARGINAL`, never `PASS`. **No best-cell is selected, reported, or ranked.** The region is a
  screen, not an optimizer.
- [ ] **Output:** `lab/analysis/c1/shape_feasibility_map_2026-08/` — harness + `RESULTS.md`
  (region table + the one-page reading: "what shape must a mechanism produce"), CATALOG row.
- [ ] **First consumers, run immediately:** (i) re-check the reopened Tradeify-native fade
  geometry ([`IMPLIED-SR-REPORT-ONLY` ADR](../../adr/2026-08-13-implied-sr-report-only-fade-reopen.md))
  against the region; (ii) pre-check the Phase-B candidates' predicted shapes (each names one in
  its card-precheck row).

**Gate (A2):** `RESOLVED` when the region is published with SE bars and both first-consumer
checks are recorded. `FALSIFIED` (design) if the region is empty at every tuple — that is a
material finding about the venue itself and routes to an operator review of the program, not to
quiet threshold-softening. `AMBIGUOUS-HOLD` if the consistency-engine harness cannot be located
and would need re-derivation (escalate before rebuilding — `lesson_unpriced_branch_search_the_corpus`).

**Forbidden moves (A2):** selecting/ranking cells; treating `MARGINAL` as `PASS`; quoting any
Bulenox/BluSky number; re-picking seeds/horizons; letting the synthetic process quietly become a
strategy pitch (it prices shapes, it does not name mechanisms).

---

## Task A3 — Conditional doctrine ruling (only if A1's revival list is non-empty)

**What:** an operator ruling on two screen amendments, pre-registered against A1's revival list
**before** any revived cell is re-scored.

- [ ] **Amendment 1 — size screen re-aim (impact-persistence):** replace "the flow must be a
  small residual" with the four-step battery: estimated compelled-flow size → measured post-event
  impact decay half-life → required participation ≪ displayed depth at event time → 4×-cost
  hurdle recomputed on **event-time** costs (spreads/slippage at 5–20× normal), not averages.
  Honest framing: a re-aim, not a relaxation — stricter on event-time entries, opens post-event
  wakes.
- [ ] **Amendment 2 — WHEN clause extension (threshold-parameterized triggers):** admit published
  structural trigger functions (margin-parameter files, exchange limit bands, strike/expiry
  registries) alongside pure calendar clocks — provided trigger parameters are public and the
  compelled response is contractual. WHO/WHY and delete/flip stay byte-untouched.
- [ ] **Vehicle:** amend-in-place addendum on the mechanism-boundaries ADR
  ([`2026-07-26`](../../adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md)) per the
  ceremony-tiering amend-in-place convention; the pre-registration freezes the exact revival list
  the amendments may touch, before re-scoring.
- [ ] **Degeneration guard (stated on the ruling card):** this is the `programme-audit`
  degeneration-signal pattern (screen change while dry) — the mitigations are the pre-registered
  revival list, the unchanged WHO/delete/flip core, and the falsifier below.

**Falsifier (A3, pre-registered with the ruling):** if, two quarters after adoption, zero revived
cells have produced even a G0 freeze, the amendments demonstrably manufactured work rather than
opening space — revert by superseding addendum.

**Gate (A3):** operator `Accepted` / `Declined` per amendment, independently. Declining either is
a clean outcome; Phase B's revive lane simply shrinks.

---

## Exit criteria (Phase A whole)

A1 matrix + revival list published · A2 region published with both first-consumer checks · A3
ruled or voided-by-empty-list. Board: SESSIONS entry per session; STATE decision-index one-liners;
no queue row unless work spans sessions.
