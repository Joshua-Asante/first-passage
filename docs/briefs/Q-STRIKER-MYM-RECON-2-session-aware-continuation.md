# Q-STRIKER-MYM-RECON-2 — Can the MYM continuation candidate be measured across the actual session calendar?

**Status:** `CLOSED-FALSIFIED`
**Authored:** 2026-07-16
**Closed:** 2026-07-16
**Authors:** Joshua + Cursor
**Parent question:** ADR 2026-07-16 Striker→MYM/MNQ venue-native reconstruction
**Predecessor:** `S-MYM-ORC-01` — `CLOSED-AMBIGUOUS`
**Sub-questions opened:** none
**Loop:** Inquire-phase Pre-Q — gates the second reconstruction candidate after candidate #1's force-flat measurement defect
**Artifact path:** `docs/briefs/Q-STRIKER-MYM-RECON-2-session-aware-continuation.md`

---

## §0 — Rule 0 reads (production-source verification)

Read before authoring on 2026-07-16:

- [`docs/briefs/Q-STRIKER-MYM-RECON-1-venue-native-continuation.md`](Q-STRIKER-MYM-RECON-1-venue-native-continuation.md) — latest source anchor `812f68d`, verified 2026-07-16; supplies the original question, forbidden moves, and binary verdict structure.
- [`docs/briefs/pre-registration/2026-07-16-striker-mym-reconstruction-candidate-1-prereg.md`](pre-registration/2026-07-16-striker-mym-reconstruction-candidate-1-prereg.md) — latest source anchor `812f68d`, verified 2026-07-16; candidate #1 semantics and D0–D9/H0–H9 are the frozen baseline.
- [`lab/analysis/striker/striker_mym_reconstruction_candidate1_2026-07/candidate_offline.py`](../../lab/analysis/striker/striker_mym_reconstruction_candidate1_2026-07/candidate_offline.py) — lines 307–312 read 2026-07-16; verifies the hard requirement for a 16:00 bar and the exact exception that aborted the run.
- [`docs/superpowers/plans/2026-07-16-striker-mym-orc-development-harness.md`](../superpowers/plans/2026-07-16-striker-mym-orc-development-harness.md) — working-tree implementation plan read 2026-07-16; runner exit 2 is the registered `AMBIGUOUS-HOLD` path and result artifacts are written only after valid computation.
- [`docs/adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md`](../adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md) — latest source anchor `812f68d`, §2.3 read 2026-07-16; canonical DSR variance rule is unconditional `V=1/n`.
- `core/data/bar_data/MYM_M15.csv` — timestamp column only read 2026-07-16; panel SHA256 remains `298ab8c8900f1144b450537f14e356681aec7448b4787ebc770de88c83f9059c`. No OHLC, returns, fills, or P&L were read for this successor.
- [`lab/analysis/striker/striker_mym_reconstruction_candidate1_2026-07/session_calendar.json`](../../lab/analysis/striker/striker_mym_reconstruction_candidate1_2026-07/session_calendar.json) — 53 timestamp-derived mappings verified 2026-07-16; canonical working-tree-byte SHA256 `7ff65ef4b0bdceb620f077708e55075f5f4295ae6fd594a56595282e72a8a3bd`.

No locked Pine, allocation, `dd_protection`, `ACTIVE_FIRM`, or production risk-control value is changed by this question.

---

## §1 — Context & motivation

Candidate #1's development runner exited 2 before publishing artifacts because 2020-07-03 has no 16:00 bar. No metrics were emitted and no P&L was inspected. A non-P&L timestamp census found 53 early-close sessions in the declared panel, so the universal 16:00 requirement makes valid scoring impossible on calendar-defined short sessions.

The operator selected the registered close-and-reopen branch: close candidate #1 `AMBIGUOUS` and pre-register session-aware force-flat semantics. This successor changes only the session-clock interpretation required to make force-flat defined; every economic candidate semantic and gate remains fixed.

---

## §2 — Prior art / lineage

