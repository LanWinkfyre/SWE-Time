# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
Regression: Zstd-compressed .7z (method 04F71101) no longer readable after switch to 7z-iterator (worked in v4 via 7zip-min)

## Summary

Igir **v4.x** could read **Zstandard-compressed `.7z` archives** (7z method **`04F71101`**, common in current No-Intro / RomVault sets) because it drove a real 7-Zip CLI via **`7zip-min`**.

Igir **v5.0+** replaced that with pure-JS **`7z-iterator`**, which does **not** implement that codec. Opening these archives fails (often as a hang / exit code **13** rather than a clean error). This is a **regression** for anyone whose primary collection is No-Intro `.7z` with Zstd.

## Regression window

| Version | `.7z` backend | Zstd-in-`.7z` (`04F71101`) |
|---------|----------------|----------------------------|
| **v4.x** (e.g. 4.2.0) | `7zip-min` → **7za** binary | ✅ worked |
| **v5.0.0+** (reproduced on **5.4.0**) | `7z-iterator` pure JS | ❌ broken |

Package evidence:
- v4.2.0 `package.json`: dependency `7zip-min`
- v5.0.0 / v5.4.0 `package.json`: dependency `7z-iterator` (no 7za path)

## Environment (repro)

- **igir:** 5.4.0 (`npx igir@5.4.0` / `@latest`)
- **Node:** v26.5.1 (also seen on v26.4.0)
- **OS:** Linux x64 (also expect pure-JS path to fail on macOS/Windows for the same bytes)
- **7z-iterator:** 2.2.9
- **xz-compat:** 1.2.7

## Archive details

Example No-Intro GBC archive metadata (`7z l -slt`):

```text
Type = 7z
Method = 04F71101
Solid = +
```

Per-entry method is also `04F71101` (Zstd inside the 7z container — **not** Zstd-in-ZIP / RVZSTD).

Note: Igir's documented Zstd support for **`.zip` / RVZSTD** is a different path and still works. This bug is specifically **Zstd as a 7z method**.

## Steps to reproduce

1. Take any solid No-Intro `.7z` with `Method = 04F71101` (or create one with a 7-Zip build that writes Zstd into `.7z`).
2. Run a minimal scan (no need for a full Love Pack DAT):

```bash
npx --yes igir@5.4.0 report \
  --dat /path/to/Nintendo\ -\ Game\ Boy\ Color\ \(Parent-Clone\).dat \
  --input /path/to/dir-with-zstd-7z \
  --input-checksum-min CRC32 \
  --input-checksum-max CRC32 \
  --reader-threads 1 \
  --disable-cache
```

3. Observe hang at "Scanning for ROMs" with progress stuck at `0B/...`, then process exit.

## Actual behavior

### UI / process

- Progress bars start (e.g. `0/N` files, `0B/...` on each archive).
- Process exits with **code 13** and:

```text
Warning: Detected unsettled top-level await at .../igir/dist/index.js
  await new Igir(options).main();
```

(Node documents exit code 13 as unsettled top-level await.)

### With `--debug-log`

Often a **secondary** crash during MultiBar teardown:

```text
Error: EBADF: bad file descriptor, write
  at Logger.write / printFrozenBar
  at MultiBar.freezeSingleBar / MultiBar.stop
  at process.exitHandler (.../multiBar.js)
```

Debug log typically ends right after `ROMScanner: found N input files` with no useful primary error.

### Root cause (library level)

Direct use of `7z-iterator` on the same file:

1. Header parse **succeeds**; entries and CRCs are visible.
2. Folder codec id is **`4-F7-11-1`** → `getCodecName` → `Unknown (4-F7-11-1)`, `isCodecSupported` → **false**.
3. `SevenZipParser.getEntryStream()` throws:

```text
UNSUPPORTED_CODEC  Unsupported codec: Unknown (4-F7-11-1)
```

4. `nextEntry()` calls `getEntryStream()` **without** try/catch and is expected to invoke its callback asynchronously. A **synchronous throw** leaves the async iterator / `stack-base-iterator` path unsettled → hang / exit 13 instead of a clean "unsupported archive" warning.

`7z-iterator`'s registered codecs include COPY, LZMA, LZMA2, BCJ*, Delta, Deflate, BZip2, AES — **no ZSTD / `04F71101`**.

Igir v5 intentionally does **not** fall back to system `7za`/`7zz` for `.7z` (docs: extract `.7z` without a third-party binary). So even if a full system 7-Zip is installed, igir 5.x never uses it for this path.

## Expected behavior

At least one of:

1. **Restore support** for Zstd-in-`.7z` (`04F71101`), e.g.:
   - implement Zstd in `7z-iterator` (Node has `zlib.createZstdDecompress` / igir already ships Zstd for zip/RVZSTD), and/or
   - optional fallback to system **`7zz`/`7za`** when the pure-JS codec set cannot open the archive (feature-detect method / on `UNSUPPORTED_CODEC`).
2. **Fail cleanly** if unsupported: per-file warning + continue, not process-wide hang / exit 13.
3. Document clearly that **Zstd-in-`.7z` is unsupported** in v5 (today docs only call out Zstd for **zip**), so users migrating from v4 know they must recompress or extract.

## Why this matters

Recent **No-Intro / RomVault** distributions increasingly ship solid **Zstd `.7z`**. Anyone upgrading **igir 4 → 5** loses the ability to scan those collections even though v4 worked on the same files.

## Workarounds (current)

- Stay on **igir 4.x** for Zstd-in-7z collections, or
- Pre-extract with a tool that supports the method (e.g. `py7zr`, official 7-Zip `7zz` where codec is present), then run igir on plain files / re-zip, or
- Repack to LZMA2 `.7z` or zip (including RVZSTD if desired for **output**).

## Related

- Igir docs "Reading Archives": `.7z` marked as extractable without third-party binary; Zstandard only mentioned for **`.zip`/`.zip64`**.
- Dependency change: `7zip-min` (v4) → `7z-iterator` (v5.0.0).

Happy to provide a sample archive or a minimal Node snippet that only exercises `7z-iterator` if useful.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `763ef991854fbafdfa521c8196cf0e61becb0251`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `main`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "emmercm_igir__2415__763ef99",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
