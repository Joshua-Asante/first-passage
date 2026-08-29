# Pre-assembly — 08-08 A1 accept-beta fork (cost × probability, decision-ready)

**Status:** **PRE-ASSEMBLED** for the 2026-08-08 Class-A **A1** decision. This packet assembles the two *closed* analyses into one page so 08-08 is a decision, not a re-read. **It is not the decision** — the accept-beta call is operator GO/NO-GO at the gate, taken together with A5's live regime re-MC.
**Date:** 2026-07-14
**Owned by:** [`docs/adr/2026-06-07-decompound-remc-hold.md`](../adr/2026-06-07-decompound-remc-hold.md) §4 (regime trigger + accept-beta fork) · 08-08 pre-triage [`2026-07-12-08-08-packet-pretriage.md`](2026-07-12-08-08-packet-pretriage.md) A1
**Pairs with:** **A5** (decompound-HOLD §4 limb-2 live regime re-MC — the current-regime input this fork reads)

---

## §0 — Reads (source-verified 2026-07-14)

- [`docs/briefs/Q-DECAY-1-closure-scope-split.md`](Q-DECAY-1-closure-scope-split.md) — the **cost** input (bust-before-signal; common-mode uncovered).
- [`docs/briefs/Q-PERSIST-1-closure-moot.md`](Q-PERSIST-1-closure-moot.md) — the **probability** input (MC understates the tail).
- [`docs/adr/2026-06-07-decompound-remc-hold.md`](../adr/2026-06-07-decompound-remc-hold.md) §4 — the standing HOLD + the k≈0.55 interim mitigation + the regime trigger.
- `CLAUDE.md` §Regime caveat — no static de-risk is regime-robust without breaking the (now-retired) challenge; both candidates fail the regime-robustness gate on the 2020-23 half.
- Family basis: `project_q_mech_1_family_synthesis` (0/4 external mechanism ⇒ one shared beta) + `project_strategy_lifecycle_governance` (4 legs `AUTHORIZED @ 1.00×`, off all live venues).

## §1 — The decision

The four legs (Guardian / Striker DJ30 / Aegis / NAS100) are a **shared-mechanism family** — Q-MECH-1 found 0/4 external mechanisms, i.e. they carry **one common beta / regime exposure**, not four independent edges. **Accept-beta** = the standing operator decision to carry that single shared-beta exposure at the locked config, versus de-risk it. The 08-08 fork feeds that decision with the paired **cost × probability** of the common-mode tail, plus A5's live reading.

**Scope honesty:** all four legs are currently `AUTHORIZED @ 1.00×` but **off every live venue** (CFD retired, futures-prop NO-GO). So today this is a **standing risk-governance decision** about the family's configuration (and the MC regression pin), not a live-capital call — the cost/probability below are dormant properties of the locked config that bind if/when the family deploys.

## §2 — COST side (Q-DECAY-1): the tail is uncovered

Accepting the shared-mechanism family means accepting that **common-mode edge death is UNCOVERED**:

- **No cheaper-than-drawdown family detector exists.** No k-of-N or aggregate-expectancy monitor. ECR is execution-fidelity (a ratio blind to edge magnitude, and dormant), not a decay detector.
- **Under genuine common-mode edge death, the earliest portfolio-DD signal arrives only after a median max DD of ~11.7% — past the 5% firm bust line.** Drawdown "detects" the death only *after the account has already busted*. Even Guardian's single-leg CUSUM is late for the family (~4.7% portfolio DD).
- **The detector can't be built today** (surfaced candidate = extend the Guardian decay-gate spine to all 4 legs + a family aggregate; operator-decision, NOT built), double-blocked by:
  1. **No validated exogenous regime classifier** (VIX>20 falsified 2026-06-22; endogenous OHLC falsified — the DP-4 interlock that caps even the Guardian gate at WATCH).
  2. **All 4 legs off their live venues** → every CUSUM accrues zero in-regime trades; even a full build is forward-armed and dormant.
- **Re-arm condition (binary):** a leg goes live on some venue (fills accrue) **AND** a regime classifier passes its own robustness gate.

