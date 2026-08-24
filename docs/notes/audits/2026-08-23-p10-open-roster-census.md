# P10 — INDEX Open roster census (2026-08-23)

**Packet:** pain-point P10 ([charter](../../superpowers/plans/2026-08-23-repo-pain-point-packets.md) · [impl](../../superpowers/plans/2026-08-23-p6-p10-residuals-implementation.md))
**Scope:** `docs/briefs/INDEX.md` §Open only. Not CATALOG. Not Dormant.
**Election:** Q-TOM-SPX-1 = formal `DEAD` (operator GO; reserved native-Pine confirmation unpaid since 2026-06 and not reserved). Do not close Q-SIGID-1 or Q-FILLTAX-1.

## Amendment-first / sub-rule 8 attestation (this session)

```
$ rg -n 'Q-TOM-SPX-1|turn-of-month-premium' lab/CATALOG.md
(no matches)

$ rg -n 'Q-TOM-SPX-1|Q-SIGID-1|Q-FILLTAX-1' docs/briefs/INDEX.md
18:| **Q-TOM-SPX-1** — … Layer A **RESOLVED-ABSENT** … formal DEAD close reserved …
19:| **Q-SIGID-1** — … **`OPEN`** …
20:| **Q-FILLTAX-1** — … **`OPEN`** …

$ rg -n 'turn-of-month-premium|Q-TOM-SPX-1' docs/rejected_candidates.md
(no matches)
```

Nearest owners: the Q-TOM-SPX-1 brief itself, `docs/pursuits/c3-q-tom-spx-1.md` (PARK until 2026-11-08 → reserved DEAD), `ops/instruments/SPX500.md` (F5 / Active concept). No existing closure under `docs/briefs/closures/`. No CATALOG row. Census is this note; close is its own closure record.

## Open table (complete as of census)

| Q | Status token on INDEX | Recommended disposition | Election |
|---|---|---|---|
| **Q-TOM-SPX-1** | Layer A `RESOLVED-ABSENT` (2026-06-16); formal DEAD close reserved | Formal DEAD/STOP close (closure + delete Open row) **or** leave reserved with a dated reason | **DEAD** — Pine confirmation not reserved |
| **Q-SIGID-1** | `OPEN` | Leave Open | **Leave** |
| **Q-FILLTAX-1** | `OPEN` | Leave Open | **Leave** |

Three Open rows. Only Q-TOM-SPX-1 is not open.

## Cheap falsifier (parent-side, before the close)

Layer-A already ran 2026-06-16 on the canonical Pepperstone US500 daily feed (n=113 turns): Welch t=0.64, perm p=0.2544, COVID-concentrated, halves sign-reverse → hard-absent. Recorded on [`SPX500.md`](../../../ops/instruments/SPX500.md) F5 / session log. The unpaid limb is the brief-reserved native Pine confirmation, not a missing Layer-A number. This packet does not re-run Dukascopy or widen the window.
