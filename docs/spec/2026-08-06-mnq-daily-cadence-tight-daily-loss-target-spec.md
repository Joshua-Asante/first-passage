# MNQDTL-1 — MNQ daily-cadence, tight-daily-loss target spec

**Type:** Target spec (decision artifact, `docs/spec/`) — same class as
[`2026-07-27-third-leg-target-spec.md`](2026-07-27-third-leg-target-spec.md)
**Status:** `RATIFIED` 2026-08-07 / JA — §8 signed. **Superseded-in-part-by** [ADR 2026-08-08](../adr/2026-08-08-edge-cohort-correction-and-necessity-retarget.md) / [TNEC-1](2026-08-08-tradeify-necessary-conditions-target-spec.md) (2026-08-08 / JA) for intake-gate role of §1 D1/D2/μ + §6; remains historical target; §3.1 C1–C11 stand. **This spec still authorizes nothing** (target
definition only). No code, no Pine, no allocation, no `dd_protection`, no lifecycle write, no rail
change, no account action, no venue re-open. **$0 · K=0 · no manifest · no candidate proposed,
admitted, or scored.**
**Authored:** 2026-08-06 · **Authors:** Joshua (direction: *"write the spec for a daily cadence,
tight daily loss target for MNQ, incorporating the findings we have made with MNQ so far across ICT
and ORB"*) + Claude Code (Fable 5)
**Amended:** 2026-08-07 — (1) operator clarification pre-ratification: D2 is **max realized loss
only** (winning-day P&L uncapped); income aspiration ≈$250/day average is not a profit ceiling;
variant **(b)** elects L = **$325** (published MNQ 0.85R EM2 frontier cell). (2) S1 forecloses R1;
§1.1 notes Q-MNQSEL-1 (selection headroom absent on restart clocks). (3) §8 ratified. Post-ratify
L changes still go through F-E. **2026-08-08** — intake-gate supersession-in-part by TNEC-1 (body unedited).
**Layer:** target definition. Sits **downstream** of the eval mechanism-shape screen
([`2026-08-05-eval-mechanism-shape-screen.md`](2026-08-05-eval-mechanism-shape-screen.md), EM0–EM5,
`RATIFIED 2026-08-06`) — this spec **adds two limbs (D1, D2) on top of EM0–EM5**; it restates none of them and
weakens none of them.
**Related:** [de-scope ADR + Addendum](../adr/2026-08-04-tradeify-venue-descope-eval-included.md)
(Tradeify-shaped *research* admissible; Striker redeploy barred — F2/F3 ruled [`S1 ADR`](../adr/2026-08-07-loop-s1-environment-ratification.md)) ·
[ORB re-park ADR](../adr/2026-08-03-orb-mnq-repark-payability-falsified.md) ·
[K-bank disclosure ADR](../adr/2026-08-04-family-k-bank-disclosure-not-gate.md) ·
[`ops/instruments/MNQ.md`](../../ops/instruments/MNQ.md) (the instrument ledger this spec inherits
wholesale in §3)

---

> ⚠ **READER INTERCEPT 2026-08-08 — edge-cohort provenance COHORT CORRECTED; frozen body unedited; intake-gate supersession `Accepted`.**
> §1.2's L=$325 election and §1.3's row "0.85R — **MNQ best-ever measured** (ORB-MNQ-1, N1)" rest on a mis-bound cohort:
> the 0.85R belongs to the **withdrawn Striker NAS100→MNQ pyramid edition** (0.35 trades/cal-day, correlated adds — the
> shape EM3 forbids), per [MNQBASE-1 §1.3](../briefs/rnd-pipeline/MNQBASE-1-tradeify-shaped-base-construct-harvest-scoping.md);
> ORB-MNQ-1's realized edge is **+0.0626R** ([re-park ADR §4](../adr/2026-08-03-orb-mnq-repark-payability-falsified.md)) —
> 6.4× below EM1 — and N1 contains no per-trade R. §3.2 **O1** ("ORB edge is real: 0.85R per-trade") and **O4** are false as
> written. **Superseded-in-part-by** [`ADR 2026-08-08`](../adr/2026-08-08-edge-cohort-correction-and-necessity-retarget.md) §8 /
> [TNEC-1](2026-08-08-tradeify-necessary-conditions-target-spec.md) (`RATIFIED`): §1 D1/D2/μ election + §6 gate demoted from
> **intake gates** to recorded preferences. This spec remains `RATIFIED` as historical target; §3.1 doors C1–C11 stand.
> Do not quote §1.3's 0.85R row, O1, or O4 without this note.
>
> ⚠ **§4 FALSIFIER DISPOSITION 2026-08-08 — this spec carries NO live falsifier. Frozen §4 table below unedited.**
> The intake-gate supersession demoted §6 but left §4's triggers dated and readable; dispositioned here so
> none fires on a premise that no longer exists — the stranded-falsifier class the 2026-08-08 quarterly
> programme audit counted **15** instances of (audit note lands with the Great Prune PR; this disposition
> does not depend on it).
>
> - **F-A** — **MOOT.** R1 foreclosed by S1; the frozen row already says so.
> - **F-B** — **MOOT, NOT `FALSIFIED`. Do not record §6 `FALSIFIED` on 2026-11-08.** Its premise — *"R2 dry ⇒
>   MNQ cannot host a daily-cadence tight-daily-loss construct at ≥ EM1"* — died with the gate it served.
>   (i) §6's μ ≥ $130/day gate is now a recorded preference, not an intake kill; (ii) L=$325 was elected
>   against a **phantom** 0.85R cell (ORB's realized edge is +0.0626R); (iii) the four Route B campaigns ran a
>   design whose promotion floor (\|ρ\| = 0.02 at σ(r) ≈ 6.9e-4 ≈ **0.3 pt per 1σ over 60 s**) sits an order of
>   magnitude below the 0.95 pt round trip and the 3–9 pt/trade band EM1 requires — *a search that could not
>   have licensed a viable candidate even on success*. **A dry pipeline under an unwinnable design is evidence
>   about the design, not about the instrument.** Recording `FALSIFIED` would enter a false finding about MNQ
>   — and one the estate already contradicts: `Q-MNQSEL-2` cleared 0.40R with real margin (S3 ≈ 0.858 both
>   arms) on the dense-1m G=10 cell, inside the catalogue-K-wall's viable 5–20 pt stop band. F-B's *"within a
>   K ≤ 2 budget"* ambiguity (per-campaign catalogue size vs cumulative program budget) is **moot with the
>   trigger** and needs no ruling.
> - **F-C** — **MOOT.** F3 ruled no-successor 2026-08-07; already scoped in-table.
> - **F-D** — **MOOT.** Its repair action ("re-derive §1.2/§1.3") targets exactly the rows this intercept
>   marks phantom and the supersession demoted; there is nothing left for it to re-derive.
> - **F-E** — **DISCHARGED by supersession.** TNEC-1 *is* the re-issue F-E anticipated ("this spec is
>   superseded by a re-issue") — reached via §8 change control rather than an L re-election.
>
> **Net:** MNQDTL-1 is a **historical target** plus its §3.1 doors C1–C11. Nothing here is owed at 2026-11-08.
> Live intake gating is [TNEC-1](2026-08-08-tradeify-necessary-conditions-target-spec.md). Re-electing D1, D2
> or μ as gates is a fresh ratification against the **corrected** cohort table — never against the phantom.

## §0 — Rule 0 reads (production source, verified 2026-08-06 at HEAD `5f5519a`, worktree clean)

| Source | Anchor (`git log -1`) | What it grounds |
|---|---|---|
| [`core/firm_rules.py`](../../core/firm_rules.py) `Tradeify_Select_100K` block ±20 lines | `83b665d` 2026-08-06 | Eval geometry: $3,000 EOD trailing rope (no lock, `dd_lock_offset_usd` unreachable) · target $6,000 · `daily_loss_pct: None` (**the venue has no daily-loss rule — D2 is operator-imposed**) · idle ≥1 trade/Mon–Fri week · consistency 40% soft · 80-micro cap · $0.91/side. Intraday-vs-EOD breach-clock residual: **every bust figure here is a lower bound.** |
| [`docs/spec/2026-08-05-eval-mechanism-shape-screen.md`](2026-08-05-eval-mechanism-shape-screen.md) §2, §2.0b, §5 | `87b0547` 2026-08-05 | EM0–EM5, composed with in §2. Its §5 forbids reintroducing a trades-per-day floor **unless justified as a preference with a stated reason** — §1.1 below is that justification, on the record. |
| [`ops/instruments/MNQ.md`](../../ops/instruments/MNQ.md) W1–W4, N1–N16, DEAD list, F2 guard | `9d8dffc` 2026-08-06 | The ICT + ORB findings inherited as constraints in §3. Read in full this session, both pages. |
| [`lab/analysis/c1/eval_inverse_requirements_2026-08-03/RESULTS.md`](../../lab/analysis/c1/eval_inverse_requirements_2026-08-03/RESULTS.md) §1 B3, §2, §2a, §4 | `cdfd2f8` 2026-08-03 | `μ_max = k × r_max × E` (linear in frequency, capped in size); max risk/trade **flat at $275 across k=1→4** at 0.65R; the **0.40R inversion floor**; hard-stop gap tail (0.6% → 8.0% bust when 5% of losses gap 5×). |
| [`lab/analysis/c1/eval_slow_archetype_2026-08-04/RESULTS.md`](../../lab/analysis/c1/eval_slow_archetype_2026-08-04/RESULTS.md) §4.2, §5 | `cad464f` 2026-08-04 | k=1 frontier by measured edge: **$250 @ 0.49R (μ $122.5/d, 46d) · $275 @ 0.65R ($178.8/d, 32d) · $325 @ 0.85R ($276.2/d, 21d)**, all ≤1% fail on the EOD clock; "MNQ's 0.85R is better than any configuration simulated"; verified no-time-limit venue fact. |
| [`docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md`](../adr/2026-08-03-orb-mnq-repark-payability-falsified.md) | `9b5ce43` 2026-08-03 | T2 FIRED: ORB-MNQ standalone at Tradeify busts ≥67.67% intraday-honest at every admissible k; falsification scoped to **one target at one firm**; non-Tradeify venues need **fresh GO + survivor-scoring pass before any unpark**. |
| [`docs/notes/2026-08-04-orb-cadence-role-adjudication.md`](../notes/2026-08-04-orb-cadence-role-adjudication.md) | `dc7adcc` 2026-08-04 | S7 kill of ORB as a *co-leg beside the incumbent book*: the property that fires daily is the property that occupies `MNQ1!` every session. Scope: same-account slot only — contingent on F2. |
| [`lab/analysis/c1/catalogue_k_wall_2026-08-05/RESULTS.md`](../../lab/analysis/c1/catalogue_k_wall_2026-08-05/RESULTS.md) | `87b0547` 2026-08-05 | DSR floor by catalogue size 0.650/0.850/0.980/1.060 at K=1/2/3/4; working budget **K=1–2**; MNQ-specific viable stop band **5–20 pt** (2-pt cell dead twice over); Route A favoured. |
| [`docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md`](../adr/2026-08-04-family-k-bank-disclosure-not-gate.md) | `2ef7405` 2026-08-04 | `K_eff = K_intrinsic`; `K_banked(family)` is mandatory **disclosure**, never a gate. Disclosure for this spec: re-derived from `discovery_manifests/` 2026-08-06 — **K_banked(MNQ/NQ) ≈ 20** (d5 1 · st_eh executed-split 1 · MNQPOOL 1 · MNQFVG 1 · MNQFLOW 1 · MNQSR-1 14 counted once, its `…b` manifest being a seed-fixed re-score of the same construct · Q-CAPA-1 1 per ledger N16 · `orb_mnq_intraday_breakout` 0, closed `executed_k=0`). ⚠ **Cap seat SPENT** (ledger N16) — any new Cap-seat discovery cell needs a fresh operator reservation. |
| [`ops/prop_envelope_default.md`](../../ops/prop_envelope_default.md) E1–E7 | `1143117` 2026-08-06 | Four-firm tradability envelope, composed with (§2), unchanged. |
| [`docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md`](../adr/2026-08-04-tradeify-venue-descope-eval-included.md) + Addendum | `8dffb9f` 2026-08-06 | Deployment bar (two Striker legs) vs research permission (this spec). Forks F2/F3 later ruled [`S1 ADR`](../adr/2026-08-07-loop-s1-environment-ratification.md) 2026-08-07. Funded-phase Tradeify economics measured hostile ($299.80/acct-mo · 49.06% 1-yr mortality) — quoted in §1.4 as an out-of-scope disclosure. |

**Gitignore pre-flight:** `**/*.pine` is ignored. No Pine source is read or cited; no constant below
derives from Pine. Citation-chain mode not required.
**Contingency note:** none — every figure traces to a file in this table.

---

## §1 — The target (what is being decided)

### 1.1 — D1: daily cadence — an operator-elected preference, recorded as such

The construct's natural cadence must satisfy: **≥1 trade on ≥80% of RTH sessions, median ≥1
trade/session over any rolling 20-session window.** This strictly tightens EM4 (weekly floor) and
clears it by construction — no token-trade mitigation is ever owed.

**Stated reason, as the EM screen's §5 requires:** the venue does not require this (ledger **N13**:
no eval time limit, verified at three primary sources; the only venue cadence rule is the weekly idle
clock). D1 exists because the operator wants a **daily P&L cadence** — direction of 2026-08-06:
*"make on average $250 a day … trading everyday."* That quote is an **income aspiration** (μ\* ≈
$250/day average across sessions — some days may print +$500), **not** a per-day profit ceiling and
**not** a §6 gate. It is an income-shape preference, elected with the arithmetic in §1.3 in front of
the decision, not inherited as a venue requirement.

**Opportunity density is not the constraint** (ledger **N11**): MNQ supports a strict upper bound of
145 independent tradeable windows/day at a 40-pt stop; 99.9% of sessions clear 3/day. Abundant
windows make the 0.40R edge floor *more* load-bearing, not less (the §2a inversion trap).

⚠ **Selection is not free headroom** ([`Q-MNQSEL-1`](../briefs/rnd-pipeline/Q-MNQSEL-1-selection-value-ceiling-scoping.md)
`CLOSED-FALSIFIED` 2026-08-07): on causal Step-1 restart clocks at s=40, oracle top-1/day mean net R
sits just **under** EM1 0.40 on both arms. N11 proves opportunity exists; it does **not** prove a
selector clears the floor. R2 must bring a **different causal candidate set** — not denser OF on the
same clocks, not completed-window ranking.

### 1.2 — D2: tight daily loss — operator-imposed, not a venue rule

**Max realized loss per calendar day: L = $325**, enforced at the execution layer (hard per-trade
stops plus a daily stop-down: no new entries after the day's realized P&L reaches −$325). **Winning-day
P&L is uncapped** — D2 truncates the left tail of *loss days* only; a session may print +$500 (or
more) without violating this limb. The venue has no daily-loss rule (`daily_loss_pct: None`); D2 is
self-imposed. Mechanically: **k·r ≤ $325** across the day's independent entries, or equivalently a
daily risk budget L = $325.

**Provenance for L:** the published k=1 EM2-safe frontier cell at MNQ's best measured edge —
**$325 @ 0.85R → μ $276.2/day** ([`eval_slow_archetype_2026-08-04/RESULTS.md`](../../lab/analysis/c1/eval_slow_archetype_2026-08-04/RESULTS.md)
§4.2). Elected as variant **(b)** on 2026-08-07 so the §1.1 income aspiration is arithmetically
reachable at measured edge without inventing a new constant. Still ≪ the $3,000 EOD rope.

Two derived consequences:

- **Rope safety at the elected cell.** $325/trade is the ≤1%-bust frontier row at 0.85R (0.9% EOD
  bust in the slow-archetype study). Below 0.85R the EM2 frontier is *tighter than* $325 —
  interpolate down, never up (EM2). At 0.49R the published cell is $250; at 0.65R it is $275.
- **The loss cap is only as hard as the stops.** EM3's gap tail applies unchanged: 5% of losses
  gapping 5× moves bust 0.6% → 8.0%. An intraday-complete, flat-by-16:00 construct removes overnight
  gaps; fast-tape slippage through stops remains and must be disclosed in any re-score, not assumed
  away.

### 1.3 — The income arithmetic (output, not input)

Under a hard daily **risk** budget L, expected daily P&L is bounded by **μ ≤ L × E**, where E is
per-trade net expectancy in R (from `μ_max = k × r_max × E` with k·r ≤ L; splitting L across more
trades changes k and r but not the product). This bounds *expectation*, not the max winning day.
At L = $325:

| Per-trade edge E (net) | Provenance | μ/day bound | vs aspiration μ\*=$250 | Median active days to +$6,000 |
|---|---|---|---|---|
| 0.40R | EM1 floor (below it, frequency inverts) | **$130** | short | ~46 |
| 0.49R | MYM measured (weakest live-venue-edition edge) | **~$159** | short | ~38 |
| 0.65R | generic reference config | **~$211** | short | ~28 |
| 0.85R | **MNQ best-ever measured** (ORB-MNQ-1, N1) | **~$276** | **clears (+$26)** | **~21** (study) |
| 1.00R | *no MNQ construct has ever measured this* | $325 | clears | ~18 |

**Read this table honestly:** under L = $325 the operator's $250/day *average* aspiration is
**reachable at MNQ's best measured edge (0.85R)** and remains aspirational at weaker edges. The
aspiration is still **not a gate of this spec** (chasing μ\* by thinning EM1 is forbidden — §5); the
§6 gate is EM1 restated in daily units: **μ ≥ $130/day** (= L × 0.40R). Further raising L after
ratification is F-E, not a mid-investigation rescue.

### 1.4 — Scope disclosures

- Passing the eval is a sim milestone; **income is a funded-phase claim this spec does not price.**
  Tradeify's funded economics measured hostile (de-scope ADR: $299.80/acct-mo chain, 49.06% 1-yr
  mortality); any successor venue's funded economics are F3 material.
- Consistency (best day ≤ 40% at pass) and the weekly idle clock are cleared **by construction**
  under D1/D2 — steady days sized to L=$325 against a $6,000 cumulative target never approach the
  $2,400 best-day soft gate; upside days are uncapped by D2 but the 40% rule remains a venue soft
  gate at pass.
- Serial correlation of losing days is not modelled in the frontier; direction of error is
  optimistic (inherited scope limit).

---

## §2 — Screen composition (nothing restated, nothing weakened)

A candidate under this target must clear, in order:

| Screen | Owner | Status | This spec's delta |
|---|---|---|---|
| **EM0–EM5** (catalogue ≤3, edge ≥0.40R net at $0.95/side, edge-indexed risk ceiling, independence + stop integrity, weekly cadence, session/slot legality) | eval mechanism-shape screen | `RATIFIED 2026-08-06` | **D1 tightens EM4** (daily vs weekly). **D2 = L $325 is identity with the 0.85R EM2 cell** ($325 → $325); may still tighten weaker-edge frontier cells if any published cell exceeds $325. Neither limb loosens EM0–EM5. |
| **E1–E7** four-firm tradability | `ops/prop_envelope_default.md` | RATIFIED | none |
| **S1–S7** same-account slot legality | third-leg target spec | RATIFIED | applies **only if** a same-account slot is sought; LEG_MAP still retained-not-released under S1 (headroom not freed). The S7 kill of ORB-as-co-leg does not bind a *standalone* deployment (§3, O6). |
| **Harvest Req 1–5** | `strategy_harvest.md` | Accepted | applies to harvested candidates; MNQBASE-1's intake pass already ran dry once (§3, O8) |
| **Route A/B K discipline** | Avenue A ADR + K-bank ADR | Accepted | catalogue ≤3 cells (EM0), working budget K=1–2, Route A (survivor-tied, K=1) favoured per the catalogue-wall session finding; **Cap seat requires fresh reservation** (§0) |

**Cost authority:** EM1's — `strategy_harvest.md` Requirement 5, screened at $0.95/side. This spec
defines no cost formula (the §3a fracture is on the 08-08 board as G3; this spec re-points with EM1
if that ruling moves).

---

## §3 — Findings inheritance: what ICT and ORB have already settled (binding constraints)

The instrument ledger is the canonical home; this section binds its contents to *this target* and
does not restate numbers it doesn't use. Two classes: **closed doors** (re-proposal barred absent
new mechanism evidence — not new parameters) and **open structure** (usable, with scope).

### 3.1 — Closed doors (any candidate keying on these is `SHAPE-DEAD` at intake)

| # | Door | What killed it | Source |
|---|---|---|---|
| C1 | ICT 1H premium/discount as a directional gate | FALSIFIED three-limbed, well-powered, multi-regime; premium resolved *up* (0.4537, CI below 0.5) | ledger DEAD list, Q-ICT-MNQ-1 |
| C2 | ICT weekly `vStruct` bias as a **sub-weekly** gate | FALSIFIED by its base-rate-matched placebo (53.77% vs p95 53.82%); four of five limbs passed — only the placebo caught it | Q-WLEGB-1 |
| C3 | Liquidity pools as attractors ("price is drawn to old highs/lows") | Anti-attractor, replicated on 3 instruments + externally (N9, N12); both constructs expressing it died on **reach** — surviving pools sit a median 572 pt away, consumed FVG edges 291 pt | MNQPOOL-1, MNQFVG-1 |
| C4 | ICT raid→FVG→DOL chain as an entry | First expectancy ever computed: −$4.90/trade net, CI straddles zero, **basis-invariant** (negative even at zero commission) | Q-ICTEXP-1 + 08-04d |
| C5 | Intraday momentum (Baltussen class) | OOS edge −0.327 bp, gross Sharpe −0.13, after the cost hurdle fell 3.7× exactly as predicted | D5-RECOST-1 (N5) |
| C6 | Opening-volume / opening-pressure signatures | Nulls at n≈2,100–2,400 — precise, not underpowered; externally corroborated | OPENPRESS-1, N12 |
| C7 | ORB conditioning gates (gap / GEX / T10Y3M / DOW) — **and any fifth gate wearing a new label** | Four pre-registered attempts FALSIFIED; the F2 guard names post-hoc slice-laundering as this instrument's highest-risk move. K no longer forecloses a filtered variant — **the evidence does** | ledger DEAD list + F2 guard |
| C8 | ORB exit redesigns (tighter stops, fixed targets, 15:30 exit, session truncation) | Pre-killed order-free: every f<1.0 loses 0.03–0.06R; no target beats baseline; the 0.50R give-back is real but **unharvestable**; EOD-adversity line closed tail-exhausted | N3 + 08-02 session entry |
| C9 | Top-of-book / depth features as entry signals | MNQFLOW-1 FALSIFIED (wrong-signed, p_emp 0.633); book too thin (median 67 contracts across 20 levels); route-2's cheapest swing closed | ledger DEAD list |
| C10 | Bars-only S/R families (pivots, fibs, camarilla, VWAP, ATR bands…) | 0/14 BH-FDR survivors, Phase B/C not licensed | mnq_sr_structure_2026-08-06 |
| C11 | N14/N16's L1 tilt as a **gate or filter** | Structurally barred: FM-1 never conditioned on outcome; it is a registered PF-CUSUM **companion tripwire**, docs-only — converting it to a gate is a fresh K-bound axis and would recreate C7 | N14/N16 + companion ADR |

### 3.2 — Open structure (usable, each with its scope pinned)

| # | Finding | Use under this target | Scope limit |
|---|---|---|---|
| O1 | **N1** — ORB edge is real: 0.85R per-trade, Stage-2/5/6/8 clean, `K_eff=2` | The only measured construct that satisfies D1 by nature (fires ~daily) | Regime-conditional; **full-window basis clears only Bulenox ≤1 tick**; 2021+ clears all four firms to 3 ticks. Quote with the Stage-7 rider, always |
| O2 | **N2** — ORB fills are known-good (81-tick median penetration, 0.7% shallow-touch) | Fill mechanics are not the risk; commission basis is | measured on TV export realism panel |
| O3 | **N11** — 145 independent windows/day ceiling | Kills "MNQ can't support daily cadence" objections | a RANGE, not a capture; licenses nothing |
| O4 | **N13** — no eval time limit; k=1 at 0.85R → 21-day median pass | The slow-archetype frontier §1.3 builds on | assumes independence; not a re-measurement of any incumbent |
| O5 | **N8** — weekly structure hit rate 0.5751 (MNQ) / 0.5880 (NQ) | A weekly-bar fact only | **does not transfer below the weekly close** (C2); no deploy license |
| O6 | S7 occupancy kill (cadence adjudication) | Binds ORB **as a co-leg beside the incumbent book** on one account | The incumbent legs are withdrawn; standalone deployment on a fresh account/venue is outside S7's scope — apply S1–S7 only if a shared slot returns under F2 |
| O7 | **W1–W4** data warnings + N7 panel provenance | Any harness under this target: `.v.0` roll rule, UTC weekend-bar drop, native-micro fill validation (never TV-tester fills), micro-era OOS reserve | standing |
| O8 | MNQBASE-1 intake result | External harvest for a Tradeify-shaped MNQ base construct ran **dry** at P2 (no named counterparty constraint) — expect R2 sourcing to fail the same way absent a new channel | N12 corroboration is rank-6, non-quantitative |
| O9 | Catalogue-wall MNQ half | New-construct stop band **5–20 pt** (2-pt cell dead twice over); required predicted edge 3–9 pt/trade | EM0 catalogue ≤3 cells regardless |

### 3.3 — The D2 × ORB coupling (named risk, must be measured, not assumed)

At L = $325/day and $2.00/pt, one micro is permitted only when the stop ≤ **162.5 pt**. ORB's stop is
the full OR range (load-bearing per N3 — winners sit through 0.34R median adverse excursion), and the
ledger already records the analogous arithmetic biting: at the 0.50× WATCH basis, MNQ base size
rounded to 0 at stops ≥93 pt (RECORD section, NOT-M8). **Sessions with OR range > 162.5 pt become
forced skip-days under D2, which erodes D1 from the other side.** Any R1 re-score (§4) must report
the skip-day fraction from the OR-range distribution (`mnq_stop_distribution_2026-08-02` is the
existing study home) and re-check D1's ≥80% floor *after* skips. If D1 and D2 cannot hold
simultaneously on ORB's realized distribution, that is a §6 FALSIFIED, not a licence to widen either
limb.

---

## §4 — Hypothesis and falsifiers

> **Scoping note (S1 ADR 2026-08-07):** F3 ruled **no successor migration**; incumbent
> `Tradeify_Select_100K` eval is the environment for **new** strategies. That **forecloses R1**
> (successor-venue precondition + F-A/F-C as written below). **R2 is the live route.** Body below
> is frozen; do not silently rewrite — this note is the reader-intercept ([S1 ADR](../adr/2026-08-07-loop-s1-environment-ratification.md)).

**H:** *A construct satisfying D1 (daily cadence) and D2 ($325/day max realized loss) and clearing
EM0–EM5 exists on MNQ and survives survivor-scoring on a registered successor-venue basis —
concretely: honest-clock (intraday) eval bust ≤ 1.0% at D2 sizing, realized μ ≥ $130/day (E ≥ 0.40R
at L = $325, i.e. EM1 restated in daily units), and D1's ≥80% session-coverage floor held after D2
skip-days.*

If no such construct exists, the daily-cadence tight-daily-loss target is falsified for MNQ and the
operator's income shape must come from (a) a further-raised L (F-E), (b) a different instrument, or
(c) the lumpy-cadence book the program has already validated.

**Two candidate routes, exhaustive under current evidence:**

- **R1 — ORB-MNQ-1 standalone, re-scored under D2 on an F3 venue basis.** ⚠ **FORECLOSED 2026-08-07** (S1 no-successor ruling). The only measured
  candidate whose natural cadence satisfies D1. Preconditions from standing ADRs: F3 must register a
  successor venue (Bulenox is the only basis where the full window clears — O1 rider); re-park ADR
  requires **fresh operator GO + survivor-scoring pass before any unpark**; the re-score must use
  ORB's **own realized trade series** (never the archetype frontier — T2's ≥67.67% Tradeify bust was
  measured on the realized distribution and busts March 2020 on both clocks), with the $325
  stop-down and §3.3 skip-rule pre-registered, on the intraday-honest clock. The daily max-loss is an
  ops-layer control (like `dd_protection`) — it touches no locked parameter and is not an exit
  redesign under C8, but it **changes the realized distribution and must be scored, not asserted**.
