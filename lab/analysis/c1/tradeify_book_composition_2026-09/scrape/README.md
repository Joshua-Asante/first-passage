# MOC-imbalance signal collection — method, formats, and the sign caveat

The MES MOC-fade candidate needs an external series TradingView does not carry: the NYSE
closing-auction imbalance, published ~15:50 ET. Phase-B lane B1 named FinancialJuice as the
candidate free source and recorded its coverage as **unverified**
([`B1.2`](../../../../../docs/notes/research/2026-08-23-phase-b-lane-b1-falsifier-results.md)).
This directory is the collection attempt that resolved the coverage question and, more
importantly, found that **the sign is not recoverable for a third of the sessions**.

**The collected data is deliberately not committed.** It is a third-party provider's content;
only the derived verdicts and the method live here. Anyone re-running this must respect the
provider's terms and the polite pacing the scripts already use (1.3–2.5 s between requests,
exponential backoff).

## Where the data came from, and why not the site itself

`financialjuice.com` serves static HTML and its article pages carry a `dd Mon yyyy HH:MM` stamp,
but it has **no listing, feed-of-record, or search** for a single tag, throttles bursts (HTTP 429),
and allocates roughly 1,900 news ids per day — so enumerating it means an id-bisection scrape at
~3 h per year of history. Not run.

Its **public Telegram mirror** (`t.me/s/FinancialJuice`, the automated X→Telegram feed) is
enumerable: the preview pages backwards by `?before=<message id>`. Its `?q=` search covers only
about the last month, so history needs the plain listing. The channel's first message is
**2025-03-13**; nothing earlier exists there.

## Scripts

| Script | Role |
|---|---|
| `scrape_tg_moc.py` | First pass, `?q=` search. Covers ~1 month; kept as the record of why it is insufficient. |
| `walk_tg_moc.py` | Day-walker: learns an id→time model from every page fetched, estimates the id at 15:50 ET per trading day, fetches one page. 232 of 384 days on one fetch each. **Misses cluster where the channel's posting rate spikes** (war-headline days doubled the rate; a 6-step corrective walk cannot cross a 2-day estimate error). |
| `fill_gaps_tg_moc.py` | Deterministic second pass: groups unfound days into brackets between found prints and scans each bracket page by page. Takes `argv` bracket ranges so it can run as parallel workers. Recovered 110 of the 151 misses; the rest genuinely have no print. |
| `merge_and_build.py` | Merges walker + worker outputs, dedups by message id, compares each partial against the walker's **frozen** statuses (comparing against a mutating merge lets a later partial revert an earlier one). |
| `build_moc_table.py` | Parses post text → per-day table; splices Pine array literals. **Holds the sign rules.** |

## Coverage

| | |
|---|---|
| Span | 2025-03-14 → 2026-09-01 |
| Trading days examined | 383 |
| Days with a print | 342 (89.3% of weekdays) |
| Days with no print | 41, of which ~15 are US holidays/half-days |
| **Days with a usable sign** | **235** |

So the source is good but not complete, and B1.2's "unverified coverage" caution was warranted:
roughly 7% of ordinary sessions carry no print at all (e.g. 2026-07-14, 07-21, 07-22).

## ⚠ The sign caveat — a falsified inference, kept on the record

FinancialJuice posts MOC imbalance in **two coexisting formats**:

1. **Inline-sign.** `MOC Imbalance / S&P 500: +197 mln / Nasdaq 100: -6.5 mln`, and the
   `❗ … MLN` variant where negatives carry `-` and positives are bare. The sign is in the text.
   **235 of 342 days.**
2. **Colour-coded.** `🔴 MOC IMBALANCE / S&P 500: 2787.9 MLN / …` — magnitudes are **bare and
   absolute**, and a red/green marker carries the side. FinancialJuice states this itself: *"The
   colours will help tell you if buy side or sell side."*

**The Telegram mirror renders 🔴/🟢 as a plain `❗`, destroying the sign.** The first pass here
inferred "bare ⇒ buy-side" for the 107 all-bare days. That inference is **falsified** by direct
cross-check: the X original for **2025-04-30 19:51 UTC** (status `1917668077795238199`) is
**🔴 = sell-side** with figures S&P 2787.9 / NDX 1281.8 / DOW 999.8 / MAG7 1013.6 MLN — identical
to the digits this table had stored as buy-side.

Consequently:

- the 107 affected rows keep their (correct) **magnitudes**, are flagged `sign_source=bare-positive`
  in `inputs/moc_imbalance_daily.csv`, and are **excluded from the Pine table and from every
  figure in `MOC_FADE_REPLAY.md`**, which uses the 235 verified-sign sessions only;
- `build_moc_table.py` splices verified-sign rows only, and says so at the splice site;
- recovering them needs the X originals (colour marker intact) or FinancialJuice Elite.

**Standing rule earned here:** a sign convention must be verified **at the source**, never through
a mirror or reformatter, and the verification must include at least one known-opposite-sign date.
A format that encodes polarity outside the text (colour, emoji, icon) is one reformatting step away
from silent, systematic sign corruption — and the magnitudes still look perfect. Sibling of
`lesson_verify_source_not_label` and `lesson_verify_content_not_path_or_id`.
