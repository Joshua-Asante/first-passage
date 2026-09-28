# S4 run logs: second-copy retention proposal

**Status:** APPROVED 2026-09-28 (option A) and executed; see the [ledger entry](../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling-and-execution--s4-run-logs-second-copy-m-41-2026-09-28). *Status at proposal, kept as history:* PROPOSAL, 2026-09-27, returned for operator approval; nothing below had been executed.

**Owner of the preservation record:** [full-E1 ledger, 2026-09-26 conditional ruling](../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--part-a-measurement-rule-conditionally-approved-s5-held-2026-09-26) ("Authorized: preservation of the existing S4 evidence"). Stage 0 context: [r2 §16.4](2026-09-27-s5-part-a-measurement-proposal-r2.md#164-stage-0). The ruling on this proposal belongs in that ledger.

## 1. Problem

The S4 run artifacts (runs 36180568493 and 36181780676, artifact `qualification-s2-supervision`) are preserved once, in the operator's primary checkout at `local_artifacts/s4-linux-run-logs-2026-09-25/`. `SHA256SUMS` there lists 222 files; its own SHA-256 is `e2c142281d819e071d15f99a242358f93389a479dcc5e6b5c1f6a20d5db189a7`.

M-41 ([methodology lessons](../methodology/lessons/methodology_lessons.md)) says a digest is not a copy: every pinned private file is registered and archived to `first-passage-archive` with `scripts/evidence_archive.py put`. None of these 222 files is registered in `docs/evidence/PRIVATE_EVIDENCE.sha256`, so `evidence_archive.py audit` does not list them. That is the silent single-copy state M-41 exists to prevent.

`put` skips any file over 95 MB (`MAX_BYTES`), because GitHub rejects files over 100 MB. Two files are over that limit:

| File | Bytes | SHA-256 |
|---|---:|---|
| `run-36180568493/boundary/journal.sqlite` | 110,350,336 | `0102ec140bf82adc03bb5db7b3f23dae0bbff42b8f788d07e538ed61d3ee6968` |
| `run-36181780676/boundary/journal.sqlite` | 110,469,120 | `d67b5d778fff4b32836f12f3dcc023bfc4afd1eeff0c4647847aef6d15bcd2a6` |

The other 220 listed files total 7,387,883 bytes and can be archived by `put` unchanged.

GitHub's own artifact copy expires about 2026-10-08 to 2026-10-09 (14-day retention; the runs' `createdAt` is still UNVERIFIED, r2 §12.1). Until then GitHub holds an incidental second copy. After that, the local directory is the only copy. That date is the natural deadline for this decision.

## 2. Measurements (read-only, 2026-09-27)

Run in the primary checkout against the originals. Compression was piped or done in memory; no copy was written.

| Codec | Run 36180568493 | Run 36181780676 |
|---|---:|---:|
| raw | 110,350,336 | 110,469,120 |
| `gzip -9` | 26,959,289 | 26,956,354 |
| `xz -6 -T0` (CLI) | 2,750,996 | 2,754,016 |
| Python `lzma.compress(preset=6)` (CPython 3.14.3) | **1,723,740** | **1,728,948** |

For both files, `lzma.decompress(lzma.compress(raw)) == raw` held, and the round trip reproduced the pinned digest. Two compressions in the same interpreter gave the same bytes. The files begin with the `SQLite format 3` header, and no `-wal` or `-shm` sibling is present.

Archive state: `first-passage-archive` is private, 146,397 KB on GitHub, clean on `main`, and uses no Git LFS.

## 3. Options

| Option | Fits in `put` | `audit --verify` works | Repo growth | Verdict |
|---|---|---|---|---|
| **A. xz-pack each large file; archive the `.xz` plus a packing manifest that maps each `.xz` digest to its original digest** | Yes (1.7 MB each) | Yes, for the `.xz` blob; the original digest is checked by decompressing (§5) | ~3.5 MB | **Recommended** |
| B. Split raw files into parts under 95 MB, with a reassembly hash | Yes | Parts only; reassembly checked by hand | ~221 MB, about 2.5× the archive's current size | Fallback, only if a future file still exceeds 95 MB once compressed (then split the `.xz`) |
| C. Git LFS on the archive | Bypasses `put` | **No.** `audit` reads the tree with `ls-tree`/`cat-file`, which see LFS pointer files, so `--verify` would hash the pointer and report CORRUPT | LFS quota, billed separately | Reject |
| D. Another store (OneDrive, Drive, release asset) | No | No; outside the audit | none in git | Optional third copy only; it cannot be the M-41 copy, because nothing audits it |

