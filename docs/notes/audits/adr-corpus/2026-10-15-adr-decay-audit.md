# Audit Note — ADR decay and retention audit (full corpus, 2026-10-15)

**Audit ID:** AUDIT-2026-10-15-ADR-DECAY
**Date:** 2026-10-15
**Triggered by:** operator direction 2026-10-15 (decay audit and pruning "as broad as possible").
**Authors:** Joshua (direction) + Claude Code
**Scope:** all 140 dated ADRs in `docs/adr/`, plus `INDEX.md`, `TOMBSTONES.md`, `README.md` and the `docs/ltm/adr/` cold store
**Lives in:** `docs/notes/audits/adr-corpus/2026-10-15-adr-decay-audit.md`

The `adr-decay-audit` method ran as 15 Phase-1 scan batches, 12 refute-first Phase-2
verifiers and 10 implementation packages. The coordinator merged and reviewed each
package, then re-ran the gates. Result: **45 ADRs removed (140 → 95)** and 7 legacy cold bodies
removed, each with a [TOMBSTONES row](../../../adr/TOMBSTONES.md#2026-10-15-adr-decay-audit-removals).
19 ADRs were trimmed, 22 owners (8 of them ADRs) absorbed consolidated text and 38 more got fixes or link pins.
ADR bytes fell from 3,080,786 to 2,262,069 (−27%). **No future trigger rider was retired**:
each one is still in place, carried verbatim to a surviving owner, or discharged by a
recorded event (§3.3). §5 holds the rulings only the operator can make.

---

## §0 — Source anchors

- Base: `main` @ `4121e84c95f4990b71962e3b9570c4c3fad88426` (all removed bodies retrievable there).
- Change: [PR #855](https://github.com/Joshua-Asante/first-passage/pull/855), branch `claude/kind-goodall-ep4b39`.
- Policy owners: [ceremony tiering](../../../adr/2026-08-08-adr-ceremony-tiering.md),
  [Rule 16](../../../operational_rules.md#16-retention--an-artifact-must-earn-its-place-and-deletion-is-classified-by-execution-not-by-folder),
  the `adr-decay-audit` skill.
- Concurrent open PRs that touch the same tree: #850 (public-exposure redaction), #851
  (wave-1 deletions), #848, #849 (idle-line dormancy), #847, #852. #855 merges last, per the
  coordinating doc-alignment session.
- Prior run: [2026-08-29 audit](2026-08-29-adr-decay-audit.md).

## §1 — Trigger

The operator directed a decay audit of every ADR, with confirmed changes landed and one decision
packet for rulings. The direction set five constraints. Removed files are deleted and rely on git
history. Track B is report-only. No new ADR is created. Riders are never retired unilaterally.
Each deletion passes the full §16 classification.

**Failure class:** source-of-truth fracture (canonical-but-stale decision records).

## §2 — What happened

1. **Inventory.** Headers, trigger-field dates and inbound referrers were collected for all 140
   ADRs. 84 carried a sentinel-read `Trigger check schedule` field. 40 named 2026-11-08, and
   STATE's `### 2026-11-08` linked only 11 of them.
2. **Phase 1 scan.** 15 family batches, Track B report-only. Each batch gave a four-way verdict and
   one of KEEP / FIX / TRIM / CONSOLIDATE / DELETE.
3. **Phase 2 verify.** 12 verifiers re-derived evidence and tried to refute each proposal. 117
   items were verified. The verifiers corrected many Phase-1 specs, most often for line-cited text,
   check-required sections, riders and Track B dependencies.
4. **Implementation.** 10 packages ran in isolated worktrees. The coordinator merged them,
   resolved 19 merge conflicts, assembled TOMBSTONES and regenerated INDEX. After each merge it ran a
   guard (no Track B, protected-code, #850-held or frozen-file edits, no redacted figure) and a
   sentinel rider-map diff.
5. **Coordinator overrides at merge.**
   - **W6 kept.** The W6 deletion was reverted, because s2b's Track-B-held 09-11 packet links it.
   - **No new frozen-surface rule.** A proposed Rule 16 sentence that froze `docs/ltm/**` links
     was not adopted: it would have created new standing text, and it contradicted today's
     pin-the-links direction.
   - **06-30 link pin.** One link pin landed in the 06-30 ADR at `:77`, clear of #850's hunks.
     It is the only edit to a file #850 redacts.

### §2.1 Verdicts

| Verdict | Phase 1 | Final (P2 where re-verified) |
|---|---:|---:|
| STILL_APPLICABLE | 72 | 71 |
| DECAYED_DOCUMENTED | 48 | 46 |
| DECAYED_UNDOCUMENTED | 15 | 18 |
| UNCERTAIN | 5 | 5 |
| **Total** | **140** | **140** |

**Phase 1 → Phase 2 reclassifications (7):**
- **Under-calls upgraded:**
  - Substrate: its Status line was stale.
  - Manifest-integrity: four directories named vs three in code, plus a stale `CLAUDE.md` link.
  - Regime-gate non-example: its own §4 revert trigger appears to have fired on 2026-10-05,
    unrecorded.
- **Over-calls corrected:**
  - FXIFY timeout: a finished one-time act.
  - Book segregation: UNCERTAIN → STILL_APPLICABLE.
- **Others:**
  - Feed policy: minor staleness that was already documented.
  - c1 GO: DECAYED_DOCUMENTED → UNCERTAIN, on the Tradeify eval §4(c) question (§5.3).

**Degenerate output:** none. Every Phase-2 file carried evidence anchors. The coordinator
spot-checked two Phase-1 claims by hand, the substrate's dead link and the manifest dirs, and
both reproduced.

**Lead quality:** about half the first-look leads needed correction. Examples:
- The s2b 09-11 packet is **not** Track-B-neutral.
- The q-tradecap G1–G3 already live in the brief.
- The rail trims shrank: GO from ~20 to 5.5 KB, M1 from ~26 to 9.3 KB.
- The rule-2 withdrawn block is 13.9 KB.
- Striker legmap removal was refuted, so it stays.

### §2.2 Disposition outcome

| Outcome | Count |
|---|---:|
| Removed (TOMBSTONES row; inbound links repointed to owner or pinned blob) | 45 ADRs + 7 cold bodies |
| Trimmed (Revision line names the pre-trim blob) | 19 |
| Received consolidated text verbatim, with provenance | 8 ADRs + 14 non-ADR owners |
| Fixed / link-pinned only | 38 |
| Unchanged (KEEP, HOLD, DEFERRED, Track B) | 31 |

Consolidation families landed:
- The CFD/challenge era (8 ADRs) went to [substrate §11](../../../adr/2026-07-22-challenge-era-substrate-retirement.md).
- The retired data vendors (Dukascopy, OANDA) went to the [feed policy](../../../adr/2026-06-12-tv-csv-canonical-feed-policy.md).
- The closure-gate pair went to [`scripts/README.md#closure-enforcement`](../../../../scripts/README.md#closure-enforcement)
  and the closure template.
- Call-1 went to `strategy_lifecycle.md`, and dedup-first to Rule 8.
- The dd lineage went to the C2 relock and ULP (append-only).
- Rung selection went to the objective map, W1 to load-bearing numbers §1, and the CFO ledger
  and catalog rules to their operating owners.

The legacy cold store now holds only the Aegis body, which #850 deletes. The
`scripts/retire_adr.py` docstring now says the stub/body form is optional. Its behaviour is
unchanged.

### §2.3 Rider accounting (sentinel map, before → after)

| Date | Before | After | Movement (all evidenced; none retired here) |
|---|---:|---:|---|
| 2026-10-20 | 2 | 0 | Eval-lock: the 90-day re-verify ran 2026-10-02/03 (#621); its next instance is STATE `### 2026-12-31` (operator default, sheet E). BluSky-unsourced: T1 fired 2026-08-05 (08-05b). |
| 2026-10-31, 2026-11-01 | 0 | 1 each | Pepperstone and bar-data 90-day checks, previously in prose only, are now sentinel-visible on the substrate. |
| 2026-11-08 | 40 | 36 | R6, claims-rescope and Gen-1 were carried to the substrate field. Unpark: T3 mooted by the operator-ruled repark (2026-08-03, `:135`). 07-16 lane-close: §4 limb 1 fired 2026-10-09. Call-1 was carried to 07-10 `:202`. The add-back rider was carried to the three-loop field. |
| 2027-01-11, 2027-02-08, 2027-05-08 | 1 / 13 / 6 | 1 / 12 / 5 | All carried to the substrate field, one line. |

## §3 — DECAYED_UNDOCUMENTED findings (18)

Each row gives the stale claim, the current reality and the remediation.

| ADR | Stale claim → reality | Remediation |
|---|---|---|
| equity-tier-deletion (04-17) | It still states the 1.0% trigger; C2 later relocked it. | Lineage appended to the [C2 relock](../../../adr/2026-05-08-dd-trigger-c2-relock.md); file removed. The AGENTS "revert triggers LOST" line stays true. |
| striker-v4.3-pyramid (04-17) | It states pyramid 350% as current; refresh-2 superseded that. | Removed; rationale in the tombstone row. |
| manifest-integrity-gate | Names four data dirs (code has three), a stale `CLAUDE.md` link and a stale `--no-verify` sentence. | FIX in place, on the same lines. |
| fixture-test-requirement | Its 2026-11-16 revoke clock is untracked, unreachable, and its pilot tests are gone. | F-1 lesson paths corrected and a correction appended. Deletion HOLD (§5.1). |
| sweep-engine | Its banner says "Python never gates deployment", which contradicts S2. | One-line dated note. Consolidation is DEFERRED (idle-lines chip). |
| rule-2-budget-before-acting | The withdrawn 13.9 KB block was rendered as code by a stray fence. AGENTS (10-13) reversed the 08-15 INQHIORI-only limit, unrecorded. | Block trimmed, fences fixed. The instruction-level reversal is §5.2. |
| no-manual-trading (06-30) | Its literal rule conflicts with AGENTS' operator-directed orders. | Held for #850, which redacts the file; §5.2. |
| bust-day-maxdd-inclusion | Its §4 rides the regime check retired 2026-07-22. | HOLD_RIDER (§5.1). |
| gen1-pipeline-retirement | One stale premise limb. | Removed; its 2027-01-11 check carried to the substrate. The premise is §5.2. |
| external-mechanism-harvest-intake | The idle guard cannot fire: H-OD-1 was admitted with a PASS on 2026-07-16. "Sole intake-class closure" is false. | Only the cosmetic `:331` path fix landed. Recording the rest would settle 11-08 readings, so it goes to §5.2. |
| sfrisk-1 T1 | The 10% bar was overtaken by the 10-09 Decision 4 standard (15%). Neither ADR cites the other. | NEEDS_OPERATOR (§5.2). |
| challenge-era substrate | Status said Phase 5 was branch-only (it merged 2026-08-02 as `0091c5f`), with a dead ltm link. | FIX: archive-pinned link, §7 record table, §11. |
| tv-agent-browser-access | §2.3 names TV as the signal origin; S2 moved it to the daemon. | FIX, qualified for TV-alert routes 2–3. The 2026-10-25 rider is §5.2. |
| orb-mnq-repark | "K_banked(MNQ) = 2, one Cap seat unspent" is stale: the live bank is 22 and the seat is spent. | Appended dated correction plus a same-line status suffix (Track B pins `:107–:115`). |
| params-toml-gate-retirement | One false claim. | Removed; content in substrate §11. |
| msl-sourcing-channel-ratification | The hard rung was met on 2026-10-07 (5 G0 freezes, 0 TNEC-1 survivors) and nothing recorded it. | Record-only addendum. **Closure is the operator's** (§5.2). |
| repo-public-visibility-transition | The archive-repo state was misdescribed, and the public repo reuses the `first-passage` name, which §5 forbids. | Trimmed and corrected; the name and 90-day checkpoint are §5.2. |
| regime-gate non-example (08-24) | Its §4 revert trigger appears fired by the 2026-10-05 prereg (I-21 / O-10 adopts a rider unchanged). | Deletion held; NEEDS_OPERATOR (§5.2). |

**Undocumented drift found outside the corpus:**
- The 2026-08-29 audit records the M1 hook-4 caveat and GO Layer-line fixes as made; neither was
  in the files (Known Trap #6). The trims carry the corrections.
- `check_adr_graph.load_tombstoned_names` exempted **live** ADR names that TOMBSTONES mentions
  (8 at base, M1 included) from A2. Fixed in source, with a regression test.

## §4 — DECAYED_DOCUMENTED and UNCERTAIN

The per-ADR ledger in the appendix gives the verdict, action and reason for every file. Most
DECAYED_DOCUMENTED files were removed or consolidated. The rest are held, deferred or kept with
"no action, already discharged in place". The UNCERTAIN five each have a named resolving check:

| ADR | Resolving check (date) |
|---|---|
| c1 GO | Tradeify compliance answer on bridges and external Python signals for evals: is §4(c) pending or fired? 11-08 sitting. |
| strategy-venue-binding-axis | Write the Aegis 6J edition row (ruled 10-02, never written), or rule T2 retired, before 2026-11-08. |
| loop-s2 | The same Tradeify-eval question as the c1 GO, for the eval only. 11-08 sitting. |
| no-counterparty channel | Its S1/S2 seams are still unruled (open since 08-29). Idle-lines chip / 11-08. |
| venue-binding-axis-t1 | Did T1′ fire at the 10-09/10-11b personal-lane decision or the 10-13 suspension? Operator, 11-08. |

## §5 — Operator packet (NEEDS_OPERATOR)

Each item names the options; a recommendation is marked **(rec)**. Nothing here was
changed on the agent's judgment.

### §5.1 Trigger riders: retire, or move to STATE? (one ruling, 37 ADRs)

Since 2026-09-08 there is no quarterly programme-audit cadence and no mandatory falsifier
([ceremony tiering](../../../adr/2026-08-08-adr-ceremony-tiering.md)). The sentinel still reads
these fields (`ops/sentinel/scan.py`; last recorded run 2026-08-24; `SLATE_DATE` 2026-11-08).
"STATE" means the ADR is linked under STATE's matching dated heading. **R** = retire the dated
check (any event condition stays as standing text); **S** = move it to STATE; **K** = keep.

| ADR (trigger field) | Dates | In STATE | What it checks / why | Rec |
|---|---|---|---|---|
| decompound-remc-hold | 11-08, 27-02, 27-05 | 11-08 | AMBIGUOUS re-raise of an unfalsifiable HOLD on a CFD book; limb-2 dates already struck by its own 08-03 addendum | R |
| instrument-ledger-and-cfg-fingerprint | 11-08 | no | P1 skip-detection; Rule 10 binds anyway (consolidation held on this rider) | R |
| three-loop-methodology-binding | 11-08 | no | Add-back first-real-run flag + ≈2026-12 split falsifier (carried here 10-15) | R |
| cost-geometry-pregate | 11-08 | no | "Alongside regime + ledger triggers" — co-scheduled regime trigger retired 07-22 (consolidation held) | R |
| no-manual-trading-cfd-retirement | 11-08, 27-02, 27-05 | no | Quarterly review of the jurisdiction/automation event trigger (event trigger stays) | R |
| guardian-pyport-public-tracking | 11-08 | no | Local manifest + no-new-tracked-port grep; rule lives in AGENTS + PORT_MANIFEST gate (deletion held) | R |
| bust-day-maxdd-inclusion | 11-08 | no | Bust≥1% coupling at a regime check retired 07-22 (deletion held) | R |
| databento-research-stack | 11-08, 27-01-10 | yes¹ | Quarterly billing review (moot) + 2027-01-10 "zero closed manifests handed to §8" — §8 SPA/PBO dormant, so it may fire | R (11-08); **S or R** (01-10, operator) |
| strategies-never-locked-lifecycle | 11-08, 27-02, 27-05 | no | Type-I/II revert triggers + Call-1 floor re-confirm (now also the carried Call-1 trigger); no live PF accrues | R (dates); K trigger 3 (test-enforced) |
| discovery-campaign-defaults | 11-08 | no | Closed campaigns exercising the defaults — none accruing | R |
| dsr-k-rule | 11-08 | no | Matrix-profile campaign input unreachable | R |
| prop-portfolio-four-friendly-firms | 11-08, 27-02 | 11-08 | **Primary program falsifier** (AGENTS table) — KEEP 11-08; 27-02 quarterly re-check | K (11-08); R (27-02) |
| harv-discovery-lane | 11-08 | no | Already fired and answered by the 07-16 supersession | R |
| prop-account-book-segregation | 11-08, 27-02 | no | Revert check fired 08-08 (27.04% reading never ruled); no joint-MC + fee producer | (a) record AMBIGUOUS and retire **(rec)** / (b) FALSIFIED at N=1 / (c) S |
| prop-portfolio-existing-strategy-candidates | 11-08 | no | Rides the parent's 11-08 hard date | K (optionally link it in the STATE 11-08 row) |
| external-mechanism-harvest-intake | 11-08 | 11-08 | Limb 1 has live unclassified inputs (D5-RECOST-1, NG-EIA-1); idle guard unreachable | K for one final reading; R "then quarterly" |
| sfrisk-1-t1 | 11-08, 27-02, 27-05 | yes¹ | Quarterly regime-check limb already struck 08-29 | R (and see §5.2 T1 ruling) |
| root-doc-charter-dedup | 11-08 | 11-08 | Queue ≤5 cap / out-of-order review — retained by the operator 09-08 | K |
| stage8-variance-dominance | 11-08, 27-02 | no | Quarterly regime clusters (retired) + the carried stage8-mechanistic hard check (module never built) | R (keep composed-candidate event trigger) |
| challenge-era-substrate | 10-31, 11-01, 11-08, 27-01-11, 27-02, 27-05 | yes¹ | 90-day Pepperstone / bar-data checks (live); carried R6 / claims-rescope / Gen-1 quarterly riders; Gen-1 extraction check | K (10-31, 11-01); R (quarterly carries); Gen-1 01-11: operator |
| prop-portfolio-s4-discharge-withdrawal | 11-08 | 11-08 | §4 hard date | K |
| mechanism-counterparty-boundaries | 11-08, 27-02 | 11-08 | 2-A three-strikes input never accrued; **2-C gaming audit has real input** (four `operator-stopped` manifests) | R (2-A); K (2-C) |
| regime-candidate-flag-lane | 11-08, 27-02 | 11-08 | Two-strikes on zero follow-ups | R (keep on-event text) |
| third-leg-symbol-occupancy-limb | 11-08, 27-02 | no | Dormant since 08-06; input cannot accrue | R |
| family-k-bank-disclosure | 11-08 | no | §4 triggers 1–2 (trigger 2 mechanized by `_REQUIRED_KEYS`) | R (keep event triggers) |
| strategy-venue-binding-axis | 11-08 | no | T2 ledger vs LEG_MAP **would fire** (Aegis 6J row never written); T3/T4 cannot | S as a ledger reconciliation, R as axis falsifier **(rec)** |
| loop-s1-environment-ratification | 11-08 | yes¹ | Rail warm/disarmed + Striker bar; host state is checked every session | R date limb; K "next armed-session GO" |
| grand-tier-quintessentials | 11-08 | 11-08 | Scheduled re-read with no decision rule | R (also remove the STATE bullet) |
| rejection-register-topology | 11-08 | 11-08 | §4(a)/(b): coverage 28.6%, 5 gaps — **reachable and failing** | S into the existing 11-08 "Evaluation and rejection review" bullet **(rec)**, or explicit R |
| deep-iteration-lane-charter | 11-08 | yes¹ | Supply-audit PARK-or-supersede; nearest supply (MNQFLOW-1-DEPTH) needs retired Databento | Idle-lines chip (#849) |
| grow-lane-build-authorization | 11-08 | no | Charter reading half (fold into deep-lane); keep first `--lane deep` event | R date half |
| grow0-two-ledger-k-question | 11-08 | yes¹ | Quarterly audit half; keep the M≥2 event | R |
| sourcing-phase-channel-retirement | 27-02 | 27-02 | Limb 2 second starvation check, limb 3 early-closure re-examination | Serve via idle-lines chip; R 27-02 limb 2 once it rules |
| venue-binding-axis-t1-disposition | 11-08 | no | T1′ at the next venue-scope decision — may already have fired (10-09/10-13) | Rule first whether those decisions were non-consultations; then R or move into 08-05 §4 |
| ssot-data-lineage-remediation | 11-08 | no | Task 2 hook fails today (5 gaps, 28.6%) → reads FALSIFIED unless changed (deletion held) | R as unbounded **or** keep as the rejection-register S above |
| candidate-contract | 11-08 | 11-08 | Initial consolidated review + owed adoptions; the MSL ceiling has now fired, which gives that review a real case | K |
| evaluation-order | 11-08 | 11-08 | Initial consolidated review | K |

¹ The ADR is linked somewhere in STATE, but not under the matching dated heading, so sentinel
board-sync reports a gap.

Two further dated obligations that no ADR field carries:
- 07-27 tv-agent-browser's **2026-10-25** hard check, invisible to STATE and the sentinel.
- 08-05b BluSky's **~2026-11-05** inactivity re-read. Options: (a) a STATE `### 2026-11-05` row;
  (b) a scope line in the 12-31 envelope row, accepting a ~2-month slip **(rec)**; (c) leave it
  in the ADR field only.

### §5.2 Rulings outside the rider table

1. **MSL closure.** The charter's hard rung was met on 2026-10-07: 5 G0 freezes and 0 TNEC-1
   survivors, eight weeks from the first freeze. This PR records it; enacting the closure is yours.
2. **Regime-gate non-example.** Its §4 revert trigger (the next pre-registration importing the
   gate as a rider) appears fired by the 2026-10-05 re-MC prereg (I-21 / O-10). Options: confirm
   it fired and revert; or rule it not applicable. Its deletion waits on this.
3. **sfrisk-1 T1.** Does the 10% per-half p99 bar keep any authority now that 10-09 Decision 4
   sets 15%? (A) retired, then the ADR can be deleted **(rec)**; (B) an additional bar for any
   Aegis→M6J proposal.
4. **Great-prune falsifiers.** F-1 has **fired**: 6+ recorded tag retrievals, including the
   arming runbook. F-3 has a likely instance. Rule their disposition; the deletion waits on it.
5. **Harvest-intake intercepts.** Recording "idle guard unreachable" and correcting "sole
   intake-class closure" settles readings ahead of 11-08. Record now, or at the sitting?
6. **06-30 no-manual rule vs AGENTS.md.** AGENTS.md allows operator-directed orders, exits and
   cancels. Should the 06-30 rule be narrowed to strategy-signal execution? The consolidation
   into substrate §11 waits on this and on #850.
7. **Gen-1 premise limb, and the OANDA key file `~/.keys/oanda.txt`** (status unknown;
   follow-up carried in the feed policy).
8. **Public repo.** The public repo reuses the `first-passage` name (the transition ADR's §5
   forbids it). Its 90-day checkpoint (~2026-11-12) is not in STATE.
9. **GRAND §2.6** (named "quarterly gate").
10. **Rule-2 / work-decomposition skill.** AGENTS.md (2026-10-13) made budget declaration standing
    in every seat, reversing the ADR's 08-15 "INQHIORI-only" limit. The fixes to
    `inqhiori/SKILL.md:39-40` and `work-decomposition/SKILL.md:63,135` change instructions, so they
    need your edit or OK.
11. **Coldstore phase A** T4-scope question (09-01): retire **(rec)**. Its deletion waits on this.
12. **STATE hygiene:**
    - The `state-currency` gate fails on `main`: `### 2026-10-14` (Grafana trial end ~10-17) is
      past and not DISCHARGED.
    - The MNQFLOW-1-DEPTH row needs a Databento pull. Databento is retired, and the row's
      "superseding K" label is wrong.
    - The tradable-anomalies Addendum (b) promotion of four null primitives has no STATE row.
    - The GLM credential isolation and the four live `cursor/*` refs on origin are owed and not
      in STATE.

### §5.3 Track B — report only (suspended to the 11-08 sitting)

1. **Tradeify eval rules.** Tradeify support said on 2026-10-12 that bridges and external Python
   signals are not allowed on eval accounts. The reply is second-hand. This plausibly fires the
   c1 GO §4(c) and undercuts S2 on the eval. Rec: treat §4(c) as pending now, and as fired at
   11-08 if compliance stays silent.
2. **Account Manager re-add trigger.** The GO's 07-19 trigger may have fired, but it conflicts with
   the Track B drill plan (CR-12). Rec: withdraw it for the eval.
3. **Incident contract (09-17) header.** It still reads only `Proposed`, while §A12 is ACCEPTED
   (2026-10-05) and §A11–A11.3 are effective. INDEX mirrors the stale header.
4. **Admission ADR.** The R4 rider points to STATE's 2026-10-11 row, which now sits at ~12-31.
   §6 says `book_policy.py` "still implements law A", but TB-I1 fixed that on 09-14.
5. **ORB DRAFT.** The §10 hook matches itself (an authoring error).
6. **Suspension not recorded.** None of the three Track B ADRs mentions the 10-13 suspension. The
   `concept-not-constant` reciprocal still says "PROPOSED, effective on ratification", although
   the admission was ratified 09-14.
7. **Blocked by Track B links** (ready once the sitting clears them):
   - the W6 deletion (s2b `:173`);
   - the s2b packet trim (~9.5 KB of Track-A-only blocks after L266);
   - the tradeify-descope trims (~20 KB if its addenda are ruled neutral);
   - the C2 relock and concept-not-constant trims.

### §5.4 Waiting on other PRs or the idle-lines chip (no ruling needed)

- **After #850 merges:**
  - mvd-discipline → `rule_0.md`, verified;
  - guardian-pyport delete (also rider-held);
  - lifecycle-governance trim, verified;
  - venue-binding reduced trim plus 2 FIXes, verified;
  - egress → browser, after the 10-25 check;
  - 06-30 → substrate §11, after §5.2 item 6.
- **After #851 merges:** fix the §0/§10 references in surviving ADRs to the specs and briefs it
  deletes.
- **Idle-lines chip:** the research-supply consolidations, all tagged DEFERRED in the ledger.
  Verdicts were checked; nothing was consolidated.

## §6 — Lessons to capture

- **Candidate:** a TOMBSTONES row that names its current owner by filename silenced that owner's
  A2 check.
  - Anchor: this audit; fixed in source with a regression test.
  - Already covered by the §16 instrument ("ADR `Supersedes*` edges" now listed as readers).
- **Candidate:** line-number citations from frozen or Track B documents are hidden readers. Most
  trims had to keep sections, or edit in place, to protect them.
  - Already covered by §16 item 3 (section references). No new lesson.

## §7 — Programme-audit signal check

- [x] **Belt that only grows, never prunes:** partially reversed. 45 removals; riders are
  undispositioned pending §5.1.
- [x] **Falsifier thresholds unreachable:** several riders read inputs that cannot accrue
  (§5.1 "R" rows), the same signal Rule 11 names.
- [ ] Other signals: not observed.

## §10 — Audit hooks

```bash
python scripts/check_adr_graph.py                          # A1–A8 OK; A2 now covers live owners named in TOMBSTONES
python -m pytest -q tests/test_check_adr_graph.py -k tombstone_mention
grep -c '^| `docs/' docs/adr/TOMBSTONES.md                  # ≥ 52 rows in the 2026-10-15 section
# Rider map vs this note's §2.3 table (sentinel field reader):
python -c "import importlib.util,sys;from pathlib import Path;from datetime import date;s=importlib.util.spec_from_file_location('s','ops/sentinel/scan.py');m=importlib.util.module_from_spec(s);sys.modules['s']=m;s.loader.exec_module(m);print({d:len(v) for d,v in sorted(m._adr_trigger_dates(Path('.'),date(2026,10,15),date(2028,1,1)).items())})"
```

## §11 — Closure

- **Status:** `Repair-in-flight`. Immediate repairs land in #855. §5 rulings and the §5.4
  dependents are open.
- **Next trigger:** the 2026-11-08 sitting (§5.1–§5.3), and the merge of #850 / #851 (§5.4).

## Appendix — per-ADR ledger

<!-- generated from the Phase-1/2 records and `git diff 4121e84c` at merge; verdict = P2 where re-verified -->

SA = still applicable · DD = decayed, documented · DU = decayed, undocumented · UN = uncertain. Action from `git diff 4121e84c`; P2 = Phase-2 verdict or hold reason ("not re-verified" = KEEP in Phase 1).

| ADR | Verdict | Action | P2 / reason | Bytes before → after |
|---|---|---|---|---|
| `2026-04-17-dd-trigger-calibration` | DD | removed | confirmed (changed) | 3,812 → 0 |
| `2026-04-17-equity-tier-deletion` | DU | removed | confirmed (changed) | 3,210 → 0 |
| `2026-04-17-portfolio-allocations` | DD | removed | confirmed (changed) | 5,517 → 0 |
| `2026-04-17-striker-v4.3-pyramid` | DU | removed | confirmed (changed) | 4,764 → 0 |
| `2026-04-23-guardian-risk-relock-0.34` | DD | removed | confirmed (changed) | 4,444 → 0 |
| `2026-04-24-mvd-discipline` | DD | unchanged | HOLD (#850 redaction) | 11,083 → 11,083 |
| `2026-05-03-sentinel-gate-decision` | SA | removed | confirmed (changed) | 6,924 → 0 |
| `2026-05-08-dd-trigger-c2-relock` | SA | consolidation target | HOLD_TRACK_B | 11,148 → 15,664 |
| `2026-05-10-dd-protection-ulp-rounding` | SA | consolidation target | confirmed (changed) | 12,050 → 14,979 |
| `2026-05-10-manifest-integrity-gate` | DU | fixed/pinned | confirmed (changed) | 6,159 → 6,715 |
| `2026-05-10-mc-c2-anchor-ratification` | DD | removed | confirmed (changed) | 9,594 → 0 |
| `2026-05-16-fixture-test-requirement` | DU | fixed/pinned | HOLD_RIDER | 13,170 → 13,400 |
| `2026-05-16-fxify-correct-timeout-semantic` | SA | removed | confirmed (changed) | 22,739 → 0 |
| `2026-05-23-allocation-refresh-2` | DD | trimmed | confirmed (changed) | 47,939 → 33,466 |
| `2026-06-04-lean-portfolio-meta-layer` | DD | removed | confirmed (changed) | 26,036 → 0 |
| `2026-06-05-concept-admissibility` | DD | fixed/pinned | DEFERRED | 17,874 → 18,302 |
| `2026-06-05-monorepo-layer-boundaries` | SA | trimmed | confirmed (changed) | 41,294 → 21,570 |
| `2026-06-05-sweep-engine` | DU | fixed/pinned | confirmed (changed) | 18,736 → 19,592 |
| `2026-06-06-firm-constants-single-source` | DD | removed | confirmed | 19,571 → 0 |
| `2026-06-07-decompound-remc-hold` | DD | trimmed | confirmed (changed) | 27,006 → 21,696 |
| `2026-06-11-instrument-ledger-and-cfg-fingerprint` | SA | unchanged | HOLD_RIDER | 22,448 → 22,448 |
| `2026-06-12-notion-surface-retirement` | SA | removed | confirmed (changed) | 14,967 → 0 |
| `2026-06-12-three-loop-methodology-binding` | SA | fixed/pinned | confirmed (changed) | 21,266 → 23,185 |
| `2026-06-12-tv-csv-canonical-feed-policy` | DD | consolidation target | confirmed (changed) | 7,840 → 13,285 |
| `2026-06-14-reject-usoil-rdm-spike-fader` | SA | fixed/pinned | confirmed | 13,204 → 13,755 |
| `2026-06-14-rejected-candidate-patterns` | SA | trimmed | confirmed (changed) | 24,396 → 20,679 |
| `2026-06-16-rule-2-budget-before-acting` | DU | trimmed | confirmed (changed) | 36,521 → 24,257 |
| `2026-06-17-dukascopy-retirement` | DD | removed | confirmed (changed) | 18,907 → 0 |
| `2026-06-22-cost-geometry-pregate` | SA | fixed/pinned | HOLD_RIDER | 16,647 → 16,937 |
| `2026-06-23-tv-backtest-egress-automation` | DD | unchanged | HOLD (#850 redaction) + HOLD_RIDER | 18,655 → 18,655 |
| `2026-06-24-oanda-retirement` | DD | removed | confirmed (changed) | 19,568 → 0 |
| `2026-06-30-no-manual-trading-cfd-retirement` | DU | fixed/pinned | HOLD (#850 redaction) | 22,785 → 22,887 |
| `2026-07-01-add-back-metric-layer-split` | DD | removed | confirmed (changed) | 18,971 → 0 |
| `2026-07-01-guardian-pyport-public-tracking` | DD | unchanged | HOLD (#850 redaction) + HOLD_RIDER | 22,708 → 22,708 |
| `2026-07-06-bust-day-maxdd-inclusion` | DU | unchanged | HOLD_RIDER | 15,098 → 15,098 |
| `2026-07-10-databento-research-stack` | DD | trimmed | confirmed (changed) | 26,345 → 17,487 |
| `2026-07-10-r6-nogo-futures-residual-disposition` | DD | removed | confirmed (changed) | 21,055 → 0 |
| `2026-07-10-strategies-never-locked-lifecycle-governance` | DD | fixed/pinned | HOLD (#850 redaction) | 53,859 → 54,224 |
| `2026-07-11-challenge-era-claims-rescope` | DD | removed | confirmed (changed) | 30,060 → 0 |
| `2026-07-11-discovery-campaign-defaults-ratified` | DD | fixed/pinned | confirmed (changed) | 13,872 → 15,208 |
| `2026-07-11-gen1-pipeline-retirement` | DU | removed | confirmed (changed) | 31,201 → 0 |
| `2026-07-11-ops-cfd-estate-retirement` | DD | removed | confirmed (changed) | 36,561 → 0 |
| `2026-07-11-tradable-anomalies-statistics-adoption` | SA | fixed/pinned | confirmed (changed) | 17,463 → 15,972 |
| `2026-07-12-dsr-k-rule-and-variance-floor-supersession` | SA | trimmed | confirmed (changed) | 28,090 → 22,279 |
| `2026-07-12-prop-portfolio-four-friendly-firms` | SA | fixed/pinned | not re-verified | 36,383 → 36,576 |
| `2026-07-13-dd-protection-concept-not-constant` | SA | fixed/pinned | HOLD_TRACK_B | 30,890 → 31,094 |
| `2026-07-13-harv-discovery-lane-ratification` | DD | fixed/pinned | confirmed (changed) | 15,948 → 16,132 |
| `2026-07-13-prop-account-book-segregation` | SA | fixed/pinned | confirmed | 11,519 → 11,627 |
| `2026-07-13-prop-envelope-v1-ratification` | SA | removed | confirmed (changed) | 11,416 → 0 |
| `2026-07-13-stage8-mechanistic-exposure-companion` | SA | removed | confirmed (changed) | 10,272 → 0 |
| `2026-07-14-cc-cursor-surface-allocation` | SA | trimmed | confirmed (changed) | 90,698 → 67,732 |
| `2026-07-14-prop-portfolio-existing-strategy-candidates` | SA | fixed/pinned | not re-verified | 16,612 → 16,868 |
| `2026-07-15-external-mechanism-harvest-intake` | DU | fixed/pinned | NEEDS_OPERATOR | 54,061 → 54,046 |
| `2026-07-15-sfrisk-1-t1-admitting-successor-risk-framework` | DU | fixed/pinned | NEEDS_OPERATOR | 20,563 → 21,068 |
| `2026-07-16-harv-attestation-same-units-supersession` | SA | unchanged | not re-verified | 8,684 → 8,684 |
| `2026-07-16-root-doc-charter-dedup` | DD | fixed/pinned | confirmed | 7,678 → 7,784 |
| `2026-07-16-self-funded-lane-close-striker-micro-reconstruction` | DD | removed | confirmed (changed) | 17,251 → 0 |
| `2026-07-17-c1-rail-build-account-registration-go` | UN | fixed/pinned | confirmed (changed) | 52,008 → 46,894 |
| `2026-07-20-stage8-variance-dominance-risk-neff-gate` | SA | fixed/pinned | confirmed (changed) | 23,802 → 22,438 |
| `2026-07-22-c1-venue-native-monitoring-maturity` | DD | trimmed | confirmed (changed) | 70,512 → 61,410 |
| `2026-07-22-challenge-era-substrate-retirement` | DU | fixed/pinned | confirmed (changed) | 36,288 → 34,045 |
| `2026-07-22-prop-portfolio-s4-discharge-withdrawal` | SA | fixed/pinned | not re-verified | 37,296 → 37,340 |
| `2026-07-23-c1-rung-selection-ev-objective` | DD | removed | confirmed (changed) | 22,891 → 0 |
| `2026-07-25-instrument-profile-index` | SA | trimmed | confirmed (changed) | 35,152 → 25,565 |
| `2026-07-26-mechanism-counterparty-constraint-boundaries` | DD | fixed/pinned | confirmed (changed) | 22,311 → 22,728 |
| `2026-07-26-regime-candidate-flag-lane` | SA | fixed/pinned | confirmed | 20,735 → 20,875 |
| `2026-07-27-tv-agent-browser-access` | DU | consolidation target | confirmed (changed) | 11,638 → 13,430 |
| `2026-07-29-third-leg-symbol-occupancy-limb` | SA | trimmed | confirmed (changed) | 21,920 → 14,331 |
| `2026-07-31-orb-mnq-unpark-payability-target` | DD | removed | confirmed (changed) | 50,855 → 0 |
| `2026-08-02-pepperstone-feed-retirement` | DD | removed | confirmed (changed) | 17,112 → 0 |
| `2026-08-03-bar-data-cfd-and-candidates-retirement` | DD | removed | confirmed (changed) | 6,563 → 0 |
| `2026-08-03-claude-md-futures-refocus` | DD | removed | confirmed (changed) | 20,927 → 0 |
| `2026-08-03-orb-mnq-repark-payability-falsified` | DU | consolidation target | confirmed (changed) | 26,271 → 31,959 |
| `2026-08-03-params-toml-gate-retirement` | DU | removed | confirmed (changed) | 9,207 → 0 |
| `2026-08-04-family-k-bank-disclosure-not-gate` | SA | trimmed | confirmed (changed) | 24,388 → 18,146 |
| `2026-08-04-firm-rules-eval-lock-fix-applied` | SA | fixed/pinned | confirmed (changed) | 22,694 → 23,473 |
| `2026-08-04-iterate-closure-exit-mandatory` | DD | removed | confirmed (changed) | 25,790 → 0 |
| `2026-08-04-strategy-coldstore-phase-a` | SA | fixed/pinned | NEEDS_OPERATOR | 21,060 → 21,416 |
| `2026-08-04-tradeify-venue-descope-eval-included` | SA | unchanged | REPORT_ONLY (Track B) | 71,391 → 71,391 |
| `2026-08-05-avenue-a-generate-confirm-route` | DD | removed | confirmed (changed) | 527 → 0 |
| `2026-08-05-blusky-inactivity-unsourced-encoding` | DD | removed | confirmed (changed) | 22,133 → 0 |
| `2026-08-05-strategy-venue-binding-axis` | UN | unchanged | HOLD (#850 redaction) | 31,949 → 31,949 |
| `2026-08-05b-blusky-inactivity-rule-sourced` | SA | consolidation target | confirmed (changed) | 17,661 → 20,360 |
| `2026-08-06-candidate-call1-action-on-breach` | SA | removed | confirmed (changed) | 14,420 → 0 |
| `2026-08-07-loop-s1-environment-ratification` | SA | unchanged | not re-verified | 8,417 → 8,417 |
| `2026-08-07-loop-s2-signal-host-fork` | UN | fixed/pinned | confirmed | 9,278 → 9,497 |
| `2026-08-07-loop-s5-bounded-promotion-lane` | SA | unchanged | not re-verified | 10,270 → 10,270 |
| `2026-08-07-w1-intraday-honest-engine-remeasure` | SA | removed | confirmed (changed) | 6,577 → 0 |
| `2026-08-07-w4-minimal-gate-set-dormancy` | SA | trimmed | confirmed (changed) | 9,440 → 8,400 |
| `2026-08-07-w6-rail-infra-closures` | DD | unchanged | HOLD_TRACK_B (s2b:173 link) | 4,866 → 4,866 |
| `2026-08-08-adr-ceremony-tiering` | SA | unchanged | not re-verified | 5,664 → 5,664 |
| `2026-08-08-edge-cohort-correction-and-necessity-retarget` | SA | trimmed | confirmed (changed) | 35,916 → 20,024 |
| `2026-08-08-great-prune` | DD | fixed/pinned | HOLD_RIDER | 21,490 → 21,739 |
| `2026-08-08-s2b-signal-daemon-build` | SA | unchanged | REPORT_ONLY (Track B) | 78,128 → 78,128 |
| `2026-08-09-grand-tier-quintessentials-binding` | SA | trimmed | confirmed (changed) | 20,333 → 16,193 |
| `2026-08-09-rejection-register-topology-and-bar-wiring` | SA | trimmed | confirmed (changed) | 15,908 → 13,044 |
| `2026-08-10-implied-sr-plausibility-gate` | DD | removed | confirmed (changed) | 573 → 0 |
| `2026-08-10-temporal-selectivity-outside-mapped-levers` | SA | unchanged | DEFERRED | 9,149 → 9,149 |
| `2026-08-12-closure-disposition-coverage-hard` | DD | removed | not re-verified | 15,397 → 0 |
| `2026-08-12-msl-implied-sr-disclosure-not-kill` | DD | removed | not re-verified | 544 → 0 |
| `2026-08-12-msl-mym-occupancy-release` | SA | unchanged | not re-verified | 2,625 → 2,625 |
| `2026-08-12-msl-sourcing-channel-ratification` | DU | consolidation target | confirmed (changed) | 7,266 → 8,565 |
| `2026-08-13-dedup-first-before-new-work` | SA | removed | confirmed (changed) | 24,057 → 0 |
| `2026-08-13-implied-sr-report-only-fade-reopen` | SA | trimmed | confirmed (changed) | 13,983 → 9,669 |
| `2026-08-13-msl-slate-2-design-box` | SA | unchanged | not re-verified | 2,675 → 2,675 |
| `2026-08-14-cc-cursor-autonomous-loop` | DD | removed | confirmed | 870 → 0 |
| `2026-08-14-repo-public-visibility-transition` | DU | trimmed | confirmed (changed) | 25,641 → 19,660 |
| `2026-08-15-analogue-modality-route-ruling` | SA | unchanged | not re-verified | 4,143 → 4,143 |
| `2026-08-15-no-counterparty-statistical-sourcing-channel` | UN | unchanged | not re-verified | 63,171 → 63,171 |
| `2026-08-15-notice-log-is-the-live-observation-routing-convention` | SA | removed | confirmed (changed) | 19,735 → 0 |
| `2026-08-16-con5-timeframe-scope-cheap-falsifier-gate` | SA | unchanged | DEFERRED | 19,590 → 19,590 |
| `2026-08-16-deep-iteration-lane-charter` | DD | fixed/pinned | confirmed (changed) | 40,564 → 42,530 |
| `2026-08-19-cme-broker-panel-admission-for-breadth-revival` | SA | fixed/pinned | not re-verified | 20,039 → 20,186 |
| `2026-08-20-analogue-modality-override-ict-ote-1-admit` | DD | removed | confirmed | 16,889 → 0 |
| `2026-08-21-cfo-subscription-ledger-consolidation` | SA | removed | confirmed (changed) | 3,636 → 0 |
| `2026-08-22-catalog-hot-vs-disposition` | SA | removed | confirmed (changed) | 28,794 → 0 |
| `2026-08-22-grow-lane-build-authorization` | SA | unchanged | not re-verified | 12,792 → 12,792 |
| `2026-08-22-grow0-two-ledger-k-question` | DD | fixed/pinned | confirmed (changed) | 44,628 → 45,187 |
| `2026-08-23-strategy-coldstore-phase-b` | SA | removed | confirmed (changed) | 11,591 → 0 |
| `2026-08-23-strategy-coldstore-phase-c` | SA | trimmed | confirmed (changed) | 13,757 → 10,889 |
| `2026-08-24-q-tradecap-2-elect-alert-tripwire` | SA | removed | confirmed | 2,711 → 0 |
| `2026-08-24-regime-gate-scope-worked-nonexample-f1-discharge` | DU | unchanged | NEEDS_OPERATOR | 18,469 → 18,469 |
| `2026-08-24-sourcing-phase-channel-retirement` | SA | fixed/pinned | confirmed (changed) | 42,831 → 43,126 |
| `2026-08-24-tradeify-growth-tier-scoring-only` | SA | removed | confirmed (changed) | 3,418 → 0 |
| `2026-08-24-validation-battery-k-tiering-and-gate-retirement` | SA | removed | confirmed (changed) | 22,807 → 0 |
| `2026-08-24-venue-binding-axis-t1-disposition` | UN | unchanged | NEEDS_OPERATOR | 28,243 → 28,243 |
| `2026-08-26-striker-legmap-cap-release` | SA | unchanged | REFUTED | 5,728 → 5,728 |
| `2026-08-27-ssot-data-lineage-remediation-program` | SA | fixed/pinned | HOLD_RIDER | 45,961 → 46,222 |
| `2026-08-29-clv-autocorrelation-admission-route-scope` | SA | unchanged | DEFERRED | 32,189 → 32,189 |
| `2026-08-30-candidate-contract` | SA | unchanged | not re-verified | 11,854 → 11,854 |
| `2026-08-30-evaluation-order` | SA | fixed/pinned | not re-verified | 13,516 → 13,503 |
| `2026-09-02-portable-edge-cultivation-campaign-objective` | SA | unchanged | not re-verified | 16,965 → 16,965 |
| `2026-09-03-venue-legality-re-expression-lane` | DD | fixed/pinned | confirmed (changed) | 19,285 → 19,525 |
| `2026-09-05-tradeify-select-striker-expression-readmission` | SA | unchanged | not re-verified | 9,569 → 9,569 |
| `2026-09-06-tracked-file-reduction-prune` | SA | unchanged | HOLD_RIDER | 13,128 → 13,128 |
| `2026-09-12-orb-mnq-r2-supersession-DRAFT` | SA | unchanged | REPORT_ONLY (Track B) | 17,157 → 17,157 |
| `2026-09-12-tradeify-book-protection-instance-admission` | SA | unchanged | REPORT_ONLY (Track B) | 69,633 → 69,633 |
| `2026-09-14-a7-attended-agent-capture` | DD | fixed/pinned | confirmed (changed) | 6,936 → 7,254 |
| `2026-09-17-bounded-platform-protection-incident-contract` | SA | unchanged | REPORT_ONLY (Track B) | 120,587 → 120,587 |
| `2026-10-09-self-funded-tradovate-lane-reopen` | SA | fixed/pinned | confirmed (changed) | 16,370 → 16,952 |
