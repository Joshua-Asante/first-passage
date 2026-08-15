# Q-STRIKER-MYM-RECON-1 — Is there a cost-reachable same-session MYM continuation edge?

**Status:** `CLOSED-AMBIGUOUS`
**Authored:** 2026-07-16
**Closed:** 2026-07-16
**Authors:** Joshua + Cursor
**Parent question:** ADR 2026-07-16 Striker→MYM/MNQ venue-native reconstruction
**Sub-questions opened:** none
**Loop:** Inquire-phase Pre-Q — gates the first reconstruction candidate before any Pine search
**Artifact path:** `docs/briefs/Q-STRIKER-MYM-RECON-1-venue-native-continuation.md`
**Closure:** [`closures/2026-07-16-striker-mym-reconstruction-candidate-1-ambiguous.md`](closures/2026-07-16-striker-mym-reconstruction-candidate-1-ambiguous.md)

---

## §0 — Rule 0 reads (production-source verification)

Read before authoring on 2026-07-16:

- [`docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md`](../adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md) — `9aa2dbf`; authorizes new venue-native candidates, forbids an R5/P2 re-run, and requires pre-registration before Pine search.
- [`core/strategies/striker/LOCK.md`](../../core/strategies/striker/LOCK.md) — `48a7a48`; locked CFD identity is long breakout + heavy pyramid and remains untouched.
- [`core/strategies/striker/striker_dj30_v4.5_mym_FUTURES_LOCK.md`](../../core/strategies/striker/striker_dj30_v4.5_mym_FUTURES_LOCK.md) — `fe83d17`; mapped edition exposes the cap/commission/force-flat constraints.
- [`lab/archive/striker_dj30_mym_prototype_2026-07/RESULTS.md`](../../lab/archive/striker_dj30_mym_prototype_2026-07/RESULTS.md) — `fad8984`; R5 failed edge preservation, but the mapped MYM edition was stable near PF 2 and explicitly said recovery would require entry-signal changes.
- [`docs/adr/2026-07-03-hardcore-p2-edge-transfer-gate.md`](../adr/2026-07-03-hardcore-p2-edge-transfer-gate.md) — `fad8984`; tolerant DJ30↔MYM divergence 8.51%, E1 failed, and shifted-window replay is permanently forbidden.
- [`core/firm_rules.py`](../../core/firm_rules.py) — `a53ee99`; verifies force-flat firms, contract caps, and index-micro costs. `ACTIVE_FIRM="FXIFY"` remains a historical fixture.
- [`docs/methodology/lessons/methodology_lessons.md`](../methodology/lessons/methodology_lessons.md) — `514a366`; opening-anchor tests require a same-day window-slide placebo.
- `core/data/bar_data/MYM_M15.csv` — working-tree SHA256 `298ab8c8900f1144b450537f14e356681aec7448b4787ebc770de88c83f9059c`; parsed from the 2026-07-16 BAR EXPORT, 141,471 bars, 2020-07-01→2026-07-02Z.

No locked Pine, allocation, `dd_protection`, or `ACTIVE_FIRM` value is changed by this question.

---

## §1 — Context & motivation

The spent locked-transfer attempts answered a narrower question: unchanged CFD Striker logic does not preserve enough edge on MYM. They did not test whether MYM supports a new, session-bounded Striker-family expression built around CME’s opening auction, low tick value, integer sizing, and mandatory force-flat.

MYM is first because the prior is cleaner than MNQ: tolerant feed divergence was 8.51% rather than 29.82%, the mapped edition remained profitable near PF 2, and the 2026-07-16 granularity floor is lower. This ordering does not prejudge the candidate.

Pre-Q gate:
  D: delete locked-CFD edge-preservation and shifted-window rescue from the working question — test: those claims were already falsified by R5/P2 and cannot answer a new-strategy question.
  S: compress the surviving issue to one instrument, one exact long-continuation candidate, one development window, and one untouched P&L holdout.
  A: bind all candidate semantics and verdict thresholds in the companion pre-registration before Pine or offline P&L is run.

---

## §2 — Prior art / lineage

- **P2 (`FALSIFIED-on-venue`)** — unchanged DJ30→MYM missed E1; this brief does not reopen it.
- **R5 MYM v0.1 (`FALSIFIED` for preservation)** — absolute MYM PF≈2 is a feasibility prior only, never proof of the new mechanism.
- **NAS100 ORB investigations** — opening-range evidence is mixed and instrument-specific; it supplies the correct same-day window-slide null, not a transferable edge claim.
- **Class-S candidate #1 (`DISCHARGED`, regime-fragile)** — proves a MYM+MNQ book can clear frozen firm geometry, but uses mapped panels and does not validate this candidate’s alpha.
- **Reconstruction ADR (`Accepted`)** — authorizes entry/hold redesign only as new artifacts with their own frozen gates.

---

## §3 — Question

**Q-STRIKER-MYM-RECON-1:** Does MYM contain a same-session directional-continuation opportunity that is frequent, opening-anchor-specific, cost-reachable, and positive on an untouched holdout under mandatory force-flat?

This names the symptom—whether such an opportunity exists—without asking which parameter should be tuned.

---

## §4 — Falsifiable hypothesis

**H-MYM-ORC-1:** If the exact opening-range continuation candidate frozen in the companion pre-registration (a) beats a same-day window-slide null on the development panel, (b) produces gross expectancy at least four times its measured all-in cost, and (c) remains positive, non-concentrated, and statistically supported on the untouched 2024-01-01→2026-06-30 holdout, then a first venue-native Striker→MYM candidate exists; otherwise this candidate is falsified and no variant may be substituted in place.

