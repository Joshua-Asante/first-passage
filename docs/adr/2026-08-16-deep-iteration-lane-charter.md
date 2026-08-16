# ADR 2026-08-16 — Deep-iteration lane charter (mechanism-family refinement at declared K, survivor-measured admission)

**Status:** `Proposed` — operator must ratify before anything below binds. Drafted at operator direction ("proceed" on the 2026-08-16 bottleneck diagnostic); authoring is not ratification.
**Tier:** full — limb 4 of the [ceremony-tiering ADR](2026-08-08-adr-ceremony-tiering.md) fires (creates doctrine: a new candidate-producing channel with its own falsifier).
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Decision date:** 2026-08-16
**Date note:** drafting date — Status `Proposed`; the ratification date lands in the change history on operator GO
**Authors:** Joshua (commission) + Claude Code (drafter)
**Supersedes:** nothing. `CAP` / `DSR_MIN` / `axis_screen.py` constants untouched; the blind channel (D-K1/D-K2/D-K3), MSL, harvest intake, and every existing admission predicate stand byte-unedited.
**Related:** [no-counterparty channel](2026-08-15-no-counterparty-statistical-sourcing-channel.md) (sibling charter; this lane mirrors its structure) · [family-K disclosure](2026-08-04-family-k-bank-disclosure-not-gate.md) · [W4 dormancy](2026-08-07-w4-minimal-gate-set-dormancy.md) · [Q-CAPBAND-1 closure](../briefs/closures/Q-CAPBAND-1-closure-resolved.md) · [M-19](../methodology/lessons/methodology_lessons.md) · [MSL slate-2 design box](2026-08-13-msl-slate-2-design-box.md)
**Layer:** research governance — no live-risk surface; no locked parameter; no allocation; no arming.

---

## §0 — Rule-0 reads (verified this session @ `c89f261`, 2026-08-16)

| Source | Anchor | Supplies |
|---|---|---|
| [`lab/research_utils/axis_screen.py`](../../lab/research_utils/axis_screen.py) | executed this session | `CAP=1.0`, `DSR_MIN=0.95`, `POWER_MIN=0.5`, `YEARS=6.5`; `floor_at_k(k, years=6.5, …)`. Computed directly: floor_at_k(3)=0.980 · (4)=1.060 · (10)=1.265 · (33)=1.475 · (100)=1.640 · (441)=1.830; at years=3.25: (10)=1.790 · (33)=2.090 |
| [M-19](../methodology/lessons/methodology_lessons.md) | lines 879–894, read this session | The floor is K-governed, not n-governed; K-sweep crossings (≤ Aegis-quality: K ≤ 441; ≤ Guardian-quality: K ≤ 33); "low-K, mechanism-first axes (a handful of pre-specified hypotheses) can pull the floor below plausible edge quality"; forbidden move: "a larger search raises the floor toward the overfit-suspect zone (SR > 2)" |
| [Q-CAPBAND-1 closure](../briefs/closures/Q-CAPBAND-1-closure-resolved.md) | read this session | Cap 1.0 evidence-ratified **on the named axes only** (D6, D2-low). Stop rule, two distinct clauses: (1) re-opening the Cap band needs a NEW axis with floor in [1.0, 2.0] clearing the four non-Cap gates; (2) "any future proposal to move Cap toward 2.0 must additionally answer the overfit-suspect zone (SR > 2) forbidden move" — this charter moves no Cap, and answers (2) anyway via §2.2(ii) |
| [Blind-channel ADR](2026-08-15-no-counterparty-statistical-sourcing-channel.md) | read this session (incl. N=3 + empty-naming addenda) | D-K1 predicate form (`floor_at_k(K) ≤ CAP`); D-K3: "Widening it requires a superseding ADR that re-derives the Cap, not a per-run exception"; frozen split discipline ("computes only on the confirm partition"); "A train/confirm split does not rescue a wide mine… Splitting is a bias control, not a K control"; N=3 addendum disposition (d) + empty-naming "Stop generating this session" — engaged in §1 below |
| [Family-K ADR](2026-08-04-family-k-bank-disclosure-not-gate.md) | read this session | K_eff = K_intrinsic; a grid pays in full; sequential single-hypothesis K disclosed but unpriced; operator header: "I also don't want to limit the discovery on any instrument. K=3 is an unnecessary requirement" |
| [W4 dormancy ADR](2026-08-07-w4-minimal-gate-set-dormancy.md) | read this session (incl. 08-15 R3/R5/R6 addendum) | SPA/StepM + PBO/CPCV dormant with named re-arm: campaign prereg names thresholds AND operator GO dated after 2026-08-07 |
| [Harvest-intake ADR](2026-07-15-external-mechanism-harvest-intake.md) | read this session | §4 limb 2 (fundability-transfer) now `Accepted`, pin `no`, count 0/2 post-mark — boundary with this lane defined in §2.7 so kills never double-count |
| [Decompound re-MC HOLD](2026-06-07-decompound-remc-hold.md) + [allocation-refresh-2 addendum](2026-05-23-allocation-refresh-2.md) | read via 2026-08-16 diagnostic, paths re-verified | The CFD-era iterated product fails the H1 half: 13.84% bust / p99 8.00% engine-correct (7.76% pre-2026-07-06 fix — [bust-day-maxdd ADR](2026-07-06-bust-day-maxdd-inclusion.md)) vs bust<1%∧p99<5% — the demonstrated failure mode of un-controlled iteration, priced into §2.4 |
| [MSL slate-2 design box](2026-08-13-msl-slate-2-design-box.md) | read this session | The surviving candidate geometry (rr ∈ [2,3] · WR 0.30–0.42 · R at the bust-≤3.0% frontier · hard stop · k=1 · no pyramiding) this lane targets |

