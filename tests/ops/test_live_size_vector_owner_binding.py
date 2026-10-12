"""P-L2: the frozen size vector in the account owner's runtime binding.

Card: docs/briefs/handoffs/2026-10-11-live-size-vector-p-l2-owner-binding-card-DRAFT.md §4
(LB1-LB10), amended by docs/notes/2026-10-11-live-wiring-decision-packet.md §6c (legacy
reading at the same-session and takeover-plan comparisons). Synthetic vectors only.
"""
from dataclasses import replace
from datetime import timedelta
from fractions import Fraction
import hashlib
import json
import sqlite3

import pytest

from c1_rail.book_account_owner import AccountOwnerError, BookAccountOwner, BrokerFact, BrokerResult
from c1_rail.book_policy import (
    IDENTITY_SIZE_VECTOR, SizeVector, add_quantity, candidate_book_protection_policy,
    entry_quantities, validate_size_vector,
)
from c1_rail.c1_rail_listener import handle_book_action
from c1_rail.qualification.contract import canonical_json_bytes
from c1_signal_daemon.book_adapters import ADAPTER_BY_LEG
from c1_signal_daemon.book_protocol import Mode
from book_bootstrap_fixtures import BootstrapBroker, activate_fresh
from test_four_leg_runtime import NOW, add, binding, entry

KEYS = ("size_vector", "size_vector_sha256")
IDENTITY = IDENTITY_SIZE_VECTOR.as_mapping()
# Synthetic, public-mapping vector; not any screened or private value.
LOWERED = {
    "aegis_6j": {"base": 4, "adds": "UNCHANGED"},
    "dj30_mym_p250": {"risk_multiplier": "1/2", "cap_reserve_multiplier": "1/1", "adds": "UNCHANGED"},
    "vanguard_mgc": {"base_by_port": {"1": 1, "2": 1}, "adds": "UNCHANGED"},
    "orb_mnq_v7": {"base": 0, "adds": "UNCHANGED"},
}
ENTRY_QTY = {"aegis_6j": (8, 1), "dj30_mym_p250": (5, 24), "vanguard_mgc": (2, 1), "orb_mnq_v7": (1, 1)}


def vector(**legs):
    return validate_size_vector({**LOWERED, **legs})


def bound(size_vector=IDENTITY_SIZE_VECTOR):
    return {**binding(), "size_vector": size_vector}


def boot(path, data, broker=None):
    return BookAccountOwner.boot(path, "synthetic-account", binding=data,
                                 synthetic_broker=broker or BootstrapBroker([]))


def next_session(data):
    """The valid next session after ``data``'s session (prior-session chain intact)."""
    later = NOW + timedelta(days=1)
    out = dict(data)
    out["session"] = replace(
        data["session"], session_id="tradeify-account-day:2026-09-16",
        prior_session_id=data["session"].session_id, opens_at=later,
        risk_add_cutoff=later + timedelta(hours=1),
        flatten_start=later + timedelta(hours=1, minutes=10),
        own_flat_deadline=later + timedelta(hours=1, minutes=15), closes_at=later + timedelta(hours=2))
    out["settlement"] = replace(data["settlement"], session_id=data["session"].session_id,
                                as_of=later - timedelta(hours=2))
    out["as_of"], out["valid_until"] = later, later + timedelta(minutes=5)
    return out


def latest_body(path):
    with sqlite3.connect(path) as db:
        return json.loads(db.execute(
            "SELECT body FROM runtime_bindings ORDER BY sequence DESC LIMIT 1").fetchone()[0])


def rewrite_retained(path, mutate):
    """Rewrite the latest retained record as an older owner would have written it."""
    with sqlite3.connect(path) as db:
        sequence, raw = db.execute(
            "SELECT sequence, body FROM runtime_bindings ORDER BY sequence DESC LIMIT 1").fetchone()
        body = json.loads(raw)
        mutate(body)
        raw = json.dumps(body, sort_keys=True, separators=(",", ":"), allow_nan=False)
        db.execute("UPDATE runtime_bindings SET body=?, digest=? WHERE sequence=?",
                   (raw, hashlib.sha256(raw.encode()).hexdigest(), sequence))


