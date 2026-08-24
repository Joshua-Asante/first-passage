# Viable-strategy surface consistency — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:executing-plans. Checkbox
> (`- [ ]`) syntax for tracking. One commit per packet unless a packet is a single
> sentence on a file another packet already has open — then fold, and say so.

**AUTHORIZATION:** **GO 2026-08-24.** Operator: `GO` on this plan. Packets 1–5
execute; Packet 0 stays operator-only. `queue-exception: operator asked to plan
the inconsistency repair on #1's owner artifacts`. This packet is hygiene of the
[`viable-strategy sequence`](2026-08-23-viable-strategy-sequence-overview.md)
owners so queue `#1` can be read without contradiction. It is **not** a Phase B
GO, **not** an A2 `sims_per_seed` ratification, and **not** an R3 / arming GO.

**Goal:** make the six named surfaces agree about what is settled, residual,
killed, or still awaiting GO — without inventing any of those statuses.

**Do not:** execute Phase B · sign off A2's N-reduction · reopen B3 · flip the
sequence-overview `AWAITING GO` (Phase B GO is still unpaid) · rewrite the
Q-FIRMEOD-1 verdict · touch Pine / `dd_protection` / allocations / the rail.

---

## What was checked and does not hold

Leave these alone (operator already cleared them):

- An apparent "Phase B" naming collision in `docs/SESSIONS.md` — both mentions
  are disambiguated in-context.
- An apparent F1-ruling dependency on a still-`Proposed` addendum — the ADR
  explicitly disclaims that dependency.

---

## Standing elections (this plan — do not re-derive at execute time)

