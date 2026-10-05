# CC handoff — four-firm re-MC §8 step 2a: input availability check

**Date:** 2026-10-05.
**Status:** FROZEN for execution, 2026-10-05. Joshua directly: "go on the availability check card".
**Brief type:** CC handoff, bounded read-only check (worker card).
**Authority:** operator go, 2026-10-05, to a coordinator (4) worker. The requirement owner is the four-firm dated re-MC prereg ([PR #616](https://github.com/Joshua-Asante/first-passage/pull/616) at `7f0cefb`), §8 step 2(a) and §7 blocker 3. O-4 names this check as the first build step.
**Rule:** existence, byte identity and header columns only. Reading no data row, counting no rows and computing no metric are what keep this check outside prereg §R.
**Return boundary:** a per-input table of status labels, paths and hashes, or a precise blocker. No series build, no harness edit and no prereg or ADR edit.

## §0 — Production reads

| Surface | Use |
|---|---|
| `core/strategies/BOOK_SOURCES.sha256` (`main@bb34ff0`) | Accepted book identity. The Pine pins are Aegis `db78ecba…`, Striker `712cf395…`, Vanguard `af26899c…` and ORB `176c4f70…`; the port pins are the four runtime ports |
| [identity ledger](../phase3-preparation/2026-09-15/identity-ledger.md) :19-108, :156-183 | Binds each export CSV to its Pine, port and panel by hash. ORB has bundles O-N and O-P; Striker has S-P, S-W1, S-W1P, S-W2 and S-W2P. Aegis and Vanguard each have one export, in the operator's Downloads (`D/`) |
| [ORB R2 ADR draft](../../adr/2026-09-12-orb-mnq-r2-supersession-DRAFT.md) :122 | O-N is "normal mode with adds" and O-P is "protected mode without" |
| [Track B scaling read](../../notes/2026-09-12-track-b-scaling-faithfulness-read.md) :100-110 | The fixed book's exports by mode:<br>• Normal: A-0 (Aegis, `71e732fc…`), S-0 (Striker, `5a500658…`), V-0 (Vanguard, `7b9cc65c…`) and O-N (ORB).<br>• Protected: S-P (Striker; Account Size × 0.40) and O-P (ORB; base one micro, no adds).<br>• Aegis protected is the fixed-size rule, verified against A-0 by timing invariance; Vanguard protected means no entries.<br>• S-W1, S-W1P, S-W2 and S-W2P are WATCH lifecycle tiers, not the 1.00× book |
| `ops/c1_rail/book_policy.py` :18-29, :137, :229-318, :431-450 | The protected mode is integer-quantity: base sizes are rescaled per leg, the ORB base is fixed and adds are refused. The mode is set from the prior session's close against the running peak, with no latch |
| [campaign record](../programs/2026-09-03-seven-strategy-select-campaign-state.md) D11, :194 | The pre-edition exports crossed the 16:45 ET flatten. The venue-bound (VB) editions are the re-expressions |
| [candidate #1 prereg](../pre-registration/2026-07-15-existing-strategy-book-candidate-1-prereg.md) §3 | The calibration reference is the 3-leg full-Aegis futures3 remc book. `lab/CATALOG.md` :265 places that panel in `first-passage-archive` |

## §0.5 — Clarifications resolved at freeze

1. **Private roots:**
   - `E/` = `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/inputs/private_overrides/op1/2026-09-14-seven/`, in the primary checkout.
   - `D/` = `C:\Users\joshu\Downloads`.
   - The checker reads them in place and copies nothing.
2. **What counts as a header:** a CSV's first line, or for the archived panel its column names. The checker reads nothing below that line.
3. **Adverse-excursion column:** a column whose name contains `Drawdown` or `Adverse`, case-insensitive. TradingView names it "Drawdown USD" (newer exports: "Adverse excursion USD").

## §1 — Goal

For each gating input, return exactly one status:

- `AVAILABLE`: file present, hash equals the ledger pin, and an adverse-excursion column is present.
- `PRESENT-NO-EXCURSION`
- `HASH-MISMATCH`
- `MISSING`
- `UNBOUND`: no ledger pin ties it to the accepted identity.
- `DERIVED`: no export is needed, because the protected mode follows from the normal export by a rule already recorded (§0, Track B read).

The gating inputs are:

| Input | Leg | What it is |
|---|---|---|
| N-1 | Aegis | normal-mode export |
| N-2 | Striker | normal-mode export, S-0 |
| N-3 | Vanguard | normal-mode export |
| N-4 | ORB | normal-mode export, O-N |
| P-1 … P-4 | all four legs | protected mode: Aegis by rule (DERIVED), S-P, Vanguard by rule (no entries, DERIVED), O-P |
| REF | calibration reference | panel, plus any intraday source |

## §4 — Hypothesis and falsifier

**H:** the four normal-mode exports are AVAILABLE. **Falsified by** any N-row that is not AVAILABLE; that input then reads INSUFFICIENT under prereg §4 unless the operator re-rules.

The P-rows and REF are reported, not gated. The P-rows bear on O-8 (see §6).

## §5 — Constraints and forbidden moves

- No data row is read, no rows are counted, no date span is taken and no P&L is summed. Byte hashing reads whole files, but nothing beyond the header line is parsed or printed.
- Pine, port bodies and setting values are not opened. Nothing private is copied or committed.
- Nothing goes to `glm_agent` or any external service.
- No series build, harness edit or prereg edit.

## §6 — Acceptance and return taxonomy

- **DONE:** every row has a status and its evidence (path, SHA-256, header column names).
- **DONE_WITH_CONCERNS:** DONE plus a finding that affects a ruled prereg item. A known one is O-8, if protected behaviour is not a P&L scale (§0, `book_policy.py`).
- **NEEDS_CONTEXT** or **BLOCKED:** with the exact obstruction.

The return is recorded in §7 of this card and posted on PR #616.

```yaml authority
seat: worker
parent: docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md
max_risk: medium
capabilities: [repository.read, worktree.write, branch.push, pr.open]
constraints:
  - no_main_write
  - no_merge
  - header_and_hash_only
  - no_private_copy_or_commit
  - no_pine_or_port_body_read
  - no_series_build
  - no_metric_or_row_count
  - no_owner_record_edit
acceptance:
  - every_gating_row_has_status_path_and_hash
```

## §7 — Return (2026-10-05, executor: the same worker)

**DONE_WITH_CONCERNS.** H holds: all four normal-mode exports are AVAILABLE. Each hash below is a fresh SHA-256 that equals its ledger or Track B pin. Every export has TradingView's 17-column trade-list header, which includes `Adverse excursion USD`. No data row was parsed.

| Row | Input | Status | Location (`E/`, `D/` per §0.5) | SHA-256 |
|---|---|---|---|---|
| N-1 | Aegis A-0 | `AVAILABLE` | `D/Aegis_6J1_VB_CME_6J1!_2026-09-03_cc310.csv` | `71e732fc92d28a56fbc1e4aa358e10b68f317a110f3facc95ed34508fad96eaa` |
| N-2 | Striker S-0 | `AVAILABLE` | `D/Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-09-03_9d7ea.csv` | `5a5006588fa5c87628df7b1c15c8af8d8ae2250be0abb0371ea4d93665ef998e` |
| N-3 | Vanguard V-0 | `AVAILABLE` | `D/Vanguard_Gold_Futures_v0.4_VB_(MGC)_COMEX_MINI_MGC1!_2026-09-03_0e3e3.csv` | `7b9cc65c98945055f35d55cdd43f049efc4b5924e2caa59f36d50b3eb872f9f2` |
| N-4 | ORB O-N | `AVAILABLE` | `E/step6-admission/exports/O-N.csv` | `8e4902c3ee6224f57e29c8e1e0491c5c70695978d38036cfdc380eaded15e861` |
| P-1 | Aegis protected | `DERIVED` | fixed-size rule on A-0 (Track B read :100) | — |
| P-2 | Striker S-P | `AVAILABLE` | `E/step6-admission/exports/S-P.csv` | `0373f211f5e44fe89976d7bcea2b7252724dc717541116dccb59932dfabc710a` |
| P-3 | Vanguard protected | `DERIVED` | no entries (Track B read :101) | — |
| P-4 | ORB O-P | `AVAILABLE` | `E/step6-admission/exports/O-P.csv` | `2cb58fb6b0ec81f5859db527821a1701675ba6305553369d9096d5ee2bd93e40` |
| REF | full-Aegis reference | `MISSING` | panel not retained. The Aegis ae744 leg export is present and listed in `core/data/tv_exports/cme/SHA256SUMS` (`e82a2c25…`), and carries `Adverse excursion USD`. But the assembled panel and `calibration_report.json` are not retained in `lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/`, and the archive keeps only `NOTES.md`/`RESULTS.md`. The MYM/MNQ leg exports were not pinned or checked | — |

**Concerns:**

1. **O-8 premise contradicted (a NEEDS_CONTEXT for the prereg, not for this card).** `book_policy.py` makes protection a quantity rule per leg, not a P&L scale:
   - Striker sizes at Account Size × 0.40;
   - the ORB base stays one micro and adds are refused;
   - Aegis follows a fixed-size rule;
   - Vanguard takes no entries.

   The kernel's continuous `dd_scale` therefore cannot pass the O-8 parity test as ruled. Because the P-rows are available or derivable, a faithful alternative exists: a mode-switching bootstrap. Each day would carry a paired normal and protected P&L/`intraday_low`, and the path would choose the protected channel on days the prior close sits ≥ 1% below the running peak. That needs a kernel or wrapper change. Ruling owed by the operator.
2. **No `intraday_low` is native to the exports.** The builder must derive the daily low from per-trade `Adverse excursion USD`. The conservative coincident-sum construction stays as recommended.
3. **REF must be reassembled.** Its panel is not retained.
4. **Location:** three normal exports (A-0, S-0, V-0) live only in the operator's Downloads. The builder card should name `D/` as a read root, or the operator copies them into `E/` first.

## §10 — Audit hooks

```bash
c=docs/briefs/handoffs/2026-10-05-four-firm-remc-availability-check-card.md
# Every gating row carries a status in the return (expect 9: N-1..N-4, P-1..P-4, REF).
grep -cE '^\| (N-[1-4]|P-[1-4]|REF) \| [^|]+ \| `(AVAILABLE|PRESENT-NO-EXCURSION|HASH-MISMATCH|MISSING|UNBOUND|DERIVED)`' "$c"
# No private CSV, Pine or port is tracked by this change (absence exits 0).
! git diff --name-only origin/main...HEAD | grep -E '\.(csv|pine|py)$'
```
