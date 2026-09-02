# Q-BUSTGATE-1 — On what basis is the Part-A eval bust ceiling set, and does eval-fee-vs-funded-upside economics yield the same number?

**Status:** `CLOSED-FALSIFIED 2026-07-23` — derivation landed **`FALSIFIED`** (H-BUSTGATE's "economics ratifies 3.0%" claim rejected: the EV-optimal admissible rung busts 4.37% > 3.0%); operator **elected fork B** (2026-07-23). Closure: [`closures/Q-BUSTGATE-1-closure-falsified.md`](closures/Q-BUSTGATE-1-closure-falsified.md); fork-B artifact: [`../adr/2026-07-23-c1-rung-selection-ev-objective.md`](adr/2026-07-23-c1-rung-selection-ev-objective.md) (`Proposed`).
⚠ Status-tag correction 2026-08-29: the fork-B artifact `../adr/2026-07-23-c1-rung-selection-ev-objective.md` was tagged (Proposed) above as of first authoring; it was ratified Accepted the same day (2026-07-23) and has stood Accepted since — see the ADR's own Status line / Change-history.
**Authored:** 2026-07-23
**Closed:** 2026-07-23 (`FALSIFIED`; fork B elected — c1 rung-selection objective → EV/dollar-day; live rung unchanged, A0b-gated)
**Authors:** Joshua (operator directive) + Claude Code (Opus 4.8, authoring)
**Parent question:** N/A — opened by 08-08-packet **A0 / P0** operator directive (2026-07-23), directive (1)
**Sub-questions opened:** none (the c1 1.00× rung question is packet **A0b**, a *downstream* item, not forked here)
**Loop:** Inquire-phase Pre-Q — closure gated on the §6 locational read of the frozen pre-registration, then the operator's fork election
**Artifact path:** `docs/briefs/Q-BUSTGATE-1-bust-gate-re-derivation.md`
**Pre-registration (frozen method, committed before this derivation is admitted):** [`pre-registration/Q-BUSTGATE-1-verdict-preregistration.md`](pre-registration/Q-BUSTGATE-1-verdict-preregistration.md)

---

## §0 — Rule 0 reads (production-source verification)

Files read **before** authoring, each with a `git log -1` anchor (verified 2026-07-23 on this worktree):

- `docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md` — anchor `be6dda6` (2026-07-13). **The object under re-derivation.** §3: Part A = headline **bust ≤ 3.0%** (daily+static+trailing) + **pass ≥ 50%**, Run-2, $100K band; **rationale = barrier-width analogy** ("3.0% = the $100K band's own barrier width; a deployable edge should bust less often than its barrier is wide"); operator declined the 2%/5% dials. §4 ceiling-mis-set reject + §5 forbidden moves + Trap-#12 (no in-place edit) read in full.
- `docs/briefs/closures/Q-FUNNEL-1-closure-resolved.md` — anchor `b56c5b3` (2026-07-22). The pinned economic evidence. Horizon-robust cell `edge_panel_historical` prefers **1.00× over 0.25×/0.50× on EV/dollar-day at every horizon {126, 252, 504} in both regime halves**; the mechanism is stated verbatim: "at $328/reset the eval-fee cost of busting more often is cheap relative to the funded-payout upside forfeited by under-sizing." Bust of the ratified 0.50× rung = **0.08%**; of 1.00× = **4.37% (H1) / 10.37% (bootstrap-95th)**, "both well over the 3% ceiling."
- `lab/analysis/c1/q_rail_1_2026-07/PHASE4.md` — anchor `43db219` (2026-07-18). Tradeify Select 100K **eval fee $181 list · $111 promo** (JULY, actual-paid); all-in cost-to-first-fill **$328 list / $258 promo**; one-reset contingency **$567 / $497**; activation after pass **$0**.
- `docs/briefs/programs/2026-07-23-tradeify-book-composition.md` — anchor `730bb29` (2026-07-23). Funded mechanics: 2-leg c1 geometry eval pass **63%** / median **8.2 mo**; funded-dead-1y **43%**; renewal-reward chain **$339/acct-mo**; Flex payout **≤ min($4,000, 50% of profit)**, 90/10.
- `core/firm_rules.py` — anchor `f8f8db1` (2026-07-22). `Tradeify_Select_100K`: `dd_type="trailing_locking"`, `max_dd_pct=3.0` ($3,000 EOD trailing / $100K), `profit_target_pct=6.0` ($6,000), `consistency_rule_pct=40.0` (eval-only); `ACTIVE_FIRM="Tradeify_Select_100K"`.
- `docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md` — anchor `549b453` (2026-07-22). §4 falsifier (≥1 candidate clears the bust ceiling on ≥2 of 4 friendly tiers; hard date 2026-11-08). The pre-reg operationalizes this §4.
- `docs/briefs/programs/2026-07-17-0808-packet-delta-and-sequence.md` — anchor `730bb29` (2026-07-23). §0.5 directive (1) [re-derive], (2) [1.00× aim]; §3 P0 [fresh Pre-Q + pre-reg; use actual-paid fee; forbidden: silently editing 3.0%]; §2 step 5 [OPEN A0 blocks any 1.00× rung ADR].

**Context-scope note (Rule-0 sub-rule):** the incumbent ceiling's rationale (barrier-width) was read in its ±20-line surrounding context (survivor-scoring pre-reg §3, lines 139–145), not a single-line grep — the "excludes falsified-book 17.70% / not null-by-construction 1%" qualifiers sit in the same paragraph and are load-bearing for §2 below.

---

## §1 — Context & motivation

The incumbent Part-A eval bust ceiling (**3.0%**) was fixed on 2026-07-13 by a **barrier-width analogy**: the $100K band's own DD barrier is 3.0% wide, so "a deployable edge should bust less often than its barrier is wide" (survivor-scoring pre-reg §3, `be6dda6`). That is a *geometric coincidence*, not an economic derivation — it never priced the actual eval fee against the actual funded upside. On 2026-07-23 the operator directed (packet §0.5 directive 1) that the ceiling be **recalculated from eval-fee-vs-funded-upside economics**, with Q-FUNNEL-1 as the named input — while in parallel (directive 2) aiming to run the c1 book at **1.00×**, a rung the incumbent 3.0% ceiling rejects (1.00× busts 4.37%). The two directives together create a live motivated-reasoning hazard: a re-derivation "from economics" that conveniently produces a ceiling 1.00× clears would launder the aim into the gate. This brief answers the economics question **independently of the 1.00× aim**, under a method frozen before the number was read (Trap #12). Standing doctrine tested: survivor-scoring §4 (the gate); the `concept-not-constant` doctrine (a risk constant changes only via pre-registered re-MC + both-halves regime gate + admitting ADR, [`docs/adr/2026-07-13-dd-protection-concept-not-constant.md`](adr/2026-07-13-dd-protection-concept-not-constant.md)); the down-only lifecycle ladder ([`docs/methodology/strategy_lifecycle.md`](methodology/strategy_lifecycle.md)).

---

## §2 — Prior art / lineage

- **`2026-07-13-prop-survivor-scoring-prereg.md`** (`be6dda6`, FROZEN) — sets the 3.0%/50% ceiling this brief re-derives. Its §3 rationale explicitly balances two rejects: not FXIFY-parity **1%** (null-by-construction on trailing geometry — demotes every program regardless of edge) and comfortably below falsified-book **17.70%** (the locked-book Tradeify-100K transfer). 3.0% was chosen as a *survival* threshold between those poles — never as a fee/upside quantity. **This is the load-bearing prior:** the incumbent number already encodes a survival preference, not economics.
- **`Q-FUNNEL-1-closure-resolved.md`** (`b56c5b3`, RESOLVED) — the pinned economic evidence. Established that on EV-per-dollar-day inclusive of resets + funded payouts, **1.00× (bust 4.37%) strictly beats 0.50× (bust 0.08%)** on the horizon-robust cell, precisely because eval fees are cheap vs funded upside. Its own disposition already flagged: "This does **not** mean 1.00× should replace WATCH-1 0.50× today. The two objectives are genuinely different" — WATCH-1 was ratified against a **P(pass) / bust-floor** objective; funnel-EV is a **different** objective. Q-BUSTGATE-1 is the brief that adjudicates that named tension.
- **`Q-COMPOSE-1-closure-falsified.md`** (2026-07-17) — bust-floor compose falsified (2-leg+ORB boot-95th bust **47.14%** vs ≤3.0%); the disposition "c1 alone @ WATCH-1 0.50×" stands. Confirms the 3.0% gate is treated as a live survival constraint elsewhere in the program.
- **`concept-not-constant` ADR** (2026-07-13) — any change to a `dd_protection`-class risk variable requires pre-registered re-MC + both-halves regime gate + admitting ADR. A successor bust ceiling inherits this chain; this brief cannot itself admit one.
- **Trap #12** (brief-authoring known trap) — a post-ratification ceiling change requires a **fresh** brief + freeze, never an in-place edit of `be6dda6`'s `3.0%`. This brief is that fresh vehicle; it does not touch `be6dda6`.

---

## §3 — Question (Q-BUSTGATE-1)

**Pre-Q gate test:** symptom-only rephrase — "the incumbent 3.0% ceiling's stated basis is a barrier-width geometric coincidence, not the fee-vs-upside economics the operator asked it to reflect; it is unknown whether economics agrees with 3.0%, points to a different number, or is the wrong basis for this gate entirely." No fix baked in (does **not** say "loosen to admit 1.00×").

**Q-BUSTGATE-1:** On what basis is the Part-A eval bust ceiling set, and does an eval-fee-vs-funded-upside economic derivation (pinned to the actual-paid fee and Q-FUNNEL-1's horizon-robust cell) reproduce 3.0%, imply a materially different number, or reveal that fee-vs-upside economics is not the objective a bust *ceiling* should encode?

---

## §4 — Falsifiable hypothesis (H-BUSTGATE)

**H-BUSTGATE:** If the eval-fee-vs-funded-upside-**optimal admissible rung** (the rung Q-FUNNEL-1's horizon-robust `edge_panel_historical` cell prefers on EV/dollar-day, capped at the ladder maximum 1.00×) busts **≤ 3.0%** on the Tradeify Select 100K deployable expression (Run-2), then the incumbent 3.0% is fee-vs-upside-consistent and is **ratified on economic grounds**. **Otherwise** — the economic optimum busts **> 3.0%** — the 3.0% ceiling is **not** a fee-vs-upside quantity; it can only be a survival / P(pass) / firm-relations gate, and the derivation's output is a two-option **operator fork** (retain 3.0% re-justified as survival; or adopt an EV objective via a fresh superseding ADR), with **no in-place edit** to the frozen pre-registration either way.

**Accept H-BUSTGATE → `RESOLVED` (ratify 3.0% on economic grounds) if:** the optimal admissible rung's Run-2 headline bust is **≤ 3.0%** on the horizon-robust cell.
**Reject H-BUSTGATE → `FALSIFIED` (economics does not ratify 3.0%; route to operator fork) if:** the optimal admissible rung's Run-2 headline bust is **> 3.0%** on the horizon-robust cell. Falsifying the *ratification hypothesis* is itself the finding (3.0% is a survival, not an economic, quantity) — the brief's **question** still resolves; only H's ratification claim fails (repo convention: cf. Q-COMPOSE-1 / Q-INVENTORY-1 closed FALSIFIED as legitimate findings).
**`AMBIGUOUS-HOLD` (OPEN) if:** the optimal rung is horizon-**fragile** (its EV-preference direction flips across {126, 252, 504}); the economic optimum is then not robustly identified and cannot decide the fork → 08-08 records OPEN; 3.0% stands; the 1.00× rung ADR (A0b) stays blocked.

**The 1.00× aim is never a trigger in these conditions.** Whether a disposition makes 1.00× admissible is an *output*, never an input to the verdict (frozen pre-reg §D).

---

## §5 — Forbidden moves

- **Tuning the derivation to clear 1.00×** — the single most tempting move given directive (2) runs alongside directive (1). Ruled out by the frozen locational method (pre-reg §B): the read is binary (inside/outside 3.0%) off a *closed* artifact, with **no free tolerance parameter** to bend. Deriving the gate to fit the desired rung is exactly the failure this pre-registration exists to prevent.
- **Editing `3.0%` in `be6dda6` in place** — Trap #12; the incumbent pre-reg is frozen. Any successor is a fresh brief + freeze + `concept-not-constant` chain.
- **Reporting the economic loosening as auto-authorization of 1.00×** — even under the reject branch (economics ⇒ looser gate), 1.00× is admissible on the *bust axis alone*; it still requires the **both-halves regime-robustness gate + an admitting ADR (packet A0b)**. Bust-gate clearance is necessary, not sufficient. Ruled out because it would smuggle a sizing change past the standing `concept-not-constant` chain.
- **Treating the EV-optimum as itself "the new ceiling"** — an EV objective wants a *point optimum*, not a survive-threshold; quoting "4.37%" as the successor bust ceiling conflates two different instruments. Ruled out: if the operator elects fork-B, the successor is an EV objective (a different gate shape), designed in that ADR, not a looser bust number transcribed here.
- **Reading the horizon-fragile `edge_half_panel` cell** to decide the fork — its H1 verdict reverses at horizon 126 (Q-FUNNEL-1 closure). Ruled out by pre-reg §C(1); a fork decided on a horizon-fragile read is a coin-flip dressed as economics.
- **Reading a prop tier's bust via `compute_default_config()['bust_rate']`** (F1 — reports ~0% on trailing geometry) — inherited forbidden move; use `preflight.summarize_outcomes` daily+static+trailing.
- **Outcome-conditional derivation** — e.g., "assume the fee that makes the ceiling land near 3.0%." The fee is the actual-paid pin ($111 promo / $328 all-in), fixed in §A before the read.

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition | Packet-A0 mapping (§2 step 5) |
|---|---|---|---|
| `RESOLVED` | Optimal admissible rung (§B) busts **≤ 3.0%** on the horizon-robust cell | 3.0% is fee-vs-upside-consistent; rationale upgrades barrier-width → economics; no successor, no edit | A0 = "RESOLVED, frozen ceiling **3.0%**"; A0b 1.00× still **blocked** (1.00× busts 4.37% > 3.0%) |
| `FALSIFIED` | Optimal admissible rung busts **> 3.0%** on the horizon-robust cell | H's ratification claim fails: 3.0% is **not** economic. Output = fork **A** (retain 3.0% re-justified as a survival gate) **or** fork **B** (adopt an EV/dollar-day objective via a fresh superseding ADR, `concept-not-constant` chain). Neither fork edits `be6dda6`. | No *successor* ceiling admitted → incumbent **3.0% stands**; treat as the **block** branch — A0b 1.00× rung ADR blocked until the operator elects a fork |
| `AMBIGUOUS-HOLD` | Optimal rung is horizon-fragile (§C(1)) | Economic optimum not robustly identified; cannot decide the fork | A0 = **OPEN**; 3.0% stands; A0b blocked; re-test when a bust-swept re-MC over the full horizon grid is authorized |

**Pre-registered before the number was read** — the frozen method + this table live in [`pre-registration/Q-BUSTGATE-1-verdict-preregistration.md`](pre-registration/Q-BUSTGATE-1-verdict-preregistration.md) §B/§D, committed ahead of the §7 read. §6 is not amended to match the result (Trap #12). **Landed verdict: `FALSIFIED`** (§7 Phase 3) — every §6 branch keeps the incumbent 3.0% in force and the A0b 1.00× rung ADR blocked until an operator act; none of them is a mechanism by which this brief loosens the live gate.

---

## §7 — Execution plan / the derivation (self-executing; closed-artifact read)

This brief is self-executing: the derivation is a **locational read of already-closed artifacts**, not a new run.

- **Phase 0 — Rule-0 reads.** Done (§0).
- **Phase 1 — Identify the fee-vs-upside-optimal admissible rung.** From Q-FUNNEL-1 (`b56c5b3`) horizon-robust cell `edge_panel_historical`: 1.00× ≻ 0.50× ≻ 0.25× on EV/dollar-day at every horizon {126, 252, 504}, both regime halves. Ladder cap = 1.00× (down-only; pre-reg §C(2)). ⇒ **optimal admissible rung = 1.00×.**
- **Phase 2 — Read its Run-2 headline bust.** From Q-FUNNEL-1 (`b56c5b3`): 1.00× busts **4.37% (H1) / 10.37% (bootstrap-95th)** on Tradeify Select 100K. (Ratified 0.50× = 0.08%, for contrast.)
- **Phase 3 — Locational verdict.** 4.37% **> 3.0%** ⇒ the economic optimum sits **outside** the incumbent ceiling. Robustly: the bootstrap-95th (10.37%) is also > 3.0%, and the read is taken on the horizon-robust cell. **⇒ middle row of §6 fires: `FALSIFIED`** (H-BUSTGATE's ratification claim rejected — economics does not justify 3.0%; route to operator fork).

**What the derivation establishes (the substantive finding):** the fee/upside asymmetry is stark — one funded Flex payout (≤ $4,000) against one eval re-attempt ($111 promo, or $328 all-in) is a **≈12–36:1** upside:cost ratio, so eval-fee economics *tolerate* a bust rate far above 3.0% (the EV-optimum already busts 4.37%). Therefore **eval-fee-vs-funded-upside economics do not reproduce 3.0%, and do not point to a tighter number — they point to a looser one, or reveal that "ceiling" is the wrong instrument for an EV objective.** The 3.0% number is retro-explained not by economics but by the **survival** poles the survivor-scoring pre-reg named (above 1%-null, below 17.70%-falsified-book). The re-derivation's honest output is thus a **fork the operator must resolve**, not a new number this brief may transcribe:

- **Fork A — retain the survival gate.** Keep 3.0% (or a survival-derived successor), re-stating its rationale explicitly as a survival / P(pass) / firm-relations / time-cost-of-an-8.2-month-re-eval / MC-understatement-of-breach-clustering threshold — **not** economics. 1.00× stays blocked on this axis. Cheapest, doctrine-preserving.
- **Fork B — adopt an EV objective.** Replace the bust *ceiling* with an EV-per-dollar-day objective in a fresh ADR that supersedes survivor-scoring §4's rationale and names Q-FUNNEL-1 as input. This is a **doctrine change** (P(pass)-gating → EV-gating), not a ceiling edit; it makes 1.00× admissible on this axis but **still** requires the both-halves regime gate + admitting ADR (A0b) before any live rung change.

**This brief takes neither fork.** The pick is an operator/ADR act (packet A0b eligibility), owed at or before 08-08.

- **Phase 4 — (deferred, only if the operator wants a precise economic ceiling number under fork B).** A bust-swept re-MC over the Q-FUNNEL harness at rungs finer than {0.25, 0.50, 1.00}× and horizons {126, 252, 504}, to locate the exact EV-maximizing point and its bust. Not authorized by this brief; named so the fork-B path has a defined next step.

---

## §8 — Verdict pre-registration

Frozen method + decision rule at `docs/briefs/pre-registration/Q-BUSTGATE-1-verdict-preregistration.md`, containing §A pinned inputs, §B locational method, §C robustness guards, §D decision-rule table, §E pinned expectation.

Pre-registration commit hash: `98d0fa6` (frozen 2026-07-23, committed ahead of this brief)
Pre-registration date: 2026-07-23

Because the derivation reads only artifacts closed **before** this brief (Q-FUNNEL-1 closed `b56c5b3` 2026-07-22; fee pin `43db219`; incumbent `be6dda6`), the "freeze before result" property holds by construction — no new result is generated after the freeze. The freeze's live function is to bar tolerance-tuning toward the 1.00× aim (§5), which §B/§D lock regardless of commit timing.

---

## §9 — Closure record format

The landed derivation-layer verdict is `FALSIFIED` (H-BUSTGATE's ratification claim rejected). On the operator's fork pick, produce the closure at `docs/briefs/closures/Q-BUSTGATE-1-closure-falsified.md` recording: the locational read (4.37% > 3.0%), the fork elected (A or B), and — if fork B — a pointer to the superseding ADR that will carry the `concept-not-constant` chain. If the operator defers at 08-08, record `AMBIGUOUS-HOLD (OPEN)` per §6 with the re-test trigger = "authorize the Phase-4 bust-swept re-MC."

---

## §10 — Audit hooks (runnable)

```bash
# §0 anchors still resolve
git log -1 --format='%h %cs' -- docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md   # expect be6dda6
git log -1 --format='%h %cs' -- docs/briefs/closures/Q-FUNNEL-1-closure-resolved.md                       # expect b56c5b3
git log -1 --format='%h %cs' -- lab/analysis/c1/q_rail_1_2026-07/PHASE4.md                                   # expect 43db219

# The incumbent 3.0% is untouched by this re-derivation (Trap #12 intact)
grep -n "3.0%\|≥ 50%" docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md             # 3.0% / 50% still there, unedited

# The pinned locational inputs are quoted, not re-derived
grep -n "4.37%\|10.37%\|0.08%\|edge_panel_historical\|horizon-robust" docs/briefs/closures/Q-FUNNEL-1-closure-resolved.md
grep -n "111\|181\|328" lab/analysis/c1/q_rail_1_2026-07/PHASE4.md | head

# The 1.00× aim is NOT wired into live sizing by this brief (must stay disarmed/WATCH-1)
grep -n "dry_run\|WATCH-1\|0.50" STATE.md docs/notes/rail_build/RUNBOOK.md | head

# This brief was actually re-read at the 08-08 gate (Trap #10 — hooks that never fire)
grep -rn "Q-BUSTGATE-1" docs/SESSIONS.md docs/briefs/programs/2026-07-17-0808-packet-delta-and-sequence.md
```

---

## Verification

```bash
# Discipline checks (mechanical)
python ~/.claude/skills/brief-authoring/scripts/check_brief.py docs/briefs/Q-BUSTGATE-1-bust-gate-re-derivation.md --type inquire
# Expected: all 6 checks PASS

# §0 anchors
git log -1 --format='%h %ci' -- docs/briefs/closures/Q-FUNNEL-1-closure-resolved.md          # b56c5b3
git log -1 --format='%h %ci' -- docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md  # be6dda6

# Cross-reference the locational numbers against the closed source
grep -n "4.37%\|10.37%\|0.08%" docs/briefs/closures/Q-FUNNEL-1-closure-resolved.md
grep -n "111\|328" lab/analysis/c1/q_rail_1_2026-07/PHASE4.md

# Freeze predates this brief's admission (commit ordering)
git log --oneline -- docs/briefs/pre-registration/Q-BUSTGATE-1-verdict-preregistration.md docs/briefs/Q-BUSTGATE-1-bust-gate-re-derivation.md
```

---

## Pre-Lock Checklist (DRAFT brief)

- [x] All §0 paths read and anchored with commit hash
- [x] §3 question passes the symptom-only rephrase test (no "loosen to admit 1.00×")
- [x] §4 hypothesis genuinely falsifiable (binary inside/outside 3.0% trigger)
- [x] §5 forbidden moves genuinely tempting (the 1.00×-laundering move is the live hazard)
- [x] §6 gates have specific numerical triggers (≤3.0% / >3.0% / horizon-fragile)
- [x] §8 pre-registration **committed BEFORE** this brief (freeze-commit `98d0fa6`, 2026-07-23)
- [x] §10 audit hooks are runnable commands
- [x] Verification block executed (`check_brief.py` 6/6 PASS; all pinned numbers cross-verified verbatim)