| # | Question | Election | Why |
|---|---|---|---|
| E1 | May this plan ratify A2's `sims_per_seed=500` vs frozen 10,000? | **No.** Propagate the residual. Sign-off is a named operator ask, not a packet. | Inventing the sign-off is the same defect as the s4 banner (body ran ahead of the authorization line). Owner of the residual: [`A2 RESULTS §4`](../../../lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS.md). |
| E2 | Is Phase B still the next doable packet? | **Yes**, with the region as a *disclosed-N screen*, not a ratified frozen-N map. | Queue placement is not a phase GO (already on the `#1` row). The residual is a caveat on the input, not a blocker of the packet. |
| E3 | What is B3's status? | **KILL** (POWER, category-inherited from F5/D3). Phase B proceeds B1/B2 only. | [`A1 audit §6`](../../notes/audits/2026-08-23-kill-register-attribution-audit.md) at 2026-08-23 17:46. A2 RESULTS §8, authored later the same day, never absorbed the kill. |
| E4 | Where does a Phase-C candidate start Phase D? | **TNEC-1 intake (Phase C step 8).** Overview adopts Phase D's own trigger. | Phase D's document is the owner of its start gate. "Reaches Pine" is step 6 — two steps earlier than "a Phase-C survivor." |
| E5 | How is a stale closure grep citation repaired? | Pointer-only currency note + count-stable hook. Do not rewrite the verdict. | Closures stay byte-unedited on the finding (Trap #12). The Iterate block already has a 2026-08-23 pointer-only update — same shape. |
| E6 | Same-class banner lag not in the original five? | Repair Phase A's `AUTHORIZATION` and the overview Phase A / ∥ rows. Do **not** flip the overview Status. | Same defect as item 4 (banner `AWAITING GO`, body already executed). Sequence-level `AWAITING GO` is still true (Phase B unpaid). |

---

## Packet 0 — Named operator ask (not executed by this plan)

**A2 N-reduction sign-off.** The disclosed deviation is `sims_per_seed` 500
(N=1,500) vs the frozen 10,000 (N=30,000), seeds/horizon untouched, full-N
corner subset 8/8 agree, MARGINAL-band subset 0 confident-verdict flips
([`RESULTS §4` / `§4.1`](../../../lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS.md)).
The 2026-08-23 decision-index bullets already name this as the one item still
open after R1's Gate-line ratification.

- [ ] **Operator only.** Accept the disclosed reduction as the published region's
  N, **or** decline and require a frozen-N re-sweep before Phase B treats the
  region as a screen. Until then, Packets 1–5 land the caveat; they do not
  close this ask.

---

## Packet 1 — Propagate the A2 residual (item 1)

**Defect:** [`STATE.md`](../../../STATE.md) queue `#1` (L57) says Phase A
executed and the region is `FEASIBLE ≥~65-70%`, unblocking Phase B. The same
page's decision index (L76–77) says A2's `sims_per_seed` reduction is still
awaiting operator sign-off. [`Phase B`](2026-08-23-viable-strategy-phase-b-mechanism-supply.md)
Inputs take "Phase A2's feasible-shape region" as a settled pre-check with no
mention of §4.

**Repair (E1+E2):** one clause on every consumer; do not delete the
decision-index residual until Packet 0 fires.

- [x] **`STATE.md` queue `#1`.** Keep "A1+A2 executed / region published /
  Phase B next doable (GO unpaid)." Add one clause: A2 `sims_per_seed`
  500-vs-frozen-10,000 residual still unsigned — link
  [`RESULTS §4`](../../../lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS.md).
  40-word cap: prefer the link over restating N.
- [x] **Phase B Inputs line.** After "Phase A2's feasible-shape region
  (pre-check)", add "disclosed-N residual unsigned — RESULTS §4." B4 lane
  already voided by empty revival list — say so in the same Inputs sentence
  if it is still implied live.
- [x] **Decision index.** Leave the 2026-08-23 residual bullets. Do not
  "refresh" them into a new newest-15 row (that would look like a new
  decision). The queue-row clause is the pointer the next reader hits first.

**Falsifier:** `rg -n "sims_per_seed|disclosed-N|RESULTS §4" STATE.md docs/superpowers/plans/2026-08-23-viable-strategy-phase-b-mechanism-supply.md`
returns a hit on both the queue row and Phase B Inputs. Phase B no longer
reads as if the region were a frozen-N settled input.

---

## Packet 2 — Retire B3 as a live lane (item 3)

**Defect:** A1 audit §6 ruled B3 **KILL** and said "Phase B proceeds with
candidates B1/B2 only." A2 RESULTS §8 (later the same day) still lists
`B1.4 / B2.3 / B3.2` as live card-precheck rows. Phase B still carries a full
unchecked B3 lane. `docs/rejected_candidates.md` has no B3 / buyback-blackout
row. Phase C's "Sleeve rule (B3-class candidates)" names a killed lane as if
it were the class.

**Repair (E3):** mark killed in situ; write the kill where the next reader
looks; keep the sleeve *rule* (it is a standing class rule).

- [x] **Phase B.** Banner Lane B3 `KILL` with a one-line cite of A1 audit §6
  (POWER, F5/D3). Check or strike B3.0–B3.2 as not-to-run. Do not delete the
  mechanism paragraph (historical record). Provenance line that says
  "candidate lanes B1–B3" → "B1–B2 live; B3 KILL (A1)."
- [x] **A2 RESULTS §8 (ii).** Drop B3.2 from the live pre-check list. Rewrite
  the B3 bullet as: killed at A1 2026-08-23 (cite audit §6); the cadence
  observation is historical, not a live pre-check. Update the §0 row that
  cites Phase B as "three Phase-B lanes."
- [x] **`docs/rejected_candidates.md`.** Append a short pre-G0 row:
  `buyback-blackout abstention × MNQ` — authoritative artifact = A1 audit §6;
  class POWER; category-inherited from F5/D3; re-proposal bar = a materially
  different magnitude argument than F5's three failed instances (A1's own
  words). HTML trailer required. No new closure (naming ≠ opening; the kill
  already happened).
- [x] **Phase C.** Retitle `## Sleeve rule (B3-class candidates)` →
  `## Sleeve rule`. One parenthetical: B3 itself is KILL (A1); the rule
  still binds any future sleeve.

**Falsifier:** `rg -n "B3\.2|B1\.4 / B2\.3 / B3\.2|candidates B1/B2 only" lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS.md docs/superpowers/plans/2026-08-23-viable-strategy-phase-b-mechanism-supply.md docs/rejected_candidates.md`
— RESULTS no longer lists B3.2 as a live card-precheck; Phase B banners
KILL; registry has a buyback-blackout / B3 row.

