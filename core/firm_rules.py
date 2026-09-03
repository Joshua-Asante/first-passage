"""
Firm rules as config. Add new firms by adding entries to FIRM_RULES dict.

PROVENANCE STATUS (2026-07-12, docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md;
updated 2026-07-30, docs/adr/2026-07-22-challenge-era-substrate-retirement.md Phase 4):
- FXIFY row + ``ACTIVE_FIRM`` + ``BASELINE_BALANCE`` **deleted** (Phase 4).
  Historical challenge semantics live in ``core/historical_challenge.py``
  (opt-in fixture only). Live c1 uses the explicit tier key
  ``Tradeify_Select_100K`` (rail JSON / ``generate_constants(tier)``).
- AUTOMATION_FRIENDLY_PROP_FIRMS (Bulenox, Tradeify, MyFundedFutures, BluSky) —
  **operational target** for the prop-portfolio program (discover → productionalize
  → execute). Challenge-pass re-MC + rail build remain separately gated.
- R6 locked-book fan-out stays NO-GO; these configs serve **new** prop-envelope
  portfolios, not redeploying the locked four-strategy book.

Onboarding any firm for live MC/ops requires an engine-support pre-flight, not
just a config entry. The pre-flight (core/mc/preflight.py, landed 2026-07-13)
threads tiers None-safely via ``firm_kwargs`` and surfaces the F1 headline bust
(daily+static+TRAILING, with a per-seed bucket-sum assertion). Still bespoke per
firm class: the engine branch each dd_type needs (bust_trailing, trailing_locking)
and the F2 fixed-$-vs-%-of-peak faithfulness caveat for the ``trailing`` firms.
Every prop tier must carry ``starting_balance`` — there is no $200K fallback.
"""

from historical_challenge import HISTORICAL_CHALLENGE_BASE_RISK

