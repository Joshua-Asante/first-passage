# Audit Note — 2026-08-08 quarterly programme audit (meta + object + D1)

**Audit ID:** AUDIT-2026-08-08-quarterly
**Date:** 2026-08-08 · **Window:** 2026-07-01 → 2026-08-08 (prior full cycle: 2026-07-01)
**Triggered by:** scheduled quarterly vehicle (the obligation ~47 ADR trigger riders name) + operator direction ("run the 2026 quarterly program audit and run an audit on D1").
**Authors:** Joshua (operator) + Claude Code.
**Method:** four multi-agent workflows against post-PR-#688 state — rider discharge sweep (15 agents, adversarial verify on every discharge claim), meta-layer seven-question audit, object-layer seven-question audit (separate workflows; layer discipline enforced structurally), D1 limb audit (6 sweeps → 5 dimensions → 3 refutation lenses each). All 19 layer diagnostics landed with high confidence; **the verify tier was partial and the verdict agents died on session limits — the layer verdicts below were synthesized in-session by CC from the landed diagnostics, not produced by an independent verdict agent.** Evidence was assembled before any verdict was drafted (trap #1).
**Reconciliation:** PRs #689–#691 landed during the audit (Rule-11 dormancy addenda on C2-relock / FXIFY-timeout / params-toml / M1 / W4; prereg-binding gate; Q-R2AGRUN-1 closed; Q-R2FLOW-1 G0 frozen). Dispositions below are reconciled to `origin/main` @ `71b516c`.
**Sentinel:** the published enumeration command crashed on the operator host (locale decode defect in `_git_lines`); fixed with RED-first regression tests in this PR. Post-fix output is byte-identical to the forced-UTF-8 run used during the audit.

---

## §1 — Verdicts

| Layer | Verdict | Prior (2026-07-01) | Trend |
|---|---|---|---|
| **Meta** (methodologies/governance) | **Stable — watch flag** (operator ruling §1.3-a) | Progressive | ↓ |
| **Object** (portfolio/programme/rail/discovery) | **Degenerating** | Proposed-Stable, **conditional — conditions never met** | ↓ (prior verdict never took effect) |
| **D1** (MNQDTL-1 daily-cadence limb, as a gate) | **Degenerating** | n/a (first audit) | — |

Every Degenerating verdict carries a named action (§5): **the Great Prune**
([`ADR 2026-08-08-great-prune`](../../../adr/2026-08-08-great-prune.md)) is the mandated belt-prune for the
**object** layer; D1's action is a deferred operator decision (§5.3). The meta layer's watch flag rides the
same prune plus the 2026-11-08 re-count.

### 1.3 — Operator rulings (2026-08-08, JA)

**(a) Meta q2 belt-churn = YELLOW, not RED.** The "consecutive audits" threshold is read as **quarterly
cycles only**; the 2026-08-03 gate-stack and 2026-08-05 claim-alignment audits were triggered/scoped and do
not count toward it. On that reading this is the **2nd** consecutive net-positive cycle (yellow flag), not the
4th (red). **Consequence:** no RED remains in the meta layer, so the Degenerating trigger does not fire and
the meta verdict moves to **Stable with a watch flag** — q3 (progressive evidence) is GREEN, but q1's
enforcement erosion and the still-net-positive belt keep it short of Progressive. **What flips it back to
Degenerating at 2026-11-08:** a third consecutive net-positive *quarterly* tally, or any belt-patch without
independent corroboration. The counting convention is now fixed and must not be re-litigated per-cycle.

> ⚠ **Trigger 2 was observed 2026-08-15** (belt-patch without independent corroboration; executed
> measurement, not impression). Read
> [`2026-08-15-governance-belt-meta-audit.md`](2026-08-15-governance-belt-meta-audit.md) §3.4 / §4
> before applying this clause at the 11-08 cycle. Trigger 1 (quarterly tally) is **not** fired — that
> audit is triggered, not scheduled, and does not count. Whether trigger 2 fires on observation or is
> banked to 11-08 is an open operator reading, flagged there.

**(b) Hard-core P1 and P3 → TOMBSTONE.** Both, with their obligations recorded in §2 above rather than
carried forward as live riders. P2 (MOOT), P4 and P5 (unfalsifiable) tombstone as already ruled — so the
entire 2026-07-03 hard-core P-gate set leaves the hot path. ⚠ **This does not retire the underlying
questions.** P3's Kill-D payout-extraction arithmetic (`M_f` per firm) was never computed and has been owed
since 2026-07-06; if the operator wants it, it re-enters as a fresh dated packet, not as a revived ADR.
Bodies retrievable via `git show pre-prune-2026-08-08:docs/adr/2026-07-03-hardcore-p*.md`.

