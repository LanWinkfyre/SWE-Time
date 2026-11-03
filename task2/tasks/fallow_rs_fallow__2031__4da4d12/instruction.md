# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
health: exclude mocked module edges from static test reachability

## Problem

Static coverage reachability follows an import into a module that Vitest replaces with `vi.mock()`.
The mocked module and its exports are therefore reported as test-covered even though the real module
is never executed by that test.

This also changes coverage-derived health severity when a wrapper test is added, which can make
stable health identities regress unexpectedly.

## Minimal reproduction

```ts
// src/dependency.ts
export const renderDependency = (): string => "real dependency";

// src/wrapper.ts
import { renderDependency } from "./dependency";

export const renderWrapper = (): string => renderDependency();

// src/wrapper.test.ts
import { describe, expect, it, vi } from "vitest";
import { renderWrapper } from "./wrapper";

vi.mock("./dependency", () => ({
  renderDependency: vi.fn<() => string>(() => "mocked dependency"),
}));

describe("renderWrapper", () => {
  it("uses the mock", () => {
    expect(renderWrapper()).toBe("mocked dependency");
  });
});
```

With `src/entry.ts` as the package entry, run:

```sh
fallow health --coverage-gaps --format json --quiet --no-cache
```

Fallow 3.9.1 reports three runtime files, two covered files, and only `src/entry.ts` as untested.
The two covered files are `src/wrapper.ts` and `src/dependency.ts`.

## Expected

The static coverage graph should treat the literal target of `vi.mock("./dependency")` as a mocked
edge for that test root. `src/wrapper.ts` is test-reachable, but `src/dependency.ts` is not covered
by this test.

The same likely applies to `jest.mock()` and `vi.doMock()` where the target is a static string.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `4da4d122e66be28e091fa1be9cb6d2b56de14889`.  There
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
{"case_id": "fallow_rs_fallow__2031__4da4d12",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
