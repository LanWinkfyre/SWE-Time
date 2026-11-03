# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
health: extend mock-aware test reachability to jest.mock, vi.doMock, and aliased vi bindings

Follow-up to #2031 / #2068, which shipped mock-aware static test reachability for the literal `import { vi } from "vitest"` binding with `vi.mock`/`vi.unmock` and statically proven closed factories.

Known under-detections that currently abstain toward the old covered behavior (a mocked module keeps its coverage credit):

- Aliased named imports: `import { vi as v } from "vitest"; v.mock(...)`
- Namespace imports: `import * as vitest from "vitest"; vitest.vi.mock(...)`
- `jest.mock` (Jest projects get no masking at all)
- `vi.doMock` (unhoisted, order-sensitive; needs its own semantics decision)
- Automock (`vi.mock` without a factory): currently abstains and keeps crediting coverage; Vitest evaluates the original for shape, so this needs an explicit decision rather than silent crediting

Each extension should reuse the span-provenance binding check and the abstain-by-default factory proof from #2068. All of these fail in the safe direction today (no false uncovered findings), so this is coverage-accuracy work, not a correctness bug.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `e054def1a0bcd1fec2cc3f5764cb523618a8a0ad`.  There
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
{"case_id": "fallow_rs_fallow__2082__e054def",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
