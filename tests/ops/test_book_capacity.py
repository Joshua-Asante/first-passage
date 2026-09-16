"""Synthetic owner events exercise conservation and fail-closed capacity."""
from dataclasses import replace
from datetime import datetime, timedelta, timezone

import pytest

from c1_rail.book_capacity import (
    CapacityState, Event, Reserve, Fill, Terminal, Reduction, Quiescence,
    CompleteTakeover, apply_event, exposures, used_micro,
)

NOW = datetime(2026, 9, 14, 15, tzinfo=timezone.utc)
AGE = timedelta(seconds=30)


def step(state, fact, seq=None, **kwargs):
    seq = state.sequence + 1 if seq is None else seq
    event = Event(f"event-{seq}", seq, NOW, "account", "epoch", fact)
    return apply_event(state, replace(event, **kwargs), now=NOW, max_age=AGE)


def flat():
    return CapacityState("account", "epoch")


def reserve(op="base", leg="dj30_mym_p250", qty=22):
    return Reserve(op, leg, "SYNTHETIC-" + leg, qty)


def test_partial_fill_terminal_and_reduction_conserve_gross():
    initial = flat()
    state = step(initial, reserve())
    assert used_micro(state) == 22 and used_micro(initial) == 0
    state = step(state, Fill("execution", "base", 7))
    own = next(e for e in exposures(state) if e.leg_id == "dj30_mym_p250")
    assert (own.confirmed, own.reserved) == (7, 15)
    state = step(state, Terminal("base", "cancelled", 7))
    assert used_micro(state) == 7
    state = step(state, Reduction("reduction", "close-request", (("execution", 3),)))
    assert used_micro(state) == 4 and not state.blocks


def test_exact_event_and_broker_fact_replays_do_not_double_count():
    state = step(flat(), reserve())
    event = Event("fill", 2, NOW, "account", "epoch", Fill("exec", "base", 5))
    state = apply_event(state, event, now=NOW, max_age=AGE)
    assert apply_event(state, event, now=NOW + timedelta(days=1), max_age=AGE) == state
    state = step(state, event.fact)
    assert used_micro(state) == 22 and not state.blocks
    state = step(state, Terminal("base", "cancelled", 5))
    reduction = Reduction("red", "close", (("exec", 2),))
    state = step(step(state, reduction), reduction)
    assert used_micro(state) == 3 and not state.blocks


@pytest.mark.parametrize("fact", [
    Fill("exec", "unknown", 1), Fill("exec", "base", 23),
    Terminal("base", "cancel_ack", 0), Terminal("base", "filled", 0),
    Terminal("base", "cancelled", 1), reserve(qty=21),
    Reduction("red", "close", (("unknown", 1),)),
])
def test_invalid_evidence_preserves_capacity_and_blocks(fact):
    state = step(step(flat(), reserve()), fact)
    assert used_micro(state) == 22 and state.blocks
    assert used_micro(step(state, reserve("other", qty=1))) == 22


@pytest.mark.parametrize("changes", [
    {"account_id": "wrong"}, {"owner_epoch": "old"}, {"sequence": 1},
    {"as_of": NOW - timedelta(seconds=31)}, {"as_of": NOW + timedelta(seconds=1)},
    {"as_of": NOW.replace(tzinfo=None)}, {"sequence": True}, {"event_id": ""},
])
def test_invalid_envelope_cannot_release(changes):
    state = step(flat(), reserve())
    state = step(state, Terminal("base", "cancelled", 0), **changes)
    assert used_micro(state) == 22 and state.blocks


def test_conflicting_execution_or_delivery_id_is_sticky():
    state = step(step(flat(), reserve()), Fill("exec", "base", 5))
    for changes in ({}, {"event_id": "event-2"}):
        bad = step(state, Fill("exec", "base", 6), **changes)
        assert bad.blocks and used_micro(bad) == 22


def test_cap_is_gross_and_no_clipping_or_refused_operation_reuse():
    state = step(flat(), reserve("aegis", "aegis_6j", 8))
    assert used_micro(state) == 80
    state = step(state, reserve("micro", qty=1))
    assert used_micro(state) == 80 and not state.blocks
    state = step(state, Terminal("aegis", "cancelled", 0))
    state = step(state, reserve("micro", qty=1))
    assert used_micro(state) == 0  # refused identity cannot turn into a new request


