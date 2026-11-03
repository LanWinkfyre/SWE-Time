# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Class member usage is not detected through object properties

### What happened?

Fallow reports a class property as unused when the class instance is stored in an object property:

```ts
import { Foo } from './foo'

const foo = { property: new Foo() }

console.log(foo.property.bar)
```

```ts
export class Foo {
  public bar = 'bar' // Unused class members (1)
}
```

### Reproduction

https://github.com/Ericlm/fallow-vue-class-unused

### Expected behavior

The property should not be reported as unused.

### Fallow version

3.22.0

### Operating system

macOS

### Configuration

```toml

```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `541e048480866080382f3401a899f3338b947f92`.  There
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
{"case_id": "fallow_rs_fallow__2546__541e048",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
