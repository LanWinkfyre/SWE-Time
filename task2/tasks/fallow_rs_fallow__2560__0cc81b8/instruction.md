# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
fallow reports destructed class members as unused

### What happened?

fallow reports `bar` as unused, while it is used in `console.log(bar)`. While reading `foo.bar` works. Using type-aware does not resolves the unused message.

The issue may be similar but was not resolved in-scope of #2549.

### Reproduction

To reproduce the issue:

```ts
class Foo {
  bar = 0
}

const foo = new Foo();
const { bar } = foo;

console.log(bar);
```


### Expected behavior

`bar` is not reported as unused.

### Fallow version

3.22.0 (or 3.23.0)

### Operating system

macOS

### Configuration

```toml

```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `0cc81b8761da239b721b3d70c3a26cc4db48d412`.  There
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
{"case_id": "fallow_rs_fallow__2560__0cc81b8",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
