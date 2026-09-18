# F1 human-reviewable candidate

**DRAFT — NOT FROZEN — NOT AN EXECUTABLE MANIFEST.** G1–G5 schemas and validators
now exist; this Markdown remains a human-reviewable proposal, with actual inputs
and combined acceptance still outstanding. It is not `tb-i1-shared-manifest-v1`, FBR, EF, a signed admission
or a result seal. `compute-observation.json` likewise has an explicit preparation
artifact class and lacks every qualification approval/result schema.

Historical identities are read-only observations originating at `c86a0a0`.
Current implementation checkpoints are in [tooling-review.md](tooling-review.md),
source/startup obligations in [production-readiness.md](production-readiness.md),
and provisional timing in [representative-workloads.md](representative-workloads.md).
Fields marked
**awaiting final binding/acceptance** must be replaced by the named owner and validated as
specified; merely hashing moving code does not close them. Source keys are in
[requirements.md](requirements.md).

## Book, sources and shared rules

| Field | Candidate value / evidence | Finalization owner and replacement check |
|---|---|---|
| Book/policy | Tradeify portfolio; K=1; `tradeify_portfolio@Tradeify_Select_100K`; canonical row `{"instance_key":"tradeify_portfolio@Tradeify_Select_100K","reference_mode":"trailing","scale":"0.4","trigger":"0.01"}` | F1 verifies candidate threaded and registry empty; D0 alone later admits |
| Legs and priority | `aegis_6j` sell, 6J, priority1; `dj30_mym_p250` buy, MYM,2; `vanguard_mgc` buy,MGC,3; `orb_mnq_v7` buy,MNQ,4 | Full `BOOK_LEGS` and accepted config bytes; one controller per symbol, independent hedging check |
| Pine identities | Aegis `db78ecba95ae78aca14501a5eaccfda2a42164d83cac12321cb7f293a9adca7c`; Striker `712cf395396568ce22ae43f1f15b085eaba23acf1b85502abb92129f277fffd7`; Vanguard `af26899ca94bb0e9ee26d09e0176b6b94bba2f5da252399ce4d899fe7e3bad15`; ORB `176c4f70c67d58053c4d3b8170d0a9be3733bc6b76b1e2f928bd7a877be052a3` | Phase 1 retained artifacts; full hashes from production book table; no source copies |
| Seven bundle identities | O-N/O-P/S-P/S-W1/S-W1P/S-W2/S-W2P; exact manifests, Pine/ports/panels/exports/Inputs/Properties/coverage and 19 runtime pins in [ledger](identity-ledger.md) | Preserve formal contract `4f027a…`, review `dd9c5e…`, result `8ddf72…`; inspect full ledger hashes, not abbreviated identities here |
| Runtime ports | Phase 2 reports Aegis `11763740bc3fdcc8b9e94cb0b465823aec202cd8333379c46878185db5e9e84f`; Vanguard `e6a03d04c65a19e7fde71103560a229630c3663f445676f06622feec4e9157a3`; ORB `b1f4e573009e62b976013e08e7ef2784497d840f490f04e3878fdaef553f317d`; corrected Striker `efd479b6b4c7eeaa7d8df3f40f36593f87d96b9d5f512dc79c4dd9b0520211f4` | Corrected registry and separate qualification loader implemented; original Striker `c81aa5…` remains a refused historical generation. **Awaiting final binding/acceptance** of affected parity and actual retained bytes on the adopted runtime; never change historical bytes |
| Effective inputs | Historical `66406dee955fa69f237fde60eacdd24259a08d5320352d98e59889acaa18158d` remains historical provenance, including ORB quantity2 | Separate qualification loader is implemented; actual reviewed successor settings and scoped review must bind fixed ORB quantity1. No fallback to historical settings |
| Panels and startup | Four-leg pins and accepted Step 3 full-origin evidence in ledger, including Aegis attested88-bar prefix derivative and MGC panel. Accepted cold origins2022-09-01T00:00Z; original unprefixed6J starts23:00Z and is not a substitute | Bind exact accepted source derivative, pool and exclusions. Proposed qualification startup uses each native cold constructor once per assembled path, preserving state through every splice; no unscored prelude or per-block prefix. See production-readiness for model/impact acceptance; historical full-origin parity is not arbitrary-start parity |
| Prior-close protection | Inclusive six-decimal DD compare against own running EOD peak; mode from prior close, no intraday switch/latch; carries unchanged; entering PROTECTED cancels resting ORB adds | I2/Phase 2 native mode/cancel tests, source/path clock separation, exact settlement in live context |
| Quantities | Aegis floor(8×scale×lifecycle), no adds; Striker floor(unrounded risk×scale×lifecycle/per-contract risk), capped by floor(cap_alloc/3.5), one add floor(confirmed base×2.5); Vanguard floor(normal base×scale) only AUTHORIZED, WATCH=0, at most two normal adds each max(1,Pine round(confirmed base×.8)); ORB fixed normal base1 with lifecycle floor, at most two one-for-one normal adds, adds off in PROTECTED | Shared `entry_quantities`/`add_quantity`, half-away-from-zero Pine rounding, zero refusal and executed-base evidence; no normal-integer reconstruction of Striker risk; Vanguard adds only AUTHORIZED/NORMAL with positive base |
| Capacity | 80 gross micro equivalents; 6J=10, others=1; confirmed+reserved; refuse never clip; Aegis whole-leg lowest-priority-first takeover after terminal/quiescent proof. Protected Striker can reach22+55=77, so protected Aegis30 can require takeover | Shared ledger and replay takeover/partial-fill tests implemented; final account-owner/replay composition and actual configuration acceptance remain required |
| Allocations | S1 §2 fixes offline Striker ceiling80; **DRAFT proposed upper request allocation80 per other leg under a single shared cap80**, not four independent allocations or live registration | I2/F1 must establish exact accepted per-leg `cap_alloc` configuration and parity consequences; production remains0 until V1; preserve ruled Striker ceiling |
| Lifecycle/modes | Decision-bearing AUTHORIZED×{NORMAL,PROTECTED}; WATCH-1=.5/WATCH-2=.25 parity/control only; RETIRED=0; Call-4 off-rail | Complete reachable-state coverage, monitoring definitions; no extra winning cell |
| Fills/costs | Native parity-validated TV OHLC path, gap fills and THIS_CLOSE/NEXT_OPEN semantics; full fills. Venue per-side costs6J3.10, MYM/MNQ.91, MGC1.06; per-side slippage1 tick except MGC3 (captured config) | Freeze commission schedule and configuration hashes; exclude Pine-cost literals as venue proxy; accepted scheduler fills at exact flatten instant |
| Intraday risk/kernel | Lifetime-scoped side-aware adverse marks combined without favourable netting; close-only entry has zero prior-bar excursion; `simulate_path` gets explicit initial state and `dd_scale=1.0`, no double scale; inactivity OFF, weekly idle counts descriptive | Continuous marked replay and kernel caller tests implemented and bounded-reviewed; actual source/runtime binding and final composition acceptance remain required |