- **Q-STRIKER-MYM-RECON-1 / S-MYM-ORC-01 (`CLOSED-AMBIGUOUS`)** — aborted before result publication on a missing 16:00 force-flat bar; no economic verdict exists.
- **Candidate #1 pre-registration (`FROZEN`)** — supplies every unchanged signal, risk, add, exit, cost, placebo, development, parity, and holdout rule.
- **Candidate #1 closure (2026-07-16)** — records the operator-selected close-and-re-register disposition and the absence of inspected P&L.
- **DSR K/V supersession ADR (`Accepted`)** — successor H4 must use cumulative candidate-bank `K=2` and unconditional `V=1/n`; candidate #1's absent returns are not invented.
- **Reconstruction ADR (`Accepted`)** — authorizes venue-native candidates but forbids an in-place semantic rescue after a registered candidate fails its measurement contract.

---

## §3 — Question (Q-STRIKER-MYM-RECON-2)

**Q-STRIKER-MYM-RECON-2:** Can the exact same-session MYM continuation opportunity be validly measured across both standard and exchange-calendar early-close sessions without changing its economic rules or verdict thresholds?

This names the measurement symptom—undefined force-flat on valid short sessions—without asking which profitable parameter should be selected.

---

## §4 — Falsifiable hypothesis (H-MYM-ORC-2)

**H-MYM-ORC-2:** If the exact candidate #1 economics, augmented only by the frozen session calendar, pass D0's exact calendar/time/15m-adjacency checks and then clear every unchanged development and untouched-holdout gate, then a cost-reachable venue-native MYM continuation candidate exists; otherwise a valid hard-gate failure falsifies candidate #2, while a calendar/parity/integrity defect closes it `AMBIGUOUS-HOLD`.

**Reject H-MYM-ORC-2 if:** any validly-computed D1–D9 or H1–H9 gate fails.

**Accept H-MYM-ORC-2 if:** D0–D9 and H0–H9 all pass with panel, session-calendar, code, config, and output hashes pinned.

**Ambiguous-hold if:** D0/H0 fails, including any date membership, scheduled fill time, exact 15m trigger→fill adjacency, post-force-flat fill, deterministic replay, or implementation-integrity mismatch.

---

## §5 — Forbidden moves

- **Editing candidate #1 in place** — its frozen universal-16:00 semantic has already closed `AMBIGUOUS`; the operator selected a new registration.
- **Adding or deleting an early-close date after candidate P&L is viewed** — the exact 53-date calendar is frozen by hash before candidate #2 runs.
- **Inferring an early close dynamically from a day's last bar during scoring** — that would let missing/corrupt data silently redefine the exit; only exact allowlist membership may select 12:45/13:00.
- **Changing any candidate #1 signal, ATR, stop, size, add, target, maximum hold, cost, placebo, D1–D9, or H1–H9 threshold** — only force-flat calendar semantics differ.
- **Treating candidate #1 as if it produced valid returns** — it counts in cumulative `K=2`, but no return series or empirical variance is fabricated.
- **Using `K=1` or `var_trials=1` at H4** — successor H4 binds cumulative `K=2` and canonical `V=1/n`.
- **Reading holdout P&L before development and Pine parity pass** — timestamp-only holdout calendar counts do not authorize an economic look.
- **Outcome-conditional date, force-flat, year, seam, or losing-trade deletion** — all valid scheduled exits remain in the scored corpus.
- **Proceeding to firm-tier MC, rail, account registration, or live spend** — those remain separately gated.

---

## §6 — Gate criteria (closure verdict)

Exact semantics and thresholds live in:
[`pre-registration/2026-07-16-striker-mym-reconstruction-candidate-2-prereg.md`](pre-registration/2026-07-16-striker-mym-reconstruction-candidate-2-prereg.md).

| Verdict | Trigger condition | Disposition |
| --- | --- | --- |
| `RESOLVED` | D0–D9 and H0–H9 all pass | Pin candidate artifacts; open a separate survivor-scoring pre-registration |
| `FALSIFIED` | Any validly-computed D1–D9 or H1–H9 gate fails | Close candidate #2; no in-place variant |
| `AMBIGUOUS-HOLD` | D0/H0, deterministic replay, session-calendar membership/time/adjacency, or implementation integrity prevents valid scoring | Close or repair measurement byte-identically; any semantic change requires candidate #3 authorization |

No criterion moves after this successor pre-registration is frozen.

---

## §7 — Execution plan

