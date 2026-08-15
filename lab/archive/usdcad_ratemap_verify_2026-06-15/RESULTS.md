# Verification report — claude.ai USDCAD rate-diff regime map + BoC decision-day array

**Date:** 2026-06-15
**Executor:** Claude Code (repo-side verification of an external web-authored research doc)
**Handoff:** CC-HANDOFF "Verify + integrate the claude.ai USDCAD rate-diff regime map + BoC array" (2026-06-15)
**Inbound artifact:** `~/Downloads/compass_artifact_wf-8ca0b3bb-0a06-418e-9b29-8ddb9764031c_text_markdown.md` (claude.ai, web search, no repo access)
**Status:** `DONE_WITH_CONCERNS` (verification clean; one integration hazard surfaced — see §2.5)

---

## §0 — Rule-0 reads (this session)

| File | Anchor | Read for |
|---|---|---|
| `ops/instruments/USDCAD.md` | `56eead6` 2026-06-14 | durable findings #4 (2024 regime split), #5 (feed policy), #6 (BoC array note); session log |
| `docs/adr/2026-06-12-tv-csv-canonical-feed-policy.md` | Accepted 2026-06-12 | §2 makes **official central-bank/treasury series canonical** (bar feeds staging-only) |
| `docs/ltm/briefs/pre-registration/FWD-PREREG-BPC-USDCAD-TUE-2026-06-11.md` | registered 2026-06-11 | BPC frozen config — **BoC blocks OFF, Tue-only**; first forward trade 2026-06-16 |
| `docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md` | ratified 2026-06-11 | operational rule 10 (append dated disposition) |
| `bpc_usdcad_v0_1.pine` | **ABSENT** (gitignored `**/*.pine`; not in this worktree; not in MANIFEST.sha256) | array lives here but not directly readable/editable in this checkout |

---

## §2.1 — Anti-confabulation structural scan → PASS

- **Repo-state claims:** none. The doc's scope note explicitly disclaims them; the one place it references in-repo context (the 2024 "worst year for one concept / best for another" flag) explicitly states *"This report makes no claim about those strategy results — it only date-pins the macro divergence the requester flagged."* No file/path/value/edit assertion anywhere.
- **Strategy-performance claims:** none. No PF / WR / DD / expectancy / R-multiple / "would have". The "CAD vs USD bias" column is documented spot-FX direction only, caveated as such.

Both forbidden classes are clean. Nothing quarantined.

## §2.2 — Task A (regime map) source verification → PASS

Load-bearing macro facts verified against primary sources (BoC FAD releases / federalreserve.gov / BoC key-rate page):

| Fact | Doc claim | Verified | Source |
|---|---|---|---|
| BoC first cut of 2024 cycle | Jun 5 2024, −25bp → 4.75% (first since Mar 2020) | ✅ | BoC release 2024-06-05; CBC/TD |
| Fed first cut of 2024 cycle | Sep 18 2024, −50bp → 4.75–5.00% (first in 4+ yrs) | ✅ | FOMC 2024-09-18 (11-1, Bowman dissent) |
| **2024 divergence window** | **Jun 5 → Sep 17 2024** (BoC eases, Fed static; widest −125bp) | ✅ | derived from the two pinned dates above |
| 2024 BoC cut path | Jul 24 → 4.50, Sep 4 → 4.25, Oct 23 → 3.75, Dec 11 → 3.25 | ✅ | BoC releases 2024-10-23, 2024-12-11 |
| 2025 BoC path | 3.00(Jan29)/2.75(Mar12)/holds/2.50(Sep17)/2.25(Oct29)/hold(Dec10) | ✅ exact | BoC key-rate page |
| 2026 BoC path | holds at 2.25% (Jan28/Mar18/Apr29/Jun10) | ✅ exact | BoC key-rate page |

Spread convention (BoC overnight − Fed upper bound) and the spread path (~−75bp end-2018 → ~0 2019–21 → −25 end-2022 → −50 end-2023 → −125 end-2024 → −150 end-2025→mid-2026) are internally consistent with the verified rate levels.

