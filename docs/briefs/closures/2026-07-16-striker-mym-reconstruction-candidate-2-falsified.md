# S-MYM-ORC-02 closure — FALSIFIED at development

**Verdict:** `CLOSED-FALSIFIED`
**Closed:** 2026-07-16
**Candidate:** `S-MYM-ORC-02`
**Question:** [`Q-STRIKER-MYM-RECON-2`](../Q-STRIKER-MYM-RECON-2-session-aware-continuation.md)
**Frozen authority:** [`2026-07-16-striker-mym-reconstruction-candidate-2-prereg.md`](../pre-registration/2026-07-16-striker-mym-reconstruction-candidate-2-prereg.md)
**Development result:** [`DEVELOPMENT_RESULTS.md`](../../../lab/analysis/striker/striker_mym_reconstruction_candidate1_2026-07/DEVELOPMENT_RESULTS.md)
**Recommendation:** none

No reserved-holdout P&L was read or computed. The valid development run mechanically fired the frozen `FALSIFIED` branch; execution stops before Pine, parity, holdout, firm-tier MC, rail, account registration, or live spend.

---

## §0 — Rule 0 reads and evidence anchors

Read before authoring this closure on 2026-07-16:

- `docs/briefs/pre-registration/2026-07-16-striker-mym-reconstruction-candidate-2-prereg.md` — operator-signed `FROZEN`; §6.2 makes any valid D1–D9 failure terminal `FALSIFIED`.
- `lab/analysis/striker/striker_mym_reconstruction_candidate1_2026-07/DEVELOPMENT_RESULTS.md` — development verdict and D0–D9 table, read 2026-07-16.
- `lab/analysis/striker/striker_mym_reconstruction_candidate1_2026-07/development_metrics.json` — exact gate booleans, metrics, Step-0 result, and fingerprints, read 2026-07-16.
- `lab/analysis/striker/striker_mym_reconstruction_candidate1_2026-07/placebo_results.json` — exact 10,000-assignment opening-anchor null result, read 2026-07-16.
- `lab/analysis/striker/striker_mym_reconstruction_candidate1_2026-07/artifact_manifest.json` — input/config/script/output hashes, canonical working-tree-byte SHA256 `67c842ef05640183be07885096af4d1e9f875d1c21aae0aa3782353ea1998b52`, verified 2026-07-16.

No `HOLDOUT_RESULTS.md`, reserved-holdout return series, holdout trade file, or holdout P&L was opened.

---

## §1 — Context and mechanical verdict

Candidate #1 closed `AMBIGUOUS` before emitting metrics because its universal 16:00 force-flat was undefined on valid early-close sessions. The operator authorized candidate #2 with an exact 53-date session calendar and otherwise unchanged economics/gates.

Candidate #2 completed a valid development-only measurement: D0 passed, so the result is economically adjudicable rather than ambiguous. D2–D8 all failed. Under frozen §6.4, any one valid D1–D9 failure is terminal `FALSIFIED`; seven independent gate failures fired.

---

## §2 — Headline evidence

- Completed base trades: **403**
- Gross expectancy: **0.04731270738440974R**
- Net expectancy: **−0.020966243740373685R**
- Mean actual cost: **0.06827895112478342R**
- Gross expectancy / mean actual cost: **0.6929325451696416**
- Net profit factor: **0.9513729444634695**
- Max closed-equity drawdown: **6.624995744263564%**
- Stationary-bootstrap block size: **1**
- 95% CI for mean net R: **[−0.12207470921977549, 0.0805699492231894]**
- Opening-anchor placebo p: **0.21437856214378562**
- First-half net expectancy: **−0.0366976777944947R**
- Second-half net expectancy: **−0.0051565438451874005R**
- Drop-top-five net expectancy: **−0.06727320147816056R**
- Development DSR diagnostic: **0.1801302824215807**; not a substitute for any failed D-gate

The key result is not a near-pass: gross edge was only **0.692933×** measured cost versus the frozen **4.00×** hurdle, net expectancy and PF were negative/sub-1, and the 09:30 opening anchor did not beat the registered same-day window-slide null.

---

## §3 — Execution and integrity diagnostics

- Step-0: **PASS**
- Panel: 141,471 rows, `2020-07-01T00:00:00Z`→`2026-07-02T00:00:00Z`
- Calendar: 53 mappings; 41 at minute 765 and 12 at minute 780; 1,548 eligible sessions checked
- ET UTC offsets observed: −5 and −4 hours
- Signals / completed base trades: 403 / 403
- Standard-session / allowlisted-session trades: 387 / 16
- Force-flat trades: 12
- Fills after scheduled force-flat: 0
- Maximum contracts: 34
- Quantity-zero skips / rate: 0 / 0.0
- Signals suppressed by scheduled force-flat: 0
- Seam-tagged trades: 0

