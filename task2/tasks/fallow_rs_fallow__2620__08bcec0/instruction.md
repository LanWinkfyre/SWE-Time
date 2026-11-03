# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Istanbul statement coverage includes nested function bodies in the outer function

## Summary

Fallow 3.25.0 includes nested function statements in the outer function's Istanbul coverage. This lowers the outer function's coverage even when all of its own statements execute.

**Disclosure:** An LLM submitted this issue at a human user's request. The LLM ran the reproduction locally and inspected the raw counters and Fallow source.

## Reproduction

Use Node.js 24 in an empty directory:

```sh
npm init -y
npm install --save-dev fallow@3.25.0 istanbul-lib-instrument@6.0.3
```

Save `nested.js`:

```js
function outer() {
  return function inner(flag) {
    if (flag) return "yes";
    return "no";
  };
}

module.exports = { outer };
```

Save `collect.cjs`:

```js
const { readFileSync, writeFileSync } = require("node:fs");
const { resolve } = require("node:path");
const { runInNewContext } = require("node:vm");
const { createInstrumenter } = require("istanbul-lib-instrument");

const path = resolve("nested.js");
const source = readFileSync(path, "utf8");
const context = { module: { exports: {} } };
runInNewContext(createInstrumenter().instrumentSync(source, path), context);
context.module.exports.outer();
writeFileSync("coverage-final.json", JSON.stringify(context.__coverage__));
```

Run:

```sh
node collect.cjs
npx fallow health nested.js --complexity --coverage coverage-final.json --max-crap 1 --format json --no-cache
```

## Expected and actual results

The raw Istanbul counters record one call to `outer`, one execution of its return statement, and zero calls to `inner`.

| Function | Cyclomatic complexity | Expected coverage | Actual coverage | Expected CRAP | Actual CRAP |
|---|---:|---:|---:|---:|---:|
| `outer` | 1 | 100% | 25% | 1 | 1.4 |
| `inner` | 2 | 0% | 0% | 6 | 6 |

Fallow counts the outer return and three unexecuted inner statements together. This produces `1 / 4 = 25%` for the outer function.

Two controls confirm the attribution:

- With `inner` declared outside `outer`, the outer function receives 100% coverage.
- After both inner branches execute, both functions receive 100% coverage.

This reproduction uses plain JavaScript and Istanbul directly. It has no Vitest, TypeScript, framework transforms, or subprocess coverage merge.

## Source

[`compute_function_statement_coverage`](https://github.com/fallow-rs/fallow/blob/1ee9062b92e2b4a002844bf4f778917433901e1b/crates/engine/src/health/scoring.rs#L2081-L2120) counts every statement contained within the function body's range. It does not exclude nested bodies. The inspected function is identical in v3.25.0 and the linked commit.

The [curried-arrow test](https://github.com/fallow-rs/fallow/blob/1ee9062b92e2b4a002844bf4f778917433901e1b/crates/engine/src/health/scoring.rs#L7013-L7063) uses an empty statement map. It checks function matching, but does not test statement ownership.

The CRAP formula itself produces the expected results. The issue is the coverage input assigned to the outer function. Assigning each statement to its innermost containing function would keep the two coverage values independent.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `08bcec083b24159ad948f90c666744c39d76b120`.  There
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
{"case_id": "fallow_rs_fallow__2620__08bcec0",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
