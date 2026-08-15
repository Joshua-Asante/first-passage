# Live-docs stale-claims audit — 2026-07-29

**Scope:** `docs/` (briefs, adr, notes, methodology, governance) + root operational
truth surfaces (`STATE.md`, `CLAUDE.md`, `LOCK.md`, `REPO_MAP.md`, `README.md`,
`PIPELINES.md`, `docs/SESSIONS.md`, `docs/operational_rules.md`, instrument ledgers,
agent skills that agents treat as live).
**Method:** Canonical posture from `CLAUDE.md` §Live-execution posture + `STATE.md`
operator queue + ADRs 2026-07-16→2026-07-28; high-churn phrase search; selective
link scan on key live docs.
**Constraint:** Read-only evidence gathering; this note records findings only —
no CLAUDE/STATE/ADR “fixes” in this pass.
**Not duplicated here:** methodology 90-day rebound review. Expected path
`docs/notes/audits/2026-07-29-methodology-90day-rebound-review.md` was **absent
from this worktree** at audit time (Glob/index may have referenced a planned or
other-worktree file). `STATE.md` still lists the 2026-07-29 methodology gate as
a forward obligation — that review’s substance is out of scope for this note.

Canonical owners for live posture (do not restate risk % / MC anchors here):
[`CLAUDE.md`](../../../CLAUDE.md) · [`STATE.md`](../../../STATE.md) ·
[`docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md`](../../adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md) ·
[`docs/adr/2026-07-22-challenge-era-substrate-retirement.md`](../../adr/2026-07-22-challenge-era-substrate-retirement.md) ·
[`docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json`](../rail_build/M1_MONITORING_ACCEPTANCE.json).

---

## Executive summary

| Severity | Count |
|---|---|
| HIGH | 6 |
| MEDIUM | 9 |
| LOW | 6 |

Priority cleanup is the HIGH set (agent/live-ops misleading) plus INDEX hygiene
and STATE queue/metadata lag. Historical ADRs that correctly narrate a past
decision and carry `Superseded-in-part-by` / banner notes are **not** listed
unless a *living* surface still asserts the superseded claim without a pointer.

---

## Findings

### HIGH

| ID | Location | Claim | Conflicts with | Disposition |
|---|---|---|---|---|
| **H1** | [`CLAUDE.md`](../../../CLAUDE.md) L14 (substrate bullet) | “Phase 2 multiplier spine **retiring**”; “destructive **Phases 3–6** remain separately gated” | Substrate ADR status + git: Phase 2 **MERGED** (`ff3510d`); Phase 3 **CODE_LANDED / merged** (`bd92d8e`); remaining gate is **Phases 4–6** | **Update** pointer language to match ADR header (Phase 2 MERGED, Phase 3 CODE_LANDED, Phases 4–6 gated) |
| **H2** | [`README.md`](../../../README.md) L5–6 | Locked-book live-execution “dormant (… **futures-prop NO-GO**)” with no c1/prop-portfolio caveat | Live path is c1 Tradeify Select 100K rail (disarmed); R6 NO-GO is **locked-book fan-out** only | **Update** — one sentence: locked-book futures-prop NO-GO; prop-portfolio c1 rail built/disarmed (link CLAUDE posture) |
| **H3** | [`ops/instruments/ES.md`](../../../ops/instruments/ES.md) L5 | “the **sole active self-funded lane** is Aegis→M6J” | Self-funded PARKED 2026-07-16; standing program = prop-portfolio c1 ([`6J.md`](../../../ops/instruments/6J.md) already repaired 07-28) | **Update** header prose (same class as D7 XAUUSD/6J repair) |
| **H4** | [`docs/briefs/INDEX.md`](../../briefs/INDEX.md) “Open” table | Rows for Q-RAIL-1, Q-PYRPARITY-1, Q-INVENTORY-1, Q-BUSTGATE-1, Q-KBUDGET-HARVEST-1, Q-GEOFIT-1 still under **Open** while Status cells say CLOSED | INDEX convention (L8–9): closed Qs move to LTM / Recently closed; Open = open/dormant only | **Update** — move CLOSED rows to “Recently closed”; leave only truly open Qs (FUNDPOL, XMEM, TOM, TVCOV, SIGID, …) |
| **H5** | [`docs/briefs/Q-RAIL-1-c1-execution-rail-go-live-scoping.md`](../../briefs/Q-RAIL-1-c1-execution-rail-go-live-scoping.md) L35 | “c1 … **discharged** the four-firms ADR §4”; “ORB-MNQ-1 is a second admitted CANDIDATE”; “**no live fills exist anywhere**” | §4 **WITHDRAWN** 2026-07-22; ORB-MNQ **PARKED** then reconstruction TERMINAL framing; canned fills exist (B6/SIM) — strategy-signal fill still absent | **Leave-as-historical** with banner, or archive pointer at top → withdrawal ADR + CLAUDE fill distinction. Do not treat as live program state |
| **H6** | [`STATE.md`](../../../STATE.md) pointer-log ~L1012 (Class-S history block) | “program §4 still **discharged** by #1” | Withdrawal ADR + CLAUDE: §4 **undischarged** | **Update** that historical narrative block with a one-line supersession note (Trap #12: do not rewrite the 07-15 discharge story; annotate withdrawal) |