---

## Packet 3 — Banner / body authorization lag (item 4 + same-class)

**Defect:** [`parallel-s4-firm-repair`](2026-08-23-viable-strategy-parallel-s4-firm-repair.md)
L6 still banners `AUTHORIZATION: AWAITING GO` and names "a fresh Q + operator
GO" as the open condition. That condition was met 2026-08-23: R1 is
`RESOLVED — WITH NAMED RESIDUAL` with recorded ratification; R2 is `RESOLVED`
at `65dc17b`. R3 is correctly still open (gated on a Phase-C survivor). Four
later commits updated the checklist and never touched the banner.

Same class, found while reading the owners (not in the original five; E6):

- [`phase-a-target-derivation`](2026-08-23-viable-strategy-phase-a-target-derivation.md)
  L6: `AWAITING GO` / "not yet given" — STATE decision index records Phase A
  GO executed. A1/A2 checkboxes still `[ ]`. A3 is voided (empty revival list).
- Overview Phase A row: "operator GO (offered, not yet given)."
- Overview ∥ row: "operator GO (fresh Q per the Q-FIRMEOD-1 closure bar)."

**Repair:** banners match body. Sequence-level Status stays `AWAITING GO`.

- [x] **s4 plan banner.** Replace `AWAITING GO` with: R1+R2 GO executed
  2026-08-23 (R1 ratified `WITH NAMED RESIDUAL`; R2 `RESOLVED`). R3 remains
  gated on a Phase-C survivor. Keep the "naming ≠ opening" sentence as
  history, not as the live condition.
- [x] **Phase A banner + checkboxes.** `AUTHORIZATION:` A1+A2 GO executed
  2026-08-23; A3 voided (empty revival list). Mark A1/A2 tasks `[x]`; mark
  A3 `[x]` as voided-not-run (one-line why).
- [x] **Overview Phase A row.** Gate: "A1+A2 executed 2026-08-23; A3 voided."
- [x] **Overview ∥ row.** Gate: "R1+R2 landed 2026-08-23; R3 gated on a
  Phase-C survivor."

**Do not change:** overview Status `AWAITING GO` · Phase B `AUTHORIZATION:
AWAITING GO` (per-lane; GO unpaid) · pain-point charter lines that call the
*sequence* `AWAITING GO` (still true).

**Falsifier:** `rg -n "AUTHORIZATION: .AWAITING GO" docs/superpowers/plans/2026-08-23-viable-strategy-parallel-s4-firm-repair.md docs/superpowers/plans/2026-08-23-viable-strategy-phase-a-target-derivation.md`
is empty. Overview Phase A / ∥ rows no longer say "not yet given" / "fresh Q."
Overview Status and Phase B banner still say `AWAITING GO`.

---

## Packet 4 — Phase D start gate (item 5)

**Defect:** Overview Phase D row names its gate as "starts automatically when
a candidate reaches Pine" (Phase C step 6) and its dependency as "a Phase-C
survivor" (Phase C step 8 / TNEC-1). Phase D's own document sides with the
later definition. Latent — nothing has reached either point.

**Repair (E4):** overview adopts the owner. **Folded into Packet 3** — single
sentence on a file Packet 3 already had open.

- [x] **Overview Phase D row.** Gate: "starts automatically when a candidate
  enters TNEC-1 intake (Phase C step 8); arming GOs operator-only."
  Dependency stays "a Phase-C survivor." Folded into Packet 3 (same file).
- [x] **Phase D / Phase C.** No body edit unless a sentence still says
  "reaches Pine" as the D trigger (none found on read). Phase C exit already
  says TNEC-1 → Phase D.

**Falsifier:** `rg -n "reaches Pine" docs/superpowers/plans/2026-08-23-viable-strategy-sequence-overview.md`
is empty. Phase D AUTHORIZATION / Input still say TNEC-1 intake.

---

## Packet 5 — Q-FIRMEOD-1 reproducibility citation (item 6)

**Defect:** [`Q-FIRMEOD-1-closure-falsified.md`](../../briefs/closures/Q-FIRMEOD-1-closure-falsified.md)
§10 prints `grep -n '"dd_type": "trailing"' core/firm_rules.py` →
`92,104,116,128,140,508,524   [7 hits, confirmed]`. Re-run 2026-08-24:

