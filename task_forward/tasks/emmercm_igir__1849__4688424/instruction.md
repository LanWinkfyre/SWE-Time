# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
--prefer-rom-regex not working in some cases

### Paste the command

npx --yes igir@latest move zip test clean report \
  --dat "${BASE_PATH}/DATs/Redump/*.dat" \
  --input "${REDUMP}" \
  --input "${INPUT}" \
  `# Trust checksums in archive headers, don't checksum archives (we only care about the contents)` \
  --input-checksum-max CRC32 \
  --input-checksum-archives never \
  --output "${REDUMP}" \
  --dir-dat-name \
  --overwrite-invalid \
  --only-retail \
  --merge-discs \
  --zip-exclude "*.{chd,iso,rvz}" \
  --single \
  --prefer-language EN \
  --prefer-region USA,WORLD,EUR,JPN \
  --prefer-revision newer \
  --prefer-rom-regex "rvz$" \
  -v

### Describe the bug

I just ran into an issue where I have my --prefer-rom-regex set to `"rvz$"`. 

I currently have in my output directory "<Some Rom>.iso" and in my input directory I have "<Some Rom>.rvz". 

If I run igir in this case I would expect the .iso to be replaced by the .rvz as it matches the preferred format. However in practice the `.iso` file stays in the output and the .rsv file stays in the input.

If I remove the .iso file from the output directory the .rsv file is correctly pulled in, so this tells me that igir is detecting it as a valid rom.

### Expected behavior

when --prefer-rom-regex is set, roms matching that pattern will replace roms that don't as long as they are both the same title.

### Debug logs

[sync-20250828-002018.log](https://github.com/user-attachments/files/22019438/sync-20250828-002018.log)

### DAT(s) used

Redump

### igir version

v4.2.0

### Node.js version

v22.11.0

### Operating system

MacOS 15.6.1

### Additional context

_No response_
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `4688424483a335fb53e550bc400472139d06e62c`.  There
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
{"case_id": "emmercm_igir__1849__4688424",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
