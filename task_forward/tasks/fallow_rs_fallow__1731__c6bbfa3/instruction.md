# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Ignore unit-size for describe()-like functions.

### Problem

Fallow 2.104.0 reports lots of "function too big" for test suites. This is to be expected since those contain hundreds of lines with individual tests.

### Proposed solution

Add a config option with a file pattern and a function name to ignore:

```
"ignoreSizeOfTestSuites": [
    { "files": "**/*.test.*", "name": "describe" ]
]
```

A more generic solution would be to list file names, the function name and whether to ignore the definition, the call sites or both.

### Alternatives considered

There is currently no way to configure the unit-size at which Fallow reports a function for being too long. The only "fix" I found by looking through the output of `fallow config-schema` is to disable health checks for tests which means I also miss test code that is too complex.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `c6bbfa3d6697269811e1e9d942e0d212832931a1`.  There
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
{"case_id": "fallow_rs_fallow__1731__c6bbfa3",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
