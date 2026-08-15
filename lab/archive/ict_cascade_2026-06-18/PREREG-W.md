# Q-ICT-W (Weekly directional bias) -- VERDICT PRE-REGISTRATION

**Registered before the W layer's offline analysis is run on the real export. No criterion below may be moved after the first real-population run. The commit of this file is the lock that lifts the firewall for the W layer.**

Parent campaign: [`TEST_PLAN.md`](lab/archive/../../lab/analysis/ict_cascade_2026-06-18/TEST_PLAN.md) (Q-ICT-CASCADE-1; W row of §6, H-W of §4, §7.B W).
Sibling format: [`docs/ltm/briefs/pre-registration/Q-ICT-SWEEPFVG-1-verdict-preregistration.md`](lab/archive/../../docs/ltm/briefs/pre-registration/Q-ICT-SWEEPFVG-1-verdict-preregistration.md).
Authored: 2026-06-18 - **Lock date: RATIFIED 2026-06-18** (operator delegated the genuine-choice calls to Claude with a "most faithful to the design" criterion; GC-1/GC-2/GC-3 LOCKED at their proposed values - see amendment log) - Lock commit: this file's introducing commit (resolve via `git log --oneline -- <this file>`; firewall lifts only from that commit onward).

> **STATUS: PROPOSED -- not yet locked.** The three values flagged in "Genuine pre-registration choices" (block-length rule L_W, n_eff_floor=30, permutation B=10000) are real operator choices, not mechanically forced by §6. They are PROPOSED until the operator commits this file. Everything else is transcribed from the §6 W row / §4 H-W / §7.B W and is not negotiable post-commit.

---

## §0 -- Rule 0 citation (production-source verification)

The W layer's behavior is defined by two gitignored Pine sources (`.gitignore:75` -> `**/*.pine`) living **outside the repo** in `C:\Users\joshu\Downloads\`. They were read verbatim (full contents, with line numbers) in this session. Because a future reader **cannot diff the gitignored bytes**, this is a CITATION-CHAIN anchor: file + bytes + LastWriteUTC + the specific line ranges every frozen-config value comes from. A resuming session MUST re-read (Downloads is mutable; line numbers drift if edited).

| Source file (Downloads) | Bytes | LastWrite (UTC) anchor | Role for W |
|---|---|---|---|
| `ict_weekly_bias_DRAFT.pine` | 9405 | 2026-06-18T17:53:06Z | **The object under test** (B2-W patched draft: adds `gateBias`/`gateScored`/`scored`). Canonical W source for this PREREG. |
| `ict_weekly_bias.pine` | 7542 | 2026-06-18T15:56:20Z | Pre-B2-W original (no `gateBias`). Cited only to show the gate column was absent before the patch; NOT the object under test. |
| `ict_1m_execution_DRAFT.pine` | 22182 | 2026-06-18T18:42:43Z | The live gate the W number must transfer to. `wEmaLen` + `structBias` cited below for the desync constraint. **Load-bearing: this is the desync source, so it is pinned with bytes + UTC like the object under test.** |

Re-anchor command (session start) -- use **PowerShell `LastWriteTimeUtc`** (the Bash `ls -la` view renders these as local ET = UTC-4, e.g. 13:53 / 14:42; the authoritative UTC is from PowerShell):
`Get-ChildItem 'C:\Users\joshu\Downloads\ict_weekly_bias_DRAFT.pine','C:\Users\joshu\Downloads\ict_1m_execution_DRAFT.pine' | Select Name,@{n='UTC';e={$_.LastWriteTimeUtc.ToString('yyyy-MM-ddTHH:mm:ssZ')}},Length`
Expect `ict_weekly_bias_DRAFT.pine` = 9405 / 2026-06-18T17:53:06Z; `ict_1m_execution_DRAFT.pine` = 22182 / 2026-06-18T18:42:43Z. If LastWriteUTC differs from this table -> RE-READ before trusting any line citation below.

