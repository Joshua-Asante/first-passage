"""Consumer checks for the producer's complete accounting/history contract.

These are conservation and identity checks, not a second broker implementation.
They never derive authority from a broker ref alone.
"""
from collections import defaultdict


def allocation_error(ev, previous):
    """Malformed external proof must refuse safely, never interrupt durable publication."""
    try:
        return _allocation_error(ev, previous)
    except (TypeError, ValueError, KeyError, AttributeError):
        return "malformed allocation proof"


def _allocation_error(ev, previous):
    """Return an invalid-proof reason; immutable identity conflicts require attended action."""
    if ev.order_symbols is None:
        return "missing global order registry"
    local = {ref for ref, sym in ev.order_symbols.items() if sym == ev.sym}
    working = {w["ref"]: w for w in ev.working}
    if (set(ev.order_facts) != local or set(ev.order_status) != local
            or len(working) != len(ev.working)):
        return "incomplete or duplicate local order facts"
    expected_working = set()
    for ref, facts in ev.order_facts.items():
        status = ev.order_status[ref]
        if (facts.get("ref") != ref or facts.get("sym") != ev.sym
                or status not in ("working", "partial", "filled", "cancelled", "rejected")
                or facts.get("filled_qty") != ev.fills.get(ref, 0)):
            return "contradictory order identity/status/fill facts"
        if status in ("working", "partial"):
            expected_working.add(ref)
            if working.get(ref) != facts:
                return "working order absent or contradictory in full W"
    if set(working) != expected_working or not set(ev.fills) <= local:
        return "working/terminal order membership mismatch"
    entries = {e.execution_id: e for e in ev.executions}
    reductions = {r.execution_id: r for r in ev.reductions}
    if len(entries) != len(ev.executions) or len(reductions) != len(ev.reductions):
        return "identity conflict: duplicate execution ID"
    if set(entries) & set(reductions):
        return "identity conflict: reused execution ID"
    if previous:
        for old, new in ((previous.executions, entries), (previous.reductions, reductions)):
            for item in old:
                current = new.get(item.execution_id)
                if current is None:
                    return "incomplete retained history"
                if current != item:
                    return "identity conflict: rewritten history"
            known = {item.execution_id for item in old}
            if any(i <= previous.acquired for i in new.keys() - known):
                return "identity conflict: new history behind complete watermark"
    quantities = defaultdict(int)
    identities = {}
    remaining = {}
    for execution in entries.values():
        if (type(execution.execution_id) is not int or not 0 < execution.execution_id < ev.acquired
                or type(execution.qty) is not int or execution.qty <= 0
                or execution.sym != ev.sym or execution.side not in ("buy", "sell")):
            return "invalid entry execution"
        identity = (execution.ref, execution.sym, execution.leg_id, execution.side)
        if identities.setdefault(execution.fill_id, identity) != identity:
            return "identity conflict: accounting lot reused"
        quantities[execution.fill_id] += execution.qty
        remaining[execution.execution_id] = execution.qty
    explicit = defaultdict(int)
    for reduction in sorted(reductions.values(), key=lambda r: r.execution_id):
        if (type(reduction.execution_id) is not int or not 0 < reduction.execution_id < ev.acquired
                or reduction.sym != ev.sym or not reduction.execution_allocations
                or reduction.transition not in ("explicit_scope", "triggered_protection")):
            return "invalid reduction"
        allocated = []
        for execution_id, qty in reduction.execution_allocations:
            entry = entries.get(execution_id)
            if (entry is None or execution_id >= reduction.execution_id
                    or type(qty) is not int or qty <= 0 or qty > remaining[execution_id]):
                return "invalid execution tranche allocation"
            remaining[execution_id] -= qty
            quantities[entry.fill_id] -= qty
            allocated.append((entry.fill_id, qty))
            if reduction.transition == "explicit_scope":
                explicit[entry.fill_id] += qty
        if tuple(allocated) != reduction.allocations:
            return "lot/tranche allocation mismatch"
        if reduction.transition == "triggered_protection":
            facts = ev.order_facts.get(reduction.order_ref, {})
            if (reduction.protection_owner not in identities
                    or facts.get("attached_to") != reduction.protection_owner):
                return "missing triggering protection identity"
    if dict(quantities) != ev.lots or set(ev.lot_facts) != set(quantities):
        return "gross quantities lack complete allocation proof"
    signed = 0
    for lot_id, qty in quantities.items():
        ref, sym, leg, side = identities[lot_id]
        facts = ev.lot_facts[lot_id]
        if (type(qty) is not int or qty < 0 or facts != {
                "entry_ref": ref, "sym": sym, "leg_id": leg, "side": side, "qty": qty}):
            return "gross lot identity mismatch"
        signed += qty if side == "buy" else -qty
    if signed != ev.position:
        return "net/gross quantity mismatch"
    if set(ev.protection_owners) != set(quantities):
        return "missing protection owner state"
    at_event = defaultdict(int)
    consumed_owners = set()
    for event_id in sorted(set(entries) | set(reductions)):
        if event_id in entries:
            entry = entries[event_id]
            at_event[entry.fill_id] += entry.qty
            continue
        reduction = reductions[event_id]
        for lot_id, qty in reduction.allocations:
            at_event[lot_id] -= qty
            if reduction.transition == "explicit_scope" and at_event[lot_id] == 0:
                consumed_owners.add(lot_id)
        if reduction.transition == "triggered_protection":
            consumed_owners.add(reduction.protection_owner)
        if not any(at_event.values()):
            consumed_owners.update(at_event)
    for lot_id, owner in ev.protection_owners.items():
        consumed = lot_id in consumed_owners
        if owner.get("consumed") is not consumed:
            return "protection consumption lacks execution proof"
        qty = owner.get("qty")
        if type(qty) is not int or qty < 0:
            return "invalid protection quantity"
        if consumed:
            if qty or owner.get("orders"):
                return "consumed owner retains protection"
        elif owner.get("orders"):
            total = sum(e.qty for e in entries.values() if e.fill_id == lot_id)
            if qty != total - explicit[lot_id]:
                return "protection quantity disagrees with allocation history"
        elif qty:
            return "bare owner has unexplained protection quantity"
    return None
