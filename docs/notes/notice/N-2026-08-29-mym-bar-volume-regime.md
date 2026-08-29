# Notice — MYM M15 bar-volume regime → next-bar range (ToD-deseasonalized, cheap falsifier)

**Notice ID:** N-2026-08-29-mym-bar-volume-regime
**Observed:** 2026-08-29
**Author:** Joshua | claude.ai
**Source:** backtest CSV (bar panel) — atheoretical mechanism harvest, MYM Phase 2
**Status:** `DROPPED`
**Lives in:** `docs/notes/notice/N-2026-08-29-mym-bar-volume-regime.md`

---

## §0 — Source anchor

- **Source:** `core/data/bar_data/MYM_M15.csv` (sha256
  `24e169528f7ea6693b75c71c3195edf6a04f3a26c6b6dff0f2e9c623fd597a58`), all 141,467 bars
  (RTH + overnight; last truncated session dropped). Script:
  `lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c3_volume_regime.py`. Results:
  `.../c3_results.json`.
- **Observed at:** 2026-08-29 (this session).

---

## §1 — The observation

**Two constraint-audit catches, before running anything:**

1. Plain M15 volume has a strong intraday U-shape (busy at the open/close, thin
   overnight) — a raw pooled trailing-median threshold would mostly rediscover that
   shape, not a genuine "regime" claim. Every value below is expressed relative to its
   **own time-of-day slot's** trailing median (20 prior same-slot occurrences, ~1
   trading month) — the same deseasonalization convention `tod-baseline-range-trigger`
   already established in `MECHANISMS.md` ("same time-of-day slot's own trailing
   median"), reused rather than invented.
2. Volume and range are **different series**. Even at 1-bar (15-min) lag, volatility
   clustering has memory far longer than that, so "high-volume bar_t → high-range
   bar_t+1" could be entirely explained by both series riding the same slow regime
   state — the identical cross-series confound flagged for candidates 2 and 4 (S2-shaped,
   not S1-shaped), just at 1-bar instead of same-session lag. Scored the same way: a $0
   increment test, not a full corrected battery, since the joint-surrogate design that
   would make an independent-series test valid here is unbuilt.

The falsifier: does an above-own-ToD-median-volume bar (bias) predict a next-bar
above-own-ToD-median range (outcome) **better than** the next bar's own predecessor
range already does (the mundane same-series comparator: "this bar's range is already
elevated")? Result on n_common=139,605 bar-pairs: volume-conditioned obs=0.6546
(n_cond=68,509) vs. own-range-conditioned obs=0.6596 (n_cond=68,113) — diff **−0.0049**,
95% block-bootstrap CI **[−0.0085, −0.0012]**, p=0.0115. Both conditioning schemes sit
far above the unconditional base rate (0.4879) — range clustering is real and strong —
but volume adds nothing beyond it; if anything, very slightly less.

## §2 — Why it stands out (the N signal)

- **Baseline:** the mundane own-series persistence comparator (0.6596).
- **Delta:** volume-conditioning underperforms that comparator by 0.49pp — small in
  magnitude but resolved with high confidence given the huge same-panel sample (CI width
  ~0.7pp).
- **Frequency check:** first instance on MYM; no prior score on this construct anywhere
  in the repo (distinct from `opening-pressure`, which is opening-window volume ×
  directional efficiency — DEAD on MYM's own limb — this is a general, any-time-of-session,
  magnitude-only claim).
- **Null-validity grounding, disclosed (per the futures-anomaly-discovery skill's
  "fresh batteries need the same check reuse gets" rule):** volume clustering as a
  stylized fact traces to the mixture-of-distributions literature (Tauchen & Pitts 1983;
  Bollerslev & Jubinski 1999) — the same general information-arrival-clustering family
  the frozen spec cites for range/TR (ARCH/GARCH canon) — not a repo-native frozen
  battery. This is a lighter, citation-based grounding, disclosed as such rather than
  claimed at the GC/CL battery's rigor.

## §3 — Candidate mechanisms (informal)

- Ordinary co-movement of volume and range under the same information-arrival process
  (MDH) — the canon explanation, and the most likely account of why the mundane
  comparator alone already captures everything volume adds.
- Could also be noise; the CI, while excluding 0, is economically negligible either way.

## §4 — Routing decision

**DROP.**

Reason: clean, well-powered NO-INCREMENT. Volume-regime conditioning carries no
information about next-bar range beyond what the range series' own one-lag persistence
already supplies, and the tiny magnitude (well under 1pp) would not survive any
realistic cost hurdle even if it were directionally useful. Statistically significant
(n≈140k) but not economically or informationally interesting — a textbook case where
significance and substance diverge.

---

## §10 — Audit hooks

```bash
python lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c3_volume_regime.py
# Expected: diff=-0.0049  95% CI=[-0.0085,-0.0012]  p_two_sided=0.0115  VERDICT=NO-INCREMENT

grep "N-2026-08-29-mym-bar-volume-regime" docs/briefs/Q-*.md
# Expected: no matches (DROPPED, not graduated)
```

---

## Verification

```bash
$ python ~/.claude/skills/brief-authoring/scripts/check_brief.py \
    docs/notes/notice/N-2026-08-29-mym-bar-volume-regime.md --type notice
# Expected: RESULT: well-formed
```