**Cost in one line:** *if the shared mechanism dies, it costs a ~bust-line drawdown before any signal fires, and no detector can currently front-run it.*

## §3 — PROBABILITY side (Q-PERSIST-1): the tail is under-priced

The MC's common-mode bust probability is **optimistic (directionally)**:

- The production one-week (iid-weekly) block bootstrap **understates bust by +0.46pp** on the tail-relevant **2020–26 decompounded** panel (**2.96% → 3.43%** under a persistence-preserving L=8 block; p90 +8 days). Median pass-time **unchanged**; p99 DD slightly *lower* under the block (5.93% → 5.78%) — a **tail-compression, not median-speed** finding, consistent with §2 (common-mode risk is a bust-tail phenomenon).
- **Feasibility caveat (load-bearing):** the +0.46pp is on the decompounded panel, **not** the locked **2022–26 compounded anchor (99.83/0.17/4.37)**. On the locked anchor the understatement is **> 0 but well below +0.46pp** (a small fraction of a pp) — the decompounded panel's persistence is dominated by 2020–21 dead-week chop (dead-share 29% / 38%), which the locked window excludes. **Bounded-small, feasibility-unmeasured; NOT a re-pin.**

**Probability in one line:** *the MC under-prices the common-mode tail in the risk-increasing direction — materially on the decompounded panel, bounded-small on the locked anchor.*

## §4 — Both biases point the same way

The common-mode tail is simultaneously **under-monitored** (§2: no detector, bust-before-signal) **and under-priced** (§3: MC bust optimistic). Neither offsets the other; both push the *true* risk of the shared-beta family above what the headline anchor (0.17% bust) and the current controls suggest. That convergence is the substance of the accept-beta decision: the operator is deciding whether to carry a tail that is worse than the pin says and invisible until it busts.

## §5 — Pairing with A5 (the live input at 08-08)

A1 is the **standing structural** characterization; **A5 is the live reading**. At 08-08, run A5 = decompound-HOLD §4 limb-2 regime re-MC (`regime_gate.py` on the trailing-6-month panel at the locked config):

- **A5 breaches** (p99 DD ≥ 5% **OR** bust ≥ 1%) ⇒ HOLD FALSIFIED ⇒ the accept-beta decision is forced toward **de-risk**: open a regime-adaptive-sizing Pre-Q **+ interim k≈0.55 haircut** (all four allocations → 55%). Operator GO/NO-GO on the haircut is a same-session live-allocation event.
- **A5 clean** ⇒ **accept-beta with eyes open** is available: hold the locked config, carry the (uncovered, under-priced) tail as a known cost, and rely on the quarterly regime trigger as the operational tripwire.

*(A5 runs a historical-semantics regime read even with no capital deployed — the rescope keeps the bust/p99-DD mechanism falsifier LIVE; it is not challenge-denominated.)*

## §6 — Decision framing + default

**Default posture (standing since 2026-06-07): locked config HELD**, tail managed operationally + a quarterly regime trigger. The accept-beta fork re-affirms or revises that.

