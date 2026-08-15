# [Q-XMEM-1] — Cross-surface agent-memory sidecar pilot

**Status:** `OPEN`
**Authored:** 2026-07-16
**Amended:** 2026-07-16 (v1.1, pre-T0) — critical review (`claude/q-xmem-1-briefs-review`): ledger-skip gate hole closed (=1 was verdict-less); locked strategy parameters added to denylist; contamination audit upgraded from token-grep to full-export read (Trap M-AHF); hosting limb restated around the extraction-LLM boundary + explicit-add-only frozen; benefit limb tightened to operator-confirmed; Phase-3/§6 verdict-date conflict fixed. **No T0, no install, no memories existed at amendment time — this is a pre-registration revision, not Known Trap #12.**
**Closed:** `N/A`
**Authors:** Joshua (authority) + Cursor (structure; prior fit canvas)
**Parent question:** `N/A`
**Sub-questions opened:** none
**Loop:** Inquire-phase Pre-Q — gates whether a scoped external memory sidecar earns a keep/abort after a time-boxed pilot, without becoming a Rule-7 owner
**Artifact path:** `docs/briefs/Q-XMEM-1-cross-surface-memory-sidecar-pilot.md`
**Verdict pre-registration:** [`docs/briefs/pre-registration/Q-XMEM-1-verdict-preregistration.md`](pre-registration/Q-XMEM-1-verdict-preregistration.md)
**Fit canvas (non-canonical):** Cursor canvas `mem0-repo-fit.canvas.tsx` (IDE canvases dir, outside git) — research only; this brief owns the gates

> **Scope discipline (binding):** this Pre-Q freezes the **pilot architecture** (what may be stored, what is forbidden, how §6 fires). It does **not** install Mem0, wire MCP, or start the clock. T0 = first successful cross-surface memory write under the allowlist below.

---

## §0 — Rule 0 reads (production-source verification)

Files / surfaces read **before** authoring this brief (2026-07-16, local tree `@ 4617007`; `origin/main` tip `4caca7f` is the merge of the same root-doc charter — no mem0/memory-sidecar delta on `origin/main ^HEAD`):

| # | Artifact | Anchor | What it establishes |
|---|---|---|---|
| 1 | `docs/operational_rules.md` §7 | `4617007` (2026-07-15 23:41 -0400) | Canonical owners: SESSIONS narrative; top-entry Open/next; **`MEMORY.md` + memory files** for durable atomic facts; mirrors must link, never restate |
| 2 | `docs/operational_rules.md` §10 | same `4617007` | Instrument ledgers exist **because** “per-surface memory is mutually invisible” (Claude Code / claude.ai / Cursor) |
| 3 | `docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md` §3 | file last-touch `fad8984` (2026-07-14); content verified 2026-07-16 | Alternatives table: **status quo SESSIONS + memory files ruled out** for instrument collisions — collision happened *with both in place*; memory is per-surface |
| 4 | `docs/spec/2026-06-27-session-log-rolloff-design.md` | last-touch `fad8984` | SESSIONS keep-N + LTM archive; durable atoms already live in MEMORY.md / git — SESSIONS is not a semantic index |
| 5 | `docs/ltm/README.md` | last-touch `fad8984` | LTM deliberately search/index-excluded; catalog → exact Read |
| 6 | Cheap falsifier (PARENT, <5 min) | 2026-07-16 | (a) `rg mem0\|OpenMemory` over tracked `*.{md,py,json,…}` → **0 hits**; (b) repo-root `MEMORY.md` → **absent**; (c) CC primary `…/memory/MEMORY.md` → **present** (mtime 2026-07-14); (d) sampled worktree project dirs → **no** `MEMORY.md` — empirical silo; (e) no `mem0` in `~/.cursor/mcp.json` (file absent or no match) |

**§0 does not read** locked Pine, `dd_protection.py`, or MC pins — this pilot must not touch them.

---

## §1 — Context & motivation

Multi-surface agent work (Cursor + Claude Code + occasional claude.ai) is the operating norm. Durable state is already well-owned in git (SESSIONS, ADRs, STATE, instrument ledgers, lab CATALOG). The residual pain is **soft / mid-flight** context: operator prefs, “what’s open on the other surface,” path pointers that are not yet ledger/ADR material. Rule 10 and ADR 2026-06-11 already name the silo; the cheap falsifier above shows `MEMORY.md` lives only on the primary CC project path and is invisible to worktrees and to Cursor.

