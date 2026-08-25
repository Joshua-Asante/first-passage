# `docs/pursuits/` — GRAND-tier pursuit records

One file per ratified inventory row (GSUB-1 / GSUB-2). There is no
derived INDEX — the files *are* the register. Filename prefix is the class:

| Prefix | Class |
|---|---|
| `a-` | Program / pipeline KEEP |
| `b-` | Transfer / reconstruction lanes |
| `c-` | Named-Q pursuits |
| `d-` | Meta-belt (skills, plugins, subscriptions, accounts) |
| `e-` | Aim-scale / terminal |

| Also here | Job |
|---|---|
| [`SUBSCRIPTION_LEDGER.md`](SUBSCRIPTION_LEDGER.md) | CFO subscription ledger |
| [`e1-first-passage-program.md`](e1-first-passage-program.md) | Aim-scale KEEP row |

Checker: `python scripts/check_pursuit_records.py` (WARN-tier) — run manually; **no longer wired into
`scripts/gates.yml`** as of 2026-08-24 (Rule 16 R5 — the check always exits 0 as invoked, so its
former `gates.yml` entry could never fail regardless of tier; see
[`retirement ADR`](../adr/2026-08-24-validation-battery-k-tiering-and-gate-retirement.md)).
Owner ADR: [`../adr/2026-08-09-grand-tier-quintessentials-binding.md`](../adr/2026-08-09-grand-tier-quintessentials-binding.md).
