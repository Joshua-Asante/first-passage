**Theme:** c1
# c1 signal-identity — intra-bar vs confirmed-close (2026-07-28)

**Status:** ACTIVE — **full-panel MEASURED** (2026-07-29); Q-SIGID-1 §6 offline limb = **FULL** (plan `docs/superpowers/plans/2026-07-29-c1-signal-identity-fullpanel.md`)
**Verdict (falsifier):** the 07-28 MNQ discharge bar is a **phantom**: mid-bar `longSignal`
true, confirmed-close `longSignal` **false** (`body_ok` fails). Entry ATR/stop Δ is
trivial; the threat is signal identity. Falsifier status on full run: **MEASURED**.
**Harness:** [`signal_identity.py`](signal_identity.py) · raw [`results.json`](results.json) · Phase 0 archive [`results_phase0_2026-04_2026-07.json`](results_phase0_2026-04_2026-07.json)

## §Pre-registered partitions (frozen 2026-07-29 — RUN COMPLETE)

Governance (operator lock): **FULL supersedes Phase 0 as Q-SIGID-1 §6 offline limb**; H1/H2 are diagnostic only; phantom algorithm stays Phase-0-as-is. Pinned exclusive end: **`2026-07-30` UTC**. Threshold **0.5** unchanged. Year calendar rows not emitted this harness (halves cover the diagnostic split).

| ID | Window (UTC, end exclusive) | Role | Status |
|---|---|---|---|
| **FULL** | 2019-05-06 → 2026-07-30 | Sole §6 offline measurement | **MEASURED** |
| **H1** | 2019-05-06 → 2023-01-01 | Diagnostic (chop-era) | MEASURED (non-gating) |
| **H2** | 2023-01-01 → 2026-07-30 | Diagnostic (trend-era) | MEASURED (non-gating) |
| **P0REP** | 2026-04-01 → 2026-07-28T19:00 | Exact replication of Phase 0 (15/22 MNQ, 21/30 MYM) | **PASS** (exact) |

**Warmup rule:** indicators on contiguous full series; partitions filter bar_open membership only.

### §Pull log

| Leg | Window | Cost | Records | Notes |
|---|---|---:|---:|---|
| MNQ | 2019-05-06 → 2026-07-30 | **$0.00** | 2,549,256 → `mnq_1m.parquet` | single stream OK |
| MYM | same | **$0.00** | 2,480,324 → `mym_1m.parquet` | year chunks; 2026 split H1/H2 after year-pull **504**; concat min `2019-05-06` max `2026-07-29 23:59` UTC |

Campaign: `C1-SIGID-1` / `--phase oos`.

---

## §FULL — Sole §6 offline limb (2019-05-06 → 2026-07-30)

| Leg | Session candidates | Confirmed signals | Phantoms | Phantom / candidates | **Phantoms / confirmed** |
|---|---:|---:|---:|---:|---:|
| MNQ | 12,002 | 439 | **336** | 2.80% | **0.765×** |
| MYM | 11,894 | 462 | **319** | 2.68% | **0.690×** |

Median mid-vs-confirmed stop Δ on FULL phantom bars: MNQ **−0.95 pts**, MYM **−2.29 pts**.

**vs 0.5:** both legs ≥ 0.5 → offline limb still supports `RESOLVED` after a non-VOID Fri §2b. Does **not** close Q-SIGID-1 alone (Fri still owed). Phase 0 (0.68 / 0.70) is historical appendix only.

### Diagnostic halves (non-gating)

| Partition | MNQ phantoms/confirmed | MYM phantoms/confirmed |
|---|---:|---:|
| H1 (→2023-01-01) | 130/202 = **0.644×** | 112/163 = **0.687×** |
| H2 (2023-01-01→) | 206/237 = **0.869×** | 207/299 = **0.692×** |

Stability note only: MNQ H2 higher than H1; MYM nearly flat across halves. Neither flips §6.

### P0REP (exact)

| Leg | Want | Got | |
|---|---|---|---|
| MNQ | 15 / 22 | 15 / 22 | PASS |
| MYM | 21 / 30 | 21 / 30 | PASS |

---

**What this is.** Offline quantification of Striker MYM/MNQ mid-bar vs bar-close signal
identity after the 2026-07-28 live discharge ([`RUNBOOK.md`](../../../docs/notes/rail_build/RUNBOOK.md)
§1c; Fri clean re-measure owed [`B7_STAGE1_DESK_CARD_2026-07-31.md`](../../../docs/notes/rail_build/B7_STAGE1_DESK_CARD_2026-07-31.md) §2b).

**What this is NOT.** Not tick-eval. Not a Pine edit. Not an execution-quality P1–P4 fill
study ([EQ note](../../../docs/notes/2026-07-24-execution-quality-investigation.md) already
defers Pine timing as locked-parameter axis). [`MNQ.md` W3](../../../ops/instruments/MNQ.md)
forbids claiming 1m fills an *execution* layer — the 1m walk here is **signal-flip
coarseness only**.

Reproduce (research env; **$0.00** `ohlcv-1m`, subscription-covered):

```bash
PYTHONPATH=lab python -m databento_fetch.db_fetch pull \
  --symbols MNQ.v.0 --stype continuous --schema ohlcv-1m \
  --start 2026-04-01 --end 2026-07-28T19:00 --max-cost 1.00 \
  --out lab/analysis/c1_signal_identity_2026-07-28/data/mnq_1m.parquet
# same for MYM.v.0 → mym_1m.parquet
python lab/analysis/c1_signal_identity_2026-07-28/signal_identity.py
```

