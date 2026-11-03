# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
unused-class-members: interface-typed property dispatch loses credit (ports-and-adapters DI)

Follow-up to #1858 / #1785, reported by @lukeramsden in https://github.com/fallow-rs/fallow/issues/1858#issuecomment-4968348915. Filing as its own issue since it is a distinct credit path (no factory or object-literal nesting involved) and #1858 (object-literal factory returns) is a separate fix that does not cover it.

### Summary

`unused-class-members` loses credit for a member reached through a property whose declared type is an **interface**, when the concrete class is an implementer of that interface (`implements`). This is the canonical ports-and-adapters / hexagonal DI shape (`deps.someRepository.someMethod()` where `deps` is an interface of interfaces), so it accounts for a large share of `unused-class-members` findings in hexagonal codebases.

### Reproduction (plain TS, 4 files, repros on 3.5.0)

```ts
// src/port.ts
export interface GreeterPort { greet(name: string): string; }
export interface Deps { greeter: GreeterPort; }

// src/adapter.ts
import type { GreeterPort } from "./port.js";
export class GreeterAdapter implements GreeterPort {
  greet(name: string): string { return `hi ${name}`; }
}

// src/index.ts (entry)
import { GreeterAdapter } from "./adapter.js";
import { useIt } from "./consumer.js";
export function run() { return useIt({ greeter: new GreeterAdapter() }); }

// src/consumer.ts
import type { Deps } from "./port.js";
export function useIt(deps: Deps) { return deps.greeter.greet("x"); }
```

```
fallow dead-code --unused-class-members
```

### Expected

No findings: `GreeterAdapter.greet` is reached via `deps.greeter.greet("x")` where `deps.greeter` is typed `GreeterPort` and `GreeterAdapter implements GreeterPort`.

### Actual (3.5.0)

`GreeterAdapter.greet` reported as an unused class member.

### What already works (nice progress since 2.x, per the reporter)

- Interface-typed **parameter**: `useIt(g: GreeterPort) { g.greet() }` with `useIt(new GreeterAdapter())` is credited.
- Abstract base class dispatch, cross-file, is credited.

### The gap

The remaining case is member access through a **property** whose declared type is an interface (`deps.greeter.greet()`), i.e. usage credit does not propagate from the interface member to the implementing class's member when the receiver's type is reached via an interface **property** hop rather than a parameter/variable type. The typed-property hop resolves the receiver to the interface, but the interface-to-implementer propagation that already covers the direct-parameter and inheritance cases is not applied to the property-hop terminal.

### Environment

- fallow 3.5.0 (also reproduced on 3.2.0 and 2.40.3)
- macOS arm64, node 24

Thanks @lukeramsden for the clean minimal reduction and the note that it dominates hexagonal-architecture findings.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `dde1979e027f33579e7f4a55251344d00925f20d`.  There
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
{"case_id": "fallow_rs_fallow__1863__dde1979",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
