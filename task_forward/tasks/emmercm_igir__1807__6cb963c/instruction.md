# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
Using "link" command does not work when "--patch" argument is supplied

### Paste the command

```sh
npx -y igir@latest \
    link \
    test \
    report \
    clean \
    -d "dats/" \
    -p "../archive/patches/" \
    -i "../archive/roms/" \
    --input-exclude "../archive/roms/no-intro/Nintendo - Game Boy Advance (e-Reader)/" \
    -i "../library/roms/" \
    -o "../library/roms/{romm}/" \
    --cache-path "./" \
    --no-bios \
    --merge-discs \
    --overwrite-invalid \
    --only-retail \
    --single \
    --prefer-language EN \
    --prefer-region USA,WORLD,EUR,JPN \
    --prefer-revision newer
```

### Describe the bug

Whenever I ran the above command, I found that it would get to step 3 "Scan each patch input path" of the internal operations. Then it would simply give up instead of processing the DATs. All scanned ROMs would become "UNUSED" in the report.

### Expected behavior

I can see two options:

1.
We add validation handling such that a "move" or "copy" command is required in order to perform any ROM patching. Which, to a degree, makes sense because you can't simply "link" the ROM when you are making alterations to it. It will have to be a copy.

2.
Whenever this unique combination of commands occurs, we'll need to default to "copying" the ROM and applying the patch to the copied ROM.

### Debug logs

```
PS Z:\roms\igir> .\igir-romm-1g1r-script.ps1

   @@@@@@   @@@@@@     @@@@@@    @@@@@@@@
 @@      @@  @@      @@      @@         @@
 @@      @@  @@      @@      @@         @@   ROM collection manager
   @@@@@@   @@         @@@@@@   @@@@@@@@@    https://igir.io/
          @@@     @@@@        @@@
     @@   @@        @@   @@   @@       @@    v4.1.2
     @@   @@        @@   @@   @@       @@
     @@   @@@@@@@@@@@@   @@   @@       @@


 ✓ Scanning for DATs » 705 DATs found

WARN: ..\archive\others\Nintendo Wii\FreeLoader for Nintendo Wii (USA) (Unl).rvz: failed to parse .rvz file:

 ✓ Scanning for ROMs » 71,223 files found
 ✓ Scanning for patches » 22 patches found
 ✓ Generating report » .\igir_2025-08-11T10;35;30.csv
```

I can run it again with -vvv if you aren't able to reproduce it.

### DAT(s) used

No-Intro PC DATs (downloaded on 7/29/25)

### igir version

4.1.2

### Node.js version

24.1.0

### Operating system

Tried both Ubuntu Linux and Windows

### Additional context

My collection does have several patch files, some of which apply to the same ROM. But all patch files are named differently.

I think for now, my only solution is going to be to run two different queries. One to handle all the linking, and then another to patch and copy the files. I assume if I do a "move" command with the same directory as both input and output (and then the patch file directory), all its going to do, is add the patched files without messing with the hard-links.

I think some command that is like "--patch-only" would also be helpful. This would indicate that I don't want it to copy any ROMs in their original form, I ONLY want it to use the original ROMs and then save the patched versions to the output directory.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `6cb963c0826cdc625fe4e62ca69c550060ce078c`.  There
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
{"case_id": "emmercm_igir__1807__6cb963c",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