- **R2 — a new construct** via Route A (survivor-tied, K=1) or a Route B catalogue ≤3 cells,
  clearing §3.1's closed doors and §3.2/O9's structure. **Live route under S1.** Prior expectation: **LOW** — route-1 ICT is
  presumptively exhausted, route-2's cheapest swing is closed, C10 just closed bars-only S/R, and
  the external harvest ran dry (O8). A fresh Cap-seat reservation is required before any K-spending
  cell (§0). Scoring basis = incumbent eval environment (S1), not a successor venue.

**Falsifier triggers:**

| # | Trigger | Threshold | Action |
|---|---|---|---|
| F-A | R1 re-score fails | bust > 1.0% intraday-honest at D2 sizing, **or** μ < $130/day, **or** D1 coverage < 80% after skips | R1 dead for this target; record in the ledger DEAD list with the failing limb — **moot while R1 foreclosed** |
| F-B | R2 pipeline dry | no R2 candidate clears EM0–EM5 + §3.1 within a K ≤ 2 budget by **2026-11-08** (program §4 hard date) | with F-A, fires §6 FALSIFIED |
| F-C | No scoring basis | F3 unruled (no successor venue registered) by **2026-09-05** | §6 AMBIGUOUS-SUSPENDED — **scoped 2026-08-07:** F3 ruled no-successor; R1 foreclosed; R2 scores on incumbent eval — F-C as written does **not** suspend R2 |
| F-D | Geometry moves | any EM-screen §4 F-C constant changes, or a successor venue publishes a daily-loss rule tighter than $325 | re-derive §1.2/§1.3; supersede, never edit in place |
| F-E | L re-elected after ratification | operator re-ratifies §8 electing a different max-loss L | this spec is superseded by a re-issue; the arithmetic in §1.3 re-derives mechanically |

