# MNQTAPE-1 — large-trade aggressor imbalance on MNQ's own tape → same-session continuation: Design accepted, EXPLORATION authorized, CONFIRM spend still outstanding

**Status:** **Design GO given** — operator (Joshua), 2026-08-23, in chat: "Go ahead and give the MNQ
pre-reg a GO." **EXPLORATION GO also given** at the same time, read as covering the mechanically-free,
cache-reuse Stage-G step (§7 step 2) — no real dollars move at this step. **CONFIRM spend GO
(§8 item 3, ~$82 real dollars) is explicitly NOT given by this authorization** — per this document's
own §8/§9 language ("must not be inferred," "requested, not assumed... only after Stage-G promotes")
and [Rule 2 — budget before acting](../../methodology/inqhiori-canon.md), that remains a separate,
future ask, contingent on Stage-G promoting and a fresh cost re-estimate. No `pull` may fire off this
document alone; only the Stage-G cache-reuse computation is authorized as of this Status line.
**Route:** [Avenue A §6](../2026-07-24-avenue-a-microstructure-scoping.md) **Route B
(generate→confirm)**, per [ADR 2026-08-05](../../adr/2026-08-05-avenue-a-generate-confirm-route.md)
(`Accepted`, unreverted as of this freeze — re-verify the Status line before GO, §10). No admitted
survivor ties this cell, so Route A is unavailable; Route B is the only route this candidate can
travel.
**Campaign tag:** `MNQTAPE-1` (fresh — not a P4 sub-item, not a reuse of `MNQFLOW-1`/`OFCHAN`/
`R2AGRUN`/`R2VBUCK`/`R2FLOW`; see §6 for why a new tag is minted).
**Authored:** 2026-08-22 · Claude Code, at operator commission (drafting only — no data pulled, no
test run, per explicit instruction).
**Mechanism id (for `scripts/instrument_profiles.py cell`):** none of the registered MNQ cells
(`opening-range-breakout`, `intraday-momentum`, `opening-pressure`, `ict-liquidity`,
`order-flow-depth-imbalance`) name this construction. **Before GO, the operator or executing session
must run** `python scripts/instrument_profiles.py cell MNQ order-flow-depth-imbalance` (the nearest
registered id) **and** re-grep `discovery_manifests/` fresh (this freeze is not a substitute for that
door-check at execution time — see the standing lesson that a snapshot is never trusted).

---

## §0 — Rule-0 reads (this session, real anchors — verify unmoved before GO)

