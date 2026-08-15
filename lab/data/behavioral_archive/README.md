# Behavioral Archive — Daily Execution System (pre-automation baseline)

**Created:** 2026-06-13 (Notion Phase-2 migration, per `docs/adr/2026-06-12-notion-surface-retirement.md` §2).
**Status:** `DONE_WITH_CONCERNS` — **database rows are NOT yet exported.** See §0.5-Q2 below.

## Why this directory exists

The ADR §2 residue table dispositions the **Daily Execution System databases** (Action Library, Daily Execution Log, Pre-Trade Log, Operational Risk Register, Reviews) to *"export historical rows → CSV at `lab/data/behavioral_archive/`; pre-automation behavioral baseline has analytical value for ECR work; no live replacement — Plan T telemetry is the successor."*

These databases served the **manual** trading loop. Trading is now automated end-to-end (TV → Copygram → DXTrade master → TradersConnect slaves), so they are vestigial — but their historical rows are a behavioral baseline worth preserving for ECR / TCA work.

## §0.5-Q2 LIMITATION — the Notion MCP cannot emit full database rows

**This blocks the automated CSV export.** The connected Notion MCP exposes `search`, `fetch`, `create`, `update`, and `move` tools only — **there is no row-dump / `query_data_sources` tool.** `fetch` on a database returns its *schema* (property definitions + SQLite DDL + views) but **not its rows**; `search` within a data source is semantic and capped at 25 results, so it cannot produce a faithful full historical dump.

Per the handoff §0.5-Q2 ("state the limitation and propose the alternative rather than partial-exporting silently"), the row export is handed to **Joshua via Notion native CSV export**:

### Joshua native-export steps (one per database)

For each database below: open it in Notion → top-right **•••** menu → **Export** → **Markdown & CSV** (or **CSV** only) → download → drop the `.csv` here under the target filename. (Notion native export emits full rows; the MCP cannot.)

| Database | Notion page-ID | collection:// | Target CSV |
|---|---|---|---|
| 📝 Pre-Trade Log | `df731a855e1d41e0aa9966355ed11b5a` | `a20976ee-3ae9-4e18-893c-e7e955f7cafb` | `pre_trade_log.csv` |
| ⚠️ Operational Risk Register | `0875d626e4444e90988bd339ddad2ea6` | `2051024f-04d0-408d-9b0f-e483e7b22b0f` | `operational_risk_register.csv` |
| Trade Journal | `a1614cd86569477a81fb111264bb53e4` | `52b2196e-eb84-4502-8272-3914bd062f80` | `trade_journal.csv` |
| Replication Health | `da7c42365a334970984fcae9b04173eb` | `34c70279-1a1a-42b5-a471-b594adeacc32` | `replication_health.csv` |
| Action Library / Daily Execution Log / Reviews | *not located by name via MCP (2026-06-13)* | — | `action_library.csv` / `daily_execution_log.csv` / `reviews.csv` |

> **NEEDS_CONTEXT (minor):** the three Daily-Execution-System DBs named in the ADR (Action Library, Daily Execution Log, Reviews) were **not enumerable by those names** via MCP search this pass. The behavioral *pages* that surfaced — Morning Anchor (`35bdc0b53c1181bd8b66d7882bb9b5e5`), Evening Wrap (`35bdc0b53c118195a5bdd4278ab5e916`), Sunday Review Sub 2 — Edge Captured + Behavioral (`35bdc0b53c118102a60ad1779ab68821`), Sunday Review Sub 3 — CTA Habits (`35bdc0b53c1181a985f7d65021b4b857`), Sick / Low-Energy Day Protocol (`35bdc0b53c118127a7d2cc3d4adc3574`) — appear to be Action-Library template/entry content. They may have been renamed/restructured since 2026-05-09. Disposition is identical regardless: native CSV export of whatever databases exist, plus markdown export of the template pages. The frozen (read-only) Notion workspace remains the reserve until Phase 3, so nothing is lost by deferring this to Joshua's native export.

## Captured schema — 📝 Pre-Trade Log (the exemplar)

The MCP *can* read schemas. Pre-Trade Log columns (use to validate the native CSV header):

`Signal` (title) · `Signal ID` (auto-increment) · `Signal Time` (date) · `Strategy` {Guardian, Striker DJ30, Aegis, Striker NAS100} · `Strategy Version` (text) · `Action` {Taken, Skipped, Partial, Discretion} · `Fired` (checkbox) · `Mechanical` (checkbox) · `Confidence` {High, Medium, Low} · `Skip Reason` {Sick/Low Energy, Travel/Connectivity, Override (manual), News/Binary Event, Tech/Platform, Collision Tier 3, Risk Gate, DD Throttle Active, Other, Signal Not Fired, Dropped Alert/Webhook, Copier Offline, Symbol Unmapped, Order Rejected} · `Outcome` {Win, Loss, Breakeven, Open, N/A (Skipped)} · `Counterfactual P&L` ($) · `Leak Leg` {Signal-Gen, Transmission, None} · `Event UUID` (text) · `Reconcile Fingerprint` (text) · `Linked Trade` (relation → Trade Journal) · `Notes` (text)

(Schemas for the other three databases can be captured the same way via `notion-fetch` on their page-IDs if needed before the native export.)

## When CSVs land

Once the native exports are dropped here, this README's status flips to `DONE`, and the CSVs become the pre-automation behavioral baseline for ECR/TCA (Plan T) work.
