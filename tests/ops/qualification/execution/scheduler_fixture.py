"""Bounded scheduler request bytes shared by funding and future R2b scheduler tests."""
from c1_rail.qualification.contract import canonical_json_bytes as encoded
from test_campaign_budget import ATTEMPT


def schedule(**changes):
    """Canonical probe_worker/noop request for ATTEMPT; keyword overrides mutate fields."""
    return encoded(dict(dict(schema='qualification_campaign_schedule_request/v1',
        attempt_id=ATTEMPT, work_id='worker', role='probe_worker', probe='noop',
        signing_retry_of=None, fault=None), **changes))
