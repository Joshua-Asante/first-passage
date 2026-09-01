# MSL second slate — two cards (Stage 0–1 only; $0 · K=0)

**Status:** ELECTED 2026-08-13 — design box + S2A sequencing via [ADR](../../adr/2026-08-13-msl-slate-2-design-box.md) (P3.4 GO). Slate-1 header remains the historical record of what slate 1 tested. **S2A explore `FALSIFIED`** (N-ACT; 2026-08-13); **S2B Stage-1 `FAIL` (route; pre-G0)** 2026-08-14 ([closure](../closures/MSL-S2B-closure-stage1-fail-route.md)) — slate-2 exhausted. **Slate-3 BLOCKED** (mechanism-dry) 2026-08-14 — [notice](../../notes/notice/N-2026-08-14-msl-slate-3-constraints.md); no camp. **§7 E1 HOLD** — [review](2026-08-14-msl-slate-generation-review.md) · [closure](../closures/MSL-S7-closure-resolved-e1-hold.md).
**Parent:** [MSL charter](../../spec/2026-08-12-msl-manual-sourcing-loop-charter.md) — steps 1→8 unchanged. A card licenses **steps 1–4 only**; G0 needs operator B4 (paid for S2A).
**Why two, not three:** slate 1 spent three cards on one thesis (MR-at-level, rr≈1) and bought one bit of information. These are two genuinely different bets, and their *routes* differ as much as their mechanisms.

## Elected design box (2026-08-13 — [ADR](../../adr/2026-08-13-msl-slate-2-design-box.md))

`rr` ∈ **[2, 3]** · target WR **0.30–0.42** · `R` solved to the **bust ≤ 3.0% frontier** per instrument (never fixed in the card) · **hard stop mandatory** ([2026-08-13 ruling](../../notes/notice/N-2026-08-13-external-eval-population-data.md) §10 — binds stop *presence*, not stop *type*) · k=1 independent entry/day · **no pyramiding** (N-SHAPE) · $200 all-win and ≤$750 worst day **at one declared design point** · no promised pass speed.

**Family:** trend-continuation / follow-through — the structural opposite of slate 1, and the Archetype-A shape the population evidence attests. **What changed and why:** at rr=1 gross expectancy is `2p−1`, negative below 50% WR; C1 measured 0.461/0.486 against a 52.1% break-even. The proposed box is *worse geometry at fixed edge* (re-derivation §4 proves high-WR strictly dominates) — it is chosen only because it is the region where positive edge has been observed under a mandatory hard stop.

---

## MSL-S2A — MCL session-trend continuation (non-index, clean route)

**Direction:** join an established intraday directional move on **MCL** after a pullback fails to reverse it — continuation entry on the resumption bar, hard stop beyond the pullback extreme, target at **rr ∈ [2,3]** of that stop, flat before the session boundary. **One** trigger class named a priori: *pullback-failure resumption*. Not breakout-from-range, not compression-expansion, not MR-at-level. Any second trigger class charges `K_intrinsic` +1.

**Mechanism story to sharpen at Stage 1 (Req 1a):** in a directionally-committed session, participants who faded the move hold losing inventory; a pullback that fails to extend forces that inventory out, and the unwind is the continuation leg. The constraint (established direction **∧** failed pullback) must **SELECT** the trade — delete (sham: a random in-session bar at matched time-of-day) and flip (join the pullback instead of its failure) are both mandatory and scored on the IS partition only. ⚠ A bare "momentum continues" story is *not* Req 1a-admissible; the WHO and the forced-unwind must be named.

**Instrument rationale (mechanism-independent, decided before any scoring):** MCL is **not an index future**, so the single-index intraday OHLCV raised bar does not reach it — the cleanest route available. Its ledger disposition is literally **"OPEN — geometry-cleared, mechanism-owed"**, i.e. an instrument waiting for exactly this. Energy is a structurally trending complex, which is a *design* prior, not evidence. Panel now exists at $0 (below). Cost RT **$4.12** (2×$1.06 commission + 2×$1.00 tick slippage) ⇒ 4× hurdle **$16.48**/contract/trade.

**Panel (landed 2026-08-13, this session):** `core/data/bar_data/MCL_M15.csv`, sha256 `5aa50456…bbd23`, 106,261 bars, **2022-01-02T23:00Z → 2026-07-02T00:00Z**. Operator-supplied CME BAR EXPORT v0.2 `MCL1!`; integrity battery clean (monotonic, no dupes, no OHLC violations, gap profile correct for a ~23h contract). ⚠ **The panel ends 2026-07-02, ~6 weeks before its export date — the CONFIRM window must end at the panel, not at "today."** Proposed split: **IS < 2025-07-01**, **CONFIRM 2025-07-01 → 2026-07-02** reserved unread.

**Standing instrument warnings that are Stage-1 obligations, not footnotes** (from [`MCL.md`](../../ops/instruments/MCL.md)):
- **W1 — monthly roll.** MCL rolls monthly; fade Stage-0 measured **~14% session exclusion** under the published roll-exclude rule, ~3× MYM's quarterly figure. The card is intraday/flat-by-close so roll exposure is confined to roll days, but the exclusion rule must be declared at G0 and applied identically to IS and CONFIRM.
- **W3 — session window is not equity RTH.** MCL trades ~23h. "Flat by 16:00 ET" is an *equity* convention; which window governs an Energy construct is an open design choice, and an equity-RTH integrity PASS certifies an arbitrary slice, not a venue session. **Stage 1 must name and justify the session window before any read.**
- **W4 — FOMC exclusion thins τ_max** (180→120 min at 09:30 for the frozen fade config). Any hold-horizon assumption must survive that exclusion.

