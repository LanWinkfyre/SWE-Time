# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
Igir doesn't appear to take advantage of multithreading, even with writer, reader, and dat threads increased

### Paste the command

npx igir@latest copy zip --zip-format torrentzip --dat ../first/IBM\ -\ PC\ compatible\ -\ Datfile\ \(55129\)\ \(2025-10-11\ 22-16-16\).dat --input Bestest/ --input ../first/IBM\ -\ PC\ compatible\ -\ Cuesheets\ \(45285\)\ \(2025-10-11\ 22-16-16\)/ --output ROMS-sorted/ --writer-threads 30 --reader-threads 30 --dat-threads 30 --cache-path ../igir_cache/igir.cache

### Describe the bug

Despite setting writer, reader, and dat threads to 30, I never see more than one of my computer's threads peak in usage, even when there are several large ROMs that igir has still yet to read, write, or hash.

### Expected behavior

I expected igir to use the number of threads I gave it in the commandline flags, using one thread per rom.

### Debug logs

[logs.txt](https://github.com/user-attachments/files/22886631/logs.txt)

### DAT(s) used

https://redump.info/datfile/pc/

### igir version

v4.2.0

### Node.js version

v22.19.0

### Operating system

endeavourOS rolling

### Additional context

If screenshots of thread utilization while several large roms are remaining is needed:
<img width="1577" height="438" alt="Image" src="https://github.com/user-attachments/assets/641c949b-ff86-435d-ace5-8fefea7ca478" />
<img width="1570" height="399" alt="Image" src="https://github.com/user-attachments/assets/6e4d0a98-20db-4a02-8a33-597a10d119ee" />
<img width="881" height="149" alt="Image" src="https://github.com/user-attachments/assets/6decaf2b-4e21-4d7e-8b4a-6fa828b33480" />
While the above screenshot is the hashing/writing step, the same issues with utilization occur during the reading step; there's always a baked in minute or two for it to re-scan all the cues, but after it's done that, it seems to go one-by-one through the remaining bin/iso files.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `0a424002fbd80493ffa871ce28428abda5098917`.  There
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
{"case_id": "emmercm_igir__1896__0a42400",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
