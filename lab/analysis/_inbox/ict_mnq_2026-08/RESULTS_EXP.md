# `Q-ICTEXP-1` — RESULTS: ICT chain gross-expectancy ceiling (native MNQ 1m)

**Date:** 2026-08-04
**Pre-registration:** [`PREREG_EXP.md`](PREREG_EXP.md) — frozen at commit `30c79c9`, **before any
expectancy number existed**. No P&L, excursion, or R had ever been computed on this chain by
anyone, on any instrument.
**Cost:** **$0.00** (MNQ 1m estimate and pull both billed `$0.0000`, 2,553,405 records) · **K=0**
(operator-affirmed) · **no manifest** · **Cap seat untouched**.
**Runner:** [`run_exp.py`](run_exp.py) · **25 new unit tests** (67 total in this directory), all
hand-computed and passing *before* the runner touched a real bar.

---

## 1. Verdict — `AMBIGUOUS` (X3), and it sits at the NULL end of that band

| Tier | Measured | Bar | Read |
|---|---|---|---|
| **T1** perfect-foresight ceiling, mean MFE | **120.413 pt**, block-CI [116.376, 124.463] | 5.640 pt | clears by ~21× — **as pre-registered, this is not evidence** |
| **T2** frozen DOL target, no stop, mean signed | **−1.039 pt**, block-CI **[−3.589, +1.444]** | 5.640 pt | **CI straddles zero; negative point estimate** |
| n | **32,355** filled events | ≥100 | floor cleared 324× |

**The frozen gate fires X3 → `AMBIGUOUS`.** Per [`PREREG_EXP.md`](PREREG_EXP.md) §6 the
consequence is fixed in advance: **NO-GO on `Q-ICT-1MEXEC-1` stands.**

**But read the number, not just the label.** X3's pre-registered gloss is *"real but
unharvestable."* The realized T2 is weaker than that phrase suggests: its 95% block-CI
**contains zero**, so the chain's directional content at its own frozen target is **not
distinguishable from nothing** — and the point estimate is **negative**. Net of the 1.410 pt
round trip, expectancy is **−2.449 pt = −$4.90 per trade**. This is a null with negative drift,
not a promising-but-untradeable edge. *(The gate is read exactly as frozen; this paragraph
describes where inside the AMBIGUOUS band the result landed, and amends no criterion.)*

---

## 2. T1's 21× clearance is an artifact, and that was written down in advance

`PREREG_EXP.md` §4 pre-committed: *"T1 is a perfect-foresight bound over a multi-hour window on
a 1m instrument; it is expected to clear 5.640 pt comfortably, and a T1 pass is therefore not
evidence of edge and not a surprise."*

That is exactly what happened, and the disclosure tier shows why: the **median hold is 660 bars
(≈11 hours)** — the window runs from fill to the E1 16:00 ET flat deadline, and only 26.1% of
events end early by touching the target. Over eleven hours MNQ's maximum favorable excursion is
naturally enormous; a mean MFE of 120 pt measures the instrument's range, not the chain's skill.

Recording that expectation *before* measuring is what keeps a 21× number from being read as a
21× edge.

---

## 3. Why T2 is ≈ 0 — the decomposition (disclosure; recomposes exactly)

| Leg | n | share | mean signed |
|---|---|---|---|
| target **touched** | 8,450 | 26.1% | **+97.947 pt** |
| target **not touched** (exits at the E1 flat deadline) | 23,905 | 73.9% | **−36.028 pt** |
| **recomposed** | 32,355 | | `0.261 × 97.947 + 0.739 × (−36.028)` = **−1.039 pt** ✓ |

A minority of events run to the 1H range extreme for a large gain; the majority bleed out to the
flat deadline. The two legs cancel almost exactly. Win rate is **56.2%** against a *negative*
mean — the signature of a left-skewed payoff, and the same drop-top-k fragility shape this
family has shown before.

**No consistency by side or by year:**

| | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|
| n | 2,963 | 4,479 | 4,359 | 4,431 | 4,347 | 4,473 | 4,609 | 2,694 |
| mean signed (pt) | +0.24 | +4.94 | −2.20 | +1.69 | −0.03 | −8.09 | +0.40 | −7.37 |

Sign alternates across eight years with no trend. By side: bull **+1.676**, bear **−3.596** —
neither reaches the bar, and they disagree in sign.

---

## 4. Population continuity with Part C (sanity check)