A is the simplest route. It needs no code change, stays inside the content-addressed archive, and costs about 3.5 MB.

## 4. Proposed execution (each step needs operator approval; none has run)

1. **Pre-check (read-only).** In the primary checkout: `sha256sum` of `SHA256SUMS` equals `e2c14228…189a7`, and `sha256sum -c --quiet SHA256SUMS` passes.
2. **Pack beside the originals, never inside them.** Write `local_artifacts/s4-linux-run-logs-2026-09-25.packed/run-<id>/boundary/journal.sqlite.xz` with the ops interpreter (`.\fp.ps1 python`), using `lzma.compress(raw, preset=6)`. Decompress each result and check that it hashes to the original digest. Write `PACKED_SHA256SUMS.tsv` in that directory, one row per packed file: `.xz` SHA-256, `.xz` bytes, original SHA-256, original bytes, original relative path, codec (`xz, lzma preset 6, CPython <version>`). The original directory is not touched, so its file count and `SHA256SUMS` stay as recorded.
3. **Archive.** Run `scripts/evidence_archive.py put` on the 220 small files, `SHA256SUMS`, both `.xz` files and `PACKED_SHA256SUMS.tsv`: 224 files, about 11 MB. Commit and push `first-passage-archive` with the `-c core.autocrlf=false` commands `put` prints. **This push is the outward step; it needs the operator's GO.**
4. **Register (public-repo PR).** Add to `docs/evidence/PRIVATE_EVIDENCE.sha256`, under one dated comment block citing this note and the ledger entry: the 221 direct digests (220 files plus `SHA256SUMS`), the two `.xz` digests and the manifest digest. The comment maps each `.xz` digest to its original digest. The originals' digests are **not** registered as pins, because `audit` would report them MISSING (the archived blob is the `.xz`). No log content enters the public repository: only digests and relative file names, consistent with r2 §12.1's rule that hashes may be committed and raw logs never are.
5. **Verify.**
   - `evidence_archive.py audit --verify` shows all 224 digests ARCHIVED.

   *[Corrected 2026-09-28: the 224 inputs hold 120 distinct digests. The registry test requires unique digests, so each is pinned once and 120 pins were registered. See the ledger entry.]*
   - A decompression check reads the committed blob from the archive's remote ref: `git -C <archive> cat-file blob origin/main:evidence/sha256/<aa>/<xz digest>`, decompressed with Python `lzma` and hashed, equals `0102ec14…6968` and `d67b5d77…d2a6` respectively. Use `cat-file`, per M-41's extraction rule, not `checkout` or `archive`.
6. **Record.** Add a dated line to the ledger entry: the archive commit, the audit counts and the decompression check result.

**Restore path** (documented in `PACKED_SHA256SUMS.tsv`'s header and the registry comment): extract with `git cat-file blob`, decompress with `lzma`/`xz -d`, check the original digest, then check with `sha256sum -c SHA256SUMS` from the restored directory.

## 5. Follow-up (not proposed for execution now)

S5 Stage 1b measure runs use the same workflow and are likely to produce `journal.sqlite` files of this size again. If that happens, a small `evidence_archive.py` change would make this a supported path rather than a manual one. That change would add `put --xz` for files over `MAX_BYTES`, an INDEX row that records the original digest, and an `audit` rule that treats an original pin as ARCHIVED when a packed row exists, with `--verify` decompressing the blob. The original digest would then be the registered pin. That is a separate ticket, a candidate for a GLM dispatch under a frozen spec.

## 6. Decision requested

1. Approve option A as the retention method for this set (or name B, C or D).
2. GO for steps 2–3, including the push to `first-passage-archive`.
3. GO for the step-4 registry PR.

Until then, the local directory remains the only durable copy, and GitHub's artifact copy expires about 2026-10-08 to 2026-10-09.
