# ADR 2026-08-05b — BluSky's activity rule sourced: the limit is real, and the unit was wrong

**Status:** `Accepted` — operator directive this session (2026-08-05): *"source BluSky's actual activity rule from help.blusky.pro"*, the limb ADR 2026-08-05 §4 T1 pre-registered as the thing that would decide F3.
**Decision date:** 2026-08-05
**Authors:** Joshua (directive) + Claude Code (sourcing + measurement + draft + apply)
**Supersedes:** [`2026-08-05-blusky-inactivity-unsourced-encoding.md`](2026-08-05-blusky-inactivity-unsourced-encoding.md) — its §4 **T1 fired**. That ADR's containment was correct for what was known at the time and is now discharged, not overturned.
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** superseded by a BluSky rule republication (§4 T2) or by an ADR that resolves the absorbing-vs-discretionary residual (§6)
**Related:** measurement [`lab/analysis/c1/f3_cadence_successor_venues_2026-08-05/RESULTS.md`](../../lab/analysis/c1/f3_cadence_successor_venues_2026-08-05/RESULTS.md) (+ its Addendum 2026-08-05b) · [`2026-08-04-tradeify-venue-descope-eval-included.md`](2026-08-04-tradeify-venue-descope-eval-included.md) §7 F3 · [`2026-08-04-firm-rules-eval-lock-fix-applied.md`](2026-08-04-firm-rules-eval-lock-fix-applied.md) (sibling `firm_rules.py` correction; its §5 no-widening-to-BluSky applies to `dd_lock_offset_usd`, untouched here)
**Layer:** production config correctness (venue-fact sourcing + unit conversion). **No `dd_protection` constant, allocation, Pine file, lifecycle state, `dd_type`, or frozen gate threshold is touched.**

---

## §0 — Rule 0 reads (primary venue sources, read in-browser 2026-08-05)

| Source | What it establishes |
|---|---|
| `help.blusky.pro` Terms of Use art. **11490284 §3.3 "Abandoned Accounts"** (under §3 *Refunds and Billing Policy*) | The rule: *"Evaluation, BluLive, SimFunded, or brokerage accounts inactive for 30 consecutive days may be closed at our discretion."* **Evaluation accounts are named explicitly**, so it binds the modelled tier. Threshold 30 consecutive days; enforcement **discretionary**. |
| `help.blusky.pro` Brokerage Funded Rules art. **12434442** | Defines what BluSky means by *active*: *"place at least one trade every 30 days to keep the account active"* — inactivity is **trade-based**, not login- or payment-based. This is the article that disambiguates §3.3's otherwise-undefined "inactive". Consequence there is warning-first (fee, warnings, *possibly* close). |
| `help.blusky.pro` Billing art. **12434108** | *"The billing period of 30 calendar days will auto renew each period"* — the actual subscription-renewal window, and the thing the 2026-07-12 sweep had encoded. Confirms the old annotation described a real object, just not the field's object. Also establishes that **BluSky says "calendar days" when it means calendar**. |
| `help.blusky.pro` Evaluations collection (7 articles, incl. Evaluation Rules art. 12434059) | Carries **no** activity rule of any kind — which is why the 2026-07-12 sweep, scoped to that collection, missed the ToU clause. Failure mode: right collection, wrong document class. |
| Help-centre search for `inactivity` / `inactive` | Exactly two articles match: the ToU and the Brokerage Funded Rules. No third rule exists to reconcile. |
| `core/mc/simulation.py:171-178` | The consumer: `consecutive_idle >= inactivity_limit` counted in **business days** (the panel is bday-indexed) and **absorbing**. This is where the unit mismatch bites. |
| `lab/analysis/c1/f3_cadence_successor_venues_2026-08-05/out/blusky_unit_sensitivity.{log,json}` | The measurement of the unit correction, this session, same panel/seeds/geometry as the parent study. |

**Gitignore pre-flight.** No Pine source read or cited; no vendor CSV re-exported. Panel is the committed 2026-07-23 `daily_panel.csv`, unchanged.

---

## §1 — Context

[`ADR 2026-08-05`](2026-08-05-blusky-inactivity-unsourced-encoding.md) contained a field it could not correct: `BluSky_Premium_*.inactivity_max_idle_days: 30`, annotated in its own comment as the *"30-day eval subscription renewal window"*, with **no** BluSky activity rule found anywhere in the repo. Its §4 T1 pre-registered the discharge: source the real rule, encode it, flip the flag, supersede, and re-run F3's BluSky arms.

