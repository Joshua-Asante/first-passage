# Vet card — `VOLREGIME-NB1` (next-bar unsigned-range first-touch, MNQ)

**Date:** 2026-09-03  
**Author:** Cursor (Grok 4.6)  
**Status:** **`T0-FAIL` / withdrawn.** Decision and Novelty **retracted**. Not `VET-PASS`.
No candidate contract. Parent T0 closed `PRE-CONTRACT DROP`.  
**Parent T0:** [`2026-09-03-volregime-translation-t0.md`](2026-09-03-volregime-translation-t0.md)  
**Funnel:** [`2026-09-01-three-speed-alpha-research-design.md`](../superpowers/specs/2026-09-01-three-speed-alpha-research-design.md)
(`Proposed` — used as the Vet field list, not as standing doctrine).  
**Spend / K:** $0 / K=0 — no payoff comparison, no extraction probe.

This card authorizes nothing. Codex review of PR #281 (accepted 2026-09-03) showed the T0
“survives” read was wrong, so the earlier Decision/Novelty Clear scores are withdrawn.

## 1. Fields

| Field | Content |
|---|---|
| **Candidate ID** | `VOLREGIME-NB1` v0.1 draft — **rejected at T0** |
| **Observation / source** | Q-VOLREGIME-1 L1–L4 presence is pooled across ToD slots, not the first RTH bar. Observed L5 **not run**. |
| **Decision bridge** | Failed T0 — no cited convexity prior; path geometry not implied by unsigned-range elevation. |
| **Trade expression** | Not a live template. Not a gate on `ORB-MNQ-1`. Not exact P50. |
| **Role** | Would have been an entry construct. Conditioner-role class finding is unchanged. |
| **Raised-bar Route** | **Unpaid.** The 2026-09-03 waiver did not lift Q-VOLREGIME-1 §5’s Route conjunct. A single-index, flat-by-close OHLCV entry is inside [`rejected_candidates.md`](../rejected_candidates.md) (2026-07-21). No Route 1/2/3 argument was recorded. |
| **Data route** | $0. No probe. |

## 2. Six-gate read (retracted)

| Gate | Read | Basis |
|---|---|---|
| Decision | **Fail** (retracted from Clear) | T0 bridge is tautological / still a first-passage continuation claim. |
| Structural | **Not scored** | T0 failed first. |
| Cost | **Not scored** | T0 failed first. A later probe would need its own operator envelope and an append-only Confirm reservation *before* any read ([`tradeable-reachable`](../adr/2026-08-30-tradeable-reachable-gate.md) · [`campaign envelope`](../adr/2026-08-30-operator-approvals-campaign-envelope.md)). The campaign $0 / 48-core-hour envelope is **not** that approval. |
| Shape | **Not scored** | Same probe-envelope bar. |
| Power | **Not scored** | T0 failed first. |
| Novelty | **Fail** (retracted from Clear) | Closest prior art was omitted: [`mym_breakout_entry_2026_09/RESULTS.md`](../../lab/analysis/mym_breakout_entry_2026_09/RESULTS.md) — two-sided opening-range stop-entry, 1R, no robust candidate; names an independently justified volume conditioner as re-entry. That is adverse evidence, not a license. P50 / `GAPCOND-ORB-1` / `OPENPRESS-1` remain distinct but were not sufficient alone. |

## 3. Disposition

`T0-FAIL`. Do not open a candidate contract. Do not hash a founding freeze. Do not Explore.
Do **not** run a pre-freeze extraction probe — no surviving template, and no probe-specific GO
or Confirm-window reservation exists.

Allowed next steps: none on this template. Campaign terminal is `PRE-CONTRACT DROP` on the
T0 owner. A later translation would be a new Packet T after a cited convexity prior **and** a
recorded raised-bar Route, not a continuation of this card.

Forbidden: threshold grids; P50 reconstruction; Packet P / observed L5; stealing STATE `#1`;
treating the campaign envelope as a probe GO.