---

## §5 — Forbidden moves (each genuinely tempting under this target)

- **Chasing the $250/day average aspiration by thinning the edge floor.** The single most likely
  failure: D1 makes frequency feel free, and μ = k·r·E makes more trades look like more income.
  Below 0.40R the frequency result **inverts** (rope binds harder, size collapses). EM1 is not
  negotiable downward, and §6's μ gate is deliberately set at EM1 ($130/day at L=$325), not at μ\*.
- **Re-proposing a §3.1 closed door with new parameters.** The registry rule is new *mechanism
  evidence*, not new thresholds/windows/horizons. Specific standing temptations: a fifth ORB gate
  (C7, F2-guard), an N14/N16-derived filter (C11), a re-cut of the S/R families (C10).
- **Scoring R1 on the archetype frontier instead of the realized series.** The frontier is a
  *screen*; T2's falsification came from the realized distribution. Substituting the synthetic
  archetype where the realized series exists is exactly the optimism that the intraday-clock
  correction was built to remove.
- **Treating the D2 max-loss as edge.** A daily stop-down truncates the left tail of *days*; it adds
  no per-trade expectancy and interacts with D1 via §3.3's skip-days. It must appear in the
  re-score's loss column, not only in its risk column. It is also **not** a profit ceiling.
- **Widening D2 (or relaxing D1) mid-investigation to rescue a failing candidate.** That is the §6
  gate being amended to fit evidence — Known Trap #12. The legal path is F-E: re-ratify first,
  re-score after.