**Line ranges the frozen-config values come from (all in `ict_weekly_bias_DRAFT.pine` unless noted):**
- Structure vote = close vs weekly EMA: L67-69 (`wEma = ta.ema(close, emaLen)`; `vStruct = close > wEma ? 1 : close < wEma ? -1 : 0`).
- `emaLen=20`: L26 (`input.int(20, "Structure EMA length", ...)`; tooltip "Match the 1M `wEmaLen`").
- GATE object = structure-only: L110-116, esp. **L116 `gateBias = vStruct`** (the object under test; NOT the composite `bias`).
- Composite vote (RESEARCH, NOT the gate): L85-89 (`score = ...`; `bias = score > 0 ? 1 : ...`).
- Outcome / de-overlap basis: L92 (`realized = close > close[1] ? 1 : ...`), L93-95 (`priorBias`/`scored`/`hit`), L117-119 (`priorGateBias`/`gateScored`/`gateHit`).
- Export columns (data_window): L159-173 -- `bias, outcome, vStruct, vSeason, vRates, vEarn, hit, gateBias, gateHit, gateScored, scored`.
- Four votes for importance: L69 `vStruct`, L73 `vSeason`, L78 `vRates`, L82 `vEarn`.
- Rates-repaint defect (W-2, no `[1]`): L76 (`request.security(rateSym, "W", close, ...)`) -- must be regenerated `close[1]` before the importance run.
- Cross-layer gate object (the desync constraint): `ict_1m_execution_DRAFT.pine` L62 (`wEmaLen = input.int(20, ...)`), L104-106 (`wEma = request.security(..., ta.ema(close, wEmaLen)[1], ...)`; `structBias = wClose > wEma ? 1 : ...`).

---

## Test object -- frozen configuration (zero touches permitted during the verdict window)

