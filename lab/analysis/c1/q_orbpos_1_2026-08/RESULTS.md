# Q-ORBPOS-1 — Phase 0 Contingency Resolution + Path Determination

**Pre-registration:** [`docs/briefs/pre-registration/2026-08-22-orbcush-1-tff-positioning-mechanism-prereg.md`](../../../../docs/briefs/pre-registration/2026-08-22-orbcush-1-tff-positioning-mechanism-prereg.md)
**Operator GO:** Joshua, 2026-08-23 chat, "take it up" (Status line + Change history of the pre-reg).
**This file authored:** 2026-08-23, Claude Code (Sonnet 5), Phase 0 only.

**Order-of-operations attestation (§4):** No CFTC TFF position value (net long/short contracts,
%OI, or any weekly number) was read before this section was written and saved. Everything below is
report *structure*/metadata — legend, category names, field names, publication-schedule text — read
from CFTC's own explanatory-notes PDF, its public report pages, and its published field-layout page,
none of which display an actual weekly position figure for any date. This file is committed to disk
as a single Phase-0-only artifact before Phase 1 (the actual TFF pull) begins.

---

## Phase 0 — Contingency Resolution

### 1. MNQ separate-reporting status

**Resolved: MNQ is separately reported. The §2.2/§4-trigger-2 combined-line contingency does NOT
fire.**

CFTC's own TFF report structure (fetched from `cftc.gov/dea/futures/financial_lf.htm`, the TFF
short-format report, and cross-checked against the market-code registry used by third-party COT
aggregators that source directly from CFTC) lists three distinct NASDAQ-100-family reportable lines,
not one combined line:

| Reportable line (as printed) | Contract spec | Relation to ORB-MNQ-1 |
|---|---|---|
| `NASDAQ-100 Consolidated` | NASDAQ 100 INDEX x $20 | Full-size + mini consolidation, legacy line |
| `NASDAQ MINI` | NASDAQ 100 STOCK INDEX x $20 | This is **NQ**, the parent mini |
| `MICRO E-MINI NASDAQ-100 INDEX` | NASDAQ 100 STOCK INDEX x $2 | This is **MNQ** — a separate, standalone reportable line, distinct from `NASDAQ MINI` |

`MICRO E-MINI NASDAQ-100 INDEX` carries its own CFTC market/commodity code (209747 in the
third-party registries that mirror CFTC's own code, e.g. Tradingster's `cot/futures/fin/209747`),
independent of NQ's own code. This is a structural fact about the report's category list, not a
position read.

**Caveat carried to Phase 1, not resolved here:** that MNQ has its *own line today* does not by
itself prove that line carries usable position data back to MNQ's 2019-05-06 launch, or through the
full pre-break window (2019-05-06 → 2021-09-28) — CFTC only breaks out a category once ≥20 traders
hold positions at or above reporting levels (per the explanatory notes, item 3 below), so a newly
launched contract can in principle start under a combined or thin-count posture and separate out
later. **This is a data-availability/depth question for Phase 1's actual pull, not a report-structure
question** — it does not reopen the §4 trigger-2 contingency (which is specifically about whether a
*separate line exists at all*, which it does), but Phase 1 must check and report the *first available
date* on the MNQ line as part of the pull, and if usable history does not extend back near
2019-05-06, that is a new fact for Phase 2/6 to reckon with under the existing Ambiguous-hold sparsity
trigger (§4 item 1), not a silent extension of this Phase-0 finding.

### 2. MNQ share of combined NQ+MNQ volume/OI — MOOT (trigger did not fire)

Since item 1 resolves MNQ as separately reported, the §2.2 "combined-line share ≥10%" test is not
reached — there is no combined line to test a share against. This item is recorded as **moot, not
skipped**, per the pre-registration's own order-of-operations discipline.

