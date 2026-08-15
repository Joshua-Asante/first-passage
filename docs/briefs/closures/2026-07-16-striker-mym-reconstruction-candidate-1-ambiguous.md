# S-MYM-ORC-01 closure — AMBIGUOUS (session-calendar measurement defect)

**Verdict:** `CLOSED-AMBIGUOUS`
**Closed:** 2026-07-16
**Operator decision:** close candidate #1 and re-register session-aware force-flat semantics
**Authority:** Joshua (operator)
**Candidate:** `S-MYM-ORC-01`
**Pre-registration:** [`2026-07-16-striker-mym-reconstruction-candidate-1-prereg.md`](../pre-registration/2026-07-16-striker-mym-reconstruction-candidate-1-prereg.md)
**Successor:** [`Q-STRIKER-MYM-RECON-2`](../Q-STRIKER-MYM-RECON-2-session-aware-continuation.md)

---

## 1. Gate that fired

The first development runner invocation exited **2** before publishing any result artifact:

```text
AMBIGUOUS-HOLD: 2020-07-03: missing required 16:00 force-flat bar
```

This is candidate #1's §6.4 `AMBIGUOUS-HOLD` branch: an implementation/measurement defect prevented a valid computation. The runner emitted no metrics, trades, placebo results, or development report. No candidate P&L was inspected, and no holdout P&L was opened.

No D1–D9 economic gate was computed. This closure therefore makes no profitability, cost-reachability, placebo, drawdown, or statistical claim.

---

## 2. Non-P&L timestamp diagnostic

A timestamp-only census of `core/data/bar_data/MYM_M15.csv` found **53** allowlisted early-close sessions:

- development: **29** sessions — 23 with final available RTH bar open at 12:45 ET (minute 765), 6 at 13:00 ET (minute 780); **16** had an opening-range break;
- untouched holdout: **24** sessions — 18 at minute 765, 6 at minute 780; **12** had an opening-range break;
- combined: **53** sessions — 41 at minute 765 and 12 at minute 780.

The opening-range-break figures are event-frequency diagnostics only. No returns, fills, trade P&L, aggregate P&L, or economic metric was read.

The exact date→force-flat-fill-minute mapping is:

`lab/analysis/striker/striker_mym_reconstruction_candidate1_2026-07/session_calendar.json`

Canonical working-tree-byte SHA256:

```text
7ff65ef4b0bdceb620f077708e55075f5f4295ae6fd594a56595282e72a8a3bd
```

---

## 3. Why candidate #1 closes

Candidate #1 froze a universal 15:45 trigger→16:00 fill and required a 16:00 bar on every signal date. The panel's exchange-calendar early closes make that semantic undefined on the 53 listed dates. Supplying an early-close schedule changes §2 force-flat semantics; it is not a byte-identical measurement repair.

Per candidate #1 §6.4 and brief-authoring Known Trap #12, the frozen candidate is not edited in place. The operator explicitly selected: **“Close AMBIGUOUS and re-register session-aware force-flat semantics.”**

---

## 4. Disposition and candidate bank

- `S-MYM-ORC-01` is terminal `CLOSED-AMBIGUOUS`; no recommendation is produced.
- The reconstruction candidate bank increments to `K_reconstruction = 2` when successor `S-MYM-ORC-02` is registered.
- Candidate #1 produced no valid return series. It remains a spent semantic candidate in the cumulative K count, but contributes no fabricated returns or empirical variance estimate to successor H4.
- Candidate #2 must use cumulative `K=2` and the canonical unconditional `V=1/n` rule, where `n` is candidate #2's valid holdout completed-trade count.
- Locked Pine, `core/`, allocation, `dd_protection`, `ACTIVE_FIRM`, firm-tier MC, rail, account registration, and live spend remain untouched.

---

## 5. Successor constraint

The successor keeps every candidate #1 semantic and D0–D9/H0–H9 threshold unchanged except force-flat becomes session-calendar aware:

- standard session fill remains 16:00 ET, ordered at 15:45 ET;
- an allowlisted early-close date fills at its final available RTH bar open (12:45 or 13:00 ET), ordered exactly one 15m bar earlier;
- D0 requires exact allowlist membership, exact scheduled fill time, and exact 15m trigger→fill adjacency;
- any calendar/time/adjacency mismatch is `AMBIGUOUS-HOLD`;
- no entry or exit may fill after that date's scheduled force-flat.

Authority and exact gates are frozen in the successor pre-registration.

---

## 6. Audit hooks

```bash
# Confirm the historical candidate-1 abort remains recorded after the shared
# study directory receives candidate-2 result artifacts.
grep -n "missing required 16:00 force-flat bar\|emitted no metrics" \
  docs/briefs/closures/2026-07-16-striker-mym-reconstruction-candidate-1-ambiguous.md
grep -n "S-MYM-ORC-02" \
  lab/analysis/striker/striker_mym_reconstruction_candidate1_2026-07/DEVELOPMENT_RESULTS.md

# Confirm the canonical timestamp-only calendar bytes
sha256sum lab/analysis/striker/striker_mym_reconstruction_candidate1_2026-07/session_calendar.json

# Confirm successor authority and K/V rule
grep -n "SIGNED / FROZEN:\|K_reconstruction = 2\|V = 1/n" \
  docs/briefs/pre-registration/2026-07-16-striker-mym-reconstruction-candidate-2-prereg.md
```
