# Q-EVALSEQ-1 — pre-registration: 2-leg c1 within-eval front-load sizing schedule

**Type:** Inquire-phase pre-registration (frozen gate; run 08-08-gated). **Authored:** 2026-07-24.
**Working Q-name:** `Q-EVALSEQ-1` (rename-safe; propagate to §-refs + STATE if renamed).
**Source:** advisor Avenue I residue — "a consistency-capped, front-loaded policy" the book-comp
flat-multiplier sweep never tested. **Status:** ⚠ **DORMANT 2026-08-04** — **not on the 08-08 slate** (venue de-scoped; "within-eval" has no eval). Frozen **K=4** policy family and §6 gate survive **unspent** and are re-usable at an F3 venue. Frozen body **byte-unedited**. Nothing is run here.

> **UN-DORMED 2026-08-16 (scoring-only)** — operator P2 mark on the
> [state-policy packet](../programs/2026-08-16-state-policy-scoring-review.md)
> ([closure](../closures/STATE-POLICY-closure-resolved-p2.md)). The dormancy ground
> ("'within-eval' has no eval") lapsed with S1's ratification of the incumbent eval as the
> environment; the subject book remains deployment-barred — this stamp licenses the frozen
> §6 run as a **lever measurement only**, on the incumbent geometry, harness recovered from
> tag `pre-prune-2026-08-08` and anchor-verified before any policy number is read. The
> lapsed "08-08 slate" schedule line is superseded by the P2 mark as the gate token;
> §0–§10 below stay **byte-unedited** (this stamp is header-level, amendment-first,
> same vehicle as the 2026-08-04 dormancy stamp).

---

## §0 — Rule-0 reads

Production read before pre-registering (concrete repo paths):

- [`core/dd_protection.py`](../../../core/dd_protection.py) `calculate_protection(equity, peak,
  lifecycle=None)` (line 207) — the sizing path. `DD_TRIGGER 0.015` / `DD_SCALE 0.40` / `BASE_RISK`
  are frozen; the `lifecycle` factor "MULTIPLIES against BASE_RISK/DD_SCALE — it never edits them
  (axis-separation)". A within-eval schedule is a **fourth multiplicative factor at that same
  risk_pct layer**, not an edit to any constant.
- [`docs/briefs/programs/2026-07-23-tradeify-book-composition.md`](../programs/2026-07-23-tradeify-book-composition.md)
  §2 (flat-multiplier sweep: cash/acct-mo $357→$337→$277→$200 across 0.5×→2×), §5 forbidden move #1
  ("size converts extraction to breach"), §7 (`Q-ORB-SIZE` — the *parked ORB-k* question this is
  distinct from).
- [`core/firm_rules.py`](../../../core/firm_rules.py) `Tradeify_Select_100K` — `dd_type
  "trailing_locking"`, `max_dd_pct 3.0` ($3,000 EOD trailing), `profit_target_pct 6.0` ($6,000),
  `consistency_rule_pct 40.0`, `min_trading_days 3`. The geometry the schedule is reasoned against.

## §1 — Context and subject

**Subject:** the **live 2-leg c1 book** (Striker NAS100/MNQ + Striker DJ30/MYM) — a *within-eval
front-load sizing schedule* `S`: time- or equity-state-varying position sizing that builds cushion
early and throttles later, applied as a risk_pct-layer multiplier (§0). This is **distinct from**:
(i) the **flat-multiplier sweep** already run (constant 0.5×–2× across the whole eval — book-comp §2,
settled negative in §5); and (ii) **`Q-ORB-SIZE`** (contract count `k` on the *parked* ORB leg —
book-comp §7). Q-EVALSEQ-1 is a *schedule* on the two live legs, not a *level* and not an ORB question.

Standing doctrine: sizing is owned by the account-multiplier layer (revocable; multiplies, never
edits locked parameters); lock HELD (99.83/0.17/4.37); the last-ratified deployable rung is WATCH-1
0.50×; B7 unarmed. A schedule is a candidate sizing policy — it changes nothing until a run clears its
gate AND a separate arm GO.

## §2 — Zero-run pre-flight (analytical; empirical half deferred)

**Question the pre-flight scopes (not answers):** can a front-load schedule beat flat sizing for
Select-100K *eval pass*, given the flat sweep already degraded monotonically as size rose?

**The asymmetry that makes this not a foregone "no":** the flat-up sweep raised size *uniformly*, so
it paid the early-breach cost (larger positions when the buffer above the $97,000 trailing floor is
thinnest, at the $100K start) with **no compensating late-game protection** — pure extraction→breach
(§5 #1). A *schedule* front-loads **then de-risks**: after early cushion lifts the EOD peak (and the
$3,000 trailing floor ratchets up under it), the late eval runs at *reduced* size on a *higher* floor.
So the schedule's late leg is strictly safer than flat-flat, while its early leg is strictly riskier
than flat-flat. **Net sign is genuinely ambiguous a priori** — it is the trade of higher early-breach
probability for faster target-reach (fewer days exposed; consistency/activity friction eased) plus a
safer tail. The flat-sweep prior leans the early-breach cost **dominant** (size-up hurt), so the
honest prior is **weakly negative for eval-pass**, with the schedule's late-de-risk asymmetry the only
reason it could net positive where flat-up did not. Under `trailing_locking` specifically, the funded
floor-lock ($100,100 freeze) sits past the eval target, so its benefit accrues mostly to the *funded*
phase, not eval pass — do not over-credit it to the eval gate.

