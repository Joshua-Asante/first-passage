# Broker and evidence producer candidate

Stage 1 of the PR365 extraction, from `23cf0e1` plus preserved round7 work.
Governing contract: PR360 rev6, §2e E1–E3. **Unaccepted offline candidate.**

This stage owns the producer halves of E1–E3: coherent captured facts, immutable
execution history, terminal order facts, gross lots, global order locations and
request fences in an external causal domain. It does not accept listener credit,
quarantine or request-owner discharge; those belong to stage2.

| Event sequence | Required externally observed fact |
|---|---|
| Acquire, fill, acquire, deliver old read | Old capture remains unchanged; execution lies between acquisitions. |
| Deferred request, read another symbol, execute | Global pending request becomes retained completion history; location is visible globally. |
| Partial fill, edit order, fill again | Earlier immutable execution remains unchanged; different side has a different lot. |
| Native partial/final close | Position and linked protection reduce by the same bounded amount. |
| Reject a request | Terminal outcome exists without fabricated fill or working order. |

Producer tests import no kernel or daemon and assert literal broker facts. This is
characterization of the offline protocol, not live L-1/L-2 qualification or an
exhaustive proof. The current production telemetry cannot produce the complete
history/fence contract. Unique request IDs are a caller precondition; retained
completion records are history, not renewed pending requests. Consumer rejection
of malformed, missing, contradictory or reordered facts is stage2's responsibility.
