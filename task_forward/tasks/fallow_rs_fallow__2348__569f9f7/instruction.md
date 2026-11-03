# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Syntactic dead-code scan misses JSX namespace member usage

### What happened?

`fallow dead-code` reports an exported JSX component as unused when it is
rendered through a direct namespace import such as `<SC.UsedStyle />`.

Ordinary JavaScript property access through the same namespace is recognized.
The problem is specific to JSX member expressions. The type-aware companion
also recognizes the JSX use and removes the false positive.

This is adjacent to #324, but that issue covered `export * as Namespace`
re-exports. This reproduction uses a direct `import * as SC`.

### Reproduction

`.fallowrc.jsonc`:

```jsonc
{
  "entry": ["src/component.tsx"]
}
```

`src/style.ts`:

```ts
export const UsedStyle = () => null;

export const ActuallyUnusedStyle = () => null;
```

`src/component.tsx`:

```tsx
import * as SC from './style';

export const RenderedStyle = () => <SC.UsedStyle />;
```

`tsconfig.json` includes `src` and sets `jsx` to `preserve`.

Run:

```bash
fallow dead-code --unused-exports --unused-types --format json --quiet
```

The syntactic result reports both `UsedStyle` and `ActuallyUnusedStyle`.

Then run:

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

The type-aware result correctly reports only `ActuallyUnusedStyle` and records
`UsedStyle` as `confirmed-used` through a `property-access` reference in the
TSX file.

### Expected behavior

The normal dead-code scan should recognize `<SC.UsedStyle />` as usage of the
`UsedStyle` export and report only `ActuallyUnusedStyle`.

### Fallow version

3.16.0

### Operating system

macOS
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `569f9f7136c3b037972ec4b48b8deeb1c5bc1e96`.  There
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
{"case_id": "fallow_rs_fallow__2348__569f9f7",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
