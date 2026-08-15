# Q-GEOFIT-1 — What daily-P&L return profiles does corrected trailing-DD eval geometry fund at the frozen floor?

**Status:** `CLOSED — AMBIGUOUS-PARAMETERIZATION` 2026-07-25 (signed and closed same day).
Closure: [`closures/Q-GEOFIT-1-closure-ambiguous-parameterization.md`](closures/Q-GEOFIT-1-closure-ambiguous-parameterization.md) ·
RESULTS: [`lab/archive/q_geofit_1_2026-07/RESULTS.md`](../../lab/archive/q_geofit_1_2026-07/RESULTS.md).
**A1 engine reproduction PASSED both arms** (4.74% / 0.11%, Δ 0.003pp); **A2 profile
sufficiency MISSED by 23.63pp at an exact parameter match** — the `(σ_d, μ/σ, shape, z)`
family omits **skew**, which is the load-bearing property for surviving a fixed-$ trailing
barrier. §6 therefore admits **no envelope claim**; the 288-cell grid was left **unrun**
(operator election — it could not produce the deliverable it exists for). H-GEOFIT is
neither accepted nor rejected. Grid, floor, practicality ceiling, and anchors remain frozen
as signed; every repair listed in the closure §8 belongs to a fresh pre-registration citing
this one (§5).
**What this is:** a Pre-Q for a **geometry funding-envelope map** — a one-time sweep of
synthetic daily-P&L profiles through the corrected `trailing_locking` engine at the frozen
survivor floor, producing the acceptance region ("what the geometry funds") as a reusable
lookup surface. It is **gate calibration, not candidate discovery**: no return data is
consulted, no candidate is selected, no K is burned.
**Loop of record:** STRATEGIC (INQHIORI).
**Feeds:** (a) a Phase-0 geometry pre-screen for every future prop-portfolio candidate
(lookup cost ≈ 0); (b) the archetype spec for harvest sourcing under
[`docs/methodology/strategy_harvest.md`](../methodology/strategy_harvest.md); (c) the
2026-11-08 §4 review — an **empty** envelope at practical parameters is itself a
program-level finding.
**Authored:** 2026-07-24 · Claude Code (Fable 5), operator-directed ("draft a discovery
brief targeting what trailing-DD geometry funds").

D-S-A domain: data (corpus = the geometry parameters + a pre-declared synthetic profile
grid; no system or framework change).

Pre-Q gate:
  D: candidate-performance corpora (CATALOG studies, panels, harvest seeds) deleted from
     this question's I/N corpus — test: outside the scope of the question class (the
     question is about the *gate*, not any candidate; consuming candidate returns here
     would contaminate §7's zero-K claim).
  S: geometry compressed to the four constants that bind at a tier (trail $, target $,
     consistency %, min trading days) + a 4-tuple profile family (§2) — preserves the
     anomaly Noticed (candidates keep dying at a wall whose shape is unmapped).
  A: the envelope surface IS the accelerator — it converts every future "could the
     geometry fund X?" from a 10K-sim run into a table lookup.

---

## §0 — Rule-0 reads (production source, verified this session 2026-07-24, HEAD `ca6fb03`)

Per-file anchors (`git log -1 --format='%h %ci'`), all content-read this session.
Primary read: [`core/mc/simulation.py`](../../core/mc/simulation.py):

- **`core/mc/simulation.py` @ `f8f8db1`** — the mechanics this map sweeps, read verbatim
  (L96–166): `trailing_locking` bust = EOD check `equity_new ≤ floor` where
  `floor = min(peak − max_dd_usd, starting_equity + dd_lock_offset_usd)` (L123–135);
  **corrected geometry** (lock unreachable) reduces this to a pure fixed-$ EOD trail off
  peak equity. Pass = `equity ≥ profit_target AND trade_days ≥ min_trading_days` plus the
  consistency clause (ratio-based, max-day/total — L159–166). Idle days count via
  `had_activity`; inactivity is disabled in the scoring configuration (inherited).
- **[`core/firm_rules.py`](../../core/firm_rules.py) @ `fd95c72`** — the primary tier's
  binding constants (L296–309): `Tradeify_Select_100K` = $3,000 trail (3.0% of 100K) /
  $6,000 target (6.0%) / consistency 40% / `min_trading_days` 3. Secondary check row
  `MFFU_Rapid_100K` (L375–389): $3,000 / $6,000 / 50% / 2.
- **[`lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_regime_gate.py`](../../lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_regime_gate.py) @ `163b0b5`** —
  `run_partition_mc` (L87–110) consumes an arbitrary daily-P&L array + `firm_key` + frozen
  thresholds (Run-2, consistency-on). **The envelope runner calls this frozen primitive on
  synthetic dailies — no re-implementation of the engine.**
- **[`docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md`](pre-registration/2026-07-13-prop-survivor-scoring-prereg.md) @ `be6dda6`** —
  frozen floor **bust ≤ 3.0% + P(pass) ≥ 50%**, 10K sims × seeds 42/123/2026, horizon
  1500. The envelope is scored against this floor and no other.
- **[`docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md`](../adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md) @ `59c2282`** —
  corrected-geometry state of record: zero Part A clearers on the frozen $100K set
  (Tradeify 4.74% / MFFU 4.25% / Bulenox 3.51% / BluSky 4.44%); the correction idiom
  (`dd_lock_offset_usd → 1_000_000.0`, never `None`).
- **[`docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md`](../adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md) @ `13ad9a1`** —
  Addendum 2026-07-24: Striker→MYM/MNQ reconstruction is **TERMINAL** (MYM ORC CLOSED,
  ORB-MNQ PARKED); reconstruction re-open needs a fresh operator GO + pre-registration.
  **This brief's §5 hard-guards against becoming a side-door re-open.**
- **[`docs/methodology/strategy_harvest.md`](../methodology/strategy_harvest.md) @ `268851b`** —
  the intake this brief's RESOLVED branch feeds: four admission requirements, K_intrinsic
  ≤ 3 confirm-don't-mine, frozen screen constants. The envelope adds a *fifth, free*
  pre-admission check (profile-in-envelope); it does not modify the intake.

---

## §1 — Context (symptom, not fix)

The prop-portfolio program has measured, one candidate at a time, that the corrected
trailing-DD eval geometry rejects everything put in front of it: the c1 book fails Part A
on all four frozen $100K tiers (4.74%/4.25%/3.51%/4.44% vs a 3.0% ceiling), and the
discovery/harvest wave produced no fundable survivor. The standing lesson
(`lesson_prop_archetype_drawdown_survival`) says the DD mechanism picks the archetype —
prop evals fund **survival**, not edge. But the program has never inverted the question:
**the acceptance region of the funding geometry itself has never been mapped.** Every
candidate to date paid full scoring cost to learn its position relative to an invisible
boundary; sourcing has no target spec ("what profile would even clear?"); and the 11-08
§4 decision will otherwise be taken without knowing whether *any* achievable profile
clears the gate.

Symptom-only phrasing: *for a proposed candidate profile, the program cannot currently
say whether the eval geometry could fund it even at perfect signal quality.*

---

## §2 — The test (FIXED — the entire grid is declared here)

Sweep synthetic daily-P&L profiles through the frozen engine at corrected geometry and
record, per cell, whether the frozen floor clears.

| Item | Fixed value |
|---|---|
| Engine | `run_partition_mc` (frozen primitive) → `run_tier_remc`, 10K sims × seeds 42/123/2026, horizon 1500, Run-2 consistency-on, `dd_protection` OFF — inherited unchanged. |
| Geometry | CORRECTED (`dd_lock_offset_usd → 1_000_000.0` runtime patch, restored after). Primary tier `Tradeify_Select_100K`; secondary check row `MFFU_Rapid_100K` on the §6-decisive cells only. |
| Profile family (4-tuple) | (μ/σ, σ_d, shape, z) where **σ_d** ∈ {0.05, 0.10, 0.15, 0.20, 0.30, 0.45}% of account (daily vol on active days); **μ/σ** ∈ {0.00, 0.025, 0.05, 0.075, 0.10, 0.15} (daily edge ratio); **shape** ∈ {gaussian, student-t ν=4, trend-mixture p_win=0.35, meanrev-mixture p_win=0.65} (mixtures = two-point win/loss profiles matching the cell's μ, σ); **z** ∈ {0.0, 0.4} (fraction of zero-P&L days — trade-cadence effect on consistency + time-to-target). |
| Grid size | 6 × 6 × 4 × 2 = **288 cells**, fixed. No post-hoc extension (a wider/finer grid is a fresh pre-registration). |
| Synthetic generation | Seeded per cell as `seed = 20260724 + cell_index` (deterministic, date-free at runtime); series length = panel-equivalent 1692 bdays, blocks fed to the engine exactly as a real daily series would be. |
| Recorded per cell | `headline_bust`, `pass_rate`, `median_days` (diagnostic), `floor_ok`. |
| Validation anchors (pre-declared) | The runner, fed the **real** c1 daily series (1.00× and 0.50×, corrected geometry), must reproduce the published corrected busts within ±0.15pp (4.74% at 1.00×; the 2026-07-24 corrected 0.50× figure). Then the profile-sufficiency check: the c1 series' fitted 4-tuple's cell must predict the real bust within **±0.5pp**; the residual measures whether the 4-tuple family is a sufficient summary. A larger residual routes to AMBIGUOUS (§6). |
| Deliverables | `envelope.json` (288 cells) + `RESULTS.md` with (i) the boundary table — minimum μ/σ that clears, per (σ_d, shape, z); (ii) the σ_d ceiling (max vol fundable at any declared μ/σ); (iii) the c1 and CFD-book profile positions relative to the boundary (context only, no re-scoring claim). |

**Practicality ceiling (fixed here, used by §4):** cells with **μ/σ ≤ 0.10** are
"practical" — a persistent daily edge ratio above 0.10 (≈ annualized Sharpe ≳ 1.6 net,
sustained) is beyond anything this program has ever measured on any panel, so an envelope
populated only above it is empty in practice.

---

## §3 — Inherited unchanged (cited, not re-decided)

- Frozen floor bust ≤ 3.0% + P(pass) ≥ 50%; engine seeds/sims/horizon (gate prereg `be6dda6`).
- Corrected-geometry idiom (withdrawal ADR / correction study).
- Harvest intake rules incl. K_intrinsic ≤ 3 and screen constants (`strategy_harvest.md`).
- TERMINAL status of the Striker reconstruction lane; ORB-MNQ PARK (ADR `13ad9a1`).

---

## §4 — Falsifiable hypothesis (H-GEOFIT; binary)

**H-GEOFIT — if** the mapped envelope contains ≥ 1 **practical** cell (μ/σ ≤ 0.10, any
σ_d ≥ 0.05%, any shape, any z) whose `bust ≤ 3.0% AND pass ≥ 50%` at corrected
`Tradeify_Select_100K` geometry **and** the validation anchors hold, **then** the
four-firm eval class can in principle fund an achievable profile — the envelope becomes
the standing Phase-0 geometry pre-screen (lookup, zero marginal cost, zero K) and the
archetype spec that harvest sourcing targets (a named fork, separately scoped; not gated
by this brief). **Otherwise** (zero practical cells, anchors holding) H-GEOFIT is
**falsified in the direction that matters**: corrected trailing-DD geometry at the frozen
floor funds **no achievable daily-P&L profile**, every future candidate is pre-doomed at
this tier class regardless of signal quality, and the finding routes to the operator as
primary 2026-11-08 §4-review evidence (the honest default becomes demotion or a
venue-class change, not more discovery).

Accept/reject (restated numerically): accept H-GEOFIT if ≥ 1 of the 192 practical cells
(μ/σ ≤ 0.10) has `floor_ok = true`; reject if 0 of 192. The 96 cells above the
practicality ceiling are reported diagnostics and can neither accept nor reject.

---

## §5 — Forbidden moves (each genuinely tempting)

- **Using the envelope to re-open Striker MYM/MNQ reconstruction or to unpark ORB-MNQ**
  ("the envelope shows a profile like ORB clears, so…") — the lane is TERMINAL / PARKED
  by operator ruling; re-open requires a fresh operator GO + pre-registration, and this
  brief cannot be cited as either.
- **Reverse-engineering a strategy to the envelope** — an in-envelope profile is a
  *necessary* condition, not an edge. Optimizing a signal to land in the envelope is the
  SNAG/best-of-K trap relocated to geometry space; candidates still enter only via
  harvest admission (K-carrying) or pre-registered discovery.
- **Counting an envelope cell as candidate evidence** in any later brief ("the mechanism
  matches cell X, which passes") — the cell says the *shape* survives, nothing about
  whether the mechanism produces that shape out-of-sample.
- **Extending or refining the grid after seeing the surface** — 288 cells is the
  declared map; a finer boundary map is a fresh pre-registration citing this one.
- **Softening the floor, scoring at defective geometry, or inventing an
  envelope-specific floor** — the pre-registered-floor rule binds identically here.
- **Spending data budget** — this runs entirely on synthetic series + already-pinned
  panel series; any databento pull under this brief's name is out of scope.
- **Skipping the validation anchors because "it's the same engine"** — the anchors test
  the *profile family's sufficiency*, not the engine; without them an empty/full envelope
  is uninterpretable.

---

## §6 — Gate criteria (binary dispositions)

| Verdict | Trigger | Disposition |
|---|---|---|
| **RESOLVED-ENVELOPE-NONEMPTY** | Anchors hold and ≥ 1 practical cell clears | Envelope published as the standing Phase-0 geometry pre-screen; archetype spec handed to harvest sourcing as a named fork (own scoping, own gates); 11-08 review cites the boundary |
| **FALSIFIED-ENVELOPE-EMPTY** | Anchors hold and 0 of 192 practical cells clear | Program-level finding: this tier class funds no achievable profile at the frozen floor — routed to the operator for the 11-08 §4 review; discovery sourcing at these tiers pauses pending an operator venue/floor decision (the floor itself is NOT edited by this brief) |
| **AMBIGUOUS-PARAMETERIZATION** | Any validation anchor misses (engine repro > ±0.15pp, or profile-sufficiency residual > ±0.5pp) | The 4-tuple family is an insufficient summary — publish the residual, close, and re-scope with a richer profile family in a fresh brief; no envelope claim is made |

---

## §7 — Prior looks + K accounting

No envelope map has ever been produced (grep hook §10-1). The grid is pre-declared and
performance-blind: no candidate return data is consulted in constructing or reading it,
no cell is selected by observed performance, and nothing tradable exits this brief —
**zero discovery K is consumed** (the K-ledger and `discovery_manifests/` are
untouched). The validation anchors reuse two already-published measurements (corrected
1.00× 4.74%; the 2026-07-24 corrected 0.50× figure) — republication, not new looks. Any
candidate later sourced *against* the envelope carries its own K per
`strategy_harvest.md`; the envelope grants no K discount.

---

## §8 — Run protocol (post-signature)

1. Runner `lab/archive/q_geofit_1_2026-07/run_envelope_map.py` — imports the frozen
   primitives (`run_partition_mc`, `load_scoring_thresholds`), patches corrected
   geometry, generates the 288 seeded synthetic series, scores each, restores offsets.
2. Anchor runs first (c1 real series at 1.00× / 0.50×, + fitted-cell prediction); a miss
   halts before any grid cell is interpreted.
3. Grid sweep (~30–60 min wall at frozen sims; may run in halves); `envelope.json` +
   `RESULTS.md` per §2 deliverables; secondary MFFU check on the boundary cells only.
4. Adjudicate §6; route per disposition. RESULTS header cites this brief + the gate
   pre-registration by path.

---

## §9 — Operator signature (gates the run; DRAFT until filled)

```
SIGNED / FROZEN: 2026-07-25 / JA          (operator-directed in-session:
                                           "apply my Q-GEOFIT-1 §9 signature
                                            and kick it off")
Authorizes: the 288-cell envelope map + validation anchors, corrected geometry,
frozen floor, zero data spend. Grid/floor/practicality-ceiling fixed as §2/§4.
Explicitly does NOT authorize: any candidate work, any reconstruction re-open,
any harvest admission — those remain separately gated.
```

---

## §10 — Audit hooks (runnable)

```bash
# 1. No prior envelope exists (expected: no hits outside this brief).
grep -rn "funding envelope\|envelope.json" docs/ lab/ --include="*.md" | grep -v GEOFIT

# 2. Grid immutability: the declared axes appear exactly once, in §2.
grep -c "0.05, 0.10, 0.15, 0.20, 0.30, 0.45" docs/briefs/Q-GEOFIT-1-trailing-dd-funding-envelope.md   # expect 1

# 3. Floor unchanged (this brief must not restate a different one).
grep -n "3.0%" docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md | head -3

# 4. TERMINAL guard: the reconstruction ADR still carries the 2026-07-24 Addendum.
grep -n "TERMINAL\|terminal" docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md | head -3

# 5. Signature-before-run: while the §9 block holds "____", no runner may exist.
ls lab/analysis/ | grep -i geofit || echo "no Q-GEOFIT runner yet (expected while DRAFT)"

# 6. Zero-K claim: discovery manifests untouched by this brief's execution.
git log --oneline -3 -- discovery_manifests/
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python scripts/check_brief.py \
  docs/briefs/Q-GEOFIT-1-trailing-dd-funding-envelope.md --type inquire

# §0 anchors (Rule-0 confirmation)
git log -1 --format='%h %ci' -- core/mc/simulation.py                       # f8f8db1
git log -1 --format='%h %ci' -- core/firm_rules.py                          # fd95c72
git log -1 --format='%h %ci' -- docs/methodology/strategy_harvest.md        # 268851b
git log -1 --format='%h %ci' -- docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md  # 13ad9a1
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-24 | Drafted (`DRAFT — awaiting operator signature`); 288-cell grid + practicality ceiling μ/σ ≤ 0.10 + validation anchors fixed pre-signature | Joshua (direction) + Claude Code (Fable 5) |
| 2026-07-25 | **§9 signed** (`SIGNED / FROZEN: 2026-07-25 / JA`, operator-directed in-session); status → executing; §8 run protocol started. Grid/floor/ceiling unchanged from the pre-signature draft | Joshua (signature) + Claude Code (Opus 5) |
| 2026-07-25 | **CLOSED `AMBIGUOUS-PARAMETERIZATION`.** A1 PASS both arms (Δ 0.003pp); A2 MISS 31.15pp clamped / **23.63pp at exact fit** ⇒ family omits skew. Both real books (c1 + CFD) fall outside the declared `z` range under every reading. Grid left unrun by operator election; $0.00 spend, zero K. Recorded three frozen-text defects (§4 count arithmetic 192/96→240/48; §8 runtime ≈8× low; undeclared zero-day placement law) as successor inputs | Joshua (signature + grid disposition) + Claude Code (Opus 5) |
