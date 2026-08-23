# Q-TOM-SPX-1 — CLOSURE: `DEAD`

**Verdict:** `DEAD` — Layer-A `RESOLVED-ABSENT` on the canonical Pepperstone US500 daily feed (2026-06-16) plus operator GO 2026-08-23 that the reserved native-Pine confirmation is **not reserved**.
**Closed:** 2026-08-23
**Lane:** `UNASSIGNED`
**Pre-registration:** the inquire brief itself ([`Q-TOM-SPX-1.md`](../Q-TOM-SPX-1.md) §8) — no separate `docs/briefs/pre-registration/` file
**Spend / K:** $0.00 · K consumed: 0 (this close). Layer-A 2026-06-16 was a prior session on operator-supplied TV CSVs.
**Live effect:** Q leaves INDEX Open; pursuit c3 flips PARK → SUBTRACT; `turn-of-month-premium × SPX500` lands on the reject registry. No book, no rail, no `BASE_RISK` change.
**Artifacts:** [`brief`](../Q-TOM-SPX-1.md) · [`census`](../../notes/audits/2026-08-23-p10-open-roster-census.md) · [`c3`](../../pursuits/c3-q-tom-spx-1.md) · [`SPX500 ledger`](../../../ops/instruments/SPX500.md) · [`harness`](../../../lab/analysis/legacy/tom_spx/README.md)

---

## 1. Verdict (§6 asserted against actual numbers)

The brief reserved the **formal** §6 close to the Pine harness on long-history TV. Layer-A on the named canonical feed already fired hard-absent. Operator GO (P10) closes DEAD without paying the reserved Pine limb.

| §6 route | Trigger | Actual | Fired? |
|---|---|---|---|
| `RESOLVED — PRESENT & TRADEABLE` | existence + persistence (t≥2.0) + capturable ≥4× measured cost on canonical TV/Pepperstone | existence battery hard-absent (t=0.64) | — |
| `RESOLVED — ABSENT / DECAYED` | any hard-absent trigger (diff≤0 / perm p≥0.10 / t<1.0 / drop-top-k flips sign) | Layer-A 2026-06-16, Pepperstone US500 daily 2017–2026, n=113: window−off **+0.0434%**/day but Welch **t=0.64**, perm **p=0.2544**, drop-top-2 (2020-03+04) → +0.0001%, halves **+0.148% / −0.060%** (sign-reverse). Alchemy cross-check (16 turns) agrees (diff −0.151%, t −1.12). | ✓ Layer-A |
| `RESOLVED — REJECT EXECUTION DESIGN` | Layer-A existence>0 but post-cost capturable ≤0 | existence did not clear | — |
| `AMBIGUOUS — HOLD` | 1.0≤t<2.0, or net>0 but <4×, or PRESENT on Dukascopy only | t=0.64 is the hard-absent band, not the underpowered band; feed was canonical Pepperstone, not Dukascopy | — |
| Formal DEAD without Pine | operator elects not to reserve the unpaid native-Pine confirmation | unpaid since 2026-06; P10 GO 2026-08-23 | ✓ this close |

Capturability stays PENDING (W3 — no measured SPX500 cost). Decay stays UNTESTED (feed starts 2017 > 2001 split) and does not contribute a pass. Neither changes the ABSENT existence verdict.

## 2. What the pre-registration predicted vs what happened

§6 predicted a Pine-gated formal close. Layer-A on the canonical feed was already near-dispositive negative (F5). The reserved Pine step was a feed-fidelity confirmation, not a second significance battery (Pine table does not compute perm/t/drop-top-k/halves). It sat unpaid for ~10 weeks. Operator elected DEAD rather than keep a reserved-open row.

## 3. What this closure does NOT license

- Quoting a Pine-harness §6 fire. Pine was not run as the gate.
- Re-running Dukascopy, widening `[T+1:T+3]`, or changing frozen thresholds to rescue the null (brief §5).
- Killing SPX500 the instrument, or any non-TOM family on that ledger.
- Treating Layer-B capturability as measured (W3 unpaid).

## 4. Defects found in the frozen brief (recorded, not repaired)

INDEX Open carried `RESOLVED-ABSENT` + “formal DEAD reserved” as if that were an open investigation. The brief’s own §6 already named the ABSENT → `rejected_candidates.md` append. Not repaired by editing frozen §4–§8.

## 5. Lesson candidates

Below the two-incident bar — watch. Sibling pattern: reserved-close rows on INDEX Open look live. P10 census is the one-page check, not a new Q.

## Iterate — loop exit

- **Verdict used:** `DEAD`
- **Model update:** a reserved confirmation that is never paid is not an open question; Layer-A ABSENT on the named canonical feed is enough to stop the thread when the operator declines the leftover limb.
- **Next:** STOP
- **Routing:** STOP — INDEX Open row deleted; c3 SUBTRACT; registry row appended. No successor Q.
- **Entry packet:** n/a
- **Stop rule / re-proposal bar:** new *mechanism* evidence, not a wider window, new thresholds, or a Dukascopy re-run of `turn-of-month-premium × SPX500`. Re-proposing the same key returns DUPLICATE.
- **Board write:** none — STOP, nothing owed (c3 dropped from the 2026-11-08 GSUB-1 PARK-expiry row; queue #1/#2 unchanged)
- **Registry:** rejected_candidates.md — ### turn-of-month-premium × SPX500

## §10 audit-hook discharge

Parent brief §10 commands, this session:

- `python -m pytest lab/analysis/legacy/tom_spx/test_verdict.py` — **file absent**. Great Prune left `README.md`, `PINE_MANIFEST.sha256`, and the gitignored Pine; `q_tom_spx_1.py` / `test_verdict.py` are not on this public tree. Frozen-threshold greps therefore have no target. Layer-A numbers used above are the ledger record ([`SPX500.md`](../../../ops/instruments/SPX500.md) F5 / 2026-06-16 session log), not a re-run.
- Collision-guard: `NOCT-SPX-001` still on `ops/instruments/SPX500.md` D1; `inventory-reversal-immediacy-premium` still on `docs/rejected_candidates.md`.
- `git log -1 --format='%h %cs' -- docs/adr/2026-06-12-rnd-feed-instrument-class-split.md` still resolves.
- Parent Verification block's `check_brief.py` path is a Windows user-skill path, not the repo checker — recorded, not silently passed (M-AHF).

```
$ ls lab/analysis/legacy/tom_spx/
PINE_MANIFEST.sha256  README.md  tom_test_spx500.pine
$ python -m pytest lab/analysis/legacy/tom_spx/test_verdict.py -q
ERROR: file or directory not found: lab/analysis/legacy/tom_spx/test_verdict.py
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-23 | Closure authored; formal DEAD; Pine confirmation not reserved | Cursor (operator-directed P10) |
