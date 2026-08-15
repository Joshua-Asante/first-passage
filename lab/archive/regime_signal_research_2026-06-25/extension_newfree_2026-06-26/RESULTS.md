# Extension — new free regime-signal candidates (2026-06-26)

**Verdict: NULL-EXTENDED.** Seven new FREE candidates, across the three signal families the
parent battery did not cover, **all FAIL** the same N=33 FWER-controlled test. The free-signal
lever for detecting the book's co-drawdown chop regime is now closed across **12 candidates
spanning every plausible free family** — not just the battery's original 5. Remaining levers are
unchanged: **PAID exogenous data** (dealer-gamma / options-flow) or **more accrued episodes**.

Parent: [`../CLOSURE.md`](lab/analysis/CLOSURE.md/), [`../run_battery.py`](lab/analysis/run_battery.py/),
[`../FINDINGS.md`](lab/analysis/FINDINGS.md/). Lock unchanged (99.83/0.17/4.37).

---

## Why this run

The 2026-06-25 battery closed NULL but scoped its verdict honestly to the family it tested:
NFCI (cross-asset financial-conditions), S5FI, RDISP, RCORR, COR3M (within-equity). It did **not**
test the implied-**volatility-surface** family, a **second implied-correlation tenor / dispersion**,
or **cross-asset bond/credit**. All three are free and keyless-fetchable. This run closes those gaps
before escalating to the paid-data lever — falsify-first.

## Method (exact battery replication)

Same recipe as `../run_battery.py`, no deviations:
- **Decision point** = last obs strictly before each episode `onset` (the pre-drawdown peak).
- **Severity** = `depth_usd` (static-$ trough depth on a flat $200K base). *Not* `depth_pct`
  (calendar-confounded — the battery's F1 trap).
- **Residualize** `rank(sev)` and `rank(candidate)` on `[1, rank(rv_at_peak), rank(calendar_rank)]`;
  partial-ρ = Pearson of the residuals.
- **FWER**: 20,000-perm max-|ρ| Westfall-Young across the M=7 family; seed 20260625.
- **Signs PRE-REGISTERED** (theory-first, frozen in `score_newfree.py::CAND` before scoring).
- Inputs frozen in [`glm_inputs.csv`](glm_inputs.csv) (I1 episodes + I2 covariates); built by
  [`make_glm_inputs.py`](make_glm_inputs.py) from `../episodes_raw.csv` + production US500 bars.

**Faithfulness gate (passed):** the premise reproduces the parent battery to 3 dp —
`Spearman(sev,RV) = +0.159, p=0.378` (vol does NOT rank severity → real beyond-vol target) and
`Spearman(sev,cal) = -0.459, p=0.007` (calendar does → controlled). This confirms the extension
is a true like-for-like, not a different test.

## Results — N=33, M=7, power floor |ρ| ≈ 0.36

| candidate | family | reg. sign | partial-ρ | raw-ρ | p_1sided | p_FWER | verdict |
|---|---|---|---:|---:|---:|---:|---|
| SKEW | vol-surface | + | **−0.349** | −0.502 | 0.976 | 0.266 | fail (wrong-sign) |
| COR1M | implied-corr | + | +0.200 | +0.389 | 0.132 | 0.859 | fail |
| DSPX | implied-corr | − | −0.176 | −0.304 | 0.164 | 0.920 | fail |
| VVIX | vol-surface | + | +0.153 | +0.205 | 0.198 | 0.959 | fail |
| HYIG (HYG/LQD) | cross-asset | − | +0.117 | −0.356 | 0.736 | 0.992 | fail (wrong-sign) |
| TERMSTRUCT (VIX/VIX3M) | vol-surface | + | +0.109 | +0.114 | 0.269 | 0.995 | fail |
| MOVE | cross-asset | + | −0.051 | +0.009 | 0.612 | 1.000 | fail (wrong-sign) |

**No candidate clears FWER<0.05 with its registered sign.** The strongest correctly-signed signal
(COR1M, +0.200) is below the power floor and at p_FWER 0.86.

## The one honest curiosity — SKEW (NOT a finding)

SKEW carries the largest |relationship| in the set (raw −0.502, partial −0.349) but in the
**opposite** direction to the pre-registered hypothesis: high crash-hedging demand at the peak
predicted **milder** subsequent co-drawdowns — the contrarian "when everyone's hedged, the crash
doesn't come" pattern (SKEW is a known poor/contrarian crash predictor). Three reasons it is **not**
a pass:
1. **Wrong-signed vs pre-registration** → flipping the sign now is HARKing; forbidden.
2. **|ρ|=0.349 < 0.36 power floor** — underpowered even charitably.
3. p_FWER 0.266 would not clear even with the correct sign at this N.

Disposition: a **pre-registration candidate** for a future run on fresh / held-out episodes
(sign −1), not a result here.

## Footnote — real HY-OAS

`BAMLH0A0HYM2` via FRED `fredgraph` is history-capped at ~3y for this series (returns 2023-06→),
so the cross-asset credit slot uses a full-history **HYG/LQD ratio** proxy at N=33. The real OAS,
scored at its own N=21, gives partial-ρ −0.140 (wrong sign vs +1) but the calendar premise is
degenerate at N=21 (cal Spearman collapses to −0.04 n.s.), so it is **not comparable** and not
load-bearing. To test the real OAS at N=33, source full-history BAMLH0A0HYM2 via the FRED API
(key) or ALFRED vintages.

## Standing implication

The free family is exhausted (12/12 null across vol-level, vol-surface, implied-corr ×2 tenors +
dispersion, and cross-asset bond/credit). This **strengthens** the 2026-06-25 closure and the
`docs/adr/2026-06-07-decompound-remc-hold.md` HOLD: the only outright H1 fix remains a
regime-conditional mechanism, and its detection input is not free at this data resolution. Escalate
to **paid** dealer-gamma / options-flow (separate web survey) or **more episodes** over time;
re-evaluate at the quarterly regime trigger (2026-08-08).

## Reproduce

```bash
cd lab/analysis/regime_signal_research_2026-06-25/extension_newfree_2026-06-26
python score_newfree.py        # fetches candidates live (keyless), prints table, writes result.json
# glm_inputs.csv is frozen-checked-in; to rebuild it you need the gitignored US500 bars:
python make_glm_inputs.py
# dealer-gamma addendum (free SqueezeMetrics DIX/GEX):
python score_dix_gex.py
```

---

## Addendum — dealer-gamma (free DIX/GEX) + paid-data survey synthesis (2026-06-26)

### Dealer-gamma free proxy (`score_dix_gex.py`)

A parallel web survey flagged dealer gamma as the one family with a genuine academic
**theory-of-lead** (Barbon & Buraschi, *Gamma Fragility*, SSRN 3725454: t−1 dealer-gamma
imbalance predicts next-period fragility). SqueezeMetrics publishes index-level **DIX & GEX
free** (CSV, 2011→). Scored against the same N=33, signs pre-registered by theory (lower GEX →
less dealer stabilization → worse; lower DIX → bearish/uncertain → worse; both −1):

| candidate | family | reg. sign | partial-ρ | raw-ρ | p_FWER | verdict |
|---|---|---:|---:|---:|---:|---|
| DIX | dealer-flow | − | **−0.223** | −0.207 | 0.384 | fail (correct-sign, underpowered) |
| GEX | dealer-gamma | − | +0.133 | −0.067 | 0.714 | fail (wrong-sign) |

DIX is the **single strongest correctly-signed signal in the entire search** (battery + extension
+ dealer-gamma = 14 free candidates) — yet still below the 0.36 power floor and non-significant.
GEX (free, index-level) is wrong-signed. **Free lever now closed across 14 candidates / 4 families.**

### Paid-data survey synthesis

The survey's central result *explains the null*: the free option-implied signals (COR, DSPX,
vol-surface) are forward-looking in *name* (expectations) but empirically **coincident** — CBOE's
own March-2020 example shows implied correlation spiking *with* the SPX decline, not ahead. My
peak-sampled test operationalizes "leading," and they fail it.

