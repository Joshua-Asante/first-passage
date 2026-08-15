# `Q-WLEGB-1` — VERDICT PRE-REGISTRATION: does the W-layer bias transfer below the weekly close?

**FROZEN ON THIS FILE'S INTRODUCING COMMIT. No criterion below may move after the first real
conditional hit-rate exists. Zero conditioning numbers have been computed at freeze time — leg (a)'s
weekly-close rates are known (NQ 0.5880 / MNQ 0.5751), but no sub-weekly conditional rate has ever
been computed for this object, on any instrument.**

**K:** `0` — one-way falsifier, no GO state (§7). **Cost:** `$0.00` (MNQ 1m already pulled at
`$0.0000`; daily and weekly are resampled from it). **No manifest. No Cap seat.**
**Class:** order-free, strategy-free, zero-run — the `Q-ICTEXP-1` mould.
**Authored:** 2026-08-04 · Claude Code (Opus 5), operator-directed.

---

## §0 — Rule 0 reads (verified this session 2026-08-04)

- **[`lab/archive/ict_cascade_2026-06-18/PREREG-W.md`](../../archive/ict_cascade_2026-06-18/PREREG-W.md) L62 @ `47cc3eb`** — the two-leg split, verbatim: *"W-1 has two legs. `gateBias` fixes **leg (a) only** … It is STILL a **weekly-close proxy**, NOT per-entry gate accuracy (**leg b**). Leg (b) is the separate offline gate-transfer probe (§7.B W-6) and is NOT settled by this layer's verdict."* And L78/L90: a RESOLVED leg (a) *"routes the structure-only bias toward continued use and a downstream per-entry transfer probe … it does **not** lock, deploy, or by itself license the 1M gate."*
- **`TEST_PLAN.md` L179 @ `47cc3eb`** — the archived W-6: *"**Gate-transfer probe** (= B2-W). 1M bias-gate ablation; compare per-entry directional accuracy to the weekly-close hit-rate."* **That form is permanently BLOCKED** — it needs per-entry records from the lost `ict_1m_execution_DRAFT.pine` under a bias-gate on/off split, and the `netBias` formula survives only in that file (verified absent four ways, 2026-08-04 audit). **This pre-registration does NOT claim to run W-6.** See §1.
- **[`lab/analysis/_inbox/ict_mnq_2026-08/build_w_export.py`](build_w_export.py) @ `9aaa578`** — leg (a)'s adapter, 28 unit tests. Reused **unmodified** for the weekly object: `pine_ema` (L48, TV `ta.ema` convention, seeded at bar 0), `vStruct = sign(close − wEma)` (L192), `EMA_LEN = 20` LOCKED, `in_roll_window` (L88, ±4 days of 3rd-Friday Mar/Jun/Sep/Dec).
- **[`RESULTS.md`](RESULTS.md) §2 @ `9aaa578`** — leg (a)'s verdict and its explicit scope limit: *"W's scope is leg (a) only … per-entry gate accuracy (leg b) is a separate probe, **not settled** by this verdict. `SLR-MYM-1` §2.1 records the overclaim to avoid here."*
- **[`RESULTS_1H_1M.md`](RESULTS_1H_1M.md) §1 @ `9aaa578`** — **the design driver.** The 1H layer's cleanest kill needed no threshold at all: discount→up measured **0.5394** against a **sign-shuffle placebo of 0.5485** — *"The real effect is weaker than its null."* And premium→down came in at **0.4537**, resolving **opposite** to the claim, because MNQ trends up. **Any directional hit rate on this instrument is inflated by the secular uptrend, so a raw rate versus 0.50 is not a test.** §3 below makes the placebo the primary bar for exactly this reason.
- **[`ops/instruments/MNQ.md`](../../../../ops/instruments/MNQ.md) F2 GUARD @ `f4b5a34`** — *"The ORB filter slices that 'look better' in-sample … are the exact class pre-reg §5 forbids amending on. Routing them into this ledger as 'instrument observations' would be that forbidden amendment wearing a different label … Highest-risk laundering move on this instrument."* **This read changed the design** — see §1.
- **[`ops/instruments/MNQ.md`](../../../../ops/instruments/MNQ.md) N8, W2** — N8 records leg (a) as instrument-general and states its own scope limit ("**NOT** per-entry gate accuracy"); W2 warns that databento `ohlcv-1d` buckets by UTC calendar day and yields phantom weekend bars, which is why §2 resamples from 1m under explicit bucketing rather than pulling a daily schema.
- **[`docs/notes/2026-08-03-ict-instrument-confirmation-nodeploy-ruling.md`](../../../../docs/notes/2026-08-03-ict-instrument-confirmation-nodeploy-ruling.md) @ `6d9e603`** — forbidden move 1: no re-framing of a RESOLVED W result as a deployability step without a fresh K-bound proposal. Binds §5 here.
- **[`docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md`](../../../../docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md) @ `2ef7405`** (`Accepted`) — `K_eff = K_intrinsic`. **`K_banked(MNQ) = 2`, disclosed here per Requirement 3 and not gating.**