**Empirical half deferred:** quantifying the trade needs the book-comp `inputs/` panel (gitignored,
absent on this worktree) → the bounded MC is 08-08-gated (§6), not run here.

## §4 — Falsifiable hypothesis

**H:** a front-load schedule `S*` on the 2-leg c1 book raises Select-100K eval pass-probability by
**> 5 absolute points** vs the flat WATCH-1 0.50× baseline, **at equal-or-lower bust**.
**Falsifier:** if the pre-registered bounded MC (08-08) shows **≤ 5-point** pass-prob lift OR **higher
bust at matched pass**, H is **falsified** — the within-eval schedule lever is spent (as the flat
level lever already is, book-comp §5), and flat WATCH-1 stands. A lift > 5pt at ≤ bust that also holds
on the both-halves regime split promotes the question to a sizing-policy Pre-Q (not an auto-adopt).

## §5 — Forbidden moves

- **Firing an unregistered MC now.** This brief pre-registers a *question* with a frozen gate; the run
  is 08-08-gated. Running early = the pre-registration-defeating move.
- **Recommending a schedule.** Pre-registration ≠ recommendation; no `S*` is endorsed here.
- **Reopening the flat-sizing conclusion.** Book-comp §5 #1 (flat size-up is negative) stands — this
  is a *different lever* (schedule shape), not a re-litigation of level.
- **Editing `BASE_RISK` / `DD_SCALE` / `DD_TRIGGER`.** The schedule multiplies the risk_pct layer
  (§0 axis-separation); any run that edits a locked constant is out of scope and voids the pre-reg.
- **Crediting the funded floor-lock to eval pass** (§2) — the lock accrues to the funded phase.

## §6 — Gate (frozen)

- **Policy family (K frozen = 4):** the bounded MC tests exactly four canonical schedules, no grid,
  no post-hoc additions — (a) **flat baseline** 0.50× (control); (b) **linear decay** 0.75×→0.25×
  over the eval; (c) **floor-distance-proportional** (size ∝ cushion above the trailing floor,
  capped 0.75×); (d) **step-down-at-cushion** (0.75× until EOD peak ≥ +$1,500, then 0.375×).
  K_intrinsic = 3 non-control policies banked to this question's multiplicity; DSR/placebo per
  `strategy-validation` applied to the best-of-K at read.
- **Pass criterion (binary):** adopt-eligible ⇔ best schedule's eval pass-prob **> baseline + 5pt**
  **AND** bust **≤ baseline bust** **AND** the lift survives the both-halves regime split
  (`regime_robustness_gate`). Any limb fails ⇒ **FALSIFIED**, flat WATCH-1 stands.
- **Schedule:** 2026-08-08 slate (rides the quarterly gate). **Reachability attested:** the book-comp
  harness (`gap_stage*.py`) exists and the panel is procurable locally — this gate is *reachable*
  (not a Q-HARV-0/DISC-CAMP-0 unreachable-frozen-gate).
- **Verdict vocabulary:** RESOLVED (adopt-eligible) / FALSIFIED (lever spent) / AMBIGUOUS (power short).

## §7 — Forked questions

- **`Q-ORB-SIZE`** (book-comp §7) — the parked-ORB `k` sizing question; sibling, **must not be
  conflated**. Q-EVALSEQ-1 is schedule-on-live-2-leg; Q-ORB-SIZE is level-on-parked-ORB.
- **Funded-phase schedule** — whether a *funded*-phase schedule exploiting the $100,100 floor-lock is
  a separate question (the §2 asymmetry that does not accrue to eval pass). Not opened here.

## §10 — Audit hooks

```bash
# 08-08 run (STAGED — do NOT execute before the gate opens):
#   extend the book-comp harness with the 4 frozen schedule policies (K=4, no grid),
#   run the bounded MC, apply DSR/placebo + both-halves regime split to best-of-K.
ls lab/analysis/c1/tradeify_book_composition_2026-07-23/gap_stage1.py
# Baseline this is measured against (flat WATCH-1 0.50x eval pass) lives in the book-comp panels:
ls lab/analysis/c1/tradeify_book_composition_2026-07-23/out 2>/dev/null || echo "panel local-only (gitignored)"
# Axis-separation invariant (must stay true — the schedule never edits these):
rg -n "DD_TRIGGER = 0.015|DD_SCALE = 0.40" core/dd_protection.py
```

## Verification

§0 cites production paths incl. the exact sizing function ✓ · §4 `H:` + falsifier, binary ✓ ·
§5 lists moves genuinely tempting (run-early; recommend; reopen flat; edit constants) ✓ ·
§6 K frozen = 4, binary criterion, reachability attested, 08-08-scheduled ✓ · §10 runnable + staged
(not executed) ✓ · distinct-from-Q-ORB-SIZE forced (§1, §7) ✓ · empirical half honestly deferred (§2) ✓.