**Not load-bearing / honestly self-caveated by the doc (no integration dependence):** exact 2-yr yield-spread magnitudes for pre-2023 years (direction-confirmed, bp approximate); WTI annual averages (qualitative; only the Apr 20 2020 −$37.63 settle is hard-sourced). These are flagged in the doc's own "could not verify" section and are **not** used in any proposed ledger edit.

## §2.3 — Task B (BoC decision-day array) reconciliation → PASS; 2022 gap CLOSED

**The 2022 gap is closed.** Eight 2022 fixed announcement dates, all 10:00 ET, confirmed against BoC FAD press releases (Mar 2, Apr 13, Jul 13, Sep 7, Dec 7 directly; Jan 26 / Jun 1 / Oct 26 confirmed as scheduled dates and rate-path-consistent):

| Year | Verification |
|---|---|
| 2022 | **VERIFIED** — Jan 26 (hold 0.25), Mar 2 (+25→0.50), Apr 13 (+50→1.00), Jun 1 (+50→1.50), Jul 13 (+100→2.50), Sep 7 (+75→3.25), Oct 26 (+50→3.75), Dec 7 (+50→4.25); all 10:00 ET |
| 2023 | **CORROBORATED** — terminal 5.00% via Jul 12 2023 confirmed; Dec 6 2023 = last announcement at 10:00 ET (convention-change context); mid-year dates standard-schedule, not each individually fetched |
| 2024 | **VERIFIED** — Jan 24 (hold, first at 09:45), Mar 6, Apr 10, Jun 5 (−25), Jul 24 (−25), Sep 4 (−25), Oct 23 (−50), Dec 11 (−50) |
| 2025 | **VERIFIED (exact)** — all 8 dates + rates match BoC key-rate page |
| 2026 | **VERIFIED (exact)** — Jan 28/Mar 18/Apr 29/Jun 10 holds @2.25; scheduled Jul 15/Sep 2/Oct 28/Dec 9 |

**Convention-change date PINNED:** announcements were **10:00 ET through 2023 (last: Dec 6 2023)** and moved to **09:45 ET beginning Jan 24 2024** (first decision under the new time; MPR concurrent; press conference ~10:30 ET). Change announced Dec 2023, motivated by removing a conflict with North-American FX-option-expiry timing. Confirmed via BoC release `fad-announcement-release-mpr-january-24-2024` + BoC 2023-12 communications-change notice.

**Unscheduled/emergency decisions 2022–2026:** none (the only recent emergency cuts — Mar 13 & Mar 27 2020 — predate the window). Consistent with the doc.

## §2.4 — Feed-policy compliance → PASS

The doc proposes/assumes **no price-data bar feed** and names no Dukascopy / Alchemy / broker-REST source. Its data sources (BoC, Fed/FOMC, FRED, EIA, Treasury) are official non-bar series — explicitly canonical/unaffected under `docs/adr/2026-06-12-tv-csv-canonical-feed-policy.md` §2.1.
- **Minor note (not a violation):** the doc cites Trading Economics for two 2-yr yield *levels*. Secondary source, self-flagged as approximate. If those yield levels ever become load-bearing, pull from BoC Valet / FRED `DGS2` (official series) per policy — not the secondary outlet.

---

## §2.5 — Proposed integration (OPERATOR-GATED — NOT applied)

### Proposal A — `ops/instruments/USDCAD.md` durable finding #6 (BoC array note)

Current:
> **BoC decision-day array 2022–2026** verified 2023–2026 vs bankofcanada.ca; 2022 pending verification; announcements 10:00 ET through 2023, 09:45 ET from 2024 (presser ~10:30). Lives in bpc_usdcad_v0_1.pine; extend yearly.

Proposed:
> **BoC decision-day array 2022–2026** verified **2022–2026** vs bankofcanada.ca (**2022 gap closed 2026-06-15**: 8 dates, all 10:00 ET, confirmed vs BoC FAD press releases). Announcement time **10:00 ET through 2023 (last: Dec 6 2023) → 09:45 ET from Jan 24 2024** (presser ~10:30; change announced Dec 2023 re: FX-option-expiry timing). Lives in bpc_usdcad_v0_1.pine (**blocks OFF for the Tue-only forward test**); extend yearly. Full verified array → `lab/analysis/usdcad_ratemap_verify_2026-06-15/RESULTS.md`.