**Route + door-check plan:** non-index ⇒ raised bar does not reach it. **R-FRAMING = §2.1** (ratified) admits non-index cards; record the framing in the door-check. ⚠ `MCL.md` carries **no `bars:` section** — verified. So `instrument_profiles.py cell MCL <id>` will emit **zero** BINDING BARs and the door-check is **vacuous by default**. Registering the SNAG bar on the MCL ledger is this card's **Stage-0 task**, exactly as C2's was for MGC (#770); the SNAG answer is an explicit card line item that blocks G0 independent of tool output.

**Known graveyard adjacencies (dedup to be executed, not asserted):** `Q-MCLTAS-1` FALSIFIED (TAS/settlement magnitude — different modality, different family) · BE3/SFX-1 fade-census kills (fade-scoped, ruled so 2026-08-10) · `CONFIG-B-MCL-2026-07-31` frozen **fade** config (geometry cleared, mechanism-owed — *this card is not that config*) · the USOIL CFD-era closures (different venue/symbol; ledger says do not inherit) — and the USOIL **spike-fader** rejection is a *fade* entry, not a continuation entry.

**Stage-1 kill list:** Req 1a delete/flip on the continuation constraint (IS only) · cost-law at RT **$4.12** vs designed span · $200/$750 at the declared design point · session-window ruling (W3) · roll-exclusion rule declared (W1) · entry-rate honesty — if < ~1/week, **N-ACT FAILS as a solo construct** · SNAG bar registered and answered. Implied-SR printed, not a kill.

---

## MSL-S2B — MYM sweep-failure-filtered continuation (consumes C1's one positive result)

**Direction:** a trend-continuation entry on **MYM**, **gated** by a PDH/PDL sweep-failure state — take continuation trades only when the session has already swept and failed a prior-day extreme. The sweep-failure is a **filter**, never the entry. rr ∈ [2,3], hard stop, k=1, flat by 16:00 ET.

**Why this card exists — the asset it consumes:** C1's explore returned `FALSIFIED` on edge but its **DELETE test PASSED on both arms** — the PDH/PDL constraint genuinely *selected* (constrained arm less negative than the sham). That is the only measured-positive selection signal slate 1 produced, and it is currently filed inside a closure and otherwise unused. Role-asymmetry is a ratified `(mechanism, role)` dedup axis ([ADR 2026-06-14](../../adr/2026-06-14-rejected-candidate-patterns.md) §3): the entry-role construct is dead; the **filter role** is a different pair.

**⚠ This card's primary risk is its ROUTE, and it must die pre-G0 if the route cannot be declared cleanly.** MYM is an index, so the raised bar binds. The entry is trend-continuation — the bar's **named exhausted lever**. Two candidate routes, both problematic, and Stage 1 must resolve *in writing* or kill:
- **Route ① via the SLR MR-at-level precedent** — carries only for the *filter signal*, which is MR-at-level; it does **not** obviously carry for a continuation *entry*.
- **Route ① via within-instrument temporal selectivity** ([ADR 2026-08-10](../../adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md)) — but the dense-1m OHLCV temporal-selectivity lane was **default-paused 2026-08-12** (Q-TNEC-CON-5), so this route needs an explicit non-route-① thesis or an operator un-pause.

**Forbidden here, explicitly:** re-arguing the raised bar, or asserting the composite "exhausted entry + route-① filter" clears it because one component does. If Stage 1 cannot answer the bar by a route that already exists, this card is a **$0 pre-G0 kill** and that is a correct outcome.

**Instrument rationale:** MYM's panel is landed and deep (1,607 IS sessions), the sweep-failure signal is measured *on this instrument* (transfer would void the asset), occupancy is released by B8, and cost RT is **$2.82**. Disclosure: `K_banked(MYM)` = 2 → **does not gate**; screening floor is `floor_at_k(1)` = **0.65**.

**Known graveyard adjacencies:** MSL-C1 closure (the entry-role kill — this card must show it crosses into filter role, not re-run the entry) · SLR-MYM-1 · opening-range continuation on MYM (dead, 7 gates) · the 2026-08-10 dense-1m packet's **"forbids PDH/PDL θ"** bar — Stage 1 must verify whether it is lane-scoped or binds here · Q-TXG-1 lane bar.

**Stage-1 kill list:** **route declaration (kill limb #1)** · Req 1a delete/flip on the *filter* — the filtered set must beat the unfiltered continuation baseline, not merely be positive · filter selectivity honesty (what fraction of sessions qualify — if it fires on most sessions the premise is void, the SWING-1 failure mode) · cost-law at $2.82 · $200/$750 · entry-rate/N-ACT.

---

## Sequencing

**S2A first, serialized — explore `FALSIFIED` (N-ACT).** [closure](../closures/MSL-S2A-closure-falsified.md) · [`RESULTS_g2`](../../lab/archive/msl_s2a_mcl_2026-08/RESULTS_g2.md). CONFIRM unread; Pine unpaid. **Board 2026-08-13:** C3-K2 revive inserted ahead of S2B ([ADR](../../adr/2026-08-13-msl-c3-k2-dual-axis-revive.md)); explore later FALSIFIED. **S2B 2026-08-14:** Stage-0/1 authored; **route FAIL** — [closure](../closures/MSL-S2B-closure-stage1-fail-route.md) · [`STAGE1`](../../lab/analysis/c1/msl_s2b_mym_2026-08/STAGE1.md). G0 never frozen.

**Counter state:** Stage-1 deaths **2/3** (C3 + S2B). Slate-3 **BLOCKED** without incrementing the counter ([notice](../../notes/notice/N-2026-08-14-msl-slate-3-constraints.md)). [§7](2026-08-14-msl-slate-generation-review.md) **E1 HOLD** (functional 3/3). Charter yield falsifier (6 pre-G0 deaths / 12 weeks zero G0s) not fired.
