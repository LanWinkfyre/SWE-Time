# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
igir fails to add symlinks if path to input is relative

### Paste the command

`npx igir@latest link --output links/ --symlink test --dat dat/*.dat --input testme/`

### Describe the bug

If you run the link command with symlink and provide the path to the input as a relative path, it outputs a warning when creating the link, and the link afterwards is broken/won't work. For comparison, `npx igir@latest link --output links/ --symlink test --dat dat/*.dat --input /home/bestest/try_igir/testme/` does work properly.

### Expected behavior

It's not a huge deal, so I understand if relative input paths aren't supported for symlinks, but at the very least a more accurate warning/failure message would be nice.

### Debug logs

Ignore the ZSTD errors, I see now that igir doesn't support that (yet?), just look at the `Team Apache (Germany)` zip that does work since it's using deflate

```
npx igir@latest link --output links/ --symlink test --dat dat/*.dat --input testme/
Need to install the following packages:
igir@3.3.0
Ok to proceed? (y) y

 ______   ______   ______  _______  
|      \ /      \ |      \|       \ 
 \$$$$$$|  $$$$$$\ \$$$$$$| $$$$$$$\
  | $$  | $$|    \  | $$  | $$    $$   ROM collection manager
  | $$  | $$|    \  | $$  | $$    $$   https://igir.io/
  | $$  | $$ \$$$$  | $$  | $$$$$$$\
 _| $$_ | $$__| $$ _| $$_ | $$  | $$   v3.3.0
|   $$ \ \$$    $$|   $$ \| $$  | $$
 \$$$$$$  \$$$$$$  \$$$$$$ \$$   \$$


✓ Scanning for DATs ··············· | 1 DAT found
ERROR: testme/Star Wars - Knights of the Old Republic II - The Sith Lords (USA) 
(Disc 1) (Play Disc).zst: failed to parse file: Zstandard isn't supported for 
.zip files
ERROR: testme/Ultimate Ride Coaster Deluxe (USA, Canada) 
(En,Fr,De,Es,It,Nl,Pt,Sv,No,Da,Fi).zst: failed to parse file: Zstandard isn't 
supported for .zip files
✓ Scanning for ROMs ··············· | 2 files found
WARN:  IBM - PC compatible: Team Apache (Germany) links/Team Apache 
(Germany).zip: written link has the target path 'testme/Team Apache 
(Germany).zip' which doesn't exist, retrying
ERROR: IBM - PC compatible: Team Apache (Germany): links/Team Apache 
(Germany).zip: failed to link from testme/Team Apache (Germany).zip: EEXIST: 
file already exists, symlink 'testme/Team Apache (Germany).zip' -> 'links/Team 
Apache (Germany).zip'
ERROR: IBM - PC compatible: Team Apache (Germany): links/Team Apache 
(Germany).zip: failed to link from testme/Team Apache (Germany).zip: EEXIST: 
file already exists, symlink 'testme/Team Apache (Germany).zip' -> 'links/Team 
Apache (Germany).zip'
✓ IBM - PC compatible ············· | 1/51,567 games, ...
```

### DAT(s) used

https://redump.info/datfile/pc/

### igir version

igir@3.3.0

### Node.js version

v18.19.1

### Operating system

Linux Mint 22

### Additional context

_No response_
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `9d4fa5a5c2daac0ed9fbb26199270d47315bbb51`.  There
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
{"case_id": "emmercm_igir__1537__9d4fa5a",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
