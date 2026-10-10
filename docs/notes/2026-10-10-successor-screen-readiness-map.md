# Successor-screen readiness map

**Status:** DRAFT recommendations for Joshua. Read-only scoping, approved by Joshua 2026-10-10 for the Deployment Coordinator. Authorizes nothing: no build, signing, replay, screen or freeze.
**Question:** for each configuration the Tier-2 pattern could select, what must change before **one** successor screen can run under [#733](../briefs/pre-registration/2026-10-08-tradeify-book-successor-screen-prereg-DRAFT.md), and how long the critical path is.
**Read at `origin/main@85563a4`:** `screen_authority.py`, `contract.py`, `trust_domain.py`, `production_source.py`, `replay.py`, `book_policy.py`, `t00_screen/verdict.py`, `book_adapters.py` (constants only), `core/lifecycle.py`; the [T00 card](../briefs/handoffs/2026-10-03-t00-screen-authority-build-card-DRAFT.md) §2–§8, the [screen-authority design](../superpowers/specs/2026-10-02-t00-screen-authority-design.md) §1–§4.5, the [Tier-2 card](../briefs/handoffs/2026-10-08-t00-step12-diagnostic-tier2-scoping-card-DRAFT.md), #581, #733, the size-feasibility [RESULTS](../../lab/analysis/c1/size_feasibility_2026-10/RESULTS.md) and wrapper source, and `discovery_manifests/`. **Not read:** Pine, ports, `effective_inputs.json`, any Tier-1/Tier-2 report or output, the step-12 run directory, any private result. Nothing was run.

## 1. Facts that shape every row

1. **The current screen authority cannot run a successor.** Its compiled checks fix the object: `R3C_CONTRACT_SHA256` (`screen_authority.py:54`, checked `:316-317`, `:347`, `:610`), `expressions == 'DECLARED_BOOK'` (`:216`), `PREREG_CHAIN[-1]` (`:56`, `:411`), and #581's A5/A6 text hashes (`:450-452`, `verdict.py:26-27`). #581 line 84 forbids "re-optimization, re-sizing or substitution". The `PARAMETER_CHANGE` refusal therefore means "no re-sizing under this authority". Every successor type is outside it.
2. **De-risking is allowed, but only in a different door.** AGENTS.md allows pre-registered de-risking and forbids re-optimization. One size vector, fixed before any successor output, is de-risking. Sweeping and keeping the best is re-optimization. The successor needs its own purpose and grant. The refusal list can stay the same if `PARAMETER_CHANGE` is defined to mean "nothing beyond the frozen configuration".
3. **Size lives in `ops/c1_rail/book_policy.py`, not in Pine or `dd_protection`.** `entry_quantities` (`:279-315`) and `add_quantity` (`:255-276`) set every quantity. `replay.py:597-613` calls them and rejects a zero quantity cleanly ("zero policy quantity"). `dd_protection`/`BASE_RISK` are not on the screen path. The 1%/0.40 book protection is hard-checked (`require_policy`, `:99-115`) and stays unchanged.
4. **Integer floors.** Aegis has a fixed base of 8. Striker is risk-sized, with a 1..22 ladder. Vanguard's base of 1 or 2 comes from the port. ORB is fixed at 1 and never scaled (`:307-313`). **Uniform k = 0.5 cannot be expressed as stated:** ORB cannot be halved, and Vanguard's base 1 floors to 0. FEASIBLE was a fractional series rescale (`run_size_feasibility.py:165-168`, lab layer; `lab↔ops` imports are forbidden). It cannot feed the screen, and its label does not carry over to any integer vector.
5. **The configuration must be bound in a signed contract.** The r3c source contract pins the startup policy's bytes (`source_startup_policy` role), the effective-settings digest (compiled from `book_adapters.RUNTIME_EFFECTIVE_INPUTS_SHA256`, `trust_domain.py:420-426`), the port pins, and `orb_normal_base == 1` (`contract.py:1132-1142`). `parse_startup_policy` accepts `AUTHORIZED` only (`production_source.py:199`). A configuration placed only in code would leave r3c's bytes describing a different book. **Every type needs a successor contract (call it r3d), a fresh approval over it, and a P7 record over r3d.** The r3c approval's expiry (2026-10-17T00:45Z) is not on the successor path.
6. **The screen-authority build card forbids `book_policy.py`, `replay.py`, `contract.py`, `trust_domain.py` and `book_adapters.py`** (card §2.2). A successor build needs its own card.
7. **#733's current shape fails `_check_prereg`/`_check_sections`.** Those checks expect a Status of `RATIFIED <date>` (#733 says `FROZEN`), byte-identical `### A5`/`### A6` sections (#733 has §6 G1–G6), a `t00-step2-values/v1` block (#733 proposes `successor-screen-values/v1`), §3 item cells and §6 Ruling/OD fields. `verdict.evaluate` scores G1 and G3 only. G2/G4 (R1 alone, H2) need verdict code. G5 needs a funded-geometry producer that the runner lacks.
8. **Depth (corrects the brief).** The T00 card §8 records **N = 1,002 per population** (`depth_per_root` = 334; 3N = 3,006 paths; budget 961,920 CPU-s = 320 × 3,006). Joshua chose this on 2026-10-05, superseding the 2026-10-03 figure of 5,001. Step 12 ran 15:43:29Z → 00:04:25Z (about 8.35 h at `--workers 8`), which is about 80 CPU-s per path against the 320 CPU-s upper bound.

## 2. Common changes (every type)

| # | Change | File / artifact | Kind | New H | Signature |
|---|---|---|---|---|---|
| X1 | Successor purpose, grant and evidence class; `PARAMETER_CHANGE` defined | `screen_authority.py` | code | yes | — |
| X2 | Bind the authority to r3d, not the compiled r3c digest: per-chain-entry contract digest | `screen_authority.py` | code | yes | — |
| X3 | Append #733 to `PREREG_CHAIN`; a per-entry prereg profile (A5/A6 hashes, values-block name, Status word), or #733 rewritten to #581's form | `screen_authority.py`, `t00_screen/verdict.py`, #733 | code + doc | yes | — |
| X4 | Verdict: G2/G4 (R1 alone on H2) under #733's precedence rule; a successor `a5_rule` ID | `t00_screen/verdict.py` | code | yes | — |
| X5 | A sizing knob carried by the signed startup policy (schema v2: per-leg size and adds rule), read by `book_policy`/`replay`; default = today's behaviour | `book_policy.py`, `replay.py`, `production_source.py` (`parse_startup_policy`) | code | yes | — |
| X6 | New startup-policy bytes and review artifact; r3d = r3c with only that artifact (and `contract_id`) changed | private root | artifact | no | r3d source approval (Joshua) |
| X7 | P7 re-run at the new H under r3d; `accept-p7` | private root | run | at H | — |
| X8 | #733 frozen and ratified (C and C′), OWED fields set | #733 | doc | no | operator ratification |
| X9 | Screen authority over r3d and #733; window ≥ 72 h after the planned start | private root | signing | no | `APPROVE_T00_SCREEN_AUTHORITY` (Joshua) |

Synthetic tests only (red-first), plus the H check (qualification suite, parity, `fp check`). A3 answers carry over unchanged.

## 3. Per configuration type (beyond §2)

| Type (Tier-2 row) | Extra change | File | Kind | New H | Signature | Notes |
|---|---|---|---|---|---|---|
| **Uniform size cut at k** (row 5 uniform; FEASIBLE target) | Integer per-leg vector in X5 | as X5 | code + artifact | yes (X5) | r3d | Joshua picks the integer form (Q1). |
| **Per-leg cut of the risk-sized leg, cap with it** (row 1) | Striker risk multiplier and cap reserve in X5 | `book_policy.py` (`:302-303`) | code | yes | r3d | Expressible exactly. |
| **Adds/pyramid off** (row 2) | Per-leg adds rule (unchanged / off when protected / off) in X5 | `book_policy.py` (`add_quantity`) | code | yes | r3d | A zero add is rejected cleanly (`replay.py:612`). Striker adds are the only adds live in protected mode today. |
| **Leg dropped** (row 3) | Leg size 0 in X5; four legs stay in the contract | as X5 | code + artifact | yes | r3d | Signals are still generated and never admitted. Freed capacity changes other legs' admissions (intended). Removing a leg from the contract is a much larger change. |
| **Leg reshaped: size only** (row 3) | Per-leg size in X5 | as X5 | code | yes | r3d | Same as a per-leg cut. |
| **Leg reshaped: signal logic** (row 3) | New effective inputs or a new port/edition; `RUNTIME_EFFECTIVE_INPUTS_SHA256` or `ADAPTERS` pins; parity re-pin; `expressions` ≠ `DECLARED_BOOK` | `book_adapters.py`, private ports/inputs, `trust_domain.py` | code + private artifacts | yes | r3d + edition preregs | **OPEN:** needs private reads (which input, which port). Locked Pine/ports are immutable, so this means a new edition (ORB-3/VAN-3 precedent), not an edit. Weeks, not days. Risk of re-optimization. |
| **Early-phase per-session cut** (row 5 early) | A cushion-conditioned sizing state in replay | `replay.py`, `book_policy.py` | code (new risk-control rule) | yes | r3d | A second sizing tier beside the 1%/0.40 cell. The card's model note says the eval floor never locks, so on the eval an early-phase cut is in effect uniform (Q4). |

## 4. Critical path after the Tier-2 report (estimates)

| Step | Owner | Estimate | Parallel with |
|---|---|---|---|
| 1. Pattern → configuration; #733 OWED fields (C-1..C-7, K₀, readers, G4–G6, depth) | Joshua + coordinator | 0.5–1 d | — |
| 2. Successor build card; approval | coordinator, Joshua | 0.5 d | 4 |
| 3. **Build X1–X5 (red-first, Codex review, CI 22–32 min per push)** | fresh CC session | **3–5 d** | 4, 5 |
| 4. #733 freeze + ratify (X8) | Joshua | 0.5 d | 3 |
| 5. Startup policy v2 bytes, review, r3d assembly (X6) | coordinator | 0.5 d | 3 |
| 6. New H + H check (about 3 h of runs) + accept | coordinator, Joshua | 0.5 d | — |
| 7. r3d approval signed; P7 at H; `accept-p7` (about 1 h last time) | Joshua, coordinator | 0.25 d | — |
| 8. Screen authority signed (X9) | Joshua | 0.25 d | — |
| 9. Screen run at N = 1,002, W = 8, then `finalize` + `verify` | executor | **9–44 h** | — |

**Total: about 6–9 calendar days after the Tier-2 report. The long pole is step 3.** Run time: 8.35 h was measured on the declared book. A cut book busts and passes later, so its paths run longer; plan for the design's upper bound of about 43 h, which the signed budget formula covers. At N = 5,001 the run is about 5× (about 42 h to 7 d), which needs windows longer than 7 days. Signal reshape adds weeks.

## 5. Open design questions for Joshua (each with a recommendation)

| # | Question | Recommendation |
|---|---|---|
| Q1 | Integer form of "k = 0.5" | Aegis 8→4; Striker risk × 0.5 with cap reserve × 0.5; Vanguard and ORB each **either** kept at 1 **or** dropped, stated per leg. Disclose that the vector is not the fractional k that cleared, and that FEASIBLE does not transfer to it. |
| Q2 | Where the size vector lives | Startup policy v2 (signed via r3d), read by `book_policy`. Not the effective inputs (Pine-input values, private, parity re-pin). Not lifecycle tiers (`WATCH-1` = 0.5 exists, but it zeroes Vanguard and ORB and conflates decay state with configuration). |
| Q3 | Authority purpose and `PARAMETER_CHANGE` | New purpose `T00_SUCCESSOR_SCREEN`, grant `T00_SUCCESSOR_SCREEN_ONCE`; keep the refusal list; define `PARAMETER_CHANGE` as anything beyond the frozen #733 configuration, any locked Pine/port/input, and the protection cell. |
| Q4 | Row 5 early-phase vs uniform | Treat row 5 as uniform for the eval screen; defer early-phase to a funded-stage study. |
| Q5 | #733 form vs code | Generalize `_check_prereg` with a per-chain-entry profile (X3), rather than forcing #733 into #581's A5/A6 bytes, because G2/G4 change the gate text anyway. |
| Q6 | G5 funded survival | Reported, not binding: no funded-geometry producer exists, and building one plus the `preflight.py` engine check would become the long pole. |
| Q7 | Depth | N = 1,002 per population (as ratified for #581 and budgeted), with fresh RNG roots disjoint from step 12, Tier 1 and Tier 2. |
| Q8 | Signal reshape | Out of scope for this successor. If Tier 2 points only there, return to Joshua (#733 §1 rule). |

## 6. Prefill for #733 (DRAFT; Joshua decides)

**K₀.** `discovery_manifests/` has **no entry** for this book's lineage. That covers the selection (the 2026-09 book composition is "EXPLORATORY … no K ledger entry"), the step-12 screen and the size grid. Recommendation: K₀ = 8 = 1 (step-12 screen of the declared book) + 7 (size grid), **including** the grid's 7 once; this successor = K₀ + 1 = 9. Register the lineage in the ledger before freeze. The component strategies' own discovery K stays with their manifests and is not added.

**Reader-log rows** (in addition to T1-1..T1-5 and SF-1..SF-3, unchanged):

| # | Reader | Date | Saw | Source |
|---|---|---|---|---|
| RM-1 | Readiness-map session (this note) | 2026-10-10 | Public code and docs only; no report, series, keys or private result | this note |
| T2-1 | Tier-2 executor session | pending | Pending: sampled per-leg series and the report | Tier-2 card §7 |
| T2-2 | Deployment Coordinator | pending | Pending: public return; report if read | Tier-2 card §6–§7 |
| T2-3 | Joshua | pending | Pending: report or summary | Tier-2 card §7 |

## 7. Changes to the T00 tree

1. Depth is N = 1,002, not 5,001 (§1 item 8).
2. Step 3 needs a successor build (card, new H, r3d, P7, authority) **before** the screen. The tree's step 3 is not "run under the existing door".
3. The FEASIBLE k does not carry over to an executable vector (§1 item 4). The screen tests Joshua's integer vector, not k.
4. The r3c approval expiry is irrelevant to the successor; the r3d approval and the authority window size the run.
