# Pre-registration v2 — Prop survivor scoring gate (four-firms ADR §4 falsifier)

**FROZEN 2026-08-26.** No item below changes after a result is seen — same discipline as v1
(Known Trap #12: amendments after a result require closing this pre-registration and opening a
fresh one). This version's own §8 documents in full why it exists and does not pretend to be
anything other than what it is: an operator risk-tolerance override, not a re-derivation finding
the old ceiling was wrong.

**Status:** FROZEN / not-yet-exercised. No DISC-CAMP-0 survivor has been scored under this
version. Same build-ahead-of-candidate posture as v1.
**Loop of record:** STRATEGIC
**Feeds:** the four-firms ADR §4 falsifier (hard date **2026-11-08**; 08-08 was a progress check
only — unaffected by this version).
**Supersedes:** [`2026-07-13-prop-survivor-scoring-prereg.md`](2026-07-13-prop-survivor-scoring-prereg.md)
in full (Part A eval ceiling 3.0% → 5.0% only — see §3). That file's own §0–§7 body stays frozen
as the historical record of the original ceiling and its rationale; nothing in it was wrong, and
this version does not claim otherwise.
**Authored:** 2026-08-26 · Claude Code (Sonnet 5), operator-directed and operator-reviewed.

---

## §0 — Rule-0 reads (re-verified this session, 2026-08-26 — not copied from v1)

v1's §0 reads are 44 days old; re-checked rather than trusted:

