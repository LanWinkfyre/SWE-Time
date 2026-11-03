# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Namespace passed whole as a JSX attribute, call argument, alias, or initializer is not a whole-object use in .ts/.tsx

A namespace import that is used through one dotted access and also handed over whole narrows to the dotted members only, because the visitor records whole-object uses solely for `Object.keys/values/entries/getOwnPropertyNames(ns)`, spread, `for...in`, computed non-string access, rest destructuring, and a few type positions. Every other bare reference (call argument, JSX attribute expression, alias, array or object literal element, variable initializer, assignment right-hand side, return value) is ignored, so the siblings the callee can reach are reported as unused.

## Reproduction

`package.json` main `src/index.ts` re-exporting both consumers; `whole-icons.ts` and `arg-icons.ts` each export `Star` and `Moon`.

```tsx
// src/whole.tsx
import * as Icons from './whole-icons';
import { Callout } from './Callout';
export const Whole = () => (<div><Icons.Star /><Callout icons={Icons} /></div>);
```

```ts
// src/arg.ts
import * as Icons from './arg-icons';
const register = (all: Record<string, unknown>): number => Object.keys(all).length;
export const useArg = (): number => { Icons.Star(); return register(Icons); };
```

`fallow dead-code --no-cache --format json` reports `src/arg-icons.ts:Moon` and `src/whole-icons.ts:Moon`. Both `Moon` exports are reachable through the whole-object pass.

Two more shapes with the same root cause: an alias (`const N = NS; <NS.Star />{N.Moon()}`) and a statement initializer (`export const all = NS;` next to `<NS.Star />`) both report every sibling that is not accessed through `NS.` directly.

Pre-existing since the #2348 narrowing widening. Since #2360 the Astro and MDX pipelines cover these shapes with their whole-file completeness guard (frontmatter, statement lines, templates), so only `.ts` / `.tsx` consumers are affected.

## Suggested shape

Treat an identifier reference to a namespace import that is not the object of a static member expression or the root of a JSX member tag as a whole-object use in `crates/extract/src/visitor/visit_impl.rs` (strictly conservative: over-credit, never a false finding), or track the alias binding. This touches every TS/TSX consumer, so it needs its own fixture, a cache bump, and a real-project run before and after.

Surfaced while reviewing #2360 (the fix for #2355).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `28b7be16fd895a1d937922b2ead2a77ad552aab2`.  There
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
{"case_id": "fallow_rs_fallow__2377__28b7be1",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