For completeness (repo-search only, no CME data pull performed, since none was needed once item 1
resolved): this repo carries **no existing daily volume or open-interest series for MNQ or NQ**.
`core/data/bar_data/` holds `MNQ_M15.csv` (a *price* bar panel per its `SHA256SUMS` manifest entry)
and `MYM_M15.csv`/`M2K_M15.csv`/`MCL_M15.csv`/`MGC_M15.csv`/`6J_M15.csv` — all price bars, none of
them volume-or-OI series. `core/data/tv_exports/cme/` and `core/data/external/` likewise carry no
volume/OI series for either instrument (`core/data/external/SHA256SUMS` lists one COT-family file,
`COT_GOLD_disaggregated_weekly_cftc.csv`, which is the Disaggregated report for Gold — a different
report, different instrument, not reusable here). `ops/instruments/MNQ.md` and `NQ.md` document price
continuous-contract roll conventions (`.v.0` vs `.c.0`) but no volume/OI panel. **Had item 1 gone the
other way, a fresh CME public contract-statistics check would have been needed — none exists in-repo
to reuse.** This is now moot given item 1's resolution, but recorded per the brief's own instruction
to check before assuming.

### 3. Exact CFTC TFF column/category names

**Resolved.** Fetched CFTC's own published field-layout page for the TFF historical/machine-readable
report (`cftc.gov/MarketReports/CommitmentsofTraders/HistoricalViewable/cotvariablestfm.html`) and
the human-readable explanatory notes PDF
(`cftc.gov/sites/default/files/idc/groups/public/@commitmentsoftraders/documents/file/tfmexplanatorynotes.pdf`).

- The four category headers are exactly: **Dealer/Intermediary**, **Asset Manager/Institutional**,
  **Leveraged Funds**, **Other Reportables** (plus Nonreportable Positions) — confirmed verbatim from
  the explanatory notes.
- The literal machine-readable field names (confirmed from CFTC's own field-layout page) are:
  - `Lev_Money_Positions_Long_All` / `Lev_Money_Positions_Short_All` — **yes**, the brief's guessed
    wording ("Lev Money Positions Long/Short (All)") is correct, this is the actual published field
    name for the primary (Leveraged Funds) category.
  - `Asset_Mgr_Positions_Long_All` / `Asset_Mgr_Positions_Short_All` — the secondary/fallback category
    field names.
  - `Open_Interest_All` — total open interest, published as its own separate field.
- **%OI is a directly published field, not something that must be derived** from raw position counts
  and a separately-published OI total: `Pct_of_OI_Lev_Money_Long_All`,
  `Pct_of_OI_Lev_Money_Short_All`, `Pct_of_OI_Asset_Mgr_Long_All`, `Pct_of_OI_Asset_Mgr_Short_All` are
  all published fields in their own right. This resolves the brief's §2.2 open question ("whether %OI
  needs to be derived or is a published field") in the simpler direction — Phase 1 can read the %OI
  fields directly rather than computing `position / Open_Interest_All`, though computing it as a
  cross-check against the published field is cheap and worth doing in Phase 2/3's independent
  second-implementation step.
- The human-readable short-format report (`financial_lf.htm`) shows the same four categories with
  Long/Short/Spreading sub-columns, and a separate "Percent of Open Interest Represented by Each
  Category of Trader" section — consistent with the machine-readable field names above.

### 4. Reporting-lag convention

**Confirmed, matches §2.2's stated assumption exactly.** From CFTC's own "About the COT Reports" page
(`cftc.gov/MarketReports/CommitmentsofTraders/AbouttheCOTReports/index.htm`), quoted directly: *"The
weekly reports for Futures-Only Commitments of Traders and for Futures-and-Options-Combined
Commitments of Traders are released every Friday at 3:30 p.m. Eastern time."* The data released each
Friday reflects that same week's **Tuesday** open interest (also confirmed in the TFF explanatory
notes PDF: *"a breakdown of each Tuesday's open interest..."*). Holiday-adjusted variants exist (a
Monday holiday shifts the snapshot day to Wednesday, still published Friday; a Friday holiday shifts
publication to Thursday) but do not change the core Tuesday-snapshot/Friday-publication convention
§2.2 assumes. **No causal-lag redesign is needed** — the brief's `.shift(1)`-equivalent discipline
("a given week's classifier value may use only TFF prints already published as of that week") is
already correctly specified against this confirmed cadence.

---

## Phase 0 — Path determination (post-write, per the brief's own ordering)

**The §2.2/§4 trigger-2 "MNQ-not-separately-reported" Ambiguous-hold contingency does NOT fire.**
MNQ (`MICRO E-MINI NASDAQ-100 INDEX`) is confirmed as its own standalone CFTC TFF reportable line,
structurally distinct from NQ (`NASDAQ MINI`) — item 1 above. Item 2 (the 10%-share floor) is
therefore moot, not failed. Items 3 and 4 raise no blocking issues: the exact field names are known
and simpler than the brief worried they might be (%OI is a direct field, not a derived one), and the
Tuesday/Friday cadence is confirmed exactly as assumed.

