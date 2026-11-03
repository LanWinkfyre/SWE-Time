# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
False positive: `unlisted-dependencies` reports a TypeScript `paths` alias as an npm package

### What happened?

Running:

```bash
npx fallow dead-code
```

reports:

```text
● Unlisted dependencies (1)
  @acme/internal
```

The JSON output from:

```bash
npx fallow dead-code --format json --unlisted-deps --unresolved-imports --explain
```

contains:

```json
{
  "unlisted_dependencies": [
    {
      "package_name": "@acme/internal",
      "imported_from": [
        { "path": "src/internal/feature-a/clients/base-client.ts", "line": 3, "col": 1 },
        { "path": "src/internal/feature-a/clients/derived-client.ts", "line": 1, "col": 9 },
        { "path": "src/internal/feature-a/services/base-service.ts", "line": 1, "col": 9 },
        { "path": "src/internal/feature-b/clients/lookup-client.ts", "line": 2, "col": 1 },
        { "path": "tests/fixtures/internal-api/service-factory.ts", "line": 3, "col": 9 }
      ]
    }
  ]
}
```

And:

```bash
npx fallow dead-code --trace-dependency @acme/internal
```

prints:

```text
USED @acme/internal (18 import(s))
```

with internal source files listed as importers.

That strongly suggests `fallow` is classifying the scoped alias prefix `@acme/internal` as a package name instead of recognizing the full import specifier as an internal path resolved by `tsconfig.json`.

### Reproduction

These steps use synthetic names, but they describe the project shape that reproduces the issue.

1. Create a TypeScript project with a `tsconfig.json` path alias mapping a scoped prefix into local source files:

```json
{
  "compilerOptions": {
    "paths": {
      "@acme/*": ["./src/*"]
    }
  }
}
```

2. Create internal source files under a structure such as:

```text
src/
  internal/
    common/
      request-context.ts
    feature-a/
      clients/
        base-client.ts
      services/
        base-service.ts
```

3. Import those files through the alias from multiple places, for example:

```ts
import { RequestContext } from "@acme/internal/common/request-context";
```

4. Add at least one additional internal import chain so the alias prefix is used across several files.

5. Run:

```bash
npx fallow dead-code
```

6. Observe that `fallow` reports:

```text
● Unlisted dependencies (1)
  @acme/internal
```

7. Confirm the classification with:

```bash
npx fallow dead-code --trace-dependency @acme/internal
npx fallow dead-code --format json --unlisted-deps --unresolved-imports --explain
```

8. Observe that `fallow` treats `@acme/internal` as a dependency name and lists internal source files as importers.

I have verified this behavior in the affected project shape above. I have not yet reduced it to a tiny standalone reproduction that triggers the same result.

### Expected behavior

mports that match a configured TypeScript `paths` alias should not produce an `unlisted dependency` finding.

If the import resolves to a source file inside the workspace, it should be treated purely as an internal module edge.

## Why this looks like a bug rather than a config problem

From the docs:

- `unlisted-dependencies` is described as: "Packages imported in source code but not declared in package.json."
- `unresolved-imports` is the rule that covers broken or unresolvable import specifiers.
- The documented config workaround is `ignoreDependencies`, but that suppresses a package-level dependency finding; it does not tell `fallow` that a prefix is a `tsconfig` path alias.

In other words, I could suppress this with:

```json
{
  "ignoreDependencies": ["@acme/internal"]
}
```

but that looks like a workaround for a false positive, not a real fix.

## Additional context

This project also has genuine unresolved imports for a different specifier:

```text
@acme/internal/files/missing-helper
```

However, the `@acme/internal` `unlisted dependency` finding does not appear to be limited to that one missing import.

`--trace-dependency @acme/internal` reports 18 import sites across otherwise valid internal alias imports, including files like:

- `src/internal/feature-a/clients/base-client.ts`
- `src/internal/feature-a/clients/derived-client.ts`
- `src/internal/feature-a/services/base-service.ts`
- `src/internal/feature-b/clients/lookup-client.ts`
- `src/internal/feature-c/services/query-service.ts`

So the behavior looks broader than a single unresolved-import side effect.

## Representative project shape

The internal alias pattern looks like this:

### `tsconfig.json`

```json
{
  "compilerOptions": {
    "paths": {
      "@acme/*": ["./src/*"]
    }
  }
}
```

### internal file layout

```text
src/
  internal/
    common/
      request-context.ts
    feature-a/
      clients/
        base-client.ts
```

### internal import

```ts
import {
  RequestContext,
  RequestOptions,
} from "@acme/internal/common/request-context";
```

There is no published or installed package named `@acme/internal` in this workspace.

### Fallow version

3.6.0

### Operating system

Windows

### Configuration

```toml

```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `124ad5cc84484f890cfd728240d6688d3b68df4d`.  There
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
{"case_id": "fallow_rs_fallow__1911__124ad5c",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
