# Scoping + seed manifest — NG-EIA-1: short-NG announcement-bracket premium on weekly EIA storage days

**Status:** `CLOSED — FALSIFIED at Phase-0` (2026-07-21). Operator GO recorded (§8, after the construct correction); Databento NG pull `$0.00`; K=0 consumed. **P0.2 power FAIL (δ/σ 0.052 vs floor 0.109) and P0.3 cost-law KILL (8.3bp vs 29.6bp hurdle, ~3.6× under) on the corrected POST-ONLY PRIMARY construct.** Per-year delta alternates sign nearly every year (noise, not a decaying real premium) despite a clean faithfulness anchor (50.7bp — larger than F-B's own 25.6bp, confirming correct dating). SANITY-1 (the wider pre+post bracket) offers no rescue. Phase-1 never reached. Results: [`lab/archive/ng_eia_recon_2026-07/RESULTS.md`](../../../lab/archive/ng_eia_recon_2026-07/RESULTS.md). Disposition: append to [`rejected_candidates.md`](../../rejected_candidates.md); lock HELD (no `core/`/allocation/`dd_protection`/Pine touch).
**Candidate:** NG-EIA-1 — short NYMEX Henry Hub Natural Gas (NG) futures across the **post**-announcement window of the weekly EIA Natural Gas Storage Report (enter ~10:25 ET, cover ~11:00 ET), harvesting the documented announcement-day risk premium. **Construct correction (2026-07-21, before any run — see change history):** the citable delta attaches to the post-only window; an earlier draft of this brief described a pre+post bracket, which is wrong — see §1/§2.
**Lane:** external-mechanism harvest intake (`docs/methodology/strategy_harvest.md`), Requirement-1 path **1a** (named risk-premium flow), Tier-B admission (announcement-day, conditional on event-rate clearing Req-4).
**Loop of record:** STRATEGIC (discovery Stage-0). **Authored:** 2026-07-20 · Claude (Sonnet 5), operator-directed (post-brainstorm workflow selection).

---

## §0 — Rule-0 reads (production source, verified this session 2026-07-20)

- **`discovery_manifests/*.json` (all 7, listed this session)** — no NG-family manifest exists ⇒ **NG family K_banked = 0** (verified via `ls discovery_manifests/`, cross-checked against the census the same-session brainstorm workflow produced). This is the load-bearing Requirement-3 input; unlike gold (foreclosed, K=3,177) or the ES/NQ/CL families (K=1–2), NG is untouched.
- **[`docs/rejected_candidates.md`](../../rejected_candidates.md) @ `568c639`** (includes today's own ORB-ZB-1 entry) — grepped for `NG`/`natural.gas`/dedup collision: **none found.** No prior NG rejection, no re-proposal bar to clear.
- **[`lab/archive/q_fbeia_1_2026-07/extract_eia_delta.py`](../../../lab/archive/q_fbeia_1_2026-07/extract_eia_delta.py) @ `8bdb071`** (F-B, CL EIA-inventory δ-extraction, `CLOSED SCREEN-FAIL`) — the **structural template** this Phase-0 harness is modeled on: pre-committed event-window construction authored *before* any return is read, Databento own-cohort δ-extraction, Req-4 power gate + Req-5 cost-law gate computed in-script, verdict string written to a `_results.json`. **Critical distinction from F-B (read in full, §1 below):** F-B tested crude oil's *Wednesday* Petroleum Status Report and found the release reaction (25.6bp) entirely surprise-conditional — zero unconditional edge. NG-EIA-1 targets a **different EIA release** (the *Thursday* Natural Gas Storage Report) and a **different published claim**: an announcement-*bracket* risk premium documented as **not** explained by the surprise (the opposite informed-flow shape from F-B — see §1).
- **[`docs/briefs/closures/H-ZNAUC-1-closure-screen-fail.md`](../closures/H-ZNAUC-1-closure-screen-fail.md) @ `aa0738d`** + **[`lab/archive/q_znauc_1_2026-07/extract_delta.py`](../../../lab/archive/q_znauc_1_2026-07/extract_delta.py) @ `aa0738d`** — the sibling own-cohort δ-extraction pattern (ZN post-auction), source of the exact power-floor arithmetic this brief reuses: `req4 = |δ/σ| ≥ 1.96/√N` (verbatim from the script: N=259 calibration gives the "0.122" constant quoted in that brief — re-derived per-N below, not copied blind).
- **[`ops/prop_envelope_default.md`](../../../ops/prop_envelope_default.md) @ `7af4224`**, §1 row E1 (line 16): *"All positions closed before the daily flat deadline; build target 16:00 ET... No overnight holds."* §2 item 4 (line 29): **"No firm names in research artifacts. Firm-specific facts enter only at the deployment fork via §4 overlays."** — this brief therefore does **not** gate on per-firm NG/MNG instrument availability (unverified in-repo for any firm; correctly out of scope for a research-stage brief per this rule) and uses the generic Bulenox `cost_per_side_usd=0.61` convention already standard across this program's harnesses (H-ZNAUC-1, H-FBEIA-1, ORB-ZB-1), not a firm-specific NG lookup.
- **`core/firm_rules.py` @ `a53ee99`** — grepped `cost_per_side_usd`: 17 hits, all index-micro-anchored (`$0.61`/`$0.91`/`$0.95` by firm tier); **no NG or MNG row exists**. Consistent with every prior event-drift harness (ZN/CL) in this program — none used a firm_rules.py per-instrument lookup either; all used the generic commission + CME public tick spec. Same convention followed here.
- **[`docs/adr/2026-07-20-stage8-variance-dominance-risk-neff-gate.md`](../../adr/2026-07-20-stage8-variance-dominance-risk-neff-gate.md) @ `7af4224`** — the binding composition gate (`n_eff_risk_delta > 0`, `ρ < 1.0`) this candidate is designed against, same as ORB-ZB-1 and RATES-EV-ZF-1 (sibling brief).
- **External, WebFetch/WebSearch-verified this session (not repo-internal; cited per source, not claimed as Rule-0 production reads):**
  - `ir.eia.gov/ngs/ngs.html` + `ir.eia.gov/ngs/schedule.html` — the Weekly Natural Gas Storage Report is released **Thursdays 10:30am ET**, with **non-uniform** holiday-week shifts (New Year's/Veterans Day → Friday 10:30am; National Day of Mourning/Juneteenth/Thanksgiving → Wednesday 12:00pm; Christmas → Monday 12:00pm). This is a **materially different and more complex** shift pattern than F-B's CL calendar (simple Wed→Thu shift) — see the calendar-construction discipline in §5.
  - CME public contract specs (WebSearch-cross-verified, two independent sources agree): NYMEX NG (Henry Hub) — 10,000 MMBtu contract, tick = $0.001/MMBtu = **$10.00/tick**. Micro NG (MNG) — 1,000 MMBtu (1/10 size).
  - Prokopczuk, Wese Simen & Wichmann, "The Natural Gas Announcement Day Puzzle," *The Energy Journal* 42(2), 2021, pp.91–112 (SSRN 3575861) — cited per the literature (peer-reviewed tier), not independently re-read this session; treated as **Tier-2 corroborated** by the adjacent NG-announcement literature named in §1, not a solo Tier-1 citation.
- **Construct-definition correction (this session, before any pull) — verified via a same-day adversarial screen this candidate went through prior to scoping:** the paper's citable ~12%/yr net-of-cost figure (t=2.93, Sharpe 1.76) attaches specifically to a **post**-announcement bracket ("short position AT announcement, closed 30 minutes afterwards"), **not** a pre+post bracket. A verified abstract fragment states *"the pre-announcement return is entirely generated on days when storage levels exceed analysts' expectations"* — i.e. **the pre-announcement leg is surprise-conditional**, the identical informed-flow shape that killed F-B (CL-EIA). Including the pre-leg in the PRIMARY construct would silently reimport the F-B trap into a candidate whose entire case rests on being *unconditional*. §2/§3 below are written to the corrected, post-only construct; the pre+post bracket is retained only as a non-gating comparison (SANITY-1).

---

## §1 — Context (the symptom this probe addresses)

**Why NG, after the vise synthesis and the ZB kill.** The 2026-07-20 brainstorm workflow (23 agents, adversarial screen) surveyed rates-event, FX/yen, flight-to-quality-lag, and NG/wildcard mechanism classes against the program's two-wall vise (cost-law admits only large-δ directional mechanisms; Stage-8 requires those same mechanisms add *risk* breadth, not just correlation breadth). Two rates-event candidates and one NG candidate survived both an executioner and a rescuer pass; this brief scopes the **higher-prior** of the two fund-worthy directions — NG-EIA-1 is the only candidate in the full supply with a **target-cohort, peer-reviewed, net-of-cost δ already published** (the sibling brief, RATES-EV-ZF-1, is the lower-prior/higher-prize δ-extraction-from-zero direction, scoped separately).

**The mechanism, and how it differs from F-B's death — with a load-bearing correction.** F-B (CL EIA, `CLOSED SCREEN-FAIL`, informed-flow) found a large release reaction (25.6bp) that was **entirely surprise-conditional**: strip the inventory number and the unconditional edge collapsed to ~1bp. Prokopczuk/Wese Simen/Wichmann document that **more than half of NG futures' annual return concentrates on the ~52 EIA storage days**, split roughly half pre-/half post-announcement. **The pre-announcement half is itself surprise-conditional** (verified: "the pre-announcement return is entirely generated on days when storage levels exceed analysts' expectations") — the same conditionality that killed F-B. The genuinely unconditional, citable claim is narrower and attaches only to the **post**-announcement half: short at/near the 10:30 ET print, cover ~30 minutes later, net of costs, regardless of realized surprise direction. That narrower claim is still the opposite failure mode from F-B (an edge that survives without reading the surprise number), but it is a **smaller, more specific** claim than "the whole bracket premium," and this brief's §2/§3 are written to it precisely — not to the wider bracket an earlier draft described.

**Threading the vise.** NG's family K-bank is untouched (0), it is weather/storage-driven and near-zero correlated to equity indices (the decorrelation thesis the book structurally lacks per Q-COMPOSE-1 / decompound-HOLD), and the reported net-of-cost δ (~23bp/event, ~6× the full-NG round-trip cost) is the largest cost-clearance margin of any non-equity candidate this program has screened — well past D5 (fails 3.7×), H-OD-1 (fails 3.4×), H-ZNAUC-1 (fails 6–10×), and F-B (fails ~5×). This is the first candidate where, on the literature's own numbers, the arithmetic points the *right* direction before any data is pulled.

**Honest grounding caveat (Requirement-1, disclosed up front, not buried — corrected to the harder reading).** R1 is **weak, not cleanly passed**. The source paper is titled a "puzzle" precisely because the authors reject the standard surprise-information explanation *and cannot confirm any alternative* — the candidate's own risk-premium story (retail UNG/BOIL-complex longs paying shorts) is this brief's post-hoc attribution, not a claim the paper itself makes. Worse: the sign runs **opposite** standard announcement-risk-premium theory (Savor-Wilson-class theory predicts *longs* get compensated for bearing event risk; here shorts collect, which requires an unnamed, unmeasured net-long hedging-pressure story to explain). The **1b fallback also fails** for the specific directional claim: the three adjacent papers (Chiou-Wei/Linn/Zhu 2014; Bjursell/Gentle/Wang 2015; Halova/Kurov/Kucher 2014) corroborate that announcement-day **volatility/jump concentration** is real — they do **not** corroborate the *unconditional negative drift* this candidate needs. That leaves effectively **one paper, one cohort, ~2–2.5 decades of underlying data, zero ≥10-year post-discovery replications** (published 2020/21) — a real 1b shortfall, not a technicality. R1 survives only as **R1-PENDING**: Phase-0's own 2019–2026 in-house measurement *is* the missing replication, not a formality layered on top of an already-strong R1. The paper's own sample **ends pre-2019** and **reports the anomaly decreasing in magnitude over its own sample window** (embargoed full text; unverifiable behind the embargo) — native-micro-era survival is exactly what Phase-0 measures, not assumed.

**Standing-doctrine connections.** Lane = external-mechanism harvest intake (`strategy_harvest.md`), Tier-B ("conditional... admits only if event rate clears requirement 4 **and** per-event δ clears the cost inequality — check both, assume neither"). Sibling to F-B (CL, same intake class, opposite verdict shape) and H-ZNAUC-1 (own-cohort δ-extraction pattern). Not a re-proposal of any dead direction — dedup confirmed clean in §0.

---

## §2 — Seed manifest (`strategy_harvest.md` §5 template)

```markdown
# Harvest-seed manifest — NG-EIA-1

- admission-date: 2026-07-20
- requirement-1 path: 1a (named risk-premium flow) — WEAKEST 1a FORM,
  R1-PENDING (see §1 corrected grounding caveat) — post-hoc attribution, sign
  runs opposite standard announcement-premium theory, 1b fallback fails for
  the directional claim (adjacent papers corroborate vol/jump concentration,
  not the unconditional drift). Phase-0 itself is the missing replication.
- mechanism (req 1a): retail-heavy long-side holders of the NG announcement-day
  exposure (UNG/BOIL-complex, event-insurance-style buyers) systematically pay
  a premium to shorts who bear the announcement-window risk. The source paper
  explicitly REJECTS the standard surprise-information explanation and frames
  the finding as an unresolved "puzzle" and does not itself make this
  who-loses attribution (contrast H-ZNAUC-1's dealer-short-gamma-unwind story,
  which IS a clean, paper-stated 1a).
- source + tier: Prokopczuk, Wese Simen & Wichmann, "The Natural Gas
  Announcement Day Puzzle," The Energy Journal 42(2) 2021, pp.91-112
  (SSRN 3575861) — peer-reviewed, Tier 1 channel (futures-native journal).
  Adjacent (NOT corroborating the directional claim, only announcement-day
  vol/jump concentration): Chiou-Wei/Linn/Zhu (JIMF 2014), Bjursell/Gentle/Wang
  (Energy Economics 2015), Halova/Kurov/Kucher (JFM 2014).
- target instrument + family (req 3): NG (NYMEX Henry Hub Natural Gas, full
  contract). MNG micro EXCLUDED at admission (see key_numbers) — 1-lot NG only.
- K_banked(family): 0 (no NG manifest exists; verified 2026-07-20 against
  discovery_manifests/ — §0)
- K_intrinsic (confirm-not-mine): 1 — single fixed PRIMARY construct: short
  ~10:25 ET (blind entry just ahead of the 10:30 print, no lookahead), cover
  11:00 ET (POST-ONLY, ~35min hold — the citable construct; NOT a pre+post
  bracket, corrected from an earlier draft, see change history). A wider
  09:30-11:00 window (adds the surprise-conditional pre-leg) is reported as
  SANITY-1 for comparison only, never gating and never K-consuming (it is not
  a second candidate, it is a diagnostic on the same PRIMARY data). NO
  window/threshold sweep beyond this single pre-committed PRIMARY cell.
- K_eff + floor(K_eff): K_eff = 1 -> floor 0.65 (most beatable; below S_B median)
- delta/sigma (req 2): on-cohort, peer-reviewed, NET-of-cost, POST-ONLY window:
  ~12%/yr AFTER transaction and funding costs (t=2.93, Sharpe 1.76), i.e.
  ~23bp/event net (12%/52) attaching specifically to the post-announcement
  bracket (verified: "short position AT announcement, closed 30 minutes
  afterwards"). Decay-haircut note: paper itself reports the anomaly
  DECREASING over its own sample; sample ends pre-2019 (exact window
  embargoed to 2026-11-30). Conservative central reading used (net-of-cost,
  not gross) per strategy_harvest.md §4. Break-even: the effect would need to
  have decayed to roughly HALF its documented magnitude before Phase-0's own
  power gate (below) starts to fail (executioner-verified: R5 breaches at
  ~35% decay, R4 at ~52% decay).
- N + event frequency (req 4): ~52 events/yr x 7y (2019-2026) = N ~ 364
  (fixed calendar; some loss to holiday-shift ambiguity, see Phase-0 design).
  Weekly frequency clears the "daily-or-intraday" structural bar Tier-B
  requires (contrast the two dead MONTHLY mechanisms at N~86, power 0.24-0.34).
- power: at documented delta/sigma ~0.15-0.20 (23bp net vs ~100-150bp weekly
  sigma), power = Phi(sqrt(364)*0.15 - 1.96) ~ 0.86 to Phi(sqrt(364)*0.20-1.96)
  ~ 0.99. At HALF documented delta (decay scenario), power ~0.50-0.59 -- the
  decay scenario is the honest edge case Phase-0's own gate resolves.
- dedup attestation: rejected_candidates.md + closed discovery manifests +
  docs/methodology/rejected_signals.md checked 2026-07-20 (grep, this
  session). No NG entry anywhere. Not a collision with the dead CL-EIA (F-B)
  direction: F-B's kill was the surprise-conditional PRE-release reaction;
  this candidate's PRIMARY construct deliberately EXCLUDES the analogous
  surprise-conditional NG pre-leg (see the K_intrinsic correction above) and
  tests only the disclosed-unconditional post-window -- the F-B failure mode
  is a real risk this construct was specifically redesigned to avoid, not an
  unrelated release.
- screen verdict: PASS (both clauses, on the cited literature numbers) ->
  licenses Phase-0 delta-extraction only, per the PASS-never-blesses
  asymmetry (strategy_harvest.md §3).
- operator ratification: PENDING (this brief requests the Phase-0 GO, §8)
```

---

## §3 — Phase-0 cheap-falsifier battery (own-cohort δ-extraction; K=0, ~$0)

Single native-NG δ-extraction (Databento GLBX.MDP3 `NG.v.0` continuous ohlcv-1m, 2019→2026 — the D5-precedent statistical/OOS-native era; the F-B/H-ZNAUC-1 pattern additionally pulls a cheaper IS-era cache first where available), producing all limbs from one script authored **before** any return is read (the F-B/H-ZNAUC-1 discipline — pre-commit the window, then look).

| # | Screen | Measure | PASS condition | Precedent |
|---|---|---|---|---|
| **P0.1 — event-day faithfulness anchor** | mean absolute reaction, 10:30→10:35 ET (immediate release window, ahead of/inside the PRIMARY hold) | reproduces a large, non-trivial reaction (sanity: confirms events are correctly dated on the native micro-era — the F-B `\|m0\|=25.6bp` pattern) | If the reaction is near-zero, the calendar is almost certainly mis-dated (see the holiday-shift risk in §5) — STOP and fix dating before reading any further limb |
| **P0.2 — PRIMARY Req-4 power (frozen formula)** | PRIMARY window ONLY: short 10:25 ET → cover 11:00 ET; `δ/σ = mean(ret)/std(ret)`; `power = Φ(√N·\|δ/σ\| − 1.96)` | power ≥ 0.50 at the realized native-era N (holiday-ambiguous weeks dropped, §5 — expect N≈300–350, not the nominal 364) | H-ZNAUC-1 / F-B formula, reused verbatim |
| **P0.3 — PRIMARY Req-5 cost-law** | `\|δ\|_bp ≥ 4 × RT_frac`; RT_frac(NG) = 2×($0.61 + 1-tick $10 slip)/notional, both single- and conservative two-RT conventions reported (H-ZNAUC-1/F-B convention) | clears the 4× hurdle on at least the single-RT convention | Same gate that killed D5/H-OD-1/H-ZNAUC-1/F-B; this is the one limb the published literature already claims a wide margin on (~6×) |
| **P0.4 — MNG sizing sanity (informational)** | same PRIMARY construct at MNG (1,000 MMBtu) economics | report only — MNG is expected to fail cost-law on a coarser relative-tick basis (per §1 research; not repo-verified) | Determines whether Phase-1, if reached, must size at 1-lot NG only (E5 micro-sizing tension flagged, not resolved, here) |
| **SANITY-1 — wider bracket comparison (informational, NEVER gating)** | short 09:30 ET → cover 11:00 ET (adds the surprise-conditional pre-leg back in) | report only — comparing SANITY-1 vs PRIMARY is the diagnostic for whether the pre-leg's informed-flow contamination materially inflates the wider bracket, corroborating or complicating the R1 sign-inversion concern (§1) | Exists to make the F-B-avoidance decision auditable, not to rescue a failed PRIMARY |

**Ordering:** P0.1 runs first as a dating sanity check (a failed faithfulness anchor invalidates everything downstream and must be diagnosed before the gate numbers are trusted). **P0.2/P0.3 on the PRIMARY (post-only) window are the actual verdict**; P0.4 and SANITY-1 are informational only and never substitute for P0.2/P0.3.

---

## §4 — Falsifiable hypothesis (H-NG-EIA-0; binary)

**H-NG-EIA-0 — if** the fixed **post-only PRIMARY** construct (short 10:25 ET → cover 11:00 ET) on native NG clears **P0.1** (faithfulness — a real, dateable reaction) **and P0.2 Req-4 power ≥ 0.50** **and P0.3 Req-5 cost-law ≥ 4× on at least the single-RT convention**, **then** NG-EIA-1 graduates to a Phase-1 K=1 confirmation campaign (`register_search open` + §R freeze + full Stage 5/6/7/8, including a properly-registered temporal-consistency battery given the paper's own documented decay); **otherwise** it closes FALSIFIED (or, if P0.1 fails, `NEEDS_CONTEXT` pending a calendar-dating fix, re-run once) and is appended to `docs/rejected_candidates.md`.

**Numeric accept threshold:** graduate iff `power ≥ 0.50` AND `|δ| ≥ 4×RT_frac(single-RT)`. **Falsified** on either failing with a correctly-dated event set. **The decay scenario is explicitly not a kill on its own** — if δ has approximately halved from the paper's documented magnitude, P0.2/P0.3 are designed to still show the honest boundary (power ≈0.5, cost-ratio ≈3×) rather than a clean pass or fail; that boundary case routes to `AMBIGUOUS`, not a forced binary call.

---

## §5 — Forbidden moves (each genuinely tempting)

- **Using a simple "Wednesday→Thursday" or "always-Thursday" holiday-shift heuristic** (the F-B/CL convention) for the NG calendar — **wrong for NG.** §0 verified the EIA's own published exception table: NG holiday shifts are non-uniform (Wed 12pm / Fri 10:30am / Mon 12pm depending on the specific holiday), and that table only documents 2025–2026 — the historical (2019–2024) pattern is **not confirmed** from this session's sources. The forbidden move is assuming the current-year exception pattern held historically without checking, or silently reusing F-B's simpler rule. **Required instead (Phase-0 execution discipline, not optional):** drop any week containing a US federal holiday Mon–Thu from the **primary** cohort (conservative — trades N for dating certainty; N≈364→≈300–310 barely moves the power gate, per §2's power arithmetic) and report a best-effort holiday-shift-mapped reconstruction as a **secondary, non-gating** robustness check only.
- **Including the pre-announcement leg in the PRIMARY construct** — the corrected, load-bearing forbidden move this session's own screen surfaced. Verified: "the pre-announcement return is entirely generated on days when storage levels exceed analysts' expectations" — the pre-leg is surprise-conditional, the exact F-B/CL-EIA informed-flow trap. PRIMARY is post-only (10:25→11:00 ET); the pre+post bracket is SANITY-1, reported but never gating.
- **Sweeping the PRIMARY window** (entry lead time before 10:30, hold length past 11:00) to find one that clears the cost hurdle — that is a K-inflating search voiding the K=1 screen. The window is pre-committed in the Phase-0 script header before any return is read, exactly per the F-B/H-ZNAUC-1 discipline.
- **Promoting SANITY-1 to the verdict if PRIMARY fails but SANITY-1 (with the conditional pre-leg) passes** — that would be re-admitting the F-B trap through the back door. SANITY-1 is diagnostic only, per §3/§4.
- **Substituting a first-Thursday-of-month or other calendar heuristic instead of the EIA's actual published release-date history** — the same class of error the BLS/NFP calendar carries (memory: NFP diverges materially from a "first Friday" heuristic — 2nd Friday ~5×, non-Friday 4× 2022–2026). The EIA's *own* schedule/history pages (`ir.eia.gov/ngs/schedule.html` and predecessor archives) are the primary source; do not infer historical dates from the current year's pattern alone.
- **Reading the P0.4 MNG result as a rescue if P0.3 fails on full NG** — MNG is expected (research-only, not repo-verified) to fail cost-law on a *coarser* relative-tick basis than full NG; a full-NG cost-law failure is not expected to be rescued by the micro. If P0.4 unexpectedly shows the opposite, that is a genuine surprise worth flagging, not a result to search for.
- **Opening `register_search` / pulling the confirm panel before Phase-0 clears and a fresh operator GO is signed** — Phase-0 is K=0; Phase-1 K binds only on a separately-signed §R-frozen GO.
- **Quoting a Phase-0 PASS as an edge** — a δ-extraction licenses campaign scoping only; it never blesses a candidate (the D5/F-B/H-ZNAUC-1 asymmetry, restated).
- **Treating the paper's documented in-sample decay as disqualifying without measuring it** — the honest move is to let P0.2/P0.3 measure where the native-era δ actually sits, not to pre-judge the outcome from the decay caveat alone (that would be a forbidden D-test in the INQHIORI sense — assuming the conclusion the data should answer).

---

## §6 — Gate criteria (binary)

| Verdict | Trigger | Disposition |
|---|---|---|
| **RESOLVED (graduate)** | P0.1 faithfulness clean AND P0.2 power ≥ 0.50 AND P0.3 cost-law ≥ 4× (single-RT) | Author Phase-1 Stage-0 pre-reg (K=1, §R attestation per the D5/ORB-ZB-1 model, including a temporal-consistency battery given the paper's own decay disclosure) → fresh operator GO → `register_search open` → confirm campaign |
| **FALSIFIED (close + register)** | P0.1 clean but P0.2 or P0.3 fails | Close; append to `rejected_candidates.md` with the measured δ/σ, power, and cost-law ratio; K=0 spent; NG family bank stays 0 |
| **AMBIGUOUS** | P0.1 dating cannot be resolved (calendar defect), OR the decay boundary case lands genuinely on the fence (power ≈0.45–0.55 and cost ratio ≈3.5–4.5×) | Closure names the re-test condition (e.g. a confirmed historical holiday-shift table) or the fence-case numbers explicitly; no in-place threshold edit |

No calendar hard-date beyond the parent programme's 2026-11-08 idle review; Phase-0 is a single-session run once GO'd.

---

## §R — Reachability attestation (SKELETON — populated only at the Phase-1 freeze)

Not required for the Phase-0 no-K δ-extraction (H-ZNAUC-1/F-B precedent). Drafted here so the Phase-1 path is visible if Phase-0 clears:

- **R.1 — confirm gate (net Sharpe / power at K=1):** reachable *iff* the Phase-0-extracted native-era δ implies power ≥0.50 with cost clearance — **this is exactly what P0.2/P0.3 measure**, so R.1 cannot be honestly written until Phase-0 returns numbers (same logic as ORB-ZB-1's §R skeleton).
- **R.2 — placebo / robustness gate:** candidate construction — a non-event-week control window (e.g. a random Thursday not carrying an EIA release) with the identical short-bracket construct; expected ≈0 under the mechanism (the flow is announcement-conditional by construction, so a non-event control should show no comparable premium). To be frozen precisely at the Phase-1 pre-reg stage, not this scoping brief.

---

## §7 — Run protocol

0. **This brief:** manifest + Phase-0 battery frozen. **Operator reviews §8 → GO/NO-GO on Phase-0.**
1. **On Phase-0 GO:** build the EIA event calendar per §5's discipline (primary: drop holiday-ambiguous weeks; secondary: best-effort shift-mapped, non-gating) → Databento `db_fetch estimate` (dry-run, mandatory) → cost-gate check → pull `NG.v.0` continuous ohlcv-1m 2019→2026 (expect ~$0, matching every prior event-drift pull in this program) → run P0.1–P0.4 in one pre-committed script (F-B/H-ZNAUC-1 pattern: gates coded in the script header before any return is read). **K = 0** (measurement). Results land in `lab/archive/ng_eia_recon_2026-07/`.
2. **On P0 RESOLVED only:** author the Phase-1 Stage-0 pre-reg (D5/ORB-ZB-1 model — §R fully populated with the extracted δ, K=1, temporal-consistency battery given the decay disclosure) → **fresh operator §R GO** → `register_search open --lane mechanism-first` → confirm panel → Stage 5/6/7/8 → survivor-scoring gate G0–G8 vs prop envelope → (only then) lifecycle CANDIDATE intake.
3. **On P0 FALSIFIED:** append to `rejected_candidates.md`; done.

---

## §8 — Operator GO gate (Phase-0 δ-extraction only; DRAFT until filled)

```
PHASE-0 GO: 2026-07-21 / JA (operator chat: "run both Phase-0 probes")
Ratifies: a single-construct (POST-ONLY PRIMARY, corrected per the change-history entry
  above, authorized AFTER the correction landed), K=0, ~$0 native-NG delta-extraction
  (P0.1/P0.2/P0.3/P0.4 + SANITY-1).
Does NOT authorize: register_search open, any K spend, the Phase-1 confirm panel, or any
                    live/Pine/allocation/dd_protection/ACTIVE_FIRM touch.
```

---

## §10 — Audit hooks (runnable)

```bash
# 1. Phase-0 GO unfilled -> no NG manifest and no orb/eia pull may exist yet.
grep -n "PHASE-0 GO: ____________" docs/briefs/rnd-pipeline/NG-EIA-1-announcement-bracket-premium-scoping.md \
  && echo "GO unfilled -- no register_search / pull for NG" || echo "GO filled"

# 2. NG family bank is 0 (Requirement-3 basis; re-derive, do not trust prose).
ls discovery_manifests/ | grep -iE '^ng|natural.?gas' && echo "NG manifest EXISTS -- recheck K" || echo "NG bank 0 confirmed"

# 3. No dedup collision (re-derive at execution time too -- the registry grows).
grep -inE '\bNG\b|natural.gas' docs/rejected_candidates.md || echo "no NG collision confirmed"

# 4. K_intrinsic pinned at 1, single construct (no sweep).
grep -n "K_intrinsic (confirm-not-mine): 1\|single fixed announcement-bracket" docs/briefs/rnd-pipeline/NG-EIA-1-announcement-bracket-premium-scoping.md

# 5. Calendar discipline: holiday-ambiguous weeks dropped from primary, not heuristically shifted.
grep -n "drop any week containing a US federal holiday" docs/briefs/rnd-pipeline/NG-EIA-1-announcement-bracket-premium-scoping.md

# 6. Stage-8 risk-N_eff gate is the binding decorrelation statistic when this reaches composition.
grep -n "n_eff_risk_delta" lab/research_utils/breadth.py  # the gate has a real input

# 7. Precedent harnesses this Phase-0 is modeled on are the actual closed, real files.
test -f lab/archive/q_fbeia_1_2026-07/extract_eia_delta.py && test -f lab/archive/q_znauc_1_2026-07/extract_delta.py && echo "both precedent harnesses present"
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python <brief-authoring>/scripts/check_brief.py docs/briefs/rnd-pipeline/NG-EIA-1-announcement-bracket-premium-scoping.md --type inquire
# Expected: all 6 checks PASS

# §0 anchors current
git log -1 --format='%h %ci' -- ops/prop_envelope_default.md                                    # 7af4224
git log -1 --format='%h %ci' -- lab/archive/q_fbeia_1_2026-07/extract_eia_delta.py              # 8bdb071
git log -1 --format='%h %ci' -- lab/archive/q_znauc_1_2026-07/extract_delta.py                  # aa0738d

# K-bank ledger reproduces the instrument-selection finding
python -c "import json,glob; [print(p, json.load(open(p))['status'], json.load(open(p))['K']) for p in glob.glob('discovery_manifests/*.json')]"
# Expected: no ng_* / natural_gas_* entry
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-20 | Scoping + seed manifest authored (post-brainstorm-workflow selection, priority-1 direction). Phase-0 δ-extraction GO requested. Calendar-dating risk (NG's non-uniform EIA holiday-shift pattern, distinct from F-B's simpler CL rule) surfaced and resolved via a conservative drop-ambiguous-weeks primary design. | Joshua (direction) + Claude (Sonnet 5) |
| 2026-07-21 | **Construct-definition correction, before any pull.** Re-checked the brainstorm workflow's full executioner finding (only partially read at authoring time) and found the citable δ attaches to a POST-ONLY window (short ~10:25 ET → cover 11:00 ET); the pre-announcement leg is surprise-conditional — the F-B/CL-EIA trap. Corrected the candidate description, §1 mechanism/grounding (R1 downgraded to R1-PENDING per the executioner's harsher, more accurate read — sign inverted vs standard theory, 1b fails for the directional claim), §2 seed manifest, §3 battery (added SANITY-1 as non-gating), §4 hypothesis, §5 forbidden moves. Operator GO (chat, "run both Phase-0 probes") recorded in §8 below, filled after this correction. | Joshua (GO) + Claude (Sonnet 5) |
| 2026-07-21 | Event calendar built (EIA schedule primary-sourced 2026-07-20; 323 PRIMARY events, holiday-ambiguous weeks dropped). NG.v.0 pulled `$0.00`; Phase-0 run. **CLOSED FALSIFIED** — P0.2 power FAIL (δ/σ 0.052 vs 0.109 floor), P0.3 cost-law KILL (8.3bp vs 29.6bp, ~3.6× under). Faithfulness anchor clean (50.7bp); per-year sign alternates (noise). K=0. RESULTS + rejected_candidates disposition. | Joshua (GO) + Claude (Sonnet 5) |
