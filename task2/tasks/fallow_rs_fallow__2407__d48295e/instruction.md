# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
React Native platform extensions: the #2073 fix surfaces the same family as "duplicate exports"

## Summary

Follow-up to #2073, same root cause in a different check.

#2073 taught the **resolver** about Metro platform families, and that half works perfectly — thank you. But now that both variants are considered reachable, `duplicate-exports` flags the pair, because a platform family necessarily exports the same name from every variant. That is not ambiguity; it is the whole mechanism.

Net effect for us: `fallow dead-code` still exits 1 on the same two component families, so the bump trades one false positive for another and we are still holding at 3.10.0.

## Repro

```
src/components/UserMenu.tsx        # Android/default implementation
src/components/UserMenu.ios.tsx    # iOS implementation
src/components/AppHeader.tsx       # import { UserMenu } from "./UserMenu"
```

`fallow dead-code -w myhr` (3.11.0 **and** 3.17.0, `react-native` plugin active):

```
● Duplicate exports (2)
  apps/myhr/src/components/dashboard/segmented-tabs.ios.tsx
    ↔ segmented-tabs.tsx (1 export)
    SegmentedTabs

  apps/myhr/src/components/UserMenu.ios.tsx
    ↔ UserMenu.tsx (1 export)
    UserMenu

✗ 2 duplicate pairs
```

Before #2073 this did not fire, because the base file was reported as an unused file instead — so the two findings were mutually exclusive and fixing the first exposed the second.

## Expected

When two files are members of the same Metro platform family (identical path modulo a `.ios` / `.android` / `.native` / `.web` extension), exporting the same name is the required pattern, not a duplicate. Metro resolves exactly one per platform, so a barrel cannot resolve ambiguously. `duplicate-exports` should skip pairs inside a platform family under the `react-native` / `expo` plugin — the same family relation #2073 already computes for the resolver.

Genuine duplicates — the same export name in two unrelated files — should keep firing.

## Environment

- fallow 3.11.0 and 3.17.0 (identical output)
- Expo SDK 57 / React Native 0.86, `react-native` plugin entry points detected
- The same two families as #2073 (`UserMenu`, `segmented-tabs`); the `// fallow-ignore-file unused-file` workarounds were removed as your note said, and `dead-code` then failed on this instead.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `d48295e8b320685985c750442a490b7884cd1139`.  There
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
{"case_id": "fallow_rs_fallow__2407__d48295e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
