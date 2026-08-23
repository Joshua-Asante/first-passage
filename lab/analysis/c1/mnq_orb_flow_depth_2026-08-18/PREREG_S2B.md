# `MNQFLOW-1-DEPTH` — S2 redraw (`S2B`), after the original sample's P0 abort

**Status:** `HOLD 2026-08-23 (operator) — value-uncertain, not cost-blocked.` §9.1 signed;
§2.2's P0 re-estimate on these 30 dates came back **$154.7320**, over the $125.00 ceiling (see
§9.2) — a structural finding, not a resolved credit question (two independent draws both land
18–24% over; the true cost is nearer $150). Presented with three named paths (raise the
ceiling / smaller-N pre-registration / decline), the operator elected **none of them**: *"I am
not ruling it out but I do not know if it is worth the spend."* Recorded verbatim, not
rounded to the nearest named path — this is a genuine fourth disposition (HOLD), not a
soft decline. No forced re-test date; naturally revisited at the 2026-11-08 slate the
deep-iteration lane's own supply question already rides, or sooner at the operator's own
initiative (e.g. if the Avenue-A credit's real balance is confirmed, or the lane's own
slot-3 decision makes this construct's value case sharper). $0.00 spent, both samples
combined. Redraw only, not a new construct. Inherits `H`, S1,
S3, S3', S4, S5, S6, S7, S8, and §§5–8 of [`PREREG.md`](PREREG.md) **verbatim, unedited** — that
document stays frozen byte-for-byte (Trap #12); this is a sibling artifact, not an amendment.
The **only** thing this document freezes fresh is a **replacement S2** (the 30-of-255 event
sample) and its own §9 sign-off/P0 cycle, because the original S2 sample is cost-contaminated
(its exact per-day MBP-10 price is now known — see [`PREREG.md`§9.2](PREREG.md)) and cannot be
reused per FM-5's own logic, extended symmetrically (excluding known-expensive days would be
exactly the cherry-pick FM-5 bars; so is silently keeping the known-cheap ones).
**Date:** 2026-08-23 · **Authorization to redraw:** operator, *"Redraw the sample"* (this
session, following the P0 abort).
**Cost of everything so far (this document):** **$0.00** (the new sample's dates are derived
from already-frozen structure — no cost byte was read to choose them; see §2).
**K_intrinsic = 0** — unchanged from `PREREG.md` §6; no outcome-bearing byte exists yet.

---

## §0 — Rule-0 reads (this session)

| Source | What it pins |
|---|---|
| [`PREREG.md`](PREREG.md) §§1–8, read in full (again, not from memory) | `H-MNQFLOW-1-DEPTH`, the frozen S1/S3/S3'/S4/S5/S6/S7/S8 statistics, §5 forbidden moves FM-1–FM-8, §6 K-accounting, §7 verdict gates — **all unchanged, all inherited**. Nothing in this document may contradict them. |
| [`PREREG.md`](PREREG.md) §9.2 | The abort record: 30-day actual cost **$148.0357** vs the **$125.00** ceiling (18.4% over); no pull ran; $0 spent; three named forward paths, "a fresh S2 sample under its own new pre-registration" among them — **this document is that path, elected by the operator**. |
| [`2026-08-23-deep-lane-supply-audit.md`](../../../../docs/notes/audits/programme-audit/2026-08-23-deep-lane-supply-audit.md) §5 item 1 (updated) | This route is the estate's nearest reachable supply lead; the audit's own record already carries the correction that the first sample blocked at P0 — this redraw is the disclosed next step, not a fresh estate-wide search. |
| The 255-trigger reconstruction (this session, `build_events.py` recovered read-only from pre-prune commit `283d1de^`, re-run against still-present `orb_lib.py` + the already-cached 1m panel) | Elementwise-verified against `orb_lib.orb_backtest`'s own output (n=255, `range` array match) before either sample (original or this one) was drawn from it — the same verified list both documents draw from, not two independent reconstructions that could silently diverge. |

**Dedup attestation.** No other redraw of this construct exists — `PREREG.md`'s own Amendment
log (2026-08-23 entry) is the only prior event, and it names this exact path as the one elected.

---

## §1 — Why a redraw, not a re-cut of `PREREG.md` or a new construct

`PREREG.md`'s own S2 declared a full-range systematic sample specifically so the event set would
never be "a convenience or outcome-informed subset." That property survives a cost-abort — the
original 30 dates are still a fair, unbiased draw of *which sessions to look at*; what they are
**not** anymore is a fair basis for *this budget cycle's pull*, because their prices are now
known and reusing them (in whole or in part) would make any subsequent inclusion/exclusion
decision cost-informed by construction. **A redraw is the only clean move that doesn't touch
FM-5's own boundary in either direction** — keeping cheap days and dropping expensive ones would
obviously cherry-pick for cost; but doing nothing and reporting the abort as terminal would also
be wrong, since the operator's own three named paths (`PREREG.md` §9.2) include exactly this
one, and the H, statistics, and gates are all untouched — only the *set of days measured*
changes, which is squarely an S2-only concern under the original document's own axis structure.

**Not a fresh construct under FM-4.** FM-4 (inherited, `PREREG.md` §5) gates a *second cell* —
a different schema, window, threshold, or instrument. This redraw changes none of those; it is
the *same* cell's data-collection step, re-attempted after a structural (budget) failure before
any book byte was ever read. No fresh Avenue-A qualifying-triple argument is owed (§3 of
`PREREG.md` already cleared it for this exact construct); re-arguing it here would be ceremony,
not discipline.

---

## §2 — The redrawn S2 (frozen now, before any cost byte for these specific dates is read)

**Derivation rule (mechanical, chosen before any of these 30 dates' costs were known):**
exclude the original 30 trigger indices (now cost-known) from the 255-trigger chronological
list, leaving a 225-element remaining pool in original chronological order; apply the
**identical** full-range systematic-sampling shape `PREREG.md` S2 used — `round(i × (N−1)/29)`
for `i = 0..29`, `N` = pool size — to this remaining pool's own 0-indexed positions, then map
each position back to its actual trigger row. This is the same rule S2 used, applied to what is
left, not a new formula invented for this document. Verified: 30 unique positions, spans the
full remaining-pool range (position 0 to 224 inclusive), **zero overlap** with the original 30
trigger indices (checked programmatically, not by inspection).

**Disclosed limitation, not hidden.** Excluding the original 30 specific calendar dates from
*any* future draw is itself a form of selection — those 30 dates, whatever their own volatility
or book-activity characteristics happen to be, can never appear in this or a later redraw of
this construct. This selection is **not** informed by their cost being high or low (five of the
30 cost $6.25–$9.12; two cost $0.00; the rest fell in between — a wide spread, not a pattern this
document has attempted to characterize or exploit), only by the mechanical fact that they were
already checked. A reader who wants to rule out a volatility-correlated bias from this exclusion
can compare this redraw's own eventual coverage/statistic against `PREREG.md`'s own disclosed
per-day cost table (§9.2) — nothing here obscures that comparison.

| Trigger idx | Date | Side | | Trigger idx | Date | Side | | Trigger idx | Date | Side |
|---:|---|---|---|---:|---|---|---|---:|---|---|
| 1 | 2025-08-07 | long | | 97 | 2025-12-19 | long | | 192 | 2026-05-06 | long |
| 10 | 2025-08-20 | short | | 106 | 2026-01-05 | long | | 202 | 2026-05-20 | short |
| 17 | 2025-08-29 | short | | 113 | 2026-01-14 | short | | 209 | 2026-05-29 | long |
| 27 | 2025-09-12 | long | | 122 | 2026-01-27 | long | | 218 | 2026-06-12 | long |
| 36 | 2025-09-25 | long | | 132 | 2026-02-10 | long | | 227 | 2026-06-26 | long |
| 45 | 2025-10-08 | long | | 141 | 2026-02-23 | short | | 237 | 2026-07-10 | short |
| 52 | 2025-10-17 | long | | 148 | 2026-03-04 | long | | 244 | 2026-07-21 | short |
| 62 | 2025-10-31 | short | | 157 | 2026-03-17 | short | | 253 | 2026-08-03 | long |
| 71 | 2025-11-13 | short | | 167 | 2026-03-31 | long | | | | |
| 80 | 2025-11-26 | short | | 174 | 2026-04-10 | short | | | | |
| 87 | 2025-12-05 | long | | 183 | 2026-04-23 | long | | | | |

**S3' (L1 comparator), S4 (controls), S5–S8 (statistics, placebo, coverage, agreement):** all
recomputed on **this** 30-event subsample, per `PREREG.md`'s own frozen rules — unchanged,
re-applied to the new set.

### §2.2 — Cost/budget guard (identical rule and ceiling; the credit is still fully untouched —
$0 has ever been spent against it, including by the original sample's abort)

**Phase P0 (blocking, at run time, before any pull):** re-estimate `metadata.get_cost` for these
*actual* 30 dates. **Abort if the re-estimated total exceeds $125.00.** No flat single-day
extrapolation is quoted here as a sanity anchor — `PREREG.md`'s own §4 already showed that a
flat multiply is not a safe proxy for the real total; P0's own re-estimate is the only number
that matters, exactly as before.

---

## §5' — One additional forbidden move for this redraw (does not amend `PREREG.md`'s own §5,
which stands verbatim; this is scoped to this document only)

- **FM-9 — A third silent redraw.** If this sample's P0 re-estimate *also* exceeds $125.00, that
  is not grounds for drawing a third sample automatically. Two structural failures in a row on
  the same construct is itself information (about the schema's true cost at this instrument's
  activity level, not about either specific sample) — it returns to the operator as a named
  finding ("30-day MBP-10 samples of this construct do not fit inside $125 at this
  instrument's activity level"; the same discipline `inqhiori`'s own tail-exhaustion guardrail
  applies to hypothesis attempts, borrowed here for resampling attempts), not another automatic
  resample.

---

## §9 — Protocol order (identical to `PREREG.md`'s own; violations void the run)

1. This file committed = freeze. Done before any cost byte for these 30 specific dates exists.
2. **Operator sign-off on the redrawn sample** — recorded in §9.1 below. Not inherited from
   `PREREG.md`'s own §9.1, which authorized a different, now-abandoned 30-day set; a new sample
   is a new thing to sign, same discipline that document held itself to.
3. **P0 — blocking cost re-estimate** on these actual 30 dates (§2.2). Abort if it exceeds
   $125.00 (FM-9 governs what happens next if it does).
4. Harness + hand-computed unit tests (unchanged from `PREREG.md`'s own S3–S8 implementation);
   all pass before the runner reads a real quote.
5. Single run. RESULTS discharges exactly one `PREREG.md` §7 branch, on this sample.

### §9.1 — Operator signature block (SIGNED 2026-08-23)

```
SIGNED / FROZEN: 2026-08-23 / JA   (date / initials — authorized via chat to Claude Code,
this session: "Redraw the sample," electing PREREG.md §9.2's named path 2, following that
document's own P0 abort)
Authorized: MNQFLOW-1-DEPTH S2B — the redrawn 30-of-225-remaining-pool trigger sample in §2
above, schema mbp-10, ceiling <= $125.00 subject to §2.2's P0 re-estimate gate. All of
PREREG.md's H, S1/S3/S3'/S4/S5/S6/S7/S8, §5 (FM-1-FM-8) + this document's own FM-9, and §6
K-accounting stand as frozen and unedited.
No pull runs before this block is filled.
```

---

### §9.2 — P0 outcome

**P0 FIRED. ABORT. Second consecutive P0 failure on this construct. No pull executed. $0.00
actual spend.**

| Date | Cost | | Date | Cost | | Date | Cost |
|---|---:|---|---|---:|---|---|---:|
| 2025-08-07 | $4.5425 | | 2025-11-26 | $5.1487 | | 2026-03-04 | $7.1781 |
| 2025-08-20 | $4.5751 | | 2025-12-05 | $4.5354 | | 2026-03-17 | $1.9716 |
| 2025-08-29 | $3.5547 | | 2025-12-19 | $4.3775 | | 2026-03-31 | $8.4335 |
| 2025-09-12 | $2.3887 | | 2026-01-05 | $4.7265 | | 2026-04-10 | $4.1267 |
| 2025-09-25 | $5.0262 | | 2026-01-14 | $6.5474 | | 2026-04-23 | $6.3016 |
| 2025-10-08 | $2.7868 | | 2026-01-27 | $3.4403 | | 2026-05-06 | $5.3819 |
| 2025-10-17 | $6.9653 | | 2026-02-10 | $6.4818 | | 2026-05-20 | $7.0890 |
| 2025-10-31 | $5.6867 | | 2026-02-23 | $6.8472 | | 2026-05-29 | $5.8129 |
| 2025-11-13 | $9.0256 | | | | | 2026-06-12 | $5.7063 |

(remaining 6: 2026-06-26 $9.7743, 2026-07-10 $6.2997, 2026-07-21 $0.0000, 2026-08-03 $0.0000 —
again two genuine-data $0 days, same Databento-side pattern as the first sample, not a
coincidence worth over-reading on n=2 but consistent with whatever recent-window pricing rule
is in effect.)

**Total: $154.7320. Ceiling: $125.00. Over by $29.7320 (23.8% over) — worse than the original
sample's $148.0357 (18.4% over).**

**This is the structural finding, not a second unlucky draw.** Two independent, disjoint,
mechanically-unbiased 30-day systematic samples of the same 255-trigger population both landed
19–24% over a $125.00 ceiling that was set from a flat single-day extrapolation
(`PREREG.md` §4: $3.33–$3.97/day × 30 ≈ $100–$120). The two samples' means ($4.93/day and
$5.16/day respectively) both run noticeably above that single-day anchor — the anchor day
itself was not representative of the panel's own cost distribution, not an unlucky pair of
samples. **The honest read: a genuine 30-day MBP-10 sample of this construct costs roughly
$150, not $125, at MNQ's current activity level.** FM-9 governs what happens next: no third
redraw. Reported to the operator.

**Updated forward paths (supersedes `PREREG.md` §9.2's framing — path 2 is now spent, not
open):**
1. **Raise the ceiling** — now informed by two real draws (mean ≈ $151, range $148–$155): a
   ceiling of roughly **$160–$175** would very likely clear a third draw, if authorized on
   updated cost knowledge rather than the original single-day extrapolation. Still needs
   confirmation the Avenue-A credit itself extends that far.
2. ~~A fresh S2 sample~~ — **spent.** Two independent draws is this document's own
   pre-committed limit (FM-9); a third is an operator-authorized exception, not automatic.
3. **A smaller N** — e.g. 20 of 255 instead of 30, scaled down proportionally
   (≈$100–103 at the measured $5.03/day pooled mean across both samples), trading some of S8's
   own power (already disclosed at n=30 as likely `AMBIGUOUS-UNDERPOWERED`, `PREREG.md` §8) for
   budget fit. A genuinely new pre-registration, not a resample of either burned set.
4. **Decline** — mark the route dead on cost at this instrument's current activity level, not on
   any scientific finding. Zero effect on `MNQFLOW-1`'s own `RESOLVED` L1 verdict (FM-4b).

**Operator disposition, 2026-08-23 (elects none of the four above): `HOLD` — see the Status
block.** Not a fifth named path so much as a decision *not* to choose among the four yet,
recorded as its own state rather than forced into the nearest one.

$0.00 actual spend throughout, both samples combined. K_intrinsic unaffected (still 0).

## §10 — Audit hooks

```bash
# Freeze ordering
git log --oneline -- lab/analysis/c1/mnq_orb_flow_depth_2026-08-18/PREREG_S2B.md | tail -1

# The parent document this redraw inherits from, and its own abort record
grep -n "9.2 — P0 outcome" lab/analysis/c1/mnq_orb_flow_depth_2026-08-18/PREREG.md

# Zero overlap between the two samples (re-verify, don't trust the prose table)
python -c "
orig = sorted(round(i*254/29) for i in range(30))
pool = [i for i in range(255) if i not in orig]
new = sorted(pool[round(i*224/29)] for i in range(30))
print('overlap:', set(orig) & set(new))
"

# Signature gate — confirm no pull is authorized until §9.1 is actually filled
grep -n "SIGNED / FROZEN: ____" lab/analysis/c1/mnq_orb_flow_depth_2026-08-18/PREREG_S2B.md \
  && echo "STILL DRAFT — no pull" || echo "signed"
```

---

## Amendment log (append-only — the frozen sections above are never edited, Trap #12)

- **2026-08-23 — FROZEN.** Authored same session as `PREREG.md`'s own P0 abort, on operator
  direction ("Redraw the sample"). No cost byte for any of these 30 dates was read before this
  freeze — the derivation rule (§2) is purely mechanical over already-frozen structure.
- **2026-08-23 — Sign-off (§9.1) and P0 (§9.2) executed same session.** P0 fired: $154.7320
  actual vs $125.00 ceiling (23.8% over) — worse than `PREREG.md`'s own first-sample result
  ($148.0357, 18.4% over). Two independent draws now point at the same structural conclusion
  (true cost ≈$150, not the $125 credit). FM-9 held: no third redraw. Reported to the operator
  with four named forward paths, none elected.
- **2026-08-23 — Operator disposition: `HOLD`.** *"I am not ruling it out but I do not know if
  it is worth the spend."* None of the four named paths elected; recorded as its own state, not
  rounded to "decline." No forced re-test date. Status block updated in place (this is the
  document's own live status field, not frozen §§1–9 body text).
