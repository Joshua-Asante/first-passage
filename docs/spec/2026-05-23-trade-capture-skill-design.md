# Design — Trade Capture Skill (chat-driven Notion writer for ECR)

**Date:** 2026-05-23
**Status:** Approved by Joshua 2026-05-23; ready for implementation plan
**Spec path convention:** `docs/spec/` singular (per memory anchor `reference_docs_spec_singular.md`, 2026-05-10)

---

## §0 Rule 0 reads

Before any implementation step touches:

- `live_journal/ingest/enum_maps.py` — single source of truth for Notion-label ↔ Pydantic-enum mappings (FM.7: ad-hoc mappings elsewhere are SEV-1)
- `live_journal/signals/schema.py` — `SCHEMA_VERSION = "0.1"`, locked
- `live_journal/ingest/notion_client.py` — Notion REST client + data source IDs (Pre-Trade Log `a20976ee…`, Trade Journal `52b2196e…`); `DEFAULT_NOTION_VERSION = "2026-03-11"`
- `live_journal/ingest/transform.py` — validators that the chat-skill's writes must satisfy at ingest time
- The live Notion DB schemas (re-fetched 2026-05-23 via MCP; baked into `references/notion_schemas.md` in the skill)

The skill writes data that the ingest pipeline reads. Any field-naming or enum drift between the writer and these files breaks the ingest.

---

## §1 Context

The 2026-04-29 audit measured the live-vs-spec edge gap at ~3% on a 7-week window (~$$/$18K). The locked strategies fired ~$18K of edge; live captured ~$. The gap is dominated by pressing-the-button discipline: skipping signals that should be taken, decomposing single-position holds, slow fills, sized-down execution.

