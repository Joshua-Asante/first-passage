# Q-CAPBAND-1 — CLOSURE: `RESOLVED` (Cap 1.0 evidence-ratified; both band axes die on non-Cap gates)

**Verdict:** `RESOLVED` — both D6 and D2-low independently fail a non-Cap gate, so `CAP = 1.0` has cost the programme nothing measurable on the axes the 2026-08-03 audit named
**Closed:** 2026-08-15
**Lane:** UNASSIGNED
**Pre-registration:** [`Q-CAPBAND-1-verdict-preregistration.md`](../pre-registration/Q-CAPBAND-1-verdict-preregistration.md) — frozen at `8fce86f`, committed **before** any gate fact was read (commit ordering is the evidence)
**Spend / K:** $0.00 · K consumed: **0** · no manifest · no edge measured
**Live effect:** none — `CAP = 1.0` byte-unedited at `lab/research_utils/axis_screen.py:31` (verified post-run)
**Artifacts:** [parent brief](../Q-CAPBAND-1-cap-band-counterfactual.md) · [pre-registration](../pre-registration/Q-CAPBAND-1-verdict-preregistration.md)

---

## 1. Verdict (§6 asserted against actual gate reads)

| §6 route | Trigger | Actual | Fired? |
|---|---|---|---|
| `RESOLVED` | **Both** band axes each fail ≥1 non-Cap gate | D6 fails gate 3 (venue); D2-low fails gate 4 (binding bar) | ✓ |
| `FALSIFIED` | ≥1 axis clears **all four** §B gates | neither axis cleared all four | — |
| `AMBIGUOUS-HOLD` | For both axes, all non-FAIL gates `unevaluable` at $0 | moot — each axis has a hard FAIL | — |

### Per-axis gate reads (recorded facts only; §C honored — nothing measured)

**D6 — `eurusd_pattern_enum Phase-4 (locked K=450)`, floor 1.835, family `6E/EURUSD`**

| Gate | Result | Evidence |
|---|---|---|
| 1 Clause-N power | `unevaluable` | frozen table records `clause_n = "n/a — Clause K kills first"` — recorded as *not evaluated*, so not a PASS |
| 2 Cost-law | **not reached** | axis already FAILed gate 3. (Also unevaluable via `cost_model.py`: `6E` sits in `NO_COMMISSION_ROW_INSTRUMENTS`; `M6E` absent from `INSTRUMENT_SPECS`.) |
| **3 Venue legality** | **FAIL** | `python scripts/instrument_profiles.py cell EURUSD trend-following` → `venue: NOT TRADABLE at the live firm — FXIFY/DXTrade CFD venue closed 2026-07-10; no live venue for this instrument at present.` |
| 4 Registry/domain bar | not reached | — |

**D2-low — `wide mining, other GLBX family`, floor 1.925 (range 1.925–2.165), family `ES/NQ/YM`, `k_intrinsic = (1000, 10000)`**

| Gate | Result | Evidence |
|---|---|---|
| 1 Clause-N power | `unevaluable` | same frozen `n/a — Clause K kills first` |
| 2 Cost-law | **not reached** | axis already FAILed gate 4 |
| 3 Venue legality | no FAIL recorded | ES/NQ/YM appear on the venue fee schedule; not decisive either way, and not needed |
| **4 Registry/domain bar** | **FAIL** | `instrument_profiles.py cell {ES,NQ,YM} trend-following` → **all three** return `BINDING BAR: index-intraday-ohlcv-directional-timing-2026-07-21` (gate `instrument-profiles`, tier=always). D2 is wide mining on exactly that bar's scope — *"a directional intraday timing edge on a single liquid US equity-index future, from OHLCV structure alone."* **Secondary independent ground:** the free-data 5th-leg SNAG names *"a wider sweep"* verbatim as not clearing its domain bar. |

**Per §B an axis fails the counterfactual test the moment it fails any one of gates 1–4.** Both did. The verdict rests on **gates 3 and 4 only** — gates 1 and 2 were never resolved for either axis, and this closure does not claim otherwise.

## 2. What the pre-registration predicted vs what happened

§E pinned **`RESOLVED`** before the read, and it fired. The reasoning was **partially** right and should be scored honestly:

- **D6 — correct, and for the named reason.** §E predicted *"gates 3–4 are plausible failure points before cost is even reached."* It died on gate 3, venue.
- **D2 — right verdict, wrong mechanism.** §E predicted D2 would die because *"the channel ADR's own K-cap addendum forecloses it."* It did **not** die that way — the K-cap addendum is dated 2026-08-15 and scoped to the blind channel, so it does not reach a 2026-07 harvest axis. The actual kill is the **2026-07-21 index raised bar**, which is older, machine-wired, and independent of anything decided this week. The prediction reached the right branch through a mechanism that does not apply.

