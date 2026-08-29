# Notice — MNQ M15 bar-volume regime predicts next-bar range (not direction), incremental beyond range's own persistence

**Notice ID:** N-2026-08-29-mnq-bar-volume-regime
**Observed:** 2026-08-29
**Author:** Claude Code
**Source:** own statistical computation this session, candidate 3 of a pre-specified 5-candidate MNQ Notice-phase batch
**Status:** `OPEN` — routing decision below is GRADUATE (range limb only); direction limb is DROP
**Lives in:** `docs/notes/notice/N-2026-08-29-mnq-bar-volume-regime.md`

---

## §0 — Source anchor

- **Source:** [`lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate3_volume_regime.py`](../../../lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate3_volume_regime.py) → `candidate3_results.json`; consolidated in [`RESULTS.md`](../../../lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/RESULTS.md) §Candidate 3.
- **Observed at:** 2026-08-29, this session, on `core/data/bar_data/MNQ_M15.csv` (all 141,541 M15 bars).
- **K:** [`discovery_manifests/mnq_dailygeom_notice_20260829.json`](../../../discovery_manifests/mnq_dailygeom_notice_20260829.json), `--lane blind`, K=5, closed p≈0.0005 for this cell (block-bootstrap on the ToD-matched range result, the smaller/survivor sub-test).
- **Prior art:** `python scripts/instrument_profiles.py cell MNQ opening-pressure` and `... order-flow-depth-imbalance` both confirmed `DEAD` on MNQ — neither is this construct (opening-pressure is opening-window-only; order-flow-depth-imbalance is tick-level MBP-10 book size, not plain OHLCV volume). No existing MECHANISMS.md class matches "plain-OHLCV bar-volume regime → next-bar conditioning."

---

## §1 — The observation

Tested two next-bar outcomes conditioned on the trigger bar's volume being above its own trailing-median (ToD-matched to remove the deterministic intraday volume-seasonality confound — see §2):

- **Directional continuation (does the next bar's close-open sign match the trigger bar's?): a clean null.** ToD-matched lift +0.01pp (n≈134,678 scored pairs) — no effect, naive or corrected.
- **Next-bar range elevation: real and large.** Naive pooled: obs 0.803 vs base 0.514, lift +28.9pp — but this is heavily confounded by intraday volume seasonality (see §2). ToD-matched: obs **0.684** vs base 0.503, lift **+18.1pp**, CI [0.673, 0.695] (block-bootstrap, block=96≈1 day, n_cond=70,545/n_scored=136,020).

A follow-up check not in the original framing, run because same-bar Spearman(volume, range)=0.88 raised the obvious question of whether "volume regime" is just relabeling range's own persistence: own-range→own-range persistence (ToD-matched) gives an almost identical point estimate (0.686) to volume→range. But stratifying the volume→range test on the trigger bar's own range state shows volume still adds **+20.6pp** (low-range stratum, n=12,430/54,167) and **+25.6pp** (high-range stratum, n=58,115/11,308) of incremental lift beyond what the trigger bar's own range already tells you.

---

## §2 — Why it stands out (the N signal)

- **Baseline:** no prior test of plain-OHLCV volume regime as a range/direction conditioner exists on MNQ. The nearest DEAD cells (`opening-pressure`, `order-flow-depth-imbalance`) are both confirmed structurally distinct.
- **Delta / null-validity note (this candidate's own required fresh citation, per the futures-anomaly-discovery skill's "fresh batteries need the same check reuse gets" rule):** M15 volume carries a strong deterministic intraday seasonality (U-shape, an RTH-open step) — a naive pooled trailing-median comparison is confounded on both sides of the test, since the 09:30 ET bar is mechanically high-volume and the following 09:45 ET bar mechanically is too, for reasons unrelated to any genuine clustering mechanism. This is the identical confound class that `tod-baseline-range-trigger` (Q-TODVOL-1) was built to avoid on a different construct, and the same fix — a causal reference conditioned on the SAME time-of-day slot — is adopted here as the null-validity design, not borrowed as a battery. The naive-vs-ToD-matched comparison (28.9pp → 18.1pp) makes the seasonality artifact's size directly visible, rather than merely asserted.
- **Frequency check:** first test of this construct on MNQ.

---

## §3 — Candidate mechanisms (informal)

- **A — the same underlying activity/volatility-clustering phenomenon as candidate 1, at finer grain.** Volume clustering and volatility clustering are both well-established ARCH-type stylized facts and are known to co-move (Clark's mixture-of-distributions hypothesis, volume-volatility literature). This candidate may not be a distinct WHO from candidate 1's daily TR persistence — just the same regime-level phenomenon observed at M15 via a different proxy.
- **B — volume genuinely carries information beyond contemporaneous range**, e.g. order-arrival intensity anticipates the NEXT bar's range even when the current bar's own range doesn't fully reflect it (a partial-information story: volume reflects participation/urgency, range reflects realized outcome, and the two decorrelate enough at M15 to matter — supported by the +20-26pp incremental-lift finding).
- **C — could be noise from the specific 60-bar trailing window / P50 threshold choice** — untested at other window/threshold combinations this session (any such retune would be a fresh K-charged axis, not a free look).

---

## §4 — Routing decision

**Split decision by outcome.** Range limb: **GRADUATE to Pre-Q.** Reason: real, well-powered (n>130k), CI clearly excludes the base rate, survives both the ToD-seasonality control and the incremental-over-own-range stratification — a construct worth a proper falsifiable H, distinct enough from candidate 1 (finer grain, incremental over range) to justify its own line even though mechanism A above is a live possibility the Pre-Q should confront directly. Direction limb: **DROP.** Reason: clean null both naive and ToD-matched, no plausible mechanism surviving, nothing to carry forward.

**Route flag for the range limb (raised bar, `index-intraday-ohlcv-directional-timing-2026-07-21`):** conditioner-role, not entry-role (same framing as candidates 1/2) — does not by itself need to clear the raised bar; an entry construct built on it later would.

---

## §5 — If HOLD: re-check trigger

N/A — routed GRADUATE (range) / DROP (direction), not HOLD.

---

## §10 — Audit hooks

```bash
# Reproduce both outcomes, naive and ToD-matched (~1-2 min, Python loop over ToD groups)
python lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate3_volume_regime.py
# Expected: dir lift ~0.0001 (ToD-matched); range lift ~0.181 (ToD-matched), CI [0.673, 0.695]

# Confirm the DEAD-cell distinctness claims this notice rests on
python scripts/instrument_profiles.py cell MNQ opening-pressure
python scripts/instrument_profiles.py cell MNQ order-flow-depth-imbalance
# Expected: both DEAD, both for reasons distinct from this construct (see §0)

# If GRADUATED: confirm the Pre-Q references this notice
grep -rn "N-2026-08-29-mnq-bar-volume-regime" docs/briefs/Q-*.md
```

---

## Verification

```bash
python .claude/skills/brief-authoring/scripts/check_brief.py docs/notes/notice/N-2026-08-29-mnq-bar-volume-regime.md --type notice
```
