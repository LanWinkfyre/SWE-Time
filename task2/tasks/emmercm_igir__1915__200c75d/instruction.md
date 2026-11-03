# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
{Romm} outputs Sega Genesis/Mega Drive games in incorrect format

### Paste the command

```
set -ou pipefail
cd "$(dirname "${0}")"

INPUT_DIR=roms-unverified
OUTPUT_DIR=roms-verified

time npx -y igir@latest \
  move \
  extract \
  report \
  test \
  -d dats/ \
  -i "${INPUT_DIR}/" \
  -o "${OUTPUT_DIR}/{romm}/" \
  --input-checksum-quick false \
  --input-checksum-min CRC32 \
  --input-checksum-max SHA256 \
  --no-demo \
  --no-beta \
  --no-sample \
  --no-prototype \
  --no-program \
  --no-homebrew \
  --no-bad \
  --only-retail \
  --single \
  --prefer-language EN \
  --prefer-region USA,WORLD,EUR,JPN \
  --prefer-revision newer
```

### Describe the bug

When using the {romm} output option, Sega Genesis/Mega Drive games will be sorted into a directory named "genesis-slash-megadrive". This would require a platform binding in Romm, since Romm wants a directory named "genesis" for this platform by default.
https://docs.romm.app/latest/Platforms-and-Players/Supported-Platforms/

### Expected behavior

Relevant games will be sorted into Romm-specific default directories.

### Debug logs

```
INFO:     [RomM][scan][2025-11-19 21:53:48] Found 1 platforms in the file system
WARNING:  [RomM][scan][2025-11-19 21:53:48] Platform genesis-slash-megadrive not identified ❌
```

### DAT(s) used

_No response_

### igir version

v4.2.0

### Node.js version

v20.11.0

### Operating system

Ubuntu 24.04.3 LTS

### Additional context

Not a big deal, just needs the directory name changed to make Romm happy.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `200c75dcf5f29518560eae83ae3933663882e37b`.  There
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
{"case_id": "emmercm_igir__1915__200c75d",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