**(c) M1 interlock hardening → spawned as a separate task** (§5 item 4). Code fix, out of the prune's scope.

### 1.1 Meta grades

| # | Diagnostic | Grade | One line |
|---|---|---|---|
| 1 | Hard-core integrity | YELLOW | Conduct intact (freeze→run held 5/5 on gate content; Rule 0 caught a phantom threshold inside P1); enforcement eroding — 5 same-commit freezes never flagged (sentinel `_corresponds` blind to the in-window filing convention), D-S-A headers ~19% compliance never once flagged, loop-of-record §10 hook unusable (242/243 false-positive rate). |
| 2 | Belt churn | **YELLOW** (ruled §1.3-a; measured RED on the wider reading) | 26–32 ADD / 4 REMOVE (6.5–8:1); ADR corpus 48→121 in 38 days, zero removed; 2nd consecutive net-positive **quarterly** cycle ⇒ yellow (4th on the all-audits reading ⇒ would have been red). Counterweights recorded: ratio improving 15:1→8:1→4:1; the three flagship "prunes" are prune-shaped ADDs by their own text (W5 "no gate dropped"; W4 forbids deleting its modules; tiering forward-only, 0 light ADRs at HEAD). ⚠ Boundary the operator owns: on a quarterly-cycles-only reading this is YELLOW; that reading discards two triggered-audit tallies incl. 08-05's own self-count. |
| 3 | Progressive evidence | GREEN | Multiple pre-registered expectations recorded WRONG rather than retrofitted (Q-CAPA-1 Cap-held, MNQFLOW-1 null, MNQBASE-1 Step-1); defects caught pre-run by synthetic dry-runs; discipline held while returning nulls. |
| 4 | Degeneration | YELLOW | No post-hoc threshold rescue found; K-bank→disclosure (2026-08-04) is the window's one loosening, operator-grounded not rationalized; 07-01 watch item (metric redefined at first consultation) did not recur. |
| 5 | Boundary | YELLOW | One crossing (blind order-flow probe vs Avenue A §6 cond 3) — REPAIRED by the 2026-08-05 ruling (recorded deviation, precedent pinned, not retro-ratified). Freeze-attestation sentence lost in `2dc14db` (no gate moved). |
| 6 | Theory comparison | YELLOW | Route A favoured by the programme's own K-wall arithmetic, yet all three R2 campaigns ran Route B (all dead: VOID-COVERAGE / FALSIFIED / non-promotable); CC/Cursor dual-limb falsifier due today, unevaluated. |
| 7 | Falsifier check | YELLOW | Thresholds unmoved (mechanical diff clean); the drift arrived as **removed inputs, not moved numbers** — see §3 unfalsifiable census. |

### 1.2 Object grades