- **`core/firm_rules.py`** — `Tradeify_Select_100K`/`Tradeify_Select_150K`/`Bulenox_100K`/
  `MFFU_Rapid_100K`/`BluSky_Premium_100K` all still present with `max_dd_pct: 3.0`,
  `profit_target_pct: 6.0`; `dd_type` split unchanged (Bulenox/BluSky `trailing`,
  Tradeify/MFFU `trailing_locking`); all four commissions still sourced. `ACTIVE_FIRM` selector
  was **deleted** (challenge-era substrate retirement, 2026-07-22) — v1's audit hook 7 (`grep -n
  "^ACTIVE_FIRM = "`, expect `FXIFY`) is now moot, not failing; no prop harness reads it, so this
  does not affect anything this gate depends on.
- **`core/mc/preflight.py`** — `firm_kwargs`, `summarize_outcomes` (daily+static+trailing
  headline, per-seed bucket-sum assertion), `assert_engine_ready` all present and unchanged in
  signature since v1.
- **`lab/discovery/prop_survivor_scoring.py`** — `load_scoring_thresholds` parses the same six
  regex patterns v1 relied on (eval ceiling, funded ceiling, pass floor, four tier names, seeds,
  sims, horizon, cost hurdle) from whatever `DEFAULT_PREREG` points at. This version's §3 below
  is phrased to match every one of those patterns byte-for-byte except the eval-ceiling number
  itself — verified by running `load_scoring_thresholds` against this file directly before
  freezing (see §10 audit hook 8).
- **No DISC-CAMP-0 survivor has ever been scored under any version of this gate** — confirmed via
  `docs/SESSIONS.md` / `lab/CATALOG.md`: `register_search` for the first live campaign has not
  opened. This is still a build-ahead-of-candidate freeze, same posture as v1, not a live-result
  re-derivation.
- **The measured result motivating this reopening — corrected 2026-08-26, pre-merge (the number
  below moved after this section was first drafted; this is the current, verified figure, not the
  one the operator's own §1 quote was made against):**
  [`lab/analysis/c1/aegis_orbmnq_combined_book_2026-08-26/RESULTS.md`](../../../lab/analysis/c1/aegis_orbmnq_combined_book_2026-08-26/RESULTS.md)
  §10.2 — Aegis-6J1 + ORB-MNQ-1 combined-book, 3yr flagship, tail-risk-consistent sizing +
  timestamp-sequenced intraday-honest remeasure, split both-halves: **h1 3.29% / h2 5.37%**
  (full-window pooled 5.03%). This supersedes the single pooled §9.3 figure (4.34%) this section
  originally cited — that number was itself already superseded by the time this document was
  authored (a proxy-based intraday remeasure, §9.3, not the timestamp-sequenced one in §10.1) and
  was never split both-halves, which this repo's own regime-robustness convention (§7 item 7,
  unchanged from v1) treats as required before trusting any ceiling result. Read both-halves, this
  exact study does **not** clear even the raised 5.0% ceiling (h2 5.37% > 5.0%) — see §1 for what
  this does and does not change about the ruling itself. This is an **EXPLORATORY** study (not
  pre-registered, not DISC-CAMP-0, not itself gated by this ceiling) — it does not admit anything
  by clearing (or failing to clear) any bar; it is cited here only as the fact that prompted this
  reopening, per §8's full disclosure.

---

## §1 — Context (why this version exists — full disclosure, not a re-derivation claim)

This is **not** a finding that v1's 3.0% ceiling was mis-set. v1's own §3 rationale — *"3.0% = the
$100K band's own barrier width... excludes falsified-book quality... while not being
null-by-construction"* — is not disputed and is not re-argued here. What changed is the operator's
own risk tolerance, stated directly: *"4.34% bust is acceptable, I am raising the minimum bar to
5%. that is still much lower than what real traders experience."* **Quote preserved verbatim — do
not edit what was said.** The 4.34% figure named in it was the correctly-cited current number at
the moment the quote was made; it was independently revised twice more the same day by a different
session (§9.3 proxy → §10.1 timestamp-sequenced → §10.2 both-halves split, landing at h1 3.29% /
h2 5.37%, both-halves FAIL — see §0's corrected citation). **This does not reopen or restate the
ruling itself** — §8 already frames the ceiling move as a general risk-tolerance dial, not a
verdict on any one candidate, and that framing holds regardless of which number the study
eventually settled on. What it does mean: the specific study that prompted the same-day reopening
turned out, on the most rigorous test available, not to clear the raised bar either. Recorded here
because omitting it would be exactly the kind of selective citation §8 already commits this
document not to do.

**This reopening is same-day as, and explicitly informed by, a result that failed the old
ceiling.** That is ordinarily exactly the pattern Known Trap #12 exists to block, and it does not
stop being that pattern just because this document says so. What makes this a legitimate use of
the close-and-reopen path rather than a violation of it: v1's own freeze list (§7 item 8) already
names "all-null close is success-eligible" and the whole gate as a **risk-tolerance calibration**,
not a claim about where the "true" edge threshold sits — moving a risk-tolerance dial on operator
judgment is a different act from re-deriving a mis-calibrated number to manufacture a pass. §8
below is the load-bearing section that makes that distinction concrete and checkable, rather than
asserted.

---

## §2 — Scoring protocol (G0–G8 scorecard) — UNCHANGED from v1, reproduced for a single source of truth

*(Identical to v1 §2. Reproduced, not re-derived — no step, gate, or order changes.)*

A DISC-CAMP-0 §6-RESOLVED survivor traverses, in order:

- **G0 Intake** — no firm names attached yet (envelope §2.4).
- **G1 Deployable-expression reduction (E1)** — decompose to EOD-flat per-session form;
  record round-trip count `R_deploy` + deployable/research expectancy ratio; emit
  `DEPLOYABLE-DEFAULT-ENVELOPE: YES/NO`. **NO → research-valid/non-deployable register, STOP**
  (a valid outcome, envelope §3).
- **G2 Cost-law kill gate (E5)** — parent→micro 1:10 rescale; `micro_contract_cap`
  feasibility; gross-edge vs **≥4× cost hurdle** at `R_deploy`, using
  `firm_rules.cost_per_side_usd`.
- **G3 Engine pre-flight** — constraint D (None-safe threading via `preflight.firm_kwargs`)
  + the F1 bucket-sum assertion (`preflight.summarize_outcomes`) **GREEN** before any re-MC.
- **G4 Per-firm re-MC** — deployable panel, `firm_kwargs` threaded (**never** module
  constants), **10k × 3 seeds (42/123/2026)**, horizon 1500, inactivity disabled. Run
  **TWICE** where eval consistency exists: Run-1 consistency-off, Run-2 consistency-on —
  **gate on Run-2** (consistency extends exposure; `simulation.py` consistency clause).
- **G5 Bust + pass-floor scoring** — read the headline bust via `summarize_outcomes`
  (daily+static+trailing), score vs the §3 ceiling per geometry.
- **G6 Standalone-vs-portfolio-slot routing (E2)** — concentrated edges whose Run-2 pass
  collapses are PORTFOLIO-SLOT-ONLY.
- **G7 Funded-phase ruin + scaling diagnostic** — funded geometry (intraday for
  Tradeify/MFFU) + tightest tiers; count of tiers holding **bust ≤ 1%** is the dominant
  score term; **does NOT gate §4**.
- **G8 Admission** — clear → lifecycle **CANDIDATE @1.00×** carrying CUSUM spec + DEPLOYABLE
  annotation; becomes §4-falsifier evidence. Rail/account stay separately gated.

---

## §3 — Numeric ceiling + tier cross-section (Part A changed; everything else UNCHANGED from v1)

**Two-part ceiling:**

- **Part A — §4 eval gate:** headline **bust ≤ 5.0%** (daily+static+trailing) on the
  deployable expression, **Run-2**, at the $100K common band, **paired with a pass floor
  P(pass) ≥ 50%** (finite median-days-to-target inside a practical horizon). Discharged
  iff **both** hold on **≥2 distinct firms**. *(Changed from 3.0% — see §8.)*
- **Part B — funded ruin ceiling:** **bust ≤ 1.0%** on funded geometry — gates allocation
  **scaling**, NOT the §4 falsifier. *(Unchanged — this ruling did not address funded-phase
  scaling risk; out of scope for this reopening. Raising Part A does not raise Part B.)*

**Frozen tier cross-section (no post-hoc substitution, unchanged from v1):** exactly
`Bulenox_100K` · `Tradeify_Select_100K` · `MFFU_Rapid_100K` · `BluSky_Premium_100K` — all at
capital $100K, barrier 3.0%, target 6.0% held constant, isolating the genuine cross-firm
variables (DD geometry 2×trailing / 2×trailing_locking; consistency none/40/50/34%). All
other tiers are reported as **diagnostics only**; only these four gate.

**Discharge rule (unchanged):** ≥2 distinct firms clear Part A, of which **≥1 MUST be
`trailing_locking`** (Tradeify or MFFU). **F2 optimism labels (unchanged):** Bulenox/BluSky
results stay labeled **optimistic-lower-bounds** until a fixed-$ trailing branch exists. A
Bulenox/BluSky-only pair does NOT satisfy "≥2 of 4".

**Rationale for 5.0% (see §8 for the full, disclosed reasoning — not re-summarized here to avoid
a shorter, cleaner-sounding version of §8 that omits its caveats).**

---

## §4 — Falsifiable hypothesis (H-SCORE) — same shape, updated number

**H-SCORE:** If a DISC-CAMP-0 survivor traverses G0–G5 and clears **bust ≤ 5.0% + pass floor
≥ 50%** on **≥2 distinct $100K firm tiers (≥1 `trailing_locking`)**, then the four-firms ADR
§4 falsifier is **discharged** and the survivor routes to G8 admission. **Otherwise** — no
pre-registered candidate clears any tier by **2026-11-08** — the prop program **demotes to
research-only** (configs retained; a success-eligible outcome). *(2026-11-08 hard date
unchanged — this reopening does not touch the falsifier's own deadline.)*

**Ceiling-mis-set reject (unchanged mechanism, unchanged from v1 in kind):** the same non-candidate
calibration reference, re-run once through the harness at the new ceiling; if it clears 5.0% on
≥2 tiers, the ceiling fails to discriminate → close this pre-registration and re-derive in a fresh
brief (do NOT tighten in place — Trap #12, same rule this version itself was created under).

---

## §5 — Forbidden moves — same as v1, plus one new item this reopening itself creates

*(v1's original list, unchanged):*

- Reading `compute_default_config()['bust_rate']` for a prop tier (reports ~0%; F1).
- Counting a Bulenox/BluSky-only pair as "≥2 of 4" without the `trailing_locking` requirement.
- Setting the eval ceiling at FXIFY-parity 1% (null-by-construction falsifier on trailing
  geometry).
- Post-hoc tier substitution after seeing per-tier results — the four $100K tiers are frozen.
- Threading a prop tier through module constants instead of `firm_kwargs`.
- Switching firm selection to run prop tiers "conveniently."
- Gating §4 on Run-1 (consistency-off) when a firm has eval consistency — Run-2 is the gate.
- Amending any number here after a re-MC result under **this version** is visible (Trap #12) —
  close + re-open again, same as this version itself did to v1.

*(New, specific to this reopening):*

- **Citing this version's existence as precedent for a future same-session ceiling move.** This
  reopening is disclosed as an operator override on stated grounds (§8), not as an established
  new norm that ceilings move whenever a candidate result is close. A future request to move this
  ceiling again needs its own independently-stated grounds — not "we did it once before."
- **Reading any bust figure from `aegis_orbmnq_combined_book_2026-08-26`'s campaign (4.34%, the
  §10.2 both-halves 3.29%/5.37%, or any later revision) as itself having cleared any gate, at
  either the 3.0% or 5.0% ceiling.** That study is EXPLORATORY, not pre-registered, not
  DISC-CAMP-0 — it is the trigger for this reopening, not evidence admitted under it. On its own
  most rigorous test to date (§10.2, both-halves) it does not clear 5.0% either (h2 5.37%).

---

## §6 — Gate criteria (binary) — same shape, updated number

| Verdict | Trigger | Disposition |
|---|---|---|
| **RESOLVED** (falsifier DISCHARGED) | ≥1 pre-registered candidate clears Part A (bust ≤5.0% + pass ≥50%, Run-2, $100K) on **≥2 distinct firms incl. ≥1 `trailing_locking`** by 2026-11-08 | Four-firms ADR §4 falsifier discharged; survivor → G8 lifecycle CANDIDATE @1.00×; rail/account stay gated |
| **FALSIFIED** (demote-to-research-only) | No pre-registered candidate clears Part A on **any** tier by 2026-11-08 | Prop program → research-only, configs retained. Success-eligible (§7(8) below), same as v1 |
| **AMBIGUOUS** (ceiling-mis-set) | The non-candidate calibration reference clears 5.0% on ≥2 tiers | The gate cannot discriminate — close this pre-registration; re-derive the ceiling in a fresh brief (no in-place edit; Trap #12) |

2026-11-08 hard date unchanged. 08-08 progress-check note is moot (already past).

---

## §7 — Freeze list — same nine items, item 1 updated

1. **Ceiling numbers** — **5.0%** eval (was 3.0%) / 1.0% funded (unchanged) / pass-floor
   **P(pass) ≥ 50%** (unchanged) + finite median inside horizon 1500 (unchanged). FIXED (§3, §8).
2. **Headline-bust definition + F1 assertion** — unchanged from v1.
3. **The four frozen tiers + discharge rule + F2 optimism labels** — unchanged from v1.
4. **E1 decomposition + `R_deploy` + ≥4× cost hurdle** — unchanged from v1.
5. **Per-firm `consistency_frac`** — unchanged from v1 (Tradeify 40% / MFFU 50% / BluSky 34%;
   Run-2 gating; seeds 42/123/2026; horizon 1500; inactivity disabled).
6. **dd_protection overlay posture** — unchanged from v1 (default OFF for scoring).
7. **Regime-robustness caveat** — unchanged from v1.
8. **All-null close is success-eligible** — unchanged from v1.
9. **Non-candidate calibration reference** — unchanged from v1 mechanism; must be re-run at the
   new 5.0% ceiling before first scoring (v1's own reference run, if any was ever performed, does
   not carry over — it tested discriminability at 3.0%, a different question).

---

## §8 — Decision driver: operator risk-tolerance override (the load-bearing section)

This section exists because v1 has no equivalent — v1 needed none, since it was never amended.
This is the section a future audit should read first if it ever questions this reopening's
legitimacy.

**This is an override, not a re-derivation.** Precedent for the form: `docs/methodology/
regime_robustness_gate.md`'s 2026-05-08 postscript — *"Joshua subsequently adopted C2 anyway, on
broker-feed-resolution + median-pass-time grounds... The gate's regime-fragility signal was
preserved as dissent, with a forward revert trigger."* Same shape here: v1's own reasoning stands,
unedited, as the frozen record of what a first-principles derivation produced (3.0%, tied to the
$100K band's own barrier width). This version does not refute it. The operator is choosing to
accept more modeled risk than that derivation would license, on separately-stated grounds below —
exactly as C2 was adopted over the regime gate's own fragility finding, not because the finding
was wrong.

**Disclosure the operator may not have had at the time of the directive:** v1 §3's own rationale
paragraph states *"Operator declined the 2%/5% dials — 3.0% stands"* (2026-07-13). **5.0% was
already offered and explicitly declined once.** This reopening reverses that specific prior
decision, at the same number, on the same day a result failed the lower bar. Recorded here in
full rather than omitted, because omitting it would make this document's own evidentiary standard
worse than the thing it is supposed to be protecting.

**Grounds stated by the operator:** *"that is still much lower than what real traders experience."*
Independently researched this session (not verified against primary sources by re-fetching every
one; treat exact decimals as secondary where noted):

- **EU CFDs — ESMA product-intervention decision (ESMA71-98-128, 2018-03-23):** national-regulator
  analyses found **74%–89%** of retail CFD accounts lose money over the measured window (window
  not uniform across jurisdictions); average loss €1,600–€29,000.
- **UK CFDs — FCA COBS 22.5 disclosures** (mandatory trailing-12-month, per-firm, in force since
  PS19/18): 2025 published figures span roughly **46%–76%+** of accounts losing money, most
  clustering 60–80%.
- **US retail forex — NFA/CFTC-mandated quarterly disclosure:** one FDM's (FOREX.com) public
  quarterly figures showed roughly **66%–74% unprofitable** through 2025; exact cells
  secondary-sourced (primary disclosure page fetch blocked), order of magnitude well corroborated.
- **Academic — Barber, Lee, Liu & Odean, "The Cross-Section of Speculator Skill," Review of
  Financial Studies 2014:** Taiwan futures day traders 1992–2006, typical 6-month period, **>80%**
  lost money after costs; **<1%** of the day-trading population earns predictable positive
  after-fee returns.
- **Prop-firm challenges — FPFX Tech analysis via Finance Magnates, Sept 2024** (vendor/press
  dataset, weaker standing than the above four): 300,000+ accounts across 10 prop firms, **14%**
  pass evaluation, **7%** ever reach payout.

**Comparability caveat (do not read past this):** none of these map cleanly onto "probability of
hitting a rule-defined drawdown breach in one bounded MC-modeled eval attempt." The first four
measure net-P&L-below-zero for ongoing, self-funded discretionary accounts over rolling
12-month/quarterly windows — a different denominator and time horizon than a single eval's bust
probability, aggregating skill, behavior, and cost drag rather than a specific sizing/DD rule. The
fifth is structurally closer (bounded challenge, firm-defined rule) but conflates first-attempt
failures, re-attempts, and traders who never seriously tried, and is self-reported to a fintech
vendor rather than regulator-filed. All five describe **discretionary** populations; the candidates
this gate screens are **systematic**. These figures support the directional claim (5% is far below
every cited figure) but do not establish a quantitative equivalence between this gate's bust-rate
definition and any of the cited loss-rate definitions. Citing "70–90% of traders lose money" as
though it were the same measurement as this gate's Part A bust rate would be exactly the kind of
category error this repo's own sourcing discipline exists to catch — noted here so a future reader
does not make it by skimming past this paragraph to the numbers above it.

**What would falsify this override, not just this gate:** if a future audit finds that 5.0% (vs.
3.0%) materially changes which candidates get admitted in a way that correlates with edge quality
rather than risk tolerance — i.e., candidates admitted only at 5.0% turn out to be systematically
worse survivors — that is evidence the ceiling move itself degraded the gate's discriminating
power, not just widened it, and should trigger a fresh review of this decision on its own terms
(not an automatic revert).

---

## §9 — Audit hooks (runnable)

```bash
# 1. The four frozen tiers are exactly these — never silently substituted.
grep -n "Bulenox_100K\|Tradeify_Select_100K\|MFFU_Rapid_100K\|BluSky_Premium_100K" \
  docs/briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md   # expect all 4