- **Deploying anything to Tradeify on this spec's authority.** The venue is de-scoped; this is
  research under the 08-04 Addendum. Any deployment needs F3 + fresh GO + a separate arming chain
  (M1 gate unchanged).
- **Quoting §1.3's μ bounds as forecasts.** They are arithmetic bounds at full risk-budget
  utilization under independence — every listed scope limit (serial correlation, gap tail,
  skip-days) pushes realized μ **down**.

---

## §6 — Gate (binary)

- **`RESOLVED`** — an **R2** candidate clears D1 + D2 + EM0–EM5 and its pre-registered
  survivor-scoring at: intraday-honest bust ≤ 1.0%, μ ≥ $130/day at D2 sizing (L=$325), D1 coverage
  ≥ 80% after skip-days, on the **incumbent** `Tradeify_Select_100K` eval basis (S1). Routes to an
  operator GO decision; **admits and arms nothing by itself.** (R1 foreclosed — do not score it.)
- **`FALSIFIED`** — F-B fired (R2 dry at K ≤ 2 by 2026-11-08; F-A moot while R1 foreclosed).
  Consequence recorded in `docs/rejected_candidates.md`: MNQ cannot host a daily-cadence
  tight-daily-loss construct at ≥ EM1 economics on the incumbent env; the income shape requires a
  further L raise (F-E), another instrument, or the validated lumpy book.
