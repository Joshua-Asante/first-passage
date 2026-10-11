# Personal-clearance plan: Tradeify book at E_0

**Status:** DRAFT plan for Joshua, prepared by the Deployment Coordinator. The coordinator owns #752 under [ADR addendum 2026-10-11b](../adr/2026-10-09-self-funded-tradovate-lane-reopen.md#addendum-2026-10-11b--tradeify-book-reused-on-the-personal-lane-supersedes-the-option-c-split) (#784, open). This plan authorizes nothing: no build, export, replay, freeze, spend, arm or order. Items marked **Joshua** are decisions for him to make. Every recommendation in this plan waits on his ruling.

**Read at:** `origin/main@2cfb3d7`. PR heads read: #752 `b02c173`, #775 `d3e4487`, #776 `99126d2`, #777 `bf5579a`, #779 `2275285`, #782 `22d0924`, #783 `a6d8f02`, #784 `0c22ad9`, plus #770, #773 and #774. The review fold re-read these sources:
- the ADR 10-09 Owed preamble;
- incident ADR §A11.1;
- the deployment-checklist roadmap (`:765-778`);
- `ops/prop_envelope_default.md` §4a;
- `book_policy.py:97-116,170-200,252-258`, `book_protection_owner.py:490-498` and `book_account_owner.py:1765-1777`;
- #752 §B, F7 and the Phase-0 classification;
- the P-L3 card §5/§8 and the #773 scope note;
- the #775 tier fields;
- the GC-5 card §9.

No private value, export body or in-flight screen output was read. Nothing was run.

**Layers:**
- **IMPL:** code and packets. Workers build them, the accepting owner named in each row accepts them, and they merge only with Joshua.
- **QUAL:** evidence that the exact candidate meets its contract.
- **AUTH:** live authority, held by Joshua alone. It covers spend, the arming GO, the live-spend GO and every per-session GO.

No layer implies another.

## 1. Ruling

> "reuse the Tradeify strategies, qualify their sizing for the personal capital, and finish the personal-account operating controls. The search for additional strategies can come off this deployment's critical path." (Joshua, 2026-10-11, to the Deployment Coordinator)

**Remaining work as Joshua set it out:**
- Pin the exact book and size vector, then test personal-account drawdown, growth, fees and margin. A Tradeify screen alone does not establish these.
- Reuse #782/#783 and #775–#777.
- Finish the live wiring, feed/API licensing and the attended end-to-end qualification.

**Constraint:** Funded Trader Agreement §6.7 requires a safeguard before both accounts run together. The sizing choice stays explicit.

