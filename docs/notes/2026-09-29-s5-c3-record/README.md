# S5 Checkpoint C3 record: coordinator evidence (2026-09-29)

This holds the durable copies of C3 step 1 evidence that the coordinator produced outside the S5 build branch. The ruling and the verdicts live in the [execution-slices ledger](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-rulings-and-recorded-harness-read--s5-c3-step-1-2026-09-29); this folder holds only the evidence.

## Executed `bind_budget` Σ-feasibility check on the built `/v7` (RC-3b)

- `bind_budget_check.py.txt` is the check script, SHA-256 of the committed (LF) bytes `10f0b3dcc15c888e702022acac487b811beb62c11074975ecadbdc19a2c8d358`; the Windows working copy that ran was CRLF, SHA-256 `af4a69ba0d9ca0714f9dae9ab0fca60d508096f44debcdf8367ac7f862dcbd1d`. It runs the real `CampaignStore.bind_budget` in a temporary directory with the built `/v7` campaign budget profile, derived from `deploy/qualification/test-profile.json` as the installation derives it, and the `/v7` fixture-producer binding. A negative control repeats the bind with the unextended binding.
- `bind_budget_check.out.json.txt` is its output, SHA-256 of the committed (LF) bytes `4852a116e1281d2ee0469f0b754b42bb0c887be8b8eb532d0d75f6ed288d2f73`; as written on Windows (CRLF) `1abfd438b2c56bdfc11d827f418eaadf7ba3ae2e7ff3b3a4709558c00a217470`.
- **Run:** 2026-09-29 through `python -I scripts/fp.py python <script>` (ops-env CPython 3.13.2). It ran from a detached worktree at the S5 head `d4afa5b`; the pushed return head `c7713e7` differs from it only in docstrings and the §7 text.

**Result:**

| Quantity | Built `/v7` | Binding | Result |
|---|---|---|---|
| Σ phase CPU | 1,680 s | 10,000 s | fits |
| Σ phase wall | 4,200 s | 10,000 s | fits |
| Max phase memory | 256,000,000 B | 256,000,000 B | fits, **zero headroom** |

- The campaign state after binding is `BOUND`.
- The control (120 s / 180 s / 230,400,000 B) is `BUDGET_EXHAUSTED`, as predicted.
- These values match the pre-build arithmetic in the PART_A application entry exactly.
- The two gaps named in r2 §10.2 still stand: Σ counts one reservation per phase, and no code checks the wall slack between works.
