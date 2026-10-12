# Q-SFCLEAR-1 — Personal clearance of the Tradeify book at R1: verdict pre-registration

**SUPERSEDED-BEFORE-RUN 2026-10-11** by [Q-SFCLEAR-2](Q-SFCLEAR-2-verdict-preregistration.md) (DRAFT — NOT RATIFIED); see its §S for the eleven Codex findings (review 5484097066) and Joshua's rulings (a)–(d) ("accept all four, have the worker draft the successor"). The freeze recorded below is void: its §12 step 2 operator re-hash was never recorded. Nothing was scored, exported or replayed under this file. The text below is the frozen record, unchanged; the successor governs.

**Status:** FROZEN 2026-10-11. Ratified by Joshua, 2026-10-11, directly to the Deployment Coordinator (relayed to the drafting worker): "confirm the §1 rulings, ratify Q-SFCLEAR-1". No constant below moves; a changed constant is a new pre-registration and a new trial. No export, replay or scoring at a personal configuration ran before this freeze.
**Re-scopes:** [Q-SFGROWTH-1](Q-SFGROWTH-1-verdict-preregistration.md) and PR #752 under [ADR addendum 2026-10-11b](https://github.com/Joshua-Asante/first-passage/blob/d7ad4d8d672790dfbe647b22fd9d75a95576f109/docs/adr/2026-10-09-self-funded-tradovate-lane-reopen.md#addendum-2026-10-11b--tradeify-book-reused-on-the-personal-lane-supersedes-the-option-c-split) (PR #784). Parent brief: [Q-SFCLEAR-1](../Q-SFCLEAR-1-personal-clearance-tradeify-book.md).
**Authored:** 2026-10-11, drafting worker for the Deployment Coordinator (owner of #752).

`E_0` is private; only the symbol appears here. Per-leg quantities are not restated here: public text uses labels, and the sizing is bound by the hash of a private canonical tuple file (§2). (R0's values are enumerable from its already-public size-vector hash, so R1 = R0 with adds OFF is not secret; the binding is for integrity.)

## §0 — Reads

All at `origin/main@2cfb3d7` unless a head is named. No export, replay, screen, MC, growth, hit or MAE output was read; the T00 step-3 result was not read.

- `ops/c1_rail/book_policy.py` — `LegSize`, `AddsRule`, `validate_size_vector` (`:212-400`); `BOOK_LEGS` directions (`:181-198`); `require_policy` (`:101-117`).
- `ops/c1_rail/qualification/contract.py:266` — `canonical_json_bytes`, the size-vector hash rule.
- `discovery_manifests/t00_tradeify_book_lineage_2026_10_10.json` — K = 9, `exposure`, `further_trials`.
- [Q-SFGROWTH-1 pre-registration](Q-SFGROWTH-1-verdict-preregistration.md) at #752 head `b02c173`: §C statistic, F6, F7, F9.
- Plan PR #785 head `7d2ce02` (`docs/notes/2026-10-11-personal-clearance-plan-tradeify-book.md`) §3–§7; ADR addendum 2026-10-11b at #784 head `d7ad4d8`.
- **Private, in place (operator O2 ruling below):** `C:\Users\joshu\t00-step3-console\personal-prescreen-20261011\` — `SIZING_PROPOSAL.md`, `prescreen.md`, `quantity_behaviour.md`, `retained_config.md`, `margin_inputs.md`, `one_contract_risk*`; all verified against its `SHA256SUMS` (sha256 `74aea70dd0df6c6e7f5a24272259511a28cf208afc4a0ff32996adeeefb3641d`). The r3d startup policy's `sizing` mapping was read in place (sha256 `53dea292…e359`, matching its folder pin).

## §1 — Context and operator rulings

Owed item 1 of the [self-funded ADR](../../adr/2026-10-09-self-funded-tradovate-lane-reopen.md#grounds), re-scoped by addendum 2026-10-11b: qualify the Tradeify book's sizing for `E_0` against Decision 4 (intraday-honest p99 peak-to-trough ≤ 15% after Tradovate costs and whole-contract rounding, with the live 15% halt). The zero-K pre-screen found the retained configuration R0 fails at least one binding pre-screen gate at `E_0`; R1 is the proposed fix (gate-level standing stays private, because pass/fail against public margins and stop risks would bound `E_0`).

**Rulings (Joshua, 2026-10-11, directly to the Deployment Coordinator; relayed to the drafting worker):** "confirm O2, accept all recommendations, go with R1". The recommendations accepted, as relayed:

| # | Ruling |
|---|---|
| O2 | Confirmed: the pre-screen's in-place read of the private retained FLOOR-HALF configuration (r3d startup policy + Q1 options sheet) is authorized |
| D2 | G0 (flat by 16:00 ET), G1 (one-contract p95 stop risk ≤ 0.20 rope), G3 (all ON legs at max size stopping together at p95 ≤ 1.0 rope) BINDING; G4 (first-notice/last-trade/roll for 6J, MGC) binding once dates are verified |
| D3 | Vanguard add-risk reading: upper (structural) |
| D4 | Rung R1 = retained FLOOR-HALF (R0) with `AddsRule.OFF` on `dj30_mym_p250` and `vanguard_mgc`; `aegis_6j` fixed live quantity at R0 base, no adds; `orb_mnq_v7` OFF |
| D5 | Cash buffer B2: u(1+h) ≤ 0.85 − g − f with g = one extra p95 stop distance on every open contract and h = 50% margin increase; PASS needs ≥ one 6J intraday-margin step of headroom |
| D6 | Personal policy: keep the existing 80-micro cap source; Striker on its port's risk$; protection P0 (normal mode + 15% halt; P0 needs code first) |
| D7 | Fixed costs paid outside the trading account; Tradovate Free plan |
| D8 | Fidelity gate extended: live path must match replay for adds OFF and for refused zero-quantity entries |
| D9 | Aegis per-contract re-sizing (RS) route allowed under P0 with its stated conditions; otherwise port replay (PR) |
| D10 | Feed funding decided separately after clearance |

Earlier rulings that stand: ADR addendum 2026-10-11b (#784: reuse the Tradeify book; §6.7 opposing-exposure restriction; one account operated at a time with the two-way switch check; §6.6 permission gate removed); the corrected plan #785; #752 F7 (captured native guards retained; no external Tradeify overlay) and F9 (retained reference friction; fee-only 1.5× stress), both of 2026-10-10. Rope = 0.15·`E_0`.

## §2 — Book identity and the frozen sizing tuple (R1)

- **Legs:** the four `BOOK_LEGS` at their locked parameters: `aegis_6j` SELL (6J full size), `dj30_mym_p250` BUY (MYM), `vanguard_mgc` BUY (MGC), `orb_mnq_v7` BUY (MNQ); Pine and accepted runtime ports pinned in `core/strategies/BOOK_SOURCES.sha256`; `effective_inputs.json` unchanged. Native guards and soft-stops as captured, `backtestMode` at reference (F7).
- **R1 (single sizing tuple; no other rung):**

| Leg | Label | Live quantity behaviour |
|---|---|---|
| `aegis_6j` | R0 base kept, no adds | Fixed quantity on every entry |
| `dj30_mym_p250` | R0 multipliers kept, **adds OFF** | Risk/cap-multiplier base; no add |
| `vanguard_mgc` | R0 port map kept, **adds OFF** | Port map (a zero-port entry is refused); no adds |
| `orb_mnq_v7` | **OFF** (R0 base 0) | Signals refused |

- **Policy:** cap source = the existing 80-micro source (shared account cap and per-leg request cap, D6); Striker risk$ = the port's configured risk$, not linked to `E_0` (D6); protection **P0** = normal mode, never PROTECTED, plus the live 15% halt (D6); lifecycle AUTHORIZED on every leg; port paper capital = the approved constructor value.
- **Capital anchor:** `E_0` by reference to the private file named in the tuple.
- **Binding:** private canonical tuple `C:\Users\joshu\t00-step3-console\personal-prescreen-20261011\R1_TUPLE.json`, **sha256 `62d7ae196059b7d98fd814c7b07a911558e8e5891dd2a669170393583b6c671f`**. It holds the `LegSize` mapping, its `size_vector_sha256` (rule: sha256 of `canonical_json_bytes(sizing)`, accepted by `validate_size_vector`), the R0 hash it derives from (`139919cd…c271`, reproduced), the change from R0 (adds only), cap source, Striker basis, P0, lifecycle, paper capital and the `E_0` file reference. It carries a random nonce, so its hash does not reveal its contents. On ratification the tuple is preserved under F6 (§12).
- **Quantity law tested = the live law:** every route reproduces the quantities the rail's `book_policy` law sends at R1 under P0 (never Pine-native sizing). This holds for the live path only once the #773 P-L1/R-SV seam carries the frozen vector (FG item 3, §7).
- **Pre-screen standing:** R1 passes every binding pre-screen gate and its rule-max book stays under the 80 cap, so the ledger never binds; R0 fails at least one binding gate. Gate-level figures and labels stay in private `prescreen.md` §4–§6.

## §3 — Binding gates (ex-ante; D2, D3, D5)

| Gate | Statement | Where enforced |
|---|---|---|
| G0 | Own-flat by 16:00 ET; denied sessions not traded (`ops/calendars/book_session_calendar_2026-10.json` `schedule_rule`) | Route and live schedule; also C-sched for RS |
| G1 | One-contract p95 stop risk ≤ 0.20 rope for every ON leg, using a leg's sizing-law bound where it has one | Pre-screen (frozen method `one_contract_risk_FREEZE.md`); re-checked at freeze |
| G3 | Σ over ON legs of rule-max stop risk at p95 ≤ 1.0 rope; Striker and Vanguard by their sizing-law bounds; Vanguard adds by the **upper** reading | Same |
| G4 | 6J and MGC: no entry or position from the start of the business day before min(first notice, last trade) of the traded contract; the live rail rolls before that window and the route uses the same roll-date list | Binding once dates are verified; the route enforces it, so a missing roll-date list is VOID (§6) |
| B2 | u·(1 + 0.5) ≤ 0.85 − g − f; u = peak concurrent intraday margin ÷ `E_0`; g = one extra p95 stop distance on every open contract ÷ `E_0` (= 0.15 × G3, with G3 in rope units); f = one month of fixed costs Tradovate actually debits from the trading account ÷ `E_0` (D7 pays them outside; if which costs are debited is still open at the run, use the pre-screen's debited-case value). u_max = (0.85 − g − f)/1.5; headroom = (u_max − u) × `E_0`, compared privately in dollars: PASS only if headroom ≥ one 6J contract's dated intraday margin (the book's largest single-contract margin step); 0 ≤ headroom < that is MARGINAL; below 0 FAIL. Only PASS clears | #782 margin check on route output (§4 test 5) |

The §6.7 opposing-exposure rule and one-account-at-a-time are deployment preconditions (§9), not scoring items.

## §4 — Hypothesis and clearance tests

**H-SFCLEAR-1:** If the Tradeify book at R1 under P0 is fit for the personal account at `E_0`, then on the exposed history it keeps hits ≤ 100 of 10,000 in every one of the 18 drawdown cells, has pooled median terminal equity > `E_0` at c = 1.5 in FULL, H1 and H2, and passes B2 on the #782 margin check. **Reject (NOT CLEARED) if** any binding cell fails.

The statistic is Q-SFGROWTH-1 §C (at #752 `b02c173`) with these changes and F9's day law:

1. **Series.** Per leg from its route (§7): per trade `g = Net PnL + Commission` once, reference slippage embedded; `d_t = Σg − c·fees_t − D_t`, `l_t = −Σ|MAE| − c·fees_t − D_t`, `h_t = Σ|MFE|`. `D_t` = fixed costs debited that day; 0 under D7 unless Tradovate debits the account anyway (open fact 6). A route output without per-trade MAE/MFE is VOID.
2. **Fees.** Dated Tradovate per-side all-in rate per instrument (commission on the Free plan + exchange + clearing + NFA; 6J at the standard rate), snapshot 2026-10-11T04:01:38Z (private, in `SHA256SUMS`), re-taken and hashed at freeze if older than 30 days. `c ∈ {1, 1.5}` multiplies only these separately deducted fees (F9). The replay emulator keeps reference friction, so native-guard and ladder behaviour is at reference friction; the fee swap is first-order for Striker's halts and Vanguard's ladder (disclosed).
3. **Calendar and windows.** One weekday calendar from the latest first session date to the earliest last session date across the four legs' admitted source panels (book `data_window` 2022-09-01..2026-09-02), fixed whatever a leg's OFF status. FULL = all W weekdays; H1 = weekdays 1…⌊W/2⌋; H2 = the rest. VOID if any window < 20 weekdays.
4. **Drawdown.** §C bootstrap unchanged per window (PCG64 `default_rng(s)`, `starts` shape (10,000, 13), non-circular 20-day blocks, H = 252, shared draws), seeds 42, 123, 2026; a hit is (intraday peak − trough)/peak ≥ 0.15 and ends the path. **Binding:** hits ≤ 100/10,000 on **each** seed at c = 1 and c = 1.5 in FULL, H1 and H2 (18 cells).
5. **Growth.** Pooled `numpy.median` of 30,000 terminal equities. **Binding:** > `E_0` at c = 1.5 in FULL, H1 and H2. The funding test g\* is separate and post-clearance (D10).
6. **Margin.** #782 `check_concurrent_margin` on route output (one tranche per add; entries before exits at equal timestamps; F9 margin correction) × the dated intraday margin per contract. **Binding:** B2 PASS (§3).
7. **Gates.** The route enforces G0 and G4; a route trade that breaches either is a route defect (VOID). G1 and G3 are re-checked at freeze on the frozen method; a failure there blocks the freeze and returns to drafting.
8. **Sensitivity (not binding, reported):** roll seams ±10 weekdays (§C), B3 stress, news-window margin.

**Label:** a RESOLVED verdict reads "clears on exposed history (model-fitted)". No out-of-sample claim.

## §5 — Forbidden moves

- Scoring, replaying or exporting at any personal configuration before ratification.
- Adding, dropping or modifying a rung, leg, gate constant, window, seed or cell after any `E_0` scoring output; a change is a new trial, a new ruling and a new freeze.
- Walking to another rung (R0, R1′, R2 or any other) after R1 fails on this data.
- Using Pine-native sizing, a capital-scaled export or RS for Striker or Vanguard; using RS for Aegis without every §7 condition.
- Turning ORB on, or re-enabling a leg R0 disables, without a new ruling.
- Toggling native guards, removing reference slippage, or adding a Tradeify overlay (F7, F9).
- Calling the result out-of-sample, a significance test, or Tradeify-screen evidence.
- Quoting `E_0`, per-leg quantities or `E_0`-linked ratios in public text.

## §6 — Verdict table

Evaluate VOID first.

| Verdict | Trigger | Disposition |
|---|---|---|
| VOID | The tuple hash, a source or anchor pin, the fee snapshot, the margin snapshot, the roll-date list (G4) or the calendar is missing or mismatched; a route trade breaches G0 or G4; a route output lacks MAE/MFE; a window < 20 weekdays; the run's input identity differs from the frozen F6 tuple; FG not PASS (the run must not start) | ITERATE: fix the input, rerun the same frozen design |
| RESOLVED | All 18 drawdown cells, all 3 growth cells, B2 PASS and §4 item 7 hold | INTEGRATE: R1 is the personal sizing binding (owed item 1 discharged on this label); the frozen sizing hash flows to the GO, loader and owner stamp (plan §8 row 4.1) |
| NOT CLEARED | VOID does not hold and RESOLVED does not hold (any drawdown or growth cell fails, or B2 is MARGINAL or FAIL) | STOP for R1: report every cell; no automatic second rung; any new rung needs a new ruling, trial entry and freeze |

A RESOLVED verdict authorizes no funding, arming, spend or order; plan §8 gates remain.

## §7 — Evidence routes and fidelity gate

| Leg | Route | Anchor and conditions |
|---|---|---|
| `aegis_6j` | **RS** (A-0 per-contract P&L, MAE, MFE ÷ qty × R1 quantity) if every condition holds; else **PR** | D9 conditions: C-mode (P0), C-life (AUTHORIZED), C-cap (ledger never binds under the 80 cap at R1 rule-max), C-sched (G0 never rejects or truncates a source trade), FG-T (fixed-quantity timing identity shown at R1's quantity with the fixed-quantity port; TB-R2 verified only two other quantities). Overrides RC-1's "any leg" text for this study, on TB-R2 §1 evidence |
| `dj30_mym_p250` | **PR** only (adds OFF is not expressible in Pine) | Corrected port `efd479b6…` Step 3 contract (`acfa7920…`/`ebcb2efb…`) and Step 6 replay, re-shown at R1 |
| `vanguard_mgc` | **PR** only (zero-port map) | V-0 (338/338), re-shown at R1 |
| `orb_mnq_v7` | none (OFF; in PR its signals are generated and refused) | — |

PR = four-leg `BookReplay` with the R1 vector under P0 and the personal schedule. If Aegis falls back to PR, all legs run in one PR.

**Fidelity gate (FG; all items PASS before the run, so before funding):**

1. Per leg, the route is the valid one above, with its anchor re-shown at R1; every re-shown anchor (V-0 included) also needs the F11 revalidation on the moved emulator (T10 reconciliation R1 hold item (ii)).
2. A test outside `lab/` shows the adapter's per-trade quantities equal the rail's sizing law (`LegSize`, `AddsRule.OFF`) at R1 on the same signals.
3. **D8:** the live path reproduces replay for `AddsRule.OFF` and for refused zero-quantity entries (live `shared_sizing_zero`, replay `zero policy quantity`; ports treat both identically). Requires the #773 P-L1/R-SV seam to carry the frozen vector.

## §8 — Trial accounting and exposure

- **One further trial.** At ratification, before any scoring, append to `discovery_manifests/t00_tradeify_book_lineage_2026_10_10.json` one trial: top-level `K` incremented by one (9 → 10 if none is added first), and inside the `params` JSON string a `further_trial_log` array (created if absent) holding `{"trial": <n>, "what": "Q-SFCLEAR-1 personal clearance of R1 (FLOOR-HALF with adds OFF on dj30_mym_p250 and vanguard_mgc) under P0 at E_0", "prereg": "docs/briefs/pre-registration/Q-SFCLEAR-1-verdict-preregistration.md", "tuple_sha256": "62d7ae196059b7d98fd814c7b07a911558e8e5891dd2a669170393583b6c671f", "reason": "R0 fails a binding pre-screen gate at E_0 (granularity of the adds; private prescreen.md §4); R1 is the only passing change that keeps R0's ON legs and base quantities and adds no constant, on either Vanguard add-risk reading"}`.
- **Reads that could have informed R1:** private `prescreen.md` §8 and `quantity_behaviour.md` §7 (bound by the `SHA256SUMS` hash in §0): #774's coverage ratios (displayed, unused), port docstrings and dataclass defaults displayed incidentally, the verifier's reads, and one memory lesson (G1 provenance). Pre-screen candidates R1′ (rejected) and R2 (withdrawn) were never scored and are not trials; they used panel volatility only.
- **Best-of-n:** one rung, no ranking; losing alternatives are disclosed above.
- **Panels fully exposed** through step 12, Tier 1 and Tier 2 (manifest `exposure`). No holdout claim; the scorer is not a significance test, so the increment deflates nothing.
- **Exposure log:** the manifest keeps K0, trial 9 and its exposure entry unchanged. At ratification append to an `exposure_log` array inside the `params` JSON string (created if absent, beside `further_trial_log`), each with reader and date and without values:
  1. the #752 Phase-0 sizing classification (2026-10-09/10; Pine read in place, no export);
  2. the private pre-screen's three entries (`prescreen.md` §8: first revision, verification pass, revision and sizing proposal, all 2026-10-11, including the panel-volatility reads of the frozen stop-risk method) and `quantity_behaviour.md` §7;
  3. *2026-10-11, drafting worker (Deployment Coordinator): read the private pre-screen records listed in §0 and the r3d startup policy's `sizing` mapping in place (O2); computed the R0 and R1 size-vector hashes with the ops launcher;*
  4. *2026-10-11, refute-first reviewer: read the same private records and `R1_TUPLE.json` in place.*

  Neither 3 nor 4 read any export, replay, screen, growth, hit, MAE or T00 step-3 output. Any later read that could inform a choice is appended the same way.

## §9 — Deployment preconditions (not scoring items)

- **One account at a time** (2026-10-11b; plan §7.2): before either account takes any order, the outgoing account is verified flat, with no working orders, and unable to submit delayed entries (instance disarmed; no queued, retrying or scheduled order path). Uncertainty blocks. No order of any kind on the inactive account.
- **§6.7 opposing exposure:** no opposing positions in the same product or Product Group across the Tradeify account and the personal account; Product Groups from `ops/prop_envelope_default.md` §4a (non-exhaustive; unmapped fails closed), re-verified by Joshua before each armed session.
- Ownership evidence (§6.6, §6.7(b)) retained; owed item 5 closes per plan §7.2. All seven ADR items, M1, arming, live-spend and per-session GO rules stand.

## §10 — Audit hooks

```bash
# Tuple binding (operator checkout; private file)
sha256sum "C:/Users/joshu/t00-step3-console/personal-prescreen-20261011/R1_TUPLE.json"   # expect 62d7ae19…671f
( cd C:/Users/joshu/t00-step3-console/personal-prescreen-20261011 && sha256sum SHA256SUMS && sha256sum -c SHA256SUMS )
# Pre-registration ratified before any scoring artifact
git log --format='%h %cI' -- docs/briefs/pre-registration/Q-SFCLEAR-1-verdict-preregistration.md | tail -1
git log --format='%h %cI' -- 'lab/analysis/c1/sfclear_2026-10/**' | tail -1   # scoring outputs live here; must postdate the freeze
# Trial entry present once
rg -n 'Q-SFCLEAR-1' discovery_manifests/t00_tradeify_book_lineage_2026_10_10.json
```

## §11 — Open facts (settle or carry before the run)

1. P0 is not executable: `require_policy` admits only trailing 1%/0.40; the personal replay path and the cap/tier parameterization are owed (plan rows 1.2, 2.2).
2. The live rail passes no size today; FG item 3 needs the #773 P-L1/R-SV seam.
3. `_cost_terms` accepts only the Tradeify fee page; the Tradovate per-instrument fee input is owed.
4. F11 revalidation of every re-shown anchor; FG-T at R1's Aegis quantity.
5. G4: delivery classification, first-notice/last-trade dates and the live roll rule for 6J and MGC (CME blocked automated access; not bypassed); the panels' roll-date list.
6. Which fixed costs Tradovate debits from the account; whether the API key balance must be held; whether API use needs Level 1.
7. Margins are undated and changeable; Tradovate's liquidation trigger is assumed at the open positions' intraday margin (to confirm); news-window rate scope (examples only, open-ended window, adds unconfirmed).
8. Vanguard's port-2 bound scales with its paper equity; stop-risk figures are lower bounds.
9. CME licence category (#770); feed funding (D10).
10. `Personal_Tradovate.micro_contract_cap` is `None` (#775); D6 requires it to carry the 80-micro source.

## §12 — Freeze procedure

Status stays **DRAFT — NOT RATIFIED** until Joshua acts. Ratification:

1. Joshua confirms in his own words the §1 rulings as recorded (they reached this draft by relay).
2. Joshua re-hashes the private tuple (§10) and confirms the R1 labels match his D4 ruling.
3. Joshua states "ratify Q-SFCLEAR-1" (or names changes, which return to drafting).
4. A coordinator commit then: sets Status to FROZEN with the date and Joshua's words; records the freeze commit in the parent brief §8 in a later metadata commit (never this file's own SHA); appends the §8 trial and exposure entries to the lineage manifest; preserves `R1_TUPLE.json` and its supporting private records under F6 in the private archive only (the tuple carries an enumerable digest of the `E_0` file, so it never enters a public surface) once Joshua grants the scoped upload authorization.
5. After the freeze no constant moves; a changed constant is a new pre-registration and a new trial.