### Proposal B — `ops/instruments/USDCAD.md` durable finding #4 (2024 regime split)

Pin the exact window into the existing sentence:
> **2024 regime split:** BoC-cutting/Fed-holding divergence (**window pinned 2026-06-15: Jun 5 2024 BoC first cut → Sep 17 2024, the day before the Fed's Sep 18 −50bp cut; widest spread −125bp**) was SVRN's worst year and BPC's best (+1.125R, n=8). … *(rest unchanged)*

### Proposal C — `ops/instruments/USDCAD.md` session-log entry (operational rule 10)
A dated 2026-06-15 disposition row recording this verification + the two updates above.

### ⚠️ Proposal D — `bpc_usdcad_v0_1.pine` BoC-array extension → **RECOMMEND DEFER, do NOT write now**

The handoff anticipated patching the verified array into the Pine file. Phase-0 reads make that the wrong move **right now**:
1. **Functionally inert for the live test.** BPC-001 is **Tuesday-only with BoC blocks OFF** (BoC announcements are Wednesdays — "both Wed phenomena" per the pre-reg). Extending the array changes nothing the forward test sees.
2. **Frozen-window hazard.** The forward pre-reg's FM#1 forbids "any parameter, session, day, or **block** change to the frozen config" once forward data exists (first trade **2026-06-16**). Editing the array — even an OFF feature — muddies the "zero touches" audit posture for no benefit.
3. **Not editable here anyway.** The `.pine` is gitignored and absent from this worktree.

**Recommendation:** record the verified array in this RESULTS.md (done — §2.3) as the durable reference, and defer writing it into `bpc_usdcad_v0_1.pine` until BoC blocks actually matter (a non-Tuesday variant or a different strategy). If/when applied, do it where the file lives, outside the BPC frozen window, with a manifest/hash note (the file is not currently manifest-pinned).

---

## Closure

- **Per-step gates:** 2.1 PASS · 2.2 PASS · 2.3 PASS (2022 closed) · 2.4 PASS · 2.5 proposed (unapplied)
- **Files written:** this RESULTS.md only. No `ops/` ledger write, no `.pine` touch.
- **Confabulations / unsourced facts quarantined:** none.
- **2024 divergence date:** Jun 5 → Sep 17 2024 (verified).
- **BoC 2022 + first-09:45-ET date:** 2022 array verified; first 09:45 ET = Jan 24 2024 (verified).
- **Concern (DONE_WITH_CONCERNS):** Proposal D — do not patch the verified array into the frozen BPC `.pine` during the forward window; record-and-defer instead.
- **Next action:** Joshua approves/declines Proposals A/B/C (ledger-only, low-risk); D deferred by recommendation.

## Sources
- Bank of Canada — Policy interest rate (key-rate history): https://www.bankofcanada.ca/core-functions/monetary-policy/key-interest-rate/
- BoC FAD releases 2022: `/2022/03/fad-press-release-2022-03-02/`, `/2022/04/...-04-13/`, `/2022/07/...-07-13/`, `/2022/09/...-09-07/`, `/2022/12/...-12-07/`
- BoC 2024: `/2024/01/fad-press-release-2024-01-24/`, `/2024/10/fad-press-release-2024-10-23/`, `/2024/12/fad-press-release-2024-12-11/`
- BoC communications-change (09:45 ET): `/2023/12/bank-canada-announces-changes-communications-interest-rate-decisions/`, `/2024/01/fad-announcement-release-mpr-january-24-2024/`
- BoC 2026 schedule: `/2025/08/bank-canada-publishes-2026-schedule-policy-interest-rate-announcements-other-major-publications/`
- Fed Sep 18 2024: FOMC statement; CNBC/JPMorgan/Fortune coverage
