# Notice — NeMo Guardrails looked at and refused; standing analog surface rejected

**Notice ID:** N-2026-08-23-nemo-guardrails-reconciliation
**Observed:** 2026-08-23
**Author:** Joshua (commission: download NeMo Guardrails and reconcile with this repo, from a Grok conversation that split LLM / harness / rails) + Cursor Cloud Agent
**Source:** operator prompt (owner GO for a constrained 4th external-mapping instance) + shallow clone of `https://github.com/NVIDIA-NeMo/Guardrails` tag `v0.23.0` @ `dc046e4e1db894893214ffab487c35f451f5baad` + later operator reject of the standing analog surface + ox-alpha consult
**Status:** `OPEN` → routed below (`DROP` for runtime adoption, imported mechanism, **and** the standing pin / inventory / Proposed ADR)
**Lives in:** `docs/notes/notice/N-2026-08-23-nemo-guardrails-reconciliation.md`
**Operator GO (instance 4):** this prompt. Scope frozen as download + map of *existing* rails. No new pipeline stage. Guardrails: [`external_mapping_guardrails.md`](../../methodology/external_mapping_guardrails.md). Audit: [`AUDIT-2026-08-20-external-mapping-move-class`](../audits/programme-audit/2026-08-20-external-mapping-move-class-audit.md).
**Rule 2:** OUTER, $0/K=0, one instance. STRATEGIC 3/3 was already tripped; this row is owner adjudication, not a self-extension.
**Addendum (operator reject):** the Proposed ADR and standing NeMo/guardrails surface (pin, `docs/agent_rails/`, checker, fetch helper) were rejected. Principles may be borrowed as needed. Ox-alpha consult: [`N-2026-08-23-ox-alpha-analog-pin-vs-inspiration.md`](N-2026-08-23-ox-alpha-analog-pin-vs-inspiration.md).

---

## §0 — Source anchor

- **Source:** NVIDIA NeMo Guardrails README “Types of Guardrails” (five stages) at `v0.23.0` @ `dc046e4e1db894893214ffab487c35f451f5baad`; Grok engine/harness/rails model in the operator prompt; live-rail owners remain on each gate (Rule 0, handoff-verify, INQHIORI Pre-Q, verify-source, `c1_rail_listener` / `c1_rail_arm`, `dd_protection`, Hermes NO-GO, `check_brief`, blast-radius, fable-judge).
- **Observed at:** 2026-08-23, this session and the follow-up reject.

---

## §1 — The observation

NeMo’s five programmable stages (input, dialog, retrieval, execution, output) already have First Passage owners. The hard execution tracks are code. Soft dialog/retrieval/output tracks are skills and gates. The analog was real; a standing pin, inventory, drift checker, and light ADR were not required to keep that knowledge.

---

## §2 — Why it stands out (the N signal)

- **Baseline:** prior mapping instances searched *outward* for a borrowable mechanism and DROPped 3/3 ([audit](../audits/programme-audit/2026-08-20-external-mapping-move-class-audit.md)).
- **Delta:** this instance was scoped to download the analog and name the in-repo tracks. Zero candidate mechanisms proposed. Belt work is a consolidation ([`external_mapping_guardrails.md`](../../methodology/external_mapping_guardrails.md)), not a sixth add. The first session overshot into a standing surface; the operator rejected that surface.
- **Frequency:** 4th mapping-shaped session; 1st under explicit owner GO and the “no imported mechanism” freeze; then an operator reject of the pin itself.

---

## §3 — Candidate mechanisms (informal)

- None proposed. Importing Colang as a runtime in front of `c1_rail_listener` was considered and refused (domain-conflation: the listener already is the execution rail; Hermes §4 still kills a third-party server in the perimeter).
- Institutionalizing the analog (pin + inventory + checker + Proposed ADR) was a second, lighter import. Operator rejected it. Borrow principles as needed.
- Could also be noise — NeMo is a conversational-LLM toolkit; First Passage rails are mostly non-LLM fail-closed Python.

---

## §4 — Routing decision

**DROP** for adopting NeMo as a runtime, pip dependency, or new pipeline stage.

**DROP** for keeping a standing NeMo/guardrails surface (version pin, `docs/agent_rails/`, `scripts/check_agent_rails.py`, `scripts/fetch_nemo_guardrails.py`, Proposed ADR `2026-08-23-nemo-guardrails-pin-not-runtime.md`). The operator rejected the ADR as unnecessary.

**Kept:** this notice as the refuse-trail (looked at `v0.23.0` @ `dc046e4`; stages already have owners; borrow principles as needed). Mapping-guardrails consolidation and the Rule-2 GO row stay — they do not depend on the pin.

Reason: the analog was a look, not a surface. Ox-alpha G/K rows and the operator reject bound the teardown; D rows bound keeping this notice.

---

## Addendum — operator rejected the standing analog surface

Dated follow-up, same notice (amend-in-place). The first routing kept a pin + inventory + checker + light ADR. That keep is withdrawn. No successor ADR. Hermes §4 remains the revisit trigger for any third-party runtime in the perimeter; it does not need a NeMo-named addendum.

---

## §10 — Audit hooks

```bash
# Standing analog surface is gone
test ! -e docs/adr/2026-08-23-nemo-guardrails-pin-not-runtime.md
test ! -d docs/agent_rails
test ! -e scripts/check_agent_rails.py
test ! -e scripts/fetch_nemo_guardrails.py

# No runtime dependency
rg -n nemoguardrails --glob '!docs/**' --glob '!tests/**' --glob '!.gitignore'
# Expected: empty

# Fourth instance still carries operator GO; standing surface later rejected
rg -n "Operator GO \(instance 4\)" docs/notes/notice/N-2026-08-23-nemo-guardrails-reconciliation.md
rg -n "operator rejected the standing" docs/notes/notice/N-2026-08-23-nemo-guardrails-reconciliation.md
```

---

## Verification

```bash
$ python scripts/check_brief.py docs/notes/notice/N-2026-08-23-nemo-guardrails-reconciliation.md --type notice
# Expected: RESULT: NOT CHECKED
```
