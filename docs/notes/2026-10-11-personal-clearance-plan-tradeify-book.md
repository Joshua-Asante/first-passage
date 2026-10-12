# Personal-clearance plan: Tradeify book at E_0

**Status:** DRAFT plan for Joshua, prepared by the Deployment Coordinator; corrected 2026-10-11 for Joshua's corrections (§1). The coordinator owns #752 under [ADR addendum 2026-10-11b](../adr/2026-10-09-self-funded-tradovate-lane-reopen.md#addendum-2026-10-11b--tradeify-book-reused-on-the-personal-lane-supersedes-the-option-c-split) (#784, open). This plan authorizes nothing: no build, export, replay, freeze, spend, arm or order. Items marked **Joshua** are decisions for him to make.

**Read at:** `origin/main@2cfb3d7`. PR heads read: #752 `b02c173`, #775 `d3e4487`, #776 `99126d2`, #777 `bf5579a`, #779 `2275285`, #782 `22d0924`, #783 `a6d8f02`, #784 `d7ad4d8` (corrected 2026-10-11), plus #770, #773 and #774. Sources re-read for the correction fold:
- the Tradeify Funded Trader Agreement (page marked last modified May 2026, read 2026-10-10), §§2.4–2.5, 6.6 and 6.7;
- `ops/c1_rail/book_policy.py`, `ops/c1_rail/qualification/production_source.py` and `replay.py`;
- the [synchronized-replay spec](../spec/2026-09-12-tradeify-synchronized-replay-spec.md) (RC-1), the [TB-R2 faithfulness read](./2026-09-12-track-b-scaling-faithfulness-read.md), the [adapters note](./2026-09-11-track-b-adapters-and-book-rules.md), the [parallel-prerequisites handoff](../briefs/handoffs/2026-09-14-track-b-parallel-prerequisites.md) and the [T10 reconciliation](./2026-09-21-t10-phase1-source-reconciliation.md) (R1, operator confirmation 2026-09-24);
- the [T00 card](../briefs/handoffs/2026-10-03-t00-screen-authority-build-card-DRAFT.md) §8, the [successor card](../briefs/handoffs/2026-10-10-t00-successor-screen-build-card-DRAFT.md) §1.2/§8, the [book lineage manifest](../../discovery_manifests/t00_tradeify_book_lineage_2026_10_10.json), and #752's Phase-0 classification.

No private value, export body, size vector, startup policy or in-flight screen output was read. Nothing was run.

**Layers:**
- **IMPL:** code and packets. Workers build them, the accepting owner named in each row accepts them, and they merge only with Joshua.
- **QUAL:** evidence that the exact candidate meets its contract.
- **AUTH:** live authority, held by Joshua alone. It covers spend, the arming GO, the live-spend GO and every per-session GO.

No layer implies another.

## 1. Ruling and corrections

> "reuse the Tradeify strategies, qualify their sizing for the personal capital, and finish the personal-account operating controls. The search for additional strategies can come off this deployment's critical path." (Joshua, 2026-10-11, to the Deployment Coordinator)

**Corrections (Joshua, 2026-10-11, to the coordinator).** He supports reusing the Tradeify strategies and the existing personal-account components, a cheap sizing, margin and risk pre-screen before expensive runs, and operating only one account at a time for the first deployment.

| # | Correction | Where applied |
|---|---|---|
| 1 | Remove the blanket §6.6 permission gate; keep the ownership and opposing-exposure restrictions | §7 |
| 2 | Remove the five-minute fix window; a two-way switch check (outgoing account flat, no working orders, cannot submit delayed entries), where uncertainty blocks | §7, §8 E5 |
| 3 | Start from the retained successor configuration; justify any change; say that personal margin inputs are missing | §3.1, §4 |
| 4 | The Striker path is bounded by the 80-micro allocation; the personal tier needs a defined sizing and protection policy | §3.2 |
| 5 | Panels are fully exposed: freeze further choices, retain exposure history, justify the trial accounting | §5.2 |
| — | No 85% margin utilization without a cash-buffer rationale | §4 |
| — | No 6–8 week forecast without a dependency breakdown | §9 |
| — | #752 re-scoped in place by default; a new study ID is optional | §5.4 |
| — | D4 before sizing: each rung names the quantity behaviour it represents | §3.3 |

**Recommendation:** authorize the corrected pre-screen and preparation (§4; decisions O1–O4 in §9), then a short decision-ready sizing proposal.

