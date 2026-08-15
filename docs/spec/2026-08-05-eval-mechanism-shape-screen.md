# Eval Mechanism-Shape Screen — what the Tradeify Select 100K geometry requires of a mechanism

**Type:** Screening standard (decision artifact, `docs/spec/`)
**Status:** `RATIFIED 2026-08-06` — §8 block filled; §7 dispositions ruled row-by-row (same session).
**This spec authorizes nothing.** No code, no Pine, no allocation, no `dd_protection`, no lifecycle
write, no rail change, no account action. Screening standard only — admits nothing, arms nothing,
spends nothing. **$0 · K=0 · no manifest · no candidate proposed, admitted, or scored.**
**Authored:** 2026-08-05 · **Ratified:** 2026-08-06 · **Authors:** Joshua (direction: *"the venue shapes the mechanism … what is the
minimum requirement"*) + Claude Code (Opus 5); ratification Cursor + JA
**Layer:** candidate screening. Sits **beside** [`ops/prop_envelope_default.md`](../../ops/prop_envelope_default.md)
(E1–E7, tradability at four firms) and [`2026-07-27-third-leg-target-spec.md`](2026-07-27-third-leg-target-spec.md)
(S1–S7, same-account slot legality). It replaces neither — see §3.
**Related:** [ADR 2026-08-04 venue de-scope + Addendum](../adr/2026-08-04-tradeify-venue-descope-eval-included.md)
(the Addendum is what makes Tradeify-shaped **research** admissible; deployment of the two Striker legs is not) ·
[ADR 2026-07-12 prop-portfolio](../adr/2026-07-12-prop-portfolio-four-friendly-firms.md) ·
[`strategy_harvest.md`](../methodology/strategy_harvest.md) (Req 1–5, unchanged and independent)

---

## §0 — Rule 0 reads (production source, verified 2026-08-05 at `45f88bf`, worktree clean)

| Source | Anchor (`git log -1`) | What it grounds |
|---|---|---|
| [`core/firm_rules.py`](../../core/firm_rules.py) `Tradeify_Select_100K` block | `8ec740d` 2026-08-05 | Every geometry constant in §1: `max_dd_pct 3.0` · `dd_type trailing_locking` · **`dd_lock_offset_usd 1_000_000.0` — unreachable, i.e. the eval has no lock** (fixed 2026-08-04; the 08-04 ADR's §0 still records the defective `100`) · `profit_target_pct 6.0` · `min_trading_days 3` · `consistency_rule_pct 40.0` · `inactivity_max_idle_days 5` · `micro_contract_cap 80` · `daily_loss_pct None` · `weekend_holds False` · `cost_per_side_usd 0.91`. Read with the ±20-line comment block above the tier per the §0 surrounding-context sub-rule — that block carries the intraday-vs-EOD residual quoted in §1. |
| [`lab/analysis/c1/eval_inverse_requirements_2026-08-03/RESULTS.md`](../../lab/analysis/c1/eval_inverse_requirements_2026-08-03/RESULTS.md) §1 B1–B3, §2, §2a, §4 | `cdfd2f8` 2026-08-03 | The rope→size frontier ($275 at 0.65R, ≤1% failure); `μ_max = k × r_max × E`; the **0.40R inversion floor**; the hard-stop sensitivity table (0.6% → 8.0%); the consistency arithmetic `max($6,000, 2.5 × best day)` and ⌈1/0.40⌉ = 3. |
| [`lab/analysis/c1/eval_slow_archetype_2026-08-04/RESULTS.md`](../../lab/analysis/c1/eval_slow_archetype_2026-08-04/RESULTS.md) §2, §4.2, §5 | `cad464f` 2026-08-04 | The k=1 frontier by measured edge ($250 / $275 / $325 at 0.49R / 0.65R / 0.85R); the 21-day median at MNQ's own 0.85R; the verified **"no time limit"** venue fact; §5's five scope limits, which this spec inherits verbatim into §2.3. |
| [`docs/notes/2026-07-24-tradeify-rulepin-verification.md`](../notes/2026-07-24-tradeify-rulepin-verification.md) Pins 1/2/6 | `cad464f` 2026-08-04 | Funded **$200** winning-day threshold (Pin 1, match) · funded ladder **30→40→50→80**, eval **not** scaled (Pin 2, mismatch corrected) · eval duration cap absent (Pin 6). Precedence: help-centre governs (FTA §11). |
| [`docs/notes/rail_build/TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md`](../notes/rail_build/TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md) §1, §2a | `10db7b9` 2026-08-05 | Idle rule is **≥1 trade per Mon–Fri week**, enforced by **irreversible account deletion** (no reinstatement, no refund) — the limb that makes EM4 a gate and not a note. Automation-identity obligations are STANDING on the eval today. |
| [`ops/prop_envelope_default.md`](../../ops/prop_envelope_default.md) E1–E7 | `cd8b617` 2026-08-02 | The four-firm tradability envelope this screen composes with, not replaces (§3). E1 flat-16:00 ET default; E2 consistency semantics (soft gate, delays never breaches); E5 micro sizing. |
| [`docs/spec/2026-07-27-third-leg-target-spec.md`](2026-07-27-third-leg-target-spec.md) §7 S1–S7 | `2345095` 2026-08-03 | The same-account slot screen, RATIFIED 2026-07-27. **S7 order-symbol occupancy** is imported by reference into EM5 rather than restated (§3). |
| [`docs/briefs/rnd-pipeline/MNQBASE-1-…-harvest-scoping.md`](../briefs/rnd-pipeline/MNQBASE-1-tradeify-shaped-base-construct-harvest-scoping.md) §2.1 T1–T7 | `5c5012c` 2026-08-04 | The prior, MNQ-scoped form of this screen — the primary supersession candidate (§7 row 1–3). |
| [`ops/instruments/MNQ.md`](../../ops/instruments/MNQ.md) N11, N13 | `b160ab2` 2026-08-05 | N13 already records T2's retirement as a durable ledger finding; N11 records that frequency is not structurally constrained on MNQ (145 independent windows/day at a 40-pt stop). This spec consolidates rather than re-derives. |

**Gitignore pre-flight.** `**/*.pine` is ignored. **No Pine source is read or cited**, and no constant
below derives from Pine — every number is a venue rule or a simulation output. Citation-chain mode not
required.

**Contingency note:** none. Every figure traces to a file in this table.

---

## §1 — Geometry held fixed (the input, not the screen)

Tradeify Select 100K, **evaluation** phase, from `core/firm_rules.py` at `8ec740d`:

| | |
|---|---|
| Rope | floor = running EOD peak − **$3,000**; ratchets up only; **no lock in eval** (`dd_lock_offset_usd` unreachable) |
| Target | **+$6,000** (6.0%) |
| Duration cap | **none** — verified in-browser 2026-08-04, three primary sources |
| Min days | **3** — the arithmetic shadow of ⌈1 ÷ 0.40⌉, not an independent constraint |
| Consistency | best single day ≤ **40%** of profit at the moment of pass ⇒ effective target `max($6,000, 2.5 × best day)`. Soft gate: delays a pass, never fails an account (envelope E2) |
| Daily loss limit | **none** |
| Idle clock | **≥1 trade per Mon–Fri week** (`inactivity_max_idle_days: 5`), enforced by **irreversible deletion** |
| Size cap | **80 micros** in eval (evaluations are **not** scaled; the 30→40→50→80 ladder is funded-only) |
| Flat | 16:45 ET, no weekend holds |
| Cost | $0.91/side all-in, index micros |

⚠ **Standing under-statement, carried not fixed.** The trail is enforced **intraday** at the venue; the
engine tests it at EOD close. **Every bust figure in this spec is a lower bound.** Source: the
`core/firm_rules.py` comment block above the Tradeify tiers, and the Phase-4 both-halves re-run spec.

---

> ⚠ **Amendment 2026-08-08 — edge-cohort provenance COHORT CORRECTED (reader-intercept; §2 table unedited per §8 change
> control).** EM2's "$325 @ 0.85R" cell and §0 row 3's "MNQ's own 0.85R": that 0.85R is the **withdrawn, pyramided Striker
> NAS100→MNQ venue edition** ([MNQBASE-1 §1.3](../briefs/rnd-pipeline/MNQBASE-1-tradeify-shaped-base-construct-harvest-scoping.md)),
> **not** "N1 / ORB-MNQ-1's realized edge" (realized **+0.0626R**, [re-park ADR §4](../adr/2026-08-03-orb-mnq-repark-payability-falsified.md)).
> EM2's principle (edge-indexed ceiling, interpolate down) and the cells' arithmetic stand; the cells' edge labels must be
> read as *hypothetical independent-entry edges*, not measured-construct provenance — re-derive per candidate.
> **Superseded-in-part-by** [`ADR 2026-08-08`](../adr/2026-08-08-edge-cohort-correction-and-necessity-retarget.md) §8 /
> [TNEC-1](2026-08-08-tradeify-necessary-conditions-target-spec.md) (`RATIFIED`): **EM1** re-typed to necessity
> (net expectancy > 0 after Req-5 costs + CI excluding 0 + DSR-at-K); 0.40R retained as **disclosure only**
> (frequency inversion). §2 EM1 row text below is historical; score intake against TNEC N-EDGE. EM0/EM2–EM5 unchanged.

## §2 — The screen

**Six limbs. A candidate passes the mechanism-shape screen iff all six hold** — EM0 (catalogue, §2.0b)
plus the five cell limbs below. Each is derived, not
chosen: the "why it binds" column names the venue rule that generates it.

| # | Limb | Threshold | Generated by | Why it binds |
|---|---|---|---|---|
| **EM1** | **Per-trade edge floor** | **≥ 0.40R net** of cost at the candidate's own realized basis. Screen at **$0.95/side** (the friendly-firm worst case, MFFU/BluSky-set) for portability, not Tradeify's $0.91. **Cost authority is [`strategy_harvest.md`](../methodology/strategy_harvest.md) Requirement 5** — this limb defines no formula of its own (see §3a) | rope + `μ_max = k · r_max · E` | Below ~0.40R the frequency result **inverts**: extra trades widen the daily distribution faster than they move it right, so the rope binds *harder* and the size cap collapses ($100 → $50 across k=1→8 at 0.139R). Frequency is a multiplier on an edge that already clears; it is never a substitute for one. |
| **EM2** | **Risk-per-trade ceiling** | **≤ the ≤1%-bust frontier at the candidate's own measured edge** — $250 @ 0.49R · $275 @ 0.65R · $325 @ 0.85R (≈0.25–0.33% of account). Interpolate down, never up | $3,000 fixed rope | The binding quantity is the depth of a losing **run** (streak × r) against a fixed rope — an order of magnitude under conventional 1–2% sizing. **Edge-indexed, not a constant**: quoting $275 against a 0.49R candidate over-sizes it. |
| **EM3** | **Independence + stop integrity** | Genuinely independent entries — **no pyramiding, no scale-ins, no same-signal multi-entry** — and **hard stops that hold**: no overnight holds, no illiquid instruments, no gap-exposed events | rope arithmetic + §4 tail table | k correlated adds at risk r ≡ **one** trade at k·r, which collapses to the k=1 row — the worst in the table, at a *worse* effective r. Separately: 5% of losses gapping 5× takes failure **0.6% → 8.0%**, a 13× move from a tail that never appears in mean or variance. This is the assumption most likely to break live. |
| **EM4** | **Cadence floor — weekly, not daily** | **≥1 trade per Mon–Fri week**, by construction, with idle weeks **uncorrelated** to any co-deployed leg. Duty cycle ≈20% minimum. **No trades/day floor applies** | `inactivity_max_idle_days: 5` + verified absence of a duration cap | The eval has **no time limit**, so speed is not required — a 21–48-day median pass is comfortably inside "no limit". What *is* required is never going a calendar week silent, on pain of **irreversible deletion**. The incumbent book's failure was clustering, not rate: 26.3% zero-trade weeks and 4 consecutive dead weeks at a duty cycle that already cleared this floor. **Correlated idleness is the failure mode this limb screens.** |
| **EM5** | **Session + slot legality** | Intraday-complete and flat by the envelope's **16:00 ET** default (inside Tradeify's 16:45 ET); long-only if Equity Index Product Group; micro-expressible; **and the order symbol unoccupied per third-leg S7** | E1/E4a/E5 + S7 + hedging rule | Tradability and slot legality. **S7 is imported, not restated** — it is a property of *the rail* (`flatten_first` / quantity-less `closeposition` keyed `account`+`instrument`), so it survives any venue change and binds identically at a successor firm. |

### 2.0a — **When** the screen is applied (binding, not stylistic)

**EM0–EM5 is applied to a candidate *class* or a *catalogue*, before any data is examined — never to a
scored candidate list afterward.** The screen consumes zero data and zero holdout: it is derived from
venue rules plus frozen simulation, so applying it early costs nothing and applying it late costs K.

Under [Avenue A **Route B**](../adr/2026-08-05-avenue-a-generate-confirm-route.md) this has an exact
address: **the screen is a G0 act.** `K_intrinsic` is the exploration catalogue size actually examined,
so pruning shape-dead cells *before* the G0 freeze removes them from K at no evidentiary cost, which
lowers the DSR floor the CONFIRM run must clear. The checklist's own rule — *"choosing among candidates
**after** G2 counts in K"* — applies to this screen with no exemption: **shape-screening a G2 candidate
list is a K charge, not a free filter**, and it is the same laundering shape as confirming an
unadjusted M > 1 budget, one stage earlier. Route A campaigns and non-Route-B tracks inherit the same
rule in its general form: **screen the class, not the winner.**

### 2.0b — **EM0: catalogue size** — the limb that fires before any cell is scored

**Added 2026-08-05 after measurement.** EM1–EM5 screen a *cell*. Nothing above screened the
*catalogue*, and the catalogue is the binding constraint.

| # | Limb | Threshold | Generated by | Why it binds |
|---|---|---|---|---|
| **EM0** | **Catalogue size** | **≤ 3 pre-registered cells.** K=4 closes the band. Treat **1–2** as the working budget; 3 only for a candidate expected to beat every result on record for the instrument | Route B C0 (`K_intrinsic` = catalogue size) ∘ [ADR 2026-08-04](../adr/2026-08-04-family-k-bank-disclosure-not-gate.md) (`K_eff` = `K_intrinsic`) ∘ ratified Cap 1.0 | The DSR floor is driven by catalogue size alone: **0.650 / 0.850 / 0.980 / 1.060** at K=1/2/3/4. Above the Cap, **no achievable Sharpe clears DSR** — so a catalogue of 4+ cells cannot produce an admissible result *no matter what it finds*. At K=3 the headroom is **0.020**, narrower than the gap between MNQ's best-ever construct (+0.835, Tradeify basis) and the Cap |

**EM0 is evaluated first and it dominates.** A 90-cell catalogue is 30× over; the same catalogue after
an EM1 prune (72 cells) is 24× over — **both equally dead, and the EM1 prune is irrelevant at that
scale.** Screening cells before screening the catalogue is wasted work.
Measurement: [`catalogue_k_wall_2026-08-05`](../../lab/analysis/c1/catalogue_k_wall_2026-08-05/RESULTS.md)
($0 · K=0). The wall is a **lower bound on severity** — `floor_at_k` is most-permissive across trade
frequencies, so a specific frequency's floor is higher, never lower.

⚠ **This is not new doctrine.** `ops/instruments/M2K.md` already states it for one instrument
(*"Do not spend this bank on a wide search. One pre-committed mechanism, `K_eff=1`"*); `DISC-CAMP-0`
demonstrated it (`k_dsr = 3177`, zero candidates reaching stage 4/5); and the 08-08 pre-triage reads
the DSR gate as *"AMBIGUOUS by zero exposure."* EM0 states the general property those three share:
**any catalogue large enough to exercise the DSR gate is automatically over Cap**, so zero exposure
is the expected state rather than an accident.

### 2.1 — Disclosure-only, explicitly **not** gates

| Item | Why it is not a gate |
|---|---|
| Per-day profit concentration (40% consistency) | A **soft** gate at every friendly firm: exceeding it delays a pass by extending required days; it cannot fail an account (envelope E2). It raises the effective target to `max($6,000, 2.5 × best day)` and therefore extends rope exposure — **annotate expected max-day share at registration**, do not screen on it. |
| Funded **$200** winning-day floor | Every archetype tested clears it several times over ($333–$1,046/winning day across the 0.49R–0.85R band). Non-binding at these edge levels. **Re-check at the candidate's own realized size** before any funded claim — do not assume this transfers. |
| Funded **30-micro** start tier | Funded-phase only, and the venue is currently de-scoped as a deployment target. It is what killed the Striker book (104.7% of net from >40-micro days). Screen a candidate on it **only** if a successor venue publishes an equivalent ladder. |
| Win rate | Near-irrelevant across the band — a 40%-win / 2.7R construct (edge 0.48R) passes 99.1% with a 21-day median. Screening on win rate screens on nothing. |

### 2.2 — What the venue does **not** constrain

Recorded because each was, at some point, treated as a requirement in this estate: **speed / trades-per-day**
· holding period · win rate · direction (subject to EM5's long-only Equity Index limb) · instrument class
within venue-tradable products · mechanism exoticism. **US Treasuries are untradable at this firm** — that
is a product restriction, not a mechanism constraint.

### 2.3 — Scope limits inherited verbatim from the source studies

1. **k=1 means genuinely independent entries.** These bounds describe a *redesigned* construct; they are not a re-measurement of any incumbent.
2. **"No time limit" ≠ "no cadence floor."** EM4 is the binding minimum-frequency constraint and is unaffected by the duration finding.
3. **The frontier is tolerance-dependent** (≤1% failure). At a looser tolerance every EM2 figure rises.
4. **No serial correlation is modelled.** Real strategies cluster losses across days; direction of error is **optimistic**.
5. **Passing this screen is not admissibility.** Harvest Req 1–5, the DSR floor at the family's disclosed `K_banked`, the cost-law screen, and the regime-robustness gate are **independent bars** and none is weakened here.

---

## §3 — How this composes with the two ratified screens

Three screens, three different questions. **A candidate must clear all three that apply.**

| Screen | Asks | Status |
|---|---|---|
| [`prop_envelope_default.md`](../../ops/prop_envelope_default.md) **E1–E7** | *Is it tradable at the four friendly firms at all?* | RATIFIED 2026-07-13 — **unchanged** |
| [`third-leg-target-spec.md`](2026-07-27-third-leg-target-spec.md) **S1–S7** | *Can it occupy a same-account slot beside the existing c1 book?* | RATIFIED 2026-07-27 — **unchanged**; applies only when a same-account slot is sought |
| **This spec, EM0–EM5** | *Does its mechanism shape survive the eval geometry?* | `RATIFIED 2026-08-06` |
| [`avenue_a_generate_confirm.md`](../methodology/avenue_a_generate_confirm.md) **Route B** | *Is the evidence for it laundered?* — a **process**, not a shape screen | `Accepted` 2026-08-05 — composes at **G0** per §2.0a |

Deliberate overlaps, and which owner wins: **EM5 ⊃ E1/E5 + S4/S7** — this spec restates none of them and
defers to their owners on any conflict. **EM2/EM3 have no counterpart** in either — the envelope prices
*tradability*, this screen prices *survival*. **EM4 vs E-none/S-none:** the idle clock reached the estate
as a c1-book operational problem, never as a candidate screen; EM4 is where it becomes one.
**Route B is orthogonal to all three** — it governs *how evidence is earned*, not *what shape is legal*;
a Route B campaign can be impeccable and still explore a shape-dead catalogue, which is precisely the
waste §2.0a exists to prevent.

### 3a — Cost authority (open fracture, deliberately not resolved here)

**EM1 defines no cost formula.** It consumes whichever authority the estate names, and it must not
become a third one. Two currently overlap and the conflict is **on the 08-08 board as G3**:
`cost_geometry_pregate.py` (`cost_R = RT / (stop_atr · median ATR15m)`, PASS < 0.05R — still named by
`operational_rules.md` Rule 10) versus [`strategy_harvest.md`](../methodology/strategy_harvest.md)
**Requirement 5** (`RT_pts / OR_range`, 4× hurdle), which declares itself *"the sole authority"* and is
what every cost-sensitive rejection since 2026-07-21 actually used. **EM1 points at Requirement 5**
because this screen composes with harvest Req 1–5 — but if 08-08 rules the other way, or keeps both
with a stated scope split, **EM1 re-points in the same change and does not fork.**
[Pre-triage](../notes/2026-08-05-0808-pretriage-g3-g8-mechanical-findings.md) §G3.

### 3b — Portability: EM1–EM3 survive the F3 fork

All four FRIENDLY firms carry a **3.0% rope at the $100K band** (`core/firm_rules.py`, verified
2026-08-05), so EM2's frontier and EM1's inversion floor are properties of the **prop archetype**, not
of Tradeify. Only **EM4** varies materially (idle: Tradeify 5 · Bulenox 5 · MFFU 5 · **BluSky 22**), and
**EM5** is rail-shaped (S7) rather than venue-shaped.

**Consequence, and it is the sharpest thing in this spec:** [Q-VENUEGEO-1 DP3](../../lab/analysis/c1/venuegeo_dp3_bustceiling_2026-08-05/RESULTS.md)
measures the **bare** incumbent book at ~97.5% bust (Bulenox/MFFU) and 15.48% (BluSky) — *no successor
firm is viable unmitigated* — and its instrumented figures (Bulenox/BluSky tied at 2.96%, MFFU 3.54%)
all **price in a token trade whose legality DP2 found unresolved at two of the three firms**. A
construct that satisfies **EM4 by construction** needs no token trade, and therefore carries neither
that ~2.96%-at-a-3.0%-ceiling margin nor that legal-risk surface. **DP3 did not measure this class.**
⚠ One input is disputed: BluSky's encoded `cost_per_side_usd: 0.95` contradicts its published
$0.50/side and is flagged for operator correction. EM1's $0.95 screen value is **MFFU-set** and holds
regardless.

---

## §4 — Falsifier

**H:** *these six limbs are the minimum sufficient mechanism-shape screen for the Tradeify Select 100K
evaluation — a construct clearing all six passes the eval geometry at ≤1% bust without further
mechanism-shape conditions, and a construct failing any one does not.*

| # | Trigger | Threshold | Action |
|---|---|---|---|
| F-A | **The screen is not sufficient.** A construct clears EM0–EM5 on frozen inputs and its own honest-clock re-MC returns a bust above the frontier | measured bust **> 1.0%** at the declared EM2 size, on the intraday clock | A limb is missing. Author the missing limb by superseding spec; do not patch in place |
| F-B | **A limb is not necessary.** A construct fails exactly one limb and still passes at ≤1% bust across both regime halves | any single limb, both halves | That limb is demoted to §2.1 disclosure |
| F-C | **The geometry moves.** Any §1 constant changes at primary source | `max_dd_pct` · `profit_target_pct` · `consistency_rule_pct` · `inactivity_max_idle_days` · `micro_contract_cap` · **duration cap appearing** | Re-derive the affected limb; this is the 90-day venue re-verify hook. ⚠ **The de-scope ADR's §4 T4 pin list does not include the duration cap** (it names winning-day threshold · funded start tier · idle days · Flex payout basis). Pin 6 was only verified 2026-08-04 and is now load-bearing for **EM4** — a duration cap appearing would void EM4's "speed is not required" ground without firing T4 as written. **Recommend 08-08 add it to T4** |
| F-D | **The intraday under-statement is material.** The Phase-4 both-halves intraday re-run shows the EOD-clock frontier over-states admissible size | EM2 frontier moves **> 20%** on the honest clock | EM2 thresholds re-issued by superseding spec |
| F-E | **Successor-venue non-portability.** A registered successor venue's rules generate a limb this screen lacks, or void one it has | any F3 venue registration | Fork the spec per venue; do not silently generalize |

**Revert action:** author a superseding spec. **Never edit §2 in place** (Known Trap #12).
**Check schedule:** F-C at the 2026-08-08 checkpoint and each 90-day venue re-verify · F-D at the Phase-4 run's completion · F-A/F-B on each candidate scored · F-E on any F3 ruling.

---

## §5 — Forbidden moves

- **Reading a screen pass as an admission.** EM0–EM5 says a construct *survives the eval geometry*. It says nothing about durable edge. Harvest Req 1–5, DSR-at-K, cost-law, and the regime gate are independent and unweakened (§2.3.5). Genuinely tempting because the screen is quantitative and feels dispositive.
- **Applying the screen to a scored candidate list instead of to the catalogue.** Under Route B this means shape-screening G2 output; under any other track it means picking the shape-clear survivor after measurement. **Both are priced in K exactly like any other post-hoc choice** (§2.0a). This is the most likely way the screen gets misused, because it is the *convenient* moment to reach for it — the candidates are already in front of you, and the screen's venue-derived provenance makes the filtering feel like a rule rather than a choice. It is a choice.
- **Letting EM1 grow its own cost formula.** §3a names Requirement 5 as the authority precisely so this screen does not become the third entry in an already-fractured stack. If the authority moves at 08-08, re-point EM1; never fork it.
- **Quoting $275 as a constant.** EM2 is **edge-indexed**. $275 is the 0.65R cell. Using it against a 0.49R candidate over-sizes by 10%.
- **Re-introducing a trades-per-day floor.** Retired on a verified venue fact (Pin 6, three primary sources). A future search that wants speed must justify it as a *preference* with a stated reason, not inherit it as a requirement.
- **Softening EM3's independence limb to admit a pyramided candidate.** The arithmetic is an identity, not a threshold: correlated adds *are* the k=1 row at a worse r. A candidate needing this softened needs a different construct.
- **Softening S7 via EM5.** S7's own ADR forbids it explicitly; importing it here creates no new softening route.
- **Treating this spec as reopening Tradeify as a deployment target.** The venue is de-scoped for the two Striker legs; the 08-04 Addendum permits *research*, and this is research. Anything clearing this screen still needs Stage-0 pre-registration, a `K_intrinsic` bound, cost-law clearance, and a **separate operator GO**.
- **Applying the screen to a successor venue unchanged.** F-E exists precisely because Bulenox / MFFU / BluSky publish different ropes, consistency semantics, and idle clocks — BluSky's own idle rule was mis-encoded by 10× until 2026-08-05.
- **Re-opening a §7 row after the 2026-08-06 ruling without a superseding spec.** §7 dispositions are locked; a changed disposition needs a new operator ruling, not an informal re-read of the pre-ratification recommendations.

---

## §6 — Gate (binary, per candidate)

Score a candidate as **PASS / FAIL / UNSCREENABLE** per limb, then:

- **`SHAPE-CLEAR`** — all six PASS. Routes to harvest Req 1–5 and Stage-0 pre-registration. **Admits nothing.**
- **`SHAPE-DEAD`** — any limb FAIL. Rejected at intake, **zero cost, before any data is pulled or K is spent**. Record which limb, in the candidate's own closure line.
- **`SHAPE-UNSCREENABLE`** — a limb cannot be evaluated from available evidence. **Never patched to PASS** (harvest Req 4). Either the evidence is obtained or the candidate stays unscreened.

A candidate's screen result is recorded as a six-character verdict string, EM0 first (e.g. `PPPPFP` = EM4 fail) so
the failing limb is never lost to a summary word.

---

## §7 — Supersession candidates — **RULED 2026-08-06** (row-by-row; dispositions locked)

Every row is a claim this screen may displace. **Disposition column is now the operator ruling**
(ratification §8 / JA 2026-08-06), locking the pre-ratification recommendations as filed.
Rows are ordered by how load-bearing the claim still is.

| # | Claim / artifact | Where it lives | Why it is a candidate | Disposition (RULED 2026-08-06) |
|---|---|---|---|---|
| 1 | **T2 — "3–8 independent trades/day"** | [MNQBASE-1 §2.1](../briefs/rnd-pipeline/MNQBASE-1-tradeify-shaped-base-construct-harvest-scoping.md), and its restatement at §162 | **Superseded outright.** Never a venue rule — a speed preference inherited from solving for a 3–12 day pass. Already contradicted by the brief's own closure §5.1 and by MNQ ledger **N13** | **RETIRE** reuse. Replaced by **EM4** (weekly, uncorrelated). Brief closed — retire claim reuse via reader-intercept, not delete the artifact |
| 2 | **T6 — "≥1 trade / 5 calendar days … trivially satisfied by T2"** | MNQBASE-1 §2.1 | **The rider inverts.** With T2 gone, the idle clock is no longer trivially satisfied — it becomes the **binding** cadence limb, and its enforcement is irreversible deletion | **RETIRE** the "trivial" rider; **EM4** is the binding cadence limb |
| 3 | **T7 — "risk ≤ $275/trade"** | MNQBASE-1 §2.1 | Not wrong, **under-specified**: $275 is the 0.65R cell of an edge-indexed frontier. Applied flat, it over-sizes weak-edge candidates and under-sizes strong ones | **SUPERSEDE** by **EM2** (edge-indexed $250/$275/$325) |
| 4 | **T1 / T3 / T4 / T5** | MNQBASE-1 §2.1 | Correct and unchanged — carried into EM1 / EM3 / EM3 / EM5 | **CARRY** FORWARD, no retirement |
| 5 | **Q-CADENCE-1's ≥90%-of-weeks firing floor** | [prereg §4](../briefs/pre-registration/2026-08-03-c1-cadence-leg-preregistration.md), `FROZEN` | Derived to answer *"can one leg rescue a co-idle **pair**"* — a much harder bar than *"does a single construct fire weekly."* Already **moot in its deployment limb** per the de-scope ADR §6 | **NARROW** — pair-rescue only; must not be quoted as a general candidate requirement. No board rewrite beyond this explicit narrowing (STATE already carries the reusable-gate line) |
| 6 | **B1's fast target rows** ($2,000 / $1,200 / $750 per active day for a 3 / 5 / 8-day pass) | [inverse-requirements §1 B1](../../lab/analysis/c1/eval_inverse_requirements_2026-08-03/RESULTS.md) | Arithmetically true, but they encode the retired speed preference. Quoting them invites re-deriving a trades/day floor | **LABEL** non-binding-on-speed (do not delete); pointer here |
| 7 | **`2026-08-02-tradeify-activity-rule-disposition-spec.md`** (status `OPEN`) | [docs/spec](2026-08-02-tradeify-activity-rule-disposition-spec.md) | Its option set exists to solve the **incumbent pair's** cadence deficit. For a construct built to EM4, the question does not arise — the mitigation is designed in, not bolted on | **DO NOT CLOSE** on this spec's authority. Spec remains `OPEN` for incumbent-pair cadence; F2 closed via [`S1`](../adr/2026-08-07-loop-s1-environment-ratification.md) (not a close trigger here) |
| 8 | **"Every c1 pass-rate figure presumes an undelivered cadence mitigation"** | [de-scope ADR §1](../adr/2026-08-04-tradeify-venue-descope-eval-included.md) item 1 | Still true of the **incumbent book**. For a construct meeting EM4, the presumption is discharged by construction | **NO CHANGE** — ADR statement about incumbents stays as filed |
| 9 | **Book-composition §0's unflagged pin practice** | [rule-pin note](../notes/2026-07-24-tradeify-rulepin-verification.md) Pins 4/6 | Two instances now of *unflagged ≠ verified*. This spec's §0 states a verification for every constant | **NO CHANGE** — lesson already recorded; no artifact edit |

**Two things this list deliberately does not touch:** the **envelope E1–E7** and the **third-leg S1–S7**
are ratified, non-overlapping, and composed with (§3) — not superseded. Any proposal to fold them into
this spec is a **different** decision needing its own ADR.

---

## §8 — Ratification

```
RATIFICATION:    Eval mechanism-shape screen (EM0-EM5) adopted as the standing
                 mechanism-shape screen for Tradeify Select 100K eval geometry.
                 Screening standard only - admits nothing, arms nothing, spends
                 nothing. Section 7 dispositions ruled separately, row by row.

DATE / INITIALS: 2026-08-06 / JA
SECTION 7 RULED: rows 1 RETIRE  2 RETIRE  3 SUPERSEDE  4 CARRY  5 NARROW
                         6 LABEL  7 DO-NOT-CLOSE  8 NO-CHANGE  9 NO-CHANGE
```

**Change control:** §2 thresholds change only by a superseding spec or by a §4 trigger firing.
§1 geometry may be re-verified and corrected without a superseding spec (it is a measurement of the
venue, not a decision) — but a change there fires **F-C**.

---

## §10 — Audit hooks (runnable)

```bash
# 1. Every geometry constant in section 1 is still what firm_rules.py says.
python -c "
import sys; sys.path.insert(0,'core')
from firm_rules import FIRM_RULES
t = FIRM_RULES['Tradeify_Select_100K']
exp = dict(max_dd_pct=3.0, profit_target_pct=6.0, min_trading_days=3,
           consistency_rule_pct=40.0, inactivity_max_idle_days=5,
           micro_contract_cap=80, daily_loss_pct=None, weekend_holds=False,
           cost_per_side_usd=0.91, dd_type='trailing_locking')
bad = {k:(t.get(k),v) for k,v in exp.items() if t.get(k)!=v}
assert not bad, f'section 1 geometry drifted: {bad} -- fires F-C'
assert t['dd_lock_offset_usd'] >= 1e6, 'eval lock became reachable -- re-derive EM2'
print('section 1 geometry OK')
"
# Expected: 'section 1 geometry OK', exit 0

# 2. The EM2 frontier cells trace to the slow-archetype study, not to this spec.
rg -n '\$250|\$275|\$325' lab/analysis/c1/eval_slow_archetype_2026-08-04/RESULTS.md
# Expected: the section 4.2 frontier table (3 rows: 0.49R / 0.65R / 0.85R)

# 3. The 0.40R inversion floor and the stop-gap tail are still as cited.
rg -n '0\.40R|0\.139R' lab/analysis/c1/eval_inverse_requirements_2026-08-03/RESULTS.md | head
rg -n '8\.0%|0\.6%' lab/analysis/c1/eval_inverse_requirements_2026-08-03/RESULTS.md | head

# 4. S7 is imported, not restated -- this spec must not carry its own occupancy threshold.
rg -c 'MNQ1!|MYM1!|flatten_first' docs/spec/2026-08-05-eval-mechanism-shape-screen.md
# Expected: 2 -- the EM5 parenthetical + THIS HOOK LINE itself (Trap M-AHF: the hook
# matches its own text; corrected after execution returned 2 on a spec that is correct).
# The property being asserted is "no current-occupancy TABLE"; a count of 3+ means one
# crept in and S7's owner has been duplicated.

# 5. The idle rule's enforcement is still deletion (this is what makes EM4 a gate).
rg -n 'deleted|deletion|no reinstatement' docs/notes/rail_build/TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md | head

# 6. No trades-per-day floor has crept back into an active screen.
rg -n '3.{0,3}8 (independent )?trades|trades/day' docs/spec/ ops/prop_envelope_default.md
# Expected: exactly 4 hits, ALL in this file, none anywhere else in docs/spec/ or the
# envelope -- EM4 ("No trades/day floor applies"), section 7 rows 1 and 6 (retirement
# records), and this hook line (Trap M-AHF self-match). A hit in any OTHER file means a
# trades-per-day floor has crept back into an active screen.

# 7. This spec changed nothing operational.
git diff --stat HEAD -- core/ ops/ '*.pine'
# Expected: empty

# 8. The three screens are still distinct artifacts (section 3 composition intact).
ls ops/prop_envelope_default.md docs/spec/2026-07-27-third-leg-target-spec.md \
   docs/spec/2026-08-05-eval-mechanism-shape-screen.md

# 9. Route B is still Accepted -- section 2.0a's G0 address depends on it.
rg -n '^\*\*Status:\*\*' docs/adr/2026-08-05-avenue-a-generate-confirm-route.md
# Expected: Accepted. If it reverts, section 2.0a's Route B paragraph is a dead pointer and
# the general form ("screen the class, not the winner") is what survives.

# 10. EM1 still points at ONE cost authority and defines no formula of its own (section 3a).
rg -n 'cost_R|RT_pts|0\.05R' docs/spec/2026-08-05-eval-mechanism-shape-screen.md
# Expected: exactly 3 LINES, all accounted for -- the two section 3a lines quoting each side of
# the G3 fracture, plus this hook line (Trap M-AHF self-match; corrected after execution
# returned 3 on a spec that is correct). A match anywhere in section 2 means EM1 has started
# carrying its own arithmetic and has become the third entry in the fracture.

# 11. The four-firm rope portability claim (section 3b) is still true at HEAD.
python -c "
import sys; sys.path.insert(0,'core')
from firm_rules import FIRM_RULES as F
tiers = ['Tradeify_Select_100K','Bulenox_100K','MFFU_Rapid_100K','BluSky_Premium_100K']
ropes = {k: F[k]['max_dd_pct'] for k in tiers}
assert set(ropes.values()) == {3.0}, f'rope divergence -- EM1-EM3 portability claim broken: {ropes}'
print('four-firm 3.0% rope OK', {k: F[k]['inactivity_max_idle_days'] for k in tiers})
"
# Expected: OK + the idle spread {5, 5, 5, 22} that section 3b calls EM4's venue-variable limb
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python "$HOME/.claude/skills/brief-authoring/scripts/check_brief.py" \
  docs/spec/2026-08-05-eval-mechanism-shape-screen.md --type adr
python scripts/check_status_consistency.py
python scripts/check_falsifier_reachability.py

# Section 0 anchors still current
for f in core/firm_rules.py ops/prop_envelope_default.md \
         docs/spec/2026-07-27-third-leg-target-spec.md \
         lab/analysis/c1/eval_inverse_requirements_2026-08-03/RESULTS.md \
         lab/analysis/c1/eval_slow_archetype_2026-08-04/RESULTS.md \
         docs/notes/rail_build/TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md; do
  git log -1 --format="%h %cs $f" -- "$f"; done
# Expected: 8ec740d / cd8b617 / 2345095 / cdfd2f8 / cad464f / 10db7b9

# Every section 7 supersession target exists and is quoted correctly
rg -n 'T2 \|' docs/briefs/rnd-pipeline/MNQBASE-1-tradeify-shaped-base-construct-harvest-scoping.md
rg -n 'trivially satisfied by T2' docs/briefs/rnd-pipeline/MNQBASE-1-tradeify-shaped-base-construct-harvest-scoping.md
rg -n '≥90%|90% of weeks' docs/briefs/pre-registration/2026-08-03-c1-cadence-leg-preregistration.md | head
rg -n '^\*\*Status:\*\*' docs/spec/2026-08-02-tradeify-activity-rule-disposition-spec.md
```
