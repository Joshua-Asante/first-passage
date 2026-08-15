# Q-CAPALLOC-2 — RESULTS

**Verdict: `RESOLVED-FRAGILE` — `51/29` clears at the verified cell but does not survive the full 6-cell drift grid. No live change on this file's authority.**

**Pre-registration (operator-signed §9):**
[`Q-CAPALLOC-2-verdict-preregistration.md`](lab/archive/../../docs/briefs/pre-registration/Q-CAPALLOC-2-verdict-preregistration.md)
@ `509193b` · **Harness:** [`../run_capalloc.py`](lab/analysis/run_capalloc.py/) verbatim (CLI pin flags only; parent `SENSITIVITY` skipped on the three `PAYOUT_MIN=250` cells via [`run_cell_fast.py`](run_cell_fast.py) — main D1–D5 sweep unchanged) · **Artifacts:** this directory’s `w*_p*.json` · **Ran:** 2026-07-30.

---

## §1 — Controls

| # | Control | Result |
|---|---|---|
| 1 | Legacy drift sentinel (`--funded-ladder legacy --payout-min 1000`) | **PASSED** — eval 10.3 / pay 5.5 / cash 32,903.8 vs pins 10.3 / 5.5 / 32,904.0 ([`legacy_sentinel.json`](legacy_sentinel.json)) |
| 2–5 | Candidate set / cap / split-identity / half coverage | green on every cell (same harness controls) |

---

## §2 — 6-cell drift grid (verified ladder; halves only)

| cell | `WIN_MIN` | `PAYOUT_MIN` | winners (D1/D2 floor) | winners (all-four floor) | `51/29` both halves |
|---|---:|---:|---|---|---|
| `w150_p0` | 150 | 0 | `51/29` | *(none)* — H1 D4 headroom 0.07 pp < 1 sd | **noise-fragile** |
| **`w200_p0`** (verified) | **200** | **0** | **`51/29`** | **`51/29`** | **PASS** |
| `w250_p0` | 250 | 0 | `51/29` | `51/29` | PASS |
| **`w150_p250`** | **150** | **250** | *(none)* | *(none)* | **FAIL** — H1 D4 (dead@1y 25.75% vs inc 23.15%; headroom −0.60 pp) |
| `w200_p250` | 200 | 250 | `51/29` | `51/29` | PASS |
| `w250_p250` | 250 | 250 | `51/29` | `51/29` | PASS |

No candidate is in the intersection of all six cells. The verified centre retains `51/29` on both floor readings (H1 D1 +5.22 mo / D2 +32.5%; H2 D1 +0.91 mo / D2 +34.8% — matches the 2026-07-29 re-run reference).

---

## §3 — Gate application (§6)

**`RESOLVED-FRAGILE`.** Clears at (`WIN_MIN=200`, `PAYOUT_MIN=0`); fails ≥1 drift cell.

Binding fail: **`WIN_MIN=150` × `PAYOUT_MIN=250`** — the corner the pre-reg named as informative. Secondary: at `WIN_MIN=150` alone, D4 headroom on H1 is only 0.07 pp and fails the all-four seed-noise floor (parent AMBIGUOUS-(b) shape on that cell alone).

Pre-registered expectation (§7): `RESOLVED-FRAGILE` at least as likely as `RESOLVED-ROBUST`; `WIN_MIN=150` uncertain. **Met.**

---

## §4 — Disposition (no operator decision invented here)

Per §6: adoption of `51/29` is conditional on rules that may move. Route to operator with:

- failing cell named: **`WIN_MIN=150` ∩ `PAYOUT_MIN=250`** (and tripwire on `WIN_MIN=150` alone under the strict noise floor);
- explicit re-verify tripwire on those pins;
- **or** decline.

No plain GO. No `LEG_MAP` edit, no arming, no rung change. Any live change stays sequenced after B7-REFIRE Stage 2 + amending ADR.

Q-CAPALLOC-1 remains `AMBIGUOUS (d)` byte-unedited (Trap #12).