# 2. The ceiling numbers read as this version froze them (5.0% eval / 1.0% funded / 50% floor).
grep -n "5.0%\|1.0%\|P(pass) ≥ 50%\|≥ 50%" docs/briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md

# 3. v1 carries the closure pointer to this file (not silently orphaned).
grep -n "CLOSED 2026-08-26" docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md

# 4. DEFAULT_PREREG points at this file, not v1.
grep -n "2026-08-26-prop-survivor-scoring-prereg-v2" lab/discovery/prop_survivor_scoring.py

# 5. The declined-5%-dial disclosure is present (the load-bearing honesty check).
grep -n "already offered and explicitly declined" docs/briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md

# 6. This pre-registration was actually re-read at the gate (Trap #10 — hooks that never fire).
grep -rn "2026-08-26-prop-survivor-scoring-prereg-v2" docs/SESSIONS.md         # the scoring session must cite it

# 7. Loader parses this file without error and returns the expected numbers.
python -c "
import sys; sys.path.insert(0, 'lab'); sys.path.insert(0, 'core')
from discovery.prop_survivor_scoring import load_scoring_thresholds
from pathlib import Path
t = load_scoring_thresholds(Path('docs/briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md'))
assert t.eval_bust_ceiling == 0.05, t.eval_bust_ceiling
assert t.funded_bust_ceiling == 0.01, t.funded_bust_ceiling
assert t.pass_floor == 0.50, t.pass_floor
print('OK', t)
"