These diagnostics establish that the session-aware measurement repair worked. They do not rescue the economic failures.

---

## §4 — Falsifiable hypothesis verdict

**H-MYM-ORC-2:** If the exact candidate cleared D0–D9 and then H0–H9, a cost-reachable venue-native MYM continuation candidate would exist; otherwise any validly-computed D1–D9 or H1–H9 failure would falsify it.

**Verdict:** H-MYM-ORC-2 is **FALSIFIED at development**. D0 passed, and D2–D8 validly failed. The untouched-holdout branch is neither needed nor authorized.

This is the pre-registered “otherwise” outcome, not an amended interpretation after seeing results.

---

## §5 — Required stop and forbidden continuations

- **No Pine implementation.**
- **No offline↔Pine parity run.**
- **No holdout run or holdout P&L read.**
- **No survivor-scoring or firm-tier MC.**
- **No rail build, account registration, live spend, or deployment work.**
- **No lower-cost rerun, parameter grid, opening-window selection, date deletion, or gross-only rescue.**
- **No in-place candidate #2 semantic or threshold edit.**
- **No candidate #3 without fresh operator authorization and a fresh frozen pre-registration.**

No recommendation is produced for this non-`RESOLVED` verdict.

---

## §6 — Exact D0–D9 gate audit

Frozen verdict taxonomy: all D0–D9 and H0–H9 passing would be `RESOLVED`; any valid D1–D9 or H1–H9 failure is `FALSIFIED`; an integrity defect preventing valid computation is `AMBIGUOUS-HOLD`. D0 passed here, so the failures below mechanically select `FALSIFIED`.

| Gate | Frozen criterion | Observed | Result |
| --- | --- | --- | --- |
| D0 | Step-0 integrity, exact calendar/time/adjacency, zero post-scheduled-force-flat fills | Step-0 PASS; panel/calendar exact; fills after scheduled force-flat = 0 | **PASS** |
| D1 | N ≥ 120 completed base trades | N = 403 | **PASS** |
| D2 | Opening-anchor placebo p < 0.05 | p = 0.21437856214378562 | **FAIL** |
| D3 | gross expectancy / mean actual cost_R ≥ 4.00 | 0.6929325451696416 | **FAIL** |
| D4 | net expectancy > 0R and PF ≥ 1.25 | −0.020966243740373685R; PF 0.9513729444634695 | **FAIL** |
| D5 | stationary-bootstrap 95% CI lower bound > 0 | CI [−0.12207470921977549, 0.0805699492231894], lower < 0 | **FAIL** |
| D6 | first-half and second-half net expectancy both > 0R | −0.0366976777944947R / −0.0051565438451874005R | **FAIL** |
| D7 | drop-top-five net expectancy > 0R | −0.06727320147816056R | **FAIL** |
| D8 | max closed-equity DD ≤ 6.0% | 6.624995744263564% | **FAIL** |
| D9 | zero fills after scheduled force-flat; contracts ≤80; quantity-zero skip rate ≤5% | 0 fills; max 34; rate 0.0 | **PASS** |

Mechanical gate vector: `D0 PASS, D1 PASS, D2 FAIL, D3 FAIL, D4 FAIL, D5 FAIL, D6 FAIL, D7 FAIL, D8 FAIL, D9 PASS`.

---

## §7 — Artifact and provenance hashes

### Inputs and frozen config

| Artifact | SHA256 |
| --- | --- |
| `core/data/bar_data/MYM_M15.csv` | `298ab8c8900f1144b450537f14e356681aec7448b4787ebc770de88c83f9059c` |
| `session_calendar.json` | `7ff65ef4b0bdceb620f077708e55075f5f4295ae6fd594a56595282e72a8a3bd` |
| `runspec.json` | `a55a6b5d9eab85800a9cd33f25b6ae10410a4f0d19ad29985ec8bf9840843d0d` |

### Scripts

| Artifact | SHA256 |
| --- | --- |
| `candidate_offline.py` | `a3e25d72845f08c3d8096b7c5be443d5503b4192115f8f3c2bc5d9234aa14acd` |
| `run_development.py` | `896b03cd71ed89feff804581937ab4b49a3f617ea6bd71756055e5e56d8bfd82` |