### MEDIUM

| ID | Location | Claim | Conflicts with | Disposition |
|---|---|---|---|---|
| **M1** | [`STATE.md`](../../../STATE.md) L3 + operator queue item 4 | `Last curated: 2026-07-27`; item 4 still framed as owed then ends with pins verified / `48/32` — SESSIONS 07-29 has re-run → `51/29`, still `AMBIGUOUS (d)` | Top of STATE has 07-28/29 content; SESSIONS supersedes `48/32` | **Update** Last curated → 2026-07-29; rewrite item 4 to “pins verified; re-run done; D1 still blocked; `(d)` adjudication open” |
| **M2** | [`docs/notes/rail_build/B7_REFIRE_PLAN_2026-07-27.md`](../rail_build/B7_REFIRE_PLAN_2026-07-27.md) ~L95–103 | Checklist still marks notification owed; status note says RESOLVED still owes items **5, 6, and 10** | `M1_MONITORING_ACCEPTANCE.json`: items **6 + 10 DONE**; only item 5 (+ signoff) owed | **Update** checklist to match acceptance JSON (or stamp plan SUPERSEDED → Fri desk card) |
| **M3** | [`docs/adr/2026-07-17-c1-rail-build-account-registration-go.md`](../../adr/2026-07-17-c1-rail-build-account-registration-go.md) L12 | Layer line: “`ACTIVE_FIRM` **stays FXIFY**” | Header already has `Superseded-in-part-by` substrate ADR; live `ACTIVE_FIRM=Tradeify_Select_100K` | **Leave-as-historical** but add inline strikethrough / “superseded — see header” on L12 so Rule-0 readers don’t miss the edge |
| **M4** | [`docs/adr/2026-07-10-strategies-never-locked-lifecycle-governance.md`](../../adr/2026-07-10-strategies-never-locked-lifecycle-governance.md) status header | Phase-2 “`ops/cli.py lots` read-only auth surface are **DONE**” | Substrate Phase 2 **deleted** that surface | **Update** header: lots surface retired Phase 2; lifecycle haircuts remain in `dd_protection` only |
| **M5** | Pre-regs asserting §4 already discharged: e.g. [`2026-07-16-class-s-c1-lifecycle-haircut-regime-remc-preregistration.md`](../../briefs/pre-registration/2026-07-16-class-s-c1-lifecycle-haircut-regime-remc-preregistration.md), candidate-2 / Aegis-6J pre-regs, [`Q-COMPOSE-1` closure](../../briefs/closures/Q-COMPOSE-1-closure-falsified.md) | “§4 already discharged / remains discharged” | Withdrawal ADR | **Leave-as-historical** + top banner pointing to withdrawal; do not bulk-rewrite frozen pre-regs |
| **M6** | [`docs/briefs/2026-07-12-08-08-packet-pretriage.md`](../../briefs/2026-07-12-08-08-packet-pretriage.md) L34 body | Still states “`ACTIVE_FIRM` stays FXIFY” / rail gated | Banner at top already marks superseded; body unedited | **Leave** if banner is load-bearing; optional body footnote. Prefer agents read banner |
| **M7** | [`ops/instruments/MYM.md`](../../../ops/instruments/MYM.md) / [`MNQ.md`](../../../ops/instruments/MNQ.md) status | “**no live fill yet**” without strategy-signal vs canned distinction | CLAUDE: canned fills exist; no strategy-signal fill | **Update** wording to match CLAUDE distinction (LOW→MEDIUM because desk cards cite ledgers) |
| **M8** | [`docs/operational_rules.md`](../../operational_rules.md) | Link `../lab/archive/usoil_rdm/RESULTS.md` | Path missing (`lab/analysis/legacy/usoil_regime_capture` exists; `usoil_rdm` does not) | **Fix link** or retarget to current owner |
| **M9** | [`STATE.md`](../../../STATE.md) owed block ~L56–60 | Q-CAPALLOC re-run “blocked behind … dashboard-verified” / “unchanged” harness | Pins verified 07-29; re-run executed; `51/29` / still `AMBIGUOUS (d)` per SESSIONS | **Update** owed block to match queue item 4 + SESSIONS (once M1 done) |

### LOW

