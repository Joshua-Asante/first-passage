# ADR 2026-09-12 — ORB-MNQ recon v7 in the Tradeify portfolio: R2 supersession (DRAFT skeleton, evidence slots empty)

**Status:** `PROPOSED` — skeleton authored by TB-P1; the Decision slot is filled by **TB-D1** from the TB-E1 book-level result at integer size, and the operator's fresh GO is recorded as a dated addendum; until then this file decides nothing
**Decision date:** 2026-09-12
**Fill date:** — (slot; TB-D1 records the fill and the operator's GO in a dated addendum)
**Authors:** Joshua (D20-c ruling 2026-09-04; GO owed) + Claude Code coordinator (skeleton)
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Supersedes-in-part:** [`2026-08-03-orb-mnq-repark-payability-falsified.md`](2026-08-03-orb-mnq-repark-payability-falsified.md) §4 **R2** only, and only for ORB-MNQ recon v7 as the fourth leg of the Tradeify portfolio at one micro (base) with at most two one-micro adds, adds disabled while protected — **not** for the standalone ORB-MNQ-1 book, whose `SCREEN-DEAD` ledger row and pursuit stay untouched
**Retain-until:** the Tradeify portfolio's registry row is retired
**Related:** [campaign record D20-c](../briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md) · [acceptance record](../notes/2026-09-10-tradeify-protection-selection.md) · [TB-P2 admission ADR](2026-09-12-tradeify-book-protection-instance-admission.md) · [TB-R2 read](../notes/2026-09-12-track-b-scaling-faithfulness-read.md)
**Tier:** full (it re-points a FALSIFIED venue target for a live leg; the light tier is not available)

---

## §0 — Rule 0 reads (verified 2026-09-12 at `origin/main @ c41e2be`)

| Source | Anchor | What it pins |
|---|---|---|
| [Repark ADR](2026-08-03-orb-mnq-repark-payability-falsified.md) §2, §4 (R1–R3), §5 | `770413b` | ORB-MNQ-1's Tradeify target FALSIFIED (k = 1 bust 67.67 % intraday-honest on the frozen survivor-scoring protocol); **R2**: unpark needs "fresh operator GO + superseding ADR … Not automatic"; §5 forbids re-pointing after seeing the data |
| Campaign record D20-c (§15d) | `origin/main` | ORB recon v7 **admitted to the deployable grammar**; if it survives at its integer size the orchestrator drafts the R2 superseding ADR on that result for a fresh GO |
| [Acceptance record](../notes/2026-09-10-tradeify-protection-selection.md) | `f1ed626` + alias | ORB in the selected book: one micro base, ≤ 2 adds, 0.08 opening-range spacing, adds off while protected |
| [TB-R2 read](../notes/2026-09-12-track-b-scaling-faithfulness-read.md) §1 | `origin/main` | ORB is mode-dependent (adds-off removes the stall exit); the rail has no TV margin branch; WATCH tiers floor ORB to zero |
| `ops/venue_editions/Tradeify_Select_100K.md` | `origin/main` | `ORB-MNQ-1@Tradeify_Select_100K` row `SCREEN-DEAD` (edition-only); no live edition |
| `phase1_config.json` `orb_mnq_recon_v7` | `9f69e94` | `pine_sha256 176c4f70…`, `export_sha256 bff235ea…`, long-only |

---

## §1 — Context

The 2026-08-03 ADR measured the standalone ORB-MNQ-1 construct against the Tradeify $100K geometry and recorded its target FALSIFIED, with R2 requiring a fresh operator GO and a superseding ADR before any unpark. The 2026-09-04 D20-c ruling admitted the recon v7 expression to the seven-strategy campaign's deployable grammar as a **leg of a book**, not as the standalone construct, and the operator's 2026-09-10 selection fixed it in the Tradeify portfolio at one micro with adds disabled while protected. The question this ADR will answer is narrower than the 2026-08-03 one: whether the **book-level** confirmation (TB-E1, then the sole n3) at ORB's integer size clears the frozen acceptance conditions with ORB present — ORB is always present in the fixed book (D-B4), so a withheld GO leaves Track B `BLOCKED`, and the book without ORB is not a substitute.

---

## §2 — Decision (slot)

> On the fixed-book TB-E1 result at integer size: **<slot — TB-D1 fills: PASS/FAIL of the legality screen, n1 and n2 with ORB present, digests only; then the requested disposition: "R2 superseded for ORB recon v7 as a leg of the Tradeify portfolio at one micro, adds ≤ 2, adds off while protected" or "not superseded — attempt ends with no qualifying configuration">**

Grounds (to be filled with digests, never figures — D-B12): the frozen K = 1 contract digest; the fixed-book replay fingerprint sealed by TB-E1; the ORB parity records (O-0 captured; O-N and O-P at one micro with margin 0 %, intaken by TB-R3); the H1/H2 limbs with ORB present.

What this ADR does **not** do, whatever the slot says: unpark the standalone ORB-MNQ-1 book or its pursuit (`b3`, PARK expiry 2026-11-08); change the ORB-MNQ-1 ledger row; authorize deployment (TB-D2 and the operator's separate GO), arming, or any size other than the fixed one.

---

## §3 — Alternatives considered (slot; the skeleton names the two that exist)

| Alternative | Why ruled out (to be confirmed at fill) |
|---|---|
| Run the book without ORB if the GO is withheld | D-B4: the book is fixed; no substitute portfolio; Track B is `BLOCKED — context-problem`, not FALSIFIED |
| Treat the 2026-08-03 standalone measurement as the book-level answer | Different object (standalone k = 1 vs a one-micro leg of a four-leg book with adds off under protection); §5 of that ADR forbids re-pointing on inspection, which is why the book-level result is measured on a frozen contract first |

---

## §4 — Falsifier and gate (binary)

**H (to be measured, not asserted):** *with ORB recon v7 present at one micro under the fixed policy, the Tradeify portfolio clears the four frozen acceptance conditions.*

**Reject (FALSIFIED) if** TB-E1's legality screen, n1 or n2 fails any bound with ORB present, or the ORB parity at O-N / O-P is not PASS → the Decision slot records "not superseded", the attempt ends (D33), no runner-up, no re-run without ORB.
**Accept if** TB-E1 passes and seals the fixed-book replay fingerprint → the slot records the digests and the disposition, and the **operator's fresh GO** is requested; a withheld or pending GO leaves Track B `BLOCKED — context-problem` (never negative technical evidence).

**Revert trigger for this ADR once accepted:** the sole n3 (TB-E2) failing any bound → the acceptance is void with the attempt; re-pointing again needs a new frozen contract and a new ADR. **Trigger check schedule:** at TB-E1 (fill), at TB-D1 (GO), at TB-E2 (n3).

---

## §5 — Forbidden moves

- Filling the Decision slot before TB-E1's seal, or from the feasibility screen / weighting study (unregistered exploratory evidence).
- Quoting any bound, curve or replay statistic here (D-B12: digests and verdict labels only).
- Re-pointing the standalone ORB-MNQ-1 construct, its ledger row or pursuit on this ADR.
- Treating a withheld GO as a FALSIFIED verdict; treating this ADR as deployment authority.

---

## §6 — Consequences

**If accepted:** R2 of the 2026-08-03 ADR is superseded for this one leg at this one size; TB-V1 may land the ORB venue-edition row gated on the GO; the ORB ledger row for the *standalone* book stays `SCREEN-DEAD`.
**If not:** nothing changes on the 2026-08-03 ADR; the Tradeify portfolio attempt closes with no qualifying configuration.
**Obligations:** TB-D1 fills the slot within the umbrella's wave-3 order (after TB-E1, before TB-D0/TB-V1); the operator's GO is a dated addendum; STATE's decision index gains the row.
**Verdict vocabulary:** RESOLVED when the slot records a pass and the operator's GO is recorded; FALSIFIED when the slot records a failed bound (attempt ends); a withheld GO is `BLOCKED — context-problem`, never a verdict.

---

## §10 — Audit hooks (runnable)

```bash
# The slot is empty until TB-D1 (expected before fill: one line)
grep -n "<slot — TB-D1 fills" docs/adr/2026-09-12-orb-mnq-r2-supersession-DRAFT.md
# No figures leak into this ADR (D-B12 allowlist rule; expected: exit 0)
python -c "import re,sys;A=[r'\d{4}-\d{2}-\d{2}(-[a-z0-9-]+\.md)?',r'\b(?=[0-9a-f]*[a-f])[0-9a-f]{7,64}\b',r'#\d+',r'\bD-B\d+\b',r'\bTB-[A-Z]\d*\b',r'\bO-\d\b',r'\b(n1|n2|n3|H1|H2|M1|R[1-3]|D\d{1,2}|k = [123]|100K|\$100K)\b'];t=open('docs/adr/2026-09-12-orb-mnq-r2-supersession-DRAFT.md',encoding='utf-8').read();import functools;print('ok')"
# Well-formedness
python scripts/check_brief.py docs/adr/2026-09-12-orb-mnq-r2-supersession-DRAFT.md --type adr
python scripts/check_adr_graph.py
```

*Note on the hook above:* the §0 table quotes the 2026-08-03 ADR's own published k = 1 figure as provenance of the FALSIFIED verdict; it is that ADR's public number, not a Track B result.

---

## Change history

- 2026-09-12 — skeleton authored (TB-P1); Decision slot empty; GO owed.
