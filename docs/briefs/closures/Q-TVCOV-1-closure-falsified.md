# Q-TVCOV-1 — CLOSURE: `FALSIFIED` (H — 2022 trade-rate break is real; MYM operator BREAK-REAL)

**Verdict:** `CLOSED-FALSIFIED` — H (coverage-artifact) **FALSIFIED** for 6J + MNQ; MYM grid
`AMBIGUOUS` → **operator-accepted BREAK-REAL** 2026-07-13. Roster row bookkeeping-closed under
GSUB-1 **2026-08-09** (no re-verdict).
**Closed:** 2026-07-13 (verdicts) · roster closure 2026-08-09 (GSUB-1 c4)
**Pre-registration / parent:** [`Q-TVCOV-1-tv-bar-coverage-census.md`](../Q-TVCOV-1-tv-bar-coverage-census.md)
**Spend / K:** $0.00 billed Databento pulls · K=0
**Live effect:** none — panels retain evidential standing (MYM: annotate 2020-03-16 TV hole);
roll-rule pin (`.v.0` not `.c.0`) already discharged in `databento-data` skill reference since
2026-07-13
**Artifacts:** [`RESULTS.md`](../../../lab/analysis/c1/tvcov_2026-07/RESULTS.md) ·
[`pursuit c4`](../../pursuits/c4-q-tvcov-1.md) ·
[`GSUB-1 inventory` row c4](../GSUB-1-inventory-and-dispositions.md)

> **Records-completeness note (2026-08-11).** INDEX Recently closed and the GSUB-1 pursuit record
> both state a formal closure brief was never authored. This file reconstructs the disposition
> from RESULTS + c4 + INDEX prose — **not** a new adjudication.

---

## 1. Verdict (§6 asserted against actual numbers)

From [`RESULTS.md` §Verdict / §Falsifier disposition](../../../lab/analysis/c1/tvcov_2026-07/RESULTS.md)
(corrected `.v.0` series; first-pass `.c.0` 6J ARTIFACT-CONFIRMED **withdrawn**):

| Instrument | §6 / limb outcome | Fired? |
|---|---|---|
| 6J | **H FALSIFIED — break real** (pre-break coverage complete; TV matches canonical exactly on all 5 pre-break months) | ✓ |
| MNQ | **H FALSIFIED — break real** | ✓ |
| MYM | Grid **AMBIGUOUS** (limb-(b) one month −4.3% = single missing TV day 2020-03-16) → **operator BREAK-REAL** | ✓ (parent call) |

Standing annotation: wherever 2020-Q1 Striker-MYM behavior is analyzed, note TV MYM 15m history
missing Sun 2020-03-15 18:00 ET → Mon 2020-03-16 17:59 ET.

## 2. What the pre-registration predicted vs what happened

The audit's first-pass used calendar-rolled `.c.0` and briefly issued a 6J ARTIFACT-CONFIRMED /
pre-2022 NON-EVIDENTIAL read — **withdrawn same day** after roll-rule attribution proved the
thinness was serial-month mapping, not feed coverage. Corrected `.v.0` flipped 6J/MNQ to
H FALSIFIED (break real). MYM stayed grid-AMBIGUOUS; operator accepted BREAK-REAL.

## 3. What this closure does NOT license

- Downgrading the 2026-07-12 seven-year panels (RESULTS: retain evidential standing).
- Re-opening the coverage-artifact H on the same instruments/months without new mechanism
  evidence (different feed class, different roll protocol, or a day TV actually served that was
  previously missing).
- Treating GSUB-1's roster close as a fresh kill — it was bookkeeping after verdicts already
  landed (`SUBTRACT-complete`).

## 4. Defects found in the frozen brief (recorded, not repaired)

GSUB-1 inventory transcribed a stale "roll-rule pin still open" residual; verified already
discharged in `.claude/skills/databento-data/reference/schemas-and-symbology.md` since
2026-07-13 — recorded on [`c4`](../../pursuits/c4-q-tvcov-1.md). Not repaired here.

## 5. Lesson candidates

Roll-rule determines which bars *exist* (not merely price continuity); `.v.0` is the
TV-`1!`-equivalent for counts-based audits. Dated 2026-07-13 in RESULTS §Roll-rule attribution —
already pinned in the databento-data skill.

---

## Iterate — loop exit

- **Verdict used:** `CLOSED-FALSIFIED` (H FALSIFIED / MYM operator BREAK-REAL)
- **Model update:** the 2022 trade-rate break is real market/session structure, not a TV coverage
  artifact; the audit's own first-pass symbology choice was the near-miss.
- **Next:** STOP
- **Routing:** STOP — residuals assigned on c4 (MYM annotation → operator; roll-rule pin
  discharged). Campaign ACTIVE CATALOG row may still hold the lab body; archival is separate
  lab housekeeping, not owed by this closure.
- **Entry packet:** n/a — STOP
- **Stop rule / re-proposal bar:** new mechanism evidence about bar *availability* (not a
  re-census of the same nine quarterly-expiry months on `.c.0`).
- **Board write:** none — STOP, nothing owed (INDEX Recently closed + c4 pursuit already carry
  the disposition; GSUB-1 closed the roster row 2026-08-09).

## §10 audit-hook discharge

```bash
ls docs/briefs/closures/Q-TVCOV-1-closure-falsified.md
rg -n 'H FALSIFIED|BREAK-REAL|Operator disposition' lab/analysis/c1/tvcov_2026-07/RESULTS.md | head
rg -n 'Q-TVCOV-1' docs/briefs/INDEX.md docs/pursuits/c4-q-tvcov-1.md
python3 -X utf8 scripts/check_closure_disposition.py docs/briefs/closures/Q-TVCOV-1-closure-falsified.md
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-13 | Verdicts landed in RESULTS | Claude Code spawn |
| 2026-08-09 | Roster SUBTRACT-complete (GSUB-1 c4); formal closure still unnamed | GSUB-1 |
| 2026-08-11 | Formal closure stub authored from RESULTS + c4 (records-completeness) | Cursor Cloud Agent |
