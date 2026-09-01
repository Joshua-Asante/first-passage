# Disposition — B3 multiplier-spine forward-relevance flag

> ⚠ **Superseded 2026-07-24:** this disposition's `KEEP-dormant` verdict (do not
> delete `calc_multiplier`) was overtaken by challenge-era substrate Phase 2, which
> **retired** the continuous-lot multiplier spine (`ops/accounts.py` `calc_multiplier`
> / `ops/cli.py lots`) outright — see
> [`docs/adr/2026-07-22-challenge-era-substrate-retirement.md`](../../adr/2026-07-22-challenge-era-substrate-retirement.md)
> §2-D. Body left as written (historical record of the KEEP-dormant reasoning); do not
> cite this disposition as current status.

**Status:** **CLOSED — DORMANT-RETAIN** (forward-relevance = NONE for either surviving scale path; do not delete, do not extend). Discharges the last open 08-08 Class-B item.
**Date:** 2026-07-14
**Owned by:** [`docs/adr/2026-07-11-ops-cfd-estate-retirement.md`](../../adr/2026-07-11-ops-cfd-estate-retirement.md) §4 Trigger-B · 08-08 pre-triage [`2026-07-12-08-08-packet-pretriage.md`](2026-07-12-08-08-packet-pretriage.md) B3
**Related:** [`ops/accounts.py`](../../ops/accounts.py) `calc_multiplier` · [`ops/instruments/6J.md`](../../ops/instruments/6J.md) J5 · R6 ADR §4 (firm-config retention)

---

## §0 — Reads (2026-07-14)

- [`ops/accounts.py`](../../ops/accounts.py):166 — `calc_multiplier(balance, phase, strategy)` = `floor((balance·tier_risk) / (200_000·baseline_risk) · 100)/100`; consumed by `get_multipliers` (4 legs) + `ops/cli.py lots`.
- [`ops/instruments/6J.md`](../../ops/instruments/6J.md) J5 (venue-throttle finding) + ACTIVE/OPEN (M6J not offered at any FRIENDLY firm, 2026-07-13).
- `CLAUDE.md` §CLI Usage / §Multiplier System — the account/multiplier commands are **dormant-historical (2026-07-11)**; zero prop accounts exist.
- Retention basis: R6 ADR §4 (firm configs + multiplier tooling retained for provenance + a possible future firm re-open, not deleted).

## §1 — The question (B3)

Does the account-multiplier layer (`accounts.py calc_multiplier` / `cli.py lots`, sized for a $200K challenge baseline) still matter **forward**, given (i) M6J native micro-contract sizing and (ii) the J5 effective-risk finding (venue structurally throttles Aegis to ≈0.5–1.0% per signal)?

## §2 — What the multiplier-spine assumes

The spine is a **continuous** scale factor applied to Pine's $200K-baseline lot output. It is well-posed **only** when three conditions all hold: a **continuous-lot venue** (fractional lots, CFD/spot — DXTrade/MT5), **multiple accounts** at varying balances, all running the **same locked Pine strategies**. That is exactly — and only — the dormant-historical FXIFY-era multi-firm CFD operation the tooling was built for.

## §3 — Neither surviving scale path meets those conditions

**(a) Self-funded Aegis→M6J (active lane).** Sizing is **integer micro contracts**, ATR-throttled, and **cap-bound** — not a continuous multiple of a $200K-baseline lot. J5: at the 0.07¥ ATR floor, risk/contract ≈ $45–90; locked 1.5% on $100K = $1,500 → ~17–33 contracts, but the 12-cap binds → **effective ≈0.5–1.0%/signal**, cap-bound on **76%** of trades (J2). The size is set in the strategy/Pine layer (ATR risk-per-contract → contracts → cap → integer), **not** by `calc_multiplier`. And **no FRIENDLY firm offers M6J** (6J.md, 2026-07-13) → a **single** self-funded account, so the multi-account premise the spine exists to serve is absent too. → **multiplier-spine N/A.**

**(b) Greenfield prop-portfolio program (4 friendly firms).** Builds **new** prop-envelope candidates via the Gen-2 pipeline (not the locked book); sizing is owned by the **survivor-scoring harness + MC engine + per-firm tiers** at the frozen $100K common band — again **integer micro-contract**, and it does not route through `cli.py lots` or the $200K baseline. → **multiplier-spine N/A.**

## §4 — Disposition

**The multiplier-spine is NOT forward-relevant to either surviving scale path.** Both are integer-micro-contract venues; the continuous "$200K-baseline lot × per-account multiplier" abstraction has no consumer there, and the multi-account premise is absent (M6J = one self-funded account; the prop program scores candidates, it does not run the locked book across many multiplier-scaled accounts).

- **KEEP (dormant-retain), do NOT delete** — consistent with R6 ADR §4 (retain the dormant multiplier/firm tooling for provenance + a possible CFD/multi-account firm re-open). Deletion buys nothing and costs provenance.
- **Do NOT wire / extend** `calc_multiplier` into the M6J or prop-portfolio sizing paths — they have their own native (integer-contract, ATR/tier) sizing. Bolting a $200K-baseline continuous multiplier onto a micro-contract venue would be a category error.
- **Re-arm condition (binary):** the spine regains forward relevance **iff** a continuous-lot, multi-account, same-locked-Pine venue re-enters the operation (a CFD/spot firm re-open under R6 §4). Futures-micro venues never re-arm it.

**This closes B3.** No code, allocation, `dd_protection`, `ACTIVE_FIRM`, or Pine touched; `calc_multiplier` is unchanged (dormant, not edited).

## §5 — Forbidden moves

- Deleting `calc_multiplier` / the `lots` command "since it has no live consumer" — over-retirement; R6 §4 retains it, and this disposition is KEEP-dormant, not remove.
- Extending the multiplier abstraction to M6J/prop sizing to "make it useful" — that manufactures a use the venues don't have (integer micro-contract sizing); it would be new dead code, not a fix.

## §10 — Audit hooks (runnable)

```bash
# The spine is unchanged by this disposition (docs-only close)
git -C . diff --stat -- ops/accounts.py | grep . && echo "UNEXPECTED: accounts.py changed" || echo "accounts.py untouched — good"

# Forward-consumer check: no surviving-path module imports calc_multiplier / get_multipliers
grep -rn "calc_multiplier\|get_multipliers" lab/discovery/ core/mc/ core/lifecycle.py 2>/dev/null \
  && echo "INVESTIGATE — a forward path references the spine" || echo "no forward consumer — disposition holds"

# STATE + pre-triage B3 should be marked CLOSED on merge (deferred to avoid a cross-branch STATE conflict with b6e604a)
grep -n "Multiplier-spine forward-relevance" STATE.md
grep -n "B3" docs/briefs/programs/2026-07-12-08-08-packet-pretriage.md
```

**On merge:** mark the STATE forward-board "Multiplier-spine forward-relevance flag — 2026-08-08" line **CLOSED (DORMANT-RETAIN, 2026-07-14)** and the pre-triage B3 row discharged. (Left un-edited here to avoid colliding with the operator's concurrent STATE edit on `b6e604a`.)
