# GSUB-1 — Phase 1 inventory + Phase 2 disposition proposals (run record)

**Run date:** 2026-08-09 · **Executing session:** Claude Code, branch `claude/gsub-1-adr-grand-tier-bb2d54`
**Spec:** [`GSUB-1-first-grand-subtract-pass.md`](GSUB-1-first-grand-subtract-pass.md) · **ADR:** [`grand-tier`](../adr/2026-08-09-grand-tier-quintessentials-binding.md) (`Accepted`)
**Pre-registration anchor (§8):** ratification commit `c90746d` — committed before any Phase-1 surface was read for inventory purposes
**Phase status:** Phases 1–2 **DONE_WITH_CONCERNS** (concerns: C-1/C-2 below) · **Phase 3 — operator ratification — PENDING** · Phase 4 (records at `docs/pursuits/`) executes only on ratified rows
**Scope attestation:** nothing was deleted, closed, or edited by this run beyond this record and its tracking rows. All dispositions below are **proposals**.

**Concerns (return `DONE_WITH_CONCERNS`):**
- **C-1:** subscription $ figures are not discoverable in-repo (§0.5-3); no disposition turns on an exact figure, but the consolidated read is qualitative until the operator supplies them.
- **C-2:** ~~no Survive bound (operator-hours budget) is written anywhere~~ → **CLOSED RESOLVED-BY-REFRAMING 2026-08-09** ([`ADR`](../adr/2026-08-09-survive-bound-is-the-queue-cap.md)). The premise was wrong twice over: GRAND §2.5 specifies **no unit and no number** (all 17 KEEPs carry the field, so it was already satisfied), and an **hours** bound would cross Rule 2 §5 forbidden move #2 ("expressing the budget in minutes anywhere in canon or ADR"). The portfolio bound is the **≤5 operator-queue cap** — concurrency-denominated, already in force; only its rationale had been deleted (2026-08-03), now restored. ⚠ This run reasoned *against* the unwritten bound at row c1 ("outside current Survive bounds (hours)") while simultaneously recording C-2 — that disposition stands on its idle-time grounds, but its stated test was loose.

---

## §0 — Rule 0 (executed; anchors as of this session)

