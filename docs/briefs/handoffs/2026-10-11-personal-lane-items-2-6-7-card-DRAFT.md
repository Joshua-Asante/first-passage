# Personal lane: ADR 2026-10-09 owed items 2, 6, 7 (build card)

**Type:** cc_handoff (build card; packets built by CC solo against this card)

**Date:** 2026-10-11 (UTC).

**Status:** DRAFT. P1–P3 are open PRs (§2); P4 is sequenced (§4).

**Authority:**
- [ADR 2026-10-09](../../adr/2026-10-09-self-funded-tradovate-lane-reopen.md) owed items 2, 6 and 7, dispatched by the Deployment Coordinator ("Portfolio deployment coordination") 2026-10-10.
- This card narrows that dispatch; it adds no authority. §0.5 rulings are Joshua's.

**Coordinator:** the Deployment Coordinator. The merge sequencer owns merges.

```yaml authority
seat: worker
parent: docs/adr/2026-10-09-self-funded-tradovate-lane-reopen.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push]
constraints:
  - no_main_write
  - no_merge
  - packet_write_footprint_only
  - red_first
  - no_dd_protection_edit
  - no_policy_registry_row
  - no_tradeify_binding_change
  - no_worker_file_edit
  - no_private_bytes_in_git
  - no_live_order_arm_or_credentials
  - no_glm_for_trust_auth_or_private_inputs
  - stop_at_coordinator_return
acceptance:
  - tests/core/test_personal_tier.py
  - tests/ops/test_personal_drawdown_halt.py
  - tests/ops/test_instance_binding.py
```

## §0 — Production reads and Phase 0

Read on `origin/main` @ `b5571a9`: the lane ADR; `core/firm_rules.py`; `core/mc/preflight.py`; `core/mc/simulation.py` (`profit_target` must exceed the start); the [concept-not-constant ADR](../../adr/2026-07-13-dd-protection-concept-not-constant.md) §2, §4, §5; `ops/c1_rail/book_policy.py`, `book_halt.py`, `c1_rail_http_server.load_config`, `write_volume_config.py`; `deploy/c1_rail/`; the `claude/protection-source-health` diff.

| Check | Finding |
|---|---|
| Qualification code (`qualification/trust_domain.py`) | Not touched. `qualification/runner.py` calls `firm_kwargs('Tradeify_Select_100K')`; P1 keeps that path byte-identical. |
| Frozen constants / locked files | None touched. `DD_TRIGGER`/`DD_SCALE`, `_validate_protection_rule`, `POLICY_REGISTRY`, `book_policy.py` unchanged; `verify_lock_anchors.py` reads only `firm_rules._BASE_RISK`. |
| Protection-health worker files | Not touched by P1–P3. Wiring the halt into entry gating and flatten needs `c1_rail_listener.py` / `book_account_owner.py` → P4, after that worker. |
| Firm-expansion coverage | The lane ADR names the tier (item 2); no separate ADR. Pre-flight in P1; re-MC gated (§4). |
| `E_0` | `first-passage-archive`, branch `archive/preserve-exposure-2026-10-09` @ `950ee0f`. Read in place only; not copied into the private overlay by this card. |

## §0.5 — Rulings requested (recommended defaults)

1. **Halt outside `POLICY_REGISTRY`.** The 15% halt is an operator-ruled barrier keyed (portfolio, tier) in its own module. A scale-down `dd_protection` instance for this lane, if any, takes the concept ADR §4 chain after item 1.
2. **Peak on resumption.** The running peak carries through a resume; re-basing it needs the GO to say so (`rebase_peak: true`).
3. **`starting_balance` indirection.** The public row carries `starting_balance: None` and `starting_balance_source: "private"`; the value loads from gitignored `core/firm_rules.private.json`, fail-closed. Writing that file (`{"Personal_Tradovate": {"starting_balance": E_0}}`) in the primary checkout is an operator act.

## §1 — Context

The lane ADR owes seven items before the first personal-account order. Items 2, 6 and 7 do not depend on the portfolio. `simulate_path` is pass/bust shaped, so the growth statistic is Q-SFGROWTH-1's harness.

## §2 — Packets

| # | Item | Footprint | Red-first tests | PR |
|---|---|---|---|---|
| P1 | 2 | `core/firm_rules.py`, `core/mc/preflight.py`, `.gitignore`, `tests/core/fixtures/firm_rules_resolved.json`, `tests/core/test_personal_tier.py` | no public balance literal; loader refuses missing/invalid; `firm_kwargs` raises `EngineUnsupported` (no profit target); prop tiers unchanged | #775 |
| P2 | 7 | `ops/c1_rail/personal_drawdown_halt.py`, `tests/ops/test_personal_drawdown_halt.py` | intraday trough latches; gap through threshold; threshold edge; restart while halted; flatten failure keeps flatten owed; missing/corrupt/foreign state blocks entries; resume needs GO after confirmed flat | #776 (on #775) |
| P3 | 6 | `deploy/c1_rail_personal/instance_binding.json`, `ops/c1_rail/instance_binding.py`, `tests/ops/test_instance_binding.py` | every instance key overridden; no credential shared with Tradeify; distinct app and volume; disarmed; destination unbound | #777 (on #775) |
| P4 | 6, 7 | `c1_rail_arm.py`, listener entry gate, flatten executor | arm refuses a personal instance without valid halt state; listener blocks entries when halted; halt persist failure routes into `book_halt` | not built |

## §4 — Hypothesis, order and gates

H: P1–P3 add the tier, halt and binding with every Tradeify path unchanged; falsified if any existing test or `fp.py check` goes red. Order: #775, then #776 and #777 (retarget to `main`), then P4 after the protection-health worker. Gated: the re-MC on #752 / item 1; any route, feed or arm on items 3–4; live use on all seven items, M1 and a per-session GO.

## §5 — Forbidden moves

- Editing `dd_protection` constants, `POLICY_REGISTRY`, `book_policy.py` or the Tradeify binding.
- Editing the protection-health worker's files before that worker lands.
- Committing `E_0`, balances, P&L or credentials.
- Any order, arm, Tradovate or CME call.

## §6 — Return taxonomy

Each packet returns its PR, red and green `record.json` and `fp.py check` record to the coordinator with one status: `DONE` (acceptance tests and check green), `DONE_WITH_CONCERNS` (green with a named residual), `NEEDS_CONTEXT` (a §0.5 ruling or owner fact is missing), `BLOCKED` (a §5 move or a worker file is required). The card is `RESOLVED` when P1–P3 are `DONE` and `FALSIFIED` if any existing test goes red with them. Two failed corrections of one issue: stop.

## §10 — Audit hooks

```bash
c=docs/briefs/handoffs/2026-10-11-personal-lane-items-2-6-7-card-DRAFT.md
python -I scripts/fp.py python scripts/check_brief.py --type handoff "$c"
python -I scripts/fp.py python scripts/check_handoff_authority.py "$c"
python -I scripts/fp.py python -m pytest tests/core/test_personal_tier.py tests/ops/test_personal_drawdown_halt.py tests/ops/test_instance_binding.py -q
git diff origin/main -- core/dd_protection.py core/dd_geometry.py ops/c1_rail/book_policy.py   # expect no output
```
