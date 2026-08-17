# ADR 2026-08-16 — CON-5 pause is dense-1m-scoped; route-①-via-temporal-selectivity outside that lane needs its own cheap-falsifier gate

**Status:** `Accepted` — operator election 2026-08-16 (in-session, presented as a blocking scope ruling with three options — narrow / broad / narrow-gated-by-cheap-falsifier; "cheap falsifier gate" elected)
**Decision date:** 2026-08-16
**Authors:** Joshua (direction + election) + Claude Code (Rule-0 recon, design)
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Related:** [`Q-TNEC-CON-5-closure-ambiguous-hold.md`](../briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md) (the pause) · [`2026-08-10-temporal-selectivity-outside-mapped-levers.md`](2026-08-10-temporal-selectivity-outside-mapped-levers.md) (route ① itself, domain-level, not timeframe-scoped) · [`2026-08-15-analogue-modality-route-ruling.md`](2026-08-15-analogue-modality-route-ruling.md) (sibling scope ruling on the same pause, different axis — construct-type, not timeframe) · [`MSL-S2B-closure-stage1-fail-route.md`](../briefs/closures/MSL-S2B-closure-stage1-fail-route.md) (the card that surfaced the ambiguity) · [`DENSE1M-UNPAUSE-closure-resolved-u0-keep.md`](../briefs/closures/DENSE1M-UNPAUSE-closure-resolved-u0-keep.md) (U0 KEEP 2026-08-15 — the pause itself stands; this ADR unpauses nothing) · [`2026-08-16-deep-lane-dl1-mgc-orc-prereg.md`](../briefs/pre-registration/2026-08-16-deep-lane-dl1-mgc-orc-prereg.md) §0 standing-pause attestation (same-day sibling adjudication — **harmonized in §2 D2a below, superseding nothing**)
**Layer:** methodology (research rules of evidence only). No strategy/risk-control parameter, allocation, `dd_protection` constant, or Pine source is touched. **$0 / K=0.** **Tier:** FULL — creates a new, reusable pre-G0 falsifier-gate mechanism binding future candidate sourcing, the same weight class as the 2026-08-15 no-counterparty-channel ADR.

---

## §0 — Rule 0 reads

Files read in full before drafting, this session:

- [`docs/briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md`](../briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md) — the pause text: "OHLCV temporal-selectivity lane default PAUSED (Branch A)." Branch A's grounds cite "8 consecutive zero-yield closes since 2026-08-08" across the short-horizon MNQ microstructure thread (Q-R2VBUCK-1, Q-R2FLOW-1, Q-R2AGRUN-1, Q-MNQDTL-CON-1, Q-TNEC-CON-2/3/4/5) as the exhaustion evidence.
- [`docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md:22`](../spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md) — the lane's own defining scope line: *"iterate named entry mechanisms... on **the dense-1m G=10 universe**"* — a specific, technically-defined population (1-minute MNQ, G=10 grid), not "OHLCV entry-geometry constructs" in general.
- [`docs/adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md`](2026-08-10-temporal-selectivity-outside-mapped-levers.md) §2-B — the ruling that opened route ① to within-instrument temporal selectivity in the first place is a **domain-level** finding against the raised bar's own mapped cost-ratio levers (price / cross-instrument-selection / hold-time); the raised bar itself is index-wide, never dense-1m-scoped. Route ① under this ADR was never timeframe-conditioned.
- `lab/analysis/c1/msl_s2b_mym_2026-08/STAGE1.md:82,84` — the same "dense-1m"-scoped qualifier read two opposite ways in adjacent BINDING BAR rows, same card: `:84` rules a sibling dense-1m bar **does not bind** ("session-scale 15m; not a new dense-1m ... family"); `:82` rules the CON-5 pause **does** bind, with no stated argument distinguishing the two.
- `lab/archive/msl_c3_m2k_2026-08/PREREG_G0.md:25`, `STAGE1_K2.md:41,98` — cite "dense-1m / CON-5 pause... does not bind session-scale 15m failed-break reclaim," but on inspection this is obiter, not a settled ruling: that campaign cleared its own raised-bar bar entirely via SLR mean-reversion-at-level precedent (a different route-① path) and never actually needed the temporal-selectivity route. It does not resolve today's scope question either way — cited here so it is not mistaken for precedent it isn't.
- `docs/briefs/closures/MSL-S2B-closure-stage1-fail-route.md:17-19` — MSL-S2B's Candidate A (SLR route ①) clears only the *filter* component (MR-at-level precedent), not the *continuation-entry* component; Candidate B (temporal selectivity) was the only remaining route to clear entry, and died specifically on the CON-5 citation.
- `lab/analysis/c1/msl_s2b_mym_2026-08/STAGE0.md:24,27` — panel pin `core/data/bar_data/MYM_M15.csv` (hash `24e169528f7ea6693b75c71c3195edf6a04f3a26c6b6dff0f2e9c623fd597a58`); this worktree confirmed to hold only `core/data/bar_data/README.md` + `SHA256SUMS` — the CSV itself is absent (gitignored vendor data, not checked out here).
- [`docs/briefs/closures/DENSE1M-UNPAUSE-closure-resolved-u0-keep.md`](../briefs/closures/DENSE1M-UNPAUSE-closure-resolved-u0-keep.md) — **read at replay, after initial drafting** (this session's worktree predated it; caught on the origin/main reconciliation). U0 KEEP 2026-08-15: the pause **stands**; the packet's election was unpause-vs-keep (U0/U1/U2), not scope/reach — no scope question was put to that election. This ADR unpauses nothing, so no conflict; recorded here so the read-set gap is visible rather than silent.
- [`docs/briefs/pre-registration/2026-08-16-deep-lane-dl1-mgc-orc-prereg.md`](../briefs/pre-registration/2026-08-16-deep-lane-dl1-mgc-orc-prereg.md) §0 standing-pause attestation + GO item 2 — **read at replay, after initial drafting** (same gap). The DL-1 GO adjudicated "pause residual broad reading **rejected for DL-1**" on two grounds chosen to avoid lane membership: (i) instrument class (every enforcement on record is entangled with the index raised bar; MGC sits outside it), (ii) route-independence (DL-1 never invokes route ①). The attestation explicitly declined lane membership as a scoping argument *because* S2B's 15m enforcement made it unreliable — the exact inconsistency this ADR resolves. Harmonization in §2 D2a.

---

## §1 — Context

MSL-S2B (`sweep-failure-filtered-continuation` × MYM, 15m) died `STAGE-1 FAIL` on 2026-08-14 by treating the CON-5 pause — textually scoped to "the dense-1m G=10 universe" — as binding on a 15m card. A 2026-08-16 recon pass (part of the S3 WHO-drought-relief thread) surfaced that this reading was applied inconsistently within the card's own record: an adjacent BINDING BAR row treated a different, equally dense-1m-scoped bar as *not* reaching the same 15m card, with no argument for the difference. A candidate precedent (`C3-K2`, frozen 2026-08-13) uses similar "does not bind session-scale 15m" language, but turns out to be obiter — that campaign never needed the temporal-selectivity route at all, having cleared its bar entirely through a different mechanism (SLR precedent).

This left a genuine question: does CON-5's pause reach cards outside its own literal dense-1m/G=10 lane? It was **not** wholly unruled — the same-day DL-1 prereg GO adjudicated it *per-campaign* ("pause residual broad reading rejected for DL-1"), but deliberately on grounds that route around the general question (instrument class + route-independence), explicitly declining lane membership as an argument because S2B's enforcement record made it unreliable. What remained unruled is the **general scope theory** — the thing whose absence forced DL-1 to argue around it and left S2B's two adjacent rows contradicting each other. Three readings of that general question were put to the operator: narrow (textual, dense-1m only), broad (the underlying failure mode is treated as evidence against the whole approach regardless of timeframe), and a third — narrow in principle, but gated by a same-shape cheap falsifier before any card may rely on the opening. The operator elected the third, in-session, 2026-08-16.

---

## §2 — Decision

**D1 — Scope is textual and narrow.** CON-5's pause, by its own defining language, is scoped to *"the dense-1m G=10 universe"* — it does not, by name, forbid a route-①-via-temporal-selectivity argument on a card outside that lane (a different timeframe, e.g. 15m; or a different instrument's own within-instrument selection axis). The domain-level ruling that opened route ① at all ([ADR 2026-08-10](2026-08-10-temporal-selectivity-outside-mapped-levers.md)) was never itself timeframe-scoped.

**D2 — Reliance on that opening requires a cheap-falsifier gate, not a free pass — and the gate is scoped to route-reliance, not to OHLCV-ness.** What the pause pauses is a *route*: temporal selectivity as a route-① clearance of the index raised bar. The falsifier gate therefore binds exactly the cards that **rely on D1's narrow scoping to invoke that paused route** — an index-instrument card outside the dense-1m lane (e.g. a 15m MYM successor to MSL-S2B) that needs temporal selectivity to clear `index-intraday-ohlcv-directional-timing-2026-07-21`. Such a card may not treat the pause as simply inapplicable and proceed straight to G0. Before route ① via temporal selectivity counts as open for it, it must first clear a fresh, **generous**, **$0**, pre-G0 cheap falsifier — same shape and acceptance discipline as every cheap falsifier already run in this lane (`lab/analysis/c1/cheap_falsifiers_2026-08/`) — testing whether CON-5's *actual finding* (gross signed points captured by a low-WR, tight-stop, named-level entry-geometry construct gets eaten by the round-trip cost) recurs at that card's own timeframe/instrument. A PASS opens the route (necessary, not sufficient — Req 1a, delete/flip, cost-law, and every other requirement still bind in full). A FAIL closes route B for that construct-shape at $0, no Board debate needed — exactly how CON-1..5 themselves were closed.

