# Phase-1 perfect-foresight oracle test — regime-adaptive sizing

**LoR:** OUTER (INQHIORI). Gating falsifier (three-tier oracle, Tier 1) for the regime-adaptive-sizing
direction. Research artifact; locked config untouched (`LOCKED_FILES_CLEAN`). 2026-06-15.

**Question.** With **perfect knowledge of the regime AND free choice of per-leg sizing**, is there *any*
regime-conditional policy that clears the regime-robustness gate on the binding hostile half (H1) at a
**viable median pass-time** (pre-registered ≤ 45 bdays)? If even perfect foresight can't, no real-world
detector can — regime-adaptive *resizing* is dead and detector research is moot.

**Basis.** Decompounded-static Pepperstone 2020-26 (canonical gate basis, single-feed). Gate floor:
bust < 1% AND p99 DD < 5% in the partition. C2 dd_protection. Regime boundary = gate bday midpoint
2023-03-21 (H1 hostile / H2 benign — perfect foresight: we *know* 2020-23 was the choppy regime).

## Result — ORACLE FAIL

**Benign half (H2) at full risk:** 99.46% pass / 0.54% bust / 4.87% p99 / **median 18** → clears (the benign policy is just "full risk", as expected).

**Hostile half (H1) policy sweep:**

| hostile policy | Σrisk | pass | bust | p99 DD | median | clears gate? | viable (≤45d)? |
|---|---:|---:|---:|---:|---:|:---:|:---:|
| REF full (all 4) | 2.91% | 75.45% | 24.54% | 8.57% | 67 | no | no |
| uniform k=0.40 | 1.16% | 92.07% | 3.43% | 6.57% | 254 | no | no |
| **uniform k=0.25** | 0.73% | 89.22% | 0.35% | 5.00% | **367** | **YES** | **no** |
| harvest OFF, Strikers full | 1.07% | 75.57% | **21.63%** | 8.43% | 166 | no | no |
| harvest OFF, Strikers k=0.5 | 0.54% | 76.80% | 3.61% | 6.30% | 366 | no | no |
| **harvest OFF, Strikers k=0.25** | 0.27% | 64.68% | 0.04% | 4.12% | **572** | **YES** | **no** |
| harvest k=0.25, Strikers full | 1.53% | 82.30% | 16.30% | 7.93% | 147 | no | no |

**The only policies that clear the hostile half require a median pass-time of 367–572 days — 8–13× the 45-day viability ceiling.** Not a close call. **ORACLE FAIL.**

## Why — the binding constraint is drift, not detection

The hostile regime has **near-zero survivable drift**:
- The harvest-only legs (Guardian, Aegis) have ~zero hostile edge (PF ≈ 1.0) — they only add drawdown.
- **The Strikers have edge but fat pyramid tails that bust on their own.** "Harvest OFF, Strikers full" — the data-indicated "keep only the regime-spanning legs in chop" policy from the realloc grid — **still busts 21.63%** in H1. The pyramid-unwind tail (−5R to −7.6R) dominates at full size. This **kills the D3 / keep-Strikers idea on the honest basis.**
- De-risking enough to survive the tail (k≈0.25) drops drift so low that reaching +5% takes 1–1.6 years.

No detector beats perfect foresight. Since perfect foresight can't pass the hostile regime at viable speed, **regime-adaptive RESIZING is dead for the challenge-pass problem.** This is a drift problem, and you cannot detect your way out of a drift problem.

## The surviving interpretation — regime-adaptive PARTICIPATION

The signal's job is **not** "resize to keep passing in chop" — it's **"decide whether to attempt the challenge now, or wait for the benign regime."** Deploy full risk only in benign (H2 clears at 99.46% / median 18); sit out (or run minimal risk) in hostile. This reframes the research:

- **Weaker, more achievable detector requirement.** The decision is made *once, at challenge start*, and only needs the regime to be **persistent** enough that "benign now" predicts "benign for the ~18-day pass window." This sidesteps the intra-challenge detection-*latency* problem that kills resizing detectors.
- **Different cost structure.** False-negative (attempt in hostile) → a bust; false-positive (wait through a benign window) → opportunity cost / idle time. No intra-challenge whipsaw.
- **Own viability question** (the new falsifier): what fraction of time is benign-and-detectable, and are hostile regimes short enough that sitting out is acceptable? The 2020-26 split is ~50/50; when you *do* deploy (in benign), you pass at 99.46% / median 18 — viable, since a challenge has no start deadline.

## Verdict and next step

- **ORACLE FAIL** for regime-adaptive resizing → **do not commission detector research for a resize signal.** The cheapest-falsifier-first discipline paid off: this one run (≈4 min) closes a direction that would otherwise have consumed a full claude.ai research cycle + a CC implementation.
- **Redirect:** if the research proceeds, it should target a **participation / deploy-vs-wait gate** (regime persistence at challenge start), not an intra-challenge resize indicator. The earlier claude.ai prompt should be re-pointed accordingly.
- Cross-check: uniform k=0.25 → 367d reproduces PR #157's `h1_check` exactly — harness fidelity confirmed.

**Artifacts (gitignored):** `lab/analysis/regime_stress_2026-06-15/oracle_check.py` (renamed from `oracle_test.py` 2026-06-22 — pytest-collection fix) + `oracle_test.json`.
