# `ops/instruments/` — per-symbol ledgers

Source of record is `ops/instruments/<SYM>.md` (PROFILE blocks).
Do not hand-edit the generated matrix.

| File | Job |
|---|---|
| [`PROFILES.md`](PROFILES.md) | Generated mechanism × instrument matrix |
| [`MECHANISMS.md`](MECHANISMS.md) | Mechanism catalog |
| `<SYM>.md` | Ledger + PROFILE + notice rows |
| [`profiles.json`](profiles.json) | Generated machine view |

```text
python scripts/instrument_profiles.py check
python scripts/instrument_profiles.py build
```
