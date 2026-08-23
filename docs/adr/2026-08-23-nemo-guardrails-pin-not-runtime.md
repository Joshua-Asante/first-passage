# ADR 2026-08-23 — NeMo Guardrails is pinned as a rails analog, not adopted as a runtime

**Status:** `Proposed` — records the pin-and-map; operator flip to `Accepted` is a separate GO
**Decision date:** 2026-08-23
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Tier:** light
**Layer:** governance citation. **$0 / K=0.**
**Loop-of-Record:** OUTER — constrained 4th instance of the external-mapping move-class under owner GO (this prompt). Not a self-granted STRATEGIC extension.

Decision: Pin NVIDIA NeMo Guardrails `v0.23.0` @ `dc046e4e1db894893214ffab487c35f451f5baad` as a study analog of the rails layer. Do not add `nemoguardrails` as a pip, server, or process dependency. Existing deterministic gates remain the live rails; `docs/agent_rails/rails.yml` is a labeled mirror checked by `scripts/check_agent_rails.py`. Colang under `docs/agent_rails/colang/` is documentation-only.

Grounds: Grok engine/harness/rails model. NeMo README five-stage list (input/dialog/retrieval/execution/output) at the pin. Hermes NO-GO three-limb falsifier ([`2026-07-27-hermes-agent-adoption-nogo.md`](2026-07-27-hermes-agent-adoption-nogo.md)) still kills a third-party rails server inside the perimeter. Mapping audit ([`2026-08-20-external-mapping-move-class-audit.md`](../notes/audits/programme-audit/2026-08-20-external-mapping-move-class-audit.md)) §5.1 required owner GO + belt consolidation before a 4th instance; this instance proposes no imported mechanism.

Reads: NeMo clone `v0.23.0` @ `dc046e4e1db894893214ffab487c35f451f5baad` README L114–130 · `ops/c1_rail/c1_rail_arm.py` @ `027a729` (`require_resolved=True`) · `ops/c1_rail/c1_rail_listener.py` @ `027a729` (`dry_run` default True) · `CLAUDE.md` @ `930bb00` (no agent-placed trades) · Hermes ADR @ `027a729` · mapping audit @ on-disk 2026-08-23

Gate: RESOLVED if `python scripts/check_agent_rails.py` exits 0 and `rg -n nemoguardrails --glob '!docs/**' --glob '!tests/**'` is empty. FALSIFIED if a later commit installs the package or starts a NeMo server without a superseding ADR that fires Hermes §4.

Boundary: Do not invent a Colang runtime in front of the c1 listener. Do not add a pre-commit gate (that would be limb-4 doctrine). Do not propose new pipeline stages under NeMo vocabulary. Do not treat this Proposed record as Accepted.
