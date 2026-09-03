# Viable-Strategy Sequence — Overview & Phase Index

**Status:** `AWAITING GO` — authored 2026-08-23 at operator request ("write these up as full
plans, each phase a separate document"). Each phase carries its own GO gate; nothing below is
authorized by this overview. Queue-bind note: under the 2026-08-23 queue-led convention, phase
GOs function as operator promotions. STATE `#1` as of 2026-08-24
([addendum](../../adr/2026-08-09-survive-bound-is-the-queue-cap.md#addendum-2026-08-24--the-blocker-of-b7m1-is-queue-1));
that placement is not a phase GO.

> ⚠ **Reader-intercept 2026-09-03 — both numbers in this objective have moved since authoring.**
> (1) The Part A ceiling is **5.0%**, not 3.0% ([`prereg v2`](../../../docs/briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md) §3, 2026-08-26).
> (2) **Tradeify counts toward §4 again** — fork F1 was ruled 2026-08-23 (Tradeify excluded, the
> three-firm reading below) and **reversed 2026-09-01** ([`F1 reversal`](../../../docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md#addendum-2026-09-01--f1-reversed-a-tradeify-resting-discharge-now-counts-toward-4)),
> restoring the four-firm set {Bulenox, Tradeify, MFFU, BluSky}. Election only; no code moved.
> Read (b) as "≥2 of the four frozen $100K tiers, ≥1 `trailing_locking`". Body unedited.

**Objective:** a strategy that (a) clears the frozen survivor gate — bust ≤ 3.0% ∧ P(pass) ≥ 50%,
intraday-honest — on `Tradeify_Select_100K`'s real geometry, deployable on the S2b→rail path, and
(b) where possible also clears ≥2 of {Bulenox, MFFU, BluSky} to discharge the four-firms §4
falsifier before **2026-11-08** (post-F1, Tradeify counts zero toward §4).

**The strategic inversion this sequence encodes:** derive the admissible payoff-shape region from
the venue rules *first* (Phase A), source only mechanisms whose structure predicts that shape
(Phase B), then run the standard gauntlet (Phase C) and deployment chain (Phase D). The last three
months' kills paid full pipeline cost to discover at step 8 what the geometry could have said at
step 0.

## Phase index

| Phase | Document | Cost | Gate to start | Serial dependency |
|---|---|---|---|---|
| **A — Derive the target** | [`phase-a-target-derivation`](2026-08-23-viable-strategy-phase-a-target-derivation.md) | $0 / K=0 | A1+A2 executed 2026-08-23; A3 voided | none — started on GO |
| **B — Mechanism supply** | [`phase-b-mechanism-supply`](2026-08-23-viable-strategy-phase-b-mechanism-supply.md) | $0 (falsifier stage) | per-candidate; two operator bar-readings named inside | A2's shape region (pre-check input; disclosed-N accepted — RESULTS §4); A1's revival list (B-revive lane voided) |
| **C — The gauntlet** | [`phase-c-gauntlet`](2026-08-23-viable-strategy-phase-c-gauntlet.md) | $0 until data pulls; per-candidate | operator B4 GO per candidate (MSL charter step 5) | a Phase-B survivor |
| **D — Deployment** | [`phase-d-deployment`](2026-08-23-viable-strategy-phase-d-deployment.md) | $0 | starts automatically when a candidate enters TNEC-1 intake (Phase C step 8); arming GOs operator-only | a Phase-C survivor |
| **∥ — §4 firm-model repair** | [`parallel-s4-firm-repair`](2026-08-23-viable-strategy-parallel-s4-firm-repair.md) | $0 / K=0 | R1+R2 landed 2026-08-23; R3 gated on a Phase-C survivor | none — parallel with A/B |

## Standing constraints inherited by every phase

- **Clocks:** 2026-11-08 (§4 falsifier; TNEC-1 intake clock; PARK expiries; GRAND re-read).
  ~11 weeks. Phase A is days; Phase C is ~1–2 weeks per candidate; Phase B is the unschedulable part.
- **Budget discipline:** Rule 2 (budget before acting); $0 falsifiers before any spend; no data
  purchases before a survivor (Avenue-A gate); MSL yield falsifier — 6 consecutive pre-G0 deaths
  across ≥2 families closes the channel — so only shape-prechecked cards get authored.
- **Screens change only via Phase A3's pre-registered ruling** — the anti-degeneration guard.
  Relaxing screens because the sweep is dry, without pre-registration, is the classic failure the
  `programme-audit` protocol names.
- **Don't-do list:** no ORB re-entry (barred); no relitigating closed kills without new mechanism
  evidence; don't spend the last blind-channel pre-G0 slot casually; E1 stands (no slate-4 card
  until a WHO clears the full admission bar).
- **Honest terminal states:** a deployed survivor; a Tradeify-only survivor (deploys; §4 reads as
  designed — ⚠ post-2026-09-01 reversal that means it contributes **one real tier** toward the
  "≥2 of four", not zero as this file's objective line assumed, and one tier is not a discharge);
  or dry — channel falsifiers fire and the programme demotes to research-only, which
  the standing base case names as the *designed* outcome, not a process failure.

## Provenance

Sequence derived from the 2026-08-23 posture review in-session; mechanism-supply inputs from the
sanctioned ox-alpha lens, Uses 3–4, fully reconciled before inclusion
([Use 3](../../notes/notice/N-2026-08-23-ox-alpha-msl-who-sourcing-methodology-review.md) ·
[Use 4](../../notes/notice/N-2026-08-23-ox-alpha-mechanism-supply-candidates.md) ·
[scope ADR](../../adr/2026-08-22-ox-alpha-adversarial-lens-scope.md)). Zero authority attaches to
the external lens's output anywhere in these plans — every load-bearing claim cites a repo
artifact.
