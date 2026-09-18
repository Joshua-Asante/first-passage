"""Canonical seed identities shared by legacy and protected execution."""
from dataclasses import dataclass
import hashlib
import json
from .regime import domain_seed

def canonical_bytes(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False,
                      allow_nan=False).encode('utf-8')


def _sha(value):
    return hashlib.sha256(value).hexdigest()


@dataclass(frozen=True)
class SeedInput:
    population: str
    path_index: int
    panel_index: int | None
    purpose: str
    canonical_bytes: bytes

    @property
    def sha256(self):
        return _sha(self.canonical_bytes)


def seed_input(contract, *, stage, population, panel_index, path_index,
               synthetic, purpose='path'):
    """Bind actual shared RNG call arguments and frozen source pool identity."""
    root=contract.replay.root_rng_namespace
    seed=domain_seed(root=root,stage=stage,population=population,panel_index=panel_index,
                     path_index=path_index,synthetic=synthetic,purpose=purpose)
    raw=canonical_bytes({'schema':'qualification-seed-input/v1',
        'contract_sha256':contract.contract_sha256,'root_rng_namespace':root,
        'trust_domain_sha256':contract.trust_domain_sha256,
        'stage':stage,'population':population,'panel_index':panel_index,
        'path_index':path_index,'purpose':purpose,'synthetic':synthetic,'seed':seed,
        'source_session_ids_sha256':_sha(canonical_bytes(list(contract.populations[population])))})
    return SeedInput(population,path_index,panel_index,purpose,raw)