| Source | Anchor | Supplies |
|---|---|---|
| [`lab/analysis/harvest/six_lead_cf_2026-08-17/P4_ROUTEMEMO.md`](../../../lab/analysis/harvest/six_lead_cf_2026-08-17/P4_ROUTEMEMO.md) | `acc9dcd` | The named mechanism this candidate inherits: dealer delta/gamma-hedging rebalancing deferred toward end-of-day (Chinese options evidence, `W4280500240`); flagged "plausible, not demonstrated" for a CME transplant |
| [`P4_DRYRUN.md`](../../../lab/analysis/harvest/six_lead_cf_2026-08-17/P4_DRYRUN.md) | `9087597` | `NQ.OPT` complex-wide density: **367×** thinner than `NQ.FUT` (OOS era); establishes `tbbo` (not bare `trades`) as the coarsest schema that can classify aggressor side — a choice this pre-reg imports directly (§2) |
| [`p4_concentration_2026-08-20/RESULTS.md`](../../../lab/analysis/harvest/six_lead_cf_2026-08-17/p4_concentration_2026-08-20/RESULTS.md) | `9087597` | Narrowing to the theoretically-correct near-the-money/near-dated options slice makes density **worse** (~1,423×) — the finding that motivates abandoning the options-tape route entirely rather than refining it |
| [`docs/adr/2026-08-05-avenue-a-generate-confirm-route.md`](../../adr/2026-08-05-avenue-a-generate-confirm-route.md) | `027a729` | Route B is `Accepted`; scope explicitly covers `tbbo`/`trades`/`mbp-1`/`mbp-10`/`mbo` order-flow discovery on MNQ; §5 forbidden moves (K_intrinsic honesty, no ES→MNQ lead-lag, ≥5s horizon floor, no CONFIRM peek) |
| [`docs/briefs/2026-07-24-avenue-a-microstructure-scoping.md`](../2026-07-24-avenue-a-microstructure-scoping.md) | `027a729` | Qualifying-triple origin (depth-shape-or-equivalent, not fill-trivial, survivor-tie-or-Route-B); the standing rule this whole campaign exists to satisfy: **"don't buy explanatory data before a survivor justifies it"** |
| [`docs/briefs/2026-07-14-a4-flow-data-fork-scoping.md`](../2026-07-14-a4-flow-data-fork-scoping.md) | `027a729` | a4 kills **participant-category** splitting (net imbalance only, can't split who's trading) — does **not** reach aggressor-side (tick/quote-rule) classification, a different, fully identifiable object |
| [`docs/briefs/Q-MSCHAN-1-microstructure-sourcing-channel-scoping.md`](../Q-MSCHAN-1-microstructure-sourcing-channel-scoping.md) | `027a729` | Salvage list this freeze imports: two-stage licensing shape, **≥5s horizon floor**, flicker-filter awareness, **no ES→MNQ lead-lag**; names "signed-trade/CVD" as a family **distinct from** "depth/book-pressure imbalance" |
| **`lab/archive/mnq_orderflow_probe_2026-08-04/{PREREG,RESULTS}.md`** (`MNQFLOW-1`) | `027a729` | DEAD 2026-08-05. 10-level **book-size** imbalance → next-**minute** mid return, `NQ.v.0` `mbp-10`, 3 days, ρ=**−0.01205**, p_emp **0.633** (wrong-signed null). NQ book median **67 contracts / 20 levels**. Re-proposal bar explicitly permits **"a named feature that is not top-of-book size imbalance"** — this pre-reg's trade-aggressor statistic satisfies that carve-out on its face |
| **`docs/briefs/closures/Q-OFCHAN-1-closure-void-coverage.md`**, **`Q-R2AGRUN-1-closure-ambiguous-hold.md`**, **`Q-R2VBUCK-1-closure-falsified.md`**, **`Q-R2FLOW-1-closure-falsified.md`** | `027a729` (all four) | **The single most damaging adverse prior — see §6.** Four consecutive Route-B Stage-G cells on `MNQ.v.0` `tbbo`, all testing some cut of "aggressor/order-flow imbalance → 60-second mid return": flicker-filtered L1 imbalance (coverage 7.36%, VOID), aggressor run-length (\|ρ\|=0.001306 < 0.02 floor at n=22.3M, AMBIGUOUS-HOLD), volume-bucket aggressor ratio (ρ=−0.005478, CI includes 0, FALSIFIED), clock-minute net signed aggressor size (ρ=−0.000701, CI includes 0, FALSIFIED). **None ever reached CONFIRM.** Standing re-proposal bar, verbatim, on all four: *"new mechanism / new G0"* — explicitly **not** a bucket/threshold/horizon retune |
| **`lab/analysis/c1/mnq_ofchan_routeb_2026-08/PREREG_G0.md`** | `027a729` | EXPLORATION window this campaign proposes to reuse: `MNQ.v.0` `tbbo`, **2026-02-06 → 2026-08-06**, priced **$0.0000** (~157.1M records, batch `GLBX-20260807-EHX5KUSF7K`, cached at `~/.databento_cache/q_ofchan_1_exploration_tbbo/`). Reserved CONFIRM for that lineage: **2025-08-06/2025-09-01 → 2026-02-06** (unread; not to be touched by this campaign — §2) |
| [`docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md`](../../adr/2026-08-04-family-k-bank-disclosure-not-gate.md) + [`ops/instruments/MNQ.md`](../../../ops/instruments/MNQ.md) `§K_BANKED` | `6608339` / `1e40b11` | `K_eff = K_intrinsic` only; family bank is mandatory **disclosure**, never a gate. **`K_banked(MNQ) = 21`** as of 2026-08-18 (dominated by `MNQSR-1` structure screen, K=14, unrelated mechanism) |
| [`ops/instruments/MNQ.md`](../../../ops/instruments/MNQ.md) **N6** | `1e40b11` | Modern MNQ 4× cost hurdle ≈ **3.01 bp/session** — the standing bar any future **strategy** construct off this cell must clear; **not** invoked at this discovery stage (§4) |
| [`docs/rejected_candidates.md`](../../rejected_candidates.md) § "Single-instrument index-futures intraday OHLCV directional timing — RAISED BAR" | `027a729` | This candidate sits **outside** the bar's "OHLCV structure alone" scope; clears via the bar's own named **route 2** (order-flow/microstructure), itself parenthesised to the same "don't buy before a survivor" rule Route B exists to satisfy |
| [`docs/briefs/2026-07-27-f1-moc-imbalance-mym-ruling.md`](../2026-07-27-f1-moc-imbalance-mym-ruling.md) | `027a729` | F1 (MOC-imbalance on MYM) cleared **no** route and was `FALSIFIED — reject-at-bar` at the paid-data procurement gate — but F1 was ruled 2026-07-27, **ten days before** Route B existed (`Accepted` 2026-08-05). This campaign clears a route F1 could not have used; F1's kill does not transfer |
| `lesson_cost_law_pre_screen_mr_fade.md` (memory) | read this session | Cost-geometry pre-screen is mandatory **before any edge build** on a **mean-reversion/fade** construction. Engaged and distinguished in §4 — this is a **continuation** hypothesis, not MR/fade, and carries no trade construction yet to price |
| `docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md` | `3c6745a` | Governs the **`daily-range-state-persistence`** claim class (own-series magnitude persistence, IAAFT-surrogate corrected null). Read and **distinguished, not applied**: this cell's claim is a **contemporaneous cross-variable, directional/base-rate** test (does today's morning flow predict today's afternoon return sign), the same class `H-DSTRUCT-MNQ-1` sits in per the futures-anomaly-discovery skill's own red-flag note — not a same-series persistence claim. The corrected battery's IAAFT machinery does not apply; §3's cross-day permutation null (preserving each series' own within-window order) is the appropriate device, following `MNQFLOW-1`'s own precedent for a directional claim |
| `.claude/skills/databento-data/SKILL.md` | `027a729` | Rule 1 (estimate before every pull, always free); Rule 2 (coarsest schema — `tbbo`, not `mbp-1`/`mbp-10`/`mbo`, since this construction needs aggressor classification, not book depth); $125/team free-credit line |
| `.claude/skills/futures-anomaly-discovery/SKILL.md` | present | K discipline; "discovery outputs are candidates, not signals"; "don't buy explanatory data before a survivor" (Simons stage-3 deferral) |

**Dedup attestation (executed, not an empty-grep-is-evidence trap):**

```bash
rg -n -i "aggressor|signed.?trade|CVD|order.?flow.?imbalance|OFI" docs/briefs/ docs/briefs/closures/ ops/instruments/MNQ.md discovery_manifests/
```

This surfaced the entire `OFCHAN → R2AGRUN → R2VBUCK → R2FLOW` lineage (§6) plus `MNQFLOW-1` — all
read in full above, not summarized from a one-line CATALOG entry. **This is the load-bearing dedup
result of this pre-reg**, and it is adverse, not clean.

---

## §1 — The named mechanism (constructed after the agent is named, per standing discipline)

**Agent:** options market-maker / dealer desks with delta-and-gamma exposure in NDX/QQQ-linked
options, who transact in the most liquid available NDX-tracking instrument — NQ/MNQ futures — to
stay delta-neutral as (a) the underlying price moves and (b) their aggregate net gamma changes
through the session.

**Constraint the mechanism relies on:** when dealers are, in aggregate, **short gamma** (the
commonly-cited dominant regime given persistent short-vol overlay and 0DTE-heavy NDX/QQQ options
flow), their hedging is **pro-cyclical** — they must buy into up-moves and sell into down-moves to
hold delta flat as gamma pushes effective delta the "wrong way." This produces a same-day,
one-directional residual pressure that (i) is disproportionately carried by **larger, urgent,
marketable** orders rather than small discretionary clips, because hedging urgency scales with
delta drift, not with a retail trader's discretion, and (ii) should **persist toward the close**
rather than mean-revert, because the mechanical pressure does not resolve until the price move or
the gamma exposure itself abates. This is the **same agent and the same qualitative claim** as
`P4_ROUTEMEMO.md`'s L2 (same-day rest-of-day return predicting last-30-minute continuation,
decaying ~3 days) — this pre-reg is that mechanism's **denser-data-source sibling**, measured
directly on the futures' own tape instead of proxied through the (367×–1,423× thinner) options tape.