| # | Diagnostic | Grade | One line |
|---|---|---|---|
| 1 | Hard-core integrity | YELLOW | Preserved in substance (8 Pine hashes byte-identical; DD constants guarded at import; allocations unchanged) — **guards collapsed to ~¼ coverage**: allocation absolute-value check covers 1 of 4 legs (Guardian band, soft, outside the 15-gate battery); a coordinated 3-site edit to Striker/Aegis/NAS100 passes every hard gate and every test. D-1: CLAUDE.md "wired: consumed by the rail" overstates — rail re-implements the DD comparison (numerically equivalent; weaker state validation fails toward full size). D-2: authorization state of record (1.00×) ≠ the value the deployed host ran (WATCH-1 0.50×, ADR-governed but recorded only in RUNBOOK arithmetic). |
| 2 | Belt churn | YELLOW | Ledger N-findings and DEAD rows grew as designed (prunes of hypothesis space); doc mass around them grew faster. |
| 3 | Progressive evidence | YELLOW | Real durable knowledge produced (depth census, event ceiling, selection ceiling, K-wall, N13 no-time-limit, eval-lock correction that withdrew the programme's only positive §4 result and changed production code) — none of it a deployable candidate. |
| 4 | Degeneration | **RED** | Signal 5 (SNAG) firing 2nd consecutive cycle **after** the 07-01 audit ordered a mandatory repair: repair authored, **never operator-ratified**, and `rejected_candidates.md` stopped being fed 2026-08-03 — exactly when the densest kill run in estate history began (~15 campaigns, zero entries). Both stopping rules non-operative. |
| 5 | Boundary | YELLOW | No re-proposal of a rejected candidate with new parameters (F2 guard held — Q-WLEGB-1 rebuilt strategy-free to avoid a fifth ORB gate); MNQDTL-1 §5 named-path defect found (F-E covers L only, not D1). |
| 6 | Theory comparison | YELLOW | S1 no-successor ruling internally consistent with measured venue evidence; 69/11 vs 51/29 unresolvable (no fills); Route B chosen against Route A arithmetic — three dead campaigns later, the arithmetic looks right. |
| 7 | Falsifier check | **RED** | Thresholds: zero drift. Reachability: **~10 of ~14 object falsifier limbs cannot fire**; the two surfaces that would catch a wrong live-sizing constant or a decaying strategy (allocation catch-paths; lifecycle Call-1 σ-source) are dark by the repo's own dated census. Degeneration arrived through removed inputs — strictly worse than drifted thresholds. |

---

## §2 — Rider discharge sweep (the 47 field-form 2026-08-08 triggers)

Canonical set = sentinel span-join enumeration (47). The published single-line `rg` under-reaches by exactly one: [`2026-07-22-c1-venue-native-monitoring-maturity.md`](../../../adr/2026-07-22-c1-venue-native-monitoring-maturity.md) carries its date on the third wrapped continuation line — **the M1/arming gate was the one rider no simple enumeration saw.**

**Partition: 2 DISCHARGED · 37 OWED · 3 MOOT · 5 UNFALSIFIABLE.** Only 5 discharge claims existed across 46 adjudicated riders; adversarial verification **refuted 3 of 5**. Full per-rider table: session record; retrieval `git show pre-prune-2026-08-08:<path>` for any tombstoned carrier. Highlights that must not be lost:

- **Refuted discharges:** P3 Kill-D "RESOLVED" was a triage label, not the computation (no M_f arithmetic exists; §10 hook still fails). P5 carries two false records (screen K completed 4 days before the addendum denying it; the 08-08 trigger field manufactures a date §6 struck). R6 §10 prints green against a rail that exists (top-level `ls` can never match one level down). Guardian pyport §4 limb (a): both hash-pinned ports absent from repo, 21 worktrees, and 3 backups — loss normalized elsewhere as "often absent on disk"; the manifest RESTORE path would recreate the tracked-exposure §2.4 forbids.
- **Fired-never-recorded (4):** existing-strategy-candidates early-fail · book-segregation at 27.04% ≥ 25% · family-K disclosure omitted from two live preregs · venue-binding T1 (degenerate always-fires while `Proposed`).
- **Unfalsifiable census (15 checks cannot fire):** P4 + SFRISK-1-T1 + bust-day-maxdd all delegate to the decompound HOLD's limb-2, struck 2026-08-03 — one orphaned limb propagated unfalsifiability to three gates. P5 both limbs dead (pegged to "before R6 issues GO"; R6 is a spent NO-GO one-shot). P1 budget clock same dead peg. Dukascopy mitigation channel deleted. No-manual-trading trigger-2 instrument deleted. params-toml + DSR-K zero-exposure by construction (DSR floor crosses Cap at K=4 ⇒ gate mechanically walled off — sits under the stack's largest loosening, K_DSR re-baselined 48.9×). Four STATE hand-check rows (05-08/05-16/05-18/05-23) moot per claims-rescope :212-214.
- **Board sync:** 9/47 riders boarded; STATE's own counts stale (36/53/17 vs measured 47/62/15) under a same-day curation stamp; "No Route B campaign has been opened" refuted (three existed by close of 08-08).

