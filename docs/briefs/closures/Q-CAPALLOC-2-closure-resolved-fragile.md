# Q-CAPALLOC-2 — Closure: `RESOLVED-FRAGILE`, operator disposition **DECLINED** (`69/11` stands)

**Verdict:** `RESOLVED-FRAGILE` — `51/29` clears D1–D5 on both halves at the verified cell
(`WIN_MIN=200, PAYOUT_MIN=0`) but fails 2 of 6 drift cells; the intersection across all six is
empty. Per the frozen §6 gate, no plain GO exists under this verdict.
**Operator disposition (2026-07-30, chat directive "Let's go with what the data says"):**
**DECLINE.** `69/11` stands as ratified. No `LEG_MAP` change, no amending ADR, no tripwire
adoption. Re-open preconditions in §4.
**Closed:** 2026-07-30
**Pre-registration:** [`Q-CAPALLOC-2-verdict-preregistration.md`](../pre-registration/Q-CAPALLOC-2-verdict-preregistration.md)
— `FROZEN`, §9 operator-signed 2026-07-30 / JA at `509193b`, strictly before any drift cell ran
(freeze-before-result git-auditable; the pre-reg stays byte-unedited after this closure per
Trap #12, as does the parent Q-CAPALLOC-1 at `AMBIGUOUS (d)`).
**Spend:** $0.00 (existing panel; no pull, no K — robustness axis on an inherited candidate set,
no fresh selection).
**Live effect:** **none.** Rail disarmed throughout; no `core/`, allocation, `dd_protection`,
Pine, rung, or rail byte modified. B7 sequencing untouched.
**Artifacts:** [`RESULTS.md` §Addendum 2026-07-30](../../../lab/archive/c1_capalloc_2026-07-27/RESULTS.md)
· [`capalloc2/RESULTS.md`](../../../lab/archive/c1_capalloc_2026-07-27/capalloc2/RESULTS.md)
· raw per-cell JSON + logs under
[`capalloc2/`](../../../lab/archive/c1_capalloc_2026-07-27/capalloc2/).

---

## 1. The measurement

Legacy drift sentinel **PASSED** (reproduces the 2026-07-29 control to $0.20 on `E[cash]`), so
every cross-cell difference is a rule-pin change, not harness noise. Six cells, `WIN_MIN`
∈ {150, 200, 250} × `PAYOUT_MIN` ∈ {0, 250}, frozen before any cell ran:

| cell | `51/29` both halves, strict floor |
|---|---|
| `w150_p0` | **FAIL** — H1 D4 headroom +0.07 pp clears the raw threshold but not the seed-noise floor |
| `w200_p0` (verified) | **PASS** — matches the 2026-07-29 re-run reference exactly |
| `w250_p0` | PASS |
| `w150_p250` | **FAIL** — H1 D4 literal breach (dead@1y 25.75% vs incumbent 23.15%; headroom −0.60 pp) |
| `w200_p250` | PASS |
| `w250_p250` | PASS |

The binding corner (`WIN_MIN=150`) is the cell the pre-reg's §7 pre-declared expectation named
as the genuinely uncertain, informative one before any cell ran. Prediction met: §7's overall
prior was "`RESOLVED-FRAGILE` at least as likely as `RESOLVED-ROBUST`."

Verification before acceptance: `capalloc2/score_grid.py` independently re-run against the raw
per-cell JSON reproduces the verdict exactly; `score()` in `run_capalloc.py` read directly to
confirm the D3/D4 noise floor is the parent's coded criterion, not a post-hoc gloss; the
`grid_fast.log` FAIL lines are a PowerShell exit-code-capture quirk documented in the RESULTS
addendum, not a computation failure.

## 2. Verdict routing (§6, mechanical)

- `RESOLVED-ROBUST` needs all 6 cells — **fails** (intersection empty).
- `FALSIFIED` needs a failure at the verified cell — **fails** (`w200_p0` clears both floors).
- **`RESOLVED-FRAGILE` — FIRES** (clears verified cell; fails ≥1 drift cell).
- `AMBIGUOUS (a/b)` — did not fire (sentinel passed; the decisive verified-cell and breach
  margins are well clear of noise; `w150_p0`'s sub-noise D4 headroom makes that *cell* a
  failure under the strict floor, which is the reading §6 requires — it does not make the
  *verdict* ambiguous, since the fragile trigger is already satisfied by `w150_p250`'s literal
  breach).

Clean single verdict.

## 3. Operator disposition — DECLINE, on the data

§6's FRAGILE row offers exactly two routes: conditional adoption with a named tripwire, or
decline. The operator elected **decline**, on the data summary presented this session. Grounds
recorded as pointers (the RESULTS addendum carries the numbers):

1. **The drift failure axis is D4/dead@1y in H1** — survival in the chop half, the axis the
   estate's precedence ranks above EV (fork-B precedent: EV-optimal 1.00× declined for the
   regime-robust 0.50×, [`2026-07-23-c1-rung-selection-ev-objective.md`](../../adr/2026-07-23-c1-rung-selection-ev-objective.md)).
2. **Drift is live and winner-churn has a measured base rate:** Tradeify moved rules ≥3 times in
   2026 on a ~90-day cadence; `$150` is its own published adjacent-tier value; and `48/32` — the
   dominating split of 2026-07-27 — was dead within 48 hours of a pin correction. `51/29` is the
   second winner in four days; the pre-reg's §7 honesty limit warned the plateau structure may
   be a panel artifact.
3. **Sequencing made adoption valueless now:** any `LEG_MAP` change is post-B7-REFIRE-Stage-2
   regardless, and the declared forward check — realized per-leg fills — arrives from that same
   process.
4. **Every D4 figure in the comparison is a lower bound from the EOD-only engine.** The venue
   enforces the trailing floor intraday (venue read 2026-07-30, fade-spec §3.2a), the intraday
   correction plausibly bites the MNQ-heavier candidate harder (measure, don't assert), and the
   engine capability to score it honestly landed the same day (PR #566). This is the next known
   venue-fact correction — the same class as the eval-lock fix that killed `48/32`.

## 4. Preconditions bound to any re-open

Re-opening `51/29` (or any successor `LEG_MAP` candidate) without all three of the following is
the churn this line's own record warns about, not new evidence:

- **(a)** D4/dead@1y re-scored under **intraday barrier enforcement** (`core/mc` opt-in, PR
  #566) for candidate and incumbent alike — a venue-fact correction, not a re-roll;
- **(b)** reconciliation against **realized per-leg fills** post-B7 (the pre-reg's declared
  forward check — not another panel re-run);
- **(c)** rule pins re-verified within the standing 90-day window at decision time.

## 5. What this closure does not establish

It does not establish that `69/11` is optimal — the incumbent remains an unpriced
compliance-driven de-risk and the slowest cell in the chop half (parent RESULTS §Addendum
2026-07-29b). It does not convert Q-CAPALLOC-1's `AMBIGUOUS (d)`. And it does not measure
`51/29` under intraday-honest geometry — that is precondition (a), deliberately left to a future
decision point rather than run now, so a re-measurement happens against a live question rather
than accumulating as an unread number.
