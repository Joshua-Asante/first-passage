# Q-CAPBAND-1 — Verdict pre-registration (H-CAPBAND)

**Frozen:** 2026-08-15, **before any non-Cap gate fact is read** for either band axis. Parent brief: [`Q-CAPBAND-1-cap-band-counterfactual.md`](../Q-CAPBAND-1-cap-band-counterfactual.md). **Execution requires a separate operator GO.**

---

## §A — Pinned inputs (frozen; no substitutions)

| Input | Value | Source |
|---|---|---|
| Cap under test | `CAP = 1.0` | `lab/research_utils/axis_screen.py:31` (frozen, no CLI/env override) |
| Band axis 1 | **D6** — `eurusd_pattern_enum Phase-4 (locked K=450)`, floor **1.835**, `clause_k = FAIL` | `lab/archive/q_kbudget_1_2026-07/floor_scan.py`, executed 2026-08-15 |
| Band axis 2 | **D2-low** — `wide mining, other GLBX family`, floor range **(1.925, 2.165)**, low end 1.925, `clause_k = FAIL` | same |
| Anchor (a) | best in-house validated edge **1.83** (legs span 1.11–1.83) | M-19 `:883` |
| Anchor (b) | corrected published top-decile net single-strategy Sharpe **S_B 0.85** (median 0.3–0.5) | M-19 `:883` |
| Naming authority for the axis set | 2026-08-03 gate-stack audit §5.4 item 3 | names D6 and D2-low explicitly |

**The axis set is closed at these two.** No axis may be added, swapped, or invented at execution time — that would be selecting evidence after seeing the question.

## §B — The non-Cap gate list (frozen; an axis "clears" only by clearing ALL of these)

1. **Clause-N confirm power ≥ 0.50** — read from the axis's own `clause_n` field in the frozen `floor_scan.py` table. Not recomputed.
2. **Cost-law reachability** — the mandatory 4× RT inequality at the axis's **venue-legal expression** at the incumbent, using primary-sourced Tradeify commissions (`help.tradeify.co` art. 10468315, 2026-04-28) and `lab/discovery/cost_model.py`.
3. **Venue legality** — the axis's instrument is tradable at `Tradeify_Select_100K` (`core/firm_rules.py` + the venue's supported-products article). An axis whose instrument the venue does not host fails here.
4. **Live registry / domain bar** — any binding bar via `scripts/instrument_profiles.py cell`, plus `docs/rejected_candidates.md` domain bars, evaluated as a door-check.

An axis **fails** the counterfactual test the moment it fails **any one** of 1–4. An axis **clears** only by clearing all four.

## §C — Method (binary locational read; no free tolerance parameter)

For each of the two frozen axes, in order, read gates 1–4 from **already-recorded facts only**. Record PASS / FAIL / `unevaluable` per gate with its source anchor. No edge is measured; no campaign is opened; no K is charged. If a gate requires new measurement to evaluate, it is recorded `unevaluable` — **it is not measured under this brief.**

## §D — Decision rule

| Verdict | Trigger |
|---|---|
| `RESOLVED` (Cap evidence-ratified) | **Both** D6 and D2-low each fail ≥1 gate from §B |
| `FALSIFIED` (counterfactual priced) | **≥1** axis clears all four §B gates |
| `AMBIGUOUS-HOLD` | For **both** axes, the gates that are not already FAIL are `unevaluable` at $0 |

**Neither branch moves `CAP`.** `RESOLVED` ratifies it on evidence; `FALSIFIED` prices a counterfactual and hands the operator a decision constrained by M-19's *"overfit-suspect zone (SR > 2)"* forbidden move. Any Cap change is a separate pre-registration → re-derivation → admitting ADR chain, and this artifact may not be cited as authorizing one.

## §E — Pinned ex-ante expectation (surprise marker)

**Predicted: `RESOLVED`.** Reasoning recorded before the read: D6 is a EURUSD pattern-enumeration axis with a *locked* K = 450 — its venue-legal expression at Tradeify would be 6E/M6E, and the EURUSD ledger already carries a DEAD `event-window-reversal` cell and an `AMBIGUOUS-PARKED` turn-of-month cell, so gates 3–4 are plausible failure points before cost is even reached. D2 is "wide mining, other GLBX family," which the channel ADR's own K-cap addendum forecloses independently and which DISC-CAMP-0 is the worked null for.

A `FALSIFIED` outcome would therefore be a **genuine surprise** and should be treated as the informative result — it would mean the programme has been declining a fundable axis on a constant alone. Recording the prediction so that outcome cannot be retrofitted as expected.

## §F — Forbidden moves (inherited from the parent §5, restated for the frozen record)

1. Editing `CAP` under this brief.
2. Reading `FALSIFIED` as "therefore Cap = 2.0."
3. Substituting or adding a band axis at execution time.
4. Scoring an axis on its **edge** rather than its **gates**.
5. Citing 2026-08 channel dryness as evidence for either branch.
6. Using Aegis 1.83 as a reachability ceiling (withdrawn 2026-08-15: cohort-bound, K-undeclared, un-deflated).
7. Amending §B's gate list after seeing a gate result.

---

**Freeze note:** this pre-registration must be committed **before** Phase 2 of the parent brief reads any gate fact, and the commit ordering is the evidence of that (the Q-BUSTGATE-1/-2 pattern). No non-Cap gate fact for D6 or D2-low has been read at the time of this freeze.