---

## §1 — What this is, and the design the F2 guard forced

**The question leg (b) asks:** the W-layer bias was RESOLVED as a **weekly-close** hit rate. Does it
carry predictive content at a granularity finer than the weekly close — or is it a statement about
weekly bars and nothing else?

**The obvious cheap design, and why it is rejected.** The tempting move is to condition an existing
real MNQ entry set on `vStruct` and read per-entry accuracy. The only large real MNQ entry set in
the repo is `ORB-MNQ-1`'s (1,026 entries with bar coverage). **That design is forbidden here.**
Conditioning ORB entries on a weekly bias is a conditioning gate on ORB — the fifth, after
gap/GEX/T10Y3M/day-of-week (N6/N8/N9/N10, all pre-registered and all FALSIFIED) — and the standing
**F2 guard** names exactly this as the highest-risk laundering move on the instrument. A favourable
result would be indistinguishable from the forbidden amendment wearing a different label, and an
unfavourable one would be uninformative about the gate (it would confound gate content with ORB's
own construct). **Rejected on both limbs.**

**The design used instead: strategy-free, at the instrument level.** Measure whether the prior
week's `vStruct` sign predicts the sign of **daily** returns inside the following week, on MNQ bars
alone. No strategy, no entries, no fills, no P&L, no ORB. This isolates the *gate* from any
construct's idiosyncrasies, which is a stronger test of the gate than the ORB design would have
been, and it is free of F2 entirely.

**Honest scope statement — this is NOT the archived W-6.** W-6 is a *1M bias-gate ablation on
per-entry records* and stays permanently `BLOCKED-LOST-PINE`. This probe answers the same underlying
question (does the weekly bias have sub-weekly predictive content?) with a strategy-free instrument.
A RESOLVED here does **not** discharge W-6; it would mean the gate has sub-weekly content in
principle, leaving open whether any particular construct's entries inherit it.

---

## §2 — Frozen construction

**Object (inherited verbatim from leg (a); nothing re-derived).** Weekly bars resampled from
`MNQ.v.0` 1m. `wEma = pine_ema(weekly_close, 20)`; `vStruct = sign(close − wEma)` ∈ {+1, 0, −1};
the predictor for week *w* is `vStruct[w−1]` — the **prior completed week**, the same `[1]` lag leg
(a) used. Weeks with `vStruct = 0` are unscored.

**Outcome — the verdict cell.** For each **day** *d* falling inside week *w*:
`realized[d] = sign(close[d] − close[d−1])` — the **direct daily analogue of leg (a)'s
`realized = sign(close − close[1])`**, inherited rather than chosen. `gateHit[d] = (vStruct[w−1] == realized[d])`.
Days with `realized = 0` are unscored.

**Bucketing (W2-aware).** Days and weeks are cut from 1m bars on **ET calendar dates**
(`America/New_York`), not UTC — this avoids the phantom-weekend-bar artifact W2 names. A day is
kept only if it carries ≥ 1 bar; a week is Monday-anchored on ET dates.

**Roll exclusion.** `in_roll_window` (±4 days of the 3rd Friday of Mar/Jun/Sep/Dec) applied at the
**day** level, inherited from `PREREG_D_W.md` §2.

**Declared DISCLOSURE cell (not a verdict, never selected from).** The same measurement with
`realized_oc[d] = sign(close[d] − open[d])` — session open-to-close. This is the granularity an
E1-compliant construct could actually trade (the overnight gap is unholdable under a 16:00 ET flat
rule), so it is the more decision-relevant number — **but it is not the verdict**, because
close-to-close is the cell that inherits leg (a)'s definition without a new choice. Reported with
its own placebo. **Selecting the verdict from whichever cell reads better is forbidden (§5).**

---