def prepared():
    state = step(flat(), reserve("mym", qty=10))
    state = step(state, reserve("orb", "orb_mnq_v7", 1))
    state = step(state, reserve("aegis", "aegis_6j", 8))
    assert state.takeover.displaced == ("orb_mnq_v7", "dj30_mym_p250")
    assert used_micro(state) == 11 and state.blocks
    return state


def proof(state, **kwargs):
    return replace(Quiescence(state.sequence + 1, state.takeover.displaced,
                              0, 0, 0, 0), **kwargs)


def test_takeover_requires_terminal_release_then_new_quiescence():
    state = prepared()
    blocked = step(state, CompleteTakeover("aegis", proof(state)))
    assert blocked.blocks and used_micro(blocked) == 11
    state = step(state, reserve("competing", "vanguard_mgc", 1))
    state = step(state, Terminal("orb", "cancelled", 0))
    state = step(state, Terminal("mym", "cancelled", 0))
    state = step(state, CompleteTakeover("aegis", proof(state)))
    assert not state.blocks and state.takeover is None and used_micro(state) == 80


@pytest.mark.parametrize("changes", [
    {"sequence": 1}, {"legs": ()}, {"gross": 1}, {"working": 1},
    {"protection": 1}, {"pending": 1}, {"gross": False},
])
def test_takeover_bad_proof_retains_block(changes):
    state = prepared()
    state = step(step(state, Terminal("orb", "cancelled", 0)),
                 Terminal("mym", "cancelled", 0))
    state = step(state, CompleteTakeover("aegis", proof(state, **changes)))
    assert state.blocks and state.takeover is not None and used_micro(state) == 0


def test_takeover_filled_lots_need_reduction_not_only_terminal():
    state = step(flat(), reserve("mym", qty=10))
    state = step(state, Fill("exec", "mym", 10))
    state = step(state, Terminal("mym", "filled", 10))
    state = step(state, reserve("aegis", "aegis_6j", 8))
    bad = step(state, CompleteTakeover("aegis", proof(state)))
    assert bad.blocks and used_micro(bad) == 10
    state = step(state, Reduction("red", "close", (("exec", 10),)))
    state = step(state, CompleteTakeover("aegis", proof(state)))
    assert used_micro(state) == 80 and not state.blocks


def test_completed_takeover_fact_can_be_reacquired():
    state = prepared()
    state = step(step(state, Terminal("orb", "cancelled", 0)),
                 Terminal("mym", "cancelled", 0))
    completed = CompleteTakeover("aegis", proof(state))
    state = step(step(state, completed), completed)
    assert used_micro(state) == 80 and not state.blocks


@pytest.mark.parametrize("quantity", [0, -1, True, 1.5, "1"])
def test_invalid_quantity_never_reserves(quantity):
    state = step(flat(), reserve(qty=quantity))
    assert state.blocks and used_micro(state) == 0


def test_reduction_conflict_and_overrelease_keep_existing_accounting():
    state = step(step(flat(), reserve()), Fill("exec", "base", 7))
    state = step(state, Reduction("red", "close", (("exec", 3),)))
    for reduction in (Reduction("red", "other-close", (("exec", 3),)),
                      Reduction("red-2", "close", (("exec", 5),)),
                      Reduction("red-3", "close", (("exec", 1), ("exec", 1)))):
        bad = step(state, reduction)
        assert bad.blocks and used_micro(bad) == 19


def test_one_close_request_cannot_change_leg_or_symbol():
    state = step(step(flat(), reserve()), Fill("exec", "base", 7))
    state = step(state, Reduction("red", "close", (("exec", 1),)))
    state = step(state, reserve("orb", "orb_mnq_v7", 1))
    state = step(state, Fill("orb-exec", "orb", 1))
    state = step(state, Reduction("red-2", "close", (("orb-exec", 1),)))
    assert state.blocks and used_micro(state) == 22


def test_event_replay_reconstructs_identical_state_including_blocks():
    state = prepared()
    state = step(state, Fill("unexpected", "unknown", 1))
    restored = flat()
    for event in state.receipts:
        restored = apply_event(restored, event, now=NOW, max_age=AGE)
    assert restored == state


def test_entry_and_close_share_a_unique_request_namespace():
    state = step(step(flat(), reserve()), Fill("exec", "base", 7))
    bad = step(state, Reduction("red", "base", (("exec", 1),)))
    assert bad.blocks and used_micro(bad) == 22
    state = step(state, Reduction("red", "close", (("exec", 1),)))
    bad = step(state, reserve("close", "orb_mnq_v7", 1))
    assert bad.blocks and used_micro(bad) == 21