def drop(*keys):
    return lambda body: [body.pop(key) for key in keys]


# ── LB1-LB3: validation at the consumption boundary ───────────────────────

def test_lb1_binding_without_size_vector_is_refused(tmp_path):
    data = bound()
    del data["size_vector"]
    with pytest.raises(AccountOwnerError, match="complete runtime binding required"):
        boot(tmp_path / "owner.sqlite", data)
    assert not (tmp_path / "owner.sqlite").exists()


CANONICAL = "canonical size vector required"


def test_lb1_none_is_not_identity(tmp_path):
    with pytest.raises(AccountOwnerError, match=CANONICAL):
        boot(tmp_path / "owner.sqlite", bound(None))
    assert not (tmp_path / "owner.sqlite").exists()


def test_lb2_untyped_mapping_is_refused(tmp_path):
    with pytest.raises(AccountOwnerError, match=CANONICAL):
        boot(tmp_path / "owner.sqlite", bound(dict(IDENTITY)))
    assert not (tmp_path / "owner.sqlite").exists()


def test_lb3_non_canonical_vector_is_refused(tmp_path):
    striker = replace(IDENTITY_SIZE_VECTOR.leg("dj30_mym_p250"), cap_reserve_multiplier="99/100")
    direct = SizeVector(tuple(striker if s.leg_id == "dj30_mym_p250" else s
                              for s in IDENTITY_SIZE_VECTOR.legs))
    with pytest.raises(ValueError, match="non-canonical"):
        validate_size_vector(direct.as_mapping())
    with pytest.raises(AccountOwnerError, match=CANONICAL):
        boot(tmp_path / "owner.sqlite", bound(direct))
    assert not (tmp_path / "owner.sqlite").exists()


# ── LB4-LB7: the stamp, its immutability and legacy records ───────────────

@pytest.mark.parametrize("size_vector", [IDENTITY_SIZE_VECTOR, vector()], ids=["identity", "lowered"])
def test_lb4_record_stamps_mapping_and_screen_hash(tmp_path, size_vector):
    path = tmp_path / "owner.sqlite"
    boot(path, bound(size_vector))
    body = latest_body(path)
    mapping = size_vector.as_mapping()
    assert body["size_vector"] == mapping
    assert body["size_vector_sha256"] == hashlib.sha256(canonical_json_bytes(mapping)).hexdigest()


def test_lb5_vector_cannot_change_within_session(tmp_path):
    path = tmp_path / "owner.sqlite"
    boot(path, bound())
    with pytest.raises(AccountOwnerError, match="runtime binding changed within session"):
        boot(path, bound(vector()))


def test_lb6_vector_cannot_change_across_sessions(tmp_path):
    path = tmp_path / "owner.sqlite"
    boot(path, bound())
    assert boot(path, next_session(bound())).permission == "HALTED"  # control: same vector boots
    path2 = tmp_path / "second.sqlite"
    boot(path2, bound())
    with pytest.raises(AccountOwnerError, match="unverified runtime binding transition"):
        boot(path2, next_session(bound(vector())))


@pytest.mark.parametrize("session", ["cross", "same"])
def test_lb7_legacy_record_reads_as_identity(tmp_path, session):
    path = tmp_path / "owner.sqlite"
    boot(path, bound())
    rewrite_retained(path, drop(*KEYS))
    data = next_session(bound()) if session == "cross" else bound()
    boot(path, data)  # no KeyError, no refusal


