# Agent rails — NeMo pin + First Passage map

**Owner:** [`2026-08-23-nemo-guardrails-pin-not-runtime.md`](../adr/2026-08-23-nemo-guardrails-pin-not-runtime.md) (`Proposed`).
**Inventory (machine):** [`rails.yml`](rails.yml) — checked by [`scripts/check_agent_rails.py`](../../scripts/check_agent_rails.py).
**Study clone:** `python scripts/fetch_nemo_guardrails.py` → gitignored `third_party/nemo-guardrails/` at the pin in `rails.yml`.

This file is a **labeled mirror**. Live authority stays with each `owner` path in `rails.yml`. Do not quote this README as the safety invariant.

## Engine / harness / rails

The Grok conversation's three-layer model maps onto surfaces this repo already has:

| Layer | Analogy | First Passage surface |
|---|---|---|
| **LLM** | engine | Session model (Cursor / Claude). Not in-tree. |
| **Harness** | vehicle | Skills, Cursor rules, `ops/c1_rail/`, `ops/c1_signal_daemon/` — tools, memory, orchestration. |
| **Rails** | tracks | Deterministic input / dialog / retrieval / execution / output checks. Hard rails fail-close in code; soft rails are paved-road prose (skills, notices). |

NeMo Guardrails ([NVIDIA-NeMo/Guardrails](https://github.com/NVIDIA-NeMo/Guardrails) `v0.23.0` @ `dc046e4e1db894893214ffab487c35f451f5baad`, Apache-2.0) is the closest open-source *vocabulary* for the rails layer: five programmable stages (input, dialog, retrieval, execution, output) plus Colang as policy-as-code. Inspected from a shallow clone of that tag; **not** added as a pip or process dependency.

Stronger rails here already enable autonomy: `dry_run` defaults true, M1 must validate `RESOLVED` before arm, no agent-placed trades, `dd_protection` refuses a broken rule at import. Those are tracks, not prompts.

## What this is not

- Not a new pipeline stage and not a Colang runtime in front of the c1 listener.
- Not a replacement for Hermes-NO-GO ([`2026-07-27-hermes-agent-adoption-nogo.md`](../adr/2026-07-27-hermes-agent-adoption-nogo.md)): a third-party rails *server* inside the perimeter fails the same three falsifier limbs.
- Not a fourth unconstrained external-framework mapping. Instance 4 was operator-GO'd to download + pin + map *existing* rails; mapping guardrails live in [`external_mapping_guardrails.md`](../methodology/external_mapping_guardrails.md).

## Colang

[`colang/execution.co`](colang/execution.co) restates the hard execution rails in Colang 1.0 shape so the NeMo analogy is readable. The file is **not executed**. The listener and arming interlock remain the live tracks.