| | Part C (2026-08-03 panel) | Here (2026-08-04 panel) |
|---|---|---|
| 1m bars | 2,552,025 | 2,553,405 |
| displacement FVGs | 128,089 | 128,163 |
| raid-paired | 55,604 | 55,645 |

One extra day of panel, deltas of the expected size. The detector is behaving identically.
Drops from raid-paired to filled: `no_fill` 22,809 (the 59%-retrace fact from Part B, seen from
the other side), `no_h1` 45 (warmup), `noDraw` 432, `no_window` 4.

---

## 5. Consequences

1. **NO-GO on `Q-ICT-1MEXEC-1` stands, and reason 3 is now measured rather than merely absent.** The draft pre-registration's third NO-GO reason was *"there is no edge hypothesis — Part C removed an objection, not a reason to expect money."* That was an argument from absence. It is now an argument from measurement: at its own frozen target, on 32,355 events across eight years, the chain's expectancy is statistically indistinguishable from zero and negative after costs.
2. **The other three NO-GO reasons are untouched**, exactly as `PREREG_EXP.md` FM-1 requires: the `K_eff=3` annSR floor of 0.980 against Cap 1.0, the permanent MNQ foreclosure at `K_eff=4`, and ADR 2026-07-12 §4 cl.4's directive language. Nothing here moves any of them.
3. **The seat is preserved.** $0.00 spent, K bank unchanged at 2, no manifest opened, Cap seat untouched. The question that would have cost the last MNQ K seat was answered for nothing.
4. **A standing negative for the `ict-liquidity` class:** the chain now has a measured expectancy on a native micro panel — the first ever computed for it anywhere. Any future proposal keying on raid→FVG→opposing-pool-draw as an *entry* must argue against this, not merely against the older robustness failures.

---

## 6. Scope limits — read before citing any number above

1. **This is stop-free, and the stop is the one untested lever.** The stop-placement rule is not transcribed anywhere in the ICT corpus (`PREREG_EXP.md` §0), so no stop was simulated. A real stop would truncate the **−36.028 pt** untouched leg, and could move T2 in **either** direction (it also exits trades that would later have reached the target). **This result therefore does not establish that the full frozen construct is negative** — it establishes that the chain, exited at its own frozen DOL target with no stop, has no measurable directional edge. Testing a stop requires inventing an unreconstructable constant *and* is K-bound; it is not free work.
2. **The R-denominated arm-time filters were NOT applied** (`minRmult=4.0`, `minAbsR=2.0`, tradeability floor) — declared in advance, for the same unreconstructability reason. Each only ever *trims*, so the measured population is **more generous** than the frozen construct's, not less.
3. **Gross, not net-of-everything.** Costs enter only through the 5.640 pt bar and the net-of-cost line; no commission was charged per-trade inside T1/T2.
4. **Bar-level touch semantics** (shared with Parts B and C), and no intrabar path modelling. A same-bar target-and-adverse sequence is resolved optimistically for the target.
5. **This measures expectancy, not annualized risk-adjusted return.** Nothing here speaks to the 0.980 annSR floor; the two are different objects and the gap between them is where every prior ICT result died.
6. **No outcome of this probe promotes anything.** It has no GO state by construction.

---

## 7. Reproduce

```bash
python -m pytest lab/analysis/_inbox/ict_mnq_2026-08/ -q          # 67 passed
python lab/analysis/_inbox/ict_mnq_2026-08/run_exp.py <mnq_1m.parquet>
git --no-pager diff HEAD -- lab/archive/ict_cascade_2026-06-18/   # must be EMPTY
```

Data (gitignored, regenerable at $0.00 — estimate first, always):

```bash
python lab/databento_fetch/db_fetch.py estimate --symbols MNQ.v.0 --stype continuous \
  --schema ohlcv-1m --start 2019-05-06 --end 2026-08-04 --phase oos
python lab/databento_fetch/db_fetch.py pull --symbols MNQ.v.0 --stype continuous \
  --schema ohlcv-1m --start 2019-05-06 --end 2026-08-04 --phase oos \
  --max-cost 1.00 --out mnq_1m.parquet
```

**Defect caught by the pre-data tests (worth keeping):** `flat_deadline_idx` originally read
`.asi8 // 1_000_000` to get milliseconds. Under pandas 2.x the intermediate carries
`datetime64[us]`, so that expression silently yields **seconds** — every deadline landed before
the panel, every window came back empty, and the run would have reported **zero events with no
error at all**. `test_flat_deadline_*` caught it before a single real bar was read. This is the
`M-AHF`-class failure in a new place: an assumed unit, not an assumed regex.
