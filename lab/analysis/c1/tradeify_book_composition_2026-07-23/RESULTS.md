**Theme:** c1
**Status:** ACTIVE — eval-lock fix + §2 book-composition re-derivation
# tradeify_book_composition — eval-lock fix + §2 re-derivation (2026-07-28)

**Defect (diagnosed, not re-litigated):** `eval_sim` applied the Funded-Flex floor
lock (`peak ≥ $103,100 → floor = $100,100`) during the **evaluation** phase.
Tradeify article 10495897: evaluations do not lock. Record:
[`docs/briefs/programs/2026-07-23-tradeify-book-composition.md`](../../../docs/briefs/programs/2026-07-23-tradeify-book-composition.md)
§Addendum 2026-07-28 (diagnosis) + §Addendum 2026-07-28b (this fix).

**Fix:** in every `eval_sim` / `esim` in this harness, `floor = peak - DD`
unconditionally. `funded_sim` / `fsim` byte-unchanged. Constants
`FLOOR_LOCK_BAL` / `FLOOR_LOCKED` retained for funded.

## STEP 1 — Reproduction control (unmodified harness)

**SHA (pre-fix / post-#542 merge):** `602b692f2851c2d7d8ddf32570cb0c5cafe041a1`

Source of published §2 chain figures: `gap_stage4.py` (brief §10), not
`gap_stage2.py` (parallel 2-leg path; same seeds, slightly different panel
construction → chain $346 vs $339).

| Cell | Published | Reproduced | Tolerance | Verdict |
|---|---|---|---|---|
| 2-leg pass % | 63% | 63% (stage4) | ±1 pp (integer print) | **MATCH** |
| 2-leg median mo | 8.2 | 8.2 | ±0.15 mo | **MATCH** |
| 2-leg chain $/acct-mo | $339 | $339 | ±$15 | **MATCH** |
| 2-leg funded dead-1y | 43% | 43% | ±1 pp | **MATCH** |
| ORB@1 pass / med / chain | 59% / 6.2 / $556 | 59% / 6.2 / $556 | same | **MATCH** |
| ORB@6 pass / med / chain | 27% / 1.2 / $941 | 27% / 1.2 / $941 | same | **MATCH** |
| ORB@6+Aegis (no caps) chain | $1,233 | $1,233 | ±$15 | **MATCH** |

Logs: `out/repro_stage4_before.log`, `out/repro_orb1_before.log`,
`out/repro_stage2_before.log` (stage2 m=1.0: 63% / 8.1 mo / $346 — noted skew,
not the §2 owner).

## STEP 2 — Code fix

| File | Change |
|---|---|
| `gap_stage2_capbound.py` `eval_sim` | `floor = peak - DD` + article 10495897 comment |
| `gap_stage2.py` `eval_sim` + `hist_chain` eval loop | same |
| `gap_stage3.py` `eval_sim` | same |
| `gap_stage4.py` `esim` | same |
| `rerun_section2.py` | new §2 re-derivation runner (corrected floor; k=1..6 frontier) |

`funded_sim` / `fsim` untouched in all files.

## STEP 3 — Before / after (corrected eval)

| Book | Eval pass (before → after) | Median mo | Funded dead-1y | Chain $/acct-mo |
|---|---|---|---|---|
| 2-leg (c1 geometry) | 63% → **38%** | 8.2 → **5.8** | 43% → 43% | **$339 → $318** |
| +ORB@1 | 59% → **30%** | 6.2 → **4.1** | 69% → 69% | **$556 → $499** |
| +ORB@2 | (brief frontier) → **22%** | → **2.3** | → 83% | → **$558** |
| +ORB@3 | → **19%** | → **1.4** | → 88% | → **$677** |
| +ORB@4 | → **16%** | → **1.1** | → 90% | → **$735** |
| +ORB@5 | → **14%** | → **0.8** | → 92% | → **$797** |
| +ORB@6 | 27% → **12%** | 1.2 → **0.7** | 93% → 93% | **$941 → $819** |
| +ORB@6 +Aegis (no caps) | 29% → **13%** | 1.2 → **0.7** | 90% → 90% | **$1,233 → $1,093** |

ORB frontier chains k=1..6 (corrected): **$499 → $558 → $677 → $735 → $797 → $819**
(published defective: $556 → $626 → $735 → $824 → $941 — five published points;
full k=1..6 after above).

**Headline:** corrected 2-leg chain rate = **$318/acct-mo** (replaces $339).

Funded dead-1y and E[cash|funded] are unchanged cell-for-cell (funded kernel
untouched). Pass% fell hard; median time-to-pass *shortened* among survivors
(slow lock-cushion paths now bust). Chain rate fell less than pass% because
E[cycle] also shortened.

Cross-check: `gap_stage4.py` post-fix prints identical 2-leg / ORB@6 / Aegis
headlines (`out/section2_stage4_corrected.log`). Full frontier:
`rerun_section2.py` → `out/section2_corrected.json`.

## Does this change book-composition conclusions?

**Yes — expected, not a failure.**

- Eval is no longer "cheap immortal": 2-leg pass 63%→38%, ORB@6 27%→12%.
- Churn still maximizes chain rate (frontier still rises with k), but absolute
  levels are lower and the pass/mortality tradeoff is sharper.
- Cadence diagnosis (ORB dissolves winning-day cycles) still holds — funded
  mechanics unchanged.
- H1 falsifier band must retarget to **$318/acct-mo** (see brief addendum).
- Q-CAPALLOC-1 remains **blocked**: still owes operator rule-pin dashboard
  verification (STATE.md operator-queue item 4) **and** now this eval-lock fix
  before any re-run. **Do not re-run Q-CAPALLOC-1 in this packet.**

## STEP 4 — M-24 mechanic sweep (surfaces CHECKED)

Search: `103_100`, `100_100`, `103100`, `100100`, `dd_lock_offset_usd`,
`eval_sim`/`esim`, `peak >= FLOOR_LOCK` / `pk >= FLB`, lock/freeze/floor in
eval-phase sims.

| Surface | Role | Eval-lock status |
|---|---|---|
| `gap_stage2_capbound.py` `eval_sim` | book-comp / Q-CAPALLOC import | **FIXED this packet** |
| `gap_stage2.py` `eval_sim` + hist eval | book-comp 2-leg | **FIXED** |
| `gap_stage3.py` `eval_sim` | Aegis counterfactual | **FIXED** |
| `gap_stage4.py` `esim` | §2 owner | **FIXED** |
| `rerun_section2.py` `esim` | §2 re-derivation | **FIXED** (authored corrected) |
| `gap_*` `funded_sim`/`fsim` | funded phase | Correct (lock belongs here) — untouched |
| `lab/archive/q_funnel_1_2026-07/funnel.py` | hard-coded 103_100/100_100 | **OK** — literals used only in `simulate_funded_phase`; eval goes through `core.mc.simulate_path` |
| `core/firm_rules.py` `dd_lock_offset_usd: 100` on eval rows | config encoding | **OUT OF SCOPE** (known; needs re-MC + amending ADR) |
| `core/mc/simulation.py` trailing_locking | engine consumer of config | inherits firm_rules defect; not this harness |
| `tests/core/test_trailing_locking_boundary.py` | engine idiom `1e6` = no-lock | reference only |
| `lab/archive/c1_capalloc_2026-07-27/run_capalloc.py` | imports `G.eval_sim` | inherits fix once capbound lands; **re-run still blocked** |
| `lab/analysis/tradeify_eval_lock_correction_2026-07-22/` | prior measurement of config defect | historical; correct idiom |
| `lab/analysis/c1_band_rescore_2026-07-24/` + rider | patches offset to 1e6 | separate family (M-23); not hard-coded 103_100 |
| `lab/analysis/class_s_*` / `tradeify_futures3_*` / `geofit_*` | MC via firm_rules | config path; out of scope |
| Docs / ADRs / lessons citing 103_100 | prose | not executable |

No additional independent **hard-coded eval-phase lock** found beyond this
harness family. The standing config defect in `firm_rules.py` remains separate.

**Post-fix SHA:** `d4c340f` (fix commit; branch `fix/eval-sim-funded-lock-2026-07-28`)


## Addendum 2026-07-29 — funded contract scaling corrected to the verified four-step ladder

Implements [`docs/superpowers/specs/2026-07-29-funded-contract-scaling-4step-design.md`](../../../docs/superpowers/specs/2026-07-29-funded-contract-scaling-4step-design.md),
which was written after the 2026-07-29 rule-pin verification found the modelled funded start tier
was wrong ([`docs/notes/2026-07-24-tradeify-rulepin-verification.md`](../../../docs/notes/2026-07-24-tradeify-rulepin-verification.md)).

### What changed

The funded contract cap was modelled as a **binary** step (40 micros → 80 at EOD $103,000). The
published rule is a **four-rung, EOD-calibrated, cumulative ladder** for a 100K funded account:
**30 → 40 @ $101,500 → 50 @ $102,000 → 80 @ $103,000**. Separately, the modelled `PAYOUT_MIN`
of $1,000 does not exist — Select **Flex** has no minimum payout ($250 belongs to Select *Daily*).

The ladder now has **exactly one definition**, in
[`funded_scaling.py`](funded_scaling.py). The mandated M-24 sweep found **six binary-cap sites
across five kernels** — one file (`gap_stage2.py`, including a **scalar** walk-forward loop) was
not in the spec's own list and would have been missed by a vectorised-only grep:

| File | Sites |
|---|---|
| `gap_stage2.py` | vectorized `funded_sim` + scalar `hist_chain` loop |
| `gap_stage2_capbound.py` | `funded_sim` |
| `gap_stage3.py` | `funded_sim` |
| `gap_stage4.py` | `fsim` |
| `rerun_section2.py` | `fsim` |

`eval_sim` is untouched (evaluations are neither locked nor scaled — the article is explicit:
"During evaluation, you have access to the full contract limits").

### Correctness evidence, in the order it was established

1. **Reproduction control before any behaviour change** — the pre-change harness reproduced its
   committed §2 values (2-leg 38% / 5.8 mo / **$318.20**, ORB frontier $499→$819).
2. **Behaviour preservation: bit-identical.** Feeding the *refactored* code a **legacy** ladder
   reproduces the committed numbers exactly — `pass_pct` 37.78, `chain` **318.20396943677065**.
   This is what isolates every downstream difference to the rule change rather than the refactor.
3. **11/11 ladder unit tests** ([`tests/lab/test_funded_scaling_ladder.py`](../../../tests/lab/test_funded_scaling_ladder.py))
   — rung sequence, one-way latch on retreat, and the **next-day** effect ordering (a rung crossed
   today must not raise today's cap).

### The three attributable arms

Artifacts: `out/arm_control.json`, `out/arm_a_ladder.json`, `out/arm_b_payoutmin.json`, `out/arm_c_both.json`.

| Arm | 2-leg eval pass | funded dead-1y | chain $/acct-mo | ORB@6 chain |
|---|---|---|---|---|
| control (legacy 40→80, PM $1,000) | 37.78% | 42.77% | $318.20 | $818.73 |
| (a) four-step ladder only | 37.78% | 44.70% | $307.32 | $802.50 |
| (b) payout-min 0 only | 37.78% | 45.61% | $312.95 | $810.65 |
| **(c) both — verified truth** | **37.78%** | **49.06%** | **$299.80** | **$792.91** |

**Eval pass is identical across every arm (37.78%)** — the correct sanity check, since both
corrections are funded-only.

**`dead-1y` is the sensitive output, as the spec predicted** — and the two corrections are
**super-additive**: +1.93 pp (ladder) and +2.84 pp (payout-min) separately, but **+6.29 pp**
together. Mechanism: removing the payout minimum makes payouts earlier and smaller, each one
withdrawing balance, while the tighter early rung slows regrowth — so the account lingers longer in
the low-equity region where the funded floor binds. The earlier floor-lock that early payouts buy
does **not** offset this.

**Chain rate: $318.20 → $299.80** (−5.8%). Cumulative against the originally published figure:
**$339 → $318 (eval-lock fix) → $299.80 (funded pins)**, −11.6%.

### Consequences

- The brief's §4 **H1 falsifier band must be retargeted again**, from $318 to **$299.80/acct-mo**.
- **Funded mortality is materially worse than modelled** — nearly half of funded accounts die
  within a year at the verified rules (49.06% vs 42.77%).
- The ORB frontier keeps its shape (chain rises monotonically with k while pass collapses), so no
  book-composition **ordering** conclusion inverts; magnitudes move.
- **Q-CAPALLOC-1 re-run is in flight at the time of writing** — its verdict is NOT recorded here.
  It is a re-run, not a new look (no fresh K).
