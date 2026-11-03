# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
copy extract fails with EBADF/LZMA Invalid distance on extraction; report succeeds on same files

### Paste the command

`npx igir@latest copy extract --dat "/media/nas/Games/Nintendo - Game Boy Advance/Nintendo - Game Boy Advance (20260812-060017).dat" --writer-threads 1 --reader-threads 1 --input "**/*.7z" --output ~/Games/staging/`

### Describe the bug

I believe this is a similar issue to #2415
`copy extract` and `move extract` fail on trying to extract any LZMA archives (`LZMA: Invalid distance` and `EBADF: bad file descriptor` errors) but report function runs fine

### Expected behavior

`igir` runs and copies or moves ROMs from LZMA2 .7z archives

### Debug log

[igir_2026-08-15T20;00;40.log](https://github.com/user-attachments/files/31107089/igir_2026-08-15T20.00.40.log)

### DAT(s) used

https://datomatic.no-intro.org/index.php?page=download&op=dat&s=23

### Additional context

### Environment
**igir:** 5.4.0 (`npx igir@latest`)
**Runtime:** Bun v1.3.14 and Node.js v22.23.1 (both fail identically)
**OS:** Linux x64 (Fedora 44 Kernel 7.1.5)
### Archive details
No-Intro GBA 7z archive
```
Type = 7z
Method = LZMA2:22
Solid = -
```
### Steps to reproduce
1. Run `igir report --dat "*.dat" --input "**/*.7z"` on a directory with either multiple 7z files or a single one with the above compression method which outputs a normal report with all games detected successfully 
2. Run `igir@latest copy extract --dat "*.dat" --input "**/*.7z" --dir-letter --output ~/Games/GBA/` which spits out `LZMA: Invalid distance` immediately on the first file and 
```node:events:497
      throw er; // Unhandled 'error' event
      ^

Error: EBADF: bad file descriptor, read
Emitted 'error' event on Readable instance at:
    at file:///home/nikcha/.npm/_npx/0d8028b15d717946/node_modules/7z-iterator/dist/esm/sevenz/ArchiveSource.js:128:23
    at file:///home/nikcha/.npm/_npx/0d8028b15d717946/node_modules/igir/dist/src/polyfill/gracefulFs.js:70:13
    at FSReqCallback.wrapper [as oncomplete] (node:fs:669:5) {
  errno: -9,
  code: 'EBADF',
  syscall: 'read'
}
``` 
but `igir` output claims files were written `✓ Nintendo - Game Boy Advance » 1/3,533 games, 0/5 BIOSes, 1/3,189 retail releases written` (either doesnt write the file or a severely malformed one `113512 'GAME.gba'` (completely wrong size for GBA game)
3. Reproducible on both Bun and Node runtimes even with a single file in directory
### Notes
I have tested this with `--reader-threads 1 --writer-threads 1` on a large collection and the same errors happened, on top of it also happening to a single file so I believe this is not related to concurrency

### Workaround
Use igir 4.2.0 which runs successfully
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
{"case_id": "emmercm_igir__2429__763ef99",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
