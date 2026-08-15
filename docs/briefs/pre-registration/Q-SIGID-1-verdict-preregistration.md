# Q-SIGID-1 — verdict pre-registration

**Brief:** [`Q-SIGID-1-intra-bar-signal-identity.md`](../Q-SIGID-1-intra-bar-signal-identity.md)
**Frozen:** 2026-07-28 (before Fri 07-31 §2b live observation)
**Note:** Offline cheap falsifier + 1m phantom proxy already measured in
[`lab/analysis/c1/c1_signal_identity_2026-07-28/RESULTS.md`](../../../lab/analysis/c1/c1_signal_identity_2026-07-28/RESULTS.md)
— that measurement **licenses** the brief (falsifier-before-brief). This file freezes the
**Friday-dependent** closure gate only; it does not authorize re-cutting the offline thresholds
after Friday's result is known.

## Offline band already on file (do not amend post-hoc)

| Leg | Phantoms | Confirmed-close signals | Ratio |
|---|---:|---:|---:|
| MNQ | 15 | 22 | **0.68** |
| MYM | 21 | 30 | **0.70** |

Threshold cited in §6: **0.5** phantom/confirmed-signal ratio.

## §6 gate (frozen)

| Verdict | Trigger |
|---|---|
| `RESOLVED` (gap real) | Fri §2b = DIFFERENT, **or** offline ratio ≥ 0.5 on either leg after a non-VOID Fri session |
| `FALSIFIED` | Fri §2b = EQUAL **and** a **new** offline re-run revises **both** legs below 0.5 |
| `AMBIGUOUS-HOLD` | Fri §2b = VOID or no MYM entry |

Fri §2b vocabulary: EQUAL / DIFFERENT / VOID per desk card fill-in block.

## Forbidden post-freeze moves

- Lowering the 0.5 ratio after seeing Friday's result.
- Declaring FALSIFIED from Fri EQUAL alone while offline ratios stay ≥ 0.5.
- Landing Pine without a separate operator GO after RESOLVED.

---

## Addendum 2026-07-29 — offline measurement source (append-only; 0.5 untouched)

Operator lock: **FULL** panel (2019-05-06 → exclusive end **2026-07-30** UTC) **supersedes** the Phase 0 Apr–Jul band as the §6 offline limb. Phase 0 ratios above remain historical. H1/H2 diagnostic only. This addendum is the pre-reg’s “new offline re-run” for the FALSIFIED limb; **threshold stays 0.5**. Fri §2b still required to close Q-SIGID-1.

| Partition | MNQ phantoms/confirmed | MYM phantoms/confirmed | Role |
|---|---:|---:|---|
| **FULL** | 336/439 = **0.765** | 319/462 = **0.690** | Sole §6 offline measurement |
| H1 | 130/202 = 0.644 | 112/163 = 0.687 | Diagnostic |
| H2 | 206/237 = 0.869 | 207/299 = 0.692 | Diagnostic |
| P0REP | 15/22 (exact) | 21/30 (exact) | Phase 0 replication PASS |

Both FULL legs ≥ 0.5 → offline still supports `RESOLVED` after non-VOID Fri. FALSIFIED remains reachable only if a *further* re-run later revises both below 0.5 **and** Fri = EQUAL. Canonical tables: [`RESULTS.md`](../../../lab/analysis/c1/c1_signal_identity_2026-07-28/RESULTS.md) §FULL · [`results.json`](../../../lab/analysis/c1/c1_signal_identity_2026-07-28/results.json).
