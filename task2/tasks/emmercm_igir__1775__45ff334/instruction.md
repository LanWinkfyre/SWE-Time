# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
In Windows 11 x64, when i execute igir.exe, no problem with igir v4.1.0, but with v4.1.1...

### Paste the command

igir.exe

### Describe the bug

node:internal/modules/cjs/loader:1850
  return process.dlopen(module, path.toNamespacedPath(filename));
                 ^

Error: error: 14001\\?\C:\Users\RoBeRt\AppData\Local\Temp\caxa\applications\igir\bpjzc4xh9v\0\dist\prebuilds\win32-x64\node.node
    at Object..node (node:internal/modules/cjs/loader:1850:18)
    at Module.load (node:internal/modules/cjs/loader:1427:32)
    at Module._load (node:internal/modules/cjs/loader:1250:12)
    at TracingChannel.traceSync (node:diagnostics_channel:322:14)
    at wrapModuleLoad (node:internal/modules/cjs/loader:235:24)
    at Module.require (node:internal/modules/cjs/loader:1449:12)
    at require (node:internal/modules/helpers:135:16)
    at load (C:\Users\RoBeRt\AppData\Local\Temp\caxa\applications\igir\bpjzc4xh9v\0\node_modules\node-gyp-build\node-gyp-build.js:22:10)
    at file:///C:/Users/RoBeRt/AppData/Local/Temp/caxa/applications/igir/bpjzc4xh9v/0/dist/bundle.js:7852:13
    at ModuleJob.run (node:internal/modules/esm/module_job:370:25) {
  code: 'ERR_DLOPEN_FAILED'
}

Node.js v24.4.0

Thanks

### Expected behavior

Normal run, help screen.

### Debug logs

node:internal/modules/cjs/loader:1850
  return process.dlopen(module, path.toNamespacedPath(filename));
                 ^

Error: error: 14001\\?\C:\Users\RoBeRt\AppData\Local\Temp\caxa\applications\igir\bpjzc4xh9v\0\dist\prebuilds\win32-x64\node.node
    at Object..node (node:internal/modules/cjs/loader:1850:18)
    at Module.load (node:internal/modules/cjs/loader:1427:32)
    at Module._load (node:internal/modules/cjs/loader:1250:12)
    at TracingChannel.traceSync (node:diagnostics_channel:322:14)
    at wrapModuleLoad (node:internal/modules/cjs/loader:235:24)
    at Module.require (node:internal/modules/cjs/loader:1449:12)
    at require (node:internal/modules/helpers:135:16)
    at load (C:\Users\RoBeRt\AppData\Local\Temp\caxa\applications\igir\bpjzc4xh9v\0\node_modules\node-gyp-build\node-gyp-build.js:22:10)
    at file:///C:/Users/RoBeRt/AppData/Local/Temp/caxa/applications/igir/bpjzc4xh9v/0/dist/bundle.js:7852:13
    at ModuleJob.run (node:internal/modules/esm/module_job:370:25) {
  code: 'ERR_DLOPEN_FAILED'
}

Node.js v24.4.0

Thanks

### DAT(s) used

None

### igir version

4.1.1

### Node.js version

24.4.0

### Operating system

Windows 11 x64

### Additional context

_No response_
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `45ff33457b69ec93367e4363d945bc7972616bd4`.  There
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
{"case_id": "emmercm_igir__1775__45ff334",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
