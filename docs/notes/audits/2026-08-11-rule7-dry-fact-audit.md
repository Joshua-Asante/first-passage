# Rule-7 DRY fact audit — 2026-08-11 (Option A)

**Status:** `DRY-AUDIT: REPAIRED` (slices 1–3); Option A closed for planned fact classes  
**Scope:** Rule-7 *fact* DRY only — load-bearing facts restated outside their owner. Not a code-duplication pass.  
**Method:** Rule 7 owner table + blast-radius checklist; token harvest from owners; grep hot surfaces; triage.  
**Slices:** (1) posture / risk% / `dd_protection` / lifecycle · (2) F10–F11 + stale-rail · (3) MC anchors / baselines / F14  
**Yardstick:** [`docs/operational_rules.md`](../../operational_rules.md) §7 · [blast-radius owner surfaces](../../../.claude/skills/blast-radius/references/owner-surfaces.md) · [root-doc charter](../../adr/2026-07-16-root-doc-charter-dedup.md).

Canonical owners (do not restate values here):

| Fact class | Owner |
|---|---|
| Live posture | owning ADRs; pointer block in [`CLAUDE.md`](../../../CLAUDE.md) §Live-execution posture |
| Risk % / versions (human record) | gated `CLAUDE.md` Strategy Reference · Pine for parameters |
| `dd_protection` / allocations | [`core/dd_protection.py`](../../../core/dd_protection.py) · [`core/firm_rules.py`](../../../core/firm_rules.py) |
| Lifecycle tiers / multipliers | [`docs/methodology/strategy_lifecycle.md`](../../methodology/strategy_lifecycle.md) |
| MC anchors | [`docs/mc_anchor_history.md`](../../mc_anchor_history.md) + synthetic engine tests · gated CLAUDE headline (recall denylist) |

---

## Phase 0 — mechanical baseline

| Gate | Exit |
|---|---|
| `check_root_doc_liveness.py` | 0 |
| `check_path_liveness.py` | 0 |
| `check_status_consistency.py` | 0 (1 advisory: uncatalogued MNQ cheap-falsifier cite) |
| `check_skills_no_constants.py` | 0 |
| `check_adr_graph.py` | 0 |

**Gap:** `check_skills_no_constants` guards only four methodology skills — operational skills exempt by design.

Prior related sweeps: 2026-08-05 claim-alignment · 2026-07-29 live-docs stale-claims · 2026-07-16 root-doc charter.

---

## Findings

| ID | path | token / claim | class | sev | action |
|---|---|---|---|---|---|
| F1 | `strategy_lifecycle.md` rail caveat | rail unbuilt / TV-typed | silent stale | **S1** | **REPAIRED** (s1) |
| F2–F4 | `prop-firm-challenge` allocations / DD / lifecycle state | risk% · `DD_*` · AUTHORIZED@1.00× | silent | **S2** | **REPAIRED** (s1) |
| F5 | `PIPELINES.md` | `1.5%/0.40×` | silent | **S2** | **REPAIRED** (s1) |
| F6 | `objective_composition_map.md` | Current live WATCH-1 + dd literals | silent/stale | **S2** | **REPAIRED** (s1) |
| F7–F9 | strategy_reference / c1-rail / instrument ledgers | labeled mirrors | n/a | left |
| F10 | `inqhiori-canon.md` §11 | dd_protection + version snapshot | silent | **S2** | **REPAIRED** (s2) |
| F11 | `prop-firm-challenge` durable block | §4 bust% / caps / WATCH cells | silent narrative | **S2** | **REPAIRED** (s2) |
| F12 | rail_build notes / idle specs | `+$127.40` / DISPROVEN | historical | left |
| F13 | `CLAUDE.md` gated surfaces | risk% / DD / MC headline | **owner** | left — recall guard depends on MC phrasing |
| F14 | `STATE.md` queue row 0 | long open-item prose | W5 accretion | **S3** | **REPAIRED** (s3) — pointer diet; owners hold detail |
| F15 | lifecycle Call-1 handoff | “rail is unbuilt” | historical misleading | **S2** | **REPAIRED** (s2) — reader-intercept |
| F16 | `prop-firm-challenge` Locked anchor | full `99.83/0.17/4.37` restatement | silent | **S2** | **REPAIRED** (s3) → mc_anchor_history + CLAUDE |
| F17 | `strategy_lifecycle.md` | inline `(99.83/0.17/4.37)` | silent | **S2** | **REPAIRED** (s3) |
| F18 | `regime_robustness_gate.md` | §refs + “does not change” risk%/dd/MC | silent | **S2** | **REPAIRED** (s3) |
| F19 | `trade-csv-reconcile/references/baselines.md` | allocation table + DD + MC pin | silent (file owns PF/WR/Net/DD only) | **S2** | **REPAIRED** (s3) — mirror banner + owner links |
| F20 | `trade-csv-reconcile/SKILL.md` | “Use locked allocations from baselines.md (0.34%/…)” | silent | **S2** | **REPAIRED** (s3) → CLAUDE / firm_rules |

Firm-rules snapshot table in `prop-firm-challenge` remains a **labeled mirror** (“if stale, trust the file”) — left.

Frozen pre-registration / closure bodies that cite H1 `4.37%` regime cells are **historical measurement citations** to RESULTS owners — not repaired (would require claim-alignment-scale banners).

---

## Severity summary (cumulative)

| Severity | Raised | Repaired | Deferred |
|---|---|---|---|
| S1 | 1 | 1 | 0 |
| S2 | 14 | 14 | 0 |
| S3 (F14) | 1 | 1 | 0 |
| n/a / historical / owner | 5+ | — | — |

---

## Out of scope (standing)

- Code-level DRY — **Option B**.
- Expanding `check_skills_no_constants` to operational skills — needs ADR.
- Full brief/ADR corpus numeric citations already covered by claim-alignment for *stale claims*.
- Rewording CLAUDE MC literals (breaks `ops/recall/guard.py`).

**Option A planned fact classes: closed.**
