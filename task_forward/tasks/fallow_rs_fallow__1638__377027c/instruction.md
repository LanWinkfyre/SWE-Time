# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
unused-class-members: false positives for framework-dispatched overrides and implicit toString() coercion

Split out from #1441. The factory/composable indirection case in #1441 is fixed; these two cases the reporter also flagged are separate extractor gaps and remain open.

`unused-class-members` can still false-flag a member when the only access is not an explicit `instance.member()` call the extractor can see:

### 1. Framework-dispatched override

A subclass overrides a method that the framework invokes by convention rather than through an explicit call site, e.g. `handleEvent` on an OpenLayers interaction subclass. There is no `instance.handleEvent()` in user code, so the override is reported as unused even though the framework calls it.

```ts
import PointerInteraction from 'ol/interaction/Pointer'

export class DragInteraction extends PointerInteraction {
  // Invoked by OpenLayers, never called explicitly in user code:
  handleEvent(evt: MapBrowserEvent): boolean {
    return super.handleEvent(evt)
  }
}
```

### 2. Implicit `toString()` coercion

A `toString()` invoked only through implicit string coercion (template literals, string concatenation, `String(x)`) has no explicit `x.toString()` call site and is reported as unused.

```ts
export class Money {
  toString() { return `$${this.amount}` }
}
const label = `Total: ${new Money(5)}` // implicit toString(), no explicit call
```

### Notes

Both share the "a real usage the extractor cannot see" shape with #1441, but neither is a type-tracing gap, so the #1441 factory/composable fix does not address them. Candidate directions: a known-framework-dispatched-method allowlist (heritage-scoped, like the existing Lit/Lexical lifecycle member handling) for case 1, and crediting `toString` when a class is used in a string-coercion position for case 2.

Reported by @Jerc92 in #1441 (offered to split these out).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `377027c5764a2cf11b79e9e9ac6b6a79321a7442`.  There
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
{"case_id": "fallow_rs_fallow__1638__377027c",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
