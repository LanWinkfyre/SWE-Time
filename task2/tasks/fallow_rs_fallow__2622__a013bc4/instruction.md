# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Built-in build/** ignore does not exclude nested build directories in monorepos

### What happened?

Fallow's built-in ignore patterns contain `build/**`, while similar generated-directory defaults such as `dist` and `coverage` are recursive (`**/dist/**`, `**/coverage/**`).

In a monorepo, this means nested build outputs such as:

```text
projects/project1/apps/web/build/**
projects/project2/apps/web/build/**
projects/project3/apps/web/build/**
```

are analyzed instead of ignored.

In my case these are generated SvelteKit build outputs and they produced a large number of false positives, including unused files, unused exports, unresolved imports, duplication findings, and health/complexity findings.

Adding this explicitly fixes the problem:

```jsonc
{
  "ignorePatterns": ["**/build/**"]
}
```

### Reproduction

Minimal structure:

```text
repo/
  package.json
  projects/
    app/
      build/
        index.js
```

Run Fallow from the repository root with no custom `ignorePatterns`.

Because the built-in pattern is:

```text
build/**
```

the nested file:

```text
projects/app/build/index.js
```

is still analyzed.

For example, my Fallow output included generated paths such as:

```text
projects/project1/apps/web/build/index.js
projects/project1/apps/web/build/server/chunks/...
projects/project2/apps/web/build/...
projects/project3/apps/web/build/...
```

### Expected behavior

I would expect the built-in build-directory exclusion to behave consistently with the other recursive generated-directory exclusions.

Would changing the built-in default from:

```text
build/**
```

to:

```text
**/build/**
```

make sense?

This would exclude `build` directories at any workspace depth and would make the default consistent with patterns such as:

```text
**/node_modules/**
**/dist/**
**/coverage/**
```

### Fallow version

```text
3.25.0
```

### Operating system

Windows 10

### Configuration

No custom build ignore was present when the issue occurred.

Adding:

```jsonc
{
  "ignorePatterns": ["**/build/**"]
}
```

removes the generated build output from the analysis.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `a013bc4285df07f9e706b1357de421222e9ebb4e`.  There
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
{"case_id": "fallow_rs_fallow__2622__a013bc4",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
