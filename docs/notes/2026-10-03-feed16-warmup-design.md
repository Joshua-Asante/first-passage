# FEED-16: adapter warm-up from provider history, with a live-only fallback

**Status:** PROPOSED design, returned to coordinator (3) for acceptance, 2026-10-03. Provider-neutral preparation under the 2026-10-02 CP-7 grant ([checklist CP-7](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md) `:500`). It dispatches no implementation, binds no spec item and edits no owner.
**Ruling served:** operator, 2026-10-02 (sitting 2), FEED-16: warm-up comes from provider history (Q11); the history-to-live seam is checked in the shadow window; live-only is the fallback. The design is due before shadow collection, with a hard stop at T16. The ruling's record at checklist T14 Checkpoint (`:286`) travels in coordinator (2)'s batch PR and is not on `main` yet.
**Owners (Rule 7):**
- the [frozen equivalence spec](../spec/2026-09-27-cme-execution-feed-equivalence-test-DRAFT.md) (`721be61`) for the verdict;
- the [OPEN-binding packet](2026-10-02-feed-spec-open-parameter-binding-packet.md) (#617) for OPEN-3, OPEN-6, OPEN-7 and OPEN-11;
- the [H8 note](2026-09-27-feed-provider-neutral-preparation.md) for the later-binding rule (§3) and the shadow topology (§4);
- A9-PREP ([#619](https://github.com/Joshua-Asante/first-passage/pull/619), head `77373bd`, open) for the live `BarSource` contract;
- the [umbrella](../briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md) TB-S3 (H) (`:563`) and TB-W1 for restart and warm-up depth.

**Citation keys.** `path:line` is `origin/main` at `1a350ec`. "Spec" is the frozen spec; "packet" is #617's note; "contract" is `ops/c1_signal_daemon/bar_source_contract.py` at #619 `77373bd`; "inventory" is the private TB-W1 inventory `ops/c1_signal_daemon/ports/TB-W1_warmup_inventory_2026-09-12.md` (primary checkout, ignored root).

## 1. The problem

- **The runtime has no warm-up path.** `FourLegRuntime` halts on any bar outside the bound session (`book_runtime.py:350–:353`). Without retained history, the first bar must be the session open, and "only the session's first bar may seed their state" (`:369–:373`). Today the adapters therefore start each session cold.
- **The adapters were qualified warm.** Parity was proven from the panel origin, where the ports and the TradingView backtest start cold together ([scaling read §4](2026-09-12-track-b-scaling-faithfulness-read.md) `:120–:140`). A cold adapter at a live session open does not have that state.
- **The live contract cannot carry history.** `ContractBarSource` forwards only bars inside the M5 deadline, and it latches `REFUSED` on any bar at or before the last forwarded `ts` outside its one-day memory (`late_bar_unverifiable`, contract `:21–:24`, `:338`). History therefore needs its own path into the adapters, never through the live source.
- **Umbrella (H) already sets the shape:** state is "rebuilt by deterministic replay of the bar history from its TB-W1 warm-up boundary … before any emission resumes" (`:563`). FEED-16 decides where those bars come from.

## 2. Depth: what each leg's adapter needs

Depth is stated as behavior. The per-leg numbers are the inventory's (private); test W-1 (§6) confirms or extends them. No value appears here.

| State class (from the ports' structure) | What warm-up needs | Legs |
|---|---|---|
| Windowed indicator (fixed window over bars) | The longest window, in bars. State is exact after it | 6J, MYM |
| Recursive indicator (EMA/RMA family; `pine_ta.py:8–:9`: EMA seeded with the first value, RMA with the SMA of the first `length`) | Never exact. The seed's weight decays as (1 − α)^D, so the depth is the point where decisions stop depending on the seed (W-1) | 6J, MYM, MGC |
| Session-count history (ORB's opening-range volume history; public at `8c15f18:docs/notes/2026-09-26-orb-lifecycle-evidence.md:22`) | A count of prior sessions, each with a completed opening range. A short or empty history changes the volume filter's decision | MNQ |
| Per-day state (trade-per-day latches, day P&L, halt flags) | None. It resets at the trading-day roll, before the session's first bar | all four |
| Account state (equity, day-start equity, realised P&L) | Not from bars. It comes from the checkpoint or account path (inventory note; TB-S3 (H)), outside FEED-16 | 6J, MYM, MGC |
| Position state | None. Every leg is flat at each session end (umbrella `:520` (G)), so warm-up runs with no fills | all four |

**Depth per leg** `D_leg` = the inventory's recommended hold for that leg, as confirmed by W-1. The **fetch depth** is `D_leg` 15-minute bars counted back from the session open over the product's trading frame, plus whole sessions to cover holidays and early closes. It is not counted in calendar time.

**What the warm set contains.** Every trade-evidenced 15-minute bar in the product's electronic frame (Sunday–Friday 18:00–17:00 ET, daily break excluded), **including sessions the book's account calendar DENIES**. The canonical panel the adapters were qualified on carries those bars, and the runtime's bound-session filter does not apply to warm-up. Expected absences are taken from the ratified product-hours and holiday-halt rows ([Step 4](2026-09-15-packet1-step4-session-calendar.md) `:35–:39`), not from the account calendar.

**Rolls.** A warm span that crosses a canonical switch is stitched by the same per-leg contract-selection object that the feed and TB-V1 consume (packet OPEN-3 and OPEN-11): before the switch, the old dated contract; after it, the new one; no back-adjustment (spec §4.5). A provider's own continuous symbol is never used (spec R-MAP-2).

## 3. Primary path: provider history

1. **Port.** A separate `HistoryTransport` port, provider-specific (later-binding item B, §7): `fetch(binding, start, end) -> Sequence[DeliveredBar]`, reusing the contract's `DeliveredBar`, `SymbolBinding` and `bar_open_utc` (`:164`) so that timestamps are translated by the same B.5 rule as live.
2. **Admission.** A `WarmSetBuilder` admits history under the rules in §4, per leg. Its output is the **warm set**: per leg, the ordered bars from the warm boundary up to the last frame slot before the session open, with its SHA-256.
3. **Cutoff.** The fetch runs in the gap before the session open. On weekdays that gap is the 17:00–18:00 ET break, and the prior session's final bar closes at 17:00 ET. The warm set must be complete by a frozen cutoff before 18:00 ET; otherwise §5 applies to that session.
4. **Durability before use.** The warm-set digest and its per-leg spans are written to the account owner's durable record **before** the session's first bar is accepted. A restart rebuilds the adapters from the same warm set (digest-checked) and then replays the retained barriers (`book_runtime.py:508–:539`). A digest mismatch halts. Rebuilding per session keeps warm-up deterministic and leaves checkpointing to TB-S3 (H).
5. **Isolation.** Warm-up calls each adapter's `on_bar` with execution feedback off. Every intent it returns is discarded. It writes no barrier, partial or action record, constructs no `ListenerClient`, and does not relax the runtime's first-bar rule: the first live bar is still the session open (`:369–:373`).
6. **No verdict role.** History bars never enter arm L (spec §13: no "substituting backfill or historical bars for live-delivered bytes"), and they are not in the equivalence verdict (packet OPEN-7, recommended descriptive, `:243`). Arm H stays the optional descriptive arm (spec `:86`). FEED-16 depth `D_leg` does **not** satisfy OPEN-7's verdict constraint, which needs Side-A bars back to the TB-W1 replay boundary, the panel origin (packet `:240`). FEED-16 therefore leaves the OPEN-7 recommendation unchanged.

## 4. When history is unacceptable

Each rule applies to one leg's warm set for one session. Any failure fails the warm-up for the **book** for that session, matching the book-level halt (spec §8), and §5 applies.

| # | Condition | Treatment | Basis |
|---|---|---|---|
| U1 | **Revision.** A history bar for `(leg, ts)` differs, in any of `ts`, O, H, L, C or V, from the bar that was live-delivered and retained for that slot; or two history fetches of one slot differ | **Latch.** The history source is `REFUSED` for the rest of the session. No retry and no fallback history | Operator ruling A9-PREP Q1, 2026-10-02 (coordinator (3) sheet 2, item 3; recorded at #619 fold `05db835`): a revision of an already-forwarded bar latches `REFUSED`. Spec M7 counts "a backfill differing from the live delivery" (`:135`) |
| U2 | **Gap.** A slot inside the product frame and outside a calendar halt has no bar | Incomplete warm set. No interpolation and no carry-forward | Spec §4.3(a)–(b) (ADOPTED, `:304`); H8(b) Q-1: missing required input halts, and no bars are invented |
| U3 | **Not trade evidence.** Zero volume, or marked synthetic, filled-forward or no-trade | Scored as absent, then U2 | Spec §4.3(c) |
| U4 | **Wrong contract.** An unmapped or expired code, a contract other than the selection object assigns, a provider continuous symbol, or back-adjusted history | Refused | Spec R-MAP-2, §4.5; contract `SymbolBinding` |
| U5 | **Time.** A naive or DST-ambiguous stamp, a stamp convention the B.5 rule cannot translate, a bar off the 15-minute grid, or a bar in the daily break | Refused | Spec §4.1, §7 DST row; contract `:13–:14` |
| U6 | **Incomplete bar.** A bar not marked final, or one whose interval has not closed at fetch time | Refused | Contract: completed bars only |
| U7 | **Depth or timing.** The provider's history depth (Q11) is less than the fetch depth, or the warm set is not complete by the cutoff | That session falls back (§5); not a latch | Q11 ([#583](https://github.com/Joshua-Asante/first-passage/pull/583) note `:117`, head `e732fb9`) |
| U8 | **Duplicates.** An identical repeat of one slot | Kept once and counted | Spec §7 duplicate row |

U1 compares against the durable retained record (the owner's retained barriers, or the collector store in the shadow window), not the contract's one-day memory.

## 5. Fallback: live-only warm-up, emission disabled

- **Trigger.** Q11 shows no usable history; the history path fails its §6 shadow-window criteria; or U1–U7 fail at a session.
- **Method.** A record-only collector (H8 §4, Stage S-1: no listener client, no B1 builder) keeps the live-delivered bars for all four legs across sessions, including account-DENIED sessions. The warm set is built from those retained live bars by the same `WarmSetBuilder`; only its source changes. Because those bars were delivered live, there is no history-to-live seam.
- **Hold.** No session runs with emission until every leg's retained span reaches `D_leg` with no U2/U3 gap. A gap restarts that leg's span after it, because state built across a missing bar differs from the canonical state. Emission stays disabled through the hold under the existing layers (H8 §4: no sender, `effective_emit` False, `dry_run=true`, no arm). The hold's start, the gap restarts and its release are recorded.
- **Cheapest route.** If the shadow collector keeps running from the window to T16 without a gap, its store is already the warm set, so no extra collection is needed.
- **Risk.** A leg with frequent thin-slot gaps may never complete the span. The shadow window measures that rate (S-4). If the span cannot complete before T16, the result is a blocker for the owner. It is not absorbed.

## 6. Acceptance tests

**Offline, before any provider data** (canonical panels; private run on the primary checkout; digests and pass/fail only are recorded).
- **W-1 Depth sufficiency.** For each leg and each sampled session start `s`: run A is the adapter from the panel origin with the emulator (the qualified run). Run B is a cold adapter warmed on the panel from `s − D_leg` to `s` through the production warm path (no fills), with account-state fields copied from A at `s`. Both then run session `s` with the emulator. PASS: identical intents in every sampled session. The sample is fixed before the run and covers Mondays, post-holiday sessions, post-switch sessions and early-close sessions. On a FAIL, `D_leg` is extended and the extension is recorded privately. Run B with `D_leg` = 0 also shows what a cold start costs.
- **W-2 Roll stitch.** With a fake history transport serving dated contracts, a warm span across a canonical switch reproduces the stitched series under the selection object, and history from the other contract is refused (U4).

**Unit tests, public** (`tests/ops/`, fake transports, no private inputs).
- **W-3 Admission:** one case per row U2–U6 and U8.
- **W-4 Seam latch:** a history bar that differs from a retained live bar in exactly one field, one case per field including volume, latches `REFUSED`; the session opens in hold; no intent leaves the loop.
- **W-5 Cutoff:** a warm set incomplete at the cutoff makes the session hold; the warm set's last bar is the last frame slot before the open.
- **W-6 Isolation:** warm-up writes no barrier or action record and constructs no listener client; a first live bar other than the session open still halts with `bar-sequence`.
- **W-7 Durability:** the warm-set digest is recorded before the first bar; a restart rebuilds identical adapter state and replays the retained barriers; a mismatched digest halts.
- **W-8 Fallback hold:** emission stays held until every leg spans `D_leg`; a gap restarts that leg's span; the release is recorded.

**Shadow window** (post-CP-7, emission disabled; the collector runs the production warm path at every session start and labels history responses separately from live bytes, spec §12 item 4).
- **S-1 History equals live:** 0 differences on every field, every leg and every slot delivered live in the window (U1).
- **S-2 Timing:** the warm set is complete by the cutoff at every session start in the window. The worst case is recorded.
- **S-3 Seam decisions:** adapters warmed from provider history and adapters warmed from the fresh canonical capture (spec §3 arm L Side B) emit identical intents through each session in the window, in the H8 §4 Stage S-2 replay. This is descriptive for the spec verdict, but it gates the history path. Canonical volume instability (Step 3 `:31–:35`) makes a single ORB difference possible; it is reported, and the path fails unless the difference traces to the canonical side.
- **S-4 Depth and gaps:** Q11 depth is at least the fetch depth on every leg. The U2/U3 rate is recorded and feeds the fallback risk (§5).

**Path selection.** The history path is selected only if W-1–W-8 and S-1–S-4 all pass for the exact source-identity configuration. Otherwise the live-only path governs. If the history path is not selected by T16, the live-only path governs; no waiver.

## 7. Freeze placement (for T10 phase 2)

Warm-up decides what the adapters see, so it is freeze-affecting (checklist §5, `:506`; H8 §3 D, first bullet). Proposed for the F1 packet's later-binding rule:
- **A.6 (frozen at F1):** this warm-up rule, meaning both paths, the warm-set content and stitching, U1–U8, the hold, `D_leg` by reference to the inventory digest, and the path-selection criteria.
- **B.8 (after F1, under C):** the history endpoint, pacing and `HistoryTransport` module; and the path selection made by the frozen criteria.

A change to any A.6 item after CP-6 voids the freeze inventory for the feed component, as for A.1–A.5.

## 8. Open for the coordinator

1. **Inventory digest.** The inventory's SHA-256 should be pinned in the coordinator record before W-1 runs. A digest in a public record is acceptable; its values stay private.
2. **Account-state source.** Copying account state from run A in W-1 assumes that TB-S3 (H) supplies account state at the session start. TB-I3 owns that.
3. **U1 scope.** Can a U1 latch on history also latch the live source of the same provider? The Q1 ruling covers forwarded live bars only. This note latches the history source only.
4. **Cutoff value.** It is a frozen field, set from the S-2 measurement before CP-6 and never after data, or it is fixed now with a margin. The coordinator chooses which.

## 9. Verification

- Worktree `claude/feed16-warmup-note` from `origin/main` `1a350ec`.
- Read: spec (all); packet (all); H8 note §3–§5; `book_runtime.py:1–:120`, `:330–:420`; `book_protocol.py:1–:80`; `pine_ta.py` (structure); contract at `77373bd` (`:1–:140` and admission names); #619 body and fold comment; #583 note at `e732fb9` (Q11 and the eligibility screen); umbrella `:225`, `:514`, `:563`; scaling read `:120–:145`; checklist `:280–:289`, `:303–:314`, `:499–:506`.
- Private reads, in place on the primary checkout under AGENTS.md's private read surface: the four accepted ports and the inventory, for state structure only. Nothing was copied, and no value or body text is reproduced here.
- No provider was contacted, and no data was fetched.