A 2026-07-16 fit assessment against [mem0ai/mem0](https://github.com/mem0ai/mem0) concluded: high fit for cross-surface prefs/pointers; **anti-fit** as a second owner of Rule-7 values or as a ledger substitute. This Pre-Q time-boxes that conclusion into a falsifiable keep/abort.

---

## §2 — Prior art / lineage

- [`docs/operational_rules.md`](../operational_rules.md) §7 / §10 — owners + silo rationale (binding)
- [`docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md`](../adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md) — memory-only already FALSIFIED for instrument anti-collision; ledgers stay
- [`docs/spec/2026-06-27-session-log-rolloff-design.md`](../spec/2026-06-27-session-log-rolloff-design.md) — SESSIONS roll-off; not a semantic store
- [`docs/ltm/README.md`](../ltm/README.md) + lab STM/LTM — spent corpus must stay catalog-gated, not fuzzy-recalled
- [`docs/adr/2026-07-14-cc-cursor-surface-allocation.md`](../adr/2026-07-14-cc-cursor-surface-allocation.md) — surface roles; does not solve shared scratch memory
- Fit canvas 2026-07-16 (non-canonical research) — candidate tool = Mem0; hosting preference = self-hosted
- **No prior Q-XMEM-*** — genuinely novel Pre-Q ID

---

## §3 — Question (Q-XMEM-1)

**Pre-Q gate test (Discipline Check #5):** symptom-only rephrase holds — the cost is mutual invisibility of soft agent context across surfaces; no product or hosting choice is baked into the question sentence. Mem0 is the **reference instrument** for the pilot (like decompound-remc for Q-SFRISK-1), not the question.

**Q-XMEM-1:** What is the cost of operating with mutually invisible per-surface agent memory for soft mid-flight context (prefs, open-thread pointers), and can a time-boxed external memory sidecar reduce that cost **without** becoming a second owner of Rule-7 facts or displacing instrument ledgers / SESSIONS?

---

## §4 — Falsifiable hypothesis (H-XMEM-1)

**H-XMEM-1:** If a Mem0 sidecar (self-hosted preferred; edge boundary = extraction LLM/embedder endpoint, not server host — see §5; explicit-add-only) is wired to Cursor **and** Claude Code under one `user_id`, with an allowlist of (a) operator prefs, (b) open-thread **pointers** (path + one-line title), (c) mid-flight notes that will later land in SESSIONS/ledger — and a hard denylist of Rule-7 owned values — then after ≥10 qualifying sessions within 14 calendar days of T0, the sidecar produces ≥1 documented material handoff benefit **and** zero Rule-7 contaminations **and** zero ledger-skip incidents. Otherwise the sidecar is net-harmful or useless and is aborted.

**Falsifier (reject H-XMEM-1 if any):**
- ≥1 Rule-7 contamination (owned value stored in Mem0 **or** cited from Mem0 as authority in a session), **or**
- ≥1 ledger-skip incident attributed to Mem0 (“mem0 had it” → skipped `ops/instruments/<SYMBOL>.md` read) — v1.1: was ≥2, which left ledger-skip=1 with no verdict row and contradicted H’s “zero ledger-skip incidents”, **or**
- after ≥10 qualifying sessions, **zero** operator-confirmed material handoff benefits logged

**Accept H-XMEM-1 if (all):**
- ≥10 qualifying sessions within 14 days of T0, **and**
- Rule-7 contamination count = 0, **and**
- ledger-skip count = 0, **and**
- ≥1 **operator-confirmed** material handoff benefit logged (pointer or pref retrieval that prevented re-derivation across surfaces; agent-logged candidates count only after operator confirmation in the tally)

The three limbs now partition every outcome: any contamination or ledger-skip ⇒ FALSIFIED; otherwise N and benefit counts route to RESOLVED / FALSIFIED / AMBIGUOUS-HOLD per §6.

**Ambiguous-hold if:**
- <10 qualifying sessions by T0+14d, **or**
- benefits only on single-surface prefs with no cross-surface retrieval — re-test window named in closure; no mid-pilot §6 edit

### Definitions (frozen)

| Term | Definition |
|---|---|
| **T0** | First successful Mem0 write under the allowlist, visible to a second surface’s search |
| **Qualifying session** | A dated work session that (1) uses Mem0 MCP on ≥1 surface **and** (2) either crosses surfaces same calendar day (Cursor↔CC) **or** retrieves on surface B a pref/pointer written on surface A |
| **Rule-7 contamination** | Mem0 memory text (or agent citation of it) restates a Rule-7 owned value **or a locked strategy parameter**: risk %, pyramid, MC anchor headlines, LOCK hashes, lifecycle multipliers, `ACTIVE_FIRM` / firm-tier constants, authorization state as if authoritative; **plus (v1.1) any Pine input / `core/config/params.toml` value — SL/TP/ATR multipliers, session hours, proximity/trail/BE constants** (the edge-protection posture makes these the most protected bytes in the programme; paraphrase counts — “about a third of a percent” restates 0.34%) |
| **Ledger-skip** | Instrument-touching session that omits the Rule-10 ledger read/append and the session log attributes the skip to Mem0 content |
| **Material handoff benefit** | **Operator-confirmed** case (v1.1: was “operator- or session-logged”; an agent may nominate a candidate in the tally, but only rows the operator marks confirmed count toward §6) where a retrieved pointer/pref avoided re-deriving open-thread location or workflow preference across surfaces — logged in the pilot tally (path below) |

---

## §5 — Forbidden moves

- **Make Mem0 (or any sidecar) a Rule-7 owner** — ruled out by §7; recreates the 2026-06-03 STATE.md drift class inside an opaque store.
- **Replace instrument ledger read+append** — ruled out by ADR 2026-06-11 §3 (memory-only already failed).
- **Replace SESSIONS / Open-next / ADR narrative** — ruled out by §7 owners; Mem0 is not git-auditable provenance.
- **Ingest `docs/ltm/**` or `lab/archive/**` into Mem0** — ruled out by LTM search-exclusion design; fuzzy recall of spent briefs is the failure mode.
- **Cite Mem0 in any ADR/brief §0 as evidence** — Rule 0 requires production/doc owners; Mem0 is never Tier-1.
- **Letting edge-adjacent content reach an external extraction endpoint** (v1.1 — restated from “cloud MCP while content is edge-adjacent”): the exposure boundary is the **extraction LLM + embedder**, not the server host. Self-hosting the Mem0 *server* does not keep content local — the default pipeline sends payloads to an external LLM (OpenAI) for extraction. Ruled out by public-clone / edge-protection posture. Either configure a fully local LLM + embedder, or rely on the explicit-add-only constraint below so only allowlist-shaped payloads ever reach the extractor (and record which in the closure).
- **Auto-ingest of conversation content** (v1.1 — new): no Mem0 auto-add / whole-message ingestion mode on any surface. The contamination counter measures what is **stored**, not what was **sent** — auto-ingest in a Pine-editing Cursor session would ship edge content to the extractor even if the resulting memory is benign. Explicit `add` calls with allowlist-shaped payloads only; this constraint is frozen with the allowlist.
- **Store restated lock numbers “for convenience”** — tempting during handoffs; forbidden; store **paths** only.
- **Widen allowlist mid-pilot to “whatever agents confirm”** — Mem0’s ADD-only agent-fact weight makes this the primary contamination path; freeze allowlist until closure.

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED` | Accept H-XMEM-1 (all accept limbs) | Keep optional MCP sidecar; write admitting note (not an ADR unless doctrine must change); add a one-line Rule-7 role note only if needed (“Mem0 = non-canonical soft scratch; never owner”) |
| `FALSIFIED` | Any reject limb | Tear down MCP; delete/export-wipe pilot memories; capture lesson; leave git memory stack unchanged |
| `AMBIGUOUS-HOLD` | Ambiguous limb | Pause MCP; re-test window = next 14d block with explicit T0′; no allowlist widen |

**Pre-registered before T0.** Amending §6 after memories accumulate is methodology `p`-hacking (Known Trap #12) — close AMBIGUOUS and open a fresh Pre-Q instead.

---

## §7 — Execution plan

Self-executing / operator-gated; no CC handoff required for Phase 0–1. Optional CC handoff only if self-host bootstrap fails.

- **Phase 0 — Install (does not start T0).** Prefer Mem0 self-hosted server (`cd server && make bootstrap` per upstream docs). Wire MCP in Cursor **and** Claude Code with one `user_id`. Confirm search empty. **v1.1:** record the extraction LLM + embedder endpoints in the tally header (local vs external provider — this is the edge boundary, not the server host); disable any auto-add/auto-ingest mode on both surfaces (explicit `add` only, per §5).
- **Phase 1 — Allowlist card (commit or local note before T0).** One page listing allowed memory shapes + denylist examples (risk %, `99.83`, LOCK hashes, Pine/params.toml values, …). Agents load this before first `add`.
- **Phase 2 — Run pilot.** Log each qualifying session in `docs/notes/pilots/q-xmem-1/TALLY.md` (create at T0): date, surfaces, write?/retrieve?, benefit candidate Y/N (one line) + operator-confirmed Y/N, contamination Y/N, ledger-skip Y/N.
- **Phase 3 — Contamination audit.** Interim audit at N=10 if reached before T0+14d; **final audit and verdict at T0+14d — the verdict date, full stop** (v1.1: was “final at max(T0+14d, N=10)”, which implied running past day 14 to reach N=10 after §6 had already returned AMBIGUOUS-HOLD). Method (v1.1): **full export + operator read of every stored memory** — the store is pilot-sized; the denylist-token search is supplemental only, because Mem0’s extraction LLM paraphrases and a token grep alone is Trap M-AHF (stored form ≠ written form). Plus: grep pilot tally + recent SESSIONS for Mem0-as-authority citations.
- **Phase 4 — Verdict.** Apply §6; write closure per §9; update INDEX.

---

## §8 — Verdict pre-registration

See [`docs/briefs/pre-registration/Q-XMEM-1-verdict-preregistration.md`](pre-registration/Q-XMEM-1-verdict-preregistration.md).

Pre-registration lineage (all pre-T0):
- v1.0 freeze: `fd71074` (2026-07-16), pinned by `501f60c` — v1.0 §8 line was left as a placeholder; corrected here
- v1.1 amendment: `1d4a866` (2026-07-16) — supersedes v1.0 as the frozen architecture

Pre-registration date: 2026-07-16

---

## §9 — Closure record format

- **If RESOLVED:** `docs/briefs/closures/Q-XMEM-1-closure-resolved.md`
- **If FALSIFIED:** `docs/briefs/closures/Q-XMEM-1-closure-falsified.md`
- **If AMBIGUOUS-HOLD:** `docs/briefs/closures/Q-XMEM-1-closure-ambiguous.md` with T0′ and re-test window

Closure must include: N qualifying sessions, contamination count, ledger-skip count, benefit count, audit commands run, hosting choice (self-host vs cloud), and whether any Rule-7 role note was added.

---

## §10 — Audit hooks (runnable)

```bash
# Confirm no in-repo mem0 wiring yet (pre-T0) / or inventory after install
rg -n "mem0|OpenMemory|mcp.mem0" --glob "!**/node_modules/**" --glob "!**/.git/**"

# Rule-7 / Rule-10 anchors still resolve
git log -1 --format="%H %ci" -- docs/operational_rules.md
rg -n "per-surface memory is mutually invisible|Durable atomic facts" docs/operational_rules.md

# Ledger doctrine still rejects memory-only
rg -n "Status quo for cross-session state" docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md

# Pilot tally present after T0
# Expect: docs/notes/pilots/q-xmem-1/TALLY.md with dated rows

# Contamination audit (post-pilot; adapt to Mem0 export/CLI)
# PRIMARY (v1.1): full export + operator read of EVERY stored memory —
#   mem0 get-all --user-id <id> > docs/notes/pilots/q-xmem-1/export-final.json
#   (extraction LLM paraphrases; token grep alone is Trap M-AHF)
# SUPPLEMENTAL token sweep:
# mem0 search "risk percent" / "99.83" / "0.70%" / "AUTHORIZED" / "ATR" / "SL" --user-id <id>
# Plus: rg -n "mem0 said|from memory:.*%|MC anchor" docs/SESSIONS.md docs/notes/pilots/q-xmem-1/

# Confirm MEMORY.md silo still structural (CC primary vs worktrees)
# Test-Path repo MEMORY.md → False; primary CC project MEMORY.md may still exist
```

---

## Verification

```bash
python scripts/check_brief.py docs/briefs/Q-XMEM-1-cross-surface-memory-sidecar-pilot.md --type inquire
# Expected: all 6 checks PASS

git log -1 --format="%H %ci %s" -- docs/operational_rules.md
# Expected: 4617007… (or successor that still contains §7/§10)

rg -n "mem0|OpenMemory" --glob "!**/node_modules/**" docs/ briefs/ 2>/dev/null
# Pre-T0 expected: only this brief + pre-reg + INDEX (+ canvas outside repo)

Test-Path MEMORY.md
# Expected: False at repo root
```

---

## Pre-Lock Checklist

- [x] All §0 paths read and anchored
- [x] §3 passes symptom-only rephrase
- [x] §4 falsifiable with binary §6 triggers
- [x] §5 forbidden moves are genuinely tempting
- [x] §6 gates specific (N, counts, windows) — no “when we know more”
- [x] §8 pre-registration **committed** before T0 (v1.0 `fd71074`; v1.1 amendment `1d4a866`)
- [x] §10 audit hooks are runnable commands
- [x] `check_brief.py` PASS (skill-side 6/6; repo-side well-formed 2026-07-16; re-run post-v1.1)
