# Venue-binding Phase 1–3 registry implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**AUTHORIZATION:** Accepted ADR [`2026-08-05-strategy-venue-binding-axis.md`](../../adr/2026-08-05-strategy-venue-binding-axis.md) — this plan is executable. Phase 0 (Accept) already landed 2026-08-22. This plan is **not** a GO to wire `M_edition`, edit `core/lifecycle.py`, or invent ACTIVE editions.

**Goal:** Land the owed venue-edition registry so "no Tradeify-shaped book entry is live" is a queryable fact, then finish the two leftover pointer/re-home steps. After this plan, `ops/venue_editions/Tradeify_Select_100K.md` exists, contains exactly three already-true rows, and has **zero** `ACTIVE` rows.

**Architecture:** One markdown ledger per firm-tier, same convention as `ops/instruments/*.md`. No code, no JSON, no validator. Book lifecycle stays in `docs/methodology/strategy_lifecycle.md` + `core/lifecycle.py`. Deployment stays `LEG_MAP` + rail config.

**Tech Stack:** Markdown only. Verification is grep + `scripts/check_adr_graph.py`.

## Global Constraints

- Record what is **already true**. Do not invent a fourth row, an ACTIVE edition, a successor venue, or a historical edition graph (ADR §5: register only what is live or under active consideration).
- T1 already fired (S1 recorded F2/F3 in prose). Do **not** rewrite S1 as an edition transition to "fix" T1.
- `M_edition` composition in ADR §2.4 is design-only. Do not touch `dd_protection.py`, `c1_sizing_host_reference.py`, `LEG_MAP`, `core/lifecycle.py`, Pine, or allocations.
- Empty edition set is a coverage fact, not a programme verdict (ADR §5).
- Docs-only. No tests-first Python. No new ADR.

## Rule 0 — production reads (verified 2026-08-23 on `origin/main` @ `5b9bd37`)