## Calendars, schedule and initialization

| Field | Candidate / disposition | Validation |
|---|---|---|
| D19 / overlay / forward | Exact hashes in ledger; D19 immutable membership; overlay no-trade dates2023-04-07/2025-01-09/2026-04-03; forward digest `650e8aab4166f74a988675a3f3dfa2dbd21c1c1b342777ac37d65aacea9d6f2f` | TB-C1 accepted artifact and source coverage; no September-to-history extrapolation |
| Forward limit | 2026-09-02T22:00Z..2026-09-30T21:00Z; review due2026-09-24T21:00Z; September7/8 denied, ordinary18 permitted; v1 evidence warning retained | Exact ratification row, product/venue clock checks; future v2 extension separately qualified |
| Schedule | America/New_York; V earliest applicable source-backed deadline; D=min(16:00,V−15min); cutoff D−15; flatten D−5. Regular15:45/15:55/16:00; verified V12:59→12:29/12:39/12:44 | I2/Phase 2 prove same behavior/costs; 16:30 reconciliation only; no next-bar scheduling substitution |
| Full and halves | DRAFT source2022-09-01..2026-09-02, panels ending2026-09-03T00:00Z; H1 first ceil(N/2) accepted venue sessions and H2 remainder | I2 supplies exact N/index hashes, late-origin and exclusion dispositions; halves partition source sessions, not MC counts |
| Horizon and clocks | DRAFT500 covered business sessions; speed200; unresolved at cap failure/T=∞; source metadata immutable, monotonic unique path times | I2/coordinator must settle unavailable-session clock treatment and historical/path/forward coverage under P1§5/S2RC-7 before F1; neither a Gregorian500-day extrapolation nor missing-session compression is assumed |
| E1 state | DRAFT `EvaluationState(original_basis=100000,current_equity=100000,historical_eod_peak=100000,prior_trade_days=0,prior_max_day_profit=0)`; synthetic pristine screening class, not a claim about actual account | Basis matches current firm config; first policy mode NORMAL; freeze before E1. Optional used-state alternative requires operator authorization and trusted T1 seal before F1 |
| E2 state | **LATER** fresh B7 used-account snapshot, historical peak from approved source; no state values here | n3 after B7, same FBR, valid seal/no activity; not an E1 prerequisite |
| Ongoing settlement | **EVIDENCE missing** timezone/query endpoints, Sep14 close equity or same-boundary flatness, correction/finality | Phase 1 sources + Phase 2 atomic chain/consumer acceptance; no proxy reconstruction, no inferred actual close from calendar |