- **`AMBIGUOUS-SUSPENDED`** — not the standing path after S1: F-C as written does **not** suspend R2
  (incumbent scoring basis exists). Revisit only if a future ADR removes the incumbent environment.

Verdict string recorded as `D1 D2 EM0–EM5 | bust | μ | coverage` per candidate, so the failing limb
is never lost to a summary word.

---

## §7 — Standing-artifact relations (nothing retired here)

| Artifact | Relation |
|---|---|
| EM screen (EM0–EM5) | Parent (`RATIFIED 2026-08-06`); D1/D2 are additive limbs — restates none, weakens none. |
| Third-leg S1–S7 | Composed with, only when a same-account slot is sought (O6). |
| ORB re-park ADR | Untouched. R1 does **not** unpark ORB — it defines the survivor-scoring pass that ADR requires *before* any unpark question reaches the operator. |
| De-scope ADR + F2/F3 | F2/F3 ruled ([`S1 ADR`](../adr/2026-08-07-loop-s1-environment-ratification.md)): incumbent env; no successor. R1 foreclosed; R2 scores on incumbent. |
| `2026-08-02-tradeify-activity-rule-disposition-spec.md` | Unaffected for D1 constructs (no token trade owed once daily cadence lands); standing account still needs weekly idle coverage until then ([`STATE` row 0](../../STATE.md)). |
| Q-CADENCE-1 ≥90%-of-weeks floor | Not quoted as a requirement (it answers rescue-a-pair, per the EM screen §7 row 5 narrowing). D1 is stricter and differently grounded. |

