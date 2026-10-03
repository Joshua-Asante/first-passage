# ED-10 — a §6 option (b) pricing algorithm for sequential one-contract splits (2026-10-02)

**Status:** DRAFT for the operator's §6 choice. This note specifies one concrete option (b). It selects nothing, amends neither successor pre-registration, and authorizes no code change, replay, E1 run or freeze. Ticket O (coordinator dispatch, 2026-10-02), deliverable ED-10. *Ruled 2026-10-02 (operator ruling 2026-10-02 (sitting 2)): option (b) as written in §2, δ = max(1, s), stress cells leave δ unchanged (B7's 'only if the battery owner says so' does not apply), the acknowledgement condition is acknowledgement (B3's resting-stop exception stands), and the same text goes in every edition file. The §6 paste text is adopted with its stress-cell sentence replaced by 'Stress cells leave δ unchanged.'*

**Serves:** the §6 item "Replay modelling of the split — OWED (operator and coordinator)" in the [ORB/Striker successor](../briefs/pre-registration/2026-10-02-tradeify-route-native-editions-successor-prereg.md#6--how-the-editions-requalify-and-what-counts-as-a-result) and the [Vanguard successor](../briefs/pre-registration/2026-10-02-tradeify-vanguard-fixed-stop-edition-successor-prereg.md#6--how-the-edition-requalifies-and-what-counts-as-a-result), and the same item in the [Aegis skeleton](../briefs/pre-registration/2026-10-02-tradeify-aegis-no-repin-edition-successor-prereg.md). Option (b) there requires "the per-request price and fill rule for request k of N, any delay model, and its frozen inputs", stated in the pre-registration in full. Naming I8 alone does not satisfy it.

**Reads (Rule 0, `origin/main@bd30646`):** `ops/c1_rail/qualification/replay.py`; `ops/c1_signal_daemon/tv_broker_emulator.py`; `ops/c1_signal_daemon/book_adapters.py`; `ops/c1_rail/qualification/production_source.py:1143-1150`; `ops/c1_rail/qualification/trust_domain.py:139-176`; [synchronized replay spec](../spec/2026-09-12-tradeify-synchronized-replay-spec.md) RC-4, RC-6, RC-9; [rail spec](../spec/2026-09-12-c1-multi-leg-rail-extension-spec.md) I8; [incident ADR §A8](../adr/2026-09-17-bounded-platform-protection-incident-contract.md#a8--revision-2026-09-25-proposed-the-whole-book-in-the-narrowed-shape) rules 9–10 and §A9.1 UB-4; [deployment checklist](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md) first-release item 7. No private Pine, port or effective-input file was read. Nothing was executed.

## 1. What the replay does today with an N-contract intent

- **Admission** sizes the whole intent once and reserves the whole quantity (`replay.py:408-423`, `:451-452`). This already matches Ruling 5's whole-intent reservation.
- **The emulator fills it as one fill of N contracts at one price** (`tv_broker_emulator.py:529-543`). The price is the base price moved by the leg's slippage ticks against the order side (`_slipped`, `:508-512`).
- **Base price by timing class:**
  - a `THIS_CLOSE` market order fills at the generating close (`:233-234`);
  - a `NEXT_OPEN` market order fills at the next open (`:351-357`);
  - a stop already crossed at registration fills at the close for `THIS_CLOSE` scripts (`:238-247`, `:175-183`), otherwise becomes a next-open market order (`:252`);
  - a resting stop fills at a gapped open (`:370-377`) or at its level on the bar path (`:435-439`).
- **One bracket covers the whole lot** (`:541-543`). A bracket exit fills at one price (`:558-585`), and a close or flatten fills every lot at one price (`:595-622`).

Today's replay is therefore option (a). Under proposed rule 10 (§A8), a split's next child is sent only after the previous one is acknowledged or refused, so "later contracts can fill at worse prices", and §6 must price that before freeze.

## 2. The algorithm

**Scope.** Every admitted `entry` or `add` intent with N ≥ 2, on any leg whose edition sends one-contract requests. Exits, brackets, closes and flattens are unchanged (§4).

**Frozen inputs.** No input is new. Each is already bound by an existing freeze identity.

| Symbol | Meaning | Source and binding |
|---|---|---|
| N | Admitted quantity of the intent | `entry_quantities` / `add_quantity` at `replay.py:412-416`, from the frozen policy and effective settings |
| k | Child index, 1 … N, in submission order | — |
| σ | +1 for a buy, −1 for a sell | `LegSpec.entry_side` (`book_policy.py:145`), enforced at `replay.py:399-401` |
| t | The leg's minimum tick | `ADAPTERS` (`book_adapters.py:39-60`) → `Instrument.mintick` (`replay.py:52`, `production_source.py:1149`) |
| s | The leg's emulator slippage ticks in the base run | `emulator.slippage_ticks` of the reviewed effective-settings successor (`production_source.py:1146-1150`), bound by the contract's `effective_settings_sha256` (`book_adapters.py:226-230`) |
| δ | Ladder step in ticks: **δ = max(1, s)** | Derived from s; one-tick floor so the ladder never collapses into option (a) |
| P₁ | The price the emulator assigns today to the whole intent | §1 rules, unchanged |

**Rules.**

- **B1 — price.** Child k fills at **P_k = P₁ + σ·(k − 1)·δ·t**, canonicalized with the emulator's `_snap` (`:291-294`). Child 1 fills exactly at today's price. P₁ is on-tick and the step is whole ticks, so every P_k is on-tick.
- **B2 — fill.** Each child is a separate one-contract fill. It fills at the timing event and bar timestamp at which today's single order fills, in full (RC-9's frozen full-fill field). Commission is the per-side commission times one (`:539`), so the intent's total commission is unchanged.
- **B3 — when the ladder applies.** It applies to fills that follow submission order: market entries and adds (`THIS_CLOSE` and `NEXT_OPEN`), and stop entries already marketable at registration (`:238-253`). It does **not** apply to a stop entry that rests past its generating bar. Rule 10 sends the next child on acknowledgement, not on fill, so every child is working before the trigger, and every child fills at P₁. UB-4 leaves the acknowledgement condition to be defined. If it is ruled to be a fill, resting stop children are sequential too, and this exception falls away.
- **B4 — delay model: none in bars.** All N children fill within the bar and timing event of today's single order. No child moves to a later bar, the next open or a schedule instant. The ladder is the only latency proxy. The replay has no intrabar clock and refuses unsupported intrabar evidence (`replay.py:1-6`).
- **B5 — protection.** Each child carries the intent's bracket levels unchanged, as absolute prices rounded as today (`_rounded`, `:312-320`). No level is recomputed from a child's fill price.
- **B6 — bookkeeping.** The whole-intent reservation is unchanged (`replay.py:423`). Each child confirms one contract (`:189`). RC-6 marks each child against its own fill price, with the intent's unslipped trigger for a midbar fill (`:262-283`).
- **B7 — guards.** A non-finite or non-positive child price refuses with `ReplayNeedsContext`; it is never clipped. The ladder uses the base-run s. A D20 stress cell that alters slippage (RC-4) changes δ only if the battery owner says so before freeze.

**Closed form.** Relative to option (a), an intent costs an extra δ·t·pointvalue·N(N − 1)/2, against the order side.

**Properties.**
- N = 1 is identical to option (a). ORB's ruled settings give one contract per base and per add (ORB/Striker successor §0), so every ORB intent is unaffected.
- Deterministic: no random draw, no seed, no new tunable.
- Side-aware, so it covers the short Aegis leg.
- Per symbol: rule 10 is per symbol, so legs do not interact. The RC-5 admission order is unchanged.

## 3. Not modelled

This list exists so that nobody reads the algorithm as covering these cases:
- **Abandonment of the unsent remainder** (UB-4; Ruling 5 for Striker and Vanguard). Under full fill the base run has no exceptional outcome. Partial fill is a stress cell (RC-4, RC-9).
- **A split sequence that crosses a bar, cutoff, flatten or takeover.**
- **Market impact or queue position** beyond the ladder. Live latency stays an I8 deviation class, measured in Phase 8 against frozen tolerances (`OWED-BY: TB-F1`).
- **A child priced at or beyond its own target level.** The emulator evaluates the absolute target by its existing rules from the next path point.

## 4. Exits are unchanged

- **Protective exits.** Each child's protective orders rest at the broker; they are not sequential sends. They are priced as today (`_fill_exit`, `:546-593`). Same-level children close at one price, FIFO. Whether same-level one-contract stops execute together live is the route's existing exit-side partial-fill item (checklist item 7.6, "Remaining").
- **Closes and flattens.** For the first release, every strategy close and scheduled flatten is one C-a request (checklist item 7.2; the successors' exit-split items are proposed moot). `_close_scope` prices every lot at one price (`:595-605`).

## 5. Realization consequences

This section names consequences; it does not design the change.
- **The emulator cannot produce this today.** It fills an intent as one fill (`:529-543`). Realizing B1–B7 changes RC-4's base-run fill model for multi-contract intents. That needs a dated RC-4 marker in the replay spec and an accepted change to the `replay_kernel` freeze-inventory module (`trust_domain.py:141`), and possibly to `c1_signal_daemon.tv_broker_emulator` (`:176`). This is the same treatment as Ruling 7(a)'s replay correction.
- **Adapter parity stays on the unmodified emulator.** Adapter acceptance is exact parity with the pinned exports (`tv_broker_emulator.py:1-9`; `book_parity.py`). The ladder belongs to the qualification replay only.
- **The `broker_factory` seam does not avoid that acceptance.** It "does not approve a stress fill model for qualification" (`replay.py:125-133`).
- **Child identities.** Adverse marking finds each entry fill's pending intent by order id (`replay.py:248-249`, `:279`), so child identities must keep that lookup exact.
- **Before freeze.** Building and testing the change on synthetic fixtures is a separately authorized change. Running it on an edition before its pre-registration freezes is barred (§R of each successor).

## 6. Paste-ready §6 text (for the operator to adopt, amend or reject)

> **Replay modelling of the split: (b).** Each admitted entry or add of N ≥ 2 contracts is priced as N one-contract fills. Child k (k = 1 … N, in submission order) fills at P₁ + σ·(k − 1)·δ·t, where P₁ is the price the emulator assigns today to the whole intent, σ is +1 for a buy and −1 for a sell, t is the leg's minimum tick, and δ = max(1, s), with s the leg's base-run emulator slippage ticks in the frozen effective settings. Every child fills in full, at the bar and timing event of today's single order, with no delay in bars. The ladder does not apply to a stop entry that rests past its generating bar; each such child fills at P₁. Bracket levels are absolute and unchanged. Commission is per child. Exits, closes and flattens are priced as today. A non-finite or non-positive child price refuses. A stress cell changes δ only if its owner says so before freeze. The same rule applies in every edition file.

*Ruled 2026-10-02 (operator ruling 2026-10-02 (sitting 2)): option (b) as written in §2, δ = max(1, s), stress cells leave δ unchanged (B7's 'only if the battery owner says so' does not apply), the acknowledgement condition is acknowledgement (B3's resting-stop exception stands), and the same text goes in every edition file. The §6 paste text is adopted with its stress-cell sentence replaced by 'Stress cells leave δ unchanged.'*

## 7. Choices left to the operator

Each choice is fixed before freeze and never after.
1. Adopt (a), this (b), or (c).
2. If (b), the δ binding: max(1, s) as written, or a separate per-symbol constant stated now.
3. If (b), whether D20 stress cells scale δ (B7).

*Ruled 2026-10-02 (operator ruling 2026-10-02 (sitting 2)): option (b) as written in §2, δ = max(1, s), stress cells leave δ unchanged (B7's 'only if the battery owner says so' does not apply), the acknowledgement condition is acknowledgement (B3's resting-stop exception stands), and the same text goes in every edition file. The §6 paste text is adopted with its stress-cell sentence replaced by 'Stress cells leave δ unchanged.'*
