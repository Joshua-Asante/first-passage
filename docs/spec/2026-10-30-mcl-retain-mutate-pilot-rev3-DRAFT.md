# MCL intraday retain/mutate versus fresh-rule pilot

**Status:** DRAFT FOR REVIEW, revision 3, 2026-10-30. Supersedes revision 2 (`2026-10-29-mcl-retain-mutate-pilot-DRAFT.md`, SHA256 `e327198f…127542a`) only by adding the fixed civil holiday calendar of section 3.1, after the MCL-1 preflight found holiday early closes (section 9). Specification only, no candidate scoring run.
**Must run locally:** the vendor panel and original export are private files on the operator's machine.
**Owner:** operator Joshua; the coordinating research agent owns combined technical acceptance.
**Authority:** direct operator instructions to draft this experiment and review/fix its methodological flaws and implementation ambiguities. Execution requires a subsequent authorized handoff against a reviewed, frozen specification.

## 1. Question, decision and bounds

Can a small, auditable retain/mutate search produce interpretable intraday MCL rules and useful component lineage, compared with an equal charged-budget fresh-rule control? The decision is whether this discovery workflow merits independent replication. One market, one pilot and one seed cannot establish general superiority of evolutionary search or an executable trading edge.

The research universe is futures, without a Tradeify restriction. This first experiment uses intraday MCL observations. Broader horizons, other markets and execution-venue selection are subsequent decisions. This is a continuous-series methodology pilot, not a deployment qualification.

Revision-3 budget: $0, one drafting pass plus calendar recomputation checks, with no vendor-data access; reuse the MCL-1 readiness evidence. Proposed future run budget: $0, 27 charged slots, one seed, two aggregate CPU-hours across calibration, generation, scoring and final diagnostics, including retries and child processes. Reaching 27 charged slots prohibits further proposals but permits completing those slots and the specified diagnostics within the CPU budget. At CPU exhaustion stop and return the partial ledger; do not expand the budget, replace failures or weaken acceptance. Implementation has its own future handoff and budget.

The primary method comparison is descriptive: report each arm's best eligible development score after cumulative slots 4, 8 and 12, its eligible/unique/null counts, and its frozen finalist's replay mean and disposition. Report grow-minus-fresh differences only where both quantities exist; missing finalists are not zeros. A shared finalist is a tie, not two independent discoveries. Any null slot means the comparison is equal in charged opportunities, not equal in actual evaluations. This tests the whole retention/edit package (including inherited direction and local neighborhood), not mutation or component retention in isolation. Mechanically reproducible completion establishes feasibility; promising replay results support a replication proposal. Neither establishes that one search method is superior.

The [MCL ledger](../../ops/instruments/MCL.md), [rejection registry](../rejected_candidates.md) and [MSL-S2A closure](../briefs/closures/MSL-S2A-closure-falsified.md) remain relevant prior exposure. That rejected construct used impulse/failed-pullback resumption, event sequencing and stop/target geometry. This pilot samples simple closed-bar state predicates at fixed clocks with fixed holding time; it does not retune or revive that construct, establish a causal mechanism, or discharge its new-mechanism-evidence re-proposal bar. Any later proposed strategy must explain its mechanism and relationship to those negative findings.