Sourcing found the rule — **in the Terms of Use, not the Evaluations collection.** The 2026-07-12 sweep read the rules articles and stopped there; the binding clause sits under *Refunds and Billing Policy*, which is also why the original annotation landed on the adjacent billing cycle. Both objects are real, both are "30 days", and the sweep encoded the wrong one.

So the threshold `30` turns out to be **right by coincidence and wrong by unit**. The clause counts *calendar* days (BluSky writes "calendar days" explicitly when it means them, and an abandonment clause has no trading-day concept). The engine counts **consecutive idle business days**. A literal `30` in the engine therefore models ~42 calendar days — roughly **40% more lenient than the published rule** — and the leniency runs in the optimistic direction on the one axis F3 turns on.

**Decision driver (one sentence):** the rule exists, binds evaluation accounts, and is trade-based — so the field can finally be sourced rather than contained; but encoding its number literally would keep a ~40% optimism that the containment flag was never designed to catch.

---

## §2 — Decision

**1. `inactivity_max_idle_days` on both `BluSky_Premium_*` tiers changes `30` → `22`.** 22 idle business days is the threshold at which 30 calendar days has certainly elapsed (4 weeks + 2 days). 21 is the tighter end of the bracket and was measured alongside it; 22 is chosen as the value that does not over-tighten beyond what the clause says.

**2. `inactivity_rule_sourced` flips `False` → `True`** on both tiers, with the comment block rewritten to cite ToU art. 11490284 §3.3 and art. 12434442, retain the billing-window history so the original error is not re-made, and record the unit conversion and the residual.

**3. ADR 2026-08-05's guard machinery is retained unchanged.** `allow_unsourced_inactivity` stays in `firm_kwargs`; no shipped tier now carries the flag, so it is dormant, and its tests are re-pointed at a synthetic tier so the machinery cannot rot. **The guard is not deleted** — it is the mechanism that will catch the next tier onboarded without provenance (that ADR's §4 T2).

**4. F3's substantive verdict is unchanged in direction, corrected in magnitude.** BluSky remains a different cadence class from the 5-day venues, by 6–20× rather than by ~100×.

**Effective:** immediately upon acceptance.
**Scope:** `core/firm_rules.py` (2 values, 2 flags, 1 comment block), `tests/core/test_mc_preflight.py`, and pointer/addendum updates. **No engine change** — `core/mc/preflight.py` and `core/mc/simulation.py` are untouched by this ADR.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Encode `30` literally now that a "30-day rule" is sourced** | The tempting move, and wrong: it silently equates the clause's calendar days with the engine's business days, preserving ~40% optimism under the cover of a fresh citation. A citation that licenses the wrong unit is worse than no citation, because the flag comes off. |
| **Encode `21`** | Defensible (4 weeks + 1 day ≈ 29 calendar days) and measured alongside 22, but it fires *before* 30 calendar days has necessarily elapsed. Prefer the value that does not over-tighten beyond the published rule; the 21-vs-22 spread is ≤1.7pp on every arm, so nothing rests on the choice. |
| **Keep `inactivity_rule_sourced: False` because "inactive" is still not perfectly defined** | Over-conservative once art. 12434442 defines *active* as placing a trade. Holding the flag after the rule is sourced would make it a permanent warning label rather than a targeted signal, and would blunt it for the tier that actually needs it next. |
| **Model the discretionary clause as non-absorbing / probabilistic** | Genuinely more faithful — *"may be closed at our discretion"* is not certain death — but it requires an enforcement-probability parameter no venue publishes, i.e. inventing a number to soften a rule. Absorbing errs conservative (real hazard ≤ modelled). Named as a residual (§6), not fixed. |
| **Re-run and rewrite the F3 RESULTS tables in place** | Not this repo's convention (2026-08-04 ADR §3/§5: pointer banner on the historical artifact, not a rewrite). The parent RESULTS keeps its measured body and gains a reader-intercept banner + addendum carrying the corrected BluSky figures. |
| **Treat this as re-opening F3's verdict** | F3 is operator-owned and dated 2026-08-08. This ADR changes an input's magnitude; it does not elect, exclude, or rank a venue. |

---

## §4 — Falsifier

