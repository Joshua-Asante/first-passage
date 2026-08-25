# Avenue A — microstructure / order-flow: scoping (staged cost dry-run, no pull)

**Type:** Inquire-phase scoping brief (zero-pull). **Authored:** 2026-07-24.
**Source:** advisor Avenue A (Stage 3 defer) — "microstructure only if Stages 0–2 disappoint AND you
commit to the Python live path; spend within the $125 Databento credit first (few-day MBP-10 pull)."
**Repo posture:** the raised-bar for the index-futures intraday-OHLCV domain names **order-flow /
microstructure as the sanctioned re-entry modality #2** ("untouched"). This brief *scopes* it; it does
**not** pull. **Verdict (this brief): scoped — not procured** (§6).

---

## §0 — Rule-0 reads

Read before scoping (concrete repo paths):

- [`docs/briefs/2026-07-14-a4-flow-data-fork-scoping.md`](2026-07-14-a4-flow-data-fork-scoping.md) —
  the adjacent prior. Its ruling is precise and must be represented precisely: Databento GLBX L3/tick
  is **"net imbalance only (can't split categories) → non-identifying"** and **"never procure for [the
  flow-categorization] fork."** That binds any question needing **participant-category attribution**;
  it does **not** by itself kill depth-shape/queue/impact features (which MBP-10 does resolve).
- [`docs/rejected_candidates.md`](../rejected_candidates.md) § "Single-instrument index-futures
  intraday OHLCV directional timing — RAISED BAR" — modality #2 (order-flow/microstructure,
  "untouched") is sanctioned re-entry; but the domain is at tail-exhaustion (STABLE/saturating).
- [`lab/analysis/orb/orb_mnq_2026-07/RESULTS_tv_export_realism.md`](../../lab/analysis/orb/orb_mnq_2026-07/RESULTS_tv_export_realism.md)
  — the survivor's fills are **already known-good**: median 81 ticks through the trigger, 0.7% land
  ≤1 tick, **zero** bars where the level never traded. Execution-microstructure has low marginal value.
- [`.claude/skills/databento-data/SKILL.md`](../../.claude/skills/databento-data/SKILL.md) — mandatory
  `metadata.get_cost` dry-run before any pull; **$125** free credit; MBP-10 is a high-granularity
  (expensive) schema — start coarse, escalate only after a cost estimate + explicit sign-off.

## §1 — Context and standing rules

Avenue A = buy order-book data (MBP-10 depth, or L3/MBO) to find or underwrite an edge OHLCV cannot
see. Two standing rules bracket it: **(a)** "don't buy explanatory data before a survivor justifies
it"; **(b)** the a4 prior (category-splitting is non-identifying from the tape). The one survivor in
this domain is **ORB-MNQ-1** (lifecycle CANDIDATE @1.00×, parked). This brief picks the fork honestly
and stages the cost dry-run so escalation — if ever justified — is one command away.

## §2 — Fork analysis (which use of MBP-10, if any)

| Fork | What it buys | Blocker | Verdict |
|---|---|---|---|
| **Execution-microstructure** | MBP-10 depth to model ORB-MNQ fills more finely | 07-21 realism audit already bounds fill risk at ~1 tick; fills are known-good | **Low marginal value** — the data answers a question already answered |
| **Discovery: flow-category** | split tape into participant categories to build a flow signal | a4 prior: L3/tick is net-imbalance-only → **non-identifying** for categories | **Killed by a4** — do not procure for this |
| **Discovery: depth-shape** | queue/depth-asymmetry/impact features OHLCV can't see | NOT killed by a4 (identifiable), but: tail-exhausted domain + "don't buy before a survivor justifies it" + blind-discovery multiplicity | **Only live sliver — but unjustified without a specific pre-registered feature** |

**Fork picked:** none currently justifies a pull. Execution-microstructure is near-valueless (audit);
flow-category discovery is a4-non-identifiable; depth-shape discovery is the only technically-live
sliver but is blind-discovery in a tail-exhausted domain with no survivor-tie. **Avenue A stays
scoped-not-procured.** The cost dry-run is staged so the $ anchor exists the moment a qualifying
feature appears — but staging ≠ authorizing.

## §4 — Falsifiable hypothesis

**H:** a few-day MBP-10 pull (within the $125 credit) can resolve a **pre-registered microstructure
question** that OHLCV **and** the existing 1-tick fill model cannot. **Falsifier:** if the candidate
question (i) reduces to participant-category flow (a4-non-identifiable), **or** (ii) is already
answered by the 07-21 fill-realism audit, **or** (iii) is blind depth-shape discovery with no tie to
the ORB-MNQ survivor, then the pull is **unjustified** and Avenue A stays scoped — H **falsified for
that question**. H is *supported* only by a specific depth-shape feature meeting all three escapes
(§6 qualifying triple). As of this brief, no such feature is on the table → **falsified as scoped.**

## §5 — Forbidden moves

- **Authorizing a pull.** This brief stages `metadata.get_cost` / `db_fetch estimate` only. No `pull`.
- **Spending any credit beyond the estimate.** `get_cost` is metadata (free); the DBN stream is not.
- **Misrepresenting the a4 prior** as killing *all* microstructure. It kills **category-splitting**;
  depth-shape is identifiable — the honest blocker there is domain-exhaustion + no-survivor-tie, not
  non-identifiability. (Conflating the two would launder a weaker rejection.)
- **Buying explanatory data before a survivor justifies it** — the standing rule; a blind depth-shape
  sweep violates it.