| Superseded | By |
|---|---|
| [Option-(c) split](../adr/2026-10-09-self-funded-tradovate-lane-reopen.md#addendum-2026-10-11--strategy-split-between-lanes-option-c), which narrowed the personal pool to strategies outside the book | 2026-10-11b: the pool is the book's legs, starting from the retained successor configuration |
| #752 F8 (exclude legs 1–4) | 2026-10-11b |
| F8's HOLD ("Hold while additional locked candidates are admitted", a separate operator ruling dated 2026-10-10) | Lifted when Joshua ratifies #752's in-place re-scope (§5.4), or by #784 if it names the HOLD. 2026-10-11b does not name it |
| #752 five-leg grid, K = 2,375 | Not restored. Sizing is an explicit ruling (§3) |

| Unchanged | Owner |
|---|---|
| The T00 step-3 Tradeify successor screen (H′ `eed60a1`) is in flight. This plan touches none of its worktrees or folders. Its verdict does not clear the personal lane | [#733](../briefs/pre-registration/2026-10-08-tradeify-book-successor-screen-prereg-DRAFT.md) |
| Locked strategy parameters. The size vector can only lower quantities: `LegSize` refuses any value above today's, and it has no side field (`book_policy.py:252-290`) | `core/strategies/CATALOG.md` |
| `dd_protection` constants and the Tradeify 1%/0.40 binding | AGENTS.md §Protection; [concept-not-constant ADR](../adr/2026-07-13-dd-protection-concept-not-constant.md) |
| Decision 4: intraday-honest p99 peak-to-trough ≤ 15% after Tradovate costs and whole-contract rounding, with a live 15% halt | [ADR 10-09](../adr/2026-10-09-self-funded-tradovate-lane-reopen.md) |
| All seven owed items gate the first live order on the personal account (ADR 10-09 Owed preamble). #784 re-scopes item 5's content, not that sentence | ADR 10-09 |
| M1, arming, live-spend and per-session GO rules | AGENTS.md |
| The Codex deployment coordinator keeps combined acceptance of a disarmed candidate and acceptance of release evidence | [Deployment checklist roadmap](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md) rows 5–6 |
| `E_0` stays private; only the symbol appears in public text | ADR 10-09 |
| Owed items 2–4, 6 and 7; the 2026-11-08 four-firm falsifier | ADR 10-09; program ADR |

## 2. Scope and non-goals

**In scope:**
1. Fix the sizing by explicit ruling, starting from the retained successor configuration, with each rung's quantity behaviour named first (§3).
2. A cheap sizing, margin and risk pre-screen at E_0 before any expensive run (§4).
3. Clear the ruled sizing at E_0 on drawdown, growth, fees (per-side and fixed) and margin (§5).
4. Finish the personal controls: tier, personal sizing and protection policy, halt, binding, P4 and the one-account switch check (§7).
5. Live wiring, feed/API licensing and the attended end-to-end qualification (§8).

**Book identity:**
- The four `BOOK_LEGS` legs: `aegis_6j` SELL, `dj30_mym_p250` BUY, `vanguard_mgc` BUY, `orb_mnq_v7` BUY (`ops/c1_rail/book_policy.py:181-198`), in the retained successor configuration (§3.1).
- Their Pine pins, and the accepted runtime ports in `core/strategies/BOOK_SOURCES.sha256`.
- The rail build (H) is pinned later, at combined acceptance (§8, row 4.1).

**Non-goals:**
- **Searching for additional strategies.** It is off the critical path but not barred. Any added leg needs its own clearance and re-runs the L0 static check (§7).
- **Excluded sizing studies:** Striker NAS100 MNQ (old leg 5); the five-leg grid; any uniform or searched grid not anchored on the retained configuration, unless Joshua names it.
- **Changes to locked or Tradeify-owned material:** the Tradeify binding, its size vector, Pine, ports, `effective_inputs.json` or `dd_protection`. Row 2.2 keeps the Tradeify path byte-identical.
- **Out-of-sample claims** (§5.2).
- **Simultaneous operation** of the Tradeify and personal accounts. The first deployment runs one account at a time (§7).

## 3. Sizing frame (before any sizing number)

### 3.1 Starting configuration

- **Start from the retained successor configuration:** FLOOR-HALF, Q1 option A: every leg at k = 0.5 under the code's round-down rule, and a leg that floors to 0 is OFF (T00 card §8, 2026-10-10; `size_vector_sha256` `139919cd…c271`; per-leg values private in the options sheet `q1-options-20261010`). At least one leg floors to 0 (successor card §1.2).
- **Legs it sets OFF stay OFF.** No "smallest base gear" or uniform rung is assumed, because either could re-enable a leg the successor disables.
- **Any change** (a leg turned on or off, a quantity field, an adds rule) is proposed in the sizing proposal with a written ex-ante justification: margin, granularity or the personal policy (§3.2). A growth, hit or MAE result is never a justification. Changes are frozen before any E_0 scoring output.
- FLOOR-HALF was chosen for the Tradeify cap frame, not for E_0. The pre-screen (§4) is the first check of its fit at E_0.
- **Read access.** The literal values sit in the r3d startup policy and the Q1 options sheet, which are outside the AGENTS.md read surface (#773 Q4). Using them in the pre-screen needs Joshua's read ruling (O2), or Joshua runs that arithmetic himself.

### 3.2 Personal sizing and protection policy

**The current Striker path is bounded, and every bound comes from Tradeify:**
- **Base ≤ 22.** `cap_term = cap_alloc ÷ 3.5`, with `cap_alloc` ≤ `ACCOUNT_MICRO_CAP` (`book_policy.py:537-546`); the ladder is 1..22 (`:176-187`), and `max_base` ≤ 22 (`LegSize`, `:252-290`).
- **Add ≤ 55.** Add = ⌊2.5 × base⌋ (`:163-167`), so Striker reaches at most 77 MYM micros.
- **Account cap of 80 micro-equivalents.** `CapacityLedger` refuses, not clips, a fill over the cap (`:815-862`).
- **Sources of the bound:** `TIER = "Tradeify_Select_100K"` and `ACCOUNT_MICRO_CAP` = 80 (`:64-65`; `core/firm_rules.py:488`); the literal 80s in the replay startup parser (`ops/c1_rail/qualification/production_source.py:190-191,207-208,211`).
- **Protection** is fixed at trailing 1%/0.40 by `require_policy` (`book_policy.py:101-117`); `replay.py:254` calls it too.
- **Risk dollars.** Striker's `risk_dollars` is the port's `account_size` × risk % (`production_source.py:100-102`), a fixed figure not linked to E_0.
- **No silent unbounding.** #775's `Personal_Tradovate` row has `micro_contract_cap: None`. Pointing `TIER` at it would fail at import (`int(None)`), so the path halts rather than running unbounded.

**So no personal sizing is executable until a personal policy is defined** (owed items 1–2; row 2.2). It has three parts:
1. a finite cap source, per account and per leg, replacing the Tradeify 80s;
2. a risk-dollar basis for Striker (the port value, or one linked to E_0);
3. a protection policy. The candidate for the sizing proposal is normal mode plus the 15% halt only, recorded as the (book, `Personal_Tradovate`) binding under the concept-not-constant ADR, with native guards and soft-stops as captured and `backtestMode` at reference. If the 1%/0.40 response map were used instead, T07 EOD settlement and its post-11-01 DST repeat would also bind.

Any personal quantity above today's also needs a code change, because `LegSize` refuses it.

### 3.3 Quantity behaviour per leg and rung (D4, ahead of sizing)

A rung is testable only if its evidence route reproduces the quantities the rail would send. Scaling a Pine input does not always do that. For example, scaling Aegis's contract cap in a Pine export keeps an equity-risk ladder, while the rail sends a fixed quantity.

| Leg | Rail quantity law (`book_policy.py`) | Expressible today | What a scaled Pine export represents | Valid route at a rung |
|---|---|---|---|---|
| `aegis_6j` (full-size 6J = 10 micro-equivalents) | **Fixed quantity** q (TB-S1 (F)); no adds. The rail sends ⌊q × scale × lifecycle⌋, with scale 0.40 in PROTECTED (`:182`, `:531`, `:553-558`) | q in 0..8 | Equity × risk %, capped by `max_contracts`, so sizes still vary: the cap bound on only 59 of 121 captured trades. A cap-scaled export is a different portfolio | Only where the rung's policy has no protected scaling (normal mode plus the 15% halt) and lifecycle is AUTHORIZED (multiplier 1): per-contract re-sizing, P&L_i ÷ qty_i × q, since timing is size-invariant (the port at fixed 8 and fixed 3 reproduced all 121 entry/exit bars and prices, TB-R2 §1), or port replay at fixed q. Under any protection response map: port replay only. Exports use the recovered effective inputs. q > 8 needs code |
| `dj30_mym_p250` (MYM) | **Risk and cap multipliers** (law B): base = min(⌊risk$ × scale × lifecycle × m ÷ per-contract risk⌋, ⌊cap_alloc × c ÷ 3.5⌋, `max_base`); add ⌊2.5 × base⌋ (`:484-511`, `:532-546`) | m and c in [0, 1]; `max_base` 0..22; bounded as in §3.2 | Scaling `accountSize` by k ≤ 1 equals m = k; `microCap` at ⌊80k⌋ equals c = k when 80k is an integer, otherwise verify the floor (⌊⌊80k⌋ ÷ 3.5⌋ can differ from ⌊80k ÷ 3.5⌋); k > 1 is not expressible. The day soft-stop and DD kill depend on size | An export at the rung's exact settings, or port replay through the size vector. The anchor is the corrected port `efd479b6…`'s Step 3 contract (`acfa7920…`/`ebcb2efb…`) with Step 6's seven-bundle replay, confirmed by the operator 2026-09-24 ([T10 reconciliation](./2026-09-21-t10-phase1-source-reconciliation.md) R1 hold item (i)). S-0's 203/203 ran the superseded port `c81aa59c…` and is not the anchor. Re-sizing S-0 is invalid: the halts move with size, ⌊m·y⌋ ≠ m·⌊y⌋, and the add floors. The rung states the port's paper-equity basis |
| `vanguard_mgc` (MGC) | **Port map** `base_by_port` {1→0..1, 2→0..2} over the port's own ladder; protected or WATCH: 0; adds round(0.8 × base) (`:508-511`, `:548-551`) | Per port, 0..port | Re-runs the Pine ladder at the scaled equity, whereas the rail maps the reference ladder. A per-port map that no single cap input reproduces is not expressible in TradingView | Port replay with the size vector, anchored to V-0 parity (338/338). Re-sizing is invalid. An export counts only if the rung is a pure input change verified against the port at that setting |
| `orb_mnq_v7` (MNQ) | **On/off**: base 1 fixed, adds 1 each up to 2; protected mode refuses adds (`:195`, `:557`, `:720-725`) | Base 0 or 1 | Fixed `qty`; turning adds off also disables the stall exit | Normal mode at lifecycle AUTHORIZED (`:557-558` also multiplies ORB by lifecycle), integer q: O-N trades × q, provided capital scales with q or margin is shown not to bind. O-N (corrected `8e4902c3…`) and O-P are ACCEPTED-by-reference at q = 1 under the operator-authorized finite-leverage substitute, not the 0% chart margin TB-R2 specified (O-7) ([T10 reconciliation](./2026-09-21-t10-phase1-source-reconciliation.md) R1; the four-firm re-MC consumes them). With any protection: port replay only. q ≥ 2 needs code |

**Rules for rungs:**
- **Port replay is the default.** The synchronized-replay spec rules recorded-trade replay inadmissible for book replay (RC-1, `:28`). The only exceptions shown above are Aegis at fixed q, only under a policy with no protected scaling (normal mode plus the 15% halt), and ORB in normal mode at integer q, both at lifecycle AUTHORIZED. Both override RC-1's "any leg" text for this personal study and depart from #752 §B and F7's post-rescale ban; the re-scope states that override with its TB-R2 evidence (RC-1's own rationale names ORB under protection and the two ladder legs as the trades that change with size or mode).
- **Each rung names, per leg,** its quantity law, the field it sets (values private), its route and, for Striker and Vanguard, the port's capital basis. A rung with no valid route is not scored.
- **R0 (the retained configuration):** Aegis at fixed q uses re-sizing or port replay only under a policy with no protected scaling and lifecycle AUTHORIZED; under any protection response map, port replay only. Striker's multiplier law uses port replay or an exact-setting export. Vanguard's port map uses port replay. ORB is OFF if the vector floors it; otherwise it uses O-N × q under the margin condition.
- **Personal replay path.** Port replay under a personal policy needs §3.2's policy and a replay path that accepts it. Today `replay.py:254` calls `require_policy`, which refuses anything but trailing 1%/0.40. The build is comparable in scope to card #758.
- **#752 §B/F1** (capital and caps scaled with k) tests Pine-native sizing. It matches the rail only for Striker's risk term at k ≤ 1, once the capital basis is fixed, and for ORB at integer k ≥ 1 in normal mode. It is not a route for Aegis or Vanguard.

## 4. Cheap pre-screen at E_0 (before expensive runs)

The pre-screen is zero-K and data-independent: it reads no export, replay or score. Its outputs stay private and are recorded by hash (O3).

| Check | Computation | Inputs | State |
|---|---|---|---|
| Margin | Rule-maximum concurrent quantity of the configuration (base, adds and `max_adds` per `BOOK_LEGS`; Striker within the §3.2 bound) × dated per-contract margin, reported as utilization of E_0 for each component of the cash buffer | Configuration values (O2); **authoritative personal margin inputs, which are missing**; E_0 (private) | Blocked on inputs |
| Granularity | Ex-ante one-contract risk (stop rule × point value × a dated volatility snapshot) ÷ (0.15·E_0). A leg over the threshold is flagged for the sizing proposal | Stop rules (read surface); dated volatility snapshot | The threshold has no repo source: it is an operator heuristic ("~20%"), stated as a chosen constant with its statistic and snapshot date |
| Fees | Per-side Tradovate commission + exchange + clearing + NFA, per instrument | A dated snapshot on a named Tradovate plan | Not taken |
| Fixed costs | API add-on, data entitlement, key balance, licence: amount, period, and whether debited from the trading account | A dated cost snapshot | Not taken (#770, #774) |

**Authoritative personal margin inputs are missing.**
- **Nothing recorded.** No dated Tradovate margin for 6J, MYM, MGC or MNQ exists in the repo, `core/firm_rules.py` or `ops/instruments/`. For Aegis, the margin unit is a full-size 6J contract.
- **Required but not produced.** The Q-SFGROWTH-1 pre-registration requires a dated initial-margin snapshot in its Phase-0 manifest (`docs/briefs/pre-registration/Q-SFGROWTH-1-verdict-preregistration.md:31`), and that Phase 0 is still listed as not done (`docs/briefs/INDEX.md:18`).
- **What the snapshot must carry:** the margin type (day/intraday versus initial/overnight), the date and the source page.
- **Not margin inputs:** the TradingView backtest-margin settings in the campaign's private overrides are not exchange margins.

**Cash buffer: a decision, with the number left open.** The earlier 0.85·E_0 margin limit is withdrawn. The sizing proposal sets the buffer with a rationale that covers at least:
- the equity at the halt boundary (0.85 × running peak), since the halt fires only after that loss;
- the adverse move between the halt trigger and the flatten, gaps and slippage included;
- exchange or broker margin increases while positions are open, and the day-versus-initial basis for anything held past the session;
- Tradovate's own liquidation threshold (an actor in the T13 inventory);
- fixed-cost debits from the trading account.

Until that ruling, the margin check reports utilization only, with no pass line.

## 5. Clearance at E_0 (after the sizing proposal is ruled)

### 5.1 Tests

| Test | Standard | Documented | Built | To build |
|---|---|---|---|---|
| Drawdown | Daily, from each leg's route (§3.3): d = Σg − c·fees − D, l = −Σ\|MAE\| − c·fees − D, h = Σ\|MFE\|. D is any fixed cost debited that day. Intraday peak = max(P, E+h). A hit is (peak − trough)/peak ≥ 0.15 and ends the path, like the live halt. Bootstrap: 10,000 paths × 13 non-circular 20-day blocks, H = 252, seeds 42, 123 and 2026 | ADR Decision 4; [#752 prereg §C](../briefs/pre-registration/Q-SFGROWTH-1-verdict-preregistration.md) (frozen baseline on main) | #783 `score`, `path_terminal`, `bootstrap_indices`, `summarize`. Builder tests only, on synthetic data, unverified | Route adapters; FG; runner; one calendar. Replace #783's literal `.15` with the tier constant, using #776's `round(dd, 6) >=` rule |
| Growth | Pooled `numpy.median` terminal equity at 252 days, net of debited fixed costs | §C | #783 `summarize`, `rank` | Funding test (private): (median terminal − E_0)/E_0 ≥ g\*. g\* = 12 × monthly cost ÷ E_0 (#774), counting only costs **not** debited in the path. This is a funding test, not clearance |
| Fees (per side) | g = Net + Commission, applied once; reference slippage stays embedded. Fee-only stress c ∈ {1, 1.5} per instrument | #752 F9 friction ruling (2026-10-10) | #783 `daily_series` (per leg, then summed) | The §4 fee snapshot passed to #783 per leg. `Personal_Tradovate.cost_per_side_usd` is a scalar, so it stays unused for scoring. Do not reuse the four-firm depth bundle: it charges a flat micro rate on 6J |
| Fixed costs | Each fixed cost is debited from the trading account (a dated periodic debit D in d and l at both c limbs, because the live halt observes account equity, #776 `observe`) or paid elsewhere | ADR Decision 4 ("after Tradovate costs") | — | The §4 fixed-cost snapshot |
| Margin | Concurrent open quantity; entries processed before exits on ties; Σ per-leg peak × dated margin within E_0 less the ruled cash buffer (§4); VOID is checked first | #752 F9 margin correction | #782 `check_concurrent_margin` (72 builder tests, unverified) | Route output → `MarginFill` adapter with one tranche per add; an expected-fill inventory; the §4 margin snapshot |
| Windows and verdict cells | **Binding:** hits ≤ 100/10,000 on **each** seed, at c = 1 and c = 1.5, in FULL, H1 and H2 (18 cells); and pooled median terminal > E_0 at c = 1.5 in FULL, H1 and H2. **Ranking** (only if more than one rung is ruled): FULL, c = 1, pooled seeds, tie-break (ii) on FULL trades. One calendar, fixed from all four legs whatever a rung's OFF status. Roll seams at ±10 weekdays are a sensitivity | §C uses Explore/Confirm, which this replaces; #733 `pass_floor_halves` precedent | #783 `common_calendar`, `outside_roll_seams` | A roll-date list. The verdict label is capped at "clears on exposed history (model-fitted)" |

**Fidelity gate FG (before the run, and so before funding):**
1. per leg, the route is the valid one for its rung (§3.3), with the parity anchor re-shown at the rung wherever port replay is used: for Striker the corrected port's Step 3 contract and Step 6 replay (§3.3), for Vanguard V-0. Any re-shown anchor, V-0 included, also needs the F11 revalidation on the moved emulator that is still owed (T10 reconciliation R1 hold item (ii));
2. a test outside `lab/` (keeping the lab↔ops boundary) showing that the adapter's per-trade quantities equal the rail's sizing law (`LegSize` and adds) at the frozen sizing on the same signals.

P-L3 is not this gate: it is a synthetic three-way sizing-law check (LE2), and its card forbids parity over real exports at a non-identity size. P-L3 stays a later QUAL gate.

### 5.2 Statistical standing

- **No holdout exists.** Every admitted panel is fully exposed through step 12, Tier 1 and Tier 2 (lineage manifest `exposure`). Excluding FLOOR-HALF, or any configuration, after another result has been read would not restore an untouched holdout, so the earlier exclusion rule is withdrawn. FLOOR-HALF stays the starting point whether or not the T00 step-3 result is read first.
- **Exposure history is retained.** The manifest's K0 composition (step-12 screen plus the size-feasibility grid), trial 9 (FLOOR-HALF) and its exposure entry stay as written. Each later read that could inform a choice is appended with reader and date: the T00 step-3 result, the #752 Phase-0 classification, and this plan's pre-screen. Nothing is removed.
- **Further choices are frozen.** The configuration, any justified change, each rung's quantity law and route, the policy, the cash buffer and the verdict cells are frozen in the re-scoped pre-registration before any E_0 scoring output. After the freeze, no rung is added or dropped on a scored result.
- **Trial accounting is justified, not just counted.** Every rung reuses subsets of one exposed signal history (not nested where size-dependent halts apply, as for Striker), and the scorer is not a significance test, so a K increment deflates nothing by itself. The pre-registration therefore states, per rung:
  1. the ex-ante reason it exists;
  2. which prior reads could have informed it;
  3. how the selection rule treats best-of-n when more than one rung clears. The default is: every rung must clear every binding cell on each seed and both halves, the winner rule is stated in advance, and losing rungs are disclosed.

  Each scored (configuration, policy, tier) is then entered as a trial in the existing lineage manifest, as its `further_trials` field requires, with no claim that the count corrects for selection.
- **Label.** "Clears on exposed history (model-fitted)". The only fresh evidence will come from live trading.

### 5.3 Pre-registration comes before any candidate replay

- **Rule.** No export, replay or scoring at a personal configuration runs before the re-scoped pre-registration is frozen and ratified. Basis: [checklist item 7.6.1](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-10-01--first-session-simplification-rulings-six-cuts), #733 §R and the lesson that replaying a candidate before the freeze contaminates the pre-registration.
- **Allowed before the freeze:** source reads within the read surface; the §4 pre-screen arithmetic; the §3.3 quantity-behaviour work; hashing; adapter and replay-path work on synthetic data.
- **Open source facts to settle before the freeze** (reading source carries no contamination risk; no values are quoted):
  1. **Capital basis.** For each capital-dependent element of the Striker and Vanguard ports (base, soft-stop, `ddHit`, maxDailyDD/maxTotalDD) and Aegis's initial-capital floor: does it read configured capital or live equity (#752 F7)? This is a private read in place within the read surface, and it fixes each rung's capital basis.
  2. How are ORB adds identified in the O-N export?
  3. Exports used by a re-sizing route live in `Downloads`. Re-hash them against their pins, then **copy** them (do not move: `run_four_firm_remc.py:42,47-54` pins those paths) into an ignored staging directory in the primary checkout under an F6 manifest (O3), never into a worktree.
  4. Which fixed costs are debited from the personal trading account, and on what dates?

### 5.4 #752: re-scope in place (default)

- **Default.** Re-scope Q-SFGROWTH-1 and #752 in place with a dated re-scope section that lists every changed element: question, pool, starting configuration, rungs and quantity laws, routes, policy, constants, verdict cells, windows, K entry and exposure record. It is re-frozen when Joshua ratifies it.
- **Nothing is lost or reused.** Nothing has run under Q-SFGROWTH-1, so no data or K is consumed.
- **Bookkeeping is not a prerequisite.** The pre-registration's own rule that a changed constant means a new pre-registration is met by the dated re-freeze; per Joshua (2026-10-11), it does not become a separate prerequisite. A new study ID (for example Q-SFCLEAR-1) is optional for clarity, and #752 can be superseded later. Neither closing #752 nor opening a replacement gates any step.
- **Kept, cited by `b02c173`:** §C, F6, F7, F9, and the classification of legs 1–4 (C1–C4, C6, C7 and the reference-evidence table).
- **Dropped:** K = 2,375, NAS leg 5, the structural-zero artifacts, the Explore/Confirm out-of-sample claim, F8 and the search-only parts. The stale "#778 pending merge" text is fixed.

"The clearance study" below means #752 as re-scoped, under whichever ID Joshua prefers.

## 6. Reuse map (owners preserved)

| Item | Owner (unchanged) | Reused as | Needs under this plan |
|---|---|---|---|
| #782 F9 margin | Codex cloud builder | Margin primitive with no pool assumptions | Point "B4 for #752" at the re-scoped study; independent verification; merge (its CI pytest was still pending when read); route output → `MarginFill` adapter; the limit from the ruled cash buffer |
| #783 acceptance | Codex cloud builder; the verifier seat is still to be named | Statistic, fees, calendar, bootstrap and manifest checks | Re-pin from `b02c173e` to the re-scoped head. Retire the search-only parts: `MULTIPLIERS`, `nominal_grid`, the F2 zero schema, the F8 `POOL_CASE` and its test, and the Confirm-top-only `verdict`. Keep `rank` only if more than one rung is ruled. Add per-leg fee rates and periodic fixed-cost debits. Replace the 6 F9 stubs with #782. Resolve the 18 skips against the four-leg pool. Independent verification before use |
| #775 tier | CC worker under #779; the coordinator dispatches; the merge sequencer merges | Tier, fail-closed private E_0 loader, preflight refusal | Joshua writes the private overlay (an operator act). Re-own the "Q-SFGROWTH-1" pointers if the ID changes. `micro_contract_cap` takes the finite personal cap from §3.2. `cost_per_side_usd` stays unused for scoring (§5.1) |
| #776 15% halt | Same as #775 | Live halt module, unchanged. It observes fixed-cost debits, which the clearance models | P4 wiring: an intraday equity source, a flatten executor, and routing `HaltStateError` into `book_halt`. Peak initialisation (later decision). `portfolio_id` from #777 v2 |
| #777 binding | Same as #775 | A separate listener instance | Schema v2 with a portfolio/sizing identity; a daemon and book-route overlay. Fix the docstring, which overclaims: the code only intersects instance keys. `activation_ready` stays False until items 3–4 |
| #779 card | Deployment Coordinator | Build order for items 2, 6 and 7, then P4 | Point §1/§4 at the re-scoped study. P4 is unblocked (#780 merged) but must build on `2cfb3d7` or later and preserve `sources_healthy` and `held_unhealthy`. Add the P-SW packet (§7). Record the `book_account_owner.py` writer order (§8). The card forbids `book_policy.py`, so row 2.2 is its own card |
| #773 P-L1, P-L2, P-L3, P-L4, R-SV, P-L5 | Per the #773 cards. Packets that touch sizing are CC solo, never GLM (#773 §5) | Live size-vector seam, owner binding, synthetic three-way sizing-law check (LE2), interlock seam, stamped vector on the live route, records chain | Personal-lane dispatch timing is a later Joshua re-ruling of #773 Q6/G-3. The personal root hash is the clearance study's frozen sizing hash. P-L4 needs a personal GO field |
| #770 licensing, #774 economics | Existing note owners | CME category (A8 recommended) and Tradovate costs; the g\* hurdle and "fund only after a lane clears" | Answers are still outstanding. Personal funding checkpoint per #774 §6 |
| #780 (merged `2cfb3d7`) | Protection-health worker | The unhealthy-source hold for protection amends | P4 must preserve its routing |

## 7. Agreement restrictions and the one-account switch check

### 7.1 What the Agreement permits and what still binds

- **Published exception; no permission gate.** §6.6 Exclusive Use says "the Trader may use the bot on the Trader's personal accounts". The same bullet bars use across multiple firms, and the next sentence keeps the bot for the trader's own use within Tradeify. On Joshua's correction 1, the personal brokerage account is read as a personal account, not another firm; this is the adopted reading, and §6.7(a) does list a broker among External Accounts (which binds the opposing-exposure rule below).
  - §6.6 sets no prior-permission step. Its Compliance & Verification requests follow a flag, but §1.6 and §6.7(g) let Tradeify request documentation, trading records and External Account statements at any time, so the ownership and records evidence below is kept ready on that basis.
  - A Tradeify reply, including support's 2026-10-08 template reply ([exclusive-use replies](./2026-10-10-tradeify-exclusive-use-replies.md)), is weighed against that published text. It does not by itself block personal-only deployment.
  - The residual ambiguity ("personal accounts" is undefined) is Joshua's to weigh; it is not a gate.
- **Ownership (binding).**
  - §6.6: the trader must be able to prove sole ownership of the bot or strategy, with nobody else having access to it or using it; the bot must not be high-frequency.
  - §6.7(b): no team trading, third-party management, or copying or mirroring trades with any other person. Its own-account copy allowance covers Tradeify accounts only; the personal-account reuse rests on §6.6.
  - §2.4: the Tradeify account is used only on Tradeify's platform.
  - Evidence kept for a §6.6 request: the Pine and ports stay private (AGENTS.md public-clone posture), authorship history is retained, and the instances share no credentials (#777).
- **Opposing exposure (binding).**
  - §6.7(c)–(e): long and short positions held at the same time in the same product or Product Group, within one account or across a Tradeify account and an External Account, are prohibited. A personal brokerage account is an External Account.
  - Liability is strict: intent, contract size, month, entry timing and whether risk actually offsets are irrelevant, and a micro against a mini counts. The rule applies at all times and to every account type.
  - §6.7(h): a breach puts every involved account in violation and can end in termination and a ban. (§6.7(i) covers Cross-Platform Accounts at other prop firms; the personal account is caught by (c) as an External Account.)
  - **No cure window.** A breach exists as soon as positions overlap, and none is published. Pending orders count, because a resting or delayed order that fills during the other account's position creates overlap.
- **Product Groups.** The canonical record is `ops/prop_envelope_default.md` §4a (re-verified 2026-10-02 against article 10495868): MYM and MNQ in Equity Index, MGC in Metals, 6J in Currencies, with Volatility cross-linked to Equity Index. The list is explicitly not exhaustive, so an unmapped product fails closed. A machine-readable mapping file linked from §4a (configuration as code) holds the groups, cross-group offset pairs, article URL, updated date, retrieval date and content hash. Joshua re-verifies it before each armed session; agent fetches of help.tradeify.co meet Cloudflare 403 responses, which are not bypassed.

### 7.2 First deployment: one account at a time

Simultaneous operation is outside the first deployment. It would need its own safeguard and Joshua's ruling.

**Switch check (both directions).** Before the incoming account takes any order (an arm, a drill row, a weekly preservation trade or a manual order), the outgoing account must be verified on all three points:
1. **Flat:** a broker-confirmed zero position in every product.
2. **No working orders:** no resting entry, protective, bracket or OCO order.
3. **Cannot submit delayed entries:** its rail instance is disarmed (`dry_run=true`, emission off on its route), and no queued, retrying or scheduled order path remains. That covers the daemon queue, listener retries, pending CrossTrade commands, alerts routed to it, and any open operator or agent order procedure.

**How the check runs.**
- **Symmetric.** It applies from Tradeify to personal and from personal to Tradeify, weekly preservation trades included.
- **Evidence.** Each point is recorded with a timestamp and a hashed capture. On the Tradeify evaluation this is Joshua's own platform observation, because automated reads beyond R-1/R-2 are not authorized and R-1/R-2 cannot show flatness. The record goes to the arm interlock and the EventLedger, which supports a §6.7(g) records request.
- **Uncertainty blocks.** A stale, failed, contradictory or incomplete read, a working order that no rail owns, or an unreachable instance stops the switch. The outgoing account is resolved first (attended) and the incoming account stays disarmed. There is no time window or tolerance.
- **No order of any kind goes on the inactive account;** any order makes it the incoming account and requires the switch check first.

**Within the active account.**
- The book's legs carry one direction per group (6J SELL; MYM, MGC and MNQ BUY, `book_policy.py:181-198`), and sizing cannot reverse a leg.
- Same-account opposition is still possible through broker-side paths: a duplicate close (`order_id` idempotency is DISPROVEN), a close racing a protective stop, an orphaned protective order, a wrong-account route, or leg drift such as micro yen or a new strategy.
- Two stale comments still describe c1 as long-only (`c1_rail_listener.py:146`, `core/firm_rules.py:255-261`); route the fix by seat.

| Layer | Behaviour | Placement |
|---|---|---|
| L0 static | At activation and at arm, resolve the leg table from the instance's deployed image and config identity, not from the source tree. Every product must be mapped, every group must carry one direction, and no cross-group offset pair may be present. The mapping file's hash and date must be valid | #777 `validate`/`activation_ready` and the `c1_rail_arm.py` interlock |
| SW switch | The three-point switch check above, in both directions; refuses on any uncertainty | The arm interlock and the operator order procedures (preservation trade, drills) |
| L1 pre-send | A risk-add is refused unless the active account's group state is fresh and shows no opposing position or working order. Exits are reduce-only, capped at the broker-confirmed quantity | The account owner's dispatch path, after the side check (`book_account_owner.py:1772-1777`) |
| L2 own-account monitor | Reads the active account on a fixed cadence and on every fill. On a net position against a leg's entry side, an opposing position or an unknown order, it writes a durable halt of risk-adds and pages the operator. No automatic resume | Per instance, own credentials only |

**If an overlap is ever observed:** it is already a breach, and no window cures it. Flatten with the route's reduce-only close (capped at the broker-confirmed quantity), halt both instances, record the incident for §6.7(g)/(h) and inform Joshua. Agents may exit positions at the operator's direction (AGENTS.md).

**Tests** are adversarial, with each layer tested while the others are mutated off.
- **Switch:** refused when the outgoing account has a position, a working order, an armed instance, a queued or retrying order, a stale read or an unknown order; both directions; the preservation-trade path is covered.
- **L0:** refuses a short Equity Index leg, a long 6J leg, an unmapped leg, a long FVS leg alongside long Equity Index, and a leg-table difference from the deployed image.
- **L1:** refuses an opposing entry with the side check off; refuses an over-sized or duplicated flatten and a wrong-account exit.
- **L2:** detects a reversal from a close-versus-stop race, and flags an orphaned protective order.
- **Restart:** nothing is released until the inventory is fresh and the mapping hash verifies.
- **Mapping:** an expired mapping blocks.

**Owner.** A new packet, **P-SW**, under #779 (coordinator). It is rail-bound, so it is CC solo. L0 can ride with P4.

**Item 5 closes** when the switch check, L0 and own-account L1/L2 are accepted, the mapping file is verified, and the ownership evidence is retained. Item 5's copy-trading, hedging and account-linking questions are answered against the published text in §7.1. A written Tradeify answer is not required. Joshua may still ask Tradeify compliance for a clarification; any reply is weighed, not treated as an automatic block.

## 8. Live path to an attended armed personal session

The personal session sits downstream of most of the Tradeify book-route build: T09, TB-I3, the live route packet, T13 and T14. It also adds new personal items. The legacy single-leg path cannot trade the book (#773 scope note §1).

| # | Packet | Layer | Owner | Depends on |
|---|---|---|---|---|
| 0.1 | Ratify #784 as corrected; rule O1–O4 (§9) | AUTH | Joshua | — |
| 0.2 | Send the external asks. **CME:** category A8/A9/A1; internal bars; non-professional device count; the Tradeify evaluation as a destination of the personal feed, including its effect on non-professional status. **Tradovate:** Q1–Q12; API order eligibility; read-only API scopes; published per-contract margins for 6J, MYM, MGC and MNQ by margin type. **CrossTrade:** terms for a live personal account. **Tradeify:** an optional clarification, not a gate | AUTH | Joshua | — |
| 1.0 | Pre-screen (§4): margin, fee, volatility and fixed-cost snapshots; private arithmetic on the retained configuration | QUAL | Coordinator (Joshua for any value outside the read surface) | 0.1 |
| 1.0b | Short decision-ready sizing proposal: any justified change from R0, quantity law and route per rung (§3.3), personal policy (§3.2), cash buffer (§4), verdict cells | AUTH input | Coordinator drafts; Joshua rules | 1.0 |
| 1.1 | Settle the open source facts (§5.3); re-scope #752 in place (new ID optional); freeze with the literal sizing, routes, anchors and snapshots | QUAL | Coordinator; Joshua ratifies | 1.0b |
| 1.2 | Route adapters, the personal replay path for port-replay legs, the #783 re-pin, #782 integration, independent verification | IMPL | Codex builder (#782/#783); the coordinator dispatches the replay-path build and names the verifier | 1.1; 2.2 or an injection path for the replay policy |
| 1.2b | FG fidelity gate (§5.1). Without FG PASS, neither 1.3 nor 1.4 proceeds | QUAL | Coordinator | 1.2 |
| 1.3 | Run the clearance **locally** by default; the Azure VM only under a per-run admission. Output: RESOLVED or not, with a frozen sizing hash | QUAL | Coordinator | 1.2b |
| 1.4 | Personal funding checkpoint: if RESOLVED and (median terminal − E_0)/E_0 ≥ g\* (compared privately), fund the API add-on, key balance, data entitlement and licence | AUTH | Joshua | 1.3, 0.2 |
| 2.1 | Merge #775, then #776 and #777 (retargeted to main) | IMPL | Existing owners; merge sequencer | — |
| 2.2 | Parameterize the book rail by tier and instance (`book_policy` `TIER`, cap and `require_policy`; the startup parser's 80s; settlement; account-close; `book_capacity`; the M1 Stage-1 contract) with the personal policy (§3.2). The Tradeify path stays byte-identical | IMPL | New card; CC solo, dispatched by the Deployment Coordinator; merge sequencer merges. Needs a D-B11 amendment | After GC-5-DISPLACED merges (it shares `book_policy.py` and `book_capacity.py`), and after the Tradeify screen has consumed H′, or via an injection path that leaves `book_policy.py` untouched. Editing that file moves H′ and repeats P7 §7 step 1 |
| 2.3 | #777 v2: sizing identity plus a daemon/book-route overlay | IMPL | #777 owner | 2.1 |
| 2.4 | P4: arm refusal without halt state, entry gate, flatten executor, `HaltStateError` → `book_halt`, intraday equity source, and a live margin gate (personal capacity against margin with the ruled buffer; `book_capacity` enforces only the Tradeify cap) | IMPL | #779 card | 2.1, 2.2; `book_account_owner.py` queue |
| 2.5 | P-SW (§7.2): switch check in both directions, L0, own-account L1/L2, adversarial tests | IMPL | #779 card; CC solo | 2.4; `book_account_owner.py` queue |
| 2.6 | #773 chain: P-L1 → P-L2 → P-L3 (the synthetic sizing-law check) → P-L4 with a personal GO field | IMPL + QUAL (P-L3) | #773 owners | #773 dispatch ruling, 1.3, 2.2; P-L2 in the `book_account_owner.py` queue |
| 2.7 | Define the personal deployment GO and monitoring acceptance; bake them into a per-instance image (TB-I3 D-3 = U) | AUTH + IMPL | Joshua (admission-ADR owner); TB-I3 card | 2.6 |
| 2.8 | Live route packet (R-A1/R-H/R-J, R-SV, D-SV-1), written instance-parameterized from the start | IMPL | Book-route owner | 2.6 |
| 2.9 | Order route: the T09 adapter (CrossTrade) or a direct Tradovate API equivalent. Gates B–D come first | IMPL | T09 owner | 0.2 |
| 2.10 | T13 per instance: heartbeat, notifier, HB-L1/L2, Q7, route preflight, the Tradovate trade-desk fallback, and an actor inventory that includes broker margin liquidation | IMPL | T13 card | 2.9 |
| 3.1 | Feed: written CME and Tradovate answers (ADR items 3–4). These gate any feed activation, shadow included | AUTH | Joshua | 0.2 |
| 3.2 | Tradovate adapter against `BarSource` (#619) → shadow with emission disabled → T14 PASS under the frozen equivalence spec, including FEED-16 | IMPL + QUAL | T14 owner | 3.1, 1.4 |
| 4.1 | Combined acceptance of the disarmed candidate (T16-analogue): the sizing hash is equal end to end (clearance → GO → loader → owner stamp); image and config manifest; feed PASS; route drills; halt, margin, switch-check and L0–L2 tests; pin H. No live GO | QUAL | **Codex deployment coordinator** (unchanged owner) | 2.1–2.10, 3.2, item 5 closed (§7.2) |

**`book_account_owner.py` has one writer at a time.** Basis: umbrella `:245` ("No two live packets share a file") and the GC-5 card §9 order, #628 → GC-5-DISPLACED → TB-I3 S2. P-L2, P4 and P-SW L1 join that queue after TB-I3 S2, in the order #779 records. Each is cut from `main` after its predecessor merges.

**Attended end-to-end qualification (after 4.1).** The Codex deployment coordinator accepts release evidence (T17-analogue). Joshua owns every GO.

| Step | Content | Layer |
|---|---|---|
| E1 | Facts: personal entitlements, the known-order definition, the actor inventory, and whether a Tradovate sim account can host the drills | QUAL |
| E2 | X-1…X-5-style commissioning drills, **on the Tradovate sim account by default**. Written CP-3 authorization before each row; each trace is reviewed before the next row | AUTH + QUAL |
| E3 | M1 for this instance (it does not transfer from the Tradeify instance); book-route monitoring acceptance. If M1 evidence itself needs a live-money row, that needs an explicit Joshua ruling recorded with the M1 owner | QUAL + AUTH |
| E3b | Any live-money drill row is a live order on the personal account. It runs only after all seven ADR items are closed, M1 is `RESOLVED` for this instance and the live-spend GO is given | AUTH + QUAL |
| E4 | Rehearsal on the final candidate with synthetic inputs: halt trip, flatten, resume-GO refusal, restart without stale authority | QUAL |
| E5 | Pre-arm capture: account, flatness, working orders, fingerprint. The switch-check record for the Tradeify account (flat, no working orders, cannot submit delayed entries), as Joshua's own platform observation with a hashed capture. Joshua's attestation listing every account he controls and its positions in mapped groups. The route authentication preflight | QUAL |
| E6 | Arming GO: the personal deployment GO is baked in; `--arm` with `armed_until`; activation acknowledgment; read back the stamped sizing hash after restart | AUTH |
| E7 | Deployment GO and a GO for one attended session; the live-spend GO is separate | AUTH |
| E8 | Session: the 15% halt is live; no Tradeify order inside the window; any incident ends automation for that session ([§A11.2](../adr/2026-09-17-bounded-platform-protection-incident-contract.md#a112--operator-ruling-no-same-session-restart-of-automation-after-an-incident-2026-09-27)); disarm before the absolute `armed_until`. Returning to the Tradeify account needs the switch check on the personal account | — |
| E9 | Reconcile, then an explicit review before any further session. Every later session needs its own GO, and a resume after a halt needs a single-use resume GO (#776) | AUTH |

| Gate | Blocks | Holder |
|---|---|---|
| All seven ADR owed items | The first live order on the personal account, live-money drill rows included | Joshua |
| ADR item 1 (clearance study RESOLVED, after FG PASS) | Capital authorization and funding | Joshua |
| ADR items 3–4 (Tradovate API, CME licence covering every destination) | Any feed activation, shadow included | Joshua |
| ADR item 5 (switch check, L0–L2, mapping, ownership evidence) | 4.1; the first live personal order | Joshua |
| M1 `RESOLVED` for this instance | Arming (`dry_run=false`); any live spend | Joshua |
| Personal deployment GO (baked into the image) | Arming, or a `dry_run=false` boot | Joshua |
| Live-spend GO | Any live order, drills included | Joshua |
| Per-session GO | Every armed session | Joshua |

## 9. Dependencies and open decisions

**No headline date.** None of the critical dependencies below has a grounded duration yet. A date can be given once the external answers arrive and each build track has an accepted card with its own estimate.

| Dependency | Gates | Current state | Timing basis |
|---|---|---|---|
| O1–O4 rulings | Pre-screen and preparation | Pending | Operator |
| Authoritative personal margin inputs | Pre-screen margin check; cash buffer; P4 live margin gate | Missing (§4) | Not grounded: depends on Tradovate's published page or its answer (0.2) |
| Fee, volatility and fixed-cost snapshots | Pre-screen; clearance fees and fixed costs | Not taken | Not grounded |
| Sizing proposal and its ruling | Freeze (1.1) | Not drafted | Follows the pre-screen; not grounded |
| Personal sizing and protection policy, row 2.2 or an injection path | Any executable personal sizing; personal port replay | Not drafted. Row 2.2 waits for GC-5-DISPLACED and the Tradeify screen's use of H′ | Depends on T00 and GC-5 timing; not grounded |
| Personal replay path (port-replay legs) | Clearance run for Striker and Vanguard, and for ORB under protection | Not built | Comparable in scope to card #758; no duration recorded here |
| #782/#783 verification and re-pin | Scorer and margin primitive | Builder tests only; CI pending when read | Not grounded |
| External answers (CME, Tradovate) | Any feed activation (items 3–4); API order eligibility | CME silent since 10-04; Tradovate's follow-up acknowledged only | Unknown |
| Feed build (adapter, shadow, T14 PASS) | 4.1 | Waits on the answers | Not grounded here |
| Order route (T09 or direct API, after gates B–D) | 4.1 | T09 owner | Not grounded here |
| P4, #777 v2, P-SW (`book_account_owner.py` queue) | 4.1 | Queue after TB-I3 S2 | Queue order; not grounded |
| #773 chain, personal GO, live route packet | 4.1 | Per the #773 cards | Not grounded |
| T16-analogue, then the attended qualification | First armed session | — | Not grounded |

**Open now (to authorize the corrected pre-screen and preparation):**

| # | Decision (Joshua) | Recommendation |
|---|---|---|
| O1 | Authorize the corrected pre-screen (§4) and preparation: the snapshots, source-fact reads (§5.3), the §3.3 quantity-behaviour work, the personal-policy draft, the #752 re-scope draft, and adapter and replay-path work on synthetic data. No export, replay or scoring at a personal configuration | Yes |
| O2 | Read access to the retained configuration's literal values (r3d startup policy, Q1 options sheet), in place in the primary checkout, for the pre-screen arithmetic only | Grant it to the coordinator, or run that arithmetic yourself |
| O3 | Private-evidence authority (F6) for every private artifact the pre-screen and preparation create: snapshots, E_0-linked arithmetic, staged export copies. They go in an ignored primary-checkout directory, never a worktree, and are recorded by hash | Yes, scoped to the pre-screen and preparation |
| O4 | Ratify #784 as corrected | Yes |

**For the sizing proposal (Joshua rules after it):**

| # | Decision | Proposal will carry |
|---|---|---|
| S1 | Changes from the retained configuration | Each change with an ex-ante justification; none by default |
| S2 | Personal sizing and protection policy (§3.2) | Finite cap source; Striker risk-dollar basis; normal mode plus the 15% halt |
| S3 | Cash buffer and margin basis (§4) | A buffer with its rationale; no number proposed yet |
| S4 | Quantity law and route per rung (§3.3) | Port replay by default; re-sizing only for Aegis at fixed q under a policy with no protected scaling and ORB in normal mode at integer q, both at lifecycle AUTHORIZED, stated as an override of RC-1 and #752 §B/F7 |
| S5 | Verdict cells, windows, label and trial accounting (§5.1–§5.2) | As in §5.1; label "clears on exposed history (model-fitted)" |
| S6 | Funding gate | g\* counting only costs not debited in the path, compared privately |
| S7 | #752 re-scope text (§5.4) | Re-scope in place; a new ID only if you want it |

**Later, at their gates (still open):**
- ADR item 2's re-MC: the clearance scorer at E_0 under `Personal_Tradovate` discharges it, since the preflight refuses this tier by design.
- Order route: CrossTrade, revisited if its personal-account terms fail.
- M1 per instance, with an instance and tier check added to the validator.
- Funding and a personal spend ceiling: the $700 rail-GO ceiling does not cover personal costs.
- Halt peak initialisation: broker-reported equity at first arm.
- VM admission for 1.3: run locally by default.
- The D-B11 amendment for row 2.2.
- #773 personal-lane dispatch: this should follow clearance RESOLVED, not the Tradeify screen GO.
- A read scope for automated own-account reads of the Tradeify evaluation: needed only to automate the switch check on that side.

**Removed as decided or obsolete:** the #752 close-and-reopen step; options A–D and the M ladder; the ordering of D3 against the T00 result; the remediation time bound; the 0.85·E_0 limit; lane priority, which is replaced by one account at a time; the Tradeify written answer as a gate.

## Review disposition

| # | Finding | Lens | Severity | Disposition |
|---|---|---|---|---|
| 1 | D12 presented as optional; item 5 already gates the first live personal order | governance | P2 | Fixed: §8 gate table. Lane priority is now subsumed by row 31 |
| 2 | Azure VM run implies an unadmitted private-data upload | governance | P2 | Fixed: 1.3 runs locally by default |
| 3 | R-1/R-2 stretched to a recurring flatness read | governance | P2 | Fixed: the switch check uses Joshua's platform observation with a hashed capture (§7.2) |
| 4 | Combined acceptance reassigned from the Codex deployment coordinator | governance | P2 | Fixed: 4.1 and release evidence go to the Codex deployment coordinator |
| 5 | P4 and P-OES missing from the `book_account_owner.py` writer queue | governance | P2 | Fixed: §8 queue note (P-OES is now P-SW) |
| 6 | Row 2.2 changes D-B11 without a ruling, conflicts with GC-5-DISPLACED, has no owner | governance | P2 | Fixed: D-B11 amendment listed; sequenced after GC-5-DISPLACED; owner named |
| 7 | Route E reverses #752 §B and F7 without saying so | governance | P2 | Superseded by row 38: port replay by default; overrides only for Aegis at fixed q and ORB normal mode |
| 8 | #773 dispatch re-gated without a decision item | governance | P3 | Fixed: listed under later decisions |
| 9 | "Joshua's ruling" labels read as rulings already made | governance | P3 | Fixed: Status and decision labels |
| 10 | F8 HOLD lift attributed to 2026-10-11b | governance | P3 | Fixed: §1 table; lifted by ratifying the re-scope, or by #784 naming it |
| 11 | Moving Downloads exports; private-evidence authority too narrow; FLOOR-HALF read outside the read surface | governance | P3 | Fixed: copy and stage (§5.3); O3; O2 |
| 12 | Route E trade set is capital-dependent; bracket bounds only quantity; P-L3 cannot be the fallback trigger | stats | P1 | Superseded by row 38: per-leg routes; capital basis per rung; FG before the run; the bracket was dropped with Route E |
| 13 | Fixed monthly costs excluded from the halt path; growth/g\* unit mismatch | stats | P2 | Fixed: Fixed-costs row, D in d/l, funding test restated as a rate |
| 14 | MAE granularity screen selects on the tested channel | stats | P2 | Fixed: ex-ante risk in the pre-screen (§4) |
| 15 | Recording exposure does not remove T00 selection on Option A | stats | P2 | Superseded by row 35: exclusion does not restore a holdout; FLOOR-HALF stays the start |
| 16 | C3 is not the minimum; k = 2 is not executable | stats | P3 | Superseded by row 32: no ladder |
| 17 | Verdict cells and ranking cell underspecified after dropping Explore/Confirm | stats | P3 | Fixed: binding cells; ranking only with more than one rung (§5.1) |
| 18 | Scalar `cost_per_side_usd` would recreate a flat rate | stats | P3 | Fixed: per-instrument rates in the snapshot; tier field unused for scoring |
| 19 | Live-money drill rows could precede item 5 closure | compliance | P1 | Fixed: item 5 is a dependency of 4.1 and of E3b; E2 runs on sim |
| 20 | Phase 1 exclusion is one-sided and checked once | compliance | P1 | Superseded by row 31: two-way switch check at every switch |
| 21 | R-1/R-2 cannot show flatness | compliance | P2 | Fixed with row 3; also applied at E5 |
| 22 | Cross-group link and non-exhaustive clause missing; mapping file duplicates §4a | compliance | P2 | Fixed: §4a canonical with a linked file; offset pairs in L0; unmapped fails closed |
| 23 | §6.7(b) copying and account-linking dropped from item 5 | compliance | P2 | Fixed: kept in item 5 and answered against the published text (§7.1) |
| 24 | Live-money drills before M1 `RESOLVED` | compliance | P2 | Fixed: sim by default; E3b after M1 |
| 25 | L2 remediation undefined; a read-only component writes halts | compliance | P2 | Superseded by row 31: own-account L2 only; an overlap is a breach and is handled as an incident, with no window |
| 26 | L1 placed beside a protection-only hold | compliance | P3 | Fixed: placed after the account-owner side check (`:1772-1777`) |
| 27 | L0 reads the source `BOOK_LEGS`, not the deployed images | compliance | P3 | Fixed: leg tables resolved per deployed image |
| 28 | Other External Accounts not enumerated | compliance | P3 | Fixed: account-list attestation at E5 |
| 29 | CME ask omits the Tradeify evaluation as a destination | compliance | P3 | Fixed: added to 0.2 |
| 30 | Blanket §6.6 permission gate has no textual basis | operator (Joshua, 2026-10-11) | correction 1 | Fixed: §7.1 quotes the published exception; ownership and §6.7 restrictions kept; no written answer required |
| 31 | Five-minute fix window is not a published allowance | operator | correction 2 | Fixed: §7.2 two-way switch check; uncertainty blocks; an overlap is a breach |
| 32 | Smallest base gear could re-enable a leg the successor disables; personal margin inputs missing | operator | correction 3 | Fixed: §3.1 starts from the retained configuration; §4 states that margin inputs are missing |
| 33 | Striker described as unbounded | operator | correction 4 | Fixed: §3.2 bound with file:line; personal policy required |
| 34 | "K 9 → 11" does not justify the trial accounting | operator | correction 5 | Fixed: §5.2 |
| 35 | Excluding FLOOR-HALF after another read does not restore a holdout | operator | correction 5 | Fixed: §5.2; exclusion rule withdrawn |
| 36 | 85% margin utilization without a cash-buffer rationale | operator | — | Fixed: §4 buffer decision, number left open |
| 37 | 6–8 weeks presented as a forecast | operator | — | Fixed: §9 dependency table, no headline |
| 38 | D4 must precede sizing; a scaled Pine input is not a fixed live quantity | operator | — | Fixed: §3.3 quantity-behaviour table and rung rules |
| 39 | Closing #752 made a prerequisite | operator | — | Fixed: §5.4 re-scope in place by default; new ID optional |
| 40 | Aegis re-sizing at fixed q ignores ⌊q × 0.40 × lifecycle⌋ under protection (`:531`, `:557-558`) | verification | P1 | Fixed: §3.3 Aegis row, rung rules, R0, S4. Re-sizing only with no protected scaling and lifecycle AUTHORIZED; ORB carries the same lifecycle condition |
| 41 | "Discretionary orders in any mapped group" implied unmapped orders on the inactive account | verification | P1 | Fixed: §7.2, no order of any kind on the inactive account |
| 42 | #784 omitted the "within Tradeify" sentence; both files stated "not another firm" as fact | verification | P2 | Fixed: §7.1 and #784 give the adopted reading, §6.7(a)'s broker term and the residual ambiguity |
| 43 | "Documentation only if flagged" overstated | verification | P2 | Fixed: §1.6 and §6.7(g) allow requests at any time (§7.1, #784) |
| 44 | Vanguard example map could disclose a retained-vector value | verification | P2 | Fixed: generic wording |
| 45 | Striker anchored to S-0 203/203, which ran the superseded port | verification | P2 | Fixed: Step 3 contract and Step 6 replay for `efd479b6…`; F11 revalidation owed for any re-shown anchor (§3.3, FG) |
| 46 | O-N/O-P status stale | verification | P3 | Fixed: ACCEPTED-by-reference at q = 1 under finite leverage (§3.3) |
| 47 | §6.7(i) cited for consequences | verification | P3 | Fixed: §6.7(h); (i) is prop-firm Cross-Platform hedging |
| 48 | Re-sizing exceptions did not say they override RC-1 | verification | P3 | Fixed: rung rules and S4 |
| 49 | `microCap` at ⌊80k⌋ = c = k only when 80k is an integer | verification | P3 | Fixed: §3.3 Striker row |
| 50 | "Nested subsets" wrong under Striker's size-dependent halts | verification | P3 | Fixed: §5.2 |

## Addendum 2026-10-12 — row 2.2 order

Joshua, 2026-10-12, directly to the Deployment Coordinator, verbatim: "1 yes, 2 yes": run-path card A (which carries row 2.2's `book_policy`/`book_capacity` parameterization for the study path) lands before GC-5-DISPLACED; GC-5 re-anchors after it ([live-wiring packet §6b](2026-10-11-live-wiring-decision-packet.md#6b-owner-file-order-amendment-2026-10-12)). P-L2 may also precede GC-5 and TB-I3 S2.