## §3 — The bar: a sign-shuffle placebo, not 0.50

**MNQ trends up, so `gateHit` is inflated by base rates alone.** If `vStruct` is +1 in most weeks
and daily returns are up in most days, a raw hit rate above 0.50 is arithmetic, not evidence. This
is precisely how the 1H layer died — discount→up measured 0.5394 against its own placebo at 0.5485.

**Placebo construction (frozen).** Shuffle the `vStruct` labels **across weeks**, holding the daily
outcome sequence fixed. This preserves (i) the marginal distribution of `vStruct`, (ii) the marginal
distribution of daily outcomes, and (iii) the within-week autocorrelation of returns — destroying
only the *pairing*. `B = 2000` shuffles, `seed = 20260804`.

**Primary bar:** measured `gateHit` must exceed the **95th percentile** of the placebo distribution.

**Supporting limbs (all required for RESOLVED, inherited from `PREREG-W.md`'s gate):**
moving-block-bootstrap CI lower bound **> 0.50** (blocks = weeks, `B = 2000`); **both halves** >
0.50; **all three thirds** > 0.50; effective N ≥ **30** scored week-blocks.

---

## §4 — Falsifiable hypothesis

**H-WLEGB-1 (the sole hypothesis under test; `K_intrinsic = 1`).** The W-layer bias carries
predictive content below the weekly close: on MNQ, prior-week `vStruct` predicts the sign of daily
close-to-close returns at a rate exceeding its own base-rate-matched sign-shuffle placebo (95th
pct), with a block-CI lower bound above 0.50 and stationarity across halves and thirds.

**Falsifier — frozen trigger table. If a trigger fires, the stated verdict follows.**

| # | Trigger | Threshold | Verdict |
|---|---|---|---|
| L1 | scored week-blocks | **< 30** | **`INSUFFICIENT-N`** |
| L2 | measured `gateHit` vs placebo 95th pct | **at or below** | **`FALSIFIED`** — the effect does not beat its own null; the 1H kill shape, and it needs no threshold argument |
| L3 | block-CI lower bound | **≤ 0.50** | **`FALSIFIED`** |
| L4 | L2 and L3 clear, but any half ≤ 0.50 or any third ≤ 0.50 | — | **`AMBIGUOUS-HOLD`** — non-stationary, exactly as leg (a)'s own gate routes it |
| L5 | all limbs clear | — | **`RESOLVED`** — sub-weekly content demonstrated. **Licenses nothing** (§5 FM-1) |

**One line:** *if* the weekly bias cannot beat a base-rate-matched shuffle of itself at daily
granularity, *then* the W finding is a statement about weekly bars only and the "W/D as a gate for
an intraday construct" idea dies for $0; *if* it can, *then* the gate has sub-weekly content and a
future K-bound construct may cite this — as warrant, never as a deployability gate.

**Pre-registered expectation, recorded so neither outcome can be over-read.** Leg (a)'s edge is
modest (0.5751 on MNQ weekly). Daily returns are noisier than weekly ones, so if the content is
real it should be **weaker** at daily granularity, not stronger. **A daily rate materially above
leg (a)'s weekly rate would be a red flag for a construction defect, not a discovery** — it would
most likely mean base-rate leakage the placebo failed to absorb, and §6 requires investigating it as
a defect before reporting it as a result.

---

## §5 — Forbidden moves

- **FM-1 — Reading `RESOLVED` as a deployability gate, or as licence to open a construct.** Barred by `CONFIRM-FREE-NODEPLOY-2026-08-03` forbidden move 1 and by leg (a)'s own routing language. RESOLVED here upgrades a belt finding; it opens nothing. **This probe has no GO state.**
- **FM-2 — Selecting the verdict from the disclosure cell.** The verdict reads close-to-close and only close-to-close (§2). If open-to-close reads better, that is a *disclosure*, and promoting it after the fact is the outcome-conditional selection this campaign has refused twice already.
- **FM-3 — Conditioning any strategy's entries on `vStruct`**, ORB's above all. F2 guard; see §1.
- **FM-4 — Adding horizons, lags, `emaLen` values, or a bias×regime split.** One frozen object, one verdict cell, one declared disclosure. A sweep is candidate generation and consumes K.
- **FM-5 — Re-reading a `FALSIFIED` here as a verdict on leg (a).** Leg (a) is RESOLVED at the weekly close and stays RESOLVED; this probe bounds its *scope*, and a failure means "weekly-only", not "wrong".
- **FM-6 — Quoting the raw hit rate without its placebo.** On an uptrending instrument the raw number is not interpretable alone; this is the specific error the 1H layer's placebo caught.
- **FM-7 — Any `core/`, lock, allocation, `dd_protection`, lifecycle, Pine, rail, or `LEG_MAP` change**; no edit to `lab/archive/` (the byte-identity pin must keep returning empty).

---

## §6 — Verdict gate and typed dispositions

Per [ADR 2026-08-04 Iterate-closure-exit](../../../../docs/adr/2026-08-04-iterate-closure-exit-mandatory.md) §2 item 2, each verdict pre-registers its disposition branch.

| Verdict | Trigger | **Disposition (pre-registered)** |
|---|---|---|
| `INSUFFICIENT-N` | L1 | **STOP** — the object is unmeasurable on 7 years of MNQ; re-proposal bar = a materially longer panel, which does not exist for a micro |
| `FALSIFIED` | L2 or L3 | **STOP** — the W finding is weekly-only. Re-proposal bar: a *mechanism* argument for why weekly structure should carry intraday, not a re-test at another horizon. Writes MNQ ledger N8 scope-narrowing + a DEAD row |
| `AMBIGUOUS-HOLD` | L4 | **ITERATE → Investigate.** Entry packet: the non-stationary half/third, the frozen object, and the placebo distribution; forbidden re-open = re-running with a different `emaLen` or horizon |
| `RESOLVED` | L5 | **ITERATE → dated packet / operator decision item.** Names, does not open, a K-bound construct proposal. Entry packet carries: this verdict, leg (a)'s numbers, the placebo margin, **and FM-1** |

**Board write** is owed at closure in all four branches (STATE forward-board row or SESSIONS
Open/next line), per the same ADR.

---

## §7 — Governance: why K = 0

Identical structure to `Q-ICTEXP-1`, which the operator ruled K-free on 2026-08-04 (*"run the
probe, it's K-free"*): the outcome set is `{INSUFFICIENT-N, FALSIFIED, AMBIGUOUS-HOLD, RESOLVED}`,
there is **no GO state**, one frozen object with zero free parameters is measured, and FM-1
forecloses reading the best outcome as licence. A one-way falsifier cannot manufacture a false
positive, so it does not consume the budget that exists to prevent one.

**And the stakes are now low either way:** under [ADR 2026-08-04](../../../../docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md)
(`Accepted`) `K_eff = K_intrinsic`, so even if a later ruling deems this K-bound, `K_intrinsic = 1`
⇒ floor **0.650** — nothing is foreclosed on either reading. **Disclosure per harvest Requirement 3:
`K_banked(MNQ) = 2`** (`d5_nq_intraday_mom` 1 + `st_eh_supertrend_grid` executed-split 1); it is
reported here and does not gate.

---

## §10 — Audit hooks (runnable)

```bash
# Freeze ordering must be git-auditable: this file's commit precedes RESULTS_LEGB.md's.
git log --format='%h %cs' -- lab/analysis/_inbox/ict_mnq_2026-08/PREREG_LEGB.md | tail -1
git log --format='%h %cs' -- lab/analysis/_inbox/ict_mnq_2026-08/RESULTS_LEGB.md | tail -1

# No K bound, no manifest opened (expect 0):
ls discovery_manifests/ | grep -icE "wlegb|legb"

# Archived detectors byte-identical -- this probe reuses, never edits:
git --no-pager diff HEAD -- lab/archive/ict_cascade_2026-06-18/

# The inherited object must still be the locked one (expect EMA_LEN = 20):
grep -n "^EMA_LEN" lab/analysis/_inbox/ict_mnq_2026-08/build_w_export.py

# The two-leg scope statement this probe exists to close (expect the leg-b sentence):
grep -n "leg b" lab/archive/ict_cascade_2026-06-18/PREREG-W.md

# The 1H placebo precedent that makes the placebo primary (expect 0.5485):
grep -n "0.5485" lab/analysis/_inbox/ict_mnq_2026-08/RESULTS_1H_1M.md
```

---

## Amendment log (append-only)

- **2026-08-04 — RATIFIED/FROZEN** on this file's introducing commit. No conditional hit rate
  existed at freeze. The strategy-free design (§1) was chosen **before any measurement**, as a
  consequence of the F2-guard Rule-0 read, not in response to a result.