```
122, 134, 146, 158, 170, 600, 616
```

Seven hits still. Underlying finding is fine and reconciled at R1/R2. The
citation is stale at its own location.

**Repair (E5):**

- [ ] In §10, keep the original printed numbers as as-of-authoring, and add a
  dated currency line: 2026-08-24 re-run is 7 hits at the lines above;
  durable hook is `grep -c '"dd_type": "trailing"' core/firm_rules.py`
  expected `7`. Do not rewrite §1 / verdict / Iterate disposition.
- [ ] One Change-history row for the currency note.

**Falsifier:** `python scripts/check_closure_disposition.py docs/briefs/closures/Q-FIRMEOD-1-closure-falsified.md`
exits 0. `grep -c '"dd_type": "trailing"' core/firm_rules.py` equals 7.
Verdict line still `FALSIFIED`.

---

## Blast-radius (run at the end, not per packet)

After the last packet, grep the **old** tokens and triage:

```
rg -n --hidden -g '!.git' \
  'B1\.4 / B2\.3 / B3\.2|AUTHORIZATION: .AWAITING GO.|reaches Pine|92,104,116,128,140,508,524' \
  CLAUDE.md STATE.md PIPELINES.md REPO_MAP.md README.md \
  docs/ .claude/skills/ lab/CATALOG.md ops/instruments/
```

Expected leftover `AWAITING GO` (leave): sequence overview Status, Phase B
banner, pain-point charter lines that describe the sequence as a whole.

Repair only clear silent restatements of (a) B3 as a live lane, (b) s4 / Phase
A as still awaiting the GO that already happened, (c) Phase D starting at
Pine. Report `BLAST-RADIUS: CLEAN | REPAIRED | OWED` in the execute-session
SESSIONS entry.

---

## Forbidden moves

- Signing off Packet 0 from this plan's AUTHORIZATION.
- Opening a Phase B lane, drafting a card, or spending K/$.
- Deleting B3's mechanism paragraph or the A2 §8 historical cadence note.
- Flipping overview Status or Phase B's per-lane `AWAITING GO`.
- Rewriting Q-FIRMEOD-1's verdict or treating the line-number shift as a
  finding about CLOCK/LOCK.
- Adding a newest-15 decision-index row that restates the A2 residual (the
  residual already lives there).
- New ADR / new brief / new lab slug — every owner already exists.

---

## Exit criteria

All five packets landed · Packet 0 still named as operator-owed · overview
Status and Phase B banner still `AWAITING GO` · blast-radius report filed ·
no Pine / rail / allocation edit.

## Verification (execute session)

```bash
# Packet 1
rg -n "disclosed-N|RESULTS §4|sims_per_seed" STATE.md \
  docs/superpowers/plans/2026-08-23-viable-strategy-phase-b-mechanism-supply.md

# Packet 2
rg -n "B3\.2|KILL" \
  lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS.md \
  docs/superpowers/plans/2026-08-23-viable-strategy-phase-b-mechanism-supply.md
rg -n "buyback-blackout|compelled-abstention" docs/rejected_candidates.md

# Packet 3
rg -n "AUTHORIZATION" \
  docs/superpowers/plans/2026-08-23-viable-strategy-parallel-s4-firm-repair.md \
  docs/superpowers/plans/2026-08-23-viable-strategy-phase-a-target-derivation.md \
  docs/superpowers/plans/2026-08-23-viable-strategy-phase-b-mechanism-supply.md \
  docs/superpowers/plans/2026-08-23-viable-strategy-sequence-overview.md

# Packet 4
rg -n "reaches Pine|TNEC-1" docs/superpowers/plans/2026-08-23-viable-strategy-*.md

# Packet 5
grep -c '"dd_type": "trailing"' core/firm_rules.py   # expected 7
python scripts/check_closure_disposition.py \
  docs/briefs/closures/Q-FIRMEOD-1-closure-falsified.md

python scripts/check_root_doc_liveness.py
python scripts/check_path_liveness.py
python scripts/check_status_consistency.py
```