Local CME `BAR_EXPORT` / `orb_mnq_2026-07/_mnq_15m.pkl` were **absent** in this environment;
Databento 1m → 15m aggregation substitutes (documented gap, not invented OHLC).

Locked params from [`nas/LOCK.md`](../../../core/strategies/nas/LOCK.md) /
[`striker/LOCK.md`](../../../core/strategies/striker/LOCK.md): lookback 15, ATR 11 / MA 85 /
expansion 0.28, minBody 0.38, SL 1.20×ATR; session 13–17 UTC; MNQ Mon/Tue, MYM Tue/Fri.

---

## §1 — Cheap falsifier (07-28 MNQ bar `bar_time` = 15:45 UTC open)

| Claim | Measured |
|---|---|
| Operator confirmed C | **28,048.50** |
| Databento aggregated 15m C | **28,048.50** (Δ 0.00 vs operator) |
| Live `parsed.close` | **28,051.50** (Δ **+3.00** vs confirmed) |
| `rawBreakout` at confirmed C (`C > highestHigh[1]`) | **TRUE** (28,048.50 > 28,035.00) |
| `longSignal` at confirmed C | **FALSE** — **`body_ok` FALSE** (other limbs true) |
| `stop_dist` at confirmed C (`atr * 1.20`) | **126.850** |
| Live `stop_dist_pts` | **126.75** |
| Δ stop (live − confirmed) | **−0.100 pts** → **−$0.20 / contract** |

**Binary answers the plan required:**

1. At confirmed C, is `rawBreakout` still true? **YES.**
2. What is confirmed `atrVal * stopAtr` vs live 126.75? **126.850 vs 126.75** — sizing
   delta is negligible.

**Load-bearing clarification:** close-mismatch **proves mid-bar fire**. Entry
`stop_dist_pts = atrVal * stopAtr` (ATR mid-bar), **not** `f(close)`. The 07-28
threat is **not** the $0.20 stop delta — it is that **`longSignal` was true mid-bar and
false at the confirmed close** (`body_ok` failed as the bar finished). Add/exit payloads
remain fully close-dependent (`close - currentStop`).

**1m path (coarse):** forming-bar `longSignal` first true at **15:46** UTC (1m close
28,049.00, body_ok true); confirmed close body_ok false. Live `parsed.close` 28,051.50
does **not** appear as any 1m close (nearest 28,050.00 / 28,053.75) — tick-level fire
inside a minute, exactly the resolution W3 says 1m cannot claim.

**07-28 bar is in-sample for the phantom proxy** (listed in MNQ phantoms).

---

## §2 — Close-eval baseline (Phase 0 band — historical)

2026-04-01 → 2026-07-28T18:59 UTC continuous `.v.0` 1m → 15m (superseded as §6 limb by §FULL):

| Leg | 15m bars | Confirmed-close `longSignal` count |
|---|---:|---:|
| MNQ | 7,725 | **22** |
| MYM | 7,725 | **30** |

These are the bars the Strategy Tester / backtest-denominated book would admit under the
locked filters (session + DOW + warmup + breakout/body/ATR limbs). No TV trade-CSV parity
claim is made here — this is the Pine boolean on Databento OHLC.

---

## §3 — Coarse 1m phantom proxy (Phase 0 band — historical)

**Definition:** a **phantom** = session+DOW+warmup candidate 15m bar where forming-bar
`longSignal` is true on **some** 1m close inside the bar, but confirmed-close `longSignal`
is **false**. Same definition underpins §FULL.

| Leg | Session candidates | Confirmed signals | Phantoms | Phantom / candidates | Phantoms / confirmed-signal count |
|---|---:|---:|---:|---:|---:|
| MNQ | 544 | 22 | **15** | **2.76%** | **0.68×** |
| MYM | 529 | 30 | **21** | **3.97%** | **0.70×** |

Median mid-vs-confirmed stop Δ on phantom bars: MNQ **−2.75 pts**, MYM **−2.29 pts**
(mid stop typically *tighter* than the eventual confirmed ATR stop — range still forming).

**Reading (Phase 0):** phantoms rare among session bars (~3–4%), ~0.7× vs confirmed.
**Canonical §6 numbers are §FULL** (0.765 / 0.690).

Caveats (binding):

- Not every tick — lower bound on true tick phantoms.
- Continuous `.v.0` ≠ TV `MNQ1!` front month; levels can differ by roll. The 07-28 close
  matched operator chart **exactly**, so that bar is clean; panel-wide counts carry roll
  caveat.
- No `canTrade` / open-position / daily-cap / DD limbs — filter-layer identity only.

---

## §4 — Disposition

- **Offline limb for Q-SIGID-1 = FULL** (MNQ 0.765 / MYM 0.690; both ≥ 0.5). Fri 07-31
  §2b still owed — this run does not close the Q alone.
- Equal Fri ⇒ 07-28 may be save-confounded as live delivery; offline phantom on that bar
  and the FULL census still stand. Different ⇒ live confirmation of the same class.
- Remediation is **locked-parameter axis**, not EQ P1–P4 — see Pre-Q
  [`Q-SIGID-1`](../../../docs/briefs/Q-SIGID-1-intra-bar-signal-identity.md).
- **No Pine edit on this branch.** Caveats unchanged: 1m = lower bound on tick phantoms;
  `.v.0` ≠ TV `1!`; filter-layer only (no `canTrade` / position / cap / DD).

---

## Verification

```bash
python lab/analysis/c1_signal_identity_2026-07-28/signal_identity.py --mode full
# expect falsifier MEASURED; p0rep_exact true; FULL ratios ~0.765 / 0.690
```