**What this pre-reg does NOT claim:** the sign of dealers' aggregate gamma on any given day (that
is exactly the unobservable P4's own thread could not construct from options volume). The mechanism
above is stated **sign-of-price-move-conditioned**, not sign-of-dealer-position-conditioned — it
predicts continuation of whatever direction already showed up in the morning's large-trade flow,
without needing to know why dealers are short gamma on that particular day.

---

## §2 — Frozen construction (single cell, `K_intrinsic = 1`, no sweep)

| # | Element | Frozen value |
|---|---|---|
| S1 | Instrument / symbology | `MNQ.v.0` continuous (native micro — **not** the `NQ` parent proxy; per this session's fresh dry-run, `MNQ.FUT` now out-trades its own `NQ.FUT` parent, so the proxy-discipline detour is unnecessary here) |
| S2 | Schema | `tbbo` (trade + prevailing BBO at time of trade — the coarsest schema that can classify aggressor side; bare `trades` cannot, per `P4_DRYRUN.md` §1's reasoning, imported directly) |
| S3 | Session | RTH **09:30:00–16:00:00 ET**, split at **12:00:00 ET** into an AM predictor window and a PM target window |
| S4 | Aggressor classification (Lee & Ready 1991, quote rule + tick-rule fallback) | trade_price ≥ `ask_px_00` in force ⇒ **BUY**; trade_price ≤ `bid_px_00` ⇒ **SELL**; strictly between (stale/hidden-liquidity edge case) ⇒ tick test vs. the immediately preceding **classified** trade price (up-tick ⇒ BUY, down-tick ⇒ SELL, zero-tick ⇒ inherit); a session's first trade with no preceding classified trade is **dropped** (≤1 trade/session) |
| S5 | Size filter ("large" trade) | size ≥ **10 contracts**, frozen **a priori** — chosen as a conservative multiple of MNQ's well-known modal 1-lot clip, **before** any MNQ trade-size distribution in this campaign's own data is examined. This is a single frozen judgment call, not a fitted or swept cutoff; sweeping it would be a new campaign |
| S6 | Predictor | `LTI_norm(s) = Σ sign_i·size_i / Σ size_i` over all large trades (S5) with `sign_i` = +1 (BUY) / −1 (SELL) (S4), restricted to 09:30–12:00 ET. Session dropped if the AM large-trade population is empty (`Σ size_i = 0`) |
| S7 | Target | `r_pm(s) = ln(P_16:00 / P_12:00)`, where `P_t` = last **trade** price at or before clock time `t` on session `s` (both reference points computed from the same `tbbo` pull — no second schema needed) |
| S8 | Predicted sign | **Positive** — `LTI_norm(s)` and `r_pm(s)` move together (continuation), matching P4/L2's own predicted direction |
| S9 | Statistic | Spearman ρ(`LTI_norm`, `r_pm`) across all usable sessions in a window |
| S10 | Null | Permutation of the **session-date pairing** between `LTI_norm` and `r_pm` (each series' own within-window sequence order preserved; only the cross-series alignment is shuffled) — the appropriate device for a contemporaneous directional/base-rate claim (§0, magnitude-persistence-battery distinction), and the same design logic `MNQFLOW-1` used for its own directional claim at a different (intraday-minute) grain |
| S11 | Permutation parameters | M = **2,000** draws, seed = **20260822** (this freeze's date, `numpy.random.default_rng(20260822)`) |
| S12 | p-value | one-sided (predicted positive): `p_emp = (1 + #{ρ_null ≥ ρ_obs}) / (M + 1)` |
| S13 | Roll handling | sessions containing a front-month volume-lead change (per the repo's standing per-UTC-day `ohlcv-1d` volume-leader stitch rule) are **excluded**, not traded through — matching the DL-1/DISC-CAMP-0 precedent, since `LTI_norm`/`r_pm` are level-adjacent, roll-sensitive objects |

**Forbidden inside the cell (frozen, no exceptions):** a second size threshold; a second session
split time; a second horizon (e.g. scoring 12:00→14:00 as well as 12:00→16:00); an ES/NQ/YM
sibling; conditioning on ORB timestamps, day-of-week, or realized volatility; reading the CONFIRM
window's raw bytes before Stage-C fires (§7).

---

## §3 — Data, cost, and the two-window design (both windows disjoint from each other AND from the OFCHAN/R2\* lineage's windows)

| Partition | Window | Records/records-cost basis | Priced | Role |
|---|---|---|---|---|
| **EXPLORATION** | `MNQ.v.0` `tbbo`, **2026-02-06 → 2026-08-06** (6 months) | **Reuse of the already-cached `q_ofchan_1_exploration_tbbo` batch** (~157.1M records, `GLBX-20260807-EHX5KUSF7K`) — **no new pull**, subject to confirming the cache is still intact at GO time | **$0.00** (cache reuse; mechanical check, not a re-purchase) | Stage-G promotion gate only (§7) |
| **CONFIRM** | `MNQ.v.0` `tbbo`, **2025-05-01 → 2025-07-31** (3 months, ≈62 RTH sessions — exact count confirmed only once the calendar is pulled) | Fresh pull, never touched by any prior campaign | **Estimated ~$82.23** (tbbo) — see correction below | Single binding verdict read (§7), once, after Stage-G promotes |

**Why CONFIRM is neither the OFCHAN-lineage window nor the most recent quarter.** The OFCHAN/R2\*
lineage's own reserved holdout (2025-08-06 or 2025-09-01 → 2026-02-06, sources disagree by three
weeks across their closures) is **still unread** and earmarked to that lineage's own possible
reopening; reusing it here would blur two campaigns' evidentiary claims onto one holdout, which
`discovery_manifests/burned_segments.json`'s own caution against a shared reserved window silently
burning across unrelated campaigns argues against. The most recent elapsed quarter (~2026-05→08) is
**also** not used, to keep it clean for any future campaign wanting the freshest liquidity regime.
2025-05→07 is genuinely fresh (untouched by any manifest, closure, or cache found in this session's
dedup sweep), sits entirely inside the native-micro, post-2019 era, and by this session's own
finding was already inside the regime where MNQ out-trades its NQ parent.

**Cost correction (load-bearing, stated explicitly).** The task background's headline figure is
**$49.3362** for a 3-month `MNQ.FUT` **`trades`** pull. That schema is **insufficient for this
construction** — S4's aggressor classification needs the prevailing quote, which bare `trades`
does not carry (§0, `P4_DRYRUN.md` §1 imported directly). The schema this pre-reg actually needs is
`tbbo`, priced at this session's own fresh dry-run as **$82.2270** for a 3-month window. **$82.23,
not $49.34, is the correct authorized-if-approved figure for the CONFIRM pull.** Both figures are
disclosed so the discrepancy is visible, not smoothed over.

**Second correction — do not trust either number at GO time.** The OFCHAN campaign's own G1 estimate
(2026-08-06, sixteen days before this freeze) priced a **six-month** `MNQ.v.0` `tbbo` pull at
**$0.0000** under whatever entitlement was live that day (`docs/notes/2026-08-04-databento-entitlement-inventory.md`
records "tbbo/trades ~1y free," consistent with that zero). This session's own fresh dry-run, sixteen
days later, priced a **three-month** window at **non-zero** cost. Entitlements evidently move (rolling
window, consumption, or a subscription change) inside weeks, and this pre-reg's proposed CONFIRM
window (2025-05→07) is neither of the two windows either estimate was run against. **Rule 1 is not
optional here**: re-run `estimate` on the exact frozen 2025-05-01→2025-07-31 / `MNQ.v.0` / `tbbo`
request immediately before GO, and treat $82.23 as a ballpark anchor, not a quote.

```bash
# Stage-G: mechanical cache-presence check only, no billing, no new pull
ls ~/.databento_cache/q_ofchan_1_exploration_tbbo/ 2>/dev/null | wc -l
# expect: 155 *.tbbo.dbn.zst files present (per Q-OFCHAN-1's own PREREG_G0 disclosure)

# Stage-C: mandatory fresh estimate before ANY GO or pull (always free, never bills)
PYTHONPATH=lab python -m databento_fetch.db_fetch estimate \
  --symbols MNQ.v.0 --stype continuous --schema tbbo \
  --start 2025-05-01 --end 2025-07-31 --phase oos --campaign-id MNQTAPE-1-confirm
# Record the returned $ figure here before any pull is even proposed: __________
```

**$125/team free-credit line (databento-data skill):** distinct from the unrelated $700 c1-rail
execution ceiling. At ~$82 (pending re-estimate), this single pull sits comfortably inside the
$125 line; it is **not** cost-gating by itself, but Rule 1's estimate-first discipline still
applies in full, and the credit line is a team-wide budget other campaigns also draw against.

---

## §4 — Cost-law pre-screen engagement (per standing discipline, not skipped)

**Does the MR/fade pre-screen (`lesson_cost_law_pre_screen_mr_fade`) apply here?** No, on its own
terms, and the reason is stated rather than assumed: that lesson's trigger is a **mean-reversion /
fade** construction, where the gross edge harvested per trade is characteristically a few bp — the
same order of magnitude as round-trip cost, so a 5-minute geometry calculation kills it before any
harness is built. §1/§2's hypothesis is explicitly a **continuation** claim (same-day flow predicts
same-direction follow-through), the opposite shape, so the specific MR/fade trigger does not fire.

**What the general discipline still demands, and how it is honored here.** The underlying rule —
compute the cost geometry before building anything — presupposes a **trade construction** (an entry,
a stop, a target, a round-trip cost) to price. This pre-reg has none: `LTI_norm` and `r_pm` are a
predictor and a target for a pure statistical-association test, not a strategy. This is not an
evasion; it is the same posture `MNQFLOW-1`, `OFCHAN`, `R2AGRUN`, `R2VBUCK`, and `R2FLOW` all took
explicitly ("not a session strategy... does not license a campaign by itself... no Stage-0 opened
here"). **If, and only if, this cell reaches `SURVIVOR` (§7) and a follow-on strategy-construction
campaign is proposed**, that campaign inherits `ops/instruments/MNQ.md` **N6** — the modern MNQ 4×
cost hurdle, **≈3.01 bp/session** — as a mandatory Harvest Requirement-5 gate before any deployment
claim. That obligation is named here as **forward-owed**, not discharged, and not evaded.

---

## §5 — Falsifiable hypothesis

**H (MNQTAPE-1):** on the frozen one-cell catalogue in §2, Stage-G promotion clears on the
EXPLORATION window (§7), and — under a separate operator confirm-GO — the CONFIRM window
(2025-05-01 → 2025-07-31) shows `ρ(LTI_norm, r_pm) > 0` with one-sided `p_emp < 0.05` (M=2,000, seed
20260822) **and** `|ρ_confirm| ≥ 0.20`.

**H fails** if the CONFIRM read shows the wrong sign, `p_emp ≥ 0.05`, or `|ρ_confirm| < 0.20` — any
one limb failing is `FALSIFIED`, not a partial credit.

**Power, computed at freeze (Fisher-z, one-sided α=0.05, N≈62 sessions, SE = 1/√(N−3) ≈ 0.1302):**

| True ρ | z(ρ) | Power |
|---|---|---|
| 0.20 | 0.2027 | ≈0.47 |
| 0.25 | 0.2554 | ≈0.62 |
| 0.30 | 0.3095 | ≈0.77 |
| 0.35 | 0.3654 | ≈0.88 |

The §5 confirm floor (`\|ρ\| ≥ 0.20`) sits at the edge of what N≈62 can even reliably detect
(power ≈0.47 at exactly the floor) — disclosed as a real limitation, not hidden. This is the honest
price of a fresh, non-colliding, 3-month window rather than a longer one; extending the window after
seeing a near-miss is a forbidden move (§ below), not a remedy.

---

## §6 — Why this is a new campaign, not a retune of the `OFCHAN → R2AGRUN → R2VBUCK → R2FLOW` lineage (operator-adjudicated, not self-certified)

All four closed cells in that lineage tested some cut of "aggressor/order-flow imbalance predicts a
**60-second** mid return," using **all** trades (or all ten book levels), with **no** size filter,
under a mechanism-agnostic, textbook market-microstructure price-impact framing (Kyle/Hasbrouck-style
— no named agent). All four died at Stage-G; none ever reached CONFIRM. Their own closures state,
verbatim and repeatedly: **"re-proposal = new mechanism / new G0"** — explicitly not a bucket,
threshold, or horizon retune.

**This pre-reg's claim to clear that bar** (stated as a claim, for the operator to weigh, not
asserted as already adjudicated — matching this repo's own convention of putting genuinely
ambiguous scope calls to the GO mark rather than self-certifying them):

1. **A named agent**, not a generic impact hypothesis — dealer/gamma-hedging desks specifically
   (§1), the same agent P4/L2 named, versus the four prior cells' agent-free "does flow move price"
   framing.
2. **A different observable population** — large trades only (≥10 contracts), hypothesized to carry
   that agent's footprint disproportionately, versus the four prior cells' **all-trade** aggregate,
   which at 60-second granularity is dominated by market-making/HFT/retail noise — exactly the
   population three of the four cells measured as null or sub-floor.
3. **A categorically different horizon** — session-scale (a 4-hour PM window, following a 2.5-hour
   AM accumulation), matching the order of magnitude of P4/L2's own "~3-day decay" claim, versus the
   prior lineage's uniform 60-second target.

**What this pre-reg does NOT claim:** that these three differences are self-evidently sufficient to
clear "new mechanism" as a matter of doctrine. That reading is offered here for the operator's GO
mark to adjudicate, the same way `DL-1`'s bar-scope questions were gathered for its GO rather than
resolved by the drafting session.

**Base-rate caution, stated with the same prominence as the case for proceeding (visible restraint,
not smoothed over).** Counting every order-flow/microstructure construction tried on this instrument
family to date — the options-tape density wall (P4/L2, ×2 findings, HOLD), 10-level book-depth
imbalance (`MNQFLOW-1`, FALSIFIED), and the four-cell `OFCHAN`/`R2AGRUN`/`R2VBUCK`/`R2FLOW` lineage
(VOID-COVERAGE, AMBIGUOUS-HOLD, FALSIFIED, FALSIFIED) — **six consecutive dead ends** now sit under
this broad modality, and none has ever reached a CONFIRM read. This pre-reg's own §5 power table
shows it is not obviously better-powered than its predecessors. The honest disclosure is: a seventh
attempt, even one arguing a different mechanism, is a real bet against a mounting base rate, and the
operator should weigh that explicitly rather than infer confidence from the length of this document.

---

## §7 — Frozen procedure and gate

| Step | What happens | Gate (frozen) |
|---|---|---|
| 1. Operator GO on this design | — | mechanical |
| 2. Stage-G EXPLORATION | Cache-presence check (§3) → compute `LTI_norm`/`r_pm` per §2 on 2026-02-06→2026-08-06 → Spearman ρ + permutation p per S9–S12 | **Promote** iff (a) `N_usable ≥ 60` sessions, **and** (b) `sign(ρ_explore) = +`, **and** (c) `p_emp(explore) < 0.20` (deliberately loose — a candidate screen, not the verdict; see rationale below). Any limb failing ⇒ **ABANDON**, $0 spent, no CONFIRM read, campaign closes |
| 3. Operator confirm-GO | Separate, explicit sign-off on the ~$82 CONFIRM spend (§3), after a fresh `estimate` | mechanical |
| 4. Stage-C CONFIRM | Single pull, single run, on 2025-05-01→2025-07-31 only | `SURVIVOR` iff `ρ_confirm > 0` **and** `p_emp(confirm) < 0.05` **and** `\|ρ_confirm\| ≥ 0.20`; `FALSIFIED` if any limb fails; `AMBIGUOUS-HOLD` if `N_usable(confirm) < 30` (report census, do not extend the window without a fresh freeze) |
| 5. Disposition | `SURVIVOR` → hands to `strategy-validation` as a **footprint candidate**, explicitly not a strategy (§4); N6 cost-hurdle owed before any construct. `FALSIFIED`/`ABANDON` → DEAD-list row on `ops/instruments/MNQ.md` under a **new** mechanism id (e.g. `aggressor-large-trade-continuation`), re-proposal bar = new mechanism, not a threshold/horizon retune | frozen |

**Why Stage-G is deliberately looser than the `OFCHAN`/`R2\*` lineage's own Stage-G gates.** Those
four cells ran what amounted to a full CI-and-placebo-and-magnitude test **at the exploration stage**
— effectively a second confirmatory test before ever reaching CONFIRM — and all four died there. This
design pushes the binding statistical bar entirely onto the single CONFIRM read (§5), matching Route
B's own stated shape ("exploration emits candidates only"); Stage-G here only screens out a dead or
wrong-signed construction before spending real money, which a sign-check plus a loose `p<0.20`
sanity bar accomplishes without repeating the prior lineage's specific failure shape of over-testing
on free data.

---

## §8 — Outstanding authorizations (updated 2026-08-23)

1. **Design GO** — **GIVEN**, operator (Joshua), 2026-08-23 chat.
2. **EXPLORATION GO** — **GIVEN**, same authorization, read as covering the mechanically-free Stage-G
   computation against the already-cached `q_ofchan_1_exploration_tbbo` bytes. This commits the
   `K_intrinsic=1` disclosure and opens a `register_search` (§11 updated on execution).
3. **CONFIRM spend GO** — **STILL OUTSTANDING.** A **separate**, explicit authorization for the ~$82
   (pending re-estimate) `tbbo` pull on 2025-05-01→2025-07-31 is required before that spend. This is
   real money against the $125/team credit line and must not be inferred from (1) or (2). Per Rule 2
   ("budget before acting") and the databento-data skill's own discipline, this GO is requested, not
   assumed, and is requested **only after** Stage-G promotes — spending it on a candidate that never
   cleared Stage-G would itself be a forbidden move.

**No data has been pulled for CONFIRM. No CONFIRM test has been run. Only the Stage-G EXPLORATION
computation (§7 step 2, $0, cache-reuse) is authorized to execute as of this update.**

---

## §9 — Forbidden moves

- Reading any CONFIRM-window byte before Stage-G promotes (§7) — the ordering trap this whole Route
  B apparatus exists to prevent.
- Retuning the ≥10-contract threshold, the 09:30/12:00/16:00 ET boundaries, the permutation seed, or
  M after seeing **any** result, exploration or confirm (Trap #12 / FM-9).
- Adding a second size bucket, a second horizon, a second session split, or an ES/NQ/MYM sibling
  without a fresh `K_intrinsic` and a fresh freeze — each is a new campaign.
- Treating a Stage-G promote as an edge, a seed, a watchlist gate, or a Cap claim — it licenses
  exactly one CONFIRM spend decision and nothing else.
- Treating a CONFIRM `SURVIVOR` as a deployable strategy. No entry, stop, target, or per-trade cost
  is defined anywhere in this document; any strategy construction is a **fresh, separate**
  pre-registration that inherits N6 (§4).
- Claiming Avenue-A Route A (survivor-tie) for this campaign — it has none and proceeds under Route
  B only (§0).
- Reusing the `OFCHAN`/`R2*` lineage's own reserved CONFIRM window (2025-08/09→2026-02-06) for this
  campaign's CONFIRM — a fresh, disjoint window is used specifically to avoid a shared-holdout
  collision (§3).
- Spending the CONFIRM-window dollar figure off the design-GO alone (§8) — a separate GO is required.
- Sub-5-second tradeable-claim framing (N/A here by construction — shortest interval is hours — but
  stated per the ADR's own standing forbidden move for completeness).
- ES→MNQ or NQ→MNQ lead-lag constructs (N/A — single-instrument throughout).
- Quoting this document's power table (§5) as if it were already-measured evidence, or citing
  `MNQFLOW-1`/the R2\* lineage's null results as proof this cell will also fail — both directions of
  overclaiming are barred; §6's base-rate caution is a disclosure, not a verdict either way.

---

## §10 — Audit hooks (runnable)

```bash
# Route B is still Accepted (re-verify before GO; a revert invalidates this entire document)
grep -n "^\*\*Status:\*\*" docs/adr/2026-08-05-avenue-a-generate-confirm-route.md
# expect: Accepted

# The adverse-prior lineage this pre-reg is judged against
rg -n "new mechanism / new G0|new G0 / new mechanism" docs/briefs/closures/Q-OFCHAN-1-closure-void-coverage.md \
  docs/briefs/closures/Q-R2AGRUN-1-closure-ambiguous-hold.md \
  docs/briefs/closures/Q-R2VBUCK-1-closure-falsified.md \
  docs/briefs/closures/Q-R2FLOW-1-closure-falsified.md

# Family K bank — re-read fresh, never trust this document's snapshot
grep -n "K_banked(MNQ)" ops/instruments/MNQ.md

# Mechanism door-check (nearest registered id; this construction has no id of its own yet)
python scripts/instrument_profiles.py cell MNQ order-flow-depth-imbalance

# EXPLORATION cache still present (mechanical, no billing)
ls ~/.databento_cache/q_ofchan_1_exploration_tbbo/ 2>/dev/null | wc -l

# Fresh CONFIRM estimate — MANDATORY before any GO, always free
PYTHONPATH=lab python -m databento_fetch.db_fetch estimate \
  --symbols MNQ.v.0 --stype continuous --schema tbbo \
  --start 2025-05-01 --end 2025-07-31 --phase oos --campaign-id MNQTAPE-1-confirm

# No procurement has happened on the back of this document (expect no manifest, no cache growth)
ls discovery_manifests/ | rg -i "mnqtape" || echo "no manifest yet, as expected (zero K spent)"
```

## §11 — Registry / logging

**Not admitted through intake.** No `register_search open`, no manifest, no `docs/briefs/INDEX.md`
row, no `lab/CATALOG.md` row — matching the standing precedent for every pre-GO route memo and every
frozen-but-unopened pre-registration in this repo (`P4_ROUTEMEMO.md`, `Q-OFCHAN-1` before its explore
GO, `Q-MSCHAN-1`'s `DRAFTED — NOT OPENED` status). Harvest §4's limb-2 counter does **not** increment.
If the operator GO(s) in §8 are given and the campaign opens, it banks `K_intrinsic=1` and, on
closure, `K_banked(MNQ)` moves **21 → 22** regardless of verdict (disclosure, not a gate, per ADR
2026-08-04).

---

## Verification

§0 cites production paths with real anchors, including the four-cell adverse-prior lineage found by
an executed (not assumed-empty) dedup sweep ✓ · §1 names the agent and mechanism before §2 freezes
the statistic ✓ · §2 single frozen cell, `K_intrinsic=1`, every threshold stated as a priori not
fitted ✓ · §3 cost figure corrected from the task's own `$49.34` to the schema-correct `$82.23`, with
the discrepancy against the OFCHAN lineage's `$0.00` estimate disclosed rather than hidden ✓ · §4
engages the MR/fade cost-law discipline and states why it doesn't fire here, without skipping the
general obligation ✓ · §5 binary `H` with a computed, disclosed power table showing the confirm floor
sits near the edge of what the window can detect ✓ · §6 states the case for "new mechanism" as a
claim for operator adjudication, not a self-certified pass, and gives the base-rate caution equal
prominence ✓ · §7 gate table binary, Stage-G deliberately looser than the failed lineage's own gate,
with the reason stated ✓ · §8 three distinct outstanding authorizations, none granted here ✓ · §9
forbidden moves include not overclaiming this document's own power table ✓ · §10 runnable ✓ · zero
data pulled, zero tests run, zero dollars spent, zero K charged ✓.