The ECR ingest pipeline (PR #100, Phase 0 complete, relocated to `live_journal/` per ADR 2026-05-23) reads Notion's Pre-Trade Log + Trade Journal databases and produces JSONL for `journal_review.py` reconciliation. The pipeline is fully built but **Notion data entry is manual** — Joshua types into Notion forms before the ingest can read anything.

Joshua's stated friction: "I rather not interface with Notion. I want to simply upload screenshot and some notes into Claude for the pre trade and post trade, and have it trigger the right questions to fill these entries and save in Notion."

This skill replaces the human→Notion typing step with a chat-driven flow. The ingest, reconciliation, and locked schemas stay unchanged.

---

## §2 Decision

Build a single Claude Code skill at `.claude/skills/trade-capture/` that:

1. **Fires on explicit phrases:** `pre-trade entry`, `post-trade entry`, plus synonyms `log a trade`, `capture a trade`, `log this trade`
2. **Asks targeted questions** via AskUserQuestion to fill the Notion schemas exactly (no field drift)
3. **Reads uploaded screenshots** for context-extraction (entry/SL/TP from TV charts, fill data from DXTrade exports)
4. **Previews the page before writing** — explicit `yes` required, no silent writes
5. **Writes directly to Notion via the Notion MCP** — uses Joshua's account auth, independent from the ingest `NOTION_TOKEN`
6. **Uploads screenshots via a new Python helper** at `live_journal/ingest/notion_files.py` — uses the integration token (shared with the ingest reader)

The skill ships with full functionality minus screenshot auto-upload. Once Joshua sets up the `NOTION_TOKEN` integration (Phase 0 §4 blocker), the helper activates and screenshot upload becomes automatic.

---

## §3 Architecture

```
.claude/skills/trade-capture/
├── SKILL.md                  # ~250 lines: triggers, flow, write patterns
└── references/
    ├── notion_schemas.md     # snapshot of both DB schemas (re-fetch via MCP at skill-build time)
    ├── enum_mapping.md       # subset of enum_maps.py relevant to the writer
    └── worked_example.md     # 2026-05-19 Aegis backfill (this design's anchor case)

live_journal/ingest/notion_files.py  # NEW — screenshot uploader (Python)
live_journal/ingest/notion_client.py # EXISTING — readers unchanged
```

### Data flow

```
Joshua: "pre-trade entry" + screenshot
   ↓
[SKILL] AskUserQuestion × ~3 → preview → write Pre-Trade Log via MCP
   ↓
(chat-session memory holds planned numbers + screenshot path)
   ↓
Joshua: "post-trade entry" + 2 screenshots
   ↓
[SKILL] search Pre-Trade Log → confirm match → extract from screenshots
   → ask gaps → preview → write Trade Journal via MCP
   → call notion_files helper to attach screenshots
   → update Pre-Trade Log Outcome + Linked Trade via MCP
   ↓
Both Notion rows fully populated.
Existing ingest pipeline reads them next month.
```

### Why this architecture

**Approach A (chosen)**: Pure chat-skill via MCP. Works today via Joshua's account auth. No new infrastructure beyond `notion_files.py`. Single source-of-truth stays Notion.

**Rejected B**: Skill writes local JSONL, ingest picks it up. Creates parallel feed (the ingest already reads Notion); breaks Screenshots field (file storage requires Notion).

**Rejected C**: Slash command → Python writer via `notion_client.py` only. Forces integration-token setup (blocked) and duplicates the MCP path for no benefit. (The Python helper for *screenshots* is justified because file upload isn't in MCP scope; full row writes aren't.)

---

## §4 Pre-trade flow

Triggered between the **anticipation trigger** and the **fire trigger**. Captures intent and accountability evidence.

### Inputs

- Trigger phrase: `pre-trade entry` (or synonyms)
- **Screenshot: required** — TV chart showing the anticipation setup. Held in chat-session memory; uploaded to Trade Journal Screenshots field at post-trade time. Rationale: prevents thin-air entries; ties the row to evidence of the actual setup.
- Optional notes from Joshua (macro context, anomalous PA)

### Question flow (max 4 prompts)

1. **Strategy?** `[Guardian / Striker DJ30 / Aegis / Striker NAS100]` — skill infers from screenshot strategy header when present
2. **Action (intent)?** `[Taken / Partial / Skipped / Discretion]`
3. *(if Skipped)* **Skip Reason?** Reads the live Notion select list at invocation (not the frozen snapshot) so additions don't require skill edits
4. **Notes?** (required if `Action=Discretion` or `Skip Reason=Other` — both are hard validator rules in `transform.py`; otherwise optional: macro context, anomalous price action)

### Captured but NOT written to Notion at pre-trade

Held in chat-session memory for post-trade comparison:
- Planned Entry / SL / TP / Lots / Risk %
- Pre-trade screenshot (path)

Rationale: the Pre-Trade Log schema has no slots for planned numbers (those live on Trade Journal as "Signal Entry/SL/TP/Lots"). Trade Journal is post-trade-only per Joshua's mental model. Session-memory bridges the gap so the post-trade flow can surface planned-vs-executed deltas.

### Aegis-specific reminder

When `Strategy=Aegis` and `Action ∈ {Taken, Partial, Discretion}`, preview includes:

> *Aegis anticipation is candle-forming estimate; actual signal entry/SL/TP captured at post-trade.*

No extra questions. The post-trade flow handles the estimate-vs-fire-vs-fill triangle for Aegis.

### Fields NOT asked (set automatically or omitted)

| Field | Pre-trade value | Reason |
|---|---|---|
| `Fired` | `False` (default) | Trade hasn't fired yet at pre-trade time |
| `Confidence` | unset | Joshua's call: not load-bearing at pre-trade |
| `Mechanical` | default (unset) | Defaults to unchecked; manually flipped only if relevant |
| `Strategy Version` | unset | Ingest backfills from `STRATEGY_DEFAULT_VERSION` |
| `Signal ID` | (auto-increment) | Notion-managed |
| `Event UUID` | unset | Ingest computes from `event_id_for(Signal ID)` |
| `Outcome` | unset | Filled at post-trade close-loop |
| `Counterfactual P&L` | unset | Filled at debrief (out of scope for this skill) |

### Preview format

```
=== Pre-Trade Log entry preview ===
Signal Time:    2026-05-19T16:15:00Z   (12:15 EDT)
Strategy:       Aegis
Action:         Taken
Skip Reason:    —
Notes:          "Aegis anticipation: candle forming below lower BB; …"

Held in chat memory for post-trade (NOT written now):
  Planned Entry/SL/TP:  158.871 / 158.715 / 159.188
  Planned Lots:         30.52
  Risk %:               1.5
  Screenshot path:      /tmp/cc-uploaded-img-abc123.png

Write Pre-Trade Log row? (yes / edit / cancel)
```

---

## §5 Post-trade flow

Triggered after the trade closes on DXTrade. Captures execution actuals + closes the loop on the Pre-Trade Log row.

### Inputs

- Trigger phrase: `post-trade entry` (or synonyms)
- **Screenshots: ≥2 required** — TV fire signal + DXTrade trade history. Optional additional screenshots (BE/trail evolution, etc.).
- Optional notes from Joshua

### Step 1 — Locate the Pre-Trade Log row

Query Notion via `notion-search` against Pre-Trade Log data source:
- `Strategy` = inferred from screenshot or asked
- `Signal Time` ≥ now - 24h (configurable)
- `Outcome` IN (`Open`, `blank`)

Branches:
- **Exactly 1 match** → confirm with Joshua ("Closing loop on Signal #N — Aegis 2026-05-19 12:15 EDT. Correct?")
- **0 matches** → backfill mode: capture both pre-trade intent and post-trade actuals in one preview
- **>1 matches** → numbered list, Joshua picks

### Step 2 — Extract from screenshots

| From | Fields |
|---|---|
| TV strategy card | Signal Entry / SL / TP / Lots, Risk %, ATR |
| TV chart caption | Signal Time, session/hour/day checks |
| DXTrade rows | Actual Entry, Actual Lots, Exit Price, P&L, fill timestamps |
| Chart BE/trail markers | BE evolution, trail evolution → Notes |

### Step 3 — Ask the gaps

Only fields not extractable from screenshots:
- **Exit Type** select (skill often infers: STOP marker → SL, "BE ACTIVE" → BE, etc.; always confirms)
- **Time zone** (first run of session only; persists for the chat)
- **Pre-trade Notes** (backfill mode only)
- **Backfill confirmation** when no Pre-Trade Log match

### Step 4 — Surface deltas

Compute and display:
```
Planned vs Executed:
  Entry slippage:   +X.X pips adverse / favorable
  Size delta:       ±X lots (sized up/down)
  Exit:             [type] [delta vs planned]
  P&L vs 1R:        X.XR  (Pine-R basis: Risk% × $200K)
```

The deltas are the load-bearing output. They drive the M-EC pattern (execution-quality measurement).

### Step 5 — Preview + confirm

```
=== Trade Journal row to create (linked from Pre-Trade Log #N) ===
Date:           2026-05-19T16:15:00Z
Strategy:       Aegis
Instrument:     USDJPY
Direction:      Long

  Pine signal (candle-close fire)
  Signal Entry:   158.871     (vs planned 158.871 — match)
  Signal SL:      158.715
  Signal TP:      159.188
  Signal Lots:    30.52
  Risk %:         1.5
  ATR:            0.11

  DXTrade execution
  Actual Entry:   159.014     (+14.3 pips adverse vs Pine signal)
  Actual SL:      158.715     (original — BE/trail in Notes)
  Actual TP:      159.188     (original — trail to 159.178 in Notes)
  Actual Lots:    25.00       (-5.52 lots from Pine 30.52, ~18% smaller)
  Entry Slippage: 0.143
  Exit Price:     158.868
  Exit Type:      BE          (BE stop fill, ~1.9 pips below BE level 158.887)

  Outcome
  P&L ($):        -2,299.50
  R Multiple:     -0.766      (Pine-R basis)
  Outcome (sel):  Loss

Notes:          [generated narrative]
Screenshots:    3 attached  → auto-uploaded via notion_files.py (if token set)

Write? (yes / edit / cancel)
```

### Step 6 — Write

On `yes`:
1. Create Trade Journal row via `notion-create-pages` → returns URL
2. **If backfill**: create Pre-Trade Log row with `Linked Trade` pointing to the Trade Journal URL
   **Else (close-loop)**: `notion-update-page` on existing Pre-Trade Log: set `Linked Trade`, `Outcome`, `Fired=True`
3. Invoke `notion_files.py` to upload all screenshots to Trade Journal Screenshots field (or instruct manual drag if token not set)
4. Return both page URLs

---

## §6 Screenshot uploader helper (`live_journal/ingest/notion_files.py`)

### Public API

```python
def upload_screenshots_to_trade_journal(
    trade_journal_page_id: str,
    screenshot_paths: list[Path],
    *,
    token: str = None,  # defaults to load_token_from_env()
) -> list[str]:
    """Upload N screenshots to Notion, attach to TJ page's Screenshots field.
    Returns list of Notion file_upload IDs (also written to the page property).
    """
```

### Wire path (Notion REST file-upload, version 2026-03-11)

1. `POST https://api.notion.com/v1/file_uploads`
   Body: `{"name": <path.name>, "content_type": <inferred>, "mode": "single_part"}`
   Returns: `{"id": <file_upload_id>, "upload_url": <signed_url>}`
2. `POST <signed_url>` with multipart form-data, key `file`, value: raw screenshot bytes (≤20 MB per file)
3. `PATCH https://api.notion.com/v1/pages/<trade_journal_page_id>`
   Body: `{"properties": {"Screenshots": {"files": [{"type": "file_upload", "file_upload": {"id": <id>}}, ...]}}}`

### CLI

```bash
python -m live_journal.ingest.notion_files attach \
    --trade <url-or-page-id> \
    <screenshot1.png> <screenshot2.png> ...
```

### Dependency

Requires `NOTION_TOKEN` integration setup (Phase 0 §4 blocker). Until set:
- Skill writes the row, returns URL, instructs manual drag
- Helper returns a clear error pointing at the Phase 0 setup steps

Once token lands: skill auto-invokes helper, screenshots upload silently.

### Tests

- Unit: mock httpx, verify the 3-call sequence (file_uploads → upload → page PATCH)
- Integration: optional, gated on `NOTION_TOKEN` env var (skip on CI / public clones)

---

## §7 Trigger phrases

| Phrase | Sub-flow |
|---|---|
| `pre-trade entry` | Pre-trade |
| `post-trade entry` | Post-trade |
| `log a trade` | Skill asks pre-or-post |
| `log this trade` | Skill asks pre-or-post |
| `capture a trade` | Skill asks pre-or-post |

The skill frontmatter description lists these explicitly so the dispatcher fires reliably. Screenshot upload alone (without a phrase) does NOT trigger — explicit per Joshua's choice (option 1 of 3, 2026-05-23).

---

## §8 Confirmation gate

**Always preview, always require explicit `yes`.** No silent writes. Joshua's choice (option 1 of 3, 2026-05-23) — adds one round-trip per entry, eliminates accidental-write risk.

Accepted confirmations: `yes`, `looks good`, `confirm`, `write`, `go`.
Rejected: anything else (treat as cancel).
Edit syntax: `edit Signal Entry 158.872` → re-preview with the change.

---

## §9 Known constraints

### C-1: MCP cannot upload files

Notion MCP (`notion-create-pages`, `notion-update-page`) writes text/select/number/date/relation fields fine. **It does not expose a file-field upload path.** Resolution: `notion_files.py` helper (§6) handles screenshots via REST.

### C-2: Pre-Trade Log lacks Screenshots field

Pre-trade screenshots cannot be stored in the Pre-Trade Log directly. Resolution: skill holds the path in chat-session memory and uploads to Trade Journal at post-trade time. If post-trade is in a different chat session, the pre-trade screenshot is lost — Joshua re-uploads at post-trade time.

### C-3: Action=Taken/Partial/Discretion requires Linked Trade

`transform.py` validators hard-fail if a Pre-Trade Log row with these Actions has no `Linked Trade`. Resolution:
- Backfill mode creates both rows in one transaction
- Close-loop mode requires Pre-Trade Log row to exist and updates it with `Linked Trade` at post-trade write time
- A pre-trade entry that creates a Pre-Trade Log row with `Action=Taken` and no `Linked Trade` will sit in the error sidecar until post-trade closes the loop (expected behavior, not a bug)

### C-4: Aegis estimation-vs-fire-vs-fill triangle

For Aegis specifically, three distinct numbers exist:
- **Anticipation estimate** (Joshua's guess at pre-trade time)
- **Pine fire** (candle close, known only at fire time)
- **DXTrade fill** (actual execution price)

For non-Aegis strategies, anticipation-estimate ≈ Pine fire (both knowable at anticipation time). Post-trade flow surfaces both deltas (estimate→fire is Aegis-specific; fire→fill is universal slippage).

### C-5: NOTION_TOKEN dependency for helper, not for MCP

The chat-skill (MCP) works today. Screenshot helper depends on the same integration token the ingest pipeline needs. Until Joshua finishes Phase 0 §4 setup:
- Skill writes rows successfully
- Helper errors with actionable setup pointer
- Manual screenshot drag is the workaround (~5 seconds per trade)

---

## §10 Worked example (2026-05-19 Aegis backfill)

Captured during this design session via direct MCP writes (validating the design before implementation).

**Inputs:** 3 screenshots (DXTrade trade history + TV fire signal + TV chart with BE→STOP)

**Pre-Trade Log row:** https://www.notion.so/36adc0b53c118176aa18d0e49c58d500
- Signal Time: 2026-05-19T16:15:00Z (12:15 EDT)
- Strategy: Aegis, Action: Taken, Fired: True, Outcome: Loss
- Notes: standard BB-below anticipation, no macro

**Trade Journal row:** https://www.notion.so/36adc0b53c1181a0a254fe82e824f723
- Signal: 158.871 / 158.715 / 159.188 @ 30.52 lots, Risk 1.5%, ATR 0.11
- Actual: 159.014 entry / 25 lots / 158.868 exit (BE), -$2,299.50, -0.766R
- Deltas: +14.3 pips entry slippage, -18% size, -1.9 pips BE fill

**Manual step needed (until token lands):** drag 3 screenshots into Trade Journal Screenshots field.

This is the design's anchor case — the question flow, preview format, and field mapping all validated against real data.

---

## §11 Forbidden moves

1. **No schema redesign.** Pre-Trade Log + Trade Journal schemas are owned by the ingest contract. Adding columns is a separate ADR (Notion-side first, then update `enum_maps.py`).
2. **No ad-hoc enum mappings in the skill.** `references/enum_mapping.md` must mirror `live_journal/ingest/enum_maps.py` byte-equivalently for the fields the skill writes. Drift = SEV-1 (FM.7).
3. **No silent writes.** Confirmation gate is load-bearing; bypassing it on "obvious" cases is forbidden.
4. **No bypassing the ingest contract.** Skill MUST write fields the ingest can consume; cannot invent fields outside the Notion schemas.
5. **No JSONL writes by the skill.** The skill is a Notion writer only. JSONL is ingest's job.
6. **No touching journal_review.py.** Reconciliation is downstream of this skill, separate scope.
7. **No modifying `notion_client.py` read paths.** Helper goes in new `notion_files.py`; readers stay untouched.

---

## §12 Falsifiable hypothesis

**H:** The skill reduces Joshua's per-trade Notion-typing time from current baseline to <60 seconds per pre-trade and <90 seconds per post-trade, while producing rows that pass `ingest signals` validation byte-equivalent to hand-entered rows for the same trade.

**RESOLVED if:**
- 10 consecutive trades captured via skill in week 1 post-deployment
- Each one writes both rows successfully on first attempt
- `ingest signals --month YYYY-MM` ingests them without error sidecar entries
- Joshua self-reports >50% friction reduction vs current Notion-form typing

**FALSIFIED if:**
- Question flow requires >6 prompts on average (too noisy)
- >20% of rows error-sidecar on ingest (field mapping wrong)
- Joshua falls back to direct Notion entry within 2 weeks (skill UX worse than the form)

**AMBIGUOUS if:**
- Mixed: skill works for some strategies (e.g., Guardian) but not Aegis (estimate-fire-fill triangle UX broken)

---

## §13 Gate criteria

Lock-able if:
- 50+ tests passing on the helper (`test_notion_files.py`)
- Skill reference docs are byte-snapshot-current vs live Notion schemas at lock time
- One full pre-trade + post-trade lifecycle captured via skill, both rows pass `ingest signals --month YYYY-MM` validation
- Worked example (this design's §10) re-runnable from the skill (not just direct MCP)

Reversal trigger: §12 falsifier fires within 4 weeks of deployment → revert to Notion-form entry, root-cause the friction, redesign question flow.

---

## §14 Audit hooks

```bash
# Skill files present
test -f .claude/skills/trade-capture/SKILL.md
test -f .claude/skills/trade-capture/references/notion_schemas.md
test -f .claude/skills/trade-capture/references/enum_mapping.md

# Helper present + importable
test -f live_journal/ingest/notion_files.py
python -c "from live_journal.ingest.notion_files import upload_screenshots_to_trade_journal"

# Enum mapping doc reflects live enum_maps.py for fields the skill writes
# (Strategy, Action, Skip Reason, Exit Type, Direction, Instrument, Confidence)
python scripts/check_skill_enum_mirror.py --skill trade-capture

# Schema snapshot is fresh (re-fetch + diff)
python scripts/check_skill_notion_schema.py --skill trade-capture

# Round-trip: skill-written row → ingest signals → JSONL → re-validate
python -m live_journal.ingest.ingest signals --month $(date +%Y-%m) --dry-run
```

---

## §15 Open items

1. **Schema-mirror checker scripts** (`scripts/check_skill_enum_mirror.py`, `scripts/check_skill_notion_schema.py`) are referenced in §14 audit hooks but don't exist yet. Either build them as part of this skill's deliverable, or document them as a follow-on tooling task.
2. **Counterfactual P&L on skipped rows** — Pre-Trade Log has a `Counterfactual P&L` field for skipped signals; this skill leaves it blank. Out of scope for v1; future enhancement could prompt Joshua at debrief time.
3. **Multi-account support** — design assumes single FXIFY account. When Joshua adds a second prop firm, the skill needs an Account select question.
4. **Pre-trade screenshot in a different chat session than post-trade** — currently lost. Future: persist to local disk under `data/screenshots/<event_uuid>.png` and have post-trade auto-find by Signal ID.
5. **Aegis estimation-vs-fire delta** — design captures fire-vs-fill but not estimate-vs-fire (because the estimate isn't captured in Notion at pre-trade time). If this delta matters for ECR, requires a Pre-Trade Log schema change.

---

## §16 Implementation order (to be planned by writing-plans)

Rough sequencing for the implementation plan that follows:

1. Build `.claude/skills/trade-capture/SKILL.md` + reference docs from this spec
2. Build `live_journal/ingest/notion_files.py` (Python helper with unit tests)
3. Build schema-mirror checker scripts (or defer to follow-on)
4. Dogfood: run the skill end-to-end on the next live trade
5. Backfill: capture any missed weeks via skill (replaces manual Notion entry for the backlog)

Detailed task breakdown happens in the implementation plan (writing-plans skill).
