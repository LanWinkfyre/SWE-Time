# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Module augmentation interfaces are reported as unused types

### What happened?

`fallow dead-code` reports an interface declared inside a valid TypeScript
module augmentation as an unused exported type. Removing the interface would
remove the augmentation and change the augmented library contract.

The type-aware companion also retains the finding as
`confirmed-no-static-references`, although TypeScript successfully applies the
augmentation to the imported `Theme` type.

### Reproduction

`.fallowrc.jsonc`:

```jsonc
{
  "entry": ["src/index.ts"]
}
```

`src/library.ts`:

```ts
export interface Theme {}
```

`src/theme-augmentation.ts`:

```ts
type AppTheme = {
  brand: string;
};

declare module './library' {
  export interface Theme extends AppTheme {}
}

export {};
```

`src/index.ts`:

```ts
import './theme-augmentation';
import type { Theme } from './library';

export const readBrand = (theme: Theme) => theme.brand;
```

`tsc -p tsconfig.json --noEmit` succeeds and proves `Theme.brand` is supplied
by the augmentation.

Run:

```bash
fallow dead-code --unused-exports --unused-types --format json --quiet
```

The result reports the augmented `Theme` interface in
`src/theme-augmentation.ts` as `unused-type`.

The same finding remains with:

```bash
fallow dead-code \
  --unused-exports \
  --unused-types \
  --type-aware \
  --type-aware-project tsconfig.json \
  --type-aware-require best-effort \
  --format json \
  --quiet
```

### Expected behavior

Interfaces that participate in a TypeScript module augmentation should not be
reported as unused exported types when the augmented module is reachable.

### Fallow version

3.16.0

### Operating system

macOS
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `38fc8704b030bd6e21a67088b8f064af1ff712ed`.  There
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
{"case_id": "fallow_rs_fallow__2349__38fc870",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
