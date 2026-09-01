# Pre-registration — Prop survivor scoring gate (four-firms ADR §4 falsifier)

> ⚠ **2026-08-26 — CLOSED per this file's own Known Trap #12 instruction.** The operator elected
> to raise the Part A eval bust ceiling from 3.0% to 5.0%, informed by (and same-day as) a measured
> 4.34% result that failed the ceiling below — exactly the "amendment after a result is seen"
> scenario this freeze names as the reason to close and reopen, not edit in place. Successor:
> [`2026-08-26-prop-survivor-scoring-prereg-v2.md`](2026-08-26-prop-survivor-scoring-prereg-v2.md),
> which documents the reversal, the full rationale (including that the 5% dial was **already
> offered and declined** at this file's own §3 authoring, below), and sourced context on
> discretionary-trader base rates. `lab/discovery/prop_survivor_scoring.py`'s `DEFAULT_PREREG`
> now points to the v2 file. Body below is frozen exactly as ratified 2026-07-13 (Trap #12) — it
> remains the accurate historical record of the original ceiling and its own stated rationale.

**FROZEN 2026-07-13, before any scored prop-tier re-MC is read.** No item below
changes after a result is seen. This artifact operationalizes the four-firms ADR
§4 primary falsifier into a fixed scoring protocol + numeric ceiling; it is a
faithful transcription of the **ratified** recommendation (no numbers re-decided
here — see §0). Amendments after a result require closing this pre-registration
and opening a fresh one (Known Trap #12).

**Status:** `CLOSED 2026-08-26 — superseded by v2 (ceiling 3.0% → 5.0%, operator ruling)`.
Frozen body below is historical record — do not amend numbers in place (Known Trap #12).
**Prior status:** FROZEN / not-yet-exercised. No DISC-CAMP-0 survivor was ever scored under this
version; `register_search` for the first campaign never opened under it. This froze the gate
*before* the first candidate existed.
**Loop of record:** STRATEGIC
**Feeds:** the four-firms ADR §4 falsifier (hard date **2026-11-08**; 08-08 is a
progress check only).
**Authored:** 2026-07-13 · Claude Code (Opus 4.8), operator-directed.

---

## §0 — Rule-0 reads (production source, verified this session 2026-07-13)

All content-read from the working tree; per-file anchors (`git log -1`):

- **`core/firm_rules.py` @ `6a0c801`** (2026-07-13) — `ACTIVE_FIRM="FXIFY"` (historical
  anchor fixture, asserted); `AUTOMATION_FRIENDLY_PROP_FIRMS` 4 families; the four
  **$100K tiers all at `max_dd_pct: 3.0` / `profit_target_pct: 6.0`**; `dd_type` per
  family — Bulenox/BluSky `trailing`, Tradeify/MFFU `trailing_locking`; all prop tiers
  carry `daily_loss_pct: None`. **Commissions present for all four families** (17
  `cost_per_side_usd` entries — Tradeify $0.91 / MFFU $0.95 / BluSky $0.95-NT-rail /
  Bulenox $0.61) + `consistency_rule_pct` on Tradeify (40.0) / MFFU (50.0) / BluSky (34.0).
- **`core/mc/simulation.py`** (this session; `simulate_path` / `run_seed`) — outcome
  buckets `{pass, bust_daily, bust_static, bust_trailing, bust_inactivity, horizon_cap}`;
  runtime daily-loss gate already `None`-safe; `dd_type` branch chain
  static/trailing/trailing_locking; scale trigger fires off `dd_from_peak` for all types.
- **`core/mc/preflight.py`** (NEW this session, landing via **PR #356**) — `firm_kwargs`
  (None-safe tier threading + `dd_type` dispatch), `summarize_outcomes` (headline bust =
  daily+static+**trailing** with the per-seed bucket-sum==n_sims assertion — the F1
  primitive this gate's G3/G5 depend on), `assert_engine_ready` (the G3 gate). Additive,
  off the anchor import path; anchor 99.83/0.17/4.37 byte-identical.
- **`core/mc/modes.py`** (this session) — `compute_default_config`'s headline `bust_rate`
  is daily+static ONLY (never surfaces `bust_trailing`); the F1 trap this gate forbids
  reading for a prop tier.
- **`ops/prop_envelope_default.md` @ `6b94032`** (2026-07-13) — **v1.0 RATIFIED**;
  §2 `DEPLOYABLE-DEFAULT-ENVELOPE: YES/NO` contract; E1 16:00 ET default (binding min
  MFFU 16:10 ET); E2 SOFT pass/payout consistency gate; E7 overlay-only; ETF PROHIBITIVE.
- **`docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md` @ `0e26a7b`** — §4
  falsifier: ≥1 pre-registered candidate clears the bust ceiling on **≥2 of 4** FRIENDLY
  tiers, else demote to research-only; hard date 2026-11-08. §4 internal wording tension
  (H "bust ceiling" vs revert trigger "pass-rate ceiling") — **resolved here by the
  two-part ceiling** (§3: bust gate + pass floor).
- **`docs/briefs/programs/2026-07-12-survivor-scoring-and-ddp-reframe-recommendation.md` @ `263c07c`**
  — **RATIFIED 2026-07-13, §6 `RESOLVED`, no dial adjustments** (§7). This pre-registration
  transcribes its §2.1 (G0–G8), §2.2 (ceiling), §2.3 (tiers/discharge), §2.4 (freeze list),
  §4 (H-SCORE), §5 (forbidden moves). Numbers are FIXED there; not re-opened here.

**Both former freeze blockers are CLEARED** (recommendation §7): prop_envelope v1.0
ratified (2026-07-13); Tradeify/MFFU/BluSky commissions sourced into `firm_rules`
(2026-07-13). The last engine blocker — the G3 pre-flight — lands via PR #356 this session.

---

## §1 — Context (the symptom this freeze addresses)

The four-firms ADR §4 names a falsifier — "≥1 candidate clears the bust ceiling on ≥2 of
4 firm tiers" — but **the ceiling was never set and no scoring protocol exists**. Absent a
frozen gate, the first DISC-CAMP-0 survivor would be scored ad hoc, after its re-MC
numbers are already visible — the exact best-of-K / criteria-drift failure the
`programme-audit` degeneration signal #4 flags ("the disposition is written before the
evidence is assembled"). Two firm-specific engine facts make ad-hoc scoring actively
wrong: **F1** — `compute_default_config()['bust_rate']` reads ~0% for a trailing-geometry
tier (all busts route to `bust_trailing`, which the headline omits); **F2** — the
`trailing` firms (Bulenox/BluSky) model %-of-peak against fixed-$ real rules, so their
bust is optimistically understated. This pre-registration freezes the gate, the numbers,
the tier cross-section, and the F1/F2 handling **before** any survivor is scored.

Standing doctrine this connects to: four-firms ADR §4; `strategy_lifecycle.md` (a cleared
survivor admits as lifecycle CANDIDATE @1.00×); the DISC-CAMP-0 governance chain (survivors
enter this gate carrying their banked K/DSR ledger + CUSUM decay spec + Stage-8 breadth read);
`docs/methodology/regime_robustness_gate.md`.

---

## §2 — Frozen scoring protocol (G0–G8 scorecard; recommendation §2.1)

A DISC-CAMP-0 §6-RESOLVED survivor traverses, in order:

- **G0 Intake** — no firm names attached yet (envelope §2.4).
- **G1 Deployable-expression reduction (E1)** — decompose to EOD-flat per-session form;
  record round-trip count `R_deploy` + deployable/research expectancy ratio; emit
  `DEPLOYABLE-DEFAULT-ENVELOPE: YES/NO`. **NO → research-valid/non-deployable register, STOP**
  (a valid outcome, envelope §3).
- **G2 Cost-law kill gate (E5)** — parent→micro 1:10 rescale; `micro_contract_cap`
  feasibility; gross-edge vs **≥4× cost hurdle** at `R_deploy`, using
  `firm_rules.cost_per_side_usd` (now present for all four families).
- **G3 Engine pre-flight** — constraint D (None-safe threading via `preflight.firm_kwargs`)
  + the F1 bucket-sum assertion (`preflight.summarize_outcomes`) **GREEN** before any re-MC.
  Satisfied by PR #356.
- **G4 Per-firm re-MC** — deployable panel, `firm_kwargs` threaded (**never** module
  constants), **10k × 3 seeds (42/123/2026)**, horizon 1500, inactivity disabled. Run
  **TWICE** where eval consistency exists: Run-1 consistency-off, Run-2 consistency-on —
  **gate on Run-2** (consistency extends exposure; `simulation.py` consistency clause).
- **G5 Bust + pass-floor scoring** — read the headline bust via `summarize_outcomes`
  (daily+static+trailing), score vs the §3 ceiling per geometry.
- **G6 Standalone-vs-portfolio-slot routing (E2)** — concentrated edges whose Run-2 pass
  collapses are PORTFOLIO-SLOT-ONLY. Candidate #1 scores **STANDALONE** (no companion book
  exists yet).
- **G7 Funded-phase ruin + scaling diagnostic** — funded geometry (intraday for
  Tradeify/MFFU) + tightest tiers; count of tiers holding **bust ≤ 1%** is the dominant
  score term; **does NOT gate §4**.
- **G8 Admission** — clear → lifecycle **CANDIDATE @1.00×** carrying CUSUM spec + DEPLOYABLE
  annotation; becomes §4-falsifier evidence. Rail/account stay separately gated.

---

## §3 — Frozen numeric ceiling + tier cross-section (recommendation §2.2/§2.3; FIXED)

**Two-part ceiling:**

- **Part A — §4 eval gate:** headline **bust ≤ 3.0%** (daily+static+trailing) on the
  deployable expression, **Run-2**, at the $100K common band, **paired with a pass floor
  P(pass) ≥ 50%** (finite median-days-to-target inside a practical horizon). Discharged
  iff **both** hold on **≥2 distinct firms**.
- **Part B — funded ruin ceiling:** **bust ≤ 1.0%** on funded geometry — gates allocation
  **scaling**, NOT the §4 falsifier.

**Frozen tier cross-section (no post-hoc substitution):** exactly
`Bulenox_100K` · `Tradeify_Select_100K` · `MFFU_Rapid_100K` · `BluSky_Premium_100K` — all at
capital $100K, barrier 3.0%, target 6.0% held constant, isolating the genuine cross-firm
variables (DD geometry 2×trailing / 2×trailing_locking; consistency none/40/50/34%). All
other tiers are reported as **diagnostics only**; only these four gate.

**Discharge rule:** ≥2 distinct firms clear Part A, of which **≥1 MUST be `trailing_locking`
(Tradeify or MFFU)** — the engine-faithful geometry. **F2 optimism labels:** Bulenox/BluSky
(`trailing` = %-of-peak vs fixed-$ real rules; Bulenox additionally intraday vs the EOD-sum
engine) results are labeled **optimistic-lower-bounds** until a fixed-$ trailing branch (and,
for Bulenox, an intraday-excursion adjustment) exist. A Bulenox/BluSky-only pair does NOT
satisfy "≥2 of 4".

**Rationale (recorded, not re-opened):** 3.0% = the $100K band's own barrier width (a
deployable edge should bust less often than its barrier is wide); excludes falsified-book
quality (the locked-book Tradeify-100K transfer ran 17.70% bust) while not being
null-by-construction (1.0% at eval on trailing geometry demotes every program regardless of
edge quality). The pass floor closes the no-trade-grinder loophole and resolves the ADR §4
bust-vs-"pass-rate" wording tension. Operator declined the 2%/5% dials — 3.0% stands (§7 of
the recommendation).

---

## §4 — Falsifiable hypothesis (H-SCORE; recommendation §4)

**H-SCORE:** If a DISC-CAMP-0 survivor traverses G0–G5 and clears **bust ≤ 3.0% + pass floor
≥ 50%** on **≥2 distinct $100K firm tiers (≥1 `trailing_locking`)**, then the four-firms ADR
§4 falsifier is **discharged** and the survivor routes to G8 admission. **Otherwise** — no
pre-registered candidate clears any tier by **2026-11-08** — the prop program **demotes to
research-only** (configs retained; a success-eligible outcome).

**Ceiling-mis-set reject (H-SCORE calibration guard):** the §7(9) non-candidate calibration
reference is run once through the harness; **if it clears the 3.0% ceiling on ≥2 tiers, the
ceiling fails to discriminate** → close this pre-registration and re-derive the ceiling in a
fresh brief (do NOT tighten in place — Trap #12).

---

## §5 — Forbidden moves (genuinely tempting; recommendation §5)

- Reading `compute_default_config()['bust_rate']` for a prop tier (reports ~0%; **F1**) —
  use `preflight.summarize_outcomes` daily+static+trailing headline.
- Counting a Bulenox/BluSky-only pair as "≥2 of 4" without the `trailing_locking`
  requirement (optimistic-geometry cherry-pick; **F2**).
- Setting the eval ceiling at FXIFY-parity 1% (null-by-construction falsifier on trailing
  geometry).
- Post-hoc tier substitution after seeing per-tier results (best-of-K at the gate layer) —
  the four $100K tiers are frozen.
- Threading a prop tier through **module constants** instead of `firm_kwargs` (would require
  switching `ACTIVE_FIRM`, breaking anchor byte-repro).
- Switching `ACTIVE_FIRM` to run prop tiers "conveniently."
- Gating §4 on Run-1 (consistency-off) when a firm has eval consistency — Run-2 is the gate.
- Amending any number here after a re-MC result is visible (Trap #12) — close + re-open.

---

## §6 — Gate criteria (binary)

| Verdict | Trigger | Disposition |
|---|---|---|
| **RESOLVED** (falsifier DISCHARGED) | ≥1 pre-registered candidate clears Part A (bust ≤3.0% + pass ≥50%, Run-2, $100K) on **≥2 distinct firms incl. ≥1 `trailing_locking`** by 2026-11-08 | Four-firms ADR §4 falsifier discharged; survivor → G8 lifecycle CANDIDATE @1.00×; rail/account stay gated |
| **FALSIFIED** (demote-to-research-only) | No pre-registered candidate clears Part A on **any** tier by 2026-11-08 | Prop program → research-only, configs retained. H-SCORE (a deployable prop edge clears) is falsified; the outcome is operationally **success-eligible** (§7(8)) — a valid research finding, not a gate failure |
| **AMBIGUOUS** (ceiling-mis-set) | The §7(9) non-candidate calibration reference clears 3.0% on ≥2 tiers | The gate cannot discriminate — close this pre-registration; re-derive the ceiling in a fresh brief (no in-place edit; Trap #12) |

08-08 is a **progress check only** (ADR §4 tags 11-08 the hard date).

---

## §7 — Freeze list (recommendation §2.4; the nine items, frozen verbatim-in-effect)

1. **Ceiling numbers** — 3.0% eval / 1.0% funded / pass-floor **P(pass) ≥ 50%** + finite
   median inside horizon 1500. FIXED (§3).
2. **Headline-bust definition + F1 assertion** — bust = daily+static+trailing via
   `preflight.summarize_outcomes`; per-seed outcome buckets sum to `n_sims` (asserted).
3. **The four frozen tiers + discharge rule + F2 optimism labels** — §3, no substitution.
4. **E1 decomposition + `R_deploy` + ≥4× cost hurdle** — commissions sourced for all four
   firms (`firm_rules.cost_per_side_usd`; the 3-of-4 gap is CLEARED). 90-day-freshness rule
   applies (envelope §4; Bulenox Rates.pdf already stale — re-verify at any deployment fork).
5. **Per-firm `consistency_frac`** — Tradeify 40% / MFFU 50% / BluSky 34% (now in
   `firm_rules.consistency_rule_pct`; the "use envelope 40%, flagged" gap is CLEARED);
   Run-2 gating; seeds **42/123/2026**; horizon **1500**; inactivity disabled.
6. **dd_protection overlay posture** — default **OFF** (`NO_PROTECTION_TRIGGER = 10.0`) for
   scoring; any tuned per-firm `(trigger, scale)` is a **pre-registered small grid**,
   K-ledgered (per the concept-not-constant reframe, `dd_geometry` provenance-only).
7. **Regime-robustness caveat** — run the regime gate on the deployable expression before
   trusting the ceiling result (panels inherit benign-regime provenance).
8. **All-null close is success-eligible** — no candidate clears ⇒ demote-to-research-only is
   a legitimate §4 outcome, not a failure of this gate.
9. **Non-candidate calibration reference** — one pre-registered non-candidate run once
   through the harness to confirm the ceilings sit in the discriminating band (feeds §4's
   ceiling-mis-set reject).

---

## §10 — Audit hooks (runnable)

```bash
# 1. The four frozen tiers are exactly these — never silently substituted.
grep -n "Bulenox_100K\|Tradeify_Select_100K\|MFFU_Rapid_100K\|BluSky_Premium_100K" \
  docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md   # expect all 4

# 2. The ceiling numbers were not re-decided (expect 3.0% eval / 1.0% funded / 50% floor).
grep -n "3.0%\|1.0%\|P(pass) ≥ 50%\|≥ 50%" docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md

# 3. Commissions present for all four families (G2 cost gate un-blocked).
grep -c "cost_per_side_usd" core/firm_rules.py                              # expect >= 4 (one per family min)

# 4. The F1 primitive + bucket-sum assertion exist in the engine pre-flight (G3 dependency).
grep -n "summarize_outcomes\|bucket-sum\|bust_trailing" core/mc/preflight.py

# 5. Any prop harness reads headline bust via summarize_outcomes, never compute_default_config['bust_rate'].
grep -rn "bust_rate" lab/ --include="*.py" | grep -i "firm\|prop\|trailing" && echo "CHECK: prop harness reading FXIFY headline" || echo "clean"

# 6. This pre-registration was actually re-read at the gate (Trap #10 — hooks that never fire).
grep -rn "2026-07-13-prop-survivor-scoring-prereg" docs/SESSIONS.md         # the scoring session must cite it

# 7. ACTIVE_FIRM never switched to run prop tiers (anchor byte-repro guard).
grep -n "^ACTIVE_FIRM = " core/firm_rules.py                                # expect FXIFY
```

**Expected at first scoring:** all four tiers present; ceiling numbers unchanged from §3;
`cost_per_side_usd` ≥4; `summarize_outcomes` present; no prop harness reading the FXIFY
headline; `ACTIVE_FIRM=FXIFY`.

---

## Verification

```bash
# Discipline checks (mechanical)
python ~/.claude/skills/brief-authoring/scripts/check_brief.py \
  docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md --type inquire

# §0 anchors
git log -1 --format='%h %ci' -- core/firm_rules.py                                      # expect 6a0c801
git log -1 --format='%h %ci' -- ops/prop_envelope_default.md                            # v1.0 RATIFIED
git log -1 --format='%h %ci' -- docs/briefs/programs/2026-07-12-survivor-scoring-and-ddp-reframe-recommendation.md  # 263c07c

# Ceiling calibration source (falsified-book quality it must exclude)
grep -n "17.70\|17.7" lab/analysis/c1/tradeify_futures3_remc_2026-07-11/RESULTS.md

# G3 dependency (engine pre-flight)
python -c "import sys; sys.path.insert(0,'core'); from mc.preflight import summarize_outcomes, firm_kwargs; print('preflight OK')"
```
