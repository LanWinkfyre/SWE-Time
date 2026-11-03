# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
completely skip `.chd` files

### Is your feature request related to a problem?

https://github.com/libretro/libretro-database/blob/82e7063f139a21289b94921087637d73f1b34e8f/dat/System.dat

```
$ igir copy test --cache-path ~/.cache/igir.cache --dat '/path/to/dat/System.dat' --input /input/path/roms --input-checksum-quick --dir-game-subdir never --exclude-disks --output /output/path/
   @@@@@@   @@@@@@     @@@@@@    @@@@@@@@
 @@      @@  @@      @@      @@         @@
 @@      @@  @@      @@      @@         @@   ROM collection manager
   @@@@@@   @@         @@@@@@   @@@@@@@@@    https://igir.io/
          @@@     @@@@        @@@
     @@   @@        @@   @@   @@       @@    v3.4.2
     @@   @@        @@   @@   @@       @@
     @@   @@@@@@@@@@@@   @@   @@       @@


✓ Scanning for DATs ··············· | 1 DAT found
WARN:  /input/path/roms/game1/game1.chd: quick checksums will skip .cue/.bin files in CD-ROM CHDs
WARN:  /input/path/roms/game2/game2.chd: quick checksums will skip .cue/.bin files in CD-ROM CHDs
WARN:  /input/path/roms/game3/game3.chd: quick checksums will skip .gdi/.bin/.raw files in GD-ROM CHDs
WARN:  ...
WARN:  ...
\\\ lots of other CHDs
WARN:  /input/path/roms/gameN/gameN.chd: quick checksums will skip .gdi/.bin/.raw files in GD-ROM CHDs
# Scanning for ROMs ··············· | ████▒░░░░░░░░░░░░░░░ | 12.053/54.357 | ETA: 1d6h | /input/path/roms/gameN/gameN.chd ...^C
# Scanning for ROMs ··············· | ████▒░░░░░░░░░░░░░░░ | 12.053/54.357 | ETA: 1d6h | /input/path/roms/gameN/gameN.chd ...
 

NOTICE: Exiting igir early
^C^C

```

Maybe I'm not fully understanding how scanning works, but CHDs still take up very long time, even if I'm using `--input-checksum-quick` and `--exclude-disks` flags.

### Describe the solution you'd like

Asking if it's possible to completely skip `.chd` files (from **INPUT** path(s)) by entirely discarding them from any reading operations.

Thanks 

### Additional context

Sometime I need to scan large collections and I'm perfectly sure I won't need CHDs at all.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `29ad915e1d88753533e27822d0278b5fca1e97cc`.  There
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
{"case_id": "emmercm_igir__1594__29ad915",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
