# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
unused-class-members: local unexported options class does not credit members of its imported property types

## Summary

Follow-up to #1785 (fixed in #1787). One receiver shape from that investigation remains uncredited: an options object typed by a LOCAL, UNEXPORTED class whose property type is imported.

```ts
// dep.ts
export class ImportedDep {
  m(): void {}
}

// user.ts
import type { ImportedDep } from './dep';

class Opts {
  constructor(public c: ImportedDep) {}
}

export class User {
  constructor(private opts: Opts) {}
  run(): void {
    this.opts.c.m(); // ImportedDep.m still reports as unused-class-member
  }
}
```

This flagged before #1787 and still flags after it (verified with both binaries during the pre-ship review), so it is not a regression; the #1785 changelog entry scopes the fix to interface/type-alias hops.

## Mechanism

The #1787 typed-property-hop expansion deliberately returns `Opaque` for a compound rooted at a local class (`expand_typed_property_compound` in `crates/extract/src/visitor/mod.rs`), deferring to the `instance_bindings` machinery. That machinery resolves the chain root through `build_local_to_export_keys`, which covers imports and local EXPORTS; a non-exported local class never resolves, so the chain dead-ends and the imported property type's member is never credited.

Note the EXPORTED variant of the same shape (`export class Opts { ... }`) already credits via the #386/#388 typed instance chains, and the same-file variant (dep class local too) credits as well; only the unexported-local-class + imported-property-type combination is uncovered.

## Possible directions

- At extract time: when the compound's local-class root is unexported, consult the class's own typed-property map (its `instance_bindings` are already extracted per class) and continue the #1787 expansion through it, emitting the same `TypedPropertyMemberAccess` fact when a hop leaves the file.
- Or at analyze time: let the typed-instance chain resolution accept unexported local classes as roots (they are per-module data, no export needed).

Either direction keeps the false-negative-only invariant: crediting through a wrong resolution is gated by `export_is_class_with_members`.

Refs #1785.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `c196a300d6a420d9c2abe69df1f771b336942b7f`.  There
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
{"case_id": "fallow_rs_fallow__1788__c196a30",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
