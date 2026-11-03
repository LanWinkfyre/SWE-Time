# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
import X = require('./x') is not recorded as an import edge, so the target file is reported as an unused file

`import X = require('./x')` (a `TSImportEqualsDeclaration` with an external module reference) is not recorded as an import edge. The target file is reported as an unused file, and nothing imported through `X` is credited.

## Reproduction

`package.json` with `"main": "src/index.ts"`:

```ts
// src/assigned.ts
namespace Assigned {
  export const viaAssignment = 1;
}
export = Assigned;

// src/index.ts (entry)
import Assigned = require('./assigned');
console.log(Assigned.viaAssignment);
```

`fallow dead-code --format json --quiet --no-cache` reports `src/assigned.ts` as an unused file.

Control: replacing the consumer line with `import Assigned from './assigned';` makes the file reachable, so the gap is specific to the import-equals form. Reproduced on the pre-#2356 binary as well, so it is pre-existing and unrelated to the local-namespace fix.

## Where

`crates/extract/src/visitor/` has no arm for `TSImportEqualsDeclaration` with an external module reference; only `visit_impl_structural.rs` sees the node, for scope shadowing. No `ImportInfo` or require edge is produced.

## Expected

`import X = require('spec')` records an import of `spec` through the CommonJS mechanism with local binding `X`, the target participates in reachability, and member accesses through `X` narrow the same way they do for a namespace import. `import X = Some.Namespace` (an entity-name reference, not a module) stays out of scope.

Surfaced while reviewing #2364 (the fix for #2356).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `f951395d7eca5f4ac3fabb338f28c5b2c2c0a869`.  There
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
{"case_id": "fallow_rs_fallow__2365__f951395",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