## Seeds, populations and bootstrap proposals

Workload and namespace choices in this section remain **DRAFT**; no qualification
stream has been consumed. Synthetic replay, benchmark and TEST_ONLY composition
namespaces have been exercised separately.

| Stage | Seed string; 64-bit hex = first16 SHA-256 hex characters | Depth/workload |
|---|---|---|
| n1 | `tradeify-f1-candidate-2026-09-15/n1/v1`; `3b6703de180cd7a3` | 200 FULL+200 H1+200 H2=600; continue iff each failure count≤10 |
| n2 | `tradeify-f1-candidate-2026-09-15/n2/v1`; `04aa31d0f99d8164` | 970 each=2,910, plus distinct Part A children; Part B is H1/H2, no duplicate draws |
| n3 | `tradeify-f1-candidate-2026-09-15/n3/v1`; `913c1a2c6484edf1` | 970 each=2,910 later, speed reuses FULL; no Part A rerun |

The implemented `regime.domain_seed` recipe is `tb-s2-rng-v2`: SHA-256 of compact
JSON `[recipe,purpose,synthetic-or-qualification,root,stage,population,panel_index,path_index]`,
using its first eight bytes as an unsigned big-endian seed for the pinned Python
`random.Random` sampler. This supersedes the earlier unimplemented counter-generator
proposal; F1 must freeze the actual root and runtime/recipe vectors. The three
candidate label rows above are not an executable seed allocation or a ratified
replacement for `root_rng_namespace` plus stage discrimination.

Implemented seed populations are FULL/H1/H2 and purposes path/outer/probe. Part A
uses stage n2, population FULL and an explicit panel index; REGIME is its retained
result-population label. The maximal panel/inner seed plan is bound before dispatch;
actual panel identities and retained initial/expanded prefixes enter receipts.
Part B reuses the joint n2 half results. Synthetic and qualification domains are
distinct; engineering does not consume qualification n3. Deterministic domain
separation is not a mathematical proof of independence. Freeze all intended
namespace bindings and the once-only consuming controls before F1.
Monitoring root `tradeify-monitoring-candidate-2026-09-15/v1` and synthetic root
`phase3-preparation/synthetic-component-benchmark/v1` are separate from all three.

**Joint-flat proposal:** moving blocks of five consecutive eligible venue sessions,
uniform over the enumerated eligible starts, replacement, independent FULL/H1/H2
pools; concatenate to500 and truncate only the final block at a session boundary.
Each start/end must have every leg flat and no working order. Preserve all four
bar panels jointly, source timestamps/TOD/holiday/reset metadata and continuous
indicator/paper/account state. A removed/missing session must not silently become
adjacent to another: the final I2 index must state its treatment, prove coverage,
and satisfy the unresolved clock rule above. No separate normal/protected-path splice.

