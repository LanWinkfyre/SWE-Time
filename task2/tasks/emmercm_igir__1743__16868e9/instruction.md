# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
igir@4.0.2: TypeError in install.mjs and zstd-napi Build Failure

### Paste the command

npm install -g igir@4.0.2 --loglevel verbose
npm install -g igir@4.0.2 --ignore-scripts
npx igir@4.0.2 sort clean --dat ./nintendo-ds.dat --input ./Nintendo_DS_Complete_Romset --output ./Nintendo_DS_Sorted --input-include "*.nds" "*.ids" --input-exclude "*.gba" --threads 8 --single --prefer-region USA,EUR,CHN --prefer-language en --report ./igir_report.csv -v

### Describe the bug

`npm install -g igir@4.0.2` fails with `TypeError [ERR_INVALID_ARG_TYPE]: The "path" argument must be of type string. Received undefined` in `install.mjs:21`. `zstd-napi@0.0.12` build (`prebuild-install -r napi || node-gyp rebuild`) fails with `code: 1`. Using `--ignore-scripts` installs but `igir --version` fails with `Error: Cannot find module './build/Release/binding.node'` in `zstd-napi`. The script exits silently, even with `-v` or `-vvv`. `igir@3.4.2` installs and runs `igir --version` fine.

### Expected behavior

`npm install -g igir@4.0.2` should install, creating the `igir` executable. `igir --version` should show 4.0.2, and the script should sort ROMs with verbose output.

### Debug logs

Script with `-vvv` exits silently, producing no logs. Installation log (`~/.npm/_logs/2025-07-10T04_15_13_000Z-debug-0.log`):
```
npm info run igir@4.0.2 install node_modules/igir node install.mjs
npm info run zstd-napi@0.0.12 install node_modules/igir/node_modules/zstd-napi prebuild-install -r napi || node-gyp rebuild
npm info run igir@4.0.2 install { code: 1, signal: null }
npm info run zstd-napi@0.0.12 install { code: 1, signal: null }
npm verbose stack Error: command failed
...
npm error TypeError [ERR_INVALID_ARG_TYPE]: The "path" argument must be of type string. Received undefined
npm error     at new NodeError (node:internal/errors:405:5)
npm error     at validateString (node:internal/validators:162:11)
npm error     at Object.join (node:path:1189:7)
npm error     at file:///.../igir/install.mjs:21:28
...
npm error Node.js v18.20.8
```
For `igir --version` after `--ignore-scripts`:
```
Error: Cannot find module './build/Release/binding.node'
Require stack:
- ~/.nvm/versions/node/v18.20.8/lib/node_modules/igir/node_modules/zstd-napi/binding.js
...
  code: 'MODULE_NOT_FOUND'
```
[Attach `~/.npm/_logs/2025-07-10T04_15_13_000Z-debug-0.log`.]

### DAT(s) used

No-Intro Nintendo DS DAT (not yet verified due to silent script exit).

### igir version

4.0.2 (failed), 3.4.2 (working)

### Node.js version

v18.20.8

### Operating system

Ubuntu (jammy)

### Additional context

- Same errors in Docker (node:18).
- Installed `build-essential`, `python3`, `node-gyp`, but errors persist.
- No similar issues found on GitHub, Stack Overflow, or Reddit.
- `igir@3.4.2` works, suggesting v4.0.2-specific bug.
- No beta versions beyond 4.0.2 via `npm view igir versions`.
- Cleared npm cache and removed `igir` before reinstall.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `16868e95b83f9df7da435f1f9fceaf66879bdcb8`.  There
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
{"case_id": "emmercm_igir__1743__16868e9",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
