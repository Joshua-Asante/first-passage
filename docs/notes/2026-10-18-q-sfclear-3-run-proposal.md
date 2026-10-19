# Next portfolio experiment: run Q-SFCLEAR-3 as frozen (proposal)

**Status:** PROPOSAL, 2026-10-18. It asks Joshua for one approval: dispatch the frozen Q-SFCLEAR-3 fidelity-gate (FG) run, then its clearance run, within the budget in §6. It changes no frozen text, card, constant or trial count. Nothing has been run or scored.

**Owner:** [Q-SFCLEAR-3](../briefs/pre-registration/Q-SFCLEAR-3-verdict-preregistration.md) (FROZEN, F₃ `15bea25`), which incorporates [Q-SFCLEAR-2](../briefs/pre-registration/Q-SFCLEAR-2-verdict-preregistration.md) at F₂ `83867f0` except its §S. Where this note differs from them, they govern.

**Source.** The NinjaTrader pilot candidate inventory (Claude session, 2026-10-18) found that the only pre-registered existing-strategy portfolio test is the three-leg Q-SFCLEAR-3 R1 subset on the personal account. It is conditional and has never been scored. This note turns that finding into one approvable run.

## 1. Question and decision

- **Question:** does the accepted book at rung R1, with ORB off and three legs on, under P0, meet every binding cell of Q-SFCLEAR-3 on the exposed 2022-09-01..2026-09-02 history at `E_0`?
- **Decisions the answer changes:**
  - **RESOLVED:** R1 becomes the personal sizing binding, which discharges owed item 1 of the [self-funded ADR](../adr/2026-10-09-self-funded-tradovate-lane-reopen.md#grounds). The three-leg book also becomes the scored "book without MNQ" reference that any later MNQ portfolio comparison can cite (§7).
  - **NOT CLEARED:** R1 stops. The personal lane has no cleared sizing, and the native pilot has no pre-registered existing-book portfolio. Any other rung needs a new ruling, a new trial and a new freeze.
- **Why now:** every code prerequisite has merged (§5). Not running it leaves the only frozen portfolio study unscored.
- **What it cannot decide:** native NinjaScript parity, any firm instance, profitability, funding, arming or orders. The unpublished native reassessment proposal (2026-10-16) drops Python FG and clearance as universal dependencies. So the value of this run is the personal-lane binding plus a scored three-leg reference, not a native qualification. Joshua should approve on that basis.

## 2. Exact versions

| Item | Pin |
|---|---|
| Pre-registration | F₃ `15bea250fc8ee9a57b59735c9e8be685c4ddbf22`; incorporates F₂ `83867f0d362931c2a516a62b990bb1c209372527`. §10 hook 4 prints nothing at `main` `3d396e2` (checked 2026-10-18) |
| Sizing tuple R1 | `R1_TUPLE.json` sha256 `62d7ae196059b7d98fd814c7b07a911558e8e5891dd2a669170393583b6c671f` (private, nonce'd), derived from R0 `139919cd…c271` |
| Legs (locked parameters) | `aegis_6j` SELL 6J: fixed R0 base quantity, no adds. `dj30_mym_p250` BUY MYM: R0 multipliers, adds OFF, port-native `ddHit` and day soft-stop live. `vanguard_mgc` BUY MGC: R0 port map, adds OFF, zero-port entries refused. `orb_mnq_v7`: **OFF**, signals generated and refused |
| Sources | Pine and runtime ports pinned in `core/strategies/BOOK_SOURCES.sha256`, with Striker on the corrected port `efd479b6…11f4`. One `FP_PORT_ROOT` (the corrected-ports folder) holds all four pins plus `effective_inputs.json` (`66406dee…`) |
| Policy | P0: normal mode plus the live 15% halt; 80-micro cap source; Striker risk$ = the port's configured value; lifecycle AUTHORIZED on every leg |
| Code at the run head | Card A #821; card B #833 plus amendment (c) #861 (`6a96af3`); card C #827; card D Part 1 #840; card E #839; P-L1 #794, P-L2 #805, P-L3 #797; fixed-leg live-sizing fix #863. The run head is a later clean `main` commit that holds all of these |
| G1/G3 calculator | sha256 `2333844dd2a9342239812baa38a119b55f4b8a65841165740a9a39633f2297bf` |
| Freeze record | `sfclear3-freeze-20261014T171313Z` (private), pinned in F₃ |
| Drivers | FG: `fg_driver.py` draft `def26ea1…` (not yet bound). Clearance: `clearance_driver.py` `e4201e3f…` (bound 2026-10-15 after independent review) |

## 3. Data

- **Panels:** CME M15 TradingView exports, private: 6J with its attested prefix (`8ae083d0…`), MYM (`15b34615…`), MGC (`c5487470…`), and MNQ (`cceaac41…`, fed only so ORB's refusals are exercised). Source build `sfclear3-source-20261014T043440Z`.
- **Window:** account dates 2022-09-01..2026-09-02, which is 1,045 weekdays. 995 are PERMITTED. 50 are DENIED: 37 SHORTENED, 10 HOLIDAY and 3 OVERLAY_CLOSURE.
- **Schedule:** the historical schedule (`ab44fada…`) and the G4 roll-date list (`72677d25…`), both public and both bound.
- **One data-exclusion zero day:** 2026-02-25 (MGC bars missing), under §4-A.
- **Exposure:** the panels are fully exposed (K = 12, lineage manifest `t00_tradeify_book_lineage_2026_10_10.json`). No out-of-sample or holdout claim is possible.

## 4. Costs, joint-risk assumptions and acceptance

**Costs**

- Dated Tradovate Free-plan per-side all-in fees per instrument. The snapshot is from 2026-10-11, and its hash is bound in the freeze record.
- Fees are tested at c = 1 and c = 1.5. The multiplier applies to these fees only.
- Reference slippage is embedded in each trade's P&L.
- Fixed costs are paid outside the trading account (D7).
- Every exposed leg's 15:55 flatten fills at the R1 adverse intrabar vertex. This placement is not a proven worst case (Q-SFCLEAR-3 §S row 2).

**Joint risk: modelled**

- **One shared-account replay.** A single three-leg port replay runs on one account. It covers the capacity ledger, Aegis's priority takeover, the P0 15% latch across all legs, and size-dependent port state.
- **Bootstrap.** The joint daily series is resampled in non-circular 20-day blocks with shared draws across legs, so cross-leg co-movement within 20 days is preserved.
- **G3.** All ON legs are assumed to stop out together at rule-max size, plus two bar-open gaps per contract. This is a comonotone stop assumption: they all lose at once.
- **B2.** Concurrent margin is tested with a 50% margin increase, plus one extra p95 stop on every open contract.
- **Product groups.** 6J (FX), MYM (equity index) and MGC (metals) are in different groups. §6.7 opposing exposure therefore cannot arise inside this book. It binds only across accounts, under the one-account-at-a-time rule.

**Joint risk: not modelled (disclosed)**

- Dependence beyond 20-day blocks, and any regime outside 2022–2026.
- Within-bar slippage past stops. The residual is reported but not binding.
- Live Vanguard paper equity above the replay's maximum.
- Sessions that live policy denies but the replay permits (evidence classes).

**Acceptance (RESOLVED)**

FG must first PASS all seven items: 1a, 1b, 1c, 2, 3, 5 and 6. Then every binding cell must hold:

- **Drawdown, 18 cells:** at most 100 of 10,000 paths hit a 15% intraday peak-to-trough drawdown within 252 days. This must hold for every combination of 3 seeds, c ∈ {1, 1.5}, and the windows FULL, H1 and H2.
- **Growth, 3 cells:** pooled median terminal equity is above `E_0` at c = 1.5 in FULL, H1 and H2.
- **G1, G3, G1-D and G3-D:** each at or below its ceiling (0.20 and 1.0 rope at p95).
- **B2:** PASS.
- **G0 and G4:** no breach.
- **Striker:** no total-DD trip.

## 5. What rejects it

| Result | Trigger | Consequence |
|---|---|---|
| **NOT CLEARED** | Any binding cell fails, including a Striker total-DD trip | FALSIFIED for R1 under this placement. Do not walk to R0, R1′, R2 or ORB-on (§5 of both pre-registrations); a new rung means a new ruling and trial (K → 13) |
| **VOID** | FG not PASS; or an input/pin mismatch, a G0/G4 breach, missing MAE/MFE, or §4-A violation | No standing. Fix the input and rerun the same design, within §6 |
| **FREEZE INVALID** | Hook 4 or 4b prints anything | Only a new pre-registration cures it |

**Remaining before dispatch (owners: coordinator, Joshua):**

1. FG items 1c and 3: rule the ex-ante comparison rules. The proposals are in private `sfclear3-fg-1c-item3-proposals-20261016T001103Z`, and no public ruling has been found.
2. Review the FG driver at the run head and bind its hash.
3. Build the digest-only run manifest.
4. Fill the run head in both dispatch records. Hook 4 must print nothing there, and hook 4b must print nothing in the operator checkout.
5. Joshua opens VM access for each run (§60 addendum 2026-10-14).

## 6. Budget (Rule 2)

- **FG:** one attended Claude executor run on the Joshua-controlled VM. Item 1 is capped at 171 s. The full R1 replay plus items 2, 3, 5 and 6 share a 4 h hang bound (#862).
- **Clearance:** one run after FG PASS. Its timeout is to be fixed in its dispatch record before start, at 4× a measured synthetic run.
- **Iteration:** at most two VOID→ITERATE cycles across both runs. At that bound, stop and return to Joshua instead of retrying.
- **Spend:** no data purchase and no paid service beyond the existing VM. Deallocate the VM after each run.
- **Outputs:** private only. The public record carries the verdict label, each cell's pass/fail standing and the hashes.

## 7. Kept apart from the new MNQ research

| Track | Identity | Status | Boundary |
|---|---|---|---|
| **This experiment** | Accepted book, R1, three legs, ORB OFF; Q-SFCLEAR-3; K = 12 (T00 lineage) | Frozen, unscored | ORB stays off; turning it on is a forbidden move |
| ORB MNQ v7 solo S4 | Contract `16ce2298…acab2a`; [ratification](../briefs/pre-registration/2026-10-18-orb-mnq-v7-s4-RATIFICATION.md) 2026-10-18; its own budget (56 CPU-h) and holds | Ratified; execution and scoring holds remain | Its own trial ledger and exposure; none of its outputs are an input here |
| MNQ 15-minute redesign | `docs/superpowers/plans/2026-10-18-mnq15-mechanism-admission.md` (primary checkout) | PARKED — NOT ADMITTED (H3, H4); no contract | No candidate exists |

Rules:

- No result crosses tracks.
- K is not pooled.
- The executor of this run reads no ORB or MNQ15 output.
- The MNQ15 plan's future comparison (incumbent book, book without MNQ, book with the candidate) needs its own pre-registration. That pre-registration declares its own venue and risk basis. It may cite a RESOLVED R1 as the "without MNQ" arm only if those bases match.