**Part A proposal:** for each full-source session start with six calendar months
available, end at the first session on/after the date six months later (day clamped
to destination month's last day); block is half-open [start,end). Enumerate only
complete contiguous qualified blocks, preserving the joint four-leg bars. Uniform
replacement sampling of that index; concatenate until original full-source
venue-session length N, truncate last block at N. Rebuild every five-session
inner window on that alternate panel independently, including artificial outer
seams only where accepted joint-flat/coverage conditions hold. Do not recycle the
original inner-block list. Inner draws produce continuous500-session paths with
fresh pristine state per path; maintain state within each path, not across paths.
Synthetic tests validate duplicate/reversed source dates, continuous state,
partition invariance and monotonic path-session identities. Actual source joins,
startup applicability and final composed acceptance still require their own evidence.

The construction has an implemented synthetic pipeline, **not authority for an
unreviewed substitution or invented source coverage**. F1 still binds exact
outer/inner start lists, coverage joins, startup model and runtime. The coordinator
resolves any inability to satisfy joint-flat requirements before freeze. No real
panels are executed to choose these rules.

Part A candidate d=200 paths/panel; initial100 alternate panels; p5 is sorted
inverse empirical CDF (nearest rank `ceil(.05*m)`, one-based, no interpolation).
If `abs(p5−.95)≤.01`, append reserved panels100..199 and recompute p5 on all200;
only this prescribed expansion is allowed, never further panels/path top-ups.
Final p5≥.95 and p5≤n2 FULL point pass rate; H1/H2 source counts partition N.
Sanity failure is a contract/integrity stop for adjudication, not permission to
resample. Part B uses n2's existing970-per-half exact bounds. Exact proposed
depth and compute decision are in [compute-depth.md](compute-depth.md).

## Monitoring and stress battery — frozen-before-results proposals

All rows below are **diagnostic/monitoring only**, never extra n3 acceptance tests
or candidate alternatives. Proposed replica count:200 paths per FULL/H1/H2 pool
for each perturbation cell (600/cell), horizon500, pristine diagnostic state;
same base cost/model except the named perturbation. Child namespace
`monitoring/<cell-id>/<population>/<replica>/<purpose>`; RNG recipe above.
Order variant IDs lexically and reject duplicate cells. No adaptive repeats.
Unresolved attempts count as failure and T=∞ in every reported bound; unavailable
inputs/implementation produce `BLOCKED diagnostic`, retain reason and no number,
never drop a replica or falsely assign PASS. Freeze feasibility for the whole
battery before results even though its execution is later.

| Cell IDs and exact unit/scope | Partitions / perturbation | Statistic, cutoff, severity and action |
|---|---|---|
| LOYO/2022..2026 (5) | Drop each source-date year within the frozen pool; 2022 startsSep1,2026 endsSep2. Rebuild blocks separately; exact surviving index hash required | FULL one-sided95% failure upper bound; WARN if>.075; operator review, no re-selection |
| DEP/2, DEP/10 (2) | Five-session base length×.5 rounded down with minimum1→2; ×2→10; only eligible joint-flat starts | FULL/H1/H2 failure upper and FULL speed lower; WARN if any crosses .05/.50; down-only monitoring review |
| COST/combined (1) | Commission1.5×; slippage2×; conservative stop-first same-bar order; each add receives floor(.5×requested) contracts, zero means no fill, remainder cancelled; base/exit fills otherwise unchanged | FULL failure upper>.075 → WARN and operator review; stress implementation must preserve capacity/residual protection |
| OUTAGE/drop-entry (1) | Independent Bernoulli.05 per new base-entry intent per replica/leg after signal generation, before reservation; no drop on exit/protection; resulting absent base prevents its adds | Descriptive bounds and realized dropped-entry count; no verdict/severity/automatic action |
| OUTAGE/missed-session (1) | One eligible session chosen uniformly per source-month occurrence in each assembled path; all four legs new entry/add blocked that session, exits/protection continue | Descriptive only; report selected sessions/blocks privately; no automatic action |
| REMOVE/leg/<four IDs> (4) | Remove each leg's new entries for entire diagnostic path; remaining shared capacity recalculates, no replacement leg | Descriptive only; never candidate promotion or runner-up |
| REMOVE/best-trade,best-month,best-year (3) | Postprocess each diagnostic base replica's realized ledger: remove the highest net-contribution closed trade/month/year, ties earliest source-time then leg ID/trade ID; aggregate by source metadata, not wall-clock run date | Descriptive cashflow/attribution only; **not a counterfactual replay or acceptance bound**; no severity/action. Removal side effects on strategy state are not claimed |
| DOWNSIDE (0 extra paths) | On unperturbed retained diagnostic records: consecutive path sessions whose total net return<0; conditional co-loss for ordered leg pairs P(loss_j\|loss_i), denominator count explicitly reported; zero denominator→undefined | Longest run and pairwise conditional proportions; descriptive, no cutoff/severity/action |
| SEAM/<seam-id> (M, awaiting index) | Each evidence-backed contract-month seam ±2 source sessions excluded separately, rebuilt blocks/coverage; exact index/digest and M required before F1 | All failure/speed bounds; WARN if any crosses acceptance value; operator review; no optimization |
| Predictive interval (no new paths) | q10/q50/q90 inverse ECDF of unconditional T from sole n3, failures/unresolved∞; clock starts first venue session after verified effective activation | Completed pass before q10 or elapsed covered sessions>finite q90 without qualifying→model-fitted proposal falsified, operator review; AUTHORIZED may downshift WATCH-1, never upward. Infinite q90 no finite upper trigger. Bust/terminal stop/recovery and fresh GO remain independent |
| Lifecycle (no new paths) | Call-1 k=1.0, two consecutive windows; runtime window definitions/baseline PF and sigma inputs still require owning monitoring artifact before F1 | Only WATCH-1/.5, WATCH-2/.25 downshifts; RETIRED operator-only, Call-4 off-rail; never continued trading after account terminal failure |
| Weekly/calendar upkeep (no new paths) | Weekly token trade unmodelled; missed venue week alarm. Fail closed after calendar coverage; review-due warning retained | Operator obligation, not an automatic token order or source approval |

There are17 parametrized non-seam cells. Proposed compute reserve is
`600*(17+M)` path evaluations, plus metadata/postprocessing and any separately
enumerated unperturbed diagnostic replicas. To avoid an unbudgeted baseline, use
the same200-per-population paths underlying COST's unperturbed paired input as
the baseline, with a separate baseline run cell: **total18+M cells,10,800+600M
paths**. Pairing is confined to the monitoring namespace, never n2/n3. The exact
M, all transformed indices and the monitoring CPU-hour ceiling remain F1 fields
owned by I2/F1, with source-proven seam mapping from Phase 1. A method proposal
does not pretend that a missing seam inventory or lifecycle window is implemented.

Continuous-roll limitations carried verbatim from P1§8:

> Phase 3 pre-registration states back-adjustment seam risk as a limitation of every campaign claim: fills cannot be attributed to a contract month, and a seam crossing is indistinguishable from a price move.

> A Phase 6 seam-sensitivity check is pre-registered with its severity frozen alongside the other Phase 6 cutoffs.

## Fingerprint inventory and trust boundary

Use the existing `ops/c1_rail/policy_fingerprint.py`, recipe
`tb-i1-canonical-v1`. Canonical policy has exactly the four strings above, sorted
compact UTF-8 JSON, no BOM/newline, `ensure_ascii=False`, `allow_nan=False`.
Geometry: frozen CPython `ast.parse(mode='exec',type_comments=True)`, exactly one
validated literal top-level registry binding removed, then `ast.dump` with fields,
without attributes/indent, UTF-8/no newline. Ordinary comments/whitespace are
absent from this AST representation; every other AST node/type comment remains.
Full bytes for `book_policy.py` and every unexcluded shared component. No other
normalization or private artifact edits are allowed to make hashes match.

The fingerprint helper's minimum seven-file inventory is insufficient for F1.
Final manifest must include all rule/sizing/capacity/protocol inputs; all actual
ports/adapters/helpers and effective settings; replay/barrier/emulator/marking/
sampler/kernel code; allocation and lifecycle configuration; panels/source
admission/warmup/coverage indices; calendars/overlay/source schedule and costs;
seed/partition/PartA/monitoring definitions; exact lockfiles/runtime distribution,
stdlib/dependencies, tool source, serializer and vector digests. Identify each
file by canonical relative path and full SHA-256 except the two defined policy/
geometry normalizations. Secret/account contents are private, with permitted
public digests only.

The original component and repeated representative benchmarks used CPython3.12.14
on Windows; later bounded integration tests used CPython3.13.2 with their recorded
dependency path. **Neither observation freezes the qualification runtime.** Phase 2/I2
must provide one executable patch/native-distribution/dependency identity across
F1/E1/D0/B7/reseal/arm consumers, or resolve the incompatibility before freeze.
Observed source/vector hashes are in [compute-observation.json](compute-observation.json).
The actual-source tool/runtime/dependency inventory and final accepted integrated
head remain **awaiting final binding and combined acceptance**. Loaded-origin and
retained-byte collection is implemented; source provenance alone is not captured
execution authority. Rehash actual loaded artifacts, run literal vectors and
complete-manifest drift rejection, and accept the signed full composition under
the final runtime before freezing it.

Registry validation must separately authenticate complete expected contents and
provenance, including both P2 dates, contract digest, E1 freeze date/FBR. Never
derive expected rows from the inspected source. Pre-D0 expectation is `{}`.
Config serialization has no excluded keys; initial arm changes only `dry_run`
and the authorized `armed_until` from the verified disarmed config. Exact real
before/after vectors and boot-bound acknowledgment/GO checks remain I3 acceptance
evidence; the helper's pure byte comparison grants no authority.

F1 contract digest, FBR and EF entries deliberately remain **not issued**.
FBR later includes the frozen contract, canonical policy/geometry and n2/Part A
result digests; EF1 binds execution/image/config/B7 with every shared component
equal; only the approved GO-only reseal may make EF2. No self-referential tool
digest or extra fingerprint exclusion is introduced by this packet.
