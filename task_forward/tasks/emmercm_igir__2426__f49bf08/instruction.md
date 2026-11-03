# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
`--input-checksum-archives auto` is decided run-wide: one MAME DAT forces archive hashing of every input file

### Paste the command

```
igir report \
  -d "E:/dats/Fresh1G1R/daily-1g1r-dat/McLean" \
  -d "E:/dats/MAME_Dats_288/DATs" \
  --dat-name-regex-exclude "/encrypted|headerless/i" \
  -i "E:/utils/bench-many" \
  --disable-cache --reader-threads 4
```

Input is 8 Nintendo Wii `.rvz` files (49.7 GB compressed, ~4.38 GiB decompressed each). igir v5.4.0, Node.js v24.19.0, Windows 11, Ryzen 9950X3D (16c/32t).

### Describe the bug

`--input-checksum-archives auto` is resolved **once for the whole run**, not per DAT. `src/igir.ts:501`:

```ts
private determineScanningChecksumArchives(dats: DAT[]): boolean {
  if (this.options.getInputChecksumArchives() === InputChecksumArchivesMode.NEVER) {
    return false;
  }
  if (this.options.getInputChecksumArchives() === InputChecksumArchivesMode.ALWAYS) {
    return true;
  }
  return dats.some(
    (dat) =>
      dat.isMame() &&
      dat.getGames().some((game) =>
        game.getRoms().some((rom) => {
          const isArchive = FileFactory.isExtensionArchive(rom.getName());
          ...
```

The result is a single boolean, computed at `igir.ts:146` and passed into the ROM scanner. So if **any** MAME DAT in the run references an archive, igir calculates raw-archive checksums for **every input file in the run** — including files that no MAME DAT could ever match.

For disc images this is expensive. Each Wii `.rvz` gets processed twice: once reconstructing the ~4.38 GiB decrypted/re-hashed image for its content checksums, and again reading the 4–6 GB `.rvz` container itself. The visible symptom is the scanned-entry count doubling.

### Measurements

Same 8 Wii `.rvz` files, `report`, `--disable-cache`, `--reader-threads 4`:

| DATs | `--input-checksum-archives` | `Scanning for ROMs` | total | ≈ per file |
|---|---|---|---|---|
| 1 (Redump Wii only) | default (`auto`) | **8 files found** | 67.0s | ~8.2s |
| 324 (console + MAME sets) | default (`auto`) | **16 files found** | 332.5s | ~34.7s |
| 324 (console + MAME sets) | `never` | **8 files found** | 206.6s | ~19.0s |

Per-file figures solve out assuming ~55s of fixed DAT parsing for the 324-DAT rows and ~1.5s of startup for the single-DAT row.

The duplicate archive pass costs **~126s across 8 files (~15.7s/file)** and produces nothing usable: none of the loaded MAME DATs can match a Wii RVZ. The entry count halving from 16 to 8 with `never` confirms the second pass is the cause.

### Expected behavior

Archive-checksum calculation should be scoped to input files that could plausibly match an archive-referencing DAT, rather than enabled globally. Some options, roughly in increasing order of effort:

1. Decide per DAT rather than per run, and only hash raw archives when matching against the DATs that reference archives.
2. Keep the run-wide flag, but skip the raw-archive pass for input file extensions that no archive-referencing DAT mentions.
3. At minimum, document that mixing MAME DATs with disc-image inputs in one invocation roughly doubles I/O per input file, and that `--input-checksum-archives never` is the workaround for the non-MAME pass.

The current workaround is to split the run — one invocation per DAT family, with `--input-checksum-archives never` on the passes that need no archive matching. That works, but it is not discoverable: nothing in the output indicates that adding a MAME DAT has doubled the work for unrelated inputs.

### Debug log

[igir-bench.log](https://github.com/user-attachments/files/31040474/igir-bench.log)

### DAT(s) used

- `Nintendo - Wii (Redump - Fresh1G1R - McLean).dat` (1,443 games) - Full `Fresh1G1R/daily-1g1r-dat/McLean` set plus `MAME_Dats_288/DATs` — 324 DATs total, including MAME sets of 50,111 / 50,100 / 43,964 / 40,166 games

### Additional context

**A second, unexplained cost.** Even with `--input-checksum-archives never`, per-file cost with 324 DATs is ~19.0s versus ~8.2s with a single DAT — a further ~10.8s per input file that appears to scale with the number of loaded DATs. `CandidateGenerator.generate()` iterates `dat.getGames()` (`candidateGenerator.ts:70`) rather than input files, and `IndexedFiles` lookups are hash-based (`indexedFiles.ts:43-101`), so nothing obvious there should scale per input file. This is reported as an observation, not a diagnosis — it may well be a measurement artifact of solving two equations from three data points, and it deserves its own investigation rather than being bundled into this issue.

**Things measured and ruled out** during the same investigation, recorded so nobody re-treads them:

- Read chunk size in `packages/dolphin-tool/index.ts` — per-read dispatch cost is 36–354µs, ~1% of wall time for a multi-GiB image.
- `UV_THREADPOOL_SIZE` — the Wii reconstruction path spawns its own threads via `std::async` and does not use the libuv pool; raising it changed nothing.
- Reader concurrency — `--reader-threads` 1 / 4 / 8 measured 121.7s / 67.0s / 68.0s on 8 files, so concurrency helps up to ~4 and then plateaus. (Field data at 16 concurrent large images was much worse, but that could not be reproduced with only 8 input files.)
- JS-side checksum count — `--input-checksum-max CRC32` versus `SHA1` measured 77.5s versus 77.8s, i.e. no difference. The Wii hash tree inside reconstruction dominates the output digests.

**Separate, lower priority:** the bundled `dolphin-tool` addon compiles Dolphin's crypto without hardware acceleration (`stubs/mbedtls_config.h` leaves `MBEDTLS_AESNI_C` / `MBEDTLS_HAVE_ASM` undefined; `binding.gyp:305` selects `GenericCPUDetect.cpp`). Measured at ~1.5x on one Wii RVZ versus igir 5.3.1 shelling out to a hardware-accelerated `DolphinTool` binary (6.1s vs 8.6s). Happy to file that separately if it's of interest — it is a deliberate-looking constraint (zstd carries `ZSTD_DISABLE_ASM` too), and it is a much smaller effect than the issue above.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `f49bf08f4fb5ae37268183d085e5d53d9be80d47`.  There
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
{"case_id": "emmercm_igir__2426__f49bf08",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
