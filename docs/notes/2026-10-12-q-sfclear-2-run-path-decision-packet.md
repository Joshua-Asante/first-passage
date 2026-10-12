# Q-SFCLEAR-2 run path: decision packet for Joshua

**Date:** 2026-10-12 · **Base:** `origin/main` `92bfca7` · **Prepared by:** drafting worker for the Deployment Coordinator, to relay. **Status:** items 1–7 RULED (2026-10-12).

**Sources:** the [scope note](2026-10-12-q-sfclear-2-run-path-code-scope.md) (#795); the FROZEN [Q-SFCLEAR-2 pre-registration at F `83867f0`](https://github.com/Joshua-Asante/first-passage/blob/83867f0d362931c2a516a62b990bb1c209372527/docs/briefs/pre-registration/Q-SFCLEAR-2-verdict-preregistration.md); the DRAFT cards [A](../briefs/handoffs/2026-10-12-q-sfclear-2-run-path-a-p0-instance-card-DRAFT.md), [B](../briefs/handoffs/2026-10-12-q-sfclear-2-run-path-b-personal-replay-card-DRAFT.md), [C](../briefs/handoffs/2026-10-12-q-sfclear-2-run-path-c-tradovate-costs-card-DRAFT.md), [D](../briefs/handoffs/2026-10-12-q-sfclear-2-run-path-d-fg-parity-card-DRAFT.md), [E](../briefs/handoffs/2026-10-12-q-sfclear-2-run-path-e-run-record-card-DRAFT.md). No private value was read.

Bound notation: **T** = trust-domain code inventory (`ops/c1_rail/qualification/trust_domain.py:140`, `:156`); **F** = TB-I1 fingerprint component (`ops/c1_rail/policy_fingerprint.py:29`); **D8** = the [C′ card](../briefs/handoffs/2026-10-02-h9-cprime-runtime-identity-build-DRAFT.md)'s P7 closure list ("none may change").

## At a glance

| # | Decision | Recommendation | Ruling |
|---|---|---|---|
| 1 | Code admissions per card | Admit A and B as bounded below; C and E need none; D is test-only; the owner seam stays with P4 | RULED: admitted as listed |
| 2 | P0 halt boundary in replay | Replay mirrors the live halt code; the §4 scorer keeps its exact hit | RULED: mirror |
| 3 | Where Tradovate fee parsing lives | Lab-side serialized consumer (option b) | RULED: (b) |
| 4 | Aegis route | PR for all legs | RULED: PR |
| 5 | Sequencing and executor per card | A0 (coordinator) → A → C → B → D → E; Codex local per card; no card enters the owner queue | RULED: as proposed |
| 6 | Whether D's FG evidence run may use the Azure VM | Yes, if you extend the §60 VM exception to this run | RULED: (b), §60 extended to the FG run |
| 7 | What a P0 latch inside the historical replay means | (b), the frozen reading: you confirm it; (a) is a stricter rule you may add | RULED: (b) |

## 1. Code admissions

**What you decide:** which bound files each card may edit. Admitting a file moves its identity even where the changed function is not called.

| Card | File | Bound | Note |
|---|---|---|---|
| A (step A0, coordinator) | `core/firm_rules.py` (`Personal_Tradovate.micro_contract_cap` → 80) | T, F, D8 | A `core/` anchor-path edit: coordinator only (routing test 1), not Codex |
| A | `ops/c1_rail/book_policy.py` | T, F, D8 | Named P0 policy type; `account_micro_cap(tier)`; Tradeify unchanged |
| A | `ops/c1_rail/book_capacity.py` | T, F | Resolved cap |
| A | `ops/c1_rail/qualification/replay.py` | T, D8 | P0 mode source and halt observation |
| A | `ops/c1_rail/personal_drawdown_halt.py` | becomes T when imported | Extract one pure breach function; live behaviour unchanged |
| A, B (conditional) | `ops/c1_rail/qualification/trust_domain.py` | T, D8 | One inventory entry each for a newly imported module |
| B | `ops/c1_rail/qualification/production_source.py` | T, D8 | Personal factory (`:1367`) and resolved cap (`:190`) |
| B | `ops/c1_rail/qualification/replay.py` | T, D8 | G4 enforcement and per-trade route output |
| B | `ops/c1_rail/qualification/personal_replay.py` (new) | enters T | Verified input envelope and route output |
| D | `tests/ops/test_personal_replay_live_parity.py` | none | Test only |
| E | `lab/analysis/c1/sfclear_2026-10/run_record.py`, `score_r1.py` (new) | none, after import audit | Lab only |
| P4 (not these cards) | `ops/c1_rail/book_sizing_context.py`, `ops/c1_rail/book_account_owner.py` | T (+F for sizing) | The live P0 consumer stays with P4 |

**Recommendation:** admit A and B as listed, including the conditional rows, with one admission covering both (as J-2 covered P-L1 and P-L2).

**RULED 2026-10-12:** Joshua, 2026-10-12, directly to the Deployment Coordinator, verbatim: "item 1 admitted as listed" (scope confirmed: card A §2.3 files including A0 `core/firm_rules.py` and the conditional rows; card B §2.2 files including new `qualification/personal_replay.py`; accepting that the Tradeify TB-I1 fingerprint and trust-domain digests move, D8 paths change and H′ moves, with P7 re-measured on the new bytes if P7 D8 is still owed; `book_sizing_context`/`book_account_owner` excluded, with P4).

**What it changes:** A moves the **Tradeify** instance's TB-I1 fingerprint, because it edits `REQUIRED_COMPONENTS` files (`firm_rules`, `book_policy`, `book_capacity` are shared components). A and B both move trust-domain digests and touch D8 paths. B edits no `REQUIRED_COMPONENTS` file, so B alone does not move the TB-I1 fingerprint. If the P7 D8 obligation is still open, admitting them also accepts that H′ moves and that P7 evidence must be re-measured on the new bytes. Refusing keeps the Tradeify identities fixed and leaves the study unrunnable (pre-registration §11 items 1 and 10).

## 2. P0 halt boundary in the replay

**Fact:** the live halt rounds the drawdown to six places before comparing (`ops/c1_rail/personal_drawdown_halt.py:171`), so it can latch fractionally before 15%. The study scorer tests the exact integer `20·(peak − trough) ≥ 3·peak` (`lab/discovery/sfgrowth_acceptance.py:270`).

| Option | Replay halt uses | Effect |
|---|---|---|
| (a) mirror live | The live predicate, imported as one pure function | Replay models the account as the rail will run it; one small extraction in `personal_drawdown_halt.py` |
| (b) exact | The scorer's exact integer predicate, reimplemented in ops | No halt-file edit; replay and live can disagree at the boundary |

**Recommendation:** (a). The replay models live. The §4 scorer keeps its own exact hit definition, which is a separate frozen contract.

**RULED 2026-10-12:** Joshua, 2026-10-12, directly to the Deployment Coordinator, verbatim: "2 mirror, 3 b, 4 PR, 5 as proposed, 6 b (extend §60 to the FG run), 7 b". Item 2: mirror (option (a)).

**What it changes:** under (a), A edits `personal_drawdown_halt.py` and the replay imports it (closure change, item 1). Under (b), neither happens, and A's row P2 asserts the exact predicate.

## 3. Where Tradovate fee parsing lives

| Option | Placement | Effect |
|---|---|---|
| (a) | A separate closed ops parser, `qualification/personal_cost_terms.py` | Bound code; needs admission; wiring into the production source is B's edit |
| (b) | Lab-only scoring input, `lab/discovery/sfclear_tradovate_fees.py` | Unbound; feeds `daily_series` per instrument |
| (c) | Not offered: `firm_rules.Personal_Tradovate.cost_per_side_usd` | One undated scalar; cannot hold a dated per-instrument snapshot |

**Recommendation:** (b). The replay does not need the Tradovate fees: reference friction stays in replay for guard and ladder behaviour (pre-registration §4 item 2), and the fees are deducted only in scoring.

**RULED 2026-10-12:** Joshua, 2026-10-12, directly to the Deployment Coordinator, verbatim: "2 mirror, 3 b, 4 PR, 5 as proposed, 6 b (extend §60 to the FG run), 7 b". Item 3: (b), lab-side.

**What it changes:** (b) keeps C out of the trust domain and out of `production_source.py`. (a) adds a bound file and couples C to B.

## 4. Aegis route

**Options:** PR for all legs; or RS for Aegis, admissible only if every D9 condition (C-mode, C-life, C-cap, C-sched) and FG-T (fixed-quantity timing identity with scaled Commission) is proved (pre-registration §7).

**Recommendation:** PR for all legs, unless the D9 conditions plus FG-T are cheap to prove.

**RULED 2026-10-12:** Joshua, 2026-10-12, directly to the Deployment Coordinator, verbatim: "2 mirror, 3 b, 4 PR, 5 as proposed, 6 b (extend §60 to the FG run), 7 b". Item 4: PR for all legs; RS is not used.

**What it changes:** PR adds no route code and drops FG-T from D's evidence run. RS adds refusing condition checks to B and an FG-T anchor to D. If Aegis falls back to PR, all legs run in one PR (§7).

## 5. Sequencing and executor per card

**Proposed order:** A0 (coordinator commit) → A → C → B → D → E.
- `production_source.py` has one writer across A, B and C: **B's writer**. A does not edit it; C does not edit it under either option.
- `replay.py`: A then B, serial.
- `book_account_owner.py` keeps GC-5-DISPLACED → TB-I3 S2 → P-L2 → P4. None of A–E edits it. D needs P-L2 and P-L3 merged; D's P0-latch row waits for P4.
- B and E need #752's frozen `lab/analysis/c1/sfclear_2026-10/` files on main.

**Executor:** Codex local for A, B, C, D (Part 1) and E, each the single writer of `codex/sfclear2-<letter>-<slug>` in a fresh worktree. Exceptions: A0 is the coordinator's (routing test 1); D Part 2 is a Claude-owned private executor act.

**Options:** the order above; or A/B after P4 so the live P0 consumer and the replay land together.

**Recommendation:** the order above. The study path does not need live P0 (FG item 3 names adds OFF and zero-quantity refusal).

**RULED 2026-10-12:** Joshua, 2026-10-12, directly to the Deployment Coordinator, verbatim: "2 mirror, 3 b, 4 PR, 5 as proposed, 6 b (extend §60 to the FG run), 7 b". Item 5: as proposed.

**What it changes:** the order sets when the Tradeify identities move (A, B) relative to TB-I3 S2 and P-L2 review, and when FG can run.

## 6. Whether D's FG evidence run may use the Azure VM

**Fact:** the VM is Joshua-controlled; laptop runs time out. The AGENTS.md "Private read surface" exception allows copying the runtime ports and `effective_inputs.json` (not Pine) to that VM **for the T00 screen** only (§60 addendum 2026-10-07).

**Options:** (a) laptop, in place; (b) the VM, under an extension of the §60 exception naming this FG run; (c) another host.

**Recommendation:** (b), if you extend the exception. (a) is the fallback with chunked runs.

**RULED 2026-10-12:** Joshua, 2026-10-12, directly to the Deployment Coordinator, verbatim: "2 mirror, 3 b, 4 PR, 5 as proposed, 6 b (extend §60 to the FG run), 7 b". Item 6: (b), the Azure VM, with §60 extended to the FG run (ports and `effective_inputs.json` only; Pine stays off the VM); the coordinator records the campaign §60 addendum 2026-10-12.

**What it changes:** (b) needs your words extending §60 to this run; Pine stays off the VM either way. (a) needs no new permission but risks timeouts.

## 7. What a P0 latch inside the historical replay means

**Fact:** the frozen pre-registration says what a Striker total-DD trip means (§4 item 8, NOT CLEARED) but names no consequence for a P0 latch inside the 2022-09-01..2026-09-02 replay. Three readings, set against the frozen §6, §7 and §12 step 6:

| Option | What it is | Against the frozen text | Needs |
|---|---|---|---|
| (b) | A latch refuses risk, so the following days come out of the replay as zero days; the §4 scorer scores the series as it stands | Arguably the frozen reading: §7 runs the replay "under P0", and P0 includes the live 15% halt (§2). No new rule | Joshua **confirms the reading** |
| (a) | A latch gives NOT CLEARED | Adds a verdict rule after the freeze: §6 lists RESOLVED's conditions exhaustively, and §12 step 6 says no constant moves after the freeze. Stricter only | A **dated operator ruling**, recorded in the brief (not the frozen files) before any run and disclosed in the closure as a post-freeze addition |
| (c) | A new pre-registration, Q-SFCLEAR-3, that defines the case | Leaves Q-SFCLEAR-2 as frozen; same tuple, K unchanged | A new ratification and freeze |

**Recommendation:** (b), the frozen reading, which Joshua confirms. (a) is a stricter option he may add on top.

**RULED 2026-10-12:** Joshua, 2026-10-12, directly to the Deployment Coordinator, verbatim: "2 mirror, 3 b, 4 PR, 5 as proposed, 6 b (extend §60 to the FG run), 7 b". Item 7: (b), the frozen reading; post-latch days are zero days produced by the replay, and no NOT CLEARED rule is added.

**Risk of (b):** if a latch fires, the post-latch tail is flat, so the bootstrap's 20-day blocks partly dilute the pre-latch drawdown.
**Risk of (a):** it adds a NOT CLEARED path after the freeze.

**What it changes:** under (b), A's mechanics produce the zero days and E adds no rule; the cards freeze as drafted. Under (a), E adds one row that maps a latch record to NOT CLEARED. Under (c), the cards wait for the new pre-registration and its freeze.