**H (binary):** *BluSky's evaluation accounts are bound by a published, trade-based activity rule at 30 consecutive calendar days (ToU §3.3 + art. 12434442), whose faithful encoding in the engine's business-day, absorbing barrier is 22 idle bdays — and the locked Striker book's exposure under it is 4.87–13.14%, materially worse than the superseded 0.52–1.40% and materially better than the 5-day venues' 90.85–97.54%.*

| # | Trigger | Threshold | Action |
|---|---|---|---|
| T1 | BluSky publishes an evaluation-phase activity rule that is **not** 30 days, or explicitly scopes §3.3 to trading days | primary source, article-cited | Re-encode; if 5-day-class, **F3's answer becomes "no successor survives the unmitigated barrier"** and all three candidates fall |
| T2 | §3.3 is republished defining "inactive" as login- or payment-based rather than trade-based | primary source | The field stops being an activity rule at all; revert to the 2026-08-05 containment posture (flag `False`) |
| T3 | A tier is onboarded whose inactivity value is not traceable to a published activity rule and which omits `inactivity_rule_sourced` | any new tier | Block at engine pre-flight — inherited from ADR 2026-08-05 §4 T2, still in force |
| T4 | An artifact quotes BluSky's **superseded** 0.52–1.40% as current | any RESULTS/ADR/brief | Banner it; the parent RESULTS' own banner + addendum is the reference form |

**Not admissible as a revert route:** restoring `30` because it matches the clause's printed number. The printed number is calendar days; the field is business days. That equivalence is the defect this ADR closes.

**Revert action:** author a superseding ADR. Never edit §2 in place.

**Trigger check schedule:** T1/T2 at the next 90-day venue-fact re-verify (~2026-11-05, and this session resets that clock for BluSky). T3 on any new tier. T4 at each programme audit.

---

## §5 — Forbidden moves