No amendment to §6 or §B was made at any point (Trap #12 clean).

## 3. What this closure does NOT license

- **It does not establish that `CAP = 1.0` is correctly calibrated in general.** It establishes that Cap cost nothing **on the two axes the 2026-08-03 audit named**. A future axis in the [1.0, 2.0] band could still be blocked by Cap alone; this closure prices the counterfactual the audit asked about, not the constant's general correctness.
- It does not authorize any change to `CAP`, `DSR_MIN`, `POWER_MIN`, or `Z` — all remain frozen under harvest-intake ADR §5.
- It does not clear D6 or D2 for re-proposal. Each carries its own re-proposal bar unchanged.
- It does not resolve gate 1 (Clause-N) or gate 2 (cost-law) for either axis — both stay unevaluated.
- It does not bear on the 2026-08-15 channel's own dryness, which was explicitly barred from being evidence here (§5 forbidden move 5).

## 4. Defects found in the frozen brief (recorded, not repaired)

1. **§B gate 3 names `core/firm_rules.py` as a venue-legality source; it cannot serve that role.** `FIRM_RULES['Tradeify_Select_100K']` encodes only account geometry — `dd_type`, `max_dd_pct`, `profit_target_pct`, `micro_contract_cap`, `cost_per_side_usd`, `consistency_rule_pct`, etc. — and carries **no product, instrument, symbol, or tradability list at all** (keys enumerated this session). Venue legality is only establishable from the instrument ledgers and the venue's published product article. The gate still resolved because the ledger consult was decisive; the brief's citation was simply wrong about where the fact lives.
2. **Gate 2 is unevaluable-by-construction for any non-index-micro axis.** `cost_model.resolve_commission` raises for everything outside `{MES, MNQ, MYM, M2K}`, and `INSTRUMENT_SPECS` omits 6E/M6E/MCL/6J. Any future band axis outside the index micros will hit the same wall — gate 2 cannot fail such an axis, only return `unevaluable`.

## 5. Lesson candidates

Below the two-incident bar — watch: **a pre-registered prediction can reach the right verdict through a mechanism that does not apply** (§2, D2). Scoring the *branch* as correct while the *reasoning* was wrong would have banked a false confirmation of the prediction method. Worth a second instance before promoting; the repair is simply to score prediction reasoning separately from prediction outcome.

## Iterate — loop exit

- **Verdict used:** `RESOLVED`
- **Model update:** the Cap was a suspect and is now cleared *on the named evidence*. The structural finding it was suspected of causing — that this programme cannot afford to search — does **not** rest on a possibly-miscalibrated constant: even at Cap 2.0, D6 is venue-dead and D2 is bar-bound, so neither becomes fundable. The binding constraints on those two axes are venue reality and a 2026-07 domain bar, both older and independent of the Cap.
- **Next:** INTEGRATE
- **Routing:** INTEGRATE → discharges [2026-08-03 gate-stack audit](../../notes/audits/programme-audit/2026-08-03-gate-stack-audit.md) §5.4 item 3 (*"Whether G2's Cap = 1.0 was the right choice… nothing in the record discriminates"*). That item may now be recorded as **discharged on the named axes**, with the scope limit in §3 attached. No ADR, no constant change, no code edit.
- **Entry packet:** n/a — no successor opened.
- **Stop rule / re-proposal bar:** re-opening the Cap band requires a **new axis** whose floor lands in [1.0, 2.0] **and** which clears gates 1–4 — not a re-argument over D6 or D2, and not the channel's dryness. Per M-19, any future proposal to move Cap toward 2.0 must additionally answer the *"overfit-suspect zone (SR > 2)"* forbidden move, which this closure does not touch.
- **Board write:** `STATE decision index: Q-CAPBAND-1 RESOLVED — Cap 1.0 evidence-ratified on the named axes (D6 venue-dead, D2 bar-bound); 2026-08-03 audit §5.4 item 3 discharged; CAP byte-unedited.` Owner: this closure · [parent brief](../Q-CAPBAND-1-cap-band-counterfactual.md)
- **Registry:** n/a — gate-calibration counterfactual, not a strategy-grounds kill. No candidate was scored, admitted, or rejected: D6 and D2-low were read at the **gate layer only** (venue legality, binding bars) and never measured, per the frozen §C method. Nothing is owed to `rejected_candidates.md`; both axes retain their own pre-existing re-proposal bars unchanged.

## §10 audit-hook discharge (run this session)

```
$ grep -n "^CAP = " lab/research_utils/axis_screen.py
31:CAP = 1.0                                    # byte-unedited ✔

$ python -c "...floor_scan...screen()"
D2 -> floor (1.925, 2.165) clause_k FAIL ✔      D6 -> floor 1.835 clause_k FAIL ✔

$ python scripts/instrument_profiles.py cell EURUSD trend-following
venue: NOT TRADABLE at the live firm — FXIFY/DXTrade CFD venue closed 2026-07-10 ✔

$ python scripts/instrument_profiles.py cell {ES,NQ,YM} trend-following
BINDING BAR: index-intraday-ohlcv-directional-timing-2026-07-21   (3 of 3) ✔

$ ls discovery_manifests/ | grep -i capband
(no match) — no campaign opened ✔
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-15 | Closure authored; Phase 2 executed under operator GO | Joshua + Claude Code |

---

## Verification

```bash
python scripts/check_closure_disposition.py docs/briefs/closures/Q-CAPBAND-1-closure-resolved.md
grep -n "^CAP = " lab/research_utils/axis_screen.py   # expect CAP = 1.0
```