What the survey adds, ranked by remaining promise:

1. **Dealer gamma at PAID resolution** — the one mechanism-backed lever the free proxy can't fully
   test. FlashAlpha (REST API; minute-level point-in-time *replay* back to 2018-04, covers 2020;
   gated to the **$1,499/mo** Alpha tier; equity/ES-NQ-centric). SqueezeMetrics per-ticker GEX+ API
   **$720/mo** (2011→). OptionMetrics IvyDB (build-your-own GEX from 1996, point-in-time) for a
   fully-controlled construction. Caveat: all SPX/SPY-centric, **not gold/FX-native** — using it
   for this book assumes equity-vol dealer stress is a cross-asset risk-off proxy (needs its own
   validation). And the free DIX hint (−0.223) is weak.
2. **OFR FSI — FALSIFIED as a leading signal.** Explicitly *coincident* ("measures stress as it
   occurs"); the OFR's separate *Vulnerabilities Monitor* is the early-warning tool. Also not
   orthogonal to vol (its 5-category composite *contains* realized vol). Do not pursue for a lead.
3. **HY-OAS access caveat (confirmed by my own run):** FRED truncated all ICE BofA series to a
   rolling ~3y window as of **April 2026** — pre-2023 history now requires ICE Data Indices direct.
   This is why `BAMLH0A0HYM2` came back capped at N=21 here.

**Standing conclusion (reinforced):** no free, detectable, static-or-simple leading signal clears
the N=33 bar across 14 candidates. The only remaining mechanism-backed lever is **paid
high-resolution dealer gamma**, gated on (a) the equity→cross-asset proxy assumption, (b) the
N=33 power floor of 0.36 (a modest real effect would still read null — favor accruing episodes in
parallel), and (c) cost ($720–$1,499/mo). HOLD unchanged; re-evaluate at the 2026-08-08 trigger.

**Sources (paid survey):** SqueezeMetrics plans/DIX (squeezemetrics.com), FlashAlpha pricing/docs
(flashalpha.com), CBOE implied-correlation & dispersion (cboe.com/us/indices), OFR FSI
(financialresearch.gov + OFRwp-17-04), FRED BAMLH0A0HYM2, Barbon & Buraschi Gamma Fragility
(SSRN 3725454). Full cited record: workflow run wf_6288027f-68e.
