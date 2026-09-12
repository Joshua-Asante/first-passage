# Tradeify portfolio — coordinator dispatch 1 (pre-A7 preparation, 2026-09-12)

**Status:** dispatch record · authorizes nothing · the umbrella's return vocabulary applies.
**Scope executed:** read-only investigation, source inventory by digest, reconciliation, behaviour
decisions against existing authority, TB-R2 draft menu + TB-W1, TB-T1 contract and packet, progress
records. **Not executed (by dispatch boundary):** any trading-behaviour change, qualification sample,
deployment, provider selection, host write, A7. A7 remains the attended session on Sunday
2026-09-13 (18:00 ET / 17:00 CT reopening).

**Alias.** The operator calls the accepted Aegis 6J · Vanguard MGC · Striker MYM · ORB MNQ
configuration, with its protection/capacity rules, the **Tradeify portfolio**; recorded with the
[acceptance record](2026-09-10-tradeify-protection-selection.md#alias--the-tradeify-portfolio-recorded-2026-09-12).
Owners: [Track B umbrella](../briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md)
(packets, §0.8 open items) · [campaign record §55](../briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md#55--track-b-release--d-b1d-b15-recorded-2026-09-11)
(rulings) · [adapters and book rules](2026-09-11-track-b-adapters-and-book-rules.md) (#356 evidence).
This record is a derived mirror of those owners plus this dispatch's own findings.

## 1 — Verified state (handoff-verify PASS)

| Item | Verified |
|---|---|
| `origin/main` | `c41e2befc2afc93b6c695477bf092f00458f5a57` (merge of #357); coordinator worktree `claude/tradeify-pre-a7-prep-1bf254` at the same SHA, clean |
| PRs | #356 **MERGED** 2026-09-12 17:57Z at `73acb5e9786498eda672fbe695b1940fbb75a534`; #357 **MERGED** 18:14Z at `c41e2be…`; both merge commits are ancestors of `main`; no open PRs; no `tb-` remote branches |
| Primary checkout | `main` at `133f043`, **10 commits behind** `origin/main` (contains neither merge); untracked `ops/c1_signal_daemon/ports/` (ignored contents) and `tmp/`; left untouched (other sessions' state) |
| Other worktrees | eleven, none on a Track B branch; none modified |
| Private inputs (by digest, primary checkout / Downloads) | four pinned Pine bodies **found in Downloads** (equal to `phase1_config.json` `pine_sha256`; none under `core/strategies/`) · four captured exports in Downloads equal to `export_sha256` · four panels verify against `core/data/bar_data/SHA256SUMS` (the file is CRLF; strip before `sha256sum -c`) · four ports + `effective_inputs.json` equal to the digests in the 09-11 note |
| LOST (unchanged from umbrella §0 / D-B3) | D26 override files (`460f40fa…`, `b7369ee3…`, `3bacd6f1…`, `102635ac…`); `local_artifacts/` ledgers; the synthetic implementation, composition receipt, feasibility-screen outputs and weighting study (not re-searched this dispatch) |
| Tests re-run (fable-judge posture) | `tests/ops/test_book_policy.py`, `test_book_review_followups.py`, `test_tv_broker_emulator.py`, `test_book_adapters_parity.py` with `FP_PORT_ROOT` / `FP_BAR_DATA_DIR` / `FP_TV_EXPORT_DIR` at the private inputs: **85 passed, 0 skipped** — the four exact-parity claims of #356 reproduce on this machine |
| Extra verification | Aegis port at a fixed 8 reproduces all **121/121** captured entry/exit bars and prices; 62 trades sized up from the captured ladder; no emulator rejections |
| STATE currency | `check_state_currency.py` OK as of 2026-09-12 (the 09-11 R-2 hook failure is cleared by the 09-18 deadline) |
| TB-W1 private inventory | `ops/c1_signal_daemon/ports/TB-W1_warmup_inventory_2026-09-12.md` (ignored root), SHA-256 `9f9e59fdcd959236cec95ea0affb9307206bf345f860ad68eb126b67db7f0866` |

## 2 — Reconciled completion matrix

| Obligation | Implementation / evidence | Remaining gap | Owner | Entry gate | Status |
|---|---|---|---|---|---|
| TB-R1 2.1 locate Pine + overrides by digest | Pine ×4 in Downloads; overrides LOST; reconstructed effective inputs pinned | override provenance (O-9) | coordinator | — | DONE-WITH-CONCERNS |
| TB-R1 2.2 regenerate ledgers | not run: `verify_input_overrides` refuses without the D26 files | O-9 ruling | operator → coordinator | O-9 | NEEDS_CONTEXT |
| TB-R1 2.3 panels | four panels verify | none | — | — | DONE |
| TB-R1 2.4 / 2.5 lost-set inventory, backup list | not run this dispatch | run before wave 2 | coordinator | — | OPEN |
| TB-R2 scaling read + export menu | [note](2026-09-12-track-b-scaling-faithfulness-read.md): classification RESOLVED; menu DRAFT (7 owed exports) | menu freeze | coordinator | O-5, O-6, O-7 | DRAFT LANDED |
| TB-W1 warm-up | private inventory; boundary = panel origin; no pre-window bars owed | freeze in TB-S3/TB-F1 | coordinator | — | LANDED |
| TB-S1 protection/capacity spec | rules (A)–(F) exist as **code** in `book_policy.py` (candidate policy, ULP trigger, prior-close clock, integer table, carried positions, ledger + atomic takeover) with 21 failing-first tests | the spec file; the O-5/O-6 law; the fixed-quantity leg type for the host | Claude | O-5, O-6 | NOT AUTHORED (blocked on rulings) |
| TB-S2 replay spec | emulator = per-leg TV-faithful replay broker (fill semantics 1–8 pinned); **not** the synchronized multi-leg replay | spec incl. C1–C5 re-derivation, calendar/overlay, missing-bar rule, week clock | Claude | TB-R1 inventory (partial) | NOT AUTHORED (authorable now) |
| TB-S3 rail/daemon extension spec | protocol (C)/(D)/(M) delivered as `book_protocol.py`; capacity/takeover (E) in `book_policy.py`; O-3 seeding unspecified | registry, barrier, sides, kill switch, scheduler, restart, packaging, policy source, live/offline split | Claude | O-8 (holiday latch), O-3 | NOT AUTHORED (authorable now; O-8 assumed "keep") |
| TB-P1 validation-contract draft + ORB ADR skeleton | not started; `certification_power.py` has no speed-limb mode | both files + additive calculator mode | Claude | — | NOT AUTHORED (authorable now) |
| TB-P2 fixed-instance ADR | not started | full-tier ADR, PROPOSED → operator ratification before TB-F1 | Claude | D-B11 ruled | NOT AUTHORED (authorable now) |
| TB-A1..A4 adapters + parity | **DELIVERED-IN-PART (#356):** ports, captured-size parity PASS 681/203/338/121, protected-size / adds-off behaviour under port semantics | parity against TB-R3-intaken exports at every protected/WATCH size and mode | Claude | OP-1 + TB-R3 | OWED-IN-PART |
| TB-A0 port manifest | `PORT_MANIFEST.sha256` carries no book line | after all TB-A parity | coordinator | TB-A parity PASS at every size | STUB |
| OP-1 exports | menu drafted: Striker ×5 (Account Size ×0.40/0.50/0.20/0.25/0.10), ORB ×2 (1 contract, margin 0 %, adds on/off); Aegis and Vanguard none | operator supplies | operator | menu freeze | QUEUED |
| TB-R3 intake | not started | intake dir + manifests | Claude | OP-1 delivered | STUB |
| TB-I1 locked surfaces | untouched (`firm_rules`, `lifecycle`, sizing host) | thread the ruled law; fixed-quantity leg type; keys/allocations at zero | Claude | TB-S1 accepted + ratified | STUB |
| TB-I2 replay engine (Codex) | none | engine + matrix | Codex | TB-S2 accepted; parity PASS at every exercised size; TB-R1 panels | **BLOCKED** |
| TB-I3 rail/daemon offline (Codex) | none | offline requirements | Codex | TB-S3 accepted + TB-I1 merged | **BLOCKED** |
| TB-T1 snapshot sealer (Codex) | [contract](../spec/2026-09-12-tradeify-account-snapshot-seal-contract.md) + [packet](../briefs/handoffs/2026-09-12-tb-t1-snapshot-sealer-packet.md) | build | Codex | contract fixed | **READY (not launched)** |
| TB-C1 forward calendar | none | needs TB-P1 horizon | Claude | TB-P1 | STUB |
| O-1 Call-4 beta term | host lacks it; `lifecycle.get_effective_multipliers` has it | ruling | operator → TB-S1 | — | recommendation below |
| O-2 initial lifecycle state | none | TB-V1 migration | operator/coordinator | wave 3 | open |
| O-3 live peak seeding | none | TB-S3 requirement + test | Claude | TB-S3 | open |
| O-4 production feed | deferred by operator | — | operator | later | DEFERRED |

Distinctions kept: original-export parity ≠ protected/lifecycle/adds-off export parity;
source-faithful mode tests ≠ TradingView exports and intake; reconstructed effective inputs ≠
recovered D26 overrides; candidate policy code ≠ admitted `POLICY_REGISTRY` row (still empty) ≠
deployment approval. #356's review-loop closure stands: its R-1/R-2 open items carry to TB-I2 and
the STATE row (R-2 is cleared).

## 3 — Behaviour questions: what existing authority settles, what remains

| # | Observed behaviour (anchors) | Existing authority | Parity evidence required | Remaining decision |
|---|---|---|---|---|
| 1 | **Aegis effective inputs and captured-vs-fixed sizing.** Export reproduces exactly only under a reconstructed input set differing from the pinned body's defaults; the capture used an equity ladder capped at 8 (59/121 at cap); the rail expresses a fixed 8 (TB-S1 (F)), so 62 trades size larger. Verified: timing and prices are size-invariant (fixed 8 and fixed 3 reproduce the captured bars/prices). | Selection note "captured 8-full-contract setting"; TB-S1 (C)/(F) fixed integer; D-B10 → 3 under protection | none beyond the captured export (size-invariant); the fixed-quantity rule is tested against it | **O-9** (provenance of the reconstructed inputs); no behaviour decision — the fixed-8/3 rule is ruled. Design consequence: the host needs a fixed-quantity leg type (TB-S1/TB-I1) |
| 2 | **ORB margin-throttled adds and adds-off exits.** Capture at 2 contracts with TradingView's default margin: adds mostly absent after 2023-05 (affordability); the rail has no margin branch; adds-off removes the stall exit and changes average-price exits (verified, `test_orb_adds_off_…`). | Selection note: one micro, ≤2 adds, adds off while protected; TB-R2 (B) mode dependence | two new exports at one contract with margin 0 % (adds on / off), intaken by TB-R3 | **O-7** (attest the margin-0 % chart state for the new exports). Also record: ORB places nothing at WATCH-1/2 (base floors to 0) |
| 3 | **Vanguard post-holiday session.** No trade on the session after a US market holiday: the EOD flat latch resets on TradingView's daily bar, which a holiday lacks; the port reproduces it (`tv_daily_key`). | captured-ledger behaviour; no ruling names it | captured export (PASS 338/338) already covers it | **O-8**: keep as captured (recommended) or treat as a strategy change (pre-registration; out of this attempt) |
| 4 | **Striker account-state halts and add-tier rounding.** Day soft-stop on the leg's realised P&L and the daily/total DD kill on the leg's own paper equity were live in the capture (backtest mode OFF); at 40 % size the halts move. Adds: TradingView and the host size the add from the executed base; `book_policy` floors each tier from its own normal (22/55 → 8/22 vs 8/20). | D-B10 floor; TB-S1 (C) "every add tier"; host law `floor(executed_base × pyr%)` | per-size exports (only expressible under the risk-scaled law) | **O-5** (sizing law) and **O-6** (add law) |
| 5 | **O-1 portfolio-wide lifecycle reduction.** `core/lifecycle.get_effective_multipliers` applies 0.50× to every leg when ≥3 of 4 are de-authorized; the sizing host applies only the per-leg tier. | Call-4 ratified (operator GO/NO-GO on the shutdown); D-B14 (a) retains the ladder | none if handled off-rail; two more quantities per size-dependent leg (0.125×, 0.05×) if on-rail | **O-1**: recommendation — handle **off-rail**: a beta-death event is an operator kill-switch / GO-NO-GO trigger (TB-S3 (F)), never a rail multiplier, so the reachable set stays `{1, 0.5, 0.25} × {1, 0.40}` |

## 4 — Operator decisions still needed (one consolidated list)

Recorded as umbrella §0.8 rows; recommendations are the coordinator's, not rulings.

| Id | Decision | Recommendation | Consequence of the recommendation |
|---|---|---|---|
| O-1 | Call-4 beta term on-rail or off-rail | off-rail (kill switch / GO-NO-GO) | finite reachable set; no extra exports; TB-S1 states it |
| O-5 | sizing law for ladder legs: quantity-floor (A, as built) vs risk-scaled (B, host law, TV-expressible) | **B for Striker MYM; A for Vanguard MGC** (Vanguard WATCH tiers restricted to zero) | Striker protected/WATCH sizes differ from the as-built table on roughly one entry in ten and at the cap (22 not 8); five Striker exports become possible and required; `book_policy` gains a per-leg law flag (TB-I1); Vanguard keeps the accepted zero-under-protection |
| O-6 | add law: floor(scale × normal add) vs floor(executed base × pyramid %) | **executed-base law** (host + TradingView) | Striker add at the protected cap 20 not 22; adds always from confirmed base (already the host doctrine) |
| O-7 | ORB new exports at margin 0 % (chart-state deviation from the capture) | yes | O-N and O-P exports become the fixed book's ORB oracles; the captured 2-contract export remains the Pine-faithful oracle only |
| O-8 | Vanguard post-holiday no-trade artefact | keep as captured | live adapter keeps the TV daily-key latch; no pre-registration needed |
| O-9 | effective-input provenance | re-capture the five Inputs tabs (§47a) if the charts exist, else accept the reconstructed set as RECONSTRUCTED with per-export Inputs/Properties captures for every OP-1 export | TB-R1 2.2 can run (a) or is recorded LOST-with-reconstruction (b); no manifest rewrite either way |

Until O-5/O-6/O-7 are ruled the export menu stays DRAFT and TB-S1 is not authored; O-8 and O-9
do not block TB-S2/TB-S3/TB-P1/TB-P2 authoring.

## 5 — Export menu

Drafted in the [TB-R2 read §3](2026-09-12-track-b-scaling-faithfulness-read.md): 4 available
(the captured exports), **7 owed** under the recommended rulings (Striker ×5 by scaling the Account
Size input; ORB ×2 at one contract with margin 0 %, scale-in on/off), Aegis and Vanguard none.
Freeze blocked by O-5 (Striker rows exist only under law B), O-6, O-7. TB-R3's intake gate stays in
front of every new export before it is decision-bearing.

## 6 — Packet dispositions (Claude / Codex split)

| Packet | Lane | Disposition | Why |
|---|---|---|---|
| TB-T1 snapshot sealer | Codex | **READY** — [packet](../briefs/handoffs/2026-09-12-tb-t1-snapshot-sealer-packet.md) | field/evidence contract fixed by the [seal contract](../spec/2026-09-12-tradeify-account-snapshot-seal-contract.md); the live capture stays a later gate |
| TB-I3 offline rail/daemon | Codex | **BLOCKED — context-problem** | TB-S3 not authored/accepted; TB-I1 not started |
| TB-I2 synchronized replay | Codex | **BLOCKED — context-problem** | TB-S2 not authored/accepted; OP-1 exports and per-size parity not delivered |
| TB-S2, TB-S3, TB-P1, TB-P2 | Claude | **authorable now** (TB-S3 under the O-8 "keep" assumption; O-3 folded in) | entry conditions met by the rulings D-B1..D-B15 |
| TB-S1 | Claude | **BLOCKED — context-problem** | O-5 / O-6 rulings fix its quantity tables |
| TB-R3, TB-A parity at new sizes, TB-A0 | Claude | BLOCKED on OP-1 | menu freeze → exports → intake |

## 7 — Next executable actions

- **Operator:** rule O-1, O-5, O-6, O-7, O-8, O-9 (one comment suffices; "defaults" applies the recommendations); merge this dispatch's PR; then produce the OP-1 exports from the frozen menu with an Inputs-tab and Properties-tab capture per export; run A7 on Sunday in its own session.
- **Claude (coordinator):** after the rulings, re-issue the TB-R2 menu as FROZEN (replacement, not extension) and author TB-S1; independently now: author TB-S2, TB-S3, TB-P2 and TB-P1 (with the additive speed-limb mode in `certification_power.py`); run TB-R1 2.4/2.5; adjudicate TB-T1 on return.
- **Codex:** execute TB-T1 when the operator launches it (branch `codex/tb-t1-snapshot-sealer`; two files; acceptance = the packet's §4 gate); review this dispatch's PR.

Checks run for this record: `make check`, `python scripts/check_md_relative_links.py --strict` on the
new and edited files, `python scripts/check_brief.py <TB-T1 packet> --type cc_handoff`,
`python scripts/check_state_currency.py`; results in the PR body.

## 8 — Boundaries respected

No host read or write, no deploy, arm, enable, inject, order or retry; no edit to `core/`, `ops/`,
Pine, ports, exports, panels, `DD_TRIGGER` / `DD_SCALE`, `POLICY_REGISTRY` or any manifest; no
qualification run; no provider action; no fifth strategy, sweep, runner-up or substitute book.
Private outputs: the TB-W1 inventory only, on the primary checkout's ignored port root. No account
value, Pine body or parameter value beyond the already-public ones appears in this dispatch.