| Source | Anchor (`git log -1`) | What it pins |
|---|---|---|
| Owning ADR | `2c3b3c5` 2026-08-22 | Status `Accepted`; §7 Phase 1 still owed; T1 acknowledged; §2.6 registry shape |
| `core/lifecycle.py` | `027a729` 2026-08-14 | Ladder / `STRATEGY_KEYS` / `_validate_ladder` — must stay byte-untouched |
| `core/dd_protection.py` | `027a729` 2026-08-14 | `scaled_risk = BASE_RISK × DD_SCALE × lifecycle` — must stay byte-untouched |
| `ops/c1_rail/c1_sizing_host_reference.py` `LEG_MAP` | `027a729` 2026-08-14 | `dj30_mym` → Striker `cap_alloc` 69; `nas100_mnq` → Striker NAS100 `cap_alloc` 11 |
| `docs/methodology/strategy_lifecycle.md` L24 | `0723587` 2026-08-22 | Third-axis one-liner already present; "Registry still owed" |
| `CLAUDE.md` L120–121 | `0723587` 2026-08-22 | Third-axis pointer already present; "registry still owed" |
| [`2026-08-04-tradeify-venue-descope-eval-included.md`](../../adr/2026-08-04-tradeify-venue-descope-eval-included.md) Related | `2c3b3c5` 2026-08-22 | Cites venue-binding ADR; does **not** carry the exact §7 Phase 2 phrase |
| [`docs/spec/2026-07-27-third-leg-target-spec.md`](../../spec/2026-07-27-third-leg-target-spec.md) | `027a729` 2026-08-14 | Header already `SCOPE DEAD`; spec body must stay unedited (Trap #12) |

Pre-flight this session: `ops/venue_editions/` is absent; no `venue_editions` hit in `lab/CATALOG.md` or `docs/rejected_candidates.md`; `docs/briefs/INDEX.md` only mentions "venue editions" inside Q-SIGID-1 (unrelated).

## File Structure

| File | Responsibility |
|---|---|
| `ops/venue_editions/Tradeify_Select_100K.md` | **Create.** Three rows, zero ACTIVE. |
| `docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md` | **Pointer only.** Add the missing Phase 2 phrase. Do not rewrite §2. |
| `docs/methodology/strategy_lifecycle.md` L24 | **Discharge "still owed"** to the new path. Do not edit the two-axis table. |
| `CLAUDE.md` L120–121 | **Discharge "still owed"** to the new path. |
| `docs/spec/2026-07-27-third-leg-target-spec.md` | **Dated header note only.** Spec body unedited. |
| `docs/adr/2026-08-05-strategy-venue-binding-axis.md` | **Optional one-line Change History** that Phase 1–3 landed. No §2 edit. |

---

### Task 1: Create the Tradeify edition ledger

**Files:**
- Create: `ops/venue_editions/Tradeify_Select_100K.md`

**Row content (copy; do not invent):**

Use this exact table. `cap_alloc` and `leg_id` come from `LEG_MAP` (historical edition facts). Edition **state** is the 2026-08-04 fact. Deployment pointer records the rail slot as RETIRED/disarmed, not live.

| strategy | edition | state | cap_alloc | symbol | screen verdict + date | deployment |
|---|---|---|---|---|---|---|
| Striker | `Striker@Tradeify_Select_100K` | `WITHDRAWN` | 69 | MYM1! | venue de-scoped 2026-08-04 ([ADR](../../docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md)) | `leg_id=dj30_mym` RETIRED (rail retained, `dry_run=true`, F2 keep-warm) |
| Striker NAS100 | `Striker NAS100@Tradeify_Select_100K` | `WITHDRAWN` | 11 | MNQ1! | venue de-scoped 2026-08-04 ([ADR](../../docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md)) | `leg_id=nas100_mnq` RETIRED (rail retained, `dry_run=true`, F2 keep-warm) |
| ORB-MNQ-1 | `ORB-MNQ-1@Tradeify_Select_100K` | `SCREEN-DEAD` | — | MNQ1! | S7 occupancy SCREEN-DEAD 2026-08-04. Book-level payability remains FALSIFIED ([repark ADR](../../docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md)) — do not read SCREEN-DEAD as the book death | none — never deployed |

Header requirements on the new file:

- Title: venue-edition ledger for `Tradeify_Select_100K`.
- One-line charter: markdown, hand-maintained; T2 (stale-vs-`LEG_MAP`) is the owning ADR's quarterly catch.
- Banner: **Live edition set is EMPTY** — zero `ACTIVE` rows. That is the §1.3 fact.
- Banner: book-level Striker / Striker NAS100 stay `AUTHORIZED · MECHANISM @ 1.00×`. Venue-fit is not decay.
- Banner: `ORB-MNQ-1` book entry is PARKED / payability FALSIFIED; `SCREEN-DEAD` here is edition-only (ADR §2.4 ruling 2).
- Owner ADR link. No JSON sidecar.

- [ ] **Step 1: Confirm the directory is still absent**

```bash
test ! -e ops/venue_editions && echo "Phase 1 not yet run"
```

- [ ] **Step 2: Write the file** with the three rows and banners above. Relative links from `ops/venue_editions/` to `docs/adr/` are `../../docs/adr/…`.

- [ ] **Step 3: Prove the live set is empty**

```bash
ls ops/venue_editions/
# expect exactly Tradeify_Select_100K.md
grep -c "ACTIVE" ops/venue_editions/Tradeify_Select_100K.md
# expect 0. If a banner must mention the word, write it as `ACTIVE` never, or spell "active set is empty" in lowercase and keep the state token only on WITHDRAWN / SCREEN-DEAD.
```

If the banner needs the token `ACTIVE` to say "zero ACTIVE rows", that will fail the owning ADR's §10 hook (`grep -c "ACTIVE"` expect 0). **Do not put the literal `ACTIVE` anywhere in the file** until a future F3 edition is actually ACTIVE. Write "live edition set is empty" instead.

---

### Task 2: Phase 2 pointer remainder

**Already done (do not restated):**

- `docs/methodology/strategy_lifecycle.md` L24 third-axis sentence
- `CLAUDE.md` L120–121 third-axis sentence

**Still owed:**

1. Exact phrase on the 08-04 ADR, as a **new header line** (not a §2 rewrite):

```
**Re-expressed under the venue-binding axis:** WITHDRAWN is the Tradeify_Select_100K edition state; book authorization is unchanged. Ledger: [`ops/venue_editions/Tradeify_Select_100K.md`](../../ops/venue_editions/Tradeify_Select_100K.md).
```

Place it after the existing `**Related:**` line. Do not edit §2, §4, or the F1/F2/F3 forks.

2. Discharge the now-false "registry still owed" clauses so they do not silently restated a landed debt:

- `docs/methodology/strategy_lifecycle.md` L24: `Registry (\`ops/venue_editions/\`) still owed` → `Registry: [\`ops/venue_editions/Tradeify_Select_100K.md\`](../ops/venue_editions/Tradeify_Select_100K.md) (Phase 1 landed; live set empty).`
- `CLAUDE.md` L121: `registry still owed:` → `registry: [\`ops/venue_editions/Tradeify_Select_100K.md\`](ops/venue_editions/Tradeify_Select_100K.md) (live set empty).`
- 08-04 ADR Related clause `registry still owed` may stay as historical citation or be pointed at the file — prefer pointing at the file in the new header line only; do not rewrite the Related sentence's other claims.

- [ ] **Step 1: Add the 08-04 header line** (exact phrase present).

- [ ] **Step 2: Flip the two "still owed" one-liners** (lifecycle.md, CLAUDE.md). No other edits in those files.

- [ ] **Step 3: Confirm book authorization text is unchanged**

```bash
grep -n "AUTHORIZED" docs/methodology/strategy_lifecycle.md | head -3
# both Striker legs remain AUTHORIZED at book level
python scripts/check_adr_graph.py
# expect OK
```

---

### Task 3: Phase 3 dated note on the third-leg spec

**File:** `docs/spec/2026-07-27-third-leg-target-spec.md`

**Do:** insert one dated header note **above** the existing `SCOPE DEAD` banner (or immediately after the Status line). Do **not** edit §2, §7 thresholds, or any limb table in the body (Trap #12).

Suggested note (byte-copy allowed):

```markdown
> **2026-08-23 — §2.5 re-homing (venue-binding ADR, recorded not executed as a rescoring).**
> Limbs S1/S2/S4/S6 are EDITION (Tradeify venue facts). S5/S7 and R1–R4 are DEPLOYMENT
> and vacuous while the account is empty. T1–T5 and M1–M3 stay BOOK and remain the real bar.
> This note does not score any limb PASS/FAIL and does not lift SCOPE DEAD.
> Owner: [`2026-08-05-strategy-venue-binding-axis.md`](../adr/2026-08-05-strategy-venue-binding-axis.md) §2.5.
```

- [ ] **Step 1: Insert the note. Diff of the rest of the file is empty.**

```bash
# body below the header banners must be unchanged
git diff -- docs/spec/2026-07-27-third-leg-target-spec.md
# only header-region additions
```

---

### Task 4: Owning-ADR change-history line (optional, recommended)

Append one Change History row on [`2026-08-05-strategy-venue-binding-axis.md`](../../adr/2026-08-05-strategy-venue-binding-axis.md): Phase 1–3 landed; §2 byte-unchanged; T1 still acknowledged. Do not flip any other Status wording that would imply T1 un-fired.

- [ ] **Step 1: Add the row. No §2 / §4 / §5 edit.**

---

### Task 5: Verification (owning ADR §10 hooks 1–6 plus graph)

Run all of these. Fail the plan if any unexpected delta appears.

```bash
# 1. ladder + pin intact
grep -n "AUTHORIZED\|WATCH-1\|WATCH-2\|RETIRED" core/lifecycle.py | head -8
grep -c "_validate_ladder" core/lifecycle.py        # expect >= 2

# 2. live sizing composition unchanged
grep -n "scaled_risk" core/dd_protection.py

# 3. cap_alloc still in LEG_MAP; B3 still fixed
grep -n "cap_alloc" ops/c1_rail/c1_sizing_host_reference.py | head
grep -c "cap_firm / (1" docs/spec/c1_watch_realization_multiplier_layer.md   # expect 0

# 4. Phase 1 landed; live set empty
ls ops/venue_editions/
grep -c "ACTIVE" ops/venue_editions/Tradeify_Select_100K.md   # expect 0

# 5. T1 is historical — do not rewrite S1
grep -n "edition\|EDITION" STATE.md | head

# 6. book AUTHORIZED intact
grep -n "AUTHORIZED" docs/methodology/strategy_lifecycle.md | head -3

python scripts/check_adr_graph.py
```

Also:

```bash
git diff --stat -- core/lifecycle.py core/dd_protection.py ops/c1_rail/c1_sizing_host_reference.py
# expect empty
```

- [ ] **Step 1: Run the block. Paste the output in the PR / SESSIONS Shipped line.**

---

## Forbidden moves (this plan)

Copied from the owning ADR §5, plus plan-local temptations:

- Wiring `M_edition` into live sizing.
- Editing `core/lifecycle.py` (ladder, multipliers, `STRATEGY_KEYS`, `_validate_ladder`).
- Using an edition row to move a book lifecycle state (or vice versa).
- Reading `SCREEN-DEAD@Tradeify` as book-level death of ORB-MNQ-1.
- Retro-fitting BluSky / MFFU / Bulenox / historical CFD editions.
- Building a JSON registry or validator.
- Putting the token `ACTIVE` in the Tradeify ledger "so the hook has something to count".
- Rewriting S1 F2/F3 as edition transitions to un-fire T1.
- Scoring third-leg limbs PASS/FAIL in the Phase 3 note.

## Out of scope (later plans / later GOs)

- Phase 4 / T1 reachability — historical.
- W5 CI-from-`gates.yml`, grow-lane leftovers, substrate Phase 6, Call-4 beta-cohesion, disaster-stop, coldstore B/C, tradable-anomalies T2–T4 — sibling plans in this campaign, not this file.
