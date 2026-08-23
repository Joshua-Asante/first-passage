# Notice — NeMo Guardrails downloaded and mapped onto existing First Passage rails; not adopted as a runtime

**Notice ID:** N-2026-08-23-nemo-guardrails-reconciliation
**Observed:** 2026-08-23
**Author:** Joshua (commission: download NeMo Guardrails and reconcile with this repo, from a Grok conversation that split LLM / harness / rails) + Cursor Cloud Agent
**Source:** operator prompt this session (owner GO for a constrained 4th external-mapping instance) + shallow clone of `https://github.com/NVIDIA-NeMo/Guardrails` tag `v0.23.0` @ `dc046e4e1db894893214ffab487c35f451f5baad` + Rule-0 reads of the live execution and mapping-audit surfaces
**Status:** `OPEN` → routed below (`DROP` for runtime adoption / imported mechanism; inventory kept)
**Lives in:** `docs/notes/notice/N-2026-08-23-nemo-guardrails-reconciliation.md`
**Operator GO (instance 4):** this prompt. Scope frozen as download + pin + map of *existing* rails. No new pipeline stage. Guardrails: [`external_mapping_guardrails.md`](../../methodology/external_mapping_guardrails.md). Audit: [`AUDIT-2026-08-20-external-mapping-move-class`](../audits/programme-audit/2026-08-20-external-mapping-move-class-audit.md).
**Rule 2:** OUTER, $0/K=0, one instance. STRATEGIC 3/3 was already tripped; this row is owner adjudication, not a self-extension.

---

## §0 — Source anchor

- **Source:** NVIDIA NeMo Guardrails README “Types of Guardrails” (five stages) at `v0.23.0` @ `dc046e4e1db894893214ffab487c35f451f5baad`; Grok engine/harness/rails model in the operator prompt; production anchors listed in [`rails.yml`](../../agent_rails/rails.yml).
- **Observed at:** 2026-08-23, this session.

---

## §1 — The observation

NeMo’s five programmable stages (input, dialog, retrieval, execution, output) already have First Passage owners. The hard execution tracks are code: `dry_run` defaults true, M1 arming calls `validate(..., require_resolved=True)`, no agent-placed trades, `dd_protection` validates at import. Soft dialog/retrieval/output tracks are skills and gates. The missing piece was an index, not a library.

---

## §2 — Why it stands out (the N signal)

- **Baseline:** prior mapping instances searched *outward* for a borrowable mechanism and DROPped 3/3 ([audit](../audits/programme-audit/2026-08-20-external-mapping-move-class-audit.md)).
- **Delta:** this instance was scoped to download the analog and name the in-repo tracks. Zero candidate mechanisms proposed. Belt work is a consolidation ([`external_mapping_guardrails.md`](../../methodology/external_mapping_guardrails.md)), not a sixth add.
- **Frequency:** 4th mapping-shaped session; 1st under explicit owner GO and the “no imported mechanism” freeze.

---

## §3 — Candidate mechanisms (informal)

- None proposed. Importing Colang as a runtime in front of `c1_rail_listener` was considered and refused (domain-conflation: the listener already is the execution rail; Hermes §4 still kills a third-party server in the perimeter).
- Could also be noise — NeMo is a conversational-LLM toolkit; First Passage rails are mostly non-LLM fail-closed Python. The vocabulary still indexes the existing tracks.

---

## §4 — Routing decision

**DROP** for adopting NeMo as a runtime, pip dependency, or new pipeline stage.

**Kept:** pin + [`rails.yml`](../../agent_rails/rails.yml) + `scripts/check_agent_rails.py` + the fetch helper. Light ADR [`2026-08-23-nemo-guardrails-pin-not-runtime.md`](../../adr/2026-08-23-nemo-guardrails-pin-not-runtime.md) (`Proposed`).

Reason: the analog is real; the import is not.

---

## §10 — Audit hooks

```bash
# Pin is the inspected SHA
python -c "import yaml; print(yaml.safe_load(open('docs/agent_rails/rails.yml'))['nemo_pin']['commit'])"
# Expected: dc046e4e1db894893214ffab487c35f451f5baad

# Inventory still matches production
python scripts/check_agent_rails.py
# Expected: agent-rails: CLEAN

# No runtime dependency
rg -n nemoguardrails --glob '!docs/**' --glob '!tests/**' --glob '!.gitignore'
# Expected: empty (or only the fetch script's clone URL / comments)

# Fourth instance carries operator GO
rg -n "Operator GO \(instance 4\)" docs/notes/notice/N-2026-08-23-nemo-guardrails-reconciliation.md
```

---

## Verification

```bash
$ python scripts/check_brief.py docs/notes/notice/N-2026-08-23-nemo-guardrails-reconciliation.md --type notice
# Expected: RESULT: NOT CHECKED
```
