"""Personal rail instance binding (ADR 2026-10-09 owed item 6): separate, no shared credentials."""
import copy
import json
from pathlib import Path

import pytest

import instance_binding as ib

ROOT = Path(__file__).resolve().parents[2]
BINDING = ROOT / "deploy" / "c1_rail_personal" / "instance_binding.json"


def _binding():
    return json.loads(BINDING.read_text(encoding="utf-8"))


def test_committed_binding_validates_and_is_not_activatable():
    binding = ib.validate(_binding())
    resolved = ib.resolve(binding)
    assert resolved["dry_run"] is True and resolved["armed_until"] is None
    assert resolved["halt_state_path"].startswith("/data/")
    assert not ib.activation_ready(binding)


def test_every_instance_key_is_overridden_away_from_the_tradeify_template():
    base = ib.load_base(_binding())
    resolved = ib.resolve(ib.validate(_binding()))
    for key in ib.INSTANCE_KEYS:
        assert resolved[key] != base[key], key


@pytest.mark.parametrize("mutate,match", [
    (lambda b: b.update(schema="v0"), "schema"),
    (lambda b: b["overrides"].pop("account"), "override"),
    (lambda b: b["overrides"].update(account="REPLACE_TRADEIFY_ACCOUNT_ID"), "shared"),
    (lambda b: b["overrides"].update(webhook_secret="REPLACE_WEBHOOK_SECRET"), "shared"),
    (lambda b: b.update(fly_app="c1-rail"), "app"),
    (lambda b: b.update(volume="c1_rail_data"), "volume"),
    (lambda b: b.update(firm_tier="Tradeify_Select_100K"), "tier"),
    (lambda b: b.update(firm_tier="Unknown"), "tier"),
    (lambda b: b["overrides"].update(dry_run=False), "disarmed"),
    (lambda b: b["overrides"].update(armed_until="2026-10-11T00:00:00+00:00"), "disarmed"),
    (lambda b: b["overrides"].pop("halt_state_path"), "halt"),
    (lambda b: b.update(extra=1), "fields"),
])
def test_invalid_bindings_refused(mutate, match):
    binding = copy.deepcopy(_binding())
    mutate(binding)
    with pytest.raises(ib.BindingError, match=match):
        ib.validate(binding)


def test_bound_destination_still_refused_while_items_3_4_open():
    binding = copy.deepcopy(_binding())
    binding["overrides"]["destination"] = "tradovate"
    with pytest.raises(ib.BindingError, match="destination"):
        ib.validate(binding)


def _filled(**values):
    keys = sorted(ib.INSTANCE_KEYS - {"destination"})
    return {k: values.get(k, f"{k}-value") for k in keys}


def test_filled_configs_must_share_no_credential():
    tradeify = _filled()
    personal = {k: f"personal-{v}" for k, v in tradeify.items()}
    ib.assert_no_shared_credentials(personal, tradeify)
    for key in tradeify:
        leaked = {**personal, key: tradeify[key]}
        with pytest.raises(ib.BindingError, match="shared"):
            ib.assert_no_shared_credentials(leaked, tradeify)
    # A Tradeify value reused under a different key is still shared.
    with pytest.raises(ib.BindingError, match="shared"):
        ib.assert_no_shared_credentials({**personal, "webhook_id": tradeify["secret_key"]}, tradeify)
    with pytest.raises(ib.BindingError, match="missing"):
        ib.assert_no_shared_credentials({}, tradeify)