**Amendment-first / dedup (executed this session):**

```
$ grep -rlniE "deep.iteration|iteration lane|lane deep|deep-search" docs/ lab/CATALOG.md
docs/briefs/rnd-pipeline/WSTRUCT-M2K-1-weekly-structure-component-confirm-scoping.md
docs/notes/audits/programme-audit/2026-07-21-index-futures-intraday-ohlcv-domain-audit.md
docs/rejected_candidates.md
```

All three hits are literature-search contexts (WSTRUCT archetype deep-search; 07-21 domain-audit external corroboration; Stocks-in-Play registry entry) — **no prior deep-iteration-lane proposal exists**; nothing is re-derived. The only adjacent prior rejection is ADR 2026-08-04 §3's "Keep the ratchet, raise the Cap" (rejects Cap-raising as laundering a mis-specified K) — this charter raises no Cap; see §2.2.

---

## §1 — Context

**Decision driver (one sentence):** the estate's generation record — no generated candidate admitted since ORB-MNQ-1 on 2026-07-16 (31 days at drafting, by date arithmetic); 8 consecutive zero-yield closes 2026-08-08→08-12 (STATE.md decision index) continuing through the MSL slate deaths; the 2026-08-15 wall-scope audit's ruling that "MSL's dryness is a *generation-input* problem (nothing found, not something found and wrongly rejected)" — combined with its own arithmetic (M-19: the floor is K-governed, and "low-K, mechanism-first axes (a handful of pre-specified hypotheses) can pull the floor below plausible edge quality") leaves exactly one unchartered corner: bounded-depth iteration inside one pre-registered mechanism family, survivor held to the K-indexed DSR floor on an untouched confirm — the disciplined form of the process that produced the four locked CFD-era strategies. (Commissioned by operator direction on the 2026-08-16 session diagnostic, which is operator-held and not in-tree; every load-bearing figure above is cited to committed surfaces, not to it.)

Every current channel is a **one-shot** channel: K ≤ 3 at open (blind D-K1; EM0 catalogue cap; S6 refusal), re-proposal bars forbid θ-retune, and campaigns are one explore + one reserved confirm. The CFD-era book was built the opposite way — tens of revisions per strategy — un-deflated, and its product demonstrably regime-fragile (§0 row 8). Neither corner is adequate: the one-shot corner has produced zero deployable candidates from generation; the un-controlled corner produced fragile survivors. This charter is the priced middle.

