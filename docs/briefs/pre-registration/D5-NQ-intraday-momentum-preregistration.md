# Stage-0 verdict pre-registration — D5 NQ/MNQ intraday-momentum-footprint campaign

**Status:** `STAGE-0 FROZEN · §R GO SIGNED 2026-07-15` (this file freezes the search
universe + gate thresholds + every data-derived-integer *rule* + the per-clause
reachability attestation). The HARV HARD gate (ADR 2026-07-13) is satisfied *in this
document* by §R, and the operator has **signed the §8 GO gate (2026-07-15/JA)** — so
`register_search open --lane mechanism-first --reachability-attestation <this file>`
(K_eff=1) + the subsequent cost-gated MNQ pull are now the unblocked **execution** step
(Operator + Cursor, §7 step 1). **This ratification does not itself run `register_search
open` or any pull — no K is consumed and no data is fetched by signing GO.**
**Campaign:** D5 — NQ/MNQ intraday-momentum footprint (Baltussen, Da, Lammers & Martens
2021, *JFE*). **NAS100/NQ sole anchor; DJ30/MYM dropped** (operator pin 2026-07-15).
**Lane:** mechanism-first (HARV HARD gate — ADR 2026-07-13 `Accepted`).
**Inherits:** ratified Campaign defaults ([`2026-07-11-discovery-campaign-defaults-ratified.md`](../../adr/2026-07-11-discovery-campaign-defaults-ratified.md)) + DSR K/V supersession ([`2026-07-12-dsr-k-rule-and-variance-floor-supersession.md`](../../adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md)) + HARV lane ([`2026-07-13-harv-discovery-lane-ratification.md`](../../adr/2026-07-13-harv-discovery-lane-ratification.md)) **by reference** — values snapshotted below, not re-ratified.
**Parents:** [`D5-NQ-intraday-momentum-scoping.md`](../rnd-pipeline/D5-NQ-intraday-momentum-scoping.md) (scoping) · [`Q-KBUDGET-1` closure](../closures/Q-KBUDGET-1-axis-reachability-screen.md) (`RESOLVED`; D5 PASS both clauses) · [`d5_clause_n_rescreen.md`](../../../lab/archive/q_kbudget_1_2026-07/d5_clause_n_rescreen.md).
**Loop of record:** STRATEGIC (discovery Stage-0). **Authored:** 2026-07-15 · Claude Code (Fable 5), operator-directed.

---

## §0 — Rule-0 reads (production source, verified this session 2026-07-15)

- **[`docs/briefs/rnd-pipeline/D5-NQ-intraday-momentum-scoping.md`](../rnd-pipeline/D5-NQ-intraday-momentum-scoping.md) @ `936a9e0`** — §0 operator pins (construct (i); NQ/MNQ; DJ30 drop/down-weight; K_eff ≤ 3); §1 draft H1–H3; §2 HARD-gate order; §3 forbidden; §4 next-actions (freeze = CC, §R GO/NO-GO = operator, `register_search open` = operator+Cursor). **This pre-reg executes §4 action 1 and writes the §R attestation action 2 reviews.**
- **[`lab/archive/q_kbudget_1_2026-07/d5_clause_n_rescreen.md`](../../../lab/archive/q_kbudget_1_2026-07/d5_clause_n_rescreen.md) @ `4a2471e`** — the reachability numbers this campaign inherits and does **not** re-derive: Clause K PASS at K_eff 1–3 (floor **0.65 / 0.85 / 0.98** ≤ Cap 1.0); Clause N power 0.947 at N≈1000, **δ/σ = 0.113** (Baltussen NQ cohort, t=7.97, OOS-R² 3.76%); the net-of-cost caveat (Baltussen Sharpe is gross; only SPX-futures shown to survive tick costs — NQ/YM net survival undemonstrated); DJ30-drop rationale (DIA/YM proxy ~25–60× thinner than QQQ/NQ).
- **[`lab/archive/q_kbudget_1_2026-07/d5_power.py`](../../../lab/archive/q_kbudget_1_2026-07/d5_power.py) @ `4a2471e`** — reproduces Clause K floor on production `lab/research_utils/deflated_sharpe.py`; zero pulls, zero K consumed.
- **[`docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md`](../../ltm/briefs/rnd-pipeline/discovery-campaign-template.md) @ `fad8984`** — Stage 0–8 pipeline; §Campaign-defaults #1–#6 (OOS axis, two-level K, universe correction + DSR K/V rule, temporal battery, decay-monitor-at-admission, cost gate). Values snapshotted in §2/§3 below.
- **[`docs/adr/2026-07-13-harv-discovery-lane-ratification.md`](../../adr/2026-07-13-harv-discovery-lane-ratification.md) @ `fad8984`** — §2 the HARD gate (reachability attestation blocks `register_search open`); §1 the Q-HARV-0 scar (placebo T-13→T-11 **inside** the conditioning window ⇒ RESOLVED structurally unreachable before data). §R below is designed to not repeat it.
- **[`lab/discovery/register_search.py`](../../../lab/discovery/register_search.py)** (read this session) — `open --lane mechanism-first` **rejects** a missing / not-found / **empty** `--reachability-attestation` file (lines 100–117). §R is authored as that committed non-empty file; §8 names the exact invocation.

