# Vanguard MGC trailing determination: bounded local handoff

**Status:** RETURNED — coordinator acceptance pending (§5). The source inspection has completed; the original bounded instructions below remain its scope record. Source verification, if needed for acceptance, follows §60 in the primary checkout. This return does not approve an edition or qualify the route.

**Selected outcome:** One source-bound answer to a single question. **Does Vanguard MGC's accepted effective binding make its bracket set trailing parameters?** The answer is `TRAILING ACTIVE`, `TRAILING INACTIVE` or `UNDETERMINED` with the exact missing input. This is the first-named next action of the [REST assessment §6.10](2026-09-25-crosstrade-rest-route-assessment.md#610-next-action-one-prerequisites-and-blockers), and it resolves or confirms [§6.7 (1)](2026-09-25-crosstrade-rest-route-assessment.md#67-corrections-to-prior-reasoning).

**Why it matters:**
- Campaign §59 Ruling 3 says no leg depends on L2(g) (triggered trailing) and records Vanguard as attested to fit the narrowed shape. That attestation covered only "a fixed stop in the same order" and one-contract expressibility.
- The [09-25 route note](../../notes/2026-09-25-tradingview-signal-route-evaluation.md) (line 243) records from a private read that "current effective defaults enable trailing".
- If trailing is active, Vanguard depends on a primitive the route does not support, and the operator must decide between a route-native fixed-stop edition and rejecting the leg.