---

## §8 — Ratification

```
RATIFICATION:    MNQDTL-1 adopted as a standing target spec: D1 (daily cadence,
                 operator preference, reason recorded) + D2 ($325/day max
                 realized loss, operator-imposed; winning-day P&L uncapped)
                 over EM0-EM5, gated per section 6.
                 Variant elected: (b) max-loss L = $325
                 (published MNQ 0.85R EM2 frontier cell).
                 Income aspiration ~$250/day average is not a profit ceiling
                 and is not a section-6 gate.
                 R1 foreclosed (S1 no-successor); R2 live on incumbent eval.
                 Target spec only - admits nothing, arms nothing, spends nothing.

DATE / INITIALS: 2026-08-07 / JA
```

**Change control:** §1–§3 change only by superseding spec or a §4 trigger firing. §1.3's table may be
re-derived without supersession only if an input study is corrected at source (it is arithmetic, not
a decision).

---

## §10 — Audit hooks (runnable)

```bash
# 1. The venue still has no daily-loss rule and the section 1 geometry holds (D2 stays operator-imposed).
python -c "
import sys; sys.path.insert(0,'core')
from firm_rules import FIRM_RULES
t = FIRM_RULES['Tradeify_Select_100K']
assert t['daily_loss_pct'] is None, 'venue grew a daily-loss rule -- D2 is no longer self-imposed; fires F-D'
assert t['max_dd_pct'] == 3.0 and t['inactivity_max_idle_days'] == 5, 'geometry drifted -- fires F-D'
print('D2 remains operator-imposed; geometry OK')
"

# 2. The frontier cells and inversion floor still trace to their studies, not to this spec.
rg -n '\$250|\$275|\$325' lab/analysis/c1/eval_slow_archetype_2026-08-04/RESULTS.md | head -5
rg -n '0\.40R' lab/analysis/c1/eval_inverse_requirements_2026-08-03/RESULTS.md | head -3

# 3. The closed doors in section 3.1 are still closed (no un-tombstoned reopen).
rg -n 'ict-liquidity|order-flow-depth-imbalance|intraday-momentum|opening-pressure' ops/instruments/MNQ.md | head -6
# Expected: all still verdict DEAD in the PROFILE cells block.

# 4. ORB-MNQ-1 is still PARKED with the payability falsification intact (R1 has not been silently unparked).
rg -n 'PARKED|FALSIFIED' ops/instruments/MNQ.md | rg -i 'ORB-MNQ-1' | head -3

# 5. The K-bank disclosure in section 0 re-derives (bank is disclosure-only; count, do not gate).
python -c "
import json, glob, os
ks = {os.path.basename(p): json.load(open(p, encoding='utf-8')).get('K') for p in glob.glob('discovery_manifests/*.json')}
mnq = {k: v for k, v in ks.items() if k.startswith('mnq') or k in ('d5_nq_intraday_mom.json','st_eh_supertrend_grid.json','orb_mnq_intraday_breakout.json')}
print(mnq)
"
# Expected: the section 0 derivation reproduces (mnqsr1 'b' file is a re-score of the same construct: count 14 once).

# 6. This spec changed nothing operational.
git diff --stat HEAD -- core/ ops/c1_rail/ '*.pine'
# Expected: empty
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python "$HOME/.claude/skills/brief-authoring/scripts/check_brief.py" \
  docs/spec/2026-08-06-mnq-daily-cadence-tight-daily-loss-target-spec.md --type adr

# Section 0 anchors still current
for f in core/firm_rules.py ops/instruments/MNQ.md \
         docs/spec/2026-08-05-eval-mechanism-shape-screen.md \
         lab/analysis/c1/eval_inverse_requirements_2026-08-03/RESULTS.md \
         lab/analysis/c1/eval_slow_archetype_2026-08-04/RESULTS.md \
         docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md \
         docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md; do
  git log -1 --format="%h %cs $f" -- "$f"; done
# Expected: 83b665d / 9d8dffc / 87b0547 / cdfd2f8 / cad464f / 9b5ce43 / 2ef7405
```
