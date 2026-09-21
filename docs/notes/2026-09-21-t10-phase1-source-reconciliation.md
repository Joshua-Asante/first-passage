# T10 Phase 1 — source reconciliation, coverage-and-clock proposal, canonical inventories (F01–F52)

Date: 2026-09-21. Worktree `.claude/worktrees/t10-source-freeze`, branch `claude/t10-source-freeze`, HEAD `1da555d` (tree dirty by design: this note, the requirements addendum and the packet §7 return only). Executor: T10 phase 1 (steps 1–3 of the packet). Step 4 (representative measurement) and phase 2 are **not** this dispatch.

Preparation only. Nothing here freezes F1, accepts Phase 2, approves a bundle, a budget, a horizon, a depth or a calendar extension; no replay, test suite or qualification draw was executed; no frozen definition, hash, threshold, seed or depth was changed; no account figure, identifier or P&L is quoted. All hashes below are reported as **fresh working-tree byte hashes** (the identity ledger's own convention — 13 of its 19 supplementary pins reproduce exactly under it on this checkout; git blob identities differ for some files under eol checkout filters, so the working-tree convention is used throughout for comparability with the ledger).

An earlier partial run of this note (step 1 skeleton, all cells TBC) was found in the worktree; it is superseded in full by this document.

## Method

Baselines: `d107ebdfaec194ac4b4448d1d121331ff7128e1a` (the owner registry-correction commit; also the independent provenance review baseline) and the identity ledger's 2026-09-15 pins. The ledger already pins the seven bundles, the four ports, the 19 supplementary runtime files and the six calendar artifacts; this note does not re-derive any pinned value — it establishes only **what moved since**, by `git log/diff d107ebd..HEAD -- <path>` plus fresh byte hashes. Private evidence roots are absent from this worktree (see Missing producer facts); nothing private was read, copied or invented.

## Step 1 — Seven-bundle reconciliation (F07/F10/F11)

Ledger facts reused, not re-derived: all seven Step 6 manifests hash as pinned; the five Striker bundles bind corrected port `dj30_mym_p250.py` = `efd479b6b4c7eeaa7d8df3f40f36593f87d96b9d5f512dc79c4dd9b0520211f4`; the two ORB bundles bind `orb_mnq_v7.py` = `b1f4e573009e62b976013e08e7ef2784497d840f490f04e3878fdaef553f317d`; the stale original Striker runtime identity is `c81aa59c811dd2f318bf2f6b51e9df32fca20315ffab0885ec1d4ec6a2ab5379`, a distinct byte identity the owner corrected in the registry at `d107ebd` without asserting semantic equivalence.

**Registry state at HEAD** (`ops/c1_signal_daemon/book_adapters.py`, worktree hash `c6ad40bd54d11545…`, last touched `7ba7844`): the four `AdapterSpec` pins are **byte-identical to `d107ebd`** — Aegis pine `db78ecba…`/runtime `11763740…` (:39–41), Striker pine `712cf395…`/runtime `efd479b6…` (:44–49), Vanguard `af26899c…`/`e6a03d04…` (:51–54), ORB `176c4f70…`/`b1f4e573…` (:55–59). The stale-byte refusal is present twice: the comment "The preserved original private port is c81aa59c... and must fail" (`book_adapters.py:46-47`) and enforcement — `load_port` now hashes the port bytes and raises `ValueError("port … does not match the accepted runtime identity")` **before** any execution (`book_adapters.py:121-123`; at `d107ebd` the check ran after module exec — the I1 repair landed). What moved in the file since `d107ebd` is: loader mechanics (I1 hash-before-exec repair), a **new derived runtime effective-inputs digest** `RUNTIME_EFFECTIVE_INPUTS_SHA256 = 9d4d4e1d…` (ORB base quantity bound to the shared fixed-book law; historical `66406dee…` retained as immutable provenance), and a TEST_ONLY qualification composition path (commit `7ba7844`).

**Port modules**: `ops/c1_signal_daemon/ports/` is gitignored except its README — the four port files "live … nowhere in git". `git log d107ebd..HEAD -- ops/c1_signal_daemon/ports/*.py` is therefore empty **by construction**, and the live bytes are unverifiable from this worktree (primary-checkout paths named under Missing producer facts). Git can testify only about the registry pins, which are unchanged.

**Parity evidence by reference** (nothing re-run):
- Track B / PR #356 (`docs/notes/2026-09-11-track-b-adapters-and-book-rules.md` §Verification): four ports replayed through `tv_broker_emulator` on frozen panels vs captured TV exports — orb 681/681, striker 203/203, vanguard 338/338, aegis 121/121, all PASS. **The striker row of that run executed the original `c81aa59c…` bytes** (the note's own port table pins Striker at `c81aa59c…`); it is evidence for the original generation, not for `efd479b6…`.
- Accepted Step 3 (nine references incl. the corrected Striker ports): contract `acfa7920…`, index `95ac6dcb…`, independent acceptance `ebcb2efb…`; port/panel/export triples re-checked against it by the ledger.
- Accepted Step 6 (the seven bundles): accepted-run `8ddf727b…`, admission-contract `4f027af5…`, independent-review `dd9c5e72…`.
- Independent provenance review (baseline `d107ebd`): "retain old nine-reference Step 3 and seven-bundle Step 6 acceptance for their exact source/settings/cold-origin domain; do not reissue with new runtime hashes."
- The packet's parity lesson slug `lesson_tv_export_parity_semantics` **does not exist** as a lesson anywhere in this repo or its history (only the packet names it) — recorded as a missing producer fact; the real anchors are the Track B note §"Verification — parity against the captured exports", §"TradingView fill semantics pinned by the exports", and methodology lesson M-15's parity-reconstruction watch-point.

### Seven-bundle reconciliation table

| bundle | admitted source hash (ledger pins) | port + hash it binds | accepting parity review/run (reference) | registry still refuses c81aa5… (file:line) | moved since review? | status |
|---|---|---|---|---|---|---|
| O-N | manifest `945b7aa5…ad3adbb`; pine `orb_mnq_7_reconstruction_venue_bound.pine` `176c4f70…` | `orb_mnq_v7.py` = `b1f4e573…f553f317d` | Step 6 run/contract/review `8ddf727b…`/`4f027af5…`/`dd9c5e72…`; Step 3 `acfa7920…`/`ebcb2efb…`; Track B PR #356 orb 681/681 PASS | YES — comment `book_adapters.py:46-47`, pre-exec refusal `:121-123` | port pins NO (byte-identical since d107ebd); **registry file YES** @ `87db6b8` (+`73e28d3`, `7ba7844`) | STALE @ `87db6b8` (registry file moved; pin block unchanged) — ACCEPTED-by-reference otherwise; ruling R1 |
| O-P | manifest `abf5b153…6f6396d9`; pine `176c4f70…` | `orb_mnq_v7.py` = `b1f4e573…` | same as O-N (own export `2cb58fb6…`, inputs/properties as ledger) | YES — same lines | same as O-N | STALE @ `87db6b8` — same terms as O-N |
| S-P | manifest `13f766bc…f921a2fae`; pine `striker_dj30_v4.5_mym_pyramid_250_cap100k.pine` `712cf395…` | `dj30_mym_p250.py` = `efd479b6…520211f4` (corrected generation) | Step 6 `8ddf727b…`/`4f027af5…`/`dd9c5e72…`; Step 3 `acfa7920…`/`ebcb2efb…` (corrected-port parity). **Not** PR #356's striker row (that ran `c81aa59c…`) | YES — same lines | same as O-N | STALE @ `87db6b8` — same terms |
| S-W1 | manifest `ab72f039…f9d0c3`; pine `712cf395…` | `dj30_mym_p250.py` = `efd479b6…` | same as S-P | YES — same lines | same as O-N | STALE @ `87db6b8` — same terms |
| S-W1P | manifest `ddcc42c6…3e618ed9`; pine `712cf395…` | `dj30_mym_p250.py` = `efd479b6…` | same as S-P | YES — same lines | same as O-N | STALE @ `87db6b8` — same terms |
| S-W2 | manifest `8c037496…8af77690`; pine `712cf395…` | `dj30_mym_p250.py` = `efd479b6…` | same as S-P | YES — same lines | same as O-N | STALE @ `87db6b8` — same terms |
| S-W2P | manifest `45fd5cd6…d6dbe1`; pine `712cf395…` | `dj30_mym_p250.py` = `efd479b6…` | same as S-P | YES — same lines | same as O-N | STALE @ `87db6b8` — same terms |

Per the packet's rule ("any bundle whose port or registry moved since its review is marked STALE with the exact commit that moved it"), all seven rows are **STALE @ `87db6b8`** — the first commit after `d107ebd` to touch the registry file (`fix_runtime_identity_schedule_feedback`), then `73e28d3` (Phase 2 integration blockers) and `7ba7844` (signed Phase 3 qualification). The material facts for the ruling: the four port identity pins and the refusal are byte-identical throughout; the movement strengthened the refusal (hash checked pre-exec) and added the derived runtime effective-inputs successor. Aegis (`11763740…`) and Vanguard (`e6a03d04…`) ports are Step 3 retained evidence, not bundle rows; they share the same registry and the same STALE-by-file marking.

### Supplementary runtime identity — movement since the ledger's 19 pins

Unchanged (worktree hash = ledger pin; zero diff `d107ebd..HEAD`), 13 files: `core/dd_geometry.py` `2195f935…`, `core/historical_challenge.py` `53ab52e1…`, `core/lib/atomic_io.py` `8d5aa7dc…`, `core/lib/mvd.py` `57d35c97…`, `core/lib/validation.py` `02aa8d6e…`, `core/lifecycle.py` `0a70785d…`, `ops/c1_rail/__init__.py` `6bec736a…`, `ops/c1_rail/book_policy.py` `ffcd3aab…`, `ops/c1_signal_daemon/__init__.py` `a7a7421a…`, `book_bundle_intake.py` `fdea76cf…`, `book_parity.py` `42df0ffa…`, `feed.py` `b94e43c0…`, `pine_ta.py` `7816638a…`.

Moved, 6 files:

| file | HEAD worktree hash | moved @ | nature of the change |
|---|---|---|---|
| `ops/c1_signal_daemon/book_adapters.py` | `c6ad40bd…` | `87db6b8`, `73e28d3`, `7ba7844` | I1 pre-exec hash refusal; derived runtime effective-inputs digest `9d4d4e1d…`; TEST_ONLY qualification path. Port pins unchanged |
| `core/dd_protection.py` | `8113bb64…` (ledger `b05f50ef…`) | `5fae4d2` (2026-09-20) | comment repoints CLAUDE.md→AGENTS.md only (13 diff lines); no law change in the diff |
| `core/firm_rules.py` | `1da4bdda…` (ledger `aea6abaa…`) | `5fae4d2` | same governance comment repoints (1076 diff lines); no rule-value change in the diff |
| `ops/c1_signal_daemon/book_bundle_execution.py` | `75864a06…` (ledger `de667940…`) | `3cf42e4` | pending-reduction identity tracking (refusal feedback) |
| `ops/c1_signal_daemon/book_protocol.py` | `743117ea…` (ledger `37d1cd78…`) | `7ba7844` | shared completed-bar clock constants `BAR_PERIOD`/`BAR_SLACK` |
| `ops/c1_signal_daemon/tv_broker_emulator.py` | `2be77bab…` (ledger `6b6c4cb3…`) | `7ba7844` | stale/empty close resolution against confirmed scope — a fill-device change; the Track B parity run's emulator bytes are not HEAD's bytes |

Also relevant to loaders: the provenance review's independently verified I1-repair file identity `2299a1aa…` **never existed as a committed blob** (committed successors are `06d22014`@87db6b8 → `9ade8da5`@73e28d3 → `de4b6a9d`@7ba7844, blob identities); the 3-passing-tests verification binds to an uncommitted state. Recorded as a missing producer fact.

## Step 2 — Source/settings, warm-up, coverage, calendars, cutoff chronology (F06/F11/F15–F18)

Retained accepted evidence (reused by reference): warm-up `cold_at_panel_origin`, first bar `2022-09-01T00:00:00+00:00`, coverage verdict PASS for every bundle; accepted cold replay `2022-09-01T00:00Z`→`2026-09-03T00:00Z` (Aegis 94,893 bars incl. the attested 88-bar prefix; Vanguard 94,617); Step 3: nine references, 3,632 trades, 851,011 ordered bar calls; Step 6: seven PASS, 3,173 matched trades, 661,501 bars, zero exclusions. No arbitrary warm restart is certified anywhere.

**Calendar digests re-verified at HEAD, all six byte-identical to the ledger and unmoved since 2026-09-15** (no commit touches `ops/calendars/` since): session calendar `650e8aab…`, overlay `483f2324…`, forward captures `56951e15…`, D19 `2698f268…`, RATIFIED `c30bf64e…`, coverage inventory `e2841b62…`. F15's immutable-D19 condition holds.

**Cutoff chronology (F16)**: the approved design D = min(16:00, V−15), cutoff D−15, flatten D−5 stands as approved; the regenerated regular/early/DST/scheduler parity and fill-at-instant evidence is Phase 2/I2 work, not established here.

### Coverage-and-clock proposal (contradiction 3)

Three explicit clock/coverage classes (matching review vector CLOCK-2), with **no date extrapolation past 2026-09-30T21:00Z**:

1. **Historical source clock** — pool `2022-09-01..2026-09-02` (DRAFT interval). Driving artifact: the per-leg source sessions enumerated from the accepted panels under the shared union grid, with per-leg late origin and exclusion reasons (COVER-1 semantics), annotated by D19 `cme_holiday_calendar_2022_2026.json` (`2698f268…`) for date membership only. The calendar-coverage inventory (`e2841b62…`) is explicitly `INCOMPLETE_NOT_RUNTIME_INPUT`: `regular_session_coverage: UNPROVEN_FOR_FULL_INTERVAL`, `exception_inventory_completeness: UNPROVEN_SECONDARY_CANDIDATES_ONLY`, one observed source day only (Labor Day 2026-09-07), and the standing warning "Unlisted dates do not default to regular sessions." **The exact usable source-session index N is therefore not computable from accepted evidence** — the missing producer fact is a proven per-symbol regular-session enumeration (or panel-derived session index with exclusion reasons) over the historical interval. Mechanism once N exists: H1 = first ⌈N/2⌉ sessions, H2 = the remainder, disjoint union = FULL after frozen exclusions (POOL-1).
2. **Forward/live clock** — `book_session_calendar_2026-09.json` (`650e8aab…`) + `book_closure_overlay.json` (`483f2324…`) under `RATIFIED.json` (`c30bf64e…`, operator, 2026-09-15T11:05Z): coverage `2026-09-02T22:00:00Z..2026-09-30T21:00:00Z`, 20 session rows (18 PERMITTED, 2 DENIED — September 7 and 8), scope "Book permission rows for the first attended release only", review due September 24. This file expires 2026-09-30; nothing beyond it may be inferred.
3. **Path/evaluation clock** — horizon counted in **covered sessions actually present in the frozen pools**, never in extrapolated wall dates: proposed 500 business/covered-session days (DRAFT, retained), speed horizon 200 (DRAFT). Freezing the exact horizon is F1's act (F18), gated on the same N ruling as F17.

No historical deadline or coverage is guessed; reduced-depth evidence remains labelled per the standing rule; a real attempt is never used as a benchmark.

## Step 3 — Canonical inventories and frozen statistical definitions (F01/F02/F12/F13/F14/F19)

Each object pinned by file hash and commit, none by description. `ops/c1_rail/book_policy.py` (worktree `ffcd3aab3e74235e…`, **zero diff since `d107ebd`**, = ledger pin; last commit touching it `5b0dc5b`, 2026-09-13, pre-baseline) carries most of them:

- **F01 fixed K=1 book** — `BOOK_LEGS` at `book_policy.py:179-197`: `aegis_6j` 6J `6J1!` **SELL** (priority 1, `ProtectedRule.SCALE`, bases (8,), no adds); `dj30_mym_p250` MYM `MYM1!` **BUY** (priority 2, SCALE, bases 1..22, add 250% floor, max 1 add); `vanguard_mgc` MGC `MGC1!` **BUY** (priority 3, SCALE, bases (1,2), add 80% round, max 2); `orb_mnq_v7` MNQ `MNQ1!` **BUY** (priority 4, `BASE_FIXED_ADDS_OFF`, base (1,), add 100% round, max 2). No optional leg; retired IDs fenced at `:199` (`dj30_mym`, `nas100_mnq` — never reused). Pine hashes per leg match the registry pins.
- **F02 fixed trailing policy/response** — `CANDIDATE_TRIGGER = "0.01"`, `CANDIDATE_SCALE = "0.40"` (`book_policy.py:65-66`); `reference_mode="trailing"` with `trailing_locking` degenerating to trailing (`:81-90`); `require_policy` halts any other instance (`:96-114`); protected scale at `:236`. Registry empty: `'pre_admission_registry': 'EMPTY'` (`ops/c1_rail/qualification/policy.py:30`, file `687648af…` @`b684878`). The freeze of the canonical row + response map is F1's act; nothing is admitted here.
- **F12 quantity/lifecycle laws** — `entry_quantities`/`add_quantity` at `book_policy.py:282-331`: explicit-integer `cap_alloc` within `ACCOUNT_MICRO_CAP = 80` (`:63`, from `FIRM_RULES[TIER]["micro_contract_cap"]`), Striker add capped by `floor(cap_alloc/(1+add_pct/100))` (`:303`), zero refusal and executed-base semantics; lifecycle multipliers in `core/lifecycle.py` (worktree `0a70785d…`, zero diff since `d107ebd`, = ledger pin). Unchanged-law tests: `tests/ops/test_book_quantity_laws.py` (`eeabd195…` @`4eec7e7`), `test_book_policy.py`, `test_book_protection_lifecycle.py` — **not executed here** (no test suite in this dispatch). Consumer path: the runtime consumer is `ops/c1_rail/book_account_owner.py`, which **moved** since `d107ebd` (@`7ba7844`, 1,530 diff lines; also `3cf42e4`) — the law module is unchanged, the consumer path is pinned at its moved identity `724667a2…` @`7ba7844` and its acceptance is Phase 2's.
- **F13 capacity/priority/allocation** — capacity law in `ops/c1_rail/book_capacity.py` (`95381097…` @`a9175a1`, moved since `d107ebd` — takeover expiry/total-silence fencing): 80 gross micro equivalents, 6J=10 others=1, confirmed+reserved, refuse-never-clip, whole-leg lowest-priority-first Aegis takeover after terminal/quiescence proof. **Per-leg `cap_alloc` inputs are NOT frozen**: the accepted offline Striker ceiling is 80 (⇒ base cap 22); the per-leg upper request allocation 80 under a single shared cap 80 remains DRAFT (freeze-candidate "Allocations" row); production stays 0 until V1. Freezing the inputs is F1's act (I2/F1).
- **F14 protection clock** — `BookProtectionClock` at `book_policy.py:414+` (unchanged file): mode for a session from the prior settled close, `peak = max(peak, close)` EOD ratchet, **no latch** (`settle` recomputes `mode_next` each close), initial state FROZEN by the caller (pristine for E1; B7's `historical_eod_peak` for E2), `initial_peak >= initial_equity` enforced. The continuous own-path close/peak, no-resize and cancellation-race traces remain I2 evidence owed at F1.
- **F19 E1 initial state class** — explicit `EvaluationState` at `ops/c1_rail/qualification/contract.py:77-83`: `state_class`, `original_basis`, `current_equity`, `historical_eod_peak`, `prior_trade_days`, `prior_max_day_profit` (Decimal/int fields; file `48d6e5e9…` blob / `c36a114c…` worktree @`1339604` — **moved since `d107ebd`**, 964 diff lines). Pristine policy: `'policy_id': 'tradeify-e1-pristine/v1'`, `state_class: 'PRISTINE'`, empty pre-admission registry (`qualification/policy.py:28-31`); contract side guards "a non-pristine state requires a separately specified and sealed consuming gate" (`contract.py:847`). Pristine E1 (equity=peak=basis, days=best=0) is permitted (INIT-1: no invented fresh-B7-before-E1 prerequisite); freezing the explicit instance is F1's act.

**F24 calculator caveat** (pinned while in scope of the inventories): `scripts/certification_power.py` at HEAD is `896a5a1f…` @`05029ba` — it **moved** since the merged `4e7a25d` identity `4cb7851e…` whose 150-test verification is on record (change: exact-decimal ceiling/alpha handling). "Preserve current byte hash; rerun on changes" → a calculator+FP rerun record at the new identity is owed before F1 cites it.

## F01–F52 phase-1 status table

ACCEPTED = the row's currently owed, phase-1-verifiable evidence is in hand (reference given; any F1 freeze *act* noted). BLOCKED = explicit unresolved item with the missing fact named. NOT-PHASE-1 = the row's remaining work sits in this packet's phase 2, step 4 or a later stage.

| F | status | reference / missing fact |
|---|---|---|
| F01 | ACCEPTED | `BOOK_LEGS` `book_policy.py:179-197`, file `ffcd3aab…` unchanged since `d107ebd`; four IDs/sides, no optional leg |
| F02 | ACCEPTED | trailing instance `book_policy.py:65-114` (same file); registry EMPTY `qualification/policy.py:30`; canonical-row freeze at F1 |
| F03 | ACCEPTED | revision-bound September 14 first decision (EP/U `8101ba49…`/blob `f94be43e…`); reuse at final head |
| F04 | NOT-PHASE-1 | integrated-revision verification is packet phase 2 |
| F05 | NOT-PHASE-1 | final adopted head + combined G1–G5 composition acceptance is packet phase 2 |
| F06 | BLOCKED | September bounded domain accepted; historical/forward coverage + horizon unresolved — missing fact: proven per-symbol regular-session enumeration 2022-09-01..2026-09-02 (inventory `e2841b62…` is INCOMPLETE_NOT_RUNTIME_INPUT) |
| F07 | ACCEPTED-with-STALE-marker | seven bundles retained-accepted (ledger; Step 6 `8ddf727b…`/`4f027af5…`/`dd9c5e72…`; Step 3 `acfa7920…`); registry file moved @`87db6b8` with pins byte-identical — ruling R1 |
| F08 | BLOCKED | universal-state coverage map + risk/stop/allocation/confirmed-base witnesses owed (historical seven results are not a universal-state proof) |
| F09 | ACCEPTED | historical WATCH bundles + zero-Vanguard-WATCH retained (ledger); parity-only binding at F1 controls |
| F10 | ACCEPTED | refusal verified at HEAD `book_adapters.py:46-47` + `:121-123`; four pins unchanged; movement characterized (see Step 1); original artifacts preserved |
| F11 | ACCEPTED | panel/export digests + warmup pins retained (ledger); four coverage reports PASS retained; on-changed-engine revalidation owed with the engine's own acceptance |
| F12 | ACCEPTED | laws pinned (`book_policy.py:282-331` `ffcd3aab…`; `core/lifecycle.py` `0a70785d…`); tests pinned not run (no suite in dispatch); consumer path moved @`7ba7844` and pinned at `724667a2…` |
| F13 | ACCEPTED-law / inputs-unfrozen | law `book_capacity.py` `95381097…` @`a9175a1`; per-leg `cap_alloc` inputs DRAFT 80/shared-80 — F1 must freeze; production 0 until V1 |
| F14 | ACCEPTED-clock / traces-owed | `BookProtectionClock` `book_policy.py:414+` (unchanged file); own-path/cancellation traces are I2 evidence at F1 |
| F15 | ACCEPTED | six calendar digests re-verified byte-identical at HEAD, unmoved since 2026-09-15; D19 immutable |
| F16 | NOT-PHASE-1 | design approved (D=min(16:00,V−15), cutoff D−15, flatten D−5); regenerated parity/fill-at-instant evidence is Phase 2/I2 |
| F17 | BLOCKED | exact N + H1⌈N/2⌉/H2 split owed; N not computable from accepted evidence — ruling R2 (driving artifact); per-leg late origins + exclusion reasons owed |
| F18 | BLOCKED | horizon 500 covered-session / speed 200 proposed (no wall-date extrapolation past 2026-09-30); freeze gated on F17 ruling — F1 act |
| F19 | ACCEPTED | explicit `EvaluationState` `contract.py:77-83` @`1339604`; pristine `tradeify-e1-pristine/v1`; no fresh-B7-before-E1 prerequisite; instance freeze at F1 |
| F20 | BLOCKED | three named facts unchanged: CSV/query timezone+endpoints; Sept-14 boundary equity/flatness; close correction status |
| F21 | NOT-PHASE-1 | fresh used-account snapshot is Phase 6 / E2 chain |
| F22 | ACCEPTED | emulator pinned at HEAD `2be77bab…` @`7ba7844` (moved: stale-close guard — noted); venue per-side costs and slippage pins per freeze-candidate; bytes frozen at F1 |
| F23 | NOT-PHASE-1 | final composed runtime acceptance is phase 2 |
| F24 | BLOCKED | calculator moved since its 150-test record (`4cb7851e…`→`896a5a1f…` @`05029ba`); rerun record owed at the new identity |
| F25 | ACCEPTED | design assumptions recorded (compute-depth: .03/.65/.80/Fréchet); frozen independently of outcomes at F1 |
| F26 | ACCEPTED | design cutoffs computed (200; ≤10 failures per population; screen adds no confidence); freeze at F1 |
| F27 | ACCEPTED | 970 per FULL/H1/H2 design (2,910/stage); n3 not sized from n1/n2; freeze at F1 |
| F28 | ACCEPTED | domain-separated seed inputs implemented; actual root/recipe freeze + old seed-label reconciliation at F1; no n3 consumption |
| F29 | ACCEPTED | six-month replacement, original length, 100/200 rule accepted (P2 §2.4); boundary/index/truncation block ledger at F1 |
| F30 | BLOCKED | five-session rebuild rule + fixtures retained; binding actual qualified joins/panel indices/startup model owed (private panels + composed acceptance) |
| F31 | ACCEPTED | floor .95, p5 sanity, 1pp expand-200 rule accepted; percentile method freeze at F1 |
| F32 | NOT-PHASE-1 | budget is step 4 + the operator's; no numerical budget approved (contradiction 4 disposition below) |
| F33 | NOT-PHASE-1 | second exact-depth decision is a dated post-F1 operator addendum |
| F34 | BLOCKED | mapping n2 H1/H2 to exact session pools depends on F17's N |
| F35 | BLOCKED | signed full composition + actual legality/source coverage owed |
| F36 | BLOCKED | complete code/data/port closure under the final reviewed runtime — 6 of 19 supplementary files moved since the ledger (Step 1 table); binding is phase 2 |
| F37 | ACCEPTED | `tb-i1-canonical-v1` + tests/vectors accepted; runtime/tool/deps pinned at F1 |
| F38 | ACCEPTED | registry validation helper exists; expected-rows authentication is the F1-recipe/D0 act (helper identity ≠ approval) |
| F39 | ACCEPTED | canonical config + two-field delta tests present; exact real baseline vectors pinned at F1 |
| F40 | NOT-PHASE-1 | E1 seal chain and later; nothing issued |
| F41 | NOT-PHASE-1 | partial-year indices materialized at F1/I2 before results |
| F42 | NOT-PHASE-1 | stress variants accepted at F1/I2 |
| F43 | NOT-PHASE-1 | transformation semantics frozen at F1 |
| F44 | BLOCKED | exact contract-month seam indices ±2 sessions, count M and budgets not yet bound in accepted evidence (ACCEPTED_UNMODELED stands) |
| F45 | NOT-PHASE-1 | exact variant list frozen at F1 before results |
| F46 | NOT-PHASE-1 | interval method/anchor frozen at F1; n3 quantities later |
| F47 | ACCEPTED | durable journal/checkpoint dispatch + terminal-prefix/no-redraw tests implemented; combined authenticated acceptance at F1/E1 |
| F48 | ACCEPTED | public/private root separation observed in this reconciliation (private roots absent from the public worktree; no private bytes copied) |
| F49 | NOT-PHASE-1 | final composition/invocation review at F1/E1 |
| F50 | NOT-PHASE-1 | pre-reopen readiness binding is packet phase 2 (T07/T08 consumption) |
| F51 | NOT-PHASE-1 | independent review of the assembled F1 packet is phase 2 |
| F52 | NOT-PHASE-1 | D0/D1/V1/live sequence later; no GO inferred |

Counts: 24 ACCEPTED (F13 and F14 carry law-accepted / inputs-or-traces-owed splits noted inline), 11 BLOCKED (F06, F08, F17, F18, F20, F24, F30, F34, F35, F36, F44), 17 NOT-PHASE-1.

## Contradictions 1–5 — dispositions (each with two admissible readings)

1. **Port generation.** Disposition: the correction is verified on the adopted integration — the registry pins `efd479b6…` and refuses `c81aa59c…` at HEAD (`book_adapters.py:46-48` comment + `:121-123` pre-exec refusal), and the original artifacts are preserved. The registry *file* moved since the review baseline with the pin block byte-identical. Two admissible readings for whether by-reference bundle acceptance survives: **(a)** acceptance binds the pinned identities, which are unchanged — the seven bundles remain ACCEPTED-by-reference and only the loader's own new acceptance (I1 successor, runtime effective-inputs digest) is owed; **(b)** acceptance binds the binding file's byte identity — any registry movement voids by-reference reuse until the affected parity/loader evidence is re-run on the committed identity. Ruling R1 requested; the packet's STALE marking is applied meanwhile.
2. **S2 stage coverage.** Disposition: dedicated implementations exist (continuous replay, G1–G5 orchestration, signed qualification after PR #413) and implementation existence is reported **as implementation only** — not as source or F1 acceptance; final signed composition and affected review remain owed (phase 2). Two admissible readings on what the movements discovered here require: **(a)** the moved surfaces (loader, emulator stale-close guard, protocol clock constants, owner path) are within Phase 2's already-owned affected acceptance, and phase 1 needs only to record them; **(b)** the emulator and loader are parity-carrying devices, so any Track B/Step 3 parity reuse is void until those devices' new identities carry their own accepted parity — the stricter reading the review's reuse decision already gestures at ("new loader … require separate affected acceptance").
3. **Coverage and clock.** Disposition: the three-clock proposal above (historical source clock / ratified forward clock expiring 2026-09-30 / covered-session path clock, horizon 500 proposed, speed 200), with N not computable from accepted evidence and no extrapolation. Two admissible readings for N's driving artifact: **(a)** panel-derived (data-first) — N is the distinct union-grid source sessions present in the four accepted panels, per-leg late origins and exclusion reasons recorded, D19 annotating date membership only; **(b)** calendar-derived (rule-first) — N is the CME regular-session enumeration of the interval with D19 exceptions applied, and any session a panel fails to cover is a blocker, not an exclusion. Reading (b) is currently unsupported by evidence (`UNPROVEN_FOR_FULL_INTERVAL`; "unlisted dates do not default to regular sessions") but remains the operator's to choose with new calendar evidence. Ruling R2 requested.
4. **Budget.** Disposition: out of this dispatch (step 4 is not phase 1 as dispatched); **no numerical budget is approved**; the representative measurements and their component breakdown remain the step-4 executor's, at reduced signed TEST_ONLY depths, labelled. Two admissible readings for what may inform the operator's F1 budget: **(a)** reduced-depth representative measurement on the accepted engine suffices to set a reserve-factored envelope (packet step 4's own design); **(b)** only the full composed controller/proof/runtime measurement closes F32, and reduced-depth figures are planning evidence only. Both readings leave the approval with the operator.
5. **Actual evidence versus prerequisites.** Disposition: pristine E1 needs no used-account reconstruction (INIT-1); F20's three missing facts remain at their real consumers; no fresh-B7-before-E1 condition is invented here. Two admissible readings on F1 blocking: **(a)** the three F20 facts block only actual-settlement/live consumers (E2 chain, actual close, activation), and F1/E1 proceed on pristine evidence; **(b)** if any F1 freeze row itself consumes actual-close evidence (e.g., SET runtime acceptance inside the combined acceptance), the claim must name that exact gate — none has been named, so under (b) F1 is not blocked by F20 either, only by that gate being named if it exists. Ruling requested only if the operator holds (b) and knows of such a row.

## Missing producer facts (early list, before anything is assembled on top)

1. **Private bundle originals** — the evidence root `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/inputs/private_overrides/op1/2026-09-14-seven/` (ledger-relative prefix) is absent from this worktree; all bundle artifacts (manifests, pine, corrected ports, exports, inputs/properties, panels, margin, attestations, Step 3 coverage) are unpinned-able by fresh hash here and are reused strictly by the ledger's pins. Anything needing original bytes is BLOCKED at that root.
2. **Live port bytes** — `ops/c1_signal_daemon/ports/{aegis_6j,dj30_mym_p250,vanguard_mgc,orb_mnq_v7}.py` and `effective_inputs.json` exist only on the operator's primary checkout (gitignored; README: never in worktrees). Fresh confirmation that the live bytes still hash to `11763740…`/`efd479b6…`/`e6a03d04…`/`b1f4e573…` and the inputs to `66406dee…`/`9d4d4e1d…` is BLOCKED at those paths.
3. **`lesson_tv_export_parity_semantics`** — named by the packet; no such lesson exists in this repo or its history. Expected: a lessons-registry entry under that slug, or a packet correction pointing at the Track B note §Verification/§fill-semantics and methodology lesson M-15.
4. **I1-repair verification-to-commit binding** — the independently verified loader identity `2299a1aa…` was never committed; a rerun or producer statement binding the verification to a committed identity (`06d22014`/`9ade8da5`/`de4b6a9d` blob lineage) is owed.
5. **Proven per-symbol regular-session enumeration** for 2022-09-01..2026-09-02 (F06/F17) — the single source day on record (Labor Day 2026-09-07, capture `3dafe4b7…`) does not certify the interval.
6. **F20's three facts** — CSV/query timezone and endpoints; September 14 boundary equity/contemporaneous flatness; close correction/acceptance status (unchanged from the provenance review).
7. **Calculator rerun record** at `896a5a1f…` @`05029ba` (F24) — the merged 150-test record binds `4cb7851e…`.
8. **Aegis current-properties capture** — never identified in the Step 3 directory (`E/step3-coverage/Aegis-current-properties.txt`); its nonexistence elsewhere must not be inferred; no pin invented.

## Rulings needed from the operator/coordinator

- **R1 (contradiction 1, F07/F10):** does registry-file movement with a byte-identical pin block void by-reference acceptance of the seven bundles (reading b) or not (reading a)? Determines whether the seven rows leave STALE.
- **R2 (contradiction 3, F17/F18/F34/F06):** panel-derived vs calendar-derived session index N. Determines N, the H1/H2 split, and the horizon freeze path.
- **R5 (contradiction 5, F20), only if held:** name the exact implementation/evidence gate, if any, at which actual-close evidence enters F1's own freeze rows.

## Provenance commands (as executed, read-only)

`git log/diff d107ebd..HEAD -- <path>` for `ops/c1_signal_daemon/book_adapters.py`, each supplementary runtime file, `ops/calendars/*`; `sha256sum` of the six calendar artifacts, the 19 supplementary files, inventory files and the calculator; `git show` per registry-touching commit; per-commit blob hashing of `book_adapters.py` across all history (`2299a1aa…` absent). No test, replay, qualification or private-input command was run.

## Rulings — 2026-09-21

- **R1 (coordinator):** reading (a). Registry-file movement with byte-identical port pins and a strengthened stale-byte refusal does **not** void by-reference acceptance. The seven rows are **ACCEPTED-by-reference, movement annotated** (`87db6b8`, `73e28d3`, `7ba7844`; pins unchanged). Two F10 hold items replace the STALE marking: (i) the corrected Striker port `efd479b6…` has no parity run of its own — PR #356's Striker row executed `c81aa59c…` — so its parity rests on the accepted Step 3 contract until a corrected-port parity run exists or the operator accepts Step 3 as sufficient at F1; (ii) `tv_broker_emulator.py` moved at `7ba7844` after the Track B parity run, so that run's fill device is not HEAD's — the on-changed-engine revalidation F11 already owes covers it.
- **R2 (operator):** **panel-derived.** N and the H1/H2 split are enumerated from the accepted per-leg panels under the shared union grid, annotated by D19 for date membership only; no calendar extrapolation. One bounded, labelled producer run is owed (phase 2 / step 4 scope); the horizon freeze (F18) waits on it.
- **R5 (operator):** **no** F1 freeze row consumes actual-close evidence; pristine E1 needs no used-account reconstruction. F20's three facts remain T07's (settlement), not an F1 gate; contradiction 5 is closed for F1.