**Authority:** read-only source inspection under [campaign §60](../programs/2026-09-03-seven-strategy-select-campaign-state.md#60--agent-read-access-to-the-accepted-books-pine-and-runtime-ports-2026-09-25) (AGENTS.md §Public-clone posture, private read surface). No modification, execution or import of private strategies. No parameter change, edition design, account access, drill or spend. Contract and expression decisions stay with the operator. The coordinator accepts the return.

**Return boundary:** fill in §5 and stop. Do not edit §59, the incident ADR, the REST assessment or the checklist; list the propagation targets instead.

## 1. Pinned identities to verify first

Verify every file against these pins before reading it for the determination. The canonical registry is `ops/c1_signal_daemon/book_adapters.py`, with `AdapterSpec("vanguard_mgc", …)` at lines 51–55.

| Item | Expected SHA-256 | Source of pin |
|---|---|---|
| Vanguard Pine `Vanguard_Gold_MGC_v0.4_venue_bound.pine` | `af26899ca94bb0e9ee26d09e0176b6b94bba2f5da252399ce4d899fe7e3bad15` | `book_adapters.py` |
| Vanguard runtime port `vanguard_mgc.py` | `e6a03d04c65a19e7fde71103560a229630c3663f445676f06622feec4e9157a3` | `book_adapters.py`; `qualification/contract.py:41` |
| Historical `effective_inputs.json` (source bytes) | `66406dee955fa69f237fde60eacdd24259a08d5320352d98e59889acaa18158d` | `EFFECTIVE_INPUTS_SHA256` |
| Runtime effective values (canonical digest, derived) | `9d4d4e1d622a3fb0ae37b7b20f8bdf960244f9e66b5d88ded79db4de6089dade` | `RUNTIME_EFFECTIVE_INPUTS_SHA256` |

Read the Pine source and runtime port at the paths `core/strategies/BOOK_SOURCES.sha256` pins: `core/strategies/book/Vanguard_Gold_MGC_v0.4_venue_bound.pine` and `ops/c1_signal_daemon/ports/vanguard_mgc.py`. `effective_inputs.json` sits beside the port (see [T10 source reconciliation](../../notes/2026-09-21-t10-phase1-source-reconciliation.md) line 162). Read all of these **in place in the operator's primary checkout**, as [campaign §60](../programs/2026-09-03-seven-strategy-select-campaign-state.md#60--agent-read-access-to-the-accepted-books-pine-and-runtime-ports-2026-09-25) requires. A worktree session uses that checkout's absolute path. If any file hashes to something else, do not use it; report the mismatch.

The runtime digest is computed over canonical effective values after derivation, not over file bytes. Recompute it with the registry's own loader or digest function, invoked through the launcher, and never by hand. If you can't reproduce it without importing or executing a private port, record `not reproduced` and rely on the historical source-byte pin.

## 2. Steps

- [ ] **Environment.** Run `.\fp.ps1 doctor` from the operator checkout. Record the revision and working-tree state.
- [ ] **Hash.** Hash the four items in §1 (`Get-FileHash -Algorithm SHA256`). All must match before continuing.
- [ ] **Port path.** In `vanguard_mgc.py`, find where brackets are constructed (the port's bracket-construction helper and its callers). Identify which inputs set the public `Bracket` trailing fields (`ops/c1_signal_daemon/book_protocol.py:71-72`), and the enabling condition, such as a boolean input or a non-zero distance. Check whether that condition is ever satisfied under the effective configuration.
- [ ] **Effective binding.** Read the effective values for those inputs from the pinned `effective_inputs.json`, applying any runtime derivation the registry performs. A source default counts only if the effective file leaves it unset and the loader falls back to it. State which of these applies.
- [ ] **Pine cross-check.** In the pinned Pine source, find the corresponding trailing inputs and whether its exit orders pass TradingView's documented trailing arguments. Confirm that the port and Pine agree on whether trailing is live under the same effective inputs. A disagreement is itself the finding: report it and do not pick a side.
- [ ] **Other inputs.** Note in one line each whether breakeven and the grace stop are active. The route note says both are inactive; this confirms or corrects that.
- [ ] **Stop.** Do not design an edition, estimate performance effects or open K.

## 3. Evidence rules

- Cite `file:line` and the pinned hash for each claim. Do not copy source bodies, parameter values or tables into tracked files. A tracked statement may say an input is enabled or disabled, but must not give a numeric distance.
- Do not copy the private files or extracts of them anywhere: no scratch directory, worktree or external service (§60). Record only `file:line` citations and hashes.
- "The input exists in source" is not evidence that the branch is active (route note line 202).

## 4. Decision the return feeds

- **`TRAILING ACTIVE`.** The §59 Ruling 3 premise is false for Vanguard. The operator decides between a route-native fixed-stop Vanguard edition under the §59 K = 1 pattern and rejecting the leg on this route. Propagation targets: campaign §59, incident ADR §A4, CAP R3 row, REST assessment §6.7 (1).
- **`TRAILING INACTIVE`.** The §59 premise holds, the route note line 243 is corrected, and the REST verdict's first driver drops. Option B and the L2(c)/(d) drills remain.
- **`UNDETERMINED`.** Name the exact missing file, hash or derivation.

## 5. Executor return

**Status:** returned 2026-09-25 (local session, operator machine).

| Field | Value |
|---|---|
| Executor / dispatch revision | Claude Code (Opus), local; packet read at `6875616` |
| Checkout revision and tree state | Primary checkout `1c5c082`; `.\fp.ps1 doctor` passed (ops-env, Python 3.13.2, 62 locked packages matched). Tree dirty: 1 modified and 4 untracked tracked-path docs (T08 handoff, REST assessment, CAP deletion map, assurance review, route note); none is a pinned file. |
| Hash results (4 rows, match/mismatch) | Pine `af26899c…` **match**. Port `e6a03d04…` **match** (runtime path and the corrected-ports copy). `effective_inputs.json` `66406dee…` **match** (both locations). Runtime digest: see next row. |
| Runtime digest reproduced? | **Yes**, `9d4d4e1d…`. Recomputed through `.\fp.ps1 python` with the registry's own derivation (`book_adapters.py:150-167`: ORB `qty` from `c1_rail.book_policy.leg`, canonical JSON). No private port was imported or executed. |
| Port evidence (`file:line`) | The port's bracket construction (`vanguard_mgc.py:175-181`) sets both trailing fields when its trailing switch is enabled, and leaves them unset otherwise. It is used for entry (`:253`), scale-in (`:269`) and every managed-bar amend (`:274`). In the source defaults (`:69-71`) the switch is enabled and the trailing distances are non-zero, so every bracket carries trailing parameters. |
| Effective-binding evidence | The pinned effective-inputs row for Vanguard supplies **no overrides**. The public loader passes that row to the port's `build` (`book_adapters.py:175`), which constructs its parameters only from those overrides (`vanguard_mgc.py:291-292`). The effective binding is therefore the port's source defaults: trailing **enabled**. This comes from loader fallback, not from an explicit effective setting. |
| Pine cross-check (`file:line`, agree/disagree) | **Agree.** Under its defaults, the Pine enables trailing with non-zero distances (`.pine:235-238`). Every exit order it places carries trailing arguments gated on that switch: at entry, including the grace branch (`:452-461`), and in per-bar management (`:499-503`). The port reproduces the same behavior. |
| Breakeven / grace (one line each) | **Breakeven: inactive** by default in both port (`:66`) and Pine (`.pine:228`), with no override. **Grace: inactive.** The port's default activates the stop at entry (`:60`, `:245`), so its grace level (`:177`) is never used. Pine agrees (`.pine:169-171`, `:497`). |
| **Verdict** | **`TRAILING ACTIVE`.** Under the accepted effective binding, every Vanguard bracket (entry, scale-in and each amend) carries triggered-trail parameters. The route note line 243 claim is **confirmed**. |
| Propagation targets (not applied) | Campaign §59 Ruling 3 (the Vanguard "fits the narrowed shape" attestation fails, because Vanguard depends on L2(g)); incident ADR §A4; CAP R3 row; REST assessment §6.7 (1) (confirmed, not corrected). The operator decision is §4 `TRAILING ACTIVE`: a route-native fixed-stop Vanguard edition (§59 K = 1 pattern) or rejecting the leg on this route. |

No scratch extracts were written, and no source bodies or numeric parameter values appear above.

**Coordinator disposition (DRAFT, 2026-09-26; not yet recorded as accepted):** recommend **ACCEPT WITH CAVEATS**. Verdict `TRAILING ACTIVE`.

*Checked from the public clone (cloud review):*
- **Loader path.** `load_book_adapters` (`ops/c1_signal_daemon/book_adapters.py:146-179`) does four things in order. It verifies the source bytes against `EFFECTIVE_INPUTS_SHA256`. It derives runtime values by changing **only** ORB's `qty` (`:159-161`). It verifies the derived bytes against `RUNTIME_EFFECTIVE_INPUTS_SHA256`. It then calls `module.build(mode=mode, **row["adapter"])` (`:175`).
- **Empty adapter means port defaults.** Vanguard's runtime row is therefore its source row, and an empty `adapter` object means `build` receives no overrides. The return's "loader fallback to port defaults" reading matches the code.
- **Trail fields must be set by the port.** `Bracket`'s trail fields default to `None` (`ops/c1_signal_daemon/book_protocol.py:71-72`), so trailing exists only if the port sets them. That is consistent with the return's bracket-construction citation.
- **Digest reproduction.** Reproducing `9d4d4e1d…` binds the inspected effective values to the registry's accepted identity. It was done through the launcher's derivation, without importing the port.
- **Pins.** The input pins cited in the return match `core/strategies/BOOK_SOURCES.sha256` (Vanguard Pine `af26899c…`, port `e6a03d04…`) and `book_adapters.py:51-55`.
- **Public-clone posture.** The return contains `file:line` references and shapes only. No source bodies or values.

*Not checked here (caveats):*
1. The private `file:line` citations in the port (`:60`, `:66`, `:69-71`, `:175-181`, `:245`, `:253`, `:269`, `:274`, `:291-292`) and in the Pine (`:169-171`, `:228`, `:235-238`, `:452-461`, `:497-503`) were not re-read. The cloud clone has no private sources. **Acceptance condition:** one §60-compliant spot-read in the primary checkout of the port's bracket construction, its three call sites and the trailing-switch default. Alternatively, the coordinator records that it relies on the executor's hashes and citations.
2. **Accepted binding assumed to be the runtime loader.** The verdict holds for the binding that the runtime loader (and the registry's accepted identity) uses. It assumes the qualification path (Phase 1 accepted run, E1) binds through the same loader and inputs. That is consistent with `RUNTIME_EFFECTIVE_INPUTS_SHA256` being the accepted identity, but it was not traced through `ops/c1_rail/qualification/` in this review.
3. **Trailing is enabled by default, not by an explicit input.** The effective file never states it. This is correct as a finding. It also means a future non-empty Vanguard override could change the answer, so any successor effective-inputs digest reopens it.
4. **Breakeven and grace inactive.** Accepted on the same basis. It confirms the route note and does not change any §59 premise.

*Effect if accepted:*
- Campaign §59 Ruling 1's Vanguard attestation ("fits the narrowed shape") is **superseded for trailing**. Vanguard depends on L2(g), which is U on this route.
- REST assessment §6.7 (1) is **confirmed** (not corrected).
- The first driver of the portfolio-route verdict stands.
- **Next decision is the operator's:** the fixed-stop edition ([pre-registration](../pre-registration/2026-09-26-tradeify-vanguard-fixed-stop-edition-prereg.md)) or rejecting the leg on this route.
- **Propagation still owed, not applied by this draft:** campaign §59 (record the acceptance and supersession), incident ADR §A4, the CAP R3 row, and the STATE index row when the operator decides.

*Recording:* the coordinator replaces "(DRAFT …)" with an accepted/rejected line, the date, and whether caveat 1 was discharged by a spot-read or by reliance.
