# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Add CSS Modules class reachability for styling findings

## Problem

CSS Modules are partially covered today: fallow extracts `.module.css` and `.module.scss` exports and includes CSS analytics. The next level is module-aware reachability for class usage and dead-surface findings.

Without that, CSS Modules get useful local analysis but not the same confidence as TypeScript exports: imported `styles.foo` usage, destructuring, namespace forwarding, and dynamic access are not yet treated as a first-class reachability graph.

## Proposed direction

Add CSS Modules class reachability:

- Treat CSS Module class exports like a small symbol table.
- Credit `styles.foo`, `styles["foo"]`, destructured usage, and common `clsx/cn` forwarding patterns.
- Abstain or lower confidence on dynamic indexed access.
- Surface unused CSS Module classes as `css-dead-surface` only when usage evidence is strong.
- Keep the existing CSS analytics and duplicate/selector signals unchanged.

## Acceptance criteria

- `.module.css` and `.module.scss` fixtures report unused classes only when no static consumer exists.
- Dynamic module access does not create false positives.
- JSON actions are verify-first unless the usage graph is strong enough.
- Audit deep mode narrows CSS Module dead-surface findings to changed anchors.
- Add public smoke coverage for a CSS Modules-heavy repo.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `2c67798f2629db09e82117ce345130c1c822bf6d`.  There
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
{"case_id": "fallow_rs_fallow__1724__2c67798",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