| Surface | Read | Anchor (`git log -1`) |
|---|---|---|
| `docs/briefs/INDEX.md` (Q-roster, full) | ✓ | `834f638` 2026-08-09 |
| `STATE.md` (queue · decision index · dormant threads · forward triggers, full) | ✓ | `c90746d` 2026-08-09 |
| `lab/CATALOG.md` (Active · legacy · _inbox · Archived, full) | ✓ | `7dfbbb5` 2026-08-09 |
| `docs/adr/` dir listing + `TOMBSTONES.md` | ✓ | `d98ca40` 2026-08-09 |
| `docs/notes/audits/programme-audit/2026-08-08-quarterly-audit.md` (full) | ✓ | `d98ca40` 2026-08-09 |
| `docs/notes/2026-07-10-operator-retirements-record.md` | ✓ | `2362bb1` 2026-08-03 |
| `.claude/skills/` (19 `SKILL.md`) | ✓ | `d98ca40` 2026-08-09 |
| `~/.claude/skills/` + plugin registry (session skill mount) | ✓ | session listing 2026-08-09 (not VC'd) |
| `docs/methodology/inqhiori-canon.md` §14 + D-gate | ✓ | `c90746d` 2026-08-09 |
| `docs/rejected_candidates.md` (registry existence + feed state per audit) | ✓ | `baaab64` 2026-08-08 |
| Advisor memory (`MEMORY.md`) — **omission-check only**; every row below cites a live surface | ✓ | n/a (input, not corpus) |

Tooling/subscription stack: **no single repo registry exists** (verified) — rows d11–d16 built from
owning ADRs/notes; $ figures marked unverified (C-1).

## §0.5 — Ambiguity rulings (provisional — operator may re-rule any at Phase 3)

1. **Granularity:** pursuit = lane/standing commitment, not per-Q. Individual Q-briefs are campaign
   internals (Delete's jurisdiction, §5-3); cross-session standing threads (roster/dormant rows) get
   their own rows.
2. **CATALOG `ACTIVE` semantics:** hot-body retention, not work-ongoing; last-activity read from slug
   dates + SESSIONS/git, not the status column.
3. **Subscription $:** absent from repo → `$ unverified`; operator supplies at Phase 3 (C-1).
4. **Recurring hrs:** not repo-measurable; recent-activity density used as proxy (C-2).
5. **Excluded as not-First-Passage:** personal-productivity surfaces (Todoist/Gmail/Calendar MCPs,
   `morning` skill, platform utilities pdf/docx/xlsx/pptx/artifact tooling). Operator may pull any in.
6. **Plugin members may not be individually deletable** — plugin-row MERGE/SUBTRACT executes at
   Phase 4 as archive-then-remove where possible, else a "superseded by repo copy — do not invoke"
   marker.
7. **Observation, not acted (§5-6):** five `CLOSED-*` rows still sit in the Q-roster **Open** table
   (OFCHAN, MNQSEL-1, R2VBUCK, R2FLOW, MNQDTL-CON-1) against the roster's own delete-on-close
   convention. Left for the roster owner.
8. **No discoverable standing:** the user/plugin-level challenge-era skills (d5–d9) have no repo
   retirement record — dispositions proposed fresh here.

Aim legend: **A1** fund/deploy at the four friendly firms · **A2** generate/validate candidates ·
**A3** operate-safely obligations · **A4** meta-process efficiency.

---

## Phase 1 — Inventory (one row per pursuit)

### (a) Active campaigns / lanes

| # | Pursuit | Standing | Last activity | Recurring cost | Aim | Falsifier / review | Residuals |
|---|---|---|---|---|---|---|---|
| a1 | **Four-firms prop-portfolio program** (umbrella) | ACTIVE | 2026-08-08 (TNEC ratified rides it) | operator: gate walks | A1 | §4 HARD 2026-11-08; F1 ruling owed | W1 intraday remeasure owed (every bust figure a LOWER BOUND) |
| a2 | **c1 rail + incumbent-eval operations** | ACTIVE — warm/disarmed | 2026-08-09 (M1 hardening PR); S2b build GO 08-08; token trade 08-07 | **weekly operator token-trade decision** (unrecoverable if missed); Fly/CrossTrade $ | A1/A3 | M1 gate; B7-REFIRE undischargeable until deploy | weekly recurrence **RULED 2026-08-16** — fresh-decision-per-week is the standing design (was UNRULED, queue row 0, at this inventory's own 2026-08-09 snapshot date). ⚠ *"R8 instrument UNDELIVERED" corrected 2026-08-09 — misnomer (closed Bulenox track); observation now booked in STATE forward triggers, read by the daily 07:04 radar. See [`a2 record`](../pursuits/a2-c1-rail-incumbent-eval-operations.md).* |
| a3 | **MNQ discovery pipeline** (TNEC intake · Route A/B campaigns · CapFLOW · dense-1m/instrument/W1 packets) | VERY ACTIVE | 2026-08-09 (CON-1 falsified; 3 Cursor packets frozen) | operator: near-daily sessions; databento per-pull | A2 | TNEC-1 gate; per-campaign preregs | SNAG register feed stopped 2026-08-03 — repair authored, **never ratified** (audit RED, object q4) |
| a4 | **Harvest / external-mechanism intake + sourcing radar** | ACTIVE-cadenced | 2026-07 burst; checkpoints 08-08/11-08 | low (on-demand) | A2 | harvest §4 + idle guard 2026-11-08 (self-converts) | — |
| a5 | **R&D tooling lane** (T2/T3/T4 gated adoption · wfo-runner v0 · sentinel Tier-2/3 promotion) | GATED-ACTIVE | 2026-08-08 (sentinel fix) | low | A4 | adoption ADR §7 dates; promotion before next slate | — |
| a6 | **Cursor-fleet worker capability** | ACTIVE | 2026-08-09 (3 frozen packets pending dispatch) | Cursor $ unverified | A2/A4 | per-packet claim manifests | — |

### (b) Parked / dormant lanes

| # | Pursuit | Standing | Last activity | Cost | Aim | Fields today | Residuals |
|---|---|---|---|---|---|---|---|
| b1 | **Aegis→6J transfer lane** | CATALOG hot, idle; no venue seat | 2026-07-29 (J4 re-run) | 0 standing | A1 | none (unbounded) | v0.3 measured record |
| b2 | **Striker MYM reconstruction** (S-MYM-ORC-02, TERMINAL lane) | idle | 2026-07 | 0 standing | A2 | none | — |
| b3 | **ORB-MNQ payability line** (orb_mnq · eodadv) | T2 payability FIRED; 15:30 exit barred | 2026-08-03 re-park | 0 standing | A2 | park lacks re-entry+expiry | sessconf_mnq continues under a3 |
| b4 | **Q-USOIL-1** (+ `usoil_regime_capture` legacy harness) | PARKED; **08-08 revisit lapsed unruled** (absent from audit + board) | 2026-07-10 record | 0 | none current (CFD-era instrument; spike-fader already REJECTED, ADR 2026-06-14) | park expired | harness body in CATALOG legacy |
| b5 | **Q-FUNDPOL-1** funded-phase policy | DORMANT (gate retired 08-04); K=4 frozen unspent | 2026-08-04 | 0 | A1 (successor venue) | no fields | §1–§5 method record retained |
| b6 | **Q-NAS-ECR-1** live edge-captured ratio | PARKED-DORMANT; **no fill source anywhere in estate** | 2026-08-04 note | 0 | A3 | no expiry | pre-reg retained; ECR concept |
| b7 | **ICT line** (PREREG-1M drafted NO-GO · Q-ICTEXP-1 scoped $0/K-free · `ict_mnq` _inbox body) | DORMANT, no dated obligation | 2026-08-06 (stop residual discharged) | 0 | A2 | none | ICTEXP wants a one-line operator K-freeness affirmation (§9) |

### (c) Standing explorations / feasibility threads

| # | Pursuit | Standing | Last activity | Cost | Aim | Note |
|---|---|---|---|---|---|---|
| c1 | **Q-XMEM-1** Mem0 memory sidecar | OPEN; frozen 07-16; **T0 never started** | 2026-07-16 | 0 | A4 | idle 3+ weeks |
| c2 | **Q-SIGID-1** signal-identity gap | OPEN — stranding **resolving**: S2b daemon build GO gives the ruled host §2b needs | 2026-08-06 intercept | 0 | A3 | offline limb stands (MNQ 0.68 / MYM 0.70) |
| c3 | **Q-TOM-SPX-1** | Layer-A RESOLVED-ABSENT 06-16; **formal DEAD close reserved** on an unrun native-Pine confirmation | 2026-06-16 | 0 | A2 | half-closed ~8 weeks |
| c4 | **Q-TVCOV-1** | verdicts landed 07-13; two residuals open | 2026-07-13 | 0 | A2 | residuals: MYM-AMBIGUOUS operator call; roll-rule pin → `databento-data` skill |
| c5 | **Q-MSCHAN-1** | DRAFTED-NOT-OPENED; **barred as scoped**; superseded pre-intake by Route B | 2026-08-05 | 0 | A2 | successor path already armored (fresh Q-ID + G0 + two GOs) |
| c6 | **Notion estate** (frozen workspace) | Phase-3 DELETE/ARCHIVE **unruled through the 07-01 AND 08-08 audits**; retirement §4 H held (no write needed; no Notion-only fact surfaced) | 2026-06-13 (Phase-2 DONE) | possible subscription $ (unverified) | A4 | the pending Phase-3 decision is an unowned residual |

### (d) Meta-belt (skills · frameworks · subscriptions)

| # | Item | Standing | Aim | Note |
|---|---|---|---|---|
| d1 | **Repo belt — 19 VC'd skills** | ACTIVE, gated (`check_skills_no_constants`, `check_skill_refs`) | A4 | churn watched at quarterly q2 (YELLOW watch flag) |
| d2 | `~/.claude/skills/brief-authoring` | ACTIVE — hosts the **canonical** skill-side `check_brief.py` | A4 | checker-canon split (repo vs skill copy) UNRULED |
| d3 | `~/.claude/skills/rule-0` | ACTIVE routing skill | A4 | — |
| d4 | `~/.claude/skills/trade-csv-reconcile` | duplicate of repo copy | A4 | repo copy authoritative |
| d5 | `~/.claude/skills/mql-developer` | MT5/MQL5 EA path retired (no-manual-trading; EA-conversion tombstone) | none current | no repo retirement record |
| d6 | `~/.claude/skills/notion-mcp-api-patterns` | exists solely for the retired Notion surface | none current | retirement ADR §0 called it the infrastructure-for-infrastructure marker |
| d7 | plugin `fxify-challenge` | challenge era closed; CFD estate retired | none current | durable successors retained: `prop-firm-challenge`, `c1-rail` |
| d8 | plugin `live-execution-journal` | manual live trading retired with DXTrade estate | none current | ECR concept lives in b6's pre-reg |
| d9 | plugin `inqhiori-algorithm` | duplicate (repo `inqhiori` + canon §14) | A4 | — |
| d10 | plugin duplicate set (brief-authoring, databento-data, pinescript-v6, programme-audit, strategy-validation, trade-csv-reconcile, notion-mcp-api-patterns) | repo copies authoritative | A4 | §0.5-6 mechanism |
| d11 | **TradingView** subscription | canonical feed source (CME TV exports) | A1/A2 | $ unverified |
| d12 | **databento** | cost-gated per-pull discipline (skill-enforced) | A2 | usage-billed |
| d13 | **Fly.io** (listener + `c1-signal-daemon`) | rail warm | A1/A3 | $ unverified |
| d14 | **CrossTrade** | rail bridge; 2-connection cap | A1/A3 | $ unverified |
| d15 | **Tradeify Select 100K account** | live eval environment; weekly-activity obligation | A1 | weekly token trade — unrecoverable if missed; observation booked 2026-08-09 (see a2) |
| d16 | **Cursor** | fleet workers | A2/A4 | $ unverified |

### (e) Aim-scale branches

| # | Branch | Standing |
|---|---|---|
| e1 | **First Passage program** — automated futures strategies at the four friendly prop firms | the Aim itself; own §4 armed (2026-11-08) |
| e2 | **Already-terminal register** — CFD estate · manual trading · challenge-era substrate · Pepperstone/OANDA/Dukascopy feeds · hard-core P-gates · Hermes NO-GO · Bulenox/futures-prop R6 era | terminal **with armor** (ADRs + tombstones; revival = fresh pre-registration by standing law). No action. |

---

## Phase 2 — Disposition proposals (all pending Phase-3 ratification)

**Test-substitution attestation:** no forbidden test (sunk cost · unbounded optionality · excitement ·
reach-down) was applied, and no permitted test below produces a disposition a forbidden one would
have — nearest call: b7 ICT, where "might be useful someday" would PARK it too; the applied test
differs by naming a **specific, dated, $0 re-entry step** (the ICTEXP affirmation) and an expiry that
converts to SUBTRACT. No new tests introduced.

All PARK expiries = **2026-11-08** (the quarterly gate the ADR §2.6 binds to — not an invented date).
At expiry, PARK → SUBTRACT absent explicit renewal (ADR §2.3).

| Row | Disposition | Test applied (from the permitted set) / rule cited |
|---|---|---|
| a1–a6 | **KEEP** (×6) | Serves a stated Aim (A1–A4) with live falsifier/review dates; entry records backfilled at Phase 4 |
| b1 Aegis→6J | **PARK**(re-entry: F3 registers a successor venue OR a 6J seat opens in book composition; expiry 2026-11-08) — ⚠ *F3 clause corrected 2026-08-16 in the ratified pursuit record: S1's "no successor migration now" ruling (2026-08-07) made it unreachable as an equal-weight route; the 6J-seat OR-fallback is the one actually open. See [`b1 record`](../pursuits/b1-aegis-6j-transfer-lane.md).* | No current venue route; idle 11 days; re-entry is a named external event |
| b2 Striker-MYM recon | **PARK**(re-entry: candidate clears its own lane gates AND a venue seat exists; expiry 2026-11-08) | Same class as b1 |
| b3 ORB-MNQ line | **PARK**(re-entry: new payability/cost-geometry evidence at an admissible venue; expiry 2026-11-08) | Park exists but lacks both required fields — backfill per ADR §2.3 |
| b4 Q-USOIL-1 | **SUBTRACT** (+ archive `usoil_regime_capture` per CATALOG stub convention) | **Expired PARK with no renewal case** (08-08 revisit lapsed unruled); note: not an oil-exposure bar — the live route is the MCL instrument-lane intake |
| b5 Q-FUNDPOL-1 | **PARK**(re-entry: F3 successor venue registered → fresh derivation, per its own note; expiry 2026-11-08) | Dormant row lacks fields; re-entry already named by the thread itself |
| b6 Q-NAS-ECR-1 | **PARK**(re-entry: F3 successor venue with live fills on a NAS100/MNQ-shaped leg; expiry 2026-11-08) — ⚠ *corrected 2026-08-16 in the ratified pursuit record: the incumbent Tradeify eval's `MYM1!`/`MNQ1!` occupancy release (2026-08-12) is the currently-open route, not F3 alone. See [`b6 record`](../pursuits/b6-q-nas-ecr-1.md).* | Same; discharge route currently nonexistent by dated record |
| b7 ICT line | **PARK**(re-entry: operator affirms Q-ICTEXP-1 §9 K-freeness → run the $0 one-way falsifier; expiry 2026-11-08 → converts SUBTRACT) | Bounded, dated, $0 re-entry — see attestation above |
| c1 Q-XMEM-1 | **PARK**(re-entry: a dated cross-surface-memory failure incident; expiry 2026-11-08) | Outside current Survive bounds (hours): frozen 3+ weeks with T0 unstarted |
| c2 Q-SIGID-1 | **KEEP** (review 2026-11-08) | Serves A3; its stranding is actively resolving via the S2b build |
| c3 Q-TOM-SPX-1 | **PARK**(re-entry: the brief-reserved native-Pine confirmation run; expiry 2026-11-08 → formal DEAD close) | Half-closed 8 weeks; §5-1 forbids dropping the reserved step, so the step **is** the re-entry |
| c4 Q-TVCOV-1 | **SUBTRACT-complete** (close roster row) with residuals assigned: MYM-AMBIGUOUS call → **operator**; ~~roll-rule pin → `databento-data` skill edit~~ **(post-ratification correction 2026-08-09: already discharged since 2026-07-13 — the inventory transcribed a stale roster "open item" without checking the target surface; see [`c4 record`](../pursuits/c4-q-tvcov-1.md))** | ADR §2.3 Residuals rule — verdicts already landed; only residual ownership was missing |
| c5 Q-MSCHAN-1 | **SUBTRACT** | **Duplicated by a higher-fidelity pursuit already retained** (Route B lane); successor armor already recorded (fresh Q-ID + G0 freeze + two GOs) |
| c6 Notion estate | **SUBTRACT-complete**: operator rules Phase-3 **cold archival**, closing the retirement ADR's own pending step | ADR §2.3 Residuals rule — the Phase-3 decision is an unowned residual, two audits overdue; its own §4 H held |
| d1 repo belt · d2 brief-authoring(user) · d3 rule-0 | **KEEP** (×3) | Serves A4, actively consumed; d2 residual assigned: checker-canon split → **operator one-line ruling** (later, not this run) |
| d4 trade-csv-reconcile(user) | **MERGE**(target: repo copy; verify-no-unique-content diff, archive verbatim, then remove) | **Duplicated by a higher-fidelity pursuit already retained** |
| d5 mql-developer | **SUBTRACT** (archive verbatim to `docs/ltm/notes/archive/skills/` first — user dir is not VC'd) | **Serves no currently stated Aim** (MT5/EA path tombstoned) |
| d6 notion-mcp-api-patterns(user) | **SUBTRACT** (archive first) | **Serves no currently stated Aim** (surface retired; Phase-2 migration long DONE) |
| d7 fxify-challenge(plugin) | **SUBTRACT** (per §0.5-6 mechanism; archive first) | **Serves no currently stated Aim** + duplicated by retained `prop-firm-challenge`/`c1-rail` |
| d8 live-execution-journal(plugin) | **SUBTRACT** (archive first) | **Serves no currently stated Aim**; residual (ECR concept) already owned by b6 |
| d9 inqhiori-algorithm(plugin) | **SUBTRACT** (archive first) | **Duplicated by a higher-fidelity pursuit already retained** (repo `inqhiori` + canon §14) |
| d10 plugin duplicate set | **MERGE**(target: repo copies; §0.5-6 mechanism) | **Duplicated by a higher-fidelity pursuit already retained** |
| d11–d16 subscriptions | **KEEP** (×6) | Each serves a named Aim through a live consumer (feed · data · rail · rail · venue · fleet); $ verification owed at Phase 3 (C-1) |
| e1 First Passage program | **KEEP** | The Aim; its own §4 falsifier armed 2026-11-08 |
| e2 terminal register | **no action** | Already subtracted with armor; standing law covers revival |

**Proposed disposition-differences vs status quo: 19** (b1–b7, c1, c3–c6, d4–d10). The §4 gate needs
**≥1 ratified** difference for `RESOLVED-LOADBEARING`.

---

## Consolidated read (§7 pass 3 — preliminary, completes at Phase 3)

The KEEP set is **6 active lanes + 2 standing explorations + the belt + 6 subscriptions + the
umbrella**. Fixed operator floor per week: the row-0 token-trade decision (unrecoverable), a3's
near-daily cadence, and the 2026-11-08 gate stack (four-firms §4 + GRAND §4 + F1 + harvest guard +
GSUB expiries now co-scheduled). ⚠ **Superseded 2026-08-09:** the claim that *"no written Survive
bound exists to check this against"* was wrong — the bound is the **≤5 operator-queue cap**
(concurrency, not hours; [`ADR`](../adr/2026-08-09-survive-bound-is-the-queue-cap.md)), which was in
force throughout; only its rationale had been deleted. **The aggregate read will never become
hours-arithmetic** — Rule 2 §5 #2 bars that denomination. The portfolio test is instead: does the
queue hold ≤5 and are items served in dependency order? Qualitative flag stands: a3 is the only lane
consuming near-daily hours; everything else is
event-driven or cadenced — the binding-resource question at Phase 3 is whether a3's cadence plus
row-0 fits the actual weekly budget.

## Phase 3 — RATIFIED 2026-08-09 · Phase 4 — EXECUTED

**Operator ratification:** in-session, 2026-08-09 — *"these are good judgements. proceed as
recommended"* — bulk ratification of the full table above (Phase 3 explicitly permits bulk).
**Verdict:** `RESOLVED-LOADBEARING` (19 ≥ 1) → [`closure`](closures/GSUB-1-closure-resolved-loadbearing.md).

**Phase-4 execution, exactly:**
- 37 pursuit records written to [`docs/pursuits/`](../pursuits/) (KEEP entry records · 8 fielded
  PARKs · armored SUBTRACTs · MERGE targets+residuals). Park-compliance hook: 8/8 PASS.
- d4/d5/d6 archived verbatim → [`docs/ltm/notes/archive/skills/`](../ltm/notes/archive/skills/),
  then removed from `~/.claude/skills/` (which now holds only the two KEEPs).
- d7–d10 **marker-only**: `anthropic-skills` verified platform-bundled (not in
  `installed_plugins.json`/`known_marketplaces.json`/`cache/`) — no deletion path exists.
- Q-TVCOV-1 roster row closed; Q-USOIL-1 retirements-record row flipped to SUBTRACT.

**Deliberately NOT executed at GSUB-1 close (named follow-ups, outside §5-3/§5-6 scope):**
lab-archival of `usoil_regime_capture` (since executed — see CATALOG / SESSIONS 2026-08-11g);
the Notion cold-archival account action; a formal Q-TVCOV-1 closure brief (**authored 2026-08-11**
as [`closures/Q-TVCOV-1-closure-falsified.md`](closures/Q-TVCOV-1-closure-falsified.md), not under
`docs/ltm/briefs/`).

<details><summary>Original Phase-3 instructions (superseded by the ratification above)</summary>

Per row: **ratify / adjust / reject**. Bulk options are legitimate ("ratify all KEEPs", "ratify all
PARKs as fielded", "ratify d5–d10 subtracts"). Low-reversibility note: the skill SUBTRACTs delete
non-VC'd files — Phase 4 archives verbatim copies first, so reversal stays possible. Cooling period
(ADR Phase 3 option) is available on any row; none is aim-scale, so none requires one by default.
On ratification: Phase 4 writes `docs/pursuits/` records (entry records for KEEPs; fielded PARKs;
armored SUBTRACTs), and the closure note lands per the spec §9 with the §4 verdict.

</details>

---

## Addendum — mid-run landings (2026-08-09, merge of origin/main)

PRs [#706](https://github.com/Joshua-Asante/first-passage-archive/pull/706) and
[#707](https://github.com/Joshua-Asante/first-passage-archive/pull/707) merged to main while Phases 1–2
ran: the instrument-lane SPEC resolved (MCL scored — geometry PASS, TNEC mechanism-owed; MES/MGC
`RE-ENTERED`; election left to operator) and Q-TNEC-CON-2's compression-break G0 froze (explore GO
unpaid; Family A displacement-fade killed at the cheap falsifier). **Both are a3-lane internals
under the TNEC intake gate — no inventory row changes** (granularity ruling §0.5-1); a3's
last-activity strengthens to 2026-08-09 post-inventory. The §0 anchors for `docs/briefs/INDEX.md`
/ `lab/CATALOG.md` / `docs/SESSIONS.md` predate these merges by hours; the §10 drift check covers
the delta at the next gate. The two pending operator items they add (instrument-lane election;
CON-2 explore GO) are campaign elections **inside** a3, not new pursuits — no intake-rule entry
records owed for them.