- **Reading "sourced" as "faithful".** The unit is converted and the modality is not: a discretionary clause is still modelled as an absorbing barrier. §6 keeps that visible.
- **Loosening the limit because enforcement is discretionary.** *"May be closed"* is not *"will not be closed"*. Soft enforcement is not a licence to assume non-enforcement — the Tradeify sibling learned the opposite lesson the hard way when a *"soft-enforced, warning first"* reading turned out to be permanent deletion (`c1_cadence_inactivity_2026-08-02` Addendum 2026-08-02b).
- **Deleting the `allow_unsourced_inactivity` machinery** because no tier currently uses it. It is the standing gate for the next onboarding.
- **Electing or excluding a successor venue on this ADR.** F3 stays operator-owned at 2026-08-08.
- **Quoting the superseded BluSky figures** (0.52–1.40%) as current.
- **Loosening any §4 trigger without a superseding ADR** (Known Trap #12).

---

## §6 — Consequences

**Positive:**
- The field is a sourced venue fact for the first time, on all four FRIENDLY firms simultaneously — the provenance asymmetry RESULTS §1 documented is closed.
- The correction runs **against** the program's convenience: it makes the only surviving successor candidate look ~10× worse, which is the direction a sourcing pass is least likely to produce by motivated reasoning.
- ADR 2026-08-05's pre-registered T1 discharged in under a day, exactly as written.

**Negative consequences (real, not theatrical):**
- **The parent F3 RESULTS' BluSky rows are superseded within a day of publication**, and PR #647 carries both the original tables and their correction. That is the cost of publishing a measurement before the venue-fact sweep it depended on was complete — the honest sequencing would have sourced first.
- Re-running `run_f3_cadence.py` no longer reproduces its own published BluSky rows (Bulenox, MFFU and the Tradeify control still reproduce exactly). Flagged in the harness itself and in the RESULTS banner.
- The 2026-07-12 BluSky sourcing sweep is now known to have been **collection-scoped rather than document-scoped** — it read the Evaluations articles and never opened the Terms of Use. Other fields sourced in that same sweep (consistency 34%, cost, auto-liquidation) were not re-verified here and inherit the same scope risk.

**Risks:**
- **Absorbing-vs-discretionary residual (unfixed).** The engine kills every path at the barrier; the venue *may* close the account. Direction is conservative, magnitude unmeasured.
- **Calendar↔business-day conversion is an approximation.** 22 assumes a holiday-free 5-day week; a period containing exchange holidays reaches 30 calendar days in fewer than 22 idle bdays, so 22 is mildly lenient in holiday-heavy stretches.
- **The 2026-07-12 sweep's other BluSky fields remain un-re-verified** (see above). Named here rather than silently assumed sound.

**Downstream artifacts needing update (this commit):** `core/firm_rules.py` · `core/mc/preflight.py` (docstring/pointer — claim-alignment M41/C13) · `tests/core/test_mc_preflight.py` · the parent RESULTS (banner + Addendum 2026-08-05b) · `run_f3_cadence.py` (reproduction note) · ADR 2026-08-05 (`Superseded-by`) · `docs/adr/INDEX.md` · `STATE.md` row 3 · `docs/SESSIONS.md`.

---

## §7 — Verification result

**Sourcing** — four primary articles read in-browser; help-centre search for `inactivity`/`inactive` returns exactly two rule-bearing articles, both cited in §0. No third rule exists to reconcile.

**Measurement** — `run_blusky_unit_sensitivity.py`, same panel/seeds/geometry as the parent study, `BluSky_Premium_100K`:

| Arm | limit 30 (superseded) | **limit 22 (this ADR)** | limit 21 |
|---|---|---|---|
| C2-off · 1.00× | 0.52% | **4.87%** | 5.59% |
| C2-off · 0.50× | 1.09% | **10.48%** | 11.88% |
| C2-on · 1.00× | 0.76% | **7.04%** | 7.98% |
| C2-on · 0.50× | 1.40% | **13.14%** | 14.80% |

Worst at the **C2-on 0.50× rung** — the WATCH-1 rung the c1 book would actually deploy at. The 21-vs-22 spread is ≤1.7pp on every arm, so §3's choice between them is not load-bearing.

**Regression** — `tests/core/test_mc_preflight.py` 32 passed, with the guard tests re-pointed at a synthetic unsourced tier and a new pin asserting `22` + `sourced: True`. Full-suite result recorded in the session entry.

---

## §10 — Audit hooks (runnable)

```bash
# 1. Both BluSky tiers carry the corrected, unit-converted limit.
grep -n "inactivity_max_idle_days\": 22" core/firm_rules.py
# Expected: two occurrences, both on BluSky_Premium_* rows

# 2. Both are marked sourced; no shipped tier is flagged unsourced any more.
grep -c '"inactivity_rule_sourced": True' core/firm_rules.py   # Expected: 2
grep -c '"inactivity_rule_sourced": False' core/firm_rules.py  # Expected: 0

# 3. The guard machinery survives its own obsolescence (ADR 2026-08-05 §4 T3).
grep -n "allow_unsourced_inactivity" core/mc/preflight.py
python -m pytest tests/core/test_mc_preflight.py -q -k unsourced
# Expected: keyword still present; synthetic-tier guard tests pass

# 4. Every shipped tier runs inactivity-ON with no acknowledgement.
python -m pytest tests/core/test_mc_preflight.py -q -k sourced_tiers

# 5. The superseded figures carry a pointer wherever they appear.
grep -n "Addendum 2026-08-05b" lab/analysis/c1/f3_cadence_successor_venues_2026-08-05/RESULTS.md
# Expected: banner near the top AND the addendum section

# 6. No engine, risk-control, allocation, or Pine change in this ADR.
git diff --stat HEAD~1 -- core/mc/simulation.py core/mc/preflight.py core/dd_protection.py core/lifecycle.py core/strategies/
# Expected: empty
```

---

## Verification

```bash
python scripts/check_adr_graph.py
python scripts/check_status_consistency.py
python scripts/check_falsifier_reachability.py
python -m pytest tests/core/test_mc_preflight.py -q
python lab/analysis/c1/f3_cadence_successor_venues_2026-08-05/run_blusky_unit_sensitivity.py
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-05 | Initial authoring, `Accepted` on operator directive. Supersedes the same-day containment ADR by discharging its §4 T1: BluSky's activity rule sourced to ToU art. 11490284 §3.3 (+ art. 12434442 defining *active* as trade-based), limit unit-corrected 30 → **22 idle bdays**, `inactivity_rule_sourced` flipped to `True` on both tiers. Guard machinery retained and re-tested against a synthetic tier. F3's direction unchanged, magnitude ~10× worse. Absorbing-vs-discretionary and the 2026-07-12 sweep's collection-scoping named as residuals. | Joshua (directive) + Claude Code (sourcing + measurement + draft + apply) |
