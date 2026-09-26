# Vanguard MGC trailing determination: bounded local handoff

**Status:** DRAFT for a local session on the operator's machine. This work cannot run in a cloud clone, because the private port, the Pine source and `effective_inputs.json` are gitignored and exist only locally. Commit this packet before dispatch and record the dispatch revision in §5.

**Selected outcome:** One source-bound answer to a single question. **Does Vanguard MGC's accepted effective binding make its bracket set trailing parameters?** The answer is `TRAILING ACTIVE`, `TRAILING INACTIVE` or `UNDETERMINED` with the exact missing input. This is the first-named next action of the [REST assessment §6.10](2026-09-25-crosstrade-rest-route-assessment.md#610-next-action-one-prerequisites-and-blockers), and it resolves or confirms [§6.7 (1)](2026-09-25-crosstrade-rest-route-assessment.md#67-corrections-to-prior-reasoning).

**Why it matters:**
- Campaign §59 Ruling 3 says no leg depends on L2(g) (triggered trailing) and records Vanguard as attested to fit the narrowed shape. That attestation covered only "a fixed stop in the same order" and one-contract expressibility.
- The [09-25 route note](../../notes/2026-09-25-tradingview-signal-route-evaluation.md) (line 243) records from a private read that "current effective defaults enable trailing".
- If trailing is active, Vanguard depends on a primitive the route does not support, and the operator must decide between a route-native fixed-stop edition and rejecting the leg.

**Authority:** read-only source inspection under [AGENTS.md §Private strategy source access](../../../AGENTS.md#private-strategy-source-access). No modification, execution or import of private strategies. No parameter change, edition design, account access, drill or spend. Contract and expression decisions stay with the operator. The coordinator accepts the return.

**Return boundary:** fill in §5 and stop. Do not edit §59, the incident ADR, the REST assessment or the checklist; list the propagation targets instead.

## 1. Pinned identities to verify first

Verify every file against these pins before reading it for the determination. The canonical registry is `ops/c1_signal_daemon/book_adapters.py`, with `AdapterSpec("vanguard_mgc", …)` at lines 51–55.

| Item | Expected SHA-256 | Source of pin |
|---|---|---|
| Vanguard Pine `Vanguard_Gold_MGC_v0.4_venue_bound.pine` | `af26899ca94bb0e9ee26d09e0176b6b94bba2f5da252399ce4d899fe7e3bad15` | `book_adapters.py` |
| Vanguard runtime port `vanguard_mgc.py` | `e6a03d04c65a19e7fde71103560a229630c3663f445676f06622feec4e9157a3` | `book_adapters.py`; `qualification/contract.py:41` |
| Historical `effective_inputs.json` (source bytes) | `66406dee955fa69f237fde60eacdd24259a08d5320352d98e59889acaa18158d` | `EFFECTIVE_INPUTS_SHA256` |
| Runtime effective values (canonical digest, derived) | `9d4d4e1d622a3fb0ae37b7b20f8bdf960244f9e66b5d88ded79db4de6089dade` | `RUNTIME_EFFECTIVE_INPUTS_SHA256` |

Expected locations are `ops/c1_signal_daemon/ports/vanguard_mgc.py` and `ops/c1_signal_daemon/ports/effective_inputs.json` in the operator checkout. See [T10 source reconciliation](../../notes/2026-09-21-t10-phase1-source-reconciliation.md) line 162. The corrected-ports tree under `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/inputs/private_overrides/op1/2026-09-14-seven/step3-coverage/corrected-ports/` also holds a copy. If any file hashes to something else, do not use it; report the mismatch.

The runtime digest is computed over canonical effective values after derivation, not over file bytes. Recompute it with the registry's own loader or digest function, invoked through the launcher, and never by hand. If you can't reproduce it without importing or executing a private port, record `not reproduced` and rely on the historical source-byte pin.

## 2. Steps

- [ ] **Environment.** Run `.\fp.ps1 doctor` from the operator checkout. Record the revision and working-tree state.
- [ ] **Hash.** Hash the four items in §1 (`Get-FileHash -Algorithm SHA256`). All must match before continuing.
- [ ] **Port path.** In `vanguard_mgc.py`, find where brackets are constructed (the `_bracket` helper and its callers in `on_bar` and `on_execution`). Identify which inputs set `trail_activation_ticks` and `trail_offset_ticks` on `Bracket` (`ops/c1_signal_daemon/book_protocol.py`), and the enabling condition, such as a boolean input or a non-zero distance. Check whether that condition is ever satisfied under the effective configuration.
- [ ] **Effective binding.** Read the effective values for those inputs from the pinned `effective_inputs.json`, applying any runtime derivation the registry performs. A source default counts only if the effective file leaves it unset and the loader falls back to it. State which of these applies.
- [ ] **Pine cross-check.** In the pinned Pine source, find the corresponding trailing inputs and the `strategy.exit` trail arguments (`trail_points`/`trail_price`/`trail_offset`). Confirm that the port and Pine agree on whether trailing is live under the same effective inputs. A disagreement is itself the finding: report it and do not pick a side.
- [ ] **Other inputs.** Note in one line each whether breakeven and the grace stop are active. The route note says both are inactive; this confirms or corrects that.
- [ ] **Stop.** Do not design an edition, estimate performance effects or open K.

## 3. Evidence rules

- Cite `file:line` and the pinned hash for each claim. Do not copy source bodies, parameter values or tables into tracked files. A tracked statement may say an input is enabled or disabled, but must not give a numeric distance.
- Put any scratch notes or extracts under an ignored path (confirm with `git check-ignore`) and list only their hashes in §5.
- "The input exists in source" is not evidence that the branch is active (route note line 202).

## 4. Decision the return feeds

- **`TRAILING ACTIVE`.** The §59 Ruling 3 premise is false for Vanguard. The operator decides between a route-native fixed-stop Vanguard edition under the §59 K = 1 pattern and rejecting the leg on this route. Propagation targets: campaign §59, incident ADR §A4, CAP R3 row, REST assessment §6.7 (1).
- **`TRAILING INACTIVE`.** The §59 premise holds, the route note line 243 is corrected, and the REST verdict's first driver drops. Option B and the L2(c)/(d) drills remain.
- **`UNDETERMINED`.** Name the exact missing file, hash or derivation.

## 5. Executor return

**Status:** not dispatched.

| Field | Value |
|---|---|
| Executor / dispatch revision | |
| Checkout revision and tree state | |
| Hash results (4 rows, match/mismatch) | |
| Runtime digest reproduced? | |
| Port evidence (`file:line`) | |
| Effective-binding evidence | |
| Pine cross-check (`file:line`, agree/disagree) | |
| Breakeven / grace (one line each) | |
| **Verdict** | |
| Propagation targets (not applied) | |

**Coordinator disposition:** pending.
