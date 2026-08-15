# Verdict pre-registration — Q-XMEM-1 (cross-surface memory sidecar pilot)

**Status:** `ARCHITECTURE FROZEN` (2026-07-16, v1.1)
**Pre-registered:** 2026-07-16 — **BEFORE T0** (no Mem0 install / no MCP write yet)
**Amended:** 2026-07-16 (v1.1, pre-T0 — no memories existed; a pre-registration revision, not Trap #12): ledger-skip≥1 now FALSIFIES (was ≥2, leaving =1 verdict-less); locked strategy parameters added to denylist; benefit limb operator-confirmed; contamination audit = full-export read (token grep supplemental, Trap M-AHF); explicit-add-only frozen; edge boundary restated as extraction LLM/embedder, not server host
**Parent brief:** [`docs/briefs/Q-XMEM-1-cross-surface-memory-sidecar-pilot.md`](../Q-XMEM-1-cross-surface-memory-sidecar-pilot.md)
**Reference instrument:** [mem0ai/mem0](https://github.com/mem0ai/mem0) (self-hosted preferred)

---

## What is frozen now

1. **Question (symptom form):** What is the cost of mutually invisible per-surface agent memory for soft mid-flight context, and can a time-boxed external memory sidecar reduce that cost without becoming a Rule-7 owner or displacing ledgers/SESSIONS?
2. **Allowlist (only):** operator prefs; open-thread pointers (path + one-line title); mid-flight notes destined for SESSIONS/ledger. **Explicit `add` calls only — no auto-add/auto-ingest of conversation content on any surface (v1.1, frozen with the allowlist).**
3. **Denylist (hard):** risk %, pyramid, MC anchors, LOCK hashes, lifecycle multipliers, firm-tier / `ACTIVE_FIRM` constants, authorization state as authority; **any locked strategy parameter — Pine inputs / `core/config/params.toml` values (SL/TP/ATR multipliers, session hours, proximity/trail/BE constants); paraphrase counts (v1.1)**; any `docs/ltm/**` or `lab/archive/**` ingest; Mem0-as-§0-evidence.
4. **Hypothesis H-XMEM-1:** ≥10 qualifying sessions in 14d of T0 + ≥1 **operator-confirmed** material benefit + 0 contaminations + 0 ledger-skips ⇒ keep; else abort (see parent §4).
5. **§6 verdict table** — copied from parent (RESOLVED / FALSIFIED / AMBIGUOUS-HOLD).
6. **Contamination audit method (v1.1):** full export + operator read of every stored memory at closure; denylist-token search is supplemental only (extraction LLM paraphrases — Trap M-AHF).

---

## §6 table (frozen)

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` | N≥10 within T0+14d **and** contamination=0 **and** ledger-skip=0 **and** operator-confirmed benefit≥1 | Keep optional MCP; optional one-line Rule-7 role note |
| `FALSIFIED` | contamination≥1 **or** ledger-skip≥1 **or** (N≥10 and confirmed benefit=0) | Tear down; wipe pilot memories; lesson capture |
| `AMBIGUOUS-HOLD` | N<10 by T0+14d (and no reject limb) **or** prefs-only / no cross-surface retrieval | Pause; re-test window = next 14d (T0′) |

v1.1 note: ledger-skip threshold was ≥2, which left the {contamination=0, ledger-skip=1, N≥10, benefit≥1} outcome with no verdict row and contradicted H’s “zero ledger-skip incidents.” The table now partitions every outcome.

---

## Definitions (frozen — identical to parent §4)

Qualifying session, Rule-7 contamination, ledger-skip, material handoff benefit, T0 — as in parent brief.

---

## Pilot tally path (frozen)

`docs/notes/pilots/q-xmem-1/TALLY.md` — created at T0; one row per qualifying session.

---

## Hosting preference (frozen preference, not a gate limb)

Self-hosted Mem0 server preferred. **v1.1 — the edge boundary is the extraction LLM + embedder endpoint, not the server host:** a self-hosted server with default config still sends payloads to an external LLM (OpenAI) for extraction. Acceptable configurations: (a) fully local LLM + embedder, or (b) external extractor reachable **only** by explicit-add allowlist-shaped payloads (never conversation auto-ingest). Extraction/embedder endpoints are recorded in the tally header at Phase 0 and the closure records which configuration ran. Switching host mid-pilot does **not** reset T0 unless the memory store is wiped (wipe ⇒ new T0).

---

## Commit discipline

This file + parent brief must be **committed before T0**. Pre-registration lineage (all pre-T0):

- v1.0 freeze: `fd710745ec1db0b21f2ffaf71b797a6d8481e1fe`
- v1.1 amendment (supersedes v1.0 as the frozen architecture): `1d4a866b5bcbb0fa9d6cf01211d929d4e2f3ccbb`

Any §6 edit after T0 requires closing AMBIGUOUS and opening a fresh Pre-Q (Known Trap #12).