- **Accept-beta (HOLD, eyes-open)** — justified if A5 is clean *and* the operator accepts a bust-before-signal, under-priced tail as the price of the shared-mechanism family, with the quarterly A5 re-MC as the tripwire. Note the family is off-venue, so this is a governance re-affirmation, not a fresh capital commitment.
- **De-risk** — the pre-registered interim is **k≈0.55** (all four → 55%). **Caveat (do not overclaim it as a fix):** no static de-risk is regime-robust — both k=0.55 and DD_SCALE→0.20 **fail the regime-robustness gate on the 2020-23 half**. De-risk trades headline tail for a still-regime-fragile posture; it is a mitigation, not a solution. (The old "makes the challenge impractical" cost is now moot — the venue is closed; the trade-off today is against the self-funded / prop paths' economics.)

**The genuine crux for the operator:** is a **~11.7% bust-before-signal, detector-less, mildly-under-priced** common-mode tail acceptable as the standing posture of the shared-beta family — or does it warrant the (regime-fragile) 55% haircut? A1 says the tail is real, uncovered, and under-priced; A5 says whether it is firing *now*.

## §7 — What this pre-assembly does NOT do

- It is **not** the accept-beta decision (operator, at the gate, with A5's result).
- **No MC re-pin, no block-length change, no allocation change, no `dd_protection` edit.** The +0.46pp is not carried onto the locked anchor; 99.83/0.17/4.37 stands as the pin.
- It does **not** build the family detector (blocked; operator-decision) or re-open Q-DECAY-1 / Q-PERSIST-1 (both CLOSED).

## §10 — Audit hooks (runnable) + the numbers to cite at 08-08

```bash
# Both closures still present + carry their §Re-check hooks
grep -n "accept-beta\|Re-check hook" docs/briefs/Q-DECAY-1-closure-scope-split.md docs/briefs/Q-PERSIST-1-closure-moot.md

# The load-bearing figures (cite verbatim at 08-08)
grep -n "11.7%\|4.7%" docs/briefs/Q-DECAY-1-closure-scope-split.md       # cost: ~11.7% common-mode; ~4.7% Guardian-late
grep -n "0.46pp\|2.96%\|3.43%" docs/briefs/Q-PERSIST-1-closure-moot.md    # probability: +0.46pp (decompounded), bounded-small on anchor

# A5 pairing — the live falsifier that decides accept vs de-risk
grep -n "p99 DD ≥ 5% OR bust ≥ 1%\|k≈0.55\|55%" docs/adr/2026-06-07-decompound-remc-hold.md

# At 08-08, the SESSIONS entry must record the accept-beta disposition + A5 result (not a silent re-park)
grep -n "accept-beta\|A5\|regime re-MC" docs/SESSIONS.md
```

**Cite at 08-08:** cost **~11.7%** median common-mode max DD (bust-before-signal); probability **+0.46pp** bust understatement (decompounded; bounded-small on the locked anchor); default **HOLD**; de-risk = **k≈0.55** (regime-fragile). Decision gated on **A5** breach/clean.

---

## Addendum 2026-08-29 — §5 pairing mechanism SUSPENDED-ORPHANED (DECAYED_UNDOCUMENTED, brief-decay-audit)

Per Rule 14, this correction lands here because §5 above ("Pairing with A5") and §6 ("Decision
framing + default") are the sections a reader consults to run this fork — both stay
byte-unedited; this addendum is the reader-intercept + record.

1. **§5's A5 (decompound-HOLD §4 limb-2 regime re-MC) cannot run.** It was declared
   **SUSPENDED-ORPHANED / permanently `NOT_EXECUTABLE`** by
   [`docs/adr/2026-06-07-decompound-remc-hold.md`](../adr/2026-06-07-decompound-remc-hold.md)'s
   own 2026-08-03 addendum, following the 2026-08-02 Pepperstone feed retirement — it can never
   run at 08-08 or any future quarterly date (the schedule itself is struck, not deferred). 08-08
   has now passed with **no A5 result recorded anywhere**: `docs/SESSIONS.md` carries no such
   entry, confirmed by direct check of this brief's own §10 hook.

2. **The standing re-scope of record is the successor packet.**
   [`docs/briefs/2026-07-17-0808-packet-delta-and-sequence.md`](2026-07-17-0808-packet-delta-and-sequence.md)
   already recorded, 2026-08-02: *"A5 + P1 struck with the Pepperstone feed retirement… A1
   re-scoped not decided"* — cite that packet, not this one, for the current disposition of the
   A5 input.

3. **§6's accept-beta decision was never actually made, under either framing.** It is not a
   silent re-park to HOLD-by-default — it is **still open**, gated on an input (A5) that no
   longer exists. The re-scoping brief that carries the current framing is itself stale: it
   carries its own 2026-08-06 reader intercept warning that it predates the 2026-08-04 Tradeify
   venue de-scope and must not be read as the live slate without re-walking the board at the
   gate.

4. **If the operator wants A1 decided, it needs a fresh dated packet** reading current
   post-de-scope, post-Great-Prune state — not a re-read of this pre-assembly (which still frames
   the decision around a now-unrunnable A5) and not a silent adoption of the 07-17/08-06 packet's
   framing without re-verifying it against today's board.
