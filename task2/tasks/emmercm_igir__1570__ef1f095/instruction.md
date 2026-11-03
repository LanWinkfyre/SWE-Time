# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
"multiple games writing to the same output path" without an apparent reason

### Paste the command

igir move zip test clean report --dat ~/Tools/Storage/Igir/dat/aftermarket/*.dat --input ~/Tools/Testing/Aftermarket --input ~/Tools/Storage/Igir/newroms --output ~/Tools/Testing/Aftermarket/{es} --clean-backup ~/Tools/Storage/Igir/backup --report-output ~/Tools/Storage/Igir/log/igir-aftermarket-%YYYY-%MM-%DD-%HH-%mm-%ss.csv --overwrite-invalid

### Describe the bug

I get this error message:
```
ERROR: Microsoft - MSX2 (Aftermarket): multiple games writing to the same output path: 
/home/matthias/Tools/Testing/Aftermarket/msx2/Sword of Ianna, The (World) (En,Es) (v1.2)
 (Aftermarket) (Unl).zip
ERROR:   Sword of Ianna, The (World) (En,Es) (v1.2) (Aftermarket) (Unl)
ERROR:   Sword of Ianna, The (World) (En,Es) (v1.2) (Aftermarket) (Unl)
ERROR:   Sword of Ianna, The (World) (En,Es) (v1.2) (Aftermarket) (Unl)
ERROR:   Sword of Ianna, The (World) (En,Es) (v1.2) (Aftermarket) (Unl)

```

The rom dump (one file, there are no duplicates present) also does not get moved or renamed.

### Expected behavior

Moving / renaming / zipping this rom dump should work as well as all other dumps work. igir should also be able to handle duplicates.

### Debug logs

[vvv.txt](https://github.com/user-attachments/files/19959697/vvv.txt)

### DAT(s) used

Atari - Atari 7800 (A78) (Aftermarket) (20250416-124715).dat

### igir version

3.4.2

### Node.js version

18.19.1

### Operating system

Linux Mint 22.1 Cinnamon

### Additional context

As this game ("Sword of Ianna") is freeware, I oculd alsp provide the files if needed.
https://retroworks.itch.io/the-sword-of-ianna-msx2
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `ef1f095c61fe385041591a7e9369a466f323f1f8`.  There
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
{"case_id": "emmercm_igir__1570__ef1f095",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