- **Phase 0 — calendar-aware implementation.** Bind the canonical 53-date calendar by hash; add exact D0 allowlist/time/adjacency and post-force-flat assertions. Do not compute candidate P&L while implementing or testing timestamp semantics.
- **Phase 1 — development-only run.** Run the exact candidate once through unchanged D0–D9. Emit every registered artifact only after valid computation.
- **Phase 2 — Pine parity + untouched holdout.** After all development gates pass, implement identical calendar semantics in the gitignored/hash-pinned Pine candidate; require parity, then run the holdout once.
- **Phase 3 — verdict.** Apply the frozen table mechanically. Only `RESOLVED` may open survivor scoring.

---

## §8 — Verdict pre-registration

Companion:
[`docs/briefs/pre-registration/2026-07-16-striker-mym-reconstruction-candidate-2-prereg.md`](pre-registration/2026-07-16-striker-mym-reconstruction-candidate-2-prereg.md).

Pre-registration authority: operator choice “Close AMBIGUOUS and re-register session-aware force-flat semantics”

Signature: `SIGNED / FROZEN: 2026-07-16 / JA`

Commit hash: not populated; the operator explicitly requested no commit in this authoring session.

---

## §9 — Closure record format

- `RESOLVED`: `docs/briefs/closures/2026-07-16-striker-mym-reconstruction-candidate-2-resolved.md`
- `FALSIFIED`: `docs/briefs/closures/2026-07-16-striker-mym-reconstruction-candidate-2-falsified.md`
- `AMBIGUOUS-HOLD`: `docs/briefs/closures/2026-07-16-striker-mym-reconstruction-candidate-2-ambiguous.md`

The closure must disclose every gate, panel/calendar/config/code/output hashes, actual trial count, cumulative `K=2`, H4's `V=1/n`, all prior looks, and whether any criterion moved. Non-`RESOLVED` outcomes produce no recommendation.

**Actual closure:** [`docs/briefs/closures/2026-07-16-striker-mym-reconstruction-candidate-2-falsified.md`](closures/2026-07-16-striker-mym-reconstruction-candidate-2-falsified.md) — development D0/D1/D9 passed; D2–D8 failed; no Pine, parity, or holdout run.

---

## §10 — Audit hooks (runnable)

```bash
# Calendar identity and exact 53 mappings
sha256sum lab/analysis/striker/striker_mym_reconstruction_candidate1_2026-07/session_calendar.json
python -c "import json; p='lab/analysis/striker/striker_mym_reconstruction_candidate1_2026-07/session_calendar.json'; x=json.load(open(p)); assert len(x)==53; assert sum(v==765 for v in x.values())==41; assert sum(v==780 for v in x.values())==12"

# Successor keeps the cumulative bank and canonical variance rule
grep -n "K_reconstruction = 2\|cumulative K=2\|V = 1/n\|SIGNED / FROZEN:" \
  docs/briefs/pre-registration/2026-07-16-striker-mym-reconstruction-candidate-2-prereg.md

# Candidate #1 closure remains explicit about the aborted run
grep -n "exited 2\|No candidate P&L was inspected\|no valid return series" \
  docs/briefs/closures/2026-07-16-striker-mym-reconstruction-candidate-1-ambiguous.md

# Locked/production surfaces remain untouched
git diff -- core/strategies/striker/LOCK.md core/config/params.toml \
  core/dd_protection.py core/firm_rules.py
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python scripts/check_brief.py \
  docs/briefs/Q-STRIKER-MYM-RECON-2-session-aware-continuation.md --type inquire

sha256sum lab/analysis/striker/striker_mym_reconstruction_candidate1_2026-07/session_calendar.json

grep -n "D0\|D9\|H9\|K_reconstruction = 2\|V = 1/n" \
  docs/briefs/pre-registration/2026-07-16-striker-mym-reconstruction-candidate-2-prereg.md
```

---

## Pre-Lock Checklist

- [x] §0 paths read and anchored
- [x] §3 question passes the symptom-only rephrase test
- [x] §4 is falsifiable
- [x] §5 changes behavior
- [x] §6 is binary
- [x] Companion pre-registration operator-signed
- [x] No candidate #2 P&L was read before freeze
- [x] §10 hooks are runnable
- [ ] Verification block passing