# 8. DEFAULT_PREREG itself now loads to 0.05, matching hook 4+7 together.
python -c "
import sys; sys.path.insert(0, 'lab'); sys.path.insert(0, 'core')
from discovery.prop_survivor_scoring import load_scoring_thresholds, DEFAULT_PREREG
t = load_scoring_thresholds()
assert '2026-08-26-prop-survivor-scoring-prereg-v2' in str(DEFAULT_PREREG)
assert t.eval_bust_ceiling == 0.05
print('OK', DEFAULT_PREREG)
"
```

**Expected at first scoring:** four tiers present; ceiling numbers 5.0%/1.0%/50%; v1 carries the
closure pointer; `DEFAULT_PREREG` resolves to this file; loader returns `eval_bust_ceiling=0.05`.

---

## Verification

```bash
# §0 anchors
git log -1 --format='%h %ci' -- core/firm_rules.py
git log -1 --format='%h %ci' -- lab/discovery/prop_survivor_scoring.py

# The measured result that motivated this reopening -- current, corrected figures (§10.2
# both-halves; supersedes the 4.34% pooled figure this section originally cited, itself
# already stale by the time of authoring -- see §0's dated correction)
grep -n "3.29%\|5.37%" lab/analysis/c1/aegis_orbmnq_combined_book_2026-08-26/RESULTS.md

# The declined-5%-dial fact in v1's own frozen text (confirms this isn't a fabricated citation)
grep -n "declined the 2%/5% dials" docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md
```