- **Committing the Python live path** off this brief (the advisor's precondition) — out of scope; the
  rail/arm chain is separately gated (B7).

## §6 — Gate (frozen: what would justify a pull)

A future MBP-10 pull is authorized **only** by a pre-registration naming a depth-shape feature that
clears the **qualifying triple** (all three, from §4's falsifier):

1. **Depth-shape, not category** — a book-geometry feature (queue imbalance dynamics, depth
   asymmetry, micro-impact) that MBP-10 *identifies* (escapes a4); AND
2. **Not fill-trivial** — answers something the 07-21 1-tick fill model does not (escapes execution
   triviality); AND
3. **Survivor-tied** — improves or monitors **ORB-MNQ-1** (or another admitted survivor), not blind
   discovery (escapes "don't buy before a survivor").

**Plus** the cost dry-run (§10) returns an estimate inside the $125 credit AND an operator sign-off.
Absent the qualifying triple, the verdict is **FALSIFIED (as scoped)** → **scoped — not procured**
(current state; §4 H unmet, no qualifying feature on the table). This is a *reachable* gate (the
estimate command is runnable today); it is deliberately hard to satisfy. A qualifying feature would
re-open toward RESOLVED, never AMBIGUOUS (the gate is binary on the triple).

### Addendum 2026-08-05 — condition 3 gains a second route (ADR [`2026-08-05-avenue-a-generate-confirm-route`](../adr/2026-08-05-avenue-a-generate-confirm-route.md), `Accepted`) — **WITHDRAWN 2026-08-24**

> ⚠ **Withdrawn 2026-08-24.** [`ADR 2026-08-05-avenue-a-generate-confirm-route`](../adr/2026-08-05-avenue-a-generate-confirm-route.md)
> is now `Superseded` in full by [`ADR 2026-08-24 — sourcing-phase channel retirement`](../adr/2026-08-24-sourcing-phase-channel-retirement.md).
> Per that ADR's own §7 pre-specified revert instruction ("If this ADR ever reverts to
> `Proposed`/`Withdrawn`, ... Avenue A §6's addendum block must be withdrawn in the same change"),
> this entire addendum block is withdrawn. §6's frozen original text is restored as the sole reading:
> condition 3 is **survivor-tied only** (Route A). This addendum's text below is left unedited
> (dated-decision integrity); this note is the reader intercept.

The frozen §6 text above is **unchanged and still binding**; this addendum **adds** an alternative
way to satisfy condition 3. Conditions 1–2 (depth-shape-not-category; not fill-trivial) bind under
both routes.

> **3 — Either (Route A) survivor-tied** — improves or monitors ORB-MNQ-1 (or another admitted
> survivor), **or (Route B) generate→confirm** under
> [`docs/methodology/avenue_a_generate_confirm.md`](../methodology/avenue_a_generate_confirm.md) —
> not an unguided screen that claims admission from the exploration window.

**Route A is unchanged and remains the default reading.** Route B is available *only* when that
checklist is frozen and followed: exploration on a frozen catalogue + frozen EXPLORATION window emits
**candidates only** (never edges, seeds, or watchlist gates); admission requires a separate
confirmatory PREREG committed **before any CONFIRM score**, on a pre-reserved CONFIRM window, with
`K_intrinsic` = the exploration catalogue size, a multiplicity-adjusted bar when the confirm budget
M > 1, and a single run.

⚠ **A blind screen that skips the confirm limb is still inadmissible.** The 2026-08-05 admissibility
ruling's shape requirement is *satisfied by* the confirm limb, not waived by it — and cost ($0
entitlement) still does not substitute for shape. If the deciding ADR reverts to `Proposed` /
`Withdrawn`, this addendum is withdrawn with it and §6's survivor-tie-only reading is restored.

## §7 — Forked questions

- **Q-MICRO-FEATURE (dormant):** does a specific depth-shape feature meeting the §6 triple exist for
  ORB-MNQ? Not opened here — opening it requires the feature, not the data.
- The advisor's **D1/D3 re-rank** (if Tradeify ever permits overnight holds) and **Tradovate-API
  Python-path** unlock are noted as *ranking-changers*, not scoped here.

## §10 — Audit hooks

```bash
# STAGED cost dry-run — do NOT execute in this plan; may be delegated (API key in Cursor Runtime
# Secrets). Confirm the module path resolves as DISC-CAMP-0 used it (databento_fetch.db_fetch).
PYTHONPATH=lab python -m databento_fetch.db_fetch estimate \
    --symbols NQ.FUT --stype parent --schema mbp-10 \
    --start 2026-07-20 --end 2026-07-23 --max-cost 5.00
# Record the returned $ estimate here before any pull is even proposed:  __________
# The two priors this scoping rests on:
rg -n "net imbalance only|never procure" docs/briefs/2026-07-14-a4-flow-data-fork-scoping.md
rg -n "frac ≤1 tick|zero.*entry bars where the panel says the level never traded" lab/analysis/orb/orb_mnq_2026-07/RESULTS_tv_export_realism.md
```

## Verification

§0 cites production paths + represents the a4 prior precisely (category-split, not all-microstructure)
✓ · §2 fork table with an honest "none justifies a pull" pick ✓ · §4 `H:` + three-limb falsifier,
adjudicated ✓ · §5 lists moves genuinely tempting (authorize pull; overstate a4; blind-buy) ✓ ·
§6 frozen qualifying triple + reachable gate ✓ · §10 stages get_cost (not executed) + prior-check
hooks ✓ · no pull authorized ✓.