FIRM_RULES = {
    # Define when onboarding:
    # "FundedNext": { ... },
    # "The5ers": { ... },
    # "BrightFunded": { ... },

    # Bulenox futures-prop, Option 1 (real-time trailing drawdown, no daily
    # loss limit) — added 2026-07-01 for the futures-prop pivot (see CLAUDE.md
    # "Live-execution posture"). Read by lab remc harnesses that thread
    # dd_type/starting_balance/etc. into portfolio_mc's firm_kwargs. Requires
    # the 2026-07-01 bust_trailing engine support (core/portfolio_mc.py::
    # _simulate_path) — dd_type="trailing" is inert (KeyError-safe, but
    # silently ignored) on any pre-2026-07-01 checkout.
    #
    # Sources: bulenox.com/help/qualification-account/ (primary — confirms
    # no daily loss limit on Option 1 and no minimum trading days) and
    # bulenox.com/help/master-account/ (primary — the per-tier trailing-DD
    # dollar table below, which the page states carries over unchanged from
    # Qualification).
    #
    # MASTER-ACCOUNT DIFFERENCES — sourced 2026-07-01 sweep, completeness
    # gap closed 2026-08-23 (Q-FIRMEOD-1 closure + its R2 successor,
    # docs/notes/audits/2026-08-23-bulenox-lock-scope-resolution.md). Two
    # differences, not one:
    #   (1) "no reset option" (originally the only one captured here).
    #   (2) The Master Account Rules page ALSO states: "The trailing or EOD
    #       drawdown stops moving when the trailing or EOD drawdown reaches
    #       the initial starting balance +100." — a fixed +$100 lock offset,
    #       Tradeify-`dd_lock_offset_usd`-shaped. Both pages verbatim-confirm
    #       this lock is scoped to the MASTER stage (post-Qualification
    #       promotion): the Qualification Account page's own Option 1
    #       ("No Scaling Account (Trailing Drawdown)" — the exact geometry
    #       this dd_type="trailing" tier encodes) describes the floor as
    #       following the balance with NO lock language anywhere in that
    #       section; the +100 language only appears under Option 2 (EOD)
    #       prefixed "After Qualification, for Master Account:", and again
    #       on the Master Account page itself under "Master Account Rules".
    #       CONCLUSION (primary-source + engine-code grounded): the lock
    #       does NOT reach the horizon this engine currently simulates:
    #       simulate_path (core/mc/simulation.py) is absorbing at "pass" —
    #       it returns the instant the Qualification profit target is hit
    #       and never threads a post-pass/Master stage at all; firm_kwargs()
    #       (core/mc/preflight.py) never sets dd_lock_offset_usd for
    #       dd_type="trailing" tiers (that kwarg is trailing_locking-only,
    #       Tradeify/MFFU). No numeric field here changes as a result — this
    #       is a documentation-completeness fix only, not a reclassification.
    #       Re-classifying to dd_type="trailing_locking" is intentionally
    #       NOT done by this comment; it would require its own
    #       pre-registration -> re-derivation -> admitting ADR.
    # profit_target_pct/micro_contract_cap/cost_per_side_usd are from the
    # 2026-07-03 primary sweep (bulenox.com pricing + help + Rates.pdf
    # 2024-09-25 vintage) — see project_futures_prop_pivot memory,
    # 2026-07-03 session-2-final update. Rates.pdf re-verified byte-exact
    # 2026-07-13 (prop_envelope v1.0 research; still the Sept-2024 vintage).
    #
    # UNIT NOTE — RESOLVED per-side 2026-07-27 (was: "an arithmetically forced
    # inference, not primary-verbatim"). The PDF header still says only
    # 'ALL IN RATES' with no per-side/round-turn qualifier, so the unit is still
    # not primary-VERBATIM — but the forcing argument it rested on is now
    # verified against published pass-through, and it holds:
    #   Rates.pdf (re-fetched 2026-07-27 from
    #     bulenox.com/wa-data/public/site/data/bulenox.com/Rates.pdf,
    #     /Title "Rates", /Creator "Google Sheets", footer "Updated Sept/25/2024")
    #     prints MES/MNQ/M2K/MYM = 0.61, MGC/MCL = 0.76, M6A/M6B/M6E = 0.5,
    #     ES/NQ/RTY/EMD/YM = 2.09, 6J = 2.36 (still NO M6J row), and states
    #     "All in Rates includes Exchange & NFA fee, Order Routing fee,
    #     Commision fee" [sic].
    #   CME non-member exchange+clearing on those four micros = $0.35/side;
    #     NFA regulatory fee = $0.01/contract  => pass-through $0.36/side,
    #     $0.72 round turn.
    #   A ROUND-TURN reading of 0.61 would have Bulenox covering $0.72 of
    #     pass-through with $0.61 of revenue — negative before the routing and
    #     commission components its own footer says are included. Impossible.
    #   PER-SIDE leaves 0.61 - 0.36 = $0.25/side for routing + margin. Coherent.
    # => cost_per_side_usd IS per-side. Corpus cost verdicts do NOT halve.
    #
    # RESIDUAL STALENESS (direction is conservative, so not blocking): the PDF is
    # a Sept-2024 vintage and CME announced transaction-fee changes effective
    # 2026-04-01. If exchange fees rose while Bulenox's printed rate did not, the
    # true current per-side cost is >= 0.61, so hurdles computed from 0.61 are
    # mildly OPTIMISTIC, never pessimistic. Re-verify before lock-grade use.
    # E1 correction (2026-07-13): 15:59 CT = 16:59 ET YEAR-ROUND (CT/ET shift
    # together on US DST; the prior 'summer/winter ET split' was erroneous).
    # 40% payout consistency now PRIMARY-sourced (bulenox.com/help/master-account/,
    # 2026-07-13): checkpoint-at-withdrawal, blocks payout, never violates;
    # no eval-phase consistency. NO M6J row in Rates.pdf (full 6J $2.36 only). inactivity_max_idle_days was a
    # carried-over FXIFY placeholder through 2026-07-05; corrected 2026-07-06
    # (residual track R2) to Bulenox's actual rule (≥1 trade per 5 trading
    # days, confirmed in the same 2026-07-03 sweep) — NOTE this counts
    # calendar trading days idle, not the FXIFY-style consecutive-bday
    # counter verbatim; the engine's existing INACTIVITY_LIMIT semantic
    # (consecutive zero-P&L bdays) is the intended encoding pending a
    # scheduled token-micro-trade mitigation at the execution layer (still
    # owed — see futures_residual_program_2026-07-05.md R8).
    "Bulenox_25K": {
        "dd_type": "trailing",
        "starting_balance": 25_000,
        "max_dd_pct": 6.0,          # $1,500 trailing DD / $25,000
        "daily_loss_pct": None,     # Option 1: no daily loss limit
        "profit_target_pct": 6.0,
        "min_trading_days": 0,
        "weekend_holds": False,     # Bulenox force-flattens EOD; no overnight/weekend carry
        "inactivity_max_idle_days": 5,
        "micro_contract_cap": 30,   # Bulenox Option 1 micro-contract cap, this tier
        "cost_per_side_usd": 0.61,  # all-in commission, $/contract/side (MNQ/MYM; MGC=$0.76)
    },
    "Bulenox_50K": {
        "dd_type": "trailing",
        "starting_balance": 50_000,
        "max_dd_pct": 5.0,          # $2,500 trailing DD / $50,000
        "daily_loss_pct": None,
        "profit_target_pct": 6.0,
        "min_trading_days": 0,
        "weekend_holds": False,
        "inactivity_max_idle_days": 5,
        "micro_contract_cap": 70,
        "cost_per_side_usd": 0.61,
    },
    "Bulenox_100K": {
        "dd_type": "trailing",
        "starting_balance": 100_000,
        "max_dd_pct": 3.0,          # $3,000 trailing DD / $100,000
        "daily_loss_pct": None,
        "profit_target_pct": 6.0,
        "min_trading_days": 0,
        "weekend_holds": False,
        "inactivity_max_idle_days": 5,
        "micro_contract_cap": 120,
        "cost_per_side_usd": 0.61,
    },
    "Bulenox_150K": {
        "dd_type": "trailing",
        "starting_balance": 150_000,
        "max_dd_pct": 3.0,          # $4,500 trailing DD / $150,000
        "daily_loss_pct": None,
        "profit_target_pct": 6.0,
        "min_trading_days": 0,
        "weekend_holds": False,
        "inactivity_max_idle_days": 5,
        "micro_contract_cap": 150,
        "cost_per_side_usd": 0.61,
    },
    "Bulenox_250K": {
        "dd_type": "trailing",
        "starting_balance": 250_000,
        "max_dd_pct": 2.2,          # $5,500 trailing DD / $250,000
        "daily_loss_pct": None,
        "profit_target_pct": 6.0,
        "min_trading_days": 0,
        "weekend_holds": False,
        "inactivity_max_idle_days": 5,
        "micro_contract_cap": 250,
        "cost_per_side_usd": 0.61,
    },

    # Tradeify "Select Flex" futures-prop — added 2026-07-10 for the firm
    # re-selection off Bulenox (barrier-geometry + own-account-scaling grounds;
    # CC-HANDOFF-tradeify-target-firm.md + §1 ADDENDUM). NOT the ACTIVE_FIRM;
    # read only by lab/analysis/tradeify_selectflex_remc_2026-07-10/. Requires
    # the 2026-07-10 dd_type="trailing_locking" engine support in
    # core/portfolio_mc.py::_simulate_path (inert / KeyError-safe on any
    # pre-2026-07-10 checkout, same soft-degrade contract the Bulenox
    # dd_type="trailing" tiers rely on).
    #
    # dd_type="trailing_locking" — the geometric fix that motivated the switch.
    # The end-of-day trailing floor ratchets UP on EOD balance (never intraday,
    # never down) as a FIXED-DOLLAR cushion below the running EOD peak, then
    # FREEZES permanently at (starting_balance + dd_lock_offset_usd) once the
    # EOD balance first clears max_dd by dd_lock_offset_usd (or on first payout
    # request, whichever first). Worked example (50K, $2,000 DD, $100 lock):
    # floor = peak - $2,000 until EOD balance hits $52,100, then floor freezes
    # at $50,100 forever. This is materially different from the Bulenox tiers'
    # dd_type="trailing" (which never locks) AND from FXIFY's dd_type="static"
    # (floor never moves).
    #
    # CRITICAL — the cushion is FIXED-DOLLAR, not %-of-peak. The "$100 lock"
    # only has meaning in dollar terms; modeling the pre-lock trail as
    # %-of-peak (what the shipped Bulenox `trailing` branch does) cannot
    # express a fixed-dollar lock and would mis-place the freeze point. The
    # engine's trailing_locking branch therefore reads max_dd as a constant
    # dollar amount = max_dd_pct/100 * starting_balance (exact for these clean
    # 4%/4%/3%/3% ratios: $1,000/$2,000/$3,000/$4,500) and caps the trailing
    # floor at starting_balance + dd_lock_offset_usd via min().
    #
    # CRITICAL — use the SELECT drawdown column, NOT Growth. Select is
    # $1,000/$2,000/$3,000/$4,500 (25K/50K/100K/150K); Growth diverges at
    # 100K/150K ($3,500/$5,000). max_dd_pct below encodes the Select column.
    #
    # daily_loss_pct=None: Flex has no daily loss limit (Select *Daily* differs).
    # min_trading_days=3: forced by the 40%-consistency eval rule (cannot pass
    #   in 1-2 days); consistency itself is eval-only and is modeled as an
    #   optional pass-gate in the re-MC harness (Run 2), not here.
    # weekend_holds=False: NinjaTrader 8 / Rithmic force-flat by 4:59pm ET.
    # inactivity_max_idle_days: VENUE FACT (help.tradeify.co article 10468318,
    #   re-verified 2026-07-30) — >=1 trade per Mon-Fri week on funded AND
    #   evaluation accounts (per account). NOT a harness assumption.
    #   ENFORCEMENT CORRECTED 2026-08-02 — the prior "soft-edged in enforcement"
    #   note was wrong. Article 10468318 states only the status change ("marked
    #   as inactive") and the procedure ("we will message you before we take any
    #   action"), never the action. Article 12268494 (Common FAQs) states it:
    #   "If inactive, your account will be deleted after an email warning" and
    #   "Accounts removed due to inactivity cannot be reactivated". Consequence
    #   is IRREVERSIBLE ACCOUNT DELETION, non-refundable; there is also no paused
    #   state ("Accounts cannot be paused or put on hold for any reason"). Owner
    #   of record: docs/notes/rail_build/TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md
    #   section 2a. A parked account still needs a weekly token trade.
    #   This is still NOT modeled as a pass/bust absorbing barrier (a ~5s token
    #   trade satisfies it), so the re-MC disables the inactivity termination
    #   rather than modeling it — modeling choice, not a claim the rule is
    #   optional. That choice is now PRICED: lab/analysis/c1/c1_cadence_inactivity_
    #   2026-08-02 measures the barrier ON at 92.6-97.6% path death, and the
    #   mitigation it assumes is undelivered at the execution layer (residual
    #   track R8, still owed). Value 5 unchanged; no constant moved by this note.
    #   ⚠ UNIT SEMANTICS (2026-09-03) — 5 is a BOUND, not the rule. The venue rule
    #   is a per-Mon-Fri-week BUCKET (">=1 trade per week"); simulation.py:171-178
    #   counts ROLLING consecutive idle business days. Those differ: a calendar
    #   trading Mon-wk1 / Fri-wk2 / Mon-wk3 / Fri-wk4 satisfies the venue in every
    #   week yet returns bust_inactivity on day 6 (measured against this engine
    #   2026-09-03) — it over-fires. On a COMPLETE business-day calendar it cannot
    #   miss a real breach (5 idle bdays inside one Mon-Fri week is necessarily 5
    #   consecutive), so barrier-ON figures are conservative CEILINGS there. ⚠ That
    #   precondition is NOT enforced: a sparse, trade-days-only input series has its
    #   idle days dropped before simulate_path ever sees them, and the engine then
    #   UNDER-fires (see the core/mc/preflight.py INACTIVITY_OFF block for the
    #   measured demonstration and the two functions responsible).
    #   This is the same calendar-vs-bday care the BluSky block below applies to
    #   its "30 consecutive days" clause, extended to the rolling-vs-bucket axis it
    #   did not cover. 5 is retained deliberately as the conservative bound; making
    #   the engine bucket-aware is unspent work needing its own ADR + re-MC. The
    #   only faithful implementation of the bucket rule is the report-only
    #   ops/sentinel/activity_week.py. Value 5 unchanged; no constant moved.
    # micro_contract_cap: EVAL micro-contract cap per tier (1/10, 4/40, 8/80,
    #   12/120 mini/micro -> micro caps 10/40/80/120). Funded Select scales
    #   progressively from a reduced base on EOD-equity triggers. Used only by a
    #   lock-grade integer re-MC; the %-of-equity geometry run does not read it.
    #   CORRECTED 2026-07-22: the 25K row read 20 (2 mini) against a published
    #   "Maximum Contracts: 1 mini / 10 micro" (article 12853921, re-verified
    #   2026-07-22). 50K/100K/150K matched and are untouched. No test pinned the
    #   25K value; the c1 account is the 100K tier, so no live surface moves.
    #   ACCOUNT-AGGREGATE, NOT PER-INSTRUMENT (verified 2026-07-22, article
    #   12268167 "Maximum Contract Limits" + 10495868): "Your combined position
    #   must stay within your account's contract limit, counted at [10 micros =
    #   1 mini]." A multi-leg book on ONE account shares this single cap -- it is
    #   NOT a per-instrument allowance. The c1 sizing host therefore allocates
    #   this cap across its legs (ops/c1_rail/c1_sizing_host_reference.py LEG_MAP
    #   `cap_alloc`); it must never hand the full cap to each leg.
    # Source: Tradeify Help Center (help.tradeify.co) + Funded Trader Agreement,
    #   verified 2026-07-10 (§1 ADDENDUM). Prop rules change frequently — re-verify
    #   the drawdown and target columns before any lock-grade use.
    # cost_per_side_usd + consistency_rule_pct added 2026-07-13 (prop_envelope v1.0
    #   ratification research, adversarially verified; ADR
    #   2026-07-13-prop-envelope-v1-ratification):
    #   - Commissions: help.tradeify.co/en/articles/10468315 publishes ROUND-TRIP
    #     all-in ($1.82 MNQ/MYM/MES/M2K; $2.12 MGC/MCL; $1.60 M6E/M6A) -> per-side
    #     = RT/2 = $0.91 (index micros; MGC $1.06). Platform-uniform
    #     (Tradovate/Rithmic/WealthCharts — articles 10468315 + 14369021).
    #     NO M6J (micro FX = M6A + M6E only; full 6J $3.10/side) — article 10468222.
    #   - Consistency: 40% Select EVAL ONLY, soft at-pass gate (cannot pass until
    #     best day <= 40% of total profit; forces min_trading_days=3; big day
    #     DELAYS pass, never breaches); removed entirely in funded (Flex/Daily).
    #     Articles 10468320 + 12853921, verified 2026-07-13.
    #
    # RE-VERIFICATION PASS 2026-07-22 (articles 10495876 + 10495868 + 10468222 +
    # 10495897 + 12853921 + 12268167, all read that day). Deltas vs the 07-13
    # encoding:
    #   - FLAT DEADLINE is now 16:45 ET regular (was 16:59); 12:59 ET
    #     holiday-short unchanged; auto-flatten still explicitly NON-FATAL. No
    #     field models it -- documentation-only (ops/prop_envelope_default.md).
    #   - HEDGING / CORRELATED PRODUCTS (article 10495868): opposing directions
    #     within a Product Group are prohibited, in ONE account or ACROSS
    #     accounts. The Equity Index group is ES/MES/NQ/MNQ/YM/MYM/RTY/M2K/EMD/
    #     NKD + EUREX index -- so the c1 book's MYM and MNQ legs share a group.
    #     c1 is compliant BY CONSTRUCTION (both venue editions are structurally
    #     long-only: zero `strategy.short`; ops/c1_rail/c1_rail_listener.py `_leg_action`
    #     hard-codes "buy"; exits use closeposition). Long+long is explicitly
    #     ALLOWED. Consequences of a breach are severe (all involved accounts to
    #     violation status, profit forfeiture, possible permanent ban), so never
    #     add a short-capable Equity Index leg to this account or any account
    #     under the same control.
    #   - MINI+MICRO simultaneous holding is now ALLOWED (the standalone
    #     prohibition was withdrawn); combined position counts against the
    #     account cap at 10 micros = 1 mini.
    #   - US TREASURIES (ZB/ZN/ZF/ZT/UB) ARE NOT TRADABLE HERE (article
    #     10468222, article-dated 2026-05-20): supported exchanges are
    #     CME/COMEX/NYMEX/CBOT, but the CBOT products offered are YM/MYM +
    #     grains only. The sole rates products are EUREX bonds (FGBX/FGBS/
    #     FGBM/FGBL). Any Treasury candidate is venue-dead at this firm
    #     regardless of edge -- see docs/rejected_candidates.md (ORB-ZB-1).
    #
    # DEFECT FOUND 2026-07-22, APPLIED 2026-08-04 (ADR
    # docs/adr/2026-08-04-firm-rules-eval-lock-fix-applied.md; measurement
    # lab/analysis/tradeify_eval_lock_correction_2026-07-22/).
    # These rows model the EVALUATION phase (profit_target 6% = eval target;
    # min_trading_days 3 = forced by the eval-only consistency rule; eval micro
    # caps). `dd_lock_offset_usd` previously read `100`, encoding a mechanism
    # the eval phase does NOT have. Tradeify, verbatim (article 10495897,
    # article-dated 2026-06-18, re-verified 2026-07-22): "Q: Does drawdown lock
    # on Evaluation accounts? A: No. Drawdown only locks on Sim Funded
    # accounts. Evaluation accounts do not have drawdown locking."
    #   Direction of the old defect was OPTIMISTIC. simulation.py computes
    #   `floor = min(peak - max_dd_usd, starting_equity + dd_lock_offset_usd)`;
    #   the min() caps the floor's ascent. Real eval geometry has no cap, so the
    #   true floor is `peak - max_dd_usd` throughout. At the 100K tier the old
    #   ($100) lock engaged at EOD $103,100 while the eval passes at $106,000 --
    #   every simulated path crossed the lock region before passing, and over
    #   that stretch the modeled floor sat up to $2,900 BELOW the real one
    #   (~97% of the entire $3,000 DD).
    #   MEASURED 2026-07-22 (Tradeify_Select_100K, c1 book, frozen seeds/sims),
    #   RE-CONFIRMED AT HEAD 2026-08-04 (exact match, no drift):
    #   Run-1 bust 2.64% -> 3.98%; Run-2 bust 2.65% -> 4.74% (+2.10pp). Part A
    #   (<=3.0% ceiling) flips PASS -> FAIL. Baseline reproduced the published
    #   2026-07-15 figure (2.64% vs 2.65%), so the delta is trustworthy.
    #   The fix needed no engine change -- `trailing_locking` with an
    #   unreachable offset IS the pure fixed-$ trail (tests/core/
    #   test_trailing_locking_boundary.py uses dd_lock_offset_usd=1_000_000.0
    #   for exactly this). NOT None -- None makes the whole branch inert (no DD
    #   check at all). Every downstream harness (c1_band_rescore_2026-07-24,
    #   c1_cadence_inactivity_2026-08-02, this file's own correction study) had
    #   already been applying this exact value via runtime monkey-patch since
    #   07-22; this edit makes it the default so a fresh, undocumented
    #   invocation of the scoring CLI no longer silently inherits the old,
    #   optimistic geometry.
    #   RESIDUAL, NOT FIXED HERE: the breach is enforced INTRADAY but this
    #   engine tests only at EOD close (docs/superpowers/specs/
    #   2026-07-30-tradeify-native-fade-program-design.md section 3.2a) --
    #   every bust figure below remains a LOWER BOUND against the real venue.
    #   See the ADR section 6 for why that fix is scoped separately.
    #   2026-08-07 W1 (Accepted 2026-08-22): intraday-honest re-measure of the four
    #   decisions of record is AUTHORIZED at $0 — do not invent new bust %
    #   here; see docs/adr/2026-08-07-w1-intraday-honest-engine-remeasure.md.
    "Tradeify_Select_25K": {
        "dd_type": "trailing_locking",
        "starting_balance": 25_000,
        "max_dd_pct": 4.0,              # $1,000 EOD trailing DD / $25,000 (Select)
        "dd_lock_offset_usd": 1_000_000.0,  # unreachable -- eval has no lock (fixed 2026-08-04)
        "daily_loss_pct": None,         # Flex: no daily loss limit
        "profit_target_pct": 6.0,       # $1,500
        "min_trading_days": 3,
        "weekend_holds": False,
        "inactivity_max_idle_days": 5,  # VENUE FACT: >=1 trade/week eval+funded (art. 10468318); not absorbing
        "micro_contract_cap": 10,       # eval micro cap (1 mini / 10 micro)
        "cost_per_side_usd": 0.91,      # all-in, index micros (MNQ/MYM/MES; MGC=$1.06)
        "consistency_rule_pct": 40.0,   # Select eval-only soft at-pass gate; none funded
    },
    "Tradeify_Select_50K": {
        "dd_type": "trailing_locking",
        "starting_balance": 50_000,
        "max_dd_pct": 4.0,              # $2,000 EOD trailing DD / $50,000 (Select)
        "dd_lock_offset_usd": 1_000_000.0,  # unreachable -- eval has no lock (fixed 2026-08-04)
        "daily_loss_pct": None,
        "profit_target_pct": 6.0,       # $3,000
        "min_trading_days": 3,
        "weekend_holds": False,
        "inactivity_max_idle_days": 5,
        "micro_contract_cap": 40,       # eval micro cap (4 mini / 40 micro)
        "cost_per_side_usd": 0.91,
        "consistency_rule_pct": 40.0,
    },
    "Tradeify_Select_100K": {
        "dd_type": "trailing_locking",
        "starting_balance": 100_000,
        "max_dd_pct": 3.0,              # $3,000 EOD trailing DD / $100,000 (Select; Growth=$3,500)
        "dd_lock_offset_usd": 1_000_000.0,  # unreachable -- eval has no lock (fixed 2026-08-04)
        "daily_loss_pct": None,
        "profit_target_pct": 6.0,       # $6,000
        "min_trading_days": 3,
        "weekend_holds": False,
        "inactivity_max_idle_days": 5,  # VENUE FACT: >=1 trade/week eval+funded (art. 10468318); not absorbing
        "micro_contract_cap": 80,       # eval micro cap (8 mini / 80 micro)
        "cost_per_side_usd": 0.91,
        "consistency_rule_pct": 40.0,
    },
    "Tradeify_Select_150K": {
        "dd_type": "trailing_locking",
        "starting_balance": 150_000,
        "max_dd_pct": 3.0,              # $4,500 EOD trailing DD / $150,000 (Select; Growth=$5,000)
        "dd_lock_offset_usd": 1_000_000.0,  # unreachable -- eval has no lock (fixed 2026-08-04)
        "daily_loss_pct": None,
        "profit_target_pct": 6.0,       # $9,000
        "min_trading_days": 3,
        "weekend_holds": False,
        "inactivity_max_idle_days": 5,
        "micro_contract_cap": 120,      # eval micro cap (12 mini / 120 micro)
        "cost_per_side_usd": 0.91,
        "consistency_rule_pct": 40.0,
    },

    # Tradeify "Growth" EVALUATION tier -- added 2026-08-24.
    # PRIMARY SOURCE: help.tradeify.co art. 10495915 "Growth Evaluation Accounts",
    # article-dated 2026-06-05, read in-browser 2026-08-24. Rules table, $100k row,
    # verbatim: Profit Target $6,000 | Daily Loss Limit (Soft Breach) $2,500 |
    # Trailing Max Drawdown $3,500 | Max Position Size 8 Contracts (80 Micros).
    # Same article: min trading days "1 day (can pass immediately)"; consistency
    # "None"; "there is no time limit to complete a Growth Evaluation."
    #
    # WHY THIS ROW EXISTS: the 2026-08-23 shape feasibility map
    # (lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS.md Sec7) found the
    # $3,000 Select rope -- not the $6,000 target, not the 40% consistency rule
    # (which never binds: Select 40% and MFFU 50% scored bit-identically across
    # all 315 tuples) -- is the binding gate through most of the grid. Growth
    # carries the SAME $6,000 target on a $3,500 rope: +16.7% headroom on the one
    # constraint that actually binds. This row exists to measure that.
    #
    # (!) daily_loss_pct STAYS None. That is a modeling decision, not an oversight.
    #   Growth's DLL is a SOFT breach -- art. 10495915 verbatim: "If you hit this
    #   limit, trading is stopped for the day but your account is not failed."
    #   `simulate_path` has no representation for a lockout: its daily_loss_pct
    #   branch returns "bust_daily", a HARD fail (core/mc/simulation.py L137-140).
    #   Encoding 2.5 here would model a rule the venue does not have and fail
    #   paths Tradeify merely pauses. Modeling it as None instead OMITS the
    #   lockout, leaving the modeled daily left tail FATTER than the venue's (the
    #   venue truncates a losing day near -$2,500; the model does not). Direction
    #   is therefore PESSIMISTIC on the trailing rope. A Growth bust figure from
    #   this row is consequently an UPPER bound w.r.t. the missing lockout while
    #   remaining a LOWER bound w.r.t. the intraday clock (below) -- two-sided,
    #   not a point estimate. A faithful soft-DLL limb is an engine change and
    #   needs its own ADR + re-MC.
    #
    # (!) CLOCK: same two-clock geometry as Select -- the floor ratchets EOD, the
    #   breach is enforced intraday (art. 10495897, quoted verbatim in
    #   core/mc/simulation.py::simulate_path, read 2026-07-30). Art. 10495915's
    #   "intraday fluctuations won't affect the drawdown level" describes the
    #   floor's RATCHET, not the breach test, and does NOT license an EOD-only
    #   read -- see Q-FIRMEOD-1 (FALSIFIED) and the standing lower-bound rule in
    #   CLAUDE.md. Score this tier on the intraday-honest limb, same as Select.
    #   Re-verification of 10495897 for Growth specifically is OWED (the 2026-08-24
    #   in-browser pass could not reload it; relying on the dated 2026-07-30 read).
    #
    # Promoted into AUTOMATION_FRIENDLY_PROP_FIRMS["tradeify"] (below) by
    # operator GO 2026-08-24 (chat), ratifying
    # docs/adr/2026-08-24-tradeify-growth-tier-scoring-only.md. That dict is
    # the operational target set governed by ADR
    # 2026-07-12-prop-portfolio-four-friendly-firms (firm-level, not tier-level
    # -- Select's four tiers sit under it without a per-tier amendment).
    "Tradeify_Growth_100K": {
        "dd_type": "trailing_locking",  # fixed-$ EOD-ratcheting trail (NOT %-of-peak `trailing`)
        "starting_balance": 100_000,
        "max_dd_pct": 3.5,              # $3,500 trailing max DD / $100,000 (Select tier = $3,000)
        "dd_lock_offset_usd": 1_000_000.0,  # unreachable -- eval has no lock (art. 10495897)
        "daily_loss_pct": None,         # $2,500 SOFT breach; no engine representation -- see above
        "profit_target_pct": 6.0,       # $6,000 (identical to Select_100K)
        "min_trading_days": 1,          # "1 day (can pass immediately)" -- no consistency rule to force 3
        "weekend_holds": False,         # firm-wide 16:45 ET auto-flatten (prop_envelope, art. 10495876)
        "inactivity_max_idle_days": 5,  # firm-wide >=1 trade/week eval+funded (art. 10468318)
        "micro_contract_cap": 80,       # 8 mini / 80 micro (post-2025-09-12 purchases)
        "cost_per_side_usd": 0.91,
        "consistency_rule_pct": None,   # art. 10495915: "does NOT have a consistency requirement"
    },

    # MyFundedFutures "Rapid" eval tiers — added 2026-07-12 (ADR 2026-07-12-prop-portfolio).
    # Eval stage: EOD trailing MLL; funded/sim-funded switches to intraday trailing with
    # $100 lock (same trailing_locking semantic as Tradeify Select). Consistency 50% eval-only.
    #
    # SAME DEFECT AS THE TRADEIFY ROWS -- FOUND 2026-07-22, APPLIED 2026-08-04
    # (ADR docs/adr/2026-08-04-firm-rules-eval-lock-fix-applied.md).
    # The line directly above already said the $100 lock is a funded/sim-funded
    # mechanism -- but these EVAL rows carried `dd_lock_offset_usd: 100` anyway,
    # giving the eval sim a lock the eval phase does not have. Re-verified
    # 2026-07-22 (article 13286542, "Rapid Plan 100k"): the "Rapid Plan
    # Evaluation Stage Account Parameters" table lists only "Maximum Loss Limit
    # (EOD) $3,000" with NO lock; "Max Loss Lock at $100" appears solely under
    # "1. Sim Funded Account Parameters". Same optimistic direction as Tradeify.
    # MEASURED 2026-07-22: Run-2 bust 2.64% -> 4.25%; Part A flips PASS -> FAIL.
    # MFFU is the c1 FALLBACK tier, so this bites if that fork is ever taken.
    # Same fix as Tradeify: unreachable offset (1_000_000.0), not None. Same
    # unfixed residual too -- the intraday-vs-EOD breach-clock gap (see the
    # Tradeify block's comment above and the ADR section 6) is not addressed here.
    #
    # CONTRACT CAP -- MFFU publishes the consequence Tradeify leaves unstated
    # (article 13286542, verified 2026-07-22): "You may trade up to 8 minis
    # and/or 80 micros total. Exceeding a total of 8 minis or its equivalent in
    # micros (80 micros) can result in a BREACH of the trading account." This is
    # the firm-class evidence that an over-cap COMBINED position is a rule
    # breach, not merely a platform-rejected order -- load-bearing for the c1
    # per-leg-vs-account-aggregate cap allocation (see the Tradeify block above).
    # Source: help.myfundedfutures.com Rapid Plan articles 13134709 (50K), 13286542 (100K),
    #   verified 2026-07-12.
    # cost_per_side_usd added 2026-07-13 (prop_envelope v1.0 ratification research,
    #   adversarially verified): article 9735811 publishes 'Total Cost Round Trip'
    #   ($1.90 MNQ/MYM/MES; $2.20 MGC; $1.44 M6E) -> per-side = RT/2 = $0.95 (index
    #   micros; MGC $1.10, M6E $0.72). No platform attribution on the fee page.
    #   NO M6J anywhere on the instrument list (full 6J $2.56/side).
    #   Consistency semantics re-verified 2026-07-13 (article 11994562): 50%
    #   eval-only SOFT gate (exceeding never breaches; trade more days until
    #   best day <= target/2); none in sim-funded; none at payout. E1: 16:10 ET
    #   auto-liquidation ('4:10 PM EST', article 9558251); holiday half-days NO
    #   auto-liq (trader responsible); post-16:10 orders can disqualify.
    "MFFU_Rapid_50K": {
        "dd_type": "trailing_locking",
        "starting_balance": 50_000,
        "max_dd_pct": 4.0,              # $2,000 EOD MLL / $50,000 (eval)
        "dd_lock_offset_usd": 1_000_000.0,  # unreachable -- eval has no lock (fixed 2026-08-04)
        "daily_loss_pct": None,
        "profit_target_pct": 6.0,       # $3,000
        "min_trading_days": 2,
        "weekend_holds": False,
        "inactivity_max_idle_days": 5,  # >=1 trade/week; not modeled as absorbing barrier
        "micro_contract_cap": 50,       # 5 mini / 50 micro
        "consistency_rule_pct": 50.0,   # eval only; does not fail account, gates pass
        "news_trading": True,           # T1 allowed on Rapid eval
        "cost_per_side_usd": 0.95,      # all-in, index micros (MNQ/MYM/MES; MGC=$1.10)
    },
    "MFFU_Rapid_100K": {
        "dd_type": "trailing_locking",
        "starting_balance": 100_000,
        "max_dd_pct": 3.0,              # $3,000 EOD MLL / $100,000 (eval)
        "dd_lock_offset_usd": 1_000_000.0,  # unreachable -- eval has no lock (fixed 2026-08-04)
        "daily_loss_pct": None,
        "profit_target_pct": 6.0,       # $6,000
        "min_trading_days": 2,
        "weekend_holds": False,
        "inactivity_max_idle_days": 5,
        "micro_contract_cap": 80,       # 8 mini / 80 micro
        "consistency_rule_pct": 50.0,
        "news_trading": True,
        "cost_per_side_usd": 0.95,
    },

    # BluSky Trading "Premium" eval tiers — added 2026-07-12 (ADR 2026-07-12-prop-portfolio).
    # EOD trailing drawdown (minimum balance ratchets on EOD peak, never down).
    # 50K example: start $48K floor ($2,000 trail). Consistency 34% on Premium eval.
    # Source: help.blusky.pro evaluation-rules (12434059) + attention-prop-firm-traders
    #   automation FAQ (blusky.pro), verified 2026-07-12.
    # cost_per_side_usd added 2026-07-13 (prop_envelope v1.0 ratification research,
    #   adversarially verified): PLATFORM-DEPENDENT, encoded CONSERVATIVELY for the
    #   declared Option C path TV->listener->CrossTrade Cloud->Tradovate (NT8 Add-On
    #   dormant fallback) = NinjaTrader brokerage schedule as the NT-class proxy
    #   (BluSky 'Pricing set by brokerage' + linked ninjatrader_futures_commissions.pdf,
    #   Free-plan column: $0.95/side MNQ/MYM/MES; MGC $1.20; M6E $0.84 — per-side
    #   confirmed on ninjatrader.com/pricing). CHEAPER alternative exists: BluSky's
    #   own eval schedule on Rithmic/Volumetrica/Tradesea rails is a flat $0.50/side
    #   for ALL micros (article 12434069) — but that rail does not carry the Option C
    #   stack; re-encode if the rail decision changes. Funded-account pricing
    #   is 'set by brokerage' with no firm-published figures (NT PDF is the proxy).
    #
    #   FLAG 2026-08-05 (claim-alignment M40 / O-G — comment only, value unchanged):
    #   BluSky publishes $0.50/side micros at Evaluation on Rithmic/Volumetrica/
    #   Tradesea and no figure at all for funded. Encoded 0.95 is an NT-schedule
    #   proxy / confirmed open correction item awaiting operator direction — do NOT
    #   treat it as venue-published in any F3 EV/$ ranking.
    #   E1 re-verified 2026-07-13: auto-liquidate ~15m before close (best-effort,
    #   trader responsible; ~16:45 ET derived); no adjustments after 17:00 ET.
    #   Consistency 34% = Propel Premium/Static evals, SOFT (highest day re-scales
    #   target, never fails); Orbit none; 300K tier 21%.
    #
    # INACTIVITY RULE -- SOURCED 2026-08-05, UNIT-CORRECTED 30 -> 22.
    # (ADR docs/adr/2026-08-05b-blusky-inactivity-rule-sourced.md, superseding the
    # same-day containment ADR 2026-08-05-blusky-inactivity-unsourced-encoding.md.)
    #
    # HISTORY: this row previously carried 30 annotated "30-day eval subscription
    # renewal window" -- a BILLING cycle (art. 12434108: "The billing period of 30
    # calendar days will auto renew each period"). That annotation was right about
    # what it had sourced and wrong about what the field means: the 2026-07-12 sweep
    # read the Evaluations collection, which carries NO activity rule, and never
    # reached the Terms of Use.
    #
    # THE ACTUAL RULE (primary, read in-browser 2026-08-05):
    #  * Terms of Use art. 11490284 section 3.3 "Abandoned Accounts" (under section 3
    #    Refunds and Billing Policy) -- "Evaluation, BluLive, SimFunded, or brokerage
    #    accounts inactive for 30 consecutive days may be closed at our discretion."
    #    EVALUATION accounts are named explicitly, so it binds this tier.
    #  * Brokerage Funded Rules art. 12434442 defines what BluSky means by active --
    #    "place at least one trade every 30 days to keep the account active" -- i.e.
    #    inactivity is TRADE-based, not login- or billing-based. This is the article
    #    that disambiguates the ToU clause's undefined "inactive".
    #
    # UNIT CONVERSION (why 22, not 30). The clause says "30 consecutive days",
    # unqualified; BluSky writes "30 calendar days" when it means calendar (art.
    # 12434108), and an abandonment clause has no trading-day concept. The engine
    # counts consecutive idle BUSINESS days (core/mc/simulation.py:171-178), so a
    # literal 30 models ~42 calendar days -- ~40% too LENIENT. 22 idle bdays is the
    # threshold at which 30 calendar days has certainly elapsed (4 weeks + 2 days);
    # 21 is the tighter end of the bracket. Both measured, see below.
    #
    # MEASURED (lab/analysis/c1/f3_cadence_successor_venues_2026-08-05,
    # out/blusky_unit_sensitivity.{log,json}) on the locked Striker book:
    #   limit 30 bdays (old): INACT 0.52-1.40%
    #   limit 22 bdays (this): INACT 4.87-13.14%   <- ~10x the old encoding
    #   limit 21 bdays       : INACT 5.59-14.80%
    # Worst at the C2-on 0.50x rung (13.14%), i.e. exactly the WATCH-1 rung the c1
    # book would deploy at. Still 6-20x better than the 5-day venues (90.85-97.54%),
    # so BluSky remains a different cadence class -- but not the ~1% one.
    #
    # RESIDUAL, NOT CORRECTED HERE: the clause is DISCRETIONARY ("may be closed at
    # our discretion") and the funded article is warning-first ("charge a fee and
    # issue warnings, and possibly close"), whereas the engine barrier is absorbing
    # and certain. Direction is conservative -- real hazard <= modelled -- unlike
    # Tradeify's art. 12268494, which is mandatory deletion with no reactivation.
    # Do not "correct" this by loosening the limit; soft enforcement is not a
    # licence to assume non-enforcement.
    "BluSky_Premium_50K": {
        "dd_type": "trailing",
        "starting_balance": 50_000,
        "max_dd_pct": 4.0,              # $2,000 EOD trail → $48,000 initial floor
        "daily_loss_pct": None,         # eval: no standalone DLL in primary rules article
        "profit_target_pct": 6.0,       # $3,000 (6% standard Premium eval)
        "min_trading_days": 0,          # no minimum days; 34% consistency shapes pace
        "weekend_holds": False,         # auto-liquidate ~15m before CME close
        "inactivity_max_idle_days": 22, # ToU s3.3 "30 consecutive days" -> 22 idle BDAYS (see block above)
        "inactivity_rule_sourced": True,   # sourced 2026-08-05: ToU art. 11490284 s3.3 + art. 12434442
        "micro_contract_cap": 50,       # 5 mini / 50 micro (Orbit/Premium class)
        "consistency_rule_pct": 34.0,   # Premium eval; target adjusts on excess day
        "news_trading": True,
        "automation_attended": True,
        "cost_per_side_usd": 0.95,      # NT-schedule proxy (index micros; MGC=$1.20); NOT venue-published — see FLAG 2026-08-05 above; Rithmic-class eval publishes $0.50 flat
    },
    "BluSky_Premium_100K": {
        "dd_type": "trailing",
        "starting_balance": 100_000,
        "max_dd_pct": 3.0,              # $3,000 EOD trail
        "daily_loss_pct": None,
        "profit_target_pct": 6.0,       # $6,000
        "min_trading_days": 0,
        "weekend_holds": False,
        "inactivity_max_idle_days": 22, # ToU s3.3 "30 consecutive days" -> 22 idle BDAYS (see block above)
        "inactivity_rule_sourced": True,   # sourced 2026-08-05: ToU art. 11490284 s3.3 + art. 12434442
        "micro_contract_cap": 100,      # 10 mini / 100 micro
        "consistency_rule_pct": 34.0,
        "news_trading": True,
        "automation_attended": True,
        "cost_per_side_usd": 0.95,      # NT-schedule proxy (index micros; MGC=$1.20); NOT venue-published — see FLAG 2026-08-05 above; Rithmic-class eval publishes $0.50 flat
    },
}

