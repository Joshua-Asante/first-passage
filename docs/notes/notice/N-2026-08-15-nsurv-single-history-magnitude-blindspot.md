# Notice — N-SURV's single-history convention may be blind to magnitude uncertainty on skew-heavy books

**Notice ID:** N-2026-08-15-nsurv-single-history-magnitude-blindspot
**Observed:** 2026-08-15
**Author:** Claude Code (parent-side computation, fell out of building a Q-GEOFIT-1 successor family — not the task that was being run)
**Source:** `lab/analysis/c1/geofit_skewed_family_construction_2026-08-15/characterize.json` (this session's own MC output)
**Status:** `GRADUATED to Q-NSURV-1` (2026-08-20, operator ruling, in-session direct instruction "graduate N-SURV") — see [`Q-NSURV-1`](../../briefs/Q-NSURV-1-single-history-magnitude-blindspot.md) / [`closure`](../../briefs/closures/Q-NSURV-1-closure-resolved.md), `RESOLVED` same day. §4/§5 below preserved as the historical record of the HOLD reasoning; superseded by the graduation, not edited.
**Lives in:** `docs/notes/notice/N-2026-08-15-nsurv-single-history-magnitude-blindspot.md`

---

## §0 — Source anchor

- **Source:** [`geofit_skewed_family_construction_2026-08-15/characterize.json`](../../../lab/analysis/c1/geofit_skewed_family_construction_2026-08-15/characterize.json) — 50 MC realizations of a family fit to the real c1 book.
- **Observed at:** 2026-08-15, same session as [`geofit_iid_sufficiency_power_2026-08-15`](../../../lab/analysis/c1/geofit_iid_sufficiency_power_2026-08-15/README.md) and the family construction it followed.
- **Mechanism claim verified against production, not assumed:** `run_partition_mc` (`lab/analysis/c1/geofit_iid_sufficiency_power_2026-08-15/run_class_s_c1_regime_gate.py:96`, retrieved read-only from `pre-prune-2026-08-08` — original live path `lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/`, deleted by the Great Prune `283d1de`) calls `blocks_from_daily_pnl` (`lab/discovery/prop_survivor_scoring.py:327`, live, `0356be2` 2026-08-11), which builds Mon-anchored week-blocks from **one fixed, already-observed** daily series. The bootstrap inside `run_tier_remc`/`run_seed` resamples which blocks appear and in what order across simulated equity paths — it never redraws the **magnitude** of a day's P&L. Confirmed by reading both functions this session, not inferred from behavior.

---

## §1 — The observation

Fitting a skew-aware i.i.d. family to the real c1 book's own moments (n=150 real win-days, mean $463, median $85, max $4,972 — 10.7× the mean) and drawing 50 fresh realizations produced a bust-rate distribution with mean 7.46%, sd 7.07pp, and only 15/50 (30%) clearing the trailing-DD survival gate (bust≤3.0% ∧ pass≥50%). The real book's own single historical bust (4.7433%) sits at roughly the 44th percentile of that distribution — not a lucky draw, close to the shape's own median.

`run_partition_mc` — the engine behind every N-SURV verdict in this estate — never generates this second kind of uncertainty. It only resamples the order of blocks drawn from the one history that actually happened.

---

## §2 — Why it stands out

- **Baseline:** every closed N-SURV verdict (Q-TXG-1's two transfer cells, Guardian→MGC, Q-COMPOSE-1, ORB-MNQ-1, and c1's own historical record) reads a single-history block-bootstrap bust rate as if it were the candidate's survival probability.
- **Delta:** for this book's shape, a second, unmeasured source of uncertainty — would a different, equally-plausible history from the same underlying process produce a similar bust rate — is 7.07pp wide. The single-history read carries none of it.
- **Frequency check:** first time this specific gap has been measured directly in this estate. It is adjacent to, and sharpens, an existing finding: the 2026-08-03 gate-stack audit named G5 envelope rule E3 (the trailing-barrier rule) as never having acquired a level, "enforced only by G1's downstream MC" (`docs/notes/audits/programme-audit/2026-08-03-gate-stack-audit.md` §5.4). That audit did not have this mechanism measured; this notice supplies one candidate reason the downstream MC alone may not be enough.

---

## §3 — Candidate mechanisms (informal)

- **A — genuine methodology gap.** Single-history block-bootstrap systematically understates true survival-probability uncertainty for skew-heavy candidates, because it treats the one 6-year history that happened as if it fully characterizes the underlying process.
- **B — small-sample estimation noise, not process variability.** The fitted win-branch shape (Gamma k≈0.359) comes from only 150 real win-days; some of the 7.07pp spread may reflect uncertainty in the FIT itself rather than true variability in the process the real book was drawn from. This does not fully explain the finding away — even generous allowance for estimation noise, a 30% clear rate at the fitted shape's own central tendency is still informative — but it has not been ruled out, and I have not attempted to separate the two sources.
- **C — idiosyncratic to this one book.** Only c1 has been tested. Whether other skew-heavy candidates (or symmetric ones, as a control) show a comparably wide gap between single-history and magnitude-resampled uncertainty is untested. This is exactly why it is a Notice, not a ruling.

---

## §4 — Routing decision

**HOLD.** Reason: this observation's scope and priority — whether it warrants a dedicated Pre-Q, whether it should be checked against any specific closed N-SURV verdict, and whether the estate's terminal survival gate needs a second uncertainty layer at all — is an operator call, not a mechanical trigger. The finding is concrete and reproducible (one committed artifact, `characterize.json`), but it rests on one case study and does not by itself justify re-opening anything.

---

## §5 — If HOLD: re-check trigger

- **Re-check date:** none set — operator-triggered, not calendar-triggered.
- **Trigger condition:** an explicit operator ruling on scope (graduate to a Pre-Q measuring the same gap on a second, independently-fitted candidate; apply it as a re-read of one specific closed verdict; or drop as idiosyncratic to c1 pending stronger evidence).
- **Drop trigger:** if a future, properly-designed test (e.g., the same magnitude-resampling exercise on a symmetric, thin-tailed candidate) shows a comparably wide single-history/resampled gap even without skew, this notice's framing (skew-heavy books specifically) would be wrong and should be corrected or dropped in favor of a broader, less specific finding.
- **Calendar entry:** none — see re-check condition above.

**Forbidden moves, this notice:**
- Treating the 30% clear rate as the c1 book's true survival probability — it is the clear rate of one uncapped parametric fit on 350 days of data, itself carrying real estimation uncertainty (§3-B).
- Retroactively re-opening or invalidating any specific closed N-SURV verdict on the basis of this notice alone.
- Building a fix (wiring magnitude-resampling into `run_partition_mc`, adding a second uncertainty layer to the gate) without a dedicated Pre-Q — this notice observes, it does not prescribe.
- Citing this notice as if it discharges G5 envelope rule E3's missing level — it sharpens why that gap matters; it does not close it.

---

## §10 — Audit hooks

```bash
# The finding this notice rests on is reproducible from a committed artifact
python -c "import json; d=json.load(open('lab/analysis/c1/geofit_skewed_family_construction_2026-08-15/characterize.json', encoding='utf-8')); print(d['bust_mean'], d['bust_sd'], d['bust_percentiles'])"
# expect: mean ~0.0746, sd ~0.0707, p50 ~0.0557

# The mechanism claim (order-only resampling) is checkable against the live module
grep -n "def blocks_from_daily_pnl" lab/discovery/prop_survivor_scoring.py
# expect: builds week-blocks from a passed-in daily series; no distribution fit inside it

# If GRADUATED: confirm the Pre-Q references this notice
grep -rn "N-2026-08-15-nsurv-single-history-magnitude-blindspot" docs/briefs/Q-*.md
```

---

## Verification

```bash
python .claude/skills/brief-authoring/scripts/check_brief.py docs/notes/notice/N-2026-08-15-nsurv-single-history-magnitude-blindspot.md --type notice
```
