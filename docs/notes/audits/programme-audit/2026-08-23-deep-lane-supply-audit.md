# Programme audit — deep-iteration lane, §4(c) supply-side audit — 2026-08-23

**Layer:** object (research programme — the deep-iteration lane's empirical premise; not the
locked portfolio, not a methodology). No methodology-audit verdict is cited as evidence anywhere
below, and no locked-book P&L — layer discipline per the programme-audit skill.
**Programme:** [deep-iteration lane charter](../../../adr/2026-08-16-deep-iteration-lane-charter.md)
(`Accepted` 2026-08-16).
**Audit window:** 2026-08-16 (acceptance) → 2026-08-23. First audit of this programme.
**Trigger:** charter §4(c) — **2 consecutive abandonments** (DL-1 2026-08-16, DL-2 2026-08-22)
fired the audit-report duty ("the lane is absorbing calendar without testing its premise"),
owed at the next quarterly audit; brought forward on operator instruction 2026-08-23. Scoped by
the operator as a **supply-side audit**: does any candidate family exist that is
**(i) genuinely new-mechanism, (ii) reachable with the current data estate, and
(iii) venue-shape-compatible?**
**Spend / K:** $0 · K=0 (audit reads existing records; no data touched, no confirm approached).

---

## §1 — Context

The lane's hard core (charter §4 H): *bounded-depth iteration inside one pre-registered family,
survivor-measured on untouched confirm, yields at least one candidate that clears
confirm + cost-law + N-SURV where the one-shot corner has yielded none.* Two campaigns have run.
Both abandoned at the §6 step-2 screen; the confirm partition — the premise's only test — has
never been read. Root causes are established and **distinct** (reconciled 2026-08-22 against a
re-run of both harnesses): DL-1 candidate-level (40–70% of trades resolve to genuine stop/target;
adverse win-rate at 3R), DL-2 construction-level (85–95% force-flat non-resolution; geometric
infeasibility on M6A confirmed quantitatively and the construction retired per its own
pre-committed stop rule — [DL-2 Iterate block](../../../../lab/archive/dl2_m6a_pdhpdl_2026-08-22/RESULTS.md)).

## §3 — Seven diagnostic questions

**1. Hard core integrity — PRESERVED.** Both campaigns ran exactly per the hard core: preregs
frozen before data contact, K≈10 declared, nominee = strict argmax with no walk-down, all four
gates computed both times, confirm untouched (mechanically verified: zero references to the
confirm cache in either harness; fable-judge pass 2026-08-23 re-ran the checks), abandonments
dated on the canonical §4 counting line. Terminal-state rule §4(b) satisfied twice — no campaign
evaporated off a counter. Anchors: commits `414e537` / `2086a17` / `b713ba2`;
[DL-1 RESULTS](../../../../lab/archive/dl1_mgc_orc_2026-08-16/RESULTS.md) ·
[DL-2 RESULTS](../../../../lab/archive/dl2_m6a_pdhpdl_2026-08-22/RESULTS.md).

**2. Belt churn — adds 3 / removes 0 (baseline; first window).** Adds: (a) §2.2(iv)
sealed-consultation disclosure conjunct ([two-ledger K ADR](../../../adr/2026-08-22-grow0-two-ledger-k-question.md),
ratified 2026-08-22, disclosure-only); (b) roll-day skip-back lookback rule (frozen in DL-2
prereg §1 pre-data, during adversarial review); (c) geometric-feasibility-ratio gate (armed via
DL-2's Iterate entry packet — any successor reusing the construction must clear it for its own
instrument first). Removes: 0. All three adds carry independent grounding and two of the three
make future campaigns *harder* to open, not easier. Net +3 in one week is a baseline to track,
not a finding — trend needs ≥2 windows.

