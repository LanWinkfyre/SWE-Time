# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
type-coupling spends ~27s scanning a generic ZodTypeAny export

## Problem

`health --type-aware --type-coupling` spends about 27 seconds in `symbol_scan` on a one-source-file project whose only export is a generic identity function constrained by `z.ZodTypeAny`. The result is complete and contains no coupling edges.

This dominates a real seven-source-file Data Model package scan (roughly 38 seconds total). Replacing the generic declaration with a non-generic `z.ZodTypeAny` parameter makes the minimal scan complete in about 0.25 seconds, but that narrows the valid public TypeScript API and is not an acceptable repository workaround.

Downstream investigation: https://github.com/speechmetrics/speechcatcher/issues/1561

## Minimal reproduction

### `package.json`

```json
{
  "name": "fallow-type-coupling-zod-repro",
  "private": true,
  "type": "module",
  "exports": {
    ".": {
      "fallow": "./src/index.ts",
      "types": "./src/index.ts",
      "default": "./src/index.ts"
    }
  },
  "dependencies": {
    "zod": "4.4.3"
  },
  "devDependencies": {
    "fallow": "3.16.0",
    "typescript": "7.0.2"
  }
}
```

### `.fallowrc.json`

```json
{
  "entry": ["src/index.ts"]
}
```

### `tsconfig.json`

```json
{
  "compilerOptions": {
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "skipLibCheck": true,
    "strict": true,
    "target": "ES2019"
  },
  "include": ["src"]
}
```

### `src/index.ts`

```ts
import { z } from "zod";

export const identitySchema = <T extends z.ZodTypeAny>(schema: T) => schema;
```

### Command

```sh
npm install
/usr/bin/time -p npx fallow health \
  --type-aware \
  --type-coupling \
  --type-aware-project tsconfig.json \
  --type-aware-require best-effort \
  --format json \
  --quiet \
  --no-cache
```

## Actual result

On macOS 26.5.2, Apple M3 Max (36 GB, arm64), Node 22.18.0:

- wall time: 27.43 s
- type-aware elapsed: 27.207 s
- `symbol_scan`: 27.170 s
- project setup: 0.033 s
- diagnostics: 0.002 s
- Fallow/sidecar: 3.16.0
- protocol: 6
- backend: TypeScript Go 7.0.2
- project source files analyzed for coupling: 1
- result: `complete`, `no-coupling-found`, 0 edges

Control: changing only the export to the following completed in 0.25 s wall time:

```ts
export const identitySchema = (schema: z.ZodTypeAny) => schema;
```

The control is not API-equivalent: it loses the generic identity return type.

The downstream package's exported `createTranslatableSchema = <T extends z.ZodTypeAny>(schema: T) => ...` took 27.52 s by itself. Every other source module used as the sole entry point completed in 0.15–0.28 s. This points to checker-type traversal of the generic `ZodTypeAny` constraint rather than repository size or the seven reported edges.

Fallow 3.15.0 shows the same behavior. A 5-run uncached / 5-run warmed downstream matrix found 3.15.0 wall medians of 37.91 / 37.83 s and 3.16.0 medians of 39.62 / 37.62 s, so the newer compatible version does not resolve it.

## Expected

A bounded public-signature scan should avoid recursively expanding an external generic constraint when it produces no project-local type edge, or otherwise cap/short-circuit that traversal. The one-file no-edge reproduction should complete near the non-generic control rather than taking tens of seconds.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `95a7ae9faf9e987616fe2366b74e99626dfd58c6`.  There
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
{"case_id": "fallow_rs_fallow__2269__95a7ae9",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