### Development outputs

| Artifact | SHA256 |
| --- | --- |
| `DEVELOPMENT_RESULTS.md` | `7598b59f4a684dfc873a2b8911335b0de3e117e738655ac248e18356f6ee5a40` |
| `development_events.csv` | `606b5082a954c126b809d5b2f7b8685329432ecc1154c20559cfa0c964cd0b1c` |
| `development_metrics.json` | `97c8ed94f98e06c0dd9909074dbe83d2b0f2e50072c235ef200737ec7ea363c3` |
| `development_trades.csv` | `3aa452f420b18908e3482c042edb8354bbf0a678dd63b39a6ad42f486287ecd9` |
| `placebo_results.json` | `bb36402d56e9747a1eb3902ec4130399a1488c3908040e9525812ed9a17b7447` |
| `artifact_manifest.json` | `67c842ef05640183be07885096af4d1e9f875d1c21aae0aa3782353ea1998b52` |

Run declarations: `actual_candidate_trials=1`; `K_reconstruction=2`.

---

## §8 — Prior-look and criterion-move audit

Prior looks remained exactly those disclosed before freeze:

1. P2 locked replay (2026-07-03/06): DJ30↔MYM divergence/E1 evidence; no locked-transfer claim reopened.
2. R5 mapped MYM edition (2026-07-09): prior mapped profitability/preservation evidence; mapped settings excluded.
3. Class-S candidate #1 (2026-07-15/16): firm-geometry evidence only; no alpha transfer.
4. Candidate #1 cheap falsifier and aborted runner (2026-07-16): feasibility/timestamp evidence; no valid candidate return series.
5. Timestamp-only 53-session calendar census (2026-07-16): no P&L.
6. This candidate #2 development run: the first valid `S-MYM-ORC-02` economic read, development dates only.

**Criterion-move audit:** no §2 semantic, D0–D9 threshold, cost assumption, placebo definition, date window, calendar mapping, or verdict branch moved after the operator signature. The run used cumulative `K_reconstruction=2`, one actual candidate trial, the frozen panel/calendar/runspec hashes, 10,000 placebo assignments, and seed 42.

**Holdout audit:** no reserved-holdout P&L was read or computed. H0–H9 remain unrun and are now terminally blocked by the development falsification.

---

## §9 — Disposition

`S-MYM-ORC-02` and `Q-STRIKER-MYM-RECON-2` close `FALSIFIED` on 2026-07-16. The reconstruction program has no active pre-registered candidate after this closure.

Any next reconstruction candidate is a new trial with a new ID, incremented candidate bank, fresh operator authorization, and a fresh signed pre-registration. Nothing in this closure authorizes such a candidate.

---

## §10 — Audit hooks

```bash
# Reproduce the recorded gate vector and headline values from development only
python -c "import json; p='lab/analysis/striker/striker_mym_reconstruction_candidate1_2026-07/development_metrics.json'; x=json.load(open(p)); assert x['gates']['verdict']=='FALSIFIED'; assert [x['gates'][f'D{i}'] for i in range(10)] == [True,True,False,False,False,False,False,False,False,True]; assert x['metrics']['trade_count']==403"

# Verify all registered artifact hashes without opening holdout data
python -c "import hashlib,json,pathlib; d=pathlib.Path('lab/analysis/striker/striker_mym_reconstruction_candidate1_2026-07'); m=json.loads((d/'artifact_manifest.json').read_text()); assert all(hashlib.sha256((d/n).read_bytes()).hexdigest()==h for group in ('artifacts','config','scripts') for n,h in m[group].items())"

# Confirm the Pre-Q points to this terminal closure
grep -n "CLOSED-FALSIFIED\|candidate-2-falsified" \
  docs/briefs/Q-STRIKER-MYM-RECON-2-session-aware-continuation.md

# Confirm forbidden downstream stages remain absent
test ! -e lab/analysis/striker/striker_mym_reconstruction_candidate1_2026-07/HOLDOUT_RESULTS.md
test ! -e lab/analysis/striker/striker_mym_reconstruction_candidate1_2026-07/parity_report.md
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python scripts/check_brief.py \
  docs/briefs/closures/2026-07-16-striker-mym-reconstruction-candidate-2-falsified.md --type inquire

PYTHONIOENCODING=utf-8 python scripts/check_brief.py \
  docs/briefs/Q-STRIKER-MYM-RECON-2-session-aware-continuation.md --type inquire

git diff --check
```
