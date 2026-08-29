# Notice — MYM overnight gap magnitude → RTH-range conditioning (cheap falsifier)

**Notice ID:** N-2026-08-29-mym-gap-magnitude-rth-range
**Observed:** 2026-08-29
**Author:** Joshua | claude.ai
**Source:** backtest CSV (bar panel) — atheoretical mechanism harvest, MYM Phase 2
**Status:** `DROPPED`
**Lives in:** `docs/notes/notice/N-2026-08-29-mym-gap-magnitude-rth-range.md`

---

## §0 — Source anchor

- **Source:** `core/data/bar_data/MYM_M15.csv` (sha256
  `24e169528f7ea6693b75c71c3195edf6a04f3a26c6b6dff0f2e9c623fd597a58`). Gap defined as
  today's RTH open − yesterday's RTH close (standard equity-style gap), magnitude only
  (`|gap|`), sign discarded. Script:
  `lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c2_c4_increment_falsifiers.py`.
  Results: `.../c2_c4_results.json` key `candidate4_gap_magnitude`.
- **Observed at:** 2026-08-29 (this session).

---

## §1 — The observation

**Constraint-audit catch, before running anything:** the originating brief scoped this
candidate as "fully open ground" needing only its own corrected-battery run (no MNQ
external corroboration to lean on either way). On inspection, gap magnitude and RTH
range are — like candidate 2's overnight range — **different series measured the same
session**, sharing the same slow common-volatility-regime confound that pauses the "S2"
construct in the frozen spec (`docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md`
§4 D5). This is the same catch made for candidate 2, generalized here rather than
re-discovered from scratch: independent-series IAAFT surrogation would not delete the
confound, so no full battery was run — only the same $0 cheap falsifier.

Falsifier: does today's own |gap| magnitude (top-quintile, strict-prior 60 sessions)
predict an elevated RTH range **better than** yesterday's own RTH-range state already
does? Result on n_common=1,307 matched sessions: gap-conditioned obs=0.6268 (n_cond=284)
vs. day-history-conditioned obs=0.7306 (n_cond=297) — diff **−0.1039**, 95%
block-bootstrap CI **[−0.1636, −0.0404]**, p=0.0015. Gap-magnitude conditioning is
*decisively worse* than the mundane comparator, not merely uninformative.

## §2 — Why it stands out (the N signal)

- **Baseline:** the mundane day-history comparator (0.7306), and the unconditional rate
  implicit in the panel (~0.5, per candidate 2/3's disclosures).
- **Delta:** −10.4pp, CI entirely below 0 — a clean, confident kill, not a near-miss.
- **Frequency check:** first instance; no MNQ (or any-instrument) external corroboration
  exists for this exact construct on MYM (Mesfin 2026, cited in the originating brief,
  is MNQ-only and concerns fill/fade *direction*, not magnitude) — this session supplies
  the first measurement in either direction.

## §3 — Candidate mechanisms (informal)

- None needed — the result is a clean NO-INCREMENT, not a near-miss inviting a mechanism
  story.
- If anything, the negative direction is mildly interesting on its own (gap-conditioning
  actively worse than a naive persistence baseline) but not worth a separate
  investigation at this magnitude/sample.

## §4 — Routing decision

**DROP.**

Reason: clean NO-INCREMENT per the S2 un-pause precondition's own precommitted rule
("no increment → S2 dies for $0") — here decisively so, CI entirely below 0. Gap
magnitude carries no useful information about same-session RTH range beyond what
yesterday's own RTH-range state already supplies, and in fact underperforms it. No
further design work (joint-surrogate battery, operator GO) is warranted for this
specific construct.

---

## §10 — Audit hooks

```bash
python lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c2_c4_increment_falsifiers.py
# Expected: [candidate4_gap_magnitude] diff=-0.1039  95% CI=[-0.1636,-0.0404]  p=0.0015  VERDICT=NO-INCREMENT

grep "N-2026-08-29-mym-gap-magnitude-rth-range" docs/briefs/Q-*.md
# Expected: no matches (DROPPED, not graduated)
```

---

## Verification

```bash
$ python ~/.claude/skills/brief-authoring/scripts/check_brief.py \
    docs/notes/notice/N-2026-08-29-mym-gap-magnitude-rth-range.md --type notice
# Expected: RESULT: well-formed
```