@pytest.mark.parametrize("session,message", [
    ("cross", "unverified runtime binding transition"),
    ("same", "runtime binding changed within session"),
])
def test_lb7_legacy_record_refuses_a_non_identity_vector(tmp_path, session, message):
    path = tmp_path / "owner.sqlite"
    boot(path, bound())
    rewrite_retained(path, drop(*KEYS))
    data = next_session(bound(vector())) if session == "cross" else bound(vector())
    with pytest.raises(AccountOwnerError, match=message):
        boot(path, data)


@pytest.mark.parametrize("session,message", [
    ("cross", "unverified runtime binding transition"),
    ("same", "runtime binding changed within session"),
])
@pytest.mark.parametrize("kept", KEYS)
def test_one_key_record_is_refused(tmp_path, session, message, kept):
    path = tmp_path / "owner.sqlite"
    boot(path, bound())
    rewrite_retained(path, drop(*(k for k in KEYS if k != kept)))
    data = next_session(bound()) if session == "cross" else bound()
    with pytest.raises(AccountOwnerError, match=message):
        boot(path, data)


@pytest.mark.parametrize("session,message", [
    ("cross", "unverified runtime binding transition"),
    ("same", "runtime binding changed within session"),
])
def test_keyless_record_does_not_match_anything(tmp_path, session, message):
    """Mutant kill: a key-less record still compares every other immutable field."""
    path = tmp_path / "owner.sqlite"
    boot(path, bound())

    def legacy_other_allocation(body):
        drop(*KEYS)(body)
        body["cap_allocations"]["aegis_6j"] = 70
    rewrite_retained(path, legacy_other_allocation)
    data = next_session(bound()) if session == "cross" else bound()
    with pytest.raises(AccountOwnerError, match=message):
        boot(path, data)


def test_migrated_legacy_pending_takeover_plan_boots(tmp_path):
    from c1_rail.book_migration import migrate_book_owner
    from test_book_bootstrap_migration import normal_binding, restore_fixture
    path = tmp_path / "owner.sqlite"
    restore_fixture(path, "3-pending_takeover.json")
    migrate_book_owner(path, "synthetic-account", now=NOW)
    with sqlite3.connect(path) as db:
        (plan,) = db.execute("SELECT body FROM takeover_plans").fetchone()
    assert not set(KEYS) & set(json.loads(plan)["admission_binding"])
    account = BookAccountOwner.boot(path, "synthetic-account", binding=normal_binding())
    assert account.permission == "HALTED"
    with pytest.raises(AccountOwnerError, match="runtime binding changed within session"):
        BookAccountOwner.boot(path, "synthetic-account",
                              binding={**normal_binding(), "size_vector": vector()})


def _legacy_takeover(tmp_path):
    from test_book_takeover_phases import TakeoverScenario, ready_without_attempt
    s = TakeoverScenario(tmp_path)
    ready_without_attempt(s)
    rewrite_retained(s.owner.path, drop(*KEYS))
    with sqlite3.connect(s.owner.path) as db:
        identity, raw = db.execute("SELECT operation_id, body FROM takeover_plans").fetchone()
        plan = json.loads(raw)
        for key in KEYS:
            plan["admission_binding"].pop(key)
        db.execute("UPDATE takeover_plans SET body=? WHERE operation_id=?",
                   (json.dumps(plan, sort_keys=True, separators=(",", ":")), identity))
    return s


def test_legacy_takeover_plan_admits_at_identity(tmp_path):
    s = _legacy_takeover(tmp_path)
    s.owner.resume_takeover(now=s.now)
    assert any(c.operation_id == s.root.order_id for c in s.broker.commands)


def test_legacy_takeover_plan_refuses_a_non_identity_vector(tmp_path):
    s = _legacy_takeover(tmp_path)
    s.owner.binding["size_vector"] = vector(aegis_6j={"base": 8, "adds": "UNCHANGED"})
    s.owner.resume_takeover(now=s.now)
    assert not any(c.operation_id == s.root.order_id for c in s.broker.commands)


# ── LB8-LB10: the owner sizes with the bound vector ───────────────────────

