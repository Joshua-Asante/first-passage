# `ops/c1_signal_daemon/` — offline replay library

The signal daemon retired with the c1 rail on 2026-10-29. Nothing here runs live or is
rebuilt, redeployed or armed. What remains is the offline replay surface: `book_protocol`,
`feed`, `pine_ta`, `tv_broker_emulator`, `fidelity_emulator`, `book_parity` and
`book_adapters`. The package keeps its name because the private ports in `ports/` import
it and that path is pinned in `core/strategies/BOOK_SOURCES.sha256`.

