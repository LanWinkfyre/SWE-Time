# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
Fails with "Typethis.manufacturer?.toLowerCase is not a function"

### Paste the command

~/igir copy zip test --dat /Volumes/media/games/arcade/FBANEO/FinalBurn\ Neo\ \(ClrMame\ Pro\ XML\,\ Arcade\ only\).dat --input /Volumes/media/games/arcade/FBANEO/roms/ --output fbneo-fullnonmerged-78dcc8a/roms/ --merge-roms fullnonmerged --only-retail

### Describe the bug

When using the --only-retail option, this error occurs after parsing the DAT and before writing any output.  If I leave off that option, the error still occurs but only at the end of the process after roms have been written to the new location.

shawn@Shawns-Mac-mini:ext $ ~/igir copy zip test --dat /Volumes/media/games/arcade/FBANEO/FinalBurn\ Neo\ \(ClrMame\ Pro\ XML\,\ Arcade\ only\).dat --input /Volumes/media/games/arcade/FBANEO/roms/ --output fbneo-fullnonmerged-78dcc8a/roms/ --merge-roms fullnonmerged --only-retail

   @@@@@@   @@@@@@     @@@@@@    @@@@@@@@
 @@      @@  @@      @@      @@         @@
 @@      @@  @@      @@      @@         @@   ROM collection manager
   @@@@@@   @@         @@@@@@   @@@@@@@@@    https://igir.io/
          @@@     @@@@        @@@
     @@   @@        @@   @@   @@       @@    v4.2.0
     @@   @@        @@   @@   @@       @@
     @@   @@@@@@@@@@@@   @@   @@       @@

 ✓ Scanning for DATs » 1 DAT found
 ✓ Scanning for ROMs » 74,235 files found

 ∆ FinalBurn Neo - Arcade Games
   ■■■■■■■■■■■■■■■■■■■■■■■■■■■■     0/8,041
ERROR: Typethis.manufacturer?.toLowerCase is not a function
ERROR:     at _Game.isBootleg (file:///private/var/folders/yn/jlwxryrj1ds7jpvw931jk1jm0000gn/T/caxa/applications/igir/sm0kdh8bng/0/dist/bundle.js:3753:31)
ERROR:     at _Game.isRetail (file:///private/var/folders/yn/jlwxryrj1ds7jpvw931jk1jm0000gn/T/caxa/applications/igir/sm0kdh8bng/0/dist/bundle.js:3897:32)
ERROR:     at _DATStatus.pushValueIntoMap (file:///private/var/folders/yn/jlwxryrj1ds7jpvw931jk1jm0000gn/T/caxa/applications/igir/sm0kdh8bng/0/dist/bundle.js:16431:14)
ERROR:     at file:///private/var/folders/yn/jlwxryrj1ds7jpvw931jk1jm0000gn/T/caxa/applications/igir/sm0kdh8bng/0/dist/bundle.js:16405:18
ERROR:     at Array.forEach (<anonymous>)
ERROR:     at new _DATStatus (file:///private/var/folders/yn/jlwxryrj1ds7jpvw931jk1jm0000gn/T/caxa/applications/igir/sm0kdh8bng/0/dist/bundle.js:16404:20)
ERROR:     at _StatusGenerator.generate (file:///private/var/folders/yn/jlwxryrj1ds7jpvw931jk1jm0000gn/T/caxa/applications/igir/sm0kdh8bng/0/dist/bundle.js:17295:23)
ERROR:     at file:///private/var/folders/yn/jlwxryrj1ds7jpvw931jk1jm0000gn/T/caxa/applications/igir/sm0kdh8bng/0/dist/bundle.js:18354:58


### Expected behavior

Program does not error out and applies the --only-retail filter. 

### Debug logs

[igir_debug.txt](https://github.com/user-attachments/files/23153980/igir_debug.txt)

### DAT(s) used

https://archive.org/download/FBANEO/FinalBurn%20Neo%20%28ClrMame%20Pro%20XML%2C%20Arcade%20only%29.dat

### igir version

v4.2.0

### Node.js version

N/A

### Operating system

MacOS Version 15.6.1 

### Additional context

This example is from MacOS Sequoia, but I have reproduced the same error on Linux ARM (Raspberry Pi OS Bookworm) and Linux x86 Debian (also Bookworm).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `04ff5fc8ca51cf1632161c21638060be9c8db77b`.  There
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
{"case_id": "emmercm_igir__1900__04ff5fc",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
