# Q-NSURV-1 — Is the N-SURV single-history magnitude blindspot a general methodology gap, or idiosyncratic to one book?

**Status:** `OPEN — DRAFT (pre-lock)`, closing same-day (see closure)
**Authored:** 2026-08-20
**Closed:** 2026-08-20
**Authors:** Joshua + Claude Code (Sonnet 5)
**Parent question:** `N-2026-08-15-nsurv-single-history-magnitude-blindspot` (Notice-phase; this Q is its named graduation)
**Sub-questions opened:** N/A
**Loop:** Inquire-phase Pre-Q — gates whether `run_partition_mc`'s single-history block-bootstrap systematically understates survival-probability uncertainty across the estate, or only for the one book that first surfaced it
**Artifact path:** `docs/briefs/Q-NSURV-1-single-history-magnitude-blindspot.md`

---

## §0 — Rule 0 reads (production-source verification)

- `lab/discovery/prop_survivor_scoring.py` — anchor `027a729` (2026-08-14). `blocks_from_daily_pnl` confirmed to build week-blocks from one fixed, already-observed daily series; the bootstrap resamples block order/selection, never P&L magnitude.
- `docs/notes/notice/N-2026-08-15-nsurv-single-history-magnitude-blindspot.md` — anchor `19139a7` (2026-08-16). The Notice this Q graduates; §4/§5 name graduation to a Pre-Q testing a second, independently-fitted candidate as the explicit trigger condition.
- `lab/analysis/c1/geofit_skewed_family_construction_2026-08-15/characterize.json` — anchor `19139a7` (2026-08-16). First candidate: c1 book, N=50 magnitude-resampled realizations.
- `lab/analysis/c1/orbmnq1_nsurv_magnitude_probe_2026-08-20/run_nsurv_magnitude_probe.py` — anchor `bf81496` (2026-08-20, this session). Second candidate: ORB-MNQ-1, N=50 magnitude-resampled realizations, independently adversarially verified (CONFIRMED) same session.

**Honesty note on pre-registration (§8 below):** unlike this session's other closed Qs tonight (`Q-ORBCUSH-1`), the two data points this Q synthesizes were **not** gathered under a blind pre-registration written before either was seen — the c1-book result has existed since 2026-08-15, and the ORB-MNQ-1 result was gathered tonight to answer a different, narrower question (is ORB-MNQ-1's own bust-elimination finding a lucky single-history draw), not framed in advance as a test of this Q's own hypothesis. This Q is a **retrospective synthesis** of two independently-verified measurements, not a fresh blind test. Disclosed here rather than dressed up as more rigorous than it is — see §8.

---

## §1 — Context & motivation

The parent Notice (2026-08-15) found that `run_partition_mc` — the engine behind every closed N-SURV survival verdict in this estate (Q-TXG-1's two transfer cells, Guardian→MGC, Q-COMPOSE-1, ORB-MNQ-1, c1's own historical record) — only ever resamples block *order* from one observed history, never the *magnitude* of a day's P&L. On the c1 book, magnitude-resampling a skew-aware fitted family produced a bust-rate distribution 7.07pp wide, with only 30% of realizations clearing the survival gate the single real history reads as a pass. The Notice held, explicitly, because it rested on one case study and could not distinguish a general methodology gap (Mechanism A) from something idiosyncratic to c1's own shape (Mechanism C).

Tonight, unrelated to this question at the time, a second candidate got the identical treatment: ORB-MNQ-1's own cushion-sized bust-elimination finding was magnitude-resampled (N=50, same `family_skewed_gamma` machinery) to check whether it was a lucky single-history draw. It wasn't lucky on the bust axis (50/50 realizations, 0.00% every time) — but the pass axis showed real spread (sd 24.17pp, combined-gate clear rate 50%). Two independent books, two structurally different sizing mechanisms (flat vs. cushion-proportional), both show a materially wide single-history-vs-resampled gap — just on different axes. That is exactly the second data point the Notice named as its graduation trigger.

---

## §2 — Prior art / lineage

- **Parent Notice** (`N-2026-08-15-...`, `HOLD`) — full mechanism claim, first data point, and the exact graduation trigger this Q discharges.
- **`geofit_skewed_family_construction_2026-08-15`** (`lab/CATALOG.md`, HOLD) — built the general-purpose `family_skewed_gamma.py` fitter and produced the c1-book data point.
- **`orbmnq1_nsurv_magnitude_probe_2026-08-20`** (this session, `ops/instruments/MNQ.md` N18) — produced the second data point, independently adversarially verified same session (CONFIRMED: fit-quality independently re-derived analytically, all 50 realizations present, fresh rerun bit-for-bit reproduced).
- **`docs/notes/audits/programme-audit/2026-08-03-gate-stack-audit.md` §5.4** — named G5 envelope rule E3 (the trailing-barrier rule) as "enforced only by G1's downstream MC," without this specific mechanism measured. This Q sharpens, but does not close, that gap.

---

## §3 — Question (Q-NSURV-1)

**Pre-Q gate test:** "does the single-history blindspot generalize, or is it idiosyncratic to one book" names the symptom (an unverified scope boundary) and the missing thing (a second data point), not a fix. Passes.