**Campaign proceeds normally to Phase 1** with a real classifier: a trailing, causal
`Lev_Money_Positions_Long_All`/`Lev_Money_Positions_Short_All` (primary) or
`Asset_Mgr_Positions_Long_All`/`Asset_Mgr_Positions_Short_All` (secondary, fallback-only per §4/§5)
net-%OI classifier, read from the `Pct_of_OI_*` fields directly, on the standalone MNQ TFF line.

**One caveat carried forward, not a contingency-firing event:** Phase 1 must record the *first
available date* of usable (non-thin, ≥4-trader-disclosed) data on the MNQ line, since a young contract
can in principle start under a combined or suppressed-count posture before separating out cleanly.
If that first-usable-date check lands materially inside the pre-break window rather than covering it
fully, that is new information for the existing §4-item-1 sparsity Ambiguous-hold trigger to catch on
its own terms — it does not require a new contingency or a return to this Phase 0 section.

**No Ambiguous-hold fires at Phase 0.** Phase 1 (the actual TFF pull) may proceed.

---

## Phase 1 — Pull

CFTC Socrata TFF endpoint (`publicreporting.cftc.gov/resource/gpe5-46if.json`), filtered
`cftc_contract_market_code='209747'` (MICRO E-MINI NASDAQ-100 INDEX), `futonly_or_combined='FutOnly'`.
301 weekly rows, **first report_date 2020-08-04**, last **2026-08-18** (contract launched 2019-05-06;
the standalone TFF line does not begin until 15 months later — this is new information *within*
Phase 1's own scope, not a Phase-0 contingency reopening, per the RESULTS-file caveat above). **45
independent published prints exist in the pre-break span** (2020-08-04 → 2021-09-28), 11× the §4
sparsity floor of 4 — the W1 Ambiguous-hold trigger does not fire. `%OI` read directly from the
published `pct_of_oi_lev_money_long_all` / `pct_of_oi_lev_money_short_all` fields; cross-checked
against `(long−short)/open_interest_all`, max discrepancy 0.096pp (rounding-only).

## Phase 2 — Classifier + gate-clearance (build implementation)

Trailing causal extremity `= |pct_of_oi_lev_money_long − pct_of_oi_lev_money_short|`, rolling mean
over the trailing W published TFF prints (W = 4/13/26), bucket-split on the trailing series' own
expanding causal median. Publication lag respected (Tuesday snapshot, Friday publication; a print is
usable starting the next business day after publication). Gate-clearance harness
(`day_loop_intraday`/`build_paths_orb`/`run_policy_orb`/`pol_cushion`/`pol_const`) imported unchanged
from `lab/analysis/c1/orbmnq1_cushion_sizing_probe_2026-08-20/run_evalseq_orb_intraday.py`; fidelity
control reproduced the published flat-policy anchors exactly (k=1 bust 67.67%/pass 32.33%, k=2 bust
77.01%/pass 22.99%, both 0.00pp delta) before any bucket result was trusted. Full numeric output:
[`results_orbpos_tff_probe.json`](results_orbpos_tff_probe.json), full transcript:
[`run_log.txt`](run_log.txt), script: [`run_orbpos_tff_probe.py`](run_orbpos_tff_probe.py).

| Window | Higher-bucket post-break frac (day-level) | Lower-bucket post-break frac (day-level) | Date-corr clears? | Higher cushion pass % (gate) | Lower cushion pass % (gate) | Direction |
|---|---|---|---|---|---|---|
| W1 (4 prints) | 89.64% (n=724 days) | 74.44% (n=810 days) | No (lower 34.44pp over ceiling) | 23.05% (FAIL) | 99.24% (PASS) | `LOWER_CLEARS_HIGHER_DOES_NOT` |
| W2 (13 prints) | 96.29% (n=674 days) | 80.40% (n=750 days) | No (lower 40.40pp over ceiling) | 62.98% (PASS) | 98.64% (PASS) | `BOTH_CLEAR` |
| W3 (26 prints) | 99.26% (n=674 days) | 85.74% (n=680 days) | No (lower 45.74pp over ceiling) | 49.52% (FAIL — 0.48pp under floor) | 99.44% (PASS) | `LOWER_CLEARS_HIGHER_DOES_NOT` |

Date-correlation clears **0 of 3** windows. Gate direction is **not** the same sign at every window
(W2 = `BOTH_CLEAR` vs W1/W3 = `LOWER_CLEARS_HIGHER_DOES_NOT`). No Ambiguous-hold trigger fires.

## Phase 3 — Independent adversarial re-derivation (two from-scratch builds) + cross-implementation comparison

Per §7 Phase 3, two independent teams built the classifier + gate-clearance check from scratch (not a
re-read of Phase 2's script). **Implementation A** = the Phase 2 build above, whose own artifacts are
committed in this directory and independently re-verified here (JSON/log re-read, not re-run).
**Implementation B** built an entirely separate script + pull in a private per-session scratchpad
(`C:\Temp\claude\...\scratchpad\orbpos1_implB\` — a temp path scoped to that build session, not this
worktree; **its raw files are not recoverable from this session or committed anywhere in the repo** —
only its written report and the numbers therein could be cross-checked, not its code or raw CSV/JSON).
This asymmetry is disclosed, not papered over: Implementation A's numbers below are independently
re-verified against its own artifact files; Implementation B's numbers are taken as reported and
cross-checked only where B's own report gives auditable sub-detail (e.g. per-bucket day/print counts).

**Every qualitative call agrees exactly between A and B:**
- Contract line (`209747`, standalone since 2020-08-04, distinct from NQ's `209742`) — same.
- Classifier formula (`|long %OI − short %OI|`, trailing rolling mean, expanding causal median split) — same.
- Publication-lag convention (Tuesday snapshot / Friday publish, next-business-day usable) — same.
- No Ambiguous-hold trigger fires (sparsity, MNQ-not-separately-reported) — same, both explicitly checked.
- Date-correlation: fails at all 3 windows (0/3 clear) — **identical** in both.
- Gate-clearance direction per window: `LOWER_CLEARS_HIGHER_DOES_NOT` (W1), `BOTH_CLEAR` (W2),
  `LOWER_CLEARS_HIGHER_DOES_NOT` (W3) — **identical** in both, including the exact same disqualifying
  W2 sign-break.
- Final verdict: **REJECT / FALSIFIED** — identical.

**Where the two implementations diverge, materially, on exact magnitude (disclosed, not resolved):**

| Metric | Impl A (re-verified from JSON) | Impl B (as reported) | Gap |
|---|---|---|---|
| W1 higher post-break frac | 89.64% | 92.31% (n=143) | 2.67pp |
| W1 lower post-break frac | 74.44% | 78.67% (n=150) | 4.23pp |
| W2 higher post-break frac | 96.29% | 96.32% (n=136) | 0.03pp |
| W2 lower post-break frac | 80.40% | 80.41% (n=148) | 0.01pp |
| W3 higher post-break frac | 99.26% | 97.84% (n=139) | 1.42pp |
| W3 lower post-break frac | 85.74% | 86.36% (n=132) | 0.62pp |
| W1 higher-bucket cushion pass% | 23.05% | 36.62% | **13.57pp** |
| W2 higher-bucket cushion pass% | 62.98% | 52.91% | **10.07pp** |
| W3 higher-bucket cushion pass% | 49.52% | 44.61% | **4.91pp** |
| W1/W2/W3 lower-bucket cushion pass% | 99.24% / 98.64% / 99.44% | 98.68% / 97.77% / 99.29% | ≤0.80pp each |
| Pre-break published prints | 45 | 46 | 1 print |
| %OI cross-check max deviation | 0.096pp | 0.05pp | trivial (both ~rounding) |

**Two real, disclosed sources of divergence, reasoned from each report's own stated methodology
(not assumed):**

1. **Post-break date-fraction denominator differs.** Impl A's fraction is computed at the
   daily-labeled-panel level (`n_days` in the table above). Impl B's reported `n` (143/150, 136/148,
   139/132) matches Impl A's *print-level* classifier bucket counts almost exactly (A's own
   `n_higher`/`n_lower` = 143/155, 140/149, 141/135 — B's 143/150/136/148/139/132 line up closely,
   not identically), which reads as Impl B computing the post-break fraction over classified
   **TFF prints**, not labeled **calendar days**, at least for W1/W3. A print-level and a day-level
   fraction are not required to match exactly even under an identical classifier, because the
   boundary week straddling 2021-09-28 and any partial/holiday-truncated weeks assign differently at
   the two levels of aggregation. This plausibly accounts for the 1–4pp gaps on the post-break
   fractions. It does not change any Accept/Reject call: every one of these six values is either
   comfortably above the 75% floor or dramatically (34–46pp) over the 40% ceiling in **both**
   implementations — none is a close call at either level of aggregation.
2. **Per-bucket block construction was independently (re-)written by each team, not reused, and the
   two builds differ on contiguity handling for the smaller, boundary-adjacent higher-extremity
   bucket.** Impl A used "contiguous-run splitting + Monday-anchored 5-day blocks per run, matching
   `blocks_from_panel`'s own contiguity requirement." Impl B explicitly built a *different* selector
   because it judged `blocks_from_panel`'s contiguity assumption **wrong** for a scattered bucket mask
   ("feeding it a gapped panel would have silently paired non-adjacent calendar weeks"), and instead
   kept a 5-day block only when that week's Monday carried the target label. These are two genuinely
   different, defensible answers to an under-specified question the pre-registration does not settle
   (§2.3/§4 fix the classifier and the windows; neither fixes the block-selection algorithm for a
   non-contiguous bucket mask), and the resulting Monte-Carlo block sets for the higher-extremity
   bucket specifically — the smaller, more boundary-sensitive bucket — differ enough to move its
   cushion-sizing pass rate by 5–14 percentage points across all three windows, while the much larger,
   more homogeneously post-break lower-extremity bucket is stable to within 1pp between the two builds
   regardless of block-selection algorithm. **This is flagged as an open construction-method ambiguity
   for any future brief that needs the higher-extremity bucket's pass rate as a precise number** — it
   is not close enough to a threshold to change this Q's verdict (W1/W3 fail in both builds by a wide
   margin on date-correlation regardless; W2's `BOTH_CLEAR` sign-break fires under both builds'
   numbers), but a reader should not quote either implementation's higher-bucket pass% as *the*
   number without this caveat.

**Robustness of the verdict to this divergence:** H-ORBPOS's Reject condition (§4) fires on **two
independent clauses**, and both fire under **either** implementation's numbers alone:
(i) date-correlation fails at ≥2 of 3 windows — fails at 3/3 in both A and B; (ii) the gate-clearance
direction is not the same sign at every window — the W2 `BOTH_CLEAR` vs W1/W3
`LOWER_CLEARS_HIGHER_DOES_NOT` break is present in both A's and B's numbers, independent of the exact
pass-rate magnitudes. The magnitude disagreement above is real and should not be papered over, but it
does not create any verdict uncertainty here — swapping in Implementation B's numbers throughout
changes zero Accept/Reject/Ambiguous-hold routing decisions in §4/§6.

## Phase 4 — Verdict assertion (§4/§6 applied to the converged evidence)

- **Ambiguous-hold (§4 items 1–3):** none fire. Sparsity: 45–46 pre-break prints ≫ the 4-print floor,
  in both implementations. MNQ-not-separately-reported: does not fire (Phase 0 + both Phase-3 builds
  independently confirm the standalone `209747` line). Item 3 (fallback) is therefore moot — the
  Asset Manager secondary was never invoked, per §5's forbidden-move on switching category early.
- **Reject condition (§4):** fires on **both** independent clauses — date-correlation fails at 3 of 3
  windows (≥2 of 3 required), **and** gate-clearance direction sign-flips (W2 breaks the
  same-sign-at-every-window requirement set by W1/W3).
- **Accept condition (§4):** does not fire — date-correlation clears 0 of 3 windows (needs ≥2 of 3).
- **§6 verdict: `FALSIFIED`.** The 2021-09-28 break stays recorded as a real, triple-verified
  (Q-ORBCUSH-1 probe), now-thrice-refuted (volatility, mean-R, positioning) historical pattern with no
  tested causal explanation. Per §6/§9, this closes to
  [`docs/briefs/closures/Q-ORBPOS-1-closure-falsified.md`](../../../../docs/briefs/closures/Q-ORBPOS-1-closure-falsified.md)
  and appends `ops/instruments/MNQ.md` at **N20** (re-checked at closure time: N19 is the ledger's
  current tail as of 2026-08-23 — the pre-registration's own draft-time guess holds).
