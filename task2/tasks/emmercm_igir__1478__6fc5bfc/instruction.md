# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
Run on android (Termux)

### Is your feature request related to a problem?

When I try to run this tool on Android (Termux), I get the following:
```
╰─ ❯ npx igir@latest
Need to install the following packages:
igir@3.1.0
Ok to proceed? (y)

npm warn deprecated inflight@1.0.6: This module is not supported, and leaks memory. Do not use it. Check out lru-cache if you want a good and tested way to coalesce async requests by a key value, which is much more comprehensive and powerful.
npm warn deprecated lodash.isequal@4.5.0: This package is deprecated. Use require('node:util').isDeepStrictEqual instead.
npm warn deprecated glob@7.2.3: Glob versions prior to v9 are no longer supported
/data/data/com.termux/files/home/.npm/_npx/0d8028b15d717946/node_modules/node-disk-info/dist/index.js:73
            throw new Error("Platform not supported: " + platform);
                  ^

Error: Platform not supported: android
    at Object.getDiskInfoSync (/data/data/com.termux/files/home/.npm/_npx/0d8028b15d717946/node_modules/node-disk-info/dist/index.js:73:19)
    at file:///data/data/com.termux/files/home/.npm/_npx/0d8028b15d717946/node_modules/igir/dist/src/polyfill/fsPoly.js:463:30
    at ModuleJob.run (node:internal/modules/esm/module_job:272:25)
    at async onImport.tracePromise.__proto__ (node:internal/modules/esm/loader:583:26)
    at async asyncRunEntryPointWithESMLoader (node:internal/modules/run_main:98:5)

Node.js v23.8.0

```

### Describe the solution you'd like

It wolud be nice to be able to manage my roms directly from my andriod device.

### Additional context

_No response_
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `6fc5bfcd3f49646bfafaaab584ff0d0b908ce4e0`.  There
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
{"case_id": "emmercm_igir__1478__6fc5bfc",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