| Superseded | By |
|---|---|
| [Option-(c) split](../adr/2026-10-09-self-funded-tradovate-lane-reopen.md#addendum-2026-10-11--strategy-split-between-lanes-option-c), which narrowed the personal pool to strategies outside the book | 2026-10-11b: the pool is the book's four legs |
| #752 F8 (exclude legs 1–4) | 2026-10-11b |
| F8's HOLD ("Hold while additional locked candidates are admitted", a separate operator ruling dated 2026-10-10) | Lifted only by D2's closure of #752, or by #784 if it names the HOLD. 2026-10-11b does not name it |
| #752 five-leg grid, K = 2,375 | Not restored. Sizing is an explicit ruling (§3) |

| Unchanged | Owner |
|---|---|
| The T00 step-3 Tradeify successor screen (H′ `eed60a1`) is in flight. This plan touches none of its worktrees or folders. Its verdict does not clear the personal lane | [#733](../briefs/pre-registration/2026-10-08-tradeify-book-successor-screen-prereg-DRAFT.md) |
| Locked strategy parameters. The size vector can only lower quantities: `LegSize` refuses any value above today's. It has no side field (`book_policy.py:213-217,252-258`) | `core/strategies/CATALOG.md` |
| `dd_protection` constants and the Tradeify 1%/0.40 binding | AGENTS.md §Protection; [concept-not-constant ADR](../adr/2026-07-13-dd-protection-concept-not-constant.md) |
| Decision 4: intraday-honest p99 peak-to-trough ≤ 15% after Tradovate costs and whole-contract rounding, with a live 15% halt | [ADR 10-09](../adr/2026-10-09-self-funded-tradovate-lane-reopen.md) |
| All seven owed items gate the first live order on the personal account (ADR 10-09 Owed preamble). #784 re-scopes item 5's content, not that sentence | ADR 10-09 |
| M1, arming, live-spend and per-session GO rules | AGENTS.md |
| The Codex deployment coordinator keeps combined acceptance of a disarmed candidate and acceptance of release evidence | [Deployment checklist roadmap](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md) rows 5–6 |
| `E_0` stays private; only the symbol appears in public text | ADR 10-09 |
| Owed items 2–4, 6 and 7; the 2026-11-08 four-firm falsifier | ADR 10-09; program ADR |

## 2. Scope and non-goals

**In scope:**
1. Pin the book and its sizing tuple by explicit ruling.
2. Clear them at E_0 on drawdown, growth, fees (per-side and fixed) and margin.
3. Finish the personal controls: tier, halt, binding, P4 and the §6.7 safeguard.
4. Live wiring, feed/API licensing and the attended end-to-end qualification.

**Book identity:**
- The four `BOOK_LEGS` legs: `aegis_6j` SELL, `dj30_mym_p250` BUY, `vanguard_mgc` BUY, `orb_mnq_v7` BUY (`ops/c1_rail/book_policy.py:181-198`).
- Their Pine pins, and the accepted runtime ports in `core/strategies/BOOK_SOURCES.sha256`.
- The rail build (H) is pinned later, at combined acceptance (§7, row 4.1).

**Non-goals:**
- **Searching for additional strategies.** It is off the critical path but not barred. Any added leg needs its own clearance and re-runs the §6.7 static check.
- **Excluded sizing studies:**
  - Striker NAS100 MNQ (old leg 5).
  - The five-leg grid.
  - The four-leg grid (option D), unless Joshua names it.
- **Changes to locked or Tradeify-owned material:** the Tradeify binding, its size vector, Pine, ports, `effective_inputs.json` or `dd_protection`. Row 2.2 keeps the Tradeify path byte-identical.
- **Out-of-sample claims.** Every panel of this book is fully exposed (lineage manifest `exposure`), so the only fresh evidence will come from live trading.

## 3. Sizing decision (Joshua, D3)

**A personal "size vector" is really a sizing tuple with six parts:**
- per-leg `LegSize` values;
- Striker `risk_dollars`;
- Striker `cap_allocations`;
- the protection policy;
- the cap/margin basis, including a **finite** personal micro cap and Striker `max_base`;
- the **capital anchor** for each port's capital-dependent gates (§4, open fact 1).

**Why a vector hash alone does not fix live quantities at E_0:**
- The rail's sizing frame is bound to Tradeify today: `TIER`, the 80-micro `ACCOUNT_MICRO_CAP`, and `require_policy` at 1%/0.40 (`book_policy.py:64-65,99-115`).
- `Personal_Tradovate.micro_contract_cap` is None (#775).
- Without a finite cap, capped Striker trades have no upper quantity bound.

So the successor pre-registration freezes the whole tuple, not just a `size_vector_sha256`.

**Zero-K pre-screen (data-independent).** For each leg, compare one contract × dated initial margin against E_0. Granularity facts that bound the result:
- Aegis trades full-size 6J only, which is 10 micro-equivalents. No micro-yen edition has an accepted trade list.
- ORB is either 0 or 1.
- Vanguard base 1 floors to 0 when halved.
- At small Striker multipliers, wide-stop trades floor to 0. The leg then becomes a subset of its trades, not a linear scale.

Results stay private and are recorded by hash under D17.

**Ex-ante one-contract risk (replaces a realized-MAE screen).** One-contract risk = the strategy's stop rule × point value × a dated volatility snapshot taken at the freeze. Using realized MAE over the same exposed sample would select legs on the channel the 15% test then scores.

The 20% threshold has no repo source. It comes from an operator heuristic ("~20%", computed from stop distance, and window-dependent). The pre-registration therefore states it as a chosen constant, together with its statistic and snapshot date.

| Option | Definition | Reusable evidence | To build / run | K and selection | Risks |
|---|---|---|---|---|---|
| A. FLOOR-HALF | The r3d vector `139919cd…c271`: k = 0.5 under the code's round-down, with any zeroed leg OFF | Signed in r3d; re-validated at H′; #773 wiring works for any vector | The size adapter (§4) with the vector's private values. **The r3d startup policy is outside the AGENTS.md read surface (#773 Q4), so reading it needs a Joshua ruling** | +1 | Chosen for the Tradeify cap frame, not for E_0. Aegis at half the declared 6J base dominates margin. The in-flight T00 screen scores this exact vector on the same panels (trial 9), so reading that result first contaminates A |
| B. Declared book | The identity vector `dc9200a2…1fea` (equal to C2 at k = 1) | Same as A | Same as A | +1 | Eight full-size 6J; the pre-screen decides margin |
| C1. Rope-ratio cut | k = 0.15·E_0 ÷ the Tradeify rope, rounded down; any leg that rounds to zero is OFF | Formula and public rope | Private arithmetic; adapter | +1 if fixed before any E_0 output | The two ropes have different geometry (intraday % of peak vs EOD trailing) |
| C2. Largest feasible uniform k | The largest k in {1, .75, .5, .4, .33, .25, .2} where the **rule-maximum** concurrent margin (base, adds and `max_adds` per `BOOK_LEGS` at k, × dated IM) is within the D7 limit, and each leg's ex-ante one-contract risk ÷ (0.15·E_0) ≤ 20%. Failing legs are OFF | Size-feasibility grid; the minimum-contract heuristic | Dated IM and volatility snapshots; adapter. **Resolved to a literal private vector, with its hash recorded, before the freeze** | +1. Inputs are data-independent; no export is read | May still fail clearance. At k < 1, ORB and Vanguard base 1 go to 0 |
| C3. Smallest base gear | Every leg at its smallest non-zero base: Aegis 1, Striker `max_base` 1, Vanguard 1, ORB 1. Adds stay as in `BOOK_LEGS`, so a leg can reach about 3 contracts. **Resolved to a literal private vector before the freeze** | Same as C2 | Same as C2 | +1 | Lowest growth. Aegis may still fail granularity and go OFF. This is not the absolute minimum: smaller adds-OFF vectors exist (`AddsRule.OFF`), but they change each leg's trade structure |
| **M. Named ladder** | An explicit ordered set of literal vectors, fixed before any E_0 output. The clearing rung with the highest median growth in the ranking cell (§4) wins | #752 §C rank (tie-break (ii) restated on FULL); #783 `rank` | Score each vector in the set | +size of set (≤ 3); the losing rungs are disclosed | Best-of-n, disclosed |
| D. Searched grid | 4 legs × {0, 1/8, 1/4, 1/2, 1} = 5⁴ − 1 = 624 vectors, or a `SizeVector` lattice. k = 2 is dropped because `LegSize` refuses it | #783 grid machinery | Full search with Explore/Confirm | +624, registered before reads | Re-optimization in substance; a thin Confirm third. Not recommended |

**Recommendation for D3 (pending Joshua's ruling): M = {C3, C2}, each resolved to a literal private vector whose hash is recorded before the freeze. Joshua pins those literal vectors.**
- **No outcome is encoded.** Both rungs are rules over margin, ex-ante risk and dated snapshots, so neither depends on a growth, hit or MAE result.
- **Cleaner than sequential testing.** Testing C2 and then C3 after C2 fails is an adaptive best-of-2 anyway. Registering both up front states that honestly.
- **Consistent with Decision 4.** It satisfies "highest median growth among clearing candidates" without a search.
- **Ordering against T00.** Ratify D3 before Joshua or the coordinator opens the T00 step-3 result. A enters M only if Joshua rules both its private read and that ordering. If the result is opened first (for example because the Tradeify lane needs it), A is excluded and the exposure is recorded in the #733 §1a C-7 form.
- **Stopping rule.** If neither rung clears, the conclusion is "neither registered rung clears at E_0", and the next step returns to Joshua. No further vector is generated automatically. An adds-OFF or literal alternative would be a new option.
- **Alternative.** Joshua may instead pin literal per-leg values privately, with their hash recorded in the pre-registration.
- **Zero legs.** A leg below its minimum is set explicitly OFF (base 0), which matches the rail's convention. #752's structural-zero artifacts are not revived.

## 4. Personal clearance tests at E_0

**Evidence route (recommendation for D4; Joshua decides).** Use Route E only for legs whose trade set is provably invariant at the personal anchor, and use Route R or size-specific exports for the rest.

**Route E departs from two #752 rules:**
- §B ("size-specific exports, no linear rescaling", with capital scaled with k);
- F7's post-rescale ban.

D4 is therefore an explicit override of both for the legs it covers.

- **Method:**
  - Re-parse the four pinned normal-mode exports (pins at `run_four_firm_remc.py:47-54`). No new exports are made.
  - Apply the tuple per trade through the rail's sizing law.
  - Score with #783 and check margin with #782.
- **Trade-set invariance, per leg** (from the #752 Phase-0 classification; to be settled before the freeze):
  - **ORB:** no read of capital, equity or net profit, so the trade set is invariant. Route E applies, and adds are identified in the exports.
  - **Aegis:** the rail fixes the quantity. The Pine fixed-dollar rails are inert at the pinned `backtestMode` (#752 C2). Confirm that the initial-capital floor (`cap_floor_at_start`, `dd_basis`) cannot gate entries; if it cannot, Route E applies.
  - **Striker MYM:** the day soft-stop and `ddHit` are percentages of initial capital. The pinned MYM export is the cap100k body with its native guard active.
  - **Vanguard MGC:** size comes from `strategy.equity`, and maxDailyDD/maxTotalDD are percentages of day-start equity or initial capital.
  - **For Striker and Vanguard, path (a):** prove from the runtime port source and the reference export that every capital-dependent gate reads the port's configured capital, not live account equity. Then freeze that anchor as a tuple element. Under "reuse", the personal instance runs the same ports with the same effective inputs, so the anchor stays at the reference value and only rail quantities change. **Path (b):** if (a) fails, score the leg by Route R (a port replay under the personal profile, a build comparable to card #758, 5–7.5 days) or by size-specific exports per #752 §B.
- **Quantity bracket.** The exports do not carry Striker stop distances, so score a [floor, ceil] quantity bracket. Hits bind on ceil. Growth ranks on floor, and both ends are reported. The tuple's finite personal cap bounds ceil for capped trades.
- **Fidelity gate FG (before the run, and so before funding).** FG has two parts:
  1. per leg, the path-(a) proof or the path-(b) replay or exports;
  2. a test outside `lab/` (which keeps the lab↔ops boundary) showing that the adapter's per-trade quantities equal the rail's sizing law (`book_policy` `LegSize` and adds) at the frozen tuple on the same signals.

  **P-L3 is not this gate.** It is a synthetic three-way sizing-law check (LE2), and its card forbids parity over real exports at a non-identity size. P-L3 stays a later QUAL gate.

| Test | Standard | Documented | Built | To build |
|---|---|---|---|---|
| Drawdown | Daily: d = Σg − c·fees − D, l = −Σ\|MAE\| − c·fees − D, h = Σ\|MFE\|. D is any fixed cost debited that day (Fixed-costs row). Intraday peak = max(P, E+h). A hit is (peak − trough)/peak ≥ 0.15 and ends the path, like the live halt. Bootstrap: 10,000 paths × 13 non-circular 20-day blocks, H = 252, seeds 42, 123 and 2026 | ADR Decision 4; [#752 prereg §C](../briefs/pre-registration/Q-SFGROWTH-1-verdict-preregistration.md) (frozen baseline on main) | #783 `score`, `path_terminal`, `bootstrap_indices`, `summarize`. Builder tests only, on synthetic data, unverified | Size adapter; FG; runner; one calendar. Replace #783's literal `.15` with the tier constant, using #776's `round(dd, 6) >=` rule |
| Growth | Pooled `numpy.median` terminal equity at 252 days, net of debited fixed costs | §C | #783 `summarize`, `rank` | Funding test (private): (median terminal − E_0)/E_0 ≥ g\*. g\* = 12 × monthly cost ÷ E_0 (#774), counting only the costs **not** debited in the path, so no cost is counted twice. This is a funding test, not clearance |
| Fees (per side) | g = Net + Commission, applied once; reference slippage stays embedded. Fee-only stress c ∈ {1, 1.5} on Tradovate commission + exchange + clearing + NFA, per instrument | #752 F9 friction ruling (2026-10-10) | #783 `daily_series` (per leg, then summed) | A dated per-instrument snapshot for 6J, MYM, MGC and MNQ on a named Tradovate plan, kept in Q-SFCLEAR-1 and passed to #783 per leg. `Personal_Tradovate.cost_per_side_usd` is a scalar, so it stays unused for scoring; making it a mapping would be a #775-owner change. Do not reuse the four-firm depth bundle: it charges a flat micro rate on 6J and has no high channel |
| Fixed costs | Each fixed cost (API add-on, data entitlement, key balance, licence) is recorded as either debited from the personal trading account or paid elsewhere. Debited costs are dated periodic debits D in d and l at both c limbs, because the live halt observes account equity (#776 `observe`) | ADR Decision 4 ("after Tradovate costs") | — | A dated cost snapshot with the debit source of each cost (open fact 4) |
| Margin | Concurrent open quantity; entries processed before exits on ties; Σ per-leg peak × dated IM within the D7 limit; VOID is checked first | #752 F9 margin correction | #782 `check_concurrent_margin` (72 builder tests, unverified) | Export → `MarginFill` adapter with one tranche per add; an expected-fill inventory; a dated IM snapshot; the margin basis and limit (D7) |
| Granularity | Ex-ante one-contract risk ÷ (0.15·E_0) ≤ 20%, otherwise the leg is OFF (§3) | No repo source; operator heuristic | — | State the statistic, threshold and snapshot date in the pre-registration; compute from stop rules and the dated volatility snapshot |
| Windows and verdict cells | **Binding cells:** hits ≤ 100/10,000 on **each** seed, at c = 1 and at c = 1.5, in FULL, H1 and H2 (18 cells); and pooled median terminal > E_0 at c = 1.5 in FULL, H1 and H2. **Ranking cell:** FULL, c = 1, pooled seeds, floor bracket. Tie-break (ii) is restated on FULL trades. One calendar, fixed from all four pinned exports whatever a rung's OFF status, so every rung shares the same draws. Roll seams at ±10 weekdays are a sensitivity | §C uses Explore/Confirm, which this replaces; #733 `pass_floor_halves` precedent | #783 `common_calendar`, `outside_roll_seams` | A roll-date list. The verdict label is capped at "clears on exposed history (model-fitted)" |

**Open source facts to settle before the freeze.** Reading source carries no contamination risk. No values are quoted.
1. **Capital anchoring.** For each capital-dependent element of the Striker and Vanguard runtime ports (base, soft-stop, `ddHit`, maxDailyDD/maxTotalDD) and for Aegis's initial-capital floor, does it read a configured capital or live equity? (#752 F7.) This needs a private read in place, within AGENTS.md's read surface (the ports listed in `BOOK_SOURCES.sha256`). The answer decides path (a) or (b) for each leg.
2. How are ORB and Vanguard adds identified in the exports?
3. Three normal-mode exports live in `Downloads`. Re-hash them against their pins, then **copy** them (do not move: `run_four_firm_remc.py:42,47-54` pins the `Downloads` paths) into an ignored staging directory in the primary checkout, under an F6 manifest (D17). They must not go in a worktree.
4. Which fixed costs are debited from the personal trading account, and on what dates?

**Pre-registration comes before any candidate replay.**
- **Rule.** No export, replay or scoring at a personal vector runs before the successor pre-registration is frozen and ratified. Basis: [checklist item 7.6.1](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-10-01--first-session-simplification-rulings-six-cuts), #733 §R and the lesson that replaying a candidate before the freeze contaminates the pre-registration.
- **Allowed before the freeze:**
  - Pine and port source reads within the read surface;
  - rule-maximum quantity × dated IM arithmetic (no export reads);
  - ex-ante risk from stop rules and the dated volatility snapshot;
  - resolving C2 and C3 to literal vectors;
  - hashing;
  - adapter work on synthetic data.
- **K registration.** Register the ladder in [`discovery_manifests/t00_tradeify_book_lineage_2026_10_10.json`](../../discovery_manifests/t00_tradeify_book_lineage_2026_10_10.json) before any read. For M = {C3, C2}, K goes from 9 to 11. Disclose prior readers.
- **Exposure record.** See §3, "Ordering against T00".

**#752 re-scope: close it rather than amend it (Joshua decides as D2).**
- **Every constant changes.** The pre-registration's own Status says a changed constant means a new pre-registration, and here the question, pool, K, verdict rows, windows and evidence route all change.
- **The brief agrees.** Brief §5 says a new grid is a new pre-registration.
- **Standing practice agrees.** Brief-authoring Known Trap #12 says to close and reopen, and checklist item 7.6.1 set the precedent.
- **Nothing is lost.** Nothing has run, so closing loses no data and no K.

| Step | Owner |
|---|---|
| Close Q-SFGROWTH-1 as `operator-stopped` (superseded by 2026-10-11b) and close #752 unmerged. This lifts F8's HOLD. Its STATE/INDEX/CATALOG rows are not merged | Coordinator, after D2 |
| Cite the reusable text by `refs/pull/752/head` = `b02c173`: §C, F6, F7, F9, and the classification of legs 1–4 (C1–C4, C6, C7 and the reference-evidence table). Port the classification into the successor's directory | Coordinator |
| Successor pre-registration (provisional id **Q-SFCLEAR-1**). It contains: the pinned book; the literal ladder vectors or a literal tuple; the frozen capital anchors; the §4 constants and verdict cells; the fee, IM, volatility, fixed-cost and roll-date snapshots; the D4 override statement; and the K entry. It is frozen when Joshua ratifies it | Coordinator authors; Joshua ratifies |
| Drop K = 2,375, NAS leg 5, the structural-zero artifacts, the Explore/Confirm out-of-sample claim and F8. Fix the stale "#778 pending merge" text | Coordinator |

## 5. Reuse map (owners preserved)

| Item | Owner (unchanged) | Reused as | Needs under this plan |
|---|---|---|---|
| #782 F9 margin | Codex cloud builder | Margin primitive with no pool assumptions | Retarget "B4 for #752" to Q-SFCLEAR-1; independent verification; merge (its CI pytest was still pending when read); export → `MarginFill` adapter; `equity_limit` per D7 |
| #783 acceptance | Codex cloud builder; the verifier seat is still to be named | Statistic, fees, calendar, bootstrap and manifest checks | Re-pin from `#752 b02c173e` to Q-SFCLEAR-1. Retire the search-only parts: `MULTIPLIERS`, `nominal_grid`, the F2 zero schema, the F8 `POOL_CASE` and its test, and the Confirm-top-only `verdict`. Keep `rank` for the ladder, with tie-break (ii) on FULL. Add per-leg fee rates and periodic fixed-cost debits. Replace the 6 F9 stubs with #782. Resolve the 18 skips against the four-leg pool. Independent verification before use |
| #775 tier | CC worker under #779; the coordinator dispatches; the merge sequencer merges | Tier, fail-closed private E_0 loader, preflight refusal | Joshua writes the private overlay (an operator act). Re-own the "Q-SFGROWTH-1" pointers. `micro_contract_cap` takes the tuple's finite personal cap. `cost_per_side_usd` stays unused for scoring (§4). Needs D10 (item 2's re-MC) |
| #776 15% halt | Same as #775 | Live halt module, unchanged. It observes fixed-cost debits, which the clearance now models | P4 wiring: an intraday equity source, a flatten executor, and routing `HaltStateError` into `book_halt`. Peak initialisation (D16). `portfolio_id` from #777 v2 |
| #777 binding | Same as #775 | A separate listener instance | Schema v2 with a portfolio/sizing-tuple identity; a daemon and book-route overlay. Fix the docstring, which overclaims: the code only intersects instance keys. `activation_ready` stays False until items 3–4 |
| #779 card | Deployment Coordinator | Build order for items 2, 6 and 7, then P4 | Point §1/§4 at Q-SFCLEAR-1. P4 is now unblocked (#780 merged), but it must build on `2cfb3d7` or later and preserve `sources_healthy` and `held_unhealthy`. Add the P-OES packet. Record the `book_account_owner.py` writer order (§7). Reconcile `no_tradeify_binding_change` with the safeguard's reads. The card forbids `book_policy.py`, so row 2.2 is its own card |
| #773 P-L1, P-L2, P-L3, P-L4, R-SV, P-L5 | Per the #773 cards. Packets that touch sizing are CC solo, never GLM (#773 §5) | Live size-vector seam, owner binding, synthetic three-way sizing-law check (LE2), interlock seam, stamped vector on the live route, records chain | Dispatch timing for the personal lane is a Joshua re-ruling of #773 Q6/G-3 (D20). The personal root hash is Q-SFCLEAR-1's frozen tuple hash. P-L4 needs a personal GO field |
| #770 licensing, #774 economics | Existing note owners | CME category (A8 recommended) and Tradovate costs; the g\* hurdle and "fund only after a lane clears" | Answers are still outstanding. Personal funding checkpoint per #774 §6 (D15) |
| #780 (merged `2cfb3d7`) | Protection-health worker | The unhealthy-source hold for protection amends | P4 must preserve its routing |

## 6. §6.7 opposing-exposure safeguard and §6.6 residual

**Facts.**
- **Canonical record.** `ops/prop_envelope_default.md` §4a (re-verified 2026-10-02 against article 10495868, dated 2026-08-19) places MYM and MNQ in Equity Index, MGC in Metals and 6J in Currencies. It lists no micro-yen product.
  - **Cross-group link.** Volatility is cross-linked to Equity Index: long Equity Index with long FVS is treated as offsetting.
  - **Not exhaustive.** The list is explicitly not exhaustive.
  - **No threshold.** No threshold is published for cross-account or correlated-product hedging.
- **One direction per group.** 6J is SELL; MYM, MGC and MNQ are BUY (`book_policy.py:181-198`). On the signal path, the book therefore cannot oppose itself within Equity Index, and it holds no Volatility leg.
- **Sizing cannot reverse a leg.** The size vector has no side field.
- **Stale comments.** Two comments still describe c1 as long-only (`c1_rail_listener.py:146`, `core/firm_rules.py:255-261`). Route the fix by seat.

**Residual paths that direction-by-construction does not cover:**
- **Broker-side reversal or overfill:**
  - a duplicate close (`order_id` idempotency is DISPROVEN);
  - a close racing a protective stop;
  - an orphaned protective order;
  - Tradeify's auto-close racing a rail flatten.
- **Operator or agent orders:** the weekly preservation trade, drills, the M1 MYM test leg, and Joshua's own manual trades.
- **Wrong-account routing.**
- **Leg drift:** micro yen is unmapped, later strategies could add new sides or Volatility exposure, and the two instances run different images.
- **Re-mapping:** Tradeify can change its groups, effective on posting.
- **Other External Accounts** Joshua controls, at any broker or prop firm.

**Design premise.** No cross-account tolerance exists, and Tradeify's list is not exhaustive. An unmapped product, or an unknown offset relationship, therefore fails closed.

**Invariant.** The rule covers every Product Group and every cross-group offset pair under the mapping in effect, across every account Joshua controls and within any one account. Confirmed positions plus the potential exposure of working orders must never form an offsetting combination: opposite sides in one group, or a pair the mapping marks as offsetting (for example long Equity Index with long FVS). The same holds within one product across contract months.

| Layer | Behaviour | Placement |
|---|---|---|
| L0 static | At activation and at arm, take the union of the leg tables **resolved from each instance's deployed image and config identity**, not from the source tree's `BOOK_LEGS`, because the instances run different H. Every product must be mapped, every group must carry one direction, and no cross-group offset pair may be present. The mapping file's hash and date must be valid | #777 `validate`/`activation_ready` and the `c1_rail_arm.py` interlock |
| L1 pre-send | A risk-add is refused unless the group's state (and that of any linked offset group) is fresh and shows no opposing position or working order in any account. Exits are reduce-only, capped at the broker-confirmed quantity in that account | The account owner's dispatch path, after the side check (`book_account_owner.py:1772-1777`), for entry/add `OrderIntent`s. The `sources_healthy` hold (`held_unhealthy`, `book_protection_owner.py:496-498`) covers protection amends only |
| L2 monitor | Each instance reads only its own account, with its own credentials, on a fixed cadence and on every fill, and publishes a signed inventory snapshot with broker-reported side. A comparator that holds **no** credentials compares the snapshots and publishes a signed verdict. Each instance pulls that verdict and enforces it. On opposition, or on a net position against a leg's entry side, each instance writes a durable halt of risk-adds and the operator is paged. There is no automatic resume | A separate comparator component. It keeps #777's no-shared-credentials rule, and no component holds another account's credentials |

**Rules common to all layers:**
- **Bad data.** A stale, incomplete or out-of-sequence inventory blocks risk-adds on both accounts; exits stay open.
- **Unknown orders.** A working order that no rail owns counts as possible exposure and blocks.
- **Restart.** Nothing is released until both inventories are fresh and the mapping hash verifies.
- **Evidence.** Every decision goes to the EventLedger with its `as_of` values and mapping hash, which supports a §6.7(g) records request.

**Remediation (pre-authorized; attended sessions only; Joshua sets the time bound in D11).**
- **Who acts.** Joshua, or an agent at his direction. AGENTS.md lets agents exit positions when the operator directs.
- **Which position.** First, the position that does not match its leg's entry side. If both positions match their legs, the personal account's position in that group.
- **Primitive.** The route's reduce-only close, capped at the broker-confirmed quantity.
- **Time bound.** Recommended: within 5 minutes of the page and before the session ends.
- **Afterwards.** The halt stays in place on both accounts until the operator resumes.

**Mapping source.** The canonical record is §4a, with a machine-readable file linked from it (configuration as code: defined once, not copied). The file holds:
- the groups and the cross-group offset pairs;
- the URL of article 10495868;
- the article's updated date;
- the retrieval date;
- a content hash;
- a reference to Tradeify's or Joshua's confirmation.

Joshua re-verifies it before each armed session. Agent fetches of help.tradeify.co meet Cloudflare 403 responses, and those are not bypassed.

**Tests.** These are adversarial: each layer is tested with the others mutated off.
- **L0:**
  - refuses a short Equity Index leg, a long 6J leg, an unmapped leg, and a long FVS leg alongside long Equity Index;
  - catches a leg-table difference between the deployed images.
- **L1:** refuses a cross-account opposing entry with the side check off.
- **Resting orders:** a resting opposite stop entry is refused.
- **Stale data:** a stale inventory blocks adds but lets exits through.
- **Flattens:** an over-sized or duplicated flatten is refused.
- **Races:** L2 detects a reversal from a close-vs-stop race; both instances halt and the operator is paged.
- **Orphans:** an orphaned protective order is flagged.
- **Restart:** a restart holds until both inventories are fresh.
- **Operator orders:**
  - a preservation trade opposite the other account's position is detected;
  - a Tradeify order inside the personal armed window is refused at the procedure gate.
- **Mapping:** a mapping change triggers re-evaluation, and an expired mapping blocks.
- **Routing:** a wrong-account exit is refused.
- **Credentials:** the comparator holds no order or read credentials.

**Blocker.** Phase 2 needs automated reads of Tradeify evaluation positions.
- Support says the Tradovate API covers live funded accounts only.
- Automated CrossTrade reads are not authorized beyond R-1/R-2. Those are operator-performed lookups of a known order, within the drill-plan scope (incident ADR §A11.1 item 4).

**Phasing (recommended; Joshua decides as D11 and D12).**
- **Phase 1 (Tradeify rail disarmed, today's posture): L0 plus symmetric time exclusion.**
  - **Exclusion.** Neither account may hold a position or working order in a mapped group while the other can.
  - **Personal side.** Every personal arm, drill row or manual order records evidence that the Tradeify account is flat, with no working orders, and that the Tradeify book is disarmed.
  - **Tradeify side.** Every Tradeify arm, weekly preservation trade (operator- or agent-placed), drill or manual order records the same evidence about the personal account and instance.
  - **Armed-window binding.** The personal attestation holds for the personal armed window only. No Tradeify order is placed inside that window, and the window closes with the disarm.
  - **Attestation method.** The attestation is Joshua's own platform observation of the Tradeify account's positions and working orders, recorded by the arm interlock with a hashed capture. R-1/R-2 cannot show that an account is flat. Using an account-inventory read instead needs a D11 ruling.
  - **No discretionary orders** on the personal account in any mapped group while the safeguard is in force, Joshua's manual trades included. Only the drills and the remediation it names are allowed.
  - **Preservation trades.** These are placed only while the personal instance is flat and disarmed. This is feasible because the legs are session-contained.
  - **Lane priority (D12).** While the Tradeify book is armed, or a Tradeify order procedure is open, the personal instance stays disarmed and flat.
  - **Personal account.** L1 and own-account L2 run on it, and working orders count.
- **Phase 2 (both books armed).** Full L1 and cross-account L2 must be accepted first, which needs the read-access ruling (D11).
- **Owner.** A new packet, **P-OES**, under #779 (coordinator). It is rail-bound, so it is CC solo. L0 can ride with P4.

**§6.6 residual.**
- **The ambiguity.** The same §6.6 bullet reportedly allows bot use "on the Trader's personal accounts", while also saying the bot is for the trader's own use within Tradeify and that multi-firm use is against policy.
- **Support's reply does not settle it.** The 2026-10-08 reply ("used only within Tradeify") did not address a personal brokerage account and reads like a template ([exclusive-use replies](./2026-10-10-tradeify-exclusive-use-replies.md)).
- **#784 needs two fixes before it merges:**
  - verify the §6.6 bullet verbatim and cite both halves;
  - keep copy-trading (§6.7(b)) and account-linking in item 5. ADR 10-09 item 5 and the option-c addendum name both, and "Item 5 now covers the §6.7 safeguard and the §6.6 residual" reads as dropping them.

**The written answer that would retire it.** It must come from Tradeify compliance or risk (an identified role, not the help desk), with the account referenced privately and the reply stored with hashes like #772. It should state:
1. Running Joshua's solely-owned bot and these four strategies in his own self-funded Tradovate account, alongside his Tradeify account, is permitted. That is, "multiple firms" means prop or funded programs only.
2. Same-direction orders there are not copying or mirroring under §6.7(b), the accounts are not "linked", and the similar-orders scan will not act on them.
3. The Product Group of any unlisted product (micro yen), and whether 6J and micro yen count as one product.
4. The signed set {short 6J, long MGC, long MYM, long MNQ} is not treated as offsetting under the non-exhaustive clause.
5. CrossTrade into the evaluation is a sanctioned tool under §1.3.
6. How each answer applies to evaluation, simulated-funded and live-funded accounts.

**Gate (existing ADR gate, not a decision).** Item 5 gates the first live order on the personal account, live-money drill rows included (ADR 10-09 Owed preamble). It closes only when all of the following hold:
- the safeguard for the phase in use is accepted;
- the mapping file is verified;
- §6.6 is answered in writing, or Joshua accepts the residual risk in writing;
- §6.7(b) copying/mirroring and account-linking are answered in writing, or Joshua accepts the residual risk in writing.

"Simultaneous operation" means either account can hold a position or working order while the other can. Phase 1 excludes it by construction, and it also requires Phase 2 to be accepted.

## 7. Live path to an attended armed personal session

The personal session sits downstream of most of the Tradeify book-route build: T09, TB-I3, the live route packet, T13 and T14. It also adds new personal items. The legacy single-leg path cannot trade the book (#773 scope note §1).

| # | Packet | Layer | Owner | Depends on |
|---|---|---|---|---|
| 0.1 | Ratify #784 (with the §6.6 and item-5 scope fixes) and rule D1–D20 | AUTH | Joshua | — |
| 0.2 | Send the external asks. **CME:** category A8/A9/A1; internal bars; non-professional device count; the Tradeify evaluation as a destination of the personal feed, including its effect on non-professional status. **Tradovate:** Q1–Q12; API order eligibility; whether read-only API scopes exist. **CrossTrade:** terms for a live personal account; read-only scopes. **Tradeify compliance:** the §6 asks | AUTH | Joshua | — |
| 1.1 | Settle the four open source facts. Close #752. Author and freeze Q-SFCLEAR-1, with literal ladder vectors, frozen anchors, and dated fee, IM, volatility, fixed-cost and roll-date snapshots | QUAL | Coordinator; Joshua ratifies | 0.1 |
| 1.2 | Adapters, #783 re-pin, #782 integration, Route R or sized exports for any path-(b) leg, independent verification | IMPL | Codex builder (#782/#783); path-(b) builds are dispatched by the coordinator; the coordinator names the verifier | 1.1 |
| 1.2b | FG fidelity gate (§4). Without FG PASS, neither 1.3 nor 1.4 proceeds | QUAL | Coordinator | 1.2 |
| 1.3 | Run the clearance **locally** by default. The Azure VM is used only under D18's per-run admission. Output: RESOLVED or not, with a frozen tuple hash | QUAL | Coordinator | 1.2b |
| 1.4 | Personal funding checkpoint: if RESOLVED and (median terminal − E_0)/E_0 ≥ g\* (compared privately), fund the API add-on, key balance, data entitlement and licence | AUTH | Joshua | 1.3, 0.2 |
| 2.1 | Merge #775, then #776 and #777 (retargeted to main) | IMPL | Existing owners; merge sequencer | — |
| 2.2 | Parameterize the book rail by tier and instance (`book_policy` `TIER`, cap and `require_policy`; settlement; account-close; `book_capacity`; the M1 Stage-1 contract), with a personal policy profile per D5. The Tradeify path stays byte-identical | IMPL | New card; CC solo, dispatched by the Deployment Coordinator; merge sequencer merges. Needs D19 (a D-B11 amendment) | After GC-5-DISPLACED merges (it shares `book_policy.py` and `book_capacity.py`), and after the Tradeify screen has consumed H′, or via an injection path that leaves `book_policy.py` untouched. Editing that file moves H′ and repeats P7 §7 step 1 |
| 2.3 | #777 v2: tuple identity plus a daemon/book-route overlay | IMPL | #777 owner | 2.1 |
| 2.4 | P4: arm refusal without halt state, entry gate, flatten executor, `HaltStateError` → `book_halt`, intraday equity source, and a live margin gate (personal capacity against IM; `book_capacity` enforces only the Tradeify cap) | IMPL | #779 card | 2.1, 2.2; `book_account_owner.py` queue |
| 2.5 | P-OES Phase 1 (§6): L0, L1, own-account L2, symmetric exclusion records, the remediation runbook | IMPL | #779 card; CC solo | 2.4; `book_account_owner.py` queue |
| 2.6 | #773 chain: P-L1 → P-L2 → P-L3 (the synthetic sizing-law check) → P-L4 with a personal GO field | IMPL + QUAL (P-L3) | #773 owners | D20, 1.3, 2.2; P-L2 in the `book_account_owner.py` queue |
| 2.7 | Define the personal deployment GO and monitoring acceptance; bake them into a per-instance image (TB-I3 D-3 = U) | AUTH + IMPL | Joshua (admission-ADR owner); TB-I3 card | 2.6 |
| 2.8 | Live route packet (R-A1/R-H/R-J, R-SV, D-SV-1), written instance-parameterized from the start | IMPL | Book-route owner | 2.6 |
| 2.9 | Order route: the T09 adapter (CrossTrade) or a direct Tradovate API equivalent (D13). Gates B–D come first | IMPL | T09 owner | 0.2 |
| 2.10 | T13 per instance: heartbeat, notifier, HB-L1/L2, Q7, route preflight, the Tradovate trade-desk fallback, and an actor inventory that includes broker margin liquidation | IMPL | T13 card | 2.9 |
| 3.1 | Feed: written CME and Tradovate answers (ADR items 3–4). These gate any feed activation, shadow included | AUTH | Joshua | 0.2 |
| 3.2 | Tradovate adapter against `BarSource` (#619) → shadow with emission disabled → T14 PASS under the frozen equivalence spec, including FEED-16 | IMPL + QUAL | T14 owner | 3.1, 1.4 |
| 4.1 | Combined acceptance of the disarmed candidate (T16-analogue): the tuple hash is equal end to end (clearance → GO → loader → owner stamp); image and config manifest; feed PASS; route drills; halt, margin and §6.7 tests; pin H. No live GO | QUAL | **Codex deployment coordinator** (unchanged owner; moving it would be a Joshua decision) | 2.1–2.10, 3.2, item 5 closed (§6 Gate) |

**`book_account_owner.py` has one writer at a time.** Basis: umbrella `:245` ("No two live packets share a file") and the GC-5 card §9 order, #628 → GC-5-DISPLACED → TB-I3 S2. P-L2, P4 and P-OES L1 join that queue after TB-I3 S2, in the order #779 records. Each is cut from `main` after its predecessor merges.

**Attended end-to-end qualification (after 4.1).** The Codex deployment coordinator accepts release evidence (T17-analogue). Joshua owns every GO.

| Step | Content | Layer |
|---|---|---|
| E1 | Facts: personal entitlements, the known-order definition, the actor inventory, and whether a Tradovate sim account can host the drills | QUAL |
| E2 | X-1…X-5-style commissioning drills, **on the Tradovate sim account by default**. Written CP-3 authorization before each row; each trace is reviewed before the next row | AUTH + QUAL |
| E3 | M1 for this instance per D14; book-route monitoring acceptance. If M1 evidence itself needs a live-money row, that needs an explicit Joshua ruling recorded with the M1 owner | QUAL + AUTH |
| E3b | Any live-money drill row is a live order on the personal account. It runs only after all seven ADR items are closed, M1 is `RESOLVED` for this instance and the live-spend GO is given | AUTH + QUAL |
| E4 | Rehearsal on the final candidate with synthetic inputs: halt trip, flatten, resume-GO refusal, restart without stale authority | QUAL |
| E5 | Pre-arm capture: account, flatness, working orders, fingerprint. Joshua's own platform observation that the Tradeify account is flat, with a hashed capture. Joshua's attestation listing every account he controls and its positions in mapped groups. The route authentication preflight | QUAL |
| E6 | Arming GO: the personal deployment GO is baked in; `--arm` with `armed_until`; activation acknowledgment; read back the stamped tuple hash after restart | AUTH |
| E7 | Deployment GO and a GO for one attended session; the live-spend GO is separate | AUTH |
| E8 | Session: the 15% halt is live; no Tradeify order inside the window; any incident ends automation for that session ([§A11.2](../adr/2026-09-17-bounded-platform-protection-incident-contract.md#a112--operator-ruling-no-same-session-restart-of-automation-after-an-incident-2026-09-27)); disarm before the absolute `armed_until` | — |
| E9 | Reconcile, then an explicit review before any further session. Every later session needs its own GO, and a resume after a halt needs a single-use resume GO (#776) | AUTH |

| Gate | Blocks | Holder |
|---|---|---|
| All seven ADR owed items | The first live order on the personal account, live-money drill rows included | Joshua |
| ADR item 1 (Q-SFCLEAR-1 RESOLVED, after FG PASS) | Capital authorization and funding | Joshua |
| ADR items 3–4 (Tradovate API, CME licence covering every destination) | Any feed activation, shadow included | Joshua |
| ADR item 5 (§6.7 safeguard for the phase, mapping, §6.6, §6.7(b) and account-linking) | 4.1; the first live personal order; simultaneous operation (which also needs Phase 2) | Joshua |
| M1 `RESOLVED` for this instance (D14) | Arming (`dry_run=false`); any live spend | Joshua |
| Personal deployment GO (baked into the image) | Arming, or a `dry_run=false` boot | Joshua |
| Live-spend GO | Any live order, drills included | Joshua |
| Per-session GO | Every armed session | Joshua |

## 8. Critical path and decisions

These are planning estimates in working days from the rulings, not commitments. How long the external answers take is unknown.

| Track | Estimate | On the critical path? |
|---|---|---|
| Q-SFCLEAR-1: source facts and freeze (2–3 days) → adapters, FG and verification (3–5 days; add 5–7.5 days if a path-(b) leg needs Route R) → run (under 1 day) → verdict | About 1.5–2.5 weeks, or 2.5–4 weeks with Route R | No, but it gates funding (1.4) and everything that needs the tuple hash |
| External answers. CME has not replied since 10-04; Tradovate's first reply was ambiguous and the follow-up is only acknowledged; the Tradeify compliance ask is new | Unknown | **Yes**: gates any feed and item 5 |
| Feed build after the answers (adapter, shadow, T14 PASS) | About 2–3 weeks | **Yes** |
| Order route (T09 or direct API), after gates B–D | 3–4 weeks or more | **Yes**: the longest IMPL pole |
| Rail parameterization, #777 v2, P4, P-OES Phase 1 | About 2–3 weeks; the start depends on H′ timing, GC-5-DISPLACED and the `book_account_owner.py` queue | Parallel |
| #773 chain, personal GO, live route packet | About 2–3 weeks | Parallel |
| T16-analogue, then the attended qualification | About 1 week, then 1–2 weeks | **Yes** |

**Earliest attended armed session, best case:** about 6–8 weeks after the rulings. It cannot come sooner than the external answers, the item-5 closure and T09 allow. If personal protection used the 1%/0.40 response map (D5 alternative), T07 EOD settlement and its post-11-01 DST repeat would also bind.

| # | Decision (Joshua) | Recommendation | Blocks |
|---|---|---|---|
| D1 | Ratify #784 | Yes, after two fixes: verify §6.6 verbatim and cite both halves; keep §6.7(b) copy-trading and account-linking in item 5. Optionally name F8's HOLD | Everything |
| D2 | #752 disposition | Close as `operator-stopped`, unmerged, which lifts F8's HOLD; cite `b02c173`; the coordinator opens Q-SFCLEAR-1 | 1.1 |
| D3 | Sizing | Ladder M = {C3, C2}, each resolved to a literal private vector with its hash recorded before the freeze, and pinned by you; or literal private values with their hash. Ratify before the T00 step-3 result is opened. A enters only if you rule its private read and that ordering; otherwise A is excluded and any exposure is recorded. Legs below their minimum are explicitly OFF | 1.1 |
| D4 | Evidence route | Route E per leg only where trade-set invariance is proven (path (a), anchor frozen in the tuple). This explicitly overrides #752 §B and F7's post-rescale ban for those legs. Path (b) (Route R or size-specific exports) applies otherwise. FG must PASS before the run. Hits bind on ceil; growth ranks on floor | 1.1 |
| D5 | Personal protection | Normal mode plus the 15% halt only. This keeps F7's normal-mode rule: no Tradeify overlay; native guards and soft-stops as captured; `backtestMode` at reference; no guard toggled. It does not keep F7's post-rescale ban for D4 legs. Record it as the (book, `Personal_Tradovate`) binding under the concept-not-constant ADR; it needs a personal policy profile in 2.2 | 1.1, 2.2 |
| D6 | Windows, cells and label | Hits bind on each seed at c = 1 and c = 1.5 in FULL, H1 and H2. Median > E_0 binds at c = 1.5 in FULL, H1 and H2. The ranking cell is FULL, c = 1, floor bracket, with tie-break (ii) on FULL. One shared calendar. Roll seams as a sensitivity. Label "clears on exposed history"; no Confirm claim | 1.1 |
| D7 | Margin basis | Exchange initial margin, with a limit of 0.85·E_0 so the book stays affordable at the halt boundary. C2 uses the rule-maximum concurrent quantity | 1.1 |
| D8 | Growth gate | Clearance as in D6, net of debited fixed costs. Funding needs (median terminal − E_0)/E_0 ≥ g\* in FULL at c = 1.5, with g\* counting only costs not debited in the path (compared privately) | 1.1, 1.4 |
| D9 | K and stopping rule | Extend the book lineage manifest (K 9 → 11 for M) and register before any read. Record the exposure if the T00 step-3 result is read before D3. The T00 card §8 stopping rule binds the Tradeify lane only | 1.1 |
| D10 | ADR item 2's "re-MC under that tier" | Q-SFCLEAR-1's scorer at E_0 under `Personal_Tradovate` discharges it; the preflight refuses this tier by design | #775's closure of item 2 |
| D11 | §6.7 safeguard and read access | Phase 1 is L0 plus symmetric time exclusion, with the attestation made as your own platform observation and a hashed capture. Alternatively, rule an account-inventory read scope beyond R-1/R-2. No discretionary personal orders in mapped groups. Set the remediation time bound (recommended 5 minutes, before session end). Rule separately whether automated own-account reads of the Tradeify evaluation are permitted; Phase 2 is unavailable until they are | 2.5; simultaneous operation |
| D12 | Lane priority | While the Tradeify book is armed, or a Tradeify order procedure is open, the personal instance stays disarmed and flat. (Item 5 already gates the first live personal order, so it is no longer a decision here) | 2.5; E5–E8 |
| D13 | Order route | CrossTrade, which inherits T09, the drills and the close semantics. Revisit if CrossTrade's personal-account terms fail | 2.9 |
| D14 | M1 per instance | It does not transfer. Personal evidence comes from sim drills (E2) and E3; live-money rows follow M1 `RESOLVED`. Add an instance and tier check to the validator | E3, E6 |
| D15 | Funding | A separate personal checkpoint after RESOLVED and g\*. The $700 rail-GO ceiling does not cover personal costs; set a personal ceiling at that checkpoint | 1.4 |
| D16 | Halt peak initialisation | Broker-reported equity at first arm, recorded; the clearance is still simulated at E_0 | 2.4 |
| D17 | F6 private-evidence authority | A scoped authorization covering every private artifact this plan creates: the export inventory and staged copies, pre-screen results, literal vectors, E_0-linked snapshots and run outputs. Staged in an ignored primary-checkout directory, never in a worktree | 1.1 |
| D18 | VM admission for 1.3 | Run locally. Use the VM only under a per-run admission naming the exact exports and the E_0 input (the existing VM admission covers only the T00 ports and `effective_inputs.json`) | 1.3 |
| D19 | D-B11 amendment for row 2.2 | Scope `require_policy` and the tier frame to accept one named personal profile. The Tradeify path stays byte-identical, and the D-B11 Tradeify instance is unchanged | 2.2 |
| D20 | #773 dispatch for the personal lane (Q6/G-3) | Personal-lane dispatch follows Q-SFCLEAR-1 RESOLVED, not the Tradeify screen GO, and a Tradeify NO-GO does not withdraw the personal-lane packets | 2.6 |

## Review disposition

| # | Finding | Lens | Severity | Disposition |
|---|---|---|---|---|
| 1 | D12 presented as optional; item 5 already gates the first live personal order | governance | P2 | Fixed: §6 Gate, §7 gate table; D12 slot reused for lane priority |
| 2 | Azure VM run implies an unadmitted private-data upload | governance | P2 | Fixed: 1.3 runs locally by default; D18 |
| 3 | R-1/R-2 stretched to a recurring flatness read | governance | P2 | Fixed: attestation is Joshua's platform observation with a hashed capture, or a D11 read-scope ruling |
| 4 | Combined acceptance reassigned from the Codex deployment coordinator | governance | P2 | Fixed: 4.1 and release evidence go to the Codex deployment coordinator; §1 Unchanged row |
| 5 | P4 and P-OES missing from the `book_account_owner.py` writer queue | governance | P2 | Fixed: §7 queue note; rows 2.4–2.6 |
| 6 | Row 2.2 changes D-B11 without a ruling, conflicts with GC-5-DISPLACED, has no owner | governance | P2 | Fixed: D19; sequenced after GC-5-DISPLACED; owner named |
| 7 | Route E reverses #752 §B and F7 without saying so | governance | P2 | Fixed: D4 states an explicit override; D5 says which parts of F7 it keeps |
| 8 | #773 dispatch re-gated without a D-item | governance | P3 | Fixed: D20 |
| 9 | "Joshua's ruling" labels read as rulings already made | governance | P3 | Fixed: Status and §3 relabelled |
| 10 | F8 HOLD lift attributed to 2026-10-11b | governance | P3 | Fixed: §1 table; lifted only by D2 closure, or by #784 naming it |
| 11 | Moving Downloads exports; D17 too narrow; Option A read outside the read surface | governance | P3 | Fixed: copy and stage; D17 widened; A needs a Joshua read ruling |
| 12 | Route E trade set is capital-dependent; bracket bounds only quantity; P-L3 cannot be the fallback trigger | stats | P1 | Fixed: per-leg invariance (path (a)/(b)), capital anchor added as a tuple element, FG before run and funding, ceil/floor split, finite cap |
| 13 | Fixed monthly costs excluded from the halt path; growth/g\* unit mismatch | stats | P2 | Fixed: Fixed-costs row, D in d/l, open fact 4, funding test restated as a rate |
| 14 | MAE granularity screen selects on the tested channel; vector unknown at ratification | stats | P2 | Fixed: ex-ante risk; rule-maximum margin; C2/C3 resolved to literal vectors before the freeze |
| 15 | Recording exposure does not remove T00 selection on Option A | stats | P2 | Fixed: D3 ratified before the T00 result, otherwise A excluded |
| 16 | C3 is not the minimum; k = 2 is not executable | stats | P3 | Fixed: C3 renamed and stopping conclusion reworded; D grid without k = 2 (624) |
| 17 | Verdict cells and ranking cell underspecified after dropping Explore/Confirm | stats | P3 | Fixed: binding cells, ranking cell, tie-break (ii) on FULL, one calendar (§4, D6) |
| 18 | Scalar `cost_per_side_usd` would recreate a flat rate | stats | P3 | Fixed: per-instrument rates in the snapshot; tier field unused for scoring |
| 19 | Live-money drill rows could precede item 5 closure | compliance | P1 | Fixed: item 5 is a dependency of 4.1 and of E3b; E2 runs on sim |
| 20 | Phase 1 exclusion is one-sided and checked once | compliance | P1 | Fixed: symmetric exclusion, armed-window binding, no discretionary orders, D12 lane priority |
| 21 | R-1/R-2 cannot show flatness | compliance | P2 | Fixed with #3; also applied at E5 |
| 22 | Cross-group link and non-exhaustive clause missing; mapping file duplicates §4a; ask 4 moot | compliance | P2 | Fixed: §4a canonical with a linked file; offset pairs in the invariant and L0; no-tolerance premise; ask 4 replaced by a signed-set confirmation |
| 23 | §6.7(b) copying and account-linking dropped from item 5 | compliance | P2 | Fixed: §6 Gate; #784 fix in D1 |
| 24 | Live-money drills before M1 `RESOLVED` | compliance | P2 | Fixed: sim by default; E3b after M1; any exception is an explicit Joshua ruling |
| 25 | L2 remediation undefined; a read-only component writes halts | compliance | P2 | Fixed: remediation runbook; signed-verdict pull with a credential-free comparator |
| 26 | L1 placed beside a protection-only hold | compliance | P3 | Fixed: placed after the account-owner side check (`:1772-1777`) |
| 27 | L0 reads the source `BOOK_LEGS`, not the deployed images | compliance | P3 | Fixed: per-image resolved leg tables |
| 28 | Other External Accounts not enumerated; read-only scopes unverified | compliance | P3 | Fixed: account-list attestation at E5 and arm; read-only scope asks in 0.2; L2 no longer relies on them |
| 29 | CME ask omits the Tradeify evaluation as a destination | compliance | P3 | Fixed: added to 0.2 |