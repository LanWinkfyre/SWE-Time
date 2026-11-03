# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
unlisted-dependency false positive: Jest moduleNameMapper target path parsed as package name (@scope/__mocks__)

### What happened?

`fallow audit` reports a `fallow/unlisted-dependency` finding (severity: major) for a package named `@bacons/__mocks__` — a package that does not exist and is never imported anywhere. The real import is `@bacons/apple-targets`, which **is** listed in `package.json` dependencies.

The phantom name appears to be constructed from the Jest `moduleNameMapper` target path: the mapping routes the module to a local mock file under `__mocks__/@bacons/`, and the resolver seems to re-derive a "package name" from that file path, combining the `@bacons` scope directory with its parent `__mocks__` directory.

Reported finding:

```
fallow/unlisted-dependency  src/features/widgets/utils/__tests__/widget-storage.util.test.ts:14
  Package '@bacons/__mocks__' is imported but not listed in package.json
```

Since the finding is major, with `--gate new-only` + `fail-on-issues` it blocks CI on any PR touching a test file that uses such a mapping. Current workaround: `"ignoreDependencies": ["@bacons/__mocks__"]` in `.fallowrc.json`.

### Reproduction

1. In `package.json`, list a scoped dependency and map it to a local mock via Jest config:

```jsonc
{
  "dependencies": { "@bacons/apple-targets": "^5.0.0" },
  "jest": {
    "moduleNameMapper": {
      "^@bacons/apple-targets$": "<rootDir>/__mocks__/@bacons/apple-targets.ts"
    }
  }
}
```

2. Create the mock file `__mocks__/@bacons/apple-targets.ts`.
3. Create a test file importing the real package name:

```ts
import { ExtensionStorage } from '@bacons/apple-targets';
jest.mock('@bacons/apple-targets');
```

4. Run `fallow audit`.
5. A `fallow/unlisted-dependency` finding is reported for the non-existent package `@bacons/__mocks__`.

### Expected behavior

The import `@bacons/apple-targets` resolves against `package.json` dependencies (where it is listed). If the `moduleNameMapper` rewrite is followed, the local `.ts` target should be treated as a project file, not re-interpreted as an external package name.

### Fallow version

3.14.0 (reproduced both via the `fallow-rs/fallow@v3` GitHub Action on Linux and with the local CLI on macOS)

### Operating system

Linux (CI) and macOS (local)

### Configuration

No `fallow.toml` — the project uses `.fallowrc.json` (entry globs, ignorePatterns, ignoreDependencies; no rule overrides relevant to dependency resolution). Happy to share the full file or `fallow-results.json` from the failing run if useful.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `73bb630b9510462e3139b3a65ba0179999380752`.  There
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
{"case_id": "fallow_rs_fallow__2213__73bb630",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