This is not an already-admitted GROW campaign. The [existing GROW specification](2026-08-22-grow-lane-generate-refine-spec.md) has a different scope and contract. Its implementation in [grammar.py](../../lab/discovery/grammar.py) supplies schema/hash checking, not a functioning evolutionary engine. Preserve full tested-width accounting and cross-campaign exposure disclosure under the [two-ledger decision](../adr/2026-08-22-grow0-two-ledger-k-question.md). The [2026-10-24 ruling](https://github.com/Joshua-Asante/first-passage/blob/5fbf00a3d96df140bccf1626625c1a686da40b81/docs/notes/2026-10-24-assumption-challenge-rulings-proposal.md) removes universal 4x-cost and standalone component Sharpe hurdles; neither is introduced here.

## 2. Provenance decisions and bounded audit

### 2.1 Input identity and timestamps

Audited 2026-10-29, on checkout HEAD `3141f5f5074451816fcaf66dd8220c87333c1eb9`, with unrelated working-tree edits retained. Governing newer documents were read from local `origin/main` at `5fbf00a3d96df140bccf1626625c1a686da40b81`; the checkout was not switched or merged. This identifies the inspected remote-tracking snapshot, not a fresh remote fetch.

| Input / check | Observed result |
|---|---|
| Panel | `core/data/bar_data/MCL_M15.csv`; 106,261 rows; columns `time,open,high,low,close,volume` |
| Panel SHA256 | `5aa504567b943ff68506b8b5c21df293c5a553543fdf1ac606adeb0f5bfbbd23` |
| Raw export | `core/data/tv_exports/cme/BAR_EXPORT_v0.2_NYMEX_MCL1_2026-08-13_3fd7c.csv` |
| Raw SHA256 | `5f44643c2d9ddab19885b35e81177d5614e99f96cc36fb08f359a9241889b37f` |
| Original comparison | Downloads original, filename containing `MCL1!`, 41,277,823 bytes; same SHA256 as raw copy |
| Transport / bar counts | 212,522 transport rows; 106,261 Entry records; zero malformed 17-field entries; 106,261 unique encoded bar-open timestamps |
| Panel correspondence | Sorted timestamps; zero duplicates; timestamp set exactly equals raw Entry set |
| Coverage, UTC bar opens | `2022-01-02T23:00:00Z` through `2026-07-02T00:00:00Z` |
| Encoded close minus open | 900,000 ms for all 106,261 entries |
| Metadata | Constant on every Entry; matches sidecar: `MCL1!`, futures, USD, empty base currency, tick .01, point value 100, `America/New_York`, timeframe 15 |

The [loader](../../core/bar_export_loader.py) documents Signal epoch as **bar-open UTC**, authoritative over the transport's chart-time `Date and time`. Encoded `time_close` is the bar completion time. Its Entry prices transport encoded closes; they are not strategy fills. The export filename's date is not the coverage end.

Audit commands: `./fp.ps1 doctor`, then `./fp.ps1 python -c $mclAudit`, where the PowerShell here-string used standard-library CSV parsing, hashes, timestamp sets, duration counts and metadata constants only. Both exited zero using `C:\Users\joshu\multi_firm_operations\tmp\ops-env\Scripts\python.exe`, Python 3.13.2. No features, outcomes, returns or price distributions were computed. This was a metadata check, not a full OHLC reconstruction or a scored verification suite; the launcher printed no `record.json` for this `python -c` command. The table is the bounded audit result, not a claim of recorded suite acceptance.

### 2.2 Historical exposure: uncertified replay

The closure and [archived results](../../lab/archive/msl_s2a_mcl_2026-08/RESULTS_g2.md) record exploration through 2025-06-30 and CONFIRM 2025-07-01 through 2026-07-02 unread at the 2026-08-13 closure. Its [construct code](../../lab/archive/msl_s2a_mcl_2026-08/construct_lib.py) agrees on that reservation. The closure did not authorize opening it.

Later chart/backtest exposure has not been certified. Bounded prior searches found no later MCL scoring, but private/archive history is incomplete. Absence from `discovery_manifests/burned_segments.json` is not proof of virgin data. Metadata inspection does not establish independence.

**Resolution:** call 2025-07-01 through 2026-06-30 an **uncertified historical replay**, never independent OOS or confirmation. Freeze nominations before its first pilot outcome read to prevent additional adaptation, while acknowledging that this cannot undo unknown prior exposure. A future execution handoff must explicitly include reading this formerly reserved period; this specification alone does not open it. This replaces the initial independent-holdout validation interpretation. Genuine confirmation needs a separately reserved, demonstrably untouched dataset/window and a new frozen confirmation contract before observation; no such window is identified or authorized here.

### 2.3 Continuous contracts and adjustment

The inputs contain no expiry-specific contract identity, actual switch map or recorded back-adjustment toggle. TradingView describes symbol-specific switching rules informed by volume patterns, which need not coincide with expiry ([switching documentation](https://www.tradingview.com/support/solutions/43000691027-how-is-the-switching-date-of-contracts-determined-in-continuous-futures/)). Its optional back-adjustment shifts prior contracts by a price difference at switching ([adjustment documentation](https://www.tradingview.com/support/solutions/43000685266-how-can-i-enable-backadjustment-for-continuous-futures/)); the documented default does not prove this export's setting.

**Fixed pilot policy:** use the pinned continuous panel as supplied, without reconstructed contracts, roll-date exclusions or price-jump filters. Do not apply the archived `ROLL_EXCLUDED` calendar: it is an expiry-near mask, not an authenticated TradingView switch map. No FOMC/news masks. The only date mask is the fixed civil holiday calendar of section 3.1. Apply only the common availability rules below, identically to all rules and baselines, and report their exclusions.

Same-day differences and the four features are invariant to a uniform additive price shift **within one contract segment**. `MCL1!` does not establish that condition across the whole feature/holding window. Therefore this policy admits possible splice contamination and supports continuous-series comparisons only. Before executable-contract or deployment claims, separately validate expiry-contract identity, adjustment state, switch handling and actual execution assumptions with suitable data. A later roll-aware re-run is a disclosed new analysis, not a result-dependent correction to this pilot.

## 3. Fixed observation, eligibility and execution model

All research dates and clocks below are `America/New_York` civil dates/times. Convert UTC with the IANA zone, never a fixed UTC offset; record timezone-data version in a future run manifest. Restrict scheduled dates to Monday-Friday, excluding the calendar dates of section 3.1. DST changes the UTC clock, not these local times.

| Decision | Last usable M15 bar opens | Entry open | Exit open |
|---|---|---|---|
| 09:45 | 09:30 | 10:00 | 11:00 |
| 10:45 | 10:30 | 11:00 | 12:00 |
| 11:45 | 11:30 | 12:00 | 13:00 |
| 12:45 | 12:30 | 13:00 | 14:00 |
| 13:45 | 13:30 | 14:00 | 15:00 |

A bar ending exactly at the decision is available; a bar opening at the decision is not. Assume computation finishes during the fixed 15-minute delay. At entry, use only the scheduled bar's open as the price proxy; its later high/low/close cannot affect the decision. Exit uses the open exactly one hour later. No stops, targets, overnight positions or intrabar ordering assumptions. At a shared boundary, close the previous trade then open the next, even if direction is unchanged; charge both round trips. Maximum one contract-equivalent at a time, five round trips per day. This measurement unit is not production sizing.

Define a scheduled opportunity's common **signal eligibility using only information available at the decision**, before testing any predicate:

1. Five consecutive 15-minute feature bars `t-4..t` exist, with `t` closing at the decision, all on that New York date. Every required bar has a 15-minute duration. No forward filling or searching for a nearby bar.
2. Feature bars have finite OHLC satisfying `low <= min(open,close) <= max(open,close) <= high`. Invalid existing OHLC is an input error that stops the phase; absent feature bars make the signal unavailable. Duplicated timestamps or inconsistent instrument metadata abort the input before loader deduplication rather than choose an arbitrary row. The existing loader's keep-last behavior is not this experiment's input policy.
3. All four feature denominators below are strictly positive and feature values finite. Otherwise the opportunity is unavailable to **every** candidate and baseline, including rules that do not use that feature.

Unavailable signals are excluded, not deferred. An eligible session is a New York date with at least one signal-eligible opportunity; daily metrics include zero for every eligible session on which a rule stays flat. Dates with none are excluded from all series, with counts/reasons reported. Partial days use their remaining signal-eligible opportunities. This estimates performance conditional on the frozen signal-availability policy, not on every exchange trading date. Report counts for every weekday in each phase, including dates with no opportunities, and missing-feature versus zero-denominator reasons. Do not alter that denominator after seeing rule outcomes.

**Outcome availability is a phase-level integrity check, never a trade filter.** For every signal-eligible development/replay opportunity, both scheduled entry and exit opens must exist and be finite, regardless of whether any candidate would trade it. Missing either stops that phase as `INCONCLUSIVE-DATA` before scoring any rule in it. Do not drop the opportunity/day, impute, delay the exit, or substitute the previous close. Only the two open prices are needed for the holding-period outcome; intervening bars and the exit bar's later OHLC cannot determine inclusion. Holidays/early closes are never removed using observed availability: the only date exclusions are the fixed calendar of section 3.1. An eligible signal on any other date without its scheduled endpoint makes the phase `INCONCLUSIVE-DATA`; any further calendar change requires a new version before scoring.

### 3.1 Fixed civil holiday calendar

Exclude every New York weekday in set `E` from every phase (calibration, development and replay) and from every rule and baseline, before any feature or outcome is read. An excluded date contributes no signals, no flat zeros and no eligible session; report it as calendar-excluded, separately from dates with no eligible signal. `E` is computed from civil rules, never from bar presence:

1. The observed date of each US holiday named in the CME Globex holiday schedule: New Year's Day, Martin Luther King Jr. Day, Presidents Day, Good Friday, Memorial Day, Juneteenth, Independence Day, Labor Day, Thanksgiving and Christmas Day. Fixed-date holidays use the federal weekend rule of [5 U.S.C. 6103](https://www.law.cornell.edu/uscode/text/5/6103) (Saturday to the preceding Friday, Sunday to the following Monday); weekday holidays use their statutory rules. Good Friday is two days before Gregorian Easter.
2. The Friday after Thanksgiving.
3. December 24 when it falls on a weekday.

**Source.** CME's [trading-hours page](https://www.cmegroup.com/trading-hours.html), read 2026-10-30, scope Globex 2026: "CME Globex trading hour and holiday schedules being observed for 2026." It lists exactly these ten holidays. Its windows of Thanksgiving 26–28 November and Christmas 24–26 December support items 2 and 3. The page serves 2026 onward only. No primary CME source for 2022–2025 hours was reachable, so `E` makes **no claim about CME's actual hours** on any date. It is a pre-declared, outcome-independent exclusion. Over-exclusion only removes sessions; under-exclusion is never repaired by inference, because the endpoint integrity check above stops the phase.

**Resulting dates**, 2022-01-03 through 2026-06-30, 51 weekdays. The run manifest recomputes `E` and must match this list exactly.

| Year | Excluded weekdays (MM-DD) |
|---|---|
| 2022 | 01-17, 02-21, 04-15, 05-30, 06-20, 07-04, 09-05, 11-24, 11-25, 12-26 |
| 2023 | 01-02, 01-16, 02-20, 04-07, 05-29, 06-19, 07-04, 09-04, 11-23, 11-24, 12-25 |
| 2024 | 01-01, 01-15, 02-19, 03-29, 05-27, 06-19, 07-04, 09-02, 11-28, 11-29, 12-24, 12-25 |
| 2025 | 01-01, 01-20, 02-17, 04-18, 05-26, 06-19, 07-04, 09-01, 11-27, 11-28, 12-24, 12-25 |
| 2026 | 01-01, 01-19, 02-16, 04-03, 05-25, 06-19 |

**Disclosed residual replay risk.** Two replay dates fall outside `E` and might lack scheduled endpoints:

- 2025-07-03, Independence Day eve, when NYSE closes early. The comparable development date, 2023-07-03, had no endpoint gap.
- 2025-12-26, when federal offices closed by executive order. That closure is not a 5 U.S.C. 6103 holiday.

Neither is added, because doing so would need an unbound source or inference from replay availability. If either lacks an endpoint, replay stops as `INCONCLUSIVE-DATA` under section 7. 2025-11-28, whose scheduled session a Globex outage disrupted, is already in `E`.

Calibration uses signal eligibility alone and must not inspect entry/exit prices. Development integrity checks are confined to development; replay feature/value/integrity inspection waits until nominations are frozen and replay access is authorized. Metadata-only timestamp/hash checks already recorded above are distinct from this future value inspection. Do not precompute full-panel features, candidate masks or outcome caches and then slice by phase.

At each eligible opportunity a rule trades its fixed direction when its predicate is true, otherwise flat. Gross ticks are `direction * (exit_open - entry_open) / 0.01`, direction +1 or -1. Keep floating-point ticks without rounding. Primary net ticks subtract **6 per completed round trip**, inclusive assumed friction; stress subtracts **8**. These are experiment assumptions, not broker quotes. Tick value inferred from metadata is `.01 * 100 = $1` per contract-equivalent; report ticks as primary units. Break-even round-trip friction is total gross ticks divided by trade count (undefined with zero trades). No cost-to-edge admission ratio.

## 4. Features, calibration and finite grammar

Let `r_i = H_i - L_i`, and `t` be the last completed bar:

| ID | Feature |
|---|---|
| F1 | Signed body: `(C_t - O_t) / r_t` |
| F2 | Four-bar displacement: `(C_t - O_(t-3)) / sum(r_(t-3)..r_t)` |
| F3 | Four-bar closing location: `(C_t - min(L_(t-3)..L_t)) / (max(H_(t-3)..H_t) - min(L_(t-3)..L_t))` |
| F4 | Relative range: `r_t / mean(r_(t-4)..r_(t-1))` |

No volume or cross-day input. Calibration is 2022-01-03 through 2022-12-30 inclusive. Pool the five decision clocks' signal-eligible feature observations with equal observation weight. Compute each feature's 25th, 50th and 75th percentiles using sorted observations `x[0..n-1]`, `h=(n-1)p`, and `x[floor(h)] + (h-floor(h)) * (x[ceil(h)]-x[floor(h)])`. No 2022 strategy returns, candidate scoring or threshold refinement. Abort if a feature has no calibration observations. Report observation counts per clock and quarter; pooling deliberately gives more influence to clocks with more available signals, without outcome-based reweighting.

Freeze thresholds as round-trip-safe binary64 values (hex plus decimal in the manifest). Exactly equal thresholds within a feature collapse to the earliest percentile ID (`Q25`, then `Q50`, then `Q75`); do not jitter. An atom is `Fi:Qxx:LE` or `Fi:Qxx:GT`. Equality belongs to LE; GT is its complement on finite observations.

A candidate has one or two atoms, two atoms joined by AND and necessarily on different features, and one fixed action L or S. Sort atoms lexicographically by ASCII. Canonical ID is action plus `|` plus atoms joined with `&`, e.g. `L|F1:Q25:LE&F4:Q75:GT`. The ID is scoped to the frozen threshold/spec manifest. Deduplicate by that ID, not by coincident realized trade masks. No action flip is a mutation. There are at most 24 atoms, 48 single-atom candidates and 432 two-atom candidates: 480 legal IDs before threshold ties. Enumerate legal syntax without scoring it.

## 5. Exact search, randomness and accounting

Use NumPy `Generator(PCG64(SeedSequence([20261029, stream_id])))`. Streams: 0 shared initialization, 1 grow edits, 2 fresh rules, 3 final bootstrap. Freeze NumPy version and save generator states. Each generation draw selects one scalar `integers(0, len(pool))` from a freshly ASCII-ID-sorted eligible pool; remove the selected item. Empty pools consume no RNG draw and produce a charged null slot. No dependence on set iteration order. Generation draws use syntax and charged history only, except the grow parent's specified development ranking. Process grow slots 1..4, then fresh slots 1..4, then score both arms' sealed round; round 1 draws shared seeds in order and charges both arms before scoring. Round 3 replacements process the better parent first, followed by the two recombinations. Baselines are charged/scored once before round 1 and cannot influence generation. Bootstrap stream 3 uses its separately specified with-replacement rule, not generation pool removal.

| Round | Grow arm: four charged slots | Fresh arm: four charged slots |
|---|---|---|
| 1 | Four distinct two-atom rules drawn uniformly from legal two-atom IDs using stream 0 | Identical four rules, each charged again |
| 2 | Top two round-1 parents, ordered by rank; for each parent, deletion then atom replacement | Fresh uniform rules with clause counts matching grow slots 1..4 |
| 3 | Top two retained grow parents across rounds 1-2; one atom replacement from each, then two recombinations of that parent pair | Fresh uniform rules with clause counts matching grow slots 1..4 |

Rank parents with the development ordering in section 6, including ineligible parents at the bottom. Retention is elitist across evaluated grow history, not a fresh scoring/ablation pass. A negative-scoring parent can be retained: retention means best available feedback, not validated usefulness. If fewer than two actual rules exist at a parent-selection boundary, stop as `INCOMPLETE-GENERATION`.

Deletion removes exactly one atom from a two-atom parent, keeps action, and draws uniformly among its unseen legal children. Atom replacement changes exactly one atom, keeps clause count/action, allows a different feature only if the resulting features are distinct, and draws uniformly from the unique unseen legal children. Different edit paths yielding one ID count once in the pool; record all equivalent edit paths.

Recombination makes a two-atom child by taking one atom from each retained parent, requiring distinct features, and an action drawn as part of the child ID from the set of the parents' actions. Enumerate the unique legal child IDs and draw from unseen IDs sequentially for the two slots. If no legal unseen recombination exists, that slot is charged `NO-PROPOSAL`; do not substitute a random rule or another operator. The same rule applies to any exhausted edit pool. Its intended clause count is two (deletion one; replacement the parent's count).

Unseen means absent from that arm's earlier charged rule IDs, including earlier slots in the round. Cross-arm collisions are allowed and remain charged to each arm. The fresh generator sees only grow's intended clause-count schedule, not scores, atoms, direction, lineage or outcome summaries. Its pool is all unseen legal rules of that count, irrespective of grow's `NO-PROPOSAL`; a fresh pool exhaustion also consumes its slot. This matches clause complexity, but the adaptive schedule is a disclosed coupling between arms, not fully independent search.

Charge a slot before evaluation. Structural invalidity after pool construction is an implementation error: stop, retain the charged ledger, and return for correction; do not silently resample. Trade-count ineligibility is a scored result and consumes the slot. `NO-PROPOSAL` consumes a slot without a candidate score. Generate all four rules in a round before observing their scores. No hidden candidates, free repairs, ablations or alternative seeds.

Three additional slots are always-flat, always-long and always-short baselines, using identical clocks/mask/costs. Maximum budget is **12 + 12 + 3 = 27 charged slots**, at most 23 distinct scored rule/baseline objects because four seeds are shared. Cross-arm collisions or null slots can reduce distinct count further; they do not refund budget. Cache reuse does not erase charges. Retain full planned/charged/evaluated/unique/null counts, rule IDs, parent IDs, operation, pool size, RNG state, round, trade counts and all five block results. Disclose prior MCL campaigns separately; unknown historical tested width stays unknown. Do not relabel the finalist as K=1. Final evaluation of frozen nominations is a consultation, not a new generation slot.

## 6. Development feedback and nomination

Development uses five fixed blocks: 2023 H1, 2023 H2, 2024 H1, 2024 H2 and 2025 H1. H1 is January 1-June 30; H2 is July 1-December 31. Repeated access to these blocks is adaptive development, not independent validation.

For each rule and block, let `x_i` be primary six-tick daily net ticks over the common chronological eligible-session sequence, including flat zeros. Let `n` be its length, `m=mean(x)`, and

```text
gamma_l = sum((x_i-m)*(x_(i-l)-m), i=l..n-1) / n
V = gamma_0 + 2 * sum((1-l/6) * gamma_l, l=1..5)
SE = sqrt(max(V, 0) / n)
L_b = m - SE
S = median(L_b across the five blocks)
```

This is fixed-lag-five Newey-West/Bartlett HAC, with denominator n, no small-sample multiplier, and lags measured in eligible sessions rather than calendar days. Require n >= 20 in each block, finite inputs, and at least 50 completed trades overall and 10 in every block for a rule to be selection-eligible. Zero variance yields SE=0. A tiny negative V within `1e-12 * max(1, gamma_0)` is clamped to zero; a more negative V or any nonfinite metric aborts as a computation error, not a poor candidate. An insufficient common block makes the whole pilot `INCONCLUSIVE-DATA` before candidate scoring. L_b is a one-standard-error ranking penalty, not a confidence bound; S is not a statistical significance test. Twenty sessions and the trade-count minima are operational floors, not power calculations. No HAC correlation crosses block boundaries; the five-block median deliberately favors repeatable block performance over the pooled mean.

Ordering: eligible before ineligible; eligible rules by higher S, then higher minimum block mean, then fewer atoms, then ascending canonical ID. Ineligible rules are ordered solely by fewer atoms then ID, with selection score recorded as unavailable (conceptually -infinity); they may supply parents to finish the bounded feasibility search, but cannot be finalists. No stress-cost or final-period feedback enters this order.

Nominate one eligible rule per arm from all 12 slots using that order, even if its score is negative. If an arm has none, record `NO-ELIGIBLE-FINALIST`; do not replace it with a new rule. Baselines use the same primary score and block-data requirements; cash is exempt from trade-count requirements and scores exactly zero. Select the fixed benchmark by highest S among eligible baselines, breaking ties cash, long, short. Cash therefore remains available even when both directional baselines score below zero. The baseline winner and finalist IDs are frozen together before replay access. A finalist need not beat cash in development to be evaluated; its result can fail the final diagnostics.

After nomination, report eight-tick development sensitivity and break-even friction for all evaluated rules without changing selection. These are fixed repricings of the same charged trade series, not additional candidate searches or alternative nominations. Component evidence consists only of recorded parent/child comparisons already charged, including signed changes in score, block means and coverage. Report a score difference as unavailable if either endpoint is ineligible; retain its descriptive block means and counts. An atom's contextual association is not an independent causal contribution. Explain surviving rules in ordinary language with counterexamples from the already recorded logic; do not run extra deletion, reversal or feature probes.

## 7. Frozen historical replay and diagnostic decision

Replay interval: 2025-07-01 through 2026-06-30 inclusive, divided into 2025 H2 and 2026 H1. Remaining July 2026 bars are unused. Only the two frozen finalists (if present) and the fixed benchmark are evaluated on replay. No substitution, threshold update, additional arm champion or candidate-specific exclusion after access. Record the consultation even if it fails or execution is interrupted.

First perform the replay integrity and common-session checks before any finalist scoring. If either half has fewer than 20 eligible sessions, mark the replay `INCONCLUSIVE-DATA` and skip outcome diagnostics; this does not erase the development result. Otherwise compute daily paired series on the common eligible dates: each finalist's six-tick net result and its difference from benchmark. Report trade counts and distinct active dates overall/per half, half-year means, full mean, eight-tick full mean and break-even friction. Means always include flat zeros. The paired arm-to-arm difference is descriptive only. If neither arm has a finalist, skip replay entirely and record `NOT-READ-NO-FINALISTS`.

For exploratory uncertainty diagnostics use 10,000 **paired non-circular moving-block bootstrap** replicates, length five eligible sessions. For N replay sessions, form all N-4 consecutive blocks. For each replicate in order, draw `ceil(N/5)` scalar starts with `integers(0, N-4)` (exclusive upper bound) using stream 3, with replacement, concatenate their five-session indices and truncate to N. Apply the identical index vector to every finalist and benchmark, retaining flat zeros and dates' ordering within blocks. Blocks may cross the half-year boundary; the half-year checks use original data, not bootstrap slices. No resampling within a trade or within a day. Non-circular blocks underweight edge dates; fixed length five may miss longer dependence, and eligible-session gaps are compressed. These limitations and the unstudentized percentile construction are retained for bounded exploratory diagnostics, not calibrated inferential guarantees. No block-length or bootstrap-method search is allowed.

For each of four planned claims (two finalists x positive mean / advantage over benchmark), the lower diagnostic bound is the .0125 empirical quantile of its 10,000 bootstrap means, with the same linear interpolation convention as section 4. This corresponds to one-sided 98.75% percentile bounds and nominal Bonferroni family alpha .05 for four claims. It does not guarantee finite-sample coverage, independence from prior exposure, or validity under nonstationarity. Keep all four allocations even when an arm has no finalist or both nominate the same rule; no alpha recycling. If cash is the benchmark, a rule's two claims coincide, but retain the conservative four-claim allocation. Strictly positive means strictly greater than zero, without epsilon relaxation. Nonfinite calculations are a run error. Constant nonpositive daily claim series fail that claim with their constant bound; a constant positive daily claim series, or a constant bootstrap-mean distribution for a nonconstant series, is uncertainty-degenerate and cannot receive a favorable label.

Per-arm dispositions, in order:

1. No eligible development finalist: `NO-ELIGIBLE-FINALIST`.
2. Replay phase integrity or common-session checks failed: `INCONCLUSIVE-DATA`; no outcome diagnostic acceptance.
3. Fewer than 50 replay trades or 20 in either half: `INCONCLUSIVE-SAMPLE`; still disclose available descriptive results, without a favorable label. Intraday trades are not independent samples; resampling remains at session level.
4. Any observed necessary condition fails (a defined lower bound <=0, either original six-tick half-year mean <=0, or original full-period eight-tick mean <=0): `DID-NOT-MEET-PILOT-CRITERIA`, specifying the failed checks; this is not proof of no edge.
5. Otherwise any claim is uncertainty-degenerate as defined above: `INCONCLUSIVE-UNCERTAINTY`.
6. Otherwise both lower bounds >0 and all mean checks >0: `PROMISING-HISTORICAL-REPLAY`.

Even disposition 6 is exploratory. It licenses a recommendation to design independent replication, not a confirmed profitability claim. A future genuine-confirmation contract must bind untouched dates, exposure controls, data/contract provenance and an independently justified uncertainty procedure; this pilot's bootstrap is not automatically qualified for confirmation. Its dates and authority cannot be supplied retrospectively. No bootstrap is run during specification authoring.

## 8. Future execution contract and review acceptance

Roadmap: review/freeze this specification; implement and verify the deterministic runner using synthetic inputs; run the bounded calibration/development under a separate handoff; freeze nominations and return; then run the explicitly authorized historical replay and return its diagnostics. Genuine confirmation and contract execution validation are later work with separate inputs. Access to this roadmap is not an execution dispatch.

**Selected outcome (current handoff, revision 3):** the revision-2 specification plus a fixed, outcome-independent holiday calendar that resolves the MCL-1 endpoint block.
**Prerequisites:** MCL-1 readiness evidence (section 9); unknown historical exposure, missing switch/adjustment provenance and unverified 2022–2025 CME hours remain explicit limitations, resolved by narrowing claims rather than guessing facts.
**Ownership:** this research agent drafts and checks; Joshua reviews the design; the coordinating research agent retains combined acceptance of future implementation and evidence.
**Verification:** source identity, metadata counts/hashes, formulas, slot arithmetic, deterministic edge cases, link targets and document diff. No candidate scoring or broad runtime suite is needed for this draft.
**Checkpoint:** return this draft with the three provenance resolutions and any remaining implementation ambiguity; at a budget or scope conflict, return immediately without expanding the study.
**Return boundary:** delivery for review ends this assignment. Implementation, calibration feature computation, candidate scoring and replay access require a subsequent handoff.

The future runner must persist this observable sequence in one private run directory under an existing gitignored `local_artifacts` location:

| Producer -> consumer | Required state / behavior |
|---|---|
| Frozen spec + input audit -> calibration | Spec/panel/raw/sidecar/code/dependency hashes, exposure label, RNG and timezone versions pinned; validate raw duplicates before decoding; verify phase-local decoded OHLC and timestamps match the panel before opening features. The earlier metadata audit did not verify OHLC correspondence. |
| Calibration -> generator | Immutable threshold manifest; source dates and available observation counts; no calibration returns |
| Generator -> scorer | Charged slot ledger written before evaluation, canonical IDs and lineage; four-rule round sealed before feedback |
| Scorer -> next grow round | Only development feedback specified above; fresh generator receives clause-count schedule alone |
| Development -> nomination | Full ledger, two finalist IDs or absent statuses, benchmark ID, and nomination hash written before replay |
| Frozen nomination -> replay | Explicit read authority and consultation timestamp; only frozen rules evaluated; no adaptive return path |
| Replay -> coordinator | Counts, full development width/exposure disclosure, diagnostics, failure labels and resource use; return for combined acceptance |

Existing loader and grammar code do not provide this transaction flow. Implementation must supply it. Persist charged slots, proposal IDs/nulls and pre/post RNG states atomically before score publication. The baseline stage and each complete eight-slot round publish feedback atomically; partial-round results cannot select parents. On crash, either the transaction exists and is reused, or the exact pre-state regenerates the identical proposals; it cannot create an extra attempt. A partially evaluated charged slot may be recomputed for the same ID and unchanged inputs/code, without becoming a new proposal. Count repeated compute against CPU budget and disclose interruption. Hash-mismatched state stops. A bugfix after feedback exposure is a revised, exposure-disclosed experiment requiring coordinator disposition, not a transparent resume with refunded slots or reset history. Replay machine access begins the consultation even without human inspection and remains recorded after a crash. A transient unchanged-code restart does not permit new nominations, a fresh seed or result-dependent exclusions.

Before any real scoring, synthetic verification must demonstrate: 09:45 uses the 09:30 bar and excludes the 09:45 bar; winter/summer clocks map correctly; a missing required 11:00 endpoint stops the phase without dropping a signal; a section 3.1 date yields no opportunity in any phase whatever bars exist, and `E` is recomputed from civil rules to the exact listed dates; future endpoint availability cannot change calibration thresholds; zero feature denominators exclude uniformly; duplicate input timestamps abort before deduplication; tied quantiles collapse deterministically; overlapping edit paths deduplicate by ID; exhausted recombination charges a null slot without an RNG draw; ineligible parents cannot become finalists; identical actions at 11:00 still incur two round trips; HAC and percentile calculations match hand-computable examples; shared RNG bootstrap indices preserve pairing; constant-positive claim series cannot receive a favorable label; partial-round interruption cannot alter proposals, nominations or charges. These are implementation acceptance cases, not tests executed by this draft.

## 9. Revision-2 review evidence

| Confirmed flaw / ambiguity | Resolution and contract trace |
|---|---|
| Future completeness removed signals and entered calibration selection | Signal-only eligibility -> frozen denominator -> missing scheduled endpoint stops the phase; calibration never requests endpoint prices. Example: valid 09:45 signal with missing 11:00 exit remains eligible and makes development/replay inconclusive, rather than disappearing from every rule's return series. |
| Existing loader silently deduplicates despite the proposed abort policy | Input validation must precede keep-last decoding; two identical timestamps are rejected, not accepted because the final panel is unique. |
| Equal charged budget was easy to mistake for equal evaluations or a pure mutation effect | Report null/unique/eligible counts and the three score checkpoints; compare the complete search packages descriptively. A null grow recombination and a valid fresh rule remain one charge each but different evaluation counts. |
| RNG order, phase access and crash semantics were underspecified | Fixed scalar draw order, empty-pool behavior and atomic round publication; no replay-value precomputation; changed-code resumes require a revised exposure-disclosed experiment. |
| Insufficient sessions had conflicting statuses; degenerate bootstrap could look conclusive | One ordered disposition rule separates phase data, trade-count sample floors, failed conditions and unavailable uncertainty. Identical finalist/benchmark series have zero advantage and fail; constant positive claims alone cannot pass. |
| Ranking penalty and nominal bootstrap levels could be read as calibrated evidence | Label HAC score as a ranking heuristic, preserve full search width, and require a separately justified confirmation procedure. Unknown exposure and continuous-contract provenance still limit all results. |

Review verification: document-only contract traces above, formula/slot arithmetic, local-link checks and inspection of the applied patch and new-file whitespace check. No vendor prices, candidate features, returns, calibration thresholds or bootstrap samples were computed during this review. The earlier metadata audit is reused as historical evidence, not claimed as a fresh input audit. Phase-local OHLC correspondence and scheduled-endpoint completeness remain future preflight requirements; the draft does not assert this panel is ready to score.

Review acceptance is a coherent, bounded design with these limitations visible. Execution acceptance additionally requires revision-bound synthetic evidence and private run records under the project's launcher/verification conventions. Public artifacts must not contain vendor bars, trade tapes or private data; retain such evidence privately and publish only permitted aggregate results and provenance hashes.

## 10. Revision-3 trigger and evidence

**Trigger.** The MCL-1 preflight ran on 2026-10-29 against revision 2, pinned by hash. It used `lab/discovery/mcl_pilot/readiness.py` (12 synthetic acceptance tests passing) and about 6 CPU-seconds of the two-CPU-hour budget, with private report at `local_artifacts/mcl_pilot/mcl1-readiness-20261029/readiness.json`. It decoded calibration and development bars only, and the replay interval was never decoded. Results:

- Calibration was `READY`: 23,629 bars matched the panel exactly, with 258 signal-eligible sessions.
- Development was `INCONCLUSIVE-DATA`: 58,961 bars matched exactly, with 643 eligible sessions, but 27 scheduled endpoints were missing on 21 dates.
- The missing endpoints were the 15:00 ET exit on 2023-01-16, 02-20, 05-29, 06-19, 07-04, 09-04 and 11-23; on 2024-01-15, 02-19, 05-27, 06-19, 07-04, 09-02 and 11-28; and on 2025-01-20, 02-17, 05-26 and 06-19.
- On 2023-11-24, 2024-11-29 and 2024-12-24, the 14:00 and 15:00 ET opens were missing.
- No zero-denominator exclusions occurred. Weekdays with no eligible signal were 2022-04-15 and 2022-12-26, and in development 2023-01-02, 2023-04-07, 2023-12-25, 2024-01-01, 2024-03-29, 2024-12-25, 2025-01-01 and 2025-04-18.

**What the trigger exposed.** Only timestamps and bar existence were seen: no features, outcomes, returns, thresholds or prices. The calendar was then defined from civil rules and the CME holiday list, not from that dated list.

**Consistency check, not derivation.** Within development, `E` equals the union of the 21 gap dates and the 8 development no-signal weekdays exactly. The 2 calibration no-signal weekdays also fall in `E`. Calibration never checks endpoints, so the 8 other calibration-year dates in `E` carry no availability evidence either way. The coincidence follows from CME's holiday practice; `E`'s rules were not edited to match it. No federal holiday outside CME's list (Columbus Day, Veterans Day) is excluded, and none showed a gap.

**Alternative not chosen.** Trimming only the opportunities whose endpoints fall after a published halt would keep more holiday-session signals. It needs per-date energy halt times for 2022–2025, which no reachable primary source supplies, and it keeps thin holiday sessions in the sample. Whole-date exclusion needs only date membership.

**Acceptance for this revision:**

- `E` recomputes to the section 3.1 table.
- The diff from revision 2 is limited to the status line, budget line, section 2.3 mask sentence, section 3 and 3.1 calendar text, section 8 handoff lines and synthetic case, and this section.
- Joshua accepts or rejects the calendar policy and its residual replay risks.

After acceptance, MCL-1 is re-run under revision 3, with the adapter implementing `E` and its synthetic case. READY-FOR-BUILD requires both phases `READY`.