**Third-door engagement (stated plainly, eyes-open).** This charter is a candidate-producing channel drafted one day after two operator elections counsel against exactly this class of act absent independent grounds: the blind channel's N=3 addendum, disposition (d) — "It is **not** a license to open a third sourcing channel (§3: if this channel also falsifies, the fallback is the source-class post-mortem, not a third door)" — and the same-day empty-naming addendum's "**Stop generating this session.**" Strictly, neither letter is violated: the blind channel has not falsified (N sits 1/3; §4 unread), and the bar is on *dryness-as-authority*, while this charter's ground is the iteration-depth gap (no existing channel can host K > 3 inside one family — a structural absence, not a dryness reading). But the adjacency is real and is not soft-pedaled: **the default disposition is to HOLD this charter until the blind channel's 2026-11-08 §4 reading**; ratifying it earlier is an explicit overriding election the operator makes against that default, on the independent-grounds argument above — not a routine GO.

---

## §2 — Decision (Proposed)

Charter a **deep-iteration lane** (`--lane deep`) with the following properties, all frozen per-campaign at a full pre-registration before any scoring:

1. **One mechanism family per campaign.** The campaign pre-registration names one mechanism family (entry concept + instrument + timeframe + session), targeted inside the slate-2 design-box geometry on **non-index CME micros first** (no index raised bar binds there; the `instrument_profiles.py cell` consult is mandatory and must print no BINDING BAR). Families already in `docs/rejected_candidates.md` must clear their own re-proposal bars *before* the prereg freezes — the lane is never a θ-retune cover (§5). The prereg must additionally attest the family is **not under a standing operator pause or election** recorded outside the registry — currently the dense-1m OHLCV temporal-selectivity / entry-geometry pause (Branch A, U0 KEEP re-affirmed 2026-08-15) and the CON-5 θ-parameterised entry-geometry pause. **Channel-origin rule:** an externally-published family enters the lane only after clearing harvest intake — its intake-stage kills count on limb 2 there; the lane hosts internally-generated or intake-cleared families only.
2. **Declared K, hard-capped by three binding conjuncts.** The prereg declares the full variant budget K (every variant available to be chosen counts — D-K1's "the wider exploration is the K" imported verbatim). A lane prereg is **refused at freeze** unless all three hold:
   - **(i) `K ≤ 33`** — M-19's Guardian-quality crossing, a hard literal. This, not the floor alone, is what confines the lane to the tens corner: `floor_at_k(K, confirm_years) ≤ 2.0` by itself would admit K ≈ 2000 on a 6.5-year confirm (floor_at_k(441)=1.830, floor_at_k(2000)=2.000 — computed this session), i.e. wide mining through the long-confirm back door.
   - **(ii) `floor_at_k(K, confirm_years) ≤ 2.0`** — the M-19 overfit-suspect zone (SR > 2) stays unreachable; this is the conjunct that bites when the confirm is short (K=33 on a 3.25-year confirm → floor 2.090 → refused).
   - **(iii) power ≥ `POWER_MIN` (0.50), binding** — Clause-N-style pass probability at the frozen confirm length against the campaign's **design-target edge, named a priori in the prereg** (Gaussian approx., se ≈ 1/√years, method stated in the prereg). A prereg whose own target edge cannot clear its own floor at ≥ 0.50 power is refused, not disclosed-and-waved-through. Worked example at the defaults: target 1.83, K=33, 6.5-year confirm → floor 1.475, power ≈ 0.82 → admissible; target at-the-bar → power 0.50 → boundary-admissible and the prereg must say so.

   **This is not a Cap change:** `CAP = 1.0` remains the reachability prior for every one-shot channel; this lane replaces the *prior* with a *measured demand* — the survivor must itself clear `floor_at_k(K, confirm_years)` on data the search never touched. The K-cap addendum's rationale (refuse expensive deaths at the cheapest possible moment) is traded against deliberately here: the lane buys potentially-expensive confirm-stage deaths, bounded by §4's two-campaign falsification budget — that trade is the charter's price, stated, not hidden.
3. **Frozen train/confirm partition, confirm ≥ the years the floor was computed at.** Named in the prereg before any variant is scored. All iteration feedback reads **train only**; the confirm partition is read **once**, on the single pre-nominated survivor (nomination rule frozen at prereg: best-on-train under a stated statistic — selection is in-sample only). Per-variant confirm results are never computed. A 6.5-year confirm in practice means parent-era Databento history on the train side (cost dry-run mandatory before any pull) with the native panel era reserved for confirm, or an explicitly shorter confirm with the floor honestly recomputed at that length.
4. **Regime-fragility control (the CFD lesson, priced).** The prereg freezes an own-series half-split on the confirm partition — split point and per-half floor named before the read; deliberately **not** named "regime-robustness gate" (that gate is scoped to dd_protection-class sweeps; mirror of the blind channel's forbidden move 5). A survivor whose confirm passes pooled but fails a half is `FALSIFIED-FRAGILE`, not admissible — this is the control whose absence produced the locked book's H1 13.84%.
5. **Everything downstream is unchanged.** Cost-law ≥ 4× at the venue-legal expression (arithmetic run at family selection, before the search opens); N-SURV (intraday-honest bust ≤ 3.0% ∧ P(pass) ≥ 50%) byte-unedited; native-TV anchor before admission; lifecycle intake at SURVIVAL-ONLY / WATCH-1; M1 + per-session GO for anything live. The lane supplies candidates *to the existing gauntlet*; it admits nothing by itself.
6. **Multi-shot correction re-armed.** At K in the tens the frozen split is no longer the "explicit, weaker, disclosed substitute" it is at K ≤ 3: the campaign prereg must name SPA/StepM thresholds — and, if cross-validated selection is used, PBO/CPCV thresholds **plus the time-series-leakage argument W4's PBO row requires** — discharging W4's re-arm condition with the operator GO that ratifies the prereg (GO dated after 2026-08-07). The `universe_gate` orchestrator re-arms only when SPA + DSR + PBO are all re-armed for the family (W4's own all-three condition).
7. **Counter hygiene.** Lane campaigns are not blind-channel constructs (N=3 count untouched) and not MSL cards (E1/WHO untouched). The harvest boundary is the §2.1 channel-origin rule: externally-published families clear harvest intake first (their intake-stage kills count on limb 2 **there** — this lane is never a route around the R10 limb the operator armed 2026-08-15); only internally-generated or intake-cleared families are lane-resident, and their lane kills are recorded on this ADR with dates. A candidate may live in exactly one channel; double-homing to shop for the softest counter is forbidden (§5).

**Effective:** nothing is effective at `Proposed`. On operator GO: §7 step 1 (first campaign prereg) is the only immediately licensed act.

---

## §3 — Alternatives considered

| Alternative | Why not elected (draft reasoning — operator may overrule) |
|---|---|
| **Status quo (K ≤ 3 one-shot corner only)** | The measured record: no generated admission since 2026-07-16; 8 consecutive zero-yield closes 2026-08-08→08-12 (STATE.md) continuing through the MSL slate deaths; 4/4 MSL G0 freezes dead at first-expression explore (MSL program plan §6). The corner is narrow, not sterile — but its yield rate against the 2026-10-07/11-08 clocks is the problem being solved. |
| **Raise `CAP` globally** | Rejected by ADR 2026-08-04 §3 reasoning (laundering a mis-specified K) and needlessly wide: it would loosen every one-shot channel to fix a depth problem. This charter touches no constant. |
| **Wide mining (K in the hundreds-plus)** | Refused by §2.2(i) (`K ≤ 33`) regardless of confirm length — the floor-only form would admit it through the long-confirm back door (floor_at_k(2000, 6.5y)=2.000). Substantively: floor_at_k(441)=1.830 is a coin-flip even for a true-1.83 edge, and ≥80% power needs true SR ≈ 2.2 — inside the overfit-suspect zone. M-19's crossing table says the powered corner is tens, not hundreds. |
| **Hold until the blind channel's 2026-11-08 §4 reading** | Live alternative (§1 third-door engagement). Cost: the lane cannot produce evidence before the four-firms §4 reading if chartering waits; the MSL Rung B clock (~2026-10-07) passes unused. Named for the operator rather than argued away. |
| **Iterate inside existing channels via sequential K=1 campaigns** | Already legal and unpriced (family-K ADR §6) — but it iterates at mechanism-class level with no shared family learning, which is precisely the shape that produced the zero-yield streak; and the 08-15 K-cap addendum bars it channel-locally as ceiling-evasion where it would matter. |

---

## §4 — Falsifier (revert trigger)

**H (lane premise):** bounded-depth iteration inside one pre-registered family, survivor-measured on untouched confirm, yields at least one candidate that clears confirm + cost-law + N-SURV where the one-shot corner has yielded none.

**Inertness limb:** if this ADR is `Accepted` and **no lane campaign prereg is frozen within 6 weeks of acceptance** (or by 2026-11-08, whichever is earlier), the charter was decorative — report at the next quarterly programme audit and demote to `Superseded` unless the operator re-elects it with a dated schedule.

**Yield limb:** **2 consecutive completed lane campaigns** whose nominated survivor fails the confirm read (or passes confirm and then fails N-SURV) ⇒ the depth premise is `FALSIFIED` — supersede this ADR + source-class post-mortem. Not a license for a wider K, a lower floor, or a third variant of this lane.

**Counting machinery (without this, the limbs are unbinding — mirror of the blind channel's battery-closure/N=3 machinery):**
- **(a) Authoritative surface.** The running-count line below is canonical; STATE is a mirror only.
- **(b) Terminal states.** Every frozen lane prereg must terminate in exactly one of: **confirm read** (→ survivor passes or strikes the yield limb), or a **dated abandonment record on this ADR**. There is no third exit — a campaign cannot open, burn its K on train, and evaporate off every counter.
- **(c) What abandonment does.** An abandonment after open **discloses, does not strike** (the confirm never ran, so the depth premise was not tested) — but **2 consecutive abandonments** trigger the same audit-report duty as the inertness limb (report at the next quarterly audit; the lane is absorbing calendar without testing its premise). A prereg refused at freeze (bar unclear, conjunct failed, cost-law dead at family selection) counts on the refusals line only — mirror of the pre-G0-≠-strike boundary, same disclosure duty.
- **(d) What resets "consecutive".** A nominated survivor clearing confirm **and** N-SURV. Nothing else resets either consecutive count.

**Running counts (canonical, this ADR):** campaigns completed **0** · survivors falsified **0 / 2** · campaigns abandoned **0** (consecutive **0 / 2**) · preregs refused **0**.

**Trigger check schedule:** rides the standing 2026-11-08 slate (channel §4 readings) + quarterly audits.

---

## §5 — Forbidden moves (under this charter)

- **Self-ratify / run anything at `Proposed`.** Operator GO is the only activation.
- **θ-retune laundering.** A family in `docs/rejected_candidates.md` enters only by clearing its own re-proposal bar first, in writing, in the prereg — the lane never overrides a bar. Dedup attestation (executed, output pasted) is mandatory per prereg.
- **Reading confirm during iteration**, computing per-variant confirm results, or re-nominating after a confirm read. One survivor, one read, ever, per campaign.
- **Retroactive K.** Variants explored informally before the prereg count in K (D-K1 language imported); a prereg that under-declares is void.
- **Waiving the `floor_at_k(K, confirm_years) ≤ 2.0` predicate per-campaign**, shortening the confirm after seeing train results, or recomputing the floor at a friendlier `years` post-hoc.
- **Double-homing a candidate** across this lane / blind / harvest / MSL to dodge a counter, or re-classifying a lane kill to avoid the §4 yield limb.
- **Citing this charter against `CAP`, `DSR_MIN`, EM0, or any one-shot channel's predicate.** They are untouched; this lane is additive.
- **Skipping the W4 re-arm at K > 3.** The frozen split alone is not the disclosed substitute at this depth.

---

## §6 — Consequences

**Positive:** the one structurally missing lane (depth) exists with every anti-p-hacking control the estate already owns wired in at charter level; the survivor bar is *higher* than any one-shot channel's (1.265–1.475 at K=10–33 vs 0.98 at K=3), so a lane survivor is a stronger object than anything the current corner can emit; composes with Q-CAPBAND-1's stop rule — a lane campaign is an axis with floor in [1.0, 2.0] whose prereg clears all four non-Cap gates as **binding** conditions (power via §2.2(iii), cost-law via §2.5 family-selection arithmetic, venue legality + no-binding-bar via §2.1's consult and attestations), and no Cap moves, with the SR > 2 move answered by §2.2(ii) regardless.

**Negative (real, stated):** the floor arithmetic demands a mechanism materially better than anything measured in the futures era (best Tradeify-basis annSR on record +0.835); ≈ 0.82 power even at a true-1.83 edge means a real edge can die at the bar ~1 time in 5; a 6.5-year confirm likely requires parent-era data procurement (Databento cost dry-run, $ bounded); operator decisions per campaign ≈ 3 (charter GO once, prereg GO, confirm-read GO); and two consecutive survivor failures kill the lane by its own §4 — the depth premise gets exactly one falsification budget.

**Downstream artifacts NOT changed:** `core/` (all), `axis_screen.py`, `register_search.py` semantics for existing lanes, harvest/blind/MSL counters, N-SURV, lifecycle, M1/arming chain.

---

## §7 — Implementation plan (licensed only on `Accepted`, in order)

1. **First campaign prereg** — filed as `docs/briefs/pre-registration/*deep-lane*.md` (mandatory filename pattern; its path is recorded on this ADR's running-count line at freeze) — family (design-box geometry, non-index micro), declared K, train/confirm partition + years, all three §2.2 conjuncts computed and shown, half-split + per-half floor, nomination rule, SPA/StepM thresholds (W4 re-arm), cost-law arithmetic at the venue-legal expression, `instrument_profiles.py cell` output pasted, standing-pause attestation, dedup attestation pasted, re-proposal-bar clearance if any bar is adjacent. Operator GO on the prereg is a separate mark.
2. **Code:** `--lane deep` flag on `register_search` (open requires the prereg path + declared K + partition; refuses on the §2.2 predicate), lane-scoped tests. No change to other lanes' predicates.
3. **Doc scoping:** one-line lane-scoping note on `docs/methodology/strategy_harvest.md` Clause-K and a reader-intercept on M-19 (its K-sweep will otherwise be quoted against the lane without §2.2's answer).
4. **Skill wiring:** `futures-anomaly-discovery` SKILL K-accounting section gains the lane row.
5. **Data (if the 6.5-year-confirm geometry is elected):** Databento parent-era cost dry-run → operator GO → pull → panel manifest.

---

## §10 — Audit hooks

```bash
# Charter status (must not read Accepted without an operator GO line in change history):
grep -n "Status:" docs/adr/2026-08-16-deep-iteration-lane-charter.md

# Floor arithmetic reproduces (constants frozen):
python -c "import sys; sys.path.insert(0,'lab'); from research_utils import axis_screen as a; print(a.CAP, a.DSR_MIN, round(a.floor_at_k(33),3), round(a.floor_at_k(33, years=3.25),3))"
# Expected: 1.0 0.95 1.475 2.09

# Untouched surfaces:
grep -n "DD_TRIGGER = 0.015\|DD_SCALE = 0.40" core/dd_protection.py
grep -n "CAP = 1.0" lab/research_utils/axis_screen.py

# Inertness limb (post-Accept): a lane prereg exists within 6 weeks (mandatory *deep-lane* pattern, §7.1) —
ls docs/briefs/pre-registration/ | grep -i "deep-lane" || echo "no lane prereg yet"

# Counter hygiene — lane kills recorded here, never on the blind/harvest counters:
grep -n "Running counts (canonical, this ADR)" docs/adr/2026-08-16-deep-iteration-lane-charter.md
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-16 | Drafted `Proposed` at operator direction on the 2026-08-16 bottleneck diagnostic; nothing binds | Claude Code (drafter) |