def owner(path, size_vector, results=()):
    account = boot(path, bound(size_vector), BootstrapBroker(list(results)))
    activate_fresh(account, now=NOW)
    return account


def law(leg_id, size):
    qty, stop = ENTRY_QTY[leg_id]
    inputs = dict(normal_base=qty)
    if leg_id == "dj30_mym_p250":
        inputs = dict(normal_base=qty, risk_dollars=100, cap_alloc=80,
                      per_contract_risk=Fraction(stop) * Fraction(str(ADAPTER_BY_LEG[leg_id].pointvalue)))
    return entry_quantities(leg_id, mode=Mode.NORMAL, policy=candidate_book_protection_policy(),
                            lifecycle_tier="AUTHORIZED", size=size, **inputs)[0]


@pytest.mark.parametrize("leg_id", ["aegis_6j", "dj30_mym_p250", "vanguard_mgc"])
def test_lb8_entry_uses_the_bound_vector(tmp_path, leg_id):
    quantities = {}
    for name, size_vector in (("identity", IDENTITY_SIZE_VECTOR), ("lowered", vector())):
        account = owner(tmp_path / name / "owner.sqlite", size_vector, [BrokerResult("accepted")])
        qty, stop = ENTRY_QTY[leg_id]
        outcome = handle_book_action(entry(leg_id, qty, stop=stop), account,
                                     occurrence=account.make_occurrence("direct", "lb8:" + name), now=NOW)
        assert outcome.quantity == law(leg_id, size_vector.leg(leg_id)) > 0
        assert account.exposure(leg_id) == (0, outcome.quantity)
        quantities[name] = outcome.quantity
    assert quantities["identity"] != quantities["lowered"]


def test_lb9_zero_leg_refuses_without_reserve_or_send(tmp_path):
    account = owner(tmp_path / "owner.sqlite", vector(), [BrokerResult("accepted")])
    outcome = handle_book_action(entry("orb_mnq_v7", 1), account,
                                 occurrence=account.make_occurrence("direct", "lb9"), now=NOW)
    assert outcome.refusal_reason == "zero_size"
    assert account.exposure("orb_mnq_v7") == (0, 0)
    assert account.synthetic_broker.commands == []


@pytest.mark.parametrize("adds", ["OFF", "UNCHANGED"])
def test_lb10_add_law_follows_the_vector(tmp_path, adds):
    striker = {"risk_multiplier": "1/1", "cap_reserve_multiplier": "1/1", "adds": adds}
    size_vector = vector(dj30_mym_p250=striker)
    fill = BrokerFact.fill("execution-1", "entry:dj30_mym_p250", "dj30_mym_p250", "entry", 1, 100.0, NOW)
    account = owner(tmp_path / "owner.sqlite", size_vector, [BrokerResult("accepted", (fill,))])
    handle_book_action(entry("dj30_mym_p250", 5, stop=24), account,
                       occurrence=account.make_occurrence("direct", "lb10-base"), now=NOW)
    account.observe(BrokerFact.terminal("entry:dj30_mym_p250", "cancelled", 1, NOW), now=NOW)
    assert account.exposure("dj30_mym_p250")[0] == 1
    account.activate_synthetic(now=NOW + timedelta(seconds=1))
    account.synthetic_broker.queue(BrokerResult("accepted"))
    commands = len(account.synthetic_broker.commands)
    outcome = handle_book_action(add("dj30_mym_p250", 12, stop=24), account,
                                 occurrence=account.make_occurrence("direct", "lb10-add"),
                                 now=NOW + timedelta(seconds=1))
    expected = add_quantity("dj30_mym_p250", 1, mode=Mode.NORMAL, policy=candidate_book_protection_policy(),
                            lifecycle_tier="AUTHORIZED", size=size_vector.leg("dj30_mym_p250"))
    if adds == "OFF":
        assert expected == 0 and outcome.refusal_reason == "zero_size"
        assert len(account.synthetic_broker.commands) == commands
    else:
        assert outcome.quantity == expected > 0
