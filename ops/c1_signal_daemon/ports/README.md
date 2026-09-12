# `ops/c1_signal_daemon/ports/` — private adapter port root (Track B)

Executable Python ports of the four fixed-book strategies live here on the
operator's primary checkout and **nowhere in git** (directory-local
`.gitignore` ignores everything but this README). They import the daemon's protocol, so they live inside `ops/` (the `core -> ops` import edge is illegal). They are the daemon
adapters of umbrella packets TB-A1..A4 and implement
`ops/c1_signal_daemon/book_protocol.BookStrategy`.

| File | `leg_id` | Ported from (`phase1_config.json` `pine_sha256`) |
|---|---|---|
| `aegis_6j.py` | `aegis_6j` | `db78ecba…` `aegis_6J1_venue_bound.pine` |
| `dj30_mym_p250.py` | `dj30_mym_p250` | `712cf395…` `striker_dj30_v4.5_mym_pyramid_250_cap100k.pine` |
| `vanguard_mgc.py` | `vanguard_mgc` | `af26899c…` `Vanguard_Gold_MGC_v0.4_venue_bound.pine` |
| `orb_mnq_v7.py` | `orb_mnq_v7` | `176c4f70…` `orb_mnq_7_reconstruction_venue_bound.pine` |

* Loader: `ops/c1_signal_daemon/book_adapters.py` (`FP_PORT_ROOT` overrides
  the root; default is this directory of the running checkout).
* Parity: `tests/ops/test_book_adapters_parity.py` replays each port through
  `ops/c1_signal_daemon/tv_broker_emulator.py` on the frozen CME panels and
  compares against the captured TradingView export by digest; skips when the
  private inputs are absent (public clone, CI, bare worktree).
* Hash pinning: each port's SHA-256 line is reported in its PR body and landed
  in `PORT_MANIFEST.sha256` by TB-A0 — never committed here.
* Worktrees: write ports here on the **primary checkout**, never under
  `.claude/worktrees/*` (private artifacts in a worktree die with it).
