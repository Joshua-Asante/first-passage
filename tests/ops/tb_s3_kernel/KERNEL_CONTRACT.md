# Durable primitive kernel candidate

Stage 2 consumes stage 1 evidence and owns consumer enforcement of E1–E3 and
K1–K3 in PR360 rev6 §2e. **Unaccepted offline candidate.** Ownership and recovery
stay in one state machine. No daemon or account orchestration module is imported
or required to run the primitive suite.

The listener owns order reservations, verified allocation, quarantine, individual
obligations, CANCEL/CLOSE/AMEND/ATTACH, gap recovery, attempts and persisted effects.
The producer owns facts; the production aggregate capacity ledger receives only
verified per-order credit. `completion_actions(now)` is a transaction extension
point: account composition may plan journaled effects before the same final store
write, but no status query may invoke it. Recovery does not require that extension.

| Contract | Independently expected outcome |
|---|---|
| E1 | Duplicate/older, position-only or pre-dispatch evidence cannot settle newer work. |
| E2 | No sibling reserve funds overfill; changed or backdated identity retains quarantine across restart. |
| E3 | Every unresolved request blocks admission until its future exposure is resolved or transferred to another owner. |
| K1 | Completing one owner preserves all others; zero net with gross lots or working remainders is not quiescent. |
| K2 | Unsupported/removing/incomplete brackets are refused; only dispatched component values explain transitions. |
| K3 | Store/dispatch crashes retain required work; unknown sends are not blindly retried; bounded reductions do not execute twice. |

`EXTRACTION_INVENTORY.md` maps every inherited test to a semantic contract and stage.
Historical filenames preserve traceability, not acceptance boundaries. Expected
quantities, owner sets and broker facts remain literal or event-derived; extraction
does not introduce a second copy of the kernel as the test oracle.

Schema 4 is an offline primitive snapshot with explicit required fields. Missing
or incompatible snapshots are refused; no production migration is supplied.

## Unresolved candidate findings

The five findings on published PR365 head `23cf0e1` have candidate repairs in the
preserved round7 source. Passing inherited regressions is not independent acceptance.
Review must still close these compositions before this candidate is accepted:

- Request completion can expose unowned gross offsetting lots whose net is zero;
  request-to-lot ownership must not disappear behind net position equality.
- A covering external request must expand coverage when a later global registry
  introduces another symbol, even if that read omits its completion record.
- Renewed pending state after completion must retain an ID conflict, including
  before coverage of all possible symbols has completed.
- The inherited retained-close gross-lot case restarts before the relevant fresh
  read and therefore does not establish the intended no-op race on its own.

These are acceptance blockers, preserved explicitly rather than hidden by the split.
Production L1 equivalence, L2 qualification and operator gates remain separate.