---

## §1 — Context (the symptom this freeze addresses)

Q-KBUDGET-1 resolved D5 to a screened PASS on both clauses after the operator pinned
construct (i) — the intraday-momentum footprint (dealer short-gamma hedging → rest-of-day
return predicts the last-30-minute return), NQ/MNQ expression, DJ30 dropped. A screen PASS
**licenses campaign scoping only — it never blesses a candidate and never authorizes a
pull** (closure §6). Absent a Stage-0 freeze, the first MNQ intraday-momentum signal would
be scored after its numbers are visible, and — the load-bearing risk here — a bundled
placebo clause could be frozen **structurally unreachable**, exactly the Q-HARV-0 failure
(placebo nested inside the conditioning window, ~30–39 bp mechanical floor vs a 9.6 bp
allowance, RESOLVED impossible before data). This file freezes the universe, the gate
thresholds, every data-derived-integer rule, and — under the HARV HARD gate — a
reachability attestation for each bundled clause, **before** `register_search open`.

Standing doctrine this connects to: HARV lane HARD gate (ADR 2026-07-13); Campaign
defaults (ADR 2026-07-11) + DSR K/V (ADR 2026-07-12); `strategy_lifecycle.md` (a survivor
admits as lifecycle CANDIDATE @1.00×); `docs/methodology/regime_robustness_gate.md`.

---

## §2 — Frozen search universe + design (Stage-0)

