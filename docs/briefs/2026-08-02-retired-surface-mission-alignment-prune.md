# 2026-08-02 — Retired-surface mission-alignment prune (two-pass audit + Slice 1)

**Status:** PARTIAL — Slice 1 CODE_LANDED (cd8b617f / PR #612); Packets A–E SHIPPED on `cursor/prune-packets-a-e-mission-alignment`; Packet F DEFERRED (separate operator ruling)
**Authored:** 2026-08-02
**Authors:** Joshua (operator GO on Slice 1) + Cursor Cloud Agent (two-pass audit + Slice 1 execution + this brief)
**Parent question:** N/A — this **is** the parent disposition. It is not a Pre-Q into markets; it is a Delete/Simplify ruling on requirements that no longer fit the live mission.
**Loop:** Ruling / disposition — closure when every packet in §6 is dispositioned (ship / decline / defer-with-date).
**Artifact path:** `docs/briefs/2026-08-02-retired-surface-mission-alignment-prune.md`
**Related:** [`docs/adr/2026-07-11-fxify-ops-surface-retirement.md`](../adr/2026-07-11-fxify-ops-surface-retirement.md) Addendum 2026-08-02 · [`docs/briefs/handoffs/2026-07-24-cursor-handoff-dead-surface-retirements.md`](handoffs/2026-07-24-cursor-handoff-dead-surface-retirements.md) (broader orphan slate still GO-gated) · monorepo ADR H3 ("a gate that never bites decays to ceremony") [`docs/adr/2026-06-05-monorepo-layer-boundaries.md`](../adr/2026-06-05-monorepo-layer-boundaries.md) §4

---

## §0 — Rule 0 reads (production-source verification)

Anchors verified 2026-08-02T17:10Z on branch `cursor/prune-retired-fxify-nt8-surfaces-8f35` at `cd8b617f` (post-Slice-1 commit). Form: `git log -1 --format='%h %ci' -- <path>`.

| Path | Anchor | What was verified |
|---|---|---|
| `scripts/validate_alert_payloads.py` | **absent** after `cd8b617f` | Was Copygram→FXIFY Gate 1; `ops/c1_rail/crosstrade_payload.py` never imported it (consumer sweep: only self + `check_boundaries` registry) |
| `core/config/symbol_inventory.toml` | **absent** after `cd8b617f` | Companion inventory; deleted with validator |
| `ops/c1_rail/crosstrade_payload.py` | pre-existing on `main` | Live c1 payload builder — sole payload contract |
| `ops/prop_envelope_default.md` | `cd8b617f` | E6 now Option C / disarmed; NT8 dormant fallback |
| `docs/notes/rail_build/RUNBOOK.md` | `cd8b617f` | Pre-session checklist = B7 arming days only, not daily `DRY_RUN=false` |
| `docs/methodology/regime_robustness_gate.md` | `cd8b617f` | Pin → `tests/core/test_mc_synthetic_engine.py` + `docs/mc_anchor_history.md`; deleted `test_mc_anchors.py` confirmed absent |
| `.claude/skills/trade-csv-reconcile/SKILL.md` | `cd8b617f` | Mission framing; DXTrade/`$200K` historical |
| `docs/operational_rules.md` | `e95f41d6` 2026-08-02 | Rule 4 still cites weekly review (L45); Rule 8.5 still lists `accounts` / `cli` (L232) |
| `.claude/skills/ooda-loop/SKILL.md` | `1772f26f` 2026-07-08 | FIRE-alert manual-execution playbook still live (L112, L118) |
| `.claude/skills/prop-firm-challenge/SKILL.md` | `cf757506` 2026-07-28 | Header notes retirement; body still teaches FIRE lots + `ACTIVE_FIRM` as switch (L73, L175, L231, L293) |
| `core/firm_rules.py` | Phase-4 deletion on `main` | `ACTIVE_FIRM` **absent** as a live assignment (comment-only / historical mentions) |
| `scripts/githooks/pre-commit` | `e0fcab7a` 2026-07-31 | Gates 1–12 always-on inventory (data manifests already staging-conditional) |
| `docs/briefs/handoffs/2026-07-24-cursor-handoff-dead-surface-retirements.md` | `58d803fd` 2026-07-24 | Operator GO line still unfilled; Copygram limb discharged by Slice 1 addendum; orphans (`inactivity_simulator`, `migrate_adr_headers_m1`, `mc-anchors`, …) still present on disk |
| `STATE.md` | `4279853d` 2026-08-02 | Operator-hours = binding resource; ≤5 queue; B7 Stage 1 / M1 dominate |
| `docs/adr/2026-07-22-challenge-era-substrate-retirement.md` | on `main` | Phase 2 deleted accounts/cli; Phase 3 retired Pepperstone executable pin; Phase 4 deleted `ACTIVE_FIRM` |

Cheap falsifier (pre-authoring): `test ! -f scripts/validate_alert_payloads.py && test ! -f core/config/symbol_inventory.toml` → both gone; `rg -n "Option C|disarmed" ops/prop_envelope_default.md docs/notes/rail_build/RUNBOOK.md` → Slice 1 language present; `rg -n "FIRE alert|accounts.*/.*cli|weekly review" .claude/skills/ooda-loop/SKILL.md .claude/skills/prop-firm-challenge/SKILL.md docs/operational_rules.md` → deferred surfaces still present.

---

## §1 — Context & motivation

Mission (canonical posture in [`CLAUDE.md`](../../CLAUDE.md)): **c1 Tradeify Select 100K rail** (Option C: TV→listener→CrossTrade→Tradovate), currently **disarmed**; research = prop-portfolio + ORB-MNQ; locked Pine untouched; self-funded parked; MYM ORC terminal; FXIFY/manual CFD retired. [`STATE.md`](../../STATE.md) names **operator-hours** as the binding resource.

A two-pass repo-wide search (2026-08-02) looked for requirements that (a) no longer align with that mission or (b) overcomplicate it relative to operator-hour scarcity. Pattern that emerged: **process gates and agent playbooks accreted around a live CFD desk that no longer exists**, while the live path is a disarmed Tradovate rail.

Slice 1 (dead FXIFY/NT8 surfaces) was operator-authorized and shipped in PR #612. This brief is the durable record of both passes, the Slice 1 disposition, and the remaining prune packets — so the next session does not re-derive the inventory.

---

## §2 — Prior art / finding inventory (both passes)

### Pass 1 — process / board / skill lag (summary)

| # | Finding | Severity | Disposition |
|---|---|---|---|
| P1-1 | ~12 always-on pre-commit gates | HIGH | **Defer** — path-stage later; keep capital/Pine/data always-on |
| P1-2 | Instrument-profile gate ceremony falsifier still open | MED | **Defer** — ADR H3 falsifier owns it at programme-audit |
| P1-3 | Pine hard-fail in partial worktrees | HIGH | **Defer** — M-9 intentional; sync pre-flight exists (Rule 9) |
| P1-5 | Rule 8.5 still lists `accounts` / `cli` | HIGH | **Packet B** below |
| P1-6 | Rule 4 still says “log in the weekly review” | MED | **Packet B** below |
| P1-7 | OODA + prop-firm FIRE/DXTrade playbooks | HIGH | **Packet A** below |
| P1-8 | c1-rail skill still cites `ACTIVE_FIRM` | LOW–MED | **Packet A** (same skill pass) |
| P1-9 | SESSIONS / STATE / CLAUDE Open-next triple-carry | HIGH | **Defer** — living-board prune already owed on Open/next |
| P1-10 / P1-18 | Decompound A5 + vacuous Call-4 on 08-08 | HIGH | **Defer** — operator-hour competitor; needs separate ruling, not silent demote — ⚠ *see Addendum 2026-08-29 above §6's "Remaining packets" table: A5 discharged same-day by operator ruling, not deferred* |
| P1-13 | Sentinel PREREG ~2/3 false positives | MED | **Keep** — already named in Rule 8.7; fail-open |

Already correctly rejected (do not re-propose): status-grammar gate (`docs/methodology/rejected_signals.md`); dual central `profiles.yaml`.

### Pass 2 — retired CFD/NT8 contracts still binding (summary)

| # | Finding | Severity | Disposition |
|---|---|---|---|
| P2-1 | Copygram/FXIFY `validate_alert_payloads` + inventory + tests | HIGH | **Slice 1 — SHIPPED** (`cd8b617f`) |
| P2-2 | `trade-csv-reconcile` always DXTrade/`$200K`/Alchemy | HIGH | **Slice 1 — SHIPPED** |
| P2-3 | Prop envelope E6 → TV→CrossTrade→NT8 | HIGH | **Slice 1 — SHIPPED** |
| P2-4 | RUNBOOK “every active day” NT8 + `DRY_RUN=false` | HIGH | **Slice 1 — SHIPPED** |
| P2-5 | `regime_robustness_gate.md` pins deleted `test_mc_anchors.py` | HIGH | **Slice 1 — SHIPPED** |
| P2-6 | sync-skills hook + post-merge `make sync-skills` | HIGH | **Packet C** below |
| P2-7 | CI workflows inert; stale regime-check comment | MED | **Packet C** |
| P2-8 | Notion still live brief destination / Daily Execution skill | MED | **Packet D** (overlaps 07-24 handoff notion limb) |
| P2-11 | Programme-audit calendar portfolio re-MC | MED | **Defer** — skill already says calendar without evidence is ceremony |
| P2-12 | Sentinel Tier-2/3 promotion before quarterly slate | MED | **Defer** — hygiene; does not advance B7 |
| P2-16 | CC/Cursor handoff brief for small tooling | MED | **Keep** — surface-allocation ADR; do not weaken locked-surface gate |

### Slice 1 shipped (this branch / PR #612)

- `git rm` `core/config/symbol_inventory.toml` + `scripts/validate_alert_payloads.py` + `tests/test_validate_alert_payloads.py`
- ADR addendum on FXIFY-ops retirement ADR (Copygram estate only; broader 07-24 slate **not** discharged)
- `trade-csv-reconcile` mission framing; envelope E6 + RUNBOOK Option C; regime-gate pin repair
- Registry: `REPO_MAP.md`, `PIPELINES.md`, `scripts/check_boundaries.py`

---

## §3 — Question

**Pre-Q gate test (symptom-only):** *"Requirements and playbooks still bind a retired CFD/NT8 desk and compete with B7/M1 for operator attention. Which obligations are load-bearing for the live mission, and which are ceremony or dead-surface lag?"*

**Q-PRUNE-1:** Which standing requirements (gates, skills, rules, runbooks, methodology pins) are misaligned with the c1/ORB mission or overbearing relative to operator-hour scarcity, and what is the Delete/Simplify disposition for each?

---

## §4 — Falsifiable hypothesis

**H-PRUNE-1:** A material set of standing requirements still encode the retired FXIFY/Copygram/DXTrade/NT8-as-live path (or challenge-era `$200K` ceremony) as if it were the current mission, and pruning those surfaces **does not** weaken c1 rail safety, locked Pine, or `dd_protection`.

**Falsifier:** H-PRUNE-1 is **falsified** if any of the following holds after Slice 1 (or a later packet):

1. c1 payload validation regresses — i.e. `ops/c1_rail/crosstrade_payload.py` (or the listener) depended on the deleted Copygram validator / inventory (consumer sweep finds a live import), **or**
2. A Slice-1 doc/skill change causes an attended B7 session to arm without the M1 / `armed_until` / disarm obligations that RUNBOOK and the monitoring ADR already require, **or**
3. The regime-robustness gate can no longer be located / run because the pin rewrite points at a nonexistent file.

**Accept H (Slice 1 holds)** if: consumer sweep stays empty for the deleted estate; RUNBOOK still requires M1 `RESOLVED` + operator GO before `dry_run=false`; `test -f tests/core/test_mc_synthetic_engine.py` is true; and no Pine / `dd_protection` / sizing-host law changed in the prune commit.

**Ambiguous** if a later packet (A–D) is declined by the operator because the surface is judged still load-bearing for a dated reason — record the decline on that packet; do not stretch H to cover declines.

---

## §5 — Forbidden moves

- **Silent delete of the full 2026-07-24 orphan slate** under cover of Slice 1. That handoff's GO line still gates `inactivity_simulator`, `migrate_adr_headers_m1`, `mc-anchors`, GBPUSD RUNBOOKs, `lab/codification/`, and the notion skill. Slice 1 discharged **only** the Copygram validator estate.
- **Weakening M1 / arming / `armed_until` / disarm rules** while “simplifying” the RUNBOOK. Option C / disarmed-default language must preserve the 07-31 self-brick lesson and the monitoring ADR gate.
- **Editing locked Pine, `dd_protection` literals, firm-tier risk %, or c1 sizing law** as part of a prune. Out of scope.
- **Demoting Decompound-HOLD A5 or Call-4 by drive-by edit** without an operator ruling. Those compete with B7 for attention, but they are dated falsifier limbs — Rule 11 applies (back-propagate with re-arm conditions), not silent deletion. ⚠ *See Addendum 2026-08-29 above §6's "Remaining packets" table — A5 itself was struck outright by a same-day operator ruling on a different ADR; this forbidden-move clause is unaffected (it was never the vehicle that struck it) but reads stale on its own if taken to mean A5 is still pending.*
- **Path-staging all pre-commit gates in the same PR as skill rewrites** without measuring which gates actually bite. Accretion is real; so is the incident history that earned M-9 / boundary / status-consistency.
- **Re-proposing the rejected status-grammar state machine** (`rejected_signals.md` 2026-07-29).
- **Treating this brief as permission to skip session-log / Rule 7** while pruning living boards — prune by deleting discharged lines, not by inventing a second owner table.

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` | Every packet in the table below is SHIPPED, DECLINED (with dated reason), or DEFERRED-WITH-DATE; H-PRUNE-1 Slice-1 falsifier limbs 1–3 still clear | Close this brief to `docs/briefs/closures/`; point SESSIONS Open/next at remaining DEFERRED dates only |
| `PARTIAL` (current) | Slice 1 shipped; ≥1 packet still OPEN | Keep this brief hot; next prune PR links here |
| `FALSIFIED` | Any §4 falsifier limb fires | Revert or repair the offending prune; do not continue packets until H is re-established |
| `AMBIGUOUS` | Operator holds a packet without ship/decline and without a review date | Escalate — AMBIGUOUS without a date becomes living-board noise |

> ⚠ **SUPERSEDED 2026-08-02** (same day this brief's Pass-1 table was authored): **Decompound A5
> was not deferred pending "Call-4 vs B7 sequencing"** — it was **struck outright by operator
> ruling**, per [`docs/adr/2026-08-02-pepperstone-feed-retirement.md`](../adr/2026-08-02-pepperstone-feed-retirement.md)
> §2-B/§2-D. Discharge corroborated at
> [`docs/briefs/2026-07-17-0808-packet-delta-and-sequence.md`](2026-07-17-0808-packet-delta-and-sequence.md)
> §0. **The actual live open question is a build-gate-scope ruling for A5's venue-native successor
> monitor**, tracked at `STATE.md`'s "Forward regime monitor / decompound limb-2 successor —
> Q-MONSURF-1 M-A" line. **Packet F's Call-4 limb is unaffected** and continues under its own
> track ([`docs/superpowers/plans/2026-08-23-call4-beta-cohesion-implementation.md`](../superpowers/plans/2026-08-23-call4-beta-cohesion-implementation.md),
> landed 2026-08-23). Packet F's disposition cell below carries a matching one-clause note; the
> Pass-1/Pass-2 tables and §5 above are otherwise unedited (Rule 14) — see Change history
> 2026-08-29.

### Remaining packets (A–E SHIPPED this branch; F still GO-gated / separate ruling)

| Packet | Scope | Suggested shape | Blocks |
|---|---|---|---|
| **A — Agent FIRE playbooks** | Rewrite `.claude/skills/ooda-loop/SKILL.md` + `.claude/skills/prop-firm-challenge/SKILL.md` (+ `c1-rail` `ACTIVE_FIRM` pointer) off manual FIRE/DXTrade; point live execution at `c1-rail` only; keep historical CFD facts labeled HISTORICAL/DORMANT | Skill-only PR; no capital path | Agents loading illegal action set |
| **B — Operational rules dead pointers** | Rule 4: replace weekly-review logging with ledger / SESSIONS / c1 telemetry owner; Rule 8.5: replace `accounts`/`cli` with c1 sizing host + `firm_rules`/`dd_protection`/`lifecycle` | `docs/operational_rules.md` edit + edit-log entry | Lock checklists chasing deleted CLI |
| **C — Sync-skills / CI theater** | Soften post-merge sync-skills obligation for Cloud/worktree; fix `.github/workflows/tests.yml` stale quarterly-regime comment (C2→C0 retired) | Docs + workflow comment; optional hook skip-if-worktree already exists — verify | Operator tax + stale duty signal |
| **D — 07-24 orphan slate residue** | Execute or explicitly decline remaining limbs of [`2026-07-24-cursor-handoff-dead-surface-retirements.md`](handoffs/2026-07-24-cursor-handoff-dead-surface-retirements.md) under a filled GO line | Deletion PR per that handoff | Spent one-shots still greppable as live |
| **E — Living-board prune** | STATE / SESSIONS Open-next / CLAUDE posture: delete discharged lines; no value restatement (Rule 7) | Docs-only; already on Open/next | Triple-carry every session |
| **F — 08-08 vacuous limbs** | Separate operator ruling: Call-4 / Decompound A5 vs B7 sequencing (Rule 11 if darkened) | Ruling brief or ADR addendum — **not** this prune PR | Operator-hour collision with B7 Stage 1 |

**
### Packet dispositions (2026-08-02 execute pass)

| Packet | Disposition | Notes |
|---|---|---|
| A | **SHIPPED** | OODA + prop-firm-challenge + c1-rail off FIRE/`ACTIVE_FIRM` live path |
| B | **SHIPPED** | Rule 4 → SESSIONS/c1 telemetry; Rule 8.5 → firm_rules/dd_protection/lifecycle/c1 sizing host |
| C | **SHIPPED** | post-merge sync-skills optional; tests.yml C2→C0 comment retired |
| D | **SHIPPED** | 07-24 GO line filled; orphans + codification + repo notion skill deleted; ADR addenda |
| E | **SHIPPED** | SESSIONS Open/next + brief status; discharged prune lines removed from carry |
| F | **DEFERRED** | Call-4 / Decompound A5 vs B7 sequencing — separate operator ruling (not this PR). ⚠ *A5 limb discharged by the Addendum 2026-08-29 above (struck outright same-day, not deferred); Call-4 limb unaffected, continues under its own track.* |

Standing keep (not packets):** M1 item 5 / B7 Stage 1 desk card; Rule 13 venue-fact convention; surface-allocation handoff gate for locked surfaces; Pine/data manifest gates; instrument-ledger collision Rule 10 (cost-geometry Pepperstone assumption may get a futures note under Packet A/B if touched — do not gut the collision rule).

---

## §10 — Audit hooks (runnable)

```bash
# Slice 1 — deleted estate stays gone; no new executable consumer
test ! -f scripts/validate_alert_payloads.py
test ! -f core/config/symbol_inventory.toml
test ! -f tests/test_validate_alert_payloads.py
rg --no-ignore -l "validate_alert_payloads|symbol_inventory" --type py \
  | grep -vE 'check_boundaries|test_validate_alert' || true
# expect: empty (or retirement-pointer prose only in non-.py)

# Slice 1 — live payload + Option C language
rg -n "Option C|disarmed" ops/prop_envelope_default.md docs/notes/rail_build/RUNBOOK.md
test -f ops/c1_rail/crosstrade_payload.py
test -f tests/core/test_mc_synthetic_engine.py
rg -n "test_mc_anchors" docs/methodology/regime_robustness_gate.md  # expect empty

# Packet A still owed (expect hits until shipped)
rg -n "FIRE alert|ACTIVE_FIRM is the single switch" \
  .claude/skills/ooda-loop/SKILL.md .claude/skills/prop-firm-challenge/SKILL.md

# Packet B still owed
rg -n "weekly review|accounts.*/.*cli|/ \`accounts\`" docs/operational_rules.md

# Packet D — orphans still on disk until GO
test -f scripts/inactivity_simulator.py && echo ORPHAN_INACTIVITY
test -f scripts/migrate_adr_headers_m1.py && echo ORPHAN_MIGRATOR
test -f .claude/commands/mc-anchors.md && echo ORPHAN_MC_ANCHORS

# Gates (regression)
python scripts/check_boundaries.py
python scripts/check_skill_refs.py --all
python scripts/check_brief.py docs/briefs/2026-08-02-retired-surface-mission-alignment-prune.md --type brief
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-02 | Brief authored; Slice 1 recorded CODE_LANDED (`cd8b617f` / PR #612); packets A–F opened | Cursor Cloud Agent |
| 2026-08-29 | **Addendum (Rule 14 correction, no rewrite).** Decompound A5 was struck outright the same day this brief's Pass-1 table was authored (`docs/adr/2026-08-02-pepperstone-feed-retirement.md` §2-B/§2-D), not "deferred pending Call-4 vs B7 sequencing" as §2's P1-10/P1-18 row, §5's A5 forbidden-move clause, and §6's Packet F disposition still read. Reader-intercept added above §6's "Remaining packets" table plus one-line pointers at both stale sites; Packet F disposition cell gained a matching clause. The live open question is now a build-gate-scope ruling for A5's venue-native successor monitor (`STATE.md` "Forward regime monitor / decompound limb-2 successor — Q-MONSURF-1 M-A"); Call-4 continues unaffected under its own landed track. Pass-1/Pass-2 tables and §5 body left byte-identical otherwise. | Claude Code (brief-corpus decay audit remediation) |
