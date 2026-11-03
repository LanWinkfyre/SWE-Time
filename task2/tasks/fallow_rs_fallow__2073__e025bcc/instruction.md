# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
React Native platform extensions (.ios.tsx/.android.tsx): base file reported as unused-file

## Summary

When a module has React Native platform-extension siblings (e.g. `UserMenu.tsx` + `UserMenu.ios.tsx`), fallow resolves `import { UserMenu } from "./UserMenu"` to the `.ios.tsx` variant only, and reports the base `.tsx` file as an unused file — even though Metro resolves the base file on every non-iOS platform (and it is the Android/default implementation).

## Repro

```
src/components/UserMenu.tsx        # Android/default implementation
src/components/UserMenu.ios.tsx    # iOS implementation
src/components/AppHeader.tsx       # import { UserMenu } from "./UserMenu"
```

`fallow dead-code` (3.10.0) reports:

```
● Unused files
  src/components/UserMenu.tsx
```

Expected: an import specifier that matches a platform-extension family should credit **all** platform variants (`.ios`, `.android`, `.native`, `.web`, and the base file), matching Metro's resolution semantics (https://reactnative.dev/docs/platform-specific-code#platform-specific-extensions).

## Environment

- fallow 3.10.0
- Expo SDK / React Native app (`react-native` plugin entry points detected)
- Observed on two independent component families in our repo (`UserMenu`, `segmented-tabs`); currently worked around with `// fallow-ignore-file unused-file`.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `e025bccb9edd184b0c3c3e586b8441eb8b31d880`.  There
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
{"case_id": "fallow_rs_fallow__2073__e025bcc",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