| Item | Frozen value |
|---|---|
| **Instrument** | **MNQ** (NAS100/NQ family) sole anchor. **DJ30/MYM DROPPED** (operator pin; DIA/YM gamma proxy ~25–60× thinner than QQQ/NQ — d5_clause_n_rescreen). Single-instrument campaign. |
| **Mechanism (named, π argument)** | Dealer short-gamma intraday hedging ⇒ same-session **rest-of-day return predicts the last-30-minute return** (Baltussen et al. 2021 *JFE*). Not a rediscovery of unconditional long-only drift — the null is zero-timing conditional on the morning/rest-of-day footprint (§R hygiene). |
| **Tool ladder (mechanism-first — NOT mining)** | The pre-specified Baltussen construct only: a **single fixed** rest-of-day→last-30-min timing signal at the canonical session split. **No STUMPY / tsfresh / ruptures window search** (that is the Clause-K FAIL wide-mining class the scoping §3 forbids). No penalty/feature/window sweep. |
| **Candidate set (fixes K)** | **One primary candidate = H1** (canonical construct, canonical window). H2 (alternate session window) is **DROPPED at freeze** — it would be a second candidate raising K_eff to 2 (floor 0.85) and risks a free-window-search; adding it later requires a fresh Stage-0 freeze. **H3 is a placebo *falsification clause*, not a candidate** (consumes no selection-K). |
| **K_eff (bound now, pre-result)** | **K_eff = 1** (H1 sole candidate; family MNQ banks K_banked = 0, no closed manifest). Clause-K DSR floor at K_eff=1 = **annualized Sharpe ≥ 0.65** (the most beatable floor; reproduced d5_power.py). `V = 1/n` per Default #3 (n = OOS trade count). Min-detectable disclosed in §3. |
| **OOS axis (Default #1)** | IS + all tuning on **parent NQ 2010-01-01 : 2018-12-31**; statistical/realism OOS on **native micro MNQ 2019-05-06 : present**. Native-micro re-run is a **realism** gate, not an independence axis (same order book — Jaccard-0.96 same-path scar). |
| **Frequency / N** | One signal/session (the last-30-min timing trade) ⇒ ~10³ daily events on the declared panel (N≈1000, the Clause-N declared panel). |
| **Deployable envelope** | The construct is **inherently EOD-flat / same-session** (enter in the final window on the rest-of-day footprint, exit at session close) → E1-compliant by construction; `DEPLOYABLE-DEFAULT-ENVELOPE` expected **YES**, confirmed with the deployable round-trip count at Stage 1. |

---

## §3 — Frozen gate thresholds + data-derived-integer *rules* (Stage-0; each bound at its own pre-result step, back-filled)

Snapshot of the inherited Campaign defaults (single source of truth = the template; this is a permitted snapshot, not a competing canonical source). No override is declared — every value below is the inherited default.

| Gate | Frozen threshold / rule | Bound at |
|---|---|---|
| **Stage-2 cost-law kill** | Gross edge ≥ **4× cost hurdle** at the deployable round-trip count, using native MNQ commissions (`firm_rules.cost_per_side_usd`) + modeled slippage. | Stage 2 |
| **Confirm / DSR (Clause-K floor)** | **Net-of-cost annualized Sharpe ≥ 0.65** on the OOS era (the DSR ≥ 0.95 threshold at K_eff = 1, V = 1/n). This is the campaign HARD quality bar (scoping §2.5). **Min-detectable disclosure (Default #3, pre-freeze):** at K_eff=1, V=1/n, the bound requires a per-trade Sharpe whose annualization clears 0.65 — the plausible-true world (§R.1) shows this is reachable; the *net* MNQ realization is what the campaign tests. | Stage 6 |
| **Universe correction** | SPA/StepM degenerate at K=1 (single candidate — reported, not gating); **DSR ≥ 0.95** is the operative universe gate; **PBO < 0.5** via CPCV (`n_folds=10, n_test_folds=8`) **only if** any config selection occurs (none planned — single fixed construct ⇒ PBO N/A, stated). | Stage 6 |
| **Block size** | Set from the **IS return-series ACF** (never `sqrt(T)`); for a daily-frequency timing signal, expected small (≈1–5 bd) — **value bound at Stage 5, back-filled here**, not guessed now. | Stage 5 |
| **Temporal-consistency battery (Default #4)** | Sub-era **sign** consistency ≥ ⌈0.7·Y⌉ of Y OOS calendar-year sub-eras positive; **drop-top-year** (edge > gate with best year removed); **regime-slice survival** (ruptures/HMM labels are **test conditions, never filters** — Q-REGIME-COND-1 scar); **CUSUM** on the candidate's own OOS edge series. | Stage 6 |
| **Decay monitor (Default #5)** | Inadmissible without a **CUSUM decay-monitor spec whose null was calibrated during validation** (Stage-6d death certificate). | Admission |
| **Cost gate (Default #6)** | Declared **`--max-cost`** checked against the summed `db_fetch estimate` before any pull; first run inside the **$125 free-credit** window. MNQ intraday-bar scope only. | Stage 1 |
| **Breadth (Stage 8)** | 5th-column ENB / cross-leg-correlation delta vs the locked 4-leg frame (reproduce the Q-NEFF-1 anchor first) + the mechanistic-exposure declaration (side; entry-session window ET; in-market min/yr; per-leg structural overlap). Episodic (in-market < 5% of session clock) ⇒ realized-corr not sufficient for breadth admission. | Stage 8 |

---

## §R — Reachability attestation (HARV HARD gate, ADR 2026-07-13 §2 — the load-bearing section)

**Requirement (verbatim intent):** simulate every bundled clause under a *plausible-true
world*; a clause structurally un-passable under a true-mechanism world must be redesigned
or dropped **pre-freeze**. H1-style power disclosure on the primary alone is insufficient
(Q-HARV-0). Two clauses are bundled: **R.1** the H1 confirm gate, **R.2** the H3 placebo
gate.

### R.1 — H1 confirm gate (net-of-cost annualized Sharpe ≥ 0.65) — **REACHABLE**

*Plausible-true world:* the Baltussen NQ effect is real at the cohort-cited central
magnitude (δ/σ = 0.113 conservative t-scaled reading; OOS-R² 3.76% ⇒ IC upper bound 0.194)
**and** survives native MNQ micro costs.

- Gross annualized Sharpe under the **conservative** central effect ≈ 0.113 × √252 ≈ **1.79**
  (under the R² upper-bound IC 0.194 ≈ 3.08). The confirm floor is **0.65**.
- The effect would have to lose **~64%** of its conservative gross Sharpe to costs to fall
  below 0.65 — a large but not structurally-forced haircut. **A plausible-true world where
  net ≥ 0.65 clears therefore exists** ⇒ the gate is **not** un-passable by construction.
- **Contrast the un-reachable case:** DISC-CAMP-0's Clause-K floor was **2.05** (family bank
  3,177) — above even the gross 1.79, so no plausible-true world passed; that campaign's
  floor was unreachable. D5's floor 0.65 sits **below** the gross effect ⇒ reachable. This
  is exactly the low-K regime the M-19 floor is beatable in (rescreen).
- **Honest caveat carried forward (not a reachability failure):** reachability means *a
  true world can pass*, **not** *it will pass*. NQ/MNQ net-of-cost survival is undemonstrated
  in the literature (only SPX-futures shown to survive tick costs); the Stage-6 confirm gate
  is where the *net* MNQ realization is adjudicated. §R attests the gate is passable, not
  that the effect is real.

**R.1 verdict: REACHABLE** (floor 0.65 < conservative gross 1.79).

### R.2 — H3 placebo gate — **REACHABLE** (and explicitly not the Q-HARV-0 geometry)

*Placebo construction (frozen):* **shuffled-day** placebo — predict this session's
last-30-min return from a **different, randomly-permuted session's** rest-of-day footprint
(break the same-day morning→close link). *Placebo gate:* the shuffled-day placebo effect is
**not significant at the primary's α AND its magnitude < 50% of the H1 effect**.

- *Plausible-true world:* under the dealer-hedging mechanism, this-session hedging flow is
  what links this session's rest-of-day to its own close; a **different** day's footprint
  has **no** mechanistic link to this day's close ⇒ the shuffled-day placebo is expected
  **≈ 0**. The gate (placebo ≈ null) is therefore comfortably passed under a true world.
- **The Q-HARV-0 scar is structurally avoided:** the failure there was placebo window
  **⊂ conditioning window** (T-13→T-11 inside the conditioning span), forcing a ~30–39 bp
  mechanical carryover floor above the 9.6 bp allowance. Here the placebo uses a **disjoint
  session's** footprint — there is **no window overlap** and **no mechanical carryover
  floor** to breach the allowance. `placebo_window ∩ conditioning_window = ∅` **by
  construction** (different calendar day). The allowance (< 50% of the H1 effect, and
  non-significance) is sized so a plausible-true world (placebo ≈ 0) clears with wide margin.

**R.2 verdict: REACHABLE** (no conditioning-overlap floor; placebo null-by-mechanism under a true world).

**Attestation conclusion:** both bundled clauses are reachable under a plausible-true world;
no clause is structurally un-passable before data. This file is the non-empty
`--reachability-attestation` artifact `register_search open --lane mechanism-first` requires.

---

## §4 — Falsifiable hypothesis (H-D5; binary)

**H-D5 — if** the fixed MNQ intraday-momentum construct (H1), scored on the native-micro
OOS era (2019-05-06→present) under the frozen gates, delivers **net-of-cost annualized
Sharpe ≥ 0.65** (DSR ≥ 0.95 at K_eff=1) **AND** clears the temporal-consistency battery
(sign ≥ ⌈0.7·Y⌉, drop-top-year, CUSUM, regime-slice-as-test) **AND** the shuffled-day
placebo (H3) stays null per the §R.2 gate, **then** D5 is a confirmed candidate → routes to
Stage-7 realism + Stage-8 breadth + lifecycle CANDIDATE @1.00× intake; **otherwise** D5
closes (all-null close is success-eligible — banks the MNQ family cumulative K + the
process-defect log, per Default #8 analogue).

**Reject/accept threshold (numeric):** accept iff net-of-cost annualized Sharpe ≥ 0.65 on
the OOS era with the placebo null and the temporal battery cleared. **H-D5 is falsified**
on any of: net Sharpe < 0.65, placebo fires (§R.2 gate breached), or the
sign/drop-top-year/CUSUM battery fails — the FALSIFIED disposition of §6.

---

## §5 — Forbidden moves (each genuinely tempting)

- **Opening the search / pulling data before this freeze + §R are committed and the operator
  GOes** — freeze-order is git-checkable; a pull before `register_search open` voids the campaign (Default discipline).
- **Widening to a STUMPY/tsfresh window search** because a single fixed construct "might miss
  the best window" — that is the Clause-K FAIL wide-mining class (scoping §3); it would blow
  K_eff past 3 and void the screen PASS.
- **Re-introducing H2 (alternate window) after seeing H1's result** — a post-hoc second
  candidate is a free search; K was bound at 1 pre-result. A genuine second window needs a
  fresh Stage-0 freeze.
- **Re-litigating the gamma-*sign* mechanism (construct ii) as a silent third hypothesis** —
  it stays UNSCREENABLE (no NDX/Dow cohort); the operator pinned construct (i).
- **Re-adding the DJ30/MYM leg** — dropped by operator pin (DIA/YM proxy too thin); adding it
  is a fresh axis, not this campaign.
- **Nesting the placebo inside the conditioning window** (the Q-HARV-0 geometry) — §R.2 freezes
  the disjoint-session placebo precisely to prevent it.
- **Quoting the Clause-N power 0.947 or the Baltussen gross Sharpe as tradeable net edge** —
  they are the statistical footprint; the Stage-6 net-of-cost gate is the real test (rescreen caveat).
- **Amending any threshold here after a result is visible** (Trap #12) — close + re-open a fresh Stage-0.

---

## §6 — Gate criteria (binary)

| Verdict | Trigger | Disposition |
|---|---|---|
| **RESOLVED** (candidate confirmed) | Net-of-cost annualized Sharpe ≥ 0.65 on OOS AND placebo null (§R.2) AND temporal battery cleared | Route to Stage-7 realism → Stage-8 breadth → lifecycle CANDIDATE @1.00×; feeds the 08-08→11-08 slate as a live candidate |
| **FALSIFIED** (all-null) | Net Sharpe < 0.65 OR placebo fires OR temporal battery fails | Close; bank MNQ family cumulative K + defect log; success-eligible research outcome |
| **AMBIGUOUS** | Instrument cannot discriminate (e.g. OOS trade count too low for a stable Sharpe estimate — Default #3 `dsr_unreachable_low_n`) | Closure names the re-test condition; no in-place threshold edit |

08-08 is a **progress check**; the campaign's own confirm run is the hard adjudication (no calendar hard-date is imposed here beyond the parent programme's 11-08).

---

## §7 — Run protocol (maps to the template Stage pipeline; gated at each step)

0. **Stage 0 (this file):** universe + gates + integer-rules + §R frozen. **Operator reviews §R → GO/NO-GO** (scoping §4 action 2).
1. **On GO:** `register_search open --lane mechanism-first --reachability-attestation <this file> --tool baltussen-fixed --search-space-size 1 --data-window 2010-01-01:2018-12-31 --hypothesis "..."` (binds K_eff=1). **Then** `db_fetch estimate` → cost-gate check → `pull` (MNQ intraday bars; $125 window).
2. **Stage 2** cost-law kill (≥4× hurdle). **Stage 4** IS edge series (single fixed construct). **Stage 5** block size from IS ACF. **Stage 6** DSR ≥ 0.95 (Sharpe ≥ 0.65) + temporal battery + placebo §R.2, on OOS. **Stage 7** MNQ realism. **Stage 8** breadth + exposure declaration.
3. **Admission** only from RESOLVED: lifecycle CANDIDATE @1.00× with the Stage-6d decay monitor.

Results land in `lab/analysis/` under a dated slug citing this pre-registration by path.

---

## §8 — Operator GO gate (the §4-action-2 decision; DRAFT until filled)

```
§R REVIEWED / GO: 2026-07-15 / JA
Confirms both bundled clauses REACHABLE (R.1 confirm ≥0.65 reachable; R.2 placebo disjoint-session, no conditioning overlap).
Authorizes `register_search open --lane mechanism-first` (K_eff=1) and the subsequent cost-gated MNQ pull.
NO register_search open and NO Databento pull before this block is filled.  ← now filled; §7-step-1 execution (Operator + Cursor) is unblocked.
```

---

## §10 — Audit hooks (runnable)

```bash
# 1. Freeze-before-open: while GO is unfilled, no register_search ledger entry and no pull may exist for D5.
grep -n "§R REVIEWED / GO: ____________" docs/briefs/pre-registration/D5-NQ-intraday-momentum-preregistration.md \
  && echo "GO unfilled — register_search open + pull must NOT have run" || echo "GO filled"

# 2. The reachability attestation is non-empty (register_search open rejects empty).
test -s docs/briefs/pre-registration/D5-NQ-intraday-momentum-preregistration.md && echo "attestation non-empty OK"

# 3. Both clauses attested REACHABLE (HARD gate satisfied in-file). Anchor on the bold
#    body form so this grep does not match its own line (M-AHF discipline).
grep -c "\*\*R\.[12] verdict: REACHABLE\*\*" docs/briefs/pre-registration/D5-NQ-intraday-momentum-preregistration.md  # expect 2

# 4. Placebo is disjoint-session, not nested in conditioning (Q-HARV-0 scar avoided).
#    The R.2 body carries the empty-intersection set equation.
grep -n "placebo_window . conditioning_window = " docs/briefs/pre-registration/D5-NQ-intraday-momentum-preregistration.md  # expect 1 (R.2 body)

# 5. K bound at 1 pre-result; DJ30 dropped; construct (i) only.
grep -n "K_eff = 1\|DJ30/MYM DROPPED\|construct (i)" docs/briefs/pre-registration/D5-NQ-intraday-momentum-preregistration.md

# 6. Inherited defaults referenced, not re-ratified (no override declared).
grep -n "inherits.*by reference\|No override is declared" docs/briefs/pre-registration/D5-NQ-intraday-momentum-preregistration.md

# 7. register_search HARD-gate flag exists in production (the gate this file feeds).
grep -n "reachability-attestation" lab/discovery/register_search.py | head -2
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python scripts/check_brief.py docs/briefs/pre-registration/D5-NQ-intraday-momentum-preregistration.md --type inquire

# §0 anchors
git log -1 --format='%h %ci' -- docs/briefs/rnd-pipeline/D5-NQ-intraday-momentum-scoping.md     # 936a9e0
git log -1 --format='%h %ci' -- lab/archive/q_kbudget_1_2026-07/d5_clause_n_rescreen.md        # 4a2471e
git log -1 --format='%h %ci' -- docs/adr/2026-07-13-harv-discovery-lane-ratification.md         # fad8984

# Clause-K floor + Clause-N power reproduce (zero pulls, zero K)
python lab/archive/q_kbudget_1_2026-07/d5_power.py   # expect floor 0.65/0.85/0.98; power 0.947

# register_search rejects an empty attestation (the gate is real)
grep -n "file empty" lab/discovery/register_search.py
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-15 | Stage-0 FROZEN — universe (MNQ sole, DJ30 dropped), K_eff=1 (H1 sole candidate; H2 dropped), gates snapshotted from inherited defaults, §R reachability attestation (R.1 confirm REACHABLE, R.2 disjoint-session placebo REACHABLE). Awaiting operator §R GO before `register_search open` / any pull. | Joshua (direction) + Claude Code (Fable 5) |
| 2026-07-15 | **§R GO signed (§8, JA)** — both clauses confirmed REACHABLE; `register_search open` + cost-gated MNQ pull unblocked as the Operator+Cursor execution step. GO signature consumes no K and fetches no data. | Joshua (GO) |
