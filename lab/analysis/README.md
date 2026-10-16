# `lab/analysis/` — hot campaign bodies + archive stubs

**Open [`../CATALOG.md`](../CATALOG.md) In flight first.** Do not glob this
directory to infer what is live. Hot bodies means the body is still here, not
“do this next.” The operator work list is [`STATE.md`](../../STATE.md).

| Layout | Meaning |
|---|---|
| `<theme>/<slug>/` | Hot body (theme README names the family) |
| `<slug>/CARD.md` | Archived stub only; body is `lab/archive/<slug>/` — **not** a second live tree |
| `_inbox/` | Cataloged theme — unassigned until RESULTS/PREREG/Verdict; must leave before `--slug` |

Theme READMEs today: `_inbox/`, `c1/`, `harvest/`, `regime/`, `striker/`, `aegis/`,
`orb/`, `legacy/`, `mc/`.
Archive tool: `python scripts/archive_lab_analysis.py --help`.

## Phase 2 leftovers (2026-08-22)

Not a second catalog. Status / `hot` cells still flip only via
`python scripts/archive_lab_analysis.py --slug …` then `--regenerate-catalog`.
Owner for the column split: [CATALOG schema rules](#catalog-schema-rules) below. This table remains the pin list (`--slug` still two-part);
CATALOG can now list a stay-hot terminal `status` with `hot=yes`.

**This pass slugged:** `dstruct_mnq_2026-08` (`NULL` — already on the RESULTS
card; Verdict stamped first so `--slug` could see it). Body:
[`lab/archive/dstruct_mnq_2026-08/`](../archive/dstruct_mnq_2026-08/).

| Hold / leave | Why `--slug` is refused or withheld |
|---|---|
| `msl_s2b_mym_2026-08` | HOLD; STAGE-1 FAIL is not archiveable |
| `cheap_falsifiers_2026-08` | HOLD; stay hot while CON-* cite them |
| `mnq_r2agrun_routeb_2026-08`, TNEC CON-2…5 | `AMBIGUOUS-HOLD` |
| `q_trainkill_{1,2,3}_2026-08` | HOLD |
| `xauusd_cgb_2026-06-15` | operational HOLD |
| `lab/analysis/time_to_pass.py` | C-P2-05; separate GO; Rule 16 inbound index first |
| `geofit_iid_sufficiency_power_2026-08-15`, `geofit_skewed_family_construction_2026-08-15` | stay-hot imports (C-P1-10) |
| `aegis_6j_prop_reconstruction_2026-07` | Wave-1 artifacts retained hot |
| `q_rail_1_2026-07` | rail evidence; many living cites |
| `msl_s4_mgc_2026-08` | PARKED; explore GO unpaid — [`README.md`](c1/msl_s4_mgc_2026-08/README.md) |
| informal ORB probes (`orbmnq1_*_probe_2026-08-20`) | C-P1-10 left ACTIVE |
| `rangestate_gc_2026-08` / `rangestate_corrected_2026-08` / `rangestate_mcl_2026-08` | family coupled; mixed SIGNAL-GENERIC |
| `ict_mnq_2026-08` | mixed W/D confirm; `cheap_falsifiers` coupling |
| `driftex_2026-08`, `eodadv_mnq_2026-08` | `**Verdict:** FALSIFIED` stamped 2026-08-23; stay-hot (frozen prereg + `rejected_candidates` + sentinel path pins); no `--slug` |
| `tnec_l2_sourcing_2026-08-10` | SCREEN-FAIL is not archiveable |
| NO_SOURCE slugs (`mnq_orb_level_proximity_tod_2026-08-06`, `mnq_sizediv_blind_2026-08`) | no RESULTS/README for `--slug` |

## CATALOG schema rules

Consolidated 2026-10-15 from 2026-08-22-catalog-hot-vs-disposition (removed; see
[TOMBSTONES](../../docs/adr/TOMBSTONES.md#2026-10-15-adr-decay-audit-removals)). Operator-ratified
2026-08-22 ("accepted. GO"), with addenda ratified 2026-08-29 and commissioned 2026-09-03. They bind
`scripts/archive_lab_analysis.py`, `scripts/check_status_consistency.py` (C2) and every CATALOG
reader.

1. **Two axes.** `hot` — is the body still under `lab/analysis/<theme>/<slug>/`? This, and only
   this, is what Hot-bodies-vs-Archived table membership means. `status` holds the
   **disposition** — the campaign verdict, read from the card's `**Verdict:**` field when one is
   present. `hot=yes` with a terminal disposition is a legal, common row. Neither the parser's
   field-precedence rule nor C2's join key may collapse the two back into one value.
2. **Keep the `status` column name; `hot` sits beside it.** Do not rename `status` →
   `disposition`: `check_status_consistency.py` reads it by name and `sync_liveness_indexes.py`
   carries further `status`-keyed references, so a rename is blast radius for a cosmetic gain.
   Revisiting it requires new Phase-0 evidence that this blast estimate was wrong, not a naming
   preference. A mixed schema (some tables renamed, others not) is not authorized, nor is a third
   schema (`hot` as a third status token, or a third table): the compound-token grammar
   (`**Status:** ACTIVE — NULL: …`) was the original masking bug.
3. **Verdict wins.** When a card's head carries both a `**Verdict:**` and a `**Status:**` field as
   separate lines, the disposition resolves from `**Verdict:**`, not from whichever field line
   appears first. Dominance inside a single value is unaffected: `HOLD` in the verdict clause still
   dominates a later terminal-looking token (do not archive an `AMBIGUOUS-HOLD` card); `NULL` in the
   verdict clause dominates a co-occurring `ACTIVE`.
4. **C2 joins to `hot`, not to disposition class:** it checks `hot == (table == "active")`. A
   `FALSIFIED` or `NULL` disposition in the Hot-bodies table is legal exactly when `hot=yes`.
   Unrecognised disposition tokens stay non-class-checked.
5. **`--slug` eligibility is unchanged and still two-part:** an archiveable disposition
   (`CLOSED` / `FALSIFIED` / `RETIRED` / `NULL`) **and** no stay-hot pin (`_hot_sys_path_dependent`
   plus the pins named in the table above). Parser/C2 honesty does not auto-move any body; do not
   silently loosen eligibility on that ground.
6. **The regenerator stays the sole CATALOG writer** (`archive_lab_analysis.py --regenerate-catalog`;
   C-P1-10); no hand-edit of a `status` or `hot` cell. **Sanctioned exception (2026-08-29):** when
   `--regenerate-catalog` would clobber concurrent worktree state, a single new row may be
   appended in slug-sorted position, verified by `git diff --stat` to add exactly that one line with
   no existing cell touched. This is not a general hand-edit license: any edit to an existing row's
   cells still requires the regenerator.
7. **Presentation (2026-09-03).** The Active table is headed `## Hot bodies` (internal table id
   stays `active`; parsers accept both headings). Hot means "keep the body," not "in flight." A
   generated `## In flight` comes first; its membership is derived, not "every leftover `ACTIVE`":
   lab slugs in the `STATE.md` operator-queue **Owner artifact** column, lab slugs in
   `docs/briefs/INDEX.md` `## Open` **Home (canonical)** (legacy header `Home` also accepted), and
   any head card (`RESULTS*` / `verdict.md` / `CLOSURE.md` / `README.md`) carrying
   `**In-flight:** yes`. Exclude `HOLD` and archiveable statuses. It is not the operator work list
   (that remains `STATE.md`).
8. **`ACTIVE` is forbidden on a decided campaign.** Stamp `**Verdict:**` as a separate line (the
   2026-09-03 mass-Verdict GO); do not `--slug`. `_inbox` stays a cataloged theme, rendered first
   under Hot bodies; outcome-bearing work must carry a Verdict and leave `_inbox` before `--slug`.
   Do not mass-relocate trees.
9. **Forbidden:** a sixth root doc; a `LIVE` token; mass `--slug`; hand-editing `status` / `hot`
   cells.

**Reversal.** If a full-corpus `python scripts/check_status_consistency.py` run raises C2 on a
`hot=yes` row whose pin is named in the table above, or fails to flag a row where `hot` and table
membership genuinely disagree, the join is defective. Repair it through a recorded decision (the
[ADR admission rule](../../docs/adr/2026-08-08-adr-ceremony-tiering.md) decides whether that needs an
ADR); never edit C2's logic or these rules silently. The path-conditional `status-consistency` gate
re-runs the check whenever `lab/CATALOG.md`, `docs/rejected_candidates.md` or `ops/instruments/` is
staged; the full corpus was clean on 2026-10-15; `tests/test_check_status_consistency.py` pins both
limbs.