**3. Progressive evidence — NONE at the market level; real at the process level.** The lane's H
has produced zero corroborated market predictions — it has never been tested (that is this
audit's trigger). Process-level: the feasibility diagnostic's stop rule was pre-committed in the
Iterate block *before* the diagnostic ran and resolved exactly as written (R<<1 → construction
retired) — a prediction-then-outcome at the control layer. Surplus content produced in-window:
the construction-feasibility constraint itself (a reusable, mechanical pre-flight gate that did
not exist a week ago) and two registry-recorded family kills.

**4. Degeneration evidence — NONE.** No gate threshold touched post-hoc; no walk-down; no
re-nomination; no retune; both abandonments accepted at face value. Trap #12 respected — DL-2's
construction defect was recorded as a concern, never silently patched into the frozen prereg. The
one post-failure belt add (feasibility gate) is a *control tightening* with a pre-committed
decision rule, not a rescue patch.

**5. Boundary respected — YES.** Charter §5 + prereg §5 forbidden moves: no confirm reads
(verified), no variant-set edits, no instrument-hop mid-campaign, no K under-declaration, no
threshold amendments mid-execution. The external second-opinion lens stayed inside its own ADR's
rails (sanitized-only, zero authority) and its one load-bearing hypothesis ("one disease at two
stages") was **refuted by re-running DL-1's harness** before anything was logged — the boundary
worked as designed.

**6. Theory-comparison — one incomplete screen surfaced and repaired.** DL-2's family selection
chose M6A over MGC/MCL on a clean governance door + cheapest RT. The door-check screened bars and
cost but **not geometric feasibility** — the chosen family then died on exactly the unscreened
dimension. Counterfactuals (MGC/MCL) were not run, so outperformance is unknowable; the durable
yield is the screen-set repair (the feasibility gate now sits ahead of any successor freeze). The
mechanism-id NEW-vs-reuse reversal (operator, on a second opinion) has no measurable outcome
difference yet.

**7. Falsifier check — ZERO DRIFT.** §4 limb text (inertness 6-weeks/2026-11-08; yield
2-consecutive-confirm-fails; §4(c) 2-consecutive-abandonment report duty; reset rule (d))
diffed between the charter's first commit (`f60959a`) and HEAD: **byte-identical**. The
running-count line changed as designed (it is the authoritative counting surface); no threshold
moved. Inertness limb: discharged (DL-1 froze same-day as acceptance). Yield limb: 0/2 —
untouched; **the depth premise is NOT falsified**, it is untested.

## §3.5 — The supply-side question (evidence census)

**Conjunct (i) — genuinely new-mechanism.** The registry
([`MECHANISMS.md`](../../../../ops/instruments/MECHANISMS.md), 30 ids) is saturated in the
OHLCV session-geometry family space, with kills or non-promotable holds across every role and
reference type: through-break continuation (CON-4 `AMBIGUOUS-HOLD` at 0.27× cost; DL-2
construction-walled), failed-break fades (MYM, MGC, M2K×2 — all explore-`FALSIFIED`),
opening-range continuation/breakout (MYM 7-ground kill; DL-1 abandoned; ZB sign-reversed),
pullback-failure resumption (MCL `FALSIFIED` on cadence), VWAP-reclaim (0.11× cost),
compression families (non-promotable holds; net-negative under venue RT), time-of-day volatility
trigger (9% of its own pass bar), intraday momentum (statistically ABSENT on modern MNQ +
external corroboration), ICT objects (three-instrument anti-attractor falsification; the one
RESOLVED positive — bear-FVG draw — died at expression on the horizon-mismatch wall, `MNQFVG-1`
`AMBIGUOUS-UNDERPOWERED` with uniformly adverse disclosure; route-1 on `MNQ × ict-liquidity`
**presumptively exhausted** per its own ledger). External channels: the Koijen axis-2 harvest
push closed with **zero admissions** (P1/P2 cheap-falsifier FAIL, P3 venue SCREEN-FAIL, P4 HOLD
on a data-sourcing question, P5 UNSCREENABLE); six discovery threads terminated 2026-08-20 on
"needs a genuinely new mechanism/data source, not another test"
([ox-alpha ADR §1's dated anchor](../../../adr/2026-08-22-ox-alpha-adversarial-lens-scope.md));
MSL S4's expiry-OI construct came back **wrong-signed** at explore (net divergence, FLIP-FAIL).
What is left that is genuinely new: **(1) the order-flow modality** — its own class finding
states the null probe "does **not** close the order-flow modality; it closes that modality's
cheapest swing," and two independent exhaustion rulings name route 2 (order-flow) as the
sanctioned next step; **(2) the event-window auction limb** — cheapest re-open is **free**
(a published, citable cohort δ for MOC-imbalance → index response; no procurement);
**(3) the blind channel** — alive, unsourced (count 1/3 pre-G0 kills; `AMBIGUOUS-HOLD` reading
due 2026-11-08).

**Conjunct (ii) — reachable with the current data estate. THIS IS THE BINDING CONJUNCT.** The
OHLCV estate is mined for this family space (above). The one concrete, already-designed new-
modality lead — [`MNQFLOW-1-DEPTH`](../../../../lab/analysis/c1/mnq_orb_flow_depth_2026-08-18/PREREG.md)
— is **`FROZEN — PULL NOT AUTHORIZED`**: prereg written, K_intrinsic=0, ≤$125 inside the
untouched Avenue-A credit, waiting on exactly one operator sign-off. Reachable with a signature,
not with bytes on hand. The auction limb waits on an external published cohort (free but not yet
found); the blind channel waits on its own sourcing event.

**Conjunct (iii) — venue-shape-compatible.** Shape is determined at construction, and the estate
already owns the screen for it (EM0–EM5 mechanism-shape spec, ratified 2026-08-06; the MSL
design box rr∈[2,3] / WR 0.30–0.42 / hard-stop / k=1 / no-pyramiding is itself the
venue-compatible shape). The constraint genuinely kills daily hold-to-close reversal shapes
(the Koijen P3 venue SCREEN-FAIL is the worked instance) and pyramided/high-skew shapes — it
does not pre-kill an intraday order-flow-derived construct. Conjunct (iii) is satisfiable but
per-candidate, at construction time, through the existing screen.

⚠ **CORRECTED 2026-08-24 — the bolded clause above, read as a sufficiency claim, is falsified by
measurement.** [`RESULTS_DESIGNBOX_EXT.md`](../../../../lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS_DESIGNBOX_EXT.md)
(design-box vs A2-region reconciliation, operator-GO'd 2026-08-24) extended the A2 payoff-shape
feasibility map to the design box's own geometry — win rates spanning its 30–40% floor (shared row
with A2; 42% not tested), A2's own cadence axis, A2's own EM2 risk axis, **plus the box's own
computed bust-≤3.0% diffusion frontier-R** (an executable closed form from
[N-2026-08-13 §9](../../notice/N-2026-08-13-msl-design-box-rederivation.md), independently re-run
and verified against the notice's own published table) — scored against the identical production
survivor-MC engine and gates A2 uses, on both `Tradeify_Select_100K` and `MFFU_Rapid_100K`.
**Result: 80/80 cells `INFEASIBLE`. 0 `FEASIBLE`, 0 `MARGINAL`.** The closest cell (WR=35%,
cadence=1, frontier-R $124.21) posts 5.05% bust — 68% over the 3.0% ceiling the closed form was
solved to hit exactly, and a confident fail (2σ lower bound 4.80%), not a near-miss obscured by
noise. **Landing inside the design box's stated geometry is not, by itself, sufficient for
venue-shape-compatibility** at the win rates this extension covers. What survives, and is
reinforced: this paragraph's own final sentence — "satisfiable but **per-candidate**, at
construction time, **through the existing screen**" — already declined to claim automatic
clearance; the correction sharpens that qualifier rather than reversing it. The design box's own
*directional* premise is independently corroborated by the same measurement (its 2–3R-win shape
cuts bust 3–10× versus A2's best-surviving shape at the identical win rate/risk, RESULTS_DESIGNBOX_EXT.md
§7) — the shape is a real improvement, just not shown sufficient on its own at these win rates.
This correction does not change §4's `AMBIGUOUS` disposition (conjunct (ii) remains the binding
constraint there) and does not itself decide the deep-iteration lane's fate — see
RESULTS_DESIGNBOX_EXT.md §10/§11 for the full reconciliation and the owed reader-intercepts (the
charter and the design-box ADR itself, both ratified decision artifacts, neither edited by this
correction).

**Answer:** **No candidate family satisfies all three conjuncts with data on hand.** The nearest
satisfier is the order-flow route: (i) ✓ genuinely new modality, (iii) ✓ determinable at
construction via the existing shape screen, (ii) **one operator sign-off away** (≤$125, K=0,
prereg already frozen). Everything else in the estate is killed, held non-promotable,
shape-incompatible, or waiting on external evidence that has not appeared.

## §4 — Disposition verdict

**`AMBIGUOUS`** — dated 2026-08-23, with named re-test conditions (below). Reasoning against the
alternatives: not **Falsified** (the yield limb is 0/2 — the premise was never tested; §4's own
text is explicit that abandonment discloses, does not strike); not **Degenerating** (Q4/Q5 clean —
no patches, no drift, boundaries held; this is the *opposite* of the degeneration signature); not
**Progressive** (zero market-level corroborations); not **Stable** ("delivering value without new
insight" misdescribes a programme that has never once reached its own value-delivery step). The
lane's premise is **untestable until supply exists** — that is an evidence-insufficiency verdict,
which is exactly what `AMBIGUOUS` is for, and the supply census above names precisely what
resolves it.

**Re-test conditions (any one resolves the AMBIGUOUS):**
1. **A supply event** — the `MNQFLOW-1-DEPTH` pull is authorized and its measurement yields a
   candidate family, OR the blind channel sources its first candidate, OR a published
   MOC-imbalance cohort δ is found (free re-open of the auction limb). On any of these, the
   lane's slot-3 decision re-opens with an actual family to weigh.
2. **The 2026-11-08 slate** arrives with none of the above — then the lane's disposition
   escalates beyond this audit (PARK or supersede per the charter's own inertness-limb template),
   adjudicated at that slate alongside the four-firms §4 falsifier, the harvest idle guard, and
   the blind-channel reading it already shares the date with.

**Slot-3 recommendation (operator-gated, not executed by this audit):** do **not** spend the
lane's third campaign slot now. Both remaining template paths — path (a) new instrument under
the now-gated construction, path (b) construction redesign — spend the slot on the depleted
OHLCV session-geometry pool the census above documents. Hold slot 3 **gated on a supply event,
not a calendar date**. This subsumes the three-path question the
[STATE row](../../../../STATE.md) carried: the answer path (c) resolved to is "pause," but the
audit's finding is that the pause's exit condition is *supply*, not further process audit — the
process questions (Q1–Q7) came back clean.

## §5 — Spawned follow-ups

1. **Operator decision item (primary) — UPDATED 2026-08-23 twice, same day, post-audit.** The
   operator signed off on `MNQFLOW-1-DEPTH` same day this audit landed. Its own P0 cost gate
   fired ($148.04 vs $125.00, 18.4% over — [§9.2](../../../../lab/analysis/c1/mnq_orb_flow_depth_2026-08-18/PREREG.md)).
   The operator then elected the redraw path; a second, independent, non-overlapping 30-day
   sample (`PREREG_S2B.md`) was drawn, signed, and P0-checked — **also blocked**, $154.73 vs
   $125.00 (23.8% over — [§9.2](../../../../lab/analysis/c1/mnq_orb_flow_depth_2026-08-18/PREREG_S2B.md)).
   **Two independent draws landing 18–24% over the same ceiling reframes this from "unlucky
   sample" to a structural finding**: this construct's real 30-day MBP-10 cost at MNQ's current
   activity level is closer to $150 than the $125 the ceiling was set from (a single-day
   extrapolation that undershot both times). This audit's own characterization of the route as
   "≤$125, one sign-off away" was stale within hours; left uncorrected above per this note's own
   dated-record convention, corrected here instead. Per the redraw's own pre-committed FM-9, no
   third resample follows automatically — the operator decision is now: raise the ceiling to
   ≈$160–175 (informed by two real draws, not one extrapolated day), pre-register a smaller N
   (e.g. 20 of 255, ≈$100–103 at the measured pooled rate), or fall back to the two remaining
   named routes (free MOC-imbalance literature check; blind channel). **Operator disposition,
   2026-08-23 (elects none of the above): `HOLD`** — *"I am not ruling it out but I do not know
   if it is worth the spend."* No forced re-test date; owner remains operator, naturally
   revisited at 2026-11-08 alongside the lane's own broader supply question, or sooner at the
   operator's own initiative. The two remaining named supply routes (free MOC-imbalance
   literature check; blind channel, unsourced) are unaffected and remain independently
   available regardless of this HOLD.
2. **Free literature check (bounded):** one pass for a published, citable MOC-imbalance cohort δ
   (the auction limb's own recorded cheapest re-open). Owner: any future research session;
   bounded to citation-search only, no procurement. No date — opportunistic.
3. **Belt-churn baseline logged:** 3 adds / 0 removes this window; next lane audit compares.
4. **Charter/STATE/SESSIONS surfaces updated** with this audit's pointer (same commit).

## §10 — Audit hooks (runnable at next cycle)

```bash
# Falsifier drift (must stay byte-identical on the limb text)
git show f60959a:docs/adr/2026-08-16-deep-iteration-lane-charter.md | grep -E "Inertness limb|Yield limb|What resets" > /tmp/limbs_orig.txt
grep -E "Inertness limb|Yield limb|What resets" docs/adr/2026-08-16-deep-iteration-lane-charter.md > /tmp/limbs_now.txt
diff /tmp/limbs_orig.txt /tmp/limbs_now.txt && echo "no drift"

# Supply re-test condition 1 — has the depth pull been authorized / run?
grep -n "PULL NOT AUTHORIZED" lab/analysis/c1/mnq_orb_flow_depth_2026-08-18/PREREG.md || echo "STATUS CHANGED — re-test fires"

# Supply re-test condition 1 — has the blind channel sourced a candidate?
ls lab/discovery_manifests/ 2>/dev/null | grep -i blind || echo "blind channel still unsourced"

# Slot-3 hold still in force (running-count line: active campaign none, abandoned 2)
grep -n "campaigns abandoned \*\*2\*\*" docs/adr/2026-08-16-deep-iteration-lane-charter.md

# Belt churn vs this baseline (3 adds / 0 removes)
git log --oneline --since=2026-08-23 -- docs/adr/2026-08-16-deep-iteration-lane-charter.md
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-23 | Audit authored; §4(c) report duty discharged early on operator instruction ("run the supply-side audit"); verdict `AMBIGUOUS` with named supply-event re-test conditions; slot-3 hold recommended | Claude Code |
| 2026-08-23 | §5 item 1 updated same day: operator signed `MNQFLOW-1-DEPTH`; its own P0 cost gate fired ($148.04 actual vs $125.00 ceiling, 18.4% over) — blocked, $0 spent, no pull. The audit's "one sign-off away" characterization corrected as stale. Verdict/§3.5 census unchanged — this is a downstream event on the named lead, not a revision of the process findings | Claude Code |
| 2026-08-23 | §5 item 1 updated again, same day: operator elected the redraw path; a second independent 30-day sample (`PREREG_S2B.md`) also blocked at P0 ($154.73 vs $125.00, 23.8% over). Two draws now read as a structural cost finding (~$150 true cost, not $125), not an unlucky sample. FM-9 (pre-committed on the redraw) bars a third automatic resample. Verdict/§3.5 census still unchanged | Claude Code |
| 2026-08-23 | §5 item 1 closed out for now: operator disposition `HOLD` ("not ruling it out but I do not know if it is worth the spend"), electing none of the three named paths. No re-test date forced; the audit's other two named routes (free MOC-imbalance check; blind channel) stand unaffected. Verdict/§3.5 census still unchanged | Claude Code |
| 2026-08-24 | §3.5 conjunct (iii) corrected in place, dated: the design-box-vs-A2-region reconciliation (`RESULTS_DESIGNBOX_EXT.md`, operator-GO'd) scored 80/80 design-box-geometry cells `INFEASIBLE` against the production engine — the bolded "is itself the venue-compatible shape" clause is falsified as a sufficiency claim; the paragraph's own "satisfiable but per-candidate" qualifier is sharpened, not reversed. §4's `AMBIGUOUS` disposition and conjunct (ii)'s binding status are unchanged — this correction does not decide the lane's fate | Claude Code |
