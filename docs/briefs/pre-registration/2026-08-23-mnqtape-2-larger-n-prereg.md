# MNQTAPE-2 — large-trade aggressor imbalance on MNQ's own tape → same-session continuation: fresh, larger-N replication window (successor to MNQTAPE-1's underpowered near-miss)

**Status:** **FROZEN — PROPOSED. No GO given.** This document is authored and frozen before any
CONFIRM-grade byte is read. The only things touched this session are (a) a real, $0
Databento cost **dry-run** on the new window (metadata-only per Rule 1 — never bills, §3), and (b)
text-only dedup/window-collision greps against already-committed repo files. **No pull. No test. No
spend. No operator authorization exists yet for anything beyond reading this document.**
**Campaign tag:** `MNQTAPE-2` — a **new** campaign, banking a **fresh** `K_intrinsic = 1` (not a
continuation of `MNQTAPE-1`'s own already-(pending-)banked slot). Reasoning in §6 — read before
assuming this is "the same trial, more data."
**Route:** Avenue A **Route B** (generate→confirm), per
[ADR 2026-08-05](../../adr/2026-08-05-avenue-a-generate-confirm-route.md) (re-verified `Accepted`
this session, §10). No admitted survivor ties this cell; Route A remains unavailable.
**Authored:** 2026-08-23 · Claude Code, at operator commission (drafting only — no data pulled, no
test run, per explicit instruction).
**Mechanism id (for `scripts/instrument_profiles.py cell`):** none of the registered MNQ cells names
this construction (carried over unchanged from `MNQTAPE-1`). **Before GO, the operator or executing
session must run** `python scripts/instrument_profiles.py cell MNQ order-flow-depth-imbalance` (the
nearest registered id) **and** re-grep `discovery_manifests/` fresh — this freeze is not a substitute
for that door-check at execution time.

---

## §0 — Rule-0 reads (this session, real anchors — verify unmoved before GO)

| Source | Anchor | Supplies |
|---|---|---|
| [`docs/briefs/pre-registration/2026-08-22-mnq-tape-imbalance-prereg.md`](2026-08-22-mnq-tape-imbalance-prereg.md) (`MNQTAPE-1`) | **untracked, session-local** (`git status` shows `??`; no commit exists) | The frozen S1–S13 construction this document inherits **byte-for-byte** (§2 below); its own real Stage-G EXPLORATION result (see next row); its own §8 authorization history (Design GO + EXPLORATION GO given 2026-08-23 in chat, CONFIRM spend GO never given) |
| `lab/analysis/c1/mnqtape1_power_check_2026-08-23/RESULTS.md` | **untracked, session-local** (no commit; a scratchpad-anchored apparatus check per its own §5) | The real Stage-G artifact it reused (`n_usable=126`, `rho_observed=+0.07514`, `p_emp=0.2054`, missed the loose `p<0.20` screen by 11/2000 draws, `PROMOTE=False`) and its own quantitative finding: **empirical power of that screen at the observed magnitude is only ≈49.9% (N=126)** — a near-coin-flip, so the near-miss cannot discriminate "real, modest effect" from "nothing" on its own; a likelihood-ratio read (~1.46:1) and a median-`p_emp` match both lean weakly toward "real, modest, underpowered" over "noise." **This is the finding this entire document exists to act on.** |
| [`ops/instruments/MNQ.md`](../../../ops/instruments/MNQ.md) §K_BANKED | `1e40b11` | Live reconciled `K_banked(MNQ) = 21` (2026-08-18). Per `MNQTAPE-1` §11, its own EXPLORATION GO + real (scratchpad) Stage-G ABANDON *should* move this to 22 on proper intake — but **no `discovery_manifests/mnqtape*.json` exists and no closure doc exists**, so by the letter of "re-read `discovery_manifests/` at admission," `MNQTAPE-1`'s own +1 is still **owed, not yet reconciled**, as of this freeze. Disclosed, not this document's obligation to fix (§6). |
| [`docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md`](../../adr/2026-08-04-family-k-bank-disclosure-not-gate.md) | `66083395ccedbfd74625d3097d8640a85d7304e8` | `K_eff = K_intrinsic` only; family bank is mandatory **disclosure**, never a gate — governs §6's K-accounting call |
| `discovery_manifests/burned_segments.json` | `fcb4ac7` | **MNQ 2025-09-01 → 2026-08-05 is BURNED** — shared `CON-2/3/4/5` reserved CONFIRM window, spent under a U1 override; "a second consultation is forbidden regardless of which CON-class campaign proposes it." Confirms, independently of `MNQTAPE-1`'s own table, that essentially the entire trailing year is spoken for by *someone's* reservation. |
| `lab/analysis/c1/mnq_sizediv_blind_2026-08/{DESIGN_FREEZE,STAGE1_DIAG,STAGE2_FALSIFIER}.md` (`MNQ-SIZEDIV-1`) | `e10e5f8` | **A finding this session's own sweep surfaced that `MNQTAPE-1`'s own dedup did not.** `MNQ-SIZEDIV-1` (frozen 2026-08-15, **before** `MNQTAPE-1`) declares `MNQ.v.0` **2024-08-14 → 2026-08-14 "virgin to all selection and evaluation until the Stage-3 battery"** — a reservation that fully **contains** `MNQTAPE-1`'s own proposed (never-executed) CONFIRM window, 2025-05-01→2025-07-31. No harm resulted (that window was never pulled), but the miss is disclosed here rather than silently repeated. **Also found:** `STAGE2_FALSIFIER.md` shows this candidate already **KILLED** on its TRAIN semester (2026-08-15: mean signed gross −2.06 bp ≤ the +0.911 bp F1 floor; F2 and F3 also fired) — per its own §5 ("no retune revive"), it will never reach Stage 3, so its CONFIRM reservation is very likely moot. No closure doc formally releases it, so this campaign routes around it anyway (§3), out of caution rather than adjudicating an ambiguous release. |
| [`docs/briefs/pre-registration/2026-07-26-st-eh-1-preregistration.md`](../2026-07-26-st-eh-1-preregistration.md) (`ST-EH-1`) | `027a729` | **A second reservation this session's sweep found.** MNQ **is** one of ST-EH-1's own two candidate instrument families. Its own design reserves **2024-01-01 → present** as a holdout ("reserved-holdout discipline... 2024-01-01→present per-cell numbers absent from every table... all phases"), with its own IS/flag read spanning each instrument's panel start → 2023-12-31. Different schema (`ohlcv-1m`/15m bars, Supertrend signal) and a different mechanism entirely from this campaign's tape-aggressor construction — per precedent (below), an unrelated-mechanism bar-level campaign does not burn a tbbo-schema window — but its **reserved** (not merely already-read) 2024-01-01+ boundary is treated with the same courtesy `MNQTAPE-1` gave the OFCHAN/R2\* reserved window, out of caution. |
| **`lab/archive/mnq_orderflow_probe_2026-08-04/{PREREG,RESULTS}.md`** (`MNQFLOW-1`) | `027a729` | DEAD 2026-08-05, unchanged from `MNQTAPE-1`'s own citation: 10-level book-size imbalance → next-minute mid return, `NQ.v.0` `mbp-10`, 3 days, ρ=−0.01205, p_emp 0.633 |
| **`docs/briefs/closures/Q-OFCHAN-1-closure-void-coverage.md`**, **`Q-R2AGRUN-1-closure-ambiguous-hold.md`**, **`Q-R2VBUCK-1-closure-falsified.md`**, **`Q-R2FLOW-1-closure-falsified.md`** | `027a729` (all four) | Unchanged from `MNQTAPE-1`'s own citation — the four-cell adverse-prior lineage, all Route-B `tbbo`/`MNQ.v.0`, all dead at Stage-G, none ever reaching CONFIRM. Re-verified this session (§10) that all four still name **"new mechanism / new G0"** as their re-proposal bar. This document does not reopen any of them; it inherits `MNQTAPE-1`'s own already-adjudicated claim to sit outside that bar (§6). |
| [`.claude/skills/databento-data/SKILL.md`](../../../.claude/skills/databento-data/SKILL.md) | `027a729` | Rule 1 (estimate before every pull, always free — executed in full this session, §3); Rule 2 (coarsest schema — `tbbo`, unchanged, inherited from `MNQTAPE-1`'s own S2 reasoning); $125/team free-credit line — **this campaign's real quote exceeds it** (§3, disclosed not smoothed over) |
| [`.claude/skills/futures-anomaly-discovery/SKILL.md`](../../../.claude/skills/futures-anomaly-discovery/SKILL.md) | `3c6745a` | K discipline; "discovery outputs are candidates, not signals" |
| [`docs/adr/2026-06-16-rule-2-budget-before-acting.md`](../../adr/2026-06-16-rule-2-budget-before-acting.md) | `d060698` (working tree carries an uncommitted local addition beyond this anchor as of this session — read the committed text, not assumed to be stale) | "Budget before acting" — the real, non-trivial spend in §3 is an operator financial decision, not a formality |
| `lab/databento_fetch/db_fetch.py` | `027a729` | The `estimate` CLI actually invoked in §3 (metadata endpoints only, never bills) |

**Dedup attestation (executed, not an empty-grep-is-evidence trap):**

```bash
rg -n -i "\baggressor\b|signed.?trade|\bCVD\b|order.?flow.?imbalance|\bOFI\b|LTI_norm|large.?trade.?continuation" \
  docs/briefs/ docs/briefs/closures/ ops/instruments/MNQ.md discovery_manifests/
```

This re-surfaced the same `OFCHAN → R2AGRUN → R2VBUCK → R2FLOW` lineage `MNQTAPE-1` already read in
full, plus `MNQ-SIZEDIV-1`, `Q-CAPFLOW-1`/`Q-CAPRES-2` (OR-window net signed aggressor → ORB trade R
— a different target entirely, same-day OR-to-trade not AM-to-PM session split), and the M2K
aggressor-flow ruling (different instrument). **No exact duplicate of the frozen LTI_norm/r_pm
construction exists anywhere in the estate.** The load-bearing new information from this sweep is
not "a duplicate exists" — it is the two reservation windows in the table above that `MNQTAPE-1`'s
own (narrower) dedup terms did not surface, both of which this document's own window choice (§3)
routes around.

---

## §1 — The named mechanism (inherited unchanged from `MNQTAPE-1` §1 — cited, not restated)

Identical to [`MNQTAPE-1` §1](2026-08-22-mnq-tape-imbalance-prereg.md#§1--the-named-mechanism-constructed-after-the-agent-is-named-per-standing-discipline):
options market-maker/dealer desks, short-gamma-dominant regime, pro-cyclical delta-hedging carried
disproportionately by large, urgent, marketable orders, predicting **same-day continuation** (not
mean-reversion) from morning flow into the afternoon. **Nothing in this section is retuned, extended,
or reinterpreted.** The only change this document makes anywhere is the calendar window the
construction is measured on (§3).

---

## §2 — Frozen construction (inherited unchanged from `MNQTAPE-1` §2 — `K_intrinsic = 1`, no sweep)

Every element below is **byte-identical** to `MNQTAPE-1`'s own frozen S1–S13. This section restates
only the element **labels** as a navigational aid; the full operational text (classification rule,
exact predictor/target formulas, roll-handling precedent) lives solely in
[`MNQTAPE-1` §2](2026-08-22-mnq-tape-imbalance-prereg.md#§2--frozen-construction-single-cell-k_intrinsic--1-no-sweep)
and is **cited, not copied** — restating it wholesale here would create a second, driftable copy of a
frozen object, exactly the failure `MNQTAPE-1`'s own single-source-of-truth discipline exists to
prevent.

| # | Element | Status here |
|---|---|---|
| S1 | Instrument/symbology: `MNQ.v.0` continuous | unchanged |
| S2 | Schema: `tbbo` | unchanged |
| S3 | Session: RTH 09:30–16:00 ET, split at 12:00 ET | unchanged |
| S4 | Aggressor classification: Lee & Ready 1991, quote rule + tick-rule fallback | unchanged |
| S5 | Size filter: large trade = size ≥ 10 contracts, frozen a priori | unchanged — **not** re-examined against this new era's own trade-size distribution (a disclosed limitation, §3) |
| S6 | Predictor: `LTI_norm(s)` over 09:30–12:00 ET | unchanged |
| S7 | Target: `r_pm(s) = ln(P_16:00/P_12:00)` | unchanged |
| S8 | Predicted sign: positive (continuation) | unchanged |
| S9 | Statistic: Spearman ρ(`LTI_norm`, `r_pm`) | unchanged |
| S10 | Null: permutation of session-date pairing | unchanged |
| S11 | Permutation parameters: M = 2,000, **seed = this freeze's date** | **M unchanged (2,000). Seed re-derived under the identical rule** ("seed = this freeze's date," `MNQTAPE-1` S11) → **`20260823`** for this document, not a retune of S11 — S11 was always a date-derived rule, never a magic literal, and reusing `20260822` across a different window would itself violate the "never reuse a seed across a different apparatus" precedent the power-check itself set (its own base seed `20260823` vs. the original `20260822`) |
| S12 | p-value: one-sided `p_emp = (1+#{ρ_null≥ρ_obs})/(M+1)` | unchanged |
| S13 | Roll handling: exclude sessions with a front-month volume-lead change | unchanged (rule); the specific dates differ by construction — this window's own roll dates are unknown until pulled (§3, §7 Step 0) |

**Forbidden inside the cell (frozen, no exceptions, unchanged from `MNQTAPE-1`):** a second size
threshold; a second session split time; a second horizon; an ES/NQ/YM sibling; conditioning on ORB
timestamps, day-of-week, or realized volatility; reading this document's own CONFIRM-window bytes
before the operator Pull-spend GO (§8) fires.

---

## §3 — Data, cost, and the new window (the only thing this document changes)

### 3.1 Why every window `MNQTAPE-1` named or implied is unavailable

| Window | Owner | Status |
|---|---|---|
| 2026-02-06 → 2026-08-06 | `MNQTAPE-1` EXPLORATION | **Already read**, real data, real (near-miss) result — reusing it is not "fresh," it is the exact forbidden move this document's own §9 names |
| 2025-08-06/09-01 → 2026-02-06 | OFCHAN/R2\* lineage | **Reserved holdout**, explicitly barred by `MNQTAPE-1` §9 and re-barred here |
| 2025-09-01 → 2026-08-05 | `burned_segments.json` (CON-2/3/4/5) | **Burned**, cross-campaign, independent of mechanism family |
| 2025-05-01 → 2025-07-31 | `MNQTAPE-1`'s own proposed (never-executed) CONFIRM | Technically never pulled, but **fully contained inside** `MNQ-SIZEDIV-1`'s own 2024-08-14→2026-08-14 "virgin to all selection" reservation (§0) — reusing it here would repeat a collision `MNQTAPE-1`'s own (narrower) dedup missed |
| 2024-08-14 → 2026-08-14 | `MNQ-SIZEDIV-1` CONFIRM | **Reserved** (very likely moot post-KILL, §0, but not formally released) |
| 2024-01-01 → present | `ST-EH-1` reserved holdout | **Reserved** (different mechanism, but a live, explicit reservation this campaign routes around out of caution) |

Stacking these: essentially **the entire 2024-01-01 → 2026-08-23 span is spoken for**, by at least
one live or recently-live reservation, independent of `MNQTAPE-1`'s own narrower "OFCHAN/R2\* only"
framing. A genuinely fresh window must sit **entirely before 2024-01-01**.

### 3.2 The frozen window

**`MNQ.v.0`, `tbbo`, 2022-08-01 → 2023-08-01** (12 calendar months; `--end` exclusive per this repo's
own CLI convention, so the last included session is 2023-07-31).

- **Clear of every reservation in 3.1** with a comfortable buffer (ends two weeks before
  `MNQ-SIZEDIV-1`'s own TRAIN start of 2023-08-14, so it does not even touch that campaign's
  already-read-with-outcomes data, let alone its reserved CONFIRM).
- **Inside the native-micro era** (MNQ launched 2019-05-06, per the databento-data skill's own Rule
  4) with over three years of accumulated liquidity maturity by August 2022 — not the thin early-launch
  period.
- **Overlaps only with unrelated-mechanism bar-level campaigns' already-read (non-reserved) IS
  windows** (`ST-EH-1`'s own 2019-05-06→2023-12-31 IS/flag reads on `ohlcv-1m`; several
  `ohlcv-1m`/multi-year bar catalogues). Per the same precedent `MNQTAPE-1` itself relied on when it
  chose 2025-05→07 despite that window also sitting inside several bar-level campaigns' spans — a
  different mechanism family, on a different (coarser) schema, does not burn a `tbbo`-schema
  order-flow window. This is stated as a claim following established precedent, not re-litigated from
  scratch.
- This repo's local `core/data/bar_data/MNQ_M15.csv` (vendor-licensed, gitignored per CLAUDE.md's
  public-clone posture) is **not present in this worktree**, so no local recount of exact session
  dates was possible from here; **N is estimated, not measured, until pulled** (§3.3, §7 Step 0) —
  the same honest hedge `MNQTAPE-1` itself used ("exact count confirmed only once the calendar is
  pulled").

### 3.3 Real cost dry-run (executed this session, $0, no pull — Rule 1)

```bash
PYTHONPATH=lab python -m databento_fetch.db_fetch estimate \
  --symbols MNQ.v.0 --stype continuous --schema tbbo \
  --start 2022-08-01 --end 2023-08-01 --phase oos --campaign-id MNQTAPE-2-confirm
```

**Real output, this session, 2026-08-23:**

```
[estimate] cost      : $308.6934 USD (streaming)
[estimate] billable  : 11,837,751,680 bytes  (~11.8378 GB)
[estimate] records   : 147,971,896
```

**$308.6934 is the real, quoted, load-bearing figure for this window.** Sanity check against
`MNQTAPE-1`'s own real quote: its 3-month window (2025-05→07) priced at $82.2270 for ~62 sessions;
this 12-month window (4× the calendar span) prices at ~3.75× that figure — same order of magnitude,
sub-linear (consistent with differing trade-volume regimes across the two eras, not a red flag).
**Second correction, carried forward from `MNQTAPE-1`'s own standing caution:** entitlements move
(rolling free-year windows, consumption) inside weeks — `MNQTAPE-1` itself watched a $0.00 six-month
EXPLORATION quote (2026-08-06) sit beside an $82.23 three-month CONFIRM quote (2026-08-22) sixteen
days later, on different windows. **Treat $308.69 as a ballpark anchor from this exact freeze date,
not a permanent quote.** Rule 1 is not optional: re-run this exact `estimate` command immediately
before any Pull-spend GO (§8, §10).

**Budget disclosure (real money, stated plainly).** $308.69 **exceeds** the $125/team free-credit
line by $183.69 — unlike `MNQTAPE-1`'s ~$82 CONFIRM, which fit inside that line whole. This is not a
formality: an operator GO on this document is a GO on spending real dollars beyond the team's free
allotment (or on whatever remains of it — this document does not attempt to reconstruct the live
running balance across every other campaign's spend; re-check that balance fresh at GO time, per the
standing "never trust a snapshot" discipline). The unrelated $700 c1-rail execution ceiling does not
apply here and is not being drawn against.

### 3.4 Estimated session count and roll exposure (estimate, not measurement)

~261 raw weekdays in the 12-month span, less an estimated ~9 CME full-day RTH closures (New Year's
Day, Good Friday, Memorial Day, Independence Day, Labor Day, Thanksgiving, Christmas, etc.) →
**N ≈ 252 RTH sessions**, before any S4 (`no_rth_trades`) or S13 (roll-date) exclusions. `MNQTAPE-1`'s
own 3-month window realized 126 pre-roll-exclusion sessions against a raw-weekday count of ~65 (a
~3% dropout rate for `no_rth_trades`) plus 2 roll exclusions in 6 months; scaling that same dropout
and roll rate to 12 months gives an estimated **N_usable ≈ 240–250**, with **~4 roll-affected
sessions** expected (quarterly futures roll cadence: ~4 rolls/year vs. `MNQTAPE-1`'s 2 in 6 months).
**These are estimates for planning purposes only — the real census runs at §7 Step 0, at $0, before
any tbbo spend.**

---

## §4 — Cost-law pre-screen engagement (inherited unchanged from `MNQTAPE-1` §4 — cited, not restated)

Identical reasoning to
[`MNQTAPE-1` §4](2026-08-22-mnq-tape-imbalance-prereg.md#§4--cost-law-pre-screen-engagement-per-standing-discipline-not-skipped):
the MR/fade cost-law pre-screen does not fire (this is a continuation claim, not MR/fade); the
general "price the trade construction before building" discipline does not apply because
`LTI_norm`/`r_pm` remain a pure statistical-association test, not a strategy — no entry, stop,
target, or per-trade cost is defined here or anywhere in this lineage. **If, and only if,** this cell
(or `MNQTAPE-1`'s own, separately) reaches `SURVIVOR`, the follow-on strategy-construction campaign
inherits `ops/instruments/MNQ.md` **N6** (modern MNQ 4× cost hurdle ≈3.01 bp/session) as a mandatory
Harvest Requirement-5 gate. Forward-owed, not discharged, not evaded — unchanged from `MNQTAPE-1`.

---

## §5 — Falsifiable hypothesis

**H (`MNQTAPE-2`):** on the frozen one-cell catalogue in §2, measured **once**, on the frozen window
in §3.2 (2022-08-01→2023-08-01), `ρ(LTI_norm, r_pm) > 0` with one-sided `p_emp < 0.05` (M=2,000,
seed 20260823) **and** `|ρ| ≥ 0.20`. **This decision rule is byte-identical to `MNQTAPE-1`'s own §5**
— alpha and the effect-size floor are not retuned, only the window changes (per this document's own
governing constraint).

**H fails** if the read shows the wrong sign, `p_emp ≥ 0.05`, or `|ρ| < 0.20` — any one limb failing
is `FALSIFIED`, not partial credit. `AMBIGUOUS-HOLD` if `N_usable < 120` (§7).

### 5.1 Power, computed at freeze (Fisher-z, one-sided α=0.05, SE = 1/√(N−3))

**Primary table — N ≈ 252 (this document's own proposed window):**

| True ρ | z(ρ) = atanh(ρ) | z·√(N−3) | Power |
|---|---|---|---|
| 0.075 (≈ `MNQTAPE-1`'s own observed magnitude) | 0.0751 | 1.185 | ≈**0.323** |
| 0.10 | 0.1003 | 1.583 | ≈**0.475** |
| 0.15 | 0.1511 | 2.385 | ≈**0.770** |
| 0.20 (the confirm floor) | 0.2027 | 3.199 | ≈**0.940** |
| 0.25 | 0.2554 | 4.030 | ≈**0.999** |
| 0.30 | 0.3095 | 4.885 | ≈**>0.999** |
| 0.35 | 0.3654 | 5.771 | ≈**>0.999** |

**Comparison table — same decision rule (p<0.05, |ρ|≥0.20 bar), three sample sizes, Fisher-z
throughout** (the N=126 column is a **hypothetical**, applying the CONFIRM-grade bar retroactively to
Stage-G's actual realized N, for comparison only — Stage-G itself used the looser p<0.20 screening
gate, a different, already-published table in the power-check, not this one):

| True ρ | N=62 (`MNQTAPE-1`'s own CONFIRM design) | N≈126 (Stage-G's actual N, hypothetical CONFIRM-grade bar) | N≈252 (this document) |
|---|---|---|---|
| 0.075 | 0.143 | 0.209 | 0.323 |
| 0.10 | 0.191 | 0.297 | 0.475 |
| 0.15 | 0.314 | 0.513 | 0.770 |
| 0.20 | 0.465 | 0.727 | 0.940 |
| 0.25 | 0.624 | 0.883 | 0.999 |
| 0.30 | 0.768 | 0.963 | >0.999 |
| 0.35 | 0.878 | 0.992 | >0.999 |

**Reading this honestly.** At the exact magnitude `MNQTAPE-1` actually observed (ρ≈0.075), this
window roughly **doubles to 2.3×'s** the power of the original CONFIRM design (14.3%→32.3%) and is a
genuine, meaningful improvement — but it is **not** close to conventional 80% power at that specific
magnitude. Solving the same Fisher-z equation for **N at 80% power, ρ=0.075**:
`√(N−3) = (1.645+0.8416)/0.0751 ≈ 33.1` → **N ≈ 1,099 sessions (≈4.3 years)**. Extrapolating this
session's own measured $308.69/year rate linearly gives a **rough estimate of ~$1,300–1,400** for
that window — **stated as an estimate, not a quotation, and not proposed here.** This document
instead targets a **bounded, cost-proportionate** improvement: ≥77% power at ρ=0.15 (the upper end of
the range the power-check's own §4.3 interpretation judged more plausible than the confirm floor
itself) while roughly doubling power across the whole 0.075–0.20 band relative to the original design
— a disclosed, deliberate compromise between power and real spend, not a claim that this window fully
resolves the near-miss. **If this campaign itself lands ambiguous, a still-larger third window is a
question for its own future pre-registration, its own K, its own operator GO — not decided here**
(§9).

---

## §6 — Why this is a new campaign (banking fresh K), not an extension of `MNQTAPE-1`

**Verdict: new campaign, `K_intrinsic = 1`, fresh.** Reasoning, for the operator to weigh (matching
this repo's convention of putting genuinely load-bearing scope calls to the GO mark rather than
self-certifying them):

1. **`MNQTAPE-1` is formally closed, not paused.** Its own frozen §7 gate states: "Any limb failing ⇒
   ABANDON, $0 spent, no CONFIRM read, **campaign closes**." The real Stage-G result (§0) failed limb
   (c) — `p_emp = 0.2054 ≥ 0.20`. There is no "still-open `MNQTAPE-1`" to extend; it is dead by its
   own rule, exactly like the four `OFCHAN`/`R2*` cells before it.
2. **The K-bank ledger treats a closed campaign's slot as spent, not returned.** `MNQTAPE-1` §11:
   "If the operator GO(s) in §8 are given and the campaign opens, it banks `K_intrinsic=1` and, on
   closure, `K_banked(MNQ)` moves 21→22 **regardless of verdict**." The EXPLORATION GO **was** given
   and Stage-G **did** execute and close (as ABANDON) — that slot is consumed (pending only a
   mechanical ledger reconciliation, §0), independent of whether CONFIRM ever ran. A fresh,
   independently-billed, independently-verdictable statistical look is a **separate** opportunity for
   a false positive under the family's own disclosed multiplicity accounting, which is precisely what
   the K-bank exists to count.
3. **Precedent distinguishes a same-sample re-score from a new-sample replication.** `ops/instruments/MNQ.md`
   §N-row for `MNQSR-1` states its seed-fixed re-score "`...20260806b` is the RESULTS pin (same
   14-cell construct as `20260806`, **not a second campaign**)" — because it re-ran the *identical*
   construct on the *identical* data for reproducibility. This document does the opposite: identical
   construct, **entirely disjoint data**. That is a replication in the ordinary scientific sense, not
   a re-score, and this repo's own K-bank philosophy (ADR 2026-08-04: disclosure of every real
   selection/spend event) treats it as its own event.
4. **`MNQTAPE-1` itself set the operative precedent for "closed cell + any further work = new
   campaign, new K," even for higher similarity than this.** When `MNQTAPE-1` proposed testing what
   was arguably "the same broad modality" as the closed `OFCHAN`/`R2*` lineage, it minted a **brand
   new** campaign tag and K rather than reopening a closed R2\* cell, on the strength of a named
   agent, population, and horizon difference (its own §6). This document's relationship to
   `MNQTAPE-1` is **more**, not less, similar than that (the statistic is literally byte-identical) —
   if anything, the case for "new campaign" is at least as strong here, not weaker.
5. **A freshly-authored, freshly-dated document responding to new information (the power-check, which
   did not exist at `MNQTAPE-1`'s freeze time) is this repo's own definition of a new campaign** — a
   new `register_search open` event, a new manifest, its own operator GO.

**Naming: `MNQTAPE-2`, not a new descriptive name, not a "-B"/"-CONFIRM" suffix.** The `R2*` family
(`R2AGRUN`/`R2VBUCK`/`R2FLOW`) used distinct descriptive names, not sequential numbers, specifically
**because each tested a different statistic** under a shared "R2" umbrella — a numeral there would
have obscured that the construct itself had changed. Here the construct has **not** changed at all;
only the window has. A numeral suffix (`-2`) is the more accurate signal: it tells a future reader
"same design as `MNQTAPE-1`, attempt 2, fresh data" at a glance, is immediately dedup-discoverable
alongside `MNQTAPE-1` by the same search terms, and does not misleadingly imply a new mechanism the
way inventing an unrelated name would. This matches the task's own suggested default and this
document adopts it after considering the alternative.

**K-bank disclosure on opening (mechanical, disclosure-only, per ADR 2026-08-04 — re-read fresh, not
from this snapshot):** `K_banked(MNQ)` is currently tracked at **21** in `ops/instruments/MNQ.md`
(reconciled 2026-08-18); `MNQTAPE-1`'s own pending +1 is owed but unreconciled (§0). This campaign's
own opening (on operator GO + intake) banks its **own** `K_intrinsic = 1`, landing the family figure
at **22 or 23** depending on which reconciliation lands first at that time — this document does not
resolve that ordering and does not treat either number as fixed.

---

## §7 — Frozen procedure and gate (single-stage design — a disclosed departure from `MNQTAPE-1`'s
Stage-G/CONFIRM split, reasoned below, not a change to the statistical construction)

**Why single-stage, not Stage-G→Stage-C.** `MNQTAPE-1`'s two-stage split existed to exploit a **free**
cache-reuse EXPLORATION window (borrowed from the unrelated OFCHAN campaign) before committing real
money to a separate, paid CONFIRM window. This campaign has **no** analogous free window — every
`tbbo` byte on the frozen window costs real money (§3.3). Splitting this document's own scarce,
paid-for window into a cheap "screen" sub-window and a smaller "confirm" sub-window would (a) pay for
`tbbo` bytes twice under two different labels, and — more importantly — (b) **fragment the very N
this campaign exists to grow**, reproducing in miniature the exact underpowering problem the
power-check diagnosed in `MNQTAPE-1`'s own screen. A second underpowered screen ahead of an even
smaller confirm would not fix the near-miss; it would manufacture another one. This is therefore a
**single pre-registered pull, one binding statistical test, scored once** — a procedural
(operational) adaptation to the changed cost structure, not a retune of any S1–S13 element (§2), which
remain untouched.

| Step | What happens | Gate (frozen) |
|---|---|---|
| 1. Operator **Design GO** | Sign-off on this document as designed | mechanical |
| 2. **Step 0 — data-integrity census ($0, `ohlcv-1d`, `MNQ.v.0`, 2022-08-01→2023-08-01)** | Count full RTH session-days present; identify front-month volume-lead change dates for S13 exclusion; confirm no wholesale data gaps. **No price, return, or aggressor-side value is read or joined to anything — calendar/coverage only**, matching `MNQ-SIZEDIV-1`'s own precedent for an outcome-free pre-flight | `HALT` (data defect, `NEEDS_CONTEXT` to operator) iff full-session count is implausibly low (< 230, i.e. > 8.7% missing relative to the §3.4 estimate) or the roll-date count is wildly inconsistent with the ~4-per-year expectation. Passes silently otherwise — **this is a data-quality gate, never a directional or statistical read**, and cannot itself promote or kill the hypothesis |
| 3. Operator **Pull-spend GO** | Separate, explicit sign-off on the real `tbbo` cost (§3.3; **re-estimate immediately before this GO**, Rule 1) | mechanical |
| 4. **The single CONFIRM-grade pull + score** | `tbbo` pull on 2022-08-01→2023-08-01; compute `LTI_norm`/`r_pm` per S1–S13 exactly (§2); Spearman ρ + one-sided permutation p (M=2,000, seed 20260823, S11) | `SURVIVOR` iff `ρ > 0` **and** `p_emp < 0.05` **and** `\|ρ\| ≥ 0.20`; `FALSIFIED` if any limb fails; `AMBIGUOUS-HOLD` if `N_usable < 120` (≈48% of the §3.4 estimate, proportional to `MNQTAPE-1`'s own 30/62≈48% threshold — report census, do not extend the window without a fresh freeze) |
| 5. Disposition | `SURVIVOR` → hands to `strategy-validation` as a **footprint candidate**, explicitly not a strategy (§4); N6 cost-hurdle owed before any construct. `FALSIFIED`/`AMBIGUOUS-HOLD` → DEAD-list/disclosed-hold row on `ops/instruments/MNQ.md` under the same mechanism id `MNQTAPE-1` would have used (e.g. `aggressor-large-trade-continuation`); re-proposal bar = **new mechanism**, not a third window-only retry (§9) | frozen |

---

## §8 — Outstanding authorizations (nothing granted by this document)

1. **Design GO — NOT GIVEN.** This document is frozen and proposed only. No operator sign-off exists
   for anything in it.
2. **Pull-spend GO — NOT GIVEN, and cannot be requested before Step 0 (§7) completes at $0.** The
   ~$308.69 (pending re-estimate at GO time) real-dollar `tbbo` spend requires its own separate,
   explicit authorization, weighed against the live $125/team credit-line balance (§3.3) — this is
   real money exceeding that line, not a formality, and per Rule 2 ("budget before acting") it is
   requested, never assumed.
3. **No data has been pulled. No test has been run. No `register_search` has been opened. No K has
   been banked.** Only the $0 Databento cost-estimate (§3.3, already executed and quoted above) and
   this session's own text-only dedup/window sweeps (§0) have occurred.

---

## §9 — Forbidden moves

- **Treating a pass or fail on this document's own CONFIRM read as license to reopen or relitigate
  `MNQTAPE-1`'s own already-closed EXPLORATION verdict (`PROMOTE=False`, ABANDON).** That verdict
  stands, on its own window, under its own frozen gate, permanently. This document's result — whatever
  it turns out to be — is evidence about the *underlying hypothesis*, not a retroactive re-grade of a
  different, already-adjudicated statistical test on different data.
- **Informally pooling this document's CONFIRM-grade result with `MNQTAPE-1`'s own Stage-G N=126
  result** (e.g., combining p-values, computing a meta-analytic ρ, or quoting a "combined N=378") to
  manufacture apparent power neither test alone has. Any such pooling would need its **own**,
  separately pre-registered meta-analytic method declared before either result is inspected together
  — retrofitting one after seeing both p-values is a forking-paths trap this document explicitly bars.
- Reading any byte of the frozen 2022-08-01→2023-08-01 window before the operator Pull-spend GO fires
  (§8) — the ordering trap Route B exists to prevent, unchanged from `MNQTAPE-1`.
- Retuning the ≥10-contract threshold, the 09:30/12:00/16:00 ET boundaries, M, the alpha (0.05), or
  the effect-size floor (0.20) after seeing **any** result from this window (Trap #12/FM-9, unchanged).
- Retuning the permutation seed away from the "freeze-date" rule (S11) after seeing any result — the
  rule, not a specific past literal, is what is frozen (§2).
- Choosing a **different** window after this one produces an unwelcome result ("window-shopping") —
  if this campaign lands `FALSIFIED` or `AMBIGUOUS-HOLD`, the re-proposal bar is a **new mechanism**,
  not a third disjoint calendar slice of the identical statistic (§7 disposition).
- Reusing any window this document identified as reserved or burned (§3.1) for **any** future
  candidate on this instrument, tape-aggressor or otherwise, without a fresh check that the
  reservation has actually lapsed — this document explicitly declines to adjudicate `MNQ-SIZEDIV-1`'s
  likely-moot reservation itself (§0) and a future session should not silently inherit this
  document's caution as a permanent bar either.
- Treating a `SURVIVOR` verdict here as a deployable strategy, or as license to skip the forward-owed
  N6 cost-hurdle gate (§4) — unchanged from `MNQTAPE-1`.
- Adding a second horizon, session split, or sibling instrument without a fresh `K_intrinsic` and a
  fresh freeze — unchanged from `MNQTAPE-1`.
- Sub-5-second tradeable-claim framing, ES→MNQ/NQ→MNQ lead-lag constructs — N/A here by construction,
  stated for completeness, unchanged from `MNQTAPE-1`.
- Quoting §5's power table as already-measured evidence in either direction, or treating the
  `MNQFLOW-1`/R2\* lineage's null results as proof this cell will also fail — both overclaiming
  directions barred, unchanged from `MNQTAPE-1`.

---

## §10 — Audit hooks (runnable)

```bash
# Route B is still Accepted (re-verify before GO; a revert invalidates this entire document)
grep -n "^\*\*Status:\*\*" docs/adr/2026-08-05-avenue-a-generate-confirm-route.md
# expect: Accepted

# The adverse-prior lineage this pre-reg is judged against — re-verify the re-proposal bar unchanged
rg -n "new mechanism / new G0|new G0 / new mechanism" docs/briefs/closures/Q-OFCHAN-1-closure-void-coverage.md \
  docs/briefs/closures/Q-R2AGRUN-1-closure-ambiguous-hold.md \
  docs/briefs/closures/Q-R2VBUCK-1-closure-falsified.md \
  docs/briefs/closures/Q-R2FLOW-1-closure-falsified.md

# Family K bank — re-read fresh, never trust this document's snapshot
grep -n "K_banked(MNQ)" ops/instruments/MNQ.md

# MNQTAPE-1's own admission status — has its pending +1 landed yet?
ls discovery_manifests/ | rg -i "mnqtape" || echo "MNQTAPE-1 still not admitted through intake, as this document assumed"

# MNQ-SIZEDIV-1's reservation — still un-formally-released as this document assumed?
find docs/briefs/closures -iname "*sizediv*" 2>/dev/null || echo "no closure found; reservation status unchanged from this freeze's read"

# Mechanism door-check (nearest registered id; this construction has no id of its own yet)
python scripts/instrument_profiles.py cell MNQ order-flow-depth-imbalance

# Re-run the dedup sweep fresh — do not trust this document's own snapshot
rg -n -i "\baggressor\b|signed.?trade|\bCVD\b|order.?flow.?imbalance|\bOFI\b|LTI_norm|large.?trade.?continuation" \
  docs/briefs/ docs/briefs/closures/ ops/instruments/MNQ.md discovery_manifests/

# Step 0: the mandatory $0 data-integrity census (must run and pass before any tbbo spend proposal)
PYTHONPATH=lab python -m databento_fetch.db_fetch estimate \
  --symbols MNQ.v.0 --stype continuous --schema ohlcv-1d \
  --start 2022-08-01 --end 2023-08-01

# Fresh CONFIRM-grade estimate — MANDATORY before any Pull-spend GO, always free
PYTHONPATH=lab python -m databento_fetch.db_fetch estimate \
  --symbols MNQ.v.0 --stype continuous --schema tbbo \
  --start 2022-08-01 --end 2023-08-01 --phase oos --campaign-id MNQTAPE-2-confirm

# No procurement has happened on the back of this document (expect no manifest, no cache growth)
ls discovery_manifests/ | rg -i "mnqtape-2|mnqtape2" || echo "no manifest yet, as expected (zero K spent)"
```

---

## §11 — Registry / logging

**Not admitted through intake.** No `register_search open`, no manifest, no
`docs/briefs/INDEX.md` row, no `lab/CATALOG.md` row — matching `MNQTAPE-1`'s own standing precedent
for every pre-GO route memo and every frozen-but-unopened pre-registration in this repo. If the
operator GOs in §8 are given and the campaign opens, it banks its **own** `K_intrinsic = 1` on proper
intake (§6) — re-read `discovery_manifests/` and `ops/instruments/MNQ.md` fresh at that time rather
than trusting this document's snapshot of `K_banked(MNQ) = 21` (§0, §6).

---

## Verification

§0 cites real anchors including two reservation windows (`MNQ-SIZEDIV-1`, `ST-EH-1`) `MNQTAPE-1`'s
own narrower dedup missed, disclosed rather than silently corrected in place ✓ · §1/§2 inherit the
named mechanism and frozen construction byte-for-byte, cited not restated, with the one necessary
rule-following exception (S11's seed re-derived under its own stated rule) explicitly flagged as not
a retune ✓ · §3 names every window `MNQTAPE-1` implied or proposed and shows each is unavailable,
selects a window clear of all of them with a stated buffer, and reports a **real, executed** $0
dry-run cost ($308.6934) rather than an extrapolated guess ✓ · §4 engages the cost-law discipline by
pointer, not duplication ✓ · §5 states a byte-identical decision rule to `MNQTAPE-1`'s own H, with a
freshly-computed power table at the new N, an honest comparison table across three sample sizes, and
a disclosed, non-pursued estimate of what full resolving power at the observed magnitude would cost
✓ · §6 states plainly and reasons through why this is a new campaign (not an extension), with a
specific precedent-based naming decision offered for operator adjudication rather than
self-certified ✓ · §7 states and justifies a real procedural departure (single-stage vs. `MNQTAPE-1`'s
two-stage) as a response to the changed cost structure and the power-check's own diagnosis, explicitly
not a change to the frozen statistical construction, and adds a $0 data-integrity Step 0 ahead of any
real spend ✓ · §8 authorizes nothing — both GOs explicitly outstanding ✓ · §9 forbidden moves include
the task's own required new bar (no relitigating `MNQTAPE-1`'s closed EXPLORATION verdict) plus an
explicit anti-pooling bar ✓ · §10 runnable, including hooks that re-check this document's own
disclosed uncertainties (MNQTAPE-1 admission status, sizediv reservation release) rather than only
re-checking claims favorable to proceeding ✓ · §11 registry unchanged from standing precedent ✓ ·
**zero data pulled, zero tests run, zero dollars spent, zero K banked ✓.**
