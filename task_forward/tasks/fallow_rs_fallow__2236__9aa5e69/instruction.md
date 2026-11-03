# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
type-aware sidecar requires typescript 7 but the root lockfile pins 6.0.3

# type-aware sidecar requires typescript 7 but the root lockfile pins 6.0.3

The sidecar and the repository root disagree about typescript, and the failure mode is seven red tests on any checkout that only ran the root install.

## The contradiction

- `tools/type-aware-sidecar/package.json` declares `typescript: 7.0.2`, and `src/semantic.mjs` imports `typescript/unstable/sync` (the TypeScript-Go API entry point).
- The root `package-lock.json` pins `typescript` at 6.0.3, which has no `unstable/sync` entry point.

Node module resolution walks upward, so on a checkout where only the root `npm ci` ran, the sidecar resolves the root copy and dies:

```
Error [ERR_MODULE_NOT_FOUND]: Cannot find module '<repo>/node_modules/typescript/unstable/sync'
imported from <repo>/tools/type-aware-sidecar/src/semantic.mjs
```

The CLI surfaces this as `Type-aware analysis failed: type-aware sidecar exited with status exit status: 1`, exit code 2.

## Impact

Seven tests across three targets fail on every such checkout:

- `-p fallow-cli --test audit_tests`: the three type-aware attribution tests
- `-p fallow-cli --test check_tests`: the three type-aware impact and refinement tests
- `-p fallow-cli --test schema_conformance`: `cli_json_documents_conform_to_output_schema`

The sidecar ships its own `package-lock.json`, so an install inside `tools/type-aware-sidecar` makes it self-sufficient, which is why CI and releases stay green while local runs fail. That split is exactly what makes the break easy to misread as an environment problem: it has been carried as a known local failure for over a week.

## Fix directions

- Bump the root `typescript` to 7 so both resolutions agree, or
- Anchor the sidecar's resolution to its own `node_modules` so the root copy is never a candidate, or
- Make the type-aware test harness perform the sidecar install it depends on and fail with a clear message when it is missing.

Any of the three beats the current state, where the failure names a module path instead of the version conflict that caused it.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `9aa5e697ccead870f7137a39a758feb470f1dc72`.  There
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
{"case_id": "fallow_rs_fallow__2236__9aa5e69",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