# Operational target set — prop-portfolio program (ADR 2026-07-12-prop-portfolio-four-friendly-firms).
# Keys are stable family slugs; values list FIRM_RULES tier keys for challenge-pass / scaling reference.
AUTOMATION_FRIENDLY_PROP_FIRMS = {
    "bulenox": [
        "Bulenox_25K",
        "Bulenox_50K",
        "Bulenox_100K",
        "Bulenox_150K",
        "Bulenox_250K",
    ],
    "tradeify": [
        "Tradeify_Select_25K",
        "Tradeify_Select_50K",
        "Tradeify_Select_100K",
        "Tradeify_Select_150K",
        # Growth product line -- operator GO 2026-08-24 (chat), ratifying
        # docs/adr/2026-08-24-tradeify-growth-tier-scoring-only.md. Only the
        # $100K tier is defined (FIRM_RULES); add the 25K/50K/150K rows before
        # extending this list to them.
        "Tradeify_Growth_100K",
    ],
    "myfundedfutures": [
        "MFFU_Rapid_50K",
        "MFFU_Rapid_100K",
    ],
    "blusky": [
        "BluSky_Premium_50K",
        "BluSky_Premium_100K",
    ],
}

# Unified allocations — challenge phase = funded phase.
# Living source of truth for *deployable* risk %: this module (`_BASE_RISK`).
# The frozen 4-leg lock book (Guardian/Aegis included) lives on
# historical_challenge.HISTORICAL_CHALLENGE_BASE_RISK — Phase C 2026-08-23.
# Consumers: `dd_protection.BASE_RISK` (living display keys) and
# `mc.modes.ALLOCATIONS` (historical 4-leg book).
# Allocation rationale: docs/adr/2026-05-23-allocation-refresh-2.md (current lock ADR).
# (Prior Notion pointer 346…d1b8d5 = SUPERSEDED/archived 2026-04-17 brief.)
# Unified 2026-04-17; Guardian re-locked 0.30% → 0.34% on 2026-04-23 after
# Pepperstone-sourced CSVs (2022→2026) showed headroom under 1% bust + 5% p99 DD.
# Striker NAS100 v1 added 2026-05-07 at 0.40% (DXTrade contractValue=10
# broker-verified; 4-strategy MC anchor 97.88/0.22/4.55 already covers it).
# 2026-05-14 allocation refresh: DJ30 risk 1.00% → 0.75% (with Pine pyramid
# 350% → 500%); NAS100 0.40% → 0.45%. See docs/adr/2026-05-14-allocation-refresh.md.
# 2026-05-23 allocation refresh: DJ30 risk 0.75% → 0.70% (with Pine pyramid
# 500% → 750%); NAS100 0.45% → 0.37% (pyramid 1000% unchanged). Same v4.5/v1
# designations retained per the no-version-bump doctrine (2026-05-14 ADR §Open
# items 1+2, ratified 2026-05-23). See docs/adr/2026-05-23-allocation-refresh-2.md.
# RISK_TIERS / BASELINE_RISK (challenge|funded phase wrappers for the continuous-lot
# multiplier spine) were removed in substrate Phase 2 — ops/accounts.py retired;
# live sizing is c1 + dd_protection.BASE_RISK, not a $200K lot multiplier.
_LIVE_BASE_RISK_SLUGS = ("striker", "striker_nas100")
_BASE_RISK = {k: HISTORICAL_CHALLENGE_BASE_RISK[k] for k in _LIVE_BASE_RISK_SLUGS}

# Slug → Title-Case keys used by dd_protection.BASE_RISK / c1 LEG_MAP leg_key.
_BASE_RISK_DISPLAY_KEYS = {
    "striker": "Striker",
    "striker_nas100": "Striker NAS100",
}


def base_risk_display() -> dict[str, float]:
    """Locked allocations keyed for live sizing (`dd_protection.BASE_RISK`)."""
    return {_BASE_RISK_DISPLAY_KEYS[k]: v for k, v in _BASE_RISK.items()}