**Falsifier spec (frozen here, reusable by any card invoking D1's opening):**

- **Test:** on the card's own IS panel only (CONFIRM never touched), compute mean signed gross points per filtered/gated entry-geometry signal, using the construct's own already-frozen stop/target box — not re-tuned for this test.
- **Pass bar:** `mean signed gross ≥ 0.5 × (4 × RT_frac)` at the panel's own price/cost basis — half of CON-5's own clearance bar, generous by design so a FAIL is conclusive (`lesson_run_cheap_falsifier_before_authoring`: design it generous).
- **Report:** coverage %, n, mean signed gross, 4×RT hurdle in matching units, and WR — the same four figures CON-5's own closure reported, for direct comparability.
- **Cost:** $0, no `register_search open`, no Q-ID, no K spend — a pre-G0 falsifier exactly like the 2026-08-10 cell-#3 and CON-5 precedents.

**D2a — Harmonization with the DL-1 adjudication (supersedes nothing).** A card that never invokes the paused route needs **no** D2 falsifier — it is outside the pause's subject matter entirely, whatever its bar timeframe or data sourcing. DL-1 (MGC, non-index, no raised bar to clear, route ① never invoked) is the worked instance: its GO-adjudicated exemption on instrument-class + route-independence grounds stands untouched, and this ADR would have reached the same result through D2's own scoping. Going forward, the DL-1 attestation's stated reason for distrusting lane membership as an argument — S2B's 15m enforcement — is resolved by this ADR (that enforcement was an over-broad reading, prospectively corrected), so future attestations may cite lane scope *plus* route analysis directly instead of arguing around the gap; per-campaign attestation at GO remains good practice, not a superseded ceremony.

**D3 — MSL-S2B's own `STAGE-1 FAIL` verdict is unchanged; this ADR is prospective, not retroactive.** No D2 falsifier was run before that card's 2026-08-14 disposition, so it cannot resurrect itself. What this ADR licenses is a **fresh successor card** (new commit, same or adjacent mechanism id) that runs the D2 falsifier for `sweep-failure-filtered-continuation` × MYM 15m before relying on route B. The falsifier is fully specified above and needs only panel access — `core/data/bar_data/MYM_M15.csv` — which is **absent in this worktree** (confirmed by directory listing; only `README.md` + `SHA256SUMS` present). Unexecuted here for that reason, not deferred by choice.

**D4 — `STAGE1.md`'s internal inconsistency is resolved going forward, not retroactively edited.** Both "dense-1m X" bars in that table now read the same way under D1/D2: textually scoped to the dense-1m lane, and — if a future card wants to rely on that scoping to treat either bar as non-binding — gated by the matching cheap falsifier for that bar's own underlying finding. `STAGE1.md:84`'s existing answer already satisfies this in substance for that row; no retro-edit of the frozen card record.

---

## §3 — Alternatives considered

| Alternative | Why not elected |
|---|---|
| **Pure narrow reading (D1 only, no gate).** | Opens the door by textual technicality alone, with zero evidence the underlying failure mode (low-WR entry-geometry construct, gross eaten by RT-tax) doesn't recur outside 1-minute MNQ. Risks reading as motivated — this ruling exists because S3 is hunting for open doors, and an ungated carve-out is the shape that scrutiny should be most skeptical of. |
| **Pure broad reading (pause covers any timeframe/instrument).** | Forecloses the door by extrapolation, equally without evidence, at the exact moment MSL is estate-wide dry (`N-2026-08-14-msl-who-track.md`, `RESOLVED (STILL DRY)`). Treats an untested hypothesis as settled and contributes $0 forward capacity to the drought this thread exists to relieve. |
| **Retroactively reopen MSL-S2B under D1 alone.** | No falsifier was run at the time of its disposition; reopening it without one would be exactly the "silent reopen" pattern the card's own closure explicitly forbids (`MSL-S2B-closure-stage1-fail-route.md:26`). |

---

## §4 — Falsifiable hypothesis

**H:** the D2 falsifier gate, applied to future cards outside the literal dense-1m lane, correctly separates constructs that share CON-5's actual failure mode (gross eaten by RT-tax) from those that don't — i.e. it neither reopens a door onto more CON-1..5-shaped dead ends, nor keeps shut a door onto a genuinely different cost geometry at a different timeframe.

**Accept H (informally) if:** at least one card runs the D2 falsifier and its PASS/FAIL disposition tracks a genuinely different cost-geometry finding than CON-1..5's own (i.e., the gate discriminates, not just rubber-stamps one way).
**Reject H if:** a card's D2 falsifier PASSes and the resulting G0/explore still dies to the identical RT-tax/low-WR shape CON-5 found — evidence the gate's pass bar (0.5× CON-5's clearance bar) was set too loose.
**Re-test:** at the next card that actually invokes D1/D2, or the 2026-11-08 quarterly audit if none does.

---

## §5 — Forbidden moves

1. Treating a D2 falsifier PASS as a G0 freeze, a delete/flip PASS, or any other downstream gate discharge — it is a pre-G0 door-check only.
2. Reading D1 as reopening CON-1..CON-4's own dense-1m findings, or any candidate genuinely inside the literal dense-1m/G=10 lane — those stay paused exactly as ratified 2026-08-12.
3. Treating this ADR itself as the D2 falsifier for MSL-S2B or any other specific card — the spec is frozen here; execution is a separate, future act.
4. Re-tuning the falsifier's pass bar (`0.5 × 4×RT`) per-candidate to admit a marginal construct — the bar is a channel property, not a candidate property (mirrors the blind-channel K-cap addendum's D-K3).
5. Citing this ADR as a Board un-pause of the dense-1m lane itself — untouched.
6. Silently editing `STAGE1.md`'s frozen 2026-08-14 record — corrections land as a forward pointer to this ADR, not a retro-edit of the card.

---

## §6 — Consequences

**Positive:** resolves a real, adversarially-caught internal inconsistency (the same qualifier read two ways in one document) without deciding the underlying empirical question by fiat in either direction. Reuses the exact cheap-falsifier machinery and acceptance discipline already standing in this lane — invents a pass-bar number, nothing else. Keeps a real, previously load-bearing door open pending a $0 test rather than closed by extrapolation, at a moment (MSL estate-wide dry) where that matters.

**Negative / watched:** the falsifier-gate pattern is now a second interpretive mechanism (alongside the 2026-08-15 analogue-modality ruling) for narrowing what a pause actually reaches — a future audit should watch that this doesn't become a standing technique for relitigating every inconvenient pause. The 0.5× pass bar is a judgment call, not derived from data; §4's falsifiable hypothesis exists specifically so that judgment gets checked against a real outcome rather than standing unexamined.

---

## §7 — Implementation plan

- **Phase 0** — §0 reads (done, this ADR).
- **Phase 1** — this ADR ships as the ruling; no code changes required (reuses existing cheap-falsifier pattern and `lab/analysis/c1/cheap_falsifiers_2026-08/` convention unmodified).
- **Phase 2** — forward pointers added to `MSL-S2B-closure-stage1-fail-route.md` and `STAGE1.md` (same commit) noting this ADR exists, without altering either's frozen verdict.
- **Phase 3** — the MSL-S2B D2 falsifier itself (`sweep-failure-filtered-continuation` × MYM 15m) is specified but **not executed** — blocked on panel access (`MYM_M15.csv` absent in this worktree). Next operator with that file locally, or a Databento pull under the standing cost-gate, can run it in under five minutes per the frozen spec above.

---

## §10 — Audit hooks

```bash
grep -n "Status:" docs/adr/2026-08-16-con5-timeframe-scope-cheap-falsifier-gate.md
# Expected: Accepted

# Has any card invoked D1/D2 since this ADR?
grep -rl "2026-08-16-con5-timeframe-scope" lab/analysis/ lab/archive/ 2>/dev/null

# MSL-S2B's own verdict is untouched (D3) — must still read STAGE-1 FAIL
grep -n "STAGE-1 FAIL" docs/briefs/closures/MSL-S2B-closure-stage1-fail-route.md

# Panel still absent in this worktree (confirms D3's stated blocker, catches drift)
test -f core/data/bar_data/MYM_M15.csv && echo "PRESENT — falsifier now runnable" || echo "absent, as recorded"
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-16 | Authored; operator elected the falsifier-gate reading (third of three options) | Joshua (election) + Claude Code |
| 2026-08-16 | Same-session amendment at origin/main replay, **before first ship**: worktree predated the 08-15 U0 KEEP closure and the DL-1 prereg's GO-adjudicated pause attestation — both added to §0 with the gap named; §1 "previously-unruled" corrected; D2 sharpened to route-reliance scoping (as first drafted it would have demanded a falsifier from DL-1-class cards, contradicting DL-1's own GO); D2a harmonization added. No decision changed; grounds completed. | Claude Code (caught on origin/main reconciliation) |

---

## Verification

```bash
python scripts/check_brief.py docs/adr/2026-08-16-con5-timeframe-scope-cheap-falsifier-gate.md --type adr
python scripts/check_adr_graph.py --regenerate-index
python scripts/check_adr_graph.py
```