**Disposition rule executed by the prune:** carrier survives → obligation stays with carrier; carrier tombstones → obligation dies as MOOT/UNFALSIFIABLE **with this note as the record**, except genuinely-live obligations which move to STATE rows. P1/P3 keep-or-tombstone is an **operator ruling at PR review** (default: tombstone with obligation recorded here — P3's Kill-D payout-extraction math remains mission-relevant if the operator wants it, but it has been owed since 07-06 with zero work).

---

## §3 — D1 audit (MNQDTL-1 daily-cadence limb)

**Reachable — YES** (~20pp headroom, demonstrated twice: ORB-MNQ-1 realized 1,846/1,857 sessions = 99.4%; Q-MNQSEL-1 S6 ≈ 99.7–99.9%). **Binding — NO, by construction, not merely upstream death:**

1. D1's operative quantity has never been computed for anything; the §6 verdict string exists in exactly one file (the spec).
2. Its only executable form is `admission_schema.d1: Optional[bool] = None` — default ADMIT, refuses only on a self-declared `false`; its single execution attested `"d1": true` on a campaign with no trades, no stop, no R.
3. The §6 limb "coverage ≥ 80% **after skip-days**" is orphaned: the only operationalization (§3.3) is R1-conditioned and R1 is foreclosed; the named study home (`mnq_stop_distribution_2026-08-02`) contains zero OR-range data and its headline was withdrawn 4 days before the spec was authored; the skip threshold is edge-indexed (L/$2/pt) but stated as a constant.
4. D1's level does not deliver D1's own reason: 0.80 × $276.2 = **$220.96/day** vs the $250 aspiration (needs 90.5% coverage); §1.3's "clears (+$26)" silently assumes 100%.
5. The "strictly tightens EM4 / clears it by construction" claim is false (ten 0s + ten 2s passes both limbs while breaching EM4 twice).
6. ~75% of D1's shaping is redundant with E1/EM3/EM5; its one genuine incremental exclusion is the 20–80% coverage band — where the estate's only EM1-clearing measured MNQ edge (0.85R at ~22% duty cycle) lives. n=2 record; not a law; recorded as cost, not verdict.

**Change-legality ruling (the misuse-prone one):** "no live candidate exists" is TRUE (verified five ways) — and does **not** make relaxing D1 legal now. Trap #12's predicate is *emerging evidence*, not a failing candidate; the repair's required AMBIGUOUS exit was closed by S1; §4's remedy list omits D1-relaxation; **F-E names L three times and D1 zero — the spec's named legal path does not cover the limb.** The legal move if the operator judges the target dead: **operator ADR recording §6 FALSIFIED ahead of 2026-11-08** (honest early closure), which immediately unlocks a successor spec carrying any D1′ with its own §8 signature and stated reason. F-B's "K ≤ 2 budget" is ambiguous (per-campaign vs cumulative — two Route B campaigns at K_intrinsic=1 each already total 2 on the cumulative reading); operator ruling either way.

---

## §4 — Prior-cycle conditions

- **Meta:** 07-01 Progressive stands as recorded for its window; this cycle's RED belt-churn is the 4th consecutive net-positive tally, including the 08-03/08-05 triggered audits' own counts.
- **Object:** 07-01 "PROPOSED STABLE" was **conditional on §5 falsifier re-arms + a mandatory SNAG repair.** The re-arm executed and returned the opposite of relief (the allocation ADR's own 2026-08-02 addendum: "zero live catch-paths"); the SNAG repair was authored, never ratified, and its register stopped being fed. **The prior verdict never took effect on its falsifiability limb.**

## §5 — Actions (protocol: every Degenerating verdict names one)

1. **The Great Prune** — [`ADR 2026-08-08-great-prune`](../../../adr/2026-08-08-great-prune.md), executed in this PR. Owner: operator (merge = ratification). This is the belt-prune both layer verdicts mandate: obligation-carriers with dead checks tombstone, cold mass deletes under tag `pre-prune-2026-08-08`, retention test becomes standing law.
2. **Operator rulings at PR review:** (a) P1/P3 hard-core gates keep-or-tombstone; (b) consecutive-audit boundary (meta q2 RED vs YELLOW); (c) prune ADR ratification itself.
3. **MNQDTL-1 §6 early-closure decision** — separate from the prune; the legal path is §3 above. No default; the operator owns it.
4. **M1 interlock hardening (code follow-up):** the arm path reads only the artifact's `status` field — a 24-byte `{"status":"RESOLVED"}` clears it while the validator fails the same bytes with 19 errors; the arm path never invokes the validator. Wire `validate_c1_monitoring_acceptance.py` into `c1_rail_arm.py` before any arming conversation.
5. **Named checks run in this PR's verification:** S5 `pytest tests/test_promotion_packet.py`; S2b five-limb record (limbs 4–5 had citable records; 1–3 recorded at verification).

## §10 — Audit hooks (next cycle: 2026-11-08 window)

```bash
# Rider census (post-fix sentinel; count should be the live-carrier set only)
PYTHONPATH=ops python -m sentinel --asof 2026-11-08
# Size regression vs this prune's floor (fails loud if accretion resumes)
git ls-tree -r HEAD --long | awk '$2=="blob"{s+=$4; n+=1} END {printf "%.1f MB / %d files\n", s/1e6, n}'
# ADR count (target: live set + tombstone index, not 121)
ls docs/adr/*.md | wc -l
# Belt-churn tally inputs (compare against 2026-08-08 anchors in this note)
git log --oneline --since=2026-08-08 -- docs/adr docs/spec docs/methodology docs/operational_rules.md scripts/gates.yml | wc -l
```
