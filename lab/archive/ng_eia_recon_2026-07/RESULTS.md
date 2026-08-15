# NG-EIA-1 Phase-0 RESULTS — native NG, POST-ONLY announcement bracket

**Verdict: CLOSED — FALSIFIED at Phase-0 (both P0.2 power and P0.3 cost-law fail decisively; per-year sign alternates — noise, not a decaying real premium).**

**Scoping brief:** [`docs/briefs/rnd-pipeline/NG-EIA-1-announcement-bracket-premium-scoping.md`](lab/archive/../../docs/briefs/rnd-pipeline/NG-EIA-1-announcement-bracket-premium-scoping.md)
**Run:** 2026-07-21 · `run_phase0.py` (K=0 δ-extraction, not a registered search) · operator GO recorded (§8), **after** the pre-run construct-definition correction (post-only, not pre+post — see brief change history).
**Engine:** fixed-bracket pattern, modeled directly on `q_fbeia_1_2026-07/extract_eia_delta.py` (F-B, CL) / `q_znauc_1_2026-07/extract_delta.py` (H-ZNAUC-1, ZN) — same Req-4/Req-5 gate formulas, own construct (not `orb_lib`, since this is a fixed-hold bracket, not a breakout-with-stop).
**Data:** native `NG.v.0` continuous 1m (Databento GLBX.MDP3, pull `$0.00`, `ohlcv-1m_continuous_718110b3fb16eece.dbn`, 2,390,503 rows). Event calendar: **primary-sourced from `ir.eia.gov/ngs/schedule.html`** (WebFetch-verified; NOT a Wednesday→Thursday heuristic — EIA's own non-uniform holiday-exception table, brief §5). PRIMARY = 323 Thursday 10:30am ET events, 2019–2026, with any Mon–Thu holiday-ambiguous week dropped entirely (conservative, per the brief's pre-committed discipline); SECONDARY (best-effort shift reconstruction) = 350, informational only.

---

## The construct correction, honored

The brainstorm workflow's own executioner caught, before this run, that my brief's original candidate description conflated a pre+post bracket with the paper's actual citable claim — which attaches only to the **post**-announcement window (the pre-leg is surprise-conditional, the F-B/CL-EIA trap). The brief was corrected before GO; this run measures the corrected **PRIMARY: short 10:25 ET (blind, no lookahead) → cover 11:00 ET**, with the wider pre+post bracket reported only as non-gating **SANITY-1**.

## P0.1 — faithfulness anchor: clean

Mean |m0| (10:30→10:35 ET reaction) = **50.7bp** (median 41.4bp), n=323 — *larger* than F-B's own 25.6bp CL anchor. The EIA storage release genuinely moves NG a lot; the calendar is correctly dated. This is not a dating defect — the null below is real.

## P0.2/P0.3 — PRIMARY: FALSIFIED on both gates

| Quantity (n=323) | Value |
|---|---|
| PRIMARY delta (short 10:25→11:00 ET) | **+8.30 bp** (σ 159.7bp, δ/σ **0.0520**, t **+0.93**) |
| Req-4 power floor (δ/σ ≥ 1.96/√323 = 0.1091) | **FAIL** (0.052 ≪ 0.109) |
| RT single-RT @ median price $2.868 | 7.40bp → 4× hurdle **29.6bp** → **KILL** (8.30bp ≪ 29.6bp, ~3.6× under) |
| RT two-RT convention | 14.8bp → 4× hurdle **59.2bp** → **KILL** |

The citable paper number (~23bp/event net, t=2.93) does **not** reproduce on the 2019–2026 native era at anywhere near the magnitude needed to clear cost, let alone the paper's own claimed significance.

## Per-year — the decisive tell

```
2019 +19.98   2020  -4.28   2021  -3.36   2022 -12.77
2023  -7.38   2024 +10.13   2025 +41.18   2026 +37.34
```

Sign **alternates nearly every year**. This is not what a decaying-but-real premium looks like (which would show a smoother, monotone-ish decline toward zero); it is what sampling noise around a true-zero effect looks like at n≈42/year. The 2025–2026 uptick is the kind of thing that would tempt a "maybe it's coming back" read — but with an alternating full history behind it, that's exactly the pattern the brief's §5 forbade treating as signal ("do not pre-judge the outcome from the decay caveat alone... let the gate measure it" — the gate measured it, and it's noise).

## SANITY-1 (informational, non-gating) — no rescue

Short 09:30→11:00 ET (re-admits the surprise-conditional pre-leg): delta +9.42bp, t +0.95 — comparable to PRIMARY, marginally larger as expected from re-including the conditional leg, but not remotely enough to flip any gate. Confirms the construct correction didn't cost anything real (there was no rescuable edge in the wider bracket either).

## P0.4 — MNG sizing sanity: moot

Fails even more badly on the coarser relative-tick cost (11.2bp RT vs the already-failing 8.3bp delta) — as expected, and moot given PRIMARY already fails on full NG.

## Disposition

- **CLOSED — FALSIFIED.** K = 0 consumed; NG family bank stays **0**. Databento spend **$0.00**.
- **R1 finding, load-bearing:** the paper's own R1 weakness (a "puzzle," sign-inverted vs standard theory, 1b failing for the directional claim — see the brief's corrected §1) is corroborated empirically: the modern-era post-window premium is statistically indistinguishable from zero and sign-unstable. Requirement-1-PENDING resolves to **not confirmed**.
- Append to [`docs/rejected_candidates.md`](lab/archive/../../docs/rejected_candidates.md) — `NG announcement-bracket premium`, class edge-failure (delta not distinguishable from zero, sign-unstable) + venue/cost-geometry (secondary, ~3.6× under hurdle even taking the point estimate at face value). Re-proposal bar: new mechanism evidence for a *different* NG construct, not a re-tune of the bracket window.
- No `core/` / allocation / `dd_protection` / `ACTIVE_FIRM` / Pine touch. Lock HELD.

## Reproduce

```bash
PYTHONIOENCODING=utf-8 .venv-research/Scripts/python.exe lab/archive/ng_eia_recon_2026-07/run_phase0.py
```
