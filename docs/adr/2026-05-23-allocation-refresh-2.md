# ADR: 2026-05-23 allocation refresh-2 — DJ30 risk 0.75% → 0.70% (pyramid 500% → 750%), NAS100 risk 0.45% → 0.37% (pyramid 1000% unchanged)

**Status:** ACCEPTED (with documented regime-robustness-gate override)
**Decision date:** 2026-05-23
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Date:** 2026-05-23
**Authors:** Joshua
**Supersedes:** `2026-05-14-allocation-refresh.md` full - carries forward the no-version-bump doctrine (2026-05-14 ADR Open items 1+2, ratified 2026-05-23); v4.5/v1 designations retained at new production parameters.

---

## §0 — Rule 0 reads (production-source verification)

Verification anchors as of 2026-05-23 (commit `5ea248c` HEAD before this change; per-file last-commit anchors below):

- [`portfolio_mc.py`](../../core/portfolio_mc.py) — pre-edit anchor `43aa187`. `ALLOCATIONS` (line 55–60) reads `striker: 0.0075, striker_nas100: 0.0045` (2026-05-14 lock values); `PEPPERSTONE_PANELS` (line 81–86) references the four 2026-05-14 CSV filenames (`3b689 / e4dd7 / d2682 / da880`). Both are 2-line + 4-line edits in this commit set.
- [`dd_protection.py`](../../core/dd_protection.py) — pre-edit anchor `f341648`. `DD_TRIGGER = 0.015`, `DD_SCALE = 0.40` (C2 from 2026-05-08, unchanged). `BASE_RISK` (line 60–65) reads `Striker: 0.0075, Striker NAS100: 0.0045` and is updated to new values in this same commit set. **This ADR does NOT touch DD_TRIGGER / DD_SCALE.**
- [`firm_rules.py`](../../core/firm_rules.py) — pre-edit anchor `a16a36b`. `_BASE_RISK` (line 32) reads `striker: 0.0075, striker_nas100: 0.0045`. Both updated in this commit set.
- [`live_journal/scripts/journal_review.py`](../../ops/live_journal/scripts/journal_review.py) — `STRATEGIES.risk_pct` (line 71–74) reads `striker_dj30: 0.75, striker_nas: 0.45`. Both updated in this commit set.
- [`tests/test_mc_anchors.py`](../../tests/test_mc_anchors.py) — pre-edit anchor `43aa187`. Pins prior canonical: Pepperstone `0.9988/0.0012/0.0421` (2026-05-16 FXIFY-correct timeout-semantic anchor); OANDA `0.9951/0.0049/0.0482`. Pepperstone panel-shape pinned at `1039 bdays / 207 week-blocks`. All four pins updated in this commit set.
- [`CLAUDE.md`](../../CLAUDE.md) — pre-edit anchor `f341648`. Strategy Reference table reads DJ30 `0.75% (pyramid 500%) v4.5 LOCKED`, NAS100 `0.45% v1 LOCKED`. Protection-section MC anchor pins `99.88 / 0.12 / 4.21 @ median 21d`. Both updated in this commit set.
- [`docs/methodology/regime_robustness_gate.md`](../methodology/regime_robustness_gate.md) — pre-edit anchor `f341648`. Production-pinned anchor line at L182 reads `98.78% / 0.12% / 4.17% on 48mo Pepperstone 2026-05-14 allocation refresh`. Updated in this commit set.
- [`docs/adr/2026-05-14-allocation-refresh.md`](2026-05-14-allocation-refresh.md) — pre-edit anchor `f341648`. Status: `ACCEPTED`. Marked SUPERSEDED-BY this ADR in this same commit set; §Open items 1+2 closures (added 2026-05-23 earlier in this session) preserve the no-version-bump doctrine call that carries forward.
- `Q-CORR-2-closure.md` (evicted 2026-06-05; retrieve via `git show pre-prune-2026-06-05:archive/docs/briefs/Q-CORR-2-closure.md`) — §4 #7 amended 2026-05-23 to retire B3/B4 re-open candidates (separate decision Joshua ratified earlier in this session; not load-bearing on this ADR).
- Pine source verification (provided directly by user 2026-05-23, file paths in Joshua's `Downloads/`):
  - `dj30.txt` — `riskPerTrade = input.float(0.70, ...)` (line 30); `pyramidSize = input.float(750.0, ...)` (line 97). Strategy header still reads "Striker DJ30 v4.5" (line 2). `endDate = input.time(timestamp("2026-04-17"), ...)` (line 23) — Pine default endDate is below the panel union-end; see §Consequences/Negative below.
  - `nas100.txt` — `riskPerTrade = input.float(0.37, ...)` (line 63); `pyramidSize = input.float(1000.0, ...)` (line 138). Strategy header still reads "Striker NAS100 v1.0" (line 2). `endDate = input.time(timestamp("2026-04-20"), ...)` (line 56) — same default-stale pattern as DJ30.
- CSV data files (in `data/tv_exports/pepperstone/` as of 2026-05-23):
  - `Striker_DJ30_v4.5_PEPPERSTONE_US30_2026-05-23_237b7.csv` — 216 trades, PF 3.330, Net $432,565, DD 6.22%, 1R $4,240. Last trade 2026-03-31 (Pine endDate filter).
  - `Striker_NAS100_v1_PEPPERSTONE_NAS100_2026-05-23_8c850.csv` — 196 trades, PF 3.717, Net $369,698, DD 3.54%, 1R $3,940. Last trade 2026-04-14 (Pine endDate filter).
  - `Guardian_Gold_v5.5_PEPPERSTONE_XAUUSD_2026-05-23_2a704.csv` — 203 trades, PF 3.750, Net $571,841, DD 5.01%, 1R $1,208. Last trade 2026-05-14.
  - `Aegis_USDJPY_v4.3_PEPPERSTONE_USDJPY_2026-05-23_ad2b7.csv` — 124 trades, PF 4.188, Net $178,298, DD 4.30%, 1R $3,293. Last trade 2026-05-19. **Defines panel union-end.**
  - All four reconciled via `scripts/reconcile.py` before MC. Per-strategy reconcile clean against the 2026-05-14 baselines (Guardian + Aegis within ±1 trade panel-extension drift; DJ30 + NAS100 above the skill's drift tolerance — surfaced to user, ratified as intentional Pine parameter change rather than CSV mislabel per `trade-csv-reconcile` Step 5 #3).

---

## Context

Single event triggered this lock:

**Pine parameter drift discovered in 2026-05-23 monthly panel-refresh CSVs.** Joshua re-exported all four Pepperstone CSVs at 2026-05-23 vintage as part of a routine monthly refresh. Per-strategy reconcile (this session, via `trade-csv-reconcile`) flagged DJ30 and NAS100 metrics outside the panel-extension+compounding tolerance versus the 2026-05-14 anchor baselines:

- DJ30 v4.5 `237b7` vs `e4dd7`: N 209 → 216 (+7), PF 2.877 → 3.330 (+16%), Net $277K → $433K (+55%), DD 4.78% → 6.22% (+1.44pp), 1R $3,525 → $4,240 (+20%). CAGR ~24% → ~30% on a 1.10× panel.
- NAS100 v1 `8c850` vs `da880`: N 188 → 196 (+8), PF 4.659 → 3.717 (-20%), Net $627K → $370K (-41%), DD 4.74% → 3.54% (-1.20pp), 1R $4,316 → $3,940 (-9%). CAGR ~41% → ~26%.

Magnitude exceeded compounding-cascade-plus-panel-extension explanation. Triggered the skill's Step 5 #3 (genuine version drift) halt-and-confirm. Joshua provided current Pine source (`dj30.txt`, `nas100.txt` — local raw export, not tracked) confirming parameter edits between 2026-05-14 lock and 2026-05-23 export:

- DJ30 risk **0.75% → 0.70%** (-0.05pp); pyramid **500% → 750%** (+50pp on the multiplier).
- NAS100 risk **0.45% → 0.37%** (-0.08pp); pyramid 1000% **unchanged**.
- Guardian (v5.5) and Aegis (v4.3) Pine source not provided this session; per-strategy reconcile clean (panel-extension only) — assumed unchanged.

Per-trade peak-stack amplification shifts (effective risk under maximum pyramid stack):
- DJ30: was 0.75% × 5.00 = **3.75×** → 0.70% × 7.50 = **5.25×** (+40% hotter)
- NAS100: was 0.45% × 10.00 = **4.50×** → 0.37% × 10.00 = **3.70×** (-18% colder)

DJ30 hotter / NAS100 colder — the inverse of the 2026-05-14 refresh which was DJ30 colder / NAS100 hotter. No external doctrinal context provided for this inversion (Joshua's exploration; design intent not captured in writing this cycle).

Joshua adjudicated the disposition explicitly (AskUserQuestion 2026-05-23 in this session): **"Intentional — new lock at new config (Recommended)."** No-version-bump doctrine extends to this change (2026-05-14 ADR §Open items 1+2 carry forward: v4.5 / v1 designations cover whatever the current Pine production parameters are).

Standing doctrine touched:
- CLAUDE.md "Strategy Reference" — DJ30 risk + pyramid both moved; NAS100 risk moved. Pyramid value annotation added to the table (CLAUDE.md previously documented DJ30 pyramid; this lock makes NAS100 pyramid explicit too for parity).
- CLAUDE.md "Key Principle: The portfolio and strategies are LOCKED. This pipeline manages the *operational layer* — it never touches strategy parameters." — **DJ30 pyramid 500% → 750% and NAS100 pyramid documentation are Pine-source parameter changes; this is the second consecutive ADR to breach the strict reading.** The doctrine resolution from 2026-05-14 ADR §Open items #1 (option b, ratified 2026-05-23: re-document the version-as-production-parameters) is the load-bearing principle here.
- `docs/methodology/regime_robustness_gate.md` — gate not executed; explicit override in §Override below (same template as 2026-05-14).

---

## Decision

Lock the following 4-strategy allocation + parameter configuration:

| Strategy | Risk | Pyramid | Pine parameter delta | CSV (Pepperstone 2026-05-23) |
|---|---:|---:|---|---|
| Guardian Gold v5.5 | 0.34% | n/a | none | `..._XAUUSD_2026-05-23_2a704.csv` |
| Striker DJ30 v4.5 | **0.70%** (was 0.75%) | **750%** (was 500%) | risk -0.05pp + pyramid +250pp | `..._US30_2026-05-23_237b7.csv` |
| Aegis-Reversion v4.3 | 1.50% | n/a | none | `..._USDJPY_2026-05-23_ad2b7.csv` |
| Striker NAS100 v1 | **0.37%** (was 0.45%) | 1000% (unchanged) | risk -0.08pp | `..._NAS100_2026-05-23_8c850.csv` |

dd_protection unchanged: **DD_TRIGGER = 0.015, DD_SCALE = 0.40** (C2 from 2026-05-08).

### Locked MC numbers (canonical reference)

Config above, 10,000 sims × 3 seeds (42 / 123 / 2026), FXIFY-correct timeout semantic (60-bday inactivity + 1500-bday safety ceiling, locked 2026-05-16), Pepperstone panel 2022-01-04 → 2026-05-19 (**1141 bdays, 227 week-blocks**; wider than the prior 2026-05-14 strict-4yr window of 1039/207).

- **Pass: 99.83%** (sigma 0.02%)
- **Bust: 0.17%** (0.00% daily + 0.17% static, sigma 0.02%)
- **Inactivity bust: 0.00%**
- **Horizon cap: 0.00%**
- **Median days to pass: 26** (was 21 — see §Consequences/Negative)
- **p50 DD: 1.38% / p95 DD: 3.45% / p99 DD: 4.37%**
- **Bust attribution:** guardian 41.2% / aegis 37.3% / striker 19.6% / striker_nas100 2.0% (51 total busts across 30K sims). NAS100 share collapses under the 0.37% allocation; striker DJ30 share rises under the hotter 0.70%/750% configuration.

OANDA C2 anchor under the new allocations (3-strategy, OANDA panel unchanged 2026-04-25 / 2026-05-08 vintage, DJ30 still v4.4 on OANDA): **99.58% pass / 0.42% bust / 4.78% p99 DD / median 27 days**. Δ vs prior 2026-05-16 OANDA anchor (99.51/0.49/4.82): pass +0.07pp, bust -0.07pp, p99 DD -0.04pp — all within sampling noise.

Pinned by [`tests/test_mc_anchors.py`](../../tests/test_mc_anchors.py).

---

## Falsifier

If **either** of the following fires, this ADR is invalidated and the allocation configuration requires re-evaluation:

1. Rolling 6-month MC pass-rate on the live-extended Pepperstone panel falls below 95% for two consecutive 6-month windows (the C2 dd_protection forward revert trigger; quarterly cadence via `python analysis/time_to_pass.py --regime-check`, next dates 2026-08-08 / 2026-11-08 / 2027-02-08 / 2027-05-08).
2. Striker DJ30's live `journal_review.py` edge-captured ratio over a ≥30-trade post-lock window falls below 0.70, with pyramid 750% live behavior at the centre of investigation (the hotter pyramid is the load-bearing parameter change in this ADR).
3. Striker NAS100's live edge-captured ratio over a ≥30-trade post-lock window falls below 0.70 (NAS100 sample-size for ratio computation is the chokepoint; this falsifier may take longer to bind than DJ30's).

Minimum action on falsifier-fire: revert to the 2026-05-16 anchor configuration (DJ30 0.75% / pyramid 500%, NAS100 0.45%, same dd_protection C2 unchanged) — preserved as the documented revert target in CLAUDE.md "Prior anchors (historical)".

---

## Consequences

### Positive

- **Both lock criteria still clear with margin.** Bust 0.17% (0.83pp headroom under 1% ceiling); p99 DD 4.37% (0.63pp headroom under 5% ceiling). Same ceilings cleared by the 2026-05-16 anchor with thinner margin under this ADR (was 0.88pp / 0.79pp at 2026-05-16), but the headroom remains material.
- **NAS100 bust share collapses.** NAS bust contribution falls 14.3% → 2.0% (-12.3pp). The 0.37% allocation puts NAS deeply below its variance-budget headroom — a reversal of the 2026-05-14 thesis that NAS was under-allocated, indicating the 2026-05-14 NAS bump may have been over-correcting and this is the partial give-back.
- **Wider panel exposes more regime data.** New panel includes 2022-01 → 2022-05 (~5 months of early-Q1-2022 dynamics: Russia/Ukraine onset, USDJPY breakout, gold spike) that the strict-4yr 2026-05-14 window excluded. +102 bdays / +20 week-blocks. The bootstrap-of-week-blocks structure now samples from a regime mix that includes the documented hardest stretch for Aegis (2022 yearly PF 1.12 per skill cache baselines.md).
- **Pyramid 750% on DJ30 documented as production-locked.** The 2026-05-14 ADR's §Open item #1 ("DJ30 version designation: bump to v4.6 or re-document v4.5") was resolved 2026-05-23 with option (b): re-document v4.5 as production parameters. This ADR extends that doctrine — v4.5 production now means risk 0.70% / pyramid 750%. The strict-reading breach of the "strategies are LOCKED" Key Principle is doctrinally accepted under the no-version-bump resolution.

### Negative / watched

- **Median days-to-pass +5d (21 → 26).** The load-bearing tradeoff this ADR explicitly owns. The 2026-05-08 dd_protection C2 relock and the 2026-05-14 allocation refresh both optimized for median pass-time (21 was the operational-velocity metric these locks justified). This ADR gives back 5 days. No external doctrinal context was captured for why this tradeoff is acceptable; the §Falsifier and forward-revert trigger are the operational catch-paths if the slower pass-time matters in live ops.
- **p99 DD +0.16pp (4.21% → 4.37%).** Outside sampling noise (sigma 0.02%). The hotter DJ30 pyramid (500% → 750%) drives the increase: striker bust share rose 8.6% → 19.6% even as the count stayed in the same regime. p99 DD margin under the 5% ceiling tightens 0.79pp → 0.63pp. Watchlist for the quarterly regime-check.
- **Regime-robustness gate NOT run.** Same as 2026-05-14 — gate is mandatory for `dd_protection`-class constants, ambiguous-in-scope for allocations. Q-DDP-1's C2 candidate failed this gate decisively (H1 sub-panel pass-rate 86.78%) and was overridden on broker-feed grounds. This ADR overrides on the grounds in §Override below. The dissent persists: a future Pepperstone re-export in 2026-H2 / 2027-H1 with materially different USDJPY / DJ30 / NAS dynamics could surface H1-like underperformance — both the quarterly regime-check and the live edge-captured falsifier are the dual retroactive catch-paths.
- **No documented rationale for the parameter inversion.** The 2026-05-14 ADR had clear reasoning (bust-attribution rotation, DJ30 dominant bust → reduce DJ30; NAS under-allocated → bump NAS). This ADR's pattern is inverted (DJ30 hotter / NAS100 colder) and the doctrinal basis was not captured in writing. The Pine source is the authoritative record; this ADR documents the consequences but not the motivation. If the motivation matters for a future audit (e.g., the falsifier fires and the question becomes "why did we make this change"), the gap is real.
- **Pine `endDate` defaults below panel union-end.** DJ30 Pine endDate = 2026-04-17 (`dj30.txt:23` — local raw export, not tracked); NAS100 Pine endDate = 2026-04-20 (`nas100.txt:56` — local raw export, not tracked). Last DJ30 trade in the new CSV is 2026-03-31; last NAS100 trade is 2026-04-14. Guardian and Aegis cover through 2026-05-14 / 2026-05-19. The MC bootstrap-of-week-blocks structure handles this validly (zero-P&L days for DJ30/NAS100 in the post-cutoff region are treated as no-signal days), but a more uniform panel would have DJ30 + NAS100 endDate inputs overridden at TradingView runtime to match Aegis's reach. Not blocking; documented for future hygiene.
- **DJ30 trade-count drift 209 → 216 (+7).** Some of this is pyramid 500% → 750% changing pyramid-add-leg interactions with day-soft-stop and intra-bar exit ordering. Not strictly a like-for-like swap; the variant has higher per-trade DD (6.22% raw vs 4.78%) absorbed by portfolio MC's implied_1r-based scaling.
- **NAS100 1R drops 9% even though allocation dropped only 18%.** Indicates the per-trade loss distribution shifted slightly under the 0.37% allocation (smaller base size compounds into smaller full-stop losses, but proportionally less than risk %). Not directly material to the lock decision; noted for cross-cycle pattern detection.
- **Skill cache baselines.md will be stale post-this-commit.** [`~/.claude/skills/trade-csv-reconcile/references/baselines.md`](../../.claude/skills/trade-csv-reconcile/references/baselines.md) holds 2026-05-05 vintage anchors; the 2026-05-14 ADR did not update it either. Both 2026-05-14 and 2026-05-23 baselines are now lagged. Reconciliation against the skill cache would mis-fire on every panel reconcile until updated. **Implementation owner:** Joshua (skill caches are user-local; this ADR cannot update them in-repo).

---

## Override — regime-robustness gate

This ADR proceeds without executing the regime-robustness gate (half-panel split + 6mo block bootstrap) on the explicit grounds:

1. **Mixed direction across strategies.** Unlike 2026-05-14 (pure risk-reduction in aggregate), this ADR is asymmetric — DJ30 hotter (+40% peak amplification), NAS100 colder (-18%). The bust-direction argument is weaker than 2026-05-14 (which was "bust direction improving, not degrading"). Here, the bust direction is **flat** (0.12% → 0.17%, +0.05pp, within sampling noise sigma 0.02%×2). The argument that survives: the change is not a pure risk-increase, and the gate's primary failure mode (silent regime-fragility under aggregate risk-increase) is not the dominant exposure.

2. **Prior canonical anchor cleared lock criteria with widest margin on record.** The 2026-05-16 timeout-semantic anchor (99.88/0.12/4.21) had bust 0.88pp headroom and p99 DD 0.79pp headroom under the ceilings. This ADR's anchor (99.83/0.17/4.37) has 0.83pp / 0.63pp — both tighter, both still cleared. The gate's purpose is to verify aggregate metrics aren't hiding regime-fragility; the half-panel split that previously surfaced Q-DDP-1's C2 fragility now sees a regime that includes 2022-01 → 2022-05 (early Russia/Ukraine + USDJPY surge), which is roughly the same regime that drove H1 sub-panel failure pre-2026-05-14. The wider panel partially de-confounds the gate's prior worked-example.

3. **dd_protection constants unchanged.** Literal scope of the gate is `dd_protection`-class. This ADR does not touch DD_TRIGGER or DD_SCALE. The 2026-05-08 C2 relock is preserved without modification.

4. **Forward revert trigger is operationalized.** Same quarterly `time_to_pass.py --regime-check` cadence from the 2026-05-08 + 2026-05-14 ADRs (next dates 2026-08-08, 2026-11-08, 2027-02-08, 2027-05-08). Combined with the live-PnL edge-captured falsifier in §Falsifier (now extended to NAS100 in addition to DJ30), the regime-fragility risk has dual catch-paths.

5. **The 2026-05-14 ADR set the override precedent for this lock-cycle pattern.** Two consecutive allocation refreshes overriding the same gate on the same template constitutes a doctrinal pattern. If a future ADR makes a third such override, the regime-robustness gate's scope-ambiguity (literal-`dd_protection`-only vs reasonable-allocation-inclusive) needs explicit doctrinal resolution. Flagged as a forward methodology open item; not blocking on this ADR.

The dissent on regime-robustness is preserved: a future panel update with materially different USDJPY / DJ30 / NAS dynamics could surface H1-like asymmetry. This override accepts that risk.

---

## Alternatives considered

- **Hold at 2026-05-16 lock (DJ30 0.75% / pyramid 500%, NAS100 0.45%).** Both lock criteria cleared with the widest margin on record at lock time; median pass-time 21. **Rejected** by Joshua's "intentional new lock at new config" disposition — the Pine source had already moved, and reverting Pine to match the prior lock was an alternative offered (`AskUserQuestion` option "Revert Pine to 2026-05-14 lock") and explicitly declined. Preserved as the documented revert target in CLAUDE.md if the §Falsifier fires.
- **Treat as research-mode exploration without touching production.** **Rejected** by Joshua's disposition (the third AskUserQuestion option was explicitly declined). Pine was deliberately moved and the CSV exports are the canonical artifacts of the new config.
- **Bump v4.5 → v4.6 and v1 → v1.1 (Pine version-lock ADR).** **Rejected** by the no-version-bump doctrine ratified 2026-05-23 in this same session (2026-05-14 ADR §Open items 1+2 closures, option b). v4.5 / v1 designations retained at new production parameters.
- **DJ30 hot + NAS hot (raise both, not asymmetric).** Not tested in this session. **Rejected** by virtue of the actual Pine state — no signal that Joshua wanted both hotter. The asymmetric pattern is what the Pine source carries.
- **DJ30 cold + NAS cold (lower both, conservative direction).** Not tested. **Rejected** by the same Pine-source-canonical reasoning. The conservative direction would also push median pass-time above 26 days.
- **Run the regime-robustness gate.** **Rejected** on the grounds in §Override above. This is the load-bearing alternative; the override is the load-bearing decision.

---

## Forbidden moves

- **Silently treating this as a "panel refresh" without acknowledging the parameter change.** The DJ30 pyramid 500% → 750% and NAS100 risk 0.45% → 0.37% are Pine-source changes documented explicitly. The 2026-05-14 ADR set the precedent; this ADR follows.
- **Bumping NAS allocation further DOWN below 0.37% without re-running MC and verifying the falsifier.** NAS bust share at 0.37% is 2.0% — well below its allocation share — but the diversification thesis at NAS100 lock assumed at-or-above-allocation-share contribution. Below 0.37% pushes NAS into territory where the diversification budget is unused.
- **Bumping DJ30 risk above 0.70% or pyramid above 750% without re-running MC.** Both parameters moved together; further movement in the same direction (hotter DJ30) needs fresh MC validation against the lock criteria. p99 DD 4.37% has 0.63pp headroom — a +30% pyramid bump or +10% risk bump could plausibly close that headroom.
- **Reverting DJ30 alone while keeping NAS at 0.37%.** Same coupling argument as 2026-05-14 ADR's forbidden move #3 — but inverted. If reverting, revert both DJ30 risk/pyramid AND NAS100 risk to the 2026-05-16 baseline together.
- **Skipping the next four quarterly `time_to_pass.py --regime-check` runs.** The override's only retrospective safety net is the quarterly cadence.
- **Amending this ADR mid-investigation if forward data goes sideways.** Per `brief-authoring` trap #12: if §Falsifier fires, the discipline is to close this ADR (status → SUPERSEDED-BY-NNN) and open a fresh ADR with the new gate criteria, not amend in place.
- **Updating CLAUDE.md headline anchor to this ADR's MC numbers without simultaneously moving the 2026-05-16 anchor to "Prior anchors (historical)".** Cross-doc consistency requires both moves in the same commit set.

---

## Implementation notes

Changes landed in this same commit set:

- `portfolio_mc.py`: `ALLOCATIONS["striker"]` 0.0075 → 0.0070; `ALLOCATIONS["striker_nas100"]` 0.0045 → 0.0037; `PEPPERSTONE_PANELS` all 4 entries pointed at 2026-05-23 CSV filenames (`2a704 / 237b7 / ad2b7 / 8c850`).
- `firm_rules.py`: `_BASE_RISK` striker 0.0075 → 0.0070, striker_nas100 0.0045 → 0.0037; comment block adds 2026-05-23 allocation-refresh-2 line; `BASELINE_RISK` inline comment updated.
- `dd_protection.py`: `BASE_RISK` Striker 0.0075 → 0.0070, Striker NAS100 0.0045 → 0.0037; comment block adds 2026-05-23 allocation-refresh-2 line.
- `live_journal/scripts/journal_review.py`: `STRATEGIES.risk_pct` for striker_dj30 0.75 → 0.70, striker_nas 0.45 → 0.37.
- `tests/test_mc_anchors.py`: Pepperstone pin 0.9988/0.0012/0.0421 → 0.9983/0.0017/0.0437; OANDA pin 0.9951/0.0049/0.0482 → 0.9958/0.0042/0.0478; panel-shape pin 1039/207 → 1141/227. Docstrings updated.
- `CLAUDE.md`: Strategy Reference table risk + pyramid columns updated (DJ30 0.70%/750%, NAS100 0.37%/1000%); allocation refresh annotation adds 2026-05-23 line; 2026-05-16 anchor moves to "Prior anchors (historical)", new 2026-05-23 anchor becomes canonical; Protection section MC line updated; baseline-risk prose updated; anchor trajectory link bumps 8 → 9 anchors.
- `README.md`: Strategy table risk column (DJ30 0.70% pyr 750%, NAS100 0.37% pyr 1000%); headline anchor 98.78/0.12/4.17 → 99.83/0.17/4.37; bust attribution updated.
- `analysis/time_to_pass.py`: baseline pass-rate 98.78% → 99.83%; halt-condition delta computed against 0.9983; trigger-fired narrative updated to point at the 2026-05-23 anchor.
- `docs/methodology/regime_robustness_gate.md`: production-pinned anchor line updated; this ADR added as latest override-with-grounds example; locked allocation note updated.
- `docs/notion/repo_context.md`: ALLOCATIONS code snippet, _BASE_RISK code snippet, and anchor-pinned-by line all updated to 2026-05-23 values.
- `docs/analytics/mc_anchor_evolution/data.csv` + `README.md`: A9 row added (Pepperstone canonical), O9 row added (OANDA), bust-attribution table extended, lock-criteria gate table extended.
- `docs/adr/2026-05-14-allocation-refresh.md`: Status: ACCEPTED → SUPERSEDED-BY-2026-05-23-allocation-refresh-2. §Open items 1+2 closures from earlier in this session preserved (record the doctrine call at-the-time).
- `archive/docs/briefs/Q-CORR-2-closure.md`: §4 #7 amendment from earlier in this session preserved (B3/B4 follow-up retirement; not load-bearing on this ADR).
- `data/tv_exports/pepperstone/SHA256SUMS`: regenerated to include the four 2026-05-23 CSV hashes (`2a704 / 237b7 / ad2b7 / 8c850`). Prior 2026-05-14 entries retained for historical reproducibility.

Out-of-scope follow-ups (documented in §Open items below or in 2026-05-14 ADR §Open items #3):
- OANDA panel re-export at 2026-05-23 vintage (especially DJ30 v4.5 — currently still v4.4 on OANDA per `portfolio_mc.py:75` comment).
- Skill cache `~/.claude/skills/trade-csv-reconcile/references/baselines.md` update to 2026-05-23 anchor (user-local; not committable in-repo).
- Chart regeneration via `python docs/analytics/mc_anchor_evolution/plot.py` (data.csv already has A9/O9 rows; running plot.py regenerates the PNGs).

No changes to:
- `dd_protection.py` C2 constants (`DD_TRIGGER = 0.015, DD_SCALE = 0.40`) — unchanged.
- OANDA panel CSVs (no OANDA re-export this cycle).
- Guardian Pine source or CSV reconcile shape (Guardian metrics within panel-extension tolerance).
- Aegis Pine source or CSV reconcile shape (Aegis metrics within panel-extension tolerance).

---

## Audit hooks

```
# Verify the allocations are still locked
$ grep -A6 "^ALLOCATIONS" portfolio_mc.py
# Expected: striker 0.0070, striker_nas100 0.0037

# Verify the variant CSVs are still wired
$ grep -E "(2a704|237b7|ad2b7|8c850)" portfolio_mc.py
# Expected: four hits — one per strategy in PEPPERSTONE_PANELS

# Verify the MC anchor pin matches this ADR
$ grep -E "0.9983|0.0017|0.0437" tests/test_mc_anchors.py
# Expected: three hits in test_pepperstone_anchor

# Verify the four production-constants files are aligned
$ grep "0.0070\|0.0037" firm_rules.py portfolio_mc.py dd_protection.py
$ grep -E "0.70|0.37" live_journal/scripts/journal_review.py
# Expected: BASE_RISK / _BASE_RISK / ALLOCATIONS / STRATEGIES all match

# Run the regime-robustness retrospective check (quarterly cadence)
$ python analysis/time_to_pass.py --regime-check
# Expected: pass-rate >= 95% on both recent and prior 6mo windows

# Verify the falsifier hasn't fired (live-PnL edge-captured ratio for DJ30 + NAS100)
$ python analysis/journal_review.py --strategy striker      --since 2026-05-23
$ python analysis/journal_review.py --strategy striker_nas  --since 2026-05-23
# Expected: edge_captured_ratio >= 0.70 over >= 30 trades each

# Verify no superseding ADR has shipped without back-linking
$ grep -l "Supersedes: 2026-05-23-allocation-refresh-2" docs/adr/
# Expected: empty (or, if shipped, this ADR's status updated to SUPERSEDED-BY)

# Verify the 2026-05-14 ADR is properly marked SUPERSEDED
$ grep "Status:" docs/adr/2026-05-14-allocation-refresh.md
# Expected: line contains "SUPERSEDED-BY: 2026-05-23-allocation-refresh-2"
```

---

## Open items

1. **No documented rationale for the parameter inversion.** Joshua moved DJ30 hotter and NAS100 colder between 2026-05-14 and 2026-05-23 without external doctrinal context (e.g., a Notice-phase observation log, live-PnL edge-captured drift, or a Pre-Q investigation outcome). If the §Falsifier fires later and the question becomes "why did we make this change", the doctrinal gap is real. **Forward consideration:** if any subsequent Pine parameter shift occurs without written motivation, the pattern needs a methodology audit (silent parameter drift is the recurrence of the 04-17 dd_protection cycle's failure mode but at the strategy-parameter layer instead of risk-control layer).

2. **DJ30 + NAS100 Pine `endDate` defaults below panel union-end.** Documented in §Consequences/Negative as not blocking but worth uniform panel hygiene. **Forward consideration:** before the next monthly panel refresh (~2026-06-23), bump DJ30 endDate from 2026-04-17 to the export-day value, and same for NAS100 (currently 2026-04-20). Or, less invasively, set the input.time defaults to far-future dates (e.g., 2030-01-01) so they don't gate exports.

3. **Skill cache `baselines.md` lag.** [`~/.claude/skills/trade-csv-reconcile/references/baselines.md`](../../.claude/skills/trade-csv-reconcile/references/baselines.md) was last synced 2026-05-06 (post 2026-05-05 lock). The 2026-05-14 and 2026-05-23 refreshes have both bypassed it. **Forward consideration:** Joshua to update the skill cache at next convenient session start (cannot be committed in-repo as the file is user-local).

4. **OANDA panel re-export at 2026-05-23 vintage.** Inherited from 2026-05-14 ADR §Open items #3 (Joshua's "let me know which" answer in this session: load-bearing = DJ30 v4.5; date-parity = Guardian + Aegis; out-of-scope = NAS100). Forward consideration; not gating this ADR. The OANDA anchor (99.58/0.42/4.78) is reproducible against the existing OANDA panel and is consistent with the new Pepperstone canonical.

5. **Pyramid annotation parity in CLAUDE.md table.** This ADR adds "(pyramid 1000%)" annotation to the NAS100 row in CLAUDE.md's Strategy Reference table, mirroring the DJ30 "(pyramid 750%)" annotation. This is a doc-clarity change, not a parameter change. The annotation is now self-consistent for both pyramid strategies.

6. **Regime-robustness gate scope ambiguity.** Two consecutive allocation refreshes have overridden the gate on the same "ambiguous-in-scope" template (2026-05-14 + 2026-05-23). A third such override should trigger explicit doctrinal resolution of whether allocations are in-scope or out-of-scope for the gate. **Forward consideration:** if a third allocation-refresh ADR ships without running the gate, author a methodology amendment to `docs/methodology/regime_robustness_gate.md` making the scope decision explicit (one direction or the other), instead of perpetuating the override-with-grounds template.

---

## Cross-references

- **Superseded ADR:** [`docs/adr/2026-05-14-allocation-refresh.md`](2026-05-14-allocation-refresh.md) — prior allocation refresh (DJ30 colder / NAS hotter, inverse of this ADR's pattern). §Open items 1+2 closures from earlier in this session preserve the no-version-bump doctrine that carries forward to this ADR.
- **Prior canonical (now historical):** [`docs/adr/2026-05-16-fxify-correct-timeout-semantic.md`](2026-05-16-fxify-correct-timeout-semantic.md) — the FXIFY-correct timeout semantic locked here is preserved unchanged; only allocations + Pine parameters move.
- **Override-with-grounds template ancestor:** [`docs/adr/2026-05-08-dd-trigger-c2-relock.md`](2026-05-08-dd-trigger-c2-relock.md) — first ADR to use the override-with-documented-grounds pattern for the regime-robustness gate.
- **Worked example for the override-with-grounds template:** `Q-DDP-1/recommendation.md` (evicted 2026-06-05; retrieve via `git show pre-prune-2026-06-05:archive/docs/briefs/Q-DDP-1/recommendation.md`).
- **Regime-robustness gate doctrine:** [`docs/methodology/regime_robustness_gate.md`](../methodology/regime_robustness_gate.md).
- **Anchor evolution trajectory:** [`docs/analytics/mc_anchor_evolution/README.md`](../analytics/mc_anchor_evolution/README.md) — A9 row pins this ADR's canonical anchor in the trajectory record.
- **Code:**
  - `portfolio_mc.py` — `ALLOCATIONS` + `PEPPERSTONE_PANELS`
  - `tests/test_mc_anchors.py` — Pepperstone + OANDA pins + panel-shape pin
  - `dd_protection.py` — `DD_TRIGGER = 0.015`, `DD_SCALE = 0.40` (unchanged)
  - `firm_rules.py` — `_BASE_RISK`
  - `live_journal/scripts/journal_review.py` — `STRATEGIES.risk_pct`
- **Forward-trigger instrumentation:** `analysis/time_to_pass.py --regime-check` mode (established 2026-05-08).

---

## Verification

```
# 1. MC anchor reproduces
$ python portfolio_mc.py --panel pepperstone
# Expected (tail): Pass: 99.83% / Bust: 0.17% / p99 DD: 4.37% / median 26

$ python portfolio_mc.py --panel oanda
# Expected (tail): Pass: 99.58% / Bust: 0.42% / p99 DD: 4.78% / median 27

# 2. Test pins pass
$ python -m pytest tests/test_mc_anchors.py -v
# Expected: 8 passed

# 3. Full test suite green (modulo pre-existing Windows-autocrlf failures in test_ingest.py)
$ python -m pytest -q
# Expected: only the 3 pre-existing test_ingest.py CRLF/LF fixture-byte-identity failures
# remain; all other tests green. The 3 ingest failures pre-date this commit and are
# documented as unrelated Windows-environment artifacts.

# 4. Manifest integrity
$ python scripts/check_data_manifests.py
# Expected: no output (silent success)

# 5. CLAUDE.md / README / regime_robustness_gate.md / repo_context.md / mc_anchor_evolution
#    headline anchor consistency
$ grep -l "99.83" CLAUDE.md README.md docs/methodology/regime_robustness_gate.md \
                  docs/notion/repo_context.md docs/analytics/mc_anchor_evolution/README.md
# Expected: all five files

# 6. Brief-authoring discipline check
$ python ~/.claude/skills/anthropic-skills/brief-authoring/scripts/check_brief.py \
         docs/adr/2026-05-23-allocation-refresh-2.md
# Expected: 6/6 checks PASS
```

---

## Addendum — 2026-07-01 — §Falsifier limbs 2–3 dormancy (retirement back-propagation)

Per operational-rules Rule 11 (retirement events back-propagate to standing
falsifiers), the 2026-07-01 programme audit records that **§Falsifier limbs 2 and 3
— the live `journal_review.py` edge-captured ratio <0.70 over a ≥30-trade post-lock
window, for DJ30 (limb 2) and NAS100 (limb 3) — are DORMANT and cannot currently
accrue.** As of the 2026-06-30 CFD retirement
(`docs/adr/2026-06-30-no-manual-trading-cfd-retirement.md`) manual/live CFD
execution is stopped and FXIFY is idle, so no post-lock live trades accumulate.
NAS100's limb (3) in fact never accrued a single verified fill; DJ30's limb (2) is
additionally unbindable on its stated instrument once the venue moves to MYM
(force-flat-modified). This is **not** a threshold change and §Falsifier is not
edited.

**Why this is load-bearing (not cosmetic):** §Override / §Consequences named "both
the quarterly regime-check **and** the live edge-captured falsifier" as the **dual
retroactive catch-paths** compensating for the regime-robustness gate this ADR
skipped. One of those two paths (the live edge-captured limbs) is now dark. The
surviving path — the quarterly `time_to_pass.py --regime-check` (next **2026-08-08**,
cron-scheduled) — remains in force and continues to carry the retroactive coverage
alone until live execution resumes.

**Re-arm condition:** limbs 2–3 re-arm when the futures automation chain goes live
and post-lock fills accrue on the actual venue. At that point a fresh Pre-Q must
re-map the edge-captured falsifier to the futures fill microstructure (the CFD-era
`cost_proxy.py` band and DXTrade-fill semantics do not transfer — see
`STATE.md` Q-NAS-ECR-1 and the 2026-07-01 SESSIONS note). No config change under
this addendum.

| Date | Change | By |
|---|---|---|
| 2026-07-01 | Addendum: §Falsifier limbs 2–3 (live edge-captured catch-paths) flagged DORMANT under go-dark; one of the two named dual catch-paths is dark, quarterly MC path intact; re-arms on futures go-live via a fresh Pre-Q. No config/threshold change. | Joshua + Claude Code (programme audit) |

---

## Addendum — 2026-08-02 — limb 1 also DORMANT: this ADR now has **zero** live catch-paths

Per operational-rules Rule 11. **This addendum corrects a standing claim made by the
2026-07-01 addendum above**, which states that the quarterly regime-check *"remains in force
and continues to carry the retroactive coverage alone until live execution resumes."*
**That is no longer true, and has not been true since 2026-07-22.**

### What went dark, and when

**Limb 1** — *"Rolling 6-month MC pass-rate on the live-extended Pepperstone panel falls
below 95% for two consecutive 6-month windows … quarterly cadence via
`python analysis/time_to_pass.py --regime-check`, next dates 2026-08-08 / 2026-11-08 /
2027-02-08 / 2027-05-08"* — is dark on **two independent grounds**:

1. **Duty retired 2026-07-22.**
   [`2026-07-11-challenge-era-claims-rescope.md`](2026-07-11-challenge-era-claims-rescope.md)
   §Addendum 2026-07-22 (D2 resolved by retirement): *"`python lab/analysis/time_to_pass.py
   --regime-check` is no longer a standing quarterly obligation, and the 2026-08-08 /
   11-08 / 2027-02-08 / 2027-05-08 dates carry **no revert-check duty**."* Grounds: the
   criterion is challenge-denominated and the FXIFY venue is closed.
2. **Tool no longer executes.** Independently, substrate Phase 3 (2026-07-24, `bd92d8e`)
   retired the Pepperstone executable anchor. Verified 2026-08-02:

   ```
   $ python lab/analysis/time_to_pass.py --regime-check
   ValueError: No registered broker panel. The Pepperstone executable anchor was retired
   (ADR 2026-07-22 Phase 3).
   ```

   Note the harness **file still exists** — only running it reveals the darkness. A
   path-existence check scores this limb REACHABLE.

**Limbs 2–3** were already recorded DORMANT on 2026-07-01 (above); `journal_review.py` has
zero occurrences in any `.py` in the tree as of 2026-08-02.

### Why this is load-bearing

§Override and §Consequences named *"dual retroactive catch-paths"* — the quarterly
regime-check **and** the live edge-captured falsifier — as compensation for the residual
regime risk this ADR accepted. **Both are now dark.** The allocations they were watching
(DJ30 0.70% / pyramid 750%, NAS100 0.37%) are **live today**.

**Correction to an earlier reading of this ADR (recorded so it is not re-derived):** the
regime-robustness gate was **not mandatory** here and was not "skipped in violation."
[`docs/methodology/regime_robustness_gate.md`](../methodology/regime_robustness_gate.md)
§"When this gate fires" has listed *"Allocation changes (governed by variance-contribution
+ MC re-balance methodology)"* under **Not required for** since its canonization commit
`26f3a26` (2026-05-06) — 17 days before this ADR, and untouched by this ADR's own lock
commit `5b8ff71`. This ADR's §Consequences called the scope *"ambiguous-in-scope for
allocations"* and self-imposed catch-paths anyway, i.e. it was **more** conservative than
methodology required. What is dark is the **forward monitoring** this ADR volunteered —
not a mandatory gate.

This ADR's §5 lists as a forbidden move: *"**Skipping the next four quarterly
`time_to_pass.py --regime-check` runs.** The override's only retrospective safety net is the
quarterly cadence."* The 2026-07-22 retirement retired exactly those four runs. The two
decisions are in direct collision and the collision was never recorded — the retiring
addendum's own §Downstream sweeps only the substrate-retirement ADR, so Rule 11
back-propagation to this ADR did not happen.

**Scope honesty — what the retirement DID leave standing, and why it does not cover this
ADR.** The D2 addendum argues change-control passes to the concept-not-constant chain
(pre-registration → re-MC → both-halves regime gate → admitting ADR), *"strictly stronger
than the retired trigger."* That is correct **for `dd_protection`'s `(trigger, scale,
reference_mode)`** — which is that chain's stated scope. **This ADR is an allocation
decision** (risk % and pyramid per strategy), not a `dd_protection` constant. The successor
chain therefore does not inherit this ADR's coverage. No claim is made here that the
allocations are wrong, that risk has changed, or that any number should move — only that the
**evidence base the override was granted against no longer exists**.

### Re-arm condition

Limb 1 does **not** re-arm by re-running the harness: both its criterion (challenge
pass-rate) and its input (the executable Pepperstone panel) were retired by decision. It
re-arms only if a panel-bearing executable anchor is re-registered **and** a successor
criterion is derived that is not challenge-denominated — each needing its own ADR. Limbs 2–3
re-arm per the 2026-07-01 addendum (futures fills accrue + fresh Pre-Q).

### The retrospective question is ALREADY ANSWERED — and this ADR never says so

The obvious remedy ("run the both-halves regime gate retroactively") is **redundant: it was
already run against this exact locked config, on a harder panel, and it FAILED.**

[`2026-06-07-decompound-remc-hold.md`](2026-06-07-decompound-remc-hold.md) (`Accepted`,
`Superseded-by: none`) names this ADR in its own header as *"the locked config being
characterized"* and `regime_robustness_gate.md` as *"the gate applied."* Its clean-vintage
re-run ([`RESULTS_cleanvintage_2026-06-25.md`](../../lab/analysis/regime/decompound_remc_2026-06-07/RESULTS_cleanvintage_2026-06-25.md)
§"Half-panel regime cut (Part B)") reports, for **LOCKED k=1.0**:

| Partition | pass | bust | p99 DD | median | verdict |
|---|---:|---:|---:|---:|:---:|
| H1 2020-01→2023-03 (843bd) | 86.16% | **13.84%** | **7.76%** | 62 | **FAIL** |
| H2 2023-03→2026-06 (844bd) | 99.79% | 0.21% | 4.53% | 20 | PASS |

against the floor *bust<1% AND p99<5%*. Notes carried from that run: *"Locked-config H1
isolated for the first time"*, and Part A (bootstrap) was **deliberately not run** because
*"the bootstrap can only matter when H1 passes."* That reasoning applies here too — the
locked config fails H1, so the full gate (bootstrap AND H1 AND H2) fails regardless.

That panel is **stricter** than anything this ADR's own gate would have used: full-history
2020-06 decompounded, versus this ADR's 2022-01→2026-05 compounded window.

The disposition was **HOLD**, on the ground that *no viable static sizing config (allocation
or dd_protection) is regime-robust* — both de-risk candidates also FAIL H1, and pass gates
only by making the challenge impractical (≥367d median). So the regime risk on these
allocations is **measured, worse than this ADR assumed, and consciously accepted.**

**The actual defect is discoverability, and it is one-directional.** The decompound ADR
points at this one; `rg "decompound|2026-06-07"` over this file returns **nothing**. A
reader of this ADR sees "regime gate not run + two catch-paths" and never learns the gate
was effectively run and failed. That cross-reference is what this addendum supplies.

### Open item — narrowed to the forward gap only

Retrospective coverage: **discharged** (decompound HOLD, above). Not re-opened.

What remains genuinely missing is **forward** monitoring — the catch-paths were tripwires
for a *future* regime shift, and a retrospective measurement is not a tripwire. Options,
none taken here:

1. **Derive a successor forward monitor** under the current venue (c1 / Tradeify), on an
   interpretable denominator. Note the constraint that retired the last one: a
   challenge-denominated pass-rate is uninterpretable with the venue closed
   ([`2026-07-11-challenge-era-claims-rescope.md`](2026-07-11-challenge-era-claims-rescope.md)
   §Addendum 2026-07-22), so a successor must not be pass-rate-shaped.
2. **Accept the absence of a forward monitor explicitly**, dated, on the ground that the
   decompound HOLD already characterizes the tail and the book is unchanged since.

Doing nothing leaves the 2026-07-01 addendum's "coverage alone" claim standing and false,
which is the exact failure Rule 11 exists to prevent.

**Forbidden under this addendum:** re-running the both-halves gate as if the answer were
unknown, or inventing a pass-rate floor for it. `regime_robustness_gate.md` §Edge cases:
*"The gate's pass-rate floor must equal the brief's full-panel pass-rate floor. No separate
'regime floor' is permitted — that would be a hidden parameter through which post-hoc
fitting could enter."* This ADR has no pre-registered floor, so a retroactive gate run
would have to invent one.

**NOT changed by this addendum:** every allocation, threshold, constant, Pine parameter, and
the §Falsifier text itself. This is a coverage-status recording only.

| Date | Change | By |
|---|---|---|
| 2026-08-02 | Addendum: limb 1 (quarterly `time_to_pass.py --regime-check`) flagged DORMANT on two grounds — duty retired 2026-07-22 (D2), harness `ValueError` post-Phase-3. Corrects the 2026-07-01 addendum's "carries coverage alone" claim: **all three catch-paths are now dark**. §5's "do not skip the four quarterly runs" clause collided with the 07-22 retirement, unrecorded until now. Also records two corrections: the regime-robustness gate was **never mandatory** for allocation changes (exempt since `26f3a26`, 2026-05-06), and the retrospective regime question is **already answered** — the decompound HOLD (2026-06-07 / clean vintage 06-25) applied the gate to this locked config on a stricter full-history panel and it **FAILS H1** (bust 13.84%, p99 7.76%), consciously HELD. Cross-reference supplied; open item narrowed to the **forward** monitor only. No config/threshold/allocation change. | Joshua + Claude Code (falsifier reachability census) |
| 2026-08-15 | Addendum: forward-monitor open item (2026-08-02 addendum, option 2 of 2) **discharged — absence accepted explicitly.** Option 1 (derive a venue-native successor monitor under c1/Tradeify) remains structurally blocked: `STATE.md` records the successor design "landed (not ratified); gated on first live fill", and the 2026-08-04 Tradeify de-scope removed the only live-execution surface the estate has — "no route" per `STATE.md`'s own five-stranded-threads note. A monitor gated on a precondition with no route is not "pending," it is closed until that precondition changes. **Disposition:** the DJ30/NAS100 allocation (0.70%/pyramid 750%, 0.37%/pyramid 1000%) has **zero forward regime tripwire today** — recorded as an accepted, dated fact, not an oversight. **Re-arm condition (unchanged from 2026-08-02):** a live-fill route reopens (fresh Pre-Q required to re-map the falsifier to futures-fill microstructure) **or** a panel-bearing executable anchor is re-registered with a non-challenge-denominated successor criterion. No config/threshold/allocation change. Discharges the F2 follow-up in the [2026-08-03](../notes/audits/programme-audit/2026-08-03-gate-stack-audit.md)/[2026-08-15](../notes/audits/programme-audit/2026-08-15-msl-wall-scope-audit.md) gate-stack audits. | Joshua (operator directive) + Claude Code |