**Q-NSURV-1:** Given two independently-fitted candidates now magnitude-resampled under the identical methodology, does the single-history-vs-resampled gap look like a general property of `run_partition_mc`'s bootstrap design (Mechanism A), or does it look confined to one book's shape (Mechanism C)?

---

## §4 — Falsifiable hypothesis (H-NSURV)

**H-NSURV:** If **both** independently-fitted candidates show a materially wide single-history-vs-resampled gap on at least one gate-relevant axis (defined, matching the magnitude actually observed on the first candidate: resampled sd ≥5pp on bust% or pass%, OR a combined-gate clear rate ≤80% i.e. ≥20% of realizations would flip the single-history verdict) — **then** Mechanism A is supported: this is a general property of the single-history bootstrap design, not confined to c1. **Otherwise**, if the second candidate shows no material spread on any gate-relevant axis, Mechanism C is favored and the finding stays scoped to c1's own shape.

**Reject H-NSURV if:** the second candidate (ORB-MNQ-1) shows resampled sd <5pp on every gate-relevant axis AND combined-gate clear rate >80%.
**Accept H-NSURV if:** the condition above fires on at least one axis for the second candidate, matching what the first candidate already showed.
**Ambiguous-hold if:** the second candidate's fit-quality control fails (family doesn't credibly match the candidate's own real moments), making its resampled distribution untrustworthy regardless of spread.

---

## §5 — Forbidden moves

- **Treating this Q's RESOLVED verdict as re-opening or invalidating any specific closed N-SURV verdict.** Carried forward verbatim from the parent Notice's own forbidden-moves list (§5 of that file) — this Q confirms the mechanism is general; it does not re-score anything.
- **Building a fix** (wiring magnitude-resampling into `run_partition_mc`, adding a second uncertainty layer to the gate) **under this Q.** The parent Notice bars this explicitly ("this notice observes, it does not prescribe") and nothing here changes that — a fix needs its own dedicated brief and operator GO, deliberately deferred to a future session per operator direction (2026-08-20).
- **Papering over the axis mismatch between the two candidates** (c1: bust-axis spread; ORB-MNQ-1: pass-axis spread, bust pinned at 0%) as if they were the same measurement. They aren't — the sizing mechanism determines which axis carries the uncertainty. Stated as a finding, not smoothed away, in §6/closure.
- **Backdating this synthesis as if it were a blind pre-registered test.** It wasn't (§0 honesty note) — the threshold in §4 is stated using the magnitude the first candidate already showed, which is a real limitation on how much this Q's own "falsification" should be trusted as bias-free. Disclosed, not hidden.

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED` | H-NSURV's Accept condition fires — second candidate shows material spread on ≥1 gate-relevant axis | `INTEGRATE — graduate the parent Notice from HOLD to GRADUATED; record the confirmed-general mechanism in a durable, cross-cutting location (not a single instrument ledger, since this bears on every N-SURV verdict); name the deferred fix-design question as an explicit forward obligation, not opened here` |
| `FALSIFIED` | H-NSURV's Reject condition fires | `STOP — parent Notice's framing (skew-heavy books specifically) narrows to c1 only; re-proposal bar is a third candidate showing the gap before re-generalizing` |
| `AMBIGUOUS-HOLD` | second candidate's fit-quality control fails | `ITERATE — return to a fresh magnitude-resampling probe on a better-fitting family or a different second candidate; re-test window 2026-11-08` |

---

## §7 — Execution plan

Already executed, retrospectively — see §0/§2. No Phase 1 owed.

---

## §8 — Verdict pre-registration

**Not filed as a separate frozen file.** Per §0's honesty note, this Q synthesizes two already-gathered, already-independently-verified measurements rather than gating a fresh blind test — a separate pre-registration file would misrepresent the actual sequence of events (both data points existed, in one case for five days, before this Q's own hypothesis was framed). The §4 threshold is stated transparently using the first candidate's own already-observed magnitude, disclosed as a real limitation, not concealed. This is a deliberate, judgment-call departure from the standing §8 convention, named explicitly rather than silently skipped.

---

## §9 — Closure record format

Closing same-day; see `docs/briefs/closures/Q-NSURV-1-closure-resolved.md`.

---

## §10 — Audit hooks (runnable)

```bash
# Confirm §0 anchors still resolve
git log -1 --format='%h' -- lab/discovery/prop_survivor_scoring.py               # expect 027a729
git log -1 --format='%h' -- docs/notes/notice/N-2026-08-15-nsurv-single-history-magnitude-blindspot.md  # expect 19139a7

# Reproduce candidate 1 (c1 book)
python -c "import json; d=json.load(open('lab/analysis/c1/geofit_skewed_family_construction_2026-08-15/characterize.json', encoding='utf-8')); print(d['bust_mean'], d['bust_sd'])"

# Reproduce candidate 2 (ORB-MNQ-1)
python lab/analysis/c1/orbmnq1_nsurv_magnitude_probe_2026-08-20/run_nsurv_magnitude_probe.py

# Confirm the parent Notice's status reflects graduation
grep -n "Status" docs/notes/notice/N-2026-08-15-nsurv-single-history-magnitude-blindspot.md
```

---

## Verification

```bash
$ PYTHONIOENCODING=utf-8 python scripts/check_brief.py docs/briefs/Q-NSURV-1-single-history-magnitude-blindspot.md
```