| Parameter | Value | Status | Source line |
|---|---|---|---|
| Object under test | **structure-only `gateHitRate`** (NOT composite `hitRate`) | LOCKED (§6 W; B2-W) | W-DRAFT L116, L125 |
| Structure definition | `close > ta.ema(close, emaLen)` -> +1 / `<` -> -1 / `==` -> 0 | LOCKED | W-DRAFT L67-69 |
| `emaLen` | **20** (MUST equal 1M `wEmaLen=20` or the gate object desyncs) | LOCKED (PREREG-pvLen sibling pin: this is the W gate-bearing knob) | W-DRAFT L26; 1M-DRAFT L62 |
| Denominator | recompute from `scored`/`gateScored` flags: `gateScored = bias[1]!=0 AND outcome!=0` on confirmed weeks | LOCKED -- **NEVER `mean(hit)`** (the `hit`/`gateHit` columns collapse miss+stand-down+flat into 0) | W-DRAFT L117-119, L170-173 |
| Outcome | `realized = sign(close - close[1])`; one row per **confirmed** week; drop live bar | LOCKED | W-DRAFT L92, L94 |
| Flat-week handling | weeks with `realized == 0` are NOT scored (excluded from the directional rate); report flat count separately | LOCKED (Appendix B #7 recommend; matches `gateScored` code) | W-DRAFT L118 |
| Composite `bias` rate | RESEARCH / REPORT-ONLY -- does NOT enter the W verdict | LOCKED forbidden (§5; W-1 leg a) | W-DRAFT L85-89, L138-139 |
| CI method | **moving-block bootstrap** (NOT binomial) | LOCKED (§7.B W-2) | -- |
| Block length `L_W` | rule: smallest lag at which step-1 `outcome` autocorr < 0.10, floored at 1, capped at 8 | **provisional -- GENUINE CHOICE (flag)** | step-1 autocorr (W-DRAFT L92) |
| n-floor `n_eff_floor` | **30 scored weeks** (block-reduced effective N) below which "CI straddles 0.50" is INSUFFICIENT-N, not a decision | **provisional -- GENUINE CHOICE (flag)** | power floor (§8) |
| Vote set (importance) | 4 inputs: `vStruct, vSeason, vRates, vEarn` | LOCKED | W-DRAFT L69/73/78/82 |
| Importance penalty | max-statistic label-permutation over the 4 inputs, **B = 10000** | **provisional -- GENUINE CHOICE GC-3** (§7.B W-3 specifies the max-statistic test, NOT the resample count B) | -- |
| Rates-vote pre-condition | regenerate `vRates` non-repaint (`close[1]`, W-2) on an **all-votes-on** export (W-5) BEFORE the importance run | LOCKED pre-condition | W-DRAFT L76 |
| Stationarity | halves AND thirds (chronological) | LOCKED (§6 W RESOLVED) | -- |
| Feed | canonical TV / Pepperstone SPX-class Weekly export | LOCKED (feed canon) | -- |

**The desync constraint is load-bearing.** `gateBias = vStruct` (W-DRAFT L116) is the object-correct number to cite ONLY IF `emaLen` (W-DRAFT L26) `== wEmaLen` (1M-DRAFT L62) `== 20`. If they differ, the W `gateHitRate` measures a different EMA than the live gate and transfers nothing. Any change to `emaLen` away from 20 VOIDS this PREREG (forbidden move #5).

**Two-leg scope (do not overclaim).** W-1 has two legs. `gateBias` fixes **leg (a) only** -- it isolates the structBias OBJECT the gate uses, replacing the composite. It is STILL a **weekly-close proxy**, NOT per-entry gate accuracy (**leg b**). Leg (b) is the separate offline gate-transfer probe (§7.B W-6) and is NOT settled by this layer's verdict. The W verdict below is a verdict on the **weekly-close structure-only hit-rate**, no more.

---

## Resampling unit -- block correction (frozen)

The unit is the **confirmed scored week** (`gateScored == 1`). Point estimate = `nGateHit / nGateScored` over all scored weeks. **CIs resample by moving block of length `L_W`** (rule above), because adjacent weekly outcomes are autocorrelated (trending regimes) -- the script's running `hitRate`/`gateHitRate` (W-DRAFT L108, L125) is a running proportion with no CI and is **not** the verdict instrument (W-4). The de-overlap is by construction one-row-per-confirmed-week (W-DRAFT L94/L118), so there is no pseudo-replication within a week; the block bootstrap exists to absorb *cross-week* autocorrelation, not within-week duplication.

**Verdict instrument = the moving-block-bootstrap 95% CI on the structure-only `gateHitRate`.** Binomial / iid CIs understate SE under weekly autocorrelation and are FORBIDDEN as the verdict (forbidden move #2 below).

---

## Power disclosure (read before judging the verdict)

The per-unit dispersion is a **binary hit/miss** on the scored week, so the relevant variance is **rate variance** `p(1-p)` (not R-sigma): at `p ~ 0.5` the per-week SD is ~0.50, maximal. The effective N is **not** `nGateScored` -- it is the **block-reduced effective N** `~ nGateScored / L_W` after the moving-block correction absorbs cross-week autocorrelation. With a single ~few-year Weekly SPX export the raw `nGateScored` is on the order of low-hundreds of weeks at most, and after block reduction the effective N can fall to the tens. At `p ~ 0.5`, a one-sided detection of a 5pp edge (0.50 -> 0.55) above the CI needs effective N on the order of ~200+ -- **not achievable on a single-instrument Weekly window.**

**Decision rules below are expectation / CI-based, not significance tests.** A "CI lower bound > 0.50" is a *credibility upgrade* that routes the structure-only bias toward continued use and a downstream per-entry transfer probe (§7.B W-6) -- it does **not** lock, deploy, or by itself license the 1M gate (the cascade-transfer pre-gate, H-CASCADE, is separate). Single-regime: cross-regime stationarity is the halves/thirds test, and a one-regime pass routes to AMBIGUOUS-HOLD, not RESOLVED.

**n-floor (mandatory power gate).** If the **block-reduced effective N (scored weeks) < `n_eff_floor` = 30**, the verdict is **INSUFFICIENT-N**, not FALSIFIED -- a starved layer returns a CI that straddles 0.50 indistinguishably from a true null, and calling that FALSIFIED would be a power artifact. INSUFFICIENT-N -> extend the export window (independent **period** / independent **price path**; never "a different feed" of the same weeks) and re-run; do not re-spec the rule to manufacture n.

---

## Verdict gate (binary)

Maps exactly to the §6 W row. The verdict instrument is the moving-block-bootstrap 95% CI on the **structure-only** `gateHitRate` (denominator from `gateScored`).

| Verdict | Trigger |
|---|---|
| `RESOLVED` (-> continued use + per-entry transfer probe, not deploy) | structure-only corrected **95% block-CI lower bound > 0.50** - AND stationary across **halves** (both halves' point estimate > 0.50) - AND stationary across **thirds** (all three thirds' point estimate > 0.50) - AND effective N >= `n_eff_floor` (30) |
| `FALSIFIED` | corrected **95% block-CI straddles 0.50** (lower bound <= 0.50) - AND effective N >= `n_eff_floor` (30) |
| `AMBIGUOUS-HOLD` | CI lower bound > 0.50 **but** non-stationary (the edge lives in one regime -- a half or a third <= 0.50) -> HOLD + **name the re-test window** (the regime the edge is absent in) |
| `INSUFFICIENT-N` | effective N (block-reduced scored weeks) **< `n_eff_floor` = 30** -> claim unfalsifiable on this data; extend period/path and re-run. Dominates FALSIFIED (a straddling CI under the floor is NOT a falsification). |

**Vote-importance sub-verdict (separate from the structure-only headline; §4 H-W "vote-adds-nothing"):** the COMPOSITE-vote claim is **KILLED** if no single input (`vStruct, vSeason, vRates, vEarn`) solo-beats the structure-only baseline after the **max-statistic label-permutation penalty (B=10000)** over the 4 inputs. Killing the composite claim does NOT change the structure-only headline verdict above -- structure-only stands or falls on its own block-CI. (Pre-condition: importance runs only on the W-2-fixed, all-votes-on export per the frozen-config table.)

**Pre-registered before any data touches analysis.** Amending this gate mid-campaign to match emerging evidence is methodology-layer p-hacking (close AMBIGUOUS, capture why, open fresh).

---

## Forbidden (during the verdict window) -- the moves that bite the W layer

1. **Citing the composite `hitRate` as the verdict.** The composite `bias` (W-DRAFT L85-89) mixes seasonal/rates/earnings; the live gate is `structBias`-only. The verdict object is `gateHitRate` (L116/L125) ONLY. (§5; W-1 leg a.)
2. **Using a binomial / iid CI as the verdict instrument.** Weekly outcomes autocorrelate; the verdict is the **moving-block-bootstrap** CI. Switching iid <-> block after outcomes is forbidden.
3. **Trusting the `hit` / `gateHit` column denominator.** Those columns (W-DRAFT L165 `hit`, L171 `gateHit`) collapse miss + stand-down + flat all into 0 (the collapse is noted in the comment at L168-169). The denominator MUST be recomputed from `scored`/`gateScored` (L172-173). Reading `mean(hit)` silently divides hits by total-weeks, not scored-weeks.
4. **Running the per-input importance test on a votes-off export.** Votes default off (W-DRAFT L31/38/46); a single default export has only `vStruct` live (W-5). The importance run requires an **all-votes-on** export with `vRates` regenerated non-repaint (`close[1]`, W-2 / L76). Running importance on the default export tests nothing.
5. **Changing `emaLen` away from 20.** It desyncs `gateBias` (W-DRAFT L116) from the 1M `structBias` gate object (`wEmaLen=20`, 1M-DRAFT L62) -- the W number then transfers nothing. `emaLen=20` is LOCKED for this verdict.
6. **Moving the block length or the n-floor after outcomes.** `L_W` is set by the pre-registered autocorrelation rule on step-1; `n_eff_floor=30` is fixed. Tuning either after seeing the CI is moving the goalposts (audit hook below catches it).
7. **Outcome-conditional flat-week reclassification.** Flat weeks (`realized==0`) are excluded from the rate (frozen). Re-counting them as miss/hit after seeing the rate to nudge it across 0.50 is forbidden.

---

## Genuine pre-registration choices (operator ratification required before run 1)

These are real choices -- NOT mechanically forced by §6. They are **PROPOSED** until the operator commits this file.

| # | Choice | Proposed value | Why it is a genuine choice (not forced) | Rationale for the proposed value |
|---|---|---|---|---|
| GC-1 | Block length `L_W` for the moving-block bootstrap | **rule:** smallest lag at which step-1 `outcome` autocorrelation drops **< 0.10**, floored at 1, capped at 8 | §6 says "moving-block bootstrap" but not the block length; any value/rule could be chosen | Data-driven (lets the observed autocorrelation set the block) + bounded so a near-zero autocorr can't collapse to iid (floor 1) and a spurious long-memory read can't over-widen the CI to un-falsifiability (cap 8). **The 0.10 autocorr cutoff, the floor (1), and the cap (8) are ALL part of the frozen rule** -- none may be nudged post-hoc; operator may revise any of the three before lock. |
| GC-2 | n-floor `n_eff_floor` (effective scored weeks) for "CI straddles 0.50" to be a decision | **30** scored weeks (block-reduced) | §6 routes the verdict to a block bootstrap; without a floor a starved layer returns FALSIFIED-looking ambiguity that is actually a power artifact. The floor value is a power/credibility trade the operator owns. | 30 is the conventional small-sample threshold below which a binary-rate CI is too wide to discriminate a plausible 5pp edge from null; operator may set higher (more conservative) given the single-window power disclosure. |
| GC-3 | Resample count `B` for the max-statistic label-permutation (vote importance) | **10000** | §7.B W-3 names the max-statistic permutation test but gives NO B; §8 lists the PREREG-W stub as owing "best-of-K cell count + penalty" -- B is a PREREG-introduced value, not a §7.B transcription | 10000 permutations resolves a max-of-4 null p-value to ~+/-0.005 SE -- enough to call the 0.05 importance threshold cleanly; operator may raise for a tighter tail. |

If the operator alters either value, edit the frozen-config table + this section IN THE SAME COMMIT that locks the file, then the firewall lifts from that commit. After the first real-population run, neither may move (forbidden move #6).

---

## Audit hook

Reviewer question at verdict time: *"Was any criterion above -- the object (structure-only vs composite), the CI method (block vs binomial), the block length `L_W`, the n-floor, the denominator source, or `emaLen` -- moved, reinterpreted, or supplemented after the outcome run?"* Any **yes** -> the verdict is void and the W pattern stays unresolved.

Runnable assertions (the W-layer cheap eyeball checks):

```bash
# This file's lock commit anchors the registration (firewall lifts only from here):
git log --oneline -- lab/analysis/ict_cascade_2026-06-18/PREREG-W.md | tail -1

# §0 re-anchor -- the object under test + the desync source are mutable + outside the repo:
#   PowerShell: Get-ChildItem 'C:\Users\joshu\Downloads\ict_weekly_bias_DRAFT.pine','C:\Users\joshu\Downloads\ict_1m_execution_DRAFT.pine' |
#     Select Name,@{n='UTC';e={$_.LastWriteTimeUtc.ToString('yyyy-MM-ddTHH:mm:ssZ')}},Length
#   Expect weekly 9405 / 2026-06-18T17:53:06Z  AND  1m 22182 / 2026-06-18T18:42:43Z.
#   (Bash `ls -la` shows local ET = UTC-4; use PowerShell UTC.) If different -> RE-READ before trusting line cites.

# Confirm the gate object is structure-only (not the composite) in the draft under test:
grep -n 'gateBias = vStruct' 'C:/Users/joshu/Downloads/ict_weekly_bias_DRAFT.pine'   # expect L116

# Confirm the export carries the denominator-recompute flags (so the harness never uses mean(hit)):
grep -nE '"scored"|"gateScored"|"gateBias"' 'C:/Users/joshu/Downloads/ict_weekly_bias_DRAFT.pine'  # L170-173

# Desync guard -- W emaLen must equal the 1M gate's wEmaLen (both 20):
grep -nE 'emaLen .*input.int' 'C:/Users/joshu/Downloads/ict_weekly_bias_DRAFT.pine'      # L26 -> 20
grep -nE 'wEmaLen .*input.int' 'C:/Users/joshu/Downloads/ict_1m_execution_DRAFT.pine'    # L62 -> 20
#   If the two defaults differ -> gateHitRate transfers nothing -> verdict void.
```

This file's hash/date anchors the registration; evaluation appends below, never edits above.

---

## Amendment log (append-only)

- **2026-06-18 — RATIFIED (operator-delegated; criterion: most faithful to the design).** The operator delegated the genuine-choice calls to Claude. GC-1 (`L_W` = smallest lag autocorr<0.10, floor 1, cap 8), GC-2 (`n_eff_floor` = 30 scored weeks), GC-3 (importance permutation `B` = 10000) are **LOCKED at their proposed values** — each is the design-faithful default (data-driven block length; conventional small-sample power floor; tail-resolving permutation count). **No value changed.** Pre-data: no criterion may move after run 1 (audit hook). Firewall lifts on this file's commit.