| ID | Location | Claim | Conflicts with | Disposition |
|---|---|---|---|---|
| **L1** | [`docs/adr/2026-06-07-decompound-remc-hold.md`](../../adr/2026-06-07-decompound-remc-hold.md) §4 | Schedule with `time_to_pass.py --regime-check` / C2→C0 alignment | D2 retired that check 2026-07-22; STATE forward board correct | **Banner** on §4: regime limb may remain; C2→C0 companion retired |
| **L2** | [`docs/adr/2026-07-15-sfrisk-1-t1-admitting-successor-risk-framework.md`](../../adr/2026-07-15-sfrisk-1-t1-admitting-successor-risk-framework.md) | Rides “standing quarterly regime-check cadence” with decompound-HOLD | Same D2 retirement | **Banner** |
| **L3** | [`PIPELINES.md`](../../../PIPELINES.md) P5 / summary | Accurate disarmed/B6 but thin on M1 item progress / 07-27–28 fills | CLAUDE / RUNBOOK richer | **Optional refresh** — not wrong, incomplete |
| **L4** | XAUUSD PROFILE YAML `mechanism: trend-following` / `verdict: LIVE` | “LIVE” cell vs header DORMANT venue | Orthogonal axes intentional (strategy AUTHORIZED vs venue closed) — already explained in header | **Leave** — maybe rename cell to `AUTHORIZED` later to reduce agent confusion |
| **L5** | [`docs/briefs/2026-07-14-b3-multiplier-spine-forward-relevance-disposition.md`](../../briefs/2026-07-14-b3-multiplier-spine-forward-relevance-disposition.md) | KEEP-dormant / do not delete `calc_multiplier` | Phase 2 **deleted** the spine | **Banner** “superseded by substrate §2-D” |
| **L6** | Dual raised-bar-text / WSTRUCT adjudication (SESSIONS 07-29 Open/next) | Two texts of `index-intraday-ohlcv-directional-timing-2026-07-21` | Not a live-ops posture claim; research integrity | **Operator/Cursor chip** — out of posture scope; track separately |

### Orphans / dead pointers (sampled)

| Path | Issue | Disposition |
|---|---|---|
| `docs/operational_rules.md` → `lab/archive/usoil_rdm/RESULTS.md` | Missing | Retarget (M8) |
| `B7_REFIRE_PLAN` → `c1_rail_http_server.py:152` | Line-anchor link form not a real path | Cosmetic; cite file without `:line` or use code citation |
| `ops/live_journal/` (USDCAD BPC-001) | Already annotated CONTINGENT-FORWARD unreachable (tier-c 07-28) | Leave annotated; no reopen |
| Notion IDs in INDEX “Recently closed” | Redirect map exists | Leave; not live Open board |

### Already repaired (do not re-open)

- `ops/instruments/6J.md` / `XAUUSD.md` header vs YAML (D7 2026-07-28)
- `.claude/skills/prop-firm-challenge/SKILL.md` posture block (2026-07-24)
- `.claude/skills/handoff-verify/SKILL.md` live posture line
- `REPO_MAP.md` accounts/lots retirement language
- CLAUDE fill distinction (strategy-signal vs canned) — present

---

## Suggested cleanup order (top 10)

1. **H1** — `CLAUDE.md` substrate phase pointer (agents read this first)
2. **H2** — `README.md` futures-prop / c1 one-liner
3. **H3** — `ES.md` sole-active-lane prose
4. **H4** — `docs/briefs/INDEX.md` Open-table hygiene
5. **M1 + M9** — `STATE.md` Last curated + queue item 4 + CAPALLOC owed block
6. **H6** — Annotate STATE Class-S “§4 still discharged” history line
7. **M2** — Sync or supersede `B7_REFIRE_PLAN` vs M1 acceptance JSON
8. **H5** — Banner on Q-RAIL-1 brief (closed but still cited)
9. **M3 + M4** — GO ADR L12 + lifecycle ADR “lots DONE” header tweaks
10. **M5** — One shared “§4 withdrawal” banner pattern for frozen pre-regs that still say discharged

---

## Open questions (operator adjudication)

1. **Q-CAPALLOC-1 `AMBIGUOUS (d)` after verified pins** — SESSIONS says the `(d)` premise is stale (flips were under unverified pins; pins now verified) but converting to RESOLVED is a §6 / Trap #12 call. Agent must not bank RESOLVED.
2. **M1 item 5 evidence bar** — Is a non-zero MYM entry at `dry_run=true` still required for RESOLVED after the 07-28 JSON seam proof + qty-0 MNQ triad, or does operator accept a different evidence class?
3. **Methodology 90-day review (due 2026-07-29)** — Artifact not present in this worktree; is the review done elsewhere, deferred, or still owed today?
4. **INDEX closed-in-Open** — Keep CLOSED rows in Open for “priority series” narrative, or enforce convention strictly?
5. **Frozen pre-reg §4 “already discharged”** — Banner-only vs leave untouched (historical freeze fidelity)?

---

## Method notes

- Phrase searches: `ACTIVE_FIRM`/`FXIFY`, continuous-lot/`calc_multiplier`, §4 discharg*, sole active lane, no live fill, Pepperstone executable pin, C2→C0, MYM/MNQ reconstruction open, Phases 3–6.
- Link scan (key roots + sample rail notes): 445 relative links checked; 2 missing (usoil_rdm; line-anchored py path).
- LTM not exhaustively searched; catalogs used for orientation only.
