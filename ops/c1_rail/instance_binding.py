"""Personal rail instance binding (ADR 2026-10-09 owed item 6), configuration as code.

The binding is an overlay on the shared rail template: it names its own Fly app,
volume and tier and overrides every instance key, so no credential or account
identity is inherited from, or equal to, the Tradeify instance. The destination
stays unbound (refused) until ADR items 3-4 close; activation is P4's arm check.
"""
from __future__ import annotations

import json
import sys
import tomllib
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT / "core") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "core"))

import firm_rules  # noqa: E402

SCHEMA = "c1_rail_instance_binding/v1"
UNBOUND = "UNBOUND_PENDING_ADR_2026_10_09_ITEMS_3_4"
# Credential and identity keys: each instance supplies its own value.
INSTANCE_KEYS = frozenset({"account", "path_token", "crosstrade_api_token", "secret_key",
                           "webhook_id", "webhook_secret", "destination"})
_FIELDS = {"_comment", "schema", "instance", "firm_tier", "fly_app", "volume",
           "base_config", "base_fly_toml", "overrides"}


class BindingError(ValueError):
    """The binding is incomplete, shares an identity with Tradeify, or is not activatable."""


def load_base(binding):
    return json.loads((_REPO_ROOT / binding["base_config"]).read_text(encoding="utf-8"))


def _base_fly(binding):
    fly = tomllib.loads((_REPO_ROOT / binding["base_fly_toml"]).read_text(encoding="utf-8"))
    return fly["app"], {m["source"] for m in fly.get("mounts", [])}


def validate(binding):
    if type(binding) is not dict or set(binding) != _FIELDS:
        raise BindingError("binding fields must match the closed schema")
    if binding["schema"] != SCHEMA:
        raise BindingError("unknown binding schema")
    row = firm_rules.FIRM_RULES.get(binding["firm_tier"])
    if row is None or row.get("starting_balance_source") != "private":
        raise BindingError("firm_tier must be the private personal tier")
    app, volumes = _base_fly(binding)
    if binding["fly_app"] == app:
        raise BindingError("fly app shared with the Tradeify instance")
    if binding["volume"] in volumes:
        raise BindingError("volume shared with the Tradeify instance")
    over, base = binding["overrides"], load_base(binding)
    missing = INSTANCE_KEYS - set(over)
    if missing:
        raise BindingError(f"instance override missing: {sorted(missing)}")
    base_values = {v for v in base.values() if isinstance(v, str)}
    for key in INSTANCE_KEYS - {"destination"}:
        if not isinstance(over[key], str) or over[key] in base_values:
            raise BindingError(f"{key} shared with the Tradeify template")
    if over["destination"] != UNBOUND:
        raise BindingError("destination must stay unbound until ADR 2026-10-09 items 3-4")
    if over.get("dry_run") is not True or over.get("armed_until") is not None:
        raise BindingError("binding must ship disarmed")
    if not str(over.get("halt_state_path", "")).startswith("/data/"):
        raise BindingError("halt_state_path on this instance's volume is required")
    return binding


def resolve(binding):
    return {**load_base(binding), **binding["overrides"]}


def activation_ready(binding):
    """False while the destination is unbound; P4 owns the arm-time check."""
    return validate(binding)["overrides"]["destination"] != UNBOUND


def assert_no_shared_credentials(personal, tradeify):
    """Filled configs: no instance-key value of one may appear anywhere in the other's."""
    keys = INSTANCE_KEYS - {"destination"}
    absent = [k for k in keys if not personal.get(k) or not tradeify.get(k)]
    if absent:
        raise BindingError(f"credential missing: {sorted(absent)}")
    if {personal[k] for k in keys} & {tradeify[k] for k in keys}:
        raise BindingError("credential shared between instances")