**Reject H-MYM-ORC-1 if:** any development or holdout hard gate in the companion pre-registration fails.

**Accept H-MYM-ORC-1 if:** every development and holdout hard gate passes with panel/config hashes pinned.

**Ambiguous-hold if:** a pre-scoring integrity or deterministic replay defect prevents a valid verdict; this is not a numerical near-pass category.

---

## §5 — Forbidden moves

- **Reusing locked Tue/Fri, lookback, or pyramid settings as a hidden rescue grid** — that would re-litigate R5/P2 and inflate K.
- **Looking at holdout P&L before the pre-registration is frozen** — only the disclosed frequency census has touched holdout dates.
- **Adding a second direction, day filter, volatility regime, stop, target, trail, or add rule after results** — any such change is candidate #2 and requires fresh operator authorization under the reconstruction ADR’s early-fail rule.
- **Calling absolute MYM profitability evidence that P2/R5 were wrong** — their edge-preservation claims remain falsified.
- **Selecting among placebo windows** — placebo windows define the null; they are not candidate variants.
- **Using outcome-conditional deletion** — losing days, years, fills, or forced-flat exits remain in the scored corpus.
- **Proceeding to prop-firm MC or rail work on a Stage-1/2 pass** — survivor scoring needs a separate frozen pre-registration; rail/account/live-spend remain gated.

---

## §6 — Gate criteria

The exact thresholds and candidate semantics live in:
[`pre-registration/2026-07-16-striker-mym-reconstruction-candidate-1-prereg.md`](pre-registration/2026-07-16-striker-mym-reconstruction-candidate-1-prereg.md).

| Verdict | Trigger condition | Disposition |
| --- | --- | --- |
| `RESOLVED` | Every development and untouched-holdout hard gate passes | Pin candidate Pine/CSV hashes; open a separate survivor-scoring pre-registration |
| `FALSIFIED` | Any validly-computed hard gate fails, including trade rate, cost law, anchor placebo, OOS economics, concentration, or temporal split | Close candidate #1; no in-place variant; a second MYM candidate requires fresh operator authorization |
| `AMBIGUOUS-HOLD` | Panel integrity, Pine/offline parity, or deterministic replay is defective so the gate cannot be validly computed | Repair the measurement defect only; rerun byte-identical candidate or close if repair changes semantics |

No criterion moves after the pre-registration is frozen.

---

## §7 — Execution plan

- **Phase 0 — freeze.** Operator reviews and signs the companion pre-registration. No candidate P&L is run before signature.
- **Phase 1 — offline development test.** Build the exact rule once; run Step-0, cost law, opening-anchor placebo, and development gates. Emit all metrics, not only passes.
- **Phase 2 — Pine parity + untouched holdout.** Implement the same semantics in a new gitignored/hash-pinned candidate Pine; require offline↔Pine signal parity, then score the holdout once.
- **Phase 3 — verdict.** Write a dated RESULTS + closure artifact. Only `RESOLVED` may open a separate firm-tier scoring pre-registration.

---

## §8 — Verdict pre-registration

Companion:
[`docs/briefs/pre-registration/2026-07-16-striker-mym-reconstruction-candidate-1-prereg.md`](pre-registration/2026-07-16-striker-mym-reconstruction-candidate-1-prereg.md).

Pre-registration commit hash: `1bc4eb1`
Pre-registration date: 2026-07-16

---

## §9 — Closure record

- `RESOLVED`: `docs/briefs/closures/2026-07-16-striker-mym-reconstruction-candidate-1-resolved.md`
- `FALSIFIED`: `docs/briefs/closures/2026-07-16-striker-mym-reconstruction-candidate-1-falsified.md`
- `AMBIGUOUS-HOLD`: `docs/briefs/closures/2026-07-16-striker-mym-reconstruction-candidate-1-ambiguous.md`

The closure must report every gate, all prior looks, hashes, actual trial count, and whether any criterion moved. Non-RESOLVED outcomes produce no recommendation.

---

## §10 — Audit hooks

```bash
# Rule-0 anchors
git log -1 --oneline -- core/strategies/striker/LOCK.md \
  lab/archive/striker_dj30_mym_prototype_2026-07/RESULTS.md core/firm_rules.py

# Locked sources and production risk controls remain untouched
git diff -- core/strategies/striker/LOCK.md core/config/params.toml \
  core/dd_protection.py core/firm_rules.py

# Companion pre-registration exists and remains one-candidate / no-grid
grep -n "K_reconstruction = 1\|NO GRID\|SIGNED / FROZEN" \
  docs/briefs/pre-registration/2026-07-16-striker-mym-reconstruction-candidate-1-prereg.md

# R5/P2 claim separation remains explicit
grep -n "R5/P2\|edge-preservation\|new candidate" \
  docs/briefs/Q-STRIKER-MYM-RECON-1-venue-native-continuation.md
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python scripts/check_brief.py \
  docs/briefs/Q-STRIKER-MYM-RECON-1-venue-native-continuation.md --type inquire

git log -1 --format="%h %cI" -- \
  docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md \
  core/strategies/striker/LOCK.md core/firm_rules.py

python scripts/check_data_manifests.py
```

---

## Pre-Lock Checklist

- [x] §0 paths read and anchored
- [x] §3 question passes symptom-only rephrase
- [x] §4 is falsifiable
- [x] §5 changes behavior
- [x] §6 is binary
- [x] Companion pre-registration operator-signed
- [ ] Companion pre-registration committed before Phase 1
- [x] §10 hooks are runnable
- [ ] Verification block passing
